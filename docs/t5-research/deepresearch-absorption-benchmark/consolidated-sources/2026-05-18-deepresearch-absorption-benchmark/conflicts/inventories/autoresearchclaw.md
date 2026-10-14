# AutoResearchClaw — Inventory

**Repo:** https://github.com/aiming-lab/AutoResearchClaw
**Local clone:** `../bench/AutoResearchClaw/`
**License:** MIT (confirmed `LICENSE`)
**Métricas (clone scan 2026-05-18):** **363 .py files**
**Categoria:** Pipeline Científica Autônoma (ideia → paper conference-ready)
**Tagline:** "Chat an Idea. Get a Paper. Autonomous, Collaborative & Self-Evolving."

## Identidade

"Just chat with **OpenClaw**: 'Research X' → done." Pipeline autônoma de **23 estágios** que transforma uma ideia em paper conference-ready.

## Estrutura do Repo (top-level)

```
researchclaw/              ← Core pipeline
docs/
image/                     ← Framework v2 diagram, logo
prompts.default.yaml       ← System prompts
config.test_run.yaml       ← Test config
config.researchclaw.example.yaml ← Production config example
CONTRIBUTING.md
pyproject.toml
LICENSE                    ← MIT
README.md
```

## Arquitetura

**3 subsistemas multi-agente:**
1. **CodeAgent** — implementação experimental
2. **BenchmarkAgent** — comparação com baselines
3. **FigureAgent** — geração de figuras paper-grade

**Infrastructure:**
- **Docker sandbox hardened** com network policy aware
- **4-round quality audit** — multi-pass quality gate
- **6 modos HITL** — Human-in-the-loop granular (full-auto até co-pilot)
- **23 stages** end-to-end (idea → paper)

## LLM Backend

Multiplos (configurável via YAML).

## Diferenciais (vs AIOX)

1. **23 stages end-to-end** — orchestration mais ambiciosa (AIOX tem 7 molecules)
2. **3 specialized agents** (Code+Benchmark+Figure) — division of concerns clara (AIOX tem 14 mas mais genéricos)
3. **Docker sandbox network-policy-aware** — security hardened (AIOX não sandboxa code execution)
4. **6 modos HITL granulares** — controle fino (AIOX tem --yolo / --interactive binário)
5. **4-round quality audit** — multi-pass review (AIOX tem 2 gates únicos, no multi-pass)
6. **prompts.default.yaml** — prompts versionados como artefato (AIOX prompts dispersos em phase YAMLs)
7. **FigureAgent** — gera figuras para paper (AIOX não tem capacidade visual)
8. **End-to-end paper output** — vai além de research, gera o artefato final (AIOX para no report)

## Limitações

- **Foco acadêmico** (não general-purpose research/CI)
- Complexidade de setup elevada (Docker hardened + config + 23 stages)
- Qualidade depende muito do modelo base
- Sem PT-BR vertical workflow
- Comunidade ainda pequena (emergente 2026)

## Lessons para AIOX

AutoResearchClaw mostra que **deeper pipelines viáveis quando bem orquestradas**. AIOX poderia:
- Adicionar **HITL granular** (6 modos vs binário)
- Adicionar **FigureAgent** equivalente — gerar visuals para reports
- Versionar prompts como **artefato YAML** consultável
- **Multi-round quality audit** (não só 1 gate)
- **Docker sandbox** para skills que executam code (apps/research /api/research/runs)

## Sources

- `../bench/AutoResearchClaw/README.md`
- `../bench/AutoResearchClaw/LICENSE` (MIT)
- `../bench/AutoResearchClaw/pyproject.toml`
- `../bench/AutoResearchClaw/prompts.default.yaml`
- File count via `find . -name "*.py"`
- Original research dossier 2026-05-16
