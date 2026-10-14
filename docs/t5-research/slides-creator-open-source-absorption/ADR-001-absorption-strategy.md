# ADR-001 — Absorção Modular em Vez de Fork Único

## Status

Proposto.

## Contexto

O objetivo é construir uma solução de criação de slides com IA comparável ao Gamma, mas mais forte em B2B: PPTX editável, fontes rastreáveis, execução local/BYOK, API/MCP e governança SINKRA.

Analisamos 8 projetos open-source:

- `ppt-master`;
- Presenton;
- PPTAgent;
- banana-slides;
- presentation-ai;
- powerpoint-skill;
- slide-deck-ai;
- PresentAgent-2.

Nenhum cobre sozinho todo o espaço.

## Decisão

Não forkear nenhum projeto como base única.

Construir **slide creator skill stack** com:

- `slides-creator` como núcleo narrativo e governado;
- renderer inspirado em `ppt-master`;
- API/MCP inspirados em Presenton;
- planning/reflection inspirado em PPTAgent;
- UX inspirada em banana-slides e presentation-ai;
- math/diagramas inspirados em powerpoint-skill.

## Consequências

### Positivas

- Mantém governança SINKRA.
- Evita lock-in arquitetural em projeto externo.
- Reduz risco AGPL.
- Permite MVP CLI/API antes de UI.
- Preserva diferenciação B2B.

### Negativas

- Exige integração própria.
- Aumenta trabalho inicial.
- Demanda contratos claros entre DeckSpec, Native IR, Renderer e QA.

## Guardrails

- CLI-first.
- QA não pode ser pulado.
- AGPL só como referência de UX até ADR jurídico.
- Renderer antes de editor.
- Todo claim P0 precisa de evidence ledger.
