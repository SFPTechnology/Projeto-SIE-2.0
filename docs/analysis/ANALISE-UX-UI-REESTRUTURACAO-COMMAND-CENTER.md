# Análise UX/UI e proposta de reestruturação — SIE Command Center

**Autor:** Atlas (`@analyst`)  
**Data:** 2026-08-02  
**Status:** recomendação de discovery; não constitui decisão arquitetural nem autorização de implementação  
**Escopo:** utilidade da seção, conteúdo necessário, diagnóstico da implementação atual e proposta de reorganização baseada em evidência interna e referências oficiais de software técnico/enterprise  

---

## 1. Resposta executiva

O **Command Center deve ser a visão consolidada e orientada a exceções de um projeto elétrico**. Sua utilidade não é substituir os módulos de cálculo, repetir todas as suas telas ou decidir pelo projetista. Ele deve permitir que o usuário responda rapidamente a cinco perguntas:

1. **Em qual projeto e etapa estou?**
2. **O projeto está apto a avançar?**
3. **O que está pendente, inconsistente ou acima do limite?**
4. **Qual item exige atenção primeiro e por quê?**
5. **Para qual módulo devo navegar para resolver a pendência?**

Portanto, o Command Center é principalmente uma superfície de **observabilidade, orientação e navegação contextual**. Os cálculos, edições, simulações e confirmações devem continuar nas telas especializadas, onde existem contexto, validações e espaço adequados.

### Conclusão principal

A versão atual possui bons fundamentos visuais e dados reais, mas combina três produtos em uma mesma página:

- um dashboard executivo;
- um workspace de inspeção de circuitos;
- uma sequência completa de cálculo, decisão e documentação.

Essa mistura aumenta a rolagem, repete informação, enfraquece a hierarquia e dificulta identificar a próxima ação. A reestruturação recomendada é:

> **Command Center = visão geral curta, orientada a risco e prontidão; módulos especializados = trabalho técnico detalhado.**

O layout recomendado mantém um único shell global, apresenta primeiro pendências acionáveis e resumo técnico, limita a visão de circuitos aos itens críticos, usa inspetor contextual sob demanda e substitui o unifilar completo por uma prévia navegável.

---

## 2. Base documental e evidência analisada

### 2.1 Artefatos internos

- `.aiox-core/constitution.md` — especialmente o princípio `CLI First → Observability → UI` e a regra de que dashboards observam, mas não controlam ou decidem;
- `docs/analysis/GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md` — mapeamento mock → dado real;
- `docs/prd/PRD-SIE-COMMAND-CENTER-implantacao-dados-reais.md` — requisitos de integração;
- `docs/architecture/DECISION-SIE-DS-08-integracao-dados-reais.md` — decisão da rota contextualizada por projeto;
- `docs/architecture/SIE-COMMAND-CENTER-PATTERN-LIBRARY.md` — inventário implementado;
- `outputs/design-system/sie-command-center/docs/experience-architecture.md` — arquitetura de experiência original;
- `outputs/design-system/sie-command-center/research/benchmark.md` — benchmark anterior;
- protótipos desktop/mobile em `outputs/design-system/sie-command-center/prototype/`;
- implementação atual em `sistema-de-instala-es-el-tricas-sie-main/src/components/command-center/` e na rota `src/routes/projetos.$projetoId_.command-center.tsx`.

### 2.2 Limites da análise

- Não foi realizada pesquisa direta com usuários finais nesta rodada.
- A persona primária ainda não está validada entre projetista, operador assistido e responsável técnico.
- Recomendações que dependem de novos eventos, métricas ou endpoints são marcadas como hipótese/futuro; não são apresentadas como requisito existente.
- Não se propõe motor de cálculo, regra normativa ou dado de domínio novo.

---

## 3. Utilidade correta no sistema

### 3.1 Função primária

O Command Center deve funcionar como **ponto de entrada do projeto ativo** e como **radar de prontidão técnica**. Ele agrega sinais já produzidos pelos módulos e conduz o usuário ao lugar correto para agir.

| Responsabilidade | O que significa no SIE |
|---|---|
| Situational awareness | Mostrar estado do projeto, etapa atual, pendências e severidades |
| Triagem | Ordenar exceções por impacto técnico, sem obrigar o usuário a abrir módulo por módulo |
| Rastreabilidade resumida | Explicar a origem de um alerta e indicar o cálculo/módulo relacionado |
| Navegação contextual | Levar o usuário ao circuito e à tela especializada já filtrados no contexto correto |
| Monitoramento | Informar atualização, carregamento, erro, indisponibilidade e fonte dos dados |
| Continuidade | Indicar o próximo passo possível, sem fingir um percentual de progresso inexistente |

### 3.2 O que ele não deve ser

- Uma página que reproduz integralmente Circuitos, Queda de tensão e Unifilar.
- Um formulário extenso de parâmetros.
- Um local para aplicar cenários ou alterar resultados técnicos.
- Uma vitrine com dados demonstrativos misturados a dados reais.
- Uma segunda navegação completa aninhada dentro do shell principal.
- Um “score” genérico de saúde sem regra de domínio verificável.

### 3.3 Alinhamento constitucional

A Constitution define dashboards como observadores e não como controladores. A implementação atual contém `DecisionPanel`, que chama a mutação de aplicação de cenário de queda de tensão. Essa ação altera dado técnico e, portanto, ultrapassa a finalidade constitucional de observabilidade do Command Center.

**Recomendação P0:** manter no Command Center apenas a síntese do problema, as alternativas já calculadas quando apropriado e um link **“Abrir simulação em Queda de tensão”**. A simulação aplicável, justificativa e confirmação permanecem no módulo especializado.

Isso também reduz o risco de uma decisão ser tomada fora do contexto integral do cálculo.

---

## 4. O que a seção deve apresentar

### 4.1 Informação obrigatória no primeiro viewport

O primeiro viewport precisa responder “estado, risco e próxima ação”, nesta ordem:

1. **Contexto do projeto**
   - nome do projeto;
   - identificação do projeto;
   - etapa inferida, explicitamente rotulada como inferência quando não houver estado persistido;
   - momento da última atualização disponível;
   - estado de carregamento/sincronização real, ou nenhum indicador se esse dado não existir.

2. **Resumo técnico mínimo**
   - total de circuitos;
   - quantidade `OK`, `ACIMA` e `PENDENTE`;
   - pior queda de tensão, circuito associado e limite usado;
   - demanda calculada em kVA e origem normativa/distribuidora;
   - ausência de dado apresentada como pendência acionável, nunca como zero.

3. **Pendências prioritárias**
   - itens acima do limite;
   - circuitos sem comprimento;
   - módulos sem configuração necessária;
   - motivo, impacto e próxima ação;
   - link direto ao módulo/item de resolução.

4. **Jornada do projeto**
   - Levantamento;
   - Entrada;
   - Dimensionamento;
   - Documentação;
   - estado de cada etapa e critério que sustentou o estado;
   - navegação para a etapa selecionada.

### 4.2 Informação de segundo nível

- Lista curta de circuitos críticos, limitada inicialmente aos itens `ACIMA` e `PENDENTE`.
- Filtros por estado e ordenação por severidade/maior queda.
- Inspetor contextual do circuito selecionado, aberto sob demanda.
- Rastreabilidade real disponível: corrente, seção, comprimento, queda, limite e origem do cálculo.
- Miniatura/visão resumida do unifilar com ação “Abrir diagrama completo”.

### 4.3 Informação que deve sair da visão geral

- Painel completo de parâmetros de queda de tensão;
- lista completa de resultados de todos os circuitos;
- comparação e aplicação de cenários;
- textarea de justificativa e confirmação;
- workspace completo do unifilar;
- comandos demonstrativos ou botões sem handler real;
- rótulos como “Estado demonstrativo”, “Projetista (ilustrativo)” e “Conceito v1 · isolado” numa rota de dados reais.

Esses elementos podem existir nos módulos especializados, mas não devem competir com a triagem do dashboard.

---

## 5. Diagnóstico da implementação atual

### 5.1 Pontos fortes

- A rota é contextualizada por `$projetoId` e consulta dados reais.
- Métricas usam resumo real de queda de tensão e demanda.
- O estado dos circuitos respeita o triestado real `OK/ACIMA/PENDENTE`.
- A seleção da tabela alimenta parâmetros, inspetor e decisão.
- Há suporte a densidade compacta/confortável e a teclado na paleta.
- A navegação lateral reflete o ciclo do projeto.
- Estados vazios básicos foram previstos em vários componentes.
- A linguagem de resultado inclui motivo e próxima ação quando disponíveis.

### 5.2 Achados críticos

| Prioridade | Achado | Evidência | Consequência UX/UI |
|---|---|---|---|
| P0 | Dashboard executa mutação técnica | `DecisionPanel.tsx` usa `useMutation` e aplica cenário | Conflito com a Constitution e risco de decisão fora do módulo de origem |
| P0 | Dois shells completos estão aninhados | `SieShell` envolve `EngineeringShell` na rota, e ambos têm navegação/header | Duplicação de chrome, perda de espaço útil e modelo mental ambíguo |
| P0 | Elementos ilustrativos permanecem na rota real | “Estado demonstrativo”, autor ilustrativo, footer “Conceito v1 · isolado” e comandos ilustrativos | Reduz confiança e torna incerto o que é dado real |
| P1 | Overview empilha tarefas profundas | sequência atual: métricas → jornada → tabela/inspetor → parâmetros → resultados → decisão → unifilar | Página muito longa; prioridade se perde; alto custo de varredura |
| P1 | Unifilar completo é duplicado | `UnifilarWorkspace` é renderizado no final e já possui rota própria | Duas fontes visuais e excesso de peso/carga na visão geral |
| P1 | “Circuitos críticos” pode mostrar todos os circuitos | `EngineeringPanel` recebe todo o lote montado | Título e conteúdo podem divergir; itens conformes diluem exceções |
| P1 | Inspetor vazio ocupa largura | painel é persistente mesmo sem seleção | Espaço desperdiçado e redução da área da tabela |
| P1 | Rastreabilidade ainda é genérica | `rastreabilidadeGenerica` é array estático | A interface afirma rastreabilidade sem mostrar a cadeia real |
| P1 | Botões do inspetor não possuem handlers | “Abrir cálculo” e “Simular ajuste” são botões sem ação | Falsa affordance e quebra de confiança |
| P1 | Paleta não navega de fato | `CommandPalette` devolve IDs; callback apenas muda estado local; “Validar projeto” é demonstrativo | Atalho parece funcional, mas não conclui a intenção |
| P1 | Estado ativo da navegação é local | `itemAtivo` inicia sempre em `overview` | Não é derivado da rota; risco de indicador ativo incorreto |
| P1 | Carregamento é agregado e parcial | texto único depende de cinco queries e exclui queries do unifilar | Um dado lento bloqueia o painel; falhas tardias podem parecer loading infinito |
| P2 | Jornada usa heurística frágil | levantamento deriva de “há circuito”; documentação vira ativa quando dimensionamento está completo | O usuário não vê a base do estado e pode interpretá-lo como workflow formal |
| P2 | Resultado selecionado e resultado global competem | parâmetros/decisão usam um circuito; `ResultSummary` lista todos | Mudança de escopo implícita e carga cognitiva |
| P2 | Diagrama conceitual e unifilar real coexistem | modo “Diagrama” do painel + workspace unifilar | Pode haver duas representações do mesmo sistema com fidelidades diferentes |

### 5.3 Problema estrutural: overview versus workspace

O protótipo inicial já colocava métricas, jornada, tabela, diagrama e inspetor na mesma superfície. A integração real acrescentou parâmetros, todos os resultados, decisão e unifilar completo na sequência vertical. O resultado não é apenas “mais conteúdo”; é uma troca de tipo de produto durante a rolagem:

```text
Dashboard de situação
    ↓
Lista + inspetor
    ↓
Painel de parâmetros
    ↓
Relatório de resultados
    ↓
Fluxo decisório com mutação
    ↓
Editor/visualizador unifilar completo
```

Cada bloco é defensável isoladamente, mas a composição reduz foco e cria múltiplas ações primárias concorrentes.

### 5.4 Problema de confiança

Em software técnico, “parece real” não é suficiente. Qualquer texto demonstrativo, rastreabilidade genérica ou botão inoperante ao lado de resultados normativos pode contaminar a percepção de confiabilidade do conjunto. O sistema deve diferenciar claramente:

- dado medido/calculado;
- estado inferido;
- dado indisponível;
- exemplo ou preview;
- ação real;
- navegação.

Na rota de produção, exemplos e placeholders de conceito devem ser removidos, não apenas estilizados de forma discreta.

---

## 6. Benchmark de referências oficiais

### 6.1 ETAP — diagrama como superfície técnica especializada

O ETAP trata o diagrama unifilar como interface para modelar, visualizar e analisar a rede, ligado a uma camada comum de dados. Também usa visualização hierárquica, resultados, propriedades e estudos “what-if” no contexto do diagrama. Isso reforça que o unifilar completo é uma **superfície de trabalho própria**, não um bloco de rodapé do dashboard.

**Aplicação no SIE:** o Command Center deve mostrar uma miniatura/status do unifilar e navegar ao workspace completo; cálculos e estudos permanecem na tela técnica.  
Fonte: [ETAP — Intelligent Electrical Single-Line Diagram](https://etap.com/solutions/intelligent-single-line-diagram).

### 6.2 SOLIDWORKS — árvore, seleção e propriedades sincronizadas

O FeatureManager mantém árvore e área gráfica dinamicamente ligadas; a seleção pode nascer em qualquer painel, e a árvore expõe relações, erros, warnings e filtros.

**Aplicação no SIE:** seleção de circuito, linha, prévia e inspetor devem compartilhar o mesmo objeto e estado; o usuário deve chegar à origem da exceção sem procurar novamente.  
Fonte: [SOLIDWORKS — FeatureManager Design Tree Overview](https://help.solidworks.com/2024/english/Solidworks/sldworks/c_featuremanager_design_tree_overview.htm).

### 6.3 Autodesk Platform Services — modelo, objeto e propriedades

O Viewer oficial expõe árvore de objetos, seleção por identificador e consulta de propriedades. O padrão recorrente é estrutura → área principal → propriedades do objeto selecionado.

**Aplicação no SIE:** inspetor deve ser contextual e sincronizado, não um painel genérico permanente; seu conteúdo precisa derivar do circuito selecionado.  
Fonte: [Autodesk APS Viewer3D](https://aps.autodesk.com/en/docs/viewer/v6/reference/Viewing/Viewer3D/).

### 6.4 EPLAN — navegadores e filtros reutilizáveis

Os navegadores de dados de projeto permitem filtrar listas/árvores, salvar esquemas e usar entrada rápida para alterar critérios.

**Aplicação no SIE:** circuitos críticos precisam de filtro simples por estado e ordenação por severidade; filtros salvos são uma evolução possível, condicionada à validação de frequência de uso.  
Fonte: [EPLAN — Filter](https://eplan.help/en-us/Infoportal/Content/Plattform/2.9/Content/htm/modaldialogsdb_k_filter.htm).

### 6.5 Siemens Industrial Experience — um frame, panes e adaptação

O application frame organiza header, menu e conteúdo; a própria documentação alerta para ocultar o header interno quando a aplicação já está hospedada em um framework com header. Os panes agrupam informações contextuais e reduzem o conteúdo permanente da área principal.

**Aplicação no SIE:** eliminar o shell duplicado; usar o `SieShell` como frame único; abrir o inspetor como pane/drawer sob demanda e em tela cheia no mobile.  
Fontes: [Siemens IX — Basic Navigation](https://ix.siemens.io/version-2.7/docs/controls/application-frame/basic-navigation/) e [Siemens IX — Panes](https://ix.siemens.io/docs/components/panes/guide).

### 6.6 SAP Fiori — overview é entrada, não aplicação inteira

No Overview Page, cards são visões de entrada dos dados mais pertinentes. Cada card deve acrescentar valor, evitar repetição e conduzir à aplicação detalhada; cards não têm campos editáveis. A recomendação também é limitar listas e levar o usuário ao conjunto completo.

**Aplicação no SIE:** parâmetros editáveis, justificativa, aplicação de cenário e unifilar completo devem sair do overview; cards e listas curtas navegam ao módulo correspondente.  
Fontes: [SAP Fiori — Overview Page Cards](https://experience.sap.com/fiori-design-web/overview-page-card/) e [SAP Fiori — Overview Page List Cards](https://experience.sap.com/fiori-design-web/overview-page-list-cards/).

### 6.7 IBM Carbon — tabela densa com descoberta progressiva

Carbon recomenda toolbar para busca, filtros, configuração e ações globais; ordenação nos cabeçalhos; expansão para informação suplementar; e página/painel dedicado quando o detalhe ficar apertado. Também recomenda skeletons em cargas perceptíveis.

**Aplicação no SIE:** a tabela crítica ganha busca/filtro/ordenação, seleção inequívoca e inspector/detalhe externo; o carregamento deixa de bloquear toda a página com uma frase única.  
Fonte: [Carbon Design System — Data Table Usage](https://carbondesignsystem.com/components/data-table/usage/).

### 6.8 WCAG 2.2 — acessibilidade operacional

Foco não pode ficar oculto por conteúdo do autor, e alvos devem atingir pelo menos 24 × 24 CSS px, salvo exceções definidas no padrão.

**Aplicação no SIE:** drawer/inspetor não pode encobrir o elemento focado; navegação, tabela e controles compactos preservam foco visível, ordem lógica e alvos mínimos.  
Fonte: [W3C — WCAG 2.2](https://www.w3.org/TR/WCAG22/).

### 6.9 Síntese do benchmark

Os padrões convergem em seis princípios:

1. **Uma fonte de contexto e um shell por aplicação.**
2. **Overview resume e encaminha; workspace executa.**
3. **Exceções e estado precisam ser mais visíveis que volume bruto.**
4. **Seleção, visualização e propriedades permanecem sincronizadas.**
5. **Detalhes aparecem progressivamente em pane, expansão ou rota dedicada.**
6. **Dados técnicos exibem origem, unidade, precisão, estado e atualidade.**

---

## 7. Arquitetura de informação recomendada

### 7.1 Taxonomia

Renomear o item de navegação para **“Visão geral”** é mais claro que “Command Center” para a maioria dos usuários, mantendo “SIE Command Center” como nome interno do padrão/design system. A mudança de rótulo deve ser validada por PO/UX antes de implementação.

```text
Projeto ativo
├── Visão geral                ← Command Center reestruturado
│   ├── Resumo e prontidão
│   ├── Pendências prioritárias
│   ├── Jornada do projeto
│   ├── Circuitos críticos
│   └── Prévia do unifilar
├── Ambientes e cargas
├── Padrão de entrada
├── Circuitos
├── Correntes
├── Dimensionamento de condutores
├── Queda de tensão            ← parâmetros, resultados, simulação e aplicação
└── Diagrama unifilar          ← workspace completo
```

### 7.2 Modelo de conteúdo

| Bloco | Conteúdo | Interação permitida no Command Center | Destino aprofundado |
|---|---|---|---|
| Cabeçalho contextual | Projeto, etapa, atualização, status | trocar projeto; navegar para próximo módulo | Lista de projetos/módulo |
| Resumo técnico | Circuitos, pior queda, demanda, pendentes | abrir visão filtrada | Módulo correspondente |
| Pendências | severidade, item, causa, impacto, próximo passo | selecionar/abrir | Circuitos ou Queda de tensão |
| Jornada | quatro etapas e base do estado | navegar à etapa | Módulos da etapa |
| Circuitos críticos | top N `ACIMA`/`PENDENTE` | filtrar, ordenar, inspecionar, abrir | Queda de tensão/circuito |
| Inspetor | propriedades reais do selecionado | fechar; abrir cálculo | Módulo técnico |
| Unifilar | status/miniatura e cobertura | abrir diagrama | Unifilar |

### 7.3 Wireframe desktop recomendado

```text
┌──────────────────────────── SieShell único ────────────────────────────────┐
│ Breadcrumb                     Projeto / atualização / etapa               │
├────────────────────────────────────────────────────────────────────────────┤
│ Visão geral do projeto                              [Abrir próxima etapa]  │
│ Estado resumido + explicação do critério                                  │
├───────────────┬───────────────┬───────────────┬────────────────────────────┤
│ Circuitos     │ Pior ΔV       │ Demanda       │ Pendências                 │
│ total/estado  │ valor/limite  │ kVA/origem    │ ACIMA + sem comprimento    │
├───────────────────────────────────────────────┬────────────────────────────┤
│ Pendências prioritárias / Circuitos críticos  │ Jornada do projeto         │
│ busca · filtro · ordenação                    │ etapa + motivo + destino   │
│ top 5, seleção sincronizada                   │                            │
├───────────────────────────────────────────────┼────────────────────────────┤
│ Prévia do unifilar [Abrir diagrama completo]  │ Próxima ação recomendada   │
└───────────────────────────────────────────────┴────────────────────────────┘
                                      ┌─────────────────────────────────────┐
                                      │ Inspetor contextual (sob demanda)  │
                                      │ propriedades + origem + abrir tela │
                                      └─────────────────────────────────────┘
```

### 7.4 Hierarquia no mobile

No mobile, a ordem deve refletir urgência, não o layout desktop simplesmente empilhado:

1. contexto do projeto;
2. pendências prioritárias;
3. próxima ação;
4. resumo técnico em carrossel não obrigatório ou cards empilhados;
5. jornada vertical;
6. circuitos críticos;
7. prévia do unifilar.

O inspetor abre como tela/drawer completo. Tabelas devem reduzir colunas visíveis e oferecer detalhe da linha, sem depender de rolagem horizontal para a informação crítica.

---

## 8. Decisão por componente atual

| Componente/elemento | Decisão | Reestruturação proposta |
|---|---|---|
| `SieShell` | **Manter** | Torná-lo o único shell global |
| `EngineeringShell` | **Desmontar como shell aninhado** | Reaproveitar apenas padrões úteis; remover nav/header duplicados |
| `MetricCardGrid` | **Manter e refinar** | Cards clicáveis, severidade, origem e estados independentes |
| `WorkflowStepper` | **Manter e refinar** | Tornar navegável; mostrar critério/explicação da inferência |
| `EngineeringPanel` | **Manter parcialmente** | Mostrar somente top N críticos; adicionar filtro/ordenação/busca |
| modo “Diagrama” conceitual | **Remover da visão geral** | Evitar competição com o unifilar real |
| `ContextInspector` | **Refatorar** | Pane/drawer sob demanda; rastreabilidade real; ações como links de navegação |
| `ParameterPanel` | **Mover** | Permanecer no módulo Queda de tensão |
| `ResultSummary` completo | **Mover/reduzir** | No overview, apenas exceções; conjunto completo no módulo |
| `DecisionPanel` | **Mover obrigatoriamente** | Simulação/aplicação no módulo Queda de tensão |
| `UnifilarPreviewSection` | **Reduzir** | Miniatura/status + link; workspace completo na rota própria |
| `ModuleNavigation` do Command Center | **Eliminar duplicação** | Consolidar taxonomia no `SieSidebar` |
| `CommandPalette` | **Corrigir ou ocultar** | Só exibir comandos que navegam/executam de fato; preferir navegação real |
| seletor de densidade | **Manter** | Preferência global, com rótulo/tooltip claro |
| “Estado demonstrativo” | **Remover** | Substituir por atualização real apenas se o contrato fornecer |
| avatar/autor ilustrativo | **Remover duplicação** | Usar autor real já fornecido pelo shell, se pertinente |
| badge “SIE Command Center” | **Remover** | Redundante com título/rota |

---

## 9. Comportamentos e estados necessários

### 9.1 Carregamento

- Renderizar o shell e cabeçalho imediatamente.
- Usar skeleton por card/bloco, não uma única mensagem que bloqueia toda a página.
- Permitir que métricas já resolvidas apareçam enquanto outros blocos carregam.
- Informar “atualizado em” somente quando houver timestamp real.

### 9.2 Erro parcial

- Falha na demanda não deve ocultar circuitos e queda de tensão.
- Cada bloco deve mostrar: o que falhou, possível motivo, impacto e tentativa de recuperação.
- O unifilar não deve ficar indefinidamente em “Carregando” quando uma query falhar.

### 9.3 Vazio

O estado vazio deve orientar a ação correta:

- sem ambientes/cargas → “Cadastre ambientes e cargas”;
- sem circuitos → “Derive ou revise os circuitos”;
- sem comprimento → “Informe o comprimento no módulo Queda de tensão”;
- sem padrão de entrada → “Configure o padrão de entrada”;
- sem unifilar disponível → “Conclua os dados necessários para gerar o diagrama”.

Os textos finais devem ser validados contra as regras reais de habilitação de cada módulo.

### 9.4 Seleção e inspeção

- Selecionar um circuito destaca o mesmo item em lista/prévia quando ambos estiverem presentes.
- O inspetor mostra somente dado real ou declara explicitamente indisponibilidade.
- “Abrir cálculo” deve navegar com contexto suficiente para reencontrar o circuito.
- Fechar o inspetor devolve foco ao elemento que o abriu.

### 9.5 Severidade

- `ACIMA`: prioridade alta, com causa e limite;
- `PENDENTE`: dado necessário ausente, com instrução objetiva;
- `OK`: informação positiva, visualmente subordinada às exceções;
- cor nunca é o único canal; usar texto e ícone/forma;
- não converter esses estados em “percentual de projeto concluído”.

---

## 10. Recomendações de UI visual

### Densidade e layout

- Manter escala de 4 px e densidades existentes.
- Aumentar a largura útil da tabela, eliminando o inspetor vazio persistente.
- Limitar o overview a aproximadamente 2–3 blocos verticais principais antes do aprofundamento.
- Fixar a hierarquia por contraste e tipografia; evitar novos acentos ou efeitos decorativos.
- Usar números tabulares e manter unidade junto ao valor.

### Cards

- Um card responde a uma pergunta única.
- Título curto, valor, unidade, estado e complemento causal.
- Card inteiro ou cabeçalho navega ao detalhe, com affordance explícita.
- Não repetir o mesmo número em card, jornada e lista sem acrescentar contexto.

### Tabela de circuitos

- Padrão inicial: apenas `ACIMA` e `PENDENTE`.
- Filtros rápidos: “Todos críticos”, “Acima do limite”, “Sem comprimento”.
- Ordenação inicial: severidade → maior ΔV → identificador.
- Colunas prioritárias: circuito/aplicação, estado, ΔV/limite, corrente, seção.
- Em telas estreitas: circuito, estado e ΔV; restante no detalhe.
- Ações de linha visíveis e consistentes com Carbon, evitando transformar toda a linha em controle ambíguo.

### Jornada

- Tratar como navegação e explicação, não como barra de progresso matemática.
- Exibir tooltip/popover “Como este estado foi determinado”.
- Diferenciar `concluído`, `em curso`, `pendente` e `bloqueado` apenas se `bloqueado` tiver regra real.
- Não inferir “Documentação em curso” apenas porque o dimensionamento está completo sem deixar o critério explícito.

---

## 11. Priorização recomendada

### P0 — coerência, governança e confiança

1. Remover a capacidade de aplicar cenário no dashboard; encaminhar ao módulo Queda de tensão.
2. Eliminar o shell aninhado e consolidar tudo no `SieShell`.
3. Remover textos, comandos e ações ilustrativas da rota real.
4. Remover ou conectar de fato os botões sem handler.
5. Não exibir rastreabilidade genérica como se fosse evidência real.

### P1 — foco e produtividade

1. Reorganizar o overview por exceções e próxima ação.
2. Limitar circuitos à lista crítica e oferecer filtros/ordenação.
3. Transformar o inspetor em pane sob demanda.
4. Mover parâmetros, resultados completos e decisão ao módulo especializado.
5. Trocar o unifilar completo por preview/status navegável.
6. Implementar loading/error/empty por bloco.
7. Derivar item ativo da rota e tornar jornada/cards navegáveis.

### P2 — refinamento após pesquisa com usuários

1. Filtros salvos ou views personalizadas.
2. Personalização da ordem dos cards por papel.
3. Atividade recente baseada em eventos de auditoria, caso exista contrato de leitura adequado.
4. Comparação temporal/tendências, somente se houver histórico confiável.
5. Preferências persistentes de densidade e composição.

---

## 12. Plano de validação UX

Antes de consolidar a arquitetura visual, recomenda-se validar as seguintes hipóteses:

| Hipótese | Método | Critério sugerido |
|---|---|---|
| Usuário encontra a principal pendência sem abrir vários módulos | teste moderado com projeto contendo `ACIMA` e `PENDENTE` | identificar corretamente causa e destino em até 30 s |
| Próxima ação é compreendida sem confundir navegação com aplicação | teste de primeiro clique | maioria escolhe o módulo correto |
| Jornada inferida é compreendida | entrevista + think-aloud | usuário explica por que a etapa tem aquele estado |
| Lista crítica é suficiente no overview | comparação com lista completa | menor tempo sem perda de achados relevantes |
| Inspetor sob demanda reduz carga sem ocultar contexto | teste desktop e tablet | usuário alterna itens e retorna o foco sem erro |
| “Visão geral” é rótulo mais claro que “Command Center” | teste de árvore/rotulagem | melhor associação com resumo do projeto |

Perfis mínimos para a pesquisa: projetista que executa cálculos, responsável técnico que revisa e usuário menos frequente que acompanha o processo. A quantidade de participantes deve ser definida pelo plano de pesquisa, não assumida como requisito deste documento.

---

## 13. Indicadores de sucesso

Os indicadores abaixo medem UX; não criam regra normativa de engenharia:

- tempo para identificar a pendência mais crítica;
- taxa de primeiro clique correto para resolver uma pendência;
- quantidade de navegações necessárias até o módulo correto;
- taxa de ações em controles sem efeito — alvo zero;
- taxa de erro ao distinguir `ACIMA`, `PENDENTE` e `OK`;
- percentual de blocos que exibem origem/atualidade quando esses dados existem;
- sucesso de navegação por teclado e retorno de foco do inspetor;
- tempo de conteúdo útil do primeiro viewport;
- percepção de confiança nos dados, medida em pesquisa qualitativa.

Não usar “percentual de fluxo concluído” como KPI até existir uma regra de domínio formal, rastreável e aprovada.

---

## 14. Riscos e decisões pendentes

| Tema | Situação | Responsável adequado |
|---|---|---|
| Command Center observacional versus transacional | Constitution favorece observação; implementação hoje altera cenário | `@architect` + `@po` |
| Rótulo “Visão geral” | recomendação de UX ainda não ratificada | `@po` + UX |
| Regra da jornada | heurística implementada, não workflow persistido | `@po` + domínio |
| Rastreabilidade por circuito | conteúdo atual é genérico | `@architect` + `@dev` em story própria |
| Deep-link para circuito | intenção clara, contrato de rota/estado precisa ser definido | `@architect` |
| Timestamp/sincronização | não confirmado em todos os contratos atuais | `@architect` + dados |
| Atividade recente | tabela/evento existe, consulta adequada não foi validada nesta análise | dados + produto |
| Personalização por papel | depende de persona e frequência de uso | UX research + `@po` |

---

## 15. Recomendação final

O SIE já possui os elementos certos, porém no nível errado de composição. A maior melhoria não virá de acrescentar novos widgets; virá de **reduzir a visão geral ao que ajuda a perceber, priorizar e navegar**.

A decisão recomendada é:

1. adotar um único shell;
2. posicionar pendências e próxima ação acima do conteúdo exploratório;
3. restringir o Command Center à observabilidade e navegação;
4. mover edição, simulação, aplicação e workspace completo para os módulos de origem;
5. sincronizar seleção e propriedades com dado real;
6. eliminar qualquer aparência de dado real para conteúdo demonstrativo;
7. validar a nova organização com usuários antes de personalização ou métricas novas.

Essa estrutura preserva o investimento já realizado em tokens e componentes, reduz risco constitucional, aproxima o produto dos padrões de software técnico e torna a interface mais rápida de interpretar sem inventar capacidade de domínio.

---

— Atlas, investigando a verdade 🔎
