# Task: Validate Action Title Rhetoric (Narrative sub-dimension, P4+)

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `validate-action-title-rhetoric` |
| phase | P05 + P04.5 |
| bounded_context | BC-01 (Narrative) → BC-06 (QA) |
| invariants_enforced | P4+ (extends P4) |
| rubric_dim_ref | data/qa-rubric.yaml#dimensions.narrativa.sub_dimensions.action_title_rhetoric |
| killer_items | KI-07 (descriptive_violation) |
| session | SESSION-QA |
| duration | <60s (LLM call per slide, batched) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-012) |
| model_params | temperature=0, model=sonnet |

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateActionTitleRhetoric
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # classification rhetoric requires semantic judgement
```

### 4. Inputs
```yaml
Inputs:
  - name: deck_spec
    type: YAML
    source: "{output_dir}/deck-spec.yaml"
  - name: action_title_corpus
    type: optional
    source: squads/slides-creator/examples/action-titles-corpus.yaml
    desc: "labeled corpus for in-context calibration"
  - name: classification_taxonomy
    type: inline
    spec: "ver Taxonomy abaixo"
```

### 5. Outputs
```yaml
Outputs:
  - name: action_title_rhetoric_report
    type: YAML
    destination: "{output_dir}/validator-reports/action-title-rhetoric.yaml"
    schema:
      dimension: action_title_rhetoric
      dimension_score: "number 0-10"
      verdict: "PASS | REVIEW | FAIL"
      classifications:
        executive_strong: integer
        executive_weak: integer
        descriptive_violation: integer
        total: integer
      per_slide:
        - slide_id: string
          action_title: string
          classification: "executive_strong | executive_weak | descriptive_violation"
          components:
            has_verb: boolean
            has_subject: boolean
            has_magnitude_or_implication: boolean
            tense: "past | present | future | none"
            cinematic_strength: "number 0-10"  # carries momentum?
          rationale: string
          suggested_rewrite: "string OR null"
      killer_items_triggered: "array<string>"  # KI-07 when descriptive_violation > 0
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Extrair action_titles de cada slide em deck_spec."
  - id: 2
    action: "Classificar via LLM (sonnet, temp=0) em 3 classes:"
    sub_actions:
      - "executive_strong: verb + subject + (magnitude OR implication) + cinematic momentum"
      - "executive_weak: verb + subject + ausência de magnitude/implication OR cinematicamente fraca"
      - "descriptive_violation: sem verbo OR título apenas nominal ('Análise de mercado')"
  - id: 3
    action: "Per slide, decompor em componentes: has_verb, has_subject, has_magnitude_or_implication, tense, cinematic_strength."
  - id: 4
    action: "Calcular dimension_score:"
    sub_actions:
      - "Base = (executive_strong / total) * 10"
      - "Penalty = (descriptive_violation / total) * 8"
      - "score = max(0, base - penalty)"
  - id: 5
    action: "Verdict:"
    sub_actions:
      - "PASS if zero descriptive_violation AND executive_weak <= 20% AND score >= 7"
      - "REVIEW if descriptive_violation == 0 AND score >= 5"
      - "FAIL if any descriptive_violation → KI-07 triggered"
  - id: 6
    action: "Suggested_rewrite via LLM para cada executive_weak e descriptive_violation."
  - id: 7
    action: "Append planning-reflection.jsonl entries (1 por slide com classification != executive_strong)."
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Temperature=0, sonnet pinned"
  - "Classification em 3 classes discretas"
  - "Decomposição em components obrigatória"
  - "KI-07 disparado se ANY descriptive_violation"
  - "Suggested_rewrite para todo título não-strong"
  - "Calibração: corpus gold scores >=80% executive_strong"
```

### 8. handoff_token
```yaml
handoff_token: BC-06_ACTION_TITLE_RHETORIC_REPORT
on_fail_route: per data/qa-routing-table.yaml → @content-architect + tasks/write-action-titles.md
```

## Classification Taxonomy

### EXECUTIVE_STRONG
- Verbo de ação concreto (cresceu, caiu, captura, perdeu, ganha)
- Sujeito explícito (não pronome vago)
- Magnitude OU implicação carregada
- Tense: past (preferido) OR present (acontecendo)
- Cinematic: imagem mental se forma

Exemplos:
- "Receita LATAM cresceu 30% YoY apesar de inflação 8%"
- "Concorrente X captura 12pp de share em 4 meses sem aumentar gasto"
- "Margem operacional cai 5pp em Q4 — cost-to-serve dobrou"

### EXECUTIVE_WEAK
- Tem verbo + sujeito + (magnitude OU implicação) mas faltando força narrativa
- Cinematic strength baixo
- Tense pode ser presente neutro

Exemplos:
- "Mercado cresce 8% ao ano" (sem implicação)
- "Customers preferem produto X" (sem magnitude)
- "Tendência de digitalização continua" (sem ambos quantitativos)

### DESCRIPTIVE_VIOLATION (KILLER)
- Sem verbo (apenas nominal)
- "Análise de X", "Visão geral de Y", "Sobre Z"
- "Gráfico de receita", "Tabela comparativa"
- "Estatísticas do mercado"

Esses dispara KI-07 automaticamente.

## Calibração

Corpus gold em `squads/slides-creator/examples/action-titles-corpus.yaml`:
- 30 títulos labeled executive_strong (target)
- 20 labeled executive_weak (boundary)
- 15 labeled descriptive_violation (anti-pattern)

Test set: re-classificar; accuracy >=85% para considerar calibrado.
