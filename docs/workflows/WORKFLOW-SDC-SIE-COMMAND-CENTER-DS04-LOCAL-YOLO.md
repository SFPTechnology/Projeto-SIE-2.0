# Workflow SDC Headless YOLO — SIE Command Center: SIE-DS-04 (List + Inspector, local-only)

**Versão:** 1.0.0
**Data:** 2026-07-31
**Status:** Ready for execution — escopo local-only, sem operações remotas
**Modo:** YOLO agente-a-agente (sessão manual real), zero prompts durante a execução de cada fase
**Escopo:** implementação real do item canônico `SIE-DS-04` do backlog-semente (seleção de circuito sincronizada com um Inspector panel)
**Ratificações reutilizadas:** stories `SIE-DS-00`, `SIE-DS-LOCAL-01`, `SIE-DS-02`, `SIE-DS-03`
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
**Conformidade:** `.aiox-core/constitution.md`

> **Decisão do usuário (reafirmada):** mesmo formato de `SIE-DS-02`/`SIE-DS-03` — sem fase `@devops`. Cadeia termina em `@qa` → `local_done`.

## 1. Objetivo

Implementar o item canônico `SIE-DS-04` (List + Inspector): a tabela de circuitos de `EngineeringPanel` (`SIE-DS-03`) passa a ter seleção real, sincronizada com um painel de inspeção lateral (`ContextInspector`), replicando `prototype/index.html` linhas 396-470.

## 2. Princípios inegociáveis

Herdados de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §2. **DevOps Exclusivo aplica-se mas não é acionado.**

## 3. Escopo

### 3.1 IN

- `ContextInspector` (organism): painel lateral com propriedades do circuito selecionado (aplicação, fases, corrente, condutor, comprimento — ilustrativos), badge de estado, seção de rastreabilidade, ações ilustrativas;
- Seleção real na tabela de `EngineeringPanel`: clique e teclado (`Enter`/`Espaço`) selecionam uma linha; estado elevado ao componente pai (rota) para sincronizar com o Inspector;
- Estado vazio do Inspector quando nenhum circuito está selecionado;
- Detalhe progressivo: Inspector só aparece/preenche após seleção — sem duplicar nenhuma regra de cálculo ou normativa (dados são o mesmo array ilustrativo já existente, apenas exibidos).

### 3.2 OUT

- Sincronização com o modo Diagrama (seleção via SVG) — apenas a tabela seleciona, mesmo comportamento do protótipo;
- Navegação real entre módulos, dados reais de projeto;
- Qualquer alteração em `AppShell.tsx` ou rotas de produção;
- Qualquer operação remota.

## 4. Fontes de verdade

- `outputs/design-system/sie-command-center/prototype/index.html` linhas 296-347 (tabela) e 396-470 (inspector-panel);
- `outputs/design-system/sie-command-center/docs/experience-architecture.md` §3 (Workspace — Inspector), §4 (padrão List + Inspector).

## 5. Máquina de estados

```text
sm_story_creation → po_story_validation → architect_ratification → dev_implementation → qa_review → local_done
```

## 6. Critério de conclusão

`local_done` quando: story `Done`, QA sem bloqueio, gates técnicos locais verdes, legado intocado, seleção de circuito → Inspector funcionando de verdade no dev server local.

---

— Orion (`@aiox-master`), escopando SIE-DS-04 sem tocar produção
