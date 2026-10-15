# F00 — Matriz de motores, grandezas, fontes e riscos

**Baseline auditada:** `8d86db26f5e8675eaced4638af14bd84019e15e7`.<br>
**Data:** 2026-10-15. **Perspectiva:** QA-02, engenharia elétrica e fontes.<br>
**Escopo:** diagnóstico e preservação do material presente nessa árvore. Nenhum resultado deste documento homologa projeto, tabela, edição de norma, instalação ou padrão de entrada.

Esta matriz resulta da leitura dos arquivos e da execução local das primitivas identificadas abaixo. As referências `arquivo:linha` apontam para a baseline; números dentro dos documentos `EXTRACAO*` são linhas desses documentos, e não comprovação de que seus caminhos internos existam como código executável. O inventário SHA-256 prova identidade de bytes, não autenticidade normativa.

## 1. Estados e limite observado

| Estado | Significado nesta auditoria |
| --- | --- |
| CONFIRMADO | Implementação, contrato ou arquivo efetivamente localizado; somente os casos explicitamente exercitados foram executados. |
| PARCIAL | Existe um subconjunto demonstrativo, um adaptador, dependências ausentes ou trecho documental, sem equivalência integral comprovada. |
| NÃO IDENTIFICADO | O motor ou dado procurado não foi localizado como implementação nesta árvore. Isso não declara sua inexistência em outro repositório. |
| NÃO VERIFICADO | Valor/fonte sem confirmação suficiente de proveniência, fidelidade integral, edição vigente ou aplicabilidade. |

O arquivo `.gitmodules:1` aponta para `sistema-de-instala-es-el-tricas-sie-main`, mas esse diretório e seu gitlink não constam da árvore `HEAD` inspecionada. Não foi possível executar o aplicativo TypeScript completo citado nos planos e extratos. As primitivas Python são implementações demonstrativas presentes na baseline, e não substitutos comprovadamente equivalentes de todos os motores históricos.

## 2. Motores executáveis presentes

| ID | Motor e evidência | Entradas e unidades | Regra e saída observadas | Fonte e valores embutidos | Estado e risco |
| --- | --- | --- | --- | --- | --- |
| ENG-PY-QT-1 | `restructuring/apps/api/sie_api/domain/engines.py:34–43` | `I` [A], comprimento de ida `L` [m], resistência linear `R` [Ω/km], tensão `U` [V]; valores `Decimal` | `ΔV=2×(L/1000)×I×R`; `100×ΔV/U`; saída em V e %, duas casas, `ROUND_HALF_UP`. `L=0` é aceito; I/R/U devem ser positivos e finitos. | Fórmula algébrica de um modelo monofásico puramente resistivo. `2`, conversão `1000` e escala `100`; R vem do chamador e sua origem é NÃO VERIFICADA. Nenhuma tabela de resistências é consultada. | CONFIRMADO para o modelo e casos E1/E0. Não inclui X, FP variável, temperatura, harmônicas, desbalanceamento ou queda anterior; não avalia limite normativo. Uso como verificação completa: risco ALTO. |
| ENG-PY-QT-3 | `engines.py:107–128` | I [A], L [m], R [Ω/km], tensão entre fases [V] | `ΔV=√3×(L/1000)×I×R`; percentual sobre tensão de linha; mesmas validações e arredondamento. | Hipóteses escritas no código: trifásico equilibrado, `cos(phi)=1`, `X=0`. √3 é constante matemática; R não tem vínculo com catálogo/temperatura. | CONFIRMADO para modelo/E2; PARCIAL como queda trifásica geral. Não integrado por `application.py` ao endpoint de análise. |
| ENG-PY-COND | `engines.py:80–104` | Ib [A], fator global adimensional `0<f≤1`, pares `(seção [mm²], Iz_base [A])` | Escolhe a menor seção informada para a qual `Iz_base×f≥Ib`; rejeita tabela vazia, duplicatas, não finitos e insuficiência. Retorna seção, Iz corrigida e fator arredondados. | Toda a tabela e fator são dados do chamador; fonte, método, material, isolação e número de condutores não são verificados pelo motor. Limite `f≤1` é do protótipo, não regra normativa universal. | CONFIRMADO/E3; PARCIAL para dimensionamento. E5 comprova perda de precisão quando o valor arredondado de Iz alimenta proteção. |
| ENG-PY-PROT | `engines.py:54–69` | Ib [A], Iz corrigida [A], catálogo de correntes nominais In [A] | Ordena candidatos e devolve menor In com `Ib≤In≤Iz`; rejeita catálogo vazio/valores inválidos e ausência de candidato. | Catálogo vem do chamador; comparação dimensional apenas. A aplicação utiliza `[6,10,16,20,25,32,40,50,63,80,100,125] A` em `application.py:6`, sem fabricante/modelo/fonte primária. | CONFIRMADO/E4. NÃO VERIFICADO como proteção completa: sem I2, curto presumido, capacidade de interrupção, curva, tempo, seletividade, coordenação, DR ou DPS. |
| ENG-PY-ORQ | `restructuring/apps/api/sie_api/application.py:9–26` | Payload com os valores anteriores, tabela de condutores e metadados de evidência | Executa condutor → queda monofásica → disjuntor; retorna números, critérios e rastreabilidade. | `resistencia_ohm_km` é independente da seção selecionada; não existe busca de R para essa seção nem iteração por queda. `gates.py:26–32` mantém PENDENTE com metadados completos e BLOQUEADO sem evidência suficiente; cliente não consegue conceder aprovação. | CONFIRMADO; integração PARCIAL. E5: arredondamento de Iz pode permitir In maior que capacidade bruta. Gate normativo permanece falso. |
| ENG-PY-EDP | `restructuring/apps/api/sie_api/domain/edp.py:29–65` | Modalidade U/D/T, corrente de demanda [A], carga instalada [kW], presença de carga trifásica [bool] | Filtra modalidade e escolhe menor disjuntor ≥ corrente; retorna categoria, seções e alertas. Bloqueia carga >75 kW, T sem carga trifásica e corrente acima do catálogo. Sempre `liberado_para_padrao_entrada=False`. | 13 categorias transcritas de 001/002; limiar 75 kW e identificação v09/14-04-2026. O próprio retorno classifica a regra automática como `DOCUMENTADO_SEM_FONTE_PRIMARIA`; não há cálculo de demanda neste motor. | CONFIRMADO como seleção simplificada/E6. PARCIAL como elegibilidade EDP: sem tensão, tipo de rede, local, limites de motor, geração distribuída e demais condições. U/D com carga trifásica não recebe alerta no caso exercitado E7. |

**Outro dado embutido:** `restructuring/apps/web/app.js:18` envia automaticamente `(2,5 mm²,24 A)`, `(4,32)`, `(6,41)` e `(10,57)`. A aplicação não verifica a fonte desses pares; são NÃO VERIFICADOS para uma instalação real. A interface não transforma esses números em tabela normativa validada.

**Divergência documental constatada:** `restructuring/docs/CONTRATOS-ENGENHARIA.md:21` descreve o arredondamento como exclusivo de apresentação. E5 demonstra que a Iz arredondada também participa da decisão de disjuntor em `application.py:17`. Preservar essa declaração sem ressalva induziria uma interpretação incorreta.

## 3. Otimizador TypeScript incompleto

| Item | Evidência e grandezas | Regras/valores encontrados | Fonte e risco |
| --- | --- | --- | --- |
| Pré-seleção C1 | `src/domain/calculo/otimizador.ts:138–175`; corrente [A], temperatura [°C], quantidade de circuitos [inteiro] | Série de seções [mm²]: `1.5,2.5,4,6,10,16,25,35,50,70,95,120`. Capacidades [A] correspondentes: `15.5,21,27,36,50,68,89,120,155,195,245,295`. Necessidade: `I/(fT×fG)`. | Código denomina tabela “simplificada” para cobre/PVC/30 °C; não identifica método, coluna, geometria e fonte para cada célula. Todos os valores: NÃO VERIFICADOS para dimensionamento normativo. |
| Temperatura | `otimizador.ts:182–188` | Até 30 °C: 1. Acima: `max(0.7,1-ceil((T-30)/10)×0.13)`. Em 40 °C, fT=0,87; em 70 °C, fT=0,70 pelo piso. | Heurística descontínua e piso embutidos. O comentário atribui aproximação à NBR 5410, mas nenhuma tabela rastreável sustenta esse algoritmo nesta árvore. NÃO VERIFICADO; risco ALTO. |
| Agrupamento | `otimizador.ts:194–200` | 1 ou 2 circuitos: 1; 3–4: 0,8; 5–6: 0,7; mais: 0,6. | Não distingue disposição, espaçamento, método e condições de aplicação. NÃO VERIFICADO; risco ALTO. |
| Validação C1–C6 | `otimizador.ts:6–20,70–95`; esquema em `src/api/schemas/otimizar.schema.ts:6–75` | Importa seis validadores e tipos; só retorna APROVADO se todos retornarem APROVADO. Schema aceita corrente 0,1–500 A, comprimento 0–1000 m, temperatura 10–70 °C, 1–10 circuitos, métodos B1/C/E, materiais cobre/alumínio e PVC/XLPE/EPR. | `../modelo/tipos` e `./validadores` ausentes. Não foi possível executar o otimizador. Pré-seleção ignora material/isolação/método aceitos no schema. Não presumir que dependências corrigiriam isso. |
| Significado dos critérios | `otimizador.ts:15–19` e `otimizar.schema.ts:90–95`, comparados a `EXTRACAO-COMPLEMENTAR-SIE-2.md:28–63` | Otimizador usa C4 “seletividade/coordenação”, C5 “qualidade técnica”; extrato MOD-DC usa C4 “seccionamento automático”, C5 “queda de tensão”. | Contratos diferentes com rótulos iguais. Não os unir por nome sem um adaptador explícito e testes de semântica. |

Uma aritmética isolada do pré-filtro não prova funcionamento do motor: para 20 A, 40 °C e quatro circuitos, `20/(0,87×0,8)=28,7356… A`; na tabela embutida, 4 mm²/27 A falha e 6 mm²/36 A passa. Esse exemplo caracteriza a heurística documental; a saída completa C1–C6 continua NÃO EXECUTADA.

## 4. Motores históricos citados, extratos e artefatos arquivados

| Comportamento procurado | Referência realmente disponível | Entradas/saídas identificáveis | Regra ou fonte identificada e lacuna |
| --- | --- | --- | --- |
| Geometria e soma de cargas | `EXTRACAO-COMPLEMENTAR-SIE.md:219–353,365–386` | Dimensões [m], área real [m²], perímetro real [m], dependências/cargas; área, perímetro, VA e quantidades agregadas. | Orquestrador chama `geometria`, `iluminacao`, `tomadas`, `cargas-adicionais` ausentes como módulos executáveis. Documenta `A=C×L`, `P=2(C+L)` e soma VA por categoria. Extrato PARCIAL, sem equivalência executável. |
| Previsão de iluminação | `EXTRACAO-COMPLEMENTAR-SIE.md:389–405`; `Arquivos_Diversos/NBR_5410_original/NBR-5410.md:13324–13330` | Área [m²] → VA e mínimo de pontos | Amostra registra 100 VA até 6 m² e incrementos de 60 VA por 4 m² inteiros; `status_verificacao=VERIFICAR`. Transcrição local contém critério compatível, mas código `iluminacao.ts` e catálogo completo estão ausentes. Não confundir VA previsto com potência de lâmpadas ou lux. |
| Quantidade e carga de TUG | `EXTRACAO-COMPLEMENTAR-SIE.md:407–419`; transcrição NBR local:13334–13366 | Tipo de recinto, área/perímetro [m²/m], quantitativos → pontos e VA | Amostra CAT-A: `ceil(P/5)`; referência de alínea `.c` difere da localização de salas/dormitórios `.d` na transcrição local. Tipos completos, categorias e fórmulas de `tomadas.ts` não estão presentes. Casos cozinha/banheiro, exceções e regra agregada >6 pontos não podem ser reconstruídos de uma amostra. Risco ALTO. |
| Carga instalada, demanda EDP A–I e FP | `Arquivos_Diversos/Correção_1/PLANO-CORRECAO-SIE-RECONCILIADO.md:135–143`; `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md:22–59`; PDF EDP local, §§5.5.1/5.5.2, pp.22–25 | Potências declaradas [W/VA/kW/kVA], tipo, quantidade, FP, grupo e instalação → demanda [kVA] e corrente [A] | O PDF descreve soma das parcelas a–i e tabelas de demanda. Não foram localizados `motor-demanda.ts`, `motor-edp-sp.ts`, tabelas de FD em runtime nem testes históricos executáveis. O seletor Python recebe a corrente pronta, portanto não cobre esses motores. Valores de FP/FD históricos: NÃO VERIFICADOS nesta fase. |
| Corrente por carga, divisão e balanceamento de fases | Planos em `Arquivos_Diversos/Correção_1/PLANO-CORRECAO-SIE-RECONCILIADO.md:58–76,157–162`; contratos nos `EXTRACAO*` | S [VA], U [V], número de fases, FP quando entrada for W, destinação e fases → Ib [A], circuitos e distribuição | Implementação completa NÃO IDENTIFICADA. Sem reproduzir caminho W→VA→A nem tratamento de duas/três fases. Não assumir equivalência a partir de rotas/hook documentados. |
| Condutores C1/C2/C6 e neutro/PE/PEN | `EXTRACAO-COMPLEMENTAR-SIE.md:582–1001`; contratos em `EXTRACAO-COMPLEMENTAR-SIE-2.md:83–155` | Ib/In/I2 [A], seção [mm²], material, isolação, método, temperatura [°C], agrupamento, solo, esquema e harmônicas → seções e estados | Extrato consulta tabelas 36/37, fatores FCT/FRS/FCA/neutro e tabelas de seção mínima. Os motores e repositórios importados não existem como código nesta baseline. Série comercial extratada vai de 0,5 a 630 mm²; não igual à série do otimizador raiz. Fonte/colunas/casos não foram homologados. |
| Curto-circuito MOD-CC | `EXTRACAO-COMPLEMENTAR-SIE.md:728–749`; `EXTRACAO-SIE.md:682–806` | Icc [A], tempo [s], integral de Joule [A²s], fonte e booleano aprovado → estado C3 | Trecho consome resultado downstream; não calcula curto/integral de Joule. Handlers de mock estão transcritos em Markdown, sem implementação executável correspondente. Não contar como motor real preservado. |
| Seccionamento MOD-SEC | `EXTRACAO-COMPLEMENTAR-SIE.md:752–783`; `EXTRACAO-SIE.md:808–938` | Esquema TT/TN/IT, tempo [s], fonte/booleano → estado C4 | Extrato considera TT NAO-APLICAVEL e aguarda resultado nos demais; não calcula desligamento nem valida proteção de pessoas. Regra/aplicabilidade: NÃO VERIFICADAS; documentação não concede aprovação. |
| Queda de tensão MOD-QT e integração C5 | `EXTRACAO-COMPLEMENTAR-SIE.md:464–580,785–807` | Corrente [A], U [V], seção [mm²], queda/limite [%], seção requerida e fonte → estado e seção requerida | Contrato e consumidor identificados; não há motor R/X completo nem suas tabelas executáveis. As funções Python resistivas não comprovam equivalência. JSON Prysmian em `docs/research/2026-07-28-resolucao-ver-qt/impedancia-prysmian.json` é extração derivada, não está integrado a `engines.py`; seu PDF-fonte não foi localizado. |
| Proteção MOD-PROT completa | `EXTRACAO-COMPLEMENTAR-SIE-2.md:65–81,145–152`; PRD e stories locais | In/I2 [A], capacidade de interrupção, norma do dispositivo e tempo [s] → parâmetros de proteção | A unidade da capacidade de interrupção não está explícita na interface transcrita; não assumir A ou kA silenciosamente. Implementação completa do MOD-PROT NÃO IDENTIFICADA nesta árvore; seletor Python cobre apenas desigualdade de corrente. |
| Unifilar arquivado / adaptador 1:1 | Três cópias em `Arquivos_Diversos/Unifilar/Unifilar/files (5)/(6)/(7)/sie-camada-visualizacao-fase0-1b/backend/`; exemplo `(7)/adaptador_1x1.py:1–22,44–50,67–141` | Ponto com VA, U, Ib e fases → circuito provisório, metadados e pendências | Não recalcula Ib: copia valor; mapeia A/B/C→R/S/T e carrega regra documental `IB=S/V`. Default ILU/TUG 127 V tem origem declarada de contrato; não equivale à tensão de placa de TUE. Zona molhada booleana vira requisito de DR, sem estudo completo. Produto integrado não comprovado; preservar como artefato e contrato, não motor normativo. |
| DR, DPS, aterramento e SPDA completos | Campos, PRDs e descrições encontrados; nenhum motor completo localizado | Grandezas/condições de exposição e coordenação não suficientemente especificadas | NÃO IDENTIFICADO como engenharia executável. Schema do otimizador contém resistência de aterramento default 5 Ω e intervalo 1–100 Ω (`otimizar.schema.ts:59–64`), sem fonte primária/aplicabilidade. Valor NÃO VERIFICADO; não tratar como critério universal. |

Planos e relatórios anteriores são úteis como índice histórico, mas suas declarações de conclusão não substituem a observação dos arquivos nesta baseline. Os scripts de pesquisa Prysmian também referenciam um PDF em caminho absoluto Windows de outra máquina (`docs/research/2026-07-28-resolucao-ver-qt/verificar-coerencia.py:16–32`), de modo que não são reprodução portátil disponível do dado-fonte.

## 5. Fontes locais e conferência limitada EDP

| Fonte | Natureza observada | Evidência/limite |
| --- | --- | --- |
| `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf` | PDF de 91 páginas, título EDP São Paulo, versão 09, início de vigência impresso 14/04/2026 | Foram extraídas as pp.30–32 e renderizadas/inspecionadas visualmente as pp.31–32 nesta sessão. O próprio PDF se identifica como cópia não controlada, gerada em 07/07/2026. Presença local não comprova vigência atual nem aplicabilidade ao empreendimento. |
| `PT.DT.PDN.00068_V9_markdown_limpo.md` / `_chunks.json` no mesmo diretório | Extrações derivadas da fonte anterior | Contêm metadados e conteúdos úteis para localização. Integridade do arquivo e fidelidade de cada tabela são verificações diferentes. Não usar comparação entre duas extrações da mesma origem como auditoria independente. |
| `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md` | Registro de conferência anterior por agente de IA, datado 01/07/2026 | Herda rótulos VERIFICADO, informa ausência de `PT.DT.PDN.03.14.020 v06` e reconhece `corrente_demanda_max_A` como campo derivado. Não é aprovação humana/profissional nem sua simples leitura reexecuta toda a conferência. |
| `Arquivos_Diversos/tabelas_001_002_padrao_edp.md` | Consolidação documental | Pode auxiliar a leitura, mas a conferência abaixo usou também o PDF local para evitar somente comparar resumos. |
| `Arquivos_Diversos/NBR_5410_original/NBR-5410.md` e `_chunks.json` | Transcrição/extração declarada de ABNT NBR 5410:2004, corrigida em 2008; PDF original indicado não localizado nessa pasta | Algumas regras e referências foram confrontadas entre extrato e transcrição. Edição vigente, integralidade e fidelidade ao PDF autorizado: NÃO VERIFICADAS. Há sinais de extração com ordem de símbolos alterada; ex.: desigualdade em torno de `NBR-5410.md:3949`. Não ler equação mal extraída como regra pronta para runtime. |
| `Arquivos_Diversos/NBR_5410_comentada/` | PDF comentado e 16 módulos em PDF, Markdown e JSON com manifesto | Material secundário presente. Comentário técnico não substitui fonte primária nem valida coluna/temperatura/método de todas as tabelas. Não se declarou conferência integral dos 16 módulos. |
| `docs/research/2026-07-28-resolucao-ver-qt/impedancia-prysmian.json` | Extração de tabela de fabricante com metadados e hash alegado do PDF de origem | PDF-fonte não localizado e script usa caminho Windows externo. Dados Rca/X/temperatura: NÃO VERIFICADOS nesta auditoria e não usados pelos motores Python. |
| ABNT NBR 5419 / NR-10 / outra concessionária | Há menções documentais; nenhum conjunto completo correspondente identificado como fonte e motor aplicável | Não declarar cobertura dessas normas por associação ao nome SIE ou à presença de NBR 5410. |

### Células efetivamente confrontadas com pp.31–32 do PDF EDP local

As 13 linhas abaixo coincidem visualmente com os campos implementados em `edp.py:32–46`. É uma conferência de transcrição de subconjunto, sem julgar adequação da seleção automática. Caixa, poste, eletrodutos, NH/chave e limite de maior motor existem na tabela visual, mas não fazem parte do contrato implementado em Python.

| Categoria | In [A] | Medição | Entrada PVC / EPR-XLPE [mm²] | Aterramento PVC / EPR-XLPE [mm²] |
| --- | ---: | --- | --- | --- |
| U2 | 70 | Direta | Responsabilidade da distribuidora | 16 / 16 |
| D2 | 63 | Direta | Responsabilidade da distribuidora | 16 / 16 |
| D4 | 100 | Direta | 35 / 25 | 16 / 16 |
| D6 | 150 | Direta | 70 / 50 | 35 / 25 |
| D7 | 200 | Indireta | 95 / 70 | 50 / 35 |
| D9 | 300 | Indireta | 185 / 120 | 95 / 70 |
| D10 | 350 | Indireta | 240 / 185 | 120 / 95 |
| T2 | 63 | Direta | Responsabilidade da distribuidora | 16 / 16 |
| T4 | 100 | Direta | 35 / 25 | 16 / 16 |
| T6 | 150 | Direta | 70 / 50 | 35 / 25 |
| T7 | 200 | Indireta | 95 / 70 | 50 / 35 |
| T9 | 300 | Indireta | 185 / 120 | 95 / 70 |
| T10 | 350 | Indireta | 240 / 185 | 120 / 95 |

O PDF local também condiciona atendimento a características de rede/local e contém observação sobre comparar corrente de geração distribuída com a de carga instalada. Esses fatores não são entradas do seletor Python. A tensão e a modalidade não podem ser deduzidas apenas da menor corrente nominal de disjuntor.

### Identidade de fontes e extratos preservados

| Arquivo | SHA-256 calculado nesta sessão |
| --- | --- |
| EDP v09 PDF, caminho completo acima | `b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810` |
| EDP v09 Markdown limpo | `36061a47dca1a3a9ff2e820936d90bc9f51a600637ad69af30272c466906c09f` |
| EDP v09 chunks JSON | `f9133f5d9599f6c6f6b104e5f9a028acefdf232f12aec99381dfee06bfdcc6cd` |
| QA_CONFERENCIA_CERTFID_TABELAS_EDP.md | `f32cedd687823bf49a64cd8edccbacf1c733263c7cb75a348b42df4662b51b08` |
| NBR_5410_original/NBR-5410.md | `c0a6b2aa1925ead4c3aa10c50f21958f8916c9e29f6871e30fc6eb8e14758fbe` |
| NBR_5410_original/NBR_5410_chunks.json | `7c95cd03fcf24475ce2f65b28a471873e30274ef66d0548aff64d772208d3d92` |
| NBR_5410_comentada/chunks_json_16_pdfs_v2/manifesto_processamento.json | `f255c262d9354e59a3552107a04684bd8bceaecb998cd63018b7469eba19eab5` |
| EXTRACAO-SIE.md | `3eadd76b16d9d690da2ed537b38b762e6f9acad6b5f08f95aa4900eb7b204a89` |
| EXTRACAO-COMPLEMENTAR-SIE.md | `9470575e948966e6bccd68817c8ffdb398385125ebb97721f7ed83d0d7dbbe00` |
| EXTRACAO-COMPLEMENTAR-SIE-2.md | `c4b2e8f557b551fad5a6ac072277258d06132abd9fa64b6cebaca22439857721` |

## 6. Casos aritméticos independentes e reprodução

Os valores dos exemplos são dados de ensaio: por exemplo, `R=7,41 Ω/km` e o par `(4 mm²,32 A)` não certificam cabo específico nem ampacidade normativa. A referência é calculada da fórmula/hipótese expressa; o valor retornado pelo legado não é o oráculo de correção. Os golden tests da fase têm outro papel: caracterizar exatamente a baseline, inclusive anomalias conhecidas.

| Caso | Conta de referência, independente da saída antiga | Observação local |
| --- | --- | --- |
| E0 — comprimento nulo | Para ambos os modelos resistivos, qualquer I/R/U positivo com `L=0` produz 0 V e 0%. | Executado com 20 A, 0 m, 7,41 Ω/km e 220 V: 0,00 V / 0,00% em ambas as funções. Não prova um circuito físico instalado. |
| E1 — monofásico | `I=20 A`, `L=30 m`, `R=7,41 Ω/km`, `U=220 V`. `2×0,03×20×7,41=8,892 V`; percentual `4,041818…%`; apresentação esperada 8,89 V / 4,04%. | Retorno efetivamente observado: 8,89 V / 4,04%. Nenhuma verificação de limite foi realizada pelo motor. |
| E2 — trifásico equilibrado resistivo | Mesmos I/L/R, `Ulinha=380 V`: `√3×0,03×20×7,41=7,700697890… V`; `2,026499…%`; apresentação 7,70 V / 2,03%. | Retorno efetivamente observado: 7,70 V / 2,03%, com cos(phi)=1 explícito. |
| E3 — condutor sintético | `Ib=20`, `f=0,8`, pares `(2,5;24)` e `(4;32)`: capacidades corrigidas 19,2 e 25,6 A; menor seção suficiente =4 mm². | Retorno 4,00 mm² e 25,60 A. A correção aritmética não valida as capacidades-base. |
| E4 — disjuntor sintético | `Ib=20`, `Iz=25,6`, catálogo 16/20/25/32 A: 20 e 25 satisfazem a relação; o menor é 20 A. | Retorno 20,00 A; outras condições de proteção não verificadas. |
| E5 — anomalia de precisão | `Ib=19,99`, capacidade-base 20, fator 0,99975: `Iz_bruta=19,995 A`. Disjuntor de 20 A é maior que Iz bruta; a relação superior falha. | O condutor retorna Iz arredondada 20,00 A e a aplicação escolhe 20 A. Defeito caracterizado; não aprovação do resultado. Gate normativo observado =False. |
| E6 — seletor simplificado | Para T/58,3 A/22,215 kW/carga trifásica verdadeira, menor corrente de catálogo ≥58,3 é 63 A, categoria T2. | Retorno T2, candidato para estudo=True, status PENDENTE e liberação=False. Isso verifica busca no catálogo, não elegibilidade da instalação. |
| E7 — entrada incompatível não barrada | U ou D/20 A/4,4 kW/presença de carga trifásica=True. Categorias U/D são mono/bifásicas no PDF local. | Executados ambos: U2 e D2, candidato=True e alertas vazios. Nenhuma incompatibilidade com a carga trifásica declarada é apontada. Liberação final continua=False. |

Comando executado com sucesso na raiz do repositório para E1–E5; ele recalcula as referências e explicita a anomalia, sem alterar produto ou resultados esperados:

```bash
PYTHONPATH=restructuring/apps/api python3 - <<'PY'
from decimal import Decimal as D, ROUND_HALF_UP
from sie_api.domain.engines import (
    calcular_queda_tensao_monofasica as mono,
    calcular_queda_tensao_trifasica_resistiva as tri,
    selecionar_condutor as cond,
    selecionar_disjuntor as prot,
)
from sie_api.application import analisar_circuito
q = lambda v: v.quantize(D('.01'), rounding=ROUND_HALF_UP)
l, ir = D('30') / D('1000'), D('20') * D('7.41')
m, t = l * ir * 2, l * ir * D(3).sqrt()
a = mono(D(20), D(30), D('7.41'), D(220))
b = tri(D(20), D(30), D('7.41'), D(380))
assert (a.queda_v, a.queda_percentual) == (q(m), q(m * 100 / 220))
assert (b.queda_v, b.queda_percentual) == (q(t), q(t * 100 / 380))
c = cond(D(20), D('.8'), ((D('2.5'), D(24)), (D(4), D(32))))
assert D(24) * D('.8') < 20 <= D(32) * D('.8')
assert (c.secao_mm2, c.capacidade_corrigida_a) == (D(4), D('25.60'))
p = prot(D(20), D('25.60'), (D(16), D(20), D(25), D(32)))
assert p.corrente_disjuntor_comercial_a == D(20)
r = analisar_circuito({
    'corrente_a': '19.99', 'comprimento_m': '1', 'tensao_v': '220',
    'fator_correcao': '.99975', 'resistencia_ohm_km': '1',
    'tabela_condutores': [{'secao_mm2': '2.5', 'capacidade_a': '20'}],
    'evidencia': {'documento': 'MOCK', 'edicao': '1', 'referencia': 'teste'},
})
iz_bruta = D(20) * D('.99975')
assert D(str(r['disjuntor']['corrente_a'])) > iz_bruta
assert r['liberado_para_uso_normativo'] is False
print('E1-E4: aritmetica conferida; E5: anomalia conhecida, Iz bruta=', iz_bruta)
PY
```

Não há caso independente executável de demanda A–I, cálculo de curto, seccionamento, neutro/PE/PEN, DR/DPS, divisão real ou balanceamento completo nesta árvore. A lacuna é explícita; esses comportamentos não são anunciados como preservados por execução.

## 7. Achados e disposição para a preservação

| Achado | Gravidade para uso técnico | Evidência/reprodução | Disposição F00 e condição futura |
| --- | --- | --- | --- |
| ENG-001 — Iz arredondada influencia escolha de In | ALTA | `engines.py:104` → `application.py:17`; caso E5 | Fixar o comportamento antigo em caracterização, registrar exceção de correção pendente e conservar bloqueio normativo. Antes de liberar esse motor: comparar capacidades com precisão integral e ter regressão independente da desigualdade. Não alterar golden antigo para apagar o defeito. |
| ENG-006 — fonte de ampacidade e R não vinculada ao cabo/método | ALTA | `application.py:15–16`, `app.js:18`; tabelas/impedância são entradas independentes | Preservar somente contrato demonstrativo. Motor normativo futuro precisa fonte/coluna/condições, identidade do condutor e R/X apropriados à seção final. |
| ENG-003 — proteção cobre apenas Ib/In/Iz | ALTA | `engines.py:54–69`; ausência dos demais parâmetros | Registrar parcialidade; não chamar “dimensionamento completo de proteção”. Critérios de curto/sobrecarga/coordenação exigem implementação e validação de fontes posteriores. |
| ENG-004 — otimizador sem dependências e com heurísticas não verificadas | ALTA | `otimizador.ts:6–20,141–199`; imports ausentes | Preservar arquivo e exceção de não execução. Nenhuma seleção C1–C6 foi comprovada. Recuperar módulos/dados completos antes de comparar equivalência. |
| ENG-005 — fontes normativas incompletas/derivadas | ALTA | NBR original PDF não localizado; v06 ausente reconhecida no QA anterior; JSON Prysmian sem PDF acessível | Inventário e hashes preservados. Tratar conteúdo como NÃO VERIFICADO quanto a edição/aplicabilidade/fidelidade integral; não inventar números substitutos. |
| ENG-002 — seleção EDP omite critérios de elegibilidade | ALTA | `edp.py:49–65`; E7; campos de rede/local/motor/geração ausentes | Preservar como estudo simplificado e `liberado=False`. Validação de topologia, demanda, local/rede, geração e condições EDP deve anteceder futura aprovação. |
| ENG-007 — extratos não são motores executáveis | ALTA | Múltiplos imports nos `EXTRACAO*` sem arquivos correspondentes | Matriz de preservação deve distinguir arquivo documental preservado de funcionalidade integral preservada. Golden do Python não cobre esses motores históricos. |
| ENG-008 — semântica divergente de C4/C5 e referência TUG | MÉDIA | Seção 3 e tabela histórica de TUG acima | Manter variantes separadas e registrar necessidade de reconciliação. Não transplantar indicadores APROVADO por coincidência de nomes. |
| ENG-009 — rastreabilidade de campo do chamador pode parecer validação | MÉDIA | `application.py:25` e rótulo herdado `edp.py:29` | Relatório deve separar referência declarada, conferência local do subconjunto e aprovação profissional. `dados_validados=True` do cliente não concede liberação (`gates.py:21–32`). |

## 8. O que impede a F00, e o que impede apenas liberação futura

Para a **F00 de diagnóstico**, seriam impeditivos: omitir um comportamento crítico identificado; ocultar a falha E5; afirmar execução do legado não disponível; apresentar golden como validação independente ou declarar homologação com base em rótulos herdados; deixar fonte/valor sem classificação; ou marcar preservação integral sem equivalência/exceção formal. A cobertura desta matriz e sua associação aos golden, riscos e preservação precisam ser conferidas no parecer final QA-02.

As lacunas históricas e os defeitos do cálculo não precisam ser corrigidos silenciosamente numa fase que congela a baseline. Podem permanecer como **exceções formais identificadas**, com comportamento caracterizado quando executável e bloqueio de uso normativo mantido. Isso não autoriza a fase de engenharia dependente a tratá-los como resolvidos. Correção de ENG-001, motores completos, fontes rastreáveis e validação profissional continuam pendências para futuros gates específicos.

Esta é uma perspectiva de revisão por IA. As três perspectivas QA previstas no artefato de fase não são três auditorias humanas independentes.
