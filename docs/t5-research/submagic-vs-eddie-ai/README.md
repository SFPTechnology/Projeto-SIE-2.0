# Bench — Submagic vs Eddie AI

**Lente:** Feature extraction para substituição open-source
**Data:** 2026-05-06
**Solicitado por:** Alan Nicolas (@oalanicolas)
**Status:** Completed

## TL;DR

- **Submagic** ($0-54/mês) = editor final short-form, gera MP4 polido pra postar.
- **Eddie AI** ($0-333/mês) = assistente pré-edit pro, gera XML pra Premiere/Resolve/FCP.
- Não competem 1:1 — resolvem **problemas diferentes**.
- **Composite scores:** Submagic 82 / Eddie AI 76.
- **Para OSS substitution: Eddie é ~80% clonável, Submagic ~50%.**

## Artefatos

| # | Arquivo | Conteúdo |
|---|---|---|
| 1 | `metadata.json` | Configuração do bench, fontes, confidence |
| 2 | `inventory-submagic.md` | 34 features de Submagic categorizadas |
| 3 | `inventory-eddie-ai.md` | 35 features de Eddie AI categorizadas |
| 4 | `comparison-matrix.md` | Paridade 5/5 - 1/5 em 35 features |
| 5 | `scorecard.md` | 6 dimensões + persona-weighted scoring |
| 6 | `gap-analysis.md` | GAPs bidirecionais + tier OSS substitution |
| 7 | `battle-card.md` | 1-page quick reference |
| 8 | `executive-report.md` | Sumário executivo + recomendações por cenário |
| 9 | `deep/feature-comparison.md` | Análise behavioral por categoria |
| 10 | **`deep/oss-substitution-roadmap.md`** | ⭐ **Stack OSS completo por feature** |

## Quick start

Para a sua intenção (encontrar OSS substituto), comece por:

1. **Leia `deep/oss-substitution-roadmap.md`** — mapa completo de cada feature → OSS top-1 e top-2.
2. **Quick wins (1 dia setup):**
   ```bash
   pip install faster-whisper auto-editor captacity chromadb opentimelineio
   git clone https://github.com/mutonby/openshorts
   ```
3. **Veredicto principal:** Eddie AI é mais clonável. Stack mínimo: WhisperX + SigLIP + ChromaDB + Llama 3.1 + OpenTimelineIO.

## Sources

### Submagic
- https://www.submagic.co/ (oficial)
- https://docs.submagic.co/api-reference/upload-project (API com layouts)
- https://care.submagic.co/ (help center)
- Reviews: thebusinessdive.com, filmora.wondershare.com, aicloudbase.com, ucstrategies.com

### Eddie AI
- https://www.heyeddie.ai/ (oficial)
- https://www.heyeddie.ai/features (features oficial)
- https://help.heyeddie.ai/ (help center)
- Reviews: aichief.com, capterra.com, bestaitools.com, jimgrootes.com, nofilmschool.com, cined.com

### OSS ecosystem
- github.com/SYSTRAN/faster-whisper
- github.com/m-bain/whisperX
- github.com/mlfoundations/open_clip
- github.com/pyannote/pyannote-audio
- github.com/mutonby/openshorts
- github.com/Professor833/video_semantic_search
- github.com/AcademySoftwareFoundation/OpenTimelineIO
- github.com/WyattBlue/auto-editor
- github.com/unconv/captacity
- github.com/remotion-dev/remotion
- github.com/ollama/ollama

## Próxima ação

```bash
# Para deep dive numa camada específica:
/tech-research "WhisperX vs faster-whisper vs whisper.cpp benchmark accuracy speed"

# Para benchmark de tools OSS específicas:
*bench-product "OpenShorts vs MoneyPrinterTurbo vs Captacity"

# Para implementar (NÃO escopo desta skill — pedir @aiox-pm):
@aiox-pm priorizar epic "OSS video pipeline para Sinkra Hub"
```

> **Implementação não é escopo desta skill.** Para construir, acione `@aiox-pm` (priorização) ou `@aiox-architect` (arquitetura).
