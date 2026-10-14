# Architecture Blueprint — AIOX Research v6.0 (post-absorption)

## Current State (v5.0.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                      AIOX Research                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────┐│
│  │  Squad/research  │──►│ Skill/tech-      │──►│ apps/research││
│  │  (Cognitive Brain)│  │ research v2.0.0  │   │  (Observatory)││
│  │                  │   │                  │   │              ││
│  │ 14 agents        │   │ 7 molecules      │   │ Next.js 16   ││
│  │ 6 workflows      │   │ 17 atoms         │   │ Elastic v2   ││
│  │ 129 .md files    │   │ 13 phase YAMLs   │   │              ││
│  │                  │   │                  │   │ /observatory ││
│  │ research-chief   │   │ COVERAGE_GATE    │   │ /research    ││
│  │ +13 specialists  │   │ CITATION_GATE    │   │ /api/research││
│  │ (Booth, Creswell │   │ Incremental log  │   │              ││
│  │  Sackett, Klein, │   │                  │   │              ││
│  │  Gilad, Forsgren)│   │                  │   │              ││
│  └──────────────────┘   └──────────────────┘   └──────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Target State (v6.0.0 post-absorption)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    AIOX Research Hybrid v6.0.0                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐   ┌──────────────────────┐   ┌──────────────────┐  │
│  │  Squad/research  │──►│  Skill/tech-research │──►│ apps/research-pro │  │
│  │  (UNCHANGED)     │   │  v3.0.0              │   │  + community CE   │  │
│  │                  │   │  + sandbox phase     │   │  (Elastic v2 +    │  │
│  │ 14 agents        │   │  + scholarly phase   │   │   AGPLv3)         │  │
│  │ + FigureAgent    │   │  + memory read/write │   │                   │  │
│  │                  │   │  + model backend opt │   │ + sandbox SSE     │  │
│  │ Multi-mode:      │   │                      │   │ + benchmark dash  │  │
│  │ - tech-research  │   │                      │   │ + figure renderer │  │
│  │ - product-disc   │   │                      │   │                   │  │
│  │ - competitive    │   │                      │   │                   │  │
│  │ - benchmarking   │   │                      │   │                   │  │
│  │ - marketing      │   │                      │   │                   │  │
│  │ - /quick-answer  │   │                      │   │                   │  │
│  └──────────────────┘   └──────────────────────┘   └──────────────────┘  │
│           │                       │                         │              │
│           │                       │                         │              │
│           └───────────────────────┼─────────────────────────┘              │
│                                   │                                        │
│  ┌────────────────────────────────▼────────────────────────────────────┐ │
│  │                 NEW PACKAGES (Wave 1-2 absorption)                  │ │
│  ├──────────────────────────────────────────────────────────────────────┤ │
│  │                                                                      │ │
│  │  @sinkra/research-cli      @sinkra/research-mcp                     │ │
│  │  (PyPI + Docker Hub)       (MCP Server)                             │ │
│  │  - Standalone CLI          - Tools: tech_research_query,            │ │
│  │  - No hub dependency         tech_research_followup,                │ │
│  │  - 5 scholarly adapters      tech_research_status                   │ │
│  │  - 3 model backends opt    - Apache-2.0                             │ │
│  │                                                                      │ │
│  │  @sinkra/research-memory   @sinkra/research-adapters                │ │
│  │  (Cross-session memory)    (Scholarly + Web search engines)         │ │
│  │  - SQLite/Postgres+pgvec   - arXiv, PubMed, Semantic Scholar        │ │
│  │  - Confidence scores       - SearXNG, DuckDuckGo, Tavily            │ │
│  │  - TIAMAT-inspired         - Adapter pattern                         │ │
│  │                                                                      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │              EXTERNAL BACKENDS (Wave 2 optional)                     │ │
│  ├──────────────────────────────────────────────────────────────────────┤ │
│  │                                                                      │ │
│  │  OpenResearcher-30B (HF, Apache-2.0)                                │ │
│  │  DeepResearcher-7B (HF, Apache-2.0)                                 │ │
│  │  Tongyi-DeepResearch-30B (HF, Apache-2.0)                           │ │
│  │  BYOK: Claude, GPT, Gemini, Ollama (current)                        │ │
│  │                                                                      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Decomposition (v6.0.0)

### Layer 1 — Cognitive Brain (Squad)
- **Owner:** research-chief
- **Specialists:** 14 + FigureAgent (new)
- **Workflows:** 6 + tech-research/* + bench-comparison
- **License:** SINKRA project

### Layer 2 — Execution Pipeline (Skill)
- **Owner:** tech-research v3.0.0
- **Phases:** 13 existing + sandbox-exec + scholarly-search + memory-rw + visualize
- **Gates:** COVERAGE_GATE + CITATION_GATE (unchanged)
- **License:** SINKRA project

### Layer 3 — Observability + Execution (App)
- **Owner:** apps/research-pro + apps/research-community
- **Routes:** existing + sandbox API + benchmark dashboard
- **Streaming:** SSE existing + sandbox execution stream
- **License:** Dual (Elastic v2 + AGPLv3)

### Layer 4 — Distribution & Integration (NEW Packages)
- **@sinkra/research-cli** — PyPI + Docker Hub standalone
- **@sinkra/research-mcp** — MCP server (stdio + HTTP/SSE)
- **@sinkra/research-memory** — Cross-session memory layer
- **@sinkra/research-adapters** — Scholarly + web search engines

### Layer 5 — Model Backend (External Optional)
- BYOK: Claude/GPT/Gemini/Ollama (default)
- HF: OpenResearcher-30B / DeepResearcher-7B / Tongyi-30B (opt-in com GPU)

## Data Flow (v6.0.0)

```
User query
    │
    ▼
[MCP Client] / [CLI] / [Web UI] / [Bash skill invocation]
    │
    ▼
@sinkra/research-cli OR /tech-research skill
    │
    ├──► @sinkra/research-memory.read(query) → relevant facts pre-loaded
    │
    ▼
Phase 0: auto-clarify (or Phase 0-Q for /quick-answer)
    │
    ▼
Phase 1: clarify (interactive)
    │
    ▼
Phase 1.5: decompose (NEW: scholarly-aware sub-queries)
    │
    ▼
Phase 2: generate-prompt
    │
    ▼
Phase 3: execute-research (multi-wave bounded)
    │   ├── @sinkra/research-adapters.search(arxiv/pubmed/web)
    │   ├── Phase 3-sandbox-exec (when query requires code) — NEW
    │   └── COVERAGE_GATE check
    │
    ▼
Phase 4: synthesize
    │
    ▼
Phase 4.5: verify-citations → CITATION_GATE
    │
    ▼
Phase 4.5b: visualize (NEW — uses sandbox) → figures
    │
    ▼
Phase 5: document
    │
    ├──► @sinkra/research-memory.write(new_facts, confidence)
    │
    ▼
Final output: docs/research/{date}-{slug}/02-research-report.md + figures
```

## Quality Gates (UNCHANGED — moat AIOX)

- **COVERAGE_GATE:** halt if coverage < 50% after 3 waves
- **CITATION_GATE:** halt if verified_ratio < 0.85 after 2 fix attempts
- **Incremental Learning Log:** write per-phase em `.aiox/learning/logs/tech-research/`
- **Guardrails:** veto on code-writing intent, etc.

## Reusability Map

| Component | Reusable across modes? |
|---|---|
| Cognitive Brain (squad) | ✅ Yes — all 5+ modes |
| tech-research skill | ✅ Yes — base for all modes |
| @sinkra/research-memory | ✅ Yes — cross-mode |
| @sinkra/research-adapters | ✅ Yes — used by ANY skill |
| MCP server | ✅ Yes — exposes core to any consumer |
| App routes | ✅ Yes — all modes browse-able |
| Model backends | ✅ Yes — per-mode override |

## Migration Path

- v5.0.0 → v5.1.0: + Sandbox + MCP + Distribution (Wave 1, ~8 weeks)
- v5.1.0 → v5.5.0: + Memory + Scholarly + Model backends + Benchmark (Wave 2, ~8 weeks)
- v5.5.0 → v6.0.0: + FigureAgent + Dual License (Wave 3, ~4 weeks)

**Total absorption time:** ~20 weeks (5 sprints × 4 weeks each), assuming 1 dev FT or 2 part-time.

## Risks

| Risk | Probability | Mitigation |
|---|---|---|
| MCP spec evolution breaks API | LOW | Pin spec version; auto-test against latest |
| Docker sandbox security CVE | MEDIUM | Quarterly security audit + minimal image |
| HF model availability | LOW | Fallback to BYOK always functional |
| Memory schema regression | MEDIUM | Versioned schema + migration tests |
| Apache-2.0 NOTICE oversight | LOW | CI guard `validate:license-headers` |
| Community AGPLv3 adoption fails | MEDIUM | Marketing + early advocates + Discord |

## Success Indicators

- AIOX score: 60.25 → 88 ✅
- AIOX scenarios won: 3 → 5+ ✅
- Public benchmark score visible ✅
- 100+ PyPI downloads/mês dentro 60 dias
- 50+ Docker Hub pulls/mês
- 5+ community PRs aceitas dentro 90 dias
