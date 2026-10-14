# Deep Dive — Renderer Nativo Editável

## Tese

O renderer é o gap mais importante. Sem PPTX realmente editável, a solução pode ser útil para preview, mas não compete em B2B. O padrão de qualidade precisa ser mais próximo de `ppt-master` do que de pipelines image-based.

## Estado Atual SINKRA

Evidências:

- `squads/slides-creator/data/editable-vs-image-pptx-decision.md`
- `squads/slides-creator/tasks/export-editable-pptx.md`
- `squads/slides-creator/data/slide-spec-schema.yaml`
- `squads/slides-creator/templates/deck-manifest.json`

O squad já tem a decisão conceitual:

- **editable mode:** DOM/estrutura para objetos nativos, menor fidelidade visual, maior valor B2B;
- **image mode:** screenshots com alta fidelidade, baixa editabilidade;
- **hybrid mode:** decide por slide/elemento.

O que falta é runtime real, validador de editabilidade e um IR estável.

## Referência Externa

`ppt-master` é a referência P0 porque declara e estrutura o objetivo certo: PowerPoint real, com shapes/textos/charts editáveis, template replication e export OOXML.

Evidências:

- `../bench/ppt-master/README.md`
- `../bench/ppt-master/docs/templates-guide.md`
- `../bench/ppt-master/skills/ppt-master/workflows/live-preview.md`

## Arquitetura Recomendada

```text
DeckSpec
  -> SlideSpec[]
  -> Visual IR
      - text_box
      - shape
      - image
      - chart
      - table
      - diagram
      - group
  -> Renderer
      - native DrawingML path
      - raster fallback path
      - notes/narration path
  -> PPTX
  -> Editability QA
```

## Regra de Ouro

Não deixar o LLM gerar PPTX diretamente. O LLM deve gerar uma especificação validável. O renderer converte para PPTX.

## Estratégia de Implementação

### P0.1 — IR mínimo

Criar `native-slide-ir.schema.json` com:

- canvas `16:9`;
- unidades fixas;
- textos com `id`, `role`, `content`, `font`, `fit_policy`;
- shapes com `fill`, `stroke`, `corner_radius`;
- images com `source`, `crop`, `alt`;
- charts/tables com dados estruturados;
- fallback `raster_allowed: true/false`.

### P0.2 — Exportador inicial

Começar com:

- title slide;
- text blocks;
- rectangles/cards;
- images;
- simple charts;
- speaker notes.

Evitar no início:

- animação;
- vídeo;
- edição regional;
- SVG arbitrário;
- efeitos CSS complexos.

### P0.3 — Editability QA

Relatório obrigatório:

```json
{
  "deck_id": "deck-123",
  "slides": [
    {
      "slide_id": "s01",
      "native_objects": 14,
      "raster_objects": 1,
      "editable_text_boxes": 4,
      "editability_score": 0.91
    }
  ],
  "overall_editability_score": 0.86
}
```

### P0.4 — Hybrid fallback

Critérios para rasterizar:

- composição visual altamente decorativa;
- imagem de fundo;
- gráfico não suportado;
- efeito impossível em DrawingML;
- erro de fitting de texto.

Mesmo quando rasterizar, manter camada de texto opcional se possível.

## Métricas

| Métrica | MVP | P1 |
|---|---:|---:|
| Elementos principais editáveis | >= 80% | >= 90% |
| Slides sem overflow | >= 95% | >= 98% |
| Round-trip PowerPoint abre sem reparo | 100% | 100% |
| PDF visual diff aceitável | >= 90% | >= 95% |
| Tempo export 20 slides | <= 60s | <= 30s |

## Riscos

| Risco | Mitigação |
|---|---|
| SVG livre vira impossível de converter | Schema restrito e lint antes do renderer. |
| PPTX abre, mas não é editável | Editability QA obrigatório. |
| Layout quebra por fonte | Font registry e fallback determinístico. |
| Template corporativo complexo | Começar com subset e reportar unsupported features. |

## Critério de Done

Um deck de 10 slides gerado pelo `slides-creator` deve:

- exportar `.pptx` e `.pdf`;
- abrir no PowerPoint sem repair;
- ter títulos e textos editáveis;
- preservar fontes/cores do template;
- gerar `editability-report.json`;
- passar `qa-report.json` sem killer items.
