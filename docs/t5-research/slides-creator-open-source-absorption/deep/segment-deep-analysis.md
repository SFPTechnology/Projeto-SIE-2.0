# Segment Deep Analysis — Apps, Skills e Engines

Data: 2026-05-17

## Leitura Executiva

A comparação mais justa não pergunta “quem vence tudo?”. A pergunta correta é:

1. **Qual app vira base de produto?**
2. **Qual skill/agente vira cérebro narrativo?**
3. **Qual engine vira renderer/runtime?**
4. **Qual player entra só como referência de UX, teste ou capability futura?**

O resultado técnico é:

| Camada | Base primária | Complementos | Por quê |
|---|---|---|---|
| App/produto | Presenton | presentation-ai, banana-slides | Presenton já tem API/MCP/self-hosting; presentation-ai melhora temas/share/local UX; banana inspira prompt-to-edit. |
| Skill/agente | slide creator skill | PPTAgent, PresentAgent-2, powerpoint-skill | SINKRA governa narrativa/QA; PPTAgent dá reflection/PPTEval; PresentAgent-2 dá research→vídeo; powerpoint-skill dá rigor técnico. |
| Engine/runtime | ppt-master | Presenton, powerpoint-skill, slide-deck-ai | ppt-master resolve PPTX editável; Presenton resolve API/MCP; powerpoint-skill resolve matemática/QA; slide-deck-ai resolve Python/CLI/offline. |

## 1. Apps e Produto Final

### Presenton vs presentation-ai

Presenton vence como **runtime de produto** porque combina Docker, desktop, FastAPI, Next.js, API de geração, MCP, BYOK, Ollama e export. Isso é mais próximo de um produto operável em SINKRA.

presentation-ai é mais forte em **experiência de editor**, temas, importação de tema PPTX, sharing público e fluxo de modelo local via Ollama/LM Studio. Ele parece melhor como referência de UI e branding do que como backend canônico.

**Decisão:** Presenton deve virar referência de runtime/app; presentation-ai deve virar referência de editor, theme manager, model selector e sharing.

### Presenton vs banana-slides

banana-slides vence em inspiração de **prompt-to-edit/vibe PPT**: criação, edição natural, export e vídeo aparecem como proposta central. Mas o risco AGPL e a maturidade ainda impedem absorção direta.

Presenton é mais seguro para base de produto: licença permissiva, self-hosting, API, MCP e configuração enterprise.

**Decisão:** banana-slides entra como benchmark de UX e testes black-box; Presenton entra como arquitetura absorvível.

### presentation-ai vs banana-slides

presentation-ai é mais absorvível para editor web, temas, sharing e modelo local. banana-slides é mais agressivo na experiência prompt-native.

**Decisão:** usar presentation-ai para estrutura de produto/editor e banana-slides para comportamento esperado de prompt-to-edit.

## 2. Skills, Agentes e Workflows

### slide creator skill vs PPTAgent

SINKRA vence no que importa para decks executivos: briefing, Pyramid/SCQA, action titles, fontes, APA, human gates, KBs por indústria e QA governado.

PPTAgent vence como referência de arquitetura agentic acadêmica: Planner, Research, Design, SubAgent, MCP, offline mode e PPTEval.

**Decisão:** não substituir SINKRA por PPTAgent. Absorver o que falta: reflection loop, PPTEval formalizado e separação clara planner/research/design.

### slide creator skill vs PresentAgent-2

PresentAgent-2 é mais avançado em pesquisa aberta, multimodalidade, vídeo narrado e Q&A grounded. SINKRA é melhor para deck corporativo rastreável e governado.

**Decisão:** PresentAgent-2 deve virar trilha P2/P3 para `query -> research -> video/Q&A`, não MVP do core de slides.

### slide creator skill vs powerpoint-skill

powerpoint-skill é melhor em matemática nativa, diagramas, PptxGenJS, OMML, overlap checks e QA técnico. SINKRA é melhor em narrativa e governança.

**Decisão:** absorver o rigor técnico do powerpoint-skill dentro de `qa-inspector` e `design-renderer`, sem transformar o squad em uma skill acadêmica.

## 3. Engines, Renderer e Runtime

### ppt-master vs Presenton

ppt-master vence na tese mais crítica para B2B: PPTX nativo editável com shapes, texto, charts e template replication. Presenton vence em produto, API, MCP e self-hosting.

**Decisão:** o renderer enterprise deve seguir ppt-master; o runtime de serviço deve seguir Presenton.

### ppt-master vs powerpoint-skill

ppt-master é melhor para geração visual livre e conversão SVG→DrawingML. powerpoint-skill é melhor para decks técnicos com fórmulas, diagramas, PptxGenJS helpers e QA de overlap.

**Decisão:** usar ppt-master como caminho principal de PPTX editável e powerpoint-skill como subengine para matemática, diagramas e QA técnico.

### Presenton vs slide-deck-ai

Presenton é produto completo. slide-deck-ai é mais simples, Python-first, CLI/API e bom para fluxo offline/Ollama com baixa superfície.

**Decisão:** slide-deck-ai não vira app; vira referência para CLI/headless, Python adapters e provider abstraction.

## 4. O Que Ainda Não Está Bem Resolvido por Nenhum Player

| Gap | Situação | Implicação |
|---|---|---|
| Colaboração realtime robusta | Nenhum player de slides resolve de forma completa. | Entrar com Yjs/Hocuspocus depois do editor básico. |
| Analytics de deck | Quase ausente nos players OSS. | Usar PostHog/Umami/Plausible no share runtime. |
| QA visual automatizado end-to-end | Fragmentado entre SINKRA, PPTAgent, ppt-master e powerpoint-skill. | Criar QA composto: PPTEval + editability + screenshot + overlap + fontes. |
| PPTX editável + visual premium + app UX | Nenhum player único cobre as três coisas. | Arquitetura composta é obrigatória. |
| Licença segura para UX prompt-to-edit | banana-slides é útil, mas AGPL. | Absorver comportamento, não código. |

## 5. Ranking de Absorção Real

| Ordem | Absorção | Tipo | Por que vem antes |
|---:|---|---|---|
| 1 | ppt-master Native IR / SVG→DrawingML | Engine | Fecha o gap mais difícil: PPTX editável real. |
| 2 | Presenton API/MCP/self-hosting | Runtime | Transforma skill em serviço operável. |
| 3 | SINKRA narrative core preservado | Skill | É o diferencial próprio; não pode ser diluído. |
| 4 | powerpoint-skill QA técnico/math/diagramas | Subengine QA | Evita decks tecnicamente bonitos, mas quebrados. |
| 5 | PPTAgent reflection/PPTEval | Agentic QA | Melhora coerência e revisão multi-etapa. |
| 6 | presentation-ai editor/theme/share | App UX | Fecha adoção diária e branding. |
| 7 | banana prompt-to-edit patterns | UX reference | Inspira, mas exige isolamento legal. |
| 8 | PresentAgent-2 research/video/Q&A | P2/P3 multimodal | Alto valor, mas não é MVP de deck corporativo. |
| 9 | slide-deck-ai Python/CLI/offline | Infra fallback | Útil para batch e adapters, não para produto principal. |

## 6. Conclusão Técnica

O benchmark mais profundo aponta para uma arquitetura inevitavelmente composta:

```text
SINKRA narrative/QA
  + PPTAgent reflection
  + PresentAgent-2 research/video mode
  + ppt-master native PPTX engine
  + powerpoint-skill math/diagram/technical QA
  + Presenton API/MCP/self-hosted runtime
  + presentation-ai editor/theme/share patterns
  + banana-slides prompt-to-edit behavior
  + slide-deck-ai CLI/Python/offline fallback
```

O erro seria escolher um “vencedor” único. O acerto é transformar cada vencedor local em uma camada do slide creator skill stack.

