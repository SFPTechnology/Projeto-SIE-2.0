# Capability Matrix — O Que Absorver

| Capacidade | Dono externo mais forte | Já temos? | Ação recomendada |
|---|---|---|---|
| Narrativa consultiva | Nosso `slides-creator` | Sim, forte | Manter como núcleo. |
| QA narrativa/design | Nosso `qa-inspector` + PPTAgent PPTEval | Sim, forte | Absorver rubricas/reflection do PPTAgent. |
| PPTX nativo editável | `ppt-master` | Parcial | Absorver SVG→DrawingML, template replication, animation/narration pipeline. |
| App/API self-hosted | Presenton | Não | Criar serviço SINKRA Slides API inspirado em Presenton. |
| MCP para geração | Presenton + PPTAgent | Parcial | Expor MCP do nosso workflow. |
| UX prompt-to-edit | banana-slides | Não | Estudar padrões, não copiar código AGPL sem decisão. |
| Editor rich web | presentation-ai | Parcial fora do squad | Absorver outline/editor/theme patterns. |
| Query→deep research→video | PresentAgent-2 | Não | Roadmap futuro, não MVP. |
| CLI/Python API simples | slide-deck-ai | Não | Criar CLI mínima para smoke tests. |
| Math/diagrams acadêmicos | powerpoint-skill | Parcial | Absorver OMML, Mermaid/Graphviz/TikZ e hard rules. |
| Share links/analytics | Gamma benchmark, PostHog/Umami/Plausible | Não | Criar camada web depois do renderer. |

## Scoring de Absorção

| Projeto | Valor para nossa stack | Esforço de absorção | Risco | Prioridade |
|---|---:|---:|---:|---|
| ppt-master | 10 | 8 | 4 | P0 |
| Presenton | 9 | 7 | 3 | P0 |
| PPTAgent | 9 | 6 | 3 | P0 |
| banana-slides | 8 | 7 | 8 AGPL | P1 |
| presentation-ai | 7 | 6 | 4 | P1 |
| powerpoint-skill | 7 | 3 | 2 | P1 |
| slide-deck-ai | 5 | 3 | 2 | P2 |
| PresentAgent-2 | 6 | 9 | 6 | P2/Futuro |

## Decisão

P0 não é UI. P0 é:

1. render/PPTX nativo editável;
2. API/MCP self-hosted;
3. agentic planning/reflection;
4. integração com o workflow `slides-creator` existente.

