# F08 — Catálogo finito de fabricante e proveniência

Conferência em **22/10/2026**. Esta vinculação registra fatos de fabricante; não
declara certificação do produto no Brasil, conformidade integral ABNT, ART ou
aprovação de instalação. PDFs/HTML completos permanecem temporários fora dos
arquivos versionados, sem redistribuição do material integral.

## Arquivos oficiais efetivamente recuperados

| Fonte | Integridade observada | Evidência utilizada |
|---|---|---|
| [Schneider A9F74116, página oficial](https://www.se.com/hk/en/product/A9F74116/miniature-circuit-breaker-mcb-acti9-ic60n-1p-16a-c-curve-6000a-iec-en-608981-10ka-iec-en-609472/) | HTML, 1.546.545 bytes; SHA256 `144a5c03662d0cf86653221d298664a370e9448b2d9d7c749efa49b3d3f9196e` | JSON-LD Product: SKU, título e descrição técnica |
| [Schneider CA908024E, curvas](https://ckm-content.se.com/ckmContent/sfc/servlet.shepherd/document/download/0691H00000DxLluQAF) | PDF1.5, 10 páginas, 1.322.680 bytes; SHA256 `e9665f22fd3e0ec6346a8e682090b2f118c83724df92e72b494a75ea74ec06d6` | Versão2.9, 05/09/2014; PDF2/impressa3, gráfico DB124185, renderizado e conferido visualmente |

O HTML possui conteúdo dinâmico; seu hash identifica a resposta recuperada, sem
promessa de que downloads futuros produzam bytes idênticos. A edição da página
é a fotografia datada; não foi inventado número de revisão do fabricante. O PDF
tem metadados de criação05/09/2014 e modificação25/11/2014. A conferência não
afirma ser a publicação mais recente da família.

Tentativas de obter ficha por URLs de download retornaram HTML, não PDF, e foram
descartadas como evidência. A descrição JSON-LD da página oficial forneceu as
condições de tensão que o título isolado não explicitava.

## Recorte conferido e computável

Único registro: `SCHNEIDER_A9F74116_IEC60898_1`, modelo A9F74116, família MCB,
1polo, 16A, curvaC. O registro usa **Icn6000A a230VAC segundo IEC/EN60898-1**.
A descrição também informa capacidade10kA com outra norma e faixa de tensão;
esse valor não integra a seleção deste registro. Icn/Icu não são intercambiados.

A curva DB124185 abrange iC60a/N/H/L de6–63A, AC50/60Hz, referência30°C.
I2=1,45In resulta23,2A e tempo convencional3600s. A faixa magnéticaC é5–10In.
São pontos/faixas documentais, sem digitalização da curva inteira, interpolação
de tempos, transformação da faixa em tempo de eliminação ou inferência deI²t.

`applicable()` exige230V,30°C,50ou60Hz, AC e1polo. Outros valores requerem dados
adicionais. A faixa de temperatura operacional do produto não substitui os
fatores de correção da corrente nominal. Também cabe ao motor conferir
topologia, condutores vivos protegidos, conexão e instalação real.

O catálogo retorna cópias e valida identidade, grandezas, norma, fonte e ausência
de aprovação profissional. `verified_fields` limita o significado de
`source_verified`: fatos conferidos no recorte, sem autenticar instalações.

## Limites impeditivos explícitos

- O texto introdutório do PDF, páginaimpressa2, exige características de energia
  para seletividade de curto e informa insuficiência da curva tempo/corrente
  acima20In. Não há tabela de seletividade de pares nem curva de energia neste
  registro individual. O catálogo de pares separado abaixo cobre uma única
  combinação; comparar In ou letras de curvas não comprova outras combinações.
- Nenhum produto fusível, DR ou DPS é autenticado por este catálogo. Os modelos
  declaratórios desses dispositivos devem permanecer identificados como tais.
- Nenhum dado de fonte, aterramento, ensaio físico ou inspeção de obra foi
  obtido destes documentos de produto.
- Não existe extrapolação para outra tensão, temperatura, frequência, polos ou
  condição de instalação; a ausência mantém avaliação dependente pendente.
- Fontes normativas locais e aceites F01 são preservados. Este catálogo não
  substitui requisitos da NBR5410, NBR5419, NR10 ou concessionária.

## Evidência de software

Arquivos: `protection_registry_f08.py`,
`data/protection_schneider_f08.json`, `tests/test_protection_registry_f08.py`.
Os testes verificam escopo exato, rejeição de misturaIcn/Icu/norma/tensão,
proveniência incompleta, aprovação inventada, catálogo desconhecido e cópias
isoladas. Os resultados reais de execução constam do relatório da fase.

## Complemento: par de seletividade autenticado

- Documento: **Selectivity, Cascading and Coordination Guide2026**, referência
  **LVPED318033EN**, versão4.0, lançamento03/08/2026 confirmado na
  [página oficial](https://www.se.com/us/en/download/document/LVPED318033EN/).
- [PDF oficial recuperado](https://download.schneider-electric.com/files?p_Doc_Ref=LVPED318033EN&p_File_Ext=.PDF):
  362páginas, 11.585.539bytes, SHA256
  `2cc52f0569eeef7323677dfee855c9ebf5bc0fb7ee7d370ad22fabfeda1b1fa3`.
- PDF39, páginaimpressaA-31, bloco jusantecurvaC: linha16A e coluna montante32A
  fornecem **260A**, limite numérico parcial, sem símboloT. O cabeçalho identifica
  iC60N/H/L/P montantecurvaC e a categoria de jusante inclui1P. A célula foi
  renderizada e conferida pelo executor e independentemente pelo QA02.
- Registro `SCHNEIDER_IC60N_C32_C16_1P_230`: recorte conservador **230VAC**,
  **iC60NcurvaC32A montante / iC60NcurvaC16A jusante**, ambos1P,
  fabricanteSchneiderElectric. A tabela abrange220–240/380–415VAC, mas o
  software não extrapola o registro para outras redes/polos/tensões.
- A identidade da série iC60N deve ser informada e confrontada com a topologia;
  o SKU A9F74116 pode ser associado à série pela página oficial já conferida.
  Nenhum SKU32A foi inventado. A tabela não autentica um equipamento instalado.
- Corrente de falta máxima jusante **≤260A**, inclusive a fronteira, satisfaz
  somente a comparação computacional do par neste recorte; acima do limite
  não se declara seletividade assegurada. Isso não prova integral passante,
  capacidade de interrupção, retaguarda, DR, DPS ou proteção geral.
- `resolve_pair()` e `coordination()` retornam cópias do par; `catalog()` inclui
  `coordination_catalog`, e `catalog_hash()` cobre também esta fonte. Mudanças
  no par invalidam a referência dos resultados persistidos. Não há inferência
  por relação de correntes nominais nem aprovação de outros pares.

Arquivo adicional: `data/protection_coordination_schneider_f08.json`. Testes do
registry, após este incremento: **40passed**, 0,12s. A prova de integração do
limite e da identidade do par pertence aos testes do motor, não é substituída
pelo teste de leitura do catálogo.
