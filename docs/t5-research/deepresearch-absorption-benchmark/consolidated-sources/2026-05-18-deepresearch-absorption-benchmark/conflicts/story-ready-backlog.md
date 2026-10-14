# Story-Ready Backlog — Deepresearch Absorption

> 12 stories prontas para go-to-backlog. Cada uma com acceptance criteria + estimated points + dependencies.

## Epic: EPIC-DRA — Deepresearch Absorption Benchmark Execution

**Goal:** Levar AIOX Research de score 60.25 → 88 absorvendo 9 gaps prioritários.
**Source:** `docs/bench/deepresearch-absorption-benchmark/ADR-001-absorption-strategy.md`
**Estimated total:** 62 pts | ~20 weeks 1FT

---

### STORY-DRA-1.1 — MCP Server expondo /tech-research [5 pts] [Wave 1]

**As a** Claude Desktop / Cursor / Cline user
**I want** invocar `/tech-research` via MCP tool
**So that** I can use AIOX research from any Claude-compatible session

**Acceptance:**
- [ ] `packages/@sinkra/research-mcp/` created
- [ ] 3 MCP tools exposed: `tech_research_query`, `tech_research_followup`, `tech_research_status`
- [ ] stdio transport works (Claude Desktop)
- [ ] HTTP/SSE transport works (remote)
- [ ] Schema validation rejects bad input
- [ ] 6 error codes documented work
- [ ] NOTICE.txt + Apache-2.0 attribution

**Source absorption:** LangChain Open DR + GPT-Researcher (`docs/bench/deepresearch-absorption-benchmark/contracts/mcp-contract.md`)

---

### STORY-DRA-1.2 — PyPI + Docker Hub Distribution [8 pts] [Wave 1]

**As a** dev wanting AIOX research without cloning hub
**I want** `pip install @sinkra/research-cli` AND `docker pull sinkra/research`
**So that** onboarding é 1-comando

**Acceptance:**
- [ ] `packages/@sinkra/research-cli/` created
- [ ] `pip install @sinkra/research-cli` works on clean venv
- [ ] `docker run sinkra/research --query "..."` works
- [ ] CI auto-publishes on tag
- [ ] NOTICE.txt validated
- [ ] Standalone (no hub clone needed)

**Source absorption:** GPT-Researcher pyproject pattern + LocalDR Docker

---

### STORY-DRA-1.3 — Docker Sandbox para Code Execution [13 pts] [Wave 1]

**As a** researcher whose query requires running code (benchmarks, calculations, data analysis)
**I want** sandbox execution durante research
**So that** I can verify claims via code without leaving the research flow

**Acceptance:**
- [ ] `apps/research/src/lib/sandbox/` integrated
- [ ] Endpoint `/api/research/runs/[runId]/sandbox/execute` works
- [ ] Container hardened (egress deny + read-only FS + resource limits)
- [ ] SSE streaming output works
- [ ] Phase YAML `phase-3-sandbox-exec.yaml` invokes when query requires
- [ ] Security audit passes
- [ ] Test: malicious code blocked from exfiltrating

**Source absorption:** AutoResearchClaw network-policy-aware + DeerFlow persistent sandbox

---

### STORY-DRA-2.1 — Public Benchmark Score em DeepResearchBench [3 pts] [Wave 2]

**As a** prospective AIOX user wanting verifiable quality
**I want** AIOX score público em standardized bench
**So that** I can compare with LangChain ODR (#6 @ 0.4344) etc

**Acceptance:**
- [ ] Deep Research Bench harness cloned
- [ ] `/tech-research` runs against bench dataset
- [ ] Results submitted to HF Spaces leaderboard
- [ ] Badge visible em GitHub README
- [ ] Eval logs persisted em `docs/research/_eval-logs/`
- [ ] Score ≥ 0.40

---

### STORY-DRA-2.2 — Scholarly DB Adapters (arXiv + PubMed + Semantic Scholar) [5 pts] [Wave 2]

**As a** academic researcher
**I want** AIOX citar fontes scholarly nativamente
**So that** CITATION_GATE é forte para queries academic

**Acceptance:**
- [ ] `packages/@sinkra/research-adapters/` created
- [ ] arxiv.py adapter functional
- [ ] pubmed.py adapter functional
- [ ] semantic_scholar.py adapter functional
- [ ] CITATION_GATE prefers scholarly when available
- [ ] Test: academic query produces ≥3 scholarly citations

**Source absorption:** LocalDR search_engines/

---

### STORY-DRA-2.3 — Model Backend Opcional (OpenResearcher/DeepResearcher/Tongyi) [5 pts] [Wave 2]

**As a** GPU-equipped user wanting cost reduction
**I want** local model backend (HF Apache-2.0)
**So that** I reduce API costs and run air-gapped

**Acceptance:**
- [ ] `squads/research/data/model-backends.yaml` registry created
- [ ] Auto-detect GPU in `/api/research/clis`
- [ ] HF transformers + vLLM integration
- [ ] UI switch para backend local
- [ ] BYOK fallback funcional sem GPU
- [ ] NOTICE.txt + Apache-2.0 attribution

---

### STORY-DRA-2.4 — Cross-Session Memory Layer (TIAMAT-inspired) [13 pts] [Wave 2]

**As a** repeat user
**I want** AIOX lembrar contexto entre runs
**So that** quality compounds over time

**Acceptance:**
- [ ] `packages/@sinkra/research-memory/` created
- [ ] Schema YAML defined
- [ ] SQLite backend functional
- [ ] CRUD APIs em apps/research
- [ ] Phase 0 reads memory
- [ ] Phase 5 writes new facts
- [ ] Confidence decay implemented
- [ ] Migration scripts versioned
- [ ] Performance: 10k facts query <100ms

**Source absorption:** DeerFlow TIAMAT pattern

---

### STORY-DRA-3.1 — Dual License (Elastic v2 + AGPLv3 CE) [2 pts] [Wave 3]

**As a** open-source contributor
**I want** AGPLv3 community edition de apps/research
**So that** I can contribute without commercial license fricion

**Acceptance:**
- [ ] `apps/research-community/` created
- [ ] AGPLv3 LICENSE present
- [ ] Enterprise features stripped
- [ ] README clearly differentiates editions
- [ ] CI lints license headers

---

### STORY-DRA-3.2 — FigureAgent (Visual Generation) [8 pts] [Wave 3, blocked by STORY-DRA-1.3]

**As a** academic researcher
**I want** figures geradas automaticamente no report
**So that** output é paper-grade

**Acceptance:**
- [ ] `squads/research/agents/figure-agent.md` persona created
- [ ] Phase `phase-4-5-visualize.yaml` created
- [ ] Uses sandbox (STORY-DRA-1.3 required)
- [ ] PNG + SVG output formats
- [ ] Embedded em MD/PDF report
- [ ] Test: time-series query → correct chart

**Source absorption:** AutoResearchClaw FigureAgent concept

---

### STORY-DRA-1.2.b — NPM Package for Node ecosystem [DEFERRED]

Considerar pós-Wave-2 baseado em demand.

---

### STORY-DRA-X.1 — Parallel Subagents Opt-in [DEFERRED]

GAP-08. Reavaliar pós-Wave-2.

---

### STORY-DRA-W1-CHECKPOINT — Wave 1 Bench Re-score

**Acceptance:**
- [ ] Re-compute scorecard.json
- [ ] AIOX score ≥ 70
- [ ] No regression em COVERAGE_GATE / CITATION_GATE / multi-mode
- [ ] AIOX v5.1.0 tag pushed

---

### STORY-DRA-W2-CHECKPOINT — Wave 2 Bench Re-score

**Acceptance:**
- [ ] Re-compute scorecard.json
- [ ] AIOX score ≥ 80
- [ ] AIOX wins ≥ 5 scenarios
- [ ] Public benchmark score visible
- [ ] AIOX v5.5.0 tag pushed

---

### STORY-DRA-W3-CHECKPOINT — Wave 3 Bench Re-score

**Acceptance:**
- [ ] Re-compute scorecard.json
- [ ] AIOX score ≥ 85 (target 88)
- [ ] AIOX v6.0.0 tag pushed
- [ ] Community PRs aceitas ≥ 5 dentro 90 dias

---

## Total Effort Summary

| Wave | Stories | Effort (pts) | Weeks (1FT) | Weeks (2FT) |
|---|---|---:|---:|---:|
| Wave 1 | 3 main + 1 checkpoint | 26 | 8 | 5 |
| Wave 2 | 4 main + 1 checkpoint | 26 | 8 | 4 |
| Wave 3 | 2 main + 1 checkpoint | 10 | 4 | 3 |
| **Total** | **9 main + 3 checkpoint** | **62** | **20** | **12** |

## Next Actions

1. Roundtable approval of ADR-001
2. Create EPIC-DRA in backlog
3. Spawn 9 stories from this backlog
4. @aiox-sm validates stories
5. @aiox-po sequences sprints
6. Wave 1 Sprint 1 begins
