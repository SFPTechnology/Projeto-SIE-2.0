# Workflow SDC Headless — YOLO até Deploy

**Versão:** 2.1  
**Modo:** YOLO headless / zero prompts durante a execução  
**Escopo:** Story Creation → Validation → Development → QA → DevOps → Deploy  
**Fonte canônica:** `.aiox-core/development/workflows/story-development-cycle.yaml`  
**Cadeia de comandos:** `.aiox-core/data/workflow-chains.yaml`  
**Conformidade:** `.aiox-core/constitution.md`

> **Limite inegociável:** execução sem intervenção humana não significa execução sem controle. Constitution, Agent Authority, Story-Driven Development, No Invention e Quality First permanecem ativos. O workflow automatiza decisões e correções dentro dessas regras; não fabrica aprovações, não transforma falha em sucesso e não concede autorização remota global.

> **Natureza deste artefato:** este `.md` é o contrato de orquestração headless do SDC. O YAML canônico `story-development-cycle.yaml` implementa nativamente as quatro primeiras fases, até QA. A Fase 5 deste documento estende o ciclo com os comandos existentes de `@devops` e com o pipeline/runbook de deploy já aprovado. Portanto, executar apenas o YAML canônico não realiza deploy.

## 1. Objetivo

Executar automaticamente todas as stories liberadas de um PRD ou épico e produzir códigos, testes, migrations, artefatos de entrega e operações remotas, preservando as autoridades do AIOX:

```text
@sm cria
  → @po valida
    → @dev implementa
      → @qa revisa e qualifica
        → @dev corrige, se necessário
          → @devops executa gates, push, PR, release e deploy configurado
```

Depois que um manifesto de execução válido for fornecido, o orquestrador não pode pedir confirmação, seleção ou feedback humano. Toda decisão rotineira deve ser resolvida pelos agentes autorizados e toda falha deve seguir roteamento determinístico.

O modo YOLO headless não ignora:

- requisitos ou gates bloqueantes do PRD/épico;
- Story-Driven Development;
- separação de autoridade entre agentes;
- `lint`, `typecheck`, testes, build e CodeRabbit;
- falhas de segurança, CI, deploy ou rollback;
- autorização declarativa prévia para operações remotas e produção;
- limites de escopo do repositório, branch, ambiente e runbook registrados no manifesto.

## 2. Entradas obrigatórias

Antes da execução, o orquestrador deve resolver e registrar:

```yaml
sdc_execution:
  source_artifact: "<caminho do PRD ou épico aprovado>"
  story_scope: "all_unblocked"
  execution_mode: "yolo"
  permissions_mode: "auto"
  interaction_policy: "never_prompt"
  on_missing_input: "block_and_log"
  target_branch: "<branch de trabalho>"
  base_branch: "<branch de integração>"
  deploy_environment: "<staging|production|outro ambiente existente>"
  deploy_runbook: "<caminho do pipeline ou runbook já aprovado>"
  remote_repository: "<remote exato autorizado>"
  remote_operations_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: true
  migrations_authorized: false
  destructive_migrations_authorized: false
  max_qa_iterations: 5
```

Regras:

- O manifesto é imutável durante a execução e vale somente para o repositório, branches e ambiente declarados.
- `source_artifact` deve existir e autorizar o desdobramento em stories.
- `deploy_runbook` deve apontar para uma automação ou procedimento existente; não pode ser inventado.
- `remote_operations_authorized: true` representa autorização prévia para push no remote declarado.
- PR, merge, release, deploy e migrations exigem seus próprios flags `true`.
- `destructive_migrations_authorized: false` mantém proibidas operações destrutivas; quando `true`, ainda exige backup verificável e rollback ensaiado.
- `deploy_authorized: true` representa autorização prévia e explícita para o ambiente informado.
- Produção sem autorização registrada causa `HALT: DEPLOY_AUTHORIZATION_MISSING`.
- Campo obrigatório ausente causa `HALT` e log automático; nunca causa prompt.

### 2.1 Política headless

```yaml
headless_policy:
  prompts: 0
  ask_user: forbidden
  manual_route_fallback: forbidden
  agent_handoffs: automatic
  routine_decisions: automatic
  external_authority_missing: block_and_log
  retries:
    task_error: 2
    story_validation: until_go_or_external_blocker
    qa: 5
    deployment: 1
  terminal_states:
    - deployed
    - blocked
    - failed
    - rolled_back
```

`blocked`, `failed` e `rolled_back` são resultados autônomos válidos. O workflow não promete `deployed` quando requisitos, qualidade, autorização ou infraestrutura não permitem.

## 3. Pré-condições bloqueantes

O workflow só inicia Story Creation quando todos os itens aplicáveis estiverem verdadeiros:

- [ ] PRD/épico aprovado para implementação.
- [ ] Gates anteriores às stories resolvidos.
- [ ] Escopo e dependências dos pacotes identificados.
- [ ] Critérios de aceite rastreáveis.
- [ ] Arquitetura necessária aprovada por `@architect`.
- [ ] Não existe story anterior incompleta que bloqueie a próxima.
- [ ] Branch e repositório corretos identificados.
- [ ] Mudanças preexistentes do usuário foram inventariadas e serão preservadas.
- [ ] Manifesto headless contém autorizações e alvos exatos.
- [ ] Pipeline/runbook de deploy existe para o ambiente solicitado.

Falha em qualquer pré-condição:

```text
HALT: PRE_SDC_GATE_BLOCKED
Registrar evidência, gate, autoridade responsável e condição de retomada.
Não criar story implementável e não alterar código.
Não solicitar intervenção humana durante esta execução.
```

## 4. Estados canônicos

```text
Draft
  → Ready
    → InProgress
      → InReview
        → Done
```

Autoridades:

| Transição | Autoridade |
|---|---|
| backlog/artefato → `Draft` | `@sm` ou `@po` |
| `Draft` → `Ready` | `@po` |
| `Ready` → `InProgress` | `@dev` |
| `InProgress` → `InReview` | `@dev` |
| `InReview` → `Done` | `@qa`, após gate |
| push, PR, release, tag e publicação remota | somente `@devops` |

## 5. Algoritmo autônomo

```text
VALIDAR pré-condições
VALIDAR manifesto e escopo remoto
ORDENAR stories/pacotes por dependência

PARA CADA item liberado:
  FASE 1 — @sm cria/refina story
  FASE 2 — @po valida story
    SE NO-GO:
      retornar para @sm
      repetir até GO ou bloqueio externo

  FASE 3 — @dev implementa em YOLO
  FASE 4 — @qa revisa e emite gate
    SE FAIL:
      retornar para @dev
      aplicar correções
      repetir QA, máximo 5 iterações
    SE CONCERNS:
      encaminhar automaticamente ao @po
      se @po exigir correção, retornar ao @dev
      repetir até PASS, waiver autorizada ou bloqueio
    SE WAIVED:
      validar artefato de waiver
      não liberar deploy se waiver não autorizar publicação
    SE PASS:
      marcar story Done

SE todas as stories do escopo estiverem Done e com QA PASS:
  FASE 5 — @devops executa pre-push, push, PR, CI, release e deploy configurado
SENÃO:
  registrar estado terminal correspondente sem prompt
```

## 6. Fase 1 — Story Creation por `@sm`

Comando preferencial:

```text
@sm
*yolo
*draft
```

Responsabilidades:

- criar a story em `docs/stories/`;
- derivar conteúdo somente do PRD/épico e artefatos aprovados;
- definir título, problema, valor, escopo IN/OUT e dependências;
- criar critérios de aceite testáveis;
- incluir riscos, rollback, testes e Definition of Done;
- prever agentes especializados e CodeRabbit quando aplicável;
- iniciar em `Draft`;
- registrar checklist e File List inicial.

Gate de saída:

- [ ] Story rastreável ao PRD/épico.
- [ ] Critérios de aceite claros e verificáveis.
- [ ] Dependências e ordem de execução definidas.
- [ ] Nenhum requisito inventado.
- [ ] Status `Draft`.

Em caso de falha, manter `Draft` e registrar `STORY_DRAFT_INCOMPLETE`.

## 7. Fase 2 — Story Validation por `@po`

Comando:

```text
@po
*validate-story-draft {story-id}
```

Checklist obrigatório:

1. Título claro.
2. Problema ou necessidade completos.
3. Critérios de aceite testáveis.
4. Escopo IN/OUT delimitado.
5. Dependências mapeadas.
6. Complexidade coerente.
7. Valor de negócio identificado.
8. Riscos documentados.
9. Definition of Done completa.
10. Alinhamento com PRD/épico.

Roteamento:

```text
10/10 e GO
  → Draft → Ready
  → handoff para @dev

NO-GO
  → permanece Draft
  → feedback estruturado para @sm
  → repetir Fases 1–2
```

Se o mesmo bloqueio externo se repetir sem nova evidência, encerrar a repetição com:

```text
HALT: STORY_VALIDATION_EXTERNAL_BLOCKER
```

Não perguntar ao usuário se deseja aceitar risco. Em modo headless, risco não autorizado mantém a story em `Draft` e encerra a execução como `blocked`.

## 8. Fase 3 — Implementação por `@dev`

Comando:

```text
@dev
*develop-yolo {story-id}
```

Transições:

```text
Ready → InProgress → InReview
```

Responsabilidades:

- implementar somente tasks e critérios da story;
- preservar alterações preexistentes não relacionadas;
- priorizar CLI → observabilidade → UI;
- criar ou atualizar testes;
- implementar migrations previstas pela story quando `migrations_authorized: true`;
- criar rollback de migration e validar apply → rollback → reapply;
- executar testes proporcionais ao risco durante o desenvolvimento;
- atualizar checkboxes, Dev Agent Record, Change Log e File List;
- executar o self-healing do CodeRabbit quando configurado;
- não executar push, PR, release ou deploy.

Gate de saída do Dev:

- [ ] Todos os critérios de aceite implementados.
- [ ] Nenhuma task obrigatória pendente.
- [ ] Testes locais relevantes passando.
- [ ] `npm run lint` passando.
- [ ] `npm run typecheck` passando.
- [ ] `npm test` passando.
- [ ] `npm run build` passando.
- [ ] Migrations aplicadas em ambiente de teste, revertidas e reaplicadas de forma determinística, quando aplicável.
- [ ] Nenhuma migration destrutiva executada sem autorização específica, backup e rollback comprovados.
- [ ] CodeRabbit sem issue `CRITICAL`.
- [ ] Checklist e File List atualizados.
- [ ] Status `InReview`.

Qualquer falha mantém a story em `InProgress` e bloqueia QA.

## 9. Fase 4 — Review e Quality Gate por `@qa`

Comandos:

```text
@qa
*review {story-id}
*gate {story-id}
```

O QA verifica:

- código, padrões, legibilidade e manutenibilidade;
- critérios de aceite e rastreabilidade;
- testes unitários, integração e regressão;
- segurança e riscos de perda de dados;
- desempenho e NFRs aplicáveis;
- documentação, checklist e File List;
- lint, typecheck, testes, build e CodeRabbit.

Roteamento:

```text
PASS
  → InReview → Done
  → story elegível para handoff DevOps

FAIL
  → InReview → InProgress
  → @dev *apply-qa-fixes
  → @dev devolve a story para InReview
  → repetir @qa *review e *gate

CONCERNS
  → registrar concerns
  → encaminhar automaticamente ao agente @po
  → corrigir até PASS ou materializar waiver autorizada

WAIVED
  → registrar waiver, autoridade, justificativa e validade
  → bloquear deploy automático se o waiver não autorizar publicação
```

Loop Dev ↔ QA:

```yaml
qa_loop:
  max_iterations: 5
  on_exhausted: "HALT: QA_MAX_ITERATIONS_EXCEEDED"
  required_output:
    - qa_report
    - gate_verdict
    - unresolved_issues
    - quality_score
```

O loop não solicita decisão humana. Ao atingir o limite, registra `QA_MAX_ITERATIONS_EXCEEDED` e encerra como `blocked`.

### 9.1 Qualificação de migrations

Quando uma story altera schema ou dados:

```text
@data-engineer avalia desenho, consistência, RLS, índices e reversibilidade
  → @dev implementa migration e rollback na story
    → @qa executa apply, validação, rollback e reapply
      → @devops executa no pipeline autorizado somente após QA PASS
```

Gates adicionais:

- [ ] backup/snapshot criado e validado;
- [ ] migration idempotente ou protegida contra reaplicação;
- [ ] rollback preserva significado e dados;
- [ ] RLS e acesso testados;
- [ ] tempo de lock e impacto operacional avaliados;
- [ ] migration destrutiva possui autorização específica no manifesto.

## 10. Fechamento do conjunto de stories

Antes do handoff para DevOps:

- [ ] Todas as stories selecionadas estão `Done`.
- [ ] Todas possuem QA `PASS`, salvo autorização formal aplicável.
- [ ] Todos os gates do PRD/épico estão aprovados para o marco.
- [ ] Não existem dependências ou migrations pendentes.
- [ ] Documentação e changelog foram atualizados.
- [ ] O candidato exato da entrega está identificável.
- [ ] Todas as migrations aplicáveis possuem QA PASS e rollback comprovado.

Se houver mais stories liberadas, retornar à Fase 1.  
Se não houver, iniciar a Fase 5.

## 11. Fase 5 — DevOps, publicação e deploy

Somente `@devops` executa esta fase.

O handoff para DevOps é automático. Nenhum outro agente pode executar operações remotas.

### 11.1 Pre-push

```text
@devops
*pre-push
```

Gate obrigatório:

```text
npm run lint
npm run typecheck
npm test
npm run build
CodeRabbit
security checks
story status
```

Qualquer `FAIL` bloqueia publicação e retorna o problema ao agente responsável.

### 11.2 Push e Pull Request

Após `pre-push = PASS`:

```text
@devops
*push
*create-pr
```

Condições:

- branch remota correta;
- nenhuma credencial ou segredo versionado;
- CI obrigatória verde;
- reviews e políticas da branch atendidos;
- merge realizado conforme a política do repositório.
- `remote_operations_authorized`, `pull_request_authorized` e `merge_authorized` estão `true`.

Se qualquer flag estiver `false`, registrar o bloqueio correspondente sem solicitar aprovação.

### 11.3 Release

Após merge e CI verde:

```text
@devops
*version-check
*release
```

O release deve registrar versão semântica, changelog, commit e artefato exato.
`release_authorized` deve estar `true`; caso contrário, `HALT: RELEASE_AUTHORIZATION_MISSING`.

### 11.4 Deploy

Não existe comando AIOX canônico `*deploy` no agente `@devops`. O deploy deve ser acionado pelo pipeline ou runbook informado em `deploy_runbook`.

```text
SE deploy_runbook não existe:
  HALT: DEPLOY_NOT_CONFIGURED

SE ambiente é production E deploy_authorized != true:
  HALT: DEPLOY_AUTHORIZATION_MISSING

SENÃO:
  @devops executa o pipeline/runbook aprovado
  acompanha o status até terminal
  registra URL/ambiente, versão, commit e horário
```

Nenhuma confirmação é solicitada durante push, PR, merge, release ou deploy. A autorização vem exclusivamente do manifesto imutável validado no início.

### 11.5 Validação pós-deploy

- [ ] Health check aprovado.
- [ ] Smoke tests aprovados.
- [ ] Versão e commit conferidos.
- [ ] Logs e métricas sem erro crítico.
- [ ] Funcionalidade principal validada por CLI.
- [ ] Observabilidade operacional ativa.

Falha pós-deploy:

```text
@devops executa rollback do runbook aprovado
registra incidente e evidências
marca execução como DEPLOY_ROLLED_BACK
não tenta novo deploy sem corrigir a causa
```

Se `rollback_authorized: true`, o rollback é automático. Se for `false`, o workflow interrompe antes do deploy porque não existe recuperação autorizada.

## 12. Estado e observabilidade

Persistir um log em:

```text
docs/workflows/logs/SDC-{epic-or-prd}-{timestamp}.md
```

Conteúdo mínimo:

```yaml
workflow_state:
  source_artifact: ""
  mode: "yolo"
  started_at: ""
  completed_at: ""
  status: "active|blocked|completed|deployed|rolled_back"
  current_story: ""
  current_phase: ""
  stories:
    - id: ""
      status: "Draft|Ready|InProgress|InReview|Done"
      po_score: null
      qa_verdict: null
      qa_iterations: 0
  quality_gates:
    lint: null
    typecheck: null
    tests: null
    build: null
    coderabbit: null
    security: null
    migrations: null
  delivery:
    branch: ""
    commit: ""
    pull_request: ""
    release: ""
    environment: ""
    deployment_status: ""
  authorization_manifest:
    remote_repository: ""
    remote_operations_authorized: false
    pull_request_authorized: false
    merge_authorized: false
    release_authorized: false
    deploy_authorized: false
    rollback_authorized: false
    migrations_authorized: false
    destructive_migrations_authorized: false
```

## 13. Política de erros

| Condição | Ação automática |
|---|---|
| PRD/épico não aprovado | bloquear antes da criação de story |
| Story NO-GO | retornar para `@sm` |
| Dev gate falhou | permanecer `InProgress` |
| QA `FAIL` | retornar para `@dev`, máximo 5 ciclos |
| QA `CONCERNS` | bloquear deploy e encaminhar ao `@po` |
| Issue CodeRabbit `CRITICAL` | bloquear push |
| CI falhou | bloquear merge/release |
| Deploy não configurado | bloquear em DevOps |
| Autorização de produção ausente | bloquear antes do deploy |
| Smoke/health falhou | rollback e incidente |
| Campo obrigatório ausente | bloquear e registrar, sem prompt |
| Operação remota não autorizada no manifesto | bloquear antes da operação |
| Migration falhou | rollback automático e retorno ao `@dev` |
| Migration destrutiva sem autorização específica | bloquear antes da execução |

YOLO nunca transforma `BLOCK` em `PASS`.

## 14. Diagrama

```mermaid
flowchart TD
    A[PRD ou épico aprovado] --> B[@sm cria Story Draft]
    B --> C[@po valida 10/10]
    C -->|NO-GO| B
    C -->|GO: Ready| D[@dev develop-yolo]
    D --> E[InReview]
    E --> F[@qa review + gate]
    F -->|FAIL| G[@dev apply-qa-fixes]
    G --> E
    F -->|CONCERNS| H[@po decide / Dev corrige]
    H --> E
    F -->|PASS| I[Story Done]
    I --> J{Mais stories?}
    J -->|Sim| B
    J -->|Não| K[@devops pre-push]
    K -->|FAIL| L[Retornar ao agente responsável]
    L --> K
    K -->|PASS| M[@devops push + PR]
    M --> N[CI + merge autorizado]
    N --> O[@devops release]
    O --> P[Pipeline/runbook autorizado]
    P -->|Falha| Q[Rollback + incidente]
    P -->|Sucesso| R[Smoke + health + observabilidade]
    R --> S[Workflow Deployed]
```

## 15. Invocação recomendada

Implementação CLI determinística adicionada pela story `SDC-AUTO-1`:

```text
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest <manifest.yaml> --dry-run
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest <manifest.yaml> --adapter-module <adapters.js>
```

O `--dry-run` usa adapters simulados para operações remotas. Em execução real, o wrapper bloqueia execução sem `--adapter-module`; `@devops` deve fornecer adapters/runbook autorizados. O runner também bloqueia qualquer operação cujo flag do manifesto não esteja `true`.

O comando nativo abaixo inicia somente o ciclo canônico SM → PO → Dev → QA e o executa passo a passo:

```text
@aiox-master
*run-workflow story-development-cycle start --mode=engine
```

Esse comando, isoladamente, não é headless até deploy: o engine persiste o estado e encerra após cada etapa, exigindo novas invocações de `continue`. O YAML canônico registra DevOps Publication como Fase 5, e o modo zero-prompt até deploy usa a extensão `story-development-cycle-headless-yolo`. Para executar o contrato completo deste documento sem prompts intermediários, o orquestrador deve receber:

```text
@aiox-master
Execute integralmente o workflow
docs/workflows/WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md
para <PRD-ou-épico>, em modo YOLO.

Use agentes separados para @sm, @po, @dev, @qa e @devops.
Carregue um manifesto de execução completo e imutável.
Não peça confirmação, seleção ou feedback humano durante a execução.
Preserve todos os gates BLOCK.
Automatize stories, código, testes, migrations e operações remotas dentro do manifesto.
Não execute operação remota fora do repositório, branches, ambiente ou flags autorizados.
Continue até deployed, rolled_back ou blocked com evidência.
```

## 16. Critério de conclusão

O workflow só termina como `DEPLOYED` quando:

- todas as stories do escopo estão `Done`;
- QA aprovou os trabalhos;
- pre-push e CI passaram;
- push, PR, merge e release foram registrados;
- o pipeline/runbook realizou o deploy;
- health check e smoke tests passaram;
- versão, commit, ambiente e evidências foram persistidos.

Qualquer outro resultado deve ser registrado como `BLOCKED`, `FAILED` ou `ROLLED_BACK`, nunca como sucesso parcial.

## 17. Garantia de não intervenção

Durante uma execução válida:

- nenhum agente pode chamar mecanismo de pergunta ao usuário;
- nenhum passo pode pausar aguardando confirmação;
- decisões de produto, arquitetura, qualidade e operação são tomadas pelos respectivos agentes;
- correções retornam automaticamente ao agente responsável;
- estado é persistido após cada transição;
- operações remotas são executadas exclusivamente por `@devops`;
- ausência de evidência ou autorização encerra como `blocked`, sem intervenção;
- falha de deploy aciona rollback automático quando previamente autorizado.

O workflow entrega todas as stories, códigos, migrations e operações remotas que forem aprovadas pelos gates e autorizadas pelo manifesto. Não há garantia legítima de entrega quando os próprios artefatos exigidos estão ausentes ou falham.

---

— Atlas (@analyst), mapeando o fluxo de entrega
