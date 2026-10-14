# Tongyi DeepResearch (Alibaba-NLP) — Inventory

**Repo:** https://github.com/Alibaba-NLP/DeepResearch
**Local clone:** `../bench/Alibaba-DeepResearch/`
**License:** Apache-2.0
**Métricas (clone scan 2026-05-18):** **174 .py files**
**Categoria:** Pipeline + Modelo Próprio (Tongyi-DeepResearch-30B-A3B)
**Paper:** arXiv:2510.24701
**Modelo:** Alibaba-NLP/Tongyi-DeepResearch-30B-A3B (HuggingFace + ModelScope)
**Conferences:** WebWalker (ACL 2025), WebDancer (NeurIPS 2025), WebSailor (associated)

## Identidade

"Leading open-source deep research agent do ecossistema Alibaba." Backed by **Alibaba** com publications em top conferences. Tech_Report.pdf incluído no repo.

## Estrutura do Repo (top-level)

```
Agent/                     ← Agent orchestration
WebAgent/                  ← Web browsing agent specialization
inference/                 ← Inference scripts
evaluation/                ← Eval harness
assets/                    ← Logos
FAQ.md
Tech_Report.pdf            ← Technical report
requirements.txt
LICENSE                    ← Apache-2.0
README.md
```

## Arquitetura

- Pipeline de pesquisa web com modelos especializados para navegação e extração
- **WebAgent** dedicado para browsing
- **Agent** core para reasoning
- Integração com ecossistema Qwen (Alibaba LLMs)
- Inference + Evaluation infrastructure separados

## LLM Backend

**Modelo próprio:** Tongyi-DeepResearch-30B-A3B
- HuggingFace: https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B
- ModelScope (Alibaba's HF equivalent)
- Same arch class as OpenResearcher (30B-A3B MoE)

## Conferences / Academic Track

Múltiplos papers associados em top venues:
- **WebWalker** — ACL 2025
- **WebDancer** — NeurIPS 2025
- **WebSailor** — published
- **Tongyi DeepResearch** — arXiv:2510.24701

## Diferenciais (vs AIOX)

1. **Backed by Alibaba** — recursos massivos + sustentabilidade
2. **Modelo próprio 30B-A3B** — autonomia de infra (AIOX usa LLMs externos)
3. **Multiple top conference papers** — ACL/NeurIPS validation acadêmica
4. **Specialized WebAgent** — agent dedicado para browsing (AIOX usa skill genérica)
5. **ModelScope + HF distribuição dual** — China + ocidente
6. **Tech_Report.pdf no repo** — academic transparency (AIOX docs em MD)
7. **Apache-2.0**
8. **Qwen ecosystem** — pode usar modelos Alibaba completos (Qwen3, Qwen-Max etc.)

## Limitações

- Documentação **parcialmente em chinês** (WeChat link, ModelScope)
- Ecossistema Alibaba-centric (Qwen lock-in moderado)
- Sem app frontend integrado (research-only)
- Sem workflow PT-BR (China-first)
- Setup pesado (30B model + infra)

## Lessons para AIOX

Tongyi mostra que **publicar em top venues amplifica credibilidade** dramaticamente. AIOX poderia:
- Publicar **Tech_Report.pdf** equivalente em docs/architecture/
- Submeter paper sobre **COVERAGE_GATE + CITATION_GATE** como metodologia
- Posicionar **research-chief** como specialized agent equivalent ao WebAgent
- Documentar **emergent behaviors** observados nos learning logs

## Sources

- `../bench/Alibaba-DeepResearch/README.md`
- `../bench/Alibaba-DeepResearch/LICENSE` (Apache-2.0)
- `../bench/Alibaba-DeepResearch/Tech_Report.pdf`
- HF model card Tongyi-DeepResearch-30B-A3B
- Blog: https://tongyi-agent.github.io/blog/introducing-tongyi-deep-research/
- arXiv paper 2510.24701
- File count via `find . -name "*.py"`
- Original research dossier 2026-05-16
