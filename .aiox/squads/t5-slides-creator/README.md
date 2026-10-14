# Slides Creator Squad

## Overview

Squad operacional para transformar briefing, materiais-fonte, template registry e
brand context em decks prontos para handoff a um runtime funcional externo ao
monorepo atual.

## Purpose

`slides-creator` existe para parar de tratar slides como artefatos soltos de
TSX e passar a tratá-los como um sistema governado: briefing normalizado,
manifesto canônico, render com paridade de presenter e QA visual obrigatório.

## Current Scope

Waves/Epics 1-8 entregam o bootstrap estrutural do squad, o `slide-chief`
operacional, o `content-architect`, `template-curator`, `design-renderer`,
`visual-scout` e `qa-inspector` operacionais, o workflow `generate-presentation`
end-to-end com checkpoints formais e o handoff final para operacao MVP.

## v2 Upgrades

A versao v9.0.0 introduz 4 upgrades independentes, cada um controlado por feature flag:

| # | Upgrade | Feature Flag | Descricao |
|---|---------|-------------|-----------|
| 1 | Auto Illustration Pipeline | `ENABLE_VISUAL_GENERATION` | Classificacao semantica de slides + geracao automatica de diagramas e ilustracoes |
| 2 | Visual Rendering Tools | `ENABLE_VISUAL_GENERATION` | Engines D2, Mermaid, Kroki, GPT Image, Recraft, Plotly com fallback chain |
| 3 | Andragogic Slide Design System | `ENABLE_ANDRAGOGIC_VALIDATION` | Mayer 12 principios + Kolb cycle + DPC + Dreyfus calibration |
| 4 | YouTube to Presentation Pipeline | `ENABLE_YOUTUBE_ENTRYPOINT` | Transcricao + keyframes + fusao multimodal de video para deck |

Todos os upgrades sao backward-compatible: com flags desativadas, a pipeline v1 funciona identicamente.

### Feature Flags

```bash
ENABLE_VISUAL_GENERATION=false       # Upgrades 1 + 2
ENABLE_ANDRAGOGIC_VALIDATION=false   # Upgrade 3
ENABLE_YOUTUBE_ENTRYPOINT=false      # Upgrade 4
```

### Configuracao do ambiente v2

Consultar `docs/environment-setup-v2.md` para pre-requisitos, instalacao, Docker setup e troubleshooting.

## When to Use This Squad

Use `slides-creator` quando você precisar:

- transformar briefing em deck navegável e apresentável
- operar templates de slides de forma brand-agnostic
- publicar deck com paridade ao presenter existente no `ds`
- validar deck por thumbnails + fullscreen presenter + QA report
- preparar a fundação de um gerador de slides renderer-agnostic

## What's Included

### Agents

| Agent | Status | Focus |
|-------|--------|-------|
| `slide-chief` | operational orchestrator | Intake, routing, release gate |
| `content-architect` | operational specialist | Grounding, outline, payloads, manifest partial |
| `template-curator` | operational specialist | Registry mirror, template binding, reference induction, provenance |
| `design-renderer` | operational specialist | Manifest -> TSX, CSS vars, multi-ratio, `ds` presenter parity, thumbnails |
| `visual-scout` | operational specialist | Asset resolution, fallback chain, anti-pattern gate, provenance |
| `qa-inspector` | operational specialist | PPTEval + GAD + killer items + refinement routing |

### Tasks

- `create-presentation.md`
- `normalize-briefing.md`
- `prepare-ds-presenter.md`
- `review-presentation.md`
- `update-slides-creator.md`
- `delete-slides-creator.md`

### Workflows

- `generate-presentation.yaml`

### Checklists

- `presentation-readiness-checklist.md`

### Data

- `data/SOP-SLIDES-001.md`
- `data/SOP-SLIDES-003.md`
- `data/template-registry.yaml`
- `data/asset-resolution.yaml`

## Prerequisites

- **Runtime ds**: O alvo histórico `apps/ds` não está presente neste monorepo e também não há `.gitmodules` registrando esse submodule. Os caminhos em `data/template-registry.yaml` e na arquitetura representam a superfície-alvo histórica, não uma superfície local executável.
- **Workspace brand context**: `workspace/_system/config.yaml` and `workspace/businesses/{brand}/` must exist for brand-aware deck generation.
- **COO readiness gate**: Publishing decks to the `ds` canonical runtime surface requires COO/c-level approval.

## Quick Start

```text
@slide-chief
*create-presentation
*review-presentation
*status
```

## Functional Target

The long-term target remains the historical `ds` slide runtime, which is currently absent from this repository:

- gallery/preview surface in `apps/ds/src/components/brandbook/pages/slides-page.tsx`
- fullscreen presenter in `apps/ds/src/components/brandbook/slides/slide-fullscreen.tsx`
- route surface mounted from `apps/ds/src/app/(brandbook)/brandbook/showcase/slides/page.tsx`

While that runtime is unavailable here, the squad operates in `handoff_only`
mode and should treat those paths as external delivery references.

## Squad Structure

```text
squads/slides-creator/
├── agents/
│   ├── slide-chief.md
│   ├── content-architect.md
│   ├── template-curator.md
│   ├── design-renderer.md
│   ├── visual-scout.md
│   └── qa-inspector.md
├── checklists/
│   └── presentation-readiness-checklist.md
├── config.yaml
├── data/
│   ├── asset-resolution.yaml
│   ├── SOP-SLIDES-001.md
│   ├── SOP-SLIDES-003.md
│   ├── template-registry.yaml
│   ├── token-registry.yaml          # SINKRA-native (GAP-001 closed)
│   └── pipeline-execution-log.yaml  # SINKRA-native (GAP-002 closed)
├── README.md
├── CHANGELOG.md
├── ARCHITECTURE.md
├── tasks/
│   ├── create-presentation.md
│   ├── normalize-briefing.md
│   ├── prepare-ds-presenter.md
│   ├── review-presentation.md
│   ├── update-slides-creator.md
│   └── delete-slides-creator.md
├── templates/
│   └── README.md
└── workflows/
    └── generate-presentation.yaml
```

## Workspace Integration Governance

- **Integration level:** `controlled_runtime_consumer`
- **Rationale:** lê brand context do workspace e entrega deck via `ds`
  sob gate do `COO`
- **Read paths:** `workspace/_system/config.yaml`, `workspace/businesses/`,
  `workspace/domains/brand/`
- **Write paths:** none during squad bootstrap; app mutation is handed off
- **Template namespace:** `slides`
- **Owner:** `c-level/coo`
- **Execution mode:** `handoff_only`

### Required structural artifacts

- `config.yaml` with `workspace_integration.level`
- `.aiox/squad-runtime/create-squad/slides-creator/workspace-integration-level.yaml`
- `.aiox/squad-runtime/create-squad/slides-creator/workspace-handoff.yaml`
- `squads/c-level/` present in the repo

## Next Handoff

The squad bootstrap is complete. Primary operational commands are:

```text
@slide-chief
*create-presentation
*review-presentation
*status
```

Validation command:

```text
*validate-squad slides-creator
```

## Version History

- **v9.0.0** - v2 Visual Intelligence & Andragogic Upgrade: Auto Illustration Pipeline, Visual Rendering Tools (D2/Kroki/Mermaid), Andragogic Design System (Mayer/Kolb/DPC/Dreyfus), YouTube to Presentation Pipeline, 3 feature flags, 8 new env vars, budget guardrails
- **v8.1.0** - Audit remediation: P0 runtime artifacts, P0 submodule prerequisite docs, P1 template schemas, P1 QUOTE governance, P1 PRD path fix, P1 tier format standardization, P2 version dedup
- **v8.0.0** - Wave 8 / Epic 8 execution handoff: final handoff pack, create-squad runtime completion, validation cadence, MVP/deferred scope boundary
- **v7.0.0** - Wave 7 / Epic 7 workflow integration: artifact chain, handoff prompts, always-active checkpoints, refinement loop cap, release gate
- **v6.0.0** - Wave 6 / Epic 6 template and asset intelligence: `template-curator`, `visual-scout`, `template-selection-summary.md`, `asset-resolution.json`, registry mirror, degraded fallback contract
- **v5.0.0** - Epic 5 QA contract: `qa-inspector`, `qa/report.json`, killer items, accessibility, refinement routing
- **v4.0.0** - Epic 4 render contract: `design-renderer`, ds parity, CSS-variable/shared-module rules, thumbnails
- **v3.0.0** - Epic 3 grounded content: source bundle, outline, payloads, manifest partial
- **v2.0.0** - Epic 2 slide-chief orchestrator: intake, planning, routing coverage
- **v1.0.0** - Epic 1 bootstrap: structure, chief shell, workflow shell, runtime artifacts

---

_Version: 9.0.0_
_Compatible with: AIOX v4+_
