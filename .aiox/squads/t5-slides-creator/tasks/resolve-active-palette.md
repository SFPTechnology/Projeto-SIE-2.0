# Task: Resolve Active Palette (+ WCAG)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `resolve-active-palette` |
| phase | P03 |
| bounded_context | BC-05 |
| session | SESSION-SPEC |
| duration | <1s |

## SINKRA Task Anatomy

### 1. task
```yaml
task: resolveActivePalette
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # lookup + WCAG compute
```

### 3. responsavel_type
```yaml
responsavel_type: Worker
```

### 4. Inputs[]
```yaml
Inputs:
  - name: brand_detection
    type: YAML
    source: "{output_dir}/brand-detection.yaml"
    required: true
  - name: palette_registry
    type: YAML
    source: "squads/slides-creator/data/palette-registry.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: active_palette
    type: YAML
    destination: "{output_dir}/active-palette.yaml"
    schema:
      palette_id: "PALETTE-CANONICAL-MCKINSEY | PALETTE-OVERRIDE-{slug}"
      hex: "map<string, string>"
      typography: "object"
      grid: "object"
      wcag_matrix:
        - {fg: "#xxxxxx", bg: "#yyyyyy", ratio: float, level: "AA | AAA | FAIL"}
      wcag_status: "PASS | FAIL"
      rationale: "string"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "palette-registry has canonical entry"
  - "If override: entry with slug exists"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "All foreground/background hex pairs used by deck have wcag_matrix entries"
  - "wcag_status is PASS if all pairs ≥ 4.5:1"

Acceptance_criteria:
  - "wcag_status == PASS → proceed to P04"
  - "wcag_status == FAIL → block D03 gate, surface failing pairs"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<500ms"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_missing_slug: "fail with explicit 'override not in registry' (no silent fallback to canonical)"
  on_wcag_fail: "return FAIL + list of failing pairs (do not auto-fix)"
```
