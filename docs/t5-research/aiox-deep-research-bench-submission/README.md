# AIOX Research × Deep Research Bench (HF Leaderboard)

**Status:** SCAFFOLD (run real ainda não executado)
**Created:** 2026-05-18
**Origin:** STORY-153.7 (EPIC-153 DEEP-RESEARCH-GOLDIFY)
**Leaderboard:** [Ayanami0730/DeepResearch-Leaderboard](https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard)

## Decisão

GO para preparação da submissão. NO-GO temporário para execução das 40+ tasks até sign-off de orçamento e janela operacional.

## Estado Atual

| Componente | Status |
|---|---|
| Folder canônico | ✅ Criado |
| Reprodutibilidade doc | ✅ Template pronto (preencher após pilot) |
| Script de execução | ✅ `scripts/run-deep-research-bench.sh` esqueleto |
| Caveats template | ✅ `caveats.md` template |
| Score report template | ✅ `score-report.template.json` |
| Pilot 5 tasks | ⏳ Pendente (`pilot-5-tasks.md` runbook) |
| Full run 40+ tasks | ⏳ Pendente sign-off |
| HF Spaces clone | ⏳ Pendente (run `scripts/clone-bench.sh`) |
| Submission PR | ⏳ Pendente score ≥0.40 |
| README badges | ✅ Adicionado a `apps/research/README.md` |
| Blog post draft | ✅ `outputs/copy/blog-posts/aiox-deepresearch-bench-submission.md` |

## Diretrizes Não-Negociáveis (Risk Mitigation)

1. **Pilot 5 tasks ANTES de full run** — gate crítico. Se pilot <0.40 → HALT.
2. **Provider típico de produção** — `claude-sonnet-4-6`, NÃO `claude-opus-4-7`. Honest reporting.
3. **Budget cap explícito** — meta $5-15 USD. HALT se exceder $20.
4. **Pin commit SHA** do bench em `reproducibility.md`.
5. **Submission só após score ≥0.40** verificado.

## Como Executar (quando autorizado)

```bash
# 1. Clone do bench (1x)
bash docs/bench/aiox-deep-research-bench-submission/scripts/clone-bench.sh

# 2. Pilot 5 tasks (~$1-3 USD, ~15min)
bash docs/bench/aiox-deep-research-bench-submission/scripts/run-deep-research-bench.sh --pilot 5

# 3. Avaliar pilot → se score ≥0.40, prosseguir

# 4. Full run (~$5-15 USD, ~1-2h)
bash docs/bench/aiox-deep-research-bench-submission/scripts/run-deep-research-bench.sh --full

# 5. Score report + submission PR
python3 docs/bench/aiox-deep-research-bench-submission/scripts/aggregate-scores.py
gh pr create --repo Ayanami0730/deep_research_bench ...
```

## Files

| File | Purpose |
|---|---|
| `README.md` | Este arquivo |
| `metadata.json` | Submission metadata (preenchido após run) |
| `reproducibility.md` | Como reproduzir o score |
| `caveats.md` | Honest disclosures (provider, custo, limites) |
| `score-report.json` | Score final (preenchido após run) |
| `score-report.template.json` | Schema reference |
| `task-runs/` | 1 jsonl per task executada |
| `scripts/clone-bench.sh` | Clone do HF repo |
| `scripts/run-deep-research-bench.sh` | Execução pilot + full |
| `scripts/aggregate-scores.py` | Compute final score |
| `pilot-5-tasks.md` | Runbook do pilot |

## Próximo Passo Operacional

1. **@aiox-pm:** revisar orçamento + janela operacional
2. **@aiox-devops:** clone do HF repo + setup deps
3. **@aiox-dev:** rodar pilot 5 tasks
4. **@aiox-qa:** validate pilot score ≥0.40
5. **GO/NO-GO:** prosseguir para full run OU criar improvement story
