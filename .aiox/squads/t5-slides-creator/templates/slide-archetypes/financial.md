# Template: Financial/P&L Slide

## Purpose
Apresentar performance financeira, business case, ROI analysis, P&L bridges com máxima precisão e credibilidade.

---

## SLIDE SPECIFICATION - FINANCIAL SLIDE

### PAGE NUMBER
**Posição:** Rodapé direito
**Coordenadas:** Coluna 11.5-12, Linha 7.9
**Formato:** Número sequencial
**Fonte:** Helvetica Neue Regular, 10pt, #6E6E6E

---

### ACTION TITLE
**Posição:** Topo
**Coordenadas:** Colunas 1-12, Linha 1

**Estrutura obrigatória:**
"[METRIC] + [PERFORMANCE vs BENCHMARK/PRIOR] + [DRIVERS] + [IMPLICATION]"

**Exemplos:**

✅ "EBITDA cresceu $45M (+32%) para $185M em 2024 via expansion de margin (4pp) e volume growth (18%), superando guidance de $170M"

✅ "ROI de transformation program atingiu 4.2× com payback de 14 meses, validando business case e suportando Phase 2 approval de $80M"

✅ "Free cash flow melhorou $120M para $340M através de working capital optimization (60% do ganho) e CAPEX discipline (40%)"

**Especificações:**
- Fonte: Helvetica Neue Bold, 16-18pt, #003B5C
- Numbers: Sempre em bold (mesmo dentro do título)
- Line height: 1.3
- Max linhas: 2

---

## FINANCIAL TABLE SPECIFICATIONS

### P&L TABLE (Income Statement)

**Quando usar:**
- Performance review
- Budget vs actual
- Multi-period comparison

**Estrutura:**

**Dimensions:**
- Width: Colunas 1-12 (full width)
- Position: Linhas 2-7
- Rows: 12-18 (mais que isso → summarize ou split)

**Column structure (típico):**

| Item | 2022 | 2023 | 2024E | Growth 23-24 | % of Revenue |
|------|------|------|-------|--------------|--------------|

**Header row:**
- Background: #003B5C (navy blue - McKinsey style)
- Font: 11pt Bold, #FFFFFF
- Height: 0.8cm
- Alignment: Center (numbers), Left (labels)
- Borders: 1pt white (separar colunas)

**Data rows:**
- Alternating: White / #FAFAFA (zebra striping para legibility)
- Font: 10pt Regular, #000000
- Height: 0.6cm
- Padding: 4pt top/bottom, 8pt left/right
- Alignment:
  - Item names: Left
  - Numbers: Right
  - Percentages: Right

**Row categories:**

**REVENUE (Top section):**
- Row 1: "Revenue" - 11pt Bold, #000000
- Indented sub-items (se breakdown):
  - "  Product A" - 10pt Regular, indent 12pt
  - "  Product B"
  - "  Services"
- Border bottom: 2pt #003B5C após last revenue item

**COGS:**
- "Cost of Goods Sold" - 10pt Regular
- Sub-items se relevant

**GROSS PROFIT:**
- Row: "Gross Profit" - 11pt Bold, background #E8F5E9 (light green highlight)
- Border: 1pt top e bottom, #00A86B

**OPEX:**
- "Operating Expenses" header
- Sub-items:
  - Sales & Marketing
  - R&D
  - G&A
- Border bottom: 1pt após last opex

**EBITDA:**
- "EBITDA" - 12pt Bold, background #E8F5E9 (light green)
- Border: 2pt top e bottom, #00A86B (key metric!)

**D&A:**
- "Depreciation & Amortization"

**EBIT:**
- "EBIT" - 11pt Bold, background #E8F5E9

**Interest, Tax:**
- Standard rows

**NET INCOME:**
- "Net Income" - 12pt Bold, background #C8E6C9 (darker green - bottom line)
- Border: 3pt top e bottom, #00A86B

**Number formatting:**
- Currency: "$XXM" OU "$XX,XXXK" (consistent units!)
- Decimals: 0-1 decimal places (não mais)
- Negative numbers: "($XX)" em red #D32F2F OU "-$XX"
- Percentages: "XX%" ou "XX.X%"
- Growth: "+XX%" (green #00A86B) ou "-XX%" (red #D32F2F)

**Variance columns:**
- Calculation: (2024 - 2023) / 2023 × 100%
- Conditional formatting:
  - Positive revenue/profit growth: Green #00A86B
  - Negative: Red #D32F2F
  - Cost reduction: Green (lower is better)
- Bold se variance >10% (material)

**% of Revenue column:**
- Calculation: Item / Revenue × 100%
- Format: "XX%" ou "XX.X%"
- Benchmark comparison (opcional): Small arrow ↑↓ se vs peers

**Borders:**
- Outer border: 2pt, #003B5C (frame todo table)
- Section dividers: 1pt, #E0E0E0 (between REVENUE, COGS, OPEX, etc.)
- Key metrics: 2-3pt, #00A86B (EBITDA, Net Income)

**Exemplo completo:**

**P&L TABLE - 3-Year Performance**

| P&L Item | 2022 | 2023 | 2024E | Var % | % Rev |
|----------|------|------|-------|-------|-------|
| **Revenue** | $450M | $520M | $615M | **+18%** | 100% |
| Product A | $250M | $290M | $350M | +21% | 57% |
| Product B | $150M | $170M | $195M | +15% | 32% |
| Services | $50M | $60M | $70M | +17% | 11% |
| **COGS** | ($225M) | ($255M) | ($295M) | +16% | 48% |
| **Gross Profit** | **$225M** | **$265M** | **$320M** | **+21%** | **52%** ⬆ |
| Operating Expenses | ($135M) | ($155M) | ($175M) | +13% | 28% |
| S&M | ($70M) | ($80M) | ($90M) | +13% | 15% |
| R&D | ($40M) | ($48M) | ($55M) | +15% | 9% |
| G&A | ($25M) | ($27M) | ($30M) | +11% | 5% |
| **EBITDA** | **$90M** | **$110M** | **$145M** | **+32%** | **24%** ⬆ |
| D&A | ($15M) | ($18M) | ($22M) | +22% | 4% |
| **EBIT** | **$75M** | **$92M** | **$123M** | **+34%** | **20%** |
| Interest | ($5M) | ($6M) | ($7M) | +17% | 1% |
| Tax | ($21M) | ($26M) | ($35M) | +35% | 6% |
| **Net Income** | **$49M** | **$60M** | **$81M** | **+35%** | **13%** |

**Highlights:**
- Gross Profit row: Background #E8F5E9, Bold
- EBITDA row: Background #E8F5E9, 12pt Bold, 2pt borders
- Net Income: Background #C8E6C9 (darker), 12pt Bold, 3pt borders
- Variance >20%: Bold e colored (green ou red)
- Arrows ⬆⬇ na coluna % Rev: Comparação vs industry benchmark (52% gross margin ⬆ acima de 48% peers)

---

### WATERFALL CHART (Financial Bridge)

**Quando usar:**
- Explicar variance (YoY, budget vs actual, target gaps)
- P&L walkdown
- Value creation in M&A

**Especificações (já detalhadas em template_data_slide, aqui specific to finance):**

**Financial waterfall specifics:**

**Start bar:**
- Label: "FY2023 EBITDA $110M"
- Color: #003B5C
- Full height de zero

**Positive drivers (green bars, floating):**
- Revenue growth: +$42M
- Margin expansion: +$18M
- Cost savings: +$12M
- Colors: #00A86B

**Negative drivers (red bars, floating):**
- Wage inflation: -$15M
- Investment in growth: -$22M
- Colors: #D32F2F

**End bar:**
- Label: "FY2024 EBITDA $145M"
- Color: #003B5C
- Full height

**Labels:**
- Valores: Acima de cada bar, "+$XXM" ou "-$XXM", 11pt Bold
- Sub-labels (opcional): Breakdown dentro do bar se múltiplos componentes

**Connectors:**
- Dashed lines (1pt, #6E6E6E) conectando bars

**Net change callout:**
- Box: "Net: +$35M (+32%)"
- Position: Top-right da chart
- Background: #E8F5E9, border 2pt #00A86B
- Font: 12pt Bold

---

### ROI/BUSINESS CASE TABLE

**Quando usar:**
- Investment approval
- Program business case
- Payback analysis

**Estrutura:**

**Investment section (top):**
| Item | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|------|--------|--------|--------|--------|-------|
| Technology | ($50M) | ($20M) | ($10M) | $0 | ($80M) |
| People/Training | ($10M) | ($5M) | $0 | $0 | ($15M) |
| **Total Investment** | **($60M)** | **($25M)** | **($10M)** | **$0** | **($95M)** |

**Benefits section:**
| Benefit | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|---------|--------|--------|--------|--------|-------|
| Revenue uplift | $0 | $20M | $50M | $80M | $150M |
| Cost reduction | $0 | $15M | $30M | $45M | $90M |
| **Total Benefits** | **$0** | **$35M** | **$80M** | **$125M** | **$240M** |

**Net cash flow:**
| Item | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|------|--------|--------|--------|--------|-------|
| **Net Cash Flow** | **($60M)** | **$10M** | **$70M** | **$125M** | **$145M** |
| **Cumulative** | ($60M) | ($50M) | $20M | $145M | - |

**Metrics (below table):**
- **Payback Period:** 1.7 years (when cumulative turns positive)
- **ROI:** 153% (Total Benefits / Total Investment - 1)
- **NPV @ 10% discount:** $98M
- **IRR:** 42%

**Formatting:**
- Investment rows: Red text #D32F2F (cash out)
- Benefit rows: Green text #00A86B (cash in)
- Net cash flow: Bold, black
- Cumulative: Italic, conditional color (negative red, positive green)
- Metrics box: Background #FFFDE7, border 2pt #FBC02D left, 11pt Bold

---

### CASH FLOW STATEMENT

**Estrutura (simplified):**

| Cash Flow Item | 2023 | 2024E | Variance |
|----------------|------|-------|----------|
| **Operating Activities** | | | |
| Net Income | $60M | $81M | +$21M |
| D&A | $18M | $22M | +$4M |
| Change in Working Capital | ($15M) | $8M | +$23M |
| **Cash from Operations** | **$63M** | **$111M** | **+$48M** |
| **Investing Activities** | | | |
| CAPEX | ($35M) | ($42M) | ($7M) |
| Acquisitions | ($20M) | $0 | +$20M |
| **Cash from Investing** | **($55M)** | **($42M)** | **+$13M** |
| **Financing Activities** | | | |
| Debt issuance/(repayment) | $10M | ($15M) | ($25M) |
| Dividends | ($12M) | ($15M) | ($3M) |
| **Cash from Financing** | **($2M)** | **($30M)** | **($28M)** |
| **Net Change in Cash** | **$6M** | **$39M** | **+$33M** |
| Cash, beginning | $45M | $51M | - |
| **Cash, ending** | **$51M** | **$90M** | **+$39M** |

**Key highlights:**
- Cash from Operations: Background #E8F5E9 (green - most important)
- Free Cash Flow (= Operations - CAPEX): Calculated e highlighted
  - FCF 2024: $111M - $42M = $69M (callout box)
- Net Change: Bold, 12pt

---

## KEY METRICS DASHBOARD (Financial)

**Purpose:** Quick snapshot de saúde financeira

**Layout:** 2×3 ou 3×2 grid

**Metric tiles:**

**Tile structure:**
- Size: 3-4cm × 2-2.5cm
- Border: 2pt, color-coded
- Background: White ou subtle color

**Content per tile:**
- **Metric name:** Top, 9pt Regular, #6E6E6E
- **Value:** Center, 24-28pt Bold, #003B5C
- **Trend:** Bottom, 10pt Regular com arrow
  - Format: "↑ +12% vs PY" (green #00A86B)
  - OR: "↓ -8% vs target" (red #D32F2F)
- **Sparkline (opcional):** Mini line chart (last 6-12 periods), 1cm × 0.5cm

**Example tiles:**

**Tile 1: Revenue**
- Name: "Revenue (LTM)"
- Value: "$615M"
- Trend: "↑ +18% YoY" (green)
- Sparkline: Ascending trend

**Tile 2: EBITDA Margin**
- Name: "EBITDA Margin"
- Value: "24%"
- Trend: "↑ +4pp YoY" (green)
- Border: #00A86B (green - good performance)

**Tile 3: Free Cash Flow**
- Name: "Free Cash Flow"
- Value: "$69M"
- Trend: "↑ +85% YoY"

**Tile 4: Net Debt / EBITDA**
- Name: "Net Debt / EBITDA"
- Value: "2.1×"
- Trend: "↓ from 2.8×" (green - improving)

**Tile 5: ROE**
- Name: "Return on Equity"
- Value: "18%"
- Trend: "Top quartile" (benchmark)

**Tile 6: DSO**
- Name: "Days Sales Outstanding"
- Value: "45 days"
- Trend: "↓ from 58 days" (green - improving)

---

## ASSUMPTIONS & FOOTNOTES (Critical for financial slides!)

**Position:** Bottom area, Linha 7.5-7.9 OU dedicated small section

**Format:**
"Assumptions: [List key assumptions]
Notes: [Accounting standards, methodology, exclusions]"

**Example:**
"Assumptions: (1) Revenue growth 15% CAGR 2024-2027 based on pipeline analysis; (2) Gross margin expansion 2pp annually via automation; (3) Forex USD/EUR 1.10 (constant); (4) No major M&A; (5) Tax rate 30% effective
Notes: (1) EBITDA excludes one-time restructuring charges $12M in 2024; (2) GAAP basis; (3) Constant currency analysis for organic growth"

**Specs:**
- Font: 8-9pt Regular, #6E6E6E
- Line height: 1.3
- Max width: 95% do slide
- Background (opcional): #FAFAFA para destacar

---

## CHECKLIST - FINANCIAL SLIDE

**Accuracy:**
- [ ] Numbers foot (rows sum correctly)?
- [ ] Variance calculations correct?
- [ ] Units consistent ($M vs $K vs $)?
- [ ] Decimals appropriate (0-1 places)?
- [ ] Negative numbers formatted correctly?

**Assumptions:**
- [ ] Key assumptions documented?
- [ ] Methodology explained (GAAP vs non-GAAP)?
- [ ] One-time items called out?
- [ ] Foreign exchange approach stated?
- [ ] Sources cited (audited financials vs management)?

**Visual:**
- [ ] Key metrics highlighted (color/bold)?
- [ ] Positive/negative clearly distinguished (green/red)?
- [ ] Borders emphasize hierarchy?
- [ ] Zebra striping aids readability?
- [ ] Not overwhelming (max 20 rows)?

**Comparisons:**
- [ ] Benchmarks included (vs peers, vs budget)?
- [ ] Variance drivers explained?
- [ ] Trend clear (multi-period view)?
- [ ] Outliers annotated?

**Credibility:**
- [ ] Conservative assumptions (não overly optimistic)?
- [ ] Sensitivity analysis (se business case)?
- [ ] Risks/downsides acknowledged?
- [ ] Board/CFO review completed?

---

## SENSITIVITY ANALYSIS (Tornado Chart)

**Purpose:** Show impact of key variables

**Structure:**
- Horizontal bars: Cada variável (ex: Revenue growth, Margin, Discount rate)
- X-axis: Impact em NPV ou ROI (ex: $50M to $150M)
- Centerline: Base case (ex: $100M NPV)
- Bar extends left (downside scenario) e right (upside scenario)
- Colors: Downside #D32F2F (red), Upside #00A86B (green)
- Order: Largest range at top (most impactful variable)

**Example:**
- Revenue growth: Downside $75M (-25%) to Upside $130M (+30%) = $55M range
- Gross margin: $85M to $118M = $33M range
- Discount rate: $92M to $109M = $17M range

---

**VERSÃO:** 1.0
**OWNER:** GPT McKinsey PPT Architect
**ÚLTIMA ATUALIZAÇÃO:** Dezembro 2024
