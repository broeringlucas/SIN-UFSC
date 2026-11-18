from conftest import mk, run

from matriculaufsc.bus import Rule
from matriculaufsc.environment import Environment
from matriculaufsc.messages import INFORM, aid_prof
from matriculaufsc.model import Event
from matriculaufsc.registrar import Registrar
from matriculaufsc.scenarios import s0
from matriculaufsc.trace import TraceLogger


def novo_ambiente(**kw):
    return Environment(mk(**kw), TraceLogger())


def enviar(env, cred, tick, sender, receiver, conv, content, perf=INFORM, protocol="demand"):
    return env.execute(tick, sender, receiver, perf, protocol, conv, content, cred[sender])


def com_agentes(env, *aids):
    return {a: env.register(a) for a in aids}


def test_percepcao_so_inclui_mensagens_enderecadas_ao_agente_e_chega_no_tick_seguinte():
    env = novo_ambiente()
    a, b, c = "aluno:a", "dept:b", "dept:c"
    cred = com_agentes(env, a)
    enviar(env, cred, 0, a, b, "demand:c1", {"course": "X", "student": "a"})
    enviar(env, cred, 0, a, c, "demand:c2", {"course": "X", "student": "a"})
    env.advance(0)
    assert env.perceive(b) == [] and env.perceive(c) == []
    env.advance(1)
    assert [m.conv for m in env.perceive(b)] == ["demand:c1"]
    assert [m.conv for m in env.perceive(c)] == ["demand:c2"]
    assert env.perceive(a) == []


def test_percepcao_nao_se_repete_no_tick_seguinte():
    env = novo_ambiente()
    a, b = "aluno:a", "dept:b"
    cred = com_agentes(env, a)
    enviar(env, cred, 0, a, b, "demand:c1", {"course": "X", "student": "a"})
    env.advance(1)
    assert len(env.perceive(b)) == 1
    env.advance(2)
    assert env.perceive(b) == []


def test_acao_sofre_as_regras_de_falha_do_ambiente():
    env = Environment(mk(), TraceLogger(), rules=[Rule(action="drop", performative=INFORM)])
    a, b = "aluno:a", "dept:b"
    cred = com_agentes(env, a)
    enviar(env, cred, 0, a, b, "demand:c1", {"course": "X", "student": "a"})
    env.advance(1)
    assert env.perceive(b) == []
    assert env.trace.of_kind("msg_dropped")


def test_evento_do_cenario_vira_mensagem_do_env_no_tick_certo():
    env = novo_ambiente(events=[Event(5, "professor_unavailable", "P1", {"slots": ["SEG08"]})])
    for t in range(0, 6):
        env.advance(t)
        assert env.perceive(aid_prof("P1")) == []
    env.advance(6)
    (m,) = env.perceive(aid_prof("P1"))
    assert m.sender == "env" and m.protocol == "event" and m.content["kind"] == "unavailable"
    assert [r["event"] for r in env.trace.of_kind("event")] == ["professor_unavailable"]


def test_snapshot_reflete_o_estado_institucional_e_as_invariantes():
    sim = run(s0(), seed=7)
    snap = sim.env.snapshot()
    assert snap["invariants"] == []
    assert {sid for sid, s in snap["sections"].items() if s["status"] == "OPEN"} >= {"INE1-A", "MTM1-A"}
    assert snap["sections"]["INE1-A"]["prof"] == "prof_ine2"
    assert all(v >= 0 for v in snap["points"].values())


def test_nenhum_agente_guarda_referencia_ao_registrar_nem_a_outro_agente():
    sim = run(mk(), seed=1)
    for agent in sim.agents:
        for name, value in vars(agent).items():
            assert not isinstance(value, Registrar), (agent.id, name)
            assert value is not sim.registrar, (agent.id, name)
            assert not (hasattr(value, "step") and hasattr(value, "id") and value is not agent), (agent.id, name)


def test_simulacao_usa_o_mesmo_barramento_e_registrar_do_ambiente():
    sim = run(mk(), seed=1)
    assert sim.bus is sim.env.bus and sim.registrar is sim.env.registrar


def test_agentes_so_usam_o_ambiente_para_agir_nunca_para_ler_o_estado():
    import re
    from pathlib import Path

    import matriculaufsc.agents as pkg

    usos = set()
    for p in Path(pkg.__file__).parent.glob("*.py"):
        usos |= set(re.findall(r"\benv\.(\w+)", p.read_text(encoding="utf-8")))
    assert usos == {"execute", "register"}  # agir (execute) e obter a credencial própria (register); nunca ler estado
