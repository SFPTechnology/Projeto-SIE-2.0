# Underused Bench Assets — Slides Creator

Data: 2026-05-18

## Veredito

O benchmark já capturou os grandes blocos corretos, mas ainda estamos deixando valor prático na mesa. O principal gap não é “mais pesquisa”; é transformar padrões observados nos benches em contratos executáveis do `slide-creator` e em tarefas do `squads/slides-creator`.

## O que ainda está subaproveitado

| Prioridade | Fonte | Asset subaproveitado | Valor real | Absorção recomendada |
|---|---|---|---|---|
| P0 | `powerpoint-skill` | QA XML/PPTX determinístico (`check_overlaps.py`, `inject_omml.py`, `thumbnail.py`, `soffice.py`) | Bloqueia decks quebrados antes de julgamento estético. | Criar `pptx-technical-report.yaml` e task `validate-pptx-technical-output` no squad. |
| P0 | `PresentAgent-2` / PPTAgent | Indução de layout por template real: cluster visual, `functional_keys`, schema extraction + retry | Permite aprender com PPTX de cliente sem copiar template manualmente. | Evoluir `induced-layout-packs.yaml` para contrato de execução com score de confiança, contagem de slots, media area e retry. |
| P0 | `presentation-ai` | Histórico de edição por snapshot, undo/redo, rate-limit e merge de mudanças | Sem isso, prompt-to-edit vira operação destrutiva e difícil de auditar. | Transformar `runtime/edit-history.yaml` em contrato obrigatório para qualquer edit operation. |
| P0 | `banana-slides` | Job lifecycle: task_id, wait/resume, progress events, export policy, batch JSONL/CSV | Necessário para CLI/API/MCP confiáveis e retomáveis. | Expandir `runtime/jobs.yaml` com `task_record`, `progress_events`, `resume_policy` e `artifact_records`. |
| P1 | `presentation-ai` | DSL XML semântica (`SECTION`, `COLUMNS`, `COMPARE`, `CHART`, `IMG`) | Boa ponte entre LLM e render sem prender a um frontend. | Adicionar `slide-structure-dsl.yaml` como IR semântico anterior ao `deck-spec.yaml`. |
| P1 | `presentation-ai` | Share/publication workflow e authorization | Gamma não é só geração; distribuição importa. | Criar `deck-publication.yaml` com permissões, share status e analytics hooks. |
| P1 | `PresentAgent-2` | PPT → vídeo: PDF frames, TTS por slide, overlays de vídeo embutidos, merge FFmpeg | Diferencial forte para webinar/aula/demo. | Criar `runtime/video-export.yaml` como P2, mas já reservar contrato. |
| P1 | `powerpoint-skill` | Tema técnico com masters, semântica de cores e regra de math/diagram | Evita “deck bonito que quebra no PowerPoint”. | Separar `theme-tokens.yaml` em visual theme + technical render theme. |
| P1 | `banana-slides` | Editable PPTX reverse export por análise recursiva de imagem + inpaint | Útil para recuperar decks rasterizados, com risco de licença. | Absorver apenas o padrão: `raster-to-editable-recovery.yaml`, sem copiar código. |
| P2 | `PresentAgent-2` | Q&A/interação e research dossier persistido | Cria pós-deck: responder perguntas com base em slides/fontes. | Criar `deck-knowledge-index.yaml` depois do renderer estabilizar. |

## Gaps do bench atual

1. **Bench diz que está 100/100, mas isso mede completude de decisão, não absorção operacional.**
   O score está correto como benchmark, mas não deve ser confundido com produto pronto. Falta uma coluna explícita: `absorbed_into_skill`, `absorbed_into_squad`, `implemented_runtime`.

2. **As decisões ainda estão pouco rastreadas até arquivos concretos da skill.**
   `templates/index.yaml` lista muitos padrões absorvidos, mas não há um mapa mecânico dizendo qual capability virou qual arquivo, qual script valida e qual task usa.

3. **Prompt-to-edit ainda está conceitual demais.**
   Temos operações (`change_theme`, `regenerate_slide`, etc.), mas falta o contrato de diff: antes/depois, região afetada, preservações, rollback e QA local.

4. **Indução de template ainda é descritiva, não executável.**
   `induced-layout-packs.yaml` já absorveu a ideia, mas precisa virar pipeline com input/output validável: slide images, layout clusters, content schema, confidence, retry log.

5. **PPTX técnico ainda não está no centro.**
   O bench aponta PPTX editável como P0, mas a skill ainda está mais forte em narrativa/contratos do que em gates técnicos de PowerPoint.

6. **Jobs não têm estado operacional suficiente.**
   `runtime/jobs.yaml` descreve presets, mas ainda não especifica `task_id`, `status`, `progress`, `resume_from`, `timeout`, `artifacts`, `error_details` e `retry_policy` com a maturidade de banana-slides/PresentAgent-2.

## Próximas absorções recomendadas

### Wave A — Fechar rastreabilidade bench → skill → squad

Criar `docs/bench/slides-creator-templates-architecture/03-absorption-traceability-matrix.md` com:

- capability;
- bench source;
- evidence path;
- target file in `.claude/skills/slide-creator`;
- target file/task in `squads/slides-creator`;
- status: `documented`, `contracted`, `validated`, `runtime`;
- next action.

### Wave B — Tornar edição auditável

Evoluir `runtime/edit-history.yaml` para incluir:

- operation id;
- user intent;
- target slide/region;
- locked elements;
- before hash;
- after hash;
- diff summary;
- rollback pointer;
- QA gates run after edit.

### Wave C — Tornar jobs retomáveis

Evoluir `runtime/jobs.yaml` com:

- `task_record`;
- `progress_events`;
- `artifact_records`;
- `resume_policy`;
- `export_policy`;
- `failure_policy`;
- `batch_input_schema`.

### Wave D — Tornar template induction executável

Evoluir `import/induced-layout-packs.yaml` com:

- `source_pptx`;
- `slide_images`;
- `functional_clusters`;
- `layout_clusters`;
- `content_schema`;
- `media_area_stats`;
- `selection_confidence`;
- `retry_log`;
- `blocked_reasons`.

### Wave E — Elevar PPTX técnico a gate obrigatório

Criar ou expandir:

- `templates/qa/pptx-technical-gates.yaml`;
- `scripts/check_pptx_placeholders.py`;
- futuro `scripts/check_pptx_geometry.py`;
- task `validate-pptx-technical-output.md` no squad.

## Decisão de arquitetura

O próximo salto não vem de copiar mais templates visuais. Vem de absorver quatro sistemas operacionais dos benches:

1. **PPTX técnico determinístico** de `powerpoint-skill`.
2. **Template induction** de PPTAgent/PresentAgent-2.
3. **Edit history/diff** de `presentation-ai`.
4. **Job lifecycle retomável** de `banana-slides`.

Esses quatro blocos aumentam mais a qualidade real da skill do que adicionar mais 30 roteiros.
