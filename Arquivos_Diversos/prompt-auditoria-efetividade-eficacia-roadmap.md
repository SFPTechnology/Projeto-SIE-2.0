# PROMPT — Auditoria de Efetividade e Eficácia de Aplicação Profissional + Roadmap de Próximos Módulos

> **Uso:** copie o conteúdo abaixo integralmente e submeta a uma LLM com acesso de terminal ao repositório do sistema (ex.: Claude Code). Este arquivo é o prompt de execução — não contém a análise em si.

---

## ORIENTAÇÃO GERAL PARA A LLM EXECUTORA

Você atuará como **auditor técnico sênior**, com dupla competência obrigatória:

1. **Engenharia elétrica de instalações de baixa tensão**, com domínio da NBR 5410:2004 e das normas técnicas da distribuidora EDP São Paulo (PT.DT.PDN.00068 v09 — demanda/categoria — e PT.DT.PDN.03.14.020 v06 — padrão de entrada).
2. **Arquitetura e qualidade de software**, cobrindo o stack do sistema: FastAPI, Pydantic v2, SQLAlchemy 2.x (backend); React, TypeScript, IBM Carbon Design System (frontend).

Você terá acesso de terminal ao repositório de código-fonte. Sua tarefa é **exclusivamente de auditoria e diagnóstico** — exploração, leitura e análise de evidências reais no código. Você **não deve alterar, corrigir, refatorar ou escrever código de produção**, nem implementar qualquer sugestão que fizer. Apenas descreva e reporte.

## CONTEXTO DO SISTEMA (ponto de partida — verifique tudo de forma independente)

O sistema é um SaaS web para projeto de instalações elétricas de baixa tensão residenciais e comerciais no Brasil, cobrindo a cadeia funcional: **levantamento de cargas → cálculo de demanda → escolha de categoria de padrão de entrada → divisão de circuitos → dimensionamento de condutores → proteção → geração de laudo técnico**. Toda configuração normativa deve ser carregada como dado rastreável, nunca hardcoded no código.

Este contexto é **apenas orientativo**. Não assuma nada como verdade estabelecida — confirme cada afirmação inspecionando o repositório real antes de incluí-la no relatório.

## OBJETIVOS DA AUDITORIA

1. **Avaliar a efetividade e a eficácia da aplicação profissional do sistema**, considerando exclusivamente os módulos até aqui implementados — isto é, determinar se, no estado atual, o sistema é confiável e apto para uso real por um engenheiro eletricista em projetos que serão submetidos à distribuidora e/ou a órgãos de fiscalização.
   - **Efetividade**: o sistema cumpre o propósito para o qual foi construído, dentro do escopo já implementado?
   - **Eficácia**: com que qualidade, robustez, precisão normativa e ausência de defeitos esse propósito é cumprido?
2. **Sugerir quais devem ser os próximos módulos a implementar**, com base nas lacunas identificadas na auditoria e na cadeia funcional completa declarada do sistema.

## METODOLOGIA OBRIGATÓRIA

A auditoria deve ser fundamentada em evidência de código, nunca em suposição. No mínimo, execute:

1. **Mapeamento estrutural** — explore a árvore de diretórios (backend e frontend) e produza um inventário real dos módulos existentes.
2. **Leitura de código-fonte** — para cada módulo implementado, leia os arquivos relevantes (models, schemas, services, rotas de API, componentes de UI) e valide se a lógica confere com a norma técnica aplicável.
3. **Rastreabilidade normativa** — verifique se valores normativos (fatores de demanda, categorias, seções de condutores etc.) estão em configuração externa rastreável ou hardcoded.
4. **Cobertura de testes** — verifique existência e abrangência real de testes automatizados (unitários/integração) para os módulos implementados.
5. **Consistência entre módulos** — verifique se diferentes módulos tratam as mesmas grandezas (ex.: VA vs. W, tensão, corrente) de forma consistente entre si.
6. **Qualidade de interface** — avalie a aderência da UI ao Carbon Design System e a requisitos de acessibilidade (WCAG 2.1 AA), quando houver frontend disponível para inspeção.
7. **Histórico de defeitos conhecidos** — procure evidências no próprio código (comentários, TODOs, flags, testes falhando) de inconsistências não resolvidas.
8. **Ciclo funcional completo** — compare os módulos implementados contra a cadeia funcional declarada para identificar lacunas remanescentes.

Sempre que possível, execute comandos de terminal (busca por padrões, contagem de ocorrências, listagem de estrutura, execução de suíte de testes, se configurada) para fundamentar as conclusões com evidência reprodutível — não apenas leitura visual de arquivos.

## CRITÉRIOS DE AVALIAÇÃO

Para cada módulo implementado, produza uma avaliação estruturada contendo:

- Nome do módulo e escopo funcional
- Nota de **efetividade** (0–10): atende ao propósito de uso profissional real?
- Nota de **eficácia** (0–10): qualidade/robustez/precisão da implementação
- Evidências específicas (arquivo + trecho/linha) que sustentam cada nota
- Riscos identificados para uso em projeto real (o que pode gerar erro de projeto, retrabalho ou reprovação pela distribuidora)

Ao final, produza:

- Nota consolidada de efetividade e eficácia para o **escopo implementado**
- Nota separada considerando o **sistema completo declarado** (implementado + não implementado), para dimensionar o gap total

## ESCOPO DA SUGESTÃO DE PRÓXIMOS MÓDULOS

Ao sugerir os próximos módulos a implementar:

- Baseie-se no gap real identificado entre a cadeia funcional completa e o que está implementado.
- Priorize por criticidade para a validade técnica/normativa do projeto elétrico final (um módulo que bloqueia a emissão de um laudo tecnicamente correto tem prioridade sobre um módulo cosmético).
- Justifique, para cada módulo sugerido, por que ele deve vir antes ou depois dos demais.
- **Não detalhe a implementação técnica** dos módulos sugeridos — sem pseudocódigo, sem especificação de API, sem schema. Apenas nomeie, justifique tecnicamente e priorize. O detalhamento de implementação de cada módulo será objeto de um prompt específico posterior.

## RESTRIÇÕES (NÃO TOCAR)

- Não altere nenhum arquivo do repositório.
- Não escreva código de produção, migração ou configuração.
- Não implemente nenhuma correção, mesmo que a solução pareça óbvia — apenas relate o achado.
- Não invente valores normativos: qualquer lacuna normativa não confirmável deve ser registrada como `[VERIFICAR]`.
- Não avalie módulos explicitamente fora do escopo de engenharia do sistema (ex.: billing, autenticação de plataforma) a menos que impactem diretamente a efetividade/eficácia da aplicação profissional.

## ENTREGÁVEL FINAL (OBRIGATÓRIO)

Ao final da auditoria, gere **um único arquivo Markdown (.md) completo e autocontido**, salvo no diretório de saída do ambiente, contendo:

1. **Sumário executivo** — achados principais em poucos parágrafos, nota consolidada
2. **Metodologia aplicada** — o que foi inspecionado, quais comandos/ferramentas foram usados
3. **Inventário de módulos** — implementados vs. não implementados, mapeados contra a cadeia funcional completa
4. **Avaliação módulo a módulo** — efetividade, eficácia, evidências, riscos (conforme critérios acima)
5. **Nota consolidada** — escopo implementado vs. sistema completo declarado
6. **Riscos consolidados para uso profissional real** — o que impediria hoje o uso do sistema em um projeto real submetido à distribuidora
7. **Roadmap sugerido de próximos módulos** — priorizado e justificado, sem detalhamento de implementação
8. **Lacunas normativas pendentes** — todos os pontos marcados como `[VERIFICAR]` encontrados durante a auditoria
9. **Anexos** (se aplicável) — lista de arquivos inspecionados, comandos executados

O relatório deve ser tecnicamente denso, direto, sem enchimento de texto, e usar tabelas sempre que a informação for tabulável (notas por módulo, lacunas normativas, roadmap priorizado).
