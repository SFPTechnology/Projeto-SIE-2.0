# KB_09: Financial Services - Banking, Insurance, Asset Management

## KPIs Principais e Benchmarks

### Banking Core Metrics

**Net Interest Margin (NIM):**
- Fórmula: (Interest Income - Interest Expense) / Average Earning Assets
- Benchmark: 3.0-3.5% (bancos tradicionais), 2.0-2.5% (fintechs)
- Tendência: Compressão contínua com digital banking

**Cost-to-Income Ratio (CIR):**
- Fórmula: Operating Expenses / Operating Income
- Excelente: <50%
- Bom: 50-60%
- Preocupante: >60%
- Digital banks: 30-40%

**Return on Equity (ROE):**
- Benchmark: 12-15% (sustentável)
- Top quartile: >15%
- Below par: <10%

**Non-Performing Loan Ratio (NPL):**
- Saudável: <2%
- Atenção: 2-5%
- Crítico: >5%

**Tier 1 Capital Ratio:**
- Mínimo regulatório: 6% (Basel III)
- Well-capitalized: >10%
- Top banks: 12-14%

**Customer Acquisition Cost (CAC):**
- Branch banking: $200-400
- Digital only: $50-150
- Payback period ideal: <12 meses

**Lifetime Value (LTV):**
- Banking retail: $500-2,000
- Private banking: $10,000-50,000
- Corporate: $50,000-500,000
- Ratio LTV:CAC ideal: >3:1

### Insurance Metrics

**Combined Ratio:**
- Fórmula: (Claims + Expenses) / Premiums
- Excelente: <90%
- Break-even: 100%
- Unprofitable: >100%

**Loss Ratio:**
- P&C insurance: 60-70%
- Life insurance: 70-85%

**Surrender Rate:**
- Saudável: <5% ao ano
- Preocupante: >10%

### Asset Management

**Assets Under Management (AUM):**
- Growth rate benchmark: 8-12% ao ano
- Fee compression: -10 to -20 bps annually

**Net Flows:**
- Positivo: Nova captação > Resgates
- Breakout success: >$1B/trimestre (large players)

**Fee Rate:**
- Active funds: 50-100 bps
- Passive/Index: 5-20 bps
- Alternative/PE: 150-200 bps + performance

## Frameworks Específicos

### RAROC (Risk-Adjusted Return on Capital)

**Conceito:** Retorno ajustado pelo risco de cada linha de negócio

**Fórmula:**
```
RAROC = (Expected Return - Expected Loss) / Economic Capital
```

**Aplicação:**
- Alocação de capital entre BUs
- Pricing de produtos
- Decisões de portfólio

**Slide tipo:**
**Título:** "RAROC de corporate lending (18%) supera retail (12%), justificando realocação de capital"

**Visual:** Bar chart comparativo
- 5-7 linhas de negócio
- RAROC % de cada
- Hurdle rate marcado (ex: 15%)
- Barras acima = verde, abaixo = vermelho

### Credit Risk Modeling

**PD, LGD, EAD:**
- **PD** (Probability of Default): 0.5-5% dependendo de rating
- **LGD** (Loss Given Default): 40-60% média
- **EAD** (Exposure at Default): Drawn + % of undrawn

**Expected Loss = PD × LGD × EAD**

### Open Banking & BaaS (Banking as a Service)

**Conceito:** APIs abertas para third parties acessarem dados bancários

**Oportunidades:**
- Novos revenue streams (API fees)
- Melhor customer experience (agregação)
- Embedded finance (checkout, BNPL)

**Riscos:**
- Disintermediation
- Data security
- Regulatory compliance

## Terminologia Especializada

**AML/KYC:** Anti-Money Laundering / Know Your Customer
**CET1:** Common Equity Tier 1 (capital mais confiável)
**CVA/DVA:** Credit/Debit Valuation Adjustment
**VaR:** Value at Risk (99% confidence, 1-day horizon típico)
**Stress Testing:** Simulação de cenários adversos (regulatório)
**CCAR:** Comprehensive Capital Analysis and Review (Fed)
**IFRS 9:** International standard de contabilidade (expected credit loss)
**RWA:** Risk-Weighted Assets
**ALCO:** Asset-Liability Committee
**FDIC:** Federal Deposit Insurance Corporation
**Dodd-Frank:** Lei regulatória US pós-2008
**MiFID II:** Markets in Financial Instruments Directive (Europa)
**PSD2:** Payment Services Directive 2 (open banking Europa)
**BNPL:** Buy Now Pay Later
**DeFi:** Decentralized Finance
**Stablecoin:** Crypto atrelada a moeda fiat
**Tokenization:** Representação digital de assets
**RegTech:** Technology para compliance regulatório
**SupTech:** Supervisory technology (reguladores)
**Neobank:** Digital-only bank sem agências
**Challenger bank:** Banco novo competindo com incumbentes

## Paleta de Cores Financial Services

**Institucional/Confiança:**
- Navy Blue: #001F3F (primário - solidez)
- Forest Green: #00563F (secundário - crescimento)
- Gold: #D4AF37 (accent - premium)

**Digital/Fintech:**
- Electric Blue: #0066FF
- Bright Cyan: #00E5FF
- Purple: #6C63FF

**Alertas e Risk:**
- Red (high risk): #D32F2F
- Yellow (medium): #FBC02D
- Green (low): #388E3C

**Neutrals:**
- Charcoal: #263238
- Silver: #B0BEC5
- White: #FFFFFF

## Tipos de Gráficos Mais Usados

### Waterfall Chart
**Quando usar:** Explicar mudanças em métricas financeiras
**Exemplo:** "ROE caiu de 15% para 12%: breakdown de drivers"
- Start: 15% ROE 2023
- -2% (NIM compression)
- -1% (Credit losses)
- +0.5% (Cost reduction)
- -0.5% (Lower volumes)
- End: 12% ROE 2024

### Funnel Chart
**Quando usar:** Customer acquisition, loan approval process
**Exemplo:** "$100M em applications → $60M approved → $40M funded"
- Stages: Application → Credit Check → Underwriting → Approval → Funding
- Conversion rate em cada estágio
- Drop-off reasons anotados

### Cohort Analysis (Heatmap)
**Quando usar:** Retention, churn, vintage analysis
**Exemplo:** Loan performance por vintage (ano de origination)
- Rows: Vintages (2020, 2021, 2022, 2023)
- Columns: Months since origination
- Color: NPL rate (verde <2%, amarelo 2-5%, vermelho >5%)

### Scenario Analysis (Tornado Chart)
**Quando usar:** Sensitivity analysis, stress testing
**Exemplo:** "Impacto de variáveis macro em ROE"
- Variables: Interest rates, GDP growth, Unemployment, FX
- Range: Base case ±1-2 standard deviations
- Visual: Horizontal bars mostrando swing

## Action Titles - Exemplos Financial Services

❌ "Análise de rentabilidade por produto"
✅ "Corporate lending entrega RAROC de 18%, 6pp acima de retail, justificando shift de capital"

❌ "Performance de NIM"
✅ "NIM comprimiu 40bps em 2 anos devido a competição digital, exigindo repricing urgente"

❌ "Métricas de aquisição"
✅ "CAC digital ($80) é 75% menor que branch ($320), acelerando shift para mobile-first"

❌ "Risco de crédito"
✅ "NPL subiu de 2.1% para 3.8% em portfolio de SME, requerendo $50M em provisões adicionais"

❌ "Resultados de stress test"
✅ "Severe stress scenario depleta CET1 de 12% para 9.2%, ainda 320bps acima de mínimo regulatório"

## Compliance e Regulação

### Basel III/IV
**Capital requirements:**
- CET1 minimum: 4.5%
- Tier 1 minimum: 6%
- Total capital: 8%
- Capital conservation buffer: +2.5%
- Countercyclical buffer: 0-2.5%
- G-SIB surcharge: 1-3.5%

### AML/CFT (Anti-Money Laundering / Counter Financing of Terrorism)
**Red flags:**
- Transações estruturadas (<$10k para evitar reporting)
- Wire transfers para high-risk jurisdictions
- Cash-intensive businesses
- PEPs (Politically Exposed Persons)

### GDPR / LGPD
**Impacto em banking:**
- Consent para data usage
- Right to be forgotten
- Data portability (open banking)
- Multas: até 4% do revenue global

## Benchmarks por Segmento

### Retail Banking
- Branches per 100k inhabitants: 10-30
- ATMs per 100k: 20-60
- Digital adoption: 60-80% dos customers
- Mobile transactions: >50% do total

### Corporate Banking
- Wallet share (% of client's banking): 20-40%
- Cross-sell ratio: 3-5 produtos por cliente
- Relationship tenure: 8-15 anos

### Private Banking
- AUM per relationship manager: $100-250M
- Clients per RM: 40-80
- Fee rate: 80-150 bps
- Referral rate: 20-30% de new clients

### Wealth Management
- Digital engagement: 40-60% use robo-advisory
- ESG assets: 25-35% e crescendo
- Alternative allocations: 10-20% de portfolio

## Slide Specifications - Financial Services

### Título Action-Oriented
14-18 palavras, insight primeiro, números de suporte

### Body
- Max 3-4 bullets por slide
- Dados quantitativos sempre
- Comparação com benchmarks

### Chart
- Waterfall para P&L walkdowns
- Scatter para risk-return tradeoffs
- Heatmap para vintage/cohort analysis
- Bridge para capital movements

### Fonte de Dados
**Exemplo completo:**
"Fonte: Internal P&L database (Q4 2024); SNL Financial para peer benchmarks (accessed Jan 2025); Basel Committee on Banking Supervision - 'Basel III Monitoring Report' (Dec 2024), disponível em https://www.bis.org/bcbs/publ/d567.pdf; Company analysis"

### Notas de Rodapé
Definições, assumptions, exclusões:
"(1) RAROC calculado usando economic capital modelo interno aprovado em 2023
(2) Peer group: 15 bancos regionais com AUM $50-200B
(3) NPL ratio exclui portfolios acquired em M&A (3 anos seasoning period)"
