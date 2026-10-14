# Repo Notes — Inspection Findings

Notas técnicas levantadas durante o scan dos 9 clones.

## DeerFlow (`../bench/deer-flow/`)

- `backend/` Python + `frontend/` TypeScript = full-stack monorepo
- `skills/` separa progressive loading (potencial pattern para Sinkra)
- 4 traduções READMEs (fr/ja/ru/zh) — investimento i18n significativo
- `deer-flow.code-workspace` VSCode workspace pre-configured
- `extensions_config.example.json` plugin system
- Python 3.11+ + Node 22+ — versions altas

**Notable code:**
- `backend/orchestrator.py` (a verificar) — lead agent pattern
- `backend/memory/` (a verificar) — TIAMAT implementation
- `docker/` — multiple Dockerfile variants

## GPT-Researcher (`../bench/gpt-researcher/`)

- `pyproject.toml` 6280 bytes — extensa dependency tree
- LICENSE 11357 bytes = Apache-2.0 boilerplate
- README com badges: PyPI, Docker, Discord, Colab, Skill
- `multi_agents/` (a verificar) — LangGraph chief/researcher/editor/reviewer/publisher
- `mcp_server/` (a verificar) — MCP integration code

**Notable pattern:**
- Built-in MCP exposure
- Multi-output formats: PDF/DOCX/HTML
- LangSmith integration

## LangChain Open Deep Research (`../bench/langchain-open-deep-research/`)

- Apenas 22 .py files = mínimo viável
- `uv.lock` — modern Python tooling
- `CLAUDE.md` nativo
- `langgraph.json` deployment config
- `tests/` separate folder = test discipline
- README documenta release cadence pública (jul/ago 2025)

**Lesson:** simplicidade não compromete qualidade (#6 leaderboard).

## Local Deep Research (`../bench/local-deep-research/`)

- **2269 .py files** = massivo
- `community_benchmark_results/` = public bench data
- `cookiecutter-docker/` = Docker templates
- `docker-compose.gpu.override.yml` + `docker-compose.unraid.yml` = multi-deploy
- `bearer.yml` = secret scanner config
- `changelog.d/` = fragment-based changelog
- README badges: OpenSSF Scorecard + CodeQL + Semgrep + SQLCipher + SimpleQA

**Notable:**
- 10+ search engines (`src/local_deep_research/search_engines/`)
- SQLCipher encrypted DB pattern

## OpenResearcher (`../bench/OpenResearcher/`)

- Apenas 10 .py files = paper-grade slim
- `backend.py` + `browser.py` + `data_utils.py` + `deploy_agent.py` + `eval.py`
- Model em HuggingFace (não no repo)
- `run_agent.sh` entry point
- NVIDIA Nemotron banner

**Lesson:** purpose-trained model permite código minimal.

## DeepResearcher (`../bench/DeepResearcher/`)

- 264 .py files
- LICENSE Apache-2.0 + `Notice.txt`
- `data/` + `evaluate/` + `examples/` + `patches/`
- `images/` paper figures
- `evaluate.sh` benchmark runner

**Notable:**
- GRPO RL training code
- Patches dir = upstream library modifications

## Jina node-DeepResearch (`../bench/node-DeepResearch/`)

- 57 .ts files
- LICENSE proprietary (`Copyright 2020-2025 Jina AI Limited. All rights reserved.`)
- `jina-ai/` subfolder com Jina-specific code
- `docker-compose.yml` + `Dockerfile`
- `jest.config.js` + `jest.setup.js` = testing discipline
- README explicit scope: "NOT for long reports"

**Critical:** **Não absorber código.** Apenas inspirar arquitetura.

## AutoResearchClaw (`../bench/AutoResearchClaw/`)

- 363 .py files
- `researchclaw/` core
- `prompts.default.yaml` versioned prompts
- `config.researchclaw.example.yaml` production config
- `config_test_run.yaml` test config
- `docs/` + `image/` (framework_v2 diagram)
- MIT LICENSE
- README: "Chat an Idea. Get a Paper."
- 23 stages mencionado no README

**Notable patterns:**
- Versioned prompts as artifacts
- Dual config (test vs production)
- OpenClaw integration concept

## Tongyi DeepResearch (`../bench/Alibaba-DeepResearch/`)

- 174 .py files
- `Agent/` + `WebAgent/` (specialization!)
- `inference/` + `evaluation/`
- `requirements.txt` (pip-style, sem pyproject)
- `Tech_Report.pdf` = academic transparency
- `FAQ.md` = community-facing
- README + WeChat link + ModelScope link = China-first
- arXiv 2510.24701 + 3 conference papers

**Notable:**
- WebAgent dedicated subagent for browsing
- Tech Report PDF as commitment artifact

## Cross-Repo Patterns

| Pattern | Players | AIOX adoption |
|---|---|---|
| Docker compose multi-env | DeerFlow, LocalDR, Jina | ABSORB |
| MCP server | GPT-Researcher, LangChain ODR | ABSORB |
| Public eval logs | OpenResearcher, LocalDR, LangChain ODR | ABSORB |
| Apache-2.0 license | GPT-Researcher, OpenResearcher, DeepResearcher, Tongyi | CONSIDER (dual-license) |
| MIT license | DeerFlow, LangChain ODR, LocalDR, AutoResearchClaw | OK |
| Versioned prompts YAML | AutoResearchClaw | ABSORB |
| Tech Report PDF | Tongyi | ADAPT |
| Multi-lang READMEs | DeerFlow | DEFER |
| OpenSSF Scorecard | LocalDR | ABSORB |
| CLAUDE.md native | LangChain ODR | Already have |

## Anti-Patterns Encontrados

- **AGPLv3 surprises:** nenhum player usa AGPLv3 (todos MIT/Apache exceto Jina)
- **License header inconsistency:** OpenResearcher LICENSE file aparece vazio inicialmente (mas modelo HF é Apache-2.0)
- **DeerFlow heavy stack:** Python 3.11+ AND Node 22+ AND Docker = barreira de entrada
- **Jina proprietary trap:** README parece open-source mas LICENSE bloqueia

## Implications for AIOX

1. **Maturidade variável:** alguns players são research-grade (OpenResearcher = 10 files), outros production-grade (LocalDR = 2269 files). AIOX está entre os dois.
2. **Documentação multi-lingual investment:** DeerFlow tem 4 traduções, AIOX é PT-BR only. PT-BR é nosso moat.
3. **Sandbox is table-stakes:** 4 dos 9 players têm Docker sandbox. AIOX precisa ter.
4. **Public benchmark is becoming table-stakes:** 4 dos 9 têm score público.
5. **Memory layer is differentiator:** apenas 2 dos 9 têm cross-session memory bem feita.
