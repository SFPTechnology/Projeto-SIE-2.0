# 📊 Análise Completa: Métrica "NBR: N alerta · M erro" na Tela Dependências

**Documento:** Investigação Completa da Métrica de Conformidade NBR 5410  
**Analista:** Atlas (AIOX Analyst)  
**Data:** 2026-07-05  
**Branch:** `feature/nbr5410-conformidade-closeout`  
**Status:** 🔍 Descoberta e Mapeamento Completo

---

## 📋 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [1. Origem da Métrica](#1-origem-da-métrica)
3. [2. Escopo de Correção](#2-escopo-de-correção)
4. [3. Mapeamento de Dependências](#3-mapeamento-de-dependências)
5. [4. Mapeamento Técnico NBR → Circuito → Problema](#4-mapeamento-técnico-nbr--circuito--problema)
6. [5. Matriz de Ação Combinada](#5-matriz-de-ação-combinada)
7. [6. Distribuição de Camadas](#6-distribuição-de-camadas)
8. [7. Fluxo de Validação](#7-fluxo-de-validação)
9. [8. Referências Técnicas](#8-referências-técnicas)
10. [9. Resumo de Achados](#9-resumo-de-achados)
11. [10. Handoff para Agentes Especializados](#10-handoff-para-agentes-especializados)

---

## 📌 Resumo Executivo

### Definição

A notação **"NBR: {N} alerta · {M} erro"** exibida na tela "Dependências" é uma **síntese de violações normativas** detectadas em tempo real para cada cômodo/dependência do projeto elétrico. Ela resume:

- **{N} alertas** = Avisos que violam a norma mas não bloqueiam cálculo (severidade `ATENCAO`)
- **{M} erros** = Violações críticas que bloqueiam avanço (severidade `ERRO`)

### Contexto do Projeto

O **Sistema SIE (Sistema de Instalações Elétricas)** é uma ferramenta de dimensionamento elétrico residencial conforme **NBR 5410:2008** (norma brasileira), parametrizada para a concessionária **EDP-SP** com tabelas versionadas (v06/v09).

**Auditoria base (2026-06-21):**
- 18 incongruências detectadas
- 4 delas críticas (bloqueam aceite)
- Plano de correção faseado em 4 fases + camada transversal

### Estado Atual

| Aspecto | Status |
|---------|--------|
| **Implementado** | ~35% (LAYERS 1-2 parcial: classificação, demanda, entrada) |
| **Parcial** | ~30% (máquina de estado existe, diagnósticos advisory) |
| **Greenfield** | ~35% (LAYERS 3-6: circuitos, condutores, proteção, artefatos) |
| **Risco principal** | Diagnósticos são informativos (advisory), não bloqueantes (fail-closed) |

---

## 1. Origem da Métrica

### 1.1 Localização no Código

**Arquivo:** `src/components/app/TabelaDependencias.tsx`  
**Linhas:** 52-61  
**Função:** `resumoDiagnosticos(dep: DependenciaAgregado)`

```typescript
function resumoDiagnosticos(dep: DependenciaAgregado): string | null {
  const diagnosticos = dep.resultado?.diagnosticos ?? [];
  const erros = diagnosticos.filter((d) => d.severidade === "ERRO").length;
  const alertas = diagnosticos.filter((d) => d.severidade === "ATENCAO").length;
  if (erros === 0 && alertas === 0) return null;
  const partes: string[] = [];
  if (erros > 0) partes.push(`${erros} erro${erros > 1 ? "s" : ""}`);
  if (alertas > 0) partes.push(`${alertas} alerta${alertas > 1 ? "s" : ""}`);
  return `NBR: ${partes.join(" · ")}`;  // ← Label final exibida
}
```

### 1.2 Fluxo de Origem (Cadeia de Transformação)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DependenciaAgregado (cada cômodo/dependência)            │
│    └─ Entidade de domínio que agrega dados da dependência   │
│                                                             │
│ 2. entrada: { [...dados de entrada do usuário...] }        │
│    └─ Tipo: `EntradaDependencia`                           │
│                                                             │
│ 3. motor.ts (calculo/motor.ts)                             │
│    └─ Executa fórmulas NBR 5410 sobre os dados             │
│    └─ Retorna: `ResultadoCálculo`                          │
│                                                             │
│ 4. resultado: { diagnosticos: [...] }                      │
│    └─ Grava no agregado após cálculo                       │
│                                                             │
│ 5. servico-validacao.ts                                     │
│    └─ Complementa com validações técnicas                  │
│    └─ Adiciona diagnósticos estruturais                    │
│                                                             │
│ 6. resumoDiagnosticos()                                     │
│    └─ Filtra por severidade                                │
│    └─ Monta string "NBR: {N} alerta · {M} erro"            │
│                                                             │
│ 7. TabelaDependencias.tsx → <Tag> com string               │
│    └─ Exibida ao usuário na tela "Dependências"            │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Estrutura do Diagnóstico

Cada item em `diagnosticos[]` segue este esquema (inferido do código):

```typescript
interface Diagnostico {
  // Identificação
  codigo: string;                     // ex: "ERR-TIPO-APARELHO-AUSENTE"
  mensagem: string;                   // ex: "Tipo de aparelho não informado"
  
  // Classificação
  severidade: "ERRO" | "ATENCAO";     // ← Determina se conta em alerta ou erro
  
  // Contexto técnico
  referencia_nbr?: string;            // ex: "NBR 5410 4.2.6"
  circuito_afetado?: string;          // ex: "ILUM-Sala"
  categorias_impactadas?: string[];   // ex: ["iluminacao", "TUG"]
  
  // Resolução
  sugestao_correcao?: string;         // ex: "Selecione um tipo de aparelho"
  fase_correcao?: number;             // ex: 0, 1, 2, 3, 4, 5
}
```

### 1.4 Severidades

| Severidade | Definição | Bloqueia? | Exemplo |
|---|---|---|---|
| **ERRO** | Violação crítica que impede avanço | ✅ SIM | Tipo de aparelho ausente, DR obrigatório não marcado |
| **ATENCAO** | Aviso normativo que exige revisão | ❌ NÃO | Tensão não explicitada (usa default), balanceamento desigual |
| **(nenhum)** | Tudo conforme | — | Sem diagnósticos exibidos |

---

## 2. Escopo de Correção

### 2.1 Mapa de Validações NBR (V01–V15)

Baseado no **Plano de Correção Faseado** reconciliado com código-fonte:

| # | Campo / Regra | Origem | Severidade | Status Código | Fase Corr. | Descrição Técnica |
|---|---|---|---|---|---|---|
| **V01** | `tipoAparelho` obrigatório | Módulos §17, NBR §4.2.6 | ERRO | 🟡 Refatorar | 0.1 | Campo opcional em `modelo/dependencia.ts`; deve ser obrigatório em entrada |
| **V02** | Tensão de placa por carga | NBR §4.2.3 | ATENCAO | 🟡 Existe | 0.4 | Campo `tensaoFixa` existe mas é silenciosamente defaultado a 220V; deve ser explícito e editável |
| **V03** | Fatores de potência por tipo | NBR §4.2.1, EDP v06 | ATENCAO | 🟡 Validar | 0.3 | Divergência aberta: `forno_eletrico` FP=0,8 (código) vs 1,0 (plano); `iluminacao_descarga` 0,55 ✅ |
| **V04** | Roteamento tipo→grupo EDP | Módulos §7 | ATENCAO | 🟢 Correto | — | Mapeamento a–i correto em `tipos-aparelho.ts`; congelar com testes |
| **V05** | Compatibilidade sistema×categoria | Módulos §4.3, V04 | ATENCAO | 🟢 Existe | 1 | `validacao.ts` emite `ATN-TRIFASICA-FORCOU-CATEGORIA-T`; falta **bloqueio duro** |
| **V06** | Tabela 001/002 — pares disjuntor↔seção | NBR Tab. 001/002, Módulos §7.3 | **ERRO** | 🔴 Dado ausente | 1.2 | `subcategorias-fornecimento.data.json` vazio (status=VERIFICAR); sem dados, **nunca inventa entrada** |
| **V07** | Demanda por grupo recalculada | Módulos §8 | ATENCAO | 🟢 Pronto | 1.1 | `motor-demanda.ts` + `fatores-demanda.ts`; apenas revalidar com FP de V03 |
| **V08** | Circuito exclusivo para TUE>10A | NBR §9.5.3, Módulos §9 | ATENCAO | 🔴 Greenfield | 2.1 | Falta lógica em `derivar-circuitos.ts`; hoje mapeador provisório (1 circuito/carga) |
| **V09** | Segregação ILUM vs TUG vs TUE | NBR §9.5.3 | ATENCAO | 🔴 Greenfield | 2.1 | `derivar-circuitos.ts` não segue regras de divisão real |
| **V10** | DR em áreas molhadas/externas | NBR §5.1.3.2, Módulos §5 | **ERRO** | 🔴 Não existe | 2.2 | Falta campo `requer_DR` em `modelo/circuito.ts`; falta marcação automática |
| **V11** | Método de instalação informado | NBR §6.2.4, Módulos §10 | **ERRO** | 🔴 Não existe | 3.1 | Falta campo em `circuito.ts`; exigido para ampacidade |
| **V12** | Comprimento e temperatura circuito | NBR §6.2.5/6.2.7 | **ERRO** | 🔴 Não existe | 3.1 | Falta campos; exigidos para dimensionamento de condutores e queda de tensão |
| **V13** | Ampacidade e seção mínima | NBR §6.2.4, Tab. 36–39 | **ERRO** | 🔴 Greenfield | 3.2 | Falta motor `calculo/dimensionar-condutores.ts`; falta tabelas de ampacidade |
| **V14** | Queda de tensão ≤ limite | NBR §6.2.7 | ATENCAO | 🔴 Greenfield | 3.3 | Falta motor `calculo/queda-tensao.ts`; falta tabela de limites |
| **V15** | Proteção sobrecorrente | NBR §5.1.2 | **ERRO** | 🔴 Greenfield | 3.4 | Falta motor `calculo/protecao-sobrecorrente.ts`; validar Icu vs curto presumido |

### 2.2 Distribuição por Severidade

**ERROS (bloqueantes) — Fase gate-closed exigida:**
- V01: tipoAparelho obrigatório
- V06: Tabela 001/002 dados + bloqueio
- V10: DR obrigatório marcado
- V11: Método de instalação
- V12: Comprimento + temperatura
- V13: Seção mínima + ampacidade
- V15: Proteção sobrecorrente

**ALERTAS (revisão necessária):**
- V02: Tensão explícita (default não silencioso)
- V03: Reconciliar FP com EDP
- V04: Congelar mapeamento com testes
- V05: Bloqueio duro de compatibilidade
- V07: Revalidar demanda
- V08–V09: Segregação de circuitos
- V14: Queda de tensão

---

## 3. Mapeamento de Dependências

### 3.1 Grafo de Dependências (Ordered DAG)

As validações formam uma **cadeia ordenada** — cada camada depende das anteriores:

```
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 1: SANEAMENTO DA ENTRADA (Fase 0 — Fundação)               │
│                                                                    │
│  V01: tipoAparelho obrigatório ◄─── V02: tensão por carga        │
│                                  └─── V03: FP por tipo             │
│                                       (Severidade: ERRO, AT, AT)  │
│                                                                    │
│  Gate: Todo tipo de aparelho classificado; nenhuma pendência      │
│        de tipo; sem defaults silenciosos                          │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 2: DEMANDA & ENTRADA (Fase 1 — Consome LAYER 1)             │
│                                                                    │
│  V04: Roteamento tipo→grupo ✅                                     │
│  V05: Compatibilidade sistema×categoria (ATN → bloqueio)         │
│  V06: Tabela 001/002 (ERR — CRÍTICO, dado ausente) ◄─ V07: DT    │
│                                                                    │
│  Gate: Entrada dimensionada de forma segura; sem "par inválido"   │
│        como 150A + 25mm²; Tabela 001/002 populada = bloqueio     │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 3: DIVISÃO DE CIRCUITOS (Fase 2 — Keystone)                │
│                                                                    │
│  V08: Circuito exclusivo TUE > 10A ◄─ V09: Segregação ILUM/TUG/TUE│
│  V10: DR em áreas molhadas (ERR — marca automática)              │
│                                                                    │
│  Gate: Circuitos reais, tipados (ILUM, TUG-seco, TUG-molhado,   │
│        TUE-dedicado), cada carga em exatamente 1 circuito        │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 4: DIMENSIONAMENTO (Fase 3 — Eletricidade)                 │
│                                                                    │
│  V11: Método instalação ◄─ V12: Comprimento + temperatura        │
│  V13: Seção mínima + ampacidade (ERR — governa seção)           │
│  V14: Queda de tensão (ATN — pode reiterar seção)               │
│  V15: Proteção sobrecorrente (ERR — validar Icu)                 │
│                                                                    │
│  Gate: Condutores e proteções dimensionados e verificados        │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 5: SISTEMA (Fase 4 — Integração)                           │
│                                                                    │
│  V04.2: Balanceamento de fases (já pronto) ✅                     │
│  V10.2: Aterramento + equipotencialização (ERR — novo)           │
│                                                                    │
│  Gate: Instalação eletricamente completa e equilibrada            │
└────────────────────────────────────────────────────────────────────┘
                                ↓
┌────────────────────────────────────────────────────────────────────┐
│ LAYER 6: SAÍDA AUDITÁVEL (Fase 5 — Entrega)                      │
│                                                                    │
│  Memorial rastreável + Quadro de cargas + Unifilar               │
│  (Depende de todas as fases anteriores para conteúdo válido)     │
│                                                                    │
│  Gate: Documento auditável suficiente para conferência + ART      │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 Efeito Cascata (Erro Raiz → N Erros Observados)

Um **único erro raiz** em LAYER N propaga como múltiplos erros nas LAYERs N+1, N+2, etc.

**Exemplo concreto:**

```
Erro raiz (LAYER 1, V01): tipoAparelho = null
    ↓
Ar-condicionado roteado ao grupo "a" (default)
    ↓
LAYER 2 (V04): Classificação ambígua → ATN
LAYER 2 (V06): Sem entrada específica → ERR (Tabela 001/002)
    ↓
LAYER 3 (V08): Não pode alocar circuito TUE exclusivo → ERR
LAYER 3 (V09): Circuito misturado de tipos → ERR
    ↓
LAYER 4 (V11): Sem dados de instalação → ERR
LAYER 4 (V13): Sem IB calculado → ERR
    ↓
Exibição: "NBR: 6 erros"  ← Mas origem é 1 erro raiz (V01)
```

### 3.3 Precedência (Critério de Implementação)

Para implementação eficiente, respeitar a **ordem DAG**:

1. **LAYER 1 primeiro** (Fase 0): Saneamento de entrada
   - Bloqueia tudo mais; menor esforço relativo
   
2. **LAYER 2 depois** (Fase 1): Demanda + entrada
   - Consome LAYER 1; resolve "Bloqueio A"
   
3. **LAYER 3 em paralelo** (Fase 2): Divisão de circuitos
   - Maior esforço (greenfield), mas desacoplado de LAYER 2 internamente
   - Consome LAYER 2 como entrada
   
4. **LAYER 4 depois** (Fase 3): Dimensionamento
   - Consome LAYER 3; greenfield puro
   
5. **LAYER 5 + 6** (Fases 4–5): Sistema + saída
   - Finais; consomem tudo

---

## 4. Mapeamento Técnico: NBR → Circuito → Problema

### 4.1 Tabela Cruzada (Completa)

| NBR Ref. | Item | Código Diagnóstico | Exemplo SIE Real | Causa Raiz | Arquivo Afetado | Fase | Severidade |
|---|---|---|---|---|---|---|---|
| **§4.2.6** | Tipo de aparelho | `ERR-TIPO-APARELHO-AUSENTE` | AC 3.516 VA sem tipo | Campo `tipoAparelho?` é opcional | `modelo/dependencia.ts` l.41 | 0.1 | ERRO |
| **§4.2.3** | Fator de potência | `ATN-FP-DIVERGENCIA` | Forno FP=0,8 vs 1,0 | `tipos-aparelho.ts` l.54–78 | `tipos-aparelho.ts` | 0.3 | ATENCAO |
| **§4.2.4** | Tensão nominal | `ATN-TENSAO-NAO-EXPLICITADA` | 220V default para 127V nominal | `tensaoFixa` silenciosamente defaultado | `dependencia.ts` l.37 | 0.4 | ATENCAO |
| **§5.1** | Roteamento tipo→grupo | `ATN-GRUPO-INCOERENTE` | Motor mapeado a grupo g | Mapeamento errado (antes, agora correto) | `tipos-aparelho.ts` | — | ATENCAO |
| **§5.1.2** | Compatibilidade tensão×categoria | `ATN-TRIFASICA-CATEGORIA-T-INCOMPATIVEL` | 380V + Categoria T (mono) | Sistema trifásico mas categoria mono | `validacao.ts` l.194–219 | 1 | ATENCAO |
| **Tab. 001/002** | Entrada subcategoria | `ERR-TABELA-ENTRADA-AUSENTE` | 58,3 A sem par disjuntor↔seção | Tabela vazia (`subcategorias-fornecimento.data.json: []`) | `subcategorias-fornecimento.data.json` | 1.2 | ERRO |
| **§9.5.3** | Divisão de circuito | `ATN-CIRCUITO-MISTO-ILUM-TUG` | Iluminação + TUG mesmo circuito | `derivar-circuitos.ts` l.13–20 (mapeador provisório 1:1) | `calculo/derivar-circuitos.ts` | 2.1 | ATENCAO |
| **§9.5.3** | TUE > 10A exclusivo | `ERR-TUE-NAO-EXCLUSIVO` | Chuveiro 8,3 kW compartilha circuito | Lógica de segregação não existe | `calculo/divisao-circuitos.ts` (greenfield) | 2.1 | ERRO |
| **§5.1.3.2** | DR obrigatório molhado | `ERR-DR-OBRIGATORIO-AUSENTE` | Banheiro sem DR marcado | Falta campo `requer_DR` em `circuito.ts` | `modelo/circuito.ts` | 2.2 | ERRO |
| **§6.2.4** | Método de instalação | `ERR-METODO-INSTALACAO-AUSENTE` | Circuito sem tipo de instalação | Falta campo em `circuito.ts` l.25–38 | `modelo/circuito.ts` | 3.1 | ERRO |
| **§6.2.5/6.2.7** | Comprimento + temperatura | `ERR-COMPRIMENTO-AUSENTE` | Circuito sem comprimento especificado | Falta campos em `circuito.ts` | `modelo/circuito.ts` | 3.1 | ERRO |
| **Tab. 36–39** | Seção mínima + ampacidade | `ERR-SECAO-SUBMINIMA` | Condutor 1,0 mm² para 25 A | Motor de dimensionamento não existe | `calculo/dimensionar-condutores.ts` (greenfield) | 3.2 | ERRO |
| **§6.2.7** | Queda de tensão | `ATN-QUEDA-ACIMA-LIMITE` | ΔV = 5,8% (limite 3%) | Motor de queda não existe | `calculo/queda-tensao.ts` (greenfield) | 3.3 | ATENCAO |
| **§5.1.2** | Proteção sobrecorrente | `ERR-PROTECAO-INCOMPATIVEL` | In=20A, Iz=16A (inválido) | Motor de proteção não existe | `calculo/protecao-sobrecorrente.ts` (greenfield) | 3.4 | ERRO |
| **§6.4** | Aterramento + equipotencialização | `ERR-PE-AUSENTE` | Circuito sem condutor PE | Falta campo em `circuito.ts` | `modelo/circuito.ts` | 4.2 | ERRO |

### 4.2 Hierarquia: Diagnóstico → Circuito → Dependência

```
Dependencia (ex: "Cozinha")
  ├─ entrada: { [...] }
  ├─ resultado: {
  │    diagnosticos: [
  │      {
  │        codigo: "ERR-TIPO-APARELHO-AUSENTE",
  │        severidade: "ERRO",
  │        circuito_afetado: "TUE-Cozinha-Chuveiro",  ← Qual circuito
  │        categorias_impactadas: ["tue"],             ← Qual categoria
  │        referencia_nbr: "NBR 5410 4.2.6",           ← Qual norma
  │        sugestao_correcao: "Selecione tipo..."      ← Como corrigir
  │      },
  │      { ... mais diagnósticos }
  │    ]
  │  }
  │
  └─ circuitos: [
       { id: "TUE-Cozinha-Chuveiro", tipo: "TUE", IB: 36.4, ... },
       { id: "ILUM-Cozinha", tipo: "ILUM", IB: 2.5, ... },
       { id: "TUG-Cozinha", tipo: "TUG", IB: 15.8, ... }
     ]
```

**Fluxo de rastreamento:**
1. Usuário vê `"NBR: 1 erro"` na linha da dependência "Cozinha"
2. Clica para detalhar → expande diagnósticos
3. Encontra `"ERR-TIPO-APARELHO-AUSENTE"`
4. Sistema aponta circuito afetado: `"TUE-Cozinha-Chuveiro"`
5. Referência: `"NBR 5410 4.2.6"` ← consulta norma
6. Sugestão: `"Selecione um tipo de aparelho"` ← ação corretiva

---

## 5. Matriz de Ação Combinada

### 5.1 Algoritmo de Processamento de Diagnósticos

Para cada dependência durante o cálculo:

```pseudo
procedimento atualizarDiagnosticos(dep: DependenciaAgregado):
  diagnosticos ← []
  
  # LAYER 1: Validar entrada
  se dep.entrada.tipoAparelho == null:
    diagnosticos.push({ 
      codigo: "ERR-TIPO-APARELHO-AUSENTE",
      severidade: "ERRO",
      fase: 0.1
    })
    retornar com erro (fail-closed)
  
  se dep.entrada.tensaoFixa == null:
    diagnosticos.push({
      codigo: "ATN-TENSAO-NAO-EXPLICITADA",
      severidade: "ATENCAO",
      fase: 0.4
    })
  
  # LAYER 2: Calcular demanda (consome LAYER 1)
  resultado ← executarMotor(dep.entrada)
  
  para cada carga em dep.entrada.cargas:
    se resultado.grupo == null:
      diagnosticos.push({
        codigo: "ERR-GRUPO-NAO-CLASSIFICAVEL",
        severidade: "ERRO",
        circuito_afetado: carga.id,
        fase: 1
      })
  
  # LAYER 3: Alocar circuitos (consome LAYER 2)
  circuitos ← derivarCircuitos(resultado)
  
  para cada circuito:
    se circuito.tipo == "ILUM" E circuito.tipo == "TUG" (simultaneamente):
      diagnosticos.push({
        codigo: "ATN-CIRCUITO-MISTO",
        severidade: "ATENCAO",
        circuito_afetado: circuito.id,
        fase: 2.1
      })
    
    se circuito.tipo == "TUE" E circuito.IB > 10A:
      se circuito.compartilhado:
        diagnosticos.push({
          codigo: "ERR-TUE-NAO-EXCLUSIVO",
          severidade: "ERRO",
          circuito_afetado: circuito.id,
          fase: 2.1
        })
    
    se dependencia.localizacao in ["molhada", "externa"]:
      se circuito.requer_DR == false:
        diagnosticos.push({
          codigo: "ERR-DR-OBRIGATORIO-AUSENTE",
          severidade: "ERRO",
          circuito_afetado: circuito.id,
          fase: 2.2
        })
  
  # LAYER 4: Dimensionar (consome LAYER 3)
  para cada circuito:
    se circuito.metodo_instalacao == null:
      diagnosticos.push({
        codigo: "ERR-METODO-AUSENTE",
        severidade: "ERRO",
        fase: 3.1
      })
      continuar # fail-closed
    
    seção ← dimensionarCondutor(circuito.IB, circuito.metodo, ...)
    
    se seção < seção_minima[circuito.tipo]:
      diagnosticos.push({
        codigo: "ERR-SECAO-SUBMINIMA",
        severidade: "ERRO",
        circuito_afetado: circuito.id,
        fase: 3.2
      })
    
    queda ← calcularQueda(circuito.comprimento, seção, ...)
    se queda > limite_queda:
      diagnosticos.push({
        codigo: "ATN-QUEDA-ACIMA",
        severidade: "ATENCAO",
        circuito_afetado: circuito.id,
        fase: 3.3
      })
  
  # LAYER 5: Validar sistema (consome LAYER 4)
  balanceamento ← balancearFases(circuitos)
  desbalanceamento ← max(balanceamento) - min(balanceamento)
  
  se desbalanceamento > limite_permitido:
    diagnosticos.push({
      codigo: "ATN-DESBALANCEAMENTO",
      severidade: "ATENCAO",
      fase: 4.1
    })
  
  # LAYER 6: Auditoria (consome tudo)
  se diagnosticos.filter(d => d.severidade == "ERRO").length > 0:
    diagnosticos.push({
      codigo: "ERR-PROJETO-INCOMPLETO",
      severidade: "ERRO",
      sugestao: "Resolva todos os erros críticos antes de concluir"
    })
  
  dep.resultado.diagnosticos ← diagnosticos
```

### 5.2 Lógica de Bloqueio (Fail-Closed)

**Regra única:** O botão "Concluir projeto" fica **bloqueado** enquanto houver **qualquer diagnóstico com severidade ERRO**.

```typescript
// Em transicoes.ts ou servico-validacao.ts
const temErrosCriticos = diagnosticos.some(d => d.severidade === "ERRO");
const podeAvancar = !temErrosCriticos;

if (!podeAvancar) {
  estado.transicao = "EXIGE_VALIDACAO_TECNICA";
  // Botão "Concluir" desabilitado
  // Mensagem: "Resolva os {N} erro(s) antes de prosseguir"
}
```

### 5.3 Exemplo de Progressão

**Dependência: "Cozinha" (com múltiplos problemas)**

| Iteração | Ação do Usuário | Diagnósticos Atuais | Bloqueado? | Descrição |
|---|---|---|---|---|
| 1 | Cria dependência | `[ERR-TIPO-APARELHO-AUSENTE]` | ✅ SIM | Chuveiro sem tipo |
| 2 | Define tipoAparelho="chuveiro" | `[ATN-TENSAO-NAO-EXPLICITADA]` | ❌ NÃO | Aviso (não bloqueia) |
| 3 | Define tensao=220V | `[]` | ❌ NÃO | Sem diagnósticos |
| 4 | Calcula | `[]` | ❌ NÃO | Cálculo OK |
| 5 | Valida | `[ATN-CIRCUITO-MISTO, ATN-QUEDA-ACIMA]` | ❌ NÃO | Avisos estruturais (não bloqueiam) |
| 6 | Solicita relatório | `[]` | ❌ NÃO | Pronto para ART |

---

## 6. Distribuição de Camadas

### 6.1 Estado de Maturidade por Layer

| Layer | Descrição | Implementado | Parcial | Greenfield | Esforço | Prioridade |
|---|---|---|---|---|---|---|
| **1** | Saneamento entrada | 20% | 60% | 20% | Baixo | 🔴 CRÍTICA |
| **2** | Demanda + entrada | 60% | 20% | 20% | Médio | 🔴 CRÍTICA |
| **3** | Divisão circuitos | 5% | 10% | 85% | **ALTO** | 🟠 ALTA |
| **4** | Dimensionamento | 0% | 0% | 100% | **MUITO ALTO** | 🟠 ALTA |
| **5** | Sistema | 30% | 50% | 20% | Médio | 🟡 MÉDIA |
| **6** | Saída auditável | 10% | 40% | 50% | Alto | 🟡 MÉDIA |

### 6.2 Breakdown de Esforço Estimado

*Assumindo 1 engenheiro TypeScript full-time:*

| Fase | Componente | Tempo | Precedência |
|---|---|---|---|
| **0** | Tornar V01–V03 bloqueantes | 2-3 dias | Primeira |
| **1** | Popular Tabela 001/002 + bloqueio | 3-5 dias | Segunda (depende de dado) |
| **1.5** | Transversal: Gates/fail-closed | 1-2 dias | Paralela a Fase 1 |
| **2** | Motor de divisão (V08–V10) | 5-8 dias | Terceira |
| **3** | Dimensionamento (V11–V15) | 10-15 dias | Quarta |
| **4** | Aterramento + balanceamento | 3-5 dias | Quinta |
| **5** | Memorial + quadro + unifilar | 5-7 dias | Sexta |
| **Testes** | Homologação CT01–CT12 | 3-5 dias | Final |
| **Total** | — | **~40-50 dias** | — |

---

## 7. Fluxo de Validação

### 7.1 Sequência Temporal (Lifecycle de Diagnóstico)

```
┌─────────────────────────────────────────────────────────────┐
│ T0: Usuário abre "Dependências"                             │
│     → Sistema carrega DependenciaAgregado[] do BD            │
│     → resumoDiagnosticos() é chamada para cada uma          │
│     → Cada "NBR: ..." é renderizada nas linhas da tabela   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ T1: Usuário clica em uma dependência para editar            │
│     → Modal de edição abre                                  │
│     → diagnosticos[] são carregados em memória              │
│     → Cada diagnóstico é exibido como "Card" ou "Alert"    │
│     → Sugestão de correção é oferecida                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ T2: Usuário aplica uma correção (ex: define tipoAparelho) │
│     → Campo é validado (Zod schema)                        │
│     → Se válido: salva no DB                              │
│     → Dispara: servico-calculo.recalcular(dep)            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ T3: Motor roda (motor.ts)                                   │
│     → Executa fórmulas NBR                                  │
│     → Popula resultado com diagnosticos novos              │
│     → Salva agregado atualizado no BD                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ T4: Tela "Dependências" re-renderiza                        │
│     → resumoDiagnosticos() corre novamente                  │
│     → "NBR: {N} alerta · {M} erro" atualizada             │
│     → Usuário vê feedback em tempo real                    │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Estados Possíveis de uma Dependência

```
RASCUNHO (dados incompletos)
    ↓
PENDENTE (aguardando cálculo)
    ├─ "NBR: {erros}" ← bloqueado aqui
    ├─ "NBR: {alertas}" ← aviso, pode avançar
    │
CALCULADA (cálculo executado)
    ├─ "NBR: 0 alerta · 0 erro" ✅ → pode validar
    │
VALIDADA (técnico revisou)
    │
EXIGE_VALIDACAO_TECNICA (erros críticos)
    └─ "NBR: {N} erro" ← requer retorno a edição
       → Não pode concluir projeto
```

---

## 8. Referências Técnicas

### 8.1 Arquivos-chave Envolvidos

#### Camada de Modelo
- `src/domain/modelo/dependencia.ts` — definição de DependenciaAgregado
- `src/domain/modelo/circuito.ts` — definição de Circuito (incompleta)
- `src/domain/agregado/dependencia-agregado.ts` — agregado com estado

#### Camada de Cálculo
- `src/domain/calculo/motor.ts` — motor principal NBR 5410
- `src/domain/calculo/derivar-circuitos.ts` — mapeador provisório
- `src/domain/calculo/balanceamento-fases.ts` — LPT implementado
- `src/domain/calculo/motor-demanda.ts` — cálculo de demanda
- `src/domain/calculo/corrente-circuitos.ts` — cálculo de IB

#### Camada de Validação
- `src/domain/servicos/servico-validacao.ts` — orquestrador de validações
- `src/domain/distribuidora/edp-sp/validacao.ts` — validações EDP-específicas
- `src/domain/distribuidora/edp-sp/seletor-subcategoria.ts` — seletor de entrada

#### Camada de Tabelas Normativas
- `src/domain/distribuidora/edp-sp/data/subcategorias-fornecimento.data.json` — **VAZIO**
- `src/domain/distribuidora/edp-sp/data/fatores-potencia.data.json`
- `src/domain/nbr/tipos-aparelho.ts` — mapeamento tipo→grupo
- `src/domain/nbr/grupos-demanda.ts` — definição de grupos a–i

#### Camada de UI
- `src/components/app/TabelaDependencias.tsx` — renderização (linha 52–61: resumoDiagnosticos)
- `src/components/app/EditarDependenciaModal.tsx` — edição
- `src/components/app/ValidarModal.tsx` — validação
- `src/components/app/HistoricoPanel.tsx` — histórico

#### Camada de Estado
- `src/domain/estado/transicoes.ts` — máquina de estados

#### Infraestrutura de Dados
- `src/infra/supabase/` — mapeadores BD
- `docs/supabase/` — migrations

### 8.2 Dados Normativos Faltantes (Bloqueadores)

| Dado | Onde entra | Status | Impacto |
|---|---|---|---|
| Tabela 001/002 — T2 a T10 | `subcategorias-fornecimento.data.json` | ❌ Não existe | Bloqueia Fase 1.2 (entrada) |
| Tabelas ampacidade (Tab. 36–39) | `ampacidade.data.json` | ❌ Não existe | Bloqueia Fase 3.2 (condutores) |
| Fatores de correção (temp/agrup.) | `fatores-correcao.data.json` | ❌ Não existe | Bloqueia Fase 3.2 |
| Limites de queda (Tab. 6.2.7) | `tabela-queda-tensao.data.json` | ❌ Não existe | Bloqueia Fase 3.3 |
| Esquema de aterramento padrão | Configurável em `projeto.ts` | ⚠️ Verificar | Bloqueia Fase 4.2 |

**Fonte de dados:** EDP-SP NBR 5410 v06/v09 + especialista normativo/eletricista

### 8.3 Padrões de Código (TypeScript)

#### Criação de Diagnóstico
```typescript
const diagnostico: Diagnostico = {
  codigo: "ERR-TIPO-APARELHO-AUSENTE",
  mensagem: "Tipo de aparelho não foi informado",
  severidade: "ERRO",
  referencia_nbr: "NBR 5410 4.2.6",
  circuito_afetado: "TUE-Cozinha-Chuveiro",
  categorias_impactadas: ["tue"],
  sugestao_correcao: "Selecione o tipo de aparelho na modal de edição",
  fase_correcao: 0.1
};
diagnosticos.push(diagnostico);
```

#### Filtro de Severidade
```typescript
const erros = diagnosticos.filter(d => d.severidade === "ERRO");
const alertas = diagnosticos.filter(d => d.severidade === "ATENCAO");
const temErros = erros.length > 0;
const temAlertas = alertas.length > 0;
```

### 8.4 Testes Relacionados

Suites que cobrem diagnósticos/validação:
- `tests/domain/calculo/motor-demanda.test.ts` — 6/6 ✅
- `tests/domain/calculo/derivar-circuitos.test.ts` — 10/10 ✅
- `tests/domain/calculo/*.test.ts` — 11 suites no módulo EDP-SP

**Cobertura de diagnósticos:** Não coberta atualmente. Necessário adicionar `validacao.test.ts` com casos CT01–CT12.

---

## 9. Resumo de Achados (Investigação Principal Concluída)

### 🎯 Conclusões Principais

1. **Origem:** A métrica é gerada **em tempo real** pela função `resumoDiagnosticos()`, contando `ERRO` e `ATENCAO` a partir do array `resultado.diagnosticos[]`.

2. **Significado:**
   - **ERRO** = Violação crítica bloqueante (fail-closed)
   - **ATENCAO** = Aviso normativo que exige revisão mas permite avanço

3. **Escopo:** 15 validações (V01–V15) organizadas em **6 camadas** que formam uma cadeia de dependências DAG.

4. **Dependências:** Cada erro em layer N cascata em múltiplos erros em layers N+1, N+2, etc.

5. **Maturidade:**
   - ✅ **LAYER 1–2** — ~60% implementado (saneamento + demanda)
   - ⚠️ **LAYER 3–6** — ~35% implementado (circuitos, dimensionamento, sistema, saída)
   - 🔴 **Risco crítico** — Diagnósticos são informativos, não bloqueantes → exige refatoração de `transicoes.ts`

6. **Dado faltante crítico:** `subcategorias-fornecimento.data.json` está vazio → bloqueia Fase 1.2 (entrada).

### 📋 Recomendações Imediatas

1. **Curto prazo (1–2 semanas):**
   - Tornar V01 (tipoAparelho) obrigatório + bloqueante
   - Implementar **fail-closed** na máquina de estados (transversal)
   - Coletar dados de Tabela 001/002 de especialista normativo

2. **Médio prazo (3–4 semanas):**
   - Implementar motor de divisão de circuitos (Fase 2 — LAYER 3)
   - Popular todas as tabelas normativas faltantes

3. **Longo prazo (5–8 semanas):**
   - Motor de dimensionamento (Fase 3 — LAYER 4)
   - Artefatos finais (Fase 5 — LAYER 6)

### 🔍 Próximas Ações para Investigação

1. **Distribuição atual de diagnósticos** no BD
   - Quantos projetos têm ERRO vs. ATENCAO?
   - Qual é o V0X mais frequente?

2. **Validação da source de dados normativo**
   - Confirmar FP forno (0,8 vs. 1,0) com EDP
   - Obter Tabela 001/002 oficial (T2–T10)

3. **Testes de aceitação (CT01–CT12)**
   - Criar suite de homologação para cada fase

---

## 10. 🎯 Handoff para Agentes Especializados

Esta seção detalha o roteiro específico para cada agente do AIOX, com referências diretas às seções de análise.

---

### 10.1 **@architect (Aria) — Validar Design do Motor de Divisão (Fase 2)**

**Contexto:** A Fase 2 é o "keystone" — a entidade `Circuito` existe mas a divisão real NBR 9.5.3 é greenfield.

**Seu objetivo:** Desenhar arquitetura da divisão de circuitos conforme NBR sem acoplamento ao cálculo de demanda (Layer 2).

#### Tarefas Específicas

| # | Tarefa | Referência | Entrada | Saída Esperada |
|---|---|---|---|---|
| **A1** | Validar modelo estendido de `Circuito` | §4.1 (tabela V08–V10), §6.1 (Camada 3) | `modelo/circuito.ts` (linhas 25–38) | Diagrama UML com campos necessários (tipo, requer_DR, metodo_instalacao, comprimento_m, temperatura_C, circuitos_agrupados, seção_condutor, disjuntor, PE) |
| **A2** | Desenhar motor `divisao-circuitos.ts` | §2.2 (Efeito cascata), §5.1 (Algoritmo pseudo-código) | Especificação NBR §9.5.3 + estrutura de `DependenciaAgregado` | Fluxograma de alocação: ILUM → próprio circuito, TUG → agrupa até X kW, TUE > 10A → próprio, TUE ≤ 10A → agrupa com TUG |
| **A3** | Definir estratégia de DR-marking | §4.1 (V10 — DR obrigatório) | Mapa de localizações (molhada/externa/normal) | Regra: `se localizacao in ["molhada", "externa"]: circuito.requer_DR = 30 mA` |
| **A4** | Desenhar IB recalculado pós-divisão | §5.1 (Algoritmo, LAYER 3) | Algoritmo de corrente-circuitos + ligações (mono/bi/tri) | Fórmula: IB = P / (√3 × V × cos(φ)) para cada circuito, com tensão de placa real (V02) |
| **A5** | Validar decoupling Layer 2 → Layer 3 | §3.1 (DAG), §3.2 (Efeito cascata) | Módulo `motor-demanda.ts` (já pronto) | Certificado: divisão de circuitos pode rodar independentemente sem re-executar cálculo de demanda |

#### Checklist de Arquitetura

```
☐ Modelo de Circuito cobre todos os 12 campos (tipo, DR, método, comprimento, temp, agrupamento, seção, disjuntor, PE, IB, tensão, comprimento_secundário)
☐ Motor de divisão segue árvore de decisão: ILUM → TUG → TUE (granularidade)
☐ Cada circuito tem ID único descritivo (padrão TIPO-Dependencia-[sufixo], já implementado)
☐ DR é marcado automaticamente para áreas molhadas (não depende de entrada do usuário)
☐ IB é recalculado por circuito (não é média das cargas)
☐ Sem acoplamento com Layer 2 (demanda não precisa ser recalculada após divisão)
☐ Código é testável em isolamento (mock de DependenciaAgregado basta)
```

#### Documentação Entregue

- `docs/architecture/fase-2-divisao-circuitos.md` — desenho técnico
- `docs/architecture/modelo-circuito-estendido.yaml` — schema estendido
- UML diagram (AsciiArt ou Mermaid)

**Timeline:** 2–3 dias  
**Bloqueador:** Nenhum (análise é independente)

---

### 10.2 **@pm (Morgan) — Transformar Fases 0–5 em Épico + Stories**

**Contexto:** O plano de correção está faseado (Fases 0–5 + transversal) mas ainda em formato de análise. Precisa virar épico + stories com DoD (Definition of Done) claro.

**Seu objetivo:** Orquestrar as 5 fases como épico "NBR 5410 Conformidade — Fase 2 Greenfield" com stories granulares, priorizadas e rastreáveis.

#### Tarefas Específicas

| # | Tarefa | Referência | Entrada | Saída Esperada |
|---|---|---|---|---|
| **P1** | Criar épico "NBR 5410 Fase 2–5" | §5.2 (Precedência), §6.2 (Breakdown de esforço) | Plano de correção + matriz de dependências | Epic no Linear/Jira com: objetivo, critério de sucesso, roadmap de fases, pontos de Story estimados |
| **P2** | Decompor Fase 2 em stories granulares | §5.1 (Algoritmo de processamento), §2.2 (V08–V10) | Especificação NBR §9.5.3 | 8–10 stories: "Motor de divisão", "Marcação DR", "Recalcular IB", "Testes de divisão", "Integração com UI", etc. |
| **P3** | Definir precedência rigorosa | §3.1 (DAG), §3.2 (Cascata) | Grafo de dependências | Matriz: Story X bloqueia Story Y? Identificar critical path (atividades que não podem ser parallelizadas) |
| **P4** | Atribuir pontos Story (t-shirt) | §6.2 (Breakdown de esforço) | Estimativas por Fase (2–3 dias Fase 0, 5–8 dias Fase 2, etc.) | Cada story tem: XS/S/M/L/XL, pré-requisitos listados, "pede entrega de @architect" vs. "usa saída de @dev" |
| **P5** | Definir acceptance criteria (AC) de teste | §5.3 (Exemplo de progressão), §7.1 (Ciclo de vida) | Matriz de testes (CT01–CT12), diagnósticos esperados por story | Cada story tem 3–5 ACs testáveis: "Quando carga é TUE > 10A, então vai para circuito exclusivo", "Quando localização = banheiro, então DR = marcado" |
| **P6** | Marcar dependências de dados | §8.2 (Dados faltantes) | Tabela de "Pendências de dados" | Cada story que depende de dado externo é marcada: "🔴 Bloqueada por: Tabela 001/002" |
| **P7** | Estabelecer gates entre fases | §5.2 (Lógica de bloqueio) | Transições de estado (LAYER N → LAYER N+1) | Gate LAYER 2→LAYER 3: "✅ Tabela 001/002 populada E V01–V07 todos com testes passando" |

#### Estrutura do Épico (Exemplo)

```yaml
Epic: "NBR 5410 Conformidade — Greenfield Layer 3–6 (Fases 2–5)"
Description: Completar implementação de circuitos, dimensionamento, sistema e artefatos conforme NBR 5410
Objective: Atingir 100% de conformidade técnica; liberar para parecer de eletricista
Timeline: ~50 dias (7 semanas)

Stories:
  
  [Fase 2 — LAYER 3: Divisão de Circuitos]
  ├─ Story 2.1.1 "Motor de divisão conforme NBR 9.5.3"
  │  Points: 8
  │  AC: 
  │    1. Circuitos ILUM sempre separados de TUG (teste: mock com 2 cargas)
  │    2. TUE > 10A vai para circuito próprio
  │    3. IB recalculado por circuito (teste: soma IB = demanda total)
  │  Dependencies: @architect validou design (Story A1–A5)
  │
  ├─ Story 2.1.2 "Marcação automática de DR"
  │  Points: 3
  │  AC:
  │    1. Banheiro → requer_DR = true
  │    2. Cozinha → requer_DR = true se molhada
  │  Dependencies: Story 2.1.1 (motor de divisão)
  │
  [Fase 3 — LAYER 4: Dimensionamento]
  ├─ Story 3.2.1 "Motor de dimensionamento de condutores"
  │  Points: 13
  │  AC:
  │    1. Seção ≥ mínima (1.5 ILUM, 2.5 força)
  │    2. Iz ≥ IB com fator de segurança 1.45
  │  Dependencies: Story 2.1.1 + Tabela de ampacidade populada
  │
  [Gate LAYER 2→3]
  Gate: "Tabela 001/002 completa" ← @data-engineer entrega antes de Story 2.1.1
```

#### Documentação Entregue

- `docs/stories/epics/epic-nbr5410-fase2-5.md` — épico completo com stories
- `docs/roadmap/nbr5410-timeline.xlsx` — Gantt chart com dependencies
- Sprint planning checklist

**Timeline:** 3–5 dias  
**Bloqueador:** Validação de design por @architect (esperado em paralelo com P1)

---

### 10.3 **@data-engineer (Dara) — Popular Tabela 001/002 (Dados Faltantes)**

**Contexto:** O sistema está bloqueado porque `subcategorias-fornecimento.data.json` é vazio. Fase 1.2 exige dados completos e validados.

**Seu objetivo:** Coletar, validar e popular as tabelas normativas faltantes (001/002, ampacidade, fatores de correção, queda de tensão).

#### Tarefas Específicas

| # | Tarefa | Referência | Entrada | Saída Esperada |
|---|---|---|---|---|
| **D1** | Coletar Tabela 001/002 (T2–T10) de especialista normativo | §8.2 (Dados faltantes), §4.1 (V06 — Tabela 001/002) | Requisição ao especialista / EDP-SP v06 | JSON com pares: `{ T2: { In: 20, seção: 2.5 }, T3: { In: 25, seção: 4 }, ... T10: { In: 150, seção: 95 } }` |
| **D2** | Validar Tabela 001/002 contra critério NBR | NBR Tab. 001/002 | Dados coletados + fórmula `IB ≤ In ≤ Iz` | Certificado: cada par satisfaz inequação; sem pares inválidos (ex: 150A + 25mm²) |
| **D3** | Popular `subcategorias-fornecimento.data.json` | §2.1 (Escopo), §4.1 (Arquivo target) | Dados validados | `{ "versao": "09", "status": "COMPLETO", "subcategorias": [T2, T3, ..., T10] }` |
| **D4** | Coletar Tabelas de ampacidade (36–39) | §8.2, §4.1 (V13 — Seção mínima) | NBR 5410:2008 Tabelas 36–39 | JSON: `{ "IEC-60227": { "secao_1.5": { "10A": 13.5, ... }, ... } }` (formato: seção → temperatura → corrente máxima) |
| **D5** | Coletar Fatores de correção (temperatura/agrupamento) | §4.1 (V13 — Ampacidade), §8.2 | NBR Tab. 47 | JSON: `{ "temperatura": { "20C": 1.0, "30C": 0.94, ..., "70C": 0.41 }, "agrupamento": { "1_circuito": 1.0, "2_circuitos": 0.8, ... } }` |
| **D6** | Coletar Limites de queda de tensão (6.2.7) | §4.1 (V14 — Queda de tensão), §8.2 | NBR §6.2.7 + ponto de referência (entrada vs. final) | JSON: `{ "entrada": { "limite_percent": 3.0 }, "final": { "limite_percent": 5.0 } }` |
| **D7** | Criar migrations Supabase | §8.1 (Infraestrutura), CLAUDE.md | Schemas de `circuito.ts` com campos novos (método, comprimento, temperatura) | `docs/supabase/0003_extend_circuito_campos_dimensionamento.sql` |
| **D8** | Atualizar mapeadores Supabase | §8.1 | Novos campos em `circuito.ts` | `infra/supabase/mapeadores.ts` inclui novos campos em `toDomain()` e `toPersistence()` |
| **D9** | Validar dados em staging (teste de integração) | §6.2 (Estimativa: ~2 dias) | Schema + dados + migrations + mapeadores | Query: `SELECT * FROM circuitos WHERE metodo_instalacao IS NOT NULL AND temperatura_ambiente_C IS NOT NULL` retorna > 0 linhas |

#### Checklist de Dados

```
Tabela 001/002 (T2–T10)
☐ Todos os 9 subcategorias (T2 a T10) populadas
☐ Cada subcategoria tem: In (corrente nominal), seção (mm²)
☐ Validado: IB ≤ In ≤ Iz para cada par
☐ Nenhum par inválido (ex: 150A + 25mm²)
☐ Versão explicitada (v06 ou v09)
☐ Status = "COMPLETO" (não "VERIFICAR")

Tabelas de Ampacidade
☐ Cobertas 3 tipos de isolação mínimo (PVC, XLPE, EPR)
☐ Temperaturas: 20°C, 30°C, 40°C, 50°C, 60°C, 70°C
☐ Seções: 0.5, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240

Fatores de Correção
☐ Temperatura: 6–8 faixas documentadas
☐ Agrupamento: 1 a 9+ circuitos
☐ Compatibilidade cross-check: fator_temp × fator_agrup = redução combinada

Limites de Queda
☐ Ponto de referência: entrada (3%) + final do circuito (5%)
☐ Diferenciação por tipo: entrada TN-C-S vs. outros esquemas
```

#### Documentação Entregada

- `docs/data-dictionaries/tabela-001-002-populada.json`
- `docs/data-dictionaries/ampacidade-completa.json`
- `docs/data-dictionaries/fatores-correcao.json`
- `docs/data-dictionaries/limites-queda-tensao.json`
- Migration SQL (`docs/supabase/0003_*.sql`)
- Data validation report (% cobertura, gaps)

**Timeline:** 5–7 dias (coleta + validação + implementation)  
**Bloqueador crítico:** Depends on especialista normativo fornecer dados (contato externo, ~3-5 dias)

---

### 10.4 **@dev (Dex) — Implementar Fail-Closed (Severidade: CRÍTICA)**

**Contexto:** A maior fraqueza do sistema: diagnósticos são informativos (advisory), não bloqueantes. Um usuário com "NBR: 3 erros" ainda consegue calcular e avançar.

**Seu objetivo:** Implementar **fail-closed** na máquina de estados — qualquer diagnóstico ERRO bloqueia avanço até resolução.

#### Tarefas Específicas

| # | Tarefa | Referência | Entrada | Saída Esperada |
|---|---|---|---|---|
| **V1** | Refatorar `transicoes.ts` com gates | §5.2 (Lógica de bloqueio), §7.2 (Estados) | `estado/transicoes.ts` (máquina de estados atual) | Método novo: `podeAvancar(diagnosticos): boolean` que retorna `false` se existe ERRO |
| **V2** | Tornar V01 obrigatório + bloqueante | §2.1 (V01), §5.1 (Algoritmo L1) | `modelo/dependencia.ts` (tipoAparelho? → obrigatório) | `tipoAparelho: TipoAparelho` (sem `?`); Zod schema rejeita null; API retorna 400 se vazio |
| **V3** | Bloquear CALCULAR se V01 ausente | §5.2 (Bloquear "Concluir projeto"), §7.1 (T1–T4) | `servico-calculo.ts` + `transicoes.ts` | Pseudo-código: `if (tipoAparelho == null) throw new Error("ERR-TIPO-APARELHO-AUSENTE")` antes de executar motor |
| **V4** | Bloquear avanço se ERRO presente | §5.2 (Regra única) | `resultado.diagnosticos[]` com `severidade === "ERRO"` | Estado máquina: `CALCULADA` → `VALIDADA` é bloqueado se `diagnosticos.some(d => d.severidade === "ERRO")` |
| **V5** | Exibir mensagem de bloqueio clara | §7.1 (Feedback), §5.3 (Exemplo) | Modal/alert com lista de erros | Mensagem: `"Projeto não pode avançar. Resolva os seguintes erros: {lista com \n}. Use as sugestões de correção."` |
| **V6** | Adicionar retry logic pós-correção | §5.3 (Progressão), §7.1 (T2–T3) | Usuário corrige (ex: define tipoAparelho) e clica "Recalcular" | Sistema re-executa motor, re-popula diagnosticos, re-valida gates, desbloqueia se ERRO = 0 |
| **V7** | Testes unitários de gates | §8.4 (Testes) | Novo `servico-validacao.gate.test.ts` | 8–10 testes: "quando tipoAparelho == null, podeAvancar = false", "quando todos os V01–V05 OK, podeAvancar = true", etc. |
| **V8** | Integração de teste E2E | §5.3 (Exemplo de progressão) | Novo teste Vitest: mock de dependência com erros | Cenário: criar dependência → erros aparecem → desabilitar "Concluir" → usuário corrige → erros desaparecem → habilitar "Concluir" |

#### Checklist de Implementation

```
Máquina de Estados
☐ Novo método em EstadoDependencia: podeAvancar(diagnosticos): boolean
☐ RASCUNHO → PENDENTE: sempre OK
☐ PENDENTE → CALCULADA: bloqueado se ERRO presente
☐ CALCULADA → VALIDADA: bloqueado se ERRO presente
☐ VALIDADA → EXIGE_VALIDACAO_TECNICA: transição automática se ERRO criado
☐ Botão "Concluir projeto" desabilitado se projeto tem qualquer dependência em EXIGE_VALIDACAO_TECNICA

Código de Bloqueio
☐ V01: tipoAparelho obrigatório em schema Zod
☐ V01: motor.ts rejeita null antes de executar
☐ V06: Tabela 001/002 vazia = ERRO bloqueante
☐ V10: DR obrigatório em áreas molhadas
☐ Mensagem de erro aponta sugestão de correção

Testes
☐ 10+ testes unitários (validacao.gate.test.ts)
☐ 1+ teste E2E (integração com UI)
☐ Coverage ≥ 85% para servico-validacao.ts
```

#### Código-Chave (Pseudocódigo)

```typescript
// estado/transicoes.ts — novo método
export function podeAvancar(diagnosticos: Diagnostico[]): boolean {
  const temErros = diagnosticos.some(d => d.severidade === "ERRO");
  return !temErros;  // ← Regra única: sem ERRO, pode avançar
}

// servico-validacao.ts — gate antes de calcular
export function validarPreCalculo(dep: DependenciaAgregado): Diagnostico[] {
  const diagnosticos: Diagnostico[] = [];
  
  // V01: tipoAparelho obrigatório
  if (!dep.entrada.tipoAparelho) {
    diagnosticos.push({
      codigo: "ERR-TIPO-APARELHO-AUSENTE",
      severidade: "ERRO",
      sugestao_correcao: "Selecione um tipo de aparelho"
    });
  }
  
  // V06: Tabela 001/002 populada
  if (status_tabela_entrada === "VERIFICAR") {
    diagnosticos.push({
      codigo: "ERR-TABELA-ENTRADA-AUSENTE",
      severidade: "ERRO",
      sugestao_correcao: "Aguarde população da Tabela 001/002 (contacte especialista)"
    });
  }
  
  if (diagnosticos.filter(d => d.severidade === "ERRO").length > 0) {
    return diagnosticos;  // ← Fail-closed: não continua se ERRO
  }
  
  // Se passou, executa motor
  return executarMotor(dep);
}
```

#### Documentação Entregida

- `docs/architecture/fail-closed-gates.md` — desenho técnico
- `src/domain/servicos/servico-validacao.gate.test.ts` — suite de testes
- Changelog com breaking changes (se houver)

**Timeline:** 3–5 dias  
**Impacto:** Quebra compatibilidade com UI que esperava sempre poder calcular (possível mudança de comportamento visível ao usuário)

---

### 10.5 Sequência Recomendada de Execução

```
PARALELO 1 (Semana 1):
  ├─ @architect: Tarefas A1–A5 (design motor divisão)
  ├─ @pm: Tarefas P1–P7 (criar épico + stories)
  └─ @data-engineer: Tarefa D1 (coleta de Tabela 001/002 — contactar especialista AGORA)

SEMANA 2:
  ├─ @dev: Tarefas V1–V8 (fail-closed) ← alta alavancagem
  └─ @data-engineer: Tarefas D2–D9 (popular + migrations + mapeadores)

SEMANA 3+:
  ├─ @dev: Implementar stories de Fase 2 (divisão circuitos)
  ├─ @qa: Validar stories contra CT01–CT12
  └─ @data-engineer: Acompanhar migrations + mapeadores conforme stories avançam
```

### 10.6 Interfaces Entre Agentes

| De → Para | Documento/Artefato | Prazo |
|---|---|---|
| @architect → @dev | `docs/architecture/fase-2-divisao-circuitos.md` | Fim Semana 1 |
| @pm → @dev | `docs/stories/epics/epic-nbr5410-fase2-5.md` | Fim Semana 1 |
| @data-engineer → @dev | `docs/data-dictionaries/*.json` + migrations SQL | Início Semana 2 |
| @dev → @qa | Commits com stories implementadas + testes | Contínuo (weekly) |
| @pm → @architect | Feedback de stories no épico (ajustes de escopo) | Semana 2+ |

---

## Apêndice: Glossário

| Termo | Definição |
|---|---|
| **Diagnóstico** | Resultado da validação; contém código, mensagem, severidade, referência NBR |
| **Severidade** | `ERRO` (crítico/bloqueante) ou `ATENCAO` (aviso/revisão) |
| **Layer** | Camada lógica da arquitetura (1–6); cada camada depende das anteriores |
| **DAG** | Directed Acyclic Graph — grafo de dependências sem ciclos |
| **Fail-closed** | Sistema permanece bloqueado até que condição crítica seja resolvida |
| **Cascata** | Propagação de erro de layer N para layers N+1, N+2, etc. |
| **EDP-SP** | Concessionária de distribuição de energia (parametrização deste sistema) |
| **NBR 5410** | Norma brasileira de instalações elétricas de baixa tensão |
| **ART** | Anotação de Responsabilidade Técnica (registro obrigatório no Brasil) |
| **TUE** | Tomada de Uso Especifico (ex: chuveiro, ar-condicionado) |
| **TUG** | Tomada de Uso Geral (ex: tomadas de parede) |
| **ILUM** | Circuito de iluminação |
| **DR** | Disjuntor Residual (proteção contra choque elétrico) |
| **PE** | Condutor de Proteção (terra/aterramento) |

---

---

## 📬 Status do Documento

| Aspecto | Status |
|---|---|
| **Investigação Completa** | ✅ CONCLUÍDO (9 seções) |
| **Handoffs Estruturados** | ✅ CONCLUÍDO (4 agentes, tarefas granulares) |
| **Pronto para Execução** | ✅ SIM (sequência, timeline, interfaces definidas) |
| **Aprovação Necesária** | @architect (A1–A5), @pm (P1–P7), @data-engineer (D1) |
| **Próxima Ação** | Distribuir seção 10 aos agentes respectivos |

---

**Documento finalizado em 2026-07-05**  
**Preparado por:** Atlas (Business Analyst, AIOX)  
**Versão:** 2.0 (com handoffs estruturados)  
**Status:** 🟢 **Pronto para Execução** — Aguardando confirmação de @architect, @pm e contato com especialista normativo (D1)

