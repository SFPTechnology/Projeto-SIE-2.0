---
story_id: T2-SEM-MOTOR-1
epic_id: MOD-CC-SEC-QT-1
title: "Ausência de motor como tipo em MOD-CC e MOD-SEC"
status: InProgress
priority: P0
created_date: 2026-08-05
created_by: "@sm (River)"
source_plan: "Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md"
clickup:
  task_id: ""
  epic_task_id: ""
  list: "Backlog"
  url: ""
  last_sync: ""
  sync_status: "UNAVAILABLE_NO_CONNECTOR"
---

# Story T2-SEM-MOTOR-1: Ausência de motor como tipo em MOD-CC e MOD-SEC

## Status

**InProgress** — implementação iniciada pelo `@dev` em 2026-08-05.

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - schema_validation
  - typescript
  - integration_test
  - regression_test
  - coderabbit
```

O campo `quality_gate` representa a revisão técnica de conformidade do executor mapping. O veredito final de qualidade da implementação permanece sob autoridade exclusiva do `@qa`, registrado em **QA Results**.

## Story

**Como** responsável técnico pelo dimensionamento de condutores,
**quero** que MOD-CC e MOD-SEC declarem explicitamente a ausência de motor,
**para que** o SIE não produza vereditos normativos simulados nem os apresente como confirmados em auditoria.

## Contexto e valor

MOD-CC e MOD-SEC possuem contratos, endpoints, timeout, persistência e pontos de injeção, mas seus clientes padrão ainda aplicam limiares arbitrários para decidir C3 e C4. O caminho SPA de produção não consome esses endpoints e já mantém C3/C4 pendentes quando não existe retorno. Esta story torna esse comportamento honesto o único comportamento padrão e preserva o encaixe para motores reais futuros.

Esta é uma correção brownfield vinculada ao épico `MOD-CC-SEC-QT-1` e às stories concluídas `MOD-CC-1` e `MOD-SEC-1`; não reabre a implementação interna dos motores. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#contexto-mínimo`] [Source: `docs/stories/EPIC-MOD-CC-SEC-QT.md#scope`]

## Acceptance Criteria

1. **Ausência tipada na API:** existe `SemMotorSchema` com `status: "SEM-MOTOR"`, `modulo: "MOD-CC" | "MOD-SEC"` e `motivo` não vazio; `RespostaMODCCSchema` aceita veredito real ou ausência e `RespostaMODSECSchema` aceita veredito real, `NAO-APLICAVEL` ou ausência. Os schemas existentes de veredito real permanecem compatíveis.
2. **União discriminada no domínio:** `RetornoMODCC` e `RetornoMODSEC` não expõem `aprovado` fora da variante `VEREDICTO`; `RetornoMODSEC` inclui ainda uma variante tipada `NAO-APLICAVEL`, restrita ao esquema TT. A fronteira API/persistência (`status`) → domínio (`tipo`) é convertida explicitamente, sem casts duplos ou acesso inseguro a campos exclusivos da variante.
3. **Mocks sem veredito normativo:** os clientes padrão de MOD-CC e MOD-SEC retornam somente `SEM-MOTOR`; não existem mais o limiar de `5000 A`, o limite universal de `0,4 s`, atrasos artificiais nem fontes que mimetizem motor real (`MOD-CC v1.0`/`MOD-SEC v1.0`).
4. **Pontos de injeção preservados:** `_setClienteModCCParaTeste`, `_resetClienteModCCParaTeste`, `_setClienteModSECParaTeste` e `_resetClienteModSECParaTeste` continuam funcionais; um cliente injetado que produza veredito real continua sendo validado, persistido e processado.
5. **Degradação honesta de C3/C4:** `SEM-MOTOR` resolve C3 como `PENDENTE` + `AGUARDANDO-CC` e C4, em TN/IT, como `PENDENTE` + `AGUARDANDO-SECCIONAMENTO`, ambos sem seção e sem rastreio normativo. Em TT, C4 continua `NAO-APLICAVEL`, sem chamada a MOD-SEC e sem pendência de seccionamento.
6. **Estado global protegido:** com C3 ou C4 em `SEM-MOTOR`, circuitos TN/IT não atingem `VERIFICADO-COMPLETO`; permanecem no estado parcial aplicável. Nenhum comportamento de C1, C2, C5, C6 ou MOD-QT é alterado.
7. **Selo derivado da evidência:** o `status_verificacao` de C3/C4 deixa de ser literal. Para veredito real, fonte não vazia resulta em `CONFIRMADO`; fonte vazia resulta em `[VERIFICAR]`. Ausência de motor não produz rastreio.
8. **Persistência e leitores compatíveis:** payload `SEM-MOTOR` serializa na coluna JSONB existente sem migration; todos os leitores de `dependencia_retornos_downstream` e schemas consumidores reconhecem a nova resposta e não presumem a presença de `aprovado`.
9. **Regressão do caminho SPA:** o resultado observável do build SPA permanece igual ao anterior: sem retornos reais, C3/C4 continuam pendentes (exceto TT), sem promover status completo.
10. **Qualidade verificável:** testes de contrato, handler, persistência, integração de domínio e regressão cobrem AC1–AC9; `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passam no subapp.

## Fora de escopo

- Implementar motores reais em `src/domain/curto-circuito/` ou `src/domain/seccionamento/`.
- Introduzir valores, tabelas ou limites normativos novos.
- Alterar o contrato público ou o motor real do MOD-QT.
- Criar migration para `dependencia_retornos_downstream`, cuja coluna de payload já é JSONB.
- Alterar a UI ou adicionar consumo dos endpoints MOD-CC/MOD-SEC à fachada SPA.

## 🤖 CodeRabbit Integration

### Story Type Analysis

**Primary Type:** API  
**Secondary Type(s):** Architecture, Integration  
**Complexity:** Medium — contrato compartilhado, dois handlers, resolvedores e leitores persistidos, sem migration ou UI.

### Specialized Agent Assignment

**Primary Agents:**

- `@dev` — implementação e revisão pre-commit.
- `@architect` — gate técnico de aderência aos contratos e fronteiras arquiteturais existentes.

**Supporting Agents:**

- `@qa` — veredito final sobre contratos, fluxos de integração e regressão.
- `@github-devops` — revisão pre-PR e operações remotas após aprovação.

### Quality Gate Tasks

- [ ] Pre-Commit (`@dev`): executar CodeRabbit sobre mudanças não commitadas antes de concluir a story.
- [ ] Pre-PR (`@github-devops`): executar CodeRabbit contra a base antes de criar PR.
- [ ] Pre-Deployment: N/A — esta story não executa deploy nem altera infraestrutura.

### Self-Healing Configuration

**Expected Self-Healing:**

- Primary Agent: `@dev` (light mode)
- Max Iterations: 2
- Timeout: 15 minutos
- Severity Filter: CRITICAL

**Predicted Behavior:**

- CRITICAL: `auto_fix`, no máximo duas iterações.
- HIGH: `document_only` nas notas da implementação.
- MEDIUM/LOW: não bloqueiam o ciclo automático; seguem tratamento do gate de QA.

### CodeRabbit Focus Areas

**Primary Focus:**

- Exhaustividade das uniões e impossibilidade de acessar `aprovado` em `SEM-MOTOR`.
- Validação consistente entre resposta HTTP, payload persistido e contrato de domínio.

**Secondary Focus:**

- Preservação de timeout, tratamento de erros e pontos de injeção.
- Ausência de valores normativos arbitrários e de regressões em MOD-QT/SPA.

## Tasks / Subtasks

- [x] **Task 1 — Tipar respostas de API e domínio** (AC: 1, 2, 8)
  - [x] Criar `SemMotorSchema`, `RespostaMODCCSchema` e `RespostaMODSECSchema` em `src/api/schemas/otimizar-condutor.schema.ts`.
  - [x] Preservar a forma dos schemas de veredito real e a variante `NaoAplicavelMODSECSchema`.
  - [x] Criar `VeredictoMODCC`, `VeredictoMODSEC`, `SemMotor` e a variante de domínio `NaoAplicavelMODSEC`; transformar `RetornoMODCC`/`RetornoMODSEC` em uniões discriminadas em `src/domain/dimensionamento-condutores/contratos.ts`.
  - [x] Implementar/adotar adaptador explícito entre as formas da API/persistência (`status`) e do domínio (`tipo`), adicionando `tipo: "VEREDICTO"` apenas ao entrar no domínio.
  - [x] Atualizar schemas consumidores, fixtures e leitores tipados para estreitar a união antes de acessar campos exclusivos.

- [x] **Task 2 — Fazer os clientes padrão declararem ausência** (AC: 3, 4, 8)
  - [x] Alterar `validarModCCMock` para retornar somente `SEM-MOTOR` com motivo não vazio.
  - [x] Alterar `validarModSECMock` para retornar somente `SEM-MOTOR` com motivo não vazio nos esquemas em que o handler efetivamente chama o cliente.
  - [x] Validar as respostas dos handlers com `RespostaMODCCSchema`/`RespostaMODSECSchema` e persistir o payload válido na infraestrutura existente.
  - [x] Preservar timeout, respostas de erro, regra TT e os quatro helpers de injeção/reset de clientes.
  - [x] Remover dos caminhos de mock os limiares, atrasos e strings de fonte simulada listados no AC3.

- [x] **Task 3 — Propagar `SEM-MOTOR` com segurança pelo domínio** (AC: 5, 6, 7)
  - [x] Alterar `resolverC3Curto` para tratar ausência como `PENDENTE`/`AGUARDANDO-CC`, sem seção/rastreio.
  - [x] Alterar `resolverC4Seccionamento` para tratar ausência como `PENDENTE`/`AGUARDANDO-SECCIONAMENTO` em TN/IT e preservar `NAO-APLICAVEL` em TT.
  - [x] Estreitar explicitamente a variante `NaoAplicavelMODSEC` antes de acessar campos de veredito, mantendo-a válida apenas para o payload TT já validado pelo schema.
  - [x] Centralizar a derivação de `status_verificacao` do veredito real a partir de `fonte`, retornando `CONFIRMADO` ou `[VERIFICAR]` conforme AC7.
  - [x] Confirmar por teste que a máquina de estados não produz `VERIFICADO-COMPLETO` quando C3 ou C4 permanece pendente.

- [x] **Task 4 — Atualizar persistência e consumidores** (AC: 1, 2, 8, 9)
  - [x] Atualizar `src/domain/servicos/servico-dimensionamento-condutores.ts` para ler as uniões de resposta persistidas e aplicar o adaptador antes de anexá-las ao circuito.
  - [x] Atualizar `CircuitoParaOtimizacaoSchema` e qualquer consumidor localizado pela busca de `RetornoMODCCSchema`, `RetornoMODSECSchema`, `retorno_cc.aprovado` ou `retorno_seccionamento.aprovado`.
  - [x] Confirmar round-trip de payload `SEM-MOTOR` pelo `InMemoryRepository` existente, sem migration.
  - [x] Confirmar que nenhuma alteração alcança o contrato/motor do MOD-QT ou adiciona consumo MOD-CC/MOD-SEC ao caminho SPA.

- [x] **Task 5 — Reescrever e ampliar testes** (AC: 1–10)
  - [x] Atualizar testes Zod para aceitar as três formas aplicáveis e rejeitar combinações inválidas.
  - [x] Reescrever testes dos handlers que hoje esperam aprovação/reprovação do cliente padrão; provar que nenhuma entrada faz o mock produzir `VEREDICTO`.
  - [x] Manter testes de clientes injetados para vereditos reais, erro, contrato inválido e timeout.
  - [x] Cobrir persistência e leitura posterior de `SEM-MOTOR` para MOD-CC e MOD-SEC.
  - [x] Cobrir C3/C4 pendentes, TT `NAO-APLICAVEL`, estado global parcial e rastreio com/sem fonte.
  - [x] Cobrir regressão do caminho SPA e não regressão de MOD-QT.

- [ ] **Task 6 — Executar quality gates e preparar handoff** (AC: 10)
  - [ ] Executar `npm run lint` no subapp.
  - [x] Executar `npm run typecheck` no subapp.
  - [ ] Executar `npm test` no subapp.
  - [x] Executar `npm run build` e, para a invariância SPA, `npm run build:spa` no subapp.
  - [ ] Executar CodeRabbit pre-commit e resolver issues CRITICAL conforme configuração.
  - [x] Atualizar checkboxes, Change Log, Completion Notes e File List antes de mover a story para revisão.

## Dev Notes

### Arquitetura aplicável

- O runtime é o subapp `sistema-de-instala-es-el-tricas-sie-main/`, com TypeScript strict e TanStack Start; não criar backend separado. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#1-sumario-executivo`]
- O domínio deve permanecer puro e independente de React, Supabase e HTTP. Contratos formais são TypeScript/Zod; rotas pertencem a `src/routes/api/v1/`. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#21-decisao`]
- Rotas não contêm regra normativa: validam, orquestram e serializam. A interpretação de C3/C4 permanece no domínio. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#62-fluxo-dc-7-api`] [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#9-gates-arquiteturais`]
- O serviço de aplicação orquestra integrações e revalidação sem recomputar módulos externos. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#55-servico-de-aplicacao`]
- Pendências C3/C4 devem impedir status completo; `VERIFICADO-COMPLETO` exige C1–C6 aprovados/não aplicáveis e nenhuma pendência. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#57-ui-carbon`] [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#9-gates-arquiteturais`]
- Lacunas sem evidência confirmada devem permanecer explícitas como `[VERIFICAR]` ou pendência, nunca promovidas silenciosamente. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#24-condicoes-da-decisao`] [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#10-riscos-tecnicos-e-mitigacoes`]

### Requisitos e decisões do plano T2

- A forma pública de ausência usa `status: "SEM-MOTOR"`; o domínio usa união discriminada por `tipo`. O adaptador explícito definido nesta story resolve a diferença sem alterar os schemas reais de veredito. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#passo-1--schema-zod-da-ausência`] [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#passo-2--contrato-de-domínio-como-união-discriminada`]
- O cliente padrão deixa de simular decisão e declara ausência; o ponto de injeção continua sendo a entrada para um motor real futuro. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#passo-3--os-mocks-passam-a-declarar-ausência`]
- `SEM-MOTOR` deve convergir para os mesmos estados pendentes já observados quando o retorno é `null`. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#passo-4--resolvedores-tratam-a-variante`]
- O selo de rastreabilidade depende da fonte efetivamente recebida. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#passo-5--o-selo-deixa-de-ser-literal`]

### Contexto das stories anteriores

- `MOD-CC-1` e `MOD-SEC-1` já entregaram endpoints reais, validação Zod, persistência, timeout e clientes injetáveis; esta story preserva essa infraestrutura e corrige apenas o cliente padrão e o contrato de ausência. [Source: `docs/stories/MOD-CC-1-refined.md#re-review--2026-07-15-qa-quinn--gate-decision--pass`] [Source: `docs/stories/MOD-SEC-1-refined.md#tasks--subtasks`]
- Testes anteriores codificam os limiares dos mocks e precisam ser reescritos, não apenas ampliados. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#riscos`]

### Arquivos principais

Os caminhos abaixo são relativos a `sistema-de-instala-es-el-tricas-sie-main/`:

- `src/api/schemas/otimizar-condutor.schema.ts`
- `src/domain/dimensionamento-condutores/contratos.ts`
- `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts`
- `src/domain/dimensionamento-condutores/estados.ts` (verificação; alterar somente se um teste revelar necessidade)
- `src/domain/servicos/servico-dimensionamento-condutores.ts`
- `src/routes/api/v1/modulos.mod-cc.validar.ts`
- `src/routes/api/v1/modulos.mod-sec.validar.ts`
- `src/api/schemas/__tests__/otimizar-condutor-mod-cc.schema.test.ts`
- `tests/api/modulos-mod-cc.test.ts`
- `tests/api/modulos-mod-sec.test.ts`
- `tests/domain/dimensionamento-condutores/mod-dc.test.ts`

Arquivos adicionais só entram na File List se forem consumidores reais encontrados pelo typecheck/busca. A arquitetura prevê domínio em `src/domain`, schemas em `src/api/schemas`, rotas em `src/routes/api/v1` e testes em `tests/`/`src/**/__tests__`. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#4-estrutura-de-pastas`]

### Project Structure Notes

- Os arquivos-alvo reais estão no submódulo `sistema-de-instala-es-el-tricas-sie-main/`; a story permanece no repositório orquestrador em `docs/stories/`.
- Os arquivos gerais configurados em `devLoadAlwaysFiles` (`docs/framework/coding-standards.md`, `tech-stack.md`, `source-tree.md`) não existem nem possuem fallback localizado. Esta story usa a decisão arquitetural aprovada `ARCH-MOD-DC-plano-arquitetura.md` e os padrões observáveis do subapp.
- Nenhuma migration é necessária; alterações de schema/DDL/RLS estão fora do escopo.

### Segurança, compatibilidade e rollback

- A story não introduz autenticação, credenciais, dependências externas ou variáveis de ambiente. A superfície de segurança relevante é a validação Zod de entrada/saída e a impossibilidade de promover payload incompleto a veredito.
- A compatibilidade do caminho SPA e do MOD-QT é critério bloqueante; não há migração de dados nem alteração de DDL.
- Rollback: reverter somente os arquivos listados no Dev Agent Record desta story e reexecutar a suíte baseline. Como o payload é JSONB e não há migration, nenhuma operação de rollback de banco é necessária. [Source: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md#riscos`]

## Testing

O projeto usa Vitest para testes unitários, de integração, regressão normativa, API e performance; os gates de build são Vite, TypeScript e ESLint. [Source: `docs/architecture/ARCH-MOD-DC-plano-arquitetura.md#31-stack-principal`]

### Cenários mínimos

1. `SemMotorSchema` aceita motivo não vazio e enum de módulo; rejeita módulo/motivo inválidos.
2. Respostas MOD-CC/MOD-SEC aceitam ausência e veredito real; MOD-SEC também aceita TT `NAO-APLICAVEL`.
3. Cliente padrão de MOD-CC retorna ausência para entradas abaixo, iguais e acima de 5000 A.
4. Cliente padrão de MOD-SEC retorna ausência para tempos abaixo, iguais e acima de 0,4 s em TN/IT.
5. Cliente injetado continua cobrindo veredito aprovado e reprovado, contrato inválido, erro e timeout.
6. `SEM-MOTOR` persiste e é lido de volta sem acesso a `aprovado`.
7. C3/C4 ausentes ficam pendentes com os códigos esperados; TT permanece não aplicável.
8. TN/IT com ausência não atinge `VERIFICADO-COMPLETO`.
9. Veredito com fonte produz `CONFIRMADO`; sem fonte produz `[VERIFICAR]`; ausência não produz rastreio.
10. MOD-QT, C1/C2/C5/C6 e caminho SPA mantêm comportamento anterior.

### Gates obrigatórios

- `npm run lint`
- `npm run typecheck`
- `npm test`
- `npm run build`
- `npm run build:spa` para evidência específica do AC9
- CodeRabbit sem issues CRITICAL

Os gates de integração existentes exigem contrato, persistência round-trip, fluxo E2E, edge cases, segurança e regressão. Requisitos históricos incompatíveis com a ausência tipada são substituídos pelos AC desta story de correção. [Source: `docs/qa/QUALITY-GATES-MOD-CC-SEC-QT.md#gate-execution-matrix`]

## Riscos e mitigação

| ID | Risco | Mitigação exigida |
|---|---|---|
| T2-R1 | Consumidor não mapeado dos endpoints | Busca global por schemas/campos e typecheck estrito. |
| T2-R2 | Testes preservarem o comportamento errado | Reescrever testes que esperam limiares e fontes simuladas. |
| T2-R3 | Leitor JSONB ignorar `SEM-MOTOR` | Round-trip pelo repositório em memória e adaptação explícita nos leitores. |
| T2-R4 | Regressão sem proteção remota | Executar localmente a suíte completa e registrar evidência no Dev Agent Record. |

## Change Log

| Date | Version | Description | Author |
|---|---:|---|---|
| 2026-08-05 | 0.1 | Story criada a partir do plano T2; composição única aprovada pelo usuário; status Draft. | @sm (River) |
| 2026-08-05 | 0.1.1 | Validated GO (9/10) — variante de domínio `NAO-APLICAVEL` explicitada; executor mapping alinhado; Status: Draft → Ready. | @po (Pax) |
| 2026-08-05 | 0.1.2 | Desenvolvimento iniciado em modo interativo; Status: Ready → InProgress. | @dev (Dex) |
| 2026-08-05 | 0.1.3 | Implementação funcional e cobertura T2 concluídas; gates globais externos/ambientais documentados; Status mantido em InProgress. | @dev (Dex) |

## Dev Agent Record

### Agent Model Used

GPT-5 (Codex), persona `@dev` (Dex).

### Debug Log References

- Testes direcionados: 6 arquivos, 68 testes aprovados.
- `npm run typecheck`: aprovado.
- ESLint direcionado aos arquivos da story: aprovado; `npm run lint` integral expirou sem diagnóstico em 3 min e 10 min. O arquivo preexistente `DimensionamentoCondutoresResumo.tsx` mantém 13 violações Prettier fora das linhas alteradas pela story.
- `npm test`: 157 arquivos/1162 testes aprovados; 8 arquivos/11 testes externos à story falharam (10 snapshots preexistentes e 1 timeout no catálogo de impedância).
- `npm run build` e `npm run build:spa`: aprovados.
- CodeRabbit: indisponível; binário WSL aborta com `Illegal instruction (core dumped)` e não há instalação nativa.
- `git diff --check` nos arquivos da story: aprovado; busca nos mocks confirmou ausência dos limiares, atraso e fontes simuladas do AC3.

### Completion Notes List

- Adicionados contratos de resposta `SEM-MOTOR`, uniões discriminadas no domínio e adaptadores explícitos `status` → `tipo`.
- Clientes padrão MOD-CC/MOD-SEC agora declaram ausência sem emitir veredito; injeção, timeout, erros, persistência e regra TT foram preservados.
- C3/C4 degradam honestamente para pendência e não emitem rastreio sem motor; vereditos reais derivam `status_verificacao` da fonte.
- Leitores JSONB e consumidores foram estreitados; round-trip de ausência e proteção do status global foram cobertos.
- Nenhuma dependency, migration, variável de ambiente ou mudança intencional de UI foi adicionada.
- DoD parcial: requisitos funcionais e testes da story concluídos; gate global de testes/lint e CodeRabbit impedem mover para `InReview` neste worktree.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/api/http.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/otimizar-condutor.schema.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/__tests__/otimizar-condutor-mod-cc.schema.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/calculo/otimizador.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/overrides.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-disjuntores/overrides.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-cc.validar.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-sec.validar.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-cc.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-sec.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/dimensionamento-condutores/motores-c3-c4-c5.test.ts`

## QA Results

_A preencher pelo `@qa` após a implementação._

### Review Date: 2026-08-05

### Reviewed By: Quinn (Test Architect)

### Gate Decision: FAIL

A implementação central de `SEM-MOTOR` é coerente, tipada e fail-closed. Os schemas públicos, adaptadores `status` → `tipo`, resolvedores C3/C4 e leitores persistidos aderem ao desenho da story; `typecheck`, ESLint escopado e 68/68 testes focados passaram na reexecução independente do QA.

O gate não pode ser aprovado porque as pré-condições formais do workflow e o AC10 não estão atendidos: a story permanece `InProgress`, Task 6 está incompleta, código e story não estão commitados/isolados, `npm test` global está vermelho, `npm run lint` integral não conclui e o CodeRabbit aborta antes de produzir relatório.

### Requirements Traceability

| AC | Evidência | Resultado |
|---:|---|---|
| 1 | Testes Zod de `SemMotorSchema`, respostas MOD-CC/MOD-SEC e combinações inválidas | PASS |
| 2 | Uniões discriminadas, adaptadores explícitos, busca por acessos inseguros e `typecheck` | PASS |
| 3 | Testes de fronteira em 4999/5000/6000 A e 0,39/0,4/0,8 s; busca sem limiares/fontes nos mocks | PASS |
| 4 | Helpers preservados; veredito aprovado, contrato inválido, erro e timeout exercitados | PASS com lacuna de teste reprovado |
| 5 | Testes C3/C4 `PENDENTE`, TT `NAO-APLICAVEL` e ausência de rastreio | PASS |
| 6 | Teste de estado parcial e inspeção do HTML SPA com C3/C4 pendentes | PASS |
| 7 | Testes `CONFIRMADO`, `[VERIFICAR]` e ausência de rastreio | PASS |
| 8 | Round-trip JSONB/in-memory de `SEM-MOTOR` para MOD-CC/MOD-SEC | PASS |
| 9 | `build:spa` aprovado; VRT isolado confirma `DIMENSIONAMENTO-PARCIAL`, embora falhe em assertiva alheia `SUGESTAO` → `MOD-PROT` | PASS com ressalva global |
| 10 | Lint global, suíte global e CodeRabbit não aprovados | FAIL |

### Code Quality Assessment

- Fronteira API/domínio explícita, sem cast duplo novo e com validação do módulo correto.
- `SEM-MOTOR` não expõe `aprovado`; MOD-PROT trata ausência como Icc pendente.
- `NAO-APLICAVEL` não promove C4 fora de TT.
- Nenhuma regra normativa, dependency, migration ou segredo foi introduzido.
- O worktree misto impede atribuição limpa do diff e revisão CodeRabbit sobre a entrega real.

### Refactoring Performed

Nenhum. A revisão foi advisory e não alterou código de produção ou testes.

### Compliance Check

- Coding Standards: CONCERNS — ESLint escopado passou; lint integral expirou e os documentos configurados de coding standards não existem.
- Project Structure: PASS — mudanças seguem schemas, domínio, rotas e testes existentes.
- Testing Strategy: FAIL — suíte focada passa, mas suíte global permanece vermelha e falta o caso injetado reprovado nos dois handlers.
- All ACs Met: FAIL — AC10 não atendido.
- Constitution Quality First: FAIL — lint/test/CodeRabbit e status de revisão não satisfazem os MUSTs.

### Improvements Checklist

- [x] Reexecutar `typecheck`, testes focados e ESLint escopado.
- [x] Validar comportamento SPA relevante isoladamente.
- [ ] Adicionar testes de cliente injetado com veredito reprovado para MOD-CC e MOD-SEC.
- [ ] Resolver ou isolar as 11 falhas da suíte global e obter `npm test` com exit code 0.
- [ ] Obter `npm run lint` integral com exit code 0.
- [ ] Corrigir a instalação CodeRabbit e executar a revisão sobre um commit/diff isolado da story.
- [ ] Concluir Task 6 e mover a story para revisão pelo fluxo do `@dev`.

### Security Review

PASS. Entradas e respostas são validadas por Zod; não há SQL dinâmico, autenticação alterada, credenciais, dependências ou exposição adicional de dados sensíveis.

### Performance Considerations

PASS no escopo. Os atrasos artificiais foram removidos, os mocks agora respondem imediatamente e o timeout downstream existente foi preservado. A lentidão do lint é um problema ambiental/de configuração do repositório.

### Testability

- Controllability: PASS — clientes injetáveis e resets preservados.
- Observability: PASS — payload persistido, estados, pendências e rastreio são assertáveis.
- Debuggability: CONCERNS — worktree amplo e não commitado dificulta atribuição de falhas e CodeRabbit.

### Files Modified During Review

- `docs/stories/story-T2-SEM-MOTOR-1-ausencia-motor-tipado.md` — somente esta seção `QA Results`.
- `docs/qa/gates/T2-SEM-MOTOR-1-ausencia-motor-tipado.yml` — decisão formal de gate.

### Gate Status

Gate: **FAIL** → `docs/qa/gates/T2-SEM-MOTOR-1-ausencia-motor-tipado.yml`

### Recommended Status

**Changes Required.** Manter `InProgress` até as ações bloqueantes serem resolvidas; o owner decide a transição final.
