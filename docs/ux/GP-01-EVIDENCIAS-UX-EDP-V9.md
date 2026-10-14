# GP-01 — Evidências UX para o Padrão Compatível EDP V9

**Documento avaliado:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Versão avaliada:** 0.8 (`InReview`)  
**Data:** 2026-07-26  
**Responsável pela evidência UX:** Uma (`@ux-design-expert`)  
**Aprovador requerido pelo PRD:** `@po`  
**Escopo deste artefato:** GP-01.1 e GP-01.4; acessibilidade e dispositivos como dependências da jornada  
**Modo:** evidência brownfield, sem implementação de UI

## 1. Decisão executiva

| Item | Estado | Decisão |
|---|---|---|
| GP-01.1 — persona, papéis e jornada | `PENDENTE` | Os papéis e a jornada afetada podem ser documentados a partir do PRD e do código, mas não existe pesquisa que identifique e valide a persona primária nem aprovação PO das responsabilidades. |
| GP-01.4 — baselines e metas UX | `PENDENTE` | As cinco métricas exigidas estão operacionalmente definidas abaixo, mas não há baseline capturado, pesquisa de compreensão, telemetria do fluxo ou metas aprovadas. |

Esta evidência **não aprova GP-01** e não libera o pacote 6 nem a Release 1. O bloqueio segue AC-36 e a seção 2.4.1 do PRD.

## 2. Fontes verificadas

- PRD V9 integral: `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`.
- Plano funcional, especialmente findings F-02/F-03 e seções 7 e 8: `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`.
- Story histórica preservada: `docs/stories/story-FORNECIMENTO-SELECAO-01.md`.
- Implementação atual do campo: `sistema-de-instala-es-el-tricas-sie-main/src/components/app/FornecimentoSelector.tsx`.
- Rota afetada: `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.padrao-entrada.tsx`.
- Shell e idioma da aplicação: `sistema-de-instala-es-el-tricas-sie-main/src/components/app/AppShell.tsx` e `sistema-de-instala-es-el-tricas-sie-main/src/routes/__root.tsx`.
- Evidências UX existentes: `sistema-de-instala-es-el-tricas-sie-main/docs/ACCESSIBILITY-AUDIT.md`, `docs/frontend/frontend-spec.md` e `docs/reviews/ux-specialist-review.md`.
- Parecer PO corrente: `docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md`.

## 3. GP-01.1 — Persona, papéis e jornada

### 3.1 Persona primária

**Estado:** `TBD — pesquisa e aprovação @po`.

Os artefatos não comprovam quem é a pessoa primária, seu contexto de uso, experiência técnica, frequência da tarefa, necessidades de acessibilidade ou dispositivo principal. O texto “projetista”, usado como autor padrão no shell, é um rótulo operacional do sistema e **não constitui persona validada**.

Não há evidência para afirmar se operador, cliente solicitante e responsável técnico são a mesma pessoa. Nenhuma autoridade técnica ou regulatória deve ser atribuída ao operador por inferência.

### 3.2 Papéis sustentados pelos requisitos

| Papel | Evidência verificável | Limite atual |
|---|---|---|
| Operador da interface | A rota permite consultar o resultado, escolher um item e acionar “Salvar e recalcular”; o shell registra texto livre em “Autor atual”. | Identidade, perfil autorizado, formação e relação com os demais papéis não estão validados. O texto livre não comprova autenticação nem autoridade. |
| Cliente solicitante | FR9 e o plano distinguem intenção do cliente, categoria mínima e categoria superior solicitada. | Não há representação validada do cliente na UI atual nem decisão aprovada em DP-04. |
| Responsável técnico | O PRD preserva ratificações e aprovações técnicas fora da autoridade do operador e do próprio produto. | Identidade, momento de intervenção, evidência de aceite e relação com o operador permanecem `TBD`. |

**Responsabilidades e segregação:** `TBD — DP-04, DP-07, GP-01.3 e aprovação @po/@architect`. Esta seção descreve papéis, mas não substitui a matriz de perfis e ações privilegiadas.

### 3.3 Jornada atual comprovada no código

1. O operador acessa “Padrão de entrada” a partir do projeto.
2. A página carrega o resultado do padrão e os cards EDP.
3. `FornecimentoSelector` monta as opções a partir de `estado.config.catalogo`.
4. Quando `resultado.status === "ok"`, os IDs de `candidatosValidos` habilitam opções.
5. Quando o resultado não é `ok`, inclusive em `sem-padrao`, o conjunto de IDs válidos fica vazio.
6. Todas as opções do catálogo ficam desabilitadas; a notificação informa a pendência, mas não oferece uma próxima ação capaz de resolvê-la no próprio fluxo.
7. Um valor válido pode ser salvo e dispara invalidação/recarregamento de Padrão de entrada, Correntes e Dimensionamento.

**Evidência de problema:** existe um caminho determinístico de dead-end no código. Isso comprova a existência do defeito, mas não mede sua frequência entre usuários.

### 3.4 Jornada-alvo derivada do PRD

1. Informar ou confirmar distribuidora/área, tipo de rede, topologia/tensões e entradas obrigatórias.
2. Avaliar pelo domínio EDP todas as alternativas e seus motivos.
3. Apresentar, para cada alternativa, estado, motivo, topologia, tensões, categoria e subcategoria disponível.
4. Distinguir categoria mínima, alternativa elegível por solicitação, intenção do cliente e confirmação da concessionária.
5. Se faltarem dados ou o caso estiver fora de escopo/em estudo, apresentar pendência e próxima ação; nunca uma lista silenciosamente inutilizável.
6. Impedir salvamento incompatível ou obsoleto no cliente e no servidor.
7. Após decisão válida, recalcular e comunicar explicitamente os impactos nos consumidores downstream.

Esta é uma jornada de requisitos, não uma jornada validada com usuários. Linguagem, ordem, compreensão, pontos de decisão e necessidades de ajuda ainda requerem teste.

### 3.5 Lacunas que impedem aprovar GP-01.1

- Persona primária e contexto de uso real.
- Confirmação de quem exerce cada papel e se há acumulação de papéis.
- Objetivos, dores, frequência e criticidade da tarefa validados com usuários.
- Autoridade e handoff entre operador, cliente e responsável técnico.
- Validação de compreensão para “determinado”, “elegível por solicitação”, “requer estudo”, “pendente”, “obsoleto” e “fora de escopo”.
- Aprovação PO da persona, papéis, responsabilidades e jornada.

**Conclusão GP-01.1:** `PENDENTE`.

## 4. Acessibilidade e compatibilidade de dispositivos

### 4.1 Evidência existente

- A aplicação declara `lang="pt-BR"` e viewport responsivo no root atual.
- A rota usa estrutura semântica básica (`nav`, `header`, `section`, headings) e componentes Carbon para seleção, botão e notificações.
- O seletor usa labels visíveis e flex wrapping, mas mantém largura mínima de 300 px no campo.
- A auditoria rápida de 2026-07-05 declara WCAG 2.1 AA, porém registra como pendentes testes completos de teclado, leitor de tela, zoom, mobile e automação.
- A revisão UX brownfield identifica ausência de anúncio confiável para feedback assíncrono e lacunas históricas de responsividade. Não foi localizada suíte automatizada de acessibilidade específica para o fluxo de Padrão de entrada.

### 4.2 Decisão de evidência

O piso documental existente é **WCAG 2.1 AA**, mas a auditoria histórica e genérica não comprova conformidade do fluxo EDP V9 reestruturado. A adoção de Carbon reduz risco, porém não substitui testes do comportamento composto.

| Dimensão | Estado | Condição antes do pacote 6 |
|---|---|---|
| Teclado, foco e ordem de navegação | `TBD — teste` | Exercitar toda a jornada, inclusive estados pendentes, confirmação e erro. |
| Leitor de tela e mensagens assíncronas | `TBD — teste` | Comprovar anúncio de avaliação, salvamento, recálculo, erro, obsolescência e bloqueio. |
| Contraste, zoom e reflow | `TBD — teste` | Validar todos os estados e textos técnicos no tema efetivo. |
| Desktop, tablet e celular | `TBD — decisão de produto e teste` | Definir matriz de dispositivos a partir da pesquisa de contexto; depois testar sem perda de informação ou ação. |
| Linguagem e carga cognitiva | `TBD — teste com usuários` | Validar compreensão de estados, motivos, próxima ação e distinção entre solicitação e aprovação. |

Não há evidência para declarar um dispositivo primário ou compatibilidade integral em qualquer classe de dispositivo.

## 5. GP-01.4 — Baselines e metas UX

### 5.1 Matriz operacional

| Métrica exigida pelo PRD | Definição operacional proposta | Baseline atual | Meta | Evidência necessária |
|---|---|---|---|---|
| Taxa de dead-end do seletor | Proporção de jornadas que chegam ao seletor e não oferecem ação válida nem próxima ação resolutiva. | `TBD — sem telemetria`. Há evidência qualitativa de um caminho determinístico em `sem-padrao`. | `TBD — aprovação @po/@ux`. O PRD exige eliminar o dead-end conhecido, mas não aprova uma meta percentual de uso real. | Eventos de visualização, estado apresentado, ações disponíveis e resolução; baseline anterior à implementação. |
| Tempo para resolver pendência | Tempo entre a primeira apresentação de uma pendência e uma decisão válida ou encaminhamento explícito para estudo/fora de escopo. | `TBD — sem instrumentação longitudinal`. | `TBD — aprovação @po/@ux`. | Definir início/fim, tratamento de retorno em outra sessão e segmentação por estado; medir baseline. |
| Compreensão de estados e motivos | Proporção de participantes que identifica corretamente estado, causa, consequência e próxima ação em teste de tarefa. | `TBD — sem pesquisa de compreensão`. | `TBD — aprovação @po/@ux`. | Roteiro e amostra aprovados, teste com usuários representativos e critérios de resposta definidos antes da coleta. |
| Abandono do fluxo | Proporção de jornadas iniciadas no Padrão de entrada que terminam sem decisão ou encaminhamento, conforme uma janela de análise aprovada. | `TBD — sem analytics e sem janela definida`. | `TBD — aprovação @po/@ux`. | Taxonomia de início, conclusão e saída; janela e exclusões aprovadas; baseline segmentado por estado/dispositivo. |
| Solicitações de suporte | Volume e proporção de contatos classificados como Padrão de entrada EDP, por motivo e período. | `TBD — fonte/taxonomia de suporte não documentadas`. | `TBD — aprovação @po/@ux`. | Fonte de suporte, taxonomia, período, deduplicação e baseline aprovados. |

### 5.2 Guardrails já aprovados no PRD, sem substituir GP-01.4

- Candidatos exibidos sem estado e motivo: meta estrutural `0`.
- Candidatos incompatíveis não podem ser salvos.
- Estados de estudo, pendência e fora de escopo devem ter motivo e próxima ação.
- CLI, API e UI devem apresentar estados e motivos equivalentes para a mesma fixture.

Esses critérios verificam integridade do produto. Eles não substituem baselines de comportamento nem metas de compreensão, tempo, abandono ou suporte.

### 5.3 Protocolo mínimo para encerrar GP-01.4

1. Aprovar definições, eventos, fonte de dados, segmentações e período de observação.
2. Capturar o baseline do fluxo atual antes da implementação do pacote 6.
3. Realizar pesquisa de compreensão com usuários que representem a persona aprovada em GP-01.1.
4. Propor metas com base nos dados coletados, registrando amostra, período e limitações.
5. Obter aprovação explícita de `@po` e `@ux`.

**Conclusão GP-01.4:** `PENDENTE`.

## 6. Registro de aprovação e validade

| Item | Evidência UX | Aprovação PO | Estado final |
|---|---|---|---|
| GP-01.1 | Documento parcial concluído; persona e validação real ausentes | `TBD` | `PENDENTE` |
| GP-01.4 | Definições concluídas; baselines e metas ausentes | `TBD` | `PENDENTE` |

Revalidar este artefato quando houver mudança de persona, papéis, jornada, dispositivos suportados, linguagem de estados, instrumentação ou metas, conforme a matriz de validade do PRD.

---

— Uma, desenhando com empatia
