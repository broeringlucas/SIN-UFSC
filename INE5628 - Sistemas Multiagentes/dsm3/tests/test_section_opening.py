"""Abertura de turma (Contract Net + reserva em duas fases) e consistência sob falhas."""
from conftest import fsm_states, mk, notes, run

from matriculaufsc.bus import Rule
from matriculaufsc.model import Event, ProfessorProfile, RoomDef, SectionDef, StudentProfile
from matriculaufsc.scenarios import ALL_SLOTS, s0
from matriculaufsc.sim import Simulation


def two_profs(**kw):
    return [ProfessorProfile("P1", "D", frozenset({"X"}), ALL_SLOTS, frozenset({"SEG08", "QUA08"})),
            ProfessorProfile("P2", "D", frozenset({"X"}), ALL_SLOTS)]


def consistent(sim):
    """Invariantes do Registrar + nenhuma reserva órfã nas salas (nem agendamento de turma não aberta)."""
    assert sim.registrar.invariants() == []
    for room in sim.rooms.values():
        assert not room.holds, f"reserva provisória órfã em {room.room.rid}: {room.holds}"
        for sid in room.booked:
            sec = sim.registrar.sections[sid]
            assert sec.status == "OPEN" and sec.room == room.room.rid


def test_T_OPEN_01_caminho_feliz_abre_turma_com_professor_de_maior_score_e_sala_justa():
    sim = run(mk(profs=two_profs(), rooms=[RoomDef("R1", "D", 5), RoomDef("R2", "D", 2)]))
    s = sim.registrar.sections["X-A"]
    assert s.status == "OPEN" and s.prof == "P1" and s.room == "R2"
    assert fsm_states(sim, "section_opening", "X-A") == [
        "AguardandoPropostas", "Avaliando", "Avaliando", "ReservandoSala", "ConfirmandoRegistrar", "Aberta"]
    assert sim.professors["P1"].committed() == {"X-A": ["SEG08", "QUA08"]}
    assert sim.rooms["R2"].booked == {"X-A": ["SEG08", "QUA08"]} and not sim.rooms["R2"].holds
    consistent(sim)


def test_T_OPEN_01_demanda_insuficiente_nao_abre_turma():
    sc = mk(sections=[SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2, min_demand=3)],
            students=[StudentProfile("s1", required=("X",))])
    sim = run(sc)
    assert sim.registrar.sections["X-A"].status == "PLANNED"
    assert fsm_states(sim, "section_opening", "X-A") == ["Falha"]


def test_capacidade_efetiva_limitada_pela_sala():
    sim = run(mk(sections=[SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 5)], rooms=[RoomDef("R1", "D", 3)]))
    assert sim.registrar.sections["X-A"].capacity == 3


def test_sala_recusa_e_departamento_tenta_a_proxima():
    sim = run(s0(), seed=7)
    assert any(r["rule"] == "R2" for r in sim.trace.of_kind("reaction"))
    assert sim.registrar.sections["INE3-A"].room == "R-I1" and sim.registrar.sections["INE2-A"].room == "R-I2"
    consistent(sim)


def test_sala_fora_do_ar_gera_timeout_e_proxima_sala():
    sc = mk(rooms=[RoomDef("R1", "D", 2), RoomDef("R2", "D", 3)], events=[Event(0, "room_down", "R1")])
    sim = run(sc)
    assert sim.registrar.sections["X-A"].room == "R2"
    assert any("timeout da sala R1" in n for n in notes(sim))
    assert not sim.rooms["R1"].holds and not sim.rooms["R1"].booked
    consistent(sim)


def test_perda_do_agree_da_sala_nao_deixa_reserva_orfa():
    rules = [Rule(action="drop", performative="agree", protocol="room_reservation", max_hits=1)]
    sim = run(mk(rooms=[RoomDef("R1", "D", 2), RoomDef("R2", "D", 3)]), rules=rules)
    assert sim.registrar.sections["X-A"].room == "R2"
    assert not sim.rooms["R1"].holds
    consistent(sim)


def test_registrar_recusa_abertura_e_reservas_sao_revertidas():
    """O professor acredita estar disponível mas o Registrar sabe que não (crença desatualizada)."""
    sc = mk(profs=two_profs())
    sim = Simulation(sc, 1)
    sim.registrar.prof_avail["P1"].discard("QUA08")
    sim.run()
    s = sim.registrar.sections["X-A"]
    assert s.status == "OPEN" and s.prof == "P2"
    assert any(r["reasons"] == ["PROF_UNAVAILABLE"] for r in sim.trace.of_kind("registrar") if not r["ok"])
    assert sim.professors["P1"].committed() == {} and not sim.professors["P1"].beliefs.keys_with("hold:")
    assert sim.professors["P2"].committed() == {"X-A": ["SEG08", "QUA08"]}
    consistent(sim)


def test_timeout_do_registrar_faz_rollback_idempotente():
    rules = [Rule(action="drop", sender="registrar", performative="inform", conv_prefix="open:", max_hits=1)]
    sim = run(mk(), rules=rules)
    st = fsm_states(sim, "section_opening", "X-A")
    assert "Revertendo" in st and st[-1] == "Falha"
    assert sim.registrar.sections["X-A"].status == "CANCELLED"
    assert not sim.rooms["R1"].holds and not sim.rooms["R1"].booked
    consistent(sim)


def test_timeout_do_registrar_com_segundo_candidato_abre_com_ele():
    rules = [Rule(action="drop", sender="registrar", performative="inform", conv_prefix="open:", max_hits=1)]
    sim = run(mk(profs=two_profs()), rules=rules)
    s = sim.registrar.sections["X-A"]
    assert s.status == "OPEN" and s.prof == "P2"
    consistent(sim)


def test_perda_do_confirm_nao_viola_invariantes_registrar_e_a_fonte_da_verdade():
    rules = [Rule(action="drop", performative="inform", protocol="section_opening", receiver="prof:P1", max_hits=1)]
    sim = run(mk(), rules=rules)
    assert sim.registrar.sections["X-A"].status == "OPEN"
    assert sim.professors["P1"].committed() == {}
    assert sim.registrar.invariants() == []


def test_cancelamento_por_evento_reembolsa_alunos_e_reabre_com_outro_professor():
    sim = run(s0(), seed=7)
    cancel = [r for r in sim.trace.of_kind("registrar") if r["op"] == "cancel_section"][0]
    assert cancel["section"] == "INE1-A" and sorted(s["student"] for s in cancel["students"]) == ["ana", "bruno", "eva"]
    assert all(s["refund"] > 0 for s in cancel["students"])
    s = sim.registrar.sections["INE1-A"]
    assert s.status == "OPEN" and s.prof == "prof_ine2"
    assert sim.registrar.prof_avail["prof_ine1"].isdisjoint({"SEG10", "QUA10"})
    assert sorted(s.roster) == ["ana", "bruno", "eva"]
    consistent(sim)


def test_timeout_envia_cancel_explicito_a_sala_sem_depender_do_ttl():
    """A reserva órfã deve ser liberada pelo `cancel` (regra R5) bem antes de o TTL (R6) expirar."""
    rules = [Rule(action="drop", performative="agree", protocol="room_reservation", max_hits=1)]
    sim = run(mk(rooms=[RoomDef("R1", "D", 2), RoomDef("R2", "D", 3)]), rules=rules)
    r1 = [(r["tick"], r["rule"]) for r in sim.trace.of_kind("reaction") if r["agent"] == "room:R1"]
    assert [rule for _, rule in r1] == ["R1", "R5"]
    assert r1[1][0] - r1[0][0] <= 5


def test_T_BDI_03_professor_recusa_alem_da_carga_maxima():
    secs = [SectionDef("X-A", "X", "D", ("SEG08", "QUA08"), 2), SectionDef("X-B", "X", "D", ("TER10", "QUI10"), 2)]
    prof = ProfessorProfile("P1", "D", frozenset({"X"}), ALL_SLOTS, max_hours=2)
    sim = run(mk(sections=secs, profs=[prof], students=[StudentProfile("s1", required=("X",)), StudentProfile("s2", required=("X",)),
                                                          StudentProfile("s3", required=("X",))]))
    status = {sid: s.status for sid, s in sim.registrar.sections.items()}
    assert sorted(status.values()) == ["OPEN", "PLANNED"]
    refusals = [r["content"]["reason"] for r in sim.trace.of_kind("msg") if r["perf"] == "refuse" and r["protocol"] == "section_opening"]
    assert refusals == ["carga máxima"]
    assert sim.registrar.prof_hours("P1") <= 2
