# Benchmark UX/UI — software moderno de engenharia e enterprise

**Pesquisa:** 2026-07-31  
**Critério:** fontes oficiais/primárias; padrões adaptados, sem copiar aparência ou layout proprietário

## Referências e achados

### Autodesk Platform Services Viewer

O viewer oficial expõe árvore de objetos, seleção, propriedades, toolbar, painéis e estado de visualização. Isso sustenta o padrão **estrutura → canvas → propriedades**, recorrente em software técnico.

- [Autodesk Viewer3D](https://aps.autodesk.com/en/docs/viewer/v6/reference/Viewing/Viewer3D/)
- [Autodesk GuiViewer3D](https://aps.autodesk.com/en/docs/viewer/v3/reference/javascript/guiviewer3d)

**Aplicação no SIE:** diagrama/cálculo no centro, contexto estrutural na navegação e propriedades rastreáveis no inspetor lateral.

### Onshape

A documentação oficial oferece toolbar contextual, busca de ferramentas, atalhos customizáveis, preview antes de confirmar e mapa pesquisável de teclado.

- [Onshape Feature Tools](https://cad.onshape.com/help/Content/PartStudio/feature_tools.htm)
- [Onshape Keyboard Shortcuts](https://cad.onshape.com/help/Content/Home/keyboard_shortcuts_and_hotkeys.htm)

**Aplicação no SIE:** paleta `Ctrl/Cmd + K`, ajuda por `?`, preview/simulação e confirmação explícita para ações que alterem cenário.

### Bentley iTwin

O iTwin combina dados de engenharia, visualização, métricas e alertas em contexto, com viewer extensível.

- [iTwin Platform — Get Started](https://developer.bentley.com/tutorials/get-started-with-itwin-platform/)
- [Bentley iTwin](https://www.bentley.com/software/itwin/)

**Aplicação no SIE:** alertas e métricas devem manter vínculo visual com o elemento/circuito de origem.

### Siemens Industrial Experience

O Siemens IX é voltado a contextos industriais e organiza application frame, navegação, grids, KPIs, message bars, pills e progresso como componentes coerentes.

- [Siemens IX — princípios](https://ix.siemens.io/version-2.7/docs/introduction/)
- [Siemens IX — componentes](https://ix.siemens.io/docs/components/overview)

**Aplicação no SIE:** shell técnico consistente, status compacto, feedback assíncrono e componentes de dados reutilizáveis.

### IBM Carbon

Carbon defende reuso sistemático e incorpora operação por teclado na tabela de dados. A aplicação atual já depende de Carbon, portanto a proposta preserva o investimento e sugere uma camada SIE por cima das primitives.

- [Carbon — componentes](https://carbondesignsystem.com/components/overview/components/)
- [Carbon — acessibilidade da Data Table](https://carbondesignsystem.com/components/data-table/accessibility/)

**Aplicação no SIE:** manter semântica e comportamento Carbon onde já funcionam; consolidar aparência, densidade e tokens sem reimplementar primitives maduras.

### SAP Fiori

Dynamic Page mantém ações importantes enquanto o cabeçalho pode reduzir; Flexible Column Layout organiza relações lista-detalhe em até três colunas e responde para uma coluna em telas pequenas.

- [SAP Fiori Dynamic Page](https://experience.sap.com/fiori-design-web/dynamic-page-layout/)
- [SAP Fiori Flexible Column Layout](https://experience.sap.com/fiori-design-web/flexible-column-layout-web-component/)

**Aplicação no SIE:** cabeçalho contextual enxuto, conteúdo central e inspetor/detalhe responsivo; o inspetor vira overlay em larguras menores.

### Linear

Linear usa busca global, command menu contextual, atalhos, seleção múltipla e preferências de visualização para acelerar usuários frequentes.

- [Linear Search](https://linear.app/docs/search)
- [Linear Select Issues](https://linear.app/docs/select-issues)
- [Linear Display Options](https://linear.app/docs/display-options)

**Aplicação no SIE:** navegação e comandos rápidos para especialistas, sem retirar os controles visíveis necessários a usuários ocasionais.

### Microsoft Power Apps / Fluent

Aplicações model-driven são indicadas para processos densos e relacionados; a modernização recente destaca command bar, grids, formas e coerência visual.

- [Power Apps model-driven overview](https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview)
- [Modern Fluent look](https://learn.microsoft.com/en-us/power-apps/user/modern-fluent-design)

**Aplicação no SIE:** organizar a interface pelo modelo e pelo processo de engenharia, não por uma coleção de páginas independentes.

### W3C WCAG 2.2

WCAG 2.2 adiciona critérios como foco não oculto, alternativa a arrastar e alvo mínimo de 24 × 24 CSS px.

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Novidades da WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)

**Aplicação no SIE:** foco forte, alvos mínimos, inspetor sem ocultar foco, alternativa a interações espaciais e `prefers-reduced-motion`.

## Síntese aplicada

Os produtos não foram usados como referência estética literal. A inferência comum foi:

1. Software técnico moderno mantém **objeto selecionado e propriedades sincronizados**.
2. Navegação deve refletir **processo e dependências**, não apenas URLs.
3. Especialistas ganham velocidade com **busca, atalhos e densidade configurável**.
4. Estados técnicos precisam de **severidade + causa + próxima ação + origem**.
5. Layout responsivo deve mudar de composição, não apenas encolher.
6. A aparência premium vem de tipografia, ritmo e precisão — não de excesso de vidro, glow ou animação.

## Hipóteses que ainda exigem pesquisa com usuários

- Quem é a persona primária: projetista, operador assistido ou responsável técnico.
- Tamanho e quantidade de monitores no uso real.
- Frequência de troca entre módulos durante revisão.
- Terminologia mais compreensível para estados normativos.
- Limites aceitáveis de densidade e customização.

