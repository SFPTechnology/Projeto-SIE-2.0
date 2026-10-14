# Inventory — AIOX/SINKRA Research Ecosystem

Recomendação: **Criar SINKRA DeepResearchRunner próprio e absorver padrões por adapters, não vendorizar um player inteiro.**

## Outputs Obrigatórios Do Runner

| Output |
| --- |
| `trace.jsonl` |
| `tool-calls.jsonl` |
| `claims.yaml` |
| `sources.yaml` |
| `report.md` |
| `rubric-results.yaml` |
| `cost-latency.yaml` |
| `failure-analysis.md` |
| `replay-manifest.yaml` |

## Waves

| Wave | Nome | Itens |
| --- | --- | --- |
| 1 | contract_and_harness | define_sinkra_deepresearchrunner, implement_trace_sources_claims_cost_contract, adapters_for_dzhng_gpt_researcher_langchain, evaluator_wrappers_for_livedrbench_drbench |
| 2 | sinkra_runtime | deerflow_lifecycle, langchain_graph_pattern, jina_action_schema, gpt_researcher_source_strategy |
| 3 | private_kb | deepsearcher_adapter, local_deep_research_mcp_api_adapter, drbench_like_synthetic_fixture, redaction_and_business_isolation |
| 4 | gold_evaluation | drbench_report_insights, livedrbench_claim_discovery, miroeval_three_lens, deep_research_bench_race_fact, autoresearchclaw_verified_registry |
