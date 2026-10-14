# Task: Compose Grid Layout

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `compose-grid-layout` |
| phase | P03 |
| bounded_context | BC-02 |
| session | SESSION-SPEC |
| duration | 1-3 min per slide |

## SINKRA Task Anatomy

### 1. task
```yaml
task: composeGridLayout
```

### 2. atomic_layer
```yaml
atomic_layer: Atom  # per slide
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # design-renderer (judgment on composition)
```

### 4. Inputs[]
```yaml
Inputs:
  - name: slide_spec_draft
    type: JSON
    source: "deck_manifest.slides[pos]"
    fields: [slide_type, action_title, chart_type, callouts, footer]
  - name: active_palette
    type: YAML
    source: "{output_dir}/active-palette.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: grid_layout
    type: YAML
    destination: "{output_dir}/grid-layouts.yaml"
    schema:
      slide_pos: int
      grid:
        columns: 12
        rows: 8
      zones:
        title:          {x, y, w, h}
        visual_primary: {x, y, w, h}
        insights:       {x, y, w, h}
        support:        {x, y, w, h}
        footer:         {x, y, w, h}
      whitespace_pct: "float"
      ascii_preview: "string"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "slide_type assigned"
  - "active-palette resolved"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "All zones within 12×8 grid bounds"
  - "No zone overlaps"
  - "whitespace_pct ≥ 30 (canonical) OR ≥ 25 (override with rationale)"

Acceptance_criteria:
  - "ascii_preview non-empty"
  - "Zone hierarchy: Title > Visual primary > Insights > Support > Footer (in visual weight)"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "1-3 min per slide"
  cacheable: false

Error_handling:
  strategy: retry
  max_retries: 2
  fallback: Worker  # deterministic default grid per slide_type
  on_overlap: "reject, re-prompt with overlap details"
```
