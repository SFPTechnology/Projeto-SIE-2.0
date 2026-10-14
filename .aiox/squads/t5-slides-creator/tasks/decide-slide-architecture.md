# decide-slide-architecture

> **Task type:** Architecture decision (pre-rendering)
> **Owner:** `design-renderer` (when rendering standalone HTML) / `slide-chief` (when TSX via ds)
> **Triggers:** executar depois de `confirm-delivery-format` e antes de qualquer emit de HTML/TSX

## Purpose

Escolher entre duas arquiteturas de rendering quando o deliverable inclui HTML (browser/PDF/PPTX):

1. **Multi-file** (DEFAULT) — cada slide é um HTML independente, `deck_index.html` iframe-composer orquestra navegação
2. **Single-file** — todos os slides em um HTML, web component (`<deck-stage>`) encapsula sections

A decisão impacta CSS scope, validation cost, parallelization, debugging, e (crucial) PDF export complexity.

## Decision tree

```
┌─ Pergunta 1: Quantas páginas o deck tem? ─┐
│                                            │
├── ≤ 10 páginas                            │
│   ├── Pitch deck / investor deck?          │
│   │   └── Precisa cross-page state         │
│   │       (Tweaks compartilhado,           │
│   │        feature flag que altera todas)? │
│   │       ├── SIM → single-file            │
│   │       └── NÃO → multi-file (preferir)  │
│   └── Longer-form / academic?              │
│       └── multi-file (mesmo com 10)        │
│                                            │
└── > 10 páginas                            │
    └── SEMPRE multi-file                    │
```

## Additional decision triggers

| Trigger | Decision |
|---|---|
| Multi-agent parallel development (N stories em paralelo) | multi-file **obrigatório** |
| Cross-page shared state (tweaks, feature flag, player progress) | single-file |
| PDF export é essencial | multi-file (evita Shadow DOM PDF bugs — ver `data/shadow-dom-pdf-troubleshooting.md`) |
| Animated transitions slide-to-slide | single-file (mais fácil coordenar timeline) |
| Deck é > 20 páginas | multi-file, sem exceção |
| Debugging fácil (abrir UM slide sem load do deck inteiro) | multi-file |
| Unit test por slide | multi-file |
| `@devops` precisa fazer deploy atomic de um slide só | multi-file |

## Architecture summary

### Multi-file

```
meu-deck/
├── index.html                # composer (iframe-based navigation)
├── shared/
│   ├── tokens.css            # design tokens (colors, fonts, spacing)
│   └── fonts.html            # @font-face imports (included per slide)
└── slides/
    ├── 01-cover.html         # 100% independent HTML, 1920×1080
    ├── 02-agenda.html
    ├── 03-problem.html
    └── ...
```

**Vantagens:**
- CSS scope isolation nativa (iframe)
- `open slides/05-personas.html` = validation direta no browser
- N agents trabalham em paralelo zero merge conflict
- 1 CSS bug afunda 1 slide, não todos
- PDF export = Playwright + loop sobre HTML files (simples)

**Trade-offs:**
- Cross-page state exige postMessage entre iframes
- Shared design tokens vão em `shared/tokens.css` (loaded per slide)
- Loading 40 iframes em composer pode ter cost (mitigar com lazy load)

### Single-file

```html
<!DOCTYPE html>
<html>
<head>
  <style>/* todas as styles de todos os slides */</style>
</head>
<body>
  <deck-stage>
    <section class="active">Slide 1</section>
    <section>Slide 2</section>
    <section>Slide 3</section>
  </deck-stage>
  <script>/* web component definition */</script>
</body>
</html>
```

**Vantagens:**
- Arquivo único = fácil distribuição (attach em email, upload em drive)
- Cross-slide state trivial (mesmo scope JS)
- Um único deploy

**Trade-offs (documented failure modes):**
- CSS specificity bugs — `.emotion-slide { display: grid }` (10) vence `::slotted(section){display:none}` (2) → todas sections renderizam sobrepostas
- Shadow DOM slot rules podem ser suprimidas por outer CSS
- localStorage + hash navigation race condition (reload stuck em old state)
- Validation cost — precisa `page.evaluate(d => d.goTo(5))` para validar slide 5, vs direct URL em multi-file
- **PDF export é complexo** — Shadow DOM saga documented em `data/shadow-dom-pdf-troubleshooting.md`

## Default assumption

**Se dúvida, multi-file.** É o path que tem mais vantagens arquiteturais e menos modos de falha documentados.

Single-file só se:
- Deck pequeno (≤10 páginas)
- Precisa mesmo de cross-page state
- Ou é pitch deck muito coeso (onde tudo é "uma narrativa")

## Output artifact

Updating `briefing.normalized.json`:

```yaml
slide_architecture:
  mode: "multi-file|single-file"
  decided_at: "ISO-8601"
  rationale: |
    Reason for choice (page count, parallelism needs, PDF requirement, etc).
  file_structure:
    type: "multi-file"  # or "single-file"
    expected_count: 17
    layout:
      index: "index.html"
      shared_assets: "shared/"
      slides_dir: "slides/"
```

Este campo é lido por `design-renderer` para escolher template + composer.

## Enforcement

design-renderer **deve bloquear** execução se tentar render sem `slide_architecture.mode` definido em briefing.normalized.json. Escalar de volta para slide-chief completar este task.

## Anti-patterns

- ❌ Começar single-file porque "é menos arquivos" (CSS scope vai morder depois)
- ❌ Começar multi-file porque "é mais robusto" em deck de 5 páginas com cross-state (overkill)
- ❌ Decidir no meio do rendering (mid-flight arch change = rework pesado)
- ❌ Escolher por preferência pessoal sem validar decision tree

## Related

- `tasks/confirm-delivery-format.md` — precisa executar ANTES deste
- `data/shadow-dom-pdf-troubleshooting.md` — leitura obrigatória se escolher single-file + delivery inclui PDF
- `tasks/render-html-standalone.md` (quando implementado) — consumidor desta decisão
