# Proposed Technical Expansion Plan — Agentic / UX / Research Depth / Providers

> **Founder ask (2026-05-18):** Aprofundar features especialmente na parte agentica, UX, profundidade das pesquisas, providers, quantidade de fontes analisadas, capacidade de sumarização.

> **Current state:** 16 groups × 3 generic dims (cobertura/profundidade/evidência) = 48 dims. **Problem:** as 3 dims por grupo são genéricas — não medem features técnicas reais.

> **Proposed state:** 16 groups com decomposição feature-específica = **~120 dims × 25 players = ~3000 cells**.

## Eixo 1 — Agentic Planning Control (3 → 15 dims)

Como o agente decompõe, planeja, replan e recupera de falhas.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `apc__plan_explicit` | Planner emite plano explícito antes de executar (não improvise step-by-step)? | Replay + auditoria; sem plano = caixa preta |
| `apc__decomposition_strategy` | Estratégia de decomposição é declarada (BFS/DFS/parallel/hierarchical)? | Determinismo de pipeline |
| `apc__subquery_count_bounded` | Min/max de subqueries por wave é explícito (não infinite loop)? | Custos previsíveis |
| `apc__replanning_on_failure` | Replan automático quando wave falha ou retorna baixa coverage? | Resiliência |
| `apc__replanning_on_contradiction` | Replan quando sources contradizem entre si? | Quality recovery |
| `apc__plan_versioning` | Cada versão do plano é persistida (replay) ou só a final? | Provenance |
| `apc__user_steerable_plan` | User pode editar/aprovar plano antes da execução? | HITL granular |
| `apc__plan_visualization` | Plano é renderizado visualmente (graph/tree/timeline)? | UX transparência |
| `apc__cost_aware_planning` | Planner considera custo estimado (tokens/$$) por step? | Cost optimization |
| `apc__time_aware_planning` | Planner respeita time budget (ex: 5min cap)? | Predictability |
| `apc__early_termination` | Skill termina cedo quando coverage suficiente (não rodar waves desnecessárias)? | Efficiency |
| `apc__plan_skeptical_branches` | Planner gera branches devil's-advocate? | Anti-confirmation-bias |
| `apc__plan_grounded_in_taxonomy` | Plan é grounded em taxonomy de domínio (ex: PICO médico, JTBD product)? | Domain rigor |
| `apc__metaplanning` | Planner explica POR QUE escolheu cada strategy? | Explainability |
| `apc__plan_amendable_mid_execution` | Plan pode ser editado durante execução (não só pre-flight)? | Adaptive HITL |

## Eixo 2 — Multi-Agent Orchestration (3 → 12 dims)

Como sub-agents são criados, coordenados, e fundidos.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `mao__role_specialization` | Sub-agents têm roles distintas (Researcher/Editor/Reviewer)? | Division of concerns |
| `mao__true_parallel_spawn` | Sub-agents executam em paralelo real (não sequencial inline)? | Performance |
| `mao__max_concurrent_bound` | Max concorrência é cap-ado (ex: max 3 por turn)? | Resource control |
| `mao__handoff_contract_explicit` | Contrato de handoff (schema input/output) é explícito? | Reliability |
| `mao__message_passing_protocol` | Sub-agents passam dados via protocol claro (MCP/JSON-schema/etc)? | Composability |
| `mao__failure_isolation` | Falha de 1 sub-agent não derruba todos? | Resilience |
| `mao__lead_synthesizer_explicit` | Há um lead-agent que sintetiza outputs dos sub-agents? | Coordination |
| `mao__sub_agent_memory_isolation` | Cada sub-agent tem memória própria isolada (vs shared global)? | Boundary clarity |
| `mao__lifecycle_observability` | Spawn/terminate de sub-agents é loggado em event stream? | Audit trail |
| `mao__cross_session_team_persistence` | Equipes podem persistir entre sessions (não recriar do zero)? | Reuse |
| `mao__byzantine_tolerance` | Lead detecta sub-agent comprometido/hallucinating? | Quality safety |
| `mao__sub_agent_cost_attribution` | Custo é atribuído por sub-agent (não só global)? | Cost insight |

## Eixo 3 — Tool Runtime Integration (3 → 14 dims) — **PROVIDERS focus**

Quais providers/tools/APIs cada player integra e com que profundidade.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `tri__mcp_server_native` | Expõe MCP server consumível por Claude Desktop/Cursor/Cline? | Composability cross-IDE |
| `tri__mcp_client_native` | Consume MCP servers de terceiros nativamente? | Tool ecosystem |
| `tri__browser_automation` | Browser automation real (Playwright/Selenium/Puppeteer)? | Dynamic web |
| `tri__pdf_extraction` | Extrai texto/tabelas/figuras de PDFs? | Document research |
| `tri__youtube_transcription` | Transcreve YouTube nativamente? | Multimedia source |
| `tri__arxiv_api_native` | API arXiv integrada? | Academic depth |
| `tri__pubmed_api_native` | API PubMed integrada? | Medical research |
| `tri__semantic_scholar_native` | API Semantic Scholar integrada? | Citation graph |
| `tri__searxng_self_hosted` | Suporta SearXNG self-hosted (privacy)? | Local-first |
| `tri__google_scholar_scrape` | Google Scholar scraping (com cautela)? | Academic search |
| `tri__github_api_native` | API GitHub para code search? | Code research |
| `tri__hackernews_reddit_native` | HN/Reddit para community signal? | Trend detection |
| `tri__llm_provider_count` | Número de LLM providers suportados (BYOK)? | Model agnostic |
| `tri__function_calling_native` | Function calling nativo (não só ReAct prompt)? | Modern API |

## Eixo 4 — Research Depth & Synthesis (3 → 14 dims) — **FONTES + SUMARIZAÇÃO focus**

Quantidade, diversidade e qualidade das fontes; capacidade de síntese.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `rds__avg_sources_per_run` | Média de sources analisadas por run (ex: GPT-Researcher ~20, Kimi-Researcher 200+)? | Breadth quantified |
| `rds__deep_read_protocol` | Lê conteúdo COMPLETO (não só snippets)? | Anti-shallow |
| `rds__source_diversity_enforcement` | Força diversidade entre sources (não só top-5 Google)? | Anti-echo-chamber |
| `rds__source_credibility_weighting` | Credibility é considerada no synthesis weight? | Quality bias |
| `rds__freshness_enforcement` | Sources velhas penalizadas/removidas conforme temporal intent? | Currency |
| `rds__cross_source_contradiction_detect` | Detecta contradições entre sources e flag? | Honest synthesis |
| `rds__multi_lingual_sources` | Aceita sources em múltiplos idiomas (não só EN)? | Coverage |
| `rds__summarization_strategy_declared` | Estratégia de sumarização é declarada (extractive/abstractive/hybrid)? | Method transparency |
| `rds__compression_ratio_bounded` | Compression ratio é cap-ada (não over-compress)? | Fidelity |
| `rds__quote_preservation` | Quotes literais preservadas (não paraphrase passing as quote)? | Citation integrity |
| `rds__synthesis_preserves_disagreement` | Synthesis preserva discordância (não flatten para fake consensus)? | Epistemic honesty |
| `rds__wave_count_for_saturation` | Quantas waves até saturar info gain? | Effort calibration |
| `rds__longform_report_native` | Gera relatório longform (10+ pages) coerente? | Output depth |
| `rds__cited_paragraph_density` | Densidade de citações por parágrafo (>= 1 cite/§ )? | Auditability |

## Eixo 5 — Evidence Fidelity (3 → 10 dims) — **citation verify**

Como cada player verifica e mantém integridade de citações.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `efe__citation_verify_loop` | Loop de verify com fix attempts bounded? | AIOX moat |
| `efe__citation_gate_veto` | Gate halts se verified_ratio < threshold? | Quality enforcement |
| `efe__url_alive_check` | URL ainda aberto/acessível? | Link rot defense |
| `efe__quote_match_exact` | Quote bate exatamente com source content? | Anti-hallucination |
| `efe__publication_date_check` | Data publicação ≥ minimum required by temporal intent? | Freshness |
| `efe__author_attribution_explicit` | Author nomeado (não só "fonte X")? | Attribution rigor |
| `efe__contradiction_flagged` | Quando 2 sources contradizem, sistema flagga? | Honest debate |
| `efe__retraction_check` | Verifica se paper foi retracted? | Scholarly integrity |
| `efe__primary_vs_secondary_classified` | Distingue primary (paper) vs secondary (blog citando paper)? | Source rigor |
| `efe__archive_snapshot_taken` | Faz archive.org snapshot da source (immutability)? | Permanence |

## Eixo 6 — UX Operator Control (3 → 10 dims)

Como o user controla, dirige, e audita o agent durante execução.

| Microdim ID | Question | Why it matters |
|---|---|---|
| `uoc__live_streaming_output` | Output streams em tempo real (SSE/WebSocket)? | Feedback latency |
| `uoc__interrupt_mid_execution` | User pode interromper mid-execution? | Steerability |
| `uoc__edit_plan_mid_execution` | User edita plano sem rebootar? | Adaptive HITL |
| `uoc__hitl_modes_granular` | Múltiplos modos HITL (yolo / interactive / pre-flight / full-auto)? | Use-case flex |
| `uoc__progress_visualization` | Progresso visualizado (não só logs texto)? | UX richness |
| `uoc__per_phase_approval` | Approval gates por fase opcionais? | Trust building |
| `uoc__cost_meter_live` | Cost meter ($/tokens) live durante run? | Cost discipline |
| `uoc__rollback_to_phase` | Rollback para fase anterior sem perder evidência? | Recovery |
| `uoc__natural_language_steering` | User dirige via natural language ("foque mais em X")? | Conversational HITL |
| `uoc__shareable_run_link` | Link compartilhável do run (URL state)? | Collaboration |

## Eixo 7 — Outros 10 grupos (decomposição moderada, 3 → 5-7 dims cada)

Recebem decomposição mais leve mas ainda feature-específica:

- **Architecture Absorption** (3→6): cobertura, profundidade, replay, REUSE-readiness, license-clean-room, ADR-quality
- **Implementation Maturity** (3→6): test-coverage, CI/CD presence, error-handling, prod-deployments, versioning, semver-discipline
- **Trace Observability** (3→6): event-jsonl, span-tracking, latency-attribution, tool-call-replay, OTEL-native, dashboard-live
- **Private KB Grounding** (3→7): vector-db-native, embedding-models, hybrid-search, doc-chunking, RAG-rerank, citation-from-private, doc-update-detection
- **Evaluation Value** (3→6): public-bench-score, eval-harness-included, reproducible-eval, golden-fixtures, regression-tests, drift-detection
- **Scientific Pipeline** (3→6): hypothesis-formal, experiment-protocol, statistical-test, peer-review-simulation, paper-format-output, replication-package
- **Training Methodology** (3→5): RL-pipeline, supervised-data, fine-tune-recipe-open, eval-on-public-bench, model-card-quality
- **Product UX Reference** (3→5): main-UI-quality, mobile-responsive, accessibility, dark-mode, i18n
- **Compliance Safety** (3→5): SOC2-ready, GDPR-aware, PII-detection, content-moderation, copyright-respect
- **Sinkra Fit** (3→3 mantém): hub-native, dogfood-presence, governance-alignment

## Distribuição final proposta

| Group | Dims |
|---|---:|
| Agentic Planning Control | 15 |
| Multi-Agent Orchestration | 12 |
| Tool Runtime Integration | 14 |
| Research Depth & Synthesis | 14 |
| Evidence Fidelity Evaluation | 10 |
| UX Operator Control | 10 |
| Private KB Grounding | 7 |
| Architecture Absorption | 6 |
| Implementation Maturity | 6 |
| Trace Observability | 6 |
| Evaluation Value | 6 |
| Scientific Pipeline | 6 |
| Training Methodology | 5 |
| Product UX Reference | 5 |
| Compliance Safety | 5 |
| Sinkra Fit | 3 |
| **Total** | **130** |

130 microdims × 25 players = **3,250 cells**.

## Pesos recalibrados

Tu pediu foco em agentica/UX/profundidade/providers/fontes/sumarização. Pesos sugeridos:

| Group | Peso | Justificativa |
|---|---:|---|
| Agentic Planning Control | 15 | Core do "deep research" |
| Tool Runtime Integration | 13 | Providers/sources discovery |
| Research Depth & Synthesis | 13 | Fontes + sumarização |
| Multi-Agent Orchestration | 10 | Paralelismo + division of concerns |
| Evidence Fidelity Evaluation | 10 | Anti-hallucination |
| UX Operator Control | 9 | Steerability |
| Private KB Grounding | 6 | RAG depth |
| Architecture Absorption | 5 | Absorbability |
| Implementation Maturity | 5 | Prod readiness |
| Trace Observability | 4 | Audit |
| Evaluation Value | 4 | Bench score |
| Scientific Pipeline | 3 | Specialized use |
| Training Methodology | 1 | Reference only |
| Product UX Reference | 1 | Visual reference |
| Compliance Safety | 1 | Enterprise gate |
| Sinkra Fit | 0 | Anchor self-ref (excluded from total) |
| **Total** | **100** | |

Sinkra Fit fica peso 0 (anchor self-reference, transparency disclosure) — endereça o pecado #6 anterior.

## Cell generation strategy

Para cada microdim × 25 players = 25 cells:

1. **AIOX scores**: derivados de evidência REAL no codebase (clones + skill source). Honest mesmo quando é 0.
2. **OSS scores**: derivados de inspeção de clones em `../bench/{player}/` + README claims + arXiv paper claims.
3. **Confidence**: `high` (clone evidence direct), `medium` (README claim), `low` (inferred from indirect signals).
4. **Notes**: 1-line factual statement (e.g. "arXiv API native via `arxiv.py` adapter — 47 lines").
5. **Source**: file path inside the clone (e.g. `../bench/local-deep-research/src/local_deep_research/search_engines/arxiv.py`).

## Approval needed before applying

Aplicar 130 dims × 25 players = 3,250 cells é trabalho grande (~30min). Confirma que essa decomposição é o que tu queria antes de eu rodar?

Alternativas:

- **A) Aplicar plano completo (130 dims, 3,250 cells)** — mais profundo, máxima granularidade técnica
- **B) Aplicar só os 6 eixos prioritários** (Agentic + Multi-Agent + Tool Runtime + Research Depth + Evidence + UX = 75 dims, 1,875 cells novas). Outros 10 grupos ficam no 3-dim atual
- **C) Pilot em 2 grupos primeiro** (Agentic Planning Control 15 dims + Research Depth 14 dims) para validar formato antes de escalar
