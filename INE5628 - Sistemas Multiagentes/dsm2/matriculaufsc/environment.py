"""Ambiente: tudo o que existe fora dos agentes e que eles só alcançam por percepção e ação.

O Environment reúne o barramento de mensagens, o Registrar (estado institucional: turmas, vagas, pontos, matrículas)
e os eventos exógenos do cenário (professor indisponível, sala fora do ar/de volta).

  advance(t)      início do tick: injeta os eventos de t como mensagens `inform` vindas de "env", entrega as mensagens
                  enviadas no tick anterior e deixa o Registrar processar seus pedidos (ordem por `mid`)
  perceive(aid)   o que o agente pode perceber neste tick: apenas as mensagens endereçadas a ele
  execute(...)    ação do agente: enviar uma mensagem (chega no tick seguinte; pode ser perdida ou atrasada por regras)
  snapshot()      visão do estado institucional, para métricas e depuração (os agentes não a usam)

Observabilidade parcial: nenhum agente lê o Registrar nem o estado de outro agente; suas crenças vêm só de `perceive`
e podem ficar desatualizadas. Quem altera o estado institucional é o Registrar, a pedido dos agentes (`execute`).
Não há aleatoriedade aqui: o mesmo cenário e as mesmas regras de falha produzem sempre a mesma sequência.
"""

from __future__ import annotations

from .bus import MessageBus
from .messages import INFORM, Message, aid_prof, aid_room
from .model import Scenario
from .registrar import RegistrarService
from .trace import TraceLogger

EVENT_KIND = {"professor_unavailable": "unavailable", "room_down": "down", "room_up": "up"}


class Environment:
    def __init__(self, scenario: Scenario, trace: TraceLogger, rules=()) -> None:
        self.scenario = scenario
        self.trace = trace
        self.bus = MessageBus(trace, rules)
        self.registrar = RegistrarService(scenario, trace)
        self.tick = 0
        self._inbox: dict[str, list[Message]] = {}

    def advance(self, t: int) -> None:
        self.tick = t
        self._inject_events(t)
        self._inbox = self.bus.deliver(t)
        self.registrar.step(t, self._inbox.get(self.registrar.id, []), self.bus)

    def perceive(self, aid: str) -> list[Message]:
        return self._inbox.get(aid, [])

    def execute(self, tick: int, sender: str, receiver: str, performative: str,
                protocol: str, conv: str, content: dict) -> Message:
        return self.bus.send(tick, sender, receiver, performative, protocol, conv, content)

    def snapshot(self) -> dict:
        reg = self.registrar
        return {
            "tick": self.tick,
            "sections": {sid: {"status": s.status, "prof": s.prof, "room": s.room, "roster": sorted(s.roster)}
                         for sid, s in sorted(reg.sections.items())},
            "points": dict(sorted(reg.points.items())),
            "invariants": reg.invariants(),
            "pending_messages": self.bus.pending(),
        }

    def _inject_events(self, t: int) -> None:
        for ev in self.scenario.events:
            if ev.tick != t:
                continue
            target = aid_prof(ev.target) if ev.kind == "professor_unavailable" else aid_room(ev.target)
            self.trace.log(t, "event", "env", event=ev.kind, target=ev.target, data=ev.data)
            self.execute(t, "env", target, INFORM, "event", f"evt:{ev.kind}:{t}", {"kind": EVENT_KIND[ev.kind], **ev.data})
