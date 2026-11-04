# Cenário controlado S0 (depuração)

Cinco alunos, dois departamentos (MTM, INE), três professores, quatro salas e seis turmas planejadas.
Tudo é determinístico: o desempate de lances iguais usa primeiro a prioridade do aluno, de modo que **os
resultados abaixo não dependem da semente** (a semente só decide empates entre alunos de mesma prioridade).

Execução: `python -m matriculaufsc --scenario S0 --seed 7 --trace out/trace.jsonl`
Linha do tempo de um agente: `python -m matriculaufsc.explain out/trace.jsonl aluno:bruno`

## O que cada elemento provoca

| Elemento | Comportamento exercitado | Onde ver no trace |
|---|---|---|
| MTM1: 5 interessados, 2 turmas de 2 vagas | disputa por vagas, lance-hedge, aluno sem vaga (bruno) | `fsm seat_auction MTM1-A:0`, `MTM1-B:0` |
| `davi` ganha MTM1-A e também seria vencedor de MTM1-B | Registrar recusa `DUP_COURSE` e o departamento promove `eva` (cascata) | `registrar ok=False` no tick 34; nota "(cascata)" |
| INE2-A e INE3-A: mesmo horário, ambas preferem a sala R-I2 (cap. 2) | sala recusa (regra R2), departamento tenta R-I1 | `reaction R2` no tick 5 |
| INE4-A: 1 interessado, `min_demand=2` | turma não abre; desejo de `davi` fica bloqueado | `fsm section_opening INE4-A → Falha` |
| `ana` evita SEG08; `carla` evita TER10/QUI10 | planos diferentes por preferência de horário | `plan_selected` das intenções de MTM1 |
| INE2-A e INE3-A no mesmo horário | `carla` reserva INE2 (obrigatória) e a eletiva INE3 fica bloqueada | `desire_change aluno:carla obtain:INE3 → blocked` |
| Evento: `prof_ine1` indisponível em SEG10/QUA10 no tick 44 | professor reconsidera (keep → withdraw), turma INE1-A cancelada, pontos reembolsados, turma reaberta com `prof_ine2`, alunos reativam o desejo e voltam a dar lance na rodada 2 | `reconsider`, `registrar cancel_section`, `fsm ... Aberta` no tick 54 |

## Lances da rodada 0 (conferíveis à mão)

Cada aluno reparte seus 100 pontos entre os desejos ativos proporcionalmente ao peso (obrigatória 0,60/n, eletiva 0,15/n).

| Turma (vagas) | Ranking (aluno, lance) | Vencedores |
|---|---|---|
| MTM1-A (2) | davi 50, carla 50, eva 40, bruno 40 | carla, davi |
| MTM1-B (2) | ana 40, davi 25, eva 20, bruno 20 | ana, **eva** (davi recusado pelo Registrar: DUP_COURSE) |
| INE1-A (3) | eva 40, bruno 40, ana 40 | os três |
| INE2-A (2) | davi 50, carla 50 | os dois |
| INE3-A (2) | eva 20, bruno 20, ana 20 (empate → prioridade) | eva, bruno |

## Resultado final esperado (valores usados em `test_resultado_de_referencia_do_cenario_s0`)

| Aluno | Turmas | R | S | E | U |
|---|---|---|---|---|---|
| ana | INE1-A, MTM1-B | 1,00 | 1,00 | 0,00 | 0,85 |
| bruno | INE1-A, INE3-A | 0,50 | 1,00 | 1,00 | 0,70 |
| carla | INE2-A, MTM1-A | 1,00 | 1,00 | 0,00 | 0,85 |
| davi | INE2-A, MTM1-A | 1,00 | 1,00 | 0,00 | 0,85 |
| eva | INE1-A, INE3-A, MTM1-B | 1,00 | 1,00 | 1,00 | 1,00 |

`bruno` fica sem MTM1 (5 interessados para 4 vagas) e, mesmo assim, U = 0,70 = θ (exatamente no limiar).

## Observação sobre o comportamento dos lances

Na rodada 2, com os pontos reembolsados e um único desejo ativo, `bruno` dá lance de 80 e `ana`/`eva` de 60 por INE1-A: como os
pontos não têm valor depois do período e o preço é o próprio lance (1º preço), o comportamento "apostar tudo no último desejo"
é emergente. Isso é uma limitação conhecida do modelo de lances (ver README, seção Limitações).
