# Gap Analysis — Deepresearch Absorption Benchmark

> Bidirectional gap analysis. **10 AIOX gaps vs open-source (P0/P1/P2) + 6 open-source gaps vs AIOX (monetization potential).**

## AIOX Gaps vs Open-Source

### 🔴 P0 — Critical (bloqueiam scenarios principais)

#### GAP-01 — Docker code-execution sandbox

- **Score delta:** -100 (AIOX 0 vs AutoResearchClaw 100)
- **Best in class:** AutoResearchClaw (network-policy-aware hardened)
- **Secondary:** DeerFlow, Local DR
- **License compat:** MIT — REUSE friendly
- **Effort:** 13 pts
- **Target:** `apps/research /api/research/sandbox` + `tech-research phase-3-sandbox-exec`
- **ROI:** Unlocks academic paper scenario (+24.5 pts)

#### GAP-02 — Distribution via PyPI + Docker Hub

- **Score delta:** -87 (AIOX 10 vs GPT-Researcher 97)
- **Best in class:** GPT-Researcher (PyPI + Docker Hub + Claude Skill marketplace)
- **License compat:** Apache-2.0 — full REUSE
- **Effort:** 8 pts
- **Target:** `packages/@sinkra/research-cli` (novo) + `infrastructure/docker/research.Dockerfile`
- **ROI:** Adoção community + posicionamento marketplace

#### GAP-03 — MCP Server nativo

- **Score delta:** -100 (AIOX 0 vs GPT-Researcher/LangChain ODR 95-100)
- **Best in class:** GPT-Researcher + LangChain ODR
- **License compat:** MIT + Apache-2.0
- **Effort:** 5 pts
- **Target:** `packages/@sinkra/research-mcp` (novo MCP server)
- **ROI:** Composability cross-IDE + cross-agent

### 🟠 P1 — High (dobram score qualitativo)

#### GAP-04 — Purpose-trained model backend (opcional)

- **Score delta:** -36 (AIOX 38.75 vs OpenResearcher/DeepResearcher/Tongyi 75-79)
- **License compat:** Apache-2.0
- **Effort:** 5 pts
- **Target:** `squads/research/data/model-backends.yaml` + `apps/research /api/research/clis` auto-detect GPU
- **ROI:** Cost reduction + air-gapped capable + posicionamento academic

#### GAP-05 — Cross-session memory with confidence scores

- **Score delta:** -40 (AIOX 52.5 vs DeerFlow TIAMAT 92.5)
- **License compat:** MIT
- **Effort:** 13 pts
- **Target:** `packages/@sinkra/research-memory` + `squads/research/data/memory-schema.yaml`
- **ROI:** Continuous learning + cross-run quality compounding

#### GAP-06 — Scholarly DB integration (arXiv, PubMed, Semantic Scholar)

- **Score delta:** -70 (AIOX 30 vs LDR 100)
- **License compat:** MIT (LDR)
- **Effort:** 5 pts
- **Target:** `squads/research/tasks/scholarly-search.md` + `adapters/{arxiv,pubmed,semantic-scholar}.py`
- **ROI:** Academic paper +20pts + credibility de citações

#### GAP-07 — Public benchmark score

- **Score delta:** -50 (AIOX 0 score público vs 4 players com score)
- **License compat:** Benchmarks open (HF Spaces)
- **Effort:** 3 pts
- **Target:** `docs/research/_eval-logs/` + apps/research benchmark dashboard
- **ROI:** Marketing leverage massivo

### 🟡 P2 — Medium (polimento competitivo)

#### GAP-08 — True parallel subagent spawn

- **Score delta:** -33
- **Effort:** 8 pts
- **Note:** Inline é mais barato em tokens. Considerar opt-in `--parallel-subagents`.

#### GAP-09 — FigureAgent (visual generation)

- **Score delta:** -90 (no academic paper scenario)
- **Effort:** 8 pts
- **Blocked by:** GAP-01 (precisa sandbox)
- **ROI:** Academic paper + executive reports

#### GAP-10 — License re-evaluation (dual: Elastic v2 + AGPLv3)

- **Score delta:** -46
- **Effort:** 2 pts
- **ROI:** Community contribution + adoção

## Open-Source Gaps vs AIOX (Monetization Potential)

### INV-GAP-01 — Quality Gates with VETO halt

- **AIOX score 100 vs open-source avg 59**
- COVERAGE_GATE + CITATION_GATE + Incremental Learning Log
- **Monetization:** Vendable as **"Research Governance Layer"** on top of any open-source backend

### INV-GAP-02 — Product Discovery framework

- **AIOX score 96.5 vs open-source avg 56**
- JTBD + Mom Test + Villain OSINT + WTP signals integrados
- **Monetization:** Vertical workflow PT-BR é **blue ocean** (confirmed pela research panel — SparkToro precedent $1.98M ARR)

### INV-GAP-03 — 14 specialist personas com lineage acadêmico

- Booth/Creswell/Forsgren/Gilad/Klein/Sackett/etc
- Open-source tem 1-3 agent roles. AIOX tem 14 com methodology DNA distinto
- **Monetization:** Specialized methodology workflows (PICO/OSINT/DORA/competitive intel) sem competidor direto

### INV-GAP-04 — PT-BR/LatAm Vertical

- **AIOX score 92 vs open-source avg 35**
- 4 negócios dogfood + Academia Lendária distribution + Sebrae 4.6M SMB market
- **Monetization:** SMB tier defensável $50-300/mo (SparkToro precedent)

### INV-GAP-05 — Multi-Mode Unified

- 1 squad para 5+ modos (tech-research + competitive intel + product discovery + benchmarking + marketing)
- Open-source típico: 1 modo fixo
- **Monetization:** All-in-one positioning vs single-purpose tools

### INV-GAP-06 — Tri-layer Architecture

- Squad (brain) + Skill (execution) + App (observability)
- Open-source típico: 1 tool standalone
- **Monetization:** Enterprise procurement narrative (clean architecture)

## Priority Summary

| Tier | Count | Effort (pts) |
|---|---:|---:|
| 🔴 P0 Critical | 3 | 26 |
| 🟠 P1 High | 4 | 26 |
| 🟡 P2 Medium | 3 | 18 |
| **Total** | **10** | **70** |

## Expected Score Trajectory

| State | Score | vs Now |
|---|---:|---:|
| Current (2026-05-18) | 60.25 | baseline |
| Post-P0 absorption | ~72 | +12 |
| Post-P0 + P1 | ~82 | +22 |
| Post-all (composition target) | ~88 | +28 |

## Absorption Strategy (IDS Principles)

**REUSE > ADAPT > CREATE.**

Priorizar **P0** primeiro:
1. Sandbox (GAP-01) — desbloqueia academic paper + FigureAgent (GAP-09)
2. Distribution (GAP-02) — desbloqueia adoção massiva
3. MCP (GAP-03) — desbloqueia composability

P1 dobra o score qualitativo (4 features → +10pts).

P2 = polimento competitivo (3 features → +6pts).

**Tudo respeitando licenças MIT/Apache. Jamais copiar Jina proprietary code.**
