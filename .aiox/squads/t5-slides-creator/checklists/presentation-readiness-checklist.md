# Presentation Readiness Checklist

## Contract

- [ ] `briefing.normalized.json` exists
- [ ] `reference-induction-notes.md` exists when `reference_assets` trigger `reference_first`
- [ ] `source-bundle.json` exists
- [ ] `deck-manifest.json` exists
- [ ] `template-selection-summary.md` exists once template binding runs
- [ ] `asset-resolution.json` exists when slides request visuals
- [ ] manifest remains the source of truth after template, asset, and render decisions
- [ ] `qa/report.json` exists once QA runs
- [ ] `release-summary.md` exists once the release gate runs
- [ ] non-trivial claims in the manifest point to source-bundle evidence or explicit assumptions
- [ ] template provenance is explicit
- [ ] degraded asset decisions are explicit
- [ ] workflow input path works with and without `reference_assets`
- [ ] selected mode is explicit and respected end-to-end (`palco`, `live`, or `async`)

## ds Parity

- [ ] deck can be mounted in the `ds` slide surface
- [ ] preview cards are available for all slides
- [ ] render output uses the canonical 1920x1080 surface scaled by preview/fullscreen runtime
- [ ] shared slide primitives or CSS variables drive brand styling
- [ ] fullscreen presenter opens from a slide preview
- [ ] keyboard controls work: `Escape`, `ArrowLeft`, `ArrowRight`, `Space`
- [ ] slide counter is visible
- [ ] progress bar is visible
- [ ] body scroll locks during presenter mode

## Visual QA

- [ ] multi-ratio adaptation notes exist for `16:9`, `9:16`, and `1:1` when layouts are risky
- [ ] every slide has a thumbnail
- [ ] every slide has a unique accessible title
- [ ] every image has alt text
- [ ] reduced-motion handling exists when animation is present
- [ ] no killer items remain (K1-K7 + K8 when education_mode + K9 always-on)
- [ ] K8: no jargon without pre-training in education_mode decks
- [ ] K9: no slide exceeds 60 words (exceptions: data_table 80, comparison_matrix 60, quote 60)
- [ ] no hardcoded `px` values remain in slide output
- [ ] no hardcoded brand hex values remain in slide output
- [ ] consumer dim-text token (`var(--{prefix}-dim)`) stays at or above `#777777` contrast minimum
- [ ] Palco/Live slides stay at or below 15 words
- [ ] Palco/Live slides contain zero paragraphs
- [ ] code appears as rendered text, not screenshots
- [ ] degraded assets are explicit
- [ ] degraded hero/opening/closing visuals set `human_checkpoint_required=true`
- [ ] degraded hero/opening/closing visuals set `human_checkpoint_recorded=true`
- [ ] degraded hero/opening/closing visuals have a human checkpoint note
- [ ] no blocked visual anti-pattern is approved for render
- [ ] composite score is at least `7.5`
- [ ] design/content/coherence/GAD score meets threshold
- [ ] andragogy score meets threshold when education_mode=true (weight 0.15)

## Release

- [ ] final surface target conforms to a render_target declared in `config.yaml#render_targets`
- [ ] refinement target is explicit when QA fails
- [ ] workflow re-entry point is explicit when QA fails
- [ ] refinement loop stops after two iterations and escalates instead of cycling indefinitely
- [ ] human approval recorded when required
