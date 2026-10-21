# Vinculação de fontes e fatores F06 — 21/10/2026

**IMPLEMENTADA.** O catálogo do servidor contém 22 regras: tabelas EDP 005/006 (12 atividades)/007/008/009/010/012/013/014/015 e o critério residencial de condicionadores de ar do item 5.5.2.f. Coeficientes e condições saem do catálogo, não de um status VERIFIED enviado pelo cliente.

## Fonte conferida

Documento: PT.DT.PDN.00068, versão 09, EDP São Paulo, início 14/04/2026, fim condicionado. Página oficial de normas e PDF oficial consultados em 21/10/2026:

- https://www.edp.com.br/normas-e-padroes-tecnicos/
- https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf

|Prova|SHA256|
|---|---|
|PDF oficial obtido nesta execução|`2c2bcad13fb44d042bdfd2d8473b035d863bf654b71e64d2e3f929d21a287690`|
|PDF já existente no repositório|`b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810`|
|Texto integral de ambos, extraído com pdftotext -layout|`f4fda196cb5335179bd9dfd2a1083eac32bda01b55ae877bd6c2235f852b9ca8`|

Os PDFs não são byte a byte iguais; os textos extraídos são idênticos (`diff` sem diferença). Tabelas conferidas por texto e imagens das páginas 34–37. A edição continua congelada: data anterior ao início ou posterior à última conferência do catálogo gera pendência, sem presumir vigência futura.

## Regras efetivas

|Regra|Fonte|Base/condição preservada|
|---|---|---|
|T005|p34, 5.5.2.a p24|Carga ativa em W, convertida dos limites em kW; limite superior inclusivo; fator aplicado aos VA individuais|
|T006, 12 atividades|p34 e notas p35|Parcelas progressivas em W; cozinha com fator 1; atividade e cargas mínimas declaradas/conferidas|
|T007|p35, 5.5.2.b p24|Quantidade total; exceção de aquecimento de água em vestiário; mistura com outras parcelas recebe diagnóstico para revisão|
|T008|p35|Quantidade de boiler/sauna|
|T009|p36|Quantidade total de aparelhos do grupo; fp por equipamento declarado|
|T010|p36|Quantidade de fogões elétricos|
|T012 / AC residencial|p37 e item 5.5.2.f p25|Quantidade para uso comercial; unidade central e uso residencial com fator 1; declaração explícita de unidade central|
|T013|p37|Um maior motor a 1 e restantes a 0,5; partidas simultâneas combinadas; ranking unitário explícito; sem inferir CV/HP/eficiência|
|T014|p37|Um maior aparelho por tipo a 1 e restantes a 0,6; não mistura tipos|
|T015|p37|Quantidade de hidromassagens|

Categorias e tipos de equipamento continuam escolhas explícitas. Quantidade é a quantidade de aparelhos já representada na potência total F02, e não novo multiplicador. O mapa F04/F02 preserva a auditoria de quantidade única. Fonte, página, tabela, regra, seleção, fatores por carga e hash do catálogo entram na memória. O hash participa do fingerprint e invalida histórico quando o catálogo muda.

IDs reservados não podem ser acompanhados de coeficientes substitutos do cliente. Rótulos de grupo não permitem fracionar artificialmente uma mesma regra por fonte. FINAL_CIRCUIT/FEEDER não aceitam regra EDP de entrada. Território, distribuidora, edição, data, atividade, tensão/frequência e tipologia incompatíveis não calculam. Mistura de conexões em regras de máximo, ranking/partida desconhecidos e condições ausentes recebem diagnóstico; nenhum coeficiente é escolhido por palpite.

A confirmação de cargas mínimas é uma declaração explícita do responsável pelos dados; o motor não faz levantamento de área, vitrine, placa ou conversão CV/HP automaticamente. A identidade da fonte e os coeficientes foram conferidos computacionalmente; isso não atribui uma assinatura de engenheiro nem aprovação da EDP.

## Uso

1. No painel, abrir **Demanda e alimentação** e **Conferir catálogo e fontes**.
2. Para conferir o exemplo documental, abrir **Referência EDP V09** e calcular. São dados de referência, não projeto real homologado.
3. Para uma instalação, declarar assignments com rule_id reservado, categoria/tipo, quantidade, alvo fonte, origem/condições e contexto aplicável. Não enviar a regra inteira em rules.
4. Conferir memória e pendências. Dados insuficientes continuam pendentes por instalação.

CLI:

```bash
PYTHONPATH=restructuring/apps/api python -m sie_api.demand_cli --catalog
PYTHONPATH=restructuring/apps/api python -m sie_api.demand_cli restructuring/examples/f06_demanda_edp_v09_referencia.json
```

API: GET `/api/v1/demanda/catalogo`; POST `/api/v1/demanda/calcular`. Resultado completo vinculado: `CALCULATED_SOURCE_LINKED`. `normative_conformity_verified=false`, `utility_approval=false` e `authoritative_for_sizing=false` permanecem explícitos: o vínculo não é homologação de uma instalação.

## Referências independentes e arredondamento

O ensaio das pp42–44 usa as potências e os fp da fonte, com fatores esperados escritos nos testes (sem lê-los do catálogo). Parcela a exata: 24426/11 VA; a fonte apresenta 2221 VA após arredondamento. b=11248 VA e d=3062,5 VA. O total exato é aproximadamente 16531,04545 VA; o exemplo impresso soma 16531,5 VA e apresenta 75,1 A em 220 V. Os testes verificam a conta exata por aritmética racional e registram a diferença de arredondamento inferior a 0,5 VA, sem alterar coeficientes para forçar igualdade.
