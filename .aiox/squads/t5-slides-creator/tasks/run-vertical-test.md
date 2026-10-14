# Task: Run Vertical Test (2-Minute Title-Only Narrative)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `run-vertical-test` |
| phase | P02 (and re-run in P05 validate-vertical-flow) |
| bounded_context | BC-01 → BC-06 |
| invariants_enforced | P3 (Pyramid coherence), P4 (action titles) |
| session | SESSION-QA   # cross-instance from SESSION-NARR — avoids self-validation blindspot |
| duration | 2-5 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: runVerticalTest
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # qa-inspector @ SESSION-QA (distinct from content-architect session)
```

### 4. Inputs[]
```yaml
Inputs:
  - name: deck_manifest_partial
    type: JSON
    source: "{output_dir}/deck-manifest.json"
    required: true
    filter: "projection: slides[].action_title only (no body content)"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: vertical_test_result
    type: YAML
    destination: "{output_dir}/vertical-test-result.yaml"
    schema:
      verdict: "PASS | REVIEW | FAIL"
      titles_projected: "array<string>  # in order"
      narrative_understood_in_2min: "boolean"
      rationale: "string — ≥ 50 words"
      recommendation:
        on_review: "array<slide_pos>  # slides whose titles are weakest"
        on_fail: "specific slides to redo + why"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-manifest.json has slides[].action_title populated for every slide"
  - "SESSION-QA context is isolated (no prior NARR turns in this session)"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Verdict is one of PASS|REVIEW|FAIL"
  - "Rationale answers: 'could a reader understand the full argument by reading only these titles in 2 minutes?'"

Acceptance_criteria:
  - "If PASS → D02 gate precondition satisfied"
  - "If REVIEW → D02 requires explicit user ack"
  - "If FAIL → D02 blocked, pipeline returns to P01/P02"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "2-5 min"
  cost: "low"
  cacheable: false

Error_handling:
  strategy: retry
  max_retries: 1
  fallback: Human  # STK-05 does the vertical test manually
  on_inconclusive: "return REVIEW with explanation"
```

## Anti-patterns
- Running this in the same session as write-action-titles → invalid (self-validation).
- Accepting PASS without rationale → reject output.
- Declaring PASS when ≥ 1 title contradicts another → must fail coherence.
