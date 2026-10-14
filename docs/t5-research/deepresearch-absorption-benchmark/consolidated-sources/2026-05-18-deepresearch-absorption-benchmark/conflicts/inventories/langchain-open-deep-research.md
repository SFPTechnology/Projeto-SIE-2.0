# LangChain Open Deep Research — Inventory

**Repo:** https://github.com/langchain-ai/open_deep_research
**Local clone:** `../bench/langchain-open-deep-research/`
**License:** MIT (confirmed `LICENSE`)
**Métricas (clone scan 2026-05-18):** 22 .py files (compact)
**Categoria:** Single-Agent Loop (Search-Read-Reason)
**Build tool:** uv (`uv.lock` present)

## Identidade

"A simple, configurable, fully open source deep research agent that works across many model providers, search tools, and MCP servers." **#6 no Deep Research Bench Leaderboard** (overall score 0.4344, ago/2025). Reference implementation da LangChain.

## Estrutura do Repo

```
CLAUDE.md                  ← Claude Code instructions (!)
src/                       ← Core implementation
tests/                     ← Test suite
examples/                  ← Usage examples
langgraph.json             ← LangGraph deployment config
pyproject.toml
uv.lock                    ← uv lockfile
README.md
LICENSE
```

## Arquitetura

- **Single-agent loop** com LangGraph
- Phases: configurable search → compression → report writing
- Roda via `langgraph dev` (LangGraph Studio UI)

## LLM Backend

Qualquer modelo (OpenAI GPT-4.1 default). Tested com GPT-5 (ago/2025).

## Diferenciais (vs AIOX)

1. **#6 Deep Research Bench score** — leaderboard público (AIOX não testado)
2. **MCP-native** — supports custom MCP servers nativamente
3. **uv-based** — modern Python tooling (AIOX usa stdlib Python)
4. **LangGraph Studio UI** — visual workflow inspection nativo
5. **22 .py files** — extremamente compacto (lições de simplicidade)
6. **CLAUDE.md** — instruções nativas pra Claude Code (mesma cultura AIOX)
7. **Course oficial** — academy.langchain.com tem curso completo
8. **Update cadence público** — release notes datados (jul/ago 2025)

## Limitações

- Performance inferior a modelos treinados end-to-end (OpenResearcher/DeepResearcher)
- Single-agent (sem paralelismo nativo)
- Sem memória persistente
- Sem Docker sandbox
- Depende do ecossistema LangChain (lock-in moderado)

## Lessons para AIOX (Simplicity Audit)

LangChain Open DR roda com 22 .py vs AIOX research squad com 129 .md tasks + tech-research skill com 13 phase YAMLs. **A simplicidade do código não compromete o benchmark score (0.4344, #6).** Vale auditar onde AIOX tem complexidade não-essencial.

## Sources

- `../bench/langchain-open-deep-research/README.md`
- `../bench/langchain-open-deep-research/LICENSE` (MIT)
- File count via `find . -name "*.py"`
- Deep Research Bench Leaderboard (HuggingFace Spaces)
- LangChain blog 2025-07-16
- Original research dossier 2026-05-16
