# Story SIE-DS-04 — List + Inspector (seleção de circuito)

**Workflow-fonte:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS04-LOCAL-YOLO.md`
**Ratificações reutilizadas:** stories `SIE-DS-00`, `SIE-DS-LOCAL-01`, `SIE-DS-02`, `SIE-DS-03`
**Status:** **Done**
**Created:** 2026-07-31
**Priority:** P1 (item canônico SIE-DS-04 do backlog-semente)

---

## 📖 Descrição

**Como** avaliador do SIE Command Center que já validou o Overview completo (`SIE-DS-03`),
**eu quero** selecionar um circuito na tabela e ver seus detalhes num painel de inspeção,
**para que** a avaliação de UX cubra o padrão List + Inspector, central ao conceito do design system.

Escopo local-only, sem push/PR/deploy, mesmo formato das stories anteriores.

---

## ✅ Acceptance Criteria

- [ ] **AC1 — Seleção real na tabela:** as linhas de `EngineeringPanel` tornam-se selecionáveis por clique **e** teclado (`Enter`/`Espaço` com a linha focada, `tabIndex={0}`), replicando o comportamento de `prototype/app.js` linhas 213-221. O estado de seleção é elevado ao componente pai (rota), não interno a `EngineeringPanel`.
- [ ] **AC2 — `ContextInspector`:** `src/components/command-center/ContextInspector.tsx` existe, exibe: cabeçalho com nome do circuito selecionado e botão de fechar; badge de estado; lista de propriedades (aplicação, fases, corrente, condutor, comprimento) via `<dl>`; seção de rastreabilidade (lista ilustrativa de 3 itens, replicando linhas 437-465 do protótipo); 2 ações ilustrativas.
- [ ] **AC3 — Sincronização:** selecionar uma linha na tabela atualiza o `ContextInspector` com os dados do circuito correspondente; nenhuma seleção → Inspector exibe estado vazio (mensagem, não painel em branco).
- [ ] **AC4 — Zero duplicação de regra de domínio:** todos os dados exibidos no Inspector vêm do mesmo array `circuitosIlustrativos` já existente (`overview-data.ts`, expandido com os campos que faltam: fases, comprimento) — nenhuma fórmula, cálculo ou validação normativa é criada na UI.
- [ ] **AC5 — Acessibilidade:** linha selecionada com `aria-selected="true"`; Inspector com `aria-labelledby`; botão de fechar com `aria-label`; foco visível em todos os elementos novos; ordem de tabulação lógica (tabela → inspector quando aberto).
- [ ] **AC6 — Zero impacto no legado:** `AppShell.tsx` e rotas de produção com `git diff` vazio. Nenhuma operação remota.
- [ ] **AC7 — Testado localmente:** lint, typecheck, suíte completa, build SPA passam.

---

## 📝 Scope

### IN Scope
Seleção real na tabela (clique + teclado), `ContextInspector` sincronizado, estado elevado à rota.

### OUT Scope
- ❌ Seleção via clique no diagrama SVG — apenas a tabela seleciona (fiel ao protótipo);
- ❌ Navegação real entre módulos, dados reais de projeto;
- ❌ Qualquer alteração em `AppShell.tsx` ou rotas de produção;
- ❌ Qualquer operação remota.

---

## 🗂️ File List (planejado)

**A serem criados:**
- `src/components/command-center/ContextInspector.tsx`, `.css`, `.test.tsx`

**A serem modificados:**
- `src/components/command-center/EngineeringPanel.tsx` (seleção controlada via props)
- `src/components/command-center/EngineeringPanel.test.tsx`
- `src/components/command-center/overview-data.ts` (campos `fases`/`comprimento` adicionados a `CircuitoIlustrativo`)
- `src/components/command-center/tokens/sie-cc-tokens.test.ts` (se novos tokens forem necessários)
- `src/routes/sie-command-center-preview.tsx` (estado de seleção elevado, monta `ContextInspector`)
- `src/routes/-sie-command-center-preview.test.tsx`

**Explicitamente não tocados (AC6):** `src/components/app/AppShell.tsx`, rotas de produção.

---

## 🤖 CodeRabbit Integration

CodeRabbit local segue indisponível (4ª ocorrência em `SIE-DS-03`, escalada). Compensado por lint/typecheck/test/build reais + revisão manual de `@qa`, mesmo padrão de todas as stories anteriores desta cadeia.

---

## 📌 Tarefas de Desenvolvimento

### Task 1: Expandir dados ilustrativos (AC4)
- [ ] Adicionar `fases` e `comprimento` a `CircuitoIlustrativo` em `overview-data.ts`

### Task 2: Tornar EngineeringPanel controlado (AC1)
- [ ] Props `circuitoSelecionadoId` + `aoSelecionarCircuito`
- [ ] Linhas com `tabIndex={0}`, `onClick`, `onKeyDown` (Enter/Espaço), `aria-selected`

### Task 3: Criar ContextInspector (AC2, AC5)
- [ ] Cabeçalho, badge, property list, rastreabilidade, ações
- [ ] Estado vazio quando `circuito` é `null`

### Task 4: Elevar estado na rota (AC3)
- [ ] `sie-command-center-preview.tsx` gerencia `circuitoSelecionadoId`, passa para `EngineeringPanel` e `ContextInspector`

### Task 5: Validações finais (AC6, AC7)
- [ ] `git diff`, lint, typecheck, suíte completa, build SPA

---

## 📊 Dependências

- **Depende de:** `SIE-DS-03` (EngineeringPanel/tabela — Done).
- **Bloqueia:** `SIE-DS-05` (Parameters + Results).

## ⚠️ Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Elevar estado de seleção pode acoplar demais `EngineeringPanel` à rota | Baixo | Interface de props mínima (id + callback), mesmo padrão já usado em `ModuleNavigation`/`EngineeringShell` |

---

## 🏛️ Architecture Ratification (@architect)

**Ratificado por:** Aria (`@architect`) — 2026-07-31
**Veredito:** **PASS**

- **Estado de seleção:** `circuitoSelecionadoId: string | null`, dono é `SieCommandCenterPreviewPage` (a rota) — mesmo padrão de "estado elevado ao nível que compõe as duas partes" já usado para paleta/densidade em `EngineeringShell`. `EngineeringPanel` recebe `circuitoSelecionadoId` + `aoSelecionarCircuito` como props controladas; não guarda seleção internamente.
- **Busca do circuito selecionado:** lookup simples (`circuitosIlustrativos.find(...)`) inline na rota — não precisa de função pura separada nem de memoização para 3 itens ilustrativos; não introduzir complexidade desproporcional ao dado.
- **Teclado na linha da tabela:** `<tr tabIndex={0} onKeyDown={...}>` tratando `Enter` e `" "` (Espaço), com `event.preventDefault()` no espaço para não rolar a página — replica `prototype/app.js` linhas 215-220 fielmente.
- **Estado vazio do Inspector:** mensagem textual simples ("Selecione um circuito na tabela para ver os detalhes"), não um painel vazio sem contexto — melhora a "detalhe progressivo" exigida pela spec.
- **AC4 (não duplicar regra de domínio):** confirmado — `fases`/`comprimento` são apenas mais 2 campos ilustrativos no mesmo array estático, não uma nova fonte de verdade nem cálculo.

---

## Dev Notes

### Fontes consultadas
- `outputs/design-system/sie-command-center/prototype/index.html` linhas 296-347, 396-470; `prototype/app.js` linhas 147-173, 213-221.
- Stories anteriores desta cadeia (convenções de CSS, dados separados, testes).

### Testing
Mesmo padrão — sem jsdom/testing-library; interações via lógica extraída quando necessário.

---

## Change Log

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-31 | 0.1.0 | Story criada em modo Draft a partir do backlog-semente SIE-DS-04, escopo local-only | @sm/River |
| 2026-07-31 | 0.2.0 | Validada GO (9/10) — Status: Draft → ReadyForArchitecture. Valor claro, rastreabilidade forte, AC4 explicitamente proíbe duplicação de regra de domínio (Constituição Art. IV respeitada), escopo IN/OUT nítido. Handoff para `@architect`. | @po/Pax |
| 2026-07-31 | 0.3.0 | Ratificação arquitetural: **PASS** — Status: ReadyForArchitecture → Ready. Estado elevado à rota; lookup simples sem função pura separada; teclado Enter/Espaço na linha; estado vazio textual do Inspector. Handoff para `@dev`. | @architect/Aria |
| 2026-07-31 | 0.3.5 | Development started (yolo mode) — Status: Ready → InProgress | @dev/Dex |
| 2026-07-31 | 0.4.0 | Development complete — Status: InProgress → InReview. AC1-AC7 implementados. Lint/typecheck limpos, 1031/1031 testes, build SPA verde. Smoke test HTTP confirmou estrutura inicial (Inspector vazio, linhas tabindex=0); interação real coberta pelos 12 testes unitários de EngineeringPanel/ContextInspector. AppShell.tsx intocado. Pronta para `@qa`. | @dev/Dex |
| 2026-07-31 | 0.5.0 | QA Gate **CONCERNS** — Status: InReview → Done. AC1-AC7 verificados. CodeRabbit indisponível pela 5ª story consecutiva. Gate file: `docs/qa/gates/SIE-DS-04-list-inspector.yml`. | @qa/Quinn |

---

## Dev Agent Record

### Agent Model Used
Claude Sonnet 5 (`claude-sonnet-5`) — modo YOLO (`*develop-yolo`)

### Debug Log References
- Nenhum bug de lógica encontrado — lint/typecheck/testes passaram após uma única rodada de `--fix` (formatação apenas), mesmo padrão de `SIE-DS-03`.
- `CircuitoIlustrativo` expandido com `fases`/`comprimento` usando os valores reais do protótipo (`prototype/app.js` `circuitContent`), não valores inventados.

### Completion Notes List
- AC1–AC7 implementados: seleção real na tabela (clique + teclado), `ContextInspector` sincronizado via estado elevado à rota, estado vazio tratado.
- **Smoke test real via dev server:** `http://localhost:5173/sie-command-center-preview` → HTTP 200; Inspector em estado vazio por padrão ("Selecione um circuito..."), linhas com `tabindex="0"`, workspace-grid presente. **Limitação honesta:** este smoke test é HTTP estático (sem execução de JS), então confirma o HTML inicial correto mas não simula o clique real — a interação clique→seleção→Inspector atualizado é coberta pelos testes unitários de `EngineeringPanel`/`ContextInspector` (12 testes), não por este smoke test.
- AC6 confirmado: `git diff` vazio em `AppShell.tsx`.
- Nenhuma operação remota executada.

### File List (real)

**Criados:** `ContextInspector.tsx`, `.css`, `.test.tsx`
**Modificados:** `EngineeringPanel.tsx`/`.css`/`.test.tsx` (seleção controlada), `overview-data.ts` (campos fases/comprimento), `sie-command-center-preview.tsx`/`.css` (estado elevado, workspace-grid), `-sie-command-center-preview.test.tsx`
**Confirmado intocado (AC6):** `AppShell.tsx`, rotas de produção.

## QA Results

### Review Date: 2026-07-31

### Reviewed By: Quinn (Test Architect)

### CodeRabbit Full Self-Healing Loop (Step 0)

**Não executado** — 5ª story consecutiva. Compensado com lint/typecheck/1031 testes/build SPA/smoke test/varredura de segurança manual (zero ocorrência de padrões de risco).

### Verificação Independente

- Smoke test HTTP confirmado (ver acima), com a limitação explicitamente documentada (sem execução de JS — interação real coberta pelos 12 testes unitários de seleção/sincronização, todos revisados e aprovados).
- AC6: `git diff` vazio, arquivos novos restritos ao escopo já estabelecido.
- Regressão: 148 arquivos / 1031 testes, zero falha; legado sem regressão.

### Requirements Traceability

Todos os 7 ACs — PASS (seleção real, Inspector sincronizado, zero duplicação de regra de domínio confirmada por inspeção do código — `ContextInspector` só lê campos de `overview-data.ts`, nenhum cálculo).

### Improvements Checklist

- [ ] **Should-Fix (recorrente, 5ª ocorrência):** CodeRabbit quebrado — urgência mantida no máximo para `@devops`.

### Gate Status

Gate: **CONCERNS** → `docs/qa/gates/SIE-DS-04-list-inspector.yml`

**Razão:** todos os 7 ACs PASS. CONCERNS exclusivamente pela indisponibilidade do CodeRabbit (5ª story consecutiva).

### Recommended Status

**✓ Ready for Done.**
(Story owner — `@po` — decide o status final.)
