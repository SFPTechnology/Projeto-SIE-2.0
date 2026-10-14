# Cross-Bench Synthesis — Slides Creator Templates Architecture

**Date:** 2026-05-17
**Mission:** MSN-2026-SLIDES-NARRATIVE-DESIGN (scope expansion)
**Inputs:** 9 benches em `/Users/alan/Code/bench/` (presenton, ppt-master, presentation-ai, PPTAgent, PresentAgent-2, banana-slides, powerpoint-skill, slide-deck-ai, deepH)
**Status:** Análise profunda concluída via 3 sub-agents paralelos

## Propósito

Antes de "bater o martelo" criando templates do zero, esta análise extrai **padrões arquiteturais transferíveis** dos 9 benches. O objetivo NÃO é copiar 174 layouts do Presenton ou 71 charts do ppt-master — é absorver o **modelo operacional** que torna esses sistemas robustos.

## Resumo Executivo

| Repo | O que ensina (peso de absorção) |
|---|---|
| **ppt-master** ⭐ | **Modelo operacional mais maduro.** Templates como contrato (`design_spec.md` + `spec_lock.md`), charts_index com regras "Pick for / Skip if", 21+ template families com keywords + summary, 71 charts catalogados, layouts SVG como referência visual. |
| **Presenton** ⭐ | **Schema first.** Templates como `.tsx` + Zod Schema + auto-compile para JSON Schema. CSS vars separam tema (visual) de estrutura (componente). settings.json por família. |
| **PPTAgent** ⭐ | **Agentic loop estruturado.** Roles YAML (planner, layout_selector, editor, coder) com prompts Jinja2 + retry com feedback explícito. Layout selection emite `{"reasoning": str, "layout": str}` — decisão auditável. |
| **presentation-ai** | **DSL XML de slide structure** (SECTION/COLUMNS/COMPARE/TABLE/CHART) separa estrutura semântica de tema visual. 41 themes pré-definidos. Edit operations Langchain (edit_slide_properties, regenerate_slide, change_theme). |
| **PresentAgent-2** | **Research integration.** ReAct loop com tools (search/scholar/visit/file_parser) + DeepResearch + multimodal (vídeo, image document parsing). Context folding para long tasks. |
| **banana-slides** | **Production patterns.** Task manager + ResourceLimiter + WebSocket progress + image editability via BBox transform + inpaint. |
| **powerpoint-skill** ⭐ | **QA técnico determinístico.** XML parsing (lxml) + boundary/overlap/gap/alignment checks. Theme system + slide masters + helper funcs. 100% regra, zero LLM. |
| **slide-deck-ai** | **Marcadores estruturais simples.** `>> step`, `[[icon_name]]`, double_col, table, key_message como heurística baseada em prefixos. Hybrid LLM + regex routing. |
| **deepH** | **Padrão de typesys/catalog transferível** (mesmo não sendo sobre slides). 60+ kinds + skill catalog YAML + agent contracts com io.inputs/outputs typed. |

⭐ = absorção prioritária para a próxima evolução do slides-creator.

## Padrões Cross-Bench Identificados

### 1. Template como CONTRATO (não como exemplo)

Todos os benches líderes (ppt-master, Presenton, PPTAgent) tratam template como **contrato estruturado**, não como markdown solto. O contrato declara:

| Campo | ppt-master | Presenton | PPTAgent | Síntese |
|---|---|---|---|---|
| Identidade | `template_name` em `layouts_index.json` | `layoutId` + `layoutName` em `.tsx` | `name` em YAML | **id + name + description** |
| Aplicabilidade | `summary` ("Pick for X. Skip if Y.") | implícito no `description` | `purpose` no planner | **pick_when + skip_when** explícitos |
| Slots | seções do `design_spec.md` | Zod schema | Jinja2 template args | **slots tipados** com constraints |
| Constraints | `spec_lock.md` (HEX/sizes/assets) | `.max()/.min()` Zod | jinja_args validation | **numeric + semantic limits** |
| Sample data | layouts SVG examples | Zod `.default()` | examples in prompts | **preview/sample obrigatório** |
| Proveniência | examples/ folders | `.tsx` files | YAML files | **source_ref** auditable |

**Princípio:** template sem contrato = exemplo. Exemplo sem contrato = lottery.

### 2. Seleção via REASONING explícito (não lookup cego)

ppt-master e PPTAgent fazem seleção LLM-driven com **rationale persistido**:

- **ppt-master** (`charts_index.json`): cada chart tem `summary` formato "Pick for {shape+scale}. Skip if {reason}". LLM strategist faz **full-read** do índice (71 entries) + matching semântico contrastivo. Decisão emite escolha + porquê.
- **PPTAgent** (`layout_selector.yaml`): role YAML recebe `slide_content + slide_description + available_layouts`, retorna `{"reasoning": str, "layout": str}`. Reasoning fica em `Turn.response` (history).

**vs. Presenton:** lookup direto por ID. Falta de reasoning torna seleção opaca — funciona para UI manual, falha para pipeline auditável.

**Para slides-creator:** seleção deve emitir `selected_template_reason` (PresentAgent-2 pattern) ou rationale formal (ppt-master/PPTAgent pattern). Isto fecha o gap **GAP-007** (routing automático após falha) com bonus de **why-decision audit trail**.

### 3. Separação radical TEMA vs ESTRUTURA

Todos os bons benches separam:

| Camada | ppt-master | Presenton | presentation-ai | Para slides-creator |
|---|---|---|---|---|
| **Tema visual** (cores, fonts, decorações, motion) | `spec_lock.md` | CSS vars + Tailwind | ThemeProperties (41 themes) | `theme/theme-tokens.yaml` |
| **Estrutura semântica** (slots, layout, contrato) | `design_spec.md` + layouts SVG | Zod Schema + React component | DSL XML tags | `slide/{function}.yaml` |
| **Conteúdo** (dados, textos, imagens) | `manifest.json` + assets | props do componente | content nodes do XML | per-deck render-time |

**Princípio:** trocar tema não deve quebrar estrutura. Trocar estrutura não deve recolocar cores. Hoje slides-creator mistura — `data/SOP-SLIDES-001.md` tem regras de cores **junto com** regras de hierarquia. Refator necessário.

### 4. Marcadores estruturais MÍNIMOS (não taxonomia infinita)

slide-deck-ai prova que 3-5 marcadores estruturais resolvem 80% dos casos:
- `>> ` (step process)
- `[[icon]]` (icon bullet)
- `dict {left, right}` (double column)
- `table {headers, rows}`
- `key_message` (callout)

ppt-master expande para 21 family templates mas mantém **slot vocabulary compacto** (cover, chapter, content, ending + variants).

**Anti-pattern observado:** Presenton tem ~174 layouts. Útil para UI exploratória, mas pipeline LLM precisa de **catálogo navegável**, não enciclopédia. Recomendação para slides-creator: **15-20 deck templates** (roteiros) + **15-20 slide function templates** (funções narrativas) + **catálogo separado de visualizações** (charts/diagrams) inspirado em ppt-master.

### 5. QA determinístico ANTES de LLM judgement

powerpoint-skill: `check_overlaps.py` faz 5 gates 100% deterministicos (boundary, overlap, gap, alignment, container) **antes** de qualquer julgamento estético. Zero LLM.

PPTAgent: agent `retry()` aceita traceback/feedback — incorpora erro determinístico ao prompt antes de re-tentar.

**Para slides-creator:** validators T-005..T-013B já estão bem split (Worker para deterministic, Agent para semantic). Mas falta **gate de overlap/boundary/overflow PPTX** que powerpoint-skill resolve. Pode ser absorvido posteriormente (out-of-scope da Mission atual).

### 6. Runtime JOBS como contrato de execução

banana-slides + PPTAgent têm padrões de runtime:
- **banana-slides**: `runtime/jobs.yaml` (não capturado mas referenciado), batch JSONL, presets por tipo (webinar/pitch/demo)
- **PPTAgent**: semáforo `max_at_once`, `length_factor` dinâmico

**Para slides-creator:** falta camada de **execution presets**. Hoje a skill `/slide-creator` aceita flags ad-hoc (`--brief`, `--mode`, `--gate-mode`). Refator: criar `templates/runtime/jobs.yaml` com presets nomeados (`webinar-sales`, `executive-pitch`, `board-update`, `demo`, `proposal`, `tactical-masterclass`).

### 7. Type system + Skill catalog (deepH pattern)

Mesmo não sendo sobre slides, deepH ensina padrão de **typesys** + **catalog** transferível:
- Kinds tipados (`plan/summary`, `design/spec`, `qa/report`)
- Skills declarativas YAML com io.inputs/outputs typed
- Validation runtime para type mismatch

Hoje slides-creator usa `data/token-registry.yaml` mas sem type system formal. Pode ser absorvido em iteração futura.

## O que NÃO devemos absorver

1. **174 layouts do Presenton** — copy não vai escalar manutenção. Absorver padrão `.tsx + Zod` mas curar manualmente 15-20 layouts canônicos.
2. **71 charts do ppt-master** — absorver o **formato do índice** (`charts_index.json` com summaries "Pick for / Skip if"), não imagens soltas.
3. **UI de presentation-ai** — fora do escopo. Mas DSL XML interessa.
4. **Prompts genéricos** — todos benches têm prompts. Não copiar; manter prompts derivados da disciplina narrativa SINKRA.
5. **Themes do presentation-ai (41)** — overkill para nossa fase. Absorver pattern do `ThemeProperties` interface, criar 5-8 themes canônicos.
6. **Edit operations do presentation-ai (Langchain tools)** — interessante mas precisa de runtime web. Out-of-scope da Mission.
7. **`spec_lock.md` machine-readable subset (ppt-master)** — interessante mas duplica `design-direction.yaml` que já criamos. Manter um SOT.

## Arquitetura Recomendada (para próximo passo)

```
.claude/skills/slide-creator/templates/
├── index.yaml                            # navigable catalog of all templates
├── schemas/
│   ├── deck-template.schema.yaml         # contract for deck-level templates (roteiros)
│   ├── slide-template.schema.yaml        # contract for slide-function templates
│   ├── visual-template.schema.yaml       # contract for charts/diagrams/infographics
│   ├── theme.schema.yaml                 # contract for theme tokens
│   └── runtime-job.schema.yaml           # contract for execution presets
├── deck/                                 # 12-15 deck roteiros (Russell Brunson, McKinsey, Y Combinator, etc.)
│   ├── webinar-sales-perfect-webinar.yaml
│   ├── webinar-sales-cold-3-pitch.yaml
│   ├── executive-pitch.yaml
│   ├── board-update.yaml
│   ├── financial-update.yaml
│   ├── tactical-masterclass.yaml
│   ├── product-demo.yaml
│   ├── benchmark-research.yaml
│   ├── sales-call-live-close.yaml
│   ├── proposal-sow.yaml
│   ├── vsl-5-step.yaml
│   ├── research-to-action.yaml
│   ├── ai-agent-demo.yaml
│   └── educational-workshop.yaml
├── slide/                                # 15-20 slide-function templates (function-based, não layout-based)
│   ├── hook-opening.yaml
│   ├── reframe.yaml
│   ├── tension-amplify.yaml
│   ├── contrast.yaml
│   ├── proof-stack.yaml
│   ├── mechanism-step.yaml
│   ├── demo-setup.yaml
│   ├── demo-payoff.yaml
│   ├── artifact-reveal.yaml
│   ├── objection-neutralize.yaml
│   ├── financial-data.yaml
│   ├── roadmap-execution.yaml
│   ├── matrix-framework.yaml
│   ├── synthesis.yaml
│   ├── cta-concrete.yaml
│   └── quiet-pause.yaml
├── visual/                               # taxonomia de charts/diagrams absorvida de ppt-master
│   ├── charts-and-diagrams.yaml          # 30-40 chart types com "Pick for / Skip if"
│   ├── layout-families.yaml              # 5-7 layout families
│   └── media-layouts.yaml                # image/video/embed patterns
├── theme/
│   ├── theme-tokens.schema.yaml
│   ├── editorial-pentagram.yaml          # 1 motif: editorial blocks
│   ├── consulting-mckinsey.yaml          # 1 motif: dense data, conservative
│   ├── demo-day-yc.yaml                  # 1 motif: bold typography, sparse decoration
│   ├── workshop-friendly.yaml            # 1 motif: warm, conversational
│   ├── financial-bloomberg.yaml          # 1 motif: data-dense, monospace accents
│   └── aiox-house.yaml                   # 1 motif: brand-specific
├── runtime/
│   ├── jobs.yaml                         # named presets: full-deck, key-slide-gate, rewrite-bad-deck, benchmark-deck
│   ├── edit-operations.yaml              # absorvido de presentation-ai DSL (out-of-Mission-scope marker)
│   └── import-template.yaml              # contract for importing external .pptx (out-of-scope marker)
├── qa/
│   ├── narrative-gates.yaml              # references qa-rubric.yaml + qa-routing-table.yaml
│   ├── visual-gates.yaml                 # references qa-rubric.yaml#dimensions.design
│   └── template-selection-gates.yaml     # gates that ensure selected template fits brief
└── wireframes/                           # HTML previews — referência visual, não código de render
    ├── README.md
    ├── gallery.html                      # index of all wireframes
    ├── webinar-flow.html
    ├── mechanism-map.html
    ├── proof-stack.html
    └── benchmark-matrix.html
```

## Próximos passos recomendados (proposta — não executar sem aprovação)

1. **Hoje (Mission scope expansion):** registrar deviation DEV-2026-003 ampliando escopo da Mission para incluir esta arquitetura de templates.
2. **Phase 5+6 ajustada:** antes de regenerar Primeiro Servico v3 fixture (T-023), criar primeiro:
   - `schemas/deck-template.schema.yaml`
   - `schemas/slide-template.schema.yaml`
   - 2-3 deck templates piloto (webinar-sales + executive-pitch + tactical-masterclass)
   - 5-7 slide function templates piloto
   - 1 theme piloto (editorial-pentagram para validar a separação)
3. **Validação:** rodar pipeline contra fixture Primeiro Serviço de IA usando os novos templates. Score baseline atual ~5 → target >=8.5.
4. **Post-Mission:** absorção continuada (chart taxonomy, edit operations, native-pptx) vira backlog para Mission futura.

## Evidências (paths citados pelos sub-agents)

- ppt-master: `/Users/alan/Code/bench/ppt-master/skills/ppt-master/references/strategist.md`, `/Users/alan/Code/bench/ppt-master/skills/ppt-master/templates/charts/charts_index.json`, `/Users/alan/Code/bench/ppt-master/skills/ppt-master/templates/layouts/layouts_index.json`
- Presenton: `/Users/alan/Code/bench/presenton/servers/nextjs/lib/compile-template-schema.ts`, `/Users/alan/Code/bench/presenton/servers/nextjs/app/presentation-templates/neo-modern/TitleKpiSnapshotGrid.tsx`, `/Users/alan/Code/bench/presenton/servers/nextjs/app/presentation-templates/defaultSchemes.ts`
- PPTAgent: `/Users/alan/Code/bench/PPTAgent/pptagent/roles/planner.yaml`, `/Users/alan/Code/bench/PPTAgent/pptagent/roles/layout_selector.yaml`, `/Users/alan/Code/bench/PPTAgent/pptagent/induct.py`, `/Users/alan/Code/bench/PPTAgent/pptagent/pptgen.py`
- presentation-ai: `/Users/alan/Code/bench/presentation-ai/src/lib/presentation/themes.ts`, `/Users/alan/Code/bench/presentation-ai/src/ai/tools/presentation/tools.ts`, `/Users/alan/Code/bench/presentation-ai/src/config/slideFormats.ts`
- powerpoint-skill: `/Users/alan/Code/bench/powerpoint-skill/powerpoint-slides/scripts/check_overlaps.py`, `/Users/alan/Code/bench/powerpoint-skill/powerpoint-slides/references/themes.md`
- slide-deck-ai: `/Users/alan/Code/bench/slide-deck-ai/src/slidedeckai/helpers/pptx_helper.py` (linhas 39-51, 142-230), `/Users/alan/Code/bench/slide-deck-ai/src/slidedeckai/prompts/initial_template_v4_two_cols_img.txt`
- deepH: `/Users/alan/Code/bench/deepH/internal/typesys/types.go`, `/Users/alan/Code/bench/deepH/internal/catalog/skills.go`, `/Users/alan/Code/bench/deepH/internal/catalog/kits.go`

## Decisão pendente

O usuário (Mission Lead) precisa decidir:
- (A) **Expandir escopo da Mission** para incluir arquitetura de templates (DEV-2026-003) e adiar Phase 5+6 atual em ~5-10 dias
- (B) **Manter escopo atual** (validators + critique loop) — entregar Phase 5+6 com workflow v3 e abrir Mission separada `MSN-2026-SLIDES-TEMPLATES-ARCHITECTURE` para os templates
- (C) **Híbrido:** criar APENAS os 3 schemas canônicos (deck/slide/visual) + 2-3 templates piloto na Mission atual, deixar índice completo para Mission futura

Recomendação técnica: **(C) Híbrido.** Schemas + 2-3 templates piloto cabem em 1-2 dias agente e fecham o gap arquitetural sem inflar appetite. Resto vira Mission separada com escopo limpo.
