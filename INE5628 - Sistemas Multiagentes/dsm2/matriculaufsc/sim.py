"""Runtime: simulação discreta síncrona por ticks (ver docs/arquitetura e README, seção "Arquitetura").

Em cada tick: (1) o ambiente injeta os eventos, entrega as mensagens do tick anterior e deixa o Registrar processar
(ver environment.py); (2) cada agente recebe suas percepções e executa um passo (perceber → deliberar → agir).
Latência fixa de 1 tick; ordem de processamento por `mid`; único gerador aleatório é
`random.Random(f"{seed}:...")` no desempate do leilão ⇒ determinismo.
"""

from __future__ import annotations

from .agents.classroom import Classroom
from .agents.department import Department
from .agents.professor import Professor
from .agents.student import Student
from .environment import Environment
from .model import Config, Scenario
from .trace import TraceLogger


class Simulation:
    def __init__(self, scenario: Scenario, seed: int = 0, rules=(), pricing: str | None = None,
                 config: dict | None = None) -> None:
        self.scenario, self.seed = scenario, seed
        cfg = {**scenario.config, **(config or {})}
        if pricing:
            cfg["pricing"] = pricing
        self.cfg = Config(**cfg)
        self.trace = TraceLogger()
        self.env = Environment(scenario, self.trace, rules)
        self.bus, self.registrar = self.env.bus, self.env.registrar
        self.departments = {d: Department(d, scenario, self.env, self.trace, self.cfg, seed) for d in scenario.depts}
        self.professors = {p.pid: Professor(p, self.env, self.trace, self.cfg) for p in scenario.professors}
        self.rooms = {r.rid: Classroom(r, self.env, self.trace, self.cfg) for r in scenario.rooms}
        self.students = {s.sid: Student(s, scenario, self.env, self.trace) for s in scenario.students}
        self.agents = (list(self.departments.values()) + list(self.professors.values())
                       + list(self.rooms.values()) + list(self.students.values()))
        self.tick = 0

    def step(self) -> None:
        t = self.tick
        self.env.advance(t)
        for a in self.agents:
            a.step(t, self.env.perceive(a.id))
        self.tick += 1

    def run(self, until: int | None = None) -> "Simulation":
        end = self.cfg.end_tick() if until is None else until
        while self.tick <= end:
            self.step()
        self.trace.log(self.tick - 1, "end", "sim", invariants=self.registrar.invariants())
        return self
