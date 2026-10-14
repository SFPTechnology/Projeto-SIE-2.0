# Absorption Priorities — 130-Dim Matrix Analysis

> **Founder direction (2026-05-18):** Training Methodology fica fora do foco (peso 0). Todo o resto é meta de absorção.

## Methodology

- Matriz expandida: **130 dims × 25 players = 3,250 cells**
- Filter: dims onde **AIOX score < 50** E **gap vs best competitor > 20pts**
- Excluídos: Training Methodology (peso 0, fora do foco) + Sinkra Fit (anchor self-ref, peso 0)
- Ordenação: `priority_index = gap × weight` (impacto no score total)

## Top 27 Absorption Targets

| Priority | Dim | Group | AIOX | Best | Gap | Wt | Absorb from |
|---:|---|---|---:|---:|---:|---:|---|
| 🔴 1 | **MCP Server expose** | Tool Runtime | 0 | 88 | 88 | 1.0 | deer-flow |
| 🔴 2 | **PubMed API native** | Tool Runtime | 0 | 95 | 95 | 1.0 | local-deep-research |
| 🔴 3 | **SearXNG self-hosted** | Tool Runtime | 0 | 95 | 95 | 1.0 | local-deep-research |
| 🔴 4 | **Semantic Scholar API** | Tool Runtime | 0 | 88 | 88 | 1.0 | local-deep-research |
| 🟠 5 | **archive.org snapshot** | Evidence Fidelity | 30 | 95 | 65 | 1.0 | local-deep-research |
| 🟠 6 | **Rollback to phase** | UX Operator | 30 | 95 | 65 | 0.9 | local-deep-research |
| 🟠 7 | **Browser automation (Playwright)** | Tool Runtime | 40 | 95 | 55 | 1.0 | local-deep-research |
| 🟠 8 | **True parallel sub-agent spawn** | Multi-Agent | 30 | 95 | 65 | 0.83 | local-deep-research |
| 🟠 9 | **Vector DB native** | Private KB | 25 | 88 | 63 | 0.86 | local-deep-research |
| 🟠 10 | **Sub-agent cost attribution** | Multi-Agent | 30 | 88 | 58 | 0.83 | deer-flow |
| 🟠 11 | **Cost meter live** | UX Operator | 35 | 88 | 53 | 0.9 | local-deep-research |
| 🟠 12 | **Multiple embedding models** | Private KB | 40 | 95 | 55 | 0.86 | local-deep-research |
| 🟡 13 | arXiv API native | Tool Runtime | 30 | 75 | 45 | 1.0 | local-deep-research |
| 🟡 14 | HN/Reddit community signals | Tool Runtime | 30 | 75 | 45 | 1.0 | local-deep-research |
| 🟡 15 | Max concurrent cap (semaphore) | Multi-Agent | 40 | 88 | 48 | 0.83 | local-deep-research |
| 🟡 16 | Doc chunking strategy | Private KB | 45 | 88 | 43 | 0.86 | local-deep-research |
| 🟡 17 | Public bench score | Evaluation Value | 0 | 55 | 55 | 0.67 | alibaba-deepresearch |
| 🟡 18 | GitHub API code search | Tool Runtime | 40 | 75 | 35 | 1.0 | local-deep-research |
| 🟡 19 | Statistical tests | Scientific Pipeline | 25 | 95 | 70 | 0.5 | local-deep-research |
| 🟡 20 | Paper-format output (LaTeX) | Scientific Pipeline | 30 | 95 | 65 | 0.5 | autoresearchclaw |
| 🟡 21 | Retraction check | Evidence Fidelity | 20 | 50 | 30 | 1.0 | drbench |
| 🟡 22 | Experimental protocol | Scientific Pipeline | 35 | 95 | 60 | 0.5 | autoresearchclaw |
| 🟡 23 | Formal hypothesis | Scientific Pipeline | 40 | 95 | 55 | 0.5 | autoresearchclaw |
| 🟡 24 | Rerank post-retrieval | Private KB | 25 | 55 | 30 | 0.86 | local-deep-research |
| 🟡 25 | Google Scholar scraping | Tool Runtime | 30 | 55 | 25 | 1.0 | autoresearchclaw |
| 🟡 26 | Hybrid search (BM25+vector) | Private KB | 30 | 55 | 25 | 0.86 | openresearcher |
| 🟡 27 | Team persistence cross-session | Multi-Agent | 25 | 50 | 25 | 0.83 | drbench |

Legenda: 🔴 P0 (gap ≥ 80) · 🟠 P1 (gap 50-79) · 🟡 P2 (gap 20-49)

## By Group — Where AIOX Loses Most

### Tool Runtime Integration (weight 14) — **9 targets, 5x P0/P1**

Maior gap absoluto. AIOX = 0 em MCP server, PubMed, SearXNG, Semantic Scholar. Local Deep Research é o package mestre — absorber adapters direto.

**Estratégia:**
- Sprint 1 (3 days): Build `packages/@sinkra/research-mcp` exposing tech-research as MCP server
- Sprint 2 (5 days): Build `packages/@sinkra/research-adapters` com arxiv.py + pubmed.py + semantic_scholar.py (ADAPT do `local-deep-research/src/local_deep_research/search_engines/`)
- Sprint 3 (3 days): SearXNG self-hosted Docker setup + integration
- **Score impact estimated:** AIOX Tool Runtime 38 → 75 (+37pts), total +5.2pts (×14 weight / 100)

### Multi-Agent Orchestration (weight 10) — **4 targets**

True parallel spawn é o maior gap. AIOX usa inline persona-fidelity. Deer-flow tem 31 files usando `asyncio.gather`.

**Estratégia:**
- Sprint 4 (5 days): Add opt-in `--parallel-subagents` flag spawning real `asyncio.gather` calls
- Sprint 5 (3 days): Cost attribution per sub-agent via `cost_meter` per-agent (absorver pattern de deer-flow)
- **Score impact:** Multi-Agent 56 → 80 (+24pts), total +2.4pts

### Private KB Grounding (weight 6) — **5 targets**

Sem vector DB nativo, sem hybrid search, sem rerank. GAP histórico do AIOX.

**Estratégia:**
- Sprint 6 (5 days): `packages/@sinkra/research-memory` com SQLite + sentence-transformers embeddings (mode local-first)
- Sprint 7 (3 days): Hybrid BM25 + vector via Whoosh + faiss
- Sprint 8 (2 days): Cross-encoder rerank (ms-marco-MiniLM-L-6-v2)
- **Score impact:** Private KB 36 → 75 (+39pts), total +2.3pts

### Evidence Fidelity (weight 10) — **2 targets**

archive.org snapshot + retraction check. Pequenos gaps mas alto peso.

**Estratégia:**
- Sprint 9 (2 days): Integration com archive.org API + Wayback CDX
- Sprint 10 (1 day): Crossref retraction watch + retracted-papers cache
- **Score impact:** Evidence 69 → 82 (+13pts), total +1.3pts

### UX Operator Control (weight 9) — **2 targets**

Rollback + cost meter live são features de polish que ajudam steerability.

**Estratégia:**
- Sprint 11 (3 days): Rollback API em apps/research /api/research/runs/[runId]/rollback
- Sprint 12 (2 days): SSE-based live cost meter component em UI
- **Score impact:** UX 60 → 75 (+15pts), total +1.35pts

### Scientific Pipeline (weight 3) — **5 targets**

Hypothesis/protocol/statistical/paper-format. Specialty — gancho para academic users.

**Estratégia:**
- Sprint 13 (5 days): Add `--scientific-mode` flag triggering hypothesis-driven phase YAMLs
- Sprint 14 (3 days): scipy.stats integration for confidence intervals
- Sprint 15 (3 days): LaTeX output template (ADAPT from autoresearchclaw)
- **Score impact:** Scientific 40 → 75 (+35pts), total +1.05pts

### Evaluation Value (weight 4) — **1 target**

Public bench score em DeepResearch Bench / BrowseComp-Plus.

**Estratégia:**
- Sprint 16 (3 days): Submit AIOX run to public leaderboard + persist eval logs
- **Score impact:** Evaluation 49 → 70 (+21pts), total +0.84pts

## Total Expected Improvement

| Wave | Sprints | Effort (days) | Pts gained | New AIOX score |
|---:|:---:|---:|---:|---:|
| W1 (Tool Runtime) | S1-S3 | 11 | +5.2 | 67.8 (target rank #1) |
| W2 (Multi-Agent) | S4-S5 | 8 | +2.4 | 70.2 |
| W3 (Private KB) | S6-S8 | 10 | +2.3 | 72.5 |
| W4 (Evidence + UX) | S9-S12 | 8 | +2.65 | 75.2 |
| W5 (Scientific + Eval) | S13-S16 | 14 | +1.89 | 77.0 |
| **Total** | **16 sprints** | **51 days** | **+14.44** | **77.0** (vs Local DR 67.7) |

**Resultado esperado: AIOX 77.0 (#1 com lead de ~10pts sobre Local Deep Research 67.7).**

## Anti-Patterns (don't absorb these)

❌ **Training Methodology** — peso 0 (founder out-of-focus 2026-05-18)
❌ **Jina node-DR code** — proprietary license, NO-GO copy
❌ **`tongyi-deepresearch` Chinese ecosystem** — fit issue
❌ **`agent-browser-workspace` opinionated browser** — too coupled

## Where AIOX Already Wins (defend, don't change)

🟢 **Agentic Planning Control (78.3)** — moat real, NÃO refatorar
🟢 **Research Depth Synthesis (81.1)** — multi-wave bounded + wave compression + synthesis preserves disagreement
🟢 **Architecture Absorption (84.2)** — REUSE-ready Clean architecture
🟢 **Sinkra Fit (100)** — anchor self-ref (peso 0)

## Persona Validation

Recomputed personas with 130-dim matrix show AIOX wins **founder_pm** persona (rank 1, score 68.39) — confirms product discovery vertical positioning. Loses in 7 of 8 personas to **Local Deep Research** (because of Tool Runtime + Private KB gaps).

**Post-absorption projection:** AIOX expected to win **5-6 of 8 personas** after Waves 1-3 complete (Tool Runtime + Multi-Agent + Private KB closed).

## Sources

- 130-dim matrix: `comparison-matrix.json`
- AIOX scoring evidence: `squads/research/` + `.claude/skills/tech-research/` + `apps/research/`
- Competitor scoring evidence: grep counts in `../bench/{player}/` clones
- Personas: `bench-output-dash.json#personas` (recomputed 2026-05-18)
