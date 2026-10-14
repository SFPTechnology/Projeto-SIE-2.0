# Implementation Playbook — Deepresearch Absorption

Playbook executável para realizar a absorption. **3 waves × 12 sprints.**

## Wave 1 — P0 Critical (26 pts, ~6-8 semanas)

### Sprint 1 — GAP-03 MCP Server (5 pts)

**Story:** STORY-DRA-1.1 — MCP server expondo `/tech-research` como tool consumível.

**Implementation:**
1. Criar `packages/@sinkra/research-mcp/`
2. Bootstrap MCP server boilerplate (TypeScript ou Python — TS recomendado pra DX)
3. Expor 3 tools: `tech-research-query`, `tech-research-followup`, `tech-research-status`
4. Map cada tool para invocar `/tech-research` skill via Claude Code agent (bash MCP server orchestration ou direct Python invocation)
5. Add `mcp_server` field em `.claude/skills/tech-research/config.yaml`
6. Test com Claude Desktop / Cursor / Cline

**Sources de ADAPT:**
- `../bench/langchain-open-deep-research/src/` (estrutura MCP-compatible)
- `../bench/gpt-researcher/` (MCP server implementation, search `MCPServer`)

**Acceptance:**
- [ ] MCP server publica 3 tools
- [ ] Claude Desktop conecta e invoca tools
- [ ] Output volta como artifact path em `docs/research/`

### Sprint 2 — GAP-02 Distribution (8 pts)

**Story:** STORY-DRA-1.2 — PyPI package + Docker Hub image.

**Implementation:**
1. Criar `packages/@sinkra/research-cli/`
2. Setuptools `pyproject.toml` com entry point `sinkra-research`
3. Bundle: skill `/tech-research` + schemas + scripts (sem hub clone)
4. CI: GitHub Actions auto-publish em PyPI quando tag `v*`
5. Dockerfile: base python:3.11-slim + skill bundled
6. Docker Hub: `sinkra/research:latest` + `sinkra/research:v0.1.0`
7. NOTICE.txt listing licenses de terceiros (Apache-2.0 attribution)

**Sources de ADAPT:**
- `../bench/gpt-researcher/pyproject.toml` (packaging pattern)
- `../bench/local-deep-research/docker-compose.yml` (Docker pattern)

**Acceptance:**
- [ ] `pip install @sinkra/research-cli` funciona
- [ ] `docker run sinkra/research --query "..."` funciona
- [ ] PyPI badge no README

### Sprint 3-4 — GAP-01 Docker Sandbox (13 pts)

**Story:** STORY-DRA-1.3 — Docker code-execution sandbox in apps/research.

**Implementation:**
1. Adicionar `apps/research/src/lib/sandbox/` com Docker SDK
2. Endpoint `/api/research/runs/[runId]/sandbox/execute` (POST: command + timeout)
3. Container: base ubuntu:22.04 + Python + Node + commonly-used tools
4. Network policy: deny all egress por default; allowlist domains via config
5. Filesystem: read-only base, writable `/tmp` apenas
6. Resource limits: CPU 1 core, memory 2GB, timeout 60s
7. UI: stream output via SSE em apps/research/src/app/research/runs/[runId]
8. Add `tech-research phase-3-sandbox-exec.yaml` opt-in

**Sources de ADAPT:**
- `../bench/AutoResearchClaw/researchclaw/sandbox/` (network-policy-aware pattern)
- `../bench/deer-flow/docker/` (persistent sandbox pattern)

**Acceptance:**
- [ ] Container hardened (egress blocked + read-only FS + resource limits)
- [ ] SSE streaming output funcional
- [ ] Phase YAML invoca sandbox quando query requer code exec
- [ ] Security audit: pass `validate:docker-security`

## Wave 2 — P1 High (26 pts, ~6-8 semanas)

### Sprint 5 — GAP-07 Public Benchmark (3 pts)

**Story:** STORY-DRA-2.1 — Run Deep Research Bench + publish score.

**Implementation:**
1. Clone https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard
2. Run `/tech-research` against bench questions
3. Submit results + create `docs/research/_eval-logs/deep-research-bench/`
4. Add badge in README + apps/research dashboard

**Acceptance:**
- [ ] Score publicado HF Spaces leaderboard
- [ ] Badge visível no README

### Sprint 6 — GAP-06 Scholarly DB (5 pts)

**Story:** STORY-DRA-2.2 — arXiv/PubMed/Semantic Scholar adapters.

**Implementation:**
1. Criar `squads/research/tasks/scholarly-search.md`
2. Adapters em `packages/@sinkra/research-cli/adapters/`:
   - `arxiv.py` — arXiv API client
   - `pubmed.py` — PubMed E-utilities
   - `semantic_scholar.py` — Semantic Scholar API
3. Integrate em `tech-research phase-3-execute-research.yaml` como secondary search
4. CITATION_GATE prefer scholarly sources when available

**Sources de ADAPT:**
- `../bench/local-deep-research/src/local_deep_research/search_engines/`

**Acceptance:**
- [ ] 3 adapters funcionais
- [ ] CITATION_GATE consultive scholarly DB
- [ ] Test query academic gera report com ≥3 scholarly citations

### Sprint 7 — GAP-04 Model Backend (5 pts)

**Story:** STORY-DRA-2.3 — OpenResearcher + DeepResearcher como backend opcional.

**Implementation:**
1. `squads/research/data/model-backends.yaml` — registry de backends
2. Auto-detect GPU em `apps/research /api/research/clis`
3. Quando GPU disponível, oferecer UI switch para backend local
4. Wrap HF transformers + vLLM
5. Fallback graceful para BYOK quando GPU absent

**Acceptance:**
- [ ] Auto-detect GPU
- [ ] Switch UI funcional
- [ ] BYOK fallback testado

### Sprint 8-9 — GAP-05 Cross-Session Memory (13 pts)

**Story:** STORY-DRA-2.4 — TIAMAT-like memory layer com confidence scores.

**Implementation:**
1. `packages/@sinkra/research-memory/`
2. Schema YAML em `squads/research/data/memory-schema.yaml`:
   - facts (claim + sources + confidence + timestamps)
   - entities (people, products, companies)
   - relations (graph)
3. SQLite backend (later: optional Postgres + pgvector)
4. CRUD APIs em apps/research/api
5. Tech-research phase-0 reads memory; phase-5 writes new facts
6. Confidence decay over time

**Sources de ADAPT:**
- `../bench/deer-flow/` — search "TIAMAT" pattern
- `../bench/local-deep-research/src/local_deep_research/utilities/db_*` — SQLCipher

**Acceptance:**
- [ ] Memory persiste cross-session
- [ ] Confidence scores recalculados
- [ ] Phase 0 reads relevant facts
- [ ] Phase 5 writes new facts

## Wave 3 — P2 Polish (18 pts, ~4-6 semanas)

### Sprint 10 — GAP-10 Dual License (2 pts)

**Story:** STORY-DRA-3.1 — Dual license apps/research.

**Implementation:**
1. Fork `apps/research/` → `apps/research-community/`
2. Strip enterprise features (ServiceBus, ClickUp, GWS integrations)
3. AGPLv3 LICENSE
4. README clearly differentiates editions
5. Update marketing pages

**Acceptance:**
- [ ] Community edition published OSI
- [ ] Differentiation clara

### Sprint 11-12 — GAP-09 FigureAgent (8 pts) [blocked by GAP-01]

**Story:** STORY-DRA-3.2 — Visual generation agent for academic/exec output.

**Implementation:**
1. `squads/research/agents/figure-agent.md` (persona)
2. Phase YAML `phase-4-5-visualize.yaml`
3. Uses Docker sandbox (depends GAP-01) to run matplotlib/plotly
4. Output: PNG/SVG figures
5. Embed in tech-research final report

**Sources de ADAPT:**
- `../bench/AutoResearchClaw/researchclaw/figure_agent.py`

**Acceptance:**
- [ ] Generates accurate figures from data
- [ ] Embedded in MD/PDF output

## Cross-Wave Dependencies

```
GAP-01 (Sandbox) ──┐
                   ├──► GAP-09 (FigureAgent)
                   └──► academic paper scenario

GAP-02 (PyPI/Docker) ──► community adoption + benchmark visibility

GAP-03 (MCP) ──► composability w/ outras Claude sessions

GAP-04 (Model backend) ──┐
                          ├──► air-gapped + cost reduction
GAP-05 (Memory) ──────────┘

GAP-06 (Scholarly DB) ──► academic credibility (+CITATION_GATE strength)

GAP-07 (Benchmark) ──► marketing leverage
```

## Risk Mitigations

| Risk | Mitigation |
|---|---|
| Apache-2.0 NOTICE compliance | Adicionar NOTICE.txt + CI check `validate:license-headers` |
| Docker sandbox segurança | Network policy + read-only FS + resource limits + security audit antes de prod |
| Memory schema evolution | Versioned schema YAML + migration scripts |
| Modelos HF download size | Lazy download + cache em volume |
| MCP server stability | Mock tests + integration tests + CI |

## Success Metrics (post-absorption)

- [ ] Score 88 no recompute (vs 60.25 baseline)
- [ ] AIOX vence em 5/8 scenarios (vs 3/8 baseline)
- [ ] DeepResearchBench score público
- [ ] PyPI downloads/mês > 100 dentro 60 dias
- [ ] Docker Hub pulls > 50/mês
- [ ] Community PRs aceitas > 5 dentro 90 dias
