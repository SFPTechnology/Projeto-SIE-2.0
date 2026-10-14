# Workflow SDC automático YOLO — DEP-UX-01: cards de Dependências

**Workflow ID:** `sdc-yolo-dep-ux-01`  
**Versão:** 1.0.0  
**Modo:** YOLO/headless — zero prompts após a validação do manifesto  
**Story-alvo:** [`story-DEP-UX-01-reestruturacao-cards-dependencias.md`](../stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md)  
**Briefing UX:** [`ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md`](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md)  
**Contrato-base:** [`.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`](../../.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml)  
**Escopo:** implementação local e validação completa da DEP-UX-01; operações remotas permanecem desabilitadas por padrão.

## 1. Finalidade

Orquestrar todas as fases da DEP-UX-01 de forma determinística: validar a story, congelar os contratos existentes, compor a experiência visual, migrar os cards e a exploração suportada, testar, revisar em QA e atualizar a rastreabilidade da story.

Este é um contrato operacional em Markdown, compatível com o SDC headless. Ele não cria um motor paralelo nem concede autoridade adicional a agentes. Para execução, o orquestrador deve materializar um manifesto imutável por execução e obedecer à máquina de estados abaixo.

## 2. Princípios YOLO e limites de autoridade

- Após o manifesto ser validado, não solicitar confirmações entre fases.
- Persistir checkpoint e evidência ao fim de cada etapa, permitindo retomada idempotente.
- Executar somente requisitos explícitos da DEP-UX-01 e do briefing UX.
- Preservar, sem exceção, `Detalhe`, `Calcular`, `Historico` e `Duplicar`: rótulo, conteúdo, comportamento, destino e permissões.
- Não alterar cálculos, NBR, APIs, persistência, schema, auditoria, permissões ou feature flags.
- Não descartar, sobrescrever ou incorporar alterações locais preexistentes. Conflito de escopo ou worktree exige estado terminal bloqueado, não resolução automática.
- Somente `@devops` pode executar push, PR, merge, release, deploy ou rollback — e apenas se as flags do manifesto autorizarem a operação.
- `@architect` é chamado somente quando uma fase concluir que a story exige novo contrato de dados, estado de domínio ou mudança arquitetural. Essa situação não é resolvida pelo modo YOLO.

## 3. Manifesto de execução imutável

Antes de iniciar, `@aiox-master` cria e congela um manifesto em `.aiox/sdc-headless/`. Alterar qualquer valor cria uma execução nova; não é permitido editar o manifesto em andamento.

```yaml
sdc_execution:
  run_id: "sdc-yolo-dep-ux-01-<timestamp>"
  workflow_id: "sdc-yolo-dep-ux-01"
  story_id: "DEP-UX-01"
  story_file: "docs/stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md"
  source_artifact: "docs/ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md"
  execution_mode: "yolo"
  interaction_policy: "never_prompt"
  on_missing_input: "block_and_log"
  on_preexisting_worktree_overlap: "block_and_log"
  max_qa_remediation_cycles: 2

  local_operations_authorized: true
  remote_operations_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: false

  protected_contracts:
    - "Detalhe"
    - "Calcular"
    - "Historico"
    - "Duplicar"
    - "DependenciaAgregado"
    - "EstadoDependencia"

  required_quality_gates:
    - "npm run lint"
    - "npm run typecheck"
    - "npm test"
    - "WCAG AA review"
```

### Validação obrigatória do manifesto

O manifesto só é válido quando:

1. A story e o briefing existem e possuem o ID/paths declarados.
2. As cinco flags remotas continuam `false`, salvo autorização explícita em nova execução.
3. Os contratos protegidos incluem as quatro ações obrigatórias.
4. O diretório da aplicação e os arquivos de superfície são inventariados antes de qualquer edição.
5. O estado anterior do mesmo `run_id` não indica manifesto alterado, execução finalizada ou checkpoint inconsistente.

Falha nesta validação encerra em `manifest_invalid`.

## 4. Máquina de estados

```text
manifest_validation
  → story_validation
  → contract_discovery
  → ux_system_composition
  → card_and_explorer_implementation
  → local_quality
  → qa_review
      ↘ remediation (máx. 2) → card_and_explorer_implementation
  → story_record_update
  → ready_for_devops | published

Terminais alternativos:
manifest_invalid | story_blocked | contract_blocked | worktree_blocked |
qa_blocked | local_quality_blocked | publication_blocked
```

## 5. Sequência automática de fases

| Fase | Responsável | Entrada | Ação headless | Evidência mínima | Próximo estado / falha |
|---|---|---|---|---|---|
| 0. Manifesto | `@aiox-master` | manifesto proposto | Validar paths, autoridades, flags, fingerprint e checkpoints. | `manifest_snapshot`, `manifest_fingerprint` | `story_validation` / `manifest_invalid` |
| 1. Story GO/NO-GO | `@po` | story Draft + briefing | Validar ACs, escopo, dependências, riscos e testabilidade. | `story_validation: GO|NO-GO` | `contract_discovery` / `story_blocked` |
| 2. Descoberta de contrato | `@ux-design-expert` | story GO | Mapear rota, tabela/cards, view model, dados, handlers, testes e arquivos modificados por outras frentes. | `contract_inventory`, `worktree_overlap_report` | `ux_system_composition` / `contract_blocked` ou `worktree_blocked` |
| 3. Composição UX | `@ux-design-expert` | inventário aprovado | Reutilizar tokens e componentes; definir organismo do card, grupos técnicos, estados reais, resumo operacional e responsividade. | `ux_implementation_plan`, `component_inventory` | `card_and_explorer_implementation` / `contract_blocked` |
| 4. Implementação | `@ux-design-expert` | plano UX aprovado | Implementar card, coleção, exploração já suportada e estados de interface, preservando contratos protegidos. | `implementation_evidence`, `changed_files` | `local_quality` / repetir fase 4 |
| 5. Qualidade local | `@dev` | evidência de implementação | Executar testes aplicáveis, lint, typecheck, teste completo, revisão de a11y e CodeRabbit quando disponível. | `quality_gate_evidence` | `qa_review` / `local_quality_blocked` ou fase 4 |
| 6. QA | `@qa` | qualidade local | Verificar os 11 ACs, regressão das quatro ações, responsividade, estados de interface e WCAG AA. | `qa_verdict: PASS|FAIL|CONCERNS|WAIVED` | `story_record_update` / remediação ou `qa_blocked` |
| 7. Registro | `@ux-design-expert` | QA PASS/WAIVED | Atualizar tarefas, Completion Notes, File List e referências de QA na story. | story atualizada + `story_record_evidence` | `ready_for_devops` / `local_quality_blocked` |
| 8. Publicação opcional | `@devops` | `ready_for_devops` | Executar apenas operações explicitamente autorizadas no manifesto. | `devops_report` | `published` / `publication_blocked` |

## 6. Regras determinísticas por fase

### Fase 1 — validação da story

- `NO-GO` encerra a execução: não é permitido escrever código, editar a story em nome do PO ou inferir aprovação.
- `GO` autoriza apenas o escopo descrito nos 11 ACs, Tasks/Subtasks e Dev Notes da DEP-UX-01.

### Fase 2 — descoberta e proteção do worktree

- Confirmar fontes reais de `Calculada`, `VERIFICAR`, iluminação, tomadas, cargas, atualização, busca e filtros.
- Confirmar os handlers e destinos atuais de `Detalhe`, `Calcular`, `Historico` e `Duplicar` antes de refatorar a apresentação.
- Registrar arquivos modificados por outra frente. Se qualquer arquivo necessário estiver sujo e a alteração não puder ser separada sem risco, encerrar em `worktree_blocked`.
- Se uma exigência depender de campo, API, persistência, regra de domínio ou estado não existente, encerrar em `contract_blocked` e encaminhar a `@architect`; não criar fallback fictício.

### Fase 3 — composição UX

- Reusar tokens SIE, tipografia e padrões de header existentes.
- Os estados apresentados devem ser derivados: `Requer verificação` só é permitido quando existir indicador atual de `VERIFICAR`.
- O resumo operacional pode mostrar total e calculadas; demais contadores exigem fonte comprovada na descoberta.
- Lista técnica, chips e ordenação só entram se puderem usar contratos existentes. Caso contrário, a grade melhorada permanece como entrega válida.

### Fase 4 — implementação

Executar Tasks 2 e 3 da story nesta ordem:

1. Card semântico com `h2`, metadados compactos e grupos comparáveis de iluminação, tomadas e cargas.
2. Estado de cálculo existente e sinalização de exceção derivada, nunca dependente apenas de cor.
3. Rodapé com as quatro ações obrigatórias sempre expostas — inclusive no mobile.
4. Busca e filtros existentes preservados; novos controles somente se suportados.
5. Estados de carregamento, vazio, sem resultados e erro.
6. Responsividade desktop/tablet/mobile sem ocultação de valores ou ações.

### Fases 5 e 6 — gates e remediação

- Falha de lint, typecheck ou teste retorna à Fase 4 até que passe; não avançar para QA com gate local falho.
- CodeRabbit indisponível é registrado com evidência e tratado conforme a política de degradação do projeto; findings CRITICAL disponíveis retornam à Fase 4.
- QA `FAIL` ou `CONCERNS` abre um ciclo de remediação. Há no máximo dois ciclos completos de implementação → qualidade local → QA depois da primeira revisão.
- Ao exceder o limite, encerrar em `qa_blocked`, mantendo logs e checklist sem marcar a story como concluída.

### Fases 7 e 8 — encerramento e publicação

- O registro na story é obrigatório para conclusão local: tasks/subtasks, Completion Notes, File List e QA Results.
- Sem autorização remota, encerrar em `ready_for_devops`. Isso é sucesso local; nenhum push ou PR é tentado.
- Com autorização explícita em manifesto novo, somente `@devops` executa push/PR/merge/release/deploy conforme as flags específicas.

## 7. Gates de aceite automatizáveis

| Gate | Evidência exigida |
|---|---|
| Contrato de ações | As quatro ações mantêm texto, handler/destino e permanecem visíveis fora do menu contextual. |
| Dados e domínio | Nenhuma modificação em cálculo, NBR, API, persistência, schema, auditoria, permissões ou feature flags. |
| Hierarquia | Nome do ambiente é título semântico; metadados, estado, grupos técnicos e atualização são legíveis sem abrir detalhes. |
| Exceções reais | `VERIFICAR` é perceptível e derivado de dado existente; não há estado fictício. |
| Exploração | Busca e filtros existentes não regressam; novos filtros/ordenação têm fonte comprovada. |
| Responsividade | Desktop, tablet e mobile mantêm todos os valores e as quatro ações. |
| Acessibilidade | Semântica, teclado, foco, rótulos acessíveis e contraste WCAG AA. |
| Testes | Cobertura do view model/tabela, indicador de verificação, busca/filtros, resultados vazios e ações preservadas. |
| Qualidade | `npm run lint`, `npm run typecheck` e `npm test` aprovados no contexto aplicável. |
| Rastreabilidade | Story atualizada com checklist, evidências, Completion Notes, File List e QA Results. |

## 8. Política de falhas e retomada

| Condição | Ação YOLO | Estado terminal/retorno |
|---|---|---|
| Manifesto inválido ou alterado | Não executar fases seguintes; salvar diagnóstico. | `manifest_invalid` |
| Story NO-GO | Não implementar; preservar estado Draft e reportar. | `story_blocked` |
| Novo contrato/estado necessário | Não inventar; registrar dependência para `@architect`. | `contract_blocked` |
| Sobreposição perigosa com worktree sujo | Não modificar os arquivos em conflito. | `worktree_blocked` |
| Gate local falha | Corrigir na Fase 4 e repetir gate. | retorno à Fase 4 |
| QA falha/concern | Remediar até duas vezes, com evidência por ciclo. | retorno à Fase 4 ou `qa_blocked` |
| Falta autorização remota | Não tentar efeito externo. | `ready_for_devops` |
| Falha em operação remota autorizada | `@devops` aplica runbook/rollback somente se permitido. | `publication_blocked` ou `rollback_completed` |

## 9. Artefatos e checkpoints

```text
.aiox/sdc-headless/
└── sdc-yolo-dep-ux-01-<timestamp>/
    ├── manifest.yaml
    ├── manifest-fingerprint.txt
    ├── 00-manifest-validation.md
    ├── 01-story-validation.md
    ├── 02-contract-inventory.md
    ├── 03-ux-composition.md
    ├── 04-implementation-evidence.md
    ├── 05-quality-gates.md
    ├── 06-qa-verdict.md
    ├── 07-story-record.md
    └── terminal-state.yaml
```

Os artefatos de checkpoint são aditivos: não substituem a story nem editam o trabalho de outra frente.

## 10. Critério de conclusão

`ready_for_devops` é alcançado somente quando:

- os 11 ACs da DEP-UX-01 foram verificados;
- todos os quality gates obrigatórios passaram;
- QA emitiu `PASS` ou `WAIVED` justificado;
- a story contém tarefas, Completion Notes, File List e QA Results atualizados;
- nenhuma operação remota foi executada sem autorização explícita.

Com operação remota autorizada e concluída por `@devops`, o terminal é `published`.

## 11. Como iniciar

```text
@aiox-master
*run-workflow story-development-cycle-headless-yolo start --mode=engine

Manifesto: .aiox/sdc-headless/sdc-yolo-dep-ux-01-<timestamp>/manifest.yaml
Story: docs/stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md
Workflow: docs/workflows/WORKFLOW-SDC-YOLO-DEP-UX-01-CARDS-DEPENDENCIAS.md
Modo: yolo
```

## Referências

- [`story-DEP-UX-01-reestruturacao-cards-dependencias.md`](../stories/story-DEP-UX-01-reestruturacao-cards-dependencias.md)
- [`ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md`](../ux/ANALISE-REESTRUTURACAO-CARDS-DEPENDENCIAS.md)
- [`PLANO-PADRONIZACAO-HEADERS-SIE.md`](../ux/PLANO-PADRONIZACAO-HEADERS-SIE.md)
- [`story-development-cycle-headless-yolo.yaml`](../../.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml)
