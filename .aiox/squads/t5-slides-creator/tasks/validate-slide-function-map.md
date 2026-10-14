# Task: Validate Slide Function Map (Narrative sub-dimension, case-study derived)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-slide-function-map` |
| phase | P05 + P04.5 |
| bounded_context | BC-01 (Narrative) → BC-06 (QA) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.narrativa.sub_dimensions.slide_function_map |
| schema_ref | data/slide-function-map.schema.yaml |
| killer_items | KI-08, KI-09 |
| session | SESSION-QA |
| duration | <15s (structural + regex semantic) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-013B) |
| case_study | outputs/webinars/primeiro-servico-ia/ |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateSlideFunctionMap
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker  # schema + regex enforcement primarily deterministic
```

### 4. Inputs
```yaml
Inputs:
  - name: slide_function_map
    type: YAML
    source: "{output_dir}/slide-function-map.yaml"
    schema_ref: squads/slides-creator/data/slide-function-map.schema.yaml
    required: true
  - name: story_arc
    type: YAML
    source: "{output_dir}/story-arc.yaml"
    required: true
  - name: outline_topics
    type: optional
    source: "{output_dir}/briefing.normalized.json#outline_topics"
    desc: "para enforcement de KI-09 (compression ratio)"
```

### 5. Outputs
```yaml
Outputs:
  - name: slide_function_map_report
    type: YAML
    destination: "{output_dir}/validator-reports/slide-function-map.yaml"
    schema:
      dimension: slide_function_map
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      killer_items_triggered: "array<string>"
      checks:
        schema_valid:                                "PASS | FAIL"
        all_entries_have_function:                   "PASS | FAIL"
        no_explanatory_audience_movement:            "PASS | FAIL"  # KI-08 enforcer
        slides_count_within_compression_limit:       "PASS | FAIL"  # KI-09 enforcer
        all_beat_refs_resolve:                       "PASS | FAIL"
        has_payoff_function:                         "PASS | FAIL"  # demo_payoff OR artifact_reveal
        has_cta_function:                            "PASS | FAIL"
        no_function_chain_monotonia:                 "PASS | FAIL"  # <5 mesmo function consecutivo
      findings:
        - slide_id: string
          check: string
          violation: string
          severity: "low | medium | high | critical | blocking"
          suggestion: string
      summary:
        entries_total: integer
        functions_distribution: "object {function: count}"
        compression_ratio: "number (outline_topics / entries)"
        function_chain_longest: integer
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Validar schema. Falha → FAIL imediato."
  - id: 2
    action: "Para cada entry, verificar function ∈ enum + não vazia."
  - id: 3
    action: "audience_movement check (regex):"
    sub_actions:
      - "Pattern bloqueado: ^(explicar|apresentar|falar|mostrar X|contar)"
      - "Match qualquer entry → KI-08 + dimension_score = 0 + FAIL imediato"
  - id: 4
    action: "Compression limit check (KI-09):"
    sub_actions:
      - "Se outline_topics presente: len(entries) <= 1.2 × len(outline_topics)"
      - "Senão: len(entries) <= 1.2 × sum(story_arc.beats[].slides_estimated)"
      - "Violation → KI-09 + FAIL"
  - id: 5
    action: "Verificar todos entries[].beat_ref resolve em story_arc.beats[].beat_id."
  - id: 6
    action: "Verificar has_payoff_function: pelo menos 1 entry com function ∈ {demo_payoff, artifact_reveal}."
  - id: 7
    action: "Verificar has_cta_function: pelo menos 1 entry com function = cta_concrete."
  - id: 8
    action: "Verificar function_chain_monotonia: rolling window — flag se >4 consecutivos com mesma function."
  - id: 9
    action: "Calcular dimension_score: 10 - sum(weighted check failures)."
  - id: 10
    action: "Verdict: FAIL se ANY killer_item triggered. PASS se score >=7 AND zero killer."
  - id: 11
    action: "Append planning-reflection.jsonl entry por slide com violation."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Schema validation obrigatória"
  - "KI-08 triggered se ANY audience_movement explanatory"
  - "KI-09 triggered se compression_ratio violated"
  - "Beat_ref integrity verificada"
  - "Payoff + CTA functions obrigatórias"
  - "Calibração: Primeiro Servico v1 → FAIL com KI-08+KI-09; v3 → PASS >=8.5"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_SLIDE_FUNCTION_MAP_REPORT
on_fail_route: per data/qa-routing-table.yaml → @content-architect + tasks/compress-outline-to-slide-functions.md
```
