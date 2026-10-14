# Prior-Art Search — Wave 3 Slides Creator Absorption

Data: 2026-05-18
Origem: bench `slides-creator-open-source-absorption` v1.5 → execução Wave 3 (F1-F5)
Owner: @aiox-architect + @aiox-pm (handoff via /aiox-pm)
Regra: `.claude/rules/prior-art-search.md` + `.claude/rules/ids-principles.md` (REUSE > ADAPT > CREATE)

## Sumário Executivo

**Veredito:** das 5 frentes propostas no diagnóstico (F1 Renderer, F2 Runtime, F3 Reflection, F4 Editor, F5 Design 100), **3 podem reusar primitivos existentes** e **2 são CREATE legítimos**.

| Frente | Decisão | Justificativa |
|---|---|---|
| F1 Native PPTX Renderer | **CREATE** | Nenhum equivalente em `packages/`, `services/`, `apps/`. `apps/open-design/skills/pptx` é apenas stub apontando upstream. |
| F2 Runtime CLI/API/MCP | **REUSE + CREATE** | REUSE `apps/squad-engine` (Fastify+tRPC+Inngest) para REST; REUSE padrão `packages/ds-mcp` (McpServer SDK) para MCP. CREATE novas rotas `/slides/*` e novo package `slides-mcp`. |
| F3 Planning/Reflection | **ADAPT** | Squad já tem `design-planner` agent e `planning-reflection.jsonl` no contrato — só falta materialização executável e adapter PPTEval. |
| F4 Editor (prompt-to-edit) | **CREATE** (CLI-first) | Nenhum editor existente. Wait F1+F2 antes; entra como módulo CLI no `slides-core` package. |
| F5 Design 100 | **ADAPT** | Skill já tem `design-mastery-contract.yaml`, `key-slide-render-review.yaml`, `visual-regression-checklist.yaml`. Falta integração executável com render real (F1). |

## Buscas Executadas

### Search 1 — Render PPTX

| Claim | Search | Matches | Verdict |
|---|---|---:|---|
| `pptxgenjs` ou similar usado no repo | `grep -r "pptxgenjs\\|python-pptx\\|officegen" --include="*.json" --include="*.ts" --include="*.js"` excluindo node_modules | 4 (todas em `docs/bench/`) | **CONFIRMED_ABSENT** em produção. Apenas referências no bench. |
| Diretório `pptx` ou `slides-renderer` | `find . -type d -name "pptx*" -o -name "slides-renderer"` | 4 (`apps/open-design/skills/pptx` stub; `.claude/skills/slide-creator`; `.codex/skills/slide-creator`; `.agents/skills/slide-creator`) | **PARTIAL_MATCH**: apenas stubs/skill contratual. Sem motor real. |
| Skill `pptx` de Anthropic local | `cat apps/open-design/skills/pptx/SKILL.md` | 1 stub apontando para `github.com/anthropics/skills/tree/main/pptx` | **CONFIRMED_ABSENT** localmente. Referência remota não vendored. |

**Decisão F1:** CREATE `packages/@sinkra/slides-renderer/` — não existe nada no repo. Fonte de absorção: `../bench/ppt-master` (Apache/permissivo, conferir LICENSE) + `../bench/powerpoint-skill`.

### Search 2 — API/CLI/MCP runtime

| Claim | Search | Matches | Verdict |
|---|---|---:|---|
| Fastify API com rotas executáveis | `ls apps/*/src/routes/` + `cat apps/*/src/server.ts \| head` | `apps/squad-engine/src/routes/rest/*.route.ts` (artifacts, context, executor, health, internal, process, tasks); `apps/gateway-ai/src/routes/*.route.ts` (complete, embed); ambos Fastify+pino+zod | **FOUND_REUSE**: squad-engine já é Fastify+tRPC+Inngest+Redis+Supabase, padrão maduro. |
| MCP server scaffold | `find . -name "mcp-server.*" -not -path "node_modules"` + `cat packages/ds-mcp/src/index.ts` | `packages/ds-mcp` (McpServer + StdioServerTransport + handlers padronizados); `packages/core/memory/mcp-server.cjs`; `squads/design-ops/scripts/extract-from-url/mcp-server.cjs` | **FOUND_REUSE**: `packages/ds-mcp` é o template canônico. Padrão `index.ts` + `handlers/*.ts` + `data/*.ts` + bin no package.json. |
| CLI Node convencional | `find . -name "cli.ts" -o -name "cli.js" -path "*/scripts/*"` | scripts variados em `squads/*/scripts/`, `scripts/sinkra/*.js`, `packages/ds-mcp/bin` | **FOUND_REUSE**: padrão `bin: { "ds-mcp": "./dist/index.js" }` no package.json + Node 18+. |
| Provider routing (BYOK/Ollama/dummy) | `find . -name "llm-router*" -o -name "providers.*" -not -path "node_modules"` | `apps/squad-engine/src/engine/llm-router.js`, `llm-config-loader.js`, `providers.js`; `services/llm-router/`; `apps/gateway-ai/src/lib/router.ts` | **FOUND_REUSE**: provider abstraction já existe (squad-engine LLM router + dedicated service). Wrap, não recriar. |
| Worker async + jobs | `find apps -name "worker*" -o -name "queue*"` | `apps/squad-engine/src/queue/jobs.js`, `worker.js`; usa Inngest + Redis BullMQ | **FOUND_REUSE**: padrão de job async já existe. |

**Decisão F2:**
- **REUSE** `apps/squad-engine` infra (Fastify, Inngest, Redis, Supabase, LLM router). Adicionar 3 novas rotas em `apps/squad-engine/src/routes/rest/`: `slides-generate.route.ts`, `slides-review.route.ts`, `slides-export.route.ts`.
- **REUSE** padrão `packages/ds-mcp` para CREATE `packages/@sinkra/slides-mcp`. Mesma estrutura (index.ts + handlers + data + bin).
- **CREATE** `scripts/sinkra/slides-cli.js` invocando o mesmo core via HTTP local (port 3500) ou import direto do package `@sinkra/slides-core`.
- **CREATE** `packages/@sinkra/slides-core` para o pipeline compartilhado entre CLI/API/MCP (briefing → deckspec → IR → render).

### Search 3 — Planning/Reflection (PPTEval)

| Claim | Search | Matches | Verdict |
|---|---|---:|---|
| Agent design-planner já existe | `cat squads/slides-creator/agents/design-planner.md` | 1 (tier_2, MSN-2026 critique loop) | **FOUND_REUSE**: agent existe e está cadastrado no config.yaml. |
| Contrato planning-reflection.jsonl | `grep -r "planning-reflection" squads/slides-creator/` | múltiplas (output schema, workflow phase P04_5) | **FOUND_REUSE**: contrato existe, só falta materialização runtime. |
| Tasks de critique loop | `ls squads/slides-creator/tasks/ \| grep -E "critique\|revis\|design-direction"` | 4 (compress-outline-to-slide-functions, define-design-direction, run-design-critique, apply-design-revision) | **FOUND_REUSE**: tasks completas. |
| Rubricas QA tipo PPTEval | `grep -r "PPTEval\|GAD\|Coherence" squads/slides-creator/` + `cat squads/slides-creator/data/qa-rubric.yaml` | múltiplas no config.yaml + checklists | **PARTIAL**: rubricas listadas, mas não executáveis como validators automatizados. |

**Decisão F3:** ADAPT — squad já tem 80% do trabalho. Falta:
- Adapter Python/TS que recebe deck-spec + render preview e roda scoring numérico pelas 4 lentes (vision/content/coherence/GAD)
- Persistir `planning-reflection.jsonl` por execução real (filesystem write durante run)
- Linkar critique-report.yaml ao diff de deck-spec.yaml com before/after

Fonte de absorção: `../bench/PPTAgent` (MIT — código copiável).

### Search 4 — Editor prompt-to-edit

| Claim | Search | Matches | Verdict |
|---|---|---:|---|
| Editor visual web no repo | `find apps -name "editor*"` | `apps/storybook` (component dev), `apps/design`, `apps/aiox-squad-design` (DS preview); nenhum slide editor | **CONFIRMED_ABSENT** para edit-slides UX. |
| Diff/patch utilities | `grep -r "diff\\|patch" packages/ --include="package.json"` | `unified` em `packages/@sinkra/engine-core` | **PARTIAL_MATCH_ADAPT**: dependência genérica disponível, sem implementação slide-aware. |
| Histórico/undo de DeckSpec | nenhum | 0 | **CONFIRMED_ABSENT** |

**Decisão F4:** CREATE — CLI-first (`slides:edit --target T --intent I --diff`). Adiar UI para Wave 4. Implementação dentro de `packages/@sinkra/slides-core`. Fonte: `../bench/presentation-ai` (MIT) padrões de outline editor; banana-slides apenas como inspiração comportamental (AGPL — não copiar código).

### Search 5 — Design 100 + brand fidelity

| Claim | Search | Matches | Verdict |
|---|---|---:|---|
| design-mastery-contract.yaml na skill | `ls .claude/skills/slide-creator/templates/visual/design-mastery-contract.yaml` | 1 | **FOUND_REUSE** |
| brand-template-manifest existe | `ls .claude/skills/slide-creator/templates/visual/brand-template-manifest.yaml` | 1 | **FOUND_REUSE** |
| key-slide-render-review | `ls .claude/skills/slide-creator/templates/visual/key-slide-render-review.yaml` | 1 | **FOUND_REUSE** |
| visual-regression-checklist | `ls .claude/skills/slide-creator/templates/visual/visual-regression-checklist.yaml` | 1 | **FOUND_REUSE** |
| Brand systems patterns | `ls .claude/skills/slide-creator/templates/visual/brand-system-patterns.yaml + aiox-brandbook-deep-patterns.yaml + redpine-deep-patterns.yaml` | 3 | **FOUND_REUSE** |
| validate_design_mastery.py | `ls .claude/skills/slide-creator/scripts/validate_design_mastery.py` | 1 | **FOUND_REUSE** |

**Decisão F5:** ADAPT — contratos e validators existem. Falta integração executável com render real (depende de F1) e materialização do `design-mastery-report.yaml` por execução. Sem CREATE.

## Side-effect: Stubs órfãos

`apps/open-design/skills/pptx/SKILL.md` é um stub que aponta para `github.com/anthropics/skills/tree/main/pptx`. Não é canônico e não tem implementação. Quando F1 entregar, marcar este stub como `archive_recommended: true` ou substituir por reference que aponta para `packages/@sinkra/slides-renderer`. Decisão fica com `@devops`.

## Componentes Identificados para REUSE (resumo)

| Componente | Local | REUSE em |
|---|---|---|
| Fastify+pino+zod stack | `apps/squad-engine` + `apps/gateway-ai` | F2 (rotas /slides/*) |
| MCP scaffold template | `packages/ds-mcp/src/index.ts` + `handlers/*` | F2 (slides-mcp) |
| Inngest async jobs + Redis | `apps/squad-engine/src/queue/` | F2 (export jobs) |
| LLM router multi-provider | `apps/squad-engine/src/engine/llm-router.js` + `services/llm-router/` | F2 (BYOK/Ollama/dummy) |
| Supabase client | `apps/squad-engine/src/lib/supabase.js` | F2 (workspace persistence) |
| Engine DAG (Kahn topological sort) | `packages/@sinkra/engine-dag` | F3 (planning DAG) |
| Engine governance (gates, proof chain) | `packages/@sinkra/engine-core` | F3 (release veto) |
| design-planner agent + 4 critique tasks | `squads/slides-creator/agents/design-planner.md` + `tasks/run-design-critique.md`, etc | F3 (materializar runtime) |
| Skill design-mastery contracts (8 YAMLs) | `.claude/skills/slide-creator/templates/visual/` | F5 (executar contra render real) |
| validate_design_mastery.py | `.claude/skills/slide-creator/scripts/` | F5 (integrar com render output) |

## Componentes CREATE Justificados (gates G1-G6)

### CREATE-1: `packages/@sinkra/slides-renderer`

- G1 Existe? NÃO — único stub é `apps/open-design/skills/pptx` (não implementado)
- G2 Funciona? n/a
- G3 Adaptável? n/a — não há implementação
- G6 Manutenível? SIM — owner `slides-creator` squad, package privado @sinkra/, testes Jest + golden fixtures
- **Decisão final:** CREATE

### CREATE-2: `packages/@sinkra/slides-core`

- G1 Existe? NÃO — squad-engine é orquestração genérica, não tem pipeline slides-specific
- G6 Manutenível? SIM — owner `slides-creator`
- **Decisão final:** CREATE como coração compartilhado CLI/API/MCP (princípio DRY)

### CREATE-3: `packages/@sinkra/slides-mcp`

- G1 Existe? NÃO — `packages/ds-mcp` expõe design-system, não slides
- G3 Adaptável? NÃO — domínios distintos
- G6 Manutenível? SIM — segue template `packages/ds-mcp` 1:1
- **Decisão final:** CREATE espelhando ds-mcp

### Não-CREATE: `apps/slides-api`

- G1 Existe? SIM — `apps/squad-engine` já é Fastify API
- G2 Funciona? Quase — só faltam rotas `/slides/*`
- G3 Adaptável? SIM — adicionar 3 rotas é low-cost
- G4 Custo adapt < criar? SIM — adapt é 3 arquivos, criar app novo é 30+
- **Decisão final:** ADAPT `apps/squad-engine` (adicionar rotas) ao invés de criar app separada. KISS-No-Overengineering aplicado.

## Próximos Passos

1. Atualizar service-catalog.yaml ao registrar `slides-renderer`, `slides-core`, `slides-mcp` (após implementação F1/F2)
2. Squad config.yaml#render_targets ganha entrada `native_pptx` apontando para `@sinkra/slides-renderer`
3. Workflow generate-presentation v3.1 ganha Phase P06.5 consumindo o novo renderer
4. Skill SKILL.md ganha 3 decision-tree branches apontando para os novos packages quando user solicitar PPTX, API, CLI ou MCP

---

*Prior-Art Search v1.0 — slides-creator-open-source-absorption Wave 3 | 2026-05-18*
