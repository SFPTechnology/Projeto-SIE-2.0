# Task: Validate Action Title (P4)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `validate-action-title` |
| phase | P05 |
| bounded_context | BC-06 |
| invariants_enforced | P4 (+ P7 sub-check for image slides) |
| session | SESSION-QA |
| duration | <2s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateActionTitle
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
  - name: deck_manifest
    type: JSON
    source: "{output_dir}/deck-manifest.json"
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: validation_report
    type: YAML
    destination: "{output_dir}/validator-reports/action-title.yaml"
    schema:
      verdict: "PASS | FAIL"
      slides_total: int
      slides_pass: int
      failures:
        - {pos, title, reason: "descriptive | missing_component | too_long | contradicts_pyramid"}
      p7_check:
        image_slides_total: int
        prompts_with_10_components: int
        prompts_incomplete: "array<{pos, missing_components}>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-manifest.json has action_title on every slide"
  - "deck-spec.yaml has image_prompt blocks for image slides"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "verdict PASS only if failures == [] AND prompts_incomplete == []"

Acceptance_criteria:
  - "Every title matches P4 regex: '^.+? (cres|cai|expan|reduz|aumen|gera|supera|repres|atinge|supera|ultrapassa|\\d+%|\\d+x).+$'  OR passes semantic P4 check"
  - "Title ≤ 120 characters"
  - "Title does not contradict pyramid_tree.level_2 pillars"
  - "If slide has image: image_prompt has all 10 components"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<2s"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_fail: "route to dimension_router.narrative_fail"
```

## Anti-patterns
- Regex-only P4 check without semantic verification → acceptable for MVP, but KB_01 semantic pattern is stronger.
- Accepting titles longer than 120 chars "because data is nuanced" → reject (compress).
