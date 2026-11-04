"""DepartamentoAgent (deliberativo): orquestra os dois protocolos da DSM1 como máquinas de estados.

section_opening (Contract Net + reserva em duas fases)         estados registrados em `fsm`
  Idle → AguardandoPropostas → Avaliando → ReservandoSala → ConfirmandoRegistrar → Aberta
                                    ↑            │ refuse/timeout: próxima sala (sem salas: libera professor)
                                    └────────────┘ falha no Registrar: libera sala (e professor) e tenta o próximo
  ConfirmandoRegistrar --timeout--> Revertendo (cancel_section idempotente) → próximo candidato
  Falha: demanda insuficiente | sem professor | sem proposta válida

  Consistência professor × sala × matrícula: nada é compromisso até o Registrar confirmar
  (professor e sala só têm reservas provisórias com TTL). Qualquer falha leva a cancel/reject
  explícito às reservas; se a mensagem de cancelamento se perder, o TTL as expira.

seat_auction (leilão selado, 1 por turma aberta e por rodada)
  Idle → AguardandoLances → Avaliando → Validando(Registrar) → Concluido | SemLanceValido
  Lances simultâneos: o departamento ordena (−lance, −prioridade, sorteio com semente) e pede ao Registrar
  o commit dos k primeiros, k = vagas; o Registrar serializa por mid. Se o Registrar acusa violação
  (conflito de horário surgido em outra turma, disciplina duplicada por lance-hedge, saldo, …) o
  departamento promove o próximo da fila (cascata, até `max_cascade`).

Resposta ou proposta tardia é ignorada e a reserva órfã é liberada. Turma cancelada: o departamento tenta reabri-la com outro professor.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from ..messages import (ACCEPT, AGREE, CANCEL, CFP, INFORM, PROPOSE, REFUSE, REJECT, REQUEST,
                        aid_dept, aid_prof, aid_room, aid_student)
from ..fsm import check
from ..model import Config, Scenario
from .base import Agent


@dataclass
class Opening:
    sid: str
    state: str = "Idle"
    expected: set = field(default_factory=set)
    proposals: dict = field(default_factory=dict)
    refused: dict = field(default_factory=dict)
    deadline: int = 0
    cands: list = field(default_factory=list)
    prof: str | None = None
    rooms: list = field(default_factory=list)
    room: str | None = None
    capacity: int = 0
    wait: int = 0


@dataclass
class Auction:
    sid: str
    rnd: int
    state: str = "Idle"
    cfp_tick: int = 0
    bids: dict = field(default_factory=dict)
    k: int = 0
    queue: list = field(default_factory=list)
    pending: dict = field(default_factory=dict)
    accepted: dict = field(default_factory=dict)
    rejected: dict = field(default_factory=dict)
    ranking: list = field(default_factory=list)
    uniform_price: int = 1
    attempts: int = 0


class Department(Agent):
    def __init__(self, dept: str, scenario: Scenario, env, trace, cfg: Config, seed: int = 0) -> None:
        super().__init__(aid_dept(dept), env, trace)
        self.dept, self.cfg, self.seed = dept, cfg, seed
        self.sections = {s.sid: s for s in scenario.sections if s.dept == dept}
        self.profs = {p.pid: p for p in scenario.professors if p.dept == dept}
        self.rooms = [r for r in scenario.rooms if r.dept == dept]
        self.student_profiles = {s.sid: s for s in scenario.students}
        self.courses = scenario.courses
        self.demand: dict[str, set] = {}
        self.op: dict[str, Opening] = {}
        self.excluded: dict[str, set] = {sid: set() for sid in self.sections}
        self.open_info: dict[str, dict] = {}
        self.cap_left: dict[str, int] = {}
        self.auctions: dict[str, Auction] = {}
        self.round = -1
        self.cfp_due: int | None = None
        self.board_dirty = False

    def go(self, proto: str, key: str, obj, new: str, why: str = "") -> None:
        check(proto, obj.state, new)
        self.log("fsm", protocol=proto, ref=key, frm=obj.state, to=new, why=why)
        obj.state = new

    def broadcast_students(self, perf, protocol, conv, content) -> None:
        for sid in sorted(self.student_profiles):
            self.send(aid_student(sid), perf, protocol, conv, content)

    def publish_board(self, removed=()) -> None:
        secs = [{"sid": sid, "course": self.sections[sid].course, "dept": self.dept,
                 "slots": list(self.sections[sid].slots), "capacity": self.open_info[sid]["capacity"],
                 "remaining": self.cap_left[sid]} for sid in sorted(self.open_info)]
        self.broadcast_students(INFORM, "board", f"board:{self.dept}:{self.tick}",
                                {"sections": secs, "removed": list(removed)})
        self.board_dirty = False

    def step(self, tick: int, inbox) -> None:
        self.tick = tick
        for m in sorted(inbox, key=lambda m: m.mid):
            self.on_message(m)
        if tick == self.cfg.open_start:
            for sid in sorted(self.sections):
                self.start_opening(sid)
        for sid in sorted(self.op):
            self.tick_opening(self.op[sid])
        starts = self.cfg.round_starts()
        if tick in starts:
            for a in list(self.auctions.values()):
                if a.state not in ("Concluido", "SemLanceValido", "Cancelado"):
                    self.conclude(a, forced=True)
            self.round = starts.index(tick)
            self.publish_board()
            self.cfp_due = tick + 1
        if self.cfp_due == tick:
            self.start_auctions()
            self.cfp_due = None
        for sid in sorted(self.auctions):
            self.tick_auction(self.auctions[sid])
        if self.board_dirty and tick >= self.cfg.first_round and self.round >= 0:
            self.publish_board()

    def on_message(self, m) -> None:
        c = m.content
        if m.protocol == "demand":
            self.demand.setdefault(c["course"], set()).add(c["student"])
        elif m.protocol == "section_opening":
            self.on_opening_msg(m)
        elif m.protocol == "room_reservation":
            self.on_room_msg(m)
        elif m.protocol == "registrar":
            self.on_registrar(m)
        elif m.protocol == "seat_auction":
            self.on_bid(m)
        elif m.protocol == "commitment":
            self.on_withdraw(m)

    def start_opening(self, sid: str) -> None:
        sd = self.sections[sid]
        o = self.op[sid] = Opening(sid)
        d = len(self.demand.get(sd.course, ()))
        earlier = sum(s.capacity for s in self.sections.values() if s.course == sd.course and s.sid < sid)
        ok = d >= sd.min_demand if earlier == 0 else d > earlier
        if not ok:
            self.go("section_opening", sid, o, "Falha", f"demanda insuficiente (demanda={d}, vagas já planejadas={earlier})")
            return
        targets = [pid for pid, p in sorted(self.profs.items())
                   if sd.course in p.teaches and pid not in self.excluded[sid]]
        if not targets:
            self.go("section_opening", sid, o, "Falha", "nenhum professor habilitado disponível")
            return
        o.expected, o.deadline = set(targets), self.tick + self.cfg.timeout
        for pid in targets:
            self.send(aid_prof(pid), CFP, "section_opening", f"open:{sid}",
                      {"section": sid, "course": sd.course, "slots": list(sd.slots)})
        self.go("section_opening", sid, o, "AguardandoPropostas", f"cfp a {len(targets)} professor(es); demanda={d}")

    def on_opening_msg(self, m) -> None:
        sid = m.content["section"]
        o = self.op.get(sid)
        pid = m.sender.split(":", 1)[1]
        if o is None or o.state != "AguardandoPropostas":
            if m.performative == PROPOSE:
                self.send(m.sender, REJECT, "section_opening", m.conv, {"section": sid, "reason": "tardia"})
            return
        if m.performative == PROPOSE:
            o.proposals[pid] = m.content["score"]
        elif m.performative == REFUSE:
            o.refused[pid] = m.content.get("reason", "")

    def tick_opening(self, o: Opening) -> None:
        if o.state == "AguardandoPropostas":
            if o.expected <= set(o.proposals) | set(o.refused) or self.tick >= o.deadline:
                self.go("section_opening", o.sid, o, "Avaliando",
                        f"{len(o.proposals)} proposta(s), {len(o.refused)} recusa(s)")
                o.cands = sorted(((-s, p) for p, s in o.proposals.items()))
                self.next_prof(o)
        elif o.state == "ReservandoSala" and self.tick >= o.wait:
            self.log("note", text=f"timeout da sala {o.room} em {o.sid}")
            self.send(aid_room(o.room), CANCEL, "room_reservation", f"open:{o.sid}", {"section": o.sid})
            self.next_room(o)
        elif o.state == "ConfirmandoRegistrar" and self.tick >= o.wait:
            self.log("note", text=f"timeout do Registrar em {o.sid}: rollback idempotente")
            self.release(o, prof=True, room=True)
            self.send("registrar", REQUEST, "registrar", f"open:{o.sid}", {"op": "cancel_section", "section": o.sid})
            o.wait = self.tick + self.cfg.timeout
            self.go("section_opening", o.sid, o, "Revertendo", "sem resposta do Registrar")
        elif o.state == "Revertendo" and self.tick >= o.wait:
            self.next_prof(o)

    def release(self, o: Opening, prof: bool = False, room: bool = False) -> None:
        if room and o.room:
            self.send(aid_room(o.room), CANCEL, "room_reservation", f"open:{o.sid}", {"section": o.sid})
        if prof and o.prof:
            self.send(aid_prof(o.prof), CANCEL, "section_opening", f"open:{o.sid}", {"section": o.sid})

    def next_prof(self, o: Opening) -> None:
        if not o.cands:
            for pid in sorted(o.proposals):
                self.send(aid_prof(pid), REJECT, "section_opening", f"open:{o.sid}", {"section": o.sid, "reason": "turma não aberta"})
            self.go("section_opening", o.sid, o, "Falha", "sem proposta válida")
            return
        _, pid = o.cands.pop(0)
        o.prof, o.room = pid, None
        sd = self.sections[o.sid]
        o.rooms = sorted(self.rooms, key=lambda r: (0, r.capacity, r.rid) if r.capacity >= sd.capacity else (1, -r.capacity, r.rid))
        self.send(aid_prof(pid), ACCEPT, "section_opening", f"open:{o.sid}", {"section": o.sid})
        self.go("section_opening", o.sid, o, "Avaliando", f"professor escolhido: {pid}")
        self.next_room(o)

    def next_room(self, o: Opening) -> None:
        sd = self.sections[o.sid]
        if not o.rooms:
            self.release(o, prof=True)
            self.go("section_opening", o.sid, o, "Avaliando", f"sem sala para {o.prof}: libera professor")
            self.next_prof(o)
            return
        r = o.rooms.pop(0)
        o.room, o.capacity = r.rid, min(sd.capacity, r.capacity)
        self.send(aid_room(r.rid), REQUEST, "room_reservation", f"open:{o.sid}",
                  {"section": o.sid, "slots": list(sd.slots), "capacity": o.capacity})
        o.wait = self.tick + self.cfg.timeout
        self.go("section_opening", o.sid, o, "ReservandoSala", f"request à sala {r.rid} (capacidade efetiva {o.capacity})")

    def on_room_msg(self, m) -> None:
        sid, rid = m.content["section"], m.content["room"]
        o = self.op.get(sid)
        current = o is not None and o.state == "ReservandoSala" and o.room == rid
        if m.performative == AGREE:
            if not current:
                self.send(m.sender, CANCEL, "room_reservation", m.conv, {"section": sid})
                return
            self.send("registrar", REQUEST, "registrar", f"open:{sid}",
                      {"op": "open_section", "section": sid, "prof": o.prof, "room": o.room, "capacity": o.capacity})
            o.wait = self.tick + self.cfg.timeout
            self.go("section_opening", sid, o, "ConfirmandoRegistrar", f"sala {rid} reservada; pedindo commit ao Registrar")
        elif m.performative == REFUSE and current:
            self.next_room(o)

    def on_registrar(self, m) -> None:
        c = m.content
        if c["op"] == "commit_enroll":
            self.on_commit_reply(m)
        elif c["op"] == "open_section":
            o = self.op.get(c["section"])
            if o is None or o.state != "ConfirmandoRegistrar":
                return
            if c["ok"]:
                self.opened(o)
            else:
                self.release(o, room=True)
                self.log("note", text=f"Registrar recusou abertura de {o.sid}: {c['reasons']}")
                if any(r.startswith("PROF_") for r in c["reasons"]):
                    self.release(o, prof=True)
                    self.go("section_opening", o.sid, o, "Avaliando", f"Registrar: {c['reasons']}")
                    self.next_prof(o)
                else:
                    self.go("section_opening", o.sid, o, "Avaliando", f"Registrar: {c['reasons']}")
                    self.next_room(o)
        elif c["op"] == "cancel_section":
            if m.conv.startswith("open:"):
                o = self.op.get(c["section"])
                if o is not None and o.state == "Revertendo":
                    self.next_prof(o)
            elif m.conv.startswith("cancel:"):
                self.on_cancel_done(m)

    def opened(self, o: Opening) -> None:
        sid = o.sid
        self.open_info[sid] = {"prof": o.prof, "room": o.room, "capacity": o.capacity}
        self.cap_left[sid] = o.capacity
        self.send(aid_prof(o.prof), INFORM, "section_opening", f"open:{sid}", {"section": sid, "slots": list(self.sections[sid].slots)})
        self.send(aid_room(o.room), INFORM, "room_reservation", f"open:{sid}", {"section": sid})
        for pid in sorted(o.proposals):
            if pid != o.prof:
                self.send(aid_prof(pid), REJECT, "section_opening", f"open:{sid}", {"section": sid, "reason": "outro professor escolhido"})
        self.board_dirty = True
        self.go("section_opening", sid, o, "Aberta", f"prof={o.prof} sala={o.room} vagas={o.capacity}")

    def on_withdraw(self, m) -> None:
        sid, pid = m.content["section"], m.content["prof"]
        if sid not in self.open_info:
            return
        self.excluded[sid].add(pid)
        self.send("registrar", REQUEST, "registrar", f"cancel:{sid}",
                  {"op": "cancel_section", "section": sid, "reason": "professor indisponível",
                   "block": {"prof": pid, "slots": m.content["slots"]}})
        self.cancel_auction(sid, "professor se retirou")

    def cancel_auction(self, sid: str, why: str) -> None:
        a = self.auctions.get(sid)
        if a and a.state in ("AguardandoLances", "Validando"):
            self.go("seat_auction", f"{sid}:{a.rnd}", a, "Cancelado", why)

    def on_cancel_done(self, m) -> None:
        c = m.content
        sid = c["section"]
        info = self.open_info.pop(sid, None)
        self.cap_left.pop(sid, None)
        self.cancel_auction(sid, "turma cancelada")
        for s in c["students"]:
            self.send(aid_student(s["student"]), INFORM, "enrollment", f"cancel:{sid}",
                      {"section": sid, "refund": s["refund"], "balance": s["balance"], "reason": c["reason"]})
        if info:
            self.send(aid_room(info["room"]), CANCEL, "room_reservation", f"cancel:{sid}", {"section": sid})
        self.publish_board(removed=[sid])
        self.start_opening(sid)

    def start_auctions(self) -> None:
        for sid in sorted(self.open_info):
            if self.cap_left.get(sid, 0) <= 0:
                continue
            a = self.auctions[sid] = Auction(sid, self.round, cfp_tick=self.tick, k=self.cap_left[sid])
            self.broadcast_students(CFP, "seat_auction", f"auc:{sid}:{self.round}",
                                    {"section": sid, "round": self.round, "remaining": self.cap_left[sid],
                                     "reserve": self.cfg.reserve})
            self.go("seat_auction", f"{sid}:{self.round}", a, "AguardandoLances", f"cfp a todos; vagas={a.k}")

    def on_bid(self, m) -> None:
        c = m.content
        a = self.auctions.get(c["section"])
        student = m.sender.split(":", 1)[1]
        rnd = int(m.conv.rsplit(":", 1)[1])
        if a is None or a.rnd != rnd or a.state != "AguardandoLances":
            if m.performative == PROPOSE:
                self.log("note", text=f"lance tardio de {student} em {c['section']} ignorado")
                self.send(m.sender, REJECT, "seat_auction", m.conv, {"section": c["section"], "reason": "lance tardio"})
            return
        if m.performative == PROPOSE:
            a.bids[student] = c["bid"]

    def tick_auction(self, a: Auction) -> None:
        if a.state == "AguardandoLances" and self.tick >= a.cfp_tick + 2:
            self.evaluate(a)

    def evaluate(self, a: Auction) -> None:
        self.go("seat_auction", f"{a.sid}:{a.rnd}", a, "Avaliando", f"{len(a.bids)} lance(s) recebido(s)")
        valid = {s: b for s, b in a.bids.items() if b >= self.cfg.reserve}
        if not valid:
            self.go("seat_auction", f"{a.sid}:{a.rnd}", a, "SemLanceValido", "nenhum lance válido")
            return
        rng = random.Random(f"{self.seed}:{a.sid}:{a.rnd}")
        tie = {s: rng.random() for s in sorted(valid)}
        a.ranking = sorted(valid.items(), key=lambda sb: (-sb[1], -self.student_profiles[sb[0]].priority, tie[sb[0]]))
        a.k = self.cap_left[a.sid]
        losing = a.ranking[a.k][1] if len(a.ranking) > a.k else self.cfg.reserve
        a.uniform_price = max(self.cfg.reserve, losing)
        a.queue = list(a.ranking[a.k:])
        self.go("seat_auction", f"{a.sid}:{a.rnd}", a, "Validando",
                f"ranking={[(s, b) for s, b in a.ranking]}; k={a.k}; preço={self.cfg.pricing}")
        for s, b in a.ranking[:a.k]:
            self.request_commit(a, s, b)

    def request_commit(self, a: Auction, student: str, bid: int) -> None:
        price = bid if self.cfg.pricing == "first" else min(bid, a.uniform_price)
        a.pending[student] = price
        self.send("registrar", REQUEST, "registrar", f"auc:{a.sid}:{a.rnd}",
                  {"op": "commit_enroll", "student": student, "section": a.sid, "price": price})

    def on_commit_reply(self, m) -> None:
        c = m.content
        a = self.auctions.get(c["section"])
        if a is None or m.conv != f"auc:{a.sid}:{a.rnd}" or a.state != "Validando":
            return
        a.pending.pop(c["student"], None)
        if c["ok"]:
            a.accepted[c["student"]] = (c["price"], c["balance"])
            self.cap_left[a.sid] = c["remaining"]
        else:
            a.rejected[c["student"]] = "violação:" + c["reasons"][0]
            a.attempts += 1
            self.log("note", text=f"Registrar recusou {c['student']} em {a.sid}: {c['reasons']} (cascata)")
        need = a.k - len(a.accepted) - len(a.pending)
        while need > 0 and a.queue and a.attempts <= self.cfg.max_cascade:
            s, b = a.queue.pop(0)
            self.request_commit(a, s, b)
            need -= 1
        if not a.pending:
            self.conclude(a)

    def conclude(self, a: Auction, forced: bool = False) -> None:
        for s, (price, balance) in sorted(a.accepted.items()):
            self.send(aid_student(s), ACCEPT, "seat_auction", f"auc:{a.sid}:{a.rnd}",
                      {"section": a.sid, "price": price, "balance": balance, "round": a.rnd})
        for s, _ in a.ranking:
            if s not in a.accepted:
                self.send(aid_student(s), REJECT, "seat_auction", f"auc:{a.sid}:{a.rnd}",
                          {"section": a.sid, "reason": a.rejected.get(s, "outbid"), "round": a.rnd})
        self.go("seat_auction", f"{a.sid}:{a.rnd}", a, "Concluido",
                f"vencedores={sorted(a.accepted)}" + (" (encerrado por tempo)" if forced else ""))
