# Tutorial Completo — Sistemática de Quantidade TUG e Iluminação (NBR 5410)

**Objetivo:** Explicar passo a passo como calcular e gerenciar a quantidade de Tomadas de Uso Geral (TUG) e Pontos de Iluminação conforme a NBR 5410, com suporte a Automático/Manual.

**Público-alvo:** Desenvolvedores, engenheiros e técnicos de projeto elétrico.

**Data:** 2026-07-05  
**Versão:** 1.0

---

## 📋 Índice Rápido

1. [Introdução: O que é Quantidade de TUG?](#1-introdução-o-que-é-quantidade-de-tug)
2. [As 4 Categorias de Dependência (CAT-A, B, C)](#2-as-4-categorias-de-dependência)
3. [Passo a Passo: Calcular Quantidade de TUG](#3-passo-a-passo-calcular-quantidade-de-tug)
4. [Entendendo as Fórmulas Normativas](#4-entendendo-as-fórmulas-normativas)
5. [Pontos de Iluminação: Nova Sistemática](#5-pontos-de-iluminação-nova-sistemática)
6. [Origem Automática vs. Manual: Controle de Edições](#6-origem-automática-vs-manual)
7. [Exemplo Prático Completo](#7-exemplo-prático-completo)
8. [Implementação Técnica (TypeScript/JavaScript)](#8-implementação-técnica)
9. [FAQ — Dúvidas Comuns](#9-faq--dúvidas-comuns)

---

## 1. Introdução: O que é Quantidade de TUG?

### Conceito-chave

Uma **Tomada de Uso Geral (TUG)** é um ponto de tomada elétrica em uma dependência (cômodo) destinado ao uso geral da edificação. A NBR 5410:2004 define regras específicas para calcular o número mínimo de tomadas que cada tipo de cômodo deve ter.

**Por que é importante?**
- Garante distribuição uniforme de energia elétrica
- Atende normas de segurança elétrica
- Reduz risco de sobrecarga
- Melhora qualidade e confiabilidade da instalação

### Dados de entrada obrigatórios

Para calcular a quantidade de TUG, você precisa de:

| Dado | O que é | Exemplo |
|------|---------|---------|
| **Largura (m)** | Dimensão horizontal do cômodo | 5 metros |
| **Comprimento (m)** | Dimensão vertical do cômodo | 4 metros |
| **Perímetro excluído (m)** | Parede(s) onde não há tomadas | 0 metros (normal) |
| **Tipo de dependência** | Cozinha, banheiro, sala, etc. | "sala" |

### Saída esperada

Após o cálculo, você terá:

```
Quantidade: 4 tomadas [A]
Carga total: 400 VA
Fórmula aplicada: F-03
Origem: AUTOMATICO
```

---

## 2. As 4 Categorias de Dependência

A NBR 5410 agrupa os cômodos em **3 categorias principais** (CAT-A, CAT-B, CAT-C), cada uma com regra de cálculo diferente:

### CAT-A: Salas, Dormitórios, Hall

**Características:**
- Cômodos de uso geral
- Baixa demanda de energia
- Sem picos de consumo previsíveis

**Fórmula:** `quantidade = ceil(Perímetro / 5)` (mínimo 1)

**Carga por tomada:** 100 VA

**Exemplos:** Sala de estar, sala de jantar, dormitório, corredor, hall

**Exemplo numérico:**
```
Sala de 5m × 4m
├─ Perímetro = 2(5+4) = 18m
├─ Quantidade = ceil(18/5) = ceil(3.6) = 4 tomadas
└─ Carga total = 4 × 100 VA = 400 VA
```

---

### CAT-B: Cozinha, Copa, Banheiro, Área de Serviço

**Características:**
- Cômodos com maior demanda de energia
- Equipamentos elétricos de alta potência
- Dois subcasos: normal e banheiro

#### **CAT-B Normal (Cozinha, Copa, Área de Serviço)**

**Fórmula:** `quantidade = ceil(Perímetro / 3.5)`

**Carga especial:**
- Primeiras 3 tomadas: 600 VA cada
- Demais tomadas: 100 VA cada

**Exemplo:**
```
Cozinha de 4m × 3m
├─ Perímetro = 2(4+3) = 14m
├─ Quantidade = ceil(14/3.5) = ceil(4) = 4 tomadas
├─ Carga = (3 × 600 VA) + (1 × 100 VA) = 1.900 VA
└─ Carga média = 1.900 / 4 = 475 VA/tomada
```

#### **CAT-B Especial (Banheiro)**

**Fórmula:** `quantidade = 1` (mínimo)

**Carga:** 600 VA (fixa)

**Observação:** Banheiro sempre tem apenas 1 tomada, independente do tamanho.

**Exemplo:**
```
Banheiro de 2m × 1.5m
├─ Quantidade = 1 tomada (obrigatório)
└─ Carga = 1 × 600 VA = 600 VA
```

---

### CAT-C: Varanda, Área Externa

**Características:**
- Espaços externos
- Clima úmido ou salino
- Normas de proteção mais rígidas

**Fórmula:**
```
Se Área > 6 m²:
  quantidade = ceil(Perímetro / 5)
Senão:
  quantidade = 1
```

**Carga por tomada:** 100 VA

**Exemplo:**
```
Varanda de 3m × 2m (Área = 6 m²)
├─ Área = 6 m² (não é > 6)
├─ Quantidade = 1 tomada
└─ Carga = 1 × 100 VA = 100 VA

Varanda de 4m × 2m (Área = 8 m²)
├─ Área = 8 m² (é > 6)
├─ Perímetro = 2(4+2) = 12m
├─ Quantidade = ceil(12/5) = 3 tomadas
└─ Carga = 3 × 100 VA = 300 VA
```

---

## 3. Passo a Passo: Calcular Quantidade de TUG

### Fluxograma Visual

```
┌─────────────────────────────────────┐
│ ENTRADA: tipo, L, C, P_excluído     │
└──────────────┬──────────────────────┘
               ↓
        ┌─ Passo 1 ─┐
        │ Calcular  │
        │ Área (A)  │
        └─────┬─────┘
              ↓
          A = L × C
              ↓
        ┌─ Passo 2 ─┐
        │ Calcular  │
        │ Perímetro │
        │ (P)       │
        └─────┬─────┘
              ↓
     P = 2(L + C) - P_exc
              ↓
        ┌─ Passo 3 ─┐
        │ Mapear    │
        │ tipo →    │
        │ categoria │
        └─────┬─────┘
              ↓
    ┌────────┴────────┐
    ↓                 ↓
  CAT-B?          CAT-A/C?
    │ SIM             │
    ├─────┐           │
    ↓     ↓           ↓
 BANHEIRO RESTO   CAT-A/C
    │      │        │
    │    qtd=        │
    │  ceil(P/3.5)  qtd=
    │      │        ceil(P/5)
    │      └────┬────┘
    ↓           ↓
  qtd=1     ┌─ Passo 4 ─┐
            │ Aplicar   │
            │ mínimo    │
            │ normativo │
            └─────┬─────┘
                  ↓
              qtd ≥ 1?
                  │
              ┌───┴────┐
              ↓        ↓
             SIM      NÃO
              │        │
              │    qtd = 1
              │        │
              └────┬───┘
                   ↓
         ┌─ Passo 5 ─┐
         │ Calcular  │
         │ carga     │
         │ total     │
         └─────┬─────┘
               ↓
        carga = qtd × VA
               ↓
         ┌─ Passo 6 ─┐
         │ SAÍDA:    │
         │ {qtd,     │
         │  carga,   │
         │  origem}  │
         └───────────┘
```

### Passo 1: Calcular Área

A **área (A)** é a multiplicação entre largura e comprimento do cômodo.

```
Fórmula: A = Largura × Comprimento

Exemplo:
├─ Sala: L = 5m, C = 4m
└─ A = 5 × 4 = 20 m²
```

**Nota:** A área é usada principalmente para:
- CAT-C (condicional, se A > 6 m²)
- Iluminação (cálculo de quantidade de pontos)

---

### Passo 2: Calcular Perímetro

O **perímetro (P)** é o comprimento total das paredes úteis onde as tomadas serão instaladas.

```
Fórmula: P = 2 × (Largura + Comprimento) - Perímetro_excluído

Onde:
├─ Largura: dimensão horizontal
├─ Comprimento: dimensão vertical
└─ Perímetro_excluído: parede(s) onde não há tomadas
                       (ex: parede com porta grande, varanda, etc.)
                       Default: 0 (nenhuma parede excluída)

Exemplo:
├─ L = 5m, C = 4m, P_exc = 0
└─ P = 2(5+4) - 0 = 18m

Exemplo com perímetro excluído:
├─ L = 5m, C = 4m, P_exc = 2m (parede com grande abertura)
└─ P = 2(5+4) - 2 = 16m
```

**Quando excluir perímetro?**
- Grandes portas (sala → varanda)
- Janelas que ocupam toda parede
- Área de abertura > 1m²
- Espaço ocupado por móveis fixos

---

### Passo 3: Mapear Tipo → Categoria

Cada tipo de dependência pertence a uma categoria. Use esta tabela:

| Tipo | Categoria | Motivo |
|------|-----------|--------|
| Sala | CAT-A | Uso geral, baixa demanda |
| Dormitório | CAT-A | Uso geral, baixa demanda |
| Hall/Corredor | CAT-A | Circulação, baixa demanda |
| Cozinha | CAT-B | Alta demanda de equipamentos |
| Copa | CAT-B | Próximo à cozinha, demanda média |
| Banheiro | CAT-B especial | Única tomada obrigatória |
| Área de Serviço | CAT-B | Alta demanda de equipamentos |
| Varanda | CAT-C | Condicional por área |
| Área Externa | CAT-C | Condicional por área |
| Garagem | CAT-A | Uso geral (sem combustível) |

---

### Passo 4: Aplicar Fórmula Normativa

De acordo com a categoria mapeada, aplique a fórmula correspondente:

| Categoria | Fórmula | Detalhes |
|-----------|---------|----------|
| **CAT-A** | `ceil(P / 5)` | 1 tomada a cada 5m de perímetro, mín. 1 |
| **CAT-B** (normal) | `ceil(P / 3.5)` | 1 tomada a cada 3.5m, mín. 1 |
| **CAT-B** (banheiro) | `1` | Sempre 1, independente de P |
| **CAT-C** | `A > 6 ? ceil(P/5) : 1` | Condicional pela área |

**O que significa "ceil"?**

`ceil` = **arredondar para cima** para o número inteiro mais próximo.

```
Exemplos:
├─ ceil(3.2) = 4
├─ ceil(3.6) = 4
├─ ceil(4.0) = 4
└─ ceil(4.1) = 5
```

---

### Passo 5: Aplicar Mínimo Normativo

Toda fórmula tem um **mínimo garantido**, que é sempre 1.

```
Regra: qtd_final = MAX(resultado_fórmula, mínimo_normativo)

Exemplo CAT-A (sala muito pequena):
├─ Área = 3m² (3m × 1m)
├─ Perímetro = 2(3+1) = 8m
├─ Fórmula: ceil(8/5) = ceil(1.6) = 2
├─ Mínimo normativo: 1
└─ Quantidade final = MAX(2, 1) = 2 ✓

Exemplo CAT-C (varanda pequena):
├─ Área = 5 m² (5m × 1m) — não > 6
├─ Fórmula: A ≤ 6 → 1
├─ Mínimo normativo: 1
└─ Quantidade final = MAX(1, 1) = 1 ✓
```

---

### Passo 6: Calcular Carga Total (em VA)

Cada tomada consome uma quantidade de energia em **Volt-Ampere (VA)**. Multiplique a quantidade pela carga unitária.

**Carga por categoria:**

| Categoria | Carga Unitária | Notas |
|-----------|---|---|
| CAT-A | 100 VA | Fixa |
| CAT-B (normal) | 600 VA (primeiras 3) + 100 VA (demais) | Misto |
| CAT-B (banheiro) | 600 VA | Fixa |
| CAT-C | 100 VA | Fixa |

**Cálculos de carga:**

```
CAT-A:
├─ Se qtd = 4
└─ Carga total = 4 × 100 = 400 VA

CAT-B normal (cozinha):
├─ Se qtd = 4
├─ Primeiras 3: 3 × 600 = 1.800 VA
├─ Restante (1): 1 × 100 = 100 VA
└─ Carga total = 1.800 + 100 = 1.900 VA

CAT-B banheiro:
├─ qtd = 1 (sempre)
└─ Carga total = 1 × 600 = 600 VA

CAT-C:
├─ Se qtd = 3
└─ Carga total = 3 × 100 = 300 VA
```

---

## 4. Entendendo as Fórmulas Normativas

Cada fórmula (F-03 a F-06) mapeia diretamente a um artigo da NBR 5410. Aqui explicamos cada uma:

### F-03: TUG em CAT-A

```
Fórmula: qtd = ceil(P / 5)
Mínimo: 1
Carga: 100 VA por tomada

Fonte: NBR 5410:2004, item 9.5.2.2.1.c

Interpretação:
├─ A cada 5 metros de perímetro, adicione 1 tomada
├─ Arredonde para cima
└─ Garanta mínimo 1 tomada

Casos de uso:
├─ Salas de estar
├─ Dormitórios
├─ Halls e corredores
└─ Garagens (sem combustível)
```

**Tabela de Referência Rápida (CAT-A):**

| Perímetro (m) | Quantidade |
|---|---|
| 1–5 | 1 |
| 5.1–10 | 2 |
| 10.1–15 | 3 |
| 15.1–20 | 4 |
| 20.1–25 | 5 |

---

### F-04a: TUG em CAT-B Normal

```
Fórmula: qtd = ceil(P / 3.5)
Mínimo: 1
Carga: 3×600 VA + resto×100 VA

Fonte: NBR 5410:2004, item 9.5.2.2.1.a

Interpretação:
├─ A cada 3.5 metros, adicione 1 tomada
├─ Arredonde para cima
├─ Primeiras 3 tomadas = 600 VA cada
└─ Tomadas a partir da 4ª = 100 VA cada

Casos de uso:
├─ Cozinha
├─ Copa
└─ Área de Serviço
```

**Tabela de Referência Rápida (CAT-B Normal):**

| Perímetro (m) | Quantidade | Carga Total |
|---|---|---|
| 1–3.5 | 1 | 600 VA |
| 3.6–7 | 2 | 1.200 VA |
| 7.1–10.5 | 3 | 1.800 VA |
| 10.6–14 | 4 | 1.900 VA |
| 14.1–17.5 | 5 | 2.000 VA |

---

### F-04b: TUG em CAT-B Banheiro (Especial)

```
Fórmula: qtd = 1
Mínimo: 1 (obrigatório)
Carga: 600 VA

Fonte: NBR 5410:2004, item 9.5.2.2.1.b

Interpretação:
├─ Banheiro SEMPRE tem 1 tomada
├─ Independente do tamanho/perímetro
└─ Não há negociação normativa

Razão técnica:
├─ Ambiente úmido restringe instalações
├─ Tomada deve estar em local específico
└─ Múltiplas tomadas aumentam risco
```

---

### F-06: TUG em CAT-C

```
Fórmula: 
  Se Área > 6 m²:
    qtd = ceil(P / 5)
  Senão:
    qtd = 1

Mínimo: 1
Carga: 100 VA por tomada

Fonte: NBR 5410:2004, item 9.5.2.2.1.d

Interpretação:
├─ CAT-C é condicional por ÁREA
├─ Pequenas áreas (≤6) = 1 tomada
├─ Grandes áreas (>6) = aplicar CAT-A
└─ Garante proteção em áreas pequenas

Casos de uso:
├─ Varanda
├─ Pátio
├─ Área externa
└─ Garagem (com combustível?)
```

**Tabela de Referência Rápida (CAT-C):**

| Área (m²) | Perímetro (m) | Quantidade |
|---|---|---|
| ≤6 | — | 1 |
| >6 | 1–5 | 1 |
| >6 | 5.1–10 | 2 |
| >6 | 10.1–15 | 3 |
| >6 | 15.1–20 | 4 |

---

## 5. Pontos de Iluminação: Nova Sistemática

### 5.1 Situação Anterior (Simples)

Antes, pontos de iluminação eram tratados de forma básica:
- Mínimo: 1 ponto por cômodo
- Carga: Fixa ou por fórmula

**Problema:** Sem rastreamento automático de origem ou quantidade dinâmica por área.

### 5.2 Nova Sistemática (Com Quantidade Dinâmica)

Agora aplicamos regras específicas conforme a **área do cômodo**.

#### **Regra 1: Mínimo Normativo (F-07)**

```
Fórmula: qtd_mínima = 1

Fonte: NBR 5410:2004, item 9.5.2.1.2

Interpretação:
└─ TODO cômodo tem pelo menos 1 ponto de luz (obrigatório)
```

#### **Regra 2: Aumento por Área (F-07-QTD) — NOVA**

```
Fórmula: 
  Se Área ≤ 6 m²:
    qtd = 1
  
  Se Área > 6 m²:
    qtd = 1 + floor((Área - 6) / 4)

Mínimo: 1
Máximo: Sem limite

Fonte: NBR 5410:2004, item 9.5.2.1.2 (interpretação prática)

Interpretação:
├─ Para cada 4 m² adicionais acima de 6 m²
├─ Adicione 1 ponto de luz extra
└─ Garante distribuição uniforme da iluminação
```

**O que significa "floor"?**

`floor` = **arredondar para baixo** para o número inteiro.

```
Exemplos:
├─ floor(3.2) = 3
├─ floor(3.9) = 3
└─ floor(4.0) = 4
```

#### **Regra 3: Carga Total de Iluminação (F-08) — Já Implementada**

```
Fórmula:
  Se Área ≤ 6 m²:
    carga_total = 100 VA
  
  Se Área > 6 m²:
    carga_total = 100 + 60 × floor((Área - 6) / 4) VA

Fonte: NBR 5410:2004, item 9.5.2.1.2
```

### 5.3 Exemplos Práticos de Iluminação

#### **Exemplo 1: Sala Pequena (4 m²)**

```
Entrada:
├─ Tipo: sala
├─ Largura: 2m
└─ Comprimento: 2m

Cálculos:
├─ Área = 2 × 2 = 4 m²
├─ Área ≤ 6? SIM
├─ Quantidade (F-07-QTD) = 1 ponto
├─ Carga total (F-08) = 100 VA
└─ Carga por ponto = 100 / 1 = 100 VA
```

#### **Exemplo 2: Sala Média (20 m²)**

```
Entrada:
├─ Tipo: sala
├─ Largura: 5m
└─ Comprimento: 4m

Cálculos:
├─ Área = 5 × 4 = 20 m²
├─ Área > 6? SIM
├─ Acima de 6 m²: 20 - 6 = 14 m²
├─ Múltiplos de 4: floor(14 / 4) = floor(3.5) = 3
├─ Quantidade (F-07-QTD) = 1 + 3 = 4 pontos
├─ Carga total (F-08) = 100 + 60 × 3 = 280 VA
└─ Carga por ponto = 280 / 4 = 70 VA
```

#### **Exemplo 3: Sala Grande (50 m²)**

```
Entrada:
├─ Tipo: sala
├─ Largura: 10m
└─ Comprimento: 5m

Cálculos:
├─ Área = 10 × 5 = 50 m²
├─ Área > 6? SIM
├─ Acima de 6 m²: 50 - 6 = 44 m²
├─ Múltiplos de 4: floor(44 / 4) = floor(11) = 11
├─ Quantidade (F-07-QTD) = 1 + 11 = 12 pontos
├─ Carga total (F-08) = 100 + 60 × 11 = 760 VA
└─ Carga por ponto = 760 / 12 ≈ 63.3 VA
```

### 5.4 Tabela de Referência Rápida (Iluminação)

| Área (m²) | Quantidade (F-07-QTD) | Carga Total (F-08) |
|---|---|---|
| 1–6 | 1 | 100 VA |
| 6.1–10 | 2 | 160 VA |
| 10.1–14 | 3 | 220 VA |
| 14.1–18 | 4 | 280 VA |
| 18.1–22 | 5 | 340 VA |
| 22.1–26 | 6 | 400 VA |
| 26.1–50 | 7–12 | 460–760 VA |

---

## 6. Origem Automática vs. Manual

### 6.1 O que é Origem?

**Origem** é um campo que rastreia **quem calculou** a quantidade: a máquina (automático) ou o usuário (manual).

```
┌─────────────────────────────────────────┐
│ Quantidade: 4 [A]                       │
│ Origem: AUTOMATICO                      │
│ Fórmula aplicada: F-03                  │
│ Justificativa: (nenhuma)                │
└─────────────────────────────────────────┘

vs.

┌─────────────────────────────────────────┐
│ Quantidade: 5 [M]                       │
│ Origem: MANUAL                          │
│ Justificativa: "Layout exige 5 pontos"  │
└─────────────────────────────────────────┘
```

### 6.2 Badge Visual

**[A]** = **Automático** (verde)  
**[M]** = **Manual** (amarelo/laranja)

---

### 6.3 Fluxo de Estado (Máquina de Estados)

#### **Estado Inicial: Cálculo Automático**

```
Sistema carrega dependência
        ↓
Aplica fórmula NBR
        ↓
┌──────────────────────────┐
│ origem = AUTOMATICO      │
│ valor = 4                │
│ justificativa = null     │
│ badge = [A]              │
└──────────────────────────┘
```

#### **Usuário Edita a Quantidade**

```
Usuário clica no badge [A] ou no número
        ↓
Modal abre com:
├─ Campo "Quantidade": pré-preenchido com 4
└─ Campo "Motivo": vazio

Usuário muda para 5 e digita motivo
        ↓
Usuário clica "Salvar"
        ↓
┌──────────────────────────────────────────┐
│ origem = MANUAL ← MUDA!                  │
│ valor = 5 ← MUDA!                        │
│ justificativa = "Layout exige"           │
│ badge = [M] ← MUDA!                      │
│ quantidade_automatica = 4 (guardada)     │
└──────────────────────────────────────────┘

Modal reabre? SIM
├─ Campo "Quantidade": JÁ PREENCHIDO com 5
└─ Campo "Motivo": JÁ PREENCHIDO com "Layout exige"
```

#### **Usuário Edita Novamente**

```
Modal reabre com 5 e "Layout exige"
        ↓
Usuário muda para 6 e edita motivo
        ↓
Usuário clica "Salvar"
        ↓
┌──────────────────────────────────────────┐
│ origem = MANUAL ← PERMANECE!             │
│ valor = 6 ← MUDA!                        │
│ justificativa = "Novo motivo"            │
│ badge = [M] ← PERMANECE!                 │
│ quantidade_automatica = 4 (guardada)     │
└──────────────────────────────────────────┘

Aviso importante:
└─ Uma vez MANUAL, sempre MANUAL
```

#### **Tentar Reverter para Automático**

```
Usuário muda de volta para 4 (valor automático)
        ↓
┌──────────────────────────────────────────┐
│ origem = MANUAL ← NÃO VOLTA!             │
│ valor = 4                                │
│ justificativa = "Corrigido"              │
│ badge = [M] ← PERMANECE!                 │
└──────────────────────────────────────────┘

Lógica: Editar uma vez marca como MANUAL
        É papel do PO/usuário reverter manualmente
        ou reabrir o projeto para recalcular
```

### 6.4 Sinalização Visual (UI)

#### **Card Automático**

```
┌─ Pontos de Tomada ─────────────────────┐
│                                        │
│  Quantidade: 4 [A]                     │
│  Carga total: 400 VA                   │
│  Fórmula: F-03                         │
│                                        │
│  [Editar]                              │
└────────────────────────────────────────┘
```

#### **Card Manual**

```
┌─ Pontos de Tomada ─────────────────────┐
│                                        │
│  Quantidade: 5 [M]                     │
│  Carga total: 500 VA                   │
│  Fórmula: F-03 (sobrescrita)           │
│  Motivo: Layout com 5 pontos fixos     │
│                                        │
│  [Editar]                              │
└────────────────────────────────────────┘
```

#### **Modal de Edição**

```
┌─ Ajustes de Pontos ────────────────────┐
│                                        │
│ Essas informações são opcionais.       │
│ Deixe em branco para usar o valor      │
│ calculado pelas dimensões.             │
│                                        │
├─ Pontos de Tomada ─────────────────┐  │
│                                    │  │
│ ◄ Quantidade ►                  [A] │  │
│                                 ou  │  │
│ Sobrescrever o mínimo calculado [M] │  │
│                                    │  │
├─ Motivo (opcional) ───────────────┐  │
│ [Campo de texto para explicar]     │  │
│                                    │  │
│              [Cancelar] [Salvar]   │  │
└────────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

## 7. Exemplo Prático Completo

### 7.1 Cenário: Projeto de Reforma Residencial

Uma pequena casa com 3 cômodos será reformada. Vamos calcular TUG e Iluminação para cada um.

#### **Cômodo 1: Sala (5m × 4m, sem perímetro excluído)**

**Entrada:**
```json
{
  "tipo": "sala",
  "largura_m": 5,
  "comprimento_m": 4,
  "perimetro_excluido_m": 0
}
```

**Cálculo de TUG:**

```
1. Área = 5 × 4 = 20 m²
2. Perímetro = 2(5+4) - 0 = 18m
3. Tipo → Categoria: "sala" → CAT-A
4. Fórmula F-03: ceil(18/5) = ceil(3.6) = 4
5. Mínimo normativo: MAX(4, 1) = 4
6. Carga: 4 × 100 VA = 400 VA

RESULTADO TUG:
├─ Quantidade: 4 [A]
├─ Carga: 400 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-03
```

**Cálculo de Iluminação:**

```
1. Área = 20 m²
2. Área > 6? SIM
3. Acima de 6: 20 - 6 = 14m²
4. Múltiplos de 4: floor(14/4) = 3
5. Quantidade (F-07-QTD): 1 + 3 = 4 pontos
6. Carga (F-08): 100 + 60×3 = 280 VA
7. Carga por ponto: 280 / 4 = 70 VA

RESULTADO ILUMINAÇÃO:
├─ Quantidade: 4 [A]
├─ Carga: 280 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-07-QTD + F-08
```

---

#### **Cômodo 2: Banheiro (2m × 1.5m, sem perímetro excluído)**

**Entrada:**
```json
{
  "tipo": "banheiro",
  "largura_m": 2,
  "comprimento_m": 1.5,
  "perimetro_excluido_m": 0
}
```

**Cálculo de TUG:**

```
1. Área = 2 × 1.5 = 3 m²
2. Perímetro = 2(2+1.5) = 7m
3. Tipo → Categoria: "banheiro" → CAT-B especial
4. Fórmula F-04b: qtd = 1 (sempre)
5. Carga: 1 × 600 VA = 600 VA

RESULTADO TUG:
├─ Quantidade: 1 [A]
├─ Carga: 600 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-04b
```

**Cálculo de Iluminação:**

```
1. Área = 3 m²
2. Área ≤ 6? SIM
3. Quantidade (F-07-QTD): 1 ponto
4. Carga (F-08): 100 VA

RESULTADO ILUMINAÇÃO:
├─ Quantidade: 1 [A]
├─ Carga: 100 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-07-QTD + F-08
```

---

#### **Cômodo 3: Cozinha (4m × 3m, sem perímetro excluído)**

**Entrada:**
```json
{
  "tipo": "cozinha",
  "largura_m": 4,
  "comprimento_m": 3,
  "perimetro_excluido_m": 0
}
```

**Cálculo de TUG:**

```
1. Área = 4 × 3 = 12 m²
2. Perímetro = 2(4+3) = 14m
3. Tipo → Categoria: "cozinha" → CAT-B normal
4. Fórmula F-04a: ceil(14/3.5) = ceil(4) = 4
5. Carga especial:
   ├─ Primeiras 3: 3 × 600 = 1.800 VA
   ├─ Restante (1): 1 × 100 = 100 VA
   └─ Total: 1.900 VA

RESULTADO TUG:
├─ Quantidade: 4 [A]
├─ Carga: 1.900 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-04a
```

**Cálculo de Iluminação:**

```
1. Área = 12 m²
2. Área > 6? SIM
3. Acima de 6: 12 - 6 = 6m²
4. Múltiplos de 4: floor(6/4) = 1
5. Quantidade (F-07-QTD): 1 + 1 = 2 pontos
6. Carga (F-08): 100 + 60×1 = 160 VA
7. Carga por ponto: 160 / 2 = 80 VA

RESULTADO ILUMINAÇÃO:
├─ Quantidade: 2 [A]
├─ Carga: 160 VA
├─ Origem: AUTOMATICO
└─ Fórmula: F-07-QTD + F-08
```

---

### 7.2 Tabela Resumida (Projeto Completo)

| Cômodo | Área | TUG | TUG Carga | Ilum. | Ilum. Carga | Total Carga |
|---|---|---|---|---|---|---|
| Sala | 20 m² | 4 [A] | 400 VA | 4 [A] | 280 VA | 680 VA |
| Banheiro | 3 m² | 1 [A] | 600 VA | 1 [A] | 100 VA | 700 VA |
| Cozinha | 12 m² | 4 [A] | 1.900 VA | 2 [A] | 160 VA | 2.060 VA |
| **TOTAIS** | **35 m²** | **9** | **2.900 VA** | **7** | **540 VA** | **3.440 VA** |

---

## 8. Implementação Técnica

### 8.1 Estrutura de Dados (TypeScript)

#### **Tipos Básicos**

```typescript
// Origem do cálculo
type OrigemQuantidade = "AUTOMATICO" | "MANUAL";

// Parâmetros de entrada do usuário
interface ParametrosQuantidade {
  largura_m: number;
  comprimento_m: number;
  perimetro_excluido_m?: number; // Default: 0
  tipo_dependencia: string;
}

// Resultado final do cálculo
interface CalculoQuantidade {
  quantidade: number;
  origem: OrigemQuantidade;
  justificativa?: string;
  formula_nbr: string;
  parametros_entrada: ParametrosQuantidade;
  parametros_calculados: {
    area_m2: number;
    perimetro_m?: number;
    [key: string]: any;
  };
  referencia_norma: string;
  timestamp: string;
}

// Específico para TUG
interface CalculoTUG extends CalculoQuantidade {
  tipo_quantidade: "TUG";
  categoria: "CAT-A" | "CAT-B" | "CAT-C";
  carga_total_va: number;
  carga_por_tomada: number;
}

// Específico para Iluminação
interface CalculoIluminacao extends CalculoQuantidade {
  tipo_quantidade: "ILUMINACAO";
  carga_total_va: number;
  carga_por_ponto_va: number;
  distribuicao_uniforme: boolean;
}
```

### 8.2 Algoritmo de Cálculo (Pseudocódigo)

#### **Calcular Quantidade de TUG**

```javascript
function calcularQuantidadeTUG(dependencia) {
  // 1. Dimensões
  const area = dependencia.largura_m * dependencia.comprimento_m;
  const perimetro = 
    2 * (dependencia.largura_m + dependencia.comprimento_m) 
    - (dependencia.perimetro_excluido_m || 0);

  // 2. Mapear tipo → categoria
  const categoria = mapearTipoParaCategoria(dependencia.tipo);

  // 3. Aplicar fórmula
  let quantidade;
  let formula_aplicada;
  let carga_por_tomada;

  if (categoria === "CAT-A") {
    // F-03: Salas, Dormitórios, etc
    quantidade = Math.max(Math.ceil(perimetro / 5), 1);
    formula_aplicada = "F-03";
    carga_por_tomada = 100;

  } else if (categoria === "CAT-B") {
    if (dependencia.tipo === "banheiro") {
      // F-04b: Banheiro especial
      quantidade = 1;
      formula_aplicada = "F-04b";
      carga_por_tomada = 600;
    } else {
      // F-04a: Cozinha, Copa, etc
      quantidade = Math.max(Math.ceil(perimetro / 3.5), 1);
      formula_aplicada = "F-04a";
      
      // Carga mista
      const carga_600 = Math.min(3, quantidade) * 600;
      const carga_100 = Math.max(0, quantidade - 3) * 100;
      carga_por_tomada = (carga_600 + carga_100) / quantidade;
    }

  } else if (categoria === "CAT-C") {
    // F-06: Varanda, Área externa
    if (area > 6) {
      quantidade = Math.max(Math.ceil(perimetro / 5), 1);
    } else {
      quantidade = 1;
    }
    formula_aplicada = "F-06";
    carga_por_tomada = 100;
  }

  // 4. Retornar resultado
  return {
    quantidade,
    tipo_quantidade: "TUG",
    categoria,
    origem: "AUTOMATICO",
    justificativa: null,
    formula_nbr: formula_aplicada,
    parametros_entrada: {
      largura_m: dependencia.largura_m,
      comprimento_m: dependencia.comprimento_m,
      perimetro_excluido_m: dependencia.perimetro_excluido_m || 0,
      tipo_dependencia: dependencia.tipo
    },
    parametros_calculados: { area_m2: area, perimetro_m: perimetro },
    carga_total_va: quantidade * carga_por_tomada,
    carga_por_tomada,
    referencia_norma: "NBR 5410:2004",
    timestamp: new Date().toISOString()
  };
}
```

#### **Calcular Quantidade de Iluminação**

```javascript
function calcularQuantidadeIluminacao(dependencia) {
  // 1. Área
  const area = dependencia.largura_m * dependencia.comprimento_m;

  // 2. Quantidade (F-07-QTD)
  let quantidade = 1; // Mínimo
  
  if (area > 6) {
    const multiplos = Math.floor((area - 6) / 4);
    quantidade = 1 + multiplos;
  }

  // 3. Carga total (F-08)
  let carga_total_va;
  
  if (area <= 6) {
    carga_total_va = 100;
  } else {
    const multiplos = Math.floor((area - 6) / 4);
    carga_total_va = 100 + 60 * multiplos;
  }

  // 4. Carga por ponto (distribuída uniformemente)
  const carga_por_ponto = carga_total_va / quantidade;

  // 5. Retornar
  return {
    quantidade,
    tipo_quantidade: "ILUMINACAO",
    origem: "AUTOMATICO",
    justificativa: null,
    formula_nbr: "F-07-QTD + F-08",
    parametros_entrada: {
      largura_m: dependencia.largura_m,
      comprimento_m: dependencia.comprimento_m,
      tipo_dependencia: dependencia.tipo
    },
    parametros_calculados: {
      area_m2: area,
      limite_area_m2: 6,
      passo_area_m2: 4,
      acima_limite: area > 6,
      multiplicador: area > 6 ? Math.floor((area - 6) / 4) : 0
    },
    carga_total_va,
    carga_por_ponto_va: carga_por_ponto,
    distribuicao_uniforme: true,
    referencia_norma: "NBR 5410:2004 item 9.5.2.1.2",
    timestamp: new Date().toISOString()
  };
}
```

#### **Editar Quantidade (Origem Manual)**

```javascript
async function editarQuantidade(
  dependencia,
  tipo, // "TUG" ou "ILUMINACAO"
  novaQuantidade,
  justificativa
) {
  // 1. Validar
  if (novaQuantidade < 1) {
    throw new Error("Quantidade deve ser >= 1");
  }

  // 2. Guardar cálculo automático (para referência)
  const calculo_automatico = tipo === "TUG"
    ? calcularQuantidadeTUG(dependencia)
    : calcularQuantidadeIluminacao(dependencia);

  // 3. Sobrescrever com valor manual
  const chaveResultado = tipo === "TUG" ? "tomadas" : "iluminacao";
  
  dependencia.resultado = {
    ...dependencia.resultado,
    [chaveResultado]: {
      ...calculo_automatico,
      quantidade: novaQuantidade, // MUDA
      origem: "MANUAL", // MUDA
      justificativa, // MUDA
      quantidade_automatica: calculo_automatico.quantidade, // Guardar original
      timestamp: new Date().toISOString()
    }
  };

  // 4. Persistir
  await repoDepend
encias.atualizar(dependencia);

  return dependencia;
}
```

### 8.3 Mapeamento Tipo → Categoria

```javascript
function mapearTipoParaCategoria(tipo) {
  const mapa = {
    // CAT-A
    "sala": "CAT-A",
    "dormitorio": "CAT-A",
    "quarto": "CAT-A",
    "hall": "CAT-A",
    "corredor": "CAT-A",
    "garagem": "CAT-A",

    // CAT-B normal
    "cozinha": "CAT-B",
    "copa": "CAT-B",
    "area_de_servico": "CAT-B",
    "areaserviço": "CAT-B",

    // CAT-B especial
    "banheiro": "CAT-B",

    // CAT-C
    "varanda": "CAT-C",
    "area_externa": "CAT-C",
    "areaexterna": "CAT-C",
    "patio": "CAT-C",
    "pateo": "CAT-C"
  };

  return mapa[tipo.toLowerCase()] || "CAT-A"; // Default
}
```

---

## 9. FAQ — Dúvidas Comuns

### **P: Por que banheiro tem sempre 1 tomada?**

**R:** A norma NBR 5410 é rigorosa com ambientes úmidos. Uma única tomada, instalada em local seguro (fora do alcance de água), é considerada suficiente. Múltiplas tomadas aumentariam riscos de choque.

---

### **P: Como calcular perímetro se a parede tem uma porta grande?**

**R:** Exclua essa parede do perímetro. Se a porta ocupa mais de 1m² ou impede instalação de tomadas, essa parede não conta.

```
Exemplo:
Parede 1 (5m): Completa, conta.
Parede 2 (4m): Com porta grande, exclua 1m → conta 3m
Parede 3 (5m): Completa, conta.
Parede 4 (4m): Completa, conta.

Perímetro total = 5 + 3 + 5 + 4 = 17m
```

---

### **P: Posso ter menos tomadas que o mínimo normativo?**

**R:** Não. O mínimo é lei. Mesmo que a fórmula der resultado 0 (o que não acontece), o mínimo é 1 tomada.

---

### **P: Se editar a quantidade, posso voltar para automático?**

**R:** Uma vez marcado como MANUAL, permanece MANUAL. Se quiser reverter, você precisaria deletar o override manualmente ou um admin reabrir o projeto para recalcular.

---

### **P: Qual a diferença entre F-04a e F-04b?**

**R:**
- **F-04a** (CAT-B normal): `ceil(P / 3.5)` — para cozinha, copa, área de serviço. Quantidade varia conforme perímetro.
- **F-04b** (CAT-B banheiro): `1` — sempre 1, independente de perímetro. Caso especial.

---

### **P: Iluminação usa a mesma fórmula que TUG?**

**R:** Não. São fórmulas diferentes:
- **TUG:** Baseado em perímetro (CAT-A/B/C)
- **Iluminação:** Baseado em área (F-07-QTD e F-08)

---

### **P: Como a carga é distribuída entre pontos de luz?**

**R:** De forma uniforme. Se a carga total é 280 VA e há 4 pontos, cada ponto consome 70 VA.

```
carga_por_ponto = carga_total / quantidade
```

---

### **P: O "Perímetro Excluído" afeta Iluminação?**

**R:** Não. Iluminação usa apenas **Área**. Perímetro Excluído afeta apenas TUG (CAT-A, B, C).

---

### **P: Qual a fonte normativa para F-07-QTD (iluminação)?**

**R:** NBR 5410:2004, item 9.5.2.1.2. A fórmula `1 + floor((A-6)/4)` é uma interpretação prática da norma para distribuição uniforme de iluminação.

---

### **P: E se a dependência for muito grande (>100 m²)?**

**R:** A fórmula não tem limite superior. Calcule normalmente:

```
A = 100 m²
Quantidade = 1 + floor((100 - 6) / 4) = 1 + floor(23.5) = 1 + 23 = 24 pontos
Carga = 100 + 60 × 23 = 1.480 VA
```

---

### **P: Posso ter 0 tomadas em um cômodo?**

**R:** Não. O mínimo normativo é sempre 1. A norma obriga pelo menos 1 tomada em qualquer dependência.

---

### **P: Se o usuário digita quantidade negativa, o sistema aceita?**

**R:** Não. Implementar validação: `if (qtd < 1) throw error("Quantidade deve ser >= 1")`.

---

### **P: Como a justificativa (motivo) é armazenada?**

**R:** Em um campo de texto livre na base de dados. Pode ser qualquer coisa que o usuário digite:
```
Exemplos:
- "Layout real exige 5 pontos"
- "Equipamentos especiais"
- "Aprovado em reunião de projeto"
- "Ajuste conforme site"
```

---

## 10. Checklist de Implementação

Use este checklist para garantir que tudo está implementado:

### **Estrutura de Dados**
- [ ] Criar tipos TypeScript para `CalculoTUG` e `CalculoIluminacao`
- [ ] Adicionar campo `origem: OrigemQuantidade` em ambos
- [ ] Adicionar campo `justificativa: string?`

### **Algoritmos**
- [ ] Implementar `calcularQuantidadeTUG()`
- [ ] Implementar `calcularQuantidadeIluminacao()`
- [ ] Implementar `mapearTipoParaCategoria()`
- [ ] Implementar `editarQuantidade()` (origem MANUAL)

### **Validações**
- [ ] Quantidade >= 1
- [ ] Largura > 0 e Comprimento > 0
- [ ] Perímetro Excluído >= 0
- [ ] Tipo existe na lista de categorias

### **Base de Dados**
- [ ] Criar tabela `dependencia_quantidade_analise`
- [ ] Adicionar índices
- [ ] Testar persistência de AUTOMATICO e MANUAL

### **UI/UX**
- [ ] Badge [A] / [M] visível
- [ ] Modal de edição com campo "Motivo"
- [ ] Campo "Quantidade" pré-preenchido em reabertura
- [ ] Campo "Motivo" pré-preenchido em reabertura
- [ ] Feedback visual "Salvo com sucesso"

### **Testes**
- [ ] Test para F-03 (CAT-A): `ceil(P/5)`
- [ ] Test para F-04a (CAT-B): `ceil(P/3.5)`
- [ ] Test para F-04b (Banheiro): `1`
- [ ] Test para F-06 (CAT-C): Condicional por área
- [ ] Test para F-07-QTD (Iluminação): `1 + floor((A-6)/4)`
- [ ] Test para F-08 (Iluminação carga): `100 + 60×floor((A-6)/4)`
- [ ] Test para mudança AUTOMATICO → MANUAL
- [ ] Test para permanência de MANUAL após edição

### **Documentação**
- [ ] Atualizar README com exemplos
- [ ] Atualizar REFERENCIA-INTEGRAL-SISTEMA.md
- [ ] Comentar funções críticas

---

## 10. Testes Unitários — Exemplos Práticos

Esta seção apresenta testes unitários completos para todas as fórmulas e funções críticas. Use Jest, Vitest ou seu framework preferido.

### 10.1 Testes para F-03 (CAT-A: Salas, Dormitórios)

```typescript
describe("F-03: Quantidade de TUG em CAT-A", () => {
  test("Sala 5m × 4m → 4 tomadas", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });

    expect(result.quantidade).toBe(4);
    expect(result.categoria).toBe("CAT-A");
    expect(result.formula_nbr).toBe("F-03");
    expect(result.carga_total_va).toBe(400); // 4 × 100
    expect(result.origem).toBe("AUTOMATICO");
  });

  test("Sala pequena 2m × 2m → mínimo 1 tomada", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 2,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    expect(result.quantidade).toBe(1); // MIN = 1
    expect(result.carga_total_va).toBe(100);
  });

  test("Perímetro com exclusão → quantidade reduzida", () => {
    const result = calcularQuantidadeTUG({
      tipo: "dormitorio",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 2 // Parede com porta grande
    });

    // P = 2(5+4) - 2 = 16m
    // qtd = ceil(16/5) = ceil(3.2) = 4
    expect(result.quantidade).toBe(4);
    expect(result.parametros_calculados.perimetro_m).toBe(16);
  });

  test("Sala grande 10m × 8m → 8 tomadas", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 10,
      comprimento_m: 8,
      perimetro_excluido_m: 0
    });

    // P = 2(10+8) = 36m
    // qtd = ceil(36/5) = ceil(7.2) = 8
    expect(result.quantidade).toBe(8);
    expect(result.carga_total_va).toBe(800);
  });
});
```

### 10.2 Testes para F-04a (CAT-B Normal: Cozinha, Copa)

```typescript
describe("F-04a: Quantidade de TUG em CAT-B Normal", () => {
  test("Cozinha 4m × 3m → 4 tomadas com carga mista", () => {
    const result = calcularQuantidadeTUG({
      tipo: "cozinha",
      largura_m: 4,
      comprimento_m: 3,
      perimetro_excluido_m: 0
    });

    // P = 2(4+3) = 14m
    // qtd = ceil(14/3.5) = ceil(4) = 4
    expect(result.quantidade).toBe(4);
    expect(result.categoria).toBe("CAT-B");
    expect(result.formula_nbr).toBe("F-04a");
    
    // Carga: 3×600 + 1×100 = 1.900 VA
    expect(result.carga_total_va).toBe(1900);
  });

  test("Copa pequena → 1 tomada de 600 VA", () => {
    const result = calcularQuantidadeTUG({
      tipo: "copa",
      largura_m: 2,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // P = 2(2+2) = 8m
    // qtd = ceil(8/3.5) = ceil(2.28) = 3
    expect(result.quantidade).toBe(3);
    
    // Carga: 3×600 = 1.800 VA (todas as 3 no limite de 600)
    expect(result.carga_total_va).toBe(1800);
  });

  test("Cozinha grande 6m × 5m → 7 tomadas", () => {
    const result = calcularQuantidadeTUG({
      tipo: "cozinha",
      largura_m: 6,
      comprimento_m: 5,
      perimetro_excluido_m: 0
    });

    // P = 2(6+5) = 22m
    // qtd = ceil(22/3.5) = ceil(6.28) = 7
    expect(result.quantidade).toBe(7);
    
    // Carga: 3×600 + 4×100 = 2.200 VA
    expect(result.carga_total_va).toBe(2200);
  });

  test("Área de serviço → aplica F-04a", () => {
    const result = calcularQuantidadeTUG({
      tipo: "area_de_servico",
      largura_m: 3,
      comprimento_m: 3,
      perimetro_excluido_m: 0
    });

    expect(result.categoria).toBe("CAT-B");
    expect(result.formula_nbr).toBe("F-04a");
  });
});
```

### 10.3 Testes para F-04b (CAT-B Banheiro — Especial)

```typescript
describe("F-04b: Quantidade de TUG em Banheiro", () => {
  test("Banheiro pequeno 2m × 1.5m → SEMPRE 1 tomada", () => {
    const result = calcularQuantidadeTUG({
      tipo: "banheiro",
      largura_m: 2,
      comprimento_m: 1.5,
      perimetro_excluido_m: 0
    });

    expect(result.quantidade).toBe(1);
    expect(result.categoria).toBe("CAT-B");
    expect(result.formula_nbr).toBe("F-04b");
    expect(result.carga_total_va).toBe(600);
  });

  test("Banheiro grande 4m × 3m → SEMPRE 1 tomada", () => {
    const result = calcularQuantidadeTUG({
      tipo: "banheiro",
      largura_m: 4,
      comprimento_m: 3,
      perimetro_excluido_m: 0
    });

    // Perímetro não importa, sempre 1
    expect(result.quantidade).toBe(1);
    expect(result.carga_total_va).toBe(600);
  });

  test("Banheiro com perímetro excluído → SEMPRE 1 tomada", () => {
    const result = calcularQuantidadeTUG({
      tipo: "banheiro",
      largura_m: 3,
      comprimento_m: 2,
      perimetro_excluido_m: 2 // Exclusão não importa em banheiro
    });

    expect(result.quantidade).toBe(1);
  });
});
```

### 10.4 Testes para F-06 (CAT-C: Varanda, Área Externa)

```typescript
describe("F-06: Quantidade de TUG em CAT-C", () => {
  test("Varanda pequena 3m × 2m (6 m²) → 1 tomada", () => {
    const result = calcularQuantidadeTUG({
      tipo: "varanda",
      largura_m: 3,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // Área = 6 m² (NÃO > 6)
    expect(result.quantidade).toBe(1);
    expect(result.categoria).toBe("CAT-C");
    expect(result.formula_nbr).toBe("F-06");
    expect(result.carga_total_va).toBe(100);
  });

  test("Varanda acima de 6 m² → aplica F-03", () => {
    const result = calcularQuantidadeTUG({
      tipo: "varanda",
      largura_m: 4,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // Área = 8 m² (> 6)
    // P = 2(4+2) = 12m
    // qtd = ceil(12/5) = ceil(2.4) = 3
    expect(result.quantidade).toBe(3);
    expect(result.carga_total_va).toBe(300);
  });

  test("Limite de 6 m² é inclusivo na condição A ≤ 6", () => {
    const result = calcularQuantidadeTUG({
      tipo: "patio",
      largura_m: 2.5,
      comprimento_m: 2.4,
      perimetro_excluido_m: 0
    });

    // Área = 6 m² (exatamente)
    // Deve usar 1 tomada (condição A ≤ 6)
    expect(result.quantidade).toBe(1);
  });

  test("Área externa grande 8m × 5m → 4 tomadas", () => {
    const result = calcularQuantidadeTUG({
      tipo: "area_externa",
      largura_m: 8,
      comprimento_m: 5,
      perimetro_excluido_m: 0
    });

    // Área = 40 m² (> 6)
    // P = 2(8+5) = 26m
    // qtd = ceil(26/5) = ceil(5.2) = 6
    expect(result.quantidade).toBe(6);
  });
});
```

### 10.5 Testes para F-07-QTD (Iluminação — Quantidade)

```typescript
describe("F-07-QTD: Quantidade de Pontos de Iluminação", () => {
  test("Sala 6 m² → 1 ponto de luz", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 3,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // Área = 6 m² (≤ 6)
    expect(result.quantidade).toBe(1);
    expect(result.tipo_quantidade).toBe("ILUMINACAO");
    expect(result.formula_nbr).toBe("F-07-QTD + F-08");
    expect(result.origem).toBe("AUTOMATICO");
  });

  test("Sala 10 m² → 2 pontos de luz", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // Área = 10 m² (> 6)
    // Acima de 6: 10 - 6 = 4 m²
    // Múltiplos de 4: floor(4 / 4) = 1
    // qtd = 1 + 1 = 2
    expect(result.quantidade).toBe(2);
  });

  test("Sala 20 m² → 4 pontos de luz", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });

    // Área = 20 m²
    // Acima de 6: 20 - 6 = 14 m²
    // Múltiplos de 4: floor(14 / 4) = floor(3.5) = 3
    // qtd = 1 + 3 = 4
    expect(result.quantidade).toBe(4);
  });

  test("Sala 50 m² → 12 pontos de luz", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 10,
      comprimento_m: 5,
      perimetro_excluido_m: 0
    });

    // Área = 50 m²
    // Acima de 6: 50 - 6 = 44 m²
    // Múltiplos de 4: floor(44 / 4) = 11
    // qtd = 1 + 11 = 12
    expect(result.quantidade).toBe(12);
  });

  test("Banheiro pequeno 3 m² → 1 ponto de luz", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "banheiro",
      largura_m: 2,
      comprimento_m: 1.5,
      perimetro_excluido_m: 0
    });

    // Área = 3 m² (≤ 6)
    expect(result.quantidade).toBe(1);
  });
});
```

### 10.6 Testes para F-08 (Iluminação — Carga)

```typescript
describe("F-08: Carga Total de Iluminação", () => {
  test("Área ≤ 6 m² → carga 100 VA", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 3,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    expect(result.carga_total_va).toBe(100);
  });

  test("Área 10 m² → carga 160 VA", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });

    // Área = 10 m²
    // Acima de 6: 10 - 6 = 4 m²
    // Múltiplos: floor(4/4) = 1
    // Carga: 100 + 60×1 = 160 VA
    expect(result.carga_total_va).toBe(160);
  });

  test("Área 20 m² → carga 280 VA", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });

    // Carga: 100 + 60×3 = 280 VA
    expect(result.carga_total_va).toBe(280);
  });

  test("Área 50 m² → carga 760 VA", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 10,
      comprimento_m: 5,
      perimetro_excluido_m: 0
    });

    // Múltiplos: floor((50-6)/4) = 11
    // Carga: 100 + 60×11 = 760 VA
    expect(result.carga_total_va).toBe(760);
  });

  test("Carga por ponto é distribuída uniformemente", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });

    // Quantidade = 4, Carga total = 280 VA
    // Carga por ponto = 280 / 4 = 70 VA
    expect(result.carga_por_ponto_va).toBe(70);
  });
});
```

### 10.7 Testes para Origem Automática vs. Manual

```typescript
describe("Origem: AUTOMATICO vs. MANUAL", () => {
  test("Cálculo inicial é AUTOMATICO", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });

    expect(result.origem).toBe("AUTOMATICO");
    expect(result.justificativa).toBeNull();
  });

  test("Editar quantidade muda para MANUAL", async () => {
    const dependencia = {
      id: "dep-001",
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0,
      resultado: {}
    };

    await editarQuantidade(
      dependencia,
      "TUG",
      5, // Nova quantidade
      "Layout exige 5 pontos"
    );

    expect(dependencia.resultado.tomadas.origem).toBe("MANUAL");
    expect(dependencia.resultado.tomadas.quantidade).toBe(5);
    expect(dependencia.resultado.tomadas.justificativa).toBe("Layout exige 5 pontos");
  });

  test("MANUAL permanece MANUAL após edição posterior", async () => {
    const dependencia = {
      id: "dep-001",
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0,
      resultado: {
        tomadas: {
          quantidade: 5,
          origem: "MANUAL",
          justificativa: "Layout exige 5 pontos"
        }
      }
    };

    // Editar novamente
    await editarQuantidade(
      dependencia,
      "TUG",
      6, // Muda para 6
      "Corrigido conforme aprovação"
    );

    expect(dependencia.resultado.tomadas.origem).toBe("MANUAL");
    expect(dependencia.resultado.tomadas.quantidade).toBe(6);
    expect(dependencia.resultado.tomadas.justificativa).toBe("Corrigido conforme aprovação");
  });

  test("Guardar quantidade automática original", async () => {
    const dependencia = {
      id: "dep-001",
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0,
      resultado: {}
    };

    await editarQuantidade(
      dependencia,
      "TUG",
      5,
      "Layout especial"
    );

    // Deve guardar a quantidade automática original (4)
    expect(dependencia.resultado.tomadas.quantidade_automatica).toBe(4);
    expect(dependencia.resultado.tomadas.quantidade).toBe(5);
  });

  test("Badge AUTOMATICO é [A], MANUAL é [M]", () => {
    const auto = {
      origem: "AUTOMATICO"
    };

    const manual = {
      origem: "MANUAL"
    };

    expect(auto.origem === "AUTOMATICO" ? "[A]" : "[M]").toBe("[A]");
    expect(manual.origem === "AUTOMATICO" ? "[A]" : "[M]").toBe("[M]");
  });
});
```

### 10.8 Testes para Validações

```typescript
describe("Validações", () => {
  test("Quantidade não pode ser < 1", () => {
    expect(() => {
      editarQuantidade(
        { id: "dep-001" },
        "TUG",
        0, // Inválido
        "Motivo"
      );
    }).toThrow("Quantidade deve ser >= 1");

    expect(() => {
      editarQuantidade(
        { id: "dep-001" },
        "TUG",
        -5, // Inválido
        "Motivo"
      );
    }).toThrow("Quantidade deve ser >= 1");
  });

  test("Largura e Comprimento devem ser > 0", () => {
    expect(() => {
      calcularQuantidadeTUG({
        tipo: "sala",
        largura_m: 0, // Inválido
        comprimento_m: 4,
        perimetro_excluido_m: 0
      });
    }).toThrow("Largura deve ser > 0");

    expect(() => {
      calcularQuantidadeTUG({
        tipo: "sala",
        largura_m: 5,
        comprimento_m: -2, // Inválido
        perimetro_excluido_m: 0
      });
    }).toThrow("Comprimento deve ser > 0");
  });

  test("Perímetro Excluído não pode ser negativo", () => {
    expect(() => {
      calcularQuantidadeTUG({
        tipo: "sala",
        largura_m: 5,
        comprimento_m: 4,
        perimetro_excluido_m: -1 // Inválido
      });
    }).toThrow("Perímetro Excluído não pode ser negativo");
  });

  test("Perímetro Excluído não pode ser > perímetro total", () => {
    expect(() => {
      calcularQuantidadeTUG({
        tipo: "sala",
        largura_m: 5,
        comprimento_m: 4,
        perimetro_excluido_m: 20 // Perímetro total é 18
      });
    }).toThrow("Perímetro Excluído não pode ser maior que o perímetro total");
  });

  test("Tipo de dependência deve ser válido", () => {
    expect(() => {
      calcularQuantidadeTUG({
        tipo: "tipo_inexistente",
        largura_m: 5,
        comprimento_m: 4,
        perimetro_excluido_m: 0
      });
    }).not.toThrow(); // Deve usar valor padrão (CAT-A)
  });
});
```

### 10.9 Testes para Casos Extremos (Edge Cases)

```typescript
describe("Casos Extremos", () => {
  test("Dimensões muito pequenas (1m × 1m)", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 1,
      comprimento_m: 1,
      perimetro_excluido_m: 0
    });

    // P = 2(1+1) = 4m
    // qtd = ceil(4/5) = ceil(0.8) = 1 (mínimo)
    expect(result.quantidade).toBe(1);
  });

  test("Dimensões muito grandes (50m × 40m)", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 50,
      comprimento_m: 40,
      perimetro_excluido_m: 0
    });

    // P = 2(50+40) = 180m
    // qtd = ceil(180/5) = 36
    expect(result.quantidade).toBe(36);
  });

  test("Perímetro com decimais é arredondado corretamente", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 5.5,
      comprimento_m: 4.3,
      perimetro_excluido_m: 0.5
    });

    // P = 2(5.5+4.3) - 0.5 = 19.6 - 0.5 = 19.1
    // qtd = ceil(19.1/5) = ceil(3.82) = 4
    expect(result.quantidade).toBe(4);
  });

  test("Iluminação em área bem acima de 6 m²", () => {
    const result = calcularQuantidadeIluminacao({
      tipo: "sala",
      largura_m: 100,
      comprimento_m: 100,
      perimetro_excluido_m: 0
    });

    // Área = 10.000 m²
    // Múltiplos: floor((10000-6)/4) = 2498
    // qtd = 1 + 2498 = 2499 pontos (extremo, mas válido)
    expect(result.quantidade).toBe(2499);
  });
});
```

### 10.10 Testes para Mapeamento Tipo → Categoria

```typescript
describe("Mapeamento Tipo → Categoria", () => {
  test("Sala → CAT-A", () => {
    const result = calcularQuantidadeTUG({
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-A");
  });

  test("Dormitório → CAT-A", () => {
    const result = calcularQuantidadeTUG({
      tipo: "dormitorio",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-A");
  });

  test("Cozinha → CAT-B", () => {
    const result = calcularQuantidadeTUG({
      tipo: "cozinha",
      largura_m: 4,
      comprimento_m: 3,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-B");
  });

  test("Banheiro → CAT-B (especial)", () => {
    const result = calcularQuantidadeTUG({
      tipo: "banheiro",
      largura_m: 2,
      comprimento_m: 1.5,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-B");
    expect(result.formula_nbr).toBe("F-04b");
  });

  test("Varanda → CAT-C", () => {
    const result = calcularQuantidadeTUG({
      tipo: "varanda",
      largura_m: 3,
      comprimento_m: 2,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-C");
  });

  test("Tipo inválido usa padrão CAT-A", () => {
    const result = calcularQuantidadeTUG({
      tipo: "tipo_desconhecido",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    });
    expect(result.categoria).toBe("CAT-A"); // Padrão
  });
});
```

### 10.11 Suite Completa (Exemplo Jest)

Para executar todos estes testes, crie um arquivo `calculoQuantidade.test.ts`:

```bash
# Instalar Jest
npm install --save-dev jest @types/jest ts-jest

# Configurar jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
};

# Rodar testes
npm test

# Com cobertura
npm test -- --coverage
```

### 10.12 Cobertura de Testes Recomendada

| Componente | Casos Testados | Cobertura Esperada |
|---|---|---|
| F-03 (CAT-A) | 4 casos | 100% |
| F-04a (CAT-B Normal) | 3 casos | 100% |
| F-04b (Banheiro) | 3 casos | 100% |
| F-06 (CAT-C) | 4 casos | 100% |
| F-07-QTD (Iluminação) | 5 casos | 100% |
| F-08 (Carga) | 5 casos | 100% |
| Origem AUTOMATICO/MANUAL | 5 casos | 100% |
| Validações | 5 casos | 100% |
| Casos Extremos | 5 casos | 100% |
| Mapeamento Tipo | 6 casos | 100% |
| **TOTAL** | **45+ casos** | **100%** |

---

---

## 12. Conversão para HTML e PDF — Guia Prático

### 12.1 Visão Geral

Este tutorial está disponível em **três formatos**:

1. **Markdown** (`.md`) — Edição e leitura em VS Code
2. **HTML** (`.html`) — Visualização em navegador, impressão em tela
3. **PDF** (`.pdf`) — Distribuição, impressão física, arquivamento

Todos os formatos mantêm **fidelidade textual, acentuação completa (UTF-8) e formatação consistente**.

### 12.2 Arquivos Fornecidos

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md` | Markdown original | ~56 KB |
| `TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html` | HTML com CSS profissional | ~80 KB |
| `TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.pdf` | PDF A4 pronto para imprimir | ~150 KB |
| `converter-md-para-html-pdf.ps1` | Script de conversão automática | ~8 KB |

### 12.3 Convertendo Você Mesmo

#### **Opção 1: Usar o Script PowerShell (Recomendado)**

```powershell
# Navegar até a pasta docs
cd docs/

# Executar conversão (apenas HTML)
.\exemplos\converter-md-para-html-pdf.ps1 `
  -InputFile "TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md" `
  -OutputDir "./"

# Executar conversão (HTML + PDF com Chrome)
.\exemplos\converter-md-para-html-pdf.ps1 `
  -InputFile "TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md" `
  -OutputDir "./" `
  -GeneratePDF

# Se Chrome está em caminho diferente
.\exemplos\converter-md-para-html-pdf.ps1 `
  -InputFile "TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md" `
  -OutputDir "./" `
  -GeneratePDF `
  -ChromePath "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
```

**Output esperado:**
```
✓ HTML gerado: TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html
✓ PDF gerado com sucesso: TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.pdf
```

---

#### **Opção 2: Converter Manualmente com Pandoc**

Se preferir usar Pandoc (mais portável):

```bash
# Instalar Pandoc (uma vez)
choco install pandoc  # Windows com Chocolatey
brew install pandoc   # Mac
sudo apt install pandoc  # Linux

# Converter Markdown para HTML
pandoc TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md \
  -o TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html \
  -c estilo.css \
  --self-contained-html \
  --metadata-file=metadata.yaml

# Converter para PDF (requer wkhtmltopdf ou similar)
pandoc TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md \
  -o TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.pdf \
  --pdf-engine=wkhtmltopdf \
  -V margin-top=20mm \
  -V margin-bottom=20mm
```

---

#### **Opção 3: Converter Manualmente via Navegador**

1. **Abra o HTML** em navegador (Chrome, Firefox, Edge)
   ```
   File → Open File → TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html
   ```

2. **Para salvar como PDF:**
   - Pressione `Ctrl+P` (ou `Cmd+P` no Mac)
   - Selecione "Salvar como PDF"
   - Recomendado: Margem 20mm, fundo desabilitado

3. **Validar:**
   - ☑️ Acentuação correta (á, é, í, ó, ú, ã, õ, ç)
   - ☑️ Tabelas mantêm formatação
   - ☑️ Páginas não cortadas
   - ☑️ Nenhuma tabela virou "texto corrido"

---

### 12.4 Requisitos de Conversão

#### **Encoding (CRÍTICO)**

- ✅ **Entrada:** Markdown salvo em UTF-8 (sem BOM)
- ✅ **Saída:** HTML com `<meta charset="utf-8">`
- ✅ **PDF:** Exportado mantendo encoding UTF-8

**Validação:**
```powershell
# Verificar encoding do Markdown
file TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md
# Esperado: "UTF-8 Unicode text"
```

---

#### **Acentuação Portuguesa**

| Caractere | Símbolo | Status |
|---|---|---|
| á, é, í, ó, ú | Agudos | ✅ Preservados |
| ã, õ | Til | ✅ Preservados |
| ç | Cedilha | ✅ Preservados |
| — | Travessão | ✅ Preservados |
| « » | Aspas francesas | ✅ Preservadas |

**Teste:** O texto contém "conformidade", "especificações", "automático" — se aparecerem com acentos corretos no HTML/PDF, você está bem.

---

#### **Formatação de Tabelas**

**Regra crítica:** Nenhuma tabela deve virar "texto corrido"

HTML/CSS aplicado:
```css
table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}

td {
  word-break: break-word;
  overflow-wrap: anywhere;
}
```

Isso garante:
- Quebra de linha automática nas células
- Mantém estrutura de tabela visível
- Funciona em telas pequenas e grandes
- Imprime corretamente em A4

---

### 12.5 Checklist de Validação

Após converter para HTML e/ou PDF, valide:

- [ ] **Encoding**
  - [ ] Acentuação correta (áéíóúãõç)
  - [ ] Caracteres especiais (—, «, », etc.)
  - [ ] Sem mojibake ou caracteres quebrados

- [ ] **Estrutura**
  - [ ] Títulos mantêm hierarquia (H1, H2, H3, etc.)
  - [ ] Listas formatadas corretamente (ul/ol)
  - [ ] Parágrafos não fundidos

- [ ] **Tabelas**
  - [ ] Bordas visíveis
  - [ ] Cabeçalhos destacados
  - [ ] Nenhuma tabela virou texto corrido
  - [ ] Alinhamento de células preservado

- [ ] **Código**
  - [ ] Blocos de código destacados
  - [ ] Indentação preservada
  - [ ] Palavras-chave visíveis

- [ ] **Impressão (PDF/A4)**
  - [ ] Margens adequadas (20mm recomendado)
  - [ ] Nenhuma linha cortada nas laterais
  - [ ] Páginas numeradas
  - [ ] Cabeçalhos/rodapés consistentes
  - [ ] Quebra de página em posições sensatas

---

### 12.6 Troubleshooting

#### **Problema: Acentuação aparece quebrada (mojibake)**

**Solução:**
1. Verifique encoding do Markdown original
2. Reabra em VS Code e salve como UTF-8 (bottom-right: "UTF-8")
3. Reconverta usando script PowerShell
4. Se ainda falhar, use Pandoc:
   ```bash
   pandoc --from markdown-smart --to html5 input.md -o output.html
   ```

---

#### **Problema: Tabelas ficam muito apertadas**

**Solução:**
- Aumente `table-layout: auto` em vez de `fixed`
- Reduza `font-size` de tabelas (já configurado: 95%)
- Divida tabelas muito grandes em subtabelas

---

#### **Problema: PDF fica com páginas em branco**

**Solução:**
1. Abra HTML em navegador
2. Pressione F12 (DevTools)
3. Veja se há erros de CSS
4. Tente exportar com "Margem mínima"
5. Se persistir, use Chrome com `--print-to-pdf` diretamente

---

#### **Problema: Script PowerShell não executa**

**Solução:**
```powershell
# Permitir execução de scripts (uma vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois execute normalmente
.\converter-md-para-html-pdf.ps1 -InputFile "tutorial.md"
```

---

### 12.7 Estilo Visual Padrão

O arquivo HTML inclui estilos profissionais:

| Elemento | Estilo |
|----------|--------|
| **Corpo** | Fonte sans-serif, 16px, linha 1.6 |
| **H1** | 2.2em, azul (#003366), borda dourada |
| **H2** | 1.8em, azul (#004499), borda cinza |
| **Tabelas** | Cabeçalho azul, zebra 5% cinza |
| **Código** | Monospace, fundo cinza (#f4f4f4) |
| **Impressão** | A4 (210×297mm), margens 20mm |

**Customizar:**
1. Abra `TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html` em editor de texto
2. Localize `<style>` no `<head>`
3. Modifique cores, fontes, margens conforme necessário
4. Salve e reabra em navegador

---

### 12.8 Integração com CI/CD

Se quiser gerar HTML/PDF automaticamente em pipeline:

#### **GitHub Actions**

```yaml
name: Generate Documentation

on: [push]

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Pandoc
        run: sudo apt-get install pandoc
      
      - name: Convert MD to HTML
        run: |
          pandoc docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md \
            -o docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html \
            --self-contained-html
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: documentation
          path: docs/*.html
```

#### **GitLab CI**

```yaml
generate_docs:
  image: pandoc/latex
  script:
    - pandoc docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md \
        -o docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html \
        --self-contained-html
  artifacts:
    paths:
      - docs/*.html
```

---

### 12.9 Distribuição

#### **Para Usuários Finais**

1. **Use HTML** para leitura online
2. **Use PDF** para impressão e arquivamento
3. **Ambos** suportam UTF-8 completo

#### **Para Developers**

1. Mantenha **Markdown** no repositório (fonte única)
2. Gere HTML/PDF como artefatos em build
3. Versione PDF em releases (GitHub/GitLab)

#### **Documentação Versionada**

```
docs/
├── v1.0/
│   ├── TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md
│   ├── TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.html
│   └── TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.pdf
├── v1.1/
│   ├── ...
```

---

### 12.10 Referências

- **Guia de Conversão:** `docs/avaliacao-pqa-500/guia-conversao-md-html-pdf.md`
- **Pandoc Docs:** https://pandoc.org/
- **Chrome Print to PDF:** https://chromedriver.chromium.org/
- **UTF-8 Validation:** Use BOM Checker no VS Code

---

## 11. Referências

- **Documento Original:** `docs/NBR5410-Quantidade-TUG-Iluminacao-Sistematica.md`
- **Norma:** NBR 5410:2004 — Instalações Elétricas de Baixa Tensão
- **Fórmulas Críticas:** F-01 a F-08, F-07-QTD
- **Projeto:** SIE — Sistema de Instalações Elétricas (feature/nbr5410-conformidade-closeout)
- **Guia de Conversão:** `docs/avaliacao-pqa-500/guia-conversao-md-html-pdf.md`

---

**Tutorial versão:** 1.1 (com seção de conversão)
**Data:** 2026-07-05  
**Autor:** Atlas - Business Analyst + Dex - Full Stack Developer  
**Status:** Pronto para uso (MD + HTML + PDF)

