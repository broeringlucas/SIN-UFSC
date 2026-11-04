"""Mini-framework BDI com ciclo explícito e *tudo registrado no trace*.

Ciclo por tick (resposta à anotação 1 do professor — operacionalização do BDI):

  1. perceive      mensagens → crenças (cada mudança gera `belief_change` com valor antigo/novo e causa)
  2. update_desires crenças → desejos (ativos / realizados / bloqueados / descartados; `desire_change`)
  3. reconsider    política de compromisso *single-minded*: uma intenção só é reavaliada se alguma
                   crença que ela observa (`watch`) mudou; se o plano deixou de ser válido, a
                   intenção é abandonada (`reconsider` + `intention_change`); se continua válida,
                   o compromisso é mantido (`reconsider` com decisão "mantida")
  4. deliberate    para cada desejo ativo sem intenção: gera opções (planos aplicáveis da biblioteca),
                   filtra pelo maior score e adota a intenção (`plan_selected`, `intention_change`);
                   sem plano aplicável → desejo bloqueado
  5. act           cada intenção ativa executa seu passo (envia mensagens)

Estados de desejo: active, achieved, blocked, dropped. Estados de intenção: active, done, dropped.
Empate de scores entre planos: vence o primeiro da biblioteca.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .base import Agent


class Beliefs:
    def __init__(self, owner: Agent) -> None:
        self.owner = owner
        self._d: dict[str, object] = {}
        self.changed: set[str] = set()

    def get(self, key: str, default=None):
        return self._d.get(key, default)

    def set(self, key: str, value, cause: str = "") -> bool:
        old = self._d.get(key)
        if old == value:
            return False
        if value is None:
            self._d.pop(key, None)
        else:
            self._d[key] = value
        self.changed.add(key)
        self.owner.log("belief_change", key=key, old=old, new=value, cause=cause)
        return True

    def keys_with(self, prefix: str) -> list[str]:
        return sorted(k for k in self._d if k.startswith(prefix))


@dataclass
class Desire:
    name: str
    kind: str
    priority: float
    params: dict = field(default_factory=dict)
    status: str = "active"


@dataclass
class Intention:
    iid: str
    desire: Desire
    plan: "Plan"
    state: dict
    watch: tuple[str, ...]
    status: str = "active"
    created: int = 0


class Plan:
    name = "plan"
    kinds: tuple[str, ...] = ()

    def applicable(self, agent, desire: Desire) -> bool:
        return False

    def score(self, agent, desire: Desire) -> float:
        return 1.0

    def start(self, agent, desire: Desire) -> tuple[dict, tuple[str, ...]]:
        return {}, ()

    def execute(self, agent, it: Intention) -> None:
        pass

    def valid(self, agent, it: Intention) -> bool:
        return True

    def achieved(self, agent, it: Intention) -> bool:
        return False


class BDIAgent(Agent):
    def __init__(self, aid, env, trace, plans: list[Plan]) -> None:
        super().__init__(aid, env, trace)
        self.beliefs = Beliefs(self)
        self.desires: dict[str, Desire] = {}
        self.intentions: list[Intention] = []
        self.plans = plans
        self._iid = 0

    def perceive(self, inbox) -> None:
        raise NotImplementedError

    def update_desires(self) -> None:
        raise NotImplementedError

    def step(self, tick: int, inbox) -> None:
        self.tick = tick
        self.beliefs.changed.clear()
        self.perceive(inbox)
        self.update_desires()
        self.reconsider()
        self.deliberate()
        self.act()

    def active_intentions(self) -> list[Intention]:
        return sorted((i for i in self.intentions if i.status == "active"),
                      key=lambda i: (-i.desire.priority, i.desire.name))

    def set_desire_status(self, d: Desire, status: str, reason: str) -> None:
        if d.status != status:
            self.log("desire_change", desire=d.name, old=d.status, new=status, reason=reason)
            d.status = status

    def add_desire(self, d: Desire) -> None:
        if d.name not in self.desires:
            self.desires[d.name] = d
            self.log("desire_change", desire=d.name, old=None, new=d.status, reason="adotado",
                     priority=round(d.priority, 4))

    def reconsider(self) -> None:
        for it in self.active_intentions():
            if it.plan.achieved(self, it):
                it.status = "done"
                self.log("intention_change", intention=it.iid, desire=it.desire.name,
                         plan=it.plan.name, action="cumprida")
                continue
            relevant = sorted(k for k in self.beliefs.changed if k.startswith(it.watch)) if it.watch else []
            if not relevant:
                continue
            if it.plan.valid(self, it):
                self.log("reconsider", intention=it.iid, plan=it.plan.name, changed=relevant,
                         decision="mantida", why="compromisso single-minded: plano ainda válido")
            else:
                it.status = "dropped"
                self.log("reconsider", intention=it.iid, plan=it.plan.name, changed=relevant,
                         decision="abandonada", why="plano inválido após mudança de crença")
                self.log("intention_change", intention=it.iid, desire=it.desire.name,
                         plan=it.plan.name, action="abandonada")

    def deliberate(self) -> None:
        for d in sorted(self.desires.values(), key=lambda d: (-d.priority, d.name)):
            if d.status not in ("active", "blocked"):
                continue
            if any(i.desire is d and i.status == "active" for i in self.intentions):
                continue
            options = [(p.score(self, d), p) for p in self.plans
                       if d.kind in p.kinds and p.applicable(self, d)]
            if not options:
                self.set_desire_status(d, "blocked", "nenhum plano aplicável com as crenças atuais")
                continue
            self.set_desire_status(d, "active", "plano aplicável")
            score, plan = max(options, key=lambda o: o[0])
            state, watch = plan.start(self, d)
            self._iid += 1
            it = Intention(f"{self.id}#{self._iid}", d, plan, state, watch, created=self.tick)
            self.intentions.append(it)
            self.log("plan_selected", desire=d.name, chosen=plan.name, score=score,
                     options=[[p.name, s] for s, p in options])
            self.log("intention_change", intention=it.iid, desire=d.name, plan=plan.name,
                     action="adotada", targets=state.get("targets"))

    def act(self) -> None:
        for it in self.active_intentions():
            it.plan.execute(self, it)
