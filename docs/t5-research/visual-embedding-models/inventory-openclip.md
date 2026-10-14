# Inventário — OpenCLIP (mlfoundations / LAION)

> Lente: visual backbone para um substituto OSS do **B-Roll Finder** do Eddie AI.

## Linhagem e papers

OpenCLIP é a **implementação open-source de referência** do CLIP, mantida em [mlfoundations/open_clip](https://github.com/mlfoundations/open_clip). Permite treinar CLIP do zero e expõe checkpoints treinados em LAION-400M, LAION-2B (LAION-5B subset EN), DataComp-XL/1B e CommonPool-XL.

Paper-base: *Reproducible scaling laws for contrastive language-image learning* (Cherti et al., CVPR 2023, [arXiv 2212.07143](https://arxiv.org/pdf/2212.07143)) — provê leis de escala reproduzíveis e tabelas R@1/R@5 em COCO/Flickr30k.

## Checkpoints e variantes

| Variante | Treino | Params | Embedding dim | Acurácia ImageNet zero-shot | Fonte |
|---|---|---|---|---|---|
| ViT-B/32 | LAION-2B | 151M | 512 | ~66% | [PRETRAINED.md](https://github.com/mlfoundations/open_clip/blob/main/docs/PRETRAINED.md) |
| ViT-B/16 | LAION-2B | 150M | 512 | ~70% | idem |
| **ViT-L/14** | **LAION-2B** | **428M** | **768** | **75.3%** | [HF model card](https://huggingface.co/laion/CLIP-ViT-L-14-laion2B-s32B-b82K) |
| **ViT-L/14** | **DataComp-XL** | **428M** | **768** | **79.2%** | [HF DataComp.XL](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K) |
| ViT-L/14 | CommonPool-XL | 428M | 768 | 72.3% | HF model card |
| ViT-H/14 | LAION-2B | 986M | 1024 | **78.0%** | [HF H/14](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K) |
| ViT-g/14 | LAION-2B | 1.4B | 1024 | ~76.6% | [HF g/14](https://huggingface.co/laion/CLIP-ViT-g-14-laion2B-s12B-b42K) |
| **ViT-G/14 (bigG)** | **LAION-2B** | **2.5B** | **1280** | **80.1%** (top OSS jan/2023) | [HF bigG](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k) · [LAION blog](https://laion.ai/blog/giant-openclip/) |

## Acurácia retrieval

### COCO (zero-shot, R@5 image retrieval)

- **ViT-G/14 LAION-2B — 74.9% R@5** ([LAION blog giant-openclip](https://laion.ai/blog/giant-openclip/))
- **ViT-H/14 LAION-2B — 73.4% R@5** ([LAION blog large-openclip](https://laion.ai/blog/large-openclip/))
- ViT-g/14 (LAION-2B-s12B) — segundo melhor em retrieval zero-shot (CLIP-as-service benchmark, Jina)

### Flickr30k / COCO R@1

Cherti et al. ([arXiv 2212.07143](https://arxiv.org/pdf/2212.07143)) — Tabelas 9-11 do paper têm R@1 detalhado por modelo. Tendência reportada: **OpenCLIP em LAION supera OpenAI WIT-400M em retrieval** mas perde em ImageNet zero-shot puro (escalas diferentes).

Para R@1 reprodutível, [LAION-AI/CLIP_benchmark](https://github.com/LAION-AI/CLIP_benchmark) é a suite canônica usada nos model cards (results notebook em `benchmark/results.ipynb`).

## Licença

- **Repositório `open_clip` — MIT** (código)
- **Checkpoints LAION (`laion/CLIP-ViT-*`) — MIT** declarado em todos os model cards (ex.: bigG, H/14, L/14)
- **Disclaimer importante:** model card adota linguagem do CLIP original — *"intended as a research output for research communities"*. LAION-5B é dataset **uncurated** crawled da web, pode conter material desconfortável.
- **Implicação prática:** MIT permite uso comercial juridicamente, mas modelo é posicionado como research. Para produção: filtrar com classificador NSFW LAION + due-diligence em compliance.

## Multilingue / Português

OpenCLIP base **NÃO é multilingue** — tokenizer é o BPE original do CLIP, treinado em texto majoritariamente EN (LAION-2B EN subset). Variantes multilingue:

- **`xlm-roberta-large-ViT-H-14-frozen_laion5b_s13b_b90k`** — versão XLM-R com texto multilingue (LAION-5B). Funciona com PT, mas latência ~2× e qualidade EN cai vs. ViT-H/14 EN.
- Coleção `openclip_multilingual` no [LAION-AI/CLIP_benchmark](https://github.com/LAION-AI/CLIP_benchmark) lista alternativas.

**Para PT-BR, OpenCLIP perde para SigLIP 2.** Não é o ferramental nativo.

## Integração FAISS / Chroma / pgvector

- **ChromaDB:** **integração nativa** via `OpenCLIPEmbeddingFunction` — texto e imagem out-of-the-box, sem código custom.
  ```python
  from chromadb.utils.embedding_functions.open_clip_embedding_function import OpenCLIPEmbeddingFunction
  ```
  ([Chroma docs](https://docs.trychroma.com/docs/embeddings/embedding-functions))
- **FAISS:** padrão estabelecido — Harper Reed's *meme search engine* ([blog](https://harper.blog/2024/04/12/i-accidentally-built-a-meme-search-engine/)) usa exatamente OpenCLIP + FAISS + Chroma.
- **LanceDB:** [embedding integration oficial](https://lancedb.com/docs/integrations/embedding/openclip/) com OpenCLIP.
- **pgvector:** sem integração first-party, mas embedding dim conhecido (768 para L, 1024 para H, 1280 para bigG) → coluna `vector(768)` direta.
- **clip-retrieval:** suporte nativo a OpenCLIP para indexar bilhões de embeddings.
- **timm dependency:** modelos com encoder timm (siglip, eva, convnext) exigem `timm` atualizado — risco de "Unknown model" se versão antiga.

## Performance / latência

- **Linux GPU (A100/3090):** ViT-B-32-256 em ~6.31ms/frame em torch GPU; ViT-L/14 ~3-5× mais lento.
- **Apple Silicon (MPS):** funciona via PyTorch MPS backend. **QuickGELU activation** dos modelos OpenAI legados **é menos eficiente que `torch.nn.GELU`** em PyTorch recente — checar config para evitar regressão.
- Throughput community gist: [TACIXAT/ecd4f636bf6af28cb69d641e29d7b362](https://gist.github.com/TACIXAT/ecd4f636bf6af28cb69d641e29d7b362)

## Pontos fortes

1. **Ecossistema #1** — integração nativa Chroma/LanceDB, suporte clip-retrieval, dezenas de tutoriais.
2. **Selecionável por dataset** — LAION-2B vs DataComp-XL vs CommonPool-XL com tradeoffs documentados.
3. **MIT pragmático** — código + weights MIT (módulo disclaimer research-only).
4. **Maturidade** — 4+ anos de uso em produção em milhares de pipelines.
5. **DataComp-XL ViT-L/14 = 79.2% ImageNet** — supera o SigLIP v1 base e empata SigLIP 2 base, com tooling muito mais maduro.

## Pontos fracos

1. **Não-multilingue por padrão** — PT-BR exige variante XLM-R com perda de qualidade EN.
2. **bigG = 2.5B params** — caro de servir e indexar em Mac.
3. Disclaimer LAION-5B (uncurated) requer **filtragem NSFW** se for público.
4. Em retrieval, **SigLIP 2 já supera** mesmo nos benchmarks que LAION criou.

## Veredicto setorial

- **Default sólido para B-Roll Finder OSS em EN** — ViT-L/14 (DataComp-XL) é o sweet spot.
- **Maturidade de ecossistema vence tudo** se time é solo e quer integrar ChromaDB hoje.
- **Perde para SigLIP 2** em (a) retrieval EN puro nos benchmarks novos e (b) multilingual PT.

## Fontes

- [GitHub mlfoundations/open_clip](https://github.com/mlfoundations/open_clip)
- [PRETRAINED.md (lista oficial de checkpoints)](https://github.com/mlfoundations/open_clip/blob/main/docs/PRETRAINED.md)
- [LAION blog — giant openclip ViT-G/14](https://laion.ai/blog/giant-openclip/)
- [LAION blog — large openclip L/14, H/14, g/14](https://laion.ai/blog/large-openclip/)
- [arXiv 2212.07143 — Reproducible scaling laws (Cherti et al.)](https://arxiv.org/pdf/2212.07143)
- [LAION-AI/CLIP_benchmark](https://github.com/LAION-AI/CLIP_benchmark)
- [HF — laion/CLIP-ViT-L-14-laion2B-s32B-b82K](https://huggingface.co/laion/CLIP-ViT-L-14-laion2B-s32B-b82K)
- [HF — laion/CLIP-ViT-bigG-14-laion2B-39B-b160k](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k)
- [HF — laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K)
- [LanceDB OpenCLIP integration](https://lancedb.com/docs/integrations/embedding/openclip/)
- [Chroma embedding functions docs](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [Harper Reed — meme search engine writeup](https://harper.blog/2024/04/12/i-accidentally-built-a-meme-search-engine/)
