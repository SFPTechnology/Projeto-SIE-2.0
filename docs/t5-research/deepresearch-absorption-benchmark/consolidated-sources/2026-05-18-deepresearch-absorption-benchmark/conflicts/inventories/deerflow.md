# DeerFlow (ByteDance) — Inventory

**Repo:** https://github.com/bytedance/deer-flow
**Local clone:** `../bench/deer-flow/`
**License:** MIT (confirmed `LICENSE`)
**Métricas (clone scan 2026-05-18):** 474 .py + 138 .ts files
**Categoria:** Framework Multi-Agente de Pesquisa

## Identidade

SuperAgent harness open-source para pesquisa, código e criação. **#1 GitHub Trending fev/2026.** ~66k+ stars. DeerFlow 2.0 lançado 2026-02-27. ByteDance é o sponsor principal.

## Estrutura do Repo (top-level)

```
backend/                  ← Python orchestration core
frontend/                 ← UI (TypeScript/React)
skills/                   ← Progressive skill loading
docker/                   ← Docker sandboxing
docs/                     ← Full docs incl. 4 traduções (fr/ja/ru/zh)
config.example.yaml
extensions_config.example.json
deer-flow.code-workspace  ← VSCode workspace
scripts/                  ← Setup utilities
Install.md, README.md (+ 4 traduções)
```

## Arquitetura

- **Multi-agente** com lead orchestrator + sub-agentes especializados (max 3 por turno)
- **Docker sandboxes persistentes** para code execution
- **Memória TIAMAT** — cross-device sync com confidence scores
- **Progressive skill loading** — carrega skills dinâmicamente
- **BytePlus InfoQuest** — smart search integration

## LLM Backend

Model-agnostic via OpenAI-compatible API. Recomenda:
- Doubao-Seed-2.0-Code (ByteDance)
- DeepSeek v3.2
- Kimi 2.5
Também: GPT-4, Claude, Gemini, Ollama.

## Requisitos

- Python 3.11+
- Node.js 22+
- Docker
- Melhor performance com modelos 100k+ context

## Diferenciais (vs AIOX)

1. **Docker sandbox** — execução isolada de código durante research (AIOX não tem)
2. **TIAMAT memory** — persistência cross-device com confidence (AIOX não tem)
3. **Progressive skill loading** — dynamic capability injection (AIOX usa static skills)
4. **474 .py + 138 .ts** — codebase 3-4× maior que squad+skill AIOX
5. **Backend+Frontend integrados** — DeerFlow já tem UI nativa (AIOX tem app/research separado)
6. **MIT license** — adoção open-source vs AIOX Elastic License v2 no app

## Limitações (citadas)

- Requer Docker (não roda em ambiente air-gapped trivialmente)
- Ecossistema ByteDance-centric em tooling
- Python 3.11+ + Node.js 22+ (versions altas)
- Best results com modelos 100k+ context (custo $$)

## Sources

- `../bench/deer-flow/README.md`
- `../bench/deer-flow/LICENSE` (MIT, 1134 bytes)
- File count via `find . -name "*.py"`
- DeerFlow 2.0 launch (DEV Community, fev 2026)
- Original research dossier 2026-05-16
