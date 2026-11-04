# MatriculaUFSC

Ajuste de matrícula e oferta de turmas na UFSC modelado como **Sistema Multiagente (SMA)**.
Projeto da disciplina INE5628 – Sistemas Multiagentes (UFSC, 2026/2), Prof. Rafael Luiz Cancian.

> **Status: DSM1 (cenário, requisitos e modelagem).** Esta entrega materializa os checkpoints CP1 a CP3
> (documentação e modelos). O código começa no CP4. Tudo que aparece marcado como *(planejado)* ainda **não existe**.


## Resumo do problema

Alunos de diversos cursos disputam vagas em turmas ofertadas por diferentes departamentos. Cada turma depende
de um professor (com limite de carga e preferências) e de uma sala, muitas vezes compartilhada entre departamentos.
Os alunos têm metas privadas e conflitantes, cada departamento só conhece a própria oferta e eventos (sala interditada,
professor indisponível, turma cancelada) mudam o problema durante a execução. O sistema coordena a alocação de vagas,
as trocas entre alunos e a abertura de novas turmas por negociação entre agentes autônomos.

O modelo é **didático**: não reproduz regras oficiais da UFSC e usa apenas **dados sintéticos**.

## Agentes

| Agente | Arquitetura | Papel |
|---|---|---|
| `StudentAgent` ×N | BDI | aluno: decide onde e quanto ofertar, quando trocar e quando desistir |
| `ProfessorAgent` ×M | BDI | professor: decide propor ou recusar a abertura de turma conforme carga e preferência |
| `DepartmentAgent` ×D | deliberativo | departamento: conduz leilões e aberturas da própria oferta |
| `ClassroomAgent` ×R | reativo com estado | sala compartilhada: arbitra reservas sem conflito de horário |
| `Registrar` / `PolicyService` | determinístico (não é agente) | valida pré-requisito, horário, carga e capacidade; efetiva matrículas |

## Protocolos

| Protocolo | Mecanismo |
|---|---|
| `seat_auction` | leilão de lance selado com orçamento de pontos (`cfp` → `propose`/`refuse` → `accept`/`reject` → `inform`) |
| `seat_swap` | troca bilateral entre alunos, com commit atômico pelo Registrar |
| `section_opening` | Contract Net entre departamento e professores para abrir turma |
| `room_reservation` | `request` → `agree`/`refuse` → `inform`, com exclusão temporal |

## Conteúdo deste repositório

```
.
├── README.md                          este arquivo
├── USO_DE_IA.md                       declaração de uso de IA (rascunho a revisar)
└── docs/
    ├── DSM1_MatriculaUFSC.pdf         relatório da DSM1 (5 páginas, layout do template)
    ├── DSM1_MatriculaUFSC.docx        fonte editável do relatório
    └── diagramas/                     fontes editáveis + imagens geradas
        ├── 01_contexto.dot            Figura 1: contexto e fronteira
        ├── 02_objetivos.dot           decomposição de objetivos (complementar; não consta no relatório)
        ├── 03_sequencia_seat_auction.py   Figura 2: sequência do leilão (matplotlib)
        ├── 04_fsm_protocolos.dot      Figura 3: FSMs dos protocolos
        └── *.png, *.svg               imagens geradas a partir das fontes
```

## Como regenerar os diagramas

Requisitos: [Graphviz](https://graphviz.org/) (`dot`), Python 3 com `matplotlib`. A fonte usada nas imagens é a
Carlito; se ela não estiver instalada, o Graphviz e o matplotlib usam uma fonte alternativa.

```bash
cd docs/diagramas
for f in 01_contexto 02_objetivos 04_fsm_protocolos; do
  dot -Tpng -Gdpi=200 $f.dot -o $f.png
  dot -Tsvg $f.dot -o $f.svg
done
python 03_sequencia_seat_auction.py      # gera .png e .svg
```

Depois de alterar uma figura, reinsira a imagem no `.docx` e exporte novamente o PDF.

## Plano de checkpoints (CP1 a CP13)

| CP | Etapa | Artefatos | Situação |
|---|---|---|---|
| CP1 | Cenário e justificativa | project charter (relatório, seções 1 e 2) | materializado |
| CP2 | Requisitos, objetivos e papéis | objetivos, requisitos, papéis e agentes (seções 1 e 3 a 5) | materializado |
| CP3 | Modelo formal e protocolos | invariantes, protocolos, FSMs, métricas (seções 5.1, 6 e 7) | especificado; executável nos CP5 e CP6 |
| CP4 | Repositório e baseline | estrutura do projeto, baseline B1 (ordem de chegada) offline com seed | README definido; código a fazer |
| CP5 | Comunicação multiagente | MessageBus, schema de mensagem, TraceLogger JSONL | planejado |
| CP6 | Coordenação e alocação | os quatro protocolos acima | planejado |
| CP7 | Tools | ToolRegistry com adapters somente-leitura (catálogo, horários de sala) | planejado |
| CP8 | Conhecimento | regulamento didático em KnowledgeBase offline com Provenance | planejado |
| CP9 | Memória | MemoryStore SQLite com lances de corte agregados, sem identificar alunos | planejado |
| CP10 | Segurança e observabilidade | Registrar/PolicyService executável, logger sem dados pessoais | planejado |
| CP11 | Testes | suíte `pytest` conforme a matriz de rastreabilidade | planejado |
| CP12 | Experimento | runner dos cenários S1 a S4 com seeds, resultados e análise | planejado |
| CP13 | Integração e apresentação | README final, relatório final, demonstração | planejado |

## Plano de implementação *(planejado, a partir do CP4)*

- **Runtime:** Python simples (biblioteca padrão e `pytest`), com MessageBus próprio e simulação por rodadas discretas.
  Justificativa: o ciclo BDI e os protocolos cabem no modelo de rodadas, sem necessidade de Jason ou JADE.
- **Reprodutibilidade:** toda aleatoriedade vem de `random.Random(seed)`; o baseline e a versão multiagente rodam
  sem API paga e sobre os mesmos cenários e seeds.
- **Estrutura prevista do código:**

  ```
  src/matriculaufsc/   bus.py, trace.py, registrar.py, agents/, protocols/, env/, baseline/
  tests/               um arquivo por grupo de testes da matriz de rastreabilidade
  scenarios/           S1 nominal, S2 alta demanda, S3 sala interditada, S4 professor indisponível
  ```

- **Comandos previstos:**

  ```bash
  python -m matriculaufsc.run --scenario S2 --seed 7 --trace out/trace.jsonl   # (planejado)
  pytest                                                                        # (planejado)
  ```

## Rastreabilidade

Cada requisito (`REQ-*`) aponta para objetivo, papel, protocolo, teste e métrica na seção 9 do relatório.
Regra do projeto: nenhum requisito crítico sem teste, e nenhum teste sem requisito.

## Autoria e uso de IA

O uso de ferramentas de IA neste trabalho está declarado em [`USO_DE_IA.md`](USO_DE_IA.md).
