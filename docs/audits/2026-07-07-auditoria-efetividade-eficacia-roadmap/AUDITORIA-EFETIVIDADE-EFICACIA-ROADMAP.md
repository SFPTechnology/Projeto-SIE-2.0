# Auditoria de Efetividade e Eficácia — Aplicação Profissional SIE + Roadmap de Próximos Módulos

**Data da auditoria:** 2026-07-07
**Repositório auditado:** `sistema-de-instala-es-el-tricas-sie-main`
**Auditor:** Auditor técnico sênior (engenharia elétrica BT / NBR 5410:2004 + EDP-SP PT.DT.PDN.00068 v09; arquitetura e qualidade de software)
**Natureza:** exclusivamente diagnóstica — nenhum arquivo do repositório foi alterado.

---

## 1. Sumário Executivo

O SIE é um sistema web em **TypeScript full-stack** (TanStack Start/React no frontend, rotas de API server-side, Supabase/PostgreSQL na persistência, domínio puro em `src/domain/`) — **não** FastAPI/Pydantic/SQLAlchemy como o contexto orientativo sugeria. A UI de produção usa **IBM Carbon Design System** (`@carbon/react`), conforme declarado; uma biblioteca shadcn/Radix completa coexiste no repositório como código morto.

Da cadeia funcional declarada — *levantamento de cargas → cálculo de demanda → categoria de padrão de entrada → divisão de circuitos → dimensionamento de condutores → proteção → laudo técnico* — o sistema implementa com qualidade real os **três primeiros elos** e o cálculo de corrente de projeto (IB) com balanceamento de fases. Os elos finais — **divisão de circuitos definitiva, dimensionamento de condutores, proteção por circuito e laudo técnico — não existem**, e o próprio código declara isso de forma honesta (contrato `ERR-DIMENSIONAMENTO-PENDENTE` em `src/domain/servicos/servico-corrente.ts:129-214`; mapeador de circuitos autodeclarado "provisório" em `src/domain/calculo/derivar-circuitos.ts:58-63`).

O ponto mais forte é o **motor EDP-SP** (demanda por grupos a–i, categoria U/D/T, corrente de demanda, subcategoria com disjuntor/condutor de entrada): tabelas 001/002 e 005–015 carregadas de JSON rastreável com `status_verificacao: "VERIFICADO"`, fonte e versão de norma declaradas, validação estrutural em carga e 13 arquivos de teste dedicados. O ponto mais frágil sob a ótica normativa é que **todas as regras NBR de tomadas e iluminação (F-03 a F-09) e todas as tabelas derivadas permanecem com `status_verificacao: "VERIFICAR"`** — o sistema calcula com valores plausíveis, mas não certificados contra o texto integral da NBR 5410:2004.

A suíte de testes é extensa (67 arquivos, **429 testes; 428 passam, 1 falha**). A falha (`src/domain/calculo/quantidade-analise.test.ts:45`) é um defeito real de rastreabilidade: o valor "automático" reportado na análise de TUG é contaminado pelo override manual.

**Veredicto:** no estado atual, o SIE é **apto como ferramenta de cálculo assistido sob revisão integral de engenheiro responsável** para levantamento de cargas e enquadramento EDP-SP, e **inapto para gerar sozinho um projeto submetível à distribuidora ou à fiscalização**, porque não dimensiona condutores, não especifica proteção por circuito e não emite laudo.

| Nota consolidada | Efetividade | Eficácia |
|---|---|---|
| **Escopo implementado** | **6,5 / 10** | **7,0 / 10** |
| **Sistema completo declarado** | **4,0 / 10** | **6,5 / 10** |

---

## 2. Metodologia Aplicada

Toda conclusão está ancorada em evidência de código ou saída de comando reprodutível.

| Passo | Ferramenta/comando | Resultado |
|---|---|---|
| Mapeamento estrutural | `find`/listagem de `src/`, `tests/`, `docs/` | 9 áreas de domínio, 67 arquivos de teste |
| Identificação de stack | `package.json`, `CLAUDE.md`, `vite.config.ts` | TanStack Start + React 19 + Supabase + Carbon |
| Execução da suíte | `npx vitest run` (72,2 s) | 429 testes, 428 pass, **1 fail** |
| Varredura de pendências | `grep -in "TODO\|FIXME\|VERIFICAR\|PENDENTE\|placeholder\|stub"` em `src/` | ~120 ocorrências mapeadas |
| Rastreabilidade normativa | Leitura de todos os `*.data.json` de `src/domain/nbr/` e `src/domain/distribuidora/edp-sp/` | Ver §8 |
| Leitura de código | Read integral dos módulos de cálculo, motor EDP, serviços, contratos, seletores | Ver §4 |
| Uso real de UI library | `grep -rl "@carbon/react"` vs `grep -rl "components/ui/"` em rotas/componentes de app | Carbon em 100% do app; shadcn não referenciado |
| Histórico de defeitos | `docs/qa/` (INC-02…INC-07, P-ACIMTETO, P-CERTFID etc.), `git log` | Processo de QA ativo e documentado |
| Auditoria de dados prévia | `docs/supabase/DB-AUDIT.md` (2026-06-20) | 11 débitos (1 crítico) confirmados por inspeção |

---

## 3. Inventário de Módulos vs. Cadeia Funcional Declarada

| # | Elo da cadeia funcional | Status | Evidência |
|---|---|---|---|
| 1 | Levantamento de cargas (iluminação, TUG, TUE/cargas adicionais, bancadas) | ✅ Implementado | `src/domain/calculo/{iluminacao,tomadas,cargas-adicionais,motor}.ts` |
| 2 | Cálculo de demanda (EDP-SP, grupos a–i) | ✅ Implementado | `src/domain/distribuidora/edp-sp/motor-demanda.ts` |
| 3 | Categoria/subcategoria de padrão de entrada (U/D/T + U2…T10, disjuntor e condutor do ramal) | ✅ Implementado | `seletor-categoria.ts`, `seletor-subcategoria.ts`, catálogo Tabelas 001/002 |
| 4 | Divisão de circuitos | ⚠️ **Provisória** — mapeador 1:1 dependência→circuito, sem regras de agrupamento/limite por circuito | `derivar-circuitos.ts:58` ("Mapeador provisório … enquanto a Divisão de Circuitos ainda não existe") |
| 5 | Corrente de projeto (IB) + balanceamento de fases | ✅ Implementado (etapa intermediária do elo 5) | `corrente-projeto.ts`, `corrente-circuitos.ts`, `balanceamento-fases.ts` |
| 5b | Dimensionamento de condutores (Iz, método de instalação, agrupamento, temperatura, queda de tensão) | ❌ **Não implementado** — bloqueado por contrato explícito | `servico-corrente.ts:129-214` (`ERR-DIMENSIONAMENTO-PENDENTE`) |
| 6 | Proteção por circuito (disjuntores IB≤In≤Iz, I2≤1,45·Iz, DR, DPS) | ❌ Não implementado (apenas disjuntor do **ramal** via subcategoria EDP; exigência de DR aparece só como diagnóstico de conformidade) | `grep "disjuntor" src/domain/calculo` → 0 resultados |
| 7 | Laudo técnico / memorial de cálculo | ❌ Não implementado | `grep -ri "laudo\|memorial" src` → 0 resultados |
| — | Transversal: estados/validação/auditoria (RASCUNHO→CALCULADA→VALIDADA, histórico imutável) | ✅ Implementado | `src/domain/estado/`, `servico-validacao.ts`, `eventos_auditoria` |
| — | Transversal: conformidade NBR 5410 (DR, IP, zonas banheiro/piscina, circuito exclusivo) | ✅ Implementado (como *checklist* declaratório, não como cálculo) | `src/domain/calculo/conformidade-nbr5410.ts` |
| — | Transversal: padrão de entrada genérico NBR (não-EDP) | ⚠️ Placeholder | `catalogo-fornecimento.data.json`, `fatores-demanda.data.json` (todos `VERIFICAR`) |

---

## 4. Avaliação Módulo a Módulo

Escala 0–10. **Efetividade** = cumpre o propósito para uso profissional real no escopo do módulo. **Eficácia** = qualidade/robustez/precisão da implementação.

### M1 — Catálogo normativo NBR (`src/domain/nbr/`)

| Efetividade | Eficácia |
|---|---|
| **7,0** | **6,0** |

- **Escopo:** regras F-01…F-09, tabelas de iluminação/TUG por categoria, tipos de dependência → categoria (CAT-A/B/C), tracker de pendências.
- **Pontos fortes:** arquitetura de rastreabilidade exemplar — cada regra carrega `referencia` (norma+item), `fonte`, `status_verificacao`, `fonte_requerida` e `validador_responsavel` (`catalog.data.json:118-189`); loader valida o catálogo em carga (`catalog.ts`); existe teste que garante que toda pendência gera linha no tracker CSV (`tests/domain/nbr/tracker.test.ts`). Nada é hardcoded no código de cálculo — valores vêm do JSON.
- **Risco central:** **F-03 a F-09 e todas as tabelas T-ILUM/T-TUG estão `VERIFICAR`** (`catalog.data.json:45,54,63,72,81,90,99,113,125,137,150,162,175,185`). A fonte declarada é uma "Especificação Técnica Orientadora — Bloco 1 v13", não o texto integral da NBR 5410. Os valores conferem com a prática usual (100 VA/600 VA, ⌈P/5⌉, ⌈P/3,5⌉, 100+60·⌊(A−6)/4⌋), mas o próprio sistema se declara não-certificado. Uso profissional exige a validação formal já prevista no campo `validador_responsavel`.
- **Risco secundário:** F-04 registra em texto "bancada de cozinha à parte — pendência".

### M2 — Cálculo de cargas por dependência (`src/domain/calculo/{geometria,iluminacao,tomadas,cargas-adicionais,motor}.ts`)

| Efetividade | Eficácia |
|---|---|
| **7,5** | **6,5** |

- **Escopo:** área/perímetro (com perímetro excluído e medidas reais), pontos e carga de iluminação, quantidade e carga de TUG por categoria (com caso especial banheiro), overrides manuais com justificativa obrigatória, análise estruturada com origem AUTOMÁTICA/MANUAL.
- **Pontos fortes:** fórmulas conferem com a regra declarada (ex.: `iluminacao.ts:29-35` implementa exatamente 100 + 60·⌊(A−6)/4⌋ com piso; `tomadas.ts:82-105` implementa 3×600+n×100 para CAT-B). Resultado rastreável cita `formula_nbr`, `referencia_norma`, parâmetros de entrada e calculados.
- **Defeito confirmado (teste falhando):** `calcularTUGAnalise` reporta `carga_automatica_va` contaminada pelo override manual — para sala 5×4 m com override de 5 tomadas, o valor "automático" reportado é 500 VA em vez de 400 VA (`npx vitest run` → `quantidade-analise.test.ts:45`, *expected 400, received 500*). Causa: `calcularTUGAnalise` (`tomadas.ts:136`) obtém `carga_automatica_va` de `cargaTUG(d)`, que internamente usa `quantidadeTUG(d)` — e esta respeita o override (`tomadas.ts:45-50`). O rastreio "valor automático vs. manual" — argumento central de auditabilidade do sistema — fica incorreto sempre que há override.
- **Observação:** quantidade de pontos de iluminação usa heurística 1+⌊(A−6)/4⌋ derivada da tabela de **carga** — a NBR só exige 1 ponto por dependência; a extrapolação de quantidade é decisão de projeto do sistema, corretamente marcada como F-07-QTD, mas herda o `VERIFICAR` de M1.

### M3 — Ciclo de vida, validação e auditoria (`src/domain/estado/`, `servico-validacao.ts`, `servico-recalculo.ts`, `servico-auditoria.ts`)

| Efetividade | Eficácia |
|---|---|
| **8,0** | **8,0** |

- **Escopo:** máquina de estados RASCUNHO→CALCULADA→VALIDADA com recálculo em cascata pós-edição, bloqueio de validação com campos de conformidade pendentes, histórico de edições manuais e log de auditoria imutável.
- **Pontos fortes:** transições testadas (`tests/domain/estado/transicoes.test.ts`, `ciclo-vida.test.ts`, `recalculo-cascata.test.ts`); validação exige resolução de tensão de TUE >600 VA antes de validar (`servico-validacao.ts:37-51`) — correção do incidente INC-04 documentada em `docs/qa/P-INC-04_*`.
- **Risco:** validação é *declaratória* (o engenheiro afirma DR/IP/zonas); o sistema não verifica fisicamente essas exigências — aceitável nesta fase, mas o laudo futuro precisa expor isso.

### M4 — Derivação de circuitos (`derivar-circuitos.ts`, `resolver-ligacao.ts`)

| Efetividade | Eficácia |
|---|---|
| **4,0** | **6,5** |

- **Escopo:** mapeia cada dependência em circuitos ILUM-*/TUG-*/ADD-* determinísticos, resolve tensão por tipo de carga (com fallback 127 V "a confirmar" apenas para TUE ≤600 VA), explode TUEs de circuito exclusivo em N circuitos unitários (NBR §9.5.2.2).
- **Pontos fortes:** honestidade arquitetural — comentário explícito "Mapeador provisório … enquanto a Divisão de Circuitos ainda não existe" (`derivar-circuitos.ts:58`); circuito exclusivo por unidade implementado (`:181-193`); `trifasica` nunca inferida.
- **Riscos para uso real:** (a) **um circuito de TUG por dependência inteira** — sem limite de VA por circuito nem agrupamento racional entre dependências, um apartamento real produz divisão tecnicamente inválida ou antieconômica; (b) iluminação+TUG jamais compartilham circuito nem são verificadas contra os limites de 9.5.3/9.5.4 (seções mínimas por uso são exatamente o elo ausente); (c) a nota de efetividade reflete que este elo declara-se placeholder.

### M5 — Correntes de projeto e balanceamento (`corrente-projeto.ts`, `corrente-circuitos.ts`, `balanceamento-fases.ts`, `servico-corrente.ts`)

| Efetividade | Eficácia |
|---|---|
| **6,0** | **8,5** |

- **Escopo:** IB = S/(fator·V) com fator √3 para trifásico, diagnósticos por circuito (tensão não ofertada, ligação incompatível, IB>63 A), balanceamento LPT determinístico em 3 fases com limite de desequilíbrio 5%, contrato de dimensionamento explicitamente bloqueado.
- **Pontos fortes:** fórmula única correta e defendida por guard clauses (`corrente-projeto.ts:20-34`); comentário tecnicamente correto de que IB trifásico já é corrente de linha e não se divide por fase (`balanceamento-fases.ts:17-23`); o sistema **recusa-se a fingir dimensionamento**: `ERR-DIMENSIONAMENTO-PENDENTE` lista método de instalação, temperatura, agrupamento, comprimento e as verificações IB≤In≤Iz / I2≤1,45·Iz como pré-requisitos pendentes (`servico-corrente.ts:129-214`), e a UI reproduz o aviso (`projetos.$projetoId_.correntes.tsx:609-615`).
- **Risco:** efetividade limitada por definição — entrega IB, não entrega condutor/proteção; profissional que ignorar o aviso da UI pode tratar IB como dimensionamento.

### M6 — Motor EDP-SP (`src/domain/distribuidora/edp-sp/` — 16 módulos + 12 JSONs)

| Efetividade | Eficácia |
|---|---|
| **8,0** | **8,0** |

- **Escopo:** adaptação Projeto NBR → cargas classificadas (grupos a–i, FP por tipo), demanda por grupo (tabela 005 por kW; quantidade; maior/restantes), categoria U/D/T por kW instalado, corrente de demanda por sistema, subcategoria U2…T10 com disjuntor/condutor do ramal (Tabelas 001/002 v09), diagnósticos, contratos de saída A/B, parâmetros com snapshot+override por projeto persistido.
- **Pontos fortes:** melhor rastreabilidade do sistema — catálogo de subcategorias com fonte, URL oficial do PDF, vigência, critério e `status_verificacao: "VERIFICADO"` (`subcategorias-fornecimento.catalogo.data.json:1-9`), validado estruturalmente linha a linha em carga (`subcategorias-fornecimento.ts:91-146`); 13 arquivos de teste dedicados; pipeline de ingestão versionado (`scripts/ingest-edp-tabelas-001-002.mjs`); seleção de subcategoria nunca inventa valor — retorna erro tipado com o maior padrão disponível (`seletor-subcategoria.ts:104-159`); pendências de derivação (tipo de aparelho ausente, suspeita de roteamento p/ grupo i, fase não declarada de motor) viram diagnósticos.
- **Riscos/pontos de atenção:**
  1. **Índice da Tabela 005 em kW vs kVA** — `calcularGrupoA` usa `soma_armazenada_VA/1000` como índice "kW" (`motor-demanda.ts:101-103`). Para cargas do grupo *a* com FP=1 (iluminação/TUG NBR) é numericamente idêntico; para iluminação de descarga (FP 0,55) roteada ao grupo *a*, o índice ficaria em kVA, deslocando a faixa de FD. `[VERIFICAR]` contra o critério de indexação da Tabela 005 da EDP (kW instalado vs kVA).
  2. Campo `p_nominal_W` armazena **VA** por contrato documentado (`motor-demanda.ts:16-17`) — consistente em todo o fluxo, mas o nome do campo é armadilha de manutenção.
  3. Histórico de incidentes (INC-02 forno/fogão, INC-05 exaustor, FP fluorescente) mostra que a taxonomia de tipos ainda estabiliza; processo de QA em `docs/qa/` está reagindo bem.
  4. `docs/qa/P-CERTFID_Certificar_Valores_Tabelas_EDP.md` indica certificação valor-a-valor das tabelas ainda em processo.

### M7 — Padrão de entrada genérico NBR (`catalogo-fornecimento.*`, `fatores-demanda.*`, `padrao-entrada.ts`)

| Efetividade | Eficácia |
|---|---|
| **3,0** | **4,0** |

- **Escopo:** fluxo alternativo de padrão de entrada para distribuidora genérica.
- **Evidência:** todas as 4 entradas do catálogo têm `"referencia": "VERIFICAR"`; fatores de demanda genéricos declaram-se "placeholder genérico; VERIFICAR contra norma da distribuidora local" (`fatores-demanda.data.json:2-5`).
- **Risco:** se exposto a usuário sem o aviso adequado, produz enquadramento sem base normativa. Corretamente marcado, mas é o único caminho para projetos fora da área EDP-SP — hoje inexistente na prática.

### M8 — Persistência, API e infraestrutura (`src/infra/`, `src/routes/api/v1/`, `src/api/schemas/`, `docs/supabase/`)

| Efetividade | Eficácia |
|---|---|
| **6,0** | **5,0** |

- **Escopo:** repositórios memória/Supabase intercambiáveis, 8 tabelas relacionais, mapeadores snake↔camel testados, schemas Zod nas bordas, log de auditoria.
- **Pontos fortes:** arquitetura hexagonal limpa; testes de isolamento por projeto e de mapeadores; validação Zod em todas as rotas.
- **Riscos (confirmando `docs/supabase/DB-AUDIT.md`, 11 débitos):** migrations manuais sem versionamento (DB-01, crítico); **ausência de CHECK constraints** — domínio validado só na borda Zod, e o acesso SSR usa `service_role` que bypassa RLS (DB-02); escrita do agregado **sem transação** (pai+4 filhas em chamadas separadas — risco de agregado parcial); no modo SPA o `CLAUDE.md` orienta política RLS `anon FOR ALL USING (true)` — em produção multiusuário isso é dado público de leitura/escrita. Para ferramenta single-tenant de engenheiro, tolerável; para SaaS, bloqueante.

### M9 — Frontend / UI (`src/routes/*.tsx`, `src/components/app/`)

| Efetividade | Eficácia |
|---|---|
| **7,0** | **6,5** |

- **Escopo:** 5 páginas (projetos, dependências, correntes, padrão de entrada, diagnóstico), modais de CRUD com justificativa para overrides, cards EDP (demanda por grupo com drill-down, categoria/subcategoria, diagnósticos, editor de parâmetros), componente `ValorRastreavel` que expõe fórmula/fonte/status de verificação por valor.
- **Pontos fortes:** 100% dos componentes de aplicação usam `@carbon/react` (grep: 20+ arquivos; nenhuma rota importa `components/ui/`); rastreabilidade normativa chega ao usuário — badge "Pendente — [VERIFICAR]" renderizada quando a regra não está certificada (`formatters.ts:15`, `correntes.tsx:1493`); pendências de dimensionamento comunicadas em tela.
- **Riscos:** auditoria própria de acessibilidade (2026-07-05, `docs/ACCESSIBILITY-AUDIT.md`) aponta correções pendentes de contraste/ARIA — WCAG 2.1 AA não plenamente atingido; ~45 componentes shadcn/Radix + Tailwind como código morto no bundle-source (risco de manutenção e de importação acidental fora do design system); página `/correntes` com 1.700+ linhas em arquivo único.

---

## 5. Nota Consolidada

| Dimensão | Escopo implementado | Sistema completo declarado | Racional |
|---|---|---|---|
| **Efetividade** | **6,5** | **4,0** | Elos 1–3 e IB funcionam para uso assistido; elos 4–7 (divisão real, condutores, proteção, laudo) ausentes — nenhum projeto sai "pronto para protocolo". |
| **Eficácia** | **7,0** | **6,5** | O que existe é bem construído (dados rastreáveis, 429 testes, diagnósticos honestos), com descontos por: 1 teste falhando (rastreabilidade TUG), regras NBR não certificadas, débitos de persistência. |

---

## 6. Riscos Consolidados para Uso Profissional Real

Ordenado por severidade — o que **hoje impediria** submeter um projeto à distribuidora/fiscalização apoiado apenas no SIE:

| # | Risco | Severidade | Evidência |
|---|---|---|---|
| R1 | **Sem dimensionamento de condutores nem proteção por circuito** — o coração normativo do projeto (IB≤In≤Iz, I2≤1,45·Iz, queda de tensão, seções mínimas) não existe; qualquer projeto exige cálculo externo | Crítica | `servico-corrente.ts:129-214`; grep "disjuntor" em `domain/calculo` = 0 |
| R2 | **Sem laudo/memorial** — não há artefato de saída submetível | Crítica | grep "laudo\|memorial" em `src` = 0 |
| R3 | **Divisão de circuitos provisória** — 1 circuito TUG por dependência, sem limites por circuito; resultado não é uma divisão de circuitos de projeto real | Alta | `derivar-circuitos.ts:58-63` |
| R4 | **Regras NBR F-03…F-09 e tabelas associadas não certificadas** (`VERIFICAR`) — base de cargas mínimas sem validação formal contra o texto da norma | Alta | `catalog.data.json` (14 entradas `VERIFICAR`) |
| R5 | **Rastreabilidade de override defeituosa** — `carga_automatica_va` contaminada pelo valor manual (teste falhando); compromete a trilha de auditoria que diferencia valor normativo de decisão do projetista | Alta | `quantidade-analise.test.ts:45` (fail reproduzido) |
| R6 | **Persistência sem garantias de integridade** — migrations manuais, sem CHECK constraints, escrita de agregado sem transação, RLS permissiva no modo SPA | Alta (para produção) | `docs/supabase/DB-AUDIT.md` DB-01…DB-05 |
| R7 | **Indexação kW/kVA da Tabela 005** para cargas de FP<1 no grupo *a* — possível deslocamento de faixa de FD | Média | `motor-demanda.ts:101-103` `[VERIFICAR]` |
| R8 | Certificação valor-a-valor das tabelas EDP em andamento (P-CERTFID) — resíduo de risco até conclusão | Média | `docs/qa/P-CERTFID_*.md` |
| R9 | Acessibilidade WCAG 2.1 AA incompleta; código morto shadcn no repositório | Baixa | `docs/ACCESSIBILITY-AUDIT.md`; grep `components/ui/` |

---

## 7. Roadmap Sugerido de Próximos Módulos

Priorizado por criticidade para a validade técnico-normativa do projeto final. Sem detalhamento de implementação (conforme instrução).

| Prioridade | Módulo | Justificativa técnica | Por que nesta posição |
|---|---|---|---|
| **P0** | **Divisão de Circuitos definitiva (NBR 5410 §9.5.3)** | Substituir o mapeador provisório por divisão real: separação iluminação/TUG/TUE, limites de carga por circuito, agrupamento entre dependências, numeração de quadro | É pré-requisito estrutural dos módulos seguintes — dimensionar condutores sobre circuitos provisórios produziria resultados descartáveis; o próprio código aponta este elo como o placeholder |
| **P0 (paralelo)** | **Certificação normativa do catálogo NBR** (resolver todos os `VERIFICAR` F-03…F-09/T-*) | Validação formal contra o texto da NBR 5410:2004 pelo responsável técnico já previsto no campo `validador_responsavel`; inclui decidir a pendência "bancada de cozinha" de F-04 | Não bloqueia código, mas bloqueia **confiança**: todo módulo a jusante herda a incerteza; é trabalho de dados/validação paralelizável com P0 |
| **P1** | **Dimensionamento de condutores** (capacidade de condução por método de instalação, correções de temperatura e agrupamento, queda de tensão, seções mínimas §6.2.6) | Elo 5b da cadeia; os pré-requisitos já estão enumerados pelo contrato `ERR-DIMENSIONAMENTO-PENDENTE` — o sistema foi desenhado esperando este módulo | Depende de P0 (circuitos definitivos com comprimento/método por circuito); destrava a verificação IB≤Iz |
| **P1.5** | **Proteção por circuito** (disjuntores IB≤In≤Iz e I2≤1,45·Iz, DR 30 mA §5.1.3.2.2, coordenação, DPS) | Completa o elo 6; transforma os diagnósticos declaratórios de DR em verificação efetiva | Depende de Iz do P1 por definição das duas desigualdades |
| **P2** | **Laudo técnico / memorial de cálculo** (documento submetível: cargas, demanda, categoria, circuitos, condutores, proteções, com trilha de fórmulas/fontes por valor) | Entregável final da cadeia; o modelo `ValorRastreavel` e os contratos A/B já fornecem a matéria-prima de rastreabilidade | Só faz sentido com elos 4–6 completos; emitir laudo antes seria formalizar um projeto incompleto |
| **P2 (paralelo)** | **Hardening de persistência e segurança** (migrations versionadas, CHECK constraints, transação/RPC no agregado, RLS real por usuário) | Resolve DB-01…DB-05; condição de produção multiusuário | Não bloqueia engenharia, bloqueia **operação**; deve concluir antes do primeiro uso comercial |
| **P3** | **Correção da rastreabilidade de overrides + estabilização da taxonomia EDP** (defeito do teste falhando; conclusão P-CERTFID) | Débito de qualidade pontual mas com peso desproporcional na credibilidade da auditoria de valores | Pequeno; pode ser absorvido em qualquer sprint — listado para não se perder |
| **P4** | **Padrão de entrada multi-distribuidora** (substituir placeholders genéricos por catálogos reais de outras concessionárias) | Expande mercado além da área EDP-SP | Só após a cadeia EDP-SP completa provar o modelo ponta a ponta |

---

## 8. Lacunas Normativas Pendentes (`[VERIFICAR]`)

Consolidação de todos os pontos não confirmáveis encontrados:

| # | Item | Local | Natureza |
|---|---|---|---|
| 1 | F-03 — tomadas CAT-A (⌈P/5⌉, 100 VA) | `catalog.data.json:45` | Regra NBR não certificada contra texto integral (9.5.2.2.1.c) |
| 2 | F-04 — tomadas CAT-B (⌈P/3,5⌉, 3×600+100 VA) + pendência "bancada de cozinha à parte" | `catalog.data.json:54` | Idem (9.5.2.2.1.a) |
| 3 | F-05 — banheiro 1 ponto 600 VA | `catalog.data.json:63` | Idem (9.5.2.2.1.b) |
| 4 | F-06 — CAT-C (A>6 m² → ⌈P/5⌉; senão 1 ponto) | `catalog.data.json:72` | Idem (9.5.2.2.1.d) |
| 5 | F-07 — 1 ponto de luz fixo no teto | `catalog.data.json:81` | Idem (9.5.2.1.2) |
| 6 | F-08 — carga mínima iluminação 100+60·⌊(A−6)/4⌋ | `catalog.data.json:90` | Idem (9.5.2.1.2) |
| 7 | F-09 — áreas externas sem mínimo normativo; DR obrigatório | `catalog.data.json:99` | Idem (nota de 9.5.2.2.1) |
| 8 | T-ILUM-CARGA, T-TUG-QTD/CAT-A/B/C, T-TUG-CARGA/CAT-A/B/C (7 tabelas) | `catalog.data.json:103-190` | Tabelas derivadas das regras acima, mesmas fontes requeridas |
| 9 | Fatores de demanda genéricos (iluminação/TUG 0,86; TUE 1,0) | `nbr/fatores-demanda.data.json:2-5` | Placeholder autodeclarado — sem norma de origem |
| 10 | Catálogo genérico de padrões de entrada (4 entradas, `referencia: "VERIFICAR"`) | `nbr/catalogo-fornecimento.data.json` | Limites sem norma de distribuidora |
| 11 | Indexação da Tabela 005 EDP: kW instalado vs kVA para cargas FP<1 no grupo *a* | `motor-demanda.ts:101-103` | Interpretação da PT.DT.PDN.00068 v09 a confirmar |
| 12 | FP default de fluorescente T5 = 0,55 (observação registra que T5 com correção atinge 0,90–0,95 mediante declaração) | `fatores-potencia.data.json` (entrada `iluminacao_fluorescente_t5`) | Interpretação EDP v09 a confirmar |
| 13 | Certificação valor-a-valor das Tabelas 001/002 ingeridas (processo P-CERTFID em aberto) | `docs/qa/P-CERTFID_*.md` | Verificação de dados em andamento |
| 14 | Quantidade de pontos de iluminação por área (F-07-QTD, 1+⌊(A−6)/4⌋) — extrapolação de projeto, não exigência literal da NBR | `iluminacao.ts:60-70` | Decisão de engenharia a homologar pelo RT |

---

## 9. Anexos

### 9.1 Comandos executados (evidência reprodutível)

```
find src tests -type f                          # inventário (67 test files, ~180 fontes)
npx vitest run                                   # 429 testes: 428 pass, 1 fail (72,2 s)
grep -in "TODO|FIXME|VERIFICAR|PENDENTE|placeholder|stub" src/   # ~120 ocorrências
grep -rl "@carbon/react" src                     # 20+ componentes de app (100% do app)
grep -rl "components/ui/" src/routes src/components/app          # 0 (shadcn = código morto)
grep -ri "laudo|memorial" src                    # 0 (sem módulo de laudo)
grep -rn "disjuntor" src/domain/calculo          # 0 (sem proteção por circuito)
git log --oneline -8                             # atividade recente: UI/UX fixes (jul/2026)
```

### 9.2 Principais arquivos inspecionados (leitura integral ou dirigida)

`REFERENCIA-INTEGRAL-SISTEMA.md`, `CLAUDE.md`, `package.json`, `src/domain/nbr/{catalog.data.json,catalog.ts,types.ts,fatores-demanda.data.json,catalogo-fornecimento.data.json}`, `src/domain/calculo/{iluminacao,tomadas,derivar-circuitos,corrente-projeto,corrente-circuitos,balanceamento-fases,conformidade-nbr5410}.ts`, `src/domain/calculo/quantidade-analise.test.ts`, `src/domain/distribuidora/edp-sp/{motor-edp-sp,motor-demanda,seletor-subcategoria,subcategorias-fornecimento,adaptador-projeto,contratos}.ts` + 12 `*.data.json`, `src/domain/servicos/{servico-corrente,servico-validacao,servico-recalculo}.ts`, `src/routes/projetos.$projetoId_.correntes.tsx`, `src/lib/formatters.ts`, `docs/supabase/DB-AUDIT.md`, `docs/ACCESSIBILITY-AUDIT.md`, `docs/qa/*` (índice), `scripts/` (índice).

### 9.3 Divergências entre contexto orientativo e realidade verificada

| Contexto orientativo | Realidade verificada |
|---|---|
| Backend FastAPI + Pydantic v2 + SQLAlchemy 2.x | TypeScript full-stack: TanStack Start (rotas API server-side) + Zod + Supabase (PostgREST) |
| "Frontend React + IBM Carbon" | Confirmado (Carbon em 100% do app); biblioteca shadcn/Radix presente porém não utilizada |
| "Toda configuração normativa carregada como dado rastreável, nunca hardcoded" | Confirmado no essencial: valores normativos vêm de `*.data.json` com fonte/status; nenhum valor de norma hardcoded encontrado nos módulos de cálculo |

---

*Relatório gerado por auditoria diagnóstica em 2026-07-07. Nenhum arquivo do repositório auditado foi modificado.*
