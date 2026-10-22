# F07 — Contrato final do recorte computacional

## Dois modos preservados

**Estudo livre existente:** CLI `python -m sie_api.conductor_cli restructuring/examples/f07_condutores_demo.json`; POST`/api/v1/condutores/analisar` com Study. Parâmetros declarados permitem investigação, mas não seleção comercial automática nem autenticação de evidência do cliente. Sua saída PENDENTE/REPROVADO continua compatível.

**Seleção fonte-vinculada:** CLI `python -m sie_api.conductor_cli --select restructuring/examples/f07_selecao_fonte_vinculada.json`; POST`/api/v1/condutores/selecionar` com Selection. GET`/api/v1/condutores/catalogo` ou CLI`--catalog` expõem versão, hash, condições e referências. Valores técnicos são resolvidos no servidor; coeficientes/mínimos/flags de aprovação enviados pelo cliente são rejeitados.

## Entrada e resolução

Selection declara a topologia canônicaF05, usoLIGHTING/POWER, aplicação fixa comum sem requisitos especiais, faseFN/FF,cosφ,N,geometriaPE,regime,produto/arranjo/método por trecho, membros dos grupos, versão do catálogo, baseNBR2004corrigida2008, data, origem no ponto de entregaBT e queda anterior com evidência(inclusivezero). Ib é a corrente canônica; F06 não é promovida automaticamente a corrente definitiva.

O resolver aplica o catálogo finito conferido em VINCULACAO_FONTES.md:2,5/4/6/10CuPVC/Superastic, B1doiscarregados,60Hz,70°C,condutoPVC,30/40°C,grupos1–3 quando todos os membros estão identificados e têm mesmaIb. FN respeitaUo450V;FF respeitaU750V, sem inferir tensão para terra quandoFF>450V. Neutrosemredução ePEmesmometal com piso de proteção mecânica explícito. Outros contextos recebem BLOQUEADO com critério/dado faltante.

As impedâncias, mínimos e limites presentes na topologia original não são usados como autoridade no modoSelection: a solicitação explícita de seleção resolve parâmetros pelo catálogo do servidor. A memória retém o pedido original, o hash do catálogo e o Study/topologia resolvidos, tornando essa derivação visível e reproduzível. Não se modifica silenciosamente o agregado persistido para as seções propostas.

## Política de seleção conjunta

1. Determinar a menor seção disponível que atende a capacidade corrigida e os mínimos em **todos os trechos** de cada circuito.
2. Equalizar seções de todos os membros dos feixes homogêneos identificados, inclusive conexões transitivas entre grupos. Não reutilizar homogeneidade declarada antes de mudar a seção.
3. Calcular o vetor completo: Rca/XL de cada seção, cada trecho, queda acumulada de cada circuito/alimentador desde a origem e limite local terminal4%, independente do total5% do casoC.
4. Se um caminho falha em queda, aumentar conservadoramente os condutores disponíveis desse caminho e seus companheiros de grupo; repetir até atender ou esgotar o catálogo. Não há promessa de ótimo econômico global.

A monotonicidade de Iz/Rca/XL é validada no carregamento do catálogo. Cada iteração aumenta pelo menos um índice, com no máximo1+3N iterações paraN circuitos. Esgotamento tem significado somente no catálogo/recorte atual. Estado PENDENTE nunca é apresentado como ausência comprovada de solução. O limite operacional é64circuitos/256trechos por requisição.

## Estados e memória

- `SELECTED_SOURCE_LINKED`: todos os critérios F07 aplicáveis do recorte atendidos; propostas de fase/N/PE por circuito, iterações, fórmulas, intermediários, fontes, topologia resolvida e hashes disponíveis.
- `NO_SOLUTION_IN_CATALOG`: nenhuma solução comprovada no catálogo finito sob as entradas declaradas; nenhuma seção selecionada.
- `BLOQUEADO`: versão/combinação/condição sem suporte ou catálogo inválido/incompleto; motivo por entidade.
- `PENDENTE`: análise inconclusiva, inclusive fronteira numérica; não permite aprovação por arredondamento.

Decimal200, entradas limitadas a30dígitos/expoenteabsoluto30, unidades explícitas. Faixa absoluta de1e−100ponto percentual na fronteira recebe PENDENTE. Apresentação0,01 ou até4casas na interface é separada da decisão. Referência tabulada admite0,02V/(A.km) somente para propagação de arredondamento da fonte, sem relaxar4%/5%.

`normative_conformity_verified=false`, `authoritative_for_sizing=false`, `professional_approval=false`, `f08_protection_checks_pending=true`. Seleção F07 não conclui Ib≤In≤Iz, adiabático, curto-circuito, sobrecarga ou choques. Flags profissionais e escopo F08 não impedem finalizar os gates computacionais F07, mas impedem alegar dimensionamento definitivo.

## Persistência, invalidação e integração

PUT`/api/v1/local/projetos/{UUID}/condutores/selecao` recebe request e expected_revision. Requer token/localidade/ambiente autorizado, mesma topologia atual e UUID novo. Histórico imutável em `conductor_selections`; revisão concorrente409, contrato inválido422. GET`.../condutores` mantém studies e acrescenta selections. CLI`--select --database local.sqlite --expected-revision N` usa o mesmo serviço.

Salvar seleção marca execuções canônicasVALID/PENDING→STALE e documentos/proteção dependentes. Mudanças de Ib, seção, trecho, método, fonte/catálogo, levantamento ou parâmetros invalidam as memórias correspondentes por fingerprint. Revisão, fonte, aceite e células F01 integram esse vínculo. Versões históricas são preservadas. Documentos exportados externamente não são apagados; conferência de hash/revisão continua necessária.

UI`condutores.html`: dois exemplos identificados, consulta do catálogo, critérios por trecho, seções propostas, totais e limites, memóriaJSON e impressão. Editar dados invalida exportação; mudar API também limpa catálogo anterior. Respostas tardias não restauram resultado/catálogo de outra geração.
