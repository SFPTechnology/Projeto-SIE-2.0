# Deep Dive — Editor UX e Prompt-to-Edit

## Tese

O editor não deve ser o primeiro componente, mas precisa ser desenhado desde já. Gamma é forte porque edição e geração estão no mesmo loop. Nossa UX deve chegar lá usando DeckSpec versionável e IDs estáveis, não edição visual solta.

## Referências

- banana-slides: prompt-to-edit, edição regional, vídeo e style references.
- presentation-ai: outline-first, editor web, temas, sharing e modelos locais.
- Presenton: templates, API e app self-hosted.
- ppt-master: live preview com annotations.

## Estado Atual SINKRA

O `slides-creator` tem contratos e templates, mas não tem editor. A experiência principal ainda é skill/workflow/handoff.

## Princípio de Produto

Toda edição visual deve virar diff em `deck-spec.yaml`.

Exemplo:

```yaml
operation:
  type: update_slide_element
  slide_id: s04
  element_id: headline
  field: content
  before: "Mercado cresce"
  after: "Mercado cresce, mas margem migra para players integrados"
  qa_required: true
```

## UX Mínima P1

| Tela | Função |
|---|---|
| Outline | Revisar storyline antes de gerar slides. |
| Slide list | Navegar por slides e status QA. |
| Canvas preview | Ver slide renderizado. |
| Prompt panel | Pedir mudança em slide/elemento. |
| Diff panel | Aprovar/rejeitar alteração. |
| Export panel | PPTX/PDF/web e relatórios. |

## Prompt-to-Edit Commands

| Tipo | Exemplo | Regra |
|---|---|---|
| Conteúdo | "deixe o título mais executivo" | Roda QA narrativa. |
| Layout | "dê mais espaço ao gráfico" | Roda QA visual. |
| Estilo | "use tom mais premium" | Altera theme tokens. |
| Fonte | "adicione fonte para esta afirmação" | Exige evidência. |
| Export | "gere versão PPTX editável" | Roda editability QA. |

## Não Fazer

- Não editar DOM diretamente como fonte de verdade.
- Não permitir prompt que muda fatos sem fonte.
- Não substituir DeckSpec por screenshots.
- Não copiar código AGPL de banana-slides sem aprovação.

## Critérios de Aceite

- Edição de slide gera diff audível/visível.
- Usuário aprova antes de aplicar.
- Histórico permite rollback por operação.
- Export final usa o mesmo renderer headless.
- QA aponta exatamente qual alteração criou falha.
