# Implementation Readiness Gate

Data: 2026-05-17

## Status

Bench: **100/100**.
Produto slide creator skill stack: **planejado, ainda não implementado**.

## Por que separar

O dashboard de bench deve mostrar que a inteligência comparativa está completa. Já o produto só chega a 100 quando os P0/P1 abaixo forem executados em código, com fixtures reais e QA.

## Bloqueadores para Produto 100

| Ordem | Prioridade | Item | Gap |
|---:|---|---|---|
| 1 | P0 | Criar native-slide-ir.schema.json | native_editable_pptx |
| 2 | P0 | Criar renderer PPTX nativo básico | native_editable_pptx |
| 3 | P0 | Criar editability-report.json | native_editable_pptx |
| 4 | P0 | Criar CLI slides:generate | api_mcp_self_hosted |
| 5 | P0 | Criar API POST /slides/generate | api_mcp_self_hosted |
| 6 | P0 | Criar MCP slides.generate/review/export | api_mcp_self_hosted |
| 7 | P0 | Persistir planning-reflection.jsonl | agentic_planning_reflection |
| 8 | P0 | Adaptar rubricas PPTEval | agentic_planning_reflection |
| 9 | P0 | Implementar provider registry | privacy_local_byok |
| 10 | P0 | Criar workspace por deck | api_mcp_self_hosted |
| 11 | P1 | Outline editor mínimo | web_editor_theme_runtime |
| 12 | P1 | Prompt-to-edit com diff | prompt_to_edit_ux |
| 13 | P1 | Theme picker e import de PPTX | web_editor_theme_runtime |
| 14 | P1 | OMML/math support | math_diagrams_academic |
| 15 | P1 | Diagram engines | math_diagrams_academic |
| 16 | P1 | Visual QA screenshots | narrative_governance_qa |
| 17 | P2 | Share links | share_publish_analytics |
| 18 | P2 | Analytics | share_publish_analytics |
| 19 | P2 | Narração/TTS | multimodal_video_narration |
| 20 | P2 | Export MP4 | multimodal_video_narration |
| 21 | P2 | Query→research→deck | source_document_parsing |
| 22 | P2 | Q&A sobre apresentação | multimodal_video_narration |
