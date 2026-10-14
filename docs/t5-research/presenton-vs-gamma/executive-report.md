# Executive Report — Presenton vs Gamma

## Resumo Executivo

Gamma vence como produto final: mais polido, mais simples para usuário não técnico, melhor para compartilhar, apresentar e operar como SaaS. Presenton vence como alternativa estratégica: open-source, self-hostable, local-first, BYOK, com Ollama, API e templates controláveis.

O score ponderado por produto fica:

- Gamma: 88.3/100
- Presenton: 82.0/100

Esse delta não significa que Gamma é sempre a escolha certa. Significa que Gamma é melhor quando a métrica principal é experiência pronta. Presenton é melhor quando a métrica principal é soberania operacional.

## Fontes e Evidências

Presenton:

- O GitHub descreve Docker/self-hosting, desktop app, providers OpenAI/Gemini/Anthropic/Ollama, API, Apache-2.0, templates e exportação PPTX/PDF: https://github.com/presenton/presenton
- A documentação descreve uso open-source, self-hosting, modelos locais/Ollama e exportação PPTX/PDF: https://docs.presenton.ai/index

Gamma:

- Produto de apresentações com criação, apresentação, compartilhamento e exportação: https://gamma.app/products/presentations
- Exporta PDF, PNG e PowerPoint/PPTX segundo help center: https://help.gamma.app/fr/articles/8022861
- Importa slides/docs de múltiplas origens segundo help center: https://help.gamma.app/en/articles/11047840-how-can-i-import-slides-or-documents-into-gamma
- Pricing oficial mostra Free/Plus/Pro/Ultra e capacidades por plano: https://gamma.app/es/pricing
- API e MCP documentados, com API keys em Pro/Ultra/Teams/Business: https://developers.gamma.app/
- Integrações oficiais incluem ChatGPT, Claude, Zapier, Make, n8n e Gamma API: https://gamma.app/integrations

## Decisão por Cenário

| Cenário | Escolha | Motivo |
|---|---|---|
| Founder quer deck bonito em 10 min | Gamma | Menor fricção e melhor UX. |
| Agência/consultoria precisa entregar via link | Gamma | Sharing, presentation mode, analytics e distribuição SaaS. |
| Empresa com dados sensíveis | Presenton | Self-hosting/local-first. |
| Pipeline automatizado interno | Presenton | API controlada e sem depender de SaaS externo. |
| Produto próprio de geração de decks | Ambos | Gamma como referência de UX; Presenton como referência técnica open-source. |
| Custo marginal em escala | Presenton | Custos ficam em infra/modelos escolhidos pelo usuário. |

## Recomendação SINKRA

Use **Gamma como benchmark de UX** e **Presenton como candidato de stack soberana**.

Não tente “substituir Gamma por Presenton” sem medir exportação e qualidade visual. O teste certo é:

1. mesmo briefing;
2. mesmo número de slides;
3. mesmo idioma PT-BR;
4. mesmo material de entrada;
5. export PPTX/PDF;
6. nota por narrativa, visual, editabilidade, fidelidade factual e tempo até entrega.

## Próximo Passo

Criar uma story curta de benchmark local com três casos:

- prompt puro;
- documento longo;
- deck com branding SINKRA.

Critério de aceite: outputs exportados, screenshots, pontuação e decisão final.

