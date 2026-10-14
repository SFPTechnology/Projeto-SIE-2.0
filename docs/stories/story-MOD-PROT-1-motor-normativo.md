---
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools: [unit_test, contract_validation, api_review]
---

# Story MOD-PROT-1: Motor Normativo de Seleção de Disjuntor

## Status

**Done**

## Story

**As a** engenheiro eletricista,
**I want** que o sistema calcule In, curva de disparo e verifique o poder de interrupção do disjuntor a partir de IB, tipo de instalação/carga e Icc já disponível no circuito,
**so that** a seleção de proteção tenha fundamentação normativa rastreável em vez de uma série fixa com fator genérico.

## Acceptance Criteria

1. Dado IB e tipo de instalação, o motor retorna In com `origem_in: "MOD-PROT"`, seguindo a tabela normativa genérica (fonte declarada em `norma_dispositivo`).
2. Dado o tipo de carga/instalação (`circuito.tipo`: `ILU`/`TUG`/`TUE`), o motor seleciona curva de disparo (B/C/D) com fallback declarado e rastreável quando a informação não estiver disponível, publicado no mesmo campo `norma_dispositivo`.
3. Dado `retorno_cc.icc_presumida_a` já disponível no circuito (campo opcional recebido como parâmetro, não buscado pelo motor), o motor verifica `capacidade_interrupcao` (Icu/Ics) do disjuntor selecionado e marca reprovação quando insuficiente.
4. Quando `retorno_cc` está ausente/nulo (circuito em `AGUARDANDO-CC`), o resultado retorna pendência explícita `PENDENTE-ICC` em `pendencias`, sem bloquear a resolução de `in_a`/`i2_a`.
5. Quando IB está fora da faixa suportada pela tabela normativa genérica, o motor retorna `in_a: null` e pendência `PROTECAO-SUGESTAO-INDISPONIVEL` (mesmo código já usado por `sugerirProtecaoCircuito`), permitindo que o chamador caia para a heurística de fallback (Story MOD-PROT-3).
6. Nenhuma mudança de assinatura pública em `motor-protecao.ts` — o novo motor vive em módulo próprio (`src/domain/dimensionamento-disjuntores/`), sem alterar o comportamento da heurística existente.

## 🤖 CodeRabbit Integration

**Story Type Analysis**
**Primary Type**: Architecture (novo motor de domínio, introduz contrato `ResultadoProtecaoCircuito` reservado por ADR anterior)
**Secondary Type(s)**: N/A
**Complexity**: Medium — lógica normativa nova, mas isolada (zero I/O, zero mudança em código existente)

**Specialized Agent Assignment**
**Primary Agents**:
- @dev (implementação, pré-commit)
- @architect (validação de aderência ao contrato do ADR)

**Supporting Agents**:
- Nenhum adicional necessário nesta story

**Quality Gate Tasks**
- [ ] Pre-Commit (@dev): `coderabbit --prompt-only -t uncommitted` antes de marcar a story completa
- [ ] Pre-PR (@github-devops): `coderabbit --prompt-only --base main` antes de criar o PR

**Self-Healing Configuration**
**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

**Predicted Behavior**:
- CRITICAL issues: auto_fix (até 2 iterações)
- HIGH issues: document_only (registrado em Dev Notes)

**CodeRabbit Focus Areas**
**Primary Focus**:
- Pureza do domínio (zero I/O, zero dependência externa em `src/domain/`)
- Aderência estrita ao contrato de campos (`in_a`, `i2_a`, `origem_in`, `norma_dispositivo`, `capacidade_interrupcao`, `tempo_atuacao_s`, `pendencias`) — nenhum campo extra

**Secondary Focus**:
- Cobertura de teste para os casos de borda (IB fora de faixa, `retorno_cc` ausente, Icc insuficiente)

## Tasks / Subtasks

- [x] Criar `src/domain/dimensionamento-disjuntores/contratos.ts` com a interface `ResultadoProtecaoCircuito` e tipos auxiliares (`FonteCatalogoProtecao`) (AC: 1, 2, 3)
  - [x] `ResultadoProtecaoCircuito`: `in_a`, `i2_a`, `origem_in: "MOD-PROT" | null`, `norma_dispositivo`, `capacidade_interrupcao`, `tempo_atuacao_s`, `pendencias`
  - [x] `FonteCatalogoProtecao = "GENERICA"` nesta story (WEG/Siemens/ABB/Schneider ficam fora de escopo — fast-follow do PRD)
- [x] Criar `src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.ts` (AC: 1, 2, 3, 4, 5)
  - [x] Implementar `selecionarProtecaoCircuito(input)` reaproveitando a série normativa já usada em `SERIE_PROTECAO_IN_A` (`motor-protecao.ts`) como tabela genérica MVP (FR2 do PRD — tabela normativa, não amarrada a fabricante)
  - [x] Selecionar curva de disparo (B/C/D) a partir de `tipo_carga` (`ILU`/`TUG`/`TUE`), com fallback declarado se ausente
  - [x] Publicar decisão de In+curva em `norma_dispositivo` (string legível, ex.: `"Tabela normativa generica - curva C"`)
  - [x] Verificar `capacidade_interrupcao` contra `input.retorno_cc?.icc_presumida_a` quando presente; pendência `PENDENTE-ICC` quando ausente
  - [x] Calcular `tempo_atuacao_s` a partir da curva selecionada
  - [x] Retornar `in_a: null` + pendência `PROTECAO-SUGESTAO-INDISPONIVEL` quando IB exceder a faixa da tabela
- [x] Testes unitários em `src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.test.ts` (AC: 1–6)
  - [x] Caso feliz: IB dentro da faixa, `retorno_cc` presente e Icc suficiente → `origem_in: "MOD-PROT"`, sem pendências
  - [x] Icc insuficiente → reprovação declarada via pendência `CAPACIDADE-INTERRUPCAO-INSUFICIENTE` (não um campo `reprovado` separado — o contrato D3 do ADR não define esse campo; manter reprovação como pendência preserva o contrato exato sem inventar campo novo)
  - [x] `retorno_cc` ausente → pendência `PENDENTE-ICC`, `in_a`/`i2_a` ainda resolvidos
  - [x] IB fora de faixa → `in_a: null`, pendência `PROTECAO-SUGESTAO-INDISPONIVEL`
  - [x] Curva de disparo: um caso por tipo de carga (`ILU`, `TUG`, `TUE`) + caso de fallback sem tipo informado
- [x] Verificar que `motor-protecao.ts` (heurística existente) permanece intocado — rodado `npx vitest run` completo, `motor-protecao.test.ts` sem alterações de expectativa (AC: 6)

## Dev Notes

### Contexto e decisão arquitetural

Este motor é a peça central do módulo **MOD-PROT**, especificado em `docs/prd/PRD-MOD-PROT-dimensionamento-disjuntores.md` (FR1–FR6) e formalizado em `sistema-de-instala-es-el-tricas-sie-main/docs/architecture/mod-prot-contrato-integracao.md` (Decisões D2–D4). [Source: architecture/mod-prot-contrato-integracao.md#2-decisões-fixadas]

**Contrato de resultado (D3 do ADR) — copiar exatamente, não inventar campos adicionais:**
```ts
export interface ResultadoProtecaoCircuito {
  readonly in_a: number | null;
  readonly i2_a: number | null;
  readonly origem_in: "MOD-PROT" | null;
  readonly norma_dispositivo: string | null;
  readonly capacidade_interrupcao: number | null; // Icu/Ics em kA
  readonly tempo_atuacao_s: number | null;
  readonly pendencias: ReadonlyArray<string>;
}
```
[Source: architecture/mod-prot-contrato-integracao.md#d3]

**Assinatura da função (D4 do ADR) — motor puro, sem I/O, recebe `retorno_cc` como parâmetro:**
```ts
export function selecionarProtecaoCircuito(input: {
  readonly ib_a: number;
  readonly tipo_instalacao: TipoInstalacao;
  readonly tipo_carga?: TipoCircuitoDimensionamento;
  readonly retorno_cc?: RetornoMODCC | null;
  readonly fonte_catalogo?: FonteCatalogoProtecao; // default "GENERICA" nesta story
}): ResultadoProtecaoCircuito
```
[Source: architecture/mod-prot-contrato-integracao.md#d4]

`origem_in: "MOD-PROT"` já é um literal válido do type `OrigemIn` em `src/domain/dimensionamento-condutores/contratos.ts:12` (`"INFORMADO" | "SUGESTAO" | "MOD-PROT"`) — **não é necessário alterar esse tipo**, apenas usá-lo. [Source: PRD-MOD-PROT-dimensionamento-disjuntores.md#0.1]

### Heurística existente (referência de reuso, NÃO modificar)

`src/domain/dimensionamento-condutores/motores/motor-protecao.ts` já implementa uma série normativa fixa (`SERIE_PROTECAO_IN_A = [6, 10, 16, 20, 25, 32, 40, 50, 63]`) e uma função `sugerirProtecaoCircuito({ ib_a, tipo_instalacao })` que escolhe o primeiro In da série ≥ IB (com piso de 10A para instalação residencial) e calcula `i2_a = in_a * 1.45`. Essa função **continua existindo sem alteração** — é o fallback tratado na Story MOD-PROT-3. Reaproveite a mesma série `SERIE_PROTECAO_IN_A` como base da "tabela normativa genérica" do novo motor (FR2 do PRD não exige uma tabela diferente para o MVP, apenas que a fonte seja declarada em `norma_dispositivo`).

### Icc — de onde vem, e por que este motor não busca sozinho

`CircuitoParaDimensionamento.retorno_cc?: RetornoMODCC | null` (`contratos.ts:74`) é o campo que carrega `icc_presumida_a` quando o critério C3 (curto-circuito, módulo `MOD-CC`) já foi resolvido para o circuito. **Este motor não chama nenhum endpoint** — quem orquestra (Story MOD-PROT-3, em `overrides.ts`) já tem acesso a `circuito.retorno_cc` e repassa como parâmetro. `RetornoMODCC` tem os campos `icc_presumida_a`, `tempo_atuacao_s`, `integral_joule_dispositivo`, `aprovado`, `fonte` (ver `src/routes/api/v1/modulos.mod-cc.validar.ts`).

**Atenção:** as rotas que populariam `retorno_cc` em produção (`retorno-cc`, planejadas em `mod-dc-rotas-retorno-downstream.md`) ainda não foram implementadas no repositório nesta data — na prática, `retorno_cc` estará quase sempre ausente até esse outro slice ser entregue. O motor deve tratar isso graciosamente (AC4), não como erro.

### Nomenclatura — cuidado

**Nunca usar o código `MOD-CC`** para nada relacionado a esta story — ele já está em uso duplo e ativo no projeto (rota de UI Command Center **e** módulo de API Curto-Circuito). Ver `docs/prd/PRD-MOD-PROT-dimensionamento-disjuntores.md`, Seção 1.1, para o histórico completo. Esta story apenas **lê** o tipo `RetornoMODCC`, não cria nada com esse código.

### Testing

- Framework: Vitest, mesmo padrão de `motor-sobrecarga.test.ts` e `motor-protecao.test.ts` (testes puros, sem mocks de infraestrutura — domínio não tem I/O).
- Localização: `src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.test.ts` (mesma pasta do motor, convenção do projeto).
- Não é necessário teste de integração/API nesta story — API só é criada na Story MOD-PROT-4.
- Rodar `npx vitest run` completo ao final para confirmar zero regressão em `motor-sobrecarga.test.ts` e `motor-protecao.test.ts` (nenhum deles deveria ser tocado por esta story).

### Project Structure Notes

Nova pasta `src/domain/dimensionamento-disjuntores/` espelha `src/domain/dimensionamento-condutores/` (mesmo padrão de camadas do CLAUDE.md do submódulo: `domain/` sem dependências externas). `dimensionamento-disjuntores/` pode importar tipos de `dimensionamento-condutores/contratos.ts` (ex.: `TipoInstalacao`, `RetornoMODCC`, `TipoCircuitoDimensionamento`); a direção inversa não é permitida (evita ciclo — ver ADR D2).

## Change Log

| Date | Version | Description | Author |
|------|---------|--------------|--------|
| 2026-08-05 | 1.0 | Story criada a partir do PRD-MOD-PROT e do ADR `mod-prot-contrato-integracao.md` | River (@sm) |
| 2026-08-05 | 1.1 | Validated GO (9/10) — Status: Draft → Ready | Pax (@po) |
| 2026-08-05 | 1.2 | Implementado e testado (13/13 testes do domínio + typecheck + lint limpos) — Status: Ready → Ready for Review | Dex (@dev) |
| 2026-08-08 | 1.3 | QA Gate CONCERNS (MNT-001: artefato revisado divergia do commitado) | Quinn (@qa) |
| 2026-08-08 | 1.4 | MNT-001 fechado: adaptacao VeredictoMODCC commitada em `2ecd1ca`; tsc exit 0, 17/17 testes do modulo | Dex (@dev) |
| 2026-08-08 | 1.5 | Status: Ready for Review -> InReview (normalizacao de ciclo de vida) | Dex (@dev) |

## Dev Agent Record

### Agent Model Used

Claude Sonnet 5 (claude-sonnet-5), modo YOLO (autônomo)

### Debug Log References

Nenhum log de debug foi necessário — implementação direta sem impasses. `npx vitest run` completo (1148/1159 passando; 3 arquivos falhando são pré-existentes e não relacionados, confirmado rodando-os isolados: `tests/ui/unifilar-canvas.vrt.test.tsx` e `tests/ui/unifilar-workspace.vrt.test.tsx` falham por instabilidade do `useId()` do React mesmo sem nenhum código do MOD-PROT envolvido; `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts` estoura timeout de 5000ms por lentidão do ambiente, não por lógica).

### Completion Notes List

- Contrato `ResultadoProtecaoCircuito` implementado exatamente como especificado no ADR (D3), sem campos extras.
- Reprovação por capacidade de interrupção insuficiente representada como pendência (`CAPACIDADE-INTERRUPCAO-INSUFICIENTE`), não como campo booleano `reprovado` — o contrato do ADR não define esse campo; manter fidelidade ao contrato teve prioridade sobre replicar o padrão de `ResultadoC2`.
- Valores de capacidade de interrupção (6 kA residencial/comercial, 10 kA industrial) e tempo de atuação (0,1s genérico) são placeholders conservadores documentados no código como tais — não vêm de catálogo real de fabricante (isso é fast-follow, fora de escopo, FR2 do PRD).
- `motor-protecao.ts` (heurística) não foi tocado — confirmado por diff e por suíte de testes sem alteração de expectativa.

### File List

**Criados:**
- `src/domain/dimensionamento-disjuntores/contratos.ts`
- `src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.ts`
- `src/domain/dimensionamento-disjuntores/motores/motor-selecao-protecao.test.ts`

## QA Results

### Review Date: 2026-08-08

### Reviewed By: Quinn (Test Architect)

**Traceability:** 6/6 ACs atendidas. AC6 (não-regressão) confirmada por diff vazio de `motores/motor-protecao.ts` entre `cf8490d` (pré-MOD-PROT) e `HEAD`.

**Evidência executada:**
- `npx tsc --noEmit` → exit 0
- `npx vitest run` (módulo) → 17/17 passando
- `npx vitest run` (suíte) → 1186/1187; a única falha é timeout de 5s em teste MOD-QT não relacionado, que passa com `--testTimeout=60000`
- `npx eslint` (arquivos MOD-PROT) → exit 0

**Ressalva (MNT-001, medium):** `motor-selecao-protecao.ts` tem alteração **não commitada** vinda da frente T2-SEM-MOTOR (`RetornoMODCC` → `VeredictoMODCC`, tratamento de `"SEM-MOTOR"`). O artefato revisado é o worktree; o commit `9f1b9e8` contém a versão anterior. Não publicar `9f1b9e8` isolado sem essa adaptação.

### Gate Status

Gate: CONCERNS → docs/qa/gates/MOD-PROT-1-motor-normativo.yml

### Re-Review Date: 2026-08-08

**MNT-001 RESOLVIDO.** Adaptacao ao `VeredictoMODCC` commitada em `2ecd1ca` com pathspec explicito. Worktree limpo em `src/domain/dimensionamento-disjuntores/`; `tsc --noEmit` exit 0; 17/17 testes do modulo. Baseline do worktree comparado antes/depois: apenas os 3 arquivos MOD-PROT sairam, zero mudanca colateral nas outras frentes.

### Gate Status (atualizado)

Gate: PASS -> docs/qa/gates/MOD-PROT-1-motor-normativo.yml
