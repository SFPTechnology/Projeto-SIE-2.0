# Gap Analysis — escolha de visual backbone para B-Roll Finder OSS

> Lente: Sinkra Hub builder solo, ~1k-50k clips de B-roll, prompts em PT/EN, indexação em Mac M-series, query também em Mac (e/ou Linux GPU para batch).

## Lacunas em cada subject

### SigLIP / SigLIP 2

| Lacuna | Severidade | Mitigação |
|---|---|---|
| Sem `EmbeddingFunction` nativo no ChromaDB / LanceDB | Média | Wrapper de ~30 linhas implementando `EmbeddingFunction` via `AutoProcessor` + `SiglipModel.get_image_features` / `get_text_features`. Ver notebook `merveenoyan/siglip` como base. |
| CoreML / Apple Neural Engine sem pipeline oficial Google | Média-baixa | Export manual via `torch.jit.trace` ou `coremltools`. Para MVP, MPS basta (~88ms/img B/16). |
| Embedding dim 1152 (So400m) eleva custo de FAISS/pgvector vs 768 do CLIP-L | Baixa | Usar variante L/16 (768) ou aplicar PCA pra 768. |
| Modelos g/14 (1B params) excedem RAM unificada em Mac ≤16GB | Baixa | Não usar g/14 em Mac — fica para Linux GPU se acurácia máxima for crítica. |
| Pegadinha do tokenizer (`padding="max_length"` obrigatório) | Baixa | Documentar no README do projeto. |
| Variante v1 multilingual (`siglip-base-patch16-256-multilingual`) tem qualidade inferior à v2 | Média | Usar SigLIP 2 (que já é multilingue de fábrica). |

### OpenCLIP

| Lacuna | Severidade | Mitigação |
|---|---|---|
| Não-multilingue por default — PT-BR exige `xlm-roberta-large-ViT-H-14-frozen_laion5b_s13b_b90k` | **Alta** para o persona | Usar variante XLM-R OU traduzir prompts PT→EN antes de embedar. Trade-off: perde nuance/idioma. |
| LAION-5B uncurated → risco de viés/NSFW residual nos embeddings | Média | Filtrar via NSFW classifier LAION; documentar limitação. |
| Modelo card declara "research output" apesar de licença MIT | Baixa-média | Due diligence legal; em prática toda comunidade usa em produção. |
| QuickGELU activation (legado OpenAI) menos eficiente que `nn.GELU` | Baixa | Setar `act_layer=nn.GELU` ao criar modelo se checkpoint suportar. |
| bigG/14 = 2.5B params, lento em Mac | Média | Usar L/14 DataComp-XL (428M) — sweet spot. |
| Tokenizer/treino EN-cêntricos significam que B-roll com **conteúdo culturalmente PT-BR** (objetos, cenas Brasil) tem precisão menor | Média | Combinar com tradução automática ou fine-tune leve com pares PT-BR. |

### CLIP OpenAI

| Lacuna | Severidade | Mitigação |
|---|---|---|
| Acurácia ultrapassada (75.4% ImageNet vs 79+% nas alternativas) | **Alta** | **Não usar** — OpenCLIP/SigLIP 2 superam em todos eixos. |
| Licença dos pesos ambígua ("out of scope for deploy") | **Alta** | Migrar para OpenCLIP MIT ou SigLIP 2 Apache. |
| Manutenção parada desde ~2022 | Alta | idem — não há fix futuro vindo. |
| Sem multilingue nativo | Alta | idem. |
| Apenas 4 variantes ViT + ResNets antigos | Média | idem. |

## Lacunas estruturais do problema "B-Roll Finder OSS" que NENHUM dos 3 resolve sozinho

| Gap | Por que importa | Quem cobre |
|---|---|---|
| **Embedding de vídeo (não só frames)** | Eddie AI casa transcript de fala com cena visual; um único frame pode perder contexto temporal. | **Nenhum dos 3.** Solução: extrair N frames por clip e fazer pooling, OU usar CLIP4Clip / CLIP2Video / NarVid (2025) por cima. |
| **ASR para transcript matching** | O input do persona é transcript de fala. Precisa Whisper antes do retrieval. | Nenhum — usar `whisper.cpp` ou `faster-whisper`. |
| **Scene segmentation com timestamps** | B-roll precisa retornar trecho, não vídeo inteiro. | Nenhum — usar PySceneDetect + Whisper segment timestamps + chunk de ~30s ([RAG video pipeline 2025](https://arxiv.org/pdf/2503.05186)). |
| **Frame-level captioning para boost de retrieval** | NarVid mostra que captions geradas frame-by-frame melhoram R@1. | Nenhum — usar VLM tipo Qwen2-VL ou LLaVA-1.6 (que internamente usa SigLIP). |
| **Re-ranking pós-ANN** | Top-100 do FAISS pode trazer ruído; rerank com cross-encoder visual sobe R@1. | Nenhum — adicionar cross-encoder tipo BLIP-2/Qwen2-VL-2B. |
| **Filtragem de NSFW / direitos autorais** | Biblioteca pessoal pode conter material privado. | Nenhum — pipeline aplicacional, não modelo. |
| **CoreML pipeline pronto para Mac** | Apple Neural Engine = 5-10× speedup. | Apple MobileCLIP cobre, mas está fora dos 3 subjects. **Considerar como complemento.** |

## Recomendação combinatória

Para o persona, a **stack mínima viável** vai além do visual encoder:

```
Pipeline B-Roll Finder OSS (proposta)
├── Ingest
│   ├── Whisper.cpp (transcript + timestamps)
│   ├── PySceneDetect (cut points)
│   └── Frame extraction (N=3-5 por scene)
├── Embedding (este bench)
│   ├── DEFAULT: OpenCLIP ViT-L/14 (DataComp-XL) — Chroma nativo
│   └── ALT (PT-pesado): SigLIP 2 base/multilingual via wrapper
├── Index
│   ├── ChromaDB (default) ou LanceDB (multimodal)
│   └── pgvector se já houver Postgres
└── Query
    ├── Transcript chunk → text embedding
    ├── ANN top-K
    └── (opcional) rerank com VLM (Qwen2-VL-2B)
```

## Decisão final por gap

- **Multilingual gap (PT-BR):** se >30% dos prompts forem PT-BR, **SigLIP 2 vence**. Caso contrário, OpenCLIP + tradutor é OK.
- **Ecosystem gap:** se o persona quer protótipo em fim de semana, OpenCLIP + Chroma. Se aceita 2-3 dias extras de wrapper, SigLIP 2 entrega melhor retrieval.
- **License gap:** se deploy for público (substituto comercial do Eddie AI), evitar CLIP OpenAI; SigLIP 2 (Apache 2.0) é o mais defensivo.

## Fontes

Ver `comparison-matrix.md`, `inventory-*.md` e `executive-report.md` para citações.
