"""Máquinas de estados executáveis dos protocolos section_opening e seat_auction (figura 4 da DSM1).

Cada protocolo é uma tabela estado -> estados permitidos. O DepartamentoAgent consulta `check` a cada
mudança de estado; uma transição fora da tabela levanta InvalidTransition. Estados sem saída são terminais.

section_opening: Idle, AguardandoPropostas, Avaliando, ReservandoSala, ConfirmandoRegistrar, Revertendo, Aberta, Falha
seat_auction:    Idle, AguardandoLances, Avaliando, Validando, Concluido, SemLanceValido, Cancelado
"""

from __future__ import annotations


class InvalidTransition(RuntimeError):
    pass


SECTION_OPENING = {
    "Idle": {"AguardandoPropostas", "Falha"},
    "AguardandoPropostas": {"Avaliando"},
    "Avaliando": {"Avaliando", "ReservandoSala", "Falha"},
    "ReservandoSala": {"ReservandoSala", "ConfirmandoRegistrar", "Avaliando"},
    "ConfirmandoRegistrar": {"Aberta", "Avaliando", "Revertendo"},
    "Revertendo": {"Avaliando", "Falha"},
    "Aberta": set(),
    "Falha": set(),
}

SEAT_AUCTION = {
    "Idle": {"AguardandoLances"},
    "AguardandoLances": {"Avaliando", "Cancelado", "Concluido"},
    "Avaliando": {"Validando", "SemLanceValido", "Concluido"},
    "Validando": {"Concluido", "Cancelado"},
    "Concluido": set(),
    "SemLanceValido": set(),
    "Cancelado": set(),
}

TABLES = {"section_opening": SECTION_OPENING, "seat_auction": SEAT_AUCTION}


def check(protocol: str, frm: str, to: str) -> None:
    if to not in TABLES[protocol][frm]:
        raise InvalidTransition(f"{protocol}: {frm} -> {to}")


def terminal_states(protocol: str) -> set[str]:
    return {state for state, nxt in TABLES[protocol].items() if not nxt}
