# Decision Log — DC-3 Motor C1 (Capacidade de Corrente)

**Agente:** @dev (Dex) — YOLO mode
**Data:** 2026-07-12
**Branch:** feature/nbr5410-conformidade-closeout

---

## IDS — SEARCH / DECIDE / LOG

| Artefato | Decisão | Justificativa |
|----------|---------|---------------|
| `motor-capacidade-corrente.ts` | **ADAPT** | Motor C1 já existia no submódulo (landed com DC-4). AC-DC-02/03/14/19 já implementados. Faltava apenas AC-DC-24. Mudança < 30%, não quebra consumidores (`servico-dimensionamento-condutores.ts`). |
| `contratos.ts` (`ParametrosDimensionamento`) | **ADAPT** | Adicionados 2 campos **opcionais** (`grupo_nao_semelhante`, `circuitos_desprezaveis_ate_30pct`). Aditivo → sem breaking change; testes API/flow pré-existentes continuam passando. |
| `tests/domain/dimensionamento-condutores/motor-c1.test.ts` | **CREATE** | `mod-dc.test.ts` é integração (serviço completo). Cobertura focada de C1 com exemplos numéricos rastreáveis por AC não existia — capacidade nova legítima. |
| `motor-c1.ts` (sugerido pela story) | **REJEITADO (CREATE)** | Criaria duplicata do motor já existente. Viola IDS (REUSE > CREATE). Nomes de arquivo da story eram placeholders; caminhos reais do submódulo prevalecem. |

---

## [AUTO-DECISION] Escopo AC-DC-24 (grupo não semelhante)

- **Q:** Como modelar "grupo não semelhante → F=1/√n" num motor de circuito único?
- **Decisão:** Novo flag opt-in `grupo_nao_semelhante` no contrato. Quando `true`, o fator de agrupamento tabelado (Tab. 42-45) é substituído por `1/√(nEfetivo)`. Default `false` → comportamento pré-existente inalterado.
- **Razão:** NBR 5410 6.2.5.5. n=10 → 1/√10 = 0,31623 ≈ 0,316 (bate com o AC). Isolado e sem efeito colateral nos fluxos existentes.

## [AUTO-DECISION] Isenção ≤30% (subtarefa 4)

- **Q:** Subtarefa pede "exclusão ≤30%", mas não há AC numérico e o motor não tem correntes por circuito do grupo.
- **Decisão:** Campo opt-in `circuitos_desprezaveis_ate_30pct` (default 0) subtraído de `n` antes da consulta ao FCA, com alerta `FCA-CIRCUITOS-DESPREZADOS-30PCT`. Implementação mínima, testada, sem disparar automaticamente (evita invenção — Constitution Art. IV).
- **Razão:** Atende a subtarefa listada sem inferir correntes que o motor não possui; caller informa a contagem desprezável.

## [AUTO-DECISION] Rastreio do fator 0,86 (AC-DC-14)

- **Q:** "fator 0,86 rastreado" — onde?
- **Decisão:** Já exposto em `ResultadoC1.fatores.neutro` e propagado por `servico` para `ResultadoDimensionamento.fator_neutro_carregado`. Teste assere `fatores.neutro === 0.86` e `num_condutores_carregados === 4`.

---

## Exemplos numéricos validados (worked examples)

| AC | Cenário | Resultado esperado | Verificado |
|----|---------|--------------------|-----------|
| AC-DC-02 | 2F/220V, IB 34,65A, B1, 3 agrup. | n=2; FCA=0,7; IB_fict=49,5A; Iz_base=57; **seção 10 mm²** | ✅ |
| AC-DC-03 | 2F+N | n=3 (col.3); sem N → n=2 | ✅ |
| AC-DC-14 | 3F+N, TH3 15-33% | n=4; neutro=0,86; **seção 16 mm²** | ✅ |
| AC-DC-19 | Método D vs B1 @30°C PVC | D→FCT=0,89 (solo); B1→FCT=1,0 (ambiente) | ✅ |
| AC-DC-24 | grupo não semelhante, n=10 | FCA=1/√10 **≈0,316** (≠0,5 tabelado) | ✅ |
| ≤30% | 5 agrup., 2 desprezados | n_ef=3 → FCA=0,7 (≠0,6) | ✅ |

---

## Quality Gates

| Gate | Comando | Resultado |
|------|---------|-----------|
| Testes focados | `npx vitest run tests/domain/dimensionamento-condutores/motor-c1.test.ts` | 6/6 PASS |
| Suíte de domínio | `npx vitest run tests/domain/dimensionamento-condutores` | 31/31 PASS (sem regressões) |
| Testes API (contrato) | `npx vitest run tests/api/dimensionamento-condutores-*.test.ts` | 2/2 PASS |
| Typecheck | `npx tsc --noEmit` | limpo (exit 0) |
| Lint | `npx eslint` (arquivos alterados, pós `--fix`) | limpo (exit 0) |

**Self-healing:** 1 iteração (eslint/prettier `--fix`). Sem escalonamento.

---

## Handoff → @qa (Quinn)

- Story `story-DC-3-motor-c1.md` → **InReview**.
- Sem `git push` (delegado a @devops).
- Atenção QA: AC-DC-24 e isenção ≤30% são lógica **nova**; AC-DC-02/03/14/19 são reforço de teste sobre código pré-existente.
