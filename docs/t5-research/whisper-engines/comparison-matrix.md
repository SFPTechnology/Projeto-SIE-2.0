# Matriz Comparativa — WhisperX vs faster-whisper vs whisper.cpp

> Escala: Forte 5/5 · Parcial alta 4/5 · Parcial 3/5 · Fraco 2/5 · Sem equivalente 1/5
>
> Lente aplicada: pipeline OSS de edição de vídeo (substituto Submagic/Eddie AI), com B-roll automatizado por transcript, multi-language com pt-BR, Mac M-series + Linux GPU.

## Matriz Principal

| Dimensão | WhisperX | faster-whisper | whisper.cpp | Vencedor |
|---|---|---|---|---|
| **Acurácia base (WER)** | 5/5 — usa Whisper large-v2/v3 sem perda | 5/5 — pesos Whisper inalterados, paridade com OpenAI | 4/5 — paridade em fp16; quantização q4/q5 pode somar 1–3 pts WER em pt | faster-whisper / WhisperX (empate) |
| **Velocidade — Linux GPU NVIDIA** | 5/5 — até ~70× RT batched (a base é faster-whisper) | 5/5 — 4× sobre Whisper original; CUDA classe mundial | 2/5 — backend CUDA instável, geralmente mais lento | faster-whisper / WhisperX |
| **Velocidade — Mac M-series** | 3/5 — roda em MPS, ~5.5× RT | 3/5 — só CPU; sem Metal/ANE | 5/5 — Metal+CoreML+ANE, ~10× RT em M2 Pro com large-v3-turbo | **whisper.cpp** |
| **Velocidade — CPU x86** | 4/5 — herda perf do faster-whisper | 5/5 — int8 + Apple Accelerate / oneDNN; ~2× faster que whisper.cpp | 3/5 — perde para faster-whisper em CPU server | faster-whisper |
| **Word-level timestamps (qualidade)** | 5/5 — ±50 ms via wav2vec2 forced alignment | 4/5 — nativo via cross-attention; bom mas com drift | 3/5 — disponível, drift 300–800 ms em fala complexa | **WhisperX** |
| **Cobertura multi-language** | 4/5 — 99 idiomas Whisper + 10 com phoneme alignment default (`pt` incluso) | 5/5 — 99 idiomas Whisper, sem dependência de phoneme model | 5/5 — 99 idiomas Whisper, mesmo backbone | faster-whisper / whisper.cpp |
| **Português (pt-BR / pt-PT) específico** | 5/5 — phoneme alignment `pt` na caixa, WER ~9% agregado CV15 | 5/5 — WER ~9% agregado; sem alinhamento dedicado mas word-ts via attention funciona | 4/5 — mesmo WER em fp16; cuidar quantização agressiva | WhisperX (margem fina) |
| **Diarização (integração nativa)** | 5/5 — pyannote.audio plug-and-play, mapping word↔speaker pronto | 3/5 — não nativo; integração documentada com pyannote | 1/5 — fora do escopo do projeto | **WhisperX** |
| **VAD pré-processamento** | 5/5 — VAD-cut do paper, batched | 4/5 — Silero VAD opcional via flag | 3/5 — plugável mas não default | WhisperX |
| **Hardware fit — fleet misto Mac+Linux** | 4/5 — Linux GPU forte, Mac OK | 4/5 — Linux GPU forte, Mac OK (CPU) | 3/5 — Mac forte, Linux GPU fraco | empate WhisperX/faster-whisper |
| **Licença / atrito legal** | 4/5 — BSD-2-Clause + dependência de pyannote (CC-BY-4.0 modelo + HF token gated) | 5/5 — MIT puro, zero atrito | 5/5 — MIT puro, zero atrito | faster-whisper / whisper.cpp |
| **Esforço de instalação (greenfield)** | 3/5 — torch + pyannote + CTranslate2; conflitos comuns; HF token pra diarização | 4/5 — `pip install faster-whisper` + cuDNN/CUDA no host se GPU | 3/5 — build CMake + CoreML script (Mac); binários pré-buildados ajudam | faster-whisper |
| **DX Python pipeline** | 4/5 — API Python rica, módulos `align`/`diarize` separáveis | 5/5 — generator idiomático, melhor DX do trio | 3/5 — bindings funcionam mas API é segunda-classe | **faster-whisper** |
| **Footprint memória / startup** | 3/5 — pesado: torch + pyannote + wav2vec2 | 3/5 — Python + CTranslate2, startup ~1.8s | 5/5 — binário C++, startup <300 ms | **whisper.cpp** |
| **Maturidade do projeto** | 4/5 — paper Interspeech 2023, mantido com forks de manutenção | 5/5 — SYSTRAN corporativo, releases regulares | 5/5 — Gerganov, lançamentos contínuos, ecossistema ggml | faster-whisper / whisper.cpp |
| **Comunidade / ecossistema** | 4/5 — forte em pesquisa e tooling; vários forks | 5/5 — base de praticamente todo wrapper Python pós-OpenAI | 5/5 — base de apps desktop/mobile, bindings em todas as linguagens | faster-whisper / whisper.cpp |
| **Streaming / low-latency** | 2/5 — design batch-first | 3/5 — possível mas não é o forte | 4/5 — startup baixo + binário enxuto facilita streaming | whisper.cpp |
| **Determinismo / reprodutibilidade** | 3/5 — alinhamento e diarização adicionam fontes de variância | 4/5 — bom, depende do beam | 5/5 — C++ puro, sem random Python | whisper.cpp |

## Resumo por Vencedor

| Categoria | Vencedor |
|---|---|
| Acurácia em pt | **WhisperX** (margem fina sobre faster-whisper) |
| Linux GPU throughput | **faster-whisper** |
| Mac M-series throughput | **whisper.cpp** |
| Word timestamps de subtitling | **WhisperX** |
| Diarização integrada | **WhisperX** (único do trio) |
| DX Python | **faster-whisper** |
| Footprint / cold start | **whisper.cpp** |
| Atrito legal | **faster-whisper** / **whisper.cpp** (empate, MIT) |
| Pipeline de vídeo OSS (composto) | **WhisperX** |

## Notas

1. **WhisperX usa faster-whisper sob o capô** — quando você roda WhisperX, está rodando faster-whisper + alignment + diarization. As linhas "Acurácia base" e "Linux GPU" empatam por isso.
2. **whisper.cpp domina Apple Silicon, faster-whisper domina Linux GPU.** Não há um vencedor único cross-hardware; a escolha depende do alvo majoritário.
3. **Diarização gated:** WhisperX depende de aceitar termos pyannote no HF; em ambiente air-gapped isso é bloqueador.
4. **Quantização em whisper.cpp para pt-BR:** q5_1 é seguro; q4 começa a degradar WER perceptivelmente.

## Fontes (resumo)

- Modal blog: https://modal.com/blog/choosing-whisper-variants
- WhisperX paper: https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf
- Voicci Apple Silicon bench: https://www.voicci.com/blog/apple-silicon-whisper-performance.html
- mac-whisper-speedtest: https://github.com/anvanvan/mac-whisper-speedtest
- whisper.cpp bench thread: https://github.com/ggml-org/whisper.cpp/issues/89
- OpenAI large-v3 release notes: https://github.com/openai/whisper/discussions/1762
