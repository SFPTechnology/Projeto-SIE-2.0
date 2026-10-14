# Task: Load KB Bundle

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `load-kb-bundle` |
| phase | P00 (and re-invoked at P01/P02/P03/P04 per-phase) |
| bounded_context | cross-BC infrastructure |
| session | null (worker, session-independent) |
| duration | <1s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: loadKBBundle
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
  - name: session_id
    type: string
    enum: [SESSION-NARR, SESSION-SPEC, SESSION-QA]
    required: true
  - name: firm_style
    type: string
    enum: [mckinsey, bcg, bain, tier2]
    required: true
  - name: industry
    type: string
    enum: [financial_services, technology_saas, healthcare_pharma, retail_consumer, manufacturing, energy_utilities, professional_services, other]
    required: true
  - name: has_image_request
    type: boolean
    default: false
  - name: kb_matrix
    type: YAML
    source: "squads/slides-creator/data/kb-loading-matrix.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: kb_bundle
    type: YAML
    destination: "{output_dir}/kb-bundle-{session_id}-{phase}.yaml"
    schema:
      kb_ids: "array<KB_id>"
      concatenated_text: "string"
      total_tokens_estimate: int
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "kb-loading-matrix.yaml valid"
  - "All KB files referenced by matrix exist on disk"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "kb_bundle contains at least the baseline KBs for the session"
  - "concatenated_text ordered by KB_id"

Acceptance_criteria:
  - "total_tokens_estimate ≤ model context window × 0.5"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<1s"
  deterministic: true
  cacheable: true

Error_handling:
  strategy: fail_fast
  on_missing_kb_file: "fail with explicit path"
  on_unknown_session: "fail"
```
