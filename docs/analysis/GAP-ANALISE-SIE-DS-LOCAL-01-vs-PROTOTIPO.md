# Gap Analysis — `/sie-command-center-preview` vs. Protótipo do SIE Command Center

**Autor:** Atlas (`@analyst`)
**Data:** 2026-07-31
**Pergunta original:** por que `http://127.0.0.1:5173/sie-command-center-preview` (entregue por `SIE-DS-LOCAL-01`) ficou visualmente diferente de `outputs/design-system/sie-command-center/prototype/index.html`, e o que falta para carregar "conforme o design system previsto".

## Resumo executivo

**A diferença não é um bug — é o escopo declarado de `SIE-DS-LOCAL-01`.** A story entregou deliberadamente um *shell mínimo* (header + nav placeholder + slot), não uma réplica do protótipo. Isso está documentado na própria story (`docs/stories/story-SIE-DS-LOCAL-01-fundacao-preview-local.md`, seção OUT Scope: *"Migração de módulos reais... isso é SIE-DS-03 a SIE-DS-06"*) e no QA Gate (`docs/qa/gates/SIE-DS-LOCAL-01-fundacao-preview-local.yml`, nice-to-have: *"nav placeholder deve ser substituído quando SIE-DS-02/03 avançarem"*).

Dito isso, há **uma divergência real e não-documentada** que vale corrigir cedo: o componente atual usa **estilos inline** (`style={{...}}`), o que viola diretamente a Restrição explícita do design system (`docs/experience-architecture.md` §10: *"Não usar estilos inline"*). O protótipo usa uma folha de estilos dedicada (`styles.css`) com classes BEM-like. Essa é a única não-conformidade que não é "escopo futuro" — é um desvio da especificação que já deveria ter sido seguida no shell mínimo.

O restante das diferenças é **trabalho de fato pendente**, mapeado abaixo para o backlog-semente já existente (`docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §8).

---

## Metodologia

Comparação direta de três fontes, na ordem de precedência definida pela Constituição do projeto (`docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §3.3: decisões ratificadas > protótipo):

1. **Especificação prescritiva:** `outputs/design-system/sie-command-center/docs/experience-architecture.md` (arquitetura de shell, atomic design, tokens, restrições) e `docs/component-catalog.md`.
2. **Referência visual/comportamental:** `outputs/design-system/sie-command-center/prototype/index.html` + `app.js` + `styles.css`.
3. **Implementação atual:** `sistema-de-instala-es-el-tricas-sie-main/src/components/command-center/EngineeringShell.tsx` e `src/routes/sie-command-center-preview.tsx` (entregues por `SIE-DS-LOCAL-01`).

---

## Gap 1 — Estrutura do Shell (Organism: `EngineeringShell`)

| Elemento prescrito (`experience-architecture.md` §3) | Protótipo | Implementação atual (`SIE-DS-LOCAL-01`) | Status |
|---|---|---|---|
| Navegação lateral (`side-rail`), 256px, colapsável em drawer < 992px | ✅ `<aside class="side-rail">` com grupos de módulos, marca, contagens, indicadores de status | ❌ Nav é uma lista horizontal simples (`<nav><ul>`), sem lateralidade, sem colapso, sem agrupamento | **Gap — SIE-DS-02** |
| Cabeçalho global 56px: projeto ativo, troca de contexto, busca/paleta, densidade, autor | Parcial: `project-switcher`, `sync-state`, `command-trigger`, `density-trigger`, `author-button` | Apenas título estático + badge "Preview local" | **Gap — SIE-DS-02/03** |
| Cabeçalho contextual: breadcrumb, título+descrição, badge de estado, ação primária | ✅ `page-heading` completo | ❌ Ausente — conteúdo vai direto para a tabela ilustrativa | **Gap — SIE-DS-03** |
| Workspace: canvas primário + inspetor lateral | ✅ `workspace-grid` com `workspace-primary` + `inspector-panel` | ❌ Apenas `<main>` com uma tabela simples, sem inspetor | **Gap — SIE-DS-04/05** |

**Causa:** `SIE-DS-LOCAL-01` implementou explicitamente a definição "mínima" ratificada por `@architect` na própria story (*"header + nav placeholder + slot de conteúdo... semântica HTML nativa, sem Radix/Carbon nesta story mínima"*) — uma decisão deliberada para manter a story pequena e testável em um ciclo, não uma tentativa de replicar o protótipo.

## Gap 2 — Conformidade com a especificação (não é "escopo futuro", é desvio da spec atual)

| Restrição (`experience-architecture.md` §10) | Situação em `EngineeringShell.tsx` | Severidade |
|---|---|---|
| "Não usar estilos inline" | Todo o componente usa `style={{...}}` inline, referenciando `var(--sie-cc-*)` | **Alta** — viola a spec diretamente, mesmo dentro do escopo mínimo já entregue |
| "Não criar mais de duas cores de acento" | Não violado (usa apenas brand-primary + status-info) | OK |
| "Números técnicos usam `tabular-nums`" | Não aplicável ainda (sem valores numéricos técnicos reais) | N/A nesta story |
| Estados obrigatórios (hover, focus-visible, pressed, disabled) em todo componente interativo | Nav é puramente estática (`<span>`, não `<button>`) — não há elemento interativo para ter esses estados ainda | Esperado (nav é placeholder declarado) |

**Recomendação prioritária:** antes de `SIE-DS-02`, migrar `EngineeringShell.tsx` de estilos inline para uma folha CSS dedicada (`.module.css` ou arquivo CSS simples com classes, no mesmo espírito de `tokens_sie.css` do legado), consumindo os tokens `--sie-cc-*` via `var()` nas classes em vez de `style={{}}`. Isso é uma correção pequena, isolada, e evita que a dívida se acumule antes dos componentes maiores de `SIE-DS-02`+.

## Gap 3 — Atomic Design ausente

Da lista prescrita em `experience-architecture.md` §5, o que existe hoje em `src/components/command-center/`:

| Camada | Prescrito | Implementado em `SIE-DS-LOCAL-01` |
|---|---|---|
| Atoms | `Button`, `IconButton`, `StatusDot`, `StatusBadge`, `MetricValue`, `EngineeringValue`, `Tag`, `Divider` | Nenhum — só elementos HTML nativos sem componentização |
| Molecules | `MetricCard`, `AlertCallout`, `PropertyRow`, `CircuitRow`, `TraceItem`, `CommandItem`, `ModuleNavItem`, `SegmentedControl` | Nenhum |
| Organisms | `ModuleNavigation`, `ContextHeader`, `WorkflowStepper`, `EngineeringDataGrid`, `ContextInspector`, `CommandPalette`, `DiagramCanvas` | Apenas `EngineeringShell` (parcial) |
| Templates | `OverviewTemplate`, `ListInspectorTemplate`, `ParametersResultsTemplate`, `CanvasInspectorTemplate`, `DecisionTemplate` | Nenhum |

**Isso é esperado.** `component-catalog.md` é o escopo de `SIE-DS-01` (Foundations e tokens — que já está PASS/Done, mas cobriu só os tokens CSS, não os átomos React) somado a `SIE-DS-03` a `SIE-DS-06` (que implementam os organisms/templates por módulo). `SIE-DS-LOCAL-01` nunca teve como objetivo entregar essa biblioteca de componentes.

## Gap 4 — Interatividade e funcionalidades demonstrativas

| Funcionalidade do protótipo (`app.js`) | Presente na implementação atual? |
|---|---|
| Paleta de comandos (`Ctrl/Cmd+K`, `dialog`) | ❌ Não |
| Alternância de densidade (`comfortable`/`compact`) | ❌ Não — tokens de densidade nem foram portados (`sie-cc-tokens.css` só tem o subconjunto necessário ao shell mínimo) |
| Seleção de linha/circuito com sincronização ao inspetor | ❌ Não — não há inspetor |
| Drawer de navegação mobile | ❌ Não |
| Atalho de ajuda (`?`) | ❌ Não |
| `prefers-reduced-motion` | ✅ Portado em `sie-cc-tokens.css` (ainda que sem nenhuma animação para reduzir hoje) |

## Gap 5 — Conteúdo e dados

Ambos usam dados **ilustrativos** (requisito atendido corretamente nos dois lados — nenhum dado real, nenhum cálculo real). O protótipo usa um cenário mais rico (projeto "Residência Sabiá", métricas, circuitos com estados variados); a implementação atual usa uma lista simples de 3 projetos fictícios. Isso é proporcional ao escopo — a story não pretendia replicar o cenário de demonstração completo.

---

## Mapeamento para o backlog (o que resolve cada gap)

| Gap | Story do backlog-semente que resolve | Status atual |
|---|---|---|
| Correção de estilos inline (Gap 2) | Nenhuma story dedicada — recomendo tratar como débito técnico de `SIE-DS-LOCAL-01` ou tarefa de abertura de `SIE-DS-02` | **Pendente, não agendado** |
| Navegação lateral, cabeçalho global, cabeçalho contextual, paleta de comandos, densidade (Gap 1, Gap 4) | `SIE-DS-02` — Engineering Shell opt-in | Não iniciada |
| Overview com métricas e jornada técnica (`WorkflowStepper`) | `SIE-DS-03` — Overview, jornada e comandos | Não iniciada |
| List + Inspector (Ambientes, Circuitos, Diagnóstico) | `SIE-DS-04` | Não iniciada |
| Parameters + Results (Padrão de entrada, Correntes, Condutores, Queda de tensão) | `SIE-DS-05` | Não iniciada |
| Canvas + Inspector (Unifilar) | `SIE-DS-06` | Não iniciada |
| Biblioteca de átomos/moléculas (`StatusBadge`, `MetricCard`, etc.) | Distribuída entre `SIE-DS-02` a `SIE-DS-06`, conforme cada componente é primeiro necessário | Não iniciada |

---

## Resposta direta à pergunta ("o que precisa ser corrigido para carregar conforme o previsto")

**Não há nada "quebrado" para corrigir** — a rota funciona exatamente como a story `SIE-DS-LOCAL-01` especificou (verificado por `@qa` com smoke test HTTP real). Para a página se aproximar do protótipo, é necessário **implementar**, não corrigir:

1. **Curto prazo (pequeno, isolado):** migrar `EngineeringShell.tsx` de estilos inline para CSS com classes — único item que é desvio real da especificação já vigente, não trabalho futuro.
2. **Médio prazo:** executar `SIE-DS-02` (shell completo: nav lateral, cabeçalho global e contextual, paleta de comandos, densidade) — é o próximo item da ordem definida em `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §8.
3. **Longo prazo:** `SIE-DS-03` a `SIE-DS-06`, um módulo real por vez, cada um migrando um `Template` (Overview, List+Inspector, Parameters+Results, Canvas+Inspector) com dados reais em vez de ilustrativos.

Nenhum desses itens é urgente para o propósito original de `SIE-DS-LOCAL-01` (permitir avaliação visual antes da decisão de investir no backlog completo) — a decisão de avançar ou não para `SIE-DS-02`+ é justamente o que essa avaliação deveria informar.

---

## Nota operacional

O dev server local (`npm run dev`) que servia a rota nesta sessão foi encerrado. Para reavaliar visualmente, é necessário reiniciá-lo (`npm run dev` em `sistema-de-instala-es-el-tricas-sie-main/`) e acessar `http://localhost:5173/sie-command-center-preview` — a flag `VITE_FEATURE_SIE_COMMAND_CENTER=true` já está configurada em `.env.local`.

— Atlas, investigando a verdade 🔎
