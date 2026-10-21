---
name: f01-calculo-independente
description: "Ensaios de referência de engenharia elétrica com unidades, tolerâncias, condições limite e fontes comprovadas"
---

# f01-calculo-independente

Ensaios de referência de engenharia elétrica com unidades, tolerâncias, condições limite e fontes comprovadas.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Implemente fixtures independentes por Ib≤In≤Iz, correção térmica e agrupamento, queda de tensão com cosφ/Rca/XL conforme regime, e enquadramento EDP por modalidade/critério comprovado. Separe CASO-MOCK-ALGORITMO de CASO-NORMATIVO-VERIFICADO; o primeiro nunca libera gate. Cada fixture deve incluir entrada, fórmula, expected calculado fora do motor SIE, unidade, arredondamento, referência primária e revisão. Detecte discrepâncias do F00 sem mudar o golden de caracterização.

## Entrega da skill
Salvar um registro `SKILL-f01-calculo-independente.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
