# Battle Card — Submagic vs Eddie AI

> 1-page quick reference. Para decisão rápida ou conversa de 2 min.

## TL;DR

- **Submagic** = Editor final de short-form. Você sai com vídeo polido pronto pra postar.
- **Eddie AI** = Assistente pré-edit pra pros. Você sai com rough cut + metadata pra abrir no Premiere/Resolve/FCP.
- **Eles NÃO competem 1:1.** Resolvem problemas adjacentes.

## Quem é

| | Submagic | Eddie AI |
|---|---|---|
| Tipo | Web SaaS (cloud) | Desktop app (Mac/Win, GPU local) |
| Job-to-be-done | "Cria meu short polido em 5 min" | "Loga e prepara meu rough cut" |
| Persona-alvo | Solo creator, social media manager | Documentary filmmaker, podcast producer |
| Output final | MP4 1080p-4K pronto pra TikTok/Reels/Shorts | XML pra Premiere/Resolve/FCP |
| Renderiza? | ✅ Sim (cloud) | ❌ Não (delega ao NLE) |

## Pricing

| | Free | Entrada | Top tier |
|---|---|---|---|
| Submagic | 5 vid/mês watermark | $24/mês (Pro) | $54/mês (Business 4K) |
| Eddie AI | 5 A-roll / 25 B-roll | $21/mês (Plus) | $333/mês (Pro+ 3 seats) |

## Feature highlights

### Submagic ganha em
- ✅ Captions animados word-by-word (best-in-class)
- ✅ Layouts split-screen nativos (`split-50-50`, `split-35-65`)
- ✅ Auto-translate 100+ idiomas
- ✅ AI Avatar generator (120+ avatares)
- ✅ Magic Zoom + Eye Contact AI
- ✅ Direct social publishing
- ✅ REST API público

### Eddie AI ganha em
- ✅ **Semantic visual search** ("office chaos" → planos certos sem tag)
- ✅ Multicam sync até 6 câmeras
- ✅ Speaker identification + diarization
- ✅ XML export Premiere/Resolve/FCP
- ✅ BRAW / R3D support (Pro+)
- ✅ Chat-prompt edit ("pull 3 best soundbites on leadership")
- ✅ Night Shift (processa overnight)
- ✅ Rough cut frameworks (narrative templates)

## Quando escolher cada um

```
Você grava no celular, posta em Reels?           → Submagic
Você faz documentário/podcast multi-cam?         → Eddie AI
Você quer publicar direto sem abrir NLE?         → Submagic
Você termina no Premiere/Resolve/FCP?            → Eddie AI
Você precisa de captions virais polidos?         → Submagic
Você tem >50h de B-roll próprio organizado?      → Eddie AI
Você quer chat tipo "edita assim"?                → Eddie AI
Seu workflow é >5min, longform?                  → Eddie AI
Seu workflow é <90s vertical?                    → Submagic
Quer pagar <$30/mês?                              → Submagic
Tem orçamento $167+/mês e cliente exigente?       → Eddie AI
```

## OSS substitution lens (a pedido)

| Quem é mais "clonável" em OSS? | **Eddie AI ganha** |
|---|---|

- Eddie produz **metadata** (XML, transcripts taggeados, timestamps). Stack OSS resolve ~80% (faster-whisper + CLIP + FAISS + pyannote + Llama local + OpenTimelineIO).
- Submagic produz **vídeo renderizado polido**. Stack OSS resolve ~50%, mas o polish (captions templates, eye contact, avatares) cria gap visível.

## Veredicto

**Não escolha um vs outro. Escolha qual problema você resolve hoje:**

- Solo creator finalizando vídeo? **Submagic.**
- Pro com NLE workflow? **Eddie AI.**
- Híbrido? **Os dois** (Eddie para rough → exporta → Submagic para shorts derivados).

Para a sua intenção declarada (caçar OSS substituto), **comece pelo Eddie AI** — o pipeline é mais clonável e cada componente já tem OSS forte hoje.
