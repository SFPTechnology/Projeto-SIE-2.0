# Native Slide IR Contract

## Objetivo

Definir a camada intermediária entre `DeckSpec` e renderer PPTX nativo editável.

## Princípios

- LLM gera especificação validável, não PPTX direto.
- Renderer converte IR para objetos PowerPoint.
- Todo fallback raster deve ser explícito.
- Cada elemento tem `id` estável para prompt-to-edit.

## Estrutura

```json
{
  "schema": "native-slide-ir.v1",
  "deck_id": "deck_20260517_001",
  "canvas": {
    "width_pt": 960,
    "height_pt": 540,
    "ratio": "16:9"
  },
  "slides": [
    {
      "id": "s01",
      "background": {"type": "solid", "color": "#FFFFFF"},
      "elements": [
        {
          "id": "headline",
          "type": "text_box",
          "role": "action_title",
          "content": "IA para slides só vira produto quando gera PPTX editável",
          "x": 48,
          "y": 40,
          "w": 720,
          "h": 64,
          "font": {"family": "Inter", "size": 30, "weight": 700},
          "fit": "shrink_to_bounds"
        }
      ]
    }
  ]
}
```

## Element Types P0

| Tipo | Render nativo | Fallback |
|---|---:|---|
| `text_box` | Sim | raster proibido para action titles |
| `shape` | Sim | raster permitido se efeito não suportado |
| `image` | Sim | raster nativo como imagem |
| `table` | Sim | raster permitido no MVP se tabela complexa |
| `chart` | Parcial | imagem + dados anexos |
| `diagram` | Parcial | SVG/PNG + source `.mmd`/`.dot` |

## Validação

O IR é inválido se:

- faltar `id` em slide ou elemento;
- texto exceder bounds sem `fit`;
- action title estiver rasterizado;
- path de imagem sair do workspace;
- cor não for hex/token resolvido;
- elemento tiver coordenadas fora do canvas sem intenção explícita.

## Métricas

O renderer deve emitir:

- `native_object_count`;
- `raster_object_count`;
- `editable_text_count`;
- `unsupported_feature_count`;
- `editability_score`.
