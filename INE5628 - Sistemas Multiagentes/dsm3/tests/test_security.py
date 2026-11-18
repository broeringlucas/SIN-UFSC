"""Autorização e validação nas fronteiras dos protocolos (resposta ao feedback da DSM2).

Reproduz os ataques descritos pelo professor e outros: remetente inexistente, remetente falsificado, papel errado,
dono errado, conteúdo malformado (NaN, falta de campo, tipo errado). Em todos os casos a operação é recusada e o
estado institucional (turmas, pontos, disponibilidade) permanece idêntico.
"""
import copy
import math

import pytest
from conftest import mk

from matriculaufsc.messages import CANCEL, FAILURE, INFORM, PROPOSE, REQUEST
from matriculaufsc.model import Course, ProfessorProfile, RoomDef, SectionDef, StudentProfile
from matriculaufsc.scenarios import ALL_SLOTS
from matriculaufsc.sim import Simulation

TICK_OPEN = 14  # turma X-A aberta; antes da primeira rodada de leilão (first_round=24)


def cenario():
    courses = {"X": Course("X", "x", "D"), "W": Course("W", "w", "E")}
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("W-A", "W", "E", ("TER08", "QUI08"), 2)]
    profs = [ProfessorProfile("P1", "D", frozenset({"X"}), ALL_SLOTS), ProfessorProfile("P2", "D", frozenset({"X"}), ALL_SLOTS),
             ProfessorProfile("Q1", "E", frozenset({"W"}), ALL_SLOTS)]
    rooms = [RoomDef("R1", "D", 3), RoomDef("R2", "E", 3)]
    studs = [StudentProfile("s1", required=("X", "W")), StudentProfile("s2", required=("X",))]
    return mk(sections=secs, students=studs, profs=profs, rooms=rooms, courses=courses)


def sim_aberta():
    sim = Simulation(cenario(), seed=1)
    sim.run(until=TICK_OPEN)
    assert sim.registrar.sections["X-A"].status == "OPEN" and sim.registrar.sections["W-A"].status == "OPEN"
    return sim


def estado(sim):
    reg = sim.registrar
    return copy.deepcopy((
        {k: (s.status, s.prof, s.room, s.capacity, dict(s.roster)) for k, s in reg.sections.items()},
        dict(reg.points), {k: set(v) for k, v in reg.prof_avail.items()}))


def processa(sim, ticks=3):
    for _ in range(ticks):
        sim.step()


def injeta_no_barramento(sim, sender, receiver, perf, protocol, conv, content):
    """Ataque com acesso direto ao barramento (ignora a fronteira do Ambiente): testa o dono do estado."""
    sim.bus.send(sim.tick, sender, receiver, perf, protocol, conv, content)


# --- achado 1: cancelamento em nome de aluno inexistente ---------------------------------------------------------
CANCEL_X = {"op": "cancel_section", "section": "X-A", "reason": "ataque"}


def test_T_SEC_01_cancelamento_por_aluno_inexistente_via_ambiente_e_rejeitado_na_fronteira():
    sim = sim_aberta()
    antes = estado(sim)
    r = sim.env.execute(sim.tick, "aluno:fantasma", "registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    assert r is None
    processa(sim)
    assert estado(sim) == antes
    assert sim.trace.of_kind("msg_rejected")[-1]["reasons"] == ["remetente não autenticado"]


def test_T_SEC_02_cancelamento_por_aluno_inexistente_direto_no_barramento_e_negado_pelo_registrar():
    sim = sim_aberta()
    antes = estado(sim)
    injeta_no_barramento(sim, "aluno:fantasma", "registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    processa(sim)
    assert estado(sim) == antes
    assert sim.registrar.invariants() == []
    den = sim.trace.of_kind("registrar_denied")
    assert den and "INVALID_MESSAGE" in den[-1]["reasons"][0]


def test_T_SEC_03_cancelamento_por_aluno_real_nao_e_permitido():
    sim = sim_aberta()
    antes = estado(sim)
    cred = sim.students["s1"]
    r = cred.send("registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    assert r is None
    injeta_no_barramento(sim, "aluno:s1", "registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    processa(sim)
    assert estado(sim) == antes


def test_T_SEC_04_departamento_de_outro_departamento_nao_cancela_turma_alheia():
    sim = sim_aberta()
    antes = estado(sim)
    sim.departments["E"].send("registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    processa(sim)
    assert estado(sim) == antes
    den = sim.trace.of_kind("registrar_denied")
    assert den and den[-1]["reasons"][0].startswith("UNAUTHORIZED")


def test_T_SEC_05_cancelamento_com_conversa_de_outra_turma_e_negado():
    sim = sim_aberta()
    antes = estado(sim)
    sim.departments["D"].send("registrar", REQUEST, "registrar", "cancel:OUTRA", CANCEL_X)
    processa(sim)
    assert estado(sim) == antes


def test_T_SEC_06_cancelamento_legitimo_do_proprio_departamento_continua_funcionando():
    sim = sim_aberta()
    sim.departments["D"].send("registrar", REQUEST, "registrar", "cancel:X-A", CANCEL_X)
    processa(sim, 2)
    assert sim.registrar.sections["X-A"].status != "OPEN"


# --- achado 2: falsa retirada de professor -----------------------------------------------------------------------
RETIRADA = {"section": "X-A", "prof": "P1", "slots": ["SEG08", "QUA08"]}


def prof_da_turma(sim):
    return sim.registrar.sections["X-A"].prof


def test_T_SEC_07_retirada_falsa_de_participante_inexistente_nao_cancela_a_turma():
    sim = sim_aberta()
    antes = estado(sim)
    pid = prof_da_turma(sim)
    r = sim.env.execute(sim.tick, "prof:fantasma", "dept:D", INFORM, "commitment", "withdraw:X-A",
                        {**RETIRADA, "prof": pid}, credential="x")
    assert r is None
    injeta_no_barramento(sim, "prof:fantasma", "dept:D", INFORM, "commitment", "withdraw:X-A", {**RETIRADA, "prof": pid})
    processa(sim, 4)
    assert estado(sim) == antes
    assert any("retirada" in r["why"] for r in sim.trace.of_kind("msg_denied"))


def test_T_SEC_08_retirada_enviada_por_outro_professor_real_e_ignorada():
    sim = sim_aberta()
    antes = estado(sim)
    dono = prof_da_turma(sim)
    outro = "P2" if dono == "P1" else "P1"
    sim.professors[outro].send("dept:D", INFORM, "commitment", "withdraw:X-A", {"section": "X-A", "prof": dono, "slots": ["SEG08"]})
    sim.professors[outro].send("dept:D", INFORM, "commitment", "withdraw:X-A", {"section": "X-A", "prof": outro, "slots": ["SEG08"]})
    processa(sim, 4)
    assert estado(sim) == antes


def test_T_SEC_09_retirada_legitima_do_professor_responsavel_continua_valendo():
    sim = sim_aberta()
    dono = prof_da_turma(sim)
    sim.professors[dono].send("dept:D", INFORM, "commitment", "withdraw:X-A", {"section": "X-A", "prof": dono, "slots": ["SEG08"]})
    processa(sim, 4)
    assert "SEG08" not in sim.registrar.prof_avail[dono]


# --- achado 3: custo NaN -----------------------------------------------------------------------------------------
@pytest.mark.parametrize("preco", [float("nan"), float("inf"), -float("inf"), -1, 2.5, "10", True, None, 10**12])
def test_T_SEC_10_matricula_com_preco_invalido_e_recusada_sem_alterar_saldo(preco):
    sim = sim_aberta()
    antes = estado(sim)
    msg = {"op": "commit_enroll", "student": "s2", "section": "X-A", "price": preco}
    sim.departments["D"].send("registrar", REQUEST, "registrar", "auc:X-A:0", msg)
    injeta_no_barramento(sim, "dept:D", "registrar", REQUEST, "registrar", "auc:X-A:0", msg)
    processa(sim)
    assert estado(sim) == antes
    assert sim.registrar.invariants() == []
    assert all(isinstance(v, int) and not isinstance(v, bool) for v in sim.registrar.points.values())


def test_T_SEC_11_registrar_direto_tambem_recusa_preco_nao_finito():
    sim = sim_aberta()
    reg = sim.registrar
    ok, why = reg.commit_enroll("s2", "X-A", math.nan)
    assert not ok and "BUDGET" in why
    assert reg.points["s2"] == 100 and reg.invariants() == []


# --- achado 4: requisição sem o campo "op" -----------------------------------------------------------------------
@pytest.mark.parametrize("conteudo", [{}, {"section": "X-A"}, {"op": None}, {"op": 7}, {"op": "apagar_tudo"}, "texto", [1], None])
def test_T_SEC_12_requisicao_sem_op_ou_malformada_nao_interrompe_o_processamento(conteudo):
    sim = sim_aberta()
    antes = estado(sim)
    injeta_no_barramento(sim, "dept:D", "registrar", REQUEST, "registrar", "open:X-A", conteudo)
    sim.departments["D"].send("registrar", REQUEST, "registrar", "open:X-A", conteudo)
    processa(sim, 3)  # não levanta exceção
    assert estado(sim) == antes
    assert sim.trace.of_kind("registrar_denied") or sim.trace.of_kind("msg_rejected")
    sim.run(until=60)
    assert sim.registrar.invariants() == []


# --- contratos genéricos -----------------------------------------------------------------------------------------
@pytest.mark.parametrize("perf,protocol,conv,conteudo", [
    (INFORM, "demand", "demand:X", {"course": "X"}),                                  # falta student
    (INFORM, "demand", "demand:X", {"course": "X", "student": "s1", "extra": 1}),     # campo desconhecido
    (INFORM, "demand", "demand:X", {"course": 5, "student": "s1"}),                   # tipo errado
    (INFORM, "desconhecido", "demand:X", {}),                                         # protocolo desconhecido
    (CANCEL, "demand", "demand:X", {"course": "X", "student": "s1"}),                 # performativa errada
    (INFORM, "demand", "qualquer coisa", {"course": "X", "student": "s1"}),           # conv fora do formato
])
def test_T_SEC_13_mensagens_fora_do_contrato_sao_rejeitadas_pelo_ambiente(perf, protocol, conv, conteudo):
    sim = sim_aberta()
    r = sim.students["s1"].send("dept:D", perf, protocol, conv, conteudo)
    assert r is None
    assert sim.trace.of_kind("msg_rejected")[-1]["reasons"]


def test_T_SEC_14_aluno_nao_se_passa_por_outro_aluno_nem_por_departamento():
    sim = sim_aberta()
    cred = sim.students["s1"]._credential
    for sender in ("aluno:s2", "dept:D", "registrar", "env"):
        r = sim.env.execute(sim.tick, sender, "dept:D", INFORM, "demand", "demand:X",
                            {"course": "X", "student": "s2"}, credential=cred)
        assert r is None
    assert [x["reasons"] for x in sim.trace.of_kind("msg_rejected")[-4:]] == [["remetente não autenticado"]] * 4


def test_T_SEC_15_demanda_em_nome_de_outro_aluno_e_negada_pelo_departamento():
    sim = Simulation(cenario(), seed=1)
    sim.run(until=0)
    sim.students["s1"].send("dept:D", INFORM, "demand", "demand:X", {"course": "X", "student": "s2"})
    processa(sim, 2)
    assert any("outro aluno" in r["why"] for r in sim.trace.of_kind("msg_denied"))


def test_T_SEC_16_lance_de_aluno_desconhecido_ou_fora_da_rodada_e_negado():
    sim = Simulation(cenario(), seed=1)
    sim.run(until=26)  # leilão da rodada 0 em andamento
    injeta_no_barramento(sim, "aluno:fantasma", "dept:D", PROPOSE, "seat_auction", "auc:X-A:0",
                         {"section": "X-A", "bid": 100, "round": 0})
    injeta_no_barramento(sim, "aluno:s2", "dept:D", PROPOSE, "seat_auction", "auc:X-A:0",
                         {"section": "X-A", "bid": 100, "round": 7})
    processa(sim, 2)
    assert len(sim.trace.of_kind("msg_denied")) >= 2
    assert sim.registrar.invariants() == []


def test_T_SEC_17_sala_so_obedece_ao_proprio_departamento():
    sim = sim_aberta()
    sala = sim.rooms["R1"]
    antes = dict(sala.booked)
    sim.departments["E"].send("room:R1", CANCEL, "room_reservation", "cancel:X-A", {"section": "X-A"})
    injeta_no_barramento(sim, "dept:E", "room:R1", CANCEL, "room_reservation", "cancel:X-A", {"section": "X-A"})
    processa(sim, 3)
    assert dict(sala.booked) == antes
    assert any("departamento da sala" in r["why"] for r in sim.trace.of_kind("msg_denied"))


def test_T_SEC_18_caixa_de_entrada_malformada_nao_derruba_nenhum_agente():
    """Fuzz de conteúdo: mensagens lixo entregues diretamente a todos os agentes; ninguém levanta exceção."""
    sim = sim_aberta()
    lixo = [{}, None, "x", {"section": None}, {"section": "X-A", "bid": math.nan}, {"kind": 3}, {"op": {}}, [1, 2]]
    alvos = ["dept:D", "dept:E", "prof:P1", "room:R1", "aluno:s1", "registrar"]
    for alvo in alvos:
        for protocolo in ("demand", "board", "section_opening", "room_reservation", "registrar", "seat_auction",
                          "enrollment", "commitment", "event"):
            for perf in ("inform", "request", "cfp", "propose", "cancel", "agree", "accept-proposal"):
                for c in lixo:
                    injeta_no_barramento(sim, "aluno:fantasma", alvo, perf, protocolo, "c1", c)
    antes = estado(sim)
    processa(sim, 3)
    assert estado(sim) == antes
    sim.run(until=sim.cfg.end_tick())
    assert sim.registrar.invariants() == []
