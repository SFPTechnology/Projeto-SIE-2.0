# Internal Audit — `squads/slides-creator`

## Estado Atual

O nosso `slides-creator` já não é um gerador simples de slides. Ele é um sistema governado:

- `slide-chief` como orquestrador;
- `content-architect`, `template-curator`, `design-renderer`, `visual-scout`, `qa-inspector`;
- workflow `generate-presentation.yaml` v2.0.0;
- narrativa McKinsey/Minto: governing thought, pyramid, SCQA, action titles;
- QA com PPTEval, GAD, WCAG, thumbnails e killer items;
- template registry, token registry, palette registry, visual engines;
- decisão explícita entre PPTX editável e PPTX imagem;
- task `export-editable-pptx.md` com constraints de HTML→PPTX.

## Forças Internas

| Área | Estado | Comentário |
|---|---|---|
| Governança | Forte | SINKRA, gates, task-first, QA, release gate. |
| Narrativa | Forte | Minto, MECE, SCQA, action titles e APA são mais avançados que os projetos externos. |
| QA | Forte | PPTEval/GAD/killer items/refinement loop. |
| Templates | Médio/Forte | Registry e design system existem, mas dependem de runtime consumidor. |
| Visual engines | Médio | D2, Mermaid, Kroki, GPT Image, Recraft, Plotly previstos por feature flag. |
| Export editável | Conceitual/Médio | A disciplina existe, mas não há evidência de renderer local completo equivalente ao `ppt-master`. |
| Runtime app | Fraco | `apps/ds` histórico está ausente; squad opera como handoff/contract-based. |
| UX editor | Fraco | Não há editor Gamma-like ou prompt-to-edit visual. |
| Publicação/analytics | Fraco | Não há camada de share links, views e analytics por deck. |
| Worker scripts | Gap conhecido | `load-kb-bundle` e `validate-fontes-apa` não têm worker determinístico implementado. |

## Gaps Confirmados

1. **Runtime local completo ausente**
   O README e a arquitetura dizem que o runtime histórico `apps/ds` está ausente ou externo. Isso impede experiência end-to-end tipo Gamma.

2. **PPTX editável ainda abaixo de `ppt-master`**
   Temos decisão e constraints, mas `ppt-master` já tem uma pipeline madura SVG→DrawingML com template replication, animações e narração.

3. **Sem editor visual prompt-to-edit**
   Nosso squad produz contrato/render, não uma UI com seleção de região, edição verbal e preview interativo.

4. **Sem produto/API autônomo**
   Presenton tem API/MCP/self-hosting. Nosso squad tem skill/workflow, mas não um serviço de geração consumível por terceiros.

5. **Sem publicação web e analytics**
   Gamma vence em compartilhar, apresentar e medir. Nossa camada ainda é entrega de artefatos.

## Conclusão

Nosso diferencial não está em “gerar o primeiro slide”. Está em **governança, narrativa e qualidade**. Para superar Gamma, precisamos adicionar runtime e renderer, não substituir o squad.

