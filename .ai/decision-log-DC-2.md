# Decision Log — Story DC-2 (Validação de Entradas e Guardas)

**Agent:** @dev (Dex) — YOLO mode
**Date:** 2026-07-12
**Branch:** feature/nbr5410-conformidade-closeout

## Context

Story DC-2 asks for a validation layer (`ValidadorEntradas`) that guards all MOD-DC
circuit inputs before calculation. On entry, the MOD-DC domain already exists in the
submodule `sistema-de-instala-es-el-tricas-sie-main` (committed as part of the DC-4
commit `1e18cc9` on the closeout branch), including a complete
`src/domain/dimensionamento-condutores/validacao/validador-entradas.ts`.

## IDS Decisions (SEARCH → DECIDE → LOG)

### D1 — Validator implementation
- **Searched:** `src/domain/dimensionamento-condutores/validacao/validador-entradas.ts`, `erros.ts`, `contratos.ts`.
- **Found:** `validarEntradasDimensionamento(circuito, parametros)` returning a
  readonly array of `DiagnosticoEntradaDimensionamento { codigo, mensagem }`.
- **Decision:** **REUSE** (relevance ~100%). The existing pure function already
  implements every guard required by AC-1..AC-5:
  - AC-1 tensão ausente → `ERRO-TENSAO-AUSENTE`
  - AC-2 isolação ausente → `ERRO-ISOLACAO-AUSENTE`; método ausente → `ERRO-METODO-AUSENTE`
  - AC-3 alumínio residencial/comercial/industrial (BA5/BD) → `ERRO-MATERIAL-NAO-ADMITIDO`
  - AC-4 `num_circuitos_agrupados <= 0` → `ERRO-AGRUPAMENTO-NAO-TABELADO`;
    `corrente_projeto_a <= 0` → `ERRO-CONSULTA-INCOMPLETA`
  - AC-5 pure domain function, imports only from `../contratos` and `../erros` — isolated.
- **Rationale:** Rewriting would violate REUSE>ADAPT>CREATE and risk regressing the
  DC-3..DC-10 motors that already consume the contract. No change was required.

### D2 — Error catalog
- **Searched:** `erros.ts`.
- **Found:** `CodigoErroDimensionamento` union already enumerates the codes used by the
  guards (`ERRO-TENSAO-AUSENTE`, `ERRO-ISOLACAO-AUSENTE`, `ERRO-METODO-AUSENTE`,
  `ERRO-MATERIAL-NAO-ADMITIDO`, `ERRO-AGRUPAMENTO-NAO-TABELADO`, `ERRO-CONSULTA-INCOMPLETA`, …).
- **Decision:** **REUSE**. Catalog is complete for the DC-2 guard surface. No new codes added.

### D3 — Non-cataloged diagnostic (diagnostics vs. throw)
- The story Dev Notes sketched a `throw new Error(...)` style validator.
- The existing implementation instead **returns a diagnostics array** (fail-closed at the
  caller). This is superior: it collects all violations at once and keeps the guard a pure
  function. **Decision: keep the array-return contract** (no throw), consistent with the
  rest of the module. `[AUTO-DECISION] throw-vs-collect → collect diagnostics
  (reason: aggregates all errors, pure/testable, already consumed downstream).`

### D4 — Test coverage
- **Searched:** `tests/domain/dimensionamento-condutores/mod-dc.test.ts`.
- **Found:** one DC-2 test covering AC-1 + AC-3(residencial) only.
- **Decision:** **ADAPT** the test file — append a dedicated
  `describe("MOD-DC DC-2 - guardas de validacao de entradas")` block with 6 tests giving
  explicit per-AC coverage (AC-1, AC-2 isolação+método, AC-3 residencial/comercial negative
  + industrial-BA5 positive, AC-4 agrupamento+corrente, and a valid-input happy path).
- **Change size:** additive only; existing tests untouched (a prettier `--fix` normalized
  three pre-existing formatting lines in the same file — no logic change).

## AC-DC-17 (cor-função) — scope note
The story-file AC list includes `AC-DC-17` (neutro azul-clara / PE verde → `ERRO-COR-FUNCAO`).
The launching-agent task scoped DC-2 to AC-1..AC-5 (tensão, isolação/método, material,
agrupamento/corrente, isolamento). Conductor-color/function validation belongs to the
neutro/PE domain (DC-5, `motor-neutro` / `motor-pe-pen`) and is intentionally NOT added to
`validador-entradas` here to avoid cross-module scope creep (AC-5). `ERRO-COR-FUNCAO`
remains reserved in the error catalog for that story.

## Verification
- `npx vitest run tests/domain/dimensionamento-condutores/mod-dc.test.ts` → 13 passed
- `npx vitest run tests/domain/dimensionamento-condutores` → 25 passed (3 files, no regressions)
- `npx tsc --noEmit` → exit 0 (clean)
- `npx eslint` on touched files → exit 0 (clean after prettier normalization)
