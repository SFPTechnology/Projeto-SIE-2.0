# Full Comparison — AIOX vs Each Player (Head-to-Head)

> 9 head-to-head comparisons baseadas em 102 microdimensões. Cada player mostrado lado-a-lado com AIOX em todas as dims, com winner indicado.

## Quick Index

1. [AIOX vs DeerFlow (ByteDance)](#aiox-vs-deerflow)
2. [AIOX vs GPT-Researcher](#aiox-vs-gpt-researcher)
3. [AIOX vs LangChain Open DR](#aiox-vs-langchain-odr)
4. [AIOX vs Local Deep Research](#aiox-vs-local-dr)
5. [AIOX vs OpenResearcher 30B](#aiox-vs-openresearcher)
6. [AIOX vs DeepResearcher 7B RL](#aiox-vs-deepresearcher)
7. [AIOX vs Jina node-DR](#aiox-vs-jina-ndr)
8. [AIOX vs AutoResearchClaw](#aiox-vs-autoresearchclaw)
9. [AIOX vs Tongyi DeepResearch](#aiox-vs-tongyi-dr)

## AIOX vs DeerFlow (ByteDance)

**Total scores:** AIOX `60.25` vs DeerFlow (ByteDance) `72.05` (delta -11.80)

**Verdict:** DeerFlow (ByteDance) vence AIOX Research em 51 de 102 dimensões

### AIOX wins (34 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `ambiguity_detect` | 100 | 80 | +20 |
| `intent_capture` | 100 | 80 | +20 |
| `scope_negotiation` | 100 | 80 | +20 |
| `subquery_count` | 95 | 85 | +10 |
| `topic_taxonomy` | 95 | 85 | +10 |
| `priority_ordering` | 95 | 85 | +10 |
| `prompts_versioned` | 95 | 75 | +20 |
| `prompt_audit_trail` | 95 | 75 | +20 |
| `prompt_reuse` | 95 | 75 | +20 |
| `wave_count_bounded` | 100 | 90 | +10 |
| `full_content_fetch` | 90 | 80 | +10 |
| `summarize_per_source` | 90 | 80 | +10 |
| `extract_quotes` | 90 | 80 | +10 |
| `inter_wave_compress` | 100 | 70 | +30 |
| `redundancy_removal` | 95 | 70 | +25 |
| `context_budget_aware` | 95 | 70 | +25 |
| `claim_to_source` | 100 | 60 | +40 |
| `hallucination_detect` | 100 | 60 | +40 |
| `fix_loop_bounded` | 100 | 60 | +40 |
| `credibility_scoring` | 85 | 65 | +20 |
| _(+14 more)_ | | | |

### DeerFlow (ByteDance) wins (51 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 90 | -15 |
| `api_entry` | 75 | 90 | -15 |
| `ui_entry` | 75 | 90 | -15 |
| `rest_endpoints` | 35 | 80 | -45 |
| `sse_streaming` | 35 | 80 | -45 |
| `auth_layer` | 35 | 80 | -45 |
| `parallel_spawn` | 40 | 95 | -55 |
| `parallel_fetch` | 40 | 90 | -50 |
| `concurrency_safe` | 40 | 90 | -50 |
| `concurrent_execution` | 30 | 90 | -60 |
| `result_aggregation` | 30 | 90 | -60 |
| `failure_isolation` | 30 | 90 | -60 |
| `ollama_support` | 60 | 85 | -25 |
| `llamacpp_support` | 60 | 85 | -25 |
| `hf_local_inference` | 60 | 85 | -25 |
| `persistent_memory` | 25 | 95 | -70 |
| `fact_recall` | 25 | 95 | -70 |
| `cross_device_sync` | 25 | 100 | -75 |
| `confidence_tier` | 80 | 90 | -10 |
| `decay_over_time` | 80 | 90 | -10 |
| _(+31 more)_ | | | |

### Strategic Implication

DeerFlow (ByteDance) vence no aggregate. AIOX deve **absorber** padrões onde DeerFlow (ByteDance) domina (especialmente dimensões em **Entrada**) sem perder vantagens em **Planejamento**.

---

## AIOX vs GPT-Researcher

**Total scores:** AIOX `60.25` vs GPT-Researcher `69.65` (delta -9.40)

**Verdict:** GPT-Researcher vence AIOX Research em 48 de 102 dimensões

### AIOX wins (42 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `ambiguity_detect` | 100 | 70 | +30 |
| `intent_capture` | 100 | 70 | +30 |
| `scope_negotiation` | 100 | 70 | +30 |
| `subquery_count` | 95 | 80 | +15 |
| `topic_taxonomy` | 95 | 80 | +15 |
| `priority_ordering` | 95 | 80 | +15 |
| `prompts_versioned` | 95 | 70 | +25 |
| `prompt_audit_trail` | 95 | 70 | +25 |
| `prompt_reuse` | 95 | 70 | +25 |
| `wave_count_bounded` | 100 | 85 | +15 |
| `wave_state_tracking` | 95 | 85 | +10 |
| `saturation_detection` | 95 | 85 | +10 |
| `full_content_fetch` | 90 | 75 | +15 |
| `summarize_per_source` | 90 | 75 | +15 |
| `extract_quotes` | 90 | 75 | +15 |
| `inter_wave_compress` | 100 | 65 | +35 |
| `redundancy_removal` | 95 | 65 | +30 |
| `context_budget_aware` | 95 | 65 | +30 |
| `confidence_tier` | 80 | 60 | +20 |
| `decay_over_time` | 80 | 60 | +20 |
| _(+22 more)_ | | | |

### GPT-Researcher wins (48 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 95 | -20 |
| `api_entry` | 75 | 95 | -20 |
| `ui_entry` | 75 | 95 | -20 |
| `mcp_server_exposed` | 0 | 100 | -100 |
| `mcp_tools_count` | 0 | 95 | -95 |
| `mcp_transport_support` | 0 | 95 | -95 |
| `rest_endpoints` | 35 | 95 | -60 |
| `sse_streaming` | 35 | 95 | -60 |
| `auth_layer` | 35 | 95 | -60 |
| `parallel_spawn` | 40 | 80 | -40 |
| `parallel_fetch` | 40 | 80 | -40 |
| `concurrency_safe` | 40 | 80 | -40 |
| `concurrent_execution` | 30 | 75 | -45 |
| `result_aggregation` | 30 | 75 | -45 |
| `failure_isolation` | 30 | 75 | -45 |
| `ollama_support` | 60 | 90 | -30 |
| `llamacpp_support` | 60 | 90 | -30 |
| `hf_local_inference` | 60 | 90 | -30 |
| `docker_isolated` | 0 | 40 | -40 |
| `language_support` | 0 | 40 | -40 |
| _(+28 more)_ | | | |

### Strategic Implication

GPT-Researcher vence no aggregate. AIOX deve **absorber** padrões onde GPT-Researcher domina (especialmente dimensões em **Entrada**) sem perder vantagens em **Planejamento**.

---

## AIOX vs LangChain Open DR

**Total scores:** AIOX `60.25` vs LangChain Open DR `51.7` (delta +8.55)

**Verdict:** AIOX Research vence LangChain Open DR em 45 de 102 dimensões

### AIOX wins (45 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `ambiguity_detect` | 100 | 60 | +40 |
| `intent_capture` | 100 | 60 | +40 |
| `scope_negotiation` | 100 | 60 | +40 |
| `subquery_count` | 95 | 65 | +30 |
| `topic_taxonomy` | 95 | 65 | +30 |
| `priority_ordering` | 95 | 65 | +30 |
| `prompts_versioned` | 95 | 60 | +35 |
| `prompt_audit_trail` | 95 | 60 | +35 |
| `prompt_reuse` | 95 | 60 | +35 |
| `wave_count_bounded` | 100 | 75 | +25 |
| `wave_state_tracking` | 95 | 75 | +20 |
| `saturation_detection` | 95 | 75 | +20 |
| `full_content_fetch` | 90 | 60 | +30 |
| `summarize_per_source` | 90 | 60 | +30 |
| `extract_quotes` | 90 | 60 | +30 |
| `inter_wave_compress` | 100 | 70 | +30 |
| `redundancy_removal` | 95 | 70 | +25 |
| `context_budget_aware` | 95 | 70 | +25 |
| `distinct_roles` | 85 | 30 | +55 |
| `handoff_explicit` | 85 | 30 | +55 |
| _(+25 more)_ | | | |

### LangChain Open DR wins (24 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `mcp_server_exposed` | 0 | 100 | -100 |
| `mcp_tools_count` | 0 | 100 | -100 |
| `mcp_transport_support` | 0 | 100 | -100 |
| `rest_endpoints` | 35 | 70 | -35 |
| `sse_streaming` | 35 | 70 | -35 |
| `auth_layer` | 35 | 70 | -35 |
| `ollama_support` | 60 | 80 | -20 |
| `llamacpp_support` | 60 | 80 | -20 |
| `hf_local_inference` | 60 | 80 | -20 |
| `benchmark_published` | 20 | 95 | -75 |
| `eval_artifacts_public` | 20 | 70 | -50 |
| `reproducible_eval` | 20 | 70 | -50 |
| `package_published` | 0 | 60 | -60 |
| `semver_releases` | 10 | 60 | -50 |
| `install_one_command` | 10 | 60 | -50 |
| `docker_image_published` | 0 | 30 | -30 |
| `multi_arch_support` | 5 | 30 | -25 |
| `compose_examples` | 5 | 30 | -25 |
| `osi_approved_license` | 30 | 100 | -70 |
| `contribution_friendly` | 30 | 100 | -70 |
| _(+4 more)_ | | | |

### Strategic Implication

AIOX vence no aggregate. Manter vantagens em **Planejamento**; reduzir surface de ataque em **Entrada**.

---

## AIOX vs Local Deep Research

**Total scores:** AIOX `60.25` vs Local Deep Research `63.9` (delta -3.65)

**Verdict:** AIOX Research vence Local Deep Research em 42 de 102 dimensões

### AIOX wins (42 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `ambiguity_detect` | 100 | 50 | +50 |
| `intent_capture` | 100 | 50 | +50 |
| `scope_negotiation` | 100 | 50 | +50 |
| `subquery_count` | 95 | 60 | +35 |
| `topic_taxonomy` | 95 | 60 | +35 |
| `priority_ordering` | 95 | 60 | +35 |
| `prompts_versioned` | 95 | 60 | +35 |
| `prompt_audit_trail` | 95 | 60 | +35 |
| `prompt_reuse` | 95 | 60 | +35 |
| `wave_count_bounded` | 100 | 80 | +20 |
| `wave_state_tracking` | 95 | 80 | +15 |
| `saturation_detection` | 95 | 80 | +15 |
| `full_content_fetch` | 90 | 70 | +20 |
| `summarize_per_source` | 90 | 70 | +20 |
| `extract_quotes` | 90 | 70 | +20 |
| `inter_wave_compress` | 100 | 60 | +40 |
| `redundancy_removal` | 95 | 60 | +35 |
| `context_budget_aware` | 95 | 60 | +35 |
| `distinct_roles` | 85 | 40 | +45 |
| `handoff_explicit` | 85 | 40 | +45 |
| _(+22 more)_ | | | |

### Local Deep Research wins (39 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `rest_endpoints` | 35 | 60 | -25 |
| `sse_streaming` | 35 | 60 | -25 |
| `auth_layer` | 35 | 60 | -25 |
| `parallel_spawn` | 40 | 50 | -10 |
| `parallel_fetch` | 40 | 50 | -10 |
| `concurrency_safe` | 40 | 50 | -10 |
| `ollama_support` | 60 | 100 | -40 |
| `llamacpp_support` | 60 | 100 | -40 |
| `hf_local_inference` | 60 | 100 | -40 |
| `persistent_memory` | 25 | 80 | -55 |
| `fact_recall` | 25 | 80 | -55 |
| `cross_device_sync` | 25 | 80 | -55 |
| `docker_isolated` | 0 | 70 | -70 |
| `language_support` | 0 | 70 | -70 |
| `stream_output` | 0 | 70 | -70 |
| `egress_deny_default` | 0 | 60 | -60 |
| `allowlist_configurable` | 0 | 60 | -60 |
| `read_only_fs` | 0 | 60 | -60 |
| `arxiv_integration` | 30 | 100 | -70 |
| `pubmed_integration` | 30 | 100 | -70 |
| _(+19 more)_ | | | |

### Strategic Implication

Local Deep Research vence no aggregate. AIOX deve **absorber** padrões onde Local Deep Research domina (especialmente dimensões em **Execucao, Entrada**) sem perder vantagens em **Planejamento**.

---

## AIOX vs OpenResearcher 30B

**Total scores:** AIOX `60.25` vs OpenResearcher 30B `48.2` (delta +12.05)

**Verdict:** AIOX Research vence OpenResearcher 30B em 63 de 102 dimensões

### AIOX wins (63 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 50 | +25 |
| `api_entry` | 75 | 50 | +25 |
| `ui_entry` | 75 | 50 | +25 |
| `ambiguity_detect` | 100 | 30 | +70 |
| `intent_capture` | 100 | 30 | +70 |
| `scope_negotiation` | 100 | 30 | +70 |
| `subquery_count` | 95 | 40 | +55 |
| `topic_taxonomy` | 95 | 40 | +55 |
| `priority_ordering` | 95 | 40 | +55 |
| `prompts_versioned` | 95 | 40 | +55 |
| `prompt_audit_trail` | 95 | 40 | +55 |
| `prompt_reuse` | 95 | 40 | +55 |
| `wave_count_bounded` | 100 | 60 | +40 |
| `wave_state_tracking` | 95 | 60 | +35 |
| `saturation_detection` | 95 | 60 | +35 |
| `full_content_fetch` | 90 | 50 | +40 |
| `summarize_per_source` | 90 | 50 | +40 |
| `extract_quotes` | 90 | 50 | +40 |
| `parallel_spawn` | 40 | 30 | +10 |
| `parallel_fetch` | 40 | 30 | +10 |
| _(+43 more)_ | | | |

### OpenResearcher 30B wins (27 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `research_dataset_train` | 0 | 100 | -100 |
| `rl_emergent_behaviors` | 0 | 100 | -100 |
| `benchmark_dominance` | 0 | 100 | -100 |
| `ollama_support` | 60 | 80 | -20 |
| `llamacpp_support` | 60 | 80 | -20 |
| `hf_local_inference` | 60 | 80 | -20 |
| `arxiv_integration` | 30 | 60 | -30 |
| `pubmed_integration` | 30 | 60 | -30 |
| `semantic_scholar_integration` | 30 | 60 | -30 |
| `benchmark_published` | 20 | 100 | -80 |
| `eval_artifacts_public` | 20 | 100 | -80 |
| `reproducible_eval` | 20 | 100 | -80 |
| `package_published` | 0 | 40 | -40 |
| `semver_releases` | 10 | 40 | -30 |
| `install_one_command` | 10 | 40 | -30 |
| `docker_image_published` | 0 | 20 | -20 |
| `multi_arch_support` | 5 | 20 | -15 |
| `compose_examples` | 5 | 20 | -15 |
| `claude_skill_listed` | 20 | 30 | -10 |
| `langchain_hub_listed` | 20 | 30 | -10 |
| _(+7 more)_ | | | |

### Strategic Implication

AIOX vence no aggregate. Manter vantagens em **Planejamento, Entrada**; reduzir surface de ataque em **Modelo**.

---

## AIOX vs DeepResearcher 7B RL

**Total scores:** AIOX `60.25` vs DeepResearcher 7B RL `50.95` (delta +9.30)

**Verdict:** AIOX Research vence DeepResearcher 7B RL em 60 de 102 dimensões

### AIOX wins (60 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 40 | +35 |
| `api_entry` | 75 | 40 | +35 |
| `ui_entry` | 75 | 40 | +35 |
| `ambiguity_detect` | 100 | 40 | +60 |
| `intent_capture` | 100 | 40 | +60 |
| `scope_negotiation` | 100 | 40 | +60 |
| `subquery_count` | 95 | 50 | +45 |
| `topic_taxonomy` | 95 | 50 | +45 |
| `priority_ordering` | 95 | 50 | +45 |
| `prompts_versioned` | 95 | 45 | +50 |
| `prompt_audit_trail` | 95 | 45 | +50 |
| `prompt_reuse` | 95 | 45 | +50 |
| `wave_count_bounded` | 100 | 70 | +30 |
| `wave_state_tracking` | 95 | 70 | +25 |
| `saturation_detection` | 95 | 70 | +25 |
| `full_content_fetch` | 90 | 65 | +25 |
| `summarize_per_source` | 90 | 65 | +25 |
| `extract_quotes` | 90 | 65 | +25 |
| `parallel_spawn` | 40 | 30 | +10 |
| `parallel_fetch` | 40 | 30 | +10 |
| _(+40 more)_ | | | |

### DeepResearcher 7B RL wins (30 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `research_dataset_train` | 0 | 95 | -95 |
| `rl_emergent_behaviors` | 0 | 100 | -100 |
| `benchmark_dominance` | 0 | 95 | -95 |
| `ollama_support` | 60 | 90 | -30 |
| `llamacpp_support` | 60 | 90 | -30 |
| `hf_local_inference` | 60 | 90 | -30 |
| `docker_isolated` | 0 | 30 | -30 |
| `language_support` | 0 | 30 | -30 |
| `stream_output` | 0 | 30 | -30 |
| `egress_deny_default` | 0 | 20 | -20 |
| `allowlist_configurable` | 0 | 20 | -20 |
| `read_only_fs` | 0 | 20 | -20 |
| `arxiv_integration` | 30 | 50 | -20 |
| `pubmed_integration` | 30 | 50 | -20 |
| `semantic_scholar_integration` | 30 | 50 | -20 |
| `benchmark_published` | 20 | 75 | -55 |
| `eval_artifacts_public` | 20 | 75 | -55 |
| `reproducible_eval` | 20 | 75 | -55 |
| `package_published` | 0 | 30 | -30 |
| `semver_releases` | 10 | 30 | -20 |
| _(+10 more)_ | | | |

### Strategic Implication

AIOX vence no aggregate. Manter vantagens em **Planejamento, Entrada**; reduzir surface de ataque em **Modelo**.

---

## AIOX vs Jina node-DR

**Total scores:** AIOX `60.25` vs Jina node-DR `44.5` (delta +15.75)

**Verdict:** AIOX Research vence Jina node-DR em 59 de 102 dimensões

### AIOX wins (59 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `ambiguity_detect` | 100 | 40 | +60 |
| `intent_capture` | 100 | 40 | +60 |
| `scope_negotiation` | 100 | 40 | +60 |
| `subquery_count` | 95 | 30 | +65 |
| `topic_taxonomy` | 95 | 30 | +65 |
| `priority_ordering` | 95 | 30 | +65 |
| `prompts_versioned` | 95 | 35 | +60 |
| `prompt_audit_trail` | 95 | 35 | +60 |
| `prompt_reuse` | 95 | 35 | +60 |
| `wave_count_bounded` | 100 | 70 | +30 |
| `wave_state_tracking` | 95 | 70 | +25 |
| `saturation_detection` | 95 | 70 | +25 |
| `full_content_fetch` | 90 | 75 | +15 |
| `summarize_per_source` | 90 | 75 | +15 |
| `extract_quotes` | 90 | 75 | +15 |
| `parallel_spawn` | 40 | 20 | +20 |
| `parallel_fetch` | 40 | 20 | +20 |
| `concurrency_safe` | 40 | 20 | +20 |
| `inter_wave_compress` | 100 | 50 | +50 |
| `redundancy_removal` | 95 | 50 | +45 |
| _(+39 more)_ | | | |

### Jina node-DR wins (27 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 85 | -10 |
| `api_entry` | 75 | 85 | -10 |
| `ui_entry` | 75 | 85 | -10 |
| `rest_endpoints` | 35 | 95 | -60 |
| `sse_streaming` | 35 | 95 | -60 |
| `auth_layer` | 35 | 95 | -60 |
| `ollama_support` | 60 | 70 | -10 |
| `llamacpp_support` | 60 | 70 | -10 |
| `hf_local_inference` | 60 | 70 | -10 |
| `docker_isolated` | 0 | 50 | -50 |
| `language_support` | 0 | 50 | -50 |
| `stream_output` | 0 | 50 | -50 |
| `egress_deny_default` | 0 | 25 | -25 |
| `allowlist_configurable` | 0 | 25 | -25 |
| `read_only_fs` | 0 | 25 | -25 |
| `markdown_output` | 50 | 65 | -15 |
| `pdf_export` | 50 | 65 | -15 |
| `docx_html_export` | 50 | 65 | -15 |
| `benchmark_published` | 20 | 30 | -10 |
| `eval_artifacts_public` | 20 | 30 | -10 |
| _(+7 more)_ | | | |

### Strategic Implication

AIOX vence no aggregate. Manter vantagens em **Planejamento**; reduzir surface de ataque em **Entrada**.

---

## AIOX vs AutoResearchClaw

**Total scores:** AIOX `60.25` vs AutoResearchClaw `69.65` (delta -9.40)

**Verdict:** AutoResearchClaw vence AIOX Research em 42 de 102 dimensões

### AIOX wins (39 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 60 | +15 |
| `api_entry` | 75 | 60 | +15 |
| `ui_entry` | 75 | 60 | +15 |
| `ambiguity_detect` | 100 | 75 | +25 |
| `intent_capture` | 100 | 75 | +25 |
| `scope_negotiation` | 100 | 75 | +25 |
| `subquery_count` | 95 | 85 | +10 |
| `topic_taxonomy` | 95 | 85 | +10 |
| `priority_ordering` | 95 | 85 | +10 |
| `wave_count_bounded` | 100 | 80 | +20 |
| `wave_state_tracking` | 95 | 80 | +15 |
| `saturation_detection` | 95 | 80 | +15 |
| `full_content_fetch` | 90 | 70 | +20 |
| `summarize_per_source` | 90 | 70 | +20 |
| `extract_quotes` | 90 | 70 | +20 |
| `inter_wave_compress` | 100 | 60 | +40 |
| `redundancy_removal` | 95 | 60 | +35 |
| `context_budget_aware` | 95 | 60 | +35 |
| `confidence_tier` | 80 | 55 | +25 |
| `decay_over_time` | 80 | 55 | +25 |
| _(+19 more)_ | | | |

### AutoResearchClaw wins (42 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `rest_endpoints` | 35 | 50 | -15 |
| `sse_streaming` | 35 | 50 | -15 |
| `auth_layer` | 35 | 50 | -15 |
| `parallel_spawn` | 40 | 75 | -35 |
| `parallel_fetch` | 40 | 75 | -35 |
| `concurrency_safe` | 40 | 75 | -35 |
| `concurrent_execution` | 30 | 80 | -50 |
| `result_aggregation` | 30 | 80 | -50 |
| `failure_isolation` | 30 | 80 | -50 |
| `ollama_support` | 60 | 80 | -20 |
| `llamacpp_support` | 60 | 80 | -20 |
| `hf_local_inference` | 60 | 80 | -20 |
| `persistent_memory` | 25 | 40 | -15 |
| `fact_recall` | 25 | 40 | -15 |
| `cross_device_sync` | 25 | 40 | -15 |
| `docker_isolated` | 0 | 100 | -100 |
| `language_support` | 0 | 100 | -100 |
| `stream_output` | 0 | 100 | -100 |
| `egress_deny_default` | 0 | 100 | -100 |
| `allowlist_configurable` | 0 | 100 | -100 |
| _(+22 more)_ | | | |

### Strategic Implication

AutoResearchClaw vence no aggregate. AIOX deve **absorber** padrões onde AutoResearchClaw domina (especialmente dimensões em **Execucao, Entrada**) sem perder vantagens em **Planejamento, Entrada**.

---

## AIOX vs Tongyi DeepResearch

**Total scores:** AIOX `60.25` vs Tongyi DeepResearch `52.1` (delta +8.15)

**Verdict:** AIOX Research vence Tongyi DeepResearch em 51 de 102 dimensões

### AIOX wins (51 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `cli_entry` | 75 | 50 | +25 |
| `api_entry` | 75 | 50 | +25 |
| `ui_entry` | 75 | 50 | +25 |
| `ambiguity_detect` | 100 | 40 | +60 |
| `intent_capture` | 100 | 40 | +60 |
| `scope_negotiation` | 100 | 40 | +60 |
| `subquery_count` | 95 | 50 | +45 |
| `topic_taxonomy` | 95 | 50 | +45 |
| `priority_ordering` | 95 | 50 | +45 |
| `prompts_versioned` | 95 | 45 | +50 |
| `prompt_audit_trail` | 95 | 45 | +50 |
| `prompt_reuse` | 95 | 45 | +50 |
| `wave_count_bounded` | 100 | 60 | +40 |
| `wave_state_tracking` | 95 | 60 | +35 |
| `saturation_detection` | 95 | 60 | +35 |
| `full_content_fetch` | 90 | 60 | +30 |
| `summarize_per_source` | 90 | 60 | +30 |
| `extract_quotes` | 90 | 60 | +30 |
| `inter_wave_compress` | 100 | 45 | +55 |
| `redundancy_removal` | 95 | 45 | +50 |
| _(+31 more)_ | | | |

### Tongyi DeepResearch wins (30 dims)

| Microdim | AIOX | Opp | Δ |
|---|---:|---:|---:|
| `parallel_spawn` | 40 | 50 | -10 |
| `parallel_fetch` | 40 | 50 | -10 |
| `concurrency_safe` | 40 | 50 | -10 |
| `concurrent_execution` | 30 | 55 | -25 |
| `result_aggregation` | 30 | 55 | -25 |
| `failure_isolation` | 30 | 55 | -25 |
| `research_dataset_train` | 0 | 95 | -95 |
| `rl_emergent_behaviors` | 0 | 95 | -95 |
| `benchmark_dominance` | 0 | 80 | -80 |
| `ollama_support` | 60 | 85 | -25 |
| `llamacpp_support` | 60 | 85 | -25 |
| `hf_local_inference` | 60 | 85 | -25 |
| `arxiv_integration` | 30 | 55 | -25 |
| `pubmed_integration` | 30 | 55 | -25 |
| `semantic_scholar_integration` | 30 | 55 | -25 |
| `benchmark_published` | 20 | 75 | -55 |
| `eval_artifacts_public` | 20 | 75 | -55 |
| `reproducible_eval` | 20 | 75 | -55 |
| `package_published` | 0 | 50 | -50 |
| `semver_releases` | 10 | 50 | -40 |
| _(+10 more)_ | | | |

### Strategic Implication

AIOX vence no aggregate. Manter vantagens em **Planejamento, Entrada**; reduzir surface de ataque em **Execucao**.

---

