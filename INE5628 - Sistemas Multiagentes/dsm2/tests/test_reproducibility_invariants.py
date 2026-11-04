import json

import pytest
from conftest import run

from matriculaufsc.__main__ import main
from matriculaufsc.baselines import compare_policies, opened_snapshot, run_baseline
from matriculaufsc.metrics import student_results, summarize
from matriculaufsc.scenarios import s0, s1


def test_T_REPRO_01_mesma_semente_gera_exatamente_o_mesmo_trace():
    a, b = run(s0(), 7), run(s0(), 7)
    assert a.trace.digest() == b.trace.digest()
    assert run(s1(3, 12), 3).trace.digest() == run(s1(3, 12), 3).trace.digest()


def test_cenarios_s1_com_sementes_diferentes_diferem():
    assert run(s1(1, 12), 1).trace.digest() != run(s1(2, 12), 2).trace.digest()


def test_T_SCEN_01_resultado_de_referencia_do_cenario_s0():
    """Regressão: valores conferidos à mão (docs/cenario_S0.md)."""
    res = student_results(run(s0(), 7).registrar, s0())
    assert {k: round(v["U"], 2) for k, v in res.items()} == {"ana": 0.85, "bruno": 0.70, "carla": 0.85, "davi": 0.85, "eva": 1.0}
    assert res["bruno"]["courses"] == ["INE1", "INE3"]


@pytest.mark.parametrize("seed", range(1, 13))
def test_invariantes_em_varias_sementes_s1(seed):
    sim = run(s1(seed, 16), seed)
    assert sim.registrar.invariants() == []
    assert all(p >= 0 for p in sim.registrar.points.values())


@pytest.mark.parametrize("event_tick", [0, 30, 36, 40, 44, 48, 52, 58])
def test_invariantes_do_s0_com_evento_em_qualquer_fase_do_protocolo(event_tick):
    sim = run(s0(event_tick), 7)
    assert sim.registrar.invariants() == []


def test_T_REPRO_01_baseline_e_sma_nos_mesmos_cenarios_e_sementes():
    for seed in (1, 2, 3):
        sc = s1(seed, 16)
        out = compare_policies(sc, seed)
        assert set(out) == {"auction", "first_come", "priority"}
        assert len({o["turmas_abertas"] for o in out.values()}) == 1
        assert all(o["invariantes_violadas"] == [] and 0 <= o["U_medio"] <= 1 for o in out.values())


def test_politica_prioridade_atende_quem_tem_maior_prioridade_primeiro():
    from conftest import mk
    from matriculaufsc.model import SectionDef, StudentProfile
    sc = mk(sections=[SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 1)],
            students=[StudentProfile("baixa", required=("X",), priority=1), StudentProfile("alta", required=("X",), priority=9)])
    sim = run(sc)
    reg = run_baseline(sc, "priority", 1, opened_snapshot(sim.registrar))
    assert sorted(reg.sections["X-A"].roster) == ["alta"]


def test_politica_ordem_de_chegada_depende_so_da_semente():
    sc = s1(5, 16)
    opened = opened_snapshot(run(sc, 5).registrar)
    a = summarize(run_baseline(sc, "first_come", 5, opened), sc)
    b = summarize(run_baseline(sc, "first_come", 5, opened), sc)
    assert a == b


def test_cli_gera_trace_jsonl_valido(tmp_path, capsys):
    out = tmp_path / "t.jsonl"
    assert main(["--scenario", "S0", "--seed", "7", "--trace", str(out)]) == 0
    lines = out.read_text().splitlines()
    recs = [json.loads(x) for x in lines]
    assert recs[0]["seq"] == 0 and recs[-1]["kind"] == "end" and recs[-1]["invariants"] == []
    assert {"msg", "belief_change", "plan_selected", "intention_change", "reconsider", "fsm", "registrar"} <= {r["kind"] for r in recs}
    assert "Alunos:" in capsys.readouterr().out


def test_cli_compare(capsys):
    assert main(["--scenario", "S1", "--seed", "7", "--policy", "compare"]) == 0
    assert "first_come" in capsys.readouterr().out


def test_explain_mostra_linha_do_tempo_bdi(tmp_path, capsys):
    from matriculaufsc.explain import main as explain
    out = tmp_path / "t.jsonl"
    main(["--scenario", "S0", "--seed", "7", "--trace", str(out)])
    capsys.readouterr()
    assert explain([str(out), "aluno:bruno", "--tick", "30:40"]) == 0
    txt = capsys.readouterr().out
    assert "PLANO" in txt and "bid_hedge" in txt and "RECONSID." in txt


def test_T_OBS_01_toda_mensagem_e_registrada_com_conversa_remetente_destinatario_e_performativa():
    from matriculaufsc.bus import Rule
    sim = run(s0(), 7, rules=[Rule(action="drop", performative="cfp", max_hits=3)])
    recs = sim.trace.of_kind("msg", "msg_dropped")
    assert sorted(r["mid"] for r in recs) == list(range(1, sim.bus._mid + 1))
    assert any(r["kind"] == "msg_dropped" for r in recs)
    assert all(r["conv"] and r["agent"] and r["to"] and r["perf"] for r in recs)


def test_T_PRIV_01_aluno_nunca_recebe_lances_nem_identidade_de_outro_aluno():
    import re
    sim = run(s0(), 7)
    ids = [s.sid for s in s0().students]
    for r in sim.trace.of_kind("msg"):
        if not r["to"].startswith("aluno:"):
            continue
        me = r["to"].split(":", 1)[1]
        text = json.dumps(r["content"], ensure_ascii=False)
        assert '"bid"' not in text
        assert not [o for o in ids if o != me and re.search(rf"\b{o}\b", text)], (r["to"], text)
    assert all(re.fullmatch(r"a\d\d", s.sid) for s in s1(1, 12).students)
