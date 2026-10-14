# Deep Dive — API/MCP Runtime

## Tese

O `slides-creator` hoje é forte como squad/skill, mas ainda não é runtime. Para competir com Gamma e operar dentro do Hub, ele precisa ser uma capacidade invocável por CLI, API e MCP.

## Estado Atual SINKRA

Evidências:

- `.agents/skills/slides-chief/SKILL.md`
- `squads/slides-creator/workflows/generate-presentation.yaml`
- `squads/slides-creator/config.yaml`

O fluxo existe como orquestração:

```text
briefing -> plan -> content -> render -> ds -> QA -> release
```

O gap é transformar esse fluxo em serviço idempotente, observável e integrável.

## Referência Externa

Presenton é a referência P0:

- Docker/self-hosted;
- FastAPI + Next.js;
- API de geração;
- MCP;
- BYOK;
- Ollama;
- providers custom/OpenAI-compatible.

## API Recomendada

### `POST /slides/generate`

Entrada:

```json
{
  "input": {
    "type": "prompt|document|url|youtube",
    "content": "..."
  },
  "options": {
    "language": "pt-BR",
    "slides": 10,
    "style": "executive",
    "template": "sinkra-default",
    "exports": ["pptx", "pdf"]
  }
}
```

Saída:

```json
{
  "deck_id": "deck_20260517_001",
  "status": "queued|running|completed|failed",
  "artifacts": {
    "deck_spec": ".../deck-spec.yaml",
    "pptx": ".../deck.pptx",
    "pdf": ".../deck.pdf",
    "qa_report": ".../qa-report.json"
  }
}
```

### `POST /slides/review`

Reavalia deck existente e retorna gaps por slide.

### `POST /slides/export`

Exporta `deck_spec` existente para PPTX/PDF/web.

## MCP Tools

| Tool | Entrada | Saída |
|---|---|---|
| `slides.generate` | briefing/prompt/documento | deck_id + artifacts |
| `slides.plan` | briefing normalizado | narrative_plan + deck_spec draft |
| `slides.review` | deck_id ou deck_spec | qa_report |
| `slides.export` | deck_id + formato | arquivo exportado |
| `slides.import_template` | PPTX referência | template_id |

## CLI First

Comandos mínimos:

```bash
npm run slides:generate -- --input briefing.md --template sinkra-default --export pptx,pdf
npm run slides:review -- --deck outputs/slides/deck_001
npm run slides:export -- --deck-spec deck-spec.yaml --format pptx
```

## Workspace por Deck

```text
outputs/slides/{deck_id}/
  input/
  briefing.normalized.json
  narrative-plan.yaml
  deck-spec.yaml
  slide-specs/
  render/
  exports/
  qa-report.json
  editability-report.json
  run-log.jsonl
```

## Provider Registry

Absorver de Presenton/slide-deck-ai:

- `openai`;
- `gemini`;
- `anthropic`;
- `azure-openai`;
- `ollama`;
- `openai-compatible`;
- `local-dummy` para testes.

## Critérios de Aceite

- CLI, API e MCP chamam o mesmo core.
- Run é idempotente por `deck_id`.
- Cada artifact é rastreável.
- Modo Ollama/local roda smoke test sem API externa.
- Falha retorna erro estruturado, não arquivo parcial silencioso.
