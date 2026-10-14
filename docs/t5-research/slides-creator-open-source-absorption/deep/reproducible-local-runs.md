# Deep Dive — Reproducible Local Runs

## Objetivo

Antes de absorver código ou arquitetura, rodar os projetos externos com inputs padronizados e guardar evidência comparável.

## Diretório de Saída

```text
outputs/bench/slides-ai/
  input/
  ppt-master/
  presenton/
  pptagent/
  banana-slides/
  presentation-ai/
  slide-deck-ai/
  powerpoint-skill/
  presentagent-2/
```

## Input Padrão

Criar:

- `input/executive-briefing.md`;
- `input/source-report.md`;
- `input/technical-math.md`;
- `input/brand-template.pptx`;
- `input/evaluation-rubric.yaml`.

## Run Sheet

Para cada projeto:

```text
project:
repo_path:
commit:
date:
setup_command:
run_command:
input:
outputs:
errors:
runtime_minutes:
manual_steps:
notes:
```

## Ordem Recomendada

1. `ppt-master`: validar editabilidade real.
2. Presenton: validar API/MCP e self-host.
3. PPTAgent: validar planning/reflection.
4. powerpoint-skill: validar math/diagramas.
5. presentation-ai: validar UX/editor.
6. banana-slides: rodar isolado por AGPL.
7. slide-deck-ai: baseline simples.
8. PresentAgent-2: apenas se dependências multimodais couberem.

## Métricas Coletadas

| Métrica | Como medir |
|---|---|
| Setup friction | tempo + número de dependências manuais |
| Geração | tempo de prompt até artifact |
| Editabilidade | contagem de objetos nativos |
| Qualidade visual | screenshot/PDF visual QA |
| Narrativa | rubrica SINKRA |
| Fontes | claims com referência |
| Custo | chamadas externas necessárias |

## Gate de Absorção

Não transformar um projeto em referência P0 sem pelo menos um run local registrado. O bench atual justifica prioridade; a implementação deve exigir evidência executável antes de copiar/adaptar arquitetura.
