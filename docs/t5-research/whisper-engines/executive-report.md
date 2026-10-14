# Executive Report — ASR Engine Pick para Pipeline OSS de Vídeo (Substituto Submagic / Eddie AI)

> **Data:** 2026-05-06
> **Requester:** Alan Nicolas (Sinkra Hub)
> **Bench correlato:** `docs/bench/submagic-vs-eddie-ai/`
> **Decisão pedida:** escolher UM motor ASR para a camada speech-to-text do pipeline.

## TL;DR — Verdict

> **Pick: WhisperX** (com fallback documentado para faster-whisper se diarização não for usada ou se ambiente air-gapped).

Justificativa em uma frase: WhisperX é a única opção do trio que entrega **word-level timestamps de qualidade subtitling (±50 ms) + diarização integrada + suporte oficial a português** numa única lib Python — exatamente o feature set que diferencia Submagic/Eddie AI e que você precisa pra B-roll match transcript-driven.

## Scoreboard

| Engine | Persona-weighted | P0s | Tempo de integração estimado |
|---|---:|---:|---|
| **WhisperX** | **83.8** | 1 (HF token) | ~1 dia |
| **faster-whisper** | **89.9** | 1 (sem diarização) | ~1 dia + 1 dia de glue pyannote |
| **whisper.cpp** | **80.1** | 2 (sem diarização + Linux GPU fraco) | inviável como motor único |

Score numérico favorece faster-whisper, mas o **delta de feature** (diarização + word-ts ±50 ms) que WhisperX traz pronto vale mais que os ~6 pontos no scorecard composto, dado o caso de uso.

## Raciocínio de Decisão

### Por que WhisperX?

1. **Cobre TODAS as 5 dimensões do pedido** (a-e):
   - (a) word-ts ±50 ms → ✅ wav2vec2 forced alignment
   - (b) multi-language + pt → ✅ phoneme model `pt` na caixa
   - (c) speed Mac+Linux GPU → ✅ Linux GPU 70× RT; Mac OK (~5.5× RT)
   - (d) Python DX → ✅ API rica
   - (e) diarização → ✅ pyannote integrado, mapping word↔speaker pronto

2. **A alternativa "faster-whisper + pyannote manual" já existe encapsulada como WhisperX.** Construir você mesmo é reinventar a roda — gasta ~1 dia para cobrir o que WhisperX entrega + você fica com glue code para manter.

3. **Substitui Submagic/Eddie AI funcionalmente.** O diferencial visual de Submagic (B-roll match + word-highlight + speaker labeling) sai diretamente de WhisperX; o resto (B-roll selection, asset matching) é layer acima.

4. **Licença BSD-2-Clause é clean** para uso comercial — apenas atenção à atribuição de pyannote (CC-BY-4.0).

### Por que NÃO faster-whisper como pick #1

- Excelente DX e melhor score composto, **mas falta diarização nativa**. Para pipeline de vídeo com 2+ falantes (entrevistas, podcasts, lives) você acaba reconstruindo WhisperX manualmente.
- É a escolha certa se: (a) você só edita vídeo single-speaker, ou (b) o ambiente é air-gapped e você não pode aceitar o termo do pyannote no HF.

### Por que NÃO whisper.cpp

- Sem diarização (escopo do projeto não inclui).
- Linux GPU é fraco — backend CUDA instável.
- Word-ts com drift 300–800 ms degrada subtitling.
- **MAS:** é o melhor para Apple Silicon. Recomendamos manter whisper.cpp como **engine secundária para preview rápido em Mac dev**, não motor único.

## Confidence Breakdown

| Claim | Confidence | Base de evidência |
|---|---|---|
| WhisperX entrega word-ts ±50 ms | **alta** | Paper Interspeech 2023 (peer-reviewed) |
| WhisperX suporta pt nativamente | **alta** | README oficial lista `pt` entre os 10 idiomas com phoneme alignment default |
| faster-whisper é mais rápido em Linux GPU que whisper.cpp | **alta** | Modal blog + community benches |
| whisper.cpp é mais rápido em Mac M-series | **alta** | Voicci bench + mac-whisper-speedtest + HN consensus |
| WER pt-BR específico de cada engine | **média** | Sem head-to-head público dedicado a pt-BR; inferimos de WER agregado Common Voice 15 (~9%) — pesos Whisper são iguais, então diferença vem de quantização e VAD |
| Diarização do pyannote 3.1 + WhisperX é estado-da-arte OSS | **alta** | Model card + WhisperX paper |
| Setup CUDA do faster-whisper exige cuDNN 9 + CUDA 12 | **alta** | README oficial |
| Atrito legal de pyannote (CC-BY-4.0) | **alta** | Model card explicitamente |

**Risk áreas:**
- WER pt-BR com áudio real do seu pipeline pode variar — **fazer um bench de 30 min** com 3 amostras (entrevista limpa, podcast com música de fundo, áudio de webcam) antes de fechar a decisão.
- pyannote 3.1 ainda tem fraqueza em overlapping speech — se seus vídeos têm muito 2-falando-junto, considerar pré-processamento estéreo.
- Forks de WhisperX (BetterWhisperX) existem por gaps de manutenção upstream — pin commit hash + monitorar.

## Plano de Adoção (Next Steps)

### Sprint 0 — Validação (2-3 dias)

1. **Bench empírico em pt-BR** (½ dia)
   - 3 áudios: (a) entrevista 1:1 limpa, (b) podcast 2 falantes com música, (c) call multi-speaker com webcam
   - Métricas: WER manual em ~30s de transcrição × 3, RTF, qualidade de timestamps
   - Roda WhisperX + faster-whisper + whisper.cpp lado a lado

2. **Setup ambiente WhisperX** (½ dia)
   - Container Docker com torch + pyannote + faster-whisper pinados
   - HF_TOKEN em secret manager
   - Aceitar termo de uso em pyannote/speaker-diarization-3.1 + segmentation

3. **Smoke test pipeline** (1 dia)
   - Receber arquivo MP4 → ffmpeg → WhisperX (transcribe + align + diarize) → JSON com words+speakers+timestamps
   - Validar que JSON é consumível pelo módulo de B-roll match

### Sprint 1 — Integração (1 semana)

4. Engine adapter: `whisper-adapter` com interface estável (`transcribe(audio_path) -> WordSegment[]`) para permitir trocar engine futuramente
5. Fallback path: `whisper-adapter` aceita `engine=faster-whisper` (sem diarização) para clipes single-speaker
6. Mac dev mode: `engine=whisper-cpp` para preview rápido (sem diarização, sem word-ts top-tier) durante edição local

### Riscos e Decisões pendentes

- ⚠️ **Validar empiricamente word-ts em pt-BR** com fala disfluente (gírias BR, hesitações). O paper foi validado em EN/AMI/Switchboard — pt-BR pode comportar-se diferente.
- ⚠️ **Decidir compute target primário:** se o pipeline rodar em Mac (laptop dev), WhisperX é OK mas mais lento. Se rodar em GPU server (Linux), é otimal.
- ⚠️ **Política de attribution pyannote** se o produto for comercializado.

## Composite confidence: **HIGH** para o veredito (pick WhisperX), **MEDIUM** para os números RTF/WER específicos

A literatura de 2025 é consistente nas três conclusões fundamentais:
1. WhisperX é único com diarização + word-ts top-tier
2. faster-whisper domina Linux GPU
3. whisper.cpp domina Apple Silicon

Variâncias quantitativas existem mas não invertem o ranking para o caso de uso.

## Fontes principais

- WhisperX paper (Interspeech 2023) — https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf
- WhisperX README — https://github.com/m-bain/whisperX
- faster-whisper README — https://github.com/SYSTRAN/faster-whisper
- whisper.cpp README — https://github.com/ggml-org/whisper.cpp
- Modal — Choosing between Whisper variants — https://modal.com/blog/choosing-whisper-variants
- OpenAI Whisper large-v3 release notes — https://github.com/openai/whisper/discussions/1762
- Voicci Apple Silicon Whisper benchmarks — https://www.voicci.com/blog/apple-silicon-whisper-performance.html
- pyannote 3.1 model card — https://huggingface.co/pyannote/speaker-diarization-3.1

Lista completa: ver `metadata.json#sources`.
