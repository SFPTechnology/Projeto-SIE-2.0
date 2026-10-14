# Expansão Técnica Da Matriz — Agenticidade, UX E Profundidade De Pesquisa

Data: 2026-05-18  
Status: gold extension  
Escopo: expansão da matriz de 30 para 48 microdimensões, mantendo 25 players e AIOX Research como referência interna na primeira coluna.

## Objetivo

A matriz anterior era forte em absorção arquitetural, observabilidade, private-KB, avaliação, maturidade, pipeline científico, treino, UX geral, compliance e fit SINKRA. A expansão adiciona detalhe técnico onde a decisão estava grossa demais:

- planejamento agentic e controle de estratégia;
- orquestração multiagente real;
- integração de tools, browser, MCP/API e runtime;
- profundidade de pesquisa e síntese;
- fidelidade de evidência e avaliação factual;
- UX operacional para configurar, acompanhar, exportar e auditar pesquisas.

## Nova Estrutura

Foram adicionados 6 macrogrupos, cada um com 3 lentes:

| Macrogrupo | Peso | Lentes | Pergunta decisiva |
| --- | ---: | --- | --- |
| Agentic Planning Control | 6 | cobertura, profundidade, evidência/replay | O sistema transforma uma pergunta aberta em plano de pesquisa executável, auditável e ajustável? |
| Multi-Agent Orchestration | 6 | cobertura, profundidade, evidência/replay | O player coordena múltiplos papéis ou agentes com estado, handoff e controle de execução? |
| Tool Runtime Integration | 5 | cobertura, profundidade, evidência/replay | O player integra ferramentas reais de busca/browser/execução com runtime controlável? |
| Research Depth Synthesis | 6 | cobertura, profundidade, evidência/replay | O player produz pesquisa profunda, multi-hop e sintetizada, não apenas resposta curta com links? |
| Evidence Fidelity Evaluation | 4 | cobertura, profundidade, evidência/replay | O player preserva fontes, mede qualidade factual e permite verificar as claims? |
| UX Operator Control | 3 | cobertura, profundidade, evidência/replay | O produto oferece uma experiência operacional clara para configurar, acompanhar e auditar a pesquisa? |

Política de peso: as 30 microdimensões anteriores foram reponderadas para 70% do total; as 18 novas dimensões somam 30%. A soma final permanece 100.

## Sinais Técnicos Usados

| Player | Sinais mais relevantes para a expansão |
| --- | --- |
| AIOX Research | `tech-research/SKILL.md`, gates de cobertura/citação, learning log incremental, dashboard Observatory, contrato SINKRA-DR e dry-runs locais. |
| GPT-Researcher | README, `multi_agents`, LangGraph/AG2, planner/execution/publisher, frontend, CLI, MCP e exportação PDF/DOCX/Markdown. |
| DeerFlow | lifecycle de runs, memória/estado, skill frontmatter, StreamBridge, web app e runtime agentic. |
| AutoResearchClaw | StageContract, VerifiedRegistry, Docker sandbox, políticas HITL, stage ledger e pipeline científico end-to-end. |
| STORM | pipeline acadêmico de outline/interview/synthesis, interfaces de retriever/engine/agent e artefatos intermediários. |
| Local Deep Research | runtime local/private, múltiplos search engines, histórico local, cards/source storage e SimpleQA-style positioning. |
| LangChain Open Deep Research | graph runtime, exemplos de relatórios, organização por etapas e boa base para pesquisa paralela. |
| OpenResearcher | runner de benchmark, search service local/dense/BM25, BrowseComp-Plus/GAIA e modelo 30B orientado a agente. |
| Alibaba/Tongyi DeepResearch | AgentFounder/WebDancer/WebWatcher, agentic CPT, search/visit tools, logs e foco em training pipeline. |
| DRBench, Deep Research Bench, LiveDRBench, MiroEval | maior peso em avaliação, datasets, judge pipeline, claim discovery e fidelidade factual do que em UX ou produto final. |
| MiroFlow, MiroRL, MiroTrain | fortes em runtime/tool registry, RL e treino; variam em UX e profundidade de produto de pesquisa. |
| dzhng, JigsawStack, node-DeepResearch, nickscamara, Auto-Deep-Research | bons sinais de baseline, API/TypeScript, UX ou AutoAgent, mas menor evidência de avaliação/replay robusto. |

## Interpretação Dos Novos Resultados

Depois da expansão, AIOX Research segue como referência interna e líder global porque a matriz passou a valorizar explicitamente governança, replay, dashboard e profundidade metodológica. A diferença não significa que AIOX tenha todos os melhores componentes: DeerFlow, GPT-Researcher, AutoResearchClaw, OpenResearcher e Alibaba/Tongyi continuam vencendo dimensões específicas que devem ser absorvidas seletivamente.

Principais leituras:

- **Agenticidade:** AIOX, OpenResearcher, Alibaba/Tongyi, MiroRL e AutoResearchClaw sobem quando a pergunta é planejamento/replanning, mas DeerFlow e GPT-Researcher continuam fortes em orquestração operacional.
- **UX:** AIOX e GPT-Researcher são as referências mais completas para operador; nickscamara/open-deep-research é útil como baseline de experiência Next.js, mesmo com menor profundidade factual.
- **Profundidade de pesquisa:** OpenResearcher, Alibaba/Tongyi, DeepResearcher, STORM, AutoResearchClaw, GPT-Researcher e AIOX formam o núcleo que merece análise mais minuciosa por cenário.
- **Evidência:** DRBench, Deep Research Bench, LiveDRBench e MiroEval não devem ser tratados como produtos de pesquisa completos, mas como peças críticas para medição, claim verification e regressão.
- **Tool runtime:** AutoResearchClaw, Agent Browser Workspace, DeerFlow, MiroFlow, GPT-Researcher, Alibaba/Tongyi e OpenResearcher são as fontes mais úteis para absorver execução, browser/tool-use e sandbox.

## Implicações Para Absorção

1. AIOX deve manter o contrato SINKRA-DR e o Observatory como camada de decisão, não trocar por um player externo.
2. Absorver de DeerFlow/GPT-Researcher o que melhora runtime de execução, streaming, MCP e distribuição.
3. Absorver de AutoResearchClaw a disciplina de stage contracts, sandbox, HITL e auditabilidade científica.
4. Usar DRBench, Deep Research Bench, LiveDRBench e MiroEval como harnesses de avaliação, não como UX principal.
5. Tratar OpenResearcher/Alibaba/Tongyi/DeepResearcher como referência de modelo/agente treinado, mas com absorção clean-room.
6. Evoluir a UX do Observatory para seleção de players, cenário/persona e replay de evidência por célula.

## Limites E Confiança

Esta expansão usa evidência local dos clones em `../bench`, artefatos code-anatomist já produzidos, README/código inspecionados e o contrato gold do próprio bench. Ela não executa novamente cada player em workload factual equivalente. Portanto:

- confiança alta para capacidades explícitas em README/código/bench local;
- confiança média para inferências por arquitetura sem execução E2E;
- confiança baixa onde o clone mostra apenas intenção ou camada parcial.

O próximo refinamento ideal é rodar um mini-protocolo factual comum em 5 players fortes: AIOX Research, GPT-Researcher, DeerFlow, AutoResearchClaw e OpenResearcher.
