"""Modelo de dados do domínio (cenário, cursos, turmas, perfis, eventos, configuração).

Slot: texto como "SEG08" = segunda-feira, 08h (1 hora-aula).
SectionDef: turma planejada pelo departamento; só vira turma aberta após o protocolo section_opening.
StudentProfile.priority: fase/semestre, usada no desempate do leilão e na política "prioridade".
Event: kind = professor_unavailable | room_down | room_up; target = id do professor ou da sala.
Config: open_start (tick dos cfp de abertura de turma), first_round e round_period (rodadas do leilão), rounds,
hold_ttl (validade das reservas provisórias), timeout (respostas, em ticks), pricing (first | uniform),
reserve (lance mínimo), max_cascade (substituições de vencedores por rodada e turma),
swaps / sync (liga e desliga trocas de turma e recuperação de crenças; usados nos experimentos de ablação),
bid_window (janela de lances do leilão), swap_timeout (espera por resposta no protocolo seat_swap).
"""

from __future__ import annotations

from dataclasses import dataclass, field

Slot = str


@dataclass(frozen=True)
class Course:
    code: str
    name: str
    dept: str
    prereqs: tuple[str, ...] = ()


@dataclass(frozen=True)
class SectionDef:
    sid: str
    course: str
    dept: str
    slots: tuple[Slot, ...]
    capacity: int
    min_demand: int = 1


@dataclass(frozen=True)
class StudentProfile:
    sid: str
    completed: frozenset[str] = frozenset()
    required: tuple[str, ...] = ()
    electives: tuple[str, ...] = ()
    undesired_slots: frozenset[Slot] = frozenset()
    points: int = 100
    priority: float = 0.0
    max_courses: int = 6


@dataclass(frozen=True)
class ProfessorProfile:
    pid: str
    dept: str
    teaches: frozenset[str]
    available: frozenset[Slot]
    preferred: frozenset[Slot] = frozenset()
    max_hours: int = 8


@dataclass(frozen=True)
class RoomDef:
    rid: str
    dept: str
    capacity: int


@dataclass(frozen=True)
class Event:
    tick: int
    kind: str
    target: str
    data: dict = field(default_factory=dict)


@dataclass
class Config:
    open_start: int = 2
    first_round: int = 30
    round_period: int = 16
    rounds: int = 3
    hold_ttl: int = 10
    timeout: int = 3
    pricing: str = "first"
    reserve: int = 1
    max_cascade: int = 4
    swaps: bool = True          # alunos podem propor trocas de turma (protocolo seat_swap)
    sync: bool = True           # aluno recupera crenças desatualizadas pedindo o quadro ao departamento
    bid_window: int = 2         # ticks que o leilão espera pelos lances (padrão 2: lances enviados no tick seguinte ao cfp)
    swap_timeout: int = 3       # ticks de espera por resposta do parceiro / do Registrar

    def round_starts(self) -> list[int]:
        return [self.first_round + i * self.round_period for i in range(self.rounds)]

    def end_tick(self) -> int:
        return self.first_round + self.rounds * self.round_period + 2


@dataclass
class Scenario:
    name: str
    courses: dict[str, Course]
    sections: list[SectionDef]
    students: list[StudentProfile]
    professors: list[ProfessorProfile]
    rooms: list[RoomDef]
    events: list[Event] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    description: str = ""

    @property
    def depts(self) -> list[str]:
        return sorted({c.dept for c in self.courses.values()})
