# Battle Card — DeepResearch Absorption Benchmark

## Melhor Escolha Por Pergunta

- Se a pergunta é **qual arquitetura absorver primeiro**, comece por **DeerFlow + LangChain Open Deep Research + GPT-Researcher**.
- Se a pergunta é **como testar qualidade de pesquisa**, comece por **DRBench + LiveDRBench + MiroEval + Deep Research Bench**.
- Se a pergunta é **como lidar com dados privados**, comece por **Local Deep Research + DeepSearcher + DRBench**.
- Se a pergunta é **paper/prior art**, use **AutoResearchClaw + STORM** como referência.
- Se a pergunta é **treino/RL**, trate **MiroRL + DeepResearcher + MiroTrain** como metodologia, não como runtime inicial.

## Anti-Decisões

- Não copiar código com licença ausente ou divergente.
- Não aceitar relatório sem `claims.yaml` e `sources.yaml`.
- Não misturar aquisição browser, RAG privado e geração final em um único blob sem trace.
- Não usar dados reais de `workspace/businesses/*` no bench; apenas fixtures sintéticas.

## Próxima Jogada

Abrir a Wave 1 `contract_and_harness`: implementar o `SINKRA DeepResearchRunner`, validar os 9 outputs obrigatórios em dry-run e rodar os 6 adapters iniciais contra os 40 tasks sintéticos antes de qualquer absorção de código.
