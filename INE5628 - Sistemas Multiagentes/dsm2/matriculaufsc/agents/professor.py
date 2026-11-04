"""ProfessorAgent (BDI): responde a convites (cfp) para turmas e honra compromissos.

Crenças:  available, committed (turmas confirmadas → slots), hold:<turma> (reserva provisória com validade).
Desejos:  respond:<conversa> (responder a um cfp) e deliver:<turma> (lecionar a turma confirmada).
Planos:   propose / decline  para `respond`;  keep_commitment / withdraw  para `deliver`.
Reconsideração: o evento "professor indisponível" muda `available`; a intenção keep_commitment
deixa de ser válida, é abandonada e o plano `withdraw` avisa o departamento e libera a carga.

Antes de enviar a proposta o professor reavalia o convite: outra proposta do mesmo tick pode ter criado reserva.
"""

from __future__ import annotations

from ..messages import ACCEPT, CANCEL, CFP, INFORM, PROPOSE, REFUSE, REJECT, aid_dept, aid_prof
from ..model import Config, ProfessorProfile
from .bdi import BDIAgent, Desire, Plan


class Professor(BDIAgent):
    def __init__(self, profile: ProfessorProfile, env, trace, cfg: Config) -> None:
        super().__init__(aid_prof(profile.pid), env, trace, [Propose(), Decline(), KeepCommitment(), Withdraw()])
        self.p = profile
        self.cfg = cfg
        self.beliefs.set("available", sorted(profile.available), "init")
        self.beliefs.set("committed", {}, "init")

    def committed(self) -> dict:
        return self.beliefs.get("committed", {}) or {}

    def hold_slots(self) -> set[str]:
        return {x for k in self.beliefs.keys_with("hold:") for x in self.beliefs.get(k)["slots"]}

    def hours(self) -> int:
        return sum(len(s) for s in self.committed().values())

    def decline_reason(self, d: Desire) -> str | None:
        slots = set(d.params["slots"])
        if d.params["course"] not in self.p.teaches:
            return "não leciona a disciplina"
        if not slots <= set(self.beliefs.get("available")):
            return "indisponível no horário"
        busy = {x for s in self.committed().values() for x in s} | self.hold_slots()
        if slots & busy:
            return "conflito com compromisso/reserva"
        if self.hours() + len(self.hold_slots()) + len(slots) > self.p.max_hours:
            return "carga máxima"
        return None

    def perceive(self, inbox) -> None:
        self.cfps = []
        for key in self.beliefs.keys_with("hold:"):
            if self.beliefs.get(key)["expiry"] <= self.tick:
                self.beliefs.set(key, None, "reserva provisória expirou (TTL)")
        for m in inbox:
            c = m.content
            if m.protocol == "event" and c["kind"] == "unavailable":
                gone = set(c.get("slots") or self.beliefs.get("available"))
                self.beliefs.set("available", sorted(set(self.beliefs.get("available")) - gone),
                                 "evento: professor indisponível")
            elif m.protocol == "section_opening":
                sid = c["section"]
                if m.performative == CFP:
                    self.add_desire(Desire(f"respond:{m.conv}@{m.tick}", "respond", 1.0,
                                           {"section": sid, "course": c["course"], "slots": list(c["slots"]),
                                            "conv": m.conv, "to": m.sender}))
                elif m.performative == ACCEPT:
                    h = self.beliefs.get(f"hold:{sid}")
                    if h:
                        self.beliefs.set(f"hold:{sid}", {**h, "expiry": self.tick + self.cfg.hold_ttl, "selected": True},
                                         "departamento aceitou minha proposta")
                elif m.performative in (REJECT, CANCEL):
                    self.beliefs.set(f"hold:{sid}", None, f"reserva liberada ({m.performative})")
                    if sid in self.committed() and m.performative == CANCEL:
                        com = dict(self.committed())
                        com.pop(sid)
                        self.beliefs.set("committed", com, "compromisso cancelado pelo departamento")
                elif m.performative == INFORM:
                    h = self.beliefs.get(f"hold:{sid}")
                    slots = h["slots"] if h else list(c.get("slots", []))
                    com = dict(self.committed())
                    com[sid] = slots
                    self.beliefs.set("committed", com, f"turma {sid} confirmada")
                    self.beliefs.set(f"hold:{sid}", None, "reserva convertida em compromisso")
                    self.add_desire(Desire(f"deliver:{sid}", "deliver", 2.0, {"section": sid}))

    def update_desires(self) -> None:
        for name, d in self.desires.items():
            if d.kind == "deliver" and d.params["section"] not in self.committed():
                self.set_desire_status(d, "dropped", "compromisso encerrado")
            elif d.kind == "deliver" and d.status == "dropped":
                self.set_desire_status(d, "active", "compromisso restabelecido")


class Propose(Plan):
    name = "propose"
    kinds = ("respond",)

    def applicable(self, agent, d):
        return agent.decline_reason(d) is None

    def score(self, agent, d):
        slots = set(d.params["slots"])
        return 1.0 + len(slots & set(agent.p.preferred)) / len(slots)

    def start(self, agent, d):
        return {"targets": []}, ()

    def execute(self, agent, it):
        d, sid = it.desire, it.desire.params["section"]
        if it.state.get("sent"):
            return
        it.state["sent"] = True
        reason = agent.decline_reason(d)
        if reason:
            agent.send(d.params["to"], REFUSE, "section_opening", d.params["conv"],
                       {"section": sid, "reason": reason})
            agent.set_desire_status(d, "achieved", "recusa enviada (conflito surgido no mesmo tick)")
            return
        score = self.score(agent, d)
        agent.beliefs.set(f"hold:{sid}", {"slots": d.params["slots"], "expiry": agent.tick + agent.cfg.hold_ttl,
                                          "selected": False}, "reserva provisória para a proposta")
        agent.send(d.params["to"], PROPOSE, "section_opening", d.params["conv"], {"section": sid, "score": score})
        agent.set_desire_status(d, "achieved", "proposta enviada")

    def achieved(self, agent, it):
        return bool(it.state.get("sent"))


class Decline(Plan):
    name = "decline"
    kinds = ("respond",)

    def applicable(self, agent, d):
        return True

    def score(self, agent, d):
        return 0.1

    def start(self, agent, d):
        return {"targets": []}, ()

    def execute(self, agent, it):
        d = it.desire
        if it.state.get("sent"):
            return
        it.state["sent"] = True
        agent.send(d.params["to"], REFUSE, "section_opening", d.params["conv"],
                   {"section": d.params["section"], "reason": agent.decline_reason(d)})
        agent.set_desire_status(d, "achieved", "recusa enviada")

    def achieved(self, agent, it):
        return bool(it.state.get("sent"))


def _slots_ok(agent: Professor, sid: str) -> bool:
    return set(agent.committed().get(sid, [])) <= set(agent.beliefs.get("available"))


class KeepCommitment(Plan):
    name = "keep_commitment"
    kinds = ("deliver",)

    def applicable(self, agent, d):
        return d.params["section"] in agent.committed() and _slots_ok(agent, d.params["section"])

    def start(self, agent, d):
        return {"targets": []}, ("available", "committed")

    def valid(self, agent, it):
        sid = it.desire.params["section"]
        return sid in agent.committed() and _slots_ok(agent, sid)


class Withdraw(Plan):
    name = "withdraw"
    kinds = ("deliver",)

    def applicable(self, agent, d):
        sid = d.params["section"]
        return sid in agent.committed() and not _slots_ok(agent, sid)

    def score(self, agent, d):
        return 2.0

    def start(self, agent, d):
        return {"targets": []}, ()

    def execute(self, agent, it):
        d, sid = it.desire, it.desire.params["section"]
        if it.state.get("sent") or sid not in agent.committed():
            return
        it.state["sent"] = True
        lost = sorted(set(agent.committed()[sid]) - set(agent.beliefs.get("available")))
        agent.send(aid_dept(agent.p.dept), INFORM, "commitment", f"withdraw:{sid}",
                   {"section": sid, "prof": agent.p.pid, "slots": lost})
        com = dict(agent.committed())
        com.pop(sid)
        agent.beliefs.set("committed", com, f"compromisso com {sid} retirado (indisponibilidade)")
        agent.set_desire_status(d, "dropped", "compromisso retirado")

    def achieved(self, agent, it):
        return bool(it.state.get("sent"))
