# Executive Report — Escolha do Visual Backbone para o B-Roll Finder OSS

> Para: Alan Nicolas / Sinkra Hub
> Lente: substituto OSS do **B-Roll Finder do Eddie AI** — semantic search numa biblioteca pessoal de B-roll, casando texto de transcript com conteúdo visual.
> Data: 2026-05-06.

## Recomendação concreta (TL;DR)

**Default: `laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K` (OpenCLIP, 428M params, 768-dim).**

**Fallback multilingual: `google/siglip2-base-patch16-256` (SigLIP 2 base, 86M params, multilingue nativo, Apache 2.0).**

**Não usar: CLIP OpenAI original** — soft-deprecated, licença dos pesos ambígua, perde em todos os benchmarks recentes.

### Por que OpenCLIP DataComp-XL é o default

1. **Acurácia/tamanho ótimos:** 79.2% ImageNet zero-shot top-1 com 428M params, virtualmente empatando o SigLIP 2 base (79.1%) e batendo CLIP OpenAI ViT-L (75.4%). ([HF DataComp.XL card](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K))
2. **Integração ChromaDB nativa:** uma linha de código com `OpenCLIPEmbeddingFunction` — sem wrapper. ([Chroma docs](https://docs.trychroma.com/docs/embeddings/embedding-functions))
3. **Integração LanceDB nativa, FAISS via clip-retrieval, padrão de mercado** desde 2022.
4. **Latência viável em Mac M1/M2:** ViT-L/14 corre em MPS na casa de 150-200ms/img, indexa 50k frames em ~2.5h.
5. **Embedding dim 768:** custo previsível em FAISS/pgvector.
6. **Licença MIT** no código e nos pesos (com disclaimer "research output" — comunidade trata como permitido em produção).

### Por que SigLIP 2 base como fallback multilingual

1. **Multilingual nativo (>100 idiomas, incluindo PT-BR)** via WebLI training, sem variante separada. ([HF Blog SigLIP 2](https://huggingface.co/blog/siglip2))
2. **Apache 2.0 inequívoco** nos pesos — defensivo se o B-Roll Finder vier a ser distribuído.
3. **Estado-da-arte em retrieval** — COCO R@1 T→I = 81.7 (vs 68.3 do CLIP OpenAI); B/16 supera ou empata baselines maiores. ([arXiv 2502.14786](https://arxiv.org/abs/2502.14786))
4. **86M params** = inferência leve em Mac (~88ms/img em M1 Pro MPS). ([HF discussão MPS](https://huggingface.co/visheratin/mexma-siglip2/discussions/2))
5. **Fairness/de-biasing explícitos** na receita de treino.

## Decisão por critério

| Critério | Vencedor | Justificativa |
|---|---|---|
| Retrieval accuracy (zero-shot ImageNet) | **OpenCLIP DataComp-XL** (79.2%) ≈ SigLIP 2 base (79.1%) | Empate técnico; OpenCLIP vence em ecosystem |
| COCO/Flickr R@1 | **SigLIP 2** (R@1 T→I = 81.7 base; supera CLIP OpenAI por 13pts) | Vencedor claro |
| Inferência Mac M-series | **Empate técnico** (ambos ~88-280ms/img dependendo do tamanho) | OpenCLIP tem QuickGELU que pode ser otimizada |
| Inferência Linux GPU | **OpenCLIP** (pipeline mais maduro, FP16/TF32) | Mais documentação |
| Licença comercial | **SigLIP 2** (Apache 2.0 limpo) | OpenCLIP MIT mas com disclaimer LAION-5B |
| Integração FAISS/Chroma/pgvector | **OpenCLIP** (Chroma e LanceDB nativos) | Ganha por margem larga |
| Multilingual / PT-BR | **SigLIP 2** (nativo) | OpenCLIP precisa variante XLM-R com perda EN |

**Score ponderado para o persona (`scorecard.md`):** OpenCLIP **88.4** > SigLIP 2 **83.0** > CLIP OpenAI **67.0**.

## Recomendação concreta de checkpoint

### Cenário A — Persona prioriza ship rápido + EN dominante

**Escolha:** `laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K`
- 428M params, embedding dim 768
- 79.2% zero-shot ImageNet
- ChromaDB nativo via `OpenCLIPEmbeddingFunction(model_name="ViT-L-14", checkpoint="datacomp_xl_s13b_b90k")`
- Tempo até MVP: 2-3 dias

### Cenário B — Persona prioriza PT-BR ou licença Apache 2.0

**Escolha:** `google/siglip2-base-patch16-256`
- 86M params, embedding dim 768
- 79.1% ImageNet, R@1 COCO 81.7 T→I
- Multilingual nativo
- Wrapper Chroma de ~30 linhas (notebook merveenoyan/siglip)
- Tempo até MVP: 4-5 dias

### Cenário C — Acurácia máxima, Linux GPU, biblioteca grande (>100k frames)

**Escolha:** `laion/CLIP-ViT-bigG-14-laion2B-39B-b160k`
- 2.5B params, embedding dim 1280
- 80.1% ImageNet, R@5 COCO 74.9%
- **Não rodar em Mac** — exige A100/3090
- Indexar offline em GPU, servir via FAISS persistido

### Anti-recomendação

**Não usar `openai/clip-vit-large-patch14` para nova produção.**
- Acurácia 4-5pts atrás dos modernos
- Licença dos pesos diz "deploy out of scope"
- Sem manutenção desde ~2022

## Stack completa proposta (contexto)

```
B-Roll Finder OSS — pipeline mínimo
┌──────────────────────────────────────────────┐
│ INGEST                                       │
│  • whisper.cpp (transcript + timestamps)     │
│  • PySceneDetect (cuts)                      │
│  • frame extraction (3-5 por scene)          │
├──────────────────────────────────────────────┤
│ EMBEDDING ← este bench                       │
│  • DEFAULT: OpenCLIP ViT-L/14 DataComp-XL    │
│  • ALT: SigLIP 2 base (multilingual)         │
├──────────────────────────────────────────────┤
│ INDEX                                        │
│  • ChromaDB (nativo OpenCLIP)                │
│  • ou LanceDB (nativo OpenCLIP)              │
│  • ou pgvector(768)                          │
├──────────────────────────────────────────────┤
│ QUERY                                        │
│  • transcript chunk → text embedding         │
│  • ANN top-K via FAISS                       │
│  • opcional: rerank com Qwen2-VL-2B          │
└──────────────────────────────────────────────┘
```

Lacunas que **nenhum dos 3 modelos resolve** sozinho — devem virar componentes adicionais:
- ASR (Whisper)
- Scene segmentation
- Frame-level captioning (NarVid-style, [arXiv 2503.05186](https://arxiv.org/pdf/2503.05186))
- Re-ranking visual (cross-encoder)

Ver `gap-analysis.md` para detalhes.

## Riscos e mitigações

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Persona terá ≥30% queries PT-BR e qualidade visual cair em OpenCLIP | Média | Adicionar SigLIP 2 como segundo backend após MVP; tradução automática como stopgap |
| Disclaimer LAION-5B levantado em compliance review | Baixa | Documentar que checkpoint é MIT; NSFW filter no pipeline |
| Apple Neural Engine seria 5-10× mais rápido que MPS | Baixa-média | Considerar MobileCLIP da Apple como complementar (fora do escopo deste bench) |
| `bigG` ser tentador mas inviável em Mac | Média | Ficar com L/14 a menos que prova de Linux GPU exista |

## Próximos passos sugeridos

1. **Spike de 1 dia:** `pip install open_clip_torch chromadb`, indexar 100 frames de B-roll com `ViT-L-14/datacomp_xl_s13b_b90k`, validar precisão visual subjetiva em 10 queries (5 EN, 5 PT).
2. Se precisão PT for ruim: rodar mesmo experimento com SigLIP 2 base.
3. Decidir backend definitivo após este spike.
4. Documentar embedding dim escolhido em ADR (`docs/architecture/adrs/ADR-XXX-broll-visual-backbone.yaml`).

## Veredicto final

> **OpenCLIP `ViT-L-14/datacomp_xl_s13b_b90k` para o MVP, com SigLIP 2 base como segundo backend opcional para queries multilingual. CLIP OpenAI fica fora.**

## Fontes consolidadas

- [arXiv 2502.14786 — SigLIP 2](https://arxiv.org/abs/2502.14786)
- [arXiv 2303.15343 — SigLIP v1](https://arxiv.org/pdf/2303.15343)
- [arXiv 2212.07143 — Reproducible scaling laws (OpenCLIP)](https://arxiv.org/pdf/2212.07143)
- [HF Blog SigLIP 2](https://huggingface.co/blog/siglip2)
- [HF — laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K](https://huggingface.co/laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K)
- [HF — google/siglip2-base-patch16-224](https://huggingface.co/google/siglip2-base-patch16-224)
- [HF — laion/CLIP-ViT-bigG-14-laion2B-39B-b160k](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k)
- [GitHub — mlfoundations/open_clip](https://github.com/mlfoundations/open_clip)
- [GitHub — openai/CLIP](https://github.com/openai/CLIP)
- [LAION blog — giant openclip](https://laion.ai/blog/giant-openclip/)
- [Chroma embedding functions](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [LanceDB OpenCLIP integration](https://lancedb.com/docs/integrations/embedding/openclip/)
- [HF MPS benchmark discussion](https://huggingface.co/visheratin/mexma-siglip2/discussions/2)
- [arXiv 2503.05186 — NarVid (frame-level captioning for retrieval, 2025)](https://arxiv.org/pdf/2503.05186)
