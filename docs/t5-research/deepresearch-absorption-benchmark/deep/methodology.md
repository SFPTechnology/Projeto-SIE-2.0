# Metodologia — DeepResearch Absorption Benchmark

## Fonte De Dados

1. Pesquisa gold em `docs/research/2026-05-16-quais-os-melhores-projetos-de-deepresearch-opensource-atuais/`.
2. Anatomias locais em `outputs/decoded/{slug}/`.
3. Revisão de qualidade em `outputs/decoded/deepresearch-batch-code-anatomist/quality-review-2026-05-18.yaml`.
4. Matriz comparativa em `outputs/decoded/deepresearch-batch-code-anatomist/comparative-matrix-2026-05-18.yaml`.

## Escopo

O bench avalia **absorção arquitetural**. Cada player recebe score por cenário e score composto, usando sinais de código local, maturidade de repositório, licença, risco operacional e aderência ao protocolo SINKRA-DR-40.

## Dimensões E Pesos

| Dimensão | Peso |
| --- | --- |
| architecture_absorption | 20 |
| trace_observability | 14 |
| private_kb_grounding | 12 |
| evaluation_value | 14 |
| implementation_maturity | 10 |
| scientific_pipeline | 7 |
| training_methodology | 5 |
| product_ux_reference | 6 |
| compliance_safety | 8 |
| sinkra_fit | 4 |

## Limitação Explícita

Este pacote ainda não é o resultado de executar os 40 tasks do protocolo contra todos os sistemas. Ele é a etapa gold de seleção, anatomia e desenho de harness. A próxima etapa é implementar o runner e executar os tasks reproduzíveis.
