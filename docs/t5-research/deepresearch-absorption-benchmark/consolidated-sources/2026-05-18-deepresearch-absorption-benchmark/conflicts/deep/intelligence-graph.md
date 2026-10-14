# Intelligence Graph

> Mapa de relações entre players, lineage, dependências e mutual influence.

## Lineage Graph

```
                    [STORM paper Stanford 2024]
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        [GPT-Researcher]  [DeerFlow]  [LangChain ODR]
              │                │
              │                ├──── inspired ────► [Auto-Deep-Research HKU]
              │                │
              │                └──── parallel ────► [Tongyi DeepResearch]
              │
              └─── inspired ────► [Jina node-DR] (Q&A focused)

[OpenAI Deep Research launched]
              │
              ├──── motivated ────► [Local Deep Research] (privacy alternative)
              │
              ├──── motivated ────► [Jina node-DR] (built in hours after launch)
              │
              └──── benchmarked against ──► [OpenResearcher 30B] (beats GPT-4.1/Claude/Gemini)

[Reinforcement Learning lineage]
              │
              ├────► [DeepResearcher 7B] (E2E RL via GRPO)
              ├────► [Kimi-Researcher] (partial OSS)
              └────► [OpenResearcher 30B] (trajectory synthesis)

[AIOX Research]
              │
              ├──── absorbed ────► [deep-research v1.0.0] (2026-04-13)
              ├──── absorbed ────► [tech-research v2.0.0 skill] (2026-05-16)
              ├──── renamed from ──► [spy squad]
              └──── lineage from ──► [BMAD analyst + Booth + Creswell + Sackett methodologies]
```

## Mutual Citation Graph

| Player | Cites/References | Cited by |
|---|---|---|
| GPT-Researcher | STORM, Plan-and-Solve, RAG | LangChain ODR (architectural inspiration), Jina (mention) |
| DeerFlow | Multi-agent papers, Doubao/DeepSeek | Auto-Deep-Research |
| OpenResearcher | BrowseComp-Plus bench, NVIDIA Nemotron | Tongyi |
| DeepResearcher | GRPO paper, Qwen2.5 | Academic citations |
| LangChain ODR | DeepResearchBench leaderboard | LangChain ecosystem |
| Tongyi | WebWalker (ACL 2025), WebDancer (NeurIPS 2025), WebSailor | OpenResearcher comparison |
| Local DR | Vitalik blog, OpenSSF | Self-sovereign LLM community |

## Influence Score (out-degree)

| Player | Influence | Influence Sources |
|---|---:|---|
| STORM paper | 9 | Foundation of multi-agent research design |
| OpenAI Deep Research | 7 | Catalyzed open-source movement (LDR, Jina, etc) |
| GPT-Researcher | 6 | Reference implementation for open multi-agent |
| LangChain | 5 | LangGraph ecosystem |
| DeerFlow | 4 | Most popular OSS (66k stars) |
| Bessemer Vertical AI thesis | 3 | Strategic positioning anchor |

## Architectural Influence on AIOX

**Direct absorption candidates:**

```
AIOX ──absorbs──► [Docker sandbox]      from AutoResearchClaw, DeerFlow
       │
       ├──absorbs──► [MCP server]        from GPT-Researcher, LangChain ODR
       │
       ├──absorbs──► [Scholarly DBs]     from Local DR
       │
       ├──absorbs──► [Memory layer]      from DeerFlow TIAMAT
       │
       ├──optional──► [Model backend]    from OpenResearcher, DeepResearcher, Tongyi
       │
       └──learns from──► [Scope honesty] from Jina node-DR
                       └──► [Simplicity audit] from LangChain ODR (22 py)
```

## Ecosystem Health Indicators

| Metric | Healthy threshold | Top players |
|---|---|---|
| GitHub stars > 10k | 6 players meet | DeerFlow (66k), GPT-Researcher (20k), LangChain ODR (high), LDR (high) |
| Active commits last 30d | All 9 active | All meeting |
| License OSI | 8 of 9 | Jina is proprietary outlier |
| Multi-language docs | DeerFlow leads | 4 translations |
| Public benchmark score | 4 of 9 | OpenResearcher (54.8% BrowseComp-Plus), LDR (~95% SimpleQA), LangChain (#6 DRB), DeepResearcher (+28.9pts) |
| Conference papers | 3 of 9 | OpenResearcher, DeepResearcher, Tongyi (multi) |
| Production endorsement | 2 of 9 | OpenResearcher (NVIDIA), LDR (Vitalik) |

## AIOX Position in Graph

**AIOX é um HUB ESPECIALIZADO**, não um competidor head-to-head:

1. **Único com governance layer** explícita (gates + learning logs)
2. **Único com 5+ modes unified** (vs single-mode opensource)
3. **Único PT-BR vertical**
4. **Único com tri-layer** (squad+skill+app)
5. **NÃO único em:** model agnosticism, prompt engineering, multi-wave search

Estratégia: **vantagens defensáveis (1-4) + absorber gaps (5)**.
