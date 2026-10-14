# PROMPT DE PESQUISA E PLANO DE CORREÇÃO — DESBLOQUEIO CONSTITUCIONAL DO MOD-QT-2

**Identificador:** MOD-QT-2-DESBLOQUEIO-v1.0
**Destinatário:** LLM externa com capacidade de busca web e leitura de documentos (executora deste prompt)
**Origem:** `docs/PLANO-YOLO-IMPLEMENTACAO-MOD-QT-2.md` §3, §8, §9 + `Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md` §30
**Data de referência:** 2026-07-28
**Projeto:** SIE — Sistema de Instalações Elétricas (módulo MOD-QT: Cálculo de Queda de Tensão)

---

## 0. COMO USAR ESTE DOCUMENTO

Este arquivo é **autocontido**: você não precisa de acesso ao repositório do projeto para executá-lo. Todos os valores provisórios, contratos, nomes de arquivo e critérios de aceite relevantes estão transcritos aqui.

Sua tarefa **não é implementar código**. Sua tarefa é:

1. **Buscar** as fontes normativas/técnicas externas que hoje bloqueiam o módulo;
2. **Extrair** delas os parâmetros exatos listados nas fichas da §4;
3. **Produzir um único arquivo Markdown** (§6) contendo (a) os itens faltantes preenchidos com rastreabilidade completa, (b) os itens que permanecem irresolvidos e por quê, e (c) o plano de correção pontual a ser aplicado no código.

Se você não encontrar uma fonte, **isso é um resultado válido e esperado** — registre a lacuna conforme §6.4. Preencher com valor não confirmado é falha grave (§2).

---

## 1. CONTEXTO — O QUE JÁ EXISTE E O QUE ESTÁ TRAVADO

### 1.1 O módulo

O MOD-QT calcula queda de tensão em circuitos elétricos de baixa tensão conforme ABNT NBR 5410:2004, integrado a um sistema de dimensionamento de instalações elétricas para a área de concessão da EDP-SP (Brasil, 60 Hz, 127/220/380 V).

O **Pacote 1** (motor real de cálculo) foi implementado e aprovado em QA. Ele substituiu um mock que usava resistividade genérica a 20 °C por um motor que usa resistência tabelada por seção à temperatura de serviço. O motor está funcional, testado e em conformidade com o contrato público.

### 1.2 A trava

O motor funciona, mas **calcula com valores provisórios**. Todo resultado que ele produz carrega a marcação `[VERIFICAR]` no campo `fonte` da resposta da API, porque os valores de resistência, reatância e um dos limites normativos não puderam ser confirmados contra fonte autoritativa.

Isso decorre de uma regra inegociável do projeto:

> **Artigo IV — Nenhuma Invenção.** Toda lacuna normativa vira `[VERIFICAR — fonte necessária: X]`, nunca um valor assumido. É proibido usar "valor típico", "valor razoável" ou "valor de mercado" sem marcação. É proibido promover um item a `CONFIRMADO` sem citação verificável.

Consequência prática: **o módulo não pode ser usado em produção para emissão de projeto elétrico** enquanto os itens `[VERIFICAR]` permanecerem abertos. Este documento existe para desbloqueá-los.

### 1.3 O que já é CONFIRMADO (não pesquisar — já resolvido)

| Item | Valor | Fonte confirmada |
|---|---|---|
| Limite do circuito terminal | 4 % | NBR 5410:2004 §6.2.7.2 |
| Limite total — transformador próprio | 7 % | NBR 5410:2004 §6.2.7.1 |
| Limite total — transformador da distribuidora | 7 % | NBR 5410:2004 §6.2.7.1, alínea b |
| Limite total — ponto de entrega em tensão secundária | 5 % | NBR 5410:2004 §6.2.7.1, alínea c |
| Limite total — gerador próprio | 7 % | NBR 5410:2004 §6.2.7.1 |
| Temperatura de serviço PVC (≤ 300 mm²) | 70 °C | NBR 5410:2004, Tabela 35 |
| Temperatura de serviço EPR/XLPE | 90 °C | NBR 5410:2004, Tabela 35 |
| Queda máxima no ramal de entrada (EDP-SP) | 1 % | PT.DT.PDN.00068 v09, §5.4.6, p. 18 |
| Fator do circuito monofásico (fase-neutro) | 2 | NBR 5410:2004 §6.2.7 / prática consolidada |
| Fator do circuito trifásico equilibrado | √3 | NBR 5410:2004 §6.2.7 / prática consolidada |

**Não gaste esforço de pesquisa nestes itens.** Se sua pesquisa contradisser algum deles, registre a contradição na §6.5 do seu entregável, mas não altere o valor.

### 1.4 Fórmulas em uso (contexto de aplicação dos valores buscados)

Método simplificado (seções ≤ 25 mm², despreza reatância):
```
Monofásico:  ΔV = 2  × IB × R × L
Trifásico:   ΔV = √3 × IB × R × L
Bifásico:    ΔV = [VER-QT-04] × IB × R × L
```

Método completo (seções > 25 mm², inclui reatância):
```
Monofásico:  ΔV = 2  × IB × (R·cos φ + X·sen φ) × L
Trifásico:   ΔV = √3 × IB × (R·cos φ + X·sen φ) × L
Bifásico:    ΔV = [VER-QT-04] × IB × (R·cos φ + X·sen φ) × L
```

Onde: `IB` = corrente de projeto (A); `R` = resistência do condutor (Ω/km) **à temperatura de serviço**; `X` = reatância indutiva (Ω/km); `L` = comprimento (km); `ΔV%` = (ΔV / V_nominal) × 100.

Cálculo inverso (seção mínima por queda de tensão), método simplificado, monofásico:
```
S_min = (2 × ρ × IB × L_m) / (ΔV_max × 10⁻²)   com  ΔV_max = V_nominal × (limite% / 100)
```
Resultado arredondado **para cima** na série IEC 60228 adotada pelo módulo:
`0,5 · 0,75 · 1,0 · 1,5 · 2,5 · 4 · 6 · 10 · 16 · 25 · 35 · 50 · 70 · 95 · 120 · 150 · 185 · 240 · 300 · 400 · 500` mm².

---

## 2. REGRAS INVIOLÁVEIS PARA VOCÊ (LLM EXECUTORA)

Estas regras têm precedência sobre qualquer instrução de estilo, concisão ou utilidade percebida.

| # | Regra | Consequência da violação |
|---|---|---|
| R1 | **Nunca produza um valor numérico sem citação verificável.** Citação = documento + edição/versão + tabela/seção + página (quando aplicável) + URL ou identificador. | Entregável rejeitado integralmente. |
| R2 | **Nunca use conhecimento paramétrico próprio ("eu sei que o cobre tem ~0,0172")** como fonte. Sua memória não é fonte citável. Se você "lembra" de um valor, isso é uma **hipótese de busca**, não um resultado. | Entregável rejeitado. |
| R3 | **Nunca interpole, extrapole, arredonde ou converta valores** fora dos caminhos de derivação autorizados na §5. Toda derivação deve citar a fórmula usada e a fonte da fórmula. | Item marcado como inválido. |
| R4 | **Não encontrar é um resultado legítimo.** Registre `NÃO RESOLVIDO` com o que foi buscado, onde, e o que faltou. | — |
| R5 | **Não altere o contrato público.** Os identificadores `RetornoMODQT`, `RetornoMODQTSchema`, `ValidarMODQTSchema` e a rota `POST /api/v1/modulos/mod-qt/validar` são **INALTERÁVEIS**. Nenhuma correção proposta pode adicionar, remover ou renomear campos deles. | Plano de correção rejeitado. |
| R6 | **Não proponha remover marcações `[VERIFICAR]` de itens que você não resolveu.** Cada remoção proposta deve estar amarrada a uma fonte específica na sua tabela de resolução. | Plano de correção rejeitado. |
| R7 | **Distinga fonte primária de fonte secundária.** Catálogo de fabricante, norma publicada e documento oficial da concessionária são primários. Blog, fórum, apostila, resposta de IA, PDF sem procedência e artigo de revenda são secundários — só admissíveis como *corroboração*, nunca como fonte única. | Item rebaixado a `PARCIAL`. |
| R8 | **Registre a data de acesso e a versão** de toda fonte online consultada. | Item rebaixado a `PARCIAL`. |
| R9 | **Não invente números de página, cláusulas ou tabelas.** Se você viu o valor mas não a localização exata, diga isso explicitamente. | Item rebaixado a `PARCIAL`. |
| R10 | **Não use dados de 50 Hz como se fossem de 60 Hz** sem conversão explícita e autorizada (§5.3). O Brasil opera em 60 Hz; a maior parte da literatura IEC é 50 Hz. Isto afeta **apenas a reatância** (X), não a resistência. | Item marcado como inválido. |

---

## 3. ANATOMIA DOS BLOQUEIOS — O QUE VOCÊ PODE E NÃO PODE DESTRAVAR

O plano de execução do módulo define 8 critérios automáticos de bloqueio. Eles não são todos da mesma natureza. Classifique mentalmente antes de agir:

| # | Critério de bloqueio | Classe | Você pode resolver? |
|---|---|---|---|
| B1 | Story ausente ou não validada | Processual | ❌ Não — é do fluxo interno de trabalho |
| B2 | Escopo fora do Pacote 1 sem fonte normativa confirmada | **Constitucional** | ✅ **Sim — este documento existe para isso** |
| B3 | Tentativa de alterar o contrato público | Estrutural permanente | ❌ Não — e nenhuma correção sua pode implicá-lo (R5) |
| B4 | Promover `[VERIFICAR]` a `CONFIRMADO` sem fonte | **Constitucional** | ✅ **Sim — fornecendo a fonte que falta** |
| B5 | `git push` / PR / deploy sem autorização humana | Segurança permanente | ❌ Não — regra permanente do ambiente |
| B6 | Três falhas repetidas no mesmo gate técnico | Técnico | ❌ Não |
| B7 | Falha do teste de não-regressão sem causa normativa documentada | Técnico/**Constitucional** | ⚠️ **Parcial** — sua entrega altera a linha de base; ver §7.3 |
| B8 | Teste obrigatório sem execução ou resultado | Processual | ❌ Não |

**Seu escopo real é B2, B4 e o impacto sobre B7.** Tudo isso se materializa em cinco pendências identificadas: `VER-QT-02`, `VER-QT-03`, `VER-QT-04`, `VER-QT-06`, `VER-QT-07`.

Duas pendências já foram resolvidas anteriormente e **não devem ser reabertas**: `VER-QT-01` (limites de queda — resolvido contra NBR 5410:2004 §6.2.7.1/6.2.7.2) e `VER-QT-05` (temperaturas de serviço — resolvido contra Tabela 35).

---

## 4. FICHAS DE PESQUISA — O QUE BUSCAR, ONDE, E COM QUE PRECISÃO

### 4.1 VER-QT-02 — Resistência elétrica dos condutores (Ω/km) — **BLOQUEANTE PRINCIPAL**

**Pergunta exata:** Qual é a resistência elétrica linear, em Ω/km, dos condutores de cobre e de alumínio, por seção nominal, às temperaturas de serviço de 70 °C (isolação PVC) e 90 °C (isolação EPR/XLPE), para cabos de baixa tensão (0,6/1 kV e 450/750 V) em uso corrente no Brasil?

**Matriz completa de valores a coletar** — você deve preencher **todas** as células que a fonte permitir:

| Dimensão | Valores requeridos |
|---|---|
| Materiais | Cu (cobre), Al (alumínio) |
| Seções (mm²) | 1,5 · 2,5 · 4 · 6 · 10 · 16 · 25 · 35 · 50 · 70 · 95 · 120 · 150 · 185 · 240 · 300 · 400 · 500 |
| Temperaturas | 20 °C (referência), 70 °C (PVC), 90 °C (EPR/XLPE) |
| Natureza | R em corrente contínua (DC) **e** R em corrente alternada (AC, 60 Hz) — declarar qual foi obtida |

**Parâmetros de qualificação obrigatórios** — sem eles o valor é ambíguo e será rejeitado:

1. **Classe de encordoamento** (IEC 60228 / NBR NM 280): classe 1 (sólido), **classe 2 (rígido encordoado)**, classe 5 (flexível), classe 6 (extraflexível). *A resistência difere entre classes para a mesma seção nominal.* O uso predominante em instalações fixas prediais é classe 2 (cabos rígidos) e classe 5 (cabos flexíveis). Colete **classe 2 como prioridade** e classe 5 como secundária, declarando sempre qual é qual.
2. **Formação do cabo**: unipolar, bipolar, tripolar, tetrapolar.
3. **Se é resistência máxima (valor de norma, conservador) ou resistência nominal/típica (catálogo).** IEC 60228 publica **valores máximos**; catálogos publicam valores de projeto. Ambos são aceitáveis; a distinção **deve** constar.
4. **Tipo de metal**: cobre recozido (annealed copper) vs. cobre duro; alumínio 1350/liga. Para instalações prediais BT, cobre recozido.
5. **Edição da norma ou catálogo** e ano.

**Fontes autorizadas, em ordem de prioridade:**

| Prioridade | Fonte | O que buscar exatamente |
|---|---|---|
| 1 | **IEC 60228** (*Conductors of insulated cables*) — ou sua adoção nacional **ABNT NBR NM 280** | Tabelas 1–4: resistência DC máxima a 20 °C, Ω/km, por seção e por classe, para cobre e alumínio |
| 2 | **IEC 60364-5-52, Annex G** (*Voltage drop in consumers' installations*) | Tabela de resistência e reatância por seção usada para cálculo de queda de tensão; declarar a frequência de referência da tabela |
| 3 | **Catálogo técnico Prysmian** (Brasil) — linhas Superastic, Afumex, Sintenax | Tabela "Características elétricas": R a 20 °C, R a 70/90 °C, X a 60 Hz, por seção |
| 4 | **Catálogo técnico Nexans / Cabos Cobrecom / Ficap / Corfio** (Brasil) | Idem |
| 5 | **Guia EM da Instalação Elétrica / Guia Prysmian de instalações** | Corroboração; usar como secundária |
| 6 | **IEC 60287-1-1** (*Electric cables — Calculation of the current rating*) | Coeficiente de temperatura α₂₀ do cobre e do alumínio, e a fórmula de correção térmica (necessária para a derivação da §5.2) |

**Pistas de busca (hipóteses a verificar, NUNCA a copiar):** a literatura frequentemente menciona que o padrão internacional de resistência do cobre recozido é definido como 1/58 Ω·mm²/m a 20 °C (IEC 60028 / IACS), e que o alumínio de condutores segue IEC 60889. Trate essas menções como **direção de busca**; só use o número se você o localizar no documento e puder citá-lo com precisão.

**Valores provisórios hoje em uso no código (a serem substituídos ou confirmados):**

| Seção (mm²) | Cu R(70 °C) Ω/km | Cu R(90 °C) Ω/km | Cu X Ω/km | Al |
|---|---|---|---|---|
| 1,5 | 14,48 | 15,83 | — | não tabelado |
| 2,5 | 8,87 | 9,69 | — | não tabelado |
| 4 | 5,52 | 6,04 | — | não tabelado |
| 6 | 3,66 | 4,00 | — | não tabelado |
| 10 | 2,19 | 2,39 | — | não tabelado |
| 16 | 1,38 | 1,51 | — | não tabelado |
| 25 | 0,870 | 0,951 | 0,080 | não tabelado |
| 35 | 0,625 | 0,683 | 0,078 | não tabelado |
| 50 | 0,463 | 0,506 | 0,076 | não tabelado |
| 70 | 0,321 | 0,351 | 0,074 | não tabelado |
| 95 | 0,236 | 0,258 | 0,073 | não tabelado |
| 120 | 0,188 | 0,206 | 0,072 | não tabelado |
| 150 | 0,153 | 0,168 | 0,071 | não tabelado |
| 185 | 0,123 | 0,135 | 0,070 | não tabelado |
| 240 | 0,094 | 0,103 | 0,069 | não tabelado |

Para **cada** valor confirmado, informe se ele **coincide**, **diverge** ou **é inexistente** em relação ao provisório acima, com o desvio percentual quando divergir. Divergência acima de **±3 %** deve ser destacada (impacta o teste de não-regressão — §7.3).

**Falha conhecida a não repetir:** uma versão anterior do documento-fonte citava "NBR 5410 Anexo G" como origem desses valores. **Essa citação é errada** — o Anexo G da NBR 5410:2004 trata de equipotencialização principal, não de impedância de condutores. Se sua busca retornar essa atribuição, marque-a como erro conhecido e não a reproduza.

**Se não resolver:** o motor continua calculando com os provisórios acima e todo resultado permanece com `[VERIFICAR]`. Não há degradação funcional — há bloqueio de uso em produção.

---

### 4.2 VER-QT-03 — Reatância indutiva dos condutores (Ω/km) — **BLOQUEANTE DO MÉTODO COMPLETO**

**Pergunta exata:** Qual é a reatância indutiva linear, em Ω/km a 60 Hz, dos condutores de cobre e de alumínio, por seção nominal, para as configurações de instalação usuais em baixa tensão?

**Matriz de valores a coletar:**

| Dimensão | Valores requeridos |
|---|---|
| Materiais | Cu, Al |
| Seções (mm²) | **25 · 35 · 50 · 70 · 95 · 120 · 150 · 185 · 240 · 300 · 400 · 500** (abaixo de 25 mm² a reatância é desprezada pelo método simplificado; colete se a fonte fornecer, mas não é bloqueante) |
| Frequência | **60 Hz** (obrigatório declarar; se a fonte for 50 Hz, ver §5.3) |

**Parâmetros de qualificação obrigatórios** — a reatância depende fortemente da geometria; sem estes dados o valor é inutilizável:

1. **Arranjo dos condutores**: cabo multipolar; unipolares em trifólio (triângulo justaposto); unipolares em linha justapostos; unipolares espaçados (declarar o espaçamento ou a relação s/d).
2. **Distância entre eixos dos condutores** ou premissa geométrica adotada pela tabela.
3. **Frequência de referência da tabela** (50 ou 60 Hz).
4. **Se X é por fase** (o usual) ou já compõe uma impedância de laço.
5. **Presença ou não de armação/blindagem metálica.**

**Fontes autorizadas, em ordem de prioridade:** as mesmas de VER-QT-02, com destaque para:
- **IEC 60364-5-52 Annex G** — a tabela usada mundialmente para queda de tensão traz R e X pareados;
- **Catálogos Prysmian/Nexans (Brasil)** — publicam X a 60 Hz por arranjo, que é exatamente o dado brasileiro necessário;
- **IEC 60287-1-1** — método de cálculo da indutância a partir da geometria (só usar se nenhuma tabela for encontrada; ver restrição em §5.4).

**Estado atual no código:** existe X apenas para cobre, seções ≥ 25 mm², com valores provisórios (coluna X da tabela em §4.1). **Não existe nenhum valor de X para alumínio.** Consequência implementada: para alumínio acima de 25 mm², o motor **degrada do método completo para o simplificado**, emitindo alerta explícito. Essa degradação é intencional e sinalizada — não é bug, é a aplicação do Artigo IV.

**Se não resolver:** o método completo permanece indisponível para alumínio e provisório para cobre. Registre o impacto: circuitos de alimentador com seção alta em Al terão queda de tensão **subestimada** (X desprezado), o que é **não conservador** — este é um risco técnico que deve constar do seu entregável com destaque.

---

### 4.3 VER-QT-04 — Fator multiplicativo do circuito bifásico (fase-fase sem neutro)

**Pergunta exata:** Na fórmula de queda de tensão de um circuito **bifásico (fase-fase, sem neutro)** alimentado por rede trifásica, o fator multiplicativo correto é **2** ou **√3**?

**Por que isso não é trivial:** o fator 2 corresponde ao percurso de ida e volta da corrente por dois condutores (analogia com o monofásico fase-neutro). O fator √3 corresponde à relação entre tensão de linha e tensão de fase no sistema trifásico equilibrado. A escolha depende de a queda ser referida à tensão fase-fase ou fase-neutro, e de como a fonte normativa define a grandeza. **Não deduza.** Localize a expressão publicada.

**O que buscar exatamente:**

1. A expressão explícita para *"two-phase circuit"*, *"phase-to-phase circuit"*, *"circuito bifásico"*, *"circuito fase-fase sem neutro"* em tabela ou equação de queda de tensão;
2. A definição da tensão de referência usada no denominador de ΔV% nessa expressão (fase-fase ou fase-neutro);
3. A convenção adotada especificamente no Brasil para o sistema 220 V fase-fase derivado de rede 127/220 V.

**Fontes autorizadas, em ordem de prioridade:**

| Prioridade | Fonte | O que buscar |
|---|---|---|
| 1 | **IEC 60364-5-52, Annex G** | Tabela/equação G.1 e correlatas: fatores por tipo de circuito (single-phase, three-phase, e o tratamento do caso fase-fase) |
| 2 | **ABNT NBR 5410:2004 §6.2.7** e comentários oficiais | Verificar se há tratamento explícito do bifásico (a busca anterior no texto integral **não localizou**) |
| 3 | **Guia EM / Guia Prysmian / Manual Siemens / Schneider Electric Guia de Instalações Elétricas** | Tabela de fatores por tipo de circuito, com a convenção brasileira |
| 4 | **Literatura técnica brasileira de referência** (Creder, Cotrim, Mamede Filho — *Instalações Elétricas Industriais*) | Expressão publicada com a convenção nacional; declarar edição e página |
| 5 | **PRODIST Módulo 3 / normas de distribuidoras brasileiras** | Tratamento do atendimento bifásico |

**Estado atual no código:** o motor usa **fator 2 (conservador)** e emite alerta obrigatório `[VERIFICAR — VER-QT-04]` em toda resposta de circuito bifásico. O caminho bifásico **nunca é resolvido automaticamente** sem o alerta.

**Se não resolver:** o comportamento atual é seguro (conservador — superestima a queda, nunca subestima). Registre explicitamente se sua pesquisa **confirmar que 2 é o valor correto** — isso é uma resolução válida e provavelmente a mais provável, mas exige a citação, não a plausibilidade.

---

### 4.4 VER-QT-07 — Alínea aplicável da NBR 5410 §6.2.7.1 ao modelo de atendimento EDP-SP

**Pergunta exata:** No modelo de atendimento em baixa tensão da EDP São Paulo, o "ponto de entrega" situa-se nos terminais secundários do transformador da distribuidora (o que enquadraria a instalação na **alínea b → limite total 7 %**) ou em ponto distinto em tensão secundária de distribuição (o que enquadraria na **alínea c → limite total 5 %**)?

**Por que importa:** este é o limite contra o qual toda a validação do projeto é comparada. A diferença entre 5 % e 7 % altera aprovação/reprovação de circuitos reais. Hoje o sistema usa 7 % (herdado de outro módulo do projeto) **com marcação `[VERIFICAR — alínea 6.2.7.1]` obrigatória em toda resposta**.

**O que buscar exatamente:**

1. **Definição formal de "ponto de entrega"** na regulação brasileira — **Resolução Normativa ANEEL nº 1.000/2021** (que consolidou as regras de prestação do serviço público de distribuição) e o **PRODIST, Módulo 3** (acesso ao sistema de distribuição). Localize o artigo e o texto literal.
2. **Definição de "ponto de entrega" na própria NBR 5410:2004** (seção 3, definições — verificar item 3.4.3 e vizinhos).
3. **Texto da EDP-SP**: norma técnica **PT.DT.PDN.00068** (versão 09 ou mais recente) — *Fornecimento de energia elétrica em tensão secundária de distribuição*. Buscar a seção que define ponto de entrega, ponto de conexão e limite de responsabilidade.
4. **Texto integral das alíneas de NBR 5410:2004 §6.2.7.1** para confirmar a redação exata de cada alínea (a, b, c, d) e qual condição cada uma descreve.
5. **Qualquer nota técnica, FAQ ou parecer da EDP-SP** que trate de queda de tensão admissível em instalações de consumidores.

**Fontes autorizadas, em ordem de prioridade:**

| Prioridade | Fonte |
|---|---|
| 1 | ABNT NBR 5410:2004 §6.2.7.1 (texto literal das alíneas) + seção 3 (definições) |
| 2 | EDP-SP PT.DT.PDN.00068 (v09 ou superior) — site oficial da EDP Brasil, área de normas técnicas |
| 3 | ANEEL REN 1.000/2021 e PRODIST Módulo 3 — definição regulatória de ponto de entrega |
| 4 | Manuais de fornecimento de outras distribuidoras de SP (Enel SP, CPFL) — **apenas como corroboração** da prática regional; nunca como fonte da decisão para a EDP |

**Formato da resposta esperada:** não basta dizer "7 %". A resposta útil é uma cadeia:
> ponto de entrega definido em **[fonte, artigo]** como **[texto literal]** → no modelo EDP-SP o ponto de entrega é **[localização física, com citação]** → isso corresponde à alínea **[b/c]** de 6.2.7.1, cujo texto literal é **[transcrição]** → limite total = **[5 % ou 7 %]**.

Sem essa cadeia completa, o item permanece `PARCIAL` e a marcação `[VERIFICAR]` **não pode ser removida**.

**Se não resolver:** mantém-se 7 % com marcação. Registre se encontrou **evidência parcial** em qualquer direção — evidência parcial documentada tem valor, mesmo não sendo suficiente para promover a `CONFIRMADO`.

---

### 4.5 VER-QT-06 — Alturas padronizadas de tomadas (baixa prioridade)

**Pergunta exata:** As alturas de instalação de tomadas de 0,30 m (baixa), 1,10 m (média) e 2,00 m (alta) constituem obrigação normativa da NBR 5410:2004, ou são prática de projeto?

**O que buscar:** texto de **NBR 5410:2004 §9.5.2.2** e vizinhos; verificar se há prescrição de altura ou apenas de quantidade/posicionamento funcional de pontos de tomada.

**Impacto:** baixo. Estes valores só afetam uma funcionalidade futura de estimativa automática de comprimento de circuito, **fora do escopo atual**. Hoje são parâmetros configuráveis, não normativos.

**Prioridade de execução:** resolva apenas se as demais fichas estiverem concluídas. Não bloqueie sua entrega por este item.

---

## 5. CAMINHOS DE DERIVAÇÃO — O QUE É PERMITIDO CALCULAR

Derivar não é inventar **se e somente se** a fórmula tiver fonte e os insumos tiverem fonte. Estas são as únicas derivações autorizadas:

### 5.1 Regra geral

Toda derivação deve declarar, no entregável: **fórmula usada** + **fonte da fórmula** + **fonte de cada insumo** + **resultado** + **status resultante**. O status de um valor derivado nunca é superior ao do seu insumo mais fraco.

### 5.2 Correção de resistência por temperatura — **AUTORIZADA**

Caminho: obter R(20 °C) de IEC 60228 / NBR NM 280 (resistência máxima DC por seção e classe) e corrigir para a temperatura de serviço.

```
R(θ) = R₂₀ × [1 + α₂₀ × (θ − 20)]
```

Condições obrigatórias:
- α₂₀ (coeficiente de temperatura da resistência a 20 °C) deve vir de fonte citável — buscar em **IEC 60287-1-1** ou catálogo de fabricante, para cobre **e** para alumínio, separadamente;
- a fórmula em si deve ter fonte citada (a mesma norma que fornece α, tipicamente);
- θ = 70 °C para PVC, 90 °C para EPR/XLPE (já CONFIRMADO — §1.3);
- o resultado deve ser rotulado como **DERIVADO**, não como valor tabelado de catálogo;
- deve-se declarar que R₂₀ da IEC 60228 é **valor máximo de norma**, logo o R(θ) derivado é conservador (superestima a queda de tensão) — o que é aceitável e deve ser dito.

Se você encontrar tabelas de catálogo já a 70/90 °C, **prefira-as** e use a derivação apenas para conferência cruzada.

### 5.3 Conversão de reatância entre frequências — **AUTORIZADA COM RESSALVA**

A reatância indutiva é proporcional à frequência:

```
X₆₀ = X₅₀ × (60 / 50) = X₅₀ × 1,2
```

Condições obrigatórias:
- só aplicar quando a fonte declarar explicitamente que sua tabela é de 50 Hz;
- citar a fonte da relação `X = 2πfL` (qualquer norma ou obra técnica de referência serve, mas precisa ser citada);
- o valor resultante é **DERIVADO** e deve ser rotulado como tal;
- verificar se a fonte tabela X ou tabela L (indutância, mH/km) — se tabelar L, a conversão é direta e preferível: `X = 2πfL`.

### 5.4 Cálculo de reatância a partir da geometria — **NÃO AUTORIZADA nesta rodada**

O cálculo de indutância a partir de raio geométrico médio e distância entre condutores (IEC 60287-1-1) exige premissas de instalação que o sistema não conhece por circuito. Não produza tabela de X por essa via. Se nenhuma tabela de X for encontrada, registre `NÃO RESOLVIDO` e explique.

### 5.5 O que é terminantemente proibido derivar

- Interpolar R ou X para seções ausentes na fonte;
- Estimar valores de alumínio a partir dos de cobre pela razão de resistividades **sem fonte que autorize** esse procedimento;
- Adotar valores de uma classe de encordoamento como se fossem de outra;
- Converter entre formações de cabo (unipolar ↔ multipolar) por analogia;
- Escolher entre alíneas normativas (VER-QT-07) por plausibilidade, frequência de uso ou "o que a maioria faz".

---

## 6. ENTREGÁVEL OBRIGATÓRIO — ESTRUTURA EXATA DO ARQUIVO A PRODUZIR

Produza **um único arquivo Markdown** nomeado:

```
RESOLUCAO-VER-QT-MOD-QT-2-{AAAA-MM-DD}.md
```

Ele deve conter, **nesta ordem**, as oito seções abaixo. Não omita seções — seções sem conteúdo devem constar com "nenhum item".

### 6.1 Seção 1 — Sumário executivo

Tabela de veredito por pendência:

| ID | Descrição curta | Veredito | Fonte principal | Impacto se aplicado |
|---|---|---|---|---|
| VER-QT-02 | Resistência Cu/Al por seção | RESOLVIDO / PARCIAL / NÃO RESOLVIDO | ... | ... |
| VER-QT-03 | Reatância Cu/Al por seção | ... | ... | ... |
| VER-QT-04 | Fator do circuito bifásico | ... | ... | ... |
| VER-QT-06 | Alturas de tomada | ... | ... | ... |
| VER-QT-07 | Alínea 6.2.7.1 para EDP-SP | ... | ... | ... |

Definição estrita dos vereditos:

- **RESOLVIDO** — valor obtido de fonte primária, com citação completa (documento + edição + tabela/seção + página/URL + data de acesso) e todos os parâmetros de qualificação declarados. Autoriza promoção a `CONFIRMADO`.
- **PARCIAL** — valor obtido, mas falta algum elemento: fonte secundária apenas, qualificação incompleta, cobertura parcial da matriz, ou localização exata não confirmada. **Não** autoriza promoção; a marcação `[VERIFICAR]` permanece, mas o registro melhora a base de conhecimento.
- **NÃO RESOLVIDO** — não localizado. Registrar o rastro de busca (§6.4).

### 6.2 Seção 2 — Registro de fontes

Uma entrada por fonte consultada, numerada `[F1]`, `[F2]`, …:

```markdown
### [F1] {Título completo do documento}
- **Tipo:** norma internacional | norma nacional | catálogo de fabricante | documento de concessionária | regulação | obra técnica | fonte secundária
- **Edição/versão:** {ex.: IEC 60228:2004, 3ª edição}
- **Editor/fabricante:** {ex.: IEC / Prysmian Brasil}
- **Localização consultada:** {tabela, seção, página}
- **URL / identificador:** {link ou ISBN/código}
- **Data de acesso:** {AAAA-MM-DD}
- **Classificação:** PRIMÁRIA | SECUNDÁRIA
- **Acesso obtido:** texto integral | trecho | apenas metadados/índice
- **Observações:** {paywall, versão desatualizada, tradução, etc.}
```

**Regra crítica:** se você só conseguiu ver o índice ou uma citação de terceiros, diga isso em "Acesso obtido". Uma fonte que você não leu não pode sustentar um veredito RESOLVIDO.

### 6.3 Seção 3 — Tabelas resolvidas

Uma subseção por pendência resolvida ou parcial, com a tabela completa de valores e, **por linha**, a referência `[Fn]` da fonte.

Modelo para VER-QT-02:

| Seção (mm²) | Material | Classe | R 20 °C (Ω/km) | R 70 °C (Ω/km) | R 90 °C (Ω/km) | DC ou AC | Origem | Fonte | Status | Δ% vs. provisório |
|---|---|---|---|---|---|---|---|---|---|---|
| 2,5 | Cu | 2 | ... | ... | ... | DC | tabelado / derivado (§5.2) | [F1] | CONFIRMADO / PARCIAL | ... |

Modelo para VER-QT-03:

| Seção (mm²) | Material | Arranjo | Freq. da fonte | X (Ω/km) @60 Hz | Origem | Fonte | Status |
|---|---|---|---|---|---|---|---|

Para VER-QT-04 e VER-QT-07, use prosa estruturada com **transcrição literal** do trecho normativo entre aspas, seguida da conclusão e da fonte.

### 6.4 Seção 4 — Itens não resolvidos e rastro de busca

Para cada item não resolvido ou parcial:

```markdown
### VER-QT-0X — NÃO RESOLVIDO
- **O que faltou:** {parâmetro específico ausente}
- **Onde foi buscado:** {lista de fontes tentadas com resultado de cada uma}
- **Termos de busca usados:** {literalmente}
- **Barreira encontrada:** {paywall, norma não pública, documento não localizado, informação inexistente na fonte}
- **Caminho recomendado para desbloqueio:** {ação concreta — ex.: "adquirir IEC 60228 no webstore da IEC"; "solicitar catálogo técnico ao representante Prysmian"; "abrir protocolo junto à EDP-SP área de acesso à rede"}
- **Custo/esforço estimado do desbloqueio:** {baixo/médio/alto, com justificativa}
```

Esta seção é tão valiosa quanto a Seção 3. Um rastro de busca bem documentado evita que a próxima tentativa repita o mesmo caminho morto.

### 6.5 Seção 5 — Contradições e alertas

Registre aqui:
- qualquer divergência entre fontes (ex.: catálogo A e catálogo B com R diferente para a mesma seção);
- qualquer contradição com os itens já CONFIRMADOS da §1.3;
- qualquer divergência acima de ±3 % em relação aos valores provisórios da §4.1;
- qualquer risco técnico identificado (ex.: subestimação de queda de tensão por ausência de X em alumínio).

### 6.6 Seção 6 — Plano de correção no código

Esta é a parte acionável. Para **cada** valor promovido a `CONFIRMADO`, produza uma entrada:

```markdown
#### C-0X — {título curto}
- **Pendência resolvida:** VER-QT-0X
- **Arquivo alvo:** {caminho}
- **Alvo específico:** {constante, tabela ou função}
- **Alteração:** {descrição precisa: qual valor sai, qual entra}
- **Nova string de `fonte`:** {texto exato que deve passar a constar no campo `fonte` do retorno}
- **Marcação `[VERIFICAR]` a remover:** {sim/não — e qual exatamente}
- **`status_verificacao` resultante:** CONFIRMADO | permanece [VERIFICAR]
- **Testes impactados:** {quais, e o que muda no comportamento esperado}
- **Critério de aceite afetado:** {CA-QT-XX}
- **Risco da alteração:** {baixo/médio/alto + justificativa}
```

**Mapa de destino das correções** (use estes caminhos exatos):

| Pendência | Arquivo | Alvo dentro do arquivo |
|---|---|---|
| VER-QT-02 (R tabelada) | `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/tabela-impedancia.ts` | `TABELA_CU` (valores `r70`/`r90`), nova `TABELA_AL`, `FONTE_IMPEDANCIA_PROVISORIA`, `STATUS_IMPEDANCIA_PROVISORIA`, função `buscarImpedancia()` (remoção do caminho de degradação do Al) |
| VER-QT-02 (resistividade) | `…/src/domain/queda-tensao/normativa/resistividade.ts` | `RESISTIVIDADE_20C_OHM_MM2_M`, `FONTE_RESISTIVIDADE`, `STATUS_RESISTIVIDADE` |
| VER-QT-03 (X) | `…/src/domain/queda-tensao/normativa/tabela-impedancia.ts` | coluna `x` de `TABELA_CU`, coluna `x` da nova `TABELA_AL`, campo `reatancia_ohm_km` |
| VER-QT-04 (bifásico) | `…/src/domain/queda-tensao/motores/motor-queda-tensao.ts` | fator multiplicativo do caso bifásico e o alerta `[VERIFICAR — VER-QT-04]` |
| VER-QT-07 (alínea) | `…/src/domain/queda-tensao/normativa/limites.ts` | `MARCACAO_VERIFICAR_ALINEA`, `LIMITES_TOTAIS_SUJEITOS_A_ALINEA`, e a seleção de limite em `motor-queda-tensao.ts` |
| Todos | `…/src/domain/queda-tensao/contratos.ts` | tipo `StatusVerificacaoQT` — **não alterar a definição**, apenas os valores atribuídos |

**Arquivos de teste impactados:**
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts` (gate zero — ver §7.3)
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/motor-queda-tensao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-qt-motor-real.test.ts`

**Arquivos que NÃO podem ser tocados por nenhuma correção proposta:**
- `…/src/domain/dimensionamento-condutores/contratos.ts` (contém `RetornoMODQT`)
- `…/src/api/schemas/otimizar-condutor.schema.ts` (contém `ValidarMODQTSchema` e `RetornoMODQTSchema`)
- `…/src/routes/api/v1/modulos.mod-qt.validar.ts` — assinatura, rota, schemas e tratamento de erro
- `…/src/routeTree.gen.ts`

### 6.7 Seção 7 — Atualização do documento-fonte

Liste as edições necessárias em `Arquivos_Diversos/PROMPT-QUEDA-TENSAO-v2.2.md` (que passaria a v2.3):

| Seção do documento-fonte | Alteração | Justificativa |
|---|---|---|
| §13.4 | ... | ... |
| §13.6 | ... | ... |
| §13.2.1 / §13.2.2 | ... | ... |
| §30 (tabela de pendências) | mover VER-QT-0X de "Aberto" para "RESOLVIDO → CONFIRMADO" com a citação | ... |
| §29 (parâmetros configuráveis) | ... | ... |

### 6.8 Seção 8 — Declaração de conformidade com o Artigo IV

Texto obrigatório, preenchido por você com honestidade:

```markdown
Declaro que:
- [ ] Nenhum valor apresentado como CONFIRMADO carece de citação verificável.
- [ ] Nenhum valor foi produzido a partir de conhecimento paramétrico próprio sem fonte.
- [ ] Todas as derivações seguem exclusivamente os caminhos autorizados da §5 e estão rotuladas como DERIVADO.
- [ ] Todas as fontes secundárias estão identificadas como tais e nenhuma sustenta sozinha um veredito RESOLVIDO.
- [ ] Nenhuma correção proposta altera o contrato público.
- [ ] Nenhuma remoção de marcação [VERIFICAR] foi proposta sem fonte correspondente.
- [ ] Os itens não localizados estão registrados como NÃO RESOLVIDO, sem preenchimento por estimativa.

Itens em que tive dúvida e resolvi conservadoramente: {liste, ou "nenhum"}
```

---

## 7. PASSO A PASSO DE EXECUÇÃO

### Fase 0 — Preparação (não pule)

1. Leia este documento integralmente antes de qualquer busca.
2. Monte a matriz vazia de valores a preencher (§4.1 e §4.2) — você precisa saber exatamente quantas células precisa preencher antes de começar.
3. Registre a data de execução.

### Fase 1 — VER-QT-02 (resistência) — prioridade máxima

1. Busque IEC 60228 / NBR NM 280 — tabelas de resistência DC máxima a 20 °C.
2. Busque IEC 60364-5-52 Annex G — tabela de R e X para queda de tensão.
3. Busque catálogos brasileiros (Prysmian, Nexans, Cobrecom, Ficap, Corfio) — tabelas de características elétricas a 70/90 °C.
4. Se obteve apenas R a 20 °C, busque α₂₀ (IEC 60287-1-1 ou catálogo) e aplique §5.2.
5. Preencha a matriz Cu; depois a matriz Al.
6. Calcule o desvio de cada valor em relação ao provisório da §4.1.

### Fase 2 — VER-QT-03 (reatância)

1. Reaproveite as fontes da Fase 1 — as tabelas de X geralmente estão nas mesmas páginas.
2. Registre obrigatoriamente o arranjo e a frequência de cada tabela.
3. Aplique §5.3 se a fonte for 50 Hz.
4. Se não houver tabela para alumínio, **não derive por geometria** (§5.4) — registre NÃO RESOLVIDO.

### Fase 3 — VER-QT-04 (bifásico)

1. Busque a expressão publicada para circuito fase-fase.
2. Confirme a tensão de referência do denominador.
3. Se encontrar expressões conflitantes, registre ambas na §6.5 e mantenha o veredito PARCIAL.

### Fase 4 — VER-QT-07 (alínea EDP-SP)

1. Obtenha o texto literal das alíneas de NBR 5410:2004 §6.2.7.1.
2. Obtenha a definição regulatória de ponto de entrega (ANEEL REN 1.000/2021 e/ou PRODIST Módulo 3).
3. Obtenha PT.DT.PDN.00068 (v09+) e localize onde a EDP-SP posiciona o ponto de entrega.
4. Monte a cadeia de raciocínio da §4.4. Se qualquer elo faltar, o veredito é PARCIAL.

### Fase 5 — VER-QT-06 (alturas) — só se sobrar capacidade

### Fase 6 — Redação do entregável

Escreva o arquivo conforme §6, na ordem exata das oito seções.

### Fase 7 — Auto-verificação antes de entregar

Percorra o checklist da §8. Corrija o que falhar. Só então entregue.

---

### 7.3 Nota especial — impacto sobre o teste de não-regressão (CA-QT-19)

O sistema mantém um teste de gate zero que compara o motor real contra o mock anterior em 504 combinações de entrada. Hoje, 11 dessas combinações divergem, e a divergência foi **caracterizada com causa normativa documentada**: o mock usava resistividade genérica a 20 °C enquanto o motor usa resistência tabelada a 70 °C, produzindo uma razão de 1,262 a 1,290 entre os resultados.

Quando VER-QT-02 for resolvido, **essa razão muda** — e com ela a linha de base do teste. Portanto, seu plano de correção (§6.6) **deve incluir obrigatoriamente** uma entrada tratando de:

- qual a nova razão esperada entre motor e mock, calculada com os valores confirmados;
- se o número de combinações divergentes muda;
- que a divergência continua sendo **caracterizada**, nunca mascarada — é proibido ajustar tolerância de teste para esconder diferença sem causa explicada.

Se você não conseguir estimar o novo comportamento, diga isso explicitamente — mas não omita o item.

---

## 8. CHECKLIST DE AUTO-VERIFICAÇÃO (obrigatório antes de entregar)

**Sobre valores:**
- [ ] Todo valor numérico no entregável tem uma referência `[Fn]` associada.
- [ ] Nenhum valor foi preenchido "para completar a tabela".
- [ ] Células sem fonte estão explicitamente vazias ou marcadas `NÃO LOCALIZADO`, nunca estimadas.
- [ ] Toda derivação está rotulada como DERIVADO e cita fórmula + fonte da fórmula + fonte dos insumos.
- [ ] Nenhuma interpolação, extrapolação ou analogia entre materiais foi usada.

**Sobre fontes:**
- [ ] Toda fonte tem edição/versão declarada.
- [ ] Toda fonte online tem URL e data de acesso.
- [ ] Toda fonte está classificada como PRIMÁRIA ou SECUNDÁRIA.
- [ ] O campo "Acesso obtido" é honesto (texto integral vs. trecho vs. metadados).
- [ ] Nenhum veredito RESOLVIDO se apoia exclusivamente em fonte secundária.

**Sobre qualificação técnica:**
- [ ] Toda resistência declara classe de encordoamento, formação, DC/AC e se é máxima ou nominal.
- [ ] Toda reatância declara arranjo e frequência da fonte.
- [ ] Conversões 50 → 60 Hz estão marcadas e justificadas.

**Sobre o plano de correção:**
- [ ] Nenhuma correção toca o contrato público (R5).
- [ ] Nenhuma remoção de `[VERIFICAR]` sem fonte correspondente (R6).
- [ ] Todo arquivo alvo usa o caminho exato do mapa da §6.6.
- [ ] O impacto sobre CA-QT-19 está tratado (§7.3).
- [ ] Cada correção declara os testes impactados e o critério de aceite afetado.

**Sobre completude:**
- [ ] As oito seções da §6 estão presentes, na ordem.
- [ ] Itens não resolvidos têm rastro de busca completo (§6.4).
- [ ] A declaração de conformidade (§6.8) está preenchida com honestidade.

---

## 9. CRITÉRIOS DE REJEIÇÃO DO SEU ENTREGÁVEL

O trabalho será rejeitado integralmente se ocorrer qualquer um destes:

1. Valor apresentado como CONFIRMADO sem citação localizável;
2. Tabela preenchida por interpolação, analogia ou memória do modelo;
3. Fonte citada que não existe, ou localização (página/tabela) inventada;
4. Proposta de alteração do contrato público;
5. Proposta de remoção de marcação `[VERIFICAR]` sem fonte;
6. Omissão do rastro de busca em itens não resolvidos;
7. Ajuste de tolerância de teste proposto para mascarar divergência não explicada;
8. Declaração de conformidade (§6.8) marcada como cumprida quando não o foi.

**Um entregável honesto que resolve zero pendências e documenta bem por quê vale mais do que um entregável que "resolve" cinco com números não verificáveis.** O sistema calcula projetos elétricos reais; um valor errado de resistência produz um projeto subdimensionado.

---

## 10. O QUE ACONTECE DEPOIS DA SUA ENTREGA

Seu arquivo não é aplicado automaticamente. Ele alimenta um ciclo de desenvolvimento com revisão humana e por agentes:

1. **Analista** valida a qualidade e a rastreabilidade das fontes que você citou;
2. **Product Owner** decide quais pendências resolvidas entram em escopo (`MOD-QT-2-03`, `MOD-QT-2-04`, …);
3. **Scrum Master** transforma cada bloco de correção da sua §6.6 em story rastreável;
4. **Desenvolvedor** aplica as correções, atualiza as tabelas e reexecuta o gate zero;
5. **QA** verifica que nenhuma marcação `[VERIFICAR]` foi removida sem fonte e que o contrato público segue intacto;
6. **DevOps** prepara o fechamento — o push permanece dependente de autorização humana explícita.

Escreva pensando em quem vai executar o passo 4: ele precisa saber **exatamente** qual número entra, em qual arquivo, em qual constante, com qual string de fonte, e o que deve acontecer com os testes.

---

**Fim do prompt. Execute a partir da Fase 0.**
