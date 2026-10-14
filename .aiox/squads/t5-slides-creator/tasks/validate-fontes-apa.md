# Task: Validate Fontes APA (P6)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `validate-fontes-apa` |
| phase | P05 |
| bounded_context | BC-06 |
| invariants_enforced | P6 |
| session | SESSION-QA |
| duration | <2s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateFontesAPA
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker
```

### 4. Inputs[]
```yaml
Inputs:
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: validation_report
    type: YAML
    destination: "{output_dir}/validator-reports/fontes-apa.yaml"
    schema:
      verdict: "PASS | FAIL"
      citations_total: int
      citations_complete: int
      incomplete:
        - {id, missing_fields: "array<{org|title|date|url|access_date}>"}
      orphan_data_points:
        - {data_point_id, slide_pos}
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "sources-apa.yaml + deck-spec.yaml exist"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "verdict PASS only if incomplete == [] AND orphan_data_points == []"

Acceptance_criteria:
  - "Every data point cited on a slide has a resolvable citation in sources-apa"
  - "Every citation has all 5 APA fields populated"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<2s"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_orphan: "route to dimension_router.spec_fail (return to P04 spec phase)"
  on_incomplete_citation: "route to dimension_router.narrative_fail (return to P01 catalog-sources)"
```
