# Dashboard Intelligence Map

Data: 2026-05-18

## KPIs

| KPI | Valor |
|---|---:|
| Score do bench | 100/100 |
| Players avaliados | 9 |
| Microdimensões | 108 |
| Células com evidência | 972 |
| Personas ponderadas | 12 |
| Nós do grafo | 67 |
| Edges do grafo | 149 |

## Top Players

| Rank | Player | Leitura |
|---:|---|---|
| 1 | slide creator skill stack | Núcleo governado que deve absorver padrões, não ser substituído. |
| 2 | ppt-master | Melhor referência para PPTX nativo editável. |
| 3 | Presenton | Melhor referência para API, MCP e runtime self-hosted. |
| 4 | PPTAgent | Melhor referência para planning/reflection e QA agentic. |
| 5 | banana-slides | Melhor referência de UX prompt-to-edit, com cautela jurídica. |

## Vencedores Por Pergunta

| Pergunta | Vencedor | Por quê |
|---|---|---|
| Como manter governança SINKRA? | slide creator skill stack | Já contém skill, workflows e regras de narrativa/QA. |
| Como exportar PPTX editável? | ppt-master | Padrões de IR visual e DrawingML são os mais absorvíveis. |
| Como expor geração por API/MCP? | Presenton | Runtime self-hosted com superfície de produto mais clara. |
| Como melhorar planejamento e reflexão? | PPTAgent | Loop agentic e avaliação antes/depois são a melhor referência. |
| Como subir UX de edição por prompt? | banana-slides | Referência de experiência, não de cópia direta de código. |

## O que o dashboard deve mostrar melhor

0. **Score:** mostrar `100/100` como completude do bench e deixar claro que produto 100 depende do gate de implementação.
1. **Slides:** começar pela storyline curada em `presentation-brief.json`, não apenas por heurística de matriz.
2. **Personas:** exibir job, must-have, anti-goal e dimensões decisivas junto do ranking.
3. **Sources:** mostrar clones/repositórios/fonte interna; antes o adapter descartava `dash.sources`.
4. **Decision:** usar tiebreakers, cliffs, categorical winners e decision tree para explicar quando a recomendação muda.
5. **Matrix:** mostrar a matriz 108D como instrumento de diagnóstico fino; manter células limpas e mover pergunta operacional, fonte e comentário para painel lateral.
6. **Execution:** exibir P0/P1/P2 de `implementation-readiness-gate.json` como próximo passo, sem reduzir o score do bench.
7. **Skill Blueprint:** destacar `slide-creator-skill-blueprint.md` como o artefato que transforma bench em skill autocontida; isso é o que faltava entre ranking e execução.
8. **Comparativo:** manter comparação par-a-par, mas nomear como `Comparativo`, não `Duelo`, para reduzir leitura de ranking absoluto.
9. **Docs:** manter documentos como apêndice navegável; eles são fonte auditável, não tela primária de decisão.
10. **Micro Gaps:** quando o usuário selecionar slide creator skill, mostrar `deep/slides-creator-micro-gap-map.md/json` como lista de absorções concretas: quem lidera, gap, peso e ação.

## Regra de UX

A apresentação vende a tese; o dash prova. Slides contam história, matriz prova magnitude, personas provam contexto, sources provam rastreabilidade e gaps provam execução.

O blueprint prova absorção. Se o usuário pergunta “e agora como isso melhora a skill?”, o dashboard deve apontar para `slide-creator-skill-blueprint.md`, não apenas para a matriz.

## Navegação Principal Recomendada

`Tese → Slides → Execução → Personas → Micro Gaps → Evidências → Matriz → Comparativo → Docs`

`Score` e `Pesos` ficam fora da navegação principal de benches de produto porque repetem a matriz e servem melhor como auditoria interna.
