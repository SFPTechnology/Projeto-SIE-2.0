# External Inventory — Open-Source Slide AI Projects

Data: 2026-05-17

Todos os repositórios foram clonados localmente em `../bench/`.

| Projeto | Local clone | Stars | Forks | Licença | Arquivos | Absorver |
|---|---|---:|---:|---|---:|---|
| `hugohe3/ppt-master` | `../bench/ppt-master` | 17.537 | 1.685 | MIT | 13.196 | Pipeline SVG → DrawingML/PPTX nativo editável, template replication, live preview, animações, narração. |
| `Anionex/banana-slides` | `../bench/banana-slides` | 14.569 | 1.713 | AGPL-3.0 | 472 | UX prompt-to-edit, seleção regional, asset toolbox, vídeo com narração. |
| `presenton/presenton` | `../bench/presenton` | 5.020 | 977 | Apache-2.0 | 2.362 | App/API/self-hosting, MCP, BYOK, Ollama, template HTML/Tailwind, geração via documentos. |
| `icip-cas/PPTAgent` | `../bench/PPTAgent` | 4.371 | 530 | MIT | 218 | Pipeline agentic: planner, research, design, reflection, PPTEval e template induction. |
| `allweonedev/presentation-ai` | `../bench/presentation-ai` | 2.806 | 491 | MIT | 878 | Next.js app, outline-first UX, editor moderno, temas, PptxGenJS, Plate/ProseMirror stack. |
| `barun-saha/slide-deck-ai` | `../bench/slide-deck-ai` | 355 | 57 | MIT | 439 | CLI/Python API simples, multi-provider via LiteLLM, Ollama/offline, PDF→deck com `python-pptx`. |
| `Noi1r/powerpoint-skill` | `../bench/powerpoint-skill` | 83 | 7 | MIT | 19 | Skill compacta com hard rules, PptxGenJS, OMML math, Mermaid/Graphviz/TikZ, visual QA. |
| `AIGeeksGroup/PresentAgent-2` | `../bench/PresentAgent-2` | 12 | 0 | sem licença detectada | 626 | Query→deep research→slides→narration/video, multimodal presentation agents. |

## Leitura por Categoria

### 1. Melhor motor de PPTX editável: `ppt-master`

É o projeto mais importante para absorção técnica. O diferencial não é só gerar slides, mas gerar **PowerPoint nativo editável** com shapes reais, texto real, charts reais, animações, narração e template replication a partir de `.pptx`.

O pipeline central é: fonte/documento → design spec → SVG por slide → conversão SVG para DrawingML → `.pptx` editável.

### 2. Melhor UX “Vibe PPT”: `banana-slides`

É forte como produto de interação: ideia/outline/descrição, upload de materiais, referência de estilo, edição verbal de regiões, export PPTX/PDF e vídeo. A licença AGPL-3.0 exige cuidado: bom para estudar padrões e benchmark, ruim para copiar código dentro de produto proprietário sem decisão jurídica.

### 3. Melhor app/API self-hosted: `Presenton`

É a melhor base se quisermos expor geração como serviço: Docker, desktop, FastAPI, Next.js, MCP, BYOK, Ollama, providers múltiplos e endpoint `/api/v1/ppt/presentation/generate`.

### 4. Melhor cérebro agentic: `PPTAgent`

Traz o melhor desenho de pipeline agentic: Planner, Research, PPTAgent, Design, reflection e PPTEval. Não substitui nosso squad; informa como fortalecer a camada de planejamento/reflexão.

### 5. Melhor app editor web para absorver UI patterns: `presentation-ai`

Tem stack Next.js moderna, editor rico, temas, agentes, PptxGenJS e rotas de geração. É menos central que Presenton, mas tem material útil para editor e UX de outline.

### 6. Melhor baseline simples/CLI: `slide-deck-ai`

Útil para extrair a disciplina de API Python/CLI, multi-provider e offline Ollama, mas não é o núcleo visual.

### 7. Melhor skill pequena para slides acadêmicos: `powerpoint-skill`

Muito relevante como referência de skill: regras duras, matemática nativa OMML, diagramas e QA visual. É pequena o bastante para virar padrão de como escrever uma skill de slides focada.

### 8. Futuro multimodal: `PresentAgent-2`

Ainda novo, mas relevante para visão de query→deep research→video presentation com TTS, mídia dinâmica e Q&A.

