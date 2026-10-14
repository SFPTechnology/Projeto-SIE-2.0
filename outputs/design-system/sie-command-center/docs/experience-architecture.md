# Arquitetura de experiência — SIE Command Center

## 1. Norte do produto

**Vibe:** centro de comando de engenharia preciso, premium e corporativo, com alta densidade controlada e hierarquia por estado.

O SIE deixa de parecer uma sequência de páginas e passa a representar um **projeto elétrico em evolução**. A interface revela o ciclo técnico, preserva o contexto e permite investigar qualquer número até sua origem.

## 2. Arquitetura da informação

```text
Portfólio de projetos
└── Projeto ativo
    ├── Workspace
    │   ├── Visão geral
    │   └── Ambientes e cargas
    ├── Entrada
    │   └── Padrão de entrada
    ├── Dimensionamento
    │   ├── Circuitos
    │   ├── Correntes
    │   ├── Condutores
    │   └── Queda de tensão
    └── Documentação
        ├── Diagrama unifilar
        └── Diagnóstico
```

Essa taxonomia reorganiza as rotas existentes. Não define novas capacidades de domínio.

## 3. Shell

### Navegação lateral — 256 px

- Marca e ambiente;
- Módulos agrupados pelo ciclo;
- Contagem/estado quando relevante;
- Item ativo com barra ciano e superfície azul;
- Colapso para drawer abaixo de 992 px.

### Cabeçalho global — 56 px

- Projeto ativo e troca de contexto;
- Estado demonstrativo/sincronização futura;
- Busca e paleta de comandos;
- Densidade;
- Autor/perfil.

### Cabeçalho contextual

- Breadcrumb;
- Título e descrição do módulo;
- Estado do projeto;
- Ação primária única;
- Ação de inspetor quando aplicável.

### Workspace

- **Primary canvas:** tabela, formulário, gráfico ou diagrama;
- **Inspector:** propriedades do item, origem, alertas e ações contextuais;
- **Feedback:** toast para conclusão simples; inline/banner para efeito persistente; dialog apenas para decisão bloqueante.

## 4. Padrões de página

| Padrão | Uso | Composição |
|---|---|---|
| Overview | Visão geral do projeto | métricas + jornada + riscos |
| List + Inspector | Ambientes, circuitos, diagnósticos | tabela/lista + detalhe contextual |
| Parameters + Results | Padrão, correntes, condutores, queda | parâmetros colapsáveis + resultados persistentes |
| Canvas + Inspector | Unifilar | árvore/contexto + canvas + propriedades |
| Decision Flow | Seleções com impacto downstream | opções comparáveis + motivo + confirmação |

## 5. Atomic Design

### Atoms

- `Button`, `IconButton`, `Input`, `Select`, `Checkbox`, `Tag`;
- `StatusDot`, `StatusBadge`, `MetricValue`, `Divider`, `KeyboardHint`;
- `EngineeringValue` com unidade, precisão e fonte.

### Molecules

- `FormField`, `SearchField`, `ProjectSwitcher`;
- `MetricCard`, `AlertCallout`, `PropertyRow`;
- `CircuitRow`, `TraceItem`, `CommandItem`;
- `ModuleNavItem` e `SegmentedControl`.

### Organisms

- `EngineeringShell`, `ModuleNavigation`, `ContextHeader`;
- `WorkflowStepper`, `EngineeringDataGrid`;
- `ContextInspector`, `CommandPalette`;
- `DiagramCanvas`, `ValidationSummary`.

### Templates

- `OverviewTemplate`;
- `ListInspectorTemplate`;
- `ParametersResultsTemplate`;
- `CanvasInspectorTemplate`;
- `DecisionTemplate`.

## 6. Tokens

### Cores

- `#0B3367` — identidade e ação primária;
- `#061E3D` — shell e superfícies inversas;
- `#3EC7D3` — seleção/telemetria, nunca ação destrutiva;
- Neutros frios — dados e superfícies;
- Status possuem texto e forma; cor nunca é o único canal.

### Tipografia

- Sans: Inter/Segoe UI para leitura e controles;
- Mono: IBM Plex Mono/Cascadia Code para valores, unidades, IDs e atalhos;
- Números técnicos usam `tabular-nums`;
- Display máximo de 32 px: software de engenharia não precisa de hero promocional.

### Geometria e profundidade

- Controles 6 px; painéis 10 px; badges pill;
- Profundidade por camadas tonais e bordas;
- Sombra whisper apenas em painéis; floating somente para dialog, drawer e toast;
- Sem glassmorphism decorativo no conteúdo técnico.

### Espaçamento e densidade

- Escala base de 4 px;
- `comfortable`: controle 40 px, linha 48 px;
- `compact`: controle 32 px, linha 40 px;
- Alvos continuam com pelo menos 24 × 24 px em ambos os modos.

### Motion

- 80 ms para feedback imediato;
- 140 ms para hover/estado;
- 220 ms para drawer/inspetor;
- Sem animações de dados que dificultem comparação;
- `prefers-reduced-motion` reduz transições.

## 7. Estados obrigatórios

Todo componente interativo possui:

- default;
- hover;
- focus-visible;
- pressed/selected;
- disabled;
- loading quando assíncrono;
- error/success quando submetível.

Todo resultado técnico possui:

- valor;
- unidade;
- precisão consistente;
- estado;
- origem/rastreabilidade;
- timestamp/versão quando o contrato disponibilizar;
- motivo e próxima ação quando inválido ou pendente.

## 8. Responsividade

| Faixa | Composição |
|---|---|
| ≥ 1400 px | navegação + canvas + inspetor |
| 992–1399 px | navegação + canvas; inspetor em drawer |
| 768–991 px | drawer de navegação + canvas; ações condensadas |
| < 768 px | uma coluna, tabelas roláveis e detalhe em tela/drawer |

Mobile é suportado para consulta e ações essenciais. A hipótese de uso principal em desktop ainda requer validação.

## 9. Linguagem

- Ação em verbo: “Recalcular circuito”, não “Processar”;
- Estado técnico em linguagem direta: “Requer revisão”;
- Mensagem sempre responde: **o que aconteceu, por quê, impacto e próximo passo**;
- Siglas como IB e ΔV acompanham explicação no primeiro contato ou tooltip;
- “Simular” nunca implica que o cenário já foi aplicado.

## 10. Restrições

- Não usar cores fora dos tokens;
- Não usar estilos inline;
- Não criar mais de duas cores de acento;
- Não ocultar ação primária em menu overflow;
- Não usar modal para leitura passiva;
- Não depender apenas de drag, hover ou cor;
- Não criar funcionalidade de domínio apenas para preencher layout;
- Não permitir que a UI contradiga resultados da CLI/API.

