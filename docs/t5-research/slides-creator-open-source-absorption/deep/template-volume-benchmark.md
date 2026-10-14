# Template Volume Benchmark — slide creator skill

Data: 2026-05-18

## Pergunta

Estamos à frente dos outros players em quantidade de templates, decks, temas e estruturas?

Resposta curta: **ainda não em source decks/PPTX reais no nível PPTAgent/ppt-master**, mas a skill já passou a meta mínima útil em roteiros, funções de slide, visuais, temas e wireframes HTML. Estamos à frente em **amplitude de roteamento, contratos, playbooks, QA e taxonomia autocontida**. O próximo gap real é criar fixtures renderizadas e source decks.

## Contagem da `slide creator skill`

| Categoria | Quantidade | Observação |
|---|---:|---|
| YAMLs em `templates/` | 75 | Inclui contratos, schemas, QA, runtime, visual, deck e import. |
| Deck templates de rota | 20 | Roteiros por tipo de apresentação, agora cobrindo demo de IA, auditoria DS, investor update, arquitetura, case, fundraising, proposta, QBR, curso, workshop, launch, postmortem e hiring. |
| Deck templates absorvidos de copy | 4 | Oferta, VSL, curso/webinar e pitch/proof. |
| Playbooks | 8 | Benchmark, webinar, sales/offer, VSL, financeiro/board, produto, pitch, curso/workshop. |
| Slide-function templates | 60 | Estruturas por função de audiência, incluindo decisão, risco, demo, evidência, arquitetura, pricing, case, facilitação, experimento, maturidade, lançamento, incidentes, onboarding, scoring, personas, compliance, survey, social proof, API/code e slides utilitários finais. |
| Visual templates | 105 | Charts, diagramas, matrizes, layouts executivos, arquitetura, risco, pricing, prova, cohort, unit economics, launch, workshop, incidentes, scoring, traceability, compliance, survey, portfolio, brand, API/code, team/contact e aliases formais usados por rotas antigas. |
| Chart data modes | 14 | Contratos de dados para gráficos. |
| AI image types | 15 | Tipos/rotas de imagem. |
| Layout families | 5 | Famílias abstratas de layout. |
| Media layouts | 4 | Estruturas para mídia. |
| Composition patterns | 5 | Primary + modifier composition. |
| Brand-system patterns | 8 | Padrões de tradução de design system para slides. |
| AIOX deep patterns | 11 | Padrões extraídos do aiox-brandbook. |
| Redpine deep patterns | 8 | Padrões extraídos do redpine-ds. |
| Theme profiles | 25 | Temas prontos por contexto: board, pitch, técnico, acadêmico, SaaS, acessibilidade, brandbook, healthcare, fintech, educação, enterprise, launch, policy, premium, cyber, creator webinar, legal, analytics, creative agency, government e startup demo. |
| Brand-system profiles | 2 | Sistemas de marca empacotados. |
| Design philosophies | 20 | Escolas visuais para fallback e direção criativa. |
| Runtime contracts | 29 | Job, render, export, edit, import, MCP-ready behavior. |
| QA gate items | 24 | Gates explícitos. |
| Research routes | 4 | HTML, motion media, scholar/benchmark, local files. |
| Import packs | 6 | Beamer, CIP, default, HIT, THU, UCAS. |
| Wireframes HTML | 58 | Exemplos visuais estáticos para executive summary, decisão, waterfall, arquitetura, auditoria DS, case, risk, pricing, agenda, workshop, launch, unit economics, cohort, maturity, incident, hiring, scoring, persona, traceability, compliance, survey, roadmap, portfolio, brand, social proof, objection, story map, architecture tradeoff, competitive landscape, dependency map, decision tree, data lineage, experiment grid, quote evidence, sankey, scatter, org chart, value chain, responsibility matrix, feature matrix, harvey balls, dashboard, screen sequence, moodboard, API request/response, code explanation, mission/vision, business challenges, service catalog, team credentials, table of contents e contact next step. |
| Design 100 fixture files | 6 | Caminho feliz validável para Design 100. |
| Source deck fixtures | 8 | Packs autocontidos para importar/replicar famílias de decks sem depender dos benches em runtime. |
| Brand fidelity playbooks | 4 | Playbooks para fidelidade além de logo/cor: template importado, editorial, operacional e técnico. |
| Rendered design fixture sets | 5 | Sets por job de deck para revisar screenshots/key slides e fechar dívida visual. |
| Design regression cases | 30 | Corpus de regressão visual por deck job, tema, densidade e wireframe. |
| Template import regression cases | 20 | Casos de importação/manifesto por família fonte. |
| Theme runtime snapshot cases | 16 | Snapshots para provar tokens em charts, diagramas, tabelas, mídia e metadata. |
| Narrative regression cases | 25 | Casos de crença atual/desejada, beats, funções, proof standard e failure test. |

## Contagem dos Players

| Player | Templates/decks/temas contados | Quantidade | Força real |
|---|---:|---:|---|
| Presenton | famílias de template | 13 | Famílias reais de UI/render. |
| Presenton | componentes de slide TSX | 183 | Maior biblioteca renderizável web/PPTX entre apps. |
| ppt-master | famílias de layout | 17 | Layout packs com SVG + design spec. |
| ppt-master | SVGs de layout | 86 | Templates visuais editáveis/importáveis. |
| ppt-master | design specs de layout | 17 | Manifestos visuais por família. |
| ppt-master | chart/diagram SVG templates | 71 | Biblioteca visual forte para charts/frameworks. |
| ppt-master | image-type templates | 15 | Hero, matrix, timeline, pyramid, scene etc. |
| ppt-master | example spec locks | 9 | Exemplos de execução/render lock. |
| ppt-master | icon SVGs | 11,631 | Biblioteca massiva de ícones, não equivalente a slide templates. |
| presentation-ai | template IDs AntV | 233 | Maior quantidade de estruturas visuais parametrizadas. |
| presentation-ai | theme names | 38 | Maior biblioteca de temas prontos. |
| PPTAgent | template packs | 6 | Packs PPTX reais com induction + image stats. |
| PPTAgent | source PPTX templates | 6 | Templates reais para indução. |
| PresentAgent-2 | resource templates PPTX | 5 | Templates PPTX prontos. |
| PresentAgent-2 | all resource PPTX | 9 | Inclui exemplos/decks. |
| banana-slides | job template rows | 2 | Forte em UX/edit, não em biblioteca local de templates. |
| powerpoint-skill | example PPTX | 1 | Forte em técnica/QA, não em volume. |
| slide-deck-ai | prompt templates | 2 | Forte em CLI simples, não em biblioteca visual. |

## Veredito por Requisito

| Requisito | Estamos à frente? | Por quê |
|---|---|---|
| Quantidade de templates visuais renderizáveis | **Não** | Presenton tem 183 componentes; presentation-ai tem 233 IDs; ppt-master tem 86 layouts + 71 charts. |
| Quantidade de temas prontos | **Ainda não, mas competitivo** | presentation-ai tem 38; nós subimos para 20 theme profiles e 2 brand-system profiles. |
| Quantidade de PPTX/source decks reais | **Não** | PPTAgent/PresentAgent têm PPTX reais; nós temos contratos/fixtures, mas não uma biblioteca PPTX. |
| Quantidade de roteiros/playbooks narrativos | **Sim** | Temos 20 route templates + 4 copy-derived + 8 playbooks com função, gates e narrativa. |
| Profundidade de QA e contratos | **Sim** | Temos 20 runtime contracts, 24 QA gates, Design 100 validator, score evidence e package validation. |
| Autocontenção da skill | **Sim** | A skill funciona sem depender do squad, com templates, scripts, references e fixture. |
| Inteligência de seleção | **Sim, em contrato** | Template selection report, runners-up, render-lock, design mastery, evidence ledger. |
| Prova visual/renderizada em volume | **Parcialmente** | Temos 58 wireframes HTML, 5 rendered design fixture sets e um fixture Design 100; ainda falta corpus de screenshots/regressão automatizada em volume. |

## Gap Real

O gargalo não é falta de “mais YAML”. É falta de volume de **templates visuais concretos**:

- mais wireframes HTML/TMPL por função;
- mais layouts por tipo de slide;
- mais temas prontos;
- mais source decks/PPTX de referência;
- mais fixtures renderizados;
- mais exemplos com screenshot/preview;
- catálogo navegável por função, densidade, mídia, chart, audience e export target.

## Wave Aplicada Nesta Revisão

Esta revisão priorizou templates de uso frequente, não variações decorativas. Wave 1:

- 5 novos route templates: AI product demo, design system audit, investor update, technical architecture review e customer case study.
- 12 novos slide-function templates: summary executivo, stack de evidência, risco, jornada, arquitetura, demo, objeção, case, pricing, market map, operating model e appendix source table.
- 28 novos visual templates: comparação, tabelas, timeline, checklist, stacked bar, gantt, gauge, progress, dumbbell, funil, executive snapshot, evidence cards, source panel, risk heatmap, swimlane, system flow, pricing, stakeholder, dashboard, screen sequence, myth/truth, case panel e responsibility matrix.
- 8 novos theme profiles: consulting midnight, boardroom graphite, founder pitch light, technical blueprint, academic paper, product SaaS clean, high contrast accessible e brandbook editorial.
- 6 novos wireframes HTML: executive summary, decision options, financial waterfall, technical architecture, design system audit e case study proof.

Wave 2:

- +8 route templates: fundraising pitch, sales proposal, QBR/operating review, training course, workshop facilitation, product launch, incident postmortem e hiring/onboarding.
- +18 slide-function templates: agenda contract, audience segmentation, problem cost, data insight, experiment results, retention cohort, unit economics, capability maturity, launch plan, training exercise, workshop canvas, governance model, migration plan, incident postmortem, hiring scorecard, roadmap decision, section divider e closing next steps.
- +20 visual templates: cohort retention, unit economics panel, competitive landscape, maturity ladder, org chart, value chain, dependency map, decision tree, data lineage, experiment grid, agenda timeline, quote evidence panel, workshop canvas, launch calendar, affinity map, incident timeline, corrective action table, hiring scorecard, ramp plan e section divider.
- +9 theme profiles: healthcare trust, fintech precision, education workshop, enterprise RFP, product launch vivid, nonprofit policy, luxury minimal, cyber security dark e creator webinar.
- +10 wireframes HTML: risk heatmap, pricing table, agenda timeline, workshop canvas, launch calendar, unit economics, cohort retention, maturity ladder, incident timeline e hiring scorecard.

Wave 3:

- +12 slide-function templates: scoring transparency, persona fit, requirements traceability, compliance readiness, survey results, roadmap status, portfolio allocation, brand principles, social proof wall, objections matrix, user story map e architecture tradeoff table.
- +19 visual templates: scoring rubric table, scoring band ladder, persona fit matrix, radar chart, traceability matrix, compliance grid, survey result panel, roadmap status board, portfolio allocation, treemap, brand principle cards, moodboard grid, logo wall, testimonial grid, objection matrix, user story map, architecture tradeoff table, sankey flow e scatter plot.
- +5 theme profiles: legal compliance, data analytics lab, creative agency, government policy e startup demo neon.
- +12 wireframes HTML: scoring rubric, persona fit matrix, traceability matrix, compliance grid, survey results, roadmap status, portfolio allocation, brand principles, social proof wall, objection matrix, user story map e architecture tradeoff table.

Wave 4:

- +17 wireframes HTML: competitive landscape, dependency map, decision tree, data lineage, experiment grid, quote evidence panel, sankey flow, scatter plot, org chart, value chain, responsibility matrix, feature matrix, harvey balls table, dashboard grid, screen sequence, roadmap decision e moodboard grid.
- Resultado: a skill bateu a meta mínima de wireframes HTML/TMPL (`50`) sem criar variações decorativas; os novos arquivos cobrem comparação, arquitetura, produto, dados, operação, design e prova.

Revisão QA:

- +10 visual templates de compatibilidade: hero claim, full bleed image, fishbone diagram, heatmap chart, roadmap vertical, circular stages, chevron process, contrast, comparison table e decision.
- Resultado: todas as referências `compatible_visuals` e `visual_family` em slide/deck templates agora apontam para visual templates existentes.

Wave 5 — absorção Presenton utilitária:

- +8 slide-function templates: API request/response, code explanation, mission/vision, business challenges, service catalog, team credentials, table of contents e contact next step.
- +10 visual templates: API request/response, code explanation split, mission vision panel, business challenges grid, service catalog grid, team credentials grid, table of contents, contact footer, closing card e social proof wall.
- +8 wireframes HTML: API request/response, code explanation, mission/vision, business challenges, service catalog, team credentials, table of contents e contact next step.
- Resultado: cobriu slides obrigatórios de decks técnicos, produto, propostas e apresentações executáveis que Presenton modela bem.

Wave 6 — Design mastery operacional:

- +8 source deck fixtures: ppt-master consulting/import, presentation-ai theme runtime, banana polish, PPTAgent academic induction, Presenton product story, Redpine operational design e AIOX brandbook editorial.
- +4 brand fidelity playbooks: template importado, brand editorial, design system operacional e diagrama técnico.
- +5 rendered design fixture sets: executivo/estratégia, produto/demo, brand manifesto, webinar/vendas e pesquisa/acadêmico.
- +1 ledger de transparência de score: explica por que uma nota é 86, 92, 96 ou 100 com base em cobertura, profundidade, fidelidade, evidência e absorvibilidade.
- Resultado: a categoria Design passa a ser liderada pela slide creator skill por média (95,22), com gaps residuais explícitos em parser/import corpus e screenshot regression.

Wave 7 — Design capability corpus:

- +30 design regression cases cobrindo 20+ deck jobs, 12+ themes, quatro níveis de densidade e key-slide review roles.
- +20 template import regression cases cobrindo ppt-master, presentation-ai, PPTAgent, Presenton, banana-slides, Redpine e AIOX brandbook.
- +16 theme runtime snapshot cases cobrindo 10 famílias de componentes: background, title, body, metric, chart, diagram, table, callout, media e metadata.
- +1 validador executável: `scripts/validate_design_capability.py`.
- Resultado: Design sobe para média 99,33 e 9/9 vitórias de linha na matriz.

Wave 8 — Narrative capability corpus:

- +24 narrative regression cases cobrindo benchmark, board, pitch, sales, webinar, VSL, demo, arquitetura, pesquisa, curso, design audit, incident, QBR, compliance, market landscape, roadmap, case, hiring, survey, portfolio, operating model, close, product strategy, thought leadership e strategy memo.
- +1 validador executável: `scripts/validate_narrative_capability.py`.
- Resultado: Planejamento/Narrativa sobe para média 100 e 9/9 vitórias de linha.

Wave 9 — Storyboard/runtime bridge:

- +1 storyboard/render bridge para conectar crença, função, visual, densidade, prova e risco de render.
- +1 speaker notes/narration contract com modos, timing, prova falada e sync de áudio.
- +1 runtime gap absorption corpus com 6 grupos: render/PPTX, editor, distribuição, multimídia, infra e automação.
- +1 validador executável: `scripts/validate_runtime_gap_capability.py`.
- Resultado: score consolidado sobe para 74,27, passa Presenton e fica a 0,52 de ppt-master.


Wave 10 — Delivery/API/MCP contracts:

- +1 delivery package contract com manifesto, modos de compartilhamento, permissões, schema de analytics e follow-up signal.
- +1 API/MCP/CLI contract com comandos, rotas, ferramentas, job lifecycle e safety boundaries.
- +1 validador executável: `scripts/validate_delivery_capability.py`.
- Resultado: score consolidado sobe para 77,51 e a slide creator skill vira #1 no mapa de absorção, mantendo PPTX renderer, editor runtime, infra e multimídia como gaps honestos de implementação.

Wave 11 — Narrative/design + editor bridge:

- +1 narrative-design moment grammar com 9 arquétipos: reframe, answer-first, tensão, mecanismo, prova, demo payoff, decisão, respiro e CTA.
- +1 storyboard edit contract para preservar crença, fontes, render-lock, regiões não selecionadas e ritmo visual durante prompt-to-edit.
- +1 validador executável: `scripts/validate_narrative_design_capability.py`.
- Resultado: Design/Narrativa ganham uma camada causal comum; Editor sobe apenas nas microdimensões cobertas por contrato, sem fingir editor visual real.

## Meta Para Virar Referência

| Camada | Meta mínima | Meta referência |
|---|---:|---:|
| Deck playbooks | 12 | 20 |
| Slide-function templates | 40 | 80 |
| Visual/layout templates | 60 | 150 |
| Chart/diagram templates | 50 | 100 |
| Theme profiles | 20 | 40 |
| Brand/template manifests | 10 | 30 |
| Wireframes HTML/TMPL | 50 | 150 |
| Design fixtures validados | 10 | 30 |
| Source decks/PPTX de referência | 5 | 20 |

## Próxima Absorção Recomendada

1. **Absorver volume estrutural de presentation-ai**: transformar os 233 IDs em taxonomy própria por categoria, não copiar UI.
2. **Absorver componentes renderizáveis de Presenton como inspiração de famílias**: criar equivalentes HTML/TMPL com slots e tokens.
3. **Absorver biblioteca de ppt-master**: mapear 71 charts + 86 layouts para `visual_templates` e `wireframes`.
4. **Criar theme pack parity**: subir de 3 para pelo menos 20 temas, com tokens completos.
5. **Criar design fixtures**: pelo menos 10 pacotes que passam em `validate_design_mastery.py`.

## Decisão

Para o requisito “quantidade de templates/decks”, a skill ainda **não está à frente de todos**. Ela está à frente em **inteligência de uso** dos templates. Para ficar referência absoluta, precisamos de uma próxima wave de **template volume absorption** focada em biblioteca visual concreta.
