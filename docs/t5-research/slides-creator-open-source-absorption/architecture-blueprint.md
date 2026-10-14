# Architecture Blueprint — slide creator skill stack

## Objetivo

Arquitetura-alvo para transformar `slides-creator` em produto/runtime sem perder a governança SINKRA.

## Componentes

```text
Inputs
  prompt | PDF | DOCX | PPTX | URL | YouTube
    |
    v
Intake Layer
  briefing.normalized.json
    |
    v
Narrative Core
  Pyramid | SCQA | action titles | sources
    |
    v
Planning Reflection
  narrative-plan.yaml | design-plan.yaml | planning-reflection.jsonl
    |
    v
DeckSpec Layer
  deck-spec.yaml | slide-specs/*.yaml
    |
    v
Render Layer
  Native IR | PPTX renderer | PDF fallback | web preview
    |
    v
QA Layer
  qa-report.json | editability-report.json | visual snapshots
    |
    v
Delivery
  PPTX | PDF | web link | future MP4
```

## Ownership por Camada

| Camada | Owner SINKRA | Referência OSS | Artifact |
|---|---|---|---|
| Intake | `slide-chief` | Presenton | `briefing.normalized.json` |
| Narrative Core | `content-architect` | interno | `narrative-plan.yaml` |
| Planning Reflection | `content-architect` + `qa-inspector` | PPTAgent | `planning-reflection.jsonl` |
| DeckSpec | `slide-chief` | interno + PPTAgent | `deck-spec.yaml` |
| Native IR | `design-renderer` | `ppt-master` | `native-slide-ir.json` |
| Renderer | future `slides-renderer` service | `ppt-master`, powerpoint-skill | `deck.pptx`, `deck.pdf` |
| API/MCP | future `slides-api` service | Presenton | endpoints + MCP tools |
| Editor | future app | presentation-ai, banana patterns | DeckSpec diffs |

## Data Flow

1. API/CLI/MCP recebe input.
2. `slide-chief` normaliza briefing.
3. `content-architect` gera plano narrativo.
4. `template-curator` resolve template e brand tokens.
5. `design-renderer` gera DeckSpec e Native IR.
6. Renderer exporta PPTX/PDF.
7. `qa-inspector` valida narrativa, visual, fontes e editabilidade.
8. Release só ocorre sem killer items.

## Não Objetivos no MVP

- Editor visual completo.
- Export MP4.
- Q&A interativo.
- Analytics avançado.
- Fork de qualquer projeto open-source.
