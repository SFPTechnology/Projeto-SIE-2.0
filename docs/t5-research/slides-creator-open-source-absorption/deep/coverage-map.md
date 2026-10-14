# Coverage Map — Ordenado por Cobertura Crítica

Este mapa organiza as capacidades por importância para chegar ao padrão Gamma+SINKRA. A coluna "cobertura atual" representa o estado do nosso `slides-creator`; a coluna "cobertura composta" representa o alvo após absorver os projetos recomendados.

| Ordem | Capacidade | Cobertura atual | Cobertura composta alvo | Fonte principal | Status |
|---:|---|---:|---:|---|---|
| 1 | PPTX nativo editável | 55 | 94 | `ppt-master` | P0 |
| 2 | API/MCP self-hosted | 35 | 92 | Presenton | P0 |
| 3 | Planejamento/reflexão agentic | 78 | 93 | PPTAgent + slides-creator | P0 |
| 4 | Governança narrativa e QA | 95 | 97 | slides-creator + PPTAgent | Core |
| 5 | Prompt-to-edit UX | 20 | 86 | banana-slides + presentation-ai | P1 |
| 6 | Editor web e temas | 35 | 88 | presentation-ai + Presenton | P1 |
| 7 | Privacidade/local/BYOK | 70 | 94 | Presenton + ppt-master + slide-deck-ai | P0 |
| 8 | Parsing de fontes | 70 | 90 | Presenton + PPTAgent + ppt-master | P0 |
| 9 | Math/diagramas acadêmicos | 45 | 90 | powerpoint-skill | P1 |
| 10 | Share/publicação/analytics | 25 | 78 | presentation-ai + produto próprio | P2 |
| 11 | Vídeo/narração/multimodal | 35 | 82 | ppt-master + banana-slides + PresentAgent-2 | P2 |
| 12 | Licença/absorção segura | 100 | 88 | política interna + licenças OSS | Core |

## Cut Line

Para dizer que estamos "à altura do Gamma" no eixo produto mínimo:

- cobertura composta P0 >= 90;
- export PPTX/PDF funcional;
- edição real no PowerPoint validada;
- API/MCP disponível;
- QA narrativo e visual rastreável.

Para dizer que superamos Gamma em B2B:

- fontes rastreadas;
- modo local/BYOK;
- deck-spec versionável;
- gates SINKRA;
- templates corporativos;
- editabilidade nativa.
