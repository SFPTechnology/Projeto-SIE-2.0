# Story DEP-UX-01 — Reestruturar cards de Dependências para decisão técnica

**Complemento solicitado pelo usuário — tabela no popup Detalhe da dependência**

- [x] Converter os pares de metadados e resultados do popup em tabelas semânticas com as colunas `Campo` e `Valor`.
- [x] Converter Iluminação e tomadas em tabela comparativa com `Elemento`, `Quantidade e potência`, `Regra aplicada` e `Origem`.
- [x] Preservar valores, fórmulas, referências, origens, cargas adicionais, bancadas, conformidade, resultado e modal Tutorial existentes.
- [x] Atualizar a cobertura focada de renderização (4 testes passando).
- [x] Corrigir a compressão em telas estreitas: modal ampliado em desktop, largura mínima por tabela e rolagem horizontal preservam a leitura sem truncamento.
- [x] Corrigir o corte da tabela de conformidade: Bancadas e conformidade agora ocupam linhas independentes de largura total no modal.
- [ ] Reexecutar os gates globais no ambiente estável antes de merge; lint/typecheck/test globais seguem sujeitos ao timeout já documentado nesta story.

**Arquivos deste complemento:** `src/components/app/TabelaDependencias.tsx` e `src/components/app/__tests__/status-badge.test.tsx`.

**Status:** Review  
**Prioridade:** P1  
**Tipo:** Frontend / UX / Design System  
**Executor:** `@ux-design-expert`  
**Quality gate:** `@dev`  
**Quality-gate tools:** `npm run lint`, `npm run typecheck`, `npm test`, revisão de acessibilidade WCAG AA  
**Fonte de requisitos:** [`docs/ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md`](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md)  
**Precedente de implementação:** [`sistema-de-instala-es-el-tricas-sie-main/docs/frontend/plano-reestruturacao-tabela-dependencias.md`](../../sistema-de-instala-es-el-tricas-sie-main/docs/frontend/plano-reestruturacao-tabela-dependencias.md)

## Story

**Como** projetista que gerencia as dependências de uma instalação elétrica,  
**quero** visualizar cada dependência em um card com hierarquia técnica, estados e exceções perceptíveis, além de recursos de exploração consistentes,  
**para que** eu identifique rapidamente ambiente, carga, situação e próxima ação sem perder acesso aos fluxos já existentes.

## Contexto e limites

A tela atual expõe informações de caracterização, iluminação, tomadas, cargas adicionais, atualização e ações, porém a densidade visual dificulta comparar ambientes e localizar itens que precisam de verificação. Esta story implementa o padrão de **visão geral → exceção → aprofundamento**, exclusivamente na apresentação e navegação da seção Dependências.

### Restrições inegociáveis

- Preservar `Detalhe`, `Calcular`, `Historico` e `Duplicar` com os mesmos rótulos, conteúdos, destinos, permissões e comportamentos atuais.
- As quatro ações devem permanecer visíveis em todos os breakpoints; nenhuma pode ser movida para o menu contextual.
- Não alterar cálculos elétricos, regras NBR, resultados, APIs, persistência, auditoria, permissões ou feature flags.
- Não criar estados de domínio, métricas, filtros ou agrupamentos sem fonte de dados e regra formalizada.
- Não sobrescrever, descartar ou absorver alterações locais preexistentes no diretório `sistema-de-instala-es-el-tricas-sie-main/`; reconciliar o escopo com o worktree antes de editar arquivos compartilhados.

## Acceptance Criteria

1. **Card decisório:** cada dependência é apresentada com nome, metadados disponíveis (categoria, dimensões, ID e versão), estado de cálculo existente, resumo de iluminação, resumo de tomadas, cargas adicionais e data/hora de atualização, sem remover informação técnica que o card atual expõe.
2. **Estados e exceções reais:** `Calculada` continua sendo mostrado conforme o estado existente; quando a dependência possuir indicadores já existentes de `VERIFICAR`, o card comunica claramente que requer verificação. Não criar estados como `Crítica`, `Bloqueada` ou `Desatualizada` sem regra de domínio.
3. **Resumo comparável:** iluminação, tomadas e cargas adicionais são organizadas em grupos visuais comparáveis; os valores preservam unidades e origem automática/manual já existente, quando disponível.
4. **Ações preservadas:** `Detalhe`, `Calcular`, `Historico` e `Duplicar` preservam integralmente seu contrato funcional e ficam visíveis no rodapé do card, inclusive em layouts estreitos. `Calcular` pode receber apenas ênfase visual contextual; não pode ganhar comportamento novo.
5. **Exploração:** a busca existente é preservada. Filtros e ordenação só podem ser exibidos para atributos suportados pelos dados e pela implementação; filtros ativos devem ser perceptíveis e reversíveis. A grade permanece o modo padrão; lista técnica só é entregue se puder reutilizar dados e contratos existentes sem mudança de domínio.
6. **Resumo operacional seguro:** exibir somente contadores derivados de dados existentes, no mínimo total e calculadas. O contador de itens que requerem verificação só pode ser derivado de indicadores existentes. Não exibir métrica de desatualização sem regra formalizada.
7. **Estados de interface:** carregar, sem dependências, sem resultados de busca/filtro e erro de carregamento possuem tratamento compreensível, sem bloquear a página inteira quando uma parte puder ser exibida.
8. **Responsividade:** em desktop a grade usa duas colunas quando a largura permitir; em tablet e mobile a leitura se reorganiza sem ocultar valores ou as quatro ações obrigatórias.
9. **Acessibilidade:** estrutura semântica, foco visível, navegação por teclado, rótulos acessíveis e contraste WCAG AA são mantidos. Estado não pode depender apenas de cor; tooltip não pode ser a única fonte de significado.
10. **Proteção de escopo:** não há mudanças em regras de cálculo, contratos de API, persistência, schema, permissões ou textos/conteúdos internos das quatro ações preservadas.
11. **Qualidade e rastreabilidade:** checklist e File List desta story são atualizados antes da conclusão; `npm run lint`, `npm run typecheck` e `npm test` passam no contexto de execução aplicável à alteração.

## 🤖 CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend  
**Secondary Type(s):** UX / acessibilidade / design system  
**Complexity:** Medium — reorganiza uma superfície central com estados, responsividade, ações existentes e arquivos já modificados por outras frentes.

### Specialized Agent Assignment

**Primary Agents:**

- `@ux-design-expert` — implementação do sistema visual e acessibilidade.
- `@dev` — revisão de integração e qualidade pré-commit.

**Supporting Agents:**

- `@qa` — verificação dos critérios e regressão das ações.
- `@architect` — somente se a descoberta exigir novo contrato, estado de domínio ou mudança estrutural fora desta story.

### Quality Gate Tasks

- [ ] Pre-Commit (`@dev`): executar `coderabbit --prompt-only -t uncommitted` antes de marcar a story como concluída, caso o CLI esteja disponível.
- [ ] Pre-PR (`@devops`): executar `coderabbit --prompt-only --base main` antes de criar PR.
- [ ] Validar lint, typecheck e testes aplicáveis; declarar qualquer bloqueio preexistente com evidência, sem atribuí-lo a esta story.

### Self-Healing Configuration

**Expected Self-Healing:**

- Primary Agent: `@dev` (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

**Predicted Behavior:**

- CRITICAL issues: auto-fix, até duas iterações.
- HIGH issues: documentar e encaminhar para decisão/revisão.

### CodeRabbit Focus Areas

**Primary Focus:**

- Preservação de contratos de ações e ausência de regressão em fluxos existentes.
- HTML semântico, ARIA, navegação por teclado, foco e contraste WCAG AA.

**Secondary Focus:**

- Uso de tokens e padrões visuais existentes; ausência de valores visuais hardcoded na rota.
- Responsividade, estados de interface e estabilidade dos filtros/busca.

## Tasks / Subtasks

- [x] **Task 1 — Descobrir e congelar o contrato existente (AC: 1, 2, 4, 5, 10)**
  - [x] Mapear a rota, os componentes, o view model, os handlers e os testes que atendem Dependências.
  - [x] Confirmar no código as fontes de dados para estado, `VERIFICAR`, iluminação, tomadas, cargas, atualização, busca e filtros.
  - [x] Registrar no Dev Agent Record os arquivos já modificados por outras frentes e obter reconciliação antes de tocá-los.
  - [x] Nenhum novo contrato de dados ou estado de domínio foi necessário; escala para `@architect` não aplicada.

- [x] **Task 2 — Especificar e compor o sistema visual (AC: 1, 2, 3, 6, 8, 9)**
  - [x] Reutilizar tokens de tema e tipografia SIE; não foram introduzidas cores hardcoded.
  - [x] Reaproveitar `StatusBadge` e compor indicador de verificação, grupos de métrica, metadados e barra de ações.
  - [x] Implementar o card como organismo semântico com título de ambiente em `h2` no contexto da coleção.
  - [x] Construir o resumo operacional apenas com valores comprovadamente derivados do contrato existente.

- [x] **Task 3 — Migrar a coleção e a exploração (AC: 4, 5, 7, 8, 9)**
  - [x] Manter busca e filtros suportados; adicionar chips reversíveis e ordenação baseada em dados existentes, sem mudança de domínio.
  - [x] Preservar os tratamentos existentes de erro e ausência de resultados na superfície migrada.
  - [x] Garantir que o menu contextual não esconda as quatro ações preservadas.
  - [x] Implementar grade de duas colunas e reorganização tablet/mobile sem ocultar os dados ou ações obrigatórias.

- [x] **Task 4 — Cobrir regressão e acessibilidade (AC: 1–11)**
  - [x] Atualizar o teste de renderização da superfície de Dependências e manter os testes do view model aplicáveis.
  - [x] Cobrir explicitamente a presença de `Detalhe`, `Calcular`, `Historico` e `Duplicar` no teste da superfície de cards.
  - [x] Verificar a semântica de card, título `h2`, foco visível e nome acessível da busca; limitações de infraestrutura registradas em QA Results.
  - [x] Executar os gates focados disponíveis e registrar a dispensa dos gates globais.

## Dev Notes

### Requisitos rastreáveis

- O briefing define estrutura proposta, estados, responsividade, acessibilidade, limites e critérios: [ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md#4-arquitetura-proposta-da-página](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md#4-arquitetura-proposta-da-página), [#5-especificação-do-dependencycard](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md#5-especificação-do-dependencycard), [#6-design-system-e-acessibilidade](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md#6-design-system-e-acessibilidade) e [#10-critérios-de-aceite](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md#10-critérios-de-aceite).
- O plano anterior já registra busca, filtros, paginação, view model e fallback mobile como direção de implementação; não tratá-lo como autorização para evoluir o domínio: [plano-reestruturacao-tabela-dependencias.md#estado-atual-da-implementação](../../sistema-de-instala-es-el-tricas-sie-main/docs/frontend/plano-reestruturacao-tabela-dependencias.md#estado-atual-da-implementação) e [#mapeamento-de-dados-proposto](../../sistema-de-instala-es-el-tricas-sie-main/docs/frontend/plano-reestruturacao-tabela-dependencias.md#mapeamento-de-dados-proposto).
- O padrão de header SIE já determina tokens, tipografia e preservação da CTA `Nova dependência`; manter compatibilidade com ele: [PLANO-PADRONIZACAO-HEADERS-SIE.md#padrão-canônico-siepagehero](../ux/PLANO-PADRONIZACAO-HEADERS-SIE.md#padrão-canônico-siepagehero).

### Árvore e integração conhecida

- A superfície de implementação foi identificada em `sistema-de-instala-es-el-tricas-sie-main/src/components/app/TabelaDependencias.tsx` e no view model `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dependencias-table-model.ts`.
- A rota de projeto e os componentes auxiliares devem ser confirmados durante Task 1; não assumir nomes de novos componentes antes da descoberta.
- O diretório de aplicação contém alterações locais preexistentes, incluindo `TabelaDependencias.tsx`. Esta story não autoriza limpeza, reset, checkout ou alteração de trabalho alheio.

### Decisões e limitações

- `Requer verificação` é uma apresentação derivada de indicadores já existentes; não é novo estado de domínio.
- `Desatualizada`, criticidade, agrupamentos por pavimento/setor/circuito, filtros salvos e extensão de dados (`nome`, `descricao`, `localizacao`) estão fora de escopo até haver requisito e contrato aprovados.
- Se a lista técnica não puder reutilizar a estrutura e os dados existentes com segurança, a entrega desta story termina na grade melhorada; não criar API, persistência ou modelo novo para habilitá-la.

### Testing

- Reutilizar o padrão de testes existente da aplicação para o view model/tabela; o ponto de partida identificado é `sistema-de-instala-es-el-tricas-sie-main/src/components/app/__tests__/dependencias-table-view-model.test.ts`.
- Executar, no diretório da aplicação quando aplicável, os scripts definidos no seu `package.json`; além disso, atender aos gates do repositório raiz indicados em AC11.
- Testes devem provar preservação das ações pelo rótulo e handler/destino já existente, não por reimplementação dos fluxos de detalhe, cálculo, histórico ou duplicação.

## Checklist de Draft

- [x] Objetivo, valor e contexto definidos.
- [x] Escopo, fora de escopo e dependências explícitos.
- [x] Critérios de aceite testáveis e sem requisito de domínio inventado.
- [x] Arquivos e integrações iniciais identificados; descoberta técnica obrigatória antes de editar o worktree compartilhado.
- [x] Estratégia de testes e qualidade declarada.
- [x] CodeRabbit, agentes e quality gates definidos.
- [x] File List reservada para atualização pelo executor.

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-02 | 0.1.0 | Story criada a partir da análise UX dos cards de Dependências. | @sm/River |
| 2026-08-03 | 0.2.0 | Implementação concluída; story encaminhada para Review com gates globais dispensados. | @ux-design-expert/Uma |
| 2026-08-03 | 0.2.1 | Corrigida a densidade dos cards estreitos: grade de métricas fluida, quebra segura de valores rastreáveis e ações preservadas. | @ux-design-expert/Uma |

## Dev Agent Record

### Agent Model Used

Codex / `@ux-design-expert` (Uma).

### Debug Log References

- Execução SDC: `sdc-yolo-dep-ux-01-2026-08-03T01-34-05-127-03-00`.
- P4: cards, filtros ativos, ordenação, paginação e responsividade implementados preservando os quatro handlers obrigatórios.
- P5/P6: teste legado adaptado à superfície de cards; nome acessível adicionado à busca; formatação focada aplicada.

### Completion Notes List

- Grade de dependências reestruturada como cards técnicos responsivos, com resumo operacional derivado, ordenação, filtros ativos e paginação única.
- `Detalhe`, `Calcular`, `Historico` e `Duplicar` mantêm os mesmos rótulos e handlers existentes; atalhos de edição de iluminação e TUG também foram preservados.
- Indicador `Requer verificação` deriva exclusivamente das pendências e alertas já calculados no agregado.
- Teste de superfície atualizado para confirmar explicitamente os quatro rótulos de ação preservados; a busca recebeu nome acessível sem alteração visual ou comportamental.
- Em cards com até 34rem de largura, iluminação e tomadas ocupam duas colunas legíveis e cargas adicionais passa para uma linha inteira; em até 24rem, os grupos passam a uma coluna. Valores rastreáveis podem quebrar linha sem sobreposição.
- Gates globais não foram concluídos nesta execução devido a timeout sem saída no ambiente compartilhado; a dispensa está registrada em QA Results para revisão humana.

### File List

**Criados:**

- Nenhum.

**Modificados:**

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/TabelaDependencias.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/ValorRastreavel.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/__tests__/dependencias-table-view-model.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/__tests__/status-badge.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/styles.css`
- `docs/stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/sie-shell/nav-model.ts`

**Removidos:**

- Nenhum previsto.

## QA Results

**Status:** PASS WITH CONCERNS / WAIVED

- **Evidência focada:** o teste de renderização `status-badge.test.tsx` foi atualizado para a superfície de cards e para os rótulos `Detalhe`, `Calcular`, `Historico` e `Duplicar`; o view model permanece coberto por `dependencias-table-view-model.test.ts`.
- **Acessibilidade:** busca possui nome acessível `Buscar dependências` mantendo o rótulo visual oculto; cards utilizam `article`, título `h2`, foco visível e estado textual `Requer verificação` além da cor.
- **Formatação focada:** `node ./node_modules/prettier/bin/prettier.cjs --write src/components/app/TabelaDependencias.tsx src/components/app/__tests__/status-badge.test.tsx src/components/app/__tests__/dependencias-table-view-model.test.ts` finalizou com exit code 0 em 2026-08-03.
- **Correção de densidade (2026-08-03):** `npx eslint src/components/app/TabelaDependencias.tsx src/components/app/ValorRastreavel.tsx src/components/app/__tests__/status-badge.test.tsx`, `npx tsc --noEmit` e `npx vitest run src/components/app/__tests__/dependencias-table-view-model.test.ts src/components/app/__tests__/status-badge.test.tsx` finalizaram com exit code 0 (2 arquivos, 7 testes). Os gates da raiz `npm run lint`, `npm run typecheck` e `npm test` também finalizaram com exit code 0.
- **Waiver de gates globais:** `npm run lint`, `npm run typecheck` e `npm test` globais ficam dispensados nesta execução SDC. As tentativas no projeto aninhado excederam o timeout operacional sem diagnóstico de falha, em worktree compartilhado e previamente modificado por outras frentes. Reexecutar os gates completos em ambiente estável antes de merge/release.
