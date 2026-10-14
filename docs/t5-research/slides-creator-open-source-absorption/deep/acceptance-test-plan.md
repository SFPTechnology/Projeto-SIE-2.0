# Deep Dive — Acceptance Test Plan

## Objetivo

Definir testes objetivos para provar que a absorção criou uma solução à altura do Gamma no que importa para SINKRA.

## Fixtures

| Fixture | Entrada | Deck esperado |
|---|---|---|
| `executive-briefing.md` | briefing textual | 10 slides executivos |
| `source-report.pdf` | documento longo | 12 slides com fontes |
| `brand-template.pptx` | template corporativo | 8 slides no template |
| `technical-math.md` | conteúdo técnico | 6 slides com fórmula/diagrama |
| `youtube-transcript.md` | transcrição | 10 slides educacionais |

## Testes P0

| Teste | Critério |
|---|---|
| CLI generate | comando gera `deck-spec.yaml`, `pptx`, `pdf`, `qa-report.json`. |
| PPTX opens | PowerPoint abre sem repair. |
| Editability | >= 80% dos elementos principais editáveis. |
| QA narrative | action titles, Pyramid e SCQA passam. |
| QA visual | sem overflow, contraste crítico ou texto ilegível. |
| Source traceability | claims relevantes apontam para fonte. |
| Local provider | smoke test com Ollama/local ou dummy provider. |

## Testes P1

| Teste | Critério |
|---|---|
| Prompt-to-edit | alteração gera diff e exige aprovação. |
| Theme switch | troca tema sem destruir conteúdo. |
| Math/diagram | fórmula e diagrama aparecem corretamente. |
| Template import | template PPTX gera tokens/masters utilizáveis. |

## Testes P2

| Teste | Critério |
|---|---|
| Share link | deck abre em modo web. |
| Analytics | view por deck/slide registrada. |
| Video export | MP4 gera com narração. |
| Q&A | pergunta usa fontes do deck. |

## Métricas Mínimas

| Métrica | Valor |
|---|---:|
| Tempo para 10 slides | <= 5 min MVP |
| Editabilidade | >= 80% MVP |
| QA killer items | 0 |
| Export success | 100% fixtures P0 |
| Fonte ausente em claim crítico | 0 |

## Evidências de Saída

Cada teste deve salvar:

```text
outputs/bench/slides-os-acceptance/{fixture}/
  command.txt
  deck-spec.yaml
  deck.pptx
  deck.pdf
  qa-report.json
  editability-report.json
  screenshots/
  notes.md
```
