# Dependency Graph — Absorption Sequencing

## DAG de Gaps

```
Wave 1 (P0 Critical — sequential):

GAP-03 (MCP, 5pts) ──┐
                     │
GAP-02 (Dist, 8pts) ─┤── parallel possible
                     │
GAP-01 (Sandbox, 13pts) ──► enables GAP-09 in Wave 3

Wave 2 (P1 High — mostly parallel):

GAP-07 (Bench, 3pts) ── independent
GAP-04 (Model, 5pts) ── independent
GAP-06 (Scholarly, 5pts) ── parallel with GAP-04
GAP-05 (Memory, 13pts) ── reads from GAP-04 if local backend, parallel with rest

Wave 3 (P2 Polish):

GAP-10 (Dual License, 2pts) ── independent
GAP-09 (FigureAgent, 8pts) ── BLOCKED by GAP-01 sandbox
GAP-08 (Parallel) ── DEFERRED (not in critical path)
```

## Visual Dependencies

```
                ┌─────────────────────────────────────┐
                │  Wave 1 (Critical Path)             │
                └─────────────────────────────────────┘
                          │
                          │
   ┌──────────────┬──────┴───────────┬──────────────┐
   │              │                  │              │
   ▼              ▼                  ▼              ▼
GAP-03 MCP    GAP-02 Dist       GAP-01 Sandbox  (independent of each other)
 (5pts)        (8pts)            (13pts)
   │              │                  │
   │ unlocks      │ unlocks          │ unlocks
   │ ── MCP       │ ── PyPI/Docker   │ ── Sandbox
   │    clients   │    adoption      │    capability
   │                                  │
   ▼                                  ▼
[Wave 2 starts]                  enables GAP-09 in W3

                ┌─────────────────────────────────────┐
                │  Wave 2 (P1 High — mostly parallel) │
                └─────────────────────────────────────┘
                          │
   ┌──────────────┬──────┴───────────┬─────────────┐
   │              │                  │             │
   ▼              ▼                  ▼             ▼
GAP-07 Bench  GAP-04 Model        GAP-06 Schol  GAP-05 Memory
 (3pts)        (5pts)              (5pts)        (13pts)
   │              │                  │             │
   │              │                  │             │
   └──────────────┴──────┬───────────┴─────────────┘
                          │
                          ▼
                [Wave 3 starts]

                ┌─────────────────────────────────────┐
                │  Wave 3 (P2 Polish)                 │
                └─────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        GAP-10 Dual License     GAP-09 FigureAgent
         (2pts)                  (8pts) [depends GAP-01]

        GAP-08 Parallel: DEFERRED
```

## Critical Path Analysis

**Caminho mais longo:**
1. GAP-01 (13pts) ── 4 sprints
2. → GAP-09 (8pts) ── 2 sprints
**Total CP:** ~6 sprints = ~12 weeks

**Caminho paralelo independente:**
- GAP-03 (5) + GAP-02 (8) + Wave 2 gaps + GAP-10 (2) podem rodar em paralelo se houver capacity

**Capacity assumption:** 1 dev FT
- Wave 1: ~8 weeks (sequential GAP-01 path + parallel GAP-02/03 where possible)
- Wave 2: ~8 weeks (parallel GAP-04/05/06/07)
- Wave 3: ~4 weeks (GAP-10 quick + GAP-09 longer after sandbox done)
- **Total:** ~20 weeks ≈ 5 months

**Capacity assumption:** 2 devs FT
- Wave 1: ~5 weeks (parallel)
- Wave 2: ~4 weeks (more parallel)
- Wave 3: ~3 weeks
- **Total:** ~12 weeks ≈ 3 months

## Risk-Based Ordering Override

Sequência recomendada se quiser **maximizar ROI early**:

1. **GAP-07 (Benchmark, 3pts)** — first. Marketing leverage massivo, quick win, sem dependency.
2. **GAP-03 (MCP, 5pts)** — second. Composability immediate value.
3. **GAP-02 (Distribution, 8pts)** — third. Adoção community.
4. **GAP-06 (Scholarly, 5pts)** — fourth. Quick + academic credibility.
5. **GAP-01 (Sandbox, 13pts)** — fifth. Maior payback, mais effort.
6. **GAP-04 (Model backend, 5pts)** — sixth. Cost reduction.
7. **GAP-05 (Memory, 13pts)** — seventh. Longest single item.
8. **GAP-10 (Dual License, 2pts)** — eighth. Quick win.
9. **GAP-09 (FigureAgent, 8pts)** — ninth. Quando sandbox pronto.
10. **GAP-08 (Parallel)** — DEFERRED.

**Total:** 62 pts em sequência otimizada por ROI.

## External Dependencies

| Dep | Risk | Mitigation |
|---|---|---|
| MCP spec stability | LOW | Pin to spec v1, monitor changes |
| PyPI publishing rights | LOW | Already have `pypi.org/project/sinkra/` reservation |
| Docker Hub account | LOW | Need to set up `sinkra` namespace |
| HF model availability | LOW | Apache-2.0, models persist |
| HuggingFace Spaces leaderboard | MEDIUM | Bench may change methodology |
| Apache-2.0 NOTICE compliance | LOW | CI check |
| AGPLv3 community uptake | MEDIUM | Marketing investment needed |

## Resource Mapping

| Gap | Effort | Tech skills needed |
|---|---|---|
| GAP-01 Sandbox | 13pts | Docker, security, Next.js API routes |
| GAP-02 Distribution | 8pts | Python packaging, GH Actions, Docker |
| GAP-03 MCP | 5pts | TypeScript/Python, MCP spec |
| GAP-04 Model backend | 5pts | HF transformers, vLLM, GPU detection |
| GAP-05 Memory | 13pts | SQLite/Postgres, schema design, confidence scoring |
| GAP-06 Scholarly | 5pts | API integration (arXiv/PubMed/SS), adapter pattern |
| GAP-07 Benchmark | 3pts | Bench framework setup, eval logging |
| GAP-09 FigureAgent | 8pts | matplotlib/plotly, sandbox integration |
| GAP-10 Dual License | 2pts | License selection, AGPLv3 fork |

**Specializations needed:**
- Backend engineer (sandbox, distribution, MCP, memory, scholarly): 80% of effort
- DevOps (CI/CD, Docker Hub, PyPI): 10%
- QA (benchmark + regression): 10%
