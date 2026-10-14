# Task: Validate SCQA Depth (Narrative sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-scqa-depth` |
| phase | P05 + P04.5 |
| bounded_context | BC-01 (Narrative) → BC-06 (QA) |
| invariants_enforced | P3 (extends apply-scqa proportions check) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.narrativa.sub_dimensions.scqa_depth |
| session | SESSION-QA |
| duration | <45s (LLM batched per bloco) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-013) |
| model_params | temperature=0, model=sonnet |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateScqaDepth
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # semantic depth per bloco
```

### 4. Inputs
```yaml
Inputs:
  - name: scqa_map
    type: YAML
    source: "{output_dir}/scqa-map.yaml"
  - name: pyramid_tree
    type: YAML
    source: "{output_dir}/pyramid-tree.yaml"
  - name: rubric
    type: inline
    spec: "per-block rubric: S grounds context, C sharpens tension, Q narrows scope, A delivers"
```

### 5. Outputs
```yaml
Outputs:
  - name: scqa_depth_report
    type: YAML
    destination: "{output_dir}/validator-reports/scqa-depth.yaml"
    schema:
      dimension: scqa_depth
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      blocks:
        situation:
          score: "number 0-10"
          rubric: "grounds context with shared facts; no contestation"
          rationale: string
          weakness: "string OR null"
        complication:
          score: "number 0-10"
          rubric: "sharpens tension; creates productive discomfort"
          rationale: string
          weakness: "string OR null"
        question:
          score: "number 0-10"
          rubric: "narrows scope to one decision; mutually exclusive options implied"
          rationale: string
          weakness: "string OR null"
        answer:
          score: "number 0-10"
          rubric: "delivers governing thought + 3 pillars with proof"
          rationale: string
          weakness: "string OR null"
      composite_score: "avg of 4 blocks"
      depth_distribution: "balanced | front-heavy | back-heavy | shallow"
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Carregar scqa_map + pyramid_tree."
  - id: 2
    action: "Para cada bloco S/C/Q/A, extrair conteúdo + alocação %."
  - id: 3
    action: "Avaliar S (Situation):"
    sub_actions:
      - "Fatos compartilhados (não contestáveis)? +3"
      - "Específico ao contexto da audiência? +3"
      - "Conciso (não overexplain)? +2"
      - "Liga para Complication? +2"
  - id: 4
    action: "Avaliar C (Complication):"
    sub_actions:
      - "Tensão concreta (não abstrata)? +3"
      - "Implica decisão necessária? +3"
      - "Conecta com governing thought? +2"
      - "Sem hedge ('talvez', 'pode ser')? +2"
  - id: 5
    action: "Avaliar Q (Question):"
    sub_actions:
      - "Pergunta única, não múltipla? +3"
      - "Forçar decisão (não open-ended)? +3"
      - "Implica 2-3 opções mutuamente exclusivas? +2"
      - "Curta (1-2 sentences)? +2"
  - id: 6
    action: "Avaliar A (Answer):"
    sub_actions:
      - "Governing thought entregue claramente? +3"
      - "3 pillars com proof per pillar? +3"
      - "Cada proof traceable a fonte (P6 connection)? +2"
      - "Síntese final ou call-back ao C/Q? +2"
  - id: 7
    action: "depth_distribution: avg de cada bloco vs proporção alocada — flag mismatches."
  - id: 8
    action: "Verdict: PASS if composite >= 7 AND no bloco < 5."
  - id: 9
    action: "Append planning-reflection.jsonl entry."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "4 sub-scores 0-10 com rationale + weakness identification"
  - "Validação independente de scqa proportions (P3 sintático)"
  - "Verdict FAIL se ANY bloco <5 (depth weakness arrasta o todo)"
  - "depth_distribution comparada com proporção alocada"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_SCQA_DEPTH_REPORT
on_fail_route: per data/qa-routing-table.yaml → @content-architect + tasks/apply-scqa.md
```
