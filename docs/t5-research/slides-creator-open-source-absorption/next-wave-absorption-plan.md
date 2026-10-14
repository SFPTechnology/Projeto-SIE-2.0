# Next Wave Absorption Plan — slide creator skill

Data: 2026-05-18

## Tese

A próxima wave não deve tentar melhorar “slides” de forma genérica. O mapa 108D mostra que a skill já é forte em narrativa, planejamento, QA, templates e governança. O que ainda impede a skill de ficar competitiva contra os melhores players é a falta de runtime operacional: PPTX nativo editável, renderer PPTX real, editor com estado/diff, pacote de execução local e materialização do contrato CLI/API/MCP recém-adicionado.

Objetivo da wave: transformar o bench em execução mensurável, fechando os maiores gaps ponderados sem diluir o diferencial narrativo da skill.

## Linha de Base

| Métrica | Valor atual |
|---|---:|
| Score atual da skill | 77.93 |
| Microdimensões | 108 |
| Células avaliadas | 972 |
| Gaps contra líder | 72 |
| Vantagens/empates da skill | 36 |
| P1 abertos | 38 |
| P2 abertos | 34 |

## Onde Está o Débito Real

| Cluster | Débito ponderado | Gaps | Líderes principais | Leitura |
|---|---:|---:|---|---|
| Editor | 760.67 | 15 | presentation-ai, banana-slides, ppt-master | Maior gap: canvas, estado, blocos, diff, prompt-to-edit e edição por alvo. |
| Renderização | 434.01 | 12 | ppt-master | Segundo gap estrutural: DrawingML, roundtrip PowerPoint e política nativo vs raster. |
| Automação | 309.33 | 9 | Presenton, slide-deck-ai | Falta converter skill em runtime consumível por CLI/API/MCP. |
| Infra | 287.68 | 6 | Presenton | Falta instalação local, workspace, storage, logs e operação offline simples. |
| Multimídia | 223.35 | 6 | PresentAgent-2, ppt-master | Alto valor, mas não bloqueia a próxima versão operacional. |
| Distribuição | 201.33 | 6 | presentation-ai | Share/export/permissões são importantes depois de runtime e renderer. |

Conclusão: a próxima wave deve atacar `Renderização + Editor mínimo + Infra + materialização CLI/API/MCP` e precisa incluir uma trilha explícita de `Design 100`. Multimídia, analytics, colaboração realtime e desktop ficam como Wave seguinte.

## Meta de Score

| Cenário | Hipótese | Score projetado |
|---|---|---:|
| Só Renderização para 90 | fecha PPTX nativo mínimo | 74.88 |
| Renderização + Automação para 90 | renderer + CLI/API/MCP | 77.14 |
| Renderização + Automação + Infra para 90 | runtime self-hosted utilizável | 79.62 |
| Top 20 gaps para 90 | fecha maior parte dos gaps P1 | 80.99 |
| Todos P1 para 90 | wave P1 completa | 82.06 |
| Todos P1 para 95 | P1 perto de referência | 83.41 |

Meta realista da próxima wave: **score >= 82** por implementação executável, não por novos contratos. Score 100 operacional exige waves posteriores de editor completo, distribuição, multimídia, desktop e analytics.

Meta específica de Design: levar as 9 microdimensões de Design para faixa `95-100`, com evidência executável. Isso exige manifest de template/brand, runtime de tema, revisão renderizada dos slides-chave e relatório de regressão visual. Não basta trocar cores, fontes ou adicionar mais templates.

## Princípios de Execução

1. CLI primeiro: cada capability precisa funcionar via comando antes de virar UI.
2. Contrato antes de engine: schema, fixtures e QA vêm antes de renderização sofisticada.
3. Código permissivo pode ser absorvido; AGPL/no-license vira inspiração comportamental, não cópia.
4. Todo score atualizado precisa apontar para evidência: arquivo, fixture, comando, output ou relatório.
5. Nada pode regredir os 22 pontos fortes da skill: narrativa, SCQA/Pyramid, action titles, QA e documentação.

## Wave 3 — Runtime Editável e Operável

### W3.0 — Baseline Reprodutível de Absorção

Fonte: `ppt-master`, Presenton, `presentation-ai`, `banana-slides`, `slide-deck-ai`.

Entregas:

- `outputs/bench/slides-ai/ppt-master/` com input, comando, hash, PPTX, PDF e screenshots.
- `outputs/bench/slides-ai/presenton/` com prompt, documento, API/local run e artifacts.
- `outputs/bench/slides-ai/presentation-ai/` com leitura de editor/state/theme e screenshots quando viável.
- `outputs/bench/slides-ai/banana-slides/` apenas como análise de padrão, isolado por risco de licença.
- `docs/bench/slides-creator-open-source-absorption/deep/wave-3-evidence-ledger.md`.

Critérios de aceite:

- Cada referência usada em implementação tem evidência local mínima.
- Cada evidência registra licença, risco de cópia e modo permitido de absorção.
- Nenhuma decisão depende de memória ou suposição sem arquivo rastreável.

### W3.1 — Native IR + Renderer MVP

Fonte primária: `ppt-master`. Fonte secundária: `powerpoint-skill`.

Microgaps fechados:

- `native_pptx_objects__drawingml_shapes`
- `native_pptx_objects__powerpoint_reopen_fidelity`
- `native_pptx_objects__image_vs_object_policy`
- `render_fidelity__roundtrip_powerpoint`
- `render_fidelity__pptx_editability_inspection`

Entregas:

- `native-slide-ir.schema.json`
- conversor `DeckSpec -> Native IR`
- renderer MVP com texto, shape, imagem, tabela simples e chart placeholder;
- `editability-report.json`
- fixtures de 5 decks: executivo, webinar, financeiro, técnico/arquitetura, brand/template.

Critérios de aceite:

- PowerPoint abre sem repair.
- Action titles e texto principal são editáveis.
- Relatório separa objeto nativo, imagem, raster fallback e unsupported.
- Fixture MVP atinge `editability_score >= 80`.
- Qualquer raster fallback precisa de motivo explícito.

### W3.2 — Runtime CLI/API/MCP

Fonte primária: Presenton. Fonte secundária: `slide-deck-ai`.

Microgaps fechados:

- `api_mcp_self_hosted__mcp_tools`
- `api_mcp_self_hosted__rest_endpoint`
- `api_mcp_self_hosted__async_job_artifacts`
- `api_mcp_self_hosted__stable_io_contract`
- `api_mcp_self_hosted__tool_safety_limits`
- `batch_automation__clear_cli`
- `batch_automation__ci_pipeline_fit`

Entregas:

- CLI `slides:generate`, `slides:review`, `slides:export`.
- API `POST /slides/generate`, `POST /slides/review`, `POST /slides/export`.
- MCP tools `slides.generate`, `slides.review`, `slides.export`.
- `job.json`, `status.json`, `artifacts.json`, `qa-report.json`.
- provider registry BYOK/local com modo dummy para smoke test.

Critérios de aceite:

- CLI, API e MCP chamam o mesmo core.
- Toda execução cria workspace por deck.
- Falhas retornam erro estruturado e preservam logs.
- Smoke test roda sem provider pago.
- Nenhum secret aparece em artifact, log ou resposta MCP.

### W3.3 — Operação Local Self-Hosted

Fonte primária: Presenton.

Microgaps fechados:

- `self_hosted_runtime__docker_compose`
- `self_hosted_runtime__local_offline_mode`
- `self_hosted_runtime__service_topology`
- `self_hosted_runtime__storage_logs_upgrade`
- `privacy_local_byok__explicit_byok`
- `privacy_local_byok__local_models`

Entregas:

- `docker-compose.yml` mínimo ou script local equivalente.
- estrutura de storage: inputs, working, exports, previews, logs, reports.
- `.env.example` sem segredo.
- modo `provider=dummy`, `provider=ollama` e BYOK.
- healthcheck local.

Critérios de aceite:

- Usuário consegue rodar localmente com README curto.
- Geração smoke funciona sem internet quando usando dummy/local.
- Logs são suficientes para debugar falha de geração, render e export.
- Upgrade não apaga workspaces existentes.

### W3.4 — Editor Mínimo com Diff

Fonte primária: `presentation-ai`. Fonte comportamental: `banana-slides`, sem cópia de código AGPL.

Microgaps fechados:

- `web_editor_runtime__canvas_editor`
- `web_editor_runtime__state_management_undo`
- `web_editor_runtime__rich_blocks`
- `prompt_to_edit__language_editing`
- `prompt_to_edit__diff_before_apply`
- `prompt_to_edit__target_slide_region_element`
- `prompt_to_edit__regenerate_only_needed_area`

Entregas:

- outline editor mínimo;
- preview por slide;
- modelo de edição por comando: `target`, `intent`, `patch`, `risk`, `diff`;
- undo/redo via histórico de DeckSpec;
- prompt-to-edit por slide, seção e elemento;
- before/after visual quando houver renderer disponível.

Critérios de aceite:

- Nenhuma edição por prompt aplica direto sem diff.
- Toda alteração gera patch reversível.
- Prompt-to-edit não reescreve o deck inteiro quando alvo é local.
- Histórico permite voltar ao estado anterior.
- O usuário vê o que vai mudar antes de aceitar.

### W3.4D — Design 100

Fonte primária: `ppt-master`. Fontes secundárias: `presentation-ai`, `banana-slides`, `powerpoint-skill`.

Microgaps fechados:

- `visual_layout_quality__layout_variety`
- `visual_layout_quality__rendered_visual_quality`
- `template_import_replication__template_manifest`
- `template_import_replication__brand_fidelity`
- `template_import_replication__template_selection_logic`
- `theme_tokens_branding__token_schema`
- `theme_tokens_branding__theme_runtime`
- `theme_tokens_branding__brand_guardrails`

Entregas:

- `templates/visual/design-mastery-contract.yaml` na skill.
- `brand-template-manifest.yaml` para qualquer deck com referência visual ou PPTX importado.
- `design-mastery-report.yaml` com score por lente: manifest, fidelidade, layout, render, tema e iteração.
- `key-slide-render-review.yaml` cobrindo cover, reframe, mecanismo, proof/demo e CTA.
- `visual-regression-checklist.yaml` para bloquear retorno a deck genérico.
- atualização de `qa/visual-gates.yaml` com brand fidelity, rendered quality e template replication.

Critérios de aceite:

- Slides decisivos passam revisão renderizada, não apenas revisão de spec.
- Layouts são escolhidos por função do slide e incluem runners-up rejeitados.
- Tema/tokens afetam texto, charts, diagramas, shapes, tabelas e imagens.
- Brand fidelity mede tipografia, grid, densidade, componentes, chart language e anti-padrões.
- Nenhum deck premium é finalizado com score de Design abaixo de 95.

### W3.5 — Bench Feedback Loop

Fonte: matriz 108D e dashboard bench.

Entregas:

- atualizar `comparison-matrix.json` só com evidência nova;
- atualizar `deep/slides-creator-micro-gap-map.*`;
- atualizar `scorecard.*`, `scenario-scorecards.*` e `bench-output-dash.json`;
- anexar outputs reais em evidence ledger;
- registrar deltas de score por microdimensão.

Critérios de aceite:

- Cada nota alterada tem `score_breakdown`, `score_reason` e evidência.
- Dashboard mostra antes/depois por cluster.
- O score da skill só sobe onde existe artifact executável ou contrato validado.
- Meta mínima da wave: `score >= 82`.

## Backlog Story-Ready

| Story | Prioridade | Entrega | Fonte | Gate |
|---|---|---|---|---|
| SLS-W3-001 | P0 | Baseline reprodutível dos players alvo | todos | evidence ledger completo |
| SLS-W3-002 | P0 | `native-slide-ir.schema.json` | ppt-master | schema valida fixtures |
| SLS-W3-003 | P0 | `DeckSpec -> Native IR` | ppt-master | 5 fixtures convertidas |
| SLS-W3-004 | P0 | Renderer PPTX MVP | ppt-master | PowerPoint abre sem repair |
| SLS-W3-005 | P0 | `editability-report.json` | ppt-master, powerpoint-skill | action titles editáveis |
| SLS-W3-006 | P0 | CLI core | slide-deck-ai, Presenton | smoke local passa |
| SLS-W3-007 | P0 | API runtime | Presenton | artifact contract estável |
| SLS-W3-008 | P0 | MCP tools | Presenton | sem vazamento de secrets |
| SLS-W3-009 | P0 | workspace/job/artifacts | Presenton | logs e status rastreáveis |
| SLS-W3-010 | P1 | provider registry | Presenton | dummy/local/BYOK |
| SLS-W3-011 | P1 | operação local | Presenton | healthcheck local |
| SLS-W3-012 | P1 | outline editor mínimo | presentation-ai | DeckSpec altera e persiste |
| SLS-W3-013 | P1 | prompt-to-edit com diff | banana-slides, presentation-ai | patch reversível |
| SLS-W3-014 | P1 | target por slide/elemento | banana-slides | não regenera deck inteiro |
| SLS-W3-015 | P1 | Design 100 contract | ppt-master, presentation-ai | design mastery report obrigatório |
| SLS-W3-016 | P1 | brand/template manifest | ppt-master | tokens/layouts/componentes auditáveis |
| SLS-W3-017 | P1 | rendered key-slide design review | powerpoint-skill, PPTAgent | slides decisivos >= 95 |
| SLS-W3-018 | P1 | atualização da matriz e dashboard | bench | score auditável |

## Fora de Escopo Nesta Wave

| Item | Motivo |
|---|---|
| Desktop app empacotado | Só faz sentido depois de runtime e renderer estáveis. |
| MP4/narração/Q&A multimodal | Alto valor, mas depende de deck e artifacts confiáveis. |
| Colaboração realtime | Prematuro antes de estado local, diff e histórico. |
| Analytics avançado | Requer share runtime e publicação. |
| UI rica estilo Gamma | Sem engine editável vira casca; entra depois do core. |

## Gates de Qualidade

1. `validate:yaml:changed` para artefatos YAML tocados.
2. Validador JSON/schema para Native IR, job, artifacts e QA.
3. Smoke CLI com provider dummy.
4. Roundtrip PPTX: gerar, abrir/extrair, validar objetos e exportar PDF.
5. QA de narrativa: tese, audience shift, action titles e CTA preservados.
6. QA de design: overflow, contraste, densidade, layout e placeholders.
7. QA de licença: nenhum código AGPL/no-license copiado.

## Riscos

| Risco | Severidade | Mitigação |
|---|---|---|
| Renderer nativo virar projeto grande demais | Alta | MVP por subset: texto, shape, imagem e tabela antes de animações/charts complexos. |
| Copiar padrão de projeto com licença restritiva | Alta | Absorver comportamento como contrato; implementar do zero quando licença impedir cópia. |
| API/MCP duplicar lógica da CLI | Média | Core único chamado por CLI/API/MCP. |
| Editor consumir a wave inteira | Média | Editor mínimo baseado em DeckSpec/diff, sem colaboração realtime. |
| Score subir sem evidência real | Alta | Matriz só muda com artifact, fixture, relatório ou comando reproduzível. |

## Definition of Done da Wave

A wave está concluída quando:

- há um caminho CLI local que gera DeckSpec, Native IR, PPTX, PDF e QA report;
- o PPTX tem objetos principais editáveis e abre sem repair;
- API e MCP expõem o mesmo core;
- prompt-to-edit gera diff reversível pelo menos por slide;
- bench e dashboard mostram score atualizado com evidência;
- a skill mantém liderança em narrativa, planejamento e QA.

## Próxima Decisão Após a Wave

Se o score ficar entre 82 e 84, a próxima wave deve priorizar editor completo e distribuição. Se ficar abaixo de 82, o gargalo provavelmente será renderização nativa ou runtime incompleto; nesse caso, não avançar para UI rica antes de fechar roundtrip/editability.
