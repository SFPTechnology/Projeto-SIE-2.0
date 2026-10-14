# Story DC-9: UI — Lote, Comparação e Resumo

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-9  
**Status:** Ready  
**Priority:** HIGH (UX lote + resumo)  
**Complexity:** L (editor de lote + comparador + resumo)  
**Dependency:** DC-7, DC-8  
**Assignee:** @dev (Dex) / @ux-design-expert (Uma)

---

## Story

Como projetista, preciso editar circuitos em lote com padrões visíveis e editáveis, comparar cenários (Cu × Al, PVC × EPR, métodos, temperaturas), e visualizar resumo do projeto (totais por estado, critério decisivo mais frequente, histograma de seções), para que decisões de projeto sejam rápidas e informadas.

---

## Acceptance Criteria

### AC-DC-10 (parcial), R-11

- [ ] **AC-DC-10 (parcial):** UI em modo assistido e avançado; edição em lote com padrões visíveis
- [ ] **R-11:** Overrides auditados (justificativa, autor, reversível, preserva valor calculado)

**Verificação:** Testes de UX; auditoria de overrides.

---

## Dev Notes

### Componentes React

```typescript
// Modo assistido vs avançado
DimenisionadorWorkspace.modo = 'assistido' | 'avançado'

// Edição em lote
EditorLote
  ├─ Seleção múltipla de circuitos
  ├─ Padrões aplicáveis (temperatura, agrupamento, método)
  ├─ Preview de impacto (Iz corrigida, seção nova)
  └─ Confirmação + rastreio de mudança

// Comparação de cenários
ComparadorCenarios
  ├─ Cenário A vs Cenário B (Cu × Al, PVC × EPR, etc.)
  ├─ Delta: diferença de seção, custo, peso
  ├─ Nota: "Opção mais barata nunca marcada como 'melhor' automaticamente"
  └─ Exportação de comparação

// Resumo do projeto
ResumoProjeto
  ├─ Totais por estado (# RASCUNHO, # DADOS-INCOMPLETOS, # DIMENSIONAL-PARCIAL, etc.)
  ├─ Critério decisivo mais frequente (histograma)
  ├─ Histograma de seções (distribuição)
  ├─ Aviso permanente: "X circuitos com pendência C3/C4/C5"
  └─ Exportação (relatório PDF)
```

### Tarefas

1. [ ] Implementar modo assistido vs avançado
2. [ ] Editor em lote com padrões visíveis e editáveis
3. [ ] Comparador de cenários (Cu × Al, PVC × EPR, etc.)
4. [ ] Resumo do projeto (totais, histogramas, avisos)
5. [ ] Testes de UX para lote e comparação

### Bloqueadores

- Nenhum novo

---

## File List

**Created/Modified:**
- `src/ui/componentes/EditorLote.tsx`
- `src/ui/componentes/ComparadorCenarios.tsx`
- `src/ui/componentes/ResumoProjeto.tsx`
- `tests/ui/EditorLote.test.tsx`
- `tests/ui/ComparadorCenarios.test.tsx`

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity L adicionada; Status Draft → Ready
