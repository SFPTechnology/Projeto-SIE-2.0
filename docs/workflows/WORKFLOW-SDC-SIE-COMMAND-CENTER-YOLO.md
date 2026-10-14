# Workflow SDC Headless YOLO — SIE Command Center

**Versão:** 1.0.0  
**Data:** 2026-07-31  
**Status:** Ready for dry-run; live execution requires the architecture-phase adapter and an authorized immutable manifest  
**Modo:** YOLO headless, zero prompts durante a execução  
**Escopo:** Design artifacts → Stories → PO → Architect → Dev → QA → DevOps → Deploy  
**Fonte de implementação:** `outputs/design-system/sie-command-center/`  
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md`  
**Workflow executável base:** `.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`  
**Conformidade:** `.aiox-core/constitution.md` e `AGENTS.md`

> Este documento define a especialização automática do SDC para implementar o SIE Command Center. Ele não cria stories, não aprova arquitetura, não emite veredito de qualidade e não autoriza operações remotas. Essas ações continuam pertencendo exclusivamente aos agentes definidos pela Constituição.

> **Zero intervenção humana** significa zero prompts depois que um manifesto completo e autorizado foi congelado. Ausência de requisito, adapter, evidência, autorização ou infraestrutura encerra a execução como `BLOCKED` ou `FAILED`; nunca gera aprovação presumida.

---

## 1. Objetivo

Implementar a variante descrita em `outputs/design-system/sie-command-center/` de forma aditiva, reversível e observável, preservando integralmente o design atual até que uma story posterior autorize qualquer mudança de padrão.

Sequência obrigatória:

```text
@sm cria/refina a story
  → @po valida requisitos e valor
    → @architect ratifica arquitetura, integração e rollback
      → @dev implementa a variante isolada
        → @qa revisa e qualifica o trabalho do @dev
          → @dev corrige automaticamente quando necessário
            → @devops executa pre-push, push, PR, release e deploy autorizados
```

O workflow continua automaticamente até um estado terminal:

```text
DEPLOYED | BLOCKED | FAILED | ROLLED_BACK
```

## 2. Princípios inegociáveis

1. **CLI First:** nenhuma interface pode redefinir cálculo, estado ou regra de domínio.
2. **Story-Driven:** nenhum código de produção é alterado sem story `Ready`.
3. **No Invention:** toda decisão deve rastrear para um artefato do Command Center, requisito/story existente ou finding aprovado.
4. **Agent Authority:** cada gate é executado pelo agente autorizado.
5. **Quality First:** lint, typecheck, testes, build, segurança e QA são bloqueantes.
6. **Legacy Preservation:** o design atual continua disponível e recuperável.
7. **Additive Delivery:** a variante nova usa namespace, shell ou feature flag ratificados pelo `@architect`.
8. **Fail Closed:** erro ou evidência ausente bloqueia; YOLO nunca transforma `BLOCK` em `PASS`.
9. **Idempotência:** resume não repete push, PR, merge, release, deploy ou rollback concluídos.
10. **DevOps Exclusivo:** apenas `@devops` realiza operações remotas e deploy.

## 3. Fontes de verdade

### 3.1 Artefatos obrigatórios do design

| Artefato | Papel no SDC |
|---|---|
| `outputs/design-system/sie-command-center/README.md` | visão, limites e inventário |
| `outputs/design-system/sie-command-center/.state.yaml` | readiness e capability gaps |
| `outputs/design-system/sie-command-center/audit/current-state.md` | baseline brownfield |
| `outputs/design-system/sie-command-center/research/benchmark.md` | findings de UX/UI verificados |
| `outputs/design-system/sie-command-center/docs/experience-architecture.md` | módulos, layouts, responsividade e restrições |
| `outputs/design-system/sie-command-center/docs/component-catalog.md` | catálogo Atomic Design e contratos |
| `outputs/design-system/sie-command-center/tokens/sie-premium.tokens.json` | tokens DTCG |
| `outputs/design-system/sie-command-center/tokens/sie-premium.css` | consumo CSS de referência |
| `outputs/design-system/sie-command-center/prototype/` | referência comportamental e visual |
| `outputs/design-system/sie-command-center/migration/adoption-plan.md` | fases, feature flag e rollback |
| `outputs/design-system/sie-command-center/validation/quality-report.md` | gates cumpridos, pendências e capability gaps |

### 3.2 Artefatos canônicos do SDC

- `.aiox-core/constitution.md`;
- `.aiox-core/development/workflows/story-development-cycle.yaml`;
- `.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`;
- `.aiox-core/core/orchestration/sdc-headless-yolo-runner.js`;
- `.aiox-core/development/scripts/sdc-headless-yolo.js`;
- `.aiox-core/data/workflow-chains.yaml`;
- `docs/architecture/ADR-SDC-AUTO-1-ORQUESTRACAO-HEADLESS-YOLO.md`;
- `docs/workflows/WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md`.

### 3.3 Ordem de precedência

```text
Constitution
  > PRD/épico/story aprovada
    > decisões ratificadas por @architect
      > artefatos do SIE Command Center
        > protótipo visual
```

O protótipo nunca substitui critérios de aceite, contratos de domínio ou decisão arquitetural.

## 4. Escopo

### 4.1 IN

- tokens semânticos `--sie-*`;
- namespace DTCG e bindings para as primitives aprovadas;
- catálogo Atomic Design;
- shell de engenharia opt-in;
- navegação por ciclo do projeto;
- cabeçalho contextual;
- paleta de comandos;
- densidade `comfortable` e `compact`;
- templates Overview, List + Inspector, Parameters + Results, Canvas + Inspector e Decision;
- migração aditiva dos módulos existentes para a variante;
- acessibilidade WCAG 2.2 AA;
- responsividade, estados, rastreabilidade e reduced motion;
- feature flag/rollback;
- testes e documentação;
- publicação e deploy autorizados.

### 4.2 OUT

- alteração de fórmulas, normas ou motores de cálculo;
- mudança de contratos CLI/API sem requisito aprovado;
- migration de banco por padrão;
- exclusão ou sobrescrita do design atual;
- remoção do `AppShell` ou componentes legacy;
- criação de novos módulos de domínio;
- definição de persona ou meta UX sem pesquisa aprovada;
- operação remota não registrada no manifesto.

## 5. Pré-condições bloqueantes

Antes da criação da primeira story, o orquestrador deve validar:

- [ ] Todos os artefatos da seção 3.1 existem e são legíveis.
- [ ] `.state.yaml` está em `ready_for_review` ou estado posterior compatível.
- [ ] O repositório e o subprojeto frontend foram identificados.
- [ ] Mudanças preexistentes do usuário foram inventariadas e preservadas.
- [ ] O design atual possui estratégia de manutenção/rollback.
- [ ] O manifesto informa branch, remote, ambiente e runbook exatos.
- [ ] O adapter headless expõe funções distintas para `sm`, `po`, `architect`, `dev`, `qa`, `gates`, `devops` e `smoke`.
- [ ] O runtime consegue persistir a fase `architect_ratification`.
- [ ] O deploy runbook existe.
- [ ] Rollback está autorizado antes de qualquer deploy.

Falha:

```text
HALT: SIE_DS_PRECONDITION_BLOCKED
Persistir evidência, owner, condição de retomada e fingerprint do manifesto.
Não perguntar ao usuário.
Não criar código.
```

## 6. Gap obrigatório do runner atual

O runner atual executa:

```text
@sm → @po → @dev → @qa → @devops
```

Ele ainda não possui uma transição explícita:

```text
@po → @architect → @dev
```

Portanto:

```yaml
architecture_phase_policy:
  required: true
  adapter_name: architect
  state_name: architect_ratification
  allowed_verdicts:
    - PASS
    - CHANGES_REQUIRED
    - BLOCKED
  on_adapter_missing: "HALT: ARCHITECT_PHASE_UNSUPPORTED"
  on_evidence_missing: "HALT: ARCHITECT_RATIFICATION_MISSING"
  bypass_allowed: false
```

É proibido:

- simular `@architect` dentro do adapter de `@po`;
- interpretar PO `GO` como aprovação arquitetural;
- permitir que `@dev` ratifique a própria solução;
- executar live usando somente o runner atual sem a extensão dessa fase.

O dry-run do workflow pode validar artefatos e demais transições, mas não pode ser declarado arquitetura-completo enquanto esse gap não for resolvido.

## 7. Manifesto imutável

O arquivo YAML de execução deve conter, no mínimo:

```yaml
sdc_execution:
  source_artifact: "docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md"
  design_source: "outputs/design-system/sie-command-center/"
  story_scope: "ordered_story_set"
  execution_mode: "yolo"
  permissions_mode: "auto"
  interaction_policy: "never_prompt"
  on_missing_input: "block_and_log"

  target_branch: "<branch-exata>"
  base_branch: "master"
  remote_repository: "<remote-exato>"
  deploy_environment: "<staging|production|ambiente-existente>"
  deploy_runbook: "<runbook-existente>"

  remote_operations_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: true
  migrations_authorized: false
  destructive_migrations_authorized: false

  max_po_iterations: 3
  max_architect_iterations: 3
  max_qa_iterations: 5

  architecture_phase_required: true
  legacy_preservation_required: true
  feature_flag_required: true
  cli_contract_regression_allowed: false

  required_agents:
    - sm
    - po
    - architect
    - dev
    - qa
    - devops
```

Regras:

- O manifesto é congelado com SHA-256 antes da primeira transição.
- Flags remotas só podem ser `true` quando a autorização prévia correspondente existir.
- Este documento não concede essas autorizações.
- Alterar o manifesto durante a execução causa `MANIFEST_IMMUTABLE_VIOLATION`.
- Produção com qualquer flag necessária em `false` causa `HALT`, nunca prompt.

### 7.1 Coordenação do conjunto de stories

O runner atual executa uma story por run e não percorre nativamente um backlog ordenado. O conjunto completo exige um coordenador pai que:

1. congele o manifesto pai;
2. resolva a ordem de dependências;
3. gere um manifesto filho imutável por story;
4. execute cada filho até estado terminal;
5. só libere o próximo filho após `DEPLOYED` ou estado autorizado equivalente;
6. consolide evidências e efeitos remotos;
7. nunca repita efeitos concluídos durante resume.

```yaml
story_set_coordinator:
  required: true
  mode: sequential
  parent_state: ".aiox/sdc-headless/sie-command-center-master.yaml"
  child_manifest_policy: "immutable_per_story"
  continue_on:
    - deployed
  stop_on:
    - blocked
    - failed
    - rolled_back
  on_coordinator_missing: "HALT: ORDERED_STORY_SET_UNSUPPORTED"
```

É proibido declarar o sistema completo após apenas uma execução individual do runner.

## 8. Backlog-semente para `@sm`

Os itens abaixo são uma decomposição derivada dos artefatos, não são stories prontas. Apenas `@sm` pode transformá-los em stories; apenas `@po` pode liberá-los.

### SIE-DS-00 — Readiness e namespace canônico

Derivar de:

- `.state.yaml`;
- capability gaps do `validation/quality-report.md`;
- plano de adoção.

Resultado esperado:

- decisão ratificada para consumo direto dos outputs ou promoção canônica;
- namespace aditivo definido;
- feature flag e rollback especificados;
- fase executável do `@architect` disponível no SDC headless.

### SIE-DS-01 — Foundations e tokens

Derivar de:

- `tokens/sie-premium.tokens.json`;
- `tokens/sie-premium.css`;
- seção de tokens da arquitetura.

Resultado esperado:

- tokens semânticos consumíveis no produto;
- bindings para primitives aprovadas;
- contraste e estados validados;
- zero alteração visual involuntária no legado.

### SIE-DS-02 — Engineering Shell opt-in

Derivar de:

- `experience-architecture.md`;
- Fase 2 do `adoption-plan.md`;
- shell do protótipo.

Resultado esperado:

- shell novo isolado;
- projeto ativo, navegação, cabeçalho e inspetor;
- variante ativável/desativável;
- `AppShell` atual preservado.

### SIE-DS-03 — Overview, jornada e comandos

Derivar de:

- `OverviewTemplate`;
- `WorkflowStepper`;
- `CommandPalette`;
- comportamento do protótipo.

Resultado esperado:

- visão geral;
- jornada técnica;
- paleta de comandos;
- atalhos com alternativas visíveis;
- dados reais apenas quando fornecidos pelos contratos existentes.

### SIE-DS-04 — List + Inspector

Derivar de:

- `ListInspectorTemplate`;
- módulos Ambientes, Circuitos e Diagnóstico;
- catálogo de componentes.

Resultado esperado:

- grids acessíveis;
- seleção e inspetor sincronizados;
- detalhe progressivo;
- sem duplicar regras de domínio na UI.

### SIE-DS-05 — Parameters + Results e Decision

Derivar de:

- `ParametersResultsTemplate`;
- `DecisionTemplate`;
- módulos Padrão de entrada, Correntes, Condutores e Queda de tensão.

Resultado esperado:

- parâmetros, resultados, motivos e impactos downstream;
- estados com causa e próxima ação;
- contratos CLI/API preservados.

### SIE-DS-06 — Canvas + Inspector para Unifilar

Derivar de:

- `CanvasInspectorTemplate`;
- componentes atuais de `src/components/unifilar/`;
- referência visual do protótipo.

Resultado esperado:

- canvas, toolbar, seleção e propriedades;
- exportação existente preservada;
- alternativa de teclado para interação espacial aplicável.

### SIE-DS-07 — Qualidade integrada e rollout

Derivar de:

- `validation/quality-report.md`;
- fases 3 e 4 do `adoption-plan.md`;
- WCAG 2.2 AA definida nos artefatos.

Resultado esperado:

- regressão visual e funcional;
- teclado, foco, leitor de tela, zoom e reflow;
- documentação/pattern library;
- deploy opt-in;
- rollback verificado;
- legado mantido.

### Ordem

```text
SIE-DS-00
  → SIE-DS-01
    → SIE-DS-02
      → SIE-DS-03
        → SIE-DS-04
          → SIE-DS-05
            → SIE-DS-06
              → SIE-DS-07
```

O `@architect` pode autorizar paralelização apenas após Foundations e somente quando os pacotes não compartilharem arquivos, contratos ou tokens.

## 9. Máquina de estados por story

```text
manifest_validation
  → sm_story_creation
    → po_story_validation
      → architect_ratification
        → dev_implementation
          → qa_review
            → quality_gates
              → devops_pre_push
                → push
                  → pull_request
                    → merge
                      → release
                        → deploy
                          → smoke
                            → deployed
```

### Loops

```text
PO NO-GO
  → @sm corrige
  → @po revalida
  → máximo 3 ciclos

Architect CHANGES_REQUIRED
  → @sm ajusta story/constraints
  → @po revalida
  → @architect reratifica
  → máximo 3 ciclos

QA FAIL
  → @dev corrige
  → @qa requalifica
  → máximo 5 ciclos
```

Limite excedido:

```text
STORY_VALIDATION_EXTERNAL_BLOCKER
ARCHITECT_MAX_ITERATIONS_EXCEEDED
QA_MAX_ITERATIONS_EXCEEDED
```

## 10. Fase A — `@sm` cria a story

Comando preferencial:

```text
@sm
*yolo
*draft
```

O `@sm` deve:

- selecionar o próximo item liberado do backlog-semente;
- criar story em `docs/stories/`;
- rastrear cada AC para os artefatos da seção 3;
- definir IN/OUT, dependências, riscos e rollback;
- declarar arquivos legacy protegidos;
- incluir testes e Definition of Done;
- iniciar checklist e File List;
- definir status `Draft`.

Gate:

- [ ] story pequena o suficiente para um ciclo;
- [ ] critérios testáveis;
- [ ] zero requisito inventado;
- [ ] preservação do legado explícita;
- [ ] dependências e rollback definidos;
- [ ] status `Draft`.

Handoff:

```text
.aiox/handoffs/{story-id}-sm-to-po.yaml
```

## 11. Fase B — `@po` valida

Comando:

```text
@po
*validate-story-draft {story-id}
```

O `@po` verifica:

1. valor e problema;
2. rastreabilidade;
3. critérios testáveis;
4. escopo IN/OUT;
5. dependências;
6. risco e rollback;
7. preservação do legado;
8. Definition of Done;
9. compatibilidade com o conjunto de stories;
10. ausência de requisito inventado.

Resultado:

```text
GO
  → Draft → ReadyForArchitecture
  → handoff automático para @architect

NO-GO
  → permanece Draft
  → feedback estruturado para @sm
```

Handoff:

```text
.aiox/handoffs/{story-id}-po-to-architect.yaml
```

## 12. Fase C — `@architect` ratifica

O `@architect` é autoridade exclusiva desta fase.

Deve ratificar:

- namespace e fronteiras da variante;
- mecanismo opt-in/feature flag;
- convivência com Carbon, Radix/shadcn e Tailwind;
- integração com rotas e contratos existentes;
- consumo dos tokens DTCG;
- composição do shell e templates;
- performance e bundle;
- estratégia de rollback;
- preservação do legado;
- dependências e ordem de implementação.

Vereditos:

```text
PASS
  → ReadyForArchitecture → Ready
  → handoff automático para @dev

CHANGES_REQUIRED
  → retorno para @sm
  → nova validação @po
  → nova ratificação @architect

BLOCKED
  → HALT com evidência e condição de retomada
```

Saída mínima:

```yaml
architecture_verdict:
  story_id: ""
  verdict: "PASS|CHANGES_REQUIRED|BLOCKED"
  namespace: ""
  integration_points: []
  protected_legacy_paths: []
  feature_flag_strategy: ""
  rollback_strategy: ""
  risks: []
  evidence: []
```

Handoff:

```text
.aiox/handoffs/{story-id}-architect-to-dev.yaml
```

## 13. Fase D — `@dev` implementa

Comando:

```text
@dev
*develop-yolo {story-id}
```

Transição:

```text
Ready → InProgress → InReview
```

O `@dev` deve:

- implementar somente a story;
- obedecer ao veredito arquitetural;
- criar arquivos aditivos no namespace ratificado;
- preservar componentes e estilos legacy;
- usar tokens, nunca novos hardcodes;
- não copiar dados ilustrativos do protótipo para produção;
- consumir dados reais pelos contratos existentes;
- criar/atualizar testes;
- atualizar checklist, Dev Agent Record, Change Log e File List;
- não executar push, PR, release ou deploy.

Gate Dev:

- [ ] ACs implementados;
- [ ] testes relevantes passando;
- [ ] nenhum arquivo legacy removido;
- [ ] feature flag/opt-in funcionando;
- [ ] rollback local verificado;
- [ ] nenhuma regra de domínio duplicada;
- [ ] tokens semânticos usados;
- [ ] story `InReview`.

Handoff:

```text
.aiox/handoffs/{story-id}-dev-to-qa.yaml
```

## 14. Fase E — `@qa` qualifica

Comandos:

```text
@qa
*review {story-id}
*gate {story-id}
```

O `@qa` verifica:

- todos os critérios de aceite;
- conformidade com o veredito arquitetural;
- ausência de regressão no legado;
- testes unitários, integração e regressão;
- teclado, foco, nomes acessíveis e semântica;
- reflow, zoom e breakpoints;
- contraste e estados;
- `prefers-reduced-motion`;
- desempenho e segurança aplicáveis;
- checklist e File List;
- gates técnicos.

Vereditos:

```text
PASS
  → InReview → Done
  → handoff para @devops

FAIL
  → InReview → InProgress
  → @dev corrige
  → retorna para @qa

CONCERNS
  → BLOCKED
  → não converter automaticamente em waiver

WAIVED
  → exige waiver previamente autorizado no manifesto
  → sem waiver válido, BLOCKED
```

Handoff:

```text
.aiox/handoffs/{story-id}-qa-to-devops.yaml
```

## 15. Gates técnicos

### 15.1 Root

```text
npm run lint
npm run typecheck
npm test
npm run build
```

### 15.2 Frontend

```text
npm --prefix sistema-de-instala-es-el-tricas-sie-main run lint
npm --prefix sistema-de-instala-es-el-tricas-sie-main run typecheck
npm --prefix sistema-de-instala-es-el-tricas-sie-main test
npm --prefix sistema-de-instala-es-el-tricas-sie-main run build
npm --prefix sistema-de-instala-es-el-tricas-sie-main run build:spa
```

### 15.3 Design e acessibilidade

- [ ] tokens DTCG válidos;
- [ ] zero hardcode novo fora da camada de tokens;
- [ ] contraste WCAG 2.2 AA;
- [ ] foco visível e não oculto;
- [ ] alvos mínimos;
- [ ] alternativa para drag/interação espacial;
- [ ] teclado completo;
- [ ] leitor de tela no fluxo migrado;
- [ ] zoom 200%;
- [ ] 320 px, 768 px e 1280 px;
- [ ] reduced motion;
- [ ] snapshots/regressão visual aprovados;
- [ ] variante desativada reproduz o legado.

### 15.4 CodeRabbit e segurança

- nenhuma issue `CRITICAL`;
- nenhuma credencial ou segredo;
- dependências sem vulnerabilidade bloqueante;
- CSP, sanitização e permissões preservadas quando aplicáveis.

Qualquer falha:

```text
HALT: PRE_SDC_GATE_BLOCKED
```

## 16. Fase F — `@devops` publica e realiza deploy

Somente `@devops` executa esta fase.

### Pre-push

```text
@devops
*pre-push
```

Condições:

- story `Done`;
- QA `PASS`;
- arquitetura `PASS`;
- todos os gates técnicos verdes;
- branch e remote iguais ao manifesto;
- rollback testado;
- feature flag preserva o legado.

### Operações remotas

```text
@devops
*push
*create-pr
*version-check
*release
```

Cada operação exige seu flag independente:

| Operação | Flag |
|---|---|
| push | `remote_operations_authorized` |
| PR | `pull_request_authorized` |
| merge | `merge_authorized` |
| release | `release_authorized` |
| deploy | `deploy_authorized` |
| rollback | `rollback_authorized` |

### Deploy

- usar somente o `deploy_runbook` do manifesto;
- deploy intermediário deve manter a variante opt-in;
- registrar ambiente, URL, commit, versão e horário;
- acompanhar até estado terminal;
- executar smoke tests no legado e na variante.

Falha:

```text
SE rollback_authorized == true:
  executar rollback
  registrar incidente
  terminal = ROLLED_BACK
SENÃO:
  bloquear antes do deploy
  terminal = BLOCKED
```

## 17. Estratégia de entrega das stories

Cada story percorre SM → PO → Architect → Dev → QA → DevOps.

Política recomendada:

```yaml
delivery_policy:
  story_integration: sequential
  deploy_target_before_final_rollout: staging
  feature_flag_default: legacy
  legacy_deletion: forbidden
  final_variant_activation:
    requires:
      - all_stories_done
      - all_qa_pass
      - architect_final_pass
      - full_regression_pass
      - authorized_manifest
```

O último deploy pode publicar a variante completa sem remover o design original. Torná-la padrão exige escopo e autorização explícitos em story própria; não é inferido por este workflow.

## 18. Observabilidade

Persistir estado após cada transição em:

```text
.aiox/sdc-headless/{run-id}.yaml
```

Persistir log legível em:

```text
docs/workflows/logs/SDC-SIE-COMMAND-CENTER-{story-id}-{timestamp}.md
```

Conteúdo mínimo:

```yaml
workflow_state:
  run_id: ""
  manifest_fingerprint: ""
  source_artifact: "docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md"
  story_id: ""
  status: "active|blocked|failed|completed|deployed|rolled_back"
  current_phase: ""
  agents:
    sm: null
    po: null
    architect: null
    dev: null
    qa: null
    devops: null
  verdicts:
    po: null
    architect: null
    qa: null
  counters:
    po_iterations: 0
    architect_iterations: 0
    qa_iterations: 0
  gates:
    lint: null
    typecheck: null
    tests: null
    build: null
    build_spa: null
    accessibility: null
    visual_regression: null
    coderabbit: null
    security: null
    legacy_regression: null
  delivery:
    branch: ""
    commit: ""
    pull_request: ""
    release: ""
    environment: ""
    deploy_status: ""
    rollback_status: ""
```

## 19. Política de erro

| Condição | Ação automática |
|---|---|
| artefato do design ausente | bloquear antes da story |
| adapter de `@architect` ausente | `ARCHITECT_PHASE_UNSUPPORTED` |
| PO `NO-GO` | retornar ao `@sm`, máximo 3 |
| Architect `CHANGES_REQUIRED` | retornar a `@sm` e `@po`, máximo 3 |
| Architect `BLOCKED` | encerrar `BLOCKED` |
| Dev falhou | manter `InProgress` |
| QA `FAIL` | retornar ao `@dev`, máximo 5 |
| QA `CONCERNS` sem waiver | encerrar `BLOCKED` |
| regressão no legado | bloquear deploy |
| gate técnico falhou | bloquear DevOps |
| autorização remota ausente | bloquear antes da operação |
| deploy runbook ausente | `DEPLOY_NOT_CONFIGURED` |
| smoke da variante falhou | rollback |
| smoke do legado falhou | rollback |
| rollback falhou | `ROLLBACK_FAILED` |
| manifesto mudou | `MANIFEST_IMMUTABLE_VIOLATION` |

## 20. Diagrama

```mermaid
flowchart TD
    A[Manifesto validado e congelado] --> B[@sm cria Story Draft]
    B --> C[@po valida]
    C -->|NO-GO| B
    C -->|GO| D[@architect ratifica]
    D -->|CHANGES_REQUIRED| B
    D -->|BLOCKED| X[Terminal BLOCKED]
    D -->|PASS| E[@dev implementa]
    E --> F[@qa review + gate]
    F -->|FAIL| E
    F -->|CONCERNS sem waiver| X
    F -->|PASS| G[Story Done]
    G --> H[@devops pre-push]
    H -->|FAIL| E
    H -->|PASS| I[Push + PR + CI]
    I --> J[Merge + Release]
    J --> K[Deploy autorizado]
    K -->|Falha| L[Rollback]
    K -->|Sucesso| M[Smoke variante + legado]
    M -->|Falha| L
    M -->|PASS| N[Story DEPLOYED]
    N --> O{Mais stories?}
    O -->|Sim| B
    O -->|Não| P[Sistema entregue, legado preservado]
```

## 21. Invocação

### 21.1 Dry-run genérico disponível

```text
node .aiox-core/development/scripts/sdc-headless-yolo.js \
  --manifest <manifest.yaml> \
  --dry-run
```

Esse comando valida o runner atual, mas não comprova a fase arquitetural especializada.

### 21.2 Execução live especializada

Somente após disponibilizar um runtime/adapter que implemente a fase `architect`:

```text
node .aiox-core/development/scripts/sdc-headless-yolo.js \
  --manifest <manifest.yaml> \
  --adapter-module <adapter-module-com-architect.js>
```

O wrapper/adapter deve bloquear live quando:

- `architect` não for função separada;
- `devops` não for função separada;
- qualquer operação não estiver autorizada;
- o fingerprint divergir;
- o runbook não existir.

### 21.3 Prompt para o orquestrador

```text
@aiox-master

Execute integralmente:
docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md

Fonte:
outputs/design-system/sie-command-center/

Modo:
YOLO headless, zero prompts.

Use agentes separados para @sm, @po, @architect, @dev, @qa e @devops.
Não pule a ratificação arquitetural.
Preserve o design original e implemente a variante de forma aditiva e reversível.
Execute uma story por vez na ordem de dependências.
Persista estado e handoffs depois de cada transição.
Não fabrique requisito, aprovação, waiver ou autorização remota.
Continue até DEPLOYED, BLOCKED, FAILED ou ROLLED_BACK.
```

## 22. Critério de conclusão

O conjunto termina como `DEPLOYED` somente quando:

- todas as stories criadas pelo `@sm` estão `Done`;
- todas receberam PO `GO`;
- todas receberam Architect `PASS`;
- todas receberam QA `PASS` ou waiver previamente autorizado;
- root e frontend passaram lint, typecheck, testes e builds;
- acessibilidade e regressão legacy passaram;
- push, PR, merge, release e deploy foram executados por `@devops`;
- smoke tests da variante e do legado passaram;
- ambiente, commit, versão e evidências foram persistidos;
- o design original continua disponível.

Qualquer condição não atendida produz `BLOCKED`, `FAILED` ou `ROLLED_BACK`, nunca sucesso parcial.

## 23. Definition of Done deste workflow

- [x] fontes de verdade identificadas;
- [x] escopo IN/OUT definido;
- [x] backlog-semente rastreável;
- [x] handoffs SM → PO → Architect → Dev → QA → DevOps definidos;
- [x] loops e limites definidos;
- [x] gates de qualidade e acessibilidade definidos;
- [x] preservação do legado definida;
- [x] autorizações remotas separadas;
- [x] deploy e rollback definidos;
- [x] observabilidade e estados terminais definidos;
- [x] gap do runner atual documentado sem bypass;
- [x] coordenador pai do conjunto de stories definido;
- [ ] adapter/runtime com fase `architect` implementado e testado;
- [ ] coordenador `ordered_story_set` implementado e testado;
- [ ] manifesto live autorizado criado;
- [ ] deploy runbook do ambiente confirmado.

---

— Atlas (`@analyst`), mapeando o caminho autônomo do design à produção
