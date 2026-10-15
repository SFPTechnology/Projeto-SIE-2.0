---
name: f01-dados-evidencias
description: "Modelagem de fontes, regras consumidas, snapshots imutáveis e trilha auditável por cálculo e projeto"
---

# f01-dados-evidencias

Modelagem de fontes, regras consumidas, snapshots imutáveis e trilha auditável por cálculo e projeto.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Distinga catálogo de candidatos de proveniência de cálculo real. Modele ProjectRevision, CircuitRun, SourceEdition, NormativeCell, RuleRevision, RuleUse, ResultVersion e QAApproval com integridade referencial e identidade de auditor. Vincule entrada/fórmula/saída/tempo/status ao conjunto de regras consumidas; não permita cliente declarar verificação. Faça migração reversível somente em SQLite temporário; teste concorrência, backfill NÃO presumido, restore, diffs. Gere relatório de impacto: histórico preservado e mudança exige revisão.

## Entrega da skill
Salvar um registro `SKILL-f01-dados-evidencias.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
