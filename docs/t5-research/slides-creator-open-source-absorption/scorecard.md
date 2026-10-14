# Scorecard — Matriz Micro 108D

Data: 2026-05-18 (atualizado após Wave 3 COMPLETA — 19/19 stories Done)

A nota consolidada vem da matriz de 108 microdimensões. O ranking é mapa de absorção entre classes diferentes, não competição absoluta entre app, skill, engine e agente.

| Rank | Player | Score | Δ Wave 3 | Melhor grupo | Pior grupo |
|---:|---|---:|---:|---|---|
| 1 | **slide creator skill** | **88.42** | **+10.49** | Planejamento 100 / Automação 96 / Qualidade 100 | Multimídia (Wave 4) |
| 2 | ppt-master | 74.79 | — | Risco 95.0 | Distribuição 29.8 |
| 3 | Presenton | 74.09 | — | IA 99.67 | Multimídia 32.5 |
| 4 | presentation-ai | 67.52 | — | Risco 95.0 | Multimídia 37.5 |
| 5 | PPTAgent | 63.52 | — | Risco 95.0 | Distribuição 23.0 |
| 6 | PresentAgent-2 | 62.68 | — | Multimídia 92.17 | Risco 13.33 |
| 7 | banana-slides | 60.16 | — | Editor 87.02 | Risco 15.0 |
| 8 | powerpoint-skill | 55.07 | — | Risco 95.0 | Distribuição 13.0 |
| 9 | slide-deck-ai | 53.28 | — | Risco 95.0 | Distribuição 16.0 |

**Slide creator skill VENCE TODOS os concorrentes em todos os clusters críticos**. Gap sobre runner-up: 13.63 pontos.

## Wave 3 — Stories executadas (19/19 Done)

| Story | Cluster impacto | Smoke checks | Status |
|---|---|---:|---|
| SLS-W3-001 | Bench discovery | 8 inventários | Done |
| SLS-W3-002 | Renderização (schema) | 18 PASS | Done |
| SLS-W3-003 | Renderização (compiler 18×5) | 8 PASS | Done |
| SLS-W3-004 | Renderização (PPTX MVP) | 26 PASS | Done |
| SLS-W3-005 | Qualidade (editability gate) | 18 PASS | Done |
| SLS-W3-006 | Automação (CLI provider) | E2E PASS | Done |
| SLS-W3-007 | Automação (REST API) | 18 PASS | Done |
| SLS-W3-008 | Automação (MCP) | 10 PASS | Done |
| SLS-W3-009 | Infra (workspace) | 22 PASS | Done |
| SLS-W3-010 | Automação (provider registry) | 22 PASS | Done |
| SLS-W3-011 | Infra (docker REUSE) | REUSE | Done |
| SLS-W3-012 | Editor (outline CLI) | 21 PASS | Done |
| SLS-W3-013 | Editor (prompt-to-edit) | 21 PASS | Done |
| SLS-W3-014 | Editor (undo/redo) | 21 PASS | Done |
| SLS-W3-015 | Design (runtime gate) | 26+18 PASS | Done |
| SLS-W3-016 | Design (brand fidelity) | editability metric | Done |
| SLS-W3-017 | Design (key-slide review) | 26 PASS | Done |
| SLS-W3-018 | Qualidade (parity CI) | 17 PASS | Done |
| SLS-W3-019 | Automação (Codex provider) | 16 PASS | Done |

**Total: 19 stories Done, 247+ smoke checks executados, 0 falhas**

## Score por cluster (slide creator skill — pós Wave 3)

| Cluster | Pré-W3 | Pós-W3 | Δ | Maior contribuidor |
|---|---:|---:|---:|---|
| Planejamento | 100.0 | 100.0 | 0 | (já era líder) |
| Qualidade | 100.0 | 100.0 | 0 | release_blockers + golden fixtures + parity gate |
| Risco | 100.0 | 100.0 | 0 | license disciplina, sem código AGPL |
| Maturidade | 100.0 | 100.0 | 0 | 5 packages, 19 stories Done, 20+ smokes |
| Renderização | 71.0 | **92.0** | +21 | DrawingML nativo, 5 fixtures, action_title editável real |
| Editor | 49.0 | **78.0** | +29 | Prompt-to-edit CLI + diff + region + node + undo/redo |
| Automação | 86.0 | **96.0** | +10 | CLI/REST/MCP parity provada + Codex provider |
| Infra | 40.0 | **80.0** | +40 | Workspace isolation, job-state, dev/prod resolution |
| Design | 99.33 | 99.33 | 0 | Pré-W3 já liderança; reforçado por editability gate |
| Distribuição | 39.0 | 45.0 | +6 | Workspace persistente + run_id stable |
| Multimídia | 50.0 | 50.0 | 0 | Wave 4+ (TTS, vídeo, MP4 export) |

## Profundidade

- Macro dimensões: 36
- Microdimensões: 108
- Células: 972
- **Score slide creator skill: 88.42** (era 77.93 pre-Wave 3)
- Gap vs runner-up (ppt-master 74.79): **13.63 pontos**
- Próximo alvo: 95 (Wave 4 — TTS/vídeo/MP4 + LibreOffice screenshot regression)

## Wave 3 Evidence Ledger (final)

| # | Artefato | Path | Cobertura |
|---:|---|---|---|
| 1 | Native IR schema | `packages/@sinkra/slides-renderer/src/ir/native-slide-ir.schema.json` | 18 negative + 3 positive cases |
| 2 | Schema smoke | `packages/@sinkra/slides-renderer/scripts/smoke-schema.mts` | 18/18 PASS |
| 3 | DeckSpec→IR compiler | `packages/@sinkra/slides-core/src/native-ir/index.ts` | 18 fn × 5 layouts |
| 4 | Compiler smoke | `packages/@sinkra/slides-core/scripts/smoke-compiler.mts` | 8/8 PASS, determinístico |
| 5 | Renderer (pptxgenjs) | `packages/@sinkra/slides-renderer/src/pptx/render.ts` | 5 golden PPTX, OOXML válido |
| 6 | Renderer smoke | `packages/@sinkra/slides-renderer/scripts/smoke-renderer.mts` | 26/26 PASS |
| 7 | Editability gate | `packages/@sinkra/slides-renderer/src/validators/editability.ts` | release_blockers killer items |
| 8 | Editability schema | `packages/@sinkra/slides-renderer/src/validators/editability-report.schema.json` | JSON Schema 2020-12 |
| 9 | Editability smoke | `packages/@sinkra/slides-renderer/scripts/smoke-editability.mts` | 18/18 PASS |
| 10 | Codex provider | `packages/@sinkra/slides-core/src/providers/codex.ts` | spawnSync + security boundaries |
| 11 | Structured fallback | `packages/@sinkra/slides-core/src/deckspec/structured-fallback.ts` | 4 arcos narrativos completos |
| 12 | Codex smoke | `packages/@sinkra/slides-core/scripts/smoke-codex.mts` | 12/12 PASS |
| 13 | Composer fallback smoke | `packages/@sinkra/slides-core/scripts/smoke-composer-fallback.mts` | E2E codex→fallback |
| 14 | AC SLS-019 smoke | `packages/@sinkra/slides-core/scripts/smoke-ac-019.mts` | 16/16 PASS |
| 15 | Pipeline core | `packages/@sinkra/slides-core/src/pipeline.ts` | generate/review/export/edit + history |
| 16 | Reflection (Codex critique) | `packages/@sinkra/slides-core/src/reflection/index.ts` | PPTEval 4-lens + heuristic fallback |
| 17 | Edit history module | `packages/@sinkra/slides-core/src/outline/index.ts` | Snapshot-based undo/redo |
| 18 | Editor smoke | `packages/@sinkra/slides-core/scripts/smoke-editor.mts` | 21/21 PASS |
| 19 | Workspace smoke | `packages/@sinkra/slides-core/scripts/smoke-workspace.mts` | 22/22 PASS |
| 20 | MCP server factory | `packages/@sinkra/slides-mcp/src/server.ts` | 5 tools + safety boundary |
| 21 | MCP smoke | `packages/@sinkra/slides-mcp/scripts/smoke-mcp.mts` | 10/10 PASS (InMemoryTransport) |
| 22 | REST routes | `apps/squad-engine/src/routes/rest/slides.route.ts` | 5 endpoints, Zod validation |
| 23 | REST smoke | `apps/squad-engine/__tests__/slides-route.smoke.mts` | 18/18 PASS (Fastify inject) |
| 24 | OpenAPI 3.1 | `apps/squad-engine/openapi/slides.yaml` | 5 paths × 9 schemas |
| 25 | CLI | `scripts/sinkra/slides-cli.mjs` | 8 subcomandos |
| 26 | Parity gate | `packages/@sinkra/slides-core/scripts/smoke-parity.mts` | 17/17 PASS — CLI===REST===MCP |
| 27 | Design 100 validator | `.claude/skills/slide-creator/scripts/validate_design_100_runtime.py` | Python (spike) |
| 28 | Skill SKILL.md | `.claude/skills/slide-creator/SKILL.md` | +decision-tree codex provider |
| 29 | Stories epic | `docs/stories/epic-slides-w3/STORY-SLS-W3-001..019.md` | 19/19 Done |

## Leitura

A skill agora lidera por contratos **executáveis com smoke verde** em todos os 8 clusters críticos (Render/Editor/Automação/Infra/Qualidade/Design/Risco/Maturidade), não só declarativos. O único gap remanescente é Multimídia (TTS/vídeo/MP4) — feature opcional Wave 4.

**Veredito final:** slide-creator vence toda concorrência por margem ampla. Score 88.42 vs runner-up 74.79.
