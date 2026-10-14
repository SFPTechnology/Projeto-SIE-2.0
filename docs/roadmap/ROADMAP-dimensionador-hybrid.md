# Roadmap: Implementacao Dimensionador Hybrid por Circuito

**Data:** 2026-07-18  
**Origem:** consolidacao Atlas + Morgan + execucao inicial do MOD-DC-HYBRID-1  
**Status:** Replanejado para execucao  
**Prioridade:** Alta

---

## Visao Geral

O objetivo continua o mesmo: permitir que o dimensionamento use parametros normativos globais por padrao, mas aceite excecoes controladas por circuito com rastreabilidade completa.

A mudanca neste roadmap e de sequenciamento. O plano original colocava UI antes da camada operacional persistente. Isso conflita com a Constitution do projeto (`CLI First -> Observability -> UI`). Em 2026-07-17 o roadmap foi reordenado para que o backend fique operacional antes da interface.

---

## Estado Atual

### Ja implementado

- Foundation de dominio e API para `circuitoOverrides`
- Merge deterministico `GLOBAL` x `CUSTOMIZADO`
- Resultado com `baseadoEm`, `parametrosUsados` e `justificativaOverride`
- Integracao inicial nos servicos e schemas existentes
- Testes de dominio/API cobrindo a base da feature

### Ainda pendente para a funcionalidade completa

- QA integrada do epic
- Ajustes residuais apontados pela validacao final

---

## Fases Replanejadas

### Phase 1: Backend Foundation

**Status:** Implementado e em `InReview`  
**Story:** `story-MOD-DC-HYBRID-1-backend.md`

Entregou a base tecnica da feature, mas nao fecha o ciclo de uso sozinho.

### Phase 2: Backend Operations

**Status:** Pronto para desenvolvimento  
**Story:** `story-MOD-DC-HYBRID-2-backend-operacoes.md`

**Objetivo:** tornar o override utilizavel sem depender da UI.

**Escopo:**

- Persistir override por projeto/circuito
- Carregar overrides junto do dimensionamento
- Salvar, remover e recalcular circuito individual
- Expor operacoes necessarias para cliente interno e fluxos CLI/API
- Garantir compatibilidade com AUTO-OTI e lote global

**Esforco estimado:** 2-3 dias

### Phase 3: UI + UX de Customizacao

**Status:** Implementado e em `InReview`  
**Story:** `story-MOD-DC-HYBRID-3-ui-ux.md`

**Objetivo:** expor a customizacao por circuito na tela de dimensionamento.

**Escopo:**

- Toggle por circuito
- Badge `GLOBAL` x `CUSTOMIZADO`
- Modal/drawer de edicao
- Validacao de justificativa e diff vs global
- Recalculo individual e reset para global

**Esforco estimado:** 2-3 dias

### Phase 4: Auditoria e Exportacao

**Status:** Implementado e em `InReview`  
**Story:** `story-MOD-DC-HYBRID-4-auditoria.md`

**Objetivo:** fechar rastreabilidade e compliance da funcionalidade.

**Escopo:**

- Historico consultavel por circuito
- Sumario de desvios no relatorio
- Exportacao PDF/Excel com `Fonte de Calculo`
- Secao de conformidade NBR5410

**Esforco estimado:** 1-2 dias

---

## Sequencia de Execucao

1. Finalizar QA da `MOD-DC-HYBRID-2`.
2. Finalizar QA da `MOD-DC-HYBRID-3`.
3. Finalizar QA da `MOD-DC-HYBRID-4`.
4. Consolidar release candidate do epic.

---

## Marcos

| Marco | Story           | Resultado esperado                          |
| ----- | --------------- | ------------------------------------------- |
| M1    | MOD-DC-HYBRID-1 | Base de override pronta                     |
| M2    | MOD-DC-HYBRID-2 | Override persistido e recalculo operacional |
| M3    | MOD-DC-HYBRID-3 | Customizacao por circuito disponivel na UI  |
| M4    | MOD-DC-HYBRID-4 | Auditoria e relatorios conformes            |

**MVP funcional:** fim da `MOD-DC-HYBRID-3`  
**Release candidate:** fim da `MOD-DC-HYBRID-4`

---

## Riscos Principais

| Risco                                      | Impacto                             | Mitigacao                                              |
| ------------------------------------------ | ----------------------------------- | ------------------------------------------------------ |
| UI ser iniciada antes da persistencia      | retrabalho e estados inconsistentes | manter `CLI First` e bloquear UI antes da Phase 2      |
| Override salvo sem justificativa confiavel | nao conformidade                    | validar no backend e refletir na UI                    |
| AUTO-OTI ignorar override ativo            | resultado incorreto por circuito    | incluir cobertura especifica na Phase 2                |
| Exportacao nao refletir `baseadoEm` real   | auditoria invalida                  | usar `parametrosUsados` como fonte canonica na Phase 4 |

---

## Proximos Passos

1. Encaminhar `MOD-DC-HYBRID-3` e `MOD-DC-HYBRID-4` para QA.
2. Consolidar feedback e ajustes finais.
3. Preparar release candidate do epic.

---

**Atualizado por:** Morgan (PM)  
**Data:** 2026-07-18
