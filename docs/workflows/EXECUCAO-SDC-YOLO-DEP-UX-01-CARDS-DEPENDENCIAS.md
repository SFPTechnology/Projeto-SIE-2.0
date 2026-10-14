# Execução SDC automática YOLO — DEP-UX-01: cards de Dependências

**Execution ID:** `sdc-yolo-dep-ux-01-execution`  
**Versão:** 1.0.0  
**Modo:** YOLO/headless, `interaction_policy: never_prompt`  
**Workflow-fonte:** [`WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md`](WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md)  
**Story-alvo:** [`story-DEP-UX-01-reestruturacao-cards-dependencias.md`](../stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md)  
**Contrato de engine:** [`.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`](../../.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml)

## 1. Objetivo

Executar, de ponta a ponta, todos os processos e fases prescritos pelo workflow-fonte para a story DEP-UX-01: validação do manifesto, aprovação da story, descoberta de contrato, composição UX, implementação, quality gates, QA, atualização da story e publicação opcional.

Este documento é a especificação operacional de uma execução. Não autoriza ações além do workflow-fonte, não altera o escopo da story e não substitui as autoridades exclusivas dos agentes.

## 2. Configuração da execução

O orquestrador cria um diretório novo por execução. O manifesto é gravado uma única vez e seu fingerprint passa a ser pré-condição de todo checkpoint seguinte.

```yaml
sdc_execution:
  run_id: "sdc-yolo-dep-ux-01-<timestamp>"
  execution_id: "sdc-yolo-dep-ux-01-execution"
  workflow_file: "docs/workflows/WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md"
  story_file: "docs/stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md"
  briefing_file: "docs/ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md"
  base_engine_workflow: ".aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml"
  mode: "yolo"
  interaction_policy: "never_prompt"

  checkpoint_root: ".aiox/sdc-headless/<run_id>"
  state_file: ".aiox/sdc-headless/<run_id>/terminal-state.yaml"
  max_qa_remediation_cycles: 2

  authorization:
    local_implementation: true
    remote_operations: false
    pull_request: false
    merge: false
    release: false
    deploy: false
    rollback: false

  failure_policy:
    missing_input: "block_and_log"
    missing_contract: "block_and_log"
    worktree_overlap: "block_and_log"
    quality_gate_failure: "remediate_within_limit"
    qa_failure: "remediate_within_limit"

  protected_contracts:
    - "Detalhe"
    - "Calcular"
    - "Historico"
    - "Duplicar"
    - "DependenciaAgregado"
    - "EstadoDependencia"
```

## 3. Regras de execução automática

1. O engine não pergunta entre fases; ele usa exclusivamente o manifesto congelado e os resultados de checkpoint.
2. Cada fase inicia somente se os artefatos de entrada, o fingerprint e as pré-condições estiverem válidos.
3. Cada fase grava seu resultado antes de emitir handoff ou avançar o estado.
4. O engine pode repetir apenas os loops de implementação e qualidade definidos na seção 6.
5. Bloqueios de contrato, story, worktree ou autorização encerram a execução; não há correção especulativa em YOLO.
6. Operações externas são negadas enquanto as flags de autorização forem `false`.

## 4. Inicialização e idempotência

### 4.1 Criar ou retomar execução

```text
Se checkpoint_root não existir:
  criar run_id e diretório de checkpoints
  gravar manifesto.yaml
  calcular manifest-fingerprint.txt
  estado atual = manifest_validation

Se checkpoint_root existir:
  comparar fingerprint atual com manifest-fingerprint.txt
  se diferente: encerrar manifest_invalid
  se terminal-state for terminal: não reexecutar
  se não terminal: retomar da primeira fase sem checkpoint PASS
```

### 4.2 Pré-flight obrigatório

| Verificação | Critério de passagem | Falha |
|---|---|---|
| Arquivos-fonte | Workflow, story, briefing e engine existem. | `manifest_invalid` |
| Escopo | Workflow e story referem DEP-UX-01. | `manifest_invalid` |
| Autoridades | DevOps é o único agente em qualquer etapa externa. | `manifest_invalid` |
| Proteções | As quatro ações obrigatórias estão em `protected_contracts`. | `manifest_invalid` |
| Flags remotas | Todas são `false`, salvo execução nova autorizada. | `manifest_invalid` |
| Limite QA | `max_qa_remediation_cycles` é `2`. | `manifest_invalid` |

O resultado é gravado em `00-manifest-validation.md`. Somente `PASS` permite a Fase 1.

## 5. Plano de execução por fase

| ID | Estado | Agente | Ação automática | Entradas obrigatórias | Saídas/checkpoint | Regra de avanço |
|---|---|---|---|---|---|---|
| P0 | `manifest_validation` | `@aiox-master` | Validar manifesto, fingerprint, pré-flight e estado recuperável. | Manifesto proposto. | `00-manifest-validation.md` | PASS → P1; falha → `manifest_invalid`. |
| P1 | `story_validation` | `@po` | Emitir GO/NO-GO contra ACs, escopo e testabilidade da DEP-UX-01. | Story Draft, briefing e workflow-fonte. | `01-story-validation.md` | GO → P2; NO-GO → `story_blocked`. |
| P2 | `contract_discovery` | `@ux-design-expert` | Mapear rota, componentes, view model, dados, handlers, testes e worktree. | Story GO. | `02-contract-inventory.md`, `02-worktree-overlap.md` | Seguro → P3; lacuna → `contract_blocked`; overlap → `worktree_blocked`. |
| P3 | `ux_system_composition` | `@ux-design-expert` | Reutilizar tokens/componentes e definir card, grupos, estados, resumo e responsividade. | Inventário PASS. | `03-ux-composition.md` | PASS → P4; novo contrato → `contract_blocked`. |
| P4 | `card_and_explorer_implementation` | `@ux-design-expert` | Implementar somente recursos suportados, preservando os contratos protegidos. | Plano UX PASS. | `04-implementation-evidence.md`, lista de arquivos. | PASS → P5; falha interna → P4. |
| P5 | `local_quality` | `@dev` | Rodar testes aplicáveis, lint, typecheck, testes completos, a11y e CodeRabbit quando disponível. | Evidência da implementação. | `05-quality-gates.md` | PASS → P6; falha corrigível → P4; limite/escalonamento → `local_quality_blocked`. |
| P6 | `qa_review` | `@qa` | Verificar os 11 ACs, regressão, responsividade e WCAG AA. | Gates PASS. | `06-qa-verdict.md` | PASS/WAIVED → P7; FAIL/CONCERNS → P4 até o limite; excedido → `qa_blocked`. |
| P7 | `story_record_update` | `@ux-design-expert` | Atualizar tasks, Completion Notes, File List e QA Results. | QA PASS/WAIVED. | `07-story-record.md`, story atualizada. | PASS → P8; falha → `local_quality_blocked`. |
| P8 | `publication_decision` | `@aiox-master` | Avaliar flags remotas sem modificar o manifesto. | Registro PASS. | `08-publication-decision.md` | Todas falsas → `ready_for_devops`; autorizada → P9. |
| P9 | `publication` | `@devops` | Executar somente os efeitos remotos explicitamente autorizados. | Flags específicas verdadeiras. | `09-devops-report.md` | PASS → `published`; falha → `publication_blocked`. |

## 6. Loops, bloqueios e transições

### 6.1 Loop local de qualidade

```text
P4 implementação → P5 qualidade local
P5 PASS → P6 QA
P5 falha corrigível → P4 implementação
P5 falha não corrigível / pré-condição ausente → local_quality_blocked
```

### 6.2 Loop de remediação QA

```text
P6 PASS ou WAIVED justificado → P7
P6 FAIL ou CONCERNS:
  registrar ciclo N em 06-qa-verdict.md
  se N <= 2: P4
  se N > 2: qa_blocked
```

`WAIVED` só passa quando o veredito contém justificativa explícita e não viola um acceptance criterion inegociável, uma proteção de contrato ou um gate obrigatório.

### 6.3 Bloqueios sem tentativa de auto-correção

| Situação detectada | Ação | Estado terminal |
|---|---|---|
| Story NO-GO | Não editar story nem código. | `story_blocked` |
| Campo/API/regra de domínio ausente | Registrar evidência e encaminhar a `@architect`. | `contract_blocked` |
| Arquivo necessário contém trabalho de outra frente sem separação segura | Não modificar o arquivo. | `worktree_blocked` |
| Manifesto alterado durante run | Preservar checkpoints e negar retomada. | `manifest_invalid` |
| Operação remota não autorizada | Não invocar DevOps. | `ready_for_devops` |

## 7. Contrato de implementação da DEP-UX-01

P4 deve executar todos os itens abaixo, mas somente quando a descoberta P2 comprovar suporte no contrato existente:

1. Card semântico com nome, metadados disponíveis, estado atual, iluminação, tomadas, cargas e atualização.
2. Indicação `Requer verificação` somente quando derivada de `VERIFICAR`; não criar estados fictícios.
3. Grupos técnicos comparáveis, mantendo unidades e origem automática/manual quando já disponível.
4. Rodapé com `Detalhe`, `Calcular`, `Historico` e `Duplicar` sempre visíveis, inclusive em mobile.
5. Busca existente preservada; filtros, chips, ordenação e lista técnica somente se reaproveitarem contratos existentes.
6. Resumo operacional usando somente contadores derivados de dados existentes.
7. Estados de loading, vazio, sem resultado e erro conforme padrões da aplicação.
8. Responsividade e acessibilidade conforme os ACs 8 e 9 da story.

## 8. Gates P5 e critérios de QA P6

### 8.1 Quality gates locais

```text
npm run lint
npm run typecheck
npm test
```

Além dos comandos, P5 deve registrar:

- o escopo de testes de tabela/view model;
- evidência de preservação de rótulo e handler/destino das quatro ações;
- resultado de semântica, teclado, foco, ARIA e contraste WCAG AA;
- resultado do CodeRabbit ou motivo factual de indisponibilidade, conforme a política de degradação já configurada no projeto.

### 8.2 Checklist QA obrigatório

- [ ] AC1 a AC11 verificados individualmente.
- [ ] Nenhuma alteração em domínio, API, persistência, schema, auditoria, permissões ou feature flags.
- [ ] `Detalhe`, `Calcular`, `Historico` e `Duplicar` continuam visíveis e funcionais.
- [ ] Nenhuma ação obrigatória foi transferida para menu contextual.
- [ ] Estado é compreensível sem cor ou hover.
- [ ] Desktop, tablet e mobile não perdem valores ou ações.
- [ ] File List, Completion Notes e QA Results da story foram atualizados antes de P8.

## 9. Formato de checkpoint

Cada checkpoint deve usar esta estrutura mínima:

```markdown
# Checkpoint <P#> — <estado>

- Run ID: `<run_id>`
- Manifest fingerprint: `<sha256>`
- Responsável: `@<agent>`
- Início/Fim: `<ISO 8601>`
- Entrada validada: `<lista>`
- Resultado: `PASS | FAIL | BLOCKED | WAIVED`
- Evidências: `<paths, comandos, diffs ou vereditos>`
- Próximo estado: `<state>`
- Motivo de bloqueio/retomada: `<quando houver>`
```

## 10. Estado terminal

Ao terminar, gravar `.aiox/sdc-headless/<run_id>/terminal-state.yaml`:

```yaml
run_id: "sdc-yolo-dep-ux-01-<timestamp>"
workflow_id: "sdc-yolo-dep-ux-01"
terminal_state: "ready_for_devops"
completed_at: "<ISO 8601>"
manifest_fingerprint: "<sha256>"
completed_phases:
  - P0
  - P1
  - P2
  - P3
  - P4
  - P5
  - P6
  - P7
evidence_root: ".aiox/sdc-headless/<run_id>"
remote_effects_executed: false
```

Estados válidos: `ready_for_devops`, `published`, `manifest_invalid`, `story_blocked`, `contract_blocked`, `worktree_blocked`, `local_quality_blocked`, `qa_blocked`, `publication_blocked` e `rollback_completed`.

## 11. Comando de partida

```text
@aiox-master
*run-workflow story-development-cycle-headless-yolo start --mode=engine

Execution: docs/workflows/EXECUCAO-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md
Workflow source: docs/workflows/WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md
Manifest: .aiox/sdc-headless/sdc-yolo-dep-ux-01-<timestamp>/manifest.yaml
```

## Referências

- [`WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md`](WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md)
- [`story-DEP-UX-01-reestruturacao-cards-dependencias.md`](../stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md)
- [`ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md`](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md)
- [`story-development-cycle-headless-yolo.yaml`](../../.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml)
