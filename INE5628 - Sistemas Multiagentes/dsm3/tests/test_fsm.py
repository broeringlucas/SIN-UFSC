import random

import pytest
from conftest import run

from matriculaufsc.bus import Rule
from matriculaufsc.fsm import TABLES, InvalidTransition, check, terminal_states
from matriculaufsc.scenarios import s0, s1


def test_transicoes_validas_das_duas_fsms():
    check("section_opening", "Idle", "AguardandoPropostas")
    check("section_opening", "ConfirmandoRegistrar", "Revertendo")
    check("seat_auction", "AguardandoLances", "Avaliando")
    check("seat_auction", "Validando", "Concluido")


@pytest.mark.parametrize("protocol,frm,to", [
    ("section_opening", "Aberta", "Avaliando"),
    ("section_opening", "Falha", "AguardandoPropostas"),
    ("section_opening", "Idle", "Aberta"),
    ("section_opening", "AguardandoPropostas", "ReservandoSala"),
    ("seat_auction", "Concluido", "AguardandoLances"),
    ("seat_auction", "Idle", "Validando"),
    ("seat_auction", "AguardandoLances", "Validando"),
])
def test_transicoes_invalidas_levantam_erro(protocol, frm, to):
    with pytest.raises(InvalidTransition):
        check(protocol, frm, to)


def test_estados_terminais_declarados():
    assert terminal_states("section_opening") == {"Aberta", "Falha"}
    assert terminal_states("seat_auction") == {"Concluido", "SemLanceValido", "Cancelado"}


def test_tabelas_so_apontam_para_estados_existentes():
    for table in TABLES.values():
        assert all(nxt <= set(table) for nxt in table.values())


def test_T_PROT_01_toda_conversa_termina_em_estado_terminal():
    for sim in (run(s0(), 7), run(s0(36), 7), run(s1(3, 12), 3)):
        last = {}
        for r in sim.trace.of_kind("fsm"):
            last[(r["protocol"], r["ref"])] = r["to"]
        assert last
        for (protocol, _), state in last.items():
            assert state in terminal_states(protocol), (protocol, state)


@pytest.mark.parametrize("event_tick", [28, 29])
def test_T_EVT_01_professor_se_retira_logo_antes_da_rodada_nao_quebra_o_leilao(event_tick):
    sim = run(s0(event_tick), 7)
    assert sim.registrar.invariants() == []
    cancelled = [r for r in sim.trace.of_kind("fsm") if r["protocol"] == "seat_auction" and r["to"] == "Cancelado"]
    assert cancelled


def test_fuzz_de_perdas_e_atrasos_nao_quebra_fsm_nem_invariantes():
    perfs = ["cfp", "propose", "refuse", "accept-proposal", "reject-proposal", "request", "agree", "inform", "failure", "cancel"]
    protos = ["section_opening", "room_reservation", "registrar", "seat_auction", "commitment", "enrollment", "board", "demand"]
    for i in range(80):
        rng = random.Random(i)
        rules = [Rule(action=rng.choice(["drop", "delay"]), performative=rng.choice(perfs + [None]),
                      protocol=rng.choice(protos + [None]), delay=rng.randint(1, 4), from_tick=rng.randint(0, 40),
                      to_tick=rng.randint(20, 80), max_hits=rng.choice([None, 1, 2, 5]))
                 for _ in range(rng.randint(1, 3))]
        sc = s0(rng.choice([0, 28, 36, 44, 50])) if i % 2 == 0 else s1(i, 12)
        assert run(sc, i, rules=rules).registrar.invariants() == []
