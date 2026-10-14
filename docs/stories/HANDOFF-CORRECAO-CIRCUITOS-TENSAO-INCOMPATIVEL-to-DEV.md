# Handoff: Correção de circuitos adicionais bloqueados por tensão

**De:** Atlas (Analyst)  
**Para:** @dev (Dex)  
**Data:** 2026-07-21  
**Status:** Ready for Dev  
**Área:** Correntes / MOD-DC / contrato de circuitos

## Objetivo

Impedir que cargas adicionais cadastradas desapareçam das telas de **Correntes de projeto (IB)** e **Dimensionamento de condutores** quando a tensão declarada da carga não estiver disponível no padrão de fornecimento do projeto.

O sistema deve preservar a entidade no fluxo, sinalizar o bloqueio técnico e transportar o estado até o contrato do MOD-DC. Um circuito incompatível não deve receber IB calculado nem ser dimensionado como se fosse válido.

## Evidência confirmada

Na evidência visual analisada:

- Cadastro: 4 cargas adicionais, total de 6.900 VA.
- Correntes: 5 circuitos exibidos.
- `ADD-Area-Servico-LuminariaLED` (127 V) aparece.
- Secadora, Lava roupa e Lava louça (220 V) não aparecem.
- O projeto está em fornecimento monofásico com tensão disponível de 127 V.

O caminho atual é:

1. `derivarCircuitos` cria os circuitos `ADD-*` a partir de `cargasAdicionais`.
2. `calcularCorrentesCircuitos` detecta tensão indisponível em `src/domain/calculo/corrente-circuitos.ts:148` e apenas registra diagnóstico.
3. O mesmo caminho não adiciona o circuito ao array de saída; o `out.push` ocorre apenas para circuitos calculados em `:191`.
4. `servico-corrente.ts:295` monta `contratoSaidaDimensionamento` exclusivamente com `resultado.circuitos`.
5. `servico-dimensionamento-condutores.ts:310` adapta somente esse contrato para o MOD-DC.

## Escopo da correção

### 1. Preservar circuitos bloqueados em Correntes

Alterar o contrato de saída de Correntes para que um circuito com tensão incompatível continue identificável em `dados.circuitos`, com:

- `id`, descrição, tipo, potência e tensão declarada;
- estado explícito de bloqueio/incompatibilidade;
- diagnóstico `ERR-CORRENTE-TENSAO-INDISPONIVEL` ou o código equivalente já existente, sem duplicar códigos;
- ausência de IB/rastreio quando o cálculo não puder ser executado.

Não calcular IB usando uma tensão diferente da tensão declarada e não converter silenciosamente 220 V para 127 V.

### 2. Propagar o estado ao contrato do MOD-DC

O contrato `ContratoSaidaDimensionamento` deve transportar os circuitos bloqueados ou um estado equivalente que permita ao MOD-DC reportá-los como pendentes/bloqueados.

O MOD-DC não deve executar dimensionamento normativo em circuito sem IB válido ou com tensão incompatível. Deve devolver resultado rastreável, com status/pendência explícita e motivo técnico.

### 3. Exibir o bloqueio nas telas

Atualizar Correntes e Dimensionamento de condutores para:

- contar os circuitos derivados, inclusive os bloqueados;
- exibir o circuito na lista/tabela;
- mostrar tensão declarada, tensões disponíveis e motivo do bloqueio;
- diferenciar `bloqueado por tensão` de `pendente por pré-requisito`;
- manter a carga adicional rastreável por ID desde o cadastro até o MOD-DC.

### 4. Manter compatibilidade com circuitos válidos

Circuitos em tensão disponível devem continuar com o comportamento atual, incluindo cálculo de IB, rastreio de fórmula, contrato de saída e dimensionamento.

## Critérios de aceite

- [ ] O cenário mono 127 V com uma carga adicional em 127 V e três cargas adicionais em 220 V exibe todos os circuitos derivados em Correntes.
- [ ] A carga de 127 V possui IB calculado normalmente.
- [ ] Cada carga de 220 V aparece como bloqueada por tensão incompatível, sem IB fictício.
- [ ] O resumo de Correntes não informa somente os circuitos calculáveis; a contagem total e a contagem bloqueada ficam distinguíveis.
- [ ] O contrato enviado ao MOD-DC contém os IDs das cargas de 220 V com estado bloqueado/pendente.
- [ ] O MOD-DC não calcula seção/proteção para circuito bloqueado por tensão.
- [ ] A tela de Dimensionamento de condutores mostra esses circuitos e o motivo do bloqueio.
- [ ] Nenhuma carga adicional cadastrada é perdida por causa da tensão incompatível.
- [ ] Cargas e circuitos válidos mantêm o resultado anterior.
- [ ] O ID e a origem da carga permanecem rastreáveis em diagnóstico, Correntes e MOD-DC.

## Testes obrigatórios

Adicionar ou ampliar testes nos pontos abaixo:

1. `tests/domain/calculo/corrente-circuitos.test.ts`
   - tensão disponível: circuito calculado;
   - tensão indisponível: circuito preservado como bloqueado e diagnóstico emitido;
   - ausência de IB para circuito bloqueado.
2. `tests/api/correntes.test.ts`
   - cenário mono 127 V com carga TUE 220 V;
   - IDs presentes em `circuitos` e no contrato de dimensionamento;
   - diagnóstico e contagem de bloqueados.
3. `tests/api/dimensionamento-condutores-flow.test.ts`
   - MOD-DC recebe o circuito incompatível;
   - resultado não dimensiona circuito sem IB/tensão compatível.
4. `tests/ui/correntes-rastreabilidade.vrt.test.tsx`
   - circuito bloqueado aparece com status e motivo.
5. `tests/ui/dimensionamento-condutores.vrt.test.tsx`
   - circuito bloqueado aparece na tela MOD-DC e não é tratado como resultado válido.
6. Teste de regressão para o cenário visual real:
   - LED 127 V;
   - Secadora 220 V;
   - Lava roupa 220 V;
   - Lava louça 220 V.

## Arquivos-alvo prováveis

- `src/domain/calculo/corrente-circuitos.ts`
- `src/domain/calculo/contratos-corrente.ts`
- `src/domain/servicos/servico-corrente.ts`
- `src/domain/dimensionamento-condutores/adaptadores/adaptador-correntes.ts`
- `src/domain/dimensionamento-condutores/contratos.ts`
- `src/domain/servicos/servico-dimensionamento-condutores.ts`
- componente da tela Correntes
- `src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- testes de domínio, API e UI correspondentes

Confirmar os arquivos efetivamente alterados no File List da story após implementação.

## Fora de escopo

- Alterar as tensões cadastradas pelo usuário.
- Trocar automaticamente o padrão de fornecimento do projeto.
- Reclassificar carga 220 V como 127 V.
- Alterar regras de cadastro ou os valores de potência.
- Corrigir outros problemas de dimensionamento não relacionados à perda de circuitos por tensão.

## Riscos e decisões esperadas

- O tipo atual de circuito pode exigir campos opcionais para representar bloqueio sem inventar IB.
- O MOD-DC deve distinguir circuito bloqueado de circuito ainda não calculado por pré-requisitos normativos.
- Se houver contrato versionado, atualizar a versão e os testes de compatibilidade.
- Preservar os diagnósticos existentes e evitar duplicação entre Correntes e MOD-DC.

## Validação final

Executar no subprojeto `sistema-de-instala-es-el-tricas-sie-main`:

- `npm run lint`
- `npm run typecheck`
- `npm test`
- `npm run build`

Atualizar o checklist, o File List e o Dev Agent Record da story usada pelo @dev.

## Dev Agent Record

### Implementação concluída

- Circuitos com tensão incompatível agora permanecem no resultado de Correntes com `status: BLOQUEADO`, diagnóstico e motivo explícito, sem cálculo de IB.
- O contrato de saída para MOD-DC preserva esses circuitos em `circuitosBloqueados`, mantendo separados os circuitos válidos dimensionáveis.
- A tela Correntes exibe contagem, status, tensão, motivo e ausência de IB para os circuitos bloqueados.
- A tela Dimensionamento de condutores exibe os bloqueios preservados e não os trata como resultados dimensionáveis.
- Cobertura adicionada/ajustada em domínio, API, fluxo Correntes → MOD-DC e snapshots de UI.

### File List

- `src/domain/modelo/circuito.ts`
- `src/domain/calculo/contratos-corrente.ts`
- `src/domain/calculo/corrente-circuitos.ts`
- `src/domain/servicos/servico-corrente.ts`
- `src/domain/servicos/servico-dimensionamento-condutores.ts`
- `src/routes/projetos.$projetoId_.correntes.tsx`
- `src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `tests/domain/calculo/corrente-circuitos.test.ts`
- `tests/api/correntes.test.ts`
- `tests/api/dimensionamento-condutores-flow.test.ts`
- `tests/ui/correntes-rastreabilidade.vrt.test.tsx`
- `tests/ui/__snapshots__/correntes-rastreabilidade.vrt.test.tsx.snap`
- `tests/ui/dimensionamento-condutores.vrt.test.tsx`

### Validação

- `npm run typecheck`: aprovado.
- Testes focados: aprovado — 6 arquivos, 42 testes.
- `npm test`: 735 testes aprovados; bloqueado por arquivo preexistente vazio `tests/domain/calculo/derivar-circuitos.test.ts` (suíte sem testes).
- `npm run lint`: excedeu o tempo limite no lint global; lint direcionado encontrou apenas divergência preexistente de finais de linha CRLF/LF.
