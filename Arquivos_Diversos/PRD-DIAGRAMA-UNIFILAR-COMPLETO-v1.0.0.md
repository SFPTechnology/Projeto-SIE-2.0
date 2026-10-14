# PRD — Diagrama Unifilar Completo

**Versão:** 1.0.0
**Data:** 2026-07-10
**Autor:** Consultoria técnica independente
**Sistema:** SIE — Sistema de Instalações Elétricas
**Módulo:** `sie_unifilar_export`
**Status:** Rascunho para revisão do Product Owner

---

## Índice

1. Visão e declaração do problema
2. Usuários e personas
3. Escopo
4. Relação com a seção existente
5. Arquitetura do pipeline
6. Contrato de entrada — UnifilarGraph
7. Catálogo de simbologia IEC 60617
8. Motor de layout Python
9. Renderizador SVG técnico
10. Renderizador DXF CAD
11. Renderizador PDF vetorial
12. Carimbo e legenda profissional
13. CLI de exportação
14. Endpoint FastAPI
15. Integração com o frontend
16. Conformidade normativa
17. Requisitos não-funcionais
18. Estratégia de testes
19. Plano de entrega faseado
20. Critérios de aceitação por fase
21. Registro de riscos
22. Dependências técnicas e restrições
23. Glossário

---

## 1. Visão e declaração do problema

### 1.1 Problema

O SIE possui uma seção "Diagrama unifilar interativo do projeto" que funciona como visualização operacional no frontend — canvas SVG navegável com inspector lateral, busca, filtros e agrupamento. Essa seção atende à necessidade de inspeção e rastreabilidade dentro do produto web, mas não produz as saídas técnicas que o engenheiro eletricista precisa para aprovar, imprimir, arquivar e submeter o projeto a concessionárias e órgãos de fiscalização.

Especificamente, o produto não gera:

- Diagrama unifilar em formato CAD (DXF) para integração com AutoCAD, BricsCAD ou outros softwares de engenharia utilizados no mercado brasileiro.
- Diagrama unifilar em PDF vetorial com carimbo profissional, legenda ABNT, e qualidade de impressão em escala (A3, A4, A1).
- Diagrama unifilar em SVG técnico com simbologia IEC 60617 normalizada, rastreável e editável em editores vetoriais (Inkscape, Illustrator).

Os botões de exportação SVG, PDF e DXF estão presentes na interface (`UnifilarExportBar`) mas desabilitados, com a mensagem informando que dependem de uma camada Python opcional.

### 1.2 Visão

Construir a seção **"Diagrama Unifilar Completo"** como um pipeline Python que consome o contrato canônico `UnifilarGraph.json` já produzido pela seção existente e gera três saídas vetoriais de qualidade profissional (SVG, DXF, PDF), com simbologia IEC 60617, layout determinístico, carimbo ABNT, e rastreabilidade completa de cada elemento gráfico ao circuito de origem.

O pipeline é uma camada de projeção — não recalcula regras normativas, não inventa valores, e não depende do frontend para operar.

### 1.3 Proposta de valor

- O engenheiro exporta o diagrama unifilar diretamente do SIE em formato profissional pronto para aprovação, eliminando a necessidade de redesenhar manualmente em AutoCAD.
- O diagrama DXF é diferencial competitivo no mercado brasileiro de SaaS para projetos elétricos, onde a maioria dos concorrentes oferece apenas PDF rasterizado ou PNG.
- O pipeline é desacoplado do frontend, podendo ser executado via CLI para automação em lote ou integrado via endpoint FastAPI para exportação sob demanda.

---

## 2. Usuários e personas

### 2.1 Engenheiro eletricista projetista (persona primária)

Responsável técnico pelo projeto de instalações elétricas. Precisa do diagrama unifilar para compor o projeto executivo que será submetido à concessionária (EDP São Paulo) e à prefeitura. Exige conformidade com ABNT NBR 5410:2004 e simbologia IEC 60617. Trabalha com AutoCAD ou BricsCAD e espera receber um DXF com layers organizadas, blocos editáveis e carimbo profissional.

**Necessidades críticas:**
- DXF com layers separadas para edição seletiva.
- Simbologia normalizada reconhecível por qualquer profissional da área.
- Carimbo com dados do projeto, responsável técnico, e escala.
- Rastreabilidade de cada circuito ao memorial de cálculo.

### 2.2 Técnico em eletrotécnica (persona secundária)

Executa projetos menores (residências, pequenos comércios) sob supervisão de engenheiro. Trabalha com ferramentas mais simples e pode não ter AutoCAD. Precisa de PDF em escala para impressão e SVG para inclusão em relatórios digitais.

**Necessidades críticas:**
- PDF imprimível em A3 com qualidade vetorial.
- SVG visualizável em navegador para envio digital.

### 2.3 Arquiteto (persona terciária)

Inclui o diagrama unifilar no projeto arquitetônico para aprovação integrada. Geralmente recebe o DXF do engenheiro e insere no projeto geral. Não edita o conteúdo elétrico, mas exige que o DXF respeite convenções de layers e escalas compatíveis com o projeto arquitetônico.

**Necessidades críticas:**
- DXF em escala compatível (1:50, 1:75, 1:100).
- Layers com nomenclatura identificável (prefixo `SIE_`).

---

## 3. Escopo

### 3.1 Dentro do escopo

| ID | Funcionalidade |
|---|---|
| E-01 | Pipeline Python que consome `UnifilarGraph.json` e gera SVG técnico |
| E-02 | Pipeline Python que consome `UnifilarGraph.json` e gera DXF R2010 |
| E-03 | Pipeline Python que consome `UnifilarGraph.json` e gera PDF vetorial |
| E-04 | Catálogo de símbolos IEC 60617 para instalações elétricas prediais |
| E-05 | Motor de layout determinístico em Python (linear e clustered) |
| E-06 | Carimbo e legenda profissional ABNT nos três formatos |
| E-07 | CLI `python -m sie_unifilar_export` com opções de formato, papel e escala |
| E-08 | Endpoint FastAPI `POST /api/projetos/{id}/unifilar/exportar` |
| E-09 | Ativação dos botões de exportação no frontend (`UnifilarExportBar`) |
| E-10 | Suíte de testes automatizados (contrato, determinismo, regressão visual) |
| E-11 | Validação estrutural do SVG gerado (XPath + W3C schema) |
| E-12 | Metadados de rastreabilidade em cada elemento gráfico (SVG `data-*`, DXF `ATTRIB`, PDF metadata) |

### 3.2 Fora do escopo

| ID | Exclusão | Justificativa |
|---|---|---|
| X-01 | Recálculo de correntes IB, demanda ou dimensionamento no pipeline | O pipeline é camada de projeção, não motor de cálculo |
| X-02 | Editor gráfico CAD no navegador | Decisão arquitetural existente: o canvas SVG não é editor livre |
| X-03 | Exportação para formatos proprietários (DWG, Revit) | DWG requer licença ODA; Revit é escopo diferente |
| X-04 | Geração de diagrama multifilar | Escopo futuro; o unifilar é a representação normalizada para aprovação |
| X-05 | Integração com plotters de grande formato | A saída PDF/DXF é compatível com plotters, mas o SIE não controla a impressão |
| X-06 | Versão offline/desktop do pipeline | O pipeline Python opera em servidor; uso local é via CLI |
| X-07 | Renderização de geometria de ambientes (plantas baixas) | O diagrama unifilar é esquemático, não planta |

---

## 4. Relação com a seção existente

### 4.1 Seção atual: "Diagrama unifilar interativo do projeto"

A seção existente (`src/components/unifilar/`) permanece inalterada. Ela é a fonte do contrato canônico `UnifilarGraph` que o novo pipeline consome. A relação é unidirecional:

```
Seção existente (frontend)              Nova seção (backend Python)
─────────────────────────               ────────────────────────────
ResultadoTelaCorrente                   
  + DependenciaAgregado                 
       │                                
       ▼                                
  montarUnifilar()                      
       │                                
       ▼                                
  UnifilarGraph (contrato canônico)     
       │                                
       ├─── Canvas SVG interativo       
       │    (renderização frontend)     
       │                                
       └─── JSON exportado ──────────── sie_unifilar_export
                                              │
                                              ├── SVG técnico
                                              ├── DXF CAD
                                              └── PDF vetorial
```

### 4.2 Ponto de integração

O contrato `UnifilarGraph` é o único ponto de integração entre as duas seções. O pipeline Python nunca acessa diretamente o banco de dados, a tela de correntes ou as dependências. Se o contrato canônico mudar de versão (campo `meta.versao`), o pipeline Python deve validar a versão e rejeitar contratos incompatíveis com mensagem explícita.

### 4.3 Independência do Planejador de Circuitos

O Planejador de Circuitos (divisor de circuitos do SIE) alimenta a montagem do `UnifilarGraph` upstream. O pipeline de exportação é agnóstico à origem do grafo — funciona identicamente com dados do adaptador 1:1 provisório ou com dados do Planejador de Circuitos real. A troca do adaptador upstream não exige refatoração do pipeline.

---

## 5. Arquitetura do pipeline

### 5.1 Visão geral

O pipeline é composto por cinco camadas sequenciais, cada uma com responsabilidade única:

```
CAMADA 1 — INGESTÃO
  Leitura do UnifilarGraph.json
  Validação Pydantic v2
  Rejeição de contratos malformados

CAMADA 2 — MODELAGEM
  Construção do DiGraph (NetworkX)
  Indexação de atributos (severidade, fase, grupo EDP, dependência)
  Resolução de grupos

CAMADA 3 — LAYOUT
  Motor de layout determinístico
  Modo linear / modo clustered
  Fallback Graphviz dot para projetos grandes
  Coordenadas absolutas em milímetros

CAMADA 4 — RENDERIZAÇÃO
  4a — SVG técnico (svgwrite + schemdraw)
  4b — DXF CAD (ezdxf)
  4c — PDF vetorial (ReportLab + svglib)

CAMADA 5 — ENTREGA
  Escrita de arquivos
  Relatório de diagnósticos
  Código de saída CLI
```

### 5.2 Princípio de fonte única

As camadas 1–3 são compartilhadas por todos os renderizadores. Os renderizadores 4a/4b/4c consomem a mesma estrutura de layout (coordenadas + simbologia resolvida) e produzem saídas visualmente equivalentes nos três formatos. Se dois formatos divergem visualmente para a mesma entrada, é um bug — não uma característica.

### 5.3 Estrutura de pacote

```
sie_unifilar_export/
├── __main__.py              # CLI entry point (click)
├── cli.py                   # Definição de comandos e opções
├── ingestao/
│   ├── __init__.py
│   ├── contrato.py          # Modelos Pydantic v2 (UnifilarGraph, Node, Edge, Group)
│   └── validacao.py         # Validação de versão, integridade referencial
├── modelagem/
│   ├── __init__.py
│   ├── grafo.py             # Construção NetworkX DiGraph
│   └── agrupamento.py       # Resolução de grupos por critério
├── layout/
│   ├── __init__.py
│   ├── motor.py             # Motor de layout determinístico
│   ├── linear.py            # Algoritmo de layout linear
│   ├── clustered.py         # Algoritmo de layout clustered
│   └── fallback_graphviz.py # Layout via Graphviz dot
├── simbologia/
│   ├── __init__.py
│   ├── catalogo.py          # Registro de símbolos IEC 60617
│   ├── disjuntor.py         # Símbolo: disjuntor termomagnético
│   ├── disjuntor_dr.py      # Símbolo: disjuntor diferencial residual
│   ├── barramento.py        # Símbolo: barramento de fases R/S/T/N/PE
│   ├── condutor.py          # Símbolo: condutor / fiação
│   ├── tomada.py            # Símbolo: tomada de uso geral (TUG) e específico (TUE)
│   ├── iluminacao.py        # Símbolo: ponto de iluminação
│   ├── quadro.py            # Símbolo: quadro de distribuição
│   ├── aterramento.py       # Símbolo: aterramento e equipotencialização
│   └── elementos_base.py   # Classe base para elementos customizados schemdraw
├── renderizadores/
│   ├── __init__.py
│   ├── svg_tecnico.py       # Renderizador SVG (svgwrite)
│   ├── dxf_cad.py           # Renderizador DXF (ezdxf)
│   ├── pdf_vetorial.py      # Renderizador PDF (ReportLab + svglib)
│   └── carimbo.py           # Carimbo e legenda ABNT (compartilhado)
├── diagnosticos/
│   ├── __init__.py
│   └── relatorio.py         # Relatório de diagnósticos pós-exportação
├── config/
│   ├── __init__.py
│   ├── escalas.py           # Escalas normalizadas (1:50, 1:75, 1:100)
│   ├── papeis.py            # Formatos de papel (A4, A3, A2, A1, A0)
│   └── fontes.py            # Fontes técnicas (ISO 3098, Romans)
└── tests/
    ├── __init__.py
    ├── conftest.py           # Fixtures: UnifilarGraph de referência (proj-1)
    ├── test_contrato.py      # Validação de contrato
    ├── test_layout.py        # Determinismo de layout
    ├── test_svg.py           # Estrutura e validade do SVG
    ├── test_dxf.py           # Layers, blocos e integridade DXF
    ├── test_pdf.py           # Metadados e vetorialidade do PDF
    ├── test_simbologia.py    # Conformidade visual dos símbolos
    └── test_regressao.py     # Hash perceptual de saídas renderizadas
```

---

## 6. Contrato de entrada — UnifilarGraph

### 6.1 Versão do contrato

O pipeline aceita contratos com `meta.versao` compatível. A versão inicial é `"1.0.0"`. O pipeline rejeita versões incompatíveis com mensagem:

```
ERRO: Versão do contrato UnifilarGraph incompatível.
  Esperada: 1.x.x
  Recebida: {meta.versao}
  Ação: Atualize o frontend ou o pipeline para versões compatíveis.
```

### 6.2 Modelos Pydantic v2

```python
class UnifilarMeta(BaseModel):
    projetoId: str
    versao: str                         # semver "1.0.0"
    origem: str                         # "adaptador_1_1" | "planejador_circuitos"
    modoDivisao: str                    # "MANUAL" | "AUTOMATICO" | "FALLBACK_AUTOMATICO"
    fallbackMotivo: Optional[str]
    calculadoEm: str                    # ISO 8601
    provisorio: bool

class UnifilarSummary(BaseModel):
    qtdCircuitos: int
    ibMaxA: float
    desequilibrioPct: float
    qtdAlertas: int
    qtdErros: int
    qtdCircuitosManuais: int
    qtdTensoesPendentes: int

class UnifilarNode(BaseModel):
    id: str
    tipoNode: str                       # "BARRAMENTO" | "CIRCUITO"
    nome: str
    tipoCarga: Optional[str]            # "ILU" | "TUG" | "TUE"
    fases: list[str]                    # ["R"] | ["R","S"] | ["R","S","T"]
    potenciaVA: float
    tensaoV: Optional[float]
    tensaoConfirmada: bool
    ibA: float
    requisitoDr: Optional[str]
    grupoEdp: Optional[str]
    severidade: str                     # "INFO" | "ATENCAO" | "ERRO"
    controle: Optional[str]             # "automatico" | "manual" | "indeterminado"
    dependenciaId: Optional[str]
    origem: Optional[str]
    pontos: Optional[int]
    diagnosticos: list[dict]
    pendencias: list[dict]
    rastreio: Optional[dict]
    fonteLinha: Optional[str]
    provisorio: bool
    exportRef: Optional[str]

class UnifilarEdge(BaseModel):
    id: str
    de: str                             # ID do node de origem
    para: str                           # ID do node de destino
    tipo: str                           # "alimentacao"

class UnifilarGroup(BaseModel):
    id: str
    label: str
    nodeIds: list[str]

class UnifilarGraph(BaseModel):
    meta: UnifilarMeta
    summary: UnifilarSummary
    nodes: list[UnifilarNode]
    edges: list[UnifilarEdge]
    groups: list[UnifilarGroup]
```

### 6.3 Validações de integridade referencial

Além da validação de tipos, o pipeline executa validações estruturais:

| ID | Validação | Severidade |
|---|---|---|
| V-01 | Todo `edge.de` e `edge.para` deve referenciar um `node.id` existente | ERRO |
| V-02 | Todo `nodeId` em `groups[].nodeIds` deve referenciar um `node.id` existente | ERRO |
| V-03 | Deve existir exatamente um node com `tipoNode == "BARRAMENTO"` | ERRO |
| V-04 | Todo node de circuito deve ter pelo menos um edge conectando-o ao barramento | ATENÇÃO |
| V-05 | `summary.qtdCircuitos` deve ser igual ao count de nodes com `tipoNode == "CIRCUITO"` | ATENÇÃO |
| V-06 | Se `meta.provisorio == true`, todos os nodes devem ter `provisorio == true` | INFO |
| V-07 | Nenhum `node.ibA` deve ser negativo ou zero para nodes do tipo CIRCUITO | ERRO |
| V-08 | Se `node.tipoCarga == "TUE"` e `node.tensaoV is None`, a severidade deve ser ATENÇÃO ou ERRO | ATENÇÃO |

---

## 7. Catálogo de simbologia IEC 60617

### 7.1 Escopo do catálogo

O catálogo cobre os símbolos necessários para representar um diagrama unifilar de quadro de distribuição residencial e comercial de baixa tensão, conforme IEC 60617 e práticas brasileiras.

### 7.2 Símbolos obrigatórios (Fase 1)

| ID | Símbolo | Referência IEC 60617 | Descrição |
|---|---|---|---|
| SB-01 | Quadro de distribuição | IEC 60617-06-02-01 | Retângulo com identificação, fases e capacidade de corrente |
| SB-02 | Barramento trifásico R/S/T/N/PE | IEC 60617-06-01-01 | Linhas horizontais paralelas com identificação de fases por cor/letra |
| SB-03 | Disjuntor termomagnético | IEC 60617-07-08-01 | Símbolo de chave com arco de proteção térmica e magnética |
| SB-04 | Disjuntor diferencial residual (DR) | IEC 60617-07-08-02 | Disjuntor com símbolo de detecção de corrente diferencial |
| SB-05 | Condutor / fiação | IEC 60617-06-01-01 | Linha com indicação de número de condutores e seção (mm²) |
| SB-06 | Ponto de iluminação (ILU) | IEC 60617-11-01-01 | Círculo com cruz interna |
| SB-07 | Tomada de uso geral (TUG) | IEC 60617-11-03-01 | Semicírculo com pinos |
| SB-08 | Tomada de uso específico (TUE) | IEC 60617-11-03-02 | Semicírculo com identificação de equipamento |
| SB-09 | Aterramento | IEC 60617-02-15-01 | Linhas horizontais decrescentes |
| SB-10 | Dispositivo de proteção contra surtos (DPS) | IEC 60617-07-12-01 | [VERIFICAR] Símbolo a confirmar na versão vigente |

### 7.3 Símbolos complementares (Fase futura)

| ID | Símbolo | Descrição |
|---|---|---|
| SB-11 | Interruptor seccionador | Chave de manobra sem proteção |
| SB-12 | Fusível | Elemento fusível com indicação de corrente nominal |
| SB-13 | Contator | Para circuitos com acionamento remoto |
| SB-14 | Relé térmico | Proteção térmica de motores |
| SB-15 | Motor elétrico | Carga tipo motor (instalações comerciais/industriais) |
| SB-16 | AFDD (Arc Fault Detection Device) | Antecipação da revisão NBR 5410 esperada até final de 2026 |

### 7.4 Representação técnica dos símbolos

Cada símbolo é implementado como:

- Uma classe Python herdando de `schemdraw.elements.Element` (para composição e ancoragem automática).
- Uma definição SVG em `<defs>` com `id` semântico (`sie-sb-03-disjuntor`, `sie-sb-04-dr`).
- Um bloco DXF (`BLOCK`) com `ATTDEF` para dados variáveis (corrente nominal, polo, curva).
- Uma função de renderização ReportLab para PDF direto (fallback quando `svglib` não atender).

### 7.5 Dimensões e escala

Todos os símbolos são desenhados em unidades de milímetro com uma escala de referência de 1:50. O catálogo define dimensões canônicas:

| Elemento | Largura (mm) | Altura (mm) |
|---|---|---|
| Disjuntor termomagnético | 10 | 20 |
| Disjuntor DR | 10 | 25 |
| Ponto de iluminação | 8 | 8 |
| Tomada (TUG/TUE) | 8 | 12 |
| Barramento (por fase) | comprimento_total | 3 |
| Quadro de distribuição | 60 | 40 |

[VERIFICAR] Dimensões a confirmar com norma de representação gráfica ABNT NBR 5444 (se vigente) ou prática de mercado consolidada.

---

## 8. Motor de layout Python

### 8.1 Responsabilidade

O motor de layout recebe o grafo modelado (Camada 2) e produz coordenadas absolutas em milímetros para cada elemento do diagrama. Ele não renderiza — apenas calcula posições.

### 8.2 Saída do motor

```python
@dataclass
class LayoutResult:
    largura_mm: float
    altura_mm: float
    barramento: BarramentoLayout
    circuitos: list[CircuitoLayout]
    arestas: list[ArestaLayout]
    grupos: list[GrupoLayout]
    legenda: LegendaLayout

@dataclass
class CircuitoLayout:
    node_id: str
    x_mm: float
    y_mm: float
    largura_mm: float
    altura_mm: float
    simbolo_id: str           # Referência ao catálogo de simbologia
    rotulo: str               # Texto de identificação
    dados_rotulo: dict        # Potência, tensão, IB, fases — para renderização
    severidade: str
    tracejado: bool           # True se tensão pendente/não confirmada

@dataclass
class ArestaLayout:
    edge_id: str
    pontos_mm: list[tuple[float, float]]   # Polilinha (mínimo 3 pontos)
    tipo: str
```

### 8.3 Modo linear

Disposição vertical dos circuitos abaixo do barramento, organizados em coluna única. Cada circuito ocupa uma faixa horizontal com espaçamento uniforme. O barramento é renderizado na parte superior como linha horizontal com derivações verticais.

```
    ┌───────────────────────────────────┐
    │         QUADRO DE DISTRIBUIÇÃO    │
    │    ══R══════S══════T══════N════PE │  ← Barramento
    └───┬──────┬──────┬──────┬─────────┘
        │      │      │      │
       ╤╤     ╤╤     ╤╤     ╤╤         ← Disjuntores
        │      │      │      │
    ┌───┤  ┌───┤  ┌───┤  ┌───┤
    │C1 │  │C2 │  │C3 │  │C4 │         ← Circuitos
    └───┘  └───┘  └───┘  └───┘
```

**Parâmetros do layout linear:**

| Parâmetro | Valor padrão | Unidade |
|---|---|---|
| Espaçamento entre circuitos (horizontal) | 30 | mm |
| Espaçamento barramento→primeiro circuito (vertical) | 50 | mm |
| Largura do card de circuito | 25 | mm |
| Altura do card de circuito | 35 | mm |
| Margem esquerda | 20 | mm |
| Margem superior | 30 | mm |
| Margem para legenda (inferior) | 60 | mm |

### 8.4 Modo clustered

Disposição agrupada por critério técnico (dependência, tipo de carga, fase ou grupo EDP). Cada grupo recebe um cabeçalho visual e os circuitos do grupo são dispostos horizontalmente dentro do bloco do grupo. Os grupos são empilhados verticalmente.

```
    ┌──────────────────────────────────────┐
    │         QUADRO DE DISTRIBUIÇÃO       │
    │    ══R══════S══════T══════N═══PE     │
    └───┬──────────────────────────────────┘
        │
        ├─── ┌─── Sala ──────────────┐
        │    │  C1-ILU   C2-TUG      │
        │    └───────────────────────┘
        │
        ├─── ┌─── Cozinha ───────────┐
        │    │  C3-TUG   C4-TUE-MO   │
        │    └───────────────────────┘
        │
        └─── ┌─── Banheiro ──────────┐
             │  C5-ILU   C6-TUG      │
             └───────────────────────┘
```

### 8.5 Fallback Graphviz

Para projetos com mais de 80 circuitos (limiar configurável), o motor pode delegar o layout ao Graphviz `dot` via o binding Python. O `dot` produz layout hierárquico otimizado com minimização de cruzamento de arestas. As coordenadas retornadas pelo Graphviz são convertidas para milímetros e normalizadas para o espaço do diagrama.

### 8.6 Determinismo

O motor de layout é uma função pura: mesma entrada (grafo + modo + parâmetros) → mesma saída (coordenadas). Nenhum estado global, nenhum random, nenhum acesso a disco ou rede. Verificável por teste:

```python
def test_layout_deterministico():
    grafo = carregar_grafo_referencia()
    r1 = calcular_layout(grafo, modo="linear")
    r2 = calcular_layout(grafo, modo="linear")
    assert r1 == r2
```

---

## 9. Renderizador SVG técnico

### 9.1 Biblioteca

`svgwrite` ≥ 1.4.3 (gerador primário) + `schemdraw` ≥ 0.23 (composição de símbolos).

### 9.2 Estrutura do documento SVG

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {largura_mm} {altura_mm}"
     width="{largura_mm}mm"
     height="{altura_mm}mm"
     data-sie-versao="1.0.0"
     data-sie-projeto="{projetoId}"
     data-sie-gerado-em="{timestamp}">

  <defs>
    <!-- Símbolos IEC 60617 reutilizáveis -->
    <g id="sie-sb-03-disjuntor">...</g>
    <g id="sie-sb-04-dr">...</g>
    <g id="sie-sb-06-iluminacao">...</g>
    <g id="sie-sb-07-tug">...</g>
    <g id="sie-sb-08-tue">...</g>
    ...
  </defs>

  <!-- Layer: Barramento -->
  <g id="layer-barramento" class="sie-layer" data-sie-tipo="barramento">
    ...
  </g>

  <!-- Layer: Arestas (condutores) -->
  <g id="layer-arestas" class="sie-layer" data-sie-tipo="arestas">
    ...
  </g>

  <!-- Layer: Dispositivos de proteção -->
  <g id="layer-protecao" class="sie-layer" data-sie-tipo="protecao">
    <use xlink:href="#sie-sb-03-disjuntor"
         transform="translate({x},{y})"
         data-sie-circuito="{node.id}"
         data-sie-ib="{node.ibA}"
         data-sie-severidade="{node.severidade}" />
    ...
  </g>

  <!-- Layer: Cargas (circuitos) -->
  <g id="layer-cargas" class="sie-layer" data-sie-tipo="cargas">
    ...
  </g>

  <!-- Layer: Rótulos e textos -->
  <g id="layer-rotulos" class="sie-layer" data-sie-tipo="rotulos">
    <text x="{x}" y="{y}" font-family="ISO 3098" font-size="3">
      {circuito.nome} — {circuito.potenciaVA} VA — IB={circuito.ibA} A
    </text>
    ...
  </g>

  <!-- Layer: Carimbo e legenda -->
  <g id="layer-carimbo" class="sie-layer" data-sie-tipo="carimbo">
    ...
  </g>

</svg>
```

### 9.3 Requisitos do SVG

| ID | Requisito | Critério de aceitação |
|---|---|---|
| SVG-01 | Textos como elementos `<text>`, nunca como paths | XPath `//svg:path` não contém texto convertido |
| SVG-02 | Todos os símbolos definidos em `<defs>` e instanciados via `<use>` | XPath `//svg:defs/svg:g` ≥ 5 símbolos |
| SVG-03 | viewBox em milímetros | Atributos `width` e `height` terminam em `mm` |
| SVG-04 | Cada elemento gráfico de circuito tem `data-sie-circuito` | XPath `//svg:use[@data-sie-circuito]` count == `summary.qtdCircuitos` |
| SVG-05 | Layers separadas por `<g>` com `id` semântico | Pelo menos 5 layers: barramento, arestas, protecao, cargas, carimbo |
| SVG-06 | SVG válido contra schema W3C SVG 1.1 | `xmlschema.validate()` sem erros |
| SVG-07 | Fonte técnica ISO 3098 declarada | `font-family` referencia ISO 3098 ou fallback sans-serif |

---

## 10. Renderizador DXF CAD

### 10.1 Biblioteca

`ezdxf` ≥ 1.4, formato DXF R2010 (AC1024).

### 10.2 Organização de layers

| Layer | Cor (ACI) | Linetype | Descrição |
|---|---|---|---|
| `SIE_BARRAMENTO` | 5 (azul) | CONTINUOUS | Barramento de fases |
| `SIE_CONDUTORES` | 7 (branco/preto) | CONTINUOUS | Condutores/fiação |
| `SIE_CONDUTORES_PENDENTE` | 7 | DASHED | Condutores com tensão pendente |
| `SIE_PROTECAO` | 1 (vermelho) | CONTINUOUS | Disjuntores e dispositivos DR |
| `SIE_CARGAS` | 3 (verde) | CONTINUOUS | Pontos de carga (ILU, TUG, TUE) |
| `SIE_ROTULOS` | 7 | CONTINUOUS | Textos de identificação |
| `SIE_COTAS` | 2 (amarelo) | CONTINUOUS | Cotas e dimensões |
| `SIE_DIAGNOSTICOS` | 1 (vermelho) | CONTINUOUS | Marcadores de diagnóstico (ERRO/ATENÇÃO) |
| `SIE_CARIMBO` | 7 | CONTINUOUS | Carimbo e legenda |
| `SIE_MARGEM` | 8 (cinza) | CONTINUOUS | Margem da folha |

### 10.3 Blocos (BLOCK)

Cada símbolo IEC 60617 é definido como bloco DXF com `ATTDEF` para dados variáveis:

```python
# Exemplo: bloco do disjuntor termomagnético
bloco = doc.blocks.new(name="SIE_DISJUNTOR")
# Geometria do símbolo (linhas, arcos)
bloco.add_line((0, 0), (0, 10))
bloco.add_arc(center=(0, 15), radius=5, start_angle=0, end_angle=180)
bloco.add_line((0, 20), (0, 25))
# Atributo: corrente nominal
bloco.add_attdef(
    tag="IN",
    insert=(12, 10),
    text="In",
    dxfattribs={"height": 2.5, "layer": "SIE_ROTULOS"}
)
# Atributo: polo
bloco.add_attdef(
    tag="POLO",
    insert=(12, 15),
    text="Polo",
    dxfattribs={"height": 2.0, "layer": "SIE_ROTULOS"}
)
```

### 10.4 Instanciação

```python
msp = doc.modelspace()
msp.add_blockref(
    name="SIE_DISJUNTOR",
    insert=(x_mm, y_mm),
    dxfattribs={"layer": "SIE_PROTECAO"},
).add_auto_attribs({
    "IN": f"{circuito.ibA:.1f} A",
    "POLO": "2P" if len(circuito.fases) <= 2 else "3P",
})
```

### 10.5 Paperspace e carimbo

O DXF inclui um layout em paperspace com:

- Viewport apontando para o modelspace com escala configurável.
- Carimbo ABNT no canto inferior direito (ver seção 12).
- Margem da folha conforme formato selecionado.

### 10.6 Requisitos DXF

| ID | Requisito | Critério de aceitação |
|---|---|---|
| DXF-01 | Formato R2010 (AC1024) | `doc.dxfversion == "AC1024"` |
| DXF-02 | Todas as 10 layers presentes | `len(doc.layers)` ≥ 10 com prefixo `SIE_` |
| DXF-03 | Blocos de simbologia definidos | `doc.blocks` contém ao menos 5 blocos `SIE_*` |
| DXF-04 | Cada circuito instanciado como `INSERT` com `ATTRIB` | Count de `INSERT` == `summary.qtdCircuitos` |
| DXF-05 | Abre sem erro em AutoCAD 2020+ | Teste manual ou via `ezdxf.addons.drawing` |
| DXF-06 | Abre sem erro em BricsCAD V23+ | Teste manual |
| DXF-07 | Paperspace com viewport e carimbo | Layout "Folha" presente com viewport |
| DXF-08 | Rastreio via ATTRIB | Cada INSERT possui ATTRIB com tag `CIRCUITO_ID` |

---

## 11. Renderizador PDF vetorial

### 11.1 Bibliotecas

`ReportLab` ≥ 4.2 + `svglib` ≥ 0.9. Fluxo primário: SVG → `svg2rlg()` → `renderPDF.draw()`.

### 11.2 Estrutura do documento PDF

```
Página 1 (ou múltiplas, conforme tamanho do diagrama):
  ┌─────────────────────────────────────────────┐
  │                 MARGEM                       │
  │  ┌─────────────────────────────────────────┐ │
  │  │                                         │ │
  │  │         DIAGRAMA UNIFILAR               │ │
  │  │         (conteúdo vetorial)              │ │
  │  │                                         │ │
  │  │                                         │ │
  │  │                                         │ │
  │  ├─────────────────────────────────────────┤ │
  │  │         CARIMBO / LEGENDA ABNT          │ │
  │  └─────────────────────────────────────────┘ │
  └─────────────────────────────────────────────┘
```

### 11.3 Metadados do documento PDF

```python
canvas.setTitle(f"Diagrama Unifilar — {projeto.nome}")
canvas.setAuthor(f"{responsavel_tecnico}")
canvas.setSubject("Diagrama unifilar de instalações elétricas de baixa tensão")
canvas.setCreator("SIE — Sistema de Instalações Elétricas")
canvas.setKeywords(["unifilar", "NBR 5410", "IEC 60617", projeto.id])
```

### 11.4 Requisitos PDF

| ID | Requisito | Critério de aceitação |
|---|---|---|
| PDF-01 | 100% vetorial (sem rasterização de símbolos) | Zoom 800% sem pixelização |
| PDF-02 | Textos selecionáveis e buscáveis | `Ctrl+F` encontra nomes de circuitos |
| PDF-03 | Carimbo profissional | Carimbo presente no canto inferior direito |
| PDF-04 | Metadados de documento preenchidos | Propriedades do PDF contêm título, autor, criador |
| PDF-05 | Tamanho de página configurável | A4, A3, A2, A1 produzem tamanhos corretos |
| PDF-06 | Escala correta para impressão | Impressão em escala real corresponde às dimensões declaradas |
| PDF-07 | Imprimível em plotter | Resolução vetorial suficiente para A1 |

---

## 12. Carimbo e legenda profissional

### 12.1 Estrutura do carimbo

O carimbo segue o padrão de prática profissional brasileira (referência: norma de apresentação de projetos da prefeitura e prática de mercado, não há norma ABNT unificada para carimbo):

```
┌──────────────────────────────────────────────────────┐
│                    CARIMBO / LEGENDA                  │
├──────────────────────────┬───────────────────────────┤
│ Proprietário / Cliente   │ {nome_cliente}            │
├──────────────────────────┼───────────────────────────┤
│ Endereço da obra         │ {endereco}                │
├──────────────────────────┼───────────────────────────┤
│ Título do projeto        │ Instalações Elétricas     │
│                          │ de Baixa Tensão           │
├──────────────────────────┼───────────────────────────┤
│ Conteúdo da prancha      │ Diagrama Unifilar         │
├──────────────────────────┼───────────────────────────┤
│ Responsável técnico      │ {nome_engenheiro}         │
│                          │ CREA {numero_crea}        │
├──────────────────────────┼───────────────────────────┤
│ Escala                   │ {escala}                  │
├──────────────────────────┼───────────────────────────┤
│ Data                     │ {data}                    │
├──────────────────────────┼───────────────────────────┤
│ Prancha                  │ {numero_prancha}/{total}  │
├──────────────────────────┼───────────────────────────┤
│ Revisão                  │ {revisao}                 │
├──────────────────────────┼───────────────────────────┤
│ Sistema gerador          │ SIE v{versao}             │
└──────────────────────────┴───────────────────────────┘
```

### 12.2 Dados do carimbo

Os dados do carimbo são fornecidos via:

- Parâmetros da CLI (`--cliente`, `--endereco`, `--responsavel`, `--crea`).
- Arquivo de configuração JSON/YAML (para reutilização entre exportações).
- Campos do projeto no banco de dados (via endpoint FastAPI).

Campos não fornecidos são renderizados com placeholder `[A PREENCHER]`.

### 12.3 Implementação compartilhada

O carimbo é implementado em `renderizadores/carimbo.py` como uma função que produz:

- Elementos `svgwrite` para o SVG técnico.
- Entidades `ezdxf` para o DXF (no paperspace).
- Flowables ReportLab para o PDF.

---

## 13. CLI de exportação

### 13.1 Interface

```bash
python -m sie_unifilar_export \
  --in UnifilarGraph.json \
  --svg unifilar.svg \
  --dxf unifilar.dxf \
  --pdf unifilar.pdf \
  --layout linear \
  --papel A3 \
  --escala 1:50 \
  --cliente "João da Silva" \
  --endereco "Rua das Flores, 123 — São Paulo/SP" \
  --responsavel "Eng. Maria Santos" \
  --crea "SP-123456/D" \
  --verbose
```

### 13.2 Opções

| Opção | Tipo | Obrigatória | Padrão | Descrição |
|---|---|---|---|---|
| `--in` | path | Sim | — | Caminho do `UnifilarGraph.json` |
| `--svg` | path | Não | — | Caminho de saída SVG (omitir = não gerar) |
| `--dxf` | path | Não | — | Caminho de saída DXF (omitir = não gerar) |
| `--pdf` | path | Não | — | Caminho de saída PDF (omitir = não gerar) |
| `--layout` | choice | Não | `linear` | `linear` ou `clustered` |
| `--agrupamento` | choice | Não | `dependencia` | `dependencia`, `tipo`, `fase`, `grupo_edp` (só com `--layout clustered`) |
| `--papel` | choice | Não | `A3` | `A4`, `A3`, `A2`, `A1`, `A0` |
| `--orientacao` | choice | Não | `paisagem` | `paisagem` ou `retrato` |
| `--escala` | string | Não | `auto` | `1:50`, `1:75`, `1:100`, `auto` (calcula pela qtd de circuitos) |
| `--cliente` | string | Não | `[A PREENCHER]` | Nome do cliente/proprietário |
| `--endereco` | string | Não | `[A PREENCHER]` | Endereço da obra |
| `--responsavel` | string | Não | `[A PREENCHER]` | Responsável técnico |
| `--crea` | string | Não | `[A PREENCHER]` | Registro CREA |
| `--carimbo-json` | path | Não | — | JSON com dados do carimbo (alternativa às opções individuais) |
| `--verbose` | flag | Não | `false` | Saída detalhada com tabela de diagnósticos |
| `--strict` | flag | Não | `false` | Aborta se houver qualquer diagnóstico ERRO |
| `--version` | flag | Não | — | Exibe versão do pipeline |

### 13.3 Códigos de saída

| Código | Significado |
|---|---|
| 0 | Exportação concluída sem erros |
| 1 | Erro de validação do contrato |
| 2 | Erro de I/O (arquivo não encontrado, permissão negada) |
| 3 | Erro de renderização |
| 10 | Exportação concluída com diagnósticos ATENÇÃO |
| 11 | Exportação abortada por diagnóstico ERRO (modo `--strict`) |

### 13.4 Saída no terminal (rich)

```
╭─────────────────────────────────────────────────╮
│ SIE — Exportação de Diagrama Unifilar Completo  │
╰─────────────────────────────────────────────────╯

  Projeto:     proj-1
  Circuitos:   44
  IB máximo:   94.41 A
  Desequilíbrio: < 0.1%
  Modo divisão: adaptador_1_1
  Layout:      linear
  Papel:       A3 paisagem
  Escala:      1:50

  Validação do contrato ........... ✓
  Modelagem do grafo .............. ✓
  Cálculo de layout ............... ✓

  ┌─────────┬──────────────┬──────────┐
  │ Formato │ Arquivo      │ Status   │
  ├─────────┼──────────────┼──────────┤
  │ SVG     │ unifilar.svg │ ✓ 245 KB │
  │ DXF     │ unifilar.dxf │ ✓ 180 KB │
  │ PDF     │ unifilar.pdf │ ✓ 320 KB │
  └─────────┴──────────────┴──────────┘

  Diagnósticos: 2 INFO, 1 ATENÇÃO, 0 ERRO
```

---

## 14. Endpoint FastAPI

### 14.1 Rota

```
POST /api/projetos/{projetoId}/unifilar/exportar
```

### 14.2 Request body

```json
{
  "formatos": ["svg", "dxf", "pdf"],
  "layout": "linear",
  "agrupamento": "dependencia",
  "papel": "A3",
  "orientacao": "paisagem",
  "escala": "auto",
  "carimbo": {
    "cliente": "João da Silva",
    "endereco": "Rua das Flores, 123",
    "responsavel": "Eng. Maria Santos",
    "crea": "SP-123456/D"
  }
}
```

### 14.3 Response

Para cada formato solicitado, o endpoint retorna um link temporário para download:

```json
{
  "status": "ok",
  "exportacoes": [
    {
      "formato": "svg",
      "arquivo": "unifilar-proj-1.svg",
      "url": "/api/downloads/temp/{token}/unifilar-proj-1.svg",
      "tamanho_bytes": 250880,
      "expira_em": "2026-07-10T15:30:00Z"
    },
    {
      "formato": "dxf",
      "arquivo": "unifilar-proj-1.dxf",
      "url": "/api/downloads/temp/{token}/unifilar-proj-1.dxf",
      "tamanho_bytes": 184320,
      "expira_em": "2026-07-10T15:30:00Z"
    },
    {
      "formato": "pdf",
      "arquivo": "unifilar-proj-1.pdf",
      "url": "/api/downloads/temp/{token}/unifilar-proj-1.pdf",
      "tamanho_bytes": 327680,
      "expira_em": "2026-07-10T15:30:00Z"
    }
  ],
  "diagnosticos": {
    "info": 2,
    "atencao": 1,
    "erro": 0,
    "detalhes": [...]
  }
}
```

### 14.4 Fluxo interno

1. Endpoint busca o `UnifilarGraph` do projeto (já calculado pela tela de correntes).
2. Serializa para JSON e alimenta o pipeline `sie_unifilar_export` programaticamente.
3. Grava os arquivos em diretório temporário com TTL.
4. Retorna URLs de download.

---

## 15. Integração com o frontend

### 15.1 Ativação dos botões de exportação

O componente `UnifilarExportBar.tsx` já possui a interface para três formatos (SVG, PDF, DXF) com estado desabilitado. A integração requer:

1. O endpoint FastAPI (seção 14) estar disponível.
2. O frontend detectar a disponibilidade do endpoint via health check ou feature flag.
3. Os botões serem habilitados quando `CAPACIDADES_EXPORT` incluir os formatos.

```typescript
// Novo valor quando o pipeline Python estiver ativo:
export const CAPACIDADES_EXPORT_COMPLETO = {
  json: true,
  svg: true,
  pdf: true,
  dxf: true,
};
```

### 15.2 Fluxo do usuário

1. Usuário acessa a seção "Diagrama unifilar interativo do projeto".
2. Clica em "Exportar SVG técnico" (ou DXF ou PDF).
3. Modal de configuração aparece (papel, escala, dados do carimbo).
4. Usuário confirma.
5. Frontend chama `POST /api/projetos/{id}/unifilar/exportar`.
6. Spinner com barra de progresso.
7. Download automático do arquivo.

### 15.3 Opção de exportação simultânea

O modal de exportação pode oferecer a opção de exportar múltiplos formatos simultaneamente (checkboxes), gerando um ZIP com os três arquivos.

---

## 16. Conformidade normativa

### 16.1 Normas aplicáveis

| Norma | Aplicação no pipeline |
|---|---|
| ABNT NBR 5410:2004 | Regras de circuitos e proteção (consumidas do contrato, não recalculadas) |
| IEC 60617 | Simbologia gráfica para diagramas esquemáticos |
| IEC 60228 | Seções normalizadas de condutores (referência nos rótulos) |
| ABNT NBR 5444 [VERIFICAR] | Representação gráfica de instalações elétricas |
| ISO 3098 | Letras e algarismos para escrita técnica |
| ABNT NBR 6492 | Representação de projetos de arquitetura (referência para carimbo) |
| EDP-SP PT.DT.PDN.00068 v09 | Classificação EDP de grupos de carga (consumida do contrato) |
| EDP-SP PT.DT.PDN.03.14.020 v06 | Padrão de entrada (consumido do contrato) |

### 16.2 Rastreabilidade normativa nos símbolos

Cada símbolo do catálogo (seção 7) declara:

```python
class SimboloMetadata:
    id: str                    # "SB-03"
    nome: str                  # "Disjuntor termomagnético"
    referencia_iec: str        # "IEC 60617-07-08-01"
    status_verificacao: str    # "verificado" | "verificar"
    fonte: str                 # "IEC 60617:2012, Part 7, Symbol 08-01"
    notas: Optional[str]
```

---

## 17. Requisitos não-funcionais

### 17.1 Desempenho

| Métrica | Alvo | Método de verificação |
|---|---|---|
| Tempo de exportação SVG (44 circuitos) | < 2 s | pytest-benchmark |
| Tempo de exportação DXF (44 circuitos) | < 3 s | pytest-benchmark |
| Tempo de exportação PDF (44 circuitos) | < 5 s | pytest-benchmark |
| Tempo de exportação SVG (200 circuitos) | < 10 s | pytest-benchmark |
| Uso de memória (200 circuitos) | < 512 MB | memory_profiler |

### 17.2 Portabilidade

- O pipeline Python deve executar em Python ≥ 3.10 em Linux (Ubuntu 22.04+), macOS e Windows.
- Nenhuma dependência de AutoCAD, BricsCAD ou outro software CAD proprietário.
- A única dependência de sistema externa ao Python é o binário `graphviz` (opcional, para fallback de layout).

### 17.3 Segurança

- O pipeline não executa código arbitrário vindo do JSON de entrada.
- A validação Pydantic rejeita campos inesperados e tipos inválidos.
- URLs de download temporário expiram após 30 minutos.

### 17.4 Manutenibilidade

- Cobertura de testes ≥ 80% por módulo.
- Cada renderizador (SVG, DXF, PDF) é testável isoladamente.
- A adição de um novo símbolo ao catálogo não requer alteração nos renderizadores existentes (princípio Open/Closed).

### 17.5 Acessibilidade do SVG

- Elementos interativos com `aria-label` descritivo.
- Contraste de cores suficiente para severidade (WCAG AA).
- Textos legíveis em tamanho mínimo de 2.5 mm na escala de referência.

---

## 18. Estratégia de testes

### 18.1 Testes de contrato (Fase 1)

| ID | Teste | Tipo |
|---|---|---|
| TC-01 | JSON válido é deserializado sem erro | Unitário |
| TC-02 | JSON com campo faltante é rejeitado | Unitário |
| TC-03 | JSON com tipo errado é rejeitado | Unitário |
| TC-04 | Integridade referencial: edge aponta para node inexistente → ERRO | Unitário |
| TC-05 | Versão incompatível é rejeitada | Unitário |
| TC-06 | Contrato do projeto de referência (proj-1) é aceito | Integração |

### 18.2 Testes de layout (Fase 3)

| ID | Teste | Tipo |
|---|---|---|
| TL-01 | Determinismo: mesma entrada → mesma saída | Unitário |
| TL-02 | Layout linear: todos os circuitos posicionados sem sobreposição | Unitário |
| TL-03 | Layout clustered: grupos corretamente delimitados | Unitário |
| TL-04 | Coordenadas dentro da área do papel selecionado | Unitário |
| TL-05 | Escala auto calcula valor apropriado para 44 circuitos em A3 | Unitário |
| TL-06 | Escala auto calcula valor apropriado para 200 circuitos em A1 | Unitário |

### 18.3 Testes de SVG (Fase 3)

| ID | Teste | Tipo |
|---|---|---|
| TS-01 | SVG gerado é XML válido | Unitário |
| TS-02 | SVG contém `<defs>` com símbolos IEC | XPath |
| TS-03 | Cada circuito tem `data-sie-circuito` | XPath |
| TS-04 | Layers semânticas presentes | XPath |
| TS-05 | Textos são `<text>`, não `<path>` | XPath |
| TS-06 | viewBox em milímetros | Unitário |
| TS-07 | Hash perceptual estável entre execuções | Regressão |

### 18.4 Testes de DXF (Fase 4)

| ID | Teste | Tipo |
|---|---|---|
| TD-01 | DXF é aberto sem erro por `ezdxf.readfile()` | Unitário |
| TD-02 | 10 layers `SIE_*` presentes | Unitário |
| TD-03 | Blocos de simbologia definidos | Unitário |
| TD-04 | Cada circuito instanciado como INSERT com ATTRIB | Unitário |
| TD-05 | Paperspace com viewport e carimbo | Unitário |
| TD-06 | Formato R2010 (AC1024) | Unitário |
| TD-07 | Pré-visualização via `ezdxf.addons.drawing` sem crash | Integração |

### 18.5 Testes de PDF (Fase 5)

| ID | Teste | Tipo |
|---|---|---|
| TP-01 | PDF gerado é aberto sem erro por PyPDF2 | Unitário |
| TP-02 | Metadados do documento preenchidos | Unitário |
| TP-03 | Textos são extraíveis (não rasterizados) | Unitário |
| TP-04 | Tamanho de página corresponde ao formato solicitado | Unitário |
| TP-05 | Hash perceptual estável entre execuções | Regressão |

### 18.6 Testes de regressão visual (Todas as fases)

Renderização das saídas para bitmap (PNG) e comparação por hash perceptual (`imagehash.phash`) contra snapshots de referência. Tolerância de hamming distance ≤ 5 para variações aceitáveis de antialiasing entre plataformas.

---

## 19. Plano de entrega faseado

### Fase 1 — Fundação

**Duração estimada:** 2 semanas
**Entregáveis:**
- Modelos Pydantic v2 espelhando o contrato `UnifilarGraph`
- Validações de integridade referencial (V-01 a V-08)
- Modelagem NetworkX DiGraph a partir do contrato
- Fixture de teste com `UnifilarGraph` do projeto de referência (proj-1, 44 circuitos)
- Testes TC-01 a TC-06

**Critério de entrada:** Contrato `UnifilarGraph` v1.0.0 estabilizado e documentado.
**Critério de saída:** Todos os testes TC-* passam. Pipeline aceita o contrato do proj-1.

---

### Fase 2 — Simbologia IEC 60617

**Duração estimada:** 3 semanas
**Entregáveis:**
- Classe base `ElementoSIE` herdando de `schemdraw.elements.Element`
- 10 símbolos obrigatórios (SB-01 a SB-10) implementados
- Definições `<defs>` SVG para cada símbolo (via `svgwrite`)
- Blocos DXF para cada símbolo (via `ezdxf`)
- Catálogo Python com metadados normativos (referência IEC, status de verificação)
- Testes visuais de cada símbolo isolado (renderização + snapshot)

**Critério de entrada:** Fase 1 completa.
**Critério de saída:** Cada símbolo renderiza corretamente em SVG e DXF isoladamente. Rastreabilidade normativa documentada.

---

### Fase 3 — SVG técnico

**Duração estimada:** 3 semanas
**Entregáveis:**
- Motor de layout Python (linear + clustered)
- Renderizador SVG completo com layers, `<defs>`, `<use>`, metadados `data-*`
- Carimbo SVG
- Suíte de testes TL-01 a TL-06 e TS-01 a TS-07
- Snapshots de referência para regressão visual
- Primeira saída visual completa: `unifilar-proj-1.svg`

**Critério de entrada:** Fase 2 completa.
**Critério de saída:** SVG do proj-1 renderiza corretamente em navegador e Inkscape. Todos os testes TL-* e TS-* passam. Determinismo verificado.

---

### Fase 4 — DXF CAD

**Duração estimada:** 2 semanas
**Entregáveis:**
- Renderizador DXF com layers, blocos, INSERT/ATTRIB, paperspace/carimbo
- Testes TD-01 a TD-07
- Verificação visual via `ezdxf.addons.drawing`
- Saída: `unifilar-proj-1.dxf`

**Critério de entrada:** Fase 3 completa (layout e simbologia estabilizados).
**Critério de saída:** DXF abre sem erro em viewer ezdxf. Layers corretas. Blocos instanciados. Carimbo no paperspace.

---

### Fase 5 — PDF vetorial

**Duração estimada:** 2 semanas
**Entregáveis:**
- Renderizador PDF via ReportLab + svglib (fluxo SVG → PDF)
- Metadados de documento
- Carimbo PDF
- Testes TP-01 a TP-05
- Saída: `unifilar-proj-1.pdf`

**Critério de entrada:** Fase 3 completa (SVG gerado é insumo do PDF).
**Critério de saída:** PDF abre sem erro em Adobe Reader e navegadores. Textos selecionáveis. Carimbo legível. Impressão em escala correta.

---

### Fase 6 — CLI, endpoint e integração frontend

**Duração estimada:** 2 semanas
**Entregáveis:**
- CLI completa `python -m sie_unifilar_export` (click + rich)
- Endpoint FastAPI `POST /api/projetos/{id}/unifilar/exportar`
- Ativação dos botões de exportação no frontend
- Modal de configuração de exportação
- Testes de ponta a ponta (CLI → arquivos gerados → validação)
- Documentação de uso

**Critério de entrada:** Fases 3, 4 e 5 completas.
**Critério de saída:** Botões de exportação habilitados no frontend. Usuário exporta SVG/DXF/PDF a partir da interface. CLI funcional em terminal.

---

### Resumo do cronograma

| Fase | Duração | Dependência | Entrega principal |
|---|---|---|---|
| F1 — Fundação | 2 semanas | Contrato v1.0.0 | Modelos + validação + grafo |
| F2 — Simbologia | 3 semanas | F1 | 10 símbolos IEC 60617 |
| F3 — SVG técnico | 3 semanas | F2 | Primeira saída visual completa |
| F4 — DXF CAD | 2 semanas | F3 | DXF profissional |
| F5 — PDF vetorial | 2 semanas | F3 | PDF profissional |
| F6 — Integração | 2 semanas | F3 + F4 + F5 | CLI + endpoint + frontend |
| **Total** | **14 semanas** | | |

Nota: F4 e F5 podem ser paralelizadas (ambas dependem apenas de F3), reduzindo o caminho crítico para **12 semanas**.

---

## 20. Critérios de aceitação por fase

### Fase 1

- [ ] `UnifilarGraph` do proj-1 é carregado e validado sem erro.
- [ ] Contrato com campo obrigatório ausente é rejeitado com mensagem descritiva.
- [ ] Contrato com versão incompatível é rejeitado.
- [ ] DiGraph NetworkX construído com 1 barramento + 44 nós de circuito + 44 arestas.
- [ ] Todos os 6 testes TC-* passam.

### Fase 2

- [ ] 10 símbolos IEC 60617 renderizam corretamente em SVG isolado.
- [ ] 10 símbolos definidos como blocos DXF com ATTDEF.
- [ ] Cada símbolo tem metadados normativos (referência IEC, status).
- [ ] Classe base `ElementoSIE` permite adicionar novos símbolos sem alterar código existente.

### Fase 3

- [ ] SVG do proj-1 (44 circuitos) gerado em < 2 segundos.
- [ ] SVG contém 5+ layers semânticas.
- [ ] SVG contém `<defs>` com símbolos e `<use>` para instanciação.
- [ ] Cada circuito rastreável via `data-sie-circuito`.
- [ ] Layout determinístico verificado por teste (duas execuções idênticas).
- [ ] SVG abre corretamente em Chrome, Firefox, Inkscape.
- [ ] Carimbo presente com dados do projeto.

### Fase 4

- [ ] DXF do proj-1 gerado em < 3 segundos.
- [ ] DXF contém 10 layers `SIE_*`.
- [ ] Blocos de simbologia definidos e instanciados.
- [ ] Paperspace com viewport e carimbo.
- [ ] DXF abre sem erro via `ezdxf.addons.drawing`.
- [ ] Formato confirmado como R2010 (AC1024).

### Fase 5

- [ ] PDF do proj-1 gerado em < 5 segundos.
- [ ] 100% vetorial (sem rasterização).
- [ ] Textos selecionáveis.
- [ ] Metadados do documento preenchidos.
- [ ] Carimbo legível.
- [ ] Tamanho de página correto (A3).

### Fase 6

- [ ] CLI executa `python -m sie_unifilar_export --in proj-1.json --svg --dxf --pdf` com sucesso.
- [ ] Endpoint FastAPI responde com URLs de download.
- [ ] Botões de exportação habilitados no frontend.
- [ ] Usuário exporta os três formatos a partir da interface web.
- [ ] Código de saída CLI reflete o estado de diagnósticos.

---

## 21. Registro de riscos

| ID | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| R-01 | `svgwrite` não recebe mais atualizações (UNMAINTAINED) | Média | Baixo | SVG 1.1 é padrão estável; fork interno se necessário |
| R-02 | `schemdraw` não possui símbolos IEC 60617 para instalações prediais | Certa | Médio | Catálogo customizado via `Element` subclass (previsto no escopo) |
| R-03 | `svglib` não converte corretamente SVGs com `<use>` + `<defs>` | Média | Alto | Fallback: renderização PDF direta via ReportLab Canvas sem SVG intermediário |
| R-04 | Graphviz binário indisponível em ambiente de deploy | Baixa | Baixo | Motor de layout nativo é primário; Graphviz é fallback opcional |
| R-05 | Contrato `UnifilarGraph` muda de versão durante o desenvolvimento | Média | Alto | Versionamento semântico + validação de compatibilidade na Camada 1 |
| R-06 | DXF gerado incompatível com AutoCAD versões antigas (< 2020) | Baixa | Médio | R2010 é suportado desde AutoCAD 2010; teste manual em versão antiga |
| R-07 | Desempenho degradado para projetos > 100 circuitos | Média | Médio | Benchmark na Fase 3; otimização de layout e rendering se necessário |
| R-08 | Dimensões dos símbolos IEC não confirmadas em norma oficial | Certa | Médio | Marcados `[VERIFICAR]`; validação com norma ABNT NBR 5444 |
| R-09 | Revisão da NBR 5410 (prevista até final de 2026) invalida símbolos ou regras | Baixa | Alto | Catálogo de simbologia externalizável; SB-16 (AFDD) já previsto como fase futura |
| R-10 | Fonte ISO 3098 não disponível como TTF/OTF para embedding em SVG/PDF | Média | Médio | Fallback para fonte sans-serif padrão com declaração explícita no artefato |

---

## 22. Dependências técnicas e restrições

### 22.1 Dependências de software

| Componente | Versão mínima | Obrigatório? | Instalação |
|---|---|---|---|
| Python | 3.10 | Sim | — |
| pydantic | 2.0 | Sim | pip |
| networkx | 3.2 | Sim | pip |
| svgwrite | 1.4.3 | Sim | pip |
| ezdxf | 1.4 | Sim | pip |
| schemdraw | 0.23 | Sim | pip |
| reportlab | 4.2 | Sim | pip |
| svglib | 0.9 | Sim | pip |
| click | 8.1 | Sim | pip |
| rich | 13.0 | Sim | pip |
| lxml | 5.0 | Sim | pip |
| pytest | 8.0 | Dev | pip |
| pillow | 10.0 | Dev | pip |
| imagehash | 4.3 | Dev | pip |
| xmlschema | 3.0 | Dev | pip |
| graphviz (Python) | 0.20 | Opcional | pip |
| graphviz (binário) | — | Opcional | apt / brew |
| drawsvg | 2.3 | Dev | pip |
| cairosvg | 2.7 | Opcional | pip + libcairo |

### 22.2 Dependências de sistema

| Componente | Requerido por | Instalação |
|---|---|---|
| `graphviz` binário | Fallback de layout | `apt install graphviz` |
| `libcairo2` | `cairosvg` (opcional) | `apt install libcairo2` |

### 22.3 Restrições arquiteturais

- O pipeline não acessa banco de dados diretamente. A interface de dados é exclusivamente o `UnifilarGraph.json`.
- O pipeline não recalcula regras normativas NBR 5410, EDP-SP ou qualquer outra. Todos os valores elétricos são projetados do contrato canônico.
- O pipeline não modifica o contrato canônico. É uma operação read-only sobre os dados de entrada.
- O pipeline não depende de interface gráfica (headless). Nenhuma operação requer display X11, Wayland ou equivalente.
- O pipeline produz saída determinística: mesma entrada → mesma saída, byte a byte (exceto timestamps nos metadados, que são controlados por parâmetro de teste).

---

## 23. Glossário

| Termo | Definição |
|---|---|
| Diagrama unifilar | Representação esquemática simplificada de um circuito elétrico onde os condutores de uma mesma fase são representados por uma única linha |
| UnifilarGraph | Contrato canônico JSON que descreve a topologia do diagrama unifilar (nodes, edges, groups, meta, summary) |
| Barramento | Condutor principal que distribui energia elétrica do padrão de entrada para os circuitos do quadro de distribuição |
| Circuito | Conjunto de pontos de utilização protegidos por um mesmo dispositivo de proteção (disjuntor) |
| IEC 60617 | Norma internacional de simbologia gráfica para diagramas esquemáticos |
| NBR 5410 | Norma brasileira para instalações elétricas de baixa tensão |
| DXF | Drawing Exchange Format — formato aberto de intercâmbio de desenhos CAD |
| Planejador de Circuitos | Módulo do SIE que funciona como divisor de circuitos, agrupando pontos de utilização em circuitos conforme regras normativas |
| Adaptador 1:1 | Adaptador provisório que mapeia cada ponto de utilização como um circuito individual (sem agrupamento), mantendo compatibilidade enquanto o Planejador de Circuitos não assume |
| Severidade | Classificação de criticidade de um diagnóstico: INFO, ATENÇÃO ou ERRO |
| Carimbo | Quadro de informações técnicas e profissionais inserido na prancha do projeto, contendo dados do responsável técnico, escala, data e identificação |
| Layer (DXF) | Camada organizacional no arquivo DXF que permite separar e controlar a visibilidade de categorias de elementos |
| Paperspace (DXF) | Espaço de layout no DXF que simula a folha impressa, com viewports apontando para o modelspace |
| Modelspace (DXF) | Espaço de trabalho principal no DXF onde os elementos técnicos são desenhados em escala real |
| schemdraw | Biblioteca Python para composição de diagramas esquemáticos elétricos |
| ezdxf | Biblioteca Python para criação e manipulação de arquivos DXF |
| svgwrite | Biblioteca Python para geração programática de SVG |
| ReportLab | Biblioteca Python para geração de documentos PDF |

---

*Fim do PRD — Diagrama Unifilar Completo v1.0.0*
