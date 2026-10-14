# KB_08: AI Image Generation Master - Elite Prompt Engineering

## VISÃO GERAL

Este é o Knowledge Base definitivo para geração de imagens com IA no contexto de apresentações executivas de consultoria estratégica. Cada prompt deve resultar em imagens indistinguíveis de fotografia profissional ou ilustração editorial de publicações como Bloomberg, McKinsey Quarterly, Harvard Business Review.

**Padrão de qualidade:** As imagens devem parecer ter sido criadas por:
- Fotógrafo profissional contratado especificamente para o projeto ($5000/dia)
- Ilustrador editorial de revista Tier-1 ($3000 por ilustração)
- 3D artist com portfólio em empresas Fortune 500

**Ferramentas cobertas:**
- Midjourney v6+ (recomendado para ilustrações e conceitos)
- DALL-E 3 (recomendado para composições complexas e texto)
- Stable Diffusion XL (recomendado para controle máximo)

---

## SEÇÃO 1: ANATOMIA DE UM PROMPT ELITE

### 1.1. Estrutura Completa

```
[ESTILO VISUAL] +
[ASSUNTO DETALHADO] +
[COMPOSIÇÃO E ENQUADRAMENTO] +
[AMBIENTE/CONTEXTO] +
[ILUMINAÇÃO ESPECÍFICA] +
[PALETA DE CORES COM HEX] +
[MOOD/ATMOSFERA] +
[QUALIDADE E RESOLUÇÃO] +
[PARÂMETROS TÉCNICOS] +
[NEGATIVE PROMPT/EXCLUSÕES]
```

**Cada componente é OBRIGATÓRIO. Nenhum pode ser omitido em prompts de produção.**

---

### 1.2. COMPONENTE 1: Estilo Visual

**Objetivo:** Definir linguagem visual dominante

**Categorias principais:**

**A) FOTOGRAFIA**

```
- corporate photography
  Uso: Pessoas em ambiente business, escritórios, meetings
  Exemplo: "corporate photography of diverse executive team"

- architectural photography
  Uso: Espaços, edifícios, facilities
  Exemplo: "architectural photography of modern office interior"

- product photography
  Uso: Objetos, devices, physical products
  Exemplo: "product photography of technology devices on desk"

- editorial photography
  Uso: Narrativo, storytelling, magazine-quality
  Exemplo: "editorial photography for business magazine"

- lifestyle photography
  Uso: Pessoas em situações naturais/autênticas
  Exemplo: "lifestyle photography of team collaboration"
```

**B) ILUSTRAÇÃO**

```
- isometric illustration
  Uso: Diagramas, processos, systems thinking
  Exemplo: "isometric illustration of supply chain network"

- flat design illustration
  Uso: Simplicidade, clareza, modernidade
  Exemplo: "flat design illustration of customer journey"

- line art illustration
  Uso: Elegância, minimalismo, sofisticação
  Exemplo: "line art illustration of business concept"

- editorial illustration
  Uso: Conceitual, interpretativo, thought leadership
  Exemplo: "editorial illustration for Harvard Business Review"

- infographic style illustration
  Uso: Data-driven, educacional, informativo
  Exemplo: "infographic style illustration of market dynamics"
```

**C) 3D/CGI**

```
- 3D render, Cinema4D aesthetic
  Uso: Tech-forward, futurista, premium
  Exemplo: "3D render of abstract business concept, Cinema4D style"

- product visualization
  Uso: Realismo fotográfico de objetos
  Exemplo: "photorealistic product visualization"

- abstract 3D composition
  Uso: Conceitual, artístico, não-literal
  Exemplo: "abstract 3D composition representing growth"
```

---

### 1.3. COMPONENTE 2: Assunto Detalhado

**Princípio:** Seja ULTRA específico. Vague input = vague output.

**Ruim (vago):**
```
business meeting
```

**Bom (específico):**
```
diverse group of 6 executives (3 women, 3 men; ages 35-60; representing
African, Asian, Hispanic, and Caucasian ethnicities) in strategic planning
session around modern glass conference table, gesturing toward large digital
screen showing abstract data visualizations
```

**Especificidade em PESSOAS:**

Sempre detalhar:
- **Número exato:** "6 people" não "several people"
- **Diversidade de gênero:** "50% women" ou "3 women, 3 men"
- **Diversidade étnica:** "multi-ethnic: 2 African descent, 1 East Asian, 1 South Asian, 1 Hispanic, 1 Caucasian"
- **Idade aproximada:** "ages 30-50" ou "mid-40s professional"
- **Atitude corporal:** "confident posture, arms crossed" ou "engaged, leaning forward"
- **Vestimenta:** "professional business attire (navy suits, white blouses)" ou "business casual"

**Especificidade em OBJETOS:**

Sempre detalhar:
- **Quantidade:** "5 glass blocks" não "some blocks"
- **Material:** "frosted glass with gradient fill" não "glass"
- **Tamanho relativo:** "2m diameter sphere" ou "small 10cm cubes"
- **Posição:** "arranged in ascending pattern from left to right"
- **Estado:** "semi-transparent, overlapping"

---

### 1.4. COMPONENTE 3: Composição e Enquadramento

**ÂNGULOS DE CÂMERA:**

```
top-down view / bird's eye view
  Uso: Overview, organização espacial, patterns
  Exemplo: "top-down view of organized workspace"

eye-level / straight-on
  Uso: Neutro, jornalístico, documental
  Exemplo: "eye-level shot of office interior"

low angle / worm's eye view
  Uso: Grandiosidade, poder, monumentalidade
  Exemplo: "low angle shot of skyscraper looking up"

high angle / elevated perspective
  Uso: Contexto amplo, visão de conjunto
  Exemplo: "high angle view of factory floor"

Dutch angle / tilted
  Uso: Tensão, dinamismo (usar raramente)
  Exemplo: "15° Dutch angle for dramatic effect"

over-the-shoulder
  Uso: Perspectiva pessoal, imersão
  Exemplo: "over-the-shoulder view of person using laptop"
```

**ENQUADRAMENTOS (para pessoas):**

```
extreme close-up (ECU): Apenas rosto ou detalhe específico
close-up (CU): Rosto completo com pequeno espaço ao redor
medium close-up (MCU): Cabeça e ombros
medium shot (MS): Cintura para cima
medium long shot (MLS): Joelhos para cima
long shot (LS): Corpo inteiro
extreme long shot (ELS): Corpo inteiro com ambiente amplo
```

**REGRAS DE COMPOSIÇÃO:**

```
rule of thirds
  Dividir frame em grade 3×3, posicionar elementos chave nas interseções

golden ratio / golden spiral
  Proporção 1:1.618 para harmonia natural

centered composition
  Formal, simétrico, estático (bom para title slides)

frame within frame
  Usar elementos arquitetônicos como moldura (portas, janelas)

leading lines
  Linhas que guiam olho para ponto focal

negative space
  Espaço vazio intencional para ênfase e respiro
```

---

### 1.5. COMPONENTE 4: Ambiente e Contexto

**AMBIENTES CORPORATIVOS:**

```
modern glass-walled office
  "modern glass-walled office with floor-to-ceiling windows overlooking
   city skyline, minimalist furniture (white desks, ergonomic chairs),
   indoor plants, polished concrete floors"

traditional executive boardroom
  "traditional executive boardroom with dark walnut wood paneling,
   large rectangular table (seats 16), leather chairs, subtle brass accents"

tech startup workspace
  "open-plan tech startup workspace with exposed brick walls,
   industrial-style lighting, collaborative zones with whiteboards,
   standing desks, casual breakout areas"

co-working space
  "modern co-working space with modular furniture, acoustic phone booths,
   mix of individual and group work areas, natural materials (wood, plants)"
```

**AMBIENTES ABSTRATOS:**

```
clean white void / limbo
  "pure white background, no horizon line, infinite space feeling,
   soft ambient lighting creating subtle shadow beneath subject"

gradient background
  "soft gradient background transitioning from [color HEX] at top
   to [color HEX] at bottom, smooth transition, no texture"

minimal geometric environment
  "minimalist environment with subtle grid pattern on floor,
   single accent wall in [color], otherwise neutral white/gray"
```

---

### 1.6. COMPONENTE 5: Iluminação

**ILUMINAÇÃO NATURAL:**

```
soft diffused window light from [direction]
  "soft natural light from large windows camera-left, diffused through
   sheer curtains, creating gentle shadows, golden hour warmth"

golden hour sunlight
  "warm golden hour sunlight (30 minutes after sunrise), long soft shadows,
   amber color temperature approximately 3500K"

overcast daylight
  "even diffused daylight from overcast sky, no harsh shadows,
   soft and flattering, color temperature 6500K neutral"

blue hour ambient
  "blue hour twilight (30 min after sunset), cool blue ambient light,
   interior artificial lights creating warm contrast"
```

**ILUMINAÇÃO ARTIFICIAL DE ESTÚDIO:**

```
three-point lighting setup
  "classic three-point studio lighting: key light camera-left at 45°,
   fill light camera-right at half intensity, backlight from behind-right
   creating rim light separation"

soft box lighting (sem sombras duras)
  "large soft box main light directly above and in front, creating
   even illumination with minimal shadows, commercial photography style"

dramatic single-source lighting
  "single spotlight from top-right creating dramatic shadows,
   high contrast, chiaroscuro effect, theatrical mood"

rim lighting / backlight
  "strong backlight creating bright outline around subject,
   separating from background, dramatic silhouette effect"
```

**ILUMINAÇÃO ESPECIAL/CONCEITUAL:**

```
volumetric lighting / god rays
  "volumetric light rays visible in atmosphere, streaming through
   windows, dust particles catching light, ethereal quality"

neon accent lighting
  "neon strip lighting in [color HEX], creating sci-fi ambiance,
   reflections on glossy surfaces, futuristic mood"

motivated lighting (source justified)
  "lighting appears to come from practical sources in scene (desk lamps,
   screens, windows), natural and realistic"
```

---

### 1.7. COMPONENTE 6: Paleta de Cores (SEMPRE com HEX)

**Nunca:** "blue and green colors"
**Sempre:** "color palette: primary #003B5C (navy blue), secondary #00A86B (emerald green), accents #FFA000 (amber)"

**PALETAS PRÉ-DEFINIDAS POR CONTEXTO:**

**Consultoria Clássica (McKinsey style):**
```
color palette: primary #003B5C (navy blue), secondary #6E6E6E (medium gray),
accent positive #00A86B (emerald green), accent negative #C8102E (crimson red),
background #FFFFFF (white) to #F5F5F5 (light gray)
```

**Tech/Startup:**
```
color palette: electric blue #0066FF, cyan #00E5FF, purple #6C63FF,
dark background #0A0A0A, white accents #FFFFFF
```

**Financial Services:**
```
color palette: deep navy #001F3F, forest green #00563F, gold #D4AF37,
burgundy red #8B0000 (for negatives), off-white #F9F9F9
```

**Healthcare/Pharma:**
```
color palette: calming teal #00897B, soft lavender #7E57C2,
warm terracotta #D84315 (accents), clean white #FFFFFF,
nature green #2E7D32
```

**Sustentabilidade/ESG:**
```
color palette: earth green #2E7D32, ocean blue #00695C,
sun yellow #F9A825, natural beige #EFEBE9, deep forest #1B5E20
```

---

### 1.8. COMPONENTE 7: Mood e Atmosfera

**Especificar emoção desejada:**

```
professional and trustworthy
innovative and forward-thinking
warm and approachable yet professional
serious and authoritative
dynamic and energetic
calm and reassuring
premium and exclusive
optimistic and aspirational
analytical and data-driven
```

**Combinações poderosas:**

```
"professional yet approachable, avoiding stiffness"
"innovative but credible, not sci-fi"
"premium without being ostentatious"
"serious but not intimidating"
```

---

### 1.9. COMPONENTE 8: Qualidade e Resolução

**SEMPRE incluir modifiers de qualidade:**

```
ultra-sharp focus, high detail, 8K resolution
professional photography, editorial quality
photorealistic rendering, sub-surface scattering
award-winning composition
magazine-worthy quality
shot on [Hasselblad H6D / Canon EOS R5 / Sony A7R IV / Phase One XF]
rendered in [Cinema4D / Octane / V-Ray / Unreal Engine 5]
```

---

### 1.10. COMPONENTE 9: Parâmetros Técnicos

**MIDJOURNEY:**

```
--ar 16:9                # Aspect ratio para slides
--ar 4:3                 # Aspect ratio clássico
--ar 3:2                 # Fotografia editorial
--ar 1:1                 # Quadrado (ícones, perfil)
--ar 21:9                # Ultra-wide (hero images)

--style raw              # Menos estilização, mais literal (RECOMENDADO business)
--style default          # Estética Midjourney clássica

--stylize 0-1000         # Interpretação artística (50-250 para business)
--chaos 0-100            # Variação (0 para consistência)
--quality 2              # Máxima qualidade
--seed 12345             # Reprodutibilidade

--no text, people, logos # Exclusões

--v 6.0                  # Versão do modelo
```

**DALL-E 3:**

```
Size: 1792×1024 (landscape, para slides 16:9)
Size: 1024×1792 (portrait, vertical)
Size: 1024×1024 (square)

Quality: hd (sempre usar)

Style hints no prompt:
"in the style of professional corporate photography"
"editorial illustration for business magazine"
"photorealistic architectural visualization"
```

**STABLE DIFFUSION:**

```
Steps: 40-50 (qualidade otimizada)
CFG Scale: 7-10 (aderência ao prompt)
Sampler: DPM++ 2M Karras (fotorrealismo) ou Euler a (ilustração)
```

---

### 1.11. COMPONENTE 10: Negative Prompt

**SEMPRE incluir para evitar problemas comuns:**

```
--no watermark, text, words, letters, numbers, typography, signature,
logo, brand name, copyright mark, ugly, blurry, low quality, low resolution,
pixelated, distorted, deformed, disfigured, amateur, oversaturated,
undersaturated, noise, grain, artifacts, jpeg artifacts, duplicate elements,
cropped edges, cut off, draft quality, cartoon (unless intended),
anime (unless intended), 3D render (unless intended), unrealistic proportions,
cluttered, messy, chaotic
```

**Para imagens com PESSOAS, adicionar:**

```
--no distorted faces, asymmetric eyes, asymmetric features, extra fingers,
missing fingers, extra hands, extra arms, extra legs, fused fingers,
mutated hands, poorly drawn hands, poorly drawn faces, bad anatomy,
bad proportions, deformed body, disfigured, duplicate people,
mannequin-like, plastic skin, uncanny valley
```

---

## SEÇÃO 2: BIBLIOTECA DE PROMPTS POR CATEGORIA

### 2.1. CONCEITOS ABSTRATOS DE NEGÓCIOS

#### CRESCIMENTO / GROWTH

**Variação A - Escada Isométrica:**

```
Isometric 3D illustration of business growth concept, ascending staircase
made of transparent frosted glass blocks (each block 1m × 1m × 0.3m), 5 steps
increasing in height, each step contains floating data visualization elements
(abstract charts, percentage numbers: 23%, 45%, 67%, 89%, increasing from
bottom to top), numbers in Helvetica Neue Bold visible through glass, small
abstract human figure silhouette (gender-neutral, 1.8m tall suggested scale,
#003B5C navy blue solid color) climbing at mid-point on step 3, surrounding
environment has floating geometric shapes (10-15 spheres and cubes of varying
sizes 10cm-40cm, #00A86B emerald green with 40% opacity) representing
opportunities, color palette (primary #00A86B emerald green for steps,
secondary #FFFFFF white background, accent #FFD700 gold for data points),
soft gradient background (pure white #FFFFFF at top transitioning to very
light gray #F8F8F8 at bottom), each glass block casts subtle drop shadow
(20% opacity, 15px blur, 10px offset down-right), ultra-modern corporate
aesthetic, clean minimalist composition, vector art style with slight 3D depth,
professional infographic quality, --ar 16:9 --style raw --stylize 300
--no people faces, detailed human features, text labels, complex background
patterns, realistic textures, shadows under figure --v 6.0
```

**Variação B - Montanha Gráfico:**

```
Conceptual photorealistic landscape where mountain range forms shape of
ascending line graph, shot from ground level viewpoint looking up at peaks,
mountains progressively increase in elevation from left to right (heights
suggesting 2000m, 3000m, 4500m, 6000m), representing exponential growth
trajectory, summit of tallest peak (right side) catching dramatic golden hour
sunlight (warm #FFA000 amber glow), mid-elevation areas in transitional light
(mix of shadow and highlight), valleys between peaks in cool shadow tones
(#003B5C navy blue), few wispy clouds at mid-altitude (3000m level) adding
depth, sky gradient (deep blue #001F3F at zenith transitioning to light
cyan #E0F7FA at horizon), composition emphasizes scale and upward progression,
dramatic perspective making viewer feel small before achievement metaphor,
shot on Hasselblad H6D, 28mm wide-angle lens, f/8 for deep depth of field,
landscape photography, editorial quality for business magazine cover,
color grading (slight cool-warm contrast, teal shadows, amber highlights),
--ar 3:2 --style raw --quality 2 --no people, buildings, infrastructure,
text, ski resorts, snow vehicles, visible trails, modern elements
```

**Variação C - Setas e Barras Minimalistas:**

```
Minimalist 3D render of growth arrow composed of stacked bar chart elements,
arrow pointing upward at 45° angle, arrow body formed by 5 bars increasing in
width and height (widths: 1.5cm, 2cm, 2.5cm, 3cm, 3.5cm; heights: 10cm, 15cm,
22cm, 30cm, 40cm), each bar segment is transparent glass material with gradient
fill (bottom #003B5C dark blue 80% opacity transitioning to top #00E5FF bright
cyan 60% opacity), internal glow effect suggesting energy/momentum, bars have
2mm gap between segments showing separation, arrow head is solid geometric shape
(equilateral triangle 8cm sides) in bright #00E5FF cyan, entire composition
floats above minimal environment (single ground plane with subtle grid pattern
in very light gray #F0F0F0, grid lines 1mm width 10% opacity), background is
pure white void (#FFFFFF), single studio light from top-right at 60° creating
soft shadows beneath each bar (shadow opacity 15%, blur 20px), ultra-clean
corporate 3D aesthetic, rendered in Cinema4D with Octane, photorealistic
materials with slight stylization, --ar 16:9 --stylize 200 --quality 2
--no text, numbers, people, complex environment, multiple objects beyond arrow,
background patterns --v 6.0
```

---

#### TRANSFORMAÇÃO DIGITAL

```
Split-screen composition showing analog-to-digital transformation journey,
image divided vertically with clear demarcation line at center (50/50 split),
LEFT SIDE (40% of width): grayscale desaturated illustration of traditional
analog office circa year 2000, elements include beige filing cabinets (4
visible, stacked papers on top), paper document stacks (manila folders, loose
papers), CRT computer monitors (bulky, showing green-screen DOS interface
suggestion), landline desk phone (corded, 1990s style), fax machine, overhead
fluorescent lighting (harsh and flat), overall color treatment (complete
desaturation, shades of gray #808080 to #D3D3D3), slightly faded appearance
suggesting past, RIGHT SIDE (40% of width): vibrant full-color modern digital
workspace, elements include floating cloud storage icons (3D isometric cubes
with cloud symbol), holographic interface screens (semi-transparent displays
showing abstract colorful data visualizations), wireless devices (sleek laptop,
tablet, smartphone arranged on clean desk), AI assistant symbol (abstract
brain-circuit hybrid icon), collaborative digital whiteboard, color palette
(electric blue #0066FF primary, bright cyan #00E5FF secondary, white #FFFFFF
background, accent purple #6C63FF), modern LED panel lighting (soft and even),
CENTER TRANSITION ZONE (20% of width, 10% on each side of center line):
morphing effect where analog elements dissolve into digital particles, visual
effect showing papers fragmenting into pixels/data bits, pixel size increasing
from left (2px) to right (8px then dispersing), color gradient in transition
zone from desaturated #808080 (left edge) through transitional teal #4ECDC4
(center) to vibrant blue #0066FF (right edge), particle flow direction left-to-right
suggesting transformation in progress, professional isometric perspective (30°
angle, consistent across both sides), ultra-high contrast between sides
(grayscale vs vibrant color), sharp clean vector art style, editorial illustration
for technology publication, --ar 21:9 --stylize 400 --no people, visible brand
names, readable text on screens, realistic office clutter, photographic elements
--v 6.0
```

---

#### ESTRATÉGIA / DECISION-MAKING

```
Top-down aerial view of premium chess board in strategic mid-game position,
shot from directly above (90° angle looking down), board positioned center-frame,
oversized scale suggested by perspective (board appears 2m × 2m, human scale
would be tiny), pieces arranged in complex strategic formation showing
competitive dynamics (12 pieces visible: 6 white, 6 black, positioned in
clusters suggesting territorial control), chess pieces reimagined as abstract
modern architectural towers (not traditional chess shapes), varying heights
representing organizational hierarchy or market position (tallest 20cm for kings,
medium 12-15cm for major pieces, shortest 8cm for pawns), material treatment
(white pieces: frosted glass with subtle internal glow #FFFFFF, semi-transparent
70% opacity, black pieces: polished obsidian #1A1A1A, reflective with sharp
highlights), board square colors (navy blue #003B5C for dark squares with matte
finish, medium gray #6E6E6E for light squares with slight sheen), dramatic
single-point lighting from directly overhead (1m above board center), creates
long dramatic shadows radiating outward from pieces (shadows 40% opacity,
sharp-edged due to direct light, extending 30-40cm from piece bases), key piece
in strategic position (white king, center-right area) in sharp focus, other
pieces have very slight blur suggesting selective depth of field (simulating
f/2.8 aperture), surrounding environment beyond board edges is pure black void
(#000000, no horizon line, pieces float in darkness), minimalist high-concept
aesthetic, photorealistic rendering with slight stylization (materials are
realistic but composition is surreal), Cinema4D rendering with Octane or V-Ray,
subsurface scattering on glass pieces, ray-traced reflections on polished
surfaces, --ar 16:9 --style raw --quality 2 --no traditional chess piece shapes
(horses, crosses), people, hands, numbers, text, game clock, multiple light
sources, color on board --v 6.0
```

---

### 2.2. INDÚSTRIAS ESPECÍFICAS

#### FINANCIAL SERVICES - Modern Banking Interior

```
Wide-angle architectural photograph of contemporary bank branch interior,
ultra-modern design language, space dimensions suggested 25m wide × 40m deep ×
5m ceiling height, soaring ceiling height emphasized by vertical composition,
geometric skylight feature (steel frame construction in matte black #2C2C2C,
rectangular panels 2m × 3m each in 3×4 grid, frosted white translucent glass
panels) centered on ceiling casting dramatic natural light patterns onto floor
below, floor is polished large-format marble tiles (Calacatta white with subtle
gray veining #F5F5F5, high-gloss finish creating reflections), customer service
area features 4 circular service pods (futuristic modular design, 3m diameter
each, white Corian® solid surface exterior, integrated touchscreen displays
embedded flush in surface showing abstract data visualizations in #00A86B green
and #0077BE blue, no readable text), 3-4 customers visible as intentionally
motion-blurred silhouettes (1-2 second exposure blur suggesting movement,
preserving anonymity, diverse body types and clothing colors), customers
interacting with wall-mounted digital kiosks (sleek 55-inch vertical touchscreens,
minimal bezels, white housing), holographic-style financial charts appear to
float in air above service pods (semi-transparent overlays in post-production
aesthetic, 40% opacity, showing abstract ascending line graphs and circular
progress indicators in #00A86B emerald green and #0077BE blue, no specific
numbers), color scheme (primary: deep navy #001F3F accent wall behind service
pods, secondary: brushed aluminum #C0C0C0 for fixtures and pod bases, dominant
white #FFFFFF surfaces throughout, strategic gold #D4AF37 accents on signage
and door handles), architectural photography style (emphasis on lines, symmetry,
and light), shot on Canon EOS R5, 16-35mm f/2.8 L lens at 16mm for dramatic
perspective, f/8 for front-to-back sharpness, HDR processing (5-bracket exposure
merge for detail in highlights and shadows), natural window light from right
side (large floor-to-ceiling windows 8m tall, diffused through sheer white
blinds) combined with artificial LED panel lighting from ceiling, color
temperature balanced 5500K neutral, editorial quality for architectural digest
or banking industry publication, --ar 21:9 --style raw --quality 2 --no clutter,
visible brand logos, traditional teller windows with glass barriers, people faces
in focus, paper documents, old-style furniture, warm color temperature, busy
crowded feeling
```

---

#### TECHNOLOGY - Cloud Infrastructure Diagram

```
Conceptual isometric technical diagram of cloud computing infrastructure,
multi-layered vertical composition showing system architecture (4 distinct
tiers stacked vertically with clear separation), BOTTOM LAYER (physical
infrastructure): 25 server units represented as glowing geometric cubes
(each cube 8cm × 8cm × 8cm, arranged in 5×5 grid pattern, spacing 2cm between
cubes), cube material (dark charcoal gray #2C2C2C solid color with matte finish),
emission glow effect (bright cyan #00E5FF light emanating from geometric line
patterns on cube faces, suggesting circuit pathways, glow intensity 80%, bloom
effect 10px), cube edges highlighted with brighter cyan #00FFFF edge lighting
(2px width), LAYER 2 (network/connectivity, positioned 15cm above bottom layer):
network connections visualized as flowing light trails (curved 3D spline paths,
fiber optic aesthetic, appearing as tubes of light 3mm diameter), trails colored
with gradient (starting cyan #00E5FF at server cubes, transitioning through teal
#00BCD4, ending at purple #6C63FF at top layer), animated flow implied by
gradient direction and particle-like segments, trails connect bottom cubes to
middle layer nodes in organic but organized pattern (not chaotic), LAYER 3
(application/services, 30cm above bottom): 8 larger geometric nodes (octagonal
prisms 12cm wide × 4cm thick, frosted glass material with 60% transparency,
internal glow in purple #6C63FF), arranged in circular pattern, LAYER 4 (top,
user layer, 45cm above bottom): 15 user icons (simple abstract human silhouettes
3cm tall, white #FFFFFF solid color), positioned around perimeter, connected to
layer 3 with thin white lines (1mm), security elements (transparent shield
overlays 20cm × 25cm, hexagonal tessellation pattern etched on surface, green
#00C853 tint 30% opacity, positioned at 2 locations protecting clusters),
background environment (deep gradient from bottom dark purple #4A148C to top
bright cyan #00BCD4, suggesting depth), base platform (dark surface #0A0A0A
with subtle grid lines 50cm × 50cm extending beyond visible frame, grid lines
#FFFFFF 10% opacity 1mm width), entire composition viewed from 30° isometric
angle (classic technical diagram perspective), lighting (no realistic light
sources, elements are self-illuminated/emissive, creating tech aesthetic),
technical illustration style with neon accent lighting, futuristic but professional
(not gaming/entertainment), suitable for enterprise presentation, --ar 16:9
--stylize 300 --no realistic hardware (actual servers, cables), people, hands,
text labels with words, company logos, photorealistic materials, physical
environment, --v 6.0
```

---

### 2.3. PROMPTS PARA PESSOAS EM CONTEXTO CORPORATIVO

#### Leadership Team - Executive Portrait

```
Environmental group portrait of C-level executive leadership team, 6 individuals
total composed in asymmetric staggered formation (not traditional straight line),
POSITIONING: back row 3 people standing (positions: left 1.5m from center, center,
right 1.2m from center), front row 3 people in varied poses (left person seated
on modern stool, center person standing but leaning slightly, right person
seated on arm of minimal chair), vertical stagger creates dynamic composition
with heads at different heights (range 1.4m to 1.8m from ground), DEMOGRAPHICS:
gender balance 50% women (3F, 3M), age distribution (1 person early 30s, 2 people
early 40s, 2 people early 50s, 1 person early 60s), ethnic diversity intentionally
representative (2 African descent, 1 East Asian, 1 South Asian, 1 Hispanic,
1 Caucasian), body types varied (not all slim, representing realistic professional
diversity), ATTIRE: professional business wear with modern interpretation (not
overly formal), women in mix of (navy blazer with white blouse, charcoal suit
with silk top, modern professional dress in teal), men in (navy suit no tie,
charcoal suit with open collar, business casual blazer with dark jeans), color
palette of clothing (navy #003B5C, charcoal #36454F, white #FFFFFF, occasional
accent colors teal #00897B, burgundy #8B0000), EXPRESSIONS: confident yet
approachable natural expressions (slight genuine smiles, not forced/cheesy grins,
engaged eye contact with camera or slight look-away suggesting candid moment),
POSES: varied and natural (person 1: arms crossed confidently, person 2: hands
in pockets relaxed, person 3: one hand on hip, person 4: arms at sides, person 5:
hands clasped in front, person 6: gesturing as if mid-conversation), body language
suggests comfortable collaboration not stiffness, ENVIRONMENT: modern executive
office interior, background features floor-to-ceiling windows (3m × 5m panels,
large-format glass) showing blurred cityscape bokeh (skyscrapers out of focus
creating professional context), interior features one accent wall in corporate
navy blue #003B5C, minimal modern furniture visible but not prominent (glass
coffee table, single modern chair), floor is polished concrete #808080,
LIGHTING: primary natural window light from camera left (large windows, diffused
daylight, soft shadows, golden hour color temperature ~3800K creating warm
flattering skin tones), subtle fill light from camera right (LED panel, 30%
power, prevents shadow side from going too dark), backlight from windows creates
slight rim light on hair (separation from background), lighting ratio 3:1
(not dramatic, professional and flattering), CAMERA: shot on Hasselblad H6D-100c
(medium format, suggests premium quality), 80mm lens (classic portrait focal length),
f/2.8 aperture (shallow depth of field, subjects tack-sharp, background pleasantly
soft), camera height at 1.6m (near eye-level of standing subjects), horizontal
orientation, STYLE: editorial corporate photography for annual report or investor
presentation, color grading (professional teal-orange, slight lift in shadows,
controlled highlights), natural realistic skin tones (avoid over-smoothing),
texture preserved (fabric, skin, hair rendered naturally), --ar 4:3 --style raw
--quality 2 --no everyone looking directly at camera (vary eye lines), forced
corporate smiles, identical poses, all standing in line, props (folders, tablets
being held awkwardly), visible brand logos, overly retouched plastic skin,
HDR overdone look, vignetting
```

---

### 2.4. DATA VISUALIZATION CONCEPTS

#### Network / Connections Visual

```
Abstract 3D network visualization floating in dark void environment, composition
features 35-40 nodes (spherical points) of varying sizes representing data points
or entities in system, NODE SPECIFICATIONS: sizes range from 8cm diameter (minor
nodes, 60% of total) to 40cm diameter (major hub nodes, 5% of total), material
frosted glass with internal volumetric glow effect, semi-transparent 70% opacity
allowing overlap visibility, COLOR CODING by category (Category A nodes: #00BCD4
teal 15 nodes, Category B nodes: #FF6F00 deep orange 12 nodes, Category C nodes:
#7C4DFF vibrant purple 8 nodes, central hub node: #FFEB3B bright yellow 1 node
60cm diameter with stronger pulsing glow suggesting activity), CONNECTION LINES:
thin curved 3D spline paths connecting related nodes (not all-to-all, strategic
connections suggesting relationships), line thickness varies based on relationship
strength (thin 2px for weak connection, medium 5px for moderate, thick 10px for
strong), line color matches source node at 60% opacity with slight gradient to
destination (e.g., teal node connects with teal line fading to receiving node color),
ANIMATION IMPLIED: light particles (small spheres 2mm diameter) traveling along
connection lines from peripheral nodes toward central hub (flow direction from
outside-in), suggests data flow and system activity, particles leave slight
motion trail (3mm trail length) implying speed, SPATIAL ARRANGEMENT: nodes
distributed in 3D space occupying rough spherical volume 2m diameter, denser
concentration near center hub (40% of nodes within 50cm of center), sparser
distribution at periphery creating depth, BACKGROUND ENVIRONMENT: deep space
aesthetic, gradient from very dark blue-black #0D1117 at edges to slightly
lighter deep blue #1A237E near center (suggests depth and focus), no horizon
line, infinite void feeling, LIGHTING: no traditional light sources, all
illumination is emissive from nodes themselves, node glow creates subtle
illumination on nearby nodes (simulating global illumination), creates sci-fi
technical aesthetic, few subtle lens flares (3-4 small starbursts at brightest
node positions, 4-point star pattern, 20% opacity) suggesting camera looking at
bright light sources, PERSPECTIVE: viewed from slight elevated angle (15° above
horizontal looking down at center), camera positioned 3m from center hub,
composition places central hub slightly off-center using rule of thirds (positioned
at right third line vertically centered), STYLE: scientific/technical visualization
aesthetic, clean and professional not gaming/entertainment, suitable for enterprise
presentation about systems, networks, data flow, connections, rendered in Cinema4D
with Octane or similar (high-quality path tracing, volumetric effects),
--ar 1:1 --stylize 250 --quality 2 --no text, labels, UI elements, numbers,
grid background, ground plane, realistic environment, people, hands interacting,
overly complex (keep network readable), --v 6.0
```

---

### 2.5. QUICK REFERENCE - PROMPTS ESSENCIAIS

**Estas são variações rápidas para 80% dos casos:**

#### Fundo Abstrato Corporativo

```
subtle geometric pattern background suitable for business presentation slide,
overlapping translucent circles and hexagons (various sizes 5cm to 20cm),
color palette (#003B5C navy blue at 30% opacity, #E8F4F8 very light blue at
50% opacity, white #FFFFFF base), elements randomly distributed but balanced
composition, minimal professional aesthetic not distracting, suitable as
presentation background layer, --ar 16:9 --stylize 200 --no busy patterns,
high contrast, text, people --v 6.0
```

#### Ícone - Crescimento (linha)

```
minimalist line art icon representing growth concept, upward trending arrow
composed of three ascending bars forming arrow shape, clean geometric design,
outline style only with 2pt line weight, single color #00A86B emerald green,
transparent background, professional corporate aesthetic simple and scalable,
vector art style, --ar 1:1 --stylize 50 --no fill, shadows, gradients, 3D
effects, text, complex details --v 6.0
```

#### Ícone - Inovação (linha)

```
minimalist line art icon of light bulb with radiating lines suggesting innovation
or idea, classic bulb shape (Edison style outline), 4-5 straight lines radiating
outward from bulb (suggesting illumination/inspiration), outline style 2pt line
weight, single color #FFA000 amber, transparent background, clean professional
corporate aesthetic, suitable for business presentation, --ar 1:1 --stylize 50
--no filled areas, shadows, 3D, text, complex background --v 6.0
```

#### Escritório Corporativo Genérico

```
modern corporate office interior, open floor plan workspace, natural daylight
from floor-to-ceiling windows (no direct sun, diffused overcast light), no
people visible (empty space or people completely out of frame), color palette
(white walls #FFFFFF, light wood floors #D4C5B0, navy blue #003B5C accent
furniture), minimalist Scandinavian-influenced design, few green plants (snake
plants, monstera in minimal white planters), clean professional not sterile,
suitable as presentation background image, professional architectural photography
style, --ar 16:9 --style raw --quality 2 --no clutter, visible brand names,
people, desks covered in items, warm yellow lighting, busy feeling
```

---

## SEÇÃO 3: TROUBLESHOOTING - PROBLEMAS COMUNS

### 3.1. Pessoas com Anatomia Distorcida

**PROBLEMA:** Dedos extras, mãos fundidas, proporções incorretas

**SOLUÇÕES:**

**A) Reforçar negative prompt:**
```
--no (bad hands:1.5), (extra fingers:1.5), (fused fingers:1.4),
(mutated hands:1.4), (poorly drawn hands:1.3), missing fingers,
extra limbs, bad anatomy
```

**B) Evitar close-ups de mãos:**
- Manter mãos parcialmente ocultas (in pockets, behind back, holding objects)
- Usar motion blur em mãos se em movimento
- Enquadrar foto de modo que mãos estão na periferia (menos atenção visual)

**C) Mostrar pessoas de longe:**
- Long shot ou extreme long shot (corpo inteiro pequeno no frame)
- Silhuetas (contraluz, sem detalhes anatômicos)
- Motion blur intencional (2 second exposure simulation)

**D) Usar imagens de referência (Midjourney):**
- Fornecer foto real de pose desejada como image prompt (--iw 1.5)

---

### 3.2. Texto Ilegível ou Nonsense

**PROBLEMA:** IA gera texto que parece escrito mas não é legível/coerente

**SOLUÇÕES:**

**A) Sempre incluir em negative prompt:**
```
--no text, words, letters, numbers, typography, readable text,
signage with words
```

**B) Se PRECISA de texto legível:**
- DALL-E 3 é melhor que Midjourney para texto
- Especificar exatamente: "the text 'INNOVATION' in Helvetica Bold appears on wall"
- Aceitar que pode precisar 3-5 tentativas
- Considerar adicionar texto em pós-produção (Photoshop) para controle perfeito

---

### 3.3. Imagens Muito "Stock Photo"

**PROBLEMA:** Resultado parece banco de imagens genérico, não autêntico

**SOLUÇÕES:**

**A) Adicionar detalhes específicos e únicos:**

❌ Generic: "business meeting"
✅ Specific: "strategic planning session where team is gesturing toward
whiteboard filled with post-it notes, coffee cups on table, one person
standing pointing, others leaning forward engaged, natural moment mid-conversation"

**B) Usar "editorial photography" no estilo:**
```
editorial photography for Bloomberg Businessweek, authentic moment
```

**C) Evitar poses clichê no negative prompt:**
```
--no forced smiles, looking at camera while shaking hands, arms crossed
in unison, everyone looking at camera, overly staged
```

**D) Adicionar imperfeição intencional:**
```
slight motion blur on gesturing hands suggesting natural movement,
candid documentary moment, authentic not posed
```

---

### 3.4. Cores Diferentes do Especificado

**PROBLEMA:** HEX codes no prompt mas resultado tem cores diferentes

**SOLUÇÕES:**

**A) Pós-processamento:**
- Usar Photoshop: Image → Adjustments → Selective Color
- Ajustar apenas range de cor problemático
- Color Balance para shift global de temperatura

**B) Aumentar peso de cor no prompt (SD):**
```
(color palette #003B5C navy blue:1.3) (other colors:1.0)
```

**C) Image prompting com swatch de cores (Midjourney):**
- Criar imagem simples com apenas cores desejadas
- Usar como image prompt: `[URL] --iw 1.0` junto com descrição

**D) Multiple generations:**
- Gerar 4-6 variações (seed diferente)
- Selecionar a mais próxima das cores
- Refinar com ajustes sutis no prompt

---

### 3.5. Inconsistência Entre Imagens da Mesma Apresentação

**PROBLEMA:** Cada imagem parece de projeto diferente (estilos incompatíveis)

**SOLUÇÕES:**

**A) Usar mesmo seed quando possível:**
```
primeira imagem: --seed 12345
imagens seguintes: --seed 12345 (mantém consistência de estilo)
```

**B) Criar "base prompt" reutilizável:**

```
[BASE_STYLE]
professional corporate style, editorial quality for business publication,
color palette (#003B5C navy blue, #00A86B emerald green, #6E6E6E gray,
#FFFFFF white), minimalist clean aesthetic, shot on Hasselblad medium format
[END_BASE]

Então cada prompt: [BASE_STYLE] + [específico desta imagem]
```

**C) Documentar todos os parâmetros:**
- Quando primeira imagem for aprovada, salvar prompt COMPLETO + parâmetros
- Reutilizar estrutura exata, mudando apenas conteúdo específico

**D) Batch generation com mesma configuração:**
- Gerar todas imagens de uma vez com prompts similares estruturalmente
- Evita drift de estilo ao longo de sessões diferentes

---

## SEÇÃO 4: WORKFLOWS DE PRODUÇÃO

### 4.1. Processo Completo (Conceito → Entrega)

**PASSO 1: Definição (5 min)**

Responder:
- Qual a mensagem do slide que esta imagem suporta?
- Tipo de imagem: Fotografia? Ilustração? 3D? Abstrato?
- Mood: Formal? Inovador? Tradicional? Tech-forward?
- Cores: Alinhar com paleta da apresentação

**PASSO 2: Rascunho de Prompt (10 min)**

- Escrever prompt seguindo anatomia completa (10 componentes)
- Definir parâmetros técnicos (AR, quality, stylize)
- Escolher ferramenta (MJ para ilustração, DALL-E para complexidade, SD para controle)
- Preparar negative prompt robusto

**PASSO 3: Geração Inicial (5 min)**

- Gerar 4 variações (batch)
- Avaliar contra critérios:
  - Comunica mensagem?
  - Qualidade técnica adequada?
  - Cores aproximadamente corretas?
  - Composição funcional?

**PASSO 4: Refinamento Iterativo (10-20 min)**

- Selecionar melhor das 4 variações
- Identificar o que precisa ajustar:
  - Composição (mudar ângulo, framing)
  - Cores (especificar HEX mais enfaticamente)
  - Detalhes (adicionar ou remover elementos)
  - Iluminação (mais dramática? mais suave?)
- Refinar prompt
- Gerar nova batch (4 variações)
- Repetir até satisfatório (geralmente 2-3 iterações)

**PASSO 5: Upscale e Otimização (5 min)**

- Upscale para resolução final:
  - Apresentação digital: 1920×1080 mínimo (3840×2160 ideal)
  - Impressão: 300 DPI (calcular pixels necessários para tamanho impresso)
- Correção de cor se necessário (Photoshop/Lightroom):
  - Ajustar para match exato de paleta
  - Corrigir exposure/contrast se necessário
- Remover pequenos artefatos (clone stamp, healing brush)
- Salvar em formato adequado:
  - PNG se precisar transparência ou máxima qualidade
  - JPG com quality 90% se otimização de tamanho for importante

**PASSO 6: Documentação (2 min)**

- Salvar prompt final usado
- Salvar todos os parâmetros (seed, stylize, etc.)
- Nomear arquivo: `[NomeProjeto]_Slide[N]_[DescricaoBrave]_v[X].png`
  - Exemplo: `BancoXYZ_Slide07_GrowthChart_v3.png`
- Catalogar em biblioteca para referência futura

**TEMPO TOTAL POR IMAGEM: 37-47 minutos (qualidade elite)**

---

### 4.2. Checklist de Qualidade

**ANTES DE APROVAR IMAGEM, VALIDAR:**

**Técnico:**
- [ ] Resolução mínima atingida (1920px width para digital, 300 DPI para impressão)
- [ ] Sem artefatos visíveis (sem dedos extras, rostos distorcidos, elementos duplicados)
- [ ] Cores alinhadas com paleta (HEX codes próximos ao especificado, ±10% OK)
- [ ] Formato correto (PNG se transparência necessária, JPG se otimização)
- [ ] Aspect ratio compatível com espaço no slide
- [ ] Tamanho de arquivo razoável (<5MB idealmente, <10MB máximo)

**Conteúdo:**
- [ ] Mensagem visual clara e imediata (10 second test: pessoa entende sem explicação?)
- [ ] Não contém texto legível (a menos que intencional e correto)
- [ ] Diversidade apropriada se há pessoas (gênero, etnia, idade)
- [ ] Culturalmente apropriado para audiência (sem símbolos/gestos ofensivos)
- [ ] Profissional (não parece amador, stock photo óbvio, ou AI-generated óbvio)
- [ ] Não distrai do conteúdo principal do slide (é suporte, não protagonista)

**Integração:**
- [ ] Estilo consistente com outras imagens da apresentação
- [ ] Funciona com texto sobreposto (se aplicável, testar contraste)
- [ ] Caption/legenda preparada ("Imagem X.Y - [descrição]")
- [ ] Fonte documentada ("Gerado com [ferramenta], prompt disponível em Appendix")
- [ ] Posição no slide especificada (grid coordinates, dimensões)

---

## SEÇÃO 5: REFERÊNCIA RÁPIDA

### 5.1. Decision Tree - Qual Ferramenta Usar?

```
PRECISA DE ILUSTRAÇÃO/CONCEITO ABSTRATO?
├─ Sim → Midjourney
│   └─ Estilo: isometric, flat design, editorial illustration
│
└─ Não → PRECISA DE FOTOGRAFIA REALISTA?
    ├─ Sim → PRECISA DE TEXTO LEGÍVEL NA IMAGEM?
    │   ├─ Sim → DALL-E 3
    │   └─ Não → Midjourney (--style raw) ou SD (Realistic Vision)
    │
    └─ Não → PRECISA DE CONTROLE MÁXIMO (poses específicas, etc)?
        ├─ Sim → Stable Diffusion + ControlNet
        └─ Não → Midjourney (mais rápido, boa qualidade)
```

### 5.2. Parâmetros Recomendados por Contexto

**Business Standard (maioria dos casos):**
```
Midjourney: --ar 16:9 --style raw --stylize 200 --quality 2 --v 6.0
DALL-E: Size 1792×1024, Quality hd
SD: Steps 40, CFG 7-9, Sampler DPM++ 2M Karras
```

**Illustração Conceitual (mais artístico):**
```
Midjourney: --ar 16:9 --stylize 400 --quality 2 --v 6.0
```

**Fotografia Ultra-realista:**
```
Midjourney: --ar 3:2 --style raw --stylize 100 --quality 2 --v 6.0
SD: Steps 50, CFG 8, Sampler DPM++ SDE Karras, Model: Realistic Vision
```

**Ícones/Símbolos Simples:**
```
Midjourney: --ar 1:1 --stylize 50 --quality 1 --v 6.0
```

---

**FIM DO KB_08**

Total: ~7500 palavras

Este é o guia definitivo para geração de imagens IA em contexto de apresentações executivas elite. Seguir estes padrões garante output visual indistinguível de trabalho profissional contratado.
