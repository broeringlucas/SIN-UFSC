"""Políticas de referência para comparação distributiva com o leilão (recomendação do professor).

As duas políticas usam *as mesmas turmas abertas* pelo SMA e o mesmo Registrar (mesmas validações),
mudando só o critério de alocação das vagas:
  first_come  alunos atendidos em ordem de chegada (permutação sorteada com a semente)
  priority    alunos atendidos por prioridade decrescente (ex.: fase), desempate por id
Cada aluno, na sua vez, pega a melhor turma válida de cada disciplina desejada (obrigatórias antes).
Não há pontos nessas políticas (preço 0).
"""

from __future__ import annotations

import random

from .metrics import summarize
from .model import Scenario
from .registrar import Registrar
from .sim import Simulation


def opened_snapshot(reg: Registrar) -> dict[str, dict]:
    return {sid: {"prof": reg.sections[sid].prof, "room": reg.sections[sid].room,
                  "capacity": reg.sections[sid].capacity} for sid in reg.open_sections()}


def run_baseline(scenario: Scenario, policy: str, seed: int, opened: dict[str, dict]) -> Registrar:
    reg = Registrar(scenario)
    for sid, info in sorted(opened.items()):
        ok, why = reg.open_section(sid, info["prof"], info["room"], info["capacity"])
        assert ok, (sid, why)
    ids = sorted(s.sid for s in scenario.students)
    if policy == "first_come":
        random.Random(seed).shuffle(ids)
    elif policy == "priority":
        ids.sort(key=lambda i: (-reg.students[i].priority, i))
    else:
        raise ValueError(policy)
    for sid in ids:
        st = reg.students[sid]
        for course in [c for c in st.required if c not in st.completed] + [c for c in st.electives if c not in st.completed]:
            options = []
            for sec in reg.open_sections():
                if reg.sections[sec].d.course == course and not reg.validate_enroll(sid, sec, 0):
                    bad = len(set(reg.sections[sec].d.slots) & st.undesired_slots)
                    options.append((bad, sec))
            if options:
                reg.commit_enroll(sid, min(options)[1], 0)
    return reg


def compare_policies(scenario: Scenario, seed: int = 0, pricing: str | None = None) -> dict[str, dict]:
    sim = Simulation(scenario, seed, pricing=pricing).run()
    opened = opened_snapshot(sim.registrar)
    out = {"auction": summarize(sim.registrar, scenario, sim.trace)}
    for policy in ("first_come", "priority"):
        out[policy] = summarize(run_baseline(scenario, policy, seed, opened), scenario)
    return out
