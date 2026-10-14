# Metodologia da Matriz v4

Data: 2026-05-18

## Objetivo

A matriz mede o quanto cada projeto contribui para construir uma solução SINKRA de criação de slides com IA no nível Gamma ou acima, preservando PPTX editável, execução local, API/MCP, governança narrativa e QA.

## Unidade de análise

- 9 players: nosso `slides-creator` + 8 projetos open-source clonados.
- 36 dimensões macro preservadas como baseline em `deep/macro-comparison-matrix.md/json`.
- 108 microdimensões operacionais na matriz principal.
- 972 células de score.
- Cada macro dimensão foi quebrada em três checks concretos: existência, profundidade operacional e absorvibilidade/risco para SINKRA.

## Escala

- 0–20: ausência ou apenas intenção.
- 21–49: capacidade fraca, protótipo ou não central.
- 50–69: cobertura parcial útil.
- 70–84: cobertura forte com gaps conhecidos.
- 85–100: referência de absorção para aquela dimensão.

## Fórmula

`score_total_player = soma(score_da_célula × peso_da_microdimensão) / soma(pesos)`

Como os pesos somam 100, o total final permanece na escala 0–100.

## Fórmula da Célula

`score_da_célula = cobertura + profundidade + fidelidade + evidência + absorvibilidade`

Cada lente vale 0–20.

| Lente | Pergunta |
|---|---|
| Cobertura funcional | A capacidade existe e cobre o caso de uso da microdimensão? |
| Profundidade operacional | É fluxo real, integrado e repetível, ou só demo/protótipo? |
| Fidelidade do output/UX | O resultado final atende o padrão esperado: PPTX editável, UX boa, QA, fonte ou runtime conforme a dimensão? |
| Força da evidência | A nota vem de código/docs/testes locais ou de inferência fraca? |
| Absorvibilidade SINKRA | Conseguimos absorver como código, contrato, fixture, padrão ou só inspiração com risco? |

## Diferença Dentro de 85–100

| Faixa | Decisão |
|---|---|
| 85–89 | Referência útil, mas ainda com uma ressalva relevante: integração parcial, evidência incompleta, risco de absorção ou gap de acabamento. |
| 90–94 | Referência forte e operacional: fluxo claro, evidência local suficiente e poucos gaps conhecidos. |
| 95–98 | Best-in-class para aquela microcapacidade: implementação profunda, repetível, bem documentada e diretamente aproveitável como padrão/contrato. |
| 99 | Praticamente ideal no contexto do bench: cobre a microcapacidade com profundidade, evidência alta, integração clara e sem gap relevante conhecido. |
| 100 | Reservado para requisito exatamente atendido no nosso alvo ou capacidade sem gap/material risk no contexto avaliado; não significa perfeição universal. |

## Pesos

Os pesos somam 100. O peso macro original foi distribuído entre os três checks filhos de cada dimensão para preservar a tese decisória e aumentar granularidade sem inflar artificialmente uma área.

## Fontes

- Clones locais em `../bench/`.
- Artefatos internos em `squads/slides-creator`, `.agents/skills/slides-chief` e `outputs/sinkra-squad/criacao-slides-ia`.
- Benchmarks correlatos em `docs/bench/presenton-vs-gamma` e pesquisa antiga consolidada em `deep/consolidated-research-archive.md`.
- Evidence ledger deste bench.

## Confiança da Evidência

| Confiança | Critério |
|---|---|
| High | Código, docs, scripts ou testes lidos no clone/local skill. |
| Medium | README, fluxo parcialmente verificado ou evidência suficiente mas não executada. |
| Low | Inferência, claim indireto ou sinal incompleto; precisa revalidação antes de implementação. |

Confiança não altera automaticamente o score. Ela indica risco da leitura e define se uma célula precisa de revalidação antes de virar story, contrato ou implementação.

## Regras de decisão

1. O score não mede estrelas do GitHub; mede valor de absorção para o nosso cenário.
2. Capacidade com licença incompatível pode pontuar alto como referência, mas não como código copiável.
3. Um projeto pode liderar uma dimensão e ainda não ser recomendação como base única.
4. A recomendação final é composição modular, não fork único.
5. A matriz 108D é o instrumento de diagnóstico fino; o score agregado serve apenas para ordenar absorção, não para declarar um vencedor universal.
