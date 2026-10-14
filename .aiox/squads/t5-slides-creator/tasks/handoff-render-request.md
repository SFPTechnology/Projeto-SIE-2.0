# Task: Handoff Render Request (BC-08 seam)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `handoff-render-request` |
| phase | P06 |
| bounded_context | BC-08 (Render Handoff seam) |
| session | null |
| duration | <5s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: handoffRenderRequest
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
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
    required: true
  - name: active_palette
    type: YAML
    source: "{output_dir}/active-palette.yaml"
    required: true
  - name: client_opt_in
    type: boolean
    source: "briefing.options.render_html"
    default: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: render_request
    type: YAML
    destination: "{output_dir}/render-request.yaml"
    schema:
      request_id: "slides-creator-render-{deck_slug}-{timestamp}"
      status: "pending"
      deck_spec_ref: "path"
      active_palette_ref: "path"
      target_runtime:
        preferred: "{consumer_app_id}"   # resolved from config.yaml#render_targets
        fallback: "llm-direct"           # markdown + deck-spec only
      client_opt_in: boolean
      handoff_contract_version: "1.0"
      consumer: "consumer_app conforming to tech_discipline contract OR fallback renderer"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "deck-spec.yaml schema-valid"
  - "active-palette.yaml wcag PASS"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "render-request.yaml written"
  - "If consumer_app runtime available: its renderer picks up the request"
  - "If consumer_app unavailable: render_state = handoff_only (documented in release summary)"

Acceptance_criteria:
  - "Idempotent — re-running produces equivalent artifact with fresh request_id"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<5s"
  deterministic: true

Error_handling:
  strategy: emit_handoff_anyway
  on_apps_ds_missing: "emit render-request with status=pending, log handoff_only state"
  on_fallback_missing: "emit anyway; mark target_runtime.fallback_available = false"
```

## Invocation contract
```
@slide-chief *handoff-render-request
# Emits BC-08 contract; downstream consumer is slides-creator design-renderer (same squad, different role)
```
