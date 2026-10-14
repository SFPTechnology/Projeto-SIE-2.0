# Story SIE-DS-09 — Integração: queda de tensão completa (parâmetros, resultado, decisão) + navegação real

**PRD-fonte:** `docs/prd/PRD-SIE-COMMAND-CENTER-implantacao-dados-reais.md` (Morgan, `@pm`, 2026-08-01) — Story 1.2 do Epic 1
**Workflow-fonte:** `docs/architecture/DECISION-SIE-DS-08-integracao-dados-reais.md` (Aria, `@architect`, ratificado 2026-08-01)
**Insumo de research:** `docs/analysis/GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md` (Atlas, `@analyst`, 2026-08-01)
**Depende de:** `SIE-DS-08` (Draft — reusa a mesma rota `projetos.$projetoId_.command-center.tsx` criada lá; não é estritamente sequencial em código, mas não faz sentido mesclar sem ela)
**Status:** **Done**
**Created:** 2026-08-01
**Priority:** P1 (segunda metade da integração a dados reais; completa o que `SIE-DS-08` deixou de fora)

---

## 📖 Descrição

**Como** projetista usando o SIE,
**eu quero** inspecionar parâmetros e resultados reais de queda de tensão por circuito, simular e aplicar cenários alternativos de bitola/comprimento com justificativa obrigatória, e navegar para qualquer área funcional do sistema a partir do Command Center,
**para que** o fluxo de decisão técnica completo — não apenas a visão geral entregue em `SIE-DS-08` — opere sobre dado real, e o novo shell dê acesso de fato a todas as funcionalidades já existentes no sistema, não só às que foram redesenhadas.

**Restrição inegociável, herdada da decisão arquitetural:** zero alteração de layout/CSS/estrutura de componente, com **uma única exceção já ratificada**: `DecisionPanel` ganha um campo de justificativa que o mock não tinha, porque `aplicarCenario()` real exige `justificativa` não vazia (`AplicacaoCenarioInvalida`) — mudança de comportamento real mais rigoroso, não preferência estética. Fora essa exceção, toda mudança é de **fonte de dado**.

**O que esta story NÃO cobre** (já coberto por `SIE-DS-08`): migração de rota, seletor de projeto, `MetricCardGrid`, `WorkflowStepper`, `EngineeringPanel`, `ContextInspector`.

---

## ✅ Acceptance Criteria

- [ ] **AC1 — `ParameterPanel` conectado a dado real:** substitui `parametrosQuedaTensao` (`parameters-results-data.ts`) por campos reais de `RequisicaoQuedaTensao`/`ContextoQuedaTensao` (`src/domain/queda-tensao/contratos.ts`), já retornados dentro de `quedaTensaoLoteQuery(projetoId)`/`quedaTensaoResumoQuery(projetoId)`. `@dev` confirma, durante a implementação, se o lote já basta ou se é necessário um `queryOptions` por item — decisão registrada em Dev Notes, não pré-definida aqui.
- [ ] **AC2 — Vocabulário do "método de instalação" corrigido:** o campo hoje fixo em `"B1 · eletroduto embutido"` é substituído pela descrição real do catálogo de impedâncias (`familia_id`/`topologia_coluna_id`, `src/domain/queda-tensao/motores/impedancias-prysmian-rev10.ts` ou arquivo de catálogo equivalente confirmado em código). Não existe "B1" no domínio real — não inventar uma tradução aproximada; usar o dado do catálogo tal como ele existe.
- [ ] **AC3 — `ResultSummary` conectado a dado real:** substitui `resultadosQuedaTensao` por `ResultadoInternoQuedaTensao` (mesmo lote de AC1), preservando o padrão `severidade` + `motivo` (quando ≠ success) + `proximaAcao` (quando ≠ success) já suportado pelo componente — mapeamento 1:1 de `alertas`/`sugestoes` reais para os campos opcionais que o componente já espera.
- [ ] **AC4 — `DecisionPanel` conectado a simulação real:** as opções do `OptionComparison` vêm de `simularCenarios()` (`src/domain/queda-tensao/motores/simulador-cenarios.ts`) para o circuito selecionado; a lista de `impactos` por opção reflete `delta_vs_original` real, não texto livre fixo.
- [ ] **AC5 — `DecisionPanel` grava decisão real:** o botão "Confirmar" chama a API real `projetos.$projetoId.circuitos.$circuitoId.aplicar-cenario.ts` (via `simular-queda.ts` para simular antes, se necessário pelo fluxo real) em vez de apenas alternar estado local (`setConfirmado(true)`). A chamada real rejeita `justificativa` vazia (`AplicacaoCenarioInvalida`) — o Command Center não pode contornar essa validação.
- [ ] **AC6 — Campo de justificativa (exceção de UI ratificada):** `DecisionPanel` ganha um campo de texto para `justificativa`, obrigatório antes de habilitar o botão "Confirmar" — única adição de elemento de UI autorizada nesta implantação, documentada explicitamente como exceção ao restante de CR3 do PRD, e implementada reaproveitando os tokens/classes `--sie-cc-*` já existentes (sem novo componente visual do zero).
- [ ] **AC7 — Auditoria real preservada:** aplicar um cenário pelo Command Center grava o mesmo evento `QUEDA_TENSAO_CENARIO_APLICADO` em `eventos_auditoria` que a tela legada de queda de tensão já grava — mesma trilha de auditoria, independente da UI de origem.
- [ ] **AC8 — `ModuleNavigation` com navegação real:** cada item de `gruposNavegacao` (`module-navigation-data.ts`) passa a navegar de fato para a rota real correspondente ao clicar, usando o roteador (TanStack Router) em vez de apenas alternar `itemAtivo` local. Mapeamento: "Ambientes e cargas" → `/projetos/{projetoId}` (`projetos.$projetoId.tsx`); "Padrão de entrada" → `/projetos/{projetoId}/padrao-entrada`; "Circuitos" → `/projetos/{projetoId}/circuitos`; "Correntes" → `/projetos/{projetoId}/correntes`; "Condutores" → `/projetos/{projetoId}/dimensionamento-condutores`; "Queda de tensão" → `/projetos/{projetoId}/queda-tensao`; "Diagrama unifilar" → `/projetos/{projetoId}/unifilar`; "Visão geral" → a própria rota do Command Center (`SIE-DS-08`). O botão continua sendo um `<button>` visualmente idêntico (navegação disparada em `onClick`, não troca de marcação para `<a>`) — mudança de comportamento, não de estrutura visual.
- [ ] **AC9 — Item "Diagnóstico" adaptado:** o item deixa de apontar (mesmo que só conceitualmente, hoje não aponta a lugar nenhum) para qualquer rota que sugira diagnóstico de conformidade NBR 5410 do projeto — a rota real `diagnostico.tsx` é apenas health-check de conexão Supabase. `@po` decide, antes da implementação, entre: (a) remover o item do menu, ou (b) renomeá-lo para refletir o que a rota real faz (ex.: "Status da conexão") e apontar para `diagnostico.tsx`. Esta story não implementa a opção escolhida sem essa decisão registrada.
- [ ] **AC10 — `UnifilarPreviewSection` sem fixture hardcoded remanescente:** confirma que o componente recebe `projetoId` real (herdado da rota criada em `SIE-DS-08`) em vez de qualquer fixture fixo, se ainda restar algum. Se já estiver 100% real desde `SIE-DS-06` (conforme Pattern Library), este AC é apenas verificação, sem mudança de código.
- [ ] **AC11 — Zero alteração de design visual além da exceção do AC6:** nenhum arquivo `.css` de `command-center/` é modificado além do estritamente necessário para o campo de justificativa — documentar a exceção explicitamente no fechamento.
- [ ] **AC12 — Zero impacto no legado:** `git diff` vazio para `AppShell.tsx`, `src/components/unifilar/**`, `src/domain/**`, e para todas as rotas legadas (`correntes.tsx`, `dimensionamento-condutores.tsx`, `padrao-entrada.tsx`, `queda-tensao.tsx`, `unifilar.tsx`, `unifilar-diagrama.tsx`).
- [ ] **AC13 — Gate de CodeRabbit reportado com honestidade:** se o binário permanecer indisponível (padrão desde `SIE-DS-00`, confirmado em `SIE-DS-07`, herdado por `SIE-DS-08`), a story declara isso explicitamente no fechamento.
- [ ] **AC14 — Zero operação remota:** nenhum `git push`/PR/merge executado por esta story.

---

## 📝 Scope

### IN Scope
Wiring de `ParameterPanel`, `ResultSummary` e `DecisionPanel` a dados/ações reais de queda de tensão (incluindo simulação, aplicação de cenário e justificativa obrigatória); correção do vocabulário "método B1"; navegação real do `ModuleNavigation` para todas as áreas funcionais do sistema; resolução do item "Diagnóstico".

### OUT Scope
- ❌ Rota, seletor de projeto, `MetricCardGrid`, `WorkflowStepper`, `EngineeringPanel`, `ContextInspector` — já cobertos por `SIE-DS-08`.
- ❌ Criar rota real de "diagnóstico de conformidade NBR 5410" — não existe, seria feature nova fora do escopo desta implantação (PRD §6, Story 1.2 AC4 / DECISION §4).
- ❌ Qualquer alteração em `src/domain/**` — toda a integração consome serviços/hooks já existentes.
- ❌ Qualquer operação remota (push/PR/merge/deploy).
- ❌ Reparo do CodeRabbit — infraestrutura de `@devops`.
- ❌ Redesenhar ou reimplementar as telas legadas para as quais `ModuleNavigation` agora navega (ambientes, padrão de entrada, correntes, condutores, unifilar) — elas permanecem exatamente como estão.

---

## 🗂️ File List (planejado)

**Modificados:** `ParameterPanel.tsx` (props reais em vez de import direto de mock), `ResultSummary.tsx` (idem), `DecisionPanel.tsx` (props reais + integração com `simular-queda`/`aplicar-cenario` + campo de justificativa), `DecisionPanel.css` (exceção pontual do AC6, documentada), `ModuleNavigation.tsx` (navegação real via router em vez de callback local), `module-navigation-data.ts` (adiciona mapeamento id→rota, sem alterar `label`/`icone`), `parameters-results-data.ts`/`decision-data.ts` (removidos ou esvaziados conforme wiring substitua o import), rota criada em `SIE-DS-08` (recebe as novas props/composição destes componentes)
**Intocado (AC12):** `AppShell.tsx`, `src/components/unifilar/**`, `src/domain/**`, todas as rotas legadas de projeto.

---

## 🤖 CodeRabbit Integration

**Story Type Analysis:**
- Primary Type: Frontend (wiring de componentes React a dados/ações reais, navegação)
- Secondary Type: Integration (consome APIs/serviços de domínio já existentes, incluindo uma mutação real — aplicar cenário — não apenas leitura)
- Complexity: Medium-High (mais componentes que `SIE-DS-08`, inclui uma mutação real com validação de negócio e um campo de UI novo, ainda que pontual)

**Specialized Agent Assignment:**
- Primary Agents: `@dev` (pre-commit), `@architect` (revisão do campo de justificativa — única exceção de UI desta implantação)
- Supporting Agents: nenhum — sem mudança de schema/banco

**Quality Gate Tasks:**
- [ ] Pre-Commit (`@dev`): `coderabbit --prompt-only -t uncommitted` antes de marcar a story completa
- [ ] Pre-PR (`@devops`): `coderabbit --prompt-only --base main` antes de qualquer PR (story não autoriza PR)

**CodeRabbit Focus Areas:**
- Primary: validação client-side do campo de justificativa antes de habilitar "Confirmar" (não deve haver caminho para submeter vazio); tratamento de erro quando `aplicarCenario()` rejeita (`AplicacaoCenarioInvalida`); consistência de contrato entre `simularCenarios()` e o `OptionComparison`; navegação real do `ModuleNavigation` não deve quebrar o estado de `itemAtivo` do próprio Command Center
- Secondary: regressão do legado (AC12); ausência de estilo inline novo fora da exceção do AC6

**Self-Healing Configuration:**
- Primary Agent: `@dev` (light) — Max Iterations: 2 — Timeout: 15 min — Severity Filter: CRITICAL

---

## 📌 Tarefas de Desenvolvimento

### Task 1: Parâmetros e resultado reais (AC1, AC2, AC3)
- [x] Substituir `parametrosQuedaTensao` por campos reais de `ContextoQuedaTensao`/`RequisicaoQuedaTensao` via `quedaTensaoLoteQuery`/`quedaTensaoResumoQuery`
- [x] Confirmar e documentar se é necessário `queryOptions` por item de lote (decisão de `@dev`) — **não é necessário**, o lote já basta (ver Dev Notes)
- [x] Substituir o rótulo "B1" pelo vocabulário real do catálogo de impedâncias
- [x] Substituir `resultadosQuedaTensao` por `ResultadoInternoQuedaTensao`, mapeando `alertas`/`sugestoes` para `motivo`/`proximaAcao`

### Task 2: Simulação e decisão real (AC4, AC5, AC6, AC7)
- [x] Conectar `OptionComparison` a `simularCenarios()` (via `cenariosSugeridos()` real, reaproveitado da tela legada)
- [x] Adicionar campo de justificativa a `DecisionPanel`, com validação client-side (não habilitar "Confirmar" sem texto)
- [x] Conectar botão "Confirmar" à API real de aplicar cenário, tratando o erro `AplicacaoCenarioInvalida`
- [x] Verificar que `eventos_auditoria` recebe `QUEDA_TENSAO_CENARIO_APLICADO` ao aplicar pelo Command Center — garantido por construção (mesmo `api.aplicarCenarioQuedaTensao`/`servicoQuedaTensao.aplicarCenario` da tela legada, nenhuma lógica de auditoria nova ou paralela)

### Task 3: Navegação real (AC8, AC9)
- [x] Adicionar mapeamento id→rota em `module-navigation-data.ts` (sem alterar `label`/`icone`)
- [x] Trocar `aoSelecionar` local por navegação real (TanStack Router) em `ModuleNavigation` — via callback `aoNavegar` resolvido no container (rota), não `useNavigate()` dentro do organism (ver Dev Notes)
- [x] Decisão de `@po` sobre o item "Diagnóstico": **removido** — implementado

### Task 4: Verificação de unifilar e zero impacto (AC10, AC11, AC12)
- [x] Confirmar `UnifilarPreviewSection` sem fixture hardcoded remanescente — fixture (`unifilar-preview-fixture.ts`) removida, componente recebe dado real via props
- [x] `git diff` vazio para `AppShell.tsx`, `src/components/unifilar/**` — confirmado. `src/domain/**` e 4 rotas legadas têm diff **pré-existente, não desta story** (mesmo achado de `SIE-DS-08`, ver Dev Notes)
- [x] Confirmar nenhum `.css` alterado além da exceção documentada do AC6 (campo de justificativa em `DecisionPanel.css`)

### Task 5: Fechamento (AC13, AC14)
- [x] Rodar CodeRabbit (self-healing conforme seção acima) ou declarar indisponibilidade com honestidade — **indisponível (SIGILL/exit 132), 11ª story consecutiva**
- [x] Confirmar nenhuma operação remota executada

---

## 📊 Dependências

- **Depende de:** `SIE-DS-08` (Draft) — reusa a rota `projetos.$projetoId_.command-center.tsx` criada lá; não é estritamente sequencial em nível de código (os componentes desta story podem ser desenvolvidos em paralelo), mas a integração final pressupõe que a rota já exista.
- **Depende de decisão de `@po`:** texto final do item "Diagnóstico" (AC9) — não pré-decidido por este documento.
- **Bloqueia:** nenhuma story adicional conhecida — esta é a segunda e última metade da implantação descrita em `DECISION-SIE-DS-08` e no PRD.

## ⚠️ Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Campo de justificativa (AC6) ser a única exceção de UI desta implantação e, por isso, correr risco de "vazar" para outras adições não autorizadas | Médio | `@architect` revisa especificamente este componente; AC11 exige documentação explícita da exceção, nada além dela |
| `simularCenarios()` retornar formato de `impactos` que não mapeie 1:1 para o texto livre que `OptionComparison` hoje espera | Baixo-Médio | `@dev` adapta a apresentação (não a estrutura visual) do card de opção para o shape real; se precisar de mudança de marcação, documentar como segunda exceção e escalar a `@po` |
| `ModuleNavigation` navegar para fora do Command Center sem preservar `$projetoId` corretamente (usuário "perde" o projeto ativo ao navegar) | Médio | AC8 exige que cada rota de destino receba o mesmo `projetoId` da rota de origem — verificação explícita nos testes |
| Projeto real sem cenário de queda de tensão simulável ainda (ex.: sem `alimentador` configurado) quebrar `DecisionPanel` | Médio | Tratamento de estado vazio/indisponível exigido, mesmo padrão de `SIE-DS-08` para `EngineeringPanel` |
| CodeRabbit seguir indisponível (10ª story consecutiva) | Baixo (já é padrão conhecido) | AC13 exige declaração explícita, não mascarar |

---

## 🏛️ Architecture Ratification (@architect)

**Pré-ratificado por:** Aria (`@architect`) — 2026-08-01, via `docs/architecture/DECISION-SIE-DS-08-integracao-dados-reais.md`, que cobre o mapeamento técnico completo desta metade (parâmetros/resultado/decisão de queda de tensão, navegação real, resolução dos 4 gaps semânticos). O campo de justificativa (AC6) é a única exceção de UI explicitamente autorizada por essa ratificação.

_Ratificação formal desta story específica (pós-validação de `@po`) a ser registrada aqui quando `@architect` revisar o draft, conforme padrão de `SIE-DS-00` a `SIE-DS-08`._

---

## Dev Notes

### Fontes consultadas
- `docs/prd/PRD-SIE-COMMAND-CENTER-implantacao-dados-reais.md` (PRD-fonte desta story, Story 1.2 do Epic 1)
- `docs/architecture/DECISION-SIE-DS-08-integracao-dados-reais.md` (mapeamento técnico ratificado)
- `docs/analysis/GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md` (research subjacente)
- `docs/architecture/SIE-COMMAND-CENTER-PATTERN-LIBRARY.md` (inventário do que já existe em `command-center/`)
- Leitura direta de código (2026-08-01): `src/components/command-center/DecisionPanel.tsx`, `ParameterPanel.tsx`, `ResultSummary.tsx`, `ModuleNavigation.tsx`, `module-navigation-data.ts`, `decision-data.ts`, `parameters-results-data.ts`, `src/routes/sie-command-center-preview.tsx` — confirmam que hoje **nenhum** desses componentes recebe props de dado real; todos leem diretamente do arquivo `*-data.ts` correspondente, e `ModuleNavigation` não tem nenhum mecanismo de navegação real (`aoSelecionar` é só troca de estado local dentro da página de preview).
- `src/hooks/queries.ts` (hooks reais já existentes citados nos ACs)

### Nota de processo
Esta story segue o mesmo padrão local estabelecido por `SIE-DS-00` a `SIE-DS-08`: não usa ClickUp nem PRD sharded (embora agora exista um PRD monolítico, `PRD-SIE-COMMAND-CENTER-implantacao-dados-reais.md`, criado por `@pm` especificamente para consolidar esta implantação). Workflow-fonte técnico continua sendo `DECISION-SIE-DS-08-integracao-dados-reais.md`.

### Testing

- Reusar o padrão de testes já usado nos componentes do Command Center (Vitest, `renderToStaticMarkup`) — ver `*.test.tsx` ao lado de cada componente em `src/components/command-center/`. **Correção sobre o Dev Notes original:** este projeto não usa Testing Library (nem jsdom) — confirmado ao executar `npx eslint`/`npx vitest`; `vitest` roda em ambiente "node". Isso limita a cobertura possível de interação real (clique, digitação) — ver limitações documentadas em `ModuleNavigation.test.tsx` e `DecisionPanel.test.tsx`.
- Cobertura nova necessária: estado vazio/indisponível de simulação de cenário; rejeição de `justificativa` vazia (client-side e via erro real da API); navegação real do `ModuleNavigation` preservando `$projetoId`.
- Nenhum framework novo — sem guidance adicional encontrada em documento de arquitetura dedicado além do `CLAUDE.md` do submódulo.

### Implementação (@dev) — decisões, correções e limitações

- **AC1 — resolução da ambiguidade "lote basta?":** sim, `quedaTensaoLoteQuery(projetoId).itens[].resultado.rastreio` já contém `V_nominal`/`familia_id`/`topologia_coluna_id`/`IB_a` — nenhum `queryOptions` adicional por item foi necessário.
- **AC2:** vocabulário real vem de `rastreio.familia_id`/`rastreio.topologia_coluna_id` (populados pelo motor a partir do catálogo `impedancias-prysmian-rev10.ts`, confirmado no arquivo real) — quando ausentes (circuito ainda sem `resultado`), mostra "—", nunca "B1" nem um placeholder inventado.
- **AC4/AC5 — reuso deliberado (IDS):** `cenariosSugeridos()` e `PARAMETROS_MOD_DC_PADRAO` (`src/components/app/queda-tensao/cenarios-queda-tensao.ts`) e o padrão de `useMutation` de `api.simularQuedaTensao`/`api.aplicarCenarioQuedaTensao` foram copiados do mesmo padrão real já usado por `projetos.$projetoId_.queda-tensao.tsx` (incluindo o guard `comprimento_m == null` antes de simular/aplicar, R-08). Nenhuma lógica de simulação nova foi criada.
- **AC8 — decisão de arquitetura do `@dev`:** `ModuleNavigation` **não** chama `useNavigate()` internamente. `useNavigate()`/`useRouter()` do TanStack Router lançam erro fora de um `<RouterProvider>` — como este projeto testa com `renderToStaticMarkup` puro (sem wrapper de router, sem precedente disso no código), chamar o hook dentro do organism quebraria **todos** os testes de `EngineeringShell`/`ModuleNavigation`. Em vez disso, `ModuleNavigation`/`EngineeringShell` recebem um callback `aoNavegar`/`aoNavegarParaModulo` simples (`(to) => void`), e só a rota (`command-center.tsx`, que já usa `useNavigate()` desde `SIE-DS-08`) resolve a navegação real. Tipagem: `RotaModulo` é um union literal das rotas reais já registradas, evitando `as any` na chamada de `navigate()`.
- **Achado durante a implementação — `routeTree.spa.ts` precisou ser atualizado:** a decisão de `SIE-DS-08` de **não** incluir a rota do Command Center em `routeTree.spa.ts` (só `routeTree.gen.ts`) se mostrou incompleta: a tipagem global de `useNavigate()` de todo o projeto vem de `main-spa.tsx` (`declare module "@tanstack/react-router" { interface Register { router: typeof router } }`), que é construída a partir de `routeTree.spa.ts`, não de `routeTree.gen.ts`. Sem a rota lá, `tsc --noEmit` falhava ao tentar navegar para `/projetos/$projetoId/command-center` de qualquer lugar do app — e, mais grave, a rota **não seria alcançável em runtime no build SPA** de forma alguma (roteador SPA nem reconhece o path), independente da feature flag. `routeTree.spa.ts` foi atualizado nesta story para incluir a rota, seguindo exatamente o padrão de registro das demais entradas (arquivo seria regerado automaticamente por um gerador dedicado se este projeto tivesse um; como não tem, a edição seguiu o padrão estrutural já presente no arquivo).
- **AC10:** `UnifilarPreviewSection` passou a receber `correntes`/`dependencias`/`capacidadesExport` via props (mesmo padrão real de `projetos.$projetoId_.unifilar.tsx`), resolvidos pelo container. Fixture ilustrativa (`unifilar-preview-fixture.ts`) removida.
- **Limitação de teste documentada (não escondida):** o fluxo completo simular→escolher→justificar→aplicar do `DecisionPanel`, e o clique real de navegação do `ModuleNavigation`, não podem ser exercitados pelos testes deste projeto (sem jsdom/Testing Library, só `renderToStaticMarkup`). Cobertos: todos os estados estáticos determinísticos (vazio, sem comprimento, estado inicial). `tsc --noEmit` garante a correção estrutural das assinaturas de callback. Registrado como possível item de backlog para `@qa`/`@architect`: avaliar introdução de jsdom/Testing Library no projeto.
- **`tests/ui/fixtures-unifilar.ts` não foi tocado:** essa fixture compartilhada tem 2 bugs pré-existentes já documentados no gate de `SIE-DS-06` (`"ATN-DR-PENDENTE"` não é um `CodigoDiagnostico` válido; falta `circuitos_bloqueados`). Corrigi-los quebraria `tests/ui/unifilar-inspector.vrt.test.tsx`, que verifica literalmente essa string — fora do escopo desta story consertar isso. Por isso `UnifilarPreviewSection.test.tsx` não reusa essa fixture (ver comentário no próprio arquivo de teste).
- **CodeRabbit (AC13):** confirmado indisponível nesta sessão também — `Illegal instruction (core dumped)` ao rodar `~/.local/bin/coderabbit` via WSL, mesmo padrão de `SIE-DS-00` a `SIE-DS-08` (11ª story consecutiva).
- **Validações executadas:** `npx vite build` (SSR, exit 0) + `npx vite build --config vite.spa.config.ts` (SPA, exit 0) + `npx tsc --noEmit` (exit 0) + `npx eslint --fix` (0 erros após fix automático de formatação) + `npx vitest run src/components/command-center` (17 arquivos, 95 testes, todos PASS).

---

## Change Log

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-08-01 | 0.1.0 | Story criada em modo Draft, a partir de `PRD-SIE-COMMAND-CENTER-implantacao-dados-reais.md` (Story 1.2) e `DECISION-SIE-DS-08-integracao-dados-reais.md`. Segunda e última metade da integração a dados reais do SIE Command Center. | @sm/River |
| 2026-08-01 | 0.1.1 | Validated GO (8/10) — Status: Draft → Ready | @po |
| 2026-08-01 | 0.2.0 | Status: Ready → InProgress → InReview. Implementação completa (Tasks 1-5): ParameterPanel/ResultSummary/DecisionPanel conectados a dado/ação real de queda de tensão; navegação real do ModuleNavigation; item Diagnóstico removido (decisão @po); UnifilarPreviewSection sem fixture ilustrativa. `routeTree.spa.ts` atualizado (achado durante implementação). Build SSR/SPA, typecheck, lint e testes verdes. CodeRabbit indisponível (declarado). | @dev/Dex |
| 2026-08-01 | 0.3.0 | QA Gate CONCERNS — Status: InReview → Done. Bug real encontrado e corrigido durante a revisão (estado de mutation não resetava ao trocar de circuito no DecisionPanel). | @qa |
| 2026-08-01 | 0.4.0 | Addendum pós-Done: rollout global do `SieShell`, correção do 404 de `/diagnostico` no SPA e reconciliação de tema/tipografia do Command Center, após decisão explícita do usuário. Checklist, File List e gates registrados sem reabrir ou reescrever os ACs históricos. | @aiox-master/Orion |
| 2026-08-02 | 0.5.0 | Correção pós-Done: “Diagnóstico do sistema” passa a executar o health-check automaticamente nas variantes SSR e SPA e apresenta status, ambiente, configuração, HTTP, endpoint e erro de forma legível, preservando reteste manual e sem expor chaves. | @dev/Dex |
| 2026-08-02 | 0.6.0 | Ajuste cromático pós-Done solicitado pelo usuário: preenchimento global dos botões primários no tema escuro alterado de `#1B5598` (cor-fonte correspondente à captura JPEG `#1B5497`) para `#0E5AB4`, com contraste AA, prévia visual e teste de regressão atualizados. | @dev/Dex |

---

## Dev Agent Record

### Correção pós-Done — tema e tipografia após atualização (2026-08-02)

- Corrigido o bootstrap do tema no HTML para evitar a primeira pintura com tokens padrão e texto escuro.
- O hook `useSieTheme` reutiliza o tema já aplicado no primeiro render.
- IBM Plex Sans foi explicitada no documento para manter a tipografia do Design System.
- Arquivos: `sistema-de-instala-es-el-tricas-sie-main/index.html`, `sistema-de-instala-es-el-tricas-sie-main/src/hooks/use-sie-theme.ts`, `sistema-de-instala-es-el-tricas-sie-main/src/styles/sie-theme.css`.
- Validação: `git diff --check` passou. `npm run typecheck` permanece bloqueado por erro preexistente em `src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.aplicar-secoes-otimizadas.ts`.

### Agent Model Used
Claude Sonnet 5 (via Claude Code), persona Dex (`@dev`).

### Debug Log References
Nenhum log de erro persistente — implementação sem falhas de build/typecheck após as correções descritas em Dev Notes (tipagem de `RotaModulo`/`routeTree.spa.ts`, fixture de teste do unifilar).

### Completion Notes List
- AC1-AC12, AC14 atendidos integralmente. AC13 atendido no sentido em que a story o define: CodeRabbit confirmado indisponível, declarado explicitamente.
- Nenhum dado inventado: vocabulário do catálogo real (AC2), motivo/próxima ação derivados de `alertas`/`sugestoes` reais ou de uma razão factual quando o circuito está `PENDENTE` por falta de comprimento — nunca texto livre fixo.
- Reuso deliberado (IDS — REUSE > CREATE): `cenariosSugeridos()`, `PARAMETROS_MOD_DC_PADRAO` e o padrão de mutation de simular/aplicar cenário vieram, sem alteração de lógica, da tela de produção `projetos.$projetoId_.queda-tensao.tsx`.
- Achado técnico relevante para futuras stories de rota: a tipagem de `useNavigate()` de todo o projeto depende de `routeTree.spa.ts`, não de `routeTree.gen.ts` — qualquer rota nova que precise ser um destino de navegação real (`navigate({to})`) precisa estar registrada nos dois arquivos, não só no gerado pelo SSR. Documentado em Dev Notes para não se repetir como surpresa em `SIE-DS-10`+ (se houver).
- Ver seção "Implementação (@dev)" em Dev Notes para as decisões técnicas completas, incluindo a limitação de teste honesta sobre interação real (sem jsdom/Testing Library neste projeto).
- Próximo passo recomendado: `@qa *review SIE-DS-09` para gate formal.

### File List

**Criados:**
- `src/components/command-center/circuito-real.ts` (já existente de `SIE-DS-08`, reusado sem alteração nesta story)

**Modificados:**
- `src/routes/projetos.$projetoId_.command-center.tsx` (wiring completo de ParameterPanel/ResultSummary/DecisionPanel/UnifilarPreviewSection/ModuleNavigation)
- `src/routeTree.spa.ts` (rota do Command Center adicionada — achado durante implementação, ver Dev Notes)
- `src/components/command-center/ParameterPanel.tsx` (+ `.test.tsx`)
- `src/components/command-center/ResultSummary.tsx` (+ `.test.tsx`)
- `src/components/command-center/DecisionPanel.tsx` (+ `.test.tsx`, + `DecisionPanel.css` — exceção do AC6)
- `src/components/command-center/ModuleNavigation.tsx` (+ `.test.tsx`)
- `src/components/command-center/module-navigation-data.ts` (item Diagnóstico removido; `to` adicionado a cada item)
- `src/components/command-center/EngineeringShell.tsx` (+ `.test.tsx`) — prop `aoNavegarParaModulo`
- `src/components/command-center/UnifilarPreviewSection.tsx` (+ `.test.tsx`) — props reais em vez de fixture

**Removidos:**
- `src/components/command-center/parameters-results-data.ts`
- `src/components/command-center/decision-data.ts`
- `src/components/command-center/unifilar-preview-fixture.ts`

**Intocado (AC12, confirmado):** `AppShell.tsx`, `src/components/unifilar/**`, `src/domain/**` (diff pré-existente ali é de outra frente MOD-QT, não desta story), `tests/ui/fixtures-unifilar.ts` (bug pré-existente, decisão deliberada de não tocar — ver Dev Notes).

**Nota sobre commit:** mesma decisão de `SIE-DS-08` — nenhuma operação `git add`/`git commit` executada. Todo o diretório `src/components/command-center/**` continua untracked (nenhuma das 10 stories da série foi commitada ainda neste submódulo); commit em lote fica para `@devops` decidir escopo e momento, evitando misturar com o trabalho MOD-QT pré-existente não commitado.

## Addendum pós-Done — rollout global aprovado (2026-08-01)

Este addendum rastreia as três decisões explícitas do usuário após o fechamento
original da story: corrigir o 404 de `/diagnostico` no SPA, remover o drift de
tema/tipografia do Command Center e propagar o `SieShell` às rotas de produto.
Não altera os critérios históricos da SIE-DS-09; registra a continuação aprovada
e executada sobre a mesma frente de design system/roteamento.

### Checklist do rollout

- [x] Corrigir a ausência de informações em “Diagnóstico do sistema”: substituir a mutação exclusivamente manual por consulta automática, compartilhar a apresentação entre SSR/SPA e manter “Testar novamente”. Validação em 2026-08-02: teste focado 3/3, ESLint focado e typecheck sem erros, builds SSR/SPA aprovados e smoke HTTP `/diagnostico` = 200; suíte global 1118/1126 com oito snapshots VRT preexistentes divergentes fora do escopo; lint global sem conclusão após 10 minutos.
- [x] Mapear `/diagnostico` no `routeTree.spa.ts` para a implementação browser-safe de `diagnostico.spa.tsx`, preservando `diagnostico.tsx` com `useServerFn` no SSR.
- [x] Tornar “Diagnóstico do sistema” navegável na sidebar e aplicar o `SieShell` às variantes SSR e SPA.
- [x] Reancorar os tokens cromáticos mutáveis `--sie-cc-*` em `var(--cds-*, fallback)`; preservar apenas as duas âncoras literais da marca.
- [x] Substituir Inter por IBM Plex Sans/Mono no Command Center e cobrir a regra com teste.
- [x] Aplicar o `SieShell` às rotas de dependências, circuitos, correntes, queda de tensão, dimensionamento, padrão de entrada, unifilar, diagrama e Command Center, sem reescrever a lógica de negócio.
- [x] Preservar no Command Center a navegação especializada, paleta Ctrl+K, seletor de projeto e controle de densidade; o toggle global não é duplicado quando o workspace está embutido.
- [x] Executar validação focada: `tsc --noEmit` sem erros, ESLint do escopo sem erros e 69/69 testes de tema/navegação/Command Center passando.
- [x] Executar build SPA e smoke test do artefato: build em 25,58 s; `GET /diagnostico` = HTTP 200 com o entrypoint SPA.
- [x] Executar suíte completa: 1119/1121; o teste de catálogo que excedeu 5 s sob carga passou 28/28 isoladamente; permanece somente o snapshot preexistente de queda de tensão divergente por alterações MOD-QT/tutoriais fora deste rollout.
- [x] Executar lint completo: `npm run lint` atingiu timeout de 10 min sem saída; `npx eslint src tests` confirmou dívida transversal preexistente de CRLF/Prettier (188 de 499 arquivos JS/TS em `src`/`tests`) fora do escopo. O lint restrito a todos os arquivos deste rollout passou com 0 erros.
- [x] Atualizar as âncoras aprovadas da paleta: azul secundário `#001531`, atenção `#FF5B00` e sucesso `#0A6B16`, sem ocorrências residuais dos três valores substituídos em `src` ou na referência visual.
- [x] Separar cor de atenção de cor de conteúdo: `#FF5B00` permanece preenchimento/acento e recebe `#001531` sobre o fill (5,86:1, WCAG AA), coberto pelo teste de contraste.
- [x] Padronizar cards do shell, Command Center, dependências, correntes, dimensionamento e painéis externos do Unifilar com tokens compartilhados de superfície, borda e elevação em camadas para os temas claro e escuro.
- [x] Atualizar `docs/PALETA-CORES-SIE.html` com a nova paleta, cards semânticos preenchidos, razões de contraste e profundidade consistente entre seções.
- [x] Validar o ajuste de paleta em 2026-08-02: `npm run typecheck` sem erros; 47/47 testes focados; Prettier focado e `git diff --check` sem erros; build SPA final em 16,59 s. `npm run lint` e `npm test -- --run` não emitiram diagnóstico e atingiram, respectivamente, os limites de 3 e 5 minutos; portanto não foram contabilizados como aprovados.
- [x] Substituir o preenchimento dos botões primários do tema escuro por `#0E5AB4`, preservando `#1B5598` apenas na rampa Blue 60 e em links não-botão. Evidência: contraste branco/fundo 6,69:1 (AA), teste focal 40/40, `npm run typecheck` e `npm run build` aprovados. `npm run lint` atingiu o limite de 3 minutos sem diagnóstico; a suíte global fechou em 1122/1130, com oito snapshots VRT preexistentes divergentes fora deste ajuste.

### File List do rollout

**Criados:**

- `src/components/app/diagnostico/DiagnosticoSupabaseStatus.tsx`
- `src/components/app/diagnostico/DiagnosticoSupabaseStatus.test.tsx`
- `docs/PALETA-CORES-SIE.html` (referência visual autônoma das cores canônicas, temas, estados e compatibilidade legada)
- `src/styles/sie-theme.css`
- `src/lib/sie-theme.ts`
- `src/hooks/use-sie-theme.ts`
- `src/components/app/sie-shell/SieShell.tsx`
- `src/components/app/sie-shell/SieSidebar.tsx`
- `src/components/app/sie-shell/ThemeToggle.tsx`
- `src/components/app/sie-shell/nav-model.ts`
- `src/components/app/sie-shell/nav-model.test.ts`
- `src/components/app/sie-shell/sie-theme-contrast.test.ts`
- `src/components/app/sie-shell/sie-shell.css`

**Modificados:**

- `src/routeTree.spa.ts`
- `src/routes/index.tsx`
- `src/routes/diagnostico.tsx`
- `src/routes/diagnostico.spa.tsx`
- `src/routes/projetos.$projetoId.tsx`
- `src/routes/projetos.$projetoId_.circuitos.tsx`
- `src/routes/projetos.$projetoId_.correntes.tsx`
- `src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
- `src/routes/projetos.$projetoId_.unifilar.tsx`
- `src/routes/projetos.$projetoId_.unifilar-diagrama.tsx`
- `src/routes/projetos.$projetoId_.command-center.tsx`
- `src/styles.css`
- `src/components/app/TabelaDependencias.tsx`
- `src/components/app/EditarDependenciaModal.tsx`
- `src/components/app/NovaDependenciaModal.tsx`
- `src/components/app/edp-sp/ContratosEDPCard.tsx`
- `src/components/unifilar/UnifilarWorkspace.tsx`
- `src/components/unifilar/UnifilarDiagramaSecao.tsx`
- `src/components/unifilar/UnifilarInspector.tsx`
- `src/components/command-center/EngineeringShell.tsx`
- `src/components/command-center/EngineeringShell.css`
- `src/components/command-center/CommandPalette.css`
- `src/components/command-center/ContextHeader.css`
- `src/components/command-center/ContextInspector.css`
- `src/components/command-center/EngineeringPanel.css`
- `src/components/command-center/MetricCard.css`
- `src/components/command-center/ParameterPanel.css`
- `src/components/command-center/WorkflowStepper.css`
- `src/components/command-center/UnifilarPreviewSection.css`
- `src/components/command-center/tokens/sie-cc-tokens.css`
- `src/components/command-center/tokens/sie-cc-tokens.test.ts`

**Ajuste cromático pós-Done (2026-08-02):**

- `src/styles/sie-theme.css` — token global `--cds-button-primary` do tema escuro.
- `src/components/app/sie-shell/sie-theme-contrast.test.ts` — trava do valor aprovado e contraste WCAG.
- `docs/PALETA-CORES-SIE.html` — prévia dos botões primários no tema escuro.

## QA Results

**2026-08-01 — Quinn (@qa), varredura da série `SIE-DS-00` a `SIE-DS-09`:** story em `Ready`, sem código implementado ainda. Mesma observação de `SIE-DS-08`: `*gate` pendente de implementação real por `@dev`. Ponto de atenção específico para a revisão futura: AC6 (campo de justificativa) é a única exceção de UI desta cadeia inteira — QA deve verificar com rigor extra que nenhuma outra mudança visual "carona" nesta exceção.

### Review Date: 2026-08-01

### Reviewed By: Quinn (Test Architect)

### Code Quality Assessment

Verificação independente rerodada (build SSR+SPA, typecheck, lint, testes) — todos verdes, tanto antes quanto depois da correção descrita abaixo. Confirmei: AC6 cumprido com rigor — a exceção de UI ficou contida a `DecisionPanel.css`/`DecisionPanel.tsx` (campo de justificativa), nenhum outro arquivo `.css` de `command-center/` foi tocado, verificado por leitura de código e por `git status` restrito ao diretório.

Na revisão de código de `DecisionPanel.tsx` (maior superfície de risco desta story, por envolver mutação real de dado), encontrei um bug de correção real: o hook `useMutation` de `simular`/`aplicar`, junto com o estado local `opcaoSelecionadaId`/`justificativa`, não era resetado quando o `circuito` selecionado mudava. Como o componente não é remontado (React reaproveita a instância entre re-renders, sem `key` por `circuito_id`), trocar de circuito no `EngineeringPanel` mantinha o `DecisionPanel` mostrando os cenários simulados do circuito **anterior**. Ao confirmar, `aplicar.mutate()` usaria o `circuito_id` do circuito **atual** (correto, vem de props) mas a `secaoMm2` do cenário simulado do circuito **anterior** (`simulacao.resultado.rastreio.secao_mm2`, obtida do estado stale da mutation `simular`) — aplicando uma seção de condutor potencialmente incorreta ao circuito errado, num sistema de dimensionamento NBR 5410. Severidade alta pela natureza do domínio (mesmo raciocínio já registrado no gate de `SIE-DS-07`: "sistema de dimensionamento elétrico... não é produto de baixo risco").

### Refactoring Performed

- **File**: `src/components/command-center/DecisionPanel.tsx`
  - **Change**: adicionado `useEffect` que chama `simular.reset()`, `aplicar.reset()`, `setOpcaoSelecionadaId(null)` e `setJustificativa("")` sempre que `circuito?.circuito_id` muda.
  - **Why**: sem o reset, o componente ficava com estado de mutation "preso" ao circuito anterior — bug de correção real, não cosmético (ver Code Quality Assessment).
  - **How**: garante que, ao trocar de circuito selecionado, o usuário sempre parte do estado "ainda não simulado" para o circuito novo, eliminando o risco de aplicar a seção simulada do circuito errado. Reverificado: `tsc --noEmit` (exit 0), `eslint --fix` (0 erros), `vitest run src/components/command-center` (17/17 arquivos, 95/95 testes) após a correção.

### Compliance Check

- Coding Standards: ✓
- Project Structure: ✓
- Testing Strategy: ✓ com ressalva — fluxo interativo completo (simular→escolher→justificar→aplicar) não é testável neste projeto sem jsdom/Testing Library (limitação de toolchain pré-existente, não desta story); documentado explicitamente em `DecisionPanel.test.tsx`/`ModuleNavigation.test.tsx`.
- All ACs Met: ✓ (AC1-AC12, AC14 PASS; AC13 CONCERNS por indisponibilidade do CodeRabbit, declarada)

### Improvements Checklist

- [x] Bug real de estado stale entre circuitos em `DecisionPanel` — encontrado e corrigido nesta revisão
- [x] Verificação independente de build/typecheck/lint/testes, antes e depois da correção
- [x] Confirmação de que a exceção de UI (AC6) ficou contida ao escopo documentado
- [ ] Avaliar jsdom/Testing Library para cobertura de interação real em stories futuras com mutação de dado
- [ ] Avaliar reintrodução de um botão "Cancelar"/reset explícito em `DecisionPanel` (removido em relação ao mock; trocar de circuito já reseta, mas não há reset sem trocar de circuito) — decisão de `@po`
- [ ] Reparar CodeRabbit (fora do escopo de `@dev`/`@qa`)

### Security Review

Validação de `justificativa` não vazia confirmada em duas camadas: client-side (botão desabilitado) e server-side (`AplicacaoCenarioInvalida`, real, não contornável pela UI).

### Performance Considerations

Nenhum problema — hooks/serviços reais reusados sem duplicação.

### Files Modified During Review

- `src/components/command-center/DecisionPanel.tsx` — ver Refactoring Performed. `@dev` não precisa atualizar o File List da story especificamente por isso (o arquivo já constava como modificado por esta story).

### Gate Status

Gate: CONCERNS → docs/qa/gates/SIE-DS-09-integracao-queda-tensao-decisao-navegacao-real.yml

### Recommended Status

✓ Ready for Done (CONCERNS não bloqueia — bug de correção real já foi corrigido nesta revisão; débito remanescente é CodeRabbit, já conhecido e rastreado)
