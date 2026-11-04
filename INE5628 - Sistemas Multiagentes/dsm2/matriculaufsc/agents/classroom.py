"""SalaAgent (reativo): sem crenças/intenções — uma tabela de regras evento → reação.

Regras:
  R1  request(reservar) e sala livre   → reserva provisória (TTL) + agree
  R2  request(reservar) e sala ocupada → refuse
  R3  request(reservar) e sala fora do ar → silêncio (o departamento sofre timeout)
  R4  inform(confirmada)               → converte a reserva em agendamento
  R5  cancel / reject                  → libera reserva ou agendamento
  R6  tempo                            → reservas provisórias expiram após `hold_ttl` ticks
  R7  evento room_down / room_up       → liga/desliga a sala
"""

from __future__ import annotations

from ..messages import AGREE, CANCEL, INFORM, REFUSE, REJECT, REQUEST, aid_room
from ..model import Config, RoomDef
from .base import Agent


class Classroom(Agent):
    def __init__(self, room: RoomDef, env, trace, cfg: Config) -> None:
        super().__init__(aid_room(room.rid), env, trace)
        self.room = room
        self.cfg = cfg
        self.holds: dict[str, dict] = {}
        self.booked: dict[str, list[str]] = {}
        self.down = False

    def busy_slots(self, except_sid: str | None = None) -> set[str]:
        out: set[str] = set()
        for table in (self.holds, self.booked):
            for sid, v in table.items():
                if sid != except_sid:
                    out |= set(v["slots"] if isinstance(v, dict) else v)
        return out

    def react(self, rule: str, **data) -> None:
        self.log("reaction", rule=rule, **data)

    def step(self, tick: int, inbox) -> None:
        self.tick = tick
        for sid in sorted(self.holds):
            if self.holds[sid]["expiry"] <= tick:
                del self.holds[sid]
                self.react("R6", section=sid, effect="reserva provisória expirou")
        for m in sorted(inbox, key=lambda m: m.mid):
            c = m.content
            if m.protocol == "event":
                self.down = c["kind"] == "down"
                self.react("R7", down=self.down)
            elif m.protocol == "room_reservation":
                sid = c["section"]
                if m.performative == REQUEST:
                    if self.down:
                        self.react("R3", section=sid, effect="sala fora do ar: sem resposta")
                    elif set(c["slots"]) & self.busy_slots(sid) or c["capacity"] > self.room.capacity:
                        self.react("R2", section=sid, effect="refuse")
                        self.send(m.sender, REFUSE, "room_reservation", m.conv,
                                  {"section": sid, "room": self.room.rid, "reason": "sala ocupada"})
                    else:
                        self.holds[sid] = {"slots": list(c["slots"]), "expiry": tick + self.cfg.hold_ttl}
                        self.react("R1", section=sid, effect="reserva provisória + agree")
                        self.send(m.sender, AGREE, "room_reservation", m.conv,
                                  {"section": sid, "room": self.room.rid, "capacity": self.room.capacity})
                elif m.performative == INFORM and sid in self.holds:
                    self.booked[sid] = self.holds.pop(sid)["slots"]
                    self.react("R4", section=sid, effect="agendamento confirmado")
                elif m.performative in (CANCEL, REJECT):
                    if self.holds.pop(sid, None) is not None or self.booked.pop(sid, None) is not None:
                        self.react("R5", section=sid, effect="liberada")
