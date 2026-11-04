"""Leilão de vagas: ordenação de lances, preço, desempate, concorrência, cascata, lances tardios."""
from conftest import fsm_states, mk, notes, run

from matriculaufsc.bus import Rule
from matriculaufsc.model import SectionDef, StudentProfile
from matriculaufsc.scenarios import s0


def enrolled(sim, sid="X-A"):
    return sorted(sim.registrar.sections[sid].roster)


def three_students(**kw):
    return mk(students=[StudentProfile("alto", required=("X",), points=100),
                        StudentProfile("medio", required=("X",), points=60),
                        StudentProfile("baixo", required=("X",), points=30)], **kw)


def test_maiores_lances_vencem_e_pagam_o_proprio_lance():
    sim = run(three_students())
    assert enrolled(sim) == ["alto", "medio"]
    assert sim.registrar.sections["X-A"].roster == {"alto": 100, "medio": 60}
    assert sim.registrar.points == {"alto": 0, "medio": 0, "baixo": 30}
    assert sim.registrar.invariants() == []


def test_preco_uniforme_vencedores_pagam_o_maior_lance_perdedor():
    sim = run(three_students(), pricing="uniform")
    assert sim.registrar.sections["X-A"].roster == {"alto": 30, "medio": 30}
    assert sim.registrar.points["alto"] == 70 and sim.registrar.points["medio"] == 30


def test_perdedor_recebe_reject_e_registra_crenca():
    sim = run(three_students())
    assert sim.students["baixo"].beliefs.get("result:X-A") == "outbid"
    assert sim.students["alto"].beliefs.get("result:X-A") == "won"


def test_empate_resolvido_por_prioridade_e_depois_por_sorteio_com_semente():
    st = [StudentProfile("a", required=("X",), priority=1), StudentProfile("b", required=("X",), priority=5),
          StudentProfile("c", required=("X",), priority=3)]
    assert enrolled(run(mk(students=st))) == ["b", "c"]
    iguais = [StudentProfile(i, required=("X",), priority=2) for i in "abcd"]
    a1, a2 = enrolled(run(mk(students=iguais), seed=3)), enrolled(run(mk(students=iguais), seed=3))
    assert a1 == a2 and len(a1) == 2
    outcomes = {tuple(enrolled(run(mk(students=iguais), seed=s))) for s in range(8)}
    assert len(outcomes) > 1


def test_sem_lance_valido_nao_matricula_ninguem():
    sc = mk(sections=[SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2, min_demand=0)],
            students=[StudentProfile("s1", required=("Y",), completed=frozenset({"X"}))],
            courses=None)
    sim = run(sc)
    assert enrolled(sim) == []
    assert "SemLanceValido" in fsm_states(sim, "seat_auction", "X-A:0")


def test_rodada_seguinte_atende_quem_perdeu_se_surgir_vaga():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 1), SectionDef("X-B", "X", "D", ("TER10", "QUI10"), 1)]
    st = [StudentProfile("a", required=("X",), priority=3), StudentProfile("b", required=("X",), priority=2),
          StudentProfile("c", required=("X",), priority=1)]
    sim = run(mk(sections=secs, students=st, rooms=None), seed=1)
    got = enrolled(sim, "X-A") + enrolled(sim, "X-B")
    assert len(got) == 2 and len(set(got)) == 2 and sim.registrar.invariants() == []


def test_T_PROT_02_lances_tardios_sao_ignorados_e_rejeitados():
    rules = [Rule(action="delay", delay=2, performative="propose", protocol="seat_auction")]
    sim = run(three_students(), rules=rules)
    assert enrolled(sim) == []
    assert any("lance tardio" in n for n in notes(sim))
    assert sim.registrar.invariants() == []


def test_lances_simultaneos_em_varias_turmas_e_cascata_no_registrar():
    """S0: davi vence MTM1-A e também seria vencedor de MTM1-B (hedge) → Registrar recusa DUP_COURSE
    e o departamento promove o próximo da fila (eva)."""
    sim = run(s0(), seed=7)
    fails = [r for r in sim.trace.of_kind("registrar") if not r["ok"] and r["op"] == "commit_enroll"]
    assert fails and fails[0]["student"] == "davi" and "DUP_COURSE" in fails[0]["reasons"]
    assert enrolled(sim, "MTM1-B") == ["ana", "eva"]
    assert enrolled(sim, "MTM1-A") == ["carla", "davi"]
    assert sim.registrar.invariants() == []
    assert "Validando" in fsm_states(sim, "seat_auction", "MTM1-B:0")


def test_T_BDI_02_pontos_consumidos_no_commit_e_nunca_negativos():
    sim = run(s0(), seed=7)
    assert all(p >= 0 for p in sim.registrar.points.values())
    for sid, st in sim.students.items():
        assert st.beliefs.get("points") == sim.registrar.points[sid]


def test_T_PROT_03_lance_abaixo_do_minimo_e_ignorado():
    st = [StudentProfile("alto", required=("X",), points=100), StudentProfile("baixo", required=("X",), points=30)]
    sim = run(mk(students=st, reserve=50))
    assert enrolled(sim) == ["alto"]
    assert sim.registrar.points["baixo"] == 30
