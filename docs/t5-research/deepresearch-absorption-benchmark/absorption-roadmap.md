# Absorption Roadmap — AIOX Research v5.0.0 → v6.0.0

> 3 waves, 12 sprints, ~20 semanas.

## Wave 1 — P0 Critical (Q3 2026, ~8 semanas)

### Sprint 1 (Week 1) — GAP-03 MCP Server (5 pts)

**Goal:** AIOX `/tech-research` consumível via MCP em Claude Desktop / Cursor / Cline.

**Stories:**
- STORY-DRA-1.1.1: Scaffold `packages/@sinkra/research-mcp/` (Node/TS or Python)
- STORY-DRA-1.1.2: Expose 3 MCP tools (query, followup, status)
- STORY-DRA-1.1.3: stdio transport (Claude Desktop)
- STORY-DRA-1.1.4: HTTP/SSE transport (remote MCP)
- STORY-DRA-1.1.5: Schema validation + error codes

**Deliverable:** `npm install @sinkra/research-mcp && sinkra-research-mcp` works in Claude Desktop config.

### Sprint 2 (Weeks 2-3) — GAP-02 Distribution (8 pts)

**Goal:** AIOX research instalável via `pip install` + `docker pull`.

**Stories:**
- STORY-DRA-1.2.1: Create `packages/@sinkra/research-cli/`
- STORY-DRA-1.2.2: Bundle skill + scripts + schemas without hub clone
- STORY-DRA-1.2.3: `pyproject.toml` + setuptools entry point
- STORY-DRA-1.2.4: GitHub Actions auto-publish on tag
- STORY-DRA-1.2.5: Dockerfile + Docker Hub `sinkra/research`
- STORY-DRA-1.2.6: NOTICE.txt + license header CI guard

**Deliverable:** `pip install @sinkra/research-cli` AND `docker run sinkra/research`.

### Sprint 3-4 (Weeks 4-7) — GAP-01 Docker Sandbox (13 pts)

**Goal:** Code execution durante research em sandbox hardened.

**Stories:**
- STORY-DRA-1.3.1: Docker SDK integration em `apps/research/src/lib/sandbox/`
- STORY-DRA-1.3.2: Endpoint `/api/research/runs/[runId]/sandbox/execute`
- STORY-DRA-1.3.3: Container image (ubuntu:22.04 + python + node + tools)
- STORY-DRA-1.3.4: Network policy (egress deny + allowlist)
- STORY-DRA-1.3.5: Resource limits (CPU 1c, memory 2GB, timeout 60s)
- STORY-DRA-1.3.6: SSE streaming output
- STORY-DRA-1.3.7: Add `tech-research phase-3-sandbox-exec.yaml` opt-in
- STORY-DRA-1.3.8: Security audit + pen test internal

**Deliverable:** Query with `requires_code_exec=true` triggers sandbox automatically. Stream output via SSE.

### Wave 1 Checkpoint (Week 8)

- [ ] Re-run scorecard → expect ~72 (vs 60.25 baseline)
- [ ] Regression tests pass (COVERAGE_GATE/CITATION_GATE/multi-mode intact)
- [ ] **AIOX v5.1.0 release**

## Wave 2 — P1 High (Q4 2026, ~8 semanas)

### Sprint 5 (Week 9) — GAP-07 Public Benchmark (3 pts)

**Goal:** Score público AIOX em DeepResearchBench / SimpleQA.

**Stories:**
- STORY-DRA-2.1.1: Clone Deep Research Bench harness
- STORY-DRA-2.1.2: Run `/tech-research` against bench dataset
- STORY-DRA-2.1.3: Submit results to HF Spaces leaderboard
- STORY-DRA-2.1.4: Add badge em README + apps/research dashboard
- STORY-DRA-2.1.5: Persist `docs/research/_eval-logs/`

**Deliverable:** Badge visible no GitHub README com score público.

### Sprint 6 (Week 10) — GAP-06 Scholarly DB (5 pts)

**Goal:** arXiv + PubMed + Semantic Scholar nativo no CITATION_GATE.

**Stories:**
- STORY-DRA-2.2.1: Create `packages/@sinkra/research-adapters/`
- STORY-DRA-2.2.2: arxiv.py adapter
- STORY-DRA-2.2.3: pubmed.py adapter
- STORY-DRA-2.2.4: semantic_scholar.py adapter
- STORY-DRA-2.2.5: Integrate em `tech-research phase-3` secondary search
- STORY-DRA-2.2.6: CITATION_GATE preference for scholarly when available

**Deliverable:** Academic query produces report with ≥3 scholarly citations.

### Sprint 7 (Weeks 11-12) — GAP-04 Model Backend (5 pts)

**Goal:** OpenResearcher / DeepResearcher / Tongyi como backend opcional.

**Stories:**
- STORY-DRA-2.3.1: `squads/research/data/model-backends.yaml` registry
- STORY-DRA-2.3.2: Auto-detect GPU em `/api/research/clis`
- STORY-DRA-2.3.3: HF transformers wrapper + vLLM
- STORY-DRA-2.3.4: UI switch para backend local
- STORY-DRA-2.3.5: Fallback BYOK quando GPU absent
- STORY-DRA-2.3.6: NOTICE.txt + Apache-2.0 attribution

**Deliverable:** GPU users get local backend option; BYOK works unchanged.

### Sprint 8-9 (Weeks 13-16) — GAP-05 Cross-Session Memory (13 pts)

**Goal:** Memory layer com confidence scores cross-session.

**Stories:**
- STORY-DRA-2.4.1: Create `packages/@sinkra/research-memory/`
- STORY-DRA-2.4.2: Schema YAML `squads/research/data/memory-schema.yaml`
- STORY-DRA-2.4.3: SQLite backend (later: Postgres + pgvector)
- STORY-DRA-2.4.4: CRUD APIs em apps/research/api
- STORY-DRA-2.4.5: Tech-research phase-0 reads memory
- STORY-DRA-2.4.6: Tech-research phase-5 writes new facts
- STORY-DRA-2.4.7: Confidence decay over time
- STORY-DRA-2.4.8: Migration scripts versioned

**Deliverable:** Re-run query → recalls relevant prior facts → builds incremental knowledge.

### Wave 2 Checkpoint (Week 16)

- [ ] Re-run scorecard → expect ~82
- [ ] AIOX wins ≥ 5 scenarios (vs 3 baseline)
- [ ] **AIOX v5.5.0 release**

## Wave 3 — P2 Polish (Q1 2027, ~4 semanas)

### Sprint 10 (Week 17) — GAP-10 Dual License (2 pts)

**Goal:** AGPLv3 community edition aberta para contribuição.

**Stories:**
- STORY-DRA-3.1.1: Fork `apps/research/` → `apps/research-community/`
- STORY-DRA-3.1.2: Strip enterprise features
- STORY-DRA-3.1.3: AGPLv3 LICENSE
- STORY-DRA-3.1.4: README differentiation
- STORY-DRA-3.1.5: Marketing pages update

**Deliverable:** Community edition pública e contribuible.

### Sprint 11-12 (Weeks 18-20) — GAP-09 FigureAgent (8 pts) [requires GAP-01]

**Goal:** Geração de figuras paper-grade no report final.

**Stories:**
- STORY-DRA-3.2.1: `squads/research/agents/figure-agent.md` persona
- STORY-DRA-3.2.2: Phase YAML `phase-4-5-visualize.yaml`
- STORY-DRA-3.2.3: Sandbox-based matplotlib/plotly executor
- STORY-DRA-3.2.4: PNG/SVG output formats
- STORY-DRA-3.2.5: Embed figures em MD/PDF report

**Deliverable:** Academic query → report with embedded figures.

### Wave 3 Checkpoint (Week 20)

- [ ] Re-run scorecard → expect ~88 (vs 60.25 baseline = +27.75)
- [ ] AIOX wins ≥ 5 scenarios
- [ ] Community PRs aceitas ≥ 5 dentro 90 dias
- [ ] **AIOX v6.0.0 release**

## Cumulative Score Trajectory

```
Score
  88 ──────────────────────────────────────────────── 🎯 (v6.0.0)
                                                      ●
  82 ────────────────────────────────────────── ●
                                                v5.5.0
  72 ──────────────────────────── ●
                                  v5.1.0
  60 ─── ● ─────────────────────────────────────────
        v5.0.0 (baseline today)

      Week:  0      8       16       20
             ↑      ↑       ↑        ↑
             Today  W1      W2       W3
             V5.0.0 V5.1.0  V5.5.0   V6.0.0
```

## Resource Allocation

**Assuming 1 dev FT:**
- Wave 1: 8 weeks
- Wave 2: 8 weeks
- Wave 3: 4 weeks
- **Total: ~20 weeks**

**Assuming 2 devs FT (parallelize possible parts):**
- Wave 1: 5 weeks
- Wave 2: 4 weeks
- Wave 3: 3 weeks
- **Total: ~12 weeks**

## Dependencies & Sequencing

```
GAP-01 ──► enables GAP-09 (Wave 3)
GAP-02 ──┐
         ├──► standalone adoption + benchmark visibility
GAP-03 ──┘

GAP-04 ──┐
         ├──► air-gapped + cost reduction
GAP-05 ──┘

GAP-06 ──► CITATION_GATE strength

GAP-07 ──► marketing leverage standalone

GAP-10 ──► community adoption standalone
```

## Decision Points Between Waves

**Pós-Wave-1 (Week 8):**
- Bench re-score atinge 72?
- Adoção PyPI/Docker mensurável (downloads > 0)?
- MCP integration funcional em pelo menos 2 IDEs?
- IF YES → proceed Wave 2
- IF NO → debug + recover (delay 2-4 weeks)

**Pós-Wave-2 (Week 16):**
- Bench score 82?
- AIOX wins 5/8 scenarios?
- Public benchmark score visible?
- IF YES → proceed Wave 3
- IF NO → reprioritize Wave 3 gaps

**Pós-Wave-3 (Week 20):**
- Final score 88?
- Community PRs ≥ 5?
- v6.0.0 release ready?

## Sources

- `gap-analysis.json` — 10 gaps detailed
- `deep/absorption-decision-table.md` — GO/NO-GO per gap
- `deep/implementation-playbook.md` — sprint-by-sprint
- `dependency-graph.md` — sequencing
- `ADR-001-absorption-strategy.md` — overarching decision
