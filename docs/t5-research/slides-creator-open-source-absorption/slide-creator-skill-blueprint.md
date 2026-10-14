# Slide Creator Skill Blueprint — Bench-Derived Absorption Map

Data: 2026-05-17  
Status: canônico para transformar o benchmark em uma skill autocontida compartilhável  
Fonte: `docs/bench/slides-creator-open-source-absorption/` + `docs/bench/presenton-vs-gamma/`

## Tese

A `slide-creator` não deve tentar “pensar do zero” toda vez que cria uma apresentação. Ela precisa operar como uma composição de padrões já provados no benchmark:

```text
Narrativa SINKRA
  + planning/reflection de PPTAgent
  + runtime/API/self-hosting de Presenton
  + PPTX editável de ppt-master
  + rigor técnico de powerpoint-skill
  + outline/theme/editor de presentation-ai
  + prompt-to-edit de banana-slides
  + pesquisa/multimodal de PresentAgent-2
  + UX/distribuição esperada de Gamma
```

O output correto do bench para a skill é uma biblioteca de decisões: **quando usar qual padrão, qual artifact emitir e o que não copiar**.

## 1. Mapa De Absorção Por Projeto

| Projeto | Absorver | Quando usar | Artifact obrigatório | Não copiar |
|---|---|---|---|---|
| slide creator skill | narrativa consultiva, briefing, Pyramid/SCQA, action titles, QA governado | qualquer deck estratégico, comercial ou executivo | `story-arc.yaml`, `slide-function-map.yaml`, `qa-report.yaml` | acoplamento a paths privados quando a skill for compartilhável |
| Presenton | self-hosting, API, MCP, providers BYOK/Ollama, workspace por deck | produto interno, runtime local, automação por agentes | `provider-registry.yaml`, `workspace/`, `api-mcp-contract.yaml` | UI completa antes do core headless |
| Gamma | UX de baixa fricção, importação, edição, share, analytics, distribuição | experiência de usuário e expectativa comercial | `publication-plan.yaml`, `import-sources.yaml`, `analytics-event-map.yaml` | lock-in SaaS, crédito, dependência de plataforma fechada |
| ppt-master | PPTX nativo editável, template import, Native IR, editability QA | entrega B2B em PowerPoint, templates corporativos | `native-slide-ir.yaml`, `editability-report.yaml`, `template-import-report.yaml` | LLM gerando PPTX direto ou SVG livre sem schema |
| PPTAgent | planner, reflection, critique, revision, PPTEval-like QA | melhorar deck ruim, aumentar qualidade antes do render | `planning-reflection.jsonl`, `critique-report.yaml`, `revision-notes.md` | framework pesado inteiro sem adaptação |
| presentation-ai | outline-first, theme picker, editor/present/share, modelos locais | criação diária por usuário não técnico | `outline-review.yaml`, `theme-selection.yaml`, `editor-state.yaml` | editor visual sem DeckSpec versionável |
| banana-slides | prompt-to-edit por slide/bloco/região, preview, diff, style reference | ajustes iterativos por linguagem natural | `edit-operation.yaml`, `diff-preview.yaml` | código AGPL ou estrutura derivada sem revisão jurídica |
| powerpoint-skill | OMML, Mermaid/Graphviz/TikZ, QA técnico, fallback por renderer | decks técnicos, acadêmicos, financeiros, engenharia | `diagram-source.*`, `technical-qa.yaml`, `math-render-report.yaml` | fórmula/diagrama rasterizado quando editabilidade é requisito |
| slide-deck-ai | CLI simples, provider abstraction, Ollama/offline smoke test | baseline local rápido e CI | `cli-run-report.yaml`, `provider-selection.yaml` | renderer final ou qualidade visual como core |
| PresentAgent-2 | query→research→source→deck, multimodal, Q&A futuro | deck nasce de pergunta aberta ou precisa de pesquisa | `source-ledger.yaml`, `refined-doc.md`, `research-plan.yaml` | vídeo/Q&A como requisito de MVP |

## 2. Fluxo Canônico Da Skill

```text
P00 Intake
  -> P01 Source/Research Plan
  -> P02 Belief Shift
  -> P03 Roteiro Template Selection
  -> P04 Story Arc
  -> P05 Slide Function Map
  -> P06 Slide Structure Selection
  -> P07 Design Direction
  -> P08 DeckSpec
  -> P09 Critique + Reflection
  -> P10 Revision
  -> P11 QA
  -> P12 Export/Runtime Plan
```

Diferença em relação à versão fraca: **a skill escolhe padrões antes de escrever slides**.

## 3. Decision Tree De Capacidades

| Se o usuário pedir... | A skill deve ativar... | Fonte benchmark | Saída mínima |
|---|---|---|---|
| “Crie uma apresentação” | narrativa + roteiro + estruturas | SINKRA + PPTAgent | `story-arc`, `slide-function-map`, `deck-spec` |
| “Webinar” | roteiro de webinar + oferta/CTA + demo | SINKRA + Gamma | `roteiro-template-selection`, `cta-map` |
| “Apresentação financeira” | templates financeiros + charts/tabelas + editabilidade | ppt-master + powerpoint-skill | `financial-slide-plan`, `editability-report` |
| “Board/investidor” | executive answer + decisão + riscos | SINKRA + ppt-master | `decision-ask`, `risk-map` |
| “PPTX editável” | Native IR + editability QA | ppt-master | `native-slide-ir`, `editability-report` |
| “API/MCP/local” | runtime self-hosted + providers | Presenton | `api-mcp-contract`, `provider-registry` |
| “Edite esse slide” | prompt-to-edit com diff | banana-slides + presentation-ai | `edit-operation`, `diff-preview` |
| “Use meu template” | template import/replication | ppt-master + Presenton | `template-import-report` |
| “Pesquise e gere” | research grounding antes de slides | PresentAgent-2 + PPTAgent | `source-ledger`, `refined-doc` |
| “Técnico/acadêmico” | OMML/diagram engines/technical QA | powerpoint-skill | `diagram-source`, `technical-qa` |
| “Compartilhar por link” | publicação + permissões + analytics | Gamma + presentation-ai | `publication-plan`, `analytics-event-map` |

## 4. Bibliotecas Que A Skill Precisa Ter

| Biblioteca | Origem | Status esperado |
|---|---|---|
| Roteiros por tipo de deck | Gamma UX + SINKRA narrative + use cases do bench | 20+ roteiros |
| Estruturas de slide | ppt-master/presentation-ai/Gamma mental model + design heuristics | 80+ estruturas com use/avoid |
| Contratos de runtime | Presenton + contracts do bench | API/MCP/provider/workspace |
| Native IR | ppt-master + `contracts/native-ir-contract.md` | schema para PPTX editável |
| Reflection/critique | PPTAgent + `deep/agentic-planning-reflection.md` | JSONL + critique report |
| Prompt-to-edit | banana-slides + editor UX deep dive | operação por região com diff |
| Technical slide rules | powerpoint-skill | math/diagram QA |
| Research grounding | PresentAgent-2 | source ledger + refined doc |
| QA rubric | bench contracts + mission narrative/design | narrativa, design, prova, técnica, editabilidade |

## 5. Artifact Contract Consolidado

```text
outputs/slide-creator/{deck_id}/
  inputs/
  briefing-normalized.yaml
  source-ledger.yaml
  research-plan.yaml
  audience-belief-shift.yaml
  roteiro-template-selection.yaml
  story-arc.yaml
  slide-function-map.yaml
  slide-structure-selection.yaml
  design-direction.yaml
  bench-capability-selection.yaml
  deck-spec.yaml
  native-slide-ir.yaml
  planning-reflection.jsonl
  critique-report.yaml
  revision-notes.md
  qa-report.yaml
  editability-report.yaml
  publication-plan.yaml
  exports/
```

Regra: nem todo deck precisa de todos os artifacts, mas a skill deve saber **por que um artifact não foi necessário**.

## 6. Critérios De Uma Skill Incrível

| Critério | Bar mínimo |
|---|---|
| Escolha de roteiro | todo deck escolhe template primário e justifica |
| Escolha de estrutura | todo slide declara `structure_id` e por que serve à função |
| Narrativa | title-only vertical test passa antes do design |
| Design | design direction antes do DeckSpec |
| Reflexão | pelo menos 1 critique/revision pass antes da entrega final |
| Bench reuse | pedido conhecido ativa fonte benchmark correta |
| Editabilidade | se PPTX solicitado, `editability-report` é obrigatório |
| Fontes | claim crítico sem fonte vira `validate` ou `assumption` |
| Prompt-to-edit | alteração gera diff e QA direcionado |
| Share/analytics | só entram quando o usuário pede distribuição, não como ruído |

## 7. Scorecard Da Skill

| Dimensão | Peso | O que mede |
|---|---:|---|
| Narrativa e tese | 20 | crença, arco, tensão, ação |
| Roteiro/template fit | 15 | deck type correto, módulos certos |
| Estrutura slide-a-slide | 15 | função + structure_id + layout adequado |
| Design editorial | 15 | hierarquia, densidade, variedade, motivo visual |
| Prova e fontes | 10 | evidência, source ledger, assumptions |
| Reflection/QA | 10 | critique/revision/routing |
| Export/runtime | 10 | PPTX/API/MCP/local quando solicitado |
| Segurança/licença | 5 | evita cópia AGPL/risco e explicita limites |

Release interno da skill: score >= 90 e sem killer items.

## 8. Killer Items

Bloqueia output final:

- deck nasce de outline direto sem `slide-function-map`;
- slide sem função ou sem estrutura selecionada;
- roteiro não escolhido;
- PPTX solicitado sem plano de Native IR/editability QA;
- prompt-to-edit sem diff;
- claim crítico sem fonte/assumption;
- benchmark pattern ignorado para capability conhecida;
- cópia direta de padrão/código AGPL sem alerta;
- deck final com card wall ou brand skinning superficial.

## 9. Como Isso Entra Na Skill

Arquivos esperados dentro de `slide-creator`:

```text
SKILL.md
references/
  narrative-patterns.md
  roteiro-template-library.md
  slide-structure-library.md
  bench-absorption-map.md
  design-system.md
  output-contracts.md
  rubrics.md
  anti-patterns.md
agents/openai.yaml
```

O `SKILL.md` deve permanecer curto e carregar referências sob demanda. O peso cognitivo fica nas bibliotecas.

## 10. Decisão

O bench não termina no ranking. O bench termina quando vira uma skill com repertório operacional. Este blueprint é a ponte: compara, escolhe, transforma em contratos e define os gates que impedem a skill de voltar a gerar slides pobres.
