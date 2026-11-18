"""Métricas de resultado (utilidade normalizada, satisfação e efeitos distributivos)."""

from __future__ import annotations

from collections import Counter

from .model import Scenario
from .registrar import Registrar
from .utility import utility


def student_results(reg: Registrar, scenario: Scenario) -> dict[str, dict]:
    out = {}
    for s in scenario.students:
        courses = reg.enrolled_courses(s.sid)
        u = utility([c for c in s.required if c not in s.completed],
                    [c for c in s.electives if c not in s.completed],
                    courses, reg.schedule_slots(s.sid), s.undesired_slots)
        out[s.sid] = {**u, "courses": sorted(courses), "sections": reg.enrolled_sections(s.sid),
                      "points_left": reg.points[s.sid], "priority": s.priority}
    return out


def gini(values) -> float:
    v = sorted(values)
    n, total = len(v), sum(v)
    if n == 0 or total == 0:
        return 0.0
    return sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(v)) / (n * total)


def summarize(reg: Registrar, scenario: Scenario, trace=None) -> dict:
    res = student_results(reg, scenario)
    us = [r["U"] for r in res.values()]
    ordered = sorted(res.items(), key=lambda kv: (kv[1]["priority"], kv[0]))
    half = len(ordered) // 2
    low = [r["U"] for _, r in ordered[:half]] or [0.0]
    high = [r["U"] for _, r in ordered[half:]] or [0.0]
    open_secs = reg.open_sections()
    seats = sum(reg.sections[s].capacity for s in open_secs)
    filled = sum(len(reg.sections[s].roster) for s in open_secs)
    out = {
        "alunos": len(res),
        "turmas_abertas": len(open_secs),
        "ocupacao_vagas": round(filled / seats, 3) if seats else 0.0,
        "U_medio": round(sum(us) / len(us), 3) if us else 0.0,
        "pct_satisfatoria": round(100 * sum(r["satisfatoria"] for r in res.values()) / len(res), 1) if res else 0.0,
        "gini_U": round(gini(us), 3),
        "U_medio_baixa_prioridade": round(sum(low) / len(low), 3),
        "U_medio_alta_prioridade": round(sum(high) / len(high), 3),
        "invariantes_violadas": reg.invariants(),
    }
    if trace is not None:
        out["mensagens"] = dict(Counter(r["perf"] for r in trace.of_kind("msg")))
        out["mudancas_de_crenca"] = len(trace.of_kind("belief_change"))
        out["reconsideracoes"] = dict(Counter(r["decision"] for r in trace.of_kind("reconsider")))
    return out
