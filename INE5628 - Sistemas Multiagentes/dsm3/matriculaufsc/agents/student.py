"""AlunoAgent (BDI): quer uma grade satisfatória e disputa vagas com pontos.

Desejos:  obtain:<disciplina> (obrigatórias pesam 0,60/n; eletivas 0,15/n — os mesmos pesos da utilidade).
Crenças:  points, enrolled, board_published, sec:<turma> (oferta publicada), result:<turma>, demand_sent:<disc>.
Troca:    desejo improve:<disciplina> (turma com horário indesejado e outra, cheia, melhor) → plano propose_swap;
          desejo swap_reply:<conv> (departamento consulta se aceito trocar) → planos accept_swap | decline_swap
Crenças desatualizadas: ao receber convite de leilão de turma que não conhece (quadro perdido), desejo resync:<dept>
          → plano resync pede o quadro ao departamento (protocolo sync)
Planos:   signal_demand  — avisa o departamento da demanda enquanto a oferta ainda não foi publicada
          bid_single     — lance na melhor turma sem horário indesejado
          bid_hedge      — obrigatória com ≥2 turmas boas: lance na 1ª (cheio) e na 2ª (metade)
          bid_tolerate   — só há turmas em horário indesejado: aceita, com lance 30% menor

Turmas candidatas de uma disciplina: ordenadas pelo nº de slots indesejados; ficam de fora as cheias, as que
conflitam com a grade ou com outra intenção e as que já rejeitaram um lance do aluno neste período.
"""

from __future__ import annotations

from .. import contracts
from ..messages import ACCEPT, AGREE, CFP, INFORM, PROPOSE, REFUSE, REJECT, REQUEST, aid_dept, aid_student
from ..model import Config, Scenario, StudentProfile
from ..utility import W_ELEC, W_REQ
from .bdi import BDIAgent, Desire, Intention, Plan


BOARD_ROW = {"sid": "str", "course": "str", "dept": "str", "slots": "strs", "capacity": "nat", "remaining": "nat"}


class Student(BDIAgent):
    def __init__(self, profile: StudentProfile, scenario: Scenario, env, trace, cfg: Config | None = None) -> None:
        super().__init__(aid_student(profile.sid), env, trace,
                         [SignalDemand(), BidSingle(), BidHedge(), BidTolerate(),
                          ProposeSwap(), AcceptSwap(), DeclineSwap(), Resync()])
        self.cfg = cfg or Config()
        self.swap_n = 0
        self.stale_cfps: list = []
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
                good = [s for s in c["sections"] if isinstance(s, dict) and m.sender == aid_dept(str(s.get("dept")))
                        and not contracts.check_fields(s, BOARD_ROW)]
                if len(good) != len(c["sections"]):
                    self.log("msg_denied", mid=m.mid, sender=m.sender, why="quadro com linhas inválidas ou de outro dept")
                self.beliefs.set("board_published", True, "oferta publicada")
                for s in good:
                    self.beliefs.set(f"sec:{s['sid']}", {"course": s["course"], "slots": list(s["slots"]),
                                                         "remaining": s["remaining"], "dept": s["dept"]}, "board")
                for sid in c.get("removed", []):
                    self.beliefs.set(f"sec:{sid}", None, "turma removida da oferta")
            elif m.protocol == "seat_swap":
                self.on_swap(m)
            elif (m.protocol == "seat_auction" and m.performative == CFP
                  and self.beliefs.get(f"sec:{c['section']}") is None):
                self.suspect_stale(m)       # convite de turma que meu quadro desconhece: peço o quadro atualizado
                self.stale_cfps.append(m)   # e guardo o convite: se o quadro chegar a tempo, ainda dou o lance
            elif m.protocol in ("seat_auction", "enrollment") and not self.from_owner(m):
                self.log("msg_denied", mid=m.mid, sender=m.sender, why="leilão/matrícula de quem não é o dept da turma")
            elif m.protocol == "seat_auction":
                if m.performative == CFP:
                    self.cfps.append(m)
                elif m.performative == ACCEPT:
                    sec = self.beliefs.get(f"sec:{c['section']}")
                    if sec is None:
                        continue
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

    def board_ready(self) -> bool:
        return bool(self.beliefs.get("board_published"))

    def bad(self, sid: str) -> int:
        sec = self.beliefs.get(f"sec:{sid}")
        return len(set(sec["slots"]) & self.p.undesired_slots) if sec else 0

    def section_of(self, course: str) -> str | None:
        for sid, v in self.enrolled().items():
            if v["course"] == course:
                return sid
        return None

    def swap_candidate(self, course: str) -> str | None:
        """Turma cheia, da mesma disciplina, estritamente melhor (menos horários indesejados) e sem conflito."""
        cur = self.section_of(course)
        if cur is None:
            return None
        cur_slots = set(self.enrolled()[cur]["slots"])
        others = self.enrolled_slots() - cur_slots
        out = []
        for key in self.beliefs.keys_with("sec:"):
            sid, sec = key[4:], self.beliefs.get(key)
            if (sid == cur or sec["course"] != course or sec["remaining"] > 0 or self.beliefs.get(f"swap_failed:{sid}")
                    or set(sec["slots"]) & others):
                continue
            if self.bad(sid) < self.bad(cur):
                out.append((self.bad(sid), sid))
        return min(out)[1] if out else None

    def swap_acceptable(self, receive: str, release: str) -> str | None:
        """None se aceito a troca (recebo `receive`, cedo `release`); senão o motivo da recusa."""
        enr = self.enrolled()
        if release not in enr:
            return "não estou na turma consultada"
        sec_in = self.beliefs.get(f"sec:{receive}")
        if sec_in is None:
            return "não conheço a turma oferecida"
        if set(sec_in["slots"]) & (self.enrolled_slots() - set(enr[release]["slots"])):
            return "conflito de horário com minha grade"
        if self.bad(receive) > self.bad(release):
            return "pioraria meus horários"
        return None

    def from_owner(self, m) -> bool:
        """Leilão e cancelamento só valem se vierem do departamento dono da turma (conforme o quadro publicado)."""
        sec = self.beliefs.get(f"sec:{m.content['section']}")
        return bool(sec) and m.sender == aid_dept(sec["dept"])

    def revisit_stale_cfps(self) -> None:
        """Convites guardados: se o quadro corrigido chegou e o leilão ainda aceita lances, responde ao convite."""
        keep = []
        for m in self.stale_cfps:
            in_time = self.tick + 1 <= m.tick + self.cfg.bid_window   # lance enviado agora chega antes do fechamento
            if not in_time:
                continue
            if self.beliefs.get(f"sec:{m.content['section']}") is not None:
                self.cfps.append(m)
                self.log("note", text=f"quadro recuperado a tempo: respondo ao convite de {m.content['section']}")
            else:
                keep.append(m)
        self.stale_cfps = keep

    def suspect_stale(self, m) -> None:
        """Convite de leilão de turma ausente do meu quadro: minhas crenças estão desatualizadas."""
        dept = m.sender.split(":", 1)[1]
        last = self.beliefs.get(f"sync_at:{dept}")
        if self.cfg.sync and (last is None or self.tick - last >= 6):
            self.beliefs.set(f"sync_at:{dept}", self.tick, "convite de turma desconhecida: quadro desatualizado")
            self.add_desire(Desire(f"resync:{dept}@{self.tick}", "resync", 1.8, {"dept": dept}))

    def on_swap(self, m) -> None:
        c = m.content
        if m.performative == CFP:
            sec = self.beliefs.get(f"sec:{c['release']}") or self.beliefs.get(f"sec:{c['receive']}")
            if not sec or m.sender != aid_dept(sec["dept"]):
                self.log("msg_denied", mid=m.mid, sender=m.sender, why="consulta de troca de quem não é o dept da turma")
                return
            self.add_desire(Desire(f"swap_reply:{m.conv}", "swap_reply", 2.5,
                                   {"conv": m.conv, "to": m.sender, "receive": c["receive"], "release": c["release"]}))
        elif m.performative == INFORM:
            sec = self.beliefs.get(f"sec:{c['old']}")
            if not sec or m.sender != aid_dept(sec["dept"]):
                self.log("msg_denied", mid=m.mid, sender=m.sender, why="resultado de troca de quem não é o dept da turma")
                return
            course = sec["course"]
            self.beliefs.set(f"swap_pending:{course}", None, "resposta do departamento recebida")
            if c["outcome"] == "done":
                new = self.beliefs.get(f"sec:{c['new']}")
                if new is None or c["old"] not in self.enrolled():
                    return
                enr = dict(self.enrolled())
                enr.pop(c["old"])
                enr[c["new"]] = {"course": new["course"], "slots": list(new["slots"])}
                self.beliefs.set("enrolled", enr, f"troca concluída: {c['old']} -> {c['new']}")
                self.beliefs.set(f"result:{c['old']}", None, "turma cedida na troca")
                self.beliefs.set(f"result:{c['new']}", "won", "turma recebida na troca")
            else:
                self.beliefs.set(f"swap_failed:{c['new']}", c.get("reason", "falhou"), "troca recusada")

    def update_desires(self) -> None:
        self.revisit_stale_cfps()
        if self.cfg.swaps:
            for course in sorted({v["course"] for v in self.enrolled().values()}):
                name = f"improve:{course}"
                cur = self.section_of(course)
                if self.bad(cur) > 0:
                    self.add_desire(Desire(name, "improve", 0.3, {"course": course}))
                    if self.desires[name].status == "achieved":
                        self.set_desire_status(self.desires[name], "active", "nova turma com horário indesejado")
        for name, d in list(self.desires.items()):
            if d.kind == "improve":
                cur = self.section_of(d.params["course"])
                if cur is None or self.bad(cur) == 0:
                    self.set_desire_status(d, "achieved", "turma atual sem horário indesejado")
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


class ProposeSwap(Plan):
    """Pede ao departamento para trocar minha turma ruim pela turma cheia melhor, com quem estiver nela."""
    name = "propose_swap"
    kinds = ("improve",)

    def applicable(self, agent, d):
        course = d.params["course"]
        return (agent.cfg.swaps and agent.board_ready() and not agent.beliefs.get(f"swap_pending:{course}")
                and agent.swap_candidate(course) is not None)

    def start(self, agent, d):
        want = agent.swap_candidate(d.params["course"])
        return {"want": want, "give": agent.section_of(d.params["course"]), "sent": False}, \
            ("enrolled", "swap_failed:", "swap_pending:")

    def execute(self, agent, it):
        if it.state["sent"]:
            return
        it.state["sent"] = True
        give, want = it.state["give"], it.state["want"]
        agent.swap_n += 1
        conv = f"swap:{agent.p.sid}:{give}:{want}:{agent.swap_n}"
        dept = agent.beliefs.get(f"sec:{want}")["dept"]
        if agent.send(aid_dept(dept), REQUEST, "seat_swap", conv, {"give": give, "want": want}):
            agent.beliefs.set(f"swap_pending:{it.desire.params['course']}", conv, "pedido de troca enviado")

    def valid(self, agent, it):
        course = it.desire.params["course"]
        return agent.section_of(course) == it.state["give"] and bool(agent.beliefs.get(f"swap_pending:{course}"))

    def achieved(self, agent, it):
        return agent.section_of(it.desire.params["course"]) == it.state["want"]


class AcceptSwap(Plan):
    name = "accept_swap"
    kinds = ("swap_reply",)

    def applicable(self, agent, d):
        return agent.swap_acceptable(d.params["receive"], d.params["release"]) is None

    def score(self, agent, d):
        return 1.0

    def start(self, agent, d):
        return {"sent": False}, ()

    def execute(self, agent, it):
        if it.state["sent"]:
            return
        it.state["sent"] = True
        d = it.desire
        agent.send(d.params["to"], AGREE, "seat_swap", d.params["conv"],
                   {"receive": d.params["receive"], "release": d.params["release"]})
        agent.set_desire_status(d, "achieved", "aceite enviado")

    def achieved(self, agent, it):
        return it.state["sent"]


class DeclineSwap(Plan):
    name = "decline_swap"
    kinds = ("swap_reply",)

    def applicable(self, agent, d):
        return True

    def score(self, agent, d):
        return 0.1

    def start(self, agent, d):
        return {"sent": False}, ()

    def execute(self, agent, it):
        if it.state["sent"]:
            return
        it.state["sent"] = True
        d = it.desire
        why = agent.swap_acceptable(d.params["receive"], d.params["release"]) or "recusa"
        agent.send(d.params["to"], REFUSE, "seat_swap", d.params["conv"], {"reason": why})
        agent.set_desire_status(d, "achieved", "recusa enviada")

    def achieved(self, agent, it):
        return it.state["sent"]


class Resync(Plan):
    name = "resync"
    kinds = ("resync",)

    def applicable(self, agent, d):
        return True

    def start(self, agent, d):
        return {"sent": False}, ()

    def execute(self, agent, it):
        if it.state["sent"]:
            return
        it.state["sent"] = True
        d = it.desire
        agent.sync_n = getattr(agent, "sync_n", 0) + 1
        agent.send(aid_dept(d.params["dept"]), REQUEST, "sync", f"sync:{agent.p.sid}:{agent.sync_n}", {})
        agent.set_desire_status(d, "achieved", "pedido de quadro enviado")

    def achieved(self, agent, it):
        return it.state["sent"]
