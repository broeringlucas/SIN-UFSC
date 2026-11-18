"""Contratos de mensagem e política de papéis nas fronteiras dos protocolos (DSM3).

Toda mensagem é conferida em três camadas (defesa em profundidade):
  1. Ambiente (`Environment.execute`): autentica o remetente (credencial emitida no registro do agente) e aplica
     este módulo; mensagem inválida nunca entra no barramento.
  2. Agente receptor (`Agent.screen`): confere de novo o contrato de tudo que chega à sua caixa de entrada.
  3. Dono do estado (Registrar, Departamento): confere a *posse* (o remetente pode agir sobre esta turma/conversa?).

Um contrato (`SPEC`) diz, por (protocolo, performativa): quais papéis podem enviar, quais podem receber, o formato da
conversa (`conv`) e os campos do conteúdo com tipo. Campos desconhecidos são rejeitados, números precisam ser finitos
e `bool` não vale como inteiro. Operações do Registrar têm contrato próprio (`OPS`).

Tipos: str, int (≥ 0 quando "nat"), num (finito), strs (lista de str), list/dict (estrutura livre, limitada em tamanho).
Sufixo "?" marca campo opcional.
"""

from __future__ import annotations

import math
import re

# papéis (prefixo do identificador do agente)
ALUNO, PROF, DEPT, ROOM, REGISTRAR, ENV = "aluno", "prof", "dept", "room", "registrar", "env"
ROLES = {ALUNO, PROF, DEPT, ROOM}

MAX_STR, MAX_LIST = 200, 200

_ID = r"[A-Za-z0-9_.\-]{1,64}"
CONV = {
    "demand": rf"demand:{_ID}",
    "board": rf"board:{_ID}:\d{{1,6}}",
    "open": rf"open:{_ID}",
    "cancel": rf"cancel:{_ID}",
    "auc": rf"auc:{_ID}:\d{{1,4}}",
    "withdraw": rf"withdraw:{_ID}",
    "evt": r"evt:[a-z_]{1,32}:\d{1,6}",
    "swap": rf"swap:{_ID}:{_ID}:{_ID}:\d{{1,6}}",
    "sync": rf"sync:{_ID}:\d{{1,6}}",
}


def role_of(aid: str) -> str | None:
    if aid in (REGISTRAR, ENV):
        return aid
    head, sep, tail = aid.partition(":")
    return head if sep and tail and head in ROLES else None


# (protocolo, performativa) -> remetentes, destinatários, conv, campos
def _spec(frm, to, conv, **fields):
    return {"from": set(frm), "to": set(to), "conv": conv, "fields": fields}


SPEC: dict[tuple[str, str], dict] = {
    ("demand", "inform"): _spec([ALUNO], [DEPT], ["demand"], course="str", student="str"),
    ("board", "inform"): _spec([DEPT], [ALUNO], ["board"], sections="list", removed="strs"),
    ("section_opening", "cfp"): _spec([DEPT], [PROF], ["open"], section="str", course="str", slots="strs"),
    ("section_opening", "propose"): _spec([PROF], [DEPT], ["open"], section="str", score="num"),
    ("section_opening", "refuse"): _spec([PROF], [DEPT], ["open"], section="str", reason="str?"),
    ("section_opening", "accept-proposal"): _spec([DEPT], [PROF], ["open"], section="str"),
    ("section_opening", "reject-proposal"): _spec([DEPT], [PROF], ["open"], section="str", reason="str?"),
    ("section_opening", "cancel"): _spec([DEPT], [PROF], ["open"], section="str"),
    ("section_opening", "inform"): _spec([DEPT], [PROF], ["open"], section="str", slots="strs"),
    ("room_reservation", "request"): _spec([DEPT], [ROOM], ["open"], section="str", slots="strs", capacity="nat"),
    ("room_reservation", "agree"): _spec([ROOM], [DEPT], ["open"], section="str", room="str", capacity="nat"),
    ("room_reservation", "refuse"): _spec([ROOM], [DEPT], ["open"], section="str", room="str", reason="str?"),
    ("room_reservation", "cancel"): _spec([DEPT], [ROOM], ["open", "cancel"], section="str"),
    ("room_reservation", "inform"): _spec([DEPT], [ROOM], ["open"], section="str"),
    ("room_reservation", "reject-proposal"): _spec([DEPT], [ROOM], ["open"], section="str", reason="str?"),
    ("registrar", "request"): _spec([DEPT], [REGISTRAR], ["open", "cancel", "auc", "swap"], op="str"),
    ("registrar", "inform"): _spec([REGISTRAR], [DEPT], ["open", "cancel", "auc", "swap"], op="str", ok="bool", reasons="strs"),
    ("registrar", "failure"): _spec([REGISTRAR], [DEPT], ["open", "cancel", "auc", "swap"], op="str", ok="bool", reasons="strs"),
    ("seat_swap", "request"): _spec([ALUNO], [DEPT], ["swap"], give="str", want="str"),
    ("seat_swap", "cfp"): _spec([DEPT], [ALUNO], ["swap"], receive="str", release="str"),
    ("seat_swap", "agree"): _spec([ALUNO], [DEPT], ["swap"], receive="str", release="str"),
    ("seat_swap", "refuse"): _spec([ALUNO], [DEPT], ["swap"], reason="str?"),
    ("seat_swap", "inform"): _spec([DEPT], [ALUNO], ["swap"], outcome="str", old="str", new="str?", reason="str?"),
    ("sync", "request"): _spec([ALUNO], [DEPT], ["sync"]),
    ("seat_auction", "cfp"): _spec([DEPT], [ALUNO], ["auc"], section="str", round="nat", remaining="nat", reserve="nat"),
    ("seat_auction", "propose"): _spec([ALUNO], [DEPT], ["auc"], section="str", bid="nat", round="nat"),
    ("seat_auction", "refuse"): _spec([ALUNO], [DEPT], ["auc"], section="str", reason="str?"),
    ("seat_auction", "accept-proposal"): _spec([DEPT], [ALUNO], ["auc"], section="str", price="nat", balance="nat", round="nat"),
    ("seat_auction", "reject-proposal"): _spec([DEPT], [ALUNO], ["auc"], section="str", reason="str?", round="nat?"),
    ("enrollment", "inform"): _spec([DEPT], [ALUNO], ["cancel", "swap"], section="str", refund="nat", balance="nat", reason="str?"),
    ("commitment", "inform"): _spec([PROF], [DEPT], ["withdraw"], section="str", prof="str", slots="strs"),
    ("event", "inform"): _spec([ENV], [PROF, ROOM], ["evt"], kind="str", slots="strs?", reason="str?"),
}

# operações do Registrar -> campos
OPS: dict[str, dict[str, str]] = {
    "commit_enroll": {"student": "str", "section": "str", "price": "nat"},
    "open_section": {"section": "str", "prof": "str", "room": "str", "capacity": "nat"},
    "cancel_section": {"section": "str", "reason": "str?", "block": "dict?"},
    "swap_enroll": {"student_a": "str", "student_b": "str", "section_a": "str", "section_b": "str"},
}


def register_protocol(spec: dict, ops: dict | None = None) -> None:
    """Extensão dos contratos por módulos novos de protocolo (seat_swap, sync)."""
    SPEC.update(spec)
    if ops:
        OPS.update(ops)


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def check_type(value, tag: str) -> str | None:
    """Devolve None se o valor cabe no tipo, senão o motivo."""
    if tag == "str":
        if not isinstance(value, str) or not value or len(value) > MAX_STR:
            return "texto inválido"
    elif tag == "nat":
        if not _is_int(value) or value < 0 or value > 10**9:
            return "inteiro ≥ 0 esperado"
    elif tag == "int":
        if not _is_int(value) or abs(value) > 10**9:
            return "inteiro esperado"
    elif tag == "num":
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return "número finito esperado"
    elif tag == "bool":
        if not isinstance(value, bool):
            return "booleano esperado"
    elif tag == "strs":
        if not isinstance(value, (list, tuple)) or len(value) > MAX_LIST:
            return "lista de textos esperada"
        if any(not isinstance(x, str) or not x or len(x) > MAX_STR for x in value):
            return "lista de textos esperada"
    elif tag == "list":
        if not isinstance(value, (list, tuple)) or len(value) > MAX_LIST:
            return "lista esperada"
    elif tag == "dict":
        if not isinstance(value, dict) or len(value) > MAX_LIST:
            return "dicionário esperado"
    else:  # pragma: no cover
        return f"tipo desconhecido {tag}"
    return None


def check_fields(content, fields: dict[str, str], extra_ok: set[str] = frozenset()) -> list[str]:
    if not isinstance(content, dict):
        return ["conteúdo não é um dicionário"]
    errs = []
    for name, tag in fields.items():
        optional = tag.endswith("?")
        base = tag.rstrip("?")
        if name not in content or content[name] is None:
            if not optional:
                errs.append(f"campo obrigatório ausente: {name}")
            continue
        why = check_type(content[name], base)
        if why:
            errs.append(f"{name}: {why}")
    for name in content:
        if name not in fields and name not in extra_ok:
            errs.append(f"campo desconhecido: {name}")
    return errs


def conv_ok(conv: str, kinds: list[str]) -> bool:
    return isinstance(conv, str) and any(re.fullmatch(CONV[k], conv) for k in kinds)


def validate(msg) -> list[str]:
    """Contrato completo de uma mensagem. Lista vazia = válida."""
    key = (msg.protocol, msg.performative)
    spec = SPEC.get(key)
    if spec is None:
        return [f"protocolo/performativa desconhecidos: {msg.protocol}/{msg.performative}"]
    errs = []
    s_role, r_role = role_of(msg.sender), role_of(msg.receiver)
    if s_role not in spec["from"]:
        errs.append(f"papel {s_role!r} não pode enviar {msg.protocol}/{msg.performative}")
    if r_role not in spec["to"]:
        errs.append(f"papel {r_role!r} não pode receber {msg.protocol}/{msg.performative}")
    if not conv_ok(msg.conv, spec["conv"]):
        errs.append(f"conv inválida: {msg.conv!r}")
    if msg.protocol == "registrar" and msg.performative == "request":
        errs += validate_request(msg.content)
    elif msg.protocol == "registrar":  # resposta: campos de eco da operação variam; só o envelope é exigido
        errs += check_fields(msg.content, spec["fields"], extra_ok=set(msg.content) if isinstance(msg.content, dict) else set())
    else:
        errs += check_fields(msg.content, spec["fields"])
    return errs


def validate_request(content) -> list[str]:
    if not isinstance(content, dict):
        return ["conteúdo não é um dicionário"]
    op = content.get("op")
    if not isinstance(op, str) or op not in OPS:
        return [f"operação desconhecida ou ausente: {op!r}"]
    return check_fields({k: v for k, v in content.items() if k != "op"}, OPS[op])
