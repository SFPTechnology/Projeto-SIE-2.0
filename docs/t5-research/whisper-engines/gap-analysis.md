# Gap Analysis — Lacunas por Engine para Pipeline OSS de Vídeo

> Severidade: **P0** (bloqueia adoção sem mitigação) · **P1** (limita escopo, requer workaround) · **P2** (cosmético / nice-to-have)
>
> Lente: substituto OSS de Submagic/Eddie AI rodando em Python, com B-roll match por transcript, multi-language com pt-BR, fleet Mac M + Linux GPU.

## WhisperX

| ID | Severidade | Lacuna | Impacto | Mitigação |
|---|---|---|---|---|
| WX-G1 | **P0** | Diarização exige `HF_TOKEN` + aceitar termo no Hugging Face | Bloqueia ambiente air-gapped; precisa secret management | Documentar setup com `.env` + fallback para fluxo sem diarização (`--diarize=false`) |
| WX-G2 | **P1** | Performance em Mac M-series fica em ~5.5× RT vs ~10× do whisper.cpp | Pipeline em Mac dev fica mais lento | Usar faster-whisper standalone para preview rápido em Mac; WhisperX em job batch (server) |
| WX-G3 | **P1** | Stack pesada (torch + pyannote + wav2vec2 + CTranslate2) — conflitos de versão comuns | Setup chato, regressões em upgrades | Pinning estrito de versões em `requirements.txt`; container Docker dedicado |
| WX-G4 | **P1** | Sobreposição de fala (overlapping speakers) é tratada mal | Calls com 2+ pessoas falando juntas viram bagunça | Pré-processar com canal estéreo separado quando possível; aceitar limite |
| WX-G5 | **P1** | Manutenção upstream foi descontínua em alguns períodos; forks (BetterWhisperX) cobrem | Risco de bug crítico não corrigido a tempo | Avaliar BetterWhisperX como upstream alternativo; pin commit hash |
| WX-G6 | **P2** | Modelo de diarização pyannote é CC-BY-4.0 — atribuição obrigatória em produto comercial | Exige menção legal no produto | Adicionar attribution em "About" / créditos |
| WX-G7 | **P2** | Sem suporte streaming nativo | Para low-latency precisa outra solução | Não impacta pipeline batch de vídeo |

## faster-whisper

| ID | Severidade | Lacuna | Impacto | Mitigação |
|---|---|---|---|---|
| FW-G1 | **P0** | Sem diarização nativa | Pipeline de vídeo com 2+ pessoas precisa identificar speaker | Adicionar pyannote.audio manualmente (~150 linhas de Python para alinhamento word↔speaker) |
| FW-G2 | **P1** | Word-level timestamps são "bons" mas inferiores a WhisperX (cross-attention vs forced alignment) | Subtitle highlight pode ter drift visível em fala disfluente | Pode ser suficiente para B-roll match (granularidade frase/segmento); validar empiricamente |
| FW-G3 | **P1** | Sem aceleração Apple GPU/Metal/ANE | Pipeline em Mac M-series é ~3× mais lento que whisper.cpp | Para preview rápido em Mac, usar whisper.cpp; produção em Linux GPU |
| FW-G4 | **P1** | Setup CUDA exige cuDNN 9 + CUDA 12 corretos no host | Atrito em CI/Docker, especialmente em GPU compartilhada | Imagem Docker base oficial NVIDIA + lock de versão |
| FW-G5 | **P2** | Cold start ~1.8s | Não impacta batch; impacta CLI interativo | Manter daemon/server para reuso de modelo |

## whisper.cpp

| ID | Severidade | Lacuna | Impacto | Mitigação |
|---|---|---|---|---|
| WC-G1 | **P0** | Sem diarização — fora do escopo do projeto e nunca terá | Para pipeline de vídeo multi-speaker é bloqueador | Combinar com pyannote (mas perdendo o atrativo "binário standalone") |
| WC-G2 | **P0** | Linux GPU CUDA backend é instável e geralmente mais lento que faster-whisper | Inviável como motor primário em fleet Linux GPU | Não usar como motor de produção em Linux GPU |
| WC-G3 | **P1** | Word-level timestamps com drift de 300–800 ms em fala complexa | Subtitle word-highlight pode ficar ruim | Aceitar timestamps em granularidade frase, não palavra |
| WC-G4 | **P1** | DX Python é segunda-classe — bindings funcionam mas API menos ergonômica | Mais glue code para integrar em pipeline | Usar via CLI subprocess para builds simples |
| WC-G5 | **P1** | Quantização agressiva (q4) pode somar 2–3 pts WER em pt-BR | Acurácia degradada em conteúdo PT | Usar q5_1 ou fp16 para conteúdo PT crítico |
| WC-G6 | **P2** | Primeira execução com CoreML é lenta (compilação ANE) | UX ruim no primeiro uso de cada modelo | Fazer warm-up no setup do app |

## Lacunas Cross-Engine (compartilhadas)

| ID | Severidade | Lacuna | Aplica a | Mitigação |
|---|---|---|---|---|
| X-G1 | P1 | Nenhum tem alinhamento phoneme treinado especificamente para pt-BR (todos usam wav2vec2 multilingue ou cross-attention) | WhisperX (wav2vec2 multilingue), faster-whisper (cross-attention), whisper.cpp (DTW) | Validar empiricamente em amostras pt-BR; fine-tune wav2vec2 PT se necessário |
| X-G2 | P1 | Sobreposição de fala (overlapping) é fraca em todos | os três | Tratamento ao nível de captura: estéreo + canais separados quando possível |
| X-G3 | P2 | Nenhum embute punctuation restoration de segunda passada para pt-BR especificamente | os três | Whisper já faz pontuação razoável; pós-processar com modelo de punctuation se preciso |

## Mapa P0 → Decisão

- **WhisperX** tem 1 P0 (HF token / gated) → **mitigação trivial** (secret management)
- **faster-whisper** tem 1 P0 (sem diarização) → **mitigação custa ~1 dia eng** (pyannote glue)
- **whisper.cpp** tem 2 P0 (sem diarização + Linux GPU fraco) → **mitigação descaracteriza o produto**

→ A combinação de P0s favorece **WhisperX** quando o pipeline precisa de diarização; **faster-whisper** quando diarização é opcional ou substituível por glue code.
→ **whisper.cpp** é fortíssimo APENAS como engine secundária para Mac dev preview, não como motor único.

## Fontes

- WhisperX issues e forks: https://github.com/m-bain/whisperX/issues/817 · https://github.com/citypages/BetterWhisperX
- faster-whisper Apple Silicon discussion: https://github.com/SYSTRAN/faster-whisper/discussions/368
- whisper.cpp benchmark thread: https://github.com/ggml-org/whisper.cpp/issues/1127
