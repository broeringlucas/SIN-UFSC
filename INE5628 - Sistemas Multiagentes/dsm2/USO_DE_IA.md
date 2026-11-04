# Uso de IA — DSM2

## Ferramenta

- **Claude** (Anthropic), via claude.ai / Claude Code, modelo Claude Sonnet 5.5.
- Material fornecido à IA: o enunciado da DSM2, a entrega da DSM1 (README, relatório em PDF, fontes dos diagramas) e as anotações do professor sobre a DSM1.

## Como a IA foi usada

| Atividade | O que a IA fez | O que a equipe fez ou decidiu |
|---|---|---|
| Planejamento da arquitetura | Auxiliou na definição da arquitetura e na organização dos componentes do sistema multiagentes | Análise das propostas, definição da estrutura final e ajustes necessários |
| Desenvolvimento do código | Auxiliou na implementação do simulador, dos agentes e das funcionalidades do sistema | Revisão do código, execução e validação da implementação |
| Refinamento das regras | Ajudou a estruturar as regras de funcionamento, os protocolos e as políticas dos agentes | Análise das regras propostas e realização de ajustes |

## Verificação e responsabilidade

A equipe é responsável por todo o conteúdo entregue. Marque apenas o que de fato foi feito:

- [X] Executei `python -m pytest -q` e `python -m matriculaufsc --scenario S0 --seed 7` na minha máquina e os resultados batem com o README.
- [X] Conferi o roteiro do cenário S0 (`docs/cenario_S0.md`) contra o trace gerado.
- [X] Revisei a tabela de rastreabilidade requisito → teste do README (§9).
- [X] Conferi que o README só descreve arquivos e comandos que existem na entrega.

## Limitações

- Nenhuma regra oficial da UFSC foi consultada; o modelo é didático e usa dados sintéticos.
- O código foi gerado pela IA e testado com testes também escritos pela IA; testes que passam não provam que o modelo representa a matrícula real.
- A comparação entre leilão, ordem de chegada e prioridade é indicativa (um cenário gerado, 15 sementes, sem teste estatístico); não é um resultado conclusivo.
- O protocolo de troca de vagas entre alunos (`seat_swap`) não foi implementado nesta entrega.
