---
titulo: 'Harmônicas'
arquivo_origem: 10_harmonicas.pdf
formato_origem: pdf
autor: 'user'
data: 'D:20020515151425-03''00'''
idioma: pt-BR
paginas: 6
mapa_de_secoes:
  - 'H A R M Ô N I C A S'
  - 'Dimensionamento dos condutores na presença de harmônicas'
  - 'Exemplos de dimensionamento'
  - 'A ameaça das harmônicas'
  - 'Método da NBR 5410'
notas_de_extracao: 'Modo verbatim-limpo; 3 figuras/diagramas referenciados; páginas com vetores preservadas por referência visual.'
---

# Harmônicas

<!-- pagina-origem: 1 -->

### H A R M Ô N I C A S

Dimensionamento dos condutores na presença de harmônicas.............240

<!-- pagina-origem: 2 -->

## Dimensionamento dos condutores na presença de harmônicas

Em relação ao modo tradicional de se determinar a seção dos condutores, o que muda no cálculo quando os fios e cabos são percorridos por correntes harmônicas? É preciso aumentar a seção dos condutores devido à presença das harmônicas? De fato, o dimensionamento de condutores tem sido feito, tradicionalmente, sem considerar a presença de harmônicas. Nada errado com os critérios básicos de dimensionamento, em si — aqueles seis critérios implícitos na NBR 5410, isto é, seção mínima, capacidade de corrente, queda de tensão, sobrecarga, curto-circuito e contato indireto (apenas quando se usa dispositivo a sobrecorrente). Não, eles não mudam, existam ou não harmônicas. O que muda é o cálculo do valor da corrente com o qual serão equacionados esses critérios. Recapitulemos. O passo prévio à aplicação desses critérios é o cálculo da corrente de projeto (IB), com base na previsão de carga do circuito. Presume-se, assim, que IB será a maior corrente (valor eficaz) a circular no circuito — incluindo, portanto, considerações seja sobre a não-simultaneidade no funcionamento das cargas (fator de demanda), seja sobre a possibilidade de aumento futuro da carga (“fator de reserva”). É a partir da corrente de projeto IB que se dimensiona o condutor pelo critério da capacidade de condução de corrente — o que é feito entrando-se com o valor de IB, corrigido ou não com fatores que levam em conta temperatura

<!-- tabela-p2-1 -->
| Tab. I – Diferença de resultados no dimensionamento do circuito
considerando ou não a presença de correntes harmônicas |  |  |
| --- | --- | --- |
|  | Seção do condutor
de fase (mm2) | Seção do condutor
neutro (mm2) |
| Considerando as harmônicas | 70 | 95 |
| Não considerando as harmônicas | 35 | 25 |

ambiente, agrupamento de circuitos, etc., nas tabelas da NBR 5410 que fornecem a capacidade de corrente de cada seção de condutor. É também a partir da corrente de projeto que se calcula a queda de tensão no circuito e que se escolhe o dispositivo de proteção contra sobrecarga. Quando as harmônicas não constituíam a dor-de-cabeça que hoje representam, tudo era mais simples, claro. No projeto de circuitos trifásicos, em especial, havia uma certa tranqüilidade em assumi-los equilibrados ou, de qualquer forma, supor que o neutro não seria percorrido por correntes de desequilíbrio altas o suficiente para nos impedir a especificação — explorando uma abertura tradicionalmente concedida pelas normas de instalações — de uma seção de neutro igual à metade da dos condutores de fase.

![Figura vetorial da página 2](figura-vetorial-p2-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Exemplo de circuito 2F com presença de harmônicas

Porém, com o uso cada vez mais generalizado de equipamentos eletrônicos e, com eles, a presença de elementos retificadores (como a simples fonte chaveada de um microcomputador, por exemplo), o cenário já não é o mesmo. Tudo muda. As correntes e tensões já não são como mostram os “álbuns de fotografia”, os nossos compêndios de eletrotécnica. Aquela forma senoidal perfeita, ortodoxa, quase sisuda, agora ficou imprevisível! Nas ondas da modernidade, ela ganhou contornos psicodélicos. Na verdade, não é a corrente ou tensão que mudou de cara e está irreconhecível. É que a corrente ou tensão se tornou plural. Já não temos mais uma só corrente, mas a corrente e suas harmônicas. Temos a tradicional corrente de 60 Hz, nossa velha conhecida, e o seu séquito de harmônicas. Não é isso o que a análise de Fourier nos diz? Que todo sinal deformado pode ser decomposto em senóides perfeitas, cada uma com sua freqüência característica? Assim, o retrato já não é o mesmo porque, na verdade, o que estamos vendo é uma série de retratos superpostos — idênticos na forma de onda, mas de amplitude e freqüências diferentes: estão lá a corrente de 60 Hz, sua prima indesejável de 180 Hz, a discreta prima de 120 Hz e toda a grande família que a eletrônica, antes mesmo de clonagem virar moda, vem produzindo.

<!-- pagina-origem: 3 -->

É essa então a novidade desagradável que a difusão da eletrônica reserva para o profissional de instalações: a sua corrente, a corrente de projeto, ganhou companhia. A corrente virou família, a família das harmônicas (ver boxe). O mais antigo e conhecido membro dessa agora família é o sinal de 60 Hz, dito fundamental — a corrente ou tensão de freqüência fundamental. Os demais são múltiplos do sinal de 60 Hz, caracterizados cada um por uma freqüência múltipla da fundamental. Há, assim, as harmônicas pares, como é o caso dos sinais superpostos de 120 Hz (2 × 60), de 240 Hz (4 × 60), etc. E há as harmônicas ímpares, como é o caso dos sinais superpostos de 180 Hz (3 × 60), de 300 Hz (5 × 60), etc. Uma forma de as identificar individualmente é designá-las pela sua ordem. Assim, a harmônica de 180 Hz (3 × 60) é a harmônica de 3ª ordem ou, simplesmente, 3ª harmônica. E assim por diante. Isso tudo para destacar que cada corrente harmônica, de uma dada ordem, possui valor eficaz próprio, que aquece o condutor individualmente e também provoca nele uma queda de tensão. E há, portanto, um efeito cumulativo, resultante da ação conjunta de todas, que deve ser levado em conta. Desse modo, quando for prevista a existência de harmônicas em um circuito — o que hoje é quase uma regra —, o correto dimensionamento desse circuito exige que elas sejam consideradas, ao lado da fundamental (aquela com o qual estamos acostumados), na obtenção do valor de IB. Além disso, em circuitos trifásicos com neutro, e dependendo da ordem das harmônicas presentes, a corrente no neutro, contrariamente ao senso habitual, que a presume de intensidade reduzida ou quase nula, poderá ser até três vezes o valor da fundamental da corrente de fase (ver boxe). Isso significa que, ao invés de especificar um neutro de seção reduzida — por exemplo, metade da do condutor de fase —, é possível que o projetista tenha, isso sim, de atribuir-lhe uma seção nominal superior à dos condutores de fase. Enfim, a corrente de projeto passa a ser o valor eficaz

<!-- tabela-p3-2 -->
| Tab. II – Fatores de correção aplicáveis a circuitos
trifásicos a 4 condutores nos quais é prevista a
presença de correntes harmônicas de 3ª ordem (*) |  |  |
| --- | --- | --- |
| Porcentagem de
3ª harmônica na
corrente de fase (%) | Fator de correção |  |
|  | Escolha da seção
com base na
corrente de fase | Escolha da seção
com base na
corrente de neutro |
| 0–15 | 1,0 | – |
| 15–33 | 0,86 | – |
| 33–45 | – | 0,86 |
| > 45 | – | 1,0 |

(*) Tabela 45 da NBR 5410 da corrente total resultante. Assim, em um circuito percorrido por correntes harmônicas de ordem 1, 2, 3, 4,..., n temos:

2 2 2 2 2 = + + + + I I I I I.... I B n 1 2 3 4

### Exemplos de dimensionamento

Circuito 2F Seja um circuito de duas fases que alimenta um quadro de distribuição, conforme figura 1. As correntes presentes nesse circuito são: a de 1ª ordem (fundamental), a 3ª, a 5ª e a 7ª harmônicas, com intensidades (valores eficazes) de, respectivamente, 110, 57, 25 e 17 A. Logo, o valor da corrente de projeto IB a considerar no dimensionamento dos condutores desse circuito é:

<!-- tabela-p3-1 -->
| I = I2+I2+I2+I2 =
B 1 3 5 7
= ((1110))22 ++ ((55 7))22 ++ ((22 5))22 ++ ((11 77))22 == 112277A |  |  |
| --- | --- | --- |
|  | ((1110))22 ++ ((55 7))22 ++ ((22 5))22 ++ ((11 77))22 == 112277A |  |

Como se vê, um valor 15,5% superior ao da corrente fundamental (110 A) — a IB que seria adotada caso não houvesse as harmônicas. Mas isso é só o começo. IB, convém repetir, é o valor com o qual se procede ao dimensionamento dos condutores. Mais exatamente, IB é utilizada no equacionamento dos critérios da capacidade de corrente, queda de tensão e sobrecarga. Ora, desses três critérios, os dois últimos apenas confirmam ou gravam o primeiro. Em suma, a seção de condutor que se busca definir deve, no mínimo, proporcionar uma capacidade de corrente suficiente para a circulação de IB, sem problemas. Fiquemos, pois, apenas com o critério da capacidade de condução de corrente, que já nos fornece, como se verá, uma boa idéia do impacto das correntes harmônicas no dimensionamento de um circuito. Os outros dois, como mencionado, apenas confirmariam ou majorariam a seção de condutor aí encontrada (a menos que o projetista mudasse de idéia e resolvesse dividir carga e circuito, substituindo o original por dois ou mais, o que já é uma outra história, pois não teríamos mais a mesma IB e o mesmo circuito). Assim, para o equacionamento da capacidade de corrente, ou seja, para determinarmos a seção de condutor capaz de atender IB = 127 A, vamos acrescentar ao nosso exemplo alguns dados necessários. Suponhamos que o cir-

<!-- pagina-origem: 4 -->

cuito do exemplo seja o único no interior de um eletroduto aparente, que a temperatura ambiente seja de 30°C e que sejam utilizados condutores Cu/PVC. A tabela da NBR que nos fornece a informação pretendida é a 31 — mais exatamente, a coluna 6 da tabela 31, referente ao método de instalação B1, no qual se enquadra a linha elétrica do exemplo, e a dois condutores carregados (os fatores de correção por agrupamento e temperatura são iguais a 1, pelas hipóteses assumidas). Portanto, na tabela 31, coluna 6, a menor seção de condutor com capacidade de corrente maior ou igual a IB = 127 A é:

S = 50 mm2

Note-se que se o dimensionamento fosse realizado sem considerar a presença das harmônicas, mas tão-somente o valor da corrente fundamental (110 A), a seção dos condutores resultaria em

S = 35 mm2

Se isso viesse a acontecer — 35 mm2ao invés de 50 mm2—, nas condições imaginadas para o circuito, os condutores iriam operar em regime de sobrecarga, com a conseqüente redução de sua vida útil e com o eventual risco desse sobreaquecimento provocar um futuro dano à integridade da instalação.

Circuito 3F+N Sejam agora as mesmas correntes do exemplo anterior, porém percorrendo um circuito com três fases e neutro (figura 2). Vamos supor, também, que as correntes nas fases sejam exatamente iguais, tanto a fundamental quanto as harmônicas. Quanto à corrente de projeto IB que percorre as fases, não há nenhuma diferença no cálculo em relação ao exemplo anterior e seu valor eficaz é 127 A. A grande diferença refere-se à corrente que irá circular pelo condutor neutro (IN). Como mencionado e como demonstrado no boxe, as correntes de ordem 3 e seus múltiplos que circulam pelas fases somam-se algebricamente no neutro. No exemplo, não temos múltiplos, apenas a corrente de terceira ordem, que vale 57 A. Desse modo, a corrente eficaz que percorrerá o neutro será:

IN = 57 + 57 + 57 = 171 A

Note-se que esse valor é 35% (171/127) maior que a corrente de fase e 55% (171/110) maior que a corrente fundamental. Vejamos como fica o dimensionamento dos condutores nesse caso, mantendo as mesmas condições de instalação já descritas para o circuito 2F. Um circuito 3F + N com corrente circulando no neutro corresponde, portanto, a quatro condutores carregados. Como a tabela 31 da NBR 5410 só nós fornece (diretamente) valores de capacidade de corrente para dois ou três condutores carregados, o expediente para usá-la, como indica a norma, é supor que os condutores a serem dimensionados compõem dois circuitos de dois condutores carregados cada. Assim, temos um fator de correção por agrupamento igual a 0,8 (tabela 35) e, conseqüentemente, uma corrente fictícia de projeto

IB’ = 127/0,8 = 159 A

Entrando com esse valor na tabela 31, coluna 6, vemos que a seção dos condutores de fase será

SF = 70 mm2

No caso do condutor neutro, a corrente de projeto a considerar será IN = 171 A, o que resulta em uma corrente fictícia de projeto de

171/0,8 = 214 A,

a qual nos leva a uma seção do condutor neutro de

SN = 95 mm2

Se o dimensionamento fosse realizado sem considerar a presença das harmônicas, mas tão-somente o valor da corrente fundamental (110 A), a seção dos condutores de fase seria também aquela apurada no caso do circuito 2F, isto é, S = 35 mm2. Só que, como se trata de circuito 2F + N, a tendência — seguindo-se o procedimento antigo — seria adotar uma seção reduzida de neutro. Mais exatamente, uma seção de 25 mm2(que é a seção de neutro admitida, na tabela 44 da NBR 5410, quando se tem condutor de fase de 35 mm2). No entanto, o procedimento correto nos aponta uma seção de

![Figura vetorial da página 4](figura-vetorial-p4-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – Exemplo de circuito 3F + N com presença de harmônicas

<!-- pagina-origem: 5 -->

Hoje, muitas instalações têm sido vítimas de “fenômenos” aparentemente inexplicáveis, como o aquecimento excessivo de transformadores que alimentam cargas até mesmo inferiores à sua potência nominal, o disparo de disjuntores com correntes bem menores que a corrente nominal, assim como o excessivo aquecimento de condutores neutros de circuitos razoavelmente equilibrados. O problema se deve às harmônicas, cuja existência, até alguns anos atrás, praticamente não afetava o funcionamento normal das instalações. Elas constituem um subproduto da eletrônica moderna e manifestam-se especialmente onde existe uma quantidade considerável de computadores, acionamentos de velocidade regulável e outras cargas “não-lineares”, cuja utilização vem se expandindo rapidamente nos últimos anos. As cargas, digamos, “tradicionais” das instalações, isto é, motores, iluminação incandescente e equipamentos de aquecimento resistivo são lineares.A corrente nessas cargas é sempre um reflexo da tensão: para tensão senoidal, teremos corrente senoidal. Nas chamadas cargas não-lineares, ao contrário, as correntes não são senoidais e, mesmo que a tensão (em vazio) da fonte tenha a forma de uma senóide pura, ela será distorcida e perderá a forma senoidal. Enquanto as cargas tradicionais (praticamente lineares) dão origem a tensões e correntes com pouquíssima ou nenhuma distorção, isto é, praticamente sem harmônicas, as cargas não-lineares podem introduzir um nível bastante significativo de harmônicas nos circuitos que as alimentam. Via de regra, as ondas de forma não-senoidal que aparecem nos sistemas de potência podem ser decompostas em uma onda (senóide) fundamental e em um número finito de harmônicas de ordem par e ímpar. Tomemos um circuito trifásico a quatro condutores que alimenta diversas cargas monofásicas ligadas entre cada fase e o neutro. As correntes circulam em cada condutor fase e retornam pelo neutro comum. As três correntes de linha de 60 Hz estão defasadas de 120° e, para cargas lineares equilibradas

neutro superior à dos condutores de fase. Embora possa parecer estranho, na era das harmônicas a especificação dos condutores do circuito-exemplo seria essa mesma:

3 × 70 mm2+ 1 × 95 mm2.

À guisa de resumo, a tabela I destaca a grande diferença entre os dimensionamentos considerando ou não a presença de harmônicas.

### A ameaça das harmônicas

nas três fases,são iguais.Quando retornam pelo neutro se cancelam e temos, então, uma corrente nula no condutor neutro. Tomemos agora um circuito trifásico a quatro condutores alimentando cargas não-lineares, ligadas entre cada fase e neutro, equilibradas nas três fases. As correntes fundamentais se anulam no neutro. As correntes de 2ª harmônica, iguais e defasadas de 120°, também se cancelam no neutro, como mostra a figura 1A. O mesmo ocorre com todos as harmônicas de ordem par. As correntes de 3aharmônica, no entanto, são iguais e estão em fase, aparecendo superpostas na figura 1B. A corrente de 3ª harmônica no neutro é, portanto, a soma das correntes de 3ª harmônica nas linhas, ou seja, é o triplo da corrente em cada linha. O mesmo ocorre com todos as harmônicas de ordem ímpar múltiplas de 3 (9ª, 15ª, 21ª, etc.). As demais harmônicas de ordem ímpar (5ª, 7ª, 11ª, etc.) têm seus respectivos valores iguais nas linhas, porém não estão em fase, o que faz com que as respectivas correntes no neutro sejam maiores do que a corrente numa linha e inferiores ao triplo da corrente em cada linha.

![Figura vetorial da página 5](figura-vetorial-p5-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Circuito trifásico a quatro condutores com cargas não-lineares equilibradas nas três fases: (A) correntes fundamental e de 2ª harmônica; (B) correntes fundamental e de 3ª harmônica

### Método da NBR 5410

Ainda considerando o circuito-exemplo 3F + N, vejamos como ele seria dimensionado seguindo-se o exposto no artigo 6.2.6.4 da NBR 5410. Esse artigo, intitulado Determinação das seções nominais de circuitos trifásicos considerando a presença de harmônicas, apresenta um método para esse fim — que, o texto esclarece, aplica-se a circuitos trifásicos a quatro condutores nos quais “o desequilíbrio entre fases é inferior a

<!-- pagina-origem: 6 -->

50% e onde é prevista a presença de correntes harmônicas de 3ª ordem nos condutores de fase, admitindo-se que os quatro condutores sejam de mesmo material e tenham a mesma seção nominal”. Uma tabela incluída no artigo (tabela 45 na norma, aqui reproduzida como tabela II) indica “os fatores de correção que, aplicados às capacidades de correção relativas a três condutores carregados (tabelas 31, 32, 33 e 34), fornecem os valores correspondentes a quatro condutores carregados, quando a corrente no condutor neutro é devida a harmônicas.” Traduzindo para a prática o uso dos fatores dados na tabela, o próprio artigo da NBR 5410 mencionado estipula que o valor de corrente adotado na determinação da seção dos quatro condutores do circuito, utilizando a tabela 31, 32, 33 ou 34 (colunas de três condutores carregados), deve ser:

I B = I f

se a escolha da seção for conduzida com base na corrente de fase (vale dizer, se usados os fatores de correção apresentados à esquerda, na tabela II); ou então

p 1 = × × × I I 3 B f 100

se a escolha da seção for conduzida com base na corrente de neutro (na tabela II, fatores de correção à direita), sendo IB a corrente de projeto do circuito, p a porcentagem de harmônica de 3ª ordem prevista (primeira coluna da tabela II) e f o fator de correção (segunda ou terceira coluna da tabela II, dependendo do caso). Assim, para aplicar ao circuito 3F + N do nosso exemplo o procedimento apresentado na norma, precisamos primeiramente determinar p, isto é, a porcentagem de terceira harmônica presente na corrente de fase. No nosso exemplo, a corrente total de fase (valor eficaz) é igual a 127 A e a corrente de terceira harmônica vale 57 A, o que resulta em

p = (57/127) × 100% = 45%

Para esse valor de p, a tabela II (tabela 45 da norma) nos fornece um fator de correção

f = 0,86 sendo a escolha da seção, conseqüentemente, com base na corrente de neutro. Assim, o cálculo de I fica:

1 45 = × × × = 127 I 3 199 A,0 86 100

Entrando com 199 A na tabela 31, método B1, coluna de três condutores carregados (coluna 7), verifica-se que a menor seção de condutor compatível é a de 95 mm2— mesmo valor obtido pelo outro modo de calcular indicado. Observe-se, porém, que o texto do artigo 6.2.6.4, como transcrito acima, associa claramente o uso do procedimento à condição de que os quatro condutores do circuito (3F + N) sejam de mesmo material e tenham a mesma seção nominal. Na prática, isso significa que esse circuito seria especificado, de acordo com a NBR 5410, como

3 × 95 mm2+ 1× 95 mm2.

## Relatório de extração

- Páginas processadas: 6.
- Figuras/diagramas referenciados: 3.
- Tabelas em grade reconstruídas em Markdown: 3.
- Páginas com elementos vetoriais complexos sinalizados pelo diagnóstico: 0.
- Modo: verbatim-limpo; cabeçalhos, rodapés, copyright recorrente e números de página foram removidos.
- A hierarquia foi inferida conservadoramente por tamanho/peso da fonte e posição; descrições geradas estão explicitamente marcadas.
