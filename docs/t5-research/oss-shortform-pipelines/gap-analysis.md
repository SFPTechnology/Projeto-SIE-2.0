# Gap Analysis — OSS vs Submagic Pro

**Baseline:** Submagic Pro (referência do bench `docs/bench/submagic-vs-eddie-ai/`).
**Objetivo:** mapear, por OSS, o que falta para paridade com Submagic Pro daily use.

---

## OpenShorts — Gaps vs Submagic Pro

### O que JÁ tem paridade ou supera Submagic
- Auto-captions word-level com styling (paridade)
- B-roll automático (paridade — usa AI gen ao invés de stock)
- Highlight clipping de podcast (paridade — Gemini 3.0 Flash)
- 9:16 smart reframe com face tracking (paridade)
- Hook overlays AI-generated (paridade)
- Multi-platform schedule + publish (paridade — Upload-Post)
- AI Avatar / UGC (**supera** Submagic — feature de outro tier comercial)
- Watermark zero (**supera** — Submagic free tem watermark)
- Voice dubbing 30+ idiomas (paridade — ElevenLabs)
- Self-hosted, dados privados (**supera** — feature inviável em SaaS)

### Gaps reais
| Gap | Severidade | Mitigação |
|---|---|---|
| **Sem template/preset library de captions** | Média | Submagic tem dezenas de presets visuais; OpenShorts permite styling mas não tem catálogo curado. **Mitigação:** criar catálogo `subtitles_presets.json` no fork |
| **Sem A/B testing de hooks integrado** | Baixa | Submagic gera variações e mostra heatmap; OpenShorts gera 1 hook por vídeo. **Mitigação:** loop de N gerações no fork |
| **Sem analytics de performance pós-publish** | Média | Submagic conecta com TikTok/YT analytics; OpenShorts publica e fim. **Mitigação:** integração TikTok Display API no fork |
| **Sem mobile app / mobile-friendly UI** | Média | UI é desktop React; Submagic tem app iOS. **Mitigação:** PWA mobile no roadmap fork |
| **Sem editor de timeline manual** | Alta | Submagic permite editar caption-por-caption visualmente; OpenShorts é mais "gerar e accept". **Mitigação:** Remotion já está no projeto — extender editor |
| **Custo variável $0,65-2/short** | Alta | Submagic é flat $20-50/mo. Em escala >50 vídeos/mês, OpenShorts pode sair mais caro. **Mitigação:** swap fal.ai por providers mais baratos no fork (Kling/Wan2/SVD) |
| **Sem free trial integrado** | Baixa | Onboarding tem fricção (4 keys). **Mitigação:** Sinkra Hub pode pré-provisionar |
| **Pipeline AI Shorts é EN/ES first** | Média | Scripts gerados são EN/ES; PT-BR não é first-class. **Mitigação:** trocar prompts para Gemini PT-BR |

**Verdict OpenShorts vs Submagic:** **paridade em ~80% das features**, supera em 3 (UGC, watermark, self-host), perde em editor visual de timeline + analytics + presets curados.

---

## MoneyPrinterTurbo — Gaps vs Submagic Pro

### O que JÁ tem
- Geração de vídeo end-to-end automatizada (mas a partir de **tema**, não de vídeo longo)
- Captions estilizadas
- TTS multi-provider
- Geração 9:16 e 16:9
- Batch generation
- Watermark zero

### Gaps fundamentais
| Gap | Severidade | Mitigação |
|---|---|---|
| **Não corta vídeo longo em shorts** | **CRÍTICA** | Pipeline é tema → vídeo, não vídeo → shorts. **Sem mitigação simples** — mudaria a arquitetura |
| **Não detecta viral moments** | **CRÍTICA** | Não há highlight detection. **Sem mitigação** sem reescrever pipeline |
| **B-roll só de stock Pexels** | Alta | Visualmente repetitivo em escala. **Mitigação:** plugar Flux/Wan2 no `material.py` |
| **Sem AI avatar / UGC** | Média | Não tem talking head. **Mitigação:** integrar VEED Lipsync |
| **Sem reframe inteligente** | Baixa | Já gera 9:16, mas se input é 16:9 não reframe. **Mitigação:** plugar mediapipe |
| **Sem schedule de publishing** | Média | upload_post.py existe mas docs removidos. **Mitigação:** restaurar do histórico |
| **ImageMagick external dep** | Alta | DX ruim em Windows. **Mitigação:** swap por Pillow puro (forks já fazem) |
| **Sem hook overlays animados** | Alta | Faltam atenção overlays estilo Submagic |
| **Sem editor visual** | Alta | Streamlit é form-based, não editor |

**Verdict MoneyPrinterTurbo vs Submagic:** **paridade em ~30% do escopo Submagic.** Categoria diferente — substitui MoneyPrinterV1 / faceless YouTube, não Submagic. Útil como **componente** de pipeline próprio (TTS multi-provider, LLM agnostic).

---

## Captacity — Gaps vs Submagic Pro

### O que tem
- Captions word-level com highlight
- Stroke + shadow customizável
- CLI simples

### Gaps
| Gap | Severidade |
|---|---|
| **Sem cortar vídeo** | CRÍTICA |
| **Sem viral detection** | CRÍTICA |
| **Sem B-roll** | CRÍTICA |
| **Sem reframe** | CRÍTICA |
| **Sem TTS** | CRÍTICA |
| **Sem publish** | CRÍTICA |
| **Sem manutenção** (0 commits 365d) | CRÍTICA |
| **Bug com openai SDK >=1.0** | Alta |
| **Sem RTL/multi-script** | Média |

**Verdict Captacity vs Submagic:** **paridade em <10%.** Não é pipeline, é uma capability de uma única camada. **Não substitui Submagic em nenhum cenário.**

---

## Resumo Cross-Repo

| Categoria de gap | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|---|---|---|
| **Architecture-level (pipeline shape errado)** | 0 | **3 críticos** (não corta, não detecta highlight, B-roll só stock) | **6 críticos** |
| **Feature-level (gap dentro do pipeline correto)** | 5 médios + 2 altos | 4 altos | N/A |
| **Manutenção / saúde** | 0 | 0 | **1 crítico (abandono)** |
| **DX / Setup** | 0 | 1 alto (ImageMagick) | 0 |
| **Custo unitário** | 1 alto ($0,65-2/short) | 0 | 0 |

**Síntese:** apenas **OpenShorts** tem a forma certa de pipeline para o use case Submagic. MPT é categoria diferente; Captacity é abandonado e parcial.
