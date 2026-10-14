# Plano YOLO de implementação automática — MOD-QT-2 (Motor real de Queda de Tensão)

**Modo:** YOLO automático, sem prompts de confirmação durante a execução
**Fonte executiva:** `Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md`
**Escopo funcional:** substituição do mock `validarModQTMock` por um motor real de cálculo de queda de tensão (critério C5 do MOD-DC), mantendo o contrato público `RetornoMODQT`/`ValidarMODQTSchema` inalterado
**Regra de segurança:** automação máxima com bloqueios constitucionais e gates de pacote respeitados
**Data de referência:** 2026-07-27

## 1. Objetivo

Executar automaticamente, do início ao fim do ciclo SDC (Story Development Cycle), a implementação do MOD-QT-2 conforme especificado em `PROMPT-QUEDA-TENSAO-v2.2.md`, sem intervenção humana durante o fluxo normal de trabalho: `@sm` cria as stories → `@po` valida → `@dev` implementa → `@qa` qualifica → `@devops` prepara o fechamento. O plano deve parar apenas quando houver bloqueio formal de gate, ausência de story válida, falha recorrente de validação, ou necessidade de fonte normativa externa ainda não confirmada (ver §3).

"YOLO" significa eliminar perguntas intermediárias entre agentes e seguir a próxima ação permitida automaticamente. Não significa pular story, assumir autoridade de outro agente, inventar valor normativo, aprovar gate pendente sem critério, ou executar `git push`/deploy sem a autorização explícita do usuário exigida pelo protocolo de segurança da sessão (ver §3 e §6.5) — essa é a única etapa deste plano que permanece fora do YOLO por desenho, não por falha de automação.

## 2. Princípios operacionais do modo YOLO

1. **Sem prompts humanos entre agentes:** cada agente executa a próxima ação permitida com base nos artefatos existentes.
2. **Fail-closed:** ausência de evidência, story, gate, valor normativo confirmado ou permissão vira bloqueio automático, não suposição.
3. **CLI First:** toda capacidade nova deve existir via domínio/API antes de UI (§18–§23 do documento-fonte já seguem essa ordem).
4. **Story-driven:** nenhum código é alterado antes de existir story aplicável em `docs/stories/`.
5. **Autoridade preservada:** `@sm` cria stories; `@po` valida; `@dev` implementa; `@qa` emite veredito de qualidade; `@devops` prepara push/PR/release — cada um dentro dos limites de `.claude/rules/agent-authority.md`.
6. **Sem invenção (Artigo IV):** nenhum valor de resistência, reatância ou fórmula normativa sem fonte confirmada pode ser tratado como definitivo — os itens `[VERIFICAR]` do documento-fonte (§30) permanecem `[VERIFICAR]` na implementação; nunca viram `CONFIRMADO` por decisão automática de um agente.
7. **Parada automática:** o fluxo interrompe quando encontrar gate `HOLD`/`BLOCK`, teste falhando sem correção segura em 3 tentativas, ou necessidade de aprovação não presente (ex.: catálogo de fabricante, confirmação da EDP).
8. **Push/deploy nunca automático de fato:** `@devops` pode preparar todos os artefatos de push/PR/release dentro do YOLO, mas a execução real de `git push`, abertura de PR, merge ou deploy exige autorização explícita do usuário no momento do ato, conforme protocolo de segurança da sessão. Isso não é uma limitação deste plano — é uma regra permanente do ambiente e vale mesmo em modo YOLO.

## 3. Escopo autorizado agora (pacotes)

O documento-fonte (`PROMPT-QUEDA-TENSAO-v2.2.md` §33, "Ordem de implementação recomendada") já define a sequência correta. Ela se traduz nos pacotes abaixo:

| Pacote | Conteúdo | Depende de | Status neste ciclo |
|---|---|---|---|
| **Pacote 1** | Motor de cálculo (§18–§20), tabela de impedância com valores provisórios `[VERIFICAR]` (§13.4/§13.6), substituição do mock no endpoint (§15.1.3), simulador de cenários (§21), UI (§24–§25), limite EDP 1% ramal de entrada (§13.8) | Nada externo — tudo confirmável com as fontes já no repositório | **Liberado** |
| Pacote 2 | Resolver VER-QT-02/VER-QT-03 (valores reais de resistência/reatância por seção, Cu e Al) | Catálogo de fabricante (Prysmian/Nexans) ou IEC 60364-5-52 — **não disponível no projeto hoje** | **Bloqueado** — não implementável sem fonte externa; permanece `[VERIFICAR]` no Pacote 1 |
| Pacote 3 | Resolver VER-QT-07 (qual alínea da NBR 5410 6.2.7.1 se aplica ao modelo de atendimento EDP-SP: 7% ou 5%) | Confirmação junto à concessionária ou fonte documental adicional | **Bloqueado** |
| Pacote 4 | Resolver VER-QT-04 (fator 2 ou √3 para circuito bifásico) | Fonte normativa não localizada nos anexos do projeto | **Bloqueado** |

**Não está autorizado agora:**
- promover qualquer valor do Pacote 2/3/4 para `CONFIRMADO` sem a fonte declarada;
- implementar cálculo bifásico como caminho automático sem alerta (o motor deve usar o fator conservador 2 com alerta explícito, conforme §13.2.1 do documento-fonte);
- remover ou simplificar a marcação `[VERIFICAR]` do campo `fonte` do `RetornoMODQT` quando valores provisórios forem usados;
- alterar o contrato público `RetornoMODQT`/`ValidarMODQTSchema`/`/api/v1/modulos/mod-qt/validar` (NÃO TOCAR, §31 do documento-fonte);
- executar `git push`, criar PR, merge ou deploy sem autorização explícita do usuário no momento do ato (§2.8).

Quando os Pacotes 2–4 forem desbloqueados (fonte obtida), este plano pode ser reaberto para cobri-los como stories adicionais (`MOD-QT-2.x`), sem necessidade de reescrever o Pacote 1.

## 4. Arquivos de controle

O fluxo YOLO deve criar e manter estes artefatos:

- `docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md`
- `.aiox/handoffs/MOD-QT-2-01-sm-to-po.yaml`
- `.aiox/handoffs/MOD-QT-2-01-po-to-dev.yaml`
- `.aiox/handoffs/MOD-QT-2-01-dev-to-qa.yaml`
- `.aiox/handoffs/MOD-QT-2-01-qa-to-devops.yaml`, somente se QA aprovar
- `.aiox/workflow-state/MOD-QT-2-01-state.yaml`
- `.aiox/logs/MOD-QT-2-01-yolo.log`

Se `.aiox/handoffs/` já tiver 5 ou mais handoffs acumulados para este pipeline ao final do ciclo, aplicar `.claude/rules/handoff-consolidation.md` (consolidar em `RUN-LOG.md`) antes de encerrar.

## 5. Máquina de estados

```yaml
workflow: MOD-QT-2-MOTOR-QUEDA-TENSAO
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

### 6.1 River `@sm` — criação automática da story

**Executa automaticamente:**

1. Ler `PROMPT-QUEDA-TENSAO-v2.2.md` integralmente (fonte única de requisitos — nenhum outro documento substitui).
2. Criar a story `docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md`, cobrindo exclusivamente o **Pacote 1** (§3).
3. Traduzir os critérios de aceite `CA-QT-01` a `CA-QT-22` (documento-fonte §26) em acceptance criteria rastreáveis da story, no formato Gherkin quando aplicável.
4. Declarar fora de escopo os Pacotes 2–4, citando os IDs `VER-QT-02`, `VER-QT-03`, `VER-QT-04`, `VER-QT-07` (documento-fonte §30) como pendências explícitas, não omissões.
5. Adicionar tarefas e subtarefas executáveis por `@dev`, seguindo a "Ordem de implementação recomendada" do documento-fonte §33 (itens 1–4; os itens 5–7 ficam fora de escopo por dependerem dos Pacotes 2–4):
   - Motor de cálculo (§18–§20) com tabela de impedância provisória
   - Substituição do mock no endpoint público (§15.1.3)
   - Validação de não-regressão contra o mock (CA-QT-19) **antes** de qualquer outro teste
   - Interface de visualização (§24–§25) e simulador (§21)
6. Incluir File List inicial com os arquivos esperados (ver §6.3, Alterações técnicas).
7. Gerar handoff para `@po`.

**Critérios obrigatórios da story:**
- status inicial `Draft`;
- referência explícita a `PROMPT-QUEDA-TENSAO-v2.2.md` como fonte, seção a seção;
- todo requisito rastreável a uma seção numerada do documento-fonte (Artigo IV — No Invention);
- contrato público (`RetornoMODQT`, `ValidarMODQTSchema`, endpoint) marcado como **inalterável** na própria story;
- nenhuma tarefa dos Pacotes 2–4.

**Parada automática:**
- se algum requisito da story não rastrear a uma seção do documento-fonte;
- se a story tentar incluir tarefa de Pacote 2/3/4;
- se a story exigir decisão de arquitetura não coberta pelo documento-fonte.

### 6.2 Pax `@po` — validação automática da story

**Executa automaticamente:**

1. Validar a story contra `PROMPT-QUEDA-TENSAO-v2.2.md`, o contrato real em produção (`contratos.ts`, `otimizar-condutor.schema.ts`, `modulos.mod-qt.validar.ts`) e o Definition of Done.
2. Aplicar o checklist de 10 pontos de `.claude/rules/story-lifecycle.md` (Fase 2).
3. Rejeitar qualquer AC que não seja testável ou que dependa de um item `[VERIFICAR]` como se fosse `CONFIRMADO`.
4. Confirmar que a story não altera o contrato público (`RetornoMODQT`/`ValidarMODQTSchema`/rota do endpoint) — qualquer tentativa de alteração é `NO-GO` automático.
5. Atualizar status de `Draft` para `Ready` se `GO` (≥ 7/10).
6. Criar handoff para `@dev`.

**Regras de validação:**
- `GO` se a story cobre apenas o Pacote 1, todos os AC são testáveis e nenhum item `[VERIFICAR]` é tratado como resolvido.
- `NO-GO` se faltar rastreabilidade a uma seção do documento-fonte, se a story tocar o contrato público, ou se incluir escopo de Pacote 2/3/4.
- Após três ciclos `NO-GO`, marcar workflow como `BLOCKED`.

### 6.3 Dex `@dev` — implementação automática

**Executa automaticamente somente se a story estiver `Ready`:**

1. Ler a story e `PROMPT-QUEDA-TENSAO-v2.2.md` (seções indicadas na story).
2. Criar o motor de cálculo em `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/` (paralelo estrutural a `src/domain/dimensionamento-condutores/`), incluindo:
   - método simplificado e completo (§18–§19 do documento-fonte);
   - seleção de método por seção (`≤ 25 mm²` vs `> 25 mm²`);
   - tabela de impedância com `status_verificacao = '[VERIFICAR]'` nos valores provisórios (§13.4);
   - cálculo de `secao_requerida_mm2` (§13.5) na série IEC 60228;
   - mapeamento modelo interno → `RetornoMODQT` (§16).
3. Substituir `validarModQTMock` em `src/routes/api/v1/modulos.mod-qt.validar.ts` pelo motor real, **sem alterar** a assinatura do endpoint, o schema Zod de request/response, ou a rota.
4. Implementar limite EDP-SP de 1% no ramal de entrada (§13.8) como validação adicional, sem alterar o contrato público (nota do documento-fonte: pode ser chamada separada com `origem = "RAMAL-ENTRADA-EDP"` e `limite_percentual = 1.0`, ou lógica interna — decisão de implementação de `@dev`, documentada no Dev Agent Record).
5. Implementar simulador de cenários (§21) e endpoints adicionais (§23.2).
6. Implementar UI mínima (§24–§25) em IBM Carbon, herdando as regras de acessibilidade (§30 do documento-fonte / R-05 deste projeto).
7. Escrever testes cobrindo `CA-QT-01` a `CA-QT-22` (documento-fonte §26/§28), com **CA-QT-19 (não-regressão do mock) executado antes de qualquer outro**.
8. Rodar os gates técnicos (ver abaixo) e corrigir falhas dentro do limite de tentativas.
9. Atualizar apenas as seções permitidas da story: Tasks/Subtasks, Dev Agent Record, Debug Log, Completion Notes, File List, Change Log, Status (`Ready` → `InProgress` → `InReview`).

**Não executa neste pacote:**
- resolver VER-QT-02/03/04/07 com valor definitivo;
- alterar `contratos.ts`, `otimizar-condutor.schema.ts` ou a rota do endpoint público;
- remover a marcação `[VERIFICAR]` de qualquer valor provisório;
- criar PR ou fazer push.

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
- CA-QT-19 (não-regressão) falhando sem causa normativa documentada;
- necessidade de valor normativo não confirmado tratado como obrigatório para prosseguir.

### 6.4 Quinn `@qa` — revisão automática de qualidade

**Executa automaticamente após `@dev` marcar `InReview`:**

1. Revisar rastreabilidade `PROMPT-QUEDA-TENSAO-v2.2.md` → story → código → testes.
2. Confirmar que o contrato público (`RetornoMODQT`, `ValidarMODQTSchema`, rota) está **byte-a-byte** igual ao que já está em produção (CA-QT-18).
3. Confirmar que todo resultado calculado com valores `[VERIFICAR]` propaga essa marcação no campo `fonte` (CA-QT-12).
4. Confirmar CA-QT-19 (não-regressão do mock) e CA-QT-21/CA-QT-22 (limite EDP 1% e marcação `[VERIFICAR]` do limite total).
5. Confirmar que nenhum item da lista NÃO TOCAR (documento-fonte §31) foi alterado.
6. Rodar quality gates (lint, typecheck, test, build) e checklist de segurança básica (OWASP).
7. Emitir gate: `PASS`, `CONCERNS` ou `FAIL`.

**Ações automáticas por veredito:**
- `PASS` ou `CONCERNS` (com observações documentadas): status `InReview` → `Done`, handoff para `@devops`.
- `FAIL`: status `InReview` → `InProgress`, retorno para `@dev` com lista objetiva de correções.

### 6.5 Gage `@devops` — fechamento operacional sem execução de push

**Executa automaticamente somente se QA der `PASS` ou `CONCERNS`:**

1. Confirmar que a story está `Done`.
2. Confirmar todos os gates: lint, typecheck, tests, build, QA gate.
3. Preparar mensagem de commit e descrição de PR (conteúdo pronto, não executado).
4. Preparar changelog/notas de release referenciando `MOD-QT-2-01` e a fonte `PROMPT-QUEDA-TENSAO-v2.2.md`.
5. Registrar em log que o fluxo está `READY_FOR_DEVOPS: pass` e **aguardando autorização explícita do usuário** para os comandos reais (`git push`, `gh pr create`, merge, deploy).

**Não executa em nenhuma hipótese dentro do YOLO:**
- `git push` real;
- `gh pr create`/`gh pr merge` real;
- deploy/release real;
- qualquer comando destrutivo ou que publique estado para fora do repositório local.

Essas ações ficam **prontas e descritas**, mas a execução delas é um novo pedido explícito do usuário, fora do escopo de "modo YOLO sem intervenção humana" — essa é uma regra permanente do ambiente (Git Safety Protocol), não uma limitação deste plano específico.

**Parada automática:**
- QA sem `PASS`/`CONCERNS`;
- story incompleta;
- quality gate falhando;
- tentativa de qualquer agente de pular esta barreira.

## 7. Pipeline YOLO detalhado

### Fase A — Preflight automático

```powershell
git status --short
Test-Path Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md
Test-Path sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts
Test-Path sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-qt.validar.ts
```

Resultado esperado:
- `PROMPT-QUEDA-TENSAO-v2.2.md` existe e é a versão vigente (verificar `Identificador: MOD-QT-v2.2` no cabeçalho);
- contrato `RetornoMODQT` e endpoint mock existem (linha de base a não regredir);
- worktree sujo é registrado, mas mudanças não relacionadas são preservadas (nunca `git clean`/`git reset --hard` automático).

### Fase B — Criação de story

Arquivo esperado: `docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md`

Comando lógico:
```text
@sm *draft MOD-QT-2-01 --source "Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md" --mode yolo
```

### Fase C — Validação da story

Comando lógico:
```text
@po *validate-story-draft docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md --mode yolo
```

Resultado esperado:
- `GO`: status atualizado para `Ready`;
- `NO-GO`: story corrigida automaticamente por `@sm`;
- três `NO-GO`: workflow `BLOCKED`.

### Fase D — Implementação do Pacote 1

Comando lógico:
```text
@dev *develop story-MOD-QT-2-01-motor-calculo-queda-tensao --mode yolo
```

Implementação esperada: motor de cálculo, substituição do mock, simulador, UI mínima, testes CA-QT-01 a CA-QT-22 — sem tocar contrato público, sem resolver Pacotes 2–4 com valor definitivo.

### Fase E — Gates técnicos

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
@qa *review docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md --mode yolo
```

Critérios:
- `PASS`/`CONCERNS`: encaminhar a `@devops`;
- `FAIL`: retornar a `@dev` (se correção localizada) ou `BLOCKED` (se escopo/gate/contrato).

### Fase G — Fechamento sem push

Comando lógico:
```text
@devops *pre-push --story MOD-QT-2-01 --mode yolo
```

Permitido: preparar commit/PR/release notes, registrar `READY_FOR_DEVOPS: pass`.
Proibido: executar push, PR, merge ou deploy reais sem autorização explícita do usuário nesse momento.

## 8. Política para os 7 passos de "Ordem de implementação recomendada" (documento-fonte §33)

| Passo do documento-fonte | Execução YOLO | Estado neste ciclo |
|---|---|---|
| 1 — Motor de cálculo com tabela `[VERIFICAR]` | Automática por `@dev` após story `Ready` | Liberado (Pacote 1) |
| 2 — Substituir mock no endpoint público | Automática por `@dev`, sem alterar contrato | Liberado (Pacote 1) |
| 3 — Validar CA-QT-19 (não-regressão) antes de tudo | Automática por `@dev`, gate bloqueante | Liberado (Pacote 1) |
| 4 — Interface de visualização e simulador | Automática por `@dev` após motor estável | Liberado (Pacote 1) |
| 5 — Resolver VER-QT-02/03 (catálogo fabricante) | Não executar — requer fonte externa não disponível | Bloqueado (Pacote 2) |
| 6 — Resolver VER-QT-07 (alínea EDP 6.2.7.1) | Não executar — requer confirmação da concessionária | Bloqueado (Pacote 3) |
| 7 — Resolver VER-QT-04 (fórmula bifásico) | Não executar — sem fonte normativa localizada | Bloqueado (Pacote 4) |

## 9. Critérios automáticos de bloqueio

O fluxo deve parar em `BLOCKED` quando ocorrer qualquer uma das condições:

- story ausente ou não validada;
- pacote alvo diferente do Pacote 1 sem nova fonte normativa confirmada;
- tentativa de alterar o contrato público (`RetornoMODQT`, `ValidarMODQTSchema`, rota do endpoint);
- tentativa de promover um item `[VERIFICAR]` (VER-QT-02/03/04/07) a `CONFIRMADO` sem fonte documentada;
- tentativa de executar `git push`, `gh pr create/merge`, ou deploy sem autorização explícita do usuário;
- três falhas repetidas no mesmo gate técnico;
- CA-QT-19 (não-regressão do mock) falhando sem causa normativa documentada;
- teste obrigatório sem execução ou sem resultado.

## 10. Critérios de sucesso do ciclo YOLO atual

O ciclo atual será considerado completo quando:

1. a story `MOD-QT-2-01` existir e estiver `Done`;
2. o motor real substituir `validarModQTMock` sem alterar o contrato público;
3. todos os `CA-QT-01` a `CA-QT-22` estiverem cobertos por teste (automatizado ou inspeção documentada);
4. `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passarem;
5. File List da story estiver atualizado;
6. QA emitir `PASS` ou `CONCERNS` tratável;
7. os Pacotes 2–4 permanecerem registrados como pendência explícita (`VER-QT-02`, `VER-QT-03`, `VER-QT-04`, `VER-QT-07`), sem implementação indevida;
8. `@devops` tiver preparado (não executado) o fechamento, aguardando autorização do usuário.

## 11. Log mínimo esperado

O arquivo `.aiox/logs/MOD-QT-2-01-yolo.log` deve registrar:

```text
[PREFLIGHT] fonte=PROMPT-QUEDA-TENSAO-v2.2.md pacote_1=PASS pacotes_2_4=BLOCK
[SM] story_created=docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md
[PO] validation=GO status=Ready
[DEV] implementation_started
[DEV] ca_qt_19_nao_regressao=PASS
[DEV] lint=PASS
[DEV] typecheck=PASS
[DEV] test=PASS
[DEV] build=PASS
[QA] gate=PASS|CONCERNS|FAIL
[DEVOPS] pre_push=READY|BLOCKED (execução real pendente de autorização do usuário)
```

## 12. Próxima ação automática

Iniciar o workflow pelo handoff:

```text
@sm *draft MOD-QT-2-01 --mode yolo --source "Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md"
```

Se a story for validada por `@po`, continuar automaticamente para:

```text
@dev *develop MOD-QT-2-01 --mode yolo
```

Se QA aprovar, continuar automaticamente para:

```text
@devops *pre-push --story MOD-QT-2-01 --mode yolo
```

Se qualquer gate bloquear (incluindo a barreira de push/deploy do §6.5), registrar o bloqueio e parar sem solicitar intervenção humana durante a execução — exceto pela autorização final de push/deploy, que é sempre um pedido explícito, mesmo em modo YOLO.
