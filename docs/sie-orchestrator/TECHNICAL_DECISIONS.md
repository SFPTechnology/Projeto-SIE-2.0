# TECHNICAL_DECISIONS — registro ADR simplificado

## ADR-SIE-001 — Desenvolvimento isolado
**Decisão:** prosseguir na branch `refactor/sie-2-foundation-2026-10-14` e PR #1 draft. **Razão:** `main` deve preservar código anterior durante reconstrução. **Reversão:** PR não mesclado.

## ADR-SIE-002 — Normativo é gate independente
**Decisão:** o servidor não aceita flags de usuário como aprovação. **Razão:** evita falsa conformidade. **Condição futura:** evidências versionadas, identidade autorizada e testes independentes.

## ADR-SIE-003 — SQLite local antes de PostgreSQL
**Decisão:** persistência de desenvolvimento via `RepositorioProjetos`; API opt-in protegida por token, sem vínculo a contas de produção. **Razão:** testes isolados com migração futura rastreável. **Risco:** token compartilhado não implementa autorização multiusuário.

## ADR-SIE-004 — CLI First
**Decisão:** publicar CLI operacional para funções de domínio já implementadas antes de expandir UI. **Base:** `.aiox-core/constitution.md`. **Teste:** CLI sem servidor web, importando repositório existente.

## ADR-SIE-005 — Sem mocks normativos como fonte
**Decisão:** fórmulas resistivas e tabelas demonstrativas permanecem apenas para exploração/testes, sem sinal de conformidade. **Razão:** rastreabilidade e engenharia responsável.

## ADR-SIE-006 — Autoridade e autonomia
**Decisão:** ações rotineiras autorizadas na branch são executadas via conector GitHub; sem merge ou alteração de produção. Os papéis AIOX são critérios de governança, não comprovação de que agentes independentes efetivamente revisaram a tarefa.

## ADR-SIE-007 — Gates AIOX executados na CI
**Decisão:** workflow GitHub Actions separado executa os quatro comandos exigidos na raiz, após instalar dependências da `.aiox-core` pelo lockfile. **Justificativa:** o pipeline FastAPI não comprova os gates do AIOX. **Evidência:** run 38572622950; sem `continue-on-error`.

## ADR-SIE-008 — Complementar AIOX sem executor duplicado
**Decisão:** `sie_api/scheduler.py` realiza DAG/estado/fila e `scheduler_cli.py` opera JSON local; os existentes `MasterOrchestrator`, `RecoveryHandler` e `SessionState` conservam a responsabilidade de execução e retomada dos agentes. **Risco residual:** ainda não existe bridge de execução automática entre fila e agentes. **Evidência:** run 38574851595.

## ADR-SIE-009 — Chromium E2E como gate independente
**Decisão:** manter suite Playwright em `restructuring/e2e/` fora da coleta padrão de testes unitários. GitHub Actions instala Chromium, inicia FastAPI, servidor web e SQLite temporário e executa testes ponta a ponta. **Razão:** testes estáticos e TestClient não comprovam comportamento real do navegador. **Evidência:** 38612351246, 3 passed; regressão API 38612351333, 90 passed. **Limites:** local, não equivale à homologação profissional ou produção.

## ADR-SIE-010 — Inventário de fontes não implica conformidade normativa
**Decisão:** usar CLI offline para SHA256 de artefatos referenciados e emitir somente metadados com `normative_conformity_verified=false`. Nenhum documento é copiado para o artefato. **Razão:** auditoria de integridade não substitui comparação de células, cláusulas e casos de referência independentes. **Evidência:** run 38613344311 (99 pytest, 6/6 artefatos, artifact 11917953248). **Limite:** NOR-01 e SIE-AUTO-003 continuam BLOCKED.

## ADR-SIE-011 — Fonte canônica de tarefas e reconciliação de dependências
**Decisão:** o estado JSON governa as transições; os arquivos de fila/grafo são documentação derivada. Atividades 003/010 existentes na fila foram reconciliadas no JSON; NOR-01 depende da normalização 003. Alteração de dependência não é transição de estado e não deve ser registrada como tal. **Razão:** evita sucesso simulado e preserva um grafo acíclico consistente.
