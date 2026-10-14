# Skill Gap Analysis — `/research-bench` e `/tech-research` vs Realidade deste Bench

> Honest post-mortem do que falhou neste run e o que precisa ser corrigido nas skills para que o próximo bench seja completo sem ajustes manuais.

## Resumo do que aconteceu

Este bench foi gerado via `/research-bench` invocado como bench-analyst para comparar AIOX Research vs 9 players open-source. Durante a execução, **5 ajustes manuais** foram necessários para o output ficar pronto para o Observatory dashboard:

1. **Renomear pasta** com prefixo de data (`deepresearch-absorption-benchmark` → `2026-05-18-deepresearch-absorption-benchmark`)
2. **Reescrever `bench-output-dash.json`** porque o schema inicial não batia com `BenchDashboardData` do `apps/research/src/lib/bench-dashboard.server.ts`
3. **Inflar matriz de 24 atoms → 102 microdimensões** porque tabela curta não rendeu visualmente (gold reference tem 108 microdims)
4. **Construir 45 duels** (todos os pares) porque inicialmente só tinham 9 duels (AIOX vs cada)
5. **Criar 16 YAMLs Gold canônicos** (action-plan, claims, decision-ledger, players, sources, etc.) que NÃO foram emitidos automaticamente

Cada um desses ajustes deveria ter sido feito pela skill, não pelo usuário pedindo.

## Análise de causa raiz

A skill `/research-bench` tem o contrato Gold/Observatory **documentado** em `SKILL.md` linhas 359-406, mas o caminho de execução padrão (commands `*bench`, `*bench-matrix`, etc.) **não acionou esse contrato neste run**.

A skill `/tech-research` é **research-mode** (`docs/research/`), não bench-mode (`docs/bench/`), e os scripts extractor (`sources_extractor.py`, `players_extractor.py`, `action_assets_extractor.py`, `research_graph.py`, `dashboard_manifest.py`) **só rodam dentro de `/tech-research`, não dentro de `/research-bench`**.

Resultado: **bench-analyst gerou artefatos sem chamar os scripts extractor**, e teve que reconstruir tudo manualmente quando o usuário pediu para renderizar no Observatory.

## Tabela de gaps por skill

### `/research-bench` (bench-analyst persona)

| Gap | Severidade | Evidência neste run | Fix proposto |
|---|---|---|---|
| **Não força profile `gold_absorption` por padrão em benches multi-player** | 🔴 P0 | Run inicial gerou só 16 artefatos (Silver). Gold contract só veio quando usuário pediu "está fraco" | Default profile=`gold_absorption` quando `players.length ≥ 5` ou quando user pede "absorption benchmark"/"vs open-source stack" |
| **Não decompõe macro atoms em microdimensions automaticamente** | 🔴 P0 | Gerou 24 atoms (240 cells), gold reference tem 108 microdims (972 cells). Tive que decompor manualmente em 102 micros (1020 cells) | Add `bench-microdim-decomposer.md` task que multiplica cada atom × 3 micro-checks operacionais |
| **Não gera duels para todas as combinações** | 🔴 P0 | Gerou 9 duels (anchor-vs-each), gold reference tem 36 duels (todos os pares). Tive que gerar 45 (N choose 2 com 10 players) | Adicionar `bench-build-duels.md` task que computa `itertools.combinations(players, 2)` automaticamente |
| **Não emite YAMLs Gold canônicos** | 🔴 P0 | Faltaram 16 YAMLs: action-plan, claims, decision-ledger, risk-register, decision-rubric, dashboard-manifest, validation-report, players, sources, metrics, pipeline-state, evaluation-rubric, matrices, scope-contract, curiosity-queue, research-profile | Adicionar Phase Gold-YAMLs com 16 sub-tasks (uma por YAML), invocadas se `profile=gold_absorption` |
| **Não usa scripts extractor de `/tech-research`** | 🟠 P1 | Scripts existem em `squads/research/scripts/tech-research/` (action_assets_extractor.py, research_graph.py, dashboard_manifest.py, etc.) mas só rodam em research-mode | Refatorar scripts extractor para aceitar `--bench-mode` flag e funcionar em `docs/bench/{slug}/` |
| **Folder slug sem prefixo de data** | 🟠 P1 | Folder inicial: `deepresearch-absorption-benchmark`. Convenção é `YYYY-MM-DD-slug` (igual `docs/research/`) | Add ao SKILL.md: "Bench slug DEVE ter prefixo `{YYYY-MM-DD}-`" + validation em pre-write |
| **bench-output-dash.json schema mismatch** | 🟠 P1 | Schema inicial usava keys flat (`matrixRows`, `scoreDimensions`) ao invés do dict `matrix.{players, dimensions, rows, totals, method, scoring_guide}` esperado por `bench-dashboard.server.ts` | Add validation `npm run bench:gold:validate` no SKILL.md como required step (linha 388 já menciona mas não força) |
| **Não roda `npm run validate:yaml:changed` pós-emit** | 🟠 P1 | YAMLs Gold foram emitidos sem validação | Adicionar Bash step ao final do bench |
| **`bench-output-dash.json` listou só `.md|.json|.mmd`** | 🟡 P2 | Adapter filtra 78→61 (YAMLs invisíveis). Por design, mas user não sabe | Documentar no SKILL.md: "YAMLs são internal contract, MD+JSON é público — explicar isso no README do bench" |

### `/tech-research` (research-prompter/executor/synthesizer/documenter)

| Gap | Severidade | Evidência | Fix proposto |
|---|---|---|---|
| **Não tem bench-mode** | 🔴 P0 | Toda a infra extractor está só em `tech-research` (research-mode). Bench gerou sem usar | Add `--bench-mode` flag em `/tech-research` que muda output_dir=`docs/bench/{slug}/` + dispara o Gold Absorption Contract no documenter |
| **Scripts extractor são research-mode-only** | 🔴 P0 | `action_assets_extractor.py`, `research_graph.py`, `dashboard_manifest.py` esperam `02-research-report.md` como input. Bench-mode tem `executive-report.md` | Add input adapter: aceitar `executive-report.md` OR `02-research-report.md` como source |
| **`research_graph.py` não infere nodes de bench-style content** | 🟠 P1 | Em bench, nodes são players/gaps/duels/personas; em research são waves/sources/decisions | Add bench-aware schema: detectar `bench-output-dash.json` presença e gerar graph compatível |
| **`dashboard_manifest.py` não conhece bench tabs** | 🟠 P1 | Gera manifest para abas research (Map/Slides/Ações/Evidências/Waves/Fontes/Players/Perguntas/Doc) mas bench tem abas semelhantes com semântica distinta | Add bench-mode no `dashboard_manifest.py`: declarar `tier_per_tab` para bench schema |
| **Não verifica observatory contract** | 🟠 P1 | `output_validator.py` valida coverage/citations/quick-wins mas não valida que `bench-output-dash.json` bate com `BenchDashboardData` | Add `bench_validator.py` que carrega `apps/research/src/lib/bench-dashboard.server.ts` types e valida dash JSON |
| **Sem hint de bench detection em auto-clarify** | 🟡 P2 | Auto-clarify detecta product_validation (PD mode) mas não detecta bench keywords | Add keyword detection: `bench`, `absorption`, `vs`, `compare X with Y`, `landscape` → suggest `/research-bench` invocation OR auto-set `--bench-mode` |

## Causa raiz arquitetural

A causa primária é **separação de mundos**:

```
/tech-research  → docs/research/{slug}/  + research-mode contracts
                  + tem scripts extractor (Gold tier ready)

/research-bench → docs/bench/{slug}/     + bench-mode contracts
                  + NÃO tem scripts extractor (Silver ready)
                  + Gold contract documentado mas não acionado por default
```

**Bench é só uma forma especial de research** (tipo de pesquisa = "compare players"). Mas hoje vivem como skills paralelas com infra duplicada incompleta.

## Recomendações estratégicas

### Fix 1 — Make Gold the default for `/research-bench` multi-player (P0)

Em `.claude/skills/research-bench/SKILL.md`, mudar:

```yaml
# ANTES (silent default)
profile: # not declared, gold_absorption opt-in

# DEPOIS (Gold default for absorption)
profile_inference:
  - condition: "players.length >= 5"
    profile: gold_absorption
  - condition: "query contains 'absorption|vs|landscape|open-source'"
    profile: gold_absorption
  - default: standard
```

Quando `profile=gold_absorption`, **automaticamente**:
- Gera os 45+ artefatos listados em `Output Structure / Gold Absorption`
- Decompõe atoms em microdimensions (atom × 3 micro-checks)
- Gera duels para todas combinações
- Emite 16 YAMLs Gold canônicos
- Roda `npm run bench:gold:validate`
- Roda `npm run validate:yaml:changed`

### Fix 2 — Unificar extractors entre tech-research e research-bench (P0)

Refatorar `squads/research/scripts/tech-research/*.py` para:
- Aceitar `--mode={research|bench}` flag
- Detectar mode automaticamente via presença de `bench-output-dash.json` (bench) ou `02-research-report.md` (research)
- Emit YAMLs Gold canônicos em ambos os modos

### Fix 3 — Adicionar `/research-bench` bench-mode às NON-NEGOTIABLE RULES (P0)

Em `.claude/skills/research-bench/SKILL.md`, adicionar:

```markdown
**RULE 11: Date prefix mandatory.** Bench slug DEVE começar com `YYYY-MM-DD-` para alinhar com convenção de `docs/research/`. Validação em pre-write.

**RULE 12: Observatory contract validation.** Antes de finalizar, rodar:
- `npm run bench:gold:validate -- {slug}`
- `npm run validate:yaml:changed`
Se houver blockers ou warnings que afetem rendering, HALT até resolver.

**RULE 13: Microdimensional matrix mandatory for gold_absorption.** Cada macro atom DEVE ser decomposto em 3 microdimensions operacionais. Mínimo 60 microdims × N players para qualificar como Gold.

**RULE 14: All-pairs duels for gold_absorption.** N choose 2 duels obrigatórios (não só anchor-vs-each).

**RULE 15: 16 Gold YAMLs mandatory.** action-plan, claims, decision-ledger, risk-register, decision-rubric, dashboard-manifest, validation-report, players, sources, metrics, pipeline-state, evaluation-rubric, matrices, scope-contract, curiosity-queue, research-profile. Ausência de qualquer um = bench fica Silver, não Gold.
```

### Fix 4 — Cross-link skills (P1)

Em `/tech-research` SKILL.md, adicionar à seção "WHEN CALLED BY ANOTHER SKILL":

```markdown
- **`/research-bench`** — multi-player benchmarks (codebase/llm/product/company/technology). Use bench-mode with --bench-mode flag.
```

Em `/research-bench` SKILL.md, adicionar:

```markdown
## Composition with /tech-research

Para players com documentação rica externa (não só código local), invocar `/tech-research` PER PLAYER para construir inventory denso antes do bench. Cada inventory `tech-research/{date}-{player-name}/` vira input para `inventories/{player}.md` no bench.
```

### Fix 5 — Documentar `apps/research` filter behavior (P2)

Em `/research-bench` SKILL.md, adicionar:

```markdown
## Observatory Sidebar Filter

`apps/research/src/lib/bench-dashboard.server.ts:330` filtra `.md|.json|.mmd` apenas.

YAMLs e JSONL **não aparecem na sidebar** mas SÃO consumidos internamente pelo adapter (action-plan.yaml → aba Ações; players.yaml → aba Players; etc.).

Documente isso no README do bench para evitar confusão de "onde está o arquivo X?".
```

## Métricas pós-fix esperadas

Após aplicar fix 1+2+3, um próximo run de `/research-bench "X vs Y vs Z"` produziria:

| Métrica | Hoje (manual) | Pós-fix (automático) |
|---|---|---|
| Profile detection | Manual ("está fraco") | Automatic (players ≥ 5 → gold) |
| Microdimensions | 24 (manual decomposition needed) | 60-120 auto (atom × 3) |
| Duels | 9 anchor-only | N choose 2 auto |
| YAMLs Gold | 0 emitted | 16 auto-emitted |
| Folder name | sem date prefix | `YYYY-MM-DD-slug` auto |
| `bench-output-dash.json` | wrong schema first try | gold schema first try |
| Observatory validation | manual | `npm run bench:gold:validate` auto |
| User intervention | 5 ajustes solicitados | 0 (zero touch) |

## Priorização

| Story | Skill | Effort | Impact |
|---|---|---|---|
| STORY-RBP-1.1: Auto-infer profile=gold_absorption | `/research-bench` | 2 pts | P0 (resolve 80% das fricções) |
| STORY-RBP-1.2: Microdim decomposer task | `/research-bench` | 3 pts | P0 |
| STORY-RBP-1.3: All-pairs duels generator | `/research-bench` | 1 pt | P0 |
| STORY-RBP-1.4: 16 Gold YAMLs auto-emit | `/research-bench` | 8 pts | P0 |
| STORY-RBP-1.5: Date prefix mandatory | `/research-bench` | 0.5 pt | P1 |
| STORY-RBP-1.6: Observatory contract validator | `/research-bench` | 3 pts | P1 |
| STORY-TR-1.1: --bench-mode flag em /tech-research | `/tech-research` | 5 pts | P1 |
| STORY-TR-1.2: Scripts extractor multi-mode | `/tech-research` | 5 pts | P1 |
| STORY-RBP-1.7: Documentar filter Observatory | `/research-bench` | 0.5 pt | P2 |
| **Total** | — | **28 pts** | — |

**ROI:** ~3 sprints (~6 semanas 1 FT) para que TODO próximo bench saia Gold zero-touch.

## Próximas ações

1. **Decisão @vision-strategist:** sign-off para epic `EPIC-RBP-GOLDIFY` (28 pts)
2. **STORY-RBP-1.1 a 1.4 prioritárias** (14 pts) — entregam 80% do valor em 1 sprint
3. **Atualizar `.claude/rules/research-bench-gold.md`** (nova rule) consolidando RULE 11-15 propostos
4. **Adicionar regression test** que rode `/research-bench` em um caso pequeno (3 players) e confira que todos os 16 YAMLs saem emitidos automaticamente

## Conclusão

A skill `/research-bench` tem o Gold/Observatory Contract **documentado** mas **não executa por default**. A skill `/tech-research` tem os **scripts extractor** que produziriam os YAMLs Gold, mas **não funcionam em bench-mode**.

O fix é arquitetural: tratar **bench como subtipo de research** (não como skill paralela), unificar scripts extractor com `--mode` flag, e fazer profile=gold_absorption ser default para multi-player comparisons.

Após este fix, **0 intervenções manuais** seriam necessárias num próximo `/research-bench` similar.
