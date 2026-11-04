"""Registro estruturado (JSONL) de tudo o que acontece na simulação.

Tipos de registro (`kind`): msg, msg_dropped, belief_change, desire_change, plan_selected,
intention_change, reconsider, fsm, reaction, registrar, event, note, end.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _default(o):
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if hasattr(o, "__dict__"):
        return vars(o)
    return str(o)


class TraceLogger:
    def __init__(self) -> None:
        self.records: list[dict] = []

    def log(self, tick: int, kind: str, agent: str, **data) -> dict:
        rec = {"seq": len(self.records), "tick": tick, "kind": kind, "agent": agent, **data}
        self.records.append(rec)
        return rec

    def of_kind(self, *kinds: str) -> list[dict]:
        return [r for r in self.records if r["kind"] in kinds]

    def where(self, kind: str | None = None, agent: str | None = None, **match) -> list[dict]:
        out = []
        for r in self.records:
            if kind and r["kind"] != kind:
                continue
            if agent and r["agent"] != agent:
                continue
            if all(r.get(k) == v for k, v in match.items()):
                out.append(r)
        return out

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True, default=_default) for r in self.records)

    def dump(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_jsonl() + "\n", encoding="utf-8")

    def digest(self) -> str:
        return hashlib.sha256(self.to_jsonl().encode("utf-8")).hexdigest()
