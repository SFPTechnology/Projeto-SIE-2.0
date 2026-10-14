# Slides Creator Squad - Architecture

## Tier System

```text
                    +------------------------+
                    |      slide-chief       |
                    | orchestrator / gate    |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |   content-architect    |
                    | grounding + outline    |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |   template-curator     |
                    | registry + induction   |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |     visual-scout       |
                    | assets + provenance    |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |    design-renderer     |
                    | TSX + ds app    |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |     qa-inspector       |
                    | PPTEval + GAD + veto   |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |      slide-chief       |
                    |      release gate      |
                    +-----------+------------+
                                |
                                v
                    +------------------------+
                    |  runtime externo |
                    | apps/ds (ausente) |
                    +------------------------+
```

## Delivery Contract

Epic 1 fixes the functional target:

1. `briefing.normalized.json`
2. `deck-manifest.json`
3. TSX slide output
4. `ds` presenter parity
5. `thumbnails/*.png`
6. `qa/report.json`

The MVP is only valid when the deck can be previewed and presented with parity
to the historical `ds` runtime. Until that runtime is reconnected, this squad
must operate as a handoff-only producer.

## Historical Runtime Reference

- route: `apps/ds/src/app/(brandbook)/brandbook/showcase/slides/page.tsx`
- gallery page: `apps/ds/src/components/brandbook/pages/slides-page.tsx`
- fullscreen presenter: `apps/ds/src/components/brandbook/slides/slide-fullscreen.tsx`

## Epic Progress

| Epic | Status | What was delivered |
|------|--------|--------------------|
| 1 | DONE | Squad shell, contracts, workflow shell, runtime handoff |
| 2 | DONE | slide-chief operational orchestrator (briefing normalization, planning rules, routing coverage) |
| 3 | DONE | content-architect operational contract (source bundle, outline, payloads, manifest partial) |
| 4 | DONE | design-renderer operational contract (manifest -> TSX, CSS vars/shared module, presenter parity, thumbnails) |
| 5 | DONE | qa-inspector operational contract (PPTEval, GAD, killer items, accessibility, refinement routing) |
| 6 | DONE | template-curator + visual-scout operational contracts (registry mirror, reference induction, asset resolution, degraded transparency) |
| 7 | DONE | workflow integration with artifact chain, handoff prompts, fail-fast checkpoints, and release gating |
| 8 | DONE | execution handoff pack, runtime completion, validation cadence, and deferred-scope isolation |

## Routing Coverage (Epic 2)

slide-chief orchestrates the full pipeline with 13 handoffs across 6 agents:

```text
user → slide-chief (normalize briefing)
         ├─→ content-architect (outline + manifest)
         │     └─→ visual-scout (assets)
         ├─→ template-curator (template binding)
         ├─→ design-renderer (TSX + ds + thumbnails)
         └─→ qa-inspector (PPTEval + GAD + killer items)
               ├─→ content-architect (Content/Coherence failure)
               ├─→ design-renderer (Design/GAD failure)
               └─→ slide-chief (release gate)
```

**Coverage:** 100% — every agent has at least one incoming and one outgoing handoff.
**Refinement loop:** max 2 iterations before human escalation.

## Grounded Content Contract (Epic 3)

Epic 3 fixes the content handoff before rendering:

1. `source-bundle.json` exists before any slide payload is expanded
2. `deck-outline.md` uses the 11 canonical slide types from `SOP-SLIDES-001`
3. Incoming `QUOTE` requests are normalized to a canonical type plus `content_variant=quote`
4. Mode constraints (`palco`, `live`, `async`) are applied before manifest emission
5. `deck-manifest.json` remains `content_status=partial` until template, asset, render, and QA phases complete

## Render Delivery Contract (Epic 4)

Epic 4 fixes the render handoff after content planning:

1. `design-renderer` consumes `deck-manifest.json` without taking SSOT away from the manifest
2. Render output is expressed as TSX on the canonical 1920x1080 surface used by `ds`
3. Brand styling flows through CSS variables and shared slide primitives, not render-only hardcodes
4. Presenter parity is defined against `SlidesPage`, `SlidePreview`, and `SlideFullscreen`
5. Thumbnail coverage becomes a hard gate before QA scoring
6. `16:9`, `9:16`, and `1:1` adaptation are recorded as composition-safe variants, not rewritten content

## Quality Evaluation Contract (Epic 5)

Epic 5 fixes the release veto after rendering:

1. `qa-inspector` scores Content, Design, Coherence, and GAD before any release recommendation
2. `qa/report.json` becomes the canonical QA artifact with scores, blockers, and `next_target`
3. Killer items block release independently of the composite score
4. Presenter parity, thumbnails, WCAG checks, and sequence checks are consolidated into the QA verdict
5. Content/Coherence failures route back to `content-architect`
6. Design/GAD/accessibility/parity failures route back to `design-renderer`
7. Refinement stops after two loops and escalates instead of cycling indefinitely

## Template and Asset Intelligence Contract (Epic 6)

Epic 6 fixes the template and asset handoffs between planning and rendering:

1. `data/template-registry.yaml` mirrors the 56 implemented templates from the
   canonical `ds` runtime registry
2. `template-curator` binds `template_ref` for every slide and records
   provenance in `template-selection-summary.md`
3. `reference_first` mode remains registry-backed: screenshots/PPTX guide the
   match, but do not bypass provenance
4. `visual-scout` resolves `asset_refs` via an explicit fallback chain and
   emits `asset-resolution.json`
5. Degraded assets stay visible to render and QA instead of being silently
   swapped out
6. Generic stock, watermarks, and narrative mismatch are blocked before render

## Workflow Integration Contract (Epic 7)

Epic 7 closes the executable contract across all specialist agents:

1. `workflow.sequence[]` now exposes a full 7-phase artifact chain through
   `creates`/`requires`
2. `handoff_prompts` are explicit for every agent transition in the canonical
   path
3. `checkpoint.policy=always_active` and `fail_fast=true` remain active across
   the whole flow
4. `palco`, `live`, and `async` stay part of the intake and content checkpoints
5. The workflow supports briefing-only intake and intake with
   `reference_assets`
6. Refinement is capped at two loops before escalation
7. Release is blocked unless QA points back to `slide-chief`

## Execution Handoff Contract (Epic 8)

Epic 8 closes the squad as an operational MVP handoff:

1. Final create-squad runtime state is marked completed instead of pointing to
   another wave
2. `validate-squad` becomes the canonical integrity command after bootstrap
3. MVP scope is frozen around the `ds` surface and the seven-phase deck
   pipeline
4. Post-MVP follow-ups remain isolated from the operational backlog
5. COO readiness is still required before publishing decks into the canonical
   runtime surface

## Visual Engine Layer (v2 Upgrade)

The visual engine layer introduces a strategy pattern for rendering visual
assets. Instead of relying solely on external image search, the pipeline can
now generate diagrams, infographics, and illustrations programmatically.

**Contract:** `data/visual-engines.yaml` (SSOT)

**Interface:** `VisualEngine` with 4 methods:
- `render(spec)` -- generate visual from specification
- `supports(engine)` -- check engine capability match
- `estimateCost(spec)` -- budget estimation before generation
- `validateBrandCompliance(output, tokens)` -- post-generation brand check

**Engines (6):**

| Engine | Category | Cost | Output | Self-Hosted |
|--------|----------|------|--------|-------------|
| D2 | diagram | free | SVG | Kroki |
| Mermaid | diagram | free | SVG | Kroki |
| GPT Image | ai_image | $0.04 | PNG | no (OpenAI) |
| Recraft | ai_vector | $0.08 | SVG | no (Recraft) |
| Plotly | data_viz | free | SVG/PNG | local lib |
| Ideogram | ai_image | $0.04 | PNG | no (Ideogram) |

**Integration point:** visual-scout's fallback chain gains a new
`ai_generation` tier (order 4) that routes through the VisualEngine interface.

**Budget cap:** $2.00/deck enforced via `estimateCost()` before each render.

**Feature flag:** `ENABLE_VISUAL_GENERATION` gates the entire layer.

---

## Quality Gates

| Gate | What must be true |
|------|-------------------|
| Planning contract | briefing and objective are explicit |
| Template provenance | template choice is versioned |
| Asset resolution | every requested visual is resolved, degraded, or blocked explicitly |
| Render gate | render stays manifest-backed, uses shared module/CSS variables, and opens in `ds` |
| Presenter gate | fullscreen controls work with keyboard navigation |
| QA gate | every dimension >= 7, composite >= 7.5, thumbnails exist, checklist passes, and killer items are zero |
| Release gate | `release-summary.md` exists, `qa/report.json.next_target` is `slide-chief`, and human approvals are recorded when required |

## Workspace Governance

`slides-creator` operates as `controlled_runtime_consumer`:

- reads brand context from workspace
- does not mutate workspace directly during bootstrap
- requires COO/c-level readiness before app-surface publication

The app surface is outside `workspace/`, but the governance model still needs
the COO gate because the deck is published into a canonical product surface.
