# API Contract — slide creator skill stack

## Objetivo

Definir a API mínima para transformar `slides-creator` em runtime invocável, mantendo CLI-first e compatibilidade futura com UI.

## Endpoints P0

### `POST /slides/generate`

Gera um deck a partir de prompt, documento, URL ou briefing normalizado.

```json
{
  "input": {
    "type": "prompt",
    "content": "Crie uma apresentação executiva sobre IA para slides",
    "attachments": []
  },
  "options": {
    "language": "pt-BR",
    "slide_count": 10,
    "template_id": "sinkra-default",
    "exports": ["pptx", "pdf"],
    "provider": "ollama",
    "model": "llama3.2"
  }
}
```

Resposta:

```json
{
  "deck_id": "deck_20260517_001",
  "status": "completed",
  "artifacts": {
    "briefing": "outputs/slides/deck_20260517_001/briefing.normalized.json",
    "deck_spec": "outputs/slides/deck_20260517_001/deck-spec.yaml",
    "pptx": "outputs/slides/deck_20260517_001/exports/deck.pptx",
    "pdf": "outputs/slides/deck_20260517_001/exports/deck.pdf",
    "qa_report": "outputs/slides/deck_20260517_001/qa-report.json",
    "editability_report": "outputs/slides/deck_20260517_001/editability-report.json"
  }
}
```

### `POST /slides/review`

Revisa deck existente.

```json
{
  "deck_id": "deck_20260517_001",
  "checks": ["narrative", "visual", "editability", "sources"]
}
```

### `POST /slides/export`

Exporta um `deck-spec.yaml`.

```json
{
  "deck_spec": "outputs/slides/deck_20260517_001/deck-spec.yaml",
  "formats": ["pptx", "pdf"]
}
```

### `POST /slides/templates/import`

Importa PPTX de referência.

```json
{
  "source_pptx": "inputs/templates/client-brand.pptx",
  "mode": "theme_and_layouts"
}
```

## Erros

| Código | Quando |
|---|---|
| `INVALID_BRIEFING` | briefing insuficiente ou contraditório |
| `UNSUPPORTED_INPUT` | tipo de entrada ainda não suportado |
| `PROVIDER_FAILED` | LLM/image provider falhou |
| `RENDER_FAILED` | renderer não gerou artifact |
| `QA_FAILED` | deck gerado, mas gate bloqueou release |
| `EXPORT_FAILED` | PPTX/PDF falhou |

## Regras

- API não pode pular QA.
- API e CLI devem chamar o mesmo core.
- Toda resposta deve trazer `deck_id`.
- Todo artifact deve estar em workspace isolado.
- Dados de negócio ficam dentro do workspace correto, nunca em cache global compartilhado.
