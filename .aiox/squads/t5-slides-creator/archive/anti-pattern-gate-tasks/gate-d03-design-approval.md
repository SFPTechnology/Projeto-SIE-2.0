# Task: Gate D03 — Design Overview Approval

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `gate-d03-design-approval` |
| phase | P03 (exit gate) |
| bounded_context | governance |
| session | null |
| duration | 4-72h |

## SINKRA Task Anatomy

### 1. task
```yaml
task: gateD03DesignApproval
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Human  # STK-07 + STK-10 (if brand override)
```

### 4. Inputs[]
```yaml
Inputs:
  - name: p03_bundle
    type: multi-file
    sources:
      - "{output_dir}/design-overview.md"
      - "{output_dir}/grid-layouts.yaml"
      - "{output_dir}/active-palette.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: checkpoint_d03
    type: YAML
    destination: "{output_dir}/checkpoints/D03.yaml"
    schema_ref: "squads/slides-creator/data/checkpoint-schema.yaml"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "D02.status == approved"
  - "active-palette.wcag_status == PASS"
  - "All slides have slide_type + chart_type + grid_layout"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "D03.yaml exists"

Acceptance_criteria:
  - "status == approved → P04 unblocks"
  - "If brand override used: approval requires STK-10 co-sign (separate approval_artifact_ref)"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "4-72h"

Error_handling:
  strategy: halt_and_wait
  sla_breach: "same ladder as D01"
  on_wcag_fail: "gate blocked — return to P03 resolve-active-palette"
```

## Anti-patterns
- Approving D03 without STK-10 co-sign when override active → reject (missing brand authority).
