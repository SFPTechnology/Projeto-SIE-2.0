# Verdict Comparativo Final — apps/research vs 12 Competidores Deep-Research

> **Slug do bench:** deepresearch-absorption-benchmark
> **URL local:** http://localhost:3004/observatory/bench?slug=deepresearch-absorption-benchmark
> **Data:** 2026-05-18
> **Auditor:** Knowledge Architect (oalanicolas)
> **Profile:** gold_absorption | anchor: `aiox_research` | 25 players × 130 dims

---

## TL;DR (3 linhas)

1. **apps/research é categoria diferente:** observatory comparativo (matrix 25×130 + sliders + personas + URL-state) vs 12 produtos que são research engines (chat → relatório). A pergunta "quem é melhor painel UX de inteligência de deep-research" tem resposta categórica: **apps/research, por ausência de competidor direto**.
2. **Cobertura factual:** apps/research marca 20/20 nas features de observatory. Os 12 competidores marcam 0–3/20 cada (média 0.8/20). O único que chega perto em ângulo adjacente é Perplexity Labs (gera dashboards on-demand) e DeerFlow (replay persistente) — mas nenhum oferece matrix multi-player nem URL-state decisional.
3. **Os gaps reais ficam na camada de produção do research**, não na camada de visualização: sandbox Docker (DeerFlow/AutoResearchClaw), distribuição PyPI/MCP (GPT-Researcher), modelo dedicado (Tongyi/DeepResearcher/OpenResearcher), benchmark harness (DRBench). Já mapeados em `action-plan.yaml` Wave 1.

---

## Tabela 20 features × 13 colunas

Legenda: **YES** = feature comprovada por evidência | **NO** = feature ausente confirmada | **PARTIAL** = sinal adjacente sem fidelidade | **UNK** = sem evidência pública

| # | Feature | apps/research | Perplexity Pro | OpenAI DR | DeerFlow | Claude Research | STORM/Co-STORM | GPT-Researcher | Kimi Researcher | Local-DR | Tongyi DR | LangChain ODR | Jina node-DR | DRBench |
|---|---------|:-------------:|:--------------:|:---------:|:--------:|:---------------:|:--------------:|:--------------:|:---------------:|:--------:|:---------:|:-------------:|:------------:|:-------:|
| 1 | URL-state decisional (`?w_id=N`, `?persona`, `?compare`) | YES `use-decision-state.ts` | NO | NO | NO | PARTIAL (artifact share link) | NO | NO | NO | NO | NO | NO | NO | NO |
| 2 | Sliders por dimensão (130 dims × 25 players) com Σ% e recálculo <300ms | YES `weights-view.tsx` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 3 | Persona presets clicáveis (8 personas) escrevem URL | YES `personas-view` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 4 | Matrix N players × M dimensões com toggle de colunas URL-persistido | YES (25×133, anchor lock) | NO (tabelas geradas ad-hoc no chat) | NO (tabelas no relatório) | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 5 | Duels all-pairs (N choose 2 = 300) com live totals respeitando pesos | YES (compute_duel.ts) | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 6 | Overview 1-pager (hero clamp + decision panel + verdict bar) | YES `observatory.tsx` | PARTIAL (Labs gera dashboards) | NO | PARTIAL (research summary block) | PARTIAL (Live Artifacts) | NO | NO | NO | NO | NO | NO | NO | NO |
| 7 | Battle card MD exportável (winner/runner/top-3/permalink) | YES (clipboard export) | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 8 | Permalink copy ao mudar overrides | YES | NO | NO | NO | PARTIAL (artifact link) | NO | NO | NO | NO | NO | NO | NO | NO |
| 9 | Reset button limpa todos params | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 10 | Delta de rank ▲/▼ ao mover slider | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 11 | 3 dims onboarding (setup_friction, time_to_first_run, docs_quality) com scores reais | YES `onboarding-scores.json` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 12 | Links GitHub clicáveis em winner H1 + runner inline + verdict bar | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 13 | 16 grupos de microdims decompostos (Agentic Planning, MAS Orch, Tool Runtime…) | YES `weights-view.tsx` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 14 | Cell-drawer com score breakdown 5-lente (0-20 cada) + evidence + source path | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 15 | Scoring transparency panel (fórmula + weight policy + 5-tier bands) | YES `matrix-view.tsx` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 16 | Sources view com credibility tags (HIGH/MEDIUM/LOW) + local_clone flags | YES `sources-view.tsx` | PARTIAL (cita fontes inline, sem tag de credibilidade) | PARTIAL (idem) | PARTIAL (idem) | PARTIAL (idem) | NO | PARTIAL (logs) | PARTIAL | NO | NO | NO | NO | NO |
| 17 | Decision view com editor's note + categorical winners + decision tree + tiebreakers + cliffs | YES `decision-view.tsx` | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 18 | Personas view com cards por cenário (ranking + verdict + tiebreaker) | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| 19 | Tri-pane shell (Index + Reader + Inspector) com URL-collapse + responsive | YES `observatory.tsx` | PARTIAL (single chat pane) | PARTIAL (idem) | PARTIAL (dual-column chat + research block) | PARTIAL | PARTIAL (mind-map + chat) | PARTIAL (NextJS frontend single pane) | PARTIAL | NO | NO | NO | NO | NO |
| 20 | 10 nav tabs ordinais (Overview, Matriz, Comparativo, Pesos, Personas, Evidências, Execução, Decisão, Slides, Docs) | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| | **TOTAL YES (de 20)** | **20** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| | **TOTAL PARTIAL** | **0** | **3** | **2** | **3** | **4** | **2** | **3** | **2** | **0** | **0** | **0** | **0** | **0** |
| | **Cobertura %** | **100%** | **7.5%** | **5%** | **7.5%** | **10%** | **5%** | **7.5%** | **5%** | **0%** | **0%** | **0%** | **0%** | **0%** |

**Evidência das colunas PARTIAL** (todos com URL pública):

- Perplexity Pro: dashboards on-demand via Labs ([nocode.mba review 2026](https://www.nocode.mba/articles/perplexity-labs-review), [changelog 2026-02-06](https://www.perplexity.ai/changelog/what-we-shipped---february-6th-2026)) — não persistente, não comparativo multi-player.
- OpenAI Deep Research: "updated visual experience" + tabelas estruturadas a pedido ([OpenAI release feb 2026](https://openai.com/index/introducing-deep-research/)) — interactive sliders são feature separada de ChatGPT (math/science modules), não do DR.
- DeerFlow: Web UI Next.js + ResearchBlock + replay persistence via Mongo/Postgres ([deepwiki.com/bytedance/deer-flow/3-web-interface](https://deepwiki.com/bytedance/deer-flow/3-web-interface)) — sem matrix multi-player nem URL-state decisional.
- Claude Research: Live Artifacts (abril 2026) + share-by-link ([anthropic.com/news/research](https://www.anthropic.com/news/research), [yourstory cowork 2026](https://yourstory.com/ai-story/claude-cowork-live-dashboards-ai-bi-disruption)) — artifact é gerado, não é dashboard comparativo do tipo apps/research.
- STORM/Co-STORM: mind-map UI hospedado ([storm.genie.stanford.edu](https://storm.genie.stanford.edu/)) — visualização conceitual, sem matrix nem sliders.
- GPT-Researcher: frontend NextJS + AG-UI streaming + LangSmith trace ([docs.gptr.dev/frontend](https://docs.gptr.dev/docs/gpt-researcher/frontend/introduction)) — single-pane research, sem matrix nem persona presets.
- Kimi Researcher: Agent Swarm UI (até 100 sub-agents) + multimodal screenshots ([NxCode guide 2026](https://www.nxcode.io/resources/news/kimi-ai-complete-guide-features-pricing-2026)) — não tem dashboard comparativo de competidores.
- Local-DR, Tongyi DR, LangChain ODR, Jina node-DR, DRBench: confirmadamente sem web UI comparativo (inventories `docs/bench/deepresearch-absorption-benchmark/inventories/*.md` + DRBench [github.com/ServiceNow/drbench](https://github.com/ServiceNow/drbench) é CLI+Docker, sem leaderboard hospedado).

---

## 5 Features ÚNICAS de apps/research (nenhum competidor tem)

1. **URL-state decisional completa** (`?w_<dim>=N&persona=ID&players=k1,k2&compare=a,b&view=mode`) — toda decisão é um link reproduzível. Hook canônico em `apps/research/src/components/observatory/foundations/use-decision-state.ts`. Nenhum dos 12 competidores tem URL como state primária do dashboard.
2. **Sliders por dimensão com recálculo live de ranking + delta ▲/▼** — 130 dims agrupadas em 16 grupos, Σ% por grupo, recálculo <300ms, mostrando shift de posição do anchor em tempo real. `apps/research/src/components/observatory/organisms/weights-view.tsx`.
3. **Persona presets clicáveis que escrevem URL e re-rankeam** — 8 personas (Founder, Researcher, Auditor, Procurement, etc.) com `?persona=ID` + clear weights → instant ranking. Nenhum competidor expõe persona-as-preset.
4. **Matrix N×M com chip-toggle URL-persistido + anchor lock + cell-drawer 5-lente** — 25 players × 133 dimensões, cada célula clicável abre breakdown (cobertura, profundidade, fidelidade, evidência, absorção × 0-20 cada) com evidence + source path. Cumpre Rule 10.6 do `research-bench-gold.md`.
5. **Battle card MD + permalink copy + reset** — workflow exportável: winner/runner/top-3 dims/gap/permalink em uma colagem só. Não existe equivalente em Perplexity (gera prosa), Claude (gera artifact estático) nem nos OSS.

---

## 5 GAPS de apps/research (competidor tem, nós não)

1. **Live data refresh** (Claude Live Artifacts, abril 2026 — [yourstory 2026-04-21](https://yourstory.com/ai-story/claude-cowork-live-dashboards-ai-bi-disruption)): nosso dash é snapshot estático do bench-output-dash.json. Gap: dashboard que re-fetcha bench data automaticamente quando re-executado.
2. **Replay timeline persistente do run de research** (DeerFlow chat_streams + LangGraph checkpoint — [deepwiki](https://deepwiki.com/bytedance/deer-flow/3-web-interface)): podemos replayar a sessão que produziu o bench, scrubbando entre waves. Hoje só temos `execution-log.jsonl` sem viewer.
3. **MCP-as-data-source para dashboard** (OpenAI DR 2026-02-10 + GPT-Researcher MCP-native): permitir que o observatory consuma fontes via MCP (Notion, Drive, GitHub) ao vivo, não só do disco.
4. **Mind-map visualization** (Co-STORM KnowledgeBase mind-map — [storm-project.stanford.edu/research/co-storm](https://storm-project.stanford.edu/research/co-storm/)): alternativa à matrix para usuários que pensam por hierarquia conceitual em vez de scoring tabular.
5. **Agent Swarm parallel-research view** (Kimi K2.5 — até 100 sub-agents — [NxCode 2026](https://www.nxcode.io/resources/news/kimi-ai-complete-guide-features-pricing-2026)): visualização do fan-out de sub-agents durante o run (não só do resultado final), útil quando o bench escalar para >50 players.

---

## Veredito Final

apps/research é, **factualmente e por categoria**, o melhor painel UX de inteligência de deep-research em maio/2026 — não porque seja "muito superior" aos 12 competidores listados, mas porque é o **único produto de sua categoria**. Os 12 "competidores" são research engines (input: query → output: relatório), enquanto apps/research é uma **bench observatory** (input: bench gold artifact → output: dashboard decisional 25×130 navegável por URL). A comparação revelou que o estado da arte em deep-research UX (Perplexity Labs, Claude Live Artifacts, DeerFlow web UI, Co-STORM mind-map, GPT-Researcher AG-UI) opera todo no eixo "produzir conhecimento" e ninguém opera no eixo "ajudar o operador a decidir entre N alternativas com pesos editáveis". apps/research deve **manter o DNA decisional** (URL-state + sliders + personas + matrix + duels) como vantagem competitiva permanente, e os P0 gaps do `action-plan.yaml` (sandbox Docker, distribuição PyPI/MCP, model backend) devem ser absorvidos da camada engine — sem contaminar a observatory com features de chat-research que outros já fazem bem. O risco real não é UX: é a observatory virar órfã se a camada engine não acompanhar.

---

## Fontes

- [Perplexity changelog 2026-02-06](https://www.perplexity.ai/changelog/what-we-shipped---february-6th-2026)
- [Perplexity Labs review 2026 — nocode.mba](https://www.nocode.mba/articles/perplexity-labs-review)
- [OpenAI Introducing Deep Research](https://openai.com/index/introducing-deep-research/)
- [OpenAI Deep Research API docs](https://platform.openai.com/docs/guides/deep-research)
- [Anthropic Claude Research news](https://www.anthropic.com/news/research)
- [Claude Live Artifacts coverage — YourStory 2026-04-21](https://yourstory.com/ai-story/claude-cowork-live-dashboards-ai-bi-disruption)
- [DeerFlow Web Interface — DeepWiki](https://deepwiki.com/bytedance/deer-flow/3-web-interface)
- [DeerFlow GitHub (bytedance/deer-flow)](https://github.com/bytedance/deer-flow)
- [GPT-Researcher Frontend docs](https://docs.gptr.dev/docs/gpt-researcher/frontend/introduction)
- [GPT-Researcher GitHub (assafelovic/gpt-researcher)](https://github.com/assafelovic/gpt-researcher)
- [Co-STORM Stanford project page](https://storm-project.stanford.edu/research/co-storm/)
- [STORM Genie hosted UI](https://storm.genie.stanford.edu/)
- [STORM GitHub (stanford-oval/storm)](https://github.com/stanford-oval/storm)
- [Kimi guide NxCode 2026](https://www.nxcode.io/resources/news/kimi-ai-complete-guide-features-pricing-2026)
- [LangChain Open Deep Research GitHub](https://github.com/langchain-ai/open_deep_research)
- [Local Deep Research GitHub](https://github.com/LearningCircuit/local-deep-research)
- [Tongyi/Alibaba DeepResearch GitHub](https://github.com/Alibaba-NLP/DeepResearch)
- [Jina node-DeepResearch GitHub](https://github.com/jina-ai/node-DeepResearch)
- [DRBench GitHub (ServiceNow/drbench)](https://github.com/ServiceNow/drbench)
- [DRBench arXiv:2510.00172](https://arxiv.org/html/2510.00172v2)
- Inventários locais: `docs/bench/deepresearch-absorption-benchmark/inventories/` (27 arquivos)
- Players canônicos: `docs/bench/deepresearch-absorption-benchmark/players.yaml`
- Audit anterior: `docs/bench/deepresearch-absorption-benchmark/comparison-matrix.md` + `executive-report.md`

---

*Verdict Comparativo Final v1.0 — 2026-05-18 — Auditor: oalanicolas — Bench: deepresearch-absorption-benchmark*
