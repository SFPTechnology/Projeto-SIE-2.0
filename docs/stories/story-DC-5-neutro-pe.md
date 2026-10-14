# Story DC-5: Neutro, PE e PEN

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-5  
**Status:** InReview  
**Priority:** HIGH (requisito normativo)  
**Complexity:** M (Tabelas 48/58 + validação PEN)  
**Dependency:** DC-1, DC-4  
**Assignee:** @dev (Dex)

---

## Story

Como motor de cálculo, preciso implementar os critérios de dimensionamento de neutro (6.2.6.2 + Tabela 48), proteção PE (Tabela 58) e validação de PEN (esquema TN-C), para que circuitos trifásicos equilibrados aproveitem reduções de neutro quando 5 condições forem simultâneas.

---

## Acceptance Criteria

### AC-DC-15, AC-DC-16

- [x] **AC-DC-15:** Trifásico S_fase=35 mm², equilibrado, TH3≤15%, neutro protegido → neutro redutível a 25 mm² (Tab. 48); sem as 5 condições → neutro=fase
- [x] **AC-DC-16:** S_fase=50 mm² → S_PE=25 mm²; S_fase=10 → PE=10; S_fase=25 → PE=16 (Tab. 58)

**Verificação:** Testes contra tabelas; regressão CA-DC-15/16.

---

## Dev Notes

### Classes principais

```typescript
class MotorCondutorNeutro {
  dimensionar(entrada: CircuitoParaDimensionamento, secaoFase: number): SecaoNeutro {
    // 5 condições para redução (6.2.6.2)
    if (this.verificarCondicoes(entrada)) {
      // Tabela 48: redução autorizada
      return { secaoNeutro: this.consultarTab48(secaoFase), reducao: true };
    } else if (entrada.th3 > 33%) {
      return { erro: 'VERIFICAR-NEUTRO-HARMONICAS', bloqueante: true };
    } else {
      return { secaoNeutro: secaoFase, reducao: false };
    }
  }
}

class MotorCondutorProtecao {
  dimensionar(secaoFase: number): SecaoPE {
    // Tabela 58
    return this.consultarTab58(secaoFase);
  }
}
```

### Tarefas

1. [x] `MotorCondutorNeutro`: 5 condições + Tabela 48 — REUSE `motores/motor-neutro.ts` (`dimensionarNeutro`)
2. [x] `MotorCondutorProtecao`: Tabela 58 (Pe em função de seção fase) — REUSE `motores/motor-pe-pen.ts` (`dimensionarPe`)
3. [x] Validação PEN (TN-C, ≥10 mm² Cu / 16 mm² Al) — REUSE `motores/motor-pe-pen.ts` (`dimensionarPen`)
4. [x] Bloqueio `VERIFICAR-NEUTRO-HARMONICAS` quando TH3>33% — REUSE `motor-neutro.ts`
5. [x] Testes com e sem redução de neutro — CREATE `tests/domain/dimensionamento-condutores/motor-neutro-pe.test.ts`

### Bloqueadores

- **VER-DC-08:** Anexo F (TH3 > 33%) detalhes

---

## File List

> Nota (@dev): a implementação real do MOD-DC usa kebab-case sob
> `src/domain/dimensionamento-condutores/` (não os nomes PascalCase/paths
> `src/domain/dimensionamento/` do rascunho). Os motores já estavam
> implementados à frente da story (commits DC-1/DC-4). DC-5 é REUSE dos motores
> + CREATE da cobertura de testes dedicada (Task 5). Todos os paths abaixo são
> relativos ao submódulo `sistema-de-instala-es-el-tricas-sie-main/`.

**Reused (verificados, sem modificação):**
- `src/domain/dimensionamento-condutores/motores/motor-neutro.ts` — `dimensionarNeutro` (5 condições + Tab. 48 + bloqueio harmônicas)
- `src/domain/dimensionamento-condutores/motores/motor-pe-pen.ts` — `dimensionarPe` (Tab. 58) + `dimensionarPen` (TN-C)
- `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts` — integra neutro/PE/PEN sobre a seção de fase final

**Created:**
- `tests/domain/dimensionamento-condutores/motor-neutro-pe.test.ts` — 18 testes (AC-DC-15, AC-DC-16, Task 3 PEN, Task 4 harmônicas)

**Modified:**
- `docs/stories/story-DC-5-neutro-pe.md` — status, checkboxes, File List, Change Log

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity M adicionada; Status Draft → Ready
- **2026-07-13:** @dev Dex — Status Ready → InProgress. IDS: motores neutro/PE/PEN já existentes (código à frente da story) → REUSE; gap real era Task 5 (testes dedicados) → CREATE `motor-neutro-pe.test.ts` (18 testes). AC-DC-15/AC-DC-16 verificados contra os motores. AC-DC-17 (cor/função de condutores) do prompt de missão NÃO consta nas AC da story → não implementado (Art. IV No Invention). Focados 18/18 ✅; suíte domínio 60/60 (6 arquivos, sem regressão) ✅; tsc limpo ✅; eslint limpo ✅. Status InProgress → InReview.
