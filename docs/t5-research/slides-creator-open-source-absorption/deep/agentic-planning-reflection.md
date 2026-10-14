# Deep Dive — Agentic Planning e Reflection

## Tese

Gamma ganha em velocidade e UX. SINKRA deve ganhar em qualidade de raciocínio. Para isso, o fluxo precisa combinar o núcleo narrativo do `slides-creator` com loops de planejamento/reflexão inspirados no PPTAgent.

## Estado Atual

O `slides-creator` já tem:

- briefing contract;
- Pyramid/SCQA;
- action titles;
- validação vertical;
- QA não negociável;
- handoffs entre agentes.

Evidências:

- `.agents/skills/slides-chief/SKILL.md`
- `squads/slides-creator/tasks/build-pyramid.md`
- `squads/slides-creator/tasks/apply-scqa.md`
- `squads/slides-creator/tasks/validate-pyramid.md`
- `squads/slides-creator/tasks/review-presentation.md`

## Gap

O que ainda falta é uma camada persistente de reflexão:

- registro de hipóteses;
- crítica de design;
- avaliação before/after;
- decisão por slide;
- roteamento automático após falha.

## Referência Externa

PPTAgent traz padrões úteis:

- Planner;
- Research agent;
- Design agent;
- reflection;
- avaliação de conteúdo/design/coerência.

## Modelo Proposto

```text
Briefing Contract
  -> Narrative Planner
  -> Evidence Planner
  -> Design Planner
  -> Draft DeckSpec
  -> Critique Pass
  -> Revision Pass
  -> Final DeckSpec
  -> Render
  -> QA
```

## Artifact Novo

`planning-reflection.jsonl`:

```json
{"phase":"narrative","slide":"s03","claim":"headline weak","evidence":"action title lacks verb","decision":"rewrite headline"}
{"phase":"design","slide":"s05","claim":"chart too dense","evidence":"7 categories for one slide","decision":"split into 2 slides"}
```

## Rubricas

| Dimensão | Fonte | Gate |
|---|---|---|
| Conteúdo | slides-creator + PPTAgent | Claims têm fonte e síntese clara. |
| Design | PPTAgent + qa-inspector | Hierarquia, contraste, legibilidade. |
| Coerência | slides-creator | Cada slide avança a tese. |
| GAD | slides-creator | Governança, acurácia, dados. |
| Editabilidade | ppt-master-inspired renderer | Objetos nativos suficientes. |

## Roteamento Após Falha

| Falha | Rota |
|---|---|
| Action title fraco | `content-architect` |
| Pirâmide quebra | `content-architect` + `qa-inspector` |
| Visual confuso | `design-renderer` |
| Asset ruim | `visual-scout` |
| Export não editável | `slides-renderer` |
| Fonte ausente | `content-architect` |

## Critérios de Aceite

- Todo deck tem `narrative-plan.yaml`.
- Todo deck tem `planning-reflection.jsonl`.
- QA falha gera rota específica, não "tente de novo".
- Uma revisão melhora pelo menos uma dimensão sem degradar outra crítica.
