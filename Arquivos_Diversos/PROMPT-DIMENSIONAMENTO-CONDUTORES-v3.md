# PROMPT DE IMPLEMENTAÇÃO — MÓDULO: DIMENSIONAMENTO DE CONDUTORES

**1. Título:** Módulo de Dimensionamento de Condutores — Sistema SIE
**2. Identificador:** MOD-DC-v3.0 (substitui integralmente o MOD-DC-v2.0)
**Data:** 2026-07-11
**Idioma obrigatório:** Português do Brasil
**Dependências upstream:** Módulo de Circuitos (contrato canônico ou adaptador 1:1), Módulo IB (corrente de projeto), Módulo de Categoria de Entrada (contexto EDP)
**Dependências downstream:** Queda de Tensão (MOD-QT), Curto-Circuito (MOD-CC, futuro), Proteção (MOD-PROT, futuro), Seccionamento Automático (MOD-SEC, futuro), Eletrodutos, Lista de Materiais, Diagrama Unifilar, Memorial de Cálculo

---

## 3. IDENTIDADE DA LLM IMPLEMENTADORA

Você é um engenheiro de software sênior especializado em sistemas de engenharia assistida, com domínio de FastAPI, Pydantic v2, SQLAlchemy 2.x, React + TypeScript + IBM Carbon Design System e motores de cálculo científico em Python. Você implementa exatamente o que este prompt especifica, sem inventar valores normativos, sem assumir dados ausentes e sem ampliar o escopo.

## 4. MISSÃO

Implementar o módulo de dimensionamento de condutores para circuitos de baixa tensão do sistema SIE, em conformidade com a ABNT NBR 5410:2004, produzindo resultados auditáveis, reproduzíveis e rastreáveis, sem jamais apresentar como completo um dimensionamento com critérios obrigatórios pendentes.

## 5. OBJETIVO

Determinar, para cada circuito, a seção normalizada dos condutores de fase, do condutor neutro e do condutor de proteção (PE), atendendo **simultaneamente** aos **seis critérios** exigidos pela NBR 5410:2004, item 6.2.6.1.2:

| # | Critério | Fonte normativa | Situação neste módulo |
|---|----------|-----------------|----------------------|
| C1 | Capacidade de condução de corrente (Iz), incluindo componentes harmônicas e fatores de correção | NBR 5410, 6.2.5 e 6.2.6.1.2 a) | **Calculado neste módulo** |
| C2 | Proteção contra sobrecargas (coordenação IB ≤ In ≤ Iz e I2 ≤ 1,45·Iz) | NBR 5410, 5.3.4 e 6.3.4.2 | **Verificado neste módulo** (In pode ser sugestão; ver §12.5) |
| C3 | Proteção contra curtos-circuitos e solicitações térmicas (∫i²dt ≤ k²S²) | NBR 5410, 5.3.5 e 6.3.4.3 | **Pendência explícita** — contrato com MOD-CC (futuro); status `AGUARDANDO-CC` |
| C4 | Proteção contra choques por seccionamento automático em esquemas TN e IT, quando pertinente | NBR 5410, 5.1.2.2.4 e 6.2.6.1.2 d) | **Pendência explícita** — contrato com MOD-SEC (futuro); status `AGUARDANDO-SECCIONAMENTO` ou `NAO-APLICAVEL` conforme esquema de aterramento |
| C5 | Limites de queda de tensão | NBR 5410, 6.2.7 | **Integração** — contrato com MOD-QT; status `AGUARDANDO-QT` até retorno |
| C6 | Seções mínimas por tipo de utilização | NBR 5410, 6.2.6.1.1 e Tabela 47 | **Calculado neste módulo** |

A seção final de fase é a **maior** seção exigida entre os critérios já verificados, revalidada contra todos eles. O circuito **nunca** recebe status de dimensionamento completo enquanto C3, C4 ou C5 estiverem pendentes, reprovados ou sem dados.

> **CORREÇÃO SOBRE O MOD-DC-v2.0:** a versão anterior declarava apenas "três critérios da NBR 5410" e emitia status `DIMENSIONADO` com curto-circuito, seccionamento e queda de tensão não verificados. Isso contraria a NBR 5410, 6.2.6.1.2, que lista seis critérios cumulativos (alíneas a a f). O status terminal de sucesso desta versão é `DIMENSIONAMENTO-PARCIAL` (com pendências nomeadas) ou `VERIFICADO-COMPLETO` (somente quando todos os critérios aplicáveis retornarem aprovados).

## 6. ESCOPO

- Dimensionamento de condutores de fase de circuitos terminais e de distribuição em BT (cobre; alumínio somente nos contextos admitidos — ver §12.7).
- Dimensionamento do condutor neutro (NBR 5410, 6.2.6.2 e Tabela 48).
- Dimensionamento do condutor de proteção PE (NBR 5410, 6.4.3.1 e Tabela 58) e validação de PEN (6.4.3.4).
- Determinação do número de condutores carregados (NBR 5410, 6.2.5.6 e Tabela 46), incluindo o fator 0,86 para neutro carregado.
- Aplicação de fatores de correção de temperatura (Tabela 40), resistividade térmica do solo (Tabela 41) e agrupamento (Tabelas 42 a 45).
- Verificação de sobrecarga (5.3.4.1) com In informado ou sugerido.
- Máquina de estados por circuito com pendências explícitas para C3, C4 e C5.
- Validações de identificação por cores (função × cor) conforme 6.1.5.3.
- Contratos de integração com MOD-QT, MOD-CC, MOD-SEC e MOD-PROT.
- Base normativa versionada, rastreabilidade, memória de cálculo, API, UI em Carbon e testes.

## 7. FORA DE ESCOPO

- Cálculo da corrente de curto-circuito presumida e da integral de Joule (MOD-CC): apenas o **contrato** e o **bloqueio de status** são implementados aqui.
- Cálculo de queda de tensão (MOD-QT já existente): apenas integração.
- Cálculo de impedância do percurso de falta e tempos de seccionamento (MOD-SEC futuro): apenas contrato e bloqueio.
- Seleção definitiva de dispositivos de proteção, curvas e capacidade de interrupção (MOD-PROT futuro): In tratado como entrada ou sugestão marcada.
- Condutores em paralelo (NBR 5410, 6.2.5.7): **detectar e bloquear** com status próprio (ver §12.9); não dimensionar.
- Dimensionamento de eletrodutos, DR, aterramento/equipotencialização (exceto seção de PE/PEN), diagrama unifilar, memorial descritivo.
- Seletividade, coordenação energética, estudos harmônicos completos (anexo F da norma), dimensionamento econômico.
- Cabos armados (remetidos pela norma à ABNT NBR 11301 — fora dos anexos).

Itens fora de escopo são dependências registradas, nunca omissões silenciosas.

## 8. FONTES E LIMITES DE CONHECIMENTO

Fontes autorizadas, na hierarquia do §9:

1. `NBR_5410_chunks.json` — ABNT NBR 5410:2004 (texto segmentado).
2. `PT_DT_PDN_00068_V9_chunks.json` — Padrão técnico EDP São Paulo, fornecimento em tensão secundária, UC individual.
3. `04_condutores_markdown_limpo.md` — fonte técnica explicativa (Guia EM da NBR 5410, capítulo de linhas elétricas/condutores). **ATENÇÃO:** este material referencia a numeração de tabelas da **edição 1997** da norma (tabelas 28, 31–34, 35–42). É proibido copiar esses números de tabela; use exclusivamente a numeração da edição 2004 (tabelas 33, 36–39, 40–45, 46, 47, 48, 58).
4. `PROMPT-DIMENSIONAMENTO-CONDUTORES-v2.md` — artefato de implementação anterior, **não é fonte normativa**; suas regras só valem quando confirmadas pelos anexos.

> `[VERIFICAR — informação não confirmada nos anexos]` O anexo `06_dimensionamento_chunks.json`, previsto na lista de arquivos obrigatórios, **não foi disponibilizado** nesta rodada. Requisitos que dependeriam exclusivamente dele permanecem marcados `[VERIFICAR]` e não podem ser preenchidos com conhecimento externo.

É proibido: consultar internet, catálogos, normas não anexadas; inventar valores, fatores, limites ou tabelas; usar fallback silencioso. Toda lacuna vira `[VERIFICAR]` com fonte necessária declarada.

## 9. HIERARQUIA E APLICABILIDADE DAS FONTES

1. NBR 5410:2004 é a referência geral obrigatória para toda a instalação.
2. O padrão EDP PT.DT.PDN.00068 v09 aplica-se **somente**: à área de concessão da EDP São Paulo; a unidades consumidoras individuais com carga instalada até 75 kW; ligadas em redes **aéreas** secundárias de distribuição (fonte: PT.DT.PDN.00068, itens 1 e 2, chunks 3). Seus requisitos de condutores restringem-se ao **ramal de entrada** (item 5.4.6) e ao trecho ponto de conexão → medição; **não** se aplicam aos circuitos internos da instalação. Atendimento por rede subterrânea remete a outro padrão (não anexado) → `[VERIFICAR]`.
3. Requisitos NBR + EDP são cumulativos quando ambos aplicáveis (ex.: condutores do ramal de entrada).
4. Exemplos do material explicativo não são regra; divergências de numeração de tabela resolvem-se sempre a favor da edição 2004.
5. Conflitos não resolvíveis pelos anexos recebem status `CONFLITANTE` ou `[VERIFICAR]` e bloqueiam aprovação do requisito afetado.

## 10. PREMISSAS

- Sistema-alvo típico: trifásico estrela 220/127 V, mas o motor aceita monofásico, bifásico (com e sem neutro) e trifásico (com e sem neutro).
- Frequência 60 Hz; regime permanente, fator de carga 100% (condição das tabelas 36–39, NBR 5410, 6.2.5.2.2 nota 2).
- Cabos com tensão nominal até 0,6/1 kV, não armados (NBR 5410, 6.2.5.1.1 nota).
- Circuitos chegam do módulo de Circuitos com IB já calculado (VA usado diretamente — disciplina INC-01; tensão jamais assumida — disciplina INC-04).

## 11. GLOSSÁRIO

- **IB** — corrente de projeto do circuito (inclui componentes harmônicas; NBR 5410, 5.3.4.1 e 6.2.7.4 nota 1).
- **Iz** — capacidade de condução de corrente dos condutores nas condições reais de instalação (tabelas 36–39 corrigidas pelas tabelas 40–45).
- **In** — corrente nominal (ou de ajuste) do dispositivo de proteção.
- **I2** — corrente convencional de atuação (disjuntores) ou de fusão (fusíveis); depende da norma do dispositivo.
- **Método de referência** — A1, A2, B1, B2, C, D, E, F, G (NBR 5410, 6.2.5.1.2); obtido a partir do tipo de linha da Tabela 33.
- **Condutores carregados** — condutores efetivamente percorridos por corrente para fins térmicos (Tabela 46); PE nunca conta; PEN conta como neutro (6.2.5.6.2).
- **FCT / FCS / FRS / FCA** — fatores de correção de temperatura ambiente, de temperatura do solo, de resistividade térmica do solo e de agrupamento.
- **PE / PEN** — condutor de proteção / condutor com função combinada proteção+neutro (esquema TN-C).
- **TH3** — taxa de terceira harmônica e seus múltiplos na corrente de fase.

---

## 12. REQUISITOS NORMATIVOS

Cada requisito indica fonte exata e status de verificação da evidência (`CONFIRMADO` = texto/tabela localizado nos anexos; `[VERIFICAR]` = deve ser conferido no documento original antes de popular a base).

### 12.1 Critério C6 — Seções mínimas (Tabela 47) — CONFIRMADO

Fonte: NBR 5410:2004, 6.2.6.1.1 e Tabela 47 (chunks 131–132, p. 120–121).

| Tipo de linha | Utilização | Seção mínima |
|---|---|---|
| Instalações fixas, condutores e cabos isolados | Circuitos de iluminação | 1,5 mm² Cu / 16 mm² Al |
| Instalações fixas, condutores e cabos isolados | Circuitos de força²⁾ | 2,5 mm² Cu / 16 mm² Al |
| Instalações fixas, condutores e cabos isolados | Sinalização e controle | 0,5 mm² Cu³⁾ |
| Instalações fixas, condutores nus | Circuitos de força | 10 mm² Cu / 16 mm² Al |
| Instalações fixas, condutores nus | Sinalização e controle | 4 mm² Cu |
| Linhas flexíveis com cabos isolados | Equipamento específico | conforme norma do equipamento |
| Linhas flexíveis com cabos isolados | Qualquer outra aplicação | 0,75 mm² Cu⁴⁾ |
| Linhas flexíveis | Extrabaixa tensão, aplicações especiais | 0,75 mm² Cu |

Notas da tabela (preservar na base de dados): 1) mínimos ditados por razões mecânicas; 2) **circuitos de tomadas de corrente são circuitos de força**; 3) sinalização/controle para equipamentos eletrônicos admite 0,1 mm²; 4) cabos multipolares flexíveis com ≥ 7 veias admitem 0,1 mm².

Mapeamento SIE: `ILU → iluminação (1,5 Cu)`; `TUG → força (2,5 Cu)`; `TUE → força (2,5 Cu)`. **Correção sobre o v2.0:** o comentário do v2 §4.4 ("Iluminação: Al→2.5") contraria a Tabela 47, que fixa 16 mm² Al para iluminação e força; e a restrição de alumínio não decorre de "6.2.6.1.2", mas da própria Tabela 47 combinada com 6.2.3.8 (ver §12.7).

### 12.2 Critério C1 — Capacidade de condução de corrente

**12.2.1 Tabelas base (CONFIRMADO em estrutura; valores completos [VERIFICAR — popular do original]):**
- Tabela 36 — métodos A1, A2, B1, B2, C, D; Cu e Al; PVC; condutor 70 °C; referência 30 °C (ar) / 20 °C (solo). Chunk 118, p. 108–109.
- Tabela 37 — métodos A1–D; Cu e Al; EPR/XLPE; condutor 90 °C. Chunk 119, p. 110.
- Tabela 38 — métodos E, F, G; Cu e Al; PVC. Colunas específicas: E multipolar 2 e 3 carregados; F unipolares justapostos (2), trifólio (3), mesmo plano justapostos (3); G espaçados horizontal e vertical. Chunk 120, p. 111–112.
- Tabela 39 — idem para EPR/XLPE. Chunk 121, p. 112–113.

Amostra já confirmada da Tabela 36 (Cu, PVC), utilizável como teste de regressão da carga de dados — B1/2 carregados: 1,5→17,5 A; 2,5→24 A; 4→32 A; 6→41 A; 10→57 A; 16→76 A; 25→101 A; 35→125 A. B1/3 carregados: 1,5→15,5; 2,5→21; 4→28; 6→36; 10→50; 16→68; 25→89; 35→110. C/2: 2,5→27; C/3: 2,5→24. D/2: 2,5→29; D/3: 2,5→24. Qualquer valor digitado na base que divirja da célula correspondente do original é defeito bloqueante.

A chave de consulta é obrigatória e completa: `(tabela, material, isolação, método de referência, nº de condutores carregados, seção)`. Consulta sem qualquer dessas dimensões é proibida (retornar `ERRO-CONSULTA-INCOMPLETA`).

**12.2.2 Métodos de referência e Tabela 33 — CONFIRMADO (estrutura):** A1, A2, B1, B2, C, D, E, F, G conforme 6.2.5.1.2 (chunk 116). A Tabela 33 (chunk 114) mapeia cada **tipo de linha numerado** (1, 2, 3, …, 11, 11A, 11B, 12–18, 21–27, …) ao método de referência. A UI deve oferecer a seleção pelo **tipo de linha** (com descrição) e derivar o método automaticamente, exibindo ambos. Regras de consistência mínimas extraídas da Tabela 33: condutores **isolados** só são admitidos dentro de condutos (métodos A1/B1 e variantes) — não podem ser lançados expostos como em C/E/F/G, que exigem cabos uni/multipolares; o método D pressupõe cabo em eletroduto enterrado. Combinações tipo de condutor × tipo de linha não previstas na Tabela 33 devem ser bloqueadas (`ERRO-LINHA-INCOMPATIVEL`). Carga completa da Tabela 33 na base: `[VERIFICAR — transcrever todos os tipos de linha do original]`.

**12.2.3 Fator de temperatura — Tabela 40 — CONFIRMADO (chunk 122, p. 114):**

Ambiente (referência 30 °C), PVC: 10→1,22; 15→1,17; 20→1,12; 25→1,06; 35→0,94; 40→0,87; 45→0,79; 50→0,71; 55→0,61; 60→0,50; 65–80→não admitido (–).
Ambiente, EPR/XLPE: 10→1,15; 15→1,12; 20→1,08; 25→1,04; 35→0,96; 40→0,91; 45→0,87; 50→0,82; 55→0,76; 60→0,71; 65→0,65; 70→0,58; 75→0,50; 80→0,41.
Solo (referência 20 °C), PVC: 10→1,10; 15→1,05; 25→0,95; 30→0,89; 35→0,84; 40→0,77; 45→0,71; 50→0,63; 55→0,55; 60→0,45; 65–80→(–).
Solo, EPR/XLPE: 10→1,07; 15→1,04; 25→0,96; 30→0,93; 35→0,89; 40→0,85; 45→0,80; 50→0,76; 55→0,71; 60→0,65; 65→0,60; 70→0,53; 75→0,46; 80→0,38.

> **CORREÇÃO sobre o v2.0:** os valores comentados no v2 §4.2 (ex.: PVC 25 °C→1,04; 40 °C→0,91; EPR 25 °C→1,02) estão **errados** frente à Tabela 40. Use exclusivamente os valores acima. Temperaturas fora dos pontos tabelados: não interpolar sem regra documentada nos anexos → `ERRO-FATOR-NAO-ENCONTRADO` (interpolação: `[VERIFICAR — não há autorização de interpolação nos anexos]`). Célula "–" significa isolação não admitida naquela temperatura → bloquear. A escolha ambiente × solo é derivada do método: D usa bloco "solo"; demais usam "ambiente" (6.2.5.3.2).

**12.2.4 Resistividade térmica do solo — Tabela 41 — CONFIRMADO (chunk 123):** aplicável apenas ao método D; referência 2,5 K·m/W; fatores: 1→1,18; 1,5→1,10; 2→1,05; 3→0,96. Notas: valores médios (dispersão < 5%); aplicáveis a eletrodutos enterrados até 0,8 m; cabos diretamente enterrados exigem cálculo (NBR 11301, fora dos anexos → bloquear com `[VERIFICAR]`).

**12.2.5 Fatores de agrupamento — Tabelas 42 a 45:**
- Tabela 42 (CONFIRMADO, chunk 125) — feixe e camada única. Linha 1 (feixe: ao ar livre ou sobre superfície; embutidos; em conduto fechado — aplicável aos métodos A a F): 1→1,00; 2→0,80; 3→0,70; 4→0,65; 5→0,60; 6→0,57; 7→0,54; 8→0,52; 9 a 11→0,50; 12 a 15→0,45; 16 a 19→0,41; >20→0,38. Linha 2 (camada única sobre parede/piso/bandeja não perfurada, método C): 1→1,00; 2→0,85; 3→0,79; 4→0,75; 5→0,73; 6→0,72; 7→0,72; 8→0,71; ≥9→0,70. Linha 3 (camada única no teto): 0,95; 0,81; 0,72; 0,68; 0,66; 0,64; 0,63; 0,62; ≥9→0,61. Linha 4 (camada única em bandeja perfurada, métodos E/F): 1,00; 0,88; 0,82; 0,77; 0,75; 0,73; 0,73; 0,72; ≥9→0,72. Linha 5 (camada única sobre leito/suporte): 1,00; 0,87; 0,82; 0,80; 0,80; 0,79; 0,79; 0,78; ≥9→0,78.
  > **CORREÇÃO sobre o v2.0:** as faixas comentadas no v2 ("10-12→0.45, 13-16→0.41, 17-20→0.38") estão erradas; as faixas corretas são 9–11, 12–15, 16–19 e >20.
- Nota 2 da Tabela 42 (CONFIRMADO): distância horizontal entre cabos adjacentes superior a **2× o diâmetro externo** dispensa fator de redução. A UI deve oferecer essa isenção como opção declarável e rastreada.
- Notas 3–5 (CONFIRMADO): o número consultado é o de **circuitos** (grupos de 2 ou 3 condutores) e/ou cabos multipolares; N condutores isolados podem ser tratados como N/2 circuitos (2 carregados) ou N/3 (3 carregados).
- Tabela 43 (mais de uma camada), Tabela 44 (cabos diretamente enterrados) e Tabela 45 (eletrodutos enterrados): estrutura confirmada (chunks 126–128); valores completos `[VERIFICAR — popular do original]`.
- 6.2.5.5.2 (CONFIRMADO): circuitos com corrente de projeto ≤ 30% da capacidade já corrigida podem ser **desconsiderados** na contagem do grupo. Implementar como opção assistida com justificativa registrada.
- 6.2.5.5.5 (**CONFIRMADO** — fórmula verificada contra original, imagem da p. 119): grupos de condutores **não semelhantes** (fora do intervalo de três seções normalizadas sucessivas, ou temperaturas máximas distintas) exigem: **a)** cálculo caso a caso (ex.: ABNT NBR 11301); ou **b)** fator F da expressão: **F = 1/√n**, onde n = número de circuitos ou de cabos multipolares. Este fator **substitui integralmente** qualquer fator de agrupamento tabelado (Tabelas 42–45) — não é cumulativo com eles (Guia EM, chunk 8: "substitui completamente qualquer outro fator obtido nas tabelas"). Nota 2 de 6.2.5.5.5: a expressão está a favor da segurança e reduz os perigos de sobrecarga nos condutores de menor seção; pode, no entanto, resultar no superdimensionamento dos condutores de seções mais elevadas. Exemplos de referência (Guia EM, chunk 7): n=10 → F=0,32; n=30 → F=0,18. O sistema deve alertar o projetista quando F < 0,30, sugerindo revisão da disposição/agrupamento dos cabos para obter fatores menos penalizantes.
- Temperaturas máximas distintas no grupo (6.2.5.5.1 nota 2, CONFIRMADO): usar a **menor** temperatura máxima do grupo para todos.

**12.2.6 Número de condutores carregados — Tabela 46 — CONFIRMADO (chunks 129–130, p. 119–120):**

| Esquema de condutores vivos | Carregados |
|---|---|
| Monofásico a dois condutores (F+N) | 2 |
| Monofásico a três condutores | 2 |
| Duas fases sem neutro | 2 |
| **Duas fases com neutro** | **3** |
| Trifásico sem neutro | 3 |
| Trifásico com neutro | 3 ou 4¹⁾ |

¹⁾ 6.2.5.6.1: em trifásico com neutro, se TH3 > 15%, o neutro conta como carregado (4 condutores) e aplica-se o **fator 0,86** sobre a coluna de 3 condutores carregados (nenhuma tabela tem coluna de 4), acumulável com os demais fatores. Alternativa da nota 2 (fator = fator de agrupamento de 2 circuitos, sobre a coluna de 2 carregados) pode ser oferecida como modo avançado, com rastreio. PE nunca conta; PEN conta como neutro (6.2.5.6.2).

> **CORREÇÃO sobre o v2.0:** o pseudocódigo anterior usava `num_fases==3 → 3, senão 2`, o que **erra o caso bifásico com neutro** (2F+N = 3 carregados) e ignora TH3. A determinação deve usar a Tabela 46 com o esquema completo (nº de fases + presença de neutro + TH3 declarada). TH3 é campo de entrada opcional com três estados: `nao_declarada` (assumir ≤ 15% somente mediante confirmação explícita do projetista, registrada), `<=15`, `>15_e_<=33`, `>33`.

**12.2.7 Variações no percurso — 6.2.5.8 — CONFIRMADO:** havendo condições de dissipação distintas ao longo do percurso, dimensionar pela condição **mais desfavorável**. A UI deve permitir declarar mais de um trecho (método/temperatura/agrupamento) e o motor adota o pior caso, com rastreio do trecho decisivo.

### 12.3 Critério C2 — Proteção contra sobrecargas — CONFIRMADO (chunk 89, p. 71–72)

NBR 5410, 5.3.4.1: **a)** IB ≤ In ≤ Iz; **b)** I2 ≤ 1,45·Iz.

- I2 é a corrente convencional de atuação (disjuntores) ou de fusão (fusíveis), definida pela **norma do dispositivo**. Os anexos **não** estabelecem I2 = 1,45·In para nenhuma família de dispositivo → é **proibido** assumir essa equivalência genericamente. Implementação: I2 é entrada (do MOD-PROT ou do projetista, com fonte); ausente → verificação b) fica `PENDENTE-I2` e bloqueia `VERIFICADO-COMPLETO`. `[VERIFICAR — relação I2/In por norma de dispositivo (NBR NM 60898, NBR IEC 60947-2, IEC 60269) não consta dos anexos]`.
  > **CORREÇÃO sobre o v2.0:** a verificação `i2_menor_145iz = (1.45·In ≤ 1.45·Iz)` era tautológica (equivale a In ≤ Iz) e embutia I2 = 1,45·In sem sustentação documental. Remover.
- Nota de 5.3.4.1 (CONFIRMADO): se a temperatura limite de sobrecarga (Tabela 35) puder ser mantida por mais de 100 h em 12 meses ou 500 h na vida útil, a condição b) é substituída por **I2 ≤ Iz**. Expor como parâmetro de regime declarável (`regime_sobrecarga_severo: bool`, padrão `False`, com tooltip citando a nota).
- Iz usado nas duas condições é o **corrigido** pelos fatores aplicáveis.
- Omissões admitidas de proteção contra sobrecarga (5.3.4.3) e recomendadas (5.3.4.4 — ex.: bombas de incêndio): registrar como estados `SOBRECARGA-OMITIDA-DECLARADA` mediante justificativa; nunca omitir por padrão.
- Série de In comercial: os anexos **não** trazem série normalizada de disjuntores → a lista do v2 (6…125 A) permanece **parametrizável e marcada `[VERIFICAR — IEC 60898/fabricantes]`**; qualquer In sugerido automaticamente pelo sistema é rotulado `SUGESTAO` (nunca `VERIFICADO`) e precisa de confirmação do projetista ou do MOD-PROT.

Tabela 35 — Temperaturas características (CONFIRMADO, chunk 117): PVC ≤ 300 mm²: 70/100/160 °C; PVC > 300 mm²: 70/100/140 °C; EPR: 90/130/250 °C; XLPE: 90/130/250 °C.

### 12.4 Critério C3 — Curto-circuito (contrato) — CONFIRMADO (chunks 94–95)

∫i²dt ≤ k²S²; para 0,1 s ≤ t ≤ 5 s: I²·t ≤ k²·S². Valores de k (Tabela 30): Cu/PVC ≤ 300 mm² → 115; Cu/PVC > 300 → 103; Cu/EPR-XLPE → 143; Al/PVC ≤ 300 → 76; Al/PVC > 300 → 68; Al/EPR-XLPE → 94; emendas soldadas Cu/PVC → 115. Nota: k não normalizado para seções < 10 mm², durações > 5 s, condutores nus.

Contrato de saída deste módulo para o MOD-CC: `{circuito_id, secao_final_mm2, material, isolacao, k_aplicavel, temperatura_inicial, temperatura_final}`. Contrato de entrada esperado do MOD-CC: `{icc_presumida_a, tempo_atuacao_s, integral_joule_dispositivo, aprovado: bool, fonte}`. Enquanto não houver retorno: `curto_circuito_verificado = False` e pendência `AGUARDANDO-CC` visível.

### 12.5 Critério C4 — Seccionamento automático (contrato) — CONFIRMADO (referência 5.1.2.2.4 via 6.2.6.1.2 d)

Aplicável a esquemas TN e IT. O campo `esquema_aterramento` (`TT`, `TN-S`, `TN-C`, `TN-C-S`, `IT`) é entrada obrigatória do contexto do projeto. Em TT → `NAO-APLICAVEL` para este critério (registrado, não omitido); em TN/IT → `AGUARDANDO-SECCIONAMENTO` até o MOD-SEC retornar. Detalhes de 5.1.2.2.4 (tempos, impedâncias): `[VERIFICAR — transcrever do original quando o MOD-SEC for especificado]`.

### 12.6 Critério C5 — Queda de tensão (integração) — CONFIRMADO (chunks 134–135)

Limites NBR 5410, 6.2.7.1/6.2.7.2: 7% a partir do transformador próprio ou do ponto de entrega no secundário do transformador da distribuidora; 5% a partir do ponto de entrega nos demais casos em tensão secundária; 7% a partir de gerador próprio; **circuitos terminais: nunca superior a 4%**; acréscimo de 0,005%/m além de 100 m, limitado a +0,5% (nota 3). Cálculo com a corrente de projeto IB, incluindo harmônicas (6.2.7.4).

Este módulo **não calcula** queda de tensão: envia ao MOD-QT `{circuito_id, secao_candidata_mm2, material, isolacao, metodo, comprimento_m, ib_a, tensao_v, num_fases, fp}` e recebe `{atende: bool, queda_percentual, limite_aplicado, fonte}`. Se o MOD-QT exigir seção maior, o motor **revalida todos os critérios** com a nova seção (laço do §20). Sem retorno → `AGUARDANDO-QT`.

Requisito EDP (aplicável somente ao ramal de entrada, na área de concessão): queda máxima de **1%** entre ponto de conexão e medição (PT.DT.PDN.00068, 5.4.6, chunk 22 — CONFIRMADO). Nunca generalizar esse limite para circuitos internos.

### 12.7 Alumínio — restrições de uso — CONFIRMADO (chunks 113–114, 6.2.3.7/6.2.3.8)

O alumínio só é admitido:
- **Estabelecimentos industriais** (6.2.3.8.1): seção ≥ 16 mm²; instalação alimentada diretamente por subestação/transformador a partir de rede AT ou fonte própria; instalação e manutenção por pessoas qualificadas (BA5).
- **Estabelecimentos comerciais** (6.2.3.8.2): seção ≥ 50 mm²; locais exclusivamente BD1; BA5.
- **Proibido em qualquer circunstância** em locais BD4 (6.2.3.8.3).

> **CORREÇÃO sobre o v2.0:** a regra anterior ("Al sempre elevado a 16 mm² com alerta") é insuficiente e induz erro: em instalação **residencial**, alumínio não se enquadra em nenhuma das hipóteses de 6.2.3.8 e deve ser **bloqueado** com `ERRO-MATERIAL-NAO-ADMITIDO`, citando 6.2.3.8. O campo `tipo_instalacao` (`residencial`, `comercial`, `industrial`) e as condições BA5/BD tornam-se entradas obrigatórias quando `material = Al`. Nos contextos admitidos, aplicar o piso de seção (16 ou 50 mm²) e as seções mínimas Al da Tabela 47.

### 12.8 Neutro — CONFIRMADO (chunks 133–134, 6.2.6.2 e Tabela 48)

1. Neutro não pode ser comum a mais de um circuito (6.2.6.2.1) — validar contra o contrato de circuitos.
2. Monofásico: S_neutro = S_fase (6.2.6.2.2).
3. Trifásico com neutro: TH3 > 15% → S_neutro ≥ S_fase; igualdade admitida se TH3 ≤ 33% (6.2.6.2.3).
4. Duas fases com neutro: S_neutro ≥ S_fase; igualdade admitida se TH3 ≤ 33% (6.2.6.2.4).
5. TH3 > 33% → pode ser necessária S_neutro **maior** que S_fase; determinação depende do anexo F (fora dos anexos) → status `VERIFICAR-NEUTRO-HARMONICAS`, bloqueando `VERIFICADO-COMPLETO` (6.2.6.2.5).
6. Redução do neutro (Tabela 48) **somente** se, simultaneamente: trifásico com S_fase > 25 mm²; circuito presumivelmente equilibrado; TH3 ≤ 15%; neutro protegido contra sobrecorrentes conforme 5.3.2.2; mesmo metal que as fases. Tabela 48: S≤25→S; 35→25; 50→25; 70→35; 95→50; 120→70; 150→70; 185→95; 240→120; 300→150; 400→185.

### 12.9 Condutores em paralelo — CONFIRMADO (chunks 130–131, 6.2.5.7; 91–93, 5.3.4.5 e 5.3.5.4)

Fora do escopo de cálculo. Se nenhuma seção da série atender aos critérios (`ERRO-IZ-INSUFICIENTE` na maior seção), o sistema informa que a norma admite condutores em paralelo sob as condições de 6.2.5.7 (mesma constituição, seção, comprimento, sem derivações; limites 50 mm² Cu / 70 mm² Al para formações simples) e emite status `REQUER-ESTUDO-PARALELO` — nunca dimensiona sozinho.

### 12.10 PE e PEN — CONFIRMADO (chunks 180–183)

- Tabela 58 (mesmo metal que as fases): S_fase ≤ 16 → S_PE = S_fase; 16 < S_fase ≤ 35 → 16; S_fase > 35 → S_fase/2 (arredondar para a seção padronizada mais próxima; 6.4.3.1.3).
- Alternativa por cálculo adiabático (6.4.3.1.2) com k das Tabelas 56/57 — valores parcialmente confirmados (chunk 180); implementação do cálculo fica condicionada ao MOD-CC → registrar como método alternativo `[VERIFICAR]`.
- PE fora do mesmo cabo/conduto que as fases: mínimo 2,5 mm² Cu (com proteção mecânica) ou 4 mm² Cu (sem); 16 mm² Al em ambos os casos (6.4.3.1.4).
- PE comum a vários circuitos: admitido no mesmo conduto, dimensionado pela maior fase (6.4.3.1.5 b).
- PEN: apenas instalações fixas, S ≥ 10 mm² Cu ou 16 mm² Al (6.4.3.4.1); esquema TN-C; após separação PEN → N + PE, o neutro não pode ser reaterrado nem religado ao PE (6.4.3.4.3).

### 12.11 Identificação por cores — CONFIRMADO (chunks 109–110, 6.1.5.3; 04_condutores)

- Neutro: azul-clara (isolação/veia/cobertura). Veia azul-clara de multipolar pode ter outra função só se o circuito não tiver neutro.
- PE: verde-amarela ou verde — cores **exclusivas** da função de proteção.
- PEN: azul-clara com anilhas verde-amarelas nos pontos visíveis/acessíveis.
- Fase: qualquer cor, exceto as anteriores; evitar isolação exclusivamente amarela onde houver risco de confusão com verde-amarelo.
- EDP, ramal de entrada (5.4.6): neutro azul-claro; fases em cor distinta do neutro e **não verde**.
A UI deve bloquear combinações função × cor proibidas (`ERRO-COR-FUNCAO`).

### 12.12 Requisitos EDP São Paulo aplicáveis — CONFIRMADO (chunks 3, 22–23)

Aplicáveis somente na área de concessão, UC individual ≤ 75 kW, rede aérea, e **apenas ao ramal de entrada**:
- Condutores do ramal: **cobre**, isolação PVC 450/750 V ou XLPE/EPR 0,6/1,0 kV, conforme ABNT; características gravadas na isolação.
- Dimensionamento do ramal por categoria de atendimento via Tabelas 001/002 do padrão (já implementadas no SIE — **NÃO TOCAR**); nas categorias U, D2 e T2 o cliente não fornece os condutores (deixa guia passa-fio).
- Continuidade do neutro obrigatória (vedado chave, disjuntor ou fusível no neutro); sem emendas; sobras ≥ 600 mm; conectores tubulares nos terminais.
- Queda de tensão ponto de conexão → medição ≤ 1%.
O sistema mantém `contexto_concessionaria` com `perfil_normativo`, `versao` (v09) e `indicador_aplicabilidade`; projetos fora do campo de aplicação não recebem esses requisitos.

### 12.13 Série de seções normalizadas

As seções admitidas são exatamente as listadas nas tabelas 36–39 da NBR 5410: 0,5; 0,75; 1; 1,5; 2,5; 4; 6; 10; 16; 25; 35; 50; 70; 95; 120; 150; 185; 240; 300; 400; 500; 630 mm² (presença de 630 confirmada no chunk 118; existência de 800/1000 nas tabelas E/F/G: `[VERIFICAR]`). Guarda INC-07 mantida: qualquer seção fora da série é rejeitada. A atribuição da série à "IEC 60228" não consta dos anexos → manter o nome da constante, mas a `fonte` registrada é "NBR 5410:2004, tabelas 36–39, coluna de seções nominais" com nota `[VERIFICAR — correspondência com IEC 60228]`.

### 12.14 Mapeamento de tabelas — edição 1997 × 2004 — CONFIRMADO (Guia EM, 06_dimensionamento)

O material explicativo (Guia EM da NBR 5410) utiliza a numeração de tabelas da **edição 1997**. O SIE adota **exclusivamente** a numeração da edição 2004. Mapeamento de referência cruzada para evitar erros de transcrição:

| Guia EM (ed. 1997) | NBR 5410:2004 | Conteúdo |
|---|---|---|
| Tabelas 31–34 | Tabelas 36–39 | Capacidade de condução de corrente |
| Tabela 33 (do Guia, não confundir com Tab.33 da NBR 2004) | — | Mapeamento tipo de linha → método de referência (na ed. 2004 é a Tabela 33) |
| Tabela 34 | Tabela 40 | Fatores de correção por temperatura |
| Tabela 37 | Tabela 42 | Fatores de agrupamento (camada única e feixe) |
| Tabela 42 | Tabela 43 | Fatores de agrupamento (múltiplas camadas) |
| Tabela 43 | Tabela 47 | Seções mínimas |
| Tabela 46 | — | Limites de queda de tensão (na ed. 2004 esses limites estão em 6.2.7) |

Qualquer citação no código, nos testes ou na UI deve usar a coluna "NBR 5410:2004". Se um valor for transcrito de material didático que use numeração 1997, converter antes de registrar. Validação: teste automatizado que rejeita referências a "tabela 31", "tabela 34" (temperatura) ou "tabela 37" (agrupamento) fora do mapeamento.

### 12.15 Dimensionamento econômico — INFORMATIVO (Guia EM, chunks 13–17)

O Guia EM apresenta o método simplificado da IEC 60287-3-2 para determinação da seção econômica (SE = IB × √(t·e·H·N / G')). Não é requisito da NBR 5410, mas pode agregar valor ao SIE como funcionalidade futura. Status: **FORA DO ESCOPO ATUAL** — registrado para roadmap. Quando implementado, a seção econômica será comparada com a seção técnica (maior dos 6 critérios) e a UI exibirá análise de custo total (Ct = Cci + VP das perdas), sem jamais substituir a seção técnica como mínima obrigatória.

---

## 13. REGRAS GERAIS SIE (obrigatórias, herdadas e revisadas)

- **R-01 Rastreabilidade normativa:** todo valor calculado armazena `fonte` exata (documento, edição, item, tabela, linha, coluna, nota, página, `chunk_id`) e `status_verificacao` (`CONFIRMADO` | `PENDENTE` | `[VERIFICAR]`). Referência genérica ("conforme norma") é proibida.
- **R-02 Série normalizada:** conforme §12.13; erro `INC-07` para seção fora da série.
- **R-03 Tensão sem fallback:** `tensao_v is None` → `ERRO-TENSAO-AUSENTE`, nenhum cálculo (disciplina INC-04).
- **R-04 VA direto:** nunca dividir VA por fator de potência (disciplina INC-01).
- **R-05 Design System:** IBM Carbon; proibido texto branco sobre `#fa4d56` (contraste 3,35:1 < WCAG AA 4,5:1) — teste automatizado obrigatório (padrão `test_ds04`).
- **R-06 Isolação explícita:** PVC ou EPR/XLPE sempre escolhidos pelo projetista (padrão de projeto com override por circuito); ausência → `ERRO-ISOLACAO-AUSENTE` (resolução INC-12).
- **R-07 Material explícito:** Cu ou Al sempre escolhidos pelo projetista; Al sujeito ao §12.7.
- **R-08 Método de instalação explícito:** ausência → `ERRO-METODO-AUSENTE`; jamais assumir B1 silenciosamente (o "B1 padrão" do lote é um valor **proposto na UI**, visível e editável, nunca implícito no motor).
- **R-09 Nada aprovado por arredondamento:** comparações IB ≤ Iz etc. usam `Decimal` com tolerância explícita; valor original e arredondado são ambos registrados.
- **R-10 Pendência bloqueia completude:** qualquer critério obrigatório pendente/reprovado/sem dados impede `VERIFICADO-COMPLETO`.
- **R-11 Override auditado:** todo override exige justificativa, preserva o valor calculado e a rastreabilidade, e é reversível.

## 14. MODELO DE DADOS E CONTRATOS

### 14.1 Contrato de entrada (do módulo de Circuitos)

```python
class CircuitoParaDimensionamento(BaseModel):
    id: str                                  # ex.: "ILUM-Dormitorio-1" (IDs reais preservados — CONF-02)
    descricao: str
    tipo: Literal["ILU", "TUG", "TUE"]
    potencia_va: float
    tensao_v: Optional[float]                # 127 | 220 | None (None → ERRO-TENSAO-AUSENTE)
    corrente_projeto_a: float                # IB upstream (inclui harmônicas quando declaradas)
    num_fases: Literal[1, 2, 3]
    fases: list[str]                         # convenção R/S/T (CONF-01)
    tem_neutro: bool
    fp_carga: Optional[float]                # informativo; NUNCA recalcular VA
    taxa_h3: Literal["nao_declarada", "ate_15", "de_15_a_33", "acima_33"] = "nao_declarada"
    fonte_ib: str
```

### 14.2 Parâmetros de dimensionamento (por circuito ou lote, sempre explícitos)

`material` (Cu|Al), `isolacao` (PVC|EPR|XLPE), `tipo_linha_tabela33` (nº do tipo de linha; deriva `metodo_referencia`), `temperatura_c` + `origem_temperatura` (ambiente|solo, derivada do método), `resistividade_solo_kmw` (método D), `disposicao_agrupamento` (enum das linhas das Tabelas 42–45), `num_circuitos_agrupados`, `isencao_espacamento_2d: bool` (nota 2 Tab. 42, com justificativa), `esquema_aterramento`, `tipo_instalacao` (residencial|comercial|industrial), `condicoes_ba_bd` (quando Al), `regime_sobrecarga_severo: bool`, `in_a: Optional[float]` + `origem_in` (`INFORMADO`|`SUGESTAO`|`MOD-PROT`), `i2_a: Optional[float]` + `fonte_i2`, `comprimento_m: Optional[float]` (para o contrato com MOD-QT), `trechos: list[TrechoPercurso]` (§12.2.7, opcional).

Cada campo com: tipo, unidade, obrigatoriedade, intervalo (bloquear negativos e zero onde não físico), enumeração, dependências, mensagem de erro acionável e impacto da ausência.

### 14.3 Contrato de saída

```python
class ResultadoDimensionamento(BaseModel):
    circuito_id: str
    # Entradas capturadas (ecoadas para auditoria)
    material: Literal["Cu", "Al"]; isolacao: Literal["PVC", "EPR", "XLPE"]
    tipo_linha_tabela33: str; metodo_referencia: str
    temperatura_c: int; num_condutores_carregados: int   # via Tabela 46
    fator_neutro_carregado: Optional[float]              # 0,86 quando aplicável
    fatores: dict                                        # FCT/FCS/FRS/FCA com fontes
    # Seções por critério (None = pendente/não aplicável, com motivo em `criterios`)
    secao_c1_capacidade_mm2: Optional[float]
    secao_c2_sobrecarga_mm2: Optional[float]
    secao_c6_minima_mm2: Optional[float]
    secao_c5_queda_tensao_mm2: Optional[float]           # retorno do MOD-QT
    secao_c3_curto_mm2: Optional[float]                  # retorno do MOD-CC
    secao_c4_seccionamento_mm2: Optional[float]          # retorno do MOD-SEC
    # Resultado
    secao_fase_mm2: Optional[float]                      # max dos critérios verificados, na série
    secao_neutro_mm2: Optional[float]                    # §12.8
    secao_pe_mm2: Optional[float]                        # §12.10
    secao_pen_mm2: Optional[float]                       # quando TN-C
    iz_corrigida_a: Optional[float]
    in_a: Optional[float]; origem_in: Optional[str]
    criterio_decisivo: Optional[str]
    # Verificações (tri-estado: True/False/None=pendente)
    ib_menor_igual_in: Optional[bool]
    in_menor_igual_iz: Optional[bool]
    i2_menor_igual_145iz: Optional[bool]                 # usa I2 real; None se I2 ausente
    # Estado
    status: str                                          # máquina de estados do §15
    criterios: dict[str, str]                            # C1..C6 → APROVADO|REPROVADO|PENDENTE|NAO-APLICAVEL|SEM-DADOS
    alertas: list[str]; pendencias: list[str]
    rastreio: dict                                       # §17
```

### 14.4 Persistência

Manter as tabelas do v2 (`tabela_iz`, `fator_correcao_temperatura`, `fator_correcao_agrupamento`, `secao_minima_aplicacao`, colunas em `circuito`) com as seguintes alterações obrigatórias:
- `tabela_iz`: acrescentar `tabela_nbr` (36–39), `pagina_origem`, `chunk_id`; `num_condutores_carregados` admite colunas específicas das tabelas 38/39 (enum de coluna, não apenas 2|3).
- `fator_correcao_temperatura`: acrescentar `meio` (`ambiente`|`solo`); popular com os valores do §12.2.3 (status `CONFIRMADO`, fonte "NBR 5410:2004, Tabela 40, p. 114, chunk 122").
- Nova tabela `fator_resistividade_solo` (Tabela 41, CONFIRMADO).
- `fator_correcao_agrupamento`: `disposicao` referencia as linhas 1–5 da Tabela 42 e as Tabelas 43/44/45; faixas 9–11, 12–15, 16–19, >20 modeladas como intervalos, não valores pontuais.
- `secao_minima_aplicacao`: refletir integralmente a Tabela 47 do §12.1 (incluindo condutores nus e linhas flexíveis, notas 1–4).
- Novas tabelas: `secao_neutro_reduzida` (Tabela 48), `secao_pe` (regra da Tabela 58), `fator_k_curto` (Tabela 30), `tipos_linha_tabela33`.
- Toda linha carrega `fonte`, `status_verificacao`, `versao_base_normativa`. Valores `[VERIFICAR]` **impedem** o dimensionamento que dependa deles (`ERRO-TABELA-INCOMPLETA`), como no v2 (CA herdado).

## 15. ESTADOS

M�quina de estados por circuito (semântica obrigatória; nomes ajustáveis):

`RASCUNHO` → `DADOS-INCOMPLETOS` (qualquer erro de entrada: `ERRO-TENSAO-AUSENTE`, `ERRO-ISOLACAO-AUSENTE`, `ERRO-METODO-AUSENTE`, `ERRO-MATERIAL-NAO-ADMITIDO`, `ERRO-LINHA-INCOMPATIVEL`, `ERRO-COR-FUNCAO`, `ERRO-CONSULTA-INCOMPLETA`, `ERRO-TABELA-INCOMPLETA`, `ERRO-FATOR-NAO-ENCONTRADO`, `ERRO-AGRUPAMENTO-NAO-TABELADO`) → `DIMENSIONAMENTO-PARCIAL` (C1, C2, C6 aprovados; pendências entre `AGUARDANDO-QT`, `AGUARDANDO-CC`, `AGUARDANDO-SECCIONAMENTO`, `AGUARDANDO-PROTECAO`, `PENDENTE-I2`, `VERIFICAR-NEUTRO-HARMONICAS`) → `VERIFICADO-COMPLETO` (todos os critérios aplicáveis aprovados) | `REPROVADO` (qualquer critério reprovado na seção máxima admissível) | `REQUER-ESTUDO-PARALELO` | `NAO-APLICAVEL` (por critério, nunca para o circuito inteiro).

Regras: transição para `VERIFICADO-COMPLETO` exige lista de pendências vazia e todos os `criterios` em `APROVADO` ou `NAO-APLICAVEL`; qualquer novo retorno de módulo downstream que aumente a seção reabre o estado para revalidação; overrides não alteram o estado sem reexecução do motor.

## 16. FLUXO E PSEUDOCÓDIGO (motor)

```python
SERIE_SECOES = [0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70,
                95, 120, 150, 185, 240, 300, 400, 500, 630]  # §12.13

def dimensionar(circuito, p):  # p = parâmetros do §14.2
    # 1. Guardas (R-03, R-06, R-07, R-08, §12.7)
    if circuito.tensao_v is None: return erro("ERRO-TENSAO-AUSENTE")
    if p.isolacao is None:        return erro("ERRO-ISOLACAO-AUSENTE")
    if p.metodo is None:          return erro("ERRO-METODO-AUSENTE")
    if p.material == "Al" and not aluminio_admitido(p):   # 6.2.3.8
        return erro("ERRO-MATERIAL-NAO-ADMITIDO")
    validar_compatibilidade_linha(p)                      # Tabela 33

    IB = Decimal(circuito.corrente_projeto_a)

    # 2. Condutores carregados — Tabela 46 (NUNCA por num_fases isolado)
    n_carr, fator_neutro = condutores_carregados(
        circuito.num_fases, circuito.tem_neutro, circuito.taxa_h3)
    # 2F+N → 3; 3F+N com TH3>15% → base 3 carregados × 0,86

    # 3. Fatores de correção (fontes obrigatórias)
    FCT = fator_temperatura(p.isolacao, p.temperatura_c, meio(p.metodo))   # Tab. 40
    FRS = fator_resistividade(p) if p.metodo == "D" else 1                 # Tab. 41
    FCA = 1 if p.isencao_espacamento_2d else fator_agrupamento(
        p.disposicao, num_efetivo_circuitos(p))            # Tab. 42–45; 6.2.5.5.2
    f_total = FCT * FRS * FCA * (fator_neutro or 1)
    if f_total <= 0 or algum_fator_ausente(): return erro("ERRO-FATOR-NAO-ENCONTRADO")

    # 4. C1 — capacidade: IB' = IB / f_total; menor seção com Iz_base ≥ IB'
    ib_ficticia = IB / f_total
    s_c1, iz_base = menor_secao_por_iz(p, n_coluna(n_carr), ib_ficticia)
    if s_c1 is None: return status("REQUER-ESTUDO-PARALELO")  # §12.9

    # 5. C6 — mínimo por aplicação (Tabela 47 + pisos de Al do §12.7)
    s_c6 = secao_minima(circuito.tipo, p.material, p.tipo_condutor)

    # 6. C2 — sobrecarga (5.3.4.1) sobre a seção candidata
    #    In: informado, do MOD-PROT, ou SUGESTAO parametrizável
    #    a) IB ≤ In ≤ Iz_corrigida(secao)   b) I2 ≤ (1,45 ou 1,0)·Iz — I2 real ou PENDENTE-I2
    s_c2 = menor_secao_que_atende_sobrecarga(p, n_carr, f_total, IB)

    # 7. Seção candidata de fase e laço de revalidação
    s_fase = proxima_na_serie(max(s_c1, s_c2 or 0, s_c6))
    s_fase = revalidar_todos_os_criterios(s_fase, ...)  # inclui retornos de QT/CC/SEC

    # 8. Neutro (§12.8), PE (§12.10), PEN quando TN-C
    s_neutro = dimensionar_neutro(circuito, s_fase, circuito.taxa_h3)
    s_pe     = dimensionar_pe(s_fase, p)                 # Tabela 58
    # 9. Estado, critério decisivo, rastreio, memória de cálculo
    return montar_resultado(...)
```

Invariantes obrigatórios (testes de propriedade): aumentar IB nunca reduz seção; reduzir fator de correção nunca aumenta Iz corrigida; seção final ≥ toda seção por critério aplicável; seção final ∈ série; pendência obrigatória impede completude; override não apaga rastreio; Iz(seção maior) ≥ Iz(seção menor) em condições iguais.

## 17. RASTREABILIDADE E MEMÓRIA DE CÁLCULO

`rastreio` por circuito registra: por critério — tabela consultada (nº da edição 2004), linha (seção), coluna (método × nº de carregados), notas aplicadas, página, `chunk_id`, valores intermediários (IB, f_total e cada fator com fonte, IB', Iz_base, Iz_corrigida, margem, % de utilização); versão do módulo (`MOD-DC-v3.0`), versão da base normativa, versão do motor Python e das bibliotecas fixadas, data/hora, identificador da execução, origem de cada dado (`IMPORTADO`|`CALCULADO`|`NORMATIVO`|`SUGESTAO`|`OVERRIDE`+justificativa). A área "Como este resultado foi obtido" da UI é renderizada exclusivamente a partir desse objeto — nenhuma recomputação na camada visual.

## 18. MOTOR PYTHON E BIBLIOTECAS

- Python com Pydantic v2 (contratos), `Decimal` (comparações normativas, R-09), `pytest` (testes). `Pint` para controle de unidades **se** for adotado, com versão fixada e testes próprios; alternativa aceita: tipos de unidade próprios validados. `pandas`/`NumPy` apenas para carga e verificação das tabelas normativas — nunca como fonte de valores.
- Proibido: bibliotecas de sistemas de potência (pandapower, PyPSA, GridCal) substituírem tabelas ou limites da NBR 5410; adaptação silenciosa de norma estrangeira; interpolação de seções; `eval`; instalação de pacotes em produção.
- Toda biblioteca adotada exige: finalidade documentada, versão fixada (`pyproject.toml`/`requirements.txt`), teste independente de pelo menos um cálculo crítico (ex.: reconstrução manual de IB' e Iz corrigida do CA-DC-02), registro de limitações, participação declarada no rastreio.
- Falha de biblioteca (indisponível, erro, resultado não físico): interromper a aprovação afetada, registrar, marcar `VERIFICAR`, nunca substituir silenciosamente.
- Arquitetura em camadas (validação → unidades → contexto normativo → tabelas versionadas → regras → verificações independentes → seleção → rastreabilidade → resultado), com classes separadas: `ValidadorEntradas`, `RepositorioNormativo`, `MotorCapacidadeCorrente`, `MotorSobrecarga`, `MotorCondutorNeutro`, `MotorCondutorProtecao`, `SeletorSecaoNormalizada`, `GeradorRastreabilidade`, `VerificadorIndependente`, e adaptadores `ContratoQT`, `ContratoCC`, `ContratoSEC`, `ContratoPROT`. Não concentrar cálculo, persistência, UI e regra na mesma classe.

## 19. API — FastAPI

Manter os endpoints do v2 com estas alterações:
- `POST /api/v1/projetos/{p}/circuitos/{c}/dimensionar` e `POST /api/v1/projetos/{p}/dimensionar-lote`: corpo conforme §14.2; o lote aplica padrões **declarados** + overrides por circuito; resposta traz `criterios` (C1–C6) e `pendencias` por circuito.
- `GET /api/v1/projetos/{p}/dimensionamento`: inclui resumo por estado e por critério decisivo.
- `GET /api/v1/tabelas/{iz|fatores-temperatura|fatores-agrupamento|fatores-resistividade|secoes-minimas|tipos-linha}`: consulta da base normativa com `fonte` e `status_verificacao` em cada linha.
- `POST /api/v1/projetos/{p}/circuitos/{c}/retorno-qt|retorno-cc|retorno-seccionamento`: recebem os contratos dos §12.4–12.6 e disparam revalidação.
- Endpoint de lote com os 44 circuitos do proj-1: resposta < 2 s (CA-DC-11 herdado).

## 20. INTEGRAÇÕES (contratos explícitos)

| Integração | Recebe | Envia | Quando indisponível |
|---|---|---|---|
| Circuitos / IB | `CircuitoParaDimensionamento` | — | módulo não executa |
| MOD-QT | `{atende, queda_percentual, limite_aplicado, fonte}` | `{circuito, secao_candidata, material, isolacao, metodo, comprimento, IB, tensao, fases, fp}` | `AGUARDANDO-QT` |
| MOD-CC (futuro) | `{icc, tempo, integral_joule, aprovado, fonte}` | `{secao, material, isolacao, k, temp_inicial, temp_final}` | `AGUARDANDO-CC` |
| MOD-SEC (futuro) | `{aprovado, tempo_seccionamento, fonte}` | `{secao_fase, secao_pe, esquema, comprimento}` | `AGUARDANDO-SECCIONAMENTO` (TN/IT) ou `NAO-APLICAVEL` (TT) |
| MOD-PROT (futuro) | `{in, i2, norma_dispositivo, capacidade_interrupcao}` | `{IB, Iz_corrigida, secao}` | In vira `SUGESTAO`; I2 → `PENDENTE-I2` |
| Lista de materiais / Unifilar / Memorial | — | seções, cores, isolação, método, estados | consumidores exibem pendências, nunca as ocultam |

Todo retorno downstream que exija seção maior dispara `revalidar_todos_os_criterios` e atualiza o critério decisivo.

## 21. UX/UI — IBM Carbon

**Jornada:** identificação do circuito → revisão dos dados importados (badge de origem) → contexto normativo (perfil NBR + EDP, versões) → sistema elétrico → características do condutor (material, isolação — dropdown sem opção vazia, CA-DC-14) → tipo de linha (Tabela 33, com descrição e método derivado) → influências (temperatura, solo, TH3) → agrupamento (disposição, quantidade, isenção 2×D, exclusão ≤ 30% assistida) → proteção (In informado/sugerido, I2) → verificações por critério → comparação de alternativas → resultado → pendências → aprovação técnica (registra autor, data, versão dos dados).

**Modos:** assistido e avançado; edição individual e em lote; revisão por exceção.

**Prevenção de erros:** bloquear cálculo sem dados obrigatórios; nunca assumir tensão, isolação, método, material, nº de carregados ou TH3; padrões de lote sempre visíveis e editáveis; validar unidades; bloquear negativos; detectar inconsistência fases × tensão × sistema e função × cor; impedir aprovação com erro crítico; desfazer/restaurar valor calculado; registrar alterações.

**Tabela de resultados (DataTable Carbon):** colunas `#, Circuito, Tipo, IB, C1, C2, C6, C5(QT), C3(CC), C4(SEC), S fase, S neutro, S PE, Iz corr., In, Status`. Critério decisivo com célula destacada (borda/fundo sutil `$interactive-01`) **e** rótulo textual (nunca só cor). Pendências com ícone + texto. Filtros, ordenação, busca, agrupamento (quadro/ambiente/fase/status), colunas configuráveis, congelamento, seleção múltipla, edição em lote, resumo de erros, exportação estruturada.

**Painel de detalhe:** parâmetros com override; cadeia de cálculo (IB → fatores com fontes → IB' → tabela/linha/coluna → Iz base → Iz corrigida → margem e % de utilização); seções por critério com o decisivo destacado; verificações a) e b) de 5.3.4.1 com valores reais; pendências C3/C4/C5 sempre visíveis; área expansível **"Como este resultado foi obtido"** renderizada do `rastreio`.

**Comparação de cenários:** Cu × Al (quando admitido), PVC × EPR/XLPE (motivação técnica do 04_condutores: classe térmica 90 °C reduz seção quando C1 é decisivo), métodos, temperaturas, agrupamentos, seções candidatas; exibir impacto declarado em queda de tensão via MOD-QT; a opção mais barata nunca é marcada como "melhor" automaticamente.

**Resumo do projeto:** totais por estado, critério decisivo mais frequente, histograma de seções, aviso permanente enquanto existir qualquer circuito com C3/C4/C5 pendente.

**Linguagem visual:** diferenciar informação, recomendação, atenção, pendência, erro bloqueante, não aplicável, verificado, override, regra NBR × regra EDP, valor calculado × informado — sempre com texto/ícone/rótulo além de cor.

## 22. ACESSIBILIDADE

WCAG 2.1 AA: contraste ≥ 4,5:1 (validar programaticamente qualquer par de cores antes de usar), navegação completa por teclado, foco visível, labels associados, erros junto aos campos + resumo de erros, suporte a leitor de tela (tabela com cabeçalhos e `scope`), unidades consistentes (mm², A, °C, %), tooltips apenas complementares, responsividade desktop/tablet, densidade ajustável, zoom até 200%, confirmação de ações destrutivas, estados de carregamento/vazio/falha, textos de erro acionáveis (o que faltou + onde corrigir).

## 23. ERROS

Catálogo mínimo (código → condição → mensagem acionável): `ERRO-TENSAO-AUSENTE`, `ERRO-ISOLACAO-AUSENTE`, `ERRO-METODO-AUSENTE`, `ERRO-MATERIAL-NAO-ADMITIDO` (citar 6.2.3.8 e o contexto reprovado), `ERRO-LINHA-INCOMPATIVEL`, `ERRO-CONSULTA-INCOMPLETA`, `ERRO-TABELA-INCOMPLETA` (linha `[VERIFICAR]`), `ERRO-FATOR-NAO-ENCONTRADO`, `ERRO-AGRUPAMENTO-NAO-TABELADO`, `ERRO-COR-FUNCAO`, `INC-07` (seção fora da série), `REQUER-ESTUDO-PARALELO`, `PENDENTE-I2`, `VERIFICAR-NEUTRO-HARMONICAS`. Nenhum erro é convertido em alerta; nenhum alerta suprime pendência.

## 24. SEGURANÇA E RESPONSABILIDADE TÉCNICA

O sistema apoia e não substitui o responsável técnico: exibe fontes, registra overrides com autor/data/justificativa, diferencia sugestão de aprovação, bloqueia resultado sem dados, não emite conformidade, mantém histórico e reprocessamento, registra versão dos dados e do motor em toda aprovação, e declara que o resultado depende das condições reais da instalação. Execução em ambiente controlado: entradas validadas, sem `eval`, sem comandos de sistema, dados normativos separados do código, logs sem dados sensíveis.

## 25. CRITÉRIOS DE ACEITE

| ID | Critério | Verificação |
|----|----------|-------------|
| CA-DC-01 | ILU Cu PVC B1 30 °C, 1 circuito, IB=2,36 A → S fase = 1,5 mm² (C6 decisivo); status `DIMENSIONAMENTO-PARCIAL` com pendências C3/C4/C5 listadas | automatizado |
| CA-DC-02 | TUE 2F sem neutro (chuveiro 7 700 VA/220 V), Cu PVC B1, 3 agrupados em feixe, IB=34,65 A → n_carregados=2 (Tab. 46); IB'=34,65/(1,00×0,70)=49,5 A; coluna B1/2 → S C1 = 10 mm² (Iz base 57 A) | automatizado |
| CA-DC-03 | Bifásico **com** neutro → n_carregados = 3 (não 2) | automatizado |
| CA-DC-04 | `tensao_v=None` → `ERRO-TENSAO-AUSENTE`, nenhum cálculo | automatizado |
| CA-DC-05 | Isolação ausente → `ERRO-ISOLACAO-AUSENTE`; dropdown sem opção vazia | automatizado + inspeção |
| CA-DC-06 | Seção final ∈ série do §12.13 em 100% dos casos (INC-07) | automatizado |
| CA-DC-07 | Linha da base com `[VERIFICAR]` → `ERRO-TABELA-INCOMPLETA` | automatizado |
| CA-DC-08 | `rastreio` contém tabela/linha/coluna/nota/página/chunk_id, fatores e versões | inspeção |
| CA-DC-09 | Nenhum circuito atinge `VERIFICADO-COMPLETO` enquanto C3, C4 ou C5 pendentes | automatizado |
| CA-DC-10 | UI exibe os seis critérios e destaca o decisivo com rótulo textual | inspeção visual |
| CA-DC-11 | Lote com 44 circuitos do proj-1 < 2 s | performance |
| CA-DC-12 | In > Iz corrigida → verificação a) reprovada, C2 `REPROVADO`, sugestão de seção superior; nunca "ATENÇÃO" não bloqueante | automatizado |
| CA-DC-13 | Al em projeto **residencial** → `ERRO-MATERIAL-NAO-ADMITIDO` (6.2.3.8); Al em projeto industrial válido (≥16 mm², BA5, fonte própria) → admitido com piso 16 mm² | automatizado |
| CA-DC-14 | 3F+N com TH3 > 15% → 4 carregados, fator 0,86 aplicado e rastreado | automatizado |
| CA-DC-15 | Trifásico S_fase=35 mm², equilibrado, TH3≤15%, neutro protegido → neutro redutível a 25 mm² (Tab. 48); sem as condições → neutro = fase | automatizado |
| CA-DC-16 | S_fase=50 mm² → S_PE=25 mm²; S_fase=10 → PE=10; S_fase=25 → PE=16 (Tab. 58) | automatizado |
| CA-DC-17 | Neutro em cor não azul-clara ou PE em cor não verde/verde-amarela → `ERRO-COR-FUNCAO` | automatizado |
| CA-DC-18 | I2 ausente → `PENDENTE-I2`; I2 informado com fonte → condição b) avaliada com I2 real; `regime_sobrecarga_severo=True` → b) vira I2 ≤ Iz | automatizado |
| CA-DC-19 | Método D usa bloco "solo" da Tab. 40 (ref. 20 °C) e Tab. 41; métodos não-D usam bloco "ambiente" | automatizado |
| CA-DC-20 | Nenhuma seção atende → `REQUER-ESTUDO-PARALELO`, sem dimensionamento automático de paralelo | automatizado |
| CA-DC-21 | Retorno do MOD-QT exigindo seção maior → revalidação completa e novo critério decisivo | automatizado |
| CA-DC-22 | Texto branco sobre `#fa4d56` ausente em todos os estados (`test_ds04`) | automatizado |
| CA-DC-23 | Valores carregados da Tab. 36 conferem com a amostra do §12.2.1 | automatizado (regressão da base) |
| CA-DC-24 | Grupo de condutores não semelhantes (seções fora de 3 consecutivas normalizadas) → fator F = 1/√n aplicado, **substituindo integralmente** qualquer fator tabelado (Tab. 42–45); n=10 → F≈0,316; alerta quando F < 0,30 | automatizado |
| CA-DC-25 | Nenhuma referência a numeração de tabelas da edição 1997 (Tab.31–34, Tab.37, Tab.42 como agrupamento multicamada, Tab.43 como seções mínimas) no código, dados ou UI — apenas numeração 2004 (§12.14) | automatizado (lint/grep) |

## 26. TESTES

Suíte `pytest` cobrindo: unitários (Tabela 46 incluindo 2F+N e TH3; fatores das Tabelas 40/41/42 com os valores confirmados; Tabela 47 completa; Tabela 48; Tabela 58; série normalizada; guardas R-03/R-06/R-07/R-08; alumínio §12.7; cores §12.11; **F=1/√n para grupos não semelhantes com exemplos de referência n=10→0,316 e n=30→0,183**); integração (retornos QT/CC/SEC, revalidação, lote proj-1; **F=1/√n substitui fator tabelado e não acumula**); fronteira (IB = Iz; IB ligeiramente superior com `Decimal`; temperatura fora da faixa; célula "–" da Tab. 40; agrupamento > 20; combinação ausente; dados contraditórios; concessionária fora do campo; **F<0,30 gera alerta de revisão de disposição**); propriedades (invariantes do §16); regressão da base normativa (CA-DC-23); **conformidade de nomenclatura (CA-DC-25 — nenhuma referência a tabelas ed. 1997)**; UX/acessibilidade (teclado, leitor de tela, contraste, bloqueio por pendência, resumo de erros). Estrutura `src/{dominio,calculos,normas,integracoes,rastreabilidade}` e `tests/{unitarios,integracao,regressao,normativos,propriedades}`, `data/normas/` versionado. Não inventar números para completar testes: casos que dependam de valores `[VERIFICAR]` ficam marcados `xfail` com referência ao item pendente.

Exemplos de fixtures (dados reais do proj-1): `ILUM-Dormitorio-1` (ILU, 300 VA, 127 V, IB 2,36 A, 1F+N) e `ADD-Banheiro-2-Chuveiro-2` (TUE, 7 700 VA, 220 V, IB 34,65 A, 2F sem neutro).

## 27. EXEMPLO NUMÉRICO DE REFERÊNCIA (memória de cálculo esperada)

Chuveiro 2F sem neutro, Cu, PVC, B1, 30 °C, 3 circuitos em feixe: n_carregados = 2 (Tab. 46); FCT = 1,00 (Tab. 40); FCA = 0,70 (Tab. 42, linha 1, 3 circuitos); IB' = 34,65/0,70 = 49,5 A; Tab. 36, B1, coluna 2 carregados: 6 mm² → 41 A (insuficiente), 10 mm² → 57 A (atende) → S C1 = 10 mm²; S C6 = 2,5 mm² (força); C2 com In informado 40 A: Iz corrigida(10 mm²) = 57×0,70 = 39,9 A < In=40 → **reprovado em 10 mm²**; 16 mm² → 76×0,70 = 53,2 A ≥ 40 → S C2 = 16 mm²; S fase = 16 mm², critério decisivo C2; condição b) pendente até I2; C3/C4/C5 pendentes → `DIMENSIONAMENTO-PARCIAL`. (Este exemplo corrige o cenário do v2 §7.3, que sinalizava In > Iz como mera "ATENÇÃO".)

## 28. PENDÊNCIAS [VERIFICAR]

| ID | Item | Fonte necessária | Impacto |
|----|------|------------------|---------|
| VER-DC-01 | Valores completos das Tabelas 36–39 (todas as seções, métodos, Cu e Al, 2 e 3 carregados; colunas E/F/G) | NBR 5410:2004 original | Bloqueante para C1 fora da amostra confirmada |
| VER-DC-02 | Valores completos das Tabelas 43, 44 e 45 | NBR 5410:2004 | Bloqueante para múltiplas camadas e linhas enterradas |
| ~~VER-DC-03~~ | ~~Fórmula do fator F de 6.2.5.5.5 b)~~ — **RESOLVIDO**: F = 1/√n, confirmado por imagem do original (p. 119) e Guia EM (chunks 7–8). Incorporado em §12.2.5. | NBR 5410:2004, p. 119 | Resolvido |
| VER-DC-04 | Relação I2/In por norma de dispositivo (NBR NM 60898, NBR IEC 60947-2, IEC 60269) | Normas de dispositivo / MOD-PROT | Bloqueia condição b) sem I2 informado |
| VER-DC-05 | Série comercial de In de disjuntores | IEC 60898 / fabricantes | In automático permanece `SUGESTAO` |
| VER-DC-06 | Transcrição integral da Tabela 33 (tipos de linha) | NBR 5410:2004 | Limita o seletor de tipo de linha |
| VER-DC-07 | Presença de 800/1000 mm² nas tabelas 38/39 e correspondência da série com a IEC 60228 | NBR 5410:2004 / IEC 60228 | Baixo (extremo da série) |
| VER-DC-08 | Anexo F (neutro com TH3 > 33%) | NBR 5410:2004 Anexo F | Bloqueia neutro nesses casos |
| VER-DC-09 | Detalhes de 5.1.2.2.4 (seccionamento automático) | NBR 5410:2004 | Necessário ao MOD-SEC |
| ~~VER-DC-10~~ | ~~Conteúdo do anexo `06_dimensionamento_chunks.json`~~ — **RESOLVIDO**: 18 chunks analisados (Guia EM da NBR 5410, capítulo "Dimensionamento de circuitos"). Conteúdo: material explicativo/didático, sem requisitos normativos adicionais além dos já extraídos da NBR 5410:2004. Principais contribuições incorporadas: confirmação de F=1/√n (§12.2.5), regra de substituição integral do fator tabelado, alerta para F<0,30, numeração de tabelas da edição 1997 mapeada (Tab.37→42, Tab.31–34→36–39, Tab.43→47, Tab.34→40, Tab.42→43). Dimensionamento econômico (IEC 60287-3-2) registrado como funcionalidade futura fora do escopo atual. | Guia EM (06_dimensionamento) | Resolvido |
| VER-DC-11 | Padrão EDP para ramal de entrada subterrâneo | PT "Ramal de Entrada Subterrâneo – BT" | Fora do perfil atual |
| VER-DC-12 | Tabelas 56/57 completas (k para PE por cálculo adiabático) | NBR 5410:2004 | Método alternativo de PE |

## 29. NÃO TOCAR

M�dulo de Cargas; Módulo de Demanda (fórmula EDP D = a+b+…+i e fatores); Módulo IB; Adaptador 1:1 de circuitos (provisório, `provisorio=True`); Módulo de Categoria de Entrada (Saída A/Saída B); Tabelas 001/002 EDP (subcategorias e ramal); mapeamento de fases R/S/T e helper ABC→RST; Módulo de Queda de Tensão (apenas consumir o contrato); guardas INC-01, INC-04, INC-07 existentes.

## 30. CHECKLIST DE ENTREGA

- [ ] Os seis critérios de 6.2.6.1.2 modelados; nenhum status de completude com pendência.
- [ ] Tabela 46 implementada (incluindo 2F+N = 3 e fator 0,86) e testada.
- [ ] Tabelas 40/41/42 populadas com os valores confirmados deste prompt; demais linhas `[VERIFICAR]` bloqueiam uso.
- [ ] Alumínio bloqueado fora dos contextos de 6.2.3.8; Tabela 47 completa (16 Al).
- [ ] Condição b) de 5.3.4.1 com I2 real ou `PENDENTE-I2`; nada de I2 = 1,45·In implícito.
- [ ] Neutro, PE e PEN dimensionados com Tabelas 48/58 e mínimos de 6.4.3.
- [ ] Cores validadas (6.1.5.3 + EDP ramal).
- [ ] Contratos QT/CC/SEC/PROT publicados; revalidação em retorno.
- [ ] Rastreio completo (tabela/linha/coluna/nota/página/chunk_id/versões) alimentando "Como este resultado foi obtido".
- [ ] Numeração de tabelas exclusivamente da edição 2004 (nunca a de 1997 do material explicativo).
- [ ] Requisitos EDP restritos ao ramal de entrada e à área de concessão.
- [ ] `Decimal` nas comparações; precisão intermediária preservada; valores original e arredondado registrados.
- [ ] Versões fixadas; testes CA-DC-01 a CA-DC-25 verdes (exceto `xfail` documentados); WCAG AA validado por teste.

## 31. INSTRUÇÕES FINAIS

Implemente exatamente o especificado, em português do Brasil, sem valores inventados: toda lacuna vira `[VERIFICAR]` visível e bloqueante quando obrigatória. Corrija sem hesitar qualquer trecho herdado do MOD-DC-v2.0 que conflite com este prompt — as correções dos §§5, 12.1, 12.2.3, 12.2.5, 12.2.6, 12.3, 12.7 e 27 têm precedência. Diferencie sempre obrigação ("deve", "bloquear", "impedir") de recomendação e de sugestão. Não declare conformidade normativa em nenhum texto de UI; declare atendimento a critérios verificados, com fontes. Ao concluir, entregue: código tipado, base normativa versionada com status por linha, suíte de testes, arquivo de dependências com versões fixadas, e documentação das limitações e pendências deste prompt.
