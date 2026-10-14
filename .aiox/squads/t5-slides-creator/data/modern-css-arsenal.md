# Modern CSS Arsenal — 2026 Features Checklist

> **Purpose:** CSS features that signal "real designer, not AI template" — most are 2023-2025 shipped, underused by AI generation
> **Use as:** reference during design-renderer output + qa-inspector "recommended signal" check

---

## Why this matters

AI-generated HTML defaults to safe/boring CSS (2018-era Flexbox + basic Grid). "Taste tax" features — the ones that took years to ship and years more to adopt — are what distinguish a real designer's output from a template. Using them is cheap and signals quality at multiple levels (client review, peer review, accessibility audits).

**Rule of thumb:** if a CSS feature requires Chrome ≥110 or equivalent, AI is underusing it. Apply deliberately.

---

## Typography

### `text-wrap: balance` (Chrome 114+, Safari 17.4+)

Previne widow/orphan em títulos — última linha não fica com uma palavra solta.

```css
h1, h2, h3 { text-wrap: balance; }
```

**When:** todo `<h1>` até `<h3>`. Custo zero, benefício visual alto.

### `text-wrap: pretty` (Chrome 117+, Safari 17.4+)

Variação para prosa — aplica balance ao último cluster de linhas em parágrafos longos. Cost < `balance` mas pior para títulos.

```css
p { text-wrap: pretty; }
```

**When:** corpo de texto denso (blog, long-form slide com bullet lists).

### `text-spacing-trim: space-all` + `hanging-punctuation: first` (CJK)

Tipografia chinesa/japonesa/coreana — apara pontuação wide e pendura leading quotes fora da coluna.

```css
p { 
  text-spacing-trim: space-all;
  hanging-punctuation: first;
}
```

**When:** qualquer content em CJK (relevante para expansão multi-lang). Também útil em PT/EN com aspas tipográficas `「」` ou `""`.

### Variable fonts para hero weight-animation

```css
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@100..900&display=swap');

.hero-title {
  font-family: 'Inter Tight', sans-serif;
  font-weight: 300;
  transition: font-weight 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.hero-title:hover {
  font-weight: 900;
}
```

**When:** landing page hero, title slides de decks premium. Uma variable font no lugar de 4 static weights.

---

## Layout

### `grid-template-areas` (named grid)

Código de layout legível como diagrama:

```css
.page {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  grid-template-columns: 240px 1fr 320px;
  grid-template-rows: auto 1fr auto;
  gap: 24px;
}

.page > header { grid-area: header; }
.page > main   { grid-area: main;   }
.page > aside  { grid-area: aside;  }
```

**When:** page layouts, dashboards, admin panels, email templates.

### `grid-template-rows: subgrid` (Firefox 71+, Safari 16+, Chrome 117+)

Child elements alinham com parent grid — resolve cards de alturas diferentes.

```css
.card-grid { 
  display: grid; 
  grid-template-rows: auto auto auto;
  gap: 16px;
}
.card { 
  display: grid; 
  grid-template-rows: subgrid; 
  grid-row: span 3; 
}
```

**When:** card grids onde alinhamento vertical entre cards importa (titles alinhados, body alinhado, CTAs alinhados).

### `@container` queries (Chrome 105+, Safari 16+)

Responsive ao tamanho do CONTAINER, não do viewport. Mudança arquitetural.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 500px) {
  .card { flex-direction: row; }
}
```

**When:** componentes reutilizáveis em contextos de largura variável (sidebar vs full-width).

---

## Color & Visual

### `color-mix()` + `oklch()`

Cores matemáticas sem entrar em temas custom.

```css
:root {
  --primary: oklch(0.65 0.18 25);  /* terracotta warm */
}

.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}

.button-muted {
  background: color-mix(in oklch, var(--primary) 30%, white);
}
```

**When:** hover states, muted variants, semantic color variations. **OKLCH** vs HSL: OKLCH mantém perceived lightness constante ao rodar o hue — HSL não.

### `backdrop-filter` com `color-mix` (glassmorphism restraint)

Efeito vidro moderno — mas USAR COM PARCIMÔNIA (anti-slop: se tudo é glassmórfico, nada é especial).

```css
.header-glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
  border-bottom: 1px solid color-mix(in oklch, black 8%, transparent);
}
```

**When:** **no máximo 1 elemento por página** — header, modal overlay, toast. Nunca em cards em massa.

---

## Conditional

### `:has()` selector (Chrome 105+, Safari 15.4+)

Parent selector real — antes só era possível com JS.

```css
/* Card com imagem não tem padding top */
.card:has(> img) { padding-top: 0; }

/* Form com erro tem border vermelha */
.form:has(input:invalid) { border-color: var(--danger); }

/* Title slide com subtitle tem font-size maior */
.slide:has(.subtitle) h1 { font-size: 72px; }
```

**When:** conditional styling baseado em children. Elimina classe-gymnastics tipo `.card.has-image`.

---

## Motion & Transition

### `@view-transition` (Chrome 126+, Safari 18+)

Smooth transition entre navegações sem SPA.

```css
@view-transition { 
  navigation: auto; 
}

::view-transition-old(root) { animation: fadeOut 0.3s; }
::view-transition-new(root) { animation: fadeIn 0.3s; }
```

**When:** multi-page sites que querem feel de SPA sem o custo arquitetural. Para decks multi-file, pode dar continuity visual entre slides em PDF-view.

### `scroll-timeline` + `animation-timeline` (Chrome 115+)

Animações conectadas a scroll position — antes só via IntersectionObserver + JS.

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}

.section {
  animation: fadeInUp 1s forwards;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

**When:** long-form sites, scroll-driven narrativa em decks single-page.

---

## Details (signature polish)

### `scrollbar-width: thin` + `scrollbar-color`

Scrollbar custom sem webkit-scrollbar prefix.

```css
* { 
  scrollbar-width: thin; 
  scrollbar-color: #666 transparent; 
}
```

**When:** sempre. Não custa nada, faz diferença em reviews "pixel-perfect".

### `::marker` pseudo-element

Customizar bullets de `<ul>` / `<ol>` sem pseudo-elements custom.

```css
li::marker { 
  color: var(--primary); 
  font-size: 1.1em;
}
```

**When:** editorial lists, bullet lists em decks.

### `accent-color`

Unifica color de native form controls.

```css
:root { accent-color: oklch(0.65 0.18 25); }
```

**When:** form-heavy pages. Um token resolve checkboxes, radios, progress bars.

---

## Print (underused in decks)

### `@page` + `break-after: page`

Controle page-break em PDF export.

```css
@page { 
  size: 1920px 1080px; 
  margin: 0; 
}

.slide { 
  page-break-after: always; 
  break-after: page; 
}

.slide:last-child { 
  page-break-after: auto; 
  break-after: auto; 
}
```

**When:** qualquer deck exportado para PDF (ver `data/shadow-dom-pdf-troubleshooting.md` para casos edge).

---

## Anti-patterns

| Feature | Por que NÃO usar (mesmo sendo moderno) |
|---|---|
| `container-type: size` (2D container) | Invalidation performance horrível. Use só `inline-size` (1D). |
| Nested CSS (`.card { .title { ... } }`) | Polifilled, mas AI abusa → output torna-se incompreensível. Prefira flat. |
| `field-sizing: content` em `<textarea>` | Chrome 123+ só — fallback chato em Safari. Não depender. |
| `round()` em CSS | Interesting em teoria, quase sempre desnecessário em prática. |

---

## Integration com qa-inspector

Adicionar check opcional (não killer_item — aspirational signal):

```yaml
qa_checks:
  - id: "CSS-ARSENAL-001"
    description: "text-wrap: balance em headings"
    severity: "recommendation"
    
  - id: "CSS-ARSENAL-002"  
    description: "oklch() em semantic colors (ou hsl acceptable)"
    severity: "recommendation"
    
  - id: "CSS-ARSENAL-003"
    description: "scrollbar-width em body ou main scroll containers"
    severity: "recommendation"
```

Score agregado: se deck usa ≥ 4 arsenal features → "Modern CSS Discipline: STRONG signal".

---

## References

- [MDN CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) — canonical reference
- [State of CSS 2025](https://2025.stateofcss.com) — adoption statistics
- `data/scale-standards.yaml` (related: typography standards)
