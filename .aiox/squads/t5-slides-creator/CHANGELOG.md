# Changelog

## 2026-03-19 - v8.1.0 (Audit remediation: P0 + P1 + P2 gaps)

- [P0] Created runtime artifacts: `.aiox/squad-runtime/create-squad/slides-creator/workspace-integration-level.yaml` and `workspace-handoff.yaml`
- [P0] Documented ds submodule prerequisite in README.md and config.yaml (external repo, requires manual init)
- [P1] Added concrete template schemas: `templates/briefing.normalized.json`, `templates/deck-manifest.json`, `templates/qa-report.json`
- [P1] Resolved QUOTE incoherence: added governance note GOV-001 to template-registry.yaml marking quote template as deprecated for direct slide_type usage; updated slide-chief slide_type_mapping to normalize QUOTE to content_variant
- [P1] Fixed PRD path references in 5 agents and asset-resolution.yaml: `docs/projects/slides-creator/prd.md` corrected to `docs/projects/slides-creator-prd.md`
- [P1] Standardized tier format across all 6 agents to numeric (0, 1, 2, 3) matching config.yaml tier_system
- [P2] Eliminated metadata.version duplication in config.yaml; squad.version is the single source of truth

## 2026-03-16 - v8.0.0 (Wave 8: execution handoff + validation)

- Added final execution handoff documentation, runtime completion state, and refreshed operational next steps
- Updated stale create-squad runtime artifacts (`creation-report.yaml`, `workspace-handoff.yaml`, planning summary) to the completed squad state
- Marked the MVP scope boundary explicitly around the seven-phase `ds` pipeline and isolated deferred follow-ups from the operational backlog

## 2026-03-16 - v7.0.0 (Wave 7: workflow integration)

- Added an explicit `creates`/`requires` artifact chain across all seven phases of `generate-presentation`
- Added `handoff_prompts`, workflow-level fail-fast checkpoint policy, and refinement loop cap to the canonical workflow contract
- Hardened release gating so `release-summary.md` is emitted only after QA resolves back to `slide-chief`
- Expanded task and checklist contracts to cover mode coverage, reference-asset intake, and release blocking rules

## 2026-03-16 - v6.1.0 (Wave 6 audit remediation)

- Normalized `SECTION-BREAK` and `DATA-VIZ` aliases before template category lookup so Wave 3 content contracts bind safely into the Wave 6 registry map
- Restricted final `asset-resolution.json` outcomes to `resolved` or `degraded`, keeping blocked results only as rejected candidates
- Added explicit human checkpoint metadata for degraded `hero/opening/closing` visuals across agent, task, data, workflow, and checklist contracts
- Hardened render handoff so blocked final asset states fail before `design-renderer`

## 2026-03-16 - v6.0.0 (Epic 6: template-curator + visual-scout)

- Replaced `template-curator` shell with an operational specialist contract
- Replaced `visual-scout` shell with an operational specialist contract
- Added `data/template-registry.yaml` as the 56-template mirror of the canonical `ds` runtime registry
- Added `data/asset-resolution.yaml` with fallback chain, degraded policy, and blocked visual anti-patterns
- Expanded the phase-3 and phase-4 task/workflow/checklist contracts around provenance and degraded transparency
- Updated README, ARCHITECTURE, epic docs, and runtime state for Epic 6 completion

## 2026-03-16 - v5.0.0 (Epic 5: qa-inspector)

- Replaced `qa-inspector` shell with an operational specialist contract
- Added PPTEval-aligned scoring, GAD, killer items, accessibility vetoes, and refinement routing
- Added `qa/report.json` thresholds and routing rules to the phase-6 task/workflow/checklist contracts
- Updated README, ARCHITECTURE, epic docs, and runtime state for Epic 5 completion

## 2026-03-16 - v4.0.0 (Epic 4: design-renderer)

- Replaced `design-renderer` shell with an operational specialist contract
- Added manifest -> TSX render rules anchored to the `ds` runtime
- Codified CSS-variable/shared-module styling, multi-ratio adaptation, and presenter parity requirements
- Added render-summary and thumbnail coverage to the phase-5 task/workflow/checklist contracts
- Updated README, ARCHITECTURE, epic docs, and runtime state for Epic 4 completion

## 2026-03-16 - v3.0.0 (Epic 3: content-architect)

- Replaced `content-architect` shell with an operational specialist contract
- Added source grounding, outline sequencing, mode constraints, and manifest partial assembly
- Added `source-bundle.json` as a first-class phase-2 artifact in the task, workflow, and checklist contracts
- Normalized `QUOTE` requests into canonical slide types plus `content_variant=quote`
- Updated README, ARCHITECTURE, epic docs, and runtime state for Epic 3 completion

## 2026-03-16 - v2.0.0 (Epic 2: slide-chief Orchestrator)

- Deepened `slide-chief` from shell to operational orchestrator (v2.0.0, ~970 lines)
- Added Briefing Normalization Protocol with 6 heuristics and output schema
- Added Planning Rules Engine: format selection (7 formats), mode selection (3 modes), aspect ratio, induction mode, max_slides calculation, sequence rules (12 slide types)
- Added Routing Decision Tree with 10 heuristics, 13 handoffs, 100% coverage matrix
- Added 3 output examples, 10 anti-patterns, 3 objection algorithms
- Added Level 3 Voice DNA with 4 behavioral states
- Upgraded `normalize-briefing.md` task from skeleton to full 6-phase workflow with elicitation, veto conditions, and output example
- Updated ARCHITECTURE.md with routing coverage details

## 2026-03-16 - v1.0.0

- Bootstrapped `slides-creator` as an Epic 1 brownfield-light squad shell
- Upgraded workspace integration to `controlled_runtime_consumer`
- Fixed MVP target to `apps/ds` presenter parity
- Added `slide-chief` activation shell, lifecycle tasks, workflow shell, and QA checklist
- Initialized create-squad runtime artifacts and epic scaffolding
