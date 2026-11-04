"""Barramento de mensagens: latência de 1 tick, ordem determinística, injeção de falhas.

Rule descarta (drop) ou atrasa (delay) as mensagens que casam com o filtro; a fila guarda (tick de entrega, mid, mensagem).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .messages import Message
from .trace import TraceLogger


@dataclass
class Rule:
    action: str = "drop"
    sender: str | None = None
    receiver: str | None = None
    performative: str | None = None
    protocol: str | None = None
    conv_prefix: str | None = None
    from_tick: int = 0
    to_tick: float = math.inf
    delay: int = 0
    max_hits: int | None = None
    hits: int = 0

    def matches(self, m: Message) -> bool:
        if self.max_hits is not None and self.hits >= self.max_hits:
            return False
        if not (self.from_tick <= m.tick <= self.to_tick):
            return False
        for attr in ("sender", "receiver", "performative", "protocol"):
            want = getattr(self, attr)
            if want is not None and getattr(m, attr) != want:
                return False
        if self.conv_prefix is not None and not m.conv.startswith(self.conv_prefix):
            return False
        return True


class MessageBus:
    def __init__(self, trace: TraceLogger, rules=()) -> None:
        self.trace = trace
        self.rules: list[Rule] = list(rules)
        self._mid = 0
        self._queue: list[tuple[int, int, Message]] = []

    def send(self, tick: int, sender: str, receiver: str, performative: str,
             protocol: str, conv: str, content: dict) -> Message:
        self._mid += 1
        msg = Message(self._mid, tick, sender, receiver, performative, protocol, conv, content)
        deliver = tick + 1
        for rule in self.rules:
            if rule.matches(msg):
                rule.hits += 1
                if rule.action == "drop":
                    self.trace.log(tick, "msg_dropped", sender, mid=msg.mid, to=receiver,
                                   perf=performative, protocol=protocol, conv=conv)
                    return msg
                deliver += rule.delay
                break
        self.trace.log(tick, "msg", sender, mid=msg.mid, to=receiver, perf=performative,
                       protocol=protocol, conv=conv, content=content, deliver=deliver)
        self._queue.append((deliver, msg.mid, msg))
        return msg

    def deliver(self, tick: int) -> dict[str, list[Message]]:
        out: dict[str, list[Message]] = {}
        keep = []
        for entry in self._queue:
            if entry[0] <= tick:
                out.setdefault(entry[2].receiver, []).append(entry[2])
            else:
                keep.append(entry)
        self._queue = keep
        for msgs in out.values():
            msgs.sort(key=lambda m: m.mid)
        return out

    def pending(self) -> int:
        return len(self._queue)
