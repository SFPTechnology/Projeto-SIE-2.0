# Quality Audit — Deepresearch Absorption Benchmark

> Self-audit do bench segundo as 4 dimensões de excelência identificadas pelo founder em `docs/research`.

## 4 Dimensões de Excelência (founder feedback)

### Dimensão 1 — Estado Investigativo Vivo (Research OS)

> "A melhor pesquisa mantém um modelo vivo da investigação: missão, escopo, decomposição, perguntas abertas, claims, evidências, lacunas, crítica, decisão, próximos passos."

**Source benchmark:** `2026-05-06-tech-research-pipeline-improvements` (43 arquivos, 14 waves, 64 nós / 66 edges)
**Best artifact:** `14-autonomous-researcher-operating-system.md`

**Este bench compliance:**

| Componente | Tem? | Onde |
|---|---|---|
| Mission contract | ⚠️ Implícito | `metadata.json` |
| Scope contract | ❌ Falta | — |
| Decomposition matrix | ⚠️ Parcial | `gap-analysis.json` (10 gaps) |
| Curiosity queue | ❌ Falta | — |
| Gap findings | ✅ | `gap-analysis.json/md` |
| Critique report | ⚠️ Parcial | `executive-report.md` honest gaps |
| Claim graph | ⚠️ Parcial | `deep/evidence-strength-map.json` (42 claims) |
| Decision ledger | ⚠️ Parcial | `deep/absorption-decision-table.md` |
| Next actions | ✅ | `absorption-roadmap.md` + `story-ready-backlog.md` |

**Score:** **6/10** — falta scope-contract, curiosity-queue, critique-report-formal.

### Dimensão 2 — Dashboard Contract (não texto bom)

> "Uma pesquisa pode ser ótima em texto e ruim no dashboard se não preencher artefatos consumidos."

**Source benchmark:** `2026-05-17-codex-full-sdc-orchestration` (11/11 artefatos Gold, score 100, 88 nós / 188 edges)

**Este bench compliance:**

| Artefato Gold (codex full-sdc) | Tem? |
|---|---|
| `research-profile.yaml` | ❌ |
| `action-plan.yaml` | ❌ |
| `claims.yaml` | ❌ |
| `decision-ledger.yaml` | ❌ |
| `risk-register.yaml` | ⚠️ Tenho JSON, falta YAML format |
| `research-graph.json` | ❌ |
| `decision-rubric.yaml` | ❌ |
| `dashboard-manifest.yaml` | ❌ |
| `validation-report.yaml` | ❌ |
| `players.yaml` | ❌ (tenho como inventory-open-source-stack.json) |
| `matrices.yaml` | ❌ (tenho como comparison-matrix.json) |

**Score:** **2/11** — gap massivo no dashboard contract. **TODO crítico.**

### Dimensão 3 — Rubrica Própria + Transparência de Avaliação

> "O sistema precisa exigir transparência de avaliação, não uma avaliação fixa."

**Source benchmark:** `2026-05-16-quais-os-melhores-projetos-de-deepresearch-opensource-atuais`
**Best artifact:** `06-gold-evaluation-rubric.yaml` (dimensões + pesos + presets + gates)

**Este bench compliance:**

| Item | Tem? | Onde |
|---|---|---|
| Dimensões customizadas | ✅ | `comparison-matrix.json#groups` (13 grupos) |
| Pesos transparentes | ✅ | `comparison-matrix.json#groups.weight` + `comparison-matrix.md` |
| Scenario presets | ✅ | `scenario-scorecards.json` (8 cenários com weights_override) |
| Must-pass gates | ⚠️ Parcial | `contracts/qa-rubric.json` |
| Persona weights | ✅ | `deep/persona-weight-methodology.json` (4 personas) |
| Methodology disclosure | ✅ | `comparison-matrix.md` final section + `deep/persona-weight-methodology.md` |

**Score:** **8/10** — quase Gold. Faltam `bench-contract.json` formal + gates documentados como YAML.

### Dimensão 4 — Actionability (decisão sem owner é opinião)

> "Recomendação sem owner, alvo e tempo de valor ainda é só opinião bem escrita."

**Source benchmark:** `2026-05-17-anthropic-growth-solo-playbook` (`action-plan.yaml` exemplar)

**Padrão a absorver:**
- `decision.summary`
- `actions[].owner`
- `actions[].target_hub`
- `actions[].time_to_value`
- `actions[].deliverable`
- `roadmap_phasing`
- `blocked_by`

**Este bench compliance:**

| Item | Tem? | Onde |
|---|---|---|
| Decision summary | ✅ | `executive-report.md` TL;DR |
| Owners por gap | ⚠️ Parcial | `deep/absorption-decision-table.md` |
| Target hubs | ⚠️ Parcial | `deep/open-source-to-sinkra-map.md` |
| Time-to-value | ⚠️ Parcial | `absorption-roadmap.md` weeks per wave |
| Deliverable per action | ✅ | `story-ready-backlog.md` per-story acceptance |
| Roadmap phasing | ✅ | `absorption-roadmap.md` |
| Blocked_by relationships | ✅ | `dependency-graph.md` |

**Score:** **6/10** — bons elementos mas não consolidados em `action-plan.yaml` formal.

## Overall Quality Score (este bench)

| Dimensão | Score |
|---|---:|
| 1. Research OS (estado investigativo vivo) | 6/10 |
| 2. Dashboard Contract (artefatos consumíveis) | 2/11 |
| 3. Rubrica Própria + Transparência | 8/10 |
| 4. Actionability (decisão com owner+target+time) | 6/10 |
| **Total** | **22/41 ≈ 54%** |

## TODO para Premium Iteration

Para chegar a Gold (≥80%), TODO:

### Premium TODO 1 — Dashboard Contract (high priority)

Criar:
- `research-profile.yaml` — Profile do bench
- `action-plan.yaml` — 9 ações com owner+target+time-to-value+deliverable
- `claims.yaml` — Claim graph estruturado (extract from `deep/evidence-strength-map.json`)
- `decision-ledger.yaml` — Decisões + alternativas + sign-off
- `dashboard-manifest.yaml` — Mapeia bench files para Observatory consumption
- `validation-report.yaml` — Self-validation do bench
- `players.yaml` — Players (refactor de `inventory-open-source-stack.json` para YAML)
- `matrices.yaml` — Matrix em YAML (refactor de `comparison-matrix.json`)
- `risk-register.yaml` — Refactor JSON → YAML
- `research-graph.json` — Graph dos players + relations (lineage from `deep/intelligence-graph.md`)
- `bench-contract.json` — Contrato local agnóstico

### Premium TODO 2 — Research OS

Criar:
- `scope-contract.yaml` — Boundaries + non-goals
- `curiosity-queue.yaml` — Perguntas abertas pendentes (e.g. "DeerFlow TIAMAT implementation details", "OpenResearcher reproducibility")
- `decomposition-matrix.yaml` — Como o problema foi decomposto em 9 gaps
- `critique-report.md` — Self-critique (bias, gaps de método, sample size)

### Premium TODO 3 — Bench Contract Local

Criar `bench-contract.json`:

```json
{
  "schema": "bench-contract.v1",
  "type": "absorption-benchmark",
  "decision_improved": "Should AIOX absorb features from open-source deep research?",
  "categories": ["framework-multiagent", "single-loop", "model-trained", "local-first"],
  "dimensions": [...],
  "evaluation_method": "weighted-multi-dim with persona overrides",
  "rubric_ref": "comparison-matrix.json#groups",
  "expected_sources": ["github clone", "README", "paper", "HF model card"],
  "stop_rules": {"max_players": 10, "max_dimensions": 30},
  "completeness_criteria": {"inventories_per_player": "required", "scoring_disclosed": "required"},
  "required_artifacts": ["metadata.json", "inventory-*.json/md", "comparison-matrix.json/md", "scorecard.json/md", "gap-analysis.json/md", "executive-report.md", "battle-card.md", "ADR-001.md"]
}
```

## Verdict

Este bench está em **54% (silver/bronze)**. Para chegar a Gold (≥80%), Premium Iteration agora vai criar os artefatos listados nos 3 TODOs acima.
