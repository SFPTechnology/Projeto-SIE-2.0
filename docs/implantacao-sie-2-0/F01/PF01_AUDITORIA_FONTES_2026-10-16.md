# PF-01 — Auditoria verificável das fontes e caminhos dos motores (16/10/2026)

**Resultado:** INVENTÁRIO E TRIAGEM EXECUTADOS; **G01/G02 ainda NÃO homologados**. Este registro é uma revisão da arquitetura e fontes textuais derivadas existentes, **não** substitui inspeção do exemplar primário em PDF com páginas e notas.

## 1. Evidências observadas

| Fonte | Evidência inspecionada nesta retomada | Situação |
|---|---|---|
| EDP PT.DT.PDN.00068 V09 | Arquivo binário listado no GitHub: `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf` (2.678.187 bytes). F00 inventaria SHA-256 `b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810`. Markdown derivado associado, 91 páginas marcadas e Anexo A identificado (Tabelas 001/002, páginas derivadas ~31/32). Página oficial [EDP normas/padrões](https://www.edp.com.br/normas-e-padroes-tecnicos/) apresenta código 00068, edição V09, publicação 15/04/2026. | **CANDIDATO PRIMÁRIO NO REPOSITÓRIO.** Não confirmado que o PDF local equivale ao download oficial vigente, nem direitos/restrições. Frontmatter derivado traz 14/04/2026: diferença entre datas deve ser investigada, não converter publicação em vigência. |
| ABNT NBR 5410 | `Arquivos_Diversos/NBR_5410_original/NBR-5410.md` (628.294 caracteres) é uma **transcrição derivada de um PDF**, não original autenticado; edição indicada na transcrição 2004 com correção 2008. Identificadas nas âncoras de texto as Tabelas 36–39 (capacidade), 40–41 (temperatura), 42–45 (agrupamento), 46 (carregados), com páginas derivadas ~109–120. | **ORIGINAL AUTORIZADO NÃO COMPROVADO**; tabela HTML derivada pode conter erro de mesclagem e suas células não são verificadas. Não publicar valores ABNT sem direito de uso. |
| NR-10 | Página oficial do [MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10) informa Portaria MTE 737/2026, nova redação geral em 01/06/2027, ressalva para instalações existentes. | **METADADO EDITORIAL CONFIRMADO**; transições específicas e aplicação à situação de projeto permanecem a resolver por original/parecer. NR-10 não fornece Iz/Rca/XL no lugar da ABNT. |
| ABNT NBR 5419 | Catálogo e eventual material de apoio, sem exemplar oficial completo validado; SPDA é requisito conforme análise de aplicabilidade, **não** um mecanismo para validar Iz/Rca/XL. | **APLICABILIDADE PENDENTE, NÃO EXCLUIR POR CONVENIÊNCIA**. |

## 2. Inspeção de código: 24 dependências inventariadas (ainda NÃO número de células homologadas)

Arquivo de trabalho: `INVENTARIO_CELULAS_E_REGRAS_USADAS.csv`. As 24 entradas são **13 categorias codificadas EDP** + **11 requisitos/grupos técnicos e lacunas**; **não representam o universo completo de células de todas as tabelas**.

- `sie_api/domain/edp.py`: 13 entradas `CATALOGO_EDP` (U2, D2, D4, D6, D7, D9, D10, T2, T4, T6, T7, T9, T10) contendo disjuntor, medição, condutores e aterramento. Os valores são *candidatos legados*, não homologados. A seleção por menor In é uma simplificação que depende de outras condições da Tabela 001/002; o servidor não recebe todos os parâmetros físicos/territoriais/temporais do padrão.
- `sie_api/domain/engines.py`: `selecionar_condutor()` recebe uma tabela `secao_mm2/capacidade_a` **do cliente**; não carrega célula Iz homologada, método, isolação, agrupamento e temperatura do servidor. Seleciona pela capacidade corrigida e fator único.
- `calcular_queda_tensao_monofasica()` recebe resistência `Ω/km` **do cliente** e aplica modelo resistivo (não é o motor complexo com Rca, XL e cosφ). `calcular_queda_tensao_trifasica_resistiva()` também é resistivo. **Ainda não existe** seleção normativa autorizada de Rca/XL na API de análise.
- `sie_api/application.py` e `sie_api/calculation_traces.py`: registram o algoritmo executado, parâmetros e resultado; **não** ID/linha/coluna primária verificada e realmente consumida. `normative_rule_ids_used_verified=[]` e `release_allowed=false` são a declaração correta.
- `sie_api/domain/normative.py` realiza somente triagem de metadados territorial/temporal; catálogo continua `verified_data=false`.

## 3. Correções já aplicadas durante a execução

- **ENG-001 — arredondamento de Iz:** `selecionar_condutor()` devolve Iz exato para *decisão*; `application.py` só arredonda o valor exibido, preservando `capacidade_decisao_a` para auditoria. Testes impedem tratar Iz=19,996 A como autorização de disjuntor In=20 A.
- **ENG-002 — categoria EDP U/D com carga trifásica:** `enquadrar_edp()` retorna bloqueio `EDP-003` para combinação incompatível em seleção automática, sem presumir categoria adequada.
- **Proveniência EDP falsa:** `FONTE_EDP.status` foi rebaixada de `VERIFICADO` para `DOCUMENTADO_SEM_FONTE_PRIMARIA`; catálogo permanece acessível para estudo, **sem liberação normativa**.
- **F00:** fixtures e registro original não foram alterados; `test_legacy_golden.py` diferencia comportamentos intencionalmente corrigidos e replay histórico original, evitando preservar defeito como condição de aprovação F01.

## 4. Documento/fato faltante exatamente necessário

1. Confirmar se o arquivo local `PT.DT.PDN.00068_V9.pdf` corresponde à fonte da EDP oficial vigente, com páginas, tabela e condição, *inclusive* diferenças de data, vigência e área. Dupla leitura A/B de cada célula usada no motor.
2. Acessar exemplar **ABNT NBR 5410 oficial autorizado** da edição aplicável e conferir por duas leituras as linhas/colunas efetivas de capacidade, fatores e notas. Não extrair valores da cópia comentada e declarar homologados.
3. Obter/validar referências primárias de **Rca e XL**, dados de operação/arranjo e caso complexo de queda de tensão; o motor atual é explicitamente resistivo. Rdc20 não substitui Rca/XL.
4. Fixar jurisdição/concessionária/tensão/tipologia/data para cada regra EDP; resolver impacto NR-10 na situação concreta.
5. Calcular *expected* independente para cada seleção/motor após o item 1–4, antes de provar G03.
6. Executar revisões isoladas dos três agentes e atestação normativa profissional externa exigida pelo manifesto: nenhum processo independente foi registrado nesta sessão.

**Estado de evidência:** 0 células primárias conferidas duas vezes, 0 casos **normativos** independentes aprovados, 0 signoffs profissionais, 0 sessões QA3 autênticas até aqui. Os testes computacionais são registrados pela CI e **não** mudam esses valores.

## 5. Critério de parada eficiente

**Não executar 20 ciclos idênticos de YOLO.** Se o documento oficial autorizado não estiver disponível, registrar `BLOCKED_SOURCE`, continuar backend/UX e congelar o pedido exato: **exemplar oficial ABNT NBR 5410 aplicável e provas da conferência da EDP V09**. Se o que faltar for somente acesso à licença ou parecer técnico independente, o sistema deve registrar `AWAITING_EXTERNAL_SIGNOFF` sem reabrir F00.
