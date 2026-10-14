# Gap analysis

| ID | Player | Prioridade | Complexidade | Gap | Racional |
| --- | --- | --- | --- | --- | --- |
| GAP-GAMMA-01 | gamma | P1 | MEDIUM | PPTX exportável não significa PPTX limpo para cliente | Gamma é excelente para publicação web/PDF, mas apresentações complexas podem exigir reconstrução ao entrar em PowerPoint. |
| GAP-CANVA-01 | canva | P2 | MEDIUM | Geração narrativa por prompt abaixo dos líderes AI-native | Canva vence como suíte de design, mas a geração de narrativa deck-first ainda não é tão boa quanto Gamma/Plus. |
| GAP-PLUS-01 | plus_ai | P2 | LOW | Menos impacto visual no primeiro draft | Plus AI prioriza editabilidade e integração nativa; decks podem precisar de designer/template forte para wow visual. |
| GAP-PITCH-01 | pitch | P2 | LOW | AI não é o motor central da experiência | Pitch é excepcional para colaboração, mas menos agressivo em geração completa por prompt. |
| GAP-BEAUTIFUL-01 | beautiful_ai | P1 | LOW | Custo e rigidez para pequenos times | Sem free permanente e com Team caro, o TCO sobe rápido para squads de growth. |
| GAP-PRESENTON-01 | presenton | P1 | HIGH | Maturidade operacional menor | Open source e controle são fortes, mas adoção, UI e suporte dependem de setup interno ou cloud emergente. |
| GAP-TOME-01 | tome | P0 | HIGH | Risco de continuidade para novos decks | Fontes indicam pivot/sunset do produto original de apresentações; além disso, help oficial aponta PDF sem PPT. |
| GAP-SLIDESAI-01 | slidesai | P2 | MEDIUM | Qualidade visual limitada para high-stakes | Útil para produtividade dentro do Google Slides, mas fraco para decks premium de venda/fundraising. |
| GAP-DECKTOPUS-01 | decktopus | P2 | LOW | Transparência inferior em PPTX e limites por crédito | Pricing publica PDF export e créditos anuais, mas PPTX/fidelidade não aparecem como diferencial claro. |
| GAP-PRESENTATIONS-01 | presentations_ai | P2 | MEDIUM | Evidência pública insuficiente para recomendação principal | A proposta é relevante, mas a coleta encontrou menos fontes oficiais operacionais que nos líderes. |

## Trade-offs

- Gamma maximiza velocidade e estética inicial, mas o custo aparece quando PPTX fiel é obrigatório.
- Canva maximiza valor de suíte e colaboração de marketing, mas não é o gerador narrativo mais forte.
- Plus AI sacrifica um pouco de wow visual para ganhar em editabilidade nativa e fluxo corporativo.
- Presenton troca maturidade de SaaS por controle, API, self-host e baixo lock-in.
- Tome deve ser tratado como legado/risco, não como escolha principal para novas operações.

## Cliffs

| Player | Trigger | Impacto |
| --- | --- | --- |
| gamma | Cliente exige PPTX totalmente editável e fiel | Retrabalho provável em PowerPoint/Slides. |
| canva | Deck narrativo complexo gerado só por prompt | Exige direção humana e edição manual. |
| beautiful_ai | Time pequeno precisa de muitos assentos | TCO cresce rápido no Team. |
| tome | Novo workflow de apresentações em 2026 | Risco de produto/pivot torna adoção não recomendada. |
| presenton | Time sem engenharia/ops | Self-host/API vira custo operacional. |
| slidesai | Deck premium para venda/fundraising | Qualidade visual pode ficar abaixo do necessário. |
