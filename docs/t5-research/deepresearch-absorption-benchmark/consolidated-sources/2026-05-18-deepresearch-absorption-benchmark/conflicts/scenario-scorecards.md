# Scenario Scorecards — Deepresearch Absorption Benchmark

8 cenários reais de uso, com pesos override-ados para o caso. **AIOX vence 3, empata 1, perde 4.**

## S1 — Pesquisa Acadêmica → Paper Conference-Ready

> User wants to research a topic and produce a conference-ready paper with figures, baselines, citations.
> Weights: Citações 25 / Saída 15 / Sandbox 12 / Planejamento 12.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | AutoResearchClaw | 89.5 | 23 stages + CodeAgent/BenchmarkAgent/FigureAgent + Docker hardened |
| 2 | DeerFlow | 71.0 | Multi-agent + memory |
| 3 | GPT-Researcher | 70.5 | PDF/DOCX nativo |
| 4 | **AIOX Research** | **65.0** | Vence em Planejamento/Citações mas perde em FigureAgent + Sandbox |
| 5 | Local DR | 64.0 | Scholarly DB forte |

## S2 — Product Discovery (JTBD + Villain + WTP) ✅ **AIOX VENCE**

> User wants to validate a product idea with market research, competitive analysis, JTBD framing.
> Weights: Planejamento 20 / Citações 18 / Saída 15 / Governance 12.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | **AIOX Research** | **85.5** | **Único com product-discovery framework + JTBD + Mom Test + Villain + WTP signals built-in** |
| 2 | GPT-Researcher | 70.0 | Generic multi-agent |
| 3 | DeerFlow | 67.5 | Sandbox forte mas não product-specific |
| 4 | AutoResearchClaw | 67.0 | Academic-focused |

## S3 — Privacy / Air-Gapped Research

> Enterprise/government scenario: 100% local, no API calls externos, encrypted at rest.
> Weights: Modelo 18 / Memória 15 / Sandbox 12 / Licença 10.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | Local Deep Research | 86.0 | SQLCipher + 10+ search engines locais + Ollama + Docker GPU |
| 2 | OpenResearcher | 65.0 | 30B model self-contained mas sem encryption nativa |
| 3 | DeepResearcher | 63.5 | 7B model standalone |
| 4 | **AIOX Research** | **50.0** | App local-first mas requer LLMs externos (BYOK Ollama parcial) |

## S4 — Competitive Intelligence (B2B) ✅ **AIOX VENCE**

> Marketing/PM/founder fazendo análise de concorrente, battle cards, market positioning.
> Weights: Citações 18 / Saída 18 / Multi-Agente 12 / Governance 10.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | **AIOX Research** | **78.0** | **Squad research (renomeado de spy) + 14 specialist personas + dedicated bench-comparison workflow** |
| 2 | GPT-Researcher | 75.5 | Output PDF/DOCX/HTML perfect para battle cards |
| 3 | DeerFlow | 73.0 | Multi-agent strong |
| 4 | AutoResearchClaw | 70.0 | Generic frameworks |

## S5 — Quick Q&A (não long-form)

> User só quer resposta rápida e factual.
> Weights: Entrada 15 / Execução 18 / Saída 8 / Distribuição 15.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | Jina node-DR | 78.0 | Single-loop search/visit/reflect/answer + budget monitoring + stable API |
| 2 | GPT-Researcher | 75.0 | API REST hospedada |
| 3 | LangChain ODR | 67.0 | Compacto |
| 4 | **AIOX Research** | **45.0** | **Pipeline 7-molecule é overkill para quick Q&A. Considerar `/quick-answer` skill irmã.** |

## S6 — Benchmark-Driven (score público obrigatório)

> User precisa de research agent com score público verificável em benchmark padronizado.
> Weights: Modelo 25 / Observabilidade 18 / Execução 15.

| Rank | Player | Score | Bench |
|---:|---|---:|---|
| 🥇 | OpenResearcher | 88.5 | 54.8% BrowseComp-Plus + NVIDIA Nemotron |
| 2 | Local DR | 82.0 | ~95% SimpleQA |
| 3 | LangChain ODR | 75.0 | #6 Deep Research Bench |
| 4 | DeepResearcher | 74.0 | +28.9pts emergent behaviors |
| 5 | **AIOX Research** | **38.0** | **Sem score público. P0: rodar Deep Research Bench.** |

## S7 — PT-BR/LatAm Vertical ✅ **AIOX VENCE (LARGE)**

> User PT-BR fazendo research para lançamento, ICP, oferta, validação de mercado.
> Weights: Planejamento 22 / Saída 18 / Citações 12 / Governance 10.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | **AIOX Research** | **92.0** | **Único com PT-BR/LatAm-first positioning + workflow verticals (PRD/BMC/battle-card grade) + product-discovery framework + 4 negócios dogfood** |
| 2 | GPT-Researcher | 68.0 | Funciona em PT-BR mas EN-first |
| 3 | DeerFlow | 65.0 | China-first + EN |

## S8 — Skill Embarcada no Claude Code Ecosystem

> Skill instalável diretamente no Claude Code via marketplace.
> Weights: Entrada 22 / Distribuição 25 / Multi-Agente 12.

| Rank | Player | Score | Por quê |
|---:|---|---:|---|
| 🥇 | GPT-Researcher | 86.0 | Publicada em skills.sh + MCP Server nativo + Apache-2.0 |
| 2 | LangChain ODR | 73.0 | CLAUDE.md nativo + MCP + uv |
| 3 | **AIOX Research** | **65.0** | **Skill local mas não publicada em marketplace público** |

## Strategic Implication

**AIOX domina onde Planejamento + Governance + PT-BR vertical importam (3 wins):**
- ✅ Product Discovery (S2)
- ✅ Competitive Intelligence (S4)
- ✅ PT-BR/LatAm Vertical (S7)

**AIOX perde onde Distribuição + Modelo + Benchmark público importam (4 losses):**
- ❌ Quick Q&A (S5) — pipeline overkill
- ❌ Benchmark-Driven (S6) — sem score público
- ❌ Claude Code marketplace (S8) — não publicada
- ❌ Privacy/Air-gapped (S3) — depende de LLMs externos

**Empata em paper acadêmico (S1)** — falta FigureAgent + Sandbox para vencer.
