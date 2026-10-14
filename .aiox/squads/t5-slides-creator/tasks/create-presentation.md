# Create Presentation

## SINKRA Task Anatomy (8 sections — migrated 2026-04-20 Wave 2)

```yaml
task: createPresentation
atomic_layer: Organism  # meta-orchestrator spanning P00-P06
responsavel_type: Human  # operator-driven entry point
session: null  # spans all sessions
Inputs:
  - { name: briefing, type: text|JSON, source: user }
  - { name: source_materials, type: array, source: user }
  - { name: brand_context, source: "workspace/businesses/{slug}/L2-tactical/brand/" }
  - { name: output_target, type: enum, values: [handoff_only, {consumer_app}] }
Outputs:
  - { name: briefing.normalized.json, template: templates/briefing.normalized.json }
  - { name: deck-manifest.json, template: templates/deck-manifest.json }
  - { name: deck-spec.yaml, template: templates/deck-spec.yaml, lifecycle: [draft, validated, approved] }
  - { name: qa-report.json, template: templates/qa-report.json }
  - { name: render-request.yaml, template: templates/render-request.yaml }
  - { name: release-summary.md, type: markdown }
Pre_conditions:
  - briefing_provided OR reference_assets_provided
  - brand_context_resolvable_or_explicit_override
Post_conditions:
  - deck_manifest.status == validated
  - qa_verdict == PASS
  - release_summary.generated == true
Acceptance_criteria:
  - All 7 invariants (P1-P7) enforced at their declared enforcement_level
  - All 4 gates (D01/D02/D03 + qa_verdict) have verdicts recorded
  - render-request.yaml emitted (regardless of {consumer_app} runtime availability)
  - Max 2 refinement loops via dimension_router
Performance_and_Error_handling:
  duration_target: "< 60 min per deck"
  error_strategy: retry with dimension_router fan-out
  escalation: "Human after 2 failed refinement loops"
```

## Legacy Task Anatomy (pre-migration, retained for reference)

```yaml
task_name: "Create Presentation"
status: active
responsible_executor: "slide-chief -> content-architect -> downstream specialists"
execution_type: Agent
input:
  - briefing: "Problem, objective, audience, constraints"
  - source_materials: "Docs, notes, URLs, screenshots, assets"
  - brand_context: "Workspace brand and company references"
  - output_target: "ds presenter parity"
output:
  - briefing_contract: "briefing.normalized.json"
  - reference_induction_notes: "reference-induction-notes.md"
  - source_bundle: "source-bundle.json"
  - deck_outline: "deck-outline.md"
  - deck_manifest: "deck-manifest.json"
  - template_selection_summary: "template-selection-summary.md"
  - asset_resolution: "asset-resolution.json"
  - render_plan: "TSX + ds presenter handoff + thumbnail coverage"
  - qa_contract: "qa/report.json"
  - release_summary: "release-summary.md"
action_items:
  - "Phase 1: Normalize briefing"
  - "Phase 2: Ground source materials into source-bundle.json and deck-manifest.json"
  - "Phase 3: Bind templates and registry provenance"
  - "Phase 4: Resolve assets and fallback status"
  - "Phase 5: Prepare ds presenter delivery"
  - "Phase 6: Run QA"
  - "Phase 7: Consolidate release gate"
acceptance_criteria:
  - "Briefing normalized into an explicit contract"
  - "Reference-first intake emits guidance without bypassing manifest SSOT"
  - "Grounded content starts from source-bundle.json, not improvisation"
  - "Outline and per-slide payloads respect mode constraints"
  - "Deck manifest planned without renderer drift"
  - "Render phase stays brand-agnostic through CSS variables and shared primitives"
  - "Delivery target is {consumer_app}, not TSX-only output"
  - "QA gate references thumbnails and presenter parity"
  - "Render never starts with a final asset outcome in blocked state"
  - "Workflow supports briefing-only intake and intake with reference_assets"
  - "Workflow re-entry after QA failure is explicit and bounded to 2 iterations"
  - "Release gate emits `release-summary.md` only after QA pass or explicit human checkpoint"
```

## Delivery State

Phases 1-7 are operational after Epics 2-8:

- `slide-chief` normalizes briefing and resolves planning constraints.
- `template-curator` can emit `reference-induction-notes.md` before content
  expansion when `reference_assets` force `reference_first`.
- `content-architect` emits `source-bundle.json`, `deck-outline.md`, and
  `deck-manifest.json` (partial).
- `template-curator` emits `template-selection-summary.md` and binds
  `template_ref` with registry-backed provenance plus canonical alias
  normalization for content-contract slide types.
- `visual-scout` emits `asset-resolution.json` and keeps degraded fallback
  status explicit while restricting final asset outcomes to `resolved` or
  `degraded`.
- `design-renderer` defines the manifest -> TSX -> ds -> thumbnails
  contract without taking ownership away from the manifest.
- `qa-inspector` defines PPTEval + GAD + killer items + refinement routing
  without taking ownership away from content or render specialists.
- `slide-chief` closes the release gate only when QA returns a pass verdict or
  an explicit human approval path.
- `generate-presentation` now materializes the re-entry contract: content
  failures replay template/assets/render, render failures replay QA, and loop
  exhaustion escalates to human review.

## Phase 1 Contract

When this task is loaded for `slide-chief`, execute the intake slice in this
order:

1. Normalize the briefing into `briefing.normalized.json`.
2. Resolve `mode`, `aspect_ratio`, output target, and blockers.
3. Record whether the request is briefing-only or includes
   `source_materials/reference_assets`.
4. Block the workflow early when objective, audience, or delivery surface stay
   ambiguous.
5. Pass a stable intake contract downstream to `content-architect`.

## Phase 2 Contract

When this task is loaded for `content-architect`, execute the grounded-content
slice in this order:

1. Validate `briefing.normalized.json`, consume `reference-induction-notes.md`
   when present, and confirm `blockers=[]`.
2. Build `source-bundle.json` with evidence refs, assumptions, and warnings.
3. Sequence `deck-outline.md` using the 11 canonical slide types.
4. Generate per-slide payloads inside mode limits (`palco`, `live`, `async`).
5. Emit `deck-manifest.json` with `content_status=partial`.
6. Leave template provenance, asset resolution, and TSX fields unresolved.

## Phase 3 Contract

When this task is loaded for `template-curator`, execute the template-binding
slice in this order:

1. Validate `deck-manifest.json`, slide types, `induction_mode`, and any
   `reference-induction-notes.md` passed by the workflow.
2. Load `data/template-registry.yaml` and treat its runtime source as the
   inventory SSOT.
3. Normalize content-contract aliases (`SECTION-BREAK`, `DATA-VIZ`) to the
   registry canonical keys before category lookup.
4. Apply `reference_first` when screenshots or PPTX references exist; otherwise
   stay `registry_first`.
5. Bind `template_ref` for every slide or emit an explicit closest-match note.
6. Preserve both `slide_type` and `canonical_slide_type` in decision records.
7. Emit `template-selection-summary.md` with provenance, adaptation notes, and
   unresolved gaps.
8. Never invent a blank-slate template family or silently overwrite registry
   provenance.

## Phase 4 Contract

When this task is loaded for `visual-scout`, execute the asset-resolution slice
in this order:

1. Validate slide-level image requests, narrative purpose, and brand context.
2. Follow `data/asset-resolution.yaml` in strict order: briefing assets ->
   reference extraction -> contextual search -> AI generation ->
   degraded placeholder.
3. Record provenance and a final `fallback_status` of `resolved` or `degraded`
   for every requested asset.
4. Reject generic stock, watermarks, pixelation, or narrative mismatch.
5. Keep blocked decisions inside `rejected_candidates`; never pass a final
   `asset_ref` downstream with `fallback_status=blocked`.
6. Emit `asset-resolution.json` with rejected candidates and any required human
   checkpoints.
7. Keep degraded output explicit so render and QA cannot hide the gap.

## Phase 5 Contract

When this task is loaded for `design-renderer`, execute the render slice in
this order:

1. Validate `deck-manifest.json` plus template and asset inputs.
2. Map each slide to a shared primitive or bound template family.
3. Render TSX on the canonical 1920x1080 surface used by `ds`.
4. Keep style decisions inside CSS variables or shared slide primitives.
5. Record ratio adaptation notes for `16:9`, `9:16`, and `1:1`.
6. Emit `render-summary.md`, `ds-integration-plan.md`, and
   `thumbnails/*.png`.
7. Leave briefing, evidence, and QA verdict ownership outside the renderer.

## Phase 6 Contract

When this task is loaded for `qa-inspector`, execute the QA slice in this
order:

1. Validate `slides/*.tsx`, `thumbnails/*.png`, `deck-manifest.json`, and the readiness checklist.
2. Score Content, Design, Coherence, and GAD against the rendered deck.
3. Apply killer items and WCAG/SOP checks before considering a pass verdict.
4. Verify presenter parity, thumbnail coverage, and sequence integrity.
5. Emit `qa/report.json` with scores, blockers, `next_target`, and
   `refinement.iteration_count`.
6. Route Design/GAD/parity failures to `design-renderer` and Content/Coherence failures to `content-architect`.
7. Escalate to human review when refinement exceeds two iterations or mixed-owner failures remain unresolved.

## Workflow Integration Notes

1. If `reference_assets` are present, the workflow calls `template-curator`
   before content expansion to emit `reference-induction-notes.md`.
2. `content-architect` consumes those induction notes but keeps ownership of
   `deck-manifest.json`.
3. If QA routes to `content-architect`, the workflow re-enters at
   `template_binding` so content changes can replay template, asset, render,
   and QA effects in order.
4. If QA routes to `design-renderer`, the workflow re-enters at render and then
   returns immediately to QA.
5. After two failed refinement loops, `slide-chief` escalates to a human gate
   instead of hiding the deadlock.

## Phase 7 Contract

When this task is loaded for `slide-chief` after QA, execute the release slice
in this order:

1. Validate `qa/report.json` and confirm the active `next_target`.
2. Refuse release when QA still targets `content-architect`,
   `design-renderer`, or human escalation.
3. Consolidate the `ds` handoff, release rationale, and remaining
   operator notes into `release-summary.md`.
4. Record explicit human approval when a degraded but accepted outcome needs it.
5. Close the workflow only after the deck is approved for presentation.

## Output Promise

The completed squad must eventually produce a deck that can be previewed,
filtered, and presented fullscreen inside `ds`.
