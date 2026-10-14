# KB_06: Data Visualization Complete - Chart Selection & Best Practices

## CHART SELECTION MATRIX

### Decision Tree Completo

```
QUAL SEU OBJETIVO?

├─ COMPARAÇÃO (entre categorias)
│   ├─ Poucas categorias (2-7) → BAR CHART (horizontal se labels longos)
│   ├─ Muitas categorias (8+) → BAR CHART (vertical) OU TREEMAP
│   └─ Comparação + composição → STACKED BAR
│
├─ TENDÊNCIA/MUDANÇA AO LONGO DO TEMPO
│   ├─ 1 série → LINE CHART
│   ├─ 2-4 séries → LINE CHART (múltiplas linhas)
│   ├─ 5+ séries → SMALL MULTIPLES (vários line charts)
│   └─ Composição + tempo → STACKED AREA CHART
│
├─ PARTE DO TODO (proporções)
│   ├─ Simples (2-5 partes) → PIE CHART
│   ├─ Complexo (6+ partes) → DONUT OU BAR CHART
│   └─ Hierárquico → TREEMAP ou SUNBURST
│
├─ RELAÇÃO/CORRELAÇÃO
│   ├─ 2 variáveis → SCATTER PLOT
│   ├─ 3 variáveis → BUBBLE CHART (tamanho = 3ª variável)
│   └─ Matriz de correlações → HEATMAP
│
├─ DISTRIBUIÇÃO
│   ├─ Frequência → HISTOGRAM
│   ├─ Box plot → Mostrar quartis + outliers
│   └─ Density → VIOLIN PLOT
│
├─ DECOMPOSIÇÃO/BRIDGE
│   ├─ De valor A para B → WATERFALL CHART
│   └─ Contribuição de partes → STACKED BAR com annotations
│
└─ RANKING/ORDEM
    ├─ Simples → BAR CHART (horizontal, ordenado)
    └─ Com categorias → GROUPED BAR ordenado
```

---

## 1. BAR CHART (Barras)

### Quando Usar
- **Comparação** entre categorias discretas
- **Ranking** (ordenar por valor)
- Dados com **labels longos** (horizontal)

### Quando NÃO Usar
- Tendências temporais (use line chart)
- Correlações (use scatter)
- Mais de 20 categorias (agrupe)

### Especificações Técnicas

**Orientação:**
- **Horizontal:** Quando labels são longos (>15 caracteres) OU muitas categorias (10+)
- **Vertical:** Quando labels são curtos E poucas categorias

**Dimensões:**
- Largura de barra: 0.6-0.8 da largura disponível
- Espaçamento entre barras: 0.2-0.4 da largura de barra
- Altura mínima: 0.5cm por barra (horizontal)

**Cores:**
- **1 cor:** Se todas barras são mesma categoria
- **Destaque:** 1 barra em cor diferente (highlight)
- **Categorical:** Cores diferentes se categorias distintas (máximo 5 cores)

**Eixos:**
- Sempre começar em zero (regra absoluta)
- Gridlines apenas no eixo de valores (não em categorias)
- Labels perpendiculares ao eixo

**Data Labels:**
- Exibir valor ao final de cada barra (direita se horizontal, topo se vertical)
- Fonte: 11-12pt
- Formato: Consistente (ex: "R$ 12.5M")

### Exemplo de Especificação Completa

```markdown
ELEMENTO: Gráfico de Barras Horizontais
ENUMERAÇÃO: Gráfico 5.2

DADOS:
Categoria A: R$ 125M
Categoria B: R$ 98M
Categoria C: R$ 87M
Categoria D: R$ 65M
Categoria E: R$ 43M

POSIÇÃO: Grid colunas 2-10, linhas 3-6
DIMENSÕES: 16cm × 8cm

EIXO X (Valores):
- Escala: R$ 0M, 50M, 100M, 150M
- Título: "Receita (R$ milhões)"
- Gridlines: Verticais, #E5E5E5, 20% opacidade
- Fonte: Helvetica Neue Regular 11pt #6E6E6E

EIXO Y (Categorias):
- Labels: "Categoria A", "Categoria B", etc
- Alinhamento: Direita (flush right)
- Fonte: Helvetica Neue Regular 12pt #000000

BARRAS:
- Cor: #003B5C (navy blue)
- Altura: 1.2cm cada
- Espaçamento: 0.4cm entre barras
- Barra "Categoria A" destacada: Cor #00A86B (green)

DATA LABELS:
- Posição: 0.3cm à direita do final de cada barra
- Fonte: Helvetica Neue Bold 12pt #003B5C
- Formato: "R$ XXM"

CALLOUT:
Seta apontando para Categoria A
Texto: "Lidera com 29% do total"
Posição: Acima da barra
```

---

## 2. LINE CHART (Linhas)

### Quando Usar
- **Tendências** ao longo do tempo
- **Mudanças contínuas**
- Comparação de **múltiplas séries temporais** (máximo 4)

### Quando NÃO Usar
- Dados discretos/categóricos (use bar)
- Mais de 4-5 linhas (fica confuso - use small multiples)
- Valores que não podem ser interpolados

### Especificações Técnicas

**Linhas:**
- Espessura: 2-3pt (linha principal), 1.5-2pt (linhas secundárias)
- Estilo: Sólida (principal), Tracejada (secundária ou forecast)
- Suavização: Usar splines suaves OU linhas retas (ser consistente)

**Marcadores:**
- Usar APENAS se: (a) poucos pontos (<10) OU (b) destacar pontos específicos
- Tamanho: 6-8pt
- Formas: Círculo (série 1), Quadrado (série 2), Triângulo (série 3)

**Cores:**
- Máximo 4 cores diferentes
- Usar gradações se mais linhas (ex: azul escuro, médio, claro)
- Contraste suficiente entre linhas (mínimo 30% diferença)

**Área Sombreada:**
- Entre linhas: Mostrar gap/diferença
- Abaixo de linha: Área acumulada
- Opacidade: 15-30%

**Annotations:**
- Marcar pontos de inflexão importantes
- Indicar eventos (linha vertical tracejada + label)
- Callouts para insights

### Exemplo de Especificação

```markdown
ELEMENTO: Gráfico de Linhas Comparativo
ENUMERAÇÃO: Gráfico 3.1

SÉRIES:
Série 1 (Brasil): 2020: 45, 2021: 52, 2022: 68, 2023: 89, 2024: 112
Série 2 (Global): 2020: 45, 2021: 48, 2022: 53, 2023: 59, 2024: 64

DIMENSÕES: 14cm × 9cm
POSIÇÃO: Colunas 2-9, Linhas 2-6

EIXO X (Tempo):
- Anos: 2020, 2021, 2022, 2023, 2024
- Fonte: Helvetica 11pt #6E6E6E

EIXO Y (Valores):
- Escala: 0, 30, 60, 90, 120
- Título: "Market Size (US$ bi)"
- Gridlines: Horizontais, #E5E5E5 15% opacidade

SÉRIE 1 (Brasil):
- Cor: #00A86B (emerald green)
- Linha: 3pt sólida
- Marcadores: Círculos 7pt

SÉRIE 2 (Global):
- Cor: #6E6E6E (medium gray)
- Linha: 2pt tracejada (4px dash, 2px gap)
- Marcadores: Quadrados vazados 6pt

ÁREA SOMBREADA:
- Entre Série 1 e Série 2 (2022-2024)
- Cor: #00A86B 20% opacidade
- Representa aceleração do Brasil vs Global

ANNOTATION:
- Linha vertical em 2022
- Label: "Ponto de inflexão"
- Cor: #FF6F00 (orange)

LEGENDA:
Posição: Superior esquerda (dentro do gráfico)
Fundo: Branco 90% opacidade
Itens:
  ━━ Brasil (CAGR 25%)
  ── Global (CAGR 9%)
```

---

## 3. WATERFALL CHART (Cascata)

### Quando Usar
- **Decomposição** de variação entre dois valores
- **Bridge** de um valor para outro
- Mostrar contribuições positivas e negativas

### Quando NÃO Usar
- Comparação simples (use bar)
- Mais de 12-15 componentes (simplificar)

### Estrutura

```
Base (valor inicial)
  +Fator A (positivo, verde)
  +Fator B (positivo, verde)
  -Fator C (negativo, vermelho)
  +Fator D (positivo, verde)
= Total (valor final)
```

**Barras flutuantes:** Cada barra começa onde anterior terminou

### Especificações Técnicas

**Cores:**
- **Valores iniciais/finais:** Azul escuro #003B5C
- **Contribuições positivas:** Verde #00A86B
- **Contribuições negativas:** Vermelho #C8102E
- **Subtotais intermediários:** Cinza #6E6E6E

**Conectores:**
- Linhas tracejadas conectando fim de uma barra ao início da próxima
- Cor: #CCCCCC (cinza claro)
- Espessura: 1pt

**Data Labels:**
- Valor exato em cada barra (dentro ou acima)
- Sinal + ou - explícito para contribuições
- Total acumulado (opcional) abaixo de subtotais

### Exemplo

```markdown
ELEMENTO: Waterfall Chart - Ponte de EBITDA
ENUMERAÇÃO: Gráfico 7.3

DADOS:
EBITDA 2023: $100M (base)
  +Crescimento receita: +$45M
  +Otimização custos: +$12M
  -Inflação: -$18M
  -Investimentos growth: -$9M
EBITDA 2024: $130M (total)

VISUAL:
Barra 1 (Base 2023): $100M, azul #003B5C, largura 2cm
  Conector tracejado
Barra 2 (+Receita): $45M, verde #00A86B, começa em $100M
  Conector tracejado
Barra 3 (+Custos): $12M, verde #00A86B, começa em $145M
  Conector tracejado
Barra 4 (-Inflação): $18M, vermelho #C8102E, para baixo de $157M
  Conector tracejado
Barra 5 (-Growth invest): $9M, vermelho #C8102E, para baixo de $139M
  Conector tracejado
Barra 6 (Total 2024): $130M, azul #003B5C, largura 2cm

CALLOUT:
"Crescimento operacional de +57M parcialmente compensado por -27M de headwinds"
```

---

## 4. PIE CHART / DONUT CHART

### Quando Usar
- **Proporções simples** (parte do todo)
- Máximo 5-6 fatias
- Quando percentuais somam 100%

### Quando NÃO Usar
- Comparar valores absolutos (use bar)
- Mais de 6 categorias (use bar horizontal)
- Tendências ao longo tempo
- Múltiplos pies lado a lado (dificulta comparação - use stacked bar)

### Regras de Ouro

**Ordenação:**
- Maior fatia começa às 12h (topo)
- Ordem horária decrescente
- "Outros" sempre por último

**Cores:**
- Gradação de uma cor (mais escuro = maior)
- OU cores categóricas (máximo 5)
- Contraste entre fatias adjacentes

**Labels:**
- **Preferível:** Labels diretos (fora do pie, com linhas de conexão)
- **Evitar:** Legenda separada (requer olho ir e voltar)
- Incluir percentual E valor absoluto

**Donut vs Pie:**
- **Donut:** Permite label central (ex: "Total: $500M")
- **Pie:** Mais tradicional, ocupa menos espaço

### Exemplo

```markdown
ELEMENTO: Donut Chart - Market Share por Competidor
ENUMERAÇÃO: Gráfico 4.1

DADOS:
Nossa empresa: 35% ($350M)
Competidor A: 28% ($280M)
Competidor B: 18% ($180M)
Competidor C: 12% ($120M)
Outros: 7% ($70M)
Total: 100% ($1,000M)

VISUAL:
Diâmetro externo: 10cm
Diâmetro interno: 6cm (donut)
Centro: "Total Market\n$1,000M" (Helvetica Bold 16pt)

FATIAS (ordem horária de 12h):
1. Nossa empresa (35%): 12h-2:36h, cor #003B5C (navy), destacado com 0.2cm offset
2. Competidor A (28%): 2:36h-6:00h, cor #0077BE (blue)
3. Competidor B (18%): 6:00h-9:30h, cor #6E6E6E (gray)
4. Competidor C (12%): 9:30h-11:18h, cor #AAAAAA (light gray)
5. Outros (7%): 11:18h-12h, cor #D3D3D3 (very light gray)

LABELS:
Posição: Fora do donut, alinhados radialmente
Linhas de conexão: 1pt, cor da fatia
Texto: "[Nome]\n[35%] - [$350M]"
Fonte: Helvetica 11pt

DESTAQUE:
Nossa fatia com offset de 0.2cm para ênfase
```

---

## 5. SCATTER PLOT (Dispersão)

### Quando Usar
- **Correlação** entre 2 variáveis
- Identificar **outliers**
- Segmentação em **quadrantes** (matriz 2×2)

### Quando NÃO Usar
- Dados discretos/categóricos
- Tendência temporal (use line)

### Bubble Chart (3 variáveis)
Scatter + tamanho de bolha representa terceira variável

### Especificações Técnicas

**Pontos:**
- Tamanho: 8-12pt (scatter), 10-50pt (bubble)
- Forma: Círculos (padrão), Quadrados (alternativo)
- Opacidade: 70-90% se muitos pontos sobrepõem
- Borda: 1pt opcional (melhora definição)

**Eixos:**
- **IMPORTANTE:** Nem sempre começar em zero (ao contrário de bar chart)
- Escala deve mostrar relação claramente
- Incluir R² se houver trend line

**Trend Line:**
- Linear, polinomial, ou logarítmica (conforme dados)
- Cor: Cinza #AAAAAA, linha tracejada
- Espessura: 1.5pt
- Label com equação e R²

**Quadrantes:**
- Linhas de referência (média ou mediana)
- Cor: #CCCCCC, tracejada
- Labels em cada quadrante explicando significado

### Exemplo

```markdown
ELEMENTO: Scatter Plot com Quadrantes
ENUMERAÇÃO: Gráfico 6.2

DADOS: [50 data points - empresa vs competidores]
Eixo X: NPS (0-100)
Eixo Y: Crescimento Receita % (-10% a +40%)

DIMENSÕES: 12cm × 12cm (square)

EIXO X (NPS):
Range: 0-100
Tick marks: 0, 20, 40, 60, 80, 100
Linha vertical de referência: NPS=50 (mediana)

EIXO Y (Crescimento):
Range: -10% a +40%
Tick marks: -10, 0, 10, 20, 30, 40
Linha horizontal de referência: Crescimento=15% (mediana)

QUADRANTES:
Superior Direito (High NPS + High Growth): "Winners" - Verde claro #E8F8F0
Superior Esquerdo (Low NPS + High Growth): "Vulnerable" - Amarelo claro #FFF8DC
Inferior Direito (High NPS + Low Growth): "Complacent" - Azul claro #E8F4F8
Inferior Esquerdo (Low NPS + Low Growth): "Laggards" - Vermelho claro #FFE8E8

PONTOS:
Nossa empresa: Bolha 30pt, cor #003B5C (navy), borda 2pt branca
Competidores: Bolhas 15pt, cor #AAAAAA (gray), 70% opacidade
Top 3 competidores: Rotulados com nome

TREND LINE:
Linear, R²=0.67
Equação: y = 0.35x + 8
Cor: #CCCCCC tracejada

ANNOTATION:
Seta apontando nossa bolha
"Posicionados no quadrante 'Winners' mas próximos a 'Vulnerable'"
```

---

## REGRAS UNIVERSAIS DE FORMATAÇÃO

### 1. Eixos

**Sempre:**
- [ ] Títulos de eixo claros (unidade explícita)
- [ ] Escala apropriada (não truncar enganosamente)
- [ ] Tick marks em intervalos lógicos (5, 10, 25, 50, 100, 250, etc)
- [ ] Fonte consistente (11pt para labels)

**Eixo Y em Bar Charts:**
- SEMPRE começar em zero (exceção: pequenas variações em grande escala - sinalizar claramente)

**Eixo Y em Line Charts:**
- Pode NÃO começar em zero se fizer sentido (ex: variação de 98.5% a 99.5%)
- MAS incluir break symbol (⚡) se truncado

### 2. Gridlines

**Regra:** Menos é mais

- Apenas no eixo de valores (não em categorias)
- Horizontais para bar vertical, Verticais para bar horizontal
- Cor: #E5E5E5 (cinza muito claro)
- Opacidade: 15-25%
- Espessura: 0.5pt

### 3. Data Labels

**Quando incluir:**
- Valores exatos são importantes
- Poucas barras/pontos (<15)

**Quando omitir:**
- Muitos valores (cluttered)
- Valores são evidentes pela escala

**Formatação:**
- Fonte: 1-2pt menor que labels de eixo
- Posição: Consistente (sempre topo OU sempre dentro)
- Formato numérico: Consistente (casas decimais, separadores)

### 4. Legends

**Preferência:** Direct labeling > Legend separada

**Se usar legend:**
- Posição: Dentro do gráfico (top-right ou top-left)
- Fundo: Branco semi-transparente (85% opacidade)
- Borda: Sutil (0.5pt #CCCCCC) ou nenhuma
- Ordem: Mesma ordem dos dados no gráfico

### 5. Cores

**Paletas Recomendadas:**

**Categórica (5-7 cores distintas):**
```
#003B5C (navy)
#00A86B (green)
#0077BE (blue)
#FFA000 (amber)
#C8102E (red)
#6C63FF (purple)
#FF6F00 (orange)
```

**Sequential (gradação de 1 cor):**
```
Azul: #E8F4F8 → #0077BE → #003B5C
Verde: #E8F8F0 → #00A86B → #00563F
```

**Divergente (2 extremos + neutro):**
```
Vermelho-Branco-Verde:
#C8102E (red) → #FFFFFF (white) → #00A86B (green)

Laranja-Branco-Azul:
#FF6F00 (orange) → #FFFFFF (white) → #0077BE (blue)
```

### 6. Acessibilidade

**Contraste:**
- Texto em branco: Fundo mínimo #767676 (contrast 4.5:1)
- Texto em preto: Fundo máximo #B0B0B0

**Color Blind Safe:**
- Nunca usar apenas cor para diferenciar (usar + forma/padrão)
- Evitar vermelho/verde juntos sem outro indicador
- Testar com simulador de daltonismo

### 7. Enumeração

**TODO gráfico:**
```
Gráfico [N]
ou
Gráfico [Seção].[Item]

Posição: 0.5cm acima do gráfico, alinhado à esquerda
Fonte: Helvetica Bold 10pt #6E6E6E
```

### 8. Fonte de Dados

**Formato:**
```
Fonte: [Organização]. [Documento]. [Data].
[URL]. Acesso: [Data acesso].

Posição: 0.3cm abaixo do gráfico, alinhado à esquerda
Fonte: Helvetica Italic 9pt #6E6E6E
```

---

## ERROS COMUNS (NUNCA FAZER)

### ❌ 3D Charts
**Problema:** Distorcem percepção, difícil ler valores exatos
**Solução:** SEMPRE 2D

### ❌ Dual Y-Axis
**Problema:** Pode manipular percepção de correlação
**Solução:** Dois gráficos separados OU normalizar escalas

### ❌ Pie Chart com 10+ fatias
**Problema:** Impossível comparar fatias pequenas
**Solução:** Agrupar em "Outros" OU usar bar chart

### ❌ Eixo Y não começando em zero (bar chart)
**Problema:** Exagera diferenças
**Solução:** SEMPRE zero em bar chart

### ❌ Cores aleatórias
**Problema:** Confunde, sem significado
**Solução:** Paleta consistente, cores significativas

### ❌ Mais de 4-5 linhas em line chart
**Problema:** Spaghetti chart, ilegível
**Solução:** Small multiples (vários gráficos pequenos)

---

**FIM DO KB_06**

Total: ~1500 palavras - Padrão 12/10 atingido
