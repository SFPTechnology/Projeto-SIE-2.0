# Story SIE-AUTO-004 — Contratos de engenharia e limites

**Estado:** RUNNING. **Prioridade:** P1. **Dependência:** SIE-AUTO-011 (DONE).
**Origem:** protocolo SIE-AUTO-ORCHESTRATOR v2.0, `docs/sie-orchestrator/NEXT_ACTION.md`, motores existentes.

## Objetivo
Reforçar validações determinísticas e limites explícitos dos motores elétricos demonstrativos, sem afirmar conformidade com NBR 5410 ou EDP.

## Critérios de aceite
- [ ] AC-01: entradas e itens de catálogo não finitos, nulos ou negativos falham de modo seguro.
- [ ] AC-02: catálogo de disjuntores é validado integralmente antes da seleção.
- [ ] AC-03: comprimento zero representa queda de tensão nula, sem permitir demais entradas inválidas.
- [ ] AC-04: testes independentes cobrem casos de borda e regressões.
- [ ] AC-05: documentação informa hipóteses, limitações e interfaces.
- [ ] AC-06: pytest, JavaScript e gates AIOX passam no head final.

## Escopo e arquivos
- `restructuring/apps/api/sie_api/domain/engines.py`
- `restructuring/apps/api/tests/test_engines.py`
- `restructuring/docs/MARCO-002-RELATORIO.md`
- Este arquivo e os registros do orquestrador.

## Limites
Sem alteração de coeficientes normativos, tabelas EDP ou aprovação de projeto. A aprovação de AC depende de CI verificável.
