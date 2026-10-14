# Evidence Ledger

Este ledger liga as decisões do bench a evidências locais. Ele evita que a absorção vire opinião solta.

| Claim | Evidência | Confiança | Impacto |
|---|---|---|---|
| `ppt-master` é a melhor referência de PPTX nativo editável | `../bench/ppt-master/README.md`, `../bench/ppt-master/docs/templates-guide.md`, `../bench/ppt-master/skills/ppt-master/workflows/live-preview.md` | Alta | Define Wave 1 e Wave 2. |
| Presenton é a melhor referência para API/MCP/self-hosted | `../bench/presenton/README.md`, `../bench/presenton/docker-compose.yml`, `../bench/presenton/servers/fastapi`, `../bench/presenton/servers/nextjs` | Alta | Define `services/slides-api` e MCP. |
| PPTAgent é a melhor referência para planning/reflection | `../bench/PPTAgent/README.md`, `../bench/PPTAgent/pptagent/pptgen.py`, `../bench/PPTAgent/deeppresenter` | Alta | Define `planning-reflection.jsonl` e rubricas. |
| banana-slides é referência de UX, mas não de código | `../bench/banana-slides/README_EN.md`, licença AGPL-3.0 no inventário | Alta | Permite inspiração, bloqueia cópia direta. |
| presentation-ai é referência de editor web e outline-first | `../bench/presentation-ai/README.md`, `../bench/presentation-ai/apps/web/app`, `../bench/presentation-ai/apps/web/lib` | Alta | Define UX P1. |
| powerpoint-skill é referência de math/diagramas | `../bench/powerpoint-skill/README.md` | Alta | Define OMML, Mermaid, Graphviz e TikZ. |
| slide-deck-ai serve como baseline CLI/provider | `../bench/slide-deck-ai/README.md` | Média | Inspira smoke CLI, não renderer final. |
| PresentAgent-2 é referência futura para multimodal/vídeo/Q&A | `../bench/PresentAgent-2/README.md` | Média | Entra em P2, não MVP. |
| Nosso `slides-creator` deve seguir como cérebro | `squads/slides-creator/README.md`, `ARCHITECTURE.md`, `workflows/generate-presentation.yaml`, `.agents/skills/slides-chief/SKILL.md` | Alta | Mantém governança SINKRA. |
| O maior gap interno é runtime/editabilidade/API | `squads/slides-creator/data/editable-vs-image-pptx-decision.md`, `tasks/export-editable-pptx.md`, auditoria interna | Alta | Define ordem P0. |

## Regras de Evidência

- Claims P0 precisam de evidência local em clone ou arquivo interno.
- Claims de licença precisam citar inventário e, antes de implementação, confirmar arquivo de licença.
- Claims de qualidade só viram definitivos depois de run local reprodutível.
