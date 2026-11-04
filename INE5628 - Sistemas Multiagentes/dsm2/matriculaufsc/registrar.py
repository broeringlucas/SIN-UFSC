"""Registrar: serviço determinístico (não é agente) e ponto único de *commit* do sistema.

Guarda o estado autoritativo de turmas, matrículas, pontos e calendários de professores/salas.
Todos os agentes decidem com crenças locais (possivelmente desatualizadas); nada vale até o
Registrar validar. Isso garante as invariantes I1–I7 mesmo com mensagens perdidas ou atrasadas.

Invariantes (verificadas por `invariants()`):
  I1  vagas ocupadas ≤ capacidade efetiva da turma
  I2  nenhum aluno tem dois horários sobrepostos
  I3  nenhuma sala tem dois horários sobrepostos (calculado a partir das turmas abertas)
  I4  nenhum professor tem dois horários sobrepostos, respeita disponibilidade e carga máxima
  I5  pré-requisitos cumpridos; nenhuma disciplina repetida ou já cursada; limite de disciplinas
  I6  pontos nunca negativos e conservação: saldo + gasto em matrículas ativas = pontos iniciais
  I7  só existem matrículas em turmas abertas

open_section é atômico: aplica professor, sala e estado da turma, ou não altera nada.
cancel_section reembolsa os pontos, libera professor e sala e é idempotente.
A capacidade efetiva da turma é o mínimo entre a da turma e a da sala; o roster guarda aluno -> preço pago.
RegistrarService processa os requests na ordem de mid e responde ao remetente.
"""

from __future__ import annotations

from .bus import MessageBus
from .messages import FAILURE, INFORM, REQUEST
from .model import Scenario
from .trace import TraceLogger

OPEN, PLANNED, CANCELLED = "OPEN", "PLANNED", "CANCELLED"


class SectionState:
    def __init__(self, d):
        self.d = d
        self.status = PLANNED
        self.prof: str | None = None
        self.room: str | None = None
        self.capacity = d.capacity
        self.roster: dict[str, int] = {}


class Registrar:
    def __init__(self, scenario: Scenario) -> None:
        self.courses = scenario.courses
        self.students = {s.sid: s for s in scenario.students}
        self.profs = {p.pid: p for p in scenario.professors}
        self.rooms = {r.rid: r for r in scenario.rooms}
        self.sections = {d.sid: SectionState(d) for d in scenario.sections}
        self.points = {s.sid: s.points for s in scenario.students}
        self.initial_points = dict(self.points)
        self.prof_avail = {p.pid: set(p.available) for p in scenario.professors}

    def enrolled_sections(self, student: str) -> list[str]:
        return sorted(sid for sid, s in self.sections.items() if student in s.roster)

    def enrolled_courses(self, student: str) -> set[str]:
        return {self.sections[sid].d.course for sid in self.enrolled_sections(student)}

    def schedule_slots(self, student: str) -> list[str]:
        return [x for sid in self.enrolled_sections(student) for x in self.sections[sid].d.slots]

    def seats_left(self, sid: str) -> int:
        s = self.sections[sid]
        return s.capacity - len(s.roster)

    def prof_hours(self, pid: str) -> int:
        return sum(len(s.d.slots) for s in self.sections.values() if s.status == OPEN and s.prof == pid)

    def open_sections(self) -> list[str]:
        return sorted(sid for sid, s in self.sections.items() if s.status == OPEN)

    def validate_enroll(self, student: str, sid: str, price: int = 0) -> list[str]:
        v: list[str] = []
        st, sec = self.students.get(student), self.sections.get(sid)
        if st is None or sec is None:
            return ["UNKNOWN"]
        if sec.status != OPEN:
            return ["SECTION_NOT_OPEN"]
        if student in sec.roster:
            return ["DUP_SECTION"]
        if len(sec.roster) >= sec.capacity:
            v.append("FULL")
        course = self.courses[sec.d.course]
        if course.code in st.completed or course.code in self.enrolled_courses(student):
            v.append("DUP_COURSE")
        if not set(course.prereqs) <= set(st.completed):
            v.append("PREREQ")
        if set(sec.d.slots) & set(self.schedule_slots(student)):
            v.append("TIME_CONFLICT")
        if len(self.enrolled_sections(student)) >= st.max_courses:
            v.append("MAX_LOAD")
        if price < 0 or price > self.points[student]:
            v.append("BUDGET")
        return v

    def commit_enroll(self, student: str, sid: str, price: int) -> tuple[bool, list[str]]:
        reasons = self.validate_enroll(student, sid, price)
        if reasons:
            return False, reasons
        self.sections[sid].roster[student] = price
        self.points[student] -= price
        return True, []

    def drop_enrollment(self, student: str, sid: str) -> int:
        sec = self.sections[sid]
        price = sec.roster.pop(student, 0)
        self.points[student] += price
        return price

    def check_open(self, sid: str, pid: str, rid: str, capacity: int) -> list[str]:
        v: list[str] = []
        sec, prof, room = self.sections.get(sid), self.profs.get(pid), self.rooms.get(rid)
        if sec is None or prof is None or room is None:
            return ["UNKNOWN"]
        slots = set(sec.d.slots)
        if sec.status == OPEN:
            v.append("ALREADY_OPEN")
        if sec.d.course not in prof.teaches:
            v.append("PROF_CANNOT_TEACH")
        if not slots <= self.prof_avail[pid]:
            v.append("PROF_UNAVAILABLE")
        for o in self.sections.values():
            if o.status != OPEN or o.d.sid == sid:
                continue
            if o.prof == pid and slots & set(o.d.slots):
                v.append("PROF_CONFLICT")
            if o.room == rid and slots & set(o.d.slots):
                v.append("ROOM_CONFLICT")
        if self.prof_hours(pid) + len(slots) > prof.max_hours:
            v.append("PROF_LOAD")
        if capacity < 1 or capacity > room.capacity or capacity > sec.d.capacity:
            v.append("ROOM_CAPACITY")
        return sorted(set(v))

    def open_section(self, sid: str, pid: str, rid: str, capacity: int) -> tuple[bool, list[str]]:
        reasons = self.check_open(sid, pid, rid, capacity)
        if reasons:
            return False, reasons
        sec = self.sections[sid]
        sec.status, sec.prof, sec.room, sec.capacity = OPEN, pid, rid, capacity
        sec.roster = {}
        return True, []

    def cancel_section(self, sid: str, block: dict | None = None) -> list[dict]:
        sec = self.sections[sid]
        affected = []
        for student in sorted(sec.roster):
            refund = self.drop_enrollment(student, sid)
            affected.append({"student": student, "refund": refund, "balance": self.points[student]})
        sec.roster = {}
        if sec.status == OPEN:
            sec.status = CANCELLED
        sec.prof = sec.room = None
        sec.capacity = sec.d.capacity
        if block:
            self.prof_avail[block["prof"]] -= set(block.get("slots", ()))
        return affected

    def invariants(self) -> list[str]:
        v: list[str] = []
        prof_slots: dict[tuple[str, str], str] = {}
        room_slots: dict[tuple[str, str], str] = {}
        for sid, s in sorted(self.sections.items()):
            if len(s.roster) > s.capacity:
                v.append(f"I1 {sid}: {len(s.roster)} matrículas > capacidade {s.capacity}")
            if s.status != OPEN and s.roster:
                v.append(f"I7 {sid}: matrículas em turma {s.status}")
            if s.status == OPEN:
                for x in s.d.slots:
                    for table, who, tag in ((prof_slots, s.prof, "I4 professor"), (room_slots, s.room, "I3 sala")):
                        key = (who, x)
                        if key in table:
                            v.append(f"{tag} {who} duplicado em {x}: {table[key]} e {sid}")
                        table[key] = sid
                    if x not in self.prof_avail[s.prof]:
                        v.append(f"I4 {sid}: professor {s.prof} indisponível em {x}")
        for pid, p in self.profs.items():
            if self.prof_hours(pid) > p.max_hours:
                v.append(f"I4 professor {pid} acima da carga máxima")
        for stu, prof in self.students.items():
            secs = self.enrolled_sections(stu)
            slots = [x for sid in secs for x in self.sections[sid].d.slots]
            if len(slots) != len(set(slots)):
                v.append(f"I2 aluno {stu}: conflito de horário")
            courses = [self.sections[sid].d.course for sid in secs]
            if len(courses) != len(set(courses)) or set(courses) & set(prof.completed):
                v.append(f"I5 aluno {stu}: disciplina repetida/já cursada")
            for c in courses:
                if not set(self.courses[c].prereqs) <= set(prof.completed):
                    v.append(f"I5 aluno {stu}: pré-requisito de {c} não cumprido")
            if len(secs) > prof.max_courses:
                v.append(f"I5 aluno {stu}: acima do limite de disciplinas")
            spent = sum(self.sections[sid].roster[stu] for sid in secs)
            if self.points[stu] < 0 or self.points[stu] + spent != self.initial_points[stu]:
                v.append(f"I6 aluno {stu}: pontos inconsistentes (saldo {self.points[stu]}, gasto {spent})")
        return v


class RegistrarService(Registrar):
    id = "registrar"

    def __init__(self, scenario: Scenario, trace: TraceLogger) -> None:
        super().__init__(scenario)
        self.trace = trace

    def step(self, tick: int, inbox, bus: MessageBus) -> None:
        for m in sorted(inbox, key=lambda m: m.mid):
            if m.protocol != "registrar" or m.performative != REQUEST:
                continue
            op, c = m.content["op"], m.content
            if op == "commit_enroll":
                ok, reasons = self.commit_enroll(c["student"], c["section"], c["price"])
                extra = {"student": c["student"], "section": c["section"], "price": c["price"]}
                if ok:
                    extra.update(balance=self.points[c["student"]], remaining=self.seats_left(c["section"]))
            elif op == "open_section":
                ok, reasons = self.open_section(c["section"], c["prof"], c["room"], c["capacity"])
                extra = {"section": c["section"], "prof": c["prof"], "room": c["room"], "capacity": c["capacity"]}
            elif op == "cancel_section":
                affected = self.cancel_section(c["section"], c.get("block"))
                ok, reasons = True, []
                extra = {"section": c["section"], "students": affected, "reason": c.get("reason", "")}
            else:
                ok, reasons, extra = False, ["UNKNOWN_OP"], {}
            self.trace.log(tick, "registrar", self.id, op=op, ok=ok, reasons=reasons, **extra)
            bus.send(tick, self.id, m.sender, INFORM if ok else FAILURE, "registrar", m.conv,
                     {"op": op, "ok": ok, "reasons": reasons, **extra})
