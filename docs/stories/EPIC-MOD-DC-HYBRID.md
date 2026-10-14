# EPIC: MOD-DC Hybrid - Parametros por Circuito

**Data criacao:** 2026-07-15  
**Ultima atualizacao:** 2026-07-18  
**Owner:** Morgan (PM)  
**Status:** Stories 2, 3 e 4 implementadas; QA pendente  
**Prioridade:** Alta  
**Estimativa restante:** 1-2 dias uteis de QA e ajustes finais

---

## Visao Geral

Este epic fecha a lacuna entre o dimensionamento global atual e a necessidade de testar parametros normativos independentes por circuito com trilha de rastreabilidade.

O plano original foi ajustado em 2026-07-17 para refletir o estado real da implementacao:

- a fundacao backend ja existe;
- a proxima entrega precisa ser operacional e persistente;
- a UI so entra depois disso, em conformidade com `CLI First`.

---

## Objetivo Estrategico

Entregar customizacao por circuito sem quebrar o fluxo atual do dimensionador, preservando:

- padrao global como caminho principal;
- excecao por circuito como fluxo controlado;
- rastreabilidade do calculo utilizado em cada resultado;
- conformidade documental no relatorio final.

---

## Stories do Epic

### MOD-DC-HYBRID-1 - Backend Foundation

**Arquivo:** `story-MOD-DC-HYBRID-1-backend.md`  
**Status:** `InReview`

Entregou a base tecnica de overrides:

- contrato `CircuitoOverride`;
- merge `GLOBAL` x `CUSTOMIZADO`;
- resultado com `baseadoEm` e `parametrosUsados`;
- integracao inicial em servicos e schemas.

### MOD-DC-HYBRID-2 - Backend Operations

**Arquivo:** `story-MOD-DC-HYBRID-2-backend-operacoes.md`  
**Status:** `InReview`  
**Owner:** `@dev`

Objetivo: tornar os overrides persistentes e operacionais.

### MOD-DC-HYBRID-3 - UI + UX de Customizacao

**Arquivo:** `story-MOD-DC-HYBRID-3-ui-ux.md`  
**Status:** `InReview`  
**Owner:** `@dev`

Objetivo: expor a customizacao por circuito na tela com validacoes e feedback.

### MOD-DC-HYBRID-4 - Auditoria e Exportacao

**Arquivo:** `story-MOD-DC-HYBRID-4-auditoria.md`  
**Status:** `InReview`  
**Owner:** `@dev`

Objetivo: fechar historico, relatorio e compliance.

---

## Ordem de Execucao

1. QA consolidado em `MOD-DC-HYBRID-2`.
2. QA consolidado em `MOD-DC-HYBRID-3`.
3. QA consolidado em `MOD-DC-HYBRID-4`.
4. Fechamento do epic apos validacao final.

---

## Criterios de Sucesso

| Metrica                                                     | Target                             |
| ----------------------------------------------------------- | ---------------------------------- |
| Recalculo por circuito usa os parametros corretos           | 100% dos casos cobertos por testes |
| Overrides persistem e reaparecem ao reabrir o projeto       | 100%                               |
| Usuario consegue customizar 1 circuito sem afetar os demais | 100%                               |
| Relatorio identifica `GLOBAL` x `CUSTOMIZADO`               | 100%                               |
| Justificativas e desvios ficam auditaveis                   | 100%                               |

---

## Riscos e Tratamento

| Risco                                                         | Impacto                 | Tratamento                                     |
| ------------------------------------------------------------- | ----------------------- | ---------------------------------------------- |
| Persistencia ser modelada fora dos contratos ja implementados | retrabalho              | usar `CircuitoOverride` como contrato canonico |
| AUTO-OTI recalcular sem respeitar override ativo              | erro de engenharia      | cobrir explicitamente na story 2               |
| UI mascarar estado nao persistido                             | inconsistencias         | UI so apos backend operacional                 |
| Relatorio exportado divergir do calculo real                  | compliance comprometido | derivar exportacao de `parametrosUsados`       |

---

## Artefatos Relacionados

- `docs/roadmap/ROADMAP-dimensionador-hybrid.md`
- `docs/stories/story-MOD-DC-HYBRID-1-backend.md`
- `docs/stories/story-MOD-DC-HYBRID-2-backend-operacoes.md`
- `docs/stories/story-MOD-DC-HYBRID-3-ui-ux.md`
- `docs/stories/story-MOD-DC-HYBRID-4-auditoria.md`

---

## Decisao de Produto

O modo YOLO foi usado para executar as fases remanescentes sem checkpoints intermediarios. Isso nao substitui QA nem autoridade de release. O estado atual do epic e de implementacao concluida, aguardando validacao final.

---

**Atualizado por:** Morgan (PM)
