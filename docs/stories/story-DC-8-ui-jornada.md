# Story DC-8: UI — Jornada e Tabela de Resultados

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-8  
**Status:** Ready  
**Priority:** HIGH (UX principal)  
**Complexity:** XL (12 seções de jornada + tabela 16 colunas + WCAG AA)  
**Dependency:** DC-6, DC-7 (parcial)  
**Assignee:** @dev (Dex) / @ux-design-expert (Uma)

---

## Story

Como usuário engenheiro, preciso de uma jornada intuitiva de dimensionamento (identificação → revisão de dados → contexto normativo → sistema elétrico → condutor → tipo de linha → influências → agrupamento → proteção → verificações → comparação → resultado) e uma tabela de resultados com os 6 critérios e critério decisivo destacado, para que eu possa revisar e aprovar dimensionamentos sem erros.

---

## Acceptance Criteria

### AC-DC-10, AC-DC-22

- [ ] **AC-DC-10:** UI exibe 6 critérios (C1–C6) e destaca critério decisivo com **rótulo textual** (não só cor)
- [ ] **AC-DC-22:** Texto branco sobre `#fa4d56` ausente em todos os estados (WCAG AA contraste ≥ 4,5:1)

**Verificação:** Inspeção visual + teste automatizado de acessibilidade.

---

## Dev Notes

### Componentes React + IBM Carbon

```typescript
// Jornada em wizard/formulário
DimensionadorWorkspace
  ├─ SecaoIdentificacao
  ├─ SecaoRevisaoDados (badge de origem)
  ├─ SecaoContextoNormativo (referências NBR + EDP)
  ├─ SecaoSistemaEletrico (esquema, tensão, fases)
  ├─ SecaoCodutores (material, isolação)
  ├─ SecaoTipoLinha (Tabela 33, método derivado)
  ├─ SecaoInfluencias (temperatura, solo, agrupamento)
  ├─ SecaoAgrupamento (faixas Tabelas 42-45)
  ├─ SecaoProtecao (In, I2, tipo dispositivo)
  ├─ SecaoVerificacoes (resumo dos 6 critérios por estado)
  ├─ SecaoComparacao (Cu × Al, PVC × EPR, cenários)
  └─ SecaoResultadoAprovacao (autor, data, versão)

TabelaResultados
  ├─ Colunas: #, Circuito, Tipo, IB, C1, C2, C6, C5(QT), C3(CC), C4(SEC), S fase, S neutro, S PE, Iz corr., In, Status
  ├─ Critério decisivo: **negrito** + cor + **rótulo** ("Críte decisivo: C1")
  ├─ Filtros, ordenação, agrupamento
  ├─ Edição em lote (próxima story)
  └─ Exportação (PDF, CSV, SVG unifilar)

PainelDetalhe
  ├─ Cadeia de cálculo completa
  ├─ Area expansível: "Como este resultado foi obtido"
  └─ Renderizado exclusivamente de objeto rastreio (sem recomputação)
```

### Tarefas

1. [ ] Implementar 8 seções de jornada (wizard flow)
2. [ ] Tabela com 16 colunas, critério decisivo destacado + rótulo
3. [ ] Painel de detalhe (rastreio renderizado)
4. [ ] WCAG AA: contraste, navegação teclado, foco visível, leitor de tela
5. [ ] Testes de acessibilidade (`@testing-library/jest-axe` ou similar)

### Bloqueadores

- Nenhum novo

---

## File List

**Created/Modified:**
- `src/ui/componentes/DimensionadorWorkspace.tsx`
- `src/ui/componentes/TabelaResultados.tsx`
- `src/ui/componentes/PainelDetalhe.tsx`
- `tests/ui/DimensionadorWorkspace.test.tsx`
- `tests/ui/acessibilidade.test.tsx`

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity XL adicionada; Status Draft → Ready
