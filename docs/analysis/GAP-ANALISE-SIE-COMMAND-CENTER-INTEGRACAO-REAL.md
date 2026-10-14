# Gap Analysis — Integração do SIE Command Center a dados/funcionalidades reais

**Autor:** Atlas (`@analyst`)
**Data:** 2026-08-01
**Pedido de origem:** conectar as telas do Command Center (`/sie-command-center-preview`) à lógica de domínio real (cálculo, projetos, Supabase), **sem alterar o design original** — decisão de investir na integração cabe a `@architect` + `@dev`; este documento é o insumo de entrada, não a implementação.
**Escopo:** mapeamento factual mock → real, feito por leitura de código (próprio + agente de exploração), sem invenção de funcionalidade inexistente (Artigo IV da Constitution).

---

## Resumo executivo

O Command Center hoje é uma página **sem contexto de projeto** (`/sie-command-center-preview`, sem `$projetoId`), com 4 arquivos de dados 100% ilustrativos. O sistema real, em paralelo, tem um domínio de cálculo **mais rico e mais rigoroso** que o mock em quase todo ponto — exceto em **2 conceitos que simplesmente não existem** no domínio real (`%` de fluxo concluído, "método de instalação B1") e **1 nomenclatura que diverge** (estado binário conforme/revisar vs. o tri-estado real `OK/ACIMA/PENDENTE`).

A restrição "sem alterar o design original" é cumprível para a maior parte da UI — mas esbarra numa decisão estrutural que **não é de design, é de arquitetura**: o Command Center precisa passar a operar sobre um projeto real (`$projetoId`), o que hoje ele não faz. Essa decisão é o primeiro ponto que `@architect` precisa resolver antes de qualquer wiring.

---

## Restrição de partida: o que "sem alterar o design original" permite e o que não permite

| Permite (é wiring, não é mudança de design) | Não permite sozinho (é decisão de arquitetura/produto) |
|---|---|
| Trocar o `import` de `overview-data.ts`/`parameters-results-data.ts`/`decision-data.ts` por um hook real (`useQuery`) que devolve dado no mesmo formato de props que os organisms já esperam | Inventar contexto de projeto (`$projetoId`) do nada — a rota de preview hoje não tem nenhum |
| Passar dados reais para os mesmos componentes (`EngineeringPanel`, `ContextInspector`, `ParameterPanel`, `ResultSummary`, `DecisionPanel`) sem tocar em CSS/estrutura/props visuais | Manter labels ilustrativos ("Fluxo concluído 72%", "Método B1") quando o dado real não existe ou usa outro vocabulário — isso não é "preservar o design", é inventar dado |
| Reusar `UnifilarPreviewSection` como está — **já é real**, zero trabalho aqui | Decidir sozinho, sem `@po`/`@architect`, como resolver as 3 divergências semânticas da seção seguinte |

---

## Mapeamento peça a peça

### 1. Circuitos (Overview → tabela `EngineeringPanel` + `ContextInspector`)

| Campo da UI (mock) | Equivalente real | Prontidão |
|---|---|---|
| `id`, `aplicacao` | `Circuito.id`/`.nome` (`src/domain/modelo/circuito.ts`) ou `CircuitoParaDimensionamento.descricao` (`src/domain/dimensionamento-condutores/contratos.ts`) | ✅ Wiring direto |
| `corrente` | `Circuito.corrente_projeto_A`, calculado em `src/domain/calculo/corrente-projeto.ts` | ✅ Wiring direto |
| `secao` | **Não é input, é saída** do motor MOD-DC (`ResultadoDimensionamento.secao_fase_mm2`, via `servico-dimensionamento-condutores.ts`) | ✅ Wiring direto, mas requer já ter rodado o dimensionamento |
| `quedaTensao` | `ResultadoInternoQuedaTensao.delta_v_percentual` (`src/domain/queda-tensao/motores/motor-queda-tensao.ts`) | ✅ Wiring direto, com rastreio completo disponível de bônus |
| `fases` | `CircuitoParaDimensionamento.num_fases` / `fases` (`contratos.ts`) | ✅ Wiring direto |
| `comprimento` | `RequisicaoQuedaTensao.comprimento_m` — **dado que só o projetista informa, nunca estimado** | ✅ Wiring direto, mas pode vir vazio (circuito "sem comprimento ainda") |
| `estado` (`conforme`/`revisar`) | `StatusQuedaCircuito = "OK" \| "ACIMA" \| "PENDENTE"` (`servico-queda-tensao.ts`) | ⚠️ **Divergência semântica** — real é tri-estado, mock é binário. `PENDENTE` (sem comprimento informado) não tem lugar no mock atual |

### 2. Métricas do Overview (`MetricCardGrid`)

| Métrica mockada | Equivalente real | Prontidão |
|---|---|---|
| "Circuitos: 15 conformes · 3 requerem revisão" | `ResumoQuedaTensao.total/conformes/acimaDoLimite/semComprimento` (`servico-queda-tensao.ts`, função `resumo()`) | ✅ Wiring direto (com o ajuste do item 1 acima — 3 grupos reais, não 2) |
| "Pior queda: 3,82%" | `ResumoQuedaTensao.piorCircuito`/`pioresCircuitos` | ✅ Wiring direto |
| "Demanda calculada: 19,4 kVA" | `ResultadoDemanda.DT_VA` (`src/domain/distribuidora/edp-sp/motor-demanda.ts`) | ✅ Wiring direto |
| "Fluxo concluído: 72%" | **Não existe.** Busca no domínio inteiro por `progresso`/conclusão percentual não retornou nada | ❌ Sem equivalente — decisão de produto: inventar um cálculo de progresso (novo, fora deste gap analysis) ou remover a métrica |

### 3. Parâmetros e resultado de queda de tensão (`ParameterPanel` + `ResultSummary`)

| Item mockado | Equivalente real | Prontidão |
|---|---|---|
| Tensão nominal, comprimento, corrente de projeto | `RequisicaoQuedaTensao`/`ContextoQuedaTensao` (`src/domain/queda-tensao/contratos.ts`) | ✅ Wiring direto |
| "Método de instalação B1 · eletroduto embutido" | **Não existe.** O domínio real usa `familia_id`/`topologia_coluna_id` do catálogo Prysmian de impedâncias (`impedancias-prysmian-rev10.ts`), não a nomenclatura de métodos B1/B2/C/D/E/F da NBR 5410 | ❌ Sem equivalente direto — vocabulário do mock não é o vocabulário do sistema real |
| Resultado de queda (%, motivo, próxima ação) | `ResultadoInternoQuedaTensao` completo, incluindo `alertas` e `sugestoes` (nunca aplicadas automaticamente) | ✅ Wiring direto — real é mais rico que o mock, inclusive já tem o padrão "motivo + próxima ação" |

### 4. DecisionPanel

| Item mockado | Equivalente real | Prontidão |
|---|---|---|
| Opções "manter seção" vs "aumentar seção", com impactos | `CenarioSimulacao` + `simularCenarios()` (`src/domain/queda-tensao/motores/simulador-cenarios.ts`) | ✅ Wiring direto — real já segue o princípio "sistema sugere, projetista decide" |
| Confirmação da decisão | `servicoQuedaTensao.aplicarCenario()`, que **exige justificativa não vazia** (`AplicacaoCenarioInvalida`) e grava auditoria (`QUEDA_TENSAO_CENARIO_APLICADO`) | ✅ Wiring direto — inclusive mais rigoroso que o mock (mock não pede justificativa) |

### 5. ModuleNavigation

| Item do menu | Rota real | Prontidão |
|---|---|---|
| Ambientes e cargas | `projetos.$projetoId.tsx` | ✅ Existe |
| Padrão de entrada | `projetos.$projetoId_.padrao-entrada.tsx` | ✅ Existe |
| Circuitos | `projetos.$projetoId_.circuitos.tsx` | ✅ Existe |
| Correntes | `projetos.$projetoId_.correntes.tsx` | ✅ Existe |
| Condutores | `projetos.$projetoId_.dimensionamento-condutores.tsx` | ✅ Existe |
| Queda de tensão | `projetos.$projetoId_.queda-tensao.tsx` | ✅ Existe |
| Diagrama unifilar | `projetos.$projetoId_.unifilar.tsx` / `unifilar-diagrama.tsx` | ✅ Existe (e já é o que `UnifilarPreviewSection` embute) |
| **Diagnóstico** | `diagnostico.tsx` | ⚠️ **Existe, mas é outra coisa** — health-check de conexão Supabase, não diagnóstico de conformidade NBR 5410 do projeto. Não há rota real equivalente ao que o menu sugere |
| Visão geral | — | ❌ Não existe como rota própria — é a composição que o próprio Command Center está tentando ser |

### 6. API real já exposta (`src/routes/api/v1/`)

35 rotas HTTP já existem cobrindo dependências, correntes, dimensionamento de condutores (incl. overrides por circuito), queda de tensão (incl. simulação de cenário e aplicação), padrão de entrada, unifilar (capacidades + exportação) e módulos de validação (MOD-CC/MOD-QT/MOD-SEC). A superfície de API para wiring já existe — não é um projeto de backend do zero, é um projeto de troca de fonte de dados no frontend + resolução do contexto de projeto.

---

## O que É verdadeiramente forte neste mapeamento, não apenas alegado

- Para **circuitos, métricas de queda de tensão, demanda, painel de decisão e navegação real** (5 dos 6 blocos analisados), existe equivalente real funcional e a superfície de API HTTP já está pronta — isso é majoritariamente wiring, não é construir motor de cálculo novo.
- A seção Unifilar (`UnifilarPreviewSection`) **já é real** desde `SIE-DS-06` — zero trabalho de integração ali.
- O domínio real de queda de tensão é *mais* rigoroso que o mock (justificativa obrigatória, auditoria, rastreio completo), então a integração tende a *melhorar* a fidelidade da experiência, não simplificá-la.

## O que não tem equivalente real — decisão de produto, não de arquitetura

1. **"Fluxo concluído: 72%"** — conceito inexistente no domínio.
2. **"Método de instalação B1"** — vocabulário inexistente no domínio (que usa catálogo de impedâncias Prysmian).
3. **Estado binário conforme/revisar** — domínio real é tri-estado (`OK`/`ACIMA`/`PENDENTE`).
4. **"Diagnóstico"** no menu sugere avaliação de conformidade do projeto; a rota real com esse nome é apenas health-check de infraestrutura.

Manter esses 4 itens com a redação atual, uma vez conectados a dados reais, seria **reintroduzir invenção** (Artigo IV) sob a aparência de dado real. Alguém — `@po` ou `@architect`, não `@analyst` — precisa decidir: adaptar a redação/estados da UI ao vocabulário real, ou tratar esses 4 pontos como fora de escopo da integração.

## A decisão estrutural que antecede tudo isso

O Command Center, como existe hoje, **não tem noção de projeto**. Toda a integração descrita acima pressupõe resolver primeiro: de onde vem o `$projetoId`? Um seletor de projeto no cabeçalho (`EngineeringShell` já tem um placeholder de seletor, hoje decorativo)? A rota passa a viver sob `/projetos/$projetoId/command-center`? Isso é 100% decisão de `@architect` — nenhuma opção altera o design visual, mas todas alteram a estrutura de rotas/estado, o que está fora do que `@analyst` pode decidir ou até recomendar com segurança.

---

## Recomendação

1. **Handoff para `@architect`**: usar este documento como insumo para desenhar (a) a resolução do contexto de projeto, (b) o mapeamento de hooks reais por componente (tabela acima), (c) uma decisão explícita sobre os 4 itens sem equivalente real.
2. **Não** iniciar wiring componente por componente sem essa decisão estrutural — troca de mock por real, feita antes de resolver o `$projetoId`, geraria um Command Center que funciona só com dado hardcoded de um projeto fixo, o que é pior que o mock atual (parece real, não é).
3. Este documento não substitui uma story formal — é insumo de research/discovery, consistente com `docs/analysis/GAP-ANALISE-SIE-DS-02-vs-PROTOTIPO.md` (mesmo padrão usado nesta cadeia).

---

— Atlas, investigando a verdade 🔎
