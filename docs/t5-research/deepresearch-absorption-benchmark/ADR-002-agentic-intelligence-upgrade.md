# ADR-002 — Agentic Intelligence Upgrade (Squad Research + Skill tech-research)

**Status:** Proposed (sign-off pending) — v2.0 post-Advisory-Council
**Date:** 2026-05-18
**Deciders:** @vision-strategist, @aiox-architect, @aiox-pm, @research-chief
**Consulted:** Advisory Council (Contrarian + First Principles + Expansion + Outsider + Executor) — ✅ COMPLETED 2026-05-18, @aiox-qa, @aiox-devops
**Companion ADR:** [ADR-001 — Deepresearch Absorption Strategy](./ADR-001-absorption-strategy.md)
**Roundtable Report:** [ROUNDTABLE-REPORT-ADR-002-2026-05-18.md](./ROUNDTABLE-REPORT-ADR-002-2026-05-18.md) — Verdict: APPROVE_WITH_CONDITIONS (7,25/10, 6/6 reviewers, 0 conflicts, fast-path)
**Advisory Council Report:** [ADR-002-advisory-council-report.md](./ADR-002-advisory-council-report.md) — Verdict: PROCEED_WITH_CONDITIONS (6,5/10, 5/5 advisors, cognitive diversity) — adiciona Sprint 0 (eval suite) + STORY-RA-EXP.1 (A/B persona vs spawn) + critério git-based + plano B Spike + route-accuracy check. **Total revisado: 35 pts (worst case) ou 24 pts (se Sprint C DEFERRED via EXP.1).**
**Relationship:** Paralelo, não substitui. ADR-001 endereça **infraestrutura/distribuição** (MCP, Sandbox, PyPI, Memory). ADR-002 endereça **inteligência agentica** (heartbeat, autonomia, multi-signal stop, gap loop, specialist spawn). Roda em arquivos diferentes; podem ser executados concorrentemente — com hard gate para Sprint C aguardar ADR-001 Wave 1 iniciar (post-roundtable).

---

## Scope & Roundtable Conditions

### Scope declaration

- **Hub-only.** Todas as mudanças vivem em `squads/research/` e `.claude/skills/tech-research/`. Este ADR está **fora do allowlist de Hub→Spoke sync** durante toda a execução. Spokes (Strata, Soft, AIOX) só recebem após release tagged + compat-check explícito.
- **Companion não-substituto:** não toca em ADR-001 entregáveis (MCP, Sandbox, PyPI, Memory). Toca apenas `squads/research/` + skill core.

### Pre-conditions (BLOCKERS para qualquer Sprint iniciar)

1. ✅ **EPIC pai existente reutilizado** (não criar novo per founder directive 2026-05-18): `docs/stories/epic-research-intelligence/EPIC-RESEARCH-INTELLIGENCE.md` estendido em 2026-05-18 com Wave 6+ stories prefixadas `RA-*`. Per regra `prior-art-search.md`: EPIC-150 (Done) e EPIC-RESEARCH-INTELLIGENCE (Draft) cobrem o escopo; absorption decision = REUSE EPIC-RESEARCH-INTELLIGENCE.
2. **Schema update:** `squads/sinkra-squad/data/process-mapping-rules.yaml` declara campo `status: active | dormant | deprecated` em `agents[]`. Origem: roundtable @aiox-master F01.
3. **Advisory Council Report anexado:** ✅ `ADR-002-advisory-council-report.md` anexado em 2026-05-18 — verdict PROCEED_WITH_CONDITIONS (6,5/10). KISS Gate 2 fechado via Sprint 0 + STORY-RA-EXP.1 (ver abaixo).

### Story executor convention

- **Epic owner:** `@research-chief` (gating/QA, não codifica).
- **Code executor por story:** `@aiox-dev` (ou equivalente) nomeado **explicitamente** em cada `STORY-RA-*.md`. NUNCA implícito. Origem: roundtable @pm F03.

### Re-estimate (3 versões — histórico transparente)

| Item | v0.1 | v1.0 (post-roundtable) | v2.0 (post-Advisory-Council) | Justificativa |
|---|---:|---:|---:|---|
| **Sprint 0 — Eval Suite Skeleton** (NEW v2.0) | — | — | 2 | Council CF-1: indústria 2026 coloca eval engineering como prerequisite. Sem isso, AC-A2 ("cost signal validado") é não-falsificável. Origem: Advisor B (outsider). |
| Sprint A | 5 | 5 | 5 | — |
| Sprint B | 5 | 5 | 5 | — |
| **STORY-RA-EXP.1 — KISS Gate 1 falsificável** (NEW v2.0) | — | — | 2 | Council CF-2: 10 runs A/B persona-inline vs spawn manual. Falsifica Sprint C ANTES do Spike. Se delta < 10% → Sprint C DEFERRED. Origem: Advisor C (contrarian). |
| SPIKE-RA-C.0 | — | 1 | 1 | — |
| Sprint C (condicional ao EXP.1 + SPIKE) | 8 | 11 | 11 (ou **0 se DEFERRED**) | — |
| Sprint D | 3 | 3 | 3 | — |
| Sprint E | 2 | 3 | 3 | — |
| STORY-RA-PRE.1 (schema update) | — | 1 | 1 | — |
| STORY-RA-RESCORE.1 | — | 2 | 2 | — |
| **Total worst case** | **23 pts** | **31 pts** | **35 pts / ~6,5 sem (1 FT)** | — |
| **Total se Sprint C DEFERRED via EXP.1** | n/a | n/a | **24 pts / ~4,5 sem** | EXP.1 produz evidência empírica antes de comprometer C |

### Sequencing ENFORCED (v2.0, post-Advisory-Council)

```
EPIC-RESEARCH-INTELLIGENCE.md (extended 2026-05-18 com Wave 6+)  (precondition)
        │
        ├──► STORY-RA-PRE.1 (schema update process-mapping-rules)
        │
        ├──► Sprint 0 — Eval Suite Skeleton (NEW v2.0, 2 pts, 1-2 dias)
        │      • Instrumentação básica: cost-latency tracker + tool-call counters
        │      • eval-suite/ skeleton com 3 fixtures históricas
        │      • Rubric humana OU LLM-judge stub para regressão de qualidade
        │      • Resolve CF-1 do Advisory Council (eval-first inversion da indústria 2026)
        │
        ├──► Sprint E (3d hard timebox, achados extras → DEFERRED stories)
        │      • marca specialists status: dormant em config.yaml
        │      • prepara 5 agent files com I/O schemas no frontmatter
        │      • registry sync: ecosystem-registry.yaml update
        │      • alias entry: aliases-pending-registry.yaml
        │      • workflow refs: EDIT dos arquivos que citam dr-orchestrator
        │      • tasks/ categorização via sinkra:rename-artifact (dry-run obrigatório)
        │      • [TIMEBOX HARD] E.2 (deprecação dr-orchestrator) em 4h
        │        — achados fora dos 8 arquivos previstos → DEFERRED stories
        │
        ├──► Sprint A (paralelo a Sprint 0 + E, depende de Sprint 0 entregue)
        │      • heartbeat-policy.yaml + multi-signal (7 stop + 3 replan)
        │      • cost_confidence: exact | approximate | unavailable
        │      • Sprint 0 já forneceu cost-latency tracker — A consome
        │
        ├──► [HARD GATE — critério git-based v2.0]:
        │      ADR-001 Wave 1 tem ≥ 1 story com:
        │        • status: InProgress em docs/stories/ epic-ADR-001-*/ , OR
        │        • commit em branch feat/ADR-001-* nos últimos 3 dias úteis
        │      Quem decide: @research-chief via `gh pr list` / `git log`
        │      Resolve CP-3 do Advisory Council (gating subvertível eliminado)
        │
        ├──► Sprint B (após A entregue)
        │      • gap_detector.py com semântica APPEND-ONLY por wave declarada no spec
        │      • pipeline-state.yaml referencia gaps por ID (recovery determinístico)
        │
        ├──► STORY-RA-EXP.1 — KISS Gate 1 falsificável (NEW v2.0, 2 pts, 1 dia)
        │      • 10 runs de /tech-research em fixtures históricas
        │        — 5 com inline persona-fidelity (status quo)
        │        — 5 com spawn manual ad-hoc via Task tool
        │      • LLM-judge rubric mede delta de qualidade de output
        │      • PASS: delta ≥ 10% → Sprint C procede
        │      • FAIL: delta < 10% → Sprint C DEFERRED, total = 24 pts
        │      • Resolve CF-2 + KISS Gate 1 (Advisor C + D)
        │
        ├──► SPIKE-RA-C.0 (1d, após EXP.1 PASS)
        │      • prototipar 1 specialist spawn paralelo via Task tool em phase YAML isolada
        │      • output: SPIKE-REPORT-RA-C-0.md com verdict pass/fail/reformulate
        │      • [PLANO B v2.0] Se vermelho:
        │          — Sprint C declarado DEFERRED
        │          — ADR-003 abrirá com nova estimativa pós-mudança no executor
        │          — Sprints 0+A+B+D+E entregam valor autônomo (re-score esperado +6 pts)
        │
        ├──► Sprint C (depende de: EXP.1 PASS ∧ SPIKE verde ∧ Sprint E entregue ∧ Hard Gate)
        │      • specialist-contracts.yaml com available_tools[] (forward-compat)
        │      • dispatcher.py + failure isolation
        │      • execution-log.jsonl com timestamps sobrepostos
        │
        ├──► Sprint D (após C — usa Sackett do Sprint C)
        │      • claims.yaml com rewritten: true + original_claim no schema
        │      • per-claim retry com archive.org fallback
        │
        └──► STORY-RA-RESCORE.1
               • rodar /research-bench profile=gold_absorption em AIOX v5.X
               • atualizar players[].scores.aiox_research no decision-rubric.yaml
               • [AC epic-level v2.0] route-accuracy check:
                   3 fixtures com triggers explícitos dos 5 specialists.
                   Se nenhum invoca quando deveria → bug de routing, NÃO cleanup.
                   Resolve CF-3 do Advisory Council (specialists dormentes preservados)
```

**Hard constraints v2.0:**
- Sprint A **NÃO inicia** antes de Sprint 0 entregue (eval-first)
- Sprint C **NÃO inicia** antes de `(EXP.1 PASS) ∧ (SPIKE verde) ∧ (Sprint E entregue) ∧ (Hard Gate git-based)`
- Se EXP.1 FAIL → Sprint C DEFERRED automaticamente; demais sprints procedem; total = 24 pts
- Se SPIKE vermelho → Sprint C DEFERRED; ADR-003 abre; total = 24 pts

---

## Context

ADR-001 fechou a estratégia de absorção arquitetural (62 pts, 20 semanas, score 60.25 → 88). Restou uma dimensão não endereçada: **a qualidade agentica do loop de pesquisa em si**. A análise comparativa dos 18 repos decoded em `outputs/decoded/` e dos 12 docs deep do bench revelou que o squad research é **forte em papel e fraco em execução autônoma**:

| Eixo | Score AIOX | Líder | Δ | Diagnóstico |
|---|---:|---:|---:|---|
| Governance | **100** | nós | +35 | Moat único. Preservar. |
| Planejamento (declarado) | **96,5** | nós | +16 | Forte no papel — phase decompose explícita. |
| Multi-Agente (real) | 57,5 | DeerFlow 90 | **-32,5** | 14 agents declarados, 6-7 nunca invocados. Inline persona-fidelity em vez de spawn real. |
| Execução agentica | 82,7 | DeerFlow 83,3 | -0,7 | Empate técnico, mas single-signal stop (só `coverage >= 70`). |
| Self-criticism estruturado | médio | DeepResearcher emergent | — | Phase 4.5 existe mas é binária (veto/aprova), não adaptativa. |

### Sinais empíricos coletados

**Do bench (`docs/bench/deepresearch-absorption-benchmark/`):**
- `deep/agentic-planning-reflection.md` classifica 4 patterns agenticos no mercado. AIOX implementa só o **Pattern 2 (multi-pass + audit)**. P1 (single-pass loop), P3 (lead + specialists paralelo) e P4 (RL emergent) estão ausentes ou puramente declarativos.
- `deep/proposed-technical-expansion-plan.md` lista 15 microdims em **Agentic Planning Control** (apc_*) onde a maioria dos players empata ou perde — espaço aberto para diferenciação.
- `gap-analysis.md` (root) marca como crítico: "Nenhum player entrega integralmente trace.jsonl, tool-calls.jsonl, sources.yaml, claims.yaml, cost-latency.yaml e replay-manifest.yaml".

**Dos 18 repos decoded:**
- **deer-flow**: LangGraph checkpoint + SSE bridge + middleware chain — padrão de heartbeat mais maduro observado (`backend/packages/harness/deerflow/runtime/runs/worker.py`).
- **node-deepresearch (Jina)**: Token-budgeted state machine com gaps[] persistido e ReflectAction estruturada (`src/agent.ts:48-100`, `ReflectAction`). **Inspirar arquitetura — código proprietário, NÃO absorver.**
- **gpt-researcher**: Nested instances + follow-up generation (`gpt_researcher/skills/deep_research.py`).
- **alibaba-deepresearch**: Multi-signal stop (`MAX_LLM_CALL` + token>110k + 150min timeout) em `inference/react_agent.py:136-150`.
- **deep-research-bench**: FACT validator com Jina Reader scraping + classification `supported|unsupported|unknown` por claim (`utils/scrape.py`, `utils/validate.py`).

**Do squad audit (`squads/research/`):**
- 14 agents declarados; Sackett, Klein, Creswell, Forsgren, Gilad, Booth **nunca invocados** em pipeline. Cérebros sem corpo.
- `dr-orchestrator` e `research-chief` competem por ownership sem manifest explícito.
- COVERAGE_GATE hoje é **single-signal** (`coverage_score`); sem cost, sem wallclock, sem gap convergence.
- CITATION_GATE faz 2 fix-attempts, mas é **veto binário** — não re-rotula claim com `confidence: low + unsupported` no relatório final.
- Queries da Wave 2+ re-decompõem brief inteiro em vez de **mirar gaps específicos**.

### Por que agora

ADR-001 entrega infra/distribuição (Wave 1-3, 20 semanas). Sem ADR-002, esses entregáveis amplificam capacidade **bruta** (mais entradas via MCP, mais execução via sandbox, mais memória) sem melhorar a **qualidade do raciocínio do loop**. Resultado seria escalar um pipeline subótimo. ADR-002 corrige o pipeline antes que ele seja escalado.

---

## Decision

**5 Sprints (A-E) de upgrade agentico, em paralelo aos Waves do ADR-001**, totalizando ~23 pts em ~5 semanas (1 dev FT) ou ~3 semanas (2 devs FT).

Princípio condutor: **multi-signal sobre single-signal**, **contratos sobre invocação implícita**, **adaptive sobre binário**. Sem reescrever arquitetura — refinar o que existe.

### Sprint 0 — Eval Suite Skeleton (NEW v2.0, 1-2 dias, 2 pts)

**Problema (post-Advisory-Council):** Sem instrumentação de cost/latency/tool-calls e sem eval suite, os 7 sinais do heartbeat (Sprint A) não têm baseline para calibração; o citation adaptativo (Sprint D) não tem regressão para validar melhorias. A indústria 2026 (Gartner: 40% projetos agentic cancelados até 2027 por falta de eval/observabilidade) coloca eval engineering como **prerequisite**, não posterior. Origem: Advisor B (outsider) + Advisor A (expansion) endossa via "predictive budget".

**Mudança:**
- Instrumentação básica em `squads/research/scripts/tech-research/`:
  - `cost_tracker.py` — registra tokens used + cost estimate por phase em estrutura mínima
  - `tool_call_counter.py` — registra Tool: X invocations por run (preparação para Sprint C parallel spawn observability)
- `eval-suite/` novo diretório em `squads/research/`:
  - `eval-suite/fixtures/` — 3 fixtures históricas de runs reais (`docs/research/2026-04-*/` selecionados)
  - `eval-suite/rubric.yaml` — rubric humana de qualidade (5 dimensões: coverage, citation quality, claim verifiability, narrative coherence, actionability)
  - `eval-suite/llm_judge.py` — stub que aplica rubric via LLM-judge em fixture (output: score 0-100 + per-dimension breakdown)
  - `eval-suite/regression_runner.sh` — orquestrador que roda fixture → run atual → diff
- Output mínimo: 1 run completo de `/tech-research` gera `cost-latency.yaml` com estrutura preliminar (Sprint A vai expandir)
- **NÃO inclui**: full eval suite Gartner-grade. É skeleton mínimo que destrava A, B, D — não tenta resolver eval engineering completo neste sprint.

**Files touched:**
- `squads/research/scripts/tech-research/cost_tracker.py` (NEW)
- `squads/research/scripts/tech-research/tool_call_counter.py` (NEW)
- `squads/research/eval-suite/rubric.yaml` (NEW)
- `squads/research/eval-suite/llm_judge.py` (NEW)
- `squads/research/eval-suite/regression_runner.sh` (NEW)
- `squads/research/eval-suite/fixtures/` (NEW — 3 selected runs)
- `squads/research/eval-suite/README.md` (NEW — explicar escopo skeleton vs Gartner-grade)
- `squads/research/config.yaml` (EDIT — adicionar `eval-suite/` em artifact_contracts ou whitelist)

**Acceptance:**
- [ ] `cost_tracker.py` produz output válido para 1 run completo (verificável via fixture)
- [ ] `tool_call_counter.py` registra ≥ 1 tool call por run
- [ ] `eval-suite/rubric.yaml` declarada com 5 dimensões + scoring guide
- [ ] `llm_judge.py` aplica rubric em 1 fixture histórica retorna score numérico
- [ ] `regression_runner.sh` executa fixture→atual com exit code coerente
- [ ] README.md documenta escopo skeleton (anti-overengineering)
- [ ] `validate:scripts-exist` passa para os 3 scripts novos
- [ ] EXP.1 (próximo) pode reusar `llm_judge.py` para A/B test de qualidade

---

### Sprint A — Heartbeat Multi-Signal (1 semana, 5 pts)

**Problema:** P3.5 hoje para por `coverage_score >= 70` OR `wave == 3`. Single-axis, frágil, sem cost-awareness.

**Mudança:**
- Novo `squads/research/data/heartbeat-policy.yaml` declara **7 stop signals** e **3 replan signals**:
  ```yaml
  stop_when_any:
    - coverage_score >= 70           # existing
    - token_budget_used > 85%         # NEW (inspired by node-deepresearch)
    - wallclock_used > timeout_sec    # NEW (inspired by alibaba 150min)
    - cost_usd_used > cost_max        # NEW (gap real no mercado — diferenciador)
    - gap_set.is_empty()              # NEW (gap loop, ver Sprint B)
    - new_information_ratio < 0.05    # NEW (convergence detection)
    - wave_num == 3 AND coverage<50   # existing (escalation)

  replan_when_any:
    - source_contradiction_detected   # NEW
    - wave_returned_low_signal        # NEW
    - unsupported_claim_top_tier > N  # NEW
  ```
- `squads/research/workflows/tech-research/phase-3-5-evaluate-coverage.yaml` lê a policy em vez de hardcode.
- `squads/research/scripts/tech-research/coverage_calculator.py` retorna struct rica:
  ```json
  {
    "coverage": 0.74,
    "token_used_pct": 0.62,
    "wallclock_sec": 142,
    "cost_usd": 0.84,
    "cost_confidence": "exact | approximate | unavailable",
    "gaps_open": 3,
    "new_info_ratio": 0.18,
    "decision": "stop|continue|replan|escalate",
    "rationale": "..."
  }
  ```
  Quando `cost_confidence == "unavailable"`, o heartbeat **IGNORA o signal `cost_usd_used`** (não trata como zero). Origem: roundtable @architect C02 + @pm F06.
- `pipeline-state.yaml` ganha bloco `budget:` com `{token_max, cost_usd_max, wallclock_max_sec}` + actuals.
- Novo artefato `cost-latency.yaml` (citado em `gap-analysis.md` como faltante no mercado inteiro).

**Files touched:**
- `squads/research/data/heartbeat-policy.yaml` (NEW — declara `governed_by: quality-gates.yaml` para precedência)
- `squads/research/data/quality-gates.yaml` (EDIT — declara precedência SOT macro)
- `squads/research/workflows/tech-research/phase-3-5-evaluate-coverage.yaml` (EDIT)
- `squads/research/scripts/tech-research/coverage_calculator.py` (EDIT)
- `squads/research/templates/tech-research/pipeline-state.yaml` (EDIT)
- `squads/research/config.yaml` (EDIT — adicionar `cost-latency.yaml` em `artifact_contracts[]`)
- `squads/research/scripts/tech-research/output_validator.py` (EDIT — validate heartbeat-policy.yaml schema)
- `.claude/skills/tech-research/SKILL.md` (EDIT — documentar stop signals) + `ide-sync sync` pós-edit
- changelog público: parágrafo em linguagem de usuário sobre cost-aware + time-aware heartbeat (origem: @vision-chief F02)

**Acceptance (split em 2 ACs distintos para evitar circular dependency — origem: @research-chief F02):**

**AC-A1 (testável com fixture sintético, validável em CI imediatamente):**
- [ ] `heartbeat-policy.yaml` declara 7 stop signals + 3 replan signals
- [ ] `output_validator.py` valida schema do `heartbeat-policy.yaml` (rejeita arquivo ausente ou inválido)
- [ ] `coverage_calculator.py` retorna struct rica incluindo `cost_confidence`
- [ ] Precedência declarada: `heartbeat-policy.yaml#governed_by: quality-gates.yaml`
- [ ] `cost-latency.yaml` em `artifact_contracts[]`
- [ ] Schema validation com 3 fixtures sintéticos: 5 dos 7 signals devem disparar `stop`; 2 dos 3 replan signals devem disparar `replan`

**AC-A2 (validável pós-merge com run real):**
- [ ] Cost signal ativo: 1 run completo de `/tech-research` produz `cost-latency.yaml` com valores reais
- [ ] `cost_confidence == "unavailable"` faz heartbeat ignorar o signal (testado via mock)
- [ ] Replan signals disparam re-execução da phase atual (não pular para próxima)
- [ ] Regression: 3 fixtures de runs históricos não quebram

---

### Sprint B — Gap Set + Reflect Phase (1 semana, 5 pts)

**Problema:** Wave 2 re-decompõe o brief inteiro. Queries não miram gaps específicos da Wave 1. Sem `gaps[]` persistido, self-criticism é implícita.

**Mudança:**
- Nova fase `squads/research/workflows/tech-research/phase-3-4-reflect-and-gap-detect.yaml` (entre P3.2 e P3.5).
- Novo script `squads/research/scripts/tech-research/gap_detector.py` emite `gaps.yaml`:
  ```yaml
  # SEMÂNTICA: APPEND-ONLY por wave (origem: roundtable @research-chief F03 + @architect C01)
  # - Wave N nunca remove gaps de waves anteriores; só transitiona status (open → closed | abandoned)
  # - Novos gaps descobertos em Wave N são adicionados ao final
  # - pipeline-state.yaml referencia gaps por ID (recovery determinístico em crash mid-wave)
  # - gap_set.is_empty() do Sprint A stop signal = TODOS os gaps com status != open
  gaps:
    - id: G001
      question: "What's the empirical cost of replan loops in production?"
      source_hint: "academic-paper OR enterprise-postmortem"
      priority: high
      attempts: 0
      status: open  # open|closed|abandoned
      opened_in_wave: 1
      closed_in_wave: null
      closed_by_source: null  # populated when status=closed
  ```
- Wave 2+ consome `gaps.yaml` e gera sub-queries **direcionadas aos gaps abertos** (não re-decompose brief).
- Learning log captura `gaps_opened`, `gaps_closed`, `gaps_persisted` por wave — telemetria de auto-melhoria.

**Files touched:**
- `squads/research/workflows/tech-research/phase-3-4-reflect-and-gap-detect.yaml` (NEW)
- `squads/research/scripts/tech-research/gap_detector.py` (NEW)
- `squads/research/workflows/tech-research/phase-3-execute-research.yaml` (EDIT — consume gaps na Wave 2+)
- `squads/research/templates/tech-research/gaps.yaml` (NEW template)
- `.claude/skills/tech-research/SKILL.md` (EDIT — documentar nova phase)

**Acceptance:**
- [ ] `gaps.yaml` emitido após Wave 1 com schema validado
- [ ] Semântica APPEND-ONLY documentada no top do arquivo + enforced em `gap_detector.py`
- [ ] **Classificador automatizado** (`squads/research/scripts/tech-research/gap_alignment_check.py`) verifica que Wave 2 gera ≥ 60% das sub-queries com alinhamento a gaps específicos (origem: @pm F07)
- [ ] Métrica `gaps_closed_per_wave`, `gaps_opened_per_wave`, `gaps_persisted` exposta no `metrics.yaml`
- [ ] Crash recovery testado: simular interrupção mid-wave → `gaps.yaml` consistente, pipeline-state.yaml referencia gaps por ID
- [ ] `validate:scripts-exist` passa com novo script (origem: @cso M-01)
- [ ] Decisão sobre product-discovery mode: Sprint B aplica-se OR ficar fora? (resolver na story spec, origem: @research-chief F06)
- [ ] Inspiração: `node-deepresearch/src/agent.ts:ReflectAction` (arquitetura, não código — Jina é proprietary)

---

### STORY-RA-EXP.1 — KISS Gate 1 Falsificável (NEW v2.0, 1 dia, 2 pts)

**Problema (post-Advisory-Council):** O ADR original saltou de "specialists declarados nunca invocados" para "Multi-Agente score 57,5 → 80+" sem evidência empírica de que spawn paralelo produz **melhor output para o usuário** (vs apenas melhor score arquitetural). KISS rule `kiss-no-overengineering.md` exige Gate 1 = "Citar real failure (não hipotético)" e Gate 2 = "Show cheaper alternative tried". Inline persona-fidelity é a cheaper alternative que não foi testada. Origem: Advisor C (contrarian) + Advisor D (first-principles, "ligação inferida, não medida") consenso.

**Mudança:**
- Experimento controlado de 10 runs em 2 fixtures históricas:
  - **5 runs com inline persona-fidelity** (status quo): `/tech-research` encarna Sackett/Klein mentalmente em P4 e P4.5 (single context).
  - **5 runs com spawn manual ad-hoc**: `/tech-research` com Task tool spawn em P4 e P4.5, invocando Sackett e Klein como subagentes paralelos. Sem `specialist-contracts.yaml` ainda — invocação manual via prompt direto.
- LLM-judge (do Sprint 0) aplica rubric 5-dim em cada output:
  - Coverage, citation quality, claim verifiability, narrative coherence, actionability.
- Análise: delta médio de score entre as duas condições.

**Critério PASS/FAIL:**
- **PASS** (delta ≥ 10% favorecendo spawn): Sprint C procede. KISS Gate 1 fechado com evidência empírica.
- **FAIL** (delta < 10% ou favorecendo inline): Sprint C **DEFERRED**. ADR-002 v2.0 procede com Sprints 0+A+B+D+E (total = 24 pts). Sprint C reabre como `EXP.2` em ADR-003 com hipótese alternativa.

**Files touched:**
- `squads/research/eval-suite/experiments/EXP-RA-001/` (NEW):
  - `protocol.md` (descreve experimento)
  - `fixtures-selected.yaml` (quais 2 runs históricos)
  - `results.yaml` (scores per run, delta médio, p-value se calculável)
- `STORY-RA-EXP.1.md` (NEW em `docs/stories/epic-research-intelligence/` (Wave 6+ stories, prefixo `RA-*`))
- `.aiox/learning/logs/tech-research/EXP-RA-001-{date}.yaml` (NEW — captura learning incremental)

**Acceptance:**
- [ ] 10 runs completos com `cost-latency.yaml` registrado (Sprint 0 entrega esse tracking)
- [ ] LLM-judge aplicado em todos os 10 outputs com rubric idêntica
- [ ] `results.yaml` declara delta médio por dimensão + delta global
- [ ] Decisão PASS/FAIL documentada com rationale
- [ ] Se FAIL: STORY-RA-RESCORE.1 reformulada (target Multi-Agente removido); ADR-003 issue aberta
- [ ] Se PASS: Sprint C procede com confidence empírica

**Não confunda EXP.1 com SPIKE-RA-C.0:**
| Artefato | Pergunta respondida | Decisão de saída |
|---|---|---|
| **EXP.1** (este) | Spawn paralelo melhora **qualidade do output** mensurável? | DEFER Sprint C ou prossegue |
| **SPIKE-RA-C.0** (depois) | Spawn paralelo é **tecnicamente viável** no executor YAML atual? | DEFER Sprint C ou prossegue |

EXP.1 vem ANTES porque se o ganho de qualidade não é provado, o esforço técnico de SPIKE+Sprint C é desperdiçado por construção.

---

### Sprint C — Specialist Contracts + Parallel Spawn (2,5 semanas, 11 pts post-roundtable)

**Problema:** 6-7 agents (Sackett, Klein, Creswell, Forsgren, Gilad, Booth) declarados mas nunca invocados. Inline persona-fidelity os encarna mentalmente em vez de chamar via Task tool. Multi-Agente score 57,5 vs DeerFlow 90.

**Pré-requisitos bloqueantes v2.0 (NÃO inicia sem todos os 4):**
1. **EXP.1 PASS** (delta de qualidade ≥ 10% no LLM-judge — KISS Gate 1 fechado empiricamente). Origem: Advisor C + D do Advisory Council.
2. `SPIKE-RA-C.0` retornou verde (Task tool spawn paralelo viável no executor YAML atual)
3. Sprint E entregue (5 agent files preparados com frontmatter schemático)
4. ADR-001 Wave 1 com ≥ 1 story atendendo critério **git-based**: `status: InProgress` em story doc OU commit em branch `feat/ADR-001-*` nos últimos 3 dias úteis (@research-chief decide via `gh pr list` / `git log`). Origem: Advisor E + @pm F04 + @vision-chief F01.

**Plano B (v2.0):** Se qualquer um dos 4 pré-requisitos falhar:
- EXP.1 FAIL → Sprint C declarado DEFERRED; ADR-002 entrega Sprints 0+A+B+D+E (total 24 pts)
- SPIKE vermelho → Sprint C DEFERRED; ADR-003 abre com nova estimativa pós-mudança no executor
- Sprint E não entregue → bloqueio simples, espera entrega
- Hard Gate não atendido → bloqueio simples, espera ADR-001 Wave 1 iniciar

**Mudança:**
- Novo `squads/research/data/specialist-contracts.yaml` formaliza I/O contratual para 5 specialists.
- **Campo `available_tools[]` (forward-compat com ADR-001 Wave 2, origem @architect H03):** hoje vazio; quando `@sinkra/research-adapters` ou MCP server estiverem disponíveis, specialists podem declarar quais tools podem chamar sem mudar schema.

  ```yaml
  sackett:
    invoked_when: "evidence_grading_required == true"
    input_schema: {claims: [{text, sources[]}]}
    output_schema: {graded_claims: [{text, sources[], grade: 1a|1b|2a|2b|3|4|5, rationale}]}
    available_tools: []  # populated when ADR-001 Wave 2 entrega adapters
    triggers_in_phase: P4.5
  klein:
    invoked_when: "mode in [product-discovery, strategic-decision]"
    input_schema: {synthesis_draft, hypotheses[]}
    output_schema: {pre_mortem[], system1_assumptions[], steelman_counter[]}
    triggers_in_phase: P4
  booth:
    invoked_when: "wave_num == 0 AND coverage_target > 70"
    input_schema: {strategic_brief}
    output_schema: {systematic_search_plan, source_taxonomy}
    triggers_in_phase: P2
  creswell:
    invoked_when: "research_design == 'mixed-methods'"
    input_schema: {brief, evidence_so_far}
    output_schema: {design_rationale, sequence: [phase_id], integration_points}
    triggers_in_phase: P1.5
  forsgren:
    invoked_when: "domain_signals contains 'devops|delivery|deployment'"
    input_schema: {claims_re_devops}
    output_schema: {dora_alignment, missing_metrics, antipatterns_detected}
    triggers_in_phase: P4
  ```
- Em P3, P4 e P4.5, **trigger map** consulta `specialist-contracts.yaml` e invoca specialists em **paralelo via Task tool nativo** quando o trigger casa.
- Failure isolation: se 1 specialist falha, os outros continuam (`failure_mode: warn_and_continue` no contract).
- Adicionar flag `--parallel-subagents` ao `/tech-research` (resolve GAP-08 que estava DEFERRED no ADR-001).
- Gilad fica fora desta wave — fica para `research-chief` redirect quando mode=spy/competitive (não no pipeline tech-research core).

**Files touched:**
- `squads/research/data/specialist-contracts.yaml` (NEW)
- `squads/research/scripts/tech-research/specialist_dispatcher.py` (NEW)
- `squads/research/workflows/tech-research/phase-3-execute-research.yaml` (EDIT — chamada paralela)
- `squads/research/workflows/tech-research/phase-4-synthesize.yaml` (EDIT)
- `squads/research/workflows/tech-research/phase-4-5-verify-citations.yaml` (EDIT)
- `squads/research/agents/sackett.md`, `klein.md`, `booth.md`, `creswell.md`, `forsgren.md` (EDIT — adicionar I/O schemas no frontmatter para match com contract)
- `.claude/skills/tech-research/SKILL.md` (EDIT — adicionar `--parallel-subagents` flag)

**Acceptance:**
- [ ] 5 contracts validados via schema
- [ ] Cada specialist tem `available_tools: []` declarado (forward-compat)
- [ ] Run com `--parallel-subagents` spawna pelo menos 2 specialists em paralelo (medido via execution-log.jsonl timestamps)
- [ ] Falha simulada de 1 specialist não derruba o run (failure isolation)
- [ ] `validate:scripts-exist` passa com `specialist_dispatcher.py`
- [ ] `ide-sync sync` executado pós-edit do SKILL.md (origem: @cso H-02)
- [ ] **Re-score Multi-Agente movido para epic-level AC** (story dedicada `STORY-RA-RESCORE.1` pós-Sprint D, origem: @vision-chief F04 + @pm F01)
- [ ] **Route-accuracy check (NEW v2.0, origem: Advisor B + Council CF-3):** 3 fixtures com triggers explícitos dos 5 specialists. Se algum specialist deveria ter sido invocado pelo `invoked_when` e NÃO foi → bug de routing identificado (não é "specialist desnecessário"). Documentar em `eval-suite/experiments/EXP-RA-002-route-accuracy/results.yaml`.

---

### Sprint D — Citation Verify Adaptativo (1 semana, 3 pts)

**Problema:** CITATION_GATE faz `2 fix attempts → VETO`. Fix attempts apenas re-buscam. Não há archive snapshot, não há rewrite-claim, não há classificação per-claim.

**Mudança:**
- `squads/research/scripts/tech-research/citation_verifier.py` evolui para per-claim retry com:
  - **archive.org snapshot fallback** quando URL retorna 404/410
  - **rewrite-claim** quando source diverge: ajusta o claim para refletir o que a fonte realmente diz, em vez de inventar suporte
  - **classification per-claim**: `supported | unsupported | unknown | ambiguous` (inspirado em `deep-research-bench/utils/validate.py`)
- Veto threshold sobe de `verified_ratio < 0.85` para `unsupported_top_tier > 20%` — claims unsupported viram **explicitamente low-confidence no relatório**, não razão para veto.
- Gate emite `confidence_distribution` em `claims.yaml`: `{high: N, medium: M, low: L, unsupported: U}`.

**Files touched:**
- `squads/research/scripts/tech-research/citation_verifier.py` (EDIT)
- `squads/research/scripts/tech-research/claim_extractor.py` (EDIT — emitir per-claim metadata)
- `squads/research/workflows/tech-research/phase-4-5-verify-citations.yaml` (EDIT)
- `squads/research/data/quality-gates.yaml` (EDIT — thresholds)
- `squads/research/templates/tech-research/claims.yaml` (EDIT — schema confidence)

**Acceptance:**
- [ ] archive.org snapshot tentado em ≥ 1 fixture com URL morto
- [ ] Per-claim classification visível em `claims.yaml` de qualquer run
- [ ] **Schema `claims.yaml` ganha `rewritten: true | false` + `original_claim: <texto>`** (origem: @architect H01 — risco epistêmico do rewrite-claim sem trail)
- [ ] Relatório final marca claims reescritos com nota de rodapé exibindo texto original
- [ ] Rewrite-claim documentado quando source diverge (com diff antes/depois no learning log)
- [ ] `cost-latency.yaml` cumpre Gold Observatory Rule 9 (mirror em JSON visual, origem: @cso M-02)
- [ ] Citações score na rubric: 76 → 85+ (target movido para epic-level)

---

### Sprint E — KISS Cleanup EXPANDIDO (3 dias hard timebox, 3 pts post-roundtable)

**Problema:** Squad acumulou entropia. Adicionar capacidade antes de remover ruído viola `kiss-no-overengineering.md`. Pós-roundtable: cleanup expandido para cobrir registry sync + alias + workflow refs + preparação de agent files para Sprint C.

**Hard timebox:** 3 dias úteis. Qualquer achado adicional vira DEFERRED story (não bloqueador). Origem: @pm F05.

**Mudança:**

1. **Mapping consumers do `dr-orchestrator` (precondition):**
   ```bash
   grep -rn "dr-orchestrator" squads/ .claude/ docs/ apps/research/ > /tmp/dr-orchestrator-consumers.txt
   ```
   Listar TODOS os consumers antes de deprecar. Origem: @architect H02 + @aiox-master F04.

2. **Deprecar `dr-orchestrator` com governance completa:**
   - `squads/research/config.yaml`: `dr-orchestrator: status: deprecated_at: 2026-05-18, redirect_to: research-chief`
   - `squads/research/agents/dr-orchestrator.md`: deprecation notice no header com link para `research-chief`
   - **Alias entry** (identity-vs-slug rule): adicionar em `outputs/qa/aliases-pending-registry.yaml` → `@dr-orchestrator → @research-chief`. Origem: @aiox-master F04.
   - **Ecosystem registry sync**: atualizar `squads/sinkra-squad/data/ecosystem-registry.yaml` (§agents linhas 1026-1055) — remover dr-orchestrator de UC-001~004 OR marcar como deprecated_at. Origem: @cso C-01.
   - **Workflow refs**: EDIT `squads/research/workflows/wf-deep-research.yaml` + qualquer outro arquivo do grep que referencie `dr-orchestrator` por nome. Origem: @research-chief F05.

3. **5 specialists dormentes preparados para Sprint C:**
   - `config.yaml`: `status: dormant` para Sackett, Klein, Booth, Creswell, Forsgren (campo agora válido via STORY-RA-PRE.1)
   - **Frontmatter schemático**: cada um dos 5 agent files ganha `input_schema:` + `output_schema:` no frontmatter, compatível com `specialist-contracts.yaml`. Origem: @research-chief F01.
   - Atualizar `squad: "spy"` → `squad: "research"` em Sackett (legacy header). Origem: @research-chief F01.
   - **Gilad explicitamente**: `status: dormant` declarado na tabela do Sprint E (não apenas em prosa). Origem: @cso L-01.

4. **`tasks/` 65 items flat → ≤ 4 subdiretórios:**
   - **Dry-run obrigatório**: `npm run sinkra:rename-artifact -- --dry-run` antes de qualquer move. Origem: @architect M02.
   - **Atualizar globs em `composition_mapping.atoms.mapping[].pattern`** no `config.yaml` simultaneamente ao move — patterns são globs, não string substitution. Origem: @research-chief F04.
   - Categorias: `tech-research/*`, `benchmark/*`, `product-discovery/*`, `marketing/*`. NÃO criar diretórios novos sem ≥ 3 arquivos cada (KISS reverse-direction). Origem: @cso H-03.

5. **Marketing-deepdive workflow:**
   - **Downgrade imediato** da skill `/research-marketing-deepdive` para `status: draft` se workflow ausente. Não criar scaffolding vazio. Origem: @research-chief F07.
   - Confirmar `entry_agent: marketing-deepdive` em `config.yaml`.

6. **product-discovery-framework.md drift check:**
   - Verificar sync com `phase-1-5-decompose.yaml`; eliminar drift. Origem: original.

**Files touched:**
- `squads/research/config.yaml` (EDIT — status flags + composition_mapping globs)
- `squads/research/agents/dr-orchestrator.md` (EDIT — deprecation notice + redirect)
- `squads/research/agents/{sackett,klein,booth,creswell,forsgren,gilad}.md` (EDIT — frontmatter schemático + status)
- `squads/sinkra-squad/data/ecosystem-registry.yaml` (EDIT — sync deprecation)
- `outputs/qa/aliases-pending-registry.yaml` (EDIT — alias entry)
- `squads/research/workflows/wf-deep-research.yaml` + outros (EDIT — refs)
- `squads/research/tasks/**` (MOVE via sinkra:rename-artifact com dry-run)
- `squads/research/data/product-discovery-framework.md` (EDIT se drift)
- `.claude/skills/research-marketing-deepdive/SKILL.md` (EDIT — `status: draft` se workflow ausente)

**Acceptance:**
- [ ] Grep `dr-orchestrator` retorna apenas refs com deprecation notice OU redirect
- [ ] Alias entry presente em `aliases-pending-registry.yaml`
- [ ] `ecosystem-registry.yaml` sincronizado (origem: @cso C-01, condição CRITICAL)
- [ ] 5 specialists com frontmatter `input_schema` + `output_schema` declarados (Sprint C bloqueado sem isso)
- [ ] Gilad explicitamente listado com `status: dormant` na tabela
- [ ] `tasks/` categorizado em ≤ 4 subdiretórios com ≥ 3 arquivos cada
- [ ] `composition_mapping` globs atualizados no `config.yaml`
- [ ] `npm run validate:squad-structure` passa com gate ≥ 3 files per subdir
- [ ] `npm run validate:reconciliation` retorna 0 inconsistências para squad research
- [ ] `npm run validate:registry-accuracy` passa (origem: @cso C-01)
- [ ] Marketing-deepdive: workflow OU skill `status: draft`

---

## Sequencing & Dependencies

> **SUPERSEDED v1.0:** Esta seção foi consolidada em [`Scope & Roundtable Conditions → Sequencing ENFORCED`](#sequencing-enforced-post-roundtable) (acima). Sequencing original v0.1 movido para histórico abaixo.

### Histórico v0.1 (pré-roundtable)

```
Sprint E (KISS cleanup) ──┐
                          │
Sprint A (heartbeat) ─────┼──► Sprint B (gap loop, depende de A para multi-signal)
                          │
                          └──► Sprint C (specialists, depende de E para contracts)
                                  │
                                  └──► Sprint D (citation adaptativo, usa Sackett do Sprint C)
```

**Mudança v1.0 (post-roundtable):**
- Sprint E vira **first hard-timebox** (3d) — não mais "pode rodar primeiro ou em paralelo".
- Adicionado **SPIKE-RA-C.0** entre Sprint B e Sprint C (1 dia, desbloqueia Sprint C).
- Sprint C ganha **hard gate**: aguarda ADR-001 Wave 1 ≥ 1 story em desenvolvimento ativo (origem: roundtable H3 — overlap mitigation).
- Adicionado **STORY-RA-RESCORE.1** após Sprint D (epic-level validation, +2 pts).

---

## Consequences

### Positive

- **Score baseline composto**: 60,25 → ~70 sem tocar em MCP/Sandbox/Memory. Combinado com ADR-001 Wave 1 (~72), chega a ~80 em ~8 semanas (vs 16 só com ADR-001).
- **Multi-Agente score**: 57,5 → 80+ ao formalizar specialists com contratos reais.
- **Citações score**: 76 → 85+ via per-claim adaptive verify.
- **Diferenciador único** em **cost-aware + time-aware heartbeat** — gap real no mercado (0/18 repos analisados fazem bem).
- **Auditabilidade** preservada — todos novos artefatos (`gaps.yaml`, `cost-latency.yaml`, `confidence_distribution`) entram no learning log e no Observatory.
- **PT-BR + Governance moats** intactos.
- Resolve GAP-08 (parallel subagents) que estava DEFERRED no ADR-001, sem novo dependency externo (usa Task tool nativo).

### Negative

- **23 pts de effort** adicional ao roadmap. Se executado serial após ADR-001: +5 semanas total. Se paralelo (recomendado): zero atraso de calendário, mas dobra carga no squad-engine durante o overlap.
- **Risco de over-specification dos contratos** (Sprint C). Mitigação: começar com 3 specialists (Sackett, Klein, Booth) e adicionar Creswell/Forsgren só quando demand for medida.
- **Cost-aware heartbeat exige token counting confiável** — depende de Anthropic SDK token estimation. Cair pra approximate tiktoken se necessário.
- **archive.org rate-limit** pode bloquear Sprint D em runs grandes. Mitigação: backoff exponencial + cache local de snapshots.
- **Sprint E cleanup pode esconder drift documentational** mais profundo. Mitigação: rodar `npm run validate:reconciliation` antes e depois.

### Neutral

- Stack permanece Node+TS para framework, Python para extractors.
- Nenhum dependency externo novo (sem LangGraph, sem vLLM, sem HF transformers).
- Compatible com Constitution: Story-Driven (cada Sprint vira uma story), Quality First (gates preservados), KISS (Sprint E faz o cleanup antes).
- Compatible com `.claude/rules/research-bench-gold.md` — não toca em research-bench skill.

---

## Alternatives Considered

### Alt 1 — Adotar LangGraph como runtime
**Rejected.** Já descartado no ADR-001 `NO-GO-03`. Architectural mismatch com Claude Code native. Perde Task tool nativo, governance gates, learning log incremental. Inspirar Supervisor pattern (Sprint C) é suficiente.

### Alt 2 — Treinar modelo agentico próprio (Pattern 4 RL emergent)
**Rejected.** Já descartado no ADR-001 `NO-GO-01`. >$200k. OpenResearcher/DeepResearcher/Tongyi vão entrar como backend opcional pelo ADR-001 Wave 2. ADR-002 mantém Pattern 2 estruturado como core, não substitui.

### Alt 3 — Re-implementar Token-Budgeted State Machine do Jina node-DR
**Rejected.** Código é proprietary (`Copyright Jina AI Limited. All rights reserved`). Bench `deep/license-risk-assessment.md` flagga absorção proibida. **Inspirar arquitetura** (token budget + ReflectAction structure) é OK e é o que Sprint A + B fazem.

### Alt 4 — Big-bang rewrite do squad em padrão Lead+Specialists (Pattern 3 wholesale)
**Rejected.** Blast radius enorme. Quebra COVERAGE_GATE/CITATION_GATE atuais que são moat. Sprint C entrega Pattern 3 como opt-in (`--parallel-subagents`), preservando Pattern 2 como default.

### Alt 5 — Não fazer ADR-002, esperar ADR-001 Wave 3 terminar
**Rejected.** Wave 3 termina semana 20. Squad continua perdendo Multi-Agente (-32,5) e Self-criticism por 5 meses. ADR-002 paralelo entrega ganho de 10 pts em 5 semanas sem custo de oportunidade do ADR-001.

### Alt 6 — Fazer só Sprint A + B (heartbeat + gap loop), pular Sprint C-E
**Rejected via Roundtable consensus 2026-05-18:** 6/6 reviewers concordam (consenso documentado em `ROUNDTABLE-REPORT-ADR-002-2026-05-18.md`) — Sprint A+B sem C re-investe num pipeline com specialists não-invocados. Sprint E (cleanup) precisa vir primeiro. Sprint C é o que move a agulha em Multi-Agente score (+22,5 pts, o gap maior). Advisory Council vai validar este reject como parte do KISS Gate 2 final.

---

## Compliance Considerations (post-roundtable)

- **Licenças:** nenhum código externo absorvido nesta ADR. Sprints só editam código próprio. Inspiração arquitetural de `node-deepresearch` (Jina, proprietary) é OK porque não copia código.
- **Constitution:**
  - Story-Driven: cada Sprint vira stories em `docs/stories/epic-research-intelligence/` (Wave 6+ stories, prefixo `RA-*`) com `EPIC.md` pai pré-criado (origem: roundtable H1)
  - Agent Authority: só @devops pushes/PRs; `@aiox-dev` nomeado como code executor em cada story (origem: roundtable @pm F03)
  - Quality First: validators rodam pré-push (preservado). Adicionados: `validate:scripts-exist`, `validate:registry-accuracy`, `validate:reconciliation` por sprint
  - KISS: Sprint E é o cleanup primeiro; Sprint C respeita reverse-direction (Dir < 3 files → flatten)
  - **KISS Gate 2 (cheaper alternative tried?):** ✅ FECHADO v2.0 — Advisory Council respondeu via 2 mecanismos: (a) Sprint 0 (eval suite skeleton) é cheaper baseline antes de Sprint A; (b) STORY-RA-EXP.1 (10 runs A/B persona-inline vs spawn manual) falsifica Sprint C antes de comprometer 11 pts. Se EXP.1 FAIL, Sprint C DEFERRED → 24 pts total. Origem: Advisory Council Report CF-2.
- **Extraction No-Fallbacks:** não aplicável (squad research não é extractor).
- **Portable Paths:** todos novos arquivos seguem repo-relative (`squads/research/...`).
- **research-bench-gold rule:** não tocado nas Sprints A-E. Cumprido em `STORY-RA-RESCORE.1` (profile=gold_absorption) e em Sprint D (cost-latency.yaml mirror em JSON, Rule 9 — origem: @cso M-02).
- **Identity-vs-slug rule:** `@dr-orchestrator` identity handle preservado via alias entry em `aliases-pending-registry.yaml` (origem: @aiox-master F04).
- **Sync rule:** ADR-002 fora do allowlist Hub→Spoke sync durante execução; `ide-sync sync` obrigatório após cada SKILL.md edit (origem: @cso H-02).

---

## Quality Gates v2.0 (preservados + estendidos + eval-first)

| Gate | Antes | Depois v2.0 |
|---|---|---|
| COVERAGE_GATE | single-signal `coverage_score` | multi-signal via `heartbeat-policy.yaml` (Sprint A) |
| CITATION_GATE | binário veto/aprova | per-claim adaptive com archive fallback (Sprint D) |
| Incremental Learning Log | per-phase write | + gaps_opened/closed métricas (Sprint B) + parallel spawn lifecycle (Sprint C) |
| Output Validator | YAML schema | + `heartbeat-policy.yaml`, `gaps.yaml`, `specialist-contracts.yaml` schemas |
| **EVAL_GATE (NEW v2.0)** | inexistente | `eval-suite/` skeleton (Sprint 0) → LLM-judge rubric 5-dim aplicado em fixtures históricas a cada release. Origem: Advisor B (Council CF-1). |
| **KISS_GATE_1 (NEW v2.0)** | conceitual | falsificável via STORY-RA-EXP.1 (10 runs A/B, delta ≥ 10%). Origem: Advisor C (Council CF-2). |
| **ROUTE_ACCURACY (NEW v2.0)** | inexistente | 3 fixtures com triggers explícitos validam que `invoked_when` dos specialists funciona. Origem: Advisor B (Council CF-3). |

---

## Implementation Plan v2.0 (post-Advisory-Council, 17 stories worst case)

Ver Sprint 0/A/B/C/D/E acima. Cada Sprint vira stories em `docs/stories/epic-research-intelligence/` (Wave 6+ stories, prefixo `RA-*`):

**Pre-conditions (bloqueiam qualquer Sprint):**
- `EPIC-RESEARCH-INTELLIGENCE.md (extended 2026-05-18 com Wave 6+)` — Epic PRD pai (origem: roundtable H1)
- `STORY-RA-PRE.1` — Schema update process-mapping-rules.yaml: campo `status` em agents[] (1 pt, origem: @aiox-master F01)

**Sprint 0 — Eval Suite Skeleton (NEW v2.0, PRIMEIRO, 2 pts):**
- `STORY-RA-0.1` — cost_tracker.py + tool_call_counter.py instrumentation
- `STORY-RA-0.2` — eval-suite/ skeleton: rubric.yaml + llm_judge.py + regression_runner.sh + 3 fixtures históricas

**Sprint E (paralelo ao Sprint 0, 3d hard timebox, 3 pts):**
- `STORY-RA-E.1` — Agent status flags + dr-orchestrator deprecation + alias entry + registry sync + workflow refs (origem: roundtable C3 multi-agent consensus)
- `STORY-RA-E.2` — 5 specialists frontmatter schemático (Sackett, Klein, Booth, Creswell, Forsgren) preparados para Sprint C
- `STORY-RA-E.3` — Tasks/ categorization via sinkra:rename-artifact com dry-run + composition_mapping globs update
- `STORY-RA-E.4` — Marketing-deepdive workflow audit + downgrade para draft se ausente

**Sprint A (após Sprint 0, 5 pts):**
- `STORY-RA-A.1` — Heartbeat policy YAML + multi-signal stop + precedência declarada (AC-A1)
- `STORY-RA-A.2` — Cost-latency artifact + budget block + cost_confidence struct + artifact_contracts entry + run real validation (AC-A2). Reusa cost_tracker.py do Sprint 0.

**[Hard Gate git-based]**: aguarda ADR-001 Wave 1 ter ≥ 1 story `InProgress` OR commit em `feat/ADR-001-*` nos últimos 3 dias úteis antes de prosseguir.

**Sprint B (após A, 5 pts):**
- `STORY-RA-B.1` — Gap detector + gaps.yaml schema com semântica APPEND-ONLY + crash recovery
- `STORY-RA-B.2` — Wave 2 consumes gaps + classificador automatizado de alinhamento ≥ 60%

**STORY-RA-EXP.1 — KISS Gate 1 falsificável (NEW v2.0, 1 dia, 2 pts):**
- 10 runs A/B (5 inline persona-fidelity vs 5 spawn manual) com LLM-judge rubric
- PASS (delta ≥ 10%) → Sprint C procede; FAIL → Sprint C DEFERRED, total = 24 pts

**Spike (após EXP.1 PASS, 1 dia, 1 pt):**
- `SPIKE-RA-C.0` — Prototipar Task tool spawn paralelo em phase YAML isolada → `SPIKE-REPORT-RA-C-0.md`
- Plano B documentado se vermelho: Sprint C → DEFERRED, ADR-003 abre

**Sprint C (após EXP.1 PASS ∧ Spike verde ∧ Sprint E entregue ∧ Hard Gate, 11 pts):**
- `STORY-RA-C.1` — specialist-contracts.yaml com available_tools[] + dispatcher.py
- `STORY-RA-C.2` — Parallel spawn em P3/P4/P4.5 + failure isolation + ide-sync sync
- `STORY-RA-C.3` — `--parallel-subagents` flag + SKILL.md docs

**Sprint D (após C OR após B se C DEFERRED, 3 pts):**
- `STORY-RA-D.1` — Per-claim verify + archive fallback + rewritten + original_claim schema
- `STORY-RA-D.2` — Confidence distribution em claims.yaml + Gold Observatory Rule 9 mirror

**Pós-Sprint D, epic-level validation (2 pts):**
- `STORY-RA-RESCORE.1` — Rodar `/research-bench` profile=gold_absorption em AIOX v5.X + atualizar `decision-rubric.yaml#players[].scores.aiox_research`
- Inclui route-accuracy check para validar CF-3 do Advisory Council

**Cenário Worst Case:** 35 pts ≈ 6,5 semanas (1 FT) — todos os pré-requisitos passam, Sprint C executa.
**Cenário Sprint C DEFERRED via EXP.1 FAIL ou SPIKE vermelho:** 24 pts ≈ 4,5 semanas (1 FT) — Sprints 0+A+B+D+E + EXP.1 entregam valor autônomo; Sprint C reabre em ADR-003.

Epic owner: `@research-chief` (gating/QA). Code executor: `@aiox-dev` (nomeado em cada story). Execution: standard SDC (`/sinkra-validate` → `/sinkra-develop` → `/sinkra-review` → `/sinkra-deploy` → `/sinkra-close`).

---

## Acceptance Criteria (epic-level, v2.0 post-Advisory-Council)

**Pre-conditions satisfeitas:**
- [ ] `EPIC-RESEARCH-INTELLIGENCE.md (extended 2026-05-18 com Wave 6+)` criado com PRD top-level
- [ ] `STORY-RA-PRE.1` completa: schema `status` válido em `process-mapping-rules.yaml`
- [ ] ✅ `ADR-002-advisory-council-report.md` anexado em 2026-05-18 (KISS Gate 2 fechado via Sprint 0 + EXP.1)
- [ ] Sprint 0 entregue: eval-suite skeleton funcional (cost_tracker, tool_call_counter, llm_judge, fixtures)
- [ ] STORY-RA-EXP.1 executada: delta de qualidade medido (PASS ou FAIL documentado)
- [ ] Decisão Sprint C: PROCEED ou DEFERRED registrada formalmente em `docs/stories/epic-RA-agentic-upgrade/SPRINT-C-GATE-DECISION.md`

**Quality outcomes:**
- [ ] Re-score em rubric baseline ≥ 70 sem mexer em ADR-001 entregáveis (multi-agente, citações, planning) — medido via `STORY-RA-RESCORE.1`
- [ ] Re-score Multi-Agente ≥ 80 (vs 57,5 baseline) — medido via `STORY-RA-RESCORE.1`
- [ ] Re-score Citações ≥ 85 (vs 76 baseline) — medido via `STORY-RA-RESCORE.1`
- [ ] Run típico de `/tech-research` emite 100% dos novos artefatos: `gaps.yaml`, `cost-latency.yaml`, `claims.yaml` com `confidence_distribution` + `rewritten` flag
- [ ] `--parallel-subagents` flag funcional com pelo menos 2 specialists spawnados (medido via `execution-log.jsonl` timestamps)

**Regression & governance:**
- [ ] Zero regression em runs existentes (snapshot test em 3 fixtures de `docs/research/` antigos)
- [ ] `npm run validate:squad-structure` retorna 0 erros para squad research
- [ ] `npm run validate:reconciliation` retorna 0 inconsistências
- [ ] `npm run validate:registry-accuracy` passa (post dr-orchestrator deprecation)
- [ ] `npm run validate:scripts-exist` passa para todos os scripts novos
- [ ] `ide-sync sync` executado pós-edit de cada SKILL.md edit
- [ ] Documentação atualizada: `.claude/skills/tech-research/SKILL.md`, `squads/research/ARCHITECTURE.md`, `squads/research/README.md`

**Narrative & GTM (origem: @vision-chief F02 + F03):**
- [ ] Sprint A produz parágrafo de changelog público sobre cost-aware + time-aware heartbeat em linguagem de usuário
- [ ] Release notes consolidadas posicionam ADR-001 + ADR-002 como "v2 quality layer" — narrativa única, duas ondas

---

## Metrics & Re-score Plan

Após Sprint E completo, rodar:

1. **Snapshot test**: re-executar `/tech-research` em 3 fixtures históricas e comparar `02-research-report.md` diff (esperado: melhor qualidade, mesma estrutura).
2. **Re-score bench**: rodar protocolo do `decision-rubric.yaml` contra AIOX v5.X (post-ADR-002) e atualizar `players[].scores.aiox_research`.
3. **Métricas runtime**: medir mean `wallclock_used_sec`, `cost_usd_used`, `gaps_closed_per_wave`, `parallel_specialist_count` em 10 runs.

| Métrica | Baseline | Target post-ADR-002 |
|---|---:|---:|
| Score rubric Multi-Agente | 57,5 | ≥ 80 |
| Score rubric Citações | 76 | ≥ 85 |
| Score rubric Execução (agentic_planning microdims) | 82,7 | ≥ 90 |
| Score composto baseline | 60,25 | ≥ 70 |
| Specialists invocados por run | 0-1 | 2-4 (com flag) |
| Cost per run (USD) — declarado | n/a | rastreado |
| Wallclock per run (sec) — declarado | n/a | rastreado |

---

## References

### Bench analysis
- `docs/bench/deepresearch-absorption-benchmark/skill-gap-analysis-tech-research.md` — gaps direto da skill
- `docs/bench/deepresearch-absorption-benchmark/deep/agentic-planning-reflection.md` — 4 patterns agenticos
- `docs/bench/deepresearch-absorption-benchmark/deep/proposed-technical-expansion-plan.md` — 130 microdims propostas
- `docs/bench/deepresearch-absorption-benchmark/deep/expanded-agentic-ux-research-depth-analysis.md` — 48 microdims aplicadas
- `docs/bench/deepresearch-absorption-benchmark/decision-rubric.yaml` — scores por dimensão
- `docs/bench/deepresearch-absorption-benchmark/gap-analysis.md` — gaps cross-player (trace.jsonl, cost-latency.yaml faltantes em TODOS)

### Source repos (inspiração arquitetural, não absorção de código)
- `outputs/decoded/deer-flow/` — heartbeat checkpoint + middleware (referencial)
- `outputs/decoded/node-deepresearch/` — token-budgeted state machine (referencial, NÃO absorver — proprietary)
- `outputs/decoded/gpt-researcher/` — nested instances + follow-ups
- `outputs/decoded/alibaba-deepresearch/` — multi-signal stop com timeout
- `outputs/decoded/deep-research-bench/` — FACT validator per-claim

### Hub rules
- `.claude/rules/kiss-no-overengineering.md` — fundamenta Sprint E
- `.claude/rules/agent-authority.md` — push/PR via @devops
- `.claude/rules/stories-and-workflows.md` — Story-Driven epic execution
- `.claude/rules/extraction-no-fallbacks.md` — N/A (research não é extractor)

### Companion
- `ADR-001-absorption-strategy.md` — infra/distribuição complementar

---

## Sign-off

| Role | Status | Notes | Date |
|---|---|---|---|
| Roundtable (6 agents) | ✅ APPROVE_WITH_CONDITIONS (7,25/10) | 6/6, 0 conflicts, fast-path → see [ROUNDTABLE-REPORT-ADR-002-2026-05-18.md](./ROUNDTABLE-REPORT-ADR-002-2026-05-18.md) | 2026-05-18 |
| @vision-strategist | Pending | v2.0: Sprint 0 (eval suite) + changelog público endereçam visibilidade de mercado; condições F01-F03 (roundtable) + CF-1 (Council) endereçadas | — |
| @aiox-architect | Pending | v2.0: SPIKE-RA-C.0 desbloqueia C; plano B documentado se vermelho (Sprint C DEFERRED → ADR-003); B01 do roundtable + CP-2 do Council endereçados | — |
| @aiox-pm | Pending | v2.0: Re-estimativa 23→31→35 pts (worst case) ou 24 pts (Sprint C DEFERRED via EXP.1); sequencing enforced com hard gate git-based | — |
| @research-chief | Pending | v2.0: Sprint E preserva workflows ativos; EXP.1 (KISS Gate 1 falsificável) protege contra over-commitment a spawn paralelo sem evidência de qualidade | — |
| Advisory Council (5 advisors) | ✅ PROCEED_WITH_CONDITIONS (6,5/10) | 5/5, cognitive diversity → see [ADR-002-advisory-council-report.md](./ADR-002-advisory-council-report.md). KISS Gate 2 fechado via Sprint 0 + STORY-RA-EXP.1 | 2026-05-18 |

**ADR moves to `Accepted` after 4/4 named deciders sign-off AND Advisory Council report attached.**

**Current status:** v2.0 (post-Advisory-Council) → todas as 5 condições do Council incorporadas → **próximo passo: sign-off 4/4 (@vision-strategist, @aiox-architect, @aiox-pm, @research-chief). ADR move para `Accepted` após 4/4.**

### Recommended next step (v2.0)

✅ Roundtable completo: [`ROUNDTABLE-REPORT-ADR-002-2026-05-18.md`](./ROUNDTABLE-REPORT-ADR-002-2026-05-18.md)
✅ Advisory Council completo: [`ADR-002-advisory-council-report.md`](./ADR-002-advisory-council-report.md)
✅ ADR v1.0 → v2.0 com todas as 10 ações do roundtable + 5 condições do council incorporadas.

**Próximo passo:** Sign-off formal 4/4 dos deciders nomeados. Ações em paralelo:

1. Criar `EPIC-RESEARCH-INTELLIGENCE.md (extended 2026-05-18 com Wave 6+)` em `docs/stories/epic-research-intelligence/` (Wave 6+ stories, prefixo `RA-*`) (precondition #1)
2. Criar `STORY-RA-PRE.1.md` para schema-update de `process-mapping-rules.yaml` (precondition #2)
3. Coletar sign-offs 4/4 via PR ou roundtable formal

Após sign-offs: `Status` move de `Proposed (sign-off pending)` → `Accepted` → entrar SDC pipeline (Sprint 0 começa imediatamente).

---

*ADR-002 v2.0 | 2026-05-18 | Author: claude+@alanicolas | Companion to ADR-001*

**Changelog incremental:**

- **v0.1 → v1.0 (post-roundtable, 6 reviewers, 7,25/10):** Scope & Conditions block, sequencing enforced, re-estimativa 23→31 pts, cost_confidence struct, gaps.yaml append-only, available_tools[] forward-compat, schema rewritten/original_claim, Sprint E expandido com registry sync + alias, EPIC pai + STORY-RA-PRE.1 + SPIKE-RA-C.0 + STORY-RA-RESCORE.1, executor convention @aiox-dev nomeado.

- **v1.0 → v2.0 (post-Advisory-Council, 5 advisors, 6,5/10):** Sprint 0 (Eval Suite Skeleton, 2 pts) inserido antes de Sprint A — eval-first per indústria 2026. STORY-RA-EXP.1 (KISS Gate 1 falsificável, 2 pts) inserida antes do SPIKE — falsifica Sprint C empiricamente via 10 runs A/B persona-inline vs spawn manual. Hard Gate ADR-001 substituído por critério git-based (`status: InProgress` OR commit em branch nos últimos 3d úteis). Plano B documentado se SPIKE-RA-C.0 vermelho (Sprint C DEFERRED → ADR-003). Route-accuracy check adicionado ao Sprint C AC. Re-estimativa 31→35 pts (worst case) ou 24 pts (Sprint C DEFERRED via EXP.1). Quality Gates v2.0 incluem EVAL_GATE + KISS_GATE_1 + ROUTE_ACCURACY. KISS Gate 2 fechado formalmente.*
