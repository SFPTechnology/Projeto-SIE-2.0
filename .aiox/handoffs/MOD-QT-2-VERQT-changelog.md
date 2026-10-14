# Notas de Changelog — MOD-QT-2 (resolução VER-QT)

**Data:** 2026-07-29
**Pipeline:** `MOD-QT-2-RESOLUCAO-VERQT`
**Stories:** `MOD-QT-2-03`, `MOD-QT-2-04` (ambas `Done`, QA gate CONCERNS · score 92)
**Fonte normativa:** `docs/research/{2026-07-28}-resolucao-ver-qt.md` (parecer, revisão 2) §6 — C-01 a C-08
**Status:** notas **preparadas**. Nenhuma tag, release ou publicação executada.

---

## Added

- **Catálogo fechado de impedância Prysmian** (1.563 registros) gerado por script versionado
  `scripts/gerar-catalogo-impedancia-prysmian.mjs`, com verificação SHA-256 da fonte, zero valores
  alterados e nulos preservados. Substitui as tabelas genéricas no caminho de produção.
  *(C-01 · `MOD-QT-2-03` · VER-QT-02/VER-QT-03)*
- **Resolvedor de perfil de impedância fail-closed** (`resolver-perfil-impedancia.ts`), integrado ao
  motor de queda de tensão. *(C-02 · `MOD-QT-2-03`)*
- **Perfil de limite normativo `EDP_SP_PTDTPDN00068_V09_AEREA_BT`** (limite total 5%), aplicado
  apenas sob declaração explícita do escopo de atendimento. *(C-05 · `MOD-QT-2-04` · VER-QT-07 parcial)*
- **Fluxo de entrada fechado de seleção de cabo** (`SeletorPerfilCabo`), com opções derivadas do
  catálogo a cada consulta — sem tabela de combinações replicada. *(C-03 · `MOD-QT-2-04`)*
- **Suítes de verificação do catálogo**: completude, unicidade de chave, rastreabilidade, casos
  negativos e teste funcional; e `integracao-mod-dc-c5-fail-closed.test.ts`. *(C-08 · `MOD-QT-2-03`)*

## Changed

- **CA-QT-19 regenerado com oracle independente do mock**: lê o JSON bruto e aplica a fórmula do
  parecer §3.3 sem importar o motor (504 vetores). A razão motor/mock passou a ser diagnóstico, não
  critério de correção. *(C-07 · `MOD-QT-2-03`)*
- **Sem perfil de impedância resolvido, a validação MOD-QT é encerrada antes de montar
  `RetornoMODQT`** — resposta 422 / `PENDENTE`. O MOD-DC recebe **ausência** de `retorno_qt`, nunca
  um resultado degradado ou uma aprovação por omissão. *(`MOD-QT-2-03` AC6/AC16)*
- **Alturas de tomada** passam a ser documentadas como parâmetro de projeto, deixando de ser
  apresentadas como cota normativa da NBR 5410. *(C-06 · `MOD-QT-2-04` · VER-QT-06)*
- **Marcação VER-QT-04 retirada** sem criação de enum inexistente (a representação continua sendo
  `num_fases === 2`). *(C-04 · `MOD-QT-2-03`)*

## Fixed

- Correção de 6 violações `prettier/prettier` em `SeletorPerfilCabo.tsx` e `opcoes-perfil-cabo.ts`,
  identificadas pelo re-gate independente do @qa em `MOD-QT-2-04`.

## Unchanged (garantias verificadas)

- Contrato público **inalterado**, verificado por símbolo: `RetornoMODQT`, `ValidarMODQTSchema`,
  `RetornoMODQTSchema` e `POST /api/v1/modulos/mod-qt/validar`.
- **MOD-DC** (`src/domain/dimensionamento-condutores/**`) **não foi tocado**.
- CA-QT-19 e CA-QT-22 preservados — nenhuma suíte deletada, nenhum `skip` introduzido.

---

## Débito técnico conhecido

- **`BLK-QT-TIMEOUT-FLAKY-01`** — severidade **baixa**, status **ABERTO**, **não bloqueante**.
  Timeout intermitente em `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts`.
  Não reproduzido em 3 execuções completas consecutivas do @qa; a causa estrutural
  (1.563 × 13 asserts sem `testTimeout` próprio) permanece inalterada. Registrado para tratamento
  futuro, não corrigido nesta entrega.
- **`npx eslint .` sobre o projeto inteiro permanece NÃO VERIFICADO** (trava ambiental
  pré-existente, >25 min sem retorno, independente destas stories). Não presumido PASS — é a única
  razão do veredito CONCERNS nas duas stories. Todos os arquivos das stories passaram por lint
  escopado com exit 0.
- **TEST-001 / TEST-002** (baixas): guarda de `[VERIFICAR]` por substring literal no gate C-07 e
  assert sobre a razão motor/mock em bloco declarado "não é critério".
- **MNT-002 / DT-04-01 / DT-04-02** (baixas): metal, temperatura e seção do perfil de cabo não
  persistidos; vocabulários de material (`Cu`/`Al`) e metal (`CU`/`AL`) não cruzados. Backlog de @po.

## Pendências fora de escopo (para story futura)

- **`MOD-DC-PRD-13.6`** — O PRD do MOD-DC §13.6 ainda assume limite total de **7%**, enquanto esta
  cadeia estabelece **5%** para o perfil EDP-SP v09. **Risco documental, não de código**: nenhum
  arquivo do MOD-DC foi alterado. Requer story de @po/@architect para alinhamento; o critério C5 do
  MOD-DC é o ponto de impacto. **Não tratado aqui deliberadamente.**
- **`SEGUNDA-FONTE-FABRICANTE`** — segunda fonte de impedância além da Prysmian (decisão PO-03). O
  catálogo já é agnóstico de fabricante (`fonte_id` como coluna discriminadora), então a inclusão
  não exige refatoração.
- **Conduto metálico fechado ferromagnético** — permanece **fora do domínio calculável** (parecer
  §3.2), tratado como **rejeição** com indisponibilidade explícita de método. Já resolvido como
  decisão de projeto, não é pendência.

---

## Métricas do ciclo

| Métrica | Valor |
|---|---|
| Stories entregues | 2 (`MOD-QT-2-03` 21 pts, `MOD-QT-2-04` 8 pts) |
| Acceptance criteria | 25 (16 + 9), 100% com evidência automatizada |
| Testes na árvore | 947 passando em 132 arquivos |
| Registros do catálogo | 1.563 (0 divergências vs. artefato de extração) |
| Rodadas de gate | 3 (1 em `2-03`, 2 em `2-04`) |
| Correções de @po aplicadas na validação | 9 |
