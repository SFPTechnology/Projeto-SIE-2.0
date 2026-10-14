# NEXT_ACTION — retomada segura

**Últimas stories concluídas:** SIE-AUTO-001 (CLI projetos) e SIE-AUTO-002 (gates raiz). Evidências: runs 38572009186 e 38572622950, ambas success, conforme seus respectivos escopos.

**Próxima atividade:** SIE-AUTO-011 — máquina de estados e escalonador determinístico de dependências, derivado diretamente do protocolo SIE-AUTO-ORCHESTRATOR v2.0 do usuário.

## Etapas para retomar
1. Verificar o head da branch `refactor/sie-2-foundation-2026-10-14`, PR #1 e os checks da última revisão.
2. Criar story em `docs/stories/` com ACs antes de editar código.
3. Implementar somente motor determinístico de grafo, estados, fila e histórico; nenhuma execução remota implícita nem aprovação normativa.
4. Executar pytest e os quatro gates AIOX; corrigir falhas reais.
5. Registrar SHA, run IDs e status em PROJECT_STATE, VALIDATION_MATRIX, EXECUTION_HISTORY e NEXT_ACTION.
6. Continuar com tarefa READY sem violar dependências.

**Bloqueios independentes:** NOR-01/NOR-02 (fontes e validação normativa), autenticação de produção, E2E real e demais módulos de engenharia. Não mesclar `main` sem validações correspondentes.
