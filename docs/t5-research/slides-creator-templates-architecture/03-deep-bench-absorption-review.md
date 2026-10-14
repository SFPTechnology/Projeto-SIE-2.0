# Deep Bench Absorption Review — Slides Creator

Data: 2026-05-18

## Objetivo

Revisar os benches em profundidade suficiente para separar:

1. o que já foi absorvido de forma útil;
2. o que foi apenas citado no bench, mas ainda não virou mecanismo;
3. o que ficou praticamente invisível e deveria entrar no próximo desenho da `slide-creator`.

## Diagnóstico principal

A absorção atual está boa em **taxonomia** e **contratos declarativos**, mas ainda fraca em **mecanismos de execução**.

Em termos simples: já sabemos nomear os padrões, mas ainda não estamos usando todos os mecanismos que fazem os melhores benches serem confiáveis em produção.

## Achados aprofundados por bench

### 1. `ppt-master`: anti-drift visual ainda está subabsorvido

O bench anterior capturou “native editable PPTX” e “template import”, mas o ponto mais profundo do `ppt-master` é outro: ele separa o design em dois níveis.

| Camada | Função |
|---|---|
| `design_spec.md` | explica o porquê visual, para humano e estratégia |
| `spec_lock.md` | trava o quê exato será executado: HEX, fontes, assets, charts, image composition |

O valor real é o **anti-drift**: antes de cada página, o executor relê o contrato curto e não reinterpreta o design inteiro. Isso combate variação de cor, fonte, estilo de imagem e composição ao longo de decks grandes.

**Gap nosso:** temos `theme-tokens.yaml`, `design-direction.yaml` e `deck-spec.yaml`, mas ainda não temos um artifact equivalente a `spec_lock.md` com regra “re-read before every slide”.

**Absorção recomendada:** criar `render-lock.yaml`.

Campos mínimos:

- canonical colors;
- font stacks;
- chart palette;
- image rendering style;
- image palette policy;
- image type per slide;
- allowed layout composition ids;
- forbidden SVG/PPTX features;
- source asset status.

### 2. `ppt-master`: composição visual por Primary + Modifier ficou rasa

O `ppt-master` não pensa imagem como “layout com foto”. Ele tem uma gramática de composição:

- Primary Structures: bones do slide;
- Modifier Layers: acabamento visual, overlay, clipping, annotation, texture.

O ponto crítico é que a composição fica declarada antes da geração. Exemplo conceitual: `#38 + #12 + #51`, não “coloque uma imagem bonita”.

**Gap nosso:** `ai-image-type-routing.yaml` define tipos de imagem, mas ainda não define composição como expressão auditável de camadas.

**Absorção recomendada:** criar `visual/composition-patterns.yaml` com:

- primary_structure;
- modifier_layers;
- native_overlay_plan;
- forbidden_if_pptx_editable;
- fallback_for_powerpoint;
- audit_id.

### 3. `ppt-master`: runners-up de chart/template são parte da auditabilidade

O `design_spec_reference.md` exige “runners-up considered” para charts: não basta dizer o escolhido; deve registrar os segundos melhores e por que foram rejeitados.

**Gap nosso:** temos `selected_template_reason`, mas não exigimos alternativas rejeitadas.

**Absorção recomendada:** todo `template-selection-report.yaml` deve registrar:

- selected;
- selected_reason;
- rejected_runners_up mínimo 2 ou 3;
- reason_by_deck_specifics;
- source index quote quando houver.

Isso melhora muito o QA porque transforma escolha visual em decisão revisável.

### 4. Presenton: schema validation before save ainda não virou regra forte

Presenton tem um protocolo muito importante:

- tool output/live deck state vence memória;
- antes de salvar slide, buscar schema do layout;
- `saveSlide` valida JSON Schema;
- se falhar por `maxLength`, encurtar automaticamente e tentar salvar de novo;
- só declarar sucesso se `saved:true`.

**Gap nosso:** os templates têm schemas, mas o fluxo da skill ainda pode “gerar deck-spec bonito” sem simular uma operação de save com validação de layout.

**Absorção recomendada:** criar `scripts/validate_slide_template_payloads.py` ou expandir `validate_deck_package.py` para validar cada slide contra o schema do template selecionado.

### 5. Presenton: source-of-truth policy para memória vs deck vivo

Presenton trata memória como contexto potencialmente stale. Ferramentas do turno são a verdade.

**Gap nosso:** em processos longos, a skill pode misturar briefing, process log, deck antigo e revisão nova sem declarar qual fonte vence.

**Absorção recomendada:** adicionar `source_of_truth_policy` ao package:

1. rendered/exported artifacts;
2. latest deck-spec;
3. explicit user constraints;
4. source ledger;
5. memory/research notes.

Quando houver conflito, o package deve registrar `conflict_resolution`.

### 6. PPTAgent / PresentAgent-2: constraints de layout estão mais fortes do que capturamos

O `Layout` do PPTAgent contém:

- elemento tipado;
- quantidade default;
- suggested_characters;
- variable_length;
- vary_mapping;
- validação de mídia local;
- rewrite automático de texto longo.

**Gap nosso:** `slide/function-library.yaml` descreve função narrativa, mas ainda não impõe com força:

- character budget por slot;
- quantidade mínima/máxima por slot;
- layout variant por cardinalidade;
- rewrite automático quando excede limite;
- validação de asset local.

**Absorção recomendada:** evoluir `slide-template.schema.yaml` e templates de slide com:

```yaml
slots:
  - id: insight
    type: text
    suggested_characters: 72
    max_characters: 110
    rewrite_if_exceeds: true
  - id: evidence_visual
    type: image
    required_when: ["slide_function == proof"]
    must_exist_locally: true
variable_layouts:
  by_item_count:
    2: two_column
    3: three_card
    4: grid_2x2
```

### 7. PresentAgent-2: speaker notes preservation ficou subvalorizado

O parser/build preserva speaker notes ao reconstruir PPTX.

**Gap nosso:** tratamos speaker notes como output textual opcional, mas não como parte da fidelidade do deck.

**Absorção recomendada:** `deck-spec.yaml` e futuro Native IR devem ter `speaker_notes` por slide com:

- delivery_mode: palco/live/async;
- source_refs;
- timing_seconds;
- must_export_to_pptx_notes: true.

QA deve bloquear quando notes existem no spec mas desaparecem no export.

### 8. `presentation-ai`: edit history ainda está muito genérico

Já absorvemos `edit-history.yaml`, mas o código real traz detalhes que devem virar regra:

- snapshots limitados;
- change type `slide | theme | full`;
- rate limit para mesma alteração;
- merge de mudanças rápidas;
- bloqueio de history push durante restore;
- undo/redo com restauração de tema e slide.

**Gap nosso:** temos contrato, mas ainda não temos formato de snapshot suficientemente operacional.

**Absorção recomendada:** `edit-history.yaml` deve incluir:

- `before_deck_spec_hash`;
- `after_deck_spec_hash`;
- `restoring_guard`;
- `future_cleared`;
- `merged_with_previous`;
- `theme_snapshot`;
- `changed_slide_snapshot`;
- `full_snapshot_ref`.

### 9. `banana-slides`: job lifecycle precisa virar runtime contract, não só inspiração

O CLI de banana trata jobs como entidades:

- `job_id`;
- `job_type`;
- `creation_type`;
- export formats;
- policy timeout/continue_on_error;
- progress events;
- task polling;
- resumibilidade.

**Gap nosso:** `runtime/jobs.yaml` tem etapas, mas ainda não define schema de execução.

**Absorção recomendada:** criar `runtime/job-state.schema.yaml`.

Campos mínimos:

- job_id;
- run_id;
- job_type;
- mode;
- inputs;
- task_records;
- progress_events;
- artifacts;
- export_policy;
- timeout_sec;
- resume_from;
- error_details;
- final_verdict.

### 10. `deepH`: precisamos de trace antes de executar decks caros

`deepH` traz uma capacidade não óbvia para slides: `trace` antes de `run`.

Para decks caros, deveríamos conseguir mostrar:

- quais stages vão rodar;
- quais artifacts entram e saem;
- quais handoffs existem;
- quais revisores paralelos serão usados;
- qual contexto será descartado.

**Gap nosso:** `trace-handoff.yaml` existe, mas o workflow da skill ainda não exige `trace_report` antes de decks complexos.

**Absorção recomendada:** adicionar modo obrigatório:

```yaml
preflight_trace_required_when:
  - source_count > 3
  - slide_count > 12
  - delivery_format includes pptx
  - research_required == true
  - user asks to share skill/process
```

### 11. `deepH`: review multiverse deve virar critique mode do slide package

O `reviewflow` roda universos diferentes e sintetiza.

**Gap nosso:** critique loop existe, mas ainda não está formalizado como branches independentes com handoff máximo e output kind.

**Absorção recomendada:** `rendered-eval.yaml` e `trace-handoff.yaml` devem aceitar branches:

- baseline;
- strict;
- narrative_focus;
- design_focus;
- render_focus;
- proof_focus;
- synth.

Cada branch deve produzir `parsed_findings`, não apenas texto.

### 12. `powerpoint-skill`: QA técnico precisa separar limites do PowerPoint e do LibreOffice

O bench deixa claro que LibreOffice não renderiza OMML corretamente; isso não deve virar falso bug visual.

**Gap nosso:** `pptx-technical-gates.yaml` fala de OMML, mas não separa suficientemente:

- XML validation;
- PowerPoint expected behavior;
- LibreOffice/PDF limitation;
- visual screenshot limitation.

**Absorção recomendada:** adicionar `validation_surface` por gate:

- `pptx_xml`;
- `powerpoint_open`;
- `libreoffice_pdf`;
- `screenshot`;
- `manual_powerpoint_check`.

## Matriz de absorção real

| Capability | Já temos? | Profundidade atual | Gap |
|---|---:|---|---|
| Template catalog | Sim | Boa | Falta runners-up e validation by selected schema |
| Theme tokens | Sim | Média | Falta `render-lock.yaml` anti-drift |
| Image type routing | Sim | Boa | Falta Primary + Modifier composition expression |
| PPTX technical gates | Parcial | Média | Falta validator real de geometry/XML completo |
| Edit history | Parcial | Média | Falta snapshot hash, undo/redo semantics e rollback real |
| Job lifecycle | Parcial | Baixa | Falta schema de task/progress/resume |
| Template induction | Parcial | Média | Falta execução com confidence/retry/local asset validation |
| Speaker notes | Parcial | Baixa | Falta QA de preservação no export |
| Source of truth policy | Não | Baixa | Falta regra explícita de conflito |
| Trace before run | Parcial | Média | Falta gate obrigatório para decks caros |
| Multiverse critique | Parcial | Média | Falta parsed findings e branches formais |
| Schema validation before save/render | Parcial | Baixa | Falta validar slide payload contra template schema |

## O que devemos implementar primeiro

### P0.1 — `render-lock.yaml`

Maior impacto na qualidade visual consistente. Absorve o verdadeiro coração do `ppt-master`.

### P0.2 — `job-state.schema.yaml`

Sem job lifecycle, CLI/API/MCP viram comandos frágeis, não produto operável.

### P0.3 — `template-selection-report.yaml` com runners-up

Melhora inteligência e auditabilidade sem precisar de renderer novo.

### P0.4 — validação de slide payload contra schema selecionado

Impede que a skill gere slides incompatíveis com seus próprios templates.

### P0.5 — speaker notes como artifact exportável e testável

Essencial para webinars, aulas e decks async.

## Conclusão

A próxima melhoria profunda não é adicionar mais dezenas de templates. É transformar a skill de “biblioteca de bons padrões” em um **sistema de execução com locks, traces, snapshots, jobs e validação por schema**.

O caminho mais curto para subir de patamar:

1. `render-lock.yaml`;
2. `job-state.schema.yaml`;
3. `template-selection-report.yaml`;
4. `slide payload schema validation`;
5. `speaker notes preservation gate`;
6. `multiverse critique parsed findings`.

Essas seis peças absorvem mais inteligência dos benches do que ampliar o catálogo visual neste momento.
