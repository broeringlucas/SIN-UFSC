import random

import pytest

from matriculaufsc.utility import THETA, utility


def test_utilidade_sempre_em_0_1_mesmo_com_entradas_extremas():
    rng = random.Random(0)
    slots = [d + h for d in ("SEG", "TER", "QUA") for h in ("08", "10")]
    for _ in range(2000):
        req = rng.sample("ABCDEF", rng.randint(0, 5))
        ele = rng.sample("UVWXYZ", rng.randint(0, 4))
        got = set(rng.sample("ABCDEFUVWXYZ", rng.randint(0, 12)))
        sched = rng.sample(slots, rng.randint(0, 6))
        und = rng.sample(slots, rng.randint(0, 6))
        r = utility(req, ele, got, sched, und)
        assert 0.0 <= r["U"] <= 1.0 + 1e-12
        assert all(0.0 <= r[k] <= 1.0 for k in "RSE")


def test_anotacao_3_do_professor_obter_mais_do_que_o_desejado_nao_passa_de_1():
    r = utility(["A"], ["U"], {"A", "B", "C", "U", "V"}, ["SEG08"], [])
    assert r["U"] == pytest.approx(1.0)


def test_pesos_somam_um_e_caso_perfeito_vale_1():
    r = utility(["A", "B"], ["U"], {"A", "B", "U"}, ["SEG08", "QUA08"], ["SEX16"])
    assert (r["R"], r["S"], r["E"]) == (1, 1, 1) and r["U"] == pytest.approx(1.0)


def test_componentes_individuais():
    r = utility(["A", "B"], ["U", "V"], {"A", "U"}, ["SEG08", "SEG10", "TER08", "TER10"], ["SEG08"])
    assert r["R"] == 0.5 and r["E"] == 0.5 and r["S"] == 0.75
    assert r["U"] == pytest.approx(0.6 * 0.5 + 0.25 * 0.75 + 0.15 * 0.5)


def test_sem_nada_desejado_cada_razao_vale_1():
    r = utility([], [], set(), ["SEG08"], [])
    assert r["R"] == 1 and r["E"] == 1 and r["U"] == pytest.approx(1.0)


def test_grade_vazia_com_desejos_tem_utilidade_zero():
    r = utility(["A"], ["U"], set(), [], [])
    assert r["S"] == 0 and r["U"] == 0 and not r["satisfatoria"]


def test_limiar_theta_tem_significado():
    assert THETA == 0.70
    assert utility(["A"], [], {"A"}, ["SEG08"], ["SEG08"])["satisfatoria"]
    r = utility(["A", "B"], ["U"], {"A", "U"}, ["SEG08"], [])
    assert r["U"] == pytest.approx(0.70) and r["satisfatoria"]
    assert not utility(["A", "B"], ["U"], {"A", "U"}, ["SEG08"], ["SEG08"])["satisfatoria"]
