# Deep Dive — Implementation Playbook

## Objetivo

Converter o benchmark em plano de execução story-driven, CLI-first e com gates.

## Epic Recomendada

**EPIC: slide creator skill stack — Open-Source Absorption P0**

Resultado: criar runtime inicial de slides com IA com `slides-creator` como núcleo, export PPTX nativo editável, API/MCP e planning/reflection.

## Waves

### Wave 0 — Baseline Reprodutível

Entregas:

- rodar pelo menos 3 projetos externos localmente: `ppt-master`, Presenton, PPTAgent;
- salvar outputs em `outputs/bench/slides-ai/{project}/`;
- documentar tempo, dependências, falhas e qualidade.

Critério de aceite:

- cada run tem comando, commit/hash, input e output.

### Wave 1 — DeckSpec + Native IR

Entregas:

- `native-slide-ir.schema.json`;
- conversor `DeckSpec -> Native IR`;
- fixtures de 5 slides;
- lint de elementos não suportados.

Critério de aceite:

- fixtures validam em CI local.

### Wave 2 — Renderer PPTX Editável

Entregas:

- `services/slides-renderer`;
- export PPTX com texto/shape/image/table básico;
- `editability-report.json`;
- PDF fallback.

Critério de aceite:

- 10-slide deck com 80%+ objetos principais editáveis.

### Wave 3 — API/MCP/CLI

Entregas:

- `services/slides-api`;
- CLI `npm run slides:generate`;
- MCP `slides.generate`, `slides.review`, `slides.export`;
- workspace por deck.

Critério de aceite:

- CLI/API/MCP produzem mesmo artifact contract.

### Wave 4 — Reflection + QA

Entregas:

- `planning-reflection.jsonl`;
- rubricas PPTEval adaptadas;
- QA de narrativa/design/editabilidade;
- reroute automático por falha.

Critério de aceite:

- QA falha aponta rota e slide-alvo.

### Wave 5 — Editor P1

Entregas:

- outline editor;
- slide preview;
- prompt-to-edit com diff;
- theme picker.

Critério de aceite:

- alteração visual altera DeckSpec e mantém histórico.

## Stories Sugeridas

| Story | Título | Wave |
|---|---|---|
| SLS-OS-001 | Definir `native-slide-ir.schema.json` | 1 |
| SLS-OS-002 | Converter `DeckSpec` para Native IR | 1 |
| SLS-OS-003 | Exportar PPTX editável básico | 2 |
| SLS-OS-004 | Criar `editability-report.json` | 2 |
| SLS-OS-005 | Expor CLI `slides:generate` | 3 |
| SLS-OS-006 | Expor API `POST /slides/generate` | 3 |
| SLS-OS-007 | Expor MCP `slides.generate` | 3 |
| SLS-OS-008 | Persistir `planning-reflection.jsonl` | 4 |
| SLS-OS-009 | Adaptar rubricas PPTAgent/PPTEval | 4 |
| SLS-OS-010 | Criar editor outline-first mínimo | 5 |

## Gate de Não Regressão

Nenhuma wave pode quebrar:

- briefing contract;
- Pyramid/SCQA;
- action titles;
- QA final;
- business isolation;
- CLI-first.
