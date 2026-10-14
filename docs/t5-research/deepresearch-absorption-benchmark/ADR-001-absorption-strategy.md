# ADR-001 — Deepresearch Absorption Strategy

**Status:** Proposed
**Date:** 2026-05-18
**Deciders:** @vision-strategist, @aiox-architect, @aiox-pm
**Consulted:** @aiox-qa, @aiox-devops, @research-chief

## Context

AIOX Research (squad/research + skill/tech-research + apps/research) ocupa posição única no espaço deep-research 2026 com **Governance gates reais + Multi-mode unified + PT-BR vertical**. Comparação rigorosa com 9 players open-source (DeerFlow, GPT-Researcher, LangChain ODR, Local DR, OpenResearcher, DeepResearcher, Jina node-DR, AutoResearchClaw, Tongyi) revela:

- **Score atual:** 60.25/100 (5º de 10)
- **AIOX vence:** Governance (100), Planejamento (96.5), PT-BR vertical
- **AIOX perde:** Sandbox (0), Distribuição (10), MCP (0), Modelo trained, Memória

Pesquisa-fonte: `docs/research/2026-05-16-quais-os-melhores-projetos-de-deepresearch-opensource-atuais/02-research-report.md` (302 linhas, 13 players analisados, confidence ALTA).

Bench completo em: `docs/bench/deepresearch-absorption-benchmark/`

## Decision

**ABSORPTION SELETIVA via REUSE > ADAPT > CREATE**, em 3 waves × 12 sprints × ~20 semanas:

### Wave 1 — P0 Critical (Q3 2026)
1. **GAP-03 MCP Server** (5 pts) — `packages/@sinkra/research-mcp` ABSORB from LangChain ODR (MIT) + GPT-Researcher (Apache-2.0)
2. **GAP-02 PyPI + Docker Hub** (8 pts) — `packages/@sinkra/research-cli` + Docker image. ADAPT from GPT-Researcher pattern.
3. **GAP-01 Docker Sandbox** (13 pts) — `apps/research /api/research/sandbox` ABSORB from AutoResearchClaw (MIT) + DeerFlow patterns.

### Wave 2 — P1 High (Q4 2026)
4. **GAP-07 Public Benchmark** (3 pts) — run Deep Research Bench, publish em HF Spaces.
5. **GAP-06 Scholarly DB** (5 pts) — `packages/@sinkra/research-adapters` ABSORB from Local DR.
6. **GAP-04 Model Backend** (5 pts) — opcional OpenResearcher/DeepResearcher/Tongyi via HF.
7. **GAP-05 Cross-Session Memory** (13 pts) — `packages/@sinkra/research-memory` ADAPT from DeerFlow TIAMAT.

### Wave 3 — P2 Polish (Q1 2027)
8. **GAP-10 Dual License** (2 pts) — `apps/research-community` em AGPLv3.
9. **GAP-09 FigureAgent** (8 pts) — ABSORB AutoResearchClaw concept (depends GAP-01).
10. **GAP-08 Parallel Subagents** — DEFERRED. Reavaliar pós-Wave-2.

**Total:** 62 pts. **Expected score post-absorption:** 88 (vs 60.25 baseline).

## Consequences

### Positive
- AIOX score: 60.25 → 88 (+27.75 pts)
- Scenarios won: 3/8 → 5+/8
- Public benchmark score visible
- Community adoption via PyPI + Docker Hub + MCP
- Composability cross-IDE (Claude Desktop, Cursor, Cline)
- Cost reduction via local model backend opcional
- Continuous learning via cross-session memory

### Negative
- Codebase expansion ~16% (~5k LOC)
- Apache-2.0 NOTICE compliance burden em packages
- Docker security audit ongoing
- AGPLv3 community adoption não é automático — precisa investimento Discord/Twitter
- 20 weeks de implementation (5 meses w/ 1 dev FT, ou 3 meses w/ 2 devs)

### Neutral
- Governance gates (COVERAGE/CITATION) **mantidos intactos** — são o moat
- Multi-mode unified **mantido**
- PT-BR vertical **mantido**
- Tri-layer architecture **mantida**

## Alternatives Considered

### Alt 1: Treinar próprio modelo 30B
**Rejected.** Custo prohibitivo (>$200k GPU + training). OpenResearcher já open Apache-2.0.

### Alt 2: Full rewrite em LangGraph
**Rejected.** Architectural mismatch. Perde Claude Code native fit.

### Alt 3: Comprar/licenciar Hebbia ou Klue
**Rejected.** $50K+/yr cada. Sem fit PT-BR. Sem control de roadmap.

### Alt 4: Continue sem absorber
**Rejected.** Score estagna em 60.25. Competidores avançam (DeerFlow 2.0 já lançado). Risk de obsolescência em 12 meses.

### Alt 5: Absorption mais ambiciosa (todos os 10 gaps em 1 quarter)
**Rejected.** Concurrent sprints = quality risk. Wave approach permite re-scoring entre waves.

## Compliance Considerations

- **Licenças absorvíveis:** MIT (4 players) + Apache-2.0 (4 players). REUSE friendly.
- **NÃO absorvível:** Jina node-DR (proprietary "All rights reserved").
- **NOTICE.txt obrigatório** em todos packages com código Apache-2.0 absorbed.
- **CI guard:** `validate:license-headers` em packages/@sinkra/research-*

## Quality Gates (mantidos)

- **COVERAGE_GATE:** halt if coverage < 50% após 3 waves (não muda)
- **CITATION_GATE:** halt if verified_ratio < 0.85 após 2 fix attempts (não muda)
- **Incremental Learning Log:** per-phase write em `.aiox/learning/logs/tech-research/` (não muda)

## Implementation Plan

Ver `deep/implementation-playbook.md` (12 sprints detailed).

## Acceptance Criteria

- [ ] Wave 1 complete: AIOX v5.1.0 → score ≥ 70
- [ ] Wave 2 complete: AIOX v5.5.0 → score ≥ 80, scenarios won ≥ 5
- [ ] Wave 3 complete: AIOX v6.0.0 → score ≥ 85
- [ ] No regression em COVERAGE_GATE / CITATION_GATE / multi-mode
- [ ] PyPI downloads/mês > 100 dentro 60 dias post-launch
- [ ] Docker Hub pulls > 50/mês
- [ ] Community PRs aceitas > 5 dentro 90 dias

## References

- Benchmark folder: `docs/bench/deepresearch-absorption-benchmark/`
- Research source: `docs/research/2026-05-16-quais-os-melhores-projetos-de-deepresearch-opensource-atuais/`
- Market validation: `docs/research/2026-05-16-validar-aiox-market-research-panel/`
- IDS Principles rule: `.claude/rules/ids-principles.md`
- KISS rule: `.claude/rules/kiss-no-overengineering.md`
- Sinkra Constitution: `.aiox-core/constitution.md`

## Sign-off

| Role | Status | Date |
|---|---|---|
| @vision-strategist | Pending | — |
| @aiox-architect | Pending | — |
| @aiox-pm | Pending | — |

**ADR moves to `Accepted` after 3/3 sign-offs.**
