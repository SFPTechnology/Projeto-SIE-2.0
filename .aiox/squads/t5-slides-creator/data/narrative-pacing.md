# Narrative Pacing — Slow-Fast-Boom-Stop Structure

> **Purpose:** estrutura de 5 stages para animated slides, motion graphics, launch videos. Derivada de análise das animações oficiais Anthropic (Claude Design / Claude Code Desktop / Claude for Word).
> **Use as:** reference quando delivery_format inclui D (MP4/GIF) ou quando slide tem motion-heavy transitions

---

## Thesis

Animações geradas por AI têm "cheap feel" porque movimento é uniforme. Animações "Anthropic-grade" têm **estrutura narrativa** — tempo alocado de forma não-uniforme, com peak de intensidade em S4 e **abrupt stop** em S5 (não fade-out).

Essa estrutura é consistente em 3 animações Anthropic analisadas (Claude Design, Claude Code Desktop, Claude for Word) e diverge diametralmente do default AI (uniform pacing, fade ending).

---

## The 5 Stages

| Stage | % of total | Pace | Function | Forbidden |
|---|---|---|---|---|
| **S1 — Trigger** | ~15% | Slow | Human reaction time; estabelecer contexto; "aterrissagem" | Jump-cut direto ao conteúdo |
| **S2 — Generate** | ~15% | Medium | Visual wow moment; revelação inicial | Nenhum "wow" (animação fica flat) |
| **S3 — Process** | ~40% | Fast | Show control, density, feature detail; rapid sequence | Uniform pace (audience fatigue) |
| **S4 — Explosion** | ~20% | Boom | Camera pull-out / 3D pop / multi-panel swarm / peak moment | Sustain current pace (no peak = no memory) |
| **S5 — Closing** | ~10% | Still | Brand logo + **abrupt stop** | Fade-to-transparent ending |

### Time mapping (exemplos)

**15s animation:**
- S1: 2.25s (sometimes 2s)
- S2: 2.25s
- S3: 6s
- S4: 3s
- S5: 1.5s

**30s animation:**
- S1: 4.5s
- S2: 4.5s
- S3: 12s
- S4: 6s
- S5: 3s

**60s launch video:**
- S1: 9s (full context-setting, often with voiceover intro)
- S2: 9s
- S3: 24s (feature showcase density)
- S4: 12s
- S5: 6s

---

## Why it works

**Signal theory:** brain registra mudança de densidade de informação. Uniform density → nenhuma mudança → nenhum peak memorizado.

- S1 slow = brain "arms itself" to pay attention
- S2-S3 crescendo = density ramp builds anticipation
- S4 boom = peak creates memory anchor (audience will remember THIS moment)
- S5 abrupt stop = brain completes the narrative loop (fade-out = ambiguity = weak closure)

**Audience retention research** (documented na indústria de cinema/advertising): peaks + abrupt endings retain 3-4x better than gradual fadeouts.

---

## The audience reaction ladder (self-check)

Depois de render, antes de ship, avaliar reação subjetiva:

| Reação | Grade | Diagnosis |
|---|---|---|
| "Looks smooth" | good (PowerPoint level) | Tecnicamente correto, sem impact |
| "Really fluid" | good+ | Tech certo, mas no wow |
| "Like something floating off the desk" | **great** | Physical weight triggered — S4 landed |
| "Doesn't look AI-made" | **great+** | Anthropic threshold reached |
| "Want to screenshot + share" | **great++** | Viral trigger — S4 + S5 + craft all worked |

**Target:** "great" mínimo. Se audience reação é "good+", falta peak em S4 ou stop em S5 está em fade.

---

## Forbidden patterns

### Uniform pacing

❌ Todo segment tem mesma densidade de informação
→ Audience fatigue, no memorable moment

### Sustained peak

❌ Animation inteira no pace de S4 (all "explosion")
→ Peak becomes baseline → no peak at all

### Fade-to-transparent ending

❌ `opacity: 1 → 0` no final
→ Ambiguous closure, brain doesn't "commit" to what happened
✅ Abrupt cut OR hold last frame for 300-500ms then cut

### Skipping S1

❌ Animation starts immediately with content (no slow lead-in)
→ No reaction time, audience misses first 1-2 seconds
→ If animation is for social feed, this costs you the hook

---

## Integration points

### Feature flag

Adicionar em `config.yaml`:
```yaml
feature_flags:
  ENABLE_MOTION_NARRATIVE:
    default: false
    description: "Apply Slow-Fast-Boom-Stop pacing to animated slides"
```

### Workflow integration

Quando `delivery_format.primary == "D"` (MP4/GIF):
1. `design-renderer` consulta este file
2. Estrutura timeline de render em 5 stages (S1-S5 proportions)
3. Enforce S5 como abrupt stop (no fade-out keyframe)

### qa-inspector check

Adicionar signal:
```yaml
qa_signals_motion:
  - id: "MOTION-PACING-001"
    description: "Timeline has 5 distinct density stages (not uniform)"
    severity: "warning"  # aspirational
    
  - id: "MOTION-PACING-002"
    description: "Ending is abrupt cut or hold, not fade-to-transparent"
    severity: "warning"
```

---

## Related

- `data/motion-export-discipline.md` (when created) — recording sync pattern
- `data/editable-vs-image-pptx-decision.md` — motion incompatible with editable PPTX export
