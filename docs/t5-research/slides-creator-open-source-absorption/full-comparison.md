# Full Comparison — Slides Creator Open-Source Absorption

## 1. Pergunta

Quais projetos open-source precisamos absorver para criar uma stack própria de criação de slides com IA no nível do Gamma, mas superior em contexto B2B: editável, rastreável, local-first, governada e integrável por API/MCP?

## 2. Resultado Curto

Nenhum projeto sozinho resolve o problema. O melhor desenho é **slide creator skill stack**:

- `squads/slides-creator`: núcleo narrativo, briefing contract, gates e QA.
- `ppt-master`: renderer nativo editável e template replication.
- Presenton: app/API/MCP/self-hosted, BYOK/Ollama.
- PPTAgent: planner, research/design agents, reflection e avaliação.
- banana-slides: benchmark de UX prompt-to-edit, edição regional e vídeo.
- presentation-ai: editor web, outline-first, temas e sharing.
- powerpoint-skill: matemática, diagramas, OMML e hard rules.
- slide-deck-ai: CLI Python e provider baseline.
- PresentAgent-2: direção futura para query→research→slides→vídeo/Q&A.

## 3. Evidência Local

| Projeto | Evidência principal | Leitura |
|---|---|---|
| `slides-creator` | `squads/slides-creator/README.md`, `ARCHITECTURE.md`, `workflows/generate-presentation.yaml`, `data/editable-vs-image-pptx-decision.md` | Forte em governança, fraco em runtime. |
| `ppt-master` | `../bench/ppt-master/README.md`, `skills/ppt-master/workflows/live-preview.md`, `docs/templates-guide.md` | Melhor evidência de PPTX editável nativo. |
| Presenton | `../bench/presenton/README.md`, `docker-compose.yml`, `servers/fastapi`, `servers/nextjs` | Melhor base app/API/MCP/self-hosted. |
| PPTAgent | `../bench/PPTAgent/README.md`, `pptagent/pptgen.py`, `deeppresenter/*` | Melhor arquitetura agentic/reflexiva. |
| banana-slides | `../bench/banana-slides/README_EN.md` | Melhor UX de edição visual, mas AGPL. |
| presentation-ai | `../bench/presentation-ai/README.md`, `apps/web/app`, `apps/web/lib` | Bom editor Next.js com outline-first e temas. |
| powerpoint-skill | `../bench/powerpoint-skill/README.md` | Melhor pacote compacto de OMML/diagramas/hard rules. |
| slide-deck-ai | `../bench/slide-deck-ai/README.md` | CLI Python útil para baseline e LiteLLM/Ollama. |
| PresentAgent-2 | `../bench/PresentAgent-2/README.md` | Mais avançado em multimodal/vídeo/Q&A, menos maduro para MVP. |

## 4. Comparação por Eixo

### 4.1 Renderer e Export

| Capacidade | Nosso estado | Melhor referência | Absorção |
|---|---|---|---|
| PPTX nativo editável | Parcial; há decisão e task | `ppt-master` | Criar IR visual restrito e exportar para DrawingML/PPTX nativo. |
| Export PDF | Parcial/dependente de downstream | Presenton, banana-slides | Pipeline de export com fallback visual. |
| Template replication | Parcial via registry interno | `ppt-master` + Presenton | Extrair tema, fontes, masters/layouts e imagens de PPTX de referência. |
| Animações/transições | Ausente ou conceitual | `ppt-master` | Deixar fora do MVP, mas desenhar schema. |
| Vídeo/narração | Conceitual | `ppt-master`, banana-slides, PresentAgent-2 | P2 depois de PPTX/API. |

### 4.2 Produto, API e Operação

| Capacidade | Nosso estado | Melhor referência | Absorção |
|---|---|---|---|
| App self-hosted | Ausente | Presenton | `services/slides-api` + app/admin mínimo. |
| MCP | Parcial conceitual | Presenton + PPTAgent | `slides.generate`, `slides.review`, `slides.export`. |
| BYOK/local | Parcial via princípios | Presenton + slide-deck-ai | Providers OpenAI/Gemini/Anthropic/Ollama/custom por config. |
| Docker/Desktop | Ausente | Presenton | P2; antes validar API headless. |
| API de geração | Ausente como produto | Presenton | Endpoint síncrono/assíncrono com `deck_spec_id`. |

### 4.3 Agentic Planning e QA

| Capacidade | Nosso estado | Melhor referência | Absorção |
|---|---|---|---|
| Briefing contract | Forte | Nosso squad | Manter como origem de verdade. |
| Pyramid/SCQA/action titles | Forte | Nosso squad | Manter e expor no DeckSpec. |
| Planner/research/design agents | Parcial | PPTAgent | Adicionar `planning_reflection` e design critique. |
| Avaliação automatizada | Forte conceitual, runtime parcial | PPTAgent PPTEval | Integrar rubricas complementares. |
| QA visual | Parcial | powerpoint-skill + PPTAgent | Render preview + checklist editabilidade + screenshots. |

### 4.4 UX e Editor

| Capacidade | Nosso estado | Melhor referência | Absorção |
|---|---|---|---|
| Outline-first | Parcial | presentation-ai | UI de outline antes de slides. |
| Prompt-to-edit | Ausente | banana-slides | Edição verbal com diff e confirmação. |
| Edição regional | Ausente | banana-slides | P2, após modelo de object IDs no DeckSpec. |
| Temas | Parcial via registries | Presenton + presentation-ai | Theme runtime com import de PPTX. |
| Sharing | Ausente | presentation-ai/Gamma | P2 depois de renderer/API. |

## 5. Equivalência Forte/Parcial/Sem Equivalente

| Capacidade | slides-creator | OSS que cobre | Nível final esperado |
|---|---|---|---|
| Narrativa consultiva | Forte | Nenhum supera | Forte |
| PPTX editável | Parcial | `ppt-master` | Forte |
| API/MCP | Fraco | Presenton | Forte |
| Agentic reflection | Parcial | PPTAgent | Forte |
| Prompt-to-edit | Sem equivalente | banana-slides/presentation-ai | Parcial alta no MVP+1 |
| Math/diagramas | Parcial | powerpoint-skill | Forte |
| Vídeo/Q&A | Fraco | PresentAgent-2 | Parcial futura |
| Licença segura | Forte internamente | MIT/Apache fortes; AGPL limita | Forte com política |

## 6. Arquitetura-Alvo

```text
Input: prompt | PDF | DOCX | PPTX | URL | YouTube
  -> briefing.normalized.json
  -> narrative-plan.yaml
  -> deck-spec.yaml
  -> slide-specs/*.yaml
  -> planning-reflection.jsonl
  -> render request
      -> native-pptx renderer
      -> pdf/image fallback
      -> web preview
  -> qa-report.json
  -> export manifest
```

## 7. Decisão de Produto

O primeiro produto não deve ser um editor completo. O MVP é:

1. CLI/API/MCP para gerar deck.
2. PPTX nativo editável validado.
3. PDF fallback.
4. QA narrativo + visual + editabilidade.
5. DeckSpec versionável.

O editor prompt-to-edit entra quando o DeckSpec tiver IDs estáveis por slide/elemento. Sem isso, a UX vira edição destrutiva.

## 8. Decisão de Absorção

| Wave | Absorver | Não absorver ainda |
|---|---|---|
| P0 | `ppt-master`, Presenton, PPTAgent | Editor completo, vídeo, analytics |
| P1 | presentation-ai, powerpoint-skill, banana patterns | Código AGPL de banana sem decisão |
| P2 | PresentAgent-2, vídeo, Q&A, analytics | Multimodal pesado no MVP |

## 9. Risco de Execução

O risco maior é subestimar o renderer. A diferença entre "gera PPTX" e "gera PPTX editável profissional" é grande. O P0 deve medir editabilidade real, não apenas arquivo que abre.

## 10. Critério de Sucesso

slide creator skill stack está à altura do Gamma quando:

- gera deck a partir de prompt/documento;
- exporta PPTX e PDF;
- mantém 80%+ dos elementos principais editáveis;
- passa QA narrativo/visual;
- roda via CLI/API/MCP;
- suporta BYOK/local;
- preserva fontes e decisões no DeckSpec.
