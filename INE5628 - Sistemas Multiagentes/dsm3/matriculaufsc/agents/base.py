"""Agent: identificador, acesso ao ambiente (só por `send`) e ao log; `step` roda uma vez por tick com as percepções."""

from __future__ import annotations

from .. import contracts
from ..environment import Environment
from ..trace import TraceLogger


class Agent:
    def __init__(self, aid: str, env: Environment, trace: TraceLogger) -> None:
        self.id = aid
        self.env = env
        self.trace = trace
        self.tick = 0
        self._credential = env.register(aid)

    def send(self, to: str, perf: str, protocol: str, conv: str, content: dict):
        return self.env.execute(self.tick, self.id, to, perf, protocol, conv, content, self._credential)

    def screen(self, inbox):
        """Segunda camada: descarta (e registra) o que chega fora do contrato, antes de qualquer decisão."""
        ok = []
        for m in inbox:
            reasons = contracts.validate(m)
            if reasons:
                self.log("msg_invalid", mid=m.mid, sender=m.sender, perf=m.performative, protocol=m.protocol,
                         reasons=reasons)
            else:
                ok.append(m)
        return ok

    def log(self, kind: str, **data) -> None:
        self.trace.log(self.tick, kind, self.id, **data)

    def step(self, tick: int, inbox) -> None:
        raise NotImplementedError
