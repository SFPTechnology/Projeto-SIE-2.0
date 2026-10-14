# Inventário — whisper.cpp

> Confidence: alta. Repo primário (Georgi Gerganov / ggml-org), benchmarks comunitários robustos.

## Identidade

- **Repo:** https://github.com/ggml-org/whisper.cpp
- **Autor:** Georgi Gerganov (também autor de llama.cpp e ggml)
- **Licença:** MIT
- **Linguagem:** C/C++ puro, sem Python no caminho de execução
- **Status:** ultra-mantido, lançamento contínuo, base para integrações em apps desktop/mobile

## Features

| Feature | whisper.cpp |
|---|---|
| Transcrição base | Port C/C++ do Whisper, usa ggml + quantização própria (q4, q5_0, q5_1, q8) |
| Word-level timestamps | **Sim** (`-ml 1` ou `--output-words`) — derivado de DTW na cross-attention; pode driftar 300–800 ms em fala complexa |
| Speaker diarization | **Não, e nunca terá nativo** — escopo é só transcrição |
| VAD | Plugável (Silero / WebRTC), não default |
| Apple Silicon | **Metal GPU + CoreML/ANE** — best-in-class; +3× sobre CPU |
| Linux GPU | CUDA experimental (`ggml-cuda`); Vulkan/OpenCL existem; geralmente mais lento que faster-whisper em NVIDIA |
| Binding | Bindings oficiais Python, Go, Rust, Node, Swift, Java, Ruby, .NET |
| Footprint | Menor do trio — binário standalone, startup <300 ms |

## Suporte a Português

- Suporta todos os 99 idiomas do Whisper (pesos idênticos).
- `--language pt` ou `auto`.
- WER pt agregado igual a Whisper-OpenAI (~8–15% para large-v3).
- Atenção: quantização q4/q5 pode inflar WER em ~1–2 pontos em línguas medium-resource como pt.

## Stack de Dependências

- Build-time: CMake, C++ compiler, opcional CoreML tools (Apple) ou CUDA toolkit
- Runtime: nenhuma dependência Python obrigatória
- Para CoreML: precisa gerar modelo CoreML uma vez (`./models/generate-coreml-model.sh large-v3`)

## Instalação

```bash
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
# Apple Silicon com CoreML + Metal
cmake -B build -DWHISPER_COREML=1 -DWHISPER_METAL=1
cmake --build build -j --config Release
./build/bin/main -m models/ggml-large-v3.bin -l pt -f audio.wav
```

Pegadinhas:
- Primeira run com CoreML é lenta (compilação ANE) — depois cacheia.
- Para usar via Python, há binding mas é menos idiomático que faster-whisper.
- Quantização q5_1 é o sweet-spot tamanho/qualidade.

## Performance (referência)

- **Apple M2 Pro com CoreML+Metal:** large-v3-turbo q5_0 a ~10× real-time (60s de áudio em ~6s)
- **Boost CoreML+Metal vs CPU only:** ~8–12× (Voice Mode hierarchy); pelo menos 3× só com CoreML
- **vs faster-whisper em Mac M2:** whisper.cpp+CoreML ~3× mais rápido (109s vs 30s para mesmo input em comparação SmartLittleApps)
- **vs faster-whisper em CPU x86:** **perde** — small.en em 46s vs 14s do faster-whisper
- **Cold start:** <300 ms (vs ~1.8s do faster-whisper)
- **Word timestamps:** disponíveis mas qualidade inferior a WhisperX (drift 300–800 ms)

## Pontos Fortes

1. **Único otimizado para Apple Silicon** — Metal + ANE via CoreML, ganho real de 3–10×.
2. **Footprint minúsculo** — binário standalone, sem Python, ideal para edge/desktop apps.
3. **Cold start instantâneo** — ótimo para CLI workflow interativo.
4. **MIT puro** + autor solidamente engajado (Gerganov).
5. **Bindings em quase toda linguagem** — fácil embedar.
6. **Determinismo** — sem random seeds Python, builds reprodutíveis.

## Pontos Fracos

1. **Linux GPU fraco** — CUDA backend instável e geralmente mais lento que faster-whisper em NVIDIA.
2. **CPU x86 pesado** — perde feio para faster-whisper em CPU server.
3. **Sem diarização** — escopo do projeto não cobre.
4. **Word timestamps menos precisos** — drift de 300–800 ms em fala complexa.
5. **DX Python é segunda-classe** — bindings funcionam mas API é menos rica que faster-whisper.
6. **Quantização agressiva degrada WER** — q4 em pt-BR pode somar 2–3 pontos de WER.

## Adequação à Persona (OSS video pipeline)

- **(a) word-level timestamps:** ★★★☆☆ — disponível, qualidade média
- **(b) multi-language + Portuguese:** ★★★★★ — paridade Whisper, mas cuidado com quantização
- **(c) Mac M / Linux GPU:** ★★★★☆ — Mac 5/5; Linux GPU 2/5
- **(d) Python pipeline:** ★★★☆☆ — bindings existem mas DX inferior
- **(e) diarization:** ★☆☆☆☆ — sem suporte nativo

## Fontes

- README: https://github.com/ggml-org/whisper.cpp
- Benchmark Issue #89: https://github.com/ggml-org/whisper.cpp/issues/89
- mac-whisper-speedtest: https://github.com/anvanvan/mac-whisper-speedtest
- Voicci Apple Silicon bench: https://www.voicci.com/blog/apple-silicon-whisper-performance.html
- Hacker News thread CoreML 3×: https://news.ycombinator.com/item?id=43880345
