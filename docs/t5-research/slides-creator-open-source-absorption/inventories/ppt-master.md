# Inventory — ppt-master

## Identidade

- **Repo:** `hugohe3/ppt-master`
- **Clone local:** `../bench/ppt-master`
- **Licença:** MIT
- **Prioridade:** P0
- **Papel na stack:** renderer nativo editável, template replication, live preview, animações e narração.

## Evidência Lida

- `../bench/ppt-master/README.md`
- `../bench/ppt-master/docs/templates-guide.md`
- `../bench/ppt-master/docs/audio-narration.md`
- `../bench/ppt-master/skills/ppt-master/workflows/live-preview.md`
- `../bench/ppt-master/skills/ppt-master/references/animations.md`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| PPTX nativo editável | O README posiciona o projeto contra decks image-based: shapes, textos e charts viram objetos editáveis. |
| Input multimodal de documentos | PDF, DOCX, URL e Markdown como entradas. |
| Template replication | Extrai cores, fontes, masters/layouts, imagens e relações de sprite do OOXML. |
| Live preview | Preview local em browser com anotações aplicáveis ao SVG antes do re-export. |
| Animações/transições | Exporta OOXML real, não vídeo embutido. |
| Narração/vídeo | Gera narração por slide e permite export MP4 via PowerPoint. |

## Limitações

- É mais um workflow/skill do que um produto multiusuário.
- Depende de disciplina de geração SVG por LLM.
- Precisa ser adaptado para contratos SINKRA (`DeckSpec`, `SlideSpec`, QA gates).
- Não resolve sozinho API, editor web, governança ou analytics.

## O Que Absorver

1. **IR visual restrito:** usar SVG/estrutura visual como representação intermediária antes de PPTX.
2. **Conversão para objetos nativos:** transformar caixas, textos, imagens, charts e formas em DrawingML.
3. **Validação de editabilidade:** abrir/exportar e verificar objetos reais, não screenshots.
4. **Template replication:** importar `.pptx` corporativo como template privado.
5. **Live preview com annotations:** útil para UX P1, não para MVP inicial.

## O Que Não Copiar Diretamente

- Fluxo de skill chat-first como arquitetura final.
- Assumir SVG livre sem restrições; SINKRA precisa de schema controlado.
- Vídeo/animações no P0.

## Integração SINKRA Recomendada

```text
deck-spec.yaml
  -> slide-specs/*.yaml
  -> visual-ir/*.svg ou visual-ir/*.json
  -> native-pptx-renderer
  -> editability-report.json
  -> qa-report.json
```

## Critério de Aceite

- PPTX abre em PowerPoint/Keynote/LibreOffice.
- Títulos, textos, shapes e principais visuais são selecionáveis.
- O relatório informa porcentagem de elementos nativos vs rasterizados.
- Export PDF visual confere com screenshot de referência.
