"""Mensagens no estilo FIPA-ACL (subconjunto de performativas usado pelos protocolos).

mid: id global crescente (define a ordem determinística de processamento); tick: quando foi enviada.
protocol: seat_auction, section_opening, room_reservation, registrar, demand, board, enrollment, commitment, event.
conv: id da conversa (ex.: "auc:MTM1-A:0", "open:INE1-A").
"""

from __future__ import annotations

from dataclasses import dataclass

CFP = "cfp"
PROPOSE = "propose"
REFUSE = "refuse"
ACCEPT = "accept-proposal"
REJECT = "reject-proposal"
REQUEST = "request"
AGREE = "agree"
INFORM = "inform"
FAILURE = "failure"
CANCEL = "cancel"


@dataclass(frozen=True)
class Message:
    mid: int
    tick: int
    sender: str
    receiver: str
    performative: str
    protocol: str
    conv: str
    content: dict


def aid_student(sid: str) -> str:
    return f"aluno:{sid}"


def aid_prof(pid: str) -> str:
    return f"prof:{pid}"


def aid_room(rid: str) -> str:
    return f"room:{rid}"


def aid_dept(dept: str) -> str:
    return f"dept:{dept}"
