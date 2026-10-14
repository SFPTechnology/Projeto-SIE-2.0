# Segmented Comparisons — Deepresearch Absorption Benchmark

## Segment 1 — Frameworks Multi-Agente

| Player | Score | Notable |
|---|---:|---|
| 🥇 DeerFlow | 72.05 | Memory TIAMAT + Docker sandbox + 90 multi-agent |
| 🥈 GPT-Researcher (tie) | 69.65 | MCP native + PyPI + LangSmith |
| 🥈 AutoResearchClaw (tie) | 69.65 | Sandbox 100 + 23 stages + 6 HITL modes |
| 4 | **AIOX Research** | **60.25** | **Vence Governance/Planejamento, perde Sandbox/Distribuição** |

**AIOX position:** **4º de 4** — último no segmento. Precisa absorver Sandbox (AutoResearchClaw), Multi-Agent parallelism (DeerFlow), Distribution (GPT-Researcher).

## Segment 2 — Single-Agent Loop (Search-Read-Reason)

| Player | Score | Notable |
|---|---:|---|
| Local Deep Research | 63.9 | Categorizado como local-first mas single-loop |
| LangChain ODR | 51.7 | 22 py files + #6 Deep Research Bench |
| Jina node-DR | 44.5 | TS-only + Jina Reader + budget monitoring |

**AIOX lesson:** LangChain ODR roda com **22 .py files** e tem score público **0.4344 #6 no leaderboard**. Simplicidade não compromete qualidade. AIOX deve auditar onde sua complexidade não compra ganho real.

## Segment 3 — Purpose-Trained Models

| Player | Score | Modelo | Benchmark |
|---|---:|---|---|
| Tongyi DR | 52.1 | 30B-A3B | arXiv 2510.24701 |
| DeepResearcher | 50.95 | 7B (Qwen2.5 + RL) | +28.9pts |
| OpenResearcher | 48.2 | 30B-A3B (MoE) | 54.8% BrowseComp-Plus |

**AIOX lesson:** Os 3 ganham **75-78.75 em Modelo** (vs AIOX 38.75) mas perdem em Multi-Agente (22-60), Entrada (22-26), Distribuição (28-37). **AIOX pode ABSORVER como backend opcional** sem reescrever sua arquitetura.

## Segment 4 — License Distribution

| License | Players |
|---|---|
| MIT | DeerFlow, LangChain ODR, Local DR, AutoResearchClaw |
| Apache-2.0 | GPT-Researcher, OpenResearcher, DeepResearcher, Tongyi |
| Jina Proprietary | Jina node-DR |
| **Elastic License v2** | **AIOX Research (app)** |

**AIOX position:** **Único Elastic License v2.** Restrição de SaaS competitor é valor real, mas atrito com community open-source. Recomendação: **dual-license** (Elastic v2 commercial + AGPLv3 community edition).

## Segment 5 — Sandbox Maturity

| Tier | Players |
|---|---|
| 🟢 Full Hardened | AutoResearchClaw (network-policy-aware) |
| 🟢 Available | DeerFlow, Local DR |
| 🟡 Partial | GPT-Researcher, Jina node-DR, DeepResearcher |
| 🔴 None | **AIOX**, LangChain ODR, OpenResearcher, Tongyi |

## Segment 6 — MCP Native

| Status | Players |
|---|---|
| ✅ Yes | GPT-Researcher, LangChain ODR |
| ❌ No | **AIOX**, DeerFlow, Local DR, OpenResearcher, DeepResearcher, Jina, AutoResearchClaw, Tongyi |

**Crítico para AIOX:** MCP é o padrão Claude Code/Anthropic. AIOX deve expor `/tech-research` como MCP server pra ser consumível por outras sessions.

## Segment 7 — Public Benchmark Scores

| Player | Benchmark | Score |
|---|---|---|
| OpenResearcher | BrowseComp-Plus | 54.8% (beats GPT-4.1/Claude Opus 4/Gemini 2.5 Pro/DeepSeek-R1) |
| LangChain ODR | Deep Research Bench | 0.4344 (#6) |
| Local Deep Research | SimpleQA | ~95% accuracy |
| DeepResearcher | Custom RL eval | +28.9pts over baselines |
| **AIOX** | — | **Não testado** |

**Crítico para AIOX:** Sem score público em benchmark padronizado, marketing fica comprometido. **Rodar Deep Research Bench** deveria ser P0 antes do próximo release.

## Segment 8 — Distribution Channels

| Channel | Players com presença |
|---|---|
| PyPI | GPT-Researcher (top), Local DR, DeepResearcher |
| Docker Hub | GPT-Researcher (top), Local DR, DeerFlow, Jina |
| HuggingFace Models | OpenResearcher, DeepResearcher, Tongyi |
| Claude Skill (skills.sh) | GPT-Researcher |
| **AIOX** | **Git clone only — sem PyPI, sem Docker Hub, sem marketplace** |
