# Story SIE-AUTO-005 — Fluxo ponta a ponta real em navegador

**Estado:** DONE (escopo local demonstrativo). **Prioridade:** P2. **Dependência:** SIE-AUTO-011 (DONE).

## Critérios de aceite
- [x] AC-01: navegador Chromium real executado em GitHub Actions.
- [x] AC-02: interface acessa API FastAPI e mostra status normativo PENDENTE.
- [x] AC-03: salvar e recuperar projeto por SQLite e token temporários, sem persistir token no navegador.
- [x] AC-04: erro de token e conflito de revisão são exibidos na interface.
- [x] AC-05: recuperação de projeto exige novo cálculo; não reaproveita liberação anterior.
- [x] AC-06: guia e evidências de CI publicados.

## Evidências confirmadas
- SHA funcional aferido: `f2642e3041b16ec0ddbf43e59b8e482f345d39d0`.
- Chromium run **38612351246**: **3 passed**.
- API run **38612351333**: **90 passed, 1 warning** e JavaScript syntax check.
- AIOX run **38612351441**: lint, typecheck, test, build aprovados.
- Guia de execução: `restructuring/docs/TESTE-E2E-NAVEGADOR.md`.

## File List
- [x] `restructuring/e2e/test_browser_flow.py`
- [x] `restructuring/apps/api/pyproject.toml`
- [x] `restructuring/apps/api/sie_api/main.py` (CORS local)
- [x] `restructuring/apps/web/app.js` (erros e conflitos)
- [x] `.github/workflows/sie-e2e-browser.yml`
- [x] `restructuring/docs/TESTE-E2E-NAVEGADOR.md`
- [x] `docs/stories/story-SIE-AUTO-005-BROWSER-E2E.md`

## Limites
Sucesso em teste de navegador controlado não comprova conformidade NBR 5410/EDP, acesso multiusuário, implantação de produção ou todos os navegadores. PR permanece em draft, `main` inalterada.
