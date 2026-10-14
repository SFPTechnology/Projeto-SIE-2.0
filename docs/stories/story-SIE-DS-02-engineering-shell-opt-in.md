# Story SIE-DS-02 — Engineering Shell opt-in (nav lateral, cabeçalho global, paleta de comandos)

**Workflow-fonte:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS02-LOCAL-YOLO.md`
**Ratificações reutilizadas:** `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md`, `docs/stories/story-SIE-DS-LOCAL-01-fundacao-preview-local.md`
**Status:** **Done**
**Created:** 2026-07-31
**Priority:** P1 (item canônico SIE-DS-02 do backlog-semente)

---

## 📖 Descrição

**Como** avaliador do SIE Command Center que já validou a fundação local (`SIE-DS-LOCAL-01`),
**eu quero** que a rota de preview mostre a navegação lateral, o cabeçalho global e a paleta de comandos reais do design system,
**para que** a avaliação de UX seja feita contra o shell completo, não apenas o placeholder mínimo entregue anteriormente.

Esta story implementa o item canônico `SIE-DS-02` do backlog-semente (`docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §8), escopado para execução **local-only** (sem push/PR/deploy) por decisão explícita do usuário nesta sessão.

---

## ✅ Acceptance Criteria

- [ ] **AC1 — Navegação lateral (`ModuleNavigation`):** `src/components/command-center/ModuleNavigation.tsx` existe, renderiza os 4 grupos definidos em `experience-architecture.md` §2 (Workspace, Entrada, Dimensionamento, Documentação) com os itens exatos do protótipo (`prototype/index.html` linhas 26-85), marca/lockup, item ativo destacável, e colapsa para um estado de drawer quando a viewport é `< 992px` (verificável via CSS `@media` ou classe condicional testável).
- [ ] **AC2 — Cabeçalho global expandido:** o header do `EngineeringShell` passa a incluir: seletor de projeto (ilustrativo, sem lógica real de troca), indicador de estado/sincronização (`role="status"`), botão de busca/paleta que abre o `CommandPalette` (AC3), alternância de densidade (`comfortable`/`compact`), botão de autor (ilustrativo).
- [ ] **AC3 — Paleta de comandos (`CommandPalette`):** `src/components/command-center/CommandPalette.tsx` existe, usa `<dialog>` nativo, abre via clique no gatilho do header **e** via atalho `Ctrl/Cmd+K`, filtra uma lista estática de comandos ilustrativos por texto digitado, navegação por teclado (`↑`/`↓` movem seleção, `Enter` seleciona, `Esc` fecha).
- [ ] **AC4 — Densidade:** atributo `data-density="comfortable"|"compact"` aplicado no elemento raiz do shell, alternável pelo botão do AC2, usando os tokens de densidade portados de `sie-premium.css` (`--sie-cc-control-height`, `--sie-cc-row-height`, `--sie-cc-panel-gap`) — ainda não existentes em `sie-cc-tokens.css` (portar nesta story).
- [ ] **AC5 — `EngineeringShell` reestruturado:** o shell passa do layout linear (header/nav/main empilhados, entregue em `SIE-DS-LOCAL-01`) para o layout `aside` (nav lateral) + `content-shell` (header global + main), consumido pela rota `src/routes/sie-command-center-preview.tsx` já existente, sem quebrar o gate da feature flag já implementado (`isCommandCenterPreviewEnabled`).
- [ ] **AC6 — Acessibilidade:** toda a navegação lateral e a paleta de comandos são operáveis 100% por teclado; foco visível em todos os elementos interativos novos; `aria-label`/`aria-current`/`role` corretos (seguindo os padrões já usados no protótipo); `prefers-reduced-motion` respeitado nas transições novas (drawer, dialog).
- [ ] **AC7 — Zero impacto no legado:** `AppShell.tsx` e todas as rotas de produção existentes permanecem com `git diff` vazio. Nenhuma operação remota (push/PR/merge/deploy) é executada por esta story.
- [ ] **AC8 — Testado localmente:** lint, typecheck, suíte completa de testes e build do frontend passam. Testes automatizados cobrem `ModuleNavigation`, `CommandPalette`, a lógica de densidade e a reestruturação do `EngineeringShell`.

---

## 📝 Scope

### IN Scope
- `ModuleNavigation`, `CommandPalette`, alternância de densidade, cabeçalho global expandido, reestruturação do `EngineeringShell` para o layout de duas colunas.

### OUT Scope
- ❌ Cabeçalho contextual (breadcrumb, título de página) — `SIE-DS-03`;
- ❌ Conteúdo real de módulos, inspector panel — `SIE-DS-03` a `SIE-DS-06`;
- ❌ Dados reais de projeto;
- ❌ Qualquer alteração em `AppShell.tsx` ou rotas de produção;
- ❌ Qualquer operação remota (push/PR/merge/release/deploy) — decisão separada e posterior.

---

## 🗂️ File List (planejado)

**A serem criados nesta story:**
- `src/components/command-center/ModuleNavigation.tsx`
- `src/components/command-center/ModuleNavigation.css`
- `src/components/command-center/ModuleNavigation.test.tsx`
- `src/components/command-center/CommandPalette.tsx`
- `src/components/command-center/CommandPalette.css`
- `src/components/command-center/CommandPalette.test.tsx`
- `src/components/command-center/use-density.ts` (hook de estado de densidade, testável isoladamente)
- `src/components/command-center/use-density.test.ts`

**A serem modificados nesta story:**
- `src/components/command-center/EngineeringShell.tsx` (reestruturação para layout de duas colunas + integração da nav lateral, cabeçalho expandido e paleta)
- `src/components/command-center/EngineeringShell.css` (novo layout)
- `src/components/command-center/EngineeringShell.test.tsx` (testes ajustados à nova estrutura)
- `src/components/command-center/tokens/sie-cc-tokens.css` (portar tokens de densidade)
- `src/components/command-center/tokens/sie-cc-tokens.test.ts` (testes dos novos tokens)

**Explicitamente não tocados (AC7):**
- `src/components/app/AppShell.tsx`, todas as rotas de produção existentes.

---

## 🤖 CodeRabbit Integration

### Story Type Analysis
**Primary Type**: Frontend (componentes interativos novos)
**Complexity**: High — 3 organisms novos, gerenciamento de estado (paleta aberta/fechada, densidade, item ativo), interação por teclado, responsividade.

### Specialized Agent Assignment
**Primary Agents**: @dev
**Supporting Agents**: @architect (composição e padrões de interação)

### Quality Gate Tasks
- [ ] Pre-Commit (@dev): lint + typecheck + testes antes de fechar a story
- [ ] Pre-PR / Pre-Deployment: não aplicável — nenhuma operação remota nesta story

### Self-Healing Configuration
Mesma nota de `SIE-DS-00`/`SIE-DS-LOCAL-01`: CodeRabbit local segue indisponível (SIGILL/exit 132) — compensado por lint/typecheck/test/build reais + revisão manual de `@qa`.

---

## 📌 Tarefas de Desenvolvimento

### Task 1: Portar tokens de densidade (AC4)
- [ ] Adicionar `--sie-cc-control-height`, `--sie-cc-row-height`, `--sie-cc-panel-gap` (variantes `[data-density="compact"]`/`[data-density="comfortable"]`) a `sie-cc-tokens.css`
- [ ] Testes cobrindo presença dos tokens

### Task 2: Criar hook de densidade (AC4)
- [ ] `use-density.ts`: estado local (`useState`), alterna entre `comfortable`/`compact`, default `comfortable`
- [ ] Testes unitários do hook isolado (sem depender de render de componente)

### Task 3: Criar ModuleNavigation (AC1, AC6)
- [ ] Grupos e itens do protótipo, semântica `nav > section[aria-labelledby] > button[aria-current]`
- [ ] Colapso para drawer < 992px via CSS
- [ ] Testes de render (grupos, itens, item ativo)

### Task 4: Criar CommandPalette (AC3, AC6)
- [ ] `<dialog>` nativo, abre/fecha via prop controlada + atalho de teclado
- [ ] Filtro de busca, navegação por seta/Enter, fechamento por Esc
- [ ] Testes de comportamento (filtro, navegação, fechamento)

### Task 5: Expandir cabeçalho global (AC2)
- [ ] Seletor de projeto, sync-state, gatilho de busca, alternância de densidade, botão de autor
- [ ] Integração com CommandPalette (abre via clique e via Ctrl/Cmd+K)

### Task 6: Reestruturar EngineeringShell (AC5)
- [ ] Layout `aside` + `content-shell`
- [ ] Integração de ModuleNavigation, cabeçalho expandido, CommandPalette
- [ ] Ajustar testes existentes de EngineeringShell à nova estrutura

### Task 7: Validações finais (AC7, AC8)
- [ ] `git diff` confirmando legado intocado
- [ ] lint, typecheck, suíte completa, build

---

## 📊 Dependências

- **Depende de:** `SIE-DS-LOCAL-01` (shell mínimo, rota, tokens base — já Done).
- **Bloqueia:** `SIE-DS-03` (cabeçalho contextual + conteúdo Overview) — não pode iniciar sem este shell.
- **Relacionada:** Gap 1 e Gap 4 de `docs/analysis/GAP-ANALISE-SIE-DS-LOCAL-01-vs-PROTOTIPO.md`.

## ⚠️ Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Complexidade de estado (paleta + densidade + nav ativa) introduzir bugs de interação | Médio | Testes unitários por unidade de estado (hook isolado) antes de integrar |
| Responsividade (drawer < 992px) difícil de testar sem browser real | Médio | Testes verificam a lógica/classe condicional; validação visual final via smoke test manual do usuário |
| Escopo maior que as stories anteriores pode gerar arquivos grandes demais para um ciclo | Baixo | Dividido em 7 tasks incrementais, cada uma testável isoladamente |

---

## 🏛️ Architecture Ratification (@architect)

**Ratificado por:** Aria (`@architect`) — 2026-07-31
**Veredito:** **PASS**

### Composição e estado

- **Estado de UI (paleta aberta/fechada, densidade, nav ativa) vive em `EngineeringShell`**, elevado (lifted state), e é passado por props para `ModuleNavigation`, cabeçalho e `CommandPalette` — nenhum estado global novo, nenhuma lib de state management introduzida (consistente com "Pragmatic Technology Selection").
- **`ModuleNavigation`:** dados de grupos/itens como array estático tipado dentro do próprio componente (mesmo padrão do `navItens` já usado em `SIE-DS-LOCAL-01`) — ilustrativo, sem contrato de API real (fora de escopo).
- **Colapso para drawer < 992px: CSS puro** (`@media (max-width: 991px)` em `ModuleNavigation.css`), sem JS de breakpoint. Motivo: evita layout thrashing e estado duplicado (CSS já é a fonte de verdade responsiva do projeto, ver `experience-architecture.md` §8). **Implicação de teste (resolve o Should-Fix do @po):** como o projeto não usa jsdom/testing-library, a cobertura desta AC não pode simular resize real — o teste correto é ler `ModuleNavigation.css` via `fs` (mesmo padrão de `sie-cc-tokens.test.ts`) e asserir que a regra `@media (max-width: 991px)` existe e referencia a mudança de exibição do side-rail. Isso é suficiente e correto; não é uma lacuna.
- **`CommandPalette`:** toda a lógica decisória (filtro por texto, navegação por índice com setas, seleção) deve ser **extraída para funções puras** testáveis sem DOM: `filtrarComandos(query, comandos)` e `moverSelecao(indiceAtual, direcao, total)`. O componente React apenas liga essas funções a `onKeyDown`/`onChange` — a cobertura de teste valida as funções puras, não eventos de teclado simulados (o projeto não tem `@testing-library/react` nem jsdom configurado; simular `keydown` em `renderToStaticMarkup` não é possível).
- **Densidade:** `useDensity()` hook simples (`useState` + toggle), aplicado como `data-density` no elemento raiz do shell — mesmo padrão de atributo já usado no protótipo e em `tokens_sie.css` legado (`[data-theme="sie-g100"]`).

### Preservação do legado e namespace

- Reafirma integralmente os paths protegidos e o namespace `--sie-cc-*` já ratificados em `SIE-DS-00`/`SIE-DS-LOCAL-01`. Nenhuma decisão nova de namespace é necessária.
- Novos arquivos seguem o mesmo padrão de CSS-ao-lado-do-componente já estabelecido (`EngineeringShell.css` desta mesma sessão).

### Acessibilidade (AC6)

- `ModuleNavigation`: `<nav aria-label>` + `<section aria-labelledby>` por grupo + `aria-current="page"` no item ativo — mesma estrutura do protótipo.
- `CommandPalette`: `<dialog>` nativo garante foco preso e `Esc` nativo; `role="listbox"`/`role="option"` nos resultados, `aria-label` no campo de busca.
- Nenhuma dependência de Radix/Carbon nesta story — semântica nativa é suficiente para o escopo (paridade com o protótipo, que também não usa framework de componentes).

### Tratamento de riscos do @po

- Should-Fix (a) resolvido acima (CSS puro + teste via leitura de arquivo).
- Should-Fix (b) aceito como está — File List "planejado" é normal, `@dev` atualiza a versão real.

---

## Dev Notes

### Fontes consultadas
- `outputs/design-system/sie-command-center/prototype/index.html` (linhas 16-149: side-rail completo e cabeçalho global) e `styles.css`/`app.js` para comportamento.
- `outputs/design-system/sie-command-center/docs/experience-architecture.md` §3 (Shell), §6 (densidade), §8 (responsividade).
- Convenção de CSS do projeto: arquivo `.css` ao lado do componente, importado diretamente, classes prefixadas (confirmado em `divisor-workspace.css`, replicado em `EngineeringShell.css` desta mesma sessão).
- Padrão de teste do projeto: `renderToStaticMarkup` + `toContain` (sem `@testing-library`, que não é dependência do projeto) — para interações (clique, teclado) que `renderToStaticMarkup` não cobre, a lógica correspondente deve ser extraída para funções/hooks puros testáveis isoladamente (mesmo padrão já usado em `feature-flag.ts`/`use-density.ts`), evitando depender de simulação de DOM não suportada pelo projeto.

### Testing
- Framework: vitest, mesmo padrão das stories anteriores.
- Interações que dependem de DOM real (clique, teclado) testadas via lógica extraída em hooks/funções puras, não via simulação de evento em `renderToStaticMarkup` (que não suporta).

---

## Change Log

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-31 | 0.1.0 | Story criada em modo Draft a partir do backlog-semente SIE-DS-02, escopo local-only | @sm/River |
| 2026-07-31 | 0.2.0 | Validada GO (8/10) — Status: Draft → ReadyForArchitecture. Valor claro, rastreabilidade forte (protótipo + spec + stories anteriores), escopo IN/OUT nítido, dependências corretas, legado protegido (AC7), zero requisito inventado. 2 Should-Fix não bloqueantes: (a) AC1 "colapsa para drawer < 992px... verificável" é o item de maior risco de teste desta story — @dev deve decidir cedo se testa via lógica extraída ou aceita cobertura parcial, documentando a decisão; (b) File List "planejado" pode divergir na implementação (aceitável, story já avisa). Handoff para `@architect`. | @po/Pax |
| 2026-07-31 | 0.3.0 | Ratificação arquitetural: **PASS** — Status: ReadyForArchitecture → Ready. Estado lifted em EngineeringShell; colapso de nav via CSS puro (resolve Should-Fix do @po, testado via leitura de arquivo); lógica de CommandPalette extraída em funções puras testáveis; densidade via hook simples + data-density. Handoff para `@dev`. | @architect/Aria |
| 2026-07-31 | 0.3.5 | Development started (yolo mode) — Status: Ready → InProgress | @dev/Dex |
| 2026-07-31 | 0.4.0 | Development complete — Status: InProgress → InReview. AC1-AC8 implementados: ModuleNavigation, CommandPalette, useDensity, EngineeringShell reestruturado. Lint/typecheck limpos, 1010/1010 testes (regressão completa), build SPA correto verde (hash inalterado — rota isolada, nem entra no bundle de produção). AppShell.tsx confirmado intocado. Smoke test HTTP real: nav lateral, "Engineering OS", command palette dialog e densidade confirmados funcionando no dev server. Pronta para `@qa`. | @dev/Dex |
| 2026-07-31 | 0.5.0 | QA Gate **CONCERNS** — Status: InReview → Done. AC1-AC8 verificados independentemente com smoke test HTTP real e dupla verificação de AC7 (git diff + hash de build SPA inalterado). CodeRabbit indisponível pela 3ª story consecutiva — escalado como prioridade para @devops. 2 Should-Fix não bloqueantes registrados (drawer mobile sem overlay/Esc; CodeRabbit recorrente). Gate file: `docs/qa/gates/SIE-DS-02-engineering-shell-opt-in.yml`. | @qa/Quinn |

---

## Dev Agent Record

### Agent Model Used
Claude Sonnet 5 (`claude-sonnet-5`) — modo YOLO (`*develop-yolo`)

### Debug Log References
- **Falso positivo no próprio teste:** `background: transparent` foi sinalizado pelo teste de "zero hardcode de cor" — corrigido o teste (regex passou a excluir `transparent`/`inherit`/`currentColor`), não o CSS.
- **Erro de tipo real:** `handleKeyDown` estava tipado para `React.KeyboardEvent<HTMLDivElement>` mas usado em `onKeyDown` de um `<dialog>` — corrigido para `HTMLDialogElement`.
- **Warnings reais de lint (`react-refresh/only-export-components`):** funções puras e dados estáticos exportados junto com componentes React quebram o Fast Refresh. Corrigido extraindo para `command-palette-logic.ts` e `module-navigation-data.ts` (mesmo padrão já usado em `use-density.ts`), com os testes correspondentes atualizados para importar dessas novas fontes.
- **Teste desatualizado de story anterior:** `-sie-command-center-preview.test.tsx` (de `SIE-DS-LOCAL-01`) esperava o texto literal "SIE Command Center", que deixou de existir após a reestruturação do shell (título linear → brand lockup "SIE" + "Engineering OS"). Corrigido para verificar "Engineering OS".
- **Build de validação:** usado `vite build --config vite.spa.config.ts` (SPA, correto) desta vez, não o SSR — lição da correção anterior nesta mesma story-chain. Confirmado que o hash do bundle SPA não mudou, porque a rota `/sie-command-center-preview` nunca foi adicionada a `routeTree.spa.ts` (mantido manualmente) — reforça o isolamento do AC7.

### Completion Notes List
- AC1–AC8 implementados: `ModuleNavigation` (nav lateral, 4 grupos/9 itens replicados do protótipo), `CommandPalette` (dialog nativo, `Ctrl/Cmd+K`, filtro + navegação por seta via funções puras), `useDensity` (hook simples), `EngineeringShell` reestruturado (layout `aside`+`content-shell`, cabeçalho global completo).
- **Divergência consciente do protótipo, documentada:** o protótipo não implementa navegação por seta na paleta (só filtra + Tab nativo). Implementei navegação por seta porque `role="listbox"`/`role="option"` (ratificado por `@architect`) exige isso pela WAI-ARIA Authoring Practices — não é invenção, é consequência do papel ARIA adotado.
- **Smoke test real via dev server:** `http://localhost:5173/sie-command-center-preview` → HTTP 200, nav lateral presente, "Engineering OS" presente, `<dialog class="sie-cc-command-palette">` presente, `data-density="comfortable"` presente, zero `style=` no header/nav. Rota raiz legada (`/`) → HTTP 200, "Projetos" presente — zero regressão.
- AC7 confirmado: `git diff` vazio em `AppShell.tsx`; nenhum outro arquivo de produção tocado (apenas `src/components/command-center/**` e as 2 rotas isoladas, todas já `??` desde `SIE-DS-LOCAL-01`).
- Nenhuma operação remota foi executada — cadeia termina em `@qa`, conforme decisão explícita do usuário.

### File List (real)

**Criados nesta story:**
- `src/components/command-center/ModuleNavigation.tsx`, `.css`, `.test.tsx`
- `src/components/command-center/module-navigation-data.ts` (extraído para preservar Fast Refresh — não estava no plano original)
- `src/components/command-center/CommandPalette.tsx`, `.css`, `.test.tsx`
- `src/components/command-center/command-palette-logic.ts` (extraído pelo mesmo motivo)
- `src/components/command-center/use-density.ts`, `.test.ts`

**Modificados nesta story:**
- `src/components/command-center/EngineeringShell.tsx` (reestruturado)
- `src/components/command-center/EngineeringShell.css` (novo layout)
- `src/components/command-center/EngineeringShell.test.tsx` (testes ajustados)
- `src/components/command-center/tokens/sie-cc-tokens.css` (tokens de densidade portados)
- `src/components/command-center/tokens/sie-cc-tokens.test.ts` (teste dos novos tokens)
- `src/routes/-sie-command-center-preview.test.tsx` (asserção desatualizada corrigida — pertence a `SIE-DS-LOCAL-01`, ajustada como efeito colateral necessário desta story)

**Confirmado intocado (AC7):**
- `src/components/app/AppShell.tsx`, todas as rotas de produção existentes, `src/routes/sie-command-center-preview.tsx` (não precisou mudar — só consome `EngineeringShell`).

## QA Results

### Review Date: 2026-07-31

### Reviewed By: Quinn (Test Architect)

### CodeRabbit Full Self-Healing Loop (Step 0)

**Não executado** — 3ª story consecutiva (`SIE-DS-00`, `SIE-DS-LOCAL-01`, `SIE-DS-02`) com o mesmo binário WSL quebrado (SIGILL/exit 132). Compensado, como nas anteriores, com: lint + typecheck + suíte completa (1010 testes) + build + varredura manual de segurança (zero ocorrência de `dangerouslySetInnerHTML`/`eval`/`innerHTML`/storage/`document.write` nos 13 arquivos novos/modificados) + smoke test HTTP real da rota rodando. **Escalado:** com 3 ocorrências seguidas e escopo de código crescente a cada story, recomendo que isso pare de ser um CONCERNS recorrente e vire um item priorizado para `@devops` antes de qualquer story futura.

### Verificação Independente

- **Smoke test real:** `/sie-command-center-preview` → HTTP 200; nav lateral (`sie-cc-nav-lateral`), brand "Engineering OS", `<dialog class="sie-cc-command-palette">` e `data-density="comfortable"` confirmados presentes no HTML servido pelo dev server real, não apenas no código-fonte.
- **Regressão do legado:** rota raiz (`/`) → HTTP 200, "Projetos" presente.
- **AC7:** `git diff` vazio em `AppShell.tsx`; todos os arquivos novos são `??` (untracked, aditivos) restritos a `src/components/command-center/**` e 2 arquivos de rota já existentes de `SIE-DS-LOCAL-01`.
- **Build SPA:** hash do bundle de produção idêntico ao anterior — confirma que `/sie-command-center-preview` não está referenciado em `routeTree.spa.ts` e portanto não pode vazar para o artefato de deploy do Hostinger.

### Requirements Traceability (AC → Evidência)

| AC | Evidência | Resultado |
|---|---|---|
| AC1 | `ModuleNavigation.tsx`/`.test.tsx` — 4 grupos/9 itens replicados do protótipo; colapso `@media (max-width: 991px)` testado via leitura de CSS | PASS |
| AC2 | `EngineeringShell.tsx` — seletor de projeto, sync-state, busca, densidade, autor, todos presentes e testados | PASS |
| AC3 | `CommandPalette.tsx` + `command-palette-logic.ts` — dialog nativo, filtro e navegação por seta testados como funções puras (10 testes) | PASS |
| AC4 | tokens de densidade portados + `useDensity`/`alternarDensidade` testados (involutividade incluída) + `data-density` confirmado no smoke test | PASS |
| AC5 | `EngineeringShell` reestruturado, rota consumidora não precisou mudar (boa decisão de estabilidade de interface) | PASS |
| AC6 | `role="listbox"`/`role="option"`/`aria-current`/`aria-label`/`aria-expanded` presentes; navegação por teclado real (Tab nativo em todos os `<button>`, setas na paleta); `prefers-reduced-motion` no drawer | PASS |
| AC7 | `git diff` vazio + build SPA com hash inalterado (dupla confirmação) | PASS |
| AC8 | lint limpo, typecheck limpo, 1010/1010 testes, build verde | PASS |

### Code Quality Assessment

Implementação consistente com as duas stories anteriores: sem estilos inline, sem hardcode de cor fora de tokens, sem dependências novas, estado local sem lib externa. Boa decisão de extrair lógica pura (`command-palette-logic.ts`, `module-navigation-data.ts`) — resolveu um warning real de lint (`react-refresh/only-export-components`) e, como efeito colateral positivo, tornou a paleta de comandos e a navegação testáveis sem simulação de DOM, que o projeto não suporta.

### Refactoring Performed

Nenhum necessário.

### Compliance Check

- Coding Standards: ✓
- Project Structure: ✓ (`src/components/command-center/`, path já ratificado)
- Testing Strategy: ✓ (mesmo padrão `renderToStaticMarkup` + funções puras)
- All ACs Met: ✓

### Improvements Checklist

- [x] Smoke test HTTP real de todos os elementos interativos novos (nav, paleta, densidade)
- [x] Verificação dupla de AC7 (git diff + hash de build inalterado)
- [x] Varredura manual de segurança
- [ ] **Should-Fix (não bloqueante):** o drawer de navegação mobile (`ModuleNavigation` < 992px) não tem overlay de fundo nem fechamento por clique-fora ou `Esc` — só fecha ao selecionar um item. Diferente da `CommandPalette`, que usa `<dialog>` nativo e ganha isso de graça. Não é uma lacuna de AC (nenhum AC exige isso), mas é uma inconsistência de UX entre os dois padrões de overlay implementados na mesma story. Registrar para quando `SIE-DS-03`+ tratar a navegação mobile com mais profundidade.
- [ ] **Should-Fix (recorrente, escalado):** CodeRabbit CLI quebrado há 3 stories — priorizar reparo antes de escopo maior.

### Security Review

Varredura manual (grep) por `dangerouslySetInnerHTML`, `eval`, `innerHTML`, `localStorage`, `sessionStorage`, `document.write`, `new Function`: zero ocorrências nos 13 arquivos novos/modificados. Nenhum dado de usuário processado — tudo ilustrativo/estático.

### Performance Considerations

Bundle SPA de produção não é afetado (rota isolada, fora de `routeTree.spa.ts`). No dev server, sem problemas de performance observados no smoke test.

### Files Modified During Review

Nenhum — revisão somente leitura + requisições HTTP ao dev server já em execução.

### Gate Status

Gate: **CONCERNS** → `docs/qa/gates/SIE-DS-02-engineering-shell-opt-in.yml`

**Razão:** todos os 8 ACs PASS com evidência forte (traceability completa + smoke test real + dupla verificação de AC7). CONCERNS mantido exclusivamente pela indisponibilidade recorrente do CodeRabbit (3ª ocorrência) — escalado como prioridade para `@devops`, não como bloqueio desta story.

### Recommended Status

**✓ Ready for Done** — nenhum item bloqueante para esta story. `@devops`: favor tratar o CodeRabbit antes da próxima.
(Story owner — `@po` — decide o status final.)
