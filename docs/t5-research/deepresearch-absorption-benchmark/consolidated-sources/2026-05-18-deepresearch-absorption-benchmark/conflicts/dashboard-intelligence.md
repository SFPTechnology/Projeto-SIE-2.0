# Dashboard Intelligence — Observatory Consumption Guide

> Como o **Research Observatory** (`apps/research`) deve consumir este bench.

## Routing

```
URL: /observatory/bench?slug=deepresearch-absorption-benchmark
Reads: docs/bench/deepresearch-absorption-benchmark/bench-output-dash.json
Falls back to: docs/bench/deepresearch-absorption-benchmark/MANIFEST.json
```

## Display Hierarchy

### Level 1 — Hero Banner
- Title: "Deepresearch Absorption Benchmark"
- Subtitle: "AIOX Research Ecosystem vs 9 Open-Source Players (2026)"
- AIOX score: **60.25** (large badge)
- Rank: 5º de 10 (chip)
- Direct link to executive-report.md

### Level 2 — Scorecard Visualization

Bar chart (recharts ou D3):
- X-axis: 10 players
- Y-axis: score 0-100
- Color: AIOX em amarelo destaque, demais em paleta

Source: `scorecard.json#ranking`

### Level 3 — Group Heatmap (13 grupos × 10 players)

Heatmap table:
- Rows: 13 groups (Entrada, Planejamento, Execução, etc)
- Cols: 10 players
- Cell value: group score 0-100
- Cell color: gradient red→yellow→green

Source: `scorecard.json#ranking[].by_group`

### Level 4 — Scenario Selector

Dropdown com 8 scenarios:
- S1 Academic Paper
- S2 Product Discovery (AIOX wins)
- S3 Privacy/Air-Gapped
- S4 Competitive Intelligence (AIOX wins)
- S5 Quick Q&A
- S6 Benchmark-Driven
- S7 PT-BR Vertical (AIOX wins)
- S8 Claude Skill Marketplace

Selecionar scenario → re-renderiza scorecard com weights overrideados.

Source: `scenario-scorecards.json#scenarios[]`

### Level 5 — Gap Analysis Drill-Down

Card list:
- 10 GAPs (P0/P1/P2)
- Score delta visualization
- Estimated effort pts
- License compat indicator
- Click → expand → ver detalhes do gap

Source: `gap-analysis.json#aiox_gaps_vs_opensource[]`

### Level 6 — Roadmap Gantt

Gantt chart:
- 3 waves
- 12 sprints
- Weeks 0-20
- Story progress (if EPIC-DRA created)

Source: `absorption-roadmap.md` (parsed)

### Level 7 — Evidence Drawer

Side drawer:
- Per claim: confidence (ALTA/MEDIA), source URL/file
- Filter: ALTA only / MEDIA only / all

Source: `deep/evidence-strength-map.json`

### Level 8 — Player Inventories

Tab navigation por player:
- DeerFlow / GPT-Researcher / LangChain ODR / Local DR / OpenResearcher / DeepResearcher / Jina node-DR / AutoResearchClaw / Tongyi

Render: `inventories/{player}.md` em react-markdown

## Interactive Features

### Re-score com weights customizados

UI: 13 sliders (um por grupo). User ajusta pesos → recompute scorecard em real-time.

Server-side: re-aplica algoritmo `Sum(group_score × weight) / total_weight` em comparison-matrix.json data.

### Compare 2 players head-to-head

Selecionar 2 players → radar chart 13 dimensions sobreposto.

### Show evidence per claim

Click em qualquer cell do heatmap → modal com:
- Score
- Confidence
- Source (file path or URL)
- Rationale

## Performance

- All bench data é static JSON/MD → server-side render OK
- Total bench size: ~250 KB (60+ artifacts)
- Initial paint: <500ms
- Heatmap interactive: <100ms (no API call needed)

## Cross-Bench Comparison

If `apps/research/observatory/bench` lists multiple benches (slides-creator + deepresearch + future), enable:
- Cross-bench filter por AIOX rank
- "How is AIOX trending across our benches?"

## Mobile UX

Heatmap collapses to vertical bar chart per group. Scenarios become accordion.

## Empty State

If bench is incomplete (missing artifacts), show "Bench in progress" with checklist of expected files (from `MANIFEST.json`).

## Sources / Artifact Map

| Display Component | Source File |
|---|---|
| Hero score | `scorecard.json#ranking[0]` |
| Bar chart | `scorecard.json#ranking` |
| Heatmap | `comparison-matrix.json` + `scorecard.json` |
| Scenario selector | `scenario-scorecards.json` |
| Gap cards | `gap-analysis.json#aiox_gaps_vs_opensource` |
| Roadmap | `absorption-roadmap.md` (parsed) |
| Evidence drawer | `deep/evidence-strength-map.json` |
| Player tabs | `inventories/*.md` |
| Player metadata | `inventory-open-source-stack.json#players` |
| Bench manifest | `MANIFEST.json` |
