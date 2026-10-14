# Wave 3 — Score Delta (spike materializado)

**Data:** 2026-05-18
**Source bench:** `comparison-matrix.json` v1.5 (108D × 9 players, score atual `slide creator skill = 77.93`)
**Próxima atualização:** após execução completa das 18 stories da Wave 3 (vide `EPIC-SLIDES-W3.md`)

## Tese desta nota

O spike pré-W3 já materializou contratos executáveis em 3 packages, 5 rotas REST, 1 CLI, 1 MCP server, 2 validators Python e 5 golden fixtures. Cada um destes artefatos é evidência *parcial* — suficiente para tirar microdimensões da banda "contrato apenas" para "contrato + spike" mas não para fechar a story de cada microdim, que ainda exige test green em CI + fixture revisada por design ops.

Esta nota lista os deltas *spike-only* — quando uma microdimensão sobe de score por evidência executável recém-introduzida — e marca quais ainda precisam de CI verde antes de virarem score oficial na `comparison-matrix.json`.

## Deltas propostos (proposed_delta — pendente de CI verde)

| Cluster | Microdim ID | Score atual | Score proposto | Evidence ledger |
|---|---|---:|---:|---|
| Automação | `api_mcp_self_hosted__rest_endpoint` | 85 | 92 | `apps/squad-engine/src/routes/rest/slides.route.ts` (5 rotas registradas) |
| Automação | `api_mcp_self_hosted__mcp_tools` | 86 | 93 | `packages/@sinkra/slides-mcp/src/index.ts` (5 tools com safety) |
| Automação | `api_mcp_self_hosted__stable_io_contract` | 88 | 94 | Zod schemas + parity contract entre CLI/API/MCP |
| Automação | `api_mcp_self_hosted__tool_safety_limits` | 88 | 94 | secrets via env apenas; sem log; structured errors |
| Automação | `batch_automation__clear_cli` | 92 | 96 | `scripts/sinkra/slides-cli.mjs` com 5 subcomandos |
| Automação | `batch_automation__ci_pipeline_fit` | 91 | 95 | `validate_runtime_parity.py` + provider=dummy smoke |
| Automação | `provider_routing__codex_cli` (novo) | 0 | 92 | **SLS-W3-019:** `providers/codex.ts` + smoke 16/16 PASS — codex CLI sem chave externa, fallback estruturado quando codex falha |
| Planejamento | `composer_real_decks` (novo) | 0 | 95 | **SLS-W3-019:** `composeStructuredFallback` emite arco persuasive/diagnostic/demo/course completo, mesmo sem provider externo. Smoke: 8 slides, all-claims, last=cta |
| Qualidade | `critique_loop_with_pptval_lenses` | 100 | 100 | **SLS-W3-019:** `prompts/critique.prompt.ts` PPTEval 4-lens (vision/content/coherence/GAD) wired via codex + heuristic fallback |
| Risco | `provider_failure_no_crash` (novo) | 0 | 98 | **SLS-W3-019:** runtime nunca crasha em provider failure; emite `job.errors[]` com `provider_fallback:*` e prossegue com fallback estruturado |
| Renderização | `native_pptx_objects__drawingml_shapes` | 57 | 78 | `slides-renderer/src/pptx/render.ts` cobre text/shape/image/table/chart |
| Renderização | `native_pptx_objects__image_vs_object_policy` | 62 | 82 | `editability.ts` distingue native vs raster |
| Renderização | `render_fidelity__pptx_editability_inspection` | 58 | 86 | `editability-report.json` schema + verdict |
| Planejamento | `slide_function_map` | 100 | 100 | mantido — sem regressão |
| Planejamento | `critique_loop` | 100 | 100 | `slides-core/reflection` materializa `planning-reflection.jsonl` |
| Design | `template_runtime__theme_runtime` | 99 | 99 | mantido (theme aplicado em ir + renderer) |
| Design | `design_governance__design_100_gate` | (novo) | 95 | `validate_design_100_runtime.py` + 4 outputs (`design-mastery-report`, `brand-template-manifest`, `key-slide-render-review`, `visual-regression-checklist`) |
| Editor | `prompt_to_edit__diff_before_apply` | 74 | 83 | `editSlide()` em `slides-core/pipeline.ts` retorna diff sem aplicar |
| Editor | `prompt_to_edit__target_slide_region_element` | 51 | 70 | `target: {slide_id, region?, node_id?}` no schema |
| Infra | `self_hosted_runtime__service_topology` | 57 | 78 | REUSE squad-engine (Fastify + Inngest + Redis + Supabase) |
| Qualidade | `qa_visual_rendered_key_slides` | 100 | 100 | mantido |
| Qualidade | `qa_inspecionar_objetos_editaveis_pptx` | 94 | 96 | `editability.ts` |

**Projeção:**
- score atual: **77.93**
- spike-only proposto: **80.6** (proposed_delta agregado, sem CI verde)
- pós-execução completa Wave 3 (todas as 18 stories): **≥ 82** (meta original)

## Microdimensões NÃO movimentadas no spike

Estas continuam pendentes de stories (W3.x) para mover:

| Microdim | Story bloqueadora |
|---|---|
| `native_pptx_objects__powerpoint_reopen_fidelity` | SLS-W3-004 (depende de manual review PPT) |
| `render_fidelity__roundtrip_powerpoint` | SLS-W3-004 |
| `self_hosted_runtime__docker_compose` | SLS-W3-011 |
| `self_hosted_runtime__local_offline_mode` | SLS-W3-011 |
| `self_hosted_runtime__storage_logs_upgrade` | SLS-W3-009 |
| `web_editor_runtime__canvas_editor` | fora-de-escopo Wave 3 (UI fica para Wave 4) |
| `web_editor_runtime__state_management_undo` | SLS-W3-014 |
| `prompt_to_edit__regenerate_only_needed_area` | SLS-W3-013 |
| `template_import_replication__template_manifest` | SLS-W3-016 |
| `multimidia__tts_*` (6 microdims) | fora-de-escopo Wave 3 |

## Regra de promoção (gate)

> Uma proposta `proposed_delta` só vira score na `comparison-matrix.json` quando:
>
> 1. CI passa para a story correspondente (jest, py compile, validate:yaml, validate:slides-parity)
> 2. Pelo menos 1 fixture executável demonstra o comportamento
> 3. Validator emite verdict PASS
> 4. Manual review do design-ops ou QA na story (PR review)

Aplicada essa regra hoje: **0 microdims promovidas** — os deltas acima são propostas, não atualização de score oficial. A `comparison-matrix.json` permanece inalterada até as stories fecharem.

## Evidence ledger Wave 3 (spike)

| Artefato | Path | Linhas | Função |
|---|---|---:|---|
| Native IR schema | `packages/@sinkra/slides-renderer/src/ir/native-slide-ir.schema.json` | ~250 | Contrato JSON Schema 2020-12 com EMU |
| Renderer | `packages/@sinkra/slides-renderer/src/pptx/render.ts` | ~240 | pptxgenjs wrapper, IR → .pptx |
| Editability inspector | `packages/@sinkra/slides-renderer/src/validators/editability.ts` | ~90 | Score 0-100 com PASS/CONCERNS/FAIL |
| CLI renderer | `packages/@sinkra/slides-renderer/src/cli.ts` | ~85 | `slides-render <ir.json>` |
| Pipeline core | `packages/@sinkra/slides-core/src/pipeline.ts` | ~270 | generate / review / export / editSlide / loadJobState |
| Reflection | `packages/@sinkra/slides-core/src/reflection/index.ts` | ~175 | Critique loop + jsonl |
| Native IR compiler | `packages/@sinkra/slides-core/src/native-ir/index.ts` | ~290 | DeckSpec → IR (18 funcs × 5 layouts) |
| MCP server | `packages/@sinkra/slides-mcp/src/index.ts` | ~125 | 5 tools com Zod input |
| REST routes | `apps/squad-engine/src/routes/rest/slides.route.ts` | ~130 | 5 endpoints `/api/v1/slides/*` |
| CLI operator | `scripts/sinkra/slides-cli.mjs` | ~150 | 5 subcomandos |
| Design 100 gate | `.claude/skills/slide-creator/scripts/validate_design_100_runtime.py` | ~280 | Render → score |
| Parity gate | `.claude/skills/slide-creator/scripts/validate_runtime_parity.py` | ~90 | Surfaces idênticos |
| Golden fixtures | `packages/@sinkra/slides-renderer/fixtures/golden/*.ir.json` | 5 | exec/webinar/finance/technical/brand |
| Tests core | `packages/@sinkra/slides-core/__tests__/*.test.ts` | 5 specs | briefing/deckspec/native-ir/reflection/pipeline |
| Tests renderer | `packages/@sinkra/slides-renderer/__tests__/*.test.ts` | 3 specs | editability/schema/golden-fixtures |

## Próximo passo

`/aiox-po` para validar as 18 stories (Draft → Ready) e `/full-sdc` para executar SLS-W3-001 → 018 sequencialmente. Score oficial só muda quando cada story fecha com CI verde e o validator de promoção aceitar.
