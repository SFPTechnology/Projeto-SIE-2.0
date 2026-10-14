# Dependency Graph — Implementação

## Ordem Técnica

```text
native-slide-ir.schema
  -> deckspec-to-ir
  -> pptx-renderer-basic
  -> editability-report
  -> cli-generate
  -> api-generate
  -> mcp-generate
  -> planning-reflection
  -> qa-rubric-integration
  -> outline-editor
  -> prompt-to-edit
```

## Dependências por Entrega

| Entrega | Depende de | Bloqueia |
|---|---|---|
| `native-slide-ir.schema.json` | DeckSpec atual | Renderer |
| `deckspec-to-ir` | Native IR | Renderer, prompt-to-edit |
| `pptx-renderer-basic` | Native IR | Editability QA, exports |
| `editability-report.json` | Renderer | Release gate |
| `slides:generate` CLI | Renderer + QA | API/MCP |
| `POST /slides/generate` | CLI core | UI/editor |
| MCP tools | API/core | agent integrations |
| `planning-reflection.jsonl` | DeckSpec + QA | reroute automático |
| Outline editor | API + DeckSpec | prompt-to-edit |
| Prompt-to-edit | element IDs + diff model | editor avançado |

## Caminho Crítico

O caminho crítico é:

`Native IR -> Renderer -> Editability QA -> CLI -> API/MCP`

Qualquer trabalho de editor antes disso é secundário.
