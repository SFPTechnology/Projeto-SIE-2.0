# Visual Embedding Models — Bench Index

> Bench: SigLIP / SigLIP 2 vs OpenCLIP vs CLIP (OpenAI) para escolher visual backbone do **B-Roll Finder OSS** (substituto do Eddie AI).
> Data: 2026-05-06 · Tipo: Universal Bench · Persona: Sinkra Hub builder solo.

## Veredicto

**Default:** OpenCLIP `ViT-L-14/datacomp_xl_s13b_b90k` (428M, 768-dim, 79.2% ImageNet, ChromaDB nativo).
**Fallback multilingual / Apache 2.0:** SigLIP 2 base (`google/siglip2-base-patch16-256`).
**Não usar:** CLIP OpenAI original (soft-deprecated, licença dos pesos ambígua).

Score persona-weighted: **OpenCLIP 88.4 · SigLIP 2 83.0 · CLIP OpenAI 67.0** (ver `scorecard.md`).

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| [`metadata.json`](./metadata.json) | Schema do bench, subjects, critérios, persona weights, sources index |
| [`inventory-siglip.md`](./inventory-siglip.md) | Linhagem, checkpoints, licença Apache 2.0, acurácia, multilingual, integrações |
| [`inventory-openclip.md`](./inventory-openclip.md) | LAION/DataComp/CommonPool variants, MIT license, integração ChromaDB/LanceDB |
| [`inventory-clip.md`](./inventory-clip.md) | OpenAI original, licença ambígua dos pesos, status soft-deprecated |
| [`comparison-matrix.md`](./comparison-matrix.md) | Paridade Forte/Parcial/Sem equivalente em 22 dimensões |
| [`scorecard.md`](./scorecard.md) | 0-100 em 6 dimensões (Maturity/Ecosystem/DX/Performance/Scalability/Community) + persona-weighted |
| [`gap-analysis.md`](./gap-analysis.md) | Lacunas individuais e estruturais; stack completa proposta |
| [`battle-card.md`](./battle-card.md) | Decisão rápida: quando usar cada um, killer features, riscos |
| [`executive-report.md`](./executive-report.md) | Recomendação concreta com checkpoint, próximos passos |

## Fluxo sugerido de leitura

1. **Tem 60s?** → `executive-report.md` (TL;DR + recomendação)
2. **Tem 5min?** → `battle-card.md` + `comparison-matrix.md`
3. **Tem 20min?** → tudo acima + `scorecard.md` + `gap-analysis.md`
4. **Vai implementar?** → inventários individuais (model cards, integração, pegadinhas)

## Critérios avaliados

- Retrieval accuracy (zero-shot ImageNet, COCO/Flickr30k retrieval, MTEB-multimodal)
- Inferência em Mac M-series (MPS / Neural Engine via CoreML) e Linux GPU
- Licença / clareza de uso comercial
- Integração FAISS / ChromaDB / pgvector / LanceDB
- Suporte multilingue, especialmente Português (PT-BR)

## Persona

**Builder solo do Sinkra Hub** construindo OSS substitute do Eddie AI's B-Roll Finder.
- Biblioteca pessoal de ~1k-50k clips
- Search via transcript text → cena visual
- Mac M-series para dev, Linux GPU para batch indexing opcional
- PT-BR + EN no input layer

Pesos do persona: Performance 0.25 · DX 0.20 · Maturity 0.15 · Ecosystem 0.15 · Community 0.15 · Scalability 0.10.

## Dependência com bench irmão

Este bench complementa [`docs/bench/submagic-vs-eddie-ai/`](../submagic-vs-eddie-ai/), que cobriu o nível de produto (Submagic vs Eddie AI). Aqui descemos uma camada — o componente técnico interno (visual embedding) que vai materializar o substituto OSS.

## Constraints respeitadas

- ≤ 12 chamadas de WebSearch/WebFetch combinadas (usei 10)
- Conteúdo em PT-BR
- Apenas escrita em `docs/bench/visual-embedding-models/`
- Nenhuma instalação local
- Cada claim com URL citada

## Fontes-chave

- [arXiv 2502.14786 — SigLIP 2 paper](https://arxiv.org/abs/2502.14786)
- [arXiv 2212.07143 — Reproducible scaling laws (OpenCLIP/Cherti et al.)](https://arxiv.org/pdf/2212.07143)
- [HF Blog — SigLIP 2 announcement](https://huggingface.co/blog/siglip2)
- [GitHub mlfoundations/open_clip](https://github.com/mlfoundations/open_clip)
- [GitHub openai/CLIP](https://github.com/openai/CLIP)
- [LAION blog — giant openclip ViT-G/14](https://laion.ai/blog/giant-openclip/)
- [Chroma docs — embedding functions](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [LanceDB OpenCLIP integration](https://lancedb.com/docs/integrations/embedding/openclip/)
- [HF model card — laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K)
- [HF model card — google/siglip2-so400m-patch14-384](https://huggingface.co/google/siglip2-so400m-patch14-384)
