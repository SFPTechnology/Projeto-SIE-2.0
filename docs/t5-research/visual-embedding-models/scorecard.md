# Scorecard — SigLIP / OpenCLIP / CLIP

> Escala 0-100. Composite simples (equal weight) + persona-weighted (OSS B-Roll Finder).
> Persona weights: **Maturity 0.15 · Ecosystem 0.15 · DX 0.20 · Performance 0.25 · Scalability 0.10 · Community 0.15**.
> Performance e DX recebem peso maior porque o persona é um builder solo, indexando sua própria biblioteca.

## Tabela base

| Dimensão | SigLIP / SigLIP 2 | OpenCLIP | CLIP (OpenAI) |
|---|---:|---:|---:|
| **Maturity** | 78 | 92 | 85 |
| **Ecosystem** | 72 | 95 | 70 |
| **DX (developer experience)** | 80 | 88 | 70 |
| **Performance** (acurácia × latência) | 92 | 85 | 65 |
| **Scalability** (escolha de tamanhos) | 85 | 90 | 60 |
| **Community** (atualizações, tutoriais, issues) | 80 | 92 | 55 |
| **Composite (equal weight, /100)** | **81.2** | **90.3** | **67.5** |
| **Persona-weighted (B-roll OSS)** | **83.0** | **88.4** | **67.0** |

## Cálculo persona-weighted

`Score = 0.15·Maturity + 0.15·Ecosystem + 0.20·DX + 0.25·Performance + 0.10·Scalability + 0.15·Community`

| Modelo | Cálculo | Total |
|---|---|---:|
| SigLIP 2 | 0.15·78 + 0.15·72 + 0.20·80 + 0.25·92 + 0.10·85 + 0.15·80 | **83.0** |
| OpenCLIP | 0.15·92 + 0.15·95 + 0.20·88 + 0.25·85 + 0.10·90 + 0.15·92 | **88.4** |
| CLIP OpenAI | 0.15·85 + 0.15·70 + 0.20·70 + 0.25·65 + 0.10·60 + 0.15·55 | **67.0** |

## Justificativa por dimensão

### Maturity

- **OpenCLIP 92** — 4+ anos em produção, milhares de pipelines documentados, scaling laws paper publicado em CVPR.
- **CLIP OpenAI 85** — paper original, citação canônica, repo estável (mas sem novas releases).
- **SigLIP 2 78** — lançado fev/2025 (SigLIP v1 em 2023). Ainda menos battle-tested que OpenCLIP, mas Google é maintainer ativo e a v2 já corrigiu lacunas reportadas.

### Ecosystem

- **OpenCLIP 95** — `OpenCLIPEmbeddingFunction` nativo no ChromaDB, integração oficial LanceDB, suporte clip-retrieval, Harper Reed e dezenas de blog posts. Padrão de fato.
- **SigLIP 2 72** — notebook FAISS oficial Merve Noyan, mas sem wrapper nativo em vector DBs. Ainda exige código custom.
- **CLIP OpenAI 70** — funciona em todo lugar via `transformers`, mas ninguém constrói novo pipeline em cima dele.

### DX (developer experience)

- **OpenCLIP 88** — `open_clip.create_model_and_transforms()` em uma linha, suporte HF, peso de model cards bem documentados.
- **SigLIP 2 80** — `AutoProcessor` + `SiglipModel.get_image_features()` é direto. Pegadinha do `padding="max_length"` exige cuidado.
- **CLIP OpenAI 70** — repo `pip install git+...` simples, mas tooling não evoluiu desde 2022; integração com vector DBs sempre indireta.

### Performance (acurácia × latência)

- **SigLIP 2 92** — vence em retrieval (R@1 COCO B/16 = 81.7 T→I, contra 68.3 do CLIP OpenAI), iguala/supera OpenCLIP em ImageNet zero-shot. Latência razoável (B/16 ~88ms/img em M1 Pro MPS).
- **OpenCLIP 85** — bigG é o melhor zero-shot ImageNet OSS (80.1%), mas custa 2.5B params; ViT-L DataComp-XL (79.2%) é o sweet spot.
- **CLIP OpenAI 65** — perde em todos os benchmarks recentes; baseline 75.4% ImageNet.

### Scalability (variantes / dimensionamento)

- **OpenCLIP 90** — 6+ escalas × 3-4 datasets de treino (LAION-2B, DataComp-XL, CommonPool-XL).
- **SigLIP 2 85** — 4 escalas (B/L/So400m/g) × FixRes/NaFlex × multilingual.
- **CLIP OpenAI 60** — apenas 4 ViT + ResNets antigos.

### Community

- **OpenCLIP 92** — repo mlfoundations + LAION discord ativos, issues respondidas, novos checkpoints frequentes.
- **SigLIP 2 80** — Google publica papers/checkpoints, HF discussions ativas, mas ritmo menor.
- **CLIP OpenAI 55** — issues abertas sem resposta, sem releases novas. **Soft-deprecated.**

## Visualização

```
Persona-weighted score (B-roll OSS):

OpenCLIP    ████████████████████████████████████████████  88.4
SigLIP 2    ██████████████████████████████████████████    83.0
CLIP OpenAI █████████████████████████████████             67.0
                                              0   25   50   75  100
```

## Sensibilidade a peso

- Se **multilingual peso ↑** (ex.: 30% do critério Performance é multilingue): SigLIP 2 ultrapassa OpenCLIP. Persona PT-BR-pesado deve recalibrar.
- Se **Ecosystem peso ↑** (ex.: 0.30): OpenCLIP amplia liderança.
- Se **License clarity peso ↑**: SigLIP 2 ganha vantagem (Apache 2.0 limpo vs MIT-com-disclaimer).

## Veredicto

OpenCLIP lidera por **margem estreita** no composite por força de ecossistema. SigLIP 2 é a escolha vencedora se o persona prioriza **multilingual ou licença limpa**. CLIP OpenAI é base de comparação, não candidato.

## Fontes

Ver `comparison-matrix.md` e inventários individuais para citações completas.
