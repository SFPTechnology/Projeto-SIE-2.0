# Handoff: Correcao C2 - Retencao e Parametros Efetivos da Auto-Otimizacao

**De:** Morgan (PM)  
**Para:** @dev (Dex)  
**Origem:** `docs/PLANO-CORRECAO-C2-RETENCAO-AUTO-OTIMIZACAO.md`  
**Data:** 2026-07-21  
**Status:** InReview  
**Modo:** YOLO  
**Area:** MOD-DC / C2 / AUTO-OTI

## Objetivo

Eliminar o uso de `resultado.parametrosUsados` como fonte atual da auto-otimizacao. A nova execucao deve usar os parametros efetivos derivados do formulario global atual, dos overrides atuais e da sugestao por circuito. Resultados e secoes confirmadas retidos devem ser descartados quando essa entrada efetiva mudar.

## Acceptance Criteria

- [x] Uma alteracao global em `In` invalida a auto-otimizacao retida dos circuitos afetados.
- [x] Uma alteracao global em `I2` invalida a auto-otimizacao retida dos circuitos afetados.
- [x] O botao de auto-otimizacao nunca envia parametros do ultimo resultado quando existem parametros atuais diferentes.
- [x] Overrides customizados continuam isolados e somente invalidam o circuito afetado quando seus parametros efetivos mudam.
- [x] Resultado base desatualizado e identificado antes de nova acao.
- [x] Resultado e secao confirmada nao ficam parcialmente retidos.
- [x] A sugestao `SUGESTAO` e a origem manual `INFORMADO` continuam rastreaveis.
- [x] Existe teste de regressao para alterar `In/I2`, invalidar retencao e otimizar novamente com os parametros atuais.
- [x] `npm run typecheck`, `npm test` e `npm run build` passam; lint global e baseline CRLF ficam documentados separadamente se necessario.

## Arquivos-Alvo

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/dimensionamento-condutores.vrt.test.tsx`

## Plano de Execucao YOLO

1. Derivar parametros efetivos atuais usando a resolucao de global + override + sugestao.
2. Usar esses parametros na assinatura da retencao e na chamada do otimizador.
3. Invalidar resultado/confirmacao quando a assinatura mudar, sem regravar estado antigo com assinatura nova.
4. Marcar resultado base como desatualizado quando os parametros atuais divergirem do ultimo calculo.
5. Adicionar testes de dominio, UI e integracao.
6. Rodar os quality gates e atualizar este registro.

## Dev Agent Record

### Implementacao

- Criado mapa de parametros efetivos atuais com global + override + sugestao.
- Assinatura de retencao e chamada do otimizador passaram a usar a entrada atual, nunca `resultado.parametrosUsados` historico.
- Adicionado bloqueio de persistencia durante troca de contexto para nao regravar resultado antigo com assinatura nova.
- Resultado pai e limpo ao alterar parametros globais; overrides sem recalculo exibem `DESATUALIZADO`.
- Mantida a separacao entre resultado historico e parametros atuais para auditoria.

### Testes

- `npm run typecheck` passou.
- `npm test` passou: 116 arquivos, 743 testes.
- Testes focados de retencao/resumo/UI passaram: 3 arquivos, 15 testes.
- `npm run build` passou.
- ESLint focado dos arquivos alterados passou.
- `npm run lint` global permanece com baseline pre-existente de erros `prettier/prettier Delete CR` em massa, documentado na story anterior.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `docs/PLANO-CORRECAO-C2-RETENCAO-AUTO-OTIMIZACAO.md`
- `docs/stories/HANDOFF-CORRECAO-C2-RETENCAO-AUTO-OTIMIZACAO-to-DEV.md`

### Change Log

| Data | Versao | Descricao | Autor |
| --- | --- | --- | --- |
| 2026-07-21 | 0.1.0 | Story criada a partir do plano de correcao C2 e preparada para execucao YOLO | @pm |
| 2026-07-21 | 1.0.0 | Parametros efetivos atuais, invalidacao de retencao, deteccao de resultado desatualizado e testes implementados; Status: InProgress -> InReview | @dev |
