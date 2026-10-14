# MCP Contract — slide creator skill stack

## Objetivo

Expor a criação de slides como ferramentas MCP para agentes e IDEs sem acoplar a UI.

## Tools

### `slides.generate`

Entrada:

```json
{
  "prompt": "Crie uma apresentação de 10 slides sobre IA para criação de slides",
  "language": "pt-BR",
  "template_id": "sinkra-default",
  "exports": ["pptx", "pdf"]
}
```

Saída:

```json
{
  "deck_id": "deck_20260517_001",
  "deck_spec": "outputs/slides/deck_20260517_001/deck-spec.yaml",
  "exports": {
    "pptx": "outputs/slides/deck_20260517_001/exports/deck.pptx",
    "pdf": "outputs/slides/deck_20260517_001/exports/deck.pdf"
  },
  "qa_status": "passed"
}
```

### `slides.plan`

Gera apenas briefing normalizado, plano narrativo e DeckSpec draft.

### `slides.review`

Roda QA em deck existente.

### `slides.export`

Exporta DeckSpec para formatos suportados.

### `slides.import_template`

Importa PPTX de referência para template registry.

## Tool Boundaries

| Tool | Pode chamar LLM | Pode escrever arquivo | Pode liberar deck |
|---|---:|---:|---:|
| `slides.plan` | Sim | Sim | Não |
| `slides.generate` | Sim | Sim | Sim, se QA passar |
| `slides.review` | Opcional | Sim | Não |
| `slides.export` | Não | Sim | Não |
| `slides.import_template` | Não | Sim | Não |

## Segurança

- Nunca aceitar path fora do workspace permitido.
- Nunca expor chaves no retorno MCP.
- Registrar provider/model em `run-log.jsonl`.
- Bloquear release se `qa_report.killer_items > 0`.
