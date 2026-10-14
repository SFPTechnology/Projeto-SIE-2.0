# Inventory — PresentAgent-2

## Identidade

- **Repo:** `AIGeeksGroup/PresentAgent-2`
- **Clone local:** `../bench/PresentAgent-2`
- **Licença:** não verificada no inventário
- **Prioridade:** P2/Futuro
- **Papel na stack:** query→deep research→slides→vídeo, discussão e Q&A.

## Evidência Lida

- `../bench/PresentAgent-2/README.md`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| Query-driven | Começa de uma pergunta aberta, não só documento pronto. |
| Deep research | Pipeline seleciona e refina fontes. |
| Multimodal | Preserva texto, imagens, GIFs e vídeos. |
| Vídeo narrado | Gera apresentação em formato de vídeo. |
| Q&A interativo | Interface para perguntas com resposta e seek no vídeo. |

## Limitações

- Mais pesado e experimental.
- Licença não deve ser assumida.
- Forte dependência de infraestrutura multimodal.
- Não é caminho de MVP para PPTX editável.

## O Que Absorver

1. Modelo de `query -> research -> source.md -> refined_doc -> deck`.
2. Benchmarks de qualidade por quiz/subjetivo.
3. Q&A como direção futura para apresentações interativas.

## Critério de Aceite Futuro

- Query gera relatório rastreável antes de slides.
- Vídeo é opcional, não substitui PPTX.
- Q&A usa fontes do deck e não inventa respostas.
