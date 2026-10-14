# Workflow SDC Headless YOLO — SIE Command Center: SIE-DS-02 (Engineering Shell opt-in, local-only)

**Versão:** 1.0.0
**Data:** 2026-07-31
**Status:** Ready for execution — escopo local-only, sem operações remotas
**Modo:** YOLO agente-a-agente (sessão manual real), zero prompts durante a execução de cada fase
**Escopo:** implementação real do item canônico `SIE-DS-02` do backlog-semente (nav lateral, cabeçalho global, paleta de comandos), consumida apenas via a rota de preview local já existente
**Ratificações reutilizadas:** `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` §"🏛️ Architecture Ratification"; `docs/stories/story-SIE-DS-LOCAL-01-fundacao-preview-local.md`
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
**Conformidade:** `.aiox-core/constitution.md`

> **Decisão explícita do usuário (2026-07-31):** este workflow NÃO inclui a fase `@devops` de operações remotas. A cadeia termina em `@qa` → `local_done`. Push, PR, merge, release e deploy ficam para decisão separada e posterior, com revisão humana do diff antes de qualquer ação remota — consistente com o mesmo padrão já usado em `SIE-DS-LOCAL-01`.

## 1. Objetivo

Implementar de verdade o item canônico `SIE-DS-02` (Engineering Shell opt-in) do backlog-semente: navegação lateral, cabeçalho global e paleta de comandos, consumidos pela rota isolada `/sie-command-center-preview` já existente (criada por `SIE-DS-LOCAL-01`). `AppShell` e todas as rotas de produção permanecem intocadas — nada muda para o usuário final até uma story futura autorizar a promoção.

## 2. Princípios inegociáveis

Herdados integralmente de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §2: CLI First, Story-Driven, No Invention, Agent Authority, Quality First, Legacy Preservation, Additive Delivery, Fail Closed, Idempotência. **DevOps Exclusivo aplica-se mas não é acionado nesta execução** — nenhuma operação remota é autorizada por este documento.

## 3. Escopo

### 3.1 IN

- `ModuleNavigation` (organism): navegação lateral 256px, marca, grupos de módulos (Workspace/Entrada/Dimensionamento/Documentação), item ativo, colapso em drawer < 992px;
- Cabeçalho global expandido: seletor de projeto (ilustrativo), indicador de estado/sincronização, gatilho de busca/paleta, alternância de densidade, botão de autor (ilustrativo);
- `CommandPalette` (organism): dialog nativo, `Ctrl/Cmd+K` para abrir, busca filtra itens, navegação por teclado (setas + Enter), `Esc` fecha;
- Alternância de densidade `comfortable`/`compact` (tokens já definidos em `sie-premium.css`, ainda não portados — portar nesta story);
- `EngineeringShell` reestruturado para o layout `aside` + `content-shell` (em vez do header+nav+main linear de `SIE-DS-LOCAL-01`);
- Testes automatizados para os 3 organisms novos e para a reestruturação do shell;
- Acessibilidade: navegação por teclado completa na paleta e na nav lateral, `aria-*` corretos, foco visível, `prefers-reduced-motion` respeitado.

### 3.2 OUT

- Cabeçalho **contextual** (breadcrumb, título de página, ação primária) — isso é `SIE-DS-03`;
- Conteúdo real de qualquer módulo (Ambientes, Circuitos, etc.) — `SIE-DS-03` a `SIE-DS-06`;
- Inspector panel — `SIE-DS-04`+;
- Dados reais de projeto — segue ilustrativo, como em `SIE-DS-LOCAL-01`;
- Qualquer alteração em `AppShell.tsx` ou rotas de produção existentes;
- **Qualquer operação remota** (push, PR, merge, release, deploy) — decisão separada, fora deste workflow.

## 4. Fontes de verdade

- `outputs/design-system/sie-command-center/docs/experience-architecture.md` §3 (Shell), §5 (Atomic Design), §6 (Tokens — densidade), §8 (Responsividade);
- `outputs/design-system/sie-command-center/prototype/index.html` + `app.js` (referência comportamental do side-rail, cabeçalho, paleta de comandos);
- `docs/analysis/GAP-ANALISE-SIE-DS-LOCAL-01-vs-PROTOTIPO.md` (Gap 1, Gap 4 — exatamente o que esta story resolve);
- `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` e `story-SIE-DS-LOCAL-01-fundacao-preview-local.md` (namespace, paths protegidos, convenções já estabelecidas — reutilizadas, não redecididas).

## 5. Máquina de estados (reduzida — sem fase DevOps remota)

```text
sm_story_creation → po_story_validation → architect_ratification → dev_implementation → qa_review → local_done
```

## 6. Backlog-semente

### SIE-DS-02 — Engineering Shell opt-in (nav lateral, cabeçalho global, paleta de comandos)

Resultado esperado: ver seção 3.1 IN. Consumida via `src/routes/sie-command-center-preview.tsx` (já existente), que passa a montar o `EngineeringShell` reestruturado em vez do shell linear mínimo.

## 7. Critério de conclusão

Termina `local_done` quando: story `Done`, QA `PASS`/`CONCERNS` sem bloqueio, lint/typecheck/test/build locais verdes, `AppShell.tsx` e rotas legadas comprovadamente intocadas, e a rota de preview acessível localmente demonstrando nav lateral, cabeçalho global funcional e paleta de comandos operante via `Ctrl/Cmd+K`.

Qualquer condição não atendida produz `BLOCKED` ou `FAILED` — nunca sucesso parcial, e nenhuma operação remota é executada.

---

— Orion (`@aiox-master`), escopando a implementação real de SIE-DS-02 sem tocar produção
