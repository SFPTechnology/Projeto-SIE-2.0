# Análise de Conformidade NBR 5410 — Seção "Dependências"

**Analista:** Atlas (Decoder) — AIOX Business Analyst  
**Data:** 20/06/2026  
**Versão normativa de referência:** ABNT NBR 5410:2004 (Instalações elétricas de baixa tensão)  
**Escopo:** Verificação da classificação e dimensionamento das dependências conforme NBR 5410, com identificação de gaps de não conformidade e incongruências no sistema proposto.

---

## Sumário

1. [Dados Extraídos das Imagens](#1-dados-extraídos-das-imagens)
2. [Metodologia de Análise](#2-metodologia-de-análise)
3. [Conformidades Identificadas](#3-conformidades-identificadas)
4. [Gaps e Não-Conformidades Potenciais](#4-gaps-e-não-conformidades-potenciais)
5. [Incongruências Internas do Sistema](#5-incongruências-internas-do-sistema)
6. [Análise de Coeficiente de Iluminação](#6-análise-de-coeficiente-de-iluminação)
7. [Análise Geométrica das Dependências](#7-análise-geométrica-das-dependências)
8. [Resumo dos Gaps por Criticidade](#8-resumo-dos-gaps-por-criticidade)
9. [Recomendações para o Sistema](#9-recomendações-para-o-sistema)
10. [Referências Normativas](#10-referências-normativas)

---

## 1. Dados Extraídos das Imagens

### 1.1 Tabela Completa de Dependências

| Dependência | ID | Versão | Dimensões (m) | Área (m²) | Perímetro (m) | Iluminação | Tomadas (TUG) | Cargas Adicionais | Estado | Atualizado |
|---|---|---|---|---|---|---|---|---|---|---|
| sala | dep-1781808008186 | v3 | 6,00 × 6,00 | 36,00 | 24,00 | 1 pt · 520 VA [VERIFICAR] | 5 · 500 VA [VERIFICAR] | 3.516 VA — TUE: Ar-condicionado 1× 3.516 VA | Calculada | 20/06/2026 09:07 |
| dormitório | dep-1781807783475 | v1 | 4,00 × 4,00 | 16,00 | 16,00 | 1 pt · 220 VA [VERIFICAR] | 4 · 400 VA [VERIFICAR] | — | Calculada | 18/06/2026 15:34 |
| dormitório | dep-1781807827642 | v1 | 6,00 × 4,00 | 24,00 | 20,00 | 1 pt · 340 VA [VERIFICAR] | 4 · 400 VA [VERIFICAR] | — | Calculada | 18/06/2026 15:34 |
| hall-corredor | dep-1781808149544 | v1 | 6,00 × 1,20 | 7,20 | 14,40 | 1 pt · 100 VA [VERIFICAR] | 3 · 300 VA [VERIFICAR] | — | Calculada | 18/06/2026 15:40 |
| banheiro | dep-1781808426942 | v1 | 6,00 × 6,00 | 36,00 | 24,00 | 1 pt · 520 VA [VERIFICAR] | 1 · 600 VA [VERIFICAR] | — | Calculada | 18/06/2026 15:43 |
| varanda | dep-1781809514324 | v1 | 3,00 × 8,00 | 24,00 | 22,00 | 1 pt · 340 VA [VERIFICAR] | 5 · 500 VA [VERIFICAR] | — | Calculada | 18/06/2026 15:59 |
| dormitório | dep-test-now | v1 | 3,00 × 4,00 | 12,00 | 14,00 | 1 pt · 160 VA [VERIFICAR] | 3 · 300 VA [VERIFICAR] | — | Calculada | 18/06/2026 16:03 |
| banheiro | dep-1781808562385 | v9 | 3,00 × 4,00 | 12,00 | 14,00 | 1 pt · 160 VA [VERIFICAR] | 1 · 600 VA [VERIFICAR] | 9.210 VA total: LED 4×15=60 VA + Banheira Hidro 1×1.650 VA + Chuveiro 1×7.500 VA | Calculada | 19/06/2026 12:28 |
| área-externa (Quintal) | dep-1781... | v12 | 8,00 × 10,00 | 80,00 | 36,00 | 1 pt · 1.180 VA [VERIFICAR] | 8 · 800 VA [VERIFICAR] | 7.500 VA: Holofote 5×100=500 VA + Motor piscina 1×3.000 VA + Bomba piscina 1×4.000 VA | Calculada | 20/06/2026 09:16 |
| cozinha | dep-1781808373935 | v4 | 6,00 × 6,00 | 36,00 | 24,00 | 1 pt · 520 VA [VERIFICAR] | 7 · 2.200 VA [VERIFICAR] | 6.360 VA: LED 4×15=60 VA + Exaustor 1×1.250 VA + Forno micro-ondas 1×2.250 VA + Forno elétrico 1×2.800 VA | Calculada | 19/06/2026 12:28 |
| área-externa (Garagem coberta) | dep-1781... | v2 | 10,00 × 6,00 | 60,00 | 32,00 | 1 pt · 880 VA [VERIFICAR] | 7 · 700 VA [VERIFICAR] | 1.272 VA: Luminária de parede 4×18=72 VA + Portão eletrônico 1×1.200 VA | Calculada | 20/06/2026 17:10 |

### 1.2 Colunas do Sistema Identificadas

O sistema apresenta as seguintes colunas na seção "Dependências":

- **Tipo** — nome descritivo da dependência
- **Dimensões (m)** — L × C em metros
- **Área (m²)** — calculada como A = L × C
- **Perímetro (m)** — calculado como P = 2(L+C)
- **Iluminação** — número de pontos e carga em VA (marcado [VERIFICAR])
- **Tomadas** — quantidade e carga unitária em VA (marcado [VERIFICAR])
- **Cargas adicionais** — TUE e Outras, com discriminação por equipamento
- **Estado** — situação do cálculo (todas "Calculada")
- **Atualizado** — data/hora da última modificação
- **Ações** — ícones para editar, histórico, menu

---

## 2. Metodologia de Análise

### 2.1 Abordagem

A análise foi conduzida em quatro eixos:

1. **Verificação dimensional** — conferência matemática das fórmulas de área e perímetro
2. **Conformidade normativa** — verificação dos valores contra os mínimos exigidos pela NBR 5410:2004
3. **Análise de classificação** — avaliação dos tipos de ambiente e sua aderência à taxonomia normativa
4. **Análise de completude** — identificação de campos e informações ausentes que a norma exige

### 2.2 Seções da NBR 5410 Consultadas

| Seção | Conteúdo |
|---|---|
| 5.1 | Influências externas (códigos AA–HZ) |
| 7.1 | Localidades de banho e ducha — zonas 0, 1, 2 |
| 7.2 | Piscinas e fontes ornamentais — zonas A, B, C |
| 9.3.1.1 | Capacidade mínima de circuitos |
| 9.4.1.1 | Pontos de tomada por tipo de ambiente |
| 9.4.1.2 | Circuitos para tomadas de uso específico (TUE) |
| 9.5.2 | Proteção por dispositivo de corrente diferencial-residual (DR/IDR) |

---

## 3. Conformidades Identificadas

### 3.1 Geometria Calculada — Correta

Verificação de todos os perímetros declarados pelo sistema:

| Dependência | L (m) | C (m) | A = L×C (m²) | P = 2(L+C) (m) | Sistema A | Sistema P | Status |
|---|---|---|---|---|---|---|---|
| sala | 6,00 | 6,00 | 36,00 | 24,00 | 36,00 | 24,00 | ✅ |
| dormitório | 4,00 | 4,00 | 16,00 | 16,00 | 16,00 | 16,00 | ✅ |
| dormitório | 6,00 | 4,00 | 24,00 | 20,00 | 24,00 | 20,00 | ✅ |
| hall-corredor | 6,00 | 1,20 | 7,20 | 14,40 | 7,20 | 14,40 | ✅ |
| banheiro | 6,00 | 6,00 | 36,00 | 24,00 | 36,00 | 24,00 | ✅ |
| varanda | 3,00 | 8,00 | 24,00 | 22,00 | 24,00 | 22,00 | ✅ |
| dormitório | 3,00 | 4,00 | 12,00 | 14,00 | 12,00 | 14,00 | ✅ |
| banheiro | 3,00 | 4,00 | 12,00 | 14,00 | 12,00 | 14,00 | ✅ |
| área-externa (Quintal) | 8,00 | 10,00 | 80,00 | 36,00 | 80,00 | 36,00 | ✅ |
| cozinha | 6,00 | 6,00 | 36,00 | 24,00 | 36,00 | 24,00 | ✅ |
| área-externa (Garagem) | 10,00 | 6,00 | 60,00 | 32,00 | 60,00 | 32,00 | ✅ |

**Conclusão:** Não há erros de cálculo dimensional. O sistema aplica corretamente as fórmulas retangulares A = L×C e P = 2(L+C).

---

### 3.2 Tomadas em Banheiros — Restrição Correta

Ambos os banheiros apresentam apenas **1 tomada (TUG)** cada. Isso está alinhado com a NBR 5410:2004, que restringe a instalação de TUG em banheiros à **Zona 3** (ou fora das zonas de risco), sendo proibido nas Zonas 0, 1 e 2. A limitação a 1 ponto é uma abordagem conservadora e segura.

### 3.3 Cozinha com TUEs Individualizados — Correto

A cozinha apresenta separação correta entre circuitos TUE para equipamentos individuais:

| Equipamento | Carga (VA) | Tipo |
|---|---|---|
| Exaustor | 1.250 | TUE |
| Forno micro-ondas | 2.250 | TUE |
| Forno elétrico | 2.800 | TUE |

Esta abordagem está em conformidade com o item 9.4.1.2 da NBR 5410, que exige circuitos dedicados para equipamentos de uso específico com potência relevante.

### 3.4 Rastreabilidade por ID e Versão

O sistema mantém rastreabilidade por ID único e versionamento por dependência (ex: v9 para o banheiro com mais iterações). Isso suporta o princípio de "rastreabilidade preservada" declarado no subtítulo da seção.

### 3.5 Sinalização [VERIFICAR] — Comportamento Adequado

O sistema reconhece a natureza provisória dos valores calculados automaticamente, sinalizando [VERIFICAR] nos campos de iluminação e tomadas. Isso indica que os valores são estimativas normativas automáticas que precisam de confirmação em campo por engenheiro responsável — comportamento correto e metodologicamente sólido.

---

## 4. Gaps e Não-Conformidades Potenciais

### 4.1 🔴 CRÍTICO — Número Mínimo de Tomadas (TUG) Subdimensionado

**Referência normativa:** NBR 5410:2004, item 9.4.1.1.1

Para ambientes de uso contínuo (sala, dormitório, escritório etc.) com área superior a 10 m², a norma estabelece:

> **n_min = 3 + ⌈(A − 10) / 5⌉**
>
> Onde: A = área do ambiente em m², ⌈x⌉ = teto (arredondamento para cima)

Para áreas menores:
- Até 6 m²: mínimo 1 TUG
- De 6 m² a 10 m²: mínimo 2 TUG
- Acima de 10 m²: aplicar fórmula acima

#### Comparativo Sistema vs. NBR 5410

| Dependência | Área (m²) | Cálculo NBR 5410 | Mínimo NBR | Sistema | Delta | Situação |
|---|---|---|---|---|---|---|
| sala | 36 | 3 + ⌈(36−10)/5⌉ = 3 + ⌈5,2⌉ = 3+6 | **9 TUG** | 5 | **−4** | 🔴 Não conforme |
| dormitório | 24 | 3 + ⌈(24−10)/5⌉ = 3 + ⌈2,8⌉ = 3+3 | **6 TUG** | 4 | **−2** | 🔴 Não conforme |
| dormitório | 16 | 3 + ⌈(16−10)/5⌉ = 3 + ⌈1,2⌉ = 3+2 | **5 TUG** | 4 | **−1** | ⚠️ Abaixo mínimo |
| dormitório | 12 | 3 + ⌈(12−10)/5⌉ = 3 + ⌈0,4⌉ = 3+1 | **4 TUG** | 3 | **−1** | ⚠️ Abaixo mínimo |
| hall-corredor | 7,20 | Área entre 6 e 10 m² | **2 TUG** | 3 | +1 | ✅ Acima mínimo |
| varanda | 24 | Área externa — regras específicas | A verificar | 5 | — | 🟡 Verificar |
| banheiro (36m²) | 36 | Regras especiais (banheiro) | 1 TUG | 1 | 0 | ✅ Conforme |
| banheiro (12m²) | 12 | Regras especiais (banheiro) | 1 TUG | 1 | 0 | ✅ Conforme |

**Impacto:** A sala apresenta o deficit mais crítico (−4 TUG). Em projeto executivo, isso resultaria em fiação subdimensionada e necessidade de extensões com benjamins/filtros, criando risco de sobrecarga e incêndio.

---

### 4.2 🔴 CRÍTICO — Ausência de Classificação de Zonas em Banheiros

**Referência normativa:** NBR 5410:2004, Seção 7.1 — *Localidades de banho e duchas*

A norma exige a classificação dos banheiros em zonas de risco com base nas distâncias do chuveiro/banheira:

| Zona | Definição | Grau de Proteção Mínimo | Equipamentos Permitidos |
|---|---|---|---|
| **Zona 0** | Interior da banheira ou box do chuveiro | IPX7 | Apenas equipamentos SELV ≤ 12V CA |
| **Zona 1** | Acima da zona 0, até 2,25 m de altura | IPX4 | Aparelhos elétricos específicos (aquecedor imersão, etc.) |
| **Zona 2** | Extensão de 0,60 m além dos limites da Zona 1 | IPX4 | Aparelhos elétricos com proteção adequada |
| **Zona 3** | Fora das zonas acima | IPX1 mínimo | TUG permitida (tomadas com proteção) |

**Gaps identificados no sistema:**

- Não há campo para classificação de zonas por banheiro
- A localização da tomada (600 VA) não é validada contra a zona em que seria instalada
- Não há referência ao grau de proteção (IP) exigido para os equipamentos de iluminação
- O banheiro maior (36 m²) sem chuveiro declarado não permite validar as zonas

**Consequência:** Sem a classificação de zonas, o sistema não pode garantir que equipamentos elétricos serão instalados em locais seguros nos banheiros, criando risco de choque elétrico.

---

### 4.3 🔴 CRÍTICO — Ausência de Classificação de Zonas para Piscina

**Referência normativa:** NBR 5410:2004, Seção 7.2 — *Piscinas e fontes ornamentais*

A norma estabelece zonas para instalações em piscinas:

| Zona | Definição | Tensão Máxima | Grau de Proteção |
|---|---|---|---|
| **Zona A** | Interior da piscina (água) | SELV ≤ 12V CA / ≤ 30V CC | IPX8 |
| **Zona B** | Extensão de 2 m além da borda da piscina | Tensão normal com DR | IPX4 |
| **Zona C** | Extensão adicional de 1,5 m além da Zona B | Tensão normal | IPX2 |

**Cargas declaradas na área-externa (Quintal) relacionadas à piscina:**

| Carga | Potência (VA) | Classificação no Sistema | Zona Provável |
|---|---|---|---|
| Motor de piscina | 3.000 | TUE | Zona B ou C (fora da água) |
| Bomba de piscina | 4.000 | Outra | Zona B ou C (fora da água) |
| Holofote (5 un.) | 500 (total) | Iluminação | Zona A se submerso |

**Gaps críticos:**

1. **Nenhuma zona de piscina é documentada** no sistema — o projeto não valida a conformidade dos equipamentos com as restrições por zona
2. **Holofotes de 100 VA cada:** se instalados submersos (Zona A), devem operar em SELV ≤ 12V CA. O sistema não indica tensão de operação dos holofotes
3. **Equalização de potencial bônus (bonding):** a NBR 5410 exige ligação equipotencial de todas as partes condutoras acessíveis na área da piscina (grades, escadas, borda metálica). Não há referência a isso no sistema
4. **DR obrigatório** para todos os circuitos das Zonas B e C — não declarado

---

### 4.4 🟡 IMPORTANTE — Proteção DR Não Representada

**Referência normativa:** NBR 5410:2004, item 9.5.2

A norma exige proteção por **Dispositivo Diferencial-Residual (DR)** com IDR ≤ 30 mA para:

| Tipo de circuito | DR Obrigatório? |
|---|---|
| Banheiros (todos os circuitos) | ✅ Sim |
| Áreas externas (varanda, quintal, garagem) | ✅ Sim |
| Cozinha (área molhada) | ✅ Sim |
| Piscina (Zonas B e C) | ✅ Sim |
| Dormitórios | Recomendado (não obrigatório por norma básica) |
| Sala | Recomendado |

**Gap:** O sistema não apresenta campo indicando se os circuitos das dependências estão associados a DR no QDC (Quadro de Distribuição de Circuitos). Esta informação deveria ser rastreável na seção de dependências ou vinculada ao diagrama unifilar.

---

### 4.5 🟡 IMPORTANTE — Grau de Proteção IP Ausente para Áreas Externas

**Referência normativa:** NBR 5410:2004, Seção 5.1 — Influências externas (código AD — presença de água)

| Tipo de área | IP Mínimo para Tomadas | IP Mínimo para Luminárias |
|---|---|---|
| Varanda coberta | IP44 | IP44 |
| Área externa descoberta | IP55 | IP55 |
| Garagem coberta | IP44 | IP22 (interior) |
| Banheiro — Zona 1 | IPX4 | IPX4 |
| Banheiro — Zona 2 | IPX4 | IPX4 |

**Gap:** As dependências de tipo "área-externa" e "varanda" não apresentam classificação de grau de proteção IP. O sistema deveria inferir ou permitir declarar o IP exigido com base no tipo de ambiente.

---

### 4.6 🟡 IMPORTANTE — Ausência de Classificação de Influências Externas (IEs)

**Referência normativa:** NBR 5410:2004, Seção 5.1

A norma classifica cada ambiente por um conjunto de **Influências Externas (IEs)** que determinam as exigências para os equipamentos elétricos instalados:

| Código | Parâmetro | Exemplos de Classes |
|---|---|---|
| AA | Temperatura ambiente | AA1 (−60°C a +5°C) … AA8 (+60°C a +85°C) |
| AB | Umidade relativa | AB1 (3–100%) … AB8 (condensação frequente) |
| AC | Altitude | AC1 (≤2.000 m) / AC2 (>2.000 m) |
| AD | Presença de água | AD1 (desprezível) … AD8 (submersão) |
| AE | Presença de corpos sólidos estranhos | AE1 (desprezível) … AE6 (pó em suspensão) |
| AF | Presença de substâncias corrosivas | AF1 (desprezível) … AF3 (forte) |
| AG | Impactos mecânicos | AG1 (leve) … AG3 (severo) |
| BA | Capacitação das pessoas | BA1 (ordinário) … BA5 (impedidos) |
| BB | Resistência elétrica do corpo humano | BB1 (normal) … BB3 (imerso) |
| BE | Natureza dos materiais tratados | BE1 (sem risco) … BE3 (explosivo) |

**Gap:** O sistema utiliza nomes descritivos (sala, banheiro, área-externa) mas não vincula códigos formais de IE a cada dependência. A classificação formal é necessária para:

- Seleção de equipamentos com IP compatível
- Dimensionamento de cabos com isolamento adequado
- Definição do tipo de eletroduto (rígido, flexível, blindado)
- Conformidade com auditorias e laudos de AVCB/CLCB

---

## 5. Incongruências Internas do Sistema

### 5.1 🔴 Banheiro 6×6 (36 m²) sem Cargas de Chuveiro

**Observação:** O banheiro maior (36 m²) não apresenta nenhuma carga adicional, enquanto o banheiro menor (12 m²) possui:
- Chuveiro elétrico: 7.500 VA
- Banheira de hidromassagem: 1.650 VA

**Análise:**

| Cenário | Plausibilidade | Impacto |
|---|---|---|
| Suite com banheiro seco (lavabo apenas) | Baixa — 36m² é incompatível com lavabo | Omissão crítica se real |
| Banheiro com chuveiro não declarado no sistema | Alta | TUE de 7.500 VA não dimensionado |
| Banheiro com aquecimento central (sem elétrico) | Possível | Aceitável, mas deve ser documentado |

**Recomendação:** O sistema deveria sinalizar [VERIFICAR] automaticamente para banheiros sem TUE de chuveiro ou aquecimento declarado, especialmente em áreas > 15 m².

---

### 5.2 🟡 Bomba de Piscina Classificada como "Outra" — Inconsistência com Motor de Piscina

| Carga | Potência (VA) | Classificação no Sistema | Classificação Correta (NBR 5410) |
|---|---|---|---|
| Motor de piscina | 3.000 | TUE | TUE ✅ |
| Bomba de piscina | 4.000 | **Outra** | **TUE** ⚠️ |

Ambos são cargas motorizadas de uso exclusivo vinculadas à piscina. A bomba de piscina, com 4.000 VA, requer circuito dedicado e, portanto, deve ser classificada como TUE. A classificação como "Outra" pode:

- Subrepresentar a exigência de circuito exclusivo
- Excluir a carga do cálculo de demanda para TUEs
- Gerar inconsistência no diagrama unifilar gerado

---

### 5.3 🟡 Portão Eletrônico Classificado como "Outra"

| Carga | Potência (VA) | Classificação no Sistema | Classificação Correta |
|---|---|---|---|
| Portão eletrônico | 1.200 | **Outra** | **TUE** ⚠️ |

O portão eletrônico é uma carga motora de acionamento dedicado. Deve ser TUE com circuito próprio. A classificação como "Outra" pode resultar no sub-dimensionamento do circuito de alimentação.

---

### 5.4 🟡 Cozinha sem Fogão/Cooktop Elétrico Declarado

A cozinha apresenta exaustor, forno micro-ondas e forno elétrico como TUEs, mas **nenhum fogão ou cooktop** é declarado.

**Cenários possíveis:**

| Cenário | Impacto |
|---|---|
| Fogão a gás (sem circuito elétrico dedicado) | Aceitável — apenas ponto de ignição eletrônica (~30 W) |
| Cooktop elétrico não declarado | Deficit de circuito TUE com 5.000–8.500 VA, fio 6 mm², disjuntor 40A |
| Fogão de indução não declarado | Mesmo impacto do cooktop elétrico, geralmente 6.000–7.200 VA |

**Recomendação:** O sistema deveria alertar quando uma cozinha não possui fogão/cooktop declarado, solicitando confirmação sobre o tipo de equipamento (gás ou elétrico).

---

### 5.5 🟡 Inconsistência no Número de TUGs na Cozinha

A cozinha 36 m² declara **7 tomadas × 2.200 VA** = 15.400 VA em TUG.

Aplicando a fórmula geral: n_min = 3 + ⌈(36−10)/5⌉ = **9 TUG mínimas**

O sistema declara 7 TUGs na cozinha, porém com VA muito superior (2.200 VA cada) ao de outros ambientes. Isso pode indicar que a cozinha tem circuitos dimensionados para cargas maiores (bancadas com equipamentos), mas a quantidade pode ser insuficiente conforme o layout real (uma tomada por seção de bancada ≥ 1,8 m).

---

## 6. Análise de Coeficiente de Iluminação

### 6.1 Padrão Identificado

Análise reversa do coeficiente de iluminação utilizado pelo sistema:

| Dependência | Área (m²) | VA Iluminação | VA/m² |
|---|---|---|---|
| hall-corredor | 7,20 | 100 | 13,9 |
| dormitório | 12,00 | 160 | 13,3 |
| dormitório | 16,00 | 220 | 13,75 |
| dormitório | 24,00 | 340 | 14,2 |
| sala / cozinha / banheiro (36m²) | 36,00 | 520 | 14,4 |
| área-externa (Garagem) | 60,00 | 880 | 14,7 |
| área-externa (Quintal) | 80,00 | 1.180 | 14,75 |

**Coeficiente médio observado: ~14,0–14,75 VA/m²**

### 6.2 Comparativo com Referências

| Referência | Coeficiente |
|---|---|
| Sistema proposto (calculado) | ~14 VA/m² |
| NBR 5410 — carga mínima para demanda da instalação (residencial, primeiros 50 m² da unidade) | 60 VA/m² |
| Prática de projeto — instalações residenciais típicas | 30–60 VA/m² por ambiente |
| ABNT NBR ISO/CIE 8995-1 (iluminância recomendada) — sala de estar: 300 lux típico | ~40–80 VA/m² (depende da tecnologia de lâmpada) |

### 6.3 Interpretação

O coeficiente de ~14 VA/m² indica que o sistema calcula a **carga mínima de um ponto de circuito de iluminação**, não a **carga de projeto real do ambiente**. Esta é uma diferença importante:

- A **carga de ponto mínimo** serve para dimensionamento normativo do circuito (bitola do condutor, disjuntor)
- A **carga de projeto real** serve para dimensionamento da entrada de serviço e do transformador

**Risco:** Se os 14 VA/m² forem usados como carga de projeto para o cálculo do QDC e da entrada de energia, haverá subdimensionamento significativo da instalação geral.

**Recomendação:** O sistema deve deixar explícito que os valores de iluminação na seção "Dependências" representam cargas mínimas normativas de ponto, distintas das cargas de projeto para dimensionamento da entrada.

---

## 7. Análise Geométrica das Dependências

### 7.1 Consistência das Fórmulas

O sistema aplica corretamente:
- Área retangular: **A = L × C**
- Perímetro retangular: **P = 2(L + C)**
- Fórmula exibida na interface: "Retângulo · A = L × C · P = 2(L+C)"

Todos os 11 ambientes analisados têm cálculos geométricos corretos (ver tabela 1.1).

### 7.2 Observações sobre Dimensões

| Dependência | Observação |
|---|---|
| Banheiro 6×6 (36 m²) | Dimensão atípica para banheiro residencial. Possível suíte master ou erro de cadastro de tipo |
| Hall-corredor 6×1,20 (7,2 m²) | Dimensão plausível para corredor de distribuição |
| Área-externa Quintal 8×10 (80 m²) | Quintal de dimensão razoável para residência padrão médio-alto |
| Área-externa Garagem 10×6 (60 m²) | Garagem para 2–3 veículos — compatível com residência de alto padrão |

---

## 8. Resumo dos Gaps por Criticidade

### 8.1 Mapa de Criticidade

```
🔴 CRÍTICO      — Não conformidade com NBR 5410, risco de segurança ou subdimensionamento grave
🟡 IMPORTANTE   — Gap normativo ou inconsistência que impacta a qualidade do projeto
🟢 OBSERVAÇÃO   — Ponto de atenção sem impacto direto de segurança
```

### 8.2 Tabela Consolidada

| # | Gap | Criticidade | Dependências Afetadas | Referência NBR 5410 |
|---|---|---|---|---|
| B1 | TUG subdimensionado (sala −4, dorm. −1 a −2) | 🔴 CRÍTICO | sala, dormitórios | Item 9.4.1.1.1 |
| B2 | Zonas de banheiro não classificadas | 🔴 CRÍTICO | banheiros (2 unid.) | Seção 7.1 |
| B3 | Zonas de piscina não classificadas + sem equalização de potencial | 🔴 CRÍTICO | área-externa Quintal | Seção 7.2 |
| C1 | Banheiro 36m² sem TUE de chuveiro — possível omissão crítica | 🔴 CRÍTICO | banheiro (6×6) | Item 9.4.1.2 |
| B4 | Proteção DR não representada nos circuitos | 🟡 IMPORTANTE | banheiros, cozinha, externas | Item 9.5.2 |
| B5 | Grau de proteção IP ausente para áreas externas | 🟡 IMPORTANTE | varanda, quintai, garagem | Seção 5.1 (AD) |
| B6 | Classificação de influências externas (IEs) ausente | 🟡 IMPORTANTE | todos os ambientes | Seção 5.1 |
| C2 | Bomba de piscina como "Outra" em vez de TUE | 🟡 IMPORTANTE | área-externa Quintal | Item 9.4.1.2 |
| C3 | Portão eletrônico como "Outra" em vez de TUE | 🟡 IMPORTANTE | área-externa Garagem | Item 9.4.1.2 |
| C4 | Cozinha sem fogão/cooktop elétrico declarado | 🟡 IMPORTANTE | cozinha | Item 9.4.1.2 |
| C5 | Inconsistência de TUG na cozinha (7 < 9 mínimo NBR) | 🟡 IMPORTANTE | cozinha | Item 9.4.1.1.1 |
| A6 | Coeficiente de iluminação ~14 VA/m² — insuficiente como demanda de projeto | 🟢 OBSERVAÇÃO | todos | Tabela demanda mínima |

### 8.3 Contagem por Criticidade

| Criticidade | Quantidade |
|---|---|
| 🔴 CRÍTICO | 4 |
| 🟡 IMPORTANTE | 7 |
| 🟢 OBSERVAÇÃO | 1 |
| **Total** | **12** |

---

## 9. Recomendações para o Sistema

### 9.1 Correções no Algoritmo de Cálculo

**R1 — Revisar cálculo de TUG mínimo**

Atualizar o algoritmo para aplicar corretamente a fórmula da NBR 5410:

```
Para ambientes com A ≤ 6 m²:     n_min = 1
Para ambientes com 6 < A ≤ 10 m²: n_min = 2
Para ambientes com A > 10 m²:     n_min = 3 + ceil((A - 10) / 5)

Exceções:
  - Banheiro: n_min = 1 (com restrições de zona)
  - Cozinha:  n_min conforme layout de bancadas + TUEs dedicados
  - Áreas externas: verificar norma específica (IP, DR, zona)
```

**R2 — Separar carga de ponto de iluminação da carga de projeto**

O campo "Iluminação" deve exibir dois valores:
- `Carga mínima normativa (VA)` — para dimensionamento do circuito
- `Carga de projeto estimada (VA)` — para dimensionamento do QDC e entrada

### 9.2 Novos Campos a Adicionar

| Campo | Tipo | Obrigatoriedade | Dependências que se Aplicam |
|---|---|---|---|
| Classificação de zona (banho) | Seletor (Zona 0/1/2/3) | Obrigatório para banheiros | Banheiros |
| Classificação de zona (piscina) | Seletor (Zona A/B/C) | Obrigatório quando houver piscina | Áreas externas com piscina |
| Grau de proteção IP declarado | Campo IP (ex: IP44) | Obrigatório para externas/banheiros | Varanda, quintal, garagem, banheiros |
| Proteção DR vinculada | Booleano + IDR (mA) | Obrigatório para ambientes molhados/externos | Banheiros, cozinha, externas |
| Influências externas (IE) | Campos por código (AA, AB, AD...) | Recomendado | Todos |
| Equalização de potencial | Booleano | Obrigatório para piscinas | Áreas com piscina |

### 9.3 Validações e Alertas

**R3 — Validações automáticas a implementar:**

1. **Alerta de TUG insuficiente:** quando o número de tomadas declaradas for inferior ao mínimo calculado pela fórmula NBR, sinalizar com badge vermelho e exibir o valor mínimo esperado
2. **Alerta de chuveiro ausente:** para banheiros com área > 5 m² sem TUE de chuveiro ou aquecimento declarado
3. **Alerta de fogão/cooktop ausente:** para cozinhas sem equipamento de cocção declarado
4. **Classificação automática de TUE:** sugerir TUE para cargas motorizadas (bombas, portões, compressores) ao serem adicionadas como "Outra"
5. **Obrigatoriedade de DR:** bloquear finalização de cálculo para banheiros, cozinhas e áreas externas sem DR declarado no QDC

### 9.4 Melhorias de Experiência

**R4 — Interface:**

- Exibir o mínimo NBR de TUGs ao lado do valor calculado (ex: "5 [VERIFICAR] | Mínimo NBR: 9")
- Adicionar tooltip nos campos [VERIFICAR] explicando o critério normativo usado no cálculo
- Para banheiros, adicionar visualização esquemática das zonas 0/1/2 com as dimensões do ambiente
- Para áreas com piscina, adicionar seção específica de "Instalações de piscina" com campos normativos

---

## 10. Referências Normativas

| Norma | Título | Relevância |
|---|---|---|
| **ABNT NBR 5410:2004** | Instalações elétricas de baixa tensão | Norma principal de referência |
| **ABNT NBR IEC 60364-7-701** | Instalações em localidades de banho e ducha | Zonas em banheiros |
| **ABNT NBR IEC 60364-7-702** | Piscinas e fontes ornamentais | Zonas em piscinas |
| **ABNT NBR ISO/CIE 8995-1** | Iluminação de ambientes de trabalho interiores | Níveis de iluminância recomendados |
| **ABNT NBR 5419** | Proteção contra descargas atmosféricas | Para áreas externas |
| **IEC 60529** | Graus de proteção IP | Classificação IP de equipamentos |

---

## Apêndice A — Fórmulas NBR 5410 para Cálculo de TUGs

### Ambientes de uso geral (sala, dormitório, escritório, etc.)

```
Se A ≤ 6 m²:      n_min = 1 TUG
Se 6 < A ≤ 10 m²: n_min = 2 TUG
Se A > 10 m²:      n_min = 3 + ceil((A - 10) / 5) TUG
```

### Cozinha

```
n_min_TUG = ceil(comprimento_bancada / 1,8) + 1  (mínimo 3 TUG)
n_TUE = 1 por equipamento de uso específico (fogão, forno, lavadora, etc.)
```

### Banheiro

```
n_min_TUG = 1 (somente em Zona 3 ou fora das zonas)
TUE obrigatório: chuveiro elétrico (se houver)
TUE recomendado: banheira de hidromassagem
```

### Área externa

```
n_min_TUG = conforme uso declarado
IP mínimo: IP44 (coberta) / IP55 (descoberta)
DR obrigatório: IDR ≤ 30 mA
```

---

## Apêndice B — Cálculo de Demanda Mínima de Iluminação

A diferença entre a carga mínima de ponto e a demanda de projeto é fundamental:

| Conceito | Definição | Uso |
|---|---|---|
| Carga de ponto mínima (~14 VA/m²) | Mínimo para dimensionamento do circuito de iluminação | Bitola do condutor, disjuntor do circuito |
| Demanda mínima NBR (60 VA/m²) | Carga mínima para demanda total da unidade | Dimensionamento do ramal de entrada, medição, transformador |
| Demanda de projeto real | Carga efetiva instalada prevista | Projeto executivo final |

Para uma unidade residencial de ~300 m² como a analisada:
- **Cálculo pelo sistema (~14 VA/m²):** 300 × 14 ≈ 4.200 VA de iluminação
- **Mínimo NBR (60 VA/m²):** primeiros 50 m² × 60 = 3.000 VA + restante (250 m²) × 25 VA = 6.250 VA → **total ≈ 9.250 VA**

Esta diferença de ~2×, se propagada para o projeto completo, pode resultar em subdimensionamento do ramal de entrada.

---

*Documento gerado por: Atlas (Decoder) — AIOX Business Analyst*  
*Data de emissão: 20/06/2026*  
*Status: Rascunho para revisão técnica pelo engenheiro responsável*  
*Classificação: Análise técnica — não substitui laudo de engenheiro habilitado (CREA)*

---

*— Atlas, investigando a verdade 🔎*
