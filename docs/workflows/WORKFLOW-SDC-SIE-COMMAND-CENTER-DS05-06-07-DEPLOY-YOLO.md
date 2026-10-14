# Workflow SDC Headless YOLO — SIE Command Center: SIE-DS-05 (Decision) + SIE-DS-06 + SIE-DS-07 até deploy

**Versão:** 1.0.0
**Data:** 2026-07-31
**Status:** Ready for dry-run; execução live de qualquer fase remota exige manifesto autorizado (seção 7) — **nenhuma autorização remota é concedida por este documento**
**Modo:** YOLO agente-a-agente (sessão manual real, mesmo padrão já usado em `SIE-DS-00` a `SIE-DS-05`), zero prompts durante cada fase local
**Escopo:** conclusão do backlog-semente de UI (`DecisionTemplate` restante de `SIE-DS-05`, `SIE-DS-06` Canvas+Inspector do Unifilar, `SIE-DS-07` Qualidade integrada e rollout), com cadeia completa `@sm → @po → @architect → @dev → @qa → @devops` até deploy
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
**Conformidade:** `.aiox-core/constitution.md`

> **Isto é uma escalada de escopo real em relação a tudo que foi executado até agora nesta sessão.** `SIE-DS-00` a `SIE-DS-05` rodaram **local-only, sem nenhuma operação remota**, por decisão explícita do usuário (reafirmada em cada story). Este documento é o primeiro desta sessão que **prevê chegar a `@devops` até deploy em produção** (`sie.applicationmanager.com.br`, sistema de dimensionamento elétrico NBR 5410 em uso real). Por isso:
>
> 1. Criar este arquivo **não autoriza deploy**. Nenhuma flag de operação remota é `true` por padrão (seção 7).
> 2. Antes de qualquer execução que chegue à Fase F (`@devops`), o orquestrador **deve** confirmar explicitamente com o usuário o escopo exato de autorização remota — mesma pergunta já feita antes de `SIE-DS-02` (push+PR-só-revisão / tudo-automático-até-produção / só-local). Este workflow não pressupõe a resposta.
> 3. Precedente real já registrado no repositório: `sistema-de-instala-es-el-tricas-sie-main/devops/deploy-local-report-2026-07-09.md` — um deploy anterior (Epic 10) fez merge **local** (fast-forward de branch), build de verificação e smoke test, mas **não executou push/PR**, aguardando autorização explícita separada. Este workflow segue o mesmo padrão como piso mínimo de segurança.

## 1. Objetivo

Fechar o restante do backlog-semente de UI do SIE Command Center:

- **`SIE-DS-05` (restante):** `DecisionTemplate` — `ContextHeader → ContextSummary → OptionComparison → ImpactSummary → Confirmation` (`docs/component-catalog.md` §Templates), explicitamente adiado em `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-LOCAL-YOLO.md`.
- **`SIE-DS-06`:** Canvas + Inspector para Unifilar — `CanvasInspectorTemplate` (`ContextHeader → CanvasToolbar → DiagramCanvas ↔ ContextInspector`), usando `src/components/unifilar/` **existente** como referência funcional (não como algo a substituir — ver Restrições).
- **`SIE-DS-07`:** Qualidade integrada e rollout — regressão visual/funcional, teclado/foco/leitor de tela/zoom/reflow, `prefers-reduced-motion`, documentação, **deploy opt-in**, rollback verificado, legado mantido.

E, se e somente se autorizado explicitamente, publicar via `@devops`.

## 2. Princípios inegociáveis

Herdados integralmente de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §2, sem exceção — incluindo **Fail Closed** (§2.8: "YOLO nunca transforma BLOCK em PASS") e **DevOps Exclusivo** (§2.10). Este documento **acrescenta**, não substitui, o Manifesto Imutável da seção 7 do workflow-fonte.

## 3. Escopo

### 3.1 IN

**SIE-DS-05 (Decision):**
- `DecisionPanel`/`DecisionTemplate`: comparação de opções (ex.: método de instalação alternativo para o circuito C14 de `SIE-DS-05`), motivo, impacto downstream ilustrativo, confirmação — sem execução de decisão real (mesmo padrão ilustrativo das stories anteriores).

**SIE-DS-06 (Canvas + Inspector):**
- `DiagramCanvas` + `CanvasToolbar` dentro do shell do Command Center, consumindo **dados reais já expostos** por `src/components/unifilar/` (`UnifilarCanvas.tsx`, `UnifilarWorkspace.tsx`, contratos existentes) — este é o primeiro item do backlog que pode legitimamente sair do "100% ilustrativo", pois o backlog-semente original (`WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §8, item `SIE-DS-06`) pede explicitamente "componentes atuais de `src/components/unifilar/`" como base, com "exportação existente preservada";
- Sincronização com `ContextInspector` (reaproveitando o organism de `SIE-DS-04`).

**SIE-DS-07 (Qualidade e rollout):**
- Checklist de regressão visual/funcional formal;
- Auditoria de teclado, foco, leitor de tela, zoom 200%, reflow (320/768/1280px), `prefers-reduced-motion` — sobre **tudo** que foi construído em `SIE-DS-LOCAL-01` a `SIE-DS-06`;
- Documentação consolidada (pattern library mínima);
- Manifesto de deploy opt-in (seção 7) preparado — **preenchido, não necessariamente autorizado**;
- Verificação de rollback (flag `VITE_FEATURE_SIE_COMMAND_CENTER` desligada reproduz o legado byte-a-byte).

### 3.2 OUT

- Qualquer alteração em `AppShell.tsx`, rotas de produção existentes, ou nos componentes de `src/components/unifilar/` além de consumi-los (SIE-DS-06 lê, não modifica o Unifilar existente);
- Migração de dados, alteração de contrato CLI/API;
- Ativação da variante como padrão para todos os usuários (fora de escopo até story própria, conforme `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §17: "Torná-la padrão exige escopo e autorização explícitos em story própria");
- **Qualquer operação remota não explicitamente autorizada pelo usuário no momento da execução da Fase F**, independentemente do que a seção 7 abaixo declarar como "preenchido".

## 4. Fontes de verdade

- `docs/component-catalog.md` (Templates `DecisionTemplate`, `CanvasInspectorTemplate`; Organisms `DiagramCanvas`, `DecisionPanel`, `ValidationSummary`);
- `outputs/design-system/sie-command-center/docs/experience-architecture.md` §4, §7, §8, §10;
- `sistema-de-instala-es-el-tricas-sie-main/src/components/unifilar/` (referência funcional real para `SIE-DS-06`);
- `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` (contrato base, seções 15 "Gates técnicos" e 22 "Critério de conclusão" aplicam-se integralmente a `SIE-DS-07`);
- `sistema-de-instala-es-el-tricas-sie-main/devops/deploy-local-report-2026-07-09.md` (precedente real de deploy local sem push/PR).

## 5. Máquina de estados (completa — inclui `@devops`)

```text
manifest_validation
  → sm_story_creation (SIE-DS-05-decision)
    → po_story_validation
      → architect_ratification
        → dev_implementation
          → qa_review
            → [repete para SIE-DS-06]
              → [repete para SIE-DS-07, incluindo gates técnicos completos de §15]
                → devops_pre_push
                  → push*
                    → pull_request*
                      → merge*
                        → release*
                          → deploy*
                            → smoke
                              → deployed
```

`*` — cada seta marcada exige sua própria flag de autorização (tabela abaixo) confirmada pelo usuário **no momento da execução**, não neste documento.

## 6. Manifesto imutável — estado inicial (NÃO autorizado)

```yaml
sdc_execution:
  source_artifact: "docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-DS05-06-07-DEPLOY-YOLO.md"
  story_scope: ["SIE-DS-05-decision", "SIE-DS-06", "SIE-DS-07"]
  execution_mode: "yolo"
  interaction_policy: "never_prompt_for_local_phases; MUST_prompt_before_any_remote_operation"

  target_branch: "<indefinido — @devops/usuário define no momento da execução>"
  base_branch: "master"
  remote_repository: "<indefinido>"
  deploy_environment: "<indefinido — staging ou produção, decisão do usuário>"
  deploy_runbook: "<indefinido — ver devops/deploy-local-report-2026-07-09.md como referência de padrão local; runbook de produção real ainda não identificado neste documento>"

  remote_operations_authorized: false
  pull_request_authorized: false
  merge_authorized: false
  release_authorized: false
  deploy_authorized: false
  rollback_authorized: true
  migrations_authorized: false

  max_po_iterations: 3
  max_architect_iterations: 3
  max_qa_iterations: 5

  required_agents: [sm, po, architect, dev, qa, devops]
```

**Regra explícita:** nenhum agente — incluindo `@aiox-master` — pode alterar `*_authorized: false` para `true` neste arquivo ou em qualquer cópia dele sem que o usuário tenha dito isso explicitamente, na conversa, no momento em que a Fase F for alcançada. "O documento existe" não é autorização. "A story está Done" não é autorização. Cada operação remota (push, PR, merge, release, deploy) exige sua própria confirmação — mesma granularidade do workflow-fonte §16.

## 7. Backlog desta execução

| Ordem | Story | Herda ratificação de |
|---|---|---|
| 1 | `SIE-DS-05-decision` (DecisionTemplate) | `SIE-DS-00`, `SIE-DS-05` (ParametersResultsTemplate) |
| 2 | `SIE-DS-06` (Canvas + Inspector Unifilar) | `SIE-DS-04` (ContextInspector), arquitetura real de `src/components/unifilar/` |
| 3 | `SIE-DS-07` (Qualidade e rollout) | Todas as anteriores — é uma auditoria + gate, não um organism novo |

Cada story passa pela cadeia completa (§5) até `qa_review` antes da próxima iniciar. **Somente após as 3 estarem `Done` com QA `PASS`/`CONCERNS`** a Fase F (`@devops`) é alcançável — e mesmo assim, sujeita à confirmação de escopo do usuário.

## 8. Gates técnicos (aplicam-se com força total a partir de `SIE-DS-07`)

Herdados de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §15 — lint, typecheck, testes, build (root e frontend, incluindo `build:spa`), acessibilidade completa, CodeRabbit/segurança. **Nota de risco herdada desta sessão:** CodeRabbit está indisponível (SIGILL/exit 132) desde `SIE-DS-00`, confirmado quebrado em 6 stories consecutivas até `SIE-DS-05`. `SIE-DS-07` **não pode** declarar qualidade "integrada" com esse gate ainda quebrado — reparar o CodeRabbit é pré-requisito de fato para `SIE-DS-07` ser honesta sobre seu próprio nome, mesmo que o restante dos gates (lint/typecheck/test/build reais) continue compensando funcionalmente.

## 9. Critério de conclusão

Terminal `DEPLOYED` **apenas** quando, além de tudo que `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §22 exige: (a) as 3 stories desta execução estão `Done`; (b) o usuário confirmou explicitamente, na conversa, a autorização de cada operação remota necessária; (c) o CodeRabbit está funcional ou uma decisão de waiver explícita e autorizada existir. Qualquer condição não atendida produz `BLOCKED`, nunca sucesso parcial — e `BLOCKED` por falta de autorização do usuário é o resultado **esperado e correto** se a pergunta da seção 6 nunca for respondida.

---

— River (`@sm`), redigindo o workflow a pedido do usuário — a criação deste arquivo não constitui autorização de deploy
