# Workflow SDC Automatico YOLO - MOD-QT Integral Permanente

**Status:** Ready for Dry-Run Execution  
**Modo:** SDC headless YOLO, sem prompts durante a execucao  
**Fonte executiva:** `docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md`  
**Manifesto:** `docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml`  
**Story alvo:** `docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md`  
**Autoridade:** SM -> PO -> Dev -> QA -> DevOps  

## 1. Objetivo

Executar automaticamente o ciclo SDC completo para transformar o workflow MOD-QT integral permanente em entrega rastreavel:

```text
@sm cria/refina story
  -> @po valida story
    -> @dev implementa em YOLO
      -> @qa revisa e emite gate
        -> @dev corrige se necessario
          -> @qa aprova
            -> @devops executa pre-push simulado ou real autorizado
```

O workflow cobre todos os processos e fases descritos em `WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md`, incluindo handoffs persistidos para `@qa` e `@devops`.

## 2. Regra de seguranca

Este workflow tem dois perfis:

1. **Dry-run completo:** percorre todas as fases, incluindo DevOps, com efeitos remotos simulados pelo runner.
2. **Execucao real local:** implementa e valida localmente, mas bloqueia antes de `git push`, PR, merge, release ou deploy se nao houver autorizacao explicita e adapter DevOps real.

Nenhum agente alem de `@devops` pode executar operacoes remotas. Mesmo em YOLO, push/PR/deploy reais exigem manifestos e adapters autorizados.

## 3. Entradas obrigatorias

```yaml
source_artifact: docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md
story_file: docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md
story_id: MOD-QT-3-01
execution_mode: yolo
interaction_policy: never_prompt
on_missing_input: block_and_log
base_branch: master
target_branch: feature/mod-qt-integral-permanente
remote_repository: https://github.com/SFPTechnology/Projeto-SIE.git
deploy_runbook: docs/workflows/PLANO-DEPLOY-COMPLETO-2026-07-18.md
```

## 4. Estados

```text
MANIFEST_VALIDATION
  -> SM_STORY_CREATION
  -> PO_STORY_VALIDATION
  -> DEV_IMPLEMENTATION
  -> DEV_LOCAL_GATES
  -> DEV_HANDOFF_QA
  -> QA_REVIEW
  -> QA_GATE
  -> QA_HANDOFF_DEVOPS
  -> DEVOPS_PRE_PUSH
  -> DEVOPS_PUBLICATION_OR_BLOCK
  -> COMPLETE | BLOCKED | FAILED | ROLLED_BACK
```

## 5. Fase 0 - Manifest validation

Comando:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml --dry-run
```

Validacoes:

- `source_artifact` existe.
- `deploy_runbook` existe.
- `execution_mode = yolo`.
- `interaction_policy = never_prompt`.
- `on_missing_input = block_and_log`.
- `max_qa_iterations >= 1`.

Falha:

```text
HALT: MANIFEST_INVALID
```

## 6. Fase 1 - @sm story creation

Agente: `@sm`  
Comando logico:

```text
@sm *draft MOD-QT-3-01 --source docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md --mode yolo
```

Responsabilidades:

- Criar a story `story-MOD-QT-3-01-modulo-integral-permanente.md` se ela ainda nao existir.
- Derivar escopo somente do workflow fonte.
- Incluir AC1 a AC6 do workflow fonte.
- Declarar explicitamente IN/OUT.
- Incluir tarefas para navegacao, fallback SPA, build canonico, artefato de deploy, testes e validacoes.
- Criar handoff para `@po`.

Handoff esperado:

```yaml
path: .aiox/handoffs/MOD-QT-3-01-sm-to-po.yaml
from_agent: "@sm"
to_agent: "@po"
story: "MOD-QT-3-01"
last_command: "*draft"
status: "Draft"
source_artifact: "docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md"
next_command: "*validate-story-draft docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md"
```

## 7. Fase 2 - @po story validation

Agente: `@po`  
Comando logico:

```text
@po *validate-story-draft docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md --mode yolo
```

Gate:

- 10/10 checks de story.
- Sem requisito inventado.
- Sem mudanca normativa de MOD-QT.
- Sem autorizacao remota embutida na story.
- Story muda para `Ready`.

Se `NO-GO`, retornar a `@sm`. Limite: 3 iteracoes.

Handoff esperado:

```yaml
path: .aiox/handoffs/MOD-QT-3-01-po-to-dev.yaml
from_agent: "@po"
to_agent: "@dev"
story: "MOD-QT-3-01"
last_command: "*validate-story-draft"
status: "Ready"
next_command: "*develop-yolo story-MOD-QT-3-01-modulo-integral-permanente"
```

## 8. Fase 3 - @dev implementation

Agente: `@dev`  
Comando logico:

```text
@dev *develop-yolo story-MOD-QT-3-01-modulo-integral-permanente
```

@dev deve executar todas as fases do workflow fonte:

1. Preflight.
2. Confirmacao do estado atual do MOD-QT.
3. Exposicao permanente no produto.
4. Rota profunda e fallback SPA.
5. Build canonico e artefatos permanentes.
6. Testes obrigatorios.
7. Validacoes completas.
8. Teste local no navegador.
9. Story updates.

Arquivos esperados:

- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.gen.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.spa.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/AppShell.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/router.spa.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/vite.spa.config.ts`
- `sistema-de-instala-es-el-tricas-sie-main/package.json`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/`

@dev deve preservar alteracoes nao relacionadas.

## 9. Fase 4 - @dev local gates

Comandos obrigatorios:

```powershell
cd sistema-de-instala-es-el-tricas-sie-main
npm run lint
npm run typecheck
npm test
npm run build
npm run build:spa
rg "queda-tensao" dist
rg "Queda de tens" dist
```

Se houver artefato canonico Hostinger, validar:

```powershell
rg "queda-tensao" <artefato-canonico>
rg "Queda de tens" <artefato-canonico>
```

Falha no mesmo gate por 3 tentativas:

```text
HALT: DEV_GATE_REPEATED_FAILURE
```

## 10. Fase 5 - @dev handoff to @qa

Quando a story estiver `InReview`, criar:

```yaml
path: .aiox/handoffs/MOD-QT-3-01-dev-to-qa.yaml
from_agent: "@dev"
to_agent: "@qa"
story: "MOD-QT-3-01"
last_command: "*develop-yolo"
status: "InReview"
source_artifact: "docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md"
evidence:
  lint: "PASS|WAIVED_WITH_EVIDENCE"
  typecheck: "PASS"
  test: "PASS"
  build: "PASS"
  build_spa: "PASS"
  route_tree_ssr: "PASS"
  route_tree_spa: "PASS"
  deep_link_fallback: "PASS"
  artifact_contains_queda_tensao: "PASS"
next_command: "*review docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md"
```

## 11. Fase 6 - @qa review and gate

Agente: `@qa`  
Comando logico:

```text
@qa *review docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md --mode yolo
```

QA deve verificar:

- AC1: modulo aparece no fluxo do projeto.
- AC2: rota carrega por navegacao.
- AC3: rota profunda carrega por refresh sem 404.
- AC4: artefato de deploy contem MOD-QT.
- AC5: builds antigos nao mascaram o modulo.
- AC6: gates tecnicos passam.
- Nenhum contrato normativo de MOD-QT foi alterado.
- Nenhuma operacao remota foi executada por agente indevido.

Roteamento:

```text
PASS -> QA_HANDOFF_DEVOPS
CONCERNS -> QA_HANDOFF_DEVOPS se concerns forem documentados e nao bloquearem deploy
FAIL -> DEV_IMPLEMENTATION, max_qa_iterations = 5
WAIVED -> QA_HANDOFF_DEVOPS apenas se waiver permitir publicacao
```

## 12. Fase 7 - @qa handoff to @devops

Handoff esperado:

```yaml
path: .aiox/handoffs/MOD-QT-3-01-qa-to-devops.yaml
from_agent: "@qa"
to_agent: "@devops"
story: "MOD-QT-3-01"
last_command: "*review"
status: "Done"
gate: "PASS|CONCERNS"
gate_file: "docs/qa/gates/MOD-QT-3-01-gate.yaml"
source_artifact: "docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md"
next_command: "*pre-push"
evidence:
  acceptance_criteria: "MET"
  regression: "PASS"
  build_artifact: "PASS"
  deep_link: "PASS"
```

## 13. Fase 8 - @devops pre-push and publication

Agente: `@devops`  
Comandos logicos:

```text
@devops *pre-push
@devops *push
@devops *create-pr
```

Dry-run:

- `--dry-run` simula push, PR, merge, release, deploy e smoke.
- Usado para validar a cadeia inteira sem efeito remoto.

Execucao real:

- `remote_operations_authorized` precisa ser `true`.
- `pull_request_authorized` precisa ser `true`.
- `merge_authorized` precisa ser `true`.
- `release_authorized` precisa ser `true`.
- `deploy_authorized` precisa ser `true`.
- `rollback_authorized` precisa ser `true` antes de deploy.
- Apenas `@devops` pode executar.

Se autorizacao estiver ausente:

```text
HALT: PUSH_AUTHORIZATION_MISSING
HALT: PULL_REQUEST_AUTHORIZATION_MISSING
HALT: MERGE_AUTHORIZATION_MISSING
HALT: RELEASE_AUTHORIZATION_MISSING
HALT: DEPLOY_AUTHORIZATION_MISSING
```

## 14. Execucao recomendada

Dry-run completo:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml --dry-run
```

Execucao real local com adapters:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml --adapter-module .aiox/adapters/sdc-mod-qt-integral.js
```

Retomar execucao:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.yaml --resume <run-id> --adapter-module .aiox/adapters/sdc-mod-qt-integral.js
```

## 15. Logs e estado

O runner deve persistir:

```text
.aiox/sdc-headless/<run-id>.yaml
docs/workflows/logs/SDC-WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md-<timestamp>.md
```

O workflow deve criar ou atualizar:

```text
.aiox/handoffs/MOD-QT-3-01-sm-to-po.yaml
.aiox/handoffs/MOD-QT-3-01-po-to-dev.yaml
.aiox/handoffs/MOD-QT-3-01-dev-to-qa.yaml
.aiox/handoffs/MOD-QT-3-01-qa-to-devops.yaml
.aiox/workflow-state/MOD-QT-3-01-state.yaml
.aiox/logs/MOD-QT-3-01-yolo.log
docs/qa/gates/MOD-QT-3-01-gate.yaml
```

## 16. Criterio de conclusao

O workflow termina como `deployed` somente em dry-run completo ou execucao real autorizada quando:

- story esta `Done`;
- QA gate esta `PASS` ou waiver autorizado;
- pre-push passou;
- publicacao DevOps foi processada por `@devops`;
- deploy runbook foi executado ou simulado;
- smoke final passou;
- logs e estado foram persistidos.

Sem autorizacao remota real, o resultado correto e `blocked` antes da operacao remota, nao sucesso parcial.

