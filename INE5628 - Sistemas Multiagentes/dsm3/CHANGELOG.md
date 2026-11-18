# Mudanças da DSM3 em relação à DSM2

Cada item indica o checkpoint (CP) e como foi verificado.

| Mudança | Motivo (feedback) | CP | Verificação |
|---|---|---|---|
| `contracts.py`: contrato por protocolo/performativa, papéis, formato de `conv`, tipos e intervalos; rejeita `NaN`/`inf` e operação desconhecida | contratos de mensagem com verificação de tipos, campos obrigatórios e intervalos | CP3, CP10 | `test_security.py` |
| `Environment.register/execute`: credencial por agente, autenticação do remetente; `msg_rejected` no trace | remetente inexistente e falsificado | CP5, CP10 | T-SEC-01…18 |
| `Agent.screen`: segunda checagem na caixa de entrada | defesa em profundidade | CP10 | `test_security.py` (fuzz) |
| `Registrar.authorize`: posse por departamento, `conv` coerente com a operação; nunca lança exceção | verificar identidade e papel; vincular requisição à conversação | CP10 | ataques 1, 3, 4 |
| `Department`: retirada só do professor responsável; demais respostas só de quem foi consultado | conferir se a retirada veio do professor da turma | CP10 | ataque 2 |
| `Registrar.validate_enroll`: preço precisa ser inteiro finito | custo `NaN` aceito | CP10 | `test_security.py` |
| Protocolo `seat_swap`, `Registrar.swap_enroll` (atômico, idempotente), FSM `SEAT_SWAP`, planos `propose_swap`/`accept_swap`/`decline_swap`, cenário S2 | concluir o protocolo seat-swap (REQ-F04) | CP3, CP6 | `test_seat_swap.py` |
| Protocolo `sync` + convite guardado + `Config.bid_window` | mecanismo de recuperação de crenças desatualizadas | CP6 | `test_sync.py` |
| `Rule(action="duplicate")` no barramento | testes com duplicidade | CP11 | `test_adversarial.py` |
| `tests/test_security.py`, `test_adversarial.py`, `test_seat_swap.py`, `test_sync.py` (de 111 para 213 testes) | ampliar testes adversariais | CP11 | `docs/evidencias/testes.txt` |
| `scripts/ataques.py`, `scripts/experimento_trocas.py` | evidência antes/depois e efeito da troca | CP12 | `docs/evidencias/` |
| `docs/protocolos.md`, `docs/seguranca.md`, `docs/cenario_S2.md`, diagrama atualizado | documentação | CP13 | — |
| README: imagem `arquitetura.png` incluída em `docs/`; matrícula a preencher | pendências de documentação | CP13 | — |

**Compatibilidade:** o cenário S0 com semente 7 gera o mesmo trace da DSM2 (725 registros, sha256 `63e955f610e43987…`).
