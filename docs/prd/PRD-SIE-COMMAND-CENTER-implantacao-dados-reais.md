# PRD — Implantação do SIE Command Center sobre Dados e Funcionalidades Reais

**Produto:** SIE — Sistema de Instalações Elétricas
**Módulo:** SIE Command Center (novo design system) — integração brownfield, sem novo backend
**Tipo:** PRD Brownfield (wiring de UI já construída a dados/funcionalidades já existentes)
**Autor:** Morgan (`@pm`) — AIOX
**Data:** 2026-08-01
**Status:** Draft — aguardando validação (`@po`) e handoff de stories (`@sm`)
**Modo de execução:** YOLO (autônomo, confirmado pelo usuário)
**Documentos-base (fonte, não invenção — Artigo IV):**
- `docs/architecture/DECISION-SIE-DS-08-integracao-dados-reais.md` (Aria, `@architect`, ratificado 2026-08-01)
- `docs/analysis/GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md` (Atlas, `@analyst`, 2026-08-01)
- `docs/architecture/SIE-COMMAND-CENTER-PATTERN-LIBRARY.md` (inventário do que já foi construído, `SIE-DS-07`)
- `docs/stories/story-SIE-DS-08-integracao-rota-projeto-overview-real.md` (Draft existente, primeira metade desta implantação)
- Inventário de código (rotas, API, hooks, domínio, schema Supabase) levantado por leitura direta do submódulo `sistema-de-instala-es-el-tricas-sie-main`, 2026-08-01

---

## 1. Intro Project Analysis and Context

### 1.1 Analysis Source

IDE-based fresh analysis (leitura direta de código no submódulo), combinada com os 3 documentos de decisão/gap já ratificados listados acima. Nenhuma etapa de `document-project` formal foi executada porque os documentos-base já cobrem exatamente o escopo desta PRD (research + decisão arquitetural já feitas por `@analyst`/`@architect` antes desta solicitação).

### 1.2 Current Project State

O SIE é um sistema de engenharia assistida para projetos elétricos residenciais/comerciais de baixa tensão (NBR 5410 + padrão EDP São Paulo), construído em TanStack Start + React 19 + TypeScript + Carbon Design System + Supabase/PostgreSQL, hospedado no submódulo `sistema-de-instala-es-el-tricas-sie-main`.

**"Sistema original" (o que já existe e é real, referido pelo usuário como `http://localhost:4321/projetos/proj-1/`):** um conjunto de telas de produção, uma por área funcional, cada uma consumindo hooks React Query (`src/hooks/queries.ts`) que chamam ~35 endpoints HTTP reais (`src/routes/api/v1/**`), que por sua vez orquestram motores de cálculo NBR5410/EDP-SP (`src/domain/**`) e persistem em tabelas Supabase reais (`public.projetos`, `dependencias`, `dimensionamento_condutores_*`, `queda_tensao_config`, `eventos_auditoria`, entre outras — ver §4.1). Não existe hoje uma rota "visão geral" única — cada área funcional (ambientes/cargas, padrão de entrada, circuitos, correntes, condutores, queda de tensão, unifilar) é uma tela própria, navegada separadamente.

**⚠️ Achado factual sobre `proj-1`:** não existe seed/fixture oficial de um projeto real com esse id no banco. `proj-1` é usado como id convencional em testes automatizados (VRT, domínio) e aparece em um artefato de output local (`deps-proj-1.json`, gerado por script de report, não versionado como seed). Ou seja, `http://localhost:4321/projetos/proj-1/` hoje só renderiza algo se esse id existir na base do ambiente onde o app está rodando. Este PRD assume que a implantação vai operar sobre **qualquer projeto real existente** (via `$projetoId` de rota), não especificamente sobre um projeto fixo chamado `proj-1` — ver Risco R1 em §4.5.

**O "novo design system" (o que já existe, mas é 100% ilustrativo):** o SIE Command Center — um shell de navegação e um conjunto completo de organisms (`src/components/command-center/**`, com protótipo estático espelhado em `outputs/design-system/sie-command-center/prototype/`) construído ao longo de 8 stories (`SIE-DS-LOCAL-01` a `SIE-DS-07`, todas com gate `CONCERNS` — ver §4.5). Hoje ele vive isolado em `src/routes/sie-command-center-preview.tsx`, atrás da feature flag `VITE_FEATURE_SIE_COMMAND_CENTER`, sem `$projetoId`, sem nenhum `useQuery` real — todo componente lê de um arquivo `*-data.ts` com dados inventados para fins de avaliação visual (`overview-data.ts`, `parameters-results-data.ts`, `decision-data.ts`, `module-navigation-data.ts`). O próprio código declara isso explicitamente em comentário JSDoc.

### 1.3 Available Documentation Analysis

| Documentação | Disponível | Fonte |
|---|---|---|
| Tech Stack | ✓ | `package.json`, código |
| Source Tree / Arquitetura | ✓ | leitura direta do submódulo |
| Mapeamento mock → real (peça a peça) | ✓ | GAP-ANALISE §1-5 |
| Decisão arquitetural ratificada | ✓ | DECISION-SIE-DS-08 |
| Inventário do que já foi construído no design system | ✓ | Pattern Library |
| Story em andamento | ✓ (Draft) | story-SIE-DS-08 |
| Coding Standards / Testing Standards | Parcial | `CLAUDE.md` do submódulo, sem doc dedicado de arquitetura |
| Schema de banco | ✓ | migrations SQL (submódulo + raiz) |

Nenhuma documentação crítica está faltando para este PRD — os dois documentos-base (GAP-ANALISE + DECISION) já cobrem a análise de compatibilidade exigida pelo template brownfield.

### 1.4 Enhancement Scope Definition

**Enhancement Type:**
- [x] Integration with New Systems — não é sistema novo, é **wiring** de UI já construída aos hooks/API/banco já existentes
- [x] Major Feature Modification — o Command Center deixa de ser protótipo isolado e passa a ser rota de produção
- [ ] UI/UX Overhaul — **explicitamente fora de escopo**, restrição de partida do usuário e da decisão arquitetural: zero alteração de design visual

**Enhancement Description:**
Conectar o SIE Command Center (design system novo, já 100% construído visualmente) aos dados e funcionalidades reais do SIE (cálculos, projetos, Supabase), sem alterar nenhum pixel do design original nem do sistema legado, e sem inventar/mockar nenhum dado que não exista no domínio real.

**Impact Assessment:**
- [x] Moderate Impact — troca de fonte de dado (`import` de arquivo mock → hook real) em ~10 organisms e 1 rota; nenhuma mudança de arquitetura, nenhuma migration nova, nenhuma lógica de domínio nova.

### 1.5 Goals and Background Context

**Goals:**
- O SIE Command Center passa a ser uma superfície de trabalho real, não mais um protótipo visual isolado.
- Todas as funcionalidades já existentes no sistema original (ambientes/cargas, padrão de entrada, circuitos, correntes, dimensionamento de condutores, queda de tensão, diagrama unifilar) ficam acessíveis a partir do novo shell — via navegação real, sem duplicar a implementação de cada tela.
- Nenhum dado exibido no novo shell é inventado: onde não existe cálculo/valor real equivalente, o campo é removido ou adaptado ao vocabulário real, nunca preenchido com placeholder.
- O sistema legado (rotas de produção atuais, `AppShell`, `src/domain/**`) permanece 100% intocado — o Command Center é aditivo e reversível via feature flag.

**Background Context:**
O Command Center foi construído (`SIE-DS-LOCAL-01` a `SIE-DS-07`) como uma exploração de design system isolada, deliberadamente sem dado real, para permitir avaliação visual sem risco ao sistema em produção. Essa fase terminou: `@analyst` e `@architect` já mapearam, peça por peça, qual hook real substitui qual mock (GAP-ANALISE + DECISION-SIE-DS-08), incluindo a resolução dos 4 pontos onde o mock usava um conceito que não existe no domínio real (percentual de fluxo, "método B1", estado binário conforme/revisar, item "Diagnóstico" enganoso). Este PRD formaliza essa decisão já ratificada em um documento de produto único, cobrindo a implantação completa (não apenas a metade já rascunhada em `SIE-DS-08`), para servir de referência a `@po` (validação) e `@sm` (formalização das stories restantes).

### 1.6 Change Log

| Change | Date | Version | Description | Author |
|---|---|---|---|---|
| Criação | 2026-08-01 | 1.0.0 | PRD criado em modo YOLO a partir de DECISION-SIE-DS-08 + GAP-ANALISE + inventário de código | Morgan (`@pm`) |

---

## 2. Requirements

*Baseado no mapeamento já ratificado em DECISION-SIE-DS-08 §2-3 e GAP-ANALISE §1-5 — nenhum requisito abaixo introduz cálculo ou dado sem equivalente real confirmado em código.*

### 2.1 Functional

- **FR1:** O SIE Command Center passa a operar sob a rota `/projetos/$projetoId/command-center` (substituindo `/sie-command-center-preview`), recebendo `$projetoId` via `Route.useParams()`, no mesmo padrão das demais rotas de projeto.
- **FR2:** O seletor de projeto no cabeçalho (`sie-cc-project-switcher`) exibe o nome do projeto real via `projetoQuery(projetoId)` e navega para `/projetos/{outroId}/command-center` ao trocar, sem alterar a estrutura visual do botão.
- **FR3:** `MetricCardGrid` exibe conformidade de queda de tensão e pior circuito via `quedaTensaoResumoQuery(projetoId)`, e demanda calculada (`ResultadoDemanda.DT_VA`) via `parametrosEDPQuery(projetoId)`.
- **FR4:** A métrica "Fluxo concluído: X%" é **removida** — não existe cálculo de progresso percentual no domínio real, e não será inventado.
- **FR5:** `WorkflowStepper` mantém as 4 etapas fixas de navegação (Levantamento/Entrada/Dimensionamento/Documentação); o estado `ativo`/`completo` de cada etapa passa a ser inferido de sinais reais já existentes (regra exata definida e documentada por `@dev` na implementação, validada por `@po`).
- **FR6:** `EngineeringPanel` (tabela de circuitos) exibe a lista real via `divisaoCircuitosQuery(projetoId)`, com corrente/seção/queda de tensão via `quedaTensaoLoteQuery(projetoId)`.
- **FR7:** O badge de estado do circuito passa a ter 3 variantes reais (`OK`→`success`, `ACIMA`→`danger`, `PENDENTE`→`warning`), substituindo o binário ilustrativo `conforme`/`revisar`. A paleta de badges já suporta 5 severidades — nenhum token CSS novo é necessário.
- **FR8:** `ContextInspector` exibe, ao selecionar um circuito na tabela, os mesmos campos reais do FR6/FR7 (aplicação/descrição, corrente, seção, queda de tensão, fases, comprimento).
- **FR9:** `ParameterPanel` e `ResultSummary` exibem parâmetros e resultados reais de queda de tensão (`RequisicaoQuedaTensao`/`ContextoQuedaTensao`/`ResultadoInternoQuedaTensao`, incluindo `alertas`/`sugestoes`), substituindo `parameters-results-data.ts`.
- **FR10:** O rótulo "Método de instalação B1 · eletroduto embutido" é substituído pelo vocabulário real do catálogo de impedâncias (`familia_id`/`topologia_coluna_id`, `impedancias-prysmian-rev10.ts`) — não existe equivalente 1:1 para "B1" no domínio.
- **FR11:** `DecisionPanel` usa `simularCenarios()` para as opções e as rotas reais `.../simular-queda` / `.../aplicar-cenario` para simular/confirmar. `aplicarCenario()` exige `justificativa` não vazia (regra real mais rigorosa que o mock) — `DecisionPanel` ganha um campo de justificativa que o mock não tinha.
- **FR12:** `ModuleNavigation` mantém rótulos/ícones estáticos, mas cada `href` passa a apontar para a rota real correspondente já existente: Ambientes e cargas → `projetos.$projetoId.tsx`; Padrão de entrada → `projetos.$projetoId_.padrao-entrada.tsx`; Circuitos → `projetos.$projetoId_.circuitos.tsx`; Correntes → `projetos.$projetoId_.correntes.tsx`; Condutores → `projetos.$projetoId_.dimensionamento-condutores.tsx`; Queda de tensão → `projetos.$projetoId_.queda-tensao.tsx`; Diagrama unifilar → `projetos.$projetoId_.unifilar.tsx`. Isso é o mecanismo pelo qual **todas** as funcionalidades do sistema original ficam acessíveis a partir do novo shell, sem reimplementar cada tela no novo design.
- **FR13:** O item "Diagnóstico" do menu é renomeado ou removido (decisão final de texto cabe a `@po`) — a rota real com esse nome é apenas health-check de conexão Supabase, não diagnóstico de conformidade do projeto; apontar para ela seria ativamente enganoso.
- **FR14:** `UnifilarPreviewSection` passa a receber `projetoId` real (já consome o `UnifilarWorkspace` de produção desde `SIE-DS-06` — apenas confirmar que nenhum fixture hardcoded restante seja usado).
- **FR15:** A feature flag `VITE_FEATURE_SIE_COMMAND_CENTER` continua controlando acesso à rota inteira, com o mesmo comportamento de "preview desabilitado" quando `false`.
- **FR16:** A rota antiga `/sie-command-center-preview` é removida (não mantida em paralelo).

### 2.2 Non Functional

- **NFR1:** Nenhum dado exibido pode ser inventado, estimado ou mockado onde não exista cálculo/valor real equivalente — quando não há equivalente, o campo é removido, nunca substituído por placeholder (Artigo IV — No Invention).
- **NFR2:** A integração deve tratar explicitamente estados vazios/loading do React Query (projeto sem circuitos, sem queda de tensão calculada ainda) — o mock sempre populava dado, o real pode não ter.
- **NFR3:** Zero regressão de performance perceptível: os hooks reais usados já existem e já são consumidos pelas telas de produção equivalentes; nenhuma chamada duplicada de rede deve ser introduzida além do que as telas legadas já fazem.
- **NFR4:** Acessibilidade existente do design system (ARIA, foco, `aria-live`) deve ser preservada integralmente — nenhuma mudança de marcação além da estritamente necessária para o 3º estado de badge (FR7).
- **NFR5:** O front-end deve respeitar RLS do Supabase como já ocorre nas telas legadas — ausência de policy resulta em array vazio (estado vazio tratado), nunca em erro não tratado.
- **NFR6:** Qualquer limitação de qualidade herdada (ex.: indisponibilidade do binário CodeRabbit, já registrada em `SIE-DS-00` a `SIE-DS-07`) deve ser declarada com honestidade no fechamento de cada story, não mascarada.

### 2.3 Compatibility Requirements

- **CR1:** Nenhum endpoint novo é criado — toda a integração consome os ~35 endpoints de `src/routes/api/v1/**` e hooks de `src/hooks/queries.ts` já existentes e já usados pelas telas legadas.
- **CR2:** Nenhuma migration nova, nenhuma alteração de schema Supabase — a implantação é 100% leitura/escrita via serviços de domínio já existentes (`src/domain/servicos/**`).
- **CR3:** Zero alteração de CSS/layout/estrutura visual do Command Center, exceto a exceção pontual e documentada do 3º estado de badge (FR7), que reusa tokens de severidade já existentes.
- **CR4:** As rotas de produção legadas (`projetos.$projetoId_.correntes.tsx`, `...dimensionamento-condutores.tsx`, etc.) e `AppShell.tsx` permanecem intocadas — `git diff` vazio para esses caminhos é critério de aceite em nível de projeto.

---

## 3. User Interface Enhancement Goals

### 3.1 Integration with Existing UI

O Command Center já implementa o design system alvo integralmente (`src/components/command-center/**`, tokens `--sie-cc-*` ratificados em `SIE-DS-00`, protótipo espelhado em `outputs/design-system/sie-command-center/prototype/`). Esta implantação **não adiciona nem redesenha nenhum componente visual** — troca exclusivamente a fonte de dado de cada organism já existente, preservando props shape sempre que possível (mudança de tipo do dado, não de estrutura de UI), com a única exceção documentada do campo de justificativa em `DecisionPanel` (FR11, exigido por comportamento real mais rigoroso, não por preferência estética).

### 3.2 Modified/New Screens and Views

| Tela/organism | Mudança |
|---|---|
| Rota `/sie-command-center-preview` | Removida, substituída por `/projetos/$projetoId/command-center` |
| `MetricCardGrid`, `WorkflowStepper`, `EngineeringPanel`, `ContextInspector`, `ParameterPanel`, `ResultSummary`, `DecisionPanel`, `ModuleNavigation`, `UnifilarPreviewSection` | Fonte de dado trocada de mock para real (ver FR3-FR14) |
| `EngineeringShell` (seletor de projeto) | Handler de troca de projeto passa a navegar de fato (FR2) |
| Telas legadas (ambientes, padrão de entrada, circuitos, correntes, condutores, queda de tensão, unifilar) | **Nenhuma mudança** — continuam existindo como estão, acessadas via `ModuleNavigation` (FR12) |

### 3.3 UI Consistency Requirements

- Nenhum arquivo `.css` de `command-center/` é modificado, exceto se estritamente necessário para o 3º estado de badge — nesse caso, a exceção deve ser documentada explicitamente na story correspondente, não é permitido alterar layout, espaçamento ou tipografia.
- Nenhum estilo inline novo.
- Densidade `comfortable`/`compact` (já suportada globalmente via `data-density`) não é afetada.

---

## 4. Technical Constraints and Integration Requirements

### 4.1 Existing Technology Stack

```
Linguagens: TypeScript (strict), React 19
Frameworks: TanStack Start (SSR) + TanStack Query + TanStack Router; Carbon Design System (componentes de produção); design system próprio do Command Center (tokens --sie-cc-*, sem Carbon)
Banco: Supabase/PostgreSQL — tabelas de projeto: public.projetos, dependencias (+ tabelas filhas: dependencia_bancadas, dependencia_cargas_adicionais, dependencia_edicoes_manuais, dependencia_validacao, dependencia_retornos_downstream), parametros_edp_overrides, dimensionamento_condutores_overrides, dimensionamento_condutores_resultado, queda_tensao_config, eventos_auditoria. Tabelas normativas MOD-DC (mod_dc_tabela_iz e correlatas) são referência, não dado de projeto.
Infraestrutura: build SSR via vite.config.ts; build SPA estático via vite.spa.config.ts + scripts/static-server.mjs (porta default 4321)
Dependências externas: nenhuma nova — API v1 interna já cobre 100% do escopo
```

### 4.2 Integration Approach

```
Database Integration Strategy: nenhuma — leitura/escrita via serviços de domínio já existentes, sem acesso direto a tabela pelo Command Center
API Integration Strategy: consumo direto dos hooks já catalogados em src/hooks/queries.ts (projetoQuery, divisaoCircuitosQuery, quedaTensaoLoteQuery, quedaTensaoResumoQuery, parametrosEDPQuery, e demais conforme FR9/FR11), sem endpoint novo
Frontend Integration Strategy: troca de import de arquivo *-data.ts por hook real dentro do mesmo organism; estado elevado (ex.: circuito selecionado) permanece como já está
Testing Integration Strategy: reuso do padrão de testes já usado nas telas legadas (Vitest + Testing Library) e nos testes VRT existentes do Command Center; estados vazios/loading (NFR2) precisam de cobertura nova
```

### 4.3 Code Organization and Standards

```
File Structure Approach: nova rota segue a convenção projetos.$projetoId_.{nome}.tsx já usada por todas as demais rotas de projeto
Naming Conventions: preservadas as já existentes no submódulo (português para domínio/UI, inglês para infraestrutura)
Coding Standards: TypeScript strict, ESLint já configurado no submódulo — sem novidade
Documentation Standards: Pattern Library (docs/architecture/SIE-COMMAND-CENTER-PATTERN-LIBRARY.md) deve ser atualizada ao final para refletir que os organisms deixaram de ser ilustrativos
```

### 4.4 Deployment and Operations

```
Build Process Integration: nenhuma mudança — mesma pipeline de build SSR/SPA já existente
Deployment Strategy: feature flag VITE_FEATURE_SIE_COMMAND_CENTER permite rollout gradual e rollback instantâneo sem redeploy de código
Monitoring and Logging: eventos_auditoria já registra aplicação de cenário de queda de tensão (QUEDA_TENSAO_CENARIO_APLICADO) — nenhum novo mecanismo de log é necessário
Configuration Management: nenhuma variável de ambiente nova além da flag já existente
```

### 4.5 Risk Assessment and Mitigation

```
Technical Risks:
  R1 — o id "proj-1" citado na solicitação original não corresponde a um projeto real seedado no banco (é id de fixture de teste). Testar/demonstrar a implantação requer um projeto real existente no ambiente-alvo, criado pelo fluxo real (POST /projetos + dependências), não um id fixo assumido.
  R2 — projeto real sem circuitos/queda de tensão calculada ainda (estado vazio) pode quebrar organisms que o mock sempre populava — mitigado por NFR2.
  R3 — inferência de ativo/completo do WorkflowStepper (FR5) não tem regra normativa formal — é heurística de navegação, não cálculo de engenharia; risco baixo, mas deve ser revisada por @po.

Integration Risks:
  R4 — todas as 8 stories já entregues do Command Center (SIE-DS-LOCAL-01 a SIE-DS-07) fecharam com gate CONCERNS, não PASS, por indisponibilidade recorrente do binário CodeRabbit (WSL) — débito de qualidade herdado, não desta implantação, mas que se estende a ela se não for resolvido por @devops.

Deployment Risks:
  R5 — nenhum, dado que a feature flag já isola o rollout; risco de deploy é equivalente a zero enquanto a flag permanecer controlável sem redeploy.

Mitigation Strategies:
  R1 → story declara explicitamente qual projeto real foi usado para verificação, nunca assume "proj-1" sem confirmar que existe
  R2 → AC de cada story exige tratamento de estado vazio/loading, não apenas o caminho feliz
  R3 → regra de inferência documentada em Dev Notes e revisada por @po antes de Done
  R4 → cada story declara o status real do CodeRabbit no fechamento (não mascarar), conforme já é prática desde SIE-DS-00
```

---

## 5. Epic and Story Structure

**Epic Structure Decision:** Epic único, com 2 stories sequenciais, porque a decisão arquitetural (DECISION-SIE-DS-08) já particionou o trabalho em exatamente 2 metades coesas — rota+Overview (métricas, tabela de circuitos, inspector) e queda-de-tensão-completa+navegação (parâmetros, resultado, decisão, `ModuleNavigation`, ajustes semânticos). Múltiplos epics não se justificam: é uma única capacidade de produto (Command Center operando com dado real) entregue em 2 incrementos verificáveis, cada um preservando o sistema legado intacto.

---

## 6. Epic 1: Implantação do SIE Command Center sobre Dados Reais

**Epic Goal:** Fazer o SIE Command Center, já construído visualmente, operar como superfície de trabalho real sobre projetos existentes — substituindo 100% dos dados ilustrativos por dado calculado/cadastrado no sistema original, dando acesso a todas as funcionalidades reais via navegação real, sem alterar nenhum pixel do design nem tocar no sistema legado.

**Integration Requirements:** Toda integração consome hooks/endpoints/serviços já existentes (FR1-FR16, CR1-CR4); nenhum backend novo; feature flag `VITE_FEATURE_SIE_COMMAND_CENTER` controla o rollout completo.

### Story 1.1 — `SIE-DS-08`: Rota com contexto de projeto + Overview real

**Status atual:** Draft, já existente em `docs/stories/story-SIE-DS-08-integracao-rota-projeto-overview-real.md` — este PRD **não substitui** essa story, apenas a referencia como Story 1.1 deste epic. Cabe a `@po` validá-la (`*validate-story-draft`) antes de `@dev` iniciar.

Como projetista usando o SIE,
eu quero que o SIE Command Center opere sobre um projeto real e mostre circuitos, métricas de conformidade e demanda reais,
para que o novo design deixe de ser um protótipo visual e passe a ser uma superfície de trabalho de verdade.

**Acceptance Criteria (resumo — ver story completa para os 10 ACs detalhados):** migração de rota (FR1, FR16); seletor de projeto funcional (FR2); `MetricCardGrid`/`WorkflowStepper` reais, sem percentual inventado (FR3-FR5); `EngineeringPanel`/`ContextInspector` reais com 3 estados de badge (FR6-FR8); zero alteração de design/zero impacto no legado (CR3, CR4).

**Integration Verification:**
1. IV1: rotas legadas (`correntes`, `dimensionamento-condutores`, `padrao-entrada`, `unifilar`) continuam funcionando sem alteração — `git diff` vazio.
2. IV2: `projetoQuery`/`divisaoCircuitosQuery`/`quedaTensaoLoteQuery`/`quedaTensaoResumoQuery`/`parametrosEDPQuery` retornam dado consistente com o que as telas legadas já exibem para o mesmo projeto.
3. IV3: nenhuma chamada de rede duplicada é introduzida além das já feitas pelas telas legadas equivalentes.

### Story 1.2 — `SIE-DS-09`: Queda de tensão completa, decisão e navegação real (a formalizar por `@sm`)

**Status:** ainda não existe como arquivo de story — este PRD define o objetivo e critérios candidatos; `@sm` deve executar `*draft` para formalizá-la seguindo o mesmo padrão de `SIE-DS-08`.

Como projetista usando o SIE,
eu quero inspecionar parâmetros e resultados reais de queda de tensão, simular e aplicar cenários alternativos com justificativa, e navegar para qualquer área funcional do sistema a partir do Command Center,
para que o fluxo de decisão técnica completo (não apenas a visão geral) opere sobre dado real.

**Acceptance Criteria (candidatos):**
1. `ParameterPanel`/`ResultSummary` exibem parâmetros e resultados reais de queda de tensão por circuito (FR9), com vocabulário do catálogo real de impedâncias em vez de "método B1" (FR10).
2. `DecisionPanel` simula cenários via `simularCenarios()` e aplica via `aplicarCenario()`, com campo de justificativa obrigatório (FR11) — nova exigência de UI justificada por comportamento real, registrada explicitamente como exceção ao CR3.
3. `ModuleNavigation` aponta para as rotas reais de todas as áreas funcionais (FR12).
4. Item "Diagnóstico" renomeado ou removido, com decisão de texto validada por `@po` (FR13).
5. `UnifilarPreviewSection` confirmado sem fixture hardcoded remanescente (FR14).
6. Zero alteração de design visual além do campo de justificativa já ressalvado; zero impacto no legado.

**Integration Verification:**
1. IV1: `aplicarCenario()` sem justificativa continua sendo rejeitado pela API real (`AplicacaoCenarioInvalida`) — o Command Center não contorna essa regra.
2. IV2: navegação real do `ModuleNavigation` leva às mesmas rotas que o menu de produção legado usa.
3. IV3: `eventos_auditoria` recebe o mesmo registro (`QUEDA_TENSAO_CENARIO_APLICADO`) independentemente de a aplicação ter sido feita pela tela legada ou pelo Command Center.

---

## 7. Handoff

- **`@po`** — validar `story-SIE-DS-08-integracao-rota-projeto-overview-real.md` (`*validate-story-draft`) contra este PRD; decidir o texto final do item "Diagnóstico" (FR13) quando `SIE-DS-09` for formalizada.
- **`@sm`** — formalizar `SIE-DS-09` (`*draft`) usando a Story 1.2 acima como insumo, seguindo o mesmo padrão de `SIE-DS-08`.
- **`@architect`** — este PRD não introduz nenhuma decisão arquitetural nova além do que já está ratificado em `DECISION-SIE-DS-08-integracao-dados-reais.md`; nenhuma ratificação adicional é necessária a menos que `@sm`/`@dev` encontrem um ponto não coberto durante `SIE-DS-09`.
- **`@devops`** — débito conhecido (R4): resolver indisponibilidade do binário CodeRabbit antes que a implantação acumule uma 10ª story consecutiva sem gate limpo.

---

— Morgan, planejando o futuro 📊
