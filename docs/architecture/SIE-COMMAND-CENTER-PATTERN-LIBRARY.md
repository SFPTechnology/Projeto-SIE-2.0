# Pattern Library — SIE Command Center (implementado)

**Story:** `SIE-DS-07` (AC6)
**Data:** 2026-07-31
**Escopo:** cataloga apenas o que foi **realmente construído** em `src/components/command-center/` ao longo de `SIE-DS-LOCAL-01` a `SIE-DS-06`. Não é o catálogo aspiracional completo (esse é `outputs/design-system/sie-command-center/docs/component-catalog.md`) — é o inventário real do que existe em produção-de-preview hoje.

Todos os componentes: consomem tokens `--sie-cc-*` (namespace ratificado em `SIE-DS-00`); não usam estilo inline; não codificam regra normativa/de domínio; densidade `comfortable`/`compact` suportada globalmente via `data-density` no `EngineeringShell`.

---

## Tokens

| Arquivo | Conteúdo |
|---|---|
| `tokens/sie-cc-tokens.css` | Cores de marca/superfície/texto/borda/status (5 severidades), tipografia, espaçamento, raio, sombra, duração/easing, densidade (`[data-density]`), `prefers-reduced-motion` |

## Atoms/Molecules (informais — não extraídos como componentes próprios, mas padrões repetidos)

| Padrão | Onde aparece | Descrição |
|---|---|---|
| Status badge | `ContextHeader`, `EngineeringPanel`, `ResultSummary`, `ContextInspector` | `.sie-cc-status-badge--{success\|info\|warning\|danger\|neutral}` — texto sempre acompanha a cor |
| Segmented control | `EngineeringPanel` | `role="group"` + `aria-pressed` |
| Property list (`<dl>`) | `ContextInspector`, `ParameterPanel` | par label/valor, `dt`/`dd` |

## Organisms

| Componente | Arquivo | Story de origem | Propósito |
|---|---|---|---|
| `EngineeringShell` | `EngineeringShell.tsx` | `SIE-DS-LOCAL-01`, reestruturado em `SIE-DS-02` | Shell global: nav lateral + cabeçalho + main + paleta de comandos |
| `ModuleNavigation` | `ModuleNavigation.tsx` | `SIE-DS-02` | Nav lateral, 4 grupos/9 itens, colapso CSS-only < 992px |
| `CommandPalette` | `CommandPalette.tsx` + `command-palette-logic.ts` | `SIE-DS-02` | Paleta `Ctrl/Cmd+K`, filtro + navegação por seta (lógica pura testável) |
| `ContextHeader` | `ContextHeader.tsx` | `SIE-DS-03`, ampliado em `SIE-DS-07` (`nivelTitulo`) | Breadcrumb + título + badge + ações; suporta `h1`/`h2` para evitar heading duplicado quando reusado na mesma página |
| `WorkflowStepper` | `WorkflowStepper.tsx` | `SIE-DS-03` | Jornada técnica, 4 etapas com estado |
| `MetricCardGrid` | `MetricCard.tsx` | `SIE-DS-03` | Grade de métricas ilustrativas |
| `EngineeringPanel` | `EngineeringPanel.tsx` | `SIE-DS-03`, seleção em `SIE-DS-04` | Tabela de circuitos (selecionável) + diagrama SVG conceitual + segmented control |
| `ContextInspector` | `ContextInspector.tsx` | `SIE-DS-04` | Painel de propriedades + rastreabilidade do item selecionado, com estado vazio |
| `ParameterPanel` | `ParameterPanel.tsx` | `SIE-DS-05` | Parâmetros colapsáveis (`<details>` nativo) |
| `ResultSummary` | `ResultSummary.tsx` | `SIE-DS-05` | Resultados com severidade + motivo + próxima ação (regra de composição do catálogo) |
| `DecisionPanel` | `DecisionPanel.tsx` + `decision-data.ts` | `SIE-DS-05-decision` | ContextSummary + OptionComparison (radio nativo) + ImpactSummary + Confirmation inline |
| `UnifilarPreviewSection` | `UnifilarPreviewSection.tsx` | `SIE-DS-06` | Wrapper fino ao redor do `UnifilarWorkspace` **real** de produção — não reimplementado |

## Hooks e utilitários

| Nome | Arquivo | Propósito |
|---|---|---|
| `useDensity`/`alternarDensidade` | `use-density.ts` | Estado de densidade `comfortable`/`compact` |
| `isCommandCenterPreviewEnabled` | `feature-flag.ts` | Gate da variante via `VITE_FEATURE_SIE_COMMAND_CENTER` |

## Dados ilustrativos (separados por convenção de Fast Refresh)

| Arquivo | Conteúdo |
|---|---|
| `module-navigation-data.ts` | Grupos/itens da nav lateral |
| `overview-data.ts` | Jornada, métricas, circuitos ilustrativos |
| `parameters-results-data.ts` | Parâmetros e resultados de Queda de tensão |
| `decision-data.ts` | Contexto e opções da decisão ilustrativa |
| `unifilar-preview-fixture.ts` | Fixture real, tipado, do `UnifilarWorkspace` (corrigido de um bug real encontrado em `tests/ui/unifilar-workspace.vrt.test.tsx` — ver `SIE-DS-06` QA gate) |

## Templates compostos (na rota de preview)

A rota `src/routes/sie-command-center-preview.tsx` empilha, na ordem: `ContextHeader` (Overview) → `MetricCardGrid` → `WorkflowStepper` → `EngineeringPanel` + `ContextInspector` (List+Inspector) → `ParameterPanel` + `ResultSummary` (Parameters+Results) → `DecisionPanel` (Decision) → `UnifilarPreviewSection` (Canvas+Inspector real).

Isso não é uma composição de produção — é uma página única de avaliação que demonstra todos os templates lado a lado, atrás da feature flag.

## O que NÃO foi construído (gaps conhecidos, não escondidos)

- `EngineeringDataGrid` completo (sort/filter/bulk) — `EngineeringPanel` é mais simples.
- `ValidationSummary` — não implementado.
- Overlay/fechamento por `Esc` no drawer de navegação mobile (`ModuleNavigation`) — registrado como Should-Fix em `SIE-DS-02`.
- Botão de ajuda (`?`) e atalho `?` para a paleta — não implementados (registrado em `docs/analysis/GAP-ANALISE-SIE-DS-02-vs-PROTOTIPO.md`).
