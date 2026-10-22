# QA-02 — Engenharia e fontes da vinculação F07

Data da revisão: 22/10/2026. **Veredito: APROVADO para o recorte computacional fonte-vinculado da F07.** Não concede homologação normativa, validação profissional de instalação ou aprovação dos critérios futuros de proteção da F08. Os pareceres anteriores ficam preservados como histórico do incremento declaratório.

## Fonte conferida pelo revisor

- Guia de dimensionamento de cabos para baixa tensão, Prysmian, arquivo oficial identificado como Rev9, 51 páginas.
- URL registrada no catálogo: `https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev9.pdf`.
- PDF local temporário conferido por SHA256: `1729461681fa12bbfe03ea92d26dfb2299c148670d3133046a52f8caf311e4d7`.
- Skill PDF aplicada. Revisão visual das páginas impressas 3, 5, 6, 7, 9, 14, 15, 20, 21, 24 e 33 com renderizações Poppler; não foi usada apenas a extração linear de colunas.
- Publicação do próprio fabricante é fonte primária de seus parâmetros de cabo e de seu guia técnico de aplicação. O guia referencia a NBR 5410:2004; não é reprodução oficial da publicação ABNT nem evidência de homologação. O limite documental inferior de 23/09/2020 é uma escolha conservadora de uso do arquivo, não declaração de início de vigência normativa.
- O PDF completo e suas imagens permanecem temporários; o repositório recebe somente dados técnicos necessários, referências e hash.

## Conferência da transcrição e aplicabilidade

|Critério|Conferência observada|Resultado|
|---|---|---|
|Produto/isolação|Página 3, tabela 1: Superastic cobre/PVC, temperatura máxima contínua 70°C, rating 450/750V. Código diferencia FN450V e FF750V e rejeita FN600V.|APROVADO|
|Método/capacidade|Página 7, tabela 5, B1; página 9, tabela 7, coluna 6, dois carregados. Para 2,5/4/6/10mm²: 24/32/41/57A; coincidem com células F01 aceitas. Métodos 3/5/7 e escopo ao ar são explícitos; outras combinações não recebem fallback.|APROVADO|
|Correções|Base30°C; página14 tabela11 PVC/AR40°C:0,87. Página15 tabela13 referência1:1/0,80/0,70 para1/2/3circuitos. Nota de grupo de mesma seção e corrente não foi omitida: membros identificados, Ib iguais e normalização conjunta das seções durante a seleção.|APROVADO|
|Mínimo de fase|Página5 tabela2, primeira categoria de condutores/cabos isolados em instalações fixas: iluminação Cu1,5mm² e força Cu2,5mm². O catálogo começa em2,5mm²; portanto iluminação pode ficar conservadoramente acima do mínimo. Não há promessa de ótimo econômico.|APROVADO|
|Neutro|Página5 seção4.2/tabela3: política sem redução e mesmo metal/seção no regime senoidal declarado. O código exige neutro em FN e o exclui da ligação FF de dois carregados; harmônicas/redução de neutro não são inferidas.|APROVADO|
|PE|Página6 seção4.3/tabela4: no intervalo do catálogo, PE do mesmo metal tem mínimo igual à fase. Fora do mesmo cabo/conduto, mínimos mecânicos Cu2,5/4mm² são combinados com esse requisito. Layout e contagem física compatível são explícitos. Não equivale à verificação adiabática.|APROVADO|
|Rca/XL|Página33 tabela28, primeiro par de colunas, dois condutores encostados:2,5→8,87/0,12;4→5,52/0,11;6→3,69/0,10;10→2,19/0,10Ω/km. Condições60Hz/70°C e produtoSuperastic foram preservadas. A nota que exclui conduto metálico fechado ferromagnético é respeitada pelo recortePVC.|APROVADO|
|Fórmula AC|Página21 seção6.2: modelo longitudinal mono/bifásico com fator2, comprimento emkm, Rca·cosφ+XL·senφ. Código reutiliza Decimal e seno positivo do regime indutivo/resistivo senoidal. Nenhuma conversão Rdc→Rca ou extrapolação de temperatura.|APROVADO|
|Limites|Página20 seção6.1, casoC e nota1:5% desde ponto de entrega BT e4% local terminal. Seletor verifica o total para cada circuito/alimentador e o local dos terminais separadamente. Não usa suplementações de outros casos.|APROVADO|

## Prova independente de cálculo e seleção

Executei `python -m pytest restructuring/apps/api/tests/test_conductor_binding_f07.py -q --tb=short`: **64 passed, 1 warning, 1,41s**. O aviso é de depreciação Starlette/httpx, não falha de engenharia.

Os esperados da referência tabulada não foram produzidos pelo seletor. Foram lidos na página24, tabela19, primeiro par de colunas para o mesmo produto/arranjo, nos fatores de potência0,80 e0,95. A tabela28 fornece Rca/XL separadamente. Os oito casos usam limite de erro propagado dos arredondamentos impressos: `0,005·[2·(cosφ+senφ)+1]`, sempre inferior a0,02V/(A·km). Essa tolerância serve apenas para confrontar tabelas arredondadas; não relaxa os limites decisórios4%/5%.

Além disso, a referência racional com10A,100m,220V e cosφ4/5 confirma para2,5/4/6/10mm² as quedas `1792/125`, `2241/250`, `753/125`, `453/125`V. A primeira seção do catálogo que atende ao limite local4% é6mm²:4mm² produz `2241/550`% e reprova;6mm² produz `753/275`% e atende. O teste observa efetivamente a sequência2,5→4→6, não somente a fórmula isolada.

A independência aqui é em relação ao algoritmo implementado: tabela pré-calculada do fabricante e conta racional separada. Não se apresenta como auditoria humana ou fonte de outro fabricante.

## Revisão cética do comportamento

- Todos os trechos entram na capacidade corrigida; fatores não são promediados. Caminhos com bases, fases ou cosφ incompatíveis ficam bloqueados em vez de serem somados como equivalentes.
- A política conjunta aumenta seções em caminhos que falham na queda, incluindo companheiros de grupos homogêneos. É conservadora e finita, sem alegar mínima massa/custo global.
- Ausência de membros de grupo, Ib distintas, mudança de método/material/isolação, temperatura fracionária não catalogada,50Hz, conduto metálico, PEN, dados ausentes e versão desconhecida têm diagnósticos explícitos.
- Fronteira numérica exata recebe PENDENTE; não se aprova por arredondamento de apresentação. Catálogo esgotado recebe ausência de solução naquele catálogo, sem extrapolar.
- Fingerprint e histórico incluem catálogo/fonte/política; os testes cobrem invalidação de memórias e documentos/proteção dependentes por seção, corrente, percurso, método, versão/fonte do catálogo e parâmetros.
- O resultado mantém `normative_conformity_verified=false`, `authoritative_for_sizing=false`, `professional_approval=false` e verificaçõesF08 pendentes. O critério Ib≤Iz não é apresentado como proteção integral.

**Achados impeditivos de engenharia nesta revisão: nenhum no recorte examinado.** Os limites acima são parte do contrato de aplicação e devem permanecer visíveis na API, memória e documentação. A decisão global de encerrar a fase ainda exige a integração/QA-03 e os testes/CI consolidados observados pelo executor.
