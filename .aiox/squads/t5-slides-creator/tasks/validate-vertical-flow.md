# Task: Validate Vertical Flow (final 2-min test)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `validate-vertical-flow` |
| phase | P05 |
| bounded_context | BC-06 |
| invariants_enforced | P3 + P4 |
| session | SESSION-QA (fresh instance — isolated from P02 run) |
| duration | 3-10 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateVerticalFlow
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # qa-inspector, final cross-instance check
```

### 4. Inputs[]
```yaml
Inputs:
  - name: deck_manifest_final
    type: JSON
    source: "{output_dir}/deck-manifest.json"  # v2 full
    filter: "slides[].action_title only (title projection)"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: validation_report
    type: YAML
    destination: "{output_dir}/validator-reports/vertical-flow.yaml"
    schema:
      verdict: "PASS | FAIL"
      narrative_understood_in_2min: boolean
      weak_titles: "array<{pos, title, weakness}>"
      coherence_score: "0-10"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-manifest.json has final action_titles"
  - "Session is a FRESH SESSION-QA instance (not reusing P02 vertical test session)"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "verdict assigned"
  - "If FAIL: weak_titles populated"

Acceptance_criteria:
  - "verdict == PASS AND coherence_score ≥ 7"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "3-10 min"

Error_handling:
  strategy: retry_once_in_new_session
  on_inconclusive: "return FAIL + rationale"
```

## Anti-patterns
- Running in same session as P02 vertical test → self-validation blindspot.
- Accepting verdict without reading the title sequence literally → must project titles first.
