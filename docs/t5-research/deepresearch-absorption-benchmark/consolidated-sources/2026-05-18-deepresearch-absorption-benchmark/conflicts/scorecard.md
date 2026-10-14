# Scorecard — Deepresearch Absorption Benchmark

> Score 0-100 ponderado por grupos × dimensões. **Total weight = 100.** Computação por: `Sum(group_score × group_weight) / total_weight`, onde `group_score = Sum(dim_score × dim_weight) / Sum(dim_weights)`.

## Ranking Geral

| Rank | Player | Score | Top Strength | Top Weakness |
|---:|---|---:|---|---|
| 🥇 1 | **DeerFlow (ByteDance)** | **72.05** | Memory (92.5) + Multi-Agente (90) + Sandbox (84.3) | Citações (55) + Modelo (45) |
| 🥈 2 | **GPT-Researcher** | **69.65** | Distribuição (97) + Entrada (95) + Saída (88.6) | Sandbox (31.4) + Memória (45) |
| 🥈 2 | **AutoResearchClaw** | **69.65** | Sandbox (100) + Saída (90) + Planejamento (85) | Entrada (34) + Distribuição (32) |
| 4 | **Local Deep Research** | **63.9** | Citações (81) + Distribuição (83) + Licença (100) | Multi-Agente (37.5) |
| 5 | **🎯 AIOX Research Ecosystem** | **60.25** | **Governance (100) + Planejamento (96.5)** | **Sandbox (0) + Distribuição (10)** |
| 6 | Tongyi DeepResearch | 52.1 | Modelo (78.75) | Sandbox (0) + Entrada (26) |
| 7 | LangChain Open DR | 51.7 | Entrada (82) + Observabilidade (71) | Sandbox (0) + Multi-Agente (27.5) |
| 8 | DeepResearcher 7B | 50.95 | Modelo (75) | Entrada (22) + Distribuição (28) |
| 9 | OpenResearcher 30B | 48.2 | Modelo (75) + Observabilidade (90) | Entrada (26) + Multi-Agente (22.5) |
| 10 | Jina node-DR | 44.5 | Distribuição (67) + Saída (67.1) | Multi-Agente (17.5) + Memória (25) |

## AIOX — Honest Assessment

### Onde AIOX VENCE (vantagens reais)

| Grupo | Score | Por quê |
|---|---:|---|
| **Governance** | **100** | Únicos com COVERAGE_GATE + CITATION_GATE reais (VETO halt) + Incremental Learning Log per-phase. Nenhum competidor implementa quality gates ao nível de Sinkra Hub. |
| **Planejamento** | **96.5** | 7 phases dedicadas (auto-clarify, clarify, decompose, prompt-gen) + product-discovery framework com JTBD/Mom Test/Villain/WTP. AutoResearchClaw (85) e DeerFlow (80.5) ficam atrás. |
| **Execução** | **82.67** | Multi-wave bounded (max=3) + wave-compression que evita context blow + deep-read protocol. Apenas DeerFlow (83.3) empata. |
| **Citações** | **76.0** | CITATION_GATE com verified_ratio ≥ 0.85 + 2 fix attempts bounded. LDR vence em scholarly DB (81), mas AIOX vence em verify loop estruturado. |

### Onde AIOX PERDE (gaps críticos)

| Grupo | Score AIOX | Líder | Δ | Gravidade |
|---|---:|---|---:|---|
| **Sandbox** | **0.0** | AutoResearchClaw (100) | **-100** | 🔴 P0 — Não temos Docker code-exec isolation |
| **Distribuição** | **10.0** | GPT-Researcher (97) | -87 | 🔴 P0 — Sem PyPI, sem Docker Hub, sem marketplace |
| **Licença** | **54.0** | Todos OSI (100) exceto Jina | -46 | 🟠 P1 — Elastic License v2 no app afasta community |
| **Modelo** | **38.75** | OpenResearcher/DeepResearcher (75) | -36 | 🟠 P1 — Sem purpose-trained model backend |
| **Multi-Agente** | **57.5** | DeerFlow (90) | -33 | 🟡 P2 — Inline persona-fidelity, não paralelo real |
| **Memória** | **52.5** | DeerFlow TIAMAT (92.5) | -40 | 🟡 P2 — Sem cross-session persistence |
| **Entrada** | **37.0** | GPT-Researcher (95) | -58 | 🟠 P1 — Sem MCP server, sem headless API |

## Composição Recomendada (post-absorption)

**Nome:** AIOX Research Hybrid (v6.0.0)
**Score esperado se absorvido:** **88** (vs 60.25 atual → +27.75 pts)

**Thesis:**
> Combinar **AIOX Governance/Planejamento/PT-BR vertical** + **DeerFlow multi-agent sandbox** + **GPT-Researcher MCP/distribution** + **OpenResearcher/DeepResearcher model backend opcional** + **LDR scholarly DB integration**.

**Regra de absorção:**
- REUSE > ADAPT > CREATE (IDS principles)
- Respeitar licenças MIT/Apache; nunca copiar Jina proprietary
- PoC antes de production absorption
- Manter Governance + Planejamento como DNA AIOX intactos

## MVP Cut para AIOX Research v6.0.0

1. **Docker sandbox** para code-execution durante research (via `apps/research /api/research/runs/[runId]`)
2. **MCP server nativo** expondo `/tech-research` como tool consumível por outras Claude Code sessions
3. **PyPI package** `@sinkra/research-cli` — standalone CLI sem hub clone
4. **Docker Hub image** `sinkra/research:latest`
5. **Backend opcional** BYOK + OpenResearcher-30B-A3B + DeepResearcher-7B (HF) com auto-detect GPU
6. **Scholarly DB integration**: arXiv + Semantic Scholar + PubMed (absorvido do LDR)
7. **Memory persistente** cross-session com confidence scores (TIAMAT-like, absorvido do DeerFlow)
8. **Public eval logs** em `docs/research/_eval-logs/` com badge DeepResearchBench score
9. **App License re-evaluation:** dual-license (Elastic v2 commercial + AGPLv3 community edition)

## Metodologia

- **24 dimensões** agrupadas em **13 grupos**
- **10 players** scored (1 AIOX ecosystem + 9 open-source)
- **Pesos somam 100**
- Scores 0-100 atribuídos com base em:
  - Inspeção direta de clones locais (`../bench/{player}/`)
  - README + LICENSE + paper claims explícitos
  - Métricas verificáveis (file counts, benchmark scores publicados)
- **Confiança:** ALTA para dimensões com evidência direta no clone; MEDIA para inferências do README
- **Anti-bias:** mesmo critério aplicado a AIOX que aos competidores. AIOX recebeu 0 onde realmente é 0 (Sandbox).
