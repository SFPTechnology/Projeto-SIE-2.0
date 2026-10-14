# Jina node-DeepResearch — Inventory

**Repo:** https://github.com/jina-ai/node-DeepResearch
**Local clone:** `../bench/node-DeepResearch/`
**License:** Jina AI proprietary (Copyright 2020-2025 Jina AI Limited. All rights reserved.) — **NÃO open-source no sentido OSI**
**Métricas (clone scan 2026-05-18):** **57 .ts files, 0 .py**
**Categoria:** Single-Agent Loop em TypeScript/Node.js
**Stable API:** https://jina.ai/deepsearch
**Official UI:** https://search.jina.ai/

## Identidade

"Keep searching, reading webpages, reasoning until an answer is found (or the token budget is exceeded). Useful for deeply investigating a query."

> **IMPORTANT (from README):** Unlike OpenAI/Gemini/Perplexity's "Deep Research", we focus solely on **finding the right answers via our iterative process**. We don't optimize for long-form articles, that's a **completely different problem** – so if you need quick, concise answers from deep search, you're in the right place. If you're looking for AI-generated long reports like OpenAI/Gemini/Perplexity does, this isn't for you.

## Estrutura do Repo (top-level)

```
config.json
docker-compose.yml
Dockerfile
jest.config.js
jest.setup.js                ← Testing infra
jina-ai/                     ← Jina-specific
package.json
package-lock.json
README.md
LICENSE                      ← Jina proprietary
```

## Arquitetura

- **Single-agent loop em TypeScript (Node.js)**
- Actions: `search`, `visit`, `reflect`, `answer`
- **JSON Schema enforcement** para structured output
- **Budget monitoring** — para quando excede token budget
- Loop until: resposta encontrada OR budget exceeded

```mermaid
flowchart LR
    subgraph Loop["until budget exceed"]
        Search → Read → Reflect → Answer
    end
```

## LLM Backend

- Gemini (gemini-2.0-flash default)
- OpenAI
- LocalLLM
- **Requer modelos com structured output / JSON Schema**

## Diferenciais (vs AIOX)

1. **TypeScript pure** — fit perfeito pra apps Next.js (AIOX é Python+MD)
2. **Jina Reader integrado** — engine de web reading especializada
3. **Single-loop minimalista** — 4 actions (search/visit/reflect/answer) vs AIOX 17 atoms
4. **Docker-ready** — Dockerfile + docker-compose
5. **Stable API hospedada** — produção-grade SaaS Jina (AIOX é self-hosted)
6. **Jest** — JS-native testing
7. **Honestidade de escopo** — README explicita que NÃO é pra long reports (anti-feature creep)

## Limitações

- **Proprietary license** — não OSI open-source, source-available
- TypeScript-only (Python ecosystem fora)
- Sem multi-agent
- Sem memória persistente
- Foco em Q&A curto, não em deep reports (não substitui AIOX/GPT-Researcher para reports longos)
- 0 .py files = sem fit em monorepo Python

## Lessons para AIOX

Jina ensina **honestidade de escopo**: definir explicitamente o que NÃO é o produto. AIOX poderia:
- Documentar tipos de research que /tech-research NÃO faz (Q&A curto)
- Considerar `/quick-answer` skill irmã para o caso curto
- Adicionar `budget_monitoring` ao COVERAGE_GATE (parar antes de exceed)

## Sources

- `../bench/node-DeepResearch/README.md`
- `../bench/node-DeepResearch/LICENSE` (Jina proprietary)
- `../bench/node-DeepResearch/package.json`
- File count via `find . -name "*.ts"`
- Jina blog: https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch
- Original research dossier 2026-05-16
