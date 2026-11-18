"""Recuperação de crenças desatualizadas: o aluno que perdeu o quadro de ofertas pede o quadro ao departamento."""
from conftest import mk

from matriculaufsc.bus import Rule
from matriculaufsc.model import ProfessorProfile, RoomDef, SectionDef, StudentProfile
from matriculaufsc.scenarios import ALL_SLOTS, s0
from matriculaufsc.sim import Simulation


def cenario(rounds=3):
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2)]
    studs = [StudentProfile("s1", required=("X",)), StudentProfile("s2", required=("X",))]
    return mk(sections=secs, students=studs, first_round=24, round_period=14, rounds=rounds)


def perde_primeiro_quadro(aluno):
    """Perde todos os quadros enviados até o início da rodada 0 (publicação do departamento); o reenvio por sync passa."""
    return Rule(action="drop", receiver=f"aluno:{aluno}", protocol="board", to_tick=24)


def matriculados(sim):
    return sorted(sim.registrar.sections["X-A"].roster)


def test_T_SYNC_01_sem_falhas_ninguem_pede_sincronizacao():
    sim = Simulation(cenario(), 1).run()
    assert not [r for r in sim.trace.of_kind("msg") if r["protocol"] == "sync"]
    assert matriculados(sim) == ["s1", "s2"]


def test_T_SYNC_02_sem_recuperacao_o_aluno_que_perdeu_o_quadro_fica_de_fora():
    sim = Simulation(cenario(rounds=1), 1, rules=[perde_primeiro_quadro("s2")], config={"sync": False}).run()
    assert matriculados(sim) == ["s1"]
    assert sim.students["s2"].beliefs.get("sec:X-A") is None          # crença nunca corrigida


def test_T_SYNC_03_com_recuperacao_o_aluno_pede_o_quadro_e_ainda_da_o_lance_a_tempo():
    sim = Simulation(cenario(rounds=1), 1, rules=[perde_primeiro_quadro("s2")], config={"bid_window": 4}).run()
    assert matriculados(sim) == ["s1", "s2"]
    assert [r["perf"] for r in sim.trace.of_kind("msg") if r["protocol"] == "sync"] == ["request"]
    assert any("quadro recuperado a tempo" in n["text"] for n in sim.trace.of_kind("note"))
    assert sim.students["s2"].beliefs.get("sec:X-A") is not None


def test_T_SYNC_04_sem_janela_suficiente_a_recuperacao_chega_tarde_e_o_lance_e_descartado():
    sim = Simulation(cenario(rounds=1), 1, rules=[perde_primeiro_quadro("s2")]).run()   # bid_window padrão = 2
    assert matriculados(sim) == ["s1"]                         # o quadro volta, mas depois do fechamento
    assert sim.students["s2"].beliefs.get("sec:X-A") is not None
    assert sim.registrar.invariants() == []


def test_T_SYNC_05_pedido_em_excesso_e_limitado_pelo_intervalo_minimo():
    sim = Simulation(cenario(), 1, rules=[Rule(action="drop", receiver="aluno:s2", protocol="board")]).run()
    pedidos = [r["tick"] for r in sim.trace.of_kind("msg") if r["protocol"] == "sync"]
    assert all(b - a >= 6 for a, b in zip(pedidos, pedidos[1:]))


def test_T_SYNC_06_s0_nao_muda_com_a_recuperacao_ligada():
    assert Simulation(s0(), 7).run().trace.digest().startswith("63e955f610e43987")
