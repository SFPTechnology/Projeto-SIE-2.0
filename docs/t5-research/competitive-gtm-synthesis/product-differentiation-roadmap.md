# Product Differentiation Roadmap — O que construir que incumbentes não copiam fácil

**Data:** 2026-05-06
**Lente:** features que (a) atacam gap categórico, (b) defensáveis por 12+ meses, (c) factíveis com OSS stack já mapeado em `docs/bench/`.
**Ranking critério:** moat depth × time-to-build (priorizar quadrante moat alto + build curto).

---

## Matriz Moat × Time-to-Build

```
Moat depth
    ↑
ALTO│  PT-BR-deep            Mobile companion
    │  Flat transparent      Multicam VLM (12-18m)
    │  pricing
    │
    │  Personal library      OSS-friendly stance
    │  semantic search
    │
MED │  Templates BR          LATAM payments
    │  culturalmente-nativos (Pix, boleto)
    │
    │  Community-driven      
    │  template library
    │
BAIXO└──────────────────────────────────────────→ Time-to-build
       <30d        30-90d         90-180d       180d+
```

---

## Feature 1 — PT-BR-deep (não tradução)  ⭐ CORE DIFFERENTIATOR

### Moat depth: 90
### Time-to-build: 60–90 dias

### Definição
**Não é "Submagic em português".** É uma camada produto que entende **pt-BR culturalmente** — gírias regionais, sotaques, linguagem brasileira de creator economy, idioms ("tá ligado", "mano", "véi", "pae", "dá um migué").

### Sub-componentes
| # | Sub-feature | Implementação | Status OSS |
|---|-------------|---------------|------------|
| 1 | ASR PT-BR com gíria regional | WhisperX + custom fine-tuning em corpus PT-BR | `docs/bench/whisper-engines/` Pick: WhisperX |
| 2 | Disfluências + hesitações capturadas | Word-ts ±50ms (WhisperX) | já entrega |
| 3 | Template captions "estilo Casimiro" | Sob licença genérica (não usar nome/likeness sem opt-in) | custom CSS/animation |
| 4 | Template captions "estilo Felipe Neto" | idem | idem |
| 5 | Template captions "estilo Whindersson" | idem | idem |
| 6 | Hooks PT-BR generator | LLM fine-tuned em corpus de hooks BR (TikTok, Reels) | Llama 3.1 + dataset próprio |
| 7 | Voice cloning PT-BR (Phase 2) | ElevenLabs API ou Bark fine-tuned | Phase 2 |

### Por que defensável
- Submagic teria que **deletar política de "tradução de UI"** e tratar PT-BR como mercado primário — que conflita com incentivo de afiliados anglófonos.
- Eddie processou áudio em PT mas UI em EN — **decisão deliberada** de positioning premium global.
- Descript's Underlord/Studio Sound/Overdub são marketing-driven feature names em EN; localizar = refazer brand.

### Validação
- 10 creators PT-BR entrevistados em D-30 a D-7 testam acurácia.
- Bench interno: 100 áudios reais (entrevista, podcast, vlog, live BR) com WER manual <8%.

---

## Feature 2 — Flat Transparent Pricing (commitment-as-feature)

### Moat depth: 85
### Time-to-build: 30 dias (engenharia de billing + workflows)

### Definição
**Pricing flat sem AI Credits + 8 commitments públicos contratuais (refund 30d, aviso 7d, 1-clique cancel, proration honesta, Pix/boleto, NF-e, suporte PT-BR <24h).**

Detalhe completo em `pricing-strategy.md`.

### Por que defensável
- Submagic ganha $1.6M acumulados em afiliados via 30% recurring habilitado por LTV alto pelo auto-renew silencioso. **Mexer destrói o motor.**
- Eddie pricing 8× é **decisão de positioning** — flatten = capitulação.
- Descript AI Credits são literalmente como cobrar inferência. **Flatten = gross margin negative em power users.**

### Implementação
- Stripe webhooks para email 7d-pre-renewal.
- Self-service cancellation page com 1 clique (não dark pattern multi-step).
- Pro-rata calc no upgrade (Stripe API nativo).
- Refund automático até 30 dias (Stripe + customer portal).
- NF-e Brasil via Conta Azul/Bling/iugu integrações.
- Pix/boleto via Pagar.me/Stripe BR.

### Compromissos públicos (literais)
ver `pricing-strategy.md` §5 — 8 commitments para landing.

---

## Feature 3 — Personal Library Semantic Search (own o gap "Eddie B-Roll Finder")

### Moat depth: 75
### Time-to-build: 90–120 dias

### Definição
**Upload sua biblioteca pessoal de B-roll/clips/photos → search semântico via VLM** ("encontra todos os clipes onde aparece praia ao pôr do sol falando sobre business").

Eddie tem isso como Pro tier feature. Nós entregamos no Creator tier R$69.

### Stack OSS (já mapeado)
- **Bench `docs/bench/visual-embedding-models/executive-report.md`:**
  - **Default:** OpenCLIP ViT-L/14 DataComp-XL (428M params, 768-dim, MIT, ChromaDB nativo).
  - **Fallback multilingual:** SigLIP 2 base (Apache 2.0, 86M params, PT-BR nativo).
- **Frame extraction:** PySceneDetect.
- **Vector DB:** ChromaDB ou pgvector(768).

### Por que defensável
- Eddie é desktop-only — sua library fica no disco do usuário. Cloud-first dá UX superior.
- Submagic não tem semantic search de library pessoal (`docs/bench/submagic-vs-eddie-ai/executive-report.md` Finding #2).
- Descript tem search de transcript, não de visual.

### UX nova
- "Pergunta em PT-BR": *"mostra os clipes onde eu falo sobre vendas e tem prédio ao fundo"*.
- Combine VLM (visual) + Whisper transcript (text) num único query.

---

## Feature 4 — Mobile Companion App (iOS first)

### Moat depth: 70
### Time-to-build: 180+ dias

### Definição
- iOS app para **capture + quick edit + upload**.
- Web/desktop para **finalização + multicam + export**.
- Sync seamless via cloud.

### Por que defensável
- Eddie é desktop-only (decisão arquitetural).
- Descript admite "no mobile editing app" (`descript.../audience-truth.md` Pattern #6).
- Submagic é web-only (mobile responsive ≠ mobile native).
- CapCut tem mobile mas não é AI-first.

### Roadmap
- Mês 0–6: web MVP.
- Mês 6–9: iOS capture + sync companion.
- Mês 9–12: iOS standalone edit.
- Mês 12+: Android.

Detalhe em `distribution-blueprint.md` Canal 7.

---

## Feature 5 — LATAM Payment Methods (Pix, boleto, parcelado)

### Moat depth: 60
### Time-to-build: 30 dias (integração)

### Definição
- **Pix** instant payment (preferred BR).
- **Boleto bancário** (PJ + cidades sem cartão).
- **Cartão parcelado em até 12× sem juros** até R$300/mês.
- **NF-e brasileira** auto-emitida.
- **Pricing em BRL/MXN/ARS** lado-a-lado com USD.

### Stack
- **Pagar.me / iugu / Asaas** para Pix + boleto + cartão BR.
- **Conta Azul / Bling** para NF-e.
- **Stripe** mantém para card internacional.

### Por que defensável
- Submagic/Eddie/Descript não emitem NF-e brasileira → **bloqueado em compliance corporativa BR**.
- Pix tem 0% taxa para o cliente, parcela mental como "barato".
- Mexer em sistema de billing para suporte BR é trabalho técnico real (90+ dias) que ninguém vai fazer só pela TAM BR isolada.

---

## Feature 6 — Community-Driven Template Library

### Moat depth: 55
### Time-to-build: 60 dias

### Definição
- Marketplace dentro do app de **templates de captions/transitions/B-roll/hooks** criados por creators.
- Creator submete → community vota → top 100 viram free, top 1000 ficam pagos (creator ganha 70/30 split).

### Por que defensável
- Submagic tem templates curados internos, não open marketplace.
- Network effect: mais creators = mais templates = mais valor = mais creators.
- Discord (Canal 6) feeds o marketplace organicamente.

### Risco
- UGC moderation custa.
- Spam/baixa qualidade.

### Mitigação
- Curation tier 1 (manual approval).
- Vote-up/down community-driven.
- Featured weekly por community manager.

---

## Feature 7 — OSS-Friendly Stance (tie to bench)

### Moat depth: 50
### Time-to-build: contínuo

### Definição
Sinkra **não é OSS** (decisão deliberada), mas adota **postura OSS-friendly**:
- Stack interna OSS-native (WhisperX, OpenCLIP/SigLIP, OpenShorts fork — `docs/bench/`).
- Contribui upstream em libs críticas.
- Publica `@sinkra/*` packages OSS (`@sinkra/whisper-captions`, `@sinkra/viral-moment-detector`, `@sinkra/smart-reframe` — sugerido em `docs/bench/oss-shortform-pipelines/executive-report.md` Fase 4).
- Self-host option no tier Pro/Agency (Docker compose).

### Por que defensável
- Submagic é closed-source SaaS, sem stack visível.
- Eddie é desktop proprietary.
- Descript é cloud closed.
- **Postura OSS-friendly atrai dev community + creator-coder + reduce CAC** (organic discovery via GitHub stars).

### Risco
- Open-source canibaliza receita?
- **Não.** Modelo: stack interna OSS, mas curation + UX + suporte + brand = closed product. Mesmo padrão de WordPress (OSS) vs WP Engine (managed).

---

## Feature 8 — Multicam VLM-decisionado (Phase 2)

### Moat depth: 90
### Time-to-build: 12–18 meses (R&D)

### Definição
Eddie usa audio peaks para multicam — falha em ambientes diferentes (`eddie-ai.../audience-truth.md` Padrão #2 confirma com Durlach docuseries).

Sinkra faz **face detection + lip sync + VLM** decidir "quem está falando agora" e cortar para essa câmera.

### Por que defensável
- Requer R&D de 12+ meses.
- Stack: face detection (MediaPipe/YOLO) + lip sync model + VLM (Qwen2-VL, LLaVA-Next).
- Não-trivial mesmo para Eddie atacar de volta.

### Quando lançar
- **Não no D-1.** Foco no PT-BR-deep + Flat pricing primeiro.
- Phase 2 (mês 12+) como differentiator técnico para Pro/Agency tier.

---

## Anti-features (NÃO construir)

| Feature | Por que NÃO |
|---------|-------------|
| Voice cloning próprio | ElevenLabs commoditizou; integrar via API. |
| Eye contact AI | Submagic já dominou; ROI marginal. |
| AI avatars | Mercado fragmentado (HeyGen, Synthesia); foco. |
| Stock library curada | Capex pesado; integrar Pexels/Pixabay (gratuito). |
| Cinematic LUTs | Vocabulário NLE; afasta nosso ICP. |
| Live streaming (RecordRT) | Riverside já dominou. |
| Podcast hosting | Anchor/Spotify dominam. |

---

## Roadmap consolidado (12 meses)

```
Mês 0-3   ┌──── PT-BR-deep MVP (ASR + captions + hooks BR)
          │     Flat pricing + 8 commitments
          │     Discord PT-BR + LATAM payments (Pix)
          │
Mês 3-6   ┝──── Personal library semantic search
          │     Free tools wedge (3 ferramentas)
          │     SEO 30 posts publicados
          │
Mês 6-9   ┝──── iOS companion app
          │     Multi-brand kit (Agency tier)
          │     Community template library
          │
Mês 9-12  ┝──── iOS standalone edit
          │     OSS packages publishing (@sinkra/*)
          │     NF-e + contrato PT-BR enterprise-ready
          │
Mês 12+   └──── Multicam VLM-decisionado (Phase 2)
                ES-LATAM expansion
                Android app
```

---

## Síntese — top 5 features priorizadas

| Rank | Feature | Moat | Time | Por que rank |
|------|---------|------|------|--------------|
| 1 | **PT-BR-deep** | 90 | 60–90d | Core differentiator. Permite tudo. |
| 2 | **Flat pricing + 8 commitments** | 85 | 30d | Trust + viral conteúdo + afiliado-friendly. |
| 3 | **LATAM payments + NF-e** | 60 | 30d | Bloqueia compliance dos incumbentes. |
| 4 | **Personal library semantic search** | 75 | 90–120d | Own o territory Eddie B-Roll Finder. |
| 5 | **iOS companion app** | 70 | 180d | Future-proof; ICP-1 é mobile-first. |

---

## Fontes
- `docs/bench/submagic-vs-eddie-ai/executive-report.md`
- `docs/bench/whisper-engines/executive-report.md`
- `docs/bench/oss-shortform-pipelines/executive-report.md`
- `docs/bench/visual-embedding-models/executive-report.md`
- `outputs/spy/research/competitive-gtm-synthesis/categorical-gap-map.md`
- `outputs/spy/research/competitive-gtm-synthesis/pricing-strategy.md`
- `outputs/spy/research/eddie-ai-marketing-deepdive/audience-truth.md`
- `outputs/spy/research/descript-marketing-deepdive/audience-truth.md`
