# Task: Compress Outline to Slide Functions

## Metadata

| Campo | Valor |
|-------|-------|
| task_id | `compress-outline-to-slide-functions` |
| phase | P02.5 (entre P02 Structure e P03 Design) |
| bounded_context | BC-01 (Narrative) |
| schema_ref | data/slide-function-map.schema.yaml + data/story-arc.schema.yaml |
| killer_items_prevented | KI-08, KI-09 |
| session | SESSION-NARR |
| duration | <90s (LLM driven, 1-3 calls) |
| mission_origin | MSN-2026-SLIDES-NARRATIVE-DESIGN (T-015A, GAP-009 closure) |
| case_study | outputs/webinars/primeiro-servico-ia/ |
| model_params | temperature=0, model=sonnet |

## Why this task exists

Lição empírica do webinar Primeiro Serviço de IA: outline de 27 tópicos virou deck de 27 slides ruim porque o pipeline traduziu tópico em slide literalmente. Esta task quebra essa tradução literal: outline → story_arc beats → slide_function_map entries, com **compressão editorial obrigatória**.

## SINKRA Task Anatomy

### 1. task
```yaml
task: compressOutlineToSlideFunctions
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # produz 2 artefatos (story_arc + slide_function_map) acoplados
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # editorial compression requires semantic judgement
```

### 4. Inputs
```yaml
Inputs:
  - name: normalized_briefing
    type: JSON
    source: "{output_dir}/briefing.normalized.json"
  - name: pyramid_tree
    type: YAML
    source: "{output_dir}/pyramid-tree.yaml"
  - name: scqa_map
    type: YAML
    source: "{output_dir}/scqa-map.yaml"
  - name: governing_thought
    type: YAML
    source: "{output_dir}/governing-thought.yaml"
  - name: slides_outline
    type: optional
    source: "{output_dir}/slides-outline.md"
    desc: "se briefing trouxe outline preexistente — usado como input, NÃO como output"
  - name: audience_context
    type: inline
    derived_from: "briefing.normalized.json#audience"
```

### 5. Outputs
```yaml
Outputs:
  - name: story_arc
    type: YAML
    destination: "{output_dir}/story-arc.yaml"
    schema_ref: squads/slides-creator/data/story-arc.schema.yaml
    lifecycle: [draft, validated, approved]
  - name: slide_function_map
    type: YAML
    destination: "{output_dir}/slide-function-map.yaml"
    schema_ref: squads/slides-creator/data/slide-function-map.schema.yaml
    lifecycle: [draft, validated, approved]
```

### 6. action_items
```yaml
action_items:
  - id: 1
    action: "Identify arc_type apropriado para o briefing:"
    sub_actions:
      - "Audience type + delivery format → enum (educational_workshop, executive_pitch, sales_narrative, etc.)"
      - "Single arc_type selected — não múltiplos"

  - id: 2
    action: "Derive beats[] (4-8 beats):"
    sub_actions:
      - "Cada beat tem narrative_function (1 sentence explaining audience movement)"
      - "Cobre minimum: 1 opening (hook/tension/reframe), 1 payoff (proof/demo/artifact_reveal), 1 closing (cta/close)"
      - "Cada beat referencia source_outline_topics (rastreabilidade — quais topics do outline original)"

  - id: 3
    action: "Para cada beat, propor slides_estimated (1-3 slides per beat):"
    sub_actions:
      - "Heuristic: hook/cta=1 slide, tension/mechanism=2-3, demo=1-2"
      - "TOTAL slides = sum(beats[].slides_estimated). Target 12-16."
      - "HARD CAP: total <= 1.2 × len(outline_topics) — enforces compression"

  - id: 4
    action: "Para cada slide planejado, criar slide_function_map.entries[]:"
    sub_actions:
      - "slide_id (s01, s02, ...)"
      - "beat_ref → liga ao beat correspondente"
      - "function → enum (cover, reframe, proof, contrast, demo_payoff, artifact_reveal, etc.)"
      - "audience_movement → 1 sentence concreta. PROIBIDO começar com 'explicar/apresentar/falar/mostrar X'"
      - "slide_type → mapped to existing 7 archetypes (title, executive_summary, framework, data, timeline, financial, appendix) OR extended set"
      - "density_target → minimal/low/medium/high"
      - "merged_from_topics → quais outline topics foram fundidos neste slide (rastreabilidade compression)"
      - "could_be_cut_if → critério de corte se appetite estourar (força priorização)"

  - id: 5
    action: "Validar localmente:"
    sub_actions:
      - "Sum slides_estimated == len(entries)"
      - "Toda entry tem function ∈ enum"
      - "Nenhuma audience_movement começa com 'explicar/apresentar/falar/mostrar X'"
      - "Has at least 1 entry com function ∈ {demo_payoff, artifact_reveal}"
      - "Has at least 1 entry com function = cta_concrete"

  - id: 6
    action: "Emit story-arc.yaml + slide-function-map.yaml."

  - id: 7
    action: "Append planning-reflection.jsonl entries:"
    sub_actions:
      - "{phase:'narrative_planning', entry_type:'decision', dimension:'story_arc', claim:'arc_type={X} chosen', rationale}"
      - "{phase:'narrative_planning', entry_type:'decision', dimension:'slide_function_map', claim:'compressed {N} topics into {M} slides', evidence:'ratio={M/N}'}"
```

### 7. acceptance_criteria
```yaml
acceptance_criteria:
  - "Output story-arc.yaml + slide-function-map.yaml ambos válidos contra seus schemas"
  - "Total slides (sum slides_estimated) <= 1.2 × len(outline_topics) — compression enforced"
  - "Toda entry tem audience_movement não-explanatória (regex check inline)"
  - "Has payoff function (demo_payoff OR artifact_reveal)"
  - "Has CTA function (cta_concrete)"
  - "Validação cross: validate-story-arc + validate-slide-function-map devem PASS antes de avançar para P03"
  - "Calibração: rodar contra Primeiro Servico v1 inputs (27 topics) deve produzir 12-16 slides com função declarada"
```

### 8. handoff_token
```yaml
handoff_token: BC-01_STORY_ARC_AND_FUNCTION_MAP
handoff_to:
  - "@design-renderer (consumes for define-design-direction + compose-grid-layout)"
  - "@content-architect (next: write-action-titles agora usa slide_function_map entries)"
  - "Validators: validate-story-arc + validate-slide-function-map"
```

## Compression Heuristics

| Outline pattern | Compression strategy |
|---|---|
| 5+ tópicos consecutivos sobre mesmo conceito | Fundir em 1-2 slides max |
| Tópico "FAQ" com 10 perguntas | Coletar em 1-2 slides de objection_neutralize |
| Tópico "Apresentação" / "Sobre nós" | 1 slide cover OR cortado |
| Tópico "Próximos passos" / "Como contratar" | 1 slide cta_concrete |
| Tópicos analíticos densos | 1 slide framework + 1 slide proof + 1 slide demo (não 3 slides explicativos) |

## Anti-Patterns

- **1:1 mapping:** 1 topic = 1 slide. Falha automaticamente se ratio > 1.2.
- **Function = explicar:** audience_movement começa com "explicar X". Falha.
- **Missing payoff:** nenhum demo_payoff/artifact_reveal. Falha.
- **Missing CTA:** nenhum cta_concrete. Falha.
