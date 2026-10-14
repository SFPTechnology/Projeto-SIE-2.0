# Explicacao do Simulador de Cenarios de Queda de Tensao

Data: 2026-07-30  
Base analisada: capturas `Screenshot_216.jpg` e `Screenshot_217.jpg`, stories `MOD-QT-2-01`, `MOD-QT-2-02` e `MOD-QT-2-03`.

## 1. Objetivo da tela

O simulador compara a queda de tensao do circuito atual com cenarios alternativos de secao de condutor. A tela ajuda o usuario a responder:

1. Quanto o circuito terminal esta perdendo em tensao.
2. Quanto a instalacao perde no total, somando alimentador e circuito terminal.
3. Se o circuito atende aos limites normativos configurados.
4. Qual seria o efeito de aumentar a secao do cabo.
5. Se a sugestao pode ser aplicada como override auditado.

O ponto central e que a tela nao mostra apenas a queda isolada do circuito. Ela mostra tambem a queda acumulada:

```text
queda total (%) = queda do alimentador (%) + queda do circuito terminal (%)
```

Nas duas imagens, o limite do circuito terminal e 4,0% e o limite total aplicado e 5,0%.

## 2. Estrutura visual da tela

Cada captura tem os mesmos blocos funcionais:

1. Titulo do simulador, identificando o circuito analisado.
2. Grafico de barras com a queda por cenario.
3. Linhas horizontais de limite: 4,0% para o circuito e 5,0% para o total.
4. Bloco de queda acumulada, mostrando a soma alimentador + circuito.
5. Campo de justificativa da aplicacao do cenario.
6. Lista de cenarios CEN-01, CEN-02 e CEN-03.
7. Botao de aplicar cenario.
8. Rodape de rastreabilidade tecnica, com metodo, impedancia, comprimento, corrente, tensao, norma, fonte e alertas.

## 3. Grafico de barras

O grafico mostra a queda de tensao do circuito terminal em percentual (`Delta V %`) para quatro situacoes:

| Barra | Significado |
|---|---|
| Atual | Resultado calculado para a secao atual do circuito |
| CEN-01 | Resultado se a primeira secao sugerida fosse aplicada |
| CEN-02 | Resultado se a segunda secao sugerida fosse aplicada |
| CEN-03 | Resultado se a terceira secao sugerida fosse aplicada |

As barras ficam pequenas porque os valores do circuito terminal estao bem abaixo das linhas de limite. O problema, quando existe, pode estar na soma com o alimentador.

### Linhas de limite

O grafico exibe duas referencias:

| Linha | Valor | Funcao |
|---|---:|---|
| Limite circuito | 4,0% | Limite para a queda do circuito terminal |
| Limite total | 5,0% | Limite para alimentador + circuito |

Isso e importante porque um circuito pode ter queda terminal baixa e ainda assim ficar reprovado no total se o alimentador ja consumir grande parte do limite.

## 4. Formula conceitual da queda de tensao

As stories do projeto registram o motor `MOD-QT-v2.2` com calculo real de queda de tensao. O calculo usa impedancia do cabo, comprimento, corrente, tensao e numero de fases.

Forma simplificada, usada quando a reatancia nao e determinante:

```text
Delta V (%) = (k x Ib x R x L / 1000) / V x 100
```

Forma completa, quando o perfil de impedancia inclui resistencia e reatancia:

```text
Delta V (%) = (k x Ib x (R x cos(phi) + X x sen(phi)) x L / 1000) / V x 100
```

Onde:

| Simbolo | Significado |
|---|---|
| `Delta V (%)` | queda de tensao percentual |
| `k` | fator do numero de fases: monofasico/bifasico/trifasico |
| `Ib` | corrente de projeto do circuito, em A |
| `R` | resistencia do cabo, em ohm/km |
| `X` | reatancia do cabo, em ohm/km |
| `L` | comprimento do trecho, em m |
| `V` | tensao nominal, em V |
| `cos(phi)` | fator de potencia |
| `sen(phi)` | componente reativa associada ao fator de potencia |

Nas capturas, o rodape indica metodo simplificado (`MOD-QT-v2.2; simplificado`), perfil Prysmian e tensao de 220 V.

## 5. Como a secao altera o resultado

A simulacao aumenta a secao do condutor. Em geral, quanto maior a secao em mm2, menor a resistencia eletrica do cabo e menor a queda de tensao.

Isso aparece claramente nas duas telas:

| Circuito | Atual | CEN-01 | CEN-02 | CEN-03 |
|---|---:|---:|---:|---:|
| Ar-condicionado | 0,67% aprox. | 0,44% | 0,31% | 0,21% |
| Banheira Hidro | 0,43% aprox. | 0,29% | 0,17% | 0,10% |

O grafico arredonda os rotulos para uma casa decimal em alguns pontos, enquanto a tabela de cenarios mostra valores com duas casas. Por isso o Ar-condicionado aparece como `0.7%` no grafico e como `0.67%` no detalhamento.

## 6. Captura 1: Ar-condicionado

### 6.1 Dados principais

Titulo: `Simulador de cenarios - Ar-condicionado`

Rodape tecnico visivel:

| Campo | Valor apresentado |
|---|---|
| Metodo | `MOD-QT-v2.2; simplificado` |
| Resistencia usada | `R=1.540/km` |
| Comprimento | `L=30m` |
| Corrente | `IB=15.981818181818182A` |
| Tensao | `V=220V` |
| Limite do circuito | `4% CONFIRMADO` |
| Norma | `NBR5410:2004 secao 6.2.7` |
| Fonte do cabo | Prysmian Brasil, Guia de Dimensionamento de Cabos para Baixa Tensao, Rev. 10, Tabela 32, p. 37 |
| Perfil | `PRYSMIAN_BT_REV10|T32|GSette Easy (cobre) e Afumex Flex (cobre)|CU|16|2_UNIPOLARES_S_2D` |
| Limite total | `5% CONFIRMADO` |
| Alertas | `alertas=1` |

### 6.2 Queda acumulada

A tela mostra:

```text
Origem => Alimentador: Delta V = 6.12%
Ar-condicionado: Delta V alim 6.12% + Delta V circ 0.67% = 6.79%
limite total 5.0%
Status: ACIMA
```

Passo a passo:

1. O alimentador ja possui queda de `6,12%`.
2. O circuito terminal do Ar-condicionado possui queda de aproximadamente `0,67%`.
3. A queda total e a soma:

```text
6,12% + 0,67% = 6,79%
```

4. O limite total configurado e `5,0%`.
5. Como `6,79% > 5,0%`, o status e `ACIMA`.

### 6.3 Por que o circuito aparece reprovado se a barra esta abaixo de 4%

A barra do circuito terminal esta abaixo de 4,0%. Portanto, isoladamente, o circuito terminal nao excede o limite do circuito.

O problema esta no acumulado:

```text
queda total = alimentador + circuito
queda total = 6,12% + 0,67% = 6,79%
```

Como o alimentador sozinho ja esta acima de 5,0%, aumentar a secao do circuito terminal reduz a queda do circuito, mas nao consegue fazer a soma total voltar para dentro do limite.

### 6.4 Cenarios simulados

| Cenario | Acao sugerida | Queda do circuito | Queda total | Status | Mudanca |
|---|---|---:|---:|---|---|
| CEN-01 | Subir secao para 25 mm2 | 0,44% | 6,55% | ACIMA | 16 -> 25 |
| CEN-02 | Subir secao para 35 mm2 | 0,31% | 6,43% | ACIMA | 16 -> 35 |
| CEN-03 | Subir secao para 50 mm2 | 0,21% | 6,33% | ACIMA | 16 -> 50 |

Calculo conferido pela tela:

```text
CEN-01: 6,12% + 0,44% = 6,56% aprox. exibido como 6,55%
CEN-02: 6,12% + 0,31% = 6,43%
CEN-03: 6,12% + 0,21% = 6,33%
```

A pequena diferenca de centesimos decorre de arredondamento visual. O motor calcula com mais precisao e a interface exibe percentuais arredondados.

### 6.5 Interpretacao tecnica

O aumento de secao funciona do ponto de vista do circuito terminal: a queda cai de `0,67%` para `0,21%` no melhor cenario exibido.

Porem, a causa principal da reprova e o alimentador com `6,12%`. Mesmo no melhor cenario:

```text
6,12% + 0,21% = 6,33%
```

O resultado continua acima de 5,0%. Assim, para aprovar esse caso, nao basta aumentar a secao do circuito terminal. E necessario revisar tambem o alimentador, a origem do limite aplicado, o comprimento, a secao do alimentador ou outro parametro que reduza a queda antes do circuito.

## 7. Captura 2: Banheira Hidro

### 7.1 Dados principais

Titulo: `Simulador de cenarios - Banheira Hidro`

Rodape tecnico visivel:

| Campo | Valor apresentado |
|---|---|
| Metodo | `MOD-QT-v2.2; simplificado` |
| Resistencia usada | `R=6.310/km` |
| Comprimento | `L=10m` |
| Corrente | `IB=7.5A` |
| Tensao | `V=220V` |
| Limite do circuito | `4% CONFIRMADO` |
| Norma | `NBR5410:2004 secao 6.2.7` |
| Fonte do cabo | Prysmian Brasil, Guia de Dimensionamento de Cabos para Baixa Tensao, Rev. 10, Tabela 32, p. 37 |
| Perfil | `PRYSMIAN_BT_REV10|T32|GSette Easy (cobre) e Afumex Flex (cobre)|CU|4|2_UNIPOLARES_S_2D` |
| Limite total | `5% CONFIRMADO` |
| Alertas | `alertas=1` |

### 7.2 Queda acumulada

A tela mostra:

```text
Origem => Alimentador: Delta V = 2.87%
Banheira Hidro: Delta V alim 2.87% + Delta V circ 0.43% = 3.30%
limite total 5.0%
Status: OK
```

Passo a passo:

1. O alimentador possui queda de `2,87%`.
2. O circuito terminal da Banheira Hidro possui queda de aproximadamente `0,43%`.
3. A queda total e:

```text
2,87% + 0,43% = 3,30%
```

4. O limite total e `5,0%`.
5. Como `3,30% <= 5,0%`, o status e `OK`.

### 7.3 Cenarios simulados

| Cenario | Acao sugerida | Queda do circuito | Queda total | Status | Mudanca |
|---|---|---:|---:|---|---|
| CEN-01 | Subir secao para 6 mm2 | 0,29% | 3,16% | OK | 4 -> 6 |
| CEN-02 | Subir secao para 10 mm2 | 0,17% | 3,04% | OK | 4 -> 10 |
| CEN-03 | Subir secao para 16 mm2 | 0,10% | 2,98% | OK | 4 -> 16 |

Calculo conferido pela tela:

```text
CEN-01: 2,87% + 0,29% = 3,16%
CEN-02: 2,87% + 0,17% = 3,04%
CEN-03: 2,87% + 0,10% = 2,97% aprox. exibido como 2,98%
```

### 7.4 Interpretacao tecnica

Este caso ja atende ao limite total na condicao atual:

```text
3,30% <= 5,00%
```

Os cenarios reduzem ainda mais a queda, mas nao sao necessarios para sair de uma nao conformidade. A decisao de aplicar uma secao maior pode depender de outro criterio de projeto, como padronizacao, margem operacional, temperatura, disponibilidade de cabo ou criterio economico. Pela queda de tensao, o circuito ja esta aprovado.

## 8. Status OK e ACIMA

A tela usa dois estados principais:

| Status | Significado |
|---|---|
| `OK` | O valor comparado esta dentro do limite aplicado |
| `ACIMA` | O valor comparado excede o limite aplicado |

Nas capturas, o status principal esta comparando a queda total com o limite total de 5,0%.

```text
OK     quando Delta V total <= limite total
ACIMA  quando Delta V total > limite total
```

Por isso:

```text
Ar-condicionado: 6,79% > 5,0% -> ACIMA
Banheira Hidro: 3,30% <= 5,0% -> OK
```

## 9. Botao Aplicar Cenario

Cada linha tem um botao `Aplicar CEN-01`, `Aplicar CEN-02` ou `Aplicar CEN-03`.

Segundo a story `MOD-QT-2-02`, aplicar um cenario deve:

1. Gravar a nova secao ou comprimento no circuito.
2. Disparar recalculo do MOD-DC com a secao aplicada como piso.
3. Registrar justificativa com valores antes/depois.
4. Gerar override auditado pela regra R-11.

O campo de justificativa existe para explicar por que o projetista esta aplicando a alteracao. O placeholder exibido e:

```text
Ex.: secao elevada para atender Delta V do circuito terminal
```

Em termos de auditoria, a acao nao deve ser silenciosa. O sistema precisa guardar a mudanca, por exemplo:

```text
antes: secao 16 mm2, Delta V circ 0,67%, Delta V total 6,79%
depois: secao 25 mm2, Delta V circ 0,44%, Delta V total 6,55%
justificativa: texto informado pelo usuario
```

## 10. Por que alguns botoes parecem desabilitados

Nas capturas, os botoes aparecem com baixo contraste visual, sugerindo estado desabilitado ou nao interativo naquele momento.

Motivos provaveis, coerentes com a propria tela:

1. A justificativa ainda nao foi preenchida.
2. O cenario nao resolve a nao conformidade total, como no Ar-condicionado.
3. A aplicacao exige confirmacao ou estado de edicao nao mostrado na captura.
4. O ambiente da captura pode estar em modo demonstrativo ou leitura.

Esta leitura e inferencial a partir da interface; as imagens nao mostram tooltip, mensagem de validacao ou evento de clique.

## 11. Rodape de rastreabilidade

O rodape e essencial para o usuario tecnico porque explica de onde veio o resultado.

Ele registra:

| Item | Funcao |
|---|---|
| Versao do modulo | Identifica o motor usado, `MOD-QT-v2.2` |
| Metodo | Indica se o calculo foi simplificado ou completo |
| R | Resistencia do cabo usada no calculo |
| L | Comprimento considerado |
| IB | Corrente de projeto |
| V | Tensao nominal |
| Limite do circuito | Confirma o criterio de 4% |
| Norma | Referencia NBR 5410:2004 secao 6.2.7 |
| Fonte do cabo | Referencia ao catalogo Prysmian |
| Perfil | Chave tecnica do registro de impedancia |
| Limite total | Confirma se o limite total aplicado e 5% ou 7% |
| Alertas | Quantidade de avisos tecnicos associados ao resultado |

Esse rodape evita que o resultado seja uma "caixa preta". O usuario consegue rastrear os parametros e a fonte usada para chegar ao percentual.

## 12. Comparacao entre as duas capturas

| Aspecto | Ar-condicionado | Banheira Hidro |
|---|---:|---:|
| Queda do alimentador | 6,12% | 2,87% |
| Queda do circuito atual | 0,67% | 0,43% |
| Queda total atual | 6,79% | 3,30% |
| Limite total | 5,0% | 5,0% |
| Status atual | ACIMA | OK |
| Secao atual inferida | 16 mm2 | 4 mm2 |
| Melhor cenario exibido | 50 mm2 | 16 mm2 |
| Queda total no melhor cenario | 6,33% | 2,98% |
| Resultado dos cenarios | Continua ACIMA | Continua OK |

Conclusao operacional:

1. No Ar-condicionado, a queda do alimentador domina o problema. Aumentar apenas o circuito terminal melhora, mas nao aprova.
2. Na Banheira Hidro, o conjunto ja esta aprovado. Os cenarios apenas aumentam a margem.

## 13. Processo mental recomendado para o usuario

Ao usar essa tela, siga esta sequencia:

1. Leia o status da queda acumulada.
2. Compare `Delta V total` com o limite total.
3. Veja se a queda do circuito terminal esta abaixo de 4,0%.
4. Se o total estiver acima, identifique se a causa principal e o alimentador ou o circuito.
5. Compare os cenarios e observe se algum muda o status para `OK`.
6. So aplique um cenario se houver justificativa tecnica.
7. Confirme no rodape se os parametros e a fonte tecnica fazem sentido para o circuito analisado.

## 14. Resumo final

O simulador nao escolhe automaticamente a solucao. Ele calcula e apresenta alternativas tecnicas.

Na captura do Ar-condicionado, a simulacao mostra que aumentar a secao do circuito terminal reduz a queda local, mas nao resolve a nao conformidade total porque o alimentador ja excede o limite. Na captura da Banheira Hidro, a instalacao ja esta conforme, e os cenarios apenas reduzem a queda ainda mais.

O valor mais importante da tela e separar claramente tres coisas: queda do circuito, queda do alimentador e queda acumulada. Sem essa separacao, o usuario poderia aumentar a secao do circuito errado e continuar sem resolver a causa real da reprova.
