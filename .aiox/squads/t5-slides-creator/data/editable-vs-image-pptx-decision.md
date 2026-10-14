# Editable vs Image PPTX — Decision Matrix

> **Purpose:** decidir qual modo de export PPTX usar quando `delivery_format` inclui C
> **Consumers:** `design-renderer`, `qa-inspector`, `slide-chief` (release gate)

---

## The two modes

### Editable mode

- **Como:** DOM lido elemento por elemento → objetos PowerPoint nativos (text frame / shape / picture)
- **Resultado:** cliente abre PPTX, duplo-clique em um texto, edita palavras
- **Restrição:** HTML precisa seguir 4 hard constraints desde a primeira linha (ver `tasks/export-editable-pptx.md`)
- **Visual fidelity:** ~70% (font fallback possível no destino; alguns features CSS não mapeiam)

### Image mode

- **Como:** cada slide HTML é screenshot via Playwright em PNG 1920×1080 → PNG inserido como full-slide image em pptxgenjs
- **Resultado:** visual 100% idêntico ao browser. Mas cliente não consegue editar texto.
- **Restrição:** nenhuma (HTML pode ter qualquer CSS)
- **Visual fidelity:** 100%

---

## Decision matrix

| Critério | Editable | Image |
|---|---|---|
| Cliente vai editar texto após entrega | ✅ | ❌ |
| Apresentação única, arquivado depois | ❌ | ✅ |
| Visual tem gradients complexos / web component / SVG avançado | ❌ (não suporta) | ✅ |
| Visual tem CSS simples (solid colors, basic layout) | ✅ | ✅ |
| Font stack não está no Office do destino | ⚠️ fallback | ✅ (raster preserva) |
| Precisa visual 100% pixel-perfect | ⚠️ ~70% | ✅ 100% |
| Precisa de texto pesquisável no PowerPoint | ✅ | ❌ (texto é pixel) |
| Precisa de text-to-speech / accessibility reader no PPTX | ✅ | ❌ |
| Tamanho de arquivo | 📄 Menor (XML + assets) | 📦 Maior (17 PNGs embutidos) |
| Manter deck ao longo do tempo (revisões) | ✅ (editar direto) | ❌ (reeditar HTML, reexport) |

---

## Decision flow

```
Cliente precisa editar texto após entrega? ─────┐
│                                                │
├── SIM                                          │
│   └── HTML já segue 4 constraints?             │
│       ├── SIM → **Editable mode**              │
│       └── NÃO → Retornar erro, reescrever HTML │
│                  OU aceitar image mode com     │
│                  caveat explícito              │
│                                                │
└── NÃO / NÃO SEI                                │
    └── Visual pede CSS complexo (gradient,      │
        web component, complex SVG)?             │
        ├── SIM → **Image mode**                 │
        └── NÃO → **Editable mode** (mais        │
                   robusto long-term)            │
```

---

## When Editable is worth the constraint discipline

Adotar editable mode + seguir as 4 constraints vale a pena quando:

1. **Deck é long-lived** — vai ser editado/revisado ao longo de meses
2. **Multiple authors** — colegas não-técnicos vão ajustar copy
3. **Content-focused, visual-simple** — cards, números, texto, charts vetoriais
4. **Template brand-governed** — CSS é limitado, constraints não doem
5. **Accessibility matters** — screen readers precisam de texto real
6. **Localization** — traduções exigem edit direto no PPTX

---

## When Image mode is the pragmatic choice

Adotar image mode quando:

1. **Deck é one-shot** — apresenta uma vez, arquiva
2. **Single author** — quem fez quem reedita (HTML-first workflow)
3. **Visual-heavy** — gradientes, glassmorphism, web components críticos
4. **Visual fidelity é dealbreaker** — 70% de fidelity não é aceitável pro cliente
5. **HTML já existe livre** — não tem budget pra reescrever seguindo 4 constraints
6. **Design-system custom** — visuals que editable não consegue traduzir

---

## Hybrid strategy (per-slide mode)

Caso real: deck de 20 páginas, sendo 5 "heavy visual" (capa, section dividers, infographic) e 15 "content-focused" (data, bullets, frameworks).

Pode-se exportar **híbrido**:
- Slides 1, 5, 10, 15, 20 (heavy) → image mode
- Slides 2-4, 6-9, 11-14, 16-19 (content) → editable mode
- Merge em pptxgenjs single deck

Trade-off: PPTX final tem ~75% dos slides editáveis + os 5 heavies em imagem. Compromise aceitável se cliente precisa editar conteúdo mas não disputa o visual dos dividers.

---

## Handoff note pro cliente

Quando entregar deck em **image mode**, incluir em delivery note:

```
⚠️ Este deck está em modo image — textos são renderizados como imagem
para preservar fidelidade visual. Para edições de conteúdo:

1. Edições pequenas (palavra, correção typo): nos retorne o ticket, refazemos
2. Edições grandes (reescrita section): forneça o novo texto, atualizamos HTML+PPTX
3. Se você precisa editar diretamente no PowerPoint no futuro, podemos migrar
   para modo editable em um sprint dedicado (ver constraints em export-editable-pptx).
```

Quando entregar **editable mode**, nenhuma nota extra — cliente edita como qualquer PPTX.

---

## Related

- `tasks/confirm-delivery-format.md` — onde decisão começa
- `tasks/export-editable-pptx.md` — implementação editable
- `data/render-modes.yaml` — config técnica dos modos
