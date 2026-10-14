# Wave 2 — Operational Intelligence Absorption

**Data:** 2026-05-17  
**Fonte:** diagnóstico do Mission Lead + leitura manual de `../bench`  
**Predecessor:** `00-cross-bench-synthesis.md`  
**Status:** Executado como contratos autocontidos do `slide-creator`

## Tese Central

> O principal que ainda estávamos deixando passar não era “mais templates visuais”; era **inteligência operacional** para transformar templates em qualidade repetível.

A Wave 1 montou a arquitetura de templates. A Wave 2 adicionou os contratos que fazem essa arquitetura funcionar como processo: pesquisa roteada, extração documental, manuscript-first, seleção de packs, ledger de evidências, render/export verificável, avaliação renderizada, trace/handoff e fixtures de regressão.

## Resultado Executado

A absorção foi implementada na skill autocontida `slide-creator`, não em `squads/slides-creator`, para que possa ser compartilhada sem depender do monorepo SINKRA.

Superfícies sincronizadas:

- `.claude/skills/slide-creator/`
- `.codex/skills/slide-creator/`
- `.agents/skills/slide-creator/`

Estado atualizado da superfície canônica em `.claude` depois da continuação YOLO:

| Métrica | Total |
|---|---:|
| YAMLs em `templates/` | 43 |
| Arquivos totais na skill | 72 |
| Scripts executáveis | 5 |
| Contratos runtime | 11 |
| Contratos research | 2 |
| Contratos import | 3 |
| Contratos visual | 8 |
| Contratos QA | 6 |
| Contratos eval | 1 |

Validações executadas:

- `npm run validate:yaml:changed`
- `node scripts/validate-skills.js --skill slide-creator --strict`
- `node scripts/validate-skill-internal-refs.js .claude/skills/slide-creator`
- Parse YAML completo em `.claude`, `.codex` e `.agents`
- `python -m py_compile .claude/skills/slide-creator/scripts/*.py`
- smoke test de `scripts/validate_chart_data.py`

Observação: em uma rodada posterior, `npm run validate:yaml:changed` falhou por erro externo já presente em `outputs/aiox-sop/the-truth-about-selling-ai-automations-to-businesses/04-score-card-v2.yaml:548`. A skill foi validada isoladamente em `.claude`, `.codex` e `.agents`.

## Decisões de Absorção

| # | Padrão | Bench | Decisão | Contrato criado |
|---|---|---|---|---|
| 1 | Document extractor estruturado | PPTAgent + PresentAgent-2 | Absorvido | `templates/import/document-extraction.yaml` |
| 2 | Template examples + per-slide override | presentation-ai | Absorvido | `templates/runtime/template-example-routing.yaml` |
| 3 | PPTEval renderizada multimodal | PPTAgent | Absorvido como contrato | `templates/eval/rendered-eval.yaml` |
| 4 | Source router por fonte/mídia | PresentAgent-2 DeepResearch | Absorvido | `templates/research/source-routing.yaml` |
| 5 | Manuscript pipeline | PPTAgent/deeppresenter | Absorvido | `templates/runtime/manuscript-pipeline.yaml` |
| 6 | HTML → PPTX contract | PPTAgent/deeppresenter | Absorvido | `templates/runtime/html-to-pptx.yaml` |
| 7 | Export job contract | Presenton + banana-slides | Absorvido como contrato, não engine | `templates/runtime/export-contract.yaml` |
| 8 | Packs induzidos adicionais | PPTAgent | Absorvido como seleção de packs | `templates/import/induced-layout-packs.yaml` |
| 9 | deepH runtime | deepH | Extraído como trace/handoff, não port de Go | `templates/runtime/trace-handoff.yaml` |
| 10 | Image → editable PPTX | banana-slides | Absorvido parcialmente como referência de export/import | `export-contract.yaml` + `bench-absorption-map.md` |
| 11 | Evidence ledger | PresentAgent-2 + PPTAgent | Absorvido | `templates/research/evidence-ledger.yaml` |
| 12 | Regression fixtures | deepH + PPTEval + powerpoint-skill | Absorvido | `templates/qa/regression-fixtures.yaml` |
| 13 | AI image type routing | ppt-master | Absorvido como seleção de composição interna | `templates/visual/ai-image-type-routing.yaml` |
| 14 | PPTX template manifest import | ppt-master | Absorvido como contrato de ingestão de template | `templates/import/pptx-template-manifest.yaml` |
| 15 | Chart data modes | presentation-ai | Absorvido como contrato + script de validação | `templates/visual/chart-data-contracts.yaml` + `scripts/validate_chart_data.py` |
| 16 | Diagram engine routing | powerpoint-skill | Absorvido como runtime técnico | `templates/runtime/diagram-rendering.yaml` |
| 17 | UI/sharing/collaboration | Presenton/presentation-ai/Gamma | Rejeitado para skill; produto/dash futuro | Não aplicável |
| 18 | Providers/scripts/detalhes de UI específicos | Vários | Rejeitado como ruído | Não aplicável |

## Arquitetura Resultante

O registry principal agora roteia a criação nesta ordem:

1. `deck_template`
2. `slide_function_template`
3. `visual_template`
4. `theme_profile`
5. `research_route`
6. `import_pipeline`
7. `runtime_job`
8. `rendered_eval`
9. `qa_gates`

Dentro dessa ordem, a continuação adicionou sub-roteiros que estavam faltando:

- `visual_template -> chart_data_contract -> chart_renderer`
- `visual_template -> ai_image_type -> image_prompt -> native_text_overlay`
- `import_pipeline -> pptx_template_manifest -> layout/style constraints`
- `runtime_job -> diagram_engine -> diagram_manifest -> technical QA`

Arquivo canônico:

- `.claude/skills/slide-creator/templates/index.yaml`

## Contratos Criados

### Research

`templates/research/source-routing.yaml`

Separa rotas de pesquisa por tipo de evidência:

- HTML source pages
- motion media: vídeo, GIF, demo, screen recording
- scholar/benchmark evidence
- local files

Regra principal: não usar um prompt genérico para todos os tipos de fonte.

`templates/research/evidence-ledger.yaml`

Cria um ledger por claim:

- `claim_id`
- `slide_id`
- claim
- tipo de evidência
- fonte
- confiança
- frescor
- risco
- uso em slide ou speaker notes

Bloqueia claims de alto risco sem fonte, métrica, período ou escopo.

### Import

`templates/import/document-extraction.yaml`

Absorve o modelo do PPTAgent:

- normalizar para Markdown
- detectar idioma
- construir árvore de headings
- extrair seções/subseções
- gerar metadata
- captionar imagens e tabelas
- mapear claims/evidências

Regra principal: preservar texto válido na extração; síntese narrativa vem depois.

`templates/import/induced-layout-packs.yaml`

Absorve comportamento dos packs:

- `beamer`: acadêmico/técnico
- `cip`: método, benchmark, pipeline, resultados
- `default`: narrativa geral com mídia variada
- `hit`: engenharia/institucional técnico
- `thu`: pesquisa universitária
- `ucas`: UI, design system, paleta, walkthrough

Regra principal: escolher pack por função, mídia e público, não por estética.

`templates/import/pptx-template-manifest.yaml`

Absorve o importador leve do `ppt-master`:

- slide size;
- theme fonts/colors;
- backgrounds por herança slide/layout/master;
- assets reutilizáveis;
- placeholders e geometria;
- text samples;
- page type;
- `manifest.json`, `summary.md`, `assets/` e `template-import-report.yaml`.

Regra principal: importar comportamento reutilizável, não fingir que screenshot ou SVG equivale a PPTX editável.

### Runtime

`templates/runtime/manuscript-pipeline.yaml`

Cria a camada intermediária:

`briefing -> outline_json -> research_manuscript -> claim/evidence map -> slide_function_map -> deck_spec`

Use quando:

- deck é research-heavy;
- tema é técnico/estratégico/educacional;
- o processo anterior falhou por gerar slides direto de outline.

`templates/runtime/template-example-routing.yaml`

Absorve o padrão do `presentation-ai`:

- serializar exemplos de templates no prompt;
- anexar usage hints;
- permitir overrides por item do outline.

`templates/runtime/html-to-pptx.yaml`

Contrato de render/export:

- lock de dimensão pelo primeiro slide;
- extração de placeholders;
- overflow check;
- margem inferior;
- rasterização explícita de CSS complexo;
- comparação entre screenshot HTML e preview exportado.

`templates/runtime/export-contract.yaml`

Export verificável:

- task JSON;
- worker;
- stdout/stderr;
- response JSON;
- output path;
- preview/thumbnail;
- bloqueio se arquivo não existe, está vazio ou não é legível.

`templates/runtime/trace-handoff.yaml`

Absorve deepH como processo:

- focused working set;
- universos de review;
- handoffs tipados;
- síntese deduplicada;
- trace report.

`templates/runtime/diagram-rendering.yaml`

Absorve o roteamento técnico do `powerpoint-skill`:

- Graphviz para arquitetura, flow, dependency graph, tree e comparison graph;
- Mermaid para sequence, gantt, pie, state e ER;
- TikZ para math/geometric/paper-faithful diagrams;
- native shapes para setas, callouts, highlights e anotações;
- PDF extraction para figuras de paper com atribuição e 300 DPI.

Regra principal: escolher engine por semântica e editabilidade antes de gerar a figura.

### Visual

`templates/visual/ai-image-type-routing.yaml`

Absorve o sistema de image types do `ppt-master`:

- background;
- hero;
- portrait;
- typography;
- infographic;
- flowchart;
- framework;
- matrix;
- cycle;
- funnel;
- pyramid;
- comparison;
- timeline;
- map;
- scene.

Regra principal: tipo de imagem é composição interna do bloco visual, não o layout da página. Texto crítico fica nativo, não embutido na imagem.

`templates/visual/chart-data-contracts.yaml`

Absorve o editor de dados do `presentation-ai`:

- label-value;
- xy;
- xyz;
- multi-series;
- range;
- waterfall;
- OHLC;
- box-plot;
- hierarchical;
- flow;
- funnel;
- heatmap;
- histogram;
- gauge.

Regra principal: o dataset precisa validar antes de escolher estilo de gráfico.

### Eval

`templates/eval/rendered-eval.yaml`

Avaliação pós-render:

- `vision`
- `content`
- `logic`
- `technical_render`

Regra principal: deck importante não pode ser aprovado só lendo spec; precisa olhar slide renderizado.

### QA

`templates/qa/regression-fixtures.yaml`

Converte falhas conhecidas em forward tests:

- narrativa
- design
- pesquisa
- render
- seleção de templates

Regra principal: se uma falha já aconteceu, ela vira blocker nomeado antes de chamarmos o processo de “melhorado”.

## Mudanças no `SKILL.md`

O `SKILL.md` agora instrui explicitamente quando carregar:

- `templates/research/source-routing.yaml`
- `templates/research/evidence-ledger.yaml`
- `templates/import/document-extraction.yaml`
- `templates/import/induced-layout-packs.yaml`
- `templates/runtime/manuscript-pipeline.yaml`
- `templates/runtime/template-example-routing.yaml`
- `templates/runtime/trace-handoff.yaml`
- `templates/runtime/html-to-pptx.yaml`
- `templates/runtime/export-contract.yaml`
- `templates/eval/rendered-eval.yaml`
- `templates/qa/regression-fixtures.yaml`
- `templates/import/pptx-template-manifest.yaml`
- `templates/visual/ai-image-type-routing.yaml`
- `templates/visual/chart-data-contracts.yaml`
- `templates/runtime/diagram-rendering.yaml`

Também adiciona gates não negociáveis:

- research routing;
- evidence ledger;
- induced pack selection;
- manuscript-first;
- traceable handoffs;
- regression fixtures;
- rendered evaluation;
- verified export.
- AI image type routing;
- chart data validation;
- diagram engine routing;
- template import honesty.

## O Que Foi Rejeitado Como Ruído

Não absorvemos:

- UI específica de Presenton/presentation-ai/banana;
- scripts de instalação;
- providers específicos que não melhoram o processo;
- dados de benchmark acadêmico que não viram qualidade de slide;
- port de código Go do deepH;
- implementação completa de image-to-editable-PPTX do banana.

A regra adotada foi: absorver comportamento e contrato, não copiar produto, UI ou runtime externo.

## Lacunas Restantes

Ainda não existe um executor real para tudo isso. A skill agora tem os contratos, mas alguns pontos ainda são especificação operacional:

| Lacuna | Estado | Próximo passo recomendado |
|---|---|---|
| Renderer HTML real | Contrato existe | Criar `scripts/render-slide-html.ts` ou runner equivalente |
| PPTEval real com VLM | Parcialmente executado | `validate_rendered_eval.py` valida relatório renderizado; VLM worker ainda é futuro |
| Export real PPTX/PDF | Contrato existe | Criar mission separada de export pipeline |
| Template serializer executable | Contrato existe | Criar script que transforma YAML template em exemplos Markdown/XML |
| Evidence ledger automático | Parcialmente executado | `build_evidence_ledger.py` existe; ampliar cobertura de evidências indiretas |
| Chart data validation | Executado mínimo | `validate_chart_data.py` existe; integrar no package validator |
| Regression suite executável | Executado mínimo | `run_regression_fixtures.py` roda fixtures narrativas, design, pesquisa, render e template-selection |
| Dash/bench UI mostrando isso | Parcial | Expor score por route/import/runtime/eval, não só matriz |

## Próxima Wave Recomendada

### Wave 3 — Executable Skill Runtime

Objetivo: transformar contratos em execução verificável.

Prioridade:

1. `rendered-eval-runner`: HTML screenshot → scores `vision/content/logic/render`; validação do relatório já executada.
2. `regression-fixture-runner`: roda fixtures contra um deck package; runner mínimo já executado.
3. `export-job-runner`: task JSON → PDF/PPTX verificado.
4. `template-import-runner`: PPTX → manifest/summary/assets/import report.
5. `diagram-render-runner`: diagram manifest → SVG/PNG/native output verificado.
6. `package-validator-plus`: integrar chart, diagram, image resource e PPTX template checks; integração inicial executada.

Esta Wave deve ser tratada como runtime/CLI, não como mais documentação.

## Evidências Principais

Paths de origem analisados:

- `/Users/alan/Code/bench/PPTAgent/pptagent/ppteval.py`
- `/Users/alan/Code/bench/PPTAgent/pptagent/prompts/ppteval/*.txt`
- `/Users/alan/Code/bench/PPTAgent/deeppresenter/roles/Planner.yaml`
- `/Users/alan/Code/bench/PPTAgent/deeppresenter/roles/Research.yaml`
- `/Users/alan/Code/bench/PPTAgent/deeppresenter/html2pptx/html2pptx.js`
- `/Users/alan/Code/bench/PPTAgent/pptagent/document/document.py`
- `/Users/alan/Code/bench/PPTAgent/pptagent/roles/doc_extractor.yaml`
- `/Users/alan/Code/bench/PPTAgent/pptagent/templates/*/slide_induction.json`
- `/Users/alan/Code/bench/PPTAgent/pptagent/templates/*/image_stats.json`
- `/Users/alan/Code/bench/presentation-ai/src/components/notebook/presentation/utils/template-serializer.ts`
- `/Users/alan/Code/bench/presentation-ai/src/components/notebook/presentation/utils/templates.tsx`
- `/Users/alan/Code/bench/presentation-ai/src/components/notebook/presentation/charts/chart-data-editor/types.ts`
- `/Users/alan/Code/bench/presentation-ai/src/components/notebook/presentation/charts/chart-data-editor/use-chart-editor.ts`
- `/Users/alan/Code/bench/ppt-master/skills/ppt-master/references/image-type-templates/_index.md`
- `/Users/alan/Code/bench/ppt-master/skills/ppt-master/references/image-type-templates/hero.md`
- `/Users/alan/Code/bench/ppt-master/skills/ppt-master/references/image-type-templates/matrix.md`
- `/Users/alan/Code/bench/ppt-master/skills/ppt-master/scripts/template_import/manifest.py`
- `/Users/alan/Code/bench/powerpoint-skill/powerpoint-slides/diagram-rendering.md`
- `/Users/alan/Code/bench/PresentAgent-2/DeepResearch/inference/prompt.py`
- `/Users/alan/Code/bench/PresentAgent-2/DeepResearch/inference/prompt_media.py`
- `/Users/alan/Code/bench/PresentAgent-2/DeepResearch/inference/file_tools`
- `/Users/alan/Code/bench/PresentAgent-2/DeepResearch/evaluation`
- `/Users/alan/Code/bench/deepH/docs/AGENTS_AND_SPECS.md`
- `/Users/alan/Code/bench/deepH/docs/WORKFLOWS_AND_UNIVERSES.md`
- `/Users/alan/Code/bench/deepH/crews/reviewflow.yaml`
- `/Users/alan/Code/bench/presenton/servers/nextjs/lib/run-bundled-presentation-export.ts`
- `/Users/alan/Code/bench/banana-slides/scripts/export_editable_pptx.py`

## Decisão Final

Wave 2 está concluída como arquitetura de contratos. O score de completude da skill subiu porque agora o `slide-creator` cobre:

- estrutura narrativa;
- seleção de templates;
- pesquisa;
- ingestão documental;
- evidência;
- manuscript;
- importação de packs;
- render/export;
- image type routing;
- chart data validation;
- diagram engine routing;
- template manifest import;
- avaliação visual;
- trace;
- regressão.

O próximo ganho real não é escrever mais YAML. É implementar runners mínimos para executar esses contratos.
