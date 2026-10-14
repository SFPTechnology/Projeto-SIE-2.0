# Evidence Strength Map — Comparação Profunda

Data: 2026-05-17

Este arquivo aprofunda a comparação separando evidência de README, código, testes e implicação de absorção. A matriz visual fica limpa; a justificativa técnica fica aqui.

## Evidência por Player

| Player | Segmento | Força da evidência | Veredito | Absorção |
|---|---|---|---|---|
| Presenton | Apps | strong-code+docs | Melhor base de produto self-hosted/API/MCP, não melhor renderer nativo. | Absorver arquitetura de produto, API, MCP, provider registry, app_data e template schema. Não usar como único renderer. |
| ppt-master | Engines/Runtime | strong-code+docs | Melhor evidência de PPTX nativo editável e pipeline técnico de export. | Absorver Native IR, SVG constraints, SVG quality checker, template replication, editability QA e chart verification. |
| slide creator skill | Skills/Agentes | strong-internal-governance | Melhor núcleo narrativo/QA, mas ainda precisa runtime e renderer. | Preservar como camada de planejamento, governança, QA e release. Conectar a engines e app layer externos. |
| PPTAgent | Skills/Agentes | strong-docs+code | Melhor referência acadêmica para planejamento/reflexão/eval, menos produto final. | Absorver taxonomia de roles, reflection loop, PPTEval e estrutura planner→design→render. |
| PresentAgent-2 | Skills/Agentes | strong-docs+tests | Melhor referência multimodal query→research→video, mas risco de licença/complexidade. | Absorver benchmark/eval multimodal, source.md pipeline, Q&A grounded e video mode como P2/P3. |
| presentation-ai | Apps | medium-code+docs | Melhor app para editor web/temas/share/local model UX, mas não engine profunda. | Absorver theme UX, model selector local, share page e estruturas de editor/outlines. |
| banana-slides | Apps | medium-docs+code-risk | Melhor inspiração de prompt-to-edit/vibe PPT, mas AGPL e maturidade exigem isolamento. | Usar como referência de UX e testes black-box; não copiar código sem ADR jurídico. |
| slide-deck-ai | Engines/Runtime | medium-code+docs | Boa base Python/CLI/headless/provider, fraca em UX e design premium. | Absorver CLI/headless, Python API patterns, provider abstraction e offline mode. |
| powerpoint-skill | Engines/Runtime | strong-skill-docs+code | Melhor disciplina para PPT técnico, matemática nativa e QA visual. | Absorver math/diagram pipeline, overlap checks, OMML injection, QA técnico e PptxGenJS helper patterns. |

## Pontos Fortes e Fracos

### Presenton

**Forças**

- Docker/self-hosting e desktop app
- FastAPI + Next.js + API de geração/export
- MCP gerado a partir de OpenAPI
- multi-provider LLM/imagem com Ollama/BYOK
- biblioteca de templates TSX

**Limitações**

- PPTX editável não é tão profundo quanto ppt-master
- analytics/collab ainda são gaps de produto
- qualidade depende de templates e modelo

**Evidências locais**

- `../bench/presenton/README.md:26-29`
- `../bench/presenton/README.md:96-103`
- `../bench/presenton/README.md:173-180`
- `../bench/presenton/README.md:362-538`
- `../bench/presenton/servers/fastapi/mcp_server.py`
- `../bench/presenton/servers/nextjs/app/api/export-presentation/route.ts`
- `../bench/presenton/servers/nextjs/app/presentation-templates/`

### ppt-master

**Forças**

- SVG como IR visual e conversão para DrawingML
- PPTX com shapes/text/charts editáveis
- live preview com anotações
- template replication via OOXML
- animações/transições reais
- narração e vídeo via PowerPoint

**Limitações**

- É skill/workflow de IDE, não app SaaS
- não resolve sharing/analytics/collab
- sequencialidade e authoring manual por IA aumentam custo operacional

**Evidências locais**

- `../bench/ppt-master/README.md:34-53`
- `../bench/ppt-master/README.md:59-71`
- `../bench/ppt-master/docs/technical-design.md:53-93`
- `../bench/ppt-master/docs/technical-design.md:203-224`
- `../bench/ppt-master/skills/ppt-master/SKILL.md:56-81`
- `../bench/ppt-master/skills/ppt-master/templates/charts/`

### slide creator skill

**Forças**

- Pyramid/SCQA/action titles
- governança de fontes e APA
- human gates e QA
- knowledge bases por indústria
- squad multiagente e handoffs

**Limitações**

- não é app visual
- não entrega sozinho API/MCP/render nativo completo
- precisa motor PPTX e editor web

**Evidências locais**

- `squads/slides-creator/`
- `.agents/skills/slides-chief/SKILL.md`
- `outputs/sinkra-squad/criacao-slides-ia/slides-creator-absorption-plan.md`

### PPTAgent

**Forças**

- Planner/Research/Design/SubAgent roles
- DeepPresenter com research e tools
- MCP support
- offline mode e PPTX export
- PPTEval para Content/Design/Coherence

**Limitações**

- setup complexo
- dependência de modelo/tuning recomendado
- UX menos pronta que apps
- não resolve produto SaaS

**Evidências locais**

- `../bench/PPTAgent/README.md:65-67`
- `../bench/PPTAgent/README.md:81-125`
- `../bench/PPTAgent/README.md:440`
- `../bench/PPTAgent/deeppresenter/roles/`
- `../bench/PPTAgent/deeppresenter/agents/`
- `../bench/PPTAgent/pptagent/mcp_server.py`

### PresentAgent-2

**Forças**

- query→DeepResearch→source.md→refined_doc.json→pptx→video
- Q&A interativo com busca no vídeo
- TTS e sincronização audiovisual
- testes para documento, vídeo, API e pipeline

**Limitações**

- licença/absorção precisa confirmação
- stack pesada com multimodal/TTS/video
- mais video presentation que PPT workflow corporativo

**Evidências locais**

- `../bench/PresentAgent-2/README.md:49`
- `../bench/PresentAgent-2/README.md:119-168`
- `../bench/PresentAgent-2/README.md:174-242`
- `../bench/PresentAgent-2/test/test_video_pipeline.py`
- `../bench/PresentAgent-2/test/test_source_md_to_document.py`
- `../bench/PresentAgent-2/test/test_ppt_to_video.py`

### presentation-ai

**Forças**

- 38 temas e custom themes
- PPTX theme import
- public sharing
- Ollama e LM Studio
- Next.js app router

**Limitações**

- não tem o runtime/API/MCP de Presenton
- PPTX editável não tem profundidade de ppt-master
- mais app visual do que engine

**Evidências locais**

- `../bench/presentation-ai/README.md:54-66`
- `../bench/presentation-ai/README.md:78`
- `../bench/presentation-ai/README.md:213-238`
- `../bench/presentation-ai/src/lib/presentation/pptx-theme-extractor.ts`
- `../bench/presentation-ai/src/app/share/presentation/[id]/page.tsx`

### banana-slides

**Forças**

- UX AI-native/prompt-first
- export PDF/PPTX e video
- evolução de PPTX editável em beta
- vários providers chineses + OpenAI/Gemini

**Limitações**

- AGPL limita absorção de código
- PPTX editável ainda em beta
- LibreOffice/font issues para upload PPTX
- menos seguro como base enterprise

**Evidências locais**

- `../bench/banana-slides/README.md:121-145`
- `../bench/banana-slides/README.md:169-190`
- `../bench/banana-slides/README.md:243-285`
- `../bench/banana-slides/README.md:394-399`

### slide-deck-ai

**Forças**

- python-pptx assembly
- Python API + CLI
- templates PPTX
- LiteLLM/provider migration
- Ollama offline
- no key storage claim

**Limitações**

- layout/design mais básico
- não resolve editor web
- sem MCP/app completo
- PPTX depende de templates e python-pptx

**Evidências locais**

- `../bench/slide-deck-ai/README.md:42-67`
- `../bench/slide-deck-ai/README.md:87-121`
- `../bench/slide-deck-ai/README.md:135-172`
- `../bench/slide-deck-ai/src/slidedeckai/core.py`
- `../bench/slide-deck-ai/src/slidedeckai/cli.py`
- `../bench/slide-deck-ai/src/slidedeckai/helpers/pptx_helper.py`

### powerpoint-skill

**Forças**

- PptxGenJS script generation
- OMML nativo
- LaTeX fallback 600DPI
- Graphviz/Mermaid/TikZ
- LibreOffice PDF visual QA
- check_overlaps e quality scoring

**Limitações**

- não é app
- não tem API/MCP/self-hosting
- pouco foco em prompt-to-edit
- depende de toolchain local ampla

**Evidências locais**

- `../bench/powerpoint-skill/README.md:3-27`
- `../bench/powerpoint-skill/README.md:142-177`
- `../bench/powerpoint-skill/README.md:221-234`
- `../bench/powerpoint-skill/powerpoint-slides/SKILL.md:22-38`
- `../bench/powerpoint-skill/powerpoint-slides/SKILL.md:69-79`
- `../bench/powerpoint-skill/powerpoint-slides/scripts/`


## Lentes de Decisão

| Lente | Pergunta | Vencedores | Ação SINKRA |
|---|---|---|---|
| Produto/App | Usuário não técnico consegue criar, editar, exportar e compartilhar? | Presenton, presentation-ai, banana-slides | Criar web app próprio usando Presenton como runtime e UX patterns dos demais. |
| PPTX editável | O arquivo final tem objetos nativos editáveis, não screenshots? | ppt-master, powerpoint-skill | Native IR + SVG/DrawingML + PptxGenJS/OMML QA. |
| Agente narrativo | O sistema pensa narrativa, fontes, outline e revisão? | slide creator skill, PPTAgent, PresentAgent-2 | Preservar slides-chief/content-architect e absorver reflection/PPTEval. |
| Self-host/API/MCP | Pode rodar como serviço e ser operado por agentes? | Presenton, slide-deck-ai, PPTAgent | API/MCP canônicos em services/slides-api e mcp/slides-server. |
| Multimodal/vídeo | Transforma fontes abertas em vídeo narrado e Q&A? | PresentAgent-2, ppt-master, banana-slides | P2/P3: video mode, TTS, Q&A grounded, não MVP. |
| Absorção legal | Pode virar código nosso com baixo risco? | Presenton, ppt-master, PPTAgent, powerpoint-skill, slide-deck-ai, presentation-ai | AGPL/sem licença ficam como referência conceitual/black-box. |

## Comparação Arquitetural

| Eixo | Comparação |
|---|---|
| Source → Plan → Render | **presenton:** Prompt/docs → FastAPI generation → TSX templates/export<br>**ppt_master:** PDF/DOCX/URL/MD → Strategist/Executor → SVG→DrawingML PPTX<br>**sinkra:** Briefing → narrative agents → DeckSpec/NativeIR → renderer services |
| Editable PPTX strategy | **presenton:** Export service; good product flow, less evidence of object-level QA<br>**ppt_master:** Primary thesis: native DrawingML objects; explicit SVG constraints/checkers<br>**sinkra:** Adopt ppt-master-style native path as enterprise target |
| UX strategy | **presenton:** Ready product UI/API<br>**banana:** Prompt-to-edit/vibe PPT reference<br>**presentation_ai:** Theme/outlines/share reference |
| QA strategy | **pptagent:** PPTEval Content/Design/Coherence<br>**powerpoint_skill:** Structural + visual + overlap + formula QA<br>**sinkra:** Combine PPTEval + editability + visual smoke + human gates |
| Runtime strategy | **presenton:** Docker/FastAPI/Next/MCP<br>**slide_deck_ai:** Python CLI/API/offline<br>**sinkra:** CLI-first + service + MCP + dashboard contract |
