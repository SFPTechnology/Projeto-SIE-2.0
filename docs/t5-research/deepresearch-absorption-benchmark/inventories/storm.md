# Inventory — STORM

- Slug: `storm`
- Repo: [stanford-oval/storm](https://github.com/stanford-oval/storm)
- Classe: `article_research_pipeline`
- Linguagem: `Python`
- Licença: `MIT`
- Stars/Forks/Issues: 28237 / 2568 / 154
- Score de absorção: **73.0**
- Decisão: `absorb_interfaces_artifacts`

## Classificação

Dois runtimes: storm_wiki stage-based e collaborative_storm multiagent.

## Padrão Absorvível

interface_layer_vectorrm_intermediate_artifacts

Sinal forte: Interface Information/Retriever/Engine/Agent, VectorRM, intermediate artifacts.

## Risco Principal

external_apis_home_cache_nondeterminism

Risco da revisão: APIs externas, cache LiteLLM em home, concorrência não determinística.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 82 |
| trace_observability | 68 |
| private_kb_grounding | 84 |
| evaluation_value | 42 |
| implementation_maturity | 98 |
| scientific_pipeline | 92 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 84 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/storm/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/storm/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/storm/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/storm/phase-8-documentation/deep-anatomist-notes.md` |
