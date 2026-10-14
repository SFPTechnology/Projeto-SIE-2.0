# Inventário — faster-whisper

> Confidence: alta. Repo primário, mantenedor corporativo (SYSTRAN), múltiplos benchmarks reproduzíveis.

## Identidade

- **Repo:** https://github.com/SYSTRAN/faster-whisper
- **Autor/Mantenedor:** SYSTRAN (empresa de tradução francesa, mantém também CTranslate2)
- **Licença:** MIT — totalmente permissiva
- **Linguagem:** Python (binding) + C++ (CTranslate2 backend)
- **Status:** mantido ativamente, é a base de praticamente todo o ecossistema Python pós-OpenAI Whisper

## Features

| Feature | faster-whisper |
|---|---|
| Transcrição base | Reimplementação do Whisper sobre CTranslate2 (engine de inferência otimizada) |
| Word-level timestamps | **Sim, nativo** (`word_timestamps=True`) — derivado da cross-attention do Whisper, não tão preciso quanto WhisperX |
| Speaker diarization | **Não nativo** — precisa pluggar pyannote manualmente |
| VAD | **Sim** — Silero VAD integrado (`vad_filter=True`) |
| Quantização | int8, int8_float16, int8_bfloat16, float16, float32 |
| GPU | CUDA (excelente), CPU (otimizado via Apple Accelerate / oneDNN / OpenBLAS) |
| Apple Silicon | CPU only — sem aceleração Metal/ANE (CTranslate2 não tem backend Apple GPU) |
| API Python | `WhisperModel("large-v3", device="cuda", compute_type="float16")` → `segments, info = model.transcribe(...)` |

## Suporte a Português

- Suporta todos os 99 idiomas do Whisper (pt incluído).
- `language="pt"` ou auto-detect com `language=None`.
- Qualidade de transcrição igual a Whisper-OpenAI (mesmos pesos), com WER agregado ~9% no Common Voice 15 multilingue para large-v3 ([release notes](https://github.com/openai/whisper/discussions/1762)).
- Para pt especificamente: 8–15% WER (categoria medium-resource).

## Stack de Dependências

- `ctranslate2 >= 4.x`
- `tokenizers`
- `huggingface_hub`
- `onnxruntime` (apenas para Silero VAD opcional)
- Sem torch obrigatório (vantagem em deploys minimalistas)

## Instalação

```bash
pip install faster-whisper
# Para GPU NVIDIA: precisa de cuDNN 9 + CUDA 12 instalados no host
```

## Performance (referência)

- **NVIDIA GPU (T4 / A100):** ~4× mais rápido que `openai/whisper` original, mesma acurácia
- **CPU x86 (small.en):** ~14s para clip que `whisper.cpp` faz em ~46s (community bench)
- **Mac M2/M3 (CPU only):** competitivo, mas perde ~30–40% em RTF para whisper.cpp+CoreML+Metal — porque CTranslate2 não acelera via ANE/Metal
- **Memória:** maior que whisper.cpp (Python + CTranslate2 stack), startup ~1.8s vs <300ms do whisper.cpp
- **Word timestamps:** disponíveis, mas derivados de cross-attention — podem ter drift maior que WhisperX em fala disfluente

## Pontos Fortes

1. **Backbone do ecossistema** — WhisperX, whisply, insanely-fast-whisper-tools usam faster-whisper sob o capô.
2. **API Python idiomática** — generator de segmentos, integra trivialmente em pipeline de vídeo.
3. **Quantização granular** (int8/fp16/bf16) — controle fino de tradeoff acurácia/velocidade.
4. **MIT puro** — zero atrito legal.
5. **GPU CUDA é classe mundial** — para Linux GPU é a opção #1.
6. **Sem dependência de torch** — deploy menor.

## Pontos Fracos

1. **Sem aceleração Apple GPU/ANE** — em Mac M-series, whisper.cpp é mais rápido.
2. **Não tem diarização** — precisa pluggar pyannote (ou usar WhisperX).
3. **Word timestamps medianos** — bons, mas WhisperX é melhor para subtitling.
4. **CUDA setup pode ser frágil** — exige cuDNN 9 + CUDA 12 corretos no host.
5. **Cold start lento** (~1.8s para subir modelo Python).

## Adequação à Persona (OSS video pipeline)

- **(a) word-level timestamps:** ★★★★☆ — bom, mas inferior a WhisperX
- **(b) multi-language + Portuguese:** ★★★★★ — paridade total com OpenAI Whisper
- **(c) Mac M / Linux GPU:** ★★★★☆ — Linux GPU 5/5; Mac M-series 3/5
- **(d) Python pipeline:** ★★★★★ — DX referência
- **(e) diarization:** ★★★☆☆ — não nativo, mas bem-documentado plug com pyannote

## Fontes

- README: https://github.com/SYSTRAN/faster-whisper
- Modal blog: https://modal.com/blog/choosing-whisper-variants
- Discussion CTranslate2 Apple Silicon: https://github.com/SYSTRAN/faster-whisper/discussions/368
- Pyannote 3.1 + faster-whisper: https://huggingface.co/pyannote/speaker-diarization-3.1
- Hotovo blog (pyannote integration): https://www.hotovo.com/blog/whisper-from-transcription-to-speaker-diarization-part-2
