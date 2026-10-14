# Scorecard Ponderado — Deep Research Absorption Benchmark

| Dimensão | Peso | Racional |
| --- | --- | --- |
| Qualidade de pesquisa | 18% | Capacidade de encontrar, cruzar e sintetizar fontes com citações úteis. |
| Profundidade de automação | 16% | Planejamento, decomposição, loops de busca/leitura/reflexão e redução de intervenção humana. |
| Evidência e benchmark | 15% | Força de papers, benchmarks externos, repositórios oficiais e claims verificáveis. |
| Local-first e privacidade | 12% | Aderência a uso local, dados sensíveis, self-hosting e controle operacional. |
| Integração e ecossistema | 12% | MCP, APIs, providers, formatos de saída e encaixe em workflows existentes. |
| Custo e eficiência | 10% | Custo por run, necessidade de hardware e previsibilidade financeira. |
| Maturidade e comunidade | 10% | Tração, documentação, releases, adoção e risco de abandono. |
| Licença e risco de adoção | 7% | Licença, abertura real, dependência de vendor e restrições para absorção. |

## Ranking

| Rank | Player | Score | Vencedor em | Veredito |
| --- | --- | --- | --- | --- |
| 1 | GPT-Researcher | 83.2 | framework multi-agente | Melhor custo-benefício e melhor encaixe MCP imediato para o Sinkra Hub. |
| 2 | Local Deep Research | 83 | local-first | Melhor opção privacy-first/air-gapped. |
| 3 | DeerFlow | 82.3 | framework multi-agente | Melhor general-purpose quando popularidade, sandbox e memória importam. |
| 4 | DeepResearcher | 81.8 | modelo RL-trained | Melhor aposta local de modelo pequeno treinado para research. |
| 5 | OpenResearcher | 80.1 | modelo RL-trained | Melhor accuracy em benchmark, mas com custo de hardware e corpus offline. |
| 6 | Hermes Agent | 79.1 | agente autônomo generalista | Melhor referência de agente 24/7 com self-learning, mas não é especializado em deep research. |
| 7 | STORM | 76.1 | artigo científico | Referência acadêmica para síntese multi-perspectiva em formato artigo. |
| 8 | LangChain Open Deep Research | 75.1 | single-loop | Melhor quick start benchmarkado; ótimo baseline, menos poderoso que RL-trained. |
| 9 | AutoResearchClaw | 71.9 | paper científico | Melhor para ideia -> paper acadêmico, não para research generalista barato. |
| 10 | DeepSearcher | 71.4 | dados privados/RAG | Melhor para knowledge base privada, não para web deep research geral. |
| 11 | Jina node-DeepResearch | 70.3 | single-loop TypeScript | Melhor protótipo rápido em TypeScript. |
| 12 | Auto-Deep-Research | 66.9 | framework multi-stage | Emergente; observar antes de adotar como core. |
| 13 | Firecrawl Open Deep Research | 58.4 | single-loop com extração web | Útil se Firecrawl já for o motor de extração; nicho no restante. |
| 14 | Kimi-Researcher | 58 | modelo RL-trained parcial | Forte como referência técnica, fraco como opção open-source absorvível. |

## Método

As notas são derivadas do relatório técnico, dos artefatos `players.yaml` e `sources.yaml`, e das recomendações do runtime Claude. O score não é benchmark executado localmente; é uma rubrica de decisão baseada em evidência pública.
