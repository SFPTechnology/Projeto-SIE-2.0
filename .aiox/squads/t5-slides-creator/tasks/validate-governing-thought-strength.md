# Task: Validate Governing Thought Strength (Narrative sub-dimension)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-governing-thought-strength` |
| phase | P05 + P04.5 |
| bounded_context | BC-01 (Narrative) → BC-06 (QA) |
| invariants_enforced | P3 (precursor), P4 (precursor) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.narrativa.sub_dimensions.governing_thought_strength |
| session | SESSION-QA |
| duration | <30s (LLM call) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-011) |
| model_params | temperature=0, model=sonnet (RH-001 mitigation) |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateGoverningThoughtStrength
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # semantic judgement via LLM com rubric calibrada
```

### 4. Inputs
```yaml
Inputs:
  - name: governing_thought
    type: YAML
    source: "{output_dir}/governing-thought.yaml"
    schema: "{sentence: string, source_topics: array}"
  - name: rubric
    type: inline
    spec: "ver Rhetoric Rubric abaixo"
  - name: gold_standard_corpus
    type: optional
    source: squads/slides-creator/examples/governing-thoughts-gold.yaml
```

### 5. Outputs
```yaml
Outputs:
  - name: governing_thought_strength_report
    type: YAML
    destination: "{output_dir}/validator-reports/governing-thought-strength.yaml"
    schema:
      dimension: governing_thought_strength
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      decomposition:
        claim_present:
          score: "number 0-10"
          rationale: string
          extracted: "string OR null"
        magnitude_present:
          score: "number 0-10"
          rationale: string
          extracted: "string OR null"
        implication_present:
          score: "number 0-10"
          rationale: string
          extracted: "string OR null"
      composite_score: "weighted: claim*0.4 + magnitude*0.3 + implication*0.3"
      word_count: integer
      executive_classification: "executive_strong | executive_weak | descriptive | hollow"
      suggested_rewrite: "string OR null"
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Carregar governing_thought.sentence."
  - id: 2
    action: "Word count check: penalizar >35 palavras (P3 boundary)."
  - id: 3
    action: "Decomposição via LLM (temperature=0, sonnet):"
    sub_actions:
      - "claim_present: a sentença tem afirmação explícita verificável? (não pergunta, não desejo)"
      - "magnitude_present: a sentença carrega escala/quantificação/proporção?"
      - "implication_present: a sentença explicita consequência/ação/decisão?"
  - id: 4
    action: "Cada sub-score 0-10 com rationale + componente extraído (ou null)."
  - id: 5
    action: "executive_classification:"
    sub_actions:
      - "executive_strong: claim AND magnitude AND implication, cada >=7"
      - "executive_weak: 2 de 3 presentes (>=6)"
      - "descriptive: apenas claim presente (factual mas opaca)"
      - "hollow: claim ausente OR aspiracional"
  - id: 6
    action: "Se executive=descriptive OR hollow → suggested_rewrite via LLM."
  - id: 7
    action: "Verdict: PASS if composite >= 7; REVIEW if 5-6.9; FAIL < 5."
  - id: 8
    action: "Append planning-reflection.jsonl: {phase:'narrative_planning', dimension:'governing_thought_strength', entry_type:'critique' OR 'hypothesis', decomposition, decision}."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Sempre temperature=0 e modelo=sonnet (reprodutibilidade)"
  - "Decomposition em 3 componentes com rationale obrigatório"
  - "executive_classification em 4 níveis discretos"
  - "Suggested_rewrite emitido para descriptive/hollow"
  - "Calibração contra gold-standard: gold scores >=8.5 average"
  - "Variance entre 2 runs no mesmo input <= 0.5 score (RH-001)"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_GOVERNING_THOUGHT_STRENGTH_REPORT
on_fail_route: per data/qa-routing-table.yaml → @content-architect + tasks/distill-governing-thought.md
```

## Rhetoric Rubric

### Componente 1: CLAIM (peso 0.4)
- 10: Afirmação verificável, específica, sem hedge
- 7: Afirmação clara mas com hedge mínimo ("provavelmente", "tende a")
- 4: Afirmação vaga ("o mercado está mudando")
- 0: Pergunta, desejo, ou aspiração ("queremos crescer")

### Componente 2: MAGNITUDE (peso 0.3)
- 10: Quantificação precisa (%, R$, X, multiplicador, range)
- 7: Comparação proporcional sem número exato ("dobrou", "metade")
- 4: Adjetivo qualitativo forte ("massivo", "explosivo")
- 0: Sem magnitude alguma

### Componente 3: IMPLICATION (peso 0.3)
- 10: Consequência/ação/decisão explícita ("portanto, devemos...")
- 7: Implicação derivável diretamente
- 4: Implicação possível mas requer raciocínio adicional
- 0: Afirmação sem ponte para ação

## Exemplos Calibração

| Sentence | claim | magnitude | implication | composite | class |
|---|---|---|---|---|---|
| "Receita cresceu 30% YoY em LATAM, exigindo expansão de fulfillment até Q2." | 9 | 9 | 9 | 9.0 | executive_strong |
| "O mercado está mudando rapidamente." | 4 | 4 | 0 | 2.8 | hollow |
| "Margem cai 5pp em Q4." | 8 | 8 | 2 | 6.2 | executive_weak |
| "78% dos microempreendedores nunca tentaram IA, criando oportunidade de R$ 200M até 2026." | 9 | 9 | 8 | 8.7 | executive_strong |
| "Nosso produto é o melhor do mercado." | 5 | 0 | 0 | 2.0 | hollow |
