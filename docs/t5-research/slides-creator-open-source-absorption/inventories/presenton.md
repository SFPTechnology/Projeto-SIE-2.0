# Inventory — Presenton

## Identidade

- **Repo:** `presenton/presenton`
- **Clone local:** `../bench/presenton`
- **Licença:** Apache-2.0
- **Prioridade:** P0
- **Papel na stack:** produto self-hosted, API, MCP, BYOK, Ollama/local e templates.

## Evidência Lida

- `../bench/presenton/README.md`
- `../bench/presenton/docker-compose.yml`
- `../bench/presenton/servers/fastapi`
- `../bench/presenton/servers/nextjs`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| API de geração | README documenta endpoint de geração com `export_as` PPTX/PDF. |
| MCP | Built-in MCP server para gerar apresentações por Model Context Protocol. |
| Self-hosted | Docker, app local, desktop/Electron e backend FastAPI. |
| Providers | OpenAI, Gemini, Vertex, Azure, Anthropic, Ollama e OpenAI-compatible/custom. |
| BYOK | Chaves próprias e opção de travar alteração de chaves. |
| Templates | Templates, temas e geração de template a partir de PowerPoint. |

## Limitações

- Não é especializado em narrativa consultiva.
- Não resolve sozinho o gap de editabilidade nativa avançada no nível `ppt-master`.
- O modelo de produto pode ser maior do que precisamos no MVP CLI-first.

## O Que Absorver

1. **Contrato de API:** `POST /slides/generate`, `POST /slides/review`, `POST /slides/export`.
2. **MCP server:** ferramentas `slides.generate`, `slides.review`, `slides.export`.
3. **Provider registry:** OpenAI/Gemini/Anthropic/Ollama/custom.
4. **Workspace por deck:** diretório isolado com inputs, DeckSpec, exports e QA.
5. **Template API:** upload/import de PPTX para theme/template registry.

## O Que Não Copiar Diretamente

- UI completa antes do renderer.
- Dependência rígida em HTML/Tailwind como único caminho de render.
- Modelo de cloud/desktop antes de estabilizar o contrato headless.

## Integração SINKRA Recomendada

```text
services/slides-api/
  routes/generate
  routes/review
  routes/export
  mcp/slides-server
  providers/*
  workspaces/{deck_id}/
```

## Critério de Aceite

- `npm run slides:generate -- --input briefing.md --export pptx,pdf` funciona.
- MCP gera o mesmo `deck-spec.yaml` que a CLI.
- Ollama/local funciona sem chave externa para smoke test.
- Cada run deixa auditoria: inputs, prompts, decisões, exports e QA.
