# Design Philosophies — Taxonomy para Decks Sinkra

> **Purpose:** taxonomia de 20 filosofias de design em 5 escolas, usada como fallback quando brief é visualmente vago e não há design context existente (brand spec, UI kit, reference).
> **Consumer:** `slide-chief` (routing) + `tasks/advise-design-direction.md` (quando implementado) + `design-renderer` (prompt composition).
> **Scope:** aplicável a qualquer deck output (slide HTML, PDF, PPTX). Escola e filosofia escolhidas influenciam typography, color palette, layout density, motion intensity.

---

## Princípio de uso

Esta taxonomia é **fallback**, não default. Ordem de precedência para resolver visual style:

1. **Brand spec existente** — se business tem brandbook/UI kit no workspace, respeitar integralmente
2. **Reference fornecido pelo user** — screenshot, link, product that inspires
3. **Existing design system (shadcn/ui + tokens)** — se deck é para produto que já tem DS, seguir
4. **Esta taxonomia** — só se 1-3 falham e user pede "sugestões de estilo"

**Regra de diferenciação:** quando recomendar 3 filosofias ao user como opções, elas DEVEM vir de **3 escolas distintas** — evitar pitch de 3 minimalismos levemente diferentes.

---

## As 5 escolas

| Escola | Princípio central | Quando escolher | Ideal para sinkra business |
|---|---|---|---|
| Information Architecture | "Dados não são decoração, são material de construção" | Audience sophisticated, data-heavy narrative | AIOX institucional, Bilhon investor deck |
| Motion Poetics | "Tecnologia tem ritmo" | Launch, product demo, brand video | AIOX launch, Academia Lendária promos |
| Minimalism | "Reduzir até não dar mais" | Premium, editorial, pitch alto-ticket | AllFluence luxo, executive deck |
| Experimental Avant-garde | "Quebrar regras cria regras" | Creative industries, cultural cover | Academia Lendária cover, creative campaigns |
| Eastern Philosophy | "Vazio é conteúdo" | Reflective, thoughtful, artisan | AllFluence premium, brand manifesto |

---

## Filosofia-por-filosofia

### Escola 1 — Information Architecture

#### 1.1 — Editorial Typography (Pentagram lineage)

**Princípio:** tipografia é a linguagem principal. Grid matemática é o esqueleto.

**Características visuais:**
- Preto + branco + 1 accent color (máx)
- Grid Swiss com spacing matemático preciso (8pt ou 4pt baseline)
- Type hierarchy extrema (título 10× body)
- Negative space estratégico (60%+ whitespace)
- Zero decoração, tudo serve conteúdo

**Quando usar:** executive summary, strategy deck, research report, corporate narrative.

**Prompt DNA:**
```
Editorial typography grade. Strict grid (8pt baseline). Display typography
as primary visual language. Two-color palette: ink black + single accent.
60%+ whitespace. Type hierarchy extreme (48pt titles over 16pt body).
No decoration. Data viz uses same type language as body text.
```

#### 1.2 — Scientific Data Visualization (Fathom lineage)

**Princípio:** cada pixel carrega informação. Rigor acadêmico com polish de design.

**Características visuais:**
- Palette neutra (grays, navy, 1 highlight color)
- Sans-serif racional (Graphik, GT America, ou Inter com ajuste)
- Charts precisos com axis labels, footnotes, attribution
- Citations integradas ao layout (não afterthought)
- Alta densidade de informação sem clutter

**Quando usar:** data-intensive deck, annual report, research whitepaper, financial analysis.

**Prompt DNA:**
```
Scientific journal meets modern design. Precision data visualization
(charts, timelines, scatter plots). Neutral scheme (grays, navy, one
highlight). Clean rationalist sans-serif. Citation and footnote design
integrated. High information density without clutter.
```

#### 1.3 — Content-First Reading (iA lineage)

**Princípio:** design é invisível. Conteúdo é a única coisa que importa.

**Características visuais:**
- System fonts apenas (SF Pro, Roboto, Inter)
- Blue classical hyperlinks (#0000EE ou variant)
- Reading-optimized line length (66 characters max)
- Progressive disclosure (headlines + collapsible detail)
- Zero visual decoration

**Quando usar:** long-form essay, policy paper, manifesto, quarterly letter.

**Prompt DNA:**
```
Content-first, zero decorative elements. System fonts only. Classic blue
hyperlinks. Reading line length 66 chars. Progressive disclosure layout.
Text-heavy, fast-loading aesthetic. Design disappears to serve text.
```

#### 1.4 — Cartographic Information (Stamen lineage)

**Princípio:** deixar dados se tornarem paisagem tocável.

**Características visuais:**
- Palette quente de dataviz (terracotta, sage, deep blue)
- Padrões algorítmicos/orgânicos
- Camadas de informação como mapa topográfico
- Sensação hand-crafted apesar da precisão digital
- Soft shadows e depth

**Quando usar:** geographic data, network analysis, flow visualization, ecosystem map.

**Prompt DNA:**
```
Cartographic approach to data visualization. Organic, algorithm-generated
patterns. Warm palette (terracotta, sage green, deep blues). Layered
information like topographic maps. Hand-crafted feel. Soft shadows.
```

---

### Escola 2 — Motion Poetics

#### 2.1 — Cinematic Scroll (Locomotive lineage)

**Princípio:** scroll não é navegação, é jornada.

**Características visuais:**
- Parallax depth + motion blur
- Generous vertical spacing
- Dark mode base com strategic glow accents
- Hero sections 100vh
- Film-like scene composition

**Quando usar:** launch site, product announcement, immersive story deck.

**Prompt DNA:**
```
Film-like scene composition with parallax depth. Generous vertical spacing.
Bold typography emerging from darkness. Smooth motion blur. Dark base
with strategic glowing accents. 100vh hero sections.
```

#### 2.2 — WebGL Particles (Active Theory lineage)

**Princípio:** tornar a tecnologia visível = tornar compreensível.

**Características visuais:**
- Sistemas de partículas 3D
- Neon gradients (cyan/magenta/electric blue) on dark
- Mouse-reactive environments
- Depth of field + bokeh
- Glassmorphism com moderação

**Quando usar:** AI product launch, tech demonstration, interactive experience.

**Prompt DNA:**
```
Particle systems representing data flow. 3D visualization in depth space.
Neon gradients (cyan, magenta, electric blue) on dark. Mouse-reactive
environment. Depth of field. Floating UI with measured glassmorphism.
```

#### 2.3 — Algorithmic Generative (Field.io lineage)

**Princípio:** código é o designer.

**Características visuais:**
- Padrões geométricos gerados por algoritmo
- Base monocromática + accent vibrante
- Precisão matemática no spacing
- Voronoi / Delaunay patterns
- Estética de clean code

**Quando usar:** tech brand foundation, generative art cover, computational design.

**Prompt DNA:**
```
Abstract geometric patterns, algorithmically generated. Dynamic
composition feeling computational. Monochromatic base with vibrant
accent. Mathematical precision. Voronoi or Delaunay patterns.
```

#### 2.4 — Narrative Interaction (Resn lineage)

**Princípio:** cada click avança a história.

**Características visuais:**
- Illustrative style + UI elements
- Gamified exploration (progress indicators)
- Warm palette apesar do subject tech
- Character-driven design
- Scroll-triggered reveals

**Quando usar:** education product, course launch, journey-style storytelling.

**Prompt DNA:**
```
Illustrative style mixed with UI. Gamified exploration with progress
indicators. Warm color palette. Character-driven design. Scroll-triggered
animations. Editorial illustration meets product design.
```

---

### Escola 3 — Minimalism

#### 3.1 — Conceptual Monochrome (Experimental Jetset lineage)

**Princípio:** uma ideia = uma forma.

**Características visuais:**
- Primary colors only (red/blue/yellow) + black/white
- Typography como gráfico principal
- Single visual metaphor pro deck inteiro
- Grid-based com deliberate rule-breaking
- Anti-commercial aesthetic

**Quando usar:** cultural deck, exhibition catalog, manifesto, brand identity pitch.

#### 3.2 — Swiss Grid Purity (Müller-Brockmann lineage)

**Princípio:** objetividade é beleza.

**Características visuais:**
- Grid matemático rigoroso (8pt baseline)
- Alinhamento estrito (flush left ou centered)
- Máximo 2 cores (preto + 1 accent)
- Akzidenz-Grotesk ou sans racional similar
- Zero ornamento

**Quando usar:** foundational brand work, timeless archival, high-culture institution.

#### 3.3 — Premium Restraint (Build lineage)

**Princípio:** simples polido é mais difícil que complexo.

**Características visuais:**
- Whitespace generoso (70%+ da área)
- Weight shifts sutis (200 → 600)
- Single accent color usada com parcimônia
- High-end photography aesthetic
- Golden ratio proportions

**Quando usar:** luxury brand, premium pricing pitch, high-ticket service, executive communication.

#### 3.4 — Joyful Minimalism (Sagmeister & Walsh lineage)

**Princípio:** beleza é função com emoção.

**Características visuais:**
- Unexpected color bursts em base minimal
- Handmade elements em digital
- Optimistic visual language
- Experimental typography que mantém legibilidade
- Warmth through deliberate imperfection

**Quando usar:** people-focused brand, mission-driven org, human service deck.

---

### Escola 4 — Experimental Avant-garde

#### 4.1 — Code as Drawing (Lieberman lineage)

**Princípio:** programar é pintar.

**Características visuais:**
- Hand-drawn feel gerado por código
- Preto e branco puros
- Real-time generative patterns
- Sketch-like line quality
- Visible process / grid / construction lines

**Quando usar:** creative tech showcase, coding education, art-code crossover.

#### 4.2 — Parametric Architecture (Kwok lineage)

**Princípio:** beleza do sistema supera beleza do indivíduo.

**Características visuais:**
- Fractal patterns, recursive structures
- High-contrast black and white
- Architectural visualization of data
- Intricate detail rewarding zoom
- Processing / creative coding aesthetic

**Quando usar:** architectural practice, computational design firm, technical depth pitch.

#### 4.3 — Cyber Poetics (Thorp lineage)

**Princípio:** o futuro não é frio, é solitário poético.

**Características visuais:**
- Film-grade lighting
- Warm cyberpunk (orange/teal, NOT cold blue)
- Industrial design meets luxury
- Narrative concept art feel
- Volumetric lighting, god rays

**Quando usar:** film/gaming brand, cyberpunk-adjacent product, cinematic narrative deck.

#### 4.4 — FUI / Fantasy Interface (Territory lineage)

**Princípio:** imaginar UI do futuro hoje.

**Características visuais:**
- Holographic projection aesthetics
- Orange/amber monochrome OR cyan accents
- Multiple overlapping data layers
- Believable future technology
- Technical readouts, data streams

**Quando usar:** sci-fi content, speculative design, experiential tech demo.

---

### Escola 5 — Eastern Philosophy

#### 5.1 — Speculative Design (Takram lineage)

**Princípio:** tecnologia é meio de pensamento.

**Características visuais:**
- Concept prototypes elegantes
- Soft tech aesthetic (rounded corners, gentle shadows)
- Charts como peças de arte
- Neutral natural colors (beige, soft gray, muted green)
- Modest sophistication

**Quando usar:** research-driven product, thoughtful consultancy pitch, strategic foresight deck.

#### 5.2 — Emptiness Design (Kenya Hara lineage)

**Princípio:** design não é preencher, é esvaziar.

**Características visuais:**
- Whitespace extremo (80%+)
- Paper texture em digital
- Camadas de branco (warm white, cool white, off-white)
- Minimal color, se houver muito desaturated
- Zen simplicity

**Quando usar:** museum exhibit, luxury minimalist brand, meditation-adjacent product, art book.

#### 5.3 — Book Architecture (Boom lineage)

**Princípio:** informação tem poética física.

**Características visuais:**
- Non-linear information structure
- Play with edges, margins, boundaries
- Unexpected color combos (pink+red, orange+brown)
- Handcraft translated to digital
- Dense information inviting exploration
- Editorial, unconventional grid

**Quando usar:** annual report art edition, catalog, dense storytelling, archive piece.

#### 5.4 — Ink Wash Digital (Eastern modernist lineage)

**Princípio:** tecnologia precisa de temperatura humana.

**Características visuais:**
- Digital interpretation of ink wash painting
- Soft glow, light diffusion
- Poetic negative space
- Emotional palette (deep blues, warm grays, soft gold)
- Calligraphic influences in typography

**Quando usar:** Asian market, cultural-tech crossover, meditative brand, artisan product.

---

## Prompt composition

Quando filosofia é aplicada a um slide/deck, prompt para AI image generation combina:

```
[Philosophy prompt DNA] + [Scene context] + [Specific content/subject]
```

**Princípio crítico (aprendido do espaço):**
> **Describe mood, not layout.** AI image generation responde melhor a
> 3 frases de emoção do que a 30 linhas de layout specification.

**Good prompt example:**
```
Data visualization with Editorial Typography feel — Bloomberg
Businessweek aesthetic. Key number "45%" dominates the composition
like a magazine headline. Warm cream tones, sharp black typography.
Data tells story of market shift.
```

**Bad prompt example (over-constrained, AI produces empty output):**
```
Professional slide. Navy 60%, white 30%, gold 10%. Title centered 36pt
Helvetica. Two columns below. Left: bullets 18pt. Right: bar chart.
Margins: 40px all sides. Grid 8pt baseline. [...]
```

---

## Workflow integration

### Task trigger: `tasks/advise-design-direction.md` (a ser criado)

Invoked quando:
- `briefing.design_context.status == "absent"`
- AND `briefing.reference_material is None`
- AND user prompted "quero sugestões de estilo" / "não sei o visual"

### Output esperado

User receives 3 filosofias (de 3 escolas diferentes) com:
- Nome da filosofia
- 50-100 palavras explicando por que é fit para este brief específico
- 3-4 características visuais centrais
- 3-5 keywords de mood
- Opcional: 1 obra de referência citada

Plus 3 visual demos (gerados em paralelo quando possível) como thumbnails para escolha rápida.

---

## Related

- `tasks/advise-design-direction.md` (a ser criado) — consumer desta taxonomy
- `data/kbs/KB_07_design_fundamentals.md` — princípios de design base
- `data/ai-slop-blacklist-2026.md` — anti-patterns a evitar mesmo dentro da filosofia escolhida
- `data/kbs/KB_08_ai_generation.md` — prompt engineering para image generation
- `agents/content-architect.md` — integra escolha de filosofia ao grounding
- `agents/design-renderer.md` — aplica no output final
