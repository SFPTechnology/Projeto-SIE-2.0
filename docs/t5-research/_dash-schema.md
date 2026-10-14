# Bench Dashboard Output Schema

`bench-output-dash.json` é a projeção normalizada usada pelo Bench Dashboard. Ele não substitui os artefatos originais do benchmark; consolida `metadata.json`, `scorecard.json`, `consolidated-scorecard.json`, `comparison-matrix.json`, `gap-analysis.json` e markdowns em um formato pronto para renderização.

## Local

```text
docs/bench/{slug}/bench-output-dash.json
```

## Contrato

```json
{
  "schema": "bench-output-dash.v1",
  "generated_at": "2026-05-11T00:00:00.000Z",
  "source_files": [],
  "benchmark": {
    "slug": "chatwoot-vs-zendesk",
    "title": "Chatwoot vs Zendesk",
    "date": "2026-05-06",
    "type": "product",
    "variant": "2-way",
    "analyst": "unknown"
  },
  "players": [
    {
      "key": "chatwoot",
      "name": "Chatwoot",
      "category": "unknown"
    }
  ],
  "summary": {
    "winner": "mixed",
    "coverage": "partial",
    "sources": 0,
    "waves": 0,
    "dimensions": 0
  },
  "matrix": {
    "players": [],
    "dimensions": [],
    "rows": [],
    "totals": [],
    "method": ""
  },
  "duels": [],
  "personas": [],
  "gaps": [],
  "sources": [],
  "artifacts": [],
  "readiness": {
    "matrix": "missing",
    "duels": "missing",
    "personas": "missing",
    "gaps": "missing",
    "sources": "missing"
  },
  "inferred": {}
}
```

## Readiness

- `complete`: dados estruturados suficientes para renderização rica.
- `derived`: dados derivados de scorecard ou matriz, sem artefato dedicado.
- `partial`: dados presentes, mas incompletos.
- `missing`: bloco ausente.

## Regras

- `benchmark.slug` sempre é o nome da pasta.
- `players[]` sempre usa array, mesmo em 2-way.
- `matrix.rows[]` é o formato preferencial para comparação visual.
- `duels[]` é derivado de `matrix.rows[]`.
- `personas[]` só aparece quando existe fonte explícita ou score por cenário.
- Campos preenchidos por heurística devem ser marcados em `inferred`.
