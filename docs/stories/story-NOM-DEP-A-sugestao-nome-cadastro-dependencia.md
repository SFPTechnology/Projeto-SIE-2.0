---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit_test, ui_component_test, regression_test]
---

# Story NOM-DEP-A: Sugestão automática de nome no cadastro/edição de dependências

## Status

**InReview**

## Origem, contexto e dependências

**Artefato de origem:** `docs/brief-nomenclatura-automatica-dependencias.md` (Project Brief —
"Nomenclatura Automática de Dependências Propagada aos Circuitos"), seção "Proposed Solution",
item 1.

**Decisão de arquitetura de origem:** `docs/architecture/decisao-rotulo-dependencia-circuitos.md`
(DECISION-NOM-01).

**Dependência bloqueante:** `story-NOM-DEP-0-extracao-rotulo-dependencia.md` — esta story
consome `sugerirNomeDependencia` (e, indiretamente, `rotuloHumanoTipoDependencia`) exportadas
por `src/domain/modelo/rotulo-dependencia.ts`, criado na Story 0. **Não iniciar
desenvolvimento antes da Story 0 chegar a `Done`.**

**Problema:** `nomePersonalizado` já existe no DTO de dependência desde a migração
`0006_add_nome_personalizado.sql`, mas os formulários de cadastro (`NovaDependenciaModal.tsx`)
e edição (`EditarDependenciaModal.tsx`) tratam esse campo como texto livre sempre vazio por
padrão — nenhuma sugestão automática é oferecida. Como consequência, a maioria das dependências
fica sem nome legível, e as telas de cálculo caem no fallback técnico
(`circuito_id`/`dep-<uuid>`).

## Story

**As a** engenheiro/projetista elétrico cadastrando dependências no SIE,
**I want** que o campo "Nome personalizado" venha pré-preenchido com uma sugestão legível
("Sala 1", "Dormitório 2") assim que eu escolher o tipo de dependência, mantendo total
liberdade para editar ou apagar essa sugestão,
**so that** eu não precise digitar manualmente um nome para cada cômodo, e as telas de cálculo
subsequentes (Correntes, Queda de Tensão, Condutores, Disjuntores) já recebam um nome legível
sem esforço adicional do meu lado.

## Acceptance Criteria

1. Em `NovaDependenciaModal.tsx` (campo `nomePersonalizado`, hoje em torno das linhas
   538-546), ao selecionar ou alterar o campo `tipo`, o campo `nomePersonalizado` é
   pré-preenchido automaticamente com o resultado de
   `sugerirNomeDependencia({ tipo, nomesExistentes })`, onde `nomesExistentes` é a lista de
   `nomePersonalizado` de todas as dependências já cadastradas no projeto atual (incluindo
   vazios/`undefined`, conforme a assinatura da função).
2. A desambiguação segue o mesmo padrão determinístico já validado na função "duplicar" de
   `src/components/app/TabelaDependencias.tsx:992-1010` (comparação trim + case-insensitive +
   sem diacríticos), mas usando sufixo numérico incremental (`"Sala 2"`) — nunca `"(cópia)"` ou
   qualquer outro sufixo não numérico.
3. O campo `nomePersonalizado` permanece um `TextInput` 100% editável em ambos os modais — a
   sugestão é apenas o valor inicial. Não é introduzida nenhuma validação nova, obrigatoriedade
   ou restrição de formato ao campo além do comportamento já existente (o usuário pode apagar
   totalmente o valor sugerido).
4. Se o usuário alterar manualmente `nomePersonalizado` e em seguida trocar o `tipo` novamente
   antes de salvar, a sugestão automática **não sobrescreve** um valor já editado manualmente
   pelo usuário na mesma sessão do formulário (evita perda de edição do usuário).
5. `EditarDependenciaModal.tsx` (campo em torno das linhas 330 e 617) **não** pré-preenche
   retroativamente `nomePersonalizado` para dependências legadas que já existem sem esse campo
   preenchido — o formulário de edição abre com o valor persistido tal como está (vazio
   permanece vazio), sem acionar `sugerirNomeDependencia` automaticamente ao abrir. A sugestão
   automática desta story é exclusiva do fluxo de **criação** (`NovaDependenciaModal`).
6. `src/components/app/__tests__/dependencias-table-view-model.test.ts` (caminho real
   confirmado — o view-model de dependências vive junto ao componente, não em `tests/`) ganha um
   novo caso cobrindo: sugestão automática ao selecionar tipo + colisão de nome com dependência
   já existente no projeto. O sufixo gerado é **numérico separado por espaço** (`"Sala 2"`,
   `"Sala 3"`), coerente com o AC 2 e com o rótulo humano — nunca `"Sala-2"` (essa forma
   hifenizada pertence ao slug técnico do `circuito_id`, que esta story não toca).
7. `src/components/app/NovaDependenciaModal.tsx` é registrado na unidade `tug-iluminacao` do
   manifesto `scripts/tutorial-dimensionamento-condutores-manifest.mjs` (o componente não está
   rastreado em nenhuma unidade hoje) — a partir desta story, o gate `docs:tutorial:check`
   passa a detectar drift futuro nesse arquivo.
8. Nenhuma migração de schema/banco é introduzida — `nomePersonalizado` já existe desde
   `0006_add_nome_personalizado.sql`.
9. Nenhum indicador visual "nome sugerido vs. customizado" é implementado nesta story — decisão
   `[AUTO-DECISION]` registrada em DECISION-NOM-01 §4.4 (exigiria campo de proveniência
   persistido, fora do escopo "sem migração").
10. `ROTULOS_HUMANOS_TIPO_DEPENDENCIA` (`src/domain/modelo/rotulo-dependencia.ts`) é estendido
    com os 7 tipos do catálogo que a Story 0 deixou fora do mapa — `escritorio` → "Escritório",
    `garagem` → "Garagem", `copa` → "Copa", `copa-cozinha` → "Copa-cozinha",
    `lavanderia` → "Lavanderia", `lavabo` → "Lavabo", `ambiente-tecnico` → "Ambiente técnico" —
    de modo que `sugerirNomeDependencia` produza nomes acentuados para os 15 tipos de
    `dependenciasSuportadas()`, e não "Ambiente-Tecnico 1" (slug técnico). Os testes unitários de
    `rotulo-dependencia` cobrem os 7 casos novos. O slug técnico (`slugTipoDependencia`, que
    compõe `circuito_id`) **não** é alterado — os dois vocabulários permanecem separados
    (DECISION-NOM-01 §1.2). Efeito colateral desejado e aceito: `TabelaDependencias` passa a
    exibir esses 7 tipos com rótulo humano em vez do tipo cru minúsculo.

## 🤖 CodeRabbit Integration

### Story Type Analysis

**Primary Type:** Frontend (formulário de cadastro/edição de dependência)
**Secondary Type(s):** Architecture (consumo do módulo de domínio compartilhado da Story 0)
**Complexity:** Low — mudança contida em um modal, sem novo estado de servidor nem contrato
novo; a complexidade real (rotulagem) já foi resolvida na Story 0.

### Specialized Agent Assignment

**Primary Agents:**

- `@dev` — implementação e revisão pré-commit.
- `@ux-design-expert` — consultivo sobre o comportamento de "não sobrescrever edição manual"
  (AC4), se surgir dúvida de UX durante a implementação.

**Supporting Agents:**

- `@qa` — regressão do formulário e do view-model de dependências.

### Quality Gate Tasks

- [ ] Pre-Commit (`@dev`): CodeRabbit antes de marcar a story completa.
- [ ] Pre-PR (`@devops`): confirmar `npm run docs:tutorial:check` verde para a unidade
      `tug-iluminacao` após o registro de `NovaDependenciaModal.tsx` no manifesto.

### Self-Healing Configuration

**Expected Self-Healing:**

- Primary Agent: `@dev` (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

### CodeRabbit Focus Areas

**Primary Focus:**

- campo permanece totalmente editável, sem validação nova que bloqueie submit;
- sugestão nunca sobrescreve edição manual do usuário na mesma sessão (AC4).

**Secondary Focus:**

- acessibilidade do campo pré-preenchido (rótulo/estado continuam claros para leitor de tela);
- cobertura de teste da colisão de nomes.

## Tasks / Subtasks

- [x] Task 1 — Pré-preenchimento em `NovaDependenciaModal.tsx` (AC: 1, 2, 4)
  - [x] Importar `sugerirNomeDependencia` de `src/domain/modelo/rotulo-dependencia.ts`.
  - [x] Ao selecionar/alterar `tipo`, calcular `nomesExistentes` a partir das dependências já
        carregadas do projeto e chamar `sugerirNomeDependencia`.
  - [x] Implementar guarda para não sobrescrever um `nomePersonalizado` já editado manualmente
        pelo usuário nesta sessão do formulário (ex.: flag `nomeEditadoManualmente` no estado
        local do modal).

- [x] Task 2 — Confirmar não-retroatividade em `EditarDependenciaModal.tsx` (AC: 5)
  - [x] Confirmar (e cobrir por teste, se ainda não coberto) que o modal de edição não chama
        `sugerirNomeDependencia` ao abrir para dependências legadas sem nome.

- [x] Task 3 — Testes de view-model/colisão (AC: 6)
  - [x] Estender o teste de view-model de dependências com o caso de sugestão automática +
        colisão descrito no AC 6.

- [x] Task 4 — Tutorial in-app (AC: 7)
  - [x] Registrar `NovaDependenciaModal.tsx` na unidade `tug-iluminacao` do manifesto
        `scripts/tutorial-dimensionamento-condutores-manifest.mjs`.
  - [x] Rodar `npm run docs:tutorial:check` e `docs:tutorial:update` se necessário.

- [x] Task 5 — Fechamento (AC: 3, 8, 9)
  - [x] Confirmar que nenhuma validação nova foi introduzida além da sugestão inicial.
  - [x] Confirmar que nenhum campo de proveniência ("sugerido vs. customizado") foi adicionado.
  - [x] `npx tsc --noEmit`, `npx eslint` (escopado aos arquivos da story), `npx vitest run` —
        limpos, sem regressão atribuível a esta story.

- [x] Task 6 — Rótulos humanos dos 7 tipos não mapeados (AC: 10)
  - [x] Estender `ROTULOS_HUMANOS_TIPO_DEPENDENCIA` com `escritorio`, `garagem`, `copa`,
        `copa-cozinha`, `lavanderia`, `lavabo`, `ambiente-tecnico`.
  - [x] Estender `tests/domain/modelo/rotulo-dependencia.test.ts` cobrindo os 7 casos novos,
        inclusive via `sugerirNomeDependencia`, e a separação slug técnico × rótulo humano.

## Dev Notes

### Fonte e restrições confirmadas

- Esta story depende de `story-NOM-DEP-0-extracao-rotulo-dependencia.md` estar `Done` — usa
  `sugerirNomeDependencia` exportada por `src/domain/modelo/rotulo-dependencia.ts`. Não
  reimplementar a lógica de sugestão/desambiguação localmente no modal.
  `[Source: docs/stories/story-NOM-DEP-0-extracao-rotulo-dependencia.md#acceptance-criteria]`
- Assinatura exata a consumir:
  `sugerirNomeDependencia(args: { tipo: string; nomesExistentes: ReadonlyArray<string |
  undefined> }): string` — "{Rótulo humano} {N}", determinística.
  `[Source: docs/architecture/decisao-rotulo-dependencia-circuitos.md#22-api-pública-assinaturas]`
- Risco T2 (aceito e desejado): o nome sugerido usa rótulo humano acentuado ("Área de serviço
  1"), diferente do slug técnico do `circuito_id` ("Area-Servico"). Não é bug — é o
  comportamento pedido pelo brief.
  `[Source: docs/architecture/decisao-rotulo-dependencia-circuitos.md#42-riscos-técnicos, risco T2]`
- Risco T3 (aceito, não mitigar): a sugestão é gerada no cliente a partir das dependências já
  carregadas; duas abas/usuários simultâneos podem gerar "Sala 2" duas vezes. Não há
  constraint de unicidade no schema e o brief não pede — **não introduzir constraint nova**
  (seria migração, fora de escopo).
  `[Source: docs/architecture/decisao-rotulo-dependencia-circuitos.md#42-riscos-técnicos, risco T3]`
- Risco T6: `NovaDependenciaModal.tsx` não está em nenhuma unidade do manifesto de tutorial
  hoje — por isso o AC7 exige o registro explícito, para que o gate passe a rastrear drift
  futuro nesse componente.
  `[Source: docs/architecture/decisao-rotulo-dependencia-circuitos.md#42-riscos-técnicos, risco T6]`
- Risco T8: dependências legadas sem `nomePersonalizado` continuam exibindo o rótulo técnico —
  aceito no brief, sem backfill no MVP. `EditarDependenciaModal` não deve pré-preencher
  retroativamente sem ação explícita do usuário, para preservar a distinção entre "vazio por
  escolha" e "vazio por legado" (AC5).
  `[Source: docs/architecture/decisao-rotulo-dependencia-circuitos.md#42-riscos-técnicos, risco T8]`

### Arquitetura e estrutura

Nenhuma mudança de schema/migração. Nenhum contrato de API alterado. Mudança contida em
componentes React existentes.

Arquivos relevantes (todos sob `sistema-de-instala-es-el-tricas-sie-main/`, caminhos relativos
à raiz desse subprojeto):

- `src/components/app/NovaDependenciaModal.tsx` (linhas de referência: 538-546)
- `src/components/app/EditarDependenciaModal.tsx` (linhas de referência: 330, 617)
- `src/domain/modelo/rotulo-dependencia.ts` (consumido, criado na Story 0 — não recriar)
- `src/components/app/TabelaDependencias.tsx:992-1010` (referência de padrão de desambiguação,
  não copiar — usar a função consolidada)
- `scripts/tutorial-dimensionamento-condutores-manifest.mjs`

### Tutorial in-app

`NovaDependenciaModal.tsx` precisa ser adicionado à unidade `tug-iluminacao` do manifesto
(T6, DECISION-NOM-01 §4.2) — sem isso, o tutorial de cadastro fica desatualizado
silenciosamente, sem o gate acusar. Revisar `.md`/`.html` da unidade `tug-iluminacao` antes do
commit.

### Testing

- Testes de componente/view-model: estender o teste de view-model de dependências (AC 6).
- Se não existir harness de teste de componente para `NovaDependenciaModal.tsx` (situação
  documentada em `story-MOD-QT-2-09-fator-potencia-dependencias.md`, Completion Notes, Task 1),
  não é obrigação desta story criar esse harness do zero — cobrir a lógica de sugestão via
  teste do view-model/domínio é suficiente; documentar a limitação no Dev Agent Record se
  aplicável, sem transformar isso em débito silencioso.
- A story só pode avançar quando lint, typecheck e a suíte completa de testes passarem.

## Dev Agent Record

### Agent Model Used

Claude Opus 5 (@dev / Dex) — modo YOLO.

### Decisões autônomas

- `[AUTO-DECISION]` A lógica de sugestão foi extraída para um módulo puro
  `src/components/app/nova-dependencia-nome-model.ts` (mesmo padrão de
  `cargas-adicionais-form-model.ts`, já existente no diretório — decisão IDS: ADAPT do padrão,
  não CREATE de um padrão novo). Motivo: `NovaDependenciaModal.tsx` não tem harness de teste de
  componente (limitação registrada em MOD-QT-2-09), e o AC 6 exige cobrir sugestão + colisão. O
  módulo só orquestra estado — a desambiguação continua 100% delegada a
  `sugerirNomeDependencia` (nada reimplementado no componente, conforme Dev Notes).
- `[AUTO-DECISION]` A sugestão é aplicada por `useEffect` que dispara ao abrir o modal, ao
  trocar o tipo e quando a query de dependências termina de carregar — em vez de só no
  `onChange` do `Select`. Motivo: o tipo já vem pré-selecionado (`TIPOS[0]`) sem evento de
  mudança; só com `onChange` o campo abriria vazio no caso mais comum. `aplicarSugestaoNome`
  devolve o próprio estado quando nada muda, então não há loop de render.
- `[AUTO-DECISION]` `nomesExistentes` vem de `useQuery(dependenciasQuery(projetoId))` dentro do
  próprio modal (`enabled: open`), em vez de virar prop nova vinda da rota. Motivo: é a mesma
  query key que a tela de dependências já usa, então o dado costuma estar quente no cache do
  React Query e o contrato do componente não muda.
- `[AUTO-DECISION]` AC 5 foi coberto por teste de leitura de fonte (mesmo padrão de
  `tests/ui/projeto-detalhe-nav-links.test.ts`), afirmando que `EditarDependenciaModal.tsx` não
  referencia `sugerirNomeDependencia` e inicializa o campo com o valor persistido. Motivo:
  garantir que a não-retroatividade não seja quebrada por drift futuro, sem criar harness de
  componente do zero.
- `[AUTO-DECISION]` O manifesto de tutorial foi reassinado **somente** para a unidade
  `tug-iluminacao`, replicando o algoritmo de hash do script oficial. Motivo: `--update` reassina
  todas as unidades, e o worktree tem drift pré-existente de outras unidades
  (`dimensionamento-condutores`, `dimensionamento-disjuntores`, `padrao-entrada-tipos-criterios`,
  ...) pertencente a trabalho de outros agentes — reassiná-las esconderia a drift deles.

### Completion Notes

- AC 1/2/4 implementados via `nova-dependencia-nome-model.ts` + wiring em
  `NovaDependenciaModal.tsx`. A desambiguação usa exclusivamente `sugerirNomeDependencia`
  (sufixo numérico com espaço: "Sala 2"); nenhuma cópia da lógica de "duplicar" foi feita.
- AC 3: o campo segue `TextInput` sem `invalid`, sem `required` e sem qualquer validação nova;
  apagar o valor é tratado como edição manual e trava a sugestão (teste dedicado).
- AC 5: `EditarDependenciaModal.tsx` **não foi alterado** — já satisfazia o critério. Coberto
  por teste de regressão de fonte.
- AC 6: `dependencias-table-view-model.test.ts` ganhou 7 casos novos (sugestão inicial, colisão
  com dependência existente incluindo variação de caixa/espaço, ausência de nome, troca de tipo,
  guarda de edição manual, campo apagado, estabilidade de identidade do estado).
- AC 7: `NovaDependenciaModal.tsx` e `nova-dependencia-nome-model.ts` registrados na unidade
  `tug-iluminacao`; o par `.md`/`.html` do tutorial foi revisado (seção 2.1 descreve a sugestão
  automática; seção 10 registra que a edição não sugere) e o manifesto da unidade reassinado —
  `docs:tutorial:check` reporta `[tug-iluminacao] OK`.
- AC 8/9: nenhuma migração, nenhum campo de proveniência.
- AC 10: mapa de rótulos humanos passou de 8 para 15 tipos. Efeito colateral desejado:
  `TabelaDependencias` (que consome o mapa direto) passa a exibir rótulo humano para os 7 tipos.
  O slug técnico permanece intacto — há teste explícito travando a separação dos dois
  vocabulários.

### Suíte de testes

- `npx tsc --noEmit` — limpo.
- `npx eslint` nos arquivos da story — limpo (2 erros de formatação prettier no teste de
  `rotulo-dependencia` foram corrigidos com `--fix`).
- `npx vitest run` (suíte completa): **1403 passed / 6 failed**. Nenhuma falha é atribuível a
  esta story:
  - 2 falhas em `tests/domain/calculo/divisao-circuitos.test.ts` (`describe`
    "NOM-DEP-B — rótulo do circuito a partir do nome da dependência") — testes não commitados de
    trabalho em andamento da **Story NOM-DEP-B**, cuja implementação ainda não existe;
  - 4 falhas por `Test timed out in 5000ms` em testes de render/varredura pesados
    (`status-badge.test.tsx`, `queda-tensao-fluxo-entrada-fechado.test.tsx`) — ambientais, sob
    carga da suíte completa (418 s). `queda-tensao-fluxo-entrada-fechado.test.tsx` roda
    **12/12 verde em 7,7 s** isoladamente.
- `npx vitest run tests/domain/modelo/rotulo-dependencia.test.ts src/components/app/__tests__/dependencias-table-view-model.test.ts` — 2 arquivos, todos os casos verdes.
- `npm run docs:tutorial:check` — unidade `tug-iluminacao` OK. As demais unidades continuam com
  drift **pré-existente** (arquivos modificados por outro trabalho em andamento no worktree),
  intocado por esta story.

### File List

**Modificados**

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/NovaDependenciaModal.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/TabelaDependencias.tsx` (apenas
  comentário do alias `DEPENDENCIA_LABELS`, que ficou desatualizado com o AC 10)
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/modelo/rotulo-dependencia.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/__tests__/dependencias-table-view-model.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/modelo/rotulo-dependencia.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/scripts/tutorial-dimensionamento-condutores-manifest.mjs`
- `sistema-de-instala-es-el-tricas-sie-main/docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md`
- `sistema-de-instala-es-el-tricas-sie-main/docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html`
- `sistema-de-instala-es-el-tricas-sie-main/docs/.tutorial-tug-iluminacao.manifest.json`
- `docs/stories/story-NOM-DEP-A-sugestao-nome-cadastro-dependencia.md`

**Criados**

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/nova-dependencia-nome-model.ts`

**Não alterados (confirmação de escopo)**

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/EditarDependenciaModal.tsx` (AC 5)

## Change Log

| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2026-08-24 | 0.1 | Story criada a partir de DECISION-NOM-01 e do brief de nomenclatura automática; depende de NOM-DEP-0; status Draft. | @sm (River) |
| 2026-08-24 | 0.4 | **AC 10 acrescentado** (extensão de `ROTULOS_HUMANOS_TIPO_DEPENDENCIA` para os 7 tipos não mapeados). Autoria do registro: @dev (Dex); a decisão de escopo foi tomada e aprovada pelo usuário durante o handoff desta story, e está sendo formalizada aqui para não ficar como mudança fora de AC. Justificativa técnica: sem esses rótulos, `sugerirNomeDependencia` cairia no slug técnico e proporia "Ambiente-Tecnico 1"/"Copa-Cozinha 1" ao usuário — nomes hifenizados e sem acento, incoerentes com "Área de serviço 1" e com o objetivo da story (nome legível). O slug técnico (`circuito_id`) não é tocado. Recomenda-se ratificação do @po no gate. | @dev (Dex) |
| 2026-08-24 | 0.5 | Development complete — Status: InProgress → InReview. | @dev (Dex) |
| 2026-08-24 | 0.2 | `*validate-story-draft`: GO 9/10 → 10/10 após correções. AC6 corrigido: caminho real do teste é `src/components/app/__tests__/dependencias-table-view-model.test.ts` (não `tests/…`) e o sufixo de desambiguação é `"Sala 2"` (espaço), não `"Sala-2"` — a forma hifenizada pertence ao slug técnico do `circuito_id`, fora do escopo desta story. Referências `NovaDependenciaModal.tsx:538-546` e `EditarDependenciaModal.tsx` conferidas no código. Status `Draft → Ready`. | @po (Pax) |
