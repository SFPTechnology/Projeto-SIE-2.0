# Task: Validate Readability (Design sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-readability` |
| phase | P05 + P04.5 |
| bounded_context | BC-06 (QA) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.design.sub_dimensions.readability |
| session | SESSION-QA |
| duration | <10s |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-008) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateReadability
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # numeric thresholds: line_length, font_size_min, viewing_distance
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
  - name: design_direction
    type: YAML
  - name: scale_standards
    type: YAML
    source: squads/slides-creator/data/scale-standards.yaml
```

### 5. Outputs
```yaml
Outputs:
  - name: readability_report
    type: YAML
    destination: "{output_dir}/validator-reports/readability.yaml"
    schema:
      dimension: readability
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      thresholds_applied:
        line_length_max_chars: integer
        font_size_min_body_pt: integer
        font_size_min_caption_pt: integer
        viewing_distance: "near | medium | far"
      findings:
        - slide_id: string
          element_id: string
          element_type: string
          line_length_chars: integer
          font_size_pt: integer
          violation_type: "long_line | small_font | dense_paragraph | bad_line_height"
          severity: "low | medium | high | critical"
      summary:
        slides_total: integer
        slides_pass: integer
        most_common_violation: string
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Resolver thresholds:"
    sub_actions:
      - "line_length_max_chars: design_direction.typography_constraints.line_length_max_chars (default 60)"
      - "font_size_min_body_pt: derivado de viewing_distance (near=14, medium=18, far=24)"
      - "font_size_min_caption_pt: max(10, body-4)"
  - id: 2
    action: "Para cada slide, varrer elementos textuais:"
    sub_actions:
      - "Verificar line_length (em chars) em cada linha — flag se > limite"
      - "Verificar font_size_pt em cada elemento — flag se < min para element_type"
      - "Detectar dense_paragraph: line_height_ratio < 1.3 em paragraph >= 3 linhas"
      - "Detectar bad_line_height: line_height_ratio < 1.1 OR > 2.0"
  - id: 3
    action: "dimension_score: 10 - violations weighted by severity."
  - id: 4
    action: "Verdict: PASS if zero critical AND <5% high."
  - id: 5
    action: "Findings sugerem fix concreto: 'reduce line length to 50 chars' OR 'upgrade caption from 10pt to 12pt'."
  - id: 6
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Line length validado per element (não per slide)"
  - "Font size validado contra viewing_distance dinamicamente"
  - "Densidade de parágrafo (line_height ratio) considerada"
  - "Findings concretos com sugestão de fix"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_READABILITY_REPORT
on_fail_route: per data/qa-routing-table.yaml → @design-renderer + tasks/compose-grid-layout.md
```

## Viewing Distance Map

| Distance | viewing_mode trigger | body_min_pt | title_min_pt |
|---|---|---|---|
| near | mobile_share, async_pdf intimate | 14 | 24 |
| medium | webinar_screen, async_pdf default | 18 | 32 |
| far | in_person_projection_large | 24 | 44 |
