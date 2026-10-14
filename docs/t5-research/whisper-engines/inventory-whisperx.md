# Inventário — WhisperX

> Confidence: alta para features e licença; média para WER pt-BR (sem bench público dedicado).

## Identidade

- **Repo:** https://github.com/m-bain/whisperX
- **Autor:** Max Bain (Oxford VGG, lab acadêmico)
- **Licença:** BSD-2-Clause (PyPI metadata) — permissiva, OK para uso comercial
- **Linguagem:** Python (envoltório sobre faster-whisper + pyannote.audio + wav2vec2)
- **Paper:** Bain et al., Interspeech 2023 — "WhisperX: Time-Accurate Speech Transcription of Long-Form Audio" ([PDF](https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf))
- **Status:** maduro, ainda ativamente mantido em 2025/2026; existe fork comunitário "BetterWhisperX" como ramo de manutenção

## Features

| Feature | WhisperX |
|---|---|
| Transcrição base | OpenAI Whisper (via faster-whisper sob o capô) |
| Word-level timestamps | **Sim — ±50 ms** via forced alignment com wav2vec2 (vanilla Whisper só dá ±500 ms) |
| Speaker diarization | **Sim** — integrado com pyannote.audio (HF token gated) |
| VAD pré-processamento | **Sim** — Voice Activity Detection corta áudio em chunks de ~30s em regiões silenciosas |
| Batched inference | **Sim** — até ~70× real-time com batch=16 em GPU adequada |
| CLI | `whisperx audio.wav --model large-v2 --diarize --highlight_words True` |
| API Python | `whisperx.load_model()` + `model.transcribe()` + `whisperx.align()` + `whisperx.assign_word_speakers()` |
| Output formats | SRT, VTT, JSON, TSV, TXT |

## Suporte a Português

- **Modelo de alinhamento phoneme padrão para `pt`** disponível (lista oficial: `en, fr, de, es, it, ja, zh, nl, uk, pt`).
- Uso: `--language pt --model large-v3` — o phoneme model é puxado automaticamente do torchaudio/HF.
- Para línguas fora dessa lista é preciso plugar phoneme model manualmente.

## Stack de Dependências

- `faster-whisper` (CTranslate2) para transcrição rápida
- `pyannote.audio >= 3.1` para diarização (gated, exige HF token)
- `torchaudio` / `transformers` para wav2vec2 alignment
- `pytorch` (CUDA recomendado para Linux; CPU/MPS funciona mas mais lento)
- `ffmpeg` para decode

## Instalação

```bash
pip install whisperx
# ou via uv/pipx
# diarização exige aceitar termos em huggingface.co/pyannote/speaker-diarization-3.1
# e exportar HF_TOKEN
```

Pegadinhas comuns:
- pyannote 3.1 exige `pytorch` (não onnxruntime) — deploy mais simples que 2.x
- mac M-series: roda em MPS, mas não tão rápido quanto whisper.cpp+CoreML
- alguns forks (`whisperx_fix`, `BetterWhisperX`) existem para resolver compatibilidade com versões novas de torch/pyannote

## Performance (referência)

- **GPU NVIDIA (T4/A100):** ~70× real-time com `large-v2` batched=16 (claim oficial do paper/README)
- **Mac M2 Pro:** ~5.5× real-time reportado em comparação com SmartLittleApps server (whisper.cpp baseado, 15.8× — ou seja, whisper.cpp é mais rápido em Apple Silicon)
- **CPU x86:** competitivo com faster-whisper (mesmo backend), mais lento que whisper.cpp
- **Word timestamp accuracy:** ±50 ms (paper)

## Pontos Fortes

1. **Único do trio que entrega palavra+speaker out-of-the-box.** Eliminação de glue code para alinhar pyannote ↔ Whisper.
2. **VAD-cut + batch** dá throughput muito alto em áudio longo (entrevistas, podcasts, calls).
3. **Word timestamps com qualidade de subtitling** sem precisar treinar nada.
4. **Paper peer-reviewed** — método validado academicamente.
5. **Default phoneme model para pt** já na caixa.

## Pontos Fracos

1. **Stack pesada:** torch + pyannote + wav2vec2 + CTranslate2 — instalação não trivial; conflitos de versão em monorepos.
2. **Diarização gated:** exige aceitar termo no HF e gerenciar `HF_TOKEN` — bloqueio em ambientes air-gapped.
3. **Apple Silicon não é o foco:** roda em MPS mas perde para whisper.cpp em RTF e em footprint de memória.
4. **Modelos de diarização baseados em CC-BY-4.0** (pyannote) — atribuição obrigatória em produto comercial.
5. **Manutenção pulou para forks** em alguns períodos (BetterWhisperX) — sinal de que upstream não é hyperactive.
6. **Sobreposição de fala (overlapping speech) ainda fraca** — limitação herdada de pyannote.

## Adequação à Persona (OSS video pipeline)

- **(a) word-level timestamps:** ★★★★★ — o melhor do trio
- **(b) multi-language + Portuguese:** ★★★★☆ — pt suportado nativamente, mas WER pt-BR específico não está em bench público
- **(c) Mac M / Linux GPU:** ★★★★☆ — Linux GPU excelente; Mac OK mas inferior a whisper.cpp
- **(d) Python pipeline:** ★★★★☆ — API Python rica, mas dependências pesadas
- **(e) diarization:** ★★★★★ — único com integração pronta

## Fontes

- README: https://github.com/m-bain/whisperX
- Paper: https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf
- Modal blog: https://modal.com/blog/choosing-whisper-variants
- Discussion #684 (openai/whisper): https://github.com/openai/whisper/discussions/684
- pyannote 3.1: https://huggingface.co/pyannote/speaker-diarization-3.1
