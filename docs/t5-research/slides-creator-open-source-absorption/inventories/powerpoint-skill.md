# Inventory — powerpoint-skill

## Identidade

- **Repo:** `Noi1r/powerpoint-skill`
- **Clone local:** `../bench/powerpoint-skill`
- **Licença:** MIT
- **Prioridade:** P1
- **Papel na stack:** regras técnicas, matemática nativa, diagramas e QA visual.

## Evidência Lida

- `../bench/powerpoint-skill/README.md`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| OMML math | Fórmulas nativas do PowerPoint via pandoc/injeção. |
| Diagramas | Pipeline Graphviz, Mermaid, TikZ e shapes PptxGenJS. |
| Hard rules | Skill pequena com regras claras de geração. |
| Temas | Temas e padrões de layout para slides técnicos. |
| QA visual | Reconhece limitações de LibreOffice vs PowerPoint para OMML. |

## Limitações

- Não é produto.
- Não tem editor/app/API.
- O foco é técnico/acadêmico, não UX geral.

## O Que Absorver

1. OMML para fórmulas editáveis.
2. Mermaid/Graphviz/TikZ como engines de diagrama.
3. Regras de fallback quando renderer não suporta elemento nativo.
4. Checklist de QA visual para slides técnicos.

## Critério de Aceite

- Fórmulas principais editáveis no PowerPoint.
- Diagramas renderizam de forma determinística.
- QA distingue limitação de LibreOffice de falha real no PowerPoint.
