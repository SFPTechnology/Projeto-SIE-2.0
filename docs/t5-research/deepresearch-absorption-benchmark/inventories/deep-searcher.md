# Inventory — DeepSearcher

- Slug: `deep-searcher`
- Repo: [zilliztech/deep-searcher](https://github.com/zilliztech/deep-searcher)
- Classe: `private_kb_rag`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 7832 / 759 / 57
- Score de absorção: **70.2**
- Decisão: `absorb_rag_patterns`

## Classificação

Runtime private-KB/RAG, não agente full web-research.

## Padrão Absorvível

provider_registry_collection_routing_chain_of_rag

Sinal forte: Provider registry, collection routing, ChainOfRAG, sentence-window wider_text.

## Risco Principal

web_search_todo_global_state_ast_literal_eval

Risco da revisão: Estado global, web search TODO, ast.literal_eval, defaults externos.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 87 |
| trace_observability | 60 |
| private_kb_grounding | 95 |
| evaluation_value | 42 |
| implementation_maturity | 95.7 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 86 |
| sinkra_fit | 89 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/deep-searcher/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/deep-searcher/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/deep-searcher/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/deep-searcher/phase-8-documentation/deep-anatomist-notes.md` |
