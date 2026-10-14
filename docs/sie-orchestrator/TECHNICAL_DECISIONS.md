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
