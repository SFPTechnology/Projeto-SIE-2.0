# Task: Emit Deck Spec (canonical DeckSpec YAML)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `emit-deck-spec` |
| phase | P04 (first emission) + P06 (final emission) |
| bounded_context | BC-07 (Deliverable Packaging) |
| invariants_enforced | P2 (schema enforcement), P5, P6, P7 (all via schema) |
| session | SESSION-SPEC |
| duration | 2-5s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: emitDeckSpec
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # deterministic serialization from deck-manifest.json v2
```

### 4. Inputs[]
```yaml
Inputs:
  - name: deck_manifest
    type: JSON
    source: "{output_dir}/deck-manifest.json"  # v2 full
    required: true
  - name: active_palette
    type: YAML
    source: "{output_dir}/active-palette.yaml"
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: deck_spec
    type: YAML
    destination: "{output_dir}/deck-spec.yaml"
    schema:
      deck_metadata:
        title: string
        slug: string
        version: string
        created_at: timestamp
        governing_thought: string
        audience: string
        aspect_ratio: "16:9"
      palette:
        id: string
        hex: map<string,string>
        typography: object
        grid: object
      slides:
        - pos: int
          slide_type: enum
          action_title: string
          grid_layout: object
          visual_elements:
            charts: "array<{id, chart_type, spec}>"
            tables: "array<{id, spec}>"
            images: "array<{id, prompt_10_components}>"
            callouts: "array<{id, spec}>"
          citations: "array<{apa_ref}>"
          speaker_notes: string
          transition: "{from_prev, to_next, suggested_phrase}"
      bibliography: "array<{apa_entry}>"
      validation_state:
        v2_schema_valid: boolean
        all_princípios_enforced: "map<P1..P7, PASS|FAIL|PENDING>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-manifest.json v2 schema valid"
  - "active-palette.yaml resolved with wcag_status PASS"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "deck-spec.yaml written and js-yaml parses"
  - "validation_state populated"

Acceptance_criteria:
  - "schema validator passes"
  - "Ready to be consumed by emit packaging tasks AND by handoff-render-request"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "2-5s"
  deterministic: true
  cacheable: true

Error_handling:
  strategy: fail_fast
  on_schema_fail: "halt, surface missing fields"
```
