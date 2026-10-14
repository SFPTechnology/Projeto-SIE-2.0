# Task: Catalog Sources (APA Business)

## Metadata
| Campo | Valor |
|-------|-------|
| task_id | `catalog-sources-apa` |
| phase | P01 — Narrative Analysis |
| bounded_context | BC-04 (Source Catalog) |
| invariants_enforced | P1 (Fidelidade), P6 (APA) |
| session | SESSION-NARR |
| duration | 10-30 min per deck |

## SINKRA Task Anatomy

### 1. task
```yaml
task: catalogSourcesAPA
```

### 2. atomic_layer
```yaml
atomic_layer: Molecule  # 4 atoms: ler_material + extrair_numero + extrair_citacao + catalogar_fonte
```

### 3. responsavel_type
```yaml
responsavel_type: Agent  # content-architect @ SESSION-NARR
```

### 4. Inputs[]
```yaml
Inputs:
  - name: briefing
    type: JSON
    source: "{output_dir}/briefing.normalized.json"
    required: true
  - name: source_materials
    type: files
    source: "briefing.source_paths[]"
    required: true
  - name: kb_bundle
    type: text
    source: "kb-loading-matrix.yaml lookup (SESSION-NARR)"
    required: true
```

### 5. Outputs[]
```yaml
Outputs:
  - name: sources_apa
    type: YAML
    destination: "{output_dir}/sources-apa.yaml"
    schema:
      data_points: "array<{id, value, unit, source_ref, precision_preserved, verbatim}>"
      citations: "array<{id, org, title, date, url, access_date, context_ref}>"
      gaps: "array<{marker: '[VALIDAR COM CLIENTE]', context, suspected_value}>"
```

### 6. Pre-conditions
```yaml
Pre-conditions:
  - "briefing.normalized.json exists and parses"
  - "at least 1 source material path exists"
  - "kb_bundle loaded (KB_01 + firm_style KB + industry KB)"
```

### 7. Post-conditions + Acceptance
```yaml
Post-conditions:
  - "Every number extracted has source_ref pointing back to a specific document + page/section"
  - "Every quote is verbatim (no paraphrase)"
  - "Gaps are marked explicitly — NEVER filled with hallucinated values"
  - "APA schema complete per citation: {org, title, date, url, access_date}"

Acceptance_criteria:
  - "P1 enforcement: 0 data_points without source_ref"
  - "P6 enforcement: 0 citations with missing APA fields"
  - "Gap register not empty if source material has ambiguity"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "10-30 min"
  cost: "moderate (heavy LLM read)"
  cacheable: true  # by briefing hash

Error_handling:
  strategy: retry
  max_retries: 2
  fallback: Human  # STK-05 senior consultant manual extraction
  on_schema_fail: halt_and_surface_gap_list
```

## Invocation contract
```
@content-architect *catalog-sources-apa --input {output_dir}/briefing.normalized.json
```

## Anti-patterns
- Inferring missing dates, URLs, or author names to "complete" citations → violates P1. Mark as gap.
- Paraphrasing quotes for brevity → violates P1 (verbatim rule).
- Rounding numbers "for readability" → violates P1.
