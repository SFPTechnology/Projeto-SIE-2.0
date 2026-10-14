# Task: Define Design Direction

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `define-design-direction` |
| phase | P03 (Design) — PRE-REQUISITE de compose-grid-layout |
| bounded_context | BC-02 (Visual) + BC-05 (Brand) |
| schema_ref | data/design-direction.schema.yaml |
| killer_items_prevented | KI-10 |
| session | SESSION-SPEC |
| duration | <60s (LLM call + brand resolution) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-015B, GAP-010 closure) |
| case_study | outputs/webinars/primeiro-servico-ia/ |
| model_params | temperature=0.3, model=sonnet |

## Why this task exists

Lição empírica: Primeiro Serviço de IA v1 aplicou identidade AIOX como skin (cores+logo+tipografia) sem deck-stage real, sem referência visual, sem motivo dominante. Resultado: wireframe bonito-mas-vazio. Esta task **força declaração explícita** de design direction ANTES do primeiro render.

## SINKRA Task Anatomy

### 1. task
```yaml
task: defineDesignDirection
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # semantic judgement + brand resolution
```

### 4. Inputs
```yaml
Inputs:
  - name: normalized_briefing
    type: JSON
  - name: story_arc
    type: YAML
    source: "{output_dir}/story-arc.yaml"
  - name: slide_function_map
    type: YAML
    source: "{output_dir}/slide-function-map.yaml"
  - name: brand_config
    type: optional
    source: "workspace/businesses/{slug}/L2-tactical/brand/"
    desc: "se deck tem brand owner — caso contrário derive de briefing"
  - name: visual_reference_hints
    type: optional
    source: "briefing.normalized.json#references"
    desc: "URLs, paths, ou descriptions de referências fornecidas"
```

### 5. Outputs
```yaml
Outputs:
  - name: design_direction
    type: YAML
    destination: "{output_dir}/design-direction.yaml"
    schema_ref: squads/slides-creator/data/design-direction.schema.yaml
    lifecycle: [draft, validated, approved]
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Resolver brand_ref:"
    sub_actions:
      - "Se brand_config presente → brand_ref = workspace/businesses/{slug}/L2-tactical/brand/"
      - "Senão → brand_ref = null (deck brand-agnostic)"

  - id: 2
    action: "Determinar visual_reference (OBRIGATÓRIO, KI-10):"
    sub_actions:
      - "Se briefing.references presente → type = external_url OR prior_deck (parsear paths)"
      - "Se brand tem reference-decks/ → type = prior_deck"
      - "Senão → REQUEST: 'Briefing não fornece referência visual. Propor 2-3 referências do mood (e.g., Pentagram editorial, Y Combinator demo, Apple keynote) para Mission Lead escolher.'"
      - "type cannot be empty. paths cannot be []. notes obrigatório (>=30 chars)."

  - id: 3
    action: "Determinar dominant_motif (OBRIGATÓRIO):"
    sub_actions:
      - "name: específico, não buzzword. 'modern/clean/minimal/professional' rejected — força segunda iteração."
      - "rationale: por que este motif para esta audiência + arc_type"
      - "rendered_as: lista concreta (paddings, bordas, fundos, decorações declarados)"

  - id: 4
    action: "Determinar density_limits:"
    sub_actions:
      - "max_claims_governing_per_slide: 1 (hard cap, schema enforces)"
      - "max_claims_supporting_per_slide: derived from arc_type (workshop=3, pitch=2, sales=2)"
      - "max_visual_elements_per_slide: derived from audience.viewing_mode (mobile=3, projection=5)"
      - "max_text_chars_per_slide: derived from viewing_distance (near=320, medium=240, far=160)"
      - "forbidden_patterns: lista. SEMPRE incluir '5+ cards iguais em grid' (Primeiro Servico lesson)"

  - id: 5
    action: "Determinar variation_rules:"
    sub_actions:
      - "layouts_count_min: max(4, ceil(total_slides * 0.4)) — garante variedade"
      - "layout_repetition_max: 3"
      - "quiet_slide_ratio_min: 0.15-0.25 conforme audience_context"
      - "accent_color_density: sparse default, dense apenas para sales arc"
      - "motion_policy: subtle_transitions default"

  - id: 6
    action: "Determinar composition_rules + palette_constraints + typography_constraints:"
    sub_actions:
      - "Derive de brand tokens quando presentes"
      - "Defaults SINKRA quando ausente brand"

  - id: 7
    action: "Determinar audience_context:"
    sub_actions:
      - "viewing_mode: extraído de briefing"
      - "viewing_distance: derivado de viewing_mode"
      - "audience_size: explícito OR inferred"
      - "attention_budget_minutes: explícito OR 45 default"

  - id: 8
    action: "Emit design-direction.yaml."

  - id: 9
    action: "Self-validate contra schema. Se falha → HALT + report exato campo missing."

  - id: 10
    action: "Append planning-reflection.jsonl: {phase:'design_planning', entry_type:'decision', dimension:'visual_coherence', claim:'direction chosen: {motif.name}', evidence:'visual_reference={paths}', decision}."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "design-direction.yaml válido contra schema"
  - "visual_reference.paths não-vazio (>=1 path real)"
  - "dominant_motif.name não é buzzword (rejected: modern/clean/minimal/professional)"
  - "density_limits.max_claims_governing_per_slide == 1"
  - "variation_rules.layouts_count_min >= 4"
  - "audience_context completo"
  - "Self-validation PASS antes de handoff"
  - "Calibração: rodar contra Primeiro Servico v3 retrospective deve gerar design-direction.yaml comparable to example no schema"
```

### 8. handoff_token
```yaml
handoff_token: BC-02_DESIGN_DIRECTION
handoff_to:
  - "@design-renderer (consumes for compose-grid-layout)"
  - "@visual-scout (consumes palette_constraints)"
  - "@design-planner (consumes for critique loop direction enforcement)"
pre_condition_for: "tasks/compose-grid-layout.md (RH-005 mitigation: render only after direction)"
```

## Anti-Patterns

- **Buzzword direction:** "modern/clean/minimal". Rejected automatically.
- **Empty visual_reference:** Triggers KI-10. HALT até resolve.
- **Skin-only:** brand tokens declarados mas nenhuma visual_reference concreta. KI-10.
- **Audience_context vazio:** decisões visuais sem contexto = chute. FAIL.

## Iteration Logic

Se Mission Lead OR @slide-chief rejeitar primeira direção:
1. Append rejection entry em planning-reflection.jsonl
2. Re-run com hints adicionais (motif preferido, refs preferidas)
3. Cap 2 iterations de direção. Após, escalate.
