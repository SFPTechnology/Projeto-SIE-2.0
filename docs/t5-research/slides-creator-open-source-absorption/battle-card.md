# Battle Card — slide creator skill stack

## Posição

**slide creator skill stack** deve ser uma stack de criação de apresentações com IA para decks consultivos, rastreáveis, editáveis e self-hosted. A tese não é copiar Gamma; é superar Gamma em contextos B2B onde governança, editabilidade e fontes importam.

## Contra Gamma

| Gamma é forte em | Nossa resposta |
|---|---|
| UX rápida e polida | UX prompt-to-edit inspirada em banana-slides/presentation-ai, depois do renderer. |
| Publicação web | Share runtime e analytics em fase P2. |
| Geração visual imediata | Planning/reflection + templates + visual QA para reduzir deck genérico. |
| Experiência produto | API/MCP self-hosted inspirada em Presenton. |

## Vantagens Defensáveis

- Decks com narrativa consultiva, Pyramid/MECE/SCQA e action titles.
- Rastreamento de fontes e QA por gates.
- Execução local/BYOK/Ollama para privacidade.
- PPTX nativo editável como saída de primeira classe.
- API/MCP para squads e automações.
- Absorção modular: não ficamos presos a um único projeto open-source.

## Mensagem de Produto

> Crie apresentações executivas com IA que continuam editáveis no PowerPoint, rastreáveis até as fontes e governadas por um workflow consultivo.

## Objeções e Respostas

| Objeção | Resposta |
|---|---|
| "Gamma já faz slides bonitos." | Sim, mas a lacuna B2B é editabilidade, rastreabilidade, governança e API local-first. |
| "Por que não usar só Presenton?" | Presenton cobre produto/API, mas não substitui nosso núcleo narrativo nem resolve sozinho PPTX nativo editável avançado. |
| "Por que não forkear ppt-master?" | Ele é referência técnica forte, mas o produto precisa de governança SINKRA, API, UX e QA integrados. |
| "banana-slides parece mais avançado visualmente." | É ótimo benchmark de UX, mas AGPL exige cautela e não deve ser base de código sem decisão jurídica. |

## Próxima Jogada

Abrir uma epic de absorção P0 com três frentes:

1. `slides-renderer` nativo editável.
2. `slides-api` com MCP.
3. `planning-reflection` integrado ao workflow existente.
