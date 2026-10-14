# Inventory — DRBench

- Slug: `drbench`
- Repo: [ServiceNow/drbench](https://github.com/ServiceNow/drbench)
- Classe: `enterprise_benchmark`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 35 / 6 / 1
- Score de absorção: **77.6**
- Decisão: `absorb_fixture_oracle`

## Classificação

Benchmark enterprise com sandbox Docker multi-serviço e oracle de relatório.

## Padrão Absorvível

task_eval_env_report_insights_sandbox

Sinal forte: task/eval/env/report_insights contract, score_report, private-KB fixture.

## Risco Principal

docker_heavy_judge_mediated_no_trace

Risco da revisão: Docker pesado, judge-mediated, outputs default, sem trace canônico.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 88 |
| trace_observability | 80 |
| private_kb_grounding | 95 |
| evaluation_value | 96 |
| implementation_maturity | 63.5 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 86 |
| sinkra_fit | 90 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/drbench/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/drbench/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/drbench/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/drbench/phase-8-documentation/deep-anatomist-notes.md` |
