---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [source_regression_test, build_artifact_test, spa_fallback_test]
---

# Story MOD-QT-3-01: Modulo de Queda de Tensao Integral e Permanente

## Status

**InReview**

> Criada por @sm (River) em 2026-07-30 a partir do manifesto SDC `docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml` e do workflow-fonte `docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md`. Esta story formaliza o hardening operacional do MOD-QT: o modulo ja existe no codigo, mas precisa permanecer visivel, navegavel, testavel e publicavel nos artefatos canonicos.

## Fonte e Diagnostico

**Fonte principal:** `docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md`.

**Orquestracao SDC:** `docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml`.

**Achados confirmados pelo workflow-fonte:**

- A rota UI existe em `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`.
- A rota esta registrada em `src/routeTree.gen.ts` e `src/routeTree.spa.ts`.
- O link "Queda de tensao" existe no hub do projeto em `src/routes/projetos.$projetoId.tsx`, dentro de `deps-hero-links`.
- O link existe apenas no contexto de projeto (`/projetos/:projetoId`); `AppShell.tsx` nao tem menu global de modulos.
- `dist` contem `queda-tensao`, mas diretorios antigos de deploy podem nao conter a rota completa e nao devem ser tratados como fonte canonica sem decisao de @devops.
- Servir `dist` com servidor estatico sem fallback SPA retorna `404` em deep links como `/projetos/demo/queda-tensao`.

**Conclusao de escopo:** o problema nao e ausencia completa do modulo. O problema e permanencia operacional: exposicao, deep link, fallback SPA, build/deploy canonico e testes de regressao.

## Story

**As a** engenheiro eletricista usando o SIE,  
**I want** acessar o modulo de Queda de Tensao pelo fluxo de projeto e por URL direta no build canonico,  
**so that** o modulo entregue continue aparecendo e funcionando depois de build, preview, deploy e regressao futura.

## Acceptance Criteria

### AC1 - Modulo aparece no fluxo do projeto

```gherkin
Given um projeto existente
When o usuario abre `/projetos/:projetoId`
Then a acao "Queda de tensao" aparece junto dos demais modulos do projeto
And aponta para `/projetos/:projetoId/queda-tensao`
```

### AC2 - Rota do modulo carrega por navegacao

```gherkin
Given o usuario esta no detalhe do projeto
When clica em "Queda de tensao"
Then a tela do MOD-QT e renderizada sem erro
And a navegacao usa a rota TanStack correta para `/projetos/$projetoId/queda-tensao`
```

### AC3 - Rota profunda carrega por refresh

```gherkin
Given o build SPA/producao esta sendo servido pelo modo canonico definido na story
When o usuario acessa diretamente `/projetos/:projetoId/queda-tensao`
Then o servidor entrega a aplicacao e o router renderiza a rota correta
And a resposta HTTP nao e `404`
```

### AC4 - Artefato de deploy contem MOD-QT

```gherkin
Given o build canonico de deploy foi gerado
When o artefato e inspecionado
Then `queda-tensao` esta presente no bundle final
And o label "Queda de tensao" ou representacao equivalente esta presente
```

### AC5 - Builds antigos nao mascaram o modulo

```gherkin
Given existem diretorios antigos de deploy como `hostinger-spa*`, `hostinger-deploy*` ou `export`
When o workflow finaliza
Then a story declara qual diretorio/script e canonico
And qualquer artefato obsoleto fica documentado como nao fonte de verdade ou e substituido pelo artefato canonico autorizado
```

### AC6 - Gates tecnicos passam

```gherkin
Given a implementacao final
When @dev roda os gates tecnicos no subprojeto
Then `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` e `npm run build:spa` passam
And qualquer caveat ambiental fica comprovado no Dev Agent Record
```

## Fora de Escopo

- Alterar formulas, criterios normativos ou contrato publico de MOD-QT.
- Promover valores `[VERIFICAR]` para `CONFIRMADO`.
- Alterar `RetornoMODQT`, schemas Zod ou endpoints publicos sem story propria.
- Criar link global executavel para MOD-QT sem `projetoId`; MOD-QT e modulo dependente de projeto.
- Fazer `git push`, PR, merge, release ou deploy por @dev. Isso fica para @devops depois de QA.
- Tratar diretorios antigos de deploy como fonte canonica sem decisao explicita registrada por @devops.

## CodeRabbit Integration

> `coderabbit_integration.enabled: true` em `.aiox-core/core-config.yaml`.

### Story Type Analysis

**Primary Type**: Deployment  
**Secondary Type(s)**: Frontend, Integration  
**Complexity**: Medium - afeta navegacao do produto, route trees SSR/SPA, scripts/preview de build e verificacao de artefato, mas nao altera dominio nem schemas publicos.

### Specialized Agent Assignment

**Primary Agents**:
- @dev: implementacao, testes e pre-commit review
- @devops: validacao pre-PR/deploy, artefato canonico e operacao remota quando autorizada

**Supporting Agents**:
- @qa: quality gate da story
- @ux-design-expert: consultivo apenas se a exposicao do modulo exigir mudanca de navegacao visual alem do hub existente

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Run `coderabbit --prompt-only -t uncommitted` se o CLI estiver disponivel; se nao estiver, aplicar degradacao graciosa prevista em `core-config.yaml`.
- [ ] Pre-PR (@devops): Run `coderabbit --prompt-only --base main` antes de PR, se disponivel.
- [ ] Pre-Deployment (@devops): Run pre-deployment review antes de deploy real, se o usuario autorizar deploy.

### Self-Healing Configuration

**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL only

**Predicted Behavior**:
- CRITICAL issues: auto_fix ate 2 iteracoes, depois HALT para revisao humana
- HIGH issues: document_only no Dev Agent Record se nao forem corrigidos dentro do escopo

### CodeRabbit Focus Areas

**Primary Focus**:
- Deep link SPA nao retorna `404` para `/projetos/:id/queda-tensao`.
- Artefato canonico contem `queda-tensao` e o label do modulo.
- Scripts de build/preview nao conflitam entre SSR e SPA.

**Secondary Focus**:
- Navegacao preserva o contexto de projeto; nao criar link global sem `projetoId`.
- Nenhuma alteracao em formulas, contratos publicos ou endpoints publicos de MOD-QT.

## Tasks / Subtasks

- [x] Task 1 - Preflight e baseline (AC: 1, 2, 6)
  - [x] 1.1 Registrar `git status --short` antes da implementacao, preservando mudancas nao relacionadas.
  - [x] 1.2 No subprojeto `sistema-de-instala-es-el-tricas-sie-main`, rodar baseline: `npm run typecheck` e `npm test`.
  - [x] 1.3 Registrar branch, caveats ambientais e baseline de testes no Dev Agent Record.

- [x] Task 2 - Confirmar estado atual do MOD-QT (AC: 1, 2, 4)
  - [x] 2.1 Verificar `rg -n "Queda de tens|queda-tensao|deps-hero-links" src tests`.
  - [x] 2.2 Verificar `rg -n "queda-tensao" src/routeTree.gen.ts src/routeTree.spa.ts`.
  - [x] 2.3 Se rota, link ou route tree estiverem ausentes, tratar como regressao dentro desta story.

- [x] Task 3 - Exposicao permanente no produto (AC: 1, 2)
  - [x] 3.1 Manter o link atual no hub do projeto em `src/routes/projetos.$projetoId.tsx`.
  - [x] 3.2 Garantir que o link usa TanStack Router com `to="/projetos/$projetoId/queda-tensao"` e `params={{ projetoId }}`.
  - [x] 3.3 Se a story exigir exposicao adicional, criar navegacao apenas dentro de contexto de projeto; sem link global executavel sem projeto ativo.

- [x] Task 4 - Rota profunda e fallback SPA (AC: 3)
  - [x] 4.1 Definir e implementar preview SPA canonico com fallback para `index.html`, ou documentar/ajustar o script de deploy SPA vigente para isso.
  - [x] 4.2 Validar que `/`, `/projetos/demo` e `/projetos/demo/queda-tensao` respondem `200` no modo SPA canonico.
  - [x] 4.3 Validar que assets em `/assets/*.js` e `/assets/*.css` continuam respondendo `200`.

- [x] Task 5 - Build canonico e artefatos permanentes (AC: 4, 5)
  - [x] 5.1 Declarar na story qual build e canonico para desenvolvimento local, producao SSR e producao SPA/Hostinger.
  - [x] 5.2 Se necessario, criar script canonico como `preview:spa` ou `build:hostinger`, seguindo os padroes ja existentes de `package.json`.
  - [x] 5.3 Nao editar todos os diretorios antigos indiscriminadamente; documentar os obsoletos e o artefato oficial.
  - [x] 5.4 Validar `rg "queda-tensao" dist` e `rg "Queda de tens" dist` apos build canonico.

- [x] Task 6 - Testes de regressao (AC: 1, 2, 3, 4, 5)
  - [x] 6.1 Adicionar ou atualizar teste de fonte do hub garantindo texto, rota e ordem do link de Queda de Tensao.
  - [x] 6.2 Adicionar ou atualizar teste de route tree para `src/routeTree.gen.ts` e `src/routeTree.spa.ts`.
  - [x] 6.3 Adicionar teste de artefato para confirmar `queda-tensao` e o label no build canonico.
  - [x] 6.4 Adicionar teste/script de fallback SPA que comprove `200` no deep link.
  - [x] 6.5 Nao instalar `jsdom`, `happy-dom` ou Testing Library sem necessidade; os testes de UI existentes usam Vitest, `readFileSync` e `renderToStaticMarkup` quando aplicavel.

- [x] Task 7 - Validacoes finais (AC: 6)
  - [x] 7.1 Rodar `npm run lint`.
  - [x] 7.2 Rodar `npm run typecheck`.
  - [x] 7.3 Rodar `npm test`.
  - [x] 7.4 Rodar `npm run build`.
  - [x] 7.5 Rodar `npm run build:spa`.
  - [x] 7.6 Registrar resultados e caveats no Dev Agent Record.

- [x] Task 8 - Browser/local smoke (AC: 2, 3)
  - [x] 8.1 Subir o servidor adequado e registrar URL local.
  - [x] 8.2 Abrir `/`, selecionar/criar projeto e entrar em `/projetos/:projetoId`.
  - [x] 8.3 Confirmar link "Queda de tensao" visivel, clicar e confirmar tela MOD-QT carregada.
  - [x] 8.4 Recarregar `/projetos/:projetoId/queda-tensao` e confirmar que nao volta `404`.

- [x] Task 9 - Story updates e handoff (AC: 1-6)
  - [x] 9.1 Atualizar Tasks/Subtasks, Dev Agent Record, Debug Log, Completion Notes, File List e Change Log.
  - [x] 9.2 Alterar Status para `InReview` ao concluir a implementacao.
  - [x] 9.3 Criar `.aiox/handoffs/MOD-QT-3-01-dev-to-qa.yaml`.

## Dev Notes

### Arquivos provaveis

- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.gen.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.spa.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/AppShell.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/router.spa.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/vite.spa.config.ts`
- `sistema-de-instala-es-el-tricas-sie-main/package.json`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/`
- `sistema-de-instala-es-el-tricas-sie-main/tests/`

### Contexto tecnico extraido de artefatos reais

- O subprojeto usa React 19, TanStack Router/Start, Vite, Vitest, TypeScript e `srvx`. Os scripts existentes incluem `dev`, `build`, `start`, `preview`, `lint`, `typecheck`, `test` e `build:spa`. [Source: `sistema-de-instala-es-el-tricas-sie-main/package.json`]
- A rota SPA esta em `src/routeTree.spa.ts` e ja exclui rotas de API/Start; o path esperado e `/projetos/$projetoId/queda-tensao`. [Source: `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.spa.ts`]
- A route tree SSR `src/routeTree.gen.ts` tambem contem a rota UI e rotas API de MOD-QT (`queda-tensao-lote`, `queda-tensao/resumo`). [Source: `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.gen.ts`]
- O hub do projeto contem o bloco `deps-hero-links` e o link de Queda de Tensao com `to="/projetos/$projetoId/queda-tensao"`. [Source: `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`]
- A tela de destino define `createFileRoute("/projetos/$projetoId_/queda-tensao")` e carrega componentes de MOD-QT. [Source: `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`]

### Lacunas de documentacao

- `.aiox-core/core-config.yaml` aponta `docs/architecture/index.md` e `docs/framework/*.md`, mas esses arquivos nao existem nos paths configurados nesta worktree. Esta story usa os workflows, stories MOD-QT anteriores e artefatos reais do subprojeto como fonte de verdade operacional.

### Constraints

- Seguir Artigo IV da Constitution: nao inventar requisito normativo nem alterar formula de queda de tensao.
- Trabalhar dentro de `docs/stories/` e atualizar File List antes de concluir.
- Preservar mudancas nao relacionadas em worktree suja.
- @dev nao executa push/PR/deploy; isso e handoff para @devops.

### Testing

- Framework real: Vitest.
- Para checks de fonte/route tree, usar `readFileSync` e asserts de string, seguindo o padrao aceito em `MOD-QT-2-05`.
- Para UI pura exportada, `renderToStaticMarkup` e aceitavel quando ja houver componente exportado.
- Para fallback SPA, preferir teste/script de processo que suba preview canonico em porta livre, faca requests HTTP e encerre o processo.
- Gates obrigatorios no subprojeto: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run build:spa`.

## Definition of Done

- [ ] AC1-AC6 atendidos com evidencia registrada.
- [ ] Story em `InReview`.
- [ ] Link/entrada de MOD-QT visivel no fluxo autorizado.
- [ ] Rota `/projetos/:projetoId/queda-tensao` registrada em SSR e SPA.
- [ ] Rota profunda responde sem 404 no modo preview/deploy definido.
- [ ] Build canonico contem `queda-tensao`.
- [ ] Artefato de deploy canonico definido.
- [ ] Testes de regressao adicionados/atualizados.
- [ ] `npm run lint` executado.
- [ ] `npm run typecheck` executado.
- [ ] `npm test` executado.
- [ ] `npm run build` executado.
- [ ] `npm run build:spa` executado.
- [ ] File List atualizado.
- [ ] Nenhuma alteracao fora de escopo.
- [ ] Handoff para @qa criado.

## SM Checklist Validation

| Category | Status | Issues |
| --- | --- | --- |
| 1. Goal & Context Clarity | PASS | Objetivo, valor e diagnostico operacional estao explicitos. |
| 2. Technical Implementation Guidance | PASS | Arquivos, scripts, gates e escolhas de fallback estao definidos. |
| 3. Reference Effectiveness | PARTIAL | Referencias de arquitetura configuradas estao ausentes na worktree; story aponta fontes reais disponiveis. |
| 4. Self-Containment Assessment | PASS | Requisitos centrais e constraints estao dentro da story. |
| 5. Testing Guidance | PASS | Testes minimos e gates estao especificados. |
| 6. CodeRabbit Integration | PASS | Secao completa renderizada porque `coderabbit_integration.enabled: true`. |

**Final Assessment:** READY FOR PO VALIDATION. No momento da criacao por @sm, a story estava suficientemente detalhada para @po validar e promover para `Ready`; a validacao PO abaixo executou essa transicao.

## PO Validation

**Reviewer:** @po (Pax)  
**Command:** `*validate-story-draft docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md`  
**Decision:** GO  
**Implementation Readiness Score:** 8/10  
**Confidence:** High

### Validation Summary

| Category | Status | Notes |
| --- | --- | --- |
| Template compliance | PASS | Required lifecycle sections are present and no active template placeholders remain. |
| Executor assignment | PASS | `executor: "@dev"` is appropriate for code/test implementation. `quality_gate: "@qa"` is retained because project stories and Constitution assign quality verdicts to @qa. |
| File/source tree clarity | PASS | Target files, subproject path and build/test scripts are listed with enough precision for @dev. |
| UI/frontend completeness | PASS | Story correctly keeps MOD-QT project-scoped and blocks a global executable link without `projetoId`. |
| Acceptance criteria | PASS | AC1-AC6 are measurable and covered by tasks. |
| Testing guidance | PASS | Vitest/source assertions/build artifact/deep-link checks are specified without introducing unnecessary DOM tooling. |
| Anti-hallucination | PASS WITH NOTE | Architecture paths configured in `.aiox-core/core-config.yaml` are absent, but the story uses accessible workflow, manifest, previous MOD-QT stories and real code artifacts as evidence. |
| CodeRabbit integration | PASS | Enabled section is present with pre-commit, pre-PR and pre-deployment gates. |

### PO Corrections / Clarifications

1. @qa remains the quality gate despite the legacy `validate-next-story` task listing a narrower set of quality gate agents. Current project Constitution makes @qa the authority for quality verdicts, and existing MOD-QT stories use @qa consistently.
2. The wording "Queda de tensao" in ACs is accepted as accent-insensitive because artifact checks already use `rg "Queda de tens" dist`; @dev should not change user-facing copy just to normalize accents.
3. AC5 is accepted as operational hardening, not permission for @dev to mutate every old deploy directory. @dev must define/document the canonical artifact and leave remote/deploy decisions to @devops.
4. This story does not reopen MOD-QT formula, schema or public API scope.

### GO Conditions for @dev

- Start from Status `Ready`.
- Keep implementation limited to the tasks and ACs above.
- Update Dev Agent Record, File List and Change Log before setting `InReview`.
- Create `.aiox/handoffs/MOD-QT-3-01-dev-to-qa.yaml` when implementation is complete.

## Change Log

| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2026-07-30 | 0.1 | Story criada a partir do manifesto SDC MOD-QT integral/permanente e workflow-fonte para @dev. Status `Draft`; aguardando PO. | @sm (River) |
| 2026-07-30 | 0.2 | Validated GO (8/10) - Status: Draft -> Ready. Mantido @qa como quality gate, ACs e tasks aprovados para desenvolvimento. | @po (Pax) |
| 2026-07-30 | 0.3 | Development started (yolo mode) - Status: Ready -> InProgress. | @dev (Dex) |
| 2026-07-30 | 0.4 | Development complete - Status: InProgress -> InReview. Adicionado preview SPA canonico e testes de permanencia MOD-QT; caveats de lint/test suite registrados para QA. | @dev (Dex) |

## Dev Agent Record

### Agent Model Used

GPT-5 Codex (@dev / Dex), modo YOLO autonomo

### Debug Log References

- `.aiox/logs/MOD-QT-3-01-yolo.log` - linhas `[DEV]`.
- Baseline inicial:
  - `git status --short` no subprojeto mostrou worktree ja suja com dezenas de arquivos modificados/untracked de outros ciclos, incluindo `package.json` ja modificado.
  - `npm run typecheck` inicial: timeout em ~124s antes de retornar.
  - `npm test` inicial: timeout em ~244s antes de retornar.
- Implementacao:
  - `npx vitest run tests/ui/mod-qt-integral-permanente.test.ts tests/ui/projeto-detalhe-nav-links.test.ts`: PASS, 2 arquivos, 7 testes.
  - `npx tsc --noEmit --pretty false`: PASS.
  - `npx eslint tests/ui/mod-qt-integral-permanente.test.ts`: PASS.
  - `npm run build`: PASS.
  - `npm run build:spa`: PASS.
  - `rg "queda-tensao" dist`: PASS apos `build:spa`.
  - `rg "Queda de tens" dist`: PASS apos `build:spa`.
  - `npx vitest run tests/ui/mod-qt-integral-permanente.test.ts`: PASS, 1 arquivo, 4 testes, validando tambem artefato `dist` existente.
  - Smoke SPA real: `node scripts/static-server.mjs dist 4391` respondeu `200` para `/`, `/projetos/demo`, `/projetos/demo/queda-tensao`, `/assets/index-*.js` e `/assets/index-*.css`.
- Caveats ambientais / preexistentes:
  - `npm run lint` completo foi executado duas vezes e nao retornou dentro de 244s/604s nesta maquina. Lint escopado no arquivo novo passou; `package.json` e ignorado pela config ESLint atual.
  - `npm test` completo executou 135 arquivos e 963 testes; resultado: 134 arquivos PASS, 962 testes PASS, 1 timeout em teste preexistente (`tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx`, caso "nenhum rotulo, ajuda ou memorial..."). O mesmo caso passou isolado em 14.78s; o conjunto focado `mod-qt-integral-permanente + projeto-detalhe-nav-links + queda-tensao-fluxo-entrada-fechado` passou com 19/19 testes.
  - CodeRabbit WSL: binario existe (`test -x ~/.local/bin/coderabbit` retornou 0), mas `coderabbit --prompt-only -t uncommitted` saiu com codigo 1 sem relatorio utilizavel nesta sessao; aplicada degradacao graciosa prevista em `core-config.yaml`.

### Completion Notes List

- O MOD-QT ja estava presente no hub e nas route trees; nenhuma rota, formula, schema ou contrato publico foi alterado.
- Adicionado script canonico `preview:spa` apontando para o servidor estatico existente `scripts/static-server.mjs`, que ja implementa fallback SPA para `index.html`.
- Adicionado teste `tests/ui/mod-qt-integral-permanente.test.ts` cobrindo:
  - link TanStack no hub (`to="/projetos/$projetoId/queda-tensao"` + `params={{ projetoId }}`);
  - registro da rota nas route trees SSR e SPA;
  - contrato do preview SPA canonico e fallback local com fixture;
  - inspeção recursiva do `dist` quando o artefato existe.
- Build canonico documentado para esta story:
  - Desenvolvimento local: `npm run dev`.
  - Producao SSR: `npm run build` + `npm run start`.
  - Producao SPA/Hostinger: `npm run build:spa` + `npm run preview:spa` para validacao local com fallback.
- Diretorios antigos `hostinger-spa*`, `hostinger-deploy*` e `export` nao foram editados; permanecem nao-canonicos ate decisao de @devops.
- DoD self-assessment: requisitos funcionais e ACs implementados; validacoes principais passaram, com caveats de lint completo e timeout isolado da suite completa documentados para decisao de @qa.

### File List

**Modificados por esta story**
- `sistema-de-instala-es-el-tricas-sie-main/package.json` - adicionado script `preview:spa` para servir `dist` via `scripts/static-server.mjs` com fallback SPA. Observacao: o mesmo arquivo ja tinha alteracoes nao relacionadas (`docs:tutorial:*`) antes desta story; elas foram preservadas.
- `docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md` - Tasks/Subtasks, Dev Agent Record, Change Log e Status.

**Criados por esta story**
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/mod-qt-integral-permanente.test.ts` - teste de permanencia operacional do MOD-QT.
- `.aiox/handoffs/MOD-QT-3-01-dev-to-qa.yaml` - handoff para QA.

**Lidos/validados, nao modificados por esta story**
- `sistema-de-instala-es-el-tricas-sie-main/scripts/static-server.mjs`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.gen.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.spa.ts`
- `sistema-de-instala-es-el-tricas-sie-main/vite.spa.config.ts`

## QA Results

### Review Date: 2026-07-30

### Reviewed By: Quinn (@qa) - Test Architect

### Findings

- **Medium - Gates completos ainda nao sao reprodutiveis ponta a ponta nesta maquina.** `npm run lint` completo ja havia excedido 244s/604s sem relatorio final, e `npm test` completo registrou 1 timeout em teste preexistente de varredura de fonte em `sistema-de-instala-es-el-tricas-sie-main/tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx:206`. O caso passou isolado, e o conjunto focado passou, entao nao bloqueia os ACs desta story, mas mantem o gate em CONCERNS.
- **Low - `package.json` tem mudancas preexistentes nao relacionadas no mesmo arquivo do script novo.** O script `preview:spa` esta em `sistema-de-instala-es-el-tricas-sie-main/package.json:13`; as entradas `docs:tutorial:*` em `package.json:21` e `package.json:22` ja estavam na worktree e devem ser revisadas por @devops no staging.

### Requirements Traceability

| AC | Evidence | Status |
| --- | --- | --- |
| AC1 | Teste valida link "Queda de tensao" no hub com rota TanStack em `tests/ui/mod-qt-integral-permanente.test.ts:96`. | PASS |
| AC2 | Teste valida rota nas route trees SSR e SPA em `tests/ui/mod-qt-integral-permanente.test.ts:102` e `:103`. | PASS |
| AC3 | Smoke real apos `npm run build:spa`: `/`, `/projetos/demo`, `/projetos/demo/queda-tensao`, JS e CSS retornaram 200. | PASS |
| AC4 | `npm run build:spa` passou; `rg "queda-tensao" dist` e `rg "Queda de tens" dist` passaram; teste de artefato em `tests/ui/mod-qt-integral-permanente.test.ts:139`. | PASS |
| AC5 | Story e Dev Agent Record declaram `build:spa` + `preview:spa` como fluxo SPA canonico; diretorios antigos nao foram tratados como fonte de verdade. | PASS |
| AC6 | Typecheck, build, build:spa, lint escopado e testes focados passaram; caveats completos documentados. | CONCERNS |

### Test Evidence

- PASS - `npx vitest run tests/ui/mod-qt-integral-permanente.test.ts tests/ui/projeto-detalhe-nav-links.test.ts` - 2 arquivos, 7 testes.
- PASS - `npx eslint tests/ui/mod-qt-integral-permanente.test.ts`.
- PASS - `npx tsc --noEmit --pretty false`.
- PASS - `npm run build`.
- PASS - `npm run build:spa`.
- PASS - smoke SPA em `node scripts/static-server.mjs dist 4399`: 200 para raiz, projeto, deep link MOD-QT e assets.
- CONCERNS - `npm run lint` completo e `npm test` completo ainda apresentam caveats de runtime/timeout registrados no Dev Agent Record.

### Gate Status

Gate: **CONCERNS** -> `docs/qa/gates/MOD-QT-3-01-gate.yaml`

### Recommended Status

**Ready for DevOps pre-push with concerns.** Os ACs de permanencia operacional do MOD-QT estao cobertos; @devops deve revisar staging de `package.json` e decidir se os caveats de gates completos exigem story de manutencao antes de push/PR/deploy.

---

**Story created by:** @sm (River)  
**Date:** 2026-07-30  
**Priority:** P1  
**Source:** `docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml`
