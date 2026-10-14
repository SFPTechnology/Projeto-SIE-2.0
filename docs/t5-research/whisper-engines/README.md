# Bench: ASR Whisper Engines (WhisperX vs faster-whisper vs whisper.cpp)

> **Data:** 2026-05-06
> **Lente:** pipeline OSS de edição de vídeo (substituto Submagic / Eddie AI), com word-level timestamps, multi-language pt-BR, diarização, fleet Mac M + Linux GPU.
> **Bench correlato:** [`docs/bench/submagic-vs-eddie-ai/`](../submagic-vs-eddie-ai/)

## TL;DR

🏆 **WhisperX** é o pick — único do trio com word-ts ±50 ms + diarização integrada + suporte oficial a `pt` numa lib Python. Score persona-weighted: WhisperX 83.8 / faster-whisper 89.9 / whisper.cpp 80.1; faster-whisper lidera o número composto, mas o delta de feature de WhisperX (que economiza ~1 dia de glue pyannote) compensa.

⚠️ **faster-whisper** é fallback (single-speaker ou air-gapped).
🍏 **whisper.cpp** é engine secundária para preview rápido em Mac dev.

Detalhes em [`executive-report.md`](./executive-report.md).

## Índice de Artefatos

| # | Arquivo | Conteúdo |
|---|---|---|
| 1 | [`metadata.json`](./metadata.json) | Bench config, fontes, confidence levels |
| 2 | [`inventory-whisperx.md`](./inventory-whisperx.md) | WhisperX — features, deps, licença, install, perf |
| 3 | [`inventory-faster-whisper.md`](./inventory-faster-whisper.md) | faster-whisper — idem |
| 4 | [`inventory-whisper-cpp.md`](./inventory-whisper-cpp.md) | whisper.cpp — idem |
| 5 | [`comparison-matrix.md`](./comparison-matrix.md) | Matriz paridade (5/5 → 1/5) em 18 dimensões |
| 6 | [`scorecard.md`](./scorecard.md) | Scores 0–100 (Maturity/Ecosystem/DX/Performance/Scalability/Community) + composite + persona-weighted |
| 7 | [`gap-analysis.md`](./gap-analysis.md) | Lacunas P0/P1/P2 por engine + cross-engine |
| 8 | [`battle-card.md`](./battle-card.md) | 1-page quick reference |
| 9 | [`executive-report.md`](./executive-report.md) | Recomendação concreta + confidence breakdown + plano de adoção |
| 10 | `README.md` | Este índice |

## Quick Verdict por Eixo

| Eixo do pedido | Vencedor |
|---|---|
| (a) word-level timestamps | **WhisperX** (±50 ms) |
| (b) multi-language + pt | empate WhisperX/faster-whisper (pesos Whisper iguais) |
| (c) speed Mac M-series | **whisper.cpp** (Metal+CoreML) |
| (c) speed Linux GPU NVIDIA | **faster-whisper** / **WhisperX** (mesmo backend) |
| (d) Python pipeline DX | **faster-whisper** |
| (e) diarização integrada | **WhisperX** (único) |
| **Composto p/ pipeline OSS de vídeo** | 🏆 **WhisperX** |

## Confidence Geral

- **Verdict:** HIGH — literatura 2025/2026 converge nas três conclusões fundamentais
- **Números RTF/WER específicos:** MEDIUM — não há head-to-head público canônico para pt-BR
- **Action recomendada antes de fechar:** bench empírico de ½ dia com 3 amostras pt-BR reais do pipeline. Ver `executive-report.md#plano-de-adoção`.

## Como Re-rodar Este Bench

1. Ler `metadata.json` para entender escopo e fontes
2. Para atualizar: rodar nova rodada de WebSearch nos termos listados em `metadata.json#sources`, atualizar inventários, recalcular scorecard
3. Manter `executive-report.md#confidence-breakdown` sincronizado

## Cross-references

- `docs/bench/submagic-vs-eddie-ai/` — bench paralelo de produtos comerciais (Submagic vs Eddie AI)
- Próximo bench sugerido: B-roll match engines (PySceneDetect, CLIP-based selectors, etc.) — fora do escopo deste documento

---

*Bench gerado por Universal Bench Analyst (spy-bench-analyst lens) | Sinkra Hub | KISS — bounded scope = ASR engine pick para 1 pipeline*
