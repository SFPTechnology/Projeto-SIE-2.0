# F07 — Fontes, recorte e conferência independente

## Fonte obtida e integridade

- Fabricante/editor: **Prysmian**. Documento: *Guia de dimensionamento de cabos para baixa tensão*, arquivo oficial **Rev9**, 51 páginas.
- URL final: https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev9.pdf
- URL anterior do próprio fabricante redirecionou para a URL acima. Download observado: 3.172.193 bytes, PDF1.7, SHA256 **1729461681fa12bbfe03ea92d26dfb2299c148670d3133046a52f8caf311e4d7**.
- Conferência: **22/10/2026**. Metadados PDF: criação22/09/2020 e modificação23/09/2020. Isso identifica o arquivo; não declara publicação, vigência normativa ou licença de redistribuição.
- O guia declara base NBR5410:2004. O catálogo oficial ABNT consultado identifica NBR5410:2004 versão corrigida2008: https://www.abntcatalogo.com.br/default.aspx?O=1 . A regra computacional é um vínculo documental finito; não equivale a acesso/homologação de todos os requisitos ABNT.
- PDF e imagens foram usados temporariamente para conferência, sem redistribuí-los no repositório público. Persistidos somente fatos técnicos necessários, URL/hash, condições e referências.

## Matriz fonte → dado → aplicação

|Dado|Página impressa / referência|Recorte vinculado|
|---|---|---|
|Produto e tensão de isolamento|3, tabela1|Superastic Cu/PVC450/750V; FN≤450V e FF≤750V, sem inferir tensão para terra em FF>450V|
|Mínimo fase|5, tabela2, primeira categoria de condutores/cabos isolados|Instalação fixa comum: iluminação1,5Cu; força/tomadas2,5Cu. Aplicações especiais não entram|
|Neutro|5, seção4.2/tabela3|Mesma seção e metal da fase; sem redução, regime senoidal sem harmônicas relevantes|
|PE|6, seção4.3/tabela4|Mesmo metal, S≤16→PE≥S. Fora do mesmo cabo/conduto fechado: pisoCu2,5 com proteção mecânica ou4 sem proteção|
|Método|7, tabela5|B1 métodos3/5/7 no recorte aceito, condutores isolados em condutoPVC|
|Iz|9, tabela7, coluna6, cobre|PVC70°C, B1, dois carregados, ambiente30°C|
|Temperatura|14, tabela11 e condição-basep9|30°C→1;40°C→0,87, sem interpolação/extrapolação|
|Agrupamento|15, tabela13 ref1, notas1/3|1/2/3circuitos→1/0,80/0,70. Cada membro do feixe identificado; mesmaIb e mesma seção preservadas pela seleção|
|Trecho crítico|19, seção5.7.7|Avaliação de cada trecho; não média de fatores|
|Limites|20, seção6.1, casoC e nota1|Total desde ponto de entregaBT≤5%; trecho/circuito terminal≤4% independentemente do total|
|ModeloAC|21, seção6.2|2·Lkm·I·(Rca·cosφ+XL·senφ) mono; sem retorno desigual, harmônicas ou cálculo transitório|
|Rca/XL|33, tabela28, primeiro par de colunas|SuperasticCu, dois carregados encostados,60Hz,70°C; exclui conduto metálico fechado ferromagnético|
|Referência pré-calculada|24, tabela19, primeiro par de colunas|Coeficientes V/(A.km), cosφ0,8/0,95 para confronto independente com Rca/XLp33|

## Catálogo finito e relação com F01

|Seção mm²|Iz base A|Rca Ω/km|XL Ω/km|Referência p24: FP0,80 / FP0,95 V/(A.km)|
|---|---:|---:|---:|---:|
|2,5|24|8,87|0,12|14,33 /16,93|
|4|32|5,52|0,11|8,96 /10,56|
|6|41|3,69|0,10|6,03 /7,07|
|10|57|2,19|0,10|3,63 /4,23|

As quatro capacidades e fatores são concordantes com CEL01–05/07/08 da F01. O resolver F01 é reaproveitado, mantendo seus aceites, revisão e hashes. O novo catálogo acrescenta parâmetros e referências F07; não altera nem reabre a F01. Combinações sem dados são bloqueadas em vez de usar o otimizador legado ou extrapolação.

Conferência visual: executor, agente pai e QA02 verificaram as páginas pertinentes; QA02 registrou inspeção de11páginas. Isso é revisão de agentes de software, sem atribuição de assinatura humana, ART ou aprovação de concessionária.

## Casos independentes e precisão

O algoritmo usa dados Rca/XL da tabela28(p33). O confronto de referência usa outra tabela, pré-calculada pelo fabricante: tabela19(p24). Não se geraram os valores esperados chamando o algoritmo testado. Os pares R/X e os coeficientes estão impressos com0,01 de resolução. O erro propagado de confronto é limitado por0,005·[2·(cosφ+senφ)+1], menor que0,02V/(A.km). **Essa tolerância serve somente para comparar tabelas arredondadas; não aumenta os limites4%/5%.**

Caso aritmético independente com Fraction:10A,100m,220V,cosφ4/5 e senφ3/5. Quedas nas seções2,5/4/6/10 são1792/125,2241/250,753/125,453/125V. A primeira seção do catálogo que atende queda local4% é6mm²:4mm² resulta2241/550%=4,0745...;6mm² resulta753/275%=2,73818... . O seletor reproduz essa transição e avalia também capacidade, fase/N/PE e queda acumulada.

Fixtures versionadas: catálogo `data/conductor_prysmian_rev9_f07.json` inclui a referência tabulada; `tests/test_conductor_binding_f07.py` contém casos independentes, fontes e expectativas racionais; o exemplo `examples/f07_selecao_fonte_vinculada.json` simula uma instalação, usando parâmetros técnicos reais resolvidos pelo servidor. A instalação de exemplo não é uma obra real nem um projeto homologado.

## Limites do recorte

- ProdutoSuperasticCu/PVC, B1 métodos3/5/7,60Hz/70°C, ambiente30/40°C, seções2,5/4/6/10, dois carregados encostados em condutoPVC; conexõesFN/FF explícitas, TT ouTN-S.
- Membros de cada feixe precisam ser informados; seleção mantém mesma seção e exige mesma corrente. Agrupamento externo desconhecido não é presumido homogêneo.
- Identidade de fases, base de tensão e cosφ devem coincidir ao longo da cadeia para soma longitudinal. Outros casos requerem modelo fora deste recorte.
- Sem paralelos, alternativas, PEN, alumínio, outra isolação/produto, instalação especial, harmônicas, desequilíbrio ou regime transitório. Não há fator/Rca presumidos.
- Data de referência2020-09-23 a2026-10-22 é um limite conservador do uso desta fotografia documental, não declaração de início/fim de vigência da NBR.
- Seleção é proposta computacional F07. Curto-circuito, sobrecarga e proteção contra choques são verificações F08; `normative_conformity_verified=false`, `authoritative_for_sizing=false` e `f08_protection_checks_pending=true` continuam explícitos.
