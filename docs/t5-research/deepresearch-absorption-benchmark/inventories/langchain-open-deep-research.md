# Inventory — LangChain Open Deep Research

- Slug: `langchain-open-deep-research`
- Repo: [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research)
- Classe: `graph_runtime`
- Linguagem: `Python`
- Licença: `MIT`
- Stars/Forks/Issues: 11423 / 1637 / 95
- Score de absorção: **69.8**
- Decisão: `absorb_graph_pattern`

## Classificação

Grafo LangGraph em três camadas com supervisor, researcher e compressão.

## Padrão Absorvível

supervisor_researcher_graphs_parallel_research

Sinal forte: Supervisor/researcher subgraphs, ConductResearch paralelo, tool contract.

## Risco Principal

exception_masking_langgraph_coupling_external_apis

Risco da revisão: Handler com `or True`, dependência LangGraph/LangSmith, necessidade de cache/trace.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 92 |
| trace_observability | 68 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 97.7 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 93 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/langchain-open-deep-research/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/langchain-open-deep-research/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/langchain-open-deep-research/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/langchain-open-deep-research/phase-8-documentation/deep-anatomist-notes.md` |
