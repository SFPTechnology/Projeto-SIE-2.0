# Story SIE-DS-05-decision — DecisionTemplate (comparação de opções)

**Workflow-fonte:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-06-07-DEPLOY-YOLO.md`
**Ratificações reutilizadas:** stories `SIE-DS-00`, `SIE-DS-05` (ParametersResultsTemplate)
**Status:** **Done**
**Created:** 2026-07-31
**Priority:** P2 (fecha o item canônico `SIE-DS-05`, adiado em `story-SIE-DS-05-parameters-results.md`)

---

## 📖 Descrição

**Como** avaliador do SIE Command Center que já validou Parameters + Results (`SIE-DS-05`),
**eu quero** ver o `DecisionTemplate` (comparação de opções com impacto downstream e confirmação),
**para que** o item canônico `SIE-DS-05` do backlog-semente seja concluído.

Escopo local-only (sem push/PR/deploy nesta story especificamente — a decisão de deploy é tratada separadamente, ao final de `SIE-DS-07`, conforme `WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-06-07-DEPLOY-YOLO.md` §6).

---

## ✅ Acceptance Criteria

- [ ] **AC1 — `DecisionPanel`:** `src/components/command-center/DecisionPanel.tsx` existe, implementa a composição do `DecisionTemplate` (`docs/component-catalog.md` §Templates: `ContextHeader → ContextSummary → OptionComparison → ImpactSummary → Confirmation`) para um cenário ilustrativo: escolha de método de instalação alternativo para o circuito C14 (já usado em `SIE-DS-04`/`SIE-DS-05`).
- [ ] **AC2 — `ContextSummary`:** resumo do contexto da decisão (circuito, situação atual, motivo de a decisão ser necessária).
- [ ] **AC3 — `OptionComparison`:** 2 opções ilustrativas comparáveis lado a lado (ex.: manter seção atual vs. aumentar seção), cada uma com suas consequências.
- [ ] **AC4 — `ImpactSummary`:** impacto downstream de cada opção (ex.: efeito na queda de tensão, no custo ilustrativo) — sem cálculo real, valores estáticos.
- [ ] **AC5 — `Confirmation`:** ação de confirmação ilustrativa (sem persistência real — mesmo padrão de "ação demonstrativa" já usado em `CommandPalette`/`ContextInspector`), com aviso textual de que é demonstrativa.
- [ ] **AC6 — Acessibilidade:** opções comparáveis navegáveis por teclado; nenhuma opção codificada só por cor (nomenclatura de estado com texto, mesmo padrão do catálogo); foco visível; confirmação não é um `<dialog>` bloqueante desnecessário (o catálogo restringe dialog a "decisão bloqueante" — este é um caso válido, mas deve permitir cancelar).
- [ ] **AC7 — Zero cálculo real:** nenhuma fórmula, validação normativa ou regra de domínio nova — mesma disciplina de todas as stories anteriores.
- [ ] **AC8 — Zero impacto no legado:** `AppShell.tsx`/rotas de produção com `git diff` vazio. Nenhuma operação remota.
- [ ] **AC9 — Testado localmente:** lint, typecheck, suíte completa, build SPA passam.

---

## 📝 Scope

### IN Scope
`DecisionPanel` com as 4 sub-seções do `DecisionTemplate`, integrado como nova seção na rota de preview.

### OUT Scope
- ❌ Persistência real de decisão;
- ❌ Cálculo real de impacto;
- ❌ Qualquer alteração em `AppShell.tsx`/rotas de produção;
- ❌ Qualquer operação remota.

---

## 🗂️ File List (planejado)

**Criados:** `DecisionPanel.tsx`/`.css`/`.test.tsx`, dados ilustrativos (`decision-data.ts` ou expansão de `parameters-results-data.ts`).
**Modificados:** `sie-command-center-preview.tsx`, `-sie-command-center-preview.test.tsx`.
**Intocado (AC8):** `AppShell.tsx`, rotas de produção.

---

## 🤖 CodeRabbit Integration

CodeRabbit local indisponível (7ª ocorrência esperada nesta sessão — ver nota de risco em `WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-06-07-DEPLOY-YOLO.md` §8). Compensado por lint/typecheck/test/build reais + revisão manual de `@qa`.

---

## 📌 Tarefas de Desenvolvimento

### Task 1: Dados ilustrativos (AC1-AC4)
- [ ] Contexto, 2 opções, impactos — dados estáticos tipados

### Task 2: DecisionPanel — ContextSummary + OptionComparison (AC2, AC3, AC6)
- [ ] Resumo + comparação lado a lado, navegável por teclado

### Task 3: DecisionPanel — ImpactSummary + Confirmation (AC4, AC5)
- [ ] Impactos por opção + ação de confirmação demonstrativa, cancelável

### Task 4: Integração (AC1)
- [ ] Nova seção na rota, abaixo de `ResultSummary`

### Task 5: Validações finais (AC7, AC8, AC9)
- [ ] `git diff`, lint, typecheck, suíte completa, build SPA

---

## 📊 Dependências

- **Depende de:** `SIE-DS-05` (ParametersResultsTemplate — Done).
- **Fecha:** o item canônico `SIE-DS-05` do backlog-semente.

## ⚠️ Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Confirmar de forma ilustrativa pode parecer uma ação real | Baixo | AC5 exige aviso textual explícito de "ação demonstrativa" |

---

## 🏛️ Architecture Ratification (@architect)

**Ratificado por:** Aria (`@architect`) — 2026-07-31
**Veredito:** **PASS**

- **`OptionComparison`:** grupo de `<input type="radio">` nativo (não botões customizados) para seleção de opção — acessibilidade de teclado/leitor de tela vem de graça da plataforma, mesmo princípio já aplicado em `ParameterPanel` (`<details>` nativo) e no colapso CSS da nav lateral.
- **`Confirmation`:** **não** usa `<dialog>` — fica inline no próprio `DecisionPanel`, com botões "Cancelar" e "Confirmar (demonstrativo)". Motivo: `component-catalog.md` regra 3 diz que `ContextInspector` não substitui dialog de confirmação **destrutiva**; esta decisão é demonstrativa e reversível (nada é persistido), não destrutiva — um modal adicional seria fricção desproporcional ao risco real.
- **Estado:** seleção de opção (`opcaoSelecionadaId`) e se a confirmação foi "efetivada" (`confirmado: boolean`) vivem localmente dentro de `DecisionPanel` — não precisam ser elevados, nenhum outro componente depende disso.
- **Dados:** novo arquivo `decision-data.ts` (não expandir `parameters-results-data.ts`, que já tem responsabilidade própria) — mesma convenção de arquivo de dados dedicado por feature.

---

## Dev Notes

### Fontes consultadas
- `outputs/design-system/sie-command-center/docs/component-catalog.md` (`DecisionTemplate`, `DecisionPanel`).
- Sem referência visual do protótipo (mesma situação de `SIE-DS-05` original) — grounded na especificação textual.
- Padrão de "ação demonstrativa" já estabelecido em `CommandPalette`/`ContextInspector`.

---

## Change Log

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-31 | 0.1.0 | Story criada em modo Draft a partir do backlog-semente SIE-DS-05 (DecisionTemplate, adiado anteriormente), escopo local-only | @sm/River |
| 2026-07-31 | 0.2.0 | Validada GO (9/10) — Status: Draft → ReadyForArchitecture. Escopo bem delimitado, AC5 evita confusão entre ação demonstrativa e real, sem operação remota nesta story. Handoff para `@architect`. | @po/Pax |
| 2026-07-31 | 0.3.0 | Ratificação arquitetural: **PASS** — Status: ReadyForArchitecture → Ready. OptionComparison via radio nativo; Confirmation inline (não dialog, decisão demonstrativa não destrutiva); estado local ao DecisionPanel; decision-data.ts dedicado. Handoff para `@dev`. | @architect/Aria |
| 2026-07-31 | 0.3.5 | Development started (yolo mode) — Status: Ready → InProgress | @dev/Dex |
| 2026-07-31 | 0.4.0 | Development complete — Status: InProgress → InReview. AC1-AC9 implementados. Lint/typecheck limpos, 1047/1047 testes, build SPA verde. Item canônico SIE-DS-05 completo (ParametersResultsTemplate + DecisionTemplate). Pronta para `@qa`. | @dev/Dex |
| 2026-07-31 | 0.5.0 | QA Gate **CONCERNS** — Status: InReview → Done. AC1-AC9 verificados. CodeRabbit indisponível pela 7ª story consecutiva — QA recomenda resolver antes de SIE-DS-06/07. Gate file: `docs/qa/gates/SIE-DS-05-decision-decision-template.yml`. | @qa/Quinn |

---

## Dev Agent Record

### Agent Model Used
Claude Sonnet 5 (`claude-sonnet-5`) — modo YOLO (`*develop-yolo`)

### Debug Log References
- Nenhum bug de código encontrado — lint/typecheck/testes passaram após uma rodada de `--fix` (formatação apenas).
- Smoke test manual ad-hoc (não persistido como teste automatizado) teve 2 falsos negativos por falha da própria checagem PowerShell (encoding de em-dash em `-match`; regex sem escopo capturando o `<dialog>` da `CommandPalette`, renderizado depois na mesma página) — corrigidos ao escopar a checagem à própria `<section>` do `DecisionPanel`. Não afetou os testes automatizados (`renderToStaticMarkup`), que já validavam isso corretamente.

### Completion Notes List
- AC1–AC9 implementados: `DecisionPanel` com as 4 sub-seções do `DecisionTemplate` (ContextSummary, OptionComparison via radio nativo, ImpactSummary reativo à seleção, Confirmation inline sem dialog).
- Isso **fecha o item canônico `SIE-DS-05`** do backlog-semente (ParametersResultsTemplate + DecisionTemplate, ambos agora Done).
- Smoke test real (escopado corretamente) confirmou: título, radio buttons, impacto padrão, botão "Confirmar (demonstrativo)", ausência de `<dialog>` interno.
- 151 arquivos / 1047 testes, zero falha. AC8 confirmado via `git diff`.
- Nenhuma operação remota executada.

### File List (real)
**Criados:** `decision-data.ts`, `DecisionPanel.tsx`/`.css`/`.test.tsx`
**Modificados:** `sie-command-center-preview.tsx`, `-sie-command-center-preview.test.tsx`
**Confirmado intocado (AC8):** `AppShell.tsx`, rotas de produção.

## QA Results

### Review Date: 2026-07-31

### Reviewed By: Quinn (Test Architect)

### CodeRabbit Full Self-Healing Loop (Step 0)

**Não executado** — 7ª story consecutiva. Compensado com lint/typecheck/1047 testes/build SPA/smoke test escopado corretamente/varredura de segurança manual.

### Verificação Independente

Smoke test re-executado com escopo corrigido (seção do `DecisionPanel` isolada) confirma zero dialog interno e todo o conteúdo esperado. AC8 via `git diff`. Regressão 151/1047, zero falha.

### Requirements Traceability

Todos os 9 ACs — PASS.

### Improvements Checklist

- [ ] **Should-Fix (recorrente, 7ª ocorrência, crítico):** CodeRabbit quebrado — este é o limite recomendado antes de `SIE-DS-06`/`SIE-DS-07`, que envolvem código real do Unifilar e um gate de qualidade formal, respectivamente. Recomendo fortemente resolver antes de prosseguir.

### Gate Status

Gate: **CONCERNS** → `docs/qa/gates/SIE-DS-05-decision-decision-template.yml`

### Recommended Status

**✓ Ready for Done.** Item canônico `SIE-DS-05` completo.
(Story owner — `@po` — decide o status final.)
