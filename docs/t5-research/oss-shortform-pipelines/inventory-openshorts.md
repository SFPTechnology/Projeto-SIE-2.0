# Inventory — OpenShorts

**Repo:** https://github.com/mutonby/openshorts
**Tagline:** *"Free & open source AI video platform — Clip Generator, AI Shorts (UGC with AI actors) & YouTube Studio. Self-hosted, no watermarks."*

## Identidade & Atividade

| Atributo | Valor | Fonte |
|---|---|---|
| Stars | 1.819 | [GitHub API repos/mutonby/openshorts](https://api.github.com/repos/mutonby/openshorts) |
| Forks | 488 | idem |
| Issues abertas | 22 | idem |
| Linguagem dominante | JavaScript (frontend) + Python (backend) | idem |
| Licença | MIT | idem |
| Criado em | 2025-12-19 | idem |
| Último commit | 2026-05-06 12:57 UTC | [GitHub commits](https://github.com/mutonby/openshorts/commits/main) |
| Commits últimos 90d | **39** | API `commits?since=2026-02-06` |
| Releases formais | 0 (sem tags) | API `releases` (vazio) |
| Default branch | `main` | API |
| Tamanho do repo | 77 MB | API |

**Sinal de atividade:** ALTÍSSIMO. 9 commits no dia 2026-05-06 (dia do bench). Repo é greenfield (5 meses de idade) com release-mode contínuo, ainda em hardening de marketing/legal (commits recentes adicionam Terms & Privacy, ownership attestation, drop de mentions de "long YouTube videos").

## Stack & Dependências

**Backend (Python 3.11):**
- `fastapi==0.136.1`, `uvicorn==0.46.0`
- `faster-whisper==1.2.1` — transcrição word-level
- `google-genai==1.75.0` — viral moment detection + scripts + thumbnails
- `mediapipe==0.10.14` + `ultralytics==8.4.46` (YOLOv8) — face tracking 9:16
- `scenedetect==0.7` (PySceneDetect) — boundary detection
- `torch==2.11.0`, `torchvision==0.26.0`
- `boto3==1.43.4` — S3
- `yt-dlp` — ingest de URL
- `httpx==0.28.1` — fal.ai/ElevenLabs/Upload-Post

**Frontend:**
- React 18 + Vite 4 + Tailwind 3.4

**Infra:**
- Docker + Docker Compose
- Remotion (subdir `remotion/` para render programático)
- AWS S3 (clips privados + galeria pública)

**APIs externas obrigatórias:**
- Google Gemini (free tier generoso)
- fal.ai (pay-per-use, ~$0.50–1.50/AI Short)
- ElevenLabs (free tier)
- Upload-Post (10 vids grátis/mês)

Fonte: [requirements.txt](https://github.com/mutonby/openshorts/blob/main/requirements.txt) + [README](https://github.com/mutonby/openshorts/blob/main/README.md).

## Features (declaradas no README)

### Clip Generator (long-form → shorts)
1. Ingest local ou yt-dlp
2. Transcrição via faster-whisper word-level
3. Boundary detection via PySceneDetect
4. **Viral moment detection** via Gemini 3.0 Flash (3-15 momentos, 15-60s cada)
5. Cut FFmpeg preciso
6. **9:16 reframing dual-mode**: TRACK (MediaPipe + YOLOv8 face tracking) ou GENERAL (blurred bg)
7. Subtitles burned ASS + word highlighting
8. **Hook text overlays** AI-generated
9. **AI Video Effects** via filtros FFmpeg gerados pela Gemini
10. **Voice dubbing 30+ idiomas** via ElevenLabs

### AI Shorts (UGC com atores AI)
- Pipeline: scrape URL → script → ator (Flux 2 Pro) → voz (ElevenLabs) → talking head (Hailuo 2.3 Fast + VEED Lipsync) → B-roll (Flux 2 Pro + Ken Burns) → composite FFmpeg → publish
- Modos: Low Cost (~$0.65/vídeo) e Premium (~$2/vídeo)

### YouTube Studio
- Thumbnails AI com face overlay
- 10 viral title suggestions com refinement chat
- Auto-descriptions com chapter timestamps
- One-click publish YouTube

### Social Auto-Publishing
- TikTok + Instagram Reels + YouTube Shorts simultâneo
- Schedule uploads
- Async upload via Upload-Post

### Infra
- S3 backup
- SEO gallery JSON-LD
- Async job queue com `MAX_CONCURRENT_JOBS`
- Auto-cleanup 1h
- API keys encrypted client-side

## Setup Effort

```
git clone ... && docker compose up --build
# http://localhost:5175
```

**Setup real:** Docker + 4 API keys (Gemini grátis, fal.ai/ElevenLabs/Upload-Post pagos). Tempo estimado: **10-30 min** (clone + keys). Sem build manual de wheels Python.

**Friction points:**
- 4 contas externas obrigatórias
- AWS S3 opcional mas necessário p/ galeria pública
- Custos AI: ~$0.50-2/vídeo em AI Shorts

## Sinais de saúde do projeto

- 39 commits/90d, 22 issues, 488 forks → **ativo e adotado**
- Sem releases tagged ainda → maturidade pré-1.0
- README extremamente polido (comparativo vs Opus Clip / CapCut / Vizard / Klap / Descript)
- Commits recentes mostram pivô de "long YouTube videos" (provavelmente DMCA-driven) → projeto tem ownership ativo do criador

## Watermark / Render / Output

- **Watermark:** NUNCA (declarado no README, "no watermarks, no limits")
- **Render:** FFmpeg (composição final) + Remotion (render programático para casos selecionados)
- **Output:** MP4 9:16 (1080×1920) ou 16:9, S3 backup opcional

## Equivalência funcional vs Submagic

| Submagic feature | OpenShorts? |
|---|---|
| Auto-captions animadas | Sim — faster-whisper + ASS burned |
| B-roll automático | Sim — Flux 2 Pro generation + Ken Burns (AI Shorts) |
| Highlight clipping de podcast | Sim — Gemini viral moment detection |
| 9:16 smart reframe | Sim — dual-mode TRACK/GENERAL |
| Hook overlays | Sim — Gemini-generated |
| Multi-platform publish | Sim — Upload-Post API |
| AI Avatar / UGC | Sim — Flux 2 Pro + Hailuo + VEED Lipsync |

## Riscos

- **Idade do repo (5 meses):** API breaking changes prováveis
- **Dependência de fal.ai:** 80% das features AI passam por lá; mudança de pricing afeta o produto
- **Sem testes automatizados visíveis** no top-level
- **CLAUDE.md no repo** sugere que foi parcialmente desenvolvido com Claude Code → forks podem ter conflitos com o style do mantenedor
