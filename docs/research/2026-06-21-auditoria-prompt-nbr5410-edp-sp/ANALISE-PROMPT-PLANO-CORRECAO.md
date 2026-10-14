# Auditoria do Prompt de Verificação NBR 5410 / EDP SP — Plano de Correção Completo

**Analista:** Atlas (AIOX Analyst)  
**Data:** 2026-06-21  
**Branch:** `feature/nbr5410-conformidade-closeout`  
**Arquivo de entrada:** `Prompt_Verificacao_Incongruencias_NBR5410_EDP_v2_complementado.md`  
**Sistema auditado:** `sistema-de-instala-es-el-tricas-sie-main`

---

## 1. RESUMO EXECUTIVO

### 1.1 Escopo da análise

Esta análise cruzou o **prompt de auditoria técnica** (v2.0, 2026-06-21) contra o **código-fonte e dados internos do SIE**, usando os seguintes artefatos:

| Artefato | Tipo | Observação |
|---|---|---|
| `Prompt_Verificacao_Incongruencias_NBR5410_EDP_v2_complementado.md` | Prompt-guia de auditoria | Referência principal de conferência |
| `REFERENCIA-INTEGRAL-SISTEMA.md` | Documentação do sistema | Consolidação dos módulos e tabelas |
| `src/domain/distribuidora/edp-sp/grupos-demanda.ts` | Código-fonte | Definição dos grupos a–i |
| `src/domain/distribuidora/edp-sp/tipos-aparelho.ts` | Código-fonte | Classificação tipo → grupo + FP |
| `src/domain/distribuidora/edp-sp/categorias-fornecimento.data.json` | Dado | Categorias U, D, T |
| `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json` | Dado | Subcategorias U2, D2…T10 |
| `src/domain/distribuidora/edp-sp/fatores-potencia.data.json` | Dado | FP por tipo de aparelho |
| `src/domain/distribuidora/edp-sp/tabela_005.data.json` | Dado | Fator de demanda grupo a |
| `src/domain/distribuidora/edp-sp/seletor-categoria.ts` | Código-fonte | Lógica de seleção U/D/T |
| `src/domain/distribuidora/edp-sp/motor-demanda.ts` | Código-fonte | Motor de demanda por grupo |
| `src/domain/calculo/padrao-entrada.ts` | Código-fonte | Seleção de padrão de entrada genérico |

### 1.2 Normas de referência

- **ABNT NBR 5410:2004** (versão corrigida 2008) — instalações internas  
- **EDP São Paulo PT.DT.PDN.00068 v09** — vigente desde 14/04/2026 (substituiu PT.DT.PDN.03.14.020 v06)  
- ANEEL REN nº 1000/2021 — referência regulatória de apoio

### 1.3 Totais encontrados

| Severidade | Quantidade |
|---|---:|
| CRÍTICA | 4 |
| ALTA | 6 |
| MÉDIA | 5 |
| BAIXA | 3 |
| **Total** | **18** |

### 1.4 Módulos mais críticos

1. **Referência normativa EDP** — todos os arquivos de dado declaram v06, mas o padrão vigente é v09 (desde 14/04/2026)
2. **Seleção de categoria U/D/T** — simplificada apenas por carga instalada; padrão exige carga + demanda + tipo de rede + local
3. **Documentação de grupos EDP** (`REFERENCIA-INTEGRAL-SISTEMA.md`) — seção 7.1 descreve grupos incorretamente, divergindo do código real
4. **Hidromassagem** — FP único de 0.80 para toda a carga, ignorando tratamento separado de resistência (FP=1.00) e motor

### 1.5 Confiabilidade técnica aparente

> **Moderada.** O código-fonte tem lógica de grupos e FP majoritariamente corretos para a v06. O risco principal é a desatualização para v09 e as simplificações na seleção de categoria, que podem gerar dimensionamento e subcategoria EDP incorretos em projetos reais.

### 1.6 Veredito técnico

> **Apto somente para estudo** — enquanto o sistema referenciar v06 e enquanto as subcategorias U2/D2/T2+ não forem efetivamente usadas no fluxo de cálculo principal. Não declarar "aprovado para uso real" sem migração completa para v09, validação técnica da tabela de subcategorias, e testes com responsável técnico habilitado.

---

## 2. MATRIZ PRINCIPAL DE INCONGRUÊNCIAS

| ID | Severidade | Eixo | Tipo | Módulo/Arquivo | Evidência observada | Referência esperada | Incongruência | Impacto técnico | Status |
|---|---|---|---|---|---|---|---|---|---|
| I-01 | CRÍTICA | E1 | norma / arquitetura | todos os `.data.json` EDP | `"versao_norma": "v06"` / `"fonte": "PT.DT.PDN.03.14.020 v06"` | EDP São Paulo PT.DT.PDN.00068 v09 (vigente desde 14/04/2026) | Sistema declara referência ao padrão v06, substituído pelo v09 há mais de 2 meses | Todas as tabelas e fatores podem estar desatualizados sem que o sistema avise | confirmada |
| I-02 | CRÍTICA | E7 | classificação / norma | `categorias-fornecimento.data.json`, `seletor-categoria.ts` | Categoria selecionada apenas por carga instalada (0–12 kW = U, 12–25 = D, 25–75 = T) | V09 define categorias por "carga instalada, demanda, tipo de rede e local" | Sistema reduz regra multidimensional a uma única variável (carga instalada) | Pode gerar categoria errada (ex: instalação com demanda alta mas carga instalada baixa) | confirmada |
| I-03 | CRÍTICA | E14 | arquitetura / rastreabilidade | `REFERENCIA-INTEGRAL-SISTEMA.md` seção 7.1 | Documenta c=ferro elétrico, d=boiler, e=sauna | Código real: b=ferro elétrico, c=boiler+sauna, d=secadora+forno+micro-ondas | Documentação de referência ativa diverge do código; qualquer desenvolvedor ou auditor que leia o REFERENCIA terá mapeamento errado de grupos | Decisões técnicas tomadas com base no REFERENCIA usarão grupo errado | confirmada |
| I-04 | CRÍTICA | E6 | segurança / norma | `fatores-potencia.data.json`, `tipos-aparelho.ts` | `hidromassagem: fp=0.80`, uma única entrada | V09 seção 8.6: "hidromassagem — resistência → FP=1.00" e "hidromassagem — motor → conforme tabela de motores" | Sistema não desagrega hidromassagem em resistência e motor; usa FP 0.80 para toda a carga | Potência aparente e demanda da hidromassagem sub ou superdimensionadas | confirmada |
| I-05 | ALTA | E1 | arquitetura | `subcategorias-fornecimento.catalogo.data.json` vs `subcategorias-fornecimento.data.json` | REFERENCIA cita `subcategorias-fornecimento.data.json`; arquivo real é `subcategorias-fornecimento.catalogo.data.json` | Referência documental correta ao arquivo de código existente | Documentação aponta para arquivo diferente do real; risco de manutenção errada | Manutentor pode editar arquivo incorreto sem perceber | confirmada |
| I-06 | ALTA | E7 | arquitetura / rastreabilidade | `categorias-fornecimento.data.json` | U: min=0, max=12; D: min=12, max=25 — sobreposição no limite 12 kW | Fronteira única: 12 kW pertence a uma única categoria (sem sobreposição) | Ambiguidade no modelo de dados: 12 kW satisfaz tanto U quanto D; código resolve por ordenação de array | Frágil: qualquer reordenação ou adição de categoria quebra a regra silenciosamente | confirmada |
| I-07 | ALTA | E1 | norma / usabilidade | Todos os arquivos de dado EDP exceto subcategorias | Versão declarada: v06 | Versão vigente: v09 (14/04/2026) | Sistema não emite alerta sobre uso de padrão desatualizado ao usuário ou ao engenheiro | Usuário não sabe que está operando com norma antiga | confirmada |
| I-08 | ALTA | E7 | classificação | `tipos-aparelho.ts` — `tue_generico: grupo "a"` | TUE genérico classificado no grupo `a` (iluminação/TUG) | V09 seção 8.4 e tabela 8.5: TUE é tomada de uso específico e pode pertencer a grupos `d`, `f`, `g`, `h` conforme tipo real | Classificar TUE genérico em `a` subestima demanda quando o equipamento real pertence a grupo com fator de demanda diferente | Demanda EDP subdimensionada para equipamentos TUE do tipo forno, AR, motor etc. | confirmada |
| I-09 | ALTA | E2 | cálculo / norma | `seletor-categoria.ts` (comentário inline) | Comentário: "Fronteira inclusiva no topo: 12.0 cai em U, 12.0001 cai em D" | O comportamento do loop depende da **ordem** das categorias no array JSON, não de uma regra explícita de precedência | Implementação frágil — correta acidentalmente por ordenação, não por design | Qualquer refatoração que altere a ordem do array inverte a fronteira U/D silenciosamente | confirmada |
| I-10 | ALTA | E7 | cálculo | `motor-demanda.ts` / `seletor-subcategoria.ts` | Corrente bifásica: `I = DT_VA / V_FF` | Para sistema bifásico (FFN) em estrela 220/127 V, corrente de linha = DT_VA / V_FF quando cargas são FF; mas cargas FN em um ramal bifásico têm tratamento diferente | Sistema acumula D1_VA (mono) e D3_VA (tri) sem desagregar bifásico como entidade separada | Corrente de demanda bifásica pode ser imprecisa quando mistura cargas FN e FF | potencial |
| I-11 | MÉDIA | E13 | usabilidade técnica | Interface geral do sistema | Sistema não exibe versão do padrão EDP em uso ao usuário | V09 seção 13: "o sistema mostra norma e versão?" — deve ser afirmativo | Ausência de declaração visível de qual versão do padrão está sendo aplicada | Auditor externo não consegue verificar conformidade normativa do cálculo | confirmada |
| I-12 | MÉDIA | E7 | cálculo / tabela | `fatores-potencia.data.json` | `iluminacao_fluorescente_t5: fp=0.95` | V09 tabela 8.6: "iluminação fluorescente, neon, vapor de sódio/mercúrio sem declaração → 0.55" | FP de 0.95 para fluorescente T5 diverge do default normativo EDP de 0.55; pode ser justificável tecnicamente mas precisa ser declarado e documentado | Demanda do grupo `a` subdimensionada quando há iluminação fluorescente T5 | potencial |
| I-13 | MÉDIA | E9 | completude | `REFERENCIA-INTEGRAL-SISTEMA.md` seções 8.5–8.10 | Sistema não implementa módulos de condutor/proteção/DR/DPS/queda de tensão para circuitos terminais | Mapa de completude E16: condutores → proteção → DR/DPS → queda de tensão devem ser implementados | Módulos críticos de segurança ausentes — sistema para antes de completar a cadeia de dimensionamento | Projeto incompleto não pode ser usado para execução | confirmada |
| I-14 | MÉDIA | E11 | completude | Fluxo de cálculo | Queda de tensão não calculada para circuitos nem para padrão de entrada | V09 seção 8.10 e NBR 5410 seção 9: queda de tensão obrigatória | Ausência total de cálculo de queda de tensão | Não é possível verificar se circuitos terminais e ramal de entrada atendem aos limites normativos | confirmada |
| I-15 | MÉDIA | E12 | completude | Sistema geral | Memorial, diagrama unifilar e lista de materiais ausentes ou placeholder | Mapa E16: quadro de cargas → memorial → diagrama → lista devem ser rastreáveis | Artefatos finais de projeto não gerados | Sistema não produz documentação de projeto utilizável | confirmada |
| I-16 | BAIXA | E13 | usabilidade técnica | `REFERENCIA-INTEGRAL-SISTEMA.md` e documentação geral | Fórmulas documentadas em `F-03` a `F-09` com status `VERIFICAR`, sem fonte primária confirmada | Cada fórmula deve ter referência ao item exato da NBR 5410:2004 confirmado | Rastreabilidade normativa incompleta — "VERIFICAR" sem data, responsável ou evidência de conferência | Dificulta auditoria por terceiro | confirmada |
| I-17 | BAIXA | E13 | usabilidade técnica | `catálogo-fornecimento.data.json` genérico | Status geral: "VERIFICAR" — padrão de entrada genérico não específico a nenhuma concessionária | Padrão de entrada deve ser derivado do padrão oficial da distribuidora aplicável | Sistema oferece padrão genérico sem vincular à distribuidora do projeto | Usuário pode selecionar padrão incompatível com sua concessionária | confirmada |
| I-18 | BAIXA | E3 | classificação | `catalog.data.json` — categorias de dependência | Sistema suporta: dormitório, sala, hall-corredor, cozinha, área de serviço, banheiro, varanda, área externa | NBR 5410 prevê também: copa, copa-cozinha, lavanderia, garagem, escritório, ambiente técnico | Conjunto de tipos de dependência incompleto | Usuários de imóveis com copa-cozinha ou lavanderia separada usam tipos incorretos, com regra de TUG errada | potencial |

---

## 3. DETALHAMENTO POR INCONGRUÊNCIA

### I-01 — Versão do padrão EDP desatualizada (v06 → v09)

```text
ID: I-01
Título: Todos os arquivos de dado EDP referenciam PT.DT.PDN.03.14.020 v06
Severidade: CRÍTICA
Eixo: E1 — Escopo, premissas e aplicabilidade normativa
Tipo: norma / arquitetura
Status: confirmada
Local no sistema: tabela_005.data.json, tabela_007–015.data.json, 
                  categorias-fornecimento.data.json, fatores-potencia.data.json,
                  fatores-demanda.ts (tipo literal hardcoded na interface)
Evidência observada:
  - tabela_005.data.json linha 5: "fonte": "EDP São Paulo PT.DT.PDN.03.14.020 v06"
  - categorias-fornecimento.data.json linha 2: mesma referência
  - fatores-potencia.data.json linha 2: mesma referência
  - fatores-demanda.ts linha 54: tipo literal hardcoded "EDP São Paulo PT.DT.PDN.03.14.020 v06"
  - subcategorias-fornecimento.catalogo.data.json linha 2: "fonte": "EDP São Paulo PT.DT.PDN.00068 v09" (correto)
Classificação da evidência: [FATO]
Referência normativa/técnica esperada:
  EDP São Paulo PT.DT.PDN.00068 v09
  Vigência: 14/04/2026
  URL: https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf
Descrição da incongruência:
  O padrão técnico EDP São Paulo foi substituído em 14/04/2026 
  (PT.DT.PDN.00068 v09 substitui PT.DT.PDN.03.14.020 v06). O sistema 
  continua declarando o padrão antigo em todos os arquivos de dado, exceto 
  no catálogo de subcategorias que já foi atualizado. Essa divergência interna 
  (subcategorias em v09, demais em v06) indica migração incompleta.
Impacto técnico:
  - As tabelas de fatores de demanda (005, 007–015) podem ter valores 
    desatualizados em relação ao v09
  - O campo "fonte" e "versao_norma" no tipo TypeScript é um literal fixo, 
    impedindo compilação correta se os dados forem atualizados para v09
  - O sistema não avisa o usuário sobre qual versão está aplicando
Artefatos afetados: todos os .data.json EDP, fatores-demanda.ts
Dados necessários para confirmação adicional:
  Comparação direta das tabelas 005, 007–015 entre v06 e v09 para confirmar
  se os valores numéricos mudaram.
```

---

### I-02 — Seleção de categoria U/D/T simplificada

```text
ID: I-02
Título: Categoria EDP selecionada apenas por carga instalada, ignorando demanda, tipo de rede e local
Severidade: CRÍTICA
Eixo: E7 — Demanda EDP
Tipo: classificação / norma
Status: confirmada
Local no sistema: seletor-categoria.ts, categorias-fornecimento.data.json
Evidência observada:
  seletor-categoria.ts linhas 12–17: comentário declara
  "(≤12 U; 12–25 D; 25–75 T)" como regra única
  A função recebe apenas (carga_instalada_kW, tem_trifasica) — sem demanda, 
  sem tipo_rede, sem localidade.
Classificação da evidência: [FATO]
Referência normativa/técnica esperada:
  V09 seção 8.2: "os tipos de fornecimento são definidos em função da 
  carga instalada, demanda, tipo de rede e local da unidade consumidora"
Descrição da incongruência:
  O padrão EDP V09 exige avaliação multidimensional para classificação U/D/T.
  O sistema ignora:
  - Demanda calculada (que pode diferir da carga instalada)
  - Tipo de rede (aérea ou subterrânea — afeta disponibilidade de categorias)
  - Tipo de local (urbano/rural)
  - Restrições de maior motor por categoria
Cálculo reproduzido:
  Exemplo: instalação com carga_instalada = 10 kW (→ U pelo sistema), 
  mas com 1 motor trifásico de 7,5 CV: o maior motor ultrapassa o limite 
  da categoria U2 (1 CV FN); o sistema não detecta a incompatibilidade.
Impacto técnico:
  - Categoria resultante pode ser insuficiente para os equipamentos do projeto
  - Maior motor não é validado contra os limites das Tabelas 001/002
  - Tipo de rede não é coletado, impossibilitando validação completa
```

---

### I-03 — REFERENCIA-INTEGRAL-SISTEMA.md documenta grupos EDP incorretamente

```text
ID: I-03
Título: Documentação de referência ativa descreve mapeamento de grupos EDP errado
Severidade: CRÍTICA
Eixo: E14 — Arquitetura, contratos e integridade do motor
Tipo: arquitetura / rastreabilidade
Status: confirmada
Local no sistema: REFERENCIA-INTEGRAL-SISTEMA.md seção 7.1
Evidência observada:
  REFERENCIA-INTEGRAL-SISTEMA.md seção 7.1:
    c → "Ferro elétrico"
    d → "Boiler"
    e → "Sauna"
  
  Código real (grupos-demanda.ts DESCRICAO_GRUPO):
    b → "Chuveiro, torneira elétrica, aquecedor de passagem, ferro elétrico"
    c → "Boiler (aquecedor central/acumulação), sauna"
    d → "Secadora, forno elétrico, lava-louça, lava-roupa, micro-ondas"
    e → "Fogão elétrico"
  
  Código real (tipos-aparelho.ts CLASSIFICACAO_APARELHO):
    ferro_eletrico.grupo = "b"  ✓ correto
    boiler.grupo = "c"  ✓ correto
    sauna.grupo = "c"  ✓ correto
Classificação da evidência: [FATO]
Referência normativa/técnica esperada:
  V09 Prompt seção 8.4 e 8.5:
    b → chuveiros, torneiras elétricas, aquecedores de passagem, ferros elétricos
    c → aquecedor central/acumulação, boiler, sauna
    d → secadora, forno elétrico, lava-louça, lava-roupa, micro-ondas
    e → fogões elétricos
Descrição da incongruência:
  A documentação central do sistema (REFERENCIA-INTEGRAL-SISTEMA.md) contém
  mapeamento de grupos EDP completamente diferente do código real.
  O código implementa os grupos corretamente; a documentação está errada.
  Qualquer desenvolvedor, QA ou auditor que use o REFERENCIA como fonte de
  verdade tomará decisões com base em informação incorreta.
Impacto técnico:
  - Manutenções guiadas pelo REFERENCIA classificarão cargas no grupo errado
  - Auditoria de conformidade baseada no documento de referência falhará
  - Onboarding de novos desenvolvedores introduzirá bugs de classificação
```

---

### I-04 — Hidromassagem com FP único (resistência + motor não desagregados)

```text
ID: I-04
Título: Hidromassagem classificada com FP=0.80 único, sem separar resistência (FP=1.00) e motor
Severidade: CRÍTICA
Eixo: E6 — TUE, cargas fixas e equipamentos
Tipo: cálculo / norma / segurança
Status: confirmada
Local no sistema: fatores-potencia.data.json linha 33, tipos-aparelho.ts linha 267–273
Evidência observada:
  fatores-potencia.data.json: { "tipo": "hidromassagem", "fp": 0.80 }
  tipos-aparelho.ts: hidromassagem.grupo = "i", fp_default = 0.8
Classificação da evidência: [FATO]
Referência normativa/técnica esperada:
  V09 Prompt seção 8.6:
    "hidromassagem — resistência → FP=1.00"
    "hidromassagem — motor → conforme tabela de motores"
  V09 Prompt seção 8.4:
    grupo i = "hidromassagem — resistência + motor da bomba"
Cálculo reproduzido:
  Hidromassagem 5.000 W total (ex: 3.500 W resistência + 1.500 W motor FP=0.75):
  
  Sistema atual:
    S = 5.000 / 0.80 = 6.250 VA
  
  Correto (desagregado):
    S_resistência = 3.500 / 1.00 = 3.500 VA
    S_motor = 1.500 / 0.75 = 2.000 VA
    S_total = 5.500 VA
  
  Diferença: sistema superdimensiona potência aparente em +13,6%
Impacto técnico:
  - Demanda do grupo i superestimada
  - Corrente de demanda superestimada
  - Pode elevar categoria EDP desnecessariamente
  - Condutor e disjuntor do circuito de hidromassagem superdimensionados
```

---

### I-05 — Documentação aponta para arquivo de subcategorias inexistente

```text
ID: I-05
Título: REFERENCIA cita subcategorias-fornecimento.data.json, mas o arquivo real é subcategorias-fornecimento.catalogo.data.json
Severidade: ALTA
Eixo: E14 — Arquitetura
Tipo: rastreabilidade / arquitetura
Status: confirmada
Local no sistema: REFERENCIA-INTEGRAL-SISTEMA.md seção 7.5
Evidência observada:
  REFERENCIA cita: "src/domain/distribuidora/edp-sp/subcategorias-fornecimento.data.json"
  Arquivo real: "src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json"
  (Confirmado via listagem do diretório — o .data.json simples não existe)
Impacto técnico:
  Manutentor que seguir o REFERENCIA tentará editar arquivo inexistente.
```

---

### I-06 — Fronteira ambígua U/D a 12 kW no modelo de dados

```text
ID: I-06
Título: categorias-fornecimento.data.json tem U.max = D.min = 12 kW (sobreposição)
Severidade: ALTA
Eixo: E7 — Demanda EDP
Tipo: arquitetura / cálculo
Status: confirmada
Local no sistema: categorias-fornecimento.data.json, seletor-categoria.ts
Evidência observada:
  U: { carga_instalada_min_kW: 0, carga_instalada_max_kW: 12 }
  D: { carga_instalada_min_kW: 12, carga_instalada_max_kW: 25 }
  Código usa >= e <= em ambas as extremidades → 12.0 satisfaz tanto U quanto D.
  Código resolve pelo primeiro match no array (U vem antes de D).
  Comentário seletor-categoria.ts linha 17: "12.0 cai em U, 12.0001 cai em D"
Classificação da evidência: [FATO]
Impacto técnico:
  - Regra de fronteira é implícita (depende de ordenação do JSON)
  - Qualquer refatoração que reordene o array inverte o comportamento
  - Não há teste que valide explicitamente o comportamento na fronteira exata
Correção recomendada: usar < no limite superior (carga < 12 → U, 12 ≤ carga < 25 → D)
```

---

### I-07 — Sistema não alerta sobre uso de padrão desatualizado

```text
ID: I-07
Título: Ausência de alerta ao usuário sobre uso do padrão EDP v06 (substituído em 14/04/2026)
Severidade: ALTA
Eixo: E1
Tipo: usabilidade técnica / norma
Status: confirmada
Local no sistema: Interface geral; nenhum ponto de aviso detectado
Impacto técnico:
  Engenheiro realiza cálculo sem saber que está usando norma desatualizada.
  Em projetos protocolados após 14/04/2026 com base no v06, há risco de 
  reprovação pela concessionária.
```

---

### I-08 — TUE genérico classificado no grupo a (iluminação/TUG)

```text
ID: I-08
Título: tue_generico roteado para grupo a independente do tipo real de equipamento
Severidade: ALTA
Eixo: E7 — Demanda EDP / E6 — TUE
Tipo: classificação / norma
Status: confirmada
Local no sistema: tipos-aparelho.ts linha 133–140
Evidência observada:
  tue_generico: { grupo: "a", fp_default: 1.0, fp_obrigatorio_declarar: false }
Referência esperada:
  Prompt seção 8.5 (roteamento): TUE deve ir ao grupo correspondente ao 
  tipo real de equipamento (ex: TUE para AC → grupo f; TUE para motor → g).
  Grupo a deve conter apenas iluminação e TUG.
Impacto técnico:
  - AR-condicionado cadastrado como TUE genérico vai para grupo a com FD de 0.24 (pior caso)
    em vez de grupo f com FD=1.0
  - Pode subestimar ou superestimar demanda dependendo do equipamento real
  - Não há mecanismo que impeça classificação genérica para equipamentos com grupo próprio
```

---

### I-09 — Fronteira U/D resolvida por ordenação de array implícita

```text
ID: I-09
Título: Regra de fronteira U/D a 12 kW dependente da ordenação do JSON, sem regra explícita
Severidade: ALTA
Eixo: E7
Tipo: arquitetura / cálculo
Status: confirmada
(Detalhado como extensão do I-06 — ver I-06)
```

---

### I-10 — Corrente bifásica potencialmente imprecisa

```text
ID: I-10
Título: Corrente de demanda bifásica calculada como DT_VA / V_FF sem desagregar cargas FN e FF
Severidade: ALTA
Eixo: E8 — Corrente elétrica
Tipo: cálculo
Status: potencial
Local no sistema: seletor-subcategoria.ts (fórmula I = DT_VA / V_FF para bi)
Evidência observada:
  REFERENCIA seção 8.8: "bi → I_A = DT_VA / V_FF"
  Motor de demanda acumula D1_VA (mono/fase única) + D3_VA (tri) em DT_VA.
Classificação da evidência: [INFERÊNCIA]
Referência esperada:
  Para sistema bifásico FFN estrela 220/127 V, cargas FN usam 127 V e 
  cargas FF usam 220 V. A corrente de demanda por fase deve considerar 
  o roteamento das cargas entre as fases.
Dados necessários para confirmação:
  Leitura completa de seletor-subcategoria.ts para verificar exatamente 
  como DT_VA é calculado e se D1_VA inclui cargas FN e FF misturadas.
```

---

### I-11 — Versão da norma não exibida ao usuário

```text
ID: I-11
Título: Interface não exibe qual versão do padrão EDP está sendo aplicada
Severidade: MÉDIA
Eixo: E13 — Usabilidade técnica
Tipo: usabilidade técnica
Status: confirmada
Impacto: Impede auditoria por terceiro; engenheiro não sabe qual norma está usando.
```

---

### I-12 — FP da fluorescente T5 diverge do default EDP

```text
ID: I-12
Título: iluminacao_fluorescente_t5 com FP=0.95, contra default EDP de 0.55 para fluorescentes
Severidade: MÉDIA
Eixo: E7 / E4
Tipo: cálculo / tabela
Status: potencial
Local: fatores-potencia.data.json, tipos-aparelho.ts
Evidência: fp=0.95 declarado para fluorescente_t5
Referência: V09 Prompt seção 8.6: "iluminação fluorescente sem declaração → 0.55"
Classificação: [DÚVIDA] — T5 com capacitor de correção pode justificar FP≥0.90;
  mas a justificativa deve estar documentada e o usuário deve ser avisado.
Impacto: Demanda de iluminação fluorescente pode ser subdimensionada se FP real for 0.55.
```

---

### I-13 — Módulos de condutor, proteção, DR/DPS e queda de tensão ausentes

```text
ID: I-13
Título: Cadeia de dimensionamento incompleta — módulos de segurança ausentes
Severidade: MÉDIA (pois o sistema é declarado parcial, mas deve ser documentado)
Eixo: E9, E10, E11, E16 — Completude
Tipo: completude
Status: confirmada
Módulos ausentes: condutores, proteções, DR, DPS, queda de tensão (parcial e total)
Impacto: Sistema não pode ser usado para execução de projeto elétrico real.
```

---

### I-16 — Fórmulas NBR marcadas como VERIFICAR sem rastreabilidade de confirmação

```text
ID: I-16
Título: F-03 a F-09 com status "VERIFICAR" sem evidência de confirmação
Severidade: BAIXA
Eixo: E16
Tipo: rastreabilidade
Status: confirmada
```

---

## 4. CONFERÊNCIAS NUMÉRICAS

### 4.1 Tabela 005 EDP-SP — Fator de demanda grupo a

| Carga (kW) | Fator no sistema | Fator esperado (Prompt seção 8.7) | Status |
|---:|---:|---:|---|
| ≤ 1 | 0.86 | 0.86 | ✓ Conforme |
| ≤ 2 | 0.75 | 0.75 | ✓ Conforme |
| ≤ 3 | 0.66 | 0.66 | ✓ Conforme |
| ≤ 4 | 0.59 | 0.59 | ✓ Conforme |
| ≤ 5 | 0.52 | 0.52 | ✓ Conforme |
| ≤ 6 | 0.45 | 0.45 | ✓ Conforme |
| ≤ 7 | 0.40 | 0.40 | ✓ Conforme |
| ≤ 8 | 0.35 | 0.35 | ✓ Conforme |
| ≤ 9 | 0.31 | 0.31 | ✓ Conforme |
| ≤ 10 | 0.27 | 0.27 | ✓ Conforme |
| > 10 | 0.24 | 0.24 | ✓ Conforme |

> Observação: os valores são idênticos entre v06 e os do prompt (que referencia o V09). Necessário confirmar no PDF do V09 se as faixas mudaram. [VERIFICAR]

### 4.2 Casos de teste NBR 5410 — Fórmulas de iluminação e TUG

| Caso | Ambiente | Área (m²) | Perímetro (m) | Iluminação sistema (fórmula F-08) | Iluminação esperada (Prompt) | Status |
|---|---|---:|---:|---|---|---|
| 1 | Quarto 3×3 | 9 | 12 | 100 + 60 × floor((9-6)/4) = 100 VA | 100 VA | ✓ Conforme |
| 2 | Sala 3×4 | 12 | 14 | 100 + 60 × floor((12-6)/4) = 160 VA | 160 VA | ✓ Conforme |
| 3 | Cozinha 3×4 | 12 | 14 | 160 VA | 160 VA | ✓ Conforme |
| 4 | Banheiro 2×1,5 | 3 | 7 | 100 VA | 100 VA | ✓ Conforme |

| Caso | Ambiente | Categoria | Divisor | TUG sistema | TUG esperada | Potência sistema | Potência esperada | Status |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Quarto | CAT-A | 5 | ceil(12/5)=3 | 3 | 300 VA | 300 VA | ✓ Conforme |
| 2 | Sala | CAT-A | 5 | ceil(14/5)=3 | 3 | 300 VA | 300 VA | ✓ Conforme |
| 3 | Cozinha | CAT-B | 3,5 | ceil(14/3,5)=4 | 4 | min(4,3)×600 + max(0,1)×100 = 1.900 VA | 1.900 VA | ✓ Conforme |
| 4 | Banheiro | CAT-B | — | 1 (mínimo fixo) | 1 | 600 VA | 600 VA | ✓ Conforme |

**Conclusão:** As fórmulas NBR de iluminação e TUG estão implementadas corretamente no código.

### 4.3 Fatores de potência EDP-SP — conferência mínima

| Tipo | FP sistema | FP esperado (Prompt 8.6) | Divergência | Status |
|---|---:|---:|---|---|
| iluminacao_incandescente | 1.00 | 1.00 | — | ✓ |
| iluminacao_descarga | 0.55 | 0.55 | — | ✓ |
| iluminacao_fluorescente_t5 | 0.95 | 0.55 (sem declaração) | **+0.40** | ⚠️ potencial (I-12) |
| tug | 1.00 | 1.00 | — | ✓ |
| chuveiro | 1.00 | 1.00 | — | ✓ |
| ferro_eletrico | 1.00 | 1.00 | — | ✓ |
| boiler / sauna | 1.00 | 1.00 | — | ✓ |
| secadora | 0.80 | 0.80 | — | ✓ |
| forno_eletrico | 1.00 | 1.00 | — | ✓ |
| lava_loucas / lava_roupas | 0.80 | 0.80 | — | ✓ |
| micro_ondas | 0.80 | 0.80 | — | ✓ |
| fogao_eletrico | 1.00 | 1.00 | — | ✓ |
| ar_condicionado | 1.00 | 1.00 (residencial) | — | ✓ |
| motor | 0.80 | conforme Tab.016/017 [VERIFICAR] | genérico | ⚠️ potencial |
| hidromassagem | 0.80 | resistência=1.00 + motor=tabela | **não desagrega** | ❌ I-04 |

---

## 5. BALANÇO ROTEAMENTO TIPO → GRUPO EDP

| Tipo | Grupo sistema | Grupo esperado (Prompt 8.5) | Status |
|---|---|---|---|
| iluminacao_* | a | a | ✓ |
| tug | a | a | ✓ |
| tue_generico | a | grupo do equipamento real (d, f, g…) | ❌ I-08 |
| chuveiro | b | b | ✓ |
| torneira_eletrica | b | b | ✓ |
| aquecedor_passagem | b | b | ✓ |
| ferro_eletrico | b | b | ✓ |
| boiler | c | c | ✓ |
| sauna | c | c | ✓ |
| secadora | d | d | ✓ |
| forno_eletrico | d | d | ✓ |
| lava_loucas | d | d | ✓ |
| lava_roupas | d | d | ✓ |
| micro_ondas | d | d | ✓ |
| fogao_eletrico | e | e | ✓ |
| ar_condicionado | f | f | ✓ |
| motor | g | g | ✓ |
| maquina_solda_motor | g | g | ✓ |
| raio_x | h | h | ✓ |
| solda_transformador | h | h | ✓ |
| forno_arco | h | h | ✓ |
| hidromassagem | i | i | ✓ (mas FP incorreto — I-04) |

---

## 6. MAPA DE COMPLETUDE (E16)

| Etapa | Implementado? | Resultado rastreável? | Saída nula/placeholder? | Divergência com etapa anterior | Observação |
|---|---|---|---|---|---|
| Cadastro de ambientes | Sim | Sim | Não | — | 8 tipos; conjunto incompleto (I-18) |
| Cálculo de área/perímetro | Sim | Sim | Não | — | Assume retangular |
| Iluminação | Sim | Sim | Não | — | Fórmulas corretas |
| TUG | Sim | Sim | Não | — | Fórmulas corretas |
| TUE/cargas fixas | Parcial | Parcial | — | tue_generico no grupo errado | I-08 |
| Demanda EDP | Sim | Sim | Não | Versão v06 | I-01 |
| Categoria U/D/T | Sim (simplificada) | Parcial | Não | Ignora demanda/rede/local | I-02 |
| Subcategoria (U2, D2…) | Implementado no catálogo | Não integrado ao fluxo principal | Pendência `SUBCAT_TABELAS_001_002_AUSENTES` | Catálogo existe mas não flui | [VERIFICAR integração] |
| Circuitos | Ausente | — | Placeholder | — | I-13 |
| Correntes de circuito | Ausente | — | Placeholder | — | I-13 |
| Condutores | Ausente | — | Placeholder | — | I-13 |
| Proteções | Ausente | — | Placeholder | — | I-13 |
| DR/DPS | Ausente | — | Placeholder | — | I-13 |
| Queda de tensão | Ausente | — | Placeholder | — | I-14 |
| Balanceamento de fases | Implementado | Parcial | Não | — | LPT implementado |
| Aterramento | Ausente | — | Placeholder | — | I-13 |
| Quadro de cargas | Ausente | — | Placeholder | — | I-15 |
| Diagrama unifilar | Ausente | — | Placeholder | — | I-15 |
| Memorial | Ausente | — | Placeholder | — | I-15 |
| Lista de materiais | Ausente | — | Placeholder | — | I-15 |

---

## 7. VERIFICAÇÃO DE TABELAS INTERNAS

| Tabela do sistema | Fonte declarada | Versão | Referência correta | Divergência | Impacto | Status |
|---|---|---|---|---|---|---|
| tabela_005 (FD grupo a) | PT.DT.PDN.03.14.020 v06 | v06 | PT.DT.PDN.00068 v09 | Fonte desatualizada | [VERIFICAR] se valores mudaram em v09 | I-01 |
| tabela_007–015 (FD grupos b–i) | PT.DT.PDN.03.14.020 v06 | v06 | PT.DT.PDN.00068 v09 | Fonte desatualizada | [VERIFICAR] | I-01 |
| fatores-potencia | PT.DT.PDN.03.14.020 v06 | v06 | PT.DT.PDN.00068 v09 | Fonte desatualizada + FP T5 divergente | Potencial subdimensionamento | I-01, I-12 |
| categorias-fornecimento | PT.DT.PDN.03.14.020 v06 | v06 | PT.DT.PDN.00068 v09 | Simplificação de critério de categoria | Categoria pode estar errada | I-01, I-02 |
| subcategorias-fornecimento.catalogo | PT.DT.PDN.00068 v09 | v09 | Correto | Inconsistente com demais tabelas | — | I-01 (parcial) |
| catalogo-fornecimento (genérico) | — | — | Padrão real da distribuidora | Genérico sem vinculação à concessionária | Padrão de entrada pode ser incompatível | I-17 |

---

## 8. SÍNTESE FINAL

### 8.1 Contagem por eixo

| Eixo | Incongruências |
|---|---:|
| E1 — Escopo/aplicabilidade normativa | 3 (I-01, I-07, I-17) |
| E7 — Demanda EDP | 4 (I-02, I-06, I-08, I-10) |
| E14 — Arquitetura/integridade | 2 (I-03, I-05) |
| E6 — TUE/cargas fixas | 1 (I-04) |
| E13 — Usabilidade técnica | 2 (I-07, I-11) |
| E16 — Completude | 3 (I-13, I-14, I-15) |
| E9/E10/E11 — Condutor/proteção/QT | 1 (I-13) |
| E3 — Classificação de ambientes | 1 (I-18) |
| E4/E12 — Iluminação/tabelas | 1 (I-12, I-16) |

### 8.2 Contagem por severidade

| Severidade | Quantidade | IDs |
|---|---:|---|
| CRÍTICA | 4 | I-01, I-02, I-03, I-04 |
| ALTA | 6 | I-05, I-06, I-07, I-08, I-09, I-10 |
| MÉDIA | 5 | I-11, I-12, I-13, I-14, I-15 |
| BAIXA | 3 | I-16, I-17, I-18 |

### 8.3 Três incongruências mais graves

1. **I-01** — Sistema declara padrão EDP v06, substituído pelo v09 em 14/04/2026, sem aviso ao usuário. Toda a cadeia de tabelas pode estar desatualizada.
2. **I-02** — Seleção de categoria U/D/T baseada apenas em carga instalada, ignorando demanda, tipo de rede e local — simplificação que pode gerar categoria incorreta e erro na seleção do padrão de entrada.
3. **I-03** — Documentação central (`REFERENCIA-INTEGRAL-SISTEMA.md`) descreve grupos EDP completamente errados, criando risco sistêmico de erro em manutenções e auditorias.

### 8.4 Módulos mais frágeis

1. **Seleção de categoria EDP** — simplificada, fronteira ambígua, sem coleta de tipo de rede
2. **Hidromassagem** — FP não desagregado
3. **TUE genérico** — roteamento para grupo `a` independente do equipamento real
4. **Referência normativa EDP** — inconsistente internamente (v06 e v09 misturados)

---

## 9. PLANO DE CORREÇÃO COMPLETO

> Este plano está organizado por prioridade técnica (CRÍTICA → ALTA → MÉDIA → BAIXA) e indica os artefatos a modificar, a ação específica e o critério de aceitação.

---

### FASE 1 — CRÍTICAS (bloqueadoras para uso em produção)

#### C-01: Migrar referência normativa de v06 para v09

**Contexto:** O padrão EDP São Paulo foi substituído em 14/04/2026. Projetos protocolados após essa data devem usar o V09.

**Ações:**

| # | Artefato | Ação |
|---|---|---|
| 1 | `tabela_005.data.json` e tabelas 007–015 | Verificar valores numéricos no PDF V09. Se iguais: atualizar `fonte` e `versao_norma`. Se diferentes: atualizar valores + metadados. |
| 2 | `categorias-fornecimento.data.json` | Atualizar `fonte` e `versao_norma`; revisar faixas de carga instalada conforme V09 |
| 3 | `fatores-potencia.data.json` | Atualizar `fonte` e `versao_norma`; verificar se FPs mudaram em V09 |
| 4 | `fatores-demanda.ts` | Remover o tipo literal hardcoded `"EDP São Paulo PT.DT.PDN.03.14.020 v06"` da interface `TabelaFatorDemanda`; tornar campo `fonte` e `versao_norma` strings genéricas ou criar enum expansível |
| 5 | `grupos-demanda.ts` | Atualizar comentário JSDoc da linha 1 para V09 |
| 6 | `tipos-aparelho.ts` | Atualizar comentário da linha 76 para V09 |

**Critério de aceitação:** todos os arquivos `.data.json` EDP declaram `"versao_norma": "v09"` e `"fonte": "EDP São Paulo PT.DT.PDN.00068 v09"`. Nenhum literal v06 no código de produção.

---

#### C-02: Corrigir documentação de grupos EDP no REFERENCIA-INTEGRAL-SISTEMA.md

**Artefato:** `REFERENCIA-INTEGRAL-SISTEMA.md` seção 7.1

**Ação:** Corrigir tabela de grupos EDP para:

```markdown
| `a` | Iluminação, TUG, TUE genérico |
| `b` | Chuveiro, torneira elétrica, aquecedor de passagem, ferro elétrico |
| `c` | Boiler (aquecedor central/acumulação), sauna |
| `d` | Secadora, forno elétrico, lava-louça, lava-roupa, micro-ondas |
| `e` | Fogão elétrico |
| `f` | Ar-condicionado |
| `g` | Motor elétrico, máquina de solda a motor |
| `h` | Equipamento especial (raio-X, solda a transformador, forno a arco) |
| `i` | Hidromassagem |
```

**Critério de aceitação:** `REFERENCIA-INTEGRAL-SISTEMA.md` seção 7.1 é idêntica ao `DESCRICAO_GRUPO` em `grupos-demanda.ts`.

---

#### C-03: Desagregar hidromassagem em resistência + motor

**Artefato:** `tipos-aparelho.ts`, `fatores-potencia.data.json`, banco de dados

**Ações:**

| # | Ação |
|---|---|
| 1 | Criar dois tipos: `hidromassagem_resistencia` (grupo `i`, FP=1.00) e `hidromassagem_motor` (grupo `i`, FP conforme tabela de motores) |
| 2 | Ou: adicionar campo `componentes` à carga do tipo `hidromassagem` com sub-cargas de resistência e motor |
| 3 | Atualizar `fatores-potencia.data.json` com os dois FPs distintos |
| 4 | Adicionar migration SQL se necessário para suportar o novo campo no banco |
| 5 | Atualizar o motor de demanda para calcular S de cada componente separadamente |

**Critério de aceitação:** Cálculo de demanda do grupo `i` usa FP=1.00 para a parcela resistiva e FP de tabela de motores para a parcela motora.

---

#### C-04: Expandir seleção de categoria U/D/T para incluir tipo de rede e maior motor

**Artefato:** `seletor-categoria.ts`, `categorias-fornecimento.data.json`, UI

**Ações:**

| # | Ação |
|---|---|
| 1 | Adicionar campo `tipo_rede` ao projeto (`aerea` / `subterranea`) |
| 2 | Adicionar campo `maior_motor_cv` (ou calcular a partir das cargas) |
| 3 | Atualizar `seletor-categoria.ts` para validar maior motor contra os limites das Tabelas 001/002 por categoria candidata |
| 4 | Adicionar validação: se maior motor excede limite da categoria calculada, emitir alerta ou elevar categoria |
| 5 | Documentar que tipo de rede subterrânea pode exigir padrão próprio não coberto pelo V09 aéreo |

**Critério de aceitação:** `selecionarCategoria` aceita `tipo_rede` e `maior_motor_cv` como parâmetros; emite `DiagnosticoMaiorMotor` quando motor ultrapassa limite da categoria.

---

### FASE 2 — ALTAS

#### A-01: Corrigir fronteira U/D a 12 kW no modelo de dados

**Artefato:** `categorias-fornecimento.data.json`

**Ação:** Adotar convenção `[min, max)` — fronteira superior exclusiva:
```json
{ "id": "U", "carga_instalada_min_kW": 0,  "carga_instalada_max_kW_exclusivo": 12 }
{ "id": "D", "carga_instalada_min_kW": 12, "carga_instalada_max_kW_exclusivo": 25 }
{ "id": "T", "carga_instalada_min_kW": 25, "carga_instalada_max_kW_exclusivo": 75 }
```
Atualizar `seletor-categoria.ts` para usar `< max_exclusivo` em vez de `<= max`.

**Critério de aceitação:** 12.0 kW resulta em D (não U). Teste unitário explícito na fronteira exata.

---

#### A-02: Adicionar alerta de versão normativa desatualizada (v06)

**Artefato:** Interface do usuário / API

**Ação:** Emitir `DiagnosticoVersaoNorma` com severidade `ALERTA` quando o sistema detectar que está usando dados com `versao_norma: "v06"` em projetos criados após 14/04/2026.

**Critério de aceitação:** Usuário vê aviso explícito: "Este projeto usa dados do padrão EDP v06, substituído em 14/04/2026 pelo V09. Resultado pode diferir do padrão vigente."

---

#### A-03: Resolver TUE genérico — forçar classificação por tipo real

**Artefato:** `tipos-aparelho.ts`, UI de cadastro de cargas adicionais

**Ação:**
- Remover `tue_generico` ou torná-lo apenas um rótulo de UI, não um tipo de classificação EDP
- Ao cadastrar TUE, exigir seleção do tipo real (chuveiro, AR, motor, forno etc.)
- Se tipo real não for informado: emitir `DiagnosticoTUEsemClassificacao` e usar grupo `a` como fallback conservador, com aviso explícito

**Critério de aceitação:** `tue_generico` não pode ser cadastrado sem seleção de tipo real, ou gera alerta visível de classificação conservadora.

---

#### A-04: Corrigir nome do arquivo de subcategorias no REFERENCIA

**Artefato:** `REFERENCIA-INTEGRAL-SISTEMA.md` seção 7.5

**Ação:** Substituir referência a `subcategorias-fornecimento.data.json` por `subcategorias-fornecimento.catalogo.data.json`.

---

#### A-05: Integrar catálogo de subcategorias ao fluxo principal de cálculo

**Artefato:** `motor-edp-sp.ts`, `seletor-subcategoria.ts`

**Contexto:** O arquivo `subcategorias-fornecimento.catalogo.data.json` já existe com dados V09 (U2, D2, D4, D6, D7, D9, D10, T2, T4, T6, T7, T9, T10), mas o motor retorna pendência `SUBCAT_TABELAS_001_002_AUSENTES`.

**Ação:**
- Conectar `seletor-subcategoria.ts` ao catálogo existente
- Selecionar subcategoria pela corrente de demanda calculada vs `corrente_demanda_max_A` do catálogo
- Expor `disjuntor_A`, `condutor_entrada_*`, `eletroduto_entrada_mm`, `aterramento_*mm2` no resultado

**Critério de aceitação:** Motor EDP retorna subcategoria (ex: U2, D4) com disjuntor e condutor de entrada preenchidos, sem pendência `SUBCAT_TABELAS_001_002_AUSENTES`.

---

#### A-06: Verificar FP da fluorescente T5

**Artefato:** `fatores-potencia.data.json`, `tipos-aparelho.ts`

**Ação:**
- Consultar Tabela EDP V09 sobre FP de iluminação fluorescente T5 com correto de FP
- Se V09 aceitar FP≥0.90 para T5 com capacitor: documentar a justificativa no arquivo
- Se V09 exigir 0.55 sem declaração: corrigir para 0.55 e marcar `fp_obrigatorio_declarar: true`

---

### FASE 3 — MÉDIAS

#### M-01: Exibir versão da norma EDP na interface

**Ação:** Adicionar rodapé ou cabeçalho no relatório/tela com: "Padrão EDP aplicado: [versao_norma]"

---

#### M-02: Implementar módulos de segurança ausentes

**Prioridade interna (sugerida para próximas sprints):**

| Módulo | Dependências | Estimativa de complexidade |
|---|---|---|
| Corrente de projeto por circuito | cargas, tensão, ligação | Média |
| Dimensionamento de condutor | corrente, método, temp., agrupamento | Alta |
| Proteções (disjuntor, curva, Icn) | condutor, Ib, Iz | Alta |
| DR por ambiente | tipo de ambiente, zona | Média |
| DPS | análise de sobretensão | Alta |
| Queda de tensão (parcial + total) | comprimento, seção, FP | Média |
| Quadro de cargas | todos os anteriores | Alta |
| Diagrama unifilar | quadro + aterramento | Alta |
| Memorial descritivo | todos | Alta |
| Lista de materiais | condutor + proteção + DR + DPS | Média |

---

#### M-03: Expandir tipos de dependência

**Artefato:** `catalog.data.json`

**Ação:** Adicionar: `copa`, `copa-cozinha`, `lavanderia`, `garagem`, `escritório`, `sala-servidores`, `ambiente-técnico`

---

### FASE 4 — BAIXAS

#### B-01: Confirmar fórmulas F-03 a F-09 e remover status VERIFICAR

**Ação:** Para cada fórmula F-03 a F-09 em `catalog.data.json`, verificar o item exato da NBR 5410:2004, documentar a referência completa e alterar `status: "verificado"`.

---

#### B-02: Vincular catálogo genérico de padrões de entrada à concessionária

**Ação:** Adicionar campo `concessionaria` ao projeto e bloquear/avisar quando `catálogo-fornecimento.data.json` genérico for usado em vez do padrão específico da distribuidora.

---

## 10. CHECKLIST DE VERIFICAÇÃO DO PROMPT (Seção 17)

| Item | Status no sistema | Referência |
|---|---|---|
| ☑ Escopo normativo declarado | PARCIAL — v06 em vez de v09 | I-01 |
| ☑ EDP São Paulo × outra concessionária | EDP SP implementada | — |
| ☑ Versão PT.DT.PDN.00068 V09 | NÃO — usa v06 | I-01 |
| ☑ Unidade individual × coletiva | Unidade individual (implícito) | I-17 |
| ☑ Rede aérea × subterrânea | NÃO coletado | I-02 |
| ☑ Limite de 75 kW | Implementado | — |
| ☑ Sistema estrela 220/127 × delta 240/120 | Apenas 220/127 | [VERIFICAR] |
| ☑ Iluminação NBR | ✓ Implementado corretamente | — |
| ☑ TUG por ambiente | ✓ Implementado corretamente | — |
| ☑ TUG × TUE | PARCIAL — tue_generico no grupo errado | I-08 |
| ☑ Cargas fixas | PARCIAL | I-13 |
| ☑ Motores | PARCIAL — sem alerta de motor > 5 CV | [VERIFICAR] |
| ☑ Equipamentos especiais | Grupo h implementado | — |
| ☑ Demanda a+b+c+d+e+f+g+h+i | ✓ Implementado | — |
| ☑ Fatores de potência | PARCIAL — hidromassagem e T5 divergentes | I-04, I-12 |
| ☑ Fatores de demanda | ✓ Implementado (v06) | I-01 |
| ☑ Tabelas EDP 001 e 002 | PARCIAL — catálogo existe, não integrado | A-05 |
| ☑ Corrente mono/bi/tri | ✓ Implementado | — |
| ☑ Condutores | NÃO implementado | I-13 |
| ☑ Proteções | NÃO implementado | I-13 |
| ☑ DR | NÃO implementado | I-13 |
| ☑ DPS | NÃO implementado | I-13 |
| ☑ Aterramento | NÃO implementado | I-13 |
| ☑ Queda de tensão | NÃO implementado | I-14 |
| ☑ Quadro de cargas | NÃO implementado | I-15 |
| ☑ Memorial | NÃO implementado | I-15 |
| ☑ Diagrama unifilar | NÃO implementado | I-15 |
| ☑ Rastreabilidade | PARCIAL | I-16 |
| ☑ Usabilidade técnica | PARCIAL — norma não exibida | I-11 |
| ☑ Experiência prática | [VERIFICAR] — sem testes end-to-end completos | — |
| ☑ Completude até a última seção | Parcial (para na demanda EDP) | I-13 |
| ☑ Lacunas de evidência | Documentadas como [VERIFICAR] | — |

---

## 11. LIMITAÇÕES DESTA ANÁLISE

```text
A análise foi feita com base nos materiais disponíveis: código-fonte TypeScript,
arquivos de dado JSON, e documentação de referência do sistema.

Gravações de tela, capturas de interface e logs de execução não foram fornecidos.
Comportamentos de UI foram inferidos a partir da lógica de código — marcados como [INFERÊNCIA].

Valores marcados como [VERIFICAR] dependem de conferência direta no PDF oficial
do PT.DT.PDN.00068 V09 e da ABNT NBR 5410:2004.

Esta auditoria de incongruências não substitui projeto elétrico, inspeção de campo,
validação completa segundo ABNT NBR 5410, consulta formal à concessionária,
ART/RRT ou responsabilidade técnica de profissional legalmente habilitado.
```

---

## 12. PRÓXIMOS PASSOS RECOMENDADOS

| Prioridade | Ação | Responsável sugerido |
|---|---|---|
| 1 | Comparar tabelas 005/007–015 do sistema com PDF EDP V09 | @architect ou engenheiro eletricista |
| 2 | Migrar todos os `.data.json` EDP para v09 | @dev |
| 3 | Corrigir `REFERENCIA-INTEGRAL-SISTEMA.md` seção 7.1 | @dev |
| 4 | Desagregar hidromassagem em resistência + motor | @dev com validação de @architect |
| 5 | Integrar `subcategorias-fornecimento.catalogo.data.json` ao fluxo de cálculo | @dev |
| 6 | Adicionar alerta de versão normativa na UI | @dev |
| 7 | Corrigir fronteira U/D (modelo de dados) | @dev |
| 8 | Criar stories para módulos ausentes (condutor, proteção, DR, QT) | @sm → @dev |

---

— Atlas, investigando a verdade 🔎  
*AIOX Analyst — 2026-06-21*
