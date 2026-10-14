# Shadow DOM PDF Export — Troubleshooting Playbook

> **Purpose:** knowledge rara documentada para quando exportar deck em single-file web-component architecture para PDF. 3 bugs reais + fix.
> **Trigger:** usar quando `render-html-standalone` em modo single-file + delivery format é PDF

---

## Quando ler este doc

Se você está em UM dos cenários abaixo, leia completo. Senão, skip.

- Arquitetura single-file deck com web component `<deck-stage>` ou similar
- Exportar para PDF multi-página via Playwright `page.pdf()`
- Primeiro export deu PDF com **apenas 1 página** (vs N esperadas)
- Ou PDF com número de páginas errado (N+1 páginas com última página vazia)

---

## Background: por que Shadow DOM PDF é hard

Single-file decks usam web component `<deck-stage>` que encapsula sections via Shadow DOM:

```html
<deck-stage>
  <section class="active">Slide 1</section>
  <section>Slide 2</section>
  <section>Slide 3</section>
</deck-stage>
```

Shadow DOM CSS interno típico:
```css
::slotted(section) { display: none; }
::slotted(section.active) { display: block; }
```

Isso funciona **perfeitamente para navegação interativa**. Quebra para PDF export por 3 razões distintas.

---

## Bug 1 — Shadow DOM vs `!important`

### Sintoma

Você roda:

```javascript
await page.pdf({ format: 'letter', printBackground: true });
```

Resultado: PDF com **1 página** (apenas a `<section class="active">` renderizada).

### Causa

Adicionou print media query em light DOM:

```css
@media print {
  deck-stage > section { display: block !important; }
}
```

Mas shadow DOM tem:
```css
::slotted(section) { display: none; }
```

Contraintuitivo: **shadow DOM internal rules têm prioridade sobre light DOM `!important`** porque são estilos de **shadow tree**, não de document root. `!important` no light DOM não alcança.

### Fix ❌ (não funciona)

Tentar `@media print` em vários scopes, pseudo-elements, higher specificity — todos falham mesmo que you think "specificity is higher".

### Fix ✅

Extrair sections de shadow DOM para light DOM antes de `page.pdf()`:

```javascript
await page.evaluate(() => {
  const stage = document.querySelector('deck-stage');
  const sections = Array.from(stage.querySelectorAll(':scope > section'));
  
  // Hide the original deck-stage
  const hideStyle = document.createElement('style');
  hideStyle.textContent = `
    @page { size: 1920px 1080px; margin: 0; }
    html, body { margin: 0 !important; padding: 0 !important; }
    deck-stage { display: none !important; }
  `;
  document.head.appendChild(hideStyle);
  
  // Move sections to a regular div
  const container = document.createElement('div');
  sections.forEach(s => {
    s.style.cssText = [
      'width: 1920px !important',
      'height: 1080px !important',
      'display: block !important',
      'position: relative !important',    // critical — see Bug 3
      'overflow: hidden !important',
      'page-break-after: always !important',
      'break-after: page !important',
      'background: #FFFFFF',
      'margin: 0 !important',
      'padding: 0 !important',
    ].join('; ');
    container.appendChild(s);
  });
  
  // Last section: disable page-break to avoid blank trailing page
  const last = sections[sections.length - 1];
  last.style.pageBreakAfter = 'auto';
  last.style.breakAfter = 'auto';
  
  document.body.appendChild(container);
});

await page.pdf({ 
  width: '1920px', 
  height: '1080px', 
  printBackground: true,
  preferCSSPageSize: true,
});
```

---

## Bug 2 — Loop `page.pdf({pageRanges:'1'})` falhar

### Sintoma

Intuitivamente você pensou: "OK, navego para `#slide-0`, `page.pdf({pageRanges: '1'})`, salvo. Repeat para cada slide. Merge PDFs."

Código:
```javascript
for (let i = 0; i < slideCount; i++) {
  await page.goto(`file://deck.html#slide-${i}`);
  await page.waitForLoadState('networkidle');
  await page.pdf({ path: `page-${i}.pdf`, pageRanges: '1' });
}
```

Resultado: **N PDFs, todos com a mesma página (a cover)**. Como se navegação por hash não funcionasse.

### Causa

Quando a print media query ativa em shadow DOM tem rule `deck-stage > section { display: block }` (override do `none`), o Chromium em print mode renderiza **todas as sections empilhadas**. `pageRanges: '1'` pega a primeira do stack — que é sempre a mesma section por ordem DOM (normalmente a cover), **não a active via hash**.

Hash navigation muda state JS interno do web component mas não muda ordem DOM. Print media ignora JS state, reorder pela ordem visual.

### Fix

Use **Bug 1 fix** (extract sections) — uma vez extraídas, ordem DOM = ordem visual desejada. Fazer um único `page.pdf()` sem loop.

---

## Bug 3 — Absolute children overflow para next page

### Sintoma

Você aplicou Bug 1 fix e agora vê N páginas. Mas o PDF tem `N+1 páginas`, com a última **contendo apenas o footer** (arrancado do último slide).

### Causa

Section no HTML original tinha `position: static`. Dentro dela, `cover-footer` ou `slide-footer` era `position: absolute`. Com `position: static`, absolute children positionam relativo ao **initial containing block** (viewport), não ao section parent.

Quando print força section height = 1080px mas containing block continua viewport-based, absolute footer posiciona onde o viewport terminaria — que para slides depois do primeiro está **fora da section**, na próxima página.

### Fix

Incluído no Bug 1 fix: inline style `position: relative !important` em cada section extraída. Isso cria novo containing block, absolute children se alinham dentro da section.

```javascript
s.style.cssText = '...; position: relative !important; ...';
```

Plus: `last-child: page-break-after: auto` evita página vazia final (a `page-break-after: always` em todas faria o renderer adicionar pagebreak após a última section, resultando em blank page).

---

## Validação final

### Contagem de páginas correta

```bash
# pdftoppm (poppler) é source of truth
pdfinfo deck.pdf | grep Pages

# OU
pdftoppm -f 1 -l 999 deck.pdf page  # gera page-1.png, page-2.png, ...
ls page-*.png | wc -l
```

### NÃO use `mdls` (macOS)

```bash
mdls -name kMDItemNumberOfPages deck.pdf  # Spotlight cache — NÃO confiável
```

Spotlight metadata tem cache. PDF reescrito pode mostrar contagem antiga. Sempre force:
```bash
mdimport deck.pdf
```

Ou simplesmente use `pdfinfo` que não tem cache.

---

## Fallback: multi-file architecture evita Shadow DOM complexity

Se o problema é recorrente + você controla architecture: **multi-file architecture não tem este problema** (cada slide é HTML independente, no shadow DOM).

Ver `tasks/decide-slide-architecture.md` para decisão e `tasks/render-html-standalone.md` (quando implementado) para modo multi-file.

---

## Reference

- [MDN Shadow DOM styling](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM#styling)
- [Playwright page.pdf() docs](https://playwright.dev/docs/api/class-page#page-pdf)
- Related: `data/render-modes.yaml` (when created — describe single-file vs multi-file output modes)
