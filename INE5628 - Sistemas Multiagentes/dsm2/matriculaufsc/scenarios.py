"""Cenários: S0 (controlado, para depuração) e S1 (reduzido, gerado com semente).

S0: 5 alunos, 2 departamentos, 3 professores, 4 salas e 6 turmas planejadas. Cada elemento provoca um comportamento
que dá para conferir à mão (roteiro completo em docs/cenario_S0.md):
  MTM1   demanda 5 > 4 vagas (A+B): disputa, lance-hedge, cascata por DUP_COURSE, aluno sem vaga
  INE1   3 alunos para 3 vagas: o professor preferido (prof_ine1) é retirado por evento
  INE2/INE3  mesmos horários e mesma sala preferida: a sala recusa (R-I2 ocupada) e o departamento tenta R-I1
  INE3   eletiva com demanda 3 > 2 vagas: leilão com derrota; carla bloqueada por conflito de horário
  INE4   demanda 1 < min_demand 2: a turma não abre (davi fica com o desejo bloqueado)
  ana evita SEG08: só a MTM1-B é "boa" (bid_single); carla evita TER10/QUI10: só a MTM1-A

S1: 2 departamentos, 8 disciplinas, ~12 turmas, 5 professores, 5 salas e N alunos em 3 fases, gerados com semente.
"""

from __future__ import annotations

import random

from .model import (Course, Event, ProfessorProfile, RoomDef, Scenario, SectionDef, StudentProfile)

DAYS = ["SEG", "TER", "QUA", "QUI", "SEX"]
HOURS = ["08", "10", "14", "16"]
ALL_SLOTS = frozenset(d + h for d in DAYS for h in HOURS)


def s0(event_tick: int = 44) -> Scenario:
    courses = {c.code: c for c in [
        Course("MTM1", "Cálculo I", "MTM"),
        Course("INE1", "Programação", "INE"),
        Course("INE2", "Estruturas de Dados", "INE", ("INE1",)),
        Course("INE3", "Redes de Computadores", "INE"),
        Course("INE4", "Tópicos Especiais", "INE"),
    ]}
    sections = [
        SectionDef("MTM1-A", "MTM1", "MTM", ("SEG08", "QUA08"), 2),
        SectionDef("MTM1-B", "MTM1", "MTM", ("TER10", "QUI10"), 2),
        SectionDef("INE1-A", "INE1", "INE", ("SEG10", "QUA10"), 3),
        SectionDef("INE2-A", "INE2", "INE", ("TER08", "QUI08"), 2),
        SectionDef("INE3-A", "INE3", "INE", ("TER08", "QUI08"), 2),
        SectionDef("INE4-A", "INE4", "INE", ("SEX10", "SEX14"), 2, min_demand=2),
    ]
    students = [
        StudentProfile("ana", frozenset(), ("MTM1", "INE1"), ("INE3",), frozenset({"SEG08"}), 100, 1),
        StudentProfile("bruno", frozenset(), ("MTM1", "INE1"), ("INE3",), frozenset(), 100, 2),
        StudentProfile("carla", frozenset({"INE1"}), ("MTM1", "INE2"), ("INE3",), frozenset({"TER10", "QUI10"}), 100, 5),
        StudentProfile("davi", frozenset({"INE1"}), ("INE2", "MTM1"), ("INE4",), frozenset(), 100, 6),
        StudentProfile("eva", frozenset(), ("MTM1", "INE1"), ("INE3",), frozenset(), 100, 3),
    ]
    professors = [
        ProfessorProfile("prof_mtm1", "MTM", frozenset({"MTM1"}), ALL_SLOTS, frozenset({"SEG08", "QUA08"})),
        ProfessorProfile("prof_ine1", "INE", frozenset({"INE1", "INE3"}), ALL_SLOTS, frozenset({"SEG10", "QUA10"})),
        ProfessorProfile("prof_ine2", "INE", frozenset({"INE1", "INE2", "INE4"}), ALL_SLOTS, frozenset({"TER08", "QUI08"})),
    ]
    rooms = [RoomDef("R-M1", "MTM", 2), RoomDef("R-M2", "MTM", 3), RoomDef("R-I1", "INE", 3), RoomDef("R-I2", "INE", 2)]
    events = [Event(event_tick, "professor_unavailable", "prof_ine1", {"slots": ["SEG10", "QUA10"]})] if event_tick else []
    return Scenario("S0", courses, sections, students, professors, rooms, events,
                    description="cenário controlado para depuração (5 alunos)")


def s1(seed: int = 7, n_students: int = 16) -> Scenario:
    rng = random.Random(seed)
    courses = {c.code: c for c in [
        Course("INE1", "Programação", "INE"), Course("INE2", "Estruturas de Dados", "INE", ("INE1",)),
        Course("INE3", "Sistemas Operacionais", "INE", ("INE2",)), Course("INE4", "Banco de Dados", "INE", ("INE1",)),
        Course("INE5", "Tópicos em IA", "INE"),
        Course("MTM1", "Cálculo I", "MTM"), Course("MTM2", "Cálculo II", "MTM", ("MTM1",)),
        Course("MTM3", "Estatística", "MTM"),
    ]}
    patterns = [("SEG", "QUA"), ("TER", "QUI"), ("QUA", "SEX")]
    sections = []
    for code, c in courses.items():
        n_sec = 2 if code in ("INE1", "INE2", "MTM1", "MTM2") else 1
        for i in range(n_sec):
            d1, d2 = rng.choice(patterns)
            h = rng.choice(HOURS)
            sections.append(SectionDef(f"{code}-{'AB'[i]}", code, c.dept, (d1 + h, d2 + h), rng.randint(3, 5)))
    professors = []
    ine = ["INE1", "INE2", "INE3", "INE4", "INE5"]
    for i in range(3):
        blocked = frozenset(rng.sample(sorted(ALL_SLOTS), 3))
        professors.append(ProfessorProfile(f"p_ine{i+1}", "INE", frozenset(ine[(i + j) % 5] for j in range(3)),
                                           ALL_SLOTS - blocked, frozenset(rng.sample(sorted(ALL_SLOTS), 4)), 6))
    for i in range(2):
        blocked = frozenset(rng.sample(sorted(ALL_SLOTS), 3))
        professors.append(ProfessorProfile(f"p_mtm{i+1}", "MTM", frozenset({"MTM1", "MTM2", "MTM3"}),
                                           ALL_SLOTS - blocked, frozenset(rng.sample(sorted(ALL_SLOTS), 4)), 6))
    rooms = [RoomDef("R-I1", "INE", 4), RoomDef("R-I2", "INE", 5), RoomDef("R-I3", "INE", 6),
             RoomDef("R-M1", "MTM", 5), RoomDef("R-M2", "MTM", 6)]
    levels = {1: ["INE1", "MTM1"], 2: ["INE2", "INE4", "MTM2"], 3: ["INE3"]}
    students = []
    for i in range(n_students):
        lvl = rng.choice([1, 1, 2, 2, 3])
        done = frozenset(c for k, cs in levels.items() if k < lvl for c in cs)
        electives = tuple(rng.sample(["INE5", "MTM3"], rng.randint(1, 2)))
        undesired = frozenset(rng.sample(sorted(ALL_SLOTS), 3))
        students.append(StudentProfile(f"a{i+1:02d}", done, tuple(levels[lvl]), electives, undesired, 100, float(lvl)))
    return Scenario("S1", courses, sections, students, professors, rooms, [],
                    description=f"cenário reduzido gerado (semente {seed}, {n_students} alunos)")


def build(name: str, seed: int = 7, n_students: int = 16, event_tick: int = 44) -> Scenario:
    if name == "S0":
        return s0(event_tick)
    if name == "S1":
        return s1(seed, n_students)
    raise ValueError(f"cenário desconhecido: {name}")
