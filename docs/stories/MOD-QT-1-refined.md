---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [api_contract_test, integration_test, e2e_test, revalidation_test, performance_test, security_scan]
---

# Story MOD-QT-1: Validação de Queda de Tensão (C5)

## Status

**Done** (2026-07-15 — @qa gate PASS 8/8 incl. verificação E2E da revalidação AC2, suíte 688/688; ciclo `Draft → Ready → InProgress → InReview → Done` no mesmo dia. Observações @po: request AC1 ganha `dependencia_id` (FK migration 0009) e `origem` (auditoria), precedente MOD-CC-1; laço de revalidação AC2 já implementado no domínio desde v3.0 — MOD-QT-1.3/1.4 viraram verificação por E2E)

## Story

**As a** engenheiro eletricista,  
**I want** que MOD-DC integre com MOD-QT para validação de queda de tensão (C5),  
**so that** NBR5410 6.2.7 conformidade seja assegurada

## Acceptance Criteria (Detalhados)

### AC1: API Contract for MOD-QT
```gherkin
When POST /api/v1/modulos/mod-qt/validar é chamado
Then request contém:
  - corrente_a: number
  - comprimento_m: number
  - secao_mm2: number
  - limite_percentual: number
And response retorna:
  - atende: boolean
  - queda_percentual: number
  - limite_aplicado: number
  - secao_requerida_mm2?: number (opcional)
  - fonte: string
```

### AC2: Revalidation Loop
```gherkin
Given retorno_qt.secao_requerida_mm2 > secao_atual
When MOD-DC processa
Then revalida C1/C2/C6 com nova seção
And resultado.secao_fase_mm2 é atualizado
And resultado.criterio_decisivo === "C5"
And resultado.alertas inclui "C5-QUEDA-TENSAO-ELEVOU-SECAO"
```

### AC3: Integration with MOD-DC
```gherkin
Given retorno_qt de MOD-QT
When dimensionarCircuito() processa
Then C5 é marcado como APROVADO se retorno.atende === true
And C5 é marcado como REPROVADO se retorno.atende === false
And resultado.rastreio.c5_queda_tensao registra queda_percentual
And resultado.rastreio.c5_queda_tensao registra secao_requerida_mm2 (if provided)
```

### AC4: Test Coverage
```gherkin
Then testes cobrem:
  - Happy path (MOD-QT aprova)
  - Fail path (MOD-QT reprova)
  - Revalidation (seção elevada)
  - Timeout
  - Invalid response
  - Performance < 2s paralelo
```

## Tasks / Subtasks

- [x] **MOD-QT-1.1: API Contract**
  - [x] Define request schema (Zod) — `ValidarMODQTSchema` (AC1 + dependencia_id + origem)
  - [x] Define response schema (RetornoMODQT) — `RetornoMODQTSchema` (já existia)
  - [x] Document endpoint — docblock em `modulos.mod-qt.validar.ts`
  
- [x] **MOD-QT-1.2: Implement Endpoint**
  - [x] Create POST /api/v1/modulos/mod-qt/validar — `src/routes/api/v1/modulos.mod-qt.validar.ts`
  - [x] Add validation — `withZod` (entrada) + `RetornoMODQTSchema.safeParse` (saída, 422 se inválida)
  - [x] Add timeout (5s) — `Promise.race` com `aguardarAbort(signal)` (504/PENDENTE)
  
- [x] **MOD-QT-1.3: Revalidation Loop** (verificação — já implementado no domínio desde v3.0)
  - [x] Check secao_requerida_mm2 > atual — `Math.max(secaoFaseObrigatoria, c5.secao_mm2)` pré-existente
  - [x] Rerun C1/C2/C6 — neutro/PE/PEN dimensionados sobre a seção final pós-C5, pré-existente
  - [x] criterio_decisivo — C5 participa de `criterioDecisivo()`, verificado por E2E
  - [x] Alerta "C5-QUEDA-TENSAO-ELEVOU-SECAO" — pré-existente, verificado por E2E
  
- [x] **MOD-QT-1.4: Integrate with MOD-DC** (verificação — pré-existente)
  - [x] `retorno_qt` em `CircuitoParaDimensionamento` — pré-existente
  - [x] `resolverC5Queda` em `dimensionarCircuito()` — pré-existente
  - [x] Rastreio `c5_queda_tensao` — verificado por teste E2E
  - [x] Revalidation loop — verificado por teste E2E (2,5 mm² → 6 mm²)
  
- [x] **MOD-QT-1.5: Database Persistence**
  - [x] Persist retorno_qt — `retornosDownstream.registrar` (modulo MOD-QT)
  - [x] Test round-trip — asserção via `porDependencia(UUID, "MOD-QT")`
  
- [x] **MOD-QT-1.6: Tests**
  - [x] Unit: Zod validation — request 400 (corrente negativa)
  - [x] Integration: API → DB — round-trip real via handler
  - [x] E2E: MOD-DC flow with revalidation — seção elevada, decisivo C5, alerta
  - [x] Edge cases & performance — 422/500/504 (timeout real com fake timers), paralelo < 2s
  - [x] Revalidation loop tests — comparação com/sem retorno_qt

## Dev Notes

**Files Created/Modified (2026-07-15, @dev Dex — YOLO):**
- `src/api/schemas/otimizar-condutor.schema.ts` — `ValidarMODQTSchema`
- `src/routes/api/v1/modulos.mod-qt.validar.ts` (novo) — endpoint padrão MOD-CC/SEC; mock com queda monofásica simplificada (cobre, 220 V) e projeção de `secao_requerida_mm2` quando reprova
- `tests/api/modulos-mod-qt.test.ts` (novo, 10 testes) — handler real, persistência, revalidação E2E, timeout
- `src/routeTree.gen.ts` — regenerado via `npx vite build`

**Evidência:** targeted 10/10 PASS; `tsc --noEmit` exit 0; eslint exit 0 (pós `--fix`); `vite build` exit 0; suíte completa em execução para o gate @qa.

## QA Results

**Reviewed by:** @qa (Quinn)
**Date:** 2026-07-15
**Gate Decision:** ✅ **PASS**

### Gate-by-Gate Assessment (per `docs/qa/QUALITY-GATES-MOD-CC-SEC-QT.md`)

| # | Gate | Result | Evidência |
|---|------|--------|-----------|
| 1 | API Contract Validation | ✅ PASS | `ValidarMODQTSchema` (campos AC1 + `dependencia_id` + `origem .max(200)`); saída validada com `RetornoMODQTSchema.safeParse` (422 se inválida), incl. `secao_requerida_mm2` opcional |
| 2 | Integration Testing | ✅ PASS | Persistência real via `retornosDownstream.registrar` (modulo MOD-QT); round-trip assertado; falhas não persistem |
| 3 | End-to-End Flow | ✅ PASS | Handler real via `chamar()`; E2E aprovado → C5 APROVADO + `rastreio.c5_queda_tensao`; sem retorno → AGUARDANDO-QT |
| 4 | Edge Case Handling | ✅ PASS | Timeout real 5s (fake timers) → 504/PENDENTE; erro → 500/PENDENTE; contrato inválido → 422; request inválido → 400 |
| 5 | Performance Validation | ✅ PASS | 3 chamadas paralelas < 2s contra o handler real (AC7 do épico) |
| 6 | Security Scanning | ✅ PASS | `origem` limitado; sem secrets/SQLi; validação Zod em entrada e saída |
| 7 | Regression Testing | ✅ PASS | Suíte completa **688/688 (107 arquivos)**; `tsc --noEmit` exit 0; `vite build` exit 0; eslint exit 0 nos arquivos da story |
| 8 | Documentation & Compliance | ✅ PASS | Endpoint documentado com referência normativa (NBR 5410 6.2.7 / laço §20); story atualizada |

### Verificação específica do AC2 (revalidação)

Teste E2E `revalidação: secao_requerida_mm2 maior eleva a seção de fase` comprova o laço já existente no domínio: circuito base fecha em 2,5 mm² (C1/C2/C6); com `retorno_qt.secao_requerida_mm2 = 6` o resultado eleva `secao_fase_mm2` para **6 mm²**, `criterio_decisivo === "C5"`, alerta `C5-QUEDA-TENSAO-ELEVOU-SECAO` presente e C5 REPROVADO rastreado. Neutro/PE dimensionados sobre a seção final (pós-revalidação) — conforme §20 do prompt-base.

**Ressalva não-bloqueante:** CodeRabbit pre-commit delegado ao ciclo @devops (checkpoint). Status: `InReview → Done`.

## Effort

**Estimated:** 6 days (YOLO: mesmo dia — o laço de revalidação já existia no domínio)  
**Depends on:** Phase 1 & 2 complete, MOD-CC-1 & MOD-SEC-1 done

## Change Log

- **2026-07-15 (@po Pax):** validate-story-draft GO 8/10. Status: `Draft → Ready`. Observação: laço de revalidação AC2 já implementado no domínio v3.0 (vira verificação E2E).
- **2026-07-15 (@dev Dex):** implementação completa reutilizando a infraestrutura de retornos downstream (MOD-CC-1). Status: `Ready → InProgress → InReview`.
- **2026-07-15 (@qa Quinn):** gate PASS 8/8 com evidência real (10/10 targeted, 688/688 suíte, tsc/eslint/build limpos), incl. verificação E2E do laço de revalidação (AC2). Status: `InReview → Done`. Ressalva: CodeRabbit pre-commit no checkpoint @devops.

---

**Story created by:** @sm (River)  
**Date:** 2026-07-15  
**Priority:** P0
