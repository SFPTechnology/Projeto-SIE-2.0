# Inventory — LiveDRBench

- Slug: `livedrbench`
- Repo: [microsoft/LiveDRBench](https://github.com/microsoft/LiveDRBench)
- Classe: `claim_evaluator`
- Linguagem: `Python`
- Licença: `MIT`
- Stars/Forks/Issues: 18 / 3 / 0
- Score de absorção: **67.6**
- Decisão: `absorb_metric_contract`

## Classificação

Avaliador offline de claim discovery com HF dataset + OpenAI judge.

## Padrão Absorvível

claim_level_precision_recall_f1

Sinal forte: Claim-level precision/recall/F1, category graders, anti-leakage key.

## Risco Principal

openai_judge_no_pins_assert_validation

Risco da revisão: Sem pins/testes, assert validation, parsing LLM frágil, stdout result.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 84 |
| trace_observability | 60 |
| private_kb_grounding | 48 |
| evaluation_value | 92 |
| implementation_maturity | 60.1 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 86 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/livedrbench/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/livedrbench/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/livedrbench/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/livedrbench/phase-8-documentation/deep-anatomist-notes.md` |
