# VALIDATION_MATRIX — critérios, evidências e gaps

| ID | Critério | Evidência observável | Resultado |
|---|---|---|---|
| BASE-01 | GitHub branch separada de main | PR #1 aberto, draft, não merged, base main | DONE |
| BASE-02 | CI do protótipo | Run 38562529663, pytest 42 passed / 1 warning, JS check success | DONE no escopo automatizado |
| SEC-01 | Cliente não autoaprova norma | `domain/gates.py`, `tests/test_api.py` e `tests/test_domain.py` | DONE — prevenção, não aprovação |
| EDP-01 | Seleção apenas candidata | `domain/edp.py` e `tests/test_edp.py` | DONE — bloqueio de liberação |
| DATA-01 | Revisão de SQLite e auditoria | `storage.py`, `tests/test_storage.py`, `tests/test_storage_api.py` | DONE — testes existentes |
| CLI-01 | CLI completa sem UI | `sie_api/cli.py` e `tests/test_cli.py`, run 38572009186 (51 passed) | DONE |
| NOR-01 | Valores de fonte primária e casos independentes | Documentação parcial do legado, engine genérico | BLOCKED |
| ENG-01 | Motor completo para uso profissional | Sem evidências suficientes de todos os critérios | BLOCKED |
| WEB-01 | QA ponta a ponta em navegador | `test_web_contract.py` é estático, sem browser | PENDING |
| PROD-01 | Autenticação/isolamento multiusuário | Token local de teste; sem autorização granular | PENDING |

Nenhuma linha prova teste normativo profissional sem fonte primária, edição, referência, cenário e resultado independente. Ao concluir story, acrescentar run ID e SHA da revisão exata.

| ROOT-01 | AIOX lint/typecheck/test/build | `.github/workflows/sie-orchestrator-quality.yml`, run 38572622950 todos os 4 steps success | DONE |
