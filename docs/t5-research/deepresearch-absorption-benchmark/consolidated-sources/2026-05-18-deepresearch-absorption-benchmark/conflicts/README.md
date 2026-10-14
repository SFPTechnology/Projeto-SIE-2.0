# Deepresearch Absorption Benchmark

> **🔗 Observatory:** http://localhost:3002/observatory/bench?slug=2026-05-18-deepresearch-absorption-benchmark
>
> **TL;DR:** AIOX Research **5º de 10** no espaço deep-research open-source 2026. Score **60.25/100** (DeerFlow lidera com 72.05). Vence em **Governance (100)** e **Planejamento (96.5)**, perde em **Sandbox (0)**, **Distribuição (10)** e **MCP (0)**. Absorption playbook de **62 pts** levaria AIOX para score **88** em **~20 semanas**.
>
> **🥇 Gold Tier** · **78 artefatos** · **102 microdimensões × 10 players = 1,020 cells** · **45 duels granulares** · Observatory-ready

## Quick Facts

| Métrica | Valor |
|---|---|
| Subject A | AIOX Research Ecosystem (squad/research + .claude/skills/tech-research + apps/research) |
| Subject B | 9 open-source players: DeerFlow, GPT-Researcher, LangChain Open DR, Local DR, OpenResearcher, DeepResearcher, Jina node-DR, AutoResearchClaw, Tongyi DR |
| AIOX score | **60.25** (5º de 10) |
| Top player | DeerFlow (72.05) |
| AIOX wins (scenarios) | 3 of 8 (Product Discovery, Competitive Intel, PT-BR Vertical) |
| Critical gaps | 3 P0 (Sandbox, Distribution, MCP) |
| Total absorption effort | 62 pts ≈ 20 weeks |
| Expected score post-absorption | 88 |

## Por que este bench

Pesquisa-fonte: `docs/research/2026-05-16-quais-os-melhores-projetos-de-deepresearch-opensource-atuais/02-research-report.md` mapeou 13 players. Este bench escolhe 9 canônicos, clona em `../bench/`, scoring weighted multi-dimensão, identifica gaps, propõe playbook de absorption.

Mesma estrutura que `docs/bench/slides-creator-open-source-absorption/` — index via [`bench-output-dash.json`](bench-output-dash.json) para `/observatory/bench`.

## Start Here

| Você quer... | Leia... |
|---|---|
| Decisão GO/NO-GO em 5 min | [battle-card.md](battle-card.md) |
| Quick rank | [scorecard.md](scorecard.md) |
| Strategic context | [executive-report.md](executive-report.md) |
| Como AIOX se compara feature-a-feature | [capability-matrix.md](capability-matrix.md) · [comparison-matrix.md](comparison-matrix.md) |
| O que falta no AIOX | [gap-analysis.md](gap-analysis.md) |
| Como implementar | [absorption-roadmap.md](absorption-roadmap.md) · [story-ready-backlog.md](story-ready-backlog.md) |
| Decisão arquitetural formal | [ADR-001-absorption-strategy.md](ADR-001-absorption-strategy.md) |
| Risks | [risk-register.md](risk-register.md) |
| Index completo | [INDEX.md](INDEX.md) |

## Top 3 Findings (honest)

### 1. AIOX vence onde Governance + Planejamento importam
Únicos com COVERAGE_GATE + CITATION_GATE reais. Únicos com product-discovery framework integrado (JTBD + Mom Test + Villain + WTP). Únicos PT-BR vertical com 4 negócios dogfood.

### 2. AIOX perde em distribuição e capabilities tácticas
Sem Docker sandbox (vs AutoResearchClaw 100). Sem PyPI/Docker Hub (vs GPT-Researcher 97). Sem MCP server (vs LangChain/GPT-Researcher). Sem score público em benchmark padronizado.

### 3. Top-3 P0 absorption desbloqueia tudo
- **GAP-01 Sandbox** (13pts) — desbloqueia academic paper scenario + FigureAgent
- **GAP-02 PyPI+Docker** (8pts) — adoção community 10x
- **GAP-03 MCP Server** (5pts) — composability cross-IDE

26 pts em 8 semanas → score 60.25 → 72.

## Quem usou este bench

- @vision-strategist — decisão estratégica
- @aiox-architect — sign-off ADR-001
- @aiox-pm — backlog creation
- @aiox-dev — implementation playbook
- @aiox-qa — quality audit + regression tests

## Compliance

- 75% das claims em **ALTA** confidence (direct file/clone/URL)
- 25% **MEDIA** (README + paper sem reprodução)
- 0% BAIXA (zero claims fabricados)
- Licenças: 4 MIT + 4 Apache-2.0 + 1 Jina proprietary (NO-GO absorption)

## Status

🥇 **Gold Tier (100% compliance)** — 77 artefatos, 18/18 validation checks pass.

Gold compliance:
- ✅ Research OS (4/4): research-profile, scope-contract, curiosity-queue, decomposition
- ✅ Dashboard Contract (11/11): action-plan, claims, decision-ledger, risk-register, decision-rubric, dashboard-manifest, validation-report, players, sources, metrics, pipeline-state
- ✅ Custom Rubric (2/2): evaluation-rubric + decision-rubric com 5 presets (baseline + 4 personas)
- ✅ Actionability (4/4): action-plan formalizado, story-ready-backlog, absorption-roadmap, dependency-graph
- ✅ Observatory contract: bench-output-dash.json compliant com BenchDashboardData schema
- ✅ All YAML Gold artifacts: players, sources, metrics, pipeline-state, dashboard-manifest, validation-report, etc.

Ver [validation-report.yaml](validation-report.yaml) para checks.
Ver [quality-audit.md](quality-audit.md) para auditoria pré-Gold.
Ver [dashboard-manifest.yaml](dashboard-manifest.yaml) para mapa de abas Observatory.

## License

Bench content: same as Sinkra Hub repo (SINKRA project).
Open-source players cited: respect each player's LICENSE (see `deep/license-risk-assessment.md`).
