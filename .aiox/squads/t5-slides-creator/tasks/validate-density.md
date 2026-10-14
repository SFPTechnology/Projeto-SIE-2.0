# Task: Validate Density (Design sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-density` |
| phase | P05 + P04.5 (critique loop) |
| bounded_context | BC-06 (QA) |
| invariants_enforced | P2 |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.design.sub_dimensions.density |
| killer_items | KI-04 (texto cortado) — quando density extrema causa overflow |
| session | SESSION-QA |
| duration | <10s |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-005) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateDensity
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # deterministic structural check + WCAG-like numeric thresholds
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
  - name: design_direction
    type: YAML
    source: "{output_dir}/design-direction.yaml"
    schema_ref: squads/slides-creator/data/design-direction.schema.yaml
  - name: grid_layouts
    type: YAML
    source: "{output_dir}/grid-layouts.yaml"
```

### 5. Outputs
```yaml
Outputs:
  - name: density_report
    type: YAML
    destination: "{output_dir}/validator-reports/density.yaml"
    schema:
      dimension: density
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      findings:
        - slide_id: string
          claims_governing_count: integer
          claims_supporting_count: integer
          visual_elements_count: integer
          text_chars_count: integer
          violations: "array<string>"
          severity: "low | medium | high | critical"
      summary:
        slides_total: integer
        slides_pass: integer
        slides_review: integer
        slides_fail: integer
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Carregar deck_spec, design_direction, grid_layouts."
  - id: 2
    action: "Para cada slide em deck_spec.slides:"
    sub_actions:
      - "Contar claims_governing (max permitido: design_direction.density_limits.max_claims_governing_per_slide, default 1)"
      - "Contar claims_supporting (max permitido: design_direction.density_limits.max_claims_supporting_per_slide, default 3)"
      - "Contar visual_elements (max permitido: design_direction.density_limits.max_visual_elements_per_slide, default 4)"
      - "Contar text_chars total (max permitido: design_direction.density_limits.max_text_chars_per_slide, default 280)"
      - "Verificar forbidden_patterns (e.g., '5+ cards iguais em grid', 'Bullet list > 5 itens')"
  - id: 3
    action: "Calcular dimension_score: 10 - (2 × % slides com violação crítica) - (0.5 × % slides com violação medium)."
  - id: 4
    action: "Verdict: PASS if score >= 7 AND zero violations critical; REVIEW if 7 > score >= 5; FAIL if score < 5 OR any slide com violação critical não justificada."
  - id: 5
    action: "Emit density.yaml com findings detalhados (slide_id + violations + suggestion)."
  - id: 6
    action: "Append entry em planning-reflection.jsonl: {phase:'critique', entry_type:'critique', dimension:'density', findings_count, score, decision}."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Validator executa em <10s para deck de 30 slides"
  - "Verdict PASS apenas se TODAS slides respeitam max_claims_governing (1) AND max_claims_supporting"
  - "Findings array contém slide_id + lista exata de violações por slide"
  - "Dimension_score reflete proporção de slides com violação (não soma absoluta)"
  - "Forbidden_patterns explícitos no design_direction são checados e reportados"
  - "Entry em planning-reflection.jsonl segue planning-reflection.schema.json"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_DENSITY_REPORT
handoff_to: qa-inspector  # consume in qa-report aggregation
on_fail_route: per data/qa-routing-table.yaml#dimension_failed=density → @design-renderer + tasks/compose-grid-layout.md
```

## Scoring Detail

```
dimension_score = 10
  - (4 × pct_slides_critical_violations)
  - (1.5 × pct_slides_high_violations)
  - (0.5 × pct_slides_medium_violations)

clamp(score, 0, 10)
```

## Edge Cases

- Slide cover (function=cover): max_claims_governing=1, max_supporting=0
- Slide artifact_reveal: max_claims_governing=1, max_supporting=1 (foco no artefato)
- Slide chart/data: visual_elements pode incluir 1 chart + legend + caption (counted as 3, not 1)
- Slide quote: text_chars cap reduzido para 180

## Calibração

- Fixture gold-standard: `squads/slides-creator/examples/gold-standard-slide-spec.md` deve scorear >=9
- Fixture known-bad: `outputs/webinars/primeiro-servico-ia/draft-slides-aiox.html` deve scorear <=5 (multiple supporting overflows)
