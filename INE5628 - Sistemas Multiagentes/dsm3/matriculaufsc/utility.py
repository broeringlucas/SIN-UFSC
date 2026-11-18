"""Função de utilidade normalizada (revisão da DSM1, anotação 3 do professor).

U = 0,60·R + 0,25·S + 0,15·E, com R, S, E ∈ [0, 1] e portanto U ∈ [0, 1].

  R = obrigatórias obtidas / obrigatórias desejadas        (1 se nenhuma desejada)
  E = min(1, eletivas obtidas / eletivas desejadas)        (1 se nenhuma desejada)
  S = 1 − (horas-aula em horários indesejados / horas-aula da grade)
      (0 se a grade está vazia e há algo desejado; 1 se a grade está vazia e nada é desejado)

Grade satisfatória: U ≥ θ = 0,70. Com esta normalização nenhum termo ultrapassa seu peso,
logo θ passa a ter significado: com 100% das obrigatórias, U ≥ 0,60 + 0,25·S; ficar apenas
nas obrigatórias com horários bons dá 0,85 + 0,15·E.
"""

from __future__ import annotations

from typing import Iterable

W_REQ, W_SCHED, W_ELEC = 0.60, 0.25, 0.15
THETA = 0.70


def _ratio(got: int, wanted: int) -> float:
    return 1.0 if wanted == 0 else min(1.0, got / wanted)


def utility(desired_required: Iterable[str], desired_electives: Iterable[str],
            obtained_courses: Iterable[str], schedule_slots: Iterable[str],
            undesired_slots: Iterable[str]) -> dict:
    dr, de, got = set(desired_required), set(desired_electives), set(obtained_courses)
    undesired = set(undesired_slots)
    slots = list(schedule_slots)
    r = _ratio(len(dr & got), len(dr))
    e = _ratio(len(de & got), len(de))
    if slots:
        s = 1.0 - sum(1 for x in slots if x in undesired) / len(slots)
    else:
        s = 1.0 if not dr and not de else 0.0
    u = W_REQ * r + W_SCHED * s + W_ELEC * e
    return {"U": u, "R": r, "S": s, "E": e, "satisfatoria": u >= THETA}
