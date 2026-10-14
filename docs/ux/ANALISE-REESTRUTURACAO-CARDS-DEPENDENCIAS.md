# Análise UX/UI — reestruturação dos cards de Dependências

**Status:** pronto para detalhamento e implementação por `aiox-ux-design-expert`  
**Escopo:** rota/seção **Dependências**; apresentação, navegação e responsividade dos cards de dependências cadastradas.  
**Evidência visual primária:** `C:\Users\User\Downloads\Screenshot_235.jpg`  
**Restrições inegociáveis:** preservar as ações `Detalhe`, `Calcular`, `Historico` e `Duplicar`, incluindo seus rótulos, conteúdo, comportamento, permissões e rotas atuais.

## 1. Objetivo

Transformar os cards de dependências de fichas densas de consulta em unidades de decisão técnica: o usuário deve identificar, sem abrir cada item, **qual ambiente é**, **qual carga apresenta**, **qual é seu estado** e **qual próxima ação é necessária**.

O redesenho deve aumentar a visão abrangente da instalação sem alterar cálculos, regras NBR, dados de domínio, APIs, auditoria ou o conteúdo já exposto pelas quatro ações preservadas.

## 2. Diagnóstico da interface atual

A captura evidencia uma grade de duas colunas sob a busca e o botão de filtros. Cada card contém um conjunto completo de dados técnicos, mas sua hierarquia visual é quase plana: rótulos, valores, indicadores de verificação e metadados competem pelo mesmo espaço e contraste.

### Estrutura atual mapeada

| Bloco | Conteúdo observado | Leitura UX |
|---|---|---|
| Cabeçalho | Nome do ambiente, identificador/versão e estado `Calculada` | O nome é reconhecível, mas o estado não comunica prioridade, atualização ou necessidade de ação. |
| Caracterização | Tipo, categoria e dimensões | Dados úteis para contexto, porém consomem espaço vertical e não são escaneáveis em comparação entre cards. |
| Iluminação | Quantidade de pontos, VA, `VERIFICAR` e `Automático` | O selo de exceção aparece misturado aos valores; não há síntese de pendências. |
| Tomadas | Quantidade, VA, `VERIFICAR` e `Automático` | Repete o mesmo padrão e amplia a densidade sem tornar a criticidade evidente. |
| Cargas adicionais | Situação e observação | Informação relevante, mas sem diferenciação visual entre ausência, aviso e impacto técnico. |
| Rastreabilidade | Data e hora de atualização | Está presente, porém não se relaciona visualmente ao estado de atualização. |
| Ações | `Detalhe`, `Calcular`, `Historico`, `Duplicar` e menu | As quatro ações obrigatórias existem, mas têm área de toque e prioridade visual reduzidas. |

### Problemas prioritários

1. **Baixa escaneabilidade:** comparar cargas e pendências entre ambientes exige leitura sequencial de todos os rótulos.
2. **Estado insuficiente:** `Calculada` descreve um evento, não a condição operacional do item; não diferencia cálculo válido, necessidade de verificação ou dado desatualizado.
3. **Exceções diluídas:** selos `VERIFICAR` não formam uma fila de trabalho perceptível.
4. **Ações pouco contextuais:** o usuário vê as ações, mas não recebe sinal claro de quando calcular é a próxima ação recomendada.
5. **Visão de conjunto limitada:** busca e filtros existem, mas faltam contadores, ordenação e agrupamento para análise de muitos ambientes.

## 3. Direção de UX

Adotar o padrão **visão geral → exceção → aprofundamento**:

1. A página apresenta o estado agregado das dependências.
2. O card comunica o resumo técnico e somente as exceções que demandam atenção.
3. As ações existentes conduzem ao conteúdo e aos fluxos atuais, sem mudança funcional.

Ferramentas atuais de engenharia reforçam este modelo: filtros compostos por propriedades, visualizações salvas e foco em subconjuntos de interesse no Model Coordination; cartões filtráveis, expansíveis e orientados a KPI no Autodesk Insight; e inspeção contextual de itens em painel sem perder a lista no Autodesk Issues. [Model Coordination](https://help.autodesk.com/cloudhelp/ENU/Coord-Models/files/Model_Coord_Object_Filters.html), [Insight](https://help.autodesk.com/cloudhelp/ENG/Docs-Insight/files/Insight_Customize_Dashboards.html), [Issues](https://help.autodesk.com/cloudhelp/ENG/Build-Issues/files/Work_with_Issues_in_Viewer.html)

Essas referências servem como benchmark de interação, não autorizam copiar interface, marca ou funcionalidades que não estejam suportadas pelos artefatos do SIE.

## 4. Arquitetura proposta da página

```text
SieShell
└── Dependências
    ├── SiePageHero existente/padronizado
    │   └── ação preservada: Nova dependência
    ├── Resumo operacional
    │   ├── Total de dependências
    │   ├── Calculadas
    │   ├── Requerem verificação
    │   └── Desatualizadas (somente se houver regra/dado real)
    ├── Barra de exploração
    │   ├── Busca
    │   ├── Filtros
    │   ├── Chips de filtros ativos
    │   ├── Ordenação
    │   └── Alternância: Grade | Lista técnica
    └── Coleção de dependências
        └── DependencyCard (um por dependência)
            ├── Cabeçalho decisório
            ├── Resumo técnico em grupos
            ├── Rastreabilidade
            └── Ações preservadas
```

### Resumo operacional

Exibir métricas somente quando derivadas de dados já disponíveis. O mínimo seguro é `total` e `calculadas`; `requerem verificação` deve ser derivado exclusivamente dos indicadores existentes. A métrica `desatualizadas` só pode existir depois que produto/engenharia definirem regra, fonte de data e limiar de desatualização.

Cada métrica deve ser acionável apenas se já houver filtro correspondente implementado; caso contrário, deve ser informativa e não se apresentar como controle.

### Barra de exploração

- Manter a busca atual.
- Evoluir `Filtros` para filtros combináveis por categoria, estado de cálculo, necessidade de verificação, presença de carga adicional e data de atualização, desde que os dados existam.
- Exibir filtros aplicados como chips removíveis e oferecer `Limpar filtros`.
- Introduzir ordenação por nome, categoria, última atualização e pendências; opções que dependam de uma regra de criticidade devem ser habilitadas somente quando a regra estiver formalizada.
- Manter a grade como modo padrão. A lista técnica é complementar para comparação de grande volume, não substitui os cards.

## 5. Especificação do `DependencyCard`

### Wireframe conceitual

```text
┌ Dormitório                                      [estado contextual] ┐
│ CAT-A · 6,00 × 4,00 m · dep-… · v4                 Calculada         │
│                                                                    │
│ [ Iluminação ]       [ Tomadas ]          [ Cargas adicionais ]   │
│ 5 pontos · 340 VA    4 tomadas · 300 VA   Sem cargas              │
│ requer verificação   requer verificação                         │
│                                                                    │
│ Atualizado em 05/07/2026, 01:05                                  │
│ [Detalhe] [Calcular] [Historico] [Duplicar]                 [•••] │
└──────────────────────────────────────────────────────────────────┘
```

O wireframe ilustra hierarquia, não altera os dados exibidos nem redefine textos funcionais existentes.

### Cabeçalho decisório

- Nome da dependência como título semântico (`h2` no contexto da coleção).
- Categoria, dimensões, ID e versão em linha de metadados compacta; usar fonte monoespaçada apenas para identificadores e valores técnicos.
- Manter `Calculada` como estado de cálculo existente.
- Exibir um estado contextual adicional apenas quando derivável: por exemplo, `Requer verificação` se houver itens já marcados como `VERIFICAR`. Não inventar `Bloqueada`, `Crítica` ou `Desatualizada` sem regra de domínio.
- Estado deve combinar texto, ícone e cor; cor nunca é a única portadora de significado.

### Resumo técnico comparável

Organizar dados em três grupos visuais equivalentes:

| Grupo | Conteúdo preservado | Regra de apresentação |
|---|---|---|
| Iluminação | pontos, VA, verificação e automático | Valor principal em destaque; unidade junto ao valor; indicador de verificação abaixo. |
| Tomadas | quantidade, VA, verificação e automático | Mesmo padrão de Iluminação para comparação lateral. |
| Cargas adicionais | existência, resumo e observações atuais | Tornar a ausência explícita, sem criar urgência artificial. |

Em telas estreitas, os grupos devem empilhar mantendo a mesma ordem e sem ocultar valores técnicos.

### Rastreabilidade

- Manter data e hora de atualização com rótulo claro.
- Não inferir validade, autoria ou histórico a partir da data apresentada.
- O acesso ao histórico deve continuar exclusivamente pela ação `Historico` existente.

### Ações — contrato de preservação

| Ação | Contrato obrigatório | Tratamento visual proposto |
|---|---|---|
| `Detalhe` | Mesmo rótulo, conteúdo, destino e permissões | Ação primária persistente no rodapé. |
| `Calcular` | Mesmo rótulo, conteúdo, destino e regras de cálculo | Recebe ênfase visual contextual quando o card já indicar necessidade real de revisão; nunca tem comportamento novo. |
| `Historico` | Mesmo rótulo, conteúdo, destino e permissões | Permanece visível no rodapé, como ação secundária. |
| `Duplicar` | Mesmo rótulo, conteúdo, destino e permissões | Permanece visível no rodapé, como ação secundária. |

O menu `•••` não pode ocultar nenhuma das quatro ações acima. Pode conter somente ações adicionais já existentes.

## 6. Design system e acessibilidade

Aplicar Atomic Design para evitar uma solução isolada:

| Nível | Elementos a especificar |
|---|---|
| Átomos | `StatusBadge`, `VerificationIndicator`, `TechnicalValue`, botão de ação, ícone, tooltip e chip de filtro. |
| Moléculas | `TechnicalMetricGroup`, `DependencyMetadata`, `DependencyActionBar`, `ActiveFilterChip`. |
| Organismos | `DependencyCard`, `DependencySummary`, `DependencyExplorerToolbar`, `DependencyTechnicalList`. |
| Template | Página de Dependências com hero, resumo, exploração e coleção. |

Requisitos mínimos:

- Consumir tokens semânticos e a tipografia SIE existentes; não introduzir hexadecimais, espaçamentos ou raios hardcoded na rota.
- Contraste WCAG 2.2 AA para texto, bordas, estados e foco.
- Navegação completa por teclado, incluindo filtros, alternância de visualização, menu e quatro ações.
- Foco visível e ordem de tabulação compatível com a leitura do card.
- Tooltips apenas como complemento: estado e valores precisam permanecer compreensíveis sem hover.
- Área de interação adequada para ações em dispositivos de toque, sem sobrepor alvos adjacentes.
- `aria-label` para controles iconográficos; títulos de card e ações precisam de nomes acessíveis inequívocos.

## 7. Estados de interface

| Estado | Tratamento esperado |
|---|---|
| Carregamento | Skeleton por card e por métrica; não bloquear toda a página por uma carga parcial. |
| Sem resultados | Informar que não há dependências para a busca/filtros atuais e oferecer limpar filtros quando aplicável. |
| Sem dependências | Orientar para a ação existente `Nova dependência`, sem inventar fluxo alternativo. |
| Erro de carregamento | Mensagem de erro clara com tentativa de recarregar conforme padrão existente da aplicação. |
| Muitos resultados | Paginação, carregamento progressivo ou virtualização devem seguir a capacidade já existente/validada pela implementação. |

## 8. Responsividade

- **Desktop (≥ 1200px):** grade de duas colunas, grupos técnicos em três colunas internas quando houver largura útil.
- **Tablet (768–1199px):** uma ou duas colunas conforme largura; grupos técnicos podem usar duas colunas e um bloco em linha seguinte.
- **Mobile (< 768px):** uma coluna; metadados quebram de forma legível; grupos técnicos empilhados; barra de ações permanece íntegra, com quebra controlada e sem esconder as quatro ações obrigatórias.

Os breakpoints finais devem seguir os tokens e padrões responsivos já adotados no SIE.

## 9. Fases de implementação

1. **Descoberta técnica:** mapear componentes, rota, contrato de dados, estados reais e testes que hoje atendem Dependências.
2. **Especificação visual:** produzir wireframe de baixa/média fidelidade e matriz de estados com base neste documento; validar que cada novo indicador é derivável de dados reais.
3. **Sistema de componentes:** definir ou reaproveitar átomos, moléculas e organismos com tokens semânticos.
4. **Implementação incremental:** construir o novo card em paralelo ao contrato atual, migrar a grade e depois a barra de exploração/lista técnica quando suportada.
5. **Validação:** executar testes funcionais e de acessibilidade; validar tarefas de localizar pendências, comparar ambientes e acessar as quatro ações preservadas.

## 10. Critérios de aceite

- [ ] Nenhuma informação técnica exibida no card atual foi removida sem decisão explícita de produto.
- [ ] `Detalhe`, `Calcular`, `Historico` e `Duplicar` mantêm rótulo, conteúdo, comportamento, rota e permissões.
- [ ] As quatro ações permanecem visíveis em todos os breakpoints e não são movidas para o menu contextual.
- [ ] Nome, estado, resumo de iluminação, resumo de tomadas e cargas adicionais podem ser identificados sem abrir o detalhe.
- [ ] Itens com `VERIFICAR` existentes são perceptíveis no card e podem ser localizados por filtro, se esse filtro for implementado.
- [ ] Busca, filtros e ordenação não ocultam resultados nem alteram dados de domínio.
- [ ] Não há novo estado de negócio sem fonte de dados e regra formalizada.
- [ ] Os cards, filtros e ações são operáveis por teclado e atendem WCAG AA.
- [ ] A página funciona em desktop, tablet e mobile sem perda de dados ou ações.
- [ ] A implementação possui story associada, checklist e file list atualizados antes da conclusão.
- [ ] `npm run lint`, `npm run typecheck` e `npm test` passam antes da entrega de código.

## 11. Fora de escopo

- Alterar cálculo elétrico, validações normativas, resultados, APIs, persistência ou permissões.
- Mudar os conteúdos, destinos ou regras das ações `Detalhe`, `Calcular`, `Historico` e `Duplicar`.
- Criar novos estados de domínio ou métricas sem contrato de dados.
- Implementar mapa, agrupamento por pavimento/setor/circuito ou filtros salvos sem que os respectivos relacionamentos e persistência existam e sejam aprovados.

## 12. Próximo passo recomendado

O `aiox-ux-design-expert` deve usar este documento como briefing e executar `*wireframe` para fechar a hierarquia e os estados visuais. Antes de código, `aiox-sm` ou `aiox-po` deve criar/refinar a story de implementação, em conformidade com a Constitution do projeto.
