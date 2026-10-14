# Story SIE-UX-01: Padronização dos headers de página do SIE

## Complemento solicitado pelo usuário — tabela de circuitos em Correntes

- [x] Apresentar os circuitos em tabela semântica com colunas distintas para circuito/tipo, status, potência, tensão, ligação, IB, fases, rastreio e acesso ao detalhe.
- [x] Preservar todos os dados apresentados pelos cards originais e o modal de detalhes/rastreabilidade, sem mudar regras de cálculo ou contratos.
- [x] Garantir leitura responsiva sem ocultar colunas: rolagem horizontal focável em largura estreita e cabeçalhos destacados.
- [x] Atualizar o VRT focado de Correntes para a composição aprovada (7 testes passando).
- [ ] Executar os gates globais restantes: `npm run typecheck` e `npm run lint` excederam 90 s sem diagnóstico; `npm test` não foi iniciado separadamente após esses bloqueios.

**Arquivos deste complemento:** `src/routes/projetos.$projetoId_.correntes.tsx`, `src/styles.css`, `tests/ui/correntes-rastreabilidade.vrt.test.tsx` e seu snapshot.

## Status

InProgress

## Executor Assignment

executor: "@ux-design-expert"
quality_gate: "@dev"
quality_gate_tools: ["npm run lint", "npm run typecheck", "npm test", "npm run build:spa"]

## Story

**As a** projetista que navega entre os módulos do SIE,  
**I want** encontrar um header de página consistente em todas as seções,  
**so that** eu reconheça o contexto, as ações e a identidade visual do sistema sem precisar reaprender cada módulo.

## Contexto e origem

Esta story foi criada por solicitação direta do usuário a partir de [`docs/ux/PLANO-PADRONIZACAO-HEADERS-SIE.md`](../ux/PLANO-PADRONIZACAO-HEADERS-SIE.md). Não há épico ou item ClickUp associado no estado atual do repositório; a rastreabilidade local desta story é a fonte autorizada para o trabalho.

## Acceptance Criteria

1. Um organismo reutilizável de header de página, denominado provisoriamente `SiePageHero`, existe e é usado pelas rotas migradas.
2. O hero segue a referência `C:\Users\User\Downloads\Screenshot_234.jpg`: breadcrumb discreto, eyebrow opcional, `h1`, descrição e trilho de ações/metadados.
3. As páginas Dependências, Padrão de entrada, Correntes, Dimensionamento de condutores, Unifilar interativo, Diagrama unifilar, Queda de tensão, Planejador de circuitos e Projetos possuem headers padronizados conforme suas variantes documentadas.
4. Cada rota migrada possui somente um `h1`; cabeçalhos de cards e workspaces permanecem `h2` ou inferiores.
5. A tipografia dos headers usa `var(--sie-font-sans)`; `var(--sie-font-mono)` fica restrita a IDs, números e dados técnicos.
6. Cores, bordas, gradientes, raio e tipografia do hero são consumidos por tokens/estilos centralizados; rotas migradas não mantêm valores visuais inline equivalentes.
7. Breadcrumbs, links de retorno e ações não são duplicados; ações existentes preservam nome, disponibilidade e comportamento.
8. Em larguras menores que 960px, conteúdo e ações do header são apresentados em coluna sem perda de acesso às ações.
9. Contraste, semântica de headings e navegação por teclado atendem WCAG AA para o header.
10. O Command Center preserva seus headers técnicos internos e sua hierarquia atual; qualquer entrada de página adicionada não cria um segundo `h1`.
11. Testes de componente/renderização e snapshots visuais relevantes são atualizados somente para o padrão aprovado, e os quality gates definidos pela story passam.

## CodeRabbit Integration

### Story Type Analysis

**Primary Type**: Frontend  
**Secondary Type(s)**: Architecture (consolidação de padrão transversal)  
**Complexity**: High — afeta um organismo reutilizável, tokens/estilos compartilhados e diversas rotas.

### Specialized Agent Assignment

**Primary Agents**:

- @ux-design-expert
- @dev

**Supporting Agents**:

- @qa
- @architect (somente se a consolidação exigir decisão arquitetural além deste plano)

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): executar `coderabbit --prompt-only -t uncommitted` antes de marcar a story como concluída.
- [ ] Pre-PR (@devops): executar `coderabbit --prompt-only --base main` antes de criar pull request.
- [ ] Pre-Deployment (@devops): não aplicável; esta story não altera infraestrutura de produção.

### Self-Healing Configuration

**Expected Self-Healing**:

- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

**Predicted Behavior**:

- CRITICAL issues: auto_fix, até duas iterações.
- HIGH issues: documentar na story para decisão subsequente.
- MEDIUM/LOW issues: não bloqueiam a conclusão; registrar como débito quando relevante.

### CodeRabbit Focus Areas

**Primary Focus**:

- WCAG 2.1 AA: HTML semântico, um único `h1`, foco e navegação por teclado.
- Responsividade e consistência de tokens, sem cores/espaçamentos visuais duplicados nas rotas.

**Secondary Focus**:

- Preservação das ações e rotas existentes.
- Ausência de regressão nos workspaces técnicos e no Command Center.

## Tasks / Subtasks

- [ ] Task 1 — Consolidar o padrão e os tokens do header (AC: 1, 2, 5, 6, 8, 9)
  - [ ] Criar o organismo `SiePageHero` e seus estilos centralizados, seguindo as regras do plano.
  - [ ] Definir variantes necessárias para módulo e índice, sem introduzir valores visuais duplicados nas rotas.
  - [ ] Criar teste de renderização que cubra `h1`, eyebrow opcional, descrição, ações e metadados.
  - [ ] Validar a adaptação responsiva abaixo de 960px.
- [ ] Task 2 — Migrar as rotas de referência e os módulos de maior divergência (AC: 2, 3, 4, 7, 9)
  - [ ] Migrar Dependências como rota piloto, preservando “Nova dependência”.
  - [ ] Migrar Queda de tensão: transformar retorno em breadcrumb, preservar Tutorial e rebaixar o título interno do alimentador a `h2` contextual.
  - [ ] Migrar Planejador de circuitos: promover o contexto de página ao hero e preservar tags, workspace e toolbar abaixo dele.
- [ ] Task 3 — Migrar os módulos técnicos restantes (AC: 3, 4, 5, 6, 7)
  - [ ] Migrar Padrão de entrada, deslocando Tutorial para ações secundárias.
  - [ ] Migrar Correntes e Dimensionamento de condutores, removendo estilos inline do hero.
  - [ ] Migrar Unifilar interativo e Diagrama unifilar, reduzindo links paralelos à navegação contextual aprovada.
  - [ ] Migrar a variante de índice da página Projetos sem remover as métricas existentes.
- [ ] Task 4 — Proteger casos especiais e remover legado (AC: 4, 6, 7, 10)
  - [ ] Revisar o Command Center habilitado, preservando headers internos e sua hierarquia de headings.
  - [ ] Remover classes e estilos de hero legados apenas quando não houver mais consumidores.
  - [ ] Atualizar testes de snapshots exclusivamente para a composição aprovada.
- [ ] Task 5 — Validar e registrar a entrega (AC: 8, 9, 11)
  - [ ] Executar lint, typecheck, testes, build SPA e testes de componente/snapshots relevantes.
  - [ ] Atualizar esta story: checkboxes, Completion Notes e File List.

## Dev Notes

### Fonte de requisitos

- O escopo, as regras visuais, a ordem de migração, riscos e critérios de aceite desta story derivam de [`docs/ux/PLANO-PADRONIZACAO-HEADERS-SIE.md`](../ux/PLANO-PADRONIZACAO-HEADERS-SIE.md).
- A referência visual canônica é `C:\Users\User\Downloads\Screenshot_234.jpg`; `Screenshot_231.jpg` e `Screenshot_232.jpg` documentam divergências de Planejador de circuitos e Queda de tensão, respectivamente.

### Contexto técnico confirmado

- `src/styles/sie-theme.css` define `--sie-font-sans`, `--sie-font-mono`, a rampa azul SIE e tokens Carbon semânticos.
- `src/styles.css` contém `.deps-hero` e `.sie-page-hero`, precedentes do padrão a consolidar.
- `src/components/app/sie-shell/SieShell.tsx` já fornece breadcrumb contextual no shell; a implementação deve evitar uma segunda trilha visual concorrente.
- `src/components/divisor/DivisorCircuitosWorkspace.tsx` contém o hero interno do Planejador; o workspace, suas tags e toolbar devem continuar disponíveis após a migração.
- `src/routes/projetos.$projetoId_.queda-tensao.tsx` e `src/components/app/queda-tensao/PainelAlimentador.tsx` concentram a navegação externa e o título interno da Queda de tensão.
- `src/components/command-center/ContextHeader.tsx` possui testes que protegem a hierarquia de headings; não reintroduzir `h1` duplicado no Command Center.

### Limites técnicos

- Não alterar cálculos, APIs, domínio, permissões, feature flags ou fluxos funcionais.
- Não eliminar informações operacionais/técnicas existentes dos workspaces.
- Não mudar nomes, handlers ou disponibilidade de ações já existentes sem requisito adicional.

### Testing

- Criar/atualizar testes unitários de renderização do organismo e suas variantes.
- Verificar explicitamente um único `h1` por rota migrada e títulos internos em nível inferior.
- Atualizar snapshots visuais relevantes somente após validação do padrão canônico.
- Executar os quality gates do repositório: `npm run lint`, `npm run typecheck`, `npm test` e `npm run build:spa`.

### Project Structure Notes

- O plano lista as rotas e estilos afetados; a File List abaixo deverá conter apenas os arquivos efetivamente alterados na implementação.
- Não foi localizado um épico de PRD específico para esta solicitação. A autorização do usuário e o plano UX são a origem documentada da story local.

## Change Log

| Date | Version | Description | Author |
|---|---:|---|---|
| 2026-08-02 | 0.1.0 | Story criada a partir do plano de padronização de headers aprovado pelo usuário. | @sm/River |
| 2026-08-03 | 0.2.0 | Validação PO em modo YOLO: GO para implementação local; status avançado para InProgress. | @po/Pax |

## Dev Agent Record

### Agent Model Used

_A preencher durante a implementação._

### Debug Log References

- 2026-08-03 — `npm run typecheck` iniciado no app e interrompido após exceder o tempo normal sem diagnóstico.
- 2026-08-03 — `npm run build:spa` iniciado no app e interrompido após exceder o tempo normal sem diagnóstico.

### Completion Notes List

- Implementação iniciada em modo YOLO após validação PO (GO).
- Criado `SiePageHero` e aplicada a rota-piloto Dependências; Planejador de circuitos e Queda de tensão passaram a expor header de página compartilhado.
- A migração completa e a validação dos gates permanecem pendentes porque os comandos de verificação ficaram sem saída no ambiente.
- Retomada SDC YOLO: `SiePageHero` recebeu variante `index` e trilhos separados de ações/metadados; Padrão de entrada, Correntes, Dimensionamento, Unifilar interativo, Diagrama unifilar e Projetos foram migrados.
- Teste focado `SiePageHero.test.tsx` passou (2 testes). Os gates globais permanecem pendentes por timeout sem diagnóstico; não marcar a story como concluída.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/SiePageHero.tsx` (novo)
- `sistema-de-instala-es-el-tricas-sie-main/src/styles.css` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.circuitos.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.padrao-entrada.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.correntes.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.unifilar.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.unifilar-diagrama.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/index.tsx` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/components/divisor/divisor-workspace.css` (modificado)
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/SiePageHero.test.tsx` (novo)

## QA Results

### QA Review — 2026-08-03

**Gate Decision:** FAIL  
**Scope:** revisão documental da SIE-UX-01 e das evidências registradas no Dev Agent Record.  
**Reason:** a story permanece em implementação parcial e não possui evidência válida dos gates obrigatórios.

| Área | Resultado | Evidência / achado |
|---|---|---|
| AC1 — organismo reutilizável | PARTIAL | `SiePageHero` foi criado e aplicado à rota-piloto Dependências. |
| AC2, AC5, AC8, AC9 — padrão visual, fonte, responsividade e a11y | CONCERNS | Estilos centralizados foram iniciados, mas não há testes de renderização, contraste, foco ou viewport menor que 960px. |
| AC3, AC6, AC7 — migração e remoção de duplicidade | FAIL | As migrações de Padrão de entrada, Correntes, Dimensionamento, Unifilar, Diagrama e Projetos não foram concluídas nem evidenciadas. |
| AC4 — hierarquia de headings | CONCERNS | Não há inventário/teste confirmando um único `h1` por rota migrada; o Planejador mantém contexto interno a revisar. |
| AC10 — Command Center | CONCERNS | Nenhuma evidência de revisão com a feature habilitada foi registrada. |
| AC11 — testes e gates | FAIL | `npm run typecheck` e `npm run build:spa` foram interrompidos sem resultado; lint, testes, snapshots e CodeRabbit não foram concluídos. |

### Correções necessárias antes de nova revisão

1. Concluir todas as rotas previstas nos ACs, removendo estilos inline/duplicações de header conforme a matriz da story.
2. Criar testes para `SiePageHero` e validar a hierarquia de headings das rotas migradas.
3. Executar e registrar `npm run lint`, `npm run typecheck`, `npm test`, `npm run build:spa` e a revisão CodeRabbit.
4. Verificar responsividade e WCAG AA, incluindo foco por teclado e contraste, em evidência reproduzível.
5. Revisar o Command Center com a feature habilitada e registrar que não há segundo `h1`.

**Reteste:** necessário após as correções acima. Nenhuma operação de publicação é recomendada neste estado.

### QA Review — 2026-08-03 (retomada SDC YOLO)

**Gate Decision:** FAIL  
**Scope:** revisão da retomada de implementação e das evidências locais disponíveis.  
**Reason:** a migração de código avançou, mas os gates globais obrigatórios não produziram resultado concluído e CodeRabbit não foi executado.

| Área | Resultado | Evidência / achado |
|---|---|---|
| AC1, AC2, AC3, AC5 | PASS parcial | `SiePageHero` foi estendido com variantes e aplicado às nove rotas previstas. |
| AC4, AC7, AC10 | CONCERNS | Breadcrumbs de rota foram removidos em favor do shell; o Planejador preserva tags, mas o hero interno legado ainda existe como estrutura técnica. O Command Center preserva `ContextHeader` e seus testes existentes, sem nova entrada de página. |
| AC6, AC8, AC9 | CONCERNS | Estilos do organismo estão centralizados e possuem regra responsiva a 960px, porém não há evidência de inspeção visual, contraste ou foco reproduzível. |
| AC11 | FAIL | `SiePageHero.test.tsx`: 2 testes passaram. `npm run typecheck`, `npm run lint` e lint limitado aos arquivos alterados excederam 60s sem diagnóstico; `npm test` completo, `npm run build:spa` e CodeRabbit permanecem pendentes. |

### Correções necessárias antes de nova revisão

1. Obter resultado conclusivo e registrar `npm run lint`, `npm run typecheck`, `npm test`, `npm run build:spa` e CodeRabbit.
2. Registrar inspeção de viewport menor que 960px, foco por teclado e contraste WCAG AA.
3. Remover ou converter a estrutura visual legada remanescente do Planejador quando não houver consumidores.

**Reteste:** necessário. A story permanece `InProgress`; publicação não autorizada.

## Story Draft Validation

**Readiness:** READY  
**Clarity score:** 9/10  
**Validation scope:** checklist de draft aplicada à story e ao plano UX de origem.

| Category | Status | Notes |
|---|---|---|
| Goal & Context Clarity | PASS | Objetivo, benefício, limites e origem local estão explícitos. |
| Technical Implementation Guidance | PASS | Organismo, rotas, estilos, limites e tarefas são identificados. |
| Reference Effectiveness | PASS | O plano UX e as referências visuais estão apontados e resumidos. |
| Self-Containment Assessment | PASS | Critérios, riscos, casos especiais e decisões de preservação estão na story. |
| Testing Guidance | PASS | Testes de renderização, headings, snapshots e quality gates estão definidos. |
| CodeRabbit Integration | PASS | Tipo frontend, agentes, gates, foco e self-healing estão documentados. |

**Known limitation:** não há épico/PRD específico nem item ClickUp disponível; a origem autorizada e rastreável é o plano UX aprovado pelo usuário. Isso não impede a implementação local, mas a associação a backlog externo deve ser feita posteriormente caso seja necessária.
