"""Bateria dos quatro ataques do feedback da DSM2, contra o pacote `matriculaufsc` que estiver no PYTHONPATH.

Uso:  PYTHONPATH=<projeto> python scripts/ataques.py
Em cada ataque a mensagem é injetada no barramento (acesso direto, o caso mais forte) e o estado é conferido.
"""
import math

from matriculaufsc.messages import INFORM, REQUEST
from matriculaufsc.scenarios import s0
from matriculaufsc.sim import Simulation


def preparado():
    sim = Simulation(s0(), 7)
    sim.run(until=25)           # turmas abertas, antes do primeiro leilão
    return sim


def secao(sim, sid):
    s = sim.registrar.sections[sid]
    return f"{s.status}, matriculados={sorted(s.roster)}"


def rodar(nome, ataque, medir):
    sim = preparado()
    antes = medir(sim)
    erro = ""
    ataque(sim)
    try:
        for _ in range(4):
            sim.step()
    except Exception as exc:  # noqa: BLE001 - o objetivo é justamente registrar a falha
        erro = f"EXCEÇÃO {type(exc).__name__}: {exc}"
    depois = medir(sim)
    inv = sim.registrar.invariants()
    efeito = "ESTADO ALTERADO" if depois != antes else "estado intacto"
    print(f"{nome}\n    antes : {antes}\n    depois: {depois}\n    => {erro or efeito}; invariantes violadas: {inv or 'nenhuma'}\n")


def main():
    rodar("1. cancelamento de turma em nome de aluno inexistente",
          lambda s: s.bus.send(s.tick, "aluno:fantasma", "registrar", REQUEST, "registrar", "cancel:MTM1-A",
                               {"op": "cancel_section", "section": "MTM1-A", "reason": "ataque"}),
          lambda s: secao(s, "MTM1-A"))

    def retirada(s):
        prof = s.registrar.sections["INE1-A"].prof
        s.bus.send(s.tick, "prof:fantasma", "dept:INE", INFORM, "commitment", "withdraw:INE1-A",
                   {"section": "INE1-A", "prof": prof, "slots": ["SEG10", "QUA10"]})
    rodar("2. falsa retirada de professor enviada por participante inexistente", retirada,
          lambda s: f"{secao(s, 'INE1-A')}; disponibilidade de {s.registrar.sections['INE1-A'].prof or 'prof_ine1'} "
                    f"= {len(s.registrar.prof_avail['prof_ine1'])} horários")
    rodar("3. matrícula com custo NaN",
          lambda s: s.bus.send(s.tick, "dept:MTM", "registrar", REQUEST, "registrar", "auc:MTM1-A:0",
                               {"op": "commit_enroll", "student": "ana", "section": "MTM1-A", "price": math.nan}),
          lambda s: f"saldo de ana = {s.registrar.points['ana']}; {secao(s, 'MTM1-A')}")
    rodar("4. requisição ao Registrar sem o campo op",
          lambda s: s.bus.send(s.tick, "dept:MTM", "registrar", REQUEST, "registrar", "open:MTM1-A", {"section": "MTM1-A"}),
          lambda s: secao(s, "MTM1-A"))


if __name__ == "__main__":
    main()
