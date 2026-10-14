# Roundtable Decision — ADR-002 Agentic Intelligence Upgrade

> **Date:** 2026-05-18
> **Mode:** decision (review-style verdict — ADR-002 já propõe decisão concreta)
> **Subject:** [ADR-002 — Agentic Intelligence Upgrade](./ADR-002-agentic-intelligence-upgrade.md)
> **Companion:** [ADR-001 — Absorption Strategy](./ADR-001-absorption-strategy.md)
> **Participants (6):** @cso, @architect, @pm, @aiox-master, @vision-chief (mapeado de @vision-strategist), @research-chief
> **Team:** `roundtable-adr002-2026-05-18` (Swarm OS mode, parallel spawn)
> **Verdict:** **APPROVE_WITH_CONDITIONS** (7,25/10)
> **Debate Rounds:** 0 (fast-path — zero conflitos substantivos)
> **Advisory Council:** Pending — anexo obrigatório para sign-off final

---

## Verdicts Summary

| Agent | Verdict | Score | Key Finding |
|---|---|---:|---|
| @cso | APPROVE_WITH_CONDITIONS | 8,0 | Atualizar `ecosystem-registry.yaml` simultâneo à deprecação do `dr-orchestrator` (Sprint E) |
| @architect | APPROVE_WITH_CONDITIONS | 7,0 | **BLOCKER**: Task tool spawn paralelo dentro de workflow YAML sem precedente — exigir SPIKE-RA-C.0 |
| @pm | APPROVE_WITH_CONDITIONS | 7,0 | **BLOCKER**: Re-score do bench (2-3 pts) fora dos 23 pts — sub-estimação |
| @aiox-master | APPROVE_WITH_CONDITIONS | 7,5 | Schema `status: dormant` precisa ser declarado antes do Sprint E + EPIC-RA pai obrigatório |
| @vision-chief | APPROVE_WITH_CONDITIONS | 7,0 | Sequencing: ADR-002 deve seguir ADR-001 Wave 1 começar; intelligence sem distribution é invisível |
| @research-chief | APPROVE_WITH_CONDITIONS | 7,0 | Sprint E PRIMEIRO + Sprint C SEGUNDO — specialists não têm I/O schemas hoje |
| **Média ponderada** | **APPROVE_WITH_CONDITIONS** | **7,25** | — |

**Quality Gate threshold (TK-RT-005 = 7,0):** ✅ PASS
**Consensus threshold (TK-RT-004 = 0,6):** ✅ 6/6 (100%) APPROVE_WITH_CONDITIONS

---

## Consolidated Findings (Deduplicated)

### BLOCKER (resolução obrigatória antes de Accepted)

**B1 — Task tool spawn paralelo dentro de workflow YAML sem precedente validado no Hub**
- Levantado por: @architect (B01) `[ARC: "execution_model_integrity"]`
- Risco: Sprint C (8 pts) produz contrato (`specialist-contracts.yaml`) que pode não ser honrável pelo executor YAML atual sem reescrita do layer de execução
- Resolução: criar **SPIKE-RA-C.0** (1 dia) para prototipar 1 specialist spawn paralelo via Task tool em phase YAML isolada, documentar resultado como evidência. Spike DESBLOQUEIA ou REFORMULA Sprint C

**B2 — Re-score do bench fora dos 23 pts (sub-estimação)**
- Levantado por: @pm (F01) `[PM: "Risk-Adjusted Estimation"]`
- Risco: AC do Sprint C cita "re-score Multi-Agente ≥ 80" que exige rodar `/research-bench` completo (16 YAMLs + N-choose-2 duels + gold_absorption profile per `research-bench-gold.md` rule) — 2-5 pts não contabilizados
- Resolução: (a) mover target de re-score para **acceptance criterion epic-level** (pós-Sprint D), e (b) **acrescentar 2-3 pts ao total** (23 → 25-26 pts) com story dedicada `STORY-RA-RESCORE.1`

### CRITICAL — Consensos (2+ agentes convergem)

**C1 — Sprint C depende de specialists com I/O schemas que não existem hoje**
- Levantado por: @research-chief (F01) + @aiox-master (F03) + @architect (H03) `[OWNER + FRAMEWORK + ARC]`
- Evidência: Sackett v1.0 (2026-02-07) ainda tem `squad: "spy"` no header; nenhum dos 5 agents (Sackett, Klein, Booth, Creswell, Forsgren) tem frontmatter com `input_schema` / `output_schema`
- Resolução: **Sprint E executa PRIMEIRO**, prepara os 5 agent files com frontmatter schemático. Sprint C inicia APÓS Sprint E entregar + após SPIKE-RA-C.0 retornar verde

**C2 — Heartbeat `cost_usd_used` é circular + token counting sem fallback explícito**
- Levantado por: @research-chief (F02) + @architect (C02) + @pm (F06) `[OWNER + ARC + PM]`
- Evidência: signal `cost_usd_used > cost_max` depende de `cost-latency.yaml` que é PRODUTO do Sprint A, não pré-requisito. Token counting tem fallback tiktoken mas sem interface declarada
- Resolução: (a) Sprint A AC reformulado em DOIS ACs — "policy declarada e schema-validada com fixture sintético" (testável imediato) + "cost signal ativo medido com run real" (validado pós-merge); (b) `coverage_calculator.py` retorna struct com `cost_confidence: exact | approximate | unavailable`; (c) heartbeat trata `unavailable` como "ignorar esse signal", não como zero

**C3 — Deprecação de `dr-orchestrator` incompleta (registry + alias + workflow refs)**
- Levantado por: @cso (C-01) + @architect (H02) + @aiox-master (F04) + @research-chief (F05) `[GOVERNANCE + ARC + FRAMEWORK + OWNER]`
- Evidência:
  - `ecosystem-registry.yaml` (§ agents, linhas 1026-1055) documenta `dr-orchestrator` como classificador de queries em UC-001~004
  - `ARCHITECTURE.md` linha 48 cita `dr-orchestrator classifies intent` como entry point Pipeline 1
  - `identity-vs-slug.md` rule exige alias entry em `outputs/qa/aliases-pending-registry.yaml` quando identity handles são depreciados
  - `wf-deep-research.yaml` referencia o agent
- Resolução: Sprint E inclui (a) `grep -r "dr-orchestrator" squads/ .claude/ docs/` para mapear consumers, (b) update simultâneo do `ecosystem-registry.yaml`, (c) alias entry no registry, (d) EDIT explícito nos workflow files

### CRITICAL — Únicos (1 agente, mas alto impacto)

**C4 — Precedência hierárquica entre `heartbeat-policy.yaml` e `quality-gates.yaml` não declarada**
- @cso (C-02) `[SOURCE: cso.md "12 dimensões — Data Governance"]`
- Resolução: ambos arquivos declaram `governed_by:` apontando para o canônico em caso de conflito (proposta: `quality-gates.yaml` é SOT macro; `heartbeat-policy.yaml` herda + especializa)

**C5 — Gap loop semântica composição vs substituição indefinida**
- @research-chief (F03) `[OWNER: "gap_set_undefined_merge_semantics"]`
- Resolução: spec explícita em Sprint B story-1 ANTES de implementar `gap_detector.py`. Recomendação: **append-only por wave** com `status` por gap; `pipeline-state.yaml` referencia gaps por ID — recovery determinístico (também adotado por @architect C01)

**C6 — Sprint C sub-estimado (8 pts → 10-12 pts realistas)**
- @pm (F02) `[PM: "Risk-Adjusted Estimation", "Critical Path Analysis"]`
- Resolução: re-estimar story-level no momento da criação de `STORY-RA-C.1/2/3`; buffer 1,5x para trabalho novo em código de pipeline

**C7 — Owner @research-chief não é dev — quem escreve código?**
- @pm (F03) `[PM: "Resource Allocation"]`
- Resolução: cada story explicitamente nomeia `@aiox-dev` (ou equivalente) como executor de código; @research-chief permanece epic owner para gating/QA

### HIGH — Consensos

**H1 — EPIC-RA pai ausente** — @cso H-01 + @aiox-master F03
> Criar `docs/stories/epic-RA-agentic-upgrade/EPIC-RA-AGENTIC-UPGRADE.md` com PRD/AC top-level **como pré-condição** de qualquer Sprint iniciar.

**H2 — Sequencing E→A paralelo→[Spike→C]→B→D ENFORCED** — @pm F05 + @research-chief Key Rec + @architect B01 + @vision-chief F01
> Sprint E **timebox hard 3 dias** como Gate 0. Sprint A em paralelo. SPIKE-RA-C.0 antes de Sprint C. Sprint C inicia somente após (E entregue ∧ Spike verde ∧ ADR-001 Wave 1 com pelo menos 1ª story em execução ativa).

**H3 — Overlap com ADR-001 Wave 1 dobra carga sem mitigação** — @pm F04 + @vision-chief F01
> Sprint C desliza 1 semana após Wave 1 do ADR-001 ter primeiro deliverable em desenvolvimento. Calendário ajustado: 5 → 6 semanas.

### HIGH — Únicos

| # | Finding | Agent | Resolução |
|---|---|---|---|
| H4 | `ide-sync sync` obrigatório pós-edit de SKILL.md (cada sprint) | @cso H-02 | AC explícito por sprint |
| H5 | `validate:squad-structure` com gate ≥ 3 files per subdir (KISS reverse) | @cso H-03 | Adicionar à AC Sprint E |
| H6 | Sprint D: `rewritten: true` + `original_claim` no schema de `claims.yaml` | @architect H01 | Adicionar à Sprint D STORY-RA-D.1 |
| H7 | KISS Gate 2 (cheaper alternative tried?) precisa resposta antes de Accepted | @aiox-master F02 | Advisory Council Contrarian responde |
| H8 | Diferenciador cost-aware invisível sem changelog público | @vision-chief F02 | Sprint A produz parágrafo de changelog em linguagem de usuário |
| H9 | Storyline ADR-001+ADR-002 = "v2 quality layer" (single narrative) | @vision-chief F03 | Documentar em release notes consolidadas |

### MEDIUM (10) — incorporar como ACs adicionais nas stories correspondentes

1. `validate:scripts-exist` para `gap_detector.py`, `specialist_dispatcher.py` — @cso M-01
2. `cost-latency.yaml` entra no Gold Observatory contract (research-bench-gold Rule 9) — @cso M-02
3. Hub-only scope declaration (fora do allowlist Hub→Spoke sync) — @aiox-master F05
4. `cost-latency.yaml` em `artifact_contracts[]` no `squads/research/config.yaml` — @aiox-master F07
5. `heartbeat-policy.yaml` schema validation no `output_validator.py` — @architect M01
6. `sinkra:rename-artifact` dry-run obrigatório antes de mover tasks/ — @architect M02
7. Spike 1 dia token counting confiabilidade — @pm F06
8. AC mensurável automatizado para Sprint B (script de classificação de queries) — @pm F07
9. Product-discovery mode herda heartbeat + gap loop? — @research-chief F06
10. Marketing-deepdive: downgrade para `status: draft` em vez de criar workflow vazio — @research-chief F07

### LOW (4) — backlog

- L1: Gilad `status: dormant` explícito na tabela do Sprint E — @cso L-01
- L2: `new_information_ratio < 0.05` threshold é heurístico — manter configurável — @architect L01
- L3: Verificar `composition-rules.yaml` aceita interpolação de phase P3.4 — @aiox-master F06
- L4: `epic-148` stories ativas — verificar não-interferência — @research-chief F08

---

## Consensus Points (2+ agentes concordam — destaque)

1. **Sequencing crítico:** Sprint E PRIMEIRO, depois A paralelo, SPIKE-RA-C.0 antes de C, Sprint C só após overlap inicial com ADR-001 Wave 1 — convergência 4 reviewers
2. **Specialists não estão prontos para contratos:** 3 reviewers convergem que Sprint C sem preparação de agent files = construir contratos sobre areia
3. **Deprecação dr-orchestrator é multi-artifact change:** 4 reviewers identificam que registry + alias + workflows precisam ser editados juntos
4. **Heartbeat cost-aware tem dependência circular operacional:** 3 reviewers exigem separar "policy declarada" de "signal ativo" em ACs distintos

---

## Decisões (mode=decision)

| # | Decisão | Resultado | Confiança |
|---|---|---|---|
| D1 | Aprovar o conceito do ADR-002 (5 sprints agenticos paralelos ao ADR-001)? | **DECIDED — SIM, com condições** | ALTA (6/6 reviewers) |
| D2 | Iniciar implementação imediatamente sem ajustes? | **DECIDED — NÃO** | ALTA (6/6 com conditions) |
| D3 | Re-estimar effort de 23 pts para 25-28 pts? | **DECIDED — SIM** | ALTA (@pm + @architect convergem na sub-estimação) |
| D4 | Sprint C antes ou depois de Sprint E? | **DECIDED — DEPOIS** | ALTA (@research-chief + @architect + @pm + @aiox-master convergem) |
| D5 | Bloquear sign-off final até Advisory Council Report? | **DECIDED — SIM** | ALTA (já documentado no ADR; @aiox-master reforça via Gate 2) |

---

## Action Plan (priorizado para sign-off)

| # | Ação | Severidade | Responsável | Quando |
|---|---|---|---|---|
| **1** | Criar `EPIC-RA-AGENTIC-UPGRADE.md` em `docs/stories/epic-RA-agentic-upgrade/` com PRD top-level | CRITICAL | @pm + @research-chief | **Pré-condição** de qualquer Sprint |
| **2** | Disparar `/advisory-council` com prompt já documentado no ADR; anexo `ADR-002-advisory-council-report.md` | BLOCKER | claude (next step) | Antes de Accepted |
| **3** | Criar `SPIKE-RA-C.0` (1 dia, 1 pt): prototipar Task tool spawn paralelo em phase YAML isolada | BLOCKER | @aiox-dev (assigned by @pm) | Antes de planejar Sprint C |
| **4** | Re-estimar total: 23 pts → 25-28 pts (incluindo SPIKE-RA-C.0 + STORY-RA-RESCORE.1 + Sprint C buffer) | CRITICAL | @pm | Update ADR seção Implementation Plan |
| **5** | Editar ADR-002 com seções: D1-D5 decisions, sequencing enforced E→A→Spike→C→B→D, struct `cost_confidence` em Sprint A spec, gap_detector.py spec append-only | CRITICAL | claude (post-roundtable) | Antes de sign-off |
| **6** | Atualizar `squads/sinkra-squad/data/process-mapping-rules.yaml`: adicionar `status: active\|dormant\|deprecated` ao schema de `agents[]` | CRITICAL | @sinkra-chief + @aiox-master | Story dedicada antes de Sprint E |
| **7** | Sprint E expandida: incluir `ecosystem-registry.yaml` sync + alias entry + workflow ref edits + grep mapeamento | CRITICAL | @aiox-dev | Sprint E story-1 |
| **8** | Declarar Hub-only scope no header do ADR-002 (fora de Hub→Spoke sync allowlist) | MEDIUM | claude (post-roundtable) | Update ADR |
| **9** | Adicionar `cost-latency.yaml` ao `artifact_contracts[]` em `squads/research/config.yaml` | MEDIUM | Sprint A story-2 | Durante Sprint A |
| **10** | Sprint A produz parágrafo de changelog público sobre cost-aware heartbeat | MEDIUM | @vision-chief + @copy-chief | Wave 1 release |

---

## Extracted Stories (novas, derivadas das condições)

| # | Story Title | Source Finding | Suggested Epic | Severity |
|---|---|---|---|---|
| `EPIC-RA-AGENTIC-UPGRADE.md` | Epic PRD pai (precondition) | H1 | epic-RA-agentic-upgrade | CRITICAL |
| `STORY-RA-PRE.1` | Schema-update process-mapping-rules: `status` field for agents | @aiox-master F01 | epic-RA-agentic-upgrade | CRITICAL |
| `SPIKE-RA-C.0` | Prototype Task tool spawn paralelo em phase YAML | B1 | epic-RA-agentic-upgrade | BLOCKER |
| `STORY-RA-RESCORE.1` | Re-score `/research-bench` Multi-Agente target ≥ 80 | B2 | epic-RA-agentic-upgrade | CRITICAL |
| `STORY-RA-E.0` | Mapear consumers de `dr-orchestrator` via grep + alias entry | C3 | epic-RA-agentic-upgrade | CRITICAL |
| (já presentes no ADR) | STORY-RA-A.1 ... STORY-RA-E.3 | — | — | — |

---

## Resolved Conflicts

Zero. Reviewers convergiram com condições complementares. Fast-path utilizado.

---

## Unresolved / Escalated

Nenhum item escalado. Quality Gate score 7,25/10 (acima do threshold 7,0).

---

## Final Verdict

**Score:** 7,25/10
**Status:** **APPROVE_WITH_CONDITIONS**
**Rounds:** 0 (fast-path, sem debate)
**Sign-off path:**

1. Editar ADR-002 com correções **derivadas das 10 ações** acima → ADR vira `Accepted-Pending-Council`
2. Disparar `/advisory-council` para steel-man cognitive diverse → anexo `ADR-002-advisory-council-report.md`
3. Sign-off formal 4/4 (@vision-strategist + @aiox-architect + @aiox-pm + @research-chief) + anexo Advisory Council = ADR `Accepted`
4. Criar EPIC + stories → enter SDC pipeline

**Pipeline Lifecycle Status:** `roundtable_complete → adr_pending_revision → advisory_council_pending → ready_for_signoff`

---

## Metrics Dashboard

| Metric | Value | Target | Status |
|---|---:|---:|---|
| Reviewers consulted | 6 | 3-7 | ✅ |
| Consensus ratio | 100% | ≥ 60% | ✅ |
| Quality gate score | 7,25 | ≥ 7,0 | ✅ |
| BLOCKER findings | 2 | resolvable | ⚠️ requer ADR revision |
| CRITICAL findings | 7 (3 consensos + 4 únicos) | resolvable | ⚠️ requer ADR revision |
| HIGH findings | 9 | absorvível em stories | ✅ |
| MEDIUM findings | 10 | AC adicionais | ✅ |
| Debate rounds | 0 | < 3 | ✅ |
| Time-to-verdict | ~2 min (parallel spawn) | n/a | ✅ |

---

## Citation Compliance Audit (per AN005 + canonical instrument reuse)

| Reviewer | Findings citados | NO-CITE | Status |
|---|---:|---:|---|
| @cso | 8/8 com `[SOURCE: ...]` | 0 | ✅ |
| @architect | 9/9 com `[ARC: ...]` | 0 | ✅ |
| @pm | 7/7 com `[PM: ...]` | 0 | ✅ |
| @aiox-master | 7/7 com `[FRAMEWORK: ...]` | 0 | ✅ |
| @vision-chief | 6/6 com `[STRAT: ...]` | 0 | ✅ |
| @research-chief | 8/8 com `[OWNER: ...]` | 0 | ✅ |
| **Total** | **45/45 cited** | **0 NO-CITE** | **✅ COMPLIANT** |

---

*Roundtable Report v1.0 | 2026-05-18 | Skill: /roundtable v2.1 Swarm OS Mode | Moderator: Claude | Persisted: `docs/bench/deepresearch-absorption-benchmark/ROUNDTABLE-REPORT-ADR-002-2026-05-18.md`*
