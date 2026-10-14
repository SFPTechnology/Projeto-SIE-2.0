# Advisory Council — ADR-002 Agentic Intelligence Upgrade

> **Date:** 2026-05-18
> **Council ID:** AC-2026-05-18-001
> **Verdict:** **PROCEED_WITH_CONDITIONS** (6,5/10)
> **Advisors:** 5/5 (Contrarian, First Principles, Expansion, Outsider, Executor)
> **Anonymization:** Heurística anti-anchoring (respostas shuffled antes da síntese)
> **Team:** `advisory-council-adr002-2026-05-18` (Swarm OS mode, parallel spawn)
> **Subject:** [ADR-002 v1.0 — Agentic Intelligence Upgrade](./ADR-002-agentic-intelligence-upgrade.md)
> **Companion:** [Roundtable Report](./ROUNDTABLE-REPORT-ADR-002-2026-05-18.md) (6 reviewers, APPROVE_WITH_CONDITIONS 7,25/10)

---

## Executive Summary (escrito ANTES da de-anonymization)

5 advisors em isolamento total convergiram em **PROCEED_WITH_CONDITIONS**. Quatro advisors (A, C, D, E) operaram com full repo access; um (B) operou com web-only access conforme Outsider Isolation Contract. Todos retornaram com lens adherence HIGH.

**Diagnóstico central:** o ADR-002 é **arquiteturalmente sólido** mas tem 2 problemas estruturais que o roundtable não capturou:

1. **Sprint C carrega 35% do esforço sem KISS Gate 2 respondido** — não foi tentada uma alternativa cheaper (10 runs A/B persona-inline vs spawn real) antes de comprometer 11 pts. Esta lacuna foi sinalizada APENAS pelo Advisor C; Advisor D confirma via raciocínio independente que "a ligação entre spawn paralelo e qualidade de claim para o usuário é inferida, não medida".

2. **Eval suite + observabilidade ausentes do plano** — sinalizado APENAS pelo Advisor B (perspectiva externa pura). Os 4 reviewers internos (A, C, D, E) aceitaram a sequência E→A→B→Spike→C→D sem questionar a ordem da indústria 2026 (eval-first, otimização-depois). Este é um **blind spot interno verificado**: groupthink reduzido pelo protocolo de isolamento.

**Convergências fortes (todos endossam):**
- Sprints A, B, D, E são sólidos e bem fundamentados
- Sprint E em 3 dias é otimista — 111 refs reais a dr-orchestrator em 4 escopos não mapeados
- Hard Gate "ADR-001 Wave 1 ativa" é subvertível sem critério git-based explícito
- SPIKE-RA-C.0 é necessário mas o plano B se vermelho não está documentado

**Divergência fundamental:**
- Advisor B (externo) diz "eval suite primeiro, depois otimização"; 4 advisors internos não veem isso.
- Advisor C ataca a assunção de que spawn paralelo melhora qualidade; D confirma via first-principles; A e E aceitam.

**Recomendação:** PROCEED com 3 condições materiais antes de Accepted. Não há razão para abandonar ADR-002 — Sprints A, B, D, E entregam valor mensurável e respondem a verdades irredutíveis do código atual. Sprint C deve ser gated por KISS Gate 2 explícito (10 runs A/B) ou tornado DEFERRED se o gate falhar.

---

## Verdict Breakdown

| Advisor (label) | Real Identity | Verdict | Confidence | Lens Adherence | Key Insight |
|---|---|---|---|---|---|
| Advisor A | expansion | THINK_BIGGER | HIGH | HIGH | `gaps.yaml` cross-session → Knowledge Debt Ledger organizacional |
| Advisor B | outsider | UNCONVENTIONAL | HIGH | HIGH | Plano otimiza motor antes de instalar painel — eval suite ausente |
| Advisor C | contrarian | APPROVED (conditional) | MEDIUM | HIGH | Sprint C = 35% do esforço, gating em Spike sem plano B documentado |
| Advisor D | first-principles | PARTIALLY_ALIGNED | MEDIUM | HIGH | Sprints A/B/D/E mapeiam 1:1 verdades primitivas; C resolve débito arquitetural, não qualidade de claim mensurada |
| Advisor E | executor | FEASIBLE_WITH_CHANGES | MEDIUM | HIGH | 111 refs reais a dr-orchestrator invalidam estimativa Sprint E 3 dias |

**Score médio:** 6,5/10 (vs 7,25 do roundtable). Diferença de -0,75 reflete o rigor adicional do framing cognitivo (Contrarian + Outsider catch coisas que domain-experts internos não veem).

---

## Consensus Points (2+ advisors concordam)

### CP-1 — Sprint E não cabe em 3 dias (Advisors C, E)
- **Evidência empírica (E):** 111 refs reais a `dr-orchestrator` em 4 escopos (squad-registry, tasks, checklists, workflows + 4 tasks com `responsavel: dr-orchestrator`). O ADR prevê ~5-10 arquivos.
- **Evidência teórica (C):** "achados extras → DEFERRED" como mitigação só funciona se aplicado agressivamente desde o dia 1; o timebox cria pressão para skip de validação.
- **Action:** explicitar no ADR que E.2 (deprecação dr-orchestrator) tem timebox de 4h hard; qualquer ref fora dos 8 arquivos listados vira story DEFERRED imediatamente.

### CP-2 — SPIKE-RA-C.0 sem plano B documentado (Advisors C, D, E)
- **C (FATAL flaw #1):** "Se Spike vermelho: ADR não define o que 'reformula' significa em effort, timeline ou escopo."
- **D:** "Sprint C representa 35% do esforço, depende de prova técnica sem fallback."
- **E:** Critério pass/fail objetivo proposto, mas plano B se vermelho falta no ADR.
- **Action:** adicionar ao ADR-002 seção "If SPIKE-RA-C.0 = vermelho": declarar Sprint C DEFERRED, publicar ADR-003 com nova estimativa pós-mudança no executor.

### CP-3 — Hard Gate ADR-001 é subvertível (Advisors C, E)
- **C (CRITICAL flaw #2):** "Em desenvolvimento ativo não tem definição operacional. Story `in_progress` por 1 hora satisfaz formalmente."
- **E (alternativa concreta):** `story.status == InProgress` OU commit em branch `feat/ADR-001-*` nos últimos 3 dias úteis. Quem decide: @research-chief via `gh pr list` / git log. Auditável.
- **Action:** substituir definição vaga por critério git-based.

### CP-4 — Sprints A, B, D, E são fundamentados (todos os 5 advisors)
- A, B, D, E mapeiam diretamente para verdades irredutíveis identificadas (D).
- O padrão é replicável cross-squad em legal/code-anatomist/copy (A).
- A indústria 2026 valida cost-aware heartbeat e gap-driven re-query como state-of-the-art (B).
- Action plan executável em 88h reais com overhead típico (E).
- **Sem ações requeridas** — proceder com confiança.

### CP-5 — Reuso cross-squad é alavanca não capturada (Advisors A, B)
- **A:** `specialist-contracts.yaml` resolve dispatch em legal (8 agentes em prosa), code-anatomist (12 shortcuts manuais), copy (tiers sem trigger). `heartbeat-policy.yaml` aplicável a design-ops, mega-brain, etl-ops.
- **B:** LangGraph Supervisor pattern adotado por Uber, LinkedIn, Replit — padrão validado.
- **Action:** adicionar AC epic-level: "Sprint C produz `squad-contract.schema.yaml` em `squads/sinkra-squad/data/` para reuso cross-squad" (story bonus, não bloqueador).

---

## Conflicts (divergências fundamentais — sinal mais valioso)

### CF-1 — Eval suite e observabilidade: primeiro vs depois

- **Posição A, C, D, E (4 advisors internos):** ordem proposta (E→A→B→Spike→C→D→RESCORE) é aceitável.
- **Posição B (1 advisor externo):** indústria 2026 coloca eval engineering como prerequisite. Sem eval suite, os 7 sinais do heartbeat não têm baseline de calibração, e citation adaptativo não tem regressão para validar melhorias. Gartner: 40% dos projetos agentic cancelados até 2027 por falta de eval/observabilidade. Sources: arxiv 2604.02988, siliconangle.com/2026/05/17.

**Resolução:** **Advisor B está certo materialmente.** Os 4 advisors internos aceitam a sequência por familiaridade com o codebase, mas a indústria externa sinaliza inversão crítica. **Action:** adicionar ao ADR-002 um **Sprint 0 / pre-Sprint A** de **2 pts (1-2 dias)**: instrumentação básica de `cost-latency` + `tool-call counters` + `eval suite skeleton` ANTES de Sprint A começar. Sem isso, AC-A2 ("cost signal ativo validado com run real") é não-falsificável.

### CF-2 — Sprint C resolve: arquitetura ou qualidade do claim?

- **Posição A, E:** débito arquitetural a resolver (declared agents nunca invocados). Action plan executável.
- **Posição C, D:** salto de "nunca invocados" para "Multi-Agente 57,5 → 80+" não tem evidência empírica. KISS Gate 1 falha sem 10 runs A/B medindo delta de qualidade.

**Resolução:** **Posição C/D é mais rigorosa.** Sprint C resolve uma assimetria real (declared vs executed), mas o sucesso medido em score arquitetural não captura o que o usuário recebe. **Action:** antes de comprometer Sprint C, executar **STORY-RA-EXP.1** (experimento de 2 pts): 10 runs de `/tech-research` com fixtures históricas, 5 com inline persona-fidelity, 5 com spawn manual (via Task tool ad-hoc). Comparar qualidade de output via rubric humana ou LLM-judge. Se delta < 10% → Sprint C vira DEFERRED. Se ≥ 10% → Sprint C procede com KISS Gate 1 fechado.

### CF-3 — Specialists dormentes: housekeeping ou design signal?

- **Posição B:** literatura LangGraph 2026 diz que agents dormentes geralmente indicam **routing bug**, não specialists desnecessários. Recomenda route-accuracy evaluators ANTES de deprecar.
- **Posição A, C, D, E:** aceitam Sprint E como cleanup mecânico.

**Resolução:** **B levanta ponto válido mas não conclusivo.** Não há evidência de que os 6 agents dormentes do squad research representem bug de routing vs. specialists genuinamente desnecessários. **Action:** Sprint E não deleta specialists — apenas marca `status: dormant`. Isso preserva a capacidade latente. Adicionar AC epic-level: "Pós-Sprint C, executar route-accuracy check: 3 fixtures com triggers explícitos dos 5 specialists. Se nenhum specialist for invocado quando deveria → bug de routing identificado, não cleanup necessário."

---

## Unique Insights (findings de apenas 1 advisor — alto valor)

| # | Insight | Advisor | Por que importa |
|---|---|---|---|
| UI-1 | **Gap Marketplace / Knowledge Debt Ledger:** `gaps.yaml` cross-session vira ativo organizacional compartilhado entre operadores e squads | A (expansion) | Transforma cada pesquisa em contribuição cumulativa. ROI exponencial vs incremental. |
| UI-2 | **Cost-Bounded SLAs como produto B2B:** `cost-latency.yaml` habilita pricing por run com budget contract — único no mercado | A | Possibilita modelo de billing granular, abre vertical B2B. |
| UI-3 | **Gartner: 40% dos projetos agentic cancelados até 2027 por falta de eval suite** | B (outsider) | Implicação direta para risco-de-execução do ADR. Eval engineering é o gap crítico da indústria 2026. |
| UI-4 | **10 runs A/B persona-inline vs spawn real** como KISS Gate 1 falsificável | C (contrarian) | Operacionaliza KISS rule com critério empírico, não conceitual. |
| UI-5 | **Verdade irredutível #7:** `wf-deep-research.yaml` é aspiração; SKILL.md é realidade — dois mundos paralelos no código | D (first-principles) | O ADR deveria explicitar que está consolidando aspiração e realidade num único mundo. |
| UI-6 | **111 refs reais a dr-orchestrator** em 4 escopos não mapeados (squad-registry linha 2319, 4 tasks com `responsavel:`, checklists, workflows) | E (executor) | Número empírico que dimensiona Sprint E corretamente. |

---

## Expansion Opportunities (Advisor A)

Capturadas como **stories pós-roadmap-base** (não bloqueiam ADR-002 atual):

| # | Opportunity | Effort | Impact | Time Horizon |
|---|---|---|---|---|
| 1 | Gap Marketplace / Knowledge Debt Ledger | M | ALTO | 6-12 meses |
| 2 | Cost-Bounded SLAs externos (B2B) | M | MUITO ALTO | 12 meses |
| 3 | `squad-contract.schema.yaml` cross-squad | L | MUITO ALTO | 6-9 meses |
| 4 | Gap Genealogy / Lineage como auditoria epistêmica | M | ALTO | 9-15 meses |
| 5 | `heartbeat-policy.schema.yaml` cross-squad | M | ALTO | 6-9 meses |
| 6 | Predictive Budget / Budget Forecaster | L | ALTO | 12-18 meses |

**The 10x Version (Advisor A):** Knowledge Debt Ledger compartilhado entre todos os operadores + Agent Capability Registry Hub-wide. Transforma Hub de "coleção de squads isolados" em "sistema multi-agente verdadeiramente integrado".

---

## External Perspective (Advisor B — outsider_status: nominal)

### Fontes citadas (verificáveis)
- Self-Optimizing Multi-Agent Systems for Deep Research — arxiv.org/pdf/2604.02988
- Best AI Deep Research Tools 2026 — awesomeagents.ai/tools/best-ai-deep-research-tools-2026
- Eval engineering: The missing piece of agentic AI governance — siliconangle.com/2026/05/17
- DeepResearch Bench II — github.com/Ayanami0730/deep_research_bench

### Industry comparison

| Approach | Used By | Pros | Cons |
|---|---|---|---|
| Multi-signal heartbeat | A2RAG, POLARIS | Elimina loops infinitos, cost explosions | Cada sinal precisa de threshold calibrado |
| Gap-driven re-query persistente | OpenResearcher, DeerFlow | Reduz redundância, foco cirúrgico | Requer schema robusto + deduplication semântica |
| Specialist spawn paralelo | LangGraph Supervisor (Uber, LinkedIn, Replit) | Throughput, separação concerns | State schema "ages worst" com 10+ nodes |
| Citation verify per-claim com archive | Padrão emergente | Gold standard | Custo de latência por claim surpreendente |

### Red Flags (4 identificadas)
1. **Eval suite ausente** — diferencial competitivo #1 da indústria 2026
2. **Observabilidade não é sprint dedicado** — playbook 2026 unânime: instrumentar antes de otimizar
3. **6/14 agents nunca invocados pode ser design signal** — não housekeeping; route-accuracy evaluators ANTES de deprecar
4. **31 pts / 6 semanas otimista** para 1 FT vs benchmarks SP2T e AI4Agile Practitioners Report 2026

---

## Action Plan (refinado pelo Team Lead)

### Pré-conditions para Accepted (ADICIONADAS pelo Advisory Council)

1. **NOVO: Sprint 0 — Eval Suite Skeleton (2 pts, 1-2 dias)** — antes de Sprint A:
   - Instrumentação básica de `cost-latency` + `tool-call counters`
   - `eval-suite/` skeleton com 3 fixtures históricas + rubric humana ou LLM-judge stub
   - Resolve CF-1 (eval-first inversion da indústria 2026)
   - Origem: Advisor B

2. **NOVO: STORY-RA-EXP.1 — KISS Gate 1 falsificável (2 pts, 1 dia)** — antes de SPIKE-RA-C.0:
   - 10 runs A/B (5 inline persona-fidelity vs 5 spawn manual)
   - Critério: delta de qualidade ≥ 10% via LLM-judge → Sprint C procede; < 10% → DEFERRED
   - Resolve CF-2 (Sprint C arquitetura vs qualidade) + KISS Gate 1
   - Origem: Advisor C

3. **NOVO: Critério git-based para Hard Gate ADR-001** — substituir definição vaga:
   - `story.status == InProgress` OU commit em branch `feat/ADR-001-*` nos últimos 3 dias úteis
   - Quem decide: @research-chief via `gh pr list` / git log
   - Resolve CP-3
   - Origem: Advisor E

4. **NOVO: Plano B documentado se SPIKE-RA-C.0 vermelho:**
   - Sprint C declarado DEFERRED
   - ADR-003 com nova estimativa pós-mudança no executor
   - Sprints A+B+D+E entregam valor autônomo (delta esperado: re-score +6 pts mesmo sem C)
   - Resolve CP-2
   - Origem: Advisors C, D, E

### Re-estimativa pós-Advisory Council

| Item | ADR v1.0 (post-roundtable) | ADR v2.0 (post-advisory) | Justificativa |
|---|---:|---:|---|
| Sprint 0 (NEW — eval suite skeleton) | — | 2 | CF-1 (Advisor B + Gartner 2027 risk) |
| STORY-RA-EXP.1 (NEW — A/B persona vs spawn) | — | 2 | CF-2 (Advisors C+D + KISS Gate 1) |
| Pré-conditions | 2 (PRE.1 + EPIC.md) | 2 | — |
| Sprint E | 3 | 3 (timebox rígido + DEFERRED escape) | Mantido com mitigação |
| Sprint A | 5 | 5 | — |
| Sprint B | 5 | 5 | — |
| SPIKE-RA-C.0 | 1 | 1 | — |
| Sprint C (condicional ao EXP.1 + SPIKE) | 11 | 11 (pode virar 0 se DEFERRED) | — |
| Sprint D | 3 | 3 | — |
| STORY-RA-RESCORE.1 | 2 | 2 | — |
| **Total worst case** | **31** | **35 pts** | +4 pts (Sprint 0 + EXP.1) |
| **Total se Sprint C DEFERRED** | n/a | **24 pts** | -7 pts (sem C, com EXP.1 falsificando) |

**Calendário ajustado:** 6 → 6,5 semanas worst case (1 FT); 4,5 semanas se Sprint C DEFERRED.

---

## KISS Gate 2 Explicit (responde @aiox-master F02 do roundtable)

**Pergunta:** "Foi tentada alternative cheaper antes de comprometer estrutura nova?"

**Resposta consolidada (Advisory Council):**

| Sprint | Cheaper alternative existe? | Foi documentada como tentada? | Status |
|---|---|---|---|
| Sprint 0 (Eval suite — NEW) | N/A | N/A — é o cheaper baseline | ✅ Self-evident |
| Sprint A (heartbeat) | Sim — single-signal coverage + adicionar APENAS cost-latency primeiro | Não, mas Sprint 0 cobre o spike. | ✅ Resolvido via Sprint 0 |
| Sprint B (gap loop) | Não | N/A | ✅ Gate 1 + 2 ambos OK |
| STORY-RA-EXP.1 (NEW) | N/A | N/A — é o cheaper test | ✅ Falsifica Sprint C antes de comprometer |
| Sprint C (specialists) | **Sim — inline persona-fidelity** | **Não — gap original** | ⚠️ Resolvido via EXP.1 |
| Sprint D (citation) | Não | N/A | ✅ |
| Sprint E (cleanup) | N/A — é KISS por definição | N/A | ✅ |

**Conclusão:** Com Sprint 0 + STORY-RA-EXP.1 adicionados, **KISS Gate 2 fecha**. Sprint C deixa de ser comprometido cegamente — torna-se condicional ao EXP.1 verde.

---

## De-anonymization

Para auditoria. Reveladas após blind synthesis acima:

| Label | Real Identity | Color |
|---|---|---|
| Advisor A | **expansion** | green |
| Advisor B | **outsider** | orange |
| Advisor C | **contrarian** | blue |
| Advisor D | **first-principles** | purple |
| Advisor E | **executor** | yellow |

Distribuição de verdicts pós-de-anonymization confirma robustez: nenhum advisor é outlier solitário — todas as posições têm pelo menos 1 confirmação cruzada, exceto Advisor B (eval-first), que é precisamente o ponto onde o protocolo Outsider entrega valor único.

---

## Final Verdict

**PROCEED_WITH_CONDITIONS** (6,5/10)

### Conditions para Accepted

1. **Adicionar Sprint 0** (Eval Suite Skeleton, 2 pts) antes de Sprint A — resolve CF-1 (eval-first)
2. **Adicionar STORY-RA-EXP.1** (A/B persona vs spawn, 2 pts) antes de SPIKE-RA-C.0 — resolve CF-2 e KISS Gate 1
3. **Substituir Hard Gate vago por critério git-based** — resolve CP-3
4. **Documentar plano B se SPIKE-RA-C.0 vermelho** (Sprint C → DEFERRED, ADR-003) — resolve CP-2
5. **Adicionar AC epic-level** para route-accuracy check pós-Sprint C (resolve CF-3 sem bloquear)
6. **Re-estimativa final:** 35 pts worst case, 24 pts se Sprint C DEFERRED via EXP.1

### Rationale

Sprints A, B, D, E têm fundamentação sólida (4 advisors confirmam). Sprint C tem fundamentação inferida — não medida — e a indústria 2026 sinaliza inversão crítica de prioridade (eval-first). Com as 5 condições, o ADR-002 v2.0 corrige groupthink interno detectado e fecha KISS Gate 2 formalmente.

### Next step

Editar ADR-002 v1.0 → v2.0 incorporando as 5 condições. Após edit, ADR move de `Proposed (conditions pending)` → `Accepted` quando 4/4 deciders nomeados assinarem + este Advisory Council Report anexado.

---

## Lineage

- **Bench source:** `docs/bench/deepresearch-absorption-benchmark/` (96 artefatos, 18 repos decoded)
- **Roundtable:** `ROUNDTABLE-REPORT-ADR-002-2026-05-18.md` (6 reviewers, 7,25/10)
- **Advisory Council:** este relatório (5 advisors, 6,5/10)
- **Net rigor adicional:** -0,75 pts de score = catch de blind spots não-detectáveis por domain experts internos

---

*Generated by Advisory Council skill v1.0*
*Anonymization: respostas shuffled antes da síntese (heurística anti-anchoring)*
*Outsider Isolation Contract: cumprido (web-only access, ≥ 2 fontes externas citadas)*
*Persisted: `docs/bench/deepresearch-absorption-benchmark/ADR-002-advisory-council-report.md`*
