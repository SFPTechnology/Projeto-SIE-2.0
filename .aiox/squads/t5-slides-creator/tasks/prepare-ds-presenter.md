# Prepare ds Presenter

## SINKRA Task Anatomy (8 sections — migrated 2026-04-20 Wave 2)

```yaml
task: prepareDsPresenter
atomic_layer: Atom
responsavel_type: Worker
session: null
phase: P06
Inputs:
  - { name: deck_spec, type: YAML, source: deck-spec.yaml }
  - { name: render_request, type: YAML, source: render-request.yaml }
Outputs:
  - { name: ds-presenter-package, type: directory, status: handoff_only }
Pre_conditions:
  - deck-spec.yaml status == approved
  - render-request.yaml emitted
Post_conditions:
  - package_prepared OR status == blocked_runtime_missing
Acceptance_criteria:
  - Package structure matches {consumer_app} expected schema when runtime reconnects
  - Blocked runtime status explicitly recorded in pipeline-execution-log
Performance_and_Error_handling:
  duration_target: "< 30 sec"
  error_strategy: record blocked status; do not fail pipeline
  blocker: "{consumer_app} absent — handoff_only mode per config.yaml#workspace_integration"
```

## Legacy Task Anatomy

```yaml
task_name: "Prepare ds Presenter"
status: active
responsible_executor: "visual-scout -> design-renderer"
execution_type: Hybrid
input:
  - deck_manifest: "deck-manifest.json"
  - template_refs: "template-selection-summary.md or equivalent registry bindings"
  - asset_refs: "asset-resolution.json with resolved or degraded visual assets"
  - brand_context: "workspace tokens or deck-level CSS variable map"
  - presenter_reference: "ds slides route + preview/fullscreen runtime"
output:
  - asset_resolution: "asset-resolution.json"
  - render_output: "slides/*.tsx"
  - render_summary: "render-summary.md"
  - app_surface_plan: "ds presenter integration notes"
  - thumbnails: "thumbnails/*.png"
action_items:
  - "Resolve or degrade asset refs before render"
  - "Render manifest-backed deck TSX on the canonical 1920x1080 surface"
  - "Use CSS variables and shared slide primitives instead of hardcoded brand tokens"
  - "Record multi-ratio adaptation notes for 16:9, 9:16, and 1:1"
  - "Map output to the ds slide surface"
  - "Verify presenter parity requirements against preview and fullscreen behaviors"
  - "Generate thumbnails for QA"
acceptance_criteria:
  - "Fallback status is recorded for every requested asset"
  - "Final asset refs arrive at render only as resolved or degraded"
  - "Degraded hero/opening/closing visuals include explicit human checkpoint metadata"
  - "Deck render output stays manifest-backed and brand-agnostic"
  - "Deck can be mounted in ds presenter surface"
  - "Fullscreen controls are part of the release contract"
  - "Counter, progress bar, and body scroll lock remain part of the presenter contract"
  - "Multi-ratio adaptation notes exist for risky layouts"
  - "Every slide has thumbnail coverage"
  - "Manifest remains the source of truth after render decisions"
```

## Phase 4 Contract

When this task is loaded for `visual-scout`, execute the asset-resolution slice
in this order:

1. Validate `deck-manifest.json`, image keywords, and requested visual roles.
2. Resolve candidates via `data/asset-resolution.yaml`.
3. Record `selected_source`, provenance, final `fallback_status`, and human
   checkpoint metadata for each slide.
4. Reject blocked patterns before passing any asset downstream.
5. Emit `asset-resolution.json` with final outcomes limited to `resolved` or
   `degraded`; keep blocked candidates under `rejected_candidates`.
6. Require `human_checkpoint_required=true`, `human_checkpoint_recorded=true`,
   and a note for degraded hero/opening/closing visuals.

## Phase 5 Contract

When this task is loaded for `design-renderer`, execute the render slice in
this order:

1. Validate `deck-manifest.json`, `template-selection-summary.md`, and `asset-resolution.json`.
2. Refuse render handoff if any final `asset_ref` still carries blocked state.
3. Preserve degraded notes instead of silently substituting prettier assets.
4. Map each slide to a shared primitive or bound template family.
5. Render TSX on the canonical 1920x1080 `ds` surface.
6. Emit `render-summary.md`, `ds-integration-plan.md`, and thumbnails.
7. Keep the manifest and provenance artifacts as SSOT after render decisions.
