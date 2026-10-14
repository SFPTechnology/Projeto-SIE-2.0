# Intelligence Graph — Slides Creator Open-Source Absorption

Data: 2026-05-18

## Tese

slide creator skill stack deve ser uma composição, não um fork: narrativa governada do squad, renderer ppt-master, runtime Presenton, QA PPTAgent/powerpoint-skill e UX aprendida de presentation-ai/banana-slides.

## Como os Arquivos Conversam

| Loop | Para que serve | Artefatos |
|---|---|---|
| Persona → Dimensão → Player | Explica por que o vencedor muda por cenário. | `scenario-scorecards.md`, `deep/persona-weight-methodology.md`, `comparison-matrix.md` |
| Gap → Fonte → Contrato | Transforma benchmark em backlog implementável. | `TODO-coverage.md`, `deep/absorption-decision-table.md`, `contracts/native-ir-contract.md`, `contracts/api-contract.md`, `contracts/mcp-contract.md` |
| Segmento → Stack composta → Roadmap | Evita comparar app, skill e engine na mesma régua. | `segmented-comparisons.md`, `deep/segmented-methodology.md`, `absorption-roadmap.md` |
| Risco → Licença → Decisão de absorção | Separa benchmark comportamental de código copiável. | `risk-register.md`, `deep/license-risk-assessment.md`, `ADR-001-absorption-strategy.md` |

## Sinais Principais

- Score canônico do bench: 100.
- Matriz atual: 9 players × 108 microdimensões = 972 células.
- Top neutro micro: slide creator skill 77.93; ppt-master 74.79; Presenton 74.09.
- Mapa de gaps micro: 72 gaps positivos contra líder, 36 vantagens/empates da slide creator skill, 38 gaps P1 por delta >=20.
- Vencedores por persona: Presenton (4); presentation-ai (3); ppt-master (2); powerpoint-skill (1); banana-slides (1); PresentAgent-2 (1).
- Gaps P0 atuais: Renderização nativa, Editor runtime, Infra local/desktop e Multimídia executável.

## Regra de Inteligência

A leitura correta não é “qual projeto vence?”. A leitura correta é: qual capability precisamos absorver, de qual fonte, com qual risco, para qual persona e em qual ordem de implementação. O score 100 fecha a inteligência do benchmark; a execução técnica segue em implementation-readiness-gate.
