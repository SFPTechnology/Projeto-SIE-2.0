# Inventory — MiroTrain

- Slug: `mirotrain`
- Repo: [MiroMindAI/MiroTrain](https://github.com/MiroMindAI/MiroTrain)
- Classe: `post_training_pipeline`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 142 / 18 / 3
- Score de absorção: **64.8**
- Decisão: `pattern_first`

## Classificação

Pós-treinamento sobre TorchTune, não runtime de pesquisa.

## Padrão Absorvível

config_first_training_dataset_tokenizer_adapter

Sinal forte: Wrapper config-first, dataset/tokenizer adapter, Ulysses, Qwen3 MoE.

## Risco Principal

cuda_flashattention_monkey_patch_distributed_validation

Risco da revisão: Monkey patch/import order, CUDA/FlashAttention, validação distribuída.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 76 |
| trace_observability | 60 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 70.8 |
| scientific_pipeline | 40 |
| training_methodology | 88 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 78 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/mirotrain/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/mirotrain/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/mirotrain/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/mirotrain/phase-8-documentation/deep-anatomist-notes.md` |
