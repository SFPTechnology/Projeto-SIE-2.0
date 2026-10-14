# 📋 Guia Completo — Conformidade NBR 5410

## Índice
1. [Visão Geral](#visão-geral)
2. [Descrição Detalhada dos Campos](#descrição-detalhada-dos-campos)
3. [Referência de Valores](#referência-de-valores)
4. [Fluxo de Preenchimento](#fluxo-de-preenchimento)
5. [Checklist de Conformidade](#checklist-de-conformidade)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Tabelas de Referência Rápida](#tabelas-de-referência-rápida)

---

## Visão Geral

Este formulário implementa os requisitos técnicos da **NBR 5410:2004** — *Instalações Elétricas de Baixa Tensão em Edificações*. É um instrumento de validação de conformidade para circuitos e equipamentos em ambientes de banheiro, que possuem requisitos de proteção rigorosos.

### O que é NBR 5410?
A Norma Brasileira NBR 5410 estabelece as exigências essenciais de segurança para instalações elétricas de baixa tensão (até 1000V CA), incluindo:
- Proteção contra choques elétricos
- Proteção contra efeitos térmicos
- Proteção contra sobrecorrentes
- Requisitos especiais para ambientes úmidos/molhados (banheiros, cozinhas, áreas externas)

---

## Descrição Detalhada dos Campos

### 1️⃣ **Zona do Banheiro** (Dropdown — Obrigatório)

#### O que é?
Define a **classificação ambiental** do banheiro conforme os requisitos de proteção da NBR 5410. A norma divide o banheiro em zonas concêntricas, cada uma com diferentes riscos de choque elétrico e contato com água.

#### Por que importa?
Diferentes zonas exigem:
- Diferentes graus de proteção IP
- Diferentes tipos de disjuntores e proteções
- Diferentes materiais de acabamento
- Diferentes restrições de uso de equipamentos

#### Valores Disponíveis

| Zona | Localização | Descrição | Proteção Mínima |
|------|-------------|-----------|-----------------|
| **Zona 0** | Interior da banheira/chuveiro | Volume onde a água está presente permanentemente ou com frequência elevada | IPX7 (submersível) |
| **Zona 1** | Ao redor da banheira/chuveiro | De 0 a 0,6m horizontalmente; de 0 a 2,25m verticalmente | IPX4 (jatos de água) |
| **Zona 2** | Área ampliada | De 0,6m a 1,2m horizontalmente além da Zona 1 | IPX4 (jatos de água) |
| **Zona 3** | Externo ao banheiro | Área próxima às zonas anteriores; até 2,4m da banheira | IPX1 (gotejamento) |

#### Como Preencher?
1. **Identifique a localização física** do equipamento/circuito dentro do banheiro
2. **Meça a distância** da banheira ou chuveiro
3. **Consulte a tabela acima** e selecione a zona correspondente

**Exemplo:**
- Tomada a 0,3m da banheira → Zona 1
- Tomada a 0,8m da banheira → Zona 2
- Circuito para ventilador a 2m de distância → Zona 3

#### ⚠️ Caso Especial: Zona 0
Equipamentos em Zona 0 são raríssimos. Apenas dispositivos especialmente certificados (ex: iluminação submersível de piscina) são permitidos. Em banheiros comuns, **Zona 0 praticamente não é utilizada**.

---

### 2️⃣ **DB Informado** (Dropdown — Obrigatório)

#### O que é?
Indica se foi especificado um **Disjuntor Diferencial-Residual (DR/DDR)** no projeto. É o componente de proteção contra choques elétricos mais importante em banheiros.

#### O que é DB/DR/DDR?
- **DB** = Disjuntor (proteção contra sobrecorrente)
- **DR** = Disjuntor Residual (proteção contra choques)
- **DDR** = Disjuntor Diferencial-Residual (nome técnico completo)

Um DR detecta **correntes de fuga** (quando parte da corrente volta por um caminho não planejado, ex: através do corpo humano) e desliga instantaneamente (10-30ms).

#### Valores Disponíveis

| Valor | Significado | Conformidade | Observação |
|-------|-------------|-------------|-----------|
| **Sim** | DB/DR foi especificado no projeto | ✅ Conforme | O circuito tem proteção |
| **Não** | DB/DR não foi informado | ❌ Não-conforme | Circuito desprotegido (CRÍTICO) |

#### Requisitos NBR 5410
- **Todos os circuitos em banheiro DEVEM ter DB/DR**
- Sensibilidade típica: **30mA** (corrente diferencial-residual nominala)
- Para certos casos: **10mA** (proteção adicional)
- Classe: **A** (detecta corrente alternada) ou **AC** (mais comum)

#### Como Preencher?
1. **Revise o projeto elétrico** do banheiro
2. **Identifique o diagrama unifilar** e localize o circuito/zona
3. **Verifique se há um DR/DDR** alimentando aquele circuito
4. Se **SIM** → Selecione "Sim"
5. Se **NÃO** → Selecione "Não" e **ALERTE** — projeto precisa de revisão

**Exemplo:**
```
Diagrama Unifilar (simplificado):
QDC (Quadro de Distribuição)
  └─ Disjuntor Diferencial-Residual 30mA
      ├─ Circuito Tomadas Banheiro (20A)
      ├─ Circuito Iluminação Banheiro (10A)
      └─ Circuito Ventilador (10A)

→ DB Informado: SIM
```

#### ⚠️ Crítico
Circuitos sem DR são a causa principal de acidentes elétricos em banheiros. Se "Não" for selecionado, o projeto está **não-conforme com NBR 5410**.

---

### 3️⃣ **Grau de Proteção IP** (Campo de Texto — Obrigatório)

#### O que é?
Define o **Índice de Proteção (IP)** de um equipamento contra:
- **Contato com partes vivas** (fios, componentes eletrônicos)
- **Ingresso de objetos sólidos** (poeira, areia)
- **Ingresso de água/umidade** (respingo, imersão)

#### Formato IP (IEC 60529)
```
IPxy

Onde:
  x = Proteção contra contato com partes vivas e objetos sólidos (0-6)
  y = Proteção contra ingresso de água (0-8)
```

#### Tabela de Proteção (x — Contato)

| Código | Proteção | Descrição | Exemplo |
|--------|----------|-----------|---------|
| **0** | Nenhuma | Nenhuma proteção | — |
| **1** | ≥50mm | Proteção contra contato com o dedo | Aberturas ≥50mm |
| **2** | ≥12.5mm | Proteção contra dedos/objetos finos | Aberturas ≥12.5mm |
| **3** | ≥2.5mm | Proteção contra ferramentas finas/arame | Aberturas ≥2.5mm |
| **4** | ≥1mm | Proteção contra fios/objetos ≥1mm | Aberturas ≥1mm |
| **5** | Proteção completa | Proteção contra poeira prejudicial | Recinto com pequena entrada de pó |
| **6** | Totalmente protegido | À prova de poeira | Recinto hermeticamente fechado |

#### Tabela de Proteção (y — Água)

| Código | Proteção | Descrição | Aplicação |
|--------|----------|-----------|-----------|
| **0** | Nenhuma | Nenhuma proteção | — |
| **1** | Gotejamento | Gotejamento de água vertical | Áreas secas |
| **2** | Gotejamento 15° | Gotejamento até 15° da vertical | Áreas secas |
| **3** | Aspersão | Jatos de água até 60° da vertical | Cozinhas, áreas próximas |
| **4** | Jatos | Jatos de água em todas as direções | **Banheiros (Zona 1-2)** |
| **5** | Jatos potentes | Jatos potentes de água em todas as direções | Piscinas, áreas externas |
| **6** | Enxurrada/mar | Possibilidade de enxurrada ou mar | Marinas, áreas costeiras |
| **7** | Imersão temporária | Submersão até 1m por até 30min | Equipamentos de piscina |
| **X** | **Submersão** | Submersão contínua a profundidades especificadas | **IPX7, IPX8** para banheiros críticos |

#### Valores Esperados por Zona

| Zona | IP Mínimo | Justificativa | Exemplo de Equipamento |
|------|-----------|---------------|----------------------|
| **Zona 0** | **IPX7** ou **IPX8** | Submersão contínua/frequente | Iluminação de piscina |
| **Zona 1** | **IPX4** | Jatos de água frequentes | Tomada em Zona 1 |
| **Zona 2** | **IPX4** | Jatos de água ocasionais | Tomada próxima ao chuveiro |
| **Zona 3** | **IPX1** | Gotejamento acidental | Tomada distante da banheira |

#### Exemplos de Códigos Válidos

| Código | Interpretação | Adequado Para |
|--------|---------------|---------------|
| **IP44** | Proteção contra fios (4) + Jatos (4) | Banheiros, Zona 1-2 ✅ |
| **IP54** | Proteção contra poeira (5) + Jatos (4) | Banheiros, ambientes úmidos ✅ |
| **IP65** | À prova de poeira (6) + Jatos potentes (5) | Áreas externas, piscinas ✅ |
| **IPX7** | Sem proteção contra contato + Submersão | Banheiro Zona 0 (raro) ✅ |
| **IP20** | Contra dedos (2) + Gotejamento (0) | Apenas áreas secas ❌ |
| **IP00** | Nenhuma proteção | Não permitido em banheiro ❌ |

#### Como Preencher?

1. **Identifique o equipamento/acessório** (tomada, luminária, interruptor)
2. **Localize a placa técnica** ou datasheet do fabricante
3. **Procure pelo código IP** (geralmente impresso no corpo)
4. **Verifique se o IP é adequado para a zona** (veja tabela acima)
5. **Digite o código exato** no campo (ex: IP44, IPX7)

**Exemplo Prático:**
```
Equipamento: Tomada dupla Legrand (Zona 2)
Placa técnica: IP44
Campo: [IP44]
Verificação: Zona 2 exige IPX4 → IP44 ✅ Conforme
```

#### ⚠️ Erros Comuns
- ❌ Deixar em branco (campo obrigatório)
- ❌ Escrever "IP 44" com espaço (padrão é sem espaço: IP44)
- ❌ Usar IP menor que o requerido para a zona
- ❌ Confundir Y (água) com X (contato) — **só a proteção contra água importa em banheiro**

---

### 4️⃣ **Influência Externa** (Dropdown — Recomendado)

#### O que é?
Classifica **fatores ambientais adicionais** que afetam a escolha de materiais, acabamentos e proteções além do requisito básico de proteção contra água.

#### Exemplos de Influências Externas
- **Temperatura extrema** (ambientes muito quentes ou frios)
- **Corrosividade** (proximidade com mar, produtos químicos)
- **Umidade relativa alta** (saunas, cozinhas comerciais)
- **Radiação solar intensa** (áreas externas)
- **Vibração/movimento** (proximidade a máquinas)
- **Poluição** (indústrias próximas)

#### Valores Disponíveis

| Valor | Significado | Quando Usar | Exemplo |
|-------|-------------|-----------|---------|
| **Obrigatório** | Há fatores ambientais críticos que exigem proteção/material especial | Quando há influências externas que aumentam riscos além do padrão | Banheiro em sauna (temperatura 80°C) |
| **Opcional** | Não há fatores especiais; equipamento é resistente o suficiente | Banheiro comum em clima temperado | Banheiro residencial normal |
| **Não aplicável** | Campo não se aplica a este circuito/equipamento | Circuitos em áreas secas ou sem fatores adicionais | Tomada em sala de estar |

#### Como Preencher?

1. **Analise o ambiente** do banheiro:
   - Localização (interior/exterior)?
   - Temperatura típica (normal/extrema)?
   - Umidade (normal/muito alta)?
   - Proximidade com produtos corrosivos?

2. **Se há fatores especiais** → Selecione **"Obrigatório"**
   - Neste caso, documente na seção **"Observações"** quais são os fatores

3. **Se é um banheiro comum** → Selecione **"Opcional"**

4. **Se não se aplica** → Selecione **"Não aplicável"**

**Exemplos:**
```
Banheiro residencial comum em apartamento em São Paulo
→ Influência Externa: Opcional

Banheiro em sauna (80°C + 80% umidade relativa)
→ Influência Externa: Obrigatório
→ Observações: "Ambiente de alta temperatura e umidade"

Circuito em garagem (área seca, sem fatores especiais)
→ Influência Externa: Não aplicável
```

#### ⚠️ Nota
Em banheiros com **umidade normal**, a proteção contra água (IP4X) já é suficiente. Use **"Obrigatório"** apenas se há fatores **adicionais** além da umidade típica.

---

### 5️⃣ **Classe** (Campo de Texto — Obrigatório)

#### O que é?
Define a **classificação técnica** do equipamento ou circuito conforme a NBR 5410. Os códigos estabelecem o padrão de proteção e acabamento esperado.

#### Nomenclatura
Os códigos seguem o padrão:
- **Primeira letra:** Categoria (A=Acessório, M=Motor, E=Equipamento, etc.)
- **Letra seguinte:** Subcategoria (D=Dispositivo, L=Luminária)
- **Número:** Classe de proteção (1-4, de menor para maior proteção)

#### Códigos Principais para Banheiro

| Código | Nome Completo | Proteção | Uso | IP Mínimo |
|--------|--------------|----------|-----|----------|
| **AD1** | Acessório Dispositivo Classe 1 | Básica | Tomada em área seca | IP20 |
| **AD2** | Acessório Dispositivo Classe 2 | Reforçada | Tomada em banheiro (sem DB integrado) | IP44 |
| **AD3** | Acessório Dispositivo Classe 3 | Extra reforçada | Tomada em banheiro com proteção adicional | IP54 |
| **AD4** | Acessório Dispositivo Classe 4 | Máxima | Equipamento classe II ou com DB integrado | IP65 |
| **MD1** | Motor Dispositivo Classe 1 | — | Ventilador/Exaustor simples | IP44 |
| **MD2** | Motor Dispositivo Classe 2 | — | Ventilador com termostato | IP54 |
| **AL1** | Acessório Luminária Classe 1 | Proteção básica | Iluminação incandescente | IP20 |
| **AL2** | Acessório Luminária Classe 2 | Proteção reforçada | Iluminação LED/fluorescente em banheiro | IP44 |

#### Seleção por Tipo de Equipamento

**Para Tomadas:**
- Zona 1-2, sem DB integrado → **AD2**
- Zona 1-2, com DB integrado ou classe II → **AD4**
- Zona 3 → **AD2**

**Para Iluminação:**
- Iluminação comum em banheiro → **AL2**
- Iluminação com proteção extra (LED selada) → **AL3**

**Para Ventilação:**
- Ventilador/exaustor simples → **MD1**
- Ventilador com termostato/timer → **MD2**

#### Como Preencher?

1. **Identifique o tipo de equipamento** (tomada, luminária, ventilador)
2. **Verifique a zona** (Zona 0-1 exigem classe maior)
3. **Consulte a tabela acima**
4. **Digite o código** exato (ex: AD2, AL2, MD1)

**Exemplo Completo:**
```
Equipamento: Tomada dupla em Zona 2
Tipo: Tomada (A)
Dispositivo (D): Acessório dispositivo
Proteção: Zona 2 (nível 2)
→ Classe: AD2

Campo: [AD2]
```

#### ⚠️ Erros Comuns
- ❌ Usar AD1 em banheiro (inadequado; IP20 é insuficiente)
- ❌ Misturar letras maiúsculas/minúsculas incorretamente (padrão: AD2, não ad2)
- ❌ Inventar códigos que não existem (ex: AD5 — máximo é AD4)

---

### 6️⃣ **Observações** (Área de Texto — Opcional)

#### O que é?
Campo livre para **notas técnicas adicionais** que:
- Justificam escolhas de conformidade
- Alertam sobre particularidades do circuito
- Documentam exceções ou casos especiais
- Facilitam auditorias futuras

#### Por que importa?
Uma boa observação torna o projeto **auditável** e **defensável** em caso de inspeção.

#### Exemplos de Observações Válidas

```
✅ "Circuito protegido por DR classe A, sensibilidade 30mA, 
   conforme Tabela 33 da NBR 5410"

✅ "Tomada localizada a 0,4m horizontalmente da banheira, 
   enquadrada em Zona 1"

✅ "Equipamento classe II (duplo isolamento), 
   não requer DR adicional"

✅ "Luminária LED IP67 submersível, adequada para Zona 0 
   em futuras ampliações"

✅ "Ventilador exaustor com sensor de umidade e timer 
   automático, MD2"

✅ "Circuito alimenta apenas tomadas em Zona 2, 
   distância mínima 0,6m da banheira"

❌ "OK" (vago, não técnico)
❌ "Tomada" (informação insuficiente)
❌ "Conforme" (sem justificativa)
```

#### Estrutura Recomendada de Observação

```
[Tipo de Equipamento] [Localização] [Proteção/Classe] [Justificativa/Referência NBR]
```

**Exemplo:**
```
"Tomada tipo Zona 2, distância 0,8m da banheira, 
 classe AD2, IP44, protegida por DR 30mA conforme 
 Figura 7 da NBR 5410:2004"
```

---

## Referência de Valores

### Resumo Rápido — Zona vs Proteção

| Zona | IP Mínimo | DB/DR | Classe Mín. | Descrição |
|------|-----------|-------|-------------|-----------|
| 0 | IPX7/X8 | Não aplicável* | — | Interior da banheira (raro) |
| 1 | IPX4 | **Sim (obrig.)** | AD2 | Ao redor da banheira |
| 2 | IPX4 | **Sim (obrig.)** | AD2 | Próximo à banheira |
| 3 | IPX1 | Recomendado | AD1/AD2 | Fora do banheiro |

*Zona 0: Equipamentos especiais apenas; DR não é proteção adequada.

### Códigos Classe — Referência Rápida

```
ACESSÓRIOS (Tomadas, Interruptores, Outlets):
  AD1 → Classe 1 (áreas secas)
  AD2 → Classe 2 (banheiros padrão) ← MAIS COMUM
  AD3 → Classe 3 (proteção extra)
  AD4 → Classe 4 (máxima proteção)

ILUMINAÇÃO:
  AL1 → Classe 1 (áreas secas)
  AL2 → Classe 2 (banheiros) ← MAIS COMUM
  AL3 → Classe 3 (proteção extra)

MOTORES (Ventiladores, Exaustores):
  MD1 → Classe 1 (ventilador simples) ← MAIS COMUM
  MD2 → Classe 2 (ventilador com controle)
```

---

## Fluxo de Preenchimento

### Passo a Passo — Ordem Recomendada

```
PASSO 1: ZONA DO BANHEIRO
  ↓ Identifique a localização do equipamento/circuito
  ↓ Meça distância da banheira
  ↓ Selecione Zona 0, 1, 2 ou 3
  
PASSO 2: GRAU DE PROTEÇÃO IP
  ↓ Consulte a placa técnica do equipamento
  ↓ Localize o código IP (ex: IP44)
  ↓ Verifique se é adequado para a zona escolhida
  ↓ Digite o código no campo
  
PASSO 3: DB INFORMADO
  ↓ Revise o diagrama unifilar do projeto
  ↓ Verifique se há DR alimentando o circuito
  ↓ Selecione Sim ou Não
  
PASSO 4: CLASSE
  ↓ Identifique o tipo de equipamento (tomada, lâmpada, motor)
  ↓ Selecione a classe apropriada (AD2, AL2, MD1, etc.)
  
PASSO 5: INFLUÊNCIA EXTERNA
  ↓ Analise se há fatores ambientais especiais
  ↓ Selecione Obrigatório, Opcional ou Não aplicável
  
PASSO 6: OBSERVAÇÕES
  ↓ Documente justificativas técnicas
  ↓ Referencie normas e tabelas quando relevante
  ↓ Deixe em branco se a conformidade é óbvia
```

### Variantes Comuns

#### Cenário 1: Tomada em Banheiro Residencial Padrão
```
Zona: Zona 2
IP: IP44
DB Informado: Sim
Classe: AD2
Influência Externa: Opcional
Observações: "Tomada dupla Legrand, classe AD2, IP44, 
             protegida por DR 30mA"
```

#### Cenário 2: Ventilador Exaustor em Banheiro
```
Zona: Zona 3
IP: IP44
DB Informado: Sim (circuito separado com DR)
Classe: MD1
Influência Externa: Opcional
Observações: "Ventilador exaustor com sensor de umidade,
             MD1, IP44, circuito independente com DR 30mA"
```

#### Cenário 3: Iluminação em Zona 1
```
Zona: Zona 1
IP: IPX4
DB Informado: Sim
Classe: AL2
Influência Externa: Opcional
Observações: "Luminária LED IP44 anti-embaçamento,
             classe AL2, adequada para Zona 1"
```

---

## Checklist de Conformidade

Use esta checklist para validar completamente a conformidade de um circuito/equipamento:

### ☑️ Checklist Técnica — NBR 5410

- [ ] **Localização identificada** — Qual é a zona exata?
- [ ] **IP adequado** — Código IP é >= mínimo para a zona?
- [ ] **DB especificado** — Há proteção DR/DDR no projeto?
- [ ] **Classe correta** — Classe corresponde ao tipo de equipamento?
- [ ] **Factores ambientais** — Há influências externas não consideradas?
- [ ] **Norma referenciada** — Observações citam artigos/tabelas da NBR 5410?
- [ ] **Equipamento certificado** — Tem marca de conformidade (ex: INMETRO)?

### ⚠️ Alertas Críticos — BLOQUEADORES

Se qualquer um desses itens está SIM, o circuito é **NÃO-CONFORME**:

- [ ] Zona 1 ou 2 **SEM DB** → ❌ CRÍTICO
- [ ] IP menor que IPX4 em Zona 1-2 → ❌ CRÍTICO
- [ ] Equipamento com IP00 em qualquer banheiro → ❌ CRÍTICO
- [ ] Classe AD1 em banheiro → ❌ CRÍTICO
- [ ] Equipo não certificado → ⚠️ VERIFICAR

---

## Exemplos Práticos

### Exemplo 1: Tomada Dupla em Banheiro Padrão

**Situação:**
```
- Localização: Parede ao lado do espelho, 1,2m da banheira
- Equipamento: Tomada dupla Legrand Domomat branca
- Projeto: Quadro com DR 30mA classe A
```

**Preenchimento:**
```
Zona do Banheiro: Zona 2 (está a 1,2m da banheira)
DB Informado: Sim (quadro tem DR 30mA)
Grau de Proteção IP: IP44 (conforme placa do equipamento)
Influência Externa: Opcional
Classe: AD2 (tomada padrão em banheiro)
Observações: "Tomada Legrand Domomat, classe AD2, IP44, 
             alimentada por circuito protegido por DR 30mA"
```

**Conformidade: ✅ CONFORME**

---

### Exemplo 2: Luminária em Zona 1 (Próxima ao Espelho)

**Situação:**
```
- Localização: Luminária acima do espelho, 0,3m da banheira
- Equipamento: Arandela LED IP67 Brilia
- Alimentação: Circuito com DR 30mA
```

**Preenchimento:**
```
Zona do Banheiro: Zona 1 (a 0,3m da banheira)
DB Informado: Sim (circuito protegido por DR 30mA)
Grau de Proteção IP: IP67 (conforme especificação técnica)
Influência Externa: Opcional
Classe: AL2 (iluminação em banheiro)
Observações: "Arandela LED anti-embaçamento Brilia, 
             classe AL2, IP67, adequada para Zona 1, 
             circuito com DR 30mA"
```

**Conformidade: ✅ CONFORME** (IP67 > IPX4 requerido)

---

### Exemplo 3: Ventilador Exaustor (Zona 3)

**Situação:**
```
- Localização: Montado na parede, a 2m da banheira
- Equipamento: Ventilador Intelbras 200mm, sensor de umidade
- Alimentação: Circuito independente com DR 30mA
```

**Preenchimento:**
```
Zona do Banheiro: Zona 3 (fora da área principal do banheiro)
DB Informado: Sim (circuito independente com DR)
Grau de Proteção IP: IP44
Influência Externa: Obrigatório (ambiente úmido - ventilação crítica)
Classe: MD1 (motor simples para ventilação)
Observações: "Ventilador Intelbras 200mm com sensor automático 
             de umidade, classe MD1, IP44, circuito independente 
             alimentado com DR 30mA. Acionamento automático em 
             ambientes com umidade relativa >80%"
```

**Conformidade: ✅ CONFORME**

---

### Exemplo 4: ❌ NÃO-CONFORME — Tomada sem DR

**Situação:**
```
- Localização: Tomada próxima ao chuveiro (Zona 1)
- Equipamento: Tomada comum com IP20
- Alimentação: Circuito geral SEM DR
```

**Preenchimento:**
```
Zona do Banheiro: Zona 1
DB Informado: Não ← ⚠️ ALERTA
Grau de Proteção IP: IP20 ← ⚠️ INSUFICIENTE
Influência Externa: Opcional
Classe: AD1 ← ⚠️ INADEQUADO
Observações: "CRÍTICO: Circuito sem proteção DR, IP insuficiente, 
             classe inadequada. Projeto NÃO CONFORME NBR 5410. 
             Requer revisão urgente."
```

**Conformidade: ❌ NÃO-CONFORME** (múltiplas violações)

**Ações Corretivas Necessárias:**
1. Instalar DR 30mA no circuito
2. Trocar tomada por modelo IP44 mínimo
3. Validar classe AD2 ou superior
4. Re-submeter para conformidade

---

## Tabelas de Referência Rápida

### Tabela 1: Zona × IP × DB — Matriz de Decisão

| Zona | Localização | IP Mínimo | DB Obrigatório | Classe Mín. | Permitidos |
|------|-------------|-----------|---|---|---|
| **0** | Interior banheira | IPX7/X8 | Não* | — | Apenas equipamentos especiais certificados |
| **1** | 0-0,6m da banheira | IPX4 | ✅ SIM | AD2 | Tomadas, luminárias, ventiladores |
| **2** | 0,6-1,2m da banheira | IPX4 | ✅ SIM | AD2 | Tomadas, luminárias, ventiladores |
| **3** | Fora do banheiro | IPX1 | Recomendado | AD1 | Qualquer equipamento comum |

---

### Tabela 2: Equipamentos Comuns × Classe × IP

| Equipamento | Tipo | Classe Recomendada | IP Mínimo | Zona Máx. |
|-------------|------|-------------------|-----------|-----------|
| Tomada dupla | Acessório | AD2 | IP44 | Zona 2 |
| Interruptor simples | Acessório | AD2 | IP44 | Zona 2 |
| Luminária LED incandescente | Luminária | AL2 | IP44 | Zona 1 |
| Arandela espelho | Luminária | AL2 | IP54 | Zona 1 |
| Ventilador exaustor | Motor | MD1 | IP44 | Zona 3 |
| Chuveiro elétrico | Acessório | AD4 | IP44 | Zona 3 |
| Secador de cabelo (tomada) | Acessório | AD2 | IP44 | Zona 2 |

---

### Tabela 3: DR — Requisitos Técnicos Mínimos

| Parâmetro | Valor Padrão | Valores Alternativos | Norma |
|-----------|--------------|-------------------|-------|
| **Sensibilidade (IΔn)** | 30 mA | 10 mA (proteção extra) | NBR 5410 |
| **Tipo de Corrente** | Classe A | Classe AC | IEC 61008 |
| **Tempo de Resposta** | < 30 ms | < 10 ms (extra) | IEC 61008 |
| **Curva de Disparo** | "B" ou "C" | "D" (industrial) | IEC 60898 |

**Nota:** Para banheiros residenciais, DR 30mA Classe A é padrão. Não há necessidade de 10mA em circuitos comuns.

---

## Referências Normativas

### Documentos Principais
- **NBR 5410:2004** — Instalações Elétricas de Baixa Tensão em Edificações
  - Seção 7: Proteção para garantir segurança
  - Tabela 33: Requisitos especiais para banheiros
  - Figura 7: Zonas do banheiro

- **IEC 60529** — Índice de Proteção (IP)
  - Classificação de graus de proteção para equipamentos elétricos

- **IEC 61008-1** — Disjuntores Diferenciais-Residuais para uso doméstico
  - Características técnicas de DRs

- **ABNT NBR 14039:2005** — Instalações Elétricas de Média Tensão (complemento)

---

## Dúvidas Frequentes (FAQ)

### P: Qual é a diferença entre IP44 e IPX4?

**R:** 
- **IP44:** Proteção contra contato (até 1mm) + Jatos de água (ambos dígitos especificados)
- **IPX4:** Sem proteção contra contato especificada + Jatos de água (X = qualquer proteção)

Em banheiros, **IP44 é preferível** pois oferece ambas as proteções. **IPX4 é aceitável**, mas menos protetor contra contato.

---

### P: Posso usar uma tomada IP20 em banheiro se tiver DR?

**R:** 
**Não.** O DR protege contra choques elétricos, mas não contra água. Uma tomada IP20 deixa partes vivas expostas à umidade, causando corrosão e risco de curto-circuito. **IP44 é obrigatório em Zona 1-2**.

---

### P: É necessário DR em Zona 3?

**R:** 
**Tecnicamente não é obrigatório** (Zona 3 está fora do banheiro), mas é **altamente recomendado**. Qualquer circuito alimentado por um mesmo DR que proteja Zona 1-2 herda a proteção. É uma boa prática.

---

### P: O que fazer se o equipamento não tem IP especificado?

**R:** 
**Não use.** Equipamentos sem certificação ou especificação de IP não devem ser instalados em banheiros. Solicite ao fornecedor a documentação técnica ou procure por alternativa certificada.

---

### P: Posso usar classe AD1 em banheiro?

**R:** 
**Não.** Classe AD1 é apenas para áreas secas (IP20). **Classe AD2 é mínimo** para banheiros (Zona 2-3). **AD4 é melhor** para Zona 1.

---

### P: DR 10mA é melhor que 30mA?

**R:** 
**Sim, é mais seguro**, mas **não é obrigatório** em banheiros residenciais. Padrão é 30mA. Use 10mA apenas se o projetista especificar (ex: chuveiro elétrico de alta potência).

---

## Conclusão

Este formulário de Conformidade NBR 5410 é uma ferramenta essencial para **validar segurança elétrica** em banheiros. O preenchimento correto exige:

1. **Compreensão das zonas** e seus requisitos
2. **Especificação correta de IP** conforme equipamento
3. **Garantia de proteção por DR** em Zona 1-2
4. **Seleção apropriada de classe** de equipamento
5. **Documentação clara** em observações

**Conformidade = Segurança. Não há atalhos.**

---

**Documento versão 1.0 | Última atualização: 2026-06-21**  
**Gerado por: Atlas (AIOX Analyst) | Synkra AIOX Framework**

