# Task: Validate Contrast (Design sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-contrast` |
| phase | P05 + P04.5 |
| bounded_context | BC-06 (QA) |
| invariants_enforced | P2, WCAG AA |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.design.sub_dimensions.contrast |
| killer_items | KI-05 (contraste ilegível) |
| session | SESSION-QA |
| duration | <15s |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-007) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateContrast
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # WCAG contrast calc é determinístico
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
  - name: active_palette
    type: YAML
    source: "{output_dir}/active-palette.yaml"
  - name: design_direction
    type: YAML
  - name: wcag_threshold
    type: enum
    derived: "design_direction.audience_context.viewing_mode → in_person_projection=AAA(7), webinar/async=AA(4.5), small text=AAA(7)"
```

### 5. Outputs
```yaml
Outputs:
  - name: contrast_report
    type: YAML
    destination: "{output_dir}/validator-reports/contrast.yaml"
    schema:
      dimension: contrast
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      wcag_level_required: "AA | AAA"
      findings:
        - slide_id: string
          element_id: string
          fg_color: "hex"
          bg_color: "hex"
          contrast_ratio: "number"
          threshold: "number"
          passes: "boolean"
          severity: "critical | high | medium"
          element_type: "title | body | caption | decoration"
      summary:
        pairs_total: integer
        pairs_pass: integer
        pairs_fail: integer
        worst_ratio: "number"
        worst_slide: string
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Determine wcag_threshold a partir de design_direction.audience_context.viewing_mode."
  - id: 2
    action: "Para cada slide, extrair todos pares (fg_color, bg_color) de elementos textuais."
  - id: 3
    action: "Resolver cores via active_palette (CSS vars → hex). Se override não declarado, FAIL palette_adherence."
  - id: 4
    action: "Calcular contrast_ratio per WCAG 2.1 formula: (L1 + 0.05) / (L2 + 0.05) onde L = relative luminance."
  - id: 5
    action: "Comparar contra threshold. Texto pequeno (<18pt regular OR <14pt bold) usa AAA mesmo em modo AA."
  - id: 6
    action: "Decorações (não-textuais) precisam apenas de 3:1 minimum."
  - id: 7
    action: "dimension_score: 10 - (5 × pct_pairs_fail_critical) - (1 × pct_pairs_fail_high)."
  - id: 8
    action: "Verdict: FAIL se ANY pair fails threshold em element_type='title' OR 'body'. KI-05 disparado."
  - id: 9
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Toda par fg/bg testado contra WCAG 2.1 contrast ratio"
  - "Threshold escalado por viewing_mode: in_person_projection=AAA"
  - "Texto pequeno SEMPRE usa AAA (4.5 -> 7.0)"
  - "Decorações testadas contra 3:1 minimum"
  - "KI-05 disparado em qualquer FAIL em title/body"
  - "Findings sugerem cor alternativa do active_palette que passa o threshold"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_CONTRAST_REPORT
on_fail_route: per data/qa-routing-table.yaml → @visual-scout + tasks/resolve-active-palette.md (followup: tasks/register-palette-override.md)
```

## WCAG Reference

| Level | Normal text | Large text (>=18pt OR >=14pt bold) | Non-text |
|---|---|---|---|
| AA | 4.5:1 | 3.0:1 | 3.0:1 |
| AAA | 7.0:1 | 4.5:1 | 3.0:1 |

## Calibração

- Brand palettes default devem passar AA em combinações canônicas (testado no `data/palette-registry.yaml`)
- Override custom em slide individual permitido apenas se registrado em palette-registry.yaml#overrides[]
