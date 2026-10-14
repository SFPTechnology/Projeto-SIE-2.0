# Scorecard — WhisperX vs faster-whisper vs whisper.cpp

> Escala 0-100 por dimensão. Composite = média simples. Persona-weighted = média ponderada para o caso "OSS video editing pipeline".

## Pesos da Persona (OSS video pipeline)

| Dimensão | Peso | Justificativa |
|---|---|---|
| Performance | 0.20 | Vídeo longo (podcasts, cursos) precisa throughput real |
| DX | 0.20 | Pipeline em Python, integração precisa ser limpa |
| Ecosystem | 0.20 | Diarização, VAD, glue libs — quanto mais pronto, menos código |
| Maturity | 0.15 | Pipeline em produção; flakiness custa caro |
| Scalability | 0.15 | Possível processar lote de horas de conteúdo |
| Community | 0.10 | Suporte a longo prazo, plugins, tutoriais |

## Scores Brutos

| Dimensão | WhisperX | faster-whisper | whisper.cpp |
|---|---:|---:|---:|
| **Maturity** | 80 | 92 | 95 |
| **Ecosystem** | 90 | 88 | 82 |
| **DX** | 78 | 92 | 65 |
| **Performance** | 85 | 88 | 80 |
| **Scalability** | 88 | 90 | 75 |
| **Community** | 80 | 90 | 92 |

### Justificativas (Scores Brutos)

**Maturity**
- WhisperX 80 — Paper Interspeech 2023 sólido; manutenção upstream descontínua, forks ativos (BetterWhisperX) compensam
- faster-whisper 92 — SYSTRAN corporativo, releases mensais, base de todo o ecosistema
- whisper.cpp 95 — Gerganov hiper-engajado, lançamentos contínuos, ggml é fundação de llama.cpp também

**Ecosystem**
- WhisperX 90 — pyannote integrado, wav2vec2, várias libs derivam (whisply, etc.)
- faster-whisper 88 — backbone de quase todos os wrappers; integra trivialmente com pyannote/silero
- whisper.cpp 82 — bindings em todas as linguagens, mas ecossistema é mais "embed" que "pipeline"

**DX**
- WhisperX 78 — API rica mas instalação chata (torch + pyannote + HF token)
- faster-whisper 92 — `WhisperModel(...).transcribe()`, generator idiomático, doc clara
- whisper.cpp 65 — bindings Python existem mas são segunda-classe; melhor via subprocess CLI

**Performance**
- WhisperX 85 — 70× RT batched em GPU, mas perde em Mac e tem overhead de alignment+diarization
- faster-whisper 88 — campeão CPU x86 e Linux GPU; Mac apenas OK
- whisper.cpp 80 — campeão Mac (Metal+CoreML), perde Linux GPU e CPU x86

**Scalability**
- WhisperX 88 — batched inference foi feito pra escala; pode chocar com pyannote em hosts grandes
- faster-whisper 90 — base usada em produção em SaaS de transcrição
- whisper.cpp 75 — ótimo para edge/single-machine; menos comum em fleet GPU server

**Community**
- WhisperX 80 — comunidade acadêmica/research forte; menos issues respondidas
- faster-whisper 90 — mantenedor corporativo + comunidade ativa
- whisper.cpp 92 — comunidade enorme via ggml; HN/Twitter constantes

## Composite (média simples)

| Engine | Composite |
|---|---:|
| **faster-whisper** | **90.0** |
| **whisper.cpp** | **81.5** |
| **WhisperX** | **83.5** |

## Persona-Weighted (OSS video pipeline)

Cálculo: `Σ score_i × peso_i`

**WhisperX**
= 85·0.20 + 78·0.20 + 90·0.20 + 80·0.15 + 88·0.15 + 80·0.10
= 17.0 + 15.6 + 18.0 + 12.0 + 13.2 + 8.0
= **83.8**

**faster-whisper**
= 88·0.20 + 92·0.20 + 88·0.20 + 92·0.15 + 90·0.15 + 90·0.10
= 17.6 + 18.4 + 17.6 + 13.8 + 13.5 + 9.0
= **89.9**

**whisper.cpp**
= 80·0.20 + 65·0.20 + 82·0.20 + 95·0.15 + 75·0.15 + 92·0.10
= 16.0 + 13.0 + 16.4 + 14.25 + 11.25 + 9.2
= **80.1**

## Ranking Final (Persona-Weighted)

| # | Engine | Score | Lacuna |
|---|---|---:|---|
| 🥇 | **faster-whisper** | **89.9** | Não tem diarização nem word-ts top-tier nativos |
| 🥈 | **WhisperX** | **83.8** | Stack pesada, Mac mais lento |
| 🥉 | **whisper.cpp** | **80.1** | Sem diarização, DX Python fraca |

## Leitura

O composite favorece **faster-whisper** porque ele é o mais sólido em DX, performance Linux GPU e maturity. Mas:

1. Para o caso de uso real (subtitling + B-roll match + diarização), **WhisperX adiciona ~1 dia de glue code que faster-whisper exigiria**. O score "puro" subestima esse atalho.
2. **whisper.cpp** é o melhor APENAS se o pipeline rodar majoritariamente em Mac M-series e dispensar diarização.

A recomendação final no `executive-report.md` parte do score numérico mas reconcilia com o caso de uso composto.

## Fontes

Ver `metadata.json` para lista completa. Justificativas baseadas em:
- Modal blog — https://modal.com/blog/choosing-whisper-variants
- Repos primários (3 subjects)
- Voicci/Mac speedtest benches
