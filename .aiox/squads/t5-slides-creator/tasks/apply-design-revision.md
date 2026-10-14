# Task: Apply Design Revision

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `apply-design-revision` |
| phase | P04.5 (entre P04 Specification e P05 QA macro) |
| bounded_context | BC-03 (Spec) |
| session | SESSION-SPEC |
| duration | <120s (LLM-driven revision per slide affected) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-017) |
| iteration_cap_enforced | 2 |

## Why this task exists

Para fechar o loop critique→revise. Sem este task, @design-planner emite critique mas o draft não é atualizado. Este task aplica as revisions roteadas, emite deck-spec atualizado, e registra before/after em planning-reflection.

## SINKRA Task Anatomy

### 1. task
```yaml
task: applyDesignRevision
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # revisions semânticas requerem LLM judgement
```

### 4. Inputs
```yaml
Inputs:
  - name: critique_report
    type: YAML
    source: "{output_dir}/critique-reports/iteration-{N}.yaml"
    required: true
    must_have_verdict: REVISE
  - name: deck_spec_current
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
  - name: design_direction
    type: YAML
    source: "{output_dir}/design-direction.yaml"
  - name: slide_function_map
    type: YAML
    source: "{output_dir}/slide-function-map.yaml"
  - name: iteration_number
    type: integer
    max: 2
```

### 5. Outputs
```yaml
Outputs:
  - name: deck_spec_revised
    type: YAML
    destination: "{output_dir}/deck-spec.yaml"
    overwrite: true
    version_field: "revision_iteration: N"
  - name: revision_log
    type: YAML
    destination: "{output_dir}/critique-reports/revision-{N}.yaml"
    schema:
      revisions_applied:
        - slide_id: string
          dimension_addressed: string
          before:
            element_id: string
            value: any
          after:
            element_id: string
            value: any
          rationale: string
          score_delta_estimate: number
      routes_resolved: integer
      routes_skipped: integer  # com motivo
      iteration: integer
      iteration_cap_reached: boolean
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Enforce iteration cap: se iteration_number > 2 → HALT + raise iteration_cap_reached escalation."

  - id: 2
    action: "Carregar critique_report. Verify verdict=REVISE (else HALT)."

  - id: 3
    action: "Para cada routing_decision em critique_report:"
    sub_actions:
      - "Filter routes by priority (P1 first)"
      - "Para cada slide_affected em route:"
      - "  - Read current slide spec from deck-spec.yaml"
      - "  - Apply revision per dimension_failed:"
      - "    * density: split slide OR remove supporting claims"
      - "    * hierarchy: adjust typography tokens"
      - "    * contrast: substitute fg/bg per active-palette"
      - "    * readability: reflow text OR upgrade font_size"
      - "    * visual_coherence: re-apply dominant_motif"
      - "    * action_title_rhetoric: rewrite title (LLM suggested_rewrite)"
      - "    * governing_thought_strength: re-distill governing thought"
      - "  - Log before/after in revision_log"

  - id: 4
    action: "Skip routes onde delta esperado < 0.5 (low-value revisions)."

  - id: 5
    action: "Update deck-spec.yaml com revisions aplicadas. Increment revision_iteration counter."

  - id: 6
    action: "Emit revision-{N}.yaml log."

  - id: 7
    action: "Append planning-reflection.jsonl entries:"
    sub_actions:
      - "1 revision_applied entry per slide+dimension revisado"
      - "1 score_before_after entry estimando delta esperado"

  - id: 8
    action: "Handoff:"
    sub_actions:
      - "Iteration < 2 → handoff back to @design-planner para run-design-critique iteration N+1"
      - "Iteration == 2 → handoff direto para @qa-inspector (macro QA) + flag iteration_cap_reached=true"
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Iteration cap enforced (max 2)"
  - "Revisions aplicadas per critique routing_decisions (não inventar fixes)"
  - "Before/after registrado em revision_log + planning-reflection.jsonl"
  - "P1 priorities processed first; P3 podem ser skipped com justificativa"
  - "deck-spec.yaml mantém schema validity após revisions"
  - "Revision_iteration counter incrementado"
```

### 8. handoff_token
```yaml
handoff_token: BC-03_DECK_SPEC_REVISED
handoff_to:
  iteration_lt_2: "@design-planner (tasks/run-design-critique.md iteration N+1)"
  iteration_eq_2: "@qa-inspector (P05 macro QA)"
```

## Revision Strategies per Dimension

| Dimension | Strategy | Cost |
|---|---|---|
| density | Split slide OR remove supporting claim OR reduce text | Low |
| hierarchy | Adjust typography token (--slide-title-X) | Low |
| contrast | Substitute fg/bg from active-palette | Low |
| readability | Reflow text OR upgrade font_size OR shorten lines | Medium |
| visual_coherence | Re-apply dominant_motif elements | Medium |
| action_title_rhetoric | LLM rewrite per suggested_rewrite from validator | Medium |
| governing_thought_strength | Re-distill (full LLM call) | High |
| scqa_depth | Strengthen affected block per validator weakness | High |
| story_arc | Re-architecture (often requires re-compress-outline) | Very High → ESCALATE |
| slide_function_map | Same as story_arc (architectural) | Very High → ESCALATE |

## Skip Logic

Routes podem ser skipped se:
- delta_estimate < 0.5 (low ROI revision)
- revision_cost = Very High AND iteration > 1 (escalation preferred)
- Mission Lead skip_directive registered

Cada skip vira entry em revision_log com `skipped: true, reason: ...`.
