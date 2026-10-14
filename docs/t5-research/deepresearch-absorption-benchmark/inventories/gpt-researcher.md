# Inventory — GPT-Researcher

- Slug: `gpt-researcher`
- Repo: [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)
- Classe: `research_facade`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 27126 / 3647 / 102
- Score de absorção: **72.1**
- Decisão: `absorb_facade_and_strategy`

## Classificação

Facade stateful de pesquisa com MCP como camada core de retrieval.

## Padrão Absorvível

source_strategy_mcp_context_compression

Sinal forte: Source strategy, retriever fan-out, MCP retriever, context compression.

## Risco Principal

llm_parsing_duplicate_routes_license_divergence

Risco da revisão: Rotas FastAPI duplicadas, parsing LLM para learnings/citações, divergência de licença.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 89 |
| trace_observability | 68 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 98 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 92 |
| compliance_safety | 90 |
| sinkra_fit | 91 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/gpt-researcher/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/gpt-researcher/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/gpt-researcher/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/gpt-researcher/phase-8-documentation/deep-anatomist-notes.md` |
