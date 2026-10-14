# Story NAV-NBR-1 — Conformidade da sequência de navegação com a NBR 5410

**Análise-fonte:** Auditoria `@analyst` (Atlas), 2026-08-07 — sequência das seções do menu lateral vs. NBR 5410 e prática de projeto elétrico. Achados 1 e 2.
**Workflow-fonte:** `.aiox-core/development/workflows/nav-sequencia-nbr5410-yolo.yaml` (Atlas, 2026-08-07)
**Contexto anterior:** `SIE-DS-09` (Done) implementou a navegação real de `module-navigation-data.ts` (AC8) — esta story trata da **outra** superfície de navegação, o menu lateral (`nav-model.ts`), e da coerência entre as duas.
**Status:** **Done**
**Created:** 2026-08-08
**Priority:** P2 (correção de conformidade normativa em superfície de navegação; sem impacto funcional em cálculo)

---

## 📖 Descrição

**Como** projetista elétrico usando o SIE,
**eu quero** que o menu lateral apresente as seções na ordem lógica em que a NBR 5410 exige que os cálculos sejam feitos, e que não atribua à NBR 5410 aquilo que é norma da concessionária,
**para que** percorrer o menu de cima para baixo corresponda a executar o projeto na ordem correta, e para que a nomenclatura resista a uma conferência de ART/CREA.

Dois defeitos foram identificados na auditoria de navegação:

**Achado 1 — inversão normativa.** O menu apresenta "Queda de tensão" **antes** de "Dimensionamento de condutores". Queda de tensão não é etapa que antecede a escolha da seção: é um dos critérios de 6.2.6, verificado **sobre uma seção já candidata**. O próprio código confirma a subordinação — `RequisicaoQuedaTensao` recebe `secao_mm2` como entrada obrigatória (`src/domain/queda-tensao/contratos.ts:32`), e o cabeçalho do mesmo arquivo declara que o contrato público do MOD-QT vive em `@/domain/dimensionamento-condutores/contratos`. Na arquitetura o MOD-QT já é subordinado ao dimensionamento; só na navegação ele aparece antes. O usuário que percorre o menu chega em "Queda de tensão" sem seção nenhuma para verificar.

**Achado 2 — agrupamento indevido.** O item "Padrão de entrada" está sob o rótulo **"Cálculo NBR 5410"**, mas seu próprio `hint` diz "Padrão de entrada EDP-SP" e seu domínio vive em `src/domain/distribuidora/edp-sp/`, fora de `src/domain/nbr/`. Padrão de entrada é governado pela norma técnica da concessionária, não pela NBR 5410.

**Evidência corroborante interna:** a navegação do Command Center (`src/components/command-center/module-navigation-data.ts`) já ordena `circuitos → correntes → condutores → queda` e já trata "entrada" como grupo separado. O produto contradiz a si mesmo em duas superfícies de navegação, e a do Command Center é a normativamente correta.

---

## ✅ Acceptance Criteria

- [x] **AC1 — Ordem do grupo de cálculo corrigida (Achado 1):** em `NAV_GROUPS`, no grupo `calculo` (`src/components/app/sie-shell/nav-model.ts`), a ordem dos itens passa a ser exatamente: `correntes`, `dimensionamento`, `queda-tensao`, `dimensionamento-disjuntores`. O item de dimensionamento de condutores precede o de queda de tensão; o de disjuntores permanece após ambos.
- [x] **AC2 — Identidade dos itens preservada:** para todos os itens movidos, os campos `id`, `label`, `hint`, `icon`, `to` e `requiresProjeto` permanecem byte-idênticos. Apenas a posição no array muda. Nenhuma URL de rota é alterada.
- [x] **AC3 — `padrao-entrada` extraído do grupo de cálculo (Achado 2):** o item `padrao-entrada` deixa de pertencer ao grupo cujo `label` é `"Cálculo NBR 5410"`, e passa a viver em um grupo novo contendo apenas ele.
- [x] **AC4 — Rótulo do grupo novo não atribui o item à NBR 5410:** o `label` do grupo novo identifica a origem normativa como a distribuidora/entrada de serviço e **não** contém a string `"NBR 5410"`.
- [x] **AC5 — Posição do grupo novo:** o grupo novo fica posicionado após o grupo `calculo` e antes do grupo `documentacao` no array `NAV_GROUPS`.
- [x] **AC6 — Grupo novo coerente com os demais:** o grupo novo tem `collapsible: true`, consistente com `projeto`, `calculo` e `documentacao`.
- [x] **AC7 — Razão normativa registrada em código:** `nav-model.ts` recebe comentários explicando (a) que queda de tensão é critério de 6.2.6 verificado sobre uma seção já candidata, com ponteiro para `secao_mm2` em `queda-tensao/contratos.ts`; e (b) que o padrão de entrada é regido pela distribuidora, com ponteiro para `src/domain/distribuidora/edp-sp/`. Um leitor futuro não deve poder "corrigir" a ordem de volta por ignorar a razão.
- [x] **AC8 — Regressão travada por teste (Achado 1):** `src/components/app/sie-shell/nav-model.test.ts` ganha asserção que **falha** se a ordem `condutores → queda` for invertida no grupo de cálculo.
- [x] **AC9 — Regressão travada por teste (Achado 2):** `nav-model.test.ts` ganha asserções que **falham** se `padrao-entrada` voltar ao grupo de cálculo, se o grupo que o contém passar a mencionar NBR 5410, ou se ele sair de sua posição relativa entre cálculo e documentação.
- [x] **AC10 — Testes asseveram sobre estrutura, não sobre texto de rótulo:** as asserções de ordem usam `id` de item e posição relativa de grupo. Rótulos podem evoluir sem quebrar os testes, exceto pela asserção negativa do AC4 (ausência de `"NBR 5410"`), que é a regra normativa em si.
- [x] **AC11 — `NAV_GROUPS` permanece fonte única:** `SieSidebar.tsx` continua consumindo a ordem diretamente de `NAV_GROUPS`, sem reordenação, filtro ou lista paralela.
- [x] **AC12 — Coerência entre superfícies de navegação:** a ordem resultante é comparada com `gruposNavegacao` (`module-navigation-data.ts`). Se a divergência for de ordenação pura, é eliminada. Se exigir alterar rótulos, escopo ou itens daquela superfície, **não** é alterada e a divergência é registrada como carry-forward justificado nas Dev Notes.
- [x] **AC13 — Zero impacto fora da navegação:** `git diff` vazio para `src/routes/**`, `src/routeTree.spa.ts`, `src/domain/**` e `src/api/**`.
- [ ] **AC14 — Gates obrigatórios verdes:** `lint`, `typecheck`, `test`, `build`, `build:spa` e `docs:tutorial:check` terminam com código 0 na mesma revisão. Falhas preexistentes no worktree (147 arquivos modificados / 74 untracked de outros épicos no baseline) são reproduzidas no baseline, registradas como não atribuíveis e **não** silenciadas.
  > **Deixado aberto deliberadamente por `@dev`.** Cinco dos seis gates saem com 0. `docs:tutorial:check` sai com 1 por drift 100% não atribuível (14 arquivos de outros épicos; zero manifesto referencia `sie-shell`/`nav-model`). Ao pé da letra o AC exige os seis em 0, e marcar como cumprido seria falso. A segunda frase do AC — registrar sem silenciar — **está** cumprida. Cabe a `@qa` decidir entre PASS com observação, CONCERNS, ou reformular o AC.
- [x] **AC15 — Gate de CodeRabbit reportado com honestidade:** se o binário permanecer indisponível (padrão desde `SIE-DS-00`, confirmado em `SIE-DS-07`/`SIE-DS-09`), a story declara isso explicitamente no fechamento em vez de afirmar revisão limpa.
- [x] **AC16 — Zero operação remota:** nenhum `git commit`/`push`/PR/merge executado por esta story.

---

## 📝 Scope

### IN

1. Reordenar os itens do grupo `calculo` em `NAV_GROUPS` para: correntes, dimensionamento (condutores), queda-tensao, dimensionamento-disjuntores.
2. Criar grupo novo para o item `padrao-entrada`, com rótulo que não o atribua à NBR 5410, posicionado após o grupo de cálculo e antes de `documentacao`.
3. Atualizar comentários de código de `nav-model.ts` para registrar a razão normativa da ordem.
4. Estender `nav-model.test.ts` com asserções de ordem e de agrupamento que travem a regressão.
5. Verificar e, se necessário, alinhar a ordem em `module-navigation-data.ts` para eliminar a divergência entre as duas superfícies.

### OUT

1. **Achado 3** da auditoria (lacunas: proteção contra choques/DR/aterramento, balanceamento de fases, quadro de cargas/memorial) — exige stories próprias com módulos de domínio. `src/domain/calculo/balanceamento-fases.ts` existe sem rota, mas expô-lo é decisão de produto.
2. **Achado 4** da auditoria (reposicionar Command Center para fora de "Documentação") — decisão de produto pendente de `@po`.
3. Qualquer alteração em rotas, `src/routes/**`, `src/routeTree.spa.ts` ou lógica de domínio.
4. Renomear paths de rota, `id` de item ou os tipos `RotaProjeto`/`RotaGlobal`.
5. Alterações visuais em `SieSidebar.tsx` além do que a mudança do modelo exigir.
6. Commit, push, PR, merge, release, deploy ou migration.

---

## 🔗 Dependências

- Nenhuma story bloqueante. `nav-model.ts` já está modificado no worktree por trabalho anterior não commitado — a implementação edita sobre o estado atual, sem reverter.

---

## 📊 Complexidade

**T-shirt: XS.** Reordenação de array e extração de grupo em um único arquivo de modelo, mais testes. Sem lógica nova, sem mudança de contrato, sem migração.

---

## 💰 Valor de negócio

Um projeto elétrico é entregue sob ART. A navegação de uma ferramenta de projeto é lida como afirmação de método: apresentar "Queda de tensão" antes do dimensionamento sugere uma ordem de cálculo que a NBR 5410 não sustenta, e rotular "Padrão de entrada" como cálculo NBR 5410 atribui à ABNT uma exigência que é da concessionária. Ambos são erros que um conferente técnico nota. O custo de correção é XS; o custo de credibilidade não é.

---

## ⚠️ Riscos

| Risco | Severidade | Mitigação |
|---|---|---|
| Divergência residual com `module-navigation-data.ts` se o alinhamento exigir mudar aquela superfície | Baixa | AC12 dá saída dupla: alinhar se for ordenação pura, ou registrar carry-forward justificado |
| Gates falharem por causa preexistente no worktree (147 M / 74 ??) | Média | AC14 exige reprodução no baseline antes de classificar como não atribuível; baseline capturado no preflight |
| Alguém reverter a ordem no futuro por não conhecer a razão | Média | AC7 (comentário em código) + AC8/AC9 (testes que falham na regressão) |
| CodeRabbit indisponível mascarar ausência de revisão | Baixa | AC15 exige declaração explícita em vez de silêncio |

---

## ✔️ Definition of Done

- [ ] AC1–AC16 satisfeitos e verificáveis.
- [ ] `nav-model.test.ts` falha quando a ordem é invertida (verificado por mutação temporária e revertido).
- [ ] Seis gates verdes na mesma revisão, com falhas preexistentes separadas das atribuíveis.
- [ ] Dev Agent Record, Completion Notes, Change Log e File List preenchidos.
- [ ] Veredito formal de `@qa` emitido com arquivo de gate.

---

## 🛠️ Dev Notes

### Forma final de `NAV_GROUPS`

```
GERAL              projetos, diagnostico
PROJETO            dependencias, circuitos
CÁLCULO NBR 5410   correntes → dimensionamento → queda-tensao → dimensionamento-disjuntores
ENTRADA DE SERVIÇO (EDP-SP)   padrao-entrada          ← grupo novo
DOCUMENTAÇÃO       unifilar, unifilar-diagrama, command-center
```

### AC12 — decisão sobre `module-navigation-data.ts`: **não alterado**, carry-forward justificado

Inspecionado `gruposNavegacao`. As duas contradições que esta story corrige **já não existiam** naquela superfície:

- grupo `dimensionamento`: `circuitos → correntes → condutores → queda` — condutores já precede queda ✅
- grupo `entrada`: já separado, título `"Entrada"`, sem menção a NBR 5410 ✅

Resta uma divergência de **posição de grupo**: o Command Center põe `entrada` **antes** de `dimensionamento`; o menu lateral põe depois. Reordenar isoladamente seria ordenação pura, mas o grupo `dimensionamento` daquela superfície também **não contém** `dimensionamento-disjuntores` — diferença de escopo/itens, não de ordem. Alinhar só a posição produziria uma superfície meio-alinhada e tocaria um arquivo de story `Done` (`SIE-DS-09`) sem ganho normativo. A completude do `ModuleNavigation` é questão do épico do Command Center.

**Carry-forward:** posição do grupo `entrada` e ausência de `dimensionamento-disjuntores` em `gruposNavegacao` — avaliar no épico do Command Center.

### Verificação de mutação (DoD)

Os testes foram provados vermelhos sob regressão, com `nav-model.ts` restaurado byte-a-byte depois (SHA-256 conferido: `2faa18886ef5cea7…`).

| Mutação | Efeito | Testes vermelhos |
|---|---|---|
| A — `queda-tensao` movido para antes de `dimensionamento` | reverte Achado 1 | **2** |
| B — `padrao-entrada` devolvido ao grupo `calculo`, grupo de entrada removido | reverte Achado 2 | **4** |
| (restaurado) | — | 0 / 23 verdes |

### Falha de gate não atribuível

`docs:tutorial:check` sai com **1**. Os 14 arquivos em drift são de MOD-PROT/MOD-QT/MOD-CC não commitados (`motor-selecao-protecao.ts`, `dimensionamento-condutores/**`, `servico-queda-tensao.ts`, `tomadas.ts`, `iluminacao.ts` …). Nenhum manifesto em `docs/.tutorial-*.manifest.json` referencia `sie-shell` ou `nav-model` (`grep -c` = 0 em todos). Esta story não pode causar nem corrigir esse drift; **não** foi executado `--update`, que reassinaria manifestos de outros épicos.

### Nota de método sobre o baseline

O baseline de testes foi disparado às 00:04:11, antes das edições, mas o vitest transforma arquivos sob demanda e provavelmente já leu o arquivo de teste editado — seu total de 1187 não serve como contagem pré-mudança confiável. O que está medido e vale: estado final = 166/166 arquivos, 1187/1187 testes, exit 0.

Uma falha observada em `catalogo-impedancia-completude.test.ts` (5156 ms contra o timeout padrão de 5000 ms do vitest) foi flake de contenção — três processos node em paralelo por decisão do operador. Isolado: 28/28 verde. Suíte completa re-executada sozinha: 1187/1187 verde.

---

## 📋 Tasks

- [x] **Task 1** — Reordenar itens do grupo `calculo` (AC1, AC2)
- [x] **Task 2** — Extrair `padrao-entrada` para grupo próprio (AC3, AC4, AC5, AC6)
- [x] **Task 3** — Registrar razão normativa em comentários (AC7)
- [x] **Task 4** — Estender `nav-model.test.ts` com asserções de regressão (AC8, AC9, AC10)
- [x] **Task 5** — Verificar coerência com `module-navigation-data.ts` (AC12)
- [x] **Task 6** — Executar os seis gates e separar falhas preexistentes (AC14)
- [x] **Task 7** — Fechamento: Dev Agent Record, File List, Change Log, transição de status (AC15, AC16)

---

## 🤖 Dev Agent Record

**Agente:** `@dev` (Dex), via workflow `nav-sequencia-nbr5410-yolo` orquestrado por `@aiox-master` (Orion)
**Modo:** YOLO, `local_only: true`

### Gates (mesma revisão, `nav-model.ts` SHA-256 `2faa1888…`)

| Gate | Exit | Nota |
|---|---|---|
| `lint` | 0 | 6 warnings / 0 errors, todos em `src/components/ui/**` (`react-refresh/only-export-components`), não atribuíveis |
| `typecheck` | 0 | — |
| `test` | 0 | 166/166 arquivos, 1187/1187 testes |
| `build` | 0 | client 16,29 s + server 14,13 s |
| `build:spa` | 0 | 11,54 s |
| `docs:tutorial:check` | **1** | preexistente, não atribuível — ver Dev Notes |

`build`/`build:spa` foram re-executados **após** a restauração pós-mutação; nenhum arquivo mudou entre eles e a suíte final.

### CodeRabbit (AC15)

**Indisponível — verificado, não presumido.** O binário existe (`/root/.local/bin/coderabbit`, 103 MB, 2026-07-21) mas aborta em qualquer invocação:

```
bash: line 1: 11 Illegal instruction (core dumped) ~/.local/bin/coderabbit --version
```

Mesmo blocker documentado em `SIE-DS-00`, confirmado em `SIE-DS-07`/`SIE-DS-09` e no gate `T2-SEM-MOTOR-1`. **Nenhuma revisão automática cobriu este diff.** Não há findings a reportar porque não houve execução — não porque o código passou limpo.

### Completion Notes

Mudança contida em dois arquivos, sem lógica nova. Nenhum `id`, `label`, `hint`, `icon`, `to` ou `requiresProjeto` foi alterado — só posição no array e comentários. `RotaProjeto`/`RotaGlobal` intocados. `SieSidebar.tsx` não precisou de mudança: consome `NAV_GROUPS.map` direto, então o grupo novo renderiza sozinho (AC11).

AC13 verificado por escopo de edição: as únicas edições de código desta sessão foram os dois arquivos em `sie-shell/`. Os marcadores `M` em `src/routes/`, `src/domain/` e `src/api/` são do baseline registrado no preflight (147 modificados / 74 untracked de outros épicos) e são anteriores a esta story.

---

## 📁 File List

| Arquivo | Ação |
|---|---|
| `sistema-de-instala-es-el-tricas-sie-main/src/components/app/sie-shell/nav-model.ts` | modificado — reordenação do grupo `calculo`, grupo `entrada-servico` novo, comentários normativos (+46 / −9) |
| `sistema-de-instala-es-el-tricas-sie-main/src/components/app/sie-shell/nav-model.test.ts` | modificado — helpers `grupo`/`posGrupo`/`posItem` e bloco `sequência normativa NBR 5410` com 9 testes (+83) |
| `docs/stories/story-NAV-NBR-1-sequencia-navegacao-nbr5410.md` | criado |
| `.aiox-core/development/workflows/nav-sequencia-nbr5410-yolo.yaml` | criado previamente (define este workflow) |

---

## 🧾 Change Log

| Data | Agente | Evento |
|---|---|---|
| 2026-08-08 | `@sm` (River) | Story criada a partir dos Achados 1 e 2 da auditoria de navegação; status Draft |
| 2026-08-08 | `@po` (Pax) | Validação 10/10 — veredito **GO**. Status **Draft → Ready** |
| 2026-08-08 | `@dev` (Dex) | Início da implementação. Status **Ready → InProgress** |
| 2026-08-08 | `@dev` (Dex) | Tasks 1–7 concluídas; 5 gates verdes, `docs:tutorial:check` falha preexistente não atribuível; CodeRabbit indisponível (Illegal instruction). Status **InProgress → InReview** |
| 2026-08-08 | `@qa` (Quinn) | Gate **CONCERNS**, score 88. 3 issues registradas (2 medium ambientais, 1 low). Status **InReview → Done** |

---

## 🧪 QA Results

**Revisor:** Quinn (Test Architect) · **Data:** 2026-08-08
**Gate:** `docs/qa/gates/NAV-NBR-1-sequencia-navegacao-nbr5410.yml`
**Veredito: CONCERNS** · Quality score **88** · Status recomendado: **Done**

### Verificações independentes

| Checagem | Resultado |
|---|---|
| Forma final de `NAV_GROUPS` | `geral → projeto → calculo → entrada-servico → documentacao` ✅ |
| Ordem do grupo de cálculo | `correntes → dimensionamento → queda-tensao → dimensionamento-disjuntores` ✅ |
| Identidade dos itens movidos (`label`/`hint`/`icon`/`to`/`requiresProjeto`) | inalterada ✅ |
| `RotaProjeto` / `RotaGlobal` | intocados ✅ |
| Mutação A (reverte Achado 1) | 2 testes vermelhos ✅ |
| Mutação B (reverte Achado 2) | 4 testes vermelhos ✅ |
| Restauração pós-mutação | hash e diff conferidos, 23/23 verde ✅ |
| Manifestos de tutorial × `sie-shell`/`nav-model` | zero referências, drift não atribuível ✅ |

### Por que CONCERNS e não PASS

Os dois achados normativos foram corrigidos corretamente, com regressão travada por teste comprovadamente vermelho sob mutação — isso é o que a story pedia, e está feito. O veredito não é PASS por duas lacunas **ambientais**, nenhuma delas atribuível ao diff:

1. **`docs:tutorial:check` sai com 1** (QA-NAV-001) — drift de MOD-PROT/MOD-QT/MOD-CC. Não bloqueia esta story, mas **bloqueará o commit dela**, porque o hook pre-commit roda a mesma checagem. Quem for commitar precisa saber disso.
2. **Nenhuma revisão automática cobriu o diff** (QA-NAV-002) — CodeRabbit aborta com `Illegal instruction`. Quarta story consecutiva assim; deixou de ser exceção e vira item de infraestrutura para `@devops`.

Há ainda uma divergência de baixa severidade entre as duas superfícies de navegação (QA-NAV-003), cuja decisão de **não** tocar `module-navigation-data.ts` a QA considera correta.

### Sobre AC14

O dev deixou o checkbox aberto em vez de marcá-lo. A leitura está correta — ao pé da letra o AC exige seis gates em 0, e isso não ocorre. A story é aceita mesmo assim porque a única falha é comprovadamente externa. A recusa em marcar o checkbox é disciplina de relato, não defeito.

### Nota sobre o baseline

A ressalva de método do dev sobre a contaminação do baseline é procedente e foi aceita: o total de 1187 do baseline não serve como contagem pré-mudança. Não afeta o veredito — o estado final é medido diretamente e não tem falha. A falha transitória de `catalogo-impedancia-completude` (5156 ms vs. timeout padrão de 5000 ms) foi corretamente diagnosticada como contenção e refutada por execução isolada (28/28) e re-execução limpa da suíte (1187/1187).
