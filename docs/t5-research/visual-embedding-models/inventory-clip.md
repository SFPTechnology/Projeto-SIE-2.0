# Inventário — CLIP (OpenAI original)

> Lente: visual backbone para um substituto OSS do **B-Roll Finder** do Eddie AI.

## Linhagem

CLIP foi anunciado pela OpenAI em **jan/2021** ([blog](https://openai.com/index/clip/)). Treinado em **WIT-400M** (dataset privado da OpenAI). Repositório canônico: [openai/CLIP](https://github.com/openai/CLIP).

## Checkpoints disponíveis

| Variante | Params | Embedding dim | ImageNet zero-shot top-1 | Fonte |
|---|---|---|---|---|
| RN50 | 102M | 1024 | ~59.6% | OpenAI repo |
| RN101 | 119M | 512 | ~62.2% | idem |
| RN50x4/16/64 | varia | 640-1024 | 70.2-73.6% | idem |
| ViT-B/32 | 151M | 512 | **63.3%** | [HF clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32) |
| ViT-B/16 | 150M | 512 | **68.1%** | [analyticsvidhya](https://www.analyticsvidhya.com/blog/2024/09/clip-vit-l14/) |
| **ViT-L/14** | **428M** | **768** | **75.4%** | [HF clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14) |
| ViT-L/14@336px | 428M | 768 | ~76.6% | OpenAI repo |

## Licença — ambígua

- **Código (`openai/CLIP` repo) — MIT.** ([LICENSE](https://github.com/openai/CLIP/blob/main/LICENSE))
- **Pesos do modelo:** OpenAI model card declara *"Any deployed use case of the model — whether commercial or not — is currently out of scope."*
- **Tensão jurídica:** discussão pública contínua em 2024-2025 sobre se MIT no código se estende aos pesos. Não há nota oficial fechando a questão. ([HF discussão #21](https://huggingface.co/openai/clip-vit-large-patch14/discussions/21) · [GitHub issue #203](https://github.com/openai/CLIP/issues/203))
- **Implicação prática:** uso comercial é **legal-cinzento** — comunidade trata como permitido, mas há risco residual. **OpenCLIP e SigLIP 2 não têm essa ambiguidade.**

## Status de manutenção

- Repositório `openai/CLIP` **não está formalmente arquivado nem deprecado** publicamente. Última atividade significativa em 2021-2022 (commits esporádicos depois).
- **Desenvolvimento ativo migrou para OpenCLIP** ([mlfoundations/open_clip](https://github.com/mlfoundations/open_clip)), que reimplementa e estende com novos datasets/escalas. Próprio README do OpenCLIP confirma que *"portions of src/open_clip/ modelling and tokenizer code are adaptations of OpenAI's official repository."*
- **Veredicto:** **soft-deprecated** de fato. Usar apenas para reprodução de paper original ou baseline histórica.

## Acurácia retrieval

CLIP ViT-L/14 em COCO (R@1) — usado como baseline em [arXiv 2502.14786](https://arxiv.org/abs/2502.14786) — Tabela comparativa SigLIP 2:

| Direção | CLIP ViT-L | SigLIP 2 B/16 |
|---|---|---|
| I→T R@1 | 61.9 | **69.7** |
| T→I R@1 | 68.3 | **81.7** |

CLIP ViT-L/14 em ImageNet zero-shot: **75.4%** ([analyticsvidhya 2024](https://www.analyticsvidhya.com/blog/2024/09/clip-vit-l14/)).

## Multilingue / Português

**Não suportado nativamente.** Tokenizer BPE treinado majoritariamente em texto EN. Para multilingue, usar `sentence-transformers/clip-ViT-B-32-multilingual-v1` que é um destilado knowledge-distilled multilingual em cima do mesmo backbone visual. Mas isso não é "OpenAI CLIP original" — é um wrap derivado.

## Integração FAISS / Chroma / pgvector

- Compatível via `transformers` (`CLIPModel`, `CLIPProcessor`).
- ChromaDB: usa por trás OpenCLIP (não OpenAI CLIP original) na embedding function nativa — mas o backbone é o mesmo, weights diferentes.
- FAISS/pgvector: trivial, embedding dim 512 (B) / 768 (L).

## Performance Apple Silicon

- **CounterAnimal benchmark:** CLIP-OpenAI-ViT/L/14 = 85.38% common / 70.28% counter (drop 15.10).
- Latência via MPS comparável ao OpenCLIP ViT-L/14 (mesma arquitetura). QuickGELU activation default → não-otimizada vs `torch.nn.GELU`. Substituir manualmente para ganhos.

## Pontos fortes

1. **Origem histórica** — paper original, citação canônica, baseline obrigatória em ablations.
2. **MIT no código** — sem disclaimer LAION-5B uncurated.
3. **Tooling enxuto** — repo simples, `pip install git+...`.
4. **Reprodutibilidade de paper** quando essa é a meta.

## Pontos fracos

1. **Acurácia ultrapassada** — perde em quase todos os benchmarks novos (ImageNet, COCO, Flickr) para OpenCLIP-DataComp e SigLIP 2.
2. **Licença dos pesos ambígua** — OpenAI model card diz "out of scope" para deploy comercial. Risco legal cinzento.
3. **Manutenção de fato encerrada** — sem novos checkpoints, sem novos datasets desde 2022.
4. **Não-multilingue** — pior dos 3 subjects para PT-BR.
5. **Sem variantes maiores** — ViT-L/14@336px é o teto. Para escalar precisão, sair para OpenCLIP/SigLIP é compulsório.

## Veredicto setorial

**Não usar como modelo principal em 2026.** OpenCLIP ViT-L/14 (DataComp-XL) é estritamente superior em acurácia E maturidade de ecossistema, com licença MIT inequívoca nos pesos. Manter o CLIP da OpenAI apenas como:

- Baseline em comparações de paper.
- Quando dependência de tooling legado exige.
- Compatibilidade com pipelines pré-2023 que hardcodem `openai/clip-vit-large-patch14`.

## Fontes

- [GitHub openai/CLIP](https://github.com/openai/CLIP)
- [OpenAI blog — CLIP announcement](https://openai.com/index/clip/)
- [LICENSE — MIT](https://github.com/openai/CLIP/blob/main/LICENSE)
- [HF clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)
- [HF clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32)
- [GitHub issue #203 — License question](https://github.com/openai/CLIP/issues/203)
- [HF discussion — License Request](https://huggingface.co/openai/clip-vit-large-patch14/discussions/21)
- [analyticsvidhya — CLIP ViT-L14 deep dive (2024)](https://www.analyticsvidhya.com/blog/2024/09/clip-vit-l14/)
- [arXiv 2403.11497 — Do CLIPs Always Generalize Better than ImageNet?](https://arxiv.org/html/2403.11497v1)
