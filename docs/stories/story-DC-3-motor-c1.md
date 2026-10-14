# Story DC-3: Motor C1 — Capacidade de Corrente

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-3  
**Status:** Done  
**Priority:** CRITICAL (C1 = critério principal)  
**Complexity:** XL (Tabelas 36–46, fatores de correção, isenções)  
**Dependency:** DC-1, DC-2  
**Assignee:** @dev (Dex)

---

## Story

Como motor de cálculo, preciso implementar o critério C1 (capacidade de condução Iz) com Tabelas 36–39 (Iz base), Tabela 46 (condutores carregados + fator 0,86), Tabelas 40–45 (fatores de correção) e isenções (2×D, ≤30%), para que a seção de condutor seja determinada com precisão.

---

## Acceptance Criteria

### AC-DC-02, AC-DC-03, AC-DC-14, AC-DC-19, AC-DC-24

- [x] **AC-DC-02:** TUE 2F/220 V, IB 34,65 A, B1, 3 agrupados → n_carregados=2, Iz corrigida calcula seção corretamente
- [x] **AC-DC-03:** Bifásico com neutro → n_carregados=3 (não 2)
- [x] **AC-DC-14:** 3F+N com TH3>15% → 4 carregados, fator 0,86 rastreado
- [x] **AC-DC-19:** Método D usa bloco "solo" da Tab. 40; outros usam "ambiente"
- [x] **AC-DC-24:** Grupo não semelhante → F=1/√n substitui fator tabelado; n=10 → F≈0,316

**Verificação:** Testes contra exemplos numéricos do documento-base; rastreio completo.

---

## Dev Notes

### Classes principais

```typescript
class MotorCapacidadeCorrente {
  calcular(entrada: CircuitoParaDimensionamento): ResultadoC1 {
    // Tabela 46: determinar n_carregados
    const nCarregados = this.determinarCondutoresCarregados(entrada);
    
    // Tabelas 36-39: Iz base
    const izBase = this.consultarIzBase(
      entrada.tabela, entrada.material, entrada.isolacao,
      entrada.metodo, nCarregados, entrada.secao
    );
    
    // Fatores de correção
    const fatores = {
      fct: this.fatorTemperatura(entrada),
      frs: this.fatorResistividadeSolo(entrada),
      fca: this.fatorAgrupamento(entrada)
    };
    
    // Iz corrigida
    const izCorrigida = izBase * fatores.fct * fatores.frs * fatores.fca;
    
    return { izBase, izCorrigida, fatores, rastreio };
  }
}
```

### Tarefas

1. [x] Implementar `MotorCapacidadeCorrente` (REUSE de `motor-capacidade-corrente.ts`)
2. [x] Tabela 46: determinar n_carregados (bifásico+N=3, fator 0,86)
3. [x] Fatores de correção (FCT, FRS, FCA)
4. [x] Isenções: espaçamento 2×D (já existente), exclusão ≤30% (`circuitos_desprezaveis_ate_30pct`)
5. [x] Grupos não semelhantes: F=1/√n (`grupo_nao_semelhante`)
6. [x] Rastreio completo: fatores (FCT/FRS/FCA/neutro) + `rastreio.c1_iz` (tabela/fonte/status)

### Bloqueadores

- **VER-DC-01:** Tabelas 36–39 incompletas → usa `[VERIFICAR]` bloqueante
- Nenhum novo bloqueio arquitetural (AD-DC-01 já decidido)

---

## File List

> Nota IDS: o Motor C1 já existia no submódulo (landed com DC-4). Decisão **ADAPT/REUSE**
> em vez de CREATE — os nomes de arquivo originalmente sugeridos na story
> (`src/domain/dimensionamento/MotorCapacidadeCorrente.ts` etc.) foram substituídos pelos
> caminhos reais do submódulo para evitar duplicação. Ver `decision-log-DC-3.md`.

**Modified (submódulo `sistema-de-instala-es-el-tricas-sie-main/`):**
- `src/domain/dimensionamento-condutores/motores/motor-capacidade-corrente.ts` — AC-DC-24 (F=1/√n) + isenção ≤30%
- `src/domain/dimensionamento-condutores/contratos.ts` — campos `grupo_nao_semelhante`, `circuitos_desprezaveis_ate_30pct`

**Created (submódulo):**
- `tests/domain/dimensionamento-condutores/motor-c1.test.ts` — 6 exemplos numéricos (AC-DC-02/03/14/19/24 + isenção ≤30%)

**Created (raiz):**
- `docs/stories/decision-log-DC-3.md`

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity XL adicionada; Status Draft → Ready
- **2026-07-12:** @dev Dex — Status Ready → InProgress. Início da implementação C1 (SEARCH IDS: motor pré-existente no submódulo).
- **2026-07-12:** @dev Dex — Implementado AC-DC-24 (grupo não semelhante F=1/√n) e isenção ≤30% no motor; AC-DC-02/03/14/19 já cobertos por código pré-existente, reforçados com testes. Contratos estendidos (2 campos opcionais). 6 testes focados PASS; suíte de domínio 31/31 PASS; typecheck limpo; eslint limpo. Status InProgress → InReview.
- **2026-07-12 (v1.0.0):** @qa Quinn — QA Gate **PASS**. 7/7 gates aprovados; evidência re-executada pela QA (domínio 31/31, API 2/2, tsc exit 0); AC-DC-24 e isenção ≤30% verificados no código-fonte (não apenas docs). Contratos confirmados aditivos/opcionais. Status InReview → Done. DC-4 desbloqueada. Gate: docs/qa/gates/DC-3-motor-c1.yml

---

## QA Results

### Review Date: 2026-07-12

### Reviewed By: Quinn (Test Architect)

**Verdict: PASS** — 7/7 quality gates clear. Evidence re-executed by QA (not accepted from handoff summary alone).

| # | Gate | Verdict | QA Evidence |
|---|------|---------|-------------|
| 1 | Acceptance Criteria | PASS | AC-DC-02/03/14/19/24 + ≤30% exemption verified in source (`motor-capacidade-corrente.ts`) and via 6 numeric worked examples |
| 2 | Type Safety & Lint | PASS | `npx tsc --noEmit` → exit 0 (re-run by QA) |
| 3 | Integration | PASS | Isolated in `motores/`; consumes DC-1 base normativa + DC-2 inputs; no cross-module contamination |
| 4 | Regression | PASS | Domain suite 31/31, API contract 2/2 (both re-run by QA) — no regressions |
| 5 | Documentation | PASS | `decision-log-DC-3.md`; AC traced to CA-DC-*; IDS ADAPT/REUSE rationale logged |
| 6 | File Inventory | PASS | Matches File List: motor + contratos (modified), motor-c1.test.ts + decision-log (created) |
| 7 | Done Criteria | PASS | All AC implemented & tested; File List complete; Change Log updated; DC-4 unblocked |

**Verification notes:**
- Confirmed `contratos.ts` additions (`grupo_nao_semelhante`, `circuitos_desprezaveis_ate_30pct`) are optional/additive → no breaking change to existing consumers.
- AC-DC-24 math confirmed in source: `1 / Math.sqrt(nEfetivo)`; n=10 → 0,316 (≠ 0,5 tabelado).
- AC-DC-19 Method-D "solo" branch confirmed at source line 57.
- ≤30% exemption is opt-in (default 0) — no auto-invention, respects Constitution Art. IV.

### Gate Status

Gate: PASS → docs/qa/gates/DC-3-motor-c1.yml
