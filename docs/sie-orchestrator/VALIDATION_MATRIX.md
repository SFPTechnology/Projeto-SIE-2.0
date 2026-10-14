# VALIDATION_MATRIX — aceitação por evidência

| Critério | Status | Evidência reproduzível | Limites |
|---|---|---|---|
| BASE-01 — isolamento do desenvolvimento | DONE | PR #1 aberto/draft, base main | Nenhum merge; branch de reestruturação separada |
| SIE-AUTO-001 — CLI de projetos | DONE | 38572009186, testes CLI | SQLite local, sem auth de produção |
| SIE-AUTO-002 — quality gates AIOX | DONE | 38572622950, lint/typecheck/test/build | Regras do repositório, não critérios normativos |
| SIE-AUTO-011 — DAG e máquina de estados | DONE | 38574851595 (67 pytest), 38574851619 (AIOX) | Escalonador, não executor permanente |
| SIE-AUTO-004 — contratos de engenharia | DONE | 38612351333: 90 pytest + JS; 38612351441: AIOX | Testes de fórmulas/limites; nenhuma aprovação ABNT |
| SIE-AUTO-005 — fluxo E2E Chromium | DONE | 38612351246: 3 Chromium E2E tests passed | Cobertura local, não multiusuário ou produção |
| SEG-01 — cliente não libera norma | DONE | `domain/gates.py` e testes API/domínio | Gate permanece PENDENTE/BLOQUEADO |
| EDP-01 — seleção só candidata | DONE como bloqueio | `domain/edp.py`, `tests/test_edp.py` | Não valida elegibilidade total da distribuidora |
| DATA-01 — revisão e SQLite | DONE no escopo local | `tests/test_storage.py`, `test_storage_api.py` | Sem banco de produção |
| PROV-01 — integridade de fontes | DONE no subescopo | 38613344311: 99 pytest; 6/6 artefatos, manifesto artifact 11917953248 | Hash não é validação de norma |
| SIE-AUTO-003 — conferir valores e origens | BLOCKED | `NORMATIVE-SOURCES-RECOVERY.md` + manifesto SHA256 | Fonte primária/edição/valores ainda não auditados |
| NOR-01 — catálogo normativo confiável | BLOCKED | Inventário local apenas | Exige casos independentes e revisão de tabelas |
| SIE-AUTO-006 — identidade e migração | HUMAN_REQUIRED | Token opcional local | Sem autorização multiusuário, sem deploy |
| SIE-AUTO-007 — motores completos | PENDING | Sem regressão normativa integral | Depende de NOR-01 e story 004 |
| SIE-AUTO-008 — memoriais/diagramas | PENDING | Sem teste de consistência | Depende de 006 e 007 |
| SIE-AUTO-009 — QA final/documentação | PENDING | Manuais parciais apenas | Depende de E2E e 008 |
| SIE-AUTO-010 — liberação final | PENDING | Não há parecer profissional final | Depende dos anteriores |

## Regras de leitura

- SUCCESS de um workflow comprova os testes configurados e somente o código daquela revisão.
- Documento presente não significa tabela validada; artefato hash é uma identificação reproduzível, sem comprovação de fonte oficial ou vigência.
- Cálculo de engenharia não deve ser liberado por checkbox, flags do cliente ou simples status de workflow.
- Em caso de mudança do head, conferir se os gates da revisão mais recente continuam verdes antes de qualquer nova promoção de estado.
