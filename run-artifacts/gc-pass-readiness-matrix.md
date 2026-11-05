# Matriz de prontidão para GC=PASS

| ID | Requisito | Estado | Evidência atual | Ação necessária | Autorização necessária |
|---|---|---|---|---|---|
| GC-01 | Recuperação independente do destino | PENDING_EXTERNAL_AUTHORIZATION | C20 rollback pré-commit e C15 sintético | executar e comprovar recuperação operacional | nova decisão operacional |
| GC-02 | A03/A04/B04/C03 no destino | TECHNICALLY_PENDING | migrations e PG17 descartável | aplicar, readback e reconciliação | autorização de DDL remoto |
| GC-03 | Auth real A/B | PENDING_EXTERNAL_AUTHORIZATION | testes `SYNTHETIC_ONLY` | testar duas contas, sessão e RLS real | autorização para teste Auth remoto |
| GC-04 | Fontes e cálculo elétrico | PENDING_PROFESSIONAL_ACCEPTANCE | contratos fail-closed C22 | fornecer/validar fontes e casos reais | disponibilidade de fontes e revisão técnica |
| GC-05 | C13 | PENDING_PROFESSIONAL_ACCEPTANCE | modelo C13 sem assinatura | revisão e aceite autêntico | profissional habilitado |
| GC-06 | CI final | READY | workflows C20 anteriores PASS | executar cinco workflows no SHA final | publicação da branch |
| GC-07 | Legado | DEFERRED | C19 | nenhuma ação nesta entrega | somente se escopo futuro mudar |

Esta matriz não autoriza operações remotas nem altera `GC=BLOCKED`.
