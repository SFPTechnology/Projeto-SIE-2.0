# Story SIE-AUTO-002 — Validar gates de qualidade AIOX na integração contínua

**Status inicial:** READY. **Prioridade:** P1.
**Justificativa:** `AGENTS.md` e `.aiox-core/constitution.md` exigem `npm run lint`, `npm run typecheck`, `npm test` e `npm run build`. O workflow `SIE modular API` verifica apenas pytest e sintaxe do frontend. Os gates AIOX da raiz não foram comprovados nesta branch.

## Fonte e escopo
- `AGENTS.md` (Quality Gates)
- `.aiox-core/constitution.md` (Quality First)
- `package.json` e `scripts/validate-sdc-auto-1.js`
- `.aiox-core/package.json` e seu `package-lock.json` (dependências internas necessárias)

## Acceptance criteria
- [ ] AC-01: workflow próprio executa `npm ci --prefix .aiox-core` a partir do lock do projeto em runner Linux limpo.
- [ ] AC-02: `npm run lint` efetivamente executa e informa resultado.
- [ ] AC-03: `npm run typecheck` efetivamente executa e informa resultado.
- [ ] AC-04: `npm test` efetivamente executa e informa resultado.
- [ ] AC-05: `npm run build` efetivamente executa e informa resultado.
- [ ] AC-06: um gate falho reprova o job; é proibido `continue-on-error` para simular sucesso.
- [ ] AC-07: logs e SHA do workflow são registrados na matriz do orquestrador e na story.
- [ ] AC-08: nenhum merge na `main` ou deploy de produção.

## Dependências e riscos
- CLI story SIE-AUTO-001: concluída no escopo de projeto local; independente do AIOX SDC, mas esta story estabelece governança transversal.
- Instalação isolada das dependências AIOX é necessária pois `.aiox-core/node_modules/` não integra o repositório.
- Caso um comando revele inconsistência preexistente, registrar bloqueio e corrigir causa-raiz, sem desabilitar gate.

## Plano
1. Criar GitHub Actions workflow dedicado.
2. Executar CI no head da branch.
3. Verificar todos os 4 comandos de qualidade no log.
4. Corrigir falhas comprovadas ou registrar bloqueio; atualizar status.

## File list
- [ ] `.github/workflows/sie-orchestrator-quality.yml`
- [ ] `docs/sie-orchestrator/VALIDATION_MATRIX.md`
- [ ] `docs/sie-orchestrator/EXECUTION_HISTORY.md`
- [ ] Esta story atualizada com evidências

## Evidências
A preencher ao final, após consultar log/execução real.
