"""Leitor de trace para depuração:  python -m matriculaufsc.explain out/trace.jsonl aluno:bruno

Mostra a linha do tempo BDI de um agente (crenças → desejos → planos → intenções → reconsiderações),
as transições de FSM, reações de sala, falhas do Registrar e notas. Use --kinds para filtrar e
--tick A:B para uma janela de tempo.
"""

from __future__ import annotations

import argparse
import json
import sys

DEFAULT_KINDS = ("desire_change", "plan_selected", "intention_change", "reconsider", "fsm", "reaction", "note")


def fmt(r: dict) -> str | None:
    k, t = r["kind"], f"{r['tick']:3d}"
    if k == "belief_change":
        return f"{t} CRENÇA    {r['key']}: {r['old']} → {r['new']}  [{r['cause']}]"
    if k == "desire_change":
        return f"{t} DESEJO    {r['desire']}: {r['old']} → {r['new']}  ({r['reason']})"
    if k == "plan_selected":
        return f"{t} PLANO     {r['desire']}: escolhido {r['chosen']} entre {r['options']}"
    if k == "intention_change":
        return f"{t} INTENÇÃO  {r['intention']} {r['action']} ({r.get('plan')}) {r.get('targets') or ''}".rstrip()
    if k == "reconsider":
        return f"{t} RECONSID. {r['intention']} {r['decision'].upper()} — mudou {r['changed']}: {r['why']}"
    if k == "fsm":
        return f"{t} FSM       {r['protocol']}[{r['ref']}] {r['frm']} → {r['to']}  {r['why']}"
    if k == "reaction":
        return f"{t} REAÇÃO    {r['rule']} {r.get('section', '')} {r.get('effect', '')}"
    if k == "registrar":
        return f"{t} REGISTRAR {r['op']} ok={r['ok']} {r['reasons'] or ''} {r.get('student', r.get('section', ''))}"
    if k == "note":
        return f"{t} NOTA      {r['text']}"
    if k == "msg":
        return f"{t} MSG       {r['agent']} → {r['to']} {r['perf']} ({r['protocol']}) {r['content']}"
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="matriculaufsc.explain")
    ap.add_argument("trace")
    ap.add_argument("agent", nargs="?", help="ex.: aluno:bruno, prof:prof_ine1, dept:INE, room:R-I2, registrar")
    ap.add_argument("--kinds", default=",".join(DEFAULT_KINDS), help="lista separada por vírgula; inclua belief_change e msg se quiser")
    ap.add_argument("--tick", default=None, help="janela A:B")
    a = ap.parse_args(argv)
    kinds = set(a.kinds.split(","))
    lo, hi = (int(x) for x in a.tick.split(":")) if a.tick else (0, 10**9)
    for line in open(a.trace, encoding="utf-8"):
        r = json.loads(line)
        if r["kind"] in kinds and lo <= r["tick"] <= hi and (a.agent is None or r["agent"] == a.agent):
            out = fmt(r)
            if out:
                print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
