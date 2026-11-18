# Autorização e validação — resposta ao feedback da DSM2

## O problema encontrado pelo professor

Na DSM2 o Registrar e o Departamento confiavam no campo `sender` da mensagem e no formato do conteúdo. O feedback relatou quatro falhas, e todas foram **reproduzidas**
com o código entregue (`scripts/ataques.py`, saída em [`evidencias/ataques_dsm2_vs_dsm3.txt`](evidencias/ataques_dsm2_vs_dsm3.txt)):

| # | Ataque | DSM2 | DSM3 |
|---|---|---|---|
| 1 | `cancel_section` em nome de um aluno inexistente | turma `OPEN` → `CANCELLED`; nenhuma invariante acusou | estado intacto; `registrar_denied` |
| 2 | falsa retirada de professor enviada por participante inexistente | turma cancelada **e** professor com 2 horários bloqueados | estado intacto; `msg_denied` no departamento |
| 3 | matrícula com custo `NaN` | saldo vira `nan`, matrícula aceita; I6 só acusa depois | estado intacto; rejeitada no contrato |
| 4 | requisição sem o campo `op` | `KeyError`, o processamento é interrompido | estado intacto; recusa registrada |

Observação: no ataque 1 as invariantes I1–I7 **não** detectam o problema, porque o estado resultante é válido. Autorização não se verifica por invariante de estado;
por isso a correção está nas fronteiras dos protocolos, e não em mais uma invariante.

## Modelo de ameaça

- **Confiáveis (infraestrutura):** o `Environment`, o barramento e o Registrar. Eles aplicam as regras.
- **Não confiáveis (principais):** todos os agentes. Qualquer um pode tentar enviar mensagem malformada, em nome de outro, sobre recurso que não é dele ou fora do estado do protocolo.
- **Fora do escopo:** um agente com acesso direto à memória do processo ou ao código da infraestrutura. A autenticação é **simulada** (credencial emitida em memória);
  num sistema real seria assinatura ou canal autenticado (TLS). Isso é uma limitação declarada.

## Três camadas de defesa

1. **Fronteira do ambiente** (`Environment.execute`). Cada agente recebe uma **credencial secreta** ao se registrar (`Environment.register`, uma vez por identificador).
   A mensagem só entra no barramento se (a) a credencial corresponde ao remetente declarado, (b) o contrato do par protocolo/performativa é cumprido e (c) o papel do remetente e do destinatário é permitido.
   Caso contrário: `msg_rejected` no trace e nada muda. Isso impede **remetente inexistente** e **remetente falsificado** por outro agente.
2. **Caixa de entrada do receptor** (`Agent.screen`). Revalida o contrato de tudo que chega (cobre mensagens injetadas direto no barramento).
3. **Dono do estado confere a posse** (Registrar, Departamento, Professor, Sala, Aluno):

| Quem | Confere |
|---|---|
| Registrar | contrato; o remetente é o **departamento dono da disciplina** da turma; a `conv` corresponde à operação e à turma (`auc:<turma>:<n>`, `open:<turma>`, `cancel:<turma>`, `swap:<A>:<SA>:<SB>:<n>`); aluno, professor e sala existem. Nunca lança exceção. |
| Departamento | retirada só do **professor responsável** pela turma (e horários da própria turma); proposta só de professor convidado; resposta de sala só da sala consultada; lance só de aluno conhecido e da rodada certa; demanda só em nome do próprio aluno e de disciplina do departamento; troca só de quem está na turma cedida |
| Professor e Sala | só obedecem ao **próprio departamento** |
| Aluno | leilão, cancelamento e troca só valem se vierem do departamento dono da turma, conforme o quadro publicado |

## Contratos de mensagem

`contracts.SPEC` define, por (protocolo, performativa): papéis que podem enviar e receber, formato da `conv` e campos com tipo.
Regras gerais: campo obrigatório ausente, campo desconhecido, `bool` onde se espera inteiro, texto vazio ou longo demais, lista grande demais,
número não finito (`NaN`, `inf`), inteiro negativo ou acima de 10⁹, `op` desconhecido ou ausente — tudo é rejeitado **sem alterar estado**.
`Registrar.validate_enroll` também recusa preço não inteiro ou não finito, para o caso de uso direto da classe.

## Testes

- `tests/test_security.py` (T-SEC-01…18): os quatro ataques acima por dois caminhos (via Ambiente e direto no barramento), remetente real mas sem papel,
  departamento de outro departamento, conversa de outra turma, preço inválido (9 valores), conteúdos malformados (8 formas),
  fuzz de lixo para todos os agentes e protocolos. Os casos legítimos (cancelamento do departamento dono, retirada do professor responsável) continuam funcionando.
- `tests/test_adversarial.py` (T-ADV-01…09): mensagens **duplicadas**, **atrasadas** e fora de ordem, cancelamentos **concorrentes**, troca com falhas e **caos aleatório**
  (12 sementes, regras de perda/atraso/duplicação sobre qualquer protocolo): invariantes I1–I7 sempre válidas.
- O traço S0 com semente 7 continua **idêntico** ao da DSM2 (725 registros, sha256 `63e955f610e43987…`): a segurança não mudou o comportamento legítimo.
