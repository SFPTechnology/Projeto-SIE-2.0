# Story FORNECIMENTO-SELECAO-01 — Seleção explícita do fornecimento

**Status:** Done  
**Modo:** SDC → YOLO  
**Módulo:** Padrão de entrada / Correntes / MOD-DC

## Objetivo

Permitir que o usuário escolha um padrão de fornecimento compatível quando as cargas cadastradas exigirem tensões que não podem ser resolvidas pelo padrão atualmente selecionado. A escolha deve ser persistida e disparar o recálculo de Correntes e Dimensionamento.

## Critérios de aceitação

- [x] A tela de Padrão de entrada apresenta o padrão selecionado e um formulário de seleção.
- [x] As opções exibidas vêm do catálogo do projeto e indicam as tensões ofertadas.
- [x] Padrões incompatíveis com potência/tensões requeridas não podem ser salvos.
- [x] A seleção persiste `padraoSelecionadoIdOverride` pela API existente.
- [x] Após salvar, Padrão de entrada, Correntes e Dimensionamento são invalidados e recarregados.
- [x] A pendência de tensão desaparece quando o padrão selecionado cobre as cargas.
- [x] O sistema não altera a tensão fixa cadastrada nas cargas.
- [x] Testes cobrem seleção, persistência, recálculo e regressão de cargas 127/220 V.

## Fora de escopo

- Inferir ou alterar automaticamente o fornecimento.
- Alterar tensões, potências ou categorias das cargas.
- Criar catálogo de distribuidora novo.

## Registro SDC

- Story criada e escopo validado: InReview.
- Implementação executada em modo YOLO.

## File List

- `src/components/app/FornecimentoSelector.tsx`
- `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
- `src/domain/nbr/catalogo-fornecimento.ts`
- `src/domain/servicos/servico-padrao-entrada.ts`
- `tests/domain/nbr/catalogo-fornecimento-legado.test.ts`
- `tests/api/padrao-entrada.test.ts` (cobertura existente de override)
- `docs/stories/story-FORNECIMENTO-SELECAO-01.md`

## QA Gate

- Typecheck: aprovado.
- API de seleção/persistência e fluxo Correntes → MOD-DC: 25 testes aprovados.
- Build client/SSR: aprovado.
- Lint direcionado do componente: aprovado sem erros.
- Status final: Done.

## Correção pós-validação

Foi identificado e corrigido um desvio de integração: Correntes consumia o contrato EDP-SP, ignorando o padrão selecionado no contrato canônico de Padrão de entrada. A fonte de tensão de Correntes agora é `tela.contratos.saidaA`, e o padrão selecionado é `tela.contratos.saidaB.padrao_selecionado`.

- Testes Correntes/API/domínio: 28 aprovados.
- Typecheck: aprovado.
- Build client/SSR: aprovado.

## Dev Agent Record

### Debug Log References

- 2026-07-27: reforçada a normalização do catálogo persistido para corrigir projetos antigos com `BI-127-220` salvo com piso incompatível.

### Completion Notes List

- `BI-127-220` passa a ser normalizado por ID para `bi`, tensões `127/220 V` e faixa `0–25 kVA`, corrigindo também assinaturas legadas inconsistentes.
- A configuração normalizada é persistida automaticamente na primeira leitura do projeto antigo.
- Adicionado teste API cobrindo cargas `127/220 V` com demanda abaixo de `8 kVA`, garantindo seleção válida de `BI-127-220`.

### Change Log

- 2026-07-27: correção pontual do catálogo legado persistido, sem alteração dos gates DP-04, DP-07, GP-01, DP-09 ou GO-01B.
- 2026-07-27: reforço da migração por ID e persistência automática do catálogo corrigido.
