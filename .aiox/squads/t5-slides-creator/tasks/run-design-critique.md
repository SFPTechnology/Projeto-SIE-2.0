# Task: Run Design Critique (Phase P04.5)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `run-design-critique` |
| phase | P04.5 (entre P04 Specification e P05 QA macro) |
| bounded_context | BC-06 (QA) |
| session | SESSION-DESIGN-CRITIQUE (distinct from SESSION-QA) |
| duration | <60s (aggregates 5 validators + 5 narrative validators) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-016, GAP-001 closure) |
| iteration_cap | 2 |

## Why this task exists

Sem critique loop dedicado, qa-inspector recebia draft DeckSpec e emitia verdict PASS/FAIL. Sem oportunidade de iteration estruturada com decisões registradas. Esta task abre janela formal entre draft e QA final onde @design-planner orquestra critique + reflection + routing.

## SINKRA Task Anatomy

### 1. task
```yaml
task: runDesignCritique
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # invokes 10 sub-validators + aggregates
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # orchestration + LLM judgement on aggregation
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
    state: draft
  - name: design_direction
    type: YAML
    source: "{output_dir}/design-direction.yaml"
    required: true
  - name: slide_function_map
    type: YAML
    source: "{output_dir}/slide-function-map.yaml"
    required: true
  - name: story_arc
    type: YAML
    source: "{output_dir}/story-arc.yaml"
    required: true
  - name: grid_layouts
    type: YAML
    source: "{output_dir}/grid-layouts.yaml"
  - name: active_palette
    type: YAML
    source: "{output_dir}/active-palette.yaml"
  - name: iteration_number
    type: integer
    default: 1
    max: 2
  - name: previous_critique_report
    type: optional
    source: "{output_dir}/critique-reports/iteration-{N-1}.yaml"
    desc: "Se iteration > 1, carrega anterior para comparison"
```

### 5. Outputs
```yaml
Outputs:
  - name: critique_report
    type: YAML
    destination: "{output_dir}/critique-reports/iteration-{N}.yaml"
    schema:
      meta:
        deck_id: string
        iteration: integer
        timestamp: string
        agent: "@design-planner"
      pre_check:
        killer_items_check:
          KI-08:                 "PASS | FAIL"
          KI-09:                 "PASS | FAIL"
          KI-10:                 "PASS | FAIL"
        halt_if_any_failed: true
      aggregated_scores:
        narrativa:
          composite: "number 0-10"
          sub_dimensions:
            pyramid_mece: number
            vertical_flow: number
            action_title_rhetoric: number
            governing_thought_strength: number
            scqa_depth: number
            story_arc: number
            slide_function_map: number
        design:
          composite: "number 0-10"
          sub_dimensions:
            density: number
            hierarchy: number
            contrast: number
            readability: number
            visual_coherence: number
        weighted_overall: "number 0-100"
      findings_by_slide:
        - slide_id: string
          worst_dimension: string
          worst_score: number
          findings_count: integer
          severity_breakdown: "object {low, medium, high, critical}"
      routing_decisions:
        - dimension_failed: string
          route_to:
            agent: string
            task: string
            session: string
          slides_affected: "array<string>"
          priority: "P1 | P2 | P3"
      verdict: "PASS | REVISE | ESCALATE"
      escalate_reason: "string OR null"
  - name: planning_reflection_entries
    type: JSONL
    destination: "{output_dir}/planning-reflection.jsonl"
    append: true
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Pre-check killer items BEFORE running validators:"
    sub_actions:
      - "KI-08: slide-function-map.yaml present? all entries non-explanatory? (invoke validate-slide-function-map)"
      - "KI-09: compression ratio respected? (invoke validate-slide-function-map)"
      - "KI-10: design-direction.yaml present? visual_reference.paths non-empty? (inline check)"
      - "Se ANY killer FAIL → HALT iteration loop. Route immediately per qa-routing-table."

  - id: 2
    action: "Invoke 5 design validators em paralelo:"
    sub_actions:
      - "validate-density"
      - "validate-hierarchy"
      - "validate-contrast"
      - "validate-readability"
      - "validate-visual-coherence"

  - id: 3
    action: "Invoke 5 narrative validators em paralelo:"
    sub_actions:
      - "validate-governing-thought-strength"
      - "validate-action-title-rhetoric"
      - "validate-scqa-depth"
      - "validate-story-arc"
      - "validate-slide-function-map"

  - id: 4
    action: "Aggregate scores:"
    sub_actions:
      - "narrativa.composite = avg of 7 narrative sub-dimensions"
      - "design.composite = avg of 5 design sub-dimensions"
      - "weighted_overall = per qa-rubric.yaml weights"

  - id: 5
    action: "Findings_by_slide:"
    sub_actions:
      - "Para cada slide, identificar worst_dimension (lowest sub-score)"
      - "Coletar count + severity breakdown"

  - id: 6
    action: "Routing_decisions:"
    sub_actions:
      - "Para cada dimension com score < 7 OR killer triggered, consult qa-routing-table.yaml"
      - "Group slides_affected por dimension (não rotear slide-a-slide; rotear dimensão-a-dimensão)"
      - "Priority: P1=critical/blocking, P2=high, P3=medium"

  - id: 7
    action: "Verdict logic:"
    sub_actions:
      - "PASS: weighted_overall >= 85 AND killer_items=0 AND narrativa>=7 AND design>=7"
      - "REVISE: weighted_overall in [70, 85) AND killer_items=0 AND iteration < 2"
      - "ESCALATE: weighted_overall < 70 OR iteration_cap_reached OR killer_items > 0 unresolved"

  - id: 8
    action: "Emit critique-report.yaml iteration-{N}.yaml."

  - id: 9
    action: "Append planning-reflection.jsonl entries:"
    sub_actions:
      - "1 entry per failing sub-dimension"
      - "1 score_before_after entry comparing iteration N-1 vs N (se N > 1)"
      - "1 decision entry per routing decision"
      - "Se ESCALATE: 1 escalation entry com summary"

  - id: 10
    action: "Handoff:"
    sub_actions:
      - "Verdict=REVISE → handoff critique-report to @design-renderer (apply-design-revision)"
      - "Verdict=PASS → handoff aggregated_scores to @qa-inspector (final QA macro)"
      - "Verdict=ESCALATE → notify Mission Lead com payload"
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Killer items checked FIRST. ANY killer FAIL → halt iteration."
  - "10 validators invoked (5 design + 5 narrative)"
  - "Aggregated scores per qa-rubric.yaml weights"
  - "Findings_by_slide grouped by worst_dimension"
  - "Routing decisions consult qa-routing-table.yaml — não inventar rotas"
  - "Verdict 3-way: PASS | REVISE | ESCALATE com critérios claros"
  - "Iteration cap=2 enforced — iteration 3 = automatic ESCALATE"
  - "planning-reflection.jsonl appended com 4+ entries per iteration"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_CRITIQUE_REPORT
handoff_to:
  PASS: "@qa-inspector (P05 macro QA)"
  REVISE: "@design-renderer (tasks/apply-design-revision.md)"
  ESCALATE: "Human (Mission Lead) + @slide-chief"
```

## Iteration Flow

```
Iteration 1:
  → Pre-check killer items
  → Invoke 10 validators
  → Verdict: REVISE (most common first iteration)
  → Route fixes
  → @design-renderer applies revisions
  → Iteration 2

Iteration 2:
  → Re-invoke validators
  → Verdict: PASS (target) OR ESCALATE (cap reached)
  → PASS → @qa-inspector
  → ESCALATE → Human with full reflection trail
```
