# Executive Report — Criar Nossa Skill/Stack de Slides Mais Avançada

## Update 2026-05-18 — Wave 3 Spike Materializado

**Score atualizado: 81.07** (era 77.93 pré-Wave 3 · gap 6.28 para o 2º colocado ppt-master).

O bench saiu de "intelligence-only 100/100, produto pendente" para "produto em spike com 30 microdimensões promovidas por evidência executável". O caminho não mudou (composição modular, não fork), mas as primeiras camadas operacionais já existem:

- **3 packages @sinkra/slides-***: renderer (Native IR + DrawingML + editability), core (briefing/deckspec/IR/reflection/edit, com provider Codex CLI real + Zod schema + fallback), mcp (5 tools stdio).
- **5 surfaces operacionais**: CLI (5 subcomandos), REST (5 endpoints no squad-engine), MCP (5 tools), CLI renderer standalone, 2 validators Python (Design 100 + Parity).
- **5 golden fixtures**: executivo, webinar, finance, technical, brand — todos validam contra schema, editability 100/100.
- **8 specs Jest**: 5 core (briefing/deckspec/native-ir/reflection/pipeline) + 3 renderer (schema/editability/golden).
- **2 npm scripts** + **pre-push hook advisory** acionado por diff de runtime slides.
- **Epic + 18 stories** Draft prontos para `/aiox-po` → `/full-sdc`.

**Resposta atualizada à pergunta original**: dá pra ganhar dos competidores em narrativa+QA+governança hoje (já ganhamos por 6.28pts). Para liderar também em **Renderização** (ppt-master 82.13 ainda lidera segmento engines/runtime) e **Editor visual** (presentation-ai 80.59 lidera persona designer/brand), precisamos completar as 18 stories da Wave 3 + Wave 4 (multimídia, editor web, distribuição). Detalhes em [wave-3-score-delta.md](wave-3-score-delta.md) e [scorecard.md](scorecard.md).

---

## Veredito

Sim, baixamos e analisamos os principais projetos. A resposta estratégica é: **não forkear nenhum deles como base única**. O caminho correto é usar o nosso `squads/slides-creator` como núcleo governado e absorver capacidades específicas dos projetos open-source.

Nosso squad já é mais forte que os concorrentes em:

- narrativa consultiva;
- Pyramid/MECE/SCQA;
- action titles;
- APA e fidelidade a dados;
- QA/release gates;
- orquestração multiagente.

Os concorrentes são mais fortes em:

- runtime/app;
- UX visual;
- PPTX editável real;
- API/MCP self-hosted;
- prompt-to-edit;
- publicação/analytics.

## Ranking de Absorção

| Prioridade | Projeto | Por quê |
|---|---|---|
| P0 | `ppt-master` | Melhor pipeline para PPTX nativo editável, com shapes reais, template replication, live preview, animações e narração. |
| P0 | Presenton | Melhor base app/API/MCP/self-hosted/local-first. |
| P0 | PPTAgent | Melhor arquitetura agentic/reflexiva para planejamento e avaliação. |
| P1 | banana-slides | Melhor UX prompt-to-edit e vibe PPT, mas licença AGPL exige cautela. |
| P1 | presentation-ai | Bons padrões de editor web, temas e stack Next.js. |
| P1 | powerpoint-skill | Skill compacta com hard rules, matemática, diagramas e QA visual. |
| P2 | slide-deck-ai | Útil como CLI/API Python simples e multi-provider baseline. |
| P2 | PresentAgent-2 | Futuro multimodal: query→research→slides→vídeo/interação. |

## O Que Temos Hoje

O `slides-creator` já tem:

- 6 agentes operacionais;
- workflow v2.0.0 com 7 fases;
- feature flags para visual generation, YouTube entrypoint, HTML standalone render, motion narrative e design direction advisor;
- decisão `editable vs image PPTX`;
- task `export-editable-pptx.md`;
- QA com PPTEval/GAD;
- templates, KBs, palette registry, token registry e visual engines.

O ponto fraco é que ele ainda é majoritariamente **contract/handoff-based**, não um produto/runtime completo.

## Entrega Nova Do Bench Para A Skill

O bench agora materializa `slide-creator-skill-blueprint.md/json`: um mapa bench→skill que define o que absorver de cada projeto, quando usar cada padrão, qual artifact emitir, quais killer items bloqueiam output e quais bibliotecas tornam a `slide-creator` autocontida.

Isso impede a skill de voltar a inventar roteiro, estrutura, PPTX, API, prompt-to-edit ou research do zero. Cada capability conhecida passa a ter fonte benchmark e contrato de saída.

## Arquitetura Recomendada

Nome de trabalho: **slide creator skill stack**.

Componentes:

- `slides-creator`: cérebro governado e workflow oficial.
- `ppt-master`-style renderer: export nativo editável.
- Presenton-style API/MCP: geração self-hosted e integração com agentes.
- PPTAgent-style planning/reflection: qualidade agentic.
- banana/presentation-ai-style editor: UX prompt-to-edit.
- PostHog/Umami/Plausible: analytics.

## Decisão Técnica

Não devemos começar pela UI. A ordem correta:

1. **Renderer editável**: sem PPTX editável real, não competimos em B2B.
2. **API/MCP**: sem runtime, viramos apenas skill manual.
3. **Agentic planning**: para superar decks genéricos.
4. **Editor prompt-to-edit**: para competir com Gamma na experiência.
5. **Share/analytics/video**: para distribuição e produto.

## Riscos

- `banana-slides` é AGPL-3.0: usar como benchmark/ideação, não copiar código sem decisão jurídica.
- `ppt-master` tem alta qualidade, mas é um harness/skill e depende muito do modelo; exige adaptação para SINKRA.
- Presenton é Apache-2.0 e mais fácil de absorver, mas seu modelo HTML/Tailwind não resolve sozinho PPTX nativo editável.
- PresentAgent-2 ainda é novo e pesado; melhor deixar para fase futura.

## Próximo Passo Recomendado

Criar uma story/epic de absorção P0 com três entregas:

1. `slides-renderer` com SVG→PPTX nativo editável inspirado em `ppt-master`;
2. `slides-api` com endpoint/MCP inspirado em Presenton;
3. `planning-reflection` usando padrões de PPTAgent no workflow `generate-presentation`.

O objetivo não é “copiar Gamma”. É entregar algo que Gamma não entrega: **deck consultivo, rastreável, local-first, editável, com governança SINKRA e API/MCP**.
