# Task: Validate Story Arc (Narrative sub-dimension, case-study derived)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-story-arc` |
| phase | P05 + P04.5 |
| bounded_context | BC-01 (Narrative) → BC-06 (QA) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.narrativa.sub_dimensions.story_arc |
| schema_ref | data/story-arc.schema.yaml |
| session | SESSION-QA |
| duration | <20s (structural + 1 LLM call for beat coherence) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-013A) |
| case_study | outputs/webinars/primeiro-servico-ia/ |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateStoryArc
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Hybrid  # structural validation (worker) + beat coherence (agent)
```

### 4. Inputs
```yaml
Inputs:
  - name: story_arc
    type: YAML
    source: "{output_dir}/story-arc.yaml"
    schema_ref: squads/slides-creator/data/story-arc.schema.yaml
  - name: slide_function_map
    type: YAML
    source: "{output_dir}/slide-function-map.yaml"
    optional: true  # se ausente, alguns checks pulam
```

### 5. Outputs
```yaml
Outputs:
  - name: story_arc_report
    type: YAML
    destination: "{output_dir}/validator-reports/story-arc.yaml"
    schema:
      dimension: story_arc
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      structural_checks:
        schema_valid:                       "PASS | FAIL"
        arc_type_canonical:                 "PASS | FAIL"
        beats_count_in_range:               "PASS | FAIL"  # 4-8
        has_opening_beat:                   "PASS | FAIL"  # hook/tension/reframe
        has_payoff_beat:                    "PASS | FAIL"  # proof/demo/artifact_reveal
        has_closing_beat:                   "PASS | FAIL"  # cta/close
        beats_have_narrative_function:      "PASS | FAIL"  # cada beat tem narrative_function
        slides_estimated_matches_map:       "PASS | FAIL"  # sum == slide-function-map count
      semantic_checks:
        beat_progression_coherent:          "PASS | FAIL"
        no_beat_function_explanatory:       "PASS | FAIL"  # narrative_function não começa com "explicar/apresentar/falar"
      anti_patterns_detected: "array<string>"
      findings:
        - check: string
          violation: string
          severity: "low | medium | high | critical"
          suggestion: string
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Validar story-arc.yaml contra schema (data/story-arc.schema.yaml). Schema invalid → FAIL."
  - id: 2
    action: "Verificar arc_type ∈ enum. Falha → FAIL."
  - id: 3
    action: "Verificar len(beats) ∈ [4, 8]."
  - id: 4
    action: "Verificar has_opening_beat: ANY beat com type ∈ {hook, tension, reframe}."
  - id: 5
    action: "Verificar has_payoff_beat: ANY beat com type ∈ {proof, demo, artifact_reveal}."
  - id: 6
    action: "Verificar has_closing_beat: ANY beat com type ∈ {cta, close}."
  - id: 7
    action: "Verificar beats[].narrative_function não vazio AND não começa com 'explicar/apresentar/falar/mostrar X' (regex)."
  - id: 8
    action: "Se slide_function_map presente: sum(beats[].slides_estimated) == len(slide_function_map.entries). Falha = critical."
  - id: 9
    action: "Semantic beat_progression_coherent (LLM): avaliar se sequência de beats forma um arco coerente (não saltos randomicos)."
  - id: 10
    action: "Detectar anti-patterns: 'Topic-list arc', 'Missing payoff', 'Monolog deck', 'Apostila'."
  - id: 11
    action: "Calcular dimension_score: structural (peso 6) + semantic (peso 4)."
  - id: 12
    action: "Verdict: FAIL se ANY structural check critical fails OR semantic incoherent."
  - id: 13
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Schema validation obrigatória"
  - "Opening + payoff + closing beats todos presentes"
  - "narrative_function explanatory bloqueia (KI-08 reinforcement)"
  - "Sum slides_estimated == slide-function-map count (acoplamento explícito)"
  - "Anti-patterns reportados"
  - "Calibração: Primeiro Servico v3 story-arc deve scorear >=8.5"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_STORY_ARC_REPORT
on_fail_route: per data/qa-routing-table.yaml → @content-architect + tasks/compress-outline-to-slide-functions.md
```
