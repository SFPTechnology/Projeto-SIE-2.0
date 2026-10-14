# OSS Substitution Roadmap — Submagic vs Eddie AI

> **Este é o artefato principal para a sua intenção declarada.**
> Para cada feature relevante dos dois produtos, mapeio a alternativa open-source mais madura, com link, maturidade e caveats.

## Como ler este documento

- **Maturidade:** ⭐⭐⭐⭐⭐ (production-ready) → ⭐ (research/abandoned)
- **Effort:** quanto trabalho para integrar (LOW = pip install, HIGH = construir produto)
- **Quality vs commercial:** % subjetiva da qualidade comparado ao SaaS comercial

---

## Camada 1 — Speech-to-text & transcription

### Whisper family (escolha aqui)

| OSS | Repo | Maturidade | Quality vs SM/ED | Effort | Notas |
|---|---|---|---|---|---|
| **faster-whisper** | https://github.com/SYSTRAN/faster-whisper | ⭐⭐⭐⭐⭐ | 95-100% | LOW | CTranslate2 — 4x mais rápido que openai-whisper, mesmo modelo |
| **WhisperX** | https://github.com/m-bain/whisperX | ⭐⭐⭐⭐⭐ | 100% + word-level timestamps | LOW | Adiciona forced alignment + diarization. **Recomendado para B-roll auto-place** porque dá word-level timestamps necessários pro match preciso |
| **whisper.cpp** | https://github.com/ggerganov/whisper.cpp | ⭐⭐⭐⭐⭐ | 95% | LOW | C++ port, roda em qualquer hardware, ideal para mobile/edge |
| **openai-whisper** | https://github.com/openai/whisper | ⭐⭐⭐⭐ | 100% baseline | LOW | Original, mas faster-whisper é estritamente superior |

**Veredicto:** **WhisperX**. Word-level timestamps são o que você precisa para matchar imagem com fala segundo-a-segundo.

---

## Camada 2 — Speaker diarization & identification

| OSS | Repo | Maturidade | Quality | Effort | Notas |
|---|---|---|---|---|---|
| **pyannote.audio** | https://github.com/pyannote/pyannote-audio | ⭐⭐⭐⭐⭐ | 90-95% | MEDIUM | State-of-art para diarization. Requer HuggingFace token (free) |
| **NVIDIA NeMo** | https://github.com/NVIDIA/NeMo | ⭐⭐⭐⭐ | 90% | HIGH | Mais pesado, mas accuracy alta em multi-speaker |
| **Resemblyzer** | https://github.com/resemble-ai/Resemblyzer | ⭐⭐⭐⭐ | 80% | LOW | Speaker identification simples (clustering), bom para 2-3 speakers |

**Veredicto:** **pyannote.audio** para multicam podcast. WhisperX já integra pyannote internamente — escolha um, ganhe ambos.

---

## Camada 3 — Visual recognition & semantic image search

> Esta é a camada CORE do feature "B-roll Finder" do Eddie e do match contextual de imagens com fala.

| OSS | Repo | Maturidade | Quality | Effort | Notas |
|---|---|---|---|---|---|
| **OpenCLIP** | https://github.com/mlfoundations/open_clip | ⭐⭐⭐⭐⭐ | Comparable to CLIP | MEDIUM | Modelo CLIP open-source. Múltiplos checkpoints (ViT-B/32, ViT-L/14, ViT-G/14) |
| **CLIP (OpenAI)** | https://github.com/openai/CLIP | ⭐⭐⭐⭐⭐ | Baseline | MEDIUM | Original 2021. Funcional mas menos atualizado que OpenCLIP |
| **SigLIP** | https://huggingface.co/google/siglip-base-patch16-256 | ⭐⭐⭐⭐⭐ | Better than CLIP | MEDIUM | Google 2023, pareceived superior em retrieval tasks |
| **BLIP-2** | https://github.com/salesforce/LAVIS | ⭐⭐⭐⭐ | Captioning + retrieval | HIGH | Adiciona captioning automático aos clips ("a person talking in office") |
| **YOLOv8** | https://github.com/ultralytics/ultralytics | ⭐⭐⭐⭐⭐ | Object detection | LOW | Não é semantic search, mas adiciona "objects in this clip" tags |

**Veredicto:** Stack ótimo é **SigLIP + WhisperX + FAISS**:
1. WhisperX transcreve áudio → texto com timestamps word-level
2. SigLIP encoda cada frame da biblioteca pessoal → vector
3. SigLIP encoda cada frase do transcript → vector
4. FAISS faz nearest-neighbor: "para cada frase do transcript, achar frame mais semelhante na biblioteca"

Isso replica o "B-Roll Finder" do Eddie em ~200 linhas de Python.

---

## Camada 4 — Vector database (semantic search backend)

| OSS | Repo | Maturidade | Use case | Effort |
|---|---|---|---|---|
| **FAISS** | https://github.com/facebookresearch/faiss | ⭐⭐⭐⭐⭐ | In-memory, single-machine | LOW |
| **ChromaDB** | https://github.com/chroma-core/chroma | ⭐⭐⭐⭐⭐ | Embedded, dev-friendly | LOW |
| **Qdrant** | https://github.com/qdrant/qdrant | ⭐⭐⭐⭐⭐ | Production, multi-tenant | MEDIUM |
| **pgvector** | https://github.com/pgvector/pgvector | ⭐⭐⭐⭐⭐ | Postgres extension (Supabase) | LOW |
| **Milvus** | https://github.com/milvus-io/milvus | ⭐⭐⭐⭐ | Production, scale-out | HIGH |

**Veredicto:** **ChromaDB** para protótipo (1 hora setup). **pgvector + Supabase** para produção (já está no stack do Sinkra Hub).

---

## Camada 5 — Multicam sync

| OSS | Repo | Maturidade | Quality | Effort |
|---|---|---|---|---|
| **audalign** | https://github.com/benfmiller/audalign | ⭐⭐⭐⭐ | Audio peak alignment | LOW |
| **FFmpeg** | https://ffmpeg.org/ | ⭐⭐⭐⭐⭐ | Manual sync via filter | MEDIUM |
| **PluralEyes-replacement scripts** | github (vários) | ⭐⭐ | Heurístico | HIGH |

**Veredicto:** **audalign** + FFmpeg para 90% dos casos. Para 6 câmeras simultâneas (Eddie tier), precisa de fluxo customizado.

---

## Camada 6 — Auto-cut & silence removal

| OSS | Repo | Maturidade | Quality | Effort | Notas |
|---|---|---|---|---|---|
| **auto-editor** | https://github.com/WyattBlue/auto-editor | ⭐⭐⭐⭐⭐ | Excellent | LOW | Remove silêncio, jump-cuts, exports MP4 |
| **FFmpeg silencedetect** | builtin | ⭐⭐⭐⭐⭐ | Manual | MEDIUM | Para integração custom |
| **Captacity** | https://github.com/unconv/captacity | ⭐⭐⭐⭐ | Captions + silence | LOW | Combina Whisper + auto-cut |

**Veredicto:** **auto-editor** é a primeira coisa que você instala. Substitui silence removal de SM/ED inteiro.

---

## Camada 7 — Captions animados word-by-word

> Onde Submagic é best-in-class. Difícil substituir 100%, mas há OSS funcionais.

| OSS | Repo | Maturidade | Quality vs SM | Effort |
|---|---|---|---|---|
| **Captacity** | https://github.com/unconv/captacity | ⭐⭐⭐⭐ | 70% | LOW | Word-by-word animados |
| **MoneyPrinterTurbo** | https://github.com/harry0703/MoneyPrinterTurbo | ⭐⭐⭐⭐ | 70% | MEDIUM | Pipeline completo short-form |
| **Tero Subtitler** | https://github.com/URUWorks/TeroSubtitler | ⭐⭐⭐⭐⭐ | 60% (manual) | MEDIUM | Editor de SRT/ASS robusto, sem animação |
| **Subtitle Edit** | https://github.com/SubtitleEdit/subtitleedit | ⭐⭐⭐⭐⭐ | 60% | MEDIUM | Idem, Windows-first |
| **Aegisub** | https://github.com/Aegisub/Aegisub | ⭐⭐⭐⭐⭐ | 90% (com ASS effects) | HIGH | Fansub-grade, anima qualquer coisa via ASS, mas curva pesada |

**Veredicto:** **Captacity** para 80/20. **Aegisub + ASS templates** para qualidade premium se você dominar.

---

## Camada 8 — Render & composição

| OSS | Repo | Maturidade | Quality | Effort | Notas |
|---|---|---|---|---|---|
| **FFmpeg** | https://ffmpeg.org/ | ⭐⭐⭐⭐⭐ | Production-grade | MEDIUM | A base de tudo |
| **Remotion** | https://github.com/remotion-dev/remotion | ⭐⭐⭐⭐⭐ | Excelente | MEDIUM | React-based, programático, ótimo para templates |
| **Motion Canvas** | https://github.com/motion-canvas/motion-canvas | ⭐⭐⭐⭐ | Excelente para animações | MEDIUM | TypeScript-based, mais artístico |
| **MoviePy** | https://github.com/Zulko/moviepy | ⭐⭐⭐⭐ | Boa | LOW | Python wrapper sobre FFmpeg, ótimo para protótipo |
| **OpenShot** | https://github.com/OpenShot/openshot-qt | ⭐⭐⭐ | Editor desktop OSS | HIGH | Editor tradicional, não programático |
| **Olive** | https://github.com/olive-editor/olive | ⭐⭐⭐ | Editor desktop OSS | HIGH | Mais moderno que OpenShot |
| **Kdenlive** | https://invent.kde.org/multimedia/kdenlive | ⭐⭐⭐⭐ | Editor desktop OSS | HIGH | KDE, recém ganhou STT (VOSK) |
| **Blender VSE** | https://www.blender.org/ | ⭐⭐⭐⭐ | Power-user | HIGH | Blender tem video editor built-in surprisingly capable |

**Veredicto:** Para programático (você escreve código que gera vídeo): **Remotion**. Para CLI rápido: **MoviePy**. Para usuário final: **Kdenlive**.

---

## Camada 9 — Auto B-roll pipelines (produtos OSS já prontos)

| OSS | Repo | Maturidade | Cobre quanto de SM/ED? | Notas |
|---|---|---|---|---|
| **OpenShorts** ⭐ | https://github.com/mutonby/openshorts | ⭐⭐⭐⭐ | ~70% Submagic | **Mais próximo de Submagic em OSS hoje.** Stack: faster-whisper + YOLOv8 + mediapipe + FFmpeg. Self-hosted, no watermark. Publica direto TikTok/IG/YT |
| **MoneyPrinterTurbo** | https://github.com/harry0703/MoneyPrinterTurbo | ⭐⭐⭐⭐ | ~50% Submagic | Pipeline curto: prompt → script → TTS → stock video → captions → render |
| **video_semantic_search** | https://github.com/Professor833/video_semantic_search | ⭐⭐⭐ | ~30% Eddie | Whisper + sentence-transformers + FAISS. Add CLIP visual branch para clonar B-Roll Finder |
| **FiftyOne semantic_video_search** | https://github.com/danielgural/semantic_video_search | ⭐⭐⭐⭐ | ~40% Eddie | Plugin FiftyOne, multimodal (visual + audio + OCR) |
| **AutoCut** | https://github.com/mli/autocut | ⭐⭐⭐⭐ | ~30% Submagic | Edit-by-text via SRT, popular no GitHub Trending |
| **Captacity** | https://github.com/unconv/captacity | ⭐⭐⭐⭐ | ~40% Submagic captions | Word-by-word captions automatic |

**Veredicto:** **OpenShorts** é o produto OSS mais avançado para clonar Submagic. Use como base e estenda.

---

## Camada 10 — NLE export (XML para Premiere/Resolve/FCP)

> Onde Eddie domina. OSS aqui é maduro mas pouco usado.

| OSS | Repo | Maturidade | Quality | Effort |
|---|---|---|---|---|
| **OpenTimelineIO (otio)** | https://github.com/AcademySoftwareFoundation/OpenTimelineIO | ⭐⭐⭐⭐⭐ | Pixar/Academy-backed | MEDIUM | Adapter pra Premiere XML, FCPXML, EDL, AAF, Resolve |
| **pyaaf2** | https://github.com/markreidvfx/pyaaf2 | ⭐⭐⭐⭐ | AAF-specific | MEDIUM | Para Avid AAF |
| **fcpxml-parser** | (vários no GitHub) | ⭐⭐⭐ | Funcional | MEDIUM | FCP XML específico |

**Veredicto:** **OpenTimelineIO** resolve 95% dos casos. É o padrão de fato para interchange.

---

## LLM local (para clonar Chat-Edit do Eddie)

| OSS | Repo / source | Maturidade | Quality vs Eddie chat | Effort |
|---|---|---|---|---|
| **Llama 3.1 70B** | Meta / HF | ⭐⭐⭐⭐⭐ | 85-90% | HIGH (precisa GPU) |
| **Qwen 2.5 72B** | Alibaba / HF | ⭐⭐⭐⭐⭐ | 90% | HIGH |
| **Mistral Large** | Mistral / HF | ⭐⭐⭐⭐⭐ | 85% | HIGH |
| **Gemma 2 27B** | Google / HF | ⭐⭐⭐⭐ | 75% | MEDIUM |
| **Ollama** (runtime) | https://github.com/ollama/ollama | ⭐⭐⭐⭐⭐ | N/A — runner | LOW |

**Veredicto:** **Ollama + Llama 3.1 70B** roda local em Mac M-series com 64GB RAM. Para chat-edit "pull best 3 soundbites on leadership", a qualidade é suficiente.

---

## Pipeline OSS recomendado — clonar Eddie AI

Eddie é o alvo mais clonável. Stack:

```
┌─────────────────────────────────────────────┐
│  INPUT: Pasta com A-roll + B-roll do user  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  WhisperX (transcript + word timestamps)    │
│  pyannote (diarization)                     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  SigLIP / OpenCLIP (visual embed por frame)│
│  YOLOv8 (object detection tags)             │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  ChromaDB / pgvector (vector store)         │
│  → indexa B-roll por embedding visual       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Ollama + Llama 3.1 (chat-prompt edit)      │
│  → "pull best 3 soundbites on X"            │
│  → "generate rough cut from this transcript"│
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  OpenTimelineIO (export XML)                │
│  → Premiere / Resolve / FCP                 │
└─────────────────────────────────────────────┘
```

**Effort estimate:** ~80h de senior engineer para MVP funcional. ~300h para qualidade próxima de Eddie AI Plus tier.

---

## Pipeline OSS recomendado — clonar Submagic

Mais difícil — Submagic é renderer com polish premium.

```
┌─────────────────────────────────────────────┐
│  INPUT: Vídeo bruto + library de imagens   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  faster-whisper (transcript word-level)     │
│  auto-editor (silence + filler removal)     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  SigLIP (semantic match para B-roll)        │
│  + Pexels/Pixabay API (stock fallback)      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Captacity (word-by-word captions)          │
│  + Aegisub ASS templates (estilo premium)   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Remotion (compose + split-50-50 layout)    │
│  + FFmpeg (encode final 1080p/4K)           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Output: MP4 pronto pra publicar            │
└─────────────────────────────────────────────┘
```

Feature gaps que ficam:
- **Eye contact correction** → não tem OSS bom (NVIDIA Maxine é proprietário)
- **AI Avatars 120+** → SadTalker / Wav2Lip funcionam mas qualidade ~60%
- **Music library curated** → licenciamento é o produto, não o código
- **Trendy templates curated** → curation humana

**Effort estimate:** ~150h para MVP. ~500h para qualidade Submagic-tier (e ainda fica gap em polish).

**Mais barato que cloning:** assinar Submagic Pro $24/mês = $288/ano. 500h de eng senior = ~$50-100k. Break-even em ~150-300 anos. Faz sentido só se você quer **construir produto concorrente** ou tem **requisito hard de privacidade local**.

---

## Quick wins (instalar HOJE, valor imediato)

Se você quer testar o pipeline OSS sem comprometimento:

```bash
# 1. Transcrição local de qualidade SaaS-grade
pip install faster-whisper
# ou
brew install whisper-cpp  # roda em qualquer Mac

# 2. Auto-cut de silêncio
pip install auto-editor

# 3. Captions animados
pip install captacity

# 4. Pipeline curto-form completo (auto B-roll + captions)
git clone https://github.com/mutonby/openshorts && cd openshorts && cat README.md

# 5. Semantic image search no seu B-roll
git clone https://github.com/Professor833/video_semantic_search

# 6. Vector search rápido
pip install chromadb sentence-transformers

# 7. NLE XML export
pip install opentimelineio
```

Cada um desses cobre uma das features-core de SM ou ED.

---

## Tabela mestre de equivalência (para referência rápida)

| Feature SM/ED | OSS top-1 | OSS top-2 |
|---|---|---|
| Auto transcription | WhisperX | faster-whisper |
| Filler removal | auto-editor | Captacity |
| Silence removal | auto-editor | FFmpeg silencedetect |
| Speaker diarization | pyannote.audio | NeMo |
| Multicam sync | audalign | FFmpeg |
| Visual recognition | SigLIP | OpenCLIP |
| Object detection | YOLOv8 | DETR |
| Semantic search (visual) | SigLIP + FAISS | OpenCLIP + Chroma |
| Vector store | ChromaDB | pgvector |
| Auto B-roll pipeline | OpenShorts | MoneyPrinterTurbo |
| Captions animados | Captacity | Aegisub + ASS |
| Subtitle editor | Tero Subtitler | Subtitle Edit |
| Auto-translate | NLLB-200 | M2M-100 |
| Render programático | Remotion | MoviePy |
| Render desktop | Kdenlive | Olive |
| NLE XML export | OpenTimelineIO | pyaaf2 |
| Chat edit (LLM) | Ollama + Llama 3.1 | Qwen 2.5 |
| Edit-by-transcript GUI | Hyperaudio Lite | AutoCut |
| Stock B-roll | Pexels API | Pixabay API |
| Lip-sync avatar | SadTalker | Wav2Lip |

---

## Conclusão para sua intenção

1. **Eddie AI é mais clonável que Submagic** em OSS (~80% vs ~50% de cobertura).
2. **OpenShorts** é o ponto de partida mais avançado para Submagic-clone.
3. **WhisperX + SigLIP + ChromaDB + OpenTimelineIO** é o stack mínimo para Eddie-clone.
4. **Não tente clonar tudo** — escolha 1-3 features que importam para o seu workflow e pegue só esses módulos.
5. **Maior valor por menor effort:** instale `auto-editor` + `Captacity` + `OpenShorts` essa semana, ganhe 60% das funcionalidades de SM grátis.
