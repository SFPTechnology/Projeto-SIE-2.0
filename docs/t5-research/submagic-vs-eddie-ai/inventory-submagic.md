# Inventory — Submagic

**Site:** https://www.submagic.co/
**Categoria:** AI short-form video editor (transcript-driven)
**Plataforma:** Web-only (Chrome, desktop-first; mobile browser limitado)
**Origem:** França
**Confidence:** HIGH (oficial + API docs + reviews 2026)

## Identidade do produto

> "Edit shorts 10x faster with AI" — único job-to-be-done: transformar bruto → short polido para TikTok/Reels/Shorts.

NÃO é editor de uso geral — não tem timeline tradicional, color grading, multi-track audio mixing.

## Inventário de features (categorizado)

### A. Captions & Transcrição
- [F-SM-01] Speech-to-text 100+ idiomas, **99%+ accuracy**
- [F-SM-02] Subtitle template library + editor completo de subtitle
- [F-SM-03] Custom vocabulary/dictionary (termos técnicos, nomes de marca)
- [F-SM-04] Green-screen export de captions (para usar em After Effects/Premiere)
- [F-SM-05] Auto-translate em 100+ idiomas com sincronização

### B. Silence & audio cleanup
- [F-SM-06] Silence removal (corta dead air automático)
- [F-SM-07] Filler word removal ("um", "uh")
- [F-SM-08] Clean Audio (improve sound quality)
- [F-SM-09] Remove Bad Takes (AI detecta takes ruins)

### C. B-Roll & Visuais
- [F-SM-10] B-roll contextual via Storyblocks library
- [F-SM-11] **Upload de mídia própria → "My videos" library persistente cross-projeto**
- [F-SM-12] Imagens, GIFs, sound effects, transições com emojis animados
- [F-SM-13] **Layouts de B-roll nativos:** `cover`, `contain`, `rounded`, `square`, `split-50-50`, `split-35-65`, `split-50-50-bordered`, `split-35-65-bordered`, `pip-top-right`, `pip-bottom-right`
- [F-SM-14] Magic AI B-roll one-click (lê transcript, insere automático, slider de densidade)

### D. Auto-zoom & transições
- [F-SM-15] One-Click Magic Zoom (zooms suaves automáticos)
- [F-SM-16] Transições automáticas

### E. Música & sound
- [F-SM-17] Built-in music library (trendy + premium)
- [F-SM-18] Upload música própria

### F. Outros AI tools
- [F-SM-19] Generate Hook Title (intro automático)
- [F-SM-20] Correct Eye Contact (mantém eye contact com câmera)
- [F-SM-21] Magic Clips (extrai melhores momentos de long-form → shorts)
- [F-SM-22] AI Avatar Video Generator (120+ avatares + lip-sync)
- [F-SM-23] Generate descriptions + hashtags para social

### G. Workflow
- [F-SM-24] **Edit-by-transcript** (delete frase no texto = remove footage)
- [F-SM-25] Timeline mode opcional (alternativa ao transcript)
- [F-SM-26] Trim tab antes de styling

### H. Colaboração & branding
- [F-SM-27] Shared workspace para times
- [F-SM-28] Brand Kit (logos, fonts, colors auto-aplicados) — Pro/Business

### I. Publishing & export
- [F-SM-29] Multi-platform scheduling (TikTok, Reels, Shorts direto)
- [F-SM-30] Export até 4K 60fps (Business); Pro 2K; Starter 1080p/30fps
- [F-SM-31] **Public REST API** (`docs.submagic.co`) para automação

### J. Upload
- [F-SM-32] Drag-and-drop MP4/MOV até 3GB
- [F-SM-33] QR code upload do celular
- [F-SM-34] Google Drive import

## Pricing (2026)

| Tier | Preço | Limite |
|---|---|---|
| Free | $0 | 5 vídeos/mês com watermark, 1080p, limitado |
| Starter | ~$10/mês | 1080p/30fps, sem watermark |
| Pro | $24/mês | 2K, custom templates, Brand Kit |
| Business | $54/mês | 4K/60fps, team workspace |

## Persona-fit

- 🎯 **Target:** Solo creators, social media managers, agências short-form
- 🎯 **Output esperado:** TikTok, Instagram Reels, YouTube Shorts, vertical 9:16
- ❌ **NÃO atende:** Documentário longo, podcast multi-cam pesado, filmmaker pro com NLE workflow

## Dependências externas (relevante para OSS-substitution)

| Componente | Vendor | Substituível por OSS? |
|---|---|---|
| Speech-to-text | Provavelmente Whisper-based ou proprietary | ✅ Whisper (faster-whisper) |
| Stock B-roll | **Storyblocks** (paid library) | ⚠️ Pexels/Pixabay free APIs |
| Music library | Submagic curated | ⚠️ YouTube Audio Library, Free Music Archive |
| AI avatars | Proprietary | ⚠️ HeyGen-like, SadTalker (OSS, qualidade menor) |
| Render engine | Cloud (web-only) | ✅ FFmpeg + Remotion/Motion Canvas |
| Eye contact AI | Proprietary | ⚠️ NVIDIA Maxine (proprietary), poucos OSS robustos |
