"""Testes adversariais de robustez: mensagens duplicadas, atrasadas, repetidas e operações concorrentes.

Em todos os casos as invariantes I1-I7 devem valer ao final e nenhum agente pode levantar exceção.
"""
import random

import pytest

from matriculaufsc.bus import Rule
from matriculaufsc.messages import REQUEST
from matriculaufsc.metrics import student_results
from matriculaufsc.scenarios import build, s0, s2
from matriculaufsc.sim import Simulation


def estado(sim):
    reg = sim.registrar
    return ({k: (s.status, dict(s.roster)) for k, s in reg.sections.items()}, dict(reg.points))


def test_T_ADV_01_mensagens_duplicadas_nao_cobram_nem_matriculam_duas_vezes():
    regras = [Rule(action="duplicate", delay=1, performative="request", protocol="registrar")]
    sim = Simulation(s0(), 7, rules=regras).run()
    assert sim.registrar.invariants() == []
    base = Simulation(s0(), 7).run()
    assert estado(sim)[0] == estado(base)[0]          # o mesmo resultado: o duplicado é recusado pelo Registrar
    dup = [r for r in sim.trace.of_kind("registrar") if not r["ok"] and set(r["reasons"]) & {"DUP_SECTION", "ALREADY_OPEN"}]
    assert dup


def test_T_ADV_02_lances_duplicados_contam_uma_vez():
    regras = [Rule(action="duplicate", delay=0, performative="propose", protocol="seat_auction")]
    sim = Simulation(s0(), 7, rules=regras).run()
    base = Simulation(s0(), 7).run()
    assert sim.registrar.invariants() == []
    assert estado(sim)[1] == estado(base)[1]          # pontos gastos idênticos


def test_T_ADV_03_resposta_atrasada_do_registrar_nao_quebra_invariantes():
    regras = [Rule(action="delay", delay=4, sender="registrar")]
    sim = Simulation(s0(), 7, rules=regras).run()
    assert sim.registrar.invariants() == []


def test_T_ADV_04_pedidos_ao_registrar_chegam_fora_de_ordem():
    regras = [Rule(action="delay", delay=2, receiver="registrar", performative="request", max_hits=7)]
    sim = Simulation(s0(), 7, rules=regras).run()
    assert sim.registrar.invariants() == []


def test_T_ADV_05_dois_cancelamentos_simultaneos_reembolsam_uma_vez():
    sim = Simulation(s0(), 7)
    sim.run(until=40)                                   # há matrículas em INE1-A
    sid = "INE1-A"
    assert sim.registrar.sections[sid].roster
    antes = sum(sim.registrar.points.values()) + sum(sum(s.roster.values()) for s in sim.registrar.sections.values())
    dept = sim.departments["INE"]
    for _ in range(2):
        dept.send("registrar", REQUEST, "registrar", f"cancel:{sid}", {"op": "cancel_section", "section": sid})
    sim.step()
    sim.step()
    assert sim.registrar.sections[sid].roster == {}
    depois = sum(sim.registrar.points.values()) + sum(sum(s.roster.values()) for s in sim.registrar.sections.values())
    assert depois == antes                               # pontos conservados: reembolso uma única vez
    assert sim.registrar.invariants() == []


def test_T_ADV_06_cancelamento_concorrente_com_retirada_do_professor():
    sim = Simulation(s0(), 7)
    sim.run(until=43)
    sim.departments["INE"].send("registrar", REQUEST, "registrar", "cancel:INE1-A",
                                {"op": "cancel_section", "section": "INE1-A"})
    sim.run()                                            # o evento do professor chega no tick 44
    assert sim.registrar.invariants() == []


def test_T_ADV_07_troca_com_mensagens_duplicadas_e_atrasadas():
    regras = [Rule(action="duplicate", delay=1, protocol="seat_swap"), Rule(action="delay", delay=1, protocol="registrar", conv_prefix="swap:")]
    sim = Simulation(s2(), 1, rules=regras).run()
    sem = Simulation(s2(), 1, config={"swaps": False}).run()
    assert sim.registrar.invariants() == []
    r, rs = student_results(sim.registrar, s2()), student_results(sem.registrar, s2())
    assert all(r[x]["U"] >= rs[x]["U"] - 1e-9 for x in r)          # com falhas na troca, ninguém fica pior que sem trocas
    assert r["u2"]["S"] == 1.0                                       # e a troca ainda acontece, uma única vez
    assert len([x for x in sim.trace.of_kind("registrar") if x["op"] == "swap_enroll" and x["ok"]]) >= 1


@pytest.mark.parametrize("seed", range(1, 13))
def test_T_ADV_08_caos_aleatorio_de_falhas_preserva_invariantes(seed):
    rnd = random.Random(seed)
    protos = ["seat_auction", "section_opening", "room_reservation", "registrar", "enrollment", "board", "demand",
              "commitment", "seat_swap", "sync"]
    regras = []
    for _ in range(4):
        regras.append(Rule(action=rnd.choice(["drop", "delay", "duplicate"]), delay=rnd.randint(1, 4),
                           protocol=rnd.choice(protos), from_tick=rnd.randint(0, 40), to_tick=rnd.randint(41, 90),
                           max_hits=rnd.choice([None, 2, 5])))
    sc = build("S1", seed, 16)
    sim = Simulation(sc, seed, rules=regras).run()        # não levanta exceção
    assert sim.registrar.invariants() == [], [(r.action, r.protocol) for r in regras]


def test_T_ADV_09_mesma_semente_mesmas_falhas_mesmo_trace():
    def regras():
        return [Rule(action="duplicate", delay=2, protocol="seat_auction"), Rule(action="drop", protocol="board", max_hits=3)]
    a = Simulation(s0(), 7, rules=regras()).run()
    b = Simulation(s0(), 7, rules=regras()).run()
    assert a.trace.digest() == b.trace.digest()
