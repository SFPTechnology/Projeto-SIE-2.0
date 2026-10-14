# Template: Timeline/Roadmap Slide

## Purpose
Apresentar sequências temporais, implementation plans, project roadmaps, milestones. Criar senso de momentum e clareza na execução.

---

## SLIDE SPECIFICATION - TIMELINE/ROADMAP

### PAGE NUMBER
**Posição:** Rodapé direito
**Coordenadas:** Coluna 11.5-12, Linha 7.9
**Formato:** Número sequencial
**Fonte:** Helvetica Neue Regular, 10pt, #6E6E6E

---

### ACTION TITLE
**Posição:** Topo
**Coordenadas:** Colunas 1-12, Linha 1

**Estrutura:**
"[PROGRAMA/INITIATIVE] + [TIMELINE SPAN] + [KEY MILESTONE/OUTCOME]"

**Exemplos:**

✅ "Transformation roadmap de 18 meses (Q1/25-Q2/26) entrega $80M impact via 5 waves sequenciadas, com quick wins em primeiros 90 dias"

✅ "Product development timeline comprime go-to-market de 12 para 7 meses através de parallel workstreams, targeting launch Q3/2025"

✅ "Integration plan de 24 meses consolida operations até Q4/2026 com 3 major milestones e $45M synergy realization"

**Especificações:**
- Fonte: Helvetica Neue Bold, 16-18pt, #003B5C
- Line height: 1.3
- Max linhas: 2

---

## TIMELINE FORMATS

### FORMAT 1: HORIZONTAL GANTT-STYLE

**Quando usar:**
- Project plans com múltiplos workstreams
- Overlapping initiatives
- Resource allocation over time

**Estrutura:**

**Time axis (horizontal, top):**
- Position: Linha 2, Colunas 2-12
- Span: Quarters, months, ou weeks (depends on duration)
- Line: 2pt, #003B5C
- Markers: Vertical ticks para cada period
- Labels: Above axis, 10pt Regular, #6E6E6E
  - Format: "Q1 2025", "Jan", "Week 1"
  - Spacing: Equal intervals

**Swim lanes (vertical):**
- Quantity: 4-7 workstreams/initiatives
- Height: 1-1.2cm cada
- Position: Linhas 2.5-7, full width
- Labels: Left side (colunas 1-1.5), 11pt Bold, #000000
  - Examples: "Technology", "Process", "People", "Governance"
- Alternating backgrounds: White / #FAFAFA (zebra striping)

**Activity bars:**
- Height: 80% da swim lane height (deixa spacing)
- Color: Status-based
  - Completed: #00A86B (green), 100% opacity
  - In progress: #FF6F00 (orange), 100% opacity
  - Planned: #B0BEC5 (gray), 60% opacity
- Border radius: 4px (rounded)
- Border: None ou 1pt darker shade

**Bar labels:**
- Inside bar (se couber): 10pt Bold, white ou black (contrast dependent)
- Format: "[Activity name]" OU "[Name] • [Duration]"
- Truncate com "..." se too long

**Dependencies (arrows):**
- Connecting bars: 2pt dashed line, #6E6E6E
- Arrowhead: 8pt, indicating dependency direction
- Apenas mostrar critical path dependencies (não todas!)

**Milestones:**
- Symbol: Diamond (◆) 16pt
- Color: #D32F2F (red - draw attention)
- Position: On timeline, acima do swim lanes
- Label: Below diamond, 9pt Regular, #000000
  - Format: "Go-Live" | "UAT Complete" | "Board Approval"
- Vertical dashed line: Connecting milestone to relevant bars

**Today marker:**
- Vertical line: 3pt, #FF6F00 (orange)
- Label: "Today" at top, 10pt Bold
- Full height through all swim lanes

**Exemplo completo:**

**HORIZONTAL GANTT - Digital Transformation (18 months: Q1/25-Q2/26)**

**Time axis:**
- Q1/25 | Q2/25 | Q3/25 | Q4/25 | Q1/26 | Q2/26
- Positioned at Linha 2, even spacing

**Swim lane 1: Technology Platform**
- Bar 1: "CRM Implementation" - Q1-Q2/25 (green, completed)
- Bar 2: "Data Warehouse Migration" - Q2-Q4/25 (orange, in progress)
- Bar 3: "AI/ML Layer" - Q4/25-Q2/26 (gray, planned)

**Swim lanes 2-5:** Similar structure para Process, People, Governance, Change Management

**Milestones:**
- ◆ "Phase 1 Go-Live" - End of Q2/25
- ◆ "Full Integration" - End of Q1/26
- ◆ "Value Realization" - End of Q2/26

**Today line:** Vertical orange at mid-Q4/24

**Dependencies:**
- Arrow de "CRM Implementation" → "Data Warehouse" (dashed)
- Arrow de "Data Warehouse" → "AI/ML Layer"

---

### FORMAT 2: VERTICAL TIMELINE (Historical ou Sequential)

**Quando usar:**
- Historical evolution
- Sequential phases (não parallel)
- Storytelling linear

**Estrutura:**

**Vertical axis (left):**
- Line: 3pt, #003B5C, vertical
- Length: Linhas 2-7.5
- Position: Coluna 2

**Time markers:**
- Circles on line: 20px Ø, #003B5C fill
- Inner circle: 8px Ø, white (donut style)
- Spacing: Even intervals (ex: 1.5cm apart para 4-6 events)

**Time labels:**
- Left of line (Coluna 1-1.5): Date/period
- Font: 12pt Bold, #003B5C
- Format: "Q1 2023", "Jan 2024", "Phase 1"
- Alignment: Right-aligned to line

**Event boxes:**
- Position: Right of timeline (Colunas 2.5-12)
- Size: Variable width (based on content), 1.5-2cm height
- Background: Alternating slight offset (stagger para avoid monotony)
- Border: 2pt left, color-coded by phase/status
  - Past: #00A86B (green)
  - Present: #FF6F00 (orange)
  - Future: #1976D2 (blue)

**Event content:**
- Title: 12pt Bold, #000000
- Description: 10pt Regular, #6E6E6E, 1-2 linhas
- Icon (opcional): 24×24px, left side

**Connector lines:**
- From circle to event box: 2pt, #E0E0E0
- Horizontal, 0.5-1cm length

**Exemplo:**

**VERTICAL TIMELINE - Company Evolution 2020-2025**

**2020 - Founded**
- Circle on vertical line
- Box (right): "Company founded with $5M seed funding, 12 employees"
- Border: 2pt green (past)

**2021 - Product Launch**
- Circle
- Box: "V1.0 launched, acquired first 50 customers, $2M ARR"
- Border: 2pt green

**2022 - Series A**
- Circle
- Box: "Raised $25M Series A, expanded to 80 employees, entered EU market"
- Border: 2pt green

**2023 - Scaling**
- Circle
- Box: "Reached $15M ARR, launched enterprise tier, 200 customers"
- Border: 2pt green

**2024 - Present**
- Circle (larger, 24px, highlighted)
- Box: "Current: $40M ARR, 500+ customers, preparing Series B"
- Border: 2pt orange (present)

**2025 - Target**
- Circle (dashed border, indicating future)
- Box: "Target: $100M ARR, market leader, potential IPO evaluation"
- Border: 2pt blue (future)

---

### FORMAT 3: PHASED ROADMAP (Waves/Sprints)

**Quando usar:**
- Agile delivery
- Wave-based transformation
- Incremental rollout

**Estrutura:**

**Phases (horizontal bands):**
- Width: Full width (Colunas 1-12)
- Heights: Proporcionais ou iguais
- Position: Stacked verticalmente, Linhas 2-7.5
- Colors: Gradient progression (#E3F2FD → #1976D2 - light to dark)
- Borders: 2pt white between phases

**Phase labels:**
- Left side: Large number + phase name
  - Number: 48pt Bold, 20% opacity, background
  - Name: 14pt Bold, #FFFFFF ou #000000 (contrast)
- Example: "1 | FOUNDATION" | "2 | BUILD" | "3 | SCALE"

**Timeline markers (top):**
- Months/quarters across phases
- Format: Small labels, 9pt Regular, #6E6E6E

**Content inside phases:**
- Bullets: 2-5 key initiatives per phase
- Font: 10pt Regular, color with good contrast
- Icons: 20×20px, matching phase theme
- Deliverables: Bold
- Metrics: In brackets, ex: "CRM rollout [500 users]"

**Phase outcomes (right side):**
- Box summarizing phase value
- Background: #FFFDE7 (light yellow)
- Border: 2pt #FBC02D (yellow) left border
- Content: "Value: $X M | Time: Y weeks"
- Font: 10pt Bold

**Transition points:**
- Gates between phases: Vertical dashed line
- Label: "Gate 1: Steering Committee Approval" - 9pt Italic
- Icon: Checkpoint symbol

**Exemplo:**

**PHASED ROADMAP - 3-Wave Transformation (12 months)**

**WAVE 1: FOUNDATION (Months 1-3)**
- Background: #E3F2FD (light blue)
- Number: "1" em 48pt, 20% opacity
- Content:
  • Current state assessment [6 weeks]
  • Technology selection [4 weeks]
  • Pilot team formation [2 weeks]
  • Quick wins identification
- Outcome box: "Value: $5M quick wins | Time: 12 weeks"
- Gate: "✓ Business Case Approved"

**WAVE 2: BUILD (Months 4-8)**
- Background: #90CAF9 (medium blue)
- Number: "2"
- Content:
  • Core platform deployment [500 users]
  • Process redesign [15 processes]
  • Training program [200 people]
  • Change management
- Outcome: "Value: $35M run-rate | Time: 20 weeks"
- Gate: "✓ UAT Passed"

**WAVE 3: SCALE (Months 9-12)**
- Background: #1976D2 (dark blue)
- Number: "3"
- Content:
  • Enterprise rollout [2,000 users]
  • Advanced features [AI/ML]
  • Optimization & tuning
  • Full value capture
- Outcome: "Value: $80M total | Time: 16 weeks"
- Gate: "✓ Go-Live Complete"

---

### FORMAT 4: CALENDAR/SPRINT VIEW

**Quando usar:**
- Short-term planning (weeks/months)
- Sprint planning
- Detailed scheduling

**Estrutura:**

**Calendar grid:**
- Columns: Days ou weeks
- Rows: Workstreams ou teams
- Cell size: 1.5-2cm × 1.5-2cm
- Gridlines: 1pt, #E0E0E0

**Header row:**
- Dates/periods: 10pt Bold, #000000
- Background: #F5F5F5
- Example: "Week 1 (Jan 2-8)" | "Week 2 (Jan 9-15)"

**Activity cells:**
- Fill color: By status ou type
  - Design: #E3F2FD (blue)
  - Development: #C8E6C9 (green)
  - Testing: #FFF9C4 (yellow)
  - Deployment: #FFCCBC (coral)
- Text: Activity name, 9pt Regular
- Icon: 16×16px indicating type

**Spanning activities:**
- Multi-cell merge para activities >1 period
- Clear borders: 2pt

**Legend:**
- Bottom-right
- Color squares + labels
- Format: ▢ Design | ▢ Development | ▢ Testing | ▢ Deployment

---

## SUPPORTING ELEMENTS

### RISK/ISSUE FLAGS
**Purpose:** Highlight blockers ou risks

**Position:** Inline com timeline, adjacent to affected items

**Format:**
- Icon: ⚠️ 16pt, #D32F2F (red)
- Callout box: Small pop-up
  - Background: #FFEBEE (light red)
  - Border: 2pt #D32F2F left
  - Text: "Risk: [Description]" - 9pt Regular
  - Mitigation: "Mitigation: [Action]" - 9pt Italic

**Example:**
⚠️ "Risk: Vendor delay (2 weeks) | Mitigation: Parallel workstream initiated"

---

### CUMULATIVE VALUE CURVE (Overlay)
**Purpose:** Show value realization over time

**Position:** Overlay on timeline, top area

**Format:**
- Line chart: Cumulative $ value
- X-axis: Aligned com timeline periods
- Y-axis: $0 - Target value
- Line: 3pt, #00A86B (green)
- Shaded area: Below line, #00A86B 20% opacity
- Milestones: Circles on line para major gates
- Target line: Horizontal dashed, #B0BEC5

**Example:**
Overlay showing cumulative value de $0 (Q1) → $80M (Q4), com milestones marcados

---

### RESOURCE ALLOCATION BAR (Optional)
**Purpose:** Show team/budget allocation

**Position:** Bottom of timeline, Linha 7.8

**Format:**
- Stacked horizontal bar
- Segments: By team ou budget category
- Colors: Distinct per segment
- Labels: Inside segments, "Team A: 40%"
- Total: "100 FTEs" ou "$5M budget"

---

## CHECKLIST - TIMELINE SLIDE

**Content:**
- [ ] Início e fim claramente marcados?
- [ ] Milestones críticos identificados?
- [ ] Dependencies mapeadas?
- [ ] Quick wins destacados (se aplicável)?
- [ ] Risks/blockers endereçados?

**Visual:**
- [ ] Timeline type apropriado (Gantt vs vertical vs phased)?
- [ ] Today marker visível (se relevant)?
- [ ] Colors indicam status/tipo consistentemente?
- [ ] Spacing adequado (não cramped)?
- [ ] Text legível em todos os elementos?

**Accuracy:**
- [ ] Dates realistas e validados?
- [ ] Dependencies factually corretas?
- [ ] Resource allocation plausível?
- [ ] Buffer time incluído (não optimistic bias)?

**Actionability:**
- [ ] Next steps claros?
- [ ] Owners identificados (se apropriado)?
- [ ] Decision points marcados?
- [ ] Success criteria definidos?

---

## AI IMAGE GENERATION - TIMELINE VISUALS

**Gantt chart concept:**
```
3D isometric project timeline visualization, horizontal gantt chart style,
5 parallel swim lanes (each 40cm wide × 8cm tall × 3cm depth), activity
blocks floating above lanes (various lengths 10-50cm, height 6cm, colors:
completed #00A86B green, in-progress #FF6F00 orange, planned #B0BEC5 gray
60% opacity), milestone diamonds (◆ 15cm, #D32F2F red) elevated 10cm above
timeline, thin connector arrows (2cm width, #6E6E6E gray, flowing between
blocks), time axis at top (metallic #003B5C navy, 2cm diameter rod), clean
modern corporate aesthetic, white background with subtle grid pattern,
professional lighting (soft shadows, 20% opacity), 8K resolution,
--ar 16:9 --stylize 450 --no people, faces, text --v 6.0
```

**Phased roadmap waves:**
```
Abstract wave-like phase visualization, 3 ascending waves (each 5m wide ×
2m tall, flowing smoothly), wave 1 light blue #E3F2FD, wave 2 medium blue
#90CAF9, wave 3 deep blue #1976D2, subtle gradient effects (top lighter,
bottom darker), floating geometric elements above each wave (cubes, spheres
representing initiatives, 30-50cm size, semi-transparent 80% opacity),
curved arrows flowing from wave to wave (3cm width, white with slight glow),
clean white background, professional business aesthetic, soft ambient
lighting, depth of field effect (foreground sharp, background soft blur),
ultra-high detail, --ar 16:9 --stylize 500 --no text, people --v 6.0
```

---

**VERSÃO:** 1.0
**OWNER:** GPT McKinsey PPT Architect
**ÚLTIMA ATUALIZAÇÃO:** Dezembro 2024
