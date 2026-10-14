# Task: P1 Fidelity Sampling (10% spot-check)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `p1-fidelity-sampling` |
| phase | P05 (optional — feature flag `enable_p1_sampling`) |
| bounded_context | BC-06 |
| invariants_enforced | P1 (Fidelidade aos dados) |
| session | null (Human task) |
| duration | 15-60 min (depending on deck size) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: p1FidelitySampling
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # random selection + human re-verification
```

### 3. responsavel_type
```yaml
responsavel_type: Human  # STK-05 senior consultant
```

### 4. Inputs[]
```yaml
Inputs:
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
  - name: source_materials
    type: files
    source: "briefing.source_paths[]"
```

### 5. Outputs[]
```yaml
Outputs:
  - name: sampling_report
    type: YAML
    destination: "{output_dir}/validator-reports/p1-sampling.yaml"
    schema:
      sample_size: "ceil(sources_apa.data_points.length × 0.1) — min 5, max 30"
      sampled_ids: "array<data_point_id>"
      re_verifications:
        - {id, claimed_value, source_ref, actual_value_in_source, match: "EXACT|PARTIAL|MISMATCH"}
      verdict: "PASS — 100% EXACT | REVIEW — ≥1 PARTIAL | FAIL — ≥1 MISMATCH"
      reviewer: "STK-05 name + timestamp"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "feature flag enable_p1_sampling == true"
  - "sources-apa has ≥ 5 data_points"
  - "source materials accessible to reviewer"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "sampling_report exists with verdict"

Acceptance_criteria:
  - "PASS → P05 invariant gate satisfied for P1"
  - "REVIEW → user decides: accept with deviation OR return to P01"
  - "FAIL (any MISMATCH) → mandatory return to P01 catalog-sources-apa with strict prompt"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "15-60 min"

Error_handling:
  strategy: halt_and_wait
  on_mismatch: "hard return to P01 — P1 violation not overridable"
```

## Invocation contract
```
@qa-inspector *p1-fidelity-sampling
# dispatches to STK-05 via notification + provides sampled IDs + source paths
```
