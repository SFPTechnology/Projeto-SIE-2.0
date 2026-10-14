# PRD — Módulo de Dimensionamento de Condutores (MOD-DC)

**Produto:** SIE — Sistema de Instalações Elétricas
**Módulo:** MOD-DC v3.0 (substitui integralmente o MOD-DC-v2.0)
**Tipo:** PRD Brownfield (integração a sistema existente)
**Autor:** Morgan (@pm) — AIOX
**Data:** 2026-07-12
**Status:** Draft — aguardando validação (@po) e decisão arquitetural (@architect)
**Documento-base:** `Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` (MOD-DC-v3.0, 2026-07-11)

---

## 1. Introdução e Contexto do Projeto Existente

### 1.1 Análise do sistema atual

O SIE é um sistema de engenharia assistida para projetos de instalações elétricas de baixa tensão, em conformidade com a ABNT NBR 5410:2004 e o padrão EDP São Paulo (PT.DT.PDN.00068 v09). Módulos já existentes e operacionais:

| Módulo | Status | Relação com o MOD-DC |
|---|---|---|
| Cargas | Operacional | Upstream indireto — **NÃO TOCAR** |
| Demanda (fórmula EDP) | Operacional | Upstream indireto — **NÃO TOCAR** |
| Circuitos (+ adaptador 1:1 provisório) | Operacional | **Upstream direto** — fornece `CircuitoParaDimensionamento` |
| IB (corrente de projeto) | Operacional | **Upstream direto** — fornece IB com harmônicas |
| Categoria de Entrada (EDP, Tabelas 001/002) | Operacional | Contexto EDP — **NÃO TOCAR** |
| Queda de Tensão (MOD-QT) | Operacional | **Downstream/integração** — critério C5 |
| Curto-Circuito (MOD-CC) | Futuro | Contrato + bloqueio de status (C3) |
| Seccionamento Automático (MOD-SEC) | Futuro | Contrato + bloqueio de status (C4) |
| Proteção (MOD-PROT) | Futuro | Contrato; In/I2 como entrada ou sugestão |

**Stack observado no repositório brownfield (2026-07-12):** TanStack Start + TypeScript + React 19 + IBM Carbon Design System, Supabase/PostgreSQL, Vitest, ESLint e TypeScript strict no app `sistema-de-instala-es-el-tricas-sie-main`.

**Atenção arquitetural:** o documento-base cita FastAPI + Pydantic v2 + SQLAlchemy 2.x e motor Python com `Decimal`, mas essa stack não é a stack principal observada no código carregado. Este PRD define os contratos funcionais e normativos do MOD-DC; a decisão de implementar como módulo TypeScript nativo do app atual, serviço Python separado ou adaptação híbrida fica bloqueada para validação de @architect antes das stories DC-1/DC-7.

### 1.2 Motivação (por que v3.0 e não evoluir o v2.0)

Auditoria técnica identificou que o MOD-DC-v2.0 **contraria a NBR 5410, item 6.2.6.1.2**: declarava apenas 3 dos 6 critérios cumulativos de dimensionamento e emitia status `DIMENSIONADO` com curto-circuito, seccionamento e queda de tensão não verificados. Defeitos adicionais confirmados no v2:

- Fatores de temperatura da Tabela 40 com valores **errados** (ex.: PVC 25 °C → 1,04 em vez de 1,06).
- Faixas de agrupamento da Tabela 42 erradas (10-12/13-16/17-20 em vez de 9-11/12-15/16-19/>20).
- Condutores carregados por `num_fases` isolado — erra o caso bifásico com neutro (2F+N = 3 carregados) e ignora TH3.
- Verificação de sobrecarga tautológica (I2 = 1,45·In embutido sem sustentação normativa).
- Alumínio "elevado a 16 mm² com alerta" quando a norma o **proíbe** em contexto residencial (6.2.3.8).
- In > Iz tratado como "ATENÇÃO" não bloqueante em vez de reprovação.

Um sistema que apresenta como completo um dimensionamento com critérios obrigatórios pendentes gera **risco de segurança e responsabilidade técnica**. Este é o problema central que o MOD-DC v3.0 resolve.

### 1.3 Fontes e limites de conhecimento

As fontes autorizadas para este PRD seguem a hierarquia do documento-base:

1. `NBR_5410_chunks.json` — ABNT NBR 5410:2004, fonte normativa primária para a instalação.
2. `PT_DT_PDN_00068_V9_chunks.json` — padrão técnico EDP São Paulo para fornecimento em tensão secundária, aplicável somente nos limites definidos na seção de hierarquia.
3. `04_condutores_markdown_limpo.md` e material `06_dimensionamento` — fontes técnicas explicativas do Guia EM da NBR 5410. Estes materiais usam numeração da edição 1997; é proibido copiar essa numeração para código, dados, UI ou documentação normativa.
4. `PROMPT-DIMENSIONAMENTO-CONDUTORES-v2.md` — artefato histórico, não é fonte normativa; só pode ser usado quando confirmado pelos anexos.

É proibido consultar internet, catálogos, normas não anexadas ou conhecimento externo para completar valores normativos. Qualquer lacuna vira `[VERIFICAR]` com fonte necessária declarada e bloqueio quando afetar critério obrigatório.

### 1.4 Hierarquia e aplicabilidade das fontes

1. A NBR 5410:2004 é a referência geral obrigatória para toda a instalação.
2. O padrão EDP PT.DT.PDN.00068 v09 aplica-se somente à área de concessão da EDP São Paulo, a unidades consumidoras individuais com carga instalada até 75 kW, ligadas em redes aéreas secundárias de distribuição.
3. Os requisitos EDP de condutores restringem-se ao ramal de entrada e ao trecho ponto de conexão → medição; não se aplicam aos circuitos internos da instalação.
4. Requisitos NBR + EDP são cumulativos quando ambos forem aplicáveis.
5. Exemplos do material explicativo não são regra. Divergências de numeração de tabela resolvem-se sempre a favor da edição 2004 da NBR 5410.
6. Conflitos não resolvíveis pelos anexos recebem status `CONFLITANTE` ou `[VERIFICAR]` e bloqueiam aprovação do requisito afetado.

### 1.5 Premissas operacionais

- Sistema-alvo típico: trifásico estrela 220/127 V, mas o motor deve aceitar monofásico, bifásico com ou sem neutro e trifásico com ou sem neutro.
- Frequência 60 Hz.
- Regime permanente e fator de carga 100%, conforme condição das tabelas 36–39.
- Cabos com tensão nominal até 0,6/1 kV, não armados.
- Circuitos chegam do módulo de Circuitos com IB já calculado.
- VA é usado diretamente, preservando a disciplina INC-01; o MOD-DC nunca divide VA por fator de potência para recalcular carga.
- Tensão jamais é assumida, preservando a disciplina INC-04; ausência de tensão gera erro bloqueante.

### 1.6 Glossário

- **IB:** corrente de projeto do circuito, incluindo componentes harmônicas quando declaradas.
- **Iz:** capacidade de condução de corrente dos condutores nas condições reais de instalação.
- **In:** corrente nominal ou corrente de ajuste do dispositivo de proteção.
- **I2:** corrente convencional de atuação ou de fusão do dispositivo de proteção; depende da norma do dispositivo.
- **Método de referência:** A1, A2, B1, B2, C, D, E, F ou G, obtido a partir do tipo de linha da Tabela 33.
- **Condutores carregados:** condutores efetivamente percorridos por corrente para fins térmicos; PE nunca conta, PEN conta como neutro.
- **FCT / FCS / FRS / FCA:** fatores de correção de temperatura ambiente, temperatura do solo, resistividade térmica do solo e agrupamento.
- **PE / PEN:** condutor de proteção / condutor com função combinada proteção + neutro.
- **TH3:** taxa de terceira harmônica e seus múltiplos na corrente de fase.

---

## 2. Objetivos e Métricas de Sucesso

### 2.1 Objetivo do produto

Determinar, para cada circuito BT, a seção normalizada dos condutores de fase, neutro e proteção (PE/PEN), atendendo **simultaneamente aos seis critérios** da NBR 5410:2004 (6.2.6.1.2), com resultados **auditáveis, reproduzíveis e rastreáveis**, e **nunca** apresentando como completo um dimensionamento com critérios pendentes.

### 2.2 Os seis critérios (núcleo funcional)

| # | Critério | Fonte NBR 5410 | Tratamento no MOD-DC |
|---|---|---|---|
| C1 | Capacidade de condução de corrente (Iz) com fatores de correção | 6.2.5, 6.2.6.1.2 a) | **Calculado** |
| C2 | Proteção contra sobrecargas (IB ≤ In ≤ Iz; I2 ≤ 1,45·Iz) | 5.3.4, 6.3.4.2 | **Verificado** (In pode ser sugestão) |
| C3 | Proteção contra curto-circuito (∫i²dt ≤ k²S²) | 5.3.5, 6.3.4.3 | **Pendência explícita** → `AGUARDANDO-CC` |
| C4 | Seccionamento automático (TN/IT) | 5.1.2.2.4 | **Pendência explícita** → `AGUARDANDO-SECCIONAMENTO` ou `NAO-APLICAVEL` (TT) |
| C5 | Limites de queda de tensão | 6.2.7 | **Integração MOD-QT** → `AGUARDANDO-QT` |
| C6 | Seções mínimas por utilização (Tabela 47) | 6.2.6.1.1 | **Calculado** |

Seção final de fase = **maior** seção entre os critérios verificados, revalidada contra todos. Status terminal de sucesso: `DIMENSIONAMENTO-PARCIAL` (pendências nomeadas) ou `VERIFICADO-COMPLETO` (todos os critérios aplicáveis aprovados).

### 2.3 Métricas de sucesso

| Métrica | Alvo |
|---|---|
| Critérios de aceite CA-DC-01 a CA-DC-25 | 100% verdes (exceto `xfail` documentados) |
| Cobertura dos 6 critérios na UI e no motor | 6/6 modelados, nenhum omitido |
| Circuitos com status de completude tendo pendência C3/C4/C5 | **Zero** (CA-DC-09) |
| Performance: lote com 44 circuitos do proj-1 | < 2 s (CA-DC-11) |
| Regressão da base normativa (amostra Tabela 36) | 100% conferente (CA-DC-23) |
| Acessibilidade | WCAG 2.1 AA, contraste ≥ 4,5:1 validado por teste (CA-DC-22) |
| Referências a numeração de tabelas ed. 1997 | Zero no código/dados/UI (CA-DC-25) |

---

## 3. Requisitos

### 3.1 Requisitos Funcionais (FR)

**Motor de cálculo**

- **FR1:** Calcular C1 (capacidade de corrente) via Tabelas 36–39, com chave de consulta completa e obrigatória `(tabela, material, isolação, método, nº condutores carregados, seção)`; consulta incompleta → `ERRO-CONSULTA-INCOMPLETA`.
- **FR2:** Determinar o número de condutores carregados exclusivamente pela **Tabela 46** (esquema completo: nº fases + neutro + TH3), incluindo 2F+N = 3 carregados e fator 0,86 para neutro carregado (3F+N com TH3 > 15%). Nunca derivar de `num_fases` isolado.
- **FR3:** Aplicar fatores de correção: temperatura (Tabela 40, blocos ambiente/solo derivados do método), resistividade térmica do solo (Tabela 41, só método D), agrupamento (Tabelas 42–45, faixas 9-11/12-15/16-19/>20 como intervalos). Temperatura fora dos pontos tabelados sem regra de interpolação autorizada → `ERRO-FATOR-NAO-ENCONTRADO`.
- **FR4:** Grupos de condutores não semelhantes: aplicar **F = 1/√n**, substituindo integralmente qualquer fator tabelado (não cumulativo); alertar o projetista quando F < 0,30.
- **FR5:** Suportar isenção de agrupamento por espaçamento > 2× diâmetro (nota 2, Tabela 42) e exclusão de circuitos com IB ≤ 30% da capacidade corrigida (6.2.5.5.2) — ambas como opções declaráveis, justificadas e rastreadas.
- **FR6:** Verificar C2 (sobrecarga, 5.3.4.1): a) IB ≤ In ≤ Iz corrigida; b) I2 ≤ 1,45·Iz com **I2 real** (entrada do MOD-PROT ou do projetista, com fonte). I2 ausente → `PENDENTE-I2`. Proibido assumir I2 = 1,45·In. Parâmetro `regime_sobrecarga_severo` transforma b) em I2 ≤ Iz.
- **FR7:** Aplicar C6 (seções mínimas, Tabela 47 completa, incluindo condutores nus e linhas flexíveis, com notas 1–4). Mapeamento SIE: ILU → 1,5 mm² Cu; TUG/TUE → 2,5 mm² Cu (tomadas são circuitos de força).
- **FR8:** Dimensionar neutro conforme 6.2.6.2 e Tabela 48 (redução só com as 5 condições simultâneas); TH3 > 33% → `VERIFICAR-NEUTRO-HARMONICAS` bloqueante.
- **FR9:** Dimensionar PE conforme Tabela 58 (≤16 → igual; 16<S≤35 → 16; >35 → S/2 arredondado à seção padronizada) e PEN (≥10 mm² Cu / 16 mm² Al, só TN-C, instalação fixa).
- **FR10:** Bloquear alumínio fora dos contextos de 6.2.3.8 (`ERRO-MATERIAL-NAO-ADMITIDO` em residencial; industrial ≥ 16 mm² com BA5 e fonte própria; comercial ≥ 50 mm² BD1/BA5; proibido em BD4). Campos `tipo_instalacao` e condições BA/BD obrigatórios quando material = Al.
- **FR11:** Suportar múltiplos trechos de percurso (6.2.5.8), dimensionando pela condição mais desfavorável, com rastreio do trecho decisivo.
- **FR12:** Condutores em paralelo: quando nenhuma seção da série atender, emitir `REQUER-ESTUDO-PARALELO` — nunca dimensionar automaticamente.
- **FR13:** Validar identificação por cores função × cor (6.1.5.3 + EDP ramal): neutro azul-clara, PE verde/verde-amarela exclusivas, PEN azul-clara com anilhas → violação = `ERRO-COR-FUNCAO`.
- **FR14:** Implementar máquina de estados por circuito: `RASCUNHO → DADOS-INCOMPLETOS → DIMENSIONAMENTO-PARCIAL → VERIFICADO-COMPLETO | REPROVADO | REQUER-ESTUDO-PARALELO`, com pendências nomeadas (`AGUARDANDO-QT/CC/SECCIONAMENTO/PROTECAO`, `PENDENTE-I2`, `VERIFICAR-NEUTRO-HARMONICAS`). `VERIFICADO-COMPLETO` exige pendências vazias e todos os critérios `APROVADO` ou `NAO-APLICAVEL`.
- **FR15:** Revalidar **todos** os critérios sempre que um retorno downstream (QT/CC/SEC) exigir seção maior, atualizando o critério decisivo.

**Integrações e API**

- **FR16:** Publicar contratos formais de entrada (`CircuitoParaDimensionamento`) e saída (`ResultadoDimensionamento`) conforme §14 do documento-base, preservando os campos, seções por critério, verificações tri-estado e objeto `rastreio`. A representação técnica concreta (Pydantic, Zod/TypeScript ou equivalente) deve seguir a decisão AD-DC-01, sem alterar o contrato funcional.
- **FR17:** Expor contratos de API/rotas server para dimensionar circuito individual e lote (`POST .../dimensionar`, `POST .../dimensionar-lote`), consulta de resultados com resumo por estado/critério (`GET .../dimensionamento`), consulta da base normativa (`GET /api/v1/tabelas/...` com fonte e status por linha), e recepção de retornos downstream (`POST .../retorno-qt|retorno-cc|retorno-seccionamento`) com revalidação automática. A tecnologia concreta do endpoint deve seguir a decisão arquitetural AD-DC-01.
- **FR18:** Integrar com MOD-QT (C5): enviar seção candidata + parâmetros, receber `{atende, queda_percentual, limite_aplicado, fonte}`; sem retorno → `AGUARDANDO-QT`. Limites: 4% circuitos terminais; 5%/7% conforme origem; EDP 1% **somente** no ramal de entrada.
- **FR19:** Publicar contratos com MOD-CC, MOD-SEC e MOD-PROT (futuros) com bloqueio de status enquanto não houver retorno; valores de k da Tabela 30 persistidos.

**UI (React + IBM Carbon)**

- **FR20:** Implementar a jornada completa: identificação → revisão de dados importados (badge de origem) → contexto normativo → sistema elétrico → condutor (material/isolação sem opção vazia) → tipo de linha (Tabela 33, método derivado e exibido) → influências → agrupamento → proteção → verificações por critério → comparação → resultado → pendências → aprovação técnica (autor, data, versão dos dados).
- **FR21:** DataTable Carbon de resultados com colunas `#, Circuito, Tipo, IB, C1, C2, C6, C5(QT), C3(CC), C4(SEC), S fase, S neutro, S PE, Iz corr., In, Status`; critério decisivo com destaque visual **e rótulo textual**; filtros, ordenação, agrupamento, edição em lote, exportação.
- **FR22:** Painel de detalhe com cadeia de cálculo completa e área expansível **"Como este resultado foi obtido"**, renderizada exclusivamente do objeto `rastreio` (nenhuma recomputação na camada visual).
- **FR23:** Comparação de cenários (Cu × Al quando admitido, PVC × EPR/XLPE, métodos, temperaturas, agrupamentos); a opção mais barata nunca é marcada como "melhor" automaticamente.
- **FR24:** Modos assistido e avançado; edição individual e em lote com padrões **visíveis e editáveis** (nunca implícitos no motor); overrides auditados (justificativa, autor, reversível, preserva valor calculado).
- **FR25:** Resumo do projeto: totais por estado, critério decisivo mais frequente, histograma de seções, aviso permanente enquanto houver pendência C3/C4/C5.

**Base normativa**

- **FR26:** Persistir base normativa versionada: `tabela_iz` (+`tabela_nbr`, `pagina_origem`, `chunk_id`), `fator_correcao_temperatura` (+`meio`), `fator_resistividade_solo` (nova), `fator_correcao_agrupamento` (faixas como intervalos), `secao_minima_aplicacao` (Tabela 47 integral), `secao_neutro_reduzida` (Tab. 48), `secao_pe` (Tab. 58), `fator_k_curto` (Tab. 30), `tipos_linha_tabela33`. Toda linha com `fonte`, `status_verificacao`, `versao_base_normativa`.
- **FR27:** Linhas com status `[VERIFICAR]` **bloqueiam** qualquer dimensionamento que dependa delas (`ERRO-TABELA-INCOMPLETA`) — nunca fallback silencioso.

### 3.2 Requisitos Não Funcionais (NFR)

- **NFR1 — Rastreabilidade (R-01):** todo valor calculado armazena fonte exata (documento, edição, item, tabela, linha, coluna, nota, página, chunk_id) e status de verificação. Referência genérica proibida.
- **NFR2 — Precisão (R-09):** comparações normativas com `Decimal` e tolerância explícita; valor original e arredondado registrados; nada aprovado por arredondamento.
- **NFR3 — Performance:** lote de 44 circuitos (proj-1) em < 2 s.
- **NFR4 — Acessibilidade:** WCAG 2.1 AA — contraste ≥ 4,5:1 validado programaticamente (proibido texto branco sobre `#fa4d56`), navegação por teclado, foco visível, leitor de tela, zoom 200%, erros acionáveis junto aos campos.
- **NFR5 — Idioma:** todo o produto (código de domínio, UI, mensagens, docs) em português do Brasil.
- **NFR6 — Segurança e responsabilidade técnica:** o sistema apoia e não substitui o responsável técnico — nunca emite "conformidade", diferencia sugestão de aprovação, registra versão de dados e motor em toda aprovação; sem `eval`, sem comandos de sistema, entradas validadas, dados normativos separados do código.
- **NFR7 — Arquitetura em camadas:** classes separadas (`ValidadorEntradas`, `RepositorioNormativo`, `MotorCapacidadeCorrente`, `MotorSobrecarga`, `MotorCondutorNeutro`, `MotorCondutorProtecao`, `SeletorSecaoNormalizada`, `GeradorRastreabilidade`, `VerificadorIndependente`, adaptadores de contrato). Proibido concentrar cálculo, persistência, UI e regra na mesma classe.
- **NFR8 — Dependências:** versões fixadas; toda biblioteca com finalidade documentada e teste independente de cálculo crítico; proibidas bibliotecas de sistemas de potência substituindo tabelas da norma; falha de biblioteca interrompe aprovação, nunca substitui silenciosamente.
- **NFR9 — Sem invenção normativa (Constitution Art. IV):** proibido inventar valores, fatores, limites ou tabelas; toda lacuna vira `[VERIFICAR]` visível e bloqueante quando obrigatória; fontes restritas aos anexos autorizados (§8 do documento-base).

### 3.3 Requisitos de Compatibilidade (CR — brownfield)

- **CR1:** Módulos **intocáveis**: Cargas, Demanda EDP, IB, Adaptador 1:1 de circuitos, Categoria de Entrada, Tabelas 001/002 EDP, mapeamento R/S/T, MOD-QT (só consumir contrato), guardas INC-01/INC-04/INC-07.
- **CR2:** Disciplinas herdadas mantidas: VA usado diretamente (INC-01, nunca dividir por FP), tensão jamais assumida (INC-04 → `ERRO-TENSAO-AUSENTE`), série normalizada estrita (INC-07).
- **CR3:** Endpoints do v2 mantidos com as alterações do §19; IDs reais de circuitos preservados (CONF-02); convenção de fases R/S/T (CONF-01).
- **CR4:** Esquema de persistência do v2 **evoluído** (não recriado): alterações aditivas nas tabelas existentes + novas tabelas, via migração.
- **CR5:** Requisitos EDP restritos ao ramal de entrada e à área de concessão (UC ≤ 75 kW, rede aérea); jamais generalizados aos circuitos internos.
- **CR6:** Numeração de tabelas exclusivamente da edição 2004 da NBR 5410; teste automatizado rejeita referências à numeração de 1997 do material explicativo.

### 3.4 Decisões arquiteturais pendentes

- **AD-DC-01 — Runtime/API do MOD-DC**
  
  **Status:** `PENDENTE-ARQUITETURA`

  **Gate:** DC-1 e DC-7 não podem iniciar implementação até @architect registrar a decisão técnica.

  **Problema:** o documento-base cita FastAPI + Pydantic v2 + SQLAlchemy 2.x e motor Python com `Decimal`, enquanto o repositório brownfield observado usa TanStack Start + TypeScript + React 19 + IBM Carbon Design System + Supabase/PostgreSQL.

  **Opções válidas:**
  1. módulo TypeScript dentro do TanStack Start existente;
  2. serviço Python/FastAPI separado, integrado ao app atual por contrato;
  3. arranjo híbrido, com justificativa explícita de fronteiras, deploy, rastreabilidade e testes.

  **Critério de decisão:** preservar compatibilidade brownfield, evitar duplicação de regras normativas, manter rastreabilidade, garantir testes locais automatizados, respeitar `CLI First -> Observability Second -> UI Third` e não introduzir backend paralelo sem plano de operação.

  **Impactos que @architect deve documentar:** fronteiras de módulo, persistência normativa, estratégia de API/rotas, estratégia de precisão numérica, deploy, testes por camada e compatibilidade com módulos intocáveis.

### 3.5 Catálogo mínimo de erros

Catálogo central derivado do §23 do documento-base. Nenhum erro pode ser convertido em alerta e nenhum alerta pode suprimir pendência:

| Código | Condição mínima | Tratamento esperado |
|---|---|---|
| `ERRO-TENSAO-AUSENTE` | `tensao_v` ausente | Bloquear cálculo; nenhum fallback de tensão |
| `ERRO-ISOLACAO-AUSENTE` | isolação ausente | Bloquear cálculo; UI não oferece opção vazia |
| `ERRO-METODO-AUSENTE` | método/tipo de linha ausente | Bloquear cálculo; nunca assumir B1 silenciosamente |
| `ERRO-MATERIAL-NAO-ADMITIDO` | material fora dos contextos admitidos, especialmente alumínio residencial | Bloquear e citar 6.2.3.8 |
| `ERRO-LINHA-INCOMPATIVEL` | combinação condutor × tipo de linha não prevista | Bloquear dimensionamento |
| `ERRO-CONSULTA-INCOMPLETA` | consulta normativa sem chave completa | Bloquear consulta |
| `ERRO-TABELA-INCOMPLETA` | linha normativa `[VERIFICAR]` usada por critério obrigatório | Bloquear dimensionamento afetado |
| `ERRO-FATOR-NAO-ENCONTRADO` | temperatura/fator fora dos pontos autorizados | Bloquear; não interpolar sem regra documentada |
| `ERRO-AGRUPAMENTO-NAO-TABELADO` | disposição/faixa de agrupamento sem fator autorizado | Bloquear critério afetado |
| `ERRO-COR-FUNCAO` | cor incompatível com função do condutor | Bloquear validação |
| `INC-07` | seção fora da série normalizada | Rejeitar seção |
| `REQUER-ESTUDO-PARALELO` | nenhuma seção da série atende | Não dimensionar paralelo automaticamente |
| `PENDENTE-I2` | I2 ausente | Manter condição b) de C2 pendente |
| `VERIFICAR-NEUTRO-HARMONICAS` | TH3 acima do limite definido para cálculo direto | Bloquear neutro até verificação específica |


---

## 4. Fora de Escopo

- Cálculo de curto-circuito presumido e integral de Joule (MOD-CC) — apenas contrato e bloqueio.
- Cálculo de queda de tensão (MOD-QT existente) — apenas integração.
- Impedância do percurso de falta e tempos de seccionamento (MOD-SEC) — apenas contrato e bloqueio.
- Seleção definitiva de dispositivos de proteção (MOD-PROT) — In como entrada/sugestão.
- Dimensionamento de condutores em paralelo (detectar e bloquear apenas).
- Eletrodutos, DR, aterramento (exceto seção PE/PEN), unifilar, memorial descritivo.
- Seletividade, estudos harmônicos completos (Anexo F), cabos armados (NBR 11301).
- Dimensionamento econômico (IEC 60287-3-2) — registrado para roadmap futuro (§12.15).

Itens fora de escopo são **dependências registradas**, nunca omissões silenciosas.

---

## 5. Estrutura de Épicos e Stories

Abordagem: **épico único brownfield** com entrega sequencial por camadas, pois o módulo é coeso e as stories têm dependência forte (base normativa → motor → integrações → API → UI → qualidade). Stories dimensionadas para execução por agente único por sessão.

### Épico: MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410

**Goal:** entregar o módulo completo de dimensionamento de condutores (fase, neutro, PE/PEN) com os seis critérios da NBR 5410:2004 modelados, pendências explícitas, rastreabilidade integral e UI Carbon, substituindo o MOD-DC-v2.0 sem regressão nos módulos existentes.

| Story | Título | Escopo resumido | ACs principais |
|---|---|---|---|
| DC-1 | Base normativa versionada | Migrações + carga das tabelas 33, 36–48, 58, 30 com fonte/status por linha; valores confirmados do §12 populados; lacunas `[VERIFICAR]` bloqueantes; teste de regressão da amostra da Tab. 36 | CA-DC-07, CA-DC-23, CA-DC-25 |
| DC-2 | Validação de entradas e guardas | `ValidadorEntradas`: R-03/R-06/R-07/R-08, alumínio §12.7, compatibilidade Tabela 33, cores 6.1.5.3, catálogo de erros §23 | CA-DC-04, CA-DC-05, CA-DC-13, CA-DC-17 |
| DC-3 | Motor C1 — capacidade de corrente | Tabela 46 (condutores carregados + fator 0,86), fatores FCT/FRS/FCA, F=1/√n, isenção 2×D, exclusão ≤30%, trechos múltiplos, seleção de seção | CA-DC-02, CA-DC-03, CA-DC-14, CA-DC-19, CA-DC-24 |
| DC-4 | Motores C2 e C6 + seleção final | Sobrecarga 5.3.4.1 (I2 real, `PENDENTE-I2`, regime severo), seções mínimas Tab. 47, laço de seleção/revalidação, invariantes de propriedade | CA-DC-01, CA-DC-06, CA-DC-12, CA-DC-18 |
| DC-5 | Neutro, PE e PEN | 6.2.6.2 + Tab. 48, Tab. 58, mínimos 6.4.3, PEN TN-C, `VERIFICAR-NEUTRO-HARMONICAS` | CA-DC-15, CA-DC-16 |
| DC-6 | Máquina de estados e contratos downstream | Estados §15, contratos QT/CC/SEC/PROT, revalidação em retorno, `REQUER-ESTUDO-PARALELO` | CA-DC-09, CA-DC-20, CA-DC-21 |
| DC-7 | API e rotas server | Endpoints/rotas §19 (individual, lote, consulta, tabelas, retornos), rastreio no payload, performance de lote, conforme decisão AD-DC-01 | CA-DC-08, CA-DC-11 |
| DC-8 | UI — jornada e tabela de resultados | Jornada §21, DataTable com 6 critérios e decisivo rotulado, painel de detalhe com "Como este resultado foi obtido" | CA-DC-10, CA-DC-22 |
| DC-9 | UI — lote, comparação e resumo | Edição em lote com padrões visíveis, comparação de cenários, resumo do projeto, overrides auditados | CA-DC-10 (parcial), R-11 |
| DC-10 | Qualidade final e acessibilidade | Suíte completa §26 (unitários, integração, fronteira, propriedades, regressão, nomenclatura), WCAG AA, checklist de entrega §30 | CA-DC-01…25 verdes |

**Sequenciamento:** DC-1 → DC-2 → DC-3 → DC-4 → DC-5 → DC-6 → DC-7 → DC-8 → DC-9 → DC-10. DC-8/DC-9 podem paralelizar com DC-7 após DC-6 estabilizar os contratos.

---

## 6. Critérios de Aceite do Módulo

Os 25 critérios de aceite CA-DC-01 a CA-DC-25 do documento-base (§25) são **normativos e integrais** para este PRD — cada story referencia seu subconjunto (tabela do §5).

- **CA-DC-09 (gate de release):** nenhum circuito atinge `VERIFICADO-COMPLETO` com C3/C4/C5 pendentes.
- **CA-DC-23 (gate da base de dados):** qualquer valor da base divergente da célula do original da norma é defeito bloqueante.
- **CA-DC-25 (gate de nomenclatura):** zero referências à numeração de tabelas da edição 1997.

| ID | Critério | Verificação |
|---|---|---|
| CA-DC-01 | ILU Cu PVC B1 30 °C, 1 circuito, IB=2,36 A → S fase = 1,5 mm² (C6 decisivo); status `DIMENSIONAMENTO-PARCIAL` com pendências C3/C4/C5 listadas | automatizado |
| CA-DC-02 | TUE 2F sem neutro (chuveiro 7 700 VA/220 V), Cu PVC B1, 3 agrupados em feixe, IB=34,65 A → n_carregados=2 (Tab. 46); IB'=34,65/(1,00×0,70)=49,5 A; coluna B1/2 → S C1 = 10 mm² (Iz base 57 A) | automatizado |
| CA-DC-03 | Bifásico **com** neutro → n_carregados = 3 (não 2) | automatizado |
| CA-DC-04 | `tensao_v=None` → `ERRO-TENSAO-AUSENTE`, nenhum cálculo | automatizado |
| CA-DC-05 | Isolação ausente → `ERRO-ISOLACAO-AUSENTE`; dropdown sem opção vazia | automatizado + inspeção |
| CA-DC-06 | Seção final ∈ série do §12.13 do documento-base em 100% dos casos (INC-07) | automatizado |
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
| CA-DC-23 | Valores carregados da Tab. 36 conferem com a amostra do §12.2.1 do documento-base | automatizado (regressão da base) |
| CA-DC-24 | Grupo de condutores não semelhantes (seções fora de 3 consecutivas normalizadas) → fator F = 1/√n aplicado, **substituindo integralmente** qualquer fator tabelado (Tab. 42–45); n=10 → F≈0,316; alerta quando F < 0,30 | automatizado |
| CA-DC-25 | Nenhuma referência a numeração de tabelas da edição 1997 (Tab.31–34, Tab.37, Tab.42 como agrupamento multicamada, Tab.43 como seções mínimas) no código, dados ou UI — apenas numeração 2004 (§12.14 do documento-base) | automatizado (lint/grep) |

Exemplo numérico de referência (§27 do documento-base) é a memória de cálculo canônica para validação manual: chuveiro 2F/220 V, IB 34,65 A, B1, 3 agrupados → S fase = 16 mm², critério decisivo C2, status `DIMENSIONAMENTO-PARCIAL`.

---

## 7. Riscos, Dependências e Pendências

### 7.1 Pendências normativas herdadas ([VERIFICAR] — §28 do documento-base)

| ID | Item | Impacto no produto |
|---|---|---|
| VER-DC-01 | Valores completos das Tabelas 36–39 | **Bloqueante** para C1 fora da amostra confirmada — priorizar transcrição antes de DC-1 concluir |
| VER-DC-02 | Tabelas 43/44/45 completas | Bloqueia múltiplas camadas e linhas enterradas |
| VER-DC-04 | Relação I2/In por norma de dispositivo | Condição b) fica `PENDENTE-I2` sem I2 informado |
| VER-DC-05 | Série comercial de In | In automático permanece `SUGESTAO` |
| VER-DC-06 | Tabela 33 integral (tipos de linha) | Limita o seletor de tipo de linha |
| VER-DC-07 | 800/1000 mm² nas Tab. 38/39; IEC 60228 | Baixo |
| VER-DC-08 | Anexo F (TH3 > 33%) | Bloqueia neutro nesses casos |
| VER-DC-09 | Detalhes 5.1.2.2.4 | Necessário só ao MOD-SEC futuro |
| VER-DC-11 | Padrão EDP subterrâneo | Fora do perfil atual |
| VER-DC-12 | Tabelas 56/57 (k para PE adiabático) | Método alternativo de PE |

### 7.2 Riscos de produto

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Transcrição incompleta das Tabelas 36–39 travar o C1 na prática | Alta | Alto | DC-1 inclui esforço dedicado de transcrição + regressão CA-DC-23; lacunas bloqueiam com erro claro, não silenciosamente |
| Usuários perceberem `DIMENSIONAMENTO-PARCIAL` como regressão vs. o antigo `DIMENSIONADO` | Média | Médio | UX explícita: pendências nomeadas com explicação normativa; comunicação da correção (v2 estava não conforme) |
| Acoplamento com MOD-QT em revalidação criar laços | Média | Médio | Laço de revalidação com limite e critério decisivo rastreado (CA-DC-21); testes de integração dedicados |
| Escopo da UI (§21) inflar as stories DC-8/DC-9 | Média | Médio | Modo assistido primeiro; comparação de cenários pode ser fatiada se necessário, sem cortar os 6 critérios nem o rastreio |
| Migração de dados do v2 divergir da nova base | Baixa | Alto | CR4: migração aditiva + regressão da base; valores v2 errados **substituídos**, nunca mesclados |

### 7.3 Dependências de processo

- **@architect:** validar arquitetura em camadas (NFR7) e contratos de integração antes de DC-3.
- **@data-engineer:** DDL das migrações da base normativa (DC-1) — delegação padrão.
- **@sm:** desdobrar as stories DC-1…DC-10 a partir deste PRD (`*draft`).
- **@po:** validar este PRD e as stories (checklist de 10 pontos).

---

## 8. Validação PM e Handoff

### 8.1 Resultado da validação PM

O PRD brownfield do MOD-DC v3.0 foi revisado contra o documento-base e contra o repositório carregado. Foi identificado e registrado um bloqueio de planejamento: o documento-base cita FastAPI/Pydantic/SQLAlchemy e motor Python com `Decimal`, enquanto o app existente em `sistema-de-instala-es-el-tricas-sie-main` usa TanStack Start + TypeScript + React 19 + Carbon + Supabase/PostgreSQL.

O PRD foi ajustado para:

- manter os requisitos funcionais e normativos do documento-base;
- remover a dependência implícita de FastAPI/Pydantic nos FR16/FR17;
- registrar a decisão arquitetural **AD-DC-01 — Runtime/API do MOD-DC**;
- renomear a story DC-7 para "API e rotas server", dependente da decisão técnica;
- transcrever os critérios CA-DC-01 a CA-DC-25 no corpo do PRD;
- completar o catálogo mínimo de erros;
- preservar fontes, hierarquia, premissas e glossário do documento-base;
- manter o status como Draft aguardando @po e @architect.

### 8.2 Checklist PM

| Categoria | Status | Observação |
|---|---|---|
| Problema e contexto | PASS | Problema central claro: MOD-DC-v2.0 emitia completude com critérios obrigatórios pendentes. |
| Escopo MVP | PARTIAL | Escopo normativo está claro, mas é grande. Precisa validação @po para confirmar se DC-1...DC-10 serão mantidas como um único épico. |
| UX | PASS | Jornada, tabela, detalhe, pendências, acessibilidade e rastreio estão descritos. |
| Requisitos funcionais | PASS | FR1...FR27 cobrem motor, integração, API, UI e base normativa. |
| Requisitos não funcionais | PASS | Rastreabilidade, precisão, acessibilidade, segurança e arquitetura em camadas definidos. |
| Épico e stories | PARTIAL | Epic structure existe, mas stories detalhadas devem ser criadas por @sm/@po. |
| Direção técnica | PARTIAL | Há decisão pendente AD-DC-01 sobre runtime/API. |
| Dados e integrações | PASS | Dependências upstream/downstream e lacunas `[VERIFICAR]` foram explicitadas. |
| Clareza e comunicação | PASS | Documento tem gates, riscos, fora de escopo e referências. |

**Decisão PM:** `NEEDS ARCHITECTURE DECISION BEFORE IMPLEMENTATION`.

O PRD pode ir para validação de produto, mas não deve virar story implementável até @architect fechar AD-DC-01.

### 8.3 Checklist de correções PO

| Item PO | Status | Evidência no PRD |
|---|---|---|
| Stack real do app e decisão @architect antes de DC-1/DC-7 | `BLOQUEADO POR AD-DC-01` | AD-DC-01 formalizada com status `PENDENTE-ARQUITETURA` e gate explícito |
| FR16 ainda citava Pydantic como tecnologia fixa | `RESOLVIDO` | FR16 agora define contrato funcional neutro e remete a AD-DC-01 |
| CA-DC-01...25 apenas referenciados | `RESOLVIDO` | Tabela integral CA-DC-01 a CA-DC-25 transcrita na seção 6 |
| Catálogo mínimo de erros incompleto | `RESOLVIDO` | Seção 3.5 inclui `ERRO-METODO-AUSENTE`, `ERRO-AGRUPAMENTO-NAO-TABELADO`, `INC-07` e demais códigos |
| Fontes, hierarquia, premissas e glossário resumidos demais | `RESOLVIDO` | Seções 1.3 a 1.6 adicionadas com regras do documento-base |

### 8.4 Bloqueadores

1. **AD-DC-01 — Runtime/API do MOD-DC:** decidir entre módulo TypeScript no TanStack Start existente, serviço Python/FastAPI separado ou modelo híbrido. Esta decisão é autoridade de @architect.
2. **Base normativa incompleta:** Tabelas 36-39, 43-45 e Tabela 33 integral ainda possuem itens `[VERIFICAR]`; DC-1 deve tratar essas lacunas como dados versionados bloqueantes.
3. **Autoridade de stories:** PM não cria stories detalhadas finais; @po valida o PRD e @sm desdobra DC-1...DC-10 em stories.

### 8.5 Próximos handoffs

**Para @architect:** validar AD-DC-01 antes da implementação, documentando decisão técnica, fronteiras de módulo, persistência normativa, estratégia de API/rotas, impacto em deploy e plano de teste por camada.

**Para @po:** validar se o escopo DC-1...DC-10 permanece como épico único, se CA-DC-01...CA-DC-25 são aceitos integralmente, se `DIMENSIONAMENTO-PARCIAL` é linguagem adequada para usuário final e se pendências C3/C4/C5 e lacunas `[VERIFICAR]` devem bloquear aprovação técnica.

**Para @sm:** após validação @po e decisão @architect, criar stories em `docs/stories/`, iniciando por DC-1, com rastreabilidade para FR/NFR/CR/CA-DC, checklist, file list e validações locais.

---

## 9. Referências

- `Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` — especificação técnica integral (MOD-DC-v3.0). **Este PRD não substitui a especificação**: em caso de divergência de detalhe normativo, a especificação v3 prevalece.
- ABNT NBR 5410:2004 (`NBR_5410_chunks.json`) — fonte normativa primária.
- PT.DT.PDN.00068 v09 (`PT_DT_PDN_00068_V9_chunks.json`) — padrão EDP SP, aplicável só ao ramal de entrada.
- Guia EM da NBR 5410 (`04_condutores_markdown_limpo.md`, `06_dimensionamento`) — material explicativo, numeração ed. 1997 (nunca copiar).
- Auditorias SIE: 2026-06-21 (18 incongruências NBR/EDP) e 2026-07-07 (dimensionamento/proteção/laudo inexistentes — este módulo ataca o P0 do roadmap).

---

*PRD gerado por Morgan (@pm) — próximo passo: validação @po, depois @sm `*draft` DC-1.*
