# Workflow SDC Headless YOLO — SIE Command Center: Local Preview (pré-implementação)

**Versão:** 1.0.0
**Data:** 2026-07-31
**Status:** Ready for execution — escopo local-only, sem operações remotas
**Modo:** YOLO agente-a-agente (sessão manual real, mesmo padrão usado em `SIE-DS-00`), zero prompts durante a execução de cada fase
**Escopo:** tokens + shell mínimo do SIE Command Center, integrados ao app real **apenas para teste local**, atrás de feature flag
**Fonte de implementação:** `outputs/design-system/sie-command-center/`
**Ratificação de base (reutilizada, não re-decidida):** `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` §"🏛️ Architecture Ratification"
**Contrato SDC base:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
**Conformidade:** `.aiox-core/constitution.md`

> Este documento é uma **especialização deliberadamente menor** do backlog-semente SIE-DS-01/02. Não substitui `SIE-DS-01` (Foundations e tokens) nem `SIE-DS-02` (Engineering Shell opt-in) do backlog canônico — ambas ainda precisam ocorrer para a "implementação definitiva". Este workflow entrega uma **fundação real, mas explicitamente local e reversível**, para permitir avaliação visual/UX no app de verdade antes de comprometer o backlog completo.

## 1. Objetivo

Tornar o novo design system (`SIE Command Center`) visível e navegável **dentro do dev server local** do app real, sem alterar nenhum arquivo do design atual, sem qualquer operação remota (push/PR/merge/release/deploy), usando os tokens e a estratégia de shell já ratificados por `@architect` em `SIE-DS-00`.

## 2. Princípios inegociáveis (herdados de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §2)

Aplicam-se integralmente: CLI First, Story-Driven, No Invention, Agent Authority, Quality First, Legacy Preservation, Additive Delivery, Fail Closed, Idempotência. **DevOps Exclusivo** aplica-se mas **não é acionado** — este workflow não autoriza nenhuma operação remota, então a fase `@devops` do SDC não é necessária para este escopo.

## 3. Escopo

### 3.1 IN

- Arquivo de tokens `--sie-cc-*` (subconjunto necessário para o shell mínimo), porta de `outputs/design-system/sie-command-center/tokens/sie-premium.css`, namespace já ratificado;
- Componente `EngineeringShell` mínimo (header contextual + navegação placeholder + área de conteúdo), estilizado exclusivamente com os novos tokens;
- Uma rota nova e isolada (`src/routes/sie-command-center-preview.tsx`) que monta o `EngineeringShell` com conteúdo de demonstração;
- Gate por feature flag `VITE_FEATURE_SIE_COMMAND_CENTER` (`.env.local`, não versionado);
- Testes automatizados mínimos (vitest) para o componente e para os tokens;
- Validação local: lint, typecheck, testes, build — **sem** deploy.

### 3.2 OUT

- Qualquer alteração em `AppShell.tsx`, rotas existentes, `routeTree.gen.ts` manual, contratos de API/domínio;
- Migração de módulos reais (Ambientes, Circuitos, Diagnóstico, Padrão de entrada, etc.) para a nova variante — isso é `SIE-DS-03` a `SIE-DS-06`;
- Dados reais de projeto — a rota de preview usa dados ilustrativos, claramente identificados como tal (mesmo padrão do protótipo original);
- `git push`, `gh pr create`, merge, release, deploy — **nenhuma operação remota é autorizada por este documento**;
- Promoção desta rota de preview a rota canônica/produção — isso exige story própria com escopo e autorização explícitos.

## 4. Fontes de verdade

- `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` (namespace `--sie-cc-*`, path `src/components/command-center/`, flag `VITE_FEATURE_SIE_COMMAND_CENTER`, paths legados protegidos — todos já ratificados, reutilizados aqui sem nova decisão);
- `outputs/design-system/sie-command-center/tokens/sie-premium.css` e `docs/component-catalog.md`;
- `outputs/design-system/sie-command-center/prototype/` (referência visual);
- `.aiox-core/constitution.md`.

## 5. Máquina de estados (reduzida — sem fase DevOps remota)

```text
sm_story_creation → po_story_validation → architect_confirmation → dev_implementation → qa_review → local_done
```

`architect_confirmation` não é uma nova investigação completa: `@architect` confirma que a ratificação de `SIE-DS-00` cobre integralmente o namespace, a flag e a estratégia de shell para este escopo reduzido, e ratifica apenas o que for específico desta story (ex.: composição exata do `EngineeringShell` mínimo).

## 6. Backlog-semente

### SIE-DS-LOCAL-01 — Fundação local do SIE Command Center (preview)

Resultado esperado:
- `src/components/command-center/tokens/sie-cc-tokens.css` criado, consumindo o namespace `--sie-cc-*`;
- `src/components/command-center/EngineeringShell.tsx` criado (mínimo viável: header + nav placeholder + slot de conteúdo);
- `src/routes/sie-command-center-preview.tsx` criado, isolado, gated por `VITE_FEATURE_SIE_COMMAND_CENTER`;
- Testes vitest cobrindo o shell e o carregamento dos tokens;
- `AppShell.tsx` e todas as rotas existentes permanecem byte-a-byte idênticas;
- Instrução clara de como habilitar localmente (`.env.local`) e acessar a rota.

## 7. Critério de conclusão

Termina `local_done` quando: story `Done`, QA `PASS`/`CONCERNS` sem bloqueio, lint/typecheck/test/build locais verdes, `AppShell.tsx` e rotas legadas comprovadamente intocadas (`git diff` vazio para esses paths), e a rota de preview acessível em `http://localhost:5173/sie-command-center-preview` com a flag ativa.

Qualquer condição não atendida produz `BLOCKED` ou `FAILED` — nunca sucesso parcial, e nunca uma operação remota é executada para "compensar".

---

— Orion (`@aiox-master`), escopando um caminho seguro de avaliação antes da decisão definitiva
