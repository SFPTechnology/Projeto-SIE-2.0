# P06 e P03 — incremento sobre o lote 01

Story: `story-SIE-F01-GOVERNANCA-NORMATIVA.md`. Base: `d0b10bf2670db24886beff70ab67ecf3ec8441e4`.

## Resultado e limites

O servidor dispõe de registro versionado separado do Python (`sie_api/data/f01_lote01_cells_v1.json`) das oito células aceitas no lote 01 e valida o vínculo de condições, IDs, capacidades e fatores antes de calcular. O aceite recebido tem SHA-256 `2ffbed5b4cb89a10eed13a42acac1fad4daa3873b90c30b5a9439af8846fdd6c`. Não se publica a identidade profissional ou o documento integral. A fonte de referência declarada pelo responsável é o exemplar `e1c02de1e1b5ed070ad7b642e60e0491a0c899e83fe8f2ad5699a743842bbda6`; não há declaração de equivalência byte a byte ou página a página com o exemplar anterior `45f246e3…aa3d`.

O verificador de sobrecarga calcula `Ib ≤ In ≤ Iz` e `I2 ≤ 1,45 Iz`; aplica `I2 ≤ Iz` quando a duração excede 100 h em 12 meses OU 500 h na vida útil. Não deduz I2 de In. Dados e hash do dispositivo são declarações de entrada, não fontes verificadas pelo servidor.

**F01 BLOCKED; P01–P08 abertas; uso normativo e F02 não liberados.** Este incremento não conclui a proteção contra curto-circuito, seletividade/coordenação, cobertura normativa integral ou QA3 final. O aceite limitado dos 14 itens permanece preservado.

## Executar via CLI ou API

Após instalar a API com `python -m pip install -e 'restructuring/apps/api[test]'`, na raiz do repositório:

```sh
python -m sie_api.cli analisar --arquivo restructuring/examples/f01_lote01_ensaio_parcial.json
```

A API recebe o mesmo objeto em `POST /api/v1/circuitos/analisar`. O exemplo utiliza as células do lote, mas o dispositivo de proteção é **sintético**, identificado explicitamente como tal. Serve apenas para testar o fluxo. Não é catálogo de fabricante nem projeto homologado.

O novo campo opcional `vinculo_celulas` exige revisão `F01-LOTE01-RT-2026-10-20-v1`, lista de IDs e todas as condições do exemplo. São aceitas apenas capacidades Cu/PVC 70°C, método B1, dois carregados, ar a 30 ou 40°C, sem radiação solar ou infravermelha, métodos de instalação declarados 3/5/7. A descrição é declaração do usuário, sem verificação do enquadramento de uma instalação real (P02 continua aberta).

As quatro células de capacidade são exigidas integralmente para impedir seleção de um subconjunto de candidatos. A 40°C é obrigatória CEL-05; a 30°C vale a condição de referência da tabela. Dois/três circuitos usam CEL-07/CEL-08 e exigem feixe homogêneo uniformemente carregado. O servidor deriva tabela e produto dos fatores e rejeita qualquer valor divergente. CEL-06 está registrada como aceita para EPR/XLPE, mas não pode ser aplicada à tabela PVC deste lote. Fatores >1 e outras condições permanecem fora deste escopo.

Sem `vinculo_celulas`, a entrada legada continua sendo ensaio com tabela/fator declarados e **não recebe classificação de célula aceita**. Os campos de evidência antigos nunca concedem aprovação.

## Proteção parcial

O campo opcional `protecao_sobrecarga` exige In do dispositivo igual ao In selecionado, I2 positivo e não inferior a In, identificação do dispositivo e documento/revisão/referência/hash. Campos vazios, desconhecidos e números não finitos são rejeitados. Este incremento verifica o par selecionado; não pesquisa catálogo de modelos/dispositivos para encontrar outro par quando I2 falha.

| Situação | Resultado da sobrecarga |
|---|---|
| I2 ou dados do dispositivo ausentes | PENDENTE |
| As duas durações conhecidas e dentro de 100/500 h | Limite 1,45 Iz |
| Qualquer duração excede seu limite | Limite Iz, mesmo se a outra duração é desconhecida |
| Duração insuficiente para determinar a condição e limite ordinário atendido | PENDENTE |
| Desigualdade aplicável não atendida | NAO_ATENDE |
| Desigualdades atendidas e condição determinada | ATENDE_CALCULO_PARCIAL |

As comparações usam Decimal sem arredondamento. Exatamente 100 e 500 h não acionam a condição restrita; exatamente no limite de corrente a desigualdade é atendida. Mesmo `ATENDE_CALCULO_PARCIAL` mantém fonte do dispositivo não verificada, curto-circuito/coordenação pendentes e liberação normativa falsa. Não atesta a proteção completa nem a instalação.

## Persistência e compatibilidade

Os novos campos pertencem ao contrato tipado de circuito e devem estar salvos na revisão imutável para registrar ensaio. A solicitação é comparada com a revisão, incluindo condições, IDs e dispositivo; divergência não é preenchida silenciosamente a partir do cliente. Valores opcionais ausentes preservam a forma histórica de entrada, sem backfill.

Trilhas com células usam formato v3, snapshot de condições/valores, hashes do registro e aceite, ID da célula de capacidade selecionada e proveniência dos módulos efetivamente executados. Trilhas sem vínculo conservam o formato v2; novas verificações de proteção exigem sua proveniência mesmo sem células. A classificação geral de conformidade e os IDs de normas homologadas permanecem falsos/vazios: o aceite limitado de células não homologa o motor, resistência ou dispositivo.

A leitura verifica coerência do snapshot e do resultado parcial de sobrecarga. Formatos históricos v1/v2 sem novos campos continuam legíveis. **Não substituir REVISION/CELLS v1 ao cadastrar novo lote:** manter o resolvedor desta revisão e acrescentar uma nova versão. Alterar o significado de uma revisão existente quebraria a reprodutibilidade histórica.

## Validação

Testes cobrem API, CLI, fonte sintética explícita, condições incompatíveis, CEL-06/PVC, adulteração de capacidades/fatores/IDs, limites exatos e epsilon de I2/duração, revisão imutável, tentativa de remover proveniência e histórico legado. O parecer de QA independente e a CI do SHA publicado complementam os testes locais. Gates normativos não são aprovados por estes testes de software.
