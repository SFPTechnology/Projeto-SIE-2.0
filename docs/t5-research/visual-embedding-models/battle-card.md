# Battle Card — SigLIP / OpenCLIP / CLIP

> Decisão rápida para o builder do B-Roll Finder OSS.

## TL;DR

| Cenário | Escolha |
|---|---|
| Default sólido, EN-pesado, ChromaDB | **OpenCLIP ViT-L/14 (DataComp-XL)** |
| Multilingual (PT-BR + EN) ou licença Apache 2.0 obrigatória | **SigLIP 2 base ou L (multilingual)** |
| Acurácia máxima sem orçamento de hardware | OpenCLIP bigG/14 (2.5B) — **só Linux GPU** |
| Reproduzir paper de 2021 ou baseline | CLIP OpenAI ViT-L/14 |
| Mac M1/M2 com biblioteca <50k frames | SigLIP 2 B/16 OU OpenCLIP ViT-L/14 — ambos viáveis em ~horas |

## One-liner por modelo

- **SigLIP 2** — *"State-of-the-art retrieval com multilingual nativo e licença Apache 2.0; tooling em vector DB ainda é DIY."*
- **OpenCLIP** — *"Padrão de mercado OSS — Chroma nativo, LanceDB nativo, milhares de tutoriais; mas EN-only e disclaimer LAION-5B."*
- **CLIP OpenAI** — *"Histórico, soft-deprecated, licença dos pesos ambígua; baseline acadêmica apenas."*

## Quando usar cada um

### SigLIP 2 — usar se:
- ✓ Prompts em PT-BR são >30% do tráfego
- ✓ Deploy comercial sem ambiguidade legal é requisito
- ✓ Acurácia em retrieval (R@1) é o KPI
- ✓ Tem tempo para escrever wrapper de Chroma/LanceDB

### OpenCLIP — usar se:
- ✓ Stack já é ChromaDB ou LanceDB
- ✓ Prompts são ~100% EN (ou tradução automática é aceitável)
- ✓ Time é solo e quer protótipo no fim de semana
- ✓ Precisa de DataComp-XL para 79.2% ImageNet com modelo "pequeno" (428M)

### CLIP OpenAI — usar se:
- ✓ Tarefa é reproduzir resultado de paper de 2021
- ✓ Compatibilidade com pipeline legado que hardcoda `openai/clip-vit-large-patch14`
- ✗ **Não usar para nova produção**

## Quando NÃO usar cada um

### NÃO usar SigLIP 2 se:
- Persona quer plug-and-play em ChromaDB hoje sem código wrapper
- Stack depende de `OpenCLIPEmbeddingFunction` em integrações já existentes
- Latência de 1B params (variante g) seria proibitiva em hardware modesto

### NÃO usar OpenCLIP se:
- Multilingual PT-BR é requisito core
- Licença Apache 2.0 explícita é obrigatória (compliance enterprise)
- Compliance proíbe LAION-5B uncurated (disclaimer NSFW residual)

### NÃO usar CLIP OpenAI se:
- Está construindo algo novo em 2026 (não use)

## Killer features

| Recurso | SigLIP 2 | OpenCLIP | CLIP OpenAI |
|---|---|---|---|
| Sigmoid loss (estabilidade em batch pequeno) | ✓ | — | — |
| Multilingual nativo (>100 idiomas) | ✓ (v2 default) | parcial (XLM-R variant) | — |
| NaFlex (resolução dinâmica) | ✓ | — | — |
| Self-distillation + masked prediction | ✓ (v2) | — | — |
| ChromaDB nativo | — | ✓ | parcial |
| LanceDB nativo | — | ✓ | — |
| LAION-5B / DataComp-XL training | — | ✓ | — |
| Sweet spot 428M-L/14 com R@1 alto | ~ | ✓ (DataComp-XL) | — |
| Apache 2.0 nos pesos | ✓ | — (MIT com disclaimer) | — (out of scope) |
| Origem histórica / paper canônico | — | — | ✓ |

## Tabela de checkpoint específico recomendada

| Persona | Checkpoint | Motivo |
|---|---|---|
| **B-roll OSS, PT-BR, Mac M2/M3** | `google/siglip2-base-patch16-256` | 86M, multilingual, ~88ms/img MPS, Apache 2.0 |
| B-roll OSS, EN, Mac, Chroma | `laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90K` | 428M, 79.2% ImageNet, integração nativa |
| B-roll OSS, EN, máxima acurácia, Linux GPU | `laion/CLIP-ViT-bigG-14-laion2B-39B-b160k` | 2.5B, 80.1% ImageNet, 74.9% R@5 COCO |
| B-roll OSS, multimodal-via-VLM | `google/siglip2-so400m-patch14-384` | Backbone de VLMs modernos (Qwen2-VL etc.) |
| Reproduzir paper 2021 | `openai/clip-vit-large-patch14` | Baseline canônica |

## Custos de migração (se trocar depois)

- **OpenCLIP → SigLIP 2:** baixo. Embedding dim muda (768→768 para B, 1024 para L), reindexar é 1 pipeline. Wrapper Chroma a escrever.
- **SigLIP 2 → OpenCLIP:** baixo. Reverso.
- **CLIP → OpenCLIP:** mínimo. Mesmo tokenizer/arch.
- **Qualquer → CLIP:** improvável, não recomendado.

## Riscos por escolha

| Escolha | Risco | Probabilidade | Mitigação |
|---|---|---|---|
| OpenCLIP | Persona terá usuários PT-BR e qualidade visual cair | Média | Tradutor automático no input layer; fallback SigLIP 2 |
| SigLIP 2 | Wrapper Chroma exige debug | Baixa | Notebook Merve Noyan + 30 linhas de código |
| CLIP OpenAI | Licença dos pesos contestada | Baixa-média | Não usar |
| bigG/14 | Indexação trava Mac | Alta se forçado em Mac | Indexar em Linux GPU; servir embedding já calculado |

## Quote do persona (decisão final)

> *"Eu sou solo dev, B-roll é meu, prompts são mistos PT/EN, e quero shipar em uma semana. ChromaDB já está no roadmap. Vou começar com OpenCLIP ViT-L/14 DataComp-XL para o protótipo, e na v2 adiciono SigLIP 2 como segundo backend opcional para queries multilingual."*

## Fontes

- Ver `comparison-matrix.md` e `executive-report.md`.
