# Protocolos de interação — MatriculaUFSC (DSM3)

Este documento reúne **todos** os protocolos do sistema: quem fala com quem, com qual performativa FIPA-ACL, com qual conteúdo e para quê.
A fonte de verdade executável é [`matriculaufsc/contracts.py`](../matriculaufsc/contracts.py) (tabela `SPEC`): uma mensagem que não bate com a tabela é
rejeitada na fronteira do ambiente (`msg_rejected`) e de novo na caixa de entrada do receptor (`msg_invalid`).
As máquinas de estados estão em [`matriculaufsc/fsm.py`](../matriculaufsc/fsm.py) e são conferidas a cada transição.

Convenções: `aluno:<id>`, `prof:<id>`, `dept:<sigla>`, `room:<id>`, `registrar`, `env`. O campo `conv` identifica a conversa e tem formato fixo por protocolo.
Toda mensagem leva 1 tick para chegar; o Registrar responde ao remetente do pedido (`inform` se ok, `failure` se recusou).

## Visão geral

| Protocolo | Participantes | Finalidade | Coordenação |
|---|---|---|---|
| `demand` | aluno → departamento | sinalizar interesse numa disciplina antes da oferta | informação |
| `section_opening` | departamento ↔ professor | escolher o professor de cada turma | **Contract Net** |
| `room_reservation` | departamento ↔ sala | reservar a sala (reserva provisória com TTL) | **reserva em duas fases** |
| `registrar` | departamento → Registrar | efetivar abertura, matrícula, cancelamento e troca | **commit atômico** |
| `board` | departamento → alunos | publicar a oferta (turmas abertas e vagas restantes) | difusão |
| `seat_auction` | departamento ↔ alunos | distribuir as vagas de uma turma | **leilão selado** |
| `seat_swap` *(novo)* | aluno → departamento ↔ aluno | trocar de turma da mesma disciplina | **negociação mediada + commit atômico** |
| `sync` *(novo)* | aluno → departamento | recuperar crenças desatualizadas | reparo de estado |
| `commitment` | professor → departamento | retirar-se de uma turma confirmada | falha anunciada |
| `enrollment` | departamento → aluno | avisar cancelamento de matrícula e reembolso | informação |
| `event` | ambiente → professor/sala | eventos exógenos (indisponibilidade, sala fora do ar) | percepção |

## 1. `seat_swap` — troca de vagas entre alunos (novo na DSM3)

**Finalidade.** Depois do leilão, um aluno pode ficar numa turma com horário indesejado enquanto a turma que ele queria está cheia. Se alguém dessa turma
topar a troca, os dois ganham ou empatam. O departamento é o **corretor**: só ele sabe quem está em cada turma (os alunos não enxergam os outros), então a privacidade se mantém.
A troca só vale quando o Registrar a executa de forma atômica.

**Participantes.** Aluno A (quem pede), departamento dono da disciplina, aluno B (quem está na turma desejada), Registrar.

```
 A (aluno)            Departamento                 B (aluno)                 Registrar
   | request(give=SA, want=SB) |                       |                         |
   |-------------------------->|  cfp(receive=SA, release=SB)                    |
   |                           |---------------------->|                         |
   |                           |  agree | refuse       |                         |
   |                           |<----------------------|                         |
   |                           |  request swap_enroll(A,SA,B,SB)   (se agree)    |
   |                           |------------------------------------------------>|
   |                           |                 inform(ok) | failure(motivos)   |
   |                           |<------------------------------------------------|
   |  inform(done|failed)      |  inform(done)         |                         |
   |<--------------------------|---------------------->|                         |
```

**Mensagens** (`conv` = `swap:<A>:<SA>:<SB>:<n>`, a mesma em toda a conversa):

| Performativa | De → Para | Conteúdo | Quando |
|---|---|---|---|
| `request` | A → dept | `give` (turma que A cede), `want` (turma que A quer) | A está em turma com horário indesejado e há turma cheia estritamente melhor, sem conflito |
| `cfp` | dept → B | `receive` (turma de A), `release` (turma de B) | o departamento consulta, um por vez, os alunos que estão em `want` (ordem determinística) |
| `agree` | B → dept | `receive`, `release` | B decide que a troca não piora seus horários e não gera conflito |
| `refuse` | B → dept | `reason` | caso contrário |
| `request` `op=swap_enroll` | dept → Registrar | `student_a`, `student_b`, `section_a`, `section_b` | B aceitou |
| `inform` / `failure` | Registrar → dept | `ok`, `reasons` | resultado do commit |
| `inform` | dept → A e B | `outcome` (`done`/`failed`), `old`, `new`, `reason?` | fim da conversa |

**Máquina de estados do departamento** (`SEAT_SWAP` em `fsm.py`, uma instância por conversa):

```
Idle → Procurando → AguardandoParceiro → ConfirmandoRegistrar → Concluida
                ↑          │ refuse/timeout/violação: próximo parceiro
                └──────────┘                                  └→ Falha (sem parceiro, turma cancelada, Registrar mudo)
```

**Conflito, falha e alternativa.**

| Situação | Tratamento |
|---|---|
| B recusa (a troca o prejudicaria ou conflita com a grade dele) | o departamento tenta o próximo aluno da turma desejada; sem mais candidatos → `Falha` e A recebe `failed` |
| B não responde | timeout (`swap_timeout`=3 ticks) → próximo candidato |
| Registrar recusa (ex.: `TIME_CONFLICT_B` surgido depois da consulta) | próximo candidato |
| resposta do Registrar perdida | reenvio **idempotente** do mesmo pedido (o Registrar guarda o resultado por `conv`); se continuar mudo → `Falha` |
| a turma é cancelada durante a troca (professor some) | `Falha` com motivo "turma cancelada durante a troca" |
| pedido de quem não está na turma que cede, ou conversa de outro aluno | negado (`msg_denied`), sem efeito |
| A recebe `failed` | marca a turma desejada como recusada e tenta a próxima melhor alternativa, se houver |

**Garantias** (verificadas em `tests/test_seat_swap.py`): a troca é atômica (ou os dois mudam de turma, ou ninguém); vagas e pontos não mudam
(cada aluno leva o preço que pagou, então I1 e I6 continuam valendo); as crenças dos alunos acompanham o resultado; a mesma semente gera o mesmo trace.

## 2. `sync` — recuperação de crenças desatualizadas (novo na DSM3)

**Finalidade.** Um aluno só conhece as turmas pelo quadro (`board`). Se o quadro se perde, ele não sabe que uma turma existe e ficaria de fora do leilão.
Ao receber um convite de leilão (`cfp`) de uma turma que **não consta** nas suas crenças, ele conclui que está desatualizado.

| Passo | Mensagem | Conteúdo |
|---|---|---|
| 1 | aluno guarda o convite e adota o desejo `resync:<dept>` | — |
| 2 | `request` aluno → dept (`conv` = `sync:<aluno>:<n>`) | vazio |
| 3 | `inform` dept → aluno, protocolo `board` | quadro atual (turmas abertas e vagas restantes) |
| 4 | se o quadro chega **antes do fechamento** do leilão (`bid_window`), o aluno ainda responde ao convite guardado | lance (`propose`) |

Limites: no máximo um pedido por departamento a cada 6 ticks; o desejo só nasce se `Config.sync` estiver ligado (chave de ablação).
Com a janela padrão (`bid_window`=2) o quadro recuperado chega tarde para o leilão em andamento: o aluno volta a participar na rodada seguinte
(`test_sync.py`, T-SYNC-04); com janela maior ele ainda dá o lance (T-SYNC-03).

## 3. `seat_auction` — leilão selado de vagas

`Idle → AguardandoLances → Avaliando → Validando(Registrar) → Concluido | SemLanceValido | Cancelado`

| Performativa | De → Para | Conteúdo |
|---|---|---|
| `cfp` | dept → todos os alunos | `section`, `round`, `remaining`, `reserve` |
| `propose` | aluno → dept | `section`, `bid`, `round` |
| `refuse` | aluno → dept | `reason` (sem pontos, preferiu outra turma) |
| `request` `op=commit_enroll` | dept → Registrar | `student`, `section`, `price` |
| `accept-proposal` | dept → vencedor | `section`, `price`, `balance`, `round` |
| `reject-proposal` | dept → perdedor | `section`, `reason`, `round?` |

`conv` = `auc:<turma>:<rodada>`. Ranking por `(−lance, −prioridade, sorteio com semente)`; os `k` primeiros (k = vagas) vão ao Registrar; se ele recusa
(`TIME_CONFLICT`, `DUP_COURSE`, `BUDGET`…), o próximo da fila é promovido (cascata, até `max_cascade`). Lance tardio ou de rodada diferente é descartado.

## 4. `section_opening` — Contract Net para abrir turma

`Idle → AguardandoPropostas → Avaliando → ReservandoSala → ConfirmandoRegistrar → Aberta | Falha` (mais `Revertendo`)

| Performativa | De → Para | Conteúdo |
|---|---|---|
| `cfp` | dept → professores habilitados | `section`, `course`, `slots` |
| `propose` / `refuse` | professor → dept | `score` / `reason` |
| `accept-proposal` / `reject-proposal` | dept → professor | `section` (e `reason`) |
| `cancel` | dept → professor | libera a reserva provisória |
| `inform` | dept → professor | turma aberta (vira compromisso) |

## 5. `room_reservation` — reserva de sala

| Performativa | De → Para | Conteúdo |
|---|---|---|
| `request` | dept → sala | `section`, `slots`, `capacity` |
| `agree` / `refuse` | sala → dept | `section`, `room`, `capacity` / `reason` |
| `inform` | dept → sala | confirma a reserva |
| `cancel` / `reject-proposal` | dept → sala | libera |

Sala fora do ar não responde (silêncio): o departamento sofre timeout. A reserva provisória expira sozinha em `hold_ttl` ticks.

## 6. `registrar` — pedidos ao ponto de commit

Só departamentos fazem pedidos, sempre com `op` e campos tipados (`OPS` em `contracts.py`):

| `op` | Campos | Efeito |
|---|---|---|
| `open_section` | `section`, `prof`, `room`, `capacity` | abre a turma (atômico) |
| `commit_enroll` | `student`, `section`, `price` | matrícula, debita pontos |
| `cancel_section` | `section`, `reason?`, `block?` | cancela, reembolsa, libera professor e sala (idempotente) |
| `swap_enroll` | `student_a`, `student_b`, `section_a`, `section_b` | troca atômica e idempotente por `conv` |

O Registrar **autentica a posse** de cada pedido antes de tocar no estado (ver [`seguranca.md`](seguranca.md)).

## 7. Mensagens que dependem do estado do protocolo

Uma mensagem válida no formato pode ser inválida **para o estado atual**. Exemplos tratados: lance fora da janela ou de outra rodada (`msg_denied`);
resposta de professor ou sala que não foi consultado; `agree` de quem não é o parceiro da troca em andamento; resposta duplicada do Registrar a uma conversa já concluída (ignorada).
