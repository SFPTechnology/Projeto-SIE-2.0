# Inventory — MiroEval

- Slug: `miroeval`
- Repo: [MiroMindAI/MiroEval](https://github.com/MiroMindAI/MiroEval)
- Classe: `benchmark_harness`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 39 / 5 / 0
- Score de absorção: **67.9**
- Decisão: `absorb_evaluator`

## Classificação

Benchmark harness de três lentes: factual, point quality e process eval.

## Padrão Absorvível

three_lens_eval_segment_parallel_merge

Sinal forte: Segment-parallel-merge, rubrica dinâmica, process/report alignment.

## Risco Principal

multimodal_path_hydra_global_private_method

Risco da revisão: Caminho multimodal inconsistente, os.chdir, Hydra global, chamada privada.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 86 |
| trace_observability | 60 |
| private_kb_grounding | 48 |
| evaluation_value | 88 |
| implementation_maturity | 64.1 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 88 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/miroeval/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/miroeval/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/miroeval/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/miroeval/phase-8-documentation/deep-anatomist-notes.md` |
