# Plano YOLO de implementação automática — Correção do Padrão compatível EDP V9

**Modo:** YOLO automático, sem prompts de confirmação durante a execução  
**Fonte executiva:** `docs/EXECUCAO-CORRECAO-PADRAO-COMPATIVEL-EDP-V9.md`  
**Escopo funcional:** correção estrutural do campo "Padrão compatível" para EDP São Paulo V9  
**Regra de segurança:** automação máxima com bloqueios constitucionais e gates de pacote respeitados  
**Data de referência:** 2026-07-27

## 1. Objetivo

Definir um plano para executar automaticamente a correção descrita em `docs/EXECUCAO-CORRECAO-PADRAO-COMPATIVEL-EDP-V9.md`, sem intervenção humana durante o ciclo normal de trabalho. O plano deve permitir que os agentes criem, validem, implementem e revisem os artefatos dentro de suas autoridades, parando apenas quando houver bloqueio formal de gate, ausência de story válida, falha recorrente de validação ou necessidade de autoridade externa ainda não aprovada.

Este plano não autoriza contornar a Constitution. "YOLO" significa eliminar perguntas intermediárias e seguir a próxima ação permitida automaticamente; não significa pular story, assumir autoridade de outro agente, aprovar gate pendente, ativar release ou remover legado.

## 2. Princípios operacionais do modo YOLO

1. **Sem prompts humanos:** cada agente executa a próxima ação permitida com base nos artefatos existentes.
2. **Fail-closed:** ausência de evidência, story, gate ou permissão vira bloqueio automático, não suposição.
3. **CLI First:** toda capacidade nova deve existir via domínio/CLI/API antes de UI.
4. **Story-driven:** nenhum código é alterado antes de existir story aplicável em `docs/stories/`.
5. **Autoridade preservada:** `@sm`/`@po` criam stories; `@dev` implementa; `@qa` emite veredito de qualidade; `@devops` faz push/PR/release.
6. **Sem invenção:** todo requisito deve rastrear para PRD, plano, QA preflight, ADR, decisões DP/RV/GP/GO ou fonte normativa oficial.
7. **Parada automática:** o fluxo interrompe quando encontrar gate de pacote `HOLD`/`BLOCK`, teste falhando sem correção segura ou necessidade de aprovação não presente.

## 3. Escopo autorizado agora

O QA preflight vigente libera apenas:

- criação de stories do **Pacote 1 — Modelo normativo e catálogo estrutural**;
- preparação documental e rastreamento dos pacotes seguintes;
- implementação somente após a story do pacote 1 estar pronta para desenvolvimento.

Não está autorizado agora:

- implementar pacote 2 ou 3 antes da conclusão sequencial do pacote 1;
- implementar API/persistência/versionamento dos pacotes bloqueados;
- implementar UI final do campo "Padrão compatível";
- ativar Release 1;
- remover catálogo genérico ou legado EDP;
- simular aprovação de DP-04, DP-07, DP-09, GP-01, GO-01A ou GO-01B.

## 4. Arquivos de controle

O fluxo YOLO deve criar e manter estes artefatos:

- `docs/stories/story-PE-EDP-V9-01-modelo-catalogo-estrutural.md`
- `.aiox/handoffs/PE-EDP-V9-01-sm-to-po.yaml`
- `.aiox/handoffs/PE-EDP-V9-01-po-to-dev.yaml`
- `.aiox/handoffs/PE-EDP-V9-01-dev-to-qa.yaml`
- `.aiox/handoffs/PE-EDP-V9-01-qa-to-devops.yaml`, somente se QA aprovar
- `.aiox/workflow-state/PE-EDP-V9-01-state.yaml`
- `.aiox/logs/PE-EDP-V9-01-yolo.log`

Se `.aiox/` não existir, o fluxo deve criá-lo com subpastas mínimas:

```text
.aiox/
  handoffs/
  workflow-state/
  logs/
```

## 5. Máquina de estados

```yaml
workflow: PE-EDP-V9-CORRECAO-PADRAO-COMPATIVEL
mode: yolo
human_intervention: false
default_on_missing_evidence: BLOCK
states:
  - PREFLIGHT_DOCUMENTAL
  - STORY_DRAFT
  - STORY_VALIDATION
  - READY_FOR_DEV
  - IMPLEMENTATION
  - DEV_VALIDATION
  - QA_REVIEW
  - READY_FOR_DEVOPS
  - BLOCKED
  - COMPLETE
```

Transições automáticas:

```yaml
PREFLIGHT_DOCUMENTAL:
  pass: STORY_DRAFT
  fail: BLOCKED
STORY_DRAFT:
  pass: STORY_VALIDATION
  fail: BLOCKED
STORY_VALIDATION:
  go: READY_FOR_DEV
  no_go: STORY_DRAFT
  repeated_no_go_limit: 3
READY_FOR_DEV:
  pass: IMPLEMENTATION
  fail: BLOCKED
IMPLEMENTATION:
  pass: DEV_VALIDATION
  fail_fixable: IMPLEMENTATION
  repeated_failure_limit: 3
DEV_VALIDATION:
  pass: QA_REVIEW
  fail: IMPLEMENTATION
QA_REVIEW:
  pass: READY_FOR_DEVOPS
  concerns: IMPLEMENTATION
  fail: BLOCKED
READY_FOR_DEVOPS:
  pass: COMPLETE
  fail: BLOCKED
```

## 6. Plano por agente

### 6.1 Atlas `@analyst` — preparação do plano e restrições

**Executa automaticamente:**

1. Ler PRD, QA preflight, plano de execução e fonte normativa indicada.
2. Extrair restrições que não podem ser violadas.
3. Produzir matriz de escopo liberado versus bloqueado.
4. Registrar o plano YOLO e os riscos.
5. Encaminhar handoff para `@sm` com `DRAFT_PACKAGE_1_STORIES`.

**Não executa:**

- criação formal de story;
- decisão de arquitetura;
- implementação;
- veredito de QA.

**Saída esperada:**

- este plano;
- handoff para `@sm`;
- estado `PREFLIGHT_DOCUMENTAL: pass`.

### 6.2 River `@sm` — criação automática da story

**Executa automaticamente:**

1. Criar a story `PE-EDP-V9-01` em `docs/stories/`.
2. Derivar escopo somente do Pacote 1.
3. Adicionar acceptance criteria rastreáveis.
4. Declarar fora de escopo os pacotes 2 a 8.
5. Adicionar tarefas e subtarefas executáveis por `@dev`.
6. Criar File List inicial.
7. Gerar handoff para `@po`.

**Critérios obrigatórios da story:**

- status inicial `Draft`;
- referência ao PRD e ao QA preflight;
- requisitos vinculados a FR/NFR/CR/AC;
- DP-01, DP-05 e RV-01 registrados como aprovados para criação de story;
- DP-04, DP-07, DP-09, GP-01, GO-01A e GO-01B registrados como bloqueios fora do pacote 1 quando aplicáveis;
- nenhuma tarefa de UI final;
- nenhuma tarefa de ativação ou remoção de legado.

**Parada automática:**

- se não houver rastreabilidade suficiente para algum critério;
- se a story tentar implementar pacote não liberado;
- se a story exigir decisão de arquitetura nova.

### 6.3 Pax `@po` — validação automática da story

**Executa automaticamente:**

1. Validar a story contra o PRD, QA preflight e Definition of Done.
2. Conferir se a story está completa e implementável.
3. Rejeitar qualquer requisito inventado.
4. Atualizar status de `Draft` para `Ready` se a validação for `GO`.
5. Criar handoff para `@dev`.

**Regras de validação:**

- `GO` se a story cobre apenas pacote 1 e é implementável sem decisão pendente.
- `NO-GO` se faltar rastreabilidade, teste, File List, critério objetivo ou se houver escopo de pacote bloqueado.
- Após três ciclos `NO-GO`, marcar workflow como `BLOCKED`.

### 6.4 Dex `@dev` — implementação automática

**Executa automaticamente somente se a story estiver `Ready`:**

1. Ler a story e apenas os artefatos indicados nela.
2. Criar ou ajustar tipos do domínio EDP V9 em `src/domain/distribuidora/edp-sp/`.
3. Criar catálogo estrutural EDP V9 separado do catálogo genérico.
4. Implementar validação estrutural do catálogo.
5. Garantir representação de estrela e delta conforme escopo do pacote 1.
6. Garantir que `380 V` seja inválido para alternativas EDP V9.
7. Garantir metadados normativos obrigatórios.
8. Criar testes unitários e de fronteira do pacote 1.
9. Atualizar apenas as seções permitidas da story:
   - Tasks/Subtasks;
   - Dev Agent Record;
   - Debug Log;
   - Completion Notes;
   - File List;
   - Change Log;
   - Status quando autorizado pelo workflow.

**Não executa no pacote 1:**

- substituir `FornecimentoSelector`;
- persistir seleção final de usuário;
- alterar fluxo de UI;
- remover catálogo genérico;
- ativar release;
- criar PR.

**Validações obrigatórias:**

```powershell
cd sistema-de-instala-es-el-tricas-sie-main
npm run lint
npm run typecheck
npm test
npm run build
```

**Parada automática:**

- ausência de story `Ready`;
- falha de teste que não seja corrigível em até três tentativas;
- necessidade de dependência externa não aprovada;
- requisito ambíguo que não possa ser resolvido pelos artefatos.

### 6.5 Quinn `@qa` — revisão automática de qualidade

**Executa automaticamente após `@dev` marcar Ready for Review:**

1. Revisar rastreabilidade PRD/story/código/testes.
2. Confirmar que o pacote implementado é somente o pacote 1.
3. Confirmar que o catálogo genérico foi preservado fora da rota EDP.
4. Confirmar que `380 V` não passa na validação EDP V9.
5. Confirmar que não houve implementação prematura de UI final.
6. Conferir execução dos quality gates.
7. Emitir gate:
   - `PASS`;
   - `CONCERNS`;
   - `FAIL`.

**Ações automáticas por veredito:**

- `PASS`: handoff para `@devops`.
- `CONCERNS`: retorno para `@dev` com lista objetiva de correções.
- `FAIL`: workflow `BLOCKED` se o problema for gate/autoridade; retorno para `@dev` se for correção técnica localizada.

### 6.6 Gage `@devops` — fechamento operacional sem release

**Executa automaticamente somente se QA der `PASS`:**

1. Confirmar que story está `Ready for Review` ou `Done`, conforme workflow local.
2. Confirmar gates:
   - lint;
   - typecheck;
   - tests;
   - build;
   - QA gate.
3. Preparar push/PR apenas se autorizado pelo fluxo DevOps e pelo estado da story.
4. Não criar release.
5. Não ativar Release 1.
6. Não remover legado.

**Parada automática:**

- QA sem `PASS`;
- story incompleta;
- quality gate falhando;
- ausência de autorização DevOps aplicável.

## 7. Pipeline YOLO detalhado

### Fase A — Preflight automático

```powershell
git status --short
rg -n "PASS — LIBERADO|DRAFT_PACKAGE_1_STORIES|packages_2_3|packages_4_8" docs/qa/QA-PREFLIGHT-SDC-EDP-V9.md
rg -n "Pacote 1|Modelo normativo|catálogo estrutural|FR1|FR2|FR3|FR4|FR20|FR22|AC-18" docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md
Test-Path Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json
```

Resultado esperado:

- pacote 1 liberado;
- pacotes 2 a 8 não implementáveis neste ciclo;
- fonte normativa existe;
- worktree sujo é registrado, mas mudanças não relacionadas são preservadas.

### Fase B — Criação de story

Arquivo esperado:

```text
docs/stories/story-PE-EDP-V9-01-modelo-catalogo-estrutural.md
```

Conteúdo mínimo:

- título;
- status `Draft`;
- objetivo;
- escopo;
- fora de escopo;
- critérios de aceitação;
- tarefas;
- testes;
- Dev Notes;
- File List;
- QA Results;
- Change Log.

Comando lógico:

```text
@sm *draft PE-EDP-V9-01 --source docs/EXECUCAO-CORRECAO-PADRAO-COMPATIVEL-EDP-V9.md --mode yolo
```

### Fase C — Validação da story

Comando lógico:

```text
@po *validate-story-draft docs/stories/story-PE-EDP-V9-01-modelo-catalogo-estrutural.md --mode yolo
```

Resultado esperado:

- `GO`: status atualizado para `Ready`;
- `NO-GO`: story corrigida automaticamente por `@sm`;
- três `NO-GO`: workflow `BLOCKED`.

### Fase D — Implementação do pacote 1

Comando lógico:

```text
@dev *develop story-PE-EDP-V9-01-modelo-catalogo-estrutural --mode yolo
```

Implementação esperada:

- tipos EDP V9 estruturais;
- catálogo estrutural EDP V9;
- validação estrutural;
- testes unitários;
- nenhum acoplamento com UI final;
- nenhum uso EDP de `catalogoFornecimentoDefault()`;
- rejeição estrutural de `380 V` no contexto EDP.

### Fase E — Gates técnicos

Comandos obrigatórios:

```powershell
cd sistema-de-instala-es-el-tricas-sie-main
npm run lint
npm run typecheck
npm test
npm run build
```

Política de retry:

- primeira falha: corrigir e repetir;
- segunda falha no mesmo ponto: reduzir escopo para a menor correção segura e repetir;
- terceira falha no mesmo ponto: marcar `BLOCKED` com log técnico.

### Fase F — QA automático

Comando lógico:

```text
@qa *review docs/stories/story-PE-EDP-V9-01-modelo-catalogo-estrutural.md --mode yolo
```

Critérios:

- `PASS`: encaminhar a `@devops`;
- `CONCERNS`: retornar a `@dev`;
- `FAIL`: bloquear se for escopo/gate; corrigir se for implementação localizada.

### Fase G — Fechamento sem ativação

Comando lógico:

```text
@devops *pre-push --story PE-EDP-V9-01 --mode yolo
```

Permitido:

- preparar push/PR se o fluxo DevOps estiver autorizado;
- registrar status e evidências.

Proibido:

- criar release;
- ativar Release 1;
- remover legado;
- alterar permissões de produção.

## 8. Política para os seis passos do guia

| Passo do guia | Execução YOLO | Estado neste ciclo |
| --- | --- | --- |
| 1 — Criar story do pacote 1 | Automática por `@sm`, validação por `@po` | Liberado |
| 2 — Catálogo EDP V9 canônico | Automática por `@dev` após story `Ready` | Liberado dentro do pacote 1 |
| 3 — Regra de candidatos antes da UI | Preparar contrato e testes se couber na story; implementação plena depende do pacote 2 | Parcial, com trava sequencial |
| 4 — Substituir origem das opções da rota EDP | Não executar até pacote/API liberados | Bloqueado neste ciclo |
| 5 — Bloquear `380 V` na EDP V9 | Executar validação estrutural no pacote 1; propagação completa nos consumidores vem depois | Parcial |
| 6 — Reestruturar campo UI | Não executar até pacotes 4–6 e GP-01/DP-04/DP-07 aplicáveis | Bloqueado neste ciclo |

## 9. Critérios automáticos de bloqueio

O fluxo deve parar em `BLOCKED` quando ocorrer qualquer uma das condições:

- story ausente ou não validada;
- pacote alvo diferente do pacote 1 sem novo QA preflight;
- necessidade de DP-04, DP-07, DP-09, GP-01, GO-01A ou GO-01B ainda pendente;
- tentativa de ativar release;
- tentativa de remover legado;
- tentativa de alterar catálogo genérico fora de escopo;
- tentativa de inferir topologia por município;
- tentativa de tratar ausência de manifestação EDP como compatibilidade;
- três falhas repetidas no mesmo gate técnico;
- teste obrigatório sem execução ou sem resultado.

## 10. Critérios de sucesso do ciclo YOLO atual

O ciclo atual será considerado completo quando:

1. a story `PE-EDP-V9-01` existir e estiver validada;
2. a implementação do pacote 1 estiver concluída;
3. os testes do pacote 1 estiverem presentes;
4. `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passarem;
5. File List da story estiver atualizado;
6. QA emitir `PASS` ou `CONCERNS` tratável;
7. pacotes 2 a 8 permanecerem bloqueados ou pendentes conforme QA preflight, sem implementação indevida.

## 11. Log mínimo esperado

O arquivo `.aiox/logs/PE-EDP-V9-01-yolo.log` deve registrar:

```text
[PREFLIGHT] pacote_1=PASS packages_2_3=HOLD packages_4_8=BLOCK
[SM] story_created=docs/stories/story-PE-EDP-V9-01-modelo-catalogo-estrutural.md
[PO] validation=GO status=Ready
[DEV] implementation_started
[DEV] lint=PASS
[DEV] typecheck=PASS
[DEV] test=PASS
[DEV] build=PASS
[QA] gate=PASS|CONCERNS|FAIL
[DEVOPS] pre_push=PASS|SKIPPED|BLOCKED
```

## 12. Próxima ação automática

Iniciar o workflow pelo handoff:

```text
@sm *draft PE-EDP-V9-01 --mode yolo --source docs/EXECUCAO-CORRECAO-PADRAO-COMPATIVEL-EDP-V9.md
```

Se a story for validada por `@po`, continuar automaticamente para:

```text
@dev *develop PE-EDP-V9-01 --mode yolo
```

Se qualquer gate bloquear, registrar o bloqueio e parar sem solicitar intervenção humana durante a execução.
