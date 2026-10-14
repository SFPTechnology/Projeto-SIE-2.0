# QA Preflight SDC — Padrão Compatível EDP V9

**Data:** 2026-07-26  
**PRD avaliado:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Status do PRD no snapshot inicial:** `InReview`  
**Escopo:** prontidão documental para entrada de stories no Story Development Cycle (SDC)  
**Veredito do snapshot inicial:** `FAIL`

> **Estado vigente:** substituído pela reexecução de 2026-07-27 na seção 6:
> `PASS — SOMENTE PACOTE 1 PARA CRIAÇÃO DE STORIES`.

## 1. Decisão

Nenhuma story dos pacotes 1–8 está autorizada a entrar no SDC neste snapshot.

O bloqueador imediato é `RV-01`, ainda `PENDENTE`. O parecer PO determina que o
PRD 0.8 não pode ser convertido em stories implementáveis enquanto não houver
revalidação formal da versão corrente. Isso também preserva o princípio
constitucional de Story-Driven Development: nenhum código pode ser escrito sem
story válida, critérios de aceitação claros e rastreabilidade aprovada.

É permitido continuar somente com investigação e produção das evidências
necessárias para encerrar os gates.

## 2. Evidências determinantes

| Evidência | Estado | Efeito sobre o SDC |
|---|---|---|
| RV-01 | `PENDENTE` | Bloqueia a criação e implementação de stories de todos os pacotes |
| DP-10 | `APROVADO` | Fecha contrato e compatibilidade, mas o próprio ADR declara que não autoriza implementação |
| GP-01.1 | `PENDENTE` | Persona, papéis e jornada ainda não validados |
| GP-01.2 | `PENDENTE` | Fronteira da Release 1 sem aprovação formal completa |
| GP-01.3 | `PENDENTE` | Matriz de perfis e ações privilegiadas ausente |
| GP-01.4 | `PENDENTE` | Baselines e metas UX não capturados nem aprovados |
| GO-01A | `PENDENTE` / `NÃO APROVADO` | Bloqueia ativação da Release 1 |
| GO-01B e evidências de dados | Contribuição de dados `PARCIAL` registrada em `docs/architecture/GO-01B-EVIDENCIA-DADOS-EDP-V9.md`; GO-01B `NÃO APROVADO` | Bloqueiam remoção controlada no pacote 8 |

## 3. Matriz resumida de gates por pacote

| Pacote | Gates e evidências exigidos antes da saída do pacote |
|---|---|
| 1 — Fundação normativa e modelo | `RV-01`; `GN-01`; decisões `DP-01`, `DP-02`, `DP-03`, `DP-05`, `DP-06` e `DP-08` conforme ramo e caso; metadados normativos consistentes; testes de fronteira e estados explícitos |
| 2 — Motor de avaliação e contrato | Gates do pacote 1 aplicáveis; `DP-10`; testes do motor, cargas especiais, demanda, categoria, corrente, subcategoria e alternativas com motivo; delta conforme decisão `DP-02` |
| 3 — API, persistência, versionamento, CLI e observabilidade | `DP-01`, `DP-04`–`DP-08` e `DP-10`; avaliação, consulta e diagnóstico via CLI; migração reversível e idempotente; rejeição de estado obsoleto; auditoria e indicadores operacionais |
| 4 — Convergência dos consumidores | Gates anteriores aplicáveis; testes integrados garantindo as mesmas tensões, fases, categoria e subcategoria; bloqueio explícito por consumidor sem fallback genérico |
| 5 — Preparação da jornada e UI | `DP-01`, `DP-04`–`DP-07`, `DP-10`; `DP-02` para ativação do ramo delta; CLI e contrato funcionais antes da UI; regressão dos fluxos existentes |
| 6 — UI, relatório e auditoria | `GP-01.1`–`GP-01.4` integralmente aprovados; `DP-04`, `DP-07`, `DP-08` e `DP-10`; acessibilidade, perfis, estados bloqueados, relatório coerente e histórico reconstruível |
| 7 — Fechamento da Release 1 | `RV-01`, `GP-01` e `GO-01A` aprovados; consumidores convergentes; regressões do dead-end, relatório e auditoria; rollout, rollback operacional, homologação e observabilidade comprovados |
| 8 — Remoção controlada do legado EDP | `DP-09`, `DP-10` e `GO-01B` aprovados, incluindo `GO-01A` válido; evidências de dados, retenção, acesso, backup/restauração e suporte; inventário sem dependências EDP; dry run e rollback semântico comprovados |

## 4. Gates universais por story

Quando `RV-01` permitir o desdobramento, cada story deverá possuir:

- rastreabilidade para FR, NFR, constraints, AC e gates aplicáveis;
- critérios de aceitação verificáveis;
- estratégia de rollback compatível com a alteração;
- testes locais e regressão proporcional ao risco;
- checklist e File List atualizados;
- `npm run lint` sem erros;
- `npm run typecheck` sem erros;
- `npm test` sem falhas;
- `npm run build` concluído com sucesso;
- CodeRabbit sem issue `CRITICAL`;
- status elegível para revisão antes do gate QA.

## 5. Parecer de prontidão

| Uso | Parecer |
|---|---|
| Investigação documental e fechamento dos gates | `PASS` |
| Criação de stories implementáveis | `FAIL` |
| Implementação dos pacotes 1–8 | `FAIL` |
| Ativação da Release 1 | `FAIL` |
| Remoção do legado EDP / Release 2 | `FAIL` |

O preflight foi exclusivamente documental. Nenhuma suíte de código foi
executada, pois não existe story EDP V9 implementada e elegível para revisão.

— Quinn, guardião da qualidade

## 6. Reexecução vigente — RV-01, DP-01 e DP-05 aprovados

**Data:** 2026-07-27  
**PRD avaliado:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Status do PRD:** `Approved`  
**Escopo decisório recebido:** `REEXECUTE_QA_PREFLIGHT_FOR_PACKAGE_1`  
**Veredito:** `PASS — SOMENTE PACOTE 1 PARA CRIAÇÃO DE STORIES`  
**Gate global dos pacotes 1–8:** `CONCERNS — LIBERAÇÃO PARCIAL E SEQUENCIAL`

### 6.1 Evidências determinantes

| Evidência | Estado vigente | Efeito sobre a criação de stories |
|---|---|---|
| RV-01 | `APPROVED` | Remove o bloqueio universal de conversão dos pacotes em stories |
| DP-01 | `APROVADO — NÃO BLOQUEIA STORIES` | Libera o desdobramento do pacote 1; manifestação EDP e confirmação técnica continuam obrigatórias e fail-closed por projeto |
| DP-05 | `APROVADO — NÃO BLOQUEIA STORIES` | Deixa de bloquear os pacotes dependentes; catálogo físico e testes pertencem à execução futura |
| Handoff PM | `PACOTE 1 PRELIMINARMENTE ELEGÍVEL` | Delimita esta autorização formal ao pacote 1 |
| Demais gates | `POR PACOTE` | Não reabrem RV-01, mas continuam bloqueando os pacotes aos quais o PRD os vincula |

Este parecer substitui, dentro da autoridade de QA, as referências
`QA PREFLIGHT PENDENTE` e `QA FAIL` ainda preservadas no corpo histórico do
PRD. A sincronização textual dessas referências pertence ao próximo ciclo de
manutenção do artefato de produto e não reabre RV-01.

Hashes SHA-256 verificados no snapshot avaliado:

```yaml
evidence_snapshot:
  prd: A8E35E111A4F4529267250ACAB37714AD405D29606975AD22FE30E445A320395
  rv_01: 21E744E8F5F919EAB96CA534FB6F3DC271BF14E57099D1FC97E1902B08295C5A
  dp_01: CBA02B07C4A3792B6BCD657E2831CDFA48D82B5AE1F88E12175726A8373E2384
  dp_05: 8C5406320ED5C09B5DCA321C9C43D05408FF57E181EBBFE8309172D2C975CD8B
  architecture_consolidation: 542B482B8FA124BEA60B500F95513A3DD4E102910FB1D48DF31167BAF07FDB95
  normative_source: C2C3AC7C0A890FE369E0A357D03F0B162A5905ACBEE1610D717454A01CA8D542
```

### 6.2 Matriz de liberação para criação de stories

| Pacote | Parecer para criação de stories | Fundamentação |
|---|---|---|
| 1 — Modelo normativo e catálogo estrutural | `PASS — LIBERADO` | RV-01 e DP-01 aprovados; representação delta não depende do fechamento operacional de DP-02 |
| 2 — Demanda e avaliador de candidatos | `HOLD — NÃO LIBERADO NESTE HANDOFF` | Gates de decisão listados estão aprovados, mas o pacote depende do pacote 1 e o handoff PM vigente seleciona somente o pacote 1 |
| 3 — Contrato canônico e fachada | `HOLD — NÃO LIBERADO NESTE HANDOFF` | DP-10 está aprovado, porém o pacote depende dos pacotes 1–2 |
| 4 — API, persistência, versionamento, CLI e observabilidade | `BLOCK` | DP-04 e DP-07 permanecem pendentes; também depende do pacote 3 |
| 5 — Convergência dos consumidores | `BLOCK POR DEPENDÊNCIA` | Depende do pacote 4, atualmente bloqueado |
| 6 — Reestruturação da UI | `BLOCK` | DP-04, DP-07 e GP-01 permanecem pendentes; também depende dos pacotes 4–5 |
| 7 — Relatório técnico e auditoria consolidada | `BLOCK` | DP-04 e DP-07 permanecem pendentes; também depende do pacote 6 |
| 8 — Regressão ponta a ponta e remoção do legado | `BLOCK` | DP-09 e GO-01B permanecem não aprovados; também depende dos pacotes 1–7 |

`GO-01A` continua reprovado para **ativação da Release 1**, mas não é usado
como bloqueio artificial para criar a story do pacote 1. Da mesma forma, a
aprovação deste preflight não antecipa a autorização do pacote 8 nem permite
remoção do legado.

### 6.3 Handoff autorizado

Fica autorizado o handoff para `@sm`/`@po` criar as stories formais do
**pacote 1**, respeitando:

- rastreabilidade para FR, NFR, CR, AC, RV-01, DP-01 e demais gates
  efetivamente aplicáveis à story;
- referência versionada à fonte normativa e preservação de proveniência;
- estados fail-closed de DP-01, sem inferência de topologia por município ou
  endereço;
- critérios verificáveis para representação estrela 220/127 V e delta
  240/120 V;
- testes locais e de fronteira proporcionais ao escopo;
- rollback, checklist e File List.

Esta autorização é para **criação e validação das stories**, não para
implementação automática. `@dev` somente poderá iniciar após existir story
válida, com critérios claros, dependências aplicáveis satisfeitas e status
compatível com o SDC.

### 6.4 Decisão estruturada

```yaml
qa_preflight_reexecution_2026_07_27:
  prd_status: APPROVED
  rv_01: APPROVED
  dp_01: APPROVED_DOES_NOT_BLOCK_STORIES
  dp_05: APPROVED_DOES_NOT_BLOCK_STORIES
  story_creation:
    package_1: PASS
    packages_2_3: HOLD_SEQUENTIAL_NOT_IN_CURRENT_HANDOFF
    packages_4_8: BLOCKED_BY_PACKAGE_GATES_OR_DEPENDENCIES
  implementation_authorized_by_preflight: false
  release_1_activation_authorized: false
  legacy_removal_authorized: false
  next_agent: "@sm"
  next_action: "DRAFT_PACKAGE_1_STORIES"
```

O preflight permanece documental. Não existe implementação EDP V9 associada a
uma story liberada para revisão; por isso, este parecer não usa testes de código
como evidência de aprovação funcional.

— Quinn, guardião da qualidade

## 7. Snapshot histórico — reexecução anterior de RV-01

**Data:** 2026-07-26  
**Snapshot RV-01:** `281296F41B8E6D80A0B399A1E7A596F95751E922D93081269E7B86FE4F5C00EF`  
**Veredito:** `FAIL`

```yaml
qa_preflight_reexecution:
  prd_status: "InReview"
  rv_01: "PENDENTE"
  implementation_authorized: false
  story_creation_gate: "FAIL"
  development_gate: "FAIL"
  devops_handoff_gate: "FAIL"
```

A reexecução não encontrou nova evidência capaz de alterar o gate. GN-01 e
DP-03 continuam sem parecer do responsável técnico; DP-01, DP-04, DP-05,
DP-07 e DP-09 continuam sem o conjunto de decisões e evidências exigido;
GP-01 continua incompleto; GO-01A permanece reprovado e GO-01B não aprovado.

Não existem stories EDP V9 em `Ready` ou implementações EDP V9 em `InReview`.
Assim, os comandos de desenvolvimento, review de código e pre-push não possuem
candidato válido. Nenhum teste de código foi executado nesta etapa.

— Quinn, guardião da qualidade
