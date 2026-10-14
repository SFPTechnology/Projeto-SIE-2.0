# Executive Report — Deepresearch Absorption Benchmark

> **TL;DR:** AIOX Research está em **5º de 10** no espaço Deep Research open-source 2026, com score **60.25/100**. Vence em **Governance (100)** e **Planejamento (96.5)**, perde em **Sandbox (0)** e **Distribuição (10)**. Absorption playbook de **62 pts** levaria AIOX para **score 88** em ~20 semanas. Decisão recomendada: **GO em P0 imediato (Sprint 1-4)**.

## Contexto Estratégico

**Mercado:** Open-source deep research explodiu em 2025-2026. 9 players canônicos identificados, 4 com modelos próprios treinados, 4 com sandbox Docker, 2 com MCP nativo. AIOX Research está no mesmo arena mas **com posicionamento diferente** (governance + multi-mode + PT-BR vertical).

**Catalysts 2026:**
- OpenAI Deep Research $200/mo catalisou open-source clones (LDR, Jina, etc)
- RL-trained models (OpenResearcher, DeepResearcher) superam GPT-4.1 em benchmarks
- Privacy-first ganha tração (LDR endorsado por Vitalik Buterin)
- DeerFlow 66k stars em semanas = product-market fit forte
- Bessemer Vertical AI thesis Jan/2026: vertical AI > horizontal SaaS

## Posição AIOX no Landscape (verifiable)

| Rank | Player | Score |
|---:|---|---:|
| 🥇 | DeerFlow (ByteDance) | 72.05 |
| 🥈 | GPT-Researcher | 69.65 |
| 🥈 | AutoResearchClaw | 69.65 |
| 4 | Local Deep Research | 63.90 |
| **5** | **AIOX Research** | **60.25** |
| 6 | Tongyi DeepResearch | 52.10 |
| 7 | LangChain Open DR | 51.70 |
| 8 | DeepResearcher 7B | 50.95 |
| 9 | OpenResearcher 30B | 48.20 |
| 10 | Jina node-DR | 44.50 |

**Posição honesta:** middle tier. Estamos perto da liderança mas com 4 players à frente.

## Diferenciais AIOX (vantagens reais defensáveis)

1. **Governance (100/100)** — único com COVERAGE_GATE + CITATION_GATE + Incremental Learning Log
2. **Planejamento (96.5/100)** — único com product-discovery framework integrado (JTBD/Mom Test/Villain/WTP)
3. **PT-BR/LatAm Vertical** — único com positioning PT-BR + 4 negócios dogfood
4. **Multi-Mode Unified** — 1 squad para tech-research + competitive intel + product discovery + benchmarking + marketing
5. **Tri-Layer Architecture** — squad (brain) + skill (execution) + app (observability) integrados
6. **14 specialist personas** com lineage acadêmico (Booth/Creswell/Sackett/Klein/Gilad/Forsgren)

## Gaps Críticos (problemas reais)

| Gap | Score AIOX | Líder | Δ | Priority |
|---|---:|---|---:|---|
| Sandbox | 0 | AutoResearchClaw (100) | -100 | 🔴 P0 |
| Distribuição | 10 | GPT-Researcher (97) | -87 | 🔴 P0 |
| MCP Server | 0 | LangChain/GPT-Researcher | -100 | 🔴 P0 |
| Modelo trained | 38.75 | OpenResearcher (75) | -36 | 🟠 P1 |
| Memória cross-session | 52.5 | DeerFlow TIAMAT (92.5) | -40 | 🟠 P1 |
| Scholarly DB | 30 | Local DR (100) | -70 | 🟠 P1 |
| Public benchmark | 0 | 4 players com score | -50 | 🟠 P1 |
| Licença OSI | 54 | 8/9 são MIT/Apache | -29 | 🟡 P2 |
| Parallel subagents | 57.5 | DeerFlow (90) | -33 | 🟡 P2 |
| FigureAgent | 0 | AutoResearchClaw | -90 | 🟡 P2 |

## Scenario Performance

AIOX vence 3 de 8 scenarios:

| Scenario | AIOX | Líder | AIOX wins? |
|---|---:|---|:---:|
| S1 Academic Paper | 65.0 | AutoResearchClaw 89.5 | ❌ |
| S2 Product Discovery | **85.5** | — | ✅ **WIN** |
| S3 Privacy/Air-Gapped | 50.0 | LocalDR 86.0 | ❌ |
| S4 Competitive Intelligence | **78.0** | — | ✅ **WIN** |
| S5 Quick Q&A | 45.0 | Jina 78.0 | ❌ |
| S6 Benchmark-Driven | 38.0 | OpenResearcher 88.5 | ❌ |
| S7 PT-BR Vertical | **92.0** | — | ✅ **WIN** |
| S8 Claude Skill Marketplace | 65.0 | GPT-Researcher 86.0 | ❌ |

**Interpretação:** AIOX domina onde Planejamento + Governance + PT-BR pesam (3 wins). Perde onde Distribuição + Modelo + Bench público pesam (4 losses).

## Decisão Estratégica Recomendada

### Strategic Posture: ABSORÇÃO SELETIVA (não competição head-to-head)

AIOX **não deve competir** em todos os fronts. Manter governance + planejamento + PT-BR como DNA, **absorver gaps específicos** dos competidores via REUSE > ADAPT > CREATE.

### Wave 1 (P0 Critical) — GO IMEDIATO (~8 semanas)

| Sprint | Gap | Effort | ROI |
|---|---|---:|---|
| 1 | GAP-03 MCP Server | 5 pts | Composability cross-IDE |
| 2 | GAP-02 PyPI + Docker Hub | 8 pts | Community adoption |
| 3-4 | GAP-01 Docker Sandbox | 13 pts | Academic + FigureAgent unlock |

**Total Wave 1:** 26 pts | Score esperado: 72

### Wave 2 (P1 High) — Quarter following (~8 semanas)

| Sprint | Gap | Effort | ROI |
|---|---|---:|---|
| 5 | GAP-07 Public Benchmark | 3 pts | Marketing leverage |
| 6 | GAP-06 Scholarly DB | 5 pts | CITATION_GATE strength |
| 7 | GAP-04 Model Backend | 5 pts | Cost reduction |
| 8-9 | GAP-05 Cross-Session Memory | 13 pts | Continuous learning |

**Total Wave 2:** 26 pts | Score esperado: 82

### Wave 3 (P2 Polish) — Following quarter (~4 semanas)

| Sprint | Gap | Effort | ROI |
|---|---|---:|---|
| 10 | GAP-10 Dual License | 2 pts | Community contribution |
| 11-12 | GAP-09 FigureAgent | 8 pts | Academic + executive |
| — | GAP-08 Parallel | (DEFERRED) | Reavaliar pós-Wave-2 |

**Total Wave 3:** 10 pts | Score esperado: **88**

## Investimento vs Retorno

| Métrica | Atual | Pós-absorption | Δ |
|---|---:|---:|---:|
| Score weighted | 60.25 | 88 | +27.75 |
| Scenarios won | 3/8 | 5+/8 | +2 |
| Codebase LOC | ~30k | ~35k | +16% |
| Effort total | — | 62 pts | ~20 weeks 1FT |
| Cost (assuming $1k/wk full-stack) | — | ~$20k | — |
| ROI | — | **Posicionamento top-3** | Marketing + adoption gain |

## Riscos Estratégicos

1. **Competidores também absorvem AIOX gaps** — DeerFlow já tem Memory + Sandbox; pode adicionar Governance facilmente
2. **Bench atual é instantâneo** — espaço evolui rápido (DeerFlow 2.0 em fev/2026 mudou ranking)
3. **AGPLv3 community adoption não é automático** — precisa investimento Discord + Twitter + marketing
4. **Apache-2.0 NOTICE compliance** — risk de license violation se descuidoso

## Anti-Patterns Rejeitados

| Anti-pattern | Por quê rejeitar |
|---|---|
| Treinar próprio modelo 30B | Custo prohibitivo (>$200k); OpenResearcher já open Apache-2.0 |
| Replace skill harness com LangGraph | Architectural mismatch; perde Claude Code native fit |
| Copiar código Jina node-DR | Proprietary license |
| Full rewrite TypeScript | KISS — Next.js + Python funciona |
| Substituir governance gates | Esse é o moat — manter intacto |

## Sources de Verdade

- Comparison Matrix: `comparison-matrix.json` (24 dims × 10 players)
- Scorecard: `scorecard.json` (weighted aggregation explicada)
- Gap Analysis: `gap-analysis.json` (10 gaps + 6 inverse gaps)
- Inventories: `inventories/{player}.md` × 9 + `inventory-aiox-research-ecosystem.md`
- Evidence Map: `deep/evidence-strength-map.md` (75% ALTA confidence)
- License Risk: `deep/license-risk-assessment.md`
- Implementation Playbook: `deep/implementation-playbook.md` (3 waves × 12 sprints detailed)

## Recommendation

**GO** com Wave 1 imediato (P0 Critical: Sandbox + Distribution + MCP). Reavaliação após cada wave usando bench re-score.

**Decision authority:** @vision-strategist + @aiox-architect + @aiox-pm (3-way roundtable approval).

**Timeline target:**
- Q3 2026: Wave 1 complete → AIOX v5.1.0 → Score 72
- Q4 2026: Wave 2 complete → AIOX v5.5.0 → Score 82
- Q1 2027: Wave 3 complete → AIOX v6.0.0 → Score 88

**Next action:** approve este bench → spawn ADR-001 (architectural decision record) → criar epic + 12 stories no backlog.
