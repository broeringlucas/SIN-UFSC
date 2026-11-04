"""Agent: identificador, acesso ao ambiente (só por `send`) e ao log; `step` roda uma vez por tick com as percepções."""

from __future__ import annotations

from ..environment import Environment
from ..trace import TraceLogger


class Agent:
    def __init__(self, aid: str, env: Environment, trace: TraceLogger) -> None:
        self.id = aid
        self.env = env
        self.trace = trace
        self.tick = 0

    def send(self, to: str, perf: str, protocol: str, conv: str, content: dict):
        return self.env.execute(self.tick, self.id, to, perf, protocol, conv, content)

    def log(self, kind: str, **data) -> None:
        self.trace.log(self.tick, kind, self.id, **data)

    def step(self, tick: int, inbox) -> None:
        raise NotImplementedError
