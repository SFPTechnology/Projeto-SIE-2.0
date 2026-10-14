# Workflow SDC Headless YOLO — Auto-otimização → S (mm²) no MOD-QT

**Versão:** 1.0  
**Data:** 2026-08-02  
**Modo:** SDC automático headless YOLO, sem prompts durante a execução  
**Escopo:** Brownfield fullstack — MOD-DC, persistência, CLI/API, MOD-QT e UI  
**Fonte normativa:** `docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md`  
**Story sucessora sugerida:** `AUTO-OTI-1.3`, com identificador final sob autoridade de `@sm`/`@po`  
**Contrato SDC-base:** `docs/workflows/WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md`  
**Workflow executável-base:** `.aiox-core/development/workflows/story-development-cycle-headless-yolo.yaml`  
**Status:** contrato de orquestração pronto; execução condicionada ao manifesto, à story e às decisões da Fase 0

> **Regra inegociável:** YOLO significa zero prompts e roteamento automático, não ausência de controle. O workflow não inventa decisões, não transforma `BLOCK` em `PASS`, não apresenta persistência volátil como durável e não executa operação remota fora das autorizações do manifesto.

> **Natureza deste arquivo:** este documento define a orquestração específica para executar todas as fases 0–7 do plano. A execução real exige um manifesto compatível com o runner SDC e, para efeitos externos, adapters autorizados. A criação desses artefatos executáveis não está implícita na criação deste `.md`.

## 1. Decisão IDS — reutilização antes de criação

O registro de workflows foi consultado antes da definição deste fluxo.

| Artefato avaliado | Similaridade funcional | Decisão |
|---|---:|---|
| `WORKFLOW-SDC-AUTOMATICO-YOLO-DEPLOY.md` | Alta no ciclo SM → PO → Dev → QA → DevOps | Reutilizar como contrato-base |
| `WORKFLOW-SDC-MOD-QT-INTEGRAL-PERMANENTE-YOLO.md` | Alta na especialização MOD-QT, handoffs e gates | Adaptar estrutura |
| `story-development-cycle-headless-yolo.yaml` | Alta no motor, checkpoints e autorizações | Reutilizar como workflow executável-base |

**Resultado IDS:** `ADAPT`. Este arquivo especializa o SDC existente; não cria um segundo motor de orquestração.

## 2. Objetivo operacional

Conduzir automaticamente a criação e validação da story, as decisões de arquitetura, dados e UX, a implementação, os testes, a revisão de qualidade e a entrega controlada necessárias para que:

1. uma seção aprovada e explicitamente aplicada na Auto-otimização do MOD-DC seja persistida por projeto/circuito;
2. somente uma seção automática durável, vigente e compatível abasteça `S (mm²)` no MOD-QT;
3. o override manual auditado continue prevalecendo e possa ser removido posteriormente;
4. valores obsoletos, voláteis ou incompatíveis nunca sejam apresentados como vigentes;
5. o fluxo completo funcione primeiro por CLI/API, sem React, navegador ou `localStorage`;
6. contratos públicos e fórmulas dos motores MOD-DC/MOD-QT permaneçam compatíveis.

Fluxo resumido:

```text
@aiox-master valida e congela o manifesto
  → @sm cria/refina a story sucessora
    → @architect + @data-engineer decidem contrato, concorrência e migration
      → @po + @ux aprovam a semântica explícita do lote
        → @qa define a estratégia de testes
          → @po valida a story consolidada como Ready
            → @dev implementa as fases 1–6
              → @data-engineer valida migration/RLS/concorrência
                → @qa revisa AC1–AC12 e NFRs
                  → @dev corrige, se necessário
                    → @devops publica e executa rollout somente quando autorizado
```

## 3. Princípios e invariantes

Durante toda a execução:

- obedecer à Constitution e a `CLI First → Observability Second → UI Third`;
- trabalhar exclusivamente por uma nova story sucessora, sem ampliar `MOD-QT-2-06`;
- usar o plano fonte como limite de requisito, sem criar fórmula ou regra normativa nova;
- preservar mudanças preexistentes e não relacionadas na worktree;
- manter `servico-queda-tensao.ts` como autoridade da precedência do MOD-QT;
- usar o mesmo caso de uso de aplicação em CLI/API e UI;
- aceitar como **Aplicado** somente resultado com persistência `DURAVEL`;
- garantir atomicidade, idempotência e concorrência explícita;
- gerar a assinatura canônica no domínio/aplicação, nunca na UI;
- não promover dados de `localStorage` para a persistência durável;
- não editar destrutivamente a migration `0011` já aplicada;
- manter o fallback volátil restrito a desenvolvimento/teste e explicitamente sinalizado;
- manter o override manual auditado acima da seção automática vigente;
- manter `—` e `PEND` quando não existir fonte válida;
- preservar fórmulas C1–C6 e fórmulas de queda de tensão;
- reservar push, PR, merge, release e deploy exclusivamente a `@devops`.

## 4. Entradas obrigatórias e manifesto imutável

O orquestrador deve receber um manifesto separado, recomendado em:

```text
docs/workflows/MANIFEST-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.yaml
```

Contrato mínimo:

```yaml
sdc_execution:
  source_artifact: docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md
  orchestration_workflow: docs/workflows/WORKFLOW-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.md
  story_scope: single_successor_story
  provisional_story_id: AUTO-OTI-1.3
  execution_mode: yolo
  permissions_mode: auto
  interaction_policy: never_prompt
  on_missing_input: block_and_log
  max_po_iterations: 3
  max_qa_iterations: 5

  base_branch: "<branch-base existente>"
  target_branch: "<branch de trabalho autorizada>"
  remote_repository: "<remote exato autorizado>"
  deploy_environment: "<staging|production|ambiente existente>"
  deploy_runbook: "<pipeline ou runbook existente>"

  remote_operations_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: true
  migrations_authorized: false
  destructive_migrations_authorized: false

  required_decisions:
    persistence_and_concurrency: pending
    batch_confirmation_semantics: pending
    cli_api_entrypoint_and_schemas: pending

  protected_contracts:
    - RetornoMODQT
    - ValidarMODQTSchema
    - RetornoMODQTSchema
    - POST /api/v1/modulos/mod-qt/validar
```

Regras do manifesto:

- validar, calcular fingerprint e congelar antes da primeira transição;
- registrar hash da fonte normativa para detectar mudança durante a execução;
- resolver branch, remote, ambiente e runbook sem valores implícitos;
- manter flags remotos `false` por padrão;
- exigir `migrations_authorized: true` antes de apply em qualquer banco;
- manter `destructive_migrations_authorized: false`, pois o plano exige migration aditiva;
- bloquear, sem perguntar, quando um campo obrigatório estiver ausente;
- reiniciar o preflight se o plano fonte mudar após o snapshot.

## 5. Autoridades e entregáveis

| Agente | Autoridade neste workflow | Entregável mínimo |
|---|---|---|
| `@aiox-master` | Orquestração, validação do manifesto, checkpoints, roteamento e retomada | Snapshot, estado, log e handoffs |
| `@sm` | Criação/refino da story sucessora | Story `Draft` completa e rastreável |
| `@architect` | Contrato headless, assinatura, limites de domínio e estratégia de concorrência | Decisão arquitetural registrada |
| `@data-engineer` | Modelo persistente, migration, atomicidade, RLS, rollback e testes de concorrência | Parecer de dados e gate de migration |
| `@ux-design-expert` | Semântica de confirmação individual/lote e estados visuais | Decisão UX documentada |
| `@po` | Validação da story e decisão de produto sobre lote/waivers | Story `Ready` ou `NO-GO` fundamentado |
| `@qa` | Estratégia de testes, revisão independente e quality gate | Relatório e gate `PASS/FAIL/CONCERNS/WAIVED` |
| `@dev` | Implementação da story, testes, migration autorizada e documentação | Código e story em `InReview` |
| `@devops` | Pre-push, operações remotas, migration em ambiente, release, deploy e rollback | Evidências de publicação/rollout |

Nenhum agente pode aprovar a própria saída em uma fronteira de autoridade.

## 6. Estados do workflow

```text
MANIFEST_VALIDATION
  → BASELINE_CAPTURE
    → STORY_DRAFT
      → ARCHITECTURE_DECISION
        → DATA_DECISION
          → PRODUCT_UX_DECISION
            → QA_TEST_DESIGN
              → STORY_VALIDATION
                → IMPLEMENTATION_PHASE_1
                  → IMPLEMENTATION_PHASE_2
                    → IMPLEMENTATION_PHASE_3
                      → IMPLEMENTATION_PHASE_4
                        → IMPLEMENTATION_PHASE_5
                          → IMPLEMENTATION_PHASE_6
                            → DEV_LOCAL_GATES
                              → DATA_FINAL_GATE
                                → QA_REVIEW
                                  → QA_GATE
                                    → DEVOPS_PRE_PUSH
                                      → PUBLICATION_AND_ROLLOUT
                                        → POST_DEPLOY_SMOKE
                                          → DEPLOYED
```

Estados terminais válidos:

- `DEPLOYED`: execução real autorizada, rollout e smoke aprovados;
- `BLOCKED`: requisito, decisão, gate ou autorização obrigatório ausente;
- `FAILED`: erro não recuperável após as tentativas previstas;
- `ROLLED_BACK`: rollout falhou e o rollback autorizado foi concluído.

Os loops `@sm ↔ @po` e `@dev ↔ @qa` são controlados por contador, motivo e evidência; não são ciclos ilimitados.

## 7. Algoritmo automático

```text
VALIDAR manifesto, paths, autorizações e fonte normativa
CONGELAR snapshot e fingerprint
INVENTARIAR worktree e baseline sem alterar trabalho alheio

@sm CRIA story sucessora em Draft
@architect DECIDE contrato, assinatura e concorrência
@data-engineer VALIDA modelo, migration, operação atômica, rollback e RLS
@po + @ux-design-expert DECIDEM semântica explícita do lote
@qa DEFINE matriz AC/NFR → testes e riscos
@sm CONSOLIDA as decisões na story
@po VALIDA a story

SE NO-GO:
  RETORNAR para @sm, no máximo 3 iterações
SE decisão condicionante estiver pendente:
  HALT com o código específico
SE GO:
  TRANSICIONAR Draft → Ready

@dev EXECUTA fases técnicas 1–6 na ordem
APÓS cada fase:
  EXECUTAR testes focados e persistir evidência
  BLOQUEAR avanço se o gate da fase falhar

@data-engineer REVALIDA migration, RLS, atomicidade e concorrência
@dev EXECUTA gates locais completos e atualiza a story
@qa REEXECUTA evidências e emite gate

SE QA FAIL:
  RETORNAR para @dev
  APLICAR correções dentro da story
  REPETIR, no máximo 5 iterações
SE QA CONCERNS:
  ENCAMINHAR automaticamente à autoridade indicada
  SÓ avançar com correção ou waiver formal que autorize publicação
SE QA PASS:
  TRANSICIONAR InReview → Done

@devops EXECUTA pre-push
SE flags remotos não autorizarem a próxima operação:
  HALT sem prompt e registrar condição de retomada
SENÃO:
  EXECUTAR push → PR → CI → merge → release → migration → deploy → smoke

SE deploy/smoke falhar E rollback_authorized = true:
  EXECUTAR rollback e registrar ROLLED_BACK
SE tudo passar:
  REGISTRAR DEPLOYED
```

## 8. Fase 0 — Decisões, baseline e story Ready

### 8.1 Preflight e baseline — `@aiox-master`

Executar verificações somente leitura:

- confirmar a existência do plano, da Constitution e do contrato SDC-base;
- confirmar que `AUTO-OTI-1.2` e `MOD-QT-2-06` permanecem artefatos predecessores, não alvos de expansão;
- capturar `git status`, branch, submódulos e mudanças preexistentes;
- reproduzir o cenário dos screenshots e registrar seção base, seção otimizada, origem, assinatura, persistência e valor atual no MOD-QT;
- registrar a suíte de testes e os gates disponíveis;
- criar snapshot/fingerprint do manifesto e do plano.

Falha bloqueante: `HALT: PRE_SDC_GATE_BLOCKED`.

### 8.2 Story draft — `@sm`

Comando lógico:

```text
@sm *draft AUTO-OTI-1.3 --source docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md --mode yolo
```

A story deve:

- referenciar `AUTO-OTI-1.2` e `MOD-QT-2-06` como predecessoras;
- conter AC1–AC12, NFRs, escopo IN/OUT, riscos e rollback do plano;
- preservar a terminologia Calculado/Aprovado/Aplicado/Persistido/Vigente/Obsoleto/Manual MOD-QT;
- declarar os contratos públicos protegidos;
- separar decisões de arquitetura, dados e UX das tasks de implementação;
- iniciar em `Draft` e ter checklist/File List inicial.

### 8.3 Decisão de arquitetura — `@architect`

Registrar antes de código:

1. fronteira e nome final do caso de uso headless;
2. entrypoint CLI/API e schemas de entrada/saída;
3. composição canônica e determinística da assinatura;
4. estratégia persistente entre linha por projeto/circuito ou merge JSONB atômico;
5. controle de versão, conflito e idempotência por `operacaoId`;
6. sequência de invalidação e leitura pelo MOD-QT;
7. compatibilidade dos contratos protegidos.

Falha bloqueante: `HALT: ARCHITECTURE_DECISION_MISSING`.

### 8.4 Decisão de dados — `@data-engineer`

Validar e registrar:

- modelo lógico por projeto/circuito, versão, origem, assinatura e estado;
- migration aditiva posterior à `0011`;
- estratégia para dados legados sem assinatura;
- operação de lote atômica e retry idempotente;
- concorrência entre circuitos diferentes e no mesmo circuito;
- rollback, compatibilidade de leitura, índices e impacto de lock;
- RLS e validação de pertencimento projeto/circuito;
- tratamento explícito do risco caso uma policy permissiva precise ser mantida.

Falha bloqueante: `HALT: DATA_DECISION_MISSING`.

### 8.5 Decisão de produto/UX — `@po` + `@ux-design-expert`

Escolher e documentar uma semântica inequívoca:

- **Otimizar e aplicar todos ({n})**; ou
- **Otimizar todos** seguido de confirmação consolidada **Aplicar {n} seções aprovadas**.

A decisão deve preservar:

- confirmação explícita individual e de lote;
- indicação separada de calculados, aprovados, persistidos, ignorados, conflitos e falhas;
- estado visual “aplicado” somente após `DURAVEL`;
- edição manual posterior, justificativa e auditoria no MOD-QT.

Falha bloqueante: `HALT: BATCH_CONFIRMATION_UNDECIDED`.

### 8.6 Estratégia de testes antecipada — `@qa`

Quinn deve transformar AC1–AC12 e NFRs em testes identificáveis antes da implementação, incluindo:

- testes de contrato headless sem navegador;
- concorrência real no repositório Supabase;
- apply → validação → rollback → reapply da migration;
- RLS e tentativas cross-project;
- persistência ausente/indisponível;
- reload, nova aba e nova sessão;
- precedência manual/automática;
- compatibilidade por símbolo e não regressão das fórmulas.

### 8.7 Validação final da story — `@po`

Comando lógico:

```text
@po *validate-story-draft docs/stories/story-AUTO-OTI-1.3*.md
```

Gate da Fase 0:

- [ ] Story sucessora existe e não amplia `MOD-QT-2-06`.
- [ ] Story atingiu 10/10 e estado `Ready`.
- [ ] Decisão arquitetural registrada.
- [ ] Parecer de dados registrado.
- [ ] Semântica de lote aprovada por PO/UX.
- [ ] Estratégia AC/NFR → testes registrada por QA.
- [ ] Nenhum requisito novo foi inventado.

## 9. Fase 1 — Assinatura e ciclo de validade

Responsável de implementação: `@dev`; revisão de desenho: `@architect`.

Executar:

1. criar assinatura canônica e determinística no domínio/aplicação;
2. incluir circuito, parâmetros efetivos e retornos downstream relevantes;
3. garantir que ordem de propriedades não altere a assinatura;
4. impedir que assinatura pronta da UI seja autoridade;
5. implementar `VIGENTE` e `OBSOLETA`;
6. invalidar por nova entrada aplicada incompatível, remoção ou recriação do circuito;
7. preservar a vigente em falha transitória com a mesma assinatura sem nova aplicação.

Gate:

- AC4, AC5 e AC10 cobertos por testes;
- valores `0`, negativos, `NaN`, infinitos ou fora do contrato rejeitados;
- assinaturas iguais/diferentes comprovadas por testes determinísticos.

Falha: `HALT: SIGNATURE_OR_VALIDITY_GATE_FAILED`.

## 10. Fase 2 — Persistência atômica

Responsável de implementação: `@dev`; autoridade técnica: `@data-engineer`.

Executar:

1. criar migration aditiva conforme a decisão aprovada;
2. implementar gravação atômica de lote;
3. implementar versão/conflito e idempotência por `operacaoId`;
4. ler somente registros automáticos vigentes;
5. distinguir `DURAVEL`, `VOLATIL` e `FALHOU`;
6. tratar legados sem assinatura sem promoção automática;
7. implementar rollback e compatibilidade de transição.

Gate:

- AC6 e AC7 passam com concorrência real;
- AC9 comprova ausência de falso sucesso;
- retry idêntico não duplica efeitos;
- lote falho não deixa itens parcialmente vigentes;
- apply → rollback → reapply passa em ambiente isolado;
- RLS e pertencimento passam em testes positivos e negativos.

Falha: `HALT: ATOMIC_PERSISTENCE_GATE_FAILED`.

## 11. Fase 3 — Operação headless CLI/API

Responsável: `@dev`; contrato aprovado por `@architect`.

Executar:

1. implementar o caso de uso que carrega o circuito real, recalcula/valida e persiste;
2. tratar `secaoEsperadaMm2` apenas como detector de divergência de preview;
3. validar projeto/circuito e resultado aprovado;
4. expor o mesmo caso de uso por CLI/API conforme decisão da Fase 0;
5. validar input/output com schema;
6. produzir auditoria de operação, projeto, circuitos, contagens e conflitos;
7. executar o fluxo sem React, navegador ou `localStorage`.

Gate:

- AC1 passa de ponta a ponta por CLI/API;
- NFR-CLI-01, NFR-REL-02, NFR-OBS-01 e NFR-SEC-01 possuem evidência;
- operação retorna persistência e contagens tipadas.

Falha: `HALT: HEADLESS_CONTRACT_GATE_FAILED`.

## 12. Fase 4 — Auto-otimização individual e em lote

Responsável: `@dev`; decisão visual: `@po`/`@ux-design-expert`.

Executar:

1. ligar **Confirmar seção** ao caso de uso headless;
2. implementar a confirmação de lote aprovada na Fase 0;
3. enviar somente resultados aprovados;
4. atualizar a UI somente após `DURAVEL`;
5. exibir contagens de calculados, aprovados, aplicados, ignorados, conflitos e falhas;
6. impedir que resultado parcial ou volátil assuma estado aplicado.

Gate:

- AC2 e AC3 passam;
- UI reutiliza o caso de uso comum;
- falha transacional mantém todos os itens como não aplicados;
- estados são distinguíveis sem depender apenas de cor.

Falha: `HALT: AUTO_OPTIMIZATION_UI_GATE_FAILED`.

## 13. Fase 5 — Consumo no MOD-QT

Responsável: `@dev`; precedência protegida pelo domínio.

Executar:

1. consultar apenas seção automática vigente e compatível;
2. manter a precedência:
   1. override explícito da chamada/simulação;
   2. edição manual auditada no MOD-QT;
   3. seção automática MOD-DC vigente;
   4. seção real disponível no contrato do circuito;
   5. ausência `null` → `—` e `PEND`;
3. invalidar/refazer a query após aplicação na mesma sessão;
4. preservar justificativa e auditoria manual;
5. revelar a automática vigente, ou `PEND`, após remover o override manual.

Gate:

- AC8 e AC11 passam;
- `S (mm²)` é preenchida automaticamente somente com fonte válida;
- circuito removido/renomeado/recriado não ressuscita valor antigo.

Falha: `HALT: MOD_QT_CONSUMPTION_GATE_FAILED`.

## 14. Fase 6 — Segurança, migration e rollout controlado

Responsáveis: `@data-engineer`, `@dev`, `@qa` e, para ambientes remotos, `@devops`.

Executar:

1. revisar migration, rollback, compatibilidade, índices e RLS;
2. validar comportamento sem migration e falha observável;
3. validar reload, nova aba e nova sessão;
4. aplicar migration antes de liberar a UI no ambiente autorizado;
5. executar rollout controlado pelo runbook existente;
6. monitorar contagens de persistidos, ignorados, conflitos, falhas e tipo de persistência;
7. acionar rollback se health/smoke falhar e houver autorização.

Gate:

- migration e rollback comprovados;
- nenhuma policy ficou mais ampla sem risco aceito, responsável e prazo;
- valores duráveis sobrevivem a novas sessões;
- ausência de infraestrutura não produz badge de aplicado;
- observabilidade permite diagnosticar cada operação.

Falha: `HALT: SECURITY_MIGRATION_ROLLOUT_GATE_FAILED`.

## 15. Fase 7 — Gates, QA e handoff DevOps

### 15.1 Gates do `@dev`

No repositório raiz:

```powershell
npm run lint
npm run typecheck
npm test
npm run build
```

Na aplicação:

```powershell
Set-Location sistema-de-instala-es-el-tricas-sie-main
npm run lint
npm run typecheck
npm test
npm run build
```

Executar também:

- testes focados dos arquivos alterados;
- teste headless do caso de uso;
- testes de concorrência Supabase;
- testes de migration/RLS;
- testes de reload/nova sessão;
- verificação dos símbolos protegidos;
- CodeRabbit conforme a política do projeto;
- atualização de checkboxes, Dev Agent Record, Change Log e File List da story.

Evidência por símbolo:

```powershell
rg -n "RetornoMODQT|ValidarMODQTSchema|RetornoMODQTSchema" sistema-de-instala-es-el-tricas-sie-main/src
rg -n "api/v1/modulos/mod-qt/validar" sistema-de-instala-es-el-tricas-sie-main/src
```

### 15.2 Review independente — `@qa`

Comandos lógicos:

```text
@qa *review docs/stories/story-AUTO-OTI-1.3*.md --mode yolo
@qa *gate AUTO-OTI-1.3
```

Quinn deve reexecutar as evidências, não apenas aceitar o registro do `@dev`.

Roteamento:

```text
PASS
  → InReview → Done
  → handoff para @devops

FAIL
  → InReview → InProgress
  → @dev corrige
  → repetir QA, máximo 5 ciclos

CONCERNS
  → documentar risco e autoridade
  → corrigir ou obter waiver formal
  → bloquear publicação sem autorização expressa

WAIVED
  → registrar escopo, justificativa, autoridade e validade
  → não inferir autorização de deploy
```

### 15.3 DevOps — publicação e deploy

Somente `@devops` executa:

```text
@devops *pre-push
@devops *push
@devops *create-pr
@devops *version-check
@devops *release
```

O deploy usa exclusivamente o `deploy_runbook` informado no manifesto; não existe autorização implícita por estar em YOLO.

Ordem obrigatória:

```text
pre-push PASS
  → push autorizado
    → PR autorizada
      → CI verde
        → merge autorizado
          → release autorizada
            → backup/snapshot validado
              → migration autorizada
                → deploy autorizado
                  → health + smoke + observabilidade
```

## 16. Rastreabilidade de aceite

| AC | Evidência obrigatória | Fase/gate |
|---|---|---|
| AC1 | Aplicação individual via CLI/API retorna `DURAVEL` e registro vigente | Fase 3 / QA |
| AC2 | Confirmação UI usa o mesmo caso de uso e preenche S após durabilidade | Fase 4 / QA |
| AC3 | Lote explícito, filtrado e atômico com contagens | Fase 4 / QA |
| AC4 | Nova assinatura inválida torna a anterior obsoleta e produz `PEND` | Fase 1 / QA |
| AC5 | Falha transitória com mesma assinatura preserva a vigente | Fase 1 / QA |
| AC6 | Sessões concorrentes em circuitos diferentes não perdem chaves | Fase 2 / Data/QA |
| AC7 | Concorrência no mesmo circuito detecta conflito/ordem | Fase 2 / Data/QA |
| AC8 | Manual prevalece; remoção revela automática vigente | Fase 5 / QA |
| AC9 | Banco/migration indisponível não produz falso sucesso | Fases 2 e 6 / QA |
| AC10 | Remoção, renomeação ou recriação não reutiliza seção antiga | Fases 1 e 5 / QA |
| AC11 | Ausência real mantém `—` e `PEND` | Fase 5 / QA |
| AC12 | Fórmulas e contratos protegidos permanecem compatíveis | Fase 7 / QA |

## 17. Rastreabilidade de NFRs

| NFR | Evidência de saída |
|---|---|
| NFR-REL-01 | Testes concorrentes AC6/AC7 e lote atômico |
| NFR-REL-02 | Retry seguro com o mesmo `operacaoId` |
| NFR-DUR-01 | AC9, reload, nova aba e nova sessão |
| NFR-OBS-01 | Log com aplicados, ignorados, conflitos, falhas e persistência |
| NFR-SEC-01 | Pertencimento projeto/circuito e parecer RLS |
| NFR-COMP-01 | AC12, typecheck, testes, build e inspeção por símbolo |
| NFR-CLI-01 | AC1 executado sem UI |

## 18. Handoffs e checkpoints

Depois que `@sm`/`@po` fixarem o identificador final, substituir `{story-id}` em todos os paths.

```text
.aiox/handoffs/{story-id}-sm-to-architect.yaml
.aiox/handoffs/{story-id}-architect-to-data-engineer.yaml
.aiox/handoffs/{story-id}-data-engineer-to-po.yaml
.aiox/handoffs/{story-id}-ux-to-po.yaml
.aiox/handoffs/{story-id}-po-to-dev.yaml
.aiox/handoffs/{story-id}-dev-to-data-engineer.yaml
.aiox/handoffs/{story-id}-data-engineer-to-qa.yaml
.aiox/handoffs/{story-id}-dev-to-qa.yaml
.aiox/handoffs/{story-id}-qa-to-devops.yaml
.aiox/workflow-state/{story-id}-state.yaml
.aiox/logs/{story-id}-yolo.log
docs/qa/gates/{story-id}-gate.yaml
```

Conteúdo mínimo de cada handoff:

```yaml
from_agent: ""
to_agent: ""
story: ""
source_artifact: docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md
workflow: docs/workflows/WORKFLOW-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.md
phase: ""
status: ""
decision_or_gate: ""
evidence: []
open_risks: []
next_command: ""
created_at: ""
```

Não avançar se o handoff declarar evidência obrigatória ausente.

## 19. Observabilidade e auditoria

Persistir o estado do runner em:

```text
.aiox/sdc-headless/<run-id>.yaml
docs/workflows/logs/SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-<timestamp>.md
```

Conteúdo mínimo:

```yaml
workflow_state:
  run_id: ""
  mode: yolo
  source_fingerprint: ""
  manifest_fingerprint: ""
  story_id: ""
  current_phase: ""
  current_agent: ""
  status: active|blocked|failed|rolled_back|deployed
  po_iterations: 0
  qa_iterations: 0
  decisions:
    persistence_and_concurrency: pending|approved|blocked
    batch_confirmation_semantics: pending|approved|blocked
    cli_api_entrypoint_and_schemas: pending|approved|blocked
  acceptance:
    AC1: pending
    AC2: pending
    AC3: pending
    AC4: pending
    AC5: pending
    AC6: pending
    AC7: pending
    AC8: pending
    AC9: pending
    AC10: pending
    AC11: pending
    AC12: pending
  quality_gates:
    lint: null
    typecheck: null
    tests: null
    build: null
    coderabbit: null
    migration: null
    rollback: null
    rls: null
    concurrency: null
    protected_contracts: null
  delivery:
    branch: ""
    commit: ""
    pull_request: ""
    release: ""
    environment: ""
    migration_status: ""
    deployment_status: ""
    smoke_status: ""
```

O log de aplicação funcional deve correlacionar `operacaoId`, projeto, circuitos, assinatura, versão, contagens, conflitos e tipo de persistência, sem expor segredos.

## 20. Política determinística de erros

| Código/condição | Ação automática |
|---|---|
| `MANIFEST_INVALID` | Bloquear antes de qualquer alteração |
| `SOURCE_ARTIFACT_CHANGED` | Invalidar snapshot e reiniciar preflight |
| `PRE_SDC_GATE_BLOCKED` | Registrar evidência e encerrar `BLOCKED` |
| `STORY_VALIDATION_NO_GO` | Retornar a `@sm`, máximo 3 ciclos |
| `ARCHITECTURE_DECISION_MISSING` | Bloquear desenvolvimento |
| `DATA_DECISION_MISSING` | Bloquear development/migration |
| `BATCH_CONFIRMATION_UNDECIDED` | Bloquear implementação de UI/lote |
| `SIGNATURE_OR_VALIDITY_GATE_FAILED` | Retornar a `@dev`; não avançar à persistência |
| `ATOMIC_PERSISTENCE_GATE_FAILED` | Retornar a `@dev`/`@data-engineer` |
| `HEADLESS_CONTRACT_GATE_FAILED` | Bloquear UI, pois CLI First não foi atendido |
| `VOLATILE_REPORTED_AS_DURABLE` | QA `FAIL` imediato |
| `CONCURRENCY_EVIDENCE_MISSING` | QA `FAIL` e bloqueio de rollout |
| `RLS_OR_OWNERSHIP_FAILED` | QA `FAIL` e bloqueio de migration/deploy |
| `PROTECTED_CONTRACT_REGRESSION` | QA `FAIL`; restaurar compatibilidade |
| `QA_MAX_ITERATIONS_EXCEEDED` | Encerrar `BLOCKED` com issues abertas |
| `CODERABBIT_CRITICAL` | Bloquear pre-push |
| `MIGRATIONS_AUTHORIZATION_MISSING` | Bloquear antes do apply remoto |
| `REMOTE_OPERATION_AUTHORIZATION_MISSING` | Bloquear antes de push/PR/merge/release/deploy |
| `DEPLOY_HEALTH_OR_SMOKE_FAILED` | Executar rollback autorizado; registrar incidente |

Falhas transitórias podem ser repetidas no máximo duas vezes quando a operação for comprovadamente idempotente. Falha de requisito, qualidade, segurança ou autorização não é transitória.

## 21. Diagrama de execução

```mermaid
flowchart TD
    A[Manifesto validado e congelado] --> B[Baseline e worktree inventariados]
    B --> C[@sm cria Story Draft]
    C --> D[@architect decide contrato e concorrência]
    D --> E[@data-engineer valida modelo, migration e RLS]
    E --> F[@po + @ux decidem confirmação do lote]
    F --> G[@qa define testes AC/NFR]
    G --> H[@po valida story]
    H -->|NO-GO até 3x| C
    H -->|GO: Ready| I[@dev Fase 1: assinatura e validade]
    I --> J[@dev Fase 2: persistência atômica]
    J --> K[@dev Fase 3: operação headless]
    K --> L[@dev Fase 4: individual e lote]
    L --> M[@dev Fase 5: consumo MOD-QT]
    M --> N[@dev/data Fase 6: segurança e migration]
    N --> O[Gates locais + story InReview]
    O --> P[@data-engineer gate final]
    P --> Q[@qa review + gate]
    Q -->|FAIL até 5x| I
    Q -->|CONCERNS| R[Correção ou waiver autorizado]
    R --> Q
    Q -->|PASS| S[Story Done]
    S --> T[@devops pre-push]
    T -->|Sem autorização| U[BLOCKED com condição de retomada]
    T -->|PASS e autorizado| V[Push, PR, CI, merge e release]
    V --> W[Migration e deploy pelo runbook]
    W -->|Falha| X[Rollback + incidente]
    W -->|Sucesso| Y[Health, smoke e métricas]
    Y --> Z[DEPLOYED]
```

## 22. Execução e retomada

Dry-run completo, com efeitos remotos simulados:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.yaml --dry-run
```

Execução real com adapter autorizado:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.yaml --adapter-module .aiox/adapters/sdc-auto-otimizacao-s-queda-tensao.js
```

Retomada idempotente:

```powershell
node .aiox-core/development/scripts/sdc-headless-yolo.js --manifest docs/workflows/MANIFEST-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.yaml --resume <run-id> --adapter-module .aiox/adapters/sdc-auto-otimizacao-s-queda-tensao.js
```

O runner deve retomar do último checkpoint aprovado, nunca pular um gate incompleto nem repetir efeito externo já confirmado.

## 23. Definition of Done do workflow

- [ ] Manifesto validado, congelado e auditável.
- [ ] Nova story sucessora criada e validada como `Ready` antes de código.
- [ ] Decisões de arquitetura/dados, produto/UX e CLI/API registradas.
- [ ] Fases 1–6 implementadas na ordem e com gates focados.
- [ ] AC1–AC12 rastreados para testes automatizados e aprovados.
- [ ] NFR-REL-01, REL-02, DUR-01, OBS-01, SEC-01, COMP-01 e CLI-01 aprovados.
- [ ] Caso de uso headless comprovado antes da UI.
- [ ] Migration aditiva, rollback, RLS, concorrência e idempotência validados.
- [ ] Aplicação individual e em lote usam o mesmo caminho durável.
- [ ] MOD-QT consome somente seção automática vigente e preserva override manual.
- [ ] Contratos protegidos e fórmulas permanecem compatíveis.
- [ ] Gates de lint, typecheck, testes e build aprovados.
- [ ] Story contém checklist, File List, Dev Agent Record, Change Log e QA Results atualizados.
- [ ] QA gate é `PASS` ou existe waiver formal que autoriza o próximo estágio.
- [ ] Operações remotas foram executadas somente por `@devops` e dentro do manifesto.
- [ ] Rollout, health check, smoke e observabilidade foram aprovados.
- [ ] Estado terminal e evidências foram persistidos.

## 24. Critério de conclusão

O workflow termina como `DEPLOYED` somente quando todas as fases do plano foram executadas, a story está `Done`, AC1–AC12 e os NFRs estão aprovados, a migration foi aplicada no ambiente autorizado, o rollout controlado foi concluído e health/smoke passaram.

Se a execução local e os gates passarem, mas uma autorização externa estiver ausente, o resultado correto é `BLOCKED` com condição objetiva de retomada — nunca “deploy concluído”. Se o rollout falhar e o rollback autorizado for executado, o resultado é `ROLLED_BACK`.

---

— Orion, orquestrando o sistema
