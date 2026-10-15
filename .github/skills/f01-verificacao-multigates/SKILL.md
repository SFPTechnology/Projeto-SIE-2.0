---
name: f01-verificacao-multigates
description: "Orquestração QA independente por evidência, regressão e seis gates não autoaprováveis"
---

# f01-verificacao-multigates

Orquestração QA independente por evidência, regressão e seis gates não autoaprováveis.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Mapeie as etapas E01–E05 aos seis gates G01–G06, critério antes/depois e bloqueio. Emita FINDING com ID e prioridade P0/P1/P2; CI não é norma aprovada. Revise três pareceres congelados em branches separadas com matriz de conflitos e divergência. Não conte múltiplos papéis executados em uma mesma sessão como verificação factual independente. Gate exige prova externa autorizada quando aplicável, não só campo JSON preenchido.

## Entrega da skill
Salvar um registro `SKILL-f01-verificacao-multigates.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
