# Task: Apply SCQA (Narrative Arc + Slide % Allocation)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `apply-scqa` |
| phase | P01 |
| bounded_context | BC-01 |
| invariants_enforced | P3 |
| session | SESSION-NARR |
| duration | 10-20 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: applySCQA
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # 4 atoms (marcar situation/complication/question/answer)
```

### 3. responsavel_type
```yaml
responsavel_type: Agent
```

### 4. Inputs[]
```yaml
Inputs:
  - name: pyramid_tree
    type: YAML
    source: "{output_dir}/pyramid-tree.yaml"
    required: true
  - name: briefing
    type: JSON
    source: "{output_dir}/briefing.normalized.json"
    required: true  # for max_slides + audience + format
```

### 5. Outputs[]
```yaml
Outputs:
  - name: scqa_map
    type: YAML
    destination: "{output_dir}/scqa-map.yaml"
    schema:
      ordering: "deductive | chronological | structural | comparative"
      ordering_rationale: "string"
      allocation:
        situation:   {pct: "10-20", slide_count: int}
        complication:{pct: "5-10",  slide_count: int}
        question:    {pct: "0-5",   slide_count: "0 or 1 (implicit ok)"}
        answer:      {pct: "70-80", slide_count: int}
      total_slides: int
      slide_sequence:
        - {pos: int, segment: "S|C|Q|A", pillar_id: "string | null"}
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "pyramid-tree.yaml MECE == PASS"
  - "briefing.max_slides declared"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "sum of allocation pcts == 100"
  - "sum of slide_counts == total_slides == briefing.max_slides (±2)"
  - "slide_sequence monotonic in pos"
  - "each Answer slide tied to a pillar_id (or explicitly appendix)"

Acceptance_criteria:
  - "Situation slide count ≥ 1"
  - "Answer allocation ≥ 70% of total"
  - "Ordering rationale ≥ 30 words"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "10-20 min"
  cost: "low"
  cacheable: true

Error_handling:
  strategy: retry
  max_retries: 2
  fallback: Human
  on_allocation_fail: "re-prompt with exact drift reason"
```

## Anti-patterns
- Answer < 70% (audience loses the narrative climax) → reject.
- Complication skipped entirely — no tension, no so-what → reject.
- Ordering picked without rationale → reject.
