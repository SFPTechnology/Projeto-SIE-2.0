# DeepResearch Absorption Benchmark

Bench canônico: `docs/bench/deepresearch-absorption-benchmark/`  
Snapshot gold: 2026-05-18  
Escopo: AIOX Research como referência interna + 24 players externos de deep research, com pesquisa gold, metadata GitHub, protocolo experimental, clones locais e anatomia local de código.

## Consolidação

Esta é a única pasta canônica do **DeepResearch Absorption Benchmark** em `docs/bench`. As versões antigas `2026-05-18-deepresearch-absorption-benchmark` e `2026-05-16-deep-research-absorption-benchmark` foram consolidadas aqui.

- Arquivos únicos úteis foram promovidos para esta raiz canônica.
- Arquivos conflitantes, mais antigos ou de modelo anterior foram preservados sem sobrescrever a versão atual em [`consolidated-sources/`](./consolidated-sources/).
- Relatório da consolidação: [`consolidated-sources/consolidation-report.md`](./consolidated-sources/consolidation-report.md).

## TL;DR

Este bench não recomenda copiar um projeto inteiro. A decisão correta é construir um **SINKRA Deep Research Stack** por absorção seletiva de padrões:

- **Runtime/lifecycle:** DeerFlow.
- **Graph de pesquisa paralela:** LangChain Open Deep Research.
- **Facade, source strategy e MCP:** GPT-Researcher.
- **Baseline mínimo audível:** dzhng/deep-research.
- **Action schema TypeScript:** Jina node-DeepResearch.
- **Private-KB:** Local Deep Research + DeepSearcher + DRBench.
- **Avaliação gold:** DRBench + LiveDRBench + MiroEval + Deep Research Bench.
- **Stage contracts científicos:** AutoResearchClaw.
- **Aquisição browser/evidência:** Agent Browser Workspace.

## Leaderboard De Absorção

Matriz expandida em 2026-05-18: **25 players × 48 microdimensões = 1.200 células**. As 30 dimensões anteriores preservam 70% do peso; as 18 novas dimensões técnicas adicionam agenticidade, tool runtime, UX, evidência e profundidade de pesquisa.

| Rank | Player | Score | Classe | Decisão | Repo |
| --- | --- | ---: | --- | --- | --- |
| 1 | AIOX Research | 84.65 | sinkra_reference_system | internal_reference | SINKRA Hub / Squad Research |
| 2 | AutoResearchClaw | 79.24 | scientific_pipeline | absorb_contracts_gates | aiming-lab/AutoResearchClaw |
| 3 | DeerFlow | 78.88 | agentic_platform | absorb_core_patterns | bytedance/deer-flow |
| 4 | GPT-Researcher | 76.41 | research_facade | absorb_facade_and_strategy | assafelovic/gpt-researcher |
| 5 | STORM | 75.15 | article_research_pipeline | absorb_interfaces_artifacts | stanford-oval/storm |
| 6 | Local Deep Research | 73.30 | local_private_runtime | absorb_private_local_adapter | LearningCircuit/local-deep-research |
| 7 | DRBench | 72.75 | enterprise_benchmark | absorb_fixture_oracle | ServiceNow/drbench |
| 8 | LangChain Open Deep Research | 72.75 | graph_runtime | absorb_graph_pattern | langchain-ai/open_deep_research |
| 9 | MiroThinker | 72.39 | hydra_mcp_runtime | absorb_profile_trace_patterns | MiroMindAI/MiroThinker |
| 10 | MiroFlow | 72.14 | agentic_benchmark_runtime | absorb_trace_tool_registry | MiroMindAI/MiroFlow |
| 11 | MiroRL | 70.99 | rl_training_framework | pattern_first | MiroMindAI/MiroRL |
| 12 | DeepResearcher | 70.97 | verl_rl_fork | pattern_first | GAIR-NLP/DeepResearcher |
| 13 | Alibaba/Tongyi DeepResearch | 70.13 | research_monorepo_react | absorb_patterns_no_vendor | Alibaba-NLP/DeepResearch |
| 14 | DeepSearcher | 70.08 | private_kb_rag | absorb_rag_patterns | zilliztech/deep-searcher |
| 15 | Jina node-DeepResearch | 69.76 | action_state_machine | absorb_action_schema | jina-ai/node-DeepResearch |
| 16 | MiroEval | 69.22 | benchmark_harness | absorb_evaluator | MiroMindAI/MiroEval |
| 17 | OpenResearcher | 69.03 | benchmark_runner_agent_harness | clean_room_patterns | TIGER-AI-Lab/OpenResearcher |
| 18 | MiroTrain | 68.06 | post_training_pipeline | pattern_first | MiroMindAI/MiroTrain |
| 19 | Deep Research Bench | 66.95 | benchmark_evaluator | absorb_evaluator | Ayanami0730/deep_research_bench |
| 20 | Agent Browser Workspace | 66.37 | browser_acquisition_toolkit | absorb_toolkit_adapter | k-kolomeitsev/agent-browser-workspace |
| 21 | LiveDRBench | 66.10 | claim_evaluator | absorb_metric_contract | microsoft/LiveDRBench |
| 22 | dzhng/deep-research | 65.68 | compact_baseline | use_as_minimal_baseline | dzhng/deep-research |
| 23 | nickscamara/open-deep-research | 61.54 | nextjs_chatbot | reference_ux_baseline | nickscamara/open-deep-research |
| 24 | HKUDS Auto-Deep-Research | 60.95 | autoagent_metachain_cli | absorb_concepts_with_sandbox | HKUDS/Auto-Deep-Research |
| 25 | JigsawStack Deep Research | 59.73 | typescript_library | absorb_interface_avoid_globals | JigsawStack/deep-research |

## Vencedores Por Cenário

| Cenário | Vencedor | Score | Sinal de absorção |
| --- | --- | --- | --- |
| Melhor arquitetura para absorção imediata | DeerFlow | 96 | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| Melhor para private-KB/local-first | Local Deep Research | 96 | MCP/API programática, AdvancedSearchSystem, search engine registry. |
| Melhor para avaliação gold | DRBench | 96 | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| Melhor para pesquisa científica | AutoResearchClaw | 96 | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| Melhor para metodologia RL/treino | MiroRL | 96 | Reward shaping para tool-use, MCPTool, rollout state machine. |
| Melhor referência de produto/UX | DeerFlow | 96 | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |

## Vencedores Por Macrogrupo Expandido

| Macrogrupo | Vencedor mais frequente | Leitura |
| --- | --- | --- |
| Architecture Absorption | DeerFlow | 3/3 microdimensões |
| Trace Observability | MiroThinker | 3/3 microdimensões |
| Private Kb Grounding | Local Deep Research | 2/3 microdimensões |
| Evaluation Value | DRBench | 3/3 microdimensões |
| Implementation Maturity | DeerFlow | 3/3 microdimensões |
| Scientific Pipeline | AutoResearchClaw | 3/3 microdimensões |
| Training Methodology | MiroRL | 3/3 microdimensões |
| Product Ux Reference | DeerFlow | 3/3 microdimensões |
| Compliance Safety | AIOX Research | 3/3 microdimensões |
| Sinkra Fit | AIOX Research | 3/3 microdimensões |
| Agentic Planning Control | AIOX Research | 3/3 microdimensões |
| Multi-Agent Orchestration | DeerFlow | 3/3 microdimensões |
| Tool Runtime Integration | Agent Browser Workspace | 3/3 microdimensões |
| Research Depth Synthesis | OpenResearcher | 3/3 microdimensões |
| Evidence Fidelity Evaluation | LiveDRBench | 3/3 microdimensões |
| UX Operator Control | AIOX Research | 3/3 microdimensões |

## Arquivos Principais

- [Scorecard JSON](./scorecard.json) e [Scorecard MD](./scorecard.md)
- [Matriz comparativa JSON](./comparison-matrix.json) e [Matriz comparativa MD](./comparison-matrix.md)
- [Rankings por cenário JSON](./scenario-scorecards.json) e [Rankings por cenário MD](./scenario-scorecards.md)
- [Relatório executivo](./executive-report.md)
- [Battle card](./battle-card.md)
- [Gap analysis](./gap-analysis.md)
- [Risk register](./risk-register.md)
- [Implementation readiness gate](./implementation-readiness-gate.md)
- [Evidence ledger](./evidence-ledger.md)
- [Metodologia](./deep/methodology.md)
- [Mapa de adoção SINKRA](./deep/sinkra-adoption-map.md)
- [Inventários por player](./inventories/)

## Nota Metodológica

A pontuação é de **prontidão de absorção técnica e arquitetural**, não uma alegação de execução end-to-end em todos os 40 tasks do protocolo SINKRA-DR-40. A versão expandida inclui 48 microdimensões: 30 originais reponderadas para 70% e 18 novas dimensões para agenticidade, UX, tool runtime, fidelidade de evidência e profundidade de pesquisa. A execução factual por player ainda exige protocolo E2E comum.
