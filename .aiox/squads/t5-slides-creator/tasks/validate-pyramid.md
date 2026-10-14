# Task: Validate Pyramid (P3 gate)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `validate-pyramid` |
| phase | P05 |
| bounded_context | BC-06 (QA) |
| invariants_enforced | P3 |
| session | SESSION-QA |
| duration | <5s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validatePyramid
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # rule-based structural check
```

### 4. Inputs[]
```yaml
Inputs:
  - name: pyramid_tree
    type: YAML
    source: "{output_dir}/pyramid-tree.yaml"
  - name: scqa_map
    type: YAML
    source: "{output_dir}/scqa-map.yaml"
  - name: deck_manifest
    type: JSON
    source: "{output_dir}/deck-manifest.json"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: validation_report
    type: YAML
    destination: "{output_dir}/validator-reports/pyramid.yaml"
    schema:
      checks:
        level_1_unique:              "PASS | FAIL"
        level_2_count_3_to_5:        "PASS | FAIL"
        level_2_mece:                "PASS | FAIL"
        level_3_all_allocated:       "PASS | FAIL — orphans ≤ appendix only"
        scqa_percentages_sum_100:    "PASS | FAIL"
        scqa_answer_70_to_80:        "PASS | FAIL"
      verdict: "PASS | FAIL"
      failing_checks: "array<string>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "All 3 P01/P02 inputs exist"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "verdict is PASS only if all 6 checks PASS"

Acceptance_criteria:
  - "P3 invariant enforced at pipeline exit"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<5s"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_any_check_fail: "verdict = FAIL; route to dimension_router.narrative_fail"
```
