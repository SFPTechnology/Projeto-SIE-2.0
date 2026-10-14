# Story DC-10: Qualidade Final e Acessibilidade

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-10  
**Status:** Ready  
**Priority:** CRITICAL (quality gate final)  
**Complexity:** L (suite ~200 testes + WCAG AA + checklist §30)  
**Dependency:** DC-1 a DC-9  
**Assignee:** @qa (Quinn) / @dev (Dex)

---

## Story

Como equipe de QA, preciso executar suite completa de testes (unitários, integração, fronteira, propriedades, regressão), validar WCAG AA em 100% da UI, e confirmar checklist de entrega §30, para que o módulo seja liberado com confiança de que nenhum critério normativo foi violado.

---

## Acceptance Criteria

### AC-DC-01 a AC-DC-25 verdes (traçam para CA-DC-01..25 do PRD)

- [ ] **AC-DC-01 a AC-DC-25:** 100% dos critérios de aceite passando (ou explicitamente marcados como `xfail` com justificativa)

**Verificação:** CI/CD executa suite completa; todos os gates passam antes de deploy.

---

## Dev Notes

### Suite de testes

```
tests/
├─ unit/
│  ├─ domain/validacao/
│  ├─ domain/dimensionamento/
│  ├─ domain/repositorio/
│  └─ servicos/
│
├─ integration/
│  ├─ api.test.ts
│  ├─ maquina_estados.test.ts
│  └─ downstream.test.ts
│
├─ frontend/
│  ├─ componentes/
│  └─ acessibilidade/
│
├─ performance/
│  └─ benchmark_lote_44.test.ts
│
├─ regressao/
│  ├─ tabela_36_amostra.sql
│  ├─ exemplos_numericos.ts
│  └─ nomenclatura_1997.sh
│
└─ e2e/
   └─ jornada_completa.test.ts
```

### Checklist de entrega (§30 PRD)

- [ ] Testes unitários: 85%+ cobertura no domínio
- [ ] Testes de integração: API + máquina de estados
- [ ] Testes de fronteira: guardas de entrada
- [ ] Testes de propriedade: invariantes de cálculo
- [ ] Testes de regressão: Tabela 36 amostra, exemplos numéricos
- [ ] WCAG AA: contraste, teclado, foco, leitor
- [ ] Nomenclatura 1997: zero referências (lint)
- [ ] Performance: lote 44 < 2 s
- [ ] Documentação: README, OpenAPI, referências normativas
- [ ] CodeRabbit: CRITICAL issues = 0 antes de merge

### Tarefas

1. [ ] Implementar suite completa de testes (~200+ testes)
2. [ ] Teste de acessibilidade (WCAG AA)
3. [ ] Benchmark de performance
4. [ ] Teste de regressão (Tabela 36 + exemplos numéricos)
5. [ ] Lint anti-nomenclatura-1997
6. [ ] Documentação final
7. [ ] CodeRabbit review (pré-merge)

### Bloqueadores

- Nenhum novo

---

## File List

**Created/Modified:**
- `tests/` (arquivos listados acima)
- `docs/API.md` (referência OpenAPI/tRPC)
- `docs/DEVELOPMENT.md` (guia de desenvolvimento)
- `README.md` (atualizado com MOD-DC v3.0)

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity L adicionada; nomenclatura AC-DC normalizada; Status Draft → Ready
