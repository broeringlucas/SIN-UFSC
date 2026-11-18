"""Protocolo seat_swap: troca atômica de turmas entre dois alunos (mediada pelo departamento).

Cobre: Registrar (atomicidade, idempotência, validações), máquina de estados do departamento, caminho nominal no
cenário S2, falhas (recusa do parceiro, parceiro sem resposta, resposta do Registrar perdida, turma cancelada no meio),
autorização, concorrência e a propriedade global (invariantes preservadas em muitas sementes).
"""
import copy

import pytest
from conftest import mk

from matriculaufsc.bus import Rule
from matriculaufsc.fsm import InvalidTransition, check, terminal_states
from matriculaufsc.messages import REQUEST
from matriculaufsc.metrics import student_results
from matriculaufsc.model import Course, ProfessorProfile, RoomDef, Scenario, SectionDef, StudentProfile
from matriculaufsc.registrar import Registrar
from matriculaufsc.scenarios import ALL_SLOTS, build, s2
from matriculaufsc.sim import Simulation


# --- Registrar: troca atômica ------------------------------------------------------------------------------------
def reg_dois_alunos(**kw):
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("X-B", "X", "D", ("TER10", "QUI10"), 2),
            SectionDef("Z-A", "Z", "D", ("TER10", "SEX14"), 2)]
    courses = {"X": Course("X", "x", "D"), "Z": Course("Z", "z", "D")}
    profs = [ProfessorProfile(p, "D", frozenset({"X", "Z"}), ALL_SLOTS) for p in ("P1", "P2", "P3")]
    rooms = [RoomDef(r, "D", 3) for r in ("R1", "R2", "R3")]
    studs = [StudentProfile("a", required=("X",)), StudentProfile("b", required=("X",)),
             StudentProfile("c", required=("X", "Z"))]
    reg = Registrar(mk(sections=secs, students=studs, profs=profs, rooms=rooms, courses=courses, **kw))
    reg.open_section("X-A", "P1", "R1", 2)
    reg.open_section("X-B", "P2", "R2", 2)
    reg.open_section("Z-A", "P3", "R3", 2)
    assert reg.commit_enroll("a", "X-A", 30)[0] and reg.commit_enroll("b", "X-B", 55)[0]
    return reg


def test_T_SWAP_01_troca_atomica_preserva_vagas_e_pontos():
    reg = reg_dois_alunos()
    pontos = dict(reg.points)
    assert reg.swap_enroll("a", "X-A", "b", "X-B") == (True, [])
    assert reg.sections["X-A"].roster == {"b": 55} and reg.sections["X-B"].roster == {"a": 30}
    assert reg.points == pontos            # ninguém paga nem recebe: cada um leva o preço que pagou
    assert reg.invariants() == []


@pytest.mark.parametrize("args,motivo", [
    (("a", "X-A", "a", "X-B"), "SAME_STUDENT"),
    (("a", "X-A", "b", "X-A"), "SAME_SECTION"),
    (("a", "X-B", "b", "X-A"), "NOT_ENROLLED_A"),   # a não está em X-B
    (("zz", "X-A", "b", "X-B"), "UNKNOWN"),
    (("a", "X-A", "b", "Z-A"), "DIFF_COURSE"),
])
def test_T_SWAP_02_troca_invalida_nao_altera_nada(args, motivo):
    reg = reg_dois_alunos()
    antes = copy.deepcopy(({k: dict(s.roster) for k, s in reg.sections.items()}, dict(reg.points)))
    ok, why = reg.swap_enroll(*args)
    assert not ok and motivo in why
    assert ({k: dict(s.roster) for k, s in reg.sections.items()}, dict(reg.points)) == antes


def test_T_SWAP_03_conflito_de_horario_de_quem_recebe_barra_a_troca():
    reg = reg_dois_alunos()
    # c cursa Z-A (TER10, SEX14) e X-A: trocar X-A por X-B (TER10/QUI10) conflita em TER10
    assert reg.commit_enroll("c", "X-A", 1)[0] and reg.commit_enroll("c", "Z-A", 1)[0]
    ok, why = reg.swap_enroll("c", "X-A", "b", "X-B")
    assert not ok and why == ["TIME_CONFLICT_A"]
    assert reg.sections["X-A"].roster.keys() == {"a", "c"} and reg.invariants() == []


def test_T_SWAP_04_turma_fechada_barra_a_troca():
    reg = reg_dois_alunos()
    reg.cancel_section("X-B")
    ok, why = reg.swap_enroll("a", "X-A", "b", "X-B")
    assert not ok and "SECTION_NOT_OPEN" in why


def test_T_SWAP_05_idempotente_por_conversa():
    reg = reg_dois_alunos()
    assert reg.swap_enroll("a", "X-A", "b", "X-B", "swap:a:X-A:X-B:1")[0]
    depois = {k: dict(s.roster) for k, s in reg.sections.items()}
    assert reg.swap_enroll("a", "X-A", "b", "X-B", "swap:a:X-A:X-B:1") == (True, [])   # reenvio: mesmo resultado
    assert {k: dict(s.roster) for k, s in reg.sections.items()} == depois            # e não desfaz nem repete


# --- máquina de estados --------------------------------------------------------------------------------------------
def test_T_SWAP_06_fsm_transicoes_validas_e_invalidas():
    check("seat_swap", "Idle", "Procurando")
    check("seat_swap", "AguardandoParceiro", "ConfirmandoRegistrar")
    for frm, to in [("Idle", "Concluida"), ("Concluida", "Procurando"), ("Falha", "Procurando"),
                    ("Procurando", "Concluida"), ("AguardandoParceiro", "Concluida")]:
        with pytest.raises(InvalidTransition):
            check("seat_swap", frm, to)
    assert terminal_states("seat_swap") == {"Concluida", "Falha"}


# --- caminho nominal (cenário S2) ---------------------------------------------------------------------------------
def estados(sim, ref_prefix="swap:"):
    return [r["to"] for r in sim.trace.of_kind("fsm") if r["protocol"] == "seat_swap" and r["ref"].startswith(ref_prefix)]


def matriculas(sim):
    return {sid: sorted(s.roster) for sid, s in sim.registrar.sections.items()}


def test_T_SWAP_07_s2_troca_melhora_a_aluna_sem_piorar_ninguem():
    com = Simulation(s2(), 1).run()
    sem = Simulation(s2(), 1, config={"swaps": False}).run()
    rc, rs = student_results(com.registrar, s2()), student_results(sem.registrar, s2())
    assert rs["u2"]["S"] == 0.0 and rc["u2"]["S"] == 1.0            # u2 sai do horário indesejado
    assert all(rc[s]["U"] >= rs[s]["U"] for s in rs)                 # ninguém piora
    assert rc["u2"]["U"] > rs["u2"]["U"]
    assert estados(com) == ["Procurando", "AguardandoParceiro", "ConfirmandoRegistrar", "Concluida"]
    assert com.registrar.invariants() == [] and sem.registrar.invariants() == []


def test_T_SWAP_08_crencas_dos_alunos_acompanham_o_resultado_da_troca():
    sim = Simulation(s2(), 1).run()
    for sid, aluno in sim.students.items():
        reais = {s for s, sec in sim.registrar.sections.items() if sid in sec.roster}
        assert set(aluno.enrolled()) == reais, sid
    u2 = sim.students["u2"]
    assert u2.beliefs.get("swap_pending:C") is None
    assert any(r["key"] == "enrolled" and "troca concluída" in r["cause"]
               for r in sim.trace.of_kind("belief_change") if r["agent"] == "aluno:u2")


def test_T_SWAP_09_trace_registra_pedido_consulta_aceite_e_commit():
    sim = Simulation(s2(), 1).run()
    msgs = [(r["perf"], r["protocol"]) for r in sim.trace.of_kind("msg") if r["protocol"] == "seat_swap"]
    assert msgs[:3] == [("request", "seat_swap"), ("cfp", "seat_swap"), ("agree", "seat_swap")]
    assert msgs.count(("inform", "seat_swap")) == 2                  # resultado para os dois alunos
    ops = [r for r in sim.trace.of_kind("registrar") if r["op"] == "swap_enroll"]
    assert len(ops) == 1 and ops[0]["ok"] is True


# --- falhas e alternativas ---------------------------------------------------------------------------------------
def s2_com(**mudancas) -> Scenario:
    sc = s2()
    for k, v in mudancas.items():
        setattr(sc, k, v)
    return sc


def test_T_SWAP_10_parceiro_que_perde_com_a_troca_recusa_e_nada_muda():
    # v1 e v2 passam a evitar TER10/QUI10: C-B é pior para eles, então ninguém aceita trocar C-A por C-B
    studs = [StudentProfile("u1", required=("C",), undesired_slots=frozenset({"SEG08"}), priority=1),
             StudentProfile("u2", required=("C",), undesired_slots=frozenset({"TER10", "QUI10"}), priority=2),
             StudentProfile("v1", required=("C",), undesired_slots=frozenset({"QUI10"}), priority=5),
             StudentProfile("v2", required=("C",), undesired_slots=frozenset({"QUI10"}), priority=6)]
    sim = Simulation(s2_com(students=studs), 1).run()
    sem = Simulation(s2_com(students=studs), 1, config={"swaps": False}).run()
    assert matriculas(sim) == matriculas(sem)
    assert "Falha" in estados(sim)
    assert any("recusou a troca" in n["text"] for n in sim.trace.of_kind("note"))


def test_T_SWAP_11_parceiro_mudo_gera_timeout_e_tenta_o_proximo():
    parceiro_mudo = Rule(action="drop", sender="aluno:v1", performative="agree")
    sim = Simulation(s2(), 1, rules=[parceiro_mudo]).run()
    assert estados(sim).count("AguardandoParceiro") >= 1
    assert estados(sim)[-1] in ("Concluida", "Falha") and sim.registrar.invariants() == []


def test_T_SWAP_12_resposta_do_registrar_perdida_reenvio_idempotente():
    perde = Rule(action="drop", sender="registrar", receiver="dept:D", conv_prefix="swap:", max_hits=1)
    sim = Simulation(s2(), 1, rules=[perde]).run()
    assert estados(sim) == ["Procurando", "AguardandoParceiro", "ConfirmandoRegistrar", "ConfirmandoRegistrar", "Concluida"]
    efetivos = [r for r in sim.trace.of_kind("registrar") if r["op"] == "swap_enroll"]
    assert len(efetivos) == 2 and all(r["ok"] for r in efetivos)     # o 2º devolve o resultado guardado
    r = student_results(sim.registrar, s2())
    assert r["u2"]["S"] == 1.0                                       # a troca valeu uma única vez
    assert sim.registrar.invariants() == []


def test_T_SWAP_13_sem_resposta_do_registrar_falha_sem_inconsistencia_de_pontos():
    perde = Rule(action="drop", sender="registrar", receiver="dept:D", conv_prefix="swap:")
    sim = Simulation(s2(), 1, rules=[perde]).run()
    assert estados(sim)[-1] == "Falha"
    assert sim.registrar.invariants() == []


def test_T_SWAP_14_pedido_de_quem_nao_esta_na_turma_e_negado():
    sim = Simulation(s2(), 1).run(until=60)
    antes = matriculas(sim)
    # u1 está em C-B e não em C-A: tenta ceder C-A
    sim.students["u1"].send("dept:D", REQUEST, "seat_swap", "swap:u1:C-A:C-B:9", {"give": "C-A", "want": "C-B"})
    for _ in range(3):
        sim.step()
    assert matriculas(sim) == antes
    assert any("não está na turma cedida" in r["why"] for r in sim.trace.of_kind("msg_denied"))


def test_T_SWAP_15_troca_pedida_por_um_aluno_nao_pode_usar_a_conversa_de_outro():
    sim = Simulation(s2(), 1).run(until=60)
    antes = matriculas(sim)
    sim.students["u1"].send("dept:D", REQUEST, "seat_swap", "swap:u2:C-A:C-B:9", {"give": "C-A", "want": "C-B"})
    for _ in range(3):
        sim.step()
    assert matriculas(sim) == antes


def test_T_SWAP_16_registrar_nega_troca_pedida_por_aluno_ou_departamento_indevido():
    sim = Simulation(s2(), 1).run(until=60)
    antes = matriculas(sim)
    pedido = {"op": "swap_enroll", "student_a": "u1", "student_b": "v1", "section_a": "C-B", "section_b": "C-A"}
    sim.bus.send(sim.tick, "aluno:u1", "registrar", REQUEST, "registrar", "swap:u1:C-B:C-A:1", pedido)
    sim.bus.send(sim.tick, "dept:D", "registrar", REQUEST, "registrar", "swap:u1:C-B:C-X:1", pedido)   # conv incoerente
    for _ in range(3):
        sim.step()
    assert matriculas(sim) == antes
    assert len(sim.trace.of_kind("registrar_denied")) >= 2


def test_T_SWAP_17_turma_cancelada_no_meio_da_troca_encerra_com_falha():
    """O professor da turma desejada some antes da troca terminar: a turma cai e a troca falha sem efeito."""
    sc = s2()
    from matriculaufsc.model import Event
    sc.events = [Event(45, "professor_unavailable", "P1", {"slots": ["SEG08", "QUA08", "TER10", "QUI10"]})]
    sim = Simulation(sc, 1).run()
    assert estados(sim)[-1] == "Falha"
    assert any(r["to"] == "Falha" and "turma cancelada" in r["why"] for r in sim.trace.of_kind("fsm"))
    assert sim.registrar.invariants() == []
    for sid, aluno in sim.students.items():
        reais = {s for s, sec in sim.registrar.sections.items() if sid in sec.roster}
        assert set(aluno.enrolled()) == reais, sid


# --- propriedade global --------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", range(1, 16))
def test_T_SWAP_18_s1_trocas_preservam_invariantes_e_nao_pioram_o_total(seed):
    sc = build("S1", seed, 16)
    com = Simulation(sc, seed).run()
    sem = Simulation(build("S1", seed, 16), seed, config={"swaps": False}).run()
    assert com.registrar.invariants() == []
    u_com = sum(r["U"] for r in student_results(com.registrar, sc).values())
    u_sem = sum(r["U"] for r in student_results(sem.registrar, sc).values())
    assert u_com >= u_sem - 1e-9
    for sid, aluno in com.students.items():                     # crenças coerentes com o estado institucional
        reais = {s for s, sec in com.registrar.sections.items() if sid in sec.roster}
        assert set(aluno.enrolled()) == reais, (seed, sid)


def test_T_SWAP_19_trocas_ocorrem_em_alguma_semente_do_s1():
    totais = 0
    for seed in (7, 8, 11):
        sim = Simulation(build("S1", seed, 16), seed).run()
        totais += sum(1 for r in sim.trace.of_kind("registrar") if r["op"] == "swap_enroll" and r["ok"])
    assert totais >= 3


def test_T_SWAP_20_determinismo_com_trocas():
    a, b = Simulation(s2(), 3).run(), Simulation(s2(), 3).run()
    assert a.trace.digest() == b.trace.digest()
