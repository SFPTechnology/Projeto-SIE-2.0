# Relatório Técnico — Análise do Prompt de Auditoria NBR5410/EDP v2.0

**Data:** 2026-06-21  
**Documento analisado:** Prompt_Verificacao_Incongruencias_NBR5410_EDP_v2_complementado.md  
**Versão do documento:** 2.0 complementada  

---

## 1. Verificação de Fórmulas e Casos de Teste

Todos os 5 casos de teste foram verificados matematicamente. Resultado: **CORRETOS**.

### 1.1 Caso 1 — Quarto 3×3 m

| Grandeza | Fórmula | Resultado prompt | Recálculo | Status |
|---|---|---:|---:|---|
| Iluminação | 100 + 60×floor((9-6)/4) | 100 VA | 100 VA | ✓ CORRETO |
| Nº TUG | teto(12/5) | 3 pontos | 3 pontos | ✓ CORRETO |
| Potência TUG | 3×100 | 300 VA | 300 VA | ✓ CORRETO |

### 1.2 Caso 2 — Sala 3×4 m

| Grandeza | Fórmula | Resultado prompt | Recálculo | Status |
|---|---|---:|---:|---|
| Iluminação | 100 + 60×floor((12-6)/4) | 160 VA | 160 VA | ✓ CORRETO |
| Nº TUG | teto(14/5) | 3 pontos | 3 pontos | ✓ CORRETO |
| Potência TUG | 3×100 | 300 VA | 300 VA | ✓ CORRETO |

### 1.3 Caso 3 — Cozinha 3×4 m

| Grandeza | Fórmula | Resultado prompt | Recálculo | Status |
|---|---|---:|---:|---|
| Iluminação | 100 + 60×floor((12-6)/4) | 160 VA | 160 VA | ✓ CORRETO |
| Nº TUG | teto(14/3,5) | 4 pontos | 4 pontos | ✓ CORRETO |
| Potência TUG | 3×600 + 1×100 | 1.900 VA | 1.900 VA | ✓ CORRETO |

### 1.4 Caso 4 — Banheiro 2×1,5 m

| Grandeza | Fórmula | Resultado prompt | Recálculo | Status |
|---|---|---:|---:|---|
| Iluminação | S≤6 → 100 VA | 100 VA | 100 VA | ✓ CORRETO |
| Nº TUG | mínimo 1 ponto | 1 ponto | 1 ponto | ✓ CORRETO |
| Potência TUG | 1×600 | 600 VA | 600 VA | ✓ CORRETO |

### 1.5 Caso 5 — Chuveiro 5.400 W / 220 V

| Grandeza | Fórmula | Resultado prompt | Recálculo | Status |
|---|---|---:|---:|---|
| Corrente 220V | 5400/220 | 24,55 A | 24,55 A | ✓ CORRETO |
| Corrente 127V | 5400/127 | 42,52 A | 42,52 A | ✓ CORRETO |

---

## 2. Inconsistências Internas Identificadas

### I-01 — Unidade VA vs W: NBR interna × EDP padrão de entrada [MÉDIA]

**Local:** Seção 7.1 vs Seção 8.3  
**Observação [FATO]:** A Seção 7.1 usa VA para previsão de iluminação NBR. A Seção 8.3 (cálculo de carga instalada EDP) menciona "100 W por ponto de luz". O prompt lista "usar W sem tratar VA/fator de potência" como incongruência a procurar (§7.1), mas não alerta explicitamente sobre esta diferença de unidade entre o critério EDP (W) e o critério NBR (VA) no próprio texto do prompt.  
**Impacto:** Auditor pode não identificar que sistema usa W para iluminação EDP e VA para iluminação NBR — comportamento esperado, mas não documentado no prompt.

### I-02 — Fórmula de queda de tensão para circuito bifásico ausente [ALTA]

**Local:** Seção 8.10  
**Observação [FATO]:** O padrão EDP V09 tem Categoria D (bifásica FFN). A Seção 8.10 apresenta apenas as fórmulas para circuito monofásico e trifásico. Não há fórmula para bifásico.  
**Referência esperada:** Para bifásico, a fórmula de queda depende do arranjo (fase-neutro com dois condutores = similar à monofásica; entre fases = diferente). O prompt deveria incluir `[VERIFICAR]` explícito para este caso.  
**Impacto:** Auditor pode aplicar fórmula monofásica a alimentador bifásico sem perceber a lacuna.

### I-03 — Lista de incongruências típicas na fronteira NBR×EDP incompleta [MÉDIA]

**Local:** Seção 6  
**Observação [INFERÊNCIA]:** A seção lista 6 incongruências típicas de fronteira mas omite a composição de quedas de tensão: queda do padrão de entrada (EDP, máx ~2%) + queda interna (NBR 5410, máx 4% condições normais / 7% desfavorável). Um sistema que calcula as quedas separadamente sem somar pode gerar resultado tecnicamente inválido.  
**Impacto:** Lacuna na cobertura do eixo E11.

### I-04 — Tensão de referência bifásica não diferenciada por sistema (estrela vs delta) [MÉDIA]

**Local:** Seção 9.1  
**Observação [FATO]:** A Seção 9.1 apresenta `I = S/Vff` para bifásico sem distinguir Vff = 220 V (estrela) vs Vff = 240 V (delta). A Seção 8.1 declara ambos os sistemas. Sem a distinção, auditor pode não checar qual Vff o sistema usa.  
**Impacto:** Erro de corrente de até ~9% ((240-220)/220) em instalações delta.

### I-05 — Seção 7.3: regra para >6 pontos no conjunto de ambientes com apenas [VERIFICAR] [BAIXA]

**Local:** Seção 7.3  
**Observação [DÚVIDA]:** O texto menciona "quando o conjunto desses ambientes tiver mais de 6 pontos, verificar a regra específica conforme texto oficial `[VERIFICAR]`". Correto manter como [VERIFICAR], mas sem mais contexto o auditor não sabe o que procurar. Seria útil indicar a cláusula da NBR 5410 correspondente.  
**Impacto:** Baixo — apenas orientação ao auditor.

### I-06 — Caso de teste 7 (demanda EDP) incompleto [MÉDIA]

**Local:** Seção 12, Caso 7  
**Observação [FATO]:** O Caso 7 ("Demanda EDP com múltiplos grupos") propõe montar uma amostra mas não fornece valores numéricos concretos. Diferente dos Casos 1-5, que têm dados e conferência explícita, o Caso 7 é apenas um roteiro. Auditores diferentes podem montar amostras diferentes e produzir resultados incomparáveis.  
**Impacto:** Reduz reprodutibilidade da auditoria para o módulo de demanda EDP.

### I-07 — Seção 9.2: seção mínima do condutor PE sem tabela de referência [ALTA]

**Local:** Seção 9.2  
**Observação [FATO]:** O item "seção do PE" está listado como verificação obrigatória mas não há tabela de dimensionamento do PE. A NBR 5410 Seção 54 (ou equivalente) define regras específicas. O prompt deveria ao menos fornecer a regra simplificada:  
- PE ≥ fase quando fase ≤ 16 mm²  
- PE ≥ fase/2 quando fase > 35 mm²  
- [VERIFICAR] para faixas intermediárias  
**Impacto:** Auditor pode não identificar PE subdimensionado.

### I-08 — Fatores de correção de temperatura de condutores sem referência numérica [MÉDIA]

**Local:** Seção 9.2 e E9  
**Observação [FATO]:** Temperatura ambiente é listada como fator de correção mas nenhum valor é fornecido. Sistema que usa fatores incorretos de temperatura não pode ser auditado sem a tabela NBR.  
**Impacto:** Lacuna no eixo E9 — auditor precisa ter a NBR em mãos para verificar.

### I-09 — DPS: ausência de critérios mínimos de aplicabilidade [MÉDIA]

**Local:** Seção 9.3 e E10  
**Observação [FATO]:** DPS é mencionado como item de verificação mas sem critérios de quando é obrigatório. A NBR 5410 Seção 443 e a NBR 5419-4 definem as condições. O prompt não fornece parâmetros — apenas `[VERIFICAR]` implícito.  
**Impacto:** Auditores podem divergir sobre exigibilidade de DPS em determinadas instalações.

### I-10 — Precisão numérica mínima não especificada [BAIXA]

**Local:** Seção 14 (E14)  
**Observação [INFERÊNCIA]:** O prompt menciona "perda de casas decimais" como item do E14 mas não especifica precisão mínima aceitável para correntes (A), quedas de tensão (%) e potências (VA/kVA).  
**Impacto:** Arredondamentos que alteram seleção de disjuntor podem não ser detectados.

---

## 3. Lacunas Normativas

### L-01 — SPDA (NBR 5419) [MÉDIA]

O prompt menciona SPDA no E1 mas não fornece critérios de análise. A presença ou ausência de SPDA afeta diretamente a necessidade de DPS (NBR 5410 Seção 534) e os condutores de aterramento. O escopo do SPDA deveria ser declarado como fora do escopo do prompt ou como `[VERIFICAR NBR 5419]`.

### L-02 — Geração Distribuída [MÉDIA]

Mencionada no E1 e §8.8 sem critérios. Sistemas com GFV afetam: proteção anti-ilhamento, medição bidirecional, categoria EDP, ramal de entrada. O prompt deveria declarar explicitamente que GD está fora do escopo ou indicar ANEEL REN 482/2012 (ou revisão vigente) como referência.

### L-03 — PRODIST Módulo 8: limites de tensão e FP [BAIXA]

O §5.3 menciona PRODIST mas sem valores. Quando um sistema exibe "tensão de atendimento adequada" ou "fator de potência conforme", o auditor precisa dos limites do PRODIST (ex: FP ≥ 0,92 indutivo para consumidores com demanda > 10 kW). A ausência de valores obriga o auditor a buscar o PRODIST externamente.

### L-04 — Circuitos em paralelo e limitações de associação [BAIXA]

A NBR 5410 tem restrições específicas para condutores em paralelo. O prompt não menciona este caso, que pode ocorrer em alimentadores de alta corrente em instalações comerciais/industriais.

---

## 4. Pontos de Excelência do Prompt

1. **Estrutura de 16 eixos de varredura (E1–E16)** — cobertura sistemática que previne omissões.
2. **Casos de teste com cálculo explícito** — permite verificação aritmética imediata.
3. **Hierarquia de evidências [FATO]/[INFERÊNCIA]/[DÚVIDA]** — controle de qualidade epistêmico.
4. **Separação clara de fronteira NBR×EDP** — reduz o principal vetor de erro em sistemas de dimensionamento.
5. **Formato de relatório prescrito** — garante auditabilidade por terceiros.
6. **Seção 8.5: tabela de roteamento tipo→parcela EDP** — elimina ambiguidade no agrupamento.
7. **Checklist final §17** — 36 itens explícitos para verificação de completude.

---

## 5. Avaliação de Completude

| Módulo normativo | Cobertura no prompt |
|---|---|
| NBR 5410 — previsão de cargas residencial | Alta |
| NBR 5410 — dimensionamento de condutores | Média (sem tabelas de Iz) |
| NBR 5410 — proteções | Média (sem tabelas de coordenação) |
| NBR 5410 — DR | Alta (critérios mencionados) |
| NBR 5410 — DPS | Baixa (apenas menção) |
| NBR 5410 — aterramento/equipotencialização | Média |
| EDP PT.DT.PDN.00068 V09 — demanda | Alta |
| EDP — categorias U/D/T | Alta |
| EDP — Tabelas 001/002 | Alta (com ressalva de PDF) |
| EDP — motores | Alta |
| EDP — queda de tensão entrada | Alta (exceto bifásico) |
| SPDA / NBR 5419 | Baixa (apenas menção) |
| GD / microgeração | Baixa (apenas menção) |
| PRODIST Módulo 8 | Baixa (sem valores) |

---

## 6. Conclusão

O prompt é um framework de auditoria robusto e tecnicamente rigoroso para o escopo declarado (instalações BT até 75 kW, EDP SP, sistema aéreo, unidade individual). As fórmulas e casos de teste estão corretos. As 10 inconsistências identificadas são de severidade baixa a alta mas nenhuma invalida o framework — são oportunidades de refinamento para a versão 3.0.

**Confiabilidade aparente do prompt:** alta  
**Veredicto:** apto para uso como ferramenta de auditoria, com as ressalvas documentadas nas Seções 2 e 3.
