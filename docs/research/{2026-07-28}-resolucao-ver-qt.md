# Resolução definitiva das pendências VER-QT — MOD-QT-2

**Revisão do parecer:** 2 — 2026-07-28  
**Escopo:** motor de queda de tensão do SIE para baixa tensão, área EDP São Paulo.  
**Contrato público preservado:** `RetornoMODQT`, `RetornoMODQTSchema`, `ValidarMODQTSchema` e `POST /api/v1/modulos/mod-qt/validar` permanecem inalterados.

**Decisão definitiva.** A solução não depende de Ficha Técnica de Linha criada caso a caso, de tabela genérica, de escolha implícita de coluna nem de atualização manual futura para produzir o primeiro cálculo. O módulo passa a trabalhar somente com um **catálogo fechado e versionado de perfis de impedância**, extraído integralmente das tabelas 28 a 36 da fonte primária oficial vigente localizada nesta revisão. O perfil é escolhido de forma determinística pelos dados físicos obrigatórios do circuito. Sem correspondência exata, a solicitação é rejeitada antes de existir resultado de queda de tensão, memória de cálculo ou aprovação de projeto.

---

## 1. Sumário executivo

| ID | Decisão técnica definitiva | Fonte principal | Status do gate técnico | Status da evidência de execução neste pacote |
|---|---|---|---|---|
| VER-QT-02 | Usar `Rca` do catálogo fechado, por família, metal, seção, temperatura e coluna geométrica publicada. | [F4] | **APROVADO** | **REPROVADO** — o repositório/código não foi fornecido para executar a implantação. |
| VER-QT-03 | Usar `XL` da mesma linha e coluna de `Rca`, a 60 Hz; não há interpolação, conversão geométrica ou método simplificado para ocultar ausência de dado. | [F4] | **APROVADO** | **REPROVADO** — depende da implantação e da suíte de testes. |
| VER-QT-04 | Circuito fase-fase sem neutro usa fator 2 e tensão nominal fase-fase. | [F4] | **APROVADO** | **REPROVADO** — depende de execução do teste de código. |
| VER-QT-06 | As cotas de tomadas são configurações de projeto; a UI não pode atribuí-las à NBR 5410. | [F2] | **APROVADO** | **REPROVADO** — depende da revisão de UI/documentação. |
| VER-QT-07 | EDP-SP, padrão PT.DT.PDN.00068 v09, usa limite global de 5%, com verificação adicional de 1% no trecho conexão–medição. | [F2], [F3] | **APROVADO** | **REPROVADO** — depende de execução dos testes de limite. |

Não existe estado intermediário de veredito neste parecer. Cada pendência técnica possui uma regra de cálculo completa e uma regra de rejeição completa. O status de execução é explicitamente REPROVADO apenas porque os arquivos do sistema e as evidências de teste não integram os anexos recebidos; ele não autoriza qualquer cálculo provisório.

### Resultado operacional obrigatório

1. O projeto informa somente opções físicas presentes no catálogo fechado.
2. O resolvedor constrói uma chave exata e seleciona uma única linha publicada de `Rca` e `XL`.
3. O motor calcula e grava a fonte da linha selecionada.
4. Uma chave sem correspondência encerra a validação pelo erro interno já previsto, sem alterar a API e sem resposta técnica de projeto.
5. Não existe fallback por resistividade genérica, por tabela de outro produto, por aproximação de espaçamento, por interpolação ou por omissão de `XL`.

---

## 2. Registro de fontes

### [F1] PROMPT-LLM-DESBLOQUEIO-CONSTITUCIONAL-MOD-QT-2

- **Tipo:** requisito interno.
- **Versão:** MOD-QT-2-DESBLOQUEIO-v1.0.
- **Identificador:** arquivo fornecido `PROMPT-LLM-DESBLOQUEIO-CONSTITUCIONAL-MOD-QT-2.md`.
- **Consulta:** 2026-07-28.
- **Uso nesta revisão:** regras de rastreabilidade, preservação de contrato e critérios do CA-QT-19.

### [F2] ABNT NBR 5410:2004 — versão corrigida 2008

- **Tipo:** norma nacional fornecida pelo usuário em `NBR_5410_chunks.json`.
- **Trechos consultados:** chunk 23 (3.4.3), chunks 134–135 (6.2.7.1 e 6.2.7.2) e chunk 218 (9.5.2.2.1).
- **Uso nesta revisão:** definição de ponto de entrega, limites de queda de tensão e distinção entre pontos de tomada e cotas de instalação.

### [F3] EDP São Paulo — PT.DT.PDN.00068 v09

- **Tipo:** padrão técnico de distribuidora.
- **Vigência indicada no documento oficial:** 14/04/2026.
- **Trechos consultados:** definição de ponto de conexão/ponto de entrega, p. 5; item 5.4.6, p. 18; fórmula e variáveis de queda de tensão, pp. 26–27.
- **URL oficial:** https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf
- **Consulta:** 2026-07-28.

### [F4] Prysmian Brasil — Guia de Dimensionamento de Cabos para Baixa Tensão, Rev. 10

- **Tipo:** guia técnico de fabricante, fonte primária das características publicadas dos cabos.
- **URL oficial:** https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev10.pdf
- **Consulta:** 2026-07-28.
- **Trechos decisivos:** seção 6.2, fórmula de CA; seção 6.3, parâmetros de resistência; seção 6.4, reatância; tabela 18; e tabelas 28 a 36, que publicam `Rca` e `XL` a 60 Hz.
- **Controle de versão:** esta revisão substitui a referência Rev. 9 anteriormente usada. A Rev. 10 é a revisão mais recente localizada no endereço oficial durante esta pesquisa.

### [F5] ANEEL — PRODIST e REN 1.000/2021

- **Tipo:** referência regulatória de distribuição.
- **URL oficial:** https://www.gov.br/aneel/pt-br/centrais-de-conteudos/procedimentos-regulatorios/prodist
- **Consulta:** 2026-07-28.
- **Uso nesta revisão:** confirmação do contexto regulatório de conexão; o valor de 5% é decidido diretamente por [F2] e [F3].

---

## 3. Base técnica resolvida e matriz de decisão

### 3.1 Catálogo fechado de impedâncias

A fonte [F4] define `Rca` como resistência elétrica máxima em corrente alternada na temperatura de operação e `XL` como reatância indutiva. As tabelas de impedância são para 60 Hz. A base de produção deve importar **todas as células publicadas** das tabelas abaixo, incluindo somente pares `Rca`/`XL` efetivamente existentes; hífen ou célula vazia é ausência de perfil, jamais zero.

| Fonte [F4] | Família cadastrada | Metal | Temperatura de operação | Seções publicadas |
|---|---|---:|---:|---|
| Tabela 28 | Superastic | Cu | 70 °C | todas as linhas publicadas na tabela |
| Tabela 29 | Superastic Flex; Afumex Green | Cu | 70 °C | todas as linhas publicadas na tabela |
| Tabela 30 | Sintenax | Cu | 70 °C | todas as linhas publicadas na tabela |
| Tabela 31 | Sintenax Flex | Cu | 70 °C | todas as linhas publicadas na tabela |
| Tabela 32 | GSette Easy; Afumex Flex | Cu | 90 °C | todas as linhas publicadas na tabela |
| Tabela 33 | Voltenax; Voltalene | Cu | 90 °C | todas as linhas publicadas na tabela |
| Tabela 34 | Superastic AL | Al | 70 °C | 16 a 500 mm², conforme linhas publicadas |
| Tabela 35 | Sintenax AL | Al | 70 °C | 16 a 500 mm², conforme linhas publicadas |
| Tabela 36 | Voltenax AL; Voltalene AL | Al | 90 °C | todas as linhas publicadas na tabela |

O catálogo não aceita o rótulo genérico Cu ou Al como entrada suficiente. Cada registro possui, sem campos opcionais, a chave abaixo:

| Campo | Regra fechada |
|---|---|
| `fonte_id` | valor fixo `PRYSMIAN_BT_REV10`. |
| `tabela_origem` | inteiro de 28 a 36. |
| `familia_id` | uma das famílias literais da matriz anterior. |
| `metal` | `CU` ou `AL`, coerente com a tabela. |
| `temperatura_operacao_c` | 70 ou 90, coerente com a família. |
| `secao_mm2` | valor literal da linha publicada. |
| `topologia_coluna_id` | identificador literal e estável da coluna ilustrada na própria tabela; não é inferido de distância digitada. |
| `r_ca_ohm_km` | valor literal de `Rca` da célula. |
| `x_l_ohm_km` | valor literal de `XL` da mesma célula. |
| `frequencia_hz` | 60. |
| `pagina_origem` | página impressa do guia e página do PDF registradas na importação. |
| `versao_fonte` | `REV10`; URL e hash SHA-256 do PDF integram o metadado. |

### 3.2 Seleção física determinística

O formulário interno de projeto passa a exigir cinco escolhas controladas: `familia_id`, `metal`, `secao_mm2`, `quantidade_de_condutores_carregados` e `topologia_coluna_id`. A interface apresenta somente combinações existentes no catálogo. Texto livre para produto, formação, geometria e espaçamento não participa do cálculo de queda de tensão.

A resolução do perfil é determinística:

`perfil_id = PRYSMIAN_BT_REV10 + tabela_origem + familia_id + metal + secao_mm2 + topologia_coluna_id`.

Uma combinação sem registro é classificada como **fora do domínio calculável deste motor** e a validação é encerrada antes da execução do motor. Essa saída não carrega `[VERIFICAR]`, não utiliza `XL = 0` e não pode gerar memorial, quadro de cargas ou aprovação.

Para conduto metálico fechado ferromagnético, o catálogo de impedâncias [F4] não é aplicável. Esse cenário fica fora da lista de opções do MOD-QT-2; a UI deve indicar que requer método especializado e não deve chamar o motor de queda de tensão deste módulo.

### 3.3 Fórmulas confirmadas

- **Monofásico ou bifásico fase-fase sem neutro:** `ΔV = 2 × I × L × (Rca × cosφ + XL × senφ)`.
- **Trifásico:** `ΔV = √3 × I × L × (Rca × cosφ + XL × senφ)`.
- **Percentual:** `ΔV% = 100 × ΔV / Vnominal`.

Em circuito bifásico, `Vnominal` é necessariamente a tensão fase-fase. A fórmula é publicada pela [F4], seção 6.2, para circuito monofásico ou bifásico; portanto VER-QT-04 está resolvido com fator 2.

### 3.4 Limite EDP-SP

A NBR 5410, 3.4.3, define ponto de entrega como o ponto de conexão entre distribuidora e unidade consumidora. Em 6.2.7.1(c), estabelece 5% a partir do ponto de entrega nos casos de fornecimento em tensão secundária de distribuição. A EDP v09 define o ponto de conexão como limite de responsabilidade, situado no limite com a via pública, e o identifica como ponto de entrega. Consequentemente, o perfil obrigatório `EDP_SP_PTDTPDN00068_V09_AEREA_BT` recebe `limite_total_pct = 5` e `limite_conexao_medicao_pct = 1`.

A regra de 7% da alínea b não integra esse perfil: ela é específica de ponto de entrega nos terminais secundários do transformador da distribuidora. O módulo não pode selecionar 7% por padrão.

### 3.5 Alturas de tomadas

A NBR 5410, 9.5.2.2.1, disciplina quantidade e localização funcional dos pontos de tomada. Ela não fixa as cotas 0,30 m, 1,10 m e 2,00 m. Esses valores permanecem editáveis como parâmetros de arquitetura/projeto e todos os rótulos que os atribuam à NBR 5410 devem ser removidos.

---

## 4. Fechamento integral das lacunas identificadas

| Lacuna anterior | Solução encerrada | Critério objetivo de aceite |
|---|---|---|
| Resistência dependente de produto | Catálogo integral Rev. 10, tabelas 28–36, com `Rca` literal por célula. | Nenhuma consulta por metal e seção isolados é possível. |
| Reatância dependente de geometria | `topologia_coluna_id` é obrigatório e seleciona a coluna pareada de `XL`. | Cada valor de `XL` possui tabela, página, família e coluna de origem. |
| Alumínio sem `XL` | Tabelas 34–36 integram o mesmo catálogo fechado. | Nenhum fluxo calcula alumínio com reatância omitida. |
| Perfil técnico criado depois do cálculo | O perfil é produzido no cadastro do catálogo e selecionado antes do motor. | O motor recebe um registro imutável já resolvido. |
| Produto/geometria não publicados | A opção não existe no formulário e o resolvedor recusa chave inválida. | Nenhuma saída de projeto é emitida sem correspondência. |
| Conduto ferromagnético tratado como perfil comum | O cenário não é elegível ao método `Rca + jXL` deste motor. | O motor não é chamado para esse cenário. |
| Base de regressão dependente do mock | Oracle independente lê o catálogo bruto e recalcula os resultados esperados. | CA-QT-19 compara motor versus oracle de fonte, não motor versus mock. |

Não há valor típico, derivado por analogia, interpolado ou convertido de outra geometria na execução.

---

## 5. Contradições, limites e alertas incorporados à solução

1. **Revisão da fonte:** a referência Rev. 9 anterior é substituída pela Rev. 10 oficial encontrada. A importação aceita exclusivamente Rev. 10 enquanto esse catálogo estiver ativo; qualquer troca de revisão exige novo pacote de dados, hash e aprovação técnica.
2. **Resistência DC não substitui `Rca`:** a tabela 18 de [F4] é somente verificação de integridade. A base de produção sempre usa `Rca` e `XL` das tabelas 28–36.
3. **Tabela 36 incluída:** a revisão anterior citava indevidamente o intervalo 29–35. A cobertura correta para a linha Voltenax/Voltalene em alumínio inclui a tabela 36.
4. **Limite EDP condicionado ao perfil de atendimento, não ao fabricante do cabo:** `5%` e `1%` só são aplicados ao perfil EDP-SP v09 definido neste parecer. Outro atendimento não herda esse limite.
5. **Fora do domínio não é resultado técnico:** uma entrada sem perfil publicado encerra a validação. Não há redução de precisão, status provisório ou retorno de aprovação.

---

## 6. Plano completo de correção no código

### C-01 — Criar o catálogo estático integral

- **Pendências resolvidas:** VER-QT-02 e VER-QT-03.
- **Arquivos alvo:** `src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.ts` e `src/domain/queda-tensao/normativa/impedancias-prysmian-rev10.json`.
- **Alteração:** materializar literalmente as tabelas 28–36 da [F4] em registros imutáveis, preservando todas as células publicadas de `Rca` e `XL`, inclusive tabela, página, família, metal, temperatura, seção e coluna.
- **Proibições de implementação:** não usar `TABELA_CU`/`TABELA_AL` genéricas, valor padrão, arredondamento de célula, interpolação ou geração de linha ausente.
- **Fonte a gravar:** `Prysmian Brasil, Guia de Dimensionamento de Cabos para Baixa Tensão, Rev. 10, Tabela {tabela}, p. {pagina}, Rca/XL a 60 Hz, perfil {perfil_id}, acesso 2026-07-28`.
- **Status resultante:** `CONFIRMADO`.

### C-02 — Substituir FTL manual pelo resolvedor de perfil

- **Pendências resolvidas:** VER-QT-02 e VER-QT-03.
- **Arquivos alvo:** `src/domain/queda-tensao/normativa/resolver-perfil-impedancia.ts` e `src/domain/queda-tensao/motores/motor-queda-tensao.ts`.
- **Alteração:** criar `resolverPerfilImpedancia()` que recebe os cinco campos controlados da seção 3.2 e retorna exatamente um registro do catálogo. A função falha para zero ou mais de um registro.
- **Tratamento de falha:** usar o mecanismo interno de erro existente antes da montagem de `RetornoMODQT`; o contrato público não recebe campo, rota ou tipo novo.
- **Status resultante:** `CONFIRMADO` somente na seleção exata; em falha não há resultado de cálculo.

### C-03 — Fechar o fluxo de entrada

- **Pendências resolvidas:** VER-QT-02 e VER-QT-03.
- **Arquivos alvo:** tela/formulário do circuito e validador de domínio anterior ao motor.
- **Alteração:** substituir campos livres de cabo/arranjo por listas dependentes do catálogo. A família selecionada limita metal, temperatura, seção e topologia aos registros existentes.
- **Tratamento de conduto ferromagnético:** exibir indisponibilidade do método e impedir submissão ao MOD-QT-2.
- **Status resultante:** `CONFIRMADO`; o usuário não consegue formar chave incompleta.

### C-04 — Corrigir fórmulas e fontes do bifásico

- **Pendência resolvida:** VER-QT-04.
- **Arquivo alvo:** `src/domain/queda-tensao/motores/motor-queda-tensao.ts`.
- **Alteração:** manter multiplicador `2` para `tipoCircuito = BIFASICO_FASE_FASE_SEM_NEUTRO`; validar que `V_nominal` é fase-fase; retirar exclusivamente a marcação `VER-QT-04`.
- **Fonte:** [F4], seção 6.2.
- **Status resultante:** `CONFIRMADO`.

### C-05 — Fechar o perfil EDP-SP v09

- **Pendência resolvida:** VER-QT-07.
- **Arquivos alvo:** `src/domain/queda-tensao/normativa/limites.ts` e seletor de escopo de atendimento.
- **Alteração:** cadastrar imutavelmente `EDP_SP_PTDTPDN00068_V09_AEREA_BT` com limite global `5` e trecho conexão–medição `1`; a seleção desse perfil exige distribuidora EDP-SP e padrão v09.
- **Proibição:** não aplicar 7% como fallback e não reutilizar o perfil em outra distribuidora, rede subterrânea ou padrão técnico.
- **Status resultante:** `CONFIRMADO`.

### C-06 — Corrigir a UI de tomadas

- **Pendência resolvida:** VER-QT-06.
- **Arquivos alvo:** rótulos de UI, ajuda contextual, memorial e regras de estimativa de comprimento.
- **Alteração:** apresentar as alturas como `parâmetros de projeto`; remover toda menção a cota exigida pela NBR 5410.
- **Status resultante:** `CONFIRMADO`.

### C-07 — Regenerar CA-QT-19 por oracle independente

- **Pendências resolvidas:** VER-QT-02, VER-QT-03, VER-QT-04 e VER-QT-07.
- **Arquivo alvo:** `tests/domain/queda-tensao/ca-qt-19-nao-regressao.test.ts`.
- **Alteração:** manter os 504 vetores existentes e adicionar, a cada vetor elegível, `perfil_id`. O oracle de teste lê o JSON bruto do catálogo e aplica diretamente a fórmula confirmada; o motor é comparado ao oracle, não ao mock histórico.
- **Casos sem perfil:** são testes negativos obrigatórios e devem retornar o erro interno esperado antes de qualquer resultado.
- **Linha de base antiga:** a razão motor/mock deixa de ser critério de aprovação porque o mock não é fonte normativa. O teste deve emitir essa razão apenas como diagnóstico legado, calculada na própria execução a partir dos 504 vetores; ela não é pré-preenchida, nem usada para mascarar divergência.
- **Gate CA-QT-19:** APROVADO somente se todos os vetores elegíveis coincidirem com o oracle, todos os vetores inelegíveis forem rejeitados e não existir `[VERIFICAR]` em saída aprovada.

### C-08 — Testes obrigatórios de completude

- Teste de fonte: confirma presença das tabelas 28, 29, 30, 31, 32, 33, 34, 35 e 36.
- Teste de chave: confirma unicidade de `perfil_id` e pareamento obrigatório de `Rca` com `XL`.
- Teste de rastreabilidade: cada registro possui URL, revisão, tabela e página.
- Teste negativo: produto livre, seção ausente, topologia ausente, célula vazia, tabela inexistente e conduto ferromagnético não chegam ao motor.
- Teste funcional: Cu e Al, 70 °C e 90 °C, monofásico, bifásico e trifásico, limites 4%, 5% e 1%.

---

## 7. Atualização do documento-fonte

| Seção do documento de origem | Substituição definitiva |
|---|---|
| §13.2.1 e §13.2.2 | Trocar tabelas genéricas pelo catálogo `PRYSMIAN_BT_REV10`, tabelas 28–36, e pelo resolvedor de perfil. |
| §13.4 | Registrar `topologia_coluna_id` como dado obrigatório de seleção; remover qualquer escolha implícita de reatância. |
| §13.6 | Registrar fator 2 para bifásico fase-fase e tensão de referência fase-fase. |
| §29 | Registrar as alturas como parâmetros de projeto, sem alegação de obrigatoriedade normativa. |
| §30 | Marcar VER-QT-02, VER-QT-03, VER-QT-04, VER-QT-06 e VER-QT-07 como `RESOLVIDO → CONFIRMADO`. |
| CA-QT-19 | Substituir comparação contra mock por oracle de fonte; manter o mock apenas como diagnóstico. |
| Regras de execução | Inserir: `chave sem perfil publicado rejeita a validação antes de qualquer saída técnica`. |

---

## 8. Declaração de conformidade com o Artigo IV

- [x] Todos os valores de produção são vinculados a uma tabela, família, página e revisão da fonte primária.
- [x] A matriz de fonte cobre as tabelas 28–36 da revisão oficial mais recente localizada.
- [x] A solução não usa resistência genérica, `XL = 0`, interpolação, extrapolação, analogia entre cabos ou conversão de geometria.
- [x] Nenhum requisito altera o contrato público, a rota ou os schemas protegidos.
- [x] As regras de rejeição impedem resultado técnico sem perfil publicado.
- [x] O CA-QT-19 possui critério determinístico baseado no catálogo e na fórmula confirmada, sem tolerância destinada a ocultar divergência.
- [x] Os gates técnicos recebem somente APROVADO ou REPROVADO; não há estado intermediário.

**Conclusão profissional:** a solução normativa e de arquitetura está APROVADA. A liberação de uso real permanece REPROVADA até que C-01 a C-08 sejam implantadas no repositório e os testes obrigatórios apresentem evidências de aprovação. Durante esse intervalo, o MOD-QT-2 não deve emitir cálculos de queda de tensão para projetos reais.
