# Sugestões de Correções — Prompt de Auditoria NBR5410/EDP v2.0

**Documento base:** Prompt_Verificacao_Incongruencias_NBR5410_EDP_v2_complementado.md  
**Data:** 2026-06-21  
**Versão sugerida:** 3.0  

---

## Como usar este documento

Cada item abaixo corresponde a uma inconsistência (I-XX) ou lacuna (L-XX) identificada na análise técnica. Para cada um está descrito: o problema, onde está no prompt atual e o texto ou regra sugerida para correção.

---

## Correções de Inconsistências Internas

---

### [I-01] Clarificar divergência de unidade VA (NBR) vs W (EDP) no próprio prompt

**Seção afetada:** 7.1 e 8.3  
**Problema:** A Seção 7.1 usa VA para previsão NBR de iluminação; a Seção 8.3 usa W para cálculo EDP de carga instalada. O prompt lista "usar W sem tratar VA/fator de potência" como incongruência a detectar no sistema, mas não alerta que o próprio padrão EDP usa W para iluminação enquanto a NBR usa VA.

**Correção sugerida:**

Adicionar nota ao final da Seção 8.3:

```
Nota de auditoria: o critério EDP de carga instalada para iluminação usa W (potência ativa),
enquanto o critério NBR 5410 de previsão mínima usa VA (potência aparente). Essa diferença de
unidade é normativa e não constitui incongruência — mas o sistema auditado deve deixar claro
qual critério e qual unidade está usando em cada módulo. Verifique se o sistema mistura
as duas unidades sem conversão explícita.
```

---

### [I-02] Adicionar fórmula de queda de tensão para circuito bifásico

**Seção afetada:** 8.10  
**Problema:** A Seção 8.10 apresenta fórmulas apenas para monofásico e trifásico. A Categoria D (bifásica FFN) não tem fórmula de referência, deixando lacuna para instalações entre 12–25 kW em estrela ou 12–75 kW em delta.

**Correção sugerida:**

Adicionar o bloco abaixo entre as fórmulas monofásica e trifásica da Seção 8.10:

```
Bifásico FFN (duas fases + neutro):

ΔV = 2 × I × l × (Rcat × cosφ + XL × senφ)

Onde a corrente I é calculada considerando a tensão fase-fase (Vff).
Atenção: verificar se o alimentador bifásico alimenta cargas em 220 V (FF) ou em 127 V (FN).
Para cargas mistas, a queda deve ser calculada separadamente por trecho e tensão [VERIFICAR].
```

Adicionar à lista de incongruências a procurar da Seção 8.10:

```
- fórmula monofásica aplicada a alimentador bifásico (Categoria D) sem distinção;
- tensão FF usada para carga FN ou vice-versa no cálculo bifásico.
```

---

### [I-03] Incluir composição de quedas de tensão na fronteira NBR×EDP

**Seção afetada:** 6  
**Problema:** A Seção 6 lista incongruências típicas de fronteira mas não menciona a necessidade de somar a queda do padrão de entrada (EDP) com a queda interna (NBR 5410) para obter a queda total até o ponto de utilização.

**Correção sugerida:**

Adicionar como 7º item na lista de incongruências típicas da Seção 6:

```
- somar queda do padrão de entrada (EDP, referência ~2% sobre a tensão nominal)
  com a queda dos circuitos internos (NBR 5410) sem normalizar pela mesma base de tensão
  e comprimento, resultando em queda total incorreta ou incomparável com o limite normativo;
- declarar apenas a queda do padrão de entrada como "queda total da instalação",
  ignorando a queda acumulada até o ponto mais desfavorável interno.
```

---

### [I-04] Diferenciar tensão Vff para sistemas estrela vs delta no cálculo de corrente

**Seção afetada:** 9.1  
**Problema:** A Seção 9.1 apresenta `I = S/Vff` para bifásico sem distinguir Vff = 220 V (estrela 220/127 V) vs Vff = 240 V (delta 240/120 V), podendo gerar erro de ~9% na corrente calculada.

**Correção sugerida:**

Substituir o bloco "Bifásico FF" da Seção 9.1 por:

```
Bifásico FF (estrela 220/127 V):

    I = S / 220
    ou
    I = P / (220 × fp)

Bifásico FF (delta 240/120 V):

    I = S / 240
    ou
    I = P / (240 × fp)
```

Adicionar à lista de incongruências da Seção 9.1:

```
- usar Vff = 220 V em instalação delta onde Vff = 240 V (diferença de ~9% na corrente);
- não verificar o sistema de distribuição (estrela ou delta) antes de aplicar a tensão de referência.
```

---

### [I-05] Indicar a cláusula NBR 5410 para a regra de >6 pontos de TUG

**Seção afetada:** 7.3  
**Problema:** O texto menciona "quando o conjunto desses ambientes tiver mais de 6 pontos, verificar a regra específica conforme texto oficial `[VERIFICAR]`" sem indicar onde na NBR 5410 encontrar essa regra.

**Correção sugerida:**

Substituir o trecho citado por:

```
Quando o conjunto desses ambientes (banheiros, cozinhas, copas, copas-cozinhas, áreas de serviço,
lavanderias e análogos) totalizar mais de 6 pontos de TUG, verificar a regra específica de
atribuição mínima conforme NBR 5410:2004+2008, Seção 9.1.2 (ou cláusula equivalente na versão
adotada pelo projeto) [VERIFICAR no texto oficial vigente].
```

---

### [I-06] Tornar o Caso de Teste 7 numérico e reprodutível

**Seção afetada:** 12, Caso 7  
**Problema:** O Caso 7 ("Demanda EDP com múltiplos grupos") é apenas um roteiro sem valores concretos, dificultando comparação entre auditores distintos.

**Correção sugerida:**

Substituir o Caso 7 pelo texto abaixo:

```
Caso 7 — Demanda EDP com múltiplos grupos

Instalação: residencial unifamiliar, EDP São Paulo, sistema estrela 220/127 V

Entradas:
  Grupo a — iluminação e TUG: carga instalada = 3,5 kW
  Grupo b — chuveiro elétrico:  5,4 kW (potência de placa, Tabela 003 EDP como mínimo)
  Grupo d — micro-ondas:        1,2 kW (dado de fabricante)
  Grupo f — ar-cond. 12.000 BTU: 1,32 kW (dado de fabricante, FP 1,00 residencial)
  Grupo g — motor bomba d'água:  0,74 kW (1 CV, dados de placa)

Fatores de demanda:
  Grupo a: C = 3,5 kW → faixa 3 < C ≤ 4 → FD = 0,59
  Grupo b: FD = 1,00 (chuveiro, sempre demanda plena)
  Grupo d: FD = 0,70 [VERIFICAR Tabela EDP aplicável]
  Grupo f: FD = 1,00 (residencial)
  Grupo g: FD = 1,00 (maior motor, único)

Cálculo de demanda por grupo (kW):
  a = 3,5 × 0,59 = 2,065 kW
  b = 5,4 × 1,00 = 5,400 kW
  d = 1,2 × 0,70 = 0,840 kW
  f = 1,32 × 1,00 = 1,320 kW
  g = 0,74 × 1,00 = 0,740 kW

Demanda total (FP médio ponderado ou conversão por grupo):
  D = 2,065 + 5,400 + 0,840 + 1,320 + 0,740 = 10,365 kW

Conversão para kVA (FP = 1,00 assumido para todos os grupos neste exemplo):
  D = 10,365 kVA ≈ 10,37 kVA

Corrente de demanda (monofásico FN 127 V):
  I = 10.365 / 127 ≈ 81,6 A  → indica necessidade de categoria D ou T [VERIFICAR]

Corrente de demanda (bifásico FF 220 V):
  I = 10.365 / 220 ≈ 47,1 A

Verificação:
  Categoria: carga instalada total = 3,5 + 5,4 + 1,2 + 1,32 + 0,74 = 12,16 kW
  → limiar U/D: carga instalada > 12 kW em estrela → Categoria D mínima
  → conferir Tabela 001 para subcategoria e proteção principal adequada

Nota: os FD dos grupos b, d, f, g devem ser conferidos nas Tabelas EDP específicas.
Os valores acima são para referência de verificação. [VERIFICAR nos documentos oficiais]
```

---

### [I-07] Adicionar tabela de dimensionamento mínimo do condutor PE

**Seção afetada:** 9.2  
**Problema:** O item "seção do PE" é listado como verificação obrigatória mas não há tabela de referência, impedindo que o auditor identifique PE subdimensionado sem ter a NBR 5410 em mãos.

**Correção sugerida:**

Adicionar ao final da Seção 9.2, após o item "seção do PE":

```
Seção mínima do condutor PE (NBR 5410, Tabela 54.2 ou equivalente) [VERIFICAR versão adotada]:

  Seção do condutor de fase (S)     →  Seção mínima do PE (condutores de cobre)
  S ≤ 16 mm²                        →  PE = S (igual à fase)
  16 mm² < S ≤ 35 mm²               →  PE = 16 mm²
  S > 35 mm²                        →  PE = S / 2

  Quando PE e neutro têm o mesmo material da fase, usar a tabela acima.
  Quando o PE for de material diferente, a seção equivalente deve ser calculada
  pela resistência elétrica. [VERIFICAR NBR 5410 texto oficial]

Incongruências a procurar:
  - PE com seção menor que a regra acima sem justificativa;
  - PE ausente no diagrama ou memorial;
  - PE com seção igual ao neutro mas inferior ao mínimo da fase;
  - condutor PE não identificado por cor (verde-amarelo) no diagrama.
```

---

### [I-08] Indicar referência para fatores de correção de temperatura dos condutores

**Seção afetada:** 9.2 e E9  
**Problema:** Temperatura ambiente é listada como fator de correção mas nenhum valor de referência é fornecido, exigindo que o auditor localize a tabela NBR externamente.

**Correção sugerida:**

Adicionar ao final do item "temperatura ambiente" na Seção 9.2:

```
Referência: fatores de correção por temperatura ambiente conforme NBR 5410
Tabela 52B (ou equivalente na versão adotada) [VERIFICAR].

Conferência mínima:
  - temperatura de referência da tabela de Iz adotada: verificar se é 30 °C ou outra;
  - temperatura ambiente do local de instalação: declarada ou assumida no projeto;
  - se temperatura ambiente ≠ temperatura de referência da tabela, verificar se o
    sistema aplica o fator de correção correspondente;
  - isolação do condutor (PVC/XLPE/EPR) afeta temperatura máxima de operação e,
    portanto, a Iz base — verificar coerência.

Incongruência crítica: sistema que usa tabela de Iz para 30 °C em ambiente com
temperatura ≥ 40 °C sem aplicar fator de correção.
```

---

### [I-09] Adicionar critérios mínimos de aplicabilidade do DPS

**Seção afetada:** 9.3 e E10  
**Problema:** DPS é mencionado como item de verificação mas sem nenhum critério de quando é obrigatório ou recomendado, deixando a decisão totalmente aberta ao auditor.

**Correção sugerida:**

Adicionar bloco ao final da Seção 9.3, após o item "DPS quando aplicável":

```
DPS — critérios de verificação mínimos [VERIFICAR NBR 5410 Seção 443 e NBR 5419-4]:

  Verificar se o sistema avalia os seguintes fatores para indicar necessidade de DPS:
  - presença de SPDA na edificação (SPDA presente → DPS interno geralmente obrigatório);
  - linha de alimentação aérea exposta (risco de surto por indução);
  - equipamentos eletrônicos sensíveis (computadores, controladores, inversores);
  - declaração do número de eventos de raio por ano na região (Nk);
  - presença de equipamentos com requisito de continuidade operacional.

  Quando DPS for indicado:
  - verificar nível de proteção Up compatível com a imunidade dos equipamentos;
  - verificar corrente de descarga nominal (In) e máxima (Imax);
  - verificar se o condutor de ligação do DPS é curto e reto (indutância mínima);
  - verificar aterramento funcional do DPS;
  - verificar coordenação entre DPS e disjuntor a montante.

  Incongruência crítica: sistema que declara "DPS não necessário" sem apresentar
  a análise de risco que justifica a dispensa.
```

---

### [I-10] Especificar precisão numérica mínima

**Seção afetada:** E14 (Seção 11)  
**Problema:** "Perda de casas decimais" é listada como item a verificar mas sem precisão mínima esperada, gerando critério subjetivo.

**Correção sugerida:**

Adicionar ao item "perda de casas decimais" do E14:

```
Precisão mínima recomendada para auditoria:

  Corrente (A):              2 casas decimais (ex: 24,55 A)
  Queda de tensão (%):       2 casas decimais (ex: 3,42 %)
  Queda de tensão (V):       2 casas decimais (ex: 7,52 V)
  Potência (VA/kVA/W/kW):    3 casas decimais intermediárias; 2 casas no resultado final
  Fator de demanda:          2 casas decimais (ex: 0,59)
  Fator de potência:         2 casas decimais (ex: 0,92)
  Seção de condutor (mm²):   valor normalizado (1,5 / 2,5 / 4 / 6 / 10 / 16 / 25 / 35 mm²)
  Resistência (Ω/km):        3 casas decimais

Incongruência a procurar: arredondamento intermediário que muda a seleção de
disjuntor (ex: 24,55 A arredondado para 24 A → disjuntor 25 A em vez de correto
32 A, dependendo da Iz do condutor).
```

---

## Correções de Lacunas Normativas

---

### [L-01] Declarar escopo do SPDA explicitamente

**Seção afetada:** E1 (Seção 11) e Seção 18  
**Problema:** SPDA é mencionado no E1 como item de verificação mas nenhum critério é fornecido, criando expectativa sem entrega.

**Correção sugerida:**

No E1, substituir "existência de SPDA" por:

```
- existência de SPDA: verificar apenas se o sistema declara ou ignora a presença de SPDA.
  A análise do SPDA em si (necessidade, classe de proteção, espaçamento de descidas,
  eletrodos, etc.) está fora do escopo deste prompt e requer NBR 5419-1 a 5419-4.
  Marcar como lacuna de verificação quando SPDA for declarado mas o sistema não indicar
  impacto no DPS interno e aterramento.
```

Adicionar à Seção 18 (Limitações):

```
Este prompt não cobre análise de SPDA (NBR 5419). Quando SPDA estiver presente,
a análise de DPS, aterramento e equipotencialização deve ser complementada com
os requisitos da NBR 5419-4.
```

---

### [L-02] Declarar escopo da Geração Distribuída explicitamente

**Seção afetada:** E1 e §8.8  
**Problema:** GD é mencionada mas sem critérios, criando expectativa sem entrega.

**Correção sugerida:**

No E1, substituir "presença de geração distribuída" por:

```
- presença de geração distribuída (GD/GFV/microgeração): verificar apenas se o
  sistema declara ou ignora GD. A análise de GD (proteção anti-ilhamento, medição
  bidirecional, categoria EDP com GD, inversores, ramais) está fora do escopo deste
  prompt e requer consulta à ANEEL REN 482/2012 e suas revisões e ao Padrão EDP
  específico para conexão de microgeração [VERIFICAR versão vigente].
  Marcar como lacuna de verificação quando GD for declarada mas o sistema não
  indicar impacto na categoria EDP e proteção principal.
```

Adicionar à Seção 18 (Limitações):

```
Este prompt não cobre dimensionamento de sistemas de geração distribuída (GD/GFV).
Instalações com microgeração ou minigeração requerem análise adicional conforme
ANEEL e Padrão EDP de conexão vigente.
```

---

### [L-03] Adicionar valores de referência do PRODIST Módulo 8

**Seção afetada:** 5.3  
**Problema:** PRODIST é citado como referência de apoio mas sem valores concretos, obrigando o auditor a buscar o módulo externamente para qualquer verificação.

**Correção sugerida:**

Adicionar ao final da Seção 5.3:

```
Valores de referência mínimos do PRODIST Módulo 8 para conferência [VERIFICAR versão vigente]:

  Fator de potência:
    - consumidores com demanda contratada > 10 kW: FP ≥ 0,92 (indutivo ou capacitivo)
    - medição em ponto de conexão; verificar se o sistema calcula FP no ponto correto

  Tensão de atendimento (faixas em relação à tensão nominal de referência Vref):
    Adequada:    0,93 × Vref ≤ V ≤ 1,05 × Vref
    Precária:    0,90 × Vref ≤ V < 0,93 × Vref  ou  1,05 × Vref < V ≤ 1,06 × Vref
    Crítica:     V < 0,90 × Vref  ou  V > 1,06 × Vref

  Para 220/127 V (Vref = 220 V fase-fase / 127 V fase-neutro):
    Adequada:    204,6 V a 231 V (FF) / 118,1 V a 133,4 V (FN)
    Precária:    198 V a 204,6 V (FF) / 114,3 V a 118,1 V (FN)
    Crítica:     < 198 V ou > 233,2 V (FF)

  Incongruência a procurar: sistema que exibe "tensão adequada" com queda calculada
  que coloca a tensão no ponto de utilização abaixo de 0,93 × Vref.
```

---

### [L-04] Mencionar condutores em paralelo como caso especial

**Seção afetada:** 9.2  
**Problema:** A NBR 5410 restringe o uso de condutores em paralelo a casos específicos. Sistemas que dimensionam alimentadores de alta corrente podem usar condutores em paralelo sem validar as condições normativas.

**Correção sugerida:**

Adicionar ao final da Seção 9.2, como item adicional de verificação:

```
Condutores em paralelo [VERIFICAR NBR 5410 texto oficial]:

  Verificar se o sistema permite ou indica condutores em paralelo. Quando presente:
  - condutores em paralelo devem ter mesma seção, mesmo comprimento, mesmo material
    e mesma isolação;
  - cada condutor deve ser dimensionado de forma que, em caso de falha de um, os
    demais possam suportar a corrente sem ultrapassar sua Iz com os fatores de correção;
  - a proteção deve ser compatível com a capacidade real do conjunto;
  - verificar se o sistema divide a corrente corretamente entre os condutores paralelos
    ou se usa apenas a seção de um único condutor para calcular Iz.

  Incongruência: sistema que exibe "condutor 2×35 mm²" mas calcula Iz como se fosse
  1×70 mm² sem verificar as condições normativas de paralelismo.
```

---

## Sugestão de Nova Seção: Casos de Teste Adicionais

Incluir como Caso 8 e Caso 9 na Seção 12:

---

### Caso 8 — Instalação bifásica Categoria D

```
Instalação: residencial com demanda média
Sistema: estrela 220/127 V, bifásico (FFN)
Carga instalada total: 14 kW

Conferência:
  Categoria mínima: D (carga instalada > 12 kW em estrela)
  Corrente de demanda (exemplo com D = 9 kVA):
    I = 9.000 / 220 = 40,9 A (bifásico FF)
  Subcategoria EDP: verificar Tabela 001 conforme demanda e maior motor
  Queda de tensão do padrão de entrada (bifásico):
    ΔV = 2 × I × l × (Rcat × cosφ + XL × senφ) [usar fórmula bifásica]
```

---

### Caso 9 — Condutor PE em circuito de 6 mm²

```
Condutor de fase: 6 mm² cobre
PE mínimo esperado: 6 mm² (S ≤ 16 mm² → PE = S)

Conferência:
  PE declarado no sistema: [observar]
  PE correto: 6 mm²
  Incongruência se sistema declarar PE de 2,5 mm² sem justificativa.
```

---

## Checklist de Aplicação das Correções

Para validar a versão 3.0 do prompt após as correções:

- [ ] I-01: nota sobre VA vs W adicionada à Seção 8.3
- [ ] I-02: fórmula bifásica de queda de tensão adicionada à Seção 8.10
- [ ] I-03: item de composição de quedas adicionado à Seção 6
- [ ] I-04: tensão Vff diferenciada por sistema (estrela/delta) na Seção 9.1
- [ ] I-05: referência à cláusula NBR 5410 para regra de >6 pontos na Seção 7.3
- [ ] I-06: Caso 7 substituído por versão com valores numéricos concretos
- [ ] I-07: tabela de dimensionamento mínimo do PE adicionada à Seção 9.2
- [ ] I-08: referência a fatores de correção de temperatura adicionada à Seção 9.2
- [ ] I-09: critérios mínimos de DPS adicionados à Seção 9.3
- [ ] I-10: precisão numérica mínima especificada no E14
- [ ] L-01: escopo do SPDA declarado explicitamente no E1 e Seção 18
- [ ] L-02: escopo da GD declarado explicitamente no E1 e Seção 18
- [ ] L-03: valores de referência do PRODIST Módulo 8 adicionados à Seção 5.3
- [ ] L-04: condutores em paralelo adicionados à Seção 9.2
- [ ] Caso 8 (bifásico Categoria D) adicionado à Seção 12
- [ ] Caso 9 (PE 6 mm²) adicionado à Seção 12

---

*Gerado em 2026-06-21 com base na análise técnica do prompt NBR5410/EDP v2.0.*
