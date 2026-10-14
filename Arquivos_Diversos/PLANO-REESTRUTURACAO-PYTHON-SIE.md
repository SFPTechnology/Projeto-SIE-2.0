# Plano de Reestruturação do SIE para Bibliotecas Python

> **Autor:** Atlas (Analyst / AIOX) — discovery + plano de re-arquitetura
> **Data:** 2026-06-20
> **Sistema-origem:** `sistema-de-instala-es-el-tricas-sie-main` (TypeScript / TanStack Start / React 19 / Supabase)
> **Objetivo:** reestruturar **lógica, matemática, gráfica e símbolos** dos componentes e do código para um ecossistema de **bibliotecas Python**.
> **Natureza:** descritivo e prescritivo. **Nenhum código foi escrito.** Este documento desenha a arquitetura-alvo, a seleção de bibliotecas e o mapeamento módulo-a-módulo.

---

## 0. Sumário executivo

O SIE hoje é uma aplicação **TypeScript full-stack** com um núcleo de domínio **puro, table-driven e testável** (`src/domain/`). Esse núcleo é o ativo de maior valor e o que melhor se traduz para Python.

A reestruturação proposta **não** é "reescrever o app React em Python". É **extrair o cérebro do sistema para um conjunto de bibliotecas Python independentes, versionáveis e publicáveis**, organizadas pelos quatro eixos pedidos:

| Eixo | O que cobre | Estado de origem | Bibliotecas Python âncora |
|---|---|---|---|
| **Lógica** | Entidades, máquina de estados, regras, gates fail-closed, divisão de circuitos | 🟢 Maduro em TS | `pydantic`, `python-statemachine`, `networkx` |
| **Matemática** | Demanda, IB, ampacidade, queda de tensão, balanceamento, arredondamento | 🟢 Maduro em TS (fórmulas com IDs F-01…) | `pint`, `numpy`, `scipy`, `sympy` |
| **Gráfica** | Diagrama unifilar, quadro de cargas, gráficos, exportação PDF/DXF/SVG | 🔴 Inexistente | `schemdraw`, `matplotlib`, `ezdxf`, `reportlab` |
| **Símbolos** | Biblioteca de símbolos elétricos NBR 5444 / IEC 60617 | 🔴 Inexistente | `schemdraw.elements` + `drawsvg` (catálogo próprio) |

**Tese central:** Python ganha decisivamente em **dois pontos** que hoje são frágeis em TS:
1. **Segurança dimensional** — `pint` torna impossível somar VA com W ou tratar 127 V como 220 V silenciosamente (o bug recorrente do sistema atual).
2. **Rastreabilidade matemática** — `sympy` permite gerar o "memorial de cálculo" automaticamente (fórmula simbólica → substituição → resultado), atendendo nativamente ao requisito de auditoria.

Em compensação, **gráfica e símbolos são greenfield** — não há nada a portar; há a construir. É justamente onde o ecossistema Python (`schemdraw`, `ezdxf`) é mais forte que o JS.

---

## 1. Diagnóstico da origem (o que existe e como está estruturado)

### 1.1 Núcleo de domínio (alvo da portabilidade)

```
src/domain/
  calculo/        ← funções puras: geometria, iluminacao, tomadas, motor,
                    corrente-projeto, corrente-circuitos, balanceamento-fases,
                    derivar-circuitos (provisório), resolver-ligacao
  distribuidora/edp-sp/  ← regras EDP-SP + tabelas .data.json + 11 suítes Vitest
  nbr/            ← catálogo NBR (tipos, fatores de demanda, fornecimento)
  modelo/         ← entidades: Projeto, Dependencia, Circuito, PadraoEntrada
  estado/         ← máquina de estados (estados, eventos, transicoes)
  servicos/       ← casos de uso (cálculo, validação, edição, recálculo, auditoria)
```

### 1.2 Características que favorecem a portabilidade

- **Funções puras com IDs de fórmula** — ex.: `geometria.ts` (F-01 Área, F-02 Perímetro), `iluminacao.ts` (F-07/F-08), `corrente-projeto.ts` (`IB = S/(fator·V)`, √3 para trifásico). Cada fórmula já é nomeada e isolada → vira função pura + caso de teste em Python 1:1.
- **Dados normativos em JSON versionável** — `categorias-fornecimento.data.json`, `fatores-potencia.data.json`, `tabela_005…015.data.json`, `subcategorias-fornecimento.data.json`. Migram para CSV/Parquet/JSON consumidos por `pandas`.
- **Máquina de estados explícita** — `estado/transicoes.ts` é uma matriz `(estado, transição) → estado`. Mapeia direto para `python-statemachine`.
- **Validação como diagnóstico** — `validacao.ts` produz lista de diagnósticos tipados. Mapeia para um motor de regras Python (Pydantic validators + regras de negócio).
- **23 tipos de aparelho + 9 grupos de demanda** como enums fechados (`tipos-aparelho.ts`, `grupos-demanda.ts`) → `enum.Enum` em Python.

### 1.3 O que NÃO existe na origem (greenfield, confirmado por inspeção)

- Nenhum código de **diagrama unifilar**, **quadro de cargas gráfico** ou **símbolos elétricos**.
- Nenhum **dimensionamento de condutor / queda de tensão / proteção por circuito** (campos ausentes em `modelo/circuito.ts`).
- Nenhuma **exportação** (PDF/DXF/SVG).

---

## 2. Arquitetura-alvo: ecossistema de pacotes Python

Monorepo Python (gerenciado por **`uv`** + **workspaces**, ou **Poetry**), com pacotes desacoplados e publicáveis independentemente:

```
sie/                         (monorepo)
├── packages/
│   ├── sie-norms/           ← dados normativos versionados (NBR 5410 + EDP-SP)
│   ├── sie-core/            ← entidades, enums, máquina de estados, gates (LÓGICA)
│   ├── sie-calc/            ← motor matemático: demanda, IB, ampacidade, queda (MATEMÁTICA)
│   ├── sie-symbols/         ← biblioteca de símbolos NBR/IEC (SÍMBOLOS)
│   ├── sie-graphics/        ← unifilar, quadro de cargas, gráficos, export (GRÁFICA)
│   ├── sie-report/          ← memorial de cálculo + relatório técnico (PDF)
│   └── sie-api/             ← (opcional) FastAPI expondo o domínio
├── tests/                   ← pytest + golden tests cruzados (TS ↔ Python)
└── pyproject.toml
```

**Dependências entre pacotes (DAG, sem ciclos):**

```
sie-norms ─┬─> sie-calc ─┬─> sie-graphics ─> sie-report
           └─> sie-core ─┘        ^
                  │                │
                  └────────────────┘
sie-symbols ─> sie-graphics
```

**Princípio:** `sie-core` e `sie-calc` são **puros** (sem I/O, sem rede). `sie-norms` é só dado. `sie-graphics`/`sie-report` são as bordas com efeitos colaterais (arquivos). Espelha a separação que o TS já pratica.

---

## 3. Eixo LÓGICA — bibliotecas e mapeamento

### 3.1 Seleção de bibliotecas

| Necessidade | Biblioteca Python | Por quê |
|---|---|---|
| Entidades imutáveis + validação | **Pydantic v2** | Substitui Zod; validação fail-closed declarativa; `model_config(frozen=True)` = imutabilidade do TS (`readonly`) |
| Enums fechados (TipoAparelho, Grupo, Estado) | **`enum.StrEnum`** (3.11+) | 1:1 com os union types do TS |
| Máquina de estados | **`python-statemachine`** | Substitui `transicoes.ts`; transições declarativas + guardas (gates) |
| Topologia de circuitos | **`networkx`** | Modela Projeto→Quadro→Circuito→Carga como grafo; valida "cada carga em exatamente 1 circuito" |
| Injeção de dependência (repos/clock) | **`dependency-injector`** | Substitui o `ContextoApp` do TS |
| Persistência (se mantida) | **`supabase-py`** ou **SQLAlchemy 2** | Reaproveita o schema Supabase existente (`docs/supabase/*.sql`) |

### 3.2 Mapeamento de módulos (TS → Python)

| Origem TS | Destino Python | Tipo |
|---|---|---|
| `modelo/dependencia.ts`, `projeto.ts`, `circuito.ts` | `sie_core.models` (Pydantic) | Port direto |
| `distribuidora/edp-sp/tipos-aparelho.ts`, `grupos-demanda.ts` | `sie_core.enums` + `sie_norms.classificacao` | Port direto |
| `estado/estados.ts`, `eventos.ts`, `transicoes.ts` | `sie_core.state.DependenciaMachine` | Port + reforço |
| `servicos/servico-*.ts` | `sie_core.services` (use-cases) | Port + **gates fail-closed** |
| `distribuidora/edp-sp/validacao.ts` | `sie_core.rules` (motor de diagnósticos) | Port + promover ERRO→blocker |
| `calculo/derivar-circuitos.ts` (provisório) | `sie_core.circuits.divisor` (NBR 9.5.3 real) | **Greenfield** (substitui o provisório) |

### 3.3 Reforços de lógica a embutir na reestruturação

- **Fail-closed nativo:** as guardas da `python-statemachine` impedem `CALCULAR` enquanto houver pendência crítica (resolve o defeito de "calcula com dado incompleto" descrito no plano de correção).
- **Gates G1–G6** como pré-condições de transição, não como avisos de UI.
- **Divisão de circuitos real** (NBR 9.5.3) usando `networkx` para garantir invariantes topológicas.

---

## 4. Eixo MATEMÁTICA — bibliotecas e mapeamento

### 4.1 Seleção de bibliotecas (núcleo da proposta)

| Necessidade | Biblioteca Python | Ganho sobre o TS atual |
|---|---|---|
| **Grandezas com unidade** (VA, W, A, V, mm², m, °C) | **Pint** | **Crítico.** Hoje a unidade vive no nome da variável (`potencia_VA`, `tensao_V`). Pint torna `127 V` ≠ `220 V` checável e impede somar VA com W. Elimina a classe de bug "TUE assume 220 V" |
| Tabelas normativas (lookup/interpolação) | **NumPy + pandas** | Lookup vetorizado em ampacidade (Tab. 36–39), interpolação de fatores de correção |
| Otimização do balanceamento de fases | **SciPy** (`optimize`) | O `balanceamento-fases.ts` usa LPT guloso; SciPy permite particionamento ótimo/quase-ótimo quando necessário |
| **Rastreabilidade simbólica** (memorial) | **SymPy** | Gera fórmula → substituição → resultado automaticamente. Atende o requisito de "memória de cálculo auditável" sem string-building manual |
| Arredondamento normativo determinístico | **`decimal.Decimal`** | Substitui `lib/utils/round.ts`; arredondamento exato e reproduzível para exibição |
| Modelagem de incerteza (opcional) | **`uncertainties`** | Propagação de tolerância em medições, se exigido pelo eng. responsável |

### 4.2 Mapeamento de fórmulas (TS → Python)

| Fórmula (ID) | Origem TS | Destino `sie-calc` | Biblioteca |
|---|---|---|---|
| F-01 Área = L×C; F-02 Perímetro = 2(L+C)−exc | `geometria.ts` | `sie_calc.geometria` | Pint (m, m²) |
| F-07/F-08 Iluminação mínima | `iluminacao.ts` | `sie_calc.iluminacao` | Pint + Decimal |
| TUG por perímetro/área | `tomadas.ts` | `sie_calc.tomadas` | Pint |
| `IB = S/(fator·V)`, √3 trifásico | `corrente-projeto.ts`, `corrente-circuitos.ts` | `sie_calc.corrente` | Pint + SymPy (rastreio) |
| Demanda por grupo (FD, D1/D3, DT) | `motor-demanda.ts`, `fatores-demanda.ts` | `sie_calc.demanda` | pandas + Pint |
| Seleção categoria/subcategoria | `seletor-categoria.ts`, `seletor-subcategoria.ts` | `sie_calc.entrada` | pandas (tabelas 001/002) |
| Balanceamento de fases (LPT) | `balanceamento-fases.ts` | `sie_calc.balanceamento` | NumPy/SciPy |
| **Ampacidade + correção (Iz)** | — (inexistente) | `sie_calc.condutores` | NumPy + pandas | **Greenfield** |
| **Queda de tensão** | — (inexistente) | `sie_calc.queda` | Pint + NumPy | **Greenfield** |
| **Proteção (IB≤In≤Iz, I₂≤1,45·Iz)** | — (inexistente) | `sie_calc.protecao` | pandas | **Greenfield** |

### 4.3 Padrão de função matemática rastreável (conceito)

Cada cálculo retorna **não só o número, mas o rastro**: fórmula simbólica (SymPy), substituições, unidade (Pint), regra/versão normativa e arredondamento. Esse objeto alimenta o memorial (Eixo Gráfica/Report) sem reprocessamento — fecha o requisito de auditoria que o sistema atual só atende parcialmente.

---

## 5. Eixo GRÁFICA — bibliotecas e mapeamento

> Greenfield total. Aqui Python tem vantagem clara sobre o stack JS atual.

### 5.1 Seleção de bibliotecas

| Artefato gráfico | Biblioteca Python | Justificativa |
|---|---|---|
| **Diagrama unifilar** | **`schemdraw`** | Biblioteca de referência para esquemas elétricos em Python; layout de barramentos, disjuntores, circuitos terminais |
| **Topologia/roteamento do diagrama** | **`networkx`** | Reusa o grafo do `sie-core`; calcula posições e ordem dos circuitos |
| **Quadro de cargas / gráficos** | **`matplotlib`** | Backend do schemdraw; barras de balanceamento de fases (A/B/C), tabelas |
| **Exportação CAD** | **`ezdxf`** | Gera DXF para AutoCAD/QCAD — requisito real de engenheiros para entregar projeto executivo |
| **Vetor web/SVG** | **`drawsvg`** ou **`svgwrite`** | Unifilar e símbolos embutíveis em web/relatório |
| **Gráficos interativos (se UI web)** | **`plotly`** | Quadro de cargas e balanceamento interativos no front |

### 5.2 Saídas a gerar (que hoje não existem)

1. **Diagrama unifilar** — entrada (padrão EDP) → medição → disjuntor geral → DPS → DR → barramentos (fase/neutro/PE) → circuitos terminais → aterramento → legenda/revisão.
2. **Quadro de cargas por circuito** — circuito, descrição, ambiente, potência, tensão, fases, IB, disjuntor, condutor (fase/N/PE), método, comprimento, queda, DR, status.
3. **Gráfico de balanceamento de fases** — corrente/potência por fase, antes/depois, % de desequilíbrio.
4. **Formatos de export** — SVG (web), PDF (entrega), DXF (CAD).

### 5.3 Estratégia de renderização

`sie-graphics` consome o **resultado do `sie-calc` + o grafo do `sie-core`** e produz uma **representação intermediária** (DSL de diagrama) que é então renderizada por múltiplos backends (schemdraw→matplotlib→PDF/SVG; ezdxf→DXF). Isso desacopla "o que desenhar" de "em qual formato", permitindo adicionar backends sem tocar na lógica.

---

## 6. Eixo SÍMBOLOS — bibliotecas e mapeamento

> Greenfield. Requer construir um **catálogo de símbolos normativos** reutilizável.

### 6.1 Norma de referência

- **ABNT NBR 5444** (símbolos gráficos para instalações elétricas prediais) e **IEC 60617** (símbolos para diagramas).

### 6.2 Seleção de bibliotecas / fontes

| Necessidade | Biblioteca / fonte | Observação |
|---|---|---|
| Símbolos de esquema (disjuntor, DR, DPS, fonte, terra) | **`schemdraw.elements`** (estender) | Já traz muitos elementos IEC; faltantes viram subclasses |
| Símbolos vetoriais próprios (ponto de luz, TUG, TUE, quadro) | **`drawsvg`** | Definir cada símbolo como SVG parametrizável |
| Fonte aberta de símbolos | **Coleção QElectroTech** (XML/SVG, licença aberta) | Acelera o catálogo; converter para o formato `sie-symbols` |
| Metadados normativos por símbolo | Pydantic (`sie_core`) | Cada símbolo carrega: nome, norma, referência, categoria |

### 6.3 Estrutura do pacote `sie-symbols`

Cada símbolo = **(a)** elemento `schemdraw` para o unifilar, **(b)** asset SVG para plantas/web, **(c)** metadado (norma + referência). Catálogo mínimo: ponto de luz, luminária, TUG (seca/molhada), TUE, disjuntor (uni/bi/tripolar), DR, DPS, barramento, aterramento/BEP, medidor, motor, quadro de distribuição.

### 6.4 Por que separar `sie-symbols` de `sie-graphics`

Símbolos são um **vocabulário reutilizável** (também úteis em plantas baixas, legendas, documentação), enquanto `sie-graphics` é a **composição** desses símbolos em diagramas. Separar permite versionar o vocabulário normativo independentemente (quando a NBR 5444 for revisada, só `sie-symbols` muda).

---

## 7. Persistência, API e front-end (decisões de fronteira)

| Aspecto | Opção recomendada | Alternativa |
|---|---|---|
| Banco | Manter **Supabase/Postgres** (reusa `docs/supabase/*.sql`), acessado por `supabase-py`/SQLAlchemy | SQLite local para uso desktop |
| API | **FastAPI** (`sie-api`) expondo casos de uso + Pydantic | Sem API (uso como biblioteca/CLI) |
| Front-end | **Manter o React atual** consumindo `sie-api` (estrangulamento gradual) | Reescrever em **Streamlit** (protótipo) ou **NiceGUI** (desktop) |
| CLI | **Typer** — `sie calcular projeto.json`, `sie unifilar projeto.json --pdf` | — |

**Recomendação:** manter o React e introduzir o FastAPI como gateway. O usuário interage igual; o cérebro passa a ser Python. Isso viabiliza o **strangler fig** (§9) sem big-bang.

---

## 8. Empacotamento, qualidade e distribuição

| Preocupação | Ferramenta |
|---|---|
| Gerenciador/monorepo | **`uv`** (rápido) com workspaces, ou Poetry |
| Tipagem estática | **`mypy`** (strict) — equivalente ao TS estrito atual |
| Lint/format | **`ruff`** (lint+format, substitui ESLint+Prettier) |
| Testes | **`pytest`** + `pytest-cov`; portar as 11 suítes Vitest do EDP-SP |
| Property-based | **`hypothesis`** — testa invariantes matemáticas (ex.: IB ≥ 0; `IB ≤ Iz`) |
| Validação de dados normativos | **`pandera`** — valida os schemas das tabelas (`sie-norms`) |
| Docs | **`mkdocs-material`** + `mkdocstrings` |
| CI | GitHub Actions (já há `.github/` no projeto) |

---

## 9. Estratégia de migração (sem big-bang)

**Padrão Strangler Fig + Golden Tests cruzados:**

```
Fase A — Fundação:    sie-norms + sie-core (entidades/enums/estado) + pytest
Fase B — Paridade:    sie-calc reproduz EXATAMENTE as fórmulas TS existentes
                      → Golden tests: mesma entrada → TS e Python devem bater (tolerância 1e-9)
Fase C — Gateway:     sie-api (FastAPI) + React passa a chamar Python para os módulos já portados
Fase D — Avanço:      construir o greenfield (condutores, queda, proteção, DR/PE) só em Python
Fase E — Gráfica:     sie-symbols + sie-graphics + sie-report (unifilar, quadro, memorial)
Fase F — Desligamento: remover os cálculos TS após paridade comprovada
```

**Golden tests cruzados** são a rede de segurança: exporta-se os casos das 11 suítes Vitest como fixtures JSON; o pytest valida que o `sie-calc` produz o mesmo resultado. Garante que a reestruturação **não muda números** (só estrutura), exceto onde a correção for intencional.

---

## 10. Mapa-resumo: módulo TS → pacote/biblioteca Python

| Origem (TS) | Pacote Python | Biblioteca-chave | Eixo |
|---|---|---|---|
| `domain/modelo/*` | `sie-core.models` | Pydantic | Lógica |
| `domain/estado/*` | `sie-core.state` | python-statemachine | Lógica |
| `domain/servicos/*` | `sie-core.services` | dependency-injector | Lógica |
| `distribuidora/edp-sp/validacao.ts` | `sie-core.rules` | Pydantic | Lógica |
| `*.data.json` (NBR/EDP) | `sie-norms` | pandas + pandera | Matemática |
| `calculo/geometria,iluminacao,tomadas` | `sie-calc.*` | Pint + Decimal | Matemática |
| `calculo/corrente-*` | `sie-calc.corrente` | Pint + SymPy | Matemática |
| `distribuidora/edp-sp/motor-demanda.ts` | `sie-calc.demanda` | pandas + Pint | Matemática |
| `calculo/balanceamento-fases.ts` | `sie-calc.balanceamento` | NumPy/SciPy | Matemática |
| `derivar-circuitos.ts` (provisório) | `sie-core.circuits` | networkx | Lógica (greenfield) |
| — (inexistente) | `sie-calc.condutores/queda/protecao` | NumPy/pandas | Matemática (greenfield) |
| — (inexistente) | `sie-symbols` | schemdraw + drawsvg | Símbolos (greenfield) |
| — (inexistente) | `sie-graphics` | schemdraw, networkx, ezdxf | Gráfica (greenfield) |
| — (inexistente) | `sie-report` | reportlab/weasyprint | Gráfica (greenfield) |
| `routes/api/v1/*` | `sie-api` | FastAPI | Fronteira |

---

## 11. Riscos e mitigações

| Risco | Impacto | Mitigação |
|---|---|---|
| Divergência numérica TS↔Python (float, arredondamento) | Resultados diferentes do validado | Golden tests com tolerância; `Decimal` para exibição |
| `pint` adicionar overhead de performance | Cálculo em lote lento | Usar `pint` na fronteira; NumPy puro no núcleo quente |
| Símbolos NBR 5444 não disponíveis prontos | Atraso no eixo Símbolos | Partir da coleção aberta QElectroTech + subclasses schemdraw |
| Manter React + FastAPI dobra superfície | Custo operacional | Estrangulamento gradual; só migrar módulo com paridade comprovada |
| Reimplementar o que já funciona em TS | Retrabalho | Portar 1:1 na Fase B; inovar só no greenfield (Fases D–E) |
| Perda de conhecimento embutido nos testes | Regressão silenciosa | Exportar as 11 suítes Vitest como fixtures antes de tocar no cálculo |

---

## 12. Próximos passos (handoff)

- **@architect (Aria):** validar o DAG de pacotes (§2), a fronteira Pint↔NumPy (§4.2) e a DSL intermediária de diagrama (§5.3) — decisões estruturais.
- **@data-engineer (Dara):** desenhar `sie-norms` (esquema das tabelas com `pandera`) e a ponte com o Postgres/Supabase existente.
- **@pm (Morgan):** transformar este plano em épico + stories por pacote (`sie-norms` → `sie-core` → `sie-calc` → …), com os golden tests como critério de aceite de paridade.
- **Eng. eletricista / especialista normativo:** fornecer os dados ausentes (Tabela 001/002, ampacidades, fatores) e validar a biblioteca de símbolos contra a NBR 5444.

> **Nota de integridade (Artigo IV — No Invention):** o estado da origem (o que existe, o que é greenfield) deriva de leitura direta dos arquivos do repositório. As bibliotecas indicadas são recomendações fundamentadas no domínio (engenharia elétrica + auditoria), não decisões fechadas — a escolha final cabe ao @architect e ao responsável técnico.

— Atlas, investigando a verdade 🔎