# Task: Select Chart Type (matrix lookup)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `select-chart-type` |
| phase | P03 |
| bounded_context | BC-02 |
| session | SESSION-SPEC |
| duration | <1s per chart |

## SINKRA Task Anatomy

### 1. task
```yaml
task: selectChartType
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # deterministic lookup, no LLM
```

### 4. Inputs[]
```yaml
Inputs:
  - name: chart_requests
    type: array
    source: "deck_manifest.slides[].chart_requests[]"
    schema: "{intent, n_series, n_points, data_refs}"
  - name: chart_matrix
    type: YAML
    source: "squads/slides-creator/data/chart-selection-matrix.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: chart_assignments
    type: JSON
    destination: "patches deck_manifest.slides[].chart_type + rationale_ref"
    schema:
      chart_type: "string (from matrix)"
      rationale_ref: "KB_06 anchor"
      confidence: "high | medium | low"
      fallback_used: "boolean"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "chart-selection-matrix.yaml loaded and valid"
  - "Every chart_request has intent + n_series + n_points"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Every chart_request resolved to a chart_type"
  - "fallback_used flagged for qa-inspector review"

Acceptance_criteria:
  - "Zero unresolved chart_requests (fallback counts as resolved)"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<1s"
  cost: "negligible (no LLM)"
  cacheable: true
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_no_match: "use fallback.no_match_found from matrix + flag to QA"
  on_n_points_exceeds: "switch to fallback.n_points_exceeds_chart_limit strategy"
```

## Invocation contract
```
@template-curator *select-chart-type --manifest {output_dir}/deck-manifest.json
# Internally calls Worker script: scripts/select-chart-type.js (reads matrix, emits decisions)
```
