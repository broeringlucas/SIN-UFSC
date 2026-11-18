# Cenário S2 — troca de vagas entre alunos (seat_swap)

Cenário controlado, pequeno o bastante para conferir à mão. Gera exatamente a situação em que a troca compensa.

**Dados.** Uma disciplina `C` (departamento D), duas turmas de 2 vagas: `C-A` (SEG08, QUA08) e `C-B` (TER10, QUI10); dois professores e duas salas.

| Aluno | Evita | Prioridade | O que esperar |
|---|---|---|---|
| u1 | SEG08 | 1 | quer `C-B` (única turma boa) |
| u2 | TER10, QUI10 | 2 | quer `C-A`, mas perde a disputa |
| v1 | — | 5 | indiferente; leva `C-A` por prioridade |
| v2 | — | 6 | indiferente; leva `C-A` por prioridade |

**Roteiro** (`python -m matriculaufsc --scenario S2 --seed 1 --trace out/s2.jsonl`; saída em `docs/evidencias/cenario_S2_trocas_resultado.txt`).

1. Rodada 0 do leilão: v1 e v2 (prioridade maior) levam as 2 vagas de `C-A`; u1 leva uma vaga de `C-B`; u2 perde `C-A`.
2. Rodada seguinte: u2 só encontra vaga em `C-B`, que tem horário indesejado; aceita (plano `bid_tolerate`) e **vence `C-B` no tick 44, pagando 70**, com **S = 0** (U = 0,75). Ela perdeu `C-A` no tick 30 (`outbid`).
3. Tick 44: u2 forma o desejo `improve:C` e adota o plano `propose_swap`: `request(give=C-B, want=C-A)` ao departamento (tick 45 no departamento).
4. O departamento consulta o primeiro aluno de `C-A` (v1) com `cfp` (tick 45); v1 **aceita** no tick 47 (a troca não piora os horários dele: continua sem horário indesejado).
5. O departamento pede `swap_enroll` ao Registrar, que troca as matrículas de forma atômica no tick 48, sem mexer em vagas nem pontos; o departamento conclui no tick 49 e u2 atualiza a crença no tick 50.
6. Resultado: u2 em `C-A` (S = 1, U = 1,00); v1 em `C-B` (U = 1,00, igual ao anterior). Sem trocas (`--no-swap`): u2 fica com U = 0,75.

Estados do protocolo no trace: `Procurando → AguardandoParceiro → ConfirmandoRegistrar → Concluida`.
Linha do tempo de u2: `python -m matriculaufsc.explain docs/evidencias/trace_S2_seed1.jsonl aluno:u2 --tick 40:50`.
