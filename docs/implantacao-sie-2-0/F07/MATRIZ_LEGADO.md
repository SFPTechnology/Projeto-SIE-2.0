# 07.01 — Equivalência e limitações observadas

Base inspecionada: d83fff44af4a543e66065c3c8423cc8a339ae060, F06.

|Componente|Comportamento existente|Tratamento F07|
|---|---|---|
|domain/engines.py selecionar_condutor|Tabela externa + fator único, sem contexto físico|Preservado para regressão; resolução F01 por trecho no módulo conductor_f07|
|domain/engines.py queda mono/tri|R puro, arredondamento a 0,01 antes da saída|Preservado; nova fórmula AC não usa a saída arredondada|
|src/domain/calculo/otimizador.ts|Catálogo simplificado embutido; aproximação térmica, agrupamento|Não é fonte de dimensionamento do novo motor; sem importação de valores presumidos|
|voltage_checks.py F01|Rca/XL e cosφ explícitos via float, condição declarada|Novo serviço Decimal por trecho, sem alterar contrato antigo|
|cell_bindings.py F01|Oito células; Cu/PVC/B1, dois carregados, condições restritas|Resolver reaproveitado integralmente; CEL-06 XLPE não entra em capacidade PVC|
|topology.py F05|Grafo canônico, percursos alternativos e hash físico|Usado diretamente; alternativas não somadas em série|
|demand.py F06|Corrente de estudo não substitui Ib canônica|F07 lê Ib canônica explicitamente; nenhuma sobrescrita automática|

## Limites de fonte

F01/CASES_REFERENCIA_ENGENHARIA/README.md registra F01-NUM-COND e F01-NUM-QT como PENDENTE. O aceite limitado de oito células não fornece todas as seções, mínimos, neutro, PE, Rca/XL e referências independentes necessárias à F07 integral. O aceite de encerramento da F01 continua preservado: a pendência atual é do gate específico da F07.

Não foram alterados o otimizador legado, engines.py, fixtures golden F00 ou os aceites anteriores. Rca/XL sintéticos da fixture F07 são só referência aritmética, jamais tabela ABNT.
