# Task: Build Pyramid (Minto 3 Levels)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `build-pyramid` |
| phase | P01 |
| bounded_context | BC-01 |
| invariants_enforced | P3 (Pyramid + MECE) |
| session | SESSION-NARR |
| duration | 10-30 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: buildPyramid
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # 3 levels + MECE validation = atomic composition
```

### 3. responsavel_type
```yaml
responsavel_type: Agent
```

### 4. Inputs[]
```yaml
Inputs:
  - name: governing_thought
    type: YAML
    source: "{output_dir}/governing-thought.yaml"
    required: true
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: pyramid_tree
    type: YAML
    destination: "{output_dir}/pyramid-tree.yaml"
    schema:
      level_1:
        thought: "string (== governing_thought.thought)"
      level_2:
        pillars: "array<{id, name, thesis, evidence_refs: array<data_point_id>}>"
        count: "3 to 5"
        mece_status:
          mutually_exclusive: "PASS | FAIL"
          collectively_exhaustive: "PASS | FAIL"
          overlaps_found: "array<{pillar_a, pillar_b, overlap_description}>"
          gaps_found: "array<{description}>"
      level_3:
        evidence_allocation: "map<pillar_id, array<data_point_id>>"
        orphans: "array<data_point_id>  # data points not allocated to any pillar"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "governing-thought.yaml exists with test_1_minute == PASS"
  - "sources-apa.data_points has ≥ 5 entries"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Level 1 == governing_thought (identity)"
  - "Level 2 has 3-5 pillars"
  - "Level 2 mece_status.mutually_exclusive == PASS (0 overlaps)"
  - "Level 2 mece_status.collectively_exhaustive == PASS (0 critical gaps)"
  - "Level 3 orphans list is either empty OR orphans have explicit 'appendix' flag"

Acceptance_criteria:
  - "validate-pyramid (P05 task) verdict PASS when this pyramid is tested"
  - "D02 human gate accepts pyramid as structure"
  - "No pillar has fewer than 2 evidence_refs"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "10-30 min"
  cost: "moderate"
  cacheable: true  # by (governing_thought + sources_hash)

Error_handling:
  strategy: retry_with_feedback
  max_retries: 3
  fallback: Human
  on_mece_fail:
    mutually_exclusive_fail: "re-prompt with overlap list to force pillar consolidation"
    collectively_exhaustive_fail: "re-prompt with gap list + sources-apa to force new pillar"
```

## Anti-patterns
- 2 pillars (too few) or 6+ pillars (cognitive overload) → schema rejects.
- Pillars that are verbs ("Analisar X") instead of theses ("X is broken because Y") → reject.
- Evidence allocation by keyword match without argument logic → reject.
