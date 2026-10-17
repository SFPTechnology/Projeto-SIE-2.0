---
name: f01-arquitetura-integridade
description: "Revisão e implementação de arquitetura segura, fronteiras confiáveis, histórico de cálculos e rollback"
---

# f01-arquitetura-integridade

Revisão e implementação de arquitetura segura, fronteiras confiáveis, histórico de cálculos e rollback.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Examine ingestão->motor->resultado->snapshot; identifique flags controladas pelo cliente e vazamento de privilégios. Modele identidade do projeto, circuito, execução, regra e célula com chave natural/revisão, constraints e FK. Exija que status normativo seja calculado só no servidor. Garanta armazenamento atômico, imutabilidade razoável, hash e teste de alteração proposital; explicite limites do SQLite. Teste conflitos entre revisões, backup/restore, autorização cruzada e não mutação de resultados históricos. Evite inventar migração Supabase.

## Entrega da skill
Salvar um registro `SKILL-f01-arquitetura-integridade.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
