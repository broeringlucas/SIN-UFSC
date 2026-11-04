"""Fábrica de mini-cenários para os testes (pequenos o bastante para conferir à mão)."""
import pytest

from matriculaufsc.model import (Course, ProfessorProfile, RoomDef, Scenario, SectionDef, StudentProfile)
from matriculaufsc.scenarios import ALL_SLOTS
from matriculaufsc.sim import Simulation

FAST = dict(first_round=24, round_period=14, rounds=2)


def mk(sections=None, students=None, profs=None, rooms=None, events=(), courses=None, **cfg) -> Scenario:
    courses = courses or {"X": Course("X", "Disc X", "D"), "Y": Course("Y", "Disc Y", "D", ("X",))}
    sections = sections if sections is not None else [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2)]
    students = students if students is not None else [StudentProfile("s1", required=("X",))]
    profs = profs if profs is not None else [ProfessorProfile("P1", "D", frozenset({"X", "Y"}), ALL_SLOTS)]
    rooms = rooms if rooms is not None else [RoomDef("R1", "D", 3)]
    return Scenario("T", courses, sections, students, profs, rooms, list(events), {**FAST, **cfg})


def run(sc: Scenario, seed: int = 1, rules=(), pricing=None) -> Simulation:
    return Simulation(sc, seed, rules=rules, pricing=pricing).run()


def notes(sim: Simulation) -> list[str]:
    return [r["text"] for r in sim.trace.of_kind("note")]


def fsm_states(sim: Simulation, protocol: str, ref: str) -> list[str]:
    return [r["to"] for r in sim.trace.of_kind("fsm") if r["protocol"] == protocol and r["ref"] == ref]


@pytest.fixture
def s0_sim():
    from matriculaufsc.scenarios import s0
    return run(s0(), seed=7)
