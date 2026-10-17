---
name: f01-ux-llm-seguranca
description: "Design UX acessível para decisões de engenharia e engenharia de prompts anti-hallucination/RAG"
---

# f01-ux-llm-seguranca

Design UX acessível para decisões de engenharia e engenharia de prompts anti-hallucination/RAG.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Projete estados explícitos VERIFICADO, PARCIAL, PENDENTE, BLOQUEADO/NAO_APLICAVEL e explique causas com links a evidências e fonte. Sem badges verdes para outputs não homologados. Design system dark/light legível, teclado, erros claros, feedback de carregamento, import/exports rastreáveis. Use escape de conteúdo externo e nunca renderize resposta LLM como HTML arbitrário. Prompts exigem: trecho fiel da fonte, edição, página, citação, confiança, recusa de inferência e justificativa; ataques de prompt injection não podem desbloquear gates. Testar Chromium, leitura com teclado, status quando API está offline, abuso de credenciais e diferenças entre resultados do servidor/UI.

## Entrega da skill
Salvar um registro `SKILL-f01-ux-llm-seguranca.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
