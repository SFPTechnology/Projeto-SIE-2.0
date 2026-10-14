# Segment Deep Analysis

> Análise profunda dos 4 segmentos (multi-agente / single-loop / model-trained / hybrid) com lessons para AIOX.

## Segmento 1 — Frameworks Multi-Agente

### Players: DeerFlow, GPT-Researcher, AutoResearchClaw, AIOX

**Padrão arquitetural comum:**
- Orchestrator + N sub-agents específicos
- Phase-based execution
- Output structured artifacts

**Onde diferem:**

| Aspecto | DeerFlow | GPT-Researcher | AutoResearchClaw | AIOX |
|---|---|---|---|---|
| Lead | Lead Agent | Chief Editor | Master Pipeline | research-chief |
| Sub-agents | Dynamic (max 3/turn) | Researcher/Editor/Reviewer/Publisher | CodeAgent + BenchmarkAgent + FigureAgent | 14 specialist personas |
| Sandbox | Docker persistent | None | Docker hardened | None |
| Memory | TIAMAT | None | None | Per-run learning log |
| Modes | General research | Reports | Paper end-to-end | 5+ modes unified |

**Lesson para AIOX:**
1. **Specialist sub-agents** (CodeAgent/BenchmarkAgent/FigureAgent) é padrão repetido — AIOX poderia ter `sandbox-agent`, `visualizer-agent`, `verifier-agent` dedicados
2. **TIAMAT memory** está fora do alcance hoje, mas memory layer básico (cross-run state.yaml) é absorvível em 1 sprint
3. **Inline persona-fidelity** preserva tokens mas perde paralelismo — modo opt-in `--parallel` seria win

## Segmento 2 — Single-Agent Loop

### Players: LangChain ODR, Jina node-DR, Local DR

**Padrão arquitetural comum:**
- Loop: search → read → reason → decide(continue|answer)
- Budget monitoring (tokens, time)
- Structured output enforcement

**Onde diferem:**

| Aspecto | LangChain ODR | Jina node-DR | Local DR |
|---|---|---|---|
| Lang | Python | TypeScript | Python |
| Budget | LangGraph | Token budget explicit | Time/token |
| Search engines | Configurable | Jina Reader | 10+ (arXiv/PubMed/etc) |
| Memory | None | None | SQLCipher encrypted |
| Scope honesty | "Performance on par with popular" | "NOT for long reports" | "~95% SimpleQA" |

**Lesson para AIOX:**
1. **Scope honesty** (Jina) — explicitar o que /tech-research NÃO faz (quick Q&A, long fluff)
2. **22 .py files (LangChain)** — auditar onde AIOX tem complexidade ornamental
3. **10+ search engines (Local DR)** — alavanca grande de citações, low effort absorption

## Segmento 3 — Purpose-Trained Models

### Players: OpenResearcher (30B), DeepResearcher (7B), Tongyi (30B)

**Padrão arquitetural comum:**
- Modelo treinado especificamente para research (trajetórias, RL, supervisão)
- Self-contained runtime (no API externo)
- Public eval logs

**Onde diferem:**

| Aspecto | OpenResearcher | DeepResearcher | Tongyi |
|---|---|---|---|
| Size | 30B-A3B MoE | 7B (Qwen2.5 base) | 30B-A3B |
| Training | Offline trajectory synth (97k traj) | E2E RL (GRPO) | Multi-stage Alibaba |
| Bench | BrowseComp-Plus 54.8% | +28.9pts custom | (no public score) |
| Adoption | NVIDIA Nemotron | Academic | Alibaba ecosystem |
| Conferences | arXiv | arXiv | ACL/NeurIPS multi |

**Lesson para AIOX:**
1. **NÃO precisa treinar modelo próprio** — pode INTEGRAR esses 3 como BACKEND OPCIONAL
2. **DeepResearcher 7B** = ROI máximo (roda em 24GB GPU comum)
3. **Public eval logs** padrão da indústria — adotar imediatamente
4. **Trajectory synthesis** — usar /tech-research learning logs como training data futuro

## Segmento 4 — Local-First/Privacy

### Players: Local Deep Research

**Padrão arquitetural único:**
- 100% local + encrypted at rest (SQLCipher)
- 10+ search engines integrados (incl. scholarly)
- Docker GPU + Unraid + pip + Docker compose
- Endorsed Vitalik Buterin

**Lesson para AIOX:**
1. **SQLCipher pattern** — encryption nativa absorvível
2. **Unraid Docker compose** — distribuição para NAS/homelab (audience nichada mas leal)
3. **OpenSSF Scorecard + CodeQL + Semgrep badges** — security signaling community-facing

## Cross-Segment Pattern: O Tetraedro do Deep Research 2026

```
         ┌─────────────────┐
         │  PURPOSE-TRAINED│
         │ (OpenResearcher │
         │  DeepResearcher │
         │     Tongyi)     │
         └────────┬────────┘
                  │
                  │ + multi-agent =
                  │
  ┌───────────────┼───────────────┐
  │               │               │
┌─▼─────────┐  ┌──▼───────┐  ┌────▼────────┐
│Multi-Agent│  │ Single-  │  │ Local-First │
│(DeerFlow, │  │ Loop     │  │   (LDR)     │
│ GPT-Res,  │  │(LangChain│  │             │
│ AutoRC)   │  │ Jina)    │  │             │
└───────────┘  └──────────┘  └─────────────┘
        ↑              ↑              ↑
        └──────────────┴──────────────┘
                       │
                  GOVERNANCE
                  ╔══════════╗
                  ║   AIOX   ║  ← Único nesta dimensão
                  ╚══════════╝
```

**Conclusão estratégica:** AIOX não compete dentro de UM segmento — opera numa **5ª dimensão (Governance)** que é ortogonal às 4 dimensões funcionais. Pode COMPOR com qualquer segmento via absorption, mantendo Governance como DNA.
