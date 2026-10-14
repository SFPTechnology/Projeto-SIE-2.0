# Workflow SDC Headless YOLO — SIE Command Center: SIE-DS-03 (Overview, jornada e cabeçalho contextual, local-only)

**Versão:** 1.0.0
**Data:** 2026-07-31
**Status:** Ready for execution — escopo local-only, sem operações remotas
**Modo:** YOLO agente-a-agente (sessão manual real), zero prompts durante a execução de cada fase
**Escopo:** implementação real do item canônico `SIE-DS-03` do backlog-semente (cabeçalho contextual, visão geral com métricas, jornada técnica), consumida apenas via a rota de preview local já existente
**Ratificações reutilizadas:** stories `SIE-DS-00`, `SIE-DS-LOCAL-01`, `SIE-DS-02`
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
**Conformidade:** `.aiox-core/constitution.md`

> **Decisão do usuário (reafirmada 2026-07-31):** mesmo formato de `SIE-DS-02` — sem fase `@devops`. A cadeia termina em `@qa` → `local_done`.

## 1. Objetivo

Fechar o gap identificado em `docs/analysis/GAP-ANALISE-SIE-DS-02-vs-PROTOTIPO.md`: implementar o cabeçalho contextual (dentro do `<main>`) e o conteúdo real de Overview (métricas, jornada técnica, painel de engenharia com tabela+diagrama), substituindo o placeholder ilustrativo de `SIE-DS-LOCAL-01` dentro do shell já completo de `SIE-DS-02`.

## 2. Princípios inegociáveis

Herdados integralmente de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §2. **DevOps Exclusivo aplica-se mas não é acionado.**

## 3. Escopo

### 3.1 IN

- `ContextHeader` (organism): breadcrumb, título + descrição do módulo, badge de status, ações primárias (Inspetor, Validar projeto — ilustrativas, sem lógica real);
- `WorkflowStepper` (organism): 4 etapas do ciclo (Levantamento, Entrada, Dimensionamento, Documentação) com estados completo/ativo/pendente;
- 4 `MetricCard`s ilustrativos (fluxo concluído, circuitos, pior queda, demanda calculada);
- Painel de engenharia: tabela de circuitos (reaproveitando/expandindo a tabela ilustrativa já existente) + `SegmentedControl` (Tabela/Diagrama) + diagrama SVG ilustrativo simplificado;
- Dados seguem **ilustrativos** — nenhum contrato real de domínio é consumido nesta story (mesmo precedente de `SIE-DS-LOCAL-01`/`SIE-DS-02`; "dados reais apenas quando fornecidos pelos contratos existentes" do backlog-fonte é satisfeito por continuar sem inventar contrato onde nenhum foi ratificado para esta variante).

### 3.2 OUT

- Seleção real de circuito com sincronização a um Inspector panel funcional — isso é `SIE-DS-04`;
- Navegação real entre módulos (jornada/nav lateral continuam ilustrativas, sem roteamento real) — `SIE-DS-04`+;
- Qualquer alteração em `AppShell.tsx` ou rotas de produção;
- Qualquer operação remota.

## 4. Fontes de verdade

- `outputs/design-system/sie-command-center/prototype/index.html` linhas 151-393 (cabeçalho contextual + workspace-grid + workflow-panel + engineering-panel);
- `outputs/design-system/sie-command-center/docs/experience-architecture.md` §3 (Cabeçalho contextual, Workspace), §4 (padrão Overview);
- `docs/analysis/GAP-ANALISE-SIE-DS-02-vs-PROTOTIPO.md`.

## 5. Máquina de estados

```text
sm_story_creation → po_story_validation → architect_ratification → dev_implementation → qa_review → local_done
```

## 6. Critério de conclusão

`local_done` quando: story `Done`, QA `PASS`/`CONCERNS` sem bloqueio, lint/typecheck/test/build locais verdes, legado intocado, e a rota de preview demonstrando cabeçalho contextual + Overview funcionais localmente.

---

— Orion (`@aiox-master`), escopando SIE-DS-03 sem tocar produção
