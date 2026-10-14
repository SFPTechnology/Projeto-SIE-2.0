# Task: Gate D02 — Structure Approval

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `gate-d02-structure-approval` |
| phase | P02 (exit gate) |
| bounded_context | governance |
| session | null |
| duration | 4-72h |

## SINKRA Task Anatomy

### 1. task
```yaml
task: gateD02StructureApproval
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Human
```

### 4. Inputs[]
```yaml
Inputs:
  - name: p02_bundle
    type: multi-file
    sources:
      - "{output_dir}/deck-manifest.json"  # action_titles populated
      - "{output_dir}/vertical-test-result.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: checkpoint_d02
    type: YAML
    destination: "{output_dir}/checkpoints/D02.yaml"
    schema_ref: "squads/slides-creator/data/checkpoint-schema.yaml"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "D01.status == approved"
  - "vertical-test-result.verdict == PASS  # hard precondition — blocks gate otherwise"
  - "Every slide has action_title + segment + slide_type_draft"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "D02.yaml exists with status ∈ enum"

Acceptance_criteria:
  - "status == approved AND vertical-test-result.verdict == PASS → P03 unblocks"
  - "If vertical test != PASS: gate blocked regardless of human status"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "4-72h"

Error_handling:
  strategy: halt_and_wait
  sla_breach: "same ladder as D01"
  on_vertical_test_fail: "cannot override — return to P02 write-action-titles"
```
