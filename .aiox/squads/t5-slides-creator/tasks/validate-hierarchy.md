# Task: Validate Hierarchy (Design sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-hierarchy` |
| phase | P05 + P04.5 (critique loop) |
| bounded_context | BC-06 (QA) |
| invariants_enforced | P2 |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.design.sub_dimensions.hierarchy |
| killer_items | KI-04 (texto cortado), KI-07 (action title fraco renderizado errado) |
| session | SESSION-QA |
| duration | <10s |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-006) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateHierarchy
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # rule-based typography scale + visual weight ordering
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
  - name: token_registry
    type: YAML
    source: squads/slides-creator/data/token-registry.yaml
  - name: scale_standards
    type: YAML
    source: squads/slides-creator/data/scale-standards.yaml
```

### 5. Outputs
```yaml
Outputs:
  - name: hierarchy_report
    type: YAML
    destination: "{output_dir}/validator-reports/hierarchy.yaml"
    schema:
      dimension: hierarchy
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      findings:
        - slide_id: string
          checks:
            scale_step_canonical:     "PASS | FAIL"  # uses --slide-title-xl/lg/md/body/caption
            visual_weight_descending: "PASS | FAIL"  # h1 > h2 > h3 visually
            single_title_anchor:      "PASS | FAIL"  # one element wins eye
            action_title_largest:     "PASS | FAIL"  # action title é o maior elemento textual
          violations: "array<string>"
          severity: "low | medium | high | critical"
      summary:
        slides_total: integer
        slides_pass: integer
        scale_violations: integer
        weight_violations: integer
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Carregar deck_spec, design_direction, token_registry, scale_standards."
  - id: 2
    action: "Para cada slide:"
    sub_actions:
      - "Extrair todos elementos textuais com (font_size, font_weight, line_height)"
      - "Verificar scale_step_canonical: cada elemento mapeia a token canonical (--slide-title-xl/lg/md/body/caption)"
      - "Verificar visual_weight_descending: ordering visual respeita hierarquia semântica (h1 → h2 → h3 → body → caption)"
      - "Verificar single_title_anchor: exatamente 1 elemento ocupa peso visual dominante"
      - "Verificar action_title_largest: action_title (se presente) é o maior elemento textual"
  - id: 3
    action: "Calcular dimension_score: 10 - (2 × % slides com violation critical) - (1 × % com violation high) - (0.3 × % com violation medium)."
  - id: 4
    action: "Verdict: PASS if score >= 7 AND single_title_anchor PASS em 100% das slides."
  - id: 5
    action: "Emit hierarchy.yaml com per-slide checks + suggestions concretas (e.g., 'subtitle s05 usa --slide-title-lg mas deveria usar --slide-title-md')."
  - id: 6
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Validator executa em <10s para deck de 30 slides"
  - "Falha quando 2+ elementos textuais competem por título dominante na mesma slide"
  - "Falha quando subtitle > title em font_size (inversão de hierarquia)"
  - "Action_title NÃO pode ser menor que body text"
  - "Findings citam token canonical sugerido (--slide-title-X) em vez de só relatar erro"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_HIERARCHY_REPORT
on_fail_route: per data/qa-routing-table.yaml → @design-renderer + tasks/compose-grid-layout.md
```

## Calibração

- gold-standard: >=9
- known-bad Primeiro Servico v1: <=5 (cards repetidos com hierarchy plana)
