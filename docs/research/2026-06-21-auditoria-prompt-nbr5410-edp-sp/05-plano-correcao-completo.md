# Plano de Correção Completo — Prompt de Auditoria NBR5410/EDP v2.0 → v3.0

**Preparado por:** Atlas (Analyst Agent)  
**Data:** 2026-06-21  
**Documento analisado:** `Prompt_Verificacao_Incongruencias_NBR5410_EDP_v2_complementado.md`  
**Versão alvo:** 3.0  
**Fontes consolidadas:**
- `02-research-report.md` — relatório técnico de análise
- `03-recommendations.md` — recomendações para o projeto SIE
- `04-sugestoes-correcoes.md` — textos sugeridos para cada correção
- `metrics.yaml` — métricas da análise

---

## Sumário Executivo

O prompt de auditoria NBR5410/EDP v2.0 é tecnicamente robusto: todas as 5 fórmulas dos casos de teste foram verificadas e estão corretas, a estrutura de 16 eixos de varredura é abrangente e o roteamento EDP de cargas está preciso.

Foram identificadas **14 oportunidades de melhoria** (10 inconsistências internas + 4 lacunas normativas). Nenhuma invalida o uso atual do prompt — mas 3 delas (I-02, I-04, I-07) podem levar auditores a não detectar falhas técnicas reais em instalações bifásicas e em circuitos com condutor PE subdimensionado.

**Recomendação:** executar o plano em 2 ondas. Onda 1 (crítica + alta prioridade) em até 5 dias úteis; Onda 2 (média + baixa) antes do próximo ciclo de uso do prompt em produção.

---

## Visão Consolidada dos Problemas

### Distribuição por Severidade

| Severidade | Quantidade | IDs |
|---|:---:|---|
| Alta | 2 | I-02, I-07 |
| Média | 7 | I-01, I-03, I-04, I-06, I-08, I-09, L-01, L-02 |
| Baixa | 5 | I-05, I-10, L-03, L-04 + Casos novos |

### Distribuição por Seção do Prompt

| Seção do prompt | Problemas |
|---|---|
| Seção 5.3 (PRODIST) | L-03 |
| Seção 6 (fronteira NBR×EDP) | I-03 |
| Seção 7.1 (iluminação) | I-01 (parcial) |
| Seção 7.3 (TUG) | I-05 |
| Seção 8.3 (carga instalada EDP) | I-01 (parcial) |
| Seção 8.10 (queda de tensão) | I-02 |
| Seção 9.1 (corrente de projeto) | I-04 |
| Seção 9.2 (condutor × proteção) | I-07, I-08, L-04 |
| Seção 9.3 (DR, DPS, aterramento) | I-09 |
| Seção 11 — E1 | L-01, L-02 |
| Seção 11 — E14 | I-10 |
| Seção 12 — Caso 7 | I-06 |
| Seção 12 — Casos novos | Caso 8, Caso 9 |
| Seção 18 (limitações) | L-01, L-02 (complemento) |

### Mapa de Risco Técnico

```
ALTA CRITICIDADE (corrigir antes de qualquer uso em produção)
├── I-02: fórmula de queda de tensão bifásica ausente
│    └── Risco: auditor usa fórmula errada em Categoria D sem perceber
└── I-07: tabela de dimensionamento PE sem referência
     └── Risco: PE subdimensionado passa em auditoria incorretamente

MÉDIA CRITICIDADE (corrigir na primeira revisão)
├── I-04: Vff não diferenciado por sistema (estrela vs delta) → erro de ~9%
├── I-03: composição de quedas NBR×EDP ausente na fronteira → queda total incorreta
├── I-06: Caso 7 sem valores numéricos → auditores produzem resultados incomparáveis
├── I-08: fatores de temperatura sem referência → Iz subestimada passa sem detecção
├── I-09: critérios DPS ausentes → divergência entre auditores
├── L-01: escopo SPDA indefinido → expectativa sem entrega
└── L-02: escopo GD indefinido → expectativa sem entrega

BAIXA CRITICIDADE (refinar na versão 3.1)
├── I-01: nota sobre VA vs W (informativa, não corretiva)
├── I-05: referência à cláusula NBR 5410 para >6 TUG
├── I-10: precisão numérica mínima não especificada
├── L-03: valores PRODIST Módulo 8 ausentes
└── L-04: condutores em paralelo não mencionados
```

---

## Plano de Correção — Onda 1 (Alta Prioridade)

**Prazo recomendado:** até 5 dias úteis da data desta análise  
**Critério de entrada:** qualquer uso do prompt em auditoria real ou treinamento

---

### Tarefa 1.1 — Corrigir I-02: Fórmula de queda de tensão bifásica

**Seção alvo:** 8.10  
**Esforço estimado:** 30 min  
**Tipo de alteração:** adição de bloco entre as fórmulas existentes

**Onde inserir:** após o bloco "Monofásico" e antes do bloco "Trifásico" da Seção 8.10.

**Texto a inserir:**

```
Bifásico FFN (duas fases + neutro):

ΔV = 2 × I × l × (Rcat × cosφ + XL × senφ)

Onde a corrente I é calculada considerando a tensão fase-fase (Vff).
Atenção: verificar se o alimentador bifásico alimenta cargas em 220 V (FF) ou em 127 V (FN).
Para cargas mistas, a queda deve ser calculada separadamente por trecho e tensão [VERIFICAR].
```

**Adição à lista de incongruências da Seção 8.10:**

```
- fórmula monofásica aplicada a alimentador bifásico (Categoria D) sem distinção;
- tensão FF usada para carga FN ou vice-versa no cálculo bifásico.
```

**Justificativa:** a Categoria D (bifásica FFN) cobre instalações de 12 a 25 kW em estrela e de 12 a 75 kW em delta — faixa de maior incidência em comércio de pequeno porte. Um auditor sem referência bifásica aplica a fórmula monofásica e não detecta o erro.

---

### Tarefa 1.2 — Corrigir I-07: Tabela de dimensionamento mínimo do condutor PE

**Seção alvo:** 9.2  
**Esforço estimado:** 20 min  
**Tipo de alteração:** adição de bloco após o item "seção do PE"

**Texto a inserir após o item "seção do PE":**

```
Seção mínima do condutor PE — regra simplificada
(NBR 5410, Tabela 54.2 ou equivalente) [VERIFICAR versão adotada]:

  Seção do condutor de fase (S)     →  Seção mínima do PE (condutores de cobre)
  S ≤ 16 mm²                        →  PE = S (igual à fase)
  16 mm² < S ≤ 35 mm²               →  PE = 16 mm²
  S > 35 mm²                        →  PE = S / 2

  Quando PE for de material diferente da fase, calcular seção equivalente
  pela resistência elétrica. [VERIFICAR NBR 5410 texto oficial]

Incongruências a procurar:
  - PE com seção menor que a regra acima sem justificativa documentada;
  - PE ausente no diagrama unifilar ou memorial de cálculo;
  - PE com seção igual ao neutro mas inferior ao mínimo exigido pela fase;
  - condutor PE não identificado pela cor verde-amarelo no diagrama.
```

**Justificativa:** PE subdimensionado é risco de segurança direto. Um auditor sem tabela de referência só detecta ausência de PE, não subdimensionamento.

---

### Tarefa 1.3 — Corrigir I-04: Diferenciar Vff por sistema (estrela vs delta)

**Seção alvo:** 9.1  
**Esforço estimado:** 20 min  
**Tipo de alteração:** substituição do bloco "Bifásico FF"

**Substituir o bloco atual "Bifásico FF" por:**

```
Bifásico FF (sistema estrela 220/127 V):

    I = S / 220
    ou
    I = P / (220 × fp)

Bifásico FF (sistema delta 240/120 V):

    I = S / 240
    ou
    I = P / (240 × fp)
```

**Adicionar à lista de incongruências da Seção 9.1:**

```
- usar Vff = 220 V em instalação delta onde Vff correto é 240 V
  (diferença de ~9% na corrente calculada);
- não verificar o tipo de sistema (estrela ou delta) antes de aplicar a tensão de referência.
```

**Justificativa:** o erro de 9% em corrente pode mudar a seleção de disjuntor em uma faixa inteira (ex.: de 50 A para 63 A), alterando a categoria EDP resultante.

---

## Plano de Correção — Onda 2 (Média Prioridade)

**Prazo recomendado:** antes do próximo ciclo de uso em produção ou treinamento  
**Critério de entrada:** conclusão da Onda 1

---

### Tarefa 2.1 — Corrigir I-03: Composição de quedas de tensão na fronteira

**Seção alvo:** 6  
**Esforço estimado:** 15 min  
**Tipo de alteração:** adição de 2 itens à lista existente

**Adicionar como 7º e 8º itens na lista de "incongruências típicas" da Seção 6:**

```
- somar a queda do padrão de entrada (EDP, limite indicativo ~2% sobre a tensão nominal)
  com a queda dos circuitos internos (NBR 5410) sem normalizar pela mesma base de tensão
  e comprimento total, resultando em queda total incorreta;
- declarar apenas a queda do padrão de entrada como "queda total da instalação",
  ignorando a queda acumulada até o ponto mais desfavorável interno
  (NBR 5410 estabelece limites para a queda total: 4% em condições normais;
  verificar limites por tipo de instalação no texto oficial [VERIFICAR]).
```

---

### Tarefa 2.2 — Corrigir I-06: Tornar o Caso 7 numérico e reprodutível

**Seção alvo:** 12 — Caso 7  
**Esforço estimado:** 30 min  
**Tipo de alteração:** substituição completa do Caso 7

**Substituir o Caso 7 atual pelo seguinte:**

```
Caso 7 — Demanda EDP com múltiplos grupos

Instalação: residencial unifamiliar, EDP São Paulo, sistema estrela 220/127 V

Entradas:
  Grupo a — iluminação e TUG:         carga instalada = 3,5 kW
  Grupo b — chuveiro elétrico:         5,4 kW (mínimo Tabela 003 EDP)
  Grupo d — micro-ondas:               1,2 kW (dado de fabricante)
  Grupo f — ar-cond. 12.000 BTU:       1,32 kW (dado de fabricante, FP 1,00 residencial)
  Grupo g — motor bomba d'água (1 CV): 0,74 kW (dados de placa)

Fatores de demanda:
  Grupo a: C = 3,5 kW → faixa (3 < C ≤ 4) → FD = 0,59
  Grupo b: FD = 1,00 (chuveiro — demanda plena sempre)
  Grupo d: FD = 0,70 [VERIFICAR Tabela EDP correspondente]
  Grupo f: FD = 1,00 (residencial)
  Grupo g: FD = 1,00 (maior motor, único)

Demanda por grupo:
  a = 3,5 × 0,59 = 2,065 kW
  b = 5,4 × 1,00 = 5,400 kW
  d = 1,2 × 0,70 = 0,840 kW
  f = 1,32 × 1,00 = 1,320 kW
  g = 0,74 × 1,00 = 0,740 kW

Demanda total = 10,365 kW ≈ 10,37 kVA (assumindo FP = 1,00 médio neste exemplo)

Carga instalada total = 3,5 + 5,4 + 1,2 + 1,32 + 0,74 = 12,16 kW

Conferência:
  Carga instalada > 12 kW em estrela → Categoria D mínima
  Corrente de demanda (bifásico 220 V): I = 10.365 / 220 ≈ 47,1 A
  → Verificar Tabela 001 EDP para subcategoria (D2/D4/D6...) e proteção principal

Nota: FD dos grupos b, d, f, g devem ser verificados nas Tabelas EDP específicas.
[VERIFICAR todos os valores nos documentos oficiais vigentes]
```

---

### Tarefa 2.3 — Corrigir I-08: Referência para fatores de correção de temperatura

**Seção alvo:** 9.2  
**Esforço estimado:** 20 min  
**Tipo de alteração:** adição de bloco após o item "temperatura ambiente"

**Texto a inserir:**

```
Fatores de correção de temperatura (NBR 5410 Tabela 52B ou equivalente) [VERIFICAR versão adotada]:

  Temperatura de referência da tabela de Iz: verificar se é 30 °C (padrão usual).
  Se a temperatura ambiente do local de instalação diferir, verificar aplicação do
  fator de correção correspondente.

  Tipo de isolação afeta temperatura máxima de operação e, portanto, a Iz base:
    PVC:  70 °C máximo na superfície do condutor
    XLPE/EPR: 90 °C máximo

  Incongruência crítica: sistema que usa tabela de Iz para 30 °C em ambiente com
  temperatura ≥ 40 °C sem aplicar fator de correção (Iz superestimada).
```

---

### Tarefa 2.4 — Corrigir I-09: Critérios mínimos de aplicabilidade do DPS

**Seção alvo:** 9.3  
**Esforço estimado:** 30 min  
**Tipo de alteração:** adição de bloco após o item "DPS quando aplicável e sua coordenação"

**Texto a inserir:**

```
DPS — critérios de verificação mínimos
[VERIFICAR NBR 5410 Seção 443 e NBR 5419-4]:

  Fatores que indicam necessidade de DPS:
  - SPDA presente na edificação → DPS interno geralmente obrigatório;
  - alimentação por linha aérea exposta (risco de surto por indução);
  - presença de equipamentos eletrônicos sensíveis (inversores, controladores, TI);
  - número de eventos de raio/ano na região (Nk) declarado no projeto;
  - equipamentos com requisito de continuidade operacional.

  Quando DPS for indicado, verificar:
  - nível de proteção Up compatível com a imunidade dos equipamentos protegidos;
  - corrente de descarga nominal In e máxima Imax;
  - comprimento mínimo e reto do condutor de ligação (reduz indutância);
  - aterramento funcional do DPS;
  - coordenação entre DPS e disjuntor a montante.

  Incongruência crítica: sistema que declara "DPS não necessário" sem apresentar
  análise de risco ou justificativa que sustente a dispensa.
```

---

### Tarefa 2.5 — Corrigir L-01: Declarar escopo do SPDA

**Seção alvo:** E1 (Seção 11) e Seção 18  
**Esforço estimado:** 15 min  
**Tipo de alteração:** substituição de texto + adição na Seção 18

**No E1, substituir** `"existência de SPDA"` **por:**

```
- existência de SPDA: verificar apenas se o sistema declara ou ignora a presença de SPDA.
  A análise completa do SPDA (necessidade, classe de proteção, espaçamento de descidas,
  eletrodos, etc.) está fora do escopo deste prompt e requer NBR 5419-1 a 5419-4.
  Marcar como lacuna de verificação quando SPDA for declarado mas o sistema não indicar
  impacto no DPS interno e no aterramento.
```

**Na Seção 18, adicionar:**

```
- Este prompt não cobre análise de SPDA (NBR 5419). Quando SPDA estiver presente,
  a análise de DPS, aterramento e equipotencialização deve ser complementada com
  os requisitos da NBR 5419-4.
```

---

### Tarefa 2.6 — Corrigir L-02: Declarar escopo da Geração Distribuída

**Seção alvo:** E1 e §8.8, mais Seção 18  
**Esforço estimado:** 15 min  
**Tipo de alteração:** substituição de texto + adição na Seção 18

**No E1 e §8.8, substituir** `"presença de geração distribuída"` **por:**

```
- presença de geração distribuída (GD/GFV/microgeração): verificar apenas se o sistema
  declara ou ignora GD. A análise de GD (proteção anti-ilhamento, medição bidirecional,
  categoria EDP com GD, inversores, ramais) está fora do escopo deste prompt.
  Requer consulta à ANEEL REN 482/2012 e revisões vigentes e ao Padrão EDP específico
  para conexão de microgeração [VERIFICAR versão em vigor na data do projeto].
  Marcar como lacuna de verificação quando GD for declarada mas o sistema não indicar
  impacto na categoria EDP e proteção principal.
```

**Na Seção 18, adicionar:**

```
- Este prompt não cobre dimensionamento de sistemas de geração distribuída (GD/GFV).
  Instalações com microgeração ou minigeração requerem análise adicional conforme
  ANEEL e Padrão EDP de conexão vigente.
```

---

## Plano de Correção — Onda 3 (Baixa Prioridade)

**Prazo recomendado:** versão 3.1, no próximo ciclo de revisão  
**Critério de entrada:** ondas 1 e 2 concluídas e validadas

---

### Tarefa 3.1 — Corrigir I-01: Nota sobre VA (NBR) vs W (EDP)

**Seção alvo:** 8.3  
**Esforço estimado:** 10 min

**Adicionar nota ao final da Seção 8.3:**

```
Nota de auditoria: o critério EDP usa W (potência ativa) para carga instalada de iluminação;
o critério NBR 5410 usa VA (potência aparente) para previsão mínima de iluminação.
Essa diferença de unidade é normativa — não constitui incongruência em si — mas o sistema
auditado deve explicitar qual critério e unidade usa em cada módulo. Verificar se o sistema
mistura as duas unidades sem conversão explícita.
```

---

### Tarefa 3.2 — Corrigir I-05: Referência à cláusula NBR para >6 TUG

**Seção alvo:** 7.3  
**Esforço estimado:** 10 min

**Substituir** `"verificar a regra específica de atribuição mínima conforme texto oficial [VERIFICAR]"` **por:**

```
verificar a regra específica de atribuição mínima conforme NBR 5410:2004+2008,
Seção 9.1.2 (ou cláusula equivalente na versão adotada pelo projeto)
[VERIFICAR no texto oficial vigente].
```

---

### Tarefa 3.3 — Corrigir I-10: Precisão numérica mínima

**Seção alvo:** E14  
**Esforço estimado:** 15 min

**Adicionar ao item "perda de casas decimais" do E14:**

```
Precisão mínima recomendada:
  Corrente (A):              2 casas decimais
  Queda de tensão (%):       2 casas decimais
  Queda de tensão (V):       2 casas decimais
  Potência (VA/kVA/W/kW):    2 casas no resultado final; 3 casas nos cálculos intermediários
  Fator de demanda:          2 casas decimais
  Fator de potência:         2 casas decimais
  Seção de condutor (mm²):   valor normalizado da série comercial
  Resistência (Ω/km):        3 casas decimais

Incongruência a procurar: arredondamento intermediário que altera a seleção do
disjuntor em uma faixa inteira (ex: 24,55 A → 24 A → disjuntor 25 A,
quando o correto seria 32 A para atender Ib ≤ In ≤ Iz com a corrente real).
```

---

### Tarefa 3.4 — Corrigir L-03: Valores de referência PRODIST Módulo 8

**Seção alvo:** 5.3  
**Esforço estimado:** 20 min

**Adicionar ao final da Seção 5.3:**

```
Valores de referência mínimos do PRODIST Módulo 8 [VERIFICAR versão vigente]:

  Fator de potência:
    Consumidores com demanda contratada > 10 kW: FP ≥ 0,92 (indutivo ou capacitivo)
    Medição no ponto de conexão — verificar se o sistema calcula FP no ponto correto.

  Tensão de atendimento (Vref = tensão nominal de referência):
    Adequada:  0,93 × Vref ≤ V ≤ 1,05 × Vref
    Precária:  0,90 × Vref ≤ V < 0,93 × Vref  ou  1,05 × Vref < V ≤ 1,06 × Vref
    Crítica:   V < 0,90 × Vref  ou  V > 1,06 × Vref

  Para 220/127 V (Vref 220 V FF / 127 V FN):
    Adequada:  204,6 V a 231 V (FF) / 118,1 V a 133,4 V (FN)
    Precária:  198 V a 204,6 V (FF)
    Crítica:   < 198 V ou > 233,2 V (FF)

  Incongruência: sistema que exibe "tensão adequada" com queda calculada que coloca
  a tensão no ponto de utilização abaixo de 0,93 × Vref.
```

---

### Tarefa 3.5 — Corrigir L-04: Condutores em paralelo

**Seção alvo:** 9.2  
**Esforço estimado:** 20 min

**Adicionar ao final da Seção 9.2:**

```
Condutores em paralelo [VERIFICAR NBR 5410 texto oficial]:

  Quando o sistema indicar ou permitir condutores em paralelo, verificar:
  - mesma seção, comprimento, material e isolação para todos os condutores paralelos;
  - Iz do conjunto = n × Iz de um condutor individual (com fatores de correção aplicados);
  - proteção dimensionada para o conjunto, não para um único condutor;
  - coerência: sistema que exibe "2×35 mm²" deve calcular Iz como 2 × Iz(35 mm²),
    não como Iz(70 mm²), pois as condições normativas de paralelismo são distintas.
```

---

### Tarefa 3.6 — Adicionar Caso de Teste 8 (Bifásico Categoria D)

**Seção alvo:** 12 — nova entrada após Caso 7  
**Esforço estimado:** 20 min

```
Caso 8 — Instalação bifásica Categoria D

Instalação: residencial/comercial de pequeno porte
Sistema: estrela 220/127 V, bifásico FFN (Categoria D)
Carga instalada total: 14 kW

Conferência:
  Categoria: carga instalada > 12 kW em estrela → Categoria D mínima
  Corrente de demanda (exemplo D = 9 kVA, bifásico 220 V):
    I = 9.000 / 220 = 40,9 A
  Queda de tensão do padrão de entrada (usar fórmula bifásica, Seção 8.10):
    ΔV = 2 × I × l × (Rcat × cosφ + XL × senφ)
  Subcategoria: verificar Tabela 001 EDP conforme demanda e maior motor declarado
```

---

### Tarefa 3.7 — Adicionar Caso de Teste 9 (Condutor PE)

**Seção alvo:** 12 — nova entrada após Caso 8  
**Esforço estimado:** 15 min

```
Caso 9 — Condutor PE em circuito de 6 mm²

Circuito: TUE, condutor de fase 6 mm² cobre
PE mínimo esperado: 6 mm² (regra S ≤ 16 mm² → PE = S)

Conferência:
  Se sistema declarar PE = 2,5 mm²: incongruência de ALTA severidade
  (PE subdimensionado — não atende NBR 5410)
  Se sistema declarar PE = 6 mm²: correto
  Se sistema declarar PE ausente: incongruência CRÍTICA
```

---

## Cronograma Consolidado

| Onda | Tarefas | Esforço total | Prazo sugerido |
|---|---|:---:|---|
| **Onda 1** — Alta prioridade | 1.1, 1.2, 1.3 | ~70 min | D+5 úteis |
| **Onda 2** — Média prioridade | 2.1 a 2.6 | ~125 min | D+10 úteis |
| **Onda 3** — Baixa prioridade | 3.1 a 3.7 | ~110 min | D+20 úteis |
| **Total** | 14 itens + 2 casos novos | **~5 horas** | — |

---

## Impacto por Módulo do Projeto SIE

| Módulo SIE | Tarefas relacionadas | Impacto esperado |
|---|---|---|
| Módulo de corrente elétrica | 1.3, 2.3 | Cálculo bifásico corrigido; erro de 9% eliminado |
| Módulo de queda de tensão | 1.1, 2.1 | Fórmula bifásica + composição NBR×EDP |
| Módulo de condutores | 1.2, 2.4, 3.5 | PE dimensionado corretamente; paralelo coberto |
| Módulo de proteções/DPS | 2.5, 2.6, 3.4 | Critérios DPS explicitados; SPDA/GD declarados |
| Casos de teste / QA | 2.2, 3.6, 3.7 | Regressão numérica para bifásico e PE |
| Documentação / UI | L-01, L-02 | Avisos de escopo na interface |

---

## Checklist Completo de Validação — Versão 3.0

Ao concluir todas as correções das ondas 1 e 2, confirmar:

**Onda 1:**
- [ ] I-02: fórmula bifásica de ΔV adicionada à Seção 8.10 com incongruências associadas
- [ ] I-07: tabela de PE mínimo (fase ≤ 16 / 16–35 / > 35 mm²) adicionada à Seção 9.2
- [ ] I-04: Vff bifásico diferenciado por sistema (220 V estrela / 240 V delta) na Seção 9.1

**Onda 2:**
- [ ] I-03: 2 itens de composição de quedas adicionados à Seção 6
- [ ] I-06: Caso 7 substituído por versão numérica completa na Seção 12
- [ ] I-08: referência a fatores de temperatura (Tabela 52B, PVC/XLPE) adicionada à Seção 9.2
- [ ] I-09: critérios de DPS (SPDA, linha aérea, Nk, Up, In, Imax) adicionados à Seção 9.3
- [ ] L-01: escopo SPDA declarado no E1 e Seção 18
- [ ] L-02: escopo GD declarado no E1, §8.8 e Seção 18

**Onda 3 (versão 3.1):**
- [ ] I-01: nota VA (NBR) vs W (EDP) adicionada à Seção 8.3
- [ ] I-05: referência à Seção 9.1.2 da NBR 5410 adicionada à Seção 7.3
- [ ] I-10: tabela de precisão numérica mínima adicionada ao E14
- [ ] L-03: valores de referência PRODIST Módulo 8 adicionados à Seção 5.3
- [ ] L-04: bloco de condutores em paralelo adicionado à Seção 9.2
- [ ] Caso 8 (bifásico Categoria D) adicionado à Seção 12
- [ ] Caso 9 (PE 6 mm²) adicionado à Seção 12

---

## Pontos Que NÃO Devem Ser Alterados

A análise confirmou que os itens abaixo estão corretos e **não devem ser modificados**:

| Item | Motivo |
|---|---|
| Fórmula de iluminação NBR (Seção 7.1) | Matematicamente correta — floor() aplicado corretamente |
| Fórmula de TUG por perímetro (Seção 7.2) | Divisores 3,5 m e 5 m corretos por tipo de ambiente |
| Fórmula de potência TUG (Seção 7.3) | 600/100 VA com lógica min(N,3) correta |
| Casos de teste 1 a 5 | Todos verificados — valores corretos |
| Tabela de roteamento tipo→parcela EDP (Seção 8.5) | Grupos a–i corretos |
| Tabela de fatores de potência EDP (Seção 8.6) | Valores coerentes com padrão |
| Tabela de fator de demanda grupo a (Seção 8.7) | Faixas e valores corretos |
| Regra de coordenação Ib ≤ In ≤ Iz (Seção 9.2) | Correta e completa |
| Estrutura de eixos E1–E16 (Seção 11) | Abrangente e adequada |
| Hierarquia de referências (Seção 4) | Correta — EDP prevalece sobre NBR para entrada |

---

## Referências Consultadas

| Documento | Código | Versão | Papel |
|---|---|---|---|
| Instalações elétricas de baixa tensão | ABNT NBR 5410 | 2004 + corr. 2008 | Norma principal interna |
| Fornecimento de Energia Elétrica em Tensão Secundária | EDP SP PT.DT.PDN.00068 | V09 (vigente 14/04/2026) | Padrão de concessionária |
| Condições Gerais de Fornecimento | ANEEL REN 1000/2021 | — | Regulatório de apoio |
| Procedimentos de Distribuição | PRODIST Módulo 8 | vigente | Qualidade / FP / tensão |
| Proteção de estruturas contra descargas atmosféricas | ABNT NBR 5419 | partes 1–4 | SPDA (fora do escopo) |
| Microgeração e minigeração distribuída | ANEEL REN 482/2012 e revisões | vigente | GD (fora do escopo) |

---

*Plano elaborado por Atlas (Analyst Agent) — 2026-06-21*  
*Baseado nos artefatos: 02-research-report.md, 03-recommendations.md, 04-sugestoes-correcoes.md, metrics.yaml*  
*— Atlas, investigando a verdade 🔎*
