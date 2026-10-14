# KB_13: Manufacturing & Industrial - Operations, Lean, Industry 4.0

## Overall Equipment Effectiveness (OEE)

### The Gold Standard Metric

**Fórmula:**
```
OEE = Availability × Performance × Quality
```

**Breakdown:**

**Availability:**
```
Availability = Operating Time / Planned Production Time
```
- Operating Time = Planned Time - Downtime (breakdowns, changeovers)
- Benchmark: >90%

**Performance:**
```
Performance = (Actual Output / Theoretical Max Output)
```
- Theoretical = Ideal cycle time × Operating time
- Benchmark: >95%

**Quality:**
```
Quality = Good Units / Total Units Produced
```
- Good units = No rework, no defects
- Benchmark: >99%

**OEE Total:**
- World-class: >85%
- Good: 70-85%
- Average: 60-70%
- Needs improvement: <60%

**Six Big Losses que impactam OEE:**
1. **Breakdowns** (Availability)
2. **Setup/Changeovers** (Availability)
3. **Small stops** (Performance)
4. **Reduced speed** (Performance)
5. **Startup rejects** (Quality)
6. **Production rejects** (Quality)

**Slide tipo:**
**Título:** "OEE aumentou de 68% para 82% em 12 meses via TPM, liberando 15% capacity adicional ($8M value)"

### TEEP (Total Effective Equipment Performance)

**Diferença vs OEE:**
- OEE usa Planned Production Time
- TEEP usa Calendar Time (24/7/365)

**Fórmula:**
```
TEEP = OEE × Utilization
Utilization = Planned Production Time / Calendar Time
```

**Exemplo:**
- OEE: 75%
- Utilization: 60% (factory runs 1 shift + weekends off)
- TEEP: 75% × 60% = 45%

**Insight:** Revela underutilization vs pure efficiency

## Lean Manufacturing

### The 7 Wastes (Muda)

1. **Transportation:** Movimento desnecessário de materiais
   - Impact: +5-10% de custo logístico
   - Solution: Layout optimization, milk runs

2. **Inventory:** Excess WIP, raw materials, finished goods
   - Impact: Tied capital, obsolescence risk
   - Target: <30 dias (pull system)

3. **Motion:** Movimento desnecessário de pessoas
   - Impact: Ergonomia, tempo perdido
   - Solution: 5S, standard work

4. **Waiting:** Idle time (pessoas ou máquinas)
   - Impact: Lost productivity
   - Solution: Heijunka (level loading)

5. **Overproduction:** Produzir além da demanda
   - Impact: Worst waste (cria outros wastes)
   - Solution: JIT, kanban

6. **Over-processing:** Fazer mais que o necessário
   - Impact: Tempo + custo extra
   - Solution: Value stream mapping

7. **Defects:** Rework, scrap
   - Impact: 1-5% de COGS típico
   - Target: <0.5%

### Value Stream Mapping (VSM)

**Componentes:**
- **Process boxes:** Cada operação
- **Data boxes:** Cycle time, changeover time, uptime %, defect rate
- **Inventory triangles:** WIP entre operações
- **Timeline:** Lead time (total) vs Value-add time

**Key metrics:**
```
Process Cycle Efficiency = Value-Add Time / Total Lead Time
```

**Benchmarks:**
- Discrete manufacturing: 5-10% (muito waste!)
- Lean factories: 20-40%
- World-class: >50%

**Exemplo:**
- Total lead time: 20 dias
- Value-add time: 2 horas
- PCE = 2h / (20d × 8h) = 1.25% → Huge opportunity!

**Slide tipo:**
**Título:** "VSM revela lead time de 18 dias com apenas 4h value-add (1.2% PCE), target de 6 dias via WIP reduction"

### Kanban System

**Cálculo de kanban cards:**
```
# Cards = (Demand during Lead Time + Safety Stock) / Container Size
```

**Exemplo:**
- Daily demand: 500 units
- Lead time: 3 dias
- Safety stock: 20%
- Container: 100 units
- Cards = (500 × 3 × 1.2) / 100 = 18 cards

**Benefits:**
- Inventory reduction: 30-50%
- Overproduction elimination
- Visual management

## Six Sigma & Quality

### DMAIC Process

**Define:**
- Charter: Problem statement, goal, scope
- CTQ (Critical to Quality) tree
- SIPOC: Suppliers, Inputs, Process, Outputs, Customers

**Measure:**
- Data collection plan
- Baseline sigma level
- Measurement system analysis (Gage R&R)

**Analyze:**
- Root cause analysis (5 Whys, Fishbone)
- Hypothesis testing
- Regression analysis

**Improve:**
- Solution brainstorming
- Pilot testing
- Implementation

**Control:**
- Control plan
- SPC (Statistical Process Control) charts
- Standard work

**Typical project timeline:** 4-6 meses

**Expected benefit:** $50-250K per project

### Sigma Levels

**Conversion:**

| Sigma | DPMO | Yield |
|-------|------|-------|
| 2σ | 308,537 | 69.1% |
| 3σ | 66,807 | 93.3% |
| 4σ | 6,210 | 99.38% |
| 5σ | 233 | 99.977% |
| 6σ | 3.4 | 99.9997% |

**DPMO:** Defects Per Million Opportunities

**Benchmarks por indústria:**
- Automotive: 4-5σ target
- Aerospace: 5-6σ
- Pharma: 6σ (cGMP requirements)

**Slide tipo:**
**Título:** "Sigma level de 3.8σ (9,000 DPMO) vs target 4.5σ (1,350 DPMO) representa $4M em custo de qualidade anual"

### Cost of Quality (CoQ)

**Categorias:**

**Prevention costs:** Training, quality planning, supplier audits
- Target: 5-10% de CoQ

**Appraisal costs:** Inspection, testing, audits
- Target: 20-30% de CoQ

**Internal failure:** Scrap, rework, downtime
- Target: 30-40% de CoQ

**External failure:** Warranty, returns, recalls
- Target: 20-30% de CoQ (ou <10% em world-class)

**Total CoQ:** 2-5% of revenue (typical), <1.5% (best-in-class)

**ROI of quality programs:** 5-10:1 típico

## Industry 4.0 / Smart Manufacturing

### Digital Maturity Levels

**Level 0 - Manual:**
- Paper-based, no automation
- Typical: Small job shops

**Level 1 - Reactive:**
- Basic automation, standalone systems
- No data integration

**Level 2 - Connected:**
- Equipment connectivity (IoT sensors)
- Data collection, dashboards
- Typical: Many plants today

**Level 3 - Predictive:**
- Advanced analytics, AI/ML
- Predictive maintenance
- Digital twin

**Level 4 - Autonomous:**
- Self-optimizing systems
- Lights-out manufacturing
- Rare: <5% de factories

**Investment required (Level 2 → Level 3):** $5-20M per plant

**Payback:** 2-4 anos via uptime, quality, efficiency

### Predictive Maintenance

**Traditional approaches:**

**Reactive (Run-to-failure):**
- Cost: $18 per maintenance dollar
- Uptime: 65-75%

**Preventive (Time-based):**
- Cost: $13 per maintenance dollar
- Uptime: 75-85%
- Issue: Over-maintenance (replacing good parts)

**Predictive (Condition-based):**
- Cost: $9 per maintenance dollar
- Uptime: 85-95%
- ROI: 5-10× vs reactive

**Technologies:**
- Vibration analysis
- Thermal imaging
- Oil analysis
- Ultrasound
- AI/ML models

**Slide tipo:**
**Título:** "Predictive maintenance reduz unplanned downtime em 45% (3.2% → 1.8%) e maintenance cost em 28%"

### Digital Twin

**Definição:** Réplica virtual do physical asset

**Use cases:**
- Product design simulation
- Process optimization
- Training (virtual commissioning)
- Scenario planning

**ROI drivers:**
- Faster time-to-market: -20-40%
- Reduced physical prototypes: -50-80%
- Optimized throughput: +5-15%

**Technologies:**
- IoT sensors (real-time data)
- 3D CAD models
- Physics simulation
- AI/ML

**Market leaders:** Siemens, GE Digital, PTC

## Supply Chain & Procurement

### Supplier Performance Metrics

**Quality:**
- PPM (Parts Per Million defects)
  - Acceptable: <500 PPM
  - Good: <100 PPM
  - Excellent: <10 PPM

**Delivery:**
- OTIF (On-Time In-Full)
  - World-class: >95%
  - Acceptable: >90%
  - Poor: <85%

**Cost:**
- YoY cost reduction: 2-5% target
- PPV (Purchase Price Variance): <±2%

**Responsiveness:**
- Lead time: Shorter = better
- Flexibility (volume changes): ±20% tolerance ideal

### Supplier Segmentation

**Strategic suppliers:**
- High spend, high risk
- Partnership approach
- Joint development

**Leverage suppliers:**
- High spend, low risk
- Competitive bidding
- Volume discounts

**Bottleneck suppliers:**
- Low spend, high risk
- Dual sourcing
- Safety stock

**Routine suppliers:**
- Low spend, low risk
- E-procurement
- Transactional

## Manufacturing Cost Structure

### Typical breakdown (discrete manufacturing):**

**Direct Materials:** 40-60%
**Direct Labor:** 10-25%
**Manufacturing Overhead:** 20-35%
- Indirect labor: 8-12%
- Depreciation: 3-8%
- Utilities: 2-5%
- Maintenance: 2-4%
- Other: 5-10%

**Total COGS:** 70-85% de revenue

**Gross margin:** 15-30% (typical), 35-50% (high-value)

### Cost Reduction Levers

**Material costs (40-60% de COGS):**
- Should cost analysis: 5-15% savings
- Supplier consolidation: 3-8%
- Design for manufacturability: 10-25%

**Labor costs (10-25%):**
- Automation: 20-50% reduction
- Standard work: 5-15%
- Cross-training: 3-8%

**Overhead (20-35%):**
- Energy efficiency: 10-30%
- Maintenance optimization: 15-25%
- Layout optimization: 5-15%

**Slide tipo:**
**Título:** "Cost reduction program ($15M target) via material (45%), labor (30%), overhead (25%) em 18 meses"

## Production Planning

### Takt Time

**Definição:** Rate de produção para atender demanda

**Cálculo:**
```
Takt Time = Available Production Time / Customer Demand
```

**Exemplo:**
- Available time: 480 min/dia (8h shift)
- Daily demand: 400 units
- Takt time = 480/400 = 1.2 min = 72 segundos

**Use:** Design cells/lines com cycle time < takt time

### Cycle Time

**Definição:** Tempo real para completar 1 unidade

**Target:**
```
Cycle Time < Takt Time (para atender demanda)
Cycle Time = Takt Time (ideal, eliminates waste)
```

**Bottleneck:** Operação com maior cycle time

**Theory of Constraints:** Optimize bottleneck first

## Terminologia Especializada

**TPM:** Total Productive Maintenance
**SMED:** Single-Minute Exchange of Die (quick changeover)
**Poka-yoke:** Mistake-proofing devices
**Andon:** Visual alert system
**Gemba:** Actual place (shop floor)
**Kaizen:** Continuous improvement
**Heijunka:** Production leveling
**Jidoka:** Automation with human intelligence
**Muda:** Waste
**Mura:** Unevenness
**Muri:** Overburden
**5S:** Sort, Set in order, Shine, Standardize, Sustain
**SMED:** Single-Minute Exchange of Dies
**Pacemaker:** Process that sets production rhythm
**Bill of Materials (BOM):** List of components
**MRP:** Material Requirements Planning
**ERP:** Enterprise Resource Planning
**MES:** Manufacturing Execution System
**SCADA:** Supervisory Control and Data Acquisition
**PLC:** Programmable Logic Controller
**HMI:** Human-Machine Interface
**CMMS:** Computerized Maintenance Management System
**WIP:** Work in Process
**FG:** Finished Goods
**RM:** Raw Materials
**EOQ:** Economic Order Quantity
**MOQ:** Minimum Order Quantity
**SKU:** Stock Keeping Unit
**PPM:** Parts Per Million (defect rate)
**Cp/Cpk:** Process capability indices
**SPC:** Statistical Process Control
**DOE:** Design of Experiments
**FMEA:** Failure Mode and Effects Analysis
**RCA:** Root Cause Analysis
**Gage R&R:** Repeatability & Reproducibility study

## Paleta de Cores Manufacturing

**Industrial/Professional:**
- Steel Blue: #455A64
- Charcoal: #37474F
- Safety Orange: #FF6F00
- Forest Green: #2E7D32

**Performance/Metrics:**
- Success Green: #388E3C
- Warning Yellow: #F9A825
- Alert Red: #C62828
- Info Blue: #1976D2

**Clean/Modern:**
- White: #FFFFFF
- Light Gray: #ECEFF1
- Medium Gray: #90A4AE

**Tech/Industry 4.0:**
- Electric Blue: #0277BD
- Neon Cyan: #00BCD4
- Digital Purple: #673AB7

## Action Titles - Exemplos Manufacturing

❌ "OEE performance"
✅ "OEE de 82% (+14pp YoY) via TPM e SMED libera 15% de capacity adicional, evitando $12M CAPEX"

❌ "Lead time analysis"
✅ "Lead time reduzido de 21 para 8 dias via kanban e VSM, melhorando cash conversion cycle em 13 dias"

❌ "Quality metrics"
✅ "PPM defects de 45 (vs 180 baseline) alcança target 6σ, eliminando $3.2M em custo de qualidade anual"

❌ "Supplier performance"
✅ "OTIF de fornecedores críticos aumentou de 87% para 96%, reduzindo line stoppages em 60%"

❌ "Industry 4.0 implementation"
✅ "Predictive maintenance (Level 3 digital maturity) reduz downtime 40% com ROI de 3.2× em 18 meses"

## Benchmarking - World Class Manufacturing (WCM)

**Shingo Prize criteria:**
- OEE: >85%
- First Pass Yield: >99%
- OTIF: >99%
- Inventory turns: >20×
- Lead time: <1 week
- Employee suggestions: >20 per year per person

**Toyota Production System (TPS) benchmarks:**
- Defect rate: <10 PPM
- Downtime: <5%
- Changeover time: <10 minutes (SMED)
- Suggestion implementation: >90%

## Slide Specifications - Manufacturing

### Chart preferences

**OEE waterfall:**
- Start: Theoretical capacity (100%)
- -Availability losses
- -Performance losses
- -Quality losses
- =Actual OEE
- Color: Gray (losses), Green (OEE)

**Pareto chart (defects, downtime):**
- Bars: Top 10 causes (descending)
- Line: Cumulative %
- 80/20 rule highlight

**Control chart (SPC):**
- Time series com UCL/LCL (Upper/Lower Control Limits)
- Centerline (mean)
- Specification limits se relevante
- Out-of-control points flagged

**Value stream map:**
- Process boxes com data
- Inventory triangles
- Lead time ladder
- Before/After comparison

### Fontes típicas

"Fonte: MES (Manufacturing Execution System) para OEE e production data; Quality database (QMS) para defect rates; ERP system (SAP) para inventory e costs; Supplier scorecards para OTIF; Industry Week 'Best Plants' survey para benchmarks externos (2024); Company analysis"

### Notas técnicas

"(1) OEE calculado usando planned production time (1 turno, 5 dias/semana)
(2) PPM defects incluem supplier components e internal manufacturing
(3) Lead time = order receipt até finished goods available
(4) Cost savings validados via P&L impact (não apenas run-rate)"
