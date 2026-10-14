# Pesquisa técnica — Tabelas 001 e 002 do Padrão EDP

**Arquivo:** `tabelas_001_002_padrao_edp.md`  
**Data da consolidação:** 20/06/2026  
**Fonte normativa principal:** EDP São Paulo — `PT.DT.PDN.00068`, versão 09  
**Título do documento:** *Fornecimento de Energia Elétrica em Tensão Secundária de Distribuição – Unidade Consumidora Individual*  
**Vigência inicial identificada:** 14/04/2026  
**Classificação:** Padrão Técnico — Pública  
**URL consultada:** https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf

---

## 1. Objetivo desta consolidação

Este documento consolida, em formato técnico e estruturado, as informações oficiais das **Tabelas 001 e 002** do padrão técnico da EDP para atendimento de unidades consumidoras individuais em tensão secundária de distribuição.

O objetivo é disponibilizar uma base técnica clara para uso em:

- validação de sistemas automatizados de projeto elétrico;
- construção de regras de enquadramento de categoria de atendimento;
- definição de proteção de entrada principal;
- definição do tipo de medição;
- seleção de condutores de entrada;
- seleção de eletrodutos;
- seleção de caixa de medição/proteção;
- definição de poste e poste com caixa incorporada;
- definição de condutor e eletroduto de aterramento;
- verificação de limite de motores por categoria;
- validação de instalações com microgeração distribuída — MMGD.

> **Nota técnica:** este arquivo é uma consolidação estruturada da pesquisa realizada. Em caso de divergência, alteração normativa ou exigência específica da distribuidora, prevalece sempre o documento oficial vigente da EDP e a análise formal da concessionária.

---

## 2. Documento oficial identificado

| Campo | Informação |
|---|---|
| Distribuidora | EDP São Paulo |
| Código do padrão | PT.DT.PDN.00068 |
| Versão | 09 |
| Vigência inicial | 14/04/2026 |
| Título | Fornecimento de Energia Elétrica em Tensão Secundária de Distribuição – Unidade Consumidora Individual |
| Tipo | Padrão Técnico |
| Classificação da informação | Pública |
| Número de páginas do PDF consultado | 91 |
| Fonte | https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf |

---

## 3. Escopo de aplicação do padrão

O padrão técnico é aplicável ao fornecimento de energia elétrica em **tensão secundária de distribuição** para **unidade consumidora individual** na área de concessão da **EDP São Paulo**.

Aplica-se, conforme o padrão, a instalações:

- residenciais;
- comerciais;
- industriais;
- urbanas;
- rurais;
- de características usuais;
- com carga instalada até **75 kW**;
- ligadas às redes aéreas secundárias de distribuição da EDP São Paulo;
- em instalações novas;
- em ligações provisórias, quando aplicável;
- em praças e jardins, quando aplicável;
- em reformas ou mudanças de padrão de entrada, conforme as condições técnicas e de segurança.

O padrão também indica que, nos casos de atendimento por **rede subterrânea de distribuição**, o interessado deve observar o padrão técnico específico de **Ramal de Entrada Subterrâneo – Baixa Tensão**.

---

## 4. Referências normativas e regulatórias citadas no padrão

O padrão técnico da EDP indica a necessidade de consulta aos seguintes documentos externos:

| Referência | Descrição |
|---|---|
| ABNT NBR 5410 | Instalações elétricas de baixa tensão |
| ABNT NBR 7285 | Cabos de potência com isolação extrudada de polietileno termofixo — XLPE — para tensão de 0,6/1 kV |
| ABNT NBR 10676 | Fornecimento de energia a edificações individuais em tensão secundária |
| ABNT NBR 13570 | Instalações elétricas em locais de afluência de público — requisitos específicos |
| ABNT NBR 15465 | Sistemas de eletrodutos plásticos para instalações elétricas de baixa tensão — requisitos de desempenho |
| ABNT NBR 15820 | Caixa para medidor de energia elétrica — requisitos |
| ABNT NBR NM 60898 | Disjuntores para proteção de sobrecorrentes para instalações domésticas e similares |
| ABNT NBR IEC 60947-2 | Dispositivos de manobra e comando de baixa tensão — disjuntores |
| ABNT NBR NM 247-3 | Cabos isolados com PVC para tensões nominais até 450/750 V |
| ANEEL Resolução Normativa nº 1000/2021 | Regras de prestação do serviço público de distribuição de energia elétrica |
| PRODIST — Módulo 8 | Qualidade do fornecimento de energia elétrica |
| ABNT NBR 16690:2019 | Instalações elétricas de arranjos fotovoltaicos — citada no contexto de MMGD |

---

## 5. Sistemas e tensões nominais de fornecimento

O padrão técnico informa que a EDP São Paulo fornece energia elétrica em tensão secundária de distribuição, frequência nominal de **60 Hz**, nos seguintes sistemas:

| Sistema | Tensões nominais |
|---|---|
| Estrela com neutro aterrado | 220/127 V |
| Delta com neutro aterrado | 240/120 V |

### Observação sobre sistema delta com neutro

No sistema delta com neutro, a fase de força, também indicada como quarto fio, deve ser utilizada **somente** para alimentação de cargas trifásicas, mantendo a mesma seção dos condutores das fases.

---

## 6. Limite de fornecimento em tensão secundária

A EDP estabelece que o fornecimento em tensão secundária de distribuição é aplicado a instalações com **carga instalada igual ou inferior a 75 kW**, observadas as exceções regulamentares aplicáveis.

Instalações com carga instalada superior a esse valor tendem a ser atendidas em **tensão primária de distribuição**, conforme a legislação vigente. Para atendimento de carga superior a 75 kW em tensão secundária, o cliente deve consultar a concessionária para análise de viabilidade técnica.

---

## 7. Categorias de atendimento

O padrão define três modalidades principais de atendimento:

| Categoria / modalidade | Sistema | Descrição |
|---|---|---|
| U | Monofásico | Dois fios: 1 fase + 1 neutro — FN |
| D | Bifásico | Três fios: 2 fases + 1 neutro — FFN |
| T | Trifásico | Quatro fios: 3 fases + 1 neutro — FFFN |

Os tipos de fornecimento são definidos em função de:

- carga instalada;
- demanda calculada;
- tipo de rede disponível;
- local onde está situada a unidade consumidora;
- tensão nominal dos equipamentos;
- existência de cargas especiais;
- existência de motores;
- existência de equipamentos trifásicos;
- enquadramento técnico pela concessionária.

---

## 8. Aplicação geral das categorias U, D e T

### 8.1 Categoria U — monofásica

| Item | Informação |
|---|---|
| Categoria | U |
| Sistema | Monofásico |
| Condutores | Dois fios — fase + neutro |
| Sigla técnica | FN |
| Aplicação geral | Instalações com carga instalada até 12 kW |
| Sistemas possíveis | Estrela com neutro ou delta com neutro |
| Condições não permitidas | Instalação de aparelhos de raio X ou máquinas de solda a transformador |

### 8.2 Categoria D — bifásica

| Item | Informação |
|---|---|
| Categoria | D |
| Sistema | Bifásico |
| Condutores | Três fios — duas fases + neutro |
| Sigla técnica | FFN |
| Aplicação em estrela com neutro | Instalações com carga instalada acima de 12 kW até 25 kW |
| Aplicação em delta com neutro | Instalações com carga instalada acima de 12 kW até 75 kW |
| Condições não permitidas | Máquina de solda a transformador em 220 V superior a 10 kVA; aparelho de raio X em 220 V com potência superior a 1500 W |

### 8.3 Categoria T — trifásica

| Item | Informação |
|---|---|
| Categoria | T |
| Sistema | Trifásico |
| Condutores | Quatro fios — três fases + neutro |
| Sigla técnica | FFFN |
| Aplicação em estrela com neutro | Instalações com carga instalada acima de 25 kW até 75 kW |
| Aplicação em delta com neutro | Instalações com carga instalada acima de 12 kW até 75 kW, somente quando houver equipamentos trifásicos |
| Condições não permitidas | Máquina de solda a transformador em 220 V com potência maior que 10 kVA; máquina de solda trifásica com retificação em ponte superior a 30 kVA; aparelho de raio X em 220 V superior a 1500 W; aparelho de raio X trifásico superior a 20 kVA |

---

## 9. Observações técnicas sobre cargas especiais e motores

O padrão prevê que, quando existirem aparelhos com potências superiores aos limites indicados, deve ser apresentado **estudo técnico detalhado** das características dos equipamentos para análise da área técnica da EDP São Paulo.

Também é previsto que, no caso de motores maiores que os especificados na:

- **Tabela 001:** limite geral de até 5 cv para motor FF;
- **Tabela 002:** limite geral de até 60 cv para motor FFF;

poderá ser solicitado enquadramento em uma das categorias de atendimento, mas deverá ser apresentado estudo técnico detalhado das características nominais do motor e do sistema de partida. A área técnica da EDP avaliará os impactos sobre a rede de distribuição e sobre os demais clientes.

---

## 10. Critério de medição direta e indireta

| Critério | Tipo de medição | Observação |
|---|---|---|
| Corrente de demanda até 150 A | Direta | Aplicável conforme Tabelas 001 e 002 |
| Corrente de demanda superior a 150 A | Indireta | Exige documento de responsabilidade técnica de execução do padrão de entrada junto à solicitação de pedido de ligação |

### Observação para D6 e T6

Para as categorias **D6** e **T6**, o padrão exige que o cliente deixe, no interior da caixa de medição, **600 mm de cabo de seção nominal de 4 mm², classe 5, com isolação azul-claro**, conectado ao condutor neutro por conector tipo parafuso fendido.

---

## 11. Localização da medição

A medição deve ser instalada:

- em local de fácil acesso;
- no limite da propriedade do consumidor com a via pública;
- com leitura e acesso à proteção voltados para a calçada, em ligações novas ou reformas.

O padrão indica que não são aceitos locais como:

- copas;
- cozinhas;
- dependências sanitárias;
- interior de vitrines;
- áreas entre prateleiras;
- pavimento superior de edificações;
- locais com iluminação inadequada;
- locais sem condições de segurança;
- proximidades de máquinas, bombas, tanques ou reservatórios;
- escadarias;
- locais sujeitos a gases corrosivos ou explosivos;
- locais sujeitos a inundações;
- locais sujeitos a trepidações excessivas.

---

## 12. Caixas de medição e proteção

O padrão estabelece que somente serão aceitas caixas de medição cujos protótipos tenham sido cadastrados pela concessionária.

Regras associadas:

- a relação de fabricantes e materiais cadastrados deve ser consultada junto à EDP;
- em caixas metálicas, é obrigatória a instalação de pingadeira;
- caixas poliméricas devem possuir visor de vidro, conforme exigências do padrão técnico.

---

# 13. Tabela 001 — Definição da categoria de atendimento “U” e “D”

**Descrição oficial:** definição da categoria de atendimento **“U”** — monofásica, 1 fase + 1 neutro — e **“D”** — bifásica, 2 fases + 1 neutro.

| Parâmetro | U2 | D2 | D4 | D6 | D7 | D9 | D10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Categoria-base | U | D | D | D | D | D | D |
| Sistema | FN | FFN | FFN | FFN | FFN | FFN | FFN |
| Nº de fases | 1 | 2 | 2 | 2 | 2 | 2 | 2 |
| Neutro | Sim | Sim | Sim | Sim | Sim | Sim | Sim |
| Disjuntor da entrada principal | 70 A | 63 A | 100 A | 150 A | 200 A | 300 A | 350 A |
| Fusível NH / chave | — | — | — | — | 160 A com chave de 250 A | 250 A com chave de 400 A | 315 A com chave de 400 A |
| Tipo de medição | Direta | Direta | Direta | Direta | Indireta | Indireta | Indireta |
| Condutor de entrada — PVC — fase e neutro | Responsabilidade da distribuidora | Responsabilidade da distribuidora | 35 mm² | 70 mm² | 95 mm² | 185 mm² | 240 mm² |
| Condutor de entrada — EPR/XLPE — fase e neutro | Responsabilidade da distribuidora | Responsabilidade da distribuidora | 25 mm² | 50 mm² | 70 mm² | 120 mm² | 185 mm² |
| Caixa | II, III, E ou Modular | II, III, E ou Modular | II, III, E ou Modular | 380 e Modular; ou 570 e Modular; ou conjunto de 3 caixas 520 × 260 mm | H ou M + T; ou Modular | M + T; ou Modular | M + T; ou Modular |
| Eletroduto de entrada | PVC 32 mm | PVC 32 mm | PVC 40 mm | PVC 60 mm | PVC 75 mm | PVC 85 mm | PVC 85 mm |
| Poste | Concreto ou aço galvanizado — 90 daN | Concreto ou aço galvanizado — 90 daN | Concreto ou aço galvanizado — 200 daN | Concreto — 300 daN | Concreto — 300 daN | Concreto — 300 daN | Concreto — 300 daN |
| Poste com caixa incorporada | PCI-1 | PCI-1 | — | — | — | — | — |
| Aterramento — condutor PVC | 16 mm² | 16 mm² | 16 mm² | 35 mm² | 50 mm² | 95 mm² | 120 mm² |
| Aterramento — condutor EPR/XLPE | 16 mm² | 16 mm² | 16 mm² | 25 mm² | 35 mm² | 70 mm² | 95 mm² |
| Aterramento — eletroduto | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 25 mm |
| Maior motor FN | 1 cv | 1 cv | 1 cv | 1 cv | 1 cv | 1 cv | 1 cv |
| Maior motor FF | — | 3 cv | 3 cv | 3 cv | 5 cv | 5 cv | 5 cv |

---

## 14. Interpretação técnica da Tabela 001

### 14.1 Enquadramento por categoria

A Tabela 001 deve ser utilizada quando a unidade consumidora for atendida por modalidade:

- **U:** monofásica — fase + neutro;
- **D:** bifásica — duas fases + neutro.

A categoria específica, por exemplo **U2**, **D2**, **D4**, **D6**, **D7**, **D9** ou **D10**, define simultaneamente:

- corrente nominal do disjuntor de entrada;
- necessidade ou não de fusível NH;
- tipo de medição;
- bitola dos condutores de entrada;
- tipo de caixa;
- diâmetro do eletroduto de entrada;
- tipo/capacidade do poste;
- existência ou não de PCI;
- seção do condutor de aterramento;
- diâmetro do eletroduto de aterramento;
- limite de motor FN e FF.

### 14.2 Categorias com medição direta

Na Tabela 001, possuem medição direta:

| Categoria | Disjuntor |
|---|---:|
| U2 | 70 A |
| D2 | 63 A |
| D4 | 100 A |
| D6 | 150 A |

### 14.3 Categorias com medição indireta

Na Tabela 001, possuem medição indireta:

| Categoria | Disjuntor | Fusível NH / chave |
|---|---:|---|
| D7 | 200 A | 160 A com chave de 250 A |
| D9 | 300 A | 250 A com chave de 400 A |
| D10 | 350 A | 315 A com chave de 400 A |

---

# 15. Tabela 002 — Definição da categoria de atendimento “T”

**Descrição oficial:** definição da categoria de atendimento **“T”** — trifásica, 3 fases + neutro.

| Parâmetro | T2 | T4 | T6 | T7 | T9 | T10 |
|---|---:|---:|---:|---:|---:|---:|
| Categoria-base | T | T | T | T | T | T |
| Sistema | FFFN | FFFN | FFFN | FFFN | FFFN | FFFN |
| Nº de fases | 3 | 3 | 3 | 3 | 3 | 3 |
| Neutro | Sim | Sim | Sim | Sim | Sim | Sim |
| Disjuntor da entrada principal | 63 A | 100 A | 150 A | 200 A | 300 A | 350 A |
| Fusível NH / chave | — | — | — | 160 A com chave de 250 A | 250 A com chave de 400 A | 315 A com chave de 400 A |
| Tipo de medição | Direta | Direta | Direta | Indireta | Indireta | Indireta |
| Condutor de entrada — PVC — fase e neutro | Responsabilidade da distribuidora | 35 mm² | 70 mm² | 95 mm² | 185 mm² | 240 mm² |
| Condutor de entrada — EPR/XLPE — fase e neutro | Responsabilidade da distribuidora | 25 mm² | 50 mm² | 70 mm² | 120 mm² | 185 mm² |
| Caixa | II, III, E ou Modular | III ou Modular | 380 e Modular; ou 570 e Modular; ou conjunto de 3 caixas 520 × 260 mm | H ou M + T; ou Modular | M + T; ou Modular | M + T; ou Modular |
| Eletroduto de entrada | PVC 32 mm | PVC 40 mm | PVC 60 mm | PVC 75 mm | PVC 85 mm | PVC 85 mm |
| Poste | Concreto ou aço galvanizado — 90 daN | Concreto ou aço galvanizado — 200 daN | Concreto — 300 daN | Concreto — 300 daN | Concreto — 300 daN | Concreto — 300 daN |
| Poste com caixa incorporada | PCI-1 | — | — | — | — | — |
| Aterramento — condutor PVC | 16 mm² | 16 mm² | 35 mm² | 50 mm² | 95 mm² | 120 mm² |
| Aterramento — condutor EPR/XLPE | 16 mm² | 16 mm² | 25 mm² | 35 mm² | 70 mm² | 95 mm² |
| Aterramento — eletroduto | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 20 mm | PVC 25 mm |
| Maior motor FN | 1 cv | 1 cv | 1 cv | 1 cv | 1 cv | 1 cv |
| Maior motor FF | 3 cv | 3 cv | 5 cv | 5 cv | 5 cv | 5 cv |
| Maior motor FFF | 8 cv | 15 cv | 25 cv | 30 cv | 60 cv | 60 cv |

---

## 16. Interpretação técnica da Tabela 002

### 16.1 Enquadramento por categoria

A Tabela 002 deve ser utilizada quando a unidade consumidora for atendida por modalidade:

- **T:** trifásica — três fases + neutro.

A categoria específica, por exemplo **T2**, **T4**, **T6**, **T7**, **T9** ou **T10**, define simultaneamente:

- corrente nominal do disjuntor de entrada;
- necessidade ou não de fusível NH;
- tipo de medição;
- bitola dos condutores de entrada;
- tipo de caixa;
- diâmetro do eletroduto de entrada;
- tipo/capacidade do poste;
- existência ou não de PCI;
- seção do condutor de aterramento;
- diâmetro do eletroduto de aterramento;
- limite de motor FN, FF e FFF.

### 16.2 Categorias com medição direta

Na Tabela 002, possuem medição direta:

| Categoria | Disjuntor |
|---|---:|
| T2 | 63 A |
| T4 | 100 A |
| T6 | 150 A |

### 16.3 Categorias com medição indireta

Na Tabela 002, possuem medição indireta:

| Categoria | Disjuntor | Fusível NH / chave |
|---|---:|---|
| T7 | 200 A | 160 A com chave de 250 A |
| T9 | 300 A | 250 A com chave de 400 A |
| T10 | 350 A | 315 A com chave de 400 A |

---

## 17. Observação oficial sobre MMGD — microgeração distribuída

As Tabelas 001 e 002 trazem observação específica sobre **microgeração distribuída — MMGD**.

A limitação para instalação de MMGD por categoria de fornecimento está associada ao critério de **demanda integral de geração**.

O dimensionamento da proteção da entrada principal deve considerar a **maior corrente** entre:

1. a corrente associada à geração distribuída; e
2. a corrente associada à carga instalada.

Esse dimensionamento deve observar as normas:

- **ABNT NBR 16690:2019**;
- **ABNT NBR 5410**.

O tipo de proteção adotado define a categoria de atendimento da unidade consumidora. Assim, pode ser necessária adequação do padrão de entrada para enquadramento na categoria correspondente.

---

## 18. Aterramento — regras associadas

O padrão técnico define que a entrada consumidora deve possuir ponto de aterramento destinado ao condutor neutro do ramal de entrada e à caixa de medição, quando metálica. Esse aterramento deve ser conectado antes do medidor.

Também informa que o condutor de proteção destinado ao aterramento de massa da instalação interna da unidade consumidora — PE, conforme NBR 5410 — deve ser interligado ao condutor PEN, desde que não exista dispositivo DR.

Nos padrões de entrada montados com PCI, o aterramento pode estar embutido no corpo do material, não sendo necessária, nesse caso, a instalação de caixa de aterramento, conforme configuração homologada.

---

## 19. Isolador roldana

O padrão técnico indica que deve ser instalado no poste ou fachada um conjunto de isolador roldana.

Exceções:

| Categoria | Quantidade exigida |
|---|---:|
| D9 | 2 conjuntos de isoladores |
| D10 | 2 conjuntos de isoladores |
| T10 | 2 conjuntos de isoladores |

Nos postes com caixa de medição incorporada podem ser utilizados parafusos tipo olhal, conforme homologação e cadastramento de fornecedores da EDP São Paulo.

---

## 20. Regras para dimensionamento do padrão de entrada

O padrão de entrada da unidade consumidora deve ser dimensionado com base na **corrente de demanda da instalação**.

Para ligações provisórias, deve ser considerado fator de demanda igual à unidade, ou seja, a demanda deve ser considerada como **100% da carga**.

Nos casos de pequenas indústrias atendidas em baixa tensão, o futuro cliente deve informar sua demanda de utilização. Caso não possua essa demanda, deve-se utilizar o procedimento de cálculo indicado no padrão.

---

## 21. Modelo lógico para uso em sistema

### 21.1 Entradas mínimas necessárias

Para enquadrar uma unidade consumidora conforme as Tabelas 001 e 002, o sistema deve solicitar, no mínimo:

| Entrada | Tipo de dado | Observação |
|---|---|---|
| Carga instalada total | kW | Deve ser calculada pela soma das potências nominais dos equipamentos |
| Demanda calculada | VA ou kVA | Após aplicação dos fatores de demanda aplicáveis |
| Corrente de demanda | A | Base para dimensionamento do padrão de entrada |
| Sistema de fornecimento | Estrela 220/127 V ou Delta 240/120 V | Deve refletir o sistema disponível na localidade |
| Modalidade pretendida | U, D ou T | Pode ser calculada ou solicitada ao usuário |
| Presença de carga trifásica | Sim/Não | Necessária para justificar categoria T, especialmente em sistema delta |
| Maior motor FN | cv | Comparar com limites da tabela |
| Maior motor FF | cv | Comparar com limites da tabela |
| Maior motor FFF | cv | Aplicável à tabela T |
| Existência de solda | Sim/Não | Verificar limites de kVA e tensão |
| Existência de aparelho de raio X | Sim/Não | Verificar potência e tensão |
| Existência de MMGD | Sim/Não | Verificar maior corrente entre geração e carga |
| Corrente da geração distribuída | A | Aplicável quando houver MMGD |
| Tipo de isolação pretendida | PVC ou EPR/XLPE | Define seção do condutor de entrada e aterramento |

---

## 22. Regra de seleção da categoria por corrente de demanda

### 22.1 Modalidade U/D — Tabela 001

| Modalidade | Corrente de referência / proteção | Categoria sugerida |
|---|---:|---|
| U | Até 70 A, quando aplicável a sistema monofásico | U2 |
| D | Até 63 A | D2 |
| D | Acima de 63 A até 100 A | D4 |
| D | Acima de 100 A até 150 A | D6 |
| D | Acima de 150 A até 200 A | D7 |
| D | Acima de 200 A até 300 A | D9 |
| D | Acima de 300 A até 350 A | D10 |

> **Atenção:** esta tabela é uma interpretação lógica para automação do enquadramento, baseada nas correntes/proteções das categorias. A validação final deve respeitar o padrão EDP, o tipo de rede, a carga instalada, a demanda calculada, as limitações de equipamentos e eventual análise da concessionária.

### 22.2 Modalidade T — Tabela 002

| Modalidade | Corrente de referência / proteção | Categoria sugerida |
|---|---:|---|
| T | Até 63 A | T2 |
| T | Acima de 63 A até 100 A | T4 |
| T | Acima de 100 A até 150 A | T6 |
| T | Acima de 150 A até 200 A | T7 |
| T | Acima de 200 A até 300 A | T9 |
| T | Acima de 300 A até 350 A | T10 |

---

## 23. Algoritmo recomendado para enquadramento automático

### 23.1 Etapa 1 — calcular carga instalada

Somar todas as potências nominais dos equipamentos da unidade consumidora.

```text
Carga Instalada [kW] = Σ Potências nominais dos equipamentos [kW]
```

### 23.2 Etapa 2 — calcular demanda

Aplicar os fatores de demanda correspondentes a cada grupo de carga, conforme as tabelas específicas do padrão EDP e demais normas aplicáveis.

```text
Demanda Total [VA ou kVA] = Σ Demandas parciais após aplicação dos fatores de demanda
```

### 23.3 Etapa 3 — calcular corrente de demanda

A corrente de demanda deve ser calculada conforme o sistema de fornecimento e a tensão aplicável.

Exemplos conceituais:

```text
Sistema monofásico ou bifásico:
I = D / V

Sistema trifásico equilibrado:
I = D / (√3 × Vff)
```

O sistema deve controlar corretamente se a tensão utilizada no cálculo é fase-neutro ou fase-fase, conforme o tipo de ligação e a formulação adotada no padrão técnico.

### 23.4 Etapa 4 — selecionar modalidade U, D ou T

A modalidade deve ser selecionada conforme:

- carga instalada;
- demanda;
- tipo de rede;
- existência de equipamentos trifásicos;
- limites por categoria;
- solicitação do cliente, quando admitida;
- análise de viabilidade da concessionária, quando necessária.

### 23.5 Etapa 5 — selecionar categoria

A categoria deve ser selecionada comparando a corrente de demanda com os degraus padronizados:

- U2;
- D2, D4, D6, D7, D9, D10;
- T2, T4, T6, T7, T9, T10.

### 23.6 Etapa 6 — validar motores

O sistema deve validar os limites de motores:

- maior motor FN;
- maior motor FF;
- maior motor FFF, quando trifásico.

Caso os limites sejam excedidos, o sistema deve exigir estudo técnico detalhado ou marcar o enquadramento como dependente de análise da EDP.

### 23.7 Etapa 7 — validar cargas especiais

O sistema deve verificar:

- máquina de solda a transformador;
- máquina de solda trifásica com retificação em ponte;
- aparelhos de raio X;
- outras cargas que possam causar perturbações na rede.

### 23.8 Etapa 8 — validar MMGD

Se houver microgeração distribuída, o sistema deve calcular a corrente associada à geração e compará-la com a corrente da carga instalada.

```text
Corrente de dimensionamento da proteção = maior valor entre:
- corrente da geração distribuída;
- corrente da carga instalada/demanda aplicável.
```

A categoria deve ser definida pela proteção correspondente ao maior valor.

### 23.9 Etapa 9 — gerar especificações do padrão de entrada

Após definida a categoria, o sistema deve retornar automaticamente:

- categoria final;
- modalidade de atendimento;
- tipo de medição;
- disjuntor de entrada;
- fusível NH e chave, se aplicável;
- condutor de entrada em PVC;
- condutor de entrada em EPR/XLPE;
- caixa de medição/proteção;
- eletroduto de entrada;
- tipo/capacidade do poste;
- possibilidade de poste com caixa incorporada;
- condutor de aterramento;
- eletroduto de aterramento;
- limites de motor;
- necessidade de ART/TRT/RRT, quando aplicável;
- alertas normativos.

---

## 24. Estrutura de dados sugerida para implementação

### 24.1 Tabela `edp_categoria_atendimento`

| Campo | Tipo sugerido | Exemplo |
|---|---|---|
| id | string | D4 |
| modalidade | enum | U, D, T |
| sistema | enum | FN, FFN, FFFN |
| fases | integer | 2 |
| neutro | boolean | true |
| disjuntor_a | integer | 100 |
| fusivel_nh_a | integer/null | null |
| chave_a | integer/null | null |
| medicao | enum | direta, indireta |
| condutor_pvc_mm2 | number/string | 35 |
| condutor_epr_xlpe_mm2 | number/string | 25 |
| caixa | string | II, III, E ou Modular |
| eletroduto_entrada_mm | integer | 40 |
| poste | string | Concreto ou aço galvanizado — 200 daN |
| pci | string/null | null |
| aterramento_pvc_mm2 | number | 16 |
| aterramento_epr_xlpe_mm2 | number | 16 |
| aterramento_eletroduto_mm | integer | 20 |
| maior_motor_fn_cv | number | 1 |
| maior_motor_ff_cv | number/null | 3 |
| maior_motor_fff_cv | number/null | null |

---

## 25. Base estruturada resumida — Tabela 001 em formato de dados

```json
[
  {
    "categoria": "U2",
    "modalidade": "U",
    "sistema": "FN",
    "disjuntor_a": 70,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "responsabilidade_distribuidora",
    "condutor_entrada_epr_xlpe": "responsabilidade_distribuidora",
    "caixa": "II, III, E ou Modular",
    "eletroduto_entrada": "PVC 32 mm",
    "poste": "Concreto ou aço galvanizado — 90 daN",
    "pci": "PCI-1",
    "aterramento_pvc": "16 mm²",
    "aterramento_epr_xlpe": "16 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": null
  },
  {
    "categoria": "D2",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 63,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "responsabilidade_distribuidora",
    "condutor_entrada_epr_xlpe": "responsabilidade_distribuidora",
    "caixa": "II, III, E ou Modular",
    "eletroduto_entrada": "PVC 32 mm",
    "poste": "Concreto ou aço galvanizado — 90 daN",
    "pci": "PCI-1",
    "aterramento_pvc": "16 mm²",
    "aterramento_epr_xlpe": "16 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "3 cv"
  },
  {
    "categoria": "D4",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 100,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "35 mm²",
    "condutor_entrada_epr_xlpe": "25 mm²",
    "caixa": "II, III, E ou Modular",
    "eletroduto_entrada": "PVC 40 mm",
    "poste": "Concreto ou aço galvanizado — 200 daN",
    "pci": null,
    "aterramento_pvc": "16 mm²",
    "aterramento_epr_xlpe": "16 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "3 cv"
  },
  {
    "categoria": "D6",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 150,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "70 mm²",
    "condutor_entrada_epr_xlpe": "50 mm²",
    "caixa": "380 e Modular; ou 570 e Modular; ou conjunto de 3 caixas 520 × 260 mm",
    "eletroduto_entrada": "PVC 60 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "35 mm²",
    "aterramento_epr_xlpe": "25 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "3 cv"
  },
  {
    "categoria": "D7",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 200,
    "fusivel_nh_a": 160,
    "chave_a": 250,
    "medicao": "indireta",
    "condutor_entrada_pvc": "95 mm²",
    "condutor_entrada_epr_xlpe": "70 mm²",
    "caixa": "H ou M + T; ou Modular",
    "eletroduto_entrada": "PVC 75 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "50 mm²",
    "aterramento_epr_xlpe": "35 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv"
  },
  {
    "categoria": "D9",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 300,
    "fusivel_nh_a": 250,
    "chave_a": 400,
    "medicao": "indireta",
    "condutor_entrada_pvc": "185 mm²",
    "condutor_entrada_epr_xlpe": "120 mm²",
    "caixa": "M + T; ou Modular",
    "eletroduto_entrada": "PVC 85 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "95 mm²",
    "aterramento_epr_xlpe": "70 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv"
  },
  {
    "categoria": "D10",
    "modalidade": "D",
    "sistema": "FFN",
    "disjuntor_a": 350,
    "fusivel_nh_a": 315,
    "chave_a": 400,
    "medicao": "indireta",
    "condutor_entrada_pvc": "240 mm²",
    "condutor_entrada_epr_xlpe": "185 mm²",
    "caixa": "M + T; ou Modular",
    "eletroduto_entrada": "PVC 85 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "120 mm²",
    "aterramento_epr_xlpe": "95 mm²",
    "aterramento_eletroduto": "PVC 25 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv"
  }
]
```

---

## 26. Base estruturada resumida — Tabela 002 em formato de dados

```json
[
  {
    "categoria": "T2",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 63,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "responsabilidade_distribuidora",
    "condutor_entrada_epr_xlpe": "responsabilidade_distribuidora",
    "caixa": "II, III, E ou Modular",
    "eletroduto_entrada": "PVC 32 mm",
    "poste": "Concreto ou aço galvanizado — 90 daN",
    "pci": "PCI-1",
    "aterramento_pvc": "16 mm²",
    "aterramento_epr_xlpe": "16 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "3 cv",
    "maior_motor_fff": "8 cv"
  },
  {
    "categoria": "T4",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 100,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "35 mm²",
    "condutor_entrada_epr_xlpe": "25 mm²",
    "caixa": "III ou Modular",
    "eletroduto_entrada": "PVC 40 mm",
    "poste": "Concreto ou aço galvanizado — 200 daN",
    "pci": null,
    "aterramento_pvc": "16 mm²",
    "aterramento_epr_xlpe": "16 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "3 cv",
    "maior_motor_fff": "15 cv"
  },
  {
    "categoria": "T6",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 150,
    "fusivel_nh_a": null,
    "chave_a": null,
    "medicao": "direta",
    "condutor_entrada_pvc": "70 mm²",
    "condutor_entrada_epr_xlpe": "50 mm²",
    "caixa": "380 e Modular; ou 570 e Modular; ou conjunto de 3 caixas 520 × 260 mm",
    "eletroduto_entrada": "PVC 60 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "35 mm²",
    "aterramento_epr_xlpe": "25 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv",
    "maior_motor_fff": "25 cv"
  },
  {
    "categoria": "T7",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 200,
    "fusivel_nh_a": 160,
    "chave_a": 250,
    "medicao": "indireta",
    "condutor_entrada_pvc": "95 mm²",
    "condutor_entrada_epr_xlpe": "70 mm²",
    "caixa": "H ou M + T; ou Modular",
    "eletroduto_entrada": "PVC 75 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "50 mm²",
    "aterramento_epr_xlpe": "35 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv",
    "maior_motor_fff": "30 cv"
  },
  {
    "categoria": "T9",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 300,
    "fusivel_nh_a": 250,
    "chave_a": 400,
    "medicao": "indireta",
    "condutor_entrada_pvc": "185 mm²",
    "condutor_entrada_epr_xlpe": "120 mm²",
    "caixa": "M + T; ou Modular",
    "eletroduto_entrada": "PVC 85 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "95 mm²",
    "aterramento_epr_xlpe": "70 mm²",
    "aterramento_eletroduto": "PVC 20 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv",
    "maior_motor_fff": "60 cv"
  },
  {
    "categoria": "T10",
    "modalidade": "T",
    "sistema": "FFFN",
    "disjuntor_a": 350,
    "fusivel_nh_a": 315,
    "chave_a": 400,
    "medicao": "indireta",
    "condutor_entrada_pvc": "240 mm²",
    "condutor_entrada_epr_xlpe": "185 mm²",
    "caixa": "M + T; ou Modular",
    "eletroduto_entrada": "PVC 85 mm",
    "poste": "Concreto — 300 daN",
    "pci": null,
    "aterramento_pvc": "120 mm²",
    "aterramento_epr_xlpe": "95 mm²",
    "aterramento_eletroduto": "PVC 25 mm",
    "maior_motor_fn": "1 cv",
    "maior_motor_ff": "5 cv",
    "maior_motor_fff": "60 cv"
  }
]
```

---

## 27. Alertas obrigatórios para validação de software

Um sistema de projetos elétricos que utilize as Tabelas 001 e 002 deve implementar, no mínimo, os seguintes alertas:

| Código | Alerta | Condição de disparo |
|---|---|---|
| EDP-001 | Carga instalada acima do limite de baixa tensão | Carga instalada > 75 kW |
| EDP-002 | Categoria incompatível com modalidade | Exemplo: selecionar T sem existência de equipamento trifásico quando exigido |
| EDP-003 | Medição indireta exige responsabilidade técnica | Corrente de demanda > 150 A |
| EDP-004 | Motor FN acima do limite | Motor FN > 1 cv |
| EDP-005 | Motor FF acima do limite | Motor FF acima do limite da categoria |
| EDP-006 | Motor FFF acima do limite | Motor FFF acima do limite da categoria |
| EDP-007 | Carga especial exige estudo técnico | Solda, raio X ou equipamento acima dos limites previstos |
| EDP-008 | MMGD exige comparação entre geração e carga | Existência de microgeração distribuída |
| EDP-009 | Categoria D6/T6 exige cabo auxiliar no interior da caixa | Categoria = D6 ou T6 |
| EDP-010 | Categorias D9/D10/T10 exigem dois conjuntos de isoladores | Categoria em D9, D10 ou T10 |
| EDP-011 | Caixa deve ser homologada/cadastrada | Sempre que for selecionado tipo de caixa |
| EDP-012 | Padrão de entrada deve estar voltado para a calçada | Ligações novas ou reformas |

---

## 28. Recomendações de implementação no sistema construtor de projetos elétricos

1. **Separar cálculo interno NBR 5410 do padrão da concessionária.**  
   A NBR 5410 deve orientar os circuitos internos, proteção, condutores, DR, DPS, queda de tensão e critérios de segurança. O padrão EDP deve orientar o padrão de entrada, categoria de atendimento, medição e interface com a distribuidora.

2. **Criar camada de regras da concessionária.**  
   As Tabelas 001 e 002 devem ser implementadas como uma base normativa versionada, com campo de versão do documento e data de vigência.

3. **Não calcular categoria somente por carga instalada.**  
   O enquadramento deve considerar carga instalada, demanda, corrente de demanda, sistema de fornecimento, tipo de rede, motores, cargas especiais e MMGD.

4. **Manter histórico de versões.**  
   Como os padrões da distribuidora podem ser alterados, o sistema deve armazenar a versão do padrão usada no projeto.

5. **Gerar relatório de justificativa.**  
   Para cada categoria selecionada, o sistema deve gerar justificativa técnica contendo: corrente calculada, modalidade, categoria, proteção, medição, condutores, eletroduto, caixa, poste e aterramento.

6. **Emitir aviso de validação pela concessionária.**  
   Para casos de medição indireta, cargas especiais, motores acima dos limites e MMGD, o sistema deve sinalizar a necessidade de análise/documentação específica.

---

## 29. Resumo executivo para uso direto

As **Tabelas 001 e 002 do padrão EDP** são matrizes normativas de enquadramento do padrão de entrada de unidades consumidoras individuais em baixa tensão.

A **Tabela 001** atende categorias:

- U2;
- D2;
- D4;
- D6;
- D7;
- D9;
- D10.

A **Tabela 002** atende categorias:

- T2;
- T4;
- T6;
- T7;
- T9;
- T10.

O principal critério operacional para o sistema é a **corrente de demanda**, associada à modalidade de atendimento e validada contra os limites de carga instalada, motores, cargas especiais e geração distribuída.

A medição é:

- **direta** até 150 A;
- **indireta** acima de 150 A.

A proteção da entrada principal, em especial quando houver MMGD, deve considerar a maior corrente entre geração distribuída e carga instalada, conforme observação da EDP e normas ABNT NBR 16690:2019 e ABNT NBR 5410.

---

## 30. Conclusão técnica

A consolidação das Tabelas 001 e 002 permite estruturar uma camada normativa robusta para o sistema de elaboração de projetos elétricos. Essas tabelas não devem ser tratadas apenas como tabelas de disjuntores, mas como uma matriz integrada de enquadramento técnico, pois cada categoria define simultaneamente proteção, medição, condutores, eletrodutos, caixa, poste, aterramento e limites de motores.

Para uso real, recomenda-se que o sistema implemente validação automática, rastreabilidade da versão normativa, justificativa técnica e alertas de dependência de análise da concessionária.
