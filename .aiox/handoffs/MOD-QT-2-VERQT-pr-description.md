# feat(mod-qt): catálogo fechado de impedância, resolvedor de perfil e limite EDP-SP v09

**Stories:** `MOD-QT-2-03`, `MOD-QT-2-04` — ambas `Done`, QA gate **CONCERNS (92)**
**Pipeline:** `MOD-QT-2-RESOLUCAO-VERQT`
**Fonte normativa:** `docs/research/{2026-07-28}-resolucao-ver-qt.md` (parecer, revisão 2) §6, correções C-01 a C-08
**Repositório de código:** submódulo `sistema-de-instala-es-el-tricas-sie-main` (branch `feature/nbr5410-conformidade-closeout`)

> **Status:** PR **preparado**, não criado. `gh pr create` aguarda autorização explícita do usuário.

---

## Sumário

Fecha a resolução das lacunas VER-QT do módulo de queda de tensão (MOD-QT-2), substituindo
tabelas de impedância genéricas e marcações `[VERIFICAR]` por um catálogo fechado, rastreável e
fail-closed, e introduzindo o limite normativo do padrão EDP-SP v09.

| VER-QT | Situação após esta entrega |
|---|---|
| VER-QT-02 | RESOLVIDO (catálogo fechado) |
| VER-QT-03 | RESOLVIDO (catálogo fechado) |
| VER-QT-04 | RESOLVIDO (parecer §3.3) |
| VER-QT-06 | RESOLVIDO (alturas de tomada são parâmetro de projeto, não cota normativa) |
| VER-QT-07 | **PARCIAL** — resolvido apenas para `EDP_SP_PTDTPDN00068_V09_AEREA_BT` |

---

## O que foi entregue

### 1. Catálogo Prysmian fechado (C-01) — `MOD-QT-2-03`

- 1.563 registros gerados por **script versionado** (`scripts/gerar-catalogo-impedancia-prysmian.mjs`)
  a partir do artefato de extração, com verificação **SHA-256** da fonte.
- **Zero** valores alterados, arredondados, interpolados ou extrapolados. 24 nulos da fonte
  preservados como nulos; **0** zeros de `Rca`/`XL`.
- Chave `(família, seção, topologia)` unívoca em 1.563/1.563; 9 tabelas, 12 topologias, 9 grupos,
  62 `nota_restricao`.
- `fonte_id` é **coluna discriminadora**, nunca constante embutida (decisão PO-03) — o catálogo é
  agnóstico de fabricante e admite uma segunda fonte no futuro sem refatoração.

### 2. Resolvedor de perfil fail-closed (C-02) — `MOD-QT-2-03`

- Integrado ao motor de queda de tensão. Perfil não resolvido ⇒ a validação é **encerrada antes
  de montar `RetornoMODQT`** (HTTP 422 / `PENDENTE`).
- Não existe resultado degradado, não existe cabo presumido, não existe aprovação por omissão.
  A rejeição chega ao MOD-DC como **ausência** de `retorno_qt`.

### 3. Oracle independente do CA-QT-19 (C-07) — `MOD-QT-2-03`

- Suíte de não-regressão regenerada com oracle que lê o JSON bruto por `readFileSync` e aplica a
  fórmula do parecer §3.3 — **sem importar o motor**. 504 vetores (8×9×7) coincidentes.
- A razão motor/mock foi convertida em diagnóstico, deixando de ser critério de correção.

### 4. Perfil de limite EDP-SP v09 (C-05) — `MOD-QT-2-04`

- Novo perfil `EDP_SP_PTDTPDN00068_V09_AEREA_BT` com limite total de **5%**.
- Aplicado **somente** quando o projetista declara o escopo de atendimento. Fora dele a alínea
  6.2.7.1 permanece `[VERIFICAR]` e a marcação continua obrigatória — generalizar seria invenção
  (Constitution, Artigo IV).
- O perfil de atendimento **confirma** o limite; nunca o substitui no motor. Divergência gera
  alerta e mantém `[VERIFICAR]`, sem ajustar nada.

### 5. Fluxo de entrada fechado (C-03) — `MOD-QT-2-04`

- `SeletorPerfilCabo` integrado à rota de queda de tensão, com estado, seed a partir do
  `perfil_cabo` persistido e persistência do perfil resolvido.
- As opções são **derivadas do catálogo a cada consulta** — nenhuma tabela de combinações válidas
  foi replicada; a decisão final é delegada a `tentarResolverPerfilImpedancia()`.

### 6. Alturas de tomada (C-06) — `MOD-QT-2-04`

- Tratadas como parâmetro de projeto. **Nenhuma atribuição das cotas 0,30/1,10/2,00 m à NBR 5410.**

---

## Gates de qualidade

| Gate | Comando | Resultado |
|---|---|---|
| Tipagem | `npx tsc --noEmit` | ✅ PASS (exit 0) |
| Testes | `npx vitest run` | ✅ PASS — 132/132 arquivos, 947/947 testes, exit 0 |
| Build | `npx vite build` | ✅ PASS |
| Lint escopado | `npx eslint <arquivos das stories>` | ✅ PASS (exit 0, 24 arquivos) |
| Lint projeto inteiro | `npx eslint .` | ⚠️ **NÃO VERIFICADO** — trava ambiental pré-existente, **não presumido PASS** |

> `--reporter=basic` **não** deve ser usado neste projeto: no Vitest 4 ele mascara falha de
> startup com exit 0.

## Garantias de escopo (verificadas pelo @qa)

- **Contrato público intacto**, verificado **por símbolo** (a worktree está suja com trabalho
  alheio, então `git diff` de arquivo inteiro não é conclusivo): `RetornoMODQT`,
  `ValidarMODQTSchema`, `RetornoMODQTSchema` e `POST /api/v1/modulos/mod-qt/validar` inalterados.
- **MOD-DC intocado**: 0 ocorrências de `queda|perfil_cabo|impedanc|prysmian|retorno_qt|limite_total`
  no diff de `src/domain/dimensionamento-condutores/`.
- **Sem regressão**: CA-QT-19 e CA-QT-22 preservados (nenhuma suíte deletada, nenhum `skip`).

---

## Ressalvas de QA (CONCERNS em ambas — nenhuma bloqueante)

Ambas as stories receberam **CONCERNS** pela **mesma razão, ambiental**: `npx eslint .` sobre o
projeto inteiro não pôde ser executado (trava pré-existente, >25 min sem retorno) e **não foi
presumido PASS**. Todos os arquivos de produção das duas stories passaram por lint escopado com
exit 0. Nenhuma ressalva aponta defeito funcional.

| ID | Story | Sev. | Achado |
|---|---|---|---|
| MNT-003 | 2-04 | low | `npx eslint .` completo NÃO VERIFICADO — trava ambiental |
| TEST-001 | 2-03 | low | Guarda de `[VERIFICAR]` por substring literal no gate C-07 — mais estreita do que o teste declara |
| TEST-002 | 2-03 | low | Assert sobre a razão motor/mock dentro de bloco declarado "não é critério" |
| OPS-001 | ambas | low | `BLK-QT-TIMEOUT-FLAKY-01` — causa estrutural do timeout intermitente inalterada |
| MNT-002 | 2-04 | low | DT-04-01 / DT-04-02 — backlog de @po |

**Histórico de gate de `MOD-QT-2-04`:** rodada 1 FAIL (score 78) por **integridade de evidência** —
os 9 ACs já estavam corretos, mas o Debug Log declarava `eslint` escopado PASS enquanto a
reexecução independente encontrava 6 violações `prettier/prettier` ainda no disco. O @dev corrigiu
apenas a formatação e **retificou o registro preservando o rastro do erro**. Rodada 2: CONCERNS (92).

## Débito técnico registrado

- **`BLK-QT-TIMEOUT-FLAKY-01`** (baixa, **aberto**): timeout intermitente em
  `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts`. Não reproduzido em 3
  execuções completas consecutivas; a causa estrutural (1.563 × 13 asserts sem `testTimeout`
  próprio) permanece. Não bloqueia o merge.

---

## Riscos e itens fora de escopo

| ID | Item | Situação |
|---|---|---|
| `MOD-DC-PRD-13.6` | O PRD do MOD-DC §13.6 ainda assume limite total de **7%**; esta cadeia estabelece **5%** para o perfil EDP-SP v09 | **ABERTO** — story futura de @po/@architect. Risco **documental, não de código**: nenhum arquivo do MOD-DC foi alterado |
| `CONDUTO-FERROMAGNETICO` | Conduto metálico fechado ferromagnético | **RESOLVIDO** como **rejeição** explícita (indisponibilidade de método), nunca como degradação de cálculo |
| `SEGUNDA-FONTE-FABRICANTE` | Segunda fonte de fabricante além da Prysmian | **BACKLOG** (decisão PO-03) — o catálogo já é agnóstico de fabricante |

**Explicitamente NÃO tratado nesta entrega:** o alinhamento do PRD do MOD-DC (7% → 5%) e qualquer
alteração em `src/domain/dimensionamento-condutores/**`.

---

## Aviso ao revisor — worktree suja

A worktree do submódulo contém **trabalho alheio a esta cadeia, não commitado** (MOD-CC,
AUTO-OTI, proteção, dimensionamento-condutores, derivar-circuitos). O commit desta cadeia foi
montado **por path explícito** a partir das File Lists das duas stories. `git add -A` /
`git commit -a` **não** foram usados e não devem ser.

---

🤖 Preparado por @devops (Gage) — execução real pendente de autorização explícita do usuário
