# TODO — Slides Creator Open-Source Absorption, Ordenado por Cobertura

Este TODO transforma o bench em backlog técnico. A ordem segue impacto de cobertura: primeiro fechar o que mais aproxima a stack do padrão Gamma+SINKRA.

## P0 — Cobertura Crítica

| Ordem | Item | Fonte | Entrega | Aceite |
|---:|---|---|---|---|
| 1 | Criar `native-slide-ir.schema.json` | `ppt-master` + `slides-creator` | Schema de IR validável | 5 fixtures passam no validador. |
| 2 | Criar renderer PPTX nativo básico | `ppt-master` | `services/slides-renderer` | 10 slides com 80%+ objetos editáveis. |
| 3 | Criar `editability-report.json` | `ppt-master` | Relatório por slide/objeto | Relatório diferencia nativo vs raster. |
| 4 | Criar CLI `slides:generate` | Presenton + slide-deck-ai | comando local | Gera DeckSpec, PPTX, PDF e QA. |
| 5 | Criar API `POST /slides/generate` | Presenton | `services/slides-api` | API chama mesmo core da CLI. |
| 6 | Criar MCP `slides.generate/review/export` | Presenton + PPTAgent | MCP server | Tool gera artifacts rastreáveis. |
| 7 | Persistir `planning-reflection.jsonl` | PPTAgent | log de reflexão | QA failures geram decisões e reroute. |
| 8 | Adaptar rubricas PPTEval | PPTAgent | QA complementar | Conteúdo/design/coerência medidos. |
| 9 | Implementar provider registry | Presenton + slide-deck-ai | OpenAI/Gemini/Anthropic/Ollama/custom | Dummy/local roda sem API externa. |
| 10 | Criar workspace por deck | Presenton | `outputs/slides/{deck_id}` | Todo run tem input, specs, exports e logs. |

## P1 — Experiência e Robustez

| Ordem | Item | Fonte | Entrega | Aceite |
|---:|---|---|---|---|
| 11 | Outline editor mínimo | presentation-ai | UI ou TUI inicial | Usuário revisa outline antes de render. |
| 12 | Prompt-to-edit com diff | banana-slides + ppt-master | operação por slide/elemento | Diff aprovado altera DeckSpec. |
| 13 | Theme picker e import de PPTX | Presenton + presentation-ai + ppt-master | template registry | Template corporativo aplica cores/fontes. |
| 14 | OMML/math support | powerpoint-skill | math renderer | Fórmulas editáveis no PowerPoint. |
| 15 | Diagram engines | powerpoint-skill | Mermaid/Graphviz/TikZ | Diagramas determinísticos com fallback. |
| 16 | Visual QA screenshots | PPTAgent + powerpoint-skill | screenshot/PDF checks | Overflow e contraste críticos bloqueiam release. |

## P2 — Produto Completo

| Ordem | Item | Fonte | Entrega | Aceite |
|---:|---|---|---|---|
| 17 | Share links | Gamma + presentation-ai | web runtime | Deck abre em link público/privado. |
| 18 | Analytics | Gamma benchmark | events por deck/slide | Views e tempo por slide registrados. |
| 19 | Narração/TTS | ppt-master | áudio por slide | PPTX inclui notes/narração opcional. |
| 20 | Export MP4 | ppt-master + banana-slides | vídeo | MP4 com narração e slides. |
| 21 | Query→research→deck | PresentAgent-2 | pipeline de pesquisa | Fonte antes de deck, não deck sem evidência. |
| 22 | Q&A sobre apresentação | PresentAgent-2 | interaction mode | Respostas citam deck/fonte. |

## Itens Bloqueados por Política

| Item | Motivo | Próximo passo |
|---|---|---|
| Reuso de código banana-slides | AGPL-3.0 | ADR/licença antes de qualquer cópia. |
| Reuso de código PresentAgent-2 | Licença não verificada | Confirmar licença. |
| Fork único de qualquer projeto | Perde governança SINKRA | Seguir absorção modular. |

## Ordem de Execução Recomendada

1. Renderer editável.
2. CLI/API/MCP.
3. Planning/reflection.
4. QA editabilidade/visual.
5. UX prompt-to-edit.
6. Sharing/analytics/vídeo.
