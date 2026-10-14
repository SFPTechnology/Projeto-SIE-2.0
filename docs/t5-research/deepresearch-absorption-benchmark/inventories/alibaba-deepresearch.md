# Inventory — Alibaba/Tongyi DeepResearch

- Slug: `alibaba-deepresearch`
- Repo: [Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch)
- Classe: `research_monorepo_react`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 18892 / 1456 / 54
- Score de absorção: **64.4**
- Decisão: `absorb_patterns_no_vendor`

## Classificação

Monorepo de pesquisa com run_multi_react e ReAct por tags XML.

## Padrão Absorvível

react_tags_webweaver_url_ids_multi_rollout

Sinal forte: CLI rollout resumível, WebWeaver citation url2id, ParallelMuse multi-rollout.

## Risco Principal

external_services_unstructured_trace_shared_state

Risco da revisão: Dependências Serper/Jina/Dashscope/SandboxFusion, trace não estruturado.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 74 |
| trace_observability | 60 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 98 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 76 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/alibaba-deepresearch/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/alibaba-deepresearch/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/alibaba-deepresearch/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/alibaba-deepresearch/phase-8-documentation/deep-anatomist-notes.md` |
