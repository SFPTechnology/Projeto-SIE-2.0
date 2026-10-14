# Story SIE-AUTO-004 — Contratos de engenharia e limites

**Estado:** DONE (escopo dos contratos determinísticos, não aprovação normativa). **Prioridade:** P1. **Dependência:** SIE-AUTO-011 (DONE).

## Objetivo
Reforçar validações determinísticas e limites dos motores elétricos demonstrativos sem afirmar conformidade com NBR 5410 ou EDP.

## Critérios de aceite — verificados

- [x] AC-01: números não finitos, inválidos, ausentes e negativos são rejeitados no domínio.
- [x] AC-02: disjuntores de catálogo são validados integralmente antes da seleção; tabelas duplicadas/vazias também falham de modo seguro.
- [x] AC-03: comprimento zero retorna ΔV=0 nas duas modalidades resistivas; negativos e não finitos continuam inválidos.
- [x] AC-04: testes de borda, domínio e contrato HTTP estão executados em CI.
- [x] AC-05: hipóteses, unidades, limites, resultados e avisos constam de `restructuring/docs/CONTRATOS-ENGENHARIA.md`.
- [x] AC-06: na revisão `f2642e3041b16ec0ddbf43e59b8e482f345d39d0`, API/pytest (run 38612351333, **90 passed, 1 warning**, inclusive sintaxe JS) e AIOX (run 38612351441, lint/typecheck/test/build) tiveram conclusão SUCCESS.

## File List conferida

- [x] `restructuring/apps/api/sie_api/domain/engines.py`
- [x] `restructuring/apps/api/sie_api/main.py` (contrato comprimento não negativo)
- [x] `restructuring/apps/web/index.html` (entrada consistente)
- [x] `restructuring/apps/api/tests/test_engines.py`
- [x] `restructuring/apps/api/tests/test_api.py`
- [x] `restructuring/docs/CONTRATOS-ENGENHARIA.md`
- [x] `docs/stories/story-SIE-AUTO-004-ENGINE-CONTRACTS.md`
- [x] `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` (rastreabilidade de status)

## Bloqueios fora do escopo desta story

- NOR-01 exige verificação das fontes normativas e tabelas primárias.
- Proteção completa, reatância, curto-circuito e equivalência normativa continuam pendentes.
- O código não concede aprovação profissional nem altera main.
