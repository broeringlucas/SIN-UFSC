from matriculaufsc.bus import MessageBus, Rule
from matriculaufsc.messages import INFORM
from matriculaufsc.trace import TraceLogger


def mkbus(*rules):
    return MessageBus(TraceLogger(), rules)


def send(bus, t, to="b", conv="c"):
    return bus.send(t, "a", to, INFORM, "p", conv, {})


def test_latencia_de_um_tick():
    bus = mkbus()
    send(bus, 3)
    assert bus.deliver(3) == {}
    assert [m.conv for m in bus.deliver(4)["b"]] == ["c"]
    assert bus.deliver(5) == {} and bus.pending() == 0


def test_ordem_de_entrega_e_por_mid():
    bus = mkbus()
    m1, m2, m3 = send(bus, 0, conv="1"), send(bus, 0, conv="2"), send(bus, 0, conv="3")
    assert [m.mid for m in bus.deliver(1)["b"]] == [m1.mid, m2.mid, m3.mid]


def test_regra_drop_com_limite_de_ocorrencias():
    bus = mkbus(Rule(action="drop", receiver="b", max_hits=1))
    send(bus, 0, conv="perdida")
    send(bus, 0, conv="ok")
    assert [m.conv for m in bus.deliver(1)["b"]] == ["ok"]
    assert bus.trace.of_kind("msg_dropped")[0]["conv"] == "perdida"


def test_regra_delay_atrasa_a_entrega():
    bus = mkbus(Rule(action="delay", delay=2, conv_prefix="lenta"))
    send(bus, 0, conv="lenta-1")
    assert bus.deliver(1) == {} and bus.deliver(2) == {}
    assert len(bus.deliver(3)["b"]) == 1
