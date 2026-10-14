# Absorption Decision Table

Data: 2026-05-17

Esta tabela transforma a comparação em decisão de implementação. Cada capability tem fonte primária, fonte secundária, prioridade, risco e artifact alvo.

| Capability | Fonte primária | Fonte secundária | Prioridade | Risco | Artifact alvo | Por quê |
|---|---|---|---|---|---|---|
| Native editable PPTX | ppt-master | powerpoint-skill | P0 | medium | `services/slides-renderer/native-ir + svg-to-pptx` | Sem isso, a solução não compete em B2B editável. |
| Template replication/import | ppt-master | Presenton/presentation-ai | P0 | medium | `template-registry + pptx-template-importer` | Necessário para decks de marca e clientes. |
| API generation runtime | Presenton | slide-deck-ai | P0 | low | `services/slides-api POST /slides/generate` | Transforma skill em produto operável. |
| MCP tools | Presenton | PPTAgent | P0 | low | `mcp/slides-server` | Permite operação por agentes e automações. |
| Narrative governance | slide creator skill | PPTAgent | P0 | low | `slides-chief/content-architect/qa-inspector` | Diferencial próprio; não substituir. |
| Editability QA | ppt-master | powerpoint-skill | P0 | medium | `qa/editability-report.json` | Provar que PPTX é editável, não só gerado. |
| Provider registry BYOK/Ollama | Presenton | slide-deck-ai/presentation-ai | P0 | low | `services/slides-ai-provider-registry` | Privacidade/custo/enterprise. |
| CLI/headless batch | slide-deck-ai | Presenton | P1 | low | `npm run slides:generate + Python adapter` | Operação recorrente e CI. |
| Reflection/PPTEval | PPTAgent | SINKRA qa-inspector | P1 | medium | `planning-reflection.jsonl + qa-report.json` | Melhora coerência e revisão. |
| Math/diagram pipeline | powerpoint-skill | ppt-master charts | P1 | medium | `math-diagram-engine + OMML injection` | Necessário para decks técnicos e acadêmicos. |
| Editor outline/theme | presentation-ai | Presenton | P1 | medium | `apps/slides-editor outline + theme manager` | Adoção diária e branding. |
| Prompt-to-edit by slide/region | banana-slides | presentation-ai | P1 | high-license | `prompt-edit command layer` | UX importante, mas sem copiar código AGPL. |
| Share runtime | presentation-ai | Presenton | P1 | medium | `web presentation + permissions` | Substitui fluxo de link do Gamma. |
| Analytics deck/slide | PostHog/Umami/Plausible | Gamma benchmark | P2 | low | `deck-publication analytics events` | Gap geral OSS; compor separado. |
| Realtime collaboration | Yjs/Hocuspocus | presentation-ai patterns | P2 | medium | `editor-state CRDT` | Depois de editor/export estabilizados. |
| Video/narration export | PresentAgent-2 | ppt-master/banana-slides | P2 | medium-high | `video-export service` | Alto valor, não bloqueia MVP. |
| Interactive Q&A grounded | PresentAgent-2 | SINKRA evidence ledger | P3 | medium-high | `deck Q&A index + video seek` | Diferencial futuro. |
| Desktop app | Presenton | Electron wrapper | P3 | low | `package after web/runtime stable` | Não priorizar antes de runtime. |
| Markdown/web fallback | Slidev/Marp | slide-deck-ai | P3 | low | `fallback renderer` | Útil para docs/técnico; não substitui PPTX editável. |
| Legal isolation for AGPL/no-license | license-risk-assessment | ADR jurídico | P0 | high | `policy + forbidden copy rules` | Bloqueia absorção direta de banana/sem licença. |

## Regra de Execução

- **P0:** entra antes de qualquer UI sofisticada.
- **P1:** entra depois do renderer/API mínimos.
- **P2:** entra quando o editor e share runtime já existirem.
- **P3:** diferencial futuro ou fallback técnico.

## Sequência Técnica Recomendada

1. Native IR + PPTX editável.
2. API/MCP self-hosted.
3. QA de editabilidade e narrativa.
4. Provider registry BYOK/Ollama.
5. Editor outline/theme.
6. Prompt-to-edit controlado.
7. Share runtime + analytics.
8. Multimodal/video/Q&A.
