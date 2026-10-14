# DeepResearcher (GAIR-NLP) — Inventory

**Repo:** https://github.com/GAIR-NLP/DeepResearcher
**Local clone:** `../bench/DeepResearcher/`
**License:** Apache-2.0 (LICENSE + Notice.txt confirmed)
**Métricas (clone scan 2026-05-18):** **264 .py files**
**Categoria:** Modelo Treinado End-to-End via RL
**Paper:** arXiv:2504.03160 (2025)

## Identidade

"The first comprehensive framework for end-to-end training of LLM-based deep research agents through scaling reinforcement learning (RL) in real-world environments with authentic web search interactions."

## Estrutura do Repo (top-level)

```
data/                      ← Training datasets
docker/                    ← Docker for training
docs/
evaluate/                  ← Evaluation harness
evaluate.sh                ← Eval entry point
examples/                  ← Usage examples
images/                    ← Paper figures
LICENSE                    ← Apache-2.0
Notice.txt                 ← Apache notice
patches/                   ← Library patches
```

## Arquitetura

- **Modelo:** Qwen2.5-7B-Instruct base
- **Training:** GRPO (Group Relative Policy Optimization)
- **Environment:** interação direta com search engines reais durante training
- **Output model:** DeepResearcher-7B (HuggingFace)
- **Self-contained:** modelo treinado independe de API externa em runtime

## Emergent Cognitive Behaviors (do paper)

Comportamentos emergentes do RL end-to-end (não programados):
1. **Planning** — formula planos antes de buscar
2. **Cross-validation** — valida informação entre múltiplas fontes
3. **Self-reflection** — re-direciona pesquisa ao detectar erro
4. **Honest abstention** — admite quando não encontra resposta

## Performance

**+28.9 pts sobre baselines de prompt engineering.** Modelo de apenas 7B parameters.

## LLM Backend

**Próprio:** DeepResearcher-7B (HuggingFace, Apache-2.0).
- Rodável em hardware modesto (single GPU 24GB)
- Self-contained (não API externa)

## Diferenciais (vs AIOX)

1. **Modelo pequeno (7B) acessível** — roda em hardware comum (AIOX usa LLMs externos via API)
2. **+28.9 pts vs prompting** — prova superioridade de RL training vs prompt eng (AIOX é puro prompting)
3. **Emergent behaviors** — comportamentos não programados (AIOX programado fase-a-fase)
4. **Apache-2.0** — friendly
5. **264 .py files** + infra de training/eval — codebase robusto
6. **Cognitive analysis paper** — research formal documentado
7. **Standalone runtime** — sem dependência de API externa (custo zero variável)

## Limitações

- 7B é limitado em raciocínio complexo vs modelos maiores
- Treinado em ambiente específico (gaps em domínios novos)
- Menos flexível que frameworks baseados em script
- Sem feature de workflow customizável (AIOX permite tunar phases)
- Sem governance gates (COVERAGE/CITATION explícitos)

## Lessons para AIOX

DeepResearcher prova que **modelos pequenos treinados E2E batem agentes baseados em prompting** em research tasks. AIOX poderia:
- Fine-tune um modelo 7B com trajetórias do CITATION_GATE/COVERAGE_GATE
- Usar DeepResearcher-7B como backend opcional pra users com GPU
- Documentar emergent behaviors observed nos próprios learning logs

## Sources

- `../bench/DeepResearcher/README.md`
- `../bench/DeepResearcher/LICENSE` (Apache-2.0)
- `../bench/DeepResearcher/Notice.txt`
- arXiv paper 2504.03160
- HF model card DeepResearcher-7B
- File count via `find . -name "*.py"`
- Original research dossier 2026-05-16
