# confirm-delivery-format

> **Task type:** Phase 0 checkpoint — executado ANTES de `normalize-briefing`
> **Owner:** `slide-chief`

## Purpose

Confirmar o formato final de entrega **antes de qualquer artefato ser gerado**. Descoberta crítica do espaço: não confirmar formato upfront = 2-3h de rework documentado quando o HTML é reescrito para caber em constraints de PPTX editável.

## Trigger

Primeira ação do slide-chief ao receber qualquer briefing novo. Anterior a `normalize-briefing`. Se pular, toda decisão downstream (content-architect, template-curator, design-renderer) pode precisar ser desfeita.

## Decision Tree

Perguntar ao user (1 pergunta, 4 opções):

```
Qual é a entrega final do deck?

A) Browser / HTML navegável (apresentação ao vivo, compartilhamento local)
   → Visual liberdade total. Qualquer motion/gradient/web-component permitido.

B) PDF vetorial (print, distribuição, archive)
   → Visual liberdade total. Exportável de qualquer arquitetura HTML.

C) PPTX editável (colegas/cliente vão editar texto após entrega)
   → 🛑 HTML precisa seguir 4 hard constraints DESDE A PRIMEIRA LINHA
   → Ver `tasks/export-editable-pptx.md` antes de qualquer coisa
   → Font fallback possível em destino (~70% visual fidelity)

D) MP4 / GIF (social media, marketing, launch video)
   → Motion engine obrigatório
   → Ver `data/narrative-pacing.md` (Slow-Fast-Boom-Stop)
   → Ver `data/motion-export-discipline.md` (recording sync)
```

## Combined formats

User pode pedir A+B, A+C, ou A+B+C — cada combinação tem regra:

| Combinação | Regra |
|---|---|
| A + B | Sem custo extra — PDF exportável de qualquer HTML |
| A + C | PPTX é constraint-mais-restritiva — **toda HTML segue 4 constraints** |
| A + B + C | Idem A + C — PDF e browser são subconjuntos do output PPTX-compliant |
| C + motion | **Contradição** — avisar user: PPTX editable não suporta web component / complex SVG / CSS gradient / animation. Pedir trade-off explícito |
| B + motion | PDF é estático — motion só faz sentido se user quer PDF mais MP4 separado |

## Output

Atualizar `briefing.normalized.json` (stub, antes de `normalize-briefing` formal) com:

```yaml
delivery_format:
  primary: "A|B|C|D"
  secondary: []       # array of additional formats if combo
  constraints_applied: []   # ex: ["editable-pptx-4-constraints"] quando C
  decided_at: "ISO-8601"
  decided_by: "user"  # ou "auto" se user não responde (bloqueio)
```

Esse campo é **lido por design-renderer** para escolher render mode (ver `data/render-modes.yaml` quando disponível).

## Enforcement

Se slide-chief tentar rotear para content-architect sem este campo preenchido em `briefing.normalized.json`, content-architect **deve bloquear e escalar de volta** para slide-chief com:

```
ERROR: delivery_format missing. Return to slide-chief and complete confirm-delivery-format.md.
```

## Failure mode (documented)

Pattern observado no espaço de design-assistance:
- HTML foi escrito livre (~17 páginas)
- No final: user revelou que precisava PPTX editável
- Rework: 2-3h (reescrever cada página para 4 constraints ou manual pptxgenjs hardcoded)
- **Custo do checkpoint:** 2-3min (uma pergunta a mais no intake)
- **ROI:** ~100x

## Anti-patterns

- ❌ Assumir "padrão é HTML com ds presenter" sem perguntar
- ❌ Pular porque "user disse deck e isso é óbvio"
- ❌ Perguntar só depois do normalize-briefing completo
- ❌ Perguntar sem as 4 opções concretas (vago → response vago)
- ❌ Aceitar resposta "ah qualquer um" sem travar no default mais restritivo ou seguro

## Anti-anti-pattern

User genuinamente não sabe formato final → default para **A (Browser / PDF)** com commitment de "se depois decidir PPTX editável, sprint dedicado para refactor" escrito em `caveats`. NÃO assumir C silenciosamente.

## References

- `tasks/export-editable-pptx.md` (quando delivery_format inclui C)
- `data/editable-vs-image-pptx-decision.md`
