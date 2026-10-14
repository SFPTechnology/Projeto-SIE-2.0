# Task: Write Action Titles

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `write-action-titles` |
| phase | P02 |
| bounded_context | BC-01 |
| invariants_enforced | P4 (Action Titles) |
| session | SESSION-NARR |
| duration | 15-45 min |

## SINKRA Task Anatomy

### 1. task
```yaml
task: writeActionTitles
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # N atoms (one per slide in scqa_map.slide_sequence)
```

### 3. responsavel_type
```yaml
responsavel_type: Agent
```

### 4. Inputs[]
```yaml
Inputs:
  - name: scqa_map
    type: YAML
    source: "{output_dir}/scqa-map.yaml"
    required: true
  - name: pyramid_tree
    type: YAML
    source: "{output_dir}/pyramid-tree.yaml"
    required: true
  - name: sources_apa
    type: YAML
    source: "{output_dir}/sources-apa.yaml"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: deck_manifest_partial
    type: JSON
    destination: "{output_dir}/deck-manifest.json"  # v2, partial fill of slides[]
    schema_patch:
      slides:
        - pos: int
          action_title: "string"
          slide_type_draft: "Title | ExecSummary | Data | Framework | Financial | Timeline | Appendix"
          segment: "S | C | Q | A"
          pillar_id: "string | null"
          evidence_refs: "array<data_point_id>"
          p4_components:
            what_happened: "string"
            magnitude_or_why: "string"
            implication: "string | null"  # optional for title/intro slides
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "scqa-map.yaml validated"
  - "pyramid-tree.yaml validated"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Every slide in scqa_map has a corresponding action_title"
  - "Every action_title has ≥ 2 of 3 P4 components (what/magnitude/implication)"
  - "Descriptive titles ('Análise de market share') flagged FAIL"

Acceptance_criteria:
  - "validate-action-title (P05) PASS when this output is tested"
  - "Reading titles in order tells a coherent story (run-vertical-test is next)"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "30s-90s per slide × N slides"
  cost: "moderate"
  cacheable: false

Error_handling:
  strategy: retry_per_slide_on_fail
  max_retries_per_slide: 2
  fallback: Human
  on_p4_fail: "re-prompt with missing component + regex"
```

## Anti-patterns
- Title starts with noun phrase + "analysis" / "overview" → descriptive, reject.
- Same magnitude phrase repeated across slides → lazy, reject.
- Title conclusions contradict pyramid pillars → logical inconsistency, reject.

## Example (good)
| Bad (descriptive) | Good (action) |
|---|---|
| "Análise de mercado" | "Mercado brasileiro crescerá 45% ao ano até 2027, 1.7× média global" |
| "Resultados financeiros" | "EBITDA expandiu 23% YoY impulsionado por mix premium (+340bps margem)" |
