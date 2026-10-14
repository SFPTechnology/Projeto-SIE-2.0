# Workflow executor SDC YOLO — SIE-UX-01

**Workflow ID:** `sdc-yolo-execucao-sie-ux-01`  
**Modo:** automático/headless YOLO  
**Fonte de verdade:** [`WORKFLOW-SDC-YOLO-SIE-UX-01.md`](./WORKFLOW-SDC-YOLO-SIE-UX-01.md)  
**Story-alvo:** [`story-SIE-UX-01-padronizacao-headers-sie.md`](../stories/story-SIE-UX-01-padronizacao-headers-sie.md)  
**Objetivo:** executar, registrar e concluir todas as fases do workflow-base, sem prompts intermediários e sem expandir autoridades de agentes.

## Limites de execução

- Este workflow é uma camada executora do playbook-base; em caso de conflito, prevalece `WORKFLOW-SDC-YOLO-SIE-UX-01.md`.
- Não inicia operações remotas por padrão. `push`, PR, merge, release, deploy e rollback só podem ser executados por `@devops` e com autorização verdadeira no manifesto congelado.
- Não altera domínio, APIs, cálculos, permissões ou feature flags.
- Não cria requisitos além da story, do plano UX e do workflow-base.
- O workflow é retomável: uma etapa concluída com evidência válida não é repetida.

## Entradas obrigatórias

```yaml
run_id: "sdc-yolo-execucao-sie-ux-01-<timestamp>"
mode: "yolo"
story_path: "docs/stories/story-SIE-UX-01-padronizacao-headers-sie.md"
workflow_path: "docs/workflows/WORKFLOW-SDC-YOLO-SIE-UX-01.md"
plan_path: "docs/ux/PLANO-PADRONIZACAO-HEADERS-SIE.md"
max_qa_remediation_cycles: 2
remote_operations:
  push_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: false
```

## Estado persistido por execução

Cada transição deve registrar um checkpoint, o agente responsável, data/hora, evidências e resultado.

```yaml
execution_state:
  manifest: pending|validated|invalid
  story_validation: pending|go|no_go
  ux_preparation: pending|complete|blocked
  implementation: pending|complete|failed
  local_quality: pending|passed|failed
  qa: pending|pass|fail|concerns|waived
  registration: pending|complete|failed
  publication: not_requested|authorized|published|blocked
  terminal_status: null
  qa_remediation_cycles: 0
```

## Sequência automática

| Ordem | ID | Responsável | Executar | Pré-condição | Evidências | Sucesso | Falha/roteamento |
|---:|---|---|---|---|---|---|---|
| 0 | `validate_manifest` | `@aiox-master` | Validar paths, manifesto, autoridade e estado persistido; congelar fingerprint. | Entradas obrigatórias presentes. | `manifest_snapshot`, `manifest_fingerprint`. | `manifest=validated`. | Encerrar `manifest_invalid`. |
| 1 | `validate_story` | `@po` | Validar ACs, escopo, riscos e Definition of Ready da SIE-UX-01. | Manifesto válido. | `story_validation`. | `story_validation=go`. | Encerrar `story_blocked`. |
| 2 | `prepare_ux` | `@ux-design-expert` | Confirmar tokens existentes, padrão `SiePageHero`, consumidores e preservação semântica. | Story GO. | inventário de tokens/consumidores; especificação do organismo. | `ux_preparation=complete`. | Se lacuna de requisito: `validate_story`; caso contrário `story_blocked`. |
| 3 | `implement_headers` | `@ux-design-expert`, revisão `@dev` | Implementar organismo, tokens/estilos centralizados e migrações da matriz da story. | Preparação UX completa. | diff local, testes do organismo, file list parcial. | `implementation=complete`. | Reexecutar a própria etapa após correção local. |
| 4 | `run_local_quality` | `@dev` | Executar testes de renderização, headings, snapshots aprovados, lint, typecheck, testes, build SPA e CodeRabbit pre-commit. | Implementação completa. | logs, resultados dos gates e relatório CodeRabbit. | `local_quality=passed`. | Retornar a `implement_headers`. |
| 5 | `qa_review` | `@qa` | Verificar ACs, WCAG AA, responsividade, preservação de ações e regressões do Command Center. | Gates locais aprovados. | `qa_verdict`. | `qa=pass` ou `qa=waived`. | Aplicar política de remediação. |
| 6 | `register_story` | `@ux-design-expert` | Atualizar checkboxes, Completion Notes, File List e QA Results. | QA PASS/WAIVED. | story atualizada. | `registration=complete`. | Encerrar `pre_publication_blocked`. |
| 7 | `publish_if_authorized` | `@devops` | Executar pre-push, push e PR conforme flags autorizadas. | Registro completo. | `devops_report`, resultados remotos. | `publication=published` ou `not_requested`. | Encerrar `pre_publication_blocked`; rollback só se autorizado. |
| 8 | `complete` | `@aiox-master` | Consolidar status e evidências finais. | Fase 6 concluída; Fase 7 concluída ou não solicitada. | sumário de execução e status terminal. | `ready_for_devops` ou `published`. | Estado terminal de bloqueio preservado. |

## Política de remediação automática

```text
QA FAIL ou CONCERNS
  └── qa_remediation_cycles < 2?
      ├── sim: incrementar contador → implement_headers → run_local_quality → qa_review
      └── não: encerrar qa_blocked com a última evidência de QA

Falha de gate local
  └── implement_headers → run_local_quality

Story NO-GO
  └── encerrar story_blocked; não modificar código

Operação remota não autorizada
  └── não é falha: registrar publication=not_requested e concluir ready_for_devops
```

## Cobertura mandatória da Fase 3

A etapa `implement_headers` só pode declarar sucesso quando as seguintes frentes tiverem evidência:

1. `SiePageHero` e variantes módulo/índice centralizados.
2. Dependências como rota piloto, preservando “Nova dependência”.
3. Queda de tensão e Planejador de circuitos, preservando Tutorial, tags e toolbar.
4. Padrão de entrada, Correntes, Dimensionamento, Unifilar interativo e Diagrama unifilar.
5. Projetos, sem remover métricas.
6. Command Center, sem segundo `h1` e sem redesenhar headers internos.
7. Remoção de legado somente sem consumidores restantes.

## Critérios automáticos de passagem

- Um único `h1` por rota migrada; títulos internos em `h2` ou inferior.
- `--sie-font-sans` nos headers e `--sie-font-mono` apenas em dados técnicos.
- Hero com tokens/estilos centralizados, sem equivalentes visuais inline nas rotas migradas.
- Ações, handlers, rotas, métricas, tags e toolbars preservados.
- Conteúdo e ações responsivos abaixo de 960px.
- Contraste, foco e semântica compatíveis com WCAG AA.
- `npm run lint`, `npm run typecheck`, `npm test` e `npm run build:spa` aprovados.
- CodeRabbit pre-commit executado; findings CRITICAL entram no loop de correção.

## Estados terminais

| Estado | Condição |
|---|---|
| `ready_for_devops` | Implementação, gates, QA e registro concluídos; publicação não autorizada. |
| `published` | Publicação autorizada e executada por `@devops`. |
| `manifest_invalid` | Manifesto inválido, incompleto ou com autoridade incompatível. |
| `story_blocked` | PO emitiu NO-GO ou há lacuna de requisito não resolvida. |
| `qa_blocked` | Dois ciclos de remediação foram consumidos sem QA PASS/WAIVED. |
| `pre_publication_blocked` | Registro, gate crítico ou publicação autorizada falhou. |
| `rollback_completed` | Rollback foi autorizado e executado por `@devops`. |

## Handoffs automáticos

| Evento | Próximo responsável | Mensagem de execução |
|---|---|---|
| Manifesto validado | `@po` | “Manifesto congelado e validado. Validar SIE-UX-01.” |
| Story GO | `@ux-design-expert` | “Story aprovada. Preparar e implementar a padronização de headers.” |
| Implementação concluída | `@dev` | “Executar gates locais e CodeRabbit pre-commit.” |
| Gates locais aprovados | `@qa` | “Avaliar ACs, a11y, responsividade e regressões.” |
| QA PASS/WAIVED | `@ux-design-expert` | “Atualizar registros finais da story.” |
| Registro concluído | `@devops` ou finalização local | “Publicar somente se o manifesto autorizar; caso contrário concluir como ready_for_devops.” |

## Comando de início

Este documento descreve o contrato de execução e não concede permissões remotas. A execução deve usar o ciclo headless do framework com o manifesto desta execução.

```text
@aiox-master
*run-workflow story-development-cycle-headless-yolo start --mode=engine

run_id: sdc-yolo-execucao-sie-ux-01-<timestamp>
story_path: docs/stories/story-SIE-UX-01-padronizacao-headers-sie.md
workflow_path: docs/workflows/WORKFLOW-SDC-YOLO-SIE-UX-01.md
mode: yolo
```

## Referências

- [`WORKFLOW-SDC-YOLO-SIE-UX-01.md`](./WORKFLOW-SDC-YOLO-SIE-UX-01.md)
- [`story-SIE-UX-01-padronizacao-headers-sie.md`](../stories/story-SIE-UX-01-padronizacao-headers-sie.md)
- [`PLANO-PADRONIZACAO-HEADERS-SIE.md`](../ux/PLANO-PADRONIZACAO-HEADERS-SIE.md)
- `.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`
