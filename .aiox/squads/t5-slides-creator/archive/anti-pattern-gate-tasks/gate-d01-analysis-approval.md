# Task: Gate D01 — Analysis Approval

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `gate-d01-analysis-approval` |
| phase | P01 (exit gate) |
| bounded_context | governance (cross-BC) |
| session | null (Human) |
| duration | 4-72h (async, SLA ladder) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: gateD01AnalysisApproval
```

### 2. atomic_layer
```yaml
atomic_layer: Atom  # binary approval
```

### 3. responsavel_type
```yaml
responsavel_type: Human  # STK-07 client strategy team (or STK-05 in internal-only mode)
```

### 4. Inputs[]
```yaml
Inputs:
  - name: p01_bundle
    type: multi-file
    sources:
      - "{output_dir}/governing-thought.yaml"
      - "{output_dir}/pyramid-tree.yaml"
      - "{output_dir}/scqa-map.yaml"
      - "{output_dir}/sources-apa.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: checkpoint_d01
    type: YAML
    destination: "{output_dir}/checkpoints/D01.yaml"
    schema_ref: "squads/slides-creator/data/checkpoint-schema.yaml"
    required_fields: [gate_id, status, approver, timestamp]
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "All 4 P01 artifacts exist and schema-valid"
  - "sources-apa.yaml has 0 entries missing APA fields"
  - "pyramid-tree.yaml MECE status == PASS"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "D01.yaml exists with status ∈ {approved, rejected, waived}"
  - "If rejected: notes ≥ 20 words explaining what to revise"

Acceptance_criteria:
  - "status == approved → P02 unblocks"
  - "status == rejected → pipeline returns to P01 with reviewer feedback"
  - "status == waived (advisory mode only) → deviation entry required"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "4-72h typical; SLA ladder at 24/72/168h"

Error_handling:
  strategy: halt_and_wait
  sla_breach:
    at_24h: "nudge STK-05 via notification channel"
    at_72h: "escalate to STK-01 (C-level)"
    at_168h: "auto_pause workflow; human resume required"
```

## Invocation contract
```
@slide-chief *run-gate-d01
# Presents P01 bundle to approver; awaits D01.yaml artifact write
```
