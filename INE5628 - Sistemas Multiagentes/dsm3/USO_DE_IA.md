# Uso de IA — DSM3
 
## Ferramenta
 
- **Claude** (Anthropic), via claude.ai / Claude Code, modelo Claude Sonnet 5.5.
- Material fornecido à IA: o enunciado da DSM3, o código e a documentação entregues na DSM2 (`dsm2.zip`) e o feedback do professor sobre a DSM2.
## Como a IA foi usada
 
| Atividade | O que a IA fez | O que a equipe fez ou decidiu |
|---|---|---|
| Análise do feedback | Auxiliou na reprodução, com scripts (`scripts/ataques.py`), das quatro falhas apontadas pelo professor no código da DSM2 | Leitura do feedback, conferência de que as falhas existiam e decisão de corrigi-las na fronteira dos protocolos |
| Autorização e validação | Auxiliou na implementação de credenciais, contratos de mensagem (`contracts.py`) e checagem de posse no Registrar, nos departamentos e nos demais agentes, e na documentação (`docs/seguranca.md`) | Revisão do código, execução e validação da implementação; aceitou a autenticação simulada como limitação |
| Protocolos novos | Auxiliou na implementação de `seat_swap` (troca de vagas) e `sync` (recuperação de crenças), com máquinas de estados e tratamento de falhas, e na escrita de `docs/protocolos.md` | Definição do escopo dos protocolos, análise das regras propostas e ajustes |
| Testes e evidências | Auxiliou na escrita dos testes de segurança, troca, sincronização e adversariais, dos scripts de experimento e dos arquivos de `docs/evidencias/` | Execução dos testes e conferência das evidências |
 
## Verificação e responsabilidade
 
A equipe é responsável por todo o conteúdo entregue. Marque apenas o que de fato foi feito:
 
- [X] Executei `py -m pytest -q` na minha máquina e o resultado bate com o README (213 testes passando).
- [X] Executei `py -m matriculaufsc --scenario S0 --seed 7` e `py -m matriculaufsc --scenario S2 --seed 1` e os hashes batem com `docs/evidencias/`.
- [X] Executei `py scripts/ataques.py` e conferi a tabela DSM2 × DSM3 de `docs/seguranca.md`.
- [X] Revisei a matriz requisito → teste do README e `docs/checkpoints.md`.
- [X] Conferi que o README só descreve arquivos e comandos que existem na entrega.

## Limitações
 
- Nenhuma regra oficial da UFSC foi consultada; o modelo é didático e usa dados sintéticos.
- O código foi gerado pela IA e testado com testes também escritos pela IA; testes que passam não provam que o modelo representa a matrícula real.
- A autenticação é simulada (credencial emitida em memória); num sistema real seria assinatura ou canal autenticado.
- O efeito das trocas de vagas é pequeno e raro (S1, 16 alunos, 15 sementes, sem teste estatístico); a comparação entre leilão, ordem de chegada e prioridade continua indicativa, não conclusiva.
- A troca de vagas só ocorre entre turmas da mesma disciplina.
 