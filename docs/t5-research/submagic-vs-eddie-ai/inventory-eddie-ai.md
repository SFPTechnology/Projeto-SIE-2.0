# Inventory — Eddie AI

**Site:** https://www.heyeddie.ai/
**Categoria:** AI assistant editor para profissionais (rough cuts + logging + multicam)
**Plataforma:** Desktop app Mac/Windows (GPU-enabled)
**Origem:** Empresa indie, foco em filmmakers/documentary
**Confidence:** HIGH (oficial features page + help center + 6+ reviews 2026)

## Identidade do produto

> "The Assistant Video Editor for Pros" — não substitui o NLE, **alimenta o NLE** com rough cuts e logging organizado.

NÃO é editor final — exporta XML/timeline para Premiere Pro, DaVinci Resolve, Final Cut Pro. É um **pre-edit assistant** orientado por chat-prompt.

## Inventário de features (categorizado)

### A. A-Roll Logging
- [F-ED-01] Auto-transcrição de A-roll (interviews, talking head)
- [F-ED-02] Filler word removal automático
- [F-ED-03] Clips agrupados por tópico (auto-segmentação semântica)
- [F-ED-04] Speaker identification

### B. B-Roll Logging
- [F-ED-05] Visual recognition para tags automáticas (objetos, cenas, ações)
- [F-ED-06] Background speech detection em B-roll
- [F-ED-07] Tags searchable cross-projeto

### C. B-Roll Finder ⭐
- [F-ED-08] **Semantic search na sua biblioteca pessoal** ("office chaos" → planos relevantes mesmo sem tags manuais)
- [F-ED-09] Sugere stock matches além da biblioteca pessoal
- [F-ED-10] Aligned com transcript do A-roll para placement contextual

### D. Talk to Transcript (Chat Edit)
- [F-ED-11] Chat-prompt interface ("pull the best three soundbites on leadership", "make a punchy two-minute hook")
- [F-ED-12] Stringouts automáticos (compilação de takes selecionados)
- [F-ED-13] Cut summaries via prompt em linguagem natural
- [F-ED-14] Rough Cut Frameworks (escolher estrutura narrativa antes de gerar draft)

### E. Multicam
- [F-ED-15] Sync de até 6 câmeras (audio peak alignment)
- [F-ED-16] Speaker identification → cuts automáticos no ângulo certo
- [F-ED-17] Funciona com podcast multi-camera

### F. Scripted Edits
- [F-ED-18] Cuts a partir de script ou outline
- [F-ED-19] Identifica melhores takes alternativos
- [F-ED-20] Refinement via prompt

### G. Social Clips
- [F-ED-21] Vertical 9:16 a partir de qualquer projeto
- [F-ED-22] Captions inclusos
- [F-ED-23] Recortes virais a partir de long-form

### H. Night Shift
- [F-ED-24] Processa footage durante off-hours
- [F-ED-25] Sincroniza multicam de madrugada
- [F-ED-26] Builds rough cuts overnight para você abrir pronto

### I. Brand Awareness
- [F-ED-27] Analisa website do cliente para gerar edit alinhado à brand

### J. Languages
- [F-ED-28] Multi-language support (adicionado em 2026; lista exata não fechada nas reviews)

### K. NLE Export
- [F-ED-29] **XML compatível Premiere Pro**
- [F-ED-30] **XML compatível DaVinci Resolve**
- [F-ED-31] **XML compatível Final Cut Pro**
- [F-ED-32] Metadata preservada (gold para team handoffs)
- [F-ED-33] BRAW/R3D files (Pro tier)

### L. Performance
- [F-ED-34] GPU-enabled processing (local)
- [F-ED-35] Mac/Windows desktop app

## Pricing (verificado jan-mar/2026)

| Tier | Preço | Limites principais |
|---|---|---|
| Free/Flex | $0 | 5 A-roll, 25 B-roll (10min ea), 5 files Chat&Edit, MP4 com light branding |
| Plus | $21/mês (anual) | +5 exports/mês, 10 A-roll, 50 B-roll |
| Pro | $167/mês (anual) | Multicam, BRAW/R3D, 20 exports/mês |
| Pro+ | $333/mês (anual) | 3 seats, modelo AI mais avançado, priority inference, 50 A-roll, 500 B-roll |

## Persona-fit

- 🎯 **Target:** Documentary filmmakers, podcast producers, corporate video teams, post-production teams
- 🎯 **Output esperado:** Rough cut → entregue ao NLE → finalização pelo editor humano
- ❌ **NÃO atende:** Solo creator querendo short polido em 5 min, mobile-first creator, quem não usa NLE

## Dependências externas (relevante para OSS-substitution)

| Componente | Vendor | Substituível por OSS? |
|---|---|---|
| Speech-to-text | Provavelmente Whisper-based + custom | ✅ Whisper (faster-whisper, WhisperX) |
| Visual recognition (B-roll tags) | Proprietary multimodal | ✅ CLIP/OpenCLIP, BLIP-2, SigLIP |
| Semantic search | Proprietary embeddings + vector DB | ✅ FAISS / Chroma / pgvector + sentence-transformers |
| Background speech detection | Proprietary | ⚠️ pyannote.audio (diarization OSS) |
| Multicam sync | Audio peak alignment (FFmpeg-able) | ✅ FFmpeg + audalign (OSS) |
| Speaker identification | Proprietary | ✅ pyannote.audio, NeMo |
| Chat-prompt UI | LLM (provavelmente GPT-4 / Claude class) | ⚠️ Llama 3.1, Qwen, Mistral local |
| NLE XML export | FCPXML / Premiere XML / DaVinci XML | ✅ Specs públicas, libs OSS (Pyaaf2, otio) |
| Render | Não renderiza output final — só rough cut metadata | N/A |

**OBS importante:** Eddie é um **logging + planning assistant**, não um renderer. Toda renderização final acontece no NLE do usuário. Isso torna a substituição OSS muito mais factível do que substituir Submagic.
