---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit_test, regression_test]
---

# Story DERIVAR-CIRCUITOS-1 — Regularizar derivação de circuitos para dependência sem resultado

**Status:** Done

> Validada por @po (Pax) em 2026-07-28 — veredito **GO**, checklist de 10 pontos: **9/10** (6 aprovados na entrega do @sm; 3 completados por correção do @po dentro da autoridade de PO sobre título/descrição/AC/escopo; 1 ressalva residual documentada em "Riscos"). Ver Change Log v0.2.

**Story ID:** `DERIVAR-CIRCUITOS-1`
**Épico:** nenhum — story standalone de regularização (a investigação descartou `MOD-CC` e `AUTO-OTI` como origem; ver seção "O que a investigação encontrou").
**Módulo:** `src/domain/calculo/derivar-circuitos.ts` (submódulo `sistema-de-instala-es-el-tricas-sie-main`)
**Executor:** @dev
**Quality Gate:** @qa
**Complexidade:** **XS (1 ponto)** — alteração restrita a um único arquivo de teste (`tests/domain/calculo/derivar-circuitos.test.ts`): 1 asserção substituída + 2 casos novos, com fixtures já existentes no próprio arquivo. Zero alteração de código de produção (Task 6). Nenhuma dependência de rede, banco, migração ou UI.
**Referência cruzada:** `BLK-DERIVAR-CIRCUITOS-01` (`.aiox/workflow-state/BLOCKER-DERIVAR-CIRCUITOS-REGRESSAO.yaml`), `PO-DIV-02` (`.aiox/handoffs/MOD-QT-2-01-po-addendum-to-qa.yaml`)
**Handoffs:** `.aiox/handoffs/DERIVAR-CIRCUITOS-1-sm-to-po.yaml` (consumido), `.aiox/handoffs/DERIVAR-CIRCUITOS-1-po-to-dev.yaml` (ativo)

## Valor de negócio

| Beneficiário | Valor entregue |
|---|---|
| **Usuário final (projetista elétrico)** | Uma dependência ainda em `RASCUNHO` continua exibindo, nas telas de Correntes e Divisor de Circuitos, as cargas adicionais que o projetista já cadastrou. O trabalho de cadastro não "some da tela" só porque o cálculo NBR ainda não foi rodado — comportamento hoje presente no código e agora protegido por teste (ver `PP-1`). |
| **Equipe de desenvolvimento** | Desbloqueia o gate técnico: `npm test` volta a fechar limpo (hoje `Test Files 1 failed | 125 passed`), destravando `@devops` para commit/push de **todo** o ciclo — inclusive das stories `MOD-QT-2-*`, que estão retidas por uma regressão de outro domínio. |
| **Processo (governança)** | Encerra a violação do Artigo III registrada em `BLK-DERIVAR-CIRCUITOS-01`: uma mudança de comportamento de domínio deixa de existir "por fora" do processo Story-Driven e passa a ter AC, cobertura e rastreabilidade. |

**Custo de não fazer:** a suíte permanece vermelha, o gate `@devops` permanece bloqueado, e o comportamento fica exposto a ser revertido silenciosamente por qualquer agente futuro que "conserte o teste vermelho" pelo caminho errado (revertendo o `src/`).

## Story

**As a** mantenedor do domínio de cálculo elétrico do SIE,
**I want** que o comportamento de `derivarCircuitos` para dependências sem `resultado` calculado seja formalizado em uma story com critérios de aceite e cobertura de teste correspondente,
**so that** o Artigo III (Story-Driven Development) deixe de ser violado, a suíte `npm test` volte a fechar limpa, e o comportamento hoje presente no código (não commitado) tenha rastreabilidade e proteção de regressão.

## Contexto

Em 2026-07-28, durante o preflight do workflow MOD-QT-2-RESOLUCAO-VERQT, o `@aiox-master` detectou que `src/domain/calculo/derivar-circuitos.ts` tem uma alteração de comportamento **não commitada** (3 inserções / 3 deleções) que não corresponde a nenhuma story, AC ou epic:

```diff
- if (!r || !vIlumTug) continue;
+ if (!vIlumTug) continue;

- const ilumVA = r.iluminacao.valor.vaTotal;
+ const ilumVA = r?.iluminacao.valor.vaTotal ?? 0;

- const tugVA = r.tomadas.valor.vaTotal;
+ const tugVA = r?.tomadas.valor.vaTotal ?? 0;
```

Isso mudou o comportamento de "dependência sem `resultado` é inteiramente ignorada" para "dependência sem `resultado` continua gerando circuitos de cargas adicionais (`ADD-*`), apenas os circuitos de iluminação (`ILUM-*`) e TUG (`TUG-*`) ficam a zero VA e são omitidos pelo guard `> 0`". O teste `tests/domain/calculo/derivar-circuitos.test.ts:85` ("dependência sem resultado é ignorada") não foi atualizado e está falhando (`Test Files 1 failed | 125 passed (126)` na suíte de baseline).

O `@po` já havia registrado (`PO-DIV-02`) que esse mesmo arquivo de teste chegou a estar com 0 linhas na worktree (281 deleções não commitadas). A restauração do arquivo — necessária para não perder cobertura — expôs esta regressão real, que o esvaziamento estava ocultando.

**Decisão do usuário (autorização explícita):** o novo comportamento do código é intencional e deve ser preservado. Esta story não reverte `derivar-circuitos.ts`; ela formaliza o comportamento com AC, atualiza o teste desatualizado e documenta o raio de impacto, para que a mudança deixe de existir "por fora" do processo Story-Driven.

### O que a investigação encontrou (e o que não encontrou)

- **Chamadores de `derivarCircuitos`:** único ponto de chamada é `resolverDivisaoCircuitos` em `src/domain/calculo/divisao-circuitos.ts:386`, usado por `src/domain/servicos/servico-corrente.ts` (tela de Correntes) e `src/domain/servicos/servico-divisao-circuitos.ts` (tela de Divisor de Circuitos). Em ambos os serviços, `fontes` é montado com `deps.map(d => ({ entrada: d.entrada, resultado: d.resultado }))` — ou seja, **todas** as dependências do projeto são enviadas, incluindo as que ainda estão em `RASCUNHO` (sem `resultado` calculado). Este não é um cenário artificial de teste; é o fluxo real de produção.
- **Papel de `cargasAdicionais`:** a função `cargasAdicionais()` em `src/domain/calculo/cargas-adicionais.ts` calcula os totais de VA diretamente de `entrada.cargasAdicionais` (nome, `vaUnitario`, `quantidade`), sem nunca depender de `resultado`. `derivarCircuitos` já seguia esse mesmo padrão para os circuitos `ADD-*` (usa `d.cargasAdicionais`, nunca `r.cargasAdicionais`). Arquiteturalmente, os circuitos de carga adicional nunca precisaram do motor NBR (`resultado`) para existir — apenas os circuitos `ILUM-*`/`TUG-*` dependem de `resultado` porque usam a área/perímetro calculados.
- **`docs/analysis/ANALISE-PLANEJADOR-DE-CIRCUITOS.md`** (2026-07-10, seção 4.3, submódulo) descreve o automático como "cada carga adicional válida pode gerar um circuito `ADD-*`", sem condicionar isso à presença de `resultado` — consistente com o comportamento novo, mas é uma análise, não uma AC formal.
- **`docs/stories/HANDOFF-CORRECAO-CIRCUITOS-TENSAO-INCOMPATIVEL-to-DEV.md`** (2026-07-21, repo raiz, de Atlas/@analyst para @dev) estabelece o princípio de produto "Nenhuma carga adicional cadastrada é perdida por causa da tensão incompatível" — **8º item da lista "Critérios de aceite"** (linha 75), no pipeline Correntes → MOD-DC. Mesma filosofia (não perder cargas adicionais cadastradas), mas trata exclusivamente de bloqueio por tensão incompatível. **Não menciona nem cobre o guard `!r`** e seu File List não inclui `derivar-circuitos.ts`.
  - *Correção de precisão aplicada por @po em 2026-07-28:* o rascunho do @sm citava esse documento como "Status: Done". O campo `**Status:**` do arquivo (linha 6) diz literalmente **"Ready for Dev"**; o que existe é uma seção de resultado posterior (linhas 148–150) descrevendo a implementação em pretérito. A rotulagem "AC8" também foi trocada por "8º item da lista de Critérios de aceite", que é o que o documento efetivamente contém — o documento não numera seus critérios.
- **Busca em `docs/stories/`, `docs/prd/` e `docs/analysis/`** (repo raiz e submódulo) por `derivar-circuitos`, `derivarCircuitos`, `cargasAdicionais` e `sem resultado`: nenhuma story, epic ou PRD contém uma AC que autorize explicitamente a remoção do guard `!r`. `MOD-CC` é o módulo de validação de curto-circuito (C3) — não tem relação com derivação de circuitos. `AUTO-OTI` trata de otimização de dimensionamento de condutores, não localizado como origem.
- **Conclusão da investigação:** existe uma motivação arquitetural plausível (cargas adicionais são, por design, independentes de `resultado`; e há um princípio de produto recente e explícito de não perder cargas cadastradas), mas **nenhuma AC formal confirma essa decisão para o caso específico de dependência sem `resultado`**. Não foi encontrada evidência para inventar uma motivação além dessa (Artigo IV). O Dev Agent Record desta story deve registrar a motivação real, se o @dev/@po tiverem contexto adicional não documentado; caso contrário, deve registrar explicitamente que o comportamento é preservado por decisão do usuário, sem origem documental localizada.
- **Correção factual em relação ao blocker:** `BLK-DERIVAR-CIRCUITOS-01` registra em `evidencia.teste_falhando.observado` que a chamada retorna "1 circuito ADD-Sala-Lampada". A execução real de `npx vitest run tests/domain/calculo/derivar-circuitos.test.ts` (verificada nesta investigação) mostra que o retorno tem **2 circuitos**: `ADD-Sala-Chuveiro` (tipo `tue`, 220 V, `tensao_resolucao.origem: "declarada"`) e `ADD-Sala-Lampada` (tipo `iluminacao`, 127 V, 200 VA). Os ACs desta story usam o valor verificado. Este campo do blocker não deve ser editado (fora do escopo de quem cria a story), mas o Dev Agent Record deve estar ciente da divergência.
- **Raio de impacto de uma eventual reversão:** buscas em `tests/` (padrão `{ entrada }` sem `resultado`) não encontraram nenhum outro teste automatizado que dependa do comportamento novo, além do próprio teste falhando na linha 85. Reverter o guard `!r` faria apenas esse teste voltar a passar, sem quebrar nenhum outro teste hoje verde. Em produção, porém, dependências em estado `RASCUNHO` (sem cálculo NBR ainda executado) deixariam de exibir circuitos `ADD-*` nas telas de Correntes e Divisor de Circuitos — comportamento sem cobertura de teste de integração hoje em nenhuma direção.

## PP-1 — Princípio de produto declarado por esta story

> **Adicionado por @po (Pax) em 2026-07-28 durante `*validate-story-draft`.** Esta seção é a correção da lacuna de rastreabilidade que o @sm identificou e havia transferido ao Dev Agent Record. Ver "Decisão do @po sobre rastreabilidade" abaixo.

**PP-1:** *Uma dependência que ainda não teve o cálculo NBR executado (sem `resultado`, tipicamente em estado `RASCUNHO`) **não perde** as cargas adicionais já cadastradas pelo projetista: essas cargas continuam derivando circuitos `ADD-*` normalmente. Apenas os circuitos que dependem do motor NBR — `ILUM-*` e `TUG-*`, calculados a partir de área/perímetro — deixam de ser emitidos, por não terem base de cálculo.*

### Fonte de PP-1 (rastreabilidade — Artigo IV)

| Elemento | Fonte | Natureza |
|---|---|---|
| **Autoridade da decisão** | Decisão explícita do dono do produto (usuário), 2026-07-28, registrada em `BLK-DERIVAR-CIRCUITOS-01` → `resolucoes_possiveis.R2` + `decisao`, e em `.aiox/handoffs/DERIVAR-CIRCUITOS-1-sm-to-po.yaml` → `decisao_do_usuario` | **Fonte primária.** É o requisito. |
| **Comportamento declarado** | Execução verificada de `npx vitest run tests/domain/calculo/derivar-circuitos.test.ts` em 2026-07-28 (2 circuitos `ADD-*`, nenhum `ILUM-*`/`TUG-*`) | **Observação verificada**, não presunção. |
| **Coerência arquitetural** | `src/domain/calculo/cargas-adicionais.ts` — VA de carga adicional sempre derivou de `entrada`, nunca de `resultado` | Corroboração. Não autoriza, mas confirma que PP-1 não contradiz o desenho. |
| **Coerência de produto** | `HANDOFF-CORRECAO-CIRCUITOS-TENSAO-INCOMPATIVEL-to-DEV.md`, 8º critério: "Nenhuma carga adicional cadastrada é perdida…"; `ANALISE-PLANEJADOR-DE-CIRCUITOS.md` §4.3: "cada carga adicional valida pode gerar um circuito `ADD-*`" | Corroboração. Escopos vizinhos, não sobrepostos. |

**O que PP-1 explicitamente NÃO afirma** (limite anti-invenção): não afirma que a remoção do guard `!r` foi motivada por PP-1 na origem. A motivação histórica do autor da mudança não commitada **permanece desconhecida** e nenhuma investigação a localizou. PP-1 é uma declaração de requisito **prospectiva**, feita agora pelo dono do produto sobre um comportamento observado — não uma reconstrução retroativa de intenção.

### Decisão do @po sobre rastreabilidade

O @sm concluiu que não existe AC/epic/PRD que autorize o comportamento e transferiu ao @dev a responsabilidade de registrar a motivação no Dev Agent Record. **Isso não é suficiente como único mecanismo de conformidade**, por duas razões:

1. **Autoridade.** `.claude/rules/agent-authority.md` e `story-lifecycle.md` reservam a edição de AC/escopo ao @po. Deixar a declaração do requisito para o Dev Agent Record equivale a pedir que o @dev origine um requisito de produto — fora da sua alçada. Se o requisito não está na story, ele não está em lugar nenhum com autoridade.
2. **Artigo IV, lido corretamente.** O Artigo IV proíbe *inventar* motivação ou fatos sem fonte. Ele não proíbe o dono do produto de **declarar** um requisito. A fonte de PP-1 é a autorização explícita do usuário, datada e registrada em dois artefatos versionados — é uma fonte real, não uma invenção. O que seria violação é o que a story anterior arriscava: afirmar que o comportamento "já era o desejado desde antes" sem evidência disso.

**Efeito:** os 4 ACs abaixo passam a rastrear para PP-1 (requisito desta story), e não mais para uma motivação a ser descoberta pelo @dev. A Task 5 é mantida, porém **rebaixada** de mecanismo de conformidade para registro complementar: se o @dev encontrar motivação histórica adicional, registra; se não encontrar, registra a ausência — em nenhum dos casos a conformidade da story depende disso.

## Acceptance Criteria (Gherkin)

> Todos os ACs abaixo rastreiam para **PP-1**. AC1 e AC2 definem o comportamento novo declarado; AC3 protege contra regressão do comportamento pré-existente; AC4 protege o único guard que permanece absoluto.

### AC1 — Dependência sem `resultado` e com cargas adicionais válidas emite somente os circuitos de carga adicional

```gherkin
Given uma fonte `{ entrada: entradaSala }` sem a propriedade `resultado`
And `entradaSala.cargasAdicionais` contém "Chuveiro" (tue, 5600 VA, tensaoFixa 220 V) e "Lampada" (iluminação, 100 VA x2)
And o padrão de fornecimento `padraoBi` (tensao_fase_neutro 127 V, tensoes_ofertadas [127, 220])
When `derivarCircuitos([{ entrada: entradaSala }], padraoBi)` é chamado
Then o retorno contém exatamente os circuitos "ADD-Sala-Chuveiro" (tipo "tue", 5600 VA, tensao_V 220) e "ADD-Sala-Lampada" (tipo "iluminacao", 200 VA, tensao_V 127)
And o retorno NÃO contém "ILUM-Sala" nem "TUG-Sala"
```

### AC2 — Dependência sem `resultado` e sem cargas adicionais retorna lista vazia

```gherkin
Given uma fonte `{ entrada: <dependência sem resultado> }` cuja `entrada.cargasAdicionais` é `[]` (ou ausente)
And um padrão de fornecimento com `vIlumTug` definido
When `derivarCircuitos` é chamado com essa fonte
Then o retorno é `[]`
```

### AC3 — Dependência com `resultado` mantém o comportamento inalterado (não regressão)

```gherkin
Given qualquer uma das fontes de teste já existentes em `tests/domain/calculo/derivar-circuitos.test.ts` que incluem `resultado`
When a suíte de testes é executada
Then todos os 11 testes atualmente verdes (que não sejam o da linha 85) continuam passando sem alteração de asserção
```

### AC4 — `vIlumTug` ausente continua sendo condição de skip total, independente de `resultado` ou cargas adicionais

```gherkin
Given um padrão de fornecimento (ou contrato EDP-SP) cujo `vIlumTug` resolvido é `undefined`
And uma dependência com `resultado` presente e com cargas adicionais válidas
When `derivarCircuitos` é chamado
Then o retorno é `[]`
And nenhum circuito ILUM-*, TUG-* ou ADD-* é emitido para essa dependência
```

## AC → Método de Verificação

| AC | Verificação | Onde |
|----|-------------|------|
| AC1 | Teste unitário substituindo a asserção da linha 84-86 do arquivo de teste | `tests/domain/calculo/derivar-circuitos.test.ts` |
| AC2 | Novo teste unitário com fonte sem `resultado` e `cargasAdicionais: []` | `tests/domain/calculo/derivar-circuitos.test.ts` |
| AC3 | Execução da suíte completa do arquivo (`npx vitest run tests/domain/calculo/derivar-circuitos.test.ts`) sem alterar as demais asserções | `tests/domain/calculo/derivar-circuitos.test.ts` |
| AC4 | Novo teste unitário com `PadraoFornecimento` sem `tensao_fase_neutro` (ex.: sistema `tri` só com `tensao_fase_fase`) combinado com `resultado` e cargas adicionais presentes | `tests/domain/calculo/derivar-circuitos.test.ts` |
| Gate geral | `npm test` fechando limpo (0 arquivos falhando) dentro de `sistema-de-instala-es-el-tricas-sie-main/` | Definition of Done |

## Tasks / Subtasks

- [x] **Task 1 — Corrigir o teste desatualizado da linha 85 (AC1, AC3)**
  - [x] Substituir a asserção de `it("dependência sem resultado é ignorada", ...)` (linha 84-86) por uma que reflita o comportamento verificado: retorno com `ADD-Sala-Chuveiro` e `ADD-Sala-Lampada`, sem `ILUM-Sala`/`TUG-Sala`.
  - [x] Renomear o `it` para descrever o comportamento real, ex.: `"dependência sem resultado emite apenas circuitos de carga adicional"`.
  - [x] Confirmar que os valores de tensão e potência do teste batem com a execução real (`tensao_V: 220` para o chuveiro, `tensao_V: 127` e `potencia_total_VA: 200` para a lâmpada).

- [x] **Task 2 — Adicionar caso "sem resultado e sem cargas adicionais" (AC2)**
  - [x] Criar novo `it` com uma dependência (pode reaproveitar `dorm1`/`dorm2` do teste de sufixo numérico ou nova fixture) com `cargasAdicionais: []` e sem `resultado`.
  - [x] Asserir `toEqual([])`.

- [x] **Task 3 — Adicionar caso "vIlumTug ausente" (AC4)**
  - [x] Criar um `PadraoFornecimento` de teste com `sistema: "tri"`, sem `tensao_fase_neutro`, apenas `tensao_fase_fase` e `tensoes_ofertadas` compatíveis.
  - [x] Chamar `derivarCircuitos` com `resultado` presente (ex.: `resultadoSala`) e `cargasAdicionais` válidas nessa fonte.
  - [x] Asserir `toEqual([])`, confirmando que o guard de tensão continua absoluto mesmo com `resultado` e cargas presentes.

- [x] **Task 4 — Validar a suíte completa (DoD)**
  - [x] Rodar `npx vitest run` (ou `npm test`) na raiz de `sistema-de-instala-es-el-tricas-sie-main/` e confirmar 0 arquivos falhando. — **Ressalva:** o arquivo desta story ficou verde, mas a suíte completa apresenta 6 arquivos falhando em `queda-tensao`/MOD-QT-2 (trabalho paralelo, untracked, fora do escopo desta story). Ver Dev Agent Record → "Gates executados".
  - [x] Rodar `npx eslint .`, `npx tsc --noEmit` e `npx vite build` (ou os scripts npm equivalentes) e registrar o resultado no Dev Agent Record.

- [x] **Task 5 — Registrar a motivação real (Artigo IV)**
  - [x] No Dev Agent Record, registrar se há motivação funcional adicional não documentada (ex.: necessidade do Planejador de Circuitos exibir cargas adicionais antes do cálculo NBR completo).
  - [x] Se nenhuma motivação adicional for encontrada, registrar explicitamente: "comportamento preservado por decisão do usuário; nenhuma AC/epic de origem localizada além desta story."

- [x] **Task 6 — Não alterar `derivar-circuitos.ts` (guarda de escopo)**
  - [x] Não modificar `src/domain/calculo/derivar-circuitos.ts`. Nenhum defeito real foi identificado durante a implementação; o arquivo de produção não foi tocado (`git diff --stat HEAD` permanece nos mesmos 3 inserções / 3 deleções pré-existentes).

## Dev Notes

### Arquivos relevantes (não exaustivo)

- `src/domain/calculo/derivar-circuitos.ts` — função sob análise; **não editar** (Task 6).
- `tests/domain/calculo/derivar-circuitos.test.ts` — único arquivo a ser editado por esta story; fixtures existentes: `padraoBi`, `entradaSala`, `resultadoSala`, `ref()`.
- `src/domain/calculo/divisao-circuitos.ts:386` — único chamador de `derivarCircuitos` (via `resolverDivisaoCircuitos`).
- `src/domain/servicos/servico-corrente.ts` e `src/domain/servicos/servico-divisao-circuitos.ts` — constroem `fontes` a partir de `ctx.repoDep.listar(...)`, incluindo dependências sem `resultado`.
- `src/domain/calculo/cargas-adicionais.ts` — referência de que cargas adicionais sempre dependeram apenas de `entrada`, nunca de `resultado`.
- `src/domain/modelo/padrao-fornecimento.ts` — `tensao_fase_neutro` é opcional (`Tensao | undefined`), usado no fixture do AC4.

### Testing

- Framework: Vitest. Rodar arquivo único com `npx vitest run tests/domain/calculo/derivar-circuitos.test.ts` durante o desenvolvimento; suíte completa com `npx vitest run` (ou `npm test`) antes de finalizar.
- Todos os comandos devem ser executados de dentro de `sistema-de-instala-es-el-tricas-sie-main/`.
- Não é necessário criar teste de integração para as telas de Correntes/Divisor de Circuitos nesta story (fora de escopo — ver abaixo); a lacuna de cobertura de integração fica registrada como débito conhecido.

## Fora de Escopo

- Qualquer alteração em `src/domain/queda-tensao/` ou nas stories `MOD-QT-2-01`, `MOD-QT-2-02`, `MOD-QT-2-03`, `MOD-QT-2-04`.
- Reverter ou alterar `src/domain/calculo/derivar-circuitos.ts` (salvo defeito real identificado e escalado, conforme Task 6).
- Alterar as telas de Correntes ou Divisor de Circuitos (`servico-corrente.ts`, `servico-divisao-circuitos.ts`, componentes de UI).
- Corrigir o bug de "circuitos bloqueados por tensão incompatível" (já tratado em `HANDOFF-CORRECAO-CIRCUITOS-TENSAO-INCOMPATIVEL-to-DEV.md`, Status Done).
- Criar testes de integração/E2E para o cenário de dependência `RASCUNHO` nas telas de Correntes/Divisor de Circuitos (registrado como débito conhecido, não como AC desta story).

## Definition of Done

Executar todos os comandos abaixo de dentro de `sistema-de-instala-es-el-tricas-sie-main/`:

- [x] `npm run lint` — sem novos erros introduzidos pela mudança. **PASS com ressalva ambiental:** `npx eslint tests/domain/calculo/derivar-circuitos.test.ts` retorna 329 erros, **todos** `prettier/prettier — Delete ␍` (uma ocorrência por linha do arquivo). Causa: `core.autocrlf=true` (índice `i/lf`, worktree `w/crlf`) — atinge todo arquivo do repositório igualmente, e não foi introduzido por esta story. **Zero** achados de qualquer outra regra.
- [x] `npm run typecheck` (`npx tsc --noEmit`) — **PASS** (saída vazia, exit 0).
- [x] `npm test` — **PARCIAL, por causa externa.** O arquivo desta story ficou **verde** (14/14). A suíte completa fechou em `Test Files 6 failed | 120 passed (126) — Tests 41 failed | 786 passed (827)`; **todos** os 6 arquivos falhando são do domínio `queda-tensao`/MOD-QT-2 (untracked, trabalho paralelo de outro @dev), fora do escopo desta story. Ver Dev Agent Record.
- [x] `npm run build` — **PASS** (`✓ built in 7.41s`).
- [x] Story atualizada com File List, Change Log e Dev Agent Record preenchidos pelo @dev.
- [x] `@po` valida a story (`*validate-story-draft`) antes da implementação. — Feito em 2026-07-28, veredito GO 9/10 (Change Log v0.2).

## File List (inicial)

- `docs/stories/story-DERIVAR-CIRCUITOS-1-dependencia-sem-resultado.md` (este arquivo)
- `tests/domain/calculo/derivar-circuitos.test.ts` (a ser modificado pelo @dev)

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-07-28 | 0.1 | Story criada a partir do blocker `BLK-DERIVAR-CIRCUITOS-01`, em modo YOLO autônomo, por decisão explícita do usuário de preservar o comportamento novo | River (@sm) |
| 2026-07-28 | 0.2 | Validação `*validate-story-draft` — veredito **GO 9/10**. **Status: Draft → Ready.** Correções de @po: (a) seção `PP-1` adicionada, declarando o princípio de produto como requisito rastreável com tabela de fontes e limite anti-invenção (Artigo IV); (b) seção "Decisão do @po sobre rastreabilidade" — a declaração do requisito deixa de ser delegada ao Dev Agent Record, e a Task 5 é rebaixada a registro complementar; (c) seção "Valor de negócio" adicionada (item 7 do checklist); (d) complexidade explicitada como XS/1 ponto (item 6); (e) correção de precisão sobre `HANDOFF-CORRECAO-CIRCUITOS-TENSAO-INCOMPATIVEL-to-DEV.md` (Status real "Ready for Dev", não "Done"; "AC8" → "8º item da lista de Critérios de aceite"); (f) divergência factual do blocker reconfirmada por reexecução e corrigida no artefato (1 → 2 circuitos, valor anterior preservado); (g) handoffs renomeados do prefixo incorreto `MOD-CC-DERIVAR-CIRCUITOS` para o story-id canônico. Nenhum AC funcional, task ou escopo alterado. Handoff ativo: `.aiox/handoffs/DERIVAR-CIRCUITOS-1-po-to-dev.yaml` | Pax (@po) |
| 2026-07-28 | 0.3 | **Status: Ready → InProgress.** Início de `*develop DERIVAR-CIRCUITOS-1 --mode yolo`. Handoff `.aiox/handoffs/DERIVAR-CIRCUITOS-1-po-to-dev.yaml` consumido | Dex (@dev) |
| 2026-07-28 | 0.4 | **Status: InProgress → InReview.** Implementação concluída: `tests/domain/calculo/derivar-circuitos.test.ts` atualizado (1 asserção substituída para AC1 + 2 testes novos para AC2/AC4 + comentário de rastreabilidade PP-1), único arquivo de produção do escopo (`src/domain/calculo/derivar-circuitos.ts`) **não** modificado (Task 6). Gates: teste escopado 14/14 PASS (era 1 failed | 11 passed); `tests/domain/calculo` 116/116 PASS; typecheck PASS; build PASS (7,41 s); lint escopado PASS com ressalva ambiental (329 erros, 100 % `prettier/prettier "Delete ␍"` por `core.autocrlf=true`, zero achados de outras regras). Suíte completa em `6 failed | 120 passed (126)` — **os 6 são do domínio `queda-tensao`/MOD-QT-2 (untracked, trabalho paralelo), nenhum atribuível a esta story**; efeito líquido desta story: −1 arquivo falhando. Task 5 (Artigo IV): nenhuma motivação histórica documental localizada (`git log` do arquivo sem menção; diff ainda não commitado, logo sem mensagem de commit/PR) — ausência registrada explicitamente, nada inventado. Handoff de saída: `.aiox/handoffs/DERIVAR-CIRCUITOS-1-dev-to-qa.yaml` | Dex (@dev) |
| 2026-07-29 | 0.5 | **Status: InReview → Done.** QA Gate executado (`*qa-gate DERIVAR-CIRCUITOS-1`, modo YOLO): veredito **CONCERNS**, quality_score **92**. Gate file: `docs/qa/gates/DERIVAR-CIRCUITOS-1-gate.yaml`. 4/4 ACs PASS com rastreabilidade verificada contra o arquivo de teste (AC3 verificado por diff: 50+/2−, as 2 deleções são o `it` obsoleto). Task 6 (guarda de escopo) confirmada byte a byte: `src/domain/calculo/derivar-circuitos.ts` segue em 3+/3− pré-existentes, nenhuma linha nova. Gates re-executados de forma independente pelo @qa: typecheck PASS; escopado 14/14 PASS; `tests/domain/calculo` 116/116 PASS; build PASS (8,74 s); suíte completa `1 failed | 128 passed (129)`; lint escopado PASS com ressalva ambiental (329 erros, 100 % `prettier/prettier "Delete ␍"`, controle em arquivo vizinho não tocado: 261 erros do mesmo perfil); `npx eslint .` NÃO VERIFICADO (fail-closed). Artigo IV PASS — os 7 commits do arquivo re-conferidos, ausência de motivação documental confirmada como estrutural, nada inventado. 3 ressalvas registradas, **nenhuma atribuível a esta story**: DC1-001 (timeout flaky em `queda-tensao/catalogo-impedancia-completude`, medium — bloqueia commit/push, não a story), DC1-002 (débito de cobertura de integração RASCUNHO, low), DC1-003 (lint de projeto travado + ruído CRLF, low). Blocker `BLK-DERIVAR-CIRCUITOS-01`: parte desta story **RESOLVIDA**; gate @devops **não** liberado automaticamente por causa de DC1-001. Handoff de saída: `.aiox/handoffs/DERIVAR-CIRCUITOS-1-qa-to-devops.yaml` | Quinn (@qa) |

## Dev Agent Record

### Agent Model Used

Dex (@dev) — Claude Opus 5 (`claude-opus-5`), modo YOLO autônomo, 2026-07-28.

### Debug Log References

- `.aiox/logs/DERIVAR-CIRCUITOS-1-yolo.log` — linhas `[DEV] ...`
- Handoff de entrada: `.aiox/handoffs/DERIVAR-CIRCUITOS-1-po-to-dev.yaml` (consumido)
- Handoff de saída: `.aiox/handoffs/DERIVAR-CIRCUITOS-1-dev-to-qa.yaml`

### Decisões IDS (Search → Decide → Log)

| Item | Busca executada | Decisão | Justificativa |
|---|---|---|---|
| Fixtures `padraoBi`, `entradaSala`, `resultadoSala`, `ref()` | Leitura integral de `tests/domain/calculo/derivar-circuitos.test.ts` | **REUSE** | Já existem no próprio arquivo e cobrem exatamente os dados dos ACs. Nenhuma fixture nova necessária para AC1/AC2. |
| Fixture com `vIlumTug` indefinido (AC4) | Grep por `sistema: "tri"` e por `tensao_fase_neutro` em `tests/` | **CREATE** (`padraoTriSemFaseNeutro`, local ao `it`) | Nenhum fixture existente omite `tensao_fase_neutro`; `src/domain/modelo/padrao-fornecimento.ts` declara o campo como opcional, então o objeto é type-safe sem ele. Mantido local ao teste para não ampliar a superfície do módulo. |
| Arquivo de produção | Leitura de `src/domain/calculo/derivar-circuitos.ts` | **NÃO TOCAR** | Task 6. Nenhum defeito real identificado — ver abaixo. |

### Gates executados (resultados reais)

| Gate | Comando | Resultado |
|---|---|---|
| Teste escopado | `npx vitest run tests/domain/calculo/derivar-circuitos.test.ts` | **PASS** — `Test Files 1 passed (1) | Tests 14 passed (14)`, 2,71 s. Antes: `1 failed | 11 passed (12)`. |
| Typecheck | `npm run typecheck` (`tsc --noEmit`) | **PASS** — saída vazia, exit 0. |
| Lint escopado | `npx eslint tests/domain/calculo/derivar-circuitos.test.ts` | **PASS com ressalva ambiental** — 329 erros, 100 % `prettier/prettier: "Delete ␍"` (verificado por `-f json`: `{"prettier/prettier":329}`, uma única mensagem distinta). Confirmado ambiental: `git config core.autocrlf` = `true` e `git ls-files --eol` dá `i/lf w/crlf` para este arquivo **e** para os arquivos vizinhos não tocados. Zero achados de qualquer outra regra. Duração ~64 s (não travou no modo escopado). `npx eslint .` (projeto inteiro) **não foi executado** — trava conhecida de 25+ min. |
| Domínio `calculo` | `npx vitest run tests/domain/calculo` | **PASS** — `15 passed (15) | 116 passed (116)`, 9,99 s. |
| Suíte completa | `npm test` | **6 failed | 120 passed (126)** — `Tests 41 failed | 786 passed (827)`, 250 s. |
| Build | `npm run build` | **PASS** — `✓ built in 7.41s`. |

### Sobre a suíte completa não fechar em 0 failed

O baseline informado no handoff (`Test Files 1 failed | 125 passed (126)`) **mudou entre a validação do @po e esta implementação**: o @dev que trabalha em paralelo no domínio `queda-tensao` adicionou arquivos de teste novos à worktree. Os 6 arquivos que falham hoje são:

- `tests/domain/queda-tensao/motor-queda-tensao.test.ts` (untracked)
- `tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts` (untracked)
- `tests/api/queda-tensao-endpoints.test.ts` (untracked)
- `tests/api/modulos-mod-qt-motor-real.test.ts` (untracked)
- `tests/api/modulos-mod-qt.test.ts`
- `tests/ui/queda-tensao.vrt.test.tsx` (untracked)

Evidências de que **não** são atribuíveis a esta story:

1. Todos pertencem a `queda-tensao`/MOD-QT-2 — domínio explicitamente proibido a este @dev (`blocked_for_dev` do handoff) e sem sobreposição de arquivos com o escopo desta story.
2. A falha dominante é `ErroQuedaTensao: familia_id ausente no contexto` lançado em `src/domain/queda-tensao/motores/motor-queda-tensao.ts:171` — nenhum caminho de código passa por `derivarCircuitos`.
3. `git status --short` mostra `src/domain/queda-tensao/` inteiro como **untracked** (`??`), isto é, trabalho em voo do agente paralelo.
4. O único arquivo alterado por esta story (`tests/domain/calculo/derivar-circuitos.test.ts`) passou de 1 falha para 0, e todo o diretório `tests/domain/calculo` está verde (116/116).

**Efeito líquido desta story sobre o gate técnico:** −1 arquivo falhando. O gate `npm test == 0 failed` só fecha quando o ciclo MOD-QT-2 paralelo também fechar. Nenhuma ação foi tomada sobre esses arquivos (proibição explícita do handoff).

### Task 5 — Motivação real (Artigo IV)

**Nenhuma motivação histórica documental foi localizada, e nenhuma foi inventada.** Investigação executada nesta implementação:

- `git log --oneline -- src/domain/calculo/derivar-circuitos.ts` — os commits que tocam o arquivo são `cb782d6` (identidade visual), `e7431ca` (FP iluminação descarga), `5374f45` (fluxo de correntes stories 7.1–7.4), `574ef8d`, `3d59bfb`/`4c186a3`/`80727db` ("Changes"/"Work in progress"). **Nenhum** menciona o guard `!r`, dependência sem `resultado` ou o comportamento em questão.
- `git diff --stat HEAD -- src/domain/calculo/derivar-circuitos.ts` — as 3 inserções / 3 deleções continuam **não commitadas**, ou seja, não existe mensagem de commit, PR ou revisão associada à mudança.
- Nenhum comentário no código de produção explica a remoção do guard.

**Registro conforme prescrito pela story:** *comportamento preservado por decisão do usuário; nenhuma AC/epic de origem localizada além desta story.* O requisito que hoje sustenta o comportamento é **PP-1**, declarado prospectivamente pelo dono do produto em 2026-07-28 e registrado por @po nesta story — não uma reconstrução retroativa de intenção. **Nenhuma motivação funcional adicional não documentada foi encontrada por este @dev.**

### Task 6 — Guarda de escopo

`src/domain/calculo/derivar-circuitos.ts` **não foi modificado**. A leitura integral do arquivo não revelou defeito real: com `r` ausente, `ilumVA`/`tugVA` caem em `?? 0` e os guards `> 0` omitem `ILUM-*`/`TUG-*`; as cargas `ADD-*` derivam de `d.cargasAdicionais`, que nunca dependeu de `resultado`. O comportamento observado é exatamente o descrito em PP-1. Nada a escalar.

### Completion Notes List

1. **AC1** — `it("dependência sem resultado emite apenas circuitos de carga adicional (AC1)")` substitui o `it` desatualizado da linha 84-86. Assere `ids toEqual ["ADD-Sala-Chuveiro", "ADD-Sala-Lampada"]`, `not.toContain("ILUM-Sala")`, `not.toContain("TUG-Sala")`, e os valores verificados: chuveiro `tue`/5600 VA/220 V/`tensao_resolucao.origem === "declarada"`/`trifasica === false`; lâmpada `iluminacao`/200 VA/127 V.
2. **AC2** — `it("dependência sem resultado e sem cargas adicionais retorna lista vazia (AC2)")` cobre **duas** variantes: `cargasAdicionais: []` e `cargasAdicionais` **ausente** (`undefined`, via rest destructuring), ambas `toEqual([])`. A segunda variante vai além do texto mínimo do AC e protege o `?? []` da linha 130 do módulo.
3. **AC3** — os 11 testes previamente verdes **não** tiveram nenhuma asserção alterada; nenhuma linha deles foi tocada. Confirmado pelo diff e pela execução (`14 passed` = 11 originais + 3 novos).
4. **AC4** — `it("vIlumTug ausente pula a dependência mesmo com resultado e cargas adicionais (AC4)")` usa `padraoTriSemFaseNeutro` (`sistema: "tri"`, `tensoes_ofertadas: [220, 380]`, `tensao_fase_fase: 380`, **sem** `tensao_fase_neutro`) combinado com `resultado: resultadoSala` e as cargas adicionais de `entradaSala` — asserindo `toEqual([])`. Confirma que o guard de tensão continua absoluto.
5. Comentário de bloco referenciando **PP-1** e a story foi adicionado acima do teste do AC1, para que um agente futuro que encontre esse teste entenda que o comportamento é intencional e não "conserte" o `src/` pelo caminho errado (risco nomeado na seção "Custo de não fazer").
6. Débito conhecido **não** endereçado (fora de escopo por decisão do @po, DEV-06): ausência de cobertura de integração para o cenário `RASCUNHO` nas telas de Correntes/Divisor de Circuitos.
7. Nenhum commit, push ou PR realizado — reservado a @devops após o QA gate.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/calculo/derivar-circuitos.test.ts` — **modificado** (1 teste substituído + 2 testes novos + comentário PP-1)
- `docs/stories/story-DERIVAR-CIRCUITOS-1-dependencia-sem-resultado.md` — **modificado** (Status, Tasks, DoD, Dev Agent Record, Change Log)
- `.aiox/handoffs/DERIVAR-CIRCUITOS-1-dev-to-qa.yaml` — **criado**
- `.aiox/logs/DERIVAR-CIRCUITOS-1-yolo.log` — **anexado** (linhas `[DEV]`)
- `.aiox/workflow-state/BLOCKER-DERIVAR-CIRCUITOS-REGRESSAO.yaml` — **atualizado** (`current_state`, `historico`, `next_agent`)

**Não modificado (confirmado):** `src/domain/calculo/derivar-circuitos.ts`.

## QA Results

**Revisor:** Quinn (@qa, Test Architect) — Claude Opus 5, modo YOLO autônomo
**Data:** 2026-07-29
**Gate file:** `docs/qa/gates/DERIVAR-CIRCUITOS-1-gate.yaml`
**Handoff de saída:** `.aiox/handoffs/DERIVAR-CIRCUITOS-1-qa-to-devops.yaml`

### Veredito: **CONCERNS** — quality_score **92**

Os 4 ACs estão cobertos por testes nomeados passando (14/14 no arquivo), a guarda de escopo da Task 6 foi respeitada (verificada por diff, byte a byte), typecheck e build passam. A única ressalva bloqueante para o push é externa: `npx vitest run` ainda não fecha em 0 arquivos falhando — 1 arquivo do domínio `queda-tensao` falha por **timeout intermitente**, comprovadamente verde quando executado isolado e **não atribuível a esta story**.

Status recomendado e aplicado: **Done** (com as ressalvas DC1-001, DC1-002 e DC1-003 registradas — nenhuma atribuível a esta story).

### Rastreabilidade AC → teste (verificada contra o arquivo, não contra a descrição)

| AC | Resultado | Evidência |
|----|-----------|-----------|
| **AC1** — dependência sem `resultado` emite somente `ADD-*` | **PASS** | `tests/domain/calculo/derivar-circuitos.test.ts:88` — `ids toEqual ["ADD-Sala-Chuveiro","ADD-Sala-Lampada"]`, `not.toContain("ILUM-Sala")`, `not.toContain("TUG-Sala")`; chuveiro `tue`/5600 VA/220 V/`origem: "declarada"`/`trifasica: false`; lâmpada `iluminacao`/200 VA/127 V. Confere com o Gherkin e com o valor corrigido do blocker (2 circuitos, não 1). Cobertura COMPLETA. |
| **AC2** — sem `resultado` e sem cargas adicionais → `[]` | **PASS** | Linha 109. Assere as **duas** variantes do "ou" do AC: `cargasAdicionais: []` e chave ausente (rest destructuring). Cobertura COMPLETA. |
| **AC3** — dependência com `resultado` inalterada (não regressão) | **PASS** | Verificado por **diff**, não por confiança: `git diff HEAD -- tests/domain/calculo/derivar-circuitos.test.ts` = 50 inserções / 2 deleções; as 2 deleções são exatamente as duas linhas do `it("dependência sem resultado é ignorada")` obsoleto. Nenhuma linha de qualquer outro `it` aparece no diff. 14 passed = 11 originais + 3 novos. |
| **AC4** — `vIlumTug` ausente continua skip total | **PASS** | Linha 118, fixture `padraoTriSemFaseNeutro` (`tri`, `[220,380]`, `tensao_fase_fase: 380`, sem `tensao_fase_neutro`) + `resultadoSala` + cargas adicionais → `toEqual([])`. Protege o único invariante que a mudança não commitada preservou — o teste de maior valor da story. |

`ac_gaps`: **nenhum**.

### Guarda de escopo (Task 6) — confirmada por diff

`git diff --stat HEAD -- src/domain/calculo/derivar-circuitos.ts` → `1 file changed, 3 insertions(+), 3 deletions(-)`. O `git diff HEAD` completo exibe **exatamente** as 3 hunks pré-existentes já catalogadas no blocker (linha 99 `!r || !vIlumTug` → `!vIlumTug`; linha 108 `r.iluminacao…` → `r?.iluminacao… ?? 0`; linha 119 idem para `tomadas`). **Nenhuma linha nova.** O @dev não tocou o `src/` — confirmado, não presumido. A story alterou apenas o arquivo de teste.

### Gates técnicos — todos re-executados de forma independente pelo @qa (2026-07-29)

| Gate | Comando | Resultado real |
|---|---|---|
| Typecheck | `npx tsc --noEmit` | **PASS** — saída vazia, exit 0 |
| Teste escopado | `npx vitest run tests/domain/calculo/derivar-circuitos.test.ts` | **PASS** — `Test Files 1 passed (1) | Tests 14 passed (14)`, 2,46 s (baseline do blocker: `1 failed | 11 passed (12)`) |
| Domínio `calculo` | `npx vitest run tests/domain/calculo` | **PASS** — `15 passed (15) | 116 passed (116)`, 10,03 s |
| Build | `npm run build` | **PASS** — `✓ built in 8.74s` |
| Suíte completa | `npx vitest run` | **FAIL NÃO ATRIBUÍVEL** — `Test Files 1 failed | 128 passed (129)` · `Tests 1 failed | 892 passed (893)`, 263,13 s |
| Lint escopado | `npx eslint tests/domain/calculo/derivar-circuitos.test.ts -f json` | **PASS com ressalva ambiental** — 329 erros, agregação `{"prettier/prettier": 329}`, **uma única** mensagem distinta (`Delete ␍`) |
| Lint projeto inteiro | `npx eslint .` | **NÃO VERIFICADO** (fail-closed) — trava conhecida de 25+ min |

**Divergência com o relato do @dev, registrada por transparência:** o @dev reportou `6 failed | 120 passed (126)`. O relato não era falso — era um retrato honesto do momento, com o ciclo paralelo MOD-QT-2-03 em voo (`familia_id ausente no contexto`). Aquele trabalho fechou depois. O número que vale neste gate é o re-executado (`1 failed | 128 passed`), não o herdado.

**Natureza da única falha remanescente:** `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts > AC3 > todos os campos exigidos… 1.563 registros` — `Error: Test timed out in 5000ms`. É **timeout, não asserção**. Re-execução isolada do mesmo arquivo: `Test Files 1 passed (1) | Tests 28 passed (28)`, 7,22 s. Nenhum caminho de código de `queda-tensao` passa por `derivarCircuitos`.

**Prova de causa ambiental do lint:** verificação de controle em arquivo vizinho **não tocado** por esta story (`tests/domain/calculo/corrente-circuitos.test.ts`): 261 erros, `{"prettier/prettier": 261}` — mesmo perfil, mesma regra única. Somado a `core.autocrlf = true` e `git ls-files --eol` = `i/lf w/crlf`, a conclusão é determinística: ruído de fim de linha do Windows. **Zero achados substantivos.**

### Artigo IV — qualidade do registro de motivação (Task 5): **PASS**

Verificação independente do @qa: re-executado `git log --oneline -- src/domain/calculo/derivar-circuitos.ts` → 7 commits (`cb782d6`, `e7431ca`, `5374f45`, `574ef8d`, `3d59bfb`, `4c186a3`, `80727db`), exatamente os 7 listados pelo @dev — nenhum inventado, nenhum omitido. Busca no corpo **e** assunto dessas mensagens por `resultado|guard|!r|rascunho`: nenhuma ocorrência. O diff do `src/` segue não commitado, logo a ausência de motivação documental é **estrutural**, não fruto de busca preguiçosa.

O @dev registrou a ausência em vez de fabricar uma justificativa plausível — que teria sido fácil, dado que a coerência arquitetural (`cargas-adicionais.ts` nunca dependeu de `resultado`) ofereceria uma narrativa convincente. Ele explicitamente não fez isso e ainda distinguiu **corroboração** de **autorização**. É o comportamento que o Artigo IV exige. A conformidade da story, ademais, não repousa sobre o Dev Agent Record: repousa sobre **PP-1**, declarado pelo @po com fonte primária datada e limite anti-invenção explícito.

*Ressalva do @qa:* PP-1 é um requisito **prospectivo** sobre um comportamento observado — legítimo e corretamente rotulado como tal. A story documenta com precisão o que **não** sabe (a motivação histórica do autor permanece desconhecida), e essa honestidade é o que torna a regularização defensável sob o Artigo III.

### 7 verificações de qualidade (story-lifecycle.md, Fase 4)

| # | Verificação | Resultado | Nota |
|---|---|---|---|
| 1 | Code review | **PASS** | Zero código de produção alterado. No teste: fixtures reusadas em vez de duplicadas; a única fixture nova (`padraoTriSemFaseNeutro`) é local ao `it` — decisão correta. Nomes de `it` carregam o ID do AC: rastreabilidade legível de dentro do arquivo. |
| 2 | Testes unitários | **PASS** | 14/14 no arquivo; 116/116 no domínio `calculo`. 3 testes novos para 3 ACs comportamentais. |
| 3 | Critérios de aceite | **PASS** | 4/4, verificados contra o arquivo de teste. |
| 4 | Sem regressões | **PASS** | Verificado por diff: 2 deleções, ambas do `it` obsoleto. Zero asserção pré-existente tocada. |
| 5 | Performance | **PASS** | Arquivo em 2,46 s; build em 8,74 s. Story sem código de produção. |
| 6 | Segurança (OWASP básico) | **N/A** | Nenhuma superfície de ataque tocada: arquivo de teste unitário de domínio puro, sem I/O, rede, banco, entrada de usuário ou renderização. |
| 7 | Documentação | **PASS** | Dev Agent Record, File List e Change Log completos e fiéis ao diff real (conferidos). O comentário de bloco PP-1 acima do teste do AC1 é mitigação de risco de processo bem posta: ancora o "porquê" exatamente onde um agente futuro ficaria tentado a "consertar" o `src/` pelo caminho errado. |

### Ressalvas (top issues) — **nenhuma atribuível a esta story**

| ID | Sev. | Categoria | Achado | Dono sugerido |
|---|---|---|---|---|
| **DC1-001** | medium | tests | `npx vitest run` não fecha em 0: `1 failed | 128 passed (129)`. Falha é **timeout (5000 ms)** em `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts`, não asserção — o mesmo arquivo passa 28/28 em 7,22 s isolado. **Não bloqueia a story; bloqueia commit/push.** Enquanto for flaky, torna o gate "suíte limpa" do @devops não determinístico — custo real maior que a falha em si. | @dev do ciclo MOD-QT-2 / @po |
| **DC1-002** | low | tests | Débito conhecido, explicitamente fora de escopo por decisão do @po: sem cobertura de integração para o cenário de dependência em **RASCUNHO** nas telas de Correntes e Divisor de Circuitos. PP-1 hoje está protegido apenas na camada unitária de `derivarCircuitos`. | @po (priorização) |
| **DC1-003** | low | code | `npx eslint .` permanece **não verificado** por trava de 25+ min, e o lint escopado é 100% ruído de CRLF. O lint de projeto é, na prática, inoperante como gate neste ambiente. Reincidente — mesma constatação do gate MOD-QT-2-02. Sugestão: `.gitattributes` com `* text=auto eol=lf` (ou `endOfLine: "auto"` no Prettier). | @devops |

### Efeito sobre o blocker `BLK-DERIVAR-CIRCUITOS-01`

**RESOLVIDO** no que toca a esta story: teste vermelho eliminado (14/14 verde, re-execução independente); Artigo III sanado (comportamento agora tem story, 4 ACs, PP-1 rastreável e cobertura de regressão); risco de reversão silenciosa mitigado pelo comentário PP-1 in-loco + AC4. Isso encerra a causa apontada por `QT201-001` e `QT202-001` (severity high nos gates MOD-QT-2-01 e MOD-QT-2-02) para o `npm test` exit 1.

**Ressalva explícita:** o gate @devops **NÃO fica automaticamente liberado**. DC1-001 (flaky de timeout em `queda-tensao`) ainda impede que a suíte feche em 0 de forma determinística. É outro item, de outro dono, e um blocker **novo e distinto** — não uma reabertura de `BLK-DERIVAR-CIRCUITOS-01`.
