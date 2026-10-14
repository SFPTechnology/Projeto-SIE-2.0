# Absorption Roadmap — slide creator skill stack

## Arquitetura-Alvo

```text
Briefing / Documento / URL / YouTube
        |
        v
slides-chief
        |
        v
Narrative Core
  governing thought + pyramid + SCQA + action titles + APA
        |
        v
Agentic Planning Layer
  PPTAgent-style planner + research + design reflection
        |
        v
DeckSpec / SlideSpec
        |
        +--> Renderer A: PPT Master-style SVG -> DrawingML -> editable PPTX
        +--> Renderer B: Presenton-style HTML/Tailwind -> PPTX/PDF/API
        +--> Renderer C: Image mode fallback for pixel-perfect deck
        |
        v
Web Runtime
  BlockNote/Tiptap-style editor + preview + prompt-to-edit + share links + analytics
        |
        v
QA / Release
  PPTEval + GAD + visual QA + human gate
```

## Fase 0 — Bench Local Reprodutível

Objetivo: gerar outputs reais com os projetos externos antes de absorver.

Tarefas:

- Rodar `ppt-master` com um briefing SINKRA e validar PPTX editável.
- Rodar Presenton via Docker/API para prompt, documento e template.
- Rodar PPTAgent em modo simples para entender planner/outline/reflection.
- Rodar banana-slides apenas em ambiente isolado por risco AGPL.

Saída: `outputs/bench/slides-ai/{project}/` com PPTX/PDF/screenshots/notes.

## Fase 1 — Renderer Nativo Editável

Absorver de `ppt-master`:

- SVG como IR visual;
- SVG constraints compatíveis com DrawingML;
- conversão para shapes/text/charts nativos;
- template replication de `.pptx`;
- live preview + annotations;
- animation/narration como extensão.

Entregar:

- `squads/slides-creator/tasks/export-native-editable-pptx.md`
- worker `services/slides-renderer/svg-to-pptx`
- QA de editabilidade: abrir PPTX, extrair objetos, verificar texto editável.

## Fase 2 — API/MCP Self-Hosted

Absorver de Presenton:

- API de geração;
- MCP server;
- BYOK/providers;
- Ollama/local model mode;
- app_data/workspace per deck;
- edit path.

Entregar:

- `services/slides-api/`
- endpoint `POST /slides/generate`
- MCP `slides.generate`, `slides.review`, `slides.export`
- CLI `npm run slides:generate`

## Fase 3 — Agentic Planning e Reflection

Absorver de PPTAgent:

- Planner;
- Research agent;
- Design agent;
- reflection com screenshot/render state;
- PPTEval complementando nosso QA.

Entregar:

- tarefas novas ou extensões de `content-architect`/`qa-inspector`;
- `deck-spec.yaml` com `reflection_history`;
- `qa-report.json` com comparação before/after.

## Fase 4 — UX Editor e Prompt-to-Edit

Absorver padrões de banana-slides, presentation-ai e da pesquisa consolidada:

- outline editor;
- editor block/card-based inspirado em BlockNote/Tiptap, sem tratar esses editores como solução de slides pronta;
- seleção de região;
- edição verbal de slide específico;
- asset toolbox;
- tema/style templates;
- undo/diff antes de aplicar.

Entregar:

- web editor minimal;
- prompt-to-edit por slide;
- preview visual;
- persistência de versão.

## Fase 5 — Publicação, Analytics e Vídeo

Absorver ideias de Gamma/banana/PresentAgent-2:

- share links;
- analytics por view/deck/slide;
- PostHog/Umami/Plausible como candidatos open-source para instrumentação;
- Yjs/Hocuspocus como camada futura de colaboração realtime, depois de editor e export estabilizados;
- presentation mode;
- narração/TTS;
- export MP4.

Entregar:

- web presentation runtime;
- PostHog/Umami/Plausible;
- video export opcional.

## Sequência Recomendada

1. `ppt-master` primeiro, porque resolve o gap mais duro: PPTX realmente editável.
2. Presenton segundo, porque transforma o sistema em API/app self-hosted.
3. PPTAgent terceiro, porque melhora qualidade de planejamento.
4. banana/presentation-ai depois, porque UX sem engine sólida vira casca bonita.
5. BlockNote/Tiptap/Yjs/PostHog entram como infraestrutura de produto, não como players de geração de slides.
6. Slidev/Marp ficam como fallback técnico para markdown/web/PDF versionável, não como substitutos de PPTX editável.
