# Battle Card — ASR Engines (1-page)

| | **WhisperX** | **faster-whisper** | **whisper.cpp** |
|---|---|---|---|
| **Repo** | m-bain/whisperX | SYSTRAN/faster-whisper | ggml-org/whisper.cpp |
| **Licença** | BSD-2-Clause | MIT | MIT |
| **Linguagem** | Python (envolve faster-whisper) | Python + C++ (CTranslate2) | C/C++ puro |
| **WER (pt agregado)** | ~9% (base Whisper large-v3) | ~9% | ~9% (fp16) / +1–3 pts em q4 |
| **Word timestamps** | ★★★★★ ±50 ms (wav2vec2 forced align) | ★★★★☆ via cross-attention | ★★★☆☆ drift 300–800 ms |
| **Diarização** | ★★★★★ pyannote integrado | ★★★☆☆ plug manual | ★☆☆☆☆ fora do escopo |
| **Linux GPU (NVIDIA)** | ★★★★★ ~70× RT batched | ★★★★★ 4× faster que Whisper original | ★★☆☆☆ CUDA experimental |
| **Mac M-series** | ★★★☆☆ MPS, ~5.5× RT | ★★★☆☆ CPU only | ★★★★★ Metal+CoreML+ANE, ~10× RT |
| **CPU x86** | ★★★★☆ herda faster-whisper | ★★★★★ ~2× faster que whisper.cpp | ★★★☆☆ |
| **DX Python** | ★★★★☆ rich API, instalação chata | ★★★★★ idiomático, melhor do trio | ★★★☆☆ bindings 2nd class |
| **Footprint / cold start** | pesado | médio (~1.8s) | leve (<300 ms) |
| **Multi-language** | 99 idiomas + 10 com phoneme align (pt incluso) | 99 idiomas | 99 idiomas |
| **Setup atrito** | torch + pyannote + HF token | pip + cuDNN9/CUDA12 (GPU) | CMake build + CoreML script |

## Quando escolher cada um

**WhisperX** quando:
- Precisa **subtitling de qualidade** (highlight word-by-word)
- Precisa **diarização** (quem disse o quê)
- Pipeline rodando em **Linux GPU** (NVIDIA)
- Pode arcar com setup pesado (torch + pyannote + HF token)

**faster-whisper** quando:
- Precisa de **maior throughput em Linux GPU** sem features extras
- Quer **DX Python idiomática** e zero atrito legal (MIT)
- Pode investir ~1 dia de glue code para diarização (pyannote)
- Não quer dependência de torch/wav2vec2

**whisper.cpp** quando:
- Pipeline rodando **predominantemente em Mac M-series**
- Quer **binário standalone** (edge, desktop app, mobile)
- **Não precisa diarização**
- DX Python é OK ser via subprocess CLI

## Top-line VERDICT (OSS video pipeline)

🏆 **WhisperX** é o pick padrão para pipeline OSS de edição de vídeo:
- single library entrega word-ts + diarização + multi-language pt
- substitui Submagic/Eddie AI com ~1 dia de integração

⚠️ **faster-whisper** é o fallback se diarização não importa OU air-gapped (sem HF token).

🍏 **whisper.cpp** vira engine secundária para preview rápido em Mac dev, **não motor único**.

## Custos hidden

- WhisperX: pyannote model é CC-BY-4.0 → atribuição obrigatória em produto comercial
- faster-whisper: setup CUDA 12 + cuDNN 9 em CI exige imagem Docker NVIDIA
- whisper.cpp: primeiro run com CoreML é lento (compilação ANE), precisa warm-up

## Sources (top)

- https://github.com/m-bain/whisperX
- https://github.com/SYSTRAN/faster-whisper
- https://github.com/ggml-org/whisper.cpp
- https://www.isca-archive.org/interspeech_2023/bain23_interspeech.pdf
- https://modal.com/blog/choosing-whisper-variants
