# Relatório de extração — tabelas de impedância (VER-QT-02 / VER-QT-03)

**Data:** 2026-07-28
**Executado por:** @analyst (Atlas), extração direta da fonte primária
**Artefato de dados:** `impedancia-prysmian.json` (1.563 células)
**Scripts:** `extrair-impedancia.py`, `verificar-coerencia.py` (reexecutáveis)

---

## 1. Fonte

| Campo | Valor |
|---|---|
| Documento | Guia de Dimensionamento de Cabos para Baixa Tensão |
| Editor | Prysmian Brasil |
| Conformidade declarada | "De acordo com a NBR 5410" |
| URL | `https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev10.pdf` |
| SHA-256 do PDF | `82131cb4aa4b2c66c4835a8fd71bb18bfe72266e0fae1f48b3cc3f05c06ea54a` |
| Páginas | 51 |
| Data de acesso | 2026-07-28 |

**Ressalva de versionamento:** o rótulo "Rev. 10" consta apenas no nome do arquivo na URL. O texto da capa não o repete, e os metadados internos do PDF indicam criação em 2020-09-22. O hash acima é a identificação confiável desta cópia; qualquer citação futura deve referenciá-lo.

### Definições literais transcritas do cabeçalho das tabelas

> *"Os valores de resistências elétricas e reatâncias indutivas indicados nas tabelas a seguir destinam-se a cálculos de circuitos elétricos e representam as impedâncias de sequência positiva ou negativa do cabo: **Z = Rca + jXL**."*

> *"**Frequência: 60 Hz** • **Rca**: Resistência elétrica máxima do condutor em corrente alternada na temperatura de operação • **XL**: Reatância Indutiva"*

> *"Valores válidos para todos os tipos de instalação, **exceto quando instalados em conduto metálico fechado ferromagnético**."*

---

## 2. Inventário extraído

| Tabela | Pág. | Metal | Família (rótulo literal) | Blocos × colunas | Seções (mm²) | Células |
|---|---|---|---|---|---|---|
| 28 | 33 | Cu | Superastic (cobre) | 5 + 4 | 1,5 – 240 | 135 |
| 29 | 34 | Cu | Superastic Flex (cobre) e Afumex Green (cobre) | 5 + 4 | 1,5 – 240 | 135 |
| 30 | 35 | Cu | Sintenax (cobre) | 6 + 6 | 1,5 – 500 | 216 |
| 31 | 36 | Cu | Sintenax Flex (cobre) | 6 + 6 | 1,5 – 500 | 216 |
| 32 | 37 | Cu | GSette Easy (cobre) e Afumex Flex (cobre) | 6 + 6 | 1,5 – 500 | 216 |
| 33 | 38 | Cu | Voltenax (cobre) e Voltalene (cobre) | 6 + 6 | 1,5 – 500 | 216 |
| 34 | 39 | Al | Superastic (alumínio) | 5 + 4 | 16 – 500 | 117 |
| 35 | 40 | Al | Sintenax (alumínio) | 6 + 6 | 16 – 500 | 156 |
| 36 | 41 | Al | Voltenax (alumínio) e Voltalene (alumínio) | 6 + 6 | 16 – 500 | 156 |

**Total: 1.563 células.** Anomalias de parsing: **0**. Células não publicadas (`-` na fonte): **24**, registradas como `null` — nunca como zero.

### Âncora de integridade — tabela 18 (p. 22)

A tabela 18 (`Resistência Elétrica em Corrente Contínua a 20 °C`, classes 2 e 5) foi extraída de forma independente e **confere integralmente** com a transcrição auditada anteriormente. Ela publica 19 seções (1,5 a **630** mm²) — uma seção a mais do que as tabelas de impedância. Serve como âncora do teste T3 e **não é substituta de `Rca`**.

---

## 3. Resultado dos testes de coerência

| # | Teste | Veredito | Medição |
|---|---|---|---|
| T0 | `Rca` invariante entre colunas geométricas | **PASSA** (ressalva) | Mediana de dispersão 0,0 % em todas as faixas. Máximo de 20 % ocorre só em 400–500 mm², onde `Rca` é publicado com 2 casas (`0,05` vs `0,06` = 1 dígito do último decimal) |
| T1 | `Rca × secção` aproximadamente constante | **PASSA** | 23,5 → 25,0 (Cu, mediana por seção), crescendo suavemente com a seção — compatível com efeito pelicular |
| T2 | `Rca(Al) / Rca(Cu)` constante | **PASSA** | 1,500 a 1,674 em 13 seções |
| T3 | `Rca / Rdc20` ≥ 1,0 (temperatura + skin) | **PASSA** | Razão mínima 1,186 · máxima 1,366 |
| T5 | `XL` varia suavemente dentro da coluna | **PASSA** | Salto máximo entre seções adjacentes: 0,03 Ω/km |
| T6 | `XL` difere entre colunas geométricas | **PASSA** | Razão XLmax/XLmin — mediana **3,44**, máxima **4,20** |
| T7 | `Rca` decrescente com a seção | **PASSA** | 0 inversões |
| T8 | Cobertura e células ausentes | **PASSA** | 1.563 células, 24 `null` |

Nenhum teste foi ajustado para passar. T0 é reportado como ressalva de precisão da fonte, não como defeito da extração.

---

## 4. Achados

### 4.1 `Rca` é invariante entre colunas — VER-QT-02 e VER-QT-03 se separam

O teste T0 estabelece um fato que reorganiza o problema: **a resistência não depende da coluna geométrica**; apenas a reatância depende. Consequência:

- **VER-QT-02 (resistência)** fica resolvido pela chave `(família, metal, seção)` — sem necessidade de identificar a topologia.
- **VER-QT-03 (reatância)** permanece dependente da identificação da coluna (ver §5).

### 4.2 A reatância provisória no código está errada em magnitude

| | Faixa |
|---|---|
| `X` provisório hoje no código (só ≥ 25 mm²) | 0,069 – 0,080 Ω/km |
| `XL` real publicado (todas as seções) | **0,08 – 0,46 Ω/km** |

O valor em uso subestima a reatância, e o teste T6 mostra que ela varia por fator de até **4,2×** conforme a geometria. Isso confirma tecnicamente a exigência de topologia explícita levantada no dossiê externo — não é excesso de rigor.

### 4.3 A resistência provisória estava substancialmente correta

Comparação com a família Superastic (cobre), tabela 28:

| Seção | Provisório no código | `Rca` publicado | |
|---|---|---|---|
| 2,5 | 8,87 | 8,87 | idêntico |
| 4 | 5,52 | 5,52 | idêntico |
| 10 | 2,19 | 2,19 | idêntico |
| 16 | 1,38 | 1,38 | idêntico |
| 25 | 0,870 | 0,87 | idêntico |
| 1,5 | 14,48 | 14,50 | −0,1 % |
| 6 | 3,66 | 3,69 | −0,8 % |

A tabela provisória correspondia, na prática, ao Superastic Cu — mas sem fonte declarada, e portanto inutilizável sob o Artigo IV. O impacto numérico da correção da resistência é pequeno; o impacto da correção da **reatância** é grande.

### 4.4 Alumínio deixa de ter lacuna de dados

As tabelas 34–36 publicam `Rca` **e** `XL` para alumínio de 16 a 500 mm². A degradação atual (Al > 25 mm² caindo para método simplificado com `X` omitido), registrada como risco RSK-4, deixa de ter causa material — era ausência de fonte, não limitação técnica.

---

## 5. Topologias das colunas — RESOLVIDO por leitura das figuras

As colunas são rotuladas por **figuras vetoriais**, não por texto: cada tabela publica só 3 rótulos textuais (`s = 2.D`, `s = 13 cm`, `s = 20 cm`) para blocos de 4, 5 ou 6 colunas. As páginas 33–41 foram renderizadas a 260–300 dpi e as figuras foram lidas visualmente.

### Método

1. **Leitura visual** dos cabeçalhos renderizados (evidências `.png` neste diretório).
2. **Assinatura geométrica vetorial**: para cada página, os desenhos circulares do cabeçalho foram extraídos e normalizados. As assinaturas são **idênticas** dentro de cada grupo de layout, o que estende com rigor a leitura visual do representante às demais tabelas do grupo.
3. **Validação cruzada por comportamento físico** (não usada como fonte, apenas como confirmação) — ver §5.3.

### 5.1 Grupo A — tabelas 28, 29, 34 (linhas só unipolares)

| Bloco | Col | `topologia_coluna_id` |
|---|---|---|
| 1 | 1 | `2_UNIPOLARES_JUSTAPOSTOS` |
| 1 | 2 | `2_UNIPOLARES_S_2D` |
| 1 | 3 | `2_UNIPOLARES_S_13CM` |
| 1 | 4 | `2_UNIPOLARES_S_20CM` |
| 1 | 5 | `3_UNIPOLARES_JUSTAPOSTOS` |
| 2 | 1 | `3_UNIPOLARES_S_2D` |
| 2 | 2 | `3_UNIPOLARES_S_13CM` |
| 2 | 3 | `3_UNIPOLARES_S_20CM` |
| 2 | 4 | `3_UNIPOLARES_TREVO` |

### 5.2 Grupo B — tabelas 30, 31, 32, 33, 35, 36 (linhas com versão multipolar)

| Bloco | Col | `topologia_coluna_id` |
|---|---|---|
| 1 | 1 | `2_UNIPOLARES_JUSTAPOSTOS` |
| 1 | 2 | `CABO_BIPOLAR` |
| 1 | 3 | `2_UNIPOLARES_S_2D` |
| 1 | 4 | `2_UNIPOLARES_S_13CM` |
| 1 | 5 | `2_UNIPOLARES_S_20CM` |
| 1 | 6 | `3_UNIPOLARES_JUSTAPOSTOS` |
| 2 | 1 | `3_UNIPOLARES_S_2D` |
| 2 | 2 | `3_UNIPOLARES_S_13CM` |
| 2 | 3 | `3_UNIPOLARES_S_20CM` |
| 2 | 4 | `3_UNIPOLARES_TREVO` |
| 2 | 5 | `CABO_TRIPOLAR` |
| 2 | 6 | `3_UNIPOLARES_20CM_X_20CM` |

**Restrição das tabelas 33 e 36:** as colunas `CABO_BIPOLAR` e `CABO_TRIPOLAR` trazem *"Ver Nota (1)"*, cujo texto é **"Nota (1): Cabo Voltenax"** — valem apenas para o Voltenax, **não** para o Voltalene. Registrado em `nota_restricao` nos 62 registros afetados.

### 5.3 Validação independente do mapeamento

Testes aplicados **após** a leitura visual, como confirmação:

| # | Teste | Resultado |
|---|---|---|
| T9 | `XL` cresce com o espaçamento (`2.D` < `13 cm` < `20 cm`) | 282 sequências, **0 violações** |
| T10 | Configurações justapostas/trevo têm `XL` menor que espaçadas | 282 comparações, **0 violações** |
| T11 | Cabo multipolar tem `XL` menor que unipolares espaçados | 160 comparações, **0 violações** |

**724 verificações, zero violações.** O comportamento eletromagnético dos dados é integralmente consistente com o mapeamento lido nas figuras.

### 5.4 Temperatura de operação — resolvida por texto literal

Transcrito da p. 21, seção 6.3:

> *"= 70 ºC para Superastic, Superastic Flex, Sintenax, Sintenax Flex e Afumex Green"*
> *"= 90 °C para GSette Easy, Voltenax, Voltalene e Afumex Flex"*
> *"= 0,00393 ºC⁻¹ para o cobre · = 0,00403 ºC⁻¹ para o alumínio"*

Aplicado a `temperatura_operacao_c`: **70 °C** nas tabelas 28–31, 34, 35; **90 °C** nas tabelas 32, 33, 36. Os coeficientes α₂₀ ficam registrados em `fonte.coeficiente_temperatura_alfa20`.

### 5.5 Hipótese descartada

A p. 22 traz *"Para 2 condutores carregados"* e *"Para 3 condutores carregados"* no contexto das fórmulas de `XL`. Seria tentador mapear os dois blocos a essa divisão — mas a leitura das figuras mostra que **não é isso**: o bloco 1 termina com uma coluna de *três* condutores justapostos, e o bloco 2 começa com três condutores espaçados. A divisão em dois blocos é de **layout de página**, não de número de condutores carregados. Hipótese registrada e descartada por evidência.

---

## 6. Situação das pendências

| Pendência | Antes | Agora |
|---|---|---|
| VER-QT-02 — resistência Cu/Al | `[VERIFICAR]`, sem fonte | **RESOLVIDO** — fonte primária, 9 famílias, Cu 1,5–500 e Al 16–500 mm², temperatura de operação por família |
| VER-QT-03 — reatância Cu/Al | `[VERIFICAR]`, Al inexistente | **RESOLVIDO** — 12 topologias identificadas por leitura das figuras, validadas por 724 verificações |
| VER-QT-04 — fator bifásico | `[VERIFICAR]` | Confirmado (§6.2 da fonte) — auditoria anterior |
| VER-QT-06 — alturas de tomada | `[VERIFICAR]` | Confirmado como não normativo — auditoria anterior |
| VER-QT-07 — alínea 6.2.7.1 | `[VERIFICAR]`, 7 % assumido | Confirmado: alínea c → **5 %** — verificado nas fontes locais |

---

## 7. O que NÃO está decidido por este relatório

Este documento entrega **dados**. Não decide arquitetura. Continuam pendentes de `@architect` e `@po`:

1. Se o motor passa a **exigir** produto e topologia explícitos, e se **bloqueia** o cálculo sem eles (proposta do dossiê externo). Isso muda o comportamento observável da API e afeta o MOD-DC, que consome a queda de tensão como critério C5.
2. Qual família de cabo é o **padrão** do projeto, se houver, e como o usuário a seleciona.
3. Se vincular a base de produção a um único fabricante é aceitável, ou se convém obter uma segunda fonte.
4. Como tratar o cenário excluído pela fonte (conduto metálico fechado ferromagnético).
5. O impacto do limite 7 % → 5 % no **MOD-DC**, cujo PRD §13.6 assume 7 %.

---

## 8. Declaração de conformidade com o Artigo IV

- [x] Todos os 1.563 valores vêm de célula publicada, com tabela, página, família e metal registrados.
- [x] Nenhuma interpolação, extrapolação, analogia entre materiais, classes, famílias ou geometrias.
- [x] Células não publicadas registradas como `null` (24 ocorrências), nunca como zero ou valor substituto.
- [x] `topologia_coluna_id` obtido por **leitura das figuras da fonte**, não por raciocínio físico; a física foi usada apenas como validação posterior.
- [x] A hipótese "2 vs 3 condutores carregados" para os blocos foi testada e **descartada por evidência** (§5.5).
- [x] A restrição "Nota (1): Cabo Voltenax" foi transcrita e aplicada aos 62 registros afetados, em vez de ignorada.
- [x] Os onze testes de coerência foram executados e reportados, inclusive o que resultou em ressalva.
- [x] A extração é reprodutível: scripts versionados, PDF identificado por hash.
- [x] Nenhuma decisão de arquitetura foi tomada aqui.
