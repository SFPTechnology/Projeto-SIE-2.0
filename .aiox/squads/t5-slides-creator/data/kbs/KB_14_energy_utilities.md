# KB_14: Energy & Utilities - Power, Renewables, Grid, Oil & Gas

## Power Generation Metrics

### Capacity Factor

**Definição:** Actual output vs theoretical maximum

**Cálculo:**
```
Capacity Factor = Actual Energy Produced / (Nameplate Capacity × Time) × 100%
```

**Benchmarks por tipo de geração:**

**Nuclear:**
- Typical: 85-95%
- Best performers: >95%
- França: ~75% (fleet average)

**Coal:**
- Typical: 50-70%
- Declining devido a retirements e economics

**Natural Gas (Combined Cycle):**
- Baseload: 50-70%
- Peaker: 5-20%

**Wind (Onshore):**
- Typical: 25-35%
- Best sites: 40-50%
- Offshore: 35-50%

**Solar PV:**
- Typical: 15-25%
- Best sites (desert): 25-30%
- Rooftop: 12-18%

**Hydro:**
- Run-of-river: 40-60%
- Reservoir: 30-50% (depende de precipitação)

**Slide tipo:**
**Título:** "Capacity factor eólico de 38% (top quartile) vs 28% fleet average justifica expansão de 500MW adicional"

### Levelized Cost of Energy (LCOE)

**Definição:** All-in cost por MWh gerado (lifetime)

**Fórmula:**
```
LCOE = (CAPEX + PV of OPEX + PV of Fuel) / PV of Energy Produced
```

**Componentes:**
- **CAPEX:** Upfront construction ($/kW)
- **OPEX:** Fixed O&M ($/kW-year) + Variable O&M ($/MWh)
- **Fuel:** $/MMBtu (fossil) ou $0 (renewables)
- **Discount rate:** 5-10% típico (WACC)
- **Lifetime:** 20-40 anos

**Benchmarks 2024 (unsubsidized, $/MWh):**

**Utility-scale solar PV:** $30-50
**Onshore wind:** $25-45
**Offshore wind:** $60-100
**Natural gas (combined cycle):** $45-75
**Coal:** $65-150 (rising com carbon pricing)
**Nuclear (new build):** $120-200
**Geothermal:** $50-100
**Hydro (new):** $40-90

**Trends:**
- Solar/wind: -70-90% desde 2010
- Battery storage: -85% desde 2013

**Slide tipo:**
**Título:** "Solar LCOE de $38/MWh (incluindo storage) é competitive vs gas peaker ($65/MWh) em 85% das horas do ano"

### Heat Rate (Thermal Efficiency)

**Definição:** Energy input / Energy output (lower = better)

**Unidade:** Btu/kWh ou kJ/kWh

**Cálculo:**
```
Heat Rate = Fuel Energy In (Btu) / Electricity Out (kWh)
```

**Perfect efficiency (3,412 Btu/kWh = 100%)** → impossível

**Benchmarks:**

**Coal (subcritical):** 10,000-11,000 Btu/kWh (~31-34% efficiency)
**Coal (supercritical):** 8,800-9,500 Btu/kWh (~36-39%)
**Natural gas (CCGT):** 6,500-7,500 Btu/kWh (~45-52%)
**Natural gas (simple cycle):** 9,500-11,000 Btu/kWh (~31-36%)

**Impact de 1% efficiency improvement:**
- 500MW CCGT, 70% capacity factor
- Savings: $2-5M/ano em fuel cost

## Grid & Transmission

### Reliability Metrics

**SAIDI (System Average Interruption Duration Index):**
```
SAIDI = Σ(Customer Interruption Durations) / Total Customers
```
- Unidade: Minutes per customer per year
- US average: 120-200 min/ano
- Best utilities: <60 min
- Worst: >300 min

**SAIFI (System Average Interruption Frequency Index):**
```
SAIFI = Σ(Number of Interruptions) / Total Customers
```
- Unidade: Interruptions per customer per year
- US average: 1.0-1.5 interruptions/ano
- Best: <0.8
- Worst: >2.0

**CAIDI (Customer Average Interruption Duration Index):**
```
CAIDI = SAIDI / SAIFI
```
- Unidade: Minutes per interruption
- Typical: 80-150 minutes

**Excludes:** Major events (storms) - "SAIDI without major events"

**Regulatory targets:** Utilities fined se ultrapassar thresholds

**Slide tipo:**
**Título:** "SAIDI de 95 min (target <100) posiciona no top decile US utilities, evitando $8M em regulatory penalties"

### Grid Modernization

**Advanced Metering Infrastructure (AMI):**
- Penetration US: ~70% (2024)
- Benefits: Real-time data, remote disconnect, outage detection
- Cost: $200-400 per meter installed
- Payback: 5-10 anos

**Distribution Automation:**
- Automated switches, reclosers
- Self-healing grid
- Benefits: -20-40% SAIDI improvement
- Investment: $500K-2M per circuit

**Distributed Energy Resources (DER):**
- Rooftop solar: 30+ GW installed (US)
- Battery storage: 10+ GW (growing 50%+ YoY)
- EVs: 3M+ vehicles (10M+ by 2030)
- Challenge: Bidirectional flows, voltage management

### Transmission Congestion

**LMP (Locational Marginal Pricing):**
- Price varies by node on grid
- Spreads: $0-100+/MWh (congestion + losses)
- High spreads = transmission constraint

**Congestion cost:**
- Total US: $10-20B annually
- Solution: New transmission lines ($2-5M per mile)

## Renewable Energy

### Solar PV Economics

**CAPEX (utility-scale):**
- 2024: $800-1,200/kW
- Breakdown: 35% modules, 25% inverters/electrical, 20% labor, 20% other

**Degradation:**
- Typical: 0.5-0.8% per year
- Warranty: 80% output at year 25

**O&M:**
- Fixed: $15-25/kW-year
- Major: Inverter replacement year 10-15 ($50-100/kW)

**PPA prices (Power Purchase Agreement):**
- US average: $25-35/MWh (20-year contract)
- Best projects: $20-25/MWh

**Value deflation (duck curve):**
- Midday solar saturation → negative prices
- Requires storage or demand flexibility

### Wind Economics

**CAPEX (onshore):**
- 2024: $1,200-1,800/kW
- Breakdown: 30% turbine, 20% tower, 15% foundation, 15% grid connection, 20% other

**CAPEX (offshore):**
- 2024: $3,000-5,000/kW (floating: $4,500-7,000)

**O&M:**
- Onshore: $40-60/kW-year
- Offshore: $100-150/kW-year (access challenges)

**Repowering:**
- Years 20-25: Replace turbines
- New capacity factor: +5-15pp (taller towers, bigger rotors)
- Cost: 50-70% de new build

**PPA prices:**
- Onshore: $20-35/MWh
- Offshore: $60-120/MWh (declining)

### Battery Storage

**CAPEX:**
- 2024: $300-500/kWh (4-hour lithium-ion)
- 2020: $1,000+/kWh → -70% em 4 anos!

**Cycle life:**
- Lithium-ion: 3,000-6,000 cycles
- Daily cycling: 8-15 year life

**Round-trip efficiency:** 85-90%

**Use cases:**
- Frequency regulation: 1-15 min response
- Peak shaving: 2-4 hour discharge
- Renewables shifting: 4-8 hours

**Economics:**
- Revenue: Energy arbitrage + capacity + ancillary services
- IRR target: 10-15%

**Slide tipo:**
**Título:** "Battery storage (100MW/400MWh) captura $18M anual via peak arbitrage ($12M) + frequency regulation ($6M), 12% IRR"

## Natural Gas & LNG

### Upstream (Production)

**Breakeven prices (WTI equivalent):**
- Permian (shale): $35-45/bbl
- Haynesville (gas): $2.50-3.50/MMBtu
- Offshore (GOM): $45-60/bbl

**Production costs:**
- Drilling: $4-8M per well (shale)
- Completion: $3-6M
- Operating: $5-15/boe

**Decline curves:**
- Shale: 60-80% decline year 1
- Conventional: 5-15% per year

### Midstream (Pipelines)

**Pipeline economics:**
- CAPEX: $1-3M per mile (diameter dependent)
- Tariffs: $0.10-0.50 per MMBtu per 100 miles
- Utilization: 70-90% target
- Regulated return: 10-12% typical

**LNG export:**
- Liquefaction cost: $2-4/MMBtu
- Shipping: $0.50-2.00/MMBtu (destination dependent)
- Regasification: $0.50-1.00/MMBtu

**Henry Hub to TTF spread:** $5-15/MMBtu (2022 crisis: $30+)

### Downstream (Power Generation)

**Gas-fired generation:**
- CCGT: 45-52% efficiency (newer plants: 55-60%)
- Peaker: 30-40% efficiency
- Variable cost: Heavily dependent on gas price

**Spark spread:**
```
Spark Spread = Power Price ($/MWh) - (Gas Price × Heat Rate) - VOM
```

**Example:**
- Power: $50/MWh
- Gas: $3/MMBtu
- Heat rate: 7,000 Btu/kWh = 7 MMBtu/MWh
- VOM: $2/MWh
- Spark spread = $50 - ($3 × 7) - $2 = $27/MWh

**Profitable:** Spark spread > Fixed costs per MWh

## Carbon & ESG

### Carbon Intensity

**Grid emissions:**
- Coal: 900-1,000 gCO2/kWh
- Natural gas (CCGT): 350-450 gCO2/kWh
- Renewables: 10-50 gCO2/kWh (lifecycle)
- Nuclear: 10-30 gCO2/kWh (lifecycle)

**Grid average (2024):**
- US: ~400 gCO2/kWh (declining)
- EU: ~250 gCO2/kWh
- China: ~550 gCO2/kWh

**Targets:**
- Many utilities: Net zero by 2050
- Interim: -50% by 2030 (vs 2005 baseline)

### Carbon Pricing

**Mechanisms:**

**Cap-and-trade (ETS):**
- EU ETS: €60-100/tonne CO2 (2024)
- California: $30-40/tonne
- RGGI (Northeast US): $10-15/tonne

**Carbon tax:**
- Canada: CAD $65/tonne (2024), rising to $170 by 2030
- Sweden: $130+/tonne

**Impact on dispatch:**
- $30/tonne adds ~$15-30/MWh to coal
- $30/tonne adds ~$5-10/MWh to gas

**Slide tipo:**
**Título:** "Carbon price de €80/tonne torna 60% do coal fleet uneconomic vs CCGT, acelerando coal phase-out em 5 anos"

### Scope 1/2/3 Emissions

**Scope 1:** Direct emissions (power plants owned)
**Scope 2:** Purchased electricity
**Scope 3:** Value chain (fuel extraction, employee commute, etc.)

**Utility típica:**
- Scope 1: 90-95% (generation)
- Scope 2: 1-3%
- Scope 3: 3-8%

**Reduction pathways:**
- Retire coal → -60-80% Scope 1
- Add renewables → -20-40%
- Efficiency improvements → -5-10%
- CCS (carbon capture) → -90% from specific plants

## Regulatory & Market Design

### Wholesale Markets

**Energy-only markets:**
- Texas (ERCOT): No capacity payments
- Price spikes during scarcity incentivize investment
- Risk: "Missing money" problem

**Capacity markets:**
- PJM, ISO-NE, NYISO
- Payments for availability ($/MW-day)
- Typical: $50-200/MW-day ($18-73K/MW-year)

**Ancillary services:**
- Frequency regulation: Fast response (seconds)
- Spinning reserve: Online backup (10 min)
- Non-spinning: Offline backup (30 min)

**Compensation:** $5-50/MW-hour (varies by service, market)

### Rate Structures (Retail)

**Residential:**
- Flat rate: $0.10-0.30/kWh (varies by state)
- Tiered: Increasing price with usage
- Time-of-Use (TOU): Peak/off-peak pricing
  - Peak: $0.20-0.40/kWh
  - Off-peak: $0.05-0.15/kWh

**Commercial/Industrial:**
- Energy charge: $/kWh
- Demand charge: $/kW (highest 15-min interval)
- Power factor penalties
- Typical: 40-60% demand charges de bill total

**Rate case (regulatory):**
- Utilities file every 3-5 anos
- Justify costs, request rate increase
- Approved ROE: 9-11% típico

## Terminologia Especializada

**MW vs MWh:** Power (capacity) vs Energy (production)
**Baseload:** Always-on generation (nuclear, coal, hydro)
**Peaker:** Runs during high demand (gas turbines, batteries)
**Dispatch:** Order plants operate (cheapest first = merit order)
**Curtailment:** Shutting down renewable output (grid constraint)
**Duck curve:** Net load shape com solar (looks like duck)
**Capacity market:** Paying for availability (not production)
**PPA:** Power Purchase Agreement (offtake contract)
**Interconnection queue:** Projects waiting for grid connection (>1,000 GW backlog!)
**Wheeling:** Transmitting power across territories
**Balancing authority:** Entity responsible for grid stability
**Ancillary services:** Frequency, voltage, reserves
**Black start:** Restarting grid after total blackout
**N-1 contingency:** Grid survives any single failure
**Load factor:** Average load / peak load
**Demand response:** Paying customers to reduce usage
**Virtual power plant (VPP):** Aggregated DERs
**Microgrid:** Local grid (can island from main grid)
**RECs:** Renewable Energy Credits (tradeable)
**ITC/PTC:** Investment Tax Credit / Production Tax Credit
**Merchant plant:** Sells into market (no long-term PPA)
**Tolling agreement:** Plant operator paid to convert fuel to power
**Nameplate capacity:** Maximum theoretical output
**Spinning reserve:** Already synchronized to grid
**Ramp rate:** MW per minute (flexibility metric)
**Shoulder months:** Spring/fall (mild weather, low demand)

## Paleta de Cores Energy/Utilities

**Power/Grid:**
- Electric Blue: #0277BD
- Bright Yellow: #FBC02D (caution/high voltage)
- Charcoal: #37474F
- Steel Gray: #546E7A

**Renewables:**
- Solar Orange: #FF6F00
- Wind Sky Blue: #03A9F4
- Hydro Aqua: #00ACC1
- Green Energy: #2E7D32

**Fossil Fuels:**
- Coal Black: #212121
- Gas Flame Blue: #1565C0
- Oil Amber: #FF8F00

**Performance:**
- Success Green: #388E3C
- Warning Yellow: #F9A825
- Alert Red: #C62828
- Info Cyan: #00BCD4

## Action Titles - Exemplos Energy

❌ "LCOE analysis"
✅ "Solar LCOE de $32/MWh (incluindo storage) é 40% abaixo de gas peaker, enabling coal retirement sem price increase"

❌ "Reliability metrics"
✅ "SAIDI de 78 min (top decile) e $12M grid automation investment evita $6M annual regulatory penalties"

❌ "Renewable portfolio"
✅ "Wind portfolio (2.5 GW, 42% capacity factor) gera $180M EBITDA e abate 4M tonnes CO2 anualmente"

❌ "Carbon emissions"
✅ "Coal retirement plan reduz Scope 1 emissions 65% até 2030, alinhando com net zero 2050 target e evitando $400M carbon cost"

❌ "Battery storage project"
✅ "100MW/400MWh battery captura $18M anual via arbitrage ($12M) + ancillary services ($6M), 12.5% IRR unlevered"

## Slide Specifications - Energy

### Charts preferidos

**Generation mix (stacked area):**
- Eixo X: Time (years ou hours)
- Eixo Y: MW ou MWh
- Colors: Coal (black), Gas (blue), Nuclear (orange), Wind (cyan), Solar (yellow), Hydro (aqua)

**Merit order curve:**
- Eixo X: Cumulative capacity (MW)
- Eixo Y: Marginal cost ($/MWh)
- Plants stacked left-to-right (cheapest → most expensive)
- Demand line intersects = clearing price

**Duck curve:**
- Eixo X: Hours of day
- Eixo Y: Net load (MW)
- Multiple lines: Different seasons ou years
- Shows evening ramp challenge

**LCOE comparison (bar chart):**
- Technologies on Y-axis
- LCOE ($/MWh) on X-axis
- Split bars: CAPEX, OPEX, Fuel components

### Fontes típicas

"Fonte: Internal SCADA system for generation data; EIA (Energy Information Administration) Form 860/923 para fleet benchmarks, disponível em https://www.eia.gov; Lazard LCOE Analysis v17.0 (2024) para cost comparisons; ISO market data (CAISO, PJM, ERCOT public dashboards); NERC Reliability Assessments; Bloomberg New Energy Finance; Company analysis"

### Notas técnicas

"(1) Capacity factor calculado usando nameplate capacity e net generation
(2) LCOE assumes 8% discount rate (WACC), 25-year lifetime para solar/wind
(3) Carbon intensity inclui upstream methane leakage (2.3% assumption para gas)
(4) SAIDI excludes Major Event Days (MEDs) per IEEE Standard 1366"
