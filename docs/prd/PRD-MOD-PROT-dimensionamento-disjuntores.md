# PRD — Módulo de Dimensionamento de Disjuntores (MOD-PROT)

**Produto:** SIE — Sistema de Instalações Elétricas
**Módulo:** MOD-PROT v1.0 (novo)
**Rota/Slug:** `dimensionamento-disjuntores`
**Tipo:** PRD Brownfield (integração a sistema existente)
**Autor:** Morgan (@pm) — AIOX
**Data:** 2026-08-04
**Status:** Draft — aguardando validação (@po) e decisão arquitetural (@architect)
**Documento-base:** `docs/research/2026-08-04-research-prompt-dimensionamento-disjuntores.md`
**Execução:** Pre-Flight Planning — ambiguidades resolvidas com o usuário antes da redação (ver Seção 0)

---

## 0. Decisões de Pre-Flight (premissas validadas com o usuário)

| # | Decisão | Escolha |
|---|---------|---------|
| 1 | Nome da rota/slug | `dimensionamento-disjuntores` |
| 2 | Fonte do catálogo de disjuntores | Tabela normativa genérica no MVP; catálogos de fabricante (WEG, Siemens, ABB, Schneider) como fast-follow — sem prioridade definida entre eles neste PRD |
| 3 | Corrente de curto-circuito presumida (Icc) | Input manual do projetista neste incremento; cálculo automático de Icc fica **fora de escopo** |
| 4 | Relação com a heurística atual (`sugerirProtecaoCircuito`) | Mantida como sugestão inicial (fallback); motor MOD-PROT assume a resolução quando disponível; override manual por circuito segue o padrão `CircuitoOverride` do MOD-DC-HYBRID |
| 5 | Estrutura do epic | Epic único, convenção brownfield do template, com Icc fora de escopo |
| 6 | Prioridade/timeline | Sem prazo declarado — backlog sem data |
| 7 | Impacto no sistema existente | **Significant** (mudanças substanciais em código existente — toca MOD-DC e MOD-SEC) |

### 0.1 Correções pós-Impact Analysis (@architect, 2026-08-04)

`@architect *analyze-impact` (ver relatório associado a este PRD) encontrou dois pontos em que a redação inicial divergia de decisões e contratos já existentes no código. Correções aplicadas:

1. **Nomes de campo do resultado MOD-PROT alinhados a ADR anterior.** O ADR `docs/architecture/mod-dc-rotas-retorno-downstream.md` (Aria, 2026-07-12, Seção 6) já declarava o contrato do MOD-PROT como `{in, i2, norma_dispositivo, capacidade_interrupcao}`. Os campos `fonte_tabela`/`curva` propostos na primeira versão deste PRD foram substituídos por `norma_dispositivo` (curva/norma do dispositivo) e `capacidade_interrupcao` (Icu/Ics), evitando inventar um contrato paralelo (Artigo IV — No Invention). O literal `origem_in: "MOD-PROT"` já existe no type system (`contratos.ts:12`, `OrigemIn`) e passa a ser usado explicitamente para distinguir o motor completo da heurística de fallback (`origem_in: "SUGESTAO"`).
2. **Icc deixa de ser um campo de entrada duplicado.** A corrente de curto-circuito presumida (Icc) já tem canal canônico no sistema: o critério C3 (`retorno_cc.icc_presumida_a`, alimentado via `POST /api/v1/modulos/mod-cc/validar`, estado `AGUARDANDO-CC` até haver retorno). MOD-PROT passa a **ler** esse valor do circuito em vez de abrir um campo manual próprio — a decisão #3 (Icc manual, sem cálculo automático) continua válida; o que muda é o canal de entrada, evitando duas fontes de verdade para o mesmo dado.

Achado adicional incorporado às stories (não muda requisitos, adiciona verificação): `src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts` (épico AUTO-OTI) também consome `resolverParametrosCircuito` diretamente — incluído no escopo de regressão da Story 1.3.

A colisão de nomenclatura `MOD-CC` (Seção 1.1) foi reclassificada de "risco futuro" para **ativa hoje** — existe endpoint real `modulos.mod-cc.validar.ts` para "Curto-Circuito" convivendo com a rota de UI `command-center.tsx`. Não é responsabilidade deste epic corrigir, mas este epic não deve introduzir nenhum uso adicional de `MOD-CC`.

---

## 1. Intro Project Analysis and Context

### 1.1 Existing Project Overview

**Analysis Source:** IDE-based fresh analysis (Atlas/@analyst via `*research-prompt`, seguida de análise de código por @pm) — sem execução prévia de `document-project`.

**Current Project State:** O SIE é um sistema de engenharia assistida para projetos de instalações elétricas de baixa tensão, conforme ABNT NBR 5410:2004 e o padrão EDP São Paulo. Já possui módulos operacionais completos com rota própria, motor de domínio, persistência Supabase e tutorial: **MOD-DC** (dimensionamento de condutores, incl. épico `MOD-DC-HYBRID` de overrides por circuito), **MOD-QT** (queda de tensão, com catálogo de impedâncias versionado por fabricante), e **MOD-SEC** (validação de seccionamento automático, critério C4, `Done` desde 2026-07-15). O nome **MOD-PROT** já havia sido reservado para este módulo desde 2026-07-12 no `PRD-MOD-DC-modulo-dimensionamento-condutores.md` (linha 29: "Proteção (MOD-PROT) | Futuro | Contrato; In/I2 como entrada ou sugestão") — este PRD entrega esse módulo pendente.

**Atenção de nomenclatura (ativa, confirmada por `*analyze-impact`):** o código `MOD-CC` já está em uso **duplo e simultâneo** no sistema: (a) como rota de UI **Command Center** (`projetos.$projetoId_.command-center.tsx`, épico `EPIC-MOD-CC-SEC-QT`) e (b) como módulo de API **Curto-Circuito** (critério C3, NBR 5410 5.3.5), com endpoint real `POST /api/v1/modulos/mod-cc/validar` (`src/routes/api/v1/modulos.mod-cc.validar.ts`), schema `RetornoMODCCSchema`/`ValidarMODCCSchema` e testes (`tests/api/modulos-mod-cc.test.ts`). Esta é uma ambiguidade de nomenclatura pré-existente e já commitada — não é escopo deste epic resolvê-la, mas este PRD **não introduz nenhum uso novo do código `MOD-CC`** e reaproveita o canal `retorno_cc` do critério C3 (ver Seção 0.1) só como fonte de leitura de Icc.

### 1.2 Available Documentation Analysis

- [x] Tech Stack Documentation — `sistema-de-instala-es-el-tricas-sie-main/CLAUDE.md`
- [x] Source Tree/Architecture — idem
- [ ] Coding Standards — parcial (convenções observadas no código, não documento formal)
- [x] API Documentation — parcial, por padrão de rotas `api/v1/modulos.*`
- [ ] External API Documentation — N/A
- [ ] UX/UI Guidelines — parcial (IBM Carbon Design System observado, sem guia formal)
- [x] Technical Debt Documentation — auditorias em `docs/research/` (2026-06-21, 2026-07-07)
- Other: `PRD-MOD-DC-modulo-dimensionamento-condutores.md` já antecipa o contrato de MOD-PROT (FR6, FR19, seção Fora de Escopo)

### 1.3 Enhancement Scope Definition

**Enhancement Type:**
- [x] New Feature Addition
- [x] Integration with New Systems (integra com MOD-DC e MOD-SEC existentes)

**Enhancement Description:** Criar o módulo MOD-PROT como seção de primeira classe (rota, motor normativo, persistência, tutorial) para dimensionamento de disjuntores — hoje resolvido apenas por uma heurística provisória embutida no MOD-DC (`motor-protecao.ts`). O módulo deve calcular In/curva/verificação de poder de interrupção e se tornar a fonte real de `tempo_atuacao_s` hoje exigido externamente pelo MOD-SEC.

**Impact Assessment:**
- [x] Significant Impact (substantial existing code changes) — confirmado pelo usuário (decisão #7). Toca o ponto de integração `aplicarSugestaoProtecaoSeAusente` em `src/domain/dimensionamento-condutores/overrides.ts` e o contrato de entrada do MOD-SEC (`tempo_atuacao_s`).

### 1.4 Goals and Background Context

**Goals:**
- Substituir a heurística provisória de sugestão de disjuntor por um motor normativo real, com fonte declarada e rastreável.
- Verificar poder de interrupção (Icu/Ics) do disjuntor contra a corrente de curto-circuito informada, hoje não verificado por lugar nenhum do sistema.
- Tornar-se a fonte real de `tempo_atuacao_s` para o MOD-SEC, eliminando a dependência de valor externo não rastreado.
- Entregar a seção completa (rota, persistência, tutorial) seguindo exatamente o padrão já validado por MOD-DC e MOD-QT.
- Preservar 100% de compatibilidade com os critérios C2 (sobrecarga) e C4 (seccionamento) já implementados.

**Background Context:** A auditoria de efetividade de 2026-07-07 já apontava "proteção" como funcionalidade inexistente no sistema. O código confirma isso: `motor-protecao.ts::sugerirProtecaoCircuito()` escolhe In numa série fixa (6 a 63 A) e calcula I2 = 1,45×In sem qualquer verificação de curva de disparo ou poder de interrupção — a própria função rotula o resultado como `"SUGESTAO"` provisória. O PRD original do MOD-DC (2026-07-12) já havia planejado este módulo como dependência futura (FR6, FR19) e explicitamente o excluiu do escopo do MOD-DC ("Seleção definitiva de dispositivos de proteção (MOD-PROT) — In como entrada/sugestão"). Este PRD fecha essa lacuna.

### 1.5 Change Log

| Change | Date | Version | Description | Author |
|--------|------|---------|--------------|--------|
| Criação | 2026-08-04 | 1.0 | PRD inicial baseado em `2026-08-04-research-prompt-dimensionamento-disjuntores.md` | Morgan (@pm) |

---

## 2. Requirements

> Estes requisitos se baseiam no meu entendimento do sistema existente (MOD-DC, MOD-QT, MOD-SEC) obtido por leitura direta do código-fonte e dos PRDs/stories já publicados. Por favor revise com atenção e confirme se alinham com a realidade do seu projeto.

### Functional

- **FR1:** MOD-PROT deve calcular a corrente nominal (In) e a corrente convencional de atuação (I2) do disjuntor a partir da corrente de projeto (IB) fornecida pelo MOD-DC e do tipo de instalação, publicando o resultado com `origem_in: "MOD-PROT"` (literal já existente em `OrigemIn`, `contratos.ts:12`, distinto de `"SUGESTAO"` da heurística de fallback) e o critério de seleção rastreável.
- **FR2:** MOD-PROT deve suportar múltiplas fontes/tabelas de disjuntores como opções configuráveis: (a) tabela normativa genérica, não amarrada a fabricante, adotada como padrão no MVP; (b) catálogos de fabricante como fast-follow, com suporte planejado para WEG, Siemens, ABB e Schneider, sem ordem de prioridade definida neste PRD. A fonte/norma ativa deve ser declarada no resultado no campo `norma_dispositivo` (nome já reservado pelo ADR `docs/architecture/mod-dc-rotas-retorno-downstream.md` §6 — não inventar campo paralelo como `fonte_tabela`).
- **FR3:** MOD-PROT deve selecionar a curva de disparo (B/C/D) conforme o tipo de carga/instalação informado, publicando a decisão no mesmo campo `norma_dispositivo`, com fallback declarado e rastreável quando a informação não estiver disponível.
- **FR4:** MOD-PROT deve verificar o poder de interrupção (`capacidade_interrupcao` — Icu/Ics, nome de campo conforme o ADR citado em FR2) do disjuntor selecionado contra a corrente de curto-circuito presumida (Icc). Icc **não é um campo de entrada próprio de MOD-PROT** — é lida do canal já existente do critério C3 (`retorno_cc.icc_presumida_a`, alimentado via `POST /api/v1/modulos/mod-cc/validar`). Enquanto o circuito estiver em `AGUARDANDO-CC` (sem retorno registrado), MOD-PROT publica pendência `PENDENTE-ICC` e segue sem bloquear In/I2. Continua sem cálculo automático de Icc no sistema (ver Fora de Escopo) — decisão #3 preservada, apenas o canal de entrada muda.
- **FR5:** A heurística atual (`sugerirProtecaoCircuito`, `src/domain/dimensionamento-condutores/motores/motor-protecao.ts`) permanece como sugestão inicial de In/I2 (fallback, `origem_in: "SUGESTAO"`) quando o motor MOD-PROT completo não puder resolver. O motor MOD-PROT assume a resolução principal (`origem_in: "MOD-PROT"`) quando disponível. Overrides manuais por circuito seguem o mesmo padrão de `CircuitoOverride` (useGlobal / customParams / justificativa obrigatória) já validado no épico `MOD-DC-HYBRID`.
- **FR6:** MOD-PROT deve publicar um resultado contendo `in_a`, `i2_a`, `origem_in`, `norma_dispositivo`, `capacidade_interrupcao`, `tempo_atuacao_s` (derivado da curva selecionada) e `pendencias`, consumível pelo MOD-DC (critério C2 — sobrecarga, já implementado em `motor-sobrecarga.ts`). Campos alinhados ao contrato já declarado em `docs/architecture/mod-dc-rotas-retorno-downstream.md` §6.
  > **Escopo reduzido, ratificado por @po em 2026-08-05 (validação da Story MOD-PROT-3):** esta story **expõe** `tempo_atuacao_s` no resultado, mas não orquestra automaticamente a chamada a `POST /api/v1/modulos/mod-sec/validar` — nenhum código do repositório chama esse endpoint hoje (achado do ADR `mod-prot-contrato-integracao.md`, Decisão D6), e criar um orquestrador novo só para isso seria invenção fora do escopo validado. Orquestração automática MOD-PROT → MOD-SEC fica como trabalho futuro (D6-b do ADR).
- **FR7:** A seção deve ter rota própria de UI (`projetos/$projetoId_/dimensionamento-disjuntores`), seguindo o padrão de layout já usado em `dimensionamento-condutores` e `queda-tensao` (`SieShell`, `SiePageHero`, componentes IBM Carbon).
- **FR8:** A seção deve persistir os overrides por circuito em tabela(s) Supabase própria(s), seguindo o padrão de repositório (`infra/repositorios` + `infra/supabase`) já usado pelo MOD-DC.
- **FR9:** Toda decisão automática (sugestão) e manual (override) deve ser rastreável em `resultado.rastreio`, incluindo fonte da tabela, curva escolhida e justificativa — seguindo o mesmo padrão do critério C4 do MOD-SEC.
- **FR10:** A seção deve ter tutorial didático (par `.md`/`.html`) sincronizado via o mecanismo de manifest já existente no projeto (`scripts/tutorial-*-manifest.mjs`), cobrindo os campos, fórmulas e mensagens introduzidos, com checagem obrigatória via `npm run docs:tutorial:check`.

### Non Functional

- **NFR1:** A integração com o MOD-DC deve ocorrer no ponto de extensão já existente (`aplicarSugestaoProtecaoSeAusente`, em `src/domain/dimensionamento-condutores/overrides.ts`), preservando a assinatura de retorno atual (`in_a`, `origem_in`, `i2_a`, `fonte_i2`) para não quebrar os critérios C2/C3 já implementados em `motor-sobrecarga.ts`.
- **NFR2:** A troca de fonte de tabela de disjuntores (genérica → fabricante) não deve invalidar resultados já persistidos; requer versionamento de catálogo análogo ao usado em `impedancias-prysmian-rev10.ts` (MOD-QT).
- **NFR3:** Cobertura de testes unitários para os critérios normativos (seleção de In, curva, verificação de Icu/Ics) equivalente ao padrão já usado nos motores de MOD-DC (ex.: `motor-sobrecarga.test.ts`).
- **NFR4:** Compatibilidade com o RLS já configurado nas demais tabelas do domínio (política `anon_all_<tabela>` documentada no `CLAUDE.md` do submódulo).

### Compatibility Requirements

- **CR1:** {{existing_api_compatibility}} — A API/contrato atual do MOD-DC que consome `in_a`/`i2_a`/`origem_in`/`fonte_i2` deve continuar funcionando sem alteração de assinatura.
- **CR2:** {{database_schema_compatibility}} — Nova(s) tabela(s) Supabase não devem alterar o schema das tabelas existentes (`dependencia_*`, `parametros_edp_overrides`, `queda_tensao_config`), apenas adicionar tabela(s) nova(s).
- **CR3:** {{ui_ux_consistency}} — UI deve seguir os componentes e padrões visuais já em uso (IBM Carbon Design System, `SieShell`, `SiePageHero`, `LoadingTabela`, `ErrorState`, `TutorialModal`).
- **CR4:** {{integration_compatibility}} — O contrato do MOD-SEC (`POST /api/v1/modulos/mod-sec/validar`, campo `tempo_atuacao_s`) deve continuar aceitando o formato atual; MOD-PROT passa a ser uma **fonte possível** desse valor, não uma mudança de contrato do MOD-SEC.
- **CR5:** MOD-PROT deve **ler** (não persistir de forma paralela) o campo `retorno_cc.icc_presumida_a` já existente no circuito (canal do critério C3/MOD-CC); nenhuma mudança no contrato de `POST /api/v1/modulos/mod-cc/validar` ou no schema `RetornoMODCCSchema`.

---

## 3. User Interface Enhancement Goals

### Integration with Existing UI

A nova seção deve reutilizar integralmente os padrões visuais e de composição já estabelecidos em `dimensionamento-condutores.tsx` e `queda-tensao.tsx`: shell (`SieShell`), cabeçalho (`SiePageHero`), estados de carregamento/erro (`LoadingTabela`, `ErrorState`), componentes Carbon (`Button`, `Select`, `SelectItem`, `NumberInput`, `Tag`, `InlineNotification`) e um componente de resumo dedicado (análogo a `DimensionamentoCondutoresResumo`), aqui `DimensionamentoDisjuntoresResumo`.

### Modified/New Screens and Views

- **Nova:** `projetos/$projetoId_/dimensionamento-disjuntores` — tela principal da seção (parâmetros globais, overrides por circuito, resultado por circuito).
- **Modificada:** nav/menu do `SieShell` — novo item de navegação (cobrir com o teste já existente `tests/ui/projeto-detalhe-nav-links.test.ts`).
- **Modificada (opcional, avaliar com @architect):** `command-center.tsx` — possível card de KPI de proteção; não obrigatório neste incremento.

### UI Consistency Requirements

- Reutilizar exatamente os mesmos componentes Carbon e wrappers de estado (loading/erro) já usados nas demais seções — sem introduzir biblioteca ou padrão visual novo.
- Seguir a mesma estrutura de rota (`createFileRoute`, `head.meta` com título e descrição do módulo) usada em `dimensionamento-condutores.tsx`.
- Tutorial injetado via `TutorialModal.tsx` com o mesmo wrapper CSS (`.tutorial-wrapper`) das demais seções.

---

## 4. Technical Constraints and Integration Requirements

### Existing Technology Stack

**Languages**: TypeScript (strict)
**Frameworks**: TanStack Start (SSR) / React 19 + Vite (SPA estático), IBM Carbon Design System, TanStack Query
**Database**: Supabase / PostgreSQL (com RLS)
**Infrastructure**: dual-mode SSR (Node, dev local) + SPA estático (deploy Hostinger, sem Node)
**External Dependencies**: nenhuma nova dependência de runtime identificada; fonte de dados do catálogo genérico pode ser um arquivo estático versionado (`.ts`/`.json`), seguindo o padrão de `impedancias-prysmian-rev10.json`

### Integration Approach

**Database Integration Strategy**: nova tabela Supabase dedicada a overrides/resultados de MOD-PROT, seguindo o padrão de `queda_tensao_config` (migration própria em `supabase/migrations/`) e política RLS `anon_all_<tabela>` para o modo SPA.

**API Integration Strategy**: nova(s) rota(s) server-side em `src/routes/api/v1/modulos/mod-prot.*.ts`, seguindo o padrão de `modulos.mod-sec.validar.ts` (schema Zod de entrada/saída, `withZod`, timeout/erro tratado). Alteração pontual em `src/domain/dimensionamento-condutores/overrides.ts::aplicarSugestaoProtecaoSeAusente` para consumir o novo motor em vez de chamar `sugerirProtecaoCircuito` diretamente. O motor MOD-PROT lê `retorno_cc.icc_presumida_a` do circuito já resolvido pelo MOD-DC (mesmo objeto usado pelo critério C3) — não chama `POST /api/v1/modulos/mod-cc/validar` diretamente nem duplica esse estado.

**Frontend Integration Strategy**: nova entrada em `hooks/queries.ts`, nova fachada em `lib/api-client.ts` (mesmo padrão de `dimensionarCondutoresLote`), nova rota React seguindo o padrão descrito na Seção 3. Lembrar de atualizar `src/routeTree.spa.ts` manualmente (armadilha documentada no `CLAUDE.md` do submódulo — regeneração de `routeTree.gen.ts` não propaga automaticamente).

**Testing Integration Strategy**: testes de domínio (Vitest) para os motores normativos (padrão `motor-sobrecarga.test.ts`), teste de integração de API (padrão `tests/api/queda-tensao-endpoints.test.ts`), teste de contrato no ponto de integração com MOD-DC (`overrides.ts`) e com MOD-SEC, teste de nav link (`tests/ui/projeto-detalhe-nav-links.test.ts`), e teste de regressão cobrindo `src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts` (consumidor de `resolverParametrosCircuito` do épico AUTO-OTI, identificado no `*analyze-impact`).

### Code Organization and Standards

**File Structure Approach**: nova pasta `src/domain/dimensionamento-disjuntores/` (contratos, motores, overrides), espelhando a estrutura de `src/domain/dimensionamento-condutores/`.
**Naming Conventions**: módulo lógico **MOD-PROT** (nome já reservado desde 2026-07-12); rota/slug `dimensionamento-disjuntores`; evitar terminantemente o código `MOD-CC` — já em uso ativo e duplo no projeto (Command Center na UI **e** Curto-Circuito na API, ver Seção 1.1) — e `MOD-DISJ` (não usado no projeto, descartado em favor de manter consistência com o PRD original do MOD-DC). Nomes de campo do resultado seguem o contrato já declarado em `docs/architecture/mod-dc-rotas-retorno-downstream.md` §6: `in`, `i2`, `norma_dispositivo`, `capacidade_interrupcao` (mapeados para `in_a`/`i2_a`/`norma_dispositivo`/`capacidade_interrupcao` no TypeScript, seguindo a convenção de sufixo `_a` para grandezas em ampere já usada em `contratos.ts`).
**Coding Standards**: TypeScript strict, ESLint, funções puras no domínio (zero dependências externas), sem uso de `any`.
**Documentation Standards**: tutorial obrigatório (par `.md`/`.html`) com entrada em manifesto de hashes, conforme regra do `CLAUDE.md` do submódulo.

### Deployment and Operations

**Build Process Integration**: nenhuma mudança no pipeline de build; validar `npx tsc --noEmit` e `npx eslint .` antes de commit.
**Deployment Strategy**: seguir `docs/DEPLOY-SPA-HOSTINGER.md`; atenção especial à armadilha de `routeTree.spa.ts` desatualizado (nova rota some do build SPA se não for adicionada manualmente).
**Monitoring and Logging**: nenhum mecanismo de monitoramento dedicado identificado além de `eventos_auditoria` (log de auditoria imutável) — reutilizar para overrides manuais de disjuntor.
**Configuration Management**: nenhuma variável de ambiente nova prevista; catálogo genérico como arquivo versionado no repositório.

### Risk Assessment and Mitigation

**Technical Risks**: fonte definitiva de catálogo de fabricante ainda não decidida (decisão adiada — FR2); tabela genérica do MVP pode divergir de catálogos reais quando o fast-follow for implementado, exigindo ajuste de contrato.
**Integration Risks**: `aplicarSugestaoProtecaoSeAusente` em `overrides.ts` é um ponto único de acoplamento com o MOD-DC — mudança de assinatura ali quebra silenciosamente os critérios C2/C3 já implementados; contrato com MOD-SEC (`tempo_atuacao_s`) tem o mesmo risco caso o formato mude; `resolverParametrosCircuito` também é consumido diretamente por `auto-otimizacao-retencao.ts` (épico AUTO-OTI), fora do fluxo principal do MOD-DC — risco de regressão silenciosa se não coberto por teste dedicado (ver Story 1.3).
**Deployment Risks**: esquecer de atualizar `routeTree.spa.ts` (armadilha já documentada e responsável por quebras de build SPA anteriores no projeto); esquecer de atualizar o manifest do tutorial (bloqueado por pre-commit hook e CI, mas passível de bypass com `--no-verify`).
**Mitigation Strategies**: testes de contrato no ponto de integração (`overrides.ts`, endpoint MOD-SEC); checklist de deploy já existente (`docs/DEPLOY-SPA-HOSTINGER.md`); não usar `--no-verify` ao commitar mudanças de UI/domínio desta seção.

---

## 5. Epic and Story Structure

### Epic Approach

**Epic Structure Decision**: Epic único, cobrindo motor normativo, persistência, integração com MOD-DC/MOD-SEC, UI e tutorial — seguindo a convenção brownfield do próprio template (favorecer epic único quando o trabalho é uma única entrega coesa) e a decisão explícita do usuário (#5) de manter o cálculo de Icc fora de escopo, o que evita que este epic dependa de um módulo de curto-circuito ainda inexistente.

---

## 6. Epic 1: Dimensionamento de Disjuntores (MOD-PROT)

**Epic Goal**: Entregar o módulo MOD-PROT como seção de primeira classe do SIE, substituindo a heurística provisória de sugestão de proteção por um motor normativo rastreável, com verificação de poder de interrupção contra Icc informado manualmente, tornando-se a fonte real de `tempo_atuacao_s` para o MOD-SEC — sem quebrar o MOD-DC existente.

**Integration Requirements**: Integração no ponto de extensão `aplicarSugestaoProtecaoSeAusente` (`overrides.ts`, MOD-DC) e no contrato de entrada do endpoint `POST /api/v1/modulos/mod-sec/validar` (MOD-SEC), preservando assinaturas atuais (CR1, CR4).

### Story 1.1 Motor Normativo de Seleção de Disjuntor

As a engenheiro eletricista,
I want que o sistema calcule In, curva de disparo e verifique o poder de interrupção do disjuntor a partir de IB, tipo de instalação/carga e Icc informado,
so that a seleção de proteção tenha fundamentação normativa rastreável em vez de uma série fixa com fator genérico.

**Acceptance Criteria**
1: Dado IB e tipo de instalação, o motor retorna In com `origem_in: "MOD-PROT"` seguindo a tabela normativa genérica (fonte declarada em `norma_dispositivo`).
2: Dado o tipo de carga/instalação, o motor seleciona curva de disparo (B/C/D) com fallback declarado quando a informação não estiver disponível, publicado em `norma_dispositivo`.
3: Dado `retorno_cc.icc_presumida_a` já disponível no circuito (canal C3/MOD-CC), o motor verifica `capacidade_interrupcao` (Icu/Ics) do disjuntor selecionado e marca reprovação quando insuficiente.
4: Quando o circuito ainda está em `AGUARDANDO-CC` (sem `retorno_cc`), o resultado retorna pendência explícita `PENDENTE-ICC` sem bloquear o restante do fluxo de sugestão de In/I2.
5: A heurística `sugerirProtecaoCircuito` continua funcionando como fallback (`origem_in: "SUGESTAO"`) quando o motor completo não conseguir resolver (ex.: IB fora da faixa suportada).

**Integration Verification**
IV1: Testes existentes de `motor-sobrecarga.test.ts` e `motor-protecao.ts` (se houver) continuam passando sem alteração.
IV2: Nenhuma mudança de assinatura pública em `motor-protecao.ts` — o novo motor vive em módulo próprio (`dimensionamento-disjuntores`).
IV3: Suíte completa (`npx vitest run`) sem regressões fora do escopo desta story.

### Story 1.2 Overrides por Circuito e Persistência

As a engenheiro eletricista,
I want customizar os parâmetros de proteção (In, curva, Icc) por circuito individualmente, com justificativa obrigatória e trilha auditável,
so that eu possa tratar exceções normativas sem perder rastreabilidade, do mesmo jeito que já faço no MOD-DC.

**Acceptance Criteria**
1: Override por circuito segue o padrão `useGlobal` / `customParams` / `justificativa obrigatória`, análogo a `CircuitoOverride` do MOD-DC-HYBRID.
2: Override sem justificativa é rejeitado com erro explícito (mesmo padrão de `OverrideCircuitoInvalido`).
3: Resultado por circuito registra `baseadoEm: "GLOBAL" | "CUSTOMIZADO"` e `parametrosUsados`.
4: Overrides são persistidos em tabela Supabase própria, com política RLS `anon_all_<tabela>` para o modo SPA.
5: Migration própria criada em `supabase/migrations/`, seguindo o padrão de `20260730_001_create_queda_tensao_config.sql`.

**Integration Verification**
IV1: Nenhuma tabela existente (`dependencia_*`, `parametros_edp_overrides`, `queda_tensao_config`) tem schema alterado.
IV2: Repositório novo segue a interface `Repository<T>` já usada nos demais módulos (compatível com `InMemoryRepository` para testes).
IV3: Teste de integração cobre GLOBAL, CUSTOMIZADO válido e CUSTOMIZADO inválido (sem justificativa/sem customParams).

### Story 1.3 Integração com MOD-DC e MOD-SEC

As a engenheiro eletricista,
I want que o resultado do MOD-PROT alimente automaticamente o critério C2 do MOD-DC e o `tempo_atuacao_s` do MOD-SEC,
so that eu não precise fornecer manualmente valores que o próprio sistema já calculou.

**Acceptance Criteria**
1: `aplicarSugestaoProtecaoSeAusente` (`overrides.ts`) passa a consultar o motor MOD-PROT (global ou override do circuito) em vez de chamar `sugerirProtecaoCircuito` diretamente; a heurística permanece como fallback interno do motor (Story 1.1, AC5).
2: A assinatura de retorno consumida pelo MOD-DC (`in_a`, `origem_in`, `i2_a`, `fonte_i2`) não muda.
3: `tempo_atuacao_s` calculado pelo MOD-PROT (a partir da curva selecionada) é aceito como input válido pelo endpoint `POST /api/v1/modulos/mod-sec/validar`, sem alteração no contrato desse endpoint.
4: Critérios C2 (`motor-sobrecarga.ts`) e C4 (MOD-SEC) continuam sendo avaliados corretamente com os valores agora vindos do MOD-PROT.

**Integration Verification**
IV1: Suíte de testes do MOD-DC (`dimensionamento-condutores-flow.test.ts`, `aplicar-secoes-otimizadas.test.ts`) passa sem alteração de expectativas fora do escopo desta story.
IV2: Suíte de testes do MOD-SEC continua passando com `tempo_atuacao_s` vindo do MOD-PROT.
IV3: Teste de regressão cobrindo o caso em que MOD-PROT não consegue resolver (IB fora de faixa) e o sistema cai para a heurística de fallback, preservando o comportamento anterior.
IV4: Teste de regressão cobrindo `auto-otimizacao-retencao.ts` (épico AUTO-OTI) — consumidor de `resolverParametrosCircuito` não documentado na primeira versão deste PRD, identificado via `*analyze-impact`.

### Story 1.4 Rota, API e UI da Seção

As a engenheiro eletricista,
I want acessar uma seção dedicada de "Dimensionamento de Disjuntores" no projeto, com os mesmos padrões visuais das demais seções,
so that eu possa revisar e ajustar a seleção de proteção por circuito de forma consistente com o resto do sistema.

**Acceptance Criteria**
1: Nova rota `projetos/$projetoId_/dimensionamento-disjuntores` lista os circuitos do projeto com In/curva/Icu/Ics sugeridos e permite override por circuito.
2: Nova(s) rota(s) de API server-side (`src/routes/api/v1/modulos/mod-prot.*.ts`) expõem cálculo e persistência, com validação Zod de entrada/saída.
3: Novo item de navegação no `SieShell` aponta para a nova rota.
4: `src/routeTree.spa.ts` é atualizado manualmente para incluir a nova rota (build SPA).

**Integration Verification**
IV1: `tests/ui/projeto-detalhe-nav-links.test.ts` atualizado e passando com o novo link.
IV2: `npx vite build --config vite.spa.config.ts` conclui com sucesso e a nova rota está acessível no bundle SPA.
IV3: Nenhuma regressão visual nas demais rotas (checar snapshots VRT existentes, ex.: `queda-tensao.vrt.test.tsx.snap`).

### Story 1.5 Tutorial, Rastreabilidade e Auditoria

As a engenheiro eletricista,
I want um tutorial didático da nova seção e rastreabilidade completa das decisões automáticas e manuais,
so that eu confie na origem de cada valor de proteção usado no projeto e consiga explicar a escolha em um laudo técnico.

**Acceptance Criteria**
1: Par `docs/TUTORIAL-DIMENSIONAMENTO-DISJUNTORES.md` + `.html` criado, seguindo a estrutura visual dos tutoriais existentes.
2: Nova unidade registrada no manifesto de tutoriais (`scripts/tutorial-*-manifest.mjs`), listando todos os arquivos-fonte reais (domínio, componentes, schemas) que o tutorial documenta.
3: `npm run docs:tutorial:check` passa sem drift após `npm run docs:tutorial:update`.
4: `resultado.rastreio` da seção registra `norma_dispositivo`, `capacidade_interrupcao`, In/I2/Icc usados (Icc lido de `retorno_cc.icc_presumida_a`) e, quando aplicável, justificativa do override — mesmo padrão do critério C4 do MOD-SEC.
5: Overrides manuais geram evento em `eventos_auditoria`.

**Integration Verification**
IV1: Pre-commit hook (`docs:tutorial:check`) bloqueia commit se o tutorial ficar desatualizado.
IV2: CI (`docs-tutorial-check.yml`) valida a mesma checagem em push/PR.
IV3: Nenhum evento de auditoria de outros módulos é alterado em formato ou volume inesperado.

---

## 7. Fora de Escopo (explícito)

- Cálculo automático de corrente de curto-circuito presumida (Icc) — permanece input manual do projetista (decisão #3), lido via o canal já existente `retorno_cc.icc_presumida_a` (critério C3/MOD-CC, ver Seção 0.1); MOD-PROT não implementa nem chama a lógica de cálculo de curto-circuito, apenas consome o retorno já persistido. Atenção à colisão de nomenclatura `MOD-CC` já registrada na Seção 1.1 caso um módulo de cálculo automático de curto-circuito seja especificado no futuro.
- Escolha definitiva de catálogo de fabricante (WEG/Siemens/ABB/Schneider) — apenas a tabela normativa genérica é obrigatória neste epic; fabricantes ficam como fast-follow (FR2).
- Estudo completo de seletividade/discriminação entre múltiplos níveis hierárquicos de disjuntores — apenas verificação básica de poder de interrupção (FR4) está no escopo.
- Geração de laudo/relatório técnico final em PDF incluindo esta seção — assunto de outro PRD, se necessário.

---

## Handoff

- **Status do impacto:** `@architect *analyze-impact` executado em 2026-08-04; achados incorporados a este PRD (Seção 0.1). Risco revisado: **HIGH** (upgrade de "Significant") até que o ADR dedicado de MOD-PROT (próximo passo) formalize o contrato de rota/persistência.
- **next_agent:** `@architect` (ADR dedicado de MOD-PROT, mesmo formato de `docs/architecture/mod-dc-rotas-retorno-downstream.md`, conforme essa própria ADR já recomendava em sua Seção 6)
- **next_command:** após o ADR, `@sm *draft` para quebrar o Epic 1 em stories formais, seguido de `@po *validate-story-draft`
- **alternative:** pular o ADR e ir direto para `@sm *draft` é possível, mas aceita o risco de as stories serem escritas sobre um contrato de campos/rota ainda não fixado formalmente
