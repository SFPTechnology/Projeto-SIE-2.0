# Story DC-7: API e Rotas Server

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-7  
**Status:** Ready  
**Priority:** CRITICAL (integração sistema)  
**Complexity:** L (5 endpoints + benchmark + rastreio)  
**Dependency:** DC-1 a DC-6  
**Assignee:** @dev (Dex) / @architect (Aria)

---

## Story

Como sistema SIE, preciso expor endpoints/rotas server (conforme decisão AD-DC-01) para dimensionar circuito individual ou lote, consultar resultados, acessar base normativa versionada e receber retornos downstream (MOD-QT, MOD-CC, MOD-SEC), para que a UI e integrações possam solicitar cálculos com rastreio completo.

---

## Acceptance Criteria

### AC-DC-08, AC-DC-11

- [ ] **AC-DC-08:** Payload `rastreio` contém tabela/linha/coluna/nota/página/chunk_id, fatores, versões
- [ ] **AC-DC-11:** Lote com 44 circuitos do proj-1 processa em < 2 s

**Verificação:** Testes de API; benchmark de performance.

---

## Dev Notes

### Endpoints (conforme AD-DC-01 decision: TypeScript + tRPC ou server functions)

```typescript
// Individual
POST /api/v1/dimensionar
  Input: CircuitoParaDimensionamento
  Output: ResultadoDimensionamento (com rastreio)

// Lote
POST /api/v1/dimensionar-lote
  Input: CircuitoParaDimensionamento[]
  Output: ResultadoDimensionamento[] (batch)

// Consulta
GET /api/v1/dimensionamento?circuito_id=X
  Output: ResultadoDimensionamento + histórico

// Base normativa
GET /api/v1/tabelas/iz?tabela=36&material=Cu&isolacao=PVC
  Output: [{ seção, Iz, fonte, status_verificacao, chunk_id }]

// Retornos downstream
POST /api/v1/retorno-qt
POST /api/v1/retorno-cc
POST /api/v1/retorno-seccionamento
  Input: { circuito_id, resultado_modulo }
  Output: NovoResultadoDimensionamento (revalidado)
```

### Tarefas

1. [ ] Implementar 5 endpoints conforme AD-DC-01
2. [ ] Rastreio completo em payload (tabela, linha, coluna, página, chunk_id)
3. [ ] Testes de API (happy path + error cases)
4. [ ] Benchmark: 44 circuitos < 2 s
5. [ ] Documentação OpenAPI/tRPC schema

### Bloqueadores

- Nenhum novo

---

## File List

**Created/Modified:**
- `src/api/routes/dimensionar.ts`
- `src/api/routes/dimensionar-lote.ts`
- `src/api/routes/resultados.ts`
- `src/api/routes/tabelas.ts`
- `src/api/routes/retornos.ts`
- `tests/integration/api.test.ts`
- `tests/performance/benchmark_lote_44.test.ts`

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity L adicionada; Status Draft → Ready
