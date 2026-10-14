# QA Rubric — slide creator skill stack

## Objetivo

Unificar QA narrativo, visual, editabilidade e fontes em uma rubrica única.

## Dimensões

| Dimensão | Peso | Gate | Fonte |
|---|---:|---|---|
| Narrativa | 25 | Pyramid, SCQA, action titles, fluxo vertical | slides-creator |
| Acurácia e fontes | 20 | Claims críticos com fonte, sem invenção | slides-creator |
| Design | 15 | Hierarquia, contraste, legibilidade, densidade | PPTAgent + qa-inspector |
| Editabilidade | 20 | Objetos nativos e textos editáveis | ppt-master-inspired renderer |
| Template/brand | 10 | Cores, fontes, layout e consistência | Presenton + ppt-master |
| Técnica | 10 | Export, links, diagramas, math, arquivos abrem | powerpoint-skill |

## Killer Items

Qualquer item abaixo bloqueia release:

- PPTX não abre ou pede repair.
- Action title rasterizado sem camada editável.
- Claim crítico sem fonte.
- Texto cortado em slide principal.
- Contraste ilegível.
- Deck viola briefing aprovado.
- Export faltando quando solicitado.

## Score

```json
{
  "overall_score": 88,
  "killer_items": 0,
  "dimensions": {
    "narrative": 92,
    "sources": 85,
    "design": 84,
    "editability": 86,
    "brand": 90,
    "technical": 88
  }
}
```

## Critérios de Release

| Status | Condição |
|---|---|
| `passed` | `killer_items = 0` e score geral >= 85 |
| `concerns` | `killer_items = 0` e score geral entre 75 e 84 |
| `failed` | `killer_items > 0` ou score geral < 75 |
