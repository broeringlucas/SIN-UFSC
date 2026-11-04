"""AlunoAgent (BDI): quer uma grade satisfatória e disputa vagas com pontos.

Desejos:  obtain:<disciplina> (obrigatórias pesam 0,60/n; eletivas 0,15/n — os mesmos pesos da utilidade).
Crenças:  points, enrolled, board_published, sec:<turma> (oferta publicada), result:<turma>, demand_sent:<disc>.
Planos:   signal_demand  — avisa o departamento da demanda enquanto a oferta ainda não foi publicada
          bid_single     — lance na melhor turma sem horário indesejado
          bid_hedge      — obrigatória com ≥2 turmas boas: lance na 1ª (cheio) e na 2ª (metade)
          bid_tolerate   — só há turmas em horário indesejado: aceita, com lance 30% menor

Turmas candidatas de uma disciplina: ordenadas pelo nº de slots indesejados; ficam de fora as cheias, as que
conflitam com a grade ou com outra intenção e as que já rejeitaram um lance do aluno neste período.
"""

from __future__ import annotations

from ..messages import ACCEPT, CFP, INFORM, PROPOSE, REFUSE, REJECT, aid_dept, aid_student
from ..model import Scenario, StudentProfile
from ..utility import W_ELEC, W_REQ
from .bdi import BDIAgent, Desire, Intention, Plan


class Student(BDIAgent):
    def __init__(self, profile: StudentProfile, scenario: Scenario, env, trace) -> None:
        super().__init__(aid_student(profile.sid), env, trace, [SignalDemand(), BidSingle(), BidHedge(), BidTolerate()])
        self.p = profile
        self.courses = scenario.courses
        self.cfps: list = []
        self.beliefs.set("points", profile.points, "init")
        self.beliefs.set("enrolled", {}, "init")
        self.beliefs.set("board_published", False, "init")
        req = [c for c in profile.required if c not in profile.completed]
        ele = [c for c in profile.electives if c not in profile.completed]
        self._wanted = [(c, True, W_REQ / len(req)) for c in req] + [(c, False, W_ELEC / len(ele)) for c in ele]

    def enrolled(self) -> dict:
        return self.beliefs.get("enrolled", {}) or {}

    def enrolled_courses(self) -> set[str]:
        return {v["course"] for v in self.enrolled().values()}

    def enrolled_slots(self) -> set[str]:
        return {x for v in self.enrolled().values() for x in v["slots"]}

    def claimed_slots(self, except_desire: Desire) -> set[str]:
        out: set[str] = set()
        for it in self.active_intentions():
            if it.desire is except_desire:
                continue
            for sid in it.state.get("targets", []):
                sec = self.beliefs.get(f"sec:{sid}")
                if sec:
                    out |= set(sec["slots"])
        return out

    def candidates(self, desire: Desire) -> list[tuple[int, str]]:
        course = desire.params["course"]
        busy = self.enrolled_slots() | self.claimed_slots(desire)
        out = []
        for key in self.beliefs.keys_with("sec:"):
            sid, sec = key[4:], self.beliefs.get(key)
            if sec["course"] != course or sec["remaining"] <= 0:
                continue
            if self.beliefs.get(f"result:{sid}") is not None:
                continue
            if set(sec["slots"]) & busy:
                continue
            out.append((len(set(sec["slots"]) & self.p.undesired_slots), sid))
        return sorted(out)

    def bid_amount(self, desire: Desire, factor: float = 1.0) -> int:
        pts = self.beliefs.get("points")
        if pts <= 0:
            return 0
        active = [d for d in self.desires.values() if d.status == "active"]
        total = sum(d.priority for d in active) or desire.priority
        return min(pts, max(1, int(pts * desire.priority / total * factor)))

    def perceive(self, inbox) -> None:
        self.cfps = []
        for m in inbox:
            c = m.content
            if m.protocol == "board":
                self.beliefs.set("board_published", True, "oferta publicada")
                for s in c["sections"]:
                    self.beliefs.set(f"sec:{s['sid']}", {"course": s["course"], "slots": list(s["slots"]),
                                                         "remaining": s["remaining"], "dept": s["dept"]}, "board")
                for sid in c.get("removed", []):
                    self.beliefs.set(f"sec:{sid}", None, "turma removida da oferta")
            elif m.protocol == "seat_auction":
                if m.performative == CFP:
                    self.cfps.append(m)
                elif m.performative == ACCEPT:
                    sec = self.beliefs.get(f"sec:{c['section']}")
                    enr = dict(self.enrolled())
                    enr[c["section"]] = {"course": sec["course"], "slots": sec["slots"]}
                    self.beliefs.set("enrolled", enr, f"venceu leilão de {c['section']} pagando {c['price']}")
                    self.beliefs.set("points", c["balance"], "pontos debitados")
                    self.beliefs.set(f"result:{c['section']}", "won", "resultado do leilão")
                elif m.performative == REJECT:
                    self.beliefs.set(f"result:{c['section']}", c["reason"], "resultado do leilão")
            elif m.protocol == "enrollment" and m.performative == INFORM:
                enr = dict(self.enrolled())
                enr.pop(c["section"], None)
                self.beliefs.set("enrolled", enr, f"matrícula cancelada: {c['reason']}")
                self.beliefs.set("points", c["balance"], f"reembolso de {c['refund']} pontos")
                self.beliefs.set(f"result:{c['section']}", None, "matrícula cancelada")

    def update_desires(self) -> None:
        for course, required, weight in self._wanted:
            name = f"obtain:{course}"
            self.add_desire(Desire(name, "obtain", weight, {"course": course, "required": required}))
            d = self.desires[name]
            if course in self.enrolled_courses():
                self.set_desire_status(d, "achieved", "disciplina obtida")
            elif d.status == "achieved":
                self.set_desire_status(d, "active", "matrícula perdida: desejo reativado")

    def act(self) -> None:
        super().act()
        self.cfps = []


def _alive(agent: Student, it: Intention) -> list[str]:
    out = []
    for sid in it.state["targets"]:
        sec = agent.beliefs.get(f"sec:{sid}")
        if (agent.beliefs.get(f"result:{sid}") is None and sec and sec["remaining"] > 0
                and not set(sec["slots"]) & agent.enrolled_slots()):
            out.append(sid)
    return out


class SignalDemand(Plan):
    name = "signal_demand"
    kinds = ("obtain",)

    def applicable(self, agent, d):
        return not agent.beliefs.get("board_published") and not agent.beliefs.get(f"demand_sent:{d.params['course']}")

    def score(self, agent, d):
        return 1.0

    def start(self, agent, d):
        return {"targets": []}, ("board_published",)

    def execute(self, agent, it):
        c = it.desire.params["course"]
        if not agent.beliefs.get(f"demand_sent:{c}"):
            dept = agent.courses[c].dept
            agent.send(aid_dept(dept), INFORM, "demand", f"demand:{c}", {"course": c, "student": agent.p.sid})
            agent.beliefs.set(f"demand_sent:{c}", True, "interesse enviado ao departamento")

    def valid(self, agent, it):
        return not agent.beliefs.get("board_published")


class _Bid(Plan):
    kinds = ("obtain",)
    watch_extra = ("enrolled",)

    def pick(self, agent, d) -> list[str]:
        return []

    def applicable(self, agent, d):
        return bool(self.pick(agent, d))

    def start(self, agent, d):
        targets = self.pick(agent, d)
        watch = tuple(f"sec:{s}" for s in targets) + tuple(f"result:{s}" for s in targets) + self.watch_extra
        return {"targets": targets, "answered": set(), "factor": getattr(self, "factor", 1.0)}, watch

    def valid(self, agent, it):
        return bool(_alive(agent, it))

    def achieved(self, agent, it):
        return it.desire.params["course"] in agent.enrolled_courses()

    def execute(self, agent, it):
        course = it.desire.params["course"]
        alive = _alive(agent, it)
        for m in agent.cfps:
            sid, rnd = m.content["section"], m.content["round"]
            if (sid, rnd) in it.state["answered"]:
                continue
            if sid in alive:
                rank = alive.index(sid)
                factor = it.state["factor"] * (0.5 if rank > 0 else 1.0)
                amount = agent.bid_amount(it.desire, factor)
                it.state["answered"].add((sid, rnd))
                if amount > 0:
                    agent.send(m.sender, PROPOSE, "seat_auction", m.conv, {"section": sid, "bid": amount, "round": rnd})
                else:
                    agent.send(m.sender, REFUSE, "seat_auction", m.conv, {"section": sid, "reason": "sem pontos"})
            else:
                sec = agent.beliefs.get(f"sec:{sid}")
                if sec and sec["course"] == course:
                    it.state["answered"].add((sid, rnd))
                    agent.send(m.sender, REFUSE, "seat_auction", m.conv, {"section": sid, "reason": "preferiu outra turma"})


class BidSingle(_Bid):
    name = "bid_single"

    def pick(self, agent, d):
        good = [sid for bad, sid in agent.candidates(d) if bad == 0]
        return good[:1]


class BidHedge(_Bid):
    name = "bid_hedge"

    def score(self, agent, d):
        return 1.5

    def pick(self, agent, d):
        if not d.params["required"]:
            return []
        good = [sid for bad, sid in agent.candidates(d) if bad == 0]
        return good[:2] if len(good) >= 2 else []


class BidTolerate(_Bid):
    name = "bid_tolerate"
    factor = 0.7

    def score(self, agent, d):
        return 0.6

    def pick(self, agent, d):
        cands = agent.candidates(d)
        if not cands or cands[0][0] == 0:
            return []
        return [cands[0][1]]
