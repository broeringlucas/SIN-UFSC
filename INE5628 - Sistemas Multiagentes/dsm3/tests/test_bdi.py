"""Ciclo BDI: crenças, desejos, seleção de plano, reconsideração e política de compromisso — tudo no trace."""
from matriculaufsc.scenarios import s0


def of(sim, kind, agent=None, **kw):
    return sim.trace.where(kind, agent, **kw)


def test_mudanca_de_crenca_registra_valor_antigo_novo_e_causa(s0_sim):
    r = [x for x in of(s0_sim, "belief_change", "aluno:ana", key="board_published") if x["new"] is True]
    assert r and r[0]["old"] is False and r[0]["cause"] == "oferta publicada"


def test_T_BDI_01_selecao_de_plano_registra_opcoes_e_escolha(s0_sim):
    sels = [x for x in of(s0_sim, "plan_selected", "aluno:bruno") if x["desire"] == "obtain:MTM1"]
    assert sels[0]["chosen"] == "signal_demand"
    sel = sels[1]
    assert sel["chosen"] == "bid_hedge"
    assert dict(sel["options"]) == {"bid_single": 1.0, "bid_hedge": 1.5}


def test_T_BDI_01_preferencia_de_horario_muda_o_plano_do_aluno(s0_sim):
    """ana evita SEG08: só MTM1-B é boa → bid_single em B; carla evita TER10/QUI10 → só MTM1-A."""
    pick = lambda who: [x for x in of(s0_sim, "intention_change", f"aluno:{who}", action="adotada")
                        if x["plan"].startswith("bid") and x["targets"] and x["targets"][0].startswith("MTM1")][0]
    assert pick("ana")["targets"] == ["MTM1-B"] and pick("ana")["plan"] == "bid_single"
    assert pick("carla")["targets"] == ["MTM1-A"]


def test_reconsideracao_abandona_intencao_quando_a_crenca_invalida_o_plano(s0_sim):
    r = [x for x in of(s0_sim, "reconsider", "aluno:bruno")
         if x["decision"] == "abandonada" and "board_published" in x["changed"]]
    assert len(r) == 3
    assert {x["plan"] for x in of(s0_sim, "intention_change", "aluno:bruno", action="adotada") if x["tick"] == r[0]["tick"]} \
        == {"bid_single", "bid_hedge"}


def test_compromisso_single_minded_mantem_intencao_quando_plano_continua_valido(s0_sim):
    kept = [x for x in of(s0_sim, "reconsider", "aluno:bruno") if x["decision"] == "mantida"]
    assert kept and "result:MTM1-A" in kept[0]["changed"]
    prof = [x for x in of(s0_sim, "reconsider", "prof:prof_ine1") if x["decision"] == "mantida"]
    assert prof


def test_T_EVT_01_evento_do_ambiente_dispara_reconsideracao_e_troca_de_plano_do_professor(s0_sim):
    ev = of(s0_sim, "event")[0]
    drops = [x for x in of(s0_sim, "reconsider", "prof:prof_ine1") if x["decision"] == "abandonada"]
    assert len(drops) == 1 and drops[0]["tick"] > ev["tick"]
    sel = [x for x in of(s0_sim, "plan_selected", "prof:prof_ine1") if x["desire"] == "deliver:INE1-A"]
    assert [x["chosen"] for x in sel] == ["keep_commitment", "withdraw"]


def test_desejo_reativado_apos_cancelamento_e_depois_realizado(s0_sim):
    seq = [(x["old"], x["new"]) for x in of(s0_sim, "desire_change", "aluno:bruno") if x["desire"] == "obtain:INE1"]
    assert seq == [(None, "active"), ("active", "achieved"), ("achieved", "active"), ("active", "blocked"),
                   ("blocked", "active"), ("active", "achieved")]


def test_desejo_bloqueado_quando_nao_ha_oferta(s0_sim):
    seq = [(x["new"], x["reason"]) for x in of(s0_sim, "desire_change", "aluno:davi") if x["desire"] == "obtain:INE4"]
    assert seq[-1][0] == "blocked"
    assert s0_sim.registrar.sections["INE4-A"].status == "PLANNED"


def test_conflito_de_horario_entre_desejos_bloqueia_o_de_menor_peso(s0_sim):
    """carla: INE2-A e INE3-A têm o mesmo horário; a obrigatória reserva o horário e a eletiva fica bloqueada."""
    assert [x["new"] for x in of(s0_sim, "desire_change", "aluno:carla") if x["desire"] == "obtain:INE3"][-1] == "blocked"
    assert "INE3" not in s0_sim.registrar.enrolled_courses("carla")


def test_aluno_sem_cenario_de_evento_nao_reativa_desejos():
    sim = __import__("conftest").run(s0(event_tick=0), seed=7)
    assert not [x for x in of(sim, "desire_change") if x["old"] == "achieved"]


def test_aluno_nao_volta_a_dar_lance_em_turma_que_ja_rejeitou_seu_lance():
    from conftest import mk
    from matriculaufsc.agents.bdi import Desire
    from matriculaufsc.agents.student import Student
    from matriculaufsc.environment import Environment
    from matriculaufsc.model import StudentProfile
    from matriculaufsc.trace import TraceLogger

    sc = mk()
    st = Student(StudentProfile("s1", required=("X",)), sc, Environment(sc, TraceLogger()), TraceLogger())
    st.beliefs.set("sec:X-A", {"course": "X", "slots": ["SEG08", "QUA08"], "remaining": 2, "dept": "D"})
    d = Desire("obtain:X", "obtain", 0.6, {"course": "X", "required": True})
    assert st.candidates(d) == [(0, "X-A")]
    st.beliefs.set("result:X-A", "violação:TIME_CONFLICT")
    assert st.candidates(d) == []
