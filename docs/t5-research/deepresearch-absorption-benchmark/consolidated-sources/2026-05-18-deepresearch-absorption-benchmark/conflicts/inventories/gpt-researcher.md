# GPT-Researcher (Assaf Elovic) — Inventory

**Repo:** https://github.com/assafelovic/gpt-researcher
**Local clone:** `../bench/gpt-researcher/`
**License:** Apache-2.0 (confirmed via LICENSE 11357 bytes — standard Apache text)
**Métricas (clone scan 2026-05-18):** 191 .py files
**Categoria:** Framework Multi-Agente de Pesquisa
**Distribuição:** PyPI (`pip install gpt-researcher`), Docker, Claude Skill (skills.sh)

## Identidade

"The first open deep research agent designed for both web and local research on any given task." Inspirado em STORM (Stanford) e Plan-and-Solve papers. Produz relatórios detalhados, factuais, com citações.

## Arquitetura

**Multi-agente via LangGraph + AG2:**
- **Chief Editor** orquestra
- **Researcher** — coleta evidência
- **Editor** — síntese
- **Reviewer** — verificação
- **Publisher** — output em formato

Parallelized agent work para reduzir tempo total.

## LLM Backend

Qualquer provider (OpenAI, Anthropic, Google, local). Custo ~$0.08/run com `gpt-4o-mini`.

## Output Formats

- PDF
- DOCX
- HTML
- Markdown
- JSON (raw)

## Integrações

- **MCP Server** nativo (Claude Code integration)
- **LangSmith** observability
- **Claude Skill** publicada em skills.sh
- Docker Hub: `elestio/gpt-researcher`
- PyPI package
- Discord community ativa

## Diferenciais (vs AIOX)

1. **MCP Server nativo** — exposição via Model Context Protocol (AIOX não)
2. **Output PDF/DOCX/HTML** — formats diversos (AIOX produz só MD)
3. **PyPI distribution** — `pip install` standalone (AIOX requer hub clone)
4. **Apache-2.0** — friendly para enterprise + community
5. **LangSmith integration** — observability tracing built-in
6. **Claude Skill publicada** — install-from-marketplace pattern (AIOX skills são local)
7. **Multi-source scraping nativo** — redução de bias por design
8. **API REST + WebSocket** standalone — não depende de skill invocation

## Limitações

- Requer API keys externas (custo por run ~$0.5-1 com GPT-4)
- Dependência de web scraping (sites podem bloquear)
- Sem memória persistente cross-session
- Sem Docker sandbox de execução

## Sources

- `../bench/gpt-researcher/README.md`
- `../bench/gpt-researcher/LICENSE` (Apache-2.0, 11357 bytes)
- `../bench/gpt-researcher/pyproject.toml` (6280 bytes)
- File count via `find . -name "*.py"`
- skills.sh marketplace
- Original research dossier 2026-05-16
