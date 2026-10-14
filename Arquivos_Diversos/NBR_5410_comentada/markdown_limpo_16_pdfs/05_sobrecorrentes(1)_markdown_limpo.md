---
titulo: 'Proteção contra sobrecorrentes'
arquivo_origem: 05_sobrecorrentes(1).pdf
formato_origem: pdf
autor: 'user'
data: 'D:20020515150755-03''00'''
idioma: pt-BR
paginas: 28
mapa_de_secoes:
  - 'P R O T E Ç Ã O C O N T R A S O B R E C O R R E N T E S'
  - 'Normalização IEC de disjuntores BT'
  - 'Características nominais'
  - 'Tipos e normalização de dispositivos fusíveis'
  - 'A ação limitadora de corrente'
  - 'Características tempo-corrente'
  - 'Equacionamento da proteção contra sobrecargas'
  - 'Equacionamento da proteção contra curtos-circuitos'
  - 'Dispositivos garantindo apenas proteção contra curtos-circuitos'
  - 'Determinação da corrente de curto-circuito presumida'
  - 'Exemplo de aplicação'
  - 'Integral de Joule: coordenando condutores e dispositivos de proteção'
  - 'Integral de Joule de condutores'
  - 'Integral de Joule dos dispositivos de proteção'
  - 'Como construir as curvas I2t dos condutores'
  - 'Corrente de curto mínima: atenção ao comprimento do circuito'
  - 'A origem das tabelas'
  - 'Um “mesmo” dispositivo, por que exigências distintas?'
  - 'Queda de tensão pode prevalecer'
  - 'Proteção de cabos em paralelo'
  - 'Proteção única e proteção individual'
notas_de_extracao: 'Modo verbatim-limpo; 17 figuras/diagramas referenciados; páginas com vetores preservadas por referência visual.'
---

# Proteção contra sobrecorrentes

<!-- pagina-origem: 1 -->

### P R O T E Ç Ã O C O N T R A S O B R E C O R R E N T E S

Normalização IEC de disjuntores BT........................................................140

Tipos e normalização de dispositivos fusíveis........................................145

Equacionamento da proteção contra sobrecargas.................................151

Equacionamento da proteção contra curtos-circuitos............................155

Determinação da corrente de curto-circuito presumida........................163

Integral de Joule: coordenando condutores e dispositivos de proteção..169

Corrente de curto mínima: atenção ao comprimento do circuito..........175

Proteção de cabos em paralelo..............................................................181

<!-- pagina-origem: 2 -->

## Normalização IEC de disjuntores BT

O s disjuntores de baixa tensão são hoje cobertos por uma completa normalização internacional (tabela I), liderada pela IEC 60947-2 — no Brasil, NBR IEC 60947-2. Esta norma aplica-se a todos os disjuntores cujos contatos principais são destinados à ligação a circuitos cuja tensão nominal não ultrapassa 1000 VCA ou 1500 VCC, quaisquer que sejam as correntes nominais, os métodos de construção e a utilização prevista. A IEC 60898 (no Brasil, NBR IEC 60898) trata especificamente dos disjuntores de tensão nominal inferior ou igual a 440 V, corrente nominal inferior ou igual a 125 A, para uso em circuitos CA de instalações domésticas e análogas, concebidos para uso por pessoas não advertidas ou qualificadas e para não exigir manutenção (o que não quer dizer que eles não possam ser usados em instalações industriais, claro). É o domínio, por excelência, dos minidisjuntores (ou, na denominação internacional, MCB, de miniature circuit-breakers). A IEC 60898 não se aplica aos disjuntores destinados à proteção de motores e àqueles cuja regulagem de corrente seja acessível ao usuário. As prescrições relativas aos disjuntores para equipamentos constam da IEC 60934, enquanto os disjuntores utilizados como dispositivos de partida de motores são tratados, pelo menos parcialmente, pela IEC 60947-4. Os disjuntores, no exercício da função principal de proteção contra sobrecorrentes, operam através de disparadores que podem ser térmicos, magnéticos e eletrônicos. Os disjuntores mais tradicionais, para uso geral, são equipados com disparadores térmicos, que atuam na ocorrência de sobrecorrentes moderadas (tipicamente correntes de sobrecarga), e disparadores magnéticos, para sobrecorrentes elevadas (tipicamente correntes de curto-circuito). Daí o nome disjuntores termomagnéticos. O disparador térmico típico é constituído de uma lâmina bimetálica que se curva sob ação do calor produzido pela passagem da corrente. Essa deformação temporária da lâmina, devido às diferentes dilatações dos dois metais que a compõem, provoca, em última análise, a abertura do disjuntor. O disparador térmico bimetálico apresenta característica de atuação a tempo inverso, isto é, o disparo se dá em um tempo tanto mais curto quanto mais elevada for a (sobre)corrente. Alguns disparadores térmicos possuem uma faixa de corrente de ajustagem. Também existem disparadores térmicos com compensação de temperatura. Já o disparador magnético é constituído por uma bobina (eletroímã) que atrai um peça articulada (armadura) quando a corrente atinge um certo valor. Esse deslocamento da armadura provoca, através de acoplamentos mecânicos, a abertura dos contatos principais do disjuntor. Há disjuntores que têm o disparo magnético ajustável. A figura 1 mostra a característica tempo–corrente típica de um disjuntor termomagnético, evidenciando a atuação do disparador térmico de sobrecarga (a tempo inverso) e do disparador magnético (instantâneo). O disparador eletrônico, por fim, compreende sensores de corrente, uma eletrônica de processamento dos sinais e de comando e atuadores. Os sensores de corrente são constituídos de um circuito magnético e elaboram a imagem da corrente medida. A eletrônica processa as informações e, dependendo do valor da corrente medida, determina o disparo do disjuntor no tempo previsto. A característica tempo–corrente dos disparadores eletrônicos apresenta três zonas de atuação (figura 2): – a zona de proteção térmica de longo retardo, que repre-

![Figura vetorial da página 2](figura-vetorial-p2-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Característica tempo-corrente típica de disjuntor termomagnético

<!-- pagina-origem: 3 -->

senta um modelamento das características de elevação de temperatura dos condutores; – a zona de curto retardo, que assegura a proteção contra correntes de falta distantes. O curto retardo, que é compatível com os limites de elevação de temperatura dos condutores, possibilita seletividade com dispositivos de proteção a montante; – a zona de atuação instantânea, que é a da proteção contra curtos-circuitos elevados e imediatamente a jusante do disjuntor.

![Figura vetorial da página 3](figura-vetorial-p3-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – Característica tempo-corrente de um disparador eletrônico. Ir pode ser ajustado, tipicamente, entre 0,4 e 1 vez a corrente nominal; e IM entre 2 e 10 vezes Ir.

### Características nominais

Tensões nominais – Os disjuntores são caracterizados pela tensão nominal de operação, ou tensão nominal de serviço (Ue) e pela tensão nominal de isolamento (Ui). Nos catálogos dos fabricantes, freqüentemente indica-se apenas a primeira, chamada simplesmente de tensão nominal (Un = Ue). Geralmente, Ui é o maior valor admissível de Ue.

Correntes nominais – De acordo com a IEC 60947-2, a corrente nominal (In) de um disjuntor é a corrente ininterrupta nominal (Iu) e tem o mesmo valor da corrente térmica convencional ao ar livre (Ith), isto é, In = Iu = Ith. A norma não padroniza valores de In. A IEC 60898, mais explícita, define corrente nominal como a corrente que o disjuntor pode suportar em regime ininterrupto, a uma temperatura de referência especificada. A norma considera 30°C como temperatura ambiente de referência e indica os seguintes valores preferenciais de In: 6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100 e 125 A. Via de regra, os fabricantes de disjuntores termomagnéticos indicam, além das correntes nominais na temperatura de referência, valores de In correspondentes a outras temperaturas ou então os fatores a aplicar para temperaturas diferentes das de referência.

Correntes convencionais – A IEC 60947-2 define a corrente convencional de atuação (I2) e a corrente convencional de não-atuação (Int) em função da corrente de ajustagem Ir. Já a IEC 60898 — que, como vimos, aplica-se a disjuntores cuja regulagem de corrente não é acessível — define ambas as grandezas em função da corrente nominal. A tabela II indica os valores definidos em ambas as normas.

Disparo instantâneo – A IEC 60898 define, para o disparo instantâneo, em geral magnético, as faixas de atuação B, C e D ilustradas na figura 3: – B: de 3 In a 5 In; – C: de 5 In a 10 In; – D: de 10 In a 20 In. A fixação das três faixas, através de valores-limite, não significa, porém, que o fabricante deva observá-los estritamente, particularmente no que se refere ao limite superior. Em outras palavras, determinado fabricante pode oferecer um disjuntor com característica D, mas com faixa de atuação de 10 In a, digamos, 15 In. A IEC 60947-2, por sua vez, refere-se a “abertura em condição de curto-circuito” e prescreve apenas que o disparador correspondente deve provocar a abertura do disjuntor com uma precisão de ±20% em torno do valor ajustado/calibrado.

![Figura vetorial da página 3](figura-vetorial-p3-2)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 3 – Características tempo-corrente de minidisjuntores normalizadas pela IEC 60898

<!-- pagina-origem: 4 -->

Tab. I – As diferentes categorias de disjuntores BT

Correntes Categoria Características Normas nominais Minidisjuntores – IEC 60898 0,5 a 125 A • Construção modular, montagem em Disjuntores para trilho (quando padrão DIN) instalações domés- • Disparador não ajustável ticas e análogas

<!-- tabela-p4-1 -->
| Construção consagrada, e tecnologia
em constante aperfeiçoamento. Ampla
variedade de disparadores e
acessórios
Ao lado da tradicional construção
aberta, versões em invólucros
isolantes. Unidades de disparo versáteis e com amplos recursos, incluindo comunicação | IEC 60947-2 | 40 a 3200 A
630 a 6300 A |
| --- | --- | --- |
| Características apropriadas às dos
motores. Podem ser usados como dispositivo de partida. | IEC 60947-2
IEC 60947-4.1 | 0,1 a 63 A |

Disjuntores para uso geral: • Disjuntores em caixa moldada

• Disjuntores de potência

Disjuntor-motor

0,1 a 125 A Disjuntores para Dispositivos simples, geralmente pro- IEC 60934 equipamentos porcionando proteção contra sobrecargas mas não contra curtos-circuitos

Capacidades de interrupção – A IEC 60947-2 define capacidade limite de interrupção (de curto-circuito) Icu e capacidade de interrupção (de curto-circuito) em serviço Ics. Já a IEC 60898 refere-se simplesmente a capacidade de interrupção nominal (Icn), igual à capacidade limite de interrupção, isto é Icn = Icu, fixando os valores de 1,5, 3, 4,5, 6, 10, 15, 20 e 25 kA. A capacidade de interrupção em serviço é definida em função de Icn, sendo fixados os seguintes valores: – para Icn ≤6 kA, Ics = Icn; – para 6 < Icn ≤10 kA, Ics = 0,75 Icn (mínimo de 6 kA); – para Icn > 10 kA, Ics = 0,5 Icn (mínimo de 7,5 kA). São as características Icu e Icn que devem ser comparadas, no projeto da instalação, com o valor da corrente de curto-circuito presumida no ponto de instalação do disjuntor [Ver artigo “Equacionamento da proteção contra curtos-circuitos]. Assim, Icu ou Icn (do disjuntor) ≥Ik presumida (do sistema) Icu e Icn representam, enfim, a máxima corrente de curto-circuito que um disjuntor é capaz de interromper. Mas no cálculo da corrente de curto-circuito presumida Ik geralmente são assumidas, em favor da segurança, condições e circunstâncias que correspondem ao pior caso. O resultado é que quando um curto-circuito ocorre, seu valor na realidade é bem inferior ao da corrente presumida Ik. Por outro lado, é importante que essas correntes de curto menores, mas com maior probabilidade de ocorrência, sejam interrompidas em perfeitas condições, de forma que o retorno ao serviço, após a eliminação da falta, seja rápido e seguro para toda a instalação. Aplicações É essa a razão da capacidade de interrupção em serviço Ics, cu- Proteção de circuitos terja comprovação as normas assim minais em instalações com tensão de no máxiespecificam: mo 440 VCA – o disjuntor deve realizar três interrupções sucessivas de Ics; Proteção de circuitos – a capacidade de o disjuntor principais, de distribuição preencher todas as suas funções é e terminais então verificada por uma série de Proteção do quadro geral medições (elevação de temperatu- (QGBT) ra, ensaio de tensão aplicada, verificação da atuação dos disparadores, etc.). Circuitos de alimentação de motores, máquinas e Todas essas exigências confiprocessos industriais guram Ics como uma característi- Destinados a ser incorca de desempenho, uma indicação porados a equipamentos de utilização (eletrododa capacidade do disjuntor em gamésticos, bombas, etc.) rantir um funcionamento completamente normal mesmo após ter interrompido correntes de curto-circuito. Embora a norma de instalações não inclua regras envolvendo especificamente a característica Ics, é importante e conveniente, a fim de garantir melhor continuidade de serviço, escolher disjuntores cujo desempenho Ics seja tal que

Ics > Ik provável.

V e j a m o s Tab. II – Correntes convencionais de dois exemplos não-atuação (Int), de atuação (I2) e genéricos, para tempo convencional para disjuntores BT melhor ilustrar essa recomen- IEC 60947-2 IEC 60898 Tempo In(*) convencional dação. (A) Int I2 I2 Int (h) No caso de um disjuntor ≤63 1 1,05 1,30 1,13 1,45 com função típi- > 63 2 ca de chave geral, em um qua- (*) In é corrente de ajustagem (IEC 60947-2) ou corrente nominal (IEC 60898) dro ou painel de distribuição, e cujo campo de proteção é geralmente limitado ao próprio quadro ou painel, as correntes de curto-circuito que caberá ao dispositivo eliminar serão apenas ligeiramente inferiores ao valor teórico da corrente de curto-circuito presumida. Assim, deve ser selecionado um disjuntor cuja Ics seja próxima de ou igual a Icu, isto é,

Ics = 100% Icu

<!-- pagina-origem: 5 -->

Já no caso de disjuntores de saída de quadros ou painéis, que basicamente protegem circuitos entre quadros (circuitos de distribuição), ou entre quadro e equipamento de utilização (circuito terminal), os curtos-circuitos prováveis resultarão em correntes bastante inferiores à Ik presumida no ponto de instalação do dispositivo, uma vez que as faltas quase sempre envolverão apenas uma ou duas fases e ocorrerão na extremidade final do circuito protegido. Assim, a corrente de curto-circuito provável será – geralmente inferior a 25% da Ik presumida na origem do circuito; – e, na quase totalidade dos casos, inferior a 50% da Ik presumida. Logo, dependendo das condições reais da instalação e, portanto, do valor da corrente de curto-circuito provável (a que ocorreria na extremidade final da linha protegida), o projetista poderia adotar, preservando o bom funcionamento e a vida útil da instalação e componentes, disjuntores de saída de quadros com Ics de 25% ou, melhor ainda, 50% (Ics = 50% Icu). Convém lembrar ou repetir que isso não tem nada a ver com a regra básica da proteção contra curtos-circuitos, contida na norma de instalações, que exige do disjuntor uma capacidade de interrupção no mínimo igual à corrente de curto-circuito presumida no ponto em que for instalado. Com efeito, e como dito inicialmente, em qualquer dos dois exemplos genéricos ilustrados acima o disjuntor deve ter

Icu > Ik presumida.

## Tipos e normalização de dispositivos fusíveis

Embora na linguagem do dia-a-dia o nome usado seja “fusível”, simplesmente, convém inicialmente lembrar que, “fusível” é apenas parte do que as normas chamam, apropriadamente, de “dispositivo fusível”. Pois, de fato, no caso mais geral um dispositivo fusível é constituído de base, porta-fusível, fusível, indicador e, eventualmente, percussor. A base é a parte fixa do dispositivo, com contatos e terminais. O porta-fusível é a parte móvel do dispositivo, onde é instalado o fusível – sendo este, por sua vez, a parte substituível, ou consumível, que deve ser trocada sempre que o dispositivo atuar. O fusível contém o elemento fusível, que é o componente que deve fundir quando percorrido por uma corrente especificada, por um tempo especificado. O indicador é a parte que dá uma indicação visível de que o dispositivo fusível operou e o percussor um dispositivo mecânico que, quando da operação do fusível, libera a energia necessária para acionar outros dispositivos ou indicadores, ou para fazer um intertravamento. A normalização internacional (IEC 60269) e nacional (NBRs 11840 a 11849) define três tipos de dispositivos fusíveis, todos limitadores de corrente (ver boxe “A ação limitadora de corrente”): gG, para proteção de circuitos contra correntes de sobrecarga e correntes de curto-circuito; gM e aM, que proporcionam apenas proteção contra correntes de curto-circuito, sendo por isso mesmo indicados tipicamente para circuitos de motores (onde a proteção contra sobrecargas geralmente é feita pelo relé térmico associado ao contator) ou como proteção de retaguarda (para completar a insuficiente capacidade de interrupção de um disjuntor, por exemplo). Outra distinção importante, e que delimita o campo de aplicação das normas que tratam do produto, é a do tipo de instalação a que o dispositivo fusível se destina. Assim, temos os dispositivos fusíveis destinados a uso doméstico ou • similar, também designados “para uso por pessoas não qualificadas”. Tratados mais particularmente na norma IEC 60269-3, são via de regra tipo gG e com correntes nominais até 100 A; e os dispositivos fusíveis para uso industrial, ou “para uso • por pessoas autorizadas”, enfocados nas normas IEC 60269-1 e 60269-2. Podem ser tipo gG, gM ou aM.

![Figura vetorial da página 5](figura-vetorial-p5-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 - Zonas tempo-corrente para fusíveis gG de 4, 10, 20, 32, 63 e 100 A

<!-- pagina-origem: 6 -->

### A ação limitadora de corrente

Todos os três tipos de dispositivos fusíveis previstos na normalização IEC (gG, gM e aM) são limitadores de corrente. Isso significa que, durante e em conseqüência da fusão do elemento fusível dentro de uma faixa de correntes especificadas, eles limitam a corrente a um valor significativamente mais baixo que o valor de crista da corrente presumida (figura B1). Fig. B1 – Limitação da corrente pelo fusível Como conseqüência, essa limitação da corrente reduz, também significativamente, as solicitações térmicas e dinâmicas que de outra forma sobreviriam — minimizando assim os danos no ponto de ocorrência da falta. A capacidade de interrupção nominal do fusível, portanto, é baseada no valor eficaz da componente CA da corrente de falta presumida. Vale lembrar que as correntes de curto-circuito contêm inicialmente componentes CC cuja magnitude e duração dependem da relação XL/R do percurso da corrente de falta. Próximo à fonte (transformador), a relação Icrista/Ief da componente CA,imediatamente após o instante da da corrente de falta presumida

As principais diferenças entre os dispositivos fusíveis “industriais” e “domésticos” referem-se às tensões nominais, à faixa de correntes nominais (que vai além de 1000 A nos industriais, o que faz do tamanho uma outra diferença importante entre as duas categorias), à capacidade de interrupção e às exigências impostas pela proteção contra choques, isto é, contra o risco de contatos acidentais com partes vivas — naturalmente, exigências falta, pode ser tão alta quanto 2,5 (relação, aliás, normalizada pela IEC, como indicado na figura B2). Já nos trechos finais da distribuição elétrica (extremidades de circuitos terminais, por exemplo), XL é pequena comparada a R e, assim, a relação Icrista/Ief cai para cerca de 1,41. A ação limitadora do valor de crista da corrente se manifesta a partir de determinado nível do valor eficaz da componente CA da corrente de falta presumida. Por exemplo, no gráfico da figura o fusível de 100 A começará a limitar o valor de crista quando a corrente de falta presumida (valor eficaz) atingir 2 kA (ponto a). No caso de uma corrente presumida eficaz de 20 kA, o mesmo fusível irá limitar o valor de crista a 10 kA (ponto b). Sem o fusível limitador de corrente, o valor de crista poderia atingir, neste caso particular, 50 kA (ponto c). Por outro lado, nos trechos finais da distribuição, como mencionado, R é bem maior que XL e os níveis de curto-circuito são geralmente baixos — talvez mesmo insuficientes para deflagrar a ação limitadora. Além disso, neste caso o efeito dos transitórios CC sobre a magnitude do valor de crista da corrente é insignificante.

maiores no caso dos dispositivos “domésticos”. Do ponto de vista da forma construtiva, os fusíveis “industriais” são disponíveis, tipicamente: • com contatos cilíndricos (usualmente chamados de “cartuchos tipo industrial”); • com contatos tipo faca (correspondendo ao tipo conhecido como NH); e • com contatos aparafusados. Fig. B2 – Ação limitadora dos fusíveis: valor de crista limitado vs valores eficazes da componente CA

<!-- pagina-origem: 7 -->

![Figura vetorial da página 7](figura-vetorial-p7-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – Zonas de fusão e de não-fusão para fusíveis gG e gM

Os fusíveis “domésticos”, ou — apelando para uma denominação popular mais apropriada quando se trata de contrapor algo àquilo que é destinado a uso industrial

- fusíveis “prediais”, por sua vez, são disponíveis, tipicamente, nos formatos: • cartucho; e • tipo D (também referidos comumente como “diazed”, que no entanto é marca de um fabricante). Evidentemente, um dispositivo fusível “predial” pode ser utilizado em uma instalação industrial; ou mesmo deve, se essa instalação, por exemplo, não for servida permanentemente por pessoas BA4 ou BA5. Mas um dispositivo fusível “industrial”, ou para uso por pessoas autorizadas, não pode, em absoluto, ser utilizado numa instalação residencial ou predial. Vale notar que os fusíveis cartucho (melhor dizendo, com formato cartucho) cobertos pelas normas aqui citadas nada têm a ver com os antigos fusíveis cartucho. Da mesma forma, não é por serem roscáveis que dispositivos fusíveis conforme as normas mencionadas, como os do tipo D, se confundem com os antigos fusíveis rolha.

### Características tempo-corrente

A figura 1 traz, a título de exemplo, as zonas tempo–corrente fixadas pela normalização para alguns fusíveis gG. Com efeito, as normas conceituam e padronizam dois parâmetros fundamentais na composição dessas zonas tempo–corrente (delimitadas, como se vê na figura 2, pela curva tempo mínimo de fusão–corrente, à esquerda, e pela curva tempo máximo de interrupção–corrente, à direita): • a corrente convencional de não–fusão Inf, que é o valor da corrente que o elemento fusível pode suportar, durante um tempo especificado (tempo convencional), sem se fundir; e • a corrente convencional de fusão I2, que é o valor da corrente que assegura a fusão do elemento fusível antes de decorrido o tempo convencional. A tabela I reproduz os valores de Inf e de I2, bem como os tempos convencionais respectivos, normalizados pela IEC 60269-1 e IEC 60269-2, em função da corrente nominal (In) do fusível. Assim, por exemplo, um fusível gG de 32 A conduzindo uma corrente equivalente a 1,25 In (ou seja, 40 A), não deve fundir antes de 1 h. Mas se circular pelo mesmo fusível uma corrente correspondente a 1,6 In (ou seja, 52,1 A), ele deve fundir em 1 h ou menos. A mesma tabela — de Inf, I2 e respectivos tempos convencionais — é aplicável também aos fusíveis gM. Mas, nesse caso, os valores de Inf e de I2 (vale dizer, a característica tempo–corrente) não estão atrelados à grandeza corrente nominal, mas sim ao que a normalização do produto chama de Ich — assim mesmo, abreviadamente, sem denominação por extenso. Explica-se. Os dispositivos fusíveis gM são caracterizados, na verdade, por dois valores de corrente de referência: o primeiro, In, representa a corrente nominal do fusível e do respectivo porta-fusível (isto é, das respectivas partes condutoras); o segundo, Ich (sendo Ich > In), refere-se à característica tempo–corrente. Trocando em miúdos: a identificação ou marcação de um fusível gM é feita por InMIch; assim, por exemplo, 16M32 indica um fusível gM cuja corrente permanente máxima (incluindo o porta–fusível) é de 16 A e cuja característica tempo–corrente é a mesma de um fusível gG de 32 A. Enfim, seria como ter um fusível gG que combinasse os contatos do modelo de 16 A com o elemento fusível do modelo de 32 A. Ou como ter, ainda, um fusível gG com corrente nominal (térmica, de regime permanente) de 16 A, mas com característica tempocorrente correspondente à de um gG de 32 A. Daí o tipo gM ser indicado para circuitos de motores, pois suporta transitoriamente as altas correntes de partida, sem se fundir,

<!-- pagina-origem: 8 -->

mas é dimensionado (entrando aí o lado econômico) para suportar permanentemente apenas a corrente de regime do motor. O dispositivo fusível tipo aM, por fim, tem a mesma aplicação do gM (circuitos de motores, assegurando apenas proteção contra correntes de curto–circuito) e é caracterizado, essencialmente, por uma corrente nominal (In) e pela zona tempo–corrente mostrada na figura 3. Em resumo, o elemento fusível de um fusível aM: a) não deve fundir para correntes menores ou iguais a K1In; b) pode fundir para correntes entre K1In e K2In, desde que o tempo de fusão seja maior que o indicado

![Figura vetorial da página 8](figura-vetorial-p8-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 3 – Características tempo-corrente dos fusíveis tipo aM na curva tempo mínimo de fusão-corrente; e c) deve fundir para correntes maiores que K2In, com os tempos correspondentes caindo dentro da zona tempo–corrente. Já a curva de sobrecarga também ilustrada na figura 3 indica, para as correntes superiores a In mas inferiores a K1In (ou seja, entre K0In e K1In), qual a duração máxima (da corrente) que o fusível suporta sem se deteriorar. Seria, enfim, a curva de suportabilidade térmica das partes condutoras do fusível. A curva de atuação do dispositivo que será responsável pela proteção contra sobrecargas deveria se situar, portanto, abaixo dessa curva, como também mostra a figura. Mas na prática essa verificação é quase sempre dispensável, uma vez que os fabricantes costumam dimensionar o fusível aM de forma compatível com o dispositivo de proteção contra sobrecargas que seria a ele associado, seja outro fusível ou um relé térmico, baseando-se para tanto na própria normalização dos dispositivos.

## Equacionamento da proteção contra sobrecargas

Uma exigência básica da proteção contra sobrecorrentes, seja a sobrecorrente uma sobrecarga ou um curto-circuito, é que haja coordenação entre o dispositivo encarregado dessa função e os condutores do circuito a ser protegido. Para garantir a proteção contra sobrecargas, conforme 5.3.3.2 da NBR 5410, a seleção do dispositivo de proteção deve satisfazer então às seguintes condições, representativas da exigência de coordenação com os condutores:

a) IB ≤In

b) In ≤Iz

c) I2 ≤1,45 Iz

onde: IB = corrente de projeto do circuito; In = corrente nominal do dispositivo de proteção (ou corrente de ajuste, para dispositivos ajustáveis); Iz = capacidade de condução de corrente dos condutores; e I2 = corrente convencional de atuação, para disjuntores, ou corrente convencional de fusão, para fusíveis. Analisemos um pouco mais detalhadamente cada um desses termos. A determinação da capacidade de condução de corrente dos condutores Iz é sempre calcada nas condições de instalação previstas no projeto. Assim, temos

Iz = f Îz

sendo Îz o valor de capacidade de condução de corrente dos condutores dado na tabela pertinente da NBR 5410 e f o fator ou o produto dos fatores de correção tabelados aplicáveis (temperatura ambiente, agrupamento e/ou, no caso de linha subterrânea, resistividade térmica do solo). In, a corrente nominal (ou de ajuste) do dispositivo de

<!-- pagina-origem: 9 -->

proteção a ser considerada, também leva em conta as condições reais da instalação. Por isso, o valor de In a ser considerado é:

In = f’ În

sendo În a corrente nominal (ou de ajuste) do dispositivo na temperatura de referência, ou temperatura de calibração (20, 30 ou 40°C), e f’ um dos, ou o produto dos, seguintes fatores dados pelos fabricantes: – fator de correção de temperatura ambiente (aplicável, claro, quando o dispositivo de proteção se encontrar submetido a uma temperatura diferente da de calibração); e – fator de agrupamento dos dispositivos. Quanto à condição c) da proteção contra sobrecargas, convém notar, primeiramente, que o termo 1,45 Iz corresponde à sobrecorrente que leva o condutor a uma temperatura de regime aproximadamente igual à temperatura limite de sobrecarga (100°C para isolação de PVC e 130°C para isolação de EPR ou XLPE). Já I2, corrente convencional de atuação do disjuntor, ou corrente convencional de fusão do fusível, pode ser expressa como múltiplo da corrente nominal do dispositivo. Assim,

I2 = α In

De fato, como mostram os dois artigos anteriores, “Normalização de disjuntores BT” [tabela II] e “Normalização de dispositivos fusíveis” [tabela I], – nos disjuntores conforme a NBR IEC 60898, I2 = 1,45 In

– nos disjuntores conforme a NBR IEC 60947-2, I2 = 1,3 In – nos disjuntores conforme a NBR 5361, I2 = 1,35 In – e, nos fusíveis gG (os que oferecem proteção contra sobrecargas) conforme a IEC 60269 (NBRs 11840 a 11849),

I2 = 1,6 In (para In > 16 A I2 = 1,9 In (para 4 < In ≤16 A I2 = 2,1 In (para In ≤4 A)

Substituindo I2, na condição c), pelos seus equivalentes das três normas, vem, no caso da NBR IEC 60898, • 1,45 In ≤1,45 Iz, ou seja, In ≤Iz;

Deslocamento da proteção

Em geral, o dispositivo responsável pela proteção contra sobrecargas é disposto na origem do circuito por ele protegido. Mas ele pode ser deslocado, no sentido a jusante de sua origem, se o circuito correspondente for protegido contra curtos-circuitos. Essa possibilidade de deslocamento da proteção contra sobrecargas, prevista em 5.7.4.1.1 da NBR 5410, está ilustrada na figura, que utiliza disjuntores como exemplo: responsável pela proteção contra sobrecargas da derivação OB, de seção S2, o disjuntor B pode ser deslocado da origem O do circuito para o ponto B se a corrente de curto-circuito mínima IkminB nos seus terminais for pelo menos igual à corrente de atuação instantânea (ou de curto retardo) IMA do disjuntor A.

<!-- pagina-origem: 10 -->

no caso da NBR IEC 60947-2, • 1,3 In ≤1,45 Iz, ou seja, In ≤1,11 Iz no caso da NBR 5361, • 1,35 In ≤1,45 Iz, ou seja In ≤1,07 Iz e, no caso da IEC 60269 (aqui já saltando a passagem • da substituição), In ≤0,91 Iz (para In > 16 A) In ≤0,76 Iz (para 4 < In ≤16 A) In ≤0,69 Iz (para In ≤4 A)

Ora, isso evidencia, no caso dos disjuntores, que a condição c) se torna dispensável — no caso de disjuntores conforme a NBR IEC 60898, porque se afigura como uma repetição da condição b); e, no caso de disjuntores conforme a NBR IEC 60947-2 e NBR 5361, porque a condição b) se mostra mais restritiva. Portanto, se o dispositivo de proteção for um disjuntor conforme a NBR IEC 60898, NBR IEC 60947-2 ou NBR 5361, a observância da regra da proteção contra sobrecargas fica reduzida às condições a) e b). Já no caso dos dispositivos fusíveis gG, todas as três possibilidades da condição c) avaliadas acima, quando comparadas com a condição b), mostram que a condição c) é mais restritiva — tornando dispensável, aqui, a condição b). Portanto, se o dispositivo de proteção for um dispositivo fusível gG conforme IEC 60269, a observância da regra da proteção contra sobrecargas fica reduzida às condições a) e c).

## Equacionamento da proteção contra curtos-circuitos

A proteção contra sobrecorrentes, como vários outros passos no projeto de uma instalação elétrica, consiste essencialmente em selecionar (ou, seguindo o jargão da engenharia, “dimensionar”) corretamente o dispositivo responsável pela função — no caso, um disjuntor, um dispositivo fusível ou uma combinação de ambos. E “corretamente” significa atender todas as regras que a norma de instalações elétricas impõe para que a proteção fique assegurada. Portanto, a essência das disposições da NBR 5410 quanto à proteção contra curtos-circuitos, como não poderia deixar de ser, gira em torno da seleção do dispositivo. E o aspecto essencial dessa seleção, por sua vez, como já salientado no artigo anterior, consiste em garantir que seja atendida a exigência de coordenação entre o dispositivo e os condutores do circuito a ser protegido — sem falar da coordenação com outros dispositivos, a montante ou a jusante, que pode ser também imperiosa. Em que pese a distinção adotada na norma (como, aliás, em todos os manuais de engenharia elétrica) entre sobrecorrentes classificáveis como de “sobrecarga” e sobrecorrentes tipicamente de “curto-circuito” — distinção que atende uma necessidade prática, real —, convém ter em mente que, afinal, todas são sobrecorrentes. Assim, e já que equacionar uma proteção é, essencialmente, selecionar o dispositivo respectivo, um bom começo para o exame da proteção contra curtos-circuitos é lembrar que a “seleção” do dispositivo, aqui, pode ser o mero prolongamento de um estudo que começou com a aplicação dos critérios referentes à proteção contra sobrecargas. Ou não. Essa é, por sinal, a abordagem presente na NBR 5410: o reconhecimento de que poderemos ter dispositivos preenchendo, simultaneamente, a proteção contra sobrecargas e contra curtos-circuitos; dispositivos preenchendo só a proteção contra sobrecargas; e, por fim, dispositivos preenchendo só a proteção contra curtos-circuitos. Assumir, como ponto de partida da seleção do dispositivo de proteção contra curtos-circuitos, as hipóteses de que esta seleção pode ser ou não o mero prosseguimento de um exame iniciado, antes, com a proteção contra sobrecargas, é provavelmente a forma mais clara de assimilar as exigências pertinentes da NBR 5410. Esta é a proposta do Guia EM para a abordagem do assunto, sintetizada no fluxograma da figura 1. O diagrama é o nosso plano de vôo para as orientações e comentários que se seguem. Por isso, ele não precisa ser entendido, por enquanto. Ele ficará claro quando as passagens que apresenta, à guisa de roteiro, forem descritas e explicadas, aqui e nos artigos seguintes. Depois, poderá servir como lembrete prático para o profissional. Assim, vamos começar com a pergunta que é o ponto de partida do diagrama: o dispositivo do qual se espera a proteção contra curtos-circuitos será também o responsável pela proteção contra sobrecargas? Provavelmente sim, certo? Afinal, essa é a situação mais geral. Os exemplos em que se faz necessária ou conveniente a existência de dispositivos distintos para a proteção contra sobrecargas e proteção contra curtos-circuitos, convenhamos, estão mais para casos particulares do que

<!-- pagina-origem: 11 -->

![Figura vetorial da página 11](figura-vetorial-p11-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Fluxograma da seleção do dispositivo de proteção contra curtos-circuitos

para o trivial. Se o mesmo dispositivo cumprirá as duas funções, ele já foi analisado sob o critério da proteção contra sobrecargas, tendo já atendido o que a NBR 5410 exige nesse particular, incluindo a questão do neutro(1)? E, ainda: o dispositivo segue as normas IEC aplicáveis ou outra norma equivalente? Se a resposta a essas duas perguntas for positiva, tudo o que o projetista precisa verificar, em matéria de proteção contra curtos-circuitos, resume-se, na grande maioria dos casos, à condição a) de 5.3.4.3 da NBR 5410: a de que o dispositivo deve possuir uma capacidade de interrupção (Icn) não inferior à corrente de curto-circuito presumida no ponto em que será instalado (Ik), isto é,

Icn ≥Ik

Isso embute, claro, uma tarefa da qual não é possível se esquivar, sejam quais forem as circunstâncias (um mesmo dispositivo, dispositivos distintos e todas as variantes imagináveis): apurar, por algum meio válido, o valor aproximado de Ik, com tanta maior precisão quanto maiores a complexidade da instalação, o vulto dos bens e dos riscos em jogo. [O artigo “Determinação da corrente de curto-

<!-- pagina-origem: 12 -->

circuito presumida” traz um método simplificado para essa determinação.] Se o dispositivo (o modelo específico cujas características nominais estão sendo consideradas) não apresenta uma capacidade de interrupção suficiente, há duas saídas: selecionar um outro modelo, com capacidade de inter- • rupção adequada (preservando-se, claro, o atendimento às condições da proteção contra sobrecargas, já que é este o nosso ponto de partida); ou “repassar” a exigência da capacidade de interrupção pa- • ra um dispositivo a montante, seguindo o esquema conhecido como “proteção de retaguarda” (back up), ou “proteção em série”. Este dispositivo de montante deverá, no mínimo, cobrir os flancos da proteção contra curtos-circuitos deixados pelo dispositivo de jusante — incluindo a capacidade de interrupção, claro —, podendo mesmo chegar à situação que caracteriza a outra hipótese inicial do nosso flu-

![Figura vetorial da página 12](figura-vetorial-p12-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – A corrente Ib, correspondente ao ponto em que as curvas I2t do condutor e do dispositivo de proteção se cruzam, deve ser superior à corrente de curto-circuito presumida Ik xograma: a de termos um dispositivo assegurando apenas proteção contra sobrecargas, o de jusante, e outro garantindo apenas a proteção contra curtos-circuitos, o de montante. Esta hipótese, em particular, é discutida mais adiante. Na prática, e levando ainda em conta a habitual exigência de seletividade, o recurso à “proteção de retaguarda” implica uma tal necessidade de coordenação, entre os dois dispositivos, que só os fabricantes têm condições de especificar. São as conhecidas tabelas de coordenação, que geralmente listam na horizontal as opções de dispositivo de jusante, na vertical as opções de dispositivo de montante e, no cruzamento das linhas e colunas, as indicações de quais combinações garantem coordenação. Retomando a seqüência do fluxograma, vamos admitir agora que o dispositivo tenha suficiente capacidade de interrupção mas não atenda uma especificação IEC (publicações IEC 60947 e 60898, para disjuntores, e IEC 60269, para dispositivos fusíveis) ou outra norma que conduza a resultados equivalentes. Neste caso, é necessário checar também a segunda exigência que a NBR 5410 impõe aos dispositivos encarregados da proteção contra curtos-circuitos (condição b) de 5.3.4.3), assim expressa: “a integral de Joule que o dispositivo deixa passar deve ser inferior ou igual à integral de Joule necessária para aquecer o condutor desde a temperatura máxima para serviço contínuo até a temperatura limite de curto-circuito.” Entenda-se: esta última exigência, bem como a relativa à capacidade de interrupção, constam da NBR 5410 e não devem ser ignoradas. Só que usando dispositivos conforme as normas IEC ou equivalentes na proteção contra sobrecargas, fica garantida, via de regra — pelas razões detalhadas mais adiante —, o atendimento da segunda exigência. E como se faz para saber se um dispositivo — seja porque não siga as normas em questão, seja porque não traga claramente indicada sua norma de referência ou, seja, ainda, pelo desejo puro e simples de verificação — preenche a segunda exigência, relativa à integral de Joule? Não é algo tão complicado quanto a redação da norma faz supor. Naturalmente, cabe ao fabricante do dispositivo prover essa informação. De que forma? Ele pode fornecer a informação sobre a integral de Joule (I2t) que o dispositivo de proteção deixa passar na forma de uma curva I2t = f(I), isto é, com os valores de I2t (em A2s) nas ordenadas e de I nas abcissas, plotada em escala bilogarítimica. Ele pode fornecer um único valor, o da I2t máxima que o dispositivo deixa passar entre a irrupção e a eliminação do curto-circuito. Ou pode, ainda, fornecer outro(s) valor(es) de I2t, além do máximo. [O artigo “Integral de Joule: coordenando condutores e dispositivos de proteção” traz explicações sobre o conceito da integral de Joule e sobre a utilização desse parâmetro na caracterização do comportamento de condutores e de dispositivos de proteção] O dado, na forma de curva ou número, deve ser então confrontado com a curva ou o número referente ao condutor utilizado no circuito que se quer proteger contra curtos-circuitos. Portanto, temos também uma curva I2t = f(I) e um I2t máximo de curto-circuito para cada tipo (cobre ou alumínio, isolação de PVC ou de EPR/XLPE) e seção (mm2) de condutor. Vejamos, primeiramente, a utilização das curvas, usando como ilustração a figura 2. A figura mostra a curva I2t do condutor (curva S), que lembra uma curva de 90° unindo duas assíntotas, uma vertical e outra horizontal; e a curva I2t do dispositivo de proteção (curva D, de um disjuntor).

<!-- pagina-origem: 13 -->

A verificação a ser feita, descrita no bloco F da figura 1, envolve a corrente Ib, correspondente ao cruzamento das curvas do condutor e do dispostivo de proteção. Para que a proteção contra curtos-circuitos seja assegurada, como exige o item 6.3.4.3 da norma, Ib deve ser superior ou, no mínimo, igual à corrente de curto-circuito presumida simétrica no ponto de instalação do dispositivo (Ik), isto é,

Ib ≥Ik

Portanto, se o Ik calculado ou estimado pelo projetista se situar à esquerda de Ib, a condição fica atendida. Vamos agora aproveitar a figura 2 — mas sobretudo como ferramenta de raciocínio — para discorrer sobre a situação em que o fabricante informa apenas um número, a I2t máxima que o dispositivo de proteção deixa passar. Como se vê na figura, os valores de I2t que o dispositivo deixa passar, na região que vai de Im a Icn (como se trata de um disjuntor, essa é a região que vai do limiar de atuação magnética, Im, à capacidade de interrupção nominal, Icn), variam do mínimo correspondente à ordenada de Im ao máximo correspondente à ordenada de Icn. Portanto, quando um fabricante informa um valor como sendo a máxima I2t que seu dispositivo deixa passar, deduz-se que ele está se referindo ao valor de I2t no ponto Icn, vale dizer, à I2t correspondente à capacidade de interrupção do disjuntor, e apurada nos ensaios de curto-circuito. Convém ressaltar, mais uma vez, que agora o projetista não dispõe da curva do dispositivo, só de um número: a I2t máxima que ele deixa passar. Como o projetista só tem um número e não sabe, portanto, onde a curva do dispositivo cruza com a curva do condutor, ele terá de necessariamente confrontar esse número com o valor assintótico horizontal da I2t do condutor. Esse trecho assintótico horizontal resulta da assunção de que, para solicitações de duração inferior a 5 s, o aquecimento do condutor é adiabático, isto é, sem troca de calor entre condutor e isolação. Como o aquecimento é considerado adiabático, a I2t suportável pelo condutor passa a ser representada por um valor constante — o que é intuitivo, pois trata-se do máximo que o condutor suporta sem troca térmica com o meio circundante. Esse valor, como informa a própria NBR 5410, é igual a k2S2, sendo S a seção do condutor, em mm2, e k uma constante também fornecida pela norma. São dados valores de k para cada tipo de condutor (cobre, alumínio, isolação em PVC, isolação em EPR ou XLPE). É possível, assim, calcular a I2t = k2S2 para todo tipo e seção de condutor. Portanto, na situação sob análise, o projetista nem precisa mesmo da curva I2t do condutor; basta fazer a conta de k2S2. E aí ele compara então os dois valores de I2t: o máximo que o dispositivo deixa passar, fornecido pelo fabricante, e o calculado para o condutor. Se o do dispositivo for inferior ao do condutor, a proteção está garantida. Perceba-se, porém, que neste caso a verificação é naturalmente conservadora. O conservadorismo (sem significado prático, como se verá, mas, de qualquer forma, inerente à abordagem) deriva do fato de se dispor apenas da I2t máxima que o dispositivo deixa passar e, por isso mesmo, necessariamente associada à capacidade de interrupção Icn do dispositivo (disjuntor). Note-se, no caso do disjuntor da figura 2, que se fosse fornecida apenas a sua I2t máxima, aquela associada a Icn, ele seria descartado, pois a I2t máxima (no ponto Icn, repita-se) é superior à k2S2do condutor (o valor assintótico horizontal da curva). Ao passo que o exame das curvas mostra que o disjuntor pode ser usado se Ib ≥Ik, como já mencionado. O comentário e a figura também são úteis para explicar por que ou como um dispositivo de proteção conforme as normas IEC ou equivalentes, que proteja o condutor contra sobrecargas, e que possua uma Icn ≥Ik, protegeria automaticamente o condutor contra curtos-circuitos — no sentido

![Figura vetorial da página 13](figura-vetorial-p13-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 3 – A corrente Ia (intersecção entre a curva de suportabilidade térmica do condutor e a curva tempo–corrente do dispositivo de proteção) deve ser inferior à corrente de curto-circuito presumida mínima (Ikmin) no circuito a ser protegido. O gráfico a) mostra o caso de um disjuntor; o b) o de um dispositivo fusível aM; e c) o de um dispositivo fusível gG

<!-- pagina-origem: 14 -->

de que dispensa a verificação do critério da integral de Joule. Ora, as regras da proteção contra sobrecargas impõem uma “amarração” entre o condutor, vale dizer, sua seção (que define, para um mesmo tipo de cabo — por exemplo cobre com isolação em PVC —, a sua capacidade de condução de corrente Iz), e a corrente nominal do dispostivo (In), pois estipulam que In ≤Iz. Simplesmente, as especificações da norma do produto são tais que, respeitadas essa relação entre dispositivo e condutor (In ≤Iz) e a condição Icn ≥Ik (o que significa dizer, em outras palavras, que por premissa o condutor jamais seria submetido a uma corrente de curto-circuito superior a Icn), a I2t máxima que o dispositivo deixa passar, aquela correspondente a Icn, via de regra sempre será inferior à k2S2do condutor (mais precisamente, à k2S2do tipo e seção de condutor aos quais o dispositivo está “amarrado”). Em outras palavras, e recorrendo mais uma vez ao gráfico da

![Figura vetorial da página 14](figura-vetorial-p14-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

figura 2: supondo que D efetivamente atenda às regras da proteção contra sobrecargas (InD ≤ IzS), não teremos a curva I2t de D cruzando com a curva I2t de S. Essa será a situação mais comum. E, com certeza, a de todos os casos em que o condutor não é de seção reduzida. Com efeito, o cruzamento só aconteceria em situações muito particulares, que supõem uma conjugação pouco realista de circunstâncias: 1) o condutor é de seção bastante reduzida; e 2) a origem do circuito em questão é tal que ele estaria sujeito a uma elevada corrente de curto-circuito presumida (digamos, um circuito com condutores de 1,5 ou 2,5 mm2 saindo diretamente de um quadro geral de baixa tensão, o que é, convenhamos, uma hipótese pouco realista). Ainda assim, seria virtualmente necessário que nenhum dos dispositivos capazes de garantir a proteção contra sobrecargas desse circuito tivesse a capacidade de interrupção exigida — e obrigando, portanto, o uso de outro dispositivo só para a proteção contra curtos-circuitos. É sintomática, a propósito, a observação da NBR 5410, de que a constante k por ela fornecida, na expressão k2S2 que dá o valor da I2t suportável pelo condutor em regime adiabático (expressão que já descrevemos acima), não seria válida, ou totalmente válida, para condutores de pequena seção — embora seja usada sem essa reserva em toda literatura técnica sobre instalações elétricas alinhada com a normalização IEC. Possivelmente porque resulta em valores conservadores. Assim, a rigor não se pode descartar a eventualidade de uma situação como a ilustrada na figura 2. Só que, na vida real, se a I2t máxima que um dispositivo deixa passar, aquela correspondente à sua Icn, é superior à I2t suportável (em regime adiabático) pelo condutor que ele protege contra sobrecargas — circunstância, como salientado, imaginável apenas no contexto de condutores de seção reduzida —, fatalmente Ik será inferior a Icn e a Ib. Em tempo: se a curva I2t = f(I) do dispositivo de proteção deve ser obtida junto ao fabricante do produto, a do condutor é fornecida pelo fabricante de cabos, não? Talvez. Mas, diferentemente da informação sobre o dispositivo, que só o fabricante reúne mesmo condições de fornecer, no caso dos condutores é possível traçar suas curvas I2t, para cada tipo e seção, utilizando um método normalizado, descrito no artigo “Integral de Joule: coordenando condutores e dispositivos de proteção.”

### Dispositivos garantindo apenas proteção contra curtos-circuitos

De volta à figura 1, verifica-se que com a análise já concluída, em torno do caso considerado mais comum — um mesmo dispositivo preenchendo simultaneamente a proteção contra sobrecargas e contra curtos-circuitos —, fica varrida a seqüência principal do fluxograma. O diagrama também deixa visualmente evidente o que significa, do ponto de vista das verificações exigidas pela norma, a opção ou necessidade de se ter um dispositivo dedicado exclusivamente à proteção contra curtos-circuitos (ficando a proteção contra sobrecargas por conta de outro dispositivo). Pois essa opção ou injunção, como se vê, acrescenta mais uma condição a ser conferida, descrita em 6.3.4.3 da NBR 5410: a de que a corrente Ia, correspondente ao cruzamento da curva tempo–corrente do dispositivo (mais exatamente, curva do tempo máximo de atuação/interrupção) com a curva de suportabilidade térmica do condutor, seja inferior ou, no máximo, igual à corrente de curto-circuito presumida mínima (Ikmin) no circuito a ser protegido. É o que mostra a figura 3, simplificadamente, para disjuntores (a), para dispositivo fusível aM (b) e para dispositivo fusível gG (c). Portanto,

Ia ≤Ikmin

No caso de disjuntores, Ia corresponde ao limiar de disparo magnético Im — mas o valor que leva seguramente o disjuntor a atuar. Assim, em disjuntores com faixa de disparo magnético definida, por exemplo entre 5 e 10 In, Im corresponderia a 10 × In. Ikmin, por sua vez, corresponde à corrente de curto-circuito mínima fase–fase, se o circuito não inclui neutro; ou à corrente (de curto-circuito mínima) fase–neutro, se o circuito inclui neutro. Se Ikmin for inferior a Ia, é preciso então redimensionar a proteção — selecionando um dispositivo com as características apropriadas, alterando definições do circuito ou

<!-- pagina-origem: 15 -->

ambos. Afinal, no plano teórico, para atingir a condição imposta pela norma, ou bem o projetista “diminui” Ia, o que significa substituir o dispositivo inicialmente cogitado por outro que resulte numa Ia inferior a Ikmin; ou bem ele “aumenta” Ikmin, o que significa aumentar a seção do condutor (S) e/ou diminuir o comprimento do circuito (l). Na verdade, ele poderá agir até mesmo nas três frentes (Ia, S e l), simultaneamente. É que a literatura dos fabricantes, visando subsidiar os projetistas, oferece tabelas que, correlacionando corrente de dispositivo (geralmente a corrente nominal, mas já “embutindo” a Ia correspondente) e seção de condutor, indicam os comprimentos máximos de circuito até os quais fica garantido um Ia inferior a Ikmin. A existência dessa documentação mostra, por outro lado, que na prática a seleção de um dispositivo de proteção que garanta apenas a proteção contra curtos-circuitos (ou mesmo, enfim, a seleção de qualquer dispositivo de proteção) não se dá como sugere uma leitura linear das regras da norma de instalações — definindo-se um dispositivo, tentativamente, e em seguida verificando se ele atende as condições impostas pela norma, uma após outra. O exemplo citado, das tabelas, mostra que é possível de pronto selecionar um dispositivo que satisfaça exigências da norma. [Os detalhes da verificação referente a Ikmin, que na prática consiste em checar o comprimento do circuito, são dados no artigo “Corrente de curto mínima: atenção ao comprimento do circuito”.] Note-se, por fim, que a observação aqui feita, sobre a eventual necessidade de “selecionar um outro dispositivo” não deve ser interpretada ao pé da letra — observação que é válida, em particular, para os disjuntores. Até porque essa nova “seleção” pode se resumir a simples mudança no ajuste do disparador magnético, tornando o novo Im compatível com Ikmin.

Notas

(1) Nos circuitos que incluem neutro, a proteção do condutor neutro fica automaticamente assegurada, pelo dispositivo que protege os condutores de fase, se a seção do neutro (SN) não for inferior à dos condutores de fase (SL). Sendo a seção inferior, o que só é possível em circuitos trifásicos nos quais SL > 25 mm2(em cobre) e não for prevista a circulação de correntes harmônicas, os caminhos possíveis para garantir a proteção do condutor neutro são: i) utilizar um dispositivo que incorpore detecção de sobrecorrentes (sobrecargas e curtos-circuitos) no neutro. Esta detecção, naturalmente adequada à seção do neutro, deve provocar o seccionamento dos condutores de fase, mas não necessariamente o do neutro (alínea b) de 5.7.4.3.2 da NBR 5410); ou então, ii) se apenas os pólos “fase” do dispositivo incorporam detecção/proteção de sobrecorrente, sua característica de proteção contra curtos-circuitos deve atender à condição Ia ≤ Ikmin, indicada no bloco H da figura 1, observando-se as especificidades do caso. Quer dizer: a corrente de curto-circuito presumida mínima Ikmin a ser considerada na verificação é aquela determinada para circuitos com neutro e levando em conta a seção menor de neutro (ver artigo “Corrente de curto mínima: atenção ao comprimento do circuito”). No caso ii), a NBR 5410 exige ainda que a máxima corrente suscetível de percorrer o condutor neutro em serviço normal seja “claramente inferior ao valor da capacidade de condução de corrente desse condutor” (nota de 5.7.4.3.2).

## Determinação da corrente de curto-circuito presumida

Dada a corrente de curto-circuito presumida Iko na origem de uma instalação de baixa tensão, é possível determinar, através de método prático, a corrente de curto-circuito presumida Ik na extremidade de qualquer circuito da instalação, conhecidos os comprimentos e as seções dos condutores até aquele ponto. O método admite curto-circuito trifásico e direto e não considera as impedâncias de barras e dispositivos de manobra e proteção. Via de regra, é suficiente para suprir as necessidades que surgem nos cálculos de instalações de baixa tensão — escolha de dispositivos de proteção, determinação da seção dos condutores de proteção, etc. Para as instalações alimentadas por transformador, a corrente de curto-circuito presumida na origem da instalação é tomada igual à corrente de curto-circuito no secundário do transformador, isto é

Ik = Int / Z%

onde Int é a corrente nominal do transformador e Z% sua impedância de curto-circuito. Esse procedimento não leva em conta a impedância da rede a montante do transformador. A tabela I dá os valores de Ik correspondentes às potências nominais usuais dos transformadores trifásicos, calculados fazendo-se

Ik ≅20 Int

Se a instalação é alimentada por dois ou mais transfor-

<!-- pagina-origem: 16 -->

madores em paralelo, a corrente de curto-circuito na origem é considerada igual à soma das correntes de curto-circuito dos transformadores. Para as instalações alimentadas diretamente por uma rede de distribuição pública, o valor da corrente de curtocircuito no ponto de entrega deve ser fornecido pela concessionária. No caso (raro) de ser a instalação alimentada por um alternador, o valor da corrente de curto-circuito deve ser indicado pelo fabricante da máquina. A tabela II, dividida em três partes, (A), (B) e (C), permite determinar, a partir da corrente de curto-circuito na origem de um circuito (ou da instalação, se for o caso), o valor da corrente de curto-circuito presumida na extremidade do circuito, conhecidos seu comprimento l e a seção S de seus condutores, como segue: 1) na parte superior (A) ou na inferior (C), procurar horizontalmente, a partir da seção do condutor em questão (coluna da esquerda), o comprimento correspondente do circuito (ou o valor imediatamente inferior ao real); 2) descer, caso de (A), ou subir, caso de (C), verticalmente à parte (B), até a linha que corresponda, na coluna “Corrente de curto-circuito a montante”, ao valor da corrente de cur-

<!-- tabela-p16-1 -->
| Tab. I - Valores aproximados da corrente de curto-circuito no
secundário de transformadores |  |  |
| --- | --- | --- |
| P
n
(kVA) | I (kA)
ko |  |
|  | 220/127 V | 380/220 V |
| 15 | 0,8 | 0,4 |
| 16 | 0,8 | 0,5 |
| 25 | 1,2 | 0,7 |
| 30 | 1,6 | 0,8 |
| 45 | 2,4 | 1,2 |
| 50 | 2,5 | 1,5 |
| 63 | 3,1 | 1,8 |
| 75 | 3,8 | 2,2 |
| 80 | 4 | 2,3 |
| 100 | 5 | 3 |
| 112,5 | 5,6 | 3,2 |
| 150 | 7,6 | 4,4 |
| 160 | 8 | 4,7 |
| 200 | 10 | 6 |
| 225 | 11 | 6,5 |
| 250 | 12 | 7 |
| 300 | 15 | 9 |
| 315 | 16 | 9 |
| 400 | 20 | 12 |
| 500 | 25 | 14 |
| 630 | 31 | 18 |
| 750 | 37 | 22 |
| 800 | 40 | 23 |
| 1000 | 50 | 28 |
|  |  |  |

![Figura vetorial da página 16](figura-vetorial-p16-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Consultando a tabela II to-circuito na origem do circuito, ou a seu valor aproximado; 3) o cruzamento, em (B), da coluna percorrida com a linha encontrada, fornece o valor de Ik no ponto considerado. A figura 1 ilustra o procedimento descrito. O método descrito não considera a contribuição dos motores, que muitas vezes pode ser desprezada em sistemas de baixa tensão. No entanto, para um cálculo mais preciso e, principalmente, quando existem muitos motores num mesmo setor do sistema, sua contribuição pode ser levada em conta adicionando, ao valor de Ik para o ponto considerado, a corrente

IM = 3,5 IΣnm onde IΣnm é a soma das correntes nominais dos motores que podem funcionar simultaneamente.

![Figura vetorial da página 16](figura-vetorial-p16-2)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – Instalação-exemplo

<!-- pagina-origem: 17 -->

### Exemplo de aplicação

Tomemos o exemplo da figura 2. Para o ponto F1 temos, da tabela I, o valor da corrente de curto-circuito presumida na origem (transformador de 630 kVA, secundário de 380 V):

Ik1 = 18 kA Da tabela II temos que, para cabo de cobre de 240 mm2, 380 V (parte (A)), o comprimento imediatamente inferior ao valor real de 100 m é 85 m. Descendo, na coluna desses 85 m, até as linhas da parte (B) em que se encontram os valores de Ik a montante que mais se aproximam de 18 kA (que são as linhas de 20 kA e de 15 kA), verificamos que o valor da corrente de curto-circuito presumida no ponto F2 da figura 2 (Ik2) será:

8,5 kA < Ik2 < 10 kA

<!-- pagina-origem: 18 -->

## Integral de Joule: coordenando condutores e dispositivos de proteção

Recurso indicado, na NBR 5410, para a verificação da coordenação entre condutores e dispositivos de proteção, no quadro da proteção contra curtos-circuitos, a integral de Joule é definida como a integral do quadrado da corrente durante um dado intervalo de tempo, isto é

t ∫ 2 i dt 0 Essa grandeza, cujo símbolo é “I2t”, representa os esforços térmicos e magnéticos reais impostos a um componente conduzindo uma corrente de curto-circuito. Quando as sobrecorrentes assumem valores muito elevados, como no caso de curtos-circuitos, os condutores atingem temperaturas da ordem de centenas de graus em tempos extremamente pequenos, freqüentemente da ordem de centésimos de segundo. Seja devido à forma de onda, seja devido à indutância do circuito, nos primeiros ciclos de uma corrente de curto-

![Figura vetorial da página 18](figura-vetorial-p18-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 1 – Característica I2t típica de um cabo de BT circuito seus efeitos não podem ser avaliados pelo valor eficaz. Nessas condições, para o estudo dos efeitos térmicos dessa corrente, considerando tempos extremamente pequenos, não é possível separar a grandeza corrente da grandeza tempo, sendo necessário considerá-las em conjunto no produto integral

que representa energia por unidade de resistência (J/Ω= A2.s). A integral de Joule de um componente elétrico pode ser calculada ou medida em ensaios de curto-circuito. As curvas da integral de Joule em função da corrente, I2t = f(I), de cabos e dispositivos de proteção são uma ferramenta valiosa no estudo da proteção dos condutores contra sobrecorrentes e da coordenação seletiva entre dispositivos.

### Integral de Joule de condutores

A figura 1 mostra a curva da integral de Joule (característica I2t) típica de um cabo de baixa tensão, que fornece, para cada valor de corrente, a “energia específica” I2t que pode “passar” pelo cabo, isto é, a integral de Joule que o cabo suporta. O trecho assintótico vertical corresponde a um valor de corrente da ordem da capacidade de condução de corrente do cabo, Iz, que faz com que seja atingida uma temperatura da ordem da temperatura máxima para serviço contínuo do cabo (função do material da isolação), θz. Essa corrente pode circular continuamente por um tempo extremamente longo, cerca de 20 anos, correspondendo a um valor de I2t praticamente infinito. O trecho assintótico horizontal corresponde aos valores de corrente para os quais o aquecimento do condutor é considerado adiabático, isto é, sem troca de calor entre condutor e isolação: I2t = cte. A região entre as assíntotas vertical

Fig. 2 – Característica I2t típica de um disjuntor termomagnético

<!-- pagina-origem: 19 -->

![Figura vetorial da página 19](figura-vetorial-p19-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 3 – Características I2t de interrupção típicas de fusíveis gG

e horizontal pode ser obtida a partir da chamada “curva de vida útil convencional” do cabo. A curva da integral de Joule de um condutor, na forma I2t = f(I), pode ser traçada calculando-se os valores de I2t a partir do método proposto pela IEC 60949 (ver boxe). Tratemos do aquecimento adiabático. A energia necessária para elevar a temperatura do condutor do cabo desde a temperatura máxima para serviço contínuo, θz (70°C para isolação em PVC, ou 90°C para EPR ou XLPE), até a temperatura de curto-circuito, θk (160°C para PVC ou 250°C para EPR ou XLPE), num processo adiabático, pode ser expressa por:

t () ∫ 2 = θ − θ γ Ri dt c S l k z 0

onde i é o valor instantâneo da corrente, t o tempo em que ela circula, R a resistência do condutor, c o calor específico do material do condutor, γ sua massa específica, S a seção do condutor e l seu comprimento. A resistência R, como sabemos, não é independente da temperatura e, portanto, não pode ser colocada fora da integral. No entanto, sendo fixos os dois limites de variação de R, para θz e para θk, podemos escrever:

t () ∫ 2 = θ − θ γ R i dt c S l eq k z o A existência de limites prefixados de temperatura (inicial e final) permite que a resistência seja tratada como um valor constante, Req, ou que a resistividade seja considerada constante e igual a ρeq (valores correspondentes a uma temperatura intermediária). Podemos escrever, então: l = ρ R eq eq S e () t − θ θ ∫ 2 2 k z = γ i dt c S ρ eq 0 Fazendo

() − θ θ k z γ = c K ρ eq virá

t ∫ 2 2 2 = i dt K S 0 Essa expressão dá a integral de Joule, isto é, a energia por unidade de resistência (energia específica) necessária para, num processo adiabático, elevar a temperatura do condutor desde a temperatura máxima para serviço contínuo, θz, até a temperatura de curto-circuito, θk. A NBR 5410 dá, em 5.3.4.3(b), os valores de K, aqui reproduzidos na tabela I. Assim, por exemplo, a integral de Joule que adiabaticamente leva um condutor isolado (ou cabo unipolar) de cobre, BT, com isolação de EPR, 25 mm2, de θz = 90°C a θk = 250°C é de I2t = K2S2 I2t = 1352× 252 I2t = 11390 × 103A2s.

### Integral de Joule dos dispositivos de proteção

A característica I2t de um disjuntor termomagnético

![Figura vetorial da página 19](figura-vetorial-p19-2)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 4 – Verificação da seletividade entre disjuntor e fusível usando as curvas I2t

<!-- pagina-origem: 20 -->

dá o valor máximo da integral de Joule que o dispositivo deixa passar, em função da corrente que por ele circula. Seu aspecto típico é mostrado na figura 2, onde destacamos quatro regiões: a região I, com correntes I ≤In (In é a corrente nominal – do disjuntor), onde não existe limitação de corrente; a região II, com In < I ≤Im (Im é o limiar de atuação – magnética), onde os tempos de atuação são relativamente longos, atuando o disparador térmico. Pode ser obtida da curva tempo-corrente do dispositivo; a região III, com Im < I ≤Icn (Icn é a capacidade de in- – terrupção do dispositivo), onde os tempos de atuação são curtos, atuando o disparador magnético. Pode ser obtida a partir de ensaio de curto-circuito do dispositivo; e a região IV, com I > Icn, na qual o disjuntor não de- –

Os valores da integral de Joule admissíveis nos condutores elétricos e, assim, as curvas respectivas [I2t = f(I)], podem ser determinados usando-se o método da IEC 60949: Calculation of thermally permissible short-circuit currents, taking into account non-adiabatic heating effects. A fórmula geral indicada na norma é:

2 2 2 = I t I G

onde:

1 − 2 + 2 + ∆ X ∆ = X 4 z S = G 1 − 2 2 z S

θ β +   2 I Y f 2 2   α = = α − K S ln z θ β + S   i

sendo: I = corrente que percorre o condutor (A); S = seção nominal do condutor (mm2); θf = temperatura final (°C); θi = temperatura inicial (°C); β = recíproco do coeficiente de temperatura da resistência do condutor, em °C (K) (ver tabela I); ve ser utilizado. No caso dos fusíveis, distinguem-se três características I2t: a de fusão, isto é, a energia específica que o fusível deixa passar entre os limites do tempo de fusão; a de arco, correspondente à energia que o fusível deixa passar entre os limites do tempo de arco; e a de interrupção, que pode ser obtida pela soma das outras duas e que corresponde à integral de Joule que o fusível deixa passar entre os limites do tempo de interrupção. É essa última que interessa no que concerne à proteção dos condutores. A figura 3 apresenta exemplos da característica I2t de interrupção. Devido à elevada capacidade de interrupção (Icn) dos fusíveis, não existem problemas para a interrupção de correntes de curto-circuito elevadas. Assim, na grande maioria das aplicações é dispensável a verificação de Ik (de acordo

Tab.I - Constantes K e β β Material K Cobre 226 234,5 Alumínio 148 228

K = constante que depende do material condutor (ver tabela I); X e Y = constantes que dependem do material, da isolação e da tensão de isolamento do condutor (ver tabela II)

Tab. II - Constantes X e Y Isolação X Y

PVC ≤3 kV 0,29 0,06 PVC > 3 kV 0,27 0,05 XLPE 0,41 0,12 EPR ≤3 kV 0,38 0,10 EPR > 3 kV 0,32 0,07

Exemplos Vamos calcular a integral de Joule suportável por um cabo de cobre, isolação de PVC, seção de 6 mm2, percorrido por uma corrente de 100 A. Lembremos que, no caso de isolação de PVC (que é o do exemplo), a temperatura máxima para serviço contínuo é de 70°C e a temperatura limite de curto-circuito é de 160°C. Portanto, θi = 70°C θf = 160°C

Temos, ainda: β = 234,5 (tabela I);

### Como construir as curvas I2t dos condutores

<!-- pagina-origem: 21 -->

com 5.3.4.3a) da norma de instalações, Ik ≤Icn). Por outro lado, ao contrário do que ocorre com os disjuntores, a I2t dos fusíveis aumenta com a redução da corrente, como se vê na figura 3. Nessas condições, o fusível apresenta um comportamento crítico para pequenas correntes de curto-circuito, isto é, ele poderá não atuar num tempo suficiente, permitindo o aquecimento excessivo do condutor. Se o fusível for dimensionado para proteger o condutor também contra correntes de sobrecarga, não existirão correntes críticas e, na prática, não haverá necessidade de se verificar a integral de Joule. Se, no entanto, o fusível for superdimensionado em relação à capacidade de condução de corrente do condutor, devem ser verificadas (pelas características I2t) as condições de proteção no caso de corrente de curto-circuito presumida mínima.

K = 226 (tabela I); X = 0,29 (tabela II); e Y = 0,06 (tabela II).

Assim,

θ β +   f 2 2   = α = K S ln θ β +   i

+   160 234 5, 2 2 = = × ×   226 6 ln 476 137 1, + 70 234 5,  

2 1002,0 06 I Y = − = − = z 0,011 α 476137 1, 6 S

2 2 = + × × = ∆ = +,0 29 (4,0 011 6) 0,348 X 4 z S

− − 1 1 + ∆ + X,0 29,0 348 2 2 = = = G 16,33 − − 1 1 × × z S 2 2,0 011 6 2 2

2 2 2 2 2 A2 = = × = I t I G 100 (16, 33) 2 665 816 s

Calculemos a integral de Joule para o mesmo condutor, mas percorrido agora por uma corrente de 1000 A:

α não muda e, portanto, α = 476137,1 As características I2t também podem ser utilizadas na verificação da seletividade entre dispositivos, como mostra a figura 4 — caso de um disjuntor com um fusível a montante. Na figura acham-se ilustradas: a característica I2t do disjuntor (curva C); • a característica I2t de fusão do fusível (curva A); e • a característica I2t de interrupção do fusível (curva B). • Verifica-se que se a corrente I for inferior a Is (intersecção das curvas C e A) o disjuntor atuará sem que seja afetado o fusível. Se I for superior a IB (intersecção das curvas C e B), atuará o fusível antes do disjuntor. Para I compreendido entre Is e IB, o disjuntor atuará, porém o fusível poderá ficar afetado, podendo atuar intempestivamente em outra ocasião.

2 I Y = − = z 2,090 α S

2 ∆ = + = X 4 z S 50,250

− 1 + ∆ X 2 = = G 0,72 − 1 z S 2 2

2 2 2 2 = = I t I G 519 229 A s

A figura B1 mostra a curva I2t = f(I) de um condutor de cobre, isolação de PVC e seção de 16 mm2, levantada utilizando-se o método descrito — naturalmente, com a ajuda de um programa de planilha eletrônica.

Fig. B1 – Curva I2t de condutor de cobre/PVC, 16 mm2

<!-- pagina-origem: 22 -->

## Corrente de curto mínima: atenção ao comprimento do circuito

Em que circunstâncias o uso de um dispositivo envolve apenas a proteção contra curtos-circuitos? Ou, examinada a questão do ângulo da norma de instalações, em que circunstâncias, na proteção contra sobrecorrentes, a adequação de um dispositivo é checada considerando apenas suas características de proteção contra curtos-circuitos? Basicamente, 1) quando o dispositivo apresenta características de funcionamento que só garantem mesmo essa proteção (caso dos disjuntores apenas com disparador magnético e dos fusíveis aM), sendo então seu uso necessariamente casado com o de um outro dispositivo responsável pela proteção contra sobrecargas. Ou 2) para complementar a insuficiente proteção contra curtos-circuitos (tipicamente, insuficiente capacidade de interrupção) de um outro dispositivo que, cogitado a princípio para prover ambas as proteções, contra sobrecargas e contra curtos-circuitos, não possuía então capacidade de interrupção nominal compatível com a corrente de curto-circuito presumida no ponto de sua instalação. Ou, ainda, 3) quando ao dispositivo cabe, “adicionalmente”, a missão de proteger contra curtos-circuitos linhas ou trechos de linhas, a jusante, nas quais houve deslocamento do dispositivo contra sobrecorrentes; isto é, quando o dispositivo assume, devido ao deslocamento de um dispositivo a jusante — do ponto onde a rigor deveria ser instalado para outro ponto mais à frente —, a proteção contra curtos-circuitos do trecho deixado a descoberto pelo deslocamento. Cabe frisar que, aqui, a verificação baseada apenas nas características de proteção contra curtos-circuitos, referida inicialmente, deve ser entendida como aquela associada especificamente a essa missão “adicional” do dispositivo, de proteger um circuito que não o “seu”. A verificação da proteção contra sobrecorrentes, no contexto do “seu” circuito, deve ser verificada na plenitude da missão que aí lhe cabe. Esses três casos ficariam então adicionalmente sujeitos, como explicado no artigo “Equacionamento da proteção contra curtos-circuitos”, à terceira verificação da proteção contra curtos-circuitos lá referida, e descrita em 6.3.4.3 da NBR 5410: a de que a corrente Ia, correspondente ao cruzamento da curva tempo–corrente do dispositivo (mais exatamente, curva do tempo máximo de atuação/interrupção) com a curva de suportabilidade térmica do condutor, seja inferior ou, no máximo, igual à corrente de curto-circuito presumida mínima (Ikmin) no circuito a ser protegido (ver

![Figura vetorial da página 22](figura-vetorial-p22-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

figura 3 do artigo mencionado). As outras duas verificações, vale lembrar, referem-se à capacidade de interrupção do dispositivo, indispensável, e à integral de Joule que ele deixa passar, necessária apenas quando houver dúvidas a respeito deste ponto. De fato, a exigência associada a Ikmin é aplicável apenas quando o dispositivo só garante proteção contra curtos-circuitos (caso de disjuntor apenas com disparador magnético ou de fusíveis aM) ou quando o dispositivo, embora reunindo recursos capazes de prover proteção contra sobrecargas e contra curtos-circuitos, é usado explorando-se apenas essa sua segunda habilidade, a de proteção contra curtos-circuitos. Como o que interessa, neste último caso, é tão-somente a proteção contra curtos-circuitos, seria como assumir que um disjuntor termomagnético, por exemplo, é apenas magnético, ignorando-se deliberadamente a habilidade associada a seu disparador térmico; e, nessas condições, assumir que a corrente nominal do dispositivo é algo representativo apenas da corrente de regime permanente para a qual suas partes condutoras foram dimensionadas, e não algo que traduza sua ação contra sobrecargas — que, mais uma vez, deve ser ignorada —, ou qualquer idéia, daí decorrente, de coordenação com o condutor que ele protegeria. O boxe “Um ‘mesmo’ dispositivo, por que exigências distintas?” explica por que a exigência associada a Ikmin só se aplica a dispositivos, por construção ou por critério de projeto, destinados exclusivamente à proteção contra curtos-circuitos. De qualquer forma, na prática, como antecipado no artigo referido, a verificação da exigência envolvendo Ikmin pode ser algo muito mais simples do que sugere, literalmente, o texto da norma. Assim, a tradução prática da regra em questão é: verifique se o comprimento do circuito a ser protegido pelo dispositivo (apenas) contra curtos-circuitos não ultrapassa o limite até o qual fica garantida sua atuação. E isso é feito recorrendo-se a tabelas de consulta direta que dão esse comprimento máximo de circuito (Lmax). Os dados de entrada são, de um lado, a seção do condutor a ser protegido e, de outro, dependendo do estilo de tabela e do produto envolvido, a corrente nominal do dispositivo ou então sua cor-

<!-- pagina-origem: 23 -->

rente de atuação instantânea. No cruzamento da linha e coluna pertinentes, obtém-se o Lmax. Seja como for, o dado de entrada, no que se refere ao dispositivo, traduz em última análise a Ia definida acima. Para disjuntores, por exemplo, sejam eles termomagnéticos ou apenas magnéticos, Ia é o menor valor de corrente que efetivamente garante a atuação do disparador magnético. Enfim, a Ia da teoria, intersecção entre as curvas tempo–corrente do dispositivo e do condutor, é a mesma corrente de disparo magnético (Im) dos disjuntores. Assim, ou bem o fabricante fornece a tabela de Lmax em função diretamente da Im de seus disjuntores/disparadores magnéticos; ou, indiretamente, em função da corrente nominal dos disjuntores (In) — caso das linhas de disjuntores mais padronizados e, em particular, quando se tem uma proporcionalidade bem definida entre Im e In. Já nas tabelas de Lmax válidas para fusíveis, em que o Ia entra também de forma indireta, já embutido nas correntes nominais listadas, os fabricantes geralmente adotam, para os Ia respectivos, a corrente que assegura (curva do tempo máximo de interrupção) a atuação do fusível em 4 ou 5 s.

### A origem das tabelas

As tabelas de Lmax publicadas pelos fabricantes, ou que qualquer profissional de instalações elétricas pode também construir, resultam da expressão:

8,0 U S L max= L ρ 2 I (1), a

aplicável a circuitos sem neutro, sejam eles 3F ou 2F (F = fase), ou de

8,0 U S L = L max + ρ 1(m) I (2), a

aplicável a circuitos com neutro, sejam eles 3F+N, 2F+N ou F+N, e resultam, inerentemente, das seguintes hipóteses: o curto–circuito (mínimo) ocorre • na extremidade “carga” do circuito; o curto–circuito (mínimo) envol- • ve dois condutores, podendo ser fase–fase ou fase–neutro. Portanto, o U das expressões é tensão de linha, no caso (1), e tensão de fase no caso (2); a tensão na origem do circuito se • mantém, na ocorrência da falta, em 80% do valor nominal. Daí o termo 0,8 U; a resistividade do material condutor do cabo é tomada • à temperatura média de curto-circuito. Para cobre, portanto, ρ = 0,027 Ω.mm2/m; reatância desprezível para seções até 120 mm2, inclu- • sive. Para seções superiores, a reatância entra no cálculo através do fator r da tabela I. Note-se que, nas fórmulas, SL representa a seção do condutor de fase, em mm2; e que na expressão (2) a parcela (1 + m) traduz a presença do condutor neutro, sendo m a relação entre a seção do condutor de fase e a do neutro, isto é, m = SL/SN. Com a inclusão do fator r, a expressão (1) ficaria:

8,0 U S L max= L ρ r 2 I (1’) a

Já na expressão (2), considerando genericamente a hipótese de seções diferentes para condutor de fase e condutor neutro, teríamos então um fator r1 para o condutor de fase e um fator r2 para o condutor neutro. Assim, 8,0 U S L = L max + ρ (r r m) I 1 2 a (2’)

A tabela II traz um exemplo de tais tabelas de consulta rápida que fornecem o Lmax até o qual fica garantida a atuação dos disjuntores listados. Ela foi construída assumindo-se Ia (ou Im) = 14 × In. Tendo em vista a Im desses disjuntores, eles poderiam ser classificados, se construídos conforme a IEC 60898, como tipo D – categoria em que aquela norma enquadra os disjuntores com faixa de disparo instantâneo de 10 a 20 × In. Mas atenção: levando em conta que disjuntores como os que seguem a IEC 60898 são produtos padronizados, de uso generalizado em instalações prediais e aplicados à proteção contra sobrecorrentes em geral (portanto, contra sobrecargas e curtos-circuitos), nunca é demais lembrar que o Lmax indicado em qualquer tabela similar à tabela II é válido quando o disjuntor for usado apenas na proteção contra curtos-circuitos. Se o disjuntor for usado também na proteção contra sobrecargas, e atender o que a NBR 5410 prescreve, neste particular, esqueça a história de Lmax! Isso para lembrar, mais particularmente, que as correntes nominais que figuram na tabela devem ser lidas desvinculadas do significado e da importância singular que a grandeza tem no contexto da proteção contra sobrecargas. Corrente nominal, aí, é estritamente sinônimo da corrente de regime per-

<!-- pagina-origem: 24 -->

### Um “mesmo” dispositivo, por que exigências distintas?

A figura (a) mostra a curva de um disjuntor D, com o qual se quer proteger um condutor, S, cuja curva tempo–corrente caracterizadora de sua suportabilidade térmica também se encontra aí ilustrada. Esse mesmo disjuntor D, acompanhado da curva do cabo, é reapresentado nas figuras abaixo, (b) e (c). O mesmo disjuntor? Sim, com a mesma corrente nominal, a mesma faixa de disparo magnético, etc. Só que vamos imaginar o disjuntor D, no caso D2 (figura c), dotado apenas de disparador magnético; ou então que, embora dotado de disparadores térmico e magnético, D (D2) seja utilizado levando em conta apenas seu disparador magnético. Em outras palavras, imaginemos que só nos interessa, no caso D2, a característica de proteção contra curtos-circuitos do disjuntor D. Já o disjuntor D do caso D1 (figura b) será explorado em toda sua plenitude, isto é, em toda sua capacidade de proteção contra sobrecorrentes, sejam elas sobrecargas ou curtos-circuitos. Ora,assumir que o disjuntor D do caso D1 (figura b) protege o condutor S contra quaisquer sobrecorrentes — não só porque ele dispõe de disparadores térmico e magnético, mas porque sua corrente nominal In, ou de ajuste do disparador térmico, é inferior à capacidade de condução de corrente (Iz) do condutor S, já que as regras da proteção contra sobrecargas impõem In ≤Iz —, significa dizer que todas as sobrecorrentes no circuito por ele protegido, até a capacidade de interrupção do dispositivo, serão eliminadas, e em tempos inferiores aos da suportabilidade térmica do cabo. É o que mostra a linha de cor verde da figura, que é a curva correspondente ao tempo máximo (considerando inércia, temperatura, tolerâncias admitidas pelas normas, etc.) em que o disjuntor irá atuar, não importa se o nome da sobrecorrente é sobrecarga ou curto-circuito.

manente suportável pelas partes condutoras do disjuntor. Seja como for, os valores da tabela II seguem a expressão (1). E, por isso, ela pode ser considerada absolutamente típica, dentro da literatura sobre assunto. Pois é assim que os fabricantes de dispositivos montam as tabelas que publicam: para tensão de linha, circuitos sem neutro, para curto fase–fase e des- Agora, quando o disjuntor D é identificado ou utilizado apenas com base na sua característica de proteção contra curtos-circuitos — seja, mais uma vez, porque só conta com disparador magnético ou porque só se conta com seu disparador magnético —, a única coisa que se pode garantir é que ele irá seguramente atuar para correntes a partir de Ia (figura c). Ora, se a atuação de D (D2) só é garantida para correntes iguais ou superiores a Ia (o que acontece com as sobrecorrentes inferiores a Ia“não é um problema de D2”),é preciso então que as correntes de curto-circuito suscetíveis de circular no circuito em questão sejam pelo menos iguais a Ia. Em outras palavras,para que D (D2) cumpra com a proteção contra curtos-circuitos que oferece, é preciso que a mínima corrente de curto-circuito suscetível de percorrer o circuito seja maior ou, no mínimo, igual a Ia. E, portanto,

Ikmin ≥Ia

ou, colocando na ordem adotada pela norma, Ia ≤Ikmin

Logo, a impedância do circuito não deve ser superior à que permitiria, com segurança, a circulação de Ikmin. Para uma mesma seção de condutor, mesmo tipo de cabo, etc., impõe-se, portanto, um limite máximo ao comprimento do circuito. Tudo isso explica por que temos um disjuntor, D = D1, para o qual não se exige a verificação da condição associada a Ikmin, e um “mesmo” disjuntor, D = D2, ao qual a exigência se aplica. Note-se, por outro lado, que se ambos são “iguais”, mas um protege contra qualquer sobrecorrente (comeprezando a reatância; e remetendo a obtenção de Lmax referentes a outras situações (circuitos com neutro, seção de neutro diferente da do condutor de fase, etc.) a fatores de correção — multiplicadores que, em resumo, são pura aritmética. Assim, como os valores da tabela II são válidos para circuito sem neutro, tensão de linha de 380 V, bastaria o interessado multiplicá-

<!-- pagina-origem: 25 -->

çando pelas sobrecargas) e o outro “só” contra curtoscircuitos, poderemos “deslocar D2 (ou seja, sua curva) para a direita”, mas jamais D1. Traduzindo: como D2 é assumido apenas como proteção contra curtos-circuitos, em princípio não há nada que obrigue a que sua corrente nominal In seja inferior à capacidade de condução de corrente Iz do condutor ao qual é aplicado. Aliás, como reconhece a NBR 5410 na nota 3 de 5.3.4.3, “a corrente nominal do dispositivo de proteção contra curtos-circuitos pode ser superior à capacidade de condução de corrente dos condutores do circuito.” E nem poderia ser diferente. Portanto, na figura, D2 poderia perfeitamente proteger (contra curtos-circuitos!) outros cabos à esquerda de S (esse o sentido do “deslocamento para a direita” referido), vale dizer, com seções menores; e, eventualmente, também cabos à direita, desde que neles não circule uma corrente de regime permanente superior à que suportam as partes condutoras do dispositivo — aqui entendido como um conjunto capaz de todas as ações dele exigidas e não apenas o disparador. É claro que para tudo há limites práticos, ditados pela realidade, sobretudo a econômica. Já D1, que se assumiu usado contra sobrecargas (ou, enfim, contra sobrecorrentes em geral), não poderá ter In superior à Iz do condutor S. Aqui, a situação é a inversa: o disjuntor poderia garantir a proteção contra sobrecorrentes (sobrecargas e curtos-circuitos) de qualquer condutor à direita de S, ou seja, com seção superior à de S — ressalvados, sempre, os limites práticos e econômicos dessa brincadeira, e outras considerações fora do propósito desses comentários, como a questão da capacidade de interrupção.

los por 1/√3 (ou, o que dá no mesmo, por 220/380) para obter o Lmax válido para qualquer circuito 3F+N, 2F+N ou F+N com tensão de fase de 220 V, correspondente à tensão de linha de 380 V. E se a tensão de fase do circuito em questão não for 220 V, mas 127 V, o multiplicador também é simples e automático: 127/380. E, ainda, se a seção do neutro for inferior à seção do condutor de fase (que é, de qualquer forma, a seção com que se consulta a tabela), deve-se aplicar ao resultado o fator

2 + 1(m)

<!-- pagina-origem: 26 -->

<!-- tabela-p26-1 -->
| Tab. II - Comprimento máximo de circuito (*) (m) |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Corrente
nominal do
disjuntor (A) | Seção nominal do condutor (mm2) |  |  |  |  |  |  |  |  |
|  | 1,5 | 2,5 | 4 | 6 | 10 | 16 | 25 | 35 | 50 |
| 6
10
13
16
20
25
32
40
50
63
80
100
125 | 100
60
46
37
30
24
18
15
12
9
7
6
4 | 167
100
77
62
50
40
31
25
20
15
12
10
8 | 268
160
123
100
80
64
50
40
32
25
20
16
12 | 402
241
185
150
120
96
75
60
48
38
30
24
19 | 670
402
309
251
201
160
125
100
80
63
50
40
32 | 1072
643
494
402
321
257
201
160
128
102
80
64
51 | 1005
773
628
502
402
314
251
201
159
125
100
80 | 1082
879
703
562
439
351
281
223
175
140
112 | 1256
1005
804
628
502
402
319
251
201
160 |

(*) Circuito com condutores de cobre, protegido por disjuntor com disparo magnético Im = 14 In Verificação prática da exigência, dada em 6.3.4.3 da NBR 5410, de que o dispositivo de proteção contra curtos-circuitos deve seguramente atuar para a corrente de curto-circuito mínima presumida no circuito considerado: basta confrontar o comprimento real do circuito a ser protegido com o comprimento máximo admissível dado na tabela. Sendo o comprimento real inferior ao limite tabelado, fica atendida a exigência. Mas a verificação só se aplica aos casos em que o dispositivo é usado apenas na proteção contra curtos-circuitos. A tabela é somente um exemplo e se refere a disjuntores cujo disparo instantâneo se dá com 14 vezes a corrente nominal.

onde m, como já mencionado, é a relação entre a seção do condutor de fase e a do neutro. Logo, se a seção do condutor neutro for metade da do condutor de fase, o fator é 2/3. Em termos genéricos, levando em conta todas as possibilidades, a composição do fator de correção total para a tabela do exemplo seria, portanto: UN 2 × + 380 1(m) onde UN é a tensão nominal do circuito considerado (a tensão de fase, se o circuito inclui neutro, ou tensão de linha, caso contrário). Na verdade, as possibilidades de aproveitamento da mesma tabela II para outras situações não param por aí. Dela podem ser extraídos também Lmax válidos para qualquer outro disjuntor com proporcionalidade bem definida entre Im e In, isto é, do tipo

Im = α × In

onde α é o multiplicador que caracteriza essa relação. Como na tabela II assumiu-se α = 14, para obter os Lmax válidos para qualquer outro disjuntor do tipo Im = α × In, bastaria aplicar aos Lmax da tabela II o multiplicador

14 α

### Queda de tensão pode prevalecer

Num projeto real, é possível que a verificação aqui comentada, a do critério do curto mínimo, acabe se mostrando “redundante” face a outras exigências da norma — melhor dizendo, ultrapassada por outras exigências, mais restritivas. Em particular, o critério que pode competir com o do curto mínimo é o da queda de tensão. De fato, uma das clássicas condições a serem atendidas no dimensionamento de um circuito refere-se à queda de tensão. A NBR 5410 impõe aí limites. A queda de tensão num circuito terminal não pode ultrapassar 4%; e a queda de tensão total, da origem da instalação até o “último dos circuitos”, não pode ultrapassar 4% para instalações alimentadas diretamente pela rede de distribuição pública de baixa tensão ou 7% para instalações equipadas com subestação ou fonte própria. Ora, uma queda de tensão máxima admissível, como as que a norma impõe, implica também um comprimento máximo admissível de circuito.

## Proteção de cabos em paralelo

A proteção contra sobrecorrentes de condutores em paralelo suscita muitas dúvidas entre projetistas e instaladores. Quando utilizar um único dispositivo, isto é, uma única proteção (um fusível ou um pólo de disjuntor) por fase ou proteções individuais, ou seja, um dispositivo para cada conjunto de fases (ver boxe)? A NBR 5410 trata do assunto de maneira bastante superficial em 5.3.3.3 (proteção contra correntes de sobrecarga), em 5.3.4.4 (proteção contra correntes de curtocircuito) e em 6.2.5.7. Na IEC 60364, a norma internacional que constitui o documento de referência da NBR 5410, o assunto já é tratado com mais clareza e detalhes — graças a incorporação de textos relativamente recentes. O que se segue é uma análise do tema da proteção de cabos em paralelo tomando como base a seção pertinente da IEC 60364. Em matéria de proteção contra sobrecargas, quando um único dispositivo protege vários condutores em paralelo não deve haver nenhuma derivação, nem dispositivos de seccionamento ou manobra ao longo dos condutores em paralelo.

<!-- pagina-origem: 27 -->

### Proteção única e proteção individual

Seja, por exemplo, um circuito trifásico (sem neutro) com três condutores por fase. Teremos então nove condutores — três para a fase R, três para a fase S e três para a fase T —, constituindo três conjuntos: R1S1T1, R2S2T2 e R3S3T3. As duas possibilidades de proteção contra sobrecor-rentes são: a) Proteção única – Um dispositivo fusível

Trata-se de uma prescrição necessária, embora não suficiente, para garantir (o mais possível) uma igual divisão de corrente entre os condutores de cada fase. Neste caso (igual divisão de corrente), o texto IEC esclarece que o valor de Iz a ser considerado é a soma das capacidades de condução de corrente dos vários condutores em paralelo. No caso de divisão desigual de corrente (diferença superior a 10%) entre os condutores de uma mesma fase, é dito que a corrente de projeto e as exigências de proteção contra sobrecarga devem ser consideradas individualmente, para cada condutor. Analisemos tais prescrições. Quando ocorre uma sobrecarga num circuito contendo condutores em paralelo, a corrente aumentará em cada condutor na mesma proporção em que se dividia a corrente normal. Se a corrente de cada fase dividir-se igualmente entre os condutores em paralelo, uma única proteção, por fase, poderá ser usada para proteger todos os respectivos condutores. A divisão da corrente entre os condutores em paralelo de cada fase é função da impedância dos condutores. Para cabos de maior seção nominal (S > 120 mm2), a reatância indutiva é maior do que a resistência e terá um efeito significativo na divisão de corrente. É importante notar que a reatância indutiva é fortemente influenciada pela posição relativa dos cabos. Se, por exemplo, tivermos um circuito com dois cabos de seção elevada por fase, de mesma seção e mesmo comprimento, dispostos de maneira desfavorável, como seria o caso de cabos de mesma fase justapostos, a divisão de corrente pode chegar a 70%/30%, ao invés de 50%/50%. Quando for previsível uma diferença de corrente superior a 10% entre os condutores em paralelo, as correntes de projeto e as exigências de proteção contra correntes de sobrecarga devem ser consideradas individualmente para cada condutor, conforme mencionado. Seja um circuito com m condutores por fase. A corrente de projeto IBk do condutor k é dada, em termos fasoriais, tripolar ou um disjuntor tripolar, com um fusível ou um pólo para o conjunto dos três condutores de cada fase (R1R2R3, S1S2S3 e T1T2T3); b) Proteção individual – Três dispositivos fusíveis tripolares ou três disjuntores tripolares, com um dispositivo fusível ou um disjuntor para cada conjunto das três fases (R1S1T1, R2S2T2 e R3S3T3).

por: I B = I Bk Z Z Z Z Z Z k k k k k k...... + + + + + + + Z Z Z Z Z Z 1 2 1 1 − + k k k m onde IB = corrente de projeto do circuito, IBk = corrente de projeto do condutor k, Z1, Z2,... Zk... Zm = impedância dos condutores 1, 2,..., k,... m. As condições de proteção dadas em 5.3.3.2 (a) e (b) da NBR 5410 podem ser escritas

IBk ≤Ink ≤Izk

I2k ≤1,45 Izk

se forem previstas proteções individuais, ou

IB ≤In ≤ΣIzk

I2 ≤1,45 ΣIzk

se for prevista uma única proteção por fase, onde Izk = capacidade de condução de corrente do condutor k, considerando todos os fatores de correção necessários; ΣIzk = soma das capacidades de condução de corrente de todos os m condutores, considerando todos os fatores de correção necessários; In = corrente nominal do dispositivo de proteção único, afetada dos fatores de correção necessários; Ink = corrente nominal do dispositivo de proteção do condutor k, afetada dos fatores de correção necessários; I2, I2k = respectivas correntes convencionais de atuação. As impedâncias dos condutores — fundamentais para o cálculo das correntes de projeto IBk —, função de sua posição relativa, podem ser obtidas dos fabricantes (para as disposições mais usuais) ou calculadas.

<!-- pagina-origem: 28 -->

Fig. 1 – Corrente no início da falta

Quanto à proteção contra correntes de curto-circuito, a NBR 5410 diz, apenas, que um mesmo dispositivo pode proteger vários condutores em paralelo, desde que suas características de atuação e a maneira de instalar os condutores sejam adequadamente coordenadas. É mais ou menos essa a abordagem do texto IEC. Mas o documento internacional acrescenta que o dispositivo deve garantir a proteção no caso de uma falta que ocorra no ponto mais desfavorável em qualquer dos condutores e lembra que a falta pode ser alimentada pelas duas extremidades de um condutor em paralelo. Assim, se não ficar garantida a atuação efetiva do dispositivo, no caso de proteção única, o texto determina a adoção de medidas complementares; ou então que seja adotada a proteção individual. As medidas complementares associadas ao uso de um único dispositivo são: reduzir, por instalação, os riscos de curto-circuito em • qualquer condutor paralelo — por exemplo, com proteção mecânica; não instalar os condutores junto a material combustível. • Ao aplicar a proteção individual deve-se, segundo o documento: 1) utilizar, no caso de dois condutores em paralelo,

![Figura vetorial da página 28](figura-vetorial-p28-1)

> [descrição gerada] Elemento visual presente no original; consulte a página indicada para interpretação gráfica.

Fig. 2 – Corrente após a atuação do dispositivo cs

um dispositivo de proteção na origem (lado da fonte) (de cada condutor); 2) utilizar, no caso de mais de dois condutores em paralelo, um dispositivo na origem (lado da fonte) e outro no final (lado da carga) (de cada condutor). Resumindo: se a atuação de uma proteção única contra correntes de curto-circuito não puder ser garantida, no caso de falta num dos condutores em paralelo, convém optar pela proteção individual, sendo que no caso de três ou mais condutores em paralelo pode ser necessário prever proteções individuais na entrada e na saída do circuito, como ilustram as figuras 1 e 2. A figura 1 mostra que se ocorre uma falta no condutor paralelo c, no ponto x, a corrente de falta circulará pelos condutores a, b e c. A maior parte dessa corrente passará pela proteção cs. A figura 2 mostra que mesmo após a atuação de cs circulará corrente para a falta, em x, pelos condutores a e b. Por estarem a e b em paralelo, a corrente que passa pelas proteções as e bs pode não ser suficiente para fazê-las atuar em tempo hábil. Nessas condições a proteção cl será necessária. Note-se que a corrente através de cl será inferior à que causou a atuação de cs. A mesma situação existirá se a falta ocorrer no condutor a ou b e, portanto, serão necessárias as proteções al e bl.

## Relatório de extração

- Páginas processadas: 28.
- Figuras/diagramas referenciados: 17.
- Tabelas em grade reconstruídas em Markdown: 3.
- Páginas com elementos vetoriais complexos sinalizados pelo diagnóstico: 1.
- Modo: verbatim-limpo; cabeçalhos, rodapés, copyright recorrente e números de página foram removidos.
- A hierarquia foi inferida conservadoramente por tamanho/peso da fonte e posição; descrições geradas estão explicitamente marcadas.
