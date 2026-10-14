# Handoff: MOD-DC Hybrid para Desenvolvimento

**De:** Morgan (PM)  
**Para:** @dev  
**Data:** 2026-07-17  
**Status:** Pacote replanejado e pronto para execucao

---

## Resumo Executivo

O backlog original desta frente foi reordenado para refletir o estado real do codigo e a regra `CLI First`.

**Veredito operacional:**

- `MOD-DC-HYBRID-1` ja entregou a fundacao tecnica e esta em `InReview`.
- O proximo passo correto nao e UI.
- O `@dev` deve iniciar por `MOD-DC-HYBRID-2`, focando persistencia, operacoes e recalculo por circuito.

---

## O que Ja Existe no Codigo

Base pronta para continuidade:

- `CircuitoOverride` e contratos relacionados
- merge `GLOBAL` x `CUSTOMIZADO`
- resultado com `baseadoEm`, `parametrosUsados` e `justificativaOverride`
- servicos e schemas aceitando `circuitoOverrides`

Referencias tecnicas centrais:

- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/dimensionamento-condutores.ts`

---

## Sequencia Obrigatoria

1. Fechar ou absorver a base de `MOD-DC-HYBRID-1`.
2. Implementar `MOD-DC-HYBRID-2-backend-operacoes.md`.
3. So depois iniciar `MOD-DC-HYBRID-3-ui-ux.md`.
4. Encerrar a frente com `MOD-DC-HYBRID-4-auditoria.md`.

Motivo: iniciar UI antes da persistencia criaria estado transitivo e retrabalho.

---

## Stories Prontas

- [story-MOD-DC-HYBRID-2-backend-operacoes.md](/C:/Users/User/Documents/2026/Projects_Smart_Systems/Projeto_SIE/docs/stories/story-MOD-DC-HYBRID-2-backend-operacoes.md)
- [story-MOD-DC-HYBRID-3-ui-ux.md](/C:/Users/User/Documents/2026/Projects_Smart_Systems/Projeto_SIE/docs/stories/story-MOD-DC-HYBRID-3-ui-ux.md)
- [story-MOD-DC-HYBRID-4-auditoria.md](/C:/Users/User/Documents/2026/Projects_Smart_Systems/Projeto_SIE/docs/stories/story-MOD-DC-HYBRID-4-auditoria.md)

Artefatos de apoio:

- [EPIC-MOD-DC-HYBRID.md](/C:/Users/User/Documents/2026/Projects_Smart_Systems/Projeto_SIE/docs/stories/EPIC-MOD-DC-HYBRID.md)
- [ROADMAP-dimensionador-hybrid.md](/C:/Users/User/Documents/2026/Projects_Smart_Systems/Projeto_SIE/docs/roadmap/ROADMAP-dimensionador-hybrid.md)

---

## PM Readiness Review

Checklist de prontidao aplicada nesta rodada:

- [x] Escopo restante separado do que ja foi implementado
- [x] Sequencia alinhada com `CLI First`
- [x] Dependencias entre stories corrigidas
- [x] ACs reescritos para o estado real da feature
- [x] DoDs dos drafts corrigidos
- [x] Handoff aponta o primeiro item acionavel para o `@dev`

---

## Acao Esperada do @dev

Comecar por `MOD-DC-HYBRID-2` e tratar como story de operacionalizacao da fundacao ja existente. O criterio de aceite da sprint e fazer override persistir, reaparecer no projeto, recalcular circuito individual e respeitar AUTO-OTI antes de qualquer trabalho de interface.

---

**Atualizado por:** Morgan (PM)
