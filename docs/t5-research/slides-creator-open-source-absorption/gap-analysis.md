# Gap Analysis — Slides Creator vs Gamma-Level Stack

## Update 2026-05-18 — Pós Wave 3 Spike

Score 77.93 → **81.07**. Mudança nos gaps abaixo:

| Gap original | Status pós-spike | Evidência | Restante |
|---|---|---|---|
| PPTX nativo editável | **PARCIALMENTE FECHADO** | `packages/@sinkra/slides-renderer/src/pptx/render.ts` cobre text/shape/image/table/chart; 5 fixtures válidos score 100; editability inspector emite verdict PASS/CONCERNS/FAIL | Animações + ppt reopen manual review (SLS-W3-004) |
| API/MCP self-hosted | **PARCIALMENTE FECHADO** | 5 REST endpoints + 5 MCP tools + 5 CLI subcomandos compartilhando `@sinkra/slides-core`; OpenAPI 3.1; parity validator | Wiring real ollama/byok provider (SLS-W3-010), docker-compose pronto (SLS-W3-011) |
| Agentic planning/reflection | **PARCIALMENTE FECHADO** | `critique-report.yaml` + `planning-reflection.jsonl` materializados por run; Zod superRefine bloqueia forbidden verbs no LLM output | Wiring real PPTEval-equivalent multimodal (SLS-W3-017) |
| Prompt-to-edit por slide/região | **PARCIALMENTE FECHADO** | `editSlide()` com target {slide_id, region?, node_id?} + patch diff + applied:false; CLI/REST/MCP expõem | History reversível (SLS-W3-014), regenerate-only-region (SLS-W3-013) |
| Math/diagramas técnicos | INALTERADO | — | SLS-W3 não tocou — Wave 4 |
| Editor web e temas | INALTERADO | — | Wave 4 (UI fica fora do escopo Wave 3) |

Detalhes microdimensão por microdimensão em [wave-3-promotions.json](wave-3-promotions.json) e [wave-3-score-delta.md](wave-3-score-delta.md).

---

## Gaps P0 (estado original — para referência)

| Gap | Estado atual | Referência externa | Absorção necessária | Critério de aceite |
|---|---|---|---|---|
| PPTX nativo editável | Parcial; decisão e task existem, mas runtime maduro não | `ppt-master` | SVG/IR visual → DrawingML, template replication, validação de objetos editáveis | PPTX exportado abre com texto, shapes, imagens e gráficos editáveis, sem depender de screenshots por slide. |
| API/MCP self-hosted | Parcial/ausente como produto | Presenton | Serviço `slides-api`, endpoint generate/review/export e MCP | `npm run slides:generate` e MCP geram deck com mesmo contrato. |
| Agentic planning/reflection | Forte em governança, parcial em loop visual/reflexivo | PPTAgent | Planner/research/design reflection + PPTEval complementar | Cada deck possui `reflection_history` e QA antes/depois. |

## Gaps P1

| Gap | Estado atual | Referência externa | Absorção necessária | Critério de aceite |
|---|---|---|---|---|
| Prompt-to-edit por slide/região | Ausente | banana-slides | Comandos naturais com diff e aplicação controlada | Usuário edita slide específico por prompt, revisa diff e aplica. |
| Editor web e temas | Parcial fora do squad | presentation-ai + Presenton | Outline editor, temas, template picker e preview | DeckSpec renderiza no editor e exporta sem quebra. |
| Math/diagramas técnicos | Parcial | powerpoint-skill | OMML, Mermaid, Graphviz, TikZ e regras de fallback | Deck técnico com fórmulas e diagramas passa render QA. |

## Gaps P2

| Gap | Estado atual | Referência externa | Absorção necessária | Critério de aceite |
|---|---|---|---|---|
| Share links e analytics | Ausente | Gamma + presentation-ai | Presentation runtime, PostHog/Umami/Plausible | Link público com views por deck/slide. |
| Vídeo/narração | Parcial conceitual | ppt-master, banana-slides, PresentAgent-2 | TTS, presenter mode, MP4 opcional | Deck exporta vídeo com narração controlada. |
| Query→deep research→deck | Parcial via tech-research/squads | PresentAgent-2 | Pipeline de pesquisa para DeckSpec | Query gera relatório rastreável e deck com fontes. |

## Risco Principal

O maior risco é começar pelo editor visual antes de fechar o renderer editável e a API. Isso produziria uma casca bonita sem vantagem real contra Gamma.

## Estratégia de Fechamento

1. Fechar renderer e editabilidade.
2. Expor API/MCP.
3. Integrar planning/reflection.
4. Só então montar editor prompt-to-edit.
