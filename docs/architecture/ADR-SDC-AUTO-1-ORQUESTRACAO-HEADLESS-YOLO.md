# ADR SDC-AUTO-1: Orquestracao headless YOLO do SDC

Date: 2026-07-27
Status: Accepted
Story: SDC-AUTO-1

## Context

O workflow canonico `story-development-cycle.yaml` era guiado/step-by-step e o engine existente em `run-workflow-engine.md` processa uma action por invocacao. O contrato `WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md` exige execucao sem prompts apos manifesto valido, loops deterministicos, estado persistido, DevOps/deploy, rollback e idempotencia.

## Decision

Implementar o modo headless como extensao separada:

- workflow executavel: `.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`;
- runtime deterministico: `.aiox-core/core/orchestration/sdc-headless-yolo-runner.js`;
- wrapper CLI: `.aiox-core/development/scripts/sdc-headless-yolo.js`.

O workflow canonico `story-development-cycle.yaml` passa a declarar a Fase 5 de DevOps Publication e aponta para a extensao headless, mas o comportamento guided/engine step-by-step permanece isolado.

## Rationale

Essa abordagem reduz regressao nos modos existentes. O runner headless trata o manifesto como snapshot imutavel com fingerprint SHA-256, persiste estado a cada transicao em `.aiox/sdc-headless/`, grava log redigido em `docs/workflows/logs/`, e permite adapters simulados para testar push, PR, merge, release, deploy, rollback e migrations sem acionar remote real.

## Consequences

- Operacoes remotas sao bloqueadas por flags independentes e sempre registradas como autoridade `@devops`.
- Resume nao repete efeitos externos ja concluidos.
- Migrations autorizadas exigem evidencia `apply -> rollback -> reapply`; migrations destrutivas tambem exigem backup e flag especifica.
- O gate arquitetural aprovou a direcao apos os fixes de execucao real do CLI e sincronizacao do workflow canonico.

## Architecture Gate Review

Reviewer: Aria (`@architect`)
Date: 2026-07-27
Verdict: PASS
Readiness: High

### Accepted Decisions

- A extensao headless separada preserva o contrato guided/engine step-by-step e reduz risco de regressao.
- O manifesto imutavel com fingerprint, persistencia por transicao e resume idempotente atende ao eixo arquitetural do contrato.
- A fronteira de autoridade `@devops` esta modelada por operacoes remotas independentes e flags explicitos.
- Migrations, rollback e deploy foram tratados como efeitos externos simulaveis, sem execucao remota direta pelo `@dev`.

### Resolved Concerns

1. O wrapper CLI agora bloqueia execucao sem `--dry-run` quando `--adapter-module` nao foi fornecido.
   - Evidence: `testCliRequiresDryRunOrAdapterModule`.
   - Evidence: `node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest missing.yaml` retorna exit non-zero com `Refusing non-dry-run execution without --adapter-module`.

2. O `--adapter-module` real tambem precisa exportar `devops` como funcao, evitando queda silenciosa para adapters default.
   - Evidence: `testCliAdapterModuleRequiresDevopsFunction`.

3. O fluxo canonico `story-development-cycle.yaml` foi sincronizado para incluir DevOps Publication no `flow_diagram` e nos `handoff_prompts`.
   - Evidence: `WorkflowValidator.validate()` em `story-development-cycle.yaml` e `story-development-cycle-headless-yolo.yaml` com 0 errors e 0 warnings.

### Final Gate Evidence

- `node .aiox-core/development/scripts/__tests__/sdc-headless-yolo.test.js` — PASS.
- `WorkflowValidator.validate()` em `story-development-cycle.yaml` e `story-development-cycle-headless-yolo.yaml` — VALID, 0 errors, 0 warnings.
- `node -c` em `sdc-headless-yolo-runner.js`, `sdc-headless-yolo.js` e `sdc-headless-yolo.test.js` — PASS.
- CLI negativo sem `--dry-run`/`--adapter-module` — PASS esperado por bloqueio.

### Non-Blocking Notes

- A ausencia de `package.json` no root impede os gates npm globais do AGENTS; isso e um problema de estrutura do repo, nao desta decisao arquitetural.
- CodeRabbit nao foi verificado nesta sessao por indisponibilidade/timeout de WSL; QA deve repetir quando o ambiente estiver disponivel.
