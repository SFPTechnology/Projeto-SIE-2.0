# Local Deep Research (LDR) — Inventory

**Repo:** https://github.com/LearningCircuit/local-deep-research
**Local clone:** `../bench/local-deep-research/`
**License:** MIT (confirmed `LICENSE`)
**Métricas (clone scan 2026-05-18):** **2269 .py files** (massivo)
**Categoria:** Local-First / Privacy-First Agent
**Endorsement:** Vitalik Buterin (blog abril 2026)

## Identidade

"~95% accuracy no SimpleQA (ex: Qwen3.6-27B numa 3090). Suporta todos LLMs locais e cloud. 10+ search engines. Tudo local e encriptado."

**SimpleQA badge:** ~95% Accuracy

## Estrutura do Repo (top-level)

```
bearer.yml                 ← Security scanner config
changelog.d                ← Changelog fragments
community_benchmark_results ← Public bench data
cookiecutter-docker        ← Docker templates
docker-compose.yml
docker-compose.gpu.override.yml ← GPU support
docker-compose.unraid.yml  ← Unraid NAS support (!)
Dockerfile
docs/
CONTRIBUTING.md
```

## Arquitetura

- **Agente local** com 20+ research strategies
- **LangGraph Agent Strategy** para modo autônomo
- **SQLCipher** — database encryption nativa
- **SearXNG local** integration para search
- **10+ search engines**: arXiv, PubMed, Semantic Scholar, docs privados, mais

## LLM Backend

Qualquer:
- **Local:** Ollama, llama.cpp (best com Qwen3.6-27B)
- **Cloud:** Google, OpenAI, Anthropic

## Diferenciais (vs AIOX)

1. **100% local + encrypted** (SQLCipher) — air-gapped capable (AIOX não)
2. **10+ search engines nativos** incluindo arXiv/PubMed/Semantic Scholar (AIOX usa só WebSearch)
3. **Docker GPU + Unraid + pip** — multi-platform packaging (AIOX é git-clone-only)
4. **OpenSSF Scorecard + CodeQL + Semgrep** — security badges visíveis (AIOX não publica)
5. **community_benchmark_results/** — dataset público de benchmarks (AIOX privado)
6. **Vitalik Buterin endorsement** — credibilidade community privacy
7. **~95% SimpleQA** — score público (AIOX não testado)
8. **2269 .py files** — codebase massivo (~10× squad+skill AIOX)
9. **PyPI Downloads badge** — distribuição PyPI ativa

## Limitações

- Performance depende de hardware local (3090 GPU recomendada)
- UI web básica (não tão polida quanto AIOX/observatory)
- Requer SearXNG local para search engine
- Setup mais complexo (Docker + SearXNG + SQLCipher)

## Sources

- `../bench/local-deep-research/README.md`
- `../bench/local-deep-research/LICENSE` (MIT)
- File count via `find . -name "*.py"`
- Badges: SimpleQA, OpenSSF, CodeQL, Semgrep
- Vitalik blog: https://vitalik.eth.limo/general/2026/04/02/secure_llms.html
- Trendshift ranking
- Original research dossier 2026-05-16
