---
executor: "@dev"
quality_gate: "@qa"
quality_gate_tools: [unit_test, api_contract_test, regression_test, static_data_integrity_test]
---

# Story MOD-QT-2-03: Catálogo Fechado de Impedância e Resolvedor de Perfil (VER-QT-02/03/04)

## Status

**Done**

> Gate de @qa (Quinn) em 2026-07-29 — veredito **CONCERNS**, quality score **92**. Transição `InReview → Done` conforme `.claude/rules/story-lifecycle.md` Fase 4. Ver seção "QA Results" ao final.

> Validada por @po (Pax) em 2026-07-28 — veredito **GO**, nota **9/10** (pré-correções: 7/10). Transição `Draft → Ready` conforme `.claude/rules/story-lifecycle.md` Fase 2. Ver seção "Validação de @po" ao final.

> Criada por @sm (River) em 2026-07-28, a partir do parecer decisório `docs/research/{2026-07-28}-resolucao-ver-qt.md` §6 (C-01, C-02, C-04, C-07, C-08). Esta story implementa a resolução definitiva de VER-QT-02, VER-QT-03 e VER-QT-04, substituindo a tabela de impedância provisória `[VERIFICAR]` por um catálogo fechado extraído da fonte primária.

## Fonte normativa e escopo

**Documento-fonte primário desta rodada:** `docs/research/{2026-07-28}-resolucao-ver-qt.md` (parecer, revisão 2, 2026-07-28). Toda referência `§N` sem outra indicação aponta para este parecer. É a fonte decisória — resolve o que os documentos anteriores (`PROMPT-QUEDA-TENSAO-v2.2.md`) deixaram `[VERIFICAR]`.

**Documento de suporte (evidência de extração):** `docs/research/2026-07-28-resolucao-ver-qt/RELATORIO-EXTRACAO-IMPEDANCIA.md` (relatório do @analyst). Referências `Relatório §N` apontam para ele.

**Artefato de dados já extraído (fonte dos registros):** `docs/research/2026-07-28-resolucao-ver-qt/impedancia-prysmian.json` — 1.563 registros, 0 anomalias, 24 células `null`. Estrutura: `fonte`, `inventario`, `anomalias`, `registros[]` (campos: `fonte_id, tabela, pagina_impressa, pagina_pdf, familia_literal, metal, bloco_ordinal, coluna_ordinal, topologia_coluna_id, secao_mm2, r_ca_ohm_km, x_l_ohm_km, frequencia_hz, topologia_descricao, temperatura_operacao_c, nota_restricao`), `ancora_tabela_18_rdc20_classe2`, `testes_coerencia`, `comparacao_valores_provisorios`, `topologias`.

**Plano de execução:** `docs/PLANO-YOLO-IMPLEMENTACAO-MOD-QT-2.md` — esta story reabre os Pacotes 2 e 4 (antes bloqueados por ausência de fonte externa), agora desbloqueados pela extração registrada no relatório.

**Stories predecessoras:** `docs/stories/story-MOD-QT-2-01-motor-calculo-queda-tensao.md` (Status: `InReview`) e `docs/stories/story-MOD-QT-2-02-simulador-endpoints-ui.md` (Status: `InReview`). Esta story substitui a tabela provisória entregue por `MOD-QT-2-01` (`src/domain/queda-tensao/normativa/tabela-impedancia.ts`, todos os registros `status_verificacao: '[VERIFICAR]'`) e o comportamento do fator bifásico (`motores/motor-queda-tensao.ts`), consumidos por `MOD-QT-2-02` (UI/endpoints) sem reimplementação do motor. As pendências técnicas PT-04 e PT-06 da story `MOD-QT-2-01` são fechadas por esta story.

## Escopo desta story (parecer §6)

| Item do parecer | Pendência resolvida | Nesta story |
|---|---|---|
| **C-01** | VER-QT-02, VER-QT-03 | Criar o catálogo estático integral |
| **C-02** | VER-QT-02, VER-QT-03 | Criar `resolverPerfilImpedancia()` e integrar ao motor |
| **C-04** | VER-QT-04 | Corrigir fórmula/fonte do bifásico |
| **C-07** | VER-QT-02, VER-QT-03, VER-QT-04, VER-QT-07 | Regenerar CA-QT-19 com oracle independente |
| **C-08** | — | Testes obrigatórios de completude do catálogo |

**Fora desta story:** C-03, C-05, C-06 (fluxo de entrada fechado, limite EDP-SP, UI de tomadas) — cobertos por `docs/stories/story-MOD-QT-2-04-fluxo-entrada-fechado-limites-edp.md`, que **depende desta story** (o formulário fechado de C-03 só pode listar combinações existentes no catálogo entregue aqui).

## Contrato público — INALTERÁVEL

Esta story **não altera** nenhum dos quatro artefatos abaixo (herdado sem exceção de `MOD-QT-2-01`/`MOD-QT-2-02`):

1. A interface `RetornoMODQT` — `src/domain/dimensionamento-condutores/contratos.ts`, linhas 50–56.
2. O schema Zod `ValidarMODQTSchema` — `src/api/schemas/otimizar-condutor.schema.ts`, linhas 86–93.
3. O schema Zod `RetornoMODQTSchema` — `src/api/schemas/otimizar-condutor.schema.ts`, linhas 74–80.
4. A rota `POST /api/v1/modulos/mod-qt/validar` — `src/routes/api/v1/modulos.mod-qt.validar.ts`.

Verificação por **símbolo**, não por status `M` de arquivo (o critério de precisão registrado pelo @po em `MOD-QT-2-01` DoD item 4 permanece válido — a worktree pode continuar suja com trabalho de outros épicos). Qualquer diff que toque byte a byte um desses quatro símbolos é bloqueio automático de QA.

## Story

**As a** engenheiro eletricista usando o SIE,
**I want** que o motor de queda de tensão use resistência (`Rca`) e reatância (`XL`) reais, publicadas por seção, família de cabo e topologia de instalação — em vez de uma tabela provisória `[VERIFICAR]` sem fonte confirmada —,
**so that** o cálculo de queda de tensão seja tecnicamente defensável perante o engenheiro responsável, sem resistência genérica, sem `XL = 0`, sem interpolação e sem promover valor não publicado a resultado técnico.

## Acceptance Criteria

Todo AC abaixo é rastreável a uma seção numerada do parecer (`§N`) ou do relatório (`Relatório §N`) — Artigo IV, sem invenção.

### AC1 (parecer §6 C-01, §3.1) — Catálogo estático integral, sem tabela genérica
```gherkin
Given as tabelas 28 a 36 da fonte primária [F4] (parecer §2, Relatório §2 "Inventário extraído")
When o catálogo `impedancias-prysmian-rev10.ts`/`.json` é carregado
Then contém exatamente 1.563 registros, cobrindo as 9 tabelas (28, 29, 30, 31, 32, 33, 34, 35, 36)
And nenhum registro é produzido por `TABELA_CU`/`TABELA_AL` genérica, valor padrão, arredondamento de célula, interpolação ou geração de linha ausente (parecer §6 C-01, "Proibições de implementação")
```

### AC2 (parecer §3.1, §6 C-01) — Células não publicadas nunca são zero
```gherkin
Given as 24 células não publicadas identificadas na extração (Relatório §2, "Total: 1.563 células... Células não publicadas: 24")
When o catálogo é inspecionado
Then essas 24 células são representadas como `null`
And nenhuma delas é representada como `0`, aproximação ou valor derivado
```

### AC3 (parecer §3.1, "Campo") — Cada registro carrega a chave fechada completa
```gherkin
Given qualquer registro do catálogo
When seus campos são inspecionados
Then contém, sem campo opcional ausente: fonte_id, tabela_origem (28-36), familia_grupo_id, metal (CU/AL), temperatura_operacao_c (70/90), secao_mm2, topologia_coluna_id, r_ca_ohm_km, x_l_ohm_km, frequencia_hz (60), pagina_origem, versao_fonte, fonte_url, fonte_sha256, nota_restricao
```

> **[PO] Mapeamento de nomes — obrigatório e verificado contra o artefato real.** Os nomes exigidos pelo parecer §3.1 **não** são os nomes gravados em `impedancia-prysmian.json` (verificado por @po em 2026-07-28). O mapeamento abaixo é **renomeação de campo, não transformação de valor** — nenhum valor de `Rca`/`XL` pode ser alterado (parecer §6 C-01, "Proibições de implementação"):
>
> | Campo exigido (parecer §3.1) | Origem real no artefato |
> |---|---|
> | `tabela_origem` | `registros[].tabela` |
> | `familia_grupo_id` | `registros[].familia_literal` (ver decisão PO-02 abaixo) |
> | `pagina_origem` | `registros[].pagina_impressa` (+ `pagina_pdf` preservado) |
> | `versao_fonte` | **não existe no registro** — deriva de `fonte` + decisão PO-01 abaixo |
> | `fonte_url`, `fonte_sha256` | `fonte.url`, `fonte.sha256_pdf` (bloco `fonte`, não `registros[]`) |
> | `fonte_id` | `registros[].fonte_id` (`PRYSMIAN_BT_GUIA`) — **remapeado** conforme decisão PO-01 |
>
> Campos do artefato sem equivalente no parecer (`bloco_ordinal`, `coluna_ordinal`, `topologia_descricao`, `pagina_pdf`, `nota_restricao`) são **preservados**, não descartados.

### AC4 (parecer §6 C-01, "Fonte a gravar") — Citação de fonte por registro
```gherkin
Given qualquer registro do catálogo
When o campo de rastreabilidade é inspecionado
Then contém tabela, página, família e perfil suficientes para reproduzir a citação do parecer §6 C-01:
     "Prysmian Brasil, Guia de Dimensionamento de Cabos para Baixa Tensão, Rev. 10, Tabela {tabela}, p. {pagina}, Rca/XL a 60 Hz, perfil {perfil_id}, acesso 2026-07-28"
```

### AC5 (parecer §3.2, §6 C-02) — `resolverPerfilImpedancia()` seleciona exatamente um registro
```gherkin
Given os cinco campos controlados da seção 3.2 do parecer (familia_id, metal, secao_mm2, quantidade_de_condutores_carregados, topologia_coluna_id)
When resolverPerfilImpedancia() é chamado com uma chave que corresponde a exatamente um registro do catálogo
Then retorna esse registro único, com r_ca_ohm_km e x_l_ohm_km pareados
And a chave de BUSCA no catálogo é (familia_grupo_id, secao_mm2, topologia_coluna_id) — verificada por @po como suficiente e unívoca: 1.563 chaves distintas para 1.563 registros
And `metal` é validado por coerência com o registro resolvido, não usado como filtro adicional (é determinado pela família — parecer §3.1, coluna "Metal")
And `quantidade_de_condutores_carregados` é validado por COERÊNCIA com topologia_coluna_id (2_* e CABO_BIPOLAR → 2; 3_* e CABO_TRIPOLAR → 3), NUNCA usado como filtro de coluna do catálogo
```

> **[PO] Correção de precisão — `quantidade_de_condutores_carregados` não é campo do catálogo.** O Relatório §5.5 registra explicitamente que a hipótese de mapear os dois blocos das tabelas a "2 vs 3 condutores carregados" foi **testada e descartada por evidência**: a divisão em blocos é de layout de página. Verificado por @po: os 16 campos de `registros[]` não incluem esse campo. Usá-lo como filtro do catálogo retornaria **0 registros sempre**, disparando a rejeição do AC6 em toda chamada. Ele permanece como o quinto campo controlado de ENTRADA (parecer §3.2), com função de validação de coerência — divergência entre ele e `topologia_coluna_id` é rejeição pelo mesmo mecanismo do AC6.

### AC6 (parecer §3.2, §6 C-02) — Falha determinística antes do motor, sem resultado técnico
```gherkin
Given uma chave sem correspondência (0 registros) ou, por erro de dado, mais de um registro
When resolverPerfilImpedancia() é chamado
Then a classe de erro já existente `ErroQuedaTensao` de src/domain/queda-tensao/erros.ts é usada, com um novo valor de `CodigoErroQuedaTensao` (a união de códigos é interna e extensível; a CLASSE e sua forma permanecem inalteradas — verificado por @po: erros.ts hoje tem 4 códigos, nenhum para perfil não resolvido)
And a falha ocorre ANTES da montagem de RetornoMODQT
And a saída não carrega [VERIFICAR], não usa XL = 0 e não gera memorial, quadro de cargas ou aprovação de projeto
```

### AC7 (parecer §3.2, §6 C-02) — Motor consome exclusivamente o catálogo fechado
```gherkin
Given uma chamada válida ao motor de cálculo com os cinco campos controlados
When calcularQuedaTensao() executa
Then o valor de Rca/XL usado vem exclusivamente de resolverPerfilImpedancia()
And a tabela provisória `normativa/tabela-impedancia.ts` (status_verificacao = "[VERIFICAR]") deixa de ser consultada no caminho de produção
```

### AC8 (parecer §3.3, §6 C-04) — Fator 2 para bifásico fase-fase, tensão fase-fase
```gherkin
Given um circuito com ContextoQuedaTensao.num_fases === 2 (tipo NumeroFasesQT, src/domain/queda-tensao/contratos.ts:17)
When o motor calcula a queda de tensão
Then fatorPorNumeroDeFases(2) retorna 2 (comportamento atual, motor-queda-tensao.ts:75-79 — CONFIRMADO, não alterado)
And o comentário de justificativa em motor-queda-tensao.ts:71-73 ("fator correto NÃO foi confirmado em nenhuma fonte") é substituído pela citação do parecer §3.3 / [F4] §6.2
And o alerta "[VERIFICAR — VER-QT-04]" emitido em motor-queda-tensao.ts:250-253 deixa de ser emitido (parecer §6 C-04, "retirar exclusivamente a marcação VER-QT-04")
And V_nominal usado é validado como tensão fase-fase (parecer §3.3, "Em circuito bifásico, Vnominal é necessariamente a tensão fase-fase")
```

> **[PO] Correção de precisão — o símbolo `BIFASICO_FASE_FASE_SEM_NEUTRO` NÃO existe no código.** Verificado por @po em 2026-07-28 (`grep -rn "BIFASICO_FASE_FASE_SEM_NEUTRO" src/ tests/` → 0 ocorrências). A representação real do circuito bifásico é `num_fases: 2` do tipo `NumeroFasesQT = 1 | 2 | 3`. **@dev não deve criar esse enum**: criá-lo alteraria a forma de `ContextoQuedaTensao` sem necessidade e não está em C-04 (cujo arquivo alvo é apenas `motor-queda-tensao.ts`). A mudança material de C-04 é **retirar a marcação e corrigir a fonte**, não mudar o fator (que já é 2).

### AC9 (parecer §6 C-07) — CA-QT-19 regenerado com oracle independente do mock
```gherkin
Given a grade de 504 vetores de tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts, GERADA EM RUNTIME pelo produto cartesiano correntes[8] × comprimentos[9] × secoes[7] = 504 (não é um array literal de fixtures)
When o teste é regenerado conforme o parecer §6 C-07
Then a grade permanece com exatamente as mesmas 8 correntes, 9 comprimentos e 7 seções (nenhum vetor adicionado ou removido — parecer §6 C-07, "manter os 504 vetores existentes")
And cada vetor elegível recebe um perfil_id do catálogo, derivado do perfil de fixture declarado (ver decisão PO-02)
And o oracle do teste lê o JSON bruto do catálogo e aplica diretamente a fórmula confirmada (parecer §3.3), sem depender de valor pré-calculado nem reimportar motor-queda-tensao.ts
And a razão motor/mock deixa de ser critério de aprovação, sendo emitida apenas como diagnóstico legado calculado em runtime
```

> **[PO] Correção de precisão — não existe fixture de 504 vetores.** Verificado por @po em 2026-07-28: o arquivo tem 152 linhas e **zero** ocorrências do literal `504`. Os 504 vetores são o produto cartesiano de três arrays declarados dentro de dois blocos `it()` (linhas 73-75 e 116-118): `correntes` (8) × `comprimentos` (9) × `secoes` (7) = 504. A instrução original "adicionar `perfil_id` a cada um dos 504 vetores existentes" **não é executável como escrita** — não há lista para anotar. O que @dev deve fazer é **extrair a grade para uma única constante compartilhada** e resolver o `perfil_id` por vetor a partir do perfil de fixture. As 7 seções da grade (1,5 / 2,5 / 4 / 6 / 10 / 16 / 25 mm²) existem todas no catálogo para a família de fixture — nenhum vetor da grade é inelegível por seção, logo os testes negativos do AC10 exigem vetores **adicionais** construídos para esse fim.

### AC10 (parecer §6 C-07, "Casos sem perfil") — Testes negativos do CA-QT-19
```gherkin
Given vetores do CA-QT-19 que não possuem perfil correspondente no catálogo
When o teste roda
Then o motor retorna o erro interno esperado (AC6) antes de qualquer resultado de queda de tensão
And o gate CA-QT-19 só é APROVADO se todos os vetores elegíveis coincidirem com o oracle, todos os inelegíveis forem rejeitados, e não existir "[VERIFICAR]" em saída aprovada (parecer §6 C-07, "Gate CA-QT-19")
```

### AC11 (Relatório §2, "Total: 1.563 células") — Teste de completude por fonte/tabela
```gherkin
Given o catálogo carregado
When o teste de completude executa
Then confirma a presença de todas as 9 tabelas: 28, 29, 30, 31, 32, 33, 34, 35 e 36 (parecer §6 C-08, "Teste de fonte")
```

### AC12 (parecer §6 C-08, "Teste de chave") — Unicidade de perfil_id e pareamento Rca+XL
```gherkin
Given o catálogo carregado
When o teste de chave executa
Then confirma que não há dois registros com o mesmo perfil_id (parecer §3.2: perfil_id = PRYSMIAN_BT_REV10 + tabela_origem + familia_grupo_id + metal + secao_mm2 + topologia_coluna_id)
And o perfil_id é composto com familia_grupo_id (o rótulo literal da tabela), NUNCA com o familia_id comercial selecionado pelo usuário — do contrário duas famílias comerciais que compartilham a mesma célula publicada gerariam perfil_id duplicado para o mesmo registro (ver decisão PO-02)
And confirma que todo registro com r_ca_ohm_km não nulo também define x_l_ohm_km (ou ambos nulos, nunca um sem o outro, exceto pelas 24 células não publicadas documentadas em AC2)
```

### AC13 (parecer §6 C-08, "Teste de rastreabilidade") — URL, revisão, tabela e página
```gherkin
Given qualquer registro do catálogo
When o teste de rastreabilidade executa
Then confirma a presença de URL da fonte, identificador de revisão, tabela de origem e página de origem
```

### AC14 (parecer §6 C-08, "Teste negativo") — Domínio calculável explícito
```gherkin
Given as entradas: produto/texto livre, seção ausente, topologia ausente, célula vazia (null, ver AC2), tabela inexistente e conduto metálico fechado ferromagnético
When cada uma é submetida a resolverPerfilImpedancia()
Then nenhuma chega ao motor de cálculo
And nenhuma produz resultado técnico de queda de tensão
```

### AC15 (parecer §6 C-08, "Teste funcional") — Cu/Al, 70/90°C, mono/bi/trifásico
```gherkin
Given as combinações Cu 70°C, Al 70°C e Cu 90°C, nos três tipos de circuito (monofásico, bifásico fase-fase, trifásico)
When o motor calcula usando registros reais do catálogo
Then os resultados usam Rca/XL do catálogo (nunca [VERIFICAR] nem valor derivado de resistividade genérica)
And os limites 4%, 5% e 1% (parecer §3.1, herdados de MOD-QT-2-01) são avaliados corretamente contra o resultado calculado
```

### AC16 (parecer §1 "Resultado operacional obrigatório" itens 1-4, §3.2, §6 C-02) — [PO, ADICIONADA] Todos os pontos de chamada de produção migram junto

```gherkin
Given os pontos de chamada de produção de calcularQuedaTensao() existentes hoje no repositório
When resolverPerfilImpedancia() passa a ser a única fonte de Rca/XL (AC7)
Then cada um dos pontos abaixo é migrado explicitamente, sem que nenhum permaneça chamando o motor sem perfil resolvido:
     | src/domain/servicos/servico-queda-tensao.ts (linha ~237)                |
     | src/routes/api/v1/modulos.mod-qt.validar.ts (linha ~111)               |
     | src/routes/api/v1/projetos.$projetoId.alimentador.ts                   |
     | src/routes/api/v1/projetos.$projetoId.queda-tensao-lote.ts             |
     | src/domain/queda-tensao/motores/simulador-cenarios.ts (linha ~56)      |
And os cinco campos controlados trafegam por ContextoQuedaTensao (contrato INTERNO, extensível — contratos.ts:42 declara "não é contrato público"), NUNCA por ValidarMODQTSchema (INALTERÁVEL)
And para toda chamada que não consiga formar chave completa, a rejeição do AC6 é o comportamento correto e DELIBERADO — não é bug (parecer §8: "Durante esse intervalo, o MOD-QT-2 não deve emitir cálculos de queda de tensão para projetos reais")
And as suítes existentes tests/domain/queda-tensao/motor-queda-tensao.test.ts, tests/api/queda-tensao-endpoints.test.ts, tests/api/modulos-mod-qt-motor-real.test.ts e tests/ui/queda-tensao.vrt.test.tsx são atualizadas para fornecer o perfil, e nenhuma é deletada ou silenciada com skip
And o consumo do MOD-DC via retorno_qt (criterio C5, servico-dimensionamento-condutores.ts:293 resolverC5Queda) é exercitado por teste que comprova que a rejeição chega ao MOD-DC como AUSÊNCIA de retorno_qt, jamais como retorno_qt aprovado sem perfil
```

> **[PO] Lacuna de escopo fechada.** Verificado por @po em 2026-07-28: existem **5 pontos de chamada de produção** de `calcularQuedaTensao()` e **4 suítes de teste** que o exercitam com `CONTEXTO_PADRAO_ENDPOINT`. Nenhum aparecia na File List original. Sem esta AC, AC6 + AC7 aplicados literalmente tornariam **todo** o MOD-QT-2 fail-closed em produção — incluindo o critério C5 do MOD-DC — sem que nenhuma AC descrevesse ou testasse esse efeito. Isto é o resíduo do Relatório §7 item 1 ("Isso muda o comportamento observável da API e afeta o MOD-DC, que consome a queda de tensão como critério C5"), que o parecer resolve na NORMA (§3.2) mas não na INTEGRAÇÃO. Escopo rastreável a C-02 (arquivo alvo `motor-queda-tensao.ts` + resolvedor) e ao §1 do parecer — **não é escopo novo, é a consequência necessária de C-02 tornada explícita e testável**.

### Método de verificação por AC

| AC | Método de verificação | Evidência exigida no gate |
|----|------------------------|----------------------------|
| AC1, AC2, AC3, AC4 | Teste automatizado (Vitest) sobre o catálogo estático | Teste nomeado citando o AC, comparando contagens/campos contra `impedancia-prysmian.json` |
| AC5, AC6, AC7 | Teste automatizado (Vitest) do `resolverPerfilImpedancia()` e do motor | Teste unitário + teste de integração do motor |
| AC8 | Teste automatizado (Vitest) | Teste do motor para `BIFASICO_FASE_FASE_SEM_NEUTRO` |
| AC9, AC10 | Teste automatizado (Vitest) — CA-QT-19 regenerado | `ca-qt-19-nao-regressao.test.ts` passando, com oracle independente |
| AC11, AC12, AC13, AC14 | Teste automatizado (Vitest) — suíte de completude | Arquivo de teste dedicado citando C-08 |
| AC15 | Teste automatizado (Vitest) — suíte funcional | Casos Cu/Al × 70/90°C × mono/bi/trifásico, um por combinação mínima |
| AC16 | Teste automatizado (Vitest) + inspeção de diff | Suíte completa verde após migração dos 5 pontos de chamada; teste de integração MOD-DC/C5; nenhum `it.skip`/`describe.skip` introduzido |

Nenhum AC desta story depende de UI ou de inspeção documentada — todos têm evidência automatizada exigível, dado que o escopo é motor/domínio/dados.

## Fora de escopo e riscos registrados

### Risco cross-módulo — limite EDP-SP de 7% para 5%

O parecer §3.4 resolve VER-QT-07 fixando `limite_total_pct = 5` para o perfil `EDP_SP_PTDTPDN00068_V09_AEREA_BT` (implementado na story `MOD-QT-2-04`, não nesta). O relatório §7, item 5, registra explicitamente: **"O impacto do limite 7% → 5% no MOD-DC, cujo PRD §13.6 assume 7%."** Este risco é registrado aqui como **pendência explícita para story futura** — **esta story e a `MOD-QT-2-04` NÃO alteram o MOD-DC**. Qualquer ajuste ao PRD do MOD-DC ou ao seu código exige uma story própria, com validação de @po/@architect sobre o impacto no critério C5.

## Decisões de @po (Pax) — FECHADAS em 2026-07-28

> As três questões que o @sm registrou como abertas foram decididas por @po durante `*validate-story-draft`. **Nenhuma permanece aberta ao entrar em implementação.** @dev implementa conforme abaixo e não reabre.

### PO-01 — Identidade da fonte (`fonte_id` / `versao_fonte`) — **DECIDIDA**

**Conflito:** parecer §3.1 exige `fonte_id = 'PRYSMIAN_BT_REV10'`; o artefato extraído grava `'PRYSMIAN_BT_GUIA'` nos 1.563 registros (verificado por @po). Relatório §1 ressalva que "Rev. 10" consta **apenas no nome do arquivo da URL** — a capa não repete e os metadados internos indicam criação em 2020-09-22.

**Decisão: ancoragem dupla — o hash é a IDENTIDADE, o rótulo é o IDENTIFICADOR.**

1. `fonte_id = 'PRYSMIAN_BT_REV10'` (literal do parecer). **Motivo:** o parecer é a fonte decisória hierarquicamente superior e o §3.2 compõe `perfil_id` com esse literal; trocá-lo divergiria silenciosamente da definição de `perfil_id` e do formato de citação obrigatório do §6 C-01 (que escreve "Rev. 10" por extenso).
2. `fonte_sha256 = '82131cb4aa4b2c66c4835a8fd71bb18bfe72266e0fae1f48b3cc3f05c06ea54a'` e `fonte_url` são campos **obrigatórios** do catálogo (AC3). O hash é o que identifica a cópia de forma verificável.
3. `versao_fonte` **não pode afirmar "REV10" como fato**. Deve gravar o rótulo **qualificado como proveniência declarada**, com esta redação obrigatória: `"REV10 — rótulo declarado no nome do arquivo da URL oficial; não repetido na capa nem nos metadados internos do PDF (criação 2020-09-22). Identidade verificável: SHA-256 82131cb4..."`. **Artigo IV:** afirmar a revisão como confirmada seria invenção; omitir o hash seria perder a única identificação confiável. As duas informações andam juntas.
4. O remapeamento `PRYSMIAN_BT_GUIA` → `PRYSMIAN_BT_REV10` é **renomeação de rótulo, não transformação de valor** — nenhuma célula de `Rca`/`XL` é tocada. Deve ser registrado no Dev Agent Record com a contagem (1.563 registros remapeados).
5. Troca futura de revisão exige novo pacote de dados, novo hash e aprovação técnica (parecer §5.1). Um teste deve falhar se `fonte_sha256` divergir do valor acima.

### PO-02 — Família de cabo padrão — **DECIDIDA: não existe padrão; seleção é obrigatória**

**Decisão: NENHUMA família é default. A seleção é obrigatória e a ausência é rejeição (fail-closed).**

**Motivo:** um default significaria o sistema escolher silenciosamente o produto de um fabricante pelo engenheiro, e dimensionar o projeto contra um cabo que o projetista nunca selecionou. É exatamente a "resistência genérica" que o parecer abole. Rastreável a §3.1 ("O catálogo não aceita o rótulo genérico Cu ou Al como entrada suficiente"), §3.2 e §4 ("A opção não existe no formulário e o resolvedor recusa chave inválida").

**Consequência estrutural — `familia_id` comercial × `familia_grupo_id` do catálogo.** O parecer §3.1 cadastra **13 famílias comerciais** (Superastic, Superastic Flex, Afumex Green, Sintenax, Sintenax Flex, GSette Easy, Afumex Flex, Voltenax, Voltalene, Superastic AL, Sintenax AL, Voltenax AL, Voltalene AL), mas o artefato tem apenas **9 rótulos literais**, dos quais 4 são compostos (ex.: `"Superastic Flex (cobre) e Afumex Green (cobre)"`) porque as famílias **compartilham a mesma célula publicada**. Verificado por @po: separar em 13 famílias produziria 2.286 registros, quebrando o AC1 (1.563).

- O catálogo armazena **1.563 registros** com `familia_grupo_id` = rótulo literal (9 grupos). Fiel 1:1 às células publicadas, sem duplicação.
- `familia_id` (13 comerciais) é um **alias de seleção** com mapa N:1 declarado para `familia_grupo_id`. O mapa é rastreável (parecer §3.1 matriz + Relatório §2 rótulos literais), não inventado.
- `perfil_id` compõe-se com `familia_grupo_id` (AC12). O `familia_id` selecionado é gravado no rastreio, para a citação de fonte refletir o produto escolhido.

**Perfil de fixture do CA-QT-19 (AC9):** os 504 vetores legados não têm família. Recebem, **como dado de teste declarado explicitamente e sem efeito em produção**, `familia_grupo_id = "Superastic (cobre)"` (tabela 28) e `topologia_coluna_id = "2_UNIPOLARES_JUSTAPOSTOS"`. **Motivo:** o Relatório §4.3 demonstra numericamente que a tabela provisória correspondia ao Superastic Cu (2,5 / 4 / 10 / 16 / 25 mm² idênticos). É continuidade baseada em evidência, não escolha arbitrária. A topologia (bloco 1, coluna 1) deve ser **declarada em constante nomeada com comentário citando esta decisão**, jamais implícita. Os vetores legados são `num_fases: 1` (`CONTEXTO_PADRAO_ENDPOINT`), coerente com a topologia de 2 condutores.

### PO-03 — Fonte única de fabricante (Prysmian) — **DECIDIDA: aceitável nesta rodada, com consequência declarada**

**Decisão: SIM, fonte única Prysmian é aceitável para esta rodada.** Rastreável ao parecer §2 [F4] e §5.1, que adotam Prysmian Rev. 10 como fonte primária operacional.

**Consequências obrigatórias, que fazem parte do escopo desta story:**

1. **O catálogo é agnóstico de fabricante por construção.** `fonte_id` é uma **coluna discriminadora do registro**, nunca uma constante embutida em tipo, assinatura de função ou filtro do resolvedor. Um segundo fabricante deve poder ser adicionado sem alterar o schema, o resolvedor ou o motor. Custo hoje: ~zero. Custo se ignorado: reescrita do resolvedor. **Esta é a consequência que torna a decisão reversível.**
2. **A citação de fonte por registro (AC4) já expõe o fabricante** — o memorial/UI mostra ao engenheiro que o cálculo está vinculado a um produto Prysmian específico. Não há vínculo oculto.
3. **Nenhuma analogia entre fabricantes é permitida, nunca** (parecer §8) — nem como fallback, nem como aproximação.
4. Item de backlog registrado para avaliação de segunda fonte. **Não é bloqueio desta story.**

### Itens do Relatório §7 ("O que NÃO está decidido por este relatório")

| # | Item (Relatório §7) | Status após o parecer |
|---|---|---|
| 1 | Se o motor passa a **exigir** produto e topologia explícitos e **bloqueia** o cálculo sem eles | **RESOLVIDO NA NORMA, FECHADO NA INTEGRAÇÃO POR @po** — §3.2 determina rejeição de chave incompleta antes do motor (AC5, AC6, AC14). ⚠️ **Correção de @po:** o parecer resolve a regra normativa, mas **não** o segundo efeito que o Relatório §7 item 1 registra — *"Isso muda o comportamento observável da API e afeta o MOD-DC, que consome a queda de tensão como critério C5"*. Esse resíduo estava **sem AC e sem File List**. Fechado pela **AC16**, adicionada por @po. |
| 2 | Qual família de cabo é o **padrão** do projeto, se houver, e como o usuário a seleciona | **FECHADO por @po — decisão PO-02**: não existe família padrão; seleção obrigatória, fail-closed. |
| 3 | Se vincular a base de produção a um único fabricante (Prysmian) é aceitável, ou se convém obter uma segunda fonte | **FECHADO por @po — decisão PO-03**: aceitável nesta rodada, com `fonte_id` obrigatoriamente como coluna discriminadora (catálogo agnóstico de fabricante). |
| 4 | Como tratar o cenário excluído pela fonte (conduto metálico fechado ferromagnético) | **RESOLVIDO pelo parecer** — §3.2, "esse cenário fica fora da lista de opções do MOD-QT-2; a UI deve indicar que requer método especializado e não deve chamar o motor"; implementado por C-03 (story `MOD-QT-2-04`), AC14 cobre a rejeição no resolvedor |
| 5 | O impacto do limite 7% → 5% no MOD-DC, cujo PRD §13.6 assume 7% | **ABERTO** — ver "Risco cross-módulo" acima |

### Também fora de escopo

- C-03, C-05, C-06 (fluxo de entrada fechado, perfil de limite EDP-SP, UI de alturas de tomada) — cobertos por `MOD-QT-2-04`.
- Qualquer alteração ao MOD-DC (§13.6 do seu PRD) — ver risco cross-módulo acima.
- Persistência de novas tabelas Supabase para o catálogo — o catálogo é estático (arquivo `.ts`/`.json` versionado no repositório), não uma tabela de banco.
- Obter/avaliar uma **segunda fonte de fabricante** — registrado no backlog por decisão PO-03; não é escopo desta story.
- Alterar o comportamento do MOD-DC em resposta à rejeição fail-closed do MOD-QT-2 — a AC16 exige apenas que a rejeição chegue ao MOD-DC como **ausência** de `retorno_qt` (comportamento já suportado: `retorno_qt` é `nullable().optional()`), não que o MOD-DC seja adaptado.

## Estimativa e valor

| Item | Valor |
|------|-------|
| **Complexidade (T-shirt)** | **XL** — substituição de fonte de dados normativa + resolvedor determinístico + regeneração de suíte de não-regressão + **migração de 5 pontos de chamada de produção e 4 suítes de teste** (AC16), sem UI nova |
| **Story points (Fibonacci)** | **21** — revisto por @po de 13 → 21 na validação. A estimativa original não contemplava a AC16 (migração dos pontos de chamada), que era uma lacuna de escopo, não um acréscimo. |
| **Prioridade** | P1 — desbloqueia VER-QT-02/03/04, hoje os únicos itens `[VERIFICAR]` que ainda produzem resultado técnico com resistência genérica/reatância ausente |
| **Valor de negócio** | Remove o último valor normativo `[VERIFICAR]` de resistência/reatância do caminho de produção do MOD-QT-2, tornando o cálculo de queda de tensão auditável contra uma fonte primária publicada, célula a célula |

## Riscos

| # | Risco | Prob. | Impacto | Mitigação (refletida nos ACs/Tasks) |
|---|-------|-------|---------|--------------------------------------|
| RSK-A1 | ~~Divergência de `fonte_id` causar retrabalho~~ | — | — | **MITIGADO/ENCERRADO por @po** — decisão PO-01 fecha a grafia antes da implementação; não há mais janela de retrabalho |
| RSK-A6 | **[PO]** Migração dos 5 pontos de chamada (AC16) tornar o MOD-QT-2 inteiramente fail-closed em produção sem que a equipe perceba o alcance | Alta | Crítico | A rejeição é o comportamento CORRETO nesta fase (parecer §8). AC16 exige teste explícito do efeito no C5 do MOD-DC, para que o fail-closed seja **observado e testado**, não descoberto em produção |
| RSK-A7 | **[PO]** `fonte_id` embutido como constante em tipos/filtros, travando o catálogo à Prysmian | Média | Alto | Decisão PO-03 item 1 exige `fonte_id` como coluna discriminadora; verificável em revisão de código |
| RSK-A2 | Regeneração do CA-QT-19 mascarar divergência ao trocar o critério de aprovação | Baixa | Crítico (Artigo IV) | AC9/AC10 exigem que a razão motor/mock vire diagnóstico, nunca critério; gate exige 0 `[VERIFICAR]` em saída aprovada |
| RSK-A3 | Restrição "Nota (1): Cabo Voltenax" (tabelas 33/36, 62 registros) ser ignorada na materialização do catálogo | Baixa | Alto (Artigo IV) | AC3 exige `nota_restricao` como campo do registro; teste de completude (AC12/AC13) deve cobrir os 62 registros afetados |
| RSK-A4 | `topologia_coluna_id` ausente ou mal mapeado quebrar a unicidade de `perfil_id` | Baixa | Alto | AC12 (teste de chave) bloqueia duplicidade; mapeamento já resolvido e validado por 724 verificações no Relatório §5.3 |
| RSK-A5 | Degradação de alumínio por resistividade genérica (RSK-4 herdado de `MOD-QT-2-01`) persistir mesmo após o catálogo cobrir Al | Baixa | Médio | AC7 exige que o motor pare de usar a tabela provisória; AC15 cobre Al explicitamente |

## Definition of Done

A story só pode ser marcada `Done` por @qa quando **todos** os itens abaixo forem verdadeiros:

1. Todos os **16** ACs cobertos por teste automatizado, conforme a tabela "Método de verificação por AC".
2. `CA-QT-19` regenerado (AC9/AC10) executado e passando, com oracle independente do mock, e razão motor/mock apenas como diagnóstico.
3. Contrato público intacto por símbolo (`RetornoMODQT`, `ValidarMODQTSchema`, `RetornoMODQTSchema`, rota `POST /api/v1/modulos/mod-qt/validar`) — critério por símbolo, não por `git diff` vazio de arquivo inteiro.
4. Nenhum valor de `Rca`/`XL` usado em produção vem de `TABELA_CU`/`TABELA_AL` genérica, resistividade, interpolação ou extrapolação.
5. As decisões **PO-01, PO-02 e PO-03** estão aplicadas e documentadas no Dev Agent Record, incluindo a contagem de registros remapeados e o mapa `familia_id` → `familia_grupo_id`.
6. `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` passando em `sistema-de-instala-es-el-tricas-sie-main/`.
7. File List da story atualizada e fiel ao diff real.
8. Nenhum item da lista NÃO TOCAR (§31 do documento-fonte `PROMPT-QUEDA-TENSAO-v2.2.md`, herdado) alterado.

## 🤖 CodeRabbit Integration

**Story Type Analysis**
**Primary Type**: Architecture (substituição de fonte de dados normativa estática, resolvedor determinístico)
**Secondary Type(s)**: API (integração ao motor de cálculo já existente)
**Complexity**: High (1.563 registros, 12 topologias, regra de rejeição fail-closed, regeneração de suíte de não-regressão de 504 vetores)

**Specialized Agent Assignment**
**Primary Agents**:
- @dev (implementação, pre-commit review — obrigatório em todas as stories)
- @architect (consultivo, se a materialização do catálogo divergir do padrão `normativa/` já usado no domínio)

**Supporting Agents**:
- @qa (quality gate desta story, com foco redobrado em Artigo IV)

**Quality Gate Tasks**
- [x] Pre-Commit (@dev): Run before marking story complete — foco em CA-QT-19 regenerado, ausência de valor genérico/interpolado, pareamento Rca+XL
- [ ] Pre-PR (@devops): Run before creating pull request — foco em regressão da suíte completa e integridade do contrato público

**Self-Healing Configuration**
**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 30 minutes
- Severity Filter: CRITICAL, HIGH

**Predicted Behavior**:
- CRITICAL issues: auto-fix (até 2 iterações), depois HALT para intervenção manual
- HIGH issues: auto-fix se iteração < 2, senão documentado como débito técnico

**CodeRabbit Focus Areas**
**Primary Focus**:
- Nenhum valor de `Rca`/`XL` inventado, interpolado, extrapolado ou convertido de outra geometria (Artigo IV)
- Contrato público (`RetornoMODQT`/schemas/rota) não alterado

**Secondary Focus**:
- Cobertura de teste de completude (9 tabelas, 1.563 registros, 24 nulos, 62 registros com `nota_restricao`)
- CA-QT-19 regenerado sem uso da razão motor/mock como critério de aprovação

## Tasks / Subtasks

Ordem executável derivada do parecer §6 (C-01 → C-02 → C-04 → C-07 → C-08):

- [x] **Task 1 — C-01: Catálogo estático integral (AC1, AC2, AC3, AC4)**
  - [x] 1.1 Criar `src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.json` materializando os 1.563 registros de `docs/research/2026-07-28-resolucao-ver-qt/impedancia-prysmian.json`, preservando literalmente cada campo (nenhuma transformação de valor)
  - [x] 1.2 Criar `src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.ts` que carrega o JSON acima como `ReadonlyArray<RegistroImpedanciaPrysmian>` tipado, sem tabela genérica auxiliar
  - [x] 1.3 Aplicar a decisão **PO-01** (`fonte_id = 'PRYSMIAN_BT_REV10'`, `fonte_sha256`/`fonte_url` obrigatórios, `versao_fonte` com a redação qualificada) e registrar no Dev Agent Record o remapeamento dos 1.563 registros. Aplicar a decisão **PO-02** (mapa `familia_id` comercial → `familia_grupo_id`, 13→9)
  - [x] 1.4 Implementar função de citação de fonte por registro conforme o formato do parecer §6 C-01

- [x] **Task 2 — C-02: Resolvedor de perfil e integração ao motor (AC5, AC6, AC7)**
  - [x] 2.1 Criar `src/domain/queda-tensao/normativa/resolver-perfil-impedancia.ts` com `resolverPerfilImpedancia(familia_id, metal, secao_mm2, quantidade_de_condutores_carregados, topologia_coluna_id)`
  - [x] 2.2 Implementar a regra de falha: 0 registros ou >1 registros usa o erro interno de `src/domain/queda-tensao/erros.ts` (criar novo código de erro se necessário, sem alterar contrato público)
  - [x] 2.3 Integrar `resolverPerfilImpedancia()` em `src/domain/queda-tensao/motores/motor-queda-tensao.ts`, removendo a chamada à tabela provisória do caminho de produção
  - [x] 2.4 Decidir e documentar no Dev Agent Record como os cinco campos controlados chegam ao motor a partir do `ContextoQuedaTensao`/`RequisicaoQuedaTensao` existentes, sem alterar `ValidarMODQTSchema`

- [x] **Task 3 — C-04: Correção do fator bifásico (AC8)**
  - [x] 3.1 Confirmar/ajustar em `motores/motor-queda-tensao.ts` que `BIFASICO_FASE_FASE_SEM_NEUTRO` usa multiplicador 2 e `V_nominal` fase-fase
  - [x] 3.2 Remover a emissão da marcação `[VERIFICAR — VER-QT-04]` para esse cenário
  - [x] 3.3 Atualizar comentários/citação de fonte para `parecer §3.3`

- [x] **Task 4 — C-07: Regeneração de CA-QT-19 (AC9, AC10)**
  - [x] 4.1 Extrair a grade de 504 vetores (`correntes[8] × comprimentos[9] × secoes[7]`, hoje duplicada nas linhas ~73-75 e ~116-118) para uma constante compartilhada, e resolver `perfil_id` por vetor a partir do perfil de fixture da decisão **PO-02** (`Superastic (cobre)` + `2_UNIPOLARES_JUSTAPOSTOS`, em constante nomeada citando a decisão). **Não procurar um array literal de 504 vetores — ele não existe** (verificado por @po)
  - [x] 4.2 Implementar o oracle de teste que lê `impedancias-prysmian-rev10.json` diretamente e aplica a fórmula do parecer §3.3, sem depender de valor pré-calculado do motor
  - [x] 4.3 Reescrever as asserções para comparar motor × oracle (não motor × mock); manter a razão motor/mock apenas como diagnóstico calculado em runtime
  - [x] 4.4 Adicionar os testes negativos: vetores sem perfil correspondente devem retornar o erro interno (AC6) antes de qualquer resultado

- [x] **Task 5 — C-08: Testes obrigatórios de completude (AC11, AC12, AC13, AC14, AC15)**
  - [x] 5.1 Criar `tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts` cobrindo: teste de fonte (9 tabelas presentes), teste de chave (unicidade de `perfil_id`, pareamento Rca+XL), teste de rastreabilidade (URL, revisão, tabela, página por registro)
  - [x] 5.2 Criar testes negativos: produto livre, seção ausente, topologia ausente, célula vazia, tabela inexistente, conduto ferromagnético — nenhum chega ao motor
  - [x] 5.3 Criar teste funcional: Cu e Al, 70°C e 90°C, monofásico/bifásico/trifásico, verificando limites 4%/5%/1%
  - [x] 5.4 Confirmar cobertura dos 62 registros com `nota_restricao` (tabelas 33/36, "Nota (1): Cabo Voltenax")

- [x] **Task 5B — [PO] AC16: Migração dos pontos de chamada de produção**
  - [x] 5B.1 Estender `ContextoQuedaTensao` (contrato INTERNO, `src/domain/queda-tensao/contratos.ts`) com os cinco campos controlados — **sem tocar `ValidarMODQTSchema`**
  - [x] 5B.2 Migrar os 5 pontos de chamada listados no AC16 (`servico-queda-tensao.ts`, `modulos.mod-qt.validar.ts`, `projetos.$projetoId.alimentador.ts`, `projetos.$projetoId.queda-tensao-lote.ts`, `simulador-cenarios.ts`)
  - [x] 5B.3 Atualizar as 4 suítes existentes que usam `CONTEXTO_PADRAO_ENDPOINT` para fornecer o perfil — **nenhum `skip`, nenhum teste deletado**
  - [x] 5B.4 Teste de integração: rejeição do MOD-QT-2 chega ao MOD-DC como ausência de `retorno_qt` (nunca como `retorno_qt` aprovado sem perfil)

- [x] **Task 6 — Gates técnicos e checklist de entrega**
  - [x] 6.1 `npm run lint` / `npm run typecheck` / `npm test` / `npm run build` (dentro de `sistema-de-instala-es-el-tricas-sie-main/`) — todos passando
  - [x] 6.2 Atualizar File List, Dev Agent Record, Completion Notes, Change Log e Status (`Ready` → `InProgress` → `InReview`)
  - [x] 6.3 Registrar no Dev Agent Record a decisão sobre a discrepância `fonte_id` (Task 1.3) de forma destacada para o gate de @qa

## Dev Notes

### Contexto herdado de MOD-QT-2-01/02

- O motor de cálculo já existe e está testado: `src/domain/queda-tensao/motores/motor-queda-tensao.ts`. Esta story **substitui a fonte de impedância** consumida pelo motor; não reescreve a orquestração de cálculo (guarda de comprimento, seleção de método, cálculo de queda do alimentador, etc.), que permanece de `MOD-QT-2-01`.
- A tabela provisória atual (`normativa/tabela-impedancia.ts`, 129 linhas) cobre apenas Cu tabelado + Al derivado de resistividade, todos `status_verificacao: '[VERIFICAR]'`. Esta story não precisa deletar esse arquivo, mas deve deixar de chamá-lo no caminho de produção (AC7); se @dev optar por removê-lo, deve confirmar que nenhum teste de `MOD-QT-2-01`/`MOD-QT-2-02` depende dele diretamente.
- `src/domain/queda-tensao/contratos.ts` já define `RastreioQuedaTensao` com `R_ohm_km`, `X_ohm_km`, `status_resistencia`, `fonte_resistencia` — esses campos devem passar a refletir o registro resolvido pelo catálogo fechado, sem alteração de forma do tipo.
- `src/domain/queda-tensao/normativa/limites.ts` não é tocado por esta story (fica para `MOD-QT-2-04`, C-05).

### Estrutura de dados do catálogo (fonte: `impedancia-prysmian.json`)

- 1.563 registros, chave: `fonte_id, tabela, familia_literal, metal, bloco_ordinal, coluna_ordinal, topologia_coluna_id, secao_mm2`.
- 12 valores distintos de `topologia_coluna_id` (Relatório §5): `2_UNIPOLARES_JUSTAPOSTOS`, `2_UNIPOLARES_S_2D`, `2_UNIPOLARES_S_13CM`, `2_UNIPOLARES_S_20CM`, `3_UNIPOLARES_JUSTAPOSTOS`, `3_UNIPOLARES_S_2D`, `3_UNIPOLARES_S_13CM`, `3_UNIPOLARES_S_20CM`, `3_UNIPOLARES_TREVO`, `CABO_BIPOLAR`, `CABO_TRIPOLAR`, `3_UNIPOLARES_20CM_X_20CM`.
- Grupo A (tabelas 28, 29, 34): 9 colunas por tabela. Grupo B (tabelas 30, 31, 32, 33, 35, 36): 12 colunas por tabela.
- Temperatura de operação: 70°C (tabelas 28, 29, 30, 31, 34, 35), 90°C (tabelas 32, 33, 36).
- Restrição "Nota (1): Cabo Voltenax" aplica-se às colunas `CABO_BIPOLAR`/`CABO_TRIPOLAR` das tabelas 33 e 36 apenas — 62 registros com `nota_restricao` preenchido, não vale para Voltalene.
- `fonte_id` no artefato já extraído: `"PRYSMIAN_BT_GUIA"` em todos os registros — ver "Discrepância de versionamento" na seção "Fora de escopo e riscos registrados".

### Testing

- Framework: Vitest, mesmo padrão de `tests/domain/queda-tensao/motor-queda-tensao.test.ts` e `ca-qt-19-nao-regressao.test.ts` já existentes.
- O oracle do CA-QT-19 regenerado deve importar o JSON do catálogo diretamente (via `import` estático ou `fs.readFileSync` em teste, seguindo o padrão já usado no projeto para dados estáticos) — não deve reimportar `motor-queda-tensao.ts` para calcular o valor esperado, sob pena de o teste comparar o motor consigo mesmo.
- Testes negativos (AC6, AC10, AC14) devem usar o mesmo mecanismo de erro (`erros.ts`) já testado em `MOD-QT-2-01`, não inventar um novo formato de erro.

## Dev Agent Record

**Agente:** @dev (Dex) · **Modo:** YOLO autônomo · **Data:** 2026-07-29
**Handoff de entrada:** `.aiox/handoffs/MOD-QT-2-VERQT-po-to-dev.yaml` (consumido)
**Transições:** `Ready` → `InProgress` → `InReview`

### Decisões de implementação

| # | Decisão | Justificativa / rastreio |
|---|---|---|
| D-03-01 | Catálogo gerado por **script versionado** (`scripts/gerar-catalogo-impedancia-prysmian.mjs`), não digitado à mão | 1.563 registros; o script só renomeia campo, renomeia o rótulo de `fonte_id` e compõe `perfil_id`. Falha se `sha256_pdf` divergir. Nenhum valor de `Rca`/`XL` é tocado |
| D-03-02 | JSON serializado com **um registro por linha** | Mantém o diff auditável célula a célula sem inflar o bundle (1,0 MB → 0,81 MB) |
| D-03-03 | Bloco `fontes` é **lista**, e a proveniência (`versao_fonte`/`fonte_url`/`fonte_sha256`) é hidratada no `.ts` via `fonte_id` | Decisão PO-03: um segundo fabricante entra sem alterar schema, resolvedor ou motor. Evita repetir ~200 chars × 1.563 no JSON |
| D-03-04 | **PO-01 aplicada.** `fonte_id = 'PRYSMIAN_BT_REV10'` em **1.563/1.563** registros remapeados de `PRYSMIAN_BT_GUIA` (renomeação de rótulo, zero células alteradas — provado pelo teste "nenhum valor de Rca/XL difere do artefato"). `versao_fonte` grava a redação qualificada obrigatória. `rotulo_revisao: "Rev. 10"` foi extraído para **campo de dado**, para que a citação do §6 C-01 não embuta o literal em código | PO-01 itens 1-5; teste de SHA-256 obrigatório implementado |
| D-03-05 | **PO-02 aplicada.** `MAPA_FAMILIA_COMERCIAL_PARA_GRUPO` (13 aliases → 9 grupos); `perfil_id` composto com `familia_grupo_id`; alias gravado no rastreio e na citação. `CONTEXTO_PADRAO_ENDPOINT` **não** ganhou família — ausência é rejeição | PO-02; testado em `catalogo-impedancia-completude.test.ts` |
| D-03-06 | **PO-03 aplicada.** `fonte_id` é coluna discriminadora; o resolvedor **não menciona "PRYSMIAN"** em lugar algum (teste de inspeção de código o garante); `citarFonteImpedancia` monta o fabricante a partir do registro | PO-03 itens 1-3 |
| D-03-07 | Os cinco campos controlados chegam ao motor por **`ContextoQuedaTensao`** (interno): `familia_id`, `topologia_coluna_id`, `quantidade_de_condutores_carregados` são novos; `secao_mm2` vem de `RequisicaoQuedaTensao` e `metal` é derivado de `material` (`Cu`→`CU`). `ValidarMODQTSchema` intocado | Task 2.4 / 5B.1; AC16 |
| D-03-08 | Persistência do perfil: novo `perfil_cabo` **opcional** em `QuedaTensaoConfig` e em `ConfiguracaoAlimentadorSchema` (`PUT /alimentador`) | É o conduto que permite às 4 suítes "fornecer o perfil" (AC16) sem tocar o contrato público. Opcional por PO-02: ausente ⇒ rejeição. C-03 (MOD-QT-2-04) preencherá pela UI |
| D-03-09 | `resolverPerfilImpedancia()` **lança**; `tentarResolverPerfilImpedancia()` devolve `null` apenas nas varreduras (seção mínima e sugestões), onde o comportamento herdado já era "pular seção desconhecida, nunca estimar" | AC6 exige falha antes de `RetornoMODQT`; a variante não-lançante não é fallback — não produz valor |
| D-03-10 | **Método SIMPLIFICADO/COMPLETO preservado** (corte em 25 mm²). Com `cosφ = 1` as duas fórmulas coincidem exatamente, e o oracle do CA-QT-19 confere os 504 vetores na igualdade | Remover o corte não está em C-01..C-08; seria escopo novo (Artigo IV) |
| D-03-11 | `isolacao` deixou de selecionar R. A temperatura de operação agora vem do **registro** (a família a determina — fonte p.21 §6.3). `isolacao` permanece no rastreio como descritivo | Consequência de C-01; nenhuma coerência isolação×temperatura foi inventada |
| D-03-12 | `CenarioSimulacao` ganhou `familia_id`/`topologia_coluna_id`/`quantidade_de_condutores_carregados` opcionais | Trocar metal sem trocar família é incoerente e agora é rejeitado — "o mesmo cabo, em alumínio" não existe (parecer §8). Testado |
| D-03-13 | Suítes de endpoint migradas pelo ponto de extensão **já existente** `_setClienteModQTParaTeste` | Preserva integralmente a cobertura de MOD-QT-2-01/02 sem `skip`, sem deleção e sem estender o schema público |
| D-03-14 | **5ª suíte afetada descoberta:** `tests/api/modulos-mod-qt.test.ts` (MOD-QT-1) não constava do handoff nem da File List. Migrada do mesmo modo, + teste novo do fail-closed | Registrado para @qa |

### Efeito observável declarado (RSK-A6)

`POST /api/v1/modulos/mod-qt/validar` responde **422 com `status: PENDENTE`** e o código
`ERRO-PERFIL-IMPEDANCIA-CHAVE-INVALIDA` enquanto o perfil não trafegar. O lote devolve o
circuito como `PENDENTE` com `resultado: null` e `retorno_publico: null`. O MOD-DC recebe
**ausência** de `retorno_qt` → C5 `PENDENTE`/`AGUARDANDO-QT`. Comprovado por teste
dedicado (`integracao-mod-dc-c5-fail-closed.test.ts`). É o comportamento correto do
parecer §8, não regressão.

### Gates técnicos (medidos)

| Gate | Resultado |
|---|---|
| `npx tsc --noEmit` | **PASS** — exit 0 |
| `npx vitest run` (suíte completa) | **PASS** — `Test Files 129 passed (129)`, `Tests 893 passed (893)`, 185,8 s |
| `npx vite build` | **PASS** — `built in 7.23s` |
| `npx eslint` **escopado** aos arquivos alterados | **PASS** — exit 0 (após `prettier --write` nos mesmos arquivos) |
| `npx eslint .` (projeto inteiro) | **NAO_VERIFICADO** — trava sem saída (>25 min), defeito ambiental pré-existente reproduzido por 3 agentes. Não presumido PASS |

Baseline informado pelo lead registrava 1 falha pré-existente em
`tests/domain/calculo/derivar-circuitos.test.ts`. No fechamento desta story a suíte
completa está **integralmente verde** — nenhuma falha nova foi introduzida e a falha
pré-existente não foi tocada por este trabalho.

### Anti-fraude — o que NÃO foi feito

Nenhum `it.skip`/`describe.skip` introduzido; nenhuma suíte deletada; nenhum valor de
célula arredondado, interpolado ou extrapolado; nenhum `XL = 0`; nenhuma família padrão;
nenhum fallback de 7%; nenhum arquivo de `src/domain/dimensionamento-condutores/`
alterado (verificado por teste); os 4 símbolos do contrato público intocados.

## File List (real — @dev, 2026-07-29)

**Novos:**
- `sistema-de-instala-es-el-tricas-sie-main/scripts/gerar-catalogo-impedancia-prysmian.mjs`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.json`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/resolver-perfil-impedancia.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/fixtures/perfil-impedancia-fixture.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/resolver-perfil-impedancia.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/integracao-mod-dc-c5-fail-closed.test.ts`

**Modificados — domínio:**
- `.../src/domain/queda-tensao/contratos.ts` (interno: `ContextoQuedaTensao` + 5 campos; `RastreioQuedaTensao` + perfil resolvido)
- `.../src/domain/queda-tensao/erros.ts` (5 novos `CodigoErroQuedaTensao`; classe inalterada)
- `.../src/domain/queda-tensao/index.ts` (exporta catálogo e resolvedor)
- `.../src/domain/queda-tensao/motores/motor-queda-tensao.ts` (C-02 + C-04)
- `.../src/domain/queda-tensao/motores/simulador-cenarios.ts` (perfil nos cenários)

**Modificados — integração (AC16):**
- `.../src/domain/servicos/servico-queda-tensao.ts`
- `.../src/infra/repositorios/repositorio-queda-tensao-config.ts` (`PerfilCaboProjeto`)
- `.../src/api/schemas/queda-tensao.ts` (`PerfilCaboSchema` — NÃO é o contrato público)
- `.../src/routes/api/v1/modulos.mod-qt.validar.ts` (**apenas o corpo do handler**)
- `.../src/routes/api/v1/projetos.$projetoId.alimentador.ts`
- `.../src/routes/api/v1/projetos.$projetoId.queda-tensao-lote.ts` (documentação do efeito)

**Modificados — testes:**
- `.../tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts` (regenerado, C-07)
- `.../tests/domain/queda-tensao/motor-queda-tensao.test.ts`
- `.../tests/api/queda-tensao-endpoints.test.ts`
- `.../tests/api/modulos-mod-qt-motor-real.test.ts`
- `.../tests/api/modulos-mod-qt.test.ts` (**não constava do handoff**)
- `.../tests/ui/queda-tensao.vrt.test.tsx` (+ snapshot regenerado)

**Confirmados NÃO modificados (contrato público / NÃO TOCAR):**
- `.../src/domain/dimensionamento-condutores/**` (verificado por teste automatizado)
- `.../src/api/schemas/otimizar-condutor.schema.ts`
- `.../src/domain/queda-tensao/normativa/limites.ts`
- `.../src/domain/queda-tensao/normativa/tabela-impedancia.ts` (mantida para auditoria; fora do caminho de produção)

## File List (planejada — @sm, mantida para auditoria)

**Novos:**
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.json`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/resolver-perfil-impedancia.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/catalogo-impedancia-completude.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/resolver-perfil-impedancia.test.ts`

**Modificados:**
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/motores/motor-queda-tensao.ts` (integração do resolvedor, correção C-04)
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/erros.ts` (novo `CodigoErroQuedaTensao` para perfil não resolvido — classe `ErroQuedaTensao` inalterada)
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/contratos.ts` (**contrato INTERNO** — estender `ContextoQuedaTensao` com os cinco campos controlados e `RastreioQuedaTensao` com o perfil resolvido)
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts` (regeneração completa, C-07)
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/index.ts` (exportar novos símbolos)

**Modificados — [PO] AC16, migração dos pontos de chamada (ausentes na File List original):**
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-queda-tensao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-qt.validar.ts` — **apenas o corpo do handler**; a rota, o path e o `ValidarMODQTSchema` permanecem intactos (verificação por símbolo)
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.alimentador.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.queda-tensao-lote.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/motores/simulador-cenarios.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/queda-tensao/motor-queda-tensao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/queda-tensao-endpoints.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-qt-motor-real.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/queda-tensao.vrt.test.tsx`

**Explicitamente NÃO modificados (contrato/lista NÃO TOCAR):**
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/otimizar-condutor.schema.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-qt.validar.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/queda-tensao/normativa/limites.ts` (fica para `MOD-QT-2-04`)

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-07-28 | 0.1 | Story criada a partir do parecer decisório `docs/research/{2026-07-28}-resolucao-ver-qt.md` §6 (C-01, C-02, C-04, C-07, C-08). Cobre VER-QT-02, VER-QT-03 e VER-QT-04. Declara dependência de nenhuma story anterior não concluída (consome `MOD-QT-2-01`/`MOD-QT-2-02`, ambas `InReview`). Registra a discrepância de `fonte_id` como questão aberta para @po. Status `Draft`. | @sm (River) |
| 2026-07-29 | 1.0 | **Implementação `*dev-develop-story` (YOLO).** Status `Ready` → `InProgress` → `InReview`. C-01: catálogo de 1.563 registros gerado por script versionado (9 tabelas, 12 topologias, 9 grupos, 24 nulos, 62 `nota_restricao`). C-02: `resolverPerfilImpedancia()` + integração fail-closed no motor. C-04: marcação `[VERIFICAR — VER-QT-04]` retirada e fonte corrigida para o parecer §3.3. C-07: CA-QT-19 regenerado com oracle independente (JSON bruto + fórmula §3.3); razão motor/mock virou diagnóstico em runtime. C-08: suítes de completude, chave, rastreabilidade, negativos e funcional. AC16: 5 pontos de chamada migrados, 4 suítes atualizadas + 1 quinta suíte descoberta (`tests/api/modulos-mod-qt.test.ts`), e teste de integração do C5 do MOD-DC. Decisões PO-01/02/03 aplicadas e documentadas no Dev Agent Record. Gates: typecheck PASS, `vitest run` 893/893 PASS, build PASS, lint escopado PASS (lint global `NAO_VERIFICADO` — trava ambiental). | @dev (Dex) |
| 2026-07-29 | 1.1 | **QA Gate `*qa-gate` — CONCERNS (quality score 92). Status `InReview` → `Done`.** Verificação independente do @qa: contrato público intacto por símbolo (schema file ausente de `git status`; diff de `dimensionamento-condutores/contratos.ts` toca só `ResultadoDimensionamento`; `createFileRoute` da rota byte a byte idêntico). Integridade do catálogo reconferida contra `impedancia-prysmian.json`: 1.563/1.563 registros, **0 valores de Rca/XL divergentes**, 24 nulos preservados, 0 zeros, `perfil_id` unívoco 1.563/1.563, 9 tabelas, 12 topologias, 9 grupos, 62 `nota_restricao`. PO-01/02/03 aplicadas corretamente (`fonte_id = PRYSMIAN_BT_REV10` em 100%, `versao_fonte` qualificada, `fonte_id` como coluna discriminadora — 0 vazamento de "PRYSMIAN" no resolvedor). Oracle do CA-QT-19 confirmado independente (lê o JSON bruto por `readFileSync`, aplica a fórmula §3.3, não importa o motor). Gates: `tsc` PASS, `vitest run` **947/947 em 2 execuções consecutivas**, `vite build` PASS (12,18 s), `eslint` escopado aos 22 arquivos desta story PASS (exit 0); `eslint .` NÃO VERIFICADO (trava ambiental, não presumido PASS). 3 ressalvas de severidade baixa (TEST-001, TEST-002, OPS-001) registradas em `docs/qa/gates/MOD-QT-2-03-gate.yaml`, nenhuma bloqueante. | @qa (Quinn) |
| 2026-07-28 | 0.2 | **Validação `*validate-story-draft` — GO, 9/10.** Correções aplicadas por @po dentro da alçada de PO (escopo/AC/rastreabilidade): (1) **AC8** — símbolo `BIFASICO_FASE_FASE_SEM_NEUTRO` não existe no código; reescrito para `num_fases === 2` / `NumeroFasesQT`. (2) **AC9 / Task 4.1** — não existe fixture de 504 vetores; são grade cartesiana 8×9×7 gerada em runtime; instrução reescrita para ser executável. (3) **AC3** — nomes de campo do parecer §3.1 divergem do artefato real; adicionada tabela de mapeamento (renomeação, não transformação de valor). (4) **AC5** — `quantidade_de_condutores_carregados` não é campo do catálogo (Relatório §5.5 descartou a hipótese); reclassificado como validação de coerência, não filtro. (5) **AC6** — permitido novo `CodigoErroQuedaTensao` (erros.ts não tem código para perfil não resolvido). (6) **AC12** — `perfil_id` composto com `familia_grupo_id`, não com o alias comercial. (7) **AC16 ADICIONADA** — migração dos 5 pontos de chamada de produção e 4 suítes de teste, lacuna de escopo que tornaria o MOD-QT-2 e o critério C5 do MOD-DC integralmente fail-closed sem AC nem teste. (8) Estimativa 13 → 21 pontos. (9) Riscos RSK-A6/RSK-A7 adicionados; RSK-A1 encerrado. (10) File List completada. **Decisões PO-01 (fonte_id/ancoragem dupla hash+rótulo), PO-02 (sem família padrão; alias 13→9) e PO-03 (fonte única aceitável com catálogo agnóstico de fabricante) FECHADAS.** Status `Draft` → `Ready`. | @po (Pax) |

---

## Validação de @po (Pax) — 2026-07-28

**Comando:** `*validate-story-draft` (modo YOLO autônomo) · **Workflow:** `MOD-QT-2-RESOLUCAO-VERQT`
**Veredito: GO** · **Nota: 9/10** (antes das correções: 7/10)

### Checklist de 10 pontos (`.claude/rules/story-lifecycle.md` Fase 2)

| # | Ponto | Veredito | Evidência |
|---|---|---|---|
| 1 | Título claro e objetivo | ✅ PASS | Título nomeia o entregável (catálogo + resolvedor) e as pendências (VER-QT-02/03/04) |
| 2 | Descrição completa | ✅ PASS | Seções "Fonte normativa e escopo", "Story" (as-a/I-want/so-that) e "Escopo desta story" mapeiam C-01/C-02/C-04/C-07/C-08 |
| 3 | ACs testáveis | ✅ PASS *(pós-correção; era ⚠️ PARTIAL)* | 16 ACs em Gherkin + tabela "Método de verificação por AC". 4 defeitos factuais corrigidos (AC3, AC5, AC8, AC9) — símbolos e fixtures inexistentes tornavam as ACs não executáveis |
| 4 | Escopo IN/OUT definido | ✅ PASS *(pós-correção; era ⚠️ PARTIAL)* | Lacuna fechada: 5 pontos de chamada de produção + 4 suítes de teste não estavam nem IN nem OUT. AC16 + Task 5B + File List |
| 5 | Dependências mapeadas | ✅ PASS | Predecessoras `MOD-QT-2-01`/`-02` (InReview) declaradas; sem `blockedBy` (correto — esta é a raiz da cadeia) |
| 6 | Estimativa de complexidade | ✅ PASS | Revista por @po: L/13 → XL/21, refletindo a AC16 |
| 7 | Valor de negócio | ✅ PASS | Remoção do último `[VERIFICAR]` de Rca/XL do caminho de produção; P1 justificada |
| 8 | Riscos documentados | ✅ PASS *(pós-correção; era ⚠️ PARTIAL)* | 5 riscos originais bons; RSK-A6/A7 adicionados; RSK-A1 encerrado por PO-01 |
| 9 | Critérios de Done | ✅ PASS | 8 itens de DoD, com verificação de contrato por símbolo |
| 10 | Alinhamento com a fonte | ✅ PASS | **Todos os 16 ACs rastreiam a seção numerada** do parecer (§N) ou do Relatório. Nenhum AC sem fonte (Artigo IV) |

**Nota: 9/10.** O ponto retido é a **estimativa (6)**: 21 pontos é a melhor aproximação disponível, mas a migração dos 5 pontos de chamada (AC16) não tem precedente medido neste repositório. Recomendação ao @dev: se a Task 5B exceder o previsto, **parar e escalar** em vez de reduzir cobertura de teste.

### Gates de NO-GO automático — todos limpos

| Gate | Resultado | Verificação |
|---|---|---|
| AC sem rastreio a seção numerada | ✅ LIMPO | 16/16 rastreados |
| Story toca o contrato público | ✅ LIMPO | `RetornoMODQT` (contratos.ts:50), `ValidarMODQTSchema` (schema:86), `RetornoMODQTSchema` (schema:74) e a rota (`createFileRoute("/api/v1/modulos/mod-qt/validar")`) confirmados existentes e **fora** de escopo. `src/domain/queda-tensao/contratos.ts` é contrato **interno** (declarado no próprio arquivo, linhas 4-7) — extensível |
| `[VERIFICAR]` tratado como resolvido sem fonte | ✅ LIMPO *(pós-correção)* | Relatório §7 item 1 estava marcado "RESOLVIDO" perdendo a metade de integração; corrigido e fechado pela AC16 |
| Escopo fora de C-01..C-08 | ✅ LIMPO | AC16 é consequência necessária de C-02, não escopo novo |

### Verificação contra o código real (não contra a descrição da story)

| Alvo | Estado |
|---|---|
| `src/domain/queda-tensao/{contratos,erros,index}.ts` | ✅ existem |
| `motores/{motor-queda-tensao,simulador-cenarios}.ts` | ✅ existem |
| `normativa/{limites,resistividade,tabela-impedancia}.ts` | ✅ existem |
| `RetornoMODQT` / `ValidarMODQTSchema` / `RetornoMODQTSchema` / rota | ✅ existem |
| `tests/.../ca-qt-19-nao-regressao.test.ts` | ✅ existe — **504 vetores CONFIRMADOS por cálculo (8×9×7), mas gerados em runtime, não como fixture** |
| `impedancia-prysmian.json` | ✅ 1.563 registros · 9 tabelas · 12 topologias · 9 famílias literais · 24 nulos (Rca e XL) · 62 `nota_restricao` · `fonte_id` = `PRYSMIAN_BT_GUIA` em 100% · chave (família, seção, topologia) unívoca em 1.563/1.563 |
| `BIFASICO_FASE_FASE_SEM_NEUTRO` | ❌ **não existe** — AC8 corrigida |

### Riscos que permanecem REGISTRADOS e FORA de escopo — confirmado

- **Limite EDP 7% → 5% vs. PRD do MOD-DC §13.6:** registrado como risco cross-módulo; **nenhum arquivo de `src/domain/dimensionamento-condutores/` está na File List** — verificado.
- **Conduto metálico fechado ferromagnético:** tratado como **rejeição** (AC14: "nenhuma chega ao motor"), nunca como degradação de cálculo — verificado.

**— Pax, equilibrando prioridades 🎯**

**Story created by:** @sm (River)
**Date:** 2026-07-28
**Priority:** P1
**Source:** `docs/research/{2026-07-28}-resolucao-ver-qt.md` (parecer, revisão 2) + `docs/research/2026-07-28-resolucao-ver-qt/RELATORIO-EXTRACAO-IMPEDANCIA.md` + `docs/research/2026-07-28-resolucao-ver-qt/impedancia-prysmian.json`

---

## QA Results

### Review Date: 2026-07-29

### Reviewed By: Quinn (Test Architect) — modo YOLO autônomo

**Veredito: CONCERNS** · **Quality score: 92** · Status `InReview` → `Done`

Gate: CONCERNS → `docs/qa/gates/MOD-QT-2-03-gate.yaml`

#### Postura de revisão

Nenhum item do relato do @dev foi aceito sem verificação própria. As 1.563 conferências
célula a célula foram refeitas por script de comparação direta contra o artefato de
extração — não por amostragem.

#### Verificações independentes

| # | Verificação | Resultado | Evidência observada |
|---|---|---|---|
| V1 | Contrato público byte-a-byte, **por símbolo** | ✅ PASS | `otimizar-condutor.schema.ts` **ausente** de `git status --porcelain` → `ValidarMODQTSchema`/`RetornoMODQTSchema` idênticos ao HEAD. `git diff -U0` de `dimensionamento-condutores/contratos.ts` toca **apenas** `ResultadoDimensionamento` (`ib_a`, `i2_a`, `fonte_i2` — trabalho alheio de MOD-CC/AUTO-OTI); `RetornoMODQT` não aparece no diff. Na rota, `createFileRoute("/api/v1/modulos/mod-qt/validar")` e o import dos 2 schemas são byte a byte idênticos; o diff é só corpo de handler |
| V2 | PO-01 — `fonte_id`, hash, URL, `versao_fonte` | ✅ PASS | `fonte_id` distintos no catálogo = `['PRYSMIAN_BT_REV10']`, **0** ocorrências de `PRYSMIAN_BT_GUIA`. `fonte_sha256`/`fonte_url` obrigatórios no tipo. `versao_fonte` grava a redação qualificada exigida; o literal "Rev. 10" foi isolado em `rotulo_revisao` e só aparece na citação — **em nenhum ponto a revisão é afirmada como fato confirmado** |
| V3 | PO-03 — `fonte_id` é coluna discriminadora | ✅ PASS | `grep PRYSMIAN\|Prysmian src/` fora do catálogo → 3 linhas, **todas comentário** em arquivos provisórios legados. `RegistroImpedanciaCatalogo.fonte_id` é `string` (não union literal); bloco `fontes` é lista; o resolvedor não filtra nem menciona fabricante |
| V4 | Nenhum `[VERIFICAR]`→`CONFIRMADO` sem fonte; nenhum `XL = 0`; nenhuma célula não publicada virou `0` | ✅ PASS | Zeros de `r_ca_ohm_km` = **0**; zeros de `x_l_ohm_km` = **0**; nulos 24 (fonte) → 24 (catálogo). Comparação chave a chave: **0 registros sem par** e **0 valores divergentes**. `tabela-impedancia.ts` e `resistividade.ts` seguem `[VERIFICAR]` e foram **aposentados** do caminho de produção (o motor importa só `resolver-perfil-impedancia`) |
| V5 | Rejeição **antes** de montar `RetornoMODQT` (teste negativo lido, não alegado) | ✅ PASS | `resolver-perfil-impedancia.test.ts` describe "AC6 / AC7 — a rejeição ocorre ANTES de montar RetornoMODQT" (:200) + 6 casos negativos (:126-198). Código: os 6 ramos lançam `ErroQuedaTensao` antes de qualquer cálculo; `calcularQuedaTensao` resolve o perfil na linha 333, antes de compor o resultado |
| V6 | CA-QT-19 — oracle independente; razão motor/mock só diagnóstico | ⚠️ CONCERNS | Oracle **confirmado independente**: lê o JSON bruto por `readFileSync` (:45-52) e aplica a fórmula §3.3, sem importar o motor; 504 vetores em runtime (8×9×7). Ressalva: o bloco "diagnóstico legado" ainda contém `expect(Math.min(...razoes)).toBeGreaterThan(1)` — a razão pode reprovar a suíte (TEST-002) |
| V8 | 422/`PENDENTE` sem perfil, **coberto por teste** | ✅ PASS | `modulos-mod-qt-motor-real.test.ts:70` e `modulos-mod-qt.test.ts:221` (+ `:233` para C5 `AGUARDANDO-QT`). Ramo 422 explícito no handler. Comportamento deliberado do parecer §8, não regressão |
| V9 | MOD-DC intocado | ✅ PASS | `git diff src/domain/dimensionamento-condutores/` → **0 ocorrências** de `queda\|perfil_cabo\|impedanc\|prysmian\|retorno_qt\|limite_total`. Os 9 arquivos modificados no diretório são de MOD-CC/AUTO-OTI/proteção, alheios a esta cadeia |
| V10 | `BLK-QT-TIMEOUT-FLAKY-01` | ⚠️ NÃO REPRODUZIDO | 2 execuções completas consecutivas: 132/132 arquivos, 947/947 testes, exit 0. **Blocker mantido ABERTO**, severidade rebaixada MÉDIA → BAIXA. Não fechado: a causa estrutural (1.563 × 13 asserts sem `testTimeout` próprio) permanece inalterada |

#### Gates técnicos (executados pelo @qa, números reais)

| Gate | Comando | Resultado |
|---|---|---|
| Tipagem | `npx tsc --noEmit` | **PASS** — exit 0, sem saída |
| Testes (1ª execução) | `npx vitest run` | **PASS** — `Test Files 132 passed (132)`, `Tests 947 passed (947)`, 242,56 s |
| Testes (2ª execução) | `npx vitest run` | **PASS** — `Test Files 132 passed (132)`, `Tests 947 passed (947)`, 239,01 s |
| Build | `npx vite build` | **PASS** — `built in 12.18s` |
| Lint escopado (22 arquivos desta story) | `npx eslint <lista>` | **PASS** — exit 0 |
| Lint do projeto inteiro | `npx eslint .` | **NÃO VERIFICADO** — trava ambiental pré-existente. Não presumido PASS |

#### Ressalvas (nenhuma bloqueante)

| ID | Sev. | Achado |
|---|---|---|
| TEST-001 | low | `ca-qt-19-nao-regressao.test.ts:174` usa `fonte.includes("[VERIFICAR]")`, que **não casa** com `MARCACAO_VERIFICAR_ALINEA = "[VERIFICAR — alínea 6.2.7.1]"`. O guarda do §6 C-07 é mais estreito do que o teste declara. Sem defeito hoje (grade usa limite 4%, fora de `[5,7]`), mas não detectaria a regressão que existe para impedir |
| TEST-002 | low | `:240` assert sobre a razão motor/mock dentro do bloco declarado "não é critério". O critério de correção continua sendo o oracle — por isso baixa |
| OPS-001 | low | Causa estrutural do timeout flaky inalterada em `catalogo-impedancia-completude.test.ts:156` |

#### 7 checks de qualidade (Fase 4)

Code review ✅ · Unit tests ✅ · Acceptance criteria ✅ (16/16) · No regressions ✅ ·
Performance ✅ · Security ➖ (N/A — dados estáticos normativos) · Documentation ✅

#### Observações ao @dev

O trabalho é de qualidade alta e a disciplina de Artigo IV é exemplar: catálogo gerado por
script versionado com verificação de SHA-256, zero valores tocados, `null` preservado, e o
resolvedor sem uma única menção a fabricante. A descoberta e migração da 5ª suíte
(`tests/api/modulos-mod-qt.test.ts`), fora de todo artefato de planejamento, foi registrada
e é reconhecida.

**— Quinn, guardião da qualidade 🛡️**
