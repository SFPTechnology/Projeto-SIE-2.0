# Story SIE-F11 — QA integrado e homologação técnica

Status: Ready for Review (checkpoint BLOCKED; critérios não concluídos). Base: F10 `540f2c8e7e61a1efb6bf71abcedc8768d7086914` na branch `feat/f09-concessionarias-especializadas`; F11 em `feat/f11-qa-integrado`.

Fonte: `F11_EXECUTAR.md` fornecido pelo responsável nesta execução, tasks 11.01–11.10. Escopo: evidências de software e decisão de release; aprovação profissional, ensaio em campo e produção são gates distintos.

## Critérios de aceite

- [ ] AC-11.01: candidato reproduzível com SHA, versões, dependências e dados de teste.
- [ ] AC-11.02: QA matemático verifica grandezas, limites, arredondamento e erros seguros.
- [ ] AC-11.03: matriz por motor explicita fontes, aplicabilidade e pendências normativas.
- [ ] AC-11.04: testes integrados de cargas até documentos preservam revisão e invalidam saídas obsoletas.
- [ ] AC-11.05: navegador real verifica jornada, mobile, teclado, persistência e impressão no escopo aplicável.
- [ ] AC-11.06: segurança de acesso, importação, logs e recuperação possui testes negativos.
- [ ] AC-11.07: concorrência, erro e desempenho têm SLO e medição observada.
- [ ] AC-11.08: documentos e unidades conciliam com snapshot e pendências.
- [ ] AC-11.09: checklist de inspeção/ensaios de campo separa software e execução física.
- [ ] AC-11.10: parecer por gate, QA-01/02/03, riscos, decisão de release e CI no SHA final.

## File List

- `docs/stories/story-SIE-F11-QA-INTEGRADO.md`
- `docs/implantacao-sie-2-0/F11/` (matriz, QA, candidato e relatórios)
- `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` (estado canônico)
- `docs/sie-orchestrator/NEXT_ACTION.md`
- `restructuring/apps/api/tests/test_f11_integrated_revision.py`
- `restructuring/apps/api/tests/test_f11_security_recovery.py`
- `.github/workflows/sie-restructuring-api.yml`, `sie-e2e-browser.yml`, `sie-orchestrator-quality.yml` (gatilhos F11)
