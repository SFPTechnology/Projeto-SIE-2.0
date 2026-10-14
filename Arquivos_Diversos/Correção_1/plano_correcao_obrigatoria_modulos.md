# Plano de Correção Obrigatória dos Módulos Antes da Liberação para Uso Real

## 1. Diretriz principal do plano

O sistema deve ser corrigido em uma sequência lógica de engenharia: primeiro corrigir dados e validações, depois regras normativas, depois cálculos, depois proteções, depois artefatos finais e auditoria.

A ordem correta não é começar pelo relatório final, diagrama unifilar ou balanceamento de fases. Esses elementos dependem de dados técnicos confiáveis. O ponto mais crítico identificado no relatório anterior foi que o sistema já calcula resultados mesmo havendo dados incompletos, como carga sem `tipo_aparelho`, e inconsistência entre **categoria T**, **subcategoria U2**, **disjuntor 150 A** e **condutor 25 mm²**.

A base normativa de referência deve ser a **ABNT NBR 5410**, aplicável a instalações elétricas de baixa tensão, e o **Padrão Técnico EDP São Paulo PT.DT.PDN.03.14.020 versão 06**, quando o projeto estiver dentro da área de concessão da EDP São Paulo.

---

## 2. Sequência estrutural recomendada

### Visão geral da ordem de implementação

| Ordem | Módulo/Etapa | Objetivo | Dependência | Resultado esperado |
|---:|---|---|---|---|
| 1 | Base normativa e versionamento de regras | Travar quais normas, tabelas e versões serão usadas | Nenhuma | Biblioteca técnica oficial do sistema |
| 2 | Modelo de dados técnico | Corrigir estrutura de ambientes, cargas, circuitos e padrões | Etapa 1 | Dados completos e rastreáveis |
| 3 | Validação impeditiva de entradas | Bloquear cálculo com dados incompletos/incoerentes | Etapa 2 | Sistema “fail-closed” |
| 4 | Previsão de cargas | Corrigir iluminação, TUG, TUE e cargas fixas | Etapas 1–3 | Carga instalada confiável |
| 5 | Enquadramento EDP | Corrigir grupos, demanda, categoria e subcategoria | Etapa 4 | Padrão de entrada coerente |
| 6 | Divisão final de circuitos | Criar circuitos terminais tecnicamente válidos | Etapa 4 | Quadro de circuitos confiável |
| 7 | Corrente IB e balanceamento | Calcular correntes e distribuir fases | Etapa 6 | Balanceamento preliminar/final |
| 8 | Dimensionamento de condutores | Definir seção por capacidade de condução e critérios técnicos | Etapas 6–7 | Condutores dimensionados |
| 9 | Queda de tensão | Validar comprimento, seção e corrente | Etapa 8 | Circuitos aprovados/reprovados |
| 10 | Sobrecorrente e curto-circuito | Coordenar IB/In/Iz e dispositivos | Etapas 8–9 | Proteção validada |
| 11 | DR, DPS, aterramento e equipotencialização | Corrigir segurança contra choque e surtos | Etapas 6–10 | Segurança elétrica mínima |
| 12 | Artefatos finais | Quadro de cargas, diagrama unifilar, memorial e relatório | Etapas 1–11 | Projeto auditável |
| 13 | Auditoria, testes e homologação | Validar o sistema antes do uso real | Todas | Liberação condicionada |

---

## 3. Fase 1 — Base normativa, tabelas técnicas e versionamento

### Objetivo

Criar uma camada centralizada de regras técnicas, normas, tabelas e parâmetros. Nenhum cálculo deve ficar solto em tela, componente ou fórmula isolada.

### Problemas corrigidos

- Fórmulas não rastreáveis;
- parâmetros EDP parcialmente exibidos;
- risco de regra técnica duplicada ou divergente;
- ausência de controle de versão normativa;
- dificuldade de auditoria.

### Implementação passo a passo

| Passo | Ação obrigatória | Resultado esperado |
|---:|---|---|
| 1.1 | Criar tabela/biblioteca de normas aplicáveis | NBR 5410, padrão EDP, versão, data, escopo |
| 1.2 | Criar tabela de regras de iluminação | Critério por ambiente, área e potência mínima |
| 1.3 | Criar tabela de regras de TUG | Critério por tipo de dependência |
| 1.4 | Criar tabela de tipos de TUE/carga fixa | Equipamento, grupo, tensão, fase, FP padrão |
| 1.5 | Criar tabela de grupos EDP | Grupos a, b, c, d, e, f, g, h, i |
| 1.6 | Criar tabela de categoria/subcategoria EDP | U, D, T e suas faixas corretas |
| 1.7 | Criar tabela de disjuntor/condutor/eletroduto de entrada | Amarrada à categoria/subcategoria correta |
| 1.8 | Criar tabela de métodos de instalação | Método, condutores carregados, isolação, temperatura |
| 1.9 | Criar tabela de condutores | Material, seção, isolação, capacidade base |
| 1.10 | Criar tabela de fatores de correção | Temperatura, agrupamento, método |
| 1.11 | Criar tabela de dispositivos de proteção | Disjuntor, curva, capacidade de interrupção, DR, DPS |
| 1.12 | Criar tabela de critérios de queda de tensão | Limites e fórmulas |
| 1.13 | Versionar cada regra | Ex.: `NBR5410_2004_CORR2008`, `EDP_PTDTPDN0314020_v06` |

### Critério de aceite

O sistema deve permitir abrir qualquer resultado e mostrar:

- regra aplicada;
- versão da regra;
- origem normativa;
- fórmula;
- dados de entrada;
- resultado intermediário;
- arredondamento;
- resultado final.

### Bloqueio obrigatório

Nenhum cálculo normativo deve ser executado se a regra técnica correspondente não estiver cadastrada, ativa e versionada.

---

## 4. Fase 2 — Correção do modelo de dados técnico

### Objetivo

Corrigir a base estrutural do sistema para que todo ambiente, carga, circuito e proteção tenha dados suficientes para cálculo técnico.

### 4.1 Entidade “Projeto”

| Campo | Obrigatório | Observação |
|---|---|---|
| Nome do projeto | Sim | Identificação |
| Concessionária | Sim | Ex.: EDP São Paulo |
| Tensão de fornecimento | Sim | Ex.: 127/220 V |
| Sistema | Sim | Monofásico, bifásico ou trifásico |
| Esquema de aterramento | Sim | TN-S, TN-C-S, TT etc. |
| Tipo de instalação | Sim | Residencial, comercial, mista, industrial leve |
| Norma-base | Sim | NBR 5410 |
| Padrão concessionária | Sim, quando aplicável | EDP, Enel, CPFL etc. |
| Responsável técnico | Sim para emissão final | Nome, CREA, ART |

### 4.2 Entidade “Dependência”

| Campo | Obrigatório | Observação |
|---|---|---|
| Nome da dependência | Sim | Ex.: cozinha, banheiro |
| Tipo normativo | Sim | Não apenas nome livre |
| Largura | Sim | m |
| Comprimento | Sim | m |
| Área | Calculado | m² |
| Perímetro | Calculado | m |
| Ambiente molhado/molhável | Sim | Impacta DR |
| Ambiente externo | Sim | Impacta DR/IP |
| Contém chuveiro/banheira/hidromassagem | Sim | Impacta DR/equipotencialização |
| Contém motores | Sim | Impacta proteção |
| Pavimento/localização | Recomendado | Ajuda diagrama e circuitos |

### 4.3 Entidade “Carga”

| Campo | Obrigatório | Observação |
|---|---|---|
| Descrição da carga | Sim | Ex.: chuveiro, micro-ondas |
| Tipo de carga | Sim | Iluminação, TUG, TUE, carga fixa, motor |
| Tipo de aparelho | Sim | Campo que falhou na gravação |
| Grupo EDP | Sim, quando usar EDP | a, b, c, d, e, f, g, h, i |
| Potência | Sim | W ou VA |
| Unidade da potência | Sim | W, VA, kW, CV etc. |
| Fator de potência | Sim se W/kW | Para conversão em VA |
| Quantidade | Sim | Número de unidades |
| Tensão | Sim | 127 ou 220 V |
| Fases | Sim | 1F, 2F ou 3F |
| Corrente nominal | Calculada | A |
| Circuito exclusivo? | Sim/Não | Regra técnica |
| Ambiente vinculado | Sim | Rastreabilidade |
| Origem do dado | Sim | Manual, tabela, fabricante, norma |

### 4.4 Entidade “Circuito”

| Campo | Obrigatório | Observação |
|---|---|---|
| Código do circuito | Sim | C01, C02, C03 |
| Tipo do circuito | Sim | Iluminação, TUG, TUE, motor |
| Cargas vinculadas | Sim | Lista de cargas |
| Tensão | Sim | V |
| Fases | Sim | A, B, C, AB, BC, CA, ABC |
| Potência total | Calculada | VA |
| IB | Calculada | A |
| Método de instalação | Sim | Necessário para condutores |
| Comprimento | Sim | Necessário para queda |
| Condutores carregados | Sim | Necessário para Iz |
| Temperatura ambiente | Sim | Fator de correção |
| Agrupamento | Sim | Fator de correção |
| Condutor fase | Calculado/selecionado | mm² |
| Condutor neutro | Calculado/selecionado | mm² |
| Condutor PE | Calculado/selecionado | mm² |
| Disjuntor | Calculado/selecionado | A |
| DR | Aplicável? | Sim/Não |
| DPS | Aplicável? | Sim/Não no quadro |
| Queda de tensão | Calculada | % |
| Status técnico | Calculado | Conforme/não conforme |

### Critério de aceite

O sistema não deve permitir que uma carga entre no cálculo final se faltar:

- tipo de carga;
- tipo de aparelho;
- potência;
- tensão;
- fases;
- grupo EDP, se a concessionária for EDP;
- ambiente;
- indicação se exige circuito exclusivo.

---

## 5. Fase 3 — Validação impeditiva de entradas e qualidade de dados

### Objetivo

Transformar o sistema em um sistema de validação segura. Ele deve impedir cálculo final com dados incompletos, incoerentes ou incompatíveis.

### Regras de validação obrigatórias

| ID | Regra impeditiva | Severidade |
|---|---|---|
| V01 | Carga sem `tipo_aparelho` não pode entrar em demanda | Crítica |
| V02 | Carga sem tensão não pode gerar IB | Crítica |
| V03 | Carga sem fase não pode gerar circuito | Crítica |
| V04 | Projeto trifásico não pode usar subcategoria U/D | Crítica |
| V05 | Projeto monofásico não pode usar categoria T | Crítica |
| V06 | Disjuntor de entrada deve pertencer à categoria/subcategoria escolhida | Crítica |
| V07 | Condutor de entrada deve pertencer à mesma linha da tabela do disjuntor | Crítica |
| V08 | Circuito sem método de instalação não pode dimensionar condutor | Crítica |
| V09 | Circuito sem comprimento não pode validar queda de tensão | Alta |
| V10 | Circuito molhado/externo sem análise de DR não pode ser aprovado | Crítica |
| V11 | Circuito sem proteção contra sobrecorrente não pode ser aprovado | Crítica |
| V12 | Projeto sem esquema de aterramento não pode ser finalizado | Crítica |
| V13 | Projeto sem relatório de pendências não pode ser concluído | Alta |
| V14 | Cálculo sem fórmula/regra versionada deve aparecer como “não rastreável” | Alta |
| V15 | Alteração de carga após validação deve invalidar os cálculos dependentes | Alta |

### Estados técnicos recomendados

| Estado | Significado |
|---|---|
| Rascunho | Dados ainda incompletos |
| Calculado preliminar | Cargas básicas calculadas |
| Inconsistente | Há erro impeditivo |
| Dimensionado | Condutores/proteções calculados |
| Validado pelo sistema | Sem erro automático |
| Revisado pelo responsável técnico | Conferido manualmente |
| Liberado para relatório | Apto a emitir artefatos |
| Projeto final bloqueado | Há pendência crítica |

### Critério de aceite

O botão **“Concluir projeto”** deve permanecer bloqueado enquanto houver qualquer pendência crítica.

---

## 6. Fase 4 — Correção do módulo de previsão de cargas

Este módulo deve ser corrigido antes da demanda EDP e antes dos circuitos, porque todos os cálculos posteriores dependem da carga instalada correta.

### 6.1 Iluminação mínima por ambiente

#### Objetivo

Garantir que o sistema calcule corretamente a potência mínima de iluminação por dependência e deixe a memória de cálculo auditável.

#### Implementação

| Passo | Ação |
|---:|---|
| 6.1.1 | Associar cada dependência a um tipo normativo |
| 6.1.2 | Calcular área automaticamente |
| 6.1.3 | Aplicar regra de iluminação mínima |
| 6.1.4 | Exibir memória: área, regra, potência base, incrementos, resultado |
| 6.1.5 | Permitir iluminação adicional separada da iluminação mínima |
| 6.1.6 | Impedir que iluminação decorativa substitua iluminação mínima |
| 6.1.7 | Registrar se a potência é normativa, real instalada ou adicional |

#### Saída esperada

| Saída | Exemplo |
|---|---|
| Área | 36 m² |
| Regra aplicada | Iluminação mínima por área |
| Potência mínima | 520 VA |
| Iluminação adicional | 60 VA |
| Total para carga instalada | Conforme regra do sistema |
| Status | Conforme |

### 6.2 TUG — quantidade e potência

#### Objetivo

Calcular pontos mínimos de tomadas e potência mínima atribuída de acordo com o tipo de ambiente.

#### Implementação

| Passo | Ação |
|---:|---|
| 6.2.1 | Classificar ambiente: sala, dormitório, cozinha, banheiro, varanda, área externa etc. |
| 6.2.2 | Definir critério: por perímetro, por ambiente ou por condição especial |
| 6.2.3 | Calcular quantidade mínima de pontos |
| 6.2.4 | Calcular potência mínima atribuída |
| 6.2.5 | Separar TUG de TUE |
| 6.2.6 | Exibir memória por dependência |
| 6.2.7 | Permitir pontos adicionais pelo usuário |
| 6.2.8 | Indicar quando ambiente exige DR ou circuito específico |

#### Saída esperada

| Saída | Exemplo |
|---|---|
| Perímetro | 24 m |
| Critério | Cozinha — pontos por perímetro |
| Pontos calculados | 7 |
| Potência atribuída | 2.200 VA |
| Status | Conforme |

### 6.3 TUE e cargas fixas

#### Objetivo

Garantir que toda carga específica ou fixa seja classificada corretamente, com tensão, potência, fases e grupo de demanda.

#### Implementação

| Passo | Ação |
|---:|---|
| 6.3.1 | Criar catálogo de aparelhos |
| 6.3.2 | Associar aparelho a tipo: TUE, carga fixa, motor, iluminação adicional |
| 6.3.3 | Associar aparelho a grupo EDP |
| 6.3.4 | Exigir potência e unidade |
| 6.3.5 | Exigir tensão e fases |
| 6.3.6 | Converter W/kW/CV para VA quando necessário |
| 6.3.7 | Definir se exige circuito exclusivo |
| 6.3.8 | Bloquear carga incompleta |
| 6.3.9 | Exibir memória de conversão e classificação |

#### Correção específica obrigatória

A falha **“carga adicional sem tipo_aparelho”** deve ser tratada como erro impeditivo.

| Antes | Depois |
|---|---|
| Sistema calcula mesmo com carga sem tipo | Sistema bloqueia demanda, IB e relatório |
| Erro aparece apenas como diagnóstico | Erro impede avanço |
| Campo pode ficar vazio | Campo obrigatório |

---

## 7. Fase 5 — Correção do módulo EDP: demanda, categoria e entrada

Este é um dos pontos mais críticos do sistema, porque houve inconsistência entre categoria, subcategoria, disjuntor e condutor.

### 7.1 Demanda por grupo EDP

#### Objetivo

Calcular a demanda por grupos da EDP com rastreabilidade total.

#### Implementação

| Passo | Ação |
|---:|---|
| 7.1.1 | Agrupar cargas automaticamente por tipo EDP |
| 7.1.2 | Validar se toda carga tem grupo EDP |
| 7.1.3 | Calcular carga instalada por grupo |
| 7.1.4 | Aplicar fator de demanda correspondente |
| 7.1.5 | Calcular demanda por grupo |
| 7.1.6 | Separar D1 e D3 conforme regra EDP |
| 7.1.7 | Calcular DT |
| 7.1.8 | Exibir memória completa |
| 7.1.9 | Permitir auditoria manual do enquadramento |

#### Saída esperada

| Campo | Obrigatório |
|---|---|
| Grupo EDP | Sim |
| Cargas incluídas | Sim |
| Potência por carga | Sim |
| Quantidade | Sim |
| Fator aplicado | Sim |
| Demanda parcial | Sim |
| Fonte da regra | Sim |
| Versão da tabela | Sim |

### 7.2 Categoria/subcategoria de entrada

#### Objetivo

Corrigir a falha crítica de associar **categoria T** com **subcategoria U2**.

#### Implementação

| Passo | Ação |
|---:|---|
| 7.2.1 | Identificar sistema de fornecimento: mono, bi ou trifásico |
| 7.2.2 | Identificar carga instalada total |
| 7.2.3 | Identificar demanda total |
| 7.2.4 | Selecionar família de categoria correta |
| 7.2.5 | Se mono: permitir apenas U |
| 7.2.6 | Se bifásico: permitir apenas D |
| 7.2.7 | Se trifásico: permitir apenas T |
| 7.2.8 | Selecionar subcategoria dentro da família correta |
| 7.2.9 | Bloquear combinações cruzadas |
| 7.2.10 | Exibir justificativa da escolha |

#### Regra impeditiva

| Condição | Resultado |
|---|---|
| Sistema trifásico + subcategoria U | Bloquear |
| Sistema trifásico + subcategoria D | Bloquear |
| Sistema monofásico + categoria T | Bloquear |
| Sistema bifásico + categoria T | Bloquear |
| Categoria/subcategoria sem linha válida na tabela | Bloquear |

### 7.3 Disjuntor e condutor de entrada

#### Objetivo

Amarrar disjuntor, condutor e eletroduto à mesma linha da tabela EDP correta.

#### Implementação

| Passo | Ação |
|---:|---|
| 7.3.1 | Selecionar linha da tabela EDP pela categoria/subcategoria |
| 7.3.2 | Buscar disjuntor da linha selecionada |
| 7.3.3 | Buscar condutor fase da mesma linha |
| 7.3.4 | Buscar neutro, proteção e eletroduto, se constarem na tabela |
| 7.3.5 | Impedir alteração manual incoerente |
| 7.3.6 | Caso permita alteração manual, marcar como “fora da tabela — exige justificativa” |
| 7.3.7 | Exibir memória de seleção |
| 7.3.8 | Validar compatibilidade com corrente de demanda |
| 7.3.9 | Exibir alerta se corrente calculada estiver muito abaixo da categoria selecionada |

#### Correção específica obrigatória

A combinação observada **disjuntor 150 A + condutor 25 mm²** não deve ser aceita sem validação explícita de tabela, material, isolação e categoria.

---

## 8. Fase 6 — Implementação da divisão final de circuitos

### Objetivo

Transformar a lista provisória de cargas em circuitos terminais tecnicamente válidos.

### Implementação passo a passo

| Passo | Ação |
|---:|---|
| 8.1 | Criar motor de geração de circuitos |
| 8.2 | Separar iluminação por dependência/grupo lógico |
| 8.3 | Separar TUG gerais |
| 8.4 | Criar circuitos específicos para cozinha, copa, área de serviço e ambientes análogos |
| 8.5 | Criar circuito exclusivo para TUE com corrente superior a limite normativo |
| 8.6 | Criar circuitos dedicados para chuveiro, aquecedor, ar-condicionado, hidromassagem, motor/bomba |
| 8.7 | Separar circuitos de áreas externas |
| 8.8 | Marcar circuitos que exigem DR |
| 8.9 | Definir tensão e fases de cada circuito |
| 8.10 | Calcular potência total por circuito |
| 8.11 | Calcular IB por circuito |
| 8.12 | Permitir edição manual pelo engenheiro |
| 8.13 | Registrar justificativa para alterações manuais |
| 8.14 | Bloquear circuitos com cargas incompatíveis |
| 8.15 | Gerar quadro preliminar de circuitos |

### Critérios de aceite

| Critério | Condição de aprovação |
|---|---|
| Todo ponto de utilização tem circuito | Sim |
| Toda carga está em exatamente um circuito | Sim |
| Todo TUE relevante possui circuito próprio | Sim |
| Circuitos de áreas molhadas identificados | Sim |
| Circuitos externos identificados | Sim |
| Circuitos com motores identificados | Sim |
| Nenhum circuito sem tensão/fase | Sim |
| Nenhum circuito sem IB | Sim |

---

## 9. Fase 7 — Corrente IB e balanceamento de fases

### Objetivo

Calcular a corrente de projeto por circuito e distribuir os circuitos entre fases de forma tecnicamente aceitável.

### Implementação

| Passo | Ação |
|---:|---|
| 9.1 | Calcular IB para circuito monofásico |
| 9.2 | Calcular IB para circuito bifásico |
| 9.3 | Calcular IB para circuito trifásico |
| 9.4 | Considerar fator de potência quando aplicável |
| 9.5 | Registrar fórmula usada |
| 9.6 | Identificar circuitos que não podem mudar de fase |
| 9.7 | Balancear cargas monofásicas |
| 9.8 | Balancear cargas bifásicas entre pares de fases |
| 9.9 | Manter cargas trifásicas nas três fases |
| 9.10 | Exibir antes/depois do balanceamento |
| 9.11 | Permitir ajuste manual |
| 9.12 | Recalcular sempre que carga/circuito mudar |

### Critério de aceite

O balanceamento deve mostrar:

- corrente por fase;
- potência por fase;
- desbalanceamento percentual;
- circuitos movimentados;
- circuitos fixos;
- justificativa do algoritmo;
- status: preliminar ou final.

### Observação técnica

O balanceamento deve ser implementado **após** a divisão final de circuitos. Balancear circuitos provisórios gera falsa precisão.

---

## 10. Fase 8 — Dimensionamento de condutores

### Objetivo

Dimensionar condutores de fase, neutro e proteção com base em corrente, método de instalação, temperatura, agrupamento, queda de tensão e seção mínima.

### Implementação passo a passo

| Passo | Ação |
|---:|---|
| 10.1 | Exigir método de instalação por circuito |
| 10.2 | Exigir tipo de condutor: cobre/alumínio |
| 10.3 | Exigir isolação: PVC, EPR, XLPE etc. |
| 10.4 | Exigir temperatura ambiente |
| 10.5 | Exigir número de circuitos agrupados |
| 10.6 | Exigir número de condutores carregados |
| 10.7 | Buscar capacidade de condução base |
| 10.8 | Aplicar fator de temperatura |
| 10.9 | Aplicar fator de agrupamento |
| 10.10 | Calcular Iz corrigida |
| 10.11 | Comparar IB com Iz |
| 10.12 | Aplicar seção mínima normativa |
| 10.13 | Dimensionar neutro |
| 10.14 | Dimensionar PE |
| 10.15 | Registrar memória de cálculo |
| 10.16 | Enviar resultado para queda de tensão |
| 10.17 | Enviar resultado para proteção contra sobrecorrente |

### Saída esperada por circuito

| Campo | Obrigatório |
|---|---|
| IB | Sim |
| Método de instalação | Sim |
| Material | Sim |
| Isolação | Sim |
| Temperatura | Sim |
| Agrupamento | Sim |
| Iz base | Sim |
| Fatores aplicados | Sim |
| Iz corrigida | Sim |
| Seção fase | Sim |
| Seção neutro | Sim |
| Seção PE | Sim |
| Status | Conforme/não conforme |

### Bloqueio obrigatório

Sem esses dados, o sistema pode mostrar apenas **“IB calculado”**, nunca **“condutor dimensionado”**.

---

## 11. Fase 9 — Queda de tensão

### Objetivo

Validar se os condutores selecionados atendem ao limite de queda de tensão.

### Implementação

| Passo | Ação |
|---:|---|
| 11.1 | Exigir comprimento de cada circuito |
| 11.2 | Definir tensão do circuito |
| 11.3 | Usar IB do circuito |
| 11.4 | Usar seção e material do condutor |
| 11.5 | Considerar fator de potência quando aplicável |
| 11.6 | Calcular queda em volts |
| 11.7 | Calcular queda percentual |
| 11.8 | Comparar com limite aplicável |
| 11.9 | Se reprovar, aumentar seção do condutor |
| 11.10 | Recalcular proteção se seção mudar |
| 11.11 | Exibir pior circuito |
| 11.12 | Exibir queda por trecho, se houver alimentadores |

### Critério de aceite

| Condição | Resultado |
|---|---|
| Circuito sem comprimento | Não validado |
| Queda acima do limite | Reprovado |
| Condutor aumentado por queda | Registrar motivo |
| Queda dentro do limite | Conforme |
| Alteração de seção | Recalcular proteção |

---

## 12. Fase 10 — Proteção contra sobrecorrente

### Objetivo

Selecionar e validar disjuntores por circuito, coordenando carga, condutor e proteção.

### Implementação

| Passo | Ação |
|---:|---|
| 12.1 | Calcular IB do circuito |
| 12.2 | Obter Iz corrigida do condutor |
| 12.3 | Selecionar In do disjuntor |
| 12.4 | Verificar relação IB ≤ In ≤ Iz |
| 12.5 | Definir curva do disjuntor |
| 12.6 | Definir número de polos |
| 12.7 | Definir capacidade de interrupção |
| 12.8 | Exigir corrente de curto-circuito presumida |
| 12.9 | Validar se Icu/Icn é compatível |
| 12.10 | Validar seletividade mínima, quando aplicável |
| 12.11 | Verificar proteção de motores |
| 12.12 | Registrar memória de proteção |
| 12.13 | Bloquear circuito sem disjuntor válido |

### Saída esperada

| Campo | Obrigatório |
|---|---|
| IB | Sim |
| Iz corrigida | Sim |
| In | Sim |
| Curva | Sim |
| Nº de polos | Sim |
| Capacidade de interrupção | Sim |
| Corrente de curto presumida | Sim |
| Relação IB/In/Iz | Sim |
| Status | Conforme/não conforme |

---

## 13. Fase 11 — DR, DPS, aterramento e equipotencialização

Esta fase deve ser tratada como módulo de segurança, não como módulo opcional.

### 13.1 Proteção diferencial residual — DR

#### Implementação

| Passo | Ação |
|---:|---|
| 13.1.1 | Identificar ambientes que exigem DR |
| 13.1.2 | Identificar circuitos de banheiro, cozinha, lavanderia, área externa e tomadas externas |
| 13.1.3 | Indicar corrente diferencial nominal |
| 13.1.4 | Definir tipo de DR |
| 13.1.5 | Agrupar circuitos por DR, quando permitido |
| 13.1.6 | Verificar compatibilidade com cargas eletrônicas |
| 13.1.7 | Exibir quais circuitos estão protegidos |
| 13.1.8 | Bloquear projeto com circuito obrigatório sem DR |

#### Saída esperada

| Circuito | Exige DR? | DR especificado | Status |
|---|---|---|---|
| Banheiro | Sim | 30 mA | Conforme/não conforme |
| Cozinha | Sim, conforme aplicação | 30 mA | Conforme/não conforme |
| Área externa | Sim | 30 mA | Conforme/não conforme |
| Hidromassagem | Sim | 30 mA | Conforme/não conforme |

### 13.2 DPS

#### Implementação

| Passo | Ação |
|---:|---|
| 13.2.1 | Verificar necessidade de DPS no quadro |
| 13.2.2 | Definir classe/tipo do DPS |
| 13.2.3 | Definir tensão de operação |
| 13.2.4 | Definir corrente nominal/máxima |
| 13.2.5 | Definir proteção de retaguarda |
| 13.2.6 | Integrar DPS ao sistema de aterramento |
| 13.2.7 | Exibir no diagrama unifilar |

### 13.3 Aterramento e equipotencialização

#### Implementação

| Passo | Ação |
|---:|---|
| 13.3.1 | Exigir esquema de aterramento do projeto |
| 13.3.2 | Definir barramento de neutro |
| 13.3.3 | Definir barramento de proteção |
| 13.3.4 | Definir separação N/PE |
| 13.3.5 | Dimensionar condutor PE |
| 13.3.6 | Definir condutor de aterramento |
| 13.3.7 | Definir equipotencialização principal |
| 13.3.8 | Definir equipotencialização suplementar quando aplicável |
| 13.3.9 | Associar massas e partes condutivas ao PE |
| 13.3.10 | Exigir ensaio/valor de resistência quando aplicável |
| 13.3.11 | Exibir aterramento no relatório |
| 13.3.12 | Bloquear projeto sem esquema de aterramento |

### Critério de aceite

Projeto sem aterramento, PE e equipotencialização deve ficar com status:

**“Projeto tecnicamente incompleto — não liberado para uso real.”**

---

## 14. Fase 12 — Quadro de cargas, diagrama unifilar, memorial e relatório final

### Objetivo

Gerar artefatos finais somente depois de todos os módulos críticos aprovados.

### 14.1 Quadro de cargas

Deve conter:

| Campo obrigatório | Observação |
|---|---|
| Circuito | C01, C02, C03 |
| Descrição | Iluminação, TUG, chuveiro etc. |
| Ambiente | Cozinha, banheiro etc. |
| Potência | VA |
| Tensão | V |
| Fases | A, B, C, AB, BC, CA, ABC |
| IB | A |
| Disjuntor | A, curva, polos |
| Condutor fase | mm² |
| Neutro | mm² |
| PE | mm² |
| Método de instalação | Código |
| Comprimento | m |
| Queda de tensão | % |
| DR | Sim/Não |
| Status | Conforme/não conforme |

### 14.2 Diagrama unifilar

Deve conter:

- padrão de entrada;
- medição;
- disjuntor geral;
- DPS;
- DR geral ou setorial;
- barramento de fase;
- barramento de neutro;
- barramento de proteção;
- circuitos terminais;
- disjuntores por circuito;
- condutores;
- indicação de fases;
- aterramento;
- legenda;
- revisão e data.

### 14.3 Memorial de cálculo auditável

| Seção | Conteúdo |
|---|---|
| Premissas | Norma, concessionária, tensão, sistema |
| Ambientes | Área, perímetro, iluminação, TUG |
| Cargas | TUE, fixas, motores, iluminação adicional |
| Demanda | Grupos, fatores, D1, D3, DT |
| Entrada | Categoria, subcategoria, disjuntor, condutor |
| Circuitos | Divisão, IB, fases |
| Condutores | Método, fatores, Iz, seção |
| Queda de tensão | Cálculo por circuito |
| Proteção | Disjuntores, DR, DPS |
| Aterramento | Esquema, PE, equipotencialização |
| Pendências | Erros e alertas |
| Revisão técnica | Campo de aprovação |

### 14.4 Relatório técnico final

O relatório só pode ser emitido se:

| Condição | Obrigatória? |
|---|---|
| Nenhum erro crítico | Sim |
| Cargas completas | Sim |
| Categoria EDP válida | Sim |
| Condutores dimensionados | Sim |
| Queda de tensão aprovada | Sim |
| Proteções validadas | Sim |
| DR analisado | Sim |
| Aterramento definido | Sim |
| Diagrama unifilar gerado | Sim |
| Quadro de cargas gerado | Sim |
| Responsável técnico informado | Sim para uso real |

---

## 15. Fase 13 — Fórmulas, referências, arredondamentos e rastreabilidade

### Objetivo

Eliminar o problema de cálculo não rastreável.

### Implementação

| Item | Correção obrigatória |
|---|---|
| Fórmulas | Mostrar fórmula em todo resultado técnico |
| Referência | Mostrar norma, tabela ou critério usado |
| Dados de entrada | Mostrar todos os dados usados |
| Resultado intermediário | Mostrar antes do arredondamento |
| Arredondamento | Informar regra de arredondamento |
| Alterações | Registrar usuário, data, valor anterior e novo |
| Reprocessamento | Recalcular dependências automaticamente |
| Status | Marcar resultado como preliminar, validado ou bloqueado |

### Exemplo de memória de cálculo esperada

| Campo | Exemplo |
|---|---|
| Cálculo | Corrente de projeto |
| Circuito | C12 — Chuveiro |
| Potência | 7.500 VA |
| Tensão | 220 V |
| Fórmula | IB = S / V |
| Resultado bruto | 34,09 A |
| Resultado exibido | 34,09 A |
| Regra aplicada | Circuito bifásico |
| Status | Conforme |

---

## 16. Fase 14 — Auditoria, testes e homologação

### Objetivo

Validar o sistema antes da liberação para uso real.

### Testes obrigatórios

| Tipo de teste | Objetivo |
|---|---|
| Teste unitário de regra | Validar cada fórmula isolada |
| Teste de integração | Validar fluxo completo: ambiente → carga → circuito → relatório |
| Teste de regressão | Garantir que correções não quebrem cálculos já validados |
| Teste com casos-padrão | Comparar com projetos calculados manualmente |
| Teste de erro | Confirmar bloqueios obrigatórios |
| Teste de rastreabilidade | Confirmar memória de cálculo |
| Teste de relatório | Confirmar artefatos finais |
| Teste de edição | Confirmar invalidação automática após mudança |
| Teste multi-concessionária | Preparar arquitetura para outros padrões |
| Teste por engenheiro responsável | Homologação técnica final |

### Casos mínimos de teste

| Caso | Cenário |
|---|---|
| CT01 | Residência monofásica simples |
| CT02 | Residência bifásica com chuveiro |
| CT03 | Residência trifásica com cozinha, área externa, motores e hidromassagem |
| CT04 | Projeto com carga sem tipo_aparelho |
| CT05 | Projeto trifásico tentando usar subcategoria U |
| CT06 | Circuito sem comprimento |
| CT07 | Circuito com queda de tensão acima do limite |
| CT08 | Circuito de banheiro sem DR |
| CT09 | Circuito com IB maior que In |
| CT10 | Condutor com Iz menor que In |
| CT11 | Alteração de carga após relatório gerado |
| CT12 | Projeto sem esquema de aterramento |

---

## 17. Backlog obrigatório em ordem de execução

### Bloco 1 — Fundação técnica

| Prioridade | Item | Resultado |
|---|---|---|
| Crítica | Criar biblioteca normativa versionada | Regras centralizadas |
| Crítica | Criar modelo de dados técnico | Dados completos |
| Crítica | Criar motor de validação impeditiva | Bloqueio seguro |
| Crítica | Corrigir carga sem tipo_aparelho | Sem carga órfã |

### Bloco 2 — Cargas e demanda

| Prioridade | Item | Resultado |
|---|---|---|
| Alta | Corrigir iluminação mínima | Carga de iluminação rastreável |
| Alta | Corrigir TUG por ambiente | Tomadas rastreáveis |
| Crítica | Corrigir TUE/carga fixa | Equipamentos corretamente enquadrados |
| Crítica | Corrigir grupos EDP | Demanda confiável |
| Crítica | Corrigir categoria/subcategoria EDP | Sem U2 em projeto trifásico |
| Crítica | Corrigir disjuntor/condutor EDP | Entrada coerente |

### Bloco 3 — Circuitos

| Prioridade | Item | Resultado |
|---|---|---|
| Crítica | Implementar divisão final de circuitos | Circuitos reais |
| Alta | Calcular IB por circuito | Correntes confiáveis |
| Alta | Implementar balanceamento final | Fases equilibradas |
| Alta | Permitir edição técnica manual | Controle pelo engenheiro |
| Alta | Invalidar cálculos após alteração | Coerência do sistema |

### Bloco 4 — Condutores e queda

| Prioridade | Item | Resultado |
|---|---|---|
| Crítica | Implementar método de instalação | Base para Iz |
| Crítica | Implementar fatores de correção | Iz corrigida |
| Crítica | Dimensionar fase/neutro/PE | Condutores completos |
| Alta | Calcular queda de tensão | Validação de desempenho |
| Alta | Recalcular seção por queda | Ajuste automático |
| Alta | Registrar memória de cálculo | Auditoria |

### Bloco 5 — Proteção e segurança

| Prioridade | Item | Resultado |
|---|---|---|
| Crítica | Dimensionar disjuntores por circuito | Sobrecorrente |
| Crítica | Validar IB/In/Iz | Coordenação |
| Crítica | Validar capacidade de interrupção | Curto-circuito |
| Crítica | Implementar DR | Proteção contra choque |
| Alta | Implementar DPS | Proteção contra surtos |
| Crítica | Implementar aterramento | Segurança das massas |
| Crítica | Implementar equipotencialização | Segurança complementar |

### Bloco 6 — Artefatos finais

| Prioridade | Item | Resultado |
|---|---|---|
| Alta | Gerar quadro de cargas | Conferência técnica |
| Alta | Gerar diagrama unifilar | Artefato executivo |
| Alta | Gerar memorial de cálculo | Rastreabilidade |
| Alta | Gerar relatório técnico final | Auditoria |
| Alta | Criar lista de pendências | Controle de qualidade |
| Alta | Criar assinatura/revisão técnica | Responsabilidade |

---

## 18. Portões de liberação do sistema

### Gate 1 — Liberação para cálculo preliminar

O sistema só pode entrar em cálculo preliminar se:

- projeto tiver tensão e sistema de fornecimento;
- dependências tiverem dimensões;
- cargas tiverem potência, tensão e tipo;
- regras normativas estiverem versionadas.

### Gate 2 — Liberação para demanda EDP

Somente se:

- todas as cargas tiverem grupo EDP;
- não houver carga sem `tipo_aparelho`;
- concessionária estiver definida;
- categoria e sistema forem compatíveis.

### Gate 3 — Liberação para circuitos

Somente se:

- cargas estiverem completas;
- TUG, TUE e iluminação estiverem validadas;
- circuitos exclusivos tiverem sido identificados;
- ambientes com DR obrigatório estiverem marcados.

### Gate 4 — Liberação para condutores

Somente se:

- cada circuito tiver IB;
- método de instalação;
- comprimento;
- temperatura;
- agrupamento;
- tipo de condutor;
- isolação;
- número de condutores carregados.

### Gate 5 — Liberação para proteção

Somente se:

- condutores estiverem dimensionados;
- Iz corrigida estiver calculada;
- queda de tensão estiver validada;
- curto-circuito presumido estiver informado ou calculado.

### Gate 6 — Liberação para relatório final

Somente se:

- não houver erro crítico;
- todos os circuitos estiverem protegidos;
- DR estiver analisado;
- aterramento estiver definido;
- quadro de cargas estiver completo;
- diagrama unifilar estiver gerado;
- memorial de cálculo estiver disponível;
- responsável técnico tiver revisado.

---

## 19. Informações complementares necessárias para transformar este plano em backlog técnico executável

| Informação necessária | Por que é importante |
|---|---|
| Stack do sistema | Define forma de implementação |
| Banco de dados usado | Define modelagem das tabelas normativas |
| Estrutura atual das tabelas | Permite propor migração correta |
| Código dos módulos de cálculo | Permite localizar as falhas |
| JSON ou payload das dependências | Permite validar campos ausentes |
| JSON ou payload das cargas adicionais | Essencial para corrigir `tipo_aparelho` |
| Regra atual de demanda EDP | Permite corrigir categoria/subcategoria |
| Tabela EDP cadastrada no sistema | Permite validar U/D/T, disjuntor e condutor |
| Fórmulas atualmente implementadas | Permite auditar cálculo por cálculo |
| Modelo atual de circuito | Necessário para divisão final |
| Critérios atuais de balanceamento | Permite melhorar algoritmo |
| Modelo de relatório pretendido | Necessário para memorial final |
| Se haverá múltiplas concessionárias | Define arquitetura de regras |
| Se o sistema será residencial, comercial, industrial ou misto | Define escopo normativo |
| Se o projeto gerará ART/assinatura técnica | Define fluxo de responsabilidade |

---

## 20. Parecer final do plano

A correção obrigatória deve seguir esta prioridade técnica:

1. Corrigir modelo de dados;
2. bloquear entradas incompletas;
3. corrigir classificação de cargas;
4. corrigir demanda e padrão EDP;
5. corrigir divisão de circuitos;
6. dimensionar condutores corretamente;
7. calcular queda de tensão;
8. validar proteção contra sobrecorrente;
9. implementar DR, DPS, aterramento e equipotencialização;
10. gerar quadro, diagrama, memorial e relatório auditável;
11. homologar com casos de teste e revisão de engenheiro eletricista.

Enquanto essas correções não forem concluídas, o sistema deve permanecer classificado como:

**“Ferramenta de pré-dimensionamento, não liberada para projeto executivo de instalações elétricas.”**

