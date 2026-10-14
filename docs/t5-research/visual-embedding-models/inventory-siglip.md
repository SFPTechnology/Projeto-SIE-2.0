# Inventário — SigLIP / SigLIP 2 (Google)

> Lente: visual backbone para um substituto OSS do **B-Roll Finder** do Eddie AI.
> Família avaliada: SigLIP v1 (2023), SigLIP-multilingual (2024), **SigLIP 2 (fev/2025)**.

## Linhagem e papers

- **SigLIP v1** — *Sigmoid Loss for Language Image Pre-Training* (Zhai et al., 2023). Substitui o softmax contrastivo do CLIP por **sigmoid pairwise loss**, melhorando estabilidade em batches grandes/pequenos. ([arXiv 2303.15343](https://arxiv.org/pdf/2303.15343))
- **SigLIP 2** — *Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features* (Tschannen et al., fev/2025). Estende a receita SigLIP com **captioning-based pretraining, self-distillation, masked prediction e online data curation**, treinada em até 2048 chips TPU-v5e sobre WebLI. ([arXiv 2502.14786](https://arxiv.org/abs/2502.14786) · [HF Blog](https://huggingface.co/blog/siglip2))

## Checkpoints e variantes

| Variante | Params | Resolução | Treino | Notas |
|---|---|---|---|---|
| `google/siglip-base-patch16-256` | ~203M | 256 | WebLI (EN) | Baseline v1 ([HF](https://huggingface.co/google/siglip-base-patch16-256)) |
| `google/siglip-base-patch16-256-multilingual` | ~370M | 256 | WebLI multi | v1 multilingue (>100 idiomas, inclui PT-BR) ([HF](https://huggingface.co/google/siglip-base-patch16-256-multilingual)) |
| `google/siglip2-base-patch16-224` | 86M (ViT-B) | 224 | WebLI multi | SigLIP 2 base FixRes ([HF](https://huggingface.co/google/siglip2-base-patch16-224)) |
| `google/siglip2-large-patch16-*` | 303M (ViT-L) | 256/384 | WebLI multi | Sweet spot precisão/latência |
| `google/siglip2-so400m-patch14-384` | 400M (SoViT) | 384 | WebLI multi | Flagship, melhor zero-shot ([HF](https://huggingface.co/google/siglip2-so400m-patch14-384)) |
| `google/siglip2-giant-patch16-*` | ~1B (ViT-g) | varia | WebLI multi | Topo de linha |
| `*-naflex-*` | mesmas tamanhos | dinâmico | WebLI multi | NaFlex preserva aspect ratio |
| `timm/vit_so400m_patch14_siglip_224.v2_webli` | 400M | 224 | WebLI | Image-encoder-only, otimizado ([HF](https://huggingface.co/timm/vit_so400m_patch14_siglip_224.v2_webli)) |

**4 tamanhos canônicos do SigLIP 2:** ViT-B (86M), L (303M), So400m (400M), g (1B). ([arXiv 2502.14786](https://arxiv.org/abs/2502.14786))

## Licença

**Apache 2.0** em todos os checkpoints (`google/siglip2-*`, `timm/*siglip*`, `google/siglip-*-multilingual`). Uso comercial permitido, sem cláusula "research-only" como o CLIP da OpenAI. ([HF Blog SigLIP 2](https://huggingface.co/blog/siglip2))

## Acurácia declarada

### Zero-shot ImageNet-1k (top-1)

| Modelo | Acurácia | Fonte |
|---|---|---|
| SigLIP B/16 @256 | 76.7% | [arXiv 2502.14786](https://arxiv.org/abs/2502.14786) |
| **SigLIP 2 B/16 @256** | **79.1%** | idem |
| SigLIP-g/14 (SigLiT) | 84.5% (top da família v1) | idem |
| SigLIP 2 So400m / g — equivalente ou superior em todas escalas | up to ~85%+ | idem |

### COCO retrieval (R@1, image↔text)

| Modelo | I→T R@1 | T→I R@1 | Fonte |
|---|---|---|---|
| SigLIP B/16 @256 | 65.1 | 78.3 | [arXiv 2502.14786](https://arxiv.org/abs/2502.14786) |
| **SigLIP 2 B/16 @256** | **69.7** | **81.7** | idem |
| CLIP (OpenAI ViT-L) baseline | 61.9 | 68.3 | idem (Tabela comparativa) |

### Multilingual (XM3600, R@1 médio em 36 idiomas)

- **SigLIP 2 B/16 — R@1 médio = 40.7%**, "quase iguala mSigLIP" e supera baselines monolingue mesmo em tarefas EN. ([HF Blog](https://huggingface.co/blog/siglip2))
- Reduz o representation bias de 7% (SigLIP 2 L/16) — fairness explícita.

## Multilingue / Português

- Treinado em **WebLI**, dataset multilingue cobrindo **>100 idiomas (incl. PT-BR)** sem precisar de variante separada. ([HF Blog SigLIP 2](https://huggingface.co/blog/siglip2))
- `Siglip2Tokenizer` aplica lowercase no backend (matching training-time) — usar `AutoProcessor` evita armadilhas. ([HF docs](https://huggingface.co/docs/transformers/main/model_doc/siglip2))

## Integração FAISS / Chroma / pgvector

- **FAISS:** notebook oficial de Merve Noyan — `siglip_faiss_indexing_and_search.ipynb`. ([repo](https://github.com/merveenoyan/siglip))
- **ChromaDB:** sem embedding-function nativa (o nativo é OpenCLIP). Usar `EmbeddingFunction` custom com `AutoProcessor` + `SiglipModel.get_image_features` / `get_text_features`.
- **pgvector:** sem tutorial oficial; padrão é gerar embedding via HF Transformers e gravar coluna `vector` (768 para B, 1024 para L, 1152 para So400m).
- **Atenção:** ao usar `SiglipTokenizer` standalone, passar `padding="max_length"` (era assim que foi treinado). ([HF docs SigLIP](https://huggingface.co/docs/transformers/en/model_doc/siglip))

## Performance em Apple Silicon

Benchmark MPS em **MBP M1 Pro 16GB** (327 imagens, batch 1) reportado em discussão HF:

| Modelo | Tempo total | Por imagem |
|---|---|---|
| ViT-B-16-SigLIP2-512 | 28.94s | ~88ms |
| ViT-L-16-SigLIP2-512 | 91.69s | ~280ms |
| mexma-siglip2 (multilingue custom) | 131.22s | ~401ms |

Fonte: [discussão HF mexma-siglip2](https://huggingface.co/visheratin/mexma-siglip2/discussions/2).

Conversão CoreML viável (timm exporta TorchScript) mas não há pipeline oficial Google ainda. Para máxima performance no Neural Engine, **MobileCLIP da Apple supera SigLIP-So400m com 2× menos params em iPhone 12 Pro Max** ([apple/ml-mobileclip](https://github.com/apple/ml-mobileclip)) — mas é fora do escopo desta bench (não está nos subjects).

## Pontos fortes

1. **Estado-da-arte open-weight 2025/26** em retrieval e classificação zero-shot.
2. **Multilingue de fábrica** — único dos 3 subjects com PT-BR nativo sem compromisso de precisão EN.
3. **Apache 2.0** sem ambiguidade comercial.
4. **Sigmoid loss** — escala melhor em batches pequenos, importante para indexação local de B-roll.
5. **Família ampla** — 86M até 1B, escolha por orçamento/latência.

## Pontos fracos

1. Embedding dim **1152** (So400m) é ~50% maior que CLIP-L/14 (768), aumentando custo de FAISS/pgvector.
2. CoreML pipeline não-oficial — depende de export manual via `timm`/`transformers`.
3. Ecossistema de tutorial em **vector DB** menor que OpenCLIP (que tem integração nativa Chroma/LanceDB).
4. Modelos ViT-g (1B) excedem orçamento de RAM unificada em Macs ≤ 16GB para batch indexing.

## Veredicto setorial

- **Multilingual / PT-BR pesado:** SigLIP 2 base ou L é a escolha óbvia — **vence OpenCLIP e CLIP por margem clara em XM3600**.
- **Pure-EN max accuracy:** SigLIP 2 So400m/384 empata ou supera OpenCLIP ViT-G/14, com **2.5× menos parâmetros**.

## Fontes

- [arXiv 2502.14786 — SigLIP 2 paper](https://arxiv.org/abs/2502.14786)
- [arXiv 2303.15343 — SigLIP v1 paper](https://arxiv.org/pdf/2303.15343)
- [HF Blog — SigLIP 2 announcement](https://huggingface.co/blog/siglip2)
- [HF model card — google/siglip-base-patch16-256](https://huggingface.co/google/siglip-base-patch16-256)
- [HF model card — google/siglip2-so400m-patch14-384](https://huggingface.co/google/siglip2-so400m-patch14-384)
- [HF model card — google/siglip-base-patch16-256-multilingual](https://huggingface.co/google/siglip-base-patch16-256-multilingual)
- [HF docs — SigLIP2 transformers](https://huggingface.co/docs/transformers/main/model_doc/siglip2)
- [merveenoyan/siglip — FAISS notebooks](https://github.com/merveenoyan/siglip)
- [HF discussion — MPS benchmarks (mexma-siglip2)](https://huggingface.co/visheratin/mexma-siglip2/discussions/2)
