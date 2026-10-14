# Open-Source → Sinkra Map

> Mapeamento componente-a-componente: do que cada player open-source nasce, onde aterrissa no Sinkra Hub.

## Map Geral

| Source Player | Source Component | Sinkra Target | Action | Wave |
|---|---|---|---|---|
| AutoResearchClaw | `researchclaw/sandbox/` Docker network-policy-aware | `apps/research/src/lib/sandbox/` | ABSORB (MIT) | W1 |
| AutoResearchClaw | `researchclaw/figure_agent.py` | `squads/research/agents/figure-agent.md` | ABSORB concept | W3 |
| AutoResearchClaw | `prompts.default.yaml` (versioned prompts) | `squads/research/data/prompts-versioned.yaml` | ABSORB pattern | W2 |
| AutoResearchClaw | 6 HITL modes granular | `squads/research/data/hitl-modes.yaml` | ABSORB | W2 |
| DeerFlow | `backend/memory/TIAMAT-like` | `packages/@sinkra/research-memory/` | ABSORB pattern (MIT) | W2 |
| DeerFlow | `skills/` progressive loading | `squads/research/data/skill-loader.yaml` | ABSORB pattern | W2 |
| DeerFlow | Docker persistent sandbox | combinar com AutoResearchClaw para apps/research | ABSORB pattern | W1 |
| DeerFlow | `frontend/` integrated UI | Já temos `apps/research/` — apenas inspirar UX | INSPIRE | — |
| GPT-Researcher | `mcp_server.py` MCP integration | `packages/@sinkra/research-mcp/` | ABSORB (Apache-2.0 + NOTICE) | W1 |
| GPT-Researcher | `pyproject.toml` packaging | `packages/@sinkra/research-cli/pyproject.toml` | ABSORB pattern | W1 |
| GPT-Researcher | Multi-output (PDF/DOCX/HTML) | `squads/research/data/output-formats.yaml` | ABSORB pattern | W2 |
| GPT-Researcher | LangSmith integration pattern | Optional: AIOX learning logs → LangSmith export | DEFER | — |
| GPT-Researcher | Discord community channel | (governance question, not code) | — | — |
| LangChain ODR | `src/` 22 py compact design | Lesson: audit AIOX for ornamental complexity | INSPIRE | W2 |
| LangChain ODR | `CLAUDE.md` nativo | Já temos | — | — |
| LangChain ODR | MCP-native pattern | Combinar com GPT-Researcher para `packages/@sinkra/research-mcp/` | ABSORB (MIT) | W1 |
| LangChain ODR | DeepResearchBench score | Roadmap GAP-07: run bench + publish | ABSORB process | W2 |
| LangChain ODR | `langgraph.json` deployment | AIOX usa skill harness — não absorber | — | — |
| Local DR | `search_engines/` 10+ adapters (arxiv/pubmed/semantic-scholar/etc) | `packages/@sinkra/research-cli/adapters/` | ABSORB (MIT) | W2 |
| Local DR | SQLCipher encrypted DB | `apps/research/src/lib/encrypted-storage.ts` | ABSORB pattern | W2 |
| Local DR | OpenSSF Scorecard + CodeQL + Semgrep CI | `.github/workflows/security-scan.yml` | ABSORB pattern | W2 |
| Local DR | Docker GPU/Unraid configs | `infrastructure/docker/research.gpu.dockerfile` | ABSORB pattern | W1 |
| OpenResearcher | Modelo 30B HuggingFace | Backend opcional via `squads/research/data/model-backends.yaml` | ABSORB (Apache-2.0) | W2 |
| OpenResearcher | 3 browser primitives (search/open/find) | Lesson: simplificar tech-research atoms | INSPIRE | — |
| OpenResearcher | Public eval logs HF | `docs/research/_eval-logs/` pattern | ABSORB pattern | W2 |
| OpenResearcher | NVIDIA Nemotron adoption pattern | Marketing/PR strategy, não código | INSPIRE | — |
| DeepResearcher | Modelo 7B Qwen2.5 + GRPO RL | Backend opcional (low-GPU tier) | ABSORB (Apache-2.0) | W2 |
| DeepResearcher | Emergent behaviors documentation | `docs/research/_observability/emergent-behaviors.md` | ADAPT concept | — |
| DeepResearcher | RL training infra | NÃO absorber (treinar próprio modelo = scope creep) | NO-GO | — |
| Jina node-DR | Single-loop pattern (search/visit/reflect/answer) | Lesson: simplificar e adicionar /quick-answer skill | INSPIRE only (proprietary) | — |
| Jina node-DR | Budget monitoring | Adicionar a COVERAGE_GATE | INSPIRE only (proprietary) | W2 |
| Jina node-DR | Scope honesty (README explicit boundaries) | Adotar pattern em todos os skills AIOX | INSPIRE | W2 |
| Jina node-DR | TypeScript implementation | NÃO copiar | NO-GO | — |
| Tongyi | Modelo 30B-A3B HuggingFace | Backend opcional alternativo | ABSORB (Apache-2.0) | W2 |
| Tongyi | WebAgent specialization | `squads/research/agents/web-agent.md` | ADAPT concept | W3 |
| Tongyi | Tech_Report.pdf padrão | `docs/architecture/research-tech-report.md` | ADAPT pattern | W2 |
| Tongyi | Multi top-venue paper strategy | Marketing/PR strategy | INSPIRE | — |

## Mapping Categorias

### Strictly ABSORB (REUSE de código)
- AutoResearchClaw Docker sandbox pattern
- GPT-Researcher MCP server code (Apache-2.0 + NOTICE)
- Local DR scholarly search adapters
- Local DR SQLCipher pattern

### ADAPT (REIMPLEMENT inspirado)
- DeerFlow TIAMAT memory schema
- AutoResearchClaw FigureAgent concept
- LangChain ODR compact design
- Tongyi Tech Report pattern

### INSPIRE only (proprietary ou too-specific)
- Jina node-DR single-loop pattern (proprietary)
- Jina budget monitoring concept (proprietary)
- DeerFlow ByteDance ecosystem integrations (too-specific)

### NO-GO
- Training own 30B/7B model (scope creep, ROI negativo)
- Copy Jina TypeScript code (proprietary)
- Replace Next.js with LangGraph deployment (architectural mismatch)

## Total Absorption Footprint

| Source | Code lines estimated |
|---|---:|
| AutoResearchClaw | ~2,000 (sandbox + figure agent + prompts) |
| GPT-Researcher | ~500 (MCP server code) |
| Local DR | ~1,500 (10 search adapters + SQLCipher wrap) |
| DeerFlow | ~800 (memory schema + skill loader) |
| OpenResearcher / DeepResearcher / Tongyi | ~200 (wrapper code only — modelos em HF) |
| **Total** | **~5,000 LOC** |

vs **Sinkra Hub atual:** ~30,000 LOC entre packages + apps + squads. **Absorption representa ~16% expansion.** Bounded e viável.

## Estratégia de Versioning

- AIOX Research **v5.0.0** atual
- Pós-Wave-1: **v5.1.0** (sandbox + MCP + distribution)
- Pós-Wave-2: **v5.5.0** (memory + scholarly + model backends + bench score)
- Pós-Wave-3: **v6.0.0** (figure agent + dual license + composition target 88)
