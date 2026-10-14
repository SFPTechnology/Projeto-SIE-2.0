# Executive Report — Submagic vs Eddie AI

**Comparison type:** product
**Lens:** feature-extraction-for-OSS-substitution
**Date:** 2026-05-06
**Requested by:** Alan Nicolas (@oalanicolas)
**Confidence:** HIGH em features (multi-source); MEDIUM-HIGH em pricing (jan-mar/2026, pode ter shift em maio)

---

## Executive summary

Submagic e Eddie AI parecem competidores diretos na categoria "AI video editor" mas resolvem **problemas adjacentes, não os mesmos**:

- **Submagic** = Editor final de short-form (web, $24/mês, gera MP4 polido para TikTok/Reels/Shorts).
- **Eddie AI** = Assistente pré-edit profissional (desktop, $21-333/mês, gera XML para Premiere/Resolve/FCP).

Composite scores (0-100): **Submagic 82 / Eddie AI 76**. Mas leitura simplista — para a persona certa, qualquer um vence o outro por margem grande.

**Para a sua intenção declarada (caçar OSS substituto):** Eddie AI é dramaticamente mais clonável (~80% vs ~50% das features cobertas por OSS maduro). O motivo: Eddie produz **metadata** (XML, transcripts, embeddings, timestamps) que cada componente OSS já resolve bem. Submagic produz **vídeo renderizado** com polish premium (captions templates, eye contact, avatares) que requer curation + engineering pesados.

---

## 5 findings principais

### Finding 1 — Não escolha "um vs outro". Escolha o problema.

| Workflow | Ferramenta certa |
|---|---|
| Solo creator postando shorts | Submagic |
| Documentary com NLE workflow | Eddie AI |
| Híbrido (long → repurpose para shorts) | Eddie + Submagic em pipeline |

A categoria parece concorrência, é complementaridade.

### Finding 2 — A feature definidora "match imagem com fala" funciona diferente nos dois

- **Submagic** faz keyword/concept-based matching contra stock + library, **renderiza direto**.
- **Eddie AI** faz semantic search verdadeiro (CLIP-class) contra biblioteca pessoal, **sugere placement** e **delega render ao NLE**.

Para a sua descrição original ("editor que sobe imagem e divide a tela"), o **layout split-screen literal só existe em Submagic** (`split-50-50`, `split-35-65` como primitives nativos).

### Finding 3 — Pricing reflete o target

- Submagic: $0/$24/$54 — ferramenta de creator (democratizar).
- Eddie AI: $0/$21/$167/$333 — software pro com pulo de 8x para Pro tier (segmentar).

O pulo entre Plus e Pro do Eddie é a barreira psicológica que limita adoção mainstream.

### Finding 4 — Eddie AI é dramaticamente mais clonável em OSS

Stack OSS para clonar Eddie cobre ~80% das features:
```
WhisperX (ASR + word timestamps)
+ pyannote.audio (diarization)
+ SigLIP / OpenCLIP (visual recognition)
+ ChromaDB / pgvector (vector search)
+ Ollama + Llama 3.1 (chat-prompt edit)
+ OpenTimelineIO (XML export Premiere/Resolve/FCP)
```
Effort estimado: ~80h para MVP, ~300h para qualidade Plus tier.

Stack OSS para clonar Submagic cobre ~50% das features. Os 50% restantes (eye contact AI, AI avatars, curated music/templates) são **products of curation**, não engenharia — não há OSS que substitua bem.

### Finding 5 — Quick wins instaláveis hoje

Sem precisar clonar nada, você pode pegar 60% das features mais úteis instalando 7 packages OSS:

| Feature | OSS | Comando |
|---|---|---|
| ASR multi-idioma | faster-whisper | `pip install faster-whisper` |
| Auto-cut silêncio + filler | auto-editor | `pip install auto-editor` |
| Captions animados | Captacity | `pip install captacity` |
| Pipeline short-form completo | OpenShorts | `git clone github.com/mutonby/openshorts` |
| Semantic search vídeo | video_semantic_search | `git clone github.com/Professor833/video_semantic_search` |
| Vector DB | ChromaDB | `pip install chromadb` |
| NLE XML export | OpenTimelineIO | `pip install opentimelineio` |

---

## Recomendações por cenário

### Cenário A — Quero testar OSS antes de assinar SaaS
1. Instale a stack acima (1 hora setup)
2. Rode `OpenShorts` num vídeo seu real
3. Compare output vs Submagic Free (free tier de SM tem watermark mas mostra qualidade)
4. **Se gap de qualidade for >30%, assine Submagic.** Caso contrário, OSS já resolve.

### Cenário B — Quero construir produto SaaS competidor
1. **Foco em Eddie AI clone** (não Submagic) — categoria menos saturada, OSS mais maduro
2. Stack: WhisperX + SigLIP + ChromaDB + Llama 3.1 + OpenTimelineIO
3. Diferencial: pricing $50-80/mês (entre Plus e Pro de Eddie), foco em PT-BR + LATAM
4. Effort: 6-9 meses, 1-2 senior engineers

### Cenário C — Quero usar tools comerciais com preço justo
1. **Comece com Submagic Pro** ($24/mês) — cobre 80% dos casos solo creator
2. Se evoluir pra documentário/podcast multi-cam, **adicione Eddie AI Plus** ($21/mês) na hora de fazer rough cut, exporta para Premiere
3. Evite Pro tier de Eddie ($167) a menos que cliente exigente compense

### Cenário D — Quero privacidade local (não-cloud)
1. **Eddie AI já é desktop local**, mas processa parte na cloud (LLM proprietário)
2. Para 100% local: stack OSS com Ollama (LLM local) + WhisperX (ASR local) + SigLIP (visual local) + Remotion/FFmpeg (render local)
3. Hardware mínimo: Mac M-series 64GB RAM (ou GPU RTX 3090+)

---

## Risk assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Pricing pode ter mudado entre mar/2026 e mai/2026 | LOW | Confirmar na landing page antes de assinar |
| OSS tools mudam de mantenedor / abandonam | MEDIUM | Pin versions, fork repos críticos |
| Quality gap OSS vs commercial em polish (captions, eye contact) | MEDIUM | Aceitar gap ou pagar comercial para essa camada específica |
| OSS LLM local requer hardware caro (M-series 64GB+) | MEDIUM | Usar Llama API hosted (Groq, Together) como fallback |
| Curated stock library (Storyblocks-grade) não tem OSS bom | HIGH | Pexels/Pixabay com expectativa de qualidade menor |
| Eye contact AI / AI avatars / lip-sync não têm OSS production-grade | HIGH | Skip features ou pagar serviço pontual |

---

## Confidence breakdown

| Claim | Confidence | Source |
|---|---|---|
| Submagic feature list | HIGH | Site oficial + docs.submagic.co + 4 reviews |
| Submagic pricing | MEDIUM-HIGH | Reviews jan-mar/2026, pode ter shift |
| Eddie AI feature list | HIGH | heyeddie.ai/features + help center + 6 reviews |
| Eddie AI pricing tiers | HIGH | Capterra + reviews jan/2026 |
| OSS maturity ratings | HIGH | GitHub stars/activity + community knowledge |
| OSS clone effort estimates | MEDIUM | Engineering judgment, sem benchmark real |
| "Eddie é mais clonável" | HIGH | Análise estrutural: Eddie produz metadata (clonável), SM produz polish (curado) |

---

## Artefatos gerados

```
docs/bench/submagic-vs-eddie-ai/
├── metadata.json                          # Configuração do bench
├── inventory-submagic.md                  # Inventário completo SM (34 features)
├── inventory-eddie-ai.md                  # Inventário completo ED (35 features)
├── comparison-matrix.md                   # Matrix paridade 35 features cross-categoria
├── scorecard.md                           # 6 dimensões + composite + persona-weighted
├── gap-analysis.md                        # GAPs bidirecionais + tier OSS substitution
├── battle-card.md                         # 1-page quick reference
├── executive-report.md                    # Este arquivo
└── deep/
    ├── feature-comparison.md              # Análise behavioral profunda
    └── oss-substitution-roadmap.md        # ⭐ Stack completo OSS por feature
```

---

## Próxima ação sugerida

```bash
# Para testar OSS pipeline em 1 dia (Cenário A)
mkdir ~/oss-video-test && cd ~/oss-video-test
pip install faster-whisper auto-editor captacity chromadb opentimelineio
git clone https://github.com/mutonby/openshorts
git clone https://github.com/Professor833/video_semantic_search
cat openshorts/README.md
```

Se quiser aprofundar em uma camada específica (ex: "deep dive em CLIP/SigLIP para semantic search da minha library pessoal"), peça `/tech-research "<tópico>"` ou continue este bench com:

```bash
*bench-tech "WhisperX vs faster-whisper vs whisper.cpp"
# ou
*bench-product "OpenShorts vs MoneyPrinterTurbo vs video_semantic_search"
```
