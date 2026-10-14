# Deep Dive — Open-Source to SINKRA Map

## Mapa de Absorção por Componente

| Componente SINKRA futuro | Fonte primária | Fonte secundária | Onde encaixa |
|---|---|---|---|
| `services/slides-renderer` | `ppt-master` | powerpoint-skill | L4 Services |
| `services/slides-api` | Presenton | slide-deck-ai | L4 Services |
| `mcp/slides-server` | Presenton | PPTAgent | L4 Services / L6 Framework |
| `deck-spec.yaml` | slides-creator | PPTAgent | L2 Execution |
| `native-slide-ir.schema.json` | `ppt-master` | slides-creator | L5/L6 shared schema |
| `planning-reflection.jsonl` | PPTAgent | slides-creator | L2 Execution |
| `editability-report.json` | `ppt-master` | powerpoint-skill | L2/L4 QA |
| `outline-editor` | presentation-ai | banana-slides | L3 Product |
| `block-card-editor` | BlockNote/Tiptap | ProseMirror | L3 Product |
| `realtime-collaboration` | Yjs/Hocuspocus | presentation-ai sharing patterns | L3 Product |
| `prompt-to-edit` | banana-slides | ppt-master live preview | L3 Product |
| `template-importer` | `ppt-master` | Presenton | L4 Services |
| `math-diagram-engine` | powerpoint-skill | slide-deck-ai | L4 Services |
| `share-runtime` | presentation-ai | Gamma benchmark | L3 Product |
| `deck-analytics` | PostHog/Umami/Plausible | Gamma benchmark | L3 Product |
| `markdown-web-fallback` | Slidev/Marp | PptxGenJS image mode | L4 Services |
| `video-export` | PresentAgent-2 | `ppt-master`, banana-slides | L3/L4 P2 |

## Mapa por Agente do Squad

| Agente | Absorção | Mudança necessária |
|---|---|---|
| `slide-chief` | Presenton API/MCP + DeckSpec workspace | Passa a orquestrar run ID e artifacts, não só handoff. |
| `content-architect` | PPTAgent planner/research | Emite plano narrativo e reflection history. |
| `template-curator` | ppt-master template replication + Presenton template import | Importa PPTX e registra tokens/layouts. |
| `design-renderer` | ppt-master renderer + powerpoint-skill diagrams | Gera Native IR e chama renderer. |
| `visual-scout` | banana UX patterns + asset providers | Resolve assets e style references. |
| `qa-inspector` | PPTAgent PPTEval + editability QA | Consolida narrativa/design/editabilidade. |

## Mapa por Artifact

| Artifact atual | Futuro | Fonte |
|---|---|---|
| `briefing.normalized.json` | manter | slides-creator |
| `deck-manifest.json` | evoluir para `deck-spec.yaml` | slides-creator + PPTAgent |
| `qa-report.json` | expandir com PPTEval/editability | PPTAgent + ppt-master |
| `render request` | virar Native IR | ppt-master |
| `visual-generation-report.json` | integrar assets/style refs | banana-slides |
| `template-registry.yaml` | suportar import PPTX | ppt-master + Presenton |
| `deck-publication.json` | novo artifact para share links, permissões e analytics | Gamma benchmark + PostHog/Umami/Plausible |
| `editor-state.json` | novo estado block/card-based para edição web | BlockNote/Tiptap + Yjs |

## Decisão

O mapa reforça que a absorção é modular. Nenhum projeto externo substitui o squad; cada um cobre uma camada que hoje está parcial ou ausente.

BlockNote, Tiptap, ProseMirror, Yjs, Hocuspocus, PostHog, Umami, Plausible, Slidev e Marp não entram como “players principais” da matriz porque não são apps completos de criação de slides com IA. Eles entram como infraestrutura de produto para fechar gaps específicos contra Gamma.
