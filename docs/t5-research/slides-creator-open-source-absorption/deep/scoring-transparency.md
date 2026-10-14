# Transparência de Scoring — Matriz 108D

Data: 2026-05-18

Este arquivo documenta como a pontuação da matriz é calculada e como deve ser lida no dashboard.

## Fórmula da Célula

`score_da_célula = cobertura + profundidade + fidelidade + evidência + absorvibilidade; cada lente vale 0-20.`

| Lente | Pontos | Pergunta |
| --- | --- | --- |
| Cobertura funcional | 0-20 | A capacidade existe e cobre o caso de uso da microdimensão? |
| Profundidade operacional | 0-20 | É fluxo real, integrado e repetível, ou só demo/protótipo? |
| Fidelidade do output/UX | 0-20 | O resultado final atende o padrão esperado: PPTX editável, UX boa, QA, fonte ou runtime conforme a dimensão? |
| Força da evidência | 0-20 | A nota vem de código/docs/testes locais ou de inferência fraca? |
| Absorvibilidade SINKRA | 0-20 | Conseguimos absorver como código, contrato, fixture, padrão ou só inspiração com risco? |

## Fórmula do Total

`score_total_player = soma(score_da_célula * peso_da_microdimensão) / soma(pesos).`

Como os pesos somam 100, o total final permanece na escala 0-100.

## Unidade de Análise

- 9 players.
- 36 dimensões macro arquivadas como baseline.
- 108 microdimensões operacionais na matriz principal.
- 972 células de score.

## Bandas

| Faixa | Significado |
| --- | --- |
| 0-20 | ausente, intenção ou sinal não operacional |
| 21-49 | fraco, protótipo, capacidade lateral ou sem profundidade suficiente |
| 50-69 | cobertura parcial útil, mas com gaps relevantes |
| 70-84 | cobertura forte com gaps conhecidos |
| 85-100 | referência de absorção para aquela microcapacidade |

## Diferença Dentro de 85-100

| Faixa | Decisão |
| --- | --- |
| 85-89 | Referência útil, mas ainda com uma ressalva relevante: integração parcial, evidência incompleta, risco de absorção ou gap de acabamento. |
| 90-94 | Referência forte e operacional: fluxo claro, evidência local suficiente e poucos gaps conhecidos. |
| 95-98 | Best-in-class para aquela microcapacidade: implementação profunda, repetível, bem documentada e diretamente aproveitável como padrão/contrato. |
| 99 | Praticamente ideal no contexto do bench: cobre a microcapacidade com profundidade, evidência alta, integração clara e sem gap relevante conhecido. |
| 100 | Reservado para requisito exatamente atendido no nosso alvo ou capacidade sem gap/material risk no contexto avaliado; não significa perfeição universal. |

## Ajustes

| Delta | Quando usar |
| --- | --- |
| +1 a +4 | Sinal acima do macro: a microcapacidade é mais forte que a dimensão-mãe. |
| -1 a -6 | Sinal abaixo do macro: a microcapacidade específica é menos comprovada que a dimensão-mãe. |
| -10 ou mais | Ausência de runtime, licença incerta, SaaS-only, saída rasterizada ou evidência fraca para aquele uso. |

## Confiança

| Confiança | Critério |
| --- | --- |
| high | Código, docs, scripts ou testes lidos no clone/local skill. |
| medium | README, fluxo parcialmente verificado ou evidência suficiente mas não executada. |
| low | Inferência, claim indireto ou sinal incompleto. |

## Regras de Leitura

1. O vencedor de uma linha é o maior score naquela microdimensão.
2. 85-89 e 99 não são equivalentes: 85-89 ainda tem uma ressalva relevante; 99 não tem gap relevante conhecido no contexto do bench.
3. O score consolidado é mapa de absorção, não ranking absoluto justo.
4. Apps, skills, engines e agentes devem ser lidos por segmentos quando a decisão for de produto.
5. Scores com baixa confiança não devem virar implementação sem revalidação.
6. Gaps da SINKRA devem ser lidos junto com `deep/slides-creator-micro-gap-map.md`.
