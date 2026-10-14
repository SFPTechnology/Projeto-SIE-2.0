# Template: Appendix/Supporting Slide

## Purpose
Fornecer informações detalhadas, dados adicionais, metodologias, supporting analysis sem sobrecarregar slides principais. Servir como reference material.

---

## SLIDE SPECIFICATION - APPENDIX SLIDE

### PAGE NUMBER
**Posição:** Rodapé direito
**Coordenadas:** Coluna 11.5-12, Linha 7.9
**Formato:** "A-[número]" (ex: "A-1", "A-2", "A-15")
**Fonte:** Helvetica Neue Regular, 10pt, #6E6E6E

**IMPORTANTE:** Appendix slides NÃO contam na numeração principal (slides 1-50 main deck, depois A-1 to A-X appendix)

---

### HEADER
**Posição:** Topo
**Coordenadas:** Colunas 1-12, Linha 0.8-1

**Formato:**
"APPENDIX | [Tópico do slide]"

OU (se appendix section específica):
"APPENDIX - METHODOLOGY | [Specific topic]"

**Exemplo:**
"APPENDIX | Detailed Market Sizing Assumptions"
"APPENDIX - DATA SOURCES | Customer Survey Methodology"

**Especificações:**
- Fonte: Helvetica Neue Bold, 14-16pt
- Cor: #6E6E6E (não #003B5C - visual cue que é appendix, não main content)
- Separator: " | " entre "APPENDIX" e topic
- Alignment: Left

**Visual cue (opcional mas recommended):**
- Top border: 3pt, #B0BEC5 (gray), full width
- Background top strip: #F5F5F5, height 0.5cm

---

## APPENDIX CATEGORIES & FORMATS

### CATEGORY 1: DETAILED DATA TABLES

**Quando usar:**
- Raw data supporting charts in main deck
- Detailed breakdowns (by geography, product, time period)
- Full datasets (main deck showed summary)

**Especificações:**

**Table structure:**
- Can be denser than main deck tables (mais rows/columns OK)
- Font: 9-10pt (slightly smaller acceptable)
- Zebra striping: Mandatory (aids scanning)
- Borders: 1pt #E0E0E0 (subtle)
- Header: Background #F5F5F5, 10pt Bold

**Max dimensions:**
- Rows: 25-30 (se mais, quebrar em múltiplos slides "A-1a, A-1b")
- Columns: 10-12 (se mais, rotate ou quebrar)

**Example:**
**Title:** "APPENDIX | Revenue by Product Line, Geography, and Customer Segment (2022-2024)"

**Table:** 3-way breakdown
- Rows: 20 product-geography combinations
- Columns: 2022 | 2023 | 2024 | CAGR | % of Total
- Format: $M, 1 decimal
- Highlights: Top 5 combinations em bold

---

### CATEGORY 2: METHODOLOGY & ASSUMPTIONS

**Quando usar:**
- Explicar calculations
- Document assumptions
- Statistical methods
- Data collection approach

**Formato:**

**Section headers:**
- "1. Data Collection"
- "2. Analysis Approach"
- "3. Key Assumptions"
- "4. Limitations"

**Content:**
- Bullets: 10-11pt Regular
- Sub-bullets: Indented, 9-10pt
- Formulas: Monospace font (Courier New), 10pt, background #F5F5F5
- References: 8pt, italics

**Example:**

**Title:** "APPENDIX - METHODOLOGY | Customer LTV Calculation"

**Section 1: Formula**
```
LTV = (Monthly Revenue per Customer × Gross Margin % × Avg Lifetime in Months)
    = (ARPU × GM% × (1 / Monthly Churn Rate))
```

**Section 2: Assumptions**
• ARPU calculated as total MRR / active customers (excludes free tier)
• Gross margin: 78% (company-wide average, excludes S&M and G&A)
• Churn rate: 12-month trailing average (2.1% monthly)
• Cohort: Customers acquired Jan 2023-Dec 2023 (n=2,450)

**Section 3: Limitations**
• Does not account for expansion revenue (upsell/cross-sell)
• Assumes constant churn rate (historically 1.8-2.4% range)
• Excludes customer acquisition cost (CAC) - see separate analysis slide A-5

---

### CATEGORY 3: DETAILED CHARTS & ANALYSIS

**Quando usar:**
- Deep-dive charts não essenciais para main story
- Alternative views of same data
- Segmentation analysis
- Outlier analysis

**Formato:**
- Similar to main deck data slides BUT:
  - Can have 2 charts per slide (vs 1 principal em main deck)
  - Smaller fonts acceptable (10pt vs 11-12pt)
  - Less white space (denser OK)

**Example:**

**Title:** "APPENDIX | Revenue Growth Drivers - Detailed Decomposition"

**Chart 1 (left half):** Waterfall breakdown
- Showing 12 components (vs 5 em main deck)
- Smaller bars, 9pt labels

**Chart 2 (right half):** Time series
- Monthly view (vs quarterly em main deck)
- 36 data points, 9pt axis labels

---

### CATEGORY 4: BENCHMARKING & COMPARABLES

**Quando usar:**
- Peer comparison details
- Industry benchmarks
- Market comps
- Valuation multiples

**Formato:**

**Comparison table:**
- Rows: Peers/comparables (15-25 companies)
- Columns: Key metrics (Revenue, EBITDA Margin, Growth, Valuation, etc.)
- Sorting: By most relevant metric (ex: descending market cap)
- Highlight: Subject company em bold, background #FFFDE7 (light yellow)

**Quartile markers:**
- Top quartile: Shaded #E8F5E9 (light green)
- Bottom quartile: Shaded #FFEBEE (light red)
- Median line: Dashed, across table

**Example:**

**Title:** "APPENDIX - BENCHMARKING | SaaS Peer Comparison (Public Companies >$500M Market Cap)"

| Company | Revenue | Growth | EBITDA Margin | NRR | EV/Revenue |
|---------|---------|--------|---------------|-----|------------|
| Peer A | $2,500M | 45% | 28% | 130% | 15.2× |
| Peer B | $1,800M | 38% | 22% | 118% | 12.5× |
| **[COMPANY]** | **$615M** | **32%** | **24%** | **125%** | **10.8×** |
| Peer C | $850M | 28% | 18% | 112% | 8.5× |
| ... | | | | | |
| **Median** | **$1,250M** | **32%** | **23%** | **120%** | **11.2×** |
| **Top Quartile** | - | 42% | 27% | 128% | 14.0× |

**Highlights:**
- Subject company: Yellow background
- Metrics > median: Bold green
- Metrics < median: Regular black

---

### CATEGORY 5: SURVEY/INTERVIEW RESULTS

**Quando usar:**
- Customer research findings
- Employee survey results
- Expert interview summaries

**Formato:**

**Survey snapshot:**
- Sample: "n=1,250 customers (response rate 34%)"
- Period: "Conducted Nov 15-30, 2024"
- Method: "Online survey, 15 questions, avg completion 8 min"

**Results visualization:**
- Horizontal bar charts (% respondents)
- Pie charts (segmentation)
- Quotes: Callout boxes, italic, 10pt

**Example:**

**Title:** "APPENDIX - VOICE OF CUSTOMER | Survey Results - Product Satisfaction"

**Sample details:**
n=1,250 | Response rate 34% | Nov 15-30, 2024 | Margin of error ±2.8%

**Q1: Overall satisfaction (1-5 scale)**
- Very Satisfied (5): 42% ████████████████████
- Satisfied (4): 38% ███████████████
- Neutral (3): 12% ████████
- Dissatisfied (2): 6% ███
- Very Dissatisfied (1): 2% █

**Mean: 4.1 | Top-2-Box: 80% (↑ from 72% in 2023)**

**Q2: Most valued features (select top 3)**
- Ease of use: 68%
- Integration capabilities: 54%
- Customer support: 48%
- Pricing: 42%
- Mobile app: 35%

**Verbatim quotes:**
> "The platform is intuitive, but mobile experience needs work" - Enterprise customer, Financial Services

> "Support team is responsive, typically <2h response time" - Mid-market customer, Healthcare

---

### CATEGORY 6: RISK MATRIX & MITIGATION

**Quando usar:**
- Detailed risk assessment
- Mitigation plans
- Scenario analysis

**Formato:**

**Risk matrix (2×2):**
- X-axis: Likelihood (Low → High)
- Y-axis: Impact (Low → High)
- Quadrants: Color-coded
  - High Impact, High Likelihood: #FFEBEE (red - priority)
  - High Impact, Low Likelihood: #FFF9E6 (yellow - monitor)
  - Low Impact, High Likelihood: #E3F2FD (blue - manage)
  - Low Impact, Low Likelihood: #F5F5F5 (gray - accept)

**Risk items:**
- Bubbles on matrix
- Size: Proportional to potential $ impact
- Label: Risk ID (R1, R2, etc.)

**Risk table (below matrix):**
| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|----|------|------------|--------|------------|-------|
| R1 | Vendor delay | Medium | High | Dual source, buffer time | PMO |
| R2 | Regulatory change | Low | High | Legal monitoring, flexibility | Compliance |

---

### CATEGORY 7: GLOSSARY & DEFINITIONS

**Quando usar:**
- Technical terms
- Industry jargon
- Acronyms
- Metric definitions

**Formato:**

**Alphabetical list:**
- Term: 11pt Bold
- Definition: 10pt Regular
- Example (optional): 9pt Italic, indented

**2-column layout** (para economizar espaço):
- Left column: A-M
- Right column: N-Z

**Example:**

**Title:** "APPENDIX - GLOSSARY | Key Terms & Definitions"

**ARR (Annual Recurring Revenue)**
Annualized value of recurring subscription contracts. Calculated as MRR × 12.
_Example: Customer with $10K/month subscription = $120K ARR_

**CAC (Customer Acquisition Cost)**
Total sales & marketing expense divided by number of new customers acquired in period.
_Includes: salaries, ads, events, tools. Excludes: customer success, support_

**Churn Rate**
Percentage of customers who cancel in a period. Calculated as churned customers / customers at start.
_Monthly churn 2% = 1 - (1 - 0.02)^12 = 21.5% annual churn_

---

### CATEGORY 8: DETAILED PROCESS FLOWS

**Quando usar:**
- Step-by-step processes
- Detailed workflows
- System architecture
- Decision trees

**Formato:**
- Swimlane diagrams (por role/system)
- Flowcharts (decision logic)
- Sequence diagrams (system interactions)

**Visual specs:**
- Shapes: Rectangle (process), Diamond (decision), Rounded (start/end)
- Connectors: 2pt arrows
- Colors: By actor/system
- Labels: 9pt, inside shapes

**Can be denser than main deck** (mais steps, smaller boxes)

---

## LAYOUT VARIATIONS

### DENSE DATA LAYOUT
**Para maximum information:**
- Margins: Reduced to 0.8cm (vs 1.5cm main deck)
- Font: 9-10pt (vs 11-12pt)
- Line height: 1.3 (vs 1.5)
- White space: Minimal
- Grid: Can violate 12×8 grid se necessário

### REFERENCE PAGE LAYOUT
**Para quick lookup:**
- Large table: Full slide
- Small header: Just "APPENDIX | Topic"
- No page number limit (pode ter A-1 through A-50 se needed)

---

## NAVIGATION & CROSS-REFERENCE

### LINKING TO APPENDIX (from main deck)

**In main deck slide:**
- Small superscript reference: "See detailed analysis^A-5"
- Hyperlinked (if digital deck)
- Font: 8pt, #1976D2 (blue = link)

**Footer in appendix slides:**
"Related main deck slide: Slide 12 - Revenue Analysis"

### APPENDIX TABLE OF CONTENTS

**If >10 appendix slides, create TOC as slide A-0:**

**Title:** "APPENDIX - TABLE OF CONTENTS"

**Format:**
A-1: Detailed Market Sizing Assumptions
A-2: Customer Survey Methodology & Results
A-3-A-5: Revenue Analysis by Segment (3 slides)
A-6: Peer Benchmarking - Full Dataset
A-7: Risk Assessment & Mitigation Plans
A-8-A-10: Financial Model Details (3 slides)
A-11: Glossary of Terms
A-12: Data Sources & Bibliography

**Hyperlinked** (each item clicks to that slide)

---

## VISUAL DIFFERENTIATION FROM MAIN DECK

**Consistent markers que isto é appendix:**

1. **Header styling:**
   - Always includes "APPENDIX" prefix
   - Gray tone (#6E6E6E) vs navy (#003B5C)
   - Top border gray vs navy

2. **Page numbers:**
   - "A-X" format vs "X"
   - Position: Same (consistency) but format different

3. **Density:**
   - Visibly denser (mais content per slide)
   - Smaller fonts acceptable
   - Less white space

4. **Polish:**
   - Less polished OK (não apresentável orally)
   - Focus on completeness vs aesthetics
   - Charts can be "rougher" (Excel screenshots acceptable se clear)

---

## SOURCES & CITATIONS (Even More Critical in Appendix)

**Format:**
"Sources: [Detailed list with dates, access info, page numbers]"

**Example:**
"Sources:
1. Company internal financials, audited by EY (FY 2022-2024), accessed via CFO office Dec 2024
2. Gartner Magic Quadrant for CRM, published Oct 15, 2024, available at https://www.gartner.com/doc/4822615, accessed Dec 10, 2024, p.12-18
3. Customer survey conducted by [Firm] Nov 15-30, 2024, n=1,250, response rate 34%, margin of error ±2.8% at 95% confidence
4. Industry benchmarks from SaaS Capital Index, Q3 2024 report, https://www.saas-capital.com/research, Table 5
5. Expert interviews with 8 industry practitioners, conducted Nov 2024 (anonymized per confidentiality agreements)"

**Position:** Bottom margin, 7-8pt, #B0B0B0

---

## CHECKLIST - APPENDIX SLIDE

**Organization:**
- [ ] Clearly labeled "APPENDIX"?
- [ ] Page numbered "A-X" format?
- [ ] Linked from main deck (se relevant)?
- [ ] Grouped logically (all methodology together, etc)?
- [ ] TOC provided se >10 appendix slides?

**Content:**
- [ ] Adds value (não duplicativo)?
- [ ] Too detailed for main deck mas relevant?
- [ ] Sources fully documented?
- [ ] Methodology explained?
- [ ] Assumptions stated?

**Formatting:**
- [ ] Visually distinguido de main deck?
- [ ] Readable (even if dense)?
- [ ] Tables properly formatted?
- [ ] Charts labeled?
- [ ] Definitions clear?

**Reference:**
- [ ] Cross-references work (links active)?
- [ ] Related main slide noted?
- [ ] Standalone understandable?

---

## COMMON APPENDIX SLIDE TYPES - QUICK REFERENCE

**A-1: Full dataset** (main deck showed summary)
**A-2: Methodology** (how we calculated key metrics)
**A-3: Assumptions** (what we assumed, why)
**A-4-A-6: Sensitivity analysis** (scenarios, what-ifs)
**A-7: Peer benchmarking detail** (full comps table)
**A-8: Survey/interview details** (verbatims, full results)
**A-9-A-10: Detailed process flows** (step-by-step)
**A-11: Risk matrix** (all risks, not just top 5)
**A-12: Financial model** (full P&L, balance sheet, cash flow)
**A-13: Glossary** (terms, acronyms, definitions)
**A-14: Bibliography** (all sources, links, citations)

---

## EXAMPLE APPENDIX SLIDE - COMPLETE SPEC

**SLIDE A-3: METHODOLOGY - MARKET SIZING**

**Header:**
- Text: "APPENDIX - METHODOLOGY | Total Addressable Market (TAM) Sizing Approach"
- Font: Helvetica Neue Bold, 14pt, #6E6E6E
- Top border: 3pt #B0BEC5, full width

**Section 1: Approach (Linhas 1.5-3)**
We used a bottom-up approach combining three data sources:
1. Government census data (total # of target businesses)
2. Industry surveys (penetration rates, avg spend)
3. Company sales data (validation, actual customer spend)

**Section 2: Calculation (Linhas 3-5)**
```
TAM = # Target Businesses × Penetration Rate × ARPU × 12 months
    = 250,000 businesses × 35% penetration × $4,200 ARPU × 12
    = $4.4 Billion
```

**Section 3: Assumptions (Linhas 5-6.5)**
• Target businesses: US companies 50-500 employees in sectors: Professional Services, Healthcare, Financial Services (SIC codes 70XX, 80XX, 60XX)
• Penetration: 35% based on Gartner survey 2024 (avg of 3-year adoption rates)
• ARPU: $4,200/month based on our mid-market tier pricing × 1.2 (accounts for upsells)
• Geography: US only (international TAM separate analysis - see slide A-4)

**Section 4: Validation (Linhas 6.5-7.5)**
Cross-check with top-down:
• Industry analyst reports (Gartner, Forrester) estimate $4.0-4.8B TAM → Our $4.4B within range ✓
• Our current market share: $615M / $4.4B = 14% (plausible given competitive landscape)

**Sources (Bottom margin):**
"Sources: (1) US Census Bureau, Statistics of U.S. Businesses 2023, accessed Dec 2024; (2) Gartner Inc., 'Market Analysis: CRM Software Adoption,' published Sep 2024; (3) Company internal sales database (2024 FY); (4) Forrester Research, 'CRM Market Forecast 2024-2027,' Mar 2024"

**Page number:** "A-3" - bottom right

---

**VERSÃO:** 1.0
**OWNER:** GPT McKinsey PPT Architect
**ÚLTIMA ATUALIZAÇÃO:** Dezembro 2024
