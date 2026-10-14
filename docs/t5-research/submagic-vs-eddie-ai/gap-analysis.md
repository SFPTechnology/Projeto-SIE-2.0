# Gap Analysis — Submagic vs Eddie AI

Gaps bidirecionais com priority e absorption complexity.

## Gaps de Submagic (features que Submagic NÃO tem mas Eddie tem)

| ID | Gap | Priority | Complexity | Justificativa |
|---|---|---|---|---|
| GAP-SM-01 | Semantic visual search na library pessoal | P0 | HIGH | É o feature definidor do Eddie. Submagic depende de transcript-only matching |
| GAP-SM-02 | Multicam sync (até 6 câmeras) | P1 | HIGH | Crítico para podcast pro / corporate; SM ignora esse mercado |
| GAP-SM-03 | NLE export (XML para Premiere/Resolve/FCP) | P0 | MEDIUM | Sem isso, SM nunca entra em workflow pro |
| GAP-SM-04 | Speaker diarization | P1 | MEDIUM | Necessário para podcast multi-speaker |
| GAP-SM-05 | Chat-prompt edit ("pull best 3 soundbites") | P1 | MEDIUM | UX paradigm-shifting que SM não tem |
| GAP-SM-06 | Rough cut frameworks (narrative templates) | P2 | LOW | Diferencial Eddie em documentário |
| GAP-SM-07 | Background speech detection em B-roll | P2 | LOW | Detail que importa em log profissional |
| GAP-SM-08 | Night Shift (processamento overnight) | P2 | LOW | Diferencial UX, não core |

## Gaps de Eddie AI (features que Eddie NÃO tem mas Submagic tem)

| ID | Gap | Priority | Complexity | Justificativa |
|---|---|---|---|---|
| GAP-ED-01 | Render final do vídeo (não é output XML) | P0 | HIGH | Mudaria o produto inteiro — Eddie é assistente, não editor |
| GAP-ED-02 | Captions animados word-by-word (best-in-class) | P0 | MEDIUM | Crítico para uso solo short-form |
| GAP-ED-03 | Subtitle templates library extensa | P1 | LOW | SM tem dezenas, ED não tem |
| GAP-ED-04 | Auto-translate em 100+ idiomas | P1 | MEDIUM | Diferencial SM massivo |
| GAP-ED-05 | Layouts split-screen nativos (split-50-50, split-35-65) | P1 | LOW | Diferencial visual SM |
| GAP-ED-06 | Direct social publishing/scheduling | P1 | MEDIUM | SM publica direto; ED depende do NLE |
| GAP-ED-07 | Eye contact correction AI | P2 | HIGH | Depende de modelo proprietário |
| GAP-ED-08 | Hook title generation | P2 | LOW | Polish feature |
| GAP-ED-09 | AI Avatar generator (120+ avatares) | P2 | HIGH | Categoria à parte (HeyGen-class) |
| GAP-ED-10 | Magic Zoom one-click | P2 | LOW | Polish feature |
| GAP-ED-11 | Public REST API documentado | P2 | MEDIUM | Para automação programática |

## Categorização para substituição open-source

### Tier 1 — Substituível com OSS maduro hoje (qualidade comparable ou melhor)

| Feature alvo | OSS recomendado | Maturidade |
|---|---|---|
| Speech-to-text multi-language | **faster-whisper / WhisperX** | ⭐⭐⭐⭐⭐ |
| Filler word removal | Whisper + heuristic post-processing | ⭐⭐⭐⭐ |
| Silence removal | **auto-editor** (github), FFmpeg silencedetect | ⭐⭐⭐⭐⭐ |
| Speaker diarization | **pyannote.audio**, NeMo | ⭐⭐⭐⭐ |
| Multicam sync por audio peak | **audalign**, FFmpeg | ⭐⭐⭐⭐ |
| Visual recognition / B-roll tagging | **CLIP / OpenCLIP / SigLIP** | ⭐⭐⭐⭐⭐ |
| Semantic image search | **CLIP + FAISS / ChromaDB / pgvector** | ⭐⭐⭐⭐⭐ |
| Stock B-roll fallback | Pexels / Pixabay free API | ⭐⭐⭐⭐ |
| Render engine | **FFmpeg** + **Remotion** (React-based) | ⭐⭐⭐⭐⭐ |
| NLE XML export | OpenTimelineIO (otio), pyaaf2 | ⭐⭐⭐⭐ |
| Captions/subtitles editor | **Tero Subtitler**, Aegisub, Subtitle Edit | ⭐⭐⭐⭐⭐ |
| Auto-translate | **NLLB-200 (Meta)**, MarianMT, M2M-100 | ⭐⭐⭐⭐ |
| Subtitle styling animado word-by-word | **Captacity** (github), **MoneyPrinterTurbo** (overlay) | ⭐⭐⭐ |

### Tier 2 — Substituível parcialmente (qualidade inferior ou requer integração)

| Feature alvo | OSS / abordagem | Caveat |
|---|---|---|
| Chat-prompt edit ("pull soundbites") | Llama 3.1 / Qwen / Mistral local + RAG sobre transcript | Funcional mas qualidade < GPT-4 |
| Rough cut auto-generation | LLM + transcript + clipping rules | Customizado, sem produto out-of-box |
| AI avatars + lip-sync | **SadTalker**, **Wav2Lip**, **Hallo** | Qualidade visivelmente inferior aos comerciais |
| AI Magic Zoom | OpenCV + face detection (mediapipe) | Heurístico, não learned |
| Edit-by-transcript GUI | **Hyperaudio Lite Editor** | Web minimal, falta polish |

### Tier 3 — Sem substituto OSS bom hoje

| Feature alvo | Razão | Workaround |
|---|---|---|
| Eye contact correction AI | NVIDIA Maxine é proprietário; OSS escasso | Skip ou pagar |
| Curated music library trendy | Licenciamento musical é o produto, não o algoritmo | YouTube Audio Library + filtragem manual |
| Storyblocks-grade stock library | Licenciamento de catálogo | Pexels + Pixabay (qualidade menor) |
| Stable production cloud rendering | Operacional / cost engineering | Self-host com fila (Celery + Redis + workers GPU) |
| Direct posting TikTok/IG/YT (oficial) | APIs com rate limits / ToS | Publicar manual ou via Buffer/Hootsuite (não-OSS) |

## Insight estratégico

A descoberta crítica: **Eddie AI é mais "substituível por OSS" do que Submagic**, contraintuitivamente.

**Por quê?** Eddie é um **logging + planning assistant** que produz METADATA (XML, timestamps, transcripts taggeados). Não renderiza nada final. Toda renderização acontece no NLE do usuário.

Stack OSS para clonar Eddie:
```
faster-whisper (ASR) +
pyannote.audio (diarization) +
CLIP/OpenCLIP (visual tagging) +
FAISS/Chroma (semantic search) +
Llama 3.1 local (chat-prompt edit) +
OpenTimelineIO (XML export para Premiere/Resolve/FCP)
```
→ ~80% das features de Eddie AI atingíveis com pipeline OSS.

Submagic é um **renderer com UX premium** — clonar exige FFmpeg + Remotion + design system + render farm + curated stock library + libraries de transitions/templates. ~50% das features factíveis em OSS, mas o polish (captions templates, eye contact, avatares) sobe a barra.
