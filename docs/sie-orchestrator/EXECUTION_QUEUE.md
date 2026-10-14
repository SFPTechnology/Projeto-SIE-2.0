# EXECUTION_QUEUE — fila dinâmica

Regra: READY somente com dependências comprovadas; DONE somente quando todos os ACs possuírem evidência.

| Ordem | ID | Atividade | Depende de | Prioridade | Estado | Critério de saída |
|---|---|---|---|---|---|---|
| 1 | SIE-AUTO-001 | Implementar CLI de projetos locais | SQLite e testes existentes | P1 | DONE | CLI + testes + documentação + CI |
| 2 | SIE-AUTO-002 | Adicionar verificações de conformidade às stories/CI | Story e estrutura AIOX | P1 | DONE | Detectar violações de qualidade sem suprimir erros |
| 3 | SIE-AUTO-003 | Normalizar evidências de tabelas e revisar origem do catálogo EDP | Pesquisa e documentos fonte | P1 | BLOCKED | Fonte primária, revisão e casos independentes |
| 4 | SIE-AUTO-004 | Reforçar contratos do núcleo elétrico e limites dos modelos | Motor atual, requisitos e SIE-AUTO-011 | P1 | READY | Testes de borda e falha segura |
| 5 | SIE-AUTO-005 | Teste E2E de API, UI, SQLite e recuperação | API/CLI/UI e SIE-AUTO-011 | P2 | READY | Fluxo reproduzido por navegador real |
| 6 | SIE-AUTO-006 | Projeto de identidade, permissões e migração para PostgreSQL | Modelos e credenciais de ambiente autorizado | P1 | PENDING | Isolamento de usuários e rollback |
| 7 | SIE-AUTO-007 | Expandir motor conforme NBR 5410 (proteção, impedância, etc.) | NOR-01 e testes independentes | P1 | BLOCKED | Casos de referência auditados |
| 8 | SIE-AUTO-008 | Integrar memoriais, diagrama e quantitativos | Domínio e cálculos aprovados | P2 | PENDING | Rastreabilidade total e regressão |
| 9 | SIE-AUTO-009 | Manuais finais, pacote local e revisão de UX/E2E | Funcionalidades consolidadas | P2 | PENDING | Documentos correspondem ao software testado |
| 10 | SIE-AUTO-010 | Liberação controlada e PR para revisão | Gates anteriores | P1 | PENDING | Evidências completas, análise independente, decisão de merge |

As linhas representam apenas tarefas fundamentadas no repositório e nas instruções do usuário. Cada execução deve validar a árvore real e os checks antes de alterar estado.

| 11 | SIE-AUTO-011 | Escalonador de estados e grafo | Stories 001, 002 | P1 | DONE | 67 pytest + gates AIOX, runs 38574851595 / 38574851619 |

Após validar 011: **SIE-AUTO-004 e SIE-AUTO-005 estão READY**; NOR-01 segue BLOCKED. O orquestrador de tarefas não substitui o executor AIOX.
