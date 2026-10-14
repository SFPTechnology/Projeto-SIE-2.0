# Story DC-2: Validação de Entradas e Guardas

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-2  
**Status:** Done  
**Priority:** CRITICAL (blocker para DC-3...DC-9)  
**Complexity:** M (validação + catálogo de 14 erros)  
**Dependency:** DC-1 (base normativa)  
**Assignee:** @dev (Dex)

---

## Story

Como motor de cálculo, preciso validar todas as entradas de circuito (tensão, isolação, material, método) antes de processar, para que erros normalizados bloqueiem o cálculo e nenhuma falha silenciosa ocorra.

---

## Acceptance Criteria

### AC-DC-04 a AC-DC-05, AC-DC-13, AC-DC-17

- [x] **AC-DC-04:** `tensao_v=None` → erro `ERRO-TENSAO-AUSENTE`, nenhum cálculo prossegue
- [x] **AC-DC-05:** Isolação ausente → `ERRO-ISOLACAO-AUSENTE` (+ `ERRO-METODO-AUSENTE` para método de referência ausente); dropdown UI sem opção vazia _(guarda de domínio implementada; enforcement do dropdown pertence à UI — DC-8)_
- [x] **AC-DC-13:** Alumínio em projeto residencial/comercial → `ERRO-MATERIAL-NAO-ADMITIDO` (6.2.3.8); industrial com BA5 → admitido
- [ ] **AC-DC-17:** Neutro não azul-clara ou PE não verde/verde-amarela → `ERRO-COR-FUNCAO` _(fora do escopo desta story: validação de cor/função pertence ao domínio neutro/PE — DC-5. `ERRO-COR-FUNCAO` permanece reservado no catálogo)_

**Verificação:** Testes unitários validam cada guarda; no painel de erro, mensagem específica vinculada à norma.

---

## Dev Notes

### Classe ValidadorEntradas

```typescript
class ValidadorEntradas {
  validar(entrada: CircuitoParaDimensionamento): ValidationResult {
    // R-03: tensao_v obrigatória
    if (!entrada.tensao_v) throw new Error('ERRO-TENSAO-AUSENTE');
    
    // R-06: isolação obrigatória
    if (!entrada.isolacao) throw new Error('ERRO-ISOLACAO-AUSENTE');
    
    // R-07: material + tipo_instalacao se alumínio
    if (entrada.material === 'Al' && entrada.tipo_instalacao === 'residencial') {
      throw new Error('ERRO-MATERIAL-NAO-ADMITIDO');
    }
    
    // R-08: cores função × cor
    if (entrada.cor_neutro !== 'azul-clara') {
      throw new Error('ERRO-COR-FUNCAO');
    }
    
    return { valid: true };
  }
}
```

### Tarefas

1. [x] Implementar `ValidadorEntradas` com 8+ guardas — `validarEntradasDimensionamento` (tensão, isolação, método, material Al × contexto/BA5/BD, agrupamento, corrente de projeto)
2. [x] Catálogo de erros: códigos em `erros.ts` (`CodigoErroDimensionamento`) cobrindo a superfície de guardas DC-2
3. [x] Testes unitários para cada guarda (happy path + error cases) — 6 testes AC-1..AC-4 em `mod-dc.test.ts`
4. [x] Mensagens de erro localizadas (português) com referência normativa

### Bloqueadores

- Nenhum novo; depende de DC-1 estar 100% funcional

---

## File List

Caminhos relativos ao submódulo `sistema-de-instala-es-el-tricas-sie-main/`.

**Reused (IDS REUSE — já existente no módulo MOD-DC, satisfaz AC-1..AC-5 sem alteração):**
- `src/domain/dimensionamento-condutores/validacao/validador-entradas.ts` — `validarEntradasDimensionamento` + `DiagnosticoEntradaDimensionamento`
- `src/domain/dimensionamento-condutores/erros.ts` — catálogo `CodigoErroDimensionamento`
- `src/domain/dimensionamento-condutores/contratos.ts` — `CircuitoParaDimensionamento`, `ParametrosDimensionamento`
- `src/domain/dimensionamento-condutores/index.ts` — barrel export do validador

**Modified (ADAPT — cobertura de testes adicionada):**
- `tests/domain/dimensionamento-condutores/mod-dc.test.ts` — bloco `describe("MOD-DC DC-2 - guardas de validacao de entradas")` com 6 testes (AC-1..AC-4)

**Created (rastreabilidade, repo raiz):**
- `.ai/decision-log-DC-2.md` — log de decisões IDS/YOLO

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity M adicionada; Status Draft → Ready
- **2026-07-12:** @dev Dex — Status Ready → InProgress. IDS: validador de entradas já presente no módulo MOD-DC (commit DC-4 `1e18cc9`) e satisfaz AC-1..AC-5 → decisão REUSE (sem reescrita). Guardas verificadas: tensão (AC-1), isolação+método (AC-2), material Al × contexto/BA5/BD (AC-3), agrupamento+corrente (AC-4), isolamento de domínio (AC-5).
- **2026-07-12:** @dev Dex — ADAPT: adicionados 6 testes unitários por-AC em `mod-dc.test.ts`. Verificação: vitest 13/13 (arquivo) e 25/25 (suíte MOD-DC); `tsc --noEmit` limpo; eslint limpo. AC-DC-17 (cor/função) marcada fora de escopo → DC-5. Status InProgress → InReview. Pronto para handoff @qa.

| Data | Versão | Descrição | Autor |
|------|--------|-----------|-------|
| 2026-07-12 | 1.0.0 | QA Gate PASS — Status: InReview → Done | @qa |

## QA Results

### Review Date: 2026-07-12

### Reviewed By: Quinn (Test Architect)

Revisão executada de forma autônoma (YOLO). Todas as alegações do @dev foram verificadas independentemente re-executando os testes e o typecheck — não confiei apenas na documentação.

**7-Point QA Gate:**

1. **Acceptance Criteria** — PASS. AC-DC-04 / AC-DC-05 / AC-DC-13 implementadas e cobertas por testes (AC-1..AC-4). AC-DC-17 (cor/função) legitimamente fora de escopo → DC-5, com `ERRO-COR-FUNCAO` reservado no catálogo.
2. **Type Safety & Linting** — PASS. `tsc --noEmit` exit 0 (verificado).
3. **Integration** — PASS. `validarEntradasDimensionamento` é função pura, isolada em `src/domain/dimensionamento-condutores/`, importa apenas `../contratos` + `../erros`. Sem contaminação cross-module.
4. **Regression** — PASS. Suíte de domínio `dimensionamento-condutores/` 25/25 verde; nenhum regresso fora do escopo DC-2.
5. **Documentation** — PASS. Decisão IDS (REUSE do validador + ADAPT dos testes) registrada; carve-outs de escopo (DC-5, DC-8) claros.
6. **File Inventory** — PASS. File List consistente com o diff (teste modificado; validador reaproveitado sem alteração).
7. **Done Criteria** — PASS. Pronto para transição; DC-3 desbloqueado.

**Evidência re-executada por @qa:**
- Focused: 13/13 pass (`tests/domain/dimensionamento-condutores/mod-dc.test.ts`)
- Domain suite: 25/25 pass (`tests/domain/dimensionamento-condutores/`)
- Typecheck: `tsc --noEmit` exit 0

**Observação (não bloqueante):** o pseudocódigo ilustrativo em Dev Notes exibe uma guarda `cor_neutro`/`ERRO-COR-FUNCAO` que **não** existe na implementação real — o que está correto, pois AC-DC-17 foi diferida para DC-5. Divergência apenas no exemplo ilustrativo da story, não no código.

### Gate Status

Gate: PASS → docs/qa/gates/DC-2-validacao.yml
