# Task: Distill Governing Thought

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `distill-governing-thought` |
| phase | P01 |
| bounded_context | BC-01 (Narrative Architecture) |
| invariants_enforced | P3 (Pyramid — unique top message), P4 (action title precursor) |
| session | SESSION-NARR |
| duration | 5-15 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: distillGoverningThought
```

### 2. atomic_layer
```yaml
atomic_layer: Atom  # single distillation
```

### 3. responsavel_type
```yaml
responsavel_type: Agent
```

### 4. Inputs[]
```yaml
Inputs:
  - name: briefing
    type: JSON
    source: "{output_dir}/briefing.normalized.json"
    required: true
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: governing_thought
    type: YAML
    destination: "{output_dir}/governing-thought.yaml"
    schema:
      thought: "string ≤ 35 words, single sentence"
      draft_candidates: "array<string> — 3 rejected drafts + rationale"
      test_1_minute: "PASS | FAIL"  # passes if it's what you'd say with 1 min left
      validated_against: "array<sources_apa.data_points[].id>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "sources-apa.yaml exists with ≥ 1 data_point"
  - "briefing has explicit audience + objective"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Thought is EXACTLY one sentence"
  - "Thought contains no conjunctions that split two separate ideas (no 'e', 'and', '+')"
  - "Word count ≤ 35"
  - "Answers: 'if you had 1 minute to convince the audience, what would you say?'"

Acceptance_criteria:
  - "Schema validator PASS (single_sentence regex + word_count)"
  - "≥ 3 draft candidates rejected with explicit rationale (avoids single-draft anchoring)"
  - "D01 human gate accepts this as the north star"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "5-15 min"
  cost: "low (short completion)"
  cacheable: false

Error_handling:
  strategy: retry_with_temperature_bump
  max_retries: 3
  fallback: Human  # STK-05 drafts by hand
  on_schema_fail: "re-prompt with 'you wrote 2+ sentences — compress to one'"
```

## Invocation contract
```
@content-architect *distill-governing-thought
```

## Anti-patterns
- Compound sentence with "e" linking two independent claims → refuses schema.
- Descriptive thought ("Analysis of market X") → must be insight-bearing.
- Overly safe corporate language ("market presents opportunities") → must have teeth.
