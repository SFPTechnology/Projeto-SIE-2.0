# Task: Validate Enumeração Universal (P5)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `validate-enumeration-universal` |
| phase | P05 |
| bounded_context | BC-06 |
| invariants_enforced | P5 |
| session | SESSION-QA |
| duration | <2s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateEnumerationUniversal
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
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: validation_report
    type: YAML
    destination: "{output_dir}/validator-reports/enumeration.yaml"
    schema:
      verdict: "PASS | FAIL"
      total_visuals: int
      enumerated: int
      unenumerated: "array<{slide_pos, visual_kind, visual_ref}>"
      duplicate_ids: "array<{id, occurrences}>"
      id_pattern_violations: "array<{id, expected_pattern}>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-spec.yaml exists and schema-valid"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "verdict PASS only if unenumerated == [] AND duplicate_ids == [] AND id_pattern_violations == []"

Acceptance_criteria:
  - "Every visual has ID matching regex: '^(Gráfico|Tabela|Figura|Diagrama) \\d+(\\.\\d+)?$'"
  - "No duplicate IDs across deck"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<2s"
  deterministic: true

Error_handling:
  strategy: fail_fast
```
