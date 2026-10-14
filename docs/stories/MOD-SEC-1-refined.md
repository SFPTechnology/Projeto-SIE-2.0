---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [api_contract_test, integration_test, e2e_test, performance_test, security_scan]
---

# Story MOD-SEC-1: Validação de Seccionamento Automático (C4)

## Status

**Done** (2026-07-15 — @qa gate PASS 8/8, suíte 688/688; ciclo `Draft → Ready → InProgress → InReview → Done` no mesmo dia. Correções @po: enum de aterramento real do domínio é `"TT" | "TN-S" | "TN-C" | "TN-C-S" | "IT"` (story omitia TN-C); MOD-SEC-1.4 já implementado no domínio desde v3.0 — task virou verificação)

## Story

**As a** engenheiro eletricista,  
**I want** que MOD-DC integre com MOD-SEC para validação de seccionamento automático (C4),  
**so that** a conformidade NBR5410 5.1.2.2.4 seja garantida

## Acceptance Criteria (Detalhados)

### AC1: API Contract for MOD-SEC
```gherkin
When POST /api/v1/modulos/mod-sec/validar é chamado
Then request contém:
  - esquema_aterramento: "TN-S" | "TN-C-S" | "TT" | "IT"
  - tempo_atuacao_s: number
And response retorna:
  - aprovado: boolean
  - tempo_seccionamento_s: number
  - fonte: string
```

### AC2: TT Regra Especial
```gherkin
Given esquema_aterramento === "TT"
When MOD-DC processa circuito
Then MOD-SEC NÃO é chamado (skip call)
And C4 é marcado como NAO-APLICAVEL
And dependencias NÃO inclui 'AGUARDANDO-SECCIONAMENTO'
```

### AC3: Integration with MOD-DC
```gherkin
Given retorno_seccionamento de MOD-SEC
When dimensionarCircuito() processa
Then C4 é marcado como APROVADO se retorno.aprovado === true
And C4 é marcado como NAO-APLICAVEL se esquema TT
And resultado.rastreio.c4_seccionamento registra tempo_seccionamento_s
And resultado.rastreio.c4_seccionamento registra fonte
```

### AC4: Test Coverage
```gherkin
Then testes cobrem:
  - TN-S com MOD-SEC (call + response handling)
  - TN-C-S com MOD-SEC (call + response handling)
  - TT sem MOD-SEC (skip logic)
  - IT com MOD-SEC (call + response handling)
  - Timeout handling
  - Invalid response handling
```

## Tasks / Subtasks

- [x] **MOD-SEC-1.1: API Contract**
  - [x] Define request schema — `ValidarMODSECSchema` (dependencia_id uuid, enum completo de aterramento incl. TN-C, tempo_atuacao_s, origem 1..200)
  - [x] Define response schema — `RetornoMODSECSchema` (já existia) + `NaoAplicavelMODSECSchema` (caso TT)
  - [x] Document endpoint — docblock em `modulos.mod-sec.validar.ts`
  
- [x] **MOD-SEC-1.2: Implement Endpoint**
  - [x] Create POST /api/v1/modulos/mod-sec/validar — `src/routes/api/v1/modulos.mod-sec.validar.ts`
  - [x] Add validation — `withZod` (entrada) + `RetornoMODSECSchema.safeParse` (saída, 422 se inválida)
  - [x] Add timeout handling (5s) — `Promise.race` com `aguardarAbort(signal)` (504/PENDENTE)
  
- [x] **MOD-SEC-1.3: TT Regra Logic**
  - [x] Check esquema_aterramento before calling MOD-SEC — guard antes do race
  - [x] Skip MOD-SEC if TT — teste prova 0 chamadas ao cliente
  - [x] Mark C4 as NAO-APLICAVEL — response `NAO-APLICAVEL`, sem persistência
  
- [x] **MOD-SEC-1.4: Integrate with MOD-DC** (verificação — já implementado no domínio desde v3.0)
  - [x] `retorno_seccionamento` em `CircuitoParaDimensionamento` — pré-existente
  - [x] `resolverC4Seccionamento` em `dimensionarCircuito()` — pré-existente
  - [x] Rastreio `c4_seccionamento` — verificado por teste E2E
  
- [x] **MOD-SEC-1.5: Database Persistence**
  - [x] Persist to dependencia_retornos_downstream — `retornosDownstream.registrar` (modulo MOD-SEC)
  - [x] Test round-trip — asserção via `porDependencia(UUID, "MOD-SEC")`
  
- [x] **MOD-SEC-1.6: Tests**
  - [x] Unit: Zod validation — request 400 (esquema inválido)
  - [x] Integration: API → DB — round-trip real via handler
  - [x] E2E: MOD-DC flow (TN-S aprova, TT NAO-APLICAVEL, TN-S sem retorno = AGUARDANDO-SECCIONAMENTO)
  - [x] Edge cases & performance — 422 contrato inválido, 500 erro, 504 timeout real (fake timers), TN-C-S/IT, reprovação

## Dev Notes

**Files Created/Modified (2026-07-15, @dev Dex — YOLO):**
- `src/api/schemas/otimizar-condutor.schema.ts` — `ValidarMODSECSchema` + `NaoAplicavelMODSECSchema`
- `src/routes/api/v1/modulos.mod-sec.validar.ts` (novo) — endpoint espelhando o padrão MOD-CC-1 pós-fix (persistência real, race de abort, cliente injetável para teste)
- `tests/api/modulos-mod-sec.test.ts` (novo, 12 testes) — handler real via `chamar()`, persistência, TT skip, timeout, E2E domínio
- `src/routeTree.gen.ts` — regenerado via `npx vite build`

**Evidência:** targeted 12/12 PASS; `tsc --noEmit` exit 0; eslint exit 0 (pós `--fix`); `vite build` exit 0; suíte completa em execução para o gate @qa.

## QA Results

**Reviewed by:** @qa (Quinn)
**Date:** 2026-07-15
**Gate Decision:** ✅ **PASS**

### Gate-by-Gate Assessment (per `docs/qa/QUALITY-GATES-MOD-CC-SEC-QT.md`)

| # | Gate | Result | Evidência |
|---|------|--------|-----------|
| 1 | API Contract Validation | ✅ PASS | `ValidarMODSECSchema` (enum completo incl. TN-C, `origem .max(200)`, `dependencia_id` uuid); saída validada com `RetornoMODSECSchema.safeParse` (422 se inválida) |
| 2 | Integration Testing | ✅ PASS | Persistência real via `retornosDownstream.registrar` (modulo MOD-SEC); round-trip assertado via `porDependencia()`; caso TT e falhas não persistem |
| 3 | End-to-End Flow | ✅ PASS | Handler real via `chamar()`; E2E alimenta `dimensionarCircuito()` → C4 APROVADO + `rastreio.c4_seccionamento`; TT → NAO-APLICAVEL sem pendência; TN-S sem retorno → AGUARDANDO-SECCIONAMENTO |
| 4 | Edge Case Handling | ✅ PASS | Timeout real 5s (fake timers) → 504/PENDENTE; erro downstream → 500/PENDENTE; contrato inválido → 422; request inválido → 400; TT prova 0 chamadas ao cliente (spy) |
| 5 | Performance Validation | ✅ PASS | Mock < 1s; sem benchmark real de MOD-SEC (módulo externo mockado — mesma ressalva do MOD-CC-1) |
| 6 | Security Scanning | ✅ PASS | `origem` limitado; sem secrets/SQLi; validação Zod em entrada e saída |
| 7 | Regression Testing | ✅ PASS | Suíte completa **688/688 (107 arquivos)**; `tsc --noEmit` exit 0; `vite build` exit 0; eslint exit 0 nos arquivos da story |
| 8 | Documentation & Compliance | ✅ PASS | Endpoint documentado com referência normativa (NBR 5410 5.1.2.2.4); story atualizada |

**Ressalva não-bloqueante:** CodeRabbit pre-commit delegado ao ciclo @devops (checkpoint). Status: `InReview → Done`.

## Effort

**Estimated:** 4 days (YOLO: mesmo dia)  
**Depends on:** Phase 1 & 2 complete — MOD-CC-1 Done forneceu a infra de persistência

## Change Log

- **2026-07-15 (@po Pax):** validate-story-draft GO 8/10. Status: `Draft → Ready`. Correções: enum real inclui TN-C; MOD-SEC-1.4 já implementado no domínio (vira verificação).
- **2026-07-15 (@dev Dex):** implementação completa reutilizando a infraestrutura de retornos downstream do MOD-CC-1 (repos + serviço + wiring já existentes). Status: `Ready → InProgress → InReview`.
- **2026-07-15 (@qa Quinn):** gate PASS 8/8 com evidência real (12/12 targeted, 688/688 suíte, tsc/eslint/build limpos). Status: `InReview → Done`. Ressalva: CodeRabbit pre-commit no checkpoint @devops.

---

**Story created by:** @sm (River)  
**Date:** 2026-07-15  
**Priority:** P0
