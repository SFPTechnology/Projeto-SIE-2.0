# export-editable-pptx

> **Task type:** Rendering discipline + export pipeline
> **Owner:** `design-renderer`
> **Trigger:** `briefing.normalized.json#delivery_format.primary == "C"` OU `secondary` inclui "C"
> **Requires:** HTML source (multi-file ou single-file) conforme `tasks/decide-slide-architecture.md`

## Purpose

Gerar PPTX com text frames **reais e editáveis** (não screenshot rasterizado). Colegas/cliente abrem o arquivo no PowerPoint/Keynote e conseguem duplo-clique para editar texto, trocar palavras, ajustar copy.

Esta é a diferença entre:
- **Image mode** (fallback): cada slide vira PNG, texto vira pixel, não editável
- **Editable mode** (este task): cada elemento HTML vira objeto PowerPoint nativo (text frame / shape / picture)

## Hard precondition

**Editable PPTX NÃO é pós-processamento.** Precisa ser decidido em `confirm-delivery-format` + HTML escrito desde a primeira linha seguindo 4 constraints abaixo. Tentar converter HTML livre para editable PPTX custa 2-3h de rework por deck.

Se este task é invocado e HTML não segue as 4 constraints, **retornar erro** e escalar para design-renderer reescrever o HTML, não tentar conversão forçada.

---

## 4 Hard Constraints do HTML source

Essas restrições vêm do formato OOXML do PowerPoint projetado para HTML. Não são design choices — são realidade física do destino. Ignorá-las = output quebra.

### Constraint 1 — DIV não pode conter texto solto

Em PPTX, texto vive em text frames. Text frame tem correspondente em HTML: `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`. DIV sozinho **não traduz** para text frame — ele é container, não conteúdo de texto.

```html
<!-- ❌ Quebra -->
<div class="title">Q3 receita cresceu 23%</div>

<!-- ✅ Correto -->
<div class="title"><h2>Q3 receita cresceu 23%</h2></div>

<!-- ✅ Também correto -->
<div class="body"><p>Novos clientes foram o driver principal</p></div>
```

**`<span>` também não serve** para texto principal — span é inline, não se torna text frame independente. Usar span só dentro de `<p>`/`<h*>` para local styling (bold, color).

### Constraint 2 — Sem CSS gradients

PPTX shape fill suporta `solid` e `gradient-fill`, mas o mapping para `linear-gradient(...)` CSS arbitrário não existe. Usar cores sólidas.

```css
/* ❌ Quebra */
.header { background: linear-gradient(to right, #003B5C, #00A86B); }

/* ✅ Cor sólida */
.header { background: #003B5C; }

/* ✅ Stripe de múltiplas cores: flex + child divs cada uma sólida */
.stripe-bar { display: flex; }
.stripe-bar > div { flex: 1; }
.blue { background: #003B5C; }
.green { background: #00A86B; }
```

### Constraint 3 — Background/border/shadow só em DIVs, não em text tags

PPTX separa shape (retângulo com fill) e text frame (texto). Não existe "text frame com fill". Se `<p>` tem background, o renderer tem que inventar uma shape adicional — o que pptxgenjs simples não faz. Resultado: background é perdido.

```html
<!-- ❌ Quebra (background perdido no export) -->
<p style="background: #FFD700; border-radius: 4px;">Highlight crítico</p>

<!-- ✅ Correto (div externa carrega visual, p carrega texto) -->
<div style="background: #FFD700; border-radius: 4px; padding: 8pt 12pt;">
  <p>Highlight crítico</p>
</div>
```

Mesma regra para `border`, `box-shadow`, `outline` — todos em divs, nunca em p/h*.

### Constraint 4 — `<img>` tags, não `background-image`

Imagem em PPTX é picture object. Picture object referencia arquivo de imagem real. `background-image: url(...)` é CSS property, não element — o parser não extrai.

```html
<!-- ❌ Quebra (imagem some no export) -->
<div style="background-image: url('chart.png'); width: 300pt; height: 200pt;"></div>

<!-- ✅ Correto -->
<img src="chart.png"
     style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;" />
```

---

## Canvas dimensions

PPTX usa inch como unidade física. HTML body precisa bater com `presentation.layout` dentro de ±0.1" para o export-validator passar.

| HTML body | Physical inches | pptxgenjs layout | Quando usar |
|---|---|---|---|
| **960pt × 540pt** | 13.333" × 7.5" | `LAYOUT_WIDE` | **Default** (PowerPoint 16:9 moderno) |
| 720pt × 405pt | 10" × 5.625" | custom | Legacy "Widescreen" templates |
| 1920px × 1080px | 20" × 11.25" | custom | **NÃO usar** (non-standard, font fica pequena projetada) |

Body write equivalente (três formas aceitas):

```css
body { width: 960pt;   height: 540pt; }   /* recommended, unit explicit */
body { width: 1280px;  height: 720px; }   /* equivalent em px */
body { width: 13.333in; height: 7.5in; }  /* equivalent em inch */
```

---

## HTML skeleton conforme as 4 constraints

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 960pt; height: 540pt;
    font-family: system-ui, -apple-system, sans-serif;
    background: #FEFEF9;           /* cor sólida, sem gradient */
    overflow: hidden;
  }

  /* DIVs carregam visual (bg/border/shadow) */
  .card {
    position: absolute;
    background: #003B5C;
    border-radius: 4pt;
    padding: 12pt 16pt;
  }
  /* Tags de texto só carregam tipografia */
  .card h2 { font-size: 24pt; color: #FFFFFF; font-weight: 700; }
  .card p  { font-size: 14pt; color: rgba(255,255,255,0.85); }
</style>
</head>
<body>

  <!-- Header: div posiciona, h1/p carregam texto -->
  <div style="position: absolute; top: 40pt; left: 60pt; right: 60pt;">
    <h1 style="font-size: 36pt; color: #1A1A1A; font-weight: 700;">
      Mercado brasileiro crescerá 45% a.a. até 2027
    </h1>
    <p style="font-size: 16pt; color: #555555; margin-top: 10pt;">
      1.7× mais rápido que média global
    </p>
  </div>

  <!-- Card: div visual, h2/p texto -->
  <div class="card" style="top: 130pt; left: 60pt; width: 240pt; height: 160pt;">
    <h2>Driver principal</h2>
    <p>Enterprise segment (+34% QoQ)</p>
  </div>

  <!-- Lista: usar ul/li, PPT converte para bullet text frame -->
  <div style="position: absolute; top: 320pt; left: 60pt; width: 540pt;">
    <ul style="font-size: 16pt; color: #1A1A1A; padding-left: 24pt;">
      <li>Enterprise: +34% QoQ</li>
      <li>SMB: +12% QoQ</li>
      <li>Self-serve: +8% QoQ</li>
    </ul>
  </div>

  <!-- Imagem: img tag real, não CSS background -->
  <img src="charts/q3-revenue.png"
       style="position: absolute; right: 60pt; top: 110pt; width: 320pt; height: 240pt;" />

</body>
</html>
```

---

## Export pipeline

```bash
# 1. Validar HTML antes de exportar
node scripts/validate-pptx-constraints.mjs slides/*.html
# → FAIL se algum <p> com background, div com bare text, etc

# 2. Export editable
node scripts/export-pptx-editable.mjs \
  --slides slides/ \
  --layout LAYOUT_WIDE \
  --out output/deck.pptx
```

Internamente, o exporter:
1. Abre HTML no Playwright
2. Lê `computedStyle` de cada DOM element
3. Mapeia element → PPTX object (text frame / shape / picture)
4. Valida overflow (body size vs layout size)
5. Escreve PPTX via pptxgenjs

---

## Common errors (exporter rejects)

| Erro | Causa | Fix |
|---|---|---|
| `DIV element contains unwrapped text "XXX"` | div com texto direto | Embrulhar em `<p>` ou `<h*>` |
| `CSS gradients are not supported` | `linear-gradient` em style | Cor sólida ou flex+child divs |
| `Text element <p> has background` | `<p>` com background/border/shadow | Mover background para div externa |
| `Background images on DIV elements are not supported` | `background-image: url()` em CSS | Trocar por `<img>` tag |
| `HTML content overflows body by Xpt vertically` | Conteúdo maior que 540pt height | Reduzir densidade ou `overflow: hidden` |
| `HTML dimensions don't match presentation layout` | Body size ≠ LAYOUT | Usar 960pt × 540pt para LAYOUT_WIDE |
| `Text box "XXX" ends too close to bottom edge` | Texto grande a < 0.5" do fundo | Subir o elemento, deixar margem bottom |

---

## qa-inspector integration

Adicionar killer items quando `delivery_format` inclui C:

```yaml
qa_checks_editable_pptx:
  - id: "PPTX-C1"
    description: "Nenhum DIV com texto solto (constraint 1)"
    enforcement: "killer_item"

  - id: "PPTX-C2"
    description: "Zero CSS gradient em .style ou style attr (constraint 2)"
    enforcement: "killer_item"

  - id: "PPTX-C3"
    description: "<p>/<h*> sem background/border/shadow (constraint 3)"
    enforcement: "killer_item"

  - id: "PPTX-C4"
    description: "Zero background-image em DIV; imagens via <img> (constraint 4)"
    enforcement: "killer_item"

  - id: "PPTX-C5"
    description: "Body dimensions = LAYOUT (within 0.1\")"
    enforcement: "killer_item"

  - id: "PPTX-C6"
    description: "Nenhum overflow vertical/horizontal"
    enforcement: "killer_item"
```

---

## Fallback paths (ordenados)

1. **HTML passes 4 constraints → editable PPTX** (esta task, success path)
2. **HTML violates constraints + user needs edit → reescrever HTML para complair** (~2-3h, mas durable)
3. **HTML violates + user accepts image-based → Image PPTX mode** (ver `data/editable-vs-image-pptx-decision.md`)
4. **Manual pptxgenjs hardcoded (addText/addShape)** — **NÃO recomendado**, manutenção perpetual, só como último recurso

---

## Anti-patterns

- ❌ Escrever HTML livre e depois rodar este export "pra ver se dá" — pass rate <30% em HTML não-disciplinado
- ❌ Usar `<span>` como container de texto principal
- ❌ Tentar `background: url()` achando que parser vai entender — não entende
- ❌ Body em `1920×1080` px achando que vai virar slide HD — não, font fica minúscula
- ❌ Esconder constraint violations com `@media print` — export lê HTML fora de print context

---

## Related

- `tasks/confirm-delivery-format.md` — precondição (C no delivery_format)
- `tasks/decide-slide-architecture.md` — precondição (arquitetura define file layout)
- `data/editable-vs-image-pptx-decision.md` — quando PPTX image mode é aceitável
- `agents/qa-inspector.md` — enforcement dos 4 constraints
