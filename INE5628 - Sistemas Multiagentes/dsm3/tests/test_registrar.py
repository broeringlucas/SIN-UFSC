"""Validação de matrícula e de abertura de turma no Registrar (ponto de commit)."""
from conftest import mk

from matriculaufsc.model import (Course, ProfessorProfile, RoomDef, SectionDef, StudentProfile)
from matriculaufsc.registrar import Registrar
from matriculaufsc.scenarios import ALL_SLOTS


def two_rooms_two_profs():
    return dict(
        profs=[ProfessorProfile("P1", "D", frozenset({"X", "Y", "Z"}), ALL_SLOTS),
               ProfessorProfile("P2", "D", frozenset({"X", "Y", "Z"}), ALL_SLOTS)],
        rooms=[RoomDef("R1", "D", 3), RoomDef("R2", "D", 3)])


def test_T_REG_01_conflito_de_horario():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("Z-A", "Z", "D", ("SEG08", "SEX10"), 2)]
    courses = {"X": Course("X", "x", "D"), "Y": Course("Y", "y", "D", ("X",)), "Z": Course("Z", "z", "D")}
    reg = Registrar(mk(sections=secs, students=[StudentProfile("s1")], courses=courses, **two_rooms_two_profs()))
    assert reg.open_section("X-A", "P1", "R1", 2)[0] and reg.open_section("Z-A", "P2", "R2", 2)[0]
    assert reg.commit_enroll("s1", "X-A", 10) == (True, [])
    ok, why = reg.commit_enroll("s1", "Z-A", 10)
    assert not ok and "TIME_CONFLICT" in why
    assert reg.points["s1"] == 90 and reg.invariants() == []


def test_T_REG_01_prerequisito():
    secs = [SectionDef("Y-A", "Y", "D", ("TER10", "QUI10"), 2)]
    reg = Registrar(mk(sections=secs, students=[StudentProfile("s1"), StudentProfile("s2", completed=frozenset({"X"}))]))
    reg.open_section("Y-A", "P1", "R1", 2)
    ok, why = reg.commit_enroll("s1", "Y-A", 1)
    assert not ok and why == ["PREREQ"]
    assert reg.commit_enroll("s2", "Y-A", 1)[0]


def test_T_REG_02_vagas_esgotadas():
    students = [StudentProfile(f"s{i}") for i in range(3)]
    reg = Registrar(mk(students=students))
    reg.open_section("X-A", "P1", "R1", 2)
    assert reg.commit_enroll("s0", "X-A", 5)[0] and reg.commit_enroll("s1", "X-A", 5)[0]
    ok, why = reg.commit_enroll("s2", "X-A", 5)
    assert not ok and "FULL" in why
    assert reg.seats_left("X-A") == 0 and reg.invariants() == []


def test_disciplina_duplicada_ou_ja_cursada():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("X-B", "X", "D", ("TER08", "QUI08"), 2)]
    reg = Registrar(mk(sections=secs, students=[StudentProfile("s1"), StudentProfile("s2", completed=frozenset({"X"}))],
                       **two_rooms_two_profs()))
    reg.open_section("X-A", "P1", "R1", 2)
    reg.open_section("X-B", "P2", "R2", 2)
    assert reg.commit_enroll("s1", "X-A", 1)[0]
    assert "DUP_COURSE" in reg.commit_enroll("s1", "X-B", 1)[1]
    assert "DUP_COURSE" in reg.commit_enroll("s2", "X-A", 1)[1]


def test_T_REG_01_saldo_insuficiente_e_limite_de_disciplinas():
    reg = Registrar(mk(students=[StudentProfile("s1", points=10, max_courses=0)]))
    reg.open_section("X-A", "P1", "R1", 2)
    ok, why = reg.commit_enroll("s1", "X-A", 11)
    assert not ok and {"BUDGET", "MAX_LOAD"} <= set(why)


def test_turma_nao_aberta_nao_aceita_matricula():
    reg = Registrar(mk())
    assert reg.commit_enroll("s1", "X-A", 1) == (False, ["SECTION_NOT_OPEN"])


def test_cancelamento_reembolsa_e_conserva_pontos():
    students = [StudentProfile("s1", points=100), StudentProfile("s2", points=50)]
    reg = Registrar(mk(students=students))
    reg.open_section("X-A", "P1", "R1", 2)
    reg.commit_enroll("s1", "X-A", 30)
    reg.commit_enroll("s2", "X-A", 20)
    assert reg.invariants() == []
    affected = reg.cancel_section("X-A", block={"prof": "P1", "slots": ["SEG08"]})
    assert {a["student"]: a["refund"] for a in affected} == {"s1": 30, "s2": 20}
    assert reg.points == {"s1": 100, "s2": 50} and reg.invariants() == []
    assert reg.sections["X-A"].status == "CANCELLED"
    assert reg.cancel_section("X-A") == []
    assert "PROF_UNAVAILABLE" in reg.check_open("X-A", "P1", "R1", 2)


def test_T_ROOM_01_abertura_conflito_de_professor_e_de_sala():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("Y-A", "Y", "D", ("SEG08", "SEX10"), 2)]
    reg = Registrar(mk(sections=secs, **two_rooms_two_profs()))
    assert reg.open_section("X-A", "P1", "R1", 2)[0]
    assert reg.check_open("Y-A", "P1", "R2", 2) == ["PROF_CONFLICT"]
    assert reg.check_open("Y-A", "P2", "R1", 2) == ["ROOM_CONFLICT"]
    assert reg.check_open("Y-A", "P2", "R2", 2) == []


def test_T_OPEN_02_abertura_capacidade_e_carga():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 5)]
    sc = mk(sections=secs, profs=[ProfessorProfile("P1", "D", frozenset({"X"}), ALL_SLOTS, max_hours=1)])
    reg = Registrar(sc)
    assert set(reg.check_open("X-A", "P1", "R1", 5)) == {"ROOM_CAPACITY", "PROF_LOAD"}


def test_abertura_e_atomica_falha_nao_deixa_rastro():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2)]
    reg = Registrar(mk(sections=secs))
    reg.prof_avail["P1"].discard("QUA08")
    ok, why = reg.open_section("X-A", "P1", "R1", 2)
    assert not ok and why == ["PROF_UNAVAILABLE"]
    s = reg.sections["X-A"]
    assert (s.status, s.prof, s.room) == ("PLANNED", None, None) and reg.prof_hours("P1") == 0


def test_T_ROOM_01_sala_nao_aceita_reservas_sobrepostas_nem_entre_departamentos():
    courses = {"X": Course("X", "x", "D"), "W": Course("W", "w", "E")}
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("W-A", "W", "E", ("SEG08", "SEX10"), 2)]
    profs = [ProfessorProfile("P1", "D", frozenset({"X"}), ALL_SLOTS), ProfessorProfile("P2", "E", frozenset({"W"}), ALL_SLOTS)]
    reg = Registrar(mk(sections=secs, courses=courses, profs=profs, rooms=[RoomDef("R1", "D", 3), RoomDef("R2", "E", 3)]))
    assert reg.open_section("X-A", "P1", "R1", 2)[0]
    assert reg.check_open("W-A", "P2", "R1", 2) == ["ROOM_CONFLICT"]
    assert reg.check_open("W-A", "P2", "R2", 2) == []
