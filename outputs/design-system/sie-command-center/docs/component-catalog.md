# Catálogo de componentes — SIE Command Center

## Contrato comum

Todo componente:

- consome tokens `--sie-*`;
- oferece `default`, `hover`, `focus-visible`, `selected/pressed` e `disabled`;
- mantém nome acessível e ordem de foco previsível;
- suporta densidade `comfortable` e `compact` quando tabular ou operacional;
- não codifica regra normativa;
- não apresenta cor como único indicador de estado.

## Atoms

| Componente | Responsabilidade | Requisitos principais |
|---|---|---|
| `Button` | ação explícita | primary, secondary, ghost, danger; loading |
| `IconButton` | ação compacta | tooltip, nome acessível, alvo ≥ 24 px |
| `TextField` | entrada de texto | label persistente, helper, erro |
| `NumberField` | valor técnico | unidade, precisão, limites, locale |
| `Select` | escolha finita | busca quando lista longa, teclado |
| `Checkbox` | seleção múltipla | indeterminate |
| `StatusDot` | sinal complementar | sempre acompanhado de texto acessível |
| `StatusBadge` | estado técnico | ícone/texto e quatro severidades |
| `EngineeringValue` | valor calculado | mono, unidade, precisão, origem |
| `KeyboardHint` | atalho | somente auxílio, nunca único caminho |
| `Divider` | estrutura | sutil, forte, inverso |
| `Skeleton` | loading | geometria equivalente ao conteúdo |

## Molecules

| Componente | Composição | Uso |
|---|---|---|
| `FormField` | label + control + helper/error | formulários técnicos |
| `SearchField` | input + ícone + clear | listas e paleta |
| `ProjectSwitcher` | avatar + projeto + trigger | cabeçalho global |
| `ModuleNavItem` | ícone + label + estado/count | navegação lateral |
| `MetricCard` | label + value + context/trend | overview |
| `AlertCallout` | severity + title + reason + next step | alerta persistente |
| `PropertyRow` | key + value + source | inspetor |
| `TraceItem` | node + label + source | rastreabilidade |
| `CircuitRow` | identity + state + values + action | grid de engenharia |
| `CommandItem` | icon + command + category + shortcut | paleta |
| `SegmentedControl` | 2–4 opções exclusivas | modos de visualização |

## Organisms

| Componente | Função | Slots/variações |
|---|---|---|
| `EngineeringShell` | estrutura global | sidebar, header, main |
| `ModuleNavigation` | módulos por ciclo | expanded, drawer |
| `ContextHeader` | contexto e ações | compact on scroll |
| `WorkflowStepper` | progresso técnico | horizontal, vertical |
| `EngineeringDataGrid` | dados densos | sort, filter, select, bulk |
| `ContextInspector` | propriedades e rastreabilidade | docked, drawer, full-screen |
| `CommandPalette` | navegação e ação rápida | contextual groups |
| `DiagramCanvas` | unifilar/interação espacial | toolbar, legend, selection |
| `ValidationSummary` | pendências agregadas | severity groups |
| `DecisionPanel` | comparação e confirmação | eligible, blocked, pending |

## Templates

### `OverviewTemplate`

`ContextHeader → MetricGrid → WorkflowStepper → RiskList`

### `ListInspectorTemplate`

`ContextHeader → FilterToolbar → EngineeringDataGrid ↔ ContextInspector`

### `ParametersResultsTemplate`

`ContextHeader → ParameterPanel → ResultSummary → EngineeringDataGrid`

### `CanvasInspectorTemplate`

`ContextHeader → CanvasToolbar → DiagramCanvas ↔ ContextInspector`

### `DecisionTemplate`

`ContextHeader → ContextSummary → OptionComparison → ImpactSummary → Confirmation`

## Regras de composição

1. Um organismo não acessa regra de domínio diretamente; recebe estado e callbacks tipados.
2. Feedback de campo fica no `FormField`; feedback do processo fica em `AlertCallout`.
3. `ContextInspector` não substitui dialog de confirmação destrutiva.
4. `EngineeringDataGrid` preserva headers, caption e operação por teclado.
5. `MetricCard` resume; deve apontar para o detalhe correspondente.
6. Status `pending`, `warning` e `blocked` sempre incluem próxima ação.

## Nomenclatura de estados

| Estado semântico | Texto preferido | Evitar |
|---|---|---|
| `success` | Conforme / Concluído | OK isolado |
| `info` | Em análise / Em dimensionamento | Processando sem contexto |
| `warning` | Requer revisão | Atenção sem motivo |
| `danger` | Bloqueado / Incompatível | Erro genérico |
| `neutral` | Pendente / Não iniciado | `-` |

