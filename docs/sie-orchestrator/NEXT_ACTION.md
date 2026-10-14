# NEXT_ACTION — ponto de retomada segura

**Estado validado:** SIE-AUTO-004 e SIE-AUTO-005 DONE em seus escopos locais, conforme CI no commit funcional `f2642e3041b16ec0ddbf43e59b8e482f345d39d0`. SIE-AUTO-003 (normalização normativa) e NOR-01 permanecem BLOCKED. SIE-AUTO-006 exige identidade/ambiente de produção autorizado (HUMAN_REQUIRED).

## Evidência recente

- Python/API: GitHub Actions **38612351333** — 90 pytest passed, JS syntax check.
- Chromium E2E: **38612351246** — 3 passed.
- Gates AIOX: **38612351441** — lint/typecheck/test/build success.
- Inventário documental: **38613344311** — 99 pytest passed; 6/6 artefatos presentes, SHA-256 no artifact **11917953248**, sem conferir norma.

## Primeira ação após retomada

1. Consultar branch e head do PR #1 e reconciliar o JSON com commits e checks atuais.
2. Validar `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` via `python -m sie_api.scheduler_cli` ou teste correspondente.
3. Consultar o artefato do manifesto de fonte; comparar dados/rótulos de origem com normas autorizadas e tabelas efetivamente consumidas pelos motores.
4. Para NOR-01, conferir legitimidade, edição, aplicabilidade e células com referências primárias; preparar cenários independentes com engenheiro responsável, sem inventar valores.
5. Prosseguir automaticamente em qualquer nova tarefa READY validada. Caso só restem bloqueios externos, registrar as dependências e encerrar legitimamente a sessão, sem simular execução contínua.
6. Manter `main` preservada; não executar deploy ou merge, e manter a aprovação normativa fechada.

## Condição para desbloquear atividades

- SIE-AUTO-007 depende de NOR-01 e SIE-AUTO-004 (este já DONE).
- SIE-AUTO-008 depende de SIE-AUTO-007 e SIE-AUTO-006.
- SIE-AUTO-009 depende de SIE-AUTO-005 (DONE) e SIE-AUTO-008.
- SIE-AUTO-010 depende dos gates anteriores.
