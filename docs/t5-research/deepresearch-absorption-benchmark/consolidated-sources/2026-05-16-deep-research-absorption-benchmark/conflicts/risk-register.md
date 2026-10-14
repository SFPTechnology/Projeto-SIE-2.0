# Risk Register — Deep Research Absorption Benchmark

| ID | Risco | Prob. | Impacto | Mitigação |
| --- | --- | --- | --- | --- |
| R01 | Adotar hype por stars sem benchmark próprio. | ALTA | ALTO | Rodar 5 queries do Deep Research Bench e 5 queries reais do Hub antes de adoção. |
| R02 | Modelo RL-trained vencer benchmark mas não servir para pesquisa atualizada em web real-time. | MEDIA | ALTO | Separar uso de OpenResearcher/DeepResearcher para accuracy offline de uso operacional real-time. |
| R03 | Vazamento de dados sensíveis ao usar frameworks cloud/search externos. | MEDIA | ALTO | Usar Local Deep Research ou stack local para workspace L0/L1; proibir queries sensíveis em providers externos. |
| R04 | Complexidade de setup matar adoção interna. | MEDIA | MÉDIO | Começar por GPT-Researcher MCP e LangChain Open DR como baseline antes de DeerFlow/AutoResearchClaw. |
| R05 | Benchmarks anglófonos não refletirem qualidade em PT-BR. | ALTA | MÉDIO | Criar fixture PT-BR com perguntas reais e avaliação por citações, nuance e utilidade executiva. |
