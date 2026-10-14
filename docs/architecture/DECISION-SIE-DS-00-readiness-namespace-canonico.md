# DECISION SIE-DS-00 — Readiness e namespace canônico do SIE Command Center

**Story:** `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md`
**Workflow-fonte:** `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` (backlog-semente §8, item SIE-DS-00)
**Fonte de design:** `outputs/design-system/sie-command-center/`
**Ratificado por:** Aria (`@architect`) — 2026-07-31
**Redigido por:** Dex (`@dev`) — 2026-07-31, conforme veredito ratificado (nenhuma decisão nova foi tomada nesta redação)

> Este documento é o artefato produzido pela story `SIE-DS-00`. Consolida, sem alterar, o `architecture_verdict` registrado em `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` (seção "🏛️ Architecture Ratification") e em `.aiox/handoffs/SIE-DS-00-architect-to-dev.yaml`. Nenhum código de produção é criado, modificado ou removido por este documento (AC5).

---

## 1. Decisão de consumo (AC1)

`outputs/design-system/sie-command-center/` permanece **consumido diretamente como fonte de implementação** para as stories SIE-DS-01 a SIE-DS-07. A promoção física para os paths canônicos do squad de design system (`squads/design-system/...`, `workspace/...`, `.aiox/squad-runtime/design/...`) **não é executada** por esta decisão nem por nenhuma story deste backlog-semente — esses paths não existem neste checkout (capability gap confirmado em `outputs/design-system/sie-command-center/.state.yaml` e em `validation/quality-report.md`, seção "Capability gap do squad").

Justificativa: a promoção canônica exigiria infraestrutura de squad ausente (`workspace/scripts/resolve-squad-workspace-readiness.cjs`, `squads/design-system/scripts/design-system/resolve_business_design_system.cjs`, `apps/design-starter/README.md`, `.aiox/squad-runtime/design/design-chief/session-context.yaml`) cuja criação está fora do escopo IN de `WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md` §4.1. Reavaliar esta decisão exigiria story própria caso a infraestrutura do squad seja criada no futuro.

## 2. Namespace aditivo (AC2)

Ratificado por `@architect` (ver `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md` §"🏛️ Architecture Ratification"):

| Camada | Namespace | Motivo |
|---|---|---|
| CSS custom properties | `--sie-cc-*` | `--sie-*` puro já em uso em produção por `sistema-de-instala-es-el-tricas-sie-main/src/components/unifilar/tokens_sie.css` (`--sie-fundo`, `--sie-texto`, `--sie-erro-fill`, etc.), consumido por `UnifilarCanvas.tsx`, `UnifilarWorkspace.tsx`, `GraficoBarrasQueda.tsx`, `PainelSimulacaoQuedaTensao.tsx`, `simbolos_iec.tsx`, `src/styles.css`. Reaproveitar a mesma raiz de namespace do design-source (`outputs/design-system/sie-command-center/tokens/sie-premium.css`, que também usa `--sie-*`) criaria ambiguidade de propriedade. |
| Componentes | `src/components/command-center/` | Sibling aditivo de `src/components/unifilar/` e `src/components/app/`, seguindo a convenção de agrupamento por feature já usada no projeto. |
| Atributo de tema (se necessário) | `[data-theme="sie-cc"]` | `[data-theme="sie-g100"]` já é reservado pelo legado em `tokens_sie.css` linha 2. |

**Verificação de colisão realizada:** `grep -rln -- "--sie-" sistema-de-instala-es-el-tricas-sie-main/src/` retornou 10 arquivos (listados acima). Nenhum nome completo de variável colide com os tokens declarados em `outputs/design-system/sie-command-center/tokens/sie-premium.css`, mas a raiz de prefixo compartilhada foi considerada risco de governança suficiente para justificar a disambiguação `--sie-cc-*`.

## 3. Feature flag e rollback (AC3)

| Fase (`adoption-plan.md`) | Mecanismo | Rollback |
|---|---|---|
| Fase 1 — camada de tokens | Import isolado do arquivo de tokens `--sie-cc-*` | Remover a importação da nova camada |
| Fase 2 — shell opt-in | `VITE_FEATURE_SIE_COMMAND_CENTER` (`import.meta.env`, mesmo padrão já usado em `src/routes/diagnostico.spa.tsx` e `src/lib/config.server.ts`), default ausente/`false` = legado (`AppShell`) | Desativar a flag |

Nenhuma biblioteca de feature flag nova é introduzida. Nenhuma migração de dados está envolvida em nenhuma das duas fases — rollback é reversão de arquivo/flag.

## 4. Gap `ARCHITECT_PHASE_UNSUPPORTED` (AC4)

Confirmado e mantido sem alteração nesta story:

- `.aiox-core/core/orchestration/sdc-headless-yolo-runner.js` e `.aiox-core/development/scripts/sdc-headless-yolo.js` não expõem nenhuma fase/adapter `@architect` distinta (grep case-insensitive, zero ocorrências — confirmado independentemente por `@aiox-master`, `@po` e `@architect` nesta mesma sessão).
- A ratificação arquitetural de `SIE-DS-00` **foi executada manualmente**, agente-a-agente (`@sm` → `@po` → `@architect` → `@dev`, cada invocação real desta sessão), **não** pelo runner headless automatizado.
- **Este documento não resolve o gap.** Qualquer tentativa de executar o restante do backlog-semente (`SIE-DS-01` a `SIE-DS-07`) em modo `--mode=yolo` totalmente automatizado permanece **BLOCKED** até que o adapter `@architect` seja implementado em `.aiox-core/core/orchestration/` — camada L1 (never-modify) sob a Framework vs Project Boundary do projeto, fora da autoridade de `@dev` e desta story. Resolução requer story própria de framework governance sob `@aiox-master`.
- Evidência primária: `.aiox/sdc-headless/sie-command-center-precondition-check-2026-07-31T05-50-15.883Z.yaml`.

## 5. Zero impacto em produção (AC5)

**Confirmado.** O único arquivo criado por esta story é este próprio documento (`docs/architecture/DECISION-SIE-DS-00-readiness-namespace-canonico.md`) e o arquivo de story em `docs/stories/`. Nenhum arquivo em `sistema-de-instala-es-el-tricas-sie-main/src/` foi criado, modificado ou removido. `AppShell.tsx` e todos os componentes legacy listados como paths protegidos permanecem intocados.

---

## Referências

- `docs/workflows/WORKFLOW-SDC-SIE-COMMAND-CENTER-YOLO.md`
- `docs/stories/story-SIE-DS-00-readiness-namespace-canonico.md`
- `.aiox/handoffs/SIE-DS-00-sm-to-po.yaml`
- `.aiox/handoffs/SIE-DS-00-po-to-architect.yaml`
- `.aiox/handoffs/SIE-DS-00-architect-to-dev.yaml`
- `outputs/design-system/sie-command-center/.state.yaml`
- `outputs/design-system/sie-command-center/validation/quality-report.md`
- `outputs/design-system/sie-command-center/migration/adoption-plan.md`
- `.aiox/sdc-headless/sie-command-center-precondition-check-2026-07-31T05-50-15.883Z.yaml`

## Próximo passo

`SIE-DS-01` (Foundations e tokens) pode iniciar somente após QA Gate desta story (`SIE-DS-00`) = PASS/CONCERNS/WAIVED, consumindo o namespace `--sie-cc-*` ratificado na seção 2.
