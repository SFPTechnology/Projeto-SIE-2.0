# Inventory — Jina node-DeepResearch

- Slug: `node-deepresearch`
- Repo: [jina-ai/node-DeepResearch](https://github.com/jina-ai/node-DeepResearch)
- Classe: `action_state_machine`
- Linguagem: `TypeScript`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 5173 / 452 / 50
- Score de absorção: **69.5**
- Decisão: `absorb_action_schema`

## Classificação

State machine action-based com API local OpenAI-compatible.

## Padrão Absorvível

schema_first_actions_safe_generation

Sinal forte: schemas.ts, safe-generator, ações search/visit/reflect/answer/coding.

## Risco Principal

jina_dependency_codesandbox_secret_validation

Risco da revisão: Dependência Jina, CodeSandbox, secrets no import, streaming não padrão.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 86 |
| trace_observability | 68 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 89.6 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 80 |
| compliance_safety | 86 |
| sinkra_fit | 88 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/node-deepresearch/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/node-deepresearch/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/node-deepresearch/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/node-deepresearch/phase-8-documentation/deep-anatomist-notes.md` |
