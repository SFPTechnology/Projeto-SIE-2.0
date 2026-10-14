# Task: Classify Slide Type

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `classify-slide-type` |
| phase | P03 |
| bounded_context | BC-02 (Slide Design) |
| session | SESSION-SPEC |
| duration | 30s-2min per slide |

## SINKRA Task Anatomy

### 1. task
```yaml
task: classifySlideType
```

### 2. atomic_layer
```yaml
atomic_layer: Atom  # per slide
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # template-curator
```

### 4. Inputs[]
```yaml
Inputs:
  - name: deck_manifest
    type: JSON
    source: "{output_dir}/deck-manifest.json"  # with action_titles populated
    required: true
  - name: template_registry
    type: YAML
    source: "squads/slides-creator/data/template-registry.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: deck_manifest_with_types
    type: JSON
    destination: "{output_dir}/deck-manifest.json"  # patches slides[].slide_type
    enum: "Title | ExecSummary | Data | Framework | Financial | Timeline | Appendix"
    also_emits:
      - template_ref: "pointer to template-registry entry"
      - semantic_class_ref: "pointer to semantic-classification.yaml"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "action_title populated for every slide"
  - "template-registry.yaml loaded"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Every slide has slide_type ∈ enum"
  - "Template ref resolves to existing entry"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "30s-2min per slide"
  cacheable: true

Error_handling:
  strategy: retry
  max_retries: 1
  fallback: Human
  on_enum_fail: "reject, re-prompt with enum"
```

## Anti-patterns
- Assigning Appendix to slide 1 (Title required first) → reject.
- Framework slide without a named framework (McKinsey 7S, Porter, BCG) → reject.
