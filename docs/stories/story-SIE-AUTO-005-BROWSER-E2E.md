# Story SIE-AUTO-005 — Fluxo ponta a ponta real em navegador

**Estado:** READY. **Prioridade:** P2. **Dependência:** SIE-AUTO-011 (DONE).
**Origem:** protocolo SIE-AUTO-ORCHESTRATOR v2.0; `docs/sie-orchestrator/EXECUTION_QUEUE.md`; implementação de API, UI e SQLite local.

## Objetivo
Provar, com Chromium real e servidor local isolado, que a jornada atual funciona: saúde da API, cálculo demonstrativo, bloqueio normativo, salvar, reabrir, revisão e recuperação de conflitos. Sem deploy.

## Critérios de aceite
- [ ] AC-01: CI executa Chromium real, não apenas mocks/TestClient.
- [ ] AC-02: interface acessa API, executa análise com aviso normativo, sem lançar erros JavaScript.
- [ ] AC-03: salvar e recuperar dados via SQLite por token local, sem gravar credencial no navegador.
- [ ] AC-04: conflito de revisão ou token inválido é exibido ao usuário sem perda silenciosa de dados.
- [ ] AC-05: uma análise reaberta exige execução de novo cálculo; não é considerada automaticamente aprovada.
- [ ] AC-06: logs do teste, instruções e limitações documentados; checks de regressão e AIOX aprovados.

## Arquivos previstos
- `restructuring/apps/api/tests/e2e/test_browser_flow.py`
- `restructuring/apps/api/pyproject.toml` (grupo opcional e2e)
- `.github/workflows/sie-e2e-browser.yml`
- `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`
- `docs/sie-orchestrator/NEXT_ACTION.md`

## Política
Executar somente em localhost, com SQLite temporário e token efêmero de teste. A UI não concede conformidade e a ação não altera main, produção ou Supabase.
