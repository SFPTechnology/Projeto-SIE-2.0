# Absorption Decision Table

Cada gap com decisão GO / NO-GO / DEFER + rationale + estimativas.

## Decisões P0 (Wave 1)

| Gap | Decision | Rationale | Effort | Owner |
|---|---|---|---|---|
| GAP-01 Docker Sandbox | **GO** | Desbloqueia academic paper scenario + FigureAgent (GAP-09). MIT license clear. | 13 pts | @cto-architect + @aiox-dev |
| GAP-02 PyPI + Docker Hub Distribution | **GO** | Adoção community + posicionamento marketplace. Apache-2.0 reference. | 8 pts | @devops + @aiox-dev |
| GAP-03 MCP Server | **GO** | Composability cross-IDE + cross-agent. Quick win 5pts. | 5 pts | @aiox-architect + @aiox-dev |

## Decisões P1 (Wave 2)

| Gap | Decision | Rationale | Effort | Owner |
|---|---|---|---|---|
| GAP-04 Model Backend | **GO** | Cost reduction + air-gapped. Sem migration risk (opcional). | 5 pts | @cto-architect |
| GAP-05 Cross-Session Memory | **GO** | Continuous learning é dobra de qualidade. | 13 pts | @aiox-architect |
| GAP-06 Scholarly DB | **GO** | Quick win 5pts + academic paper +20pts. | 5 pts | @aiox-dev |
| GAP-07 Public Benchmark Score | **GO** | Quick win 3pts + marketing massive. | 3 pts | @aiox-qa |

## Decisões P2 (Wave 3)

| Gap | Decision | Rationale | Effort | Owner |
|---|---|---|---|---|
| GAP-08 Parallel Subagents | **DEFER** | Inline é mais econômico. Adicionar opt-in `--parallel` quando demand provar. | 8 pts | — |
| GAP-09 FigureAgent | **GO** (after GAP-01) | Academic paper + executive reports. Blocked by sandbox. | 8 pts | @aiox-dev |
| GAP-10 Dual License | **GO** | Community adoption + 2pts trivial. | 2 pts | @devops |

## Anti-Patterns Rejeitados

| Anti-Pattern | Rationale |
|---|---|
| Copiar código Jina node-DR | Proprietary license — FORBIDDEN |
| Treinar próprio modelo 30B | ROI negativo. OpenResearcher/DeepResearcher já open + boa qualidade. Adotar como backend. |
| Reescrever app em Astro/Vite | KISS — Next.js 16 funciona bem. Sem ganho. |
| Full Python rewrite do squad | KISS — MD files funcionam bem com Claude Code. Sem ganho. |
| Substituir COVERAGE/CITATION gates | São o moat AIOX. Manter intactos. |

## Composition Matrix

| Component | Source | License | Status |
|---|---|---|---|
| Governance gates | AIOX original | Custom (kept) | KEEP |
| Multi-mode squad | AIOX original | Elastic v2 | KEEP |
| Product Discovery | AIOX original | — | KEEP |
| 14 specialist personas | AIOX original | — | KEEP |
| PT-BR vertical | AIOX original | — | KEEP |
| Docker sandbox pattern | AutoResearchClaw | MIT | ABSORB |
| PyPI distribution pattern | GPT-Researcher | Apache-2.0 | ABSORB |
| MCP server pattern | LangChain ODR | MIT | ABSORB |
| Model backend optional | OpenResearcher / DeepResearcher | Apache-2.0 | ABSORB (backend) |
| Cross-session memory | DeerFlow TIAMAT | MIT | ABSORB |
| Scholarly DB adapters | Local DR | MIT | ABSORB |
| Public eval logs | OpenResearcher pattern | Apache-2.0 | ABSORB (pattern) |
| FigureAgent | AutoResearchClaw concept | MIT | ABSORB (concept) |
| AGPLv3 community edition | Sentry/MongoDB precedent | AGPLv3 | NEW DUAL-LICENSE |

## Decision Summary

- **GO:** 9 gaps (87% of total)
- **DEFER:** 1 gap (GAP-08 Parallel)
- **NO-GO:** 0 gaps

**Total effort GO:** 62 pts
**Expected score after GO:** 88 (from 60.25 baseline = +27.75)
