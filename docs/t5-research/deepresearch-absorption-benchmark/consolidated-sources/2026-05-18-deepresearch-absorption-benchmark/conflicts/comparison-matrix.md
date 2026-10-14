# Comparison Matrix — Microdimensional (102 × 10)
> **1020 cells** baseadas em scan local de 9 player clones em `../bench/` + 75 overrides com evidência direta.
> Score 0-100 por microdimensão. Groups têm weights somando 100. Atoms têm weights somando dentro do group.

## Method

102 microdimensions decomposed from 34 macro atoms in 13 groups. Each macro atom split into 3 operational microchecks (some 1-2). Total cells 1020.

## Scoring Guide

| Range | Meaning |
|---|---|
| 0-20 | ausente ou não operacional |
| 21-49 | fraco / protótipo |
| 50-69 | cobertura parcial |
| 70-84 | cobertura forte |
| 85-100 | referência de absorção |

## Totals Ranking

| Rank | Player | Score |
|---:|---|---:|
| 1 | DeerFlow (ByteDance) | 72.05 |
| 2 | GPT-Researcher | 69.65 |
| 3 | AutoResearchClaw | 69.65 |
| 4 | Local Deep Research | 63.9 |
| 5 | AIOX Research Ecosystem | 60.25 |
| 6 | Tongyi DeepResearch | 52.1 |
| 7 | LangChain Open DR | 51.7 |
| 8 | DeepResearcher 7B RL | 50.95 |
| 9 | OpenResearcher 30B | 48.2 |
| 10 | Jina node-DR | 44.5 |

## Microdimensions by Group

### Entrada (weight 5)

_Como o sistema recebe a query (CLI, API, UI, MCP)_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `cli_entry` | Player aceita query via CLI standalone? | 75 | 90 | 95 | 70 | 70 | 50 | 40 | 85 | 60 | 50 | **GPT-R** (95) |
| `api_entry` | Player expõe API standalone para consumo headless? | 75 | 90 | 95 | 70 | 70 | 50 | 40 | 85 | 60 | 50 | **GPT-R** (95) |
| `ui_entry` | Player tem UI native para consumir research? | 75 | 90 | 95 | 70 | 70 | 50 | 40 | 85 | 60 | 50 | **GPT-R** (95) |
| `mcp_server_exposed` | Player publica MCP server consumível por Claude Desktop? | 0 | 0 | 100 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | **GPT-R** (100) |
| `mcp_tools_count` | Quantas tools MCP o player expõe? | 0 | 0 | 95 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | **LC-ODR** (100) |
| `mcp_transport_support` | Suporta stdio + HTTP/SSE transports? | 0 | 0 | 95 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | **LC-ODR** (100) |
| `rest_endpoints` | Tem endpoints REST documentados? | 35 | 80 | 95 | 70 | 60 | 30 | 30 | 95 | 50 | 30 | **GPT-R** (95) |
| `sse_streaming` | Suporta streaming de progresso via SSE? | 35 | 80 | 95 | 70 | 60 | 30 | 30 | 95 | 50 | 30 | **GPT-R** (95) |
| `auth_layer` | Tem camada de auth para uso multi-tenant? | 35 | 80 | 95 | 70 | 60 | 30 | 30 | 95 | 50 | 30 | **GPT-R** (95) |

### Planejamento (weight 10)

_Auto-clarify, decompose, prompt generation_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ambiguity_detect` | Detecta query ambígua automaticamente? | 100 | 80 | 70 | 60 | 50 | 30 | 40 | 40 | 75 | 40 | **AIOX** (100) |
| `intent_capture` | Captura intent + restrições antes de executar? | 100 | 80 | 70 | 60 | 50 | 30 | 40 | 40 | 75 | 40 | **AIOX** (100) |
| `scope_negotiation` | Negocia escopo com user antes de waves? | 100 | 80 | 70 | 60 | 50 | 30 | 40 | 40 | 75 | 40 | **AIOX** (100) |
| `subquery_count` | Quebra query em N sub-queries paralelas? | 95 | 85 | 80 | 65 | 60 | 40 | 50 | 30 | 85 | 50 | **AIOX** (95) |
| `topic_taxonomy` | Aplica taxonomia de tópicos coerente? | 95 | 85 | 80 | 65 | 60 | 40 | 50 | 30 | 85 | 50 | **AIOX** (95) |
| `priority_ordering` | Ordena sub-queries por importância? | 95 | 85 | 80 | 65 | 60 | 40 | 50 | 30 | 85 | 50 | **AIOX** (95) |
| `prompts_versioned` | Prompts são artefato YAML versionado? | 95 | 75 | 70 | 60 | 60 | 40 | 45 | 35 | 95 | 45 | **AIOX** (95) |
| `prompt_audit_trail` | Cada prompt traceable para fase? | 95 | 75 | 70 | 60 | 60 | 40 | 45 | 35 | 95 | 45 | **AIOX** (95) |
| `prompt_reuse` | Templates reaproveitáveis entre runs? | 95 | 75 | 70 | 60 | 60 | 40 | 45 | 35 | 95 | 45 | **AIOX** (95) |

### Execucao (weight 15)

_Multi-wave search, deep-read, parallelism_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `wave_count_bounded` | Tem max_waves cap explícito? | 100 | 90 | 85 | 75 | 80 | 60 | 70 | 70 | 80 | 60 | **AIOX** (100) |
| `wave_state_tracking` | Persiste estado entre waves? | 95 | 90 | 85 | 75 | 80 | 60 | 70 | 70 | 80 | 60 | **AIOX** (95) |
| `saturation_detection` | Detecta quando waves não trazem novidade? | 95 | 90 | 85 | 75 | 80 | 60 | 70 | 70 | 80 | 60 | **AIOX** (95) |
| `full_content_fetch` | Lê conteúdo completo (não só snippet)? | 90 | 80 | 75 | 60 | 70 | 50 | 65 | 75 | 70 | 60 | **AIOX** (90) |
| `summarize_per_source` | Sumariza source by source? | 90 | 80 | 75 | 60 | 70 | 50 | 65 | 75 | 70 | 60 | **AIOX** (90) |
| `extract_quotes` | Extrai quotes literais para citação? | 90 | 80 | 75 | 60 | 70 | 50 | 65 | 75 | 70 | 60 | **AIOX** (90) |
| `parallel_spawn` | Spawna subagents em paralelo real? | 40 | 95 | 80 | 40 | 50 | 30 | 30 | 20 | 75 | 50 | **DeerFlow** (95) |
| `parallel_fetch` | Fetch de múltiplas sources em paralelo? | 40 | 90 | 80 | 40 | 50 | 30 | 30 | 20 | 75 | 50 | **DeerFlow** (90) |
| `concurrency_safe` | Trata race conditions entre subagents? | 40 | 90 | 80 | 40 | 50 | 30 | 30 | 20 | 75 | 50 | **DeerFlow** (90) |
| `inter_wave_compress` | Comprime contexto entre waves? | 100 | 70 | 65 | 70 | 60 | 40 | 50 | 50 | 60 | 45 | **AIOX** (100) |
| `redundancy_removal` | Remove duplicação entre waves? | 95 | 70 | 65 | 70 | 60 | 40 | 50 | 50 | 60 | 45 | **AIOX** (95) |
| `context_budget_aware` | Para wave se context cap próximo? | 95 | 70 | 65 | 70 | 60 | 40 | 50 | 50 | 60 | 45 | **AIOX** (95) |

### Multi-Agente (weight 8)

_True subagent orchestration vs single-loop_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `distinct_roles` | Define roles distintos (Researcher/Editor/etc)? | 85 | 90 | 80 | 30 | 40 | 25 | 25 | 20 | 85 | 65 | **DeerFlow** (90) |
| `handoff_explicit` | Handoff entre subagents tem contrato? | 85 | 90 | 80 | 30 | 40 | 25 | 25 | 20 | 85 | 65 | **DeerFlow** (90) |
| `persona_fidelity` | Subagent mantém persona definida? | 85 | 90 | 80 | 30 | 40 | 25 | 25 | 20 | 85 | 65 | **DeerFlow** (90) |
| `concurrent_execution` | Subagents executam concorrentemente? | 30 | 90 | 75 | 25 | 35 | 20 | 20 | 15 | 80 | 55 | **DeerFlow** (90) |
| `result_aggregation` | Aggrega outputs de subagents paralelos? | 30 | 90 | 75 | 25 | 35 | 20 | 20 | 15 | 80 | 55 | **DeerFlow** (90) |
| `failure_isolation` | Falha de um subagent não derruba pipeline? | 30 | 90 | 75 | 25 | 35 | 20 | 20 | 15 | 80 | 55 | **DeerFlow** (90) |

### Modelo (weight 12)

_Purpose-trained model vs prompt-engineered_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `research_dataset_train` | Modelo treinado em trajetórias de research? | 0 | 0 | 0 | 0 | 0 | 100 | 95 | 0 | 0 | 95 | **OpenR** (100) |
| `rl_emergent_behaviors` | Behaviors emergentes documentadas? | 0 | 0 | 0 | 0 | 0 | 100 | 100 | 0 | 0 | 95 | **OpenR** (100) |
| `benchmark_dominance` | Bate frontier models em research bench? | 0 | 0 | 0 | 0 | 0 | 100 | 95 | 0 | 0 | 80 | **OpenR** (100) |
| `byok_support` | Funciona com qualquer LLM provider? | 95 | 95 | 100 | 95 | 100 | 20 | 20 | 80 | 90 | 40 | **GPT-R** (100) |
| `provider_fallback` | Fallback entre providers se um cair? | 95 | 95 | 100 | 95 | 100 | 20 | 20 | 80 | 90 | 40 | **GPT-R** (100) |
| `cost_aware_routing` | Roteia entre LLMs por custo? | 95 | 95 | 100 | 95 | 100 | 20 | 20 | 80 | 90 | 40 | **GPT-R** (100) |
| `ollama_support` | Roda com Ollama local? | 60 | 85 | 90 | 80 | 100 | 80 | 90 | 70 | 80 | 85 | **LDR** (100) |
| `llamacpp_support` | Suporta llama.cpp inference? | 60 | 85 | 90 | 80 | 100 | 80 | 90 | 70 | 80 | 85 | **LDR** (100) |
| `hf_local_inference` | Roda HF model localmente? | 60 | 85 | 90 | 80 | 100 | 80 | 90 | 70 | 80 | 85 | **LDR** (100) |

### Memoria (weight 6)

_Cross-session persistence, confidence scores_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `persistent_memory` | Tem store persistente cross-session? | 25 | 95 | 30 | 20 | 80 | 10 | 10 | 10 | 40 | 20 | **DeerFlow** (95) |
| `fact_recall` | Faz recall de facts em runs futuros? | 25 | 95 | 30 | 20 | 80 | 10 | 10 | 10 | 40 | 20 | **DeerFlow** (95) |
| `cross_device_sync` | Sincroniza memória entre devices? | 25 | 100 | 30 | 20 | 80 | 10 | 10 | 10 | 40 | 20 | **DeerFlow** (100) |
| `confidence_tier` | Cada fact tem confidence tier? | 80 | 90 | 60 | 50 | 60 | 70 | 75 | 40 | 55 | 60 | **DeerFlow** (90) |
| `decay_over_time` | Confidence decai ao longo do tempo? | 80 | 90 | 60 | 50 | 60 | 70 | 75 | 40 | 55 | 60 | **DeerFlow** (90) |
| `source_credibility_propagate` | Credibilidade da source propaga ao fact? | 80 | 90 | 60 | 50 | 60 | 70 | 75 | 40 | 55 | 60 | **DeerFlow** (90) |

### Sandbox (weight 7)

_Docker code execution isolation_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `docker_isolated` | Code roda em Docker isolado? | 0 | 95 | 40 | 0 | 70 | 0 | 30 | 50 | 100 | 0 | **ARC** (100) |
| `language_support` | Suporta múltiplas linguagens (Python+Node+etc)? | 0 | 95 | 40 | 0 | 70 | 0 | 30 | 50 | 100 | 0 | **ARC** (100) |
| `stream_output` | Stream stdout/stderr durante exec? | 0 | 95 | 40 | 0 | 70 | 0 | 30 | 50 | 100 | 0 | **ARC** (100) |
| `egress_deny_default` | Network egress denied por default? | 0 | 70 | 20 | 0 | 60 | 0 | 20 | 25 | 100 | 0 | **ARC** (100) |
| `allowlist_configurable` | Allowlist de domínios configurável? | 0 | 70 | 20 | 0 | 60 | 0 | 20 | 25 | 100 | 0 | **ARC** (100) |
| `read_only_fs` | Container tem read-only base FS? | 0 | 70 | 20 | 0 | 60 | 0 | 20 | 25 | 95 | 0 | **ARC** (95) |

### Citacoes (weight 10)

_Citation verification, source credibility_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `claim_to_source` | Cada claim mapeado para source? | 100 | 60 | 75 | 60 | 70 | 65 | 65 | 50 | 75 | 55 | **AIOX** (100) |
| `hallucination_detect` | Detecta claim sem source? | 100 | 60 | 75 | 60 | 70 | 65 | 65 | 50 | 75 | 55 | **AIOX** (100) |
| `fix_loop_bounded` | Loop de correção tem cap? | 100 | 60 | 75 | 60 | 70 | 65 | 65 | 50 | 75 | 55 | **AIOX** (100) |
| `arxiv_integration` | Busca arXiv nativamente? | 30 | 40 | 50 | 35 | 100 | 60 | 50 | 35 | 70 | 55 | **LDR** (100) |
| `pubmed_integration` | Busca PubMed nativamente? | 30 | 40 | 50 | 35 | 100 | 60 | 50 | 35 | 70 | 55 | **LDR** (100) |
| `semantic_scholar_integration` | Busca Semantic Scholar nativamente? | 30 | 40 | 50 | 35 | 100 | 60 | 50 | 35 | 70 | 55 | **LDR** (100) |
| `credibility_scoring` | Atribui score de credibilidade a sources? | 85 | 65 | 70 | 55 | 80 | 60 | 70 | 45 | 65 | 55 | **AIOX** (85) |
| `source_type_classify` | Classifica official_docs vs blog vs forum? | 85 | 65 | 70 | 55 | 80 | 60 | 70 | 45 | 65 | 55 | **AIOX** (85) |
| `freshness_check` | Verifica frescor da source? | 85 | 65 | 70 | 55 | 80 | 60 | 70 | 45 | 65 | 55 | **AIOX** (85) |

### Saida (weight 7)

_Output formats (MD/PDF/DOCX/HTML/JSON)_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `markdown_output` | Gera Markdown? | 50 | 70 | 95 | 55 | 60 | 40 | 40 | 65 | 90 | 45 | **GPT-R** (95) |
| `pdf_export` | Exporta PDF? | 50 | 70 | 100 | 55 | 60 | 40 | 40 | 65 | 90 | 45 | **GPT-R** (100) |
| `docx_html_export` | Exporta DOCX e/ou HTML? | 50 | 70 | 95 | 55 | 60 | 40 | 40 | 65 | 90 | 45 | **GPT-R** (95) |
| `yaml_artifacts` | Produz artefatos YAML estruturados? | 95 | 75 | 80 | 60 | 65 | 45 | 45 | 70 | 90 | 50 | **AIOX** (95) |
| `json_artifacts` | Produz JSON canônico? | 95 | 75 | 80 | 60 | 65 | 45 | 45 | 70 | 90 | 50 | **AIOX** (95) |
| `graph_artifacts` | Produz graph (nodes/edges) consumível? | 95 | 75 | 80 | 60 | 65 | 45 | 45 | 70 | 90 | 50 | **AIOX** (95) |

### Observabilidade (weight 5)

_Logs, dashboards, eval logs public_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `per_phase_logs` | Log estruturado por fase? | 100 | 70 | 85 | 75 | 65 | 90 | 80 | 55 | 70 | 65 | **AIOX** (100) |
| `event_jsonl` | Eventos como JSONL auditáveis? | 100 | 70 | 85 | 75 | 65 | 90 | 80 | 55 | 70 | 65 | **AIOX** (100) |
| `incremental_logs` | Log incremental (não post-hoc)? | 100 | 70 | 85 | 75 | 65 | 90 | 80 | 55 | 70 | 65 | **AIOX** (100) |
| `benchmark_published` | Score público em leaderboard? | 20 | 50 | 55 | 95 | 95 | 100 | 75 | 30 | 50 | 75 | **OpenR** (100) |
| `eval_artifacts_public` | Artefatos de eval publicamente acessíveis? | 20 | 50 | 55 | 70 | 80 | 100 | 75 | 30 | 50 | 75 | **OpenR** (100) |
| `reproducible_eval` | Eval reproduzível pela community? | 20 | 50 | 55 | 70 | 80 | 100 | 75 | 30 | 50 | 75 | **OpenR** (100) |
| `artifact_browser` | UI para navegar artefatos? | 90 | 85 | 70 | 65 | 60 | 70 | 30 | 85 | 50 | 40 | **AIOX** (90) |
| `live_run_view` | Visualização de run em tempo real? | 90 | 85 | 70 | 65 | 60 | 70 | 30 | 85 | 50 | 40 | **AIOX** (90) |
| `cross_run_compare` | Compara runs entre si? | 90 | 85 | 70 | 65 | 60 | 70 | 30 | 85 | 50 | 40 | **AIOX** (90) |

### Distribuicao (weight 5)

_PyPI, Docker Hub, marketplaces_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `package_published` | Publicado em PyPI/npm? | 0 | 50 | 100 | 60 | 95 | 40 | 30 | 70 | 45 | 50 | **GPT-R** (100) |
| `semver_releases` | Tem semver disciplinado? | 10 | 50 | 100 | 60 | 95 | 40 | 30 | 70 | 45 | 50 | **GPT-R** (100) |
| `install_one_command` | Instala com 1 comando? | 10 | 50 | 100 | 60 | 95 | 40 | 30 | 70 | 45 | 50 | **GPT-R** (100) |
| `docker_image_published` | Image em Docker Hub? | 0 | 90 | 100 | 30 | 100 | 20 | 30 | 85 | 25 | 30 | **GPT-R** (100) |
| `multi_arch_support` | amd64 + arm64? | 5 | 90 | 95 | 30 | 100 | 20 | 30 | 85 | 25 | 30 | **LDR** (100) |
| `compose_examples` | docker-compose example pronto? | 5 | 90 | 95 | 30 | 100 | 20 | 30 | 85 | 25 | 30 | **LDR** (100) |
| `claude_skill_listed` | Listada em skills.sh ou equivalente? | 20 | 30 | 100 | 25 | 25 | 30 | 20 | 25 | 20 | 25 | **GPT-R** (100) |
| `langchain_hub_listed` | Listada em LangChain Hub? | 20 | 30 | 95 | 25 | 25 | 30 | 20 | 25 | 20 | 25 | **GPT-R** (95) |
| `install_guide_video` | Tem vídeo de install? | 20 | 30 | 95 | 25 | 25 | 30 | 20 | 25 | 20 | 25 | **GPT-R** (95) |

### Licenca (weight 5)

_MIT/Apache/proprietary_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `osi_approved_license` | License é OSI-approved? | 30 | 100 | 100 | 100 | 100 | 100 | 100 | 0 | 100 | 100 | **DeerFlow** (100) |
| `contribution_friendly` | Aceita PR community sem CLA pesada? | 30 | 100 | 100 | 100 | 100 | 100 | 100 | 30 | 100 | 100 | **DeerFlow** (100) |
| `forkable_no_restrictions` | Pode forkear sem fricção? | 30 | 100 | 100 | 100 | 100 | 100 | 100 | 20 | 100 | 100 | **DeerFlow** (100) |
| `commercial_use_allowed` | Permite uso comercial? | 90 | 100 | 100 | 100 | 100 | 100 | 100 | 50 | 100 | 100 | **DeerFlow** (100) |
| `royalty_free` | Zero royalties? | 90 | 100 | 100 | 100 | 100 | 100 | 100 | 50 | 100 | 100 | **DeerFlow** (100) |
| `saas_competitor_clause` | Sem cláusula anti-SaaS-competitor? | 90 | 100 | 100 | 100 | 100 | 100 | 100 | 50 | 100 | 100 | **DeerFlow** (100) |

### Governance (weight 5)

_Quality gates, guardrails, VETO conditions_

| Microdim | Question |AIOX | DeerFlow | GPT-R | LC-ODR | LDR | OpenR | DeepR | Jina | ARC | Tongyi | Best |
|---|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `coverage_gate_veto` | Tem gate de coverage com VETO halt? | 100 | 65 | 60 | 55 | 70 | 50 | 55 | 60 | 90 | 50 | **AIOX** (100) |
| `citation_gate_veto` | Tem gate de citation com VETO halt? | 100 | 65 | 60 | 55 | 70 | 50 | 55 | 60 | 90 | 50 | **AIOX** (100) |
| `gates_bounded` | Gates têm max attempts cap? | 100 | 65 | 60 | 55 | 70 | 50 | 55 | 60 | 90 | 50 | **AIOX** (100) |
| `per_phase_log_write` | Escreve log a cada phase (não post-hoc)? | 100 | 50 | 55 | 50 | 55 | 60 | 55 | 45 | 70 | 50 | **AIOX** (100) |
| `crash_recovery_log` | Log persiste mesmo em crash? | 100 | 50 | 55 | 50 | 55 | 60 | 55 | 45 | 70 | 50 | **AIOX** (100) |
| `learning_promotion` | Path para promover learnings em heurísticas? | 100 | 50 | 55 | 50 | 55 | 60 | 55 | 45 | 70 | 50 | **AIOX** (100) |

## Duels — All 45 Pairs

| Pair | Verdict | A wins | B wins | Ties |
|---|---|---:|---:|---:|
| AIOX vs DeerFlow | DeerFlow (ByteDance) vence AIOX Research Ecosystem em 51 de 102 dimensões | 34 | 51 | 17 |
| AIOX vs GPT-R | GPT-Researcher vence AIOX Research Ecosystem em 48 de 102 dimensões | 42 | 48 | 12 |
| AIOX vs LC-ODR | AIOX Research Ecosystem vence LangChain Open DR em 45 de 102 dimensões | 45 | 24 | 33 |
| AIOX vs LDR | AIOX Research Ecosystem vence Local Deep Research em 42 de 102 dimensões | 42 | 39 | 21 |
| AIOX vs OpenR | AIOX Research Ecosystem vence OpenResearcher 30B em 63 de 102 dimensões | 63 | 27 | 12 |
| AIOX vs DeepR | AIOX Research Ecosystem vence DeepResearcher 7B RL em 60 de 102 dimensões | 60 | 30 | 12 |
| AIOX vs Jina | AIOX Research Ecosystem vence Jina node-DR em 59 de 102 dimensões | 59 | 27 | 16 |
| AIOX vs ARC | AutoResearchClaw vence AIOX Research Ecosystem em 42 de 102 dimensões | 39 | 42 | 21 |
| AIOX vs Tongyi | AIOX Research Ecosystem vence Tongyi DeepResearch em 51 de 102 dimensões | 51 | 30 | 21 |
| DeerFlow vs GPT-R | DeerFlow (ByteDance) vence GPT-Researcher em 27 de 102 dimensões | 27 | 25 | 50 |
| DeerFlow vs LC-ODR | DeerFlow (ByteDance) vence LangChain Open DR em 60 de 102 dimensões | 60 | 9 | 33 |
| DeerFlow vs LDR | DeerFlow (ByteDance) vence Local Deep Research em 54 de 102 dimensões | 54 | 21 | 27 |
| DeerFlow vs OpenR | DeerFlow (ByteDance) vence OpenResearcher 30B em 66 de 102 dimensões | 66 | 15 | 21 |
| DeerFlow vs DeepR | DeerFlow (ByteDance) vence DeepResearcher 7B RL em 69 de 102 dimensões | 69 | 12 | 21 |
| DeerFlow vs Jina | DeerFlow (ByteDance) vence Jina node-DR em 60 de 102 dimensões | 60 | 6 | 36 |
| DeerFlow vs ARC | DeerFlow (ByteDance) vence AutoResearchClaw em 36 de 102 dimensões | 36 | 24 | 42 |
| DeerFlow vs Tongyi | DeerFlow (ByteDance) vence Tongyi DeepResearch em 66 de 102 dimensões | 66 | 9 | 27 |
| GPT-R vs LC-ODR | GPT-Researcher vence LangChain Open DR em 72 de 102 dimensões | 72 | 3 | 27 |
| GPT-R vs LDR | GPT-Researcher vence Local Deep Research em 42 de 102 dimensões | 42 | 24 | 36 |
| GPT-R vs OpenR | GPT-Researcher vence OpenResearcher 30B em 75 de 102 dimensões | 75 | 12 | 15 |
| GPT-R vs DeepR | GPT-Researcher vence DeepResearcher 7B RL em 66 de 102 dimensões | 66 | 9 | 27 |
| GPT-R vs Jina | GPT-Researcher vence Jina node-DR em 81 de 102 dimensões | 81 | 6 | 15 |
| GPT-R vs ARC | GPT-Researcher vence AutoResearchClaw em 31 de 102 dimensões | 31 | 24 | 47 |
| GPT-R vs Tongyi | GPT-Researcher vence Tongyi DeepResearch em 78 de 102 dimensões | 78 | 6 | 18 |
| LC-ODR vs LDR | Local Deep Research vence LangChain Open DR em 47 de 102 dimensões | 15 | 47 | 40 |
| LC-ODR vs OpenR | LangChain Open DR vence OpenResearcher 30B em 48 de 102 dimensões | 48 | 17 | 37 |
| LC-ODR vs DeepR | LangChain Open DR vence DeepResearcher 7B RL em 43 de 102 dimensões | 43 | 21 | 38 |
| LC-ODR vs Jina | LangChain Open DR vence Jina node-DR em 54 de 102 dimensões | 54 | 30 | 18 |
| LC-ODR vs ARC | AutoResearchClaw vence LangChain Open DR em 51 de 102 dimensões | 21 | 51 | 30 |
| LC-ODR vs Tongyi | LangChain Open DR vence Tongyi DeepResearch em 43 de 102 dimensões | 43 | 18 | 41 |
| LDR vs OpenR | Local Deep Research vence OpenResearcher 30B em 69 de 102 dimensões | 69 | 14 | 19 |
| LDR vs DeepR | Local Deep Research vence DeepResearcher 7B RL em 70 de 102 dimensões | 70 | 9 | 23 |
| LDR vs Jina | Local Deep Research vence Jina node-DR em 75 de 102 dimensões | 75 | 9 | 18 |
| LDR vs ARC | AutoResearchClaw vence Local Deep Research em 36 de 102 dimensões | 33 | 36 | 33 |
| LDR vs Tongyi | Local Deep Research vence Tongyi DeepResearch em 67 de 102 dimensões | 67 | 9 | 26 |
| OpenR vs DeepR | DeepResearcher 7B RL vence OpenResearcher 30B em 30 de 102 dimensões | 21 | 30 | 51 |
| OpenR vs Jina | Jina node-DR vence OpenResearcher 30B em 45 de 102 dimensões | 39 | 45 | 18 |
| OpenR vs ARC | AutoResearchClaw vence OpenResearcher 30B em 63 de 102 dimensões | 18 | 63 | 21 |
| OpenR vs Tongyi | Tongyi DeepResearch vence OpenResearcher 30B em 30 de 102 dimensões | 19 | 30 | 53 |
| DeepR vs Jina | DeepResearcher 7B RL vence Jina node-DR em 42 de 102 dimensões | 42 | 30 | 30 |
| DeepR vs ARC | AutoResearchClaw vence DeepResearcher 7B RL em 66 de 102 dimensões | 15 | 66 | 21 |
| DeepR vs Tongyi | Tongyi DeepResearch vence DeepResearcher 7B RL em 24 de 102 dimensões | 22 | 24 | 56 |
| Jina vs ARC | AutoResearchClaw vence Jina node-DR em 75 de 102 dimensões | 15 | 75 | 12 |
| Jina vs Tongyi | Tongyi DeepResearch vence Jina node-DR em 45 de 102 dimensões | 39 | 45 | 18 |
| ARC vs Tongyi | AutoResearchClaw vence Tongyi DeepResearch em 69 de 102 dimensões | 69 | 6 | 27 |
