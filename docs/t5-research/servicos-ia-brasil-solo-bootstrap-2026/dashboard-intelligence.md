# Dashboard Intelligence — Serviços IA Brasil Solo Bootstrap 2026

## Veredicto

O bench agora está estruturado para o Observatório: `bench-output-dash.json` expõe players, score matrix, duelos, cenários, riscos, evidências, cliffs e árvore de decisão.

## Leitura correta

| Camada | Sinal | Decisão |
|---|---|---|
| Mapa | Mentoria lidera com 87,8 | Negócio principal se houver autoridade |
| Duelo | Mentoria vence Automação em moat; Automação vence em MRR | Usar automação como cross-sell, não substituto |
| Matriz | WhatsApp vence TTFR | Usar como caixa tático/validação rápida |
| Roadmap | Discovery Pago e mini-curso são gates | Não executar projeto sem pré-venda |
| Risco | Enterprise bait é o maior desvio | Vetar LGPD/Cyber/Preditivo no MVP solo |

## O que mudou nesta versão

- Adicionado `bench-output-dash.json` com schema compatível com o app Research.
- Scorecard convertido para formato dimension-first, preservando scores originais.
- Cenários por persona de decisão: caixa 30d, negócio premium 90d, moat ano 2.
- Evidências e riscos separados em arquivos próprios.
- Readiness gate para transformar o bench em execução de 13 semanas.
