# Story SIE-DS-06 — Canvas + Inspector para Unifilar (CanvasInspectorTemplate)

**Workflow-fonte:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-06-07-DEPLOY-YOLO.md`
**Ratificações reutilizadas:** stories `SIE-DS-00`, `SIE-DS-02`, `SIE-DS-04`
**Status:** **Done**
**Created:** 2026-07-31
**Priority:** P1

---

## 📖 Descrição

**Como** avaliador do SIE Command Center,
**eu quero** ver o `UnifilarWorkspace` real (não uma reimplementação) rodando dentro do shell do Command Center,
**para que** a avaliação cubra o `CanvasInspectorTemplate` usando o componente de produção de verdade, conforme o backlog-semente original pede ("componentes atuais de `src/components/unifilar/`... exportação existente preservada").

**Diferença em relação a todas as stories anteriores desta cadeia:** esta é a primeira que integra um componente de produção real com dados de domínio tipados (não mais 100% ilustrativo simplificado). Confirmado antes de iniciar: `UnifilarWorkspace` não faz nenhuma chamada de rede/roteador (`useQuery`/`useMutation`/`useNavigate`/`fetch` — zero ocorrências), é 100% controlado por props — seguro para uma rota isolada sem backend.

---

## ✅ Acceptance Criteria

- [ ] **AC1 — Integração real:** `src/components/command-center/UnifilarPreviewSection.tsx` existe, importa e renderiza `UnifilarWorkspace` de `src/components/unifilar/UnifilarWorkspace.tsx` **sem modificar esse arquivo** — reuso direto, não reimplementação.
- [ ] **AC2 — Fixture reaproveitado, não inventado:** os dados (`dados: ResultadoTelaCorrente`, `dependencias: DependenciaAgregado[]`) são adaptados do fixture já testado em `tests/ui/unifilar-workspace.vrt.test.tsx` (mesmos valores: circuitos `TUG-Sala`/`ADD-Cozinha-MicroOndas`, dependências `dep-1`/`dep-2`) — não são fabricados do zero. Arquivo dedicado `unifilar-preview-fixture.ts` em `src/components/command-center/`.
- [ ] **AC3 — Integração no shell:** `UnifilarPreviewSection` é montado dentro de `EngineeringShell` (via a rota de preview), com um `ContextHeader` próprio (breadcrumb "Projetos / Residência Sabiá / Diagrama unifilar", ilustrativo) — replicando a composição do `CanvasInspectorTemplate` (`ContextHeader → CanvasToolbar → DiagramCanvas ↔ ContextInspector`), sendo que `CanvasToolbar`/`DiagramCanvas`/inspector já vêm de dentro do próprio `UnifilarWorkspace` reutilizado.
- [ ] **AC4 — Export preservado:** nenhuma funcionalidade de exportação técnica do Unifilar (`UnifilarExportBar`) é removida ou alterada — se `UnifilarWorkspace` a inclui por padrão, ela continua presente e funcional no preview.
- [ ] **AC5 — Zero modificação do Unifilar real:** nenhum arquivo em `src/components/unifilar/` é criado, modificado ou removido. `git diff` vazio para esse diretório inteiro, não só para `AppShell.tsx`.
- [ ] **AC6 — Namespace:** `UnifilarPreviewSection` usa os tokens `--sie-cc-*` apenas para o `ContextHeader`/wrapper próprios; o conteúdo interno de `UnifilarWorkspace` continua usando seus próprios tokens `--sie-*` (`tokens_sie.css`) sem alteração — **não** re-skinar o Unifilar real com tokens do Command Center (isso seria modificá-lo, violando AC5).
- [ ] **AC7 — Zero impacto no legado geral:** `AppShell.tsx` e rotas de produção com `git diff` vazio.
- [ ] **AC8 — Testado localmente:** lint, typecheck, suíte completa, build SPA passam. `UnifilarPreviewSection.test.tsx` confirma que o `UnifilarWorkspace` real renderiza com o fixture (mesmas asserções de `tests/ui/unifilar-workspace.vrt.test.tsx`: "Diagrama unifilar interativo do projeto", "Memorial técnico", etc.).

---

## 📝 Scope

### IN Scope
`UnifilarPreviewSection` (wrapper fino), fixture adaptado, integração na rota.

### OUT Scope
- ❌ Qualquer modificação em `src/components/unifilar/**`;
- ❌ Re-skin do Unifilar com tokens `--sie-cc-*` (namespace do Unifilar é `--sie-*`, intocado);
- ❌ Dados reais de projeto (fixture é ilustrativo, do mesmo tipo já usado em testes);
- ❌ Qualquer alteração em `AppShell.tsx`/rotas de produção; qualquer operação remota.

---

## 🗂️ File List (planejado)

**Criados:** `unifilar-preview-fixture.ts`, `UnifilarPreviewSection.tsx`/`.css`/`.test.tsx`
**Modificados:** `sie-command-center-preview.tsx`, `-sie-command-center-preview.test.tsx`
**Explicitamente intocado (AC5, AC7):** `src/components/unifilar/**`, `AppShell.tsx`, rotas de produção.

---

## 🤖 CodeRabbit Integration

CodeRabbit local indisponível (8ª ocorrência esperada — severidade `high` desde `SIE-DS-05-decision`, dado que esta story integra código de produção real). Compensado por lint/typecheck/test/build reais + revisão manual mais rigorosa de `@qa` (incluindo verificação explícita de que nenhum arquivo do Unifilar foi tocado).

---

## 📌 Tarefas de Desenvolvimento

### Task 1: Fixture (AC2)
- [ ] Adaptar `dados`/`dependencias` de `tests/ui/unifilar-workspace.vrt.test.tsx` para `unifilar-preview-fixture.ts`

### Task 2: UnifilarPreviewSection (AC1, AC3, AC6)
- [ ] Wrapper fino: `ContextHeader` (tokens `--sie-cc-*`) + `UnifilarWorkspace` (tokens `--sie-*`, intocado)

### Task 3: Integração (AC3, AC4)
- [ ] Montar na rota, confirmar `UnifilarExportBar` presente

### Task 4: Validações finais (AC5, AC7, AC8)
- [ ] `git diff` de `src/components/unifilar/` **e** `AppShell.tsx`; lint, typecheck, suíte completa, build SPA

---

## 📊 Dependências

- **Depende de:** `SIE-DS-04` (ContextInspector — referência de padrão, não reutilizado diretamente aqui pois o Unifilar já tem o seu próprio inspector).
- **Fecha:** o item canônico `SIE-DS-06` do backlog-semente.

## ⚠️ Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Fixture divergir sutilmente do original e produzir estado inválido | Médio | AC2 exige reaproveitar os mesmos valores, não recriar |
| `UnifilarWorkspace` ter alguma dependência de contexto não detectada (ex.: CSS global específico) | Médio | Smoke test real via dev server antes de fechar a story |
| Confundir namespace `--sie-*` (legado) com `--sie-cc-*` (Command Center) dentro da mesma seção | Alto | AC6 explicitamente proíbe re-skin; QA verifica visualmente |

---

## 🏛️ Architecture Ratification (@architect)

**Ratificado por:** Aria (`@architect`) — 2026-07-31
**Veredito:** **PASS**

- **Estado interno:** `UnifilarWorkspace` já gerencia seleção/busca/filtros internamente (props `circuitoInicialSelecionado`, `buscaInicial` etc. são apenas sementes iniciais, não controladas de fora) — `UnifilarPreviewSection` **não** precisa (nem deve) elevar esse estado. Wrapper fino, sem lógica própria além de passar o fixture.
- **`ContextHeader` próprio (AC3):** reutiliza o componente `ContextHeader` já existente (`--sie-cc-*`), com conteúdo próprio ("Diagrama unifilar" / breadcrumb terminando em "Diagrama unifilar"), marcando visualmente o início de uma nova zona de template na mesma página de preview — mesmo espírito de empilhar templates que já vem sendo usado desde `SIE-DS-03`.
- **Fronteira de namespace (AC6) é a regra mais importante desta story:** o `<div>`/`<section>` que envolve `<UnifilarWorkspace>` não deve ter nenhum estilo `--sie-cc-*` que vaze para dentro dele via herança CSS problemática (ex.: `color`/`font-family` no wrapper que o Unifilar não sobrescreve explicitamente). Auditar visualmente no smoke test antes de fechar.
- **`projetoId`:** a interface declara `projetoId: string` como obrigatório, mas o teste VRT reaproveitado não o passa — `@dev` deve investigar na implementação (provavelmente tem valor default no destructuring da função, apesar do tipo) e não presumir; se realmente obrigatório, usar um id ilustrativo (`"proj-preview"`), nunca um id de projeto real.

---

## Dev Notes

### Fontes consultadas
- `src/components/unifilar/UnifilarWorkspace.tsx` (props, ausência de side-effects de rede/router — confirmado via grep).
- `tests/ui/unifilar-workspace.vrt.test.tsx` (fixture completo, 235 linhas, reaproveitado).
- `docs/component-catalog.md` (`CanvasInspectorTemplate`).

### Testing
Mesmo padrão de `renderToStaticMarkup`, reaproveitando as asserções já validadas no VRT test original como piso mínimo de corretude.

---

## Change Log

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-31 | 0.1.0 | Story criada em modo Draft — primeira integração de componente de produção real (UnifilarWorkspace) no Command Center, escopo confirmado com o usuário antes de iniciar (zero rede/router, fixture reaproveitado) | @sm/River |
| 2026-07-31 | 0.2.0 | Validada GO (9/10) — Status: Draft → ReadyForArchitecture. AC5/AC6/AC7 protegem rigorosamente o Unifilar real de qualquer modificação ou re-skin; AC2 evita invenção de dados; risco de contexto não-detectado (rede/router) já mitigado antes da story existir (investigação prévia do @sm). Handoff para `@architect`. | @po/Pax |
| 2026-07-31 | 0.3.0 | Ratificação arquitetural: **PASS** — Status: ReadyForArchitecture → Ready. Estado interno já gerenciado por UnifilarWorkspace (wrapper fino); ContextHeader próprio marca nova zona de template; fronteira de namespace é o ponto crítico de QA; projetoId a investigar na implementação, sem presumir. Handoff para `@dev`. | @architect/Aria |
| 2026-07-31 | 0.3.5 | Development started (yolo mode) — Status: Ready → InProgress | @dev/Dex |
| 2026-07-31 | 0.4.0 | Development complete — Status: InProgress → InReview. AC1-AC8 implementados. 2 bugs reais achados e corrigidos no fixture (circuitos_bloqueados ausente, código de diagnóstico inválido — causa raiz: tests/ fora do tsconfig.json). Achado de acessibilidade real (contraste --sie-texto vs --sie-cc-text-primary) corrigido. 152/1051 testes, build SPA verde, AC5/AC7 confirmados com git diff do diretório inteiro. Pronta para `@qa`. | @dev/Dex |
| 2026-07-31 | 0.5.0 | QA Gate **CONCERNS** — Status: InReview → Done. AC1-AC8 verificados com rigor extra (primeira story tocando fronteira com produção). CodeRabbit indisponível pela 8ª story consecutiva. Bug do fixture original de tests/ registrado como achado para o dono do módulo. Gate file: `docs/qa/gates/SIE-DS-06-canvas-inspector-unifilar.yml`. | @qa/Quinn |

---

## Dev Agent Record

### Agent Model Used
Claude Sonnet 5 (`claude-sonnet-5`) — modo YOLO (`*develop-yolo`)

### Debug Log References
- **Achado real e importante (typecheck):** o fixture reaproveitado de `tests/ui/unifilar-workspace.vrt.test.tsx` tinha 2 problemas reais que nunca foram pegos porque **`tests/` não está incluído em `tsconfig.json`** (só `src/**`). Ao colocar o fixture em `src/`, o typecheck real capturou: (1) `resumo.circuitos_bloqueados` — campo obrigatório ausente; (2) `diagnosticos[0].codigo: "ATN-DR-PENDENTE"` — não é um valor válido de `CodigoDiagnostico` (não existe código de DR/ambiente molhado nesse domínio). Corrigidos com valores reais do domínio (`circuitos_bloqueados: 0`, código `"ATN-IB-TERMINAL-ALTA"`), não inventados. **Não corrigido no arquivo de teste original** (fora do escopo desta story) — registrado como achado para o dono do módulo.
- **Achado real de acessibilidade (arquitetura, confirmado na implementação):** `UnifilarWorkspace` não define `color` no elemento raiz, só `background` (escuro, explícito). Sem o reset de `color: var(--sie-texto)` na fronteira de namespace, o texto herdaria `--sie-cc-text-primary` (escuro) sobre fundo escuro — ilegível. Corrigido e confirmado via smoke test real (o HTML servido não contém `--sie-cc-text-primary` dentro da seção do Unifilar, contém `--sie-texto`).
- Flaky de `tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx` reapareceu (3ª vez nesta sessão), desta vez como timeout (5000ms) em vez de falha de conteúdo — confirmado como contenção de recursos da suíte paralela completa (12/12 passa isolado em 823ms), não bug real, não relacionado a esta story.

### Completion Notes List
- AC1–AC8 implementados: `UnifilarPreviewSection` monta o `UnifilarWorkspace` **real** (zero modificação, zero reimplementação), com fixture tipado corretamente e fronteira de namespace que entrega o token certo ao componente legado.
- **AC5/AC7 verificados com rigor extra** (primeira story a tocar código fora de `command-center/`): `git diff --stat -- src/components/unifilar/` vazio e `git diff --stat -- src/components/app/AppShell.tsx` vazio, confirmados separadamente.
- Smoke test real via dev server confirmou o diagrama/memorial do Unifilar renderizando e a fronteira de contraste correta.
- 152 arquivos / 1051 testes, zero falha real (só o flaky de contenção de recursos, confirmado 3x nesta sessão).
- Nenhuma operação remota executada.

### File List (real)
**Criados:** `unifilar-preview-fixture.ts`, `UnifilarPreviewSection.tsx`/`.css`/`.test.tsx`
**Modificados:** `sie-command-center-preview.tsx`, `-sie-command-center-preview.test.tsx`
**Confirmado intocado (AC5, AC7):** `src/components/unifilar/**` (diretório inteiro), `AppShell.tsx`, rotas de produção.

## QA Results

### Review Date: 2026-07-31

### Reviewed By: Quinn (Test Architect)

### CodeRabbit Full Self-Healing Loop (Step 0)

**Não executado** — 8ª story consecutiva. Compensado com lint/typecheck/1051 testes/build SPA/smoke test com verificação de contraste/varredura de segurança manual — revisão mais rigorosa que o padrão, dado que esta story toca a fronteira com código de produção real pela primeira vez.

### Verificação Independente

- `git diff` vazio para `src/components/unifilar/` **inteiro** (não só arquivos individuais) e para `AppShell.tsx` — confirmado independentemente.
- Smoke test real confirma o conteúdo do Unifilar renderizando e a ausência de vazamento de `--sie-cc-text-primary` dentro da seção.
- Regressão: 152/1051, zero falha real (flaky de contenção confirmado pela 3ª vez, sempre resolvido isolado).

### Achados registrados (fora do escopo desta story, mas relevantes)

1. **Bug real em `tests/ui/unifilar-workspace.vrt.test.tsx`:** fixture desatualizado (`circuitos_bloqueados` ausente, código de diagnóstico inválido) nunca detectado porque `tests/` está fora de `tsconfig.json`. Recomendo ao dono do módulo Unifilar avaliar se `tests/` deveria ser incluído no typecheck do projeto — isso teria pego esse bug há semanas.
2. **CodeRabbit:** 8ª story consecutiva indisponível.

### Requirements Traceability

Todos os 8 ACs — PASS, com AC5 e AC7 verificados com evidência mais forte que o padrão (diff do diretório inteiro, não só arquivo único).

### Gate Status

Gate: **CONCERNS** → `docs/qa/gates/SIE-DS-06-canvas-inspector-unifilar.yml`

### Recommended Status

**✓ Ready for Done.**
(Story owner — `@po` — decide o status final.)
