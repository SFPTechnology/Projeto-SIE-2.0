# Three-Way Benchmark & Architecture Vision — Index

**Hermes Agent × OpenClaw × Sinkra Hub**
**Date:** 2026-04-04

---

## Documents

### Benchmark Artifacts

| # | Document | Description |
|---|----------|-------------|
| 1 | [metadata.json](metadata.json) | Benchmark metadata (subjects, scoring dimensions) |
| 2 | [comparison-matrix.md](comparison-matrix.md) | 12-dimension three-way feature comparison |
| 3 | [scorecard.json](scorecard.json) | Quantitative scoring (machine-readable) |
| 4 | [scorecard.md](scorecard.md) | Quantitative scoring with analysis (Sinkra 63.7 / OC 60.4 / HA 59.9) |
| 5 | [battle-card.md](battle-card.md) | 1-page quick comparison card |
| 6 | [executive-report.md](executive-report.md) | Executive report with strategic assessment |

### Architecture Vision

| # | Document | Description |
|---|----------|-------------|
| 7 | [**architecture-vision.md**](architecture-vision.md) | **Main document** — 10 sections, full architecture with ASCII diagrams |
| 8 | [synergy-positioning.md](synergy-positioning.md) | Sinkra's position in the synergy quadrant (3-axis analysis) |

### Visual Diagrams (Mermaid)

| # | Diagram | Description | Render |
|---|---------|-------------|--------|
| 9 | [architecture-vision.mmd](architecture-vision.mmd) | Full three-layer architecture (L1 Distribution → L2 Intelligence → L3 Governance) | `mmdc -i architecture-vision.mmd -o architecture-vision.svg` |
| 10 | [flywheel.mmd](flywheel.mmd) | Training flywheel (23 channels → RL → better models → better channels) | `mmdc -i flywheel.mmd -o flywheel.svg` |
| 11 | [three-axis-positioning.mmd](three-axis-positioning.mmd) | Quadrant chart: Intelligence × Distribution with all 3 projects + hybrid target | `mmdc -i three-axis-positioning.mmd -o positioning.svg` |
| 12 | [coverage-comparison.mmd](coverage-comparison.mmd) | Bar chart: capability coverage by combination (62%→97%) | `mmdc -i coverage-comparison.mmd -o coverage.svg` |
| 13 | [executor-taxonomy.mmd](executor-taxonomy.mmd) | SINKRA executor types (Human/Agent/Worker/Clone) mapped across all 3 projects | `mmdc -i executor-taxonomy.mmd -o executor.svg` |

### Prior Benchmarks (Referenced)

| # | Document | Location |
|---|----------|----------|
| — | Hermes vs OpenClaw (2-way) | `docs/bench/hermes-agent-vs-openclaw/` (8 artifacts) |
| — | Synergy Analysis | `docs/bench/hermes-agent-vs-openclaw/deep/synergy-analysis.md` |
| — | SINKRA Map (Hermes) | `outputs/sinkra-squad/hermes-agent/phase-1-*` (3 artifacts) |
| — | SINKRA Map (OpenClaw) | `outputs/sinkra-squad/openclaw/phase-1-*` (3 artifacts) |

---

## Key Findings

### The Three-Layer Model

```
L3: GOVERNANCE (Sinkra)  → HOW agents coordinate — 473 agents, constitution, quality gates
L2: INTELLIGENCE (Hermes) → WHAT the agent knows — self-improving, RL, Honcho memory
L1: DISTRIBUTION (OpenClaw) → WHERE it reaches users — 23 channels, 3 apps, 93 plugins
```

### Coverage by Combination

| Combination | Coverage | Net Synergy |
|------------|:--------:|:-----------:|
| Hermes alone | 62% | — |
| OpenClaw alone | 72% | — |
| Sinkra alone | 45% | — |
| H + OC | 93% | 7.2% |
| **H + OC + S** | **97%** | **22%** |

### The Insight

> Sinkra is not a third product in the hybrid — it is the **platform where the hybrid lives**.

---

## How to Render Diagrams

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Render all diagrams
cd docs/bench/hermes-agent-vs-openclaw-vs-sinkra-hub/
for f in *.mmd; do mmdc -i "$f" -o "${f%.mmd}.svg" -t dark; done
```

Or use the repo's D2 pipeline:
```bash
# Convert Mermaid to D2 (if needed)
# Then: d2 diagram.d2 diagram.svg
```

---

*Total artifacts in this benchmark set: 13 documents + 5 Mermaid diagrams*
*Total across all benchmarks: 28 artifacts*
