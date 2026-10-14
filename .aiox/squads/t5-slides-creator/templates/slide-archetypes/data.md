# Template: Data/Analytics Slide

## Purpose
Apresentar dados, análises, insights quantitativos com máxima clareza. O chart deve "falar por si" - audience deve entender sem explicação verbal.

---

## SLIDE SPECIFICATION - DATA/ANALYTICS SLIDE

### PAGE NUMBER
**Posição:** Rodapé direito
**Coordenadas:** Coluna 11.5-12, Linha 7.9
**Formato:** Número sequencial (ex: "15")
**Fonte:** Helvetica Neue Regular, 10pt, #6E6E6E

---

### ACTION TITLE
**Posição:** Topo da área útil
**Coordenadas:** Colunas 1-12, Linha 1
**Grid alignment:** Full width

**Estrutura obrigatória:**
"[O QUE OS DADOS MOSTRAM] + [MAGNITUDE/COMPARAÇÃO] + [IMPLICAÇÃO]"

**Exemplos BOM:**
✅ "Revenue cresceu 34% em Q4 impulsionado por enterprise segment, superando guidance de 28% e validando upmarket strategy"

✅ "Customer acquisition cost caiu de $245 para $180 (-27%) via channel optimization, melhorando unit economics para LTV:CAC de 4.2:1"

✅ "Market share ganhou 3.2pp para 18.5% liderando categoria premium, enquanto competitors perderam terreno em value segment"

**Exemplos RUIM:**
❌ "Análise de revenue por trimestre" (descriptive, não insight)
❌ "Dados mostram crescimento" (vago, sem quantificação)
❌ "Performance financeira Q4" (título sem insight)

**Especificações tipográficas:**
- **Fonte:** Helvetica Neue Bold
- **Tamanho:** 16-18pt
- **Cor:** #003B5C (navy blue)
- **Alinhamento:** Left-aligned
- **Line height:** 1.3
- **Max linhas:** 2 (idealmente 1)
- **Bold numbers:** Números devem estar em bold mesmo dentro do título

---

### MAIN CHART AREA
**Posição:** Colunas 1-12, Linhas 2-7
**Grid:** Central area, máximo espaço dedicado ao visual

**Chart dimensions:**
- Width: 22cm (90% do slide width)
- Height: 10-11cm (adequado para legibilidade)
- Position: Centralizado horizontalmente

---

## CHART TYPE SPECIFICATIONS

### BAR CHART (Horizontal ou Vertical)

**Quando usar:**
- Comparação entre categorias
- Rankings
- Before/after comparisons

**Especificações obrigatórias:**

**Bars:**
- Width: 60-80% do espaço disponível
- Spacing: 20-40% da bar width
- Color: Primary (#00A86B green) para highlight, #B0BEC5 (gray) para others
- Border: None (clean look)
- Border radius: 2px (slightly rounded, modern)

**Eixo Y (valores):**
- SEMPRE começar em zero (regra absoluta para bar charts)
- Gridlines: Horizontal, #E5E5E5, 1pt, 30% opacity
- Ticks: Every significant interval (ex: 0, 50, 100, 150, 200)
- Label: 11pt Regular, #6E6E6E, right-aligned

**Eixo X (categorias):**
- Label: 11pt Regular, #000000, center-aligned sob cada bar
- Rotation: 0° (horizontal) ideal, 45° se labels longos, 90° último recurso
- Max characters: 15-20 por label

**Data Labels:**
- Position: Acima da barra (vertical) ou à direita (horizontal)
- Font: 12pt Bold, #000000
- Format: Número + unidade (ex: "$125M", "34%", "2,450 units")
- Precision: 0-1 decimal places (não mais)

**Destacar outliers:**
- Highest bar: Color #00A86B (green)
- Lowest bar (se relevant): Color #D32F2F (red)
- Others: #78909C (medium gray)

**Legend (se múltiplas séries):**
- Position: Top-right da chart area
- Font: 10pt Regular, #000000
- Symbols: 16×8px rectangles
- Spacing: 8pt entre itens

**Exemplo de especificação completa:**

**BAR CHART - Revenue by Product Line**
- Orientation: Vertical
- # Bars: 5 (Product A, B, C, D, E)
- Values: $180M, $145M, $98M, $67M, $42M
- Y-axis: $0-200M, gridlines every $50M
- Product A (highest): #00A86B
- Product E (lowest): #D32F2F
- Others: #78909C
- Data labels: Above each bar, "$XXM" format, 12pt Bold
- Spacing: Bars use 70% width, 30% spacing

---

### LINE CHART (Time Series)

**Quando usar:**
- Trends ao longo do tempo
- Múltiplas séries comparadas temporalmente
- Projeções / forecasts

**Especificações:**

**Lines:**
- Width: 3pt (main trend), 2pt (secondary trends)
- Style: Solid para actuals, dashed (4px dash, 3px gap) para forecast
- Colors:
  - Primary metric: #003B5C (navy)
  - Secondary: #00A86B (green)
  - Tertiary: #FF6F00 (orange)
  - Benchmark/Target: #B0BEC5 (gray), 2pt dashed

**Data points:**
- Markers: 6px circles
- Fill: Solid color matching line
- Border: 1px white (para destacar do line)
- Show all points OU apenas start/end/inflections (depende de densidade)

**Eixo X (Time):**
- Format: "Q1 2023", "Jan 2024", "Week 12" (consistent formatting)
- Ticks: Every period se <12 periods, every 2-3 se >12
- Label: 10pt Regular, #6E6E6E, rotação 0°

**Eixo Y (Values):**
- Não precisa começar em zero (diferente de bar chart!)
- Range: Min-10% to Max+10% (para dar breathing room)
- Gridlines: Horizontal, #E5E5E5, 1pt, 30% opacity
- Label: 11pt Regular, #6E6E6E

**Annotations:**
- Callouts para inflection points críticos
- Format: Small box com arrow apontando para ponto
- Text: "Peak: $250M in Q3" - 10pt Regular, background #FFFDE7 (light yellow)

**Shaded areas (opcional):**
- Para indicar períodos especiais (ex: recessão, lançamento produto)
- Color: #F5F5F5, 40% opacity
- Label: 9pt Italic, dentro da área

**Forecast separation:**
- Vertical dashed line separando historical vs forecast
- Label: "Forecast →" - 9pt Regular, #6E6E6E

**Exemplo:**

**LINE CHART - Monthly Revenue 2022-2024 with 2025 Forecast**
- X-axis: Jan 2022 to Dec 2025 (48 months)
- Y-axis: $80M to $180M
- Line 1 (Actual 2022-2024): #003B5C, 3pt, solid, 36 data points
- Line 2 (Forecast 2025): #003B5C, 3pt, dashed (4-3px)
- Benchmark line (Target): #B0BEC5, 2pt, dashed, horizontal at $150M
- Vertical separator: Dec 2024, dashed, #E0E0E0
- Annotation: "COVID impact" em Mar-May 2020, shaded area #F5F5F5
- Peak callout: "All-time high $172M" em Aug 2024

---

### WATERFALL CHART

**Quando usar:**
- Explicar variações (revenue walkdown, cost breakdown, P&L bridges)
- Mostrar contribuição de componentes para total
- Before/after com steps intermediários

**Especificações:**

**Bars:**
- Start bar: #003B5C (navy), full height from zero
- Positive contributions: #00A86B (green), floating
- Negative contributions: #D32F2F (red), floating
- End bar: #003B5C (navy), full height from zero

**Connectors:**
- Thin lines (1pt, #6E6E6E, dashed) conectando end de um bar ao start do próximo
- Opcional mas helpful para seguir o flow

**Data labels:**
- Valores absolutos acima de cada bar: "+$25M", "-$10M"
- Percentages (opcional): "(+15%)", "(-8%)"
- Font: 11pt Bold, cor matching bar color

**Eixo Y:**
- Start em zero
- Gridlines: #E5E5E5, 1pt
- Max value: 110% do end bar (breathing room)

**Eixo X:**
- Labels descritivos: "FY2023 EBITDA", "Revenue Growth", "Cost Inflation", "FY2024 EBITDA"
- Font: 11pt Regular, #000000, rotação 0°
- Max width: 12-15 caracteres (quebrar em 2 linhas se necessário)

**Subtotals (opcional):**
- Se muitos componentes (>7), agrupar em subtotals
- Subtotal bars: #78909C (medium gray), outlined 2pt

**Exemplo:**

**WATERFALL - EBITDA Bridge 2023 → 2024**
- Start: "2023 EBITDA $180M" - navy bar, full height
- +Revenue Growth: $45M - green floating bar
- +Margin Expansion: $12M - green
- -Cost Inflation: -$18M - red
- -Investment in R&D: -$9M - red
- End: "2024 EBITDA $210M" - navy bar
- Connectors: Dashed lines linking each bar
- Labels: All values shown, "+$XXM" ou "-$XXM"

---

### PIE CHART / DONUT CHART

**Quando usar:**
- Part-to-whole (composição, market share, revenue mix)
- Max 5-6 slices (mais que isso → bar chart!)
- Quando % composition mais importante que absolute values

**Especificações:**

**Slices:**
- Ordenar por tamanho (maior → menor, clockwise de 12h)
- Exceção: "Others" sempre por último
- Colors: Use paleta consistente, avoid similar shades adjacentes
- Border: 2pt white (para separar slices claramente)

**Explosion (destacar slice):**
- Pull out a slice mais importante 15-20px
- Apenas 1 slice exploded (não mais!)

**Labels:**
- **Option A (outside):** Line connector + label + percentage
  - Line: 1pt, #6E6E6E
  - Label: "Product A 34%" - 11pt Regular, #000000

- **Option B (inside):** Direto no slice
  - Apenas se slice >10% (otherwise too cramped)
  - Label: "34%" - 12pt Bold, color com contrast >4.5:1

**Center (donut only):**
- Total value: "Total: $450M" - 18pt Bold, #003B5C
- Secondary metric: "↑15% vs 2023" - 12pt Regular, #00A86B

**Legend:**
- Position: Right side da chart
- Format: Color box (16×16px) + Label (category) + Value ($ ou #) + Percentage
- Example: [green] Enterprise | $150M | 34%

**Evitar:**
- 3D effects (distorção, unprofessional)
- Gradients dentro de slices (confuso)
- >7 slices (use bar chart)

**Exemplo:**

**DONUT CHART - Revenue Mix by Segment**
- Total center: "Total Revenue $450M" - 18pt Bold
- Slices (clockwise de 12h):
  1. Enterprise: 34% ($153M) - #003B5C, exploded 18px
  2. Mid-market: 28% ($126M) - #00A86B
  3. SMB: 22% ($99M) - #FF6F00
  4. Consumer: 12% ($54M) - #1976D2
  5. Others: 4% ($18M) - #B0BEC5
- Labels: Outside com connectors
- Borders: 2pt white between slices

---

### SCATTER PLOT

**Quando usar:**
- Correlações entre 2 variáveis
- Segmentação (ex: 2×2 matrix)
- Outlier identification

**Especificações:**

**Data points:**
- Size: 8-12px circles (se todos iguais) OU proporcional a 3ª dimensão (bubble chart)
- Colors: By category ou single color
- Border: 1px white se points dense
- Opacity: 90% (para ver overlaps)

**Axes:**
- Eixo X e Y: Both visible, 2pt, #6E6E6E
- Origin: (0,0) se faz sentido, caso contrário min values - 10%
- Gridlines: Both horizontal e vertical, #E5E5E5, 30% opacity
- Ticks: Evenly spaced

**Quadrants (se 2×2 matrix):**
- Dividing lines: 2pt dashed, #003B5C
- Quadrant labels: 12pt Bold, #6E6E6E, em cada canto
- Background shading (opcional): Subtle colors (#F0F8FF, #E8F5E9) para destacar "good" quadrants

**Trendline (opcional):**
- Linear regression: 2pt dashed, #D32F2F
- R² value: Mostrar se >0.5 (otherwise não meaningful)
- Label: "R² = 0.73" - 10pt Regular

**Labels para pontos:**
- Apenas outliers ou pontos críticos (não todos!)
- Format: Small callout com arrow
- Text: 9pt Regular, background white 80% opacity

**Legend:**
- Se múltiplas categorias (colors diferentes)
- Position: Top-right
- Format: Circle + Label

**Exemplo:**

**SCATTER PLOT - Customer LTV vs CAC por Segment**
- X-axis: CAC ($0-$500)
- Y-axis: LTV ($0-$3,000)
- Quadrants: Dividido em x=$250, y=$1,000
  - Top-right: "High LTV, High CAC" (background #FFF9E6)
  - Top-left: "High LTV, Low CAC" ⭐ (background #E8F5E9 - sweet spot)
  - Bottom-right: "Low LTV, High CAC" ⚠️ (background #FFEBEE - problem)
  - Bottom-left: "Low LTV, Low CAC" (neutral)
- Data points: 25 circles, color by segment (Enterprise=#003B5C, SMB=#00A86B, Consumer=#FF6F00)
- Bubble size: Proportional to # customers (legend shows size scale)
- Trendline: Dashed, R²=0.68 shown
- Outliers labeled: "Segment X (Enterprise)" callout

---

## SUPPORTING ELEMENTS

### INSIGHT BOX (Opcional)
**Posição:** Colunas 1-3, Linha 6.5-7.5 OU canto que não interfere com chart
**Purpose:** Highlight de 1-2 insights críticos do chart

**Formato:**
"💡 Insight: [Key takeaway em 1 frase com número]"

**Exemplo:**
"💡 Insight: Top 3 products geram 68% do revenue mas apenas 22% do volume, indicando opportunity em premiumization"

**Especificações:**
- Background: #FFFDE7 (light yellow)
- Border: 2pt left border #FBC02D (yellow)
- Padding: 12pt all sides
- Font: 11pt Regular, #000000
- Icon: 16×16px, positioned left
- Max width: 3 colunas (1/4 do slide)

---

### DATA TABLE (Complementar ao chart)
**Quando incluir:**
- Valores exatos importantes
- Chart shows trend, table shows precision
- Audience precisa de reference numbers

**Posição:** Abaixo do chart, Linha 7-7.8, OU lado direito se chart não usa full width

**Formato:**
- Header row: Background #F5F5F5, 11pt Bold, #000000
- Data rows: Alternating white/#FAFAFA (zebra striping)
- Borders: 1pt #E0E0E0, only horizontal (between rows)
- Alignment: Numbers right-aligned, text left-aligned
- Padding: 6pt top/bottom, 8pt left/right

**Max rows visíveis:** 8-10 (se mais, resume apenas top/bottom)

**Exemplo:**

| Product | Q3 Revenue | Q4 Revenue | Growth |
|---------|------------|------------|--------|
| Product A | $45M | $52M | +16% |
| Product B | $38M | $41M | +8% |
| Product C | $29M | $33M | +14% |

Specs: 10pt Regular para data, #000000, right-align numbers

---

## FONTES DE DADOS

**SEMPRE incluir** (não-negociável para data slides)

**Posição:** Rodapé, abaixo linha 8, fora da área principal

**Formato:**
"Fonte: [Sistema/Database] ([período/data de extração]); [Benchmark source] ([ano/versão]); [Metodologia] se relevante; Company analysis"

**Exemplo completo:**
"Fonte: Salesforce CRM database (Q1-Q4 2024, extracted Dec 15, 2024); Gartner Magic Quadrant for CRM (2024) para peer benchmarks; NPS calculation methodology: survey de 2,450 customers (Nov 2024, 34% response rate); McKinsey analysis"

**Especificações:**
- Font: Helvetica Neue Light, 8pt, #B0B0B0
- Position: Margin bottom (0.5cm da borda)
- Max width: 90% do slide
- Line height: 1.2
- Multiple sources: Separated by semicolons

---

## CHECKLIST DE QUALIDADE - DATA SLIDE

**Action Title:**
- [ ] Contém número específico (não vago)?
- [ ] Explica o "so what" (não apenas descreve)?
- [ ] 14-20 palavras (conciso mas completo)?
- [ ] Insights leading (não trailing)?

**Chart:**
- [ ] Tipo correto para os dados (bar vs line vs waterfall)?
- [ ] Eixos começam apropriadamente (zero para bar, não para line)?
- [ ] Gridlines presentes mas sutis (não dominam)?
- [ ] Colors acessíveis (contrast >4.5:1)?
- [ ] Legend presente e claro (se múltiplas séries)?

**Data Labels:**
- [ ] Todos os valores visíveis e legíveis?
- [ ] Formato consistente ($M, %, K units)?
- [ ] Precision apropriada (0-1 decimais, não mais)?
- [ ] Positioned para não overlap?

**Fontes:**
- [ ] Database/system especificado?
- [ ] Data de extração incluída?
- [ ] Benchmarks sourced (com link se público)?
- [ ] Metodologia explicada (se não-standard)?

**Visual Quality:**
- [ ] Exportado em alta resolução (300 DPI)?
- [ ] Fontes embedded (não substituídas)?
- [ ] Colors RGB (screen) ou CMYK (print) apropriado?
- [ ] Anti-aliasing enabled (smooth lines)?

---

**VERSÃO:** 1.0
**OWNER:** GPT McKinsey PPT Architect
**ÚLTIMA ATUALIZAÇÃO:** Dezembro 2024
