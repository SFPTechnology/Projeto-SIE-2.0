# Quick Wins — Deepresearch Absorption

> Ações de **baixo custo e alto retorno** identificadas durante o bench. Executáveis em <1 semana.

## QW-01 — Public Benchmark Score (3 pts, 1 week)

**Source:** GAP-07
**Effort:** 3 pts
**Impact:** Marketing leverage massivo + procurement credibility

Rodar `/tech-research` contra Deep Research Bench (HF Spaces) + publicar score. LangChain ODR scored 0.4344 @ #6 com pipeline simples. AIOX deveria atingir similar.

**Steps:**
1. Clone `https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard`
2. Run AIOX `/tech-research` against bench dataset
3. Submit results to leaderboard
4. Add badge to README

**Owner:** @aiox-qa
**Time-to-value:** 1 week

## QW-02 — Dual License Community Edition (2 pts, 1 week)

**Source:** GAP-10
**Effort:** 2 pts
**Impact:** Community contribution unlocked + adoption

Fork `apps/research/` → `apps/research-community/` em AGPLv3, strip enterprise features.

**Steps:**
1. Fork directory
2. Replace LICENSE with AGPLv3
3. Strip ServiceBus/ClickUp/GWS integrations
4. Update README
5. Marketing announcement

**Owner:** @aiox-devops + @legal-chief
**Time-to-value:** 1 week

## QW-03 — Add COVERAGE/CITATION Badges to README (0.5 pts, 1 day)

**Effort:** 0.5 pts
**Impact:** Differentiator visible

Adicionar badges visuais no README de AIOX research mostrando:
- "COVERAGE_GATE: ACTIVE"
- "CITATION_GATE: verified_ratio ≥ 0.85"
- "Incremental Learning Log: per-phase"

Move tacit advantage to visible advantage.

**Owner:** @aiox-pm + @aiox-devops
**Time-to-value:** 1 day

## QW-04 — Publish Battle Card como Blog Post (1 pt, 2 days)

**Effort:** 1 pt
**Impact:** Marketing content + SEO

`battle-card.md` deste bench está deck-ready. Publicar como blog post em alanicolas.com com cross-link para `/observatory/bench?slug=2026-05-18-deepresearch-absorption-benchmark`.

**Owner:** @copy-chief + @aiox-pm
**Time-to-value:** 2 days

## QW-05 — Run Bench Quarterly (Recurring)

**Effort:** ~4h por quarterly run
**Impact:** Trend tracking + competitive intel

Re-rodar este bench a cada quarter. DeerFlow 2.0 lançado fev/2026 já mudou ranking. AIOX precisa monitor.

**Cadence:** Q3 2026, Q4 2026, Q1 2027, Q2 2027
**Owner:** @research-chief + bench-analyst

## QW-06 — Add bench-output-dash.json to All Existing Benches

**Effort:** 2 pts (per bench, 5 benches existing)
**Impact:** Observatory dashboard coverage

`docs/bench/*/` deveria todos ter `bench-output-dash.json` no formato Observatory. Hoje só slides-creator + este deepresearch têm.

**Owner:** @aiox-architect

## Summary

| QW | Effort | Time | Impact |
|---|---|---|---|
| QW-01 Public Benchmark | 3 pts | 1 week | Marketing leverage |
| QW-02 Dual License | 2 pts | 1 week | Community unlocked |
| QW-03 Badges README | 0.5 pts | 1 day | Differentiator visible |
| QW-04 Blog Post | 1 pt | 2 days | SEO + marketing |
| QW-05 Quarterly Bench | ~4h | recurring | Competitive intel |
| QW-06 Dash all benches | 10 pts | 2 weeks | Observatory coverage |
| **Total** | **16.5 pts** | **~3 weeks** | **High leverage** |

Quick wins **paralelizáveis com Wave 1** (não bloqueiam Sandbox/Distribution/MCP).
