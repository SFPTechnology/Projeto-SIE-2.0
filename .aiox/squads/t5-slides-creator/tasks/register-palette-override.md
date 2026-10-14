# Task: Register Palette Override

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `register-palette-override` |
| phase | P03 (conditional on detect-brand-override.action_required == register) |
| bounded_context | BC-05 |
| session | null (Human task — no LLM session) |
| duration | 15-60 min (human + CODEOWNERS approval) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: registerPaletteOverride
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # human decision + artifact + registry patch
```

### 3. responsavel_type
```yaml
responsavel_type: Human  # STK-10 brand steward, dispatched by slide-chief
```

### 4. Inputs[]
```yaml
Inputs:
  - name: client_brand_platform
    type: YAML
    source: "workspace/businesses/{client_slug}/L2-tactical/brand/brand-platform.yaml"
    required: true
  - name: override_proposal
    type: YAML
    source: "human-drafted — hex map + rationale + trade_off"
  - name: approval_artifact
    type: document
    source: "outputs/slides-creator/{deck_slug}/approvals/brand-override.{pdf|md}"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: registry_entry
    type: YAML
    destination: "patches squads/slides-creator/data/palette-registry.yaml#overrides[]"
    schema: "per palette-registry.yaml#registration_protocol.required_inputs"
  - name: wcag_verification
    type: YAML
    destination: "inline in registry_entry.wcag_ratios_verified"
    required: true
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "detect-brand-override.action_required == register"
  - "client brand-platform.yaml exists"
  - "approval_artifact signed by STK-10 or equivalent"
  - "all hex pairs used in deck passed WCAG AA ≥ 4.5:1 (computed via resolve-active-palette in dry-run)"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "New entry appended to palette-registry.yaml#overrides[]"
  - "Canonical entry unchanged (verify diff)"
  - "Git commit with CODEOWNERS approval"

Acceptance_criteria:
  - "rationale ≥ 50 words"
  - "trade_off ≥ 30 words"
  - "approver stakeholder_ref populated"
  - "approval_artifact_ref points to existing file"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "15-60 min (async)"

Error_handling:
  strategy: halt_until_resolved
  on_wcag_fail: "reject override; must remediate colors before re-submitting"
  on_missing_rationale: "reject; send back to human"
  on_canonical_modified: "hard reject (immutable invariant violated)"
```

## Invocation contract
```
@slide-chief *register-palette-override --proposal <path-to-yaml>
# slide-chief is the dispatcher; STK-10 is the R+A
```

## Anti-patterns
- Override "because client said so" without trade_off rationale → reject.
- Editing canonical entry "to match client" → rejected at hook level.
- Skipping WCAG verification → rejected.
