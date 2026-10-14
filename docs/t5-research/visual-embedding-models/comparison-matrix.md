# Matriz de Comparação — SigLIP / OpenCLIP / CLIP

> Lente: substituto OSS do **B-Roll Finder** do Eddie AI.
> Níveis: **Forte** · **Parcial** · **Sem equivalente**.
> Baseline para "Forte" é o estado-da-arte open-weight em mai/2026.

## Visão geral

| Critério | SigLIP / SigLIP 2 | OpenCLIP (LAION/DataComp) | CLIP (OpenAI original) |
|---|---|---|---|
| **Zero-shot ImageNet top-1 (best variant)** | **Forte** — SigLIP 2 So400m ≈ 84-85%+ | **Forte** — bigG/14 LAION-2B = 80.1% | **Parcial** — ViT-L/14 = 75.4% |
| **Zero-shot ImageNet top-1 (base ~150-300M)** | **Forte** — SigLIP 2 B/16 = 79.1% | **Forte** — L/14 DataComp-XL = 79.2% | **Parcial** — ViT-L/14 = 75.4% |
| **COCO retrieval R@1 (T→I)** | **Forte** — SigLIP 2 B/16 = 81.7 | **Parcial** — H/14 ≈ 73-75 R@5 (R@1 ~50-55) | **Parcial** — ViT-L = 68.3 |
| **COCO retrieval R@1 (I→T)** | **Forte** — SigLIP 2 B/16 = 69.7 | **Parcial** — bigG ~55-60 estimado | **Parcial** — ViT-L = 61.9 |
| **Flickr30k zero-shot** | **Forte** — escala matching SOTA | **Forte** — L/14 LAION reportado em scaling laws paper | **Parcial** — baseline original |
| **MTEB-multimodal / XM3600 (multilingual retrieval)** | **Forte** — SigLIP 2 B/16 = 40.7% R@1 médio em 36 idiomas | **Sem equivalente** nativo (precisa XLM-R variant, perde EN) | **Sem equivalente** |
| **Suporte a português (PT-BR) nativo** | **Forte** — WebLI cobre 100+ idiomas, PT incluído | **Sem equivalente** — apenas EN no padrão; XLM-R variant é ad-hoc | **Sem equivalente** |
| **Inferência Mac M-series (MPS, batch=1)** | **Parcial** — B/16 ≈ 88ms/img, L ≈ 280ms/img (M1 Pro) | **Parcial** — ViT-L/14 latência similar; QuickGELU subótimo | **Parcial** — mesma arq, mesma latência que OpenCLIP-L |
| **Inferência Mac (Neural Engine via CoreML)** | **Parcial** — export manual via timm; sem pipeline oficial Google | **Parcial** — community CoreML conversions existem | **Parcial** — community conversions |
| **Inferência Linux GPU (3090/A100)** | **Forte** — TF32/FP16 estável | **Forte** — pipeline maduro 4 anos | **Forte** — base original |
| **Licença comercial inequívoca** | **Forte** — Apache 2.0 sem ressalvas | **Parcial** — código+weights MIT, mas card diz "research output"; LAION-5B uncurated | **Sem equivalente** — código MIT, model card diz "deploy out of scope" |
| **Embedding dimension flexibility** | **Forte** — 768 (B) / 1024 (L) / 1152 (So400m) / 1408 (g) | **Forte** — 512 / 768 / 1024 / 1280 | **Parcial** — 512 (B) / 768 (L) apenas |
| **Tamanhos de checkpoint disponíveis** | **Forte** — 4 escalas (86M / 303M / 400M / 1B) + naflex | **Forte** — 6+ escalas (B/32 a bigG 2.5B) × 3-4 datasets | **Parcial** — 4 ViT (B/32, B/16, L/14, L/14@336) + ResNets |
| **Integração ChromaDB nativa** | **Sem equivalente** — precisa wrapper custom | **Forte** — `OpenCLIPEmbeddingFunction` first-class | **Parcial** — via OpenCLIP ou wrapper transformers |
| **Integração FAISS** | **Forte** — notebook oficial Merve Noyan | **Forte** — clip-retrieval, Harper Reed pattern | **Forte** — qualquer wrapper transformers |
| **Integração LanceDB** | **Parcial** — via timm/transformers manual | **Forte** — integração oficial | **Parcial** — manual |
| **Integração pgvector** | **Parcial** — manual (gerar embedding + INSERT) | **Parcial** — manual mas dim conhecidos | **Parcial** — manual |
| **Comunidade / atualização contínua** | **Forte** — Google ativo, SigLIP 2 fev/2025 | **Forte** — LAION+mlfoundations ativos | **Sem equivalente** — soft-deprecated, sem releases novas |
| **Precedente em B-roll/video search OSS** | **Parcial** — SigLIP em VLMs (Qwen2-VL, etc.); pouco em retrieval puro de B-roll | **Forte** — Harper Reed meme search, vários writeups | **Parcial** — base de muitos protótipos antigos |
| **Memory footprint base (~300M params)** | **Forte** — 303M (L/16) | **Forte** — 428M (L/14) | **Forte** — 428M (L/14) |
| **Tooling em Python / HF Transformers** | **Forte** — `AutoProcessor`/`SiglipModel` | **Forte** — `open_clip` + HF Transformers | **Forte** — `CLIPModel`/`CLIPProcessor` |

## Condensado por dimensão crítica

### 1. Acurácia (zero-shot ImageNet + retrieval)

```
SigLIP 2 So400m  ────────█████████████████  85%+ / R@1 ~70+
OpenCLIP bigG     ─────────████████████      80.1% / R@5 74.9%
OpenCLIP L/DataComp ───────████████████      79.2% / strong R@1
SigLIP 2 B/16    ─────────███████████        79.1% / R@1 69.7
OpenCLIP L/14 LAION-2B ────██████████        75.3%
CLIP ViT-L/14   ──────────█████████          75.4% / R@1 61.9
```

### 2. Latência Mac M-series (proxy MPS, M1 Pro 16GB, 327 imgs)

| Modelo | ms/img | Total 1k imgs | Total 50k imgs |
|---|---|---|---|
| SigLIP 2 B/16-512 | ~88ms | ~88s | ~73min |
| SigLIP 2 L/16-512 | ~280ms | ~280s | ~3.9h |
| OpenCLIP ViT-L/14 (estim.) | ~150-200ms | ~3min | ~2.5h |
| OpenCLIP bigG/14 | ~600-900ms | ~12min | ~10h+ |

> Para B-roll library de **~10k clips × 5 frames/clip = 50k frames**, ViT-L/14 ou SigLIP 2 B/16 indexam em uma manhã. bigG é inviável em Mac.

### 3. Multilingual (PT-BR é requisito do persona)

| Modelo | XM3600 R@1 médio | PT-BR nativo | Notas |
|---|---|---|---|
| SigLIP 2 B/16 multilingual | **40.7%** | **Sim** | WebLI 100+ idiomas |
| OpenCLIP XLM-R-ViT-H | ~25-30% (estim. baseline LAION) | Sim, mas perde EN | Não-canônico |
| OpenCLIP padrão | N/A | **Não** | Apenas EN |
| CLIP OpenAI | N/A | **Não** | Apenas EN |

### 4. Licença / risco comercial

| Modelo | Código | Pesos | Risco |
|---|---|---|---|
| SigLIP 2 | Apache 2.0 | Apache 2.0 | **Baixo** |
| OpenCLIP LAION | MIT | MIT (research framing) | **Médio** — disclaimer LAION-5B |
| CLIP OpenAI | MIT | "Out of scope" para deploy | **Alto-médio** — ambíguo |

### 5. Integração com vector DB do persona

| Stack | Plug-and-play |
|---|---|
| OpenCLIP + ChromaDB | **Forte** — `OpenCLIPEmbeddingFunction` |
| OpenCLIP + LanceDB | **Forte** — integração oficial |
| OpenCLIP + FAISS | **Forte** — clip-retrieval |
| SigLIP + FAISS | **Forte** — notebook Merve |
| SigLIP + ChromaDB/LanceDB | **Parcial** — wrapper de 30 linhas |
| CLIP OpenAI + qualquer | **Parcial** — funcional mas ninguém recomenda |

## Trade-off resumido

- **Quer máxima acurácia EN + multilingual + licença limpa:** SigLIP 2.
- **Quer ecossistema mais maduro + ChromaDB nativo + EN puro:** OpenCLIP ViT-L/14 (DataComp-XL).
- **Quer reproduzir paper de 2021 ou baseline histórica:** CLIP OpenAI.

## Fontes

- [arXiv 2502.14786 — SigLIP 2](https://arxiv.org/abs/2502.14786)
- [arXiv 2212.07143 — Reproducible scaling laws (Cherti et al.)](https://arxiv.org/pdf/2212.07143)
- [LAION blog — giant openclip](https://laion.ai/blog/giant-openclip/)
- [LAION blog — large openclip](https://laion.ai/blog/large-openclip/)
- [HF Blog — SigLIP 2](https://huggingface.co/blog/siglip2)
- [HF model card — OpenAI CLIP ViT-L/14](https://huggingface.co/openai/clip-vit-large-patch14)
- [HF model card — laion/CLIP-ViT-L-14-DataComp.XL](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K)
- [HF discussion — MPS M1 benchmark](https://huggingface.co/visheratin/mexma-siglip2/discussions/2)
- [Chroma docs — embedding functions](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [LanceDB OpenCLIP integration](https://lancedb.com/docs/integrations/embedding/openclip/)
