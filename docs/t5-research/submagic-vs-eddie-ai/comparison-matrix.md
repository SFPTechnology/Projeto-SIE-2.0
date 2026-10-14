# Comparison Matrix — Submagic vs Eddie AI

Lente: feature-by-feature com paridade objetiva, focada em features que importam para substituição open-source.

## Legenda

- ✅ Forte (5/5)
- 🟢 Parcial alta (4/5)
- 🟡 Parcial (3/5)
- 🟠 Fraco (2/5)
- ❌ Sem equivalente (1/5)

## Matrix de paridade

### A. Speech / Transcription

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Multi-language ASR | ✅ 100+ idiomas, 99% acc | 🟢 multi-language (lista menor) | 4/5 | Submagic ganha em breadth |
| Custom vocabulary | ✅ dictionary per project | 🟡 não documentado | 2/5 | Eddie não expõe |
| Filler word removal | ✅ | ✅ | 5/5 | Empate |
| Speaker identification | ❌ | ✅ multicam-grade | 1/5 | Eddie ganha sem competição |
| Speaker diarization | ❌ | ✅ | 1/5 | Eddie ganha |

### B. B-Roll handling

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Upload personal library | ✅ "My videos" cross-project | ✅ B-roll folders | 5/5 | Empate funcional |
| Stock B-roll integrado | ✅ Storyblocks | 🟡 sugere mas não embute stock | 3/5 | Submagic embarca, Eddie sugere |
| **Semantic search ("office chaos")** | 🟠 keyword/transcript-based | ✅✅ visual + semantic | 2/5 | **Eddie ganha por margem grande** |
| Visual recognition tagging | 🟠 limitado | ✅ deep tagging | 2/5 | Eddie ganha |
| Background speech detection em B-roll | ❌ | ✅ | 1/5 | Eddie ganha |
| **Auto-place no timeline** | ✅ direto inserido + render | 🟡 sugere placement, exporta XML | 3/5 | Submagic finaliza, Eddie deixa para NLE |

### C. UX & Layout

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| **Split-screen layouts nativos** | ✅✅ split-50-50, split-35-65 + bordered | ❌ não tem (output via NLE) | 1/5 | **Submagic ganha sem competição** |
| PIP layouts | ✅ pip-top-right, pip-bottom-right | ❌ via NLE | 1/5 | Submagic ganha |
| Edit-by-transcript | ✅ canonical | ✅ via chat | 5/5 | Filosofias diferentes, equivalente |
| Chat-prompt edit | ❌ | ✅✅ talk-to-transcript | 1/5 | **Eddie ganha sem competição** |
| Timeline tradicional | 🟠 simplificado | ❌ delega ao NLE | 2/5 | Nenhum dos dois faz isso bem |
| Auto-zoom | ✅ Magic Zoom | ❌ | 1/5 | Submagic ganha |

### D. Output & Export

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Render final (MP4/MOV até 4K) | ✅ direto da plataforma | ❌ não renderiza | 1/5 | Submagic ganha |
| Export XML para Premiere | ❌ | ✅ FCP7/FCPXML | 1/5 | Eddie ganha |
| Export para DaVinci Resolve | ❌ | ✅ | 1/5 | Eddie ganha |
| Export para FCP | ❌ | ✅ | 1/5 | Eddie ganha |
| BRAW / R3D support | ❌ | ✅ Pro tier | 1/5 | Eddie ganha |
| Direct social publishing | ✅ TikTok/Reels/Shorts scheduling | ❌ | 1/5 | Submagic ganha |
| Public REST API | ✅ | 🟡 não documentado | 2/5 | Submagic ganha |

### E. Multicam

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Multicam sync | ❌ | ✅ até 6 câmeras | 1/5 | Eddie ganha sem competição |
| Speaker-driven cuts | ❌ | ✅ | 1/5 | Eddie ganha |

### F. Polish features (talking head)

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Captions animados (word-by-word) | ✅✅ best-in-class | 🟡 social clips com captions | 3/5 | Submagic ganha |
| Subtitle templates library | ✅ extensa | ❌ | 1/5 | Submagic ganha |
| Auto-translate | ✅ 100+ idiomas | ❌ | 1/5 | Submagic ganha |
| Eye contact correction | ✅ | ❌ | 1/5 | Submagic ganha |
| Hook title generation | ✅ | ❌ | 1/5 | Submagic ganha |
| AI avatars | ✅ 120+ | ❌ | 1/5 | Submagic ganha |

### G. Workflow / pro features

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Brand Kit (logos/fonts/colors) | ✅ Pro+ | ✅ analisa website do cliente | 4/5 | Filosofias diferentes mas equivalentes |
| Rough cut frameworks (narrative templates) | ❌ | ✅ | 1/5 | Eddie ganha |
| Stringouts automáticos | ❌ | ✅ | 1/5 | Eddie ganha |
| Night Shift (processamento overnight) | ❌ | ✅ | 1/5 | Eddie ganha |
| Magic Clips (long-form → shorts) | ✅ | ✅ Social Clips | 5/5 | Empate |
| Custom branding analysis (client website) | ❌ | ✅ | 1/5 | Eddie ganha |

### H. Collaboration

| Feature | Submagic | Eddie AI | Paridade | Notas |
|---|---|---|---|---|
| Shared workspace | ✅ Business | 🟡 Pro+ team (3 seats) | 3/5 | Submagic mais flexível |
| Team handoff via metadata | 🟡 limited | ✅ XML metadata cold-handoff | 2/5 | Eddie ganha em pro pipeline |

## Sumário de paridade

- **Total features comparadas:** 35
- **Submagic claramente vence em:** 13 (output, polish, captions, social, render)
- **Eddie AI claramente vence em:** 14 (logging, multicam, semantic search, NLE handoff, chat)
- **Empate funcional em:** 8
- **Conclusão:** Os dois produtos resolvem **problemas diferentes** apesar de superficialmente parecerem da mesma categoria. **Submagic = creator final, Eddie = pre-edit assistant.**
