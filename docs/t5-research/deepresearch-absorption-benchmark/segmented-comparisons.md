# Comparações Segmentadas

Este arquivo substitui o recorte antigo de 9/14 players por seis segmentações baseadas nas 24 anatomias locais.

# Rankings Por Cenário

## Melhor arquitetura para absorção imediata

Padrões de runtime, lifecycle, graph, actions e contracts.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | DeerFlow | 96 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 2 | LangChain Open Deep Research | 92 | absorb_graph_pattern | Supervisor/researcher subgraphs, ConductResearch paralelo, tool contract. |
| 3 | GPT-Researcher | 89 | absorb_facade_and_strategy | Source strategy, retriever fan-out, MCP retriever, context compression. |
| 4 | DRBench | 88 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 5 | Local Deep Research | 88 | absorb_private_local_adapter | MCP/API programática, AdvancedSearchSystem, search engine registry. |
| 6 | AutoResearchClaw | 87 | absorb_contracts_gates | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| 7 | DeepSearcher | 87 | absorb_rag_patterns | Provider registry, collection routing, ChainOfRAG, sentence-window wider_text. |
| 8 | Deep Research Bench | 86 | absorb_evaluator | Fixture/evaluator adapter, submitted article contract, utils/api boundary. |

## Melhor para private-KB/local-first

Dados internos sintéticos, RAG privado, isolamento e controle local.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | Local Deep Research | 96 | absorb_private_local_adapter | MCP/API programática, AdvancedSearchSystem, search engine registry. |
| 2 | DRBench | 95 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 3 | DeepSearcher | 95 | absorb_rag_patterns | Provider registry, collection routing, ChainOfRAG, sentence-window wider_text. |
| 4 | STORM | 84 | absorb_interfaces_artifacts | Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts. |
| 5 | Agent Browser Workspace | 80 | absorb_toolkit_adapter | Chrome CDP, links.json, Markdown/PDF extraction, site profiles/controllers. |
| 6 | DeerFlow | 68 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 7 | GPT-Researcher | 68 | absorb_facade_and_strategy | Source strategy, retriever fan-out, MCP retriever, context compression. |
| 8 | MiroThinker | 68 | absorb_profile_trace_patterns | Profiles Hydra, ToolManager MCP, TaskLog/TraceAnalyzer. |

## Melhor para avaliação gold

Harness, métricas, judge contracts, claim-level scoring e fixtures.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | DRBench | 96 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 2 | LiveDRBench | 92 | absorb_metric_contract | Claim-level precision/recall/F1, category graders, anti-leakage key. |
| 3 | MiroEval | 88 | absorb_evaluator | Segment-parallel-merge, rubrica dinâmica, process/report alignment. |
| 4 | Deep Research Bench | 84 | absorb_evaluator | Fixture/evaluator adapter, submitted article contract, utils/api boundary. |
| 5 | AutoResearchClaw | 80 | absorb_contracts_gates | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| 6 | DeerFlow | 42 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 7 | STORM | 42 | absorb_interfaces_artifacts | Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts. |
| 8 | GPT-Researcher | 42 | absorb_facade_and_strategy | Source strategy, retriever fan-out, MCP retriever, context compression. |

## Melhor para pesquisa científica

Papers, literatura, prior art, stage gates e artefatos intermediários.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | AutoResearchClaw | 96 | absorb_contracts_gates | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| 2 | STORM | 92 | absorb_interfaces_artifacts | Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts. |
| 3 | OpenResearcher | 88 | clean_room_patterns | browser.search/open/find contract, append-only shards, retriever fixture. |
| 4 | DeepResearcher | 84 | pattern_first | agent_grpo.n/idx, multi-trajectories, web_search/browse contract. |
| 5 | DRBench | 40 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 6 | DeerFlow | 40 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 7 | GPT-Researcher | 40 | absorb_facade_and_strategy | Source strategy, retriever fan-out, MCP retriever, context compression. |
| 8 | Local Deep Research | 40 | absorb_private_local_adapter | MCP/API programática, AdvancedSearchSystem, search engine registry. |

## Melhor para metodologia RL/treino

Reward shaping, trajectories, post-training e tool-use multi-turn.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | MiroRL | 96 | pattern_first | Reward shaping para tool-use, MCPTool, rollout state machine. |
| 2 | DeepResearcher | 92 | pattern_first | agent_grpo.n/idx, multi-trajectories, web_search/browse contract. |
| 3 | MiroTrain | 88 | pattern_first | Wrapper config-first, dataset/tokenizer adapter, Ulysses, Qwen3 MoE. |
| 4 | OpenResearcher | 84 | clean_room_patterns | browser.search/open/find contract, append-only shards, retriever fixture. |
| 5 | DRBench | 36 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 6 | DeerFlow | 36 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 7 | AutoResearchClaw | 36 | absorb_contracts_gates | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| 8 | STORM | 36 | absorb_interfaces_artifacts | Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts. |

## Melhor referência de produto/UX

Loops de chat, runs, threads, artifacts e experiência de pesquisa.

| Rank | Player | Score | Decisão | Por que |
| --- | --- | --- | --- | --- |
| 1 | DeerFlow | 96 | absorb_core_patterns | Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge. |
| 2 | GPT-Researcher | 92 | absorb_facade_and_strategy | Source strategy, retriever fan-out, MCP retriever, context compression. |
| 3 | nickscamara/open-deep-research | 88 | reference_ux_baseline | Loop search-extract-gap-repeat-synthesize, event vocabulary. |
| 4 | JigsawStack Deep Research | 84 | absorb_interface_avoid_globals | Factory pequena, provider custom web_search, roles de modelo separados. |
| 5 | Jina node-DeepResearch | 80 | absorb_action_schema | schemas.ts, safe-generator, ações search/visit/reflect/answer/coding. |
| 6 | DRBench | 42 | absorb_fixture_oracle | task/eval/env/report_insights contract, score_report, private-KB fixture. |
| 7 | AutoResearchClaw | 42 | absorb_contracts_gates | StageContract, VerifiedRegistry, stage ledger, HITL policy. |
| 8 | STORM | 42 | absorb_interfaces_artifacts | Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts. |


