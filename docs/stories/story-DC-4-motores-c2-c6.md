# Story DC-4: Motores C2 e C6 + Seleção Final

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-4  
**Status:** Done  
**Priority:** CRITICAL (seleção final de seção)  
**Complexity:** L (C2 + C6 + orquestração de seleção)  
**Dependency:** DC-1, DC-3  
**Assignee:** @dev (Dex)

---

## Story

Como motor de cálculo, preciso implementar os critérios C2 (proteção contra sobrecargas) e C6 (seções mínimas) e orquestrar a seleção final de seção (max entre C1, C2, C6, C5 quando aplicável), para que nenhuma seção seja subdimensionada.

---

## Acceptance Criteria

### AC-DC-01, AC-DC-06, AC-DC-12, AC-DC-18

- [x] **AC-DC-01:** ILU Cu PVC B1 30 °C, IB=2,36 A → S fase=1,5 mm² (C6 governa o piso) — ver nota decisivo no decision-log
- [x] **AC-DC-06:** Seção final ∈ série normalizada IEC 60228 (1,5; 2,5; 4; 6; 10; 16; 25; 35; 50; 70; 95; 120; 150; 185; 240; 300; 400; 500; 630; 800; 1000 mm²)
- [x] **AC-DC-12:** In > Iz corrigida → sugestão de seção superior (`proximaSecao`); IB > In → C2 REPROVADO
- [x] **AC-DC-18:** I2 ausente → `PENDENTE-I2`; I2 informado → condição b) avaliada; `regime_sobrecarga_severo` transforma b) (1,45·Iz → 1,0·Iz)

**Verificação:** Testes contra exemplos numéricos; seção selecionada é max(C1, C2, C6).

---

## Dev Notes

### Classe SeletorSecaoNormalizada

```typescript
class SeletorSecaoNormalizada {
  selecionarFinal(criterios: {c1: Resultado, c2: Resultado, c6: Resultado}): SecaoFinal {
    // Invariante: seção_final = max seção entre critérios aprovados
    const secoesAproadas = [
      criterios.c1.secao_calculada,
      criterios.c2.secao_calculada,
      criterios.c6.secao_minima
    ].filter(s => s !== null);
    
    const secaoFinal = Math.max(...secoesAprovadas);
    
    // Validar série normalizada
    if (!SERIE_NORMALIZADA.includes(secaoFinal)) {
      throw Error('INC-07: seção não normalizada');
    }
    
    return { secaoFinal, criterioDecisivo, rastreio };
  }
}
```

### Tarefas

1. [x] `MotorSobrecarga` (5.3.4.1: IB ≤ In ≤ Iz; I2 ≤ 1,45·Iz com I2 real) — REUSE `motor-sobrecarga.ts`
2. [x] Tabela 47: seções mínimas por tipo de utilização — REUSE `motor-secao-minima.ts`
3. [x] Seletor de seção normalizada (max entre critérios, valida série) — REUSE orquestração em `servico-dimensionamento-condutores.ts`
4. [x] Rastreio de critério decisivo — REUSE `criterioDecisivo` (nota: C2 absorve piso C6, ver decision-log)
5. [x] Testes parametrizados para múltiplos cenários — CREATE `motor-c2-c6.test.ts` (11 casos, AC-DC-01/06/12/18)

### Bloqueadores

- **VER-DC-04:** Relação I2/In por norma de dispositivo (condiciona PENDENTE-I2)
- Nenhum novo bloqueio

---

## File List

> Caminhos reais no submódulo `sistema-de-instala-es-el-tricas-sie-main/`. Nomes originais da story (`MotorSobrecarga.ts`, `SeletorSecaoNormalizada.ts`) eram placeholders — ver decision-log-DC-4 (IDS REUSE).

**Created:**
- `tests/domain/dimensionamento-condutores/motor-c2-c6.test.ts` (11 casos — AC-DC-01/06/12/18)
- `docs/stories/decision-log-DC-4.md`

**Reused (verificado, sem alteração — código pré-existente):**
- `src/domain/dimensionamento-condutores/motores/motor-sobrecarga.ts` (C2 — 5.3.4.1)
- `src/domain/dimensionamento-condutores/motores/motor-secao-minima.ts` (C6 — Tab. 47)
- `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts` (seleção final normalizada)

**Modified:**
- `docs/stories/story-DC-4-motores-c2-c6.md` (status, AC, subtarefas, File List, Change Log)

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity L adicionada; Status Draft → Ready
- **2026-07-12:** @dev Dex (YOLO) — Status Ready → InProgress → InReview. C2/C6/seleção final já existiam no submódulo (IDS REUSE); entrega = cobertura de teste rastreável `motor-c2-c6.test.ts` (11/11 PASS). AC-DC-01/06/12/18 validados. Gates: domínio 42/42, API 54/54, tsc limpo, eslint limpo, sem regressões. Decisões em `decision-log-DC-4.md`. Sem git push (→ @devops).
- **2026-07-12:** @qa Quinn — QA Gate **PASS** — Status: InReview → Done. Testes re-executados pela QA (focados 11/11, domínio 42/42, tsc exit 0); REUSE confirmado via git status (0 alterações de produção). Gate: `docs/qa/gates/DC-4-motores-c2-c6.yml`. DC-5 desbloqueada.

---

## QA Results

### Review Date: 2026-07-12

### Reviewed By: Quinn (Test Architect)

**Escopo verificado:** AC do arquivo da story (DC-01/06/12/18). Os AC do prompt de spawn divergiam; @dev seguiu corretamente o arquivo da story (Constitution Art. III/IV — No Invention). Gate avalia exclusivamente os AC da story.

**Evidência (re-executada pela QA, não apenas documental):**
- Focados: `npx vitest run motor-c2-c6.test.ts` → **11/11 PASS**
- Suíte de domínio: `npx vitest run tests/domain/dimensionamento-condutores` → **42/42 PASS** (sem regressões)
- Typecheck: `npx tsc --noEmit` → **exit 0**
- REUSE confirmado: `git status` mostra `motor-sobrecarga.ts`, `motor-secao-minima.ts` e `servico-dimensionamento-condutores.ts` **sem modificação**; `motor-c2-c6.test.ts` como untracked (CREATE). Zero alteração de código de produção.

**7-Point Gate:** Acceptance Criteria ✅ · Type/Lint ✅ · Integração ✅ · Regressão ✅ · Documentação ✅ · File Inventory ✅ · Done Criteria ✅

**Notas de design (informativas, não bloqueantes):**
- `criterio_decisivo` nunca reporta "C6" por design (C2 absorve o piso C6); o efeito material (piso respeitado) é testado — correto.
- In>Iz auto-remedia (sobe seção) em vez de REPROVAR; REPROVADO reservado a IB>In / I2>limite — coerente com AC-DC-12.

### Gate Status

Gate: PASS → docs/qa/gates/DC-4-motores-c2-c6.yml
