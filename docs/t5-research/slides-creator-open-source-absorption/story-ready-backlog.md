# Story-Ready Backlog — slide creator skill stack

Backlog derivado de `TODO-coverage.md`, pronto para virar stories formais.

## Epic

**SLS-OS: Absorção Open-Source para Slides Creator**

Objetivo: entregar geração de decks com IA via CLI/API/MCP, PPTX editável, QA rastreável e DeckSpec versionável.

## Stories P0

### SLS-OS-001 — Native Slide IR Schema

**Como** `design-renderer`,  
**quero** um schema `native-slide-ir.v1`,  
**para** converter DeckSpec em objetos renderizáveis de forma validável.

AC:

- schema cobre text, shape, image, table, chart e diagram;
- IDs estáveis por slide/elemento;
- valida coordenadas, bounds e fallback raster;
- fixtures passam em validador local.

### SLS-OS-002 — DeckSpec to Native IR

AC:

- converte 5 fixtures de DeckSpec;
- preserva action titles;
- marca unsupported features;
- gera `native-slide-ir.json`.

### SLS-OS-003 — Editable PPTX Renderer MVP

AC:

- exporta `.pptx`;
- títulos e textos principais editáveis;
- shapes básicos editáveis;
- imagens inseridas como objetos;
- PowerPoint abre sem repair.

### SLS-OS-004 — Editability Report

AC:

- gera `editability-report.json`;
- informa nativo vs raster por slide;
- bloqueia release se action title for rasterizado;
- score geral >= 80 para fixture MVP.

### SLS-OS-005 — Slides Generate CLI

AC:

- `npm run slides:generate` gera DeckSpec, PPTX, PDF e QA;
- suporta provider dummy/local para smoke;
- escreve workspace por deck;
- falhas retornam erro estruturado.

### SLS-OS-006 — Slides API

AC:

- `POST /slides/generate`;
- `POST /slides/review`;
- `POST /slides/export`;
- API chama mesmo core da CLI;
- resposta inclui artifact paths.

### SLS-OS-007 — Slides MCP

AC:

- tools `slides.generate`, `slides.review`, `slides.export`;
- sem vazamento de secrets;
- respeita workspace;
- bloqueia release com killer items.

### SLS-OS-008 — Planning Reflection

AC:

- gera `planning-reflection.jsonl`;
- cada QA failure tem rota;
- reflection não muda fatos sem fonte;
- before/after registrado.

## Stories P1

- SLS-OS-009 — Outline editor mínimo.
- SLS-OS-010 — Prompt-to-edit com diff.
- SLS-OS-011 — Template import de PPTX.
- SLS-OS-012 — Math/OMML support.
- SLS-OS-013 — Mermaid/Graphviz/TikZ diagrams.
- SLS-OS-014 — Visual QA screenshots.

## Stories P2

- SLS-OS-015 — Share links.
- SLS-OS-016 — Analytics por deck/slide.
- SLS-OS-017 — TTS/narração.
- SLS-OS-018 — Export MP4.
- SLS-OS-019 — Query→research→deck.
- SLS-OS-020 — Q&A sobre apresentação.
