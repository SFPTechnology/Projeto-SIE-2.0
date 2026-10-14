# Task: Detect Brand Override

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `detect-brand-override` |
| phase | P03 |
| bounded_context | BC-05 (Brand & Design System) |
| session | SESSION-SPEC |
| duration | <1s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: detectBrandOverride
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
  - name: briefing
    type: JSON
    source: "{output_dir}/briefing.normalized.json"
    fields: [client_slug, project_slug, brand_config_ref]
  - name: palette_registry
    type: YAML
    source: "squads/slides-creator/data/palette-registry.yaml"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: override_flag
    type: JSON (inline)
    destination: "{output_dir}/brand-detection.yaml"
    schema:
      override_exists: boolean
      override_slug: "string | null"
      source_checked:
        - "palette-registry.overrides[slug == project_slug]"
        - "workspace/businesses/{client_slug}/L2-tactical/brand/brand-platform.yaml"
      action_required: "register | resolve | null"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "palette-registry.yaml loaded"
  - "briefing.client_slug declared OR briefing.project_slug declared"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "If override_exists → action_required == resolve"
  - "If brand-platform.yaml exists for client AND no registry entry → action_required == register (triggers Human task `register-palette-override`)"
  - "If neither → action_required == null (canonical palette used)"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<500ms"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_path_error: "log warning, assume no override"
```
