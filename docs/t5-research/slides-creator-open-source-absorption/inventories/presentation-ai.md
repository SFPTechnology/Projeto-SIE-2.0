# Inventory — presentation-ai

## Identidade

- **Repo:** `allweonedev/presentation-ai`
- **Clone local:** `../bench/presentation-ai`
- **Licença:** MIT
- **Prioridade:** P1
- **Papel na stack:** editor web, outline-first workflow, temas, sharing e export.

## Evidência Lida

- `../bench/presentation-ai/README.md`
- `../bench/presentation-ai/apps/web/app`
- `../bench/presentation-ai/apps/web/lib`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| Outline-first | Gera outline, permite revisar e só depois vira slides. |
| Editor web | Next.js/React com experiência de app. |
| Temas | Temas built-in e import/inspiração via PPTX. |
| Local models | Ollama e LM Studio para geração local. |
| Sharing/present mode | Experiência de apresentação dentro do app. |

## Limitações

- Menos forte em governança narrativa.
- Export/editabilidade precisa validação contra padrão `ppt-master`.
- UI sem renderer robusto não resolve o gap B2B.

## O Que Absorver

1. Outline editor antes da geração.
2. Theme picker e theme model.
3. Present mode e sharing como referência P2.
4. Integração de modelos locais no seletor.

## Integração SINKRA Recomendada

O editor deve manipular `deck-spec.yaml`, não HTML solto. Toda alteração de outline vira diff no DeckSpec e passa por QA quando altera narrativa.

## Critério de Aceite

- Usuário consegue revisar outline antes de render.
- Alteração de tema não destrói conteúdo.
- Export usa o mesmo renderer headless da CLI/API.
