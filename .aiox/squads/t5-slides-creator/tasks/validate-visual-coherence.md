# Task: Validate Visual Coherence (Design sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-visual-coherence` |
| phase | P05 + P04.5 |
| bounded_context | BC-06 (QA) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.design.sub_dimensions.visual_coherence |
| killer_items | KI-10 (design direction skin-only) |
| session | SESSION-QA |
| duration | <15s |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-009) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateVisualCoherence
```

### 2. atomic_layer
```yaml
atomic_layer: Atom  # mas opera em deck-level (não slide-level)
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # mas com 1 heurística semântica (motif consistency)
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
  - name: design_direction
    type: YAML
    required: true  # se ausente, KI-10 disparado imediatamente
  - name: grid_layouts
    type: YAML
```

### 5. Outputs
```yaml
Outputs:
  - name: visual_coherence_report
    type: YAML
    destination: "{output_dir}/validator-reports/visual-coherence.yaml"
    schema:
      dimension: visual_coherence
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      killer_items_triggered: "array<string>"
      checks:
        design_direction_present:           "PASS | FAIL"
        dominant_motif_applied:             "PASS | FAIL"
        layout_variety_min:                 "PASS | FAIL"
        layout_repetition_max:              "PASS | FAIL"
        padding_consistency:                "PASS | FAIL"
        alignment_consistency:              "PASS | FAIL"
        quiet_slide_ratio_min:              "PASS | FAIL"
        accent_color_density:               "PASS | FAIL"
        motif_repetition_per_slide:         "PASS | FAIL"
      findings:
        - check: string
          violation: string
          slides_affected: "array<string>"
          severity: "low | medium | high | critical"
      summary:
        unique_layouts_count: integer
        most_repeated_layout: string
        most_repeated_layout_count: integer
        quiet_slides_pct: number
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Verificar design_direction.yaml presença. Se ausente → trigger KI-10 → FAIL imediato."
  - id: 2
    action: "Verificar dominant_motif_applied:"
    sub_actions:
      - "design_direction.dominant_motif.rendered_as deve manifestar-se em >=60% dos slides"
      - "Motif precisa aparecer (paddings, bordas, fundos, decorações declarados)"
  - id: 3
    action: "Verificar layout_variety_min: contar layouts distintos. Falha se < design_direction.variation_rules.layouts_count_min (default 4)."
  - id: 4
    action: "Verificar layout_repetition_max: rolling window de slides consecutivos. Falha se mesmo layout aparece > design_direction.variation_rules.layout_repetition_max consecutivamente (default 3)."
  - id: 5
    action: "Verificar padding_consistency: top/bottom/left/right padding em pt. Variance < 10% across slides (excluindo cover/divider)."
  - id: 6
    action: "Verificar alignment_consistency: title_anchor canonical (per design_direction.composition_rules) respeitado em >=90% dos slides."
  - id: 7
    action: "Verificar quiet_slide_ratio: slides com density=minimal/low >= design_direction.variation_rules.quiet_slide_ratio_min (default 0.15)."
  - id: 8
    action: "Verificar accent_color_density: per design_direction.variation_rules.accent_color_density (sparse=<=1 accent per slide; moderate=<=2; dense=<=4)."
  - id: 9
    action: "Calcular dimension_score: 10 - sum(check_weight × failed). Pesos: design_direction_present=5, dominant_motif=3, layout_variety=2, layout_repetition=2, restantes=1."
  - id: 10
    action: "Verdict: FAIL se design_direction ausente OR sum(criticals) > 2; REVIEW if 1-2 criticals; PASS else."
  - id: 11
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "design_direction.yaml AUSENTE → KI-10 + FAIL imediato"
  - "Motif consistency verificada em >=60% dos slides"
  - "Layout variety counted (não single layout deck)"
  - "Quiet slide ratio enforce (evita wall-of-text deck)"
  - "Padding/alignment variance numericamente verificada"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_VISUAL_COHERENCE_REPORT
on_fail_route: per data/qa-routing-table.yaml → @design-renderer + tasks/define-design-direction.md (followup: tasks/apply-design-revision.md)
```

## Calibração

- gold-standard deck deve scorear >=9
- Primeiro Servico v1 (sem design_direction) → KI-10 + FAIL imediato
- Primeiro Servico v3 (com design_direction explícita) → >=8
