# Review Presentation

## SINKRA Task Anatomy (8 sections — migrated 2026-04-20 Wave 2)

```yaml
task: reviewPresentation
atomic_layer: Atom
responsavel_type: Human
session: null
phase: null
Inputs:
  - { name: deck_manifest, type: JSON, source: deck-manifest.json }
  - { name: qa_report, type: JSON, source: qa-report.json }
  - { name: rendered_artifacts, type: array }
Outputs:
  - { name: review-notes.md, type: markdown }
  - { name: verdict, type: enum, values: [APPROVED, CHANGES_REQUESTED, REJECTED] }
Pre_conditions:
  - qa_report.qa_verdict != FAIL
Post_conditions:
  - verdict recorded
  - if CHANGES_REQUESTED, dimension_router invoked
Acceptance_criteria:
  - Human reviewer inspected all P1-P7 enforcement results
  - Brand compliance verified (or STK-10 co-sign on override)
Performance_and_Error_handling:
  duration_target: "< 15 min"
  error_strategy: CHANGES_REQUESTED returns to P01/P03 via dimension_router
```

## Legacy Task Anatomy

```yaml
task_name: "Review Presentation"
status: active
responsible_executor: "qa-inspector"
execution_type: Hybrid
input:
  - content_contract: "source-bundle.json + deck-manifest.json"
  - workflow_context: "briefing.normalized.json + reference-induction-notes.md when present"
  - rendered_deck: "TSX output + render-summary.md + ds presenter behavior"
  - thumbnails: "preview coverage for every slide"
  - checklist: "presentation-readiness-checklist.md"
  - quality_sources: "SOP-SLIDES-001.md + SOP-SLIDES-003.md"
output:
  - qa_report: "qa/report.json"
  - release_verdict: "pass | revise | fail"
  - refinement_target: "slide-chief | content-architect | design-renderer | human_escalation"
  - workflow_reentry: "template_binding | qa_gate | release_gate | human_escalation"
action_items:
  - "Score content, design, coherence, GAD, and andragogy (when education_mode=true)"
  - "Verify ds presenter parity and thumbnail coverage"
  - "Apply killer items (K1-K7 always + K8 education_mode + K9 always-on), WCAG/SOP checks, and release decision"
  - "Route findings to content-architect, design-renderer, or slide-chief"
  - "Emit iteration_count and workflow re-entry target for the next pass"
  - "Route andragogic violations: sequence issues to content-architect, layout issues to design-renderer"
acceptance_criteria:
  - "Content contract exists before release"
  - "Every QA pass emits qa/report.json with dimension scores and next_target"
  - "Composite score reaches the release threshold only when every dimension clears its minimum"
  - "No killer items remain for pass verdicts"
  - "Presenter parity passes the checklist"
  - "Deck is blocked if fullscreen, keyboard controls, thumbnails, or accessibility blockers fail"
  - "Design/GAD failures route to design-renderer; Content/Coherence failures route to content-architect"
  - "Workflow re-entry target is explicit enough to resume at template replay, QA replay, release, or human escalation"
  - "Refinement loop escalates after 2 iterations instead of cycling silently"
  - "When education_mode=true AND ENABLE_ANDRAGOGIC_VALIDATION=true: andragogy dimension is scored with weight 0.15"
  - "Andragogy scoring includes: Mayer compliance (>= 8/12), Kolb completeness, DPC ordering, Dreyfus calibration"
  - "Killer item K8 (jargon without pre-training) blocks pass verdict when education_mode=true"
  - "Killer item K9 (> 60 words per slide) blocks pass verdict always (always-on)"
```

## Workflow Re-entry Contract

- When `next_target = content-architect`, the workflow resumes at
  `template_binding` after content revision so downstream template/asset/render
  artifacts can be replayed safely.
- When `next_target = design-renderer`, the workflow resumes at `qa_gate` after
  render revision because the visual/parity owner already regenerated the app
  surface evidence.
- When `next_target = slide-chief`, the workflow resumes at `release_gate`.
- When `next_target = human_escalation` or `iteration_count >= 2`, the workflow
  stops and waits for a human decision.

## Andragogy Dimension (v2)

When `education_mode=true` AND `ENABLE_ANDRAGOGIC_VALIDATION=true`, the QA scoring
adds a fifth dimension: **Andragogy**.

### Scoring Weights

| Dimension | education_mode=false | education_mode=true |
|-----------|---------------------|---------------------|
| Content | 0.30 | 0.25 |
| Design | 0.30 | 0.25 |
| Coherence | 0.20 | 0.20 |
| GAD | 0.20 | 0.15 |
| Andragogy | -- | 0.15 |

### Andragogy Sub-scores

| Rule | Check | Type |
|------|-------|------|
| MAYER compliance | >= 8/12 principles satisfied | always-on subset (3 rules) + education_mode (full 12) |
| Kolb completeness | All 4 stages present in education deck | education_mode only |
| DPC ordering | Concrete -> Representational -> Abstract sequence | education_mode only |
| Dreyfus calibration | Audience level matches content complexity | education_mode only |
| Scaffolding fade | Support decreases across slide progression | education_mode only |

### Killer Items (v2)

| ID | Rule | Scope | Consequence |
|----|------|-------|-------------|
| K8 | Jargon without pre-training: technical term used before being defined/explained | education_mode only | Blocks pass verdict |
| K9 | > 60 words per slide (exceptions: data_table=80, comparison_matrix=60, quote=60) | always-on | Blocks pass verdict |

### Routing

- Andragogic sequence violations (Kolb, DPC, scaffolding) route to `content-architect`
- Andragogic layout violations (cognitive load, contiguity, multimedia) route to `design-renderer`
