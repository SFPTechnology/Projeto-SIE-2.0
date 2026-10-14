# Pesquisa Consolidada no Bench

Data: 2026-05-17

## Status

A pesquisa antiga `docs/research/2026-05-17-bench-analise-solucoes-slides-ia` foi consolidada neste bench e deve ser considerada substituída.

Motivo:

- usava uma matriz rasa de 1 a 5;
- misturava apps, engines, skills e agentes em uma única comparação;
- dependia mais de claims de README do que de clones locais;
- não tinha contrato de dashboard, inventários individuais, segmentação, evidence ledger ou plano de absorção implementável.

## O Que Foi Aproveitado

| Tema | Como entrou no bench |
|---|---|
| Presenton como baseline operacional | Mantido como referência de App/API/MCP/self-hosted em `segmented-comparisons.md`, `api-mcp-runtime.md` e inventário próprio. |
| banana-slides como benchmark de UX prompt-to-edit | Mantido como referência de UX, com risco AGPL explícito em `license-risk-assessment.md`. |
| PPTAgent/DeepPresenter como referência agentic | Consolidado em `agentic-planning-reflection.md` e no segmento Skills/Agentes. |
| presentation-ai para editor web, outline e temas | Consolidado no segmento Apps e em `editor-ux-prompt-to-edit.md`. |
| Slide-Deck-AI/python-pptx como fluxo controlável | Mantido no segmento Engines/Runtime como referência headless/Python/provider abstraction. |
| Slidev/Marp como fallback versionável | Rebaixado para fallback técnico de publicação/markdown, não como solução principal de PPTX editável. |
| BlockNote/Tiptap/ProseMirror | Consolidado como opção para editor block/card-based no roadmap, não como player principal do bench porque não é solução de slides com IA. |
| Yjs/Hocuspocus | Consolidado como camada futura de colaboração realtime, não prioridade antes de geração/export/editor básico. |
| PostHog/Umami/Plausible | Consolidado como camada futura de analytics de deck/share links. |

## O Que Foi Corrigido

| Problema da pesquisa antiga | Correção no bench |
|---|---|
| Presenton tratado como recomendação quase absoluta | Agora vence apenas o segmento Apps; o sistema alvo é composto. |
| Apps e engines comparados diretamente | Agora há 3 comparações: Apps, Skills/Agentes e Engines/Runtime. |
| Slidev/Marp inflavam score por controle técnico | Agora são fallback de publicação/versionamento, não substitutos de PPTX editável. |
| Gamma medido por feature list genérica | Agora o critério é absorção para slide creator skill stack: governança, PPTX editável, API/MCP, self-hosting, UX, QA e risco de licença. |
| Pouca profundidade de matriz | O bench tem matriz consolidada 108D/972 células, matriz macro arquivada 36D/324 células e matrizes segmentadas 72D/264 células. |

## Tese Final Incorporada

Para competir com Gamma, não basta “gerar PPT”. A stack precisa cobrir:

1. geração por prompt/documento;
2. editor card/block-based;
3. prompt-to-edit por slide/região;
4. PPTX nativo editável;
5. publicação por link;
6. analytics;
7. API/MCP;
8. BYOK/local/Ollama;
9. QA narrativo, visual e técnico;
10. governança de fontes e rastreabilidade.

O bench atual transforma essa tese em uma composição:

- **App layer:** Presenton + padrões de UX de banana-slides/presentation-ai;
- **Skill/agentic layer:** slide creator skill + PPTAgent + PresentAgent-2 + powerpoint-skill;
- **Engine/runtime layer:** ppt-master + Presenton + slide-deck-ai + powerpoint-skill;
- **Editor/collab layer futura:** BlockNote/Tiptap + Yjs/Hocuspocus;
- **Distribuição futura:** web runtime + PostHog/Umami/Plausible.

## Nota Sobre Pesquisa Anterior de huashu-design

O relatório `docs/research/2026-04-20-claude-design-oss-alternatives/08-slides-creator-absorption.md` não foi apagado nesta consolidação porque pertence a outro estudo maior. Os aprendizados relevantes para slides foram incorporados ao bench como requisitos:

- checkpoint `format-first`;
- target `standalone HTML`;
- decisão `editable PPTX` vs `image PPTX`;
- QA multi-viewport com Playwright;
- pipeline multi-formato HTML/PDF/PPTX/MP4;
- restrição de não copiar código de licença incompatível.
