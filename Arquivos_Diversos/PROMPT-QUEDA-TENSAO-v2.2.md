# PROMPT DE IMPLEMENTAÇÃO — MÓDULO: CÁLCULO DE QUEDA DE TENSÃO

**Identificador:** MOD-QT-v2.2
**Versão anterior:** MOD-QT-v2.1 (2026-07-27)
**Data desta versão:** 2026-07-27
**Dependências upstream:** MOD-DC (dimensionamento de condutores — seção final, material, isolação), Módulo de Circuitos (contrato canônico ou adaptador 1:1), Módulo IB (corrente de projeto)
**Dependência downstream:** Validação de conformidade, Relatório Técnico
**Artefato substituído em produção:** `validarModQTMock` (em `modulos.mod-qt.validar.ts`, linha 102) — mock monofásico/Cu/220V fixo que será substituído pelo motor real, mantendo o mesmo endpoint e contrato público

---

## 1. IDENTIFICAÇÃO DO MÓDULO

| Campo | Valor |
|---|---|
| Nome | Cálculo de Queda de Tensão |
| Código | MOD-QT |
| Épico destino | MOD-QT-2 |
| Story predecessora | MOD-QT-1 (Done — implementou contrato, endpoint e mock) |
| Norma primária | ABNT NBR 5410:2004, seção 6.2.7 |
| Stack | FastAPI + Pydantic v2 + SQLAlchemy 2.x (backend); React + TypeScript + IBM Carbon (frontend) |
| Linguagem de contratos em produção | TypeScript + Zod |
| Linguagem deste pseudocódigo | Python (notação de referência; a implementação real é TypeScript) |

---

## 2. CORREÇÕES SOBRE A v2.0

> As notas abaixo registram alterações rastreáveis da v2.0 para a v2.1. Não apagar — servem de histórico de decisão.

**CORREÇÃO 1 — Contrato de saída renomeado para compatibilidade com `RetornoMODQT` já em produção.**
O v2.0 definia `ResultadoQuedaTensao` com campos `delta_v_circuito_pct`, `conforme_circuito`, `limite_circuito_pct` etc. O contrato real já implementado e consumido pelo MOD-DC (em `contratos.ts`, linhas 50–56) é a interface `RetornoMODQT` com campos `atende`, `queda_percentual`, `limite_aplicado`, `secao_requerida_mm2`, `fonte`. O v2.1 adota esses nomes como contrato público obrigatório do endpoint e mantém nomes descritivos apenas no modelo interno do motor, com mapeamento explícito documentado na §17.

**CORREÇÃO 2 — Estimativa de comprimento via geometria removida do escopo desta versão.**
A seção 5.2 do v2.0 (`estimar_comprimento_circuito`) pressupunha `posicao_quadro: tuple[float, float]` e `posicao_ponto: tuple[float, float]` — coordenadas espaciais de cômodos. Nenhum módulo do SIE hoje armazena ou expõe coordenadas x/y de cômodo ou quadro (confirmado pela análise de `geometria.ts` e `unifilar-graph.ts`). Implementar essa função exigiria um módulo upstream novo, inexistente e fora do escopo de queda de tensão. O comprimento manual informado pelo projetista (`comprimento_m`, já presente no contrato real) é o único caminho suportado nesta versão.

**CORREÇÃO 3 — Citação de fonte de resistência/reatância corrigida.**
O v2.0 citava "NBR 5410 Anexo G" como fonte de valores de resistência e reatância dos condutores. O Anexo G da NBR 5410:2004 trata de **equipotencialização principal**, não de impedância de condutores. A citação estava errada e foi removida. Fontes reais a buscar: catálogos de fabricante (Prysmian/Nexans) ou IEC 60364-5-52 Annex G (não disponíveis localmente no projeto hoje). Os valores permanecem `[VERIFICAR — fonte necessária: catálogo Prysmian/Nexans ou IEC 60364-5-52]`.

**CORREÇÃO 4 — Limites de queda de tensão promovidos de `[VERIFICAR]` para `CONFIRMADO`.**
O v2.0 listava os limites 4%/7% como `[VERIFICAR]`. A seção 6.2.7 da NBR 5410:2004 (texto integral em `NBR-5410.md`, linhas ~10144–10178) confirma: 7% a partir de transformador próprio ou da distribuidora; 5% a partir do ponto de entrega em tensão secundária nos demais casos; circuitos terminais nunca acima de 4%; nota 3 permite +0,005%/m além de 100 m, limitado a +0,5%. Esses valores são idênticos ao que o PRD-MOD-DC §13.6 já utiliza.

**CORREÇÃO 5 (v2.2) — Requisito EDP de 1% no ramal de entrada adicionado.**
O v2.1 não mencionava o limite de 1% de queda de tensão entre ponto de conexão e medição, exigido pela norma EDP-SP (PT.DT.PDN.00068 v09, seção 5.4.6, chunk 22). Como o MOD-QT calcula a queda do alimentador, esse requisito da concessionária precisa ser conhecido e validado pelo motor. Adicionado em §13.8 com status CONFIRMADO.

**CORREÇÃO 6 (v2.2) — Nota 2 do §13.1 marcada com `[VERIFICAR]`.**
O v2.1 atribuía 7% ao contexto EDP-SP sem marcação, mas essa é uma inferência de qual alínea (b ou c) da 6.2.7.1 se aplica — depende de onde fica o "ponto de entrega" em relação ao transformador da distribuidora, o que não foi confirmado explicitamente contra a fonte EDP. Nota 2 agora marcada com `[VERIFICAR]`.

**CORREÇÃO 7 (v2.2) — Seções PREMISSAS, ESTADOS, CHECKLIST DE ENTREGA e INSTRUÇÕES FINAIS adicionadas.**
O v2.1 tinha 31 seções numeradas mas com títulos reorganizados/renomeados em relação ao template `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`. As 4 seções ausentes foram adicionadas para restaurar a auditabilidade seção-a-seção com o template do projeto.

---

## 3. IDENTIDADE DA LLM IMPLEMENTADORA

Você é um engenheiro de software sênior implementando o motor de cálculo de queda de tensão do SIE. Você domina TypeScript/Zod, FastAPI/Pydantic v2, ABNT NBR 5410:2004 e disciplina de rastreabilidade normativa. Você **não inventa** valores normativos — toda lacuna é marcada `[VERIFICAR]`. Você segue rigorosamente o contrato público já em produção (`RetornoMODQT` / `RetornoMODQTSchema`) e não altera sua interface.

---

## 4. MISSÃO

Substituir o mock `validarModQTMock` (monofásico, Cu, 220V fixo, sem reatância) por um motor real que:

1. Calcule queda de tensão para monofásico, bifásico e trifásico
2. Suporte Cu e Al
3. Suporte PVC, EPR e XLPE (temperatura de serviço diferente altera a resistência)
4. Use método simplificado (≤ 25 mm²) e método completo (> 25 mm², com reatância)
5. Valide contra os limites da NBR 5410:2004 seção 6.2.7
6. Retorne `secao_requerida_mm2` quando a seção atual não atende, disparando o laço de revalidação C1/C2/C6 no MOD-DC
7. Mantenha o mesmo endpoint (`/api/v1/modulos/mod-qt/validar`) e contrato público (`RetornoMODQT`)
8. Ofereça interface própria de visualização com simulador de cenários

---

## 5. OBJETIVO

Implementar o módulo de cálculo de queda de tensão como **módulo independente** com **interface própria de visualização** e **simulador de cenários**, permitindo ao projetista:

1. Calcular a queda de tensão (ΔV%) em cada circuito terminal, do quadro de distribuição até o ponto de utilização mais desfavorável
2. Calcular a queda de tensão acumulada (alimentador + circuito terminal) e validar contra os limites da NBR 5410:2004
3. Simular cenários alternativos: comprimentos diferentes, seções superiores, materiais alternativos
4. Visualizar a queda acumulada em diagrama de barras e/ou árvore de circuitos

O módulo usa dois métodos de cálculo:
- **Método simplificado** (seções ≤ 25 mm²): desconsidera reatância, usa apenas resistência
- **Método completo** (seções > 25 mm²): inclui reatância indutiva do condutor

---

## 6. ESCOPO

O MOD-QT nesta versão cobre:

- Cálculo de queda de tensão em circuitos terminais monofásicos e trifásicos
- Cálculo de queda de tensão em circuitos bifásicos — com fórmula `[VERIFICAR — VER-QT-04]`
- Condutores de cobre (Cu) e alumínio (Al)
- Isolação PVC (temperatura de serviço 70°C) e EPR/XLPE (temperatura de serviço 90°C) — **CONFIRMADO** por reaproveitamento do MOD-DC (Tabela 35 da NBR 5410:2004, chunk 117 do `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` §13.3)
- Queda acumulada: alimentador (ponto de entrega → QGBT) + circuito terminal (QGBT → ponto de utilização)
- Comprimento do circuito: **exclusivamente manual**, informado pelo projetista via campo `comprimento_m`
- Simulação de cenários com variação de seção, comprimento e material
- Validação contra limites normativos (4% terminal, 5% ou 7% total — conforme origem da alimentação)
- Retorno de `secao_requerida_mm2` para o laço de revalidação do MOD-DC (critério C5)
- Substituição do mock `validarModQTMock` mantendo endpoint e contrato inalterados

---

## 7. FORA DE ESCOPO (não implementar neste módulo)

### 7.1 Fora de escopo — módulos futuros do SIE

- Cálculo de curto-circuito / integral I²t (módulo MOD-CC futuro)
- Seleção automática de DR (módulo MOD-DR futuro)
- Dimensionamento de eletrodutos (módulo MOD-ELET futuro)
- Diagrama unifilar (módulo MOD-UNIF com PRD próprio)
- Relatório técnico / memorial descritivo
- Planejador de circuitos real (substituição do adaptador 1:1)

### 7.2 Fora de escopo — funcionalidades removidas da v2.0

- **Estimativa automática de comprimento via geometria dos cômodos** (v2.0, seção 5.2): removida por dependência de Motor de Geometria com coordenadas espaciais x/y de cômodo/quadro, inexistente no SIE hoje. Nenhum módulo atual (`geometria.ts`, `unifilar-graph.ts`) armazena ou expõe essas coordenadas. Trabalho futuro, depende de Motor de Geometria com coordenadas espaciais. O comprimento manual (`comprimento_m`) é o único caminho suportado.

### 7.3 Fora de escopo — exclusões técnicas

- Queda de tensão em motores durante partida (norma específica, não NBR 5410:2004 seção 6.2.7)
- Queda de tensão em circuitos de distribuição entre sub-quadros (apenas alimentador principal → QGBT nesta versão)
- Compensação automática de seção por queda de tensão (a decisão de elevar seção é do projetista via simulador; o sistema **sugere** mas **não altera** automaticamente — regra R-07)
- Tolerância adicional de +0,005%/m para circuitos > 100 m (NBR 5410, 6.2.7, nota 3) — registrar como funcionalidade futura, não implementar nesta versão
- Dimensionamento econômico de condutores (IEC 60287-3-2) — fora do escopo, conforme MOD-DC §13.15

---

## 8. FONTES E LIMITES DE CONHECIMENTO

Hierarquia de fontes, da mais para a menos autoritativa:

1. **`NBR-5410.md` / `NBR_5410_chunks.json`** — ABNT NBR 5410:2004 (texto integral local). Fonte primária para limites normativos e fórmulas.
2. **`contratos.ts` / `otimizar-condutor.schema.ts` / `modulos.mod-qt.validar.ts`** — contrato já em produção, tratado como requisito não negociável de compatibilidade (não é fonte normativa, é restrição de engenharia).
3. **`PRD-MOD-DC-modulo-dimensionamento-condutores.md`** — fonte da regra de negócio de integração C5 (seções 1.2, 3.2 FR18, 4, e tabela de critérios).
4. **`06_dimensionamento_markdown_limpo.md`** (Guia EM) — fonte explicativa; **proibido copiar numeração de tabela da edição 1997 sem converter para a edição 2004** (ver §13.7 deste documento, herdado do MOD-DC §13.14).
5. **`PROMPT-QUEDA-TENSAO-v2.md`** (documento-fonte original) — não é fonte normativa; suas fórmulas e valores só valem quando confirmados pelas fontes acima.

---

## 9. ARTIGO IV — NENHUMA INVENÇÃO

É proibido:
- Consultar internet para obter valores normativos
- Inventar valores de resistência ou reatância de condutores
- Assumir fórmula do bifásico sem fonte normativa confirmada
- Inventar coordenadas espaciais de cômodo
- Usar "valor típico" ou "valor razoável" sem marcação `[VERIFICAR]`
- Arredondar para aprovar (R-09)
- Assumir método de instalação silenciosamente (R-08)
- Completar lacuna normativa com valor plausível sem marcação explícita

Toda lacuna normativa vira `[VERIFICAR — fonte necessária: X]`, nunca um valor assumido.

---

## 10. PREMISSAS

- Sistema-alvo típico: trifásico estrela 220/127 V (EDP-SP), mas o motor aceita monofásico, bifásico e trifásico.
- Frequência 60 Hz; regime permanente.
- Condutores de cobre (Cu) ou alumínio (Al), com isolação PVC, EPR ou XLPE, tensão nominal até 0,6/1 kV.
- O comprimento do circuito é informado pelo projetista (campo `comprimento_m`). Não existe estimativa automática nesta versão (ver CORREÇÃO 2, §2).
- Circuitos chegam do MOD-DC com seção já dimensionada e IB calculado (VA usado diretamente — disciplina INC-01; tensão jamais assumida — disciplina INC-04).
- O mock `validarModQTMock` hoje em produção aceita apenas monofásico/Cu/220V fixo com resistividade genérica (`RHO_COBRE = 0.0172`). O motor real é uma evolução estrita — sem conflito de interface.
- Para projetos na área de concessão EDP-SP, além dos limites NBR 5410, aplica-se o limite de 1% no ramal de entrada (§13.8).

---

## 11. GLOSSÁRIO E CONVENÇÕES

| Termo | Definição |
|---|---|
| ΔV | Queda de tensão (absoluta em Volts ou percentual) |
| ΔV% | Queda de tensão percentual: `(ΔV / V_nominal) × 100` |
| R | Resistência do condutor (Ω/km) à temperatura de serviço |
| X | Reatância indutiva do condutor (Ω/km) — relevante apenas para seções > 25 mm² |
| L | Comprimento do circuito em km (campo `comprimento_m` / 1000) |
| IB | Corrente de projeto do circuito (A) — calculada pelo módulo IB upstream |
| cos φ | Fator de potência da carga |
| sin φ | `√(1 - cos²φ)` |
| Método simplificado | Cálculo que desconsidera reatância (apenas R) — para seções ≤ 25 mm² |
| Método completo | Cálculo que inclui reatância (R·cos φ + X·sin φ) — para seções > 25 mm² |
| QGBT | Quadro Geral de Baixa Tensão |
| Mock | `validarModQTMock` — implementação provisória em produção, a ser substituída |
| Contrato público | Interface `RetornoMODQT` + schema `RetornoMODQTSchema` — inalteráveis |
| Modelo interno | Estrutura de dados do motor com campos descritivos — visível apenas dentro do módulo |

**Severidade:** INFO / ATENÇÃO / ERRO — conforme padrão SIE.

---

## 12. POSIÇÃO NA CADEIA DE MÓDULOS

```
Cargas → Demanda → Categoria → Circuitos → IB → Dimensionamento (MOD-DC) → ★ QUEDA DE TENSÃO (MOD-QT) ★ → Proteção
                                                       │                              ▲
                                                       │   secao_requerida_mm2        │
                                                       │   (quando ΔV > limite)       │
                                                       └──────────────────────────────┘
                                                         Laço C5: MOD-DC revalida
                                                         com seção mínima forçada
```

O MOD-QT é invocado pelo MOD-DC como critério C5 (queda de tensão). Quando `atende = false`, o campo `secao_requerida_mm2` indica a seção mínima necessária e dispara o laço de revalidação dos critérios C1/C2/C6 no `servico-dimensionamento-condutores.ts`.

O MOD-QT também é acessível como módulo independente pela interface de visualização do projetista (simulador de cenários), sem estar necessariamente acoplado ao laço do MOD-DC.

---

## 13. FUNDAMENTAÇÃO NORMATIVA

### 13.1 Limites de queda de tensão — CONFIRMADO

Fonte: NBR 5410:2004, seção 6.2.7.1 e 6.2.7.2 (texto integral em `NBR-5410.md`, linhas ~10144–10178).

| Origem da alimentação | Limite total (origem → ponto de utilização) | Limite circuito terminal |
|---|---|---|
| Transformador próprio da edificação | 7% | 4% |
| Transformador da distribuidora (rede pública) | 7% | 4% |
| Ponto de entrega em tensão secundária (demais casos) | 5% | 4% |
| Gerador próprio | 7% | 4% |

**Nota 1:** "queda de tensão" refere-se à diferença entre a tensão no ponto de entrega (ou na origem) e a tensão no ponto de utilização, medida com a carga ligada.
**Nota 2:** Para o contexto EDP-SP, o limite total aplicável depende de qual alínea da 6.2.7.1 se aplica — isto é, de onde se situa o "ponto de entrega" em relação ao transformador da distribuidora. `[VERIFICAR — inferência: se o ponto de entrega coincide com os terminais secundários do transformador da distribuidora, aplica-se alínea b) → 7%; se o ponto de entrega é em tensão secundária de distribuição mas distinto dos terminais do transformador, aplica-se alínea c) → 5%. A fonte EDP (PT.DT.PDN.00068 v09) não especifica explicitamente qual alínea se aplica ao seu modelo de atendimento. O PRD-MOD-DC §13.6 assume 7%, mas essa assunção deve ser confirmada contra a prática da concessionária.]` O circuito terminal nunca excede **4%** (6.2.7.2 — CONFIRMADO).
**Nota 3 (não implementada nesta versão):** Para circuitos com comprimento acima de 100 m, o limite pode ser acrescido de 0,005% por metro adicional, sem ultrapassar um acréscimo de 0,5%. Registrado como funcionalidade futura.

Status: **CONFIRMADO** — idêntico ao PRD-MOD-DC §13.6.

### 13.2 Fórmulas de cálculo

#### 13.2.1 Método simplificado — seções ≤ 25 mm²

Desconsidera reatância indutiva (desprezível para seções ≤ 25 mm²).

**Monofásico (fase-neutro):**
```
ΔV = 2 × IB × R × L
```

**Trifásico (3 fases):**
```
ΔV = √3 × IB × R × L
```

**Bifásico (fase-fase, sem neutro):**
```
ΔV = [VERIFICAR — VER-QT-04] × IB × R × L
```
Nota: O fator para bifásico (2 ou √3) não foi confirmado nas fontes disponíveis. Até resolução, manter `[VERIFICAR]` e não implementar o cálculo bifásico como path automático — exigir confirmação manual ou usar o fator mais conservador (2) com alerta explícito.

Onde:
- R = resistência do condutor (Ω/km) à temperatura de serviço (70°C para PVC, 90°C para EPR/XLPE)
- L = comprimento em km
- IB = corrente de projeto em A

Queda percentual: `ΔV% = (ΔV / V_nominal) × 100`

#### 13.2.2 Método completo — seções > 25 mm²

Inclui reatância indutiva do condutor.

**Monofásico:**
```
ΔV = 2 × IB × (R·cos φ + X·sin φ) × L
```

**Trifásico:**
```
ΔV = √3 × IB × (R·cos φ + X·sin φ) × L
```

**Bifásico:**
```
ΔV = [VERIFICAR — VER-QT-04] × IB × (R·cos φ + X·sin φ) × L
```

Onde X = reatância indutiva do condutor (Ω/km).

#### 13.2.3 Queda acumulada

```
ΔV_total% = ΔV_alimentador% + ΔV_circuito_terminal%
```

O alimentador (ponto de entrega → QGBT) é calculado uma vez por projeto. Cada circuito terminal soma sua queda individual à queda do alimentador. A queda total não pode exceder o limite da §13.1 (5% ou 7% conforme origem), e o circuito terminal individualmente não pode exceder 4%.

### 13.3 Temperatura de serviço dos condutores — CONFIRMADO

Fonte: NBR 5410:2004, Tabela 35 (confirmado em `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` §13.3, chunk 117).

| Isolação | Temperatura de serviço contínuo |
|---|---|
| PVC (seções ≤ 300 mm²) | 70°C |
| EPR / XLPE | 90°C |

A resistência tabelada deve corresponder a essas temperaturas. Valores de R a 70°C para PVC e R a 90°C para EPR/XLPE.

### 13.4 Valores de resistência e reatância dos condutores — [VERIFICAR]

**Status:** `[VERIFICAR — fonte necessária: catálogo Prysmian/Nexans ou IEC 60364-5-52 Annex G]`

**CORREÇÃO sobre a v2.0:** O v2.0 citava "NBR 5410 Anexo G" como fonte desses valores. O Anexo G da NBR 5410:2004 trata de **equipotencialização principal**, não de impedância de condutores. A citação estava errada e foi removida.

Os valores abaixo são de referência provisória e **não podem ser usados em produção** sem confirmação contra fonte autoritativa. Todo cálculo que use esses valores deve retornar `fonte: "[VERIFICAR — valores de resistência provisórios]"` no campo `fonte` do `RetornoMODQT`.

```
Valores de referência provisórios para Cu — [VERIFICAR]

Seção (mm²) │ R(70°C) Ω/km │ R(90°C) Ω/km │ X Ω/km
1.5          │  14.48        │  15.83        │  —
2.5          │   8.87        │   9.69        │  —
4            │   5.52        │   6.04        │  —
6            │   3.66        │   4.00        │  —
10           │   2.19        │   2.39        │  —
16           │   1.38        │   1.51        │  —
25           │   0.870       │   0.951       │  0.080
35           │   0.625       │   0.683       │  0.078
50           │   0.463       │   0.506       │  0.076
70           │   0.321       │   0.351       │  0.074
95           │   0.236       │   0.258       │  0.073
120          │   0.188       │   0.206       │  0.072
150          │   0.153       │   0.168       │  0.071
185          │   0.123       │   0.135       │  0.070
240          │   0.094       │   0.103       │  0.069

Valores de referência provisórios para Al — [VERIFICAR]
(Não tabelados no v2.0 — necessário obter de catálogo)
```

**Nota sobre o mock atual:** O mock em produção usa `RHO_COBRE = 0.0172 Ω·mm²/m` (resistividade a ~20°C), não resistência tabelada por seção. O motor real deve usar resistência por seção (Ω/km) à temperatura de serviço, que é um valor mais preciso e específico. A transição do mock (resistividade genérica) para o motor (resistência tabelada por seção) é uma melhoria esperada e documentada.

### 13.5 Seção mínima por queda de tensão (cálculo inverso)

Quando ΔV% excede o limite, o motor deve calcular a seção mínima necessária para atender. Para o método simplificado:

**Monofásico:**
```
S_min = (2 × ρ × IB × L_m) / (ΔV_max × 10⁻²)
```
onde `ΔV_max = V_nominal × (limite% / 100)` e `ρ` é resistividade (Ω·mm²/m).

O resultado deve ser arredondado **para cima** para a próxima seção da série IEC 60228 e retornado no campo `secao_requerida_mm2` do `RetornoMODQT`.

### 13.6 Resistividade dos materiais — [VERIFICAR parcial]

| Material | Resistividade a 20°C (Ω·mm²/m) | Fonte |
|---|---|---|
| Cu | 0.01724 | `[VERIFICAR — fonte necessária: IEC 60228 ou catálogo]` |
| Al | 0.02826 | `[VERIFICAR — fonte necessária: IEC 60228 ou catálogo]` |

**Nota:** O mock atual usa `RHO_COBRE = 0.0172`, que é compatível com 0.01724 (arredondamento). A transição para resistência tabelada por seção (§13.4) torna a resistividade direta menos central, mas ela permanece necessária para o cálculo inverso de `secao_requerida_mm2` (§13.5).

### 13.7 Mapeamento de tabelas 1997 × 2004 — HERDADO DO MOD-DC

Conforme `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` §13.14. Qualquer citação no código, nos testes ou na UI deve usar exclusivamente a numeração da edição 2004 da NBR 5410. Se um valor for transcrito de material didático (Guia EM) que use numeração 1997, converter antes de registrar.

Mapeamento relevante para o MOD-QT:
- Tabela 46 (ed. 1997) → seção 6.2.7 (ed. 2004): limites de queda de tensão
- Tabelas 31–34 (ed. 1997) → Tabelas 36–39 (ed. 2004): capacidade de condução (referência cruzada)

### 13.8 Requisito EDP-SP: queda máxima de 1% no ramal de entrada — CONFIRMADO

Fonte: PT.DT.PDN.00068 v09, seção 5.4.6 "Condutores do ramal de entrada" (chunk 22, p. 18).

Transcrição do trecho normativo:
> "O limite máximo de queda de tensão, entre o ponto de conexão e a medição, deve ser de 1%"

Este limite de **1%** é específico do **ramal de entrada** (trecho entre o ponto de conexão da concessionária e o medidor/caixa de medição) e é **separado e adicional** aos limites gerais da NBR 5410:2004 seção 6.2.7 (4%/5%/7%).

**Implicação para o MOD-QT:** O motor deve validar, para projetos na área de concessão EDP-SP, que a queda de tensão no trecho ramal de entrada (ponto de conexão → medição) não exceda 1%. Este trecho é anterior ao alimentador interno (medição → QGBT). A queda total do projeto passa a ter três componentes:

```
ΔV_total = ΔV_ramal_entrada (≤ 1%, EDP) + ΔV_alimentador_interno (medição → QGBT) + ΔV_circuito_terminal (≤ 4%, NBR)
```

E a soma `ΔV_ramal_entrada + ΔV_alimentador_interno + ΔV_circuito_terminal` não deve exceder o limite total de 5% ou 7% (conforme §13.1, Nota 2 `[VERIFICAR]`).

**Dados de entrada necessários:**
- `comprimento_ramal_entrada_m`: comprimento do ramal de entrada (ponto de conexão → medição)
- `secao_ramal_entrada_mm2`: seção do condutor do ramal (definida pela categoria de atendimento, conforme tabela EDP)
- `material_ramal_entrada`: Cu (padrão EDP para ramal de entrada)

**Nota:** O ramal de entrada é dimensionado conforme a categoria de atendimento e instalado pelo cliente (exceto categorias U, D2 e T2 onde a concessionária fornece). Os condutores devem ser de cobre com isolação PVC 450/750V, XLPE ou EPR 0,6/1,0 kV (PT.DT.PDN.00068 v09, 5.4.6).

**Nota sobre o contrato público `RetornoMODQT`:** O contrato atual não prevê distinção entre ramal de entrada e alimentador interno. A validação do limite de 1% pode ser implementada como uma chamada separada ao endpoint (com `limite_percentual = 1.0` e `origem = "RAMAL-ENTRADA-EDP"`) ou como lógica interna do motor que verifica automaticamente quando o perfil de concessionária é EDP-SP. A decisão de implementação não altera o contrato público.

Status: **CONFIRMADO** — fonte: PT.DT.PDN.00068 v09, 5.4.6, chunk 22. Idêntico ao registrado no PRD-MOD-DC §13.6 e PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md §13.6.

---

## 14. REGRAS GERAIS SIE (obrigatórias, herdadas e revisadas)

- **R-01 Rastreabilidade normativa:** todo valor calculado armazena `fonte` exata (documento, edição, item, tabela, linha, coluna, nota, página, `chunk_id`) e `status_verificacao` (`CONFIRMADO` | `PENDENTE` | `[VERIFICAR]`). Referência genérica ("conforme norma") é proibida.
- **R-02 Série normalizada:** seções na série IEC 60228; erro `INC-07` para seção fora da série.
- **R-03 Tensão sem fallback:** `tensao_v is None` → `ERRO-TENSAO-AUSENTE`, nenhum cálculo (disciplina INC-04).
- **R-04 VA direto:** nunca dividir VA por fator de potência (disciplina INC-01).
- **R-05 Design System:** IBM Carbon; proibido texto branco sobre `#fa4d56` (contraste 3,35:1 < WCAG AA 4,5:1) — teste automatizado obrigatório (padrão `test_ds04`).
- **R-06 Isolação explícita:** PVC ou EPR/XLPE sempre escolhidos pelo projetista (padrão de projeto com override por circuito); ausência → `ERRO-ISOLACAO-AUSENTE` (resolução INC-12).
- **R-07 Queda de tensão nunca retroalimenta automaticamente:** se ΔV excede o limite, o sistema sinaliza e sugere seções superiores no simulador, mas **não altera** automaticamente a seção definida pelo MOD-DC. A decisão de elevar seção é do projetista. Na integração como critério C5, o campo `secao_requerida_mm2` **informa** o MOD-DC, que reexecuta seus critérios C1/C2/C6 com essa seção como piso; mas a decisão final permanece sujeita a verificação de coordenação (In ≤ Iz).
- **R-08 Comprimento é dado de entrada:** o comprimento do circuito é fornecido exclusivamente pelo projetista (campo `comprimento_m`). Ausência de comprimento → `atende = false` com `fonte` indicando o motivo.
- **R-09 Nada aprovado por arredondamento:** comparações ΔV% ≤ limite% usam precisão adequada; valor original e arredondado são ambos registrados.
- **R-10 Pendência bloqueia completude:** circuito sem comprimento ou com valores de impedância `[VERIFICAR]` não pode ter status `CONFIRMADO`.
- **R-11 Override auditado:** se o projetista aplica uma seção sugerida pelo simulador, a justificativa é registrada com valores antes/depois.

---

## 15. MODELO DE DADOS E CONTRATOS

### 15.1 Contrato público do endpoint — INALTERÁVEL

Estes são os contratos já em produção, consumidos pelo MOD-DC. **Não podem ser alterados, renomeados ou estendidos** sem story de migração separada.

#### 15.1.1 Request — `ValidarMODQTSchema`

Fonte: `otimizar-condutor.schema.ts`, linhas 74–93.

```typescript
// Schema Zod — exatamente como está em produção
const ValidarMODQTSchema = z.object({
  dependencia_id: z.string().uuid(),
  corrente_a: z.number().positive(),
  comprimento_m: z.number().positive(),
  secao_mm2: z.number().positive(),
  limite_percentual: z.number().positive(),
  origem: z.string(),
});
```

| Campo | Tipo | Descrição |
|---|---|---|
| `dependencia_id` | `string (uuid)` | ID da dependência/circuito |
| `corrente_a` | `number > 0` | Corrente de projeto IB (A) |
| `comprimento_m` | `number > 0` | Comprimento do circuito (m) — informado pelo projetista |
| `secao_mm2` | `number > 0` | Seção do condutor (mm²) — vinda do MOD-DC |
| `limite_percentual` | `number > 0` | Limite de queda aplicável (%) — determinado pela origem da alimentação |
| `origem` | `string` | Identificação da origem da chamada (ex.: `"MOD-DC-C5"`, `"SIMULADOR"`) |

#### 15.1.2 Response — `RetornoMODQT`

Fonte: `contratos.ts`, linhas 50–56.

```typescript
interface RetornoMODQT {
  readonly atende: boolean;
  readonly queda_percentual: number;
  readonly limite_aplicado: number;
  readonly secao_requerida_mm2?: number | null;
  readonly fonte: string;
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `atende` | `boolean` | `true` se ΔV% ≤ limite aplicado |
| `queda_percentual` | `number` | ΔV% calculado |
| `limite_aplicado` | `number` | Limite % usado na verificação (eco do request ou corrigido por §13.1) |
| `secao_requerida_mm2` | `number \| null` | Seção mínima da série IEC 60228 que atenderia o limite — `null` quando `atende = true`. **Este campo dispara o laço de revalidação C1/C2/C6 no MOD-DC.** |
| `fonte` | `string` | Rastreabilidade: fórmula, tabela, versão. Ex.: `"MOD-QT-v2.2; simplificado; R=8.87Ω/km [VERIFICAR]; NBR5410:2004 §6.2.7"` |

#### 15.1.3 Endpoint

Fonte: `modulos.mod-qt.validar.ts`.

```
POST /api/v1/modulos/mod-qt/validar
```

Request body: `ValidarMODQTSchema`
Response body: `RetornoMODQT`

O handler atual (`validarModQTMock`, linha 102) será substituído pelo motor real. O endpoint, a rota, e os schemas de validação Zod permanecem inalterados.

### 15.2 Modelo interno do motor (não exposto pela API pública)

O motor internamente pode usar um modelo mais rico para cálculos, simulações e visualização. Este modelo é visível apenas dentro do módulo MOD-QT e na interface de visualização do projetista.

```python
class ResultadoInternoQuedaTensao(BaseModel):
    """Modelo interno — NÃO é o contrato público. Mapeado para RetornoMODQT na camada de API."""
    
    circuito_id: str
    
    # Queda no circuito terminal
    delta_v_absoluto_v: float              # queda absoluta em Volts
    delta_v_percentual: float              # queda percentual (= queda_percentual no contrato público)
    metodo_calculo: Literal["SIMPLIFICADO", "COMPLETO"]
    
    # Queda no alimentador (se informado)
    delta_v_alimentador_pct: Optional[float]
    
    # Queda acumulada
    delta_v_total_pct: float               # alimentador + circuito
    
    # Limites NBR 5410 (CONFIRMADO — §13.1)
    limite_circuito_pct: float             # 4.0% (terminal)
    limite_total_pct: float                # 5.0% ou 7.0% (conforme origem)
    
    # Conformidade
    atende_circuito: bool                  # delta_v_percentual ≤ limite_circuito_pct
    atende_total: bool                     # delta_v_total_pct ≤ limite_total_pct
    
    # Seção mínima necessária (se não atende)
    secao_requerida_mm2: Optional[float]   # na série IEC 60228; None se atende
    
    # Rastreabilidade detalhada
    rastreio: dict                         # fórmula, variáveis, valores, fonte
    sugestoes: list[str]                   # para o simulador
```

---

## 16. MAPEAMENTO CONTRATO INTERNO ↔ CONTRATO PÚBLICO

Este é o mapeamento obrigatório entre o modelo interno (§15.2) e o contrato público (§15.1.2). A camada de API executa esta conversão no handler do endpoint.

```python
def mapear_para_retorno_publico(interno: ResultadoInternoQuedaTensao) -> RetornoMODQT:
    return RetornoMODQT(
        atende=interno.atende_circuito and interno.atende_total,
        queda_percentual=round(interno.delta_v_percentual, 4),
        limite_aplicado=interno.limite_circuito_pct,
        secao_requerida_mm2=interno.secao_requerida_mm2 if not (interno.atende_circuito and interno.atende_total) else None,
        fonte=construir_fonte(interno),  # ver §16.1
    )
```

### 16.1 Formato do campo `fonte`

O campo `fonte` do `RetornoMODQT` deve ser uma string legível e auditável contendo:

```
"MOD-QT-v2.2; {metodo}; R={R}Ω/km {status_R}; L={L}m; IB={IB}A; V={V}V; NBR5410:2004 §6.2.7"
```

Exemplo:
```
"MOD-QT-v2.2; simplificado; R=8.87Ω/km [VERIFICAR]; L=22.0m; IB=18.2A; V=220V; NBR5410:2004 §6.2.7"
```

Se os valores de resistência não foram confirmados, incluir `[VERIFICAR]` na string de fonte.

| Campo interno | → | Campo público |
|---|---|---|
| `delta_v_percentual` | → | `queda_percentual` |
| `atende_circuito AND atende_total` | → | `atende` |
| `limite_circuito_pct` | → | `limite_aplicado` |
| `secao_requerida_mm2` (se não atende) | → | `secao_requerida_mm2` |
| construído via `construir_fonte()` | → | `fonte` |

---

## 17. MODELO DE DADOS (persistência)

### 17.1 Tabela de impedância por condutor

```sql
CREATE TABLE impedancia_condutor (
    id SERIAL PRIMARY KEY,
    material VARCHAR(2) NOT NULL CHECK (material IN ('Cu', 'Al')),
    secao_mm2 DECIMAL(6,2) NOT NULL,
    
    -- Resistência (Ω/km) à temperatura de serviço
    resistencia_70c_ohm_km DECIMAL(8,4),       -- para PVC (70°C)
    resistencia_90c_ohm_km DECIMAL(8,4),       -- para EPR/XLPE (90°C)
    
    -- Reatância indutiva (Ω/km) — relevante para seções > 25 mm²
    reatancia_ohm_km DECIMAL(8,4),
    
    fonte VARCHAR(200) NOT NULL,
    status_verificacao VARCHAR(20) NOT NULL DEFAULT '[VERIFICAR]',
    
    UNIQUE (material, secao_mm2)
);
```

**Nota:** Todos os valores iniciais devem ter `status_verificacao = '[VERIFICAR]'` até serem confirmados contra catálogo de fabricante ou IEC 60364-5-52. O motor deve incluir `[VERIFICAR]` no campo `fonte` do `RetornoMODQT` quando usar valores não confirmados.

### 17.2 Comprimento por circuito

```sql
ALTER TABLE circuito ADD COLUMN IF NOT EXISTS (
    comprimento_m DECIMAL(6,2)                 -- informado pelo projetista (único caminho nesta versão)
);
```

**Nota sobre a v2.0:** O v2.0 previa `comprimento_estimado_m` e `fonte_comprimento`. Esses campos foram removidos nesta versão por dependência de Motor de Geometria inexistente (CORREÇÃO 2, §2). Quando o Motor de Geometria for implementado no futuro, o campo `comprimento_estimado_m` pode ser adicionado com story própria.

### 17.3 Configuração do alimentador (nível de projeto)

```sql
ALTER TABLE projeto ADD COLUMN IF NOT EXISTS (
    comprimento_alimentador_m DECIMAL(6,2),    -- do ponto de entrega ao QGBT
    secao_alimentador_mm2 DECIMAL(6,2),        -- já definido pela categoria de entrada
    material_alimentador VARCHAR(2) DEFAULT 'Cu',
    queda_tensao_alimentador_pct DECIMAL(5,2)  -- calculada uma vez, usada em todos os circuitos
);
```

### 17.4 Resultado da queda de tensão por circuito

```sql
ALTER TABLE circuito ADD COLUMN IF NOT EXISTS (
    queda_tensao_pct DECIMAL(5,2),
    queda_tensao_total_pct DECIMAL(5,2),
    queda_tensao_atende BOOLEAN,
    rastreio_queda_tensao JSONB
);
```

---

## 18. ALGORITMO — MÉTODO SIMPLIFICADO (seções ≤ 25 mm²)

```python
def calcular_queda_simplificado(IB: float, R_ohm_km: float, L_km: float,
                                 V_nominal: float, num_fases: int) -> tuple[float, float]:
    """
    Retorna (delta_v_absoluto, delta_v_percentual).
    """
    if num_fases == 3:
        delta_v = (3 ** 0.5) * IB * R_ohm_km * L_km
    elif num_fases == 1:
        delta_v = 2 * IB * R_ohm_km * L_km
    elif num_fases == 2:
        # [VERIFICAR — VER-QT-04: fator 2 ou √3 para bifásico]
        # Usar fator 2 (mais conservador) com alerta explícito até resolução
        delta_v = 2 * IB * R_ohm_km * L_km
    else:
        raise ValueError(f"num_fases inválido: {num_fases}")
    
    delta_v_pct = (delta_v / V_nominal) * 100
    return (delta_v, delta_v_pct)
```

---

## 19. ALGORITMO — MÉTODO COMPLETO (seções > 25 mm²)

```python
def calcular_queda_completo(IB: float, R_ohm_km: float, X_ohm_km: float,
                             cos_phi: float, L_km: float,
                             V_nominal: float, num_fases: int) -> tuple[float, float]:
    """
    Inclui reatância indutiva. Retorna (delta_v_absoluto, delta_v_percentual).
    """
    sin_phi = (1 - cos_phi ** 2) ** 0.5
    impedancia_efetiva = R_ohm_km * cos_phi + X_ohm_km * sin_phi
    
    if num_fases == 3:
        delta_v = (3 ** 0.5) * IB * impedancia_efetiva * L_km
    elif num_fases == 1:
        delta_v = 2 * IB * impedancia_efetiva * L_km
    elif num_fases == 2:
        # [VERIFICAR — VER-QT-04]
        delta_v = 2 * IB * impedancia_efetiva * L_km
    else:
        raise ValueError(f"num_fases inválido: {num_fases}")
    
    delta_v_pct = (delta_v / V_nominal) * 100
    return (delta_v, delta_v_pct)
```

---

## 20. ALGORITMO — MOTOR PRINCIPAL

```python
SERIE_IEC_60228 = [0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500]

def calcular_queda_tensao(request: ValidarMODQTRequest,
                           material: str = "Cu",
                           isolacao: str = "PVC",
                           num_fases: int = 1,
                           fp_carga: float = 1.0,
                           tensao_v: float = 220.0,
                           comprimento_alimentador_m: Optional[float] = None,
                           secao_alimentador_mm2: Optional[float] = None,
                           material_alimentador: str = "Cu"
                           ) -> ResultadoInternoQuedaTensao:
    """
    Motor principal de cálculo de queda de tensão.
    
    O request contém os campos do contrato público (corrente_a, comprimento_m, secao_mm2,
    limite_percentual). Os demais parâmetros vêm do contexto do circuito/projeto.
    """
    
    # ──────────────────────────────────────────
    # GUARDA: comprimento
    # ──────────────────────────────────────────
    if request.comprimento_m is None or request.comprimento_m <= 0:
        return ResultadoInternoQuedaTensao(
            atende_circuito=False, atende_total=False,
            delta_v_percentual=0, secao_requerida_mm2=None,
            rastreio={"erro": "comprimento ausente ou inválido"}
        )
    
    IB = request.corrente_a
    L_km = request.comprimento_m / 1000
    secao = request.secao_mm2
    V = tensao_v
    
    # ──────────────────────────────────────────
    # SELECIONAR MÉTODO
    # ──────────────────────────────────────────
    if secao <= 25:
        metodo = "SIMPLIFICADO"
    else:
        metodo = "COMPLETO"
    
    # ──────────────────────────────────────────
    # BUSCAR IMPEDÂNCIA
    # ──────────────────────────────────────────
    imp = buscar_impedancia(material, secao)  # consulta tabela impedancia_condutor
    
    if isolacao in ("EPR", "XLPE"):
        R = imp.resistencia_90c_ohm_km
    else:  # PVC
        R = imp.resistencia_70c_ohm_km
    
    if R is None:
        return ResultadoInternoQuedaTensao(
            atende_circuito=False, atende_total=False,
            delta_v_percentual=0, secao_requerida_mm2=None,
            rastreio={"erro": f"resistência não encontrada para {material} {secao}mm²"}
        )
    
    status_r = imp.status_verificacao  # "[VERIFICAR]" ou "CONFIRMADO"
    
    # ──────────────────────────────────────────
    # CALCULAR QUEDA NO CIRCUITO TERMINAL
    # ──────────────────────────────────────────
    if metodo == "SIMPLIFICADO":
        delta_v, delta_v_pct = calcular_queda_simplificado(IB, R, L_km, V, num_fases)
        X = None
    else:
        X = imp.reatancia_ohm_km or 0.0
        cos_phi = fp_carga if fp_carga else 1.0
        delta_v, delta_v_pct = calcular_queda_completo(IB, R, X, cos_phi, L_km, V, num_fases)
    
    # ──────────────────────────────────────────
    # CALCULAR QUEDA NO ALIMENTADOR (se informado)
    # ──────────────────────────────────────────
    delta_v_alim_pct = 0.0
    if comprimento_alimentador_m and secao_alimentador_mm2:
        imp_alim = buscar_impedancia(material_alimentador, secao_alimentador_mm2)
        R_alim = imp_alim.resistencia_70c_ohm_km  # alimentador tipicamente PVC
        if R_alim:
            # Para o alimentador, usar corrente de demanda do projeto (não IB do circuito)
            # Esta corrente deve vir do contexto do projeto
            # Por ora, calcular com IB como aproximação conservadora
            _, delta_v_alim_pct = calcular_queda_simplificado(
                IB, R_alim, comprimento_alimentador_m / 1000, V, num_fases
            )
    
    delta_v_total_pct = delta_v_alim_pct + delta_v_pct
    
    # ──────────────────────────────────────────
    # VERIFICAR CONTRA LIMITES (CONFIRMADO — §13.1)
    # ──────────────────────────────────────────
    LIMITE_CIRCUITO_PCT = 4.0  # CONFIRMADO: NBR 5410:2004 §6.2.7
    limite_total = request.limite_percentual  # 5.0 ou 7.0, passado pelo chamador
    
    atende_circuito = delta_v_pct <= LIMITE_CIRCUITO_PCT
    atende_total = delta_v_total_pct <= limite_total
    
    # ──────────────────────────────────────────
    # CALCULAR SEÇÃO REQUERIDA (se não atende)
    # ──────────────────────────────────────────
    secao_requerida = None
    if not atende_circuito:
        secao_requerida = calcular_secao_minima_queda(
            IB=IB, L_m=request.comprimento_m, V=V,
            limite_pct=LIMITE_CIRCUITO_PCT, material=material,
            isolacao=isolacao, num_fases=num_fases
        )
    
    # ──────────────────────────────────────────
    # SUGESTÕES PARA SIMULADOR
    # ──────────────────────────────────────────
    sugestoes = []
    if not atende_circuito:
        for s_alt in SERIE_IEC_60228:
            if s_alt > secao:
                imp_alt = buscar_impedancia(material, s_alt)
                R_alt = imp_alt.resistencia_70c_ohm_km if isolacao == "PVC" else imp_alt.resistencia_90c_ohm_km
                if R_alt:
                    _, dv_alt = calcular_queda_simplificado(IB, R_alt, L_km, V, num_fases)
                    if dv_alt <= LIMITE_CIRCUITO_PCT:
                        sugestoes.append(
                            f"Seção {secao}→{s_alt} mm² reduz queda de {delta_v_pct:.1f}% para {dv_alt:.1f}%"
                        )
                        break
    
    # ──────────────────────────────────────────
    # CONSTRUIR RESULTADO
    # ──────────────────────────────────────────
    return ResultadoInternoQuedaTensao(
        circuito_id=request.dependencia_id,
        delta_v_absoluto_v=round(delta_v, 4),
        delta_v_percentual=round(delta_v_pct, 4),
        metodo_calculo=metodo,
        delta_v_alimentador_pct=round(delta_v_alim_pct, 4) if delta_v_alim_pct > 0 else None,
        delta_v_total_pct=round(delta_v_total_pct, 4),
        limite_circuito_pct=LIMITE_CIRCUITO_PCT,
        limite_total_pct=limite_total,
        atende_circuito=atende_circuito,
        atende_total=atende_total,
        secao_requerida_mm2=secao_requerida,
        rastreio={
            "formula": _formula_texto(metodo, num_fases),
            "IB_a": IB, "R_ohm_km": R, "L_km": L_km, "L_m": request.comprimento_m,
            "V_nominal": V, "secao_mm2": secao,
            "X_ohm_km": X if metodo == "COMPLETO" else None,
            "cos_phi": fp_carga if metodo == "COMPLETO" else None,
            "material": material, "isolacao": isolacao,
            "num_fases": num_fases,
            "status_resistencia": status_r,
            "fonte_resistencia": imp.fonte,
            "versao_modulo": "MOD-QT-v2.2"
        },
        sugestoes=sugestoes
    )


def calcular_secao_minima_queda(IB: float, L_m: float, V: float,
                                 limite_pct: float, material: str,
                                 isolacao: str, num_fases: int) -> Optional[float]:
    """
    Calcula a menor seção da série IEC 60228 que atende o limite de queda.
    Percorre a série em ordem crescente e retorna a primeira que atende.
    """
    for secao_candidata in SERIE_IEC_60228:
        imp = buscar_impedancia(material, secao_candidata)
        R = imp.resistencia_70c_ohm_km if isolacao == "PVC" else imp.resistencia_90c_ohm_km
        if R is None:
            continue
        _, dv_pct = calcular_queda_simplificado(IB, R, L_m / 1000, V, num_fases)
        if dv_pct <= limite_pct:
            return secao_candidata
    return None  # nenhuma seção da série atende


def _formula_texto(metodo: str, num_fases: int) -> str:
    if metodo == "SIMPLIFICADO":
        if num_fases == 3:
            return "ΔV = √3 × IB × R × L"
        else:
            return "ΔV = 2 × IB × R × L"
    else:
        if num_fases == 3:
            return "ΔV = √3 × IB × (R·cosφ + X·sinφ) × L"
        else:
            return "ΔV = 2 × IB × (R·cosφ + X·sinφ) × L"
```

---

## 21. SIMULADOR DE CENÁRIOS

```python
class CenarioSimulacao(BaseModel):
    id: str                                # "CEN-01"
    descricao: str                         # "Subir seção para 10 mm²"
    secao_mm2: Optional[float] = None      # None = manter original
    comprimento_m: Optional[float] = None
    material: Optional[Literal["Cu", "Al"]] = None

class ResultadoSimulacao(BaseModel):
    cenario_id: str
    descricao: str
    resultado: ResultadoInternoQuedaTensao
    delta_vs_original: dict                # campo a campo: valor original → valor do cenário

def simular_cenarios(request_base: ValidarMODQTRequest,
                      contexto: dict,
                      cenarios: list[CenarioSimulacao]) -> list[ResultadoSimulacao]:
    """
    Recebe o request base e uma lista de cenários alternativos.
    Retorna resultado de queda para cada cenário.
    O request_base e contexto são copiados e os campos do cenário aplicados como override.
    """
    resultados = []
    for cenario in cenarios:
        request_mod = request_base.model_copy(update={
            k: v for k, v in {
                "secao_mm2": cenario.secao_mm2,
                "comprimento_m": cenario.comprimento_m,
            }.items() if v is not None
        })
        contexto_mod = {**contexto}
        if cenario.material:
            contexto_mod["material"] = cenario.material
        
        resultado = calcular_queda_tensao(request_mod, **contexto_mod)
        resultados.append(ResultadoSimulacao(
            cenario_id=cenario.id,
            descricao=cenario.descricao,
            resultado=resultado,
            delta_vs_original={
                "secao_mm2": f"{request_base.secao_mm2} → {request_mod.secao_mm2}",
                "comprimento_m": f"{request_base.comprimento_m} → {request_mod.comprimento_m}",
                "material": f"{contexto.get('material','Cu')} → {contexto_mod.get('material','Cu')}",
            }
        ))
    return resultados
```

O simulador é acessível via interface de visualização do projetista (§23) e não é invocado pelo laço C5 do MOD-DC. Ele é um recurso de exploração de projeto.

---

## 22. INTERAÇÃO MOD-DC ↔ MOD-QT

### 22.1 Fluxo como critério C5

```
MOD-DC (servico-dimensionamento-condutores.ts)
│
├── C1: Capacidade de condução → secao_c1
├── C2: Seção mínima por aplicação → secao_c2
├── C5: Queda de tensão → chama POST /api/v1/modulos/mod-qt/validar
│       │
│       ├── RetornoMODQT.atende = true → nada a fazer
│       └── RetornoMODQT.atende = false
│           └── secao_requerida_mm2 = X → secao_c5 = X
│               → MOD-DC revalida C1/C2/C6 com max(secao_c1, secao_c2, secao_c5, secao_c6)
│
├── C6: Coordenação IB ≤ In ≤ Iz → secao_c6
└── secao_final = max(todos os critérios)
```

### 22.2 Regra crítica de acoplamento

O campo `secao_requerida_mm2` do `RetornoMODQT` é o **único ponto de acoplamento** entre MOD-QT e MOD-DC. Quando não-nulo:

1. O MOD-DC usa esse valor como piso (`secao_c5`)
2. O MOD-DC recalcula `secao_final = max(secao_c1, secao_c2, secao_c5, secao_c6)`
3. O MOD-DC recalcula Iz real para a nova seção
4. O MOD-DC reavalia coordenação In ≤ Iz
5. A justificativa é registrada: `"Seção elevada para X mm² por queda de tensão (ΔV reduziu de A% para B%)"`

**Este mecanismo já existe em produção** (no `servico-dimensionamento-condutores.ts`). O motor MOD-QT real apenas precisa retornar o campo corretamente — não precisa implementar o laço, que é responsabilidade do MOD-DC.

### 22.3 Fluxo como simulador independente

Quando acessado pela interface de visualização (não pelo laço C5):

1. O projetista seleciona um circuito
2. O sistema exibe a queda atual e sugere cenários
3. O projetista pode criar cenários custom
4. Se o projetista clica "Aplicar Opção X":
   - O sistema grava `comprimento_m` e a seção escolhida
   - Dispara recálculo do MOD-DC com a seção como piso forçado
   - A justificativa é registrada com override auditado (R-11)

---

## 23. API — ENDPOINTS

### 23.1 Endpoint público (substitui mock) — INALTERÁVEL

```
POST /api/v1/modulos/mod-qt/validar
```

Request: `ValidarMODQTSchema` (§15.1.1)
Response: `RetornoMODQT` (§15.1.2)

### 23.2 Endpoints adicionais (novos, para interface de visualização)

```python
@router.post("/api/v1/projetos/{projeto_id}/queda-tensao-lote")
async def calcular_queda_lote(projeto_id: str):
    """Calcula queda de tensão para todos os circuitos do projeto.
    Retorna lista de ResultadoInternoQuedaTensao (modelo interno)."""

@router.post("/api/v1/projetos/{projeto_id}/circuitos/{circuito_id}/simular-queda")
async def simular_cenarios_queda(projeto_id: str, circuito_id: str, entrada: EntradaSimulacao):
    """Simula cenários alternativos de queda de tensão."""

@router.put("/api/v1/projetos/{projeto_id}/alimentador")
async def configurar_alimentador(projeto_id: str, config: ConfiguracaoAlimentador):
    """Define parâmetros do alimentador para cálculo acumulado."""

@router.get("/api/v1/projetos/{projeto_id}/queda-tensao/resumo")
async def resumo_queda_tensao(projeto_id: str):
    """Retorna resumo: piores circuitos, conformidade geral, estatísticas."""

@router.get("/api/v1/tabelas/impedancia")
async def listar_impedancias(material: Optional[str] = None, secao: Optional[float] = None):
    """Consulta tabela de impedâncias dos condutores com status_verificacao."""
```

---

## 24. UI — TELA PRINCIPAL (IBM Carbon Design System)

### 24.1 Configuração do alimentador (painel superior)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Queda de Tensão — Projeto: proj-1                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Alimentador: [___] m  │  Seção: [25 mm² ▾]  │  Material: [Cu ▾]          │
│  ΔV alimentador: 1.2%  │  Limite total: [7.0% ▾]   ← 5% ou 7% (§13.1)   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─ Conformidade Geral ──────────────────────────────────────────────────┐ │
│  │  44 circuitos  │  Conformes: 38 ✓  │  Acima do limite: 4 ✗          │ │
│  │  Sem comprimento: 2 ⚠                                                │ │
│  │                                                                       │ │
│  │  Pior circuito: TUE-Ar-Cond-Suite (ΔV = 5.8%, limite 4.0%)          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

O dropdown de limite total (5% ou 7%) deve refletir a origem da alimentação conforme §13.1. Para projetos EDP-SP (transformador da distribuidora), o padrão é 7%.

---

## 25. UI — TABELA DE RESULTADOS POR CIRCUITO

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Circuito              │ IB(A) │ S(mm²) │ L(m) │ ΔV circ(%) │ ΔV total(%) │ Lim. │ Status │
├───┼───────────────────────┼───────┼────────┼──────┼────────────┼─────────────┼──────┼────────┤
│ 1 │ ILUM-Dormitorio-1     │  2.36 │  1.5   │ 12.0 │    0.8     │     2.0     │ 4.0% │ ✓ OK   │
│ 2 │ TUG-Cozinha-1         │ 12.60 │  2.5   │  8.5 │    1.9     │     3.1     │ 4.0% │ ✓ OK   │
│ 3 │ TUE-Ar-Cond-Suite     │ 18.20 │  2.5   │ 22.0 │    5.8     │     7.0     │ 4.0% │ ✗ ACIMA│
│ 4 │ ADD-Banh-Chuveiro     │ 34.65 │ 10.0   │  6.0 │    0.5     │     1.7     │ 4.0% │ ✓ OK   │
│ 5 │ TUE-Forno-1           │  —    │  —     │  —   │     —      │      —      │  —   │ ⚠ PEND │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- Linhas com `✗ ACIMA`: fundo Carbon `$danger-01` com texto escuro (nunca branco — R-05 / test_ds04)
- Linhas sem comprimento: fundo Carbon `$warning-01`
- Clicar na linha abre o painel de simulação (§21 — Simulador de Cenários)
- Coluna `L(m)` editável inline pelo projetista

---

## 26. CRITÉRIOS DE ACEITE

Todos os nomes de campo testados correspondem ao contrato público (`atende`, `queda_percentual`, `limite_aplicado`, `secao_requerida_mm2`, `fonte`) ou ao modelo interno quando especificado.

| ID | Critério | Verificação |
|----|----------|-------------|
| **CA-QT-01** | Circuito monofásico Cu PVC 2.5mm² 10m IB=10A V=127V → `queda_percentual` calculado pelo método simplificado, valor coerente com `ΔV = 2×10×R×0.01/127×100` usando R da tabela de impedância `[VERIFICAR]` | Teste automatizado com tolerância ±0.05% |
| **CA-QT-02** | Circuito trifásico Cu PVC 4mm² 15m IB=20A V=220V → `queda_percentual` calculado com fator √3, método simplificado | Teste automatizado |
| **CA-QT-03** | Seção > 25mm² (ex: 35mm²) → motor usa método COMPLETO com reatância; `rastreio.X_ohm_km` não é None | Teste automatizado |
| **CA-QT-04** | Circuito com `comprimento_m` ausente ou ≤ 0 → `atende = false`, `secao_requerida_mm2 = null` | Teste automatizado |
| **CA-QT-05** | ΔV circuito > 4.0% → `atende = false` e `secao_requerida_mm2` retorna seção da série IEC 60228 que atende | Teste automatizado |
| **CA-QT-06** | ΔV total (alimentador+circuito) > limite_percentual → `atende = false` | Teste automatizado |
| **CA-QT-07** | ~~Comprimento manual prevalece sobre estimativa~~ → **REMOVIDO** nesta versão (somente manual existe — CORREÇÃO 2) | — |
| **CA-QT-08** | ~~Estimativa via geometria Manhattan + vertical + margem~~ → **FORA DE ESCOPO** nesta versão (CORREÇÃO 2, §7.2) | — |
| **CA-QT-09** | Simulador com 3 cenários retorna 3 resultados, cada um com `queda_percentual` recalculado | Teste automatizado |
| **CA-QT-10** | Botão "Aplicar" no simulador grava nova seção e dispara recálculo MOD-DC | Teste E2E |
| **CA-QT-11** | Visualização em árvore mostra queda acumulada correta (soma alimentador + circuito) | Inspeção visual |
| **CA-QT-12** | Valores de resistência com `status_verificacao = '[VERIFICAR]'` → campo `fonte` do `RetornoMODQT` inclui `[VERIFICAR]` | Teste automatizado |
| **CA-QT-13** | Endpoint público (`/api/v1/modulos/mod-qt/validar`) com 44 circuitos do proj-1 retorna em < 2 segundos | Teste de performance |
| **CA-QT-14** | Gráfico de barras no simulador renderiza com linhas de limite a 4% e ao limite total (5% ou 7%) | Inspeção visual |
| **CA-QT-15** | Campo `fonte` contém: versão do módulo, método, R com status, L, IB, V, referência normativa | Teste automatizado |
| **CA-QT-16** | Texto branco sobre fundo #fa4d56 não aparece em nenhum estado de erro | Teste automatizado (herança DS-04) |
| **CA-QT-17** | `secao_requerida_mm2` retornado está na série IEC 60228 (R-02) | Teste automatizado |
| **CA-QT-18** | Contrato de response do endpoint público é exatamente `RetornoMODQT` — campos `atende`, `queda_percentual`, `limite_aplicado`, `secao_requerida_mm2`, `fonte` — sem campos adicionais | Teste automatizado (schema validation) |
| **CA-QT-19** | **Não-regressão do mock:** toda entrada que hoje passa pelo mock (`validarModQTMock`) e retorna `atende = true` deve produzir `atende = true` com o motor real, ou a diferença deve ser documentada com causa normativa (ex.: mock usava ρ genérica, motor usa R tabelada mais precisa) | Teste automatizado |
| **CA-QT-20** | Limite de 4% para circuito terminal aparece como `CONFIRMADO` com citação `NBR 5410:2004, §6.2.7` em todo lugar onde é usado | Inspeção de código |
| **CA-QT-21** | Para projetos EDP-SP: chamada ao endpoint com `limite_percentual = 1.0` e `origem = "RAMAL-ENTRADA-EDP"` para o trecho ramal de entrada retorna `atende = false` quando ΔV > 1% | Teste automatizado |
| **CA-QT-22** | O limite total (5% ou 7%) usado para projetos EDP-SP carrega marcação `[VERIFICAR]` no campo `fonte` até que a alínea aplicável da 6.2.7.1 seja confirmada contra a prática da concessionária | Teste automatizado |

---

## 27. ESTADOS

O MOD-QT não mantém uma máquina de estados própria. O motor é **stateless**: recebe um request (`ValidarMODQTSchema`), calcula, e retorna um response (`RetornoMODQT`). O campo `atende` do response é o único indicador de estado relevante (`true` / `false`).

O estado do circuito no contexto do MOD-DC (onde o MOD-QT é invocado como critério C5) é gerenciado pelo `servico-dimensionamento-condutores.ts`, não pelo MOD-QT. Se o MOD-DC recebe `atende = false`, ele entra no laço de revalidação C1/C2/C6 com `secao_requerida_mm2` como piso — mas esse laço é responsabilidade do MOD-DC, não do MOD-QT.

O simulador de cenários (§21) é uma interface de exploração sem persistência de estado entre sessões — cada simulação é independente.

Não aplicável: máquina de estados, transições, ou estados bloqueantes próprios do MOD-QT.

---

## 28. SUITE DE NÃO-REGRESSÃO (pytest)

```python
import pytest
from motor_queda_tensao import calcular_queda_tensao, simular_cenarios
from contratos import RetornoMODQT

SERIE_IEC_60228 = [0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500]

# ─── Fixtures ───

@pytest.fixture
def request_mono_basico():
    """Request no formato do contrato público ValidarMODQTSchema."""
    return {
        "dependencia_id": "00000000-0000-0000-0000-000000000001",
        "corrente_a": 2.36,
        "comprimento_m": 12.0,
        "secao_mm2": 1.5,
        "limite_percentual": 7.0,
        "origem": "TESTE"
    }

@pytest.fixture
def contexto_mono_basico():
    """Contexto adicional (não faz parte do contrato público)."""
    return {
        "material": "Cu", "isolacao": "PVC",
        "num_fases": 1, "fp_carga": 1.0, "tensao_v": 127.0
    }

@pytest.fixture
def request_sem_comprimento():
    return {
        "dependencia_id": "00000000-0000-0000-0000-000000000002",
        "corrente_a": 22.7,
        "comprimento_m": 0,  # inválido
        "secao_mm2": 4.0,
        "limite_percentual": 7.0,
        "origem": "TESTE"
    }

@pytest.fixture
def request_acima_limite():
    return {
        "dependencia_id": "00000000-0000-0000-0000-000000000003",
        "corrente_a": 18.2,
        "comprimento_m": 22.0,
        "secao_mm2": 2.5,
        "limite_percentual": 7.0,
        "origem": "TESTE"
    }

@pytest.fixture
def contexto_acima_limite():
    return {
        "material": "Cu", "isolacao": "PVC",
        "num_fases": 1, "fp_carga": 0.85, "tensao_v": 220.0
    }

@pytest.fixture
def request_secao_grande():
    return {
        "dependencia_id": "00000000-0000-0000-0000-000000000004",
        "corrente_a": 52.5,
        "comprimento_m": 30.0,
        "secao_mm2": 35.0,
        "limite_percentual": 7.0,
        "origem": "TESTE"
    }

@pytest.fixture
def contexto_secao_grande():
    return {
        "material": "Cu", "isolacao": "PVC",
        "num_fases": 3, "fp_carga": 0.80, "tensao_v": 220.0
    }

# ─── Testes CA-QT ───

def test_ca_qt_01_mono_simplificado(request_mono_basico, contexto_mono_basico):
    """CA-QT-01: Monofásico simplificado — conferência aritmética."""
    interno = calcular_queda_tensao(request_mono_basico, **contexto_mono_basico)
    publico = mapear_para_retorno_publico(interno)
    
    assert interno.metodo_calculo == "SIMPLIFICADO"
    assert 0.0 < publico.queda_percentual < 10.0  # sanity
    assert publico.queda_percentual == pytest.approx(
        interno.delta_v_absoluto_v / 127.0 * 100, abs=0.01
    )

def test_ca_qt_02_trifasico(request_secao_grande, contexto_secao_grande):
    """CA-QT-02: Trifásico usa fator √3."""
    contexto_tri_simples = {**contexto_secao_grande, "fp_carga": 1.0}
    # Forçar seção ≤ 25 para testar simplificado com √3
    req = {**request_secao_grande, "secao_mm2": 10.0}
    interno = calcular_queda_tensao(req, **contexto_tri_simples)
    assert interno.metodo_calculo == "SIMPLIFICADO"
    assert "√3" in interno.rastreio.get("formula", "")

def test_ca_qt_03_metodo_completo(request_secao_grande, contexto_secao_grande):
    """CA-QT-03: Seção > 25 mm² → método completo com reatância."""
    interno = calcular_queda_tensao(request_secao_grande, **contexto_secao_grande)
    assert interno.metodo_calculo == "COMPLETO"
    assert interno.rastreio.get("X_ohm_km") is not None

def test_ca_qt_04_sem_comprimento(request_sem_comprimento):
    """CA-QT-04: Sem comprimento → atende = false."""
    interno = calcular_queda_tensao(request_sem_comprimento, material="Cu",
                                     isolacao="PVC", num_fases=1, fp_carga=1.0, tensao_v=220.0)
    publico = mapear_para_retorno_publico(interno)
    assert publico.atende == False

def test_ca_qt_05_acima_limite_secao_requerida(request_acima_limite, contexto_acima_limite):
    """CA-QT-05: ΔV > 4% → atende=false + secao_requerida_mm2 na série IEC."""
    interno = calcular_queda_tensao(request_acima_limite, **contexto_acima_limite)
    publico = mapear_para_retorno_publico(interno)
    if publico.queda_percentual > 4.0:
        assert publico.atende == False
        assert publico.secao_requerida_mm2 is not None
        assert publico.secao_requerida_mm2 in SERIE_IEC_60228

def test_ca_qt_09_simulador(request_acima_limite, contexto_acima_limite):
    """CA-QT-09: Simulador retorna N resultados."""
    from motor_queda_tensao import CenarioSimulacao
    cenarios = [
        CenarioSimulacao(id="CEN-01", descricao="4 mm²", secao_mm2=4.0),
        CenarioSimulacao(id="CEN-02", descricao="6 mm²", secao_mm2=6.0),
        CenarioSimulacao(id="CEN-03", descricao="Comprimento 15m", comprimento_m=15.0),
    ]
    resultados = simular_cenarios(request_acima_limite, contexto_acima_limite, cenarios)
    assert len(resultados) == 3

def test_ca_qt_12_verificar_impedancia(request_mono_basico, contexto_mono_basico):
    """CA-QT-12: Impedância com status [VERIFICAR] → fonte inclui [VERIFICAR]."""
    interno = calcular_queda_tensao(request_mono_basico, **contexto_mono_basico)
    publico = mapear_para_retorno_publico(interno)
    if interno.rastreio.get("status_resistencia") == "[VERIFICAR]":
        assert "[VERIFICAR]" in publico.fonte

def test_ca_qt_15_fonte_completa(request_mono_basico, contexto_mono_basico):
    """CA-QT-15: Campo fonte contém todas as informações obrigatórias."""
    interno = calcular_queda_tensao(request_mono_basico, **contexto_mono_basico)
    publico = mapear_para_retorno_publico(interno)
    assert "MOD-QT" in publico.fonte
    assert "§6.2.7" in publico.fonte or "6.2.7" in publico.fonte

def test_ca_qt_17_secao_serie_iec(request_acima_limite, contexto_acima_limite):
    """CA-QT-17: secao_requerida_mm2 sempre na série IEC 60228."""
    interno = calcular_queda_tensao(request_acima_limite, **contexto_acima_limite)
    publico = mapear_para_retorno_publico(interno)
    if publico.secao_requerida_mm2 is not None:
        assert publico.secao_requerida_mm2 in SERIE_IEC_60228

def test_ca_qt_18_contrato_publico_exato(request_mono_basico, contexto_mono_basico):
    """CA-QT-18: Response tem exatamente os campos de RetornoMODQT."""
    interno = calcular_queda_tensao(request_mono_basico, **contexto_mono_basico)
    publico = mapear_para_retorno_publico(interno)
    campos_esperados = {"atende", "queda_percentual", "limite_aplicado", "secao_requerida_mm2", "fonte"}
    campos_reais = set(publico.__dict__.keys()) if hasattr(publico, '__dict__') else set(publico.keys())
    assert campos_reais == campos_esperados

def test_ca_qt_19_nao_regressao_mock():
    """CA-QT-19: Entradas que passam pelo mock devem passar pelo motor real.
    O mock usa: ΔV = 2 × corrente × RHO_COBRE × comprimento / (secao × TENSAO_REF_V) × 100
    com RHO_COBRE = 0.0172 e TENSAO_REF_V = 220.
    """
    # Caso típico que passa no mock
    request_mock = {
        "dependencia_id": "00000000-0000-0000-0000-000000000099",
        "corrente_a": 10.0,
        "comprimento_m": 15.0,
        "secao_mm2": 2.5,
        "limite_percentual": 4.0,
        "origem": "TESTE-REGRESSAO"
    }
    # Resultado do mock: ΔV = 2 × 10 × 0.0172 × 15 / (2.5 × 220) × 100 = 0.94%
    # atende = true (0.94% < 4.0%)
    
    interno = calcular_queda_tensao(request_mock, material="Cu", isolacao="PVC",
                                     num_fases=1, fp_carga=1.0, tensao_v=220.0)
    publico = mapear_para_retorno_publico(interno)
    
    # Motor real deve também aprovar (resultado pode ser ligeiramente diferente
    # por usar R tabelada em vez de ρ genérica, mas a direção deve ser a mesma)
    assert publico.atende == True, (
        f"Não-regressão: mock aprovava este caso, motor real reprovou. "
        f"queda_percentual={publico.queda_percentual}. Investigar causa."
    )
```

---

## 29. PARÂMETROS CONFIGURÁVEIS

| Parâmetro | Padrão | Fonte | Status |
|-----------|--------|-------|--------|
| Limite ΔV circuito terminal | 4.0% | NBR 5410:2004 §6.2.7 | **CONFIRMADO** |
| Limite ΔV total (transformador distribuidora) | 7.0% | NBR 5410:2004 §6.2.7.1 | **CONFIRMADO** |
| Limite ΔV total (ponto de entrega tensão secundária) | 5.0% | NBR 5410:2004 §6.2.7.2 | **CONFIRMADO** |
| Resistividade Cu a 20°C | 0.01724 Ω·mm²/m | — | `[VERIFICAR — IEC 60228]` |
| Resistividade Al a 20°C | 0.02826 Ω·mm²/m | — | `[VERIFICAR — IEC 60228]` |
| Temperatura de serviço PVC | 70°C | NBR 5410:2004 Tab. 35 | **CONFIRMADO** (MOD-DC §13.3) |
| Temperatura de serviço EPR/XLPE | 90°C | NBR 5410:2004 Tab. 35 | **CONFIRMADO** (MOD-DC §13.3) |
| Altura de tomada baixa (parâmetro de projeto) | 0.30 m | Prática de arquitetura/projeto — **não** é cota exigida pela NBR 5410 | **RESOLVIDO** — parâmetro de projeto, não normativo (VER-QT-06) |
| Altura de tomada média (parâmetro de projeto) | 1.10 m | Prática de arquitetura/projeto — **não** é cota exigida pela NBR 5410 | **RESOLVIDO** — parâmetro de projeto, não normativo (VER-QT-06) |
| Altura de tomada alta (parâmetro de projeto) | 2.00 m | Prática de arquitetura/projeto — **não** é cota exigida pela NBR 5410 | **RESOLVIDO** — parâmetro de projeto, não normativo (VER-QT-06) |
| Pé-direito padrão | 2.80 m | Prática | Configurável, não normativo |
| Limite ΔV ramal de entrada EDP-SP | 1.0% | PT.DT.PDN.00068 v09, 5.4.6 | **CONFIRMADO** (chunk 22) |
| Tolerância adicional > 100 m | +0.005%/m, max +0.5% | NBR 5410:2004 §6.2.7 nota 3 | **CONFIRMADO** (não implementado nesta versão) |

---

## 30. PENDÊNCIAS [VERIFICAR]

| ID | Item | Fonte necessária | Impacto | Status |
|----|------|-------------------|---------|--------|
| **VER-QT-01** | ~~Limites de queda de tensão (4%/7%/5%)~~ | ~~NBR 5410~~ | — | **RESOLVIDO → CONFIRMADO** (§13.1). Promovido na v2.1 com citação de NBR 5410:2004 §6.2.7.1/6.2.7.2, linhas ~10144–10178 do `NBR-5410.md`. |
| **VER-QT-02** | Valores de resistência (Ω/km) por seção para Cu e Al, a 70°C (PVC) e 90°C (EPR/XLPE) | Catálogo Prysmian/Nexans ou IEC 60364-5-52 Annex G | **Bloqueante**: sem esses valores, o motor não pode calcular com precisão. Valores provisórios listados em §13.4, mas todo resultado deve incluir `[VERIFICAR]` no campo `fonte`. **CORREÇÃO:** a citação "Anexo G da NBR 5410" do v2.0 estava errada (Anexo G trata de equipotencialização, não impedância). | Aberto |
| **VER-QT-03** | Valores de reatância indutiva (Ω/km) por seção para Cu e Al (seções > 25 mm²) | Catálogo Prysmian/Nexans ou IEC 60364-5-52 Annex G | **Bloqueante para método completo**: sem reatância, seções > 25 mm² usam apenas R (degradação para método simplificado). **Mesma CORREÇÃO de fonte** do VER-QT-02. | Aberto |
| **VER-QT-04** | Fórmula para circuito bifásico (fase-fase sem neutro): fator multiplicativo é 2 ou √3? | NBR 5410:2004 ou IEC 60364-5-52 | **Bloqueante para bifásico**: até resolução, o motor usa fator 2 (conservador) com alerta explícito. Não foi localizado trecho normativo que resolva. | Aberto |
| **VER-QT-05** | ~~Temperatura de referência (70°C PVC / 90°C EPR-XLPE)~~ | ~~NBR 5410~~ | — | **RESOLVIDO → CONFIRMADO** por reaproveitamento do MOD-DC §13.3 (Tabela 35, chunk 117). |
| **VER-QT-06** | ~~Alturas padronizadas de tomada (0.30, 1.10, 2.00 m)~~ | Parecer `docs/research/{2026-07-28}-resolucao-ver-qt.md` §3.5 e §6 C-06 | **RESOLVIDO — parâmetro de projeto, não normativo.** A NBR 5410 **não fixa** essas cotas: elas são parâmetros de arquitetura/projeto, editáveis. Rótulo de UI, ajuda contextual, memorial e estimativa de comprimento **não podem** atribuí-las à NBR 5410. Implementado pela story `MOD-QT-2-04` (AC7). | **RESOLVIDO** (2026-07-29) |
| **VER-QT-07** | Qual alínea da NBR 5410 6.2.7.1 se aplica ao modelo de atendimento EDP-SP: alínea b) → 7% (ponto de entrega nos terminais do transformador da distribuidora) ou alínea c) → 5% (ponto de entrega em tensão secundária, demais casos)? | PT.DT.PDN.00068 v09 (modelo de atendimento) + definição de "ponto de entrega" em NBR 5410 3.4.3 | **RESOLVIDO APENAS para o perfil `EDP_SP_PTDTPDN00068_V09_AEREA_BT`** (EDP-SP, PT.DT.PDN.00068 v09, rede aérea, BT): alínea c) → `limite_total_pct = 5`, trecho conexão-medição 1% (parecer §3.4, §6 C-05). Sob esse perfil o campo `fonte` do `RetornoMODQT` **não** carrega `[VERIFICAR — alínea 6.2.7.1]`. Para qualquer outro modelo de atendimento a pendência **permanece aberta** e a marcação continua obrigatória. Implementado pela story `MOD-QT-2-04` (AC4/AC9). | Parcial — resolvido só no perfil EDP-SP v09; **aberto** fora dele |

---

## 31. NÃO TOCAR

- Módulo de Cargas (levantamento de cargas)
- Módulo de Demanda (cálculo de demanda, fatores de demanda)
- Módulo IB (cálculo de corrente de projeto)
- Módulo MOD-DC (dimensionamento de condutores) — o MOD-QT **retorna** `secao_requerida_mm2` mas **não modifica** diretamente o MOD-DC; o laço de revalidação é responsabilidade do `servico-dimensionamento-condutores.ts`
- Adaptador 1:1 de circuitos (provisório)
- Módulo de Categoria de Entrada (Saída A / Saída B)
- Tabelas 001/002 (subcategoria EDP)
- Fórmula de demanda EDP (D = a+b+...+i)
- Mapeamento de fases (R/S/T e helper ABC→RST)
- Contrato público `RetornoMODQT` e `ValidarMODQTSchema` (inalteráveis)
- Endpoint `/api/v1/modulos/mod-qt/validar` (rota e schema inalteráveis)

---

## 32. CHECKLIST DE ENTREGA

Verificar antes de considerar o MOD-QT implementado:

- [ ] Endpoint `POST /api/v1/modulos/mod-qt/validar` aceita `ValidarMODQTSchema` e retorna `RetornoMODQT` exatamente conforme §15.1
- [ ] Mock `validarModQTMock` substituído pelo motor real no handler
- [ ] Todos os CA-QT-01 a CA-QT-22 passando (testes automatizados e inspeções visuais)
- [ ] Suite de não-regressão (§28) executada sem falhas
- [ ] Nenhum valor normativo inventado — todo `[VERIFICAR]` mantido onde fontes não confirmadas
- [ ] Campo `fonte` do `RetornoMODQT` inclui `[VERIFICAR]` quando valores de resistência não confirmados
- [ ] Limite EDP 1% (§13.8) implementado para perfil de concessionária EDP-SP
- [ ] Limite total (5%/7%) carrega `[VERIFICAR — alínea 6.2.7.1]` no campo `fonte` até VER-QT-07 resolvido
- [ ] UI segue IBM Carbon Design System; proibido texto branco sobre `#fa4d56` (R-05, test_ds04); gráficos via `@carbon/charts-react`; contraste mínimo WCAG AA (4,5:1 texto normal, 3:1 texto grande); tooltips e labels acessíveis
- [ ] Nenhum item da lista NÃO TOCAR (§31) foi alterado
- [ ] Simulador de cenários funcional com gráfico de barras e linhas de limite

---

## 33. INSTRUÇÕES FINAIS

### Segurança e responsabilidade técnica (HERDADO DO MOD-DC)

Nenhum valor de queda de tensão aprovado por este módulo constitui declaração de conformidade normativa completa. O módulo é ferramenta de auxílio ao projetista — a responsabilidade técnica pelo projeto é do engenheiro responsável. Valores com `status_verificacao = '[VERIFICAR]'` devem ser tratados como provisórios em qualquer documento exportado, com indicação visual clara. Registros de rastreabilidade (`rastreio`, `fonte`) são preservados integralmente para auditoria e não podem ser apagados ou simplificados na exportação.

### Ordem de implementação recomendada

1. Implementar o motor de cálculo (§18–§20) com tabela de impedância provisória (`[VERIFICAR]`)
2. Substituir `validarModQTMock` pelo motor real no endpoint público (§23.1)
3. Validar CA-QT-19 (não-regressão do mock) antes de qualquer outro teste
4. Implementar interface de visualização (§24–§25) e simulador (§21)
5. Resolver VER-QT-02 e VER-QT-03 (resistência/reatância) com catálogos de fabricante
6. Resolver VER-QT-07 (alínea 6.2.7.1 para EDP-SP) com a concessionária
7. Resolver VER-QT-04 (fórmula bifásico) contra fonte normativa

### Sobre este documento

Este documento é insumo direto para abrir o épico MOD-QT-2 (motor real de queda de tensão). Nenhum revisor humano deve precisar voltar ao v2.0 ou v2.1 para esclarecer nome de campo, fonte normativa ou escopo. Toda decisão técnica está registrada nas CORREÇÕES (§2) e toda lacuna nas PENDÊNCIAS (§30).
