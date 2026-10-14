# AI Slop Blacklist — 2026 Consolidated

> **Purpose:** lista canônica de padrões visuais que AI gera por default e que diluem identidade de marca. Governance negativa — "não fazer" > "fazer".
> **Use as:** reference para design-renderer outputs + qa-inspector signal scoring

---

## Why this matters

AI gera o "maior divisor comum visual" do training corpus. O resultado, mesmo quando tecnicamente correto, não carrega informação de marca — qualquer site parece igual a qualquer outro. Anti-slop não é vaidade estética: é **proteção de identidade de marca**.

**Princípio:** se o template é AI-default, e o deliverable precisa ser reconhecível como da marca, então cada default abandonado é um ganho líquido de identidade.

---

## 1. Fonts queimados (2026-expanded)

### Evitar por default

| Font | Motivo | Pode usar se |
|---|---|---|
| **Inter** | AI default #1 para sans-serif. Acaba em ~40% dos outputs AI | Brand spec pede explicitamente (ex: GitHub, alguns SaaS) |
| **Roboto** | Default Android/Material, usado em excesso | Brand é Material-native |
| **Arial / Helvetica** | Sistema default desde 1995. Falta personalidade | Nunca por escolha ativa — só como fallback |
| **System font stack** (`-apple-system, BlinkMacSystemFont, ...`) | "não escolhi fonte" signal | Demo rápido / prototype early-stage |
| **Fraunces** | AI descobriu em 2024, explodiu em 2025. Agora saturated | Brand tem rationale serif editorial (revista, livro) |
| **Space Grotesk** | **Recent AI favorite 2025-2026**. Everywhere em tech landing pages | Explicit brand fit (techy + friendly) |

### Alternativas com personalidade

**Display + body pairings (editorial):**
- Serif display + sans body: Instrument Serif + Inter Tight / Geist Sans
- Classical serif: EB Garamond + Source Sans
- Transitional: Newsreader + Inter

**Display + body pairings (technical):**
- Mono display + sans body: JetBrains Mono + Geist Sans
- Condensed display + sans body: Sora + Inter Tight

**Display + body pairings (elegant):**
- Heavy display + light body: Canela + Freight Text

### Google Fonts cold picks (not yet saturated)

- Instrument Serif (editorial serif, generous)
- Cormorant (display serif, high contrast)
- Bricolage Grotesque (modern sans, rationalist)
- Newsreader (newspaper serif, readable)
- Sohne / Söhne (not on Google — Klim Type, paid)

---

## 2. Gradients — aggressive

### Evitar

- **Purple → pink → blue full-screen** — signature de AI SaaS 2021-2025
- **Rainbow gradient** em qualquer direção
- **Mesh gradient** cobrindo background inteiro
- **Conic gradient** em círculos decorativos (também queimado)

### Quando pode usar gradient

- Hover state sutil em button (primary → primary-dark)
- Subtle background em hero section (2 cores próximas, 5-10% diferença de lightness)
- Data viz (gradient intencional para representar valor)
- Brand signature gradient (se brand spec explícito)

**Regra:** se você adicionou gradient "porque fica bonito", NÃO adicione. Só se resolve problema concreto.

---

## 3. Layouts queimados

### O template morto

```
[ Big Hero com CTA                    ]
[ 3 colunas de features com icons    ]
[ Testimonials carrossel             ]
[ Big CTA again                      ]
[ Footer                              ]
```

**Presente em ~60% dos landing pages AI 2023-2026.** Evitar por default. Se for usar, varie com:
- Hero sem CTA (CTA na sidebar fixa)
- Features como stack vertical editorial (long-form, não colunas)
- Sem testimonials (ou editorial quote único, não carrossel)
- CTA inline no flow, não como section dedicada

### Bento grid em excesso

Bento = mosaic de cards de tamanhos variados. Funciona quando information structure é realmente bento-shape (Apple product pages). Mas AI usa para qualquer landing, mesmo onde structure não pede.

**Pergunta de validação:** "se eu remover a grid bento e apresentar como sections empilhadas, a informação fica pior?" Se não fica pior → não use bento.

### Card grids identical

AI gera N cards idênticos alinhados. Real designers fazem **asymmetric grids**:
- 1 card grande + 3 médios
- 2 primeiros cards com image, 2 últimos só texto
- Um card pode ser full-width quote

---

## 4. Decoration queimada

### Emoji em UI

Exceto brand que assume emoji (Notion, Slack workspace icons), **NÃO**:

- ❌ `🚀 Launch` em button
- ❌ `⚡️ Fast` em feature header
- ❌ `✨ New` em badge
- ❌ `✅` em feature list (usar checkmark SVG ou Unicode ✓)
- ❌ `💡` para "tip" callout (usar ícone de lâmpada real)

### Rounded card + left color border accent

```css
/* SLOP — AI signature 2020-2024 */
.card {
  border-radius: 12px;
  border-left: 4px solid var(--primary);
  padding: 16px;
}
```

**Por que é slop:** AI default desde Material + Tailwind cheatsheets. Alternativas:
- Card full-color background (não border)
- Card com divider top/bottom em vez de left
- Card sem border mas com typography weight contrast
- Card com apenas shadow sutil

### SVG drawing de pessoas/cenas/objetos

Qualquer SVG hand-drawn de humanoide, cena, objeto concreto vira AI slop. Features de face desalinhadas, proporções estranhas.

**Usar SVG só para:**
- Icons 16×16 a 32×32 (de library: Lucide, Phosphor, Heroicons)
- Geometric decoration (circles, lines, patterns)
- Data viz (charts generated by D3/Recharts)

Para imagery de hero, products, scenes: real photography (Wikimedia, Unsplash, Met Museum) ou AI-generated (Flux, Imagen 3) — nunca SVG.

### Over-iconography

**AI default:** toda feature / title / section tem icon associado.
**Result:** visual noise, page parece brinquedo.

**Regra:** icon precisa carregar informação. Se icon é "decorativo" → remover. Se icon é "navegacional" (user clica nele) → manter.

---

## 5. Data slop & Quote slop

### Data slop

- "10,000+ happy customers" — invented
- "99.9% uptime" — sem source
- "500+ integrations" — sem list concreta
- Metric cards com número + icon + word

**Se não tem dado real:** placeholder `[VALIDAR COM CLIENTE: número de customers]`. Nunca inventar.

### Quote slop

- Testimonial inventado com nome genérico ("Sarah, CEO at TechCo")
- Celebrity quote atribuído sem source
- "Industry quote" parafraseado

**Se não tem quote real:** omit section ou placeholder.

---

## 6. Color slop

### Pure black / pure white backgrounds

Nenhum background de peça premium usa `#FFFFFF` ou `#000000`. Tem color temperature — offwhite `#FAFAF7`, soft black `#0A0A0A`, warm white `#FEFEF9`.

**Por que:** AI training corpus tem muita peça com pure tones → pure = cheapness signal.

### Neon cyberpunk (#0D1117 dark mode cliché)

GitHub dark mode conquistou. `#0D1117 + cyan + magenta neon` virou cliché universal.

**Exceção:** developer tool com brand alignment real (não só "tech = blue glow").

### Inventing colors

Não criar palette do zero se não tem brand spec. Usar:
- Radix Colors (open source, accessible, semantic)
- Tailwind default palette (se já no stack)
- Brand palette existente

---

## 7. Quick Decision Cheatsheet

```
Situação                       → Default action
─────────────────────────────────────────────────
Tempted to add gradient?       → NO
Tempted to use emoji in UI?    → NO
Tempted rounded+left-border?   → NO, use other contrast
Tempted SVG hero illustration? → Placeholder ou real photo
Tempted decorative quote?      → Ask user for real quote
Tempted feature icons row?     → Ask if icons add value
Tempted Inter for display?     → Pick something with character
Tempted purple gradient bg?    → Use rationale-backed color
```

**Rule of thumb:** "I think this would make it prettier" → usually AI slop signal. Start simpler, add only on user request.

---

## 8. qa-inspector integration

Adicionar signal scoring (não killer items — aspirational):

```yaml
qa_signals_anti_slop:
  - id: "SLOP-FONT-001"
    description: "Body/display font evita lista queimada (Inter/Roboto/Arial/Fraunces/Space Grotesk)"
    weight: 0.1
    
  - id: "SLOP-GRAD-001"
    description: "Sem mesh gradient ou rainbow bg"
    weight: 0.1
    
  - id: "SLOP-LAYOUT-001"
    description: "Evita template 'hero + 3 col features + testimonials + CTA'"
    weight: 0.15
    
  - id: "SLOP-EMOJI-001"
    description: "Zero emoji em UI (exceto brand-explicit)"
    weight: 0.05
    
  - id: "SLOP-BORDER-001"
    description: "Sem padrão 'rounded card + left border accent' em massa"
    weight: 0.1
    
  - id: "SLOP-IMG-001"
    description: "Sem SVG imagery de humanoides/scenes/objects"
    weight: 0.15
    
  - id: "SLOP-COLOR-001"
    description: "Backgrounds evitam pure #FFF/#000 + evita neon cyber #0D1117"
    weight: 0.1
    
  - id: "SLOP-DATA-001"
    description: "Zero invented stats/quotes/testimonials"
    weight: 0.25

total_score_if_clean: 1.0
threshold_acceptable: 0.7
threshold_excellent: 0.85
```

**Use:** score ≥ 0.7 = release OK, 0.7-0.85 = "good", ≥ 0.85 = "exceptional anti-slop discipline".

---

## 9. Related

- `data/scale-standards.yaml` — typography specs quantitative
- `data/modern-css-arsenal.md` — positive CSS features to adopt
- `data/kbs/KB_07_design_fundamentals.md` — design governance (expand com este file)
- `agents/qa-inspector.md` — signal scoring integration point
