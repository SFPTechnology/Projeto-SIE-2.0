# OpenResearcher (TIGER-AI-Lab) — Inventory

**Repo:** https://github.com/TIGER-AI-Lab/OpenResearcher
**Local clone:** `../bench/OpenResearcher/`
**License:** Apache-2.0 (modelo Apache-2.0 conforme HF + paper)
**Métricas (clone scan 2026-05-18):** **10 .py files** (paper-grade slim)
**Categoria:** Model+Pipeline (purpose-trained 30B-A3B MoE)
**Adoption:** NVIDIA Nemotron family

## Identidade

"Pipeline totalmente aberto para síntese de trajetórias de pesquisa de longo horizonte. Modelo 30B-A3B (MoE)." Paper arXiv:2603.20278. **Adopted by NVIDIA's Nemotron family of models.**

## Estrutura do Repo (top-level)

```
backend.py                 ← Backend service
browser.py                 ← Web browser primitives (search/open/find)
data_utils.py              ← Trajectory data utilities
deploy_agent.py            ← Deployment
eval.py                    ← Evaluation harness
pyproject.toml
run_agent.sh               ← Run script
scripts/                   ← Training/inference scripts
assets/                    ← Logos, paper figures
```

## Arquitetura

- **Offline trajectory synthesis** com corpus de ~11B tokens
- **3 browser primitives:** search, open, find (minimalist API)
- **Teacher model:** GPT-OSS-120B gera 97k+ trajetórias para training data
- **Student model:** OpenResearcher-30B-A3B (MoE) treinado nas trajetórias
- **Runtime independence:** modelo próprio, não depende de API externa

## LLM Backend

**Próprio model:** OpenResearcher-30B-A3B (HuggingFace).
- **NÃO depende de OpenAI/Anthropic em runtime**
- HF Model card: https://huggingface.co/OpenResearcher/OpenResearcher-30B-A3B
- HF Dataset card: https://huggingface.co/datasets/OpenResearcher/OpenResearcher-Dataset
- HF Eval Logs: público

## Benchmarks

**54.8% accuracy no BrowseComp-Plus** — supera:
- GPT-4.1
- Claude Opus 4
- Gemini 2.5 Pro
- DeepSeek-R1

## Diferenciais (vs AIOX)

1. **Purpose-trained model** — supera frontier models em research benchmarks (AIOX usa modelos genéricos)
2. **NVIDIA Nemotron adoption** — production endorsement (AIOX sem grande sponsor)
3. **Modelo + dataset + training recipe abertos** — full reproducibility (AIOX skill é open mas processo é stateful)
4. **Browser primitives minimalistas** — 3 ações (search/open/find) vs AIOX 13 phase YAMLs
5. **Public eval logs** — auditável (AIOX learning logs são internos)
6. **Demo HF Space + Gradio** — UX comprovada (AIOX app é local)
7. **Apache-2.0** — enterprise-friendly
8. **HF model card + paper arXiv** — academic credibility

## Limitações

- Requer hardware significativo para rodar 30B (não cabe em laptop)
- **Corpus offline** (pode ficar desatualizado — não é real-time search)
- 10 .py files = paper-grade, falta features enterprise (logging, multi-user, governance)
- Sem deep workflow chain (vs AIOX 7 molecules / 17 atoms)
- Sem CITATION_GATE / COVERAGE_GATE governance

## Lessons para AIOX

OpenResearcher prova que **o modelo treinado para research vence o agente baseado em prompt engineering**. Mesmo que AIOX não treine modelo próprio, vale considerar:
- Usar OpenResearcher-30B-A3B como **default backend** quando user tem GPU
- Adicionar **public eval logs** transparency
- Simplificar pipeline (3 primitives vs 17 atoms?)

## Sources

- `../bench/OpenResearcher/README.md`
- HF model card OpenResearcher-30B-A3B
- arXiv paper 2603.20278
- NVIDIA Nemotron family adoption banner
- File count via `find . -name "*.py"`
- Original research dossier 2026-05-16
