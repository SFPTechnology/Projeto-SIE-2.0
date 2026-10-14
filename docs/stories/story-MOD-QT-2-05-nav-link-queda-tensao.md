---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit_test, render_test]
---

# Story MOD-QT-2-05: Link de Navegação para Queda de Tensão na Página de Detalhe do Projeto

## Status

**Done**

> Criada por @sm (River) em 2026-07-29, a partir do gap concreto levantado por @analyst (Atlas) após o fechamento do ciclo MOD-QT-2 (stories -01 a -04, todas `Done`). A tela `/projetos/:id/queda-tensao` existe, está registrada nas route trees, o build a inclui e a suíte de testes passa (947/947) — mas não há nenhum link de navegação até ela na página de detalhe do projeto. O usuário não consegue chegar na tela clicando; precisaria digitar a URL manualmente.

## Fonte e escopo

**Investigação de origem:** análise pós-ciclo do @analyst sobre a integração de navegação do MOD-QT-2 (não há documento de parecer formal para este achado — é um gap de UI observado diretamente no código, sem ambiguidade de interpretação).

**Evidência (já levantada, não re-investigar):**
- `src/routes/projetos.$projetoId.tsx`, bloco `<div className="deps-hero-links">` (linhas ~81-105 na versão atual): contém 5 links —
  1. "Padrão de entrada" — `<Link to="/projetos/$projetoId/padrao-entrada" params={{ projetoId }}>`
  2. "Correntes (IB)" — `<Link to="/projetos/$projetoId/correntes" params={{ projetoId }}>`
  3. "Dimensionamento de condutores" — `<a href={`/projetos/${projetoId}/dimensionamento-condutores`}>`
  4. "Planejador de circuitos" — `<a href={`/projetos/${projetoId}/circuitos`}>`
  5. "Unifilar" — `<a href={`/projetos/${projetoId}/unifilar`}>`
  Nenhum link para "Queda de tensão" existe nesta lista.
- A rota de destino já existe e funciona: `src/routes/projetos.$projetoId_.queda-tensao.tsx`, registrada em `src/routeTree.gen.ts` e `src/routeTree.spa.ts` (confirmado por grep — presente em ambas as route trees).
- Não há empty-state quebrado: se o usuário chegar na tela sem ter passado por "Padrão de entrada" → "Correntes" antes, a tela carrega vazia (array de circuitos `[]`), não crasha. Isso é fluxo esperado, **não é bug e não faz parte do escopo desta story**.

**Investigação adicional feita durante o draft desta story:**
- Não existe teste dedicado ao arquivo `src/routes/projetos.$projetoId.tsx` (hub de navegação da página de detalhe do projeto). Os testes de VRT existentes (`tests/ui/queda-tensao.vrt.test.tsx`, `tests/ui/dimensionamento-condutores.vrt.test.tsx`, `tests/ui/correntes-rastreabilidade.vrt.test.tsx`) cobrem as páginas de destino de cada módulo, não o hub em si. Portanto **não existe baseline de snapshot VRT para esta página** — ver decisão de AC4 abaixo.
- Motivo provável do padrão `<a href>` cru nos 3 últimos links (Dimensionamento, Circuitos, Unifilar): esses três destinos foram adicionados em momentos distintos do projeto (stories separadas, incluindo pelo menos uma migração incremental de rota — ver `docs/stories/story-9.4-rota-propria-planejador-circuitos.md`) e parecem ter copiado o padrão mais simples de link cru em vez de adotar o `<Link>` do TanStack Router já usado nos dois primeiros. Não há evidência de que o `<a href>` cru seja proposital (ex.: não há comentário no código, nem necessidade de full-page-reload documentada) — é dívida de padrão, não decisão de arquitetura.

## Story

**As a** engenheiro eletricista usando o SIE,
**I want** ver um link "Queda de tensão" na página de detalhe do projeto, ao lado dos demais links de módulo,
**so that** eu consiga navegar até o simulador de queda de tensão clicando, sem precisar digitar a URL manualmente.

## Acceptance Criteria

> **[PO] Método de verificação — leia antes das ACs.** Este repositório **não possui jsdom, happy-dom nem `@testing-library/*`** (confirmado por @po em `package.json`: nenhuma dessas dependências existe; não há `vitest.config.*` com `environment: "jsdom"`). O padrão real de teste de UI do projeto — declarado explicitamente no cabeçalho de `tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx` ("não há infraestrutura de browser/jsdom neste repositório") — é: (a) `renderToStaticMarkup` sobre **componentes puros exportados**, e (b) **asserção sobre o texto-fonte** do arquivo via `readFileSync`. O componente `ProjetoPage` **não é exportado** e depende de `Route.useParams()` + `useQuery`, portanto **não é renderizável** por nenhum dos dois caminhos sem alterar o arquivo de rota além do escopo XS. Consequentemente, as ACs abaixo são verificadas por **asserção de fonte + `tsc --noEmit`**, não por teste de render de DOM. Ver "Testing" em Dev Notes.

### AC1 — Link presente no bloco de navegação
```gherkin
Given o arquivo `src/routes/projetos.$projetoId.tsx` após a alteração
When o bloco `<div className="deps-hero-links">` é inspecionado
Then existe um elemento de link com o texto visível "Queda de tensão" e `className="deps-hero-link"` dentro desse bloco
```

### AC2 — Link aponta para a rota correta
```gherkin
Given o novo link "Queda de tensão"
Then ele é um `<Link>` do TanStack Router com `to="/projetos/$projetoId/queda-tensao"` e `params={{ projetoId }}`
And `npx tsc --noEmit` retorna exit 0
# A prova de que o literal de rota é válido é de nível de tipo: o <Link to> do TanStack Router
# é type-checked contra a route tree registrada; um literal inexistente ou grafado errado
# QUEBRA o tsc. Isso é verificação mais forte que uma asserção de string isolada.
```

### AC3 — Nenhuma regressão nos 5 links existentes
```gherkin
Given o bloco `deps-hero-links` após a alteração
Then os 5 links pré-existentes ("Padrão de entrada", "Correntes (IB)", "Dimensionamento de condutores", "Planejador de circuitos", "Unifilar") continuam presentes
And nenhum teve seu destino (`to`/`href`) alterado
And nenhum foi removido
And a ordem relativa entre eles não muda (o novo link é inserido, não reordena os existentes)
And a ordem final dos 6 links, na fonte, é exatamente: Padrão de entrada, Correntes (IB), Dimensionamento de condutores, Queda de tensão, Planejador de circuitos, Unifilar
```

### AC4 — Não regressão de snapshot VRT (condicional, documentado)
```gherkin
Given que não existe snapshot VRT baseline para `src/routes/projetos.$projetoId.tsx` no momento desta story (confirmado por investigação do @sm — ver seção "Investigação adicional" acima)
Then esta AC é N/A para esta story: não há snapshot a regenerar
And se o @dev, durante a implementação, encontrar um snapshot VRT desta página que não foi detectado nesta investigação, ele deve regenerá-lo deliberadamente (comando explícito de update, nunca `--u` silencioso em massa) e documentar isso no File List
```

## Decisão de posicionamento do link

**Posição escolhida: logo após "Dimensionamento de condutores", antes de "Planejador de circuitos".**

Ordem final do bloco `deps-hero-links`:
1. Padrão de entrada
2. Correntes (IB)
3. Dimensionamento de condutores
4. **Queda de tensão** ← novo
5. Planejador de circuitos
6. Unifilar

**Justificativa:** a ordem dos 3 primeiros links já reflete o fluxo real de dependência de dados do domínio (Padrão de entrada → Correntes → Dimensionamento de condutores), não uma ordem alfabética ou arbitrária. O motor de queda de tensão (MOD-QT-2) consome diretamente a saída do dimensionamento de condutores (seção/impedância do cabo escolhido — ver contrato herdado de `MOD-QT-2-01`/`-02`/`-03`, que depende do catálogo de impedância usado no dimensionamento). Colocar "Queda de tensão" imediatamente após "Dimensionamento de condutores" mantém a lista alinhada com a ordem de execução natural do projetista: dimensiona o condutor, depois verifica a queda de tensão resultante. "Planejador de circuitos" e "Unifilar" são artefatos de consolidação/visualização que fazem mais sentido ao final do fluxo, então permanecem nas últimas posições, apenas deslocadas em uma posição.

## Decisão de padrão de link (`<Link>` vs `<a>`)

**Decisão: usar `<Link>` do TanStack Router (mesmo padrão dos 2 primeiros links), não `<a href>` cru.**

**Justificativa:** a investigação não encontrou motivo técnico documentado para o uso de `<a href>` cru nos 3 links mais recentes (Dimensionamento, Circuitos, Unifilar) — nenhum comentário no código, nenhuma necessidade de full-page-reload identificada, nenhuma menção em stories relacionadas (`story-9.4-rota-propria-planejador-circuitos.md`) que justifique a escolha. Tudo indica que é dívida de padrão acumulada ao longo de stories distintas, não uma decisão de arquitetura. Como o CLAUDE.md do submódulo não define um padrão de link para esta página e a Constitution do AIOX (Artigo IV, "No Invention") não permite inventar uma justificativa que não existe, a escolha correta é seguir o padrão mais novo e tecnicamente superior já presente no mesmo arquivo (`<Link>` com roteamento client-side do TanStack Router, sem full-page-reload), reduzindo a inconsistência em vez de propagá-la. **Não é escopo desta story migrar os 3 links `<a href>` existentes para `<Link>`** — isso é dívida técnica pré-existente, fora do escopo XS desta story.

## CodeRabbit Integration

> `coderabbit_integration.enabled: true` em `.aiox-core/core-config.yaml` — seção completa abaixo.

### Story Type Analysis

**Primary Type**: Frontend
**Secondary Type(s)**: —
**Complexity**: XS — um único elemento JSX (`<Link>`) adicionado em um único arquivo (`src/routes/projetos.$projetoId.tsx`), sem alteração de domínio, rota ou lógica de negócio.

### Specialized Agent Assignment

**Primary Agents**:
- @dev (Dex): Implementação do link e do teste de render

**Supporting Agents**:
- @qa (Quinn): Verificação dos 4 gates técnicos e dos ACs

### Quality Gate Tasks

- [ ] Pre-Commit (@dev): Run before marking story complete
- [ ] Pre-PR (@github-devops): Run before creating pull request

### Self-Healing Configuration

**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: [CRITICAL, HIGH]

**Predicted Behavior**:
- CRITICAL issues: auto_fix (improvável nesta story dado o escopo XS)
- HIGH issues: document_as_debt se não resolvido em 2 iterações

### CodeRabbit Focus Areas

**Primary Focus**:
- Consistência de padrão de link (`<Link>` do TanStack Router, com `to`/`params`, não `<a href>`)
- Nenhuma alteração fora do arquivo `src/routes/projetos.$projetoId.tsx` e de um eventual arquivo de teste novo/estendido

**Secondary Focus**:
- Acessibilidade: o novo link deve ter o mesmo nível de acessibilidade dos demais (mesma classe `deps-hero-link`, texto visível, sem `aria-*` customizado que destoe dos vizinhos)
- Nenhuma regressão de contrato público (esta story não toca `RetornoMODQT`, schemas Zod, nem rotas de API — é puramente UI de navegação)

## Tasks / Subtasks

- [x] Task 1 — Adicionar o link de navegação (AC: 1, 2, 3)
  - [x] Subtask 1.1: Em `src/routes/projetos.$projetoId.tsx`, dentro do bloco `<div className="deps-hero-links">`, inserir um novo elemento `<Link to="/projetos/$projetoId/queda-tensao" params={{ projetoId }} className="deps-hero-link">Queda de tensão</Link>` imediatamente após o link "Dimensionamento de condutores" e antes do link "Planejador de circuitos"
  - [x] Subtask 1.2: Confirmar que os 5 links existentes permanecem inalterados (destino, texto, classe, ordem relativa entre si)
- [x] Task 2 — Cobertura de teste (AC: 1, 2, 3) — **[PO] reescrita: a instrução original prescrevia Testing Library, que não existe neste repositório**
  - [x] Subtask 2.1: Criar `tests/ui/nav-hub-projeto.test.tsx` (ou nome equivalente) usando **exclusivamente** o padrão real do projeto: `readFileSync` sobre `src/routes/projetos.$projetoId.tsx` + asserções sobre o texto-fonte. Espelhar o estilo de `tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx` (bloco AC7, que já faz asserção de fonte com `readFileSync`) — criado como `tests/ui/projeto-detalhe-nav-links.test.ts`
  - [x] Subtask 2.2: O teste deve extrair o trecho entre `deps-hero-links` e o fechamento do `</div>` correspondente e assertar: (a) presença do texto "Queda de tensão" (AC1); (b) presença de `to="/projetos/$projetoId/queda-tensao"` e `params={{ projetoId }}` no elemento correspondente (AC2); (c) que os 6 rótulos aparecem **nessa ordem exata** dentro do bloco (AC3); (d) que os destinos dos 5 links pré-existentes permanecem literalmente iguais aos de hoje (AC3)
  - [x] Subtask 2.3: **PROIBIDO** nesta story: instalar `jsdom`, `happy-dom`, `@testing-library/*` ou qualquer nova dependência; criar/alterar `vitest.config.*`; exportar `ProjetoPage` ou extrair o bloco de links para um componente novo só para viabilizar render. Se o @dev julgar que a asserção de fonte é insuficiente, ele deve **parar e escalar ao @po**, não expandir o escopo por conta própria — nenhuma proibição foi violada; asserção de fonte julgada suficiente
- [x] Task 3 — Gates técnicos (AC: 1, 2, 3, 4)
  - [x] Subtask 3.1: `npx tsc --noEmit` — deve retornar exit 0 → **exit 0**
  - [x] Subtask 3.2: `npx vitest run` completo — deve permanecer em 947/947 ou mais (nunca menos) → **950/950 (133 arquivos)**
  - [x] Subtask 3.3: `npx vite build` — deve completar sem erro → **built in 7.74s, exit 0**
  - [x] Subtask 3.4: `npx eslint` escopado ao(s) arquivo(s) tocado(s) (`eslint .` completo trava neste ambiente — documentado nas stories anteriores do ciclo MOD-QT-2; não é exigível rodar o comando completo) → **0 erros de regra real**; única saída é `prettier/prettier "Delete ␍"` em **todas as 146 linhas** do arquivo (artefato ambiental de `core.autocrlf=true` — ver Debug Log)
  - [x] Subtask 3.5: Se, e somente se, for encontrado um snapshot VRT pré-existente para esta página durante a implementação, regenerá-lo deliberadamente e documentar no File List (ver AC4) — **nenhum snapshot do hub encontrado**; nada regenerado

## Dev Notes

### Arquivo principal a tocar

`src/routes/projetos.$projetoId.tsx` — bloco `deps-hero-links`, linhas ~81-105 na versão do código consultada por esta story. O `projetoId` já está disponível no escopo do componente (usado pelos 2 primeiros `<Link>` existentes e pelos `params` do route loader).

### Padrão de referência (usar exatamente este, não o `<a href>` dos vizinhos mais recentes)

```tsx
<Link
  to="/projetos/$projetoId/padrao-entrada"
  params={{ projetoId }}
  className="deps-hero-link"
>
  Padrão de entrada
</Link>
```

O novo link deve seguir este padrão trocando apenas `to` e o texto:

```tsx
<Link
  to="/projetos/$projetoId/queda-tensao"
  params={{ projetoId }}
  className="deps-hero-link"
>
  Queda de tensão
</Link>
```

### Rota de destino (não tocar)

`src/routes/projetos.$projetoId_.queda-tensao.tsx` já existe, já está registrada em `src/routeTree.gen.ts` e `src/routeTree.spa.ts`. Confirmar apenas que o literal de rota usado no `to` (`/projetos/$projetoId/queda-tensao`) corresponde ao path real gerado pelo TanStack Router para esse arquivo — comparar com o padrão dos 2 links `<Link>` existentes, que já usam a mesma convenção de nomenclatura de arquivo com underscore (`_.`) para segmento não-aninhado.

### Testing

> **[PO] CORREÇÃO — o rascunho original desta seção estava factualmente errado.** Dizia "Vitest + Testing Library (padrão já usado no projeto)". **Testing Library não é usada neste projeto e não está instalada.** Verificação do @po: `package.json` não contém `@testing-library/*`, `jsdom` nem `happy-dom`; não existe `vitest.config.*` definindo `environment`. Seguir a instrução original levaria o @dev a instalar dependência nova numa story XS (violação de escopo) ou a travar. As instruções corretas estão abaixo e prevalecem.

- **Frameworks reais:** Vitest apenas. Sem DOM. Os testes de UI do projeto usam duas técnicas: `renderToStaticMarkup` (react-dom/server) sobre **componentes puros exportados**, e **asserção sobre texto-fonte** via `readFileSync`. Referência canônica: `tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx` — cujo próprio cabeçalho declara "não há infraestrutura de browser/jsdom neste repositório".
- **Por que asserção de fonte aqui:** `ProjetoPage` em `projetos.$projetoId.tsx` não é exportado e depende de `Route.useParams()` e `useQuery`. Torná-lo renderizável exigiria exportá-lo ou extrair o bloco de links para um componente novo — ambos fora do escopo XS "1 elemento JSX". A asserção de fonte cobre AC1/AC3 integralmente e AC2 no nível de literal; o `tsc --noEmit` cobre AC2 no nível de tipo (o `<Link to>` do TanStack Router é validado contra a route tree em tempo de compilação).
- **Localização:** `tests/ui/`. Os arquivos `*.vrt.test.tsx` ali cobrem as páginas de **destino** de cada módulo, não o hub. Não usar o padrão VRT para este teste.
- **Não criar teste de domínio.** Esta story não toca `src/domain/queda-tensao/` nem qualquer lógica de cálculo — nenhum teste de domínio deve ser criado ou alterado.
- **Gate de regressão:** a suíte completa (`npx vitest run`) deve continuar em 947/947 ou mais após a alteração. Uma queda no número de testes passando é motivo de FAIL no QA gate.

## Alinhamento com épico / PRD

- **Épico:** `docs/stories/EPIC-MOD-CC-SEC-QT.md` (`epic_id: MOD-CC-SEC-QT-1`, P0) — "MOD-CC/SEC/QT — Validação de Critérios Downstream (C3/C4/C5)". Esta story pertence ao ramo **C5 (Queda de tensão / MOD-QT)**.
- **Ressalva de escopo do épico (registrada, não bloqueante):** o épico lista em OUT "UI para configurar parâmetros de MOD-CC/SEC/QT". Esta story **não** é UI de configuração de parâmetros — é um link de navegação para uma tela já entregue e já aceita pelas stories MOD-QT-2-01 a -04 (todas `Done`). Portanto não conflita com o OUT do épico: é o fechamento de um gap de acesso à entrega existente, não escopo novo de produto.
- **Stories antecessoras (todas `Done`):** MOD-QT-2-01 (motor), -02 (endpoints + UI), -03 (catálogo de impedância), -04 (fluxo de entrada fechado + limites EDP). A tela existe e é funcional; falta apenas o acesso por navegação.
- **Rastreabilidade de dependência técnica (confirmada por @po no commit `1e18cc9`):** o critério C5 do MOD-DC é resolvido pelo retorno do MOD-QT e "pode exigir seção maior e revalidar a seção de fase". Isso comprova o acoplamento direto Dimensionamento → Queda de tensão que sustenta a decisão de posicionamento do link.

## Riscos

| # | Risco | Prob. | Impacto | Mitigação |
|---|-------|-------|---------|-----------|
| R1 | @dev tentar instalar `jsdom`/`@testing-library` para viabilizar um teste de render, estourando o escopo XS | **Média** (o rascunho original induzia a isso) | Alto — muda dependências do projeto numa story de 1 linha de JSX | Proibição explícita na Subtask 2.3 + seção Testing corrigida; instalar dependência nova é FAIL automático no QA gate |
| R2 | @dev "consertar de brinde" os 3 links `<a href>` vizinhos, migrando-os para `<Link>` | Média | Médio — mistura dívida técnica pré-existente numa story XS, polui o diff e amplia superfície de regressão | Já listado em "Fora de escopo"; AC3 exige que os 5 links pré-existentes fiquem literalmente inalterados |
| R3 | Literal de rota grafado errado no `to` (ex.: `$projetoId_` em vez de `$projetoId`) | Baixa | Baixo — quebra a navegação silenciosamente | `tsc --noEmit` falha (AC2): o `<Link to>` é type-checked contra a route tree; o erro não passa |
| R4 | Comportamento divergente entre build SSR e build SPA (`routeTree.gen.ts` vs `routeTree.spa.ts`) | **Baixa** | Alto se ocorrer — link quebrado só em produção Hostinger | @po confirmou que `/projetos/$projetoId/queda-tensao` está registrada em **ambas** as route trees; `npx vite build` no DoD cobre a regressão de build |
| R5 | Regressão na suíte por efeito colateral inesperado | Muito baixa | Médio | Gate de 947/947 ou mais no DoD |

## Fora de escopo

- Qualquer alteração em `src/domain/queda-tensao/`
- Qualquer alteração em `src/routes/projetos.$projetoId_.queda-tensao.tsx`
- Qualquer lógica de negócio, cálculo ou validação de domínio
- Migração dos 3 links `<a href>` existentes para `<Link>` (dívida técnica pré-existente, não desta story)
- Qualquer alteração de rota, route tree, ou registro de rota (`routeTree.gen.ts`, `routeTree.spa.ts`) — a rota já existe e já está registrada

## Definition of Done

- [x] AC1, AC2 e AC3 verificados por teste automatizado de **asserção de fonte** (padrão real do projeto — ver Testing), somado ao `tsc --noEmit` como prova de tipo para AC2 — `tests/ui/projeto-detalhe-nav-links.test.ts`, 3 testes, todos passando
- [x] Nenhuma dependência nova adicionada ao `package.json`; nenhum `vitest.config.*` criado ou alterado — `package.json` intocado nesta story
- [x] AC4 documentado como N/A (sem snapshot VRT pré-existente) ou, se aplicável, snapshot regenerado deliberadamente — N/A confirmado: `tests/ui/__snapshots__/` contém 5 snapshots, nenhum do hub
- [x] `npx tsc --noEmit` — exit 0
- [x] `npx vitest run` completo — 947/947 ou mais, nunca menos → **950/950**
- [x] `npx vite build` — sem erro
- [x] `npx eslint` escopado ao(s) arquivo(s) tocado(s) — exit 0 (`eslint .` completo não é exigível neste ambiente, conforme documentado nas stories MOD-QT-2-03/-04) — exit 0 desconsiderando `prettier/prettier` CRLF (artefato ambiental pré-existente, ver Debug Log); teste novo passa 100% limpo
- [x] File List atualizado pelo @dev com todos os arquivos criados/modificados
- [x] Nenhuma alteração fora do escopo declarado acima — `git diff --stat` do submódulo mostra `src/routes/projetos.$projetoId.tsx | 7 +` (apenas inserções), nenhum outro arquivo de código tocado por esta story

## PO Validation Record

**Validado por:** @po (Pax) — `*validate-story-draft`, modo YOLO autônomo, 2026-07-29
**Veredito:** **GO** — nota pré-correção **7/10**, pós-correção **10/10**

### Checklist de 10 pontos

| # | Critério | Pré | Pós | Nota |
|---|----------|-----|-----|------|
| 1 | Título claro e objetivo | ✅ | ✅ | — |
| 2 | Descrição completa (problema/necessidade) | ✅ | ✅ | Gap concreto, evidência de código citada |
| 3 | ACs testáveis | ❌ | ✅ | **Defeito material**: método de verificação prescrito (Testing Library) não existe no repo. Corrigido |
| 4 | Escopo bem definido (IN/OUT) | ✅ | ✅ | Seção "Fora de escopo" explícita |
| 5 | Dependências mapeadas | ✅ | ✅ | Rota de destino verificada pelo @po nas 2 route trees |
| 6 | Estimativa de complexidade | ✅ | ✅ | XS |
| 7 | Valor de negócio | ✅ | ✅ | Tela entregue e inacessível por clique |
| 8 | Riscos documentados | ❌ | ✅ | Ausente no rascunho. Seção "Riscos" (R1–R5) adicionada |
| 9 | Critérios de Done | ✅ | ✅ | + 1 item de guarda de dependências |
| 10 | Alinhamento com PRD/Épico | ⚠️ | ✅ | Rascunho citava só stories irmãs. Épico `MOD-CC-SEC-QT-1` vinculado, com ressalva de OUT tratada |

### Verificação independente contra o código real (não confiou na descrição da story)

| Alegação da story | Resultado |
|---|---|
| Bloco `deps-hero-links` com 5 links, 2 `<Link>` + 3 `<a href>` | ✅ **Confirmado** — `src/routes/projetos.$projetoId.tsx` linhas 81–105, exatamente como descrito |
| Rota destino `projetos.$projetoId_.queda-tensao.tsx` existe | ✅ **Confirmado** |
| Registrada em `routeTree.gen.ts` e `routeTree.spa.ts` | ✅ **Confirmado nas duas** — `path: '/projetos/$projetoId/queda-tensao'` |
| Não existe snapshot VRT para o hub | ✅ **Confirmado** — `tests/ui/__snapshots__/` tem 5 snapshots, nenhum do hub; nenhum teste referencia `deps-hero-link` |
| "Testing Library é o padrão do projeto" (Dev Notes) | ❌ **FALSO** — nenhum `@testing-library/*`, `jsdom` ou `happy-dom` no `package.json`; sem `vitest.config.*` com `environment` |

### Decisões do @sm — parecer do @po

**1. Posicionamento do link (após "Dimensionamento de condutores") — CONFIRMADO, concordo.**
Não apenas razoável: sustentado por evidência que o @sm não citou. O commit `1e18cc9` (MOD-DC, story DC-4) declara que o critério **C5 é resolvido pelo retorno do MOD-QT e "pode exigir seção maior e revalidar a seção de fase"** — ou seja, queda de tensão realimenta o dimensionamento. O acoplamento Dimensionamento ↔ Queda de tensão é o mais forte da lista, e adjacência na navegação reflete isso. Adicionei essa rastreabilidade à story. Registro uma observação não-bloqueante: a lista atual já não é estritamente ordenada por dependência (divisão de circuitos precede o dimensionamento no fluxo real de projeto, mas aparece depois dele). Isso é inconsistência **pré-existente** e reordenar é vetado por AC3 — fica como dívida separada.

**2. `<Link>` vs `<a href>` — CONFIRMADO, mantido `<Link>`.**
Investiguei por conta própria em vez de aceitar o "não achei motivo" do @sm. Resultado: **não há motivo técnico real.** (a) Nenhum comentário no código justificando; (b) `git log -S` mostra que os **3** `<a href>` entraram **no mesmo commit** `1e18cc9`, e não em stories distintas como o rascunho supunha — é um único episódio de drift, não padrão acumulado; (c) as três rotas de destino **já existiam e já estavam registradas** na route tree naquele commit, então a hipótese "usou `<a>` porque `<Link to>` não compilaria ainda" está **descartada**; (d) nenhum `window.location`/full-reload deliberado no arquivo. Conclusão: drift de estilo. `<Link>` é a escolha correta, e não migrar os 3 vizinhos continua fora de escopo.

**3. AC4 (VRT) N/A — CONFIRMADO.**
Verifiquei o diretório de snapshots: existem 5 (`correntes-rastreabilidade`, `edp-sp-isolacao`, `queda-tensao`, `unifilar-canvas`, `unifilar-workspace`) e **nenhum** corresponde ao hub. Nenhum teste em `tests/` referencia `deps-hero-link` ou renderiza `ProjetoPage`. O snapshot `queda-tensao.vrt.test.tsx.snap` é da página de **destino**, que esta story não toca. AC4 permanece N/A, com a cláusula de contingência do @sm mantida.

### Correções aplicadas pelo @po (autoridade sobre Título/Descrição/AC/Escopo)

1. **[Bloqueante, corrigido]** ACs e Dev Notes prescreviam Testing Library — infraestrutura inexistente. Substituído pelo padrão real (asserção de fonte + `tsc --noEmit` como prova de tipo para AC2). Sem essa correção o @dev em YOLO instalaria dependência nova numa story XS ou travaria.
2. Task 2 reescrita com proibição explícita de instalar dependências / alterar config de teste / exportar `ProjetoPage`, e ordem de escalar ao @po em vez de expandir escopo.
3. AC3 reforçada com a ordem final explícita dos 6 links.
4. Seção "Riscos" (R1–R5) adicionada.
5. Seção "Alinhamento com épico / PRD" adicionada, incl. tratamento da cláusula OUT do épico.
6. DoD acrescido da guarda de dependências.

## Change Log

| Date | Version | Description | Author |
|------|---------|--------------|--------|
| 2026-07-29 | 0.1 | Story criada a partir de gap de navegação identificado por @analyst (Atlas) pós-fechamento do ciclo MOD-QT-2 | @sm (River) |
| 2026-07-29 | 0.2 | `*validate-story-draft`: GO (7/10 pré-correção → 10/10 pós). Corrigido defeito bloqueante de método de teste (Testing Library inexistente no repo); Task 2 reescrita; ACs 2 e 3 reforçadas; seções Riscos e Alinhamento com épico adicionadas; DoD ampliado. 3 decisões do @sm confirmadas com verificação independente | @po (Pax) |
| 2026-07-29 | 0.3 | **Status: Draft → Ready.** Liberada para `*dev-develop-story` | @po (Pax) |
| 2026-07-29 | 0.4 | **Status: Ready → InProgress.** Início de `*dev-develop-story` (modo YOLO autônomo) | @dev (Dex) |
| 2026-07-29 | 1.0 | **Status: InReview → Done.** `*qa-gate`: **CONCERNS** (score 95/100). 4/4 ACs verificados por reexecução independente — todos os números do @dev conferiram (+7/-0, 950/950 em 133 arquivos, 146 erros de lint, 5 snapshots). Caveat de CRLF **provada** ambiental (mesmo modo de falha em `src/routes/index.tsx`, arquivo limpo no git, com 140/140 erros idênticos), não FAIL. Ressalva única: `eslint .` completo NÃO VERIFICADO (trava ambiental). Nenhuma correção exigida. Gate: `docs/qa/gates/MOD-QT-2-05-gate.yaml` | @qa (Quinn) |
| 2026-07-29 | 0.5 | **Status: InProgress → InReview.** Link `<Link>` "Queda de tensão" inserido no bloco `deps-hero-links` na posição 4/6; teste de asserção de fonte criado (3 casos, AC1/AC2/AC3); gates: tsc exit 0, vitest 950/950, vite build OK, eslint escopado sem erro de regra real. AC4 N/A confirmado. Handoff para @qa | @dev (Dex) |

## Dev Agent Record

### Agent Model Used

claude-opus-5 (@dev / Dex), modo YOLO autônomo

### Debug Log References

- `.aiox/logs/MOD-QT-2-05-yolo.log` — linhas `[DEV]`
- **Achado ambiental (não é regressão desta story):** `npx eslint src/routes/projetos.$projetoId.tsx` reporta 146 erros `prettier/prettier — Delete ␍`, **um por linha do arquivo inteiro**, incluindo as 139 linhas que esta story não tocou. Causa verificada: `git config core.autocrlf` = `true`. O blob no HEAD tem **0 bytes CR** (LF puro), o worktree tem **146 bytes CR** — ou seja, a conversão vem do checkout do Git, não da edição. Git normaliza de volta para LF no commit (as próprias warnings de `git diff` confirmam: "LF will be replaced by CRLF the next time Git touches it"). Prova de que não há erro de regra real: `npx eslint --rule '{"prettier/prettier":"off"}'` sobre os dois arquivos tocados retorna **exit 0**. O arquivo de teste novo (`tests/ui/projeto-detalhe-nav-links.test.ts`, escrito com LF) passa no eslint **sem nenhuma flag**. Mesma caveat já registrada nas stories do ciclo DUC/MOD-QT-2 anteriores.
- **Não houve retry:** todos os gates passaram na primeira execução. Política de retry não foi acionada.

### Completion Notes List

**IDS Protocol (SEARCH → DECIDE → LOG)**

| Artefato | Search | Decisão | Justificativa |
|---|---|---|---|
| Link "Queda de tensão" | Grep/Read no próprio `deps-hero-links` — 2 `<Link>` + 3 `<a href>` já existentes | **ADAPT** | Reusado literalmente o padrão `<Link to/params/className>` dos 2 primeiros links do mesmo bloco; só `to` e o rótulo mudam. Zero código novo de infraestrutura |
| Teste de nav do hub | `ls tests/ui/` + confirmação de que não existe teste para `projetos.$projetoId.tsx` | **CREATE** (justificado) | Não há arquivo pré-existente a estender. Padrão de asserção de fonte **ADAPTADO** de `tests/ui/queda-tensao-fluxo-entrada-fechado.test.tsx` (mesmo `readFileSync` + `resolve(process.cwd(), ...)`) |

**Evidência por AC**

- **AC1** — `bloco.toContain("Queda de tensão")` + verificação de `className="deps-hero-link"` na tag de abertura correspondente. Teste `AC1 — expõe um link 'Queda de tensão' com a classe deps-hero-link`: PASS.
- **AC2** — teste localiza o `<Link>` que envolve o rótulo (via `lastIndexOf("<Link", indiceRotulo)`) e assere `to="/projetos/$projetoId/queda-tensao"` + `params={{ projetoId }}`. Prova de tipo complementar: `npx tsc --noEmit` exit 0 — o `to` do TanStack Router é type-checked contra a route tree gerada, então um literal inválido quebraria a compilação (mitiga R3).
- **AC3** — teste assere que os 6 rótulos aparecem no bloco em posições **estritamente crescentes** na ordem canônica, e que os 5 destinos pré-existentes continuam literalmente presentes (2 `to="..."` + 3 `href={\`...\`}`). Reforço independente: `git diff --stat` mostra **`+7` linhas e 0 remoções** no arquivo — nenhum dos 5 links foi editado, movido ou removido (mitiga R2).
- **AC4** — **N/A confirmado**. `tests/ui/__snapshots__/` contém apenas 5 snapshots (`correntes-rastreabilidade`, `edp-sp-isolacao`, `queda-tensao`, `unifilar-canvas`, `unifilar-workspace`); nenhum corresponde ao hub. A cláusula de contingência não foi acionada — nada regenerado.

**Riscos da story — situação final**

- R1 (instalar jsdom/Testing Library): **não ocorreu.** `package.json` intocado; nenhuma dependência adicionada; nenhum `vitest.config.*` criado ou alterado.
- R2 (migrar os 3 `<a href>` "de brinde"): **não ocorreu.** Os 3 `<a href>` permanecem exatamente como estavam; a dívida segue registrada e fora de escopo.
- R3 (literal de rota errado): **mitigado** por `tsc --noEmit` exit 0.
- R4 (divergência SSR × SPA): `npx vite build` exit 0. As route trees **não foram tocadas** — a rota já estava registrada em ambas.
- R5 (regressão de suíte): **não ocorreu.** 947 → **950** testes passando (os 3 novos), 133 arquivos, 0 falhas.

**Observação para o @qa (não-bloqueante):** o `<Link>` novo é o único do bloco a fazer navegação client-side entre "Dimensionamento de condutores" e "Planejador de circuitos", que continuam com full-page-reload via `<a href>`. Isso é a inconsistência pré-existente já documentada pelo @po (drift do commit `1e18cc9`) e deliberadamente fora de escopo — não é defeito desta entrega.

### File List

**Modificado**
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx` — +7 linhas: `<Link>` "Queda de tensão" inserido no bloco `deps-hero-links`, entre "Dimensionamento de condutores" e "Planejador de circuitos"

**Criado**
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/projeto-detalhe-nav-links.test.ts` — 3 testes de asserção de fonte (AC1, AC2, AC3)

**Documentação / processo (fora do submódulo)**
- `docs/stories/story-MOD-QT-2-05-nav-link-queda-tensao.md` — Tasks, DoD, Dev Agent Record, Change Log, Status
- `.aiox/handoffs/MOD-QT-2-05-dev-to-qa.yaml` — criado
- `.aiox/workflow-state/MOD-QT-2-05-state.yaml` — atualizado
- `.aiox/logs/MOD-QT-2-05-yolo.log` — linhas `[DEV]` acrescentadas

**Nenhum snapshot VRT criado, alterado ou regenerado.**

## QA Results

**Revisor:** Quinn (Test Architect) — `*qa-gate`, modo YOLO autônomo, 2026-07-29
**Gate:** **CONCERNS** — quality score **95/100**
**Arquivo de gate:** `docs/qa/gates/MOD-QT-2-05-gate.yaml`
**Transição:** `InReview → Done`

### Veredito em uma linha

Os 4 ACs estão atendidos e foram verificados por reexecução independente — **nenhum número do @dev foi aceito por alegação, e todos conferiram**. CONCERNS (não PASS) por uma única ressalva herdada do ciclo: `npx eslint .` sobre o projeto inteiro continua NÃO VERIFICADO por trava ambiental. Nenhuma correção exigida.

### Escopo deste gate

Gate **pontual**, proporcional ao tamanho XS da entrega. O ciclo MOD-QT-2 (-01 a -04) já está `Done` e fechado; as verificações de motor, catálogo de impedância, limites EDP-SP e contratos públicos **não foram reabertas** — esta story comprovadamente não toca nenhuma delas.

### As 7 verificações independentes

| # | Verificação | Resultado | O que o @qa observou (números reais) |
|---|---|---|---|
| 1 | Leitura do arquivo real | ✅ PASS | Bloco `deps-hero-links` nas linhas 81-112. Ordem final dos 6 confere com a AC3: Padrão de entrada (L82) → Correntes (IB) (L89) → Dimensionamento de condutores (L96, `<a>`) → **Queda de tensão (L99-105, `<Link>`)** → Planejador de circuitos (L106, `<a>`) → Unifilar (L109, `<a>`). Novo link com `to="/projetos/$projetoId/queda-tensao"`, `params={{ projetoId }}`, `className="deps-hero-link"` — idêntico em estrutura, indentação e ordem de props ao padrão dos 2 primeiros. Os 5 pré-existentes conferem com o "antes" documentado na story (§Evidência, linhas 20-26). |
| 2 | `git diff` reexecutado | ✅ PASS | `git diff --numstat` → **`7  0`**. Alegação do @dev **confirmada**. Hunk único `@@ -96,6 +96,13 @@`, apenas as 7 linhas do novo `<Link>`. **Zero remoções** ⇒ nenhum dos 5 links foi editado, movido ou removido. R2 não ocorreu. |
| 3 | Teste novo, isolado + leitura crítica | ✅ PASS | `npx vitest run tests/ui/projeto-detalhe-nav-links.test.ts` → **1/1 arquivo, 3/3 testes, exit 0, 897ms**. Leitura crítica: **não é** um teste de "arquivo existe" — extrai o bloco `deps-hero-links` e assere rótulo + `className` (AC1), `<Link>` com `to` **e** `params` via `lastIndexOf("<Link", …)` (AC2), e posições **estritamente crescentes** dos 6 rótulos + presença literal dos 5 destinos pré-existentes (AC3). Cobre texto, destino, tipo de elemento e ordem. Nenhum import de Testing Library/jsdom/happy-dom. |
| 4 | Caveat de lint reproduzido **e causa verificada** | ⚠️ PASS COM RESSALVA | `npx eslint` nos 2 arquivos → **exit 1, ✖ 146 problems**. Contagem do @dev **confirmada**. 146/146 são `prettier/prettier — Delete ␍`; nenhuma outra regra. Linhas reportadas: 146 distintas, de `1:34` a `146:2` — **uma por linha do arquivo inteiro (146 linhas), sendo 139 fora do intervalo 99-105 das linhas novas**. Com `--rule '{"prettier/prettier":"off"}'` → **exit 0**. **Verificação de causa (a prova que o @dev não apresentou):** rodei o mesmo eslint em `src/routes/index.tsx` — arquivo **limpo em `git status`, sem nenhuma relação com esta story** → **exit 1, 140/140 `prettier/prettier`**, 140 bytes CR na worktree. O mesmo modo de falha existe em arquivo que ninguém tocou. Contraprova: `__root.tsx` (também limpo) tem 0 CR e passa exit 0. `core.autocrlf=true`; blob no HEAD com **0 CR** vs. worktree com **146 CR**. **Conclusão: a alegação ambiental se sustenta — não é FAIL.** |
| 5 | Suíte completa | ✅ PASS | `npx vitest run` → **Test Files 133 passed (133) \| Tests 950 passed (950) \| 0 falhas \| exit 0 \| 199,36s**. Baseline do ciclo era 947/947 em 132 arquivos ⇒ **+3 testes, +1 arquivo**, exatamente os do teste novo. Nada desapareceu, nada passou a falhar. |
| 6 | `tsc --noEmit` e `vite build` | ✅ PASS | `npx tsc --noEmit` → **exit 0**, sem saída (prova de tipo da AC2: o `to` é type-checked contra a route tree — R3 mitigado). `npx vite build` → **exit 0, built in 8.22s** (R4 coberto). |
| 7 | Nada fora de escopo | ✅ PASS | A worktree do submódulo está suja com ~57 arquivos de outros épicos, então usei atribuição por mtime: `find src tests -newermt "2026-07-29 10:00"` → **exatamente 2 arquivos**, o de rota e o de teste. Nada mais. `src/domain/queda-tensao/`, `projetos.$projetoId_.queda-tensao.tsx`, `routeTree.gen.ts`, `routeTree.spa.ts` → **todos limpos**. Nenhum `vitest.config.*` existe. `package.json` aparece `M`, mas o diff é a adição de 2 scripts `docs:tutorial:*` (trabalho de tutoriais MOD-DC, alheio); `dependencies` **intocado** e zero ocorrências de `testing-library\|jsdom\|happy-dom` ⇒ **R1 não ocorreu**. |

### ACs

| AC | Status | Base da decisão |
|---|---|---|
| AC1 | **MET** | Leitura direta (L99-105) + teste AC1 executado pelo @qa |
| AC2 | **MET** | Literal verificado na fonte e no teste; **tipo** verificado por `tsc --noEmit` exit 0 |
| AC3 | **MET** | `+7/-0` no diff + ordem conferida na fonte + teste de posições crescentes |
| AC4 | **N/A confirmado** | `tests/ui/__snapshots__/` tem 5 snapshots, **nenhum do hub**. Verificado pelo @qa, não aceito por alegação. Cláusula de contingência não acionada; nada regenerado |

### 7 checks de qualidade (Fase 4)

| Check | Resultado |
|---|---|
| Code review | ✅ PASS — reuso literal do padrão `<Link>` do mesmo bloco (IDS: ADAPT); acessibilidade equivalente à dos vizinhos |
| Unit tests | ✅ PASS — 3 testes novos, asserções materiais, 0 testes removidos ou alterados |
| Acceptance criteria | ✅ PASS — 3/3 MET + 1 N/A confirmado |
| No regressions | ✅ PASS — 947 → 950, 0 falhas, diff sem remoções |
| Performance | ➖ N/A — 1 elemento JSX estático, sem query/efeito/cálculo |
| Security | ➖ N/A — navegação interna, sem input, sem dado sensível, sem rota de API |
| Documentation | ✅ PASS — **integridade de evidência restabelecida**: diferente do que ocorreu em MOD-QT-2-04 (DOC-001), nenhum gate foi declarado PASS sem estar. Os cinco números do Debug Log (+7/-0, 950/950, 133 arquivos, 146 erros de lint, 5 snapshots) conferiram na reexecução |

### Ressalvas aceitas (nenhuma bloqueia)

- **MNT-005 (low)** — `npx eslint .` completo NÃO VERIFICADO (trava ambiental, >20 min). Herdado de MNT-003 do gate -04. Ambos os arquivos desta story foram verificados individualmente; nenhum ficou sem cobertura de lint.
- **MNT-006 (low)** — worktree com line endings mistos sob `core.autocrlf=true` (`index.tsx` com 140 CR sem nenhuma modificação pendente; `__root.tsx` com 0 CR). Obriga cada gate do ciclo a re-provar que a falha de lint é cosmética. **Recomendação ao @devops:** `.gitattributes` com `* text=auto eol=lf` e normalização em commit dedicado, fora de qualquer story.
- **DBT-005 (low)** — 3 links do bloco seguem em `<a href>` (full-page reload) e 3 em `<Link>`; o novo fica entre dois `<a href>`. Drift pré-existente do commit `1e18cc9`, vetado pela AC3. **Backlog de @po**: story de migração dedicada.
- **OPS-001 (low)** — BLK-QT-TIMEOUT-FLAKY-01 não reproduzido; 4ª execução completa consecutiva sem repro. Blocker mantido aberto, severidade BAIXA.

### Decisões do @dev que o @qa confirma

- **Não normalizar o CRLF nesta story: CORRETO.** Normalizar reescreveria as 139 linhas fora de escopo e violaria frontalmente a AC3. A decisão conservadora é a certa.
- **`.ts` em vez de `.tsx` no arquivo de teste: CORRETO.** O teste não contém JSX.
- **Não migrar os 3 `<a href>` vizinhos: CORRETO.** Dívida pré-existente, explicitamente fora de escopo.

### Correções exigidas

**Nenhuma.** Story liberada para `@devops *push` via `.aiox/handoffs/MOD-QT-2-05-qa-to-devops.yaml`.
