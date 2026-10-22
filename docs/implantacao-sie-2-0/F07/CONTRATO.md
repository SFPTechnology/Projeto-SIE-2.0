# F07 — Contrato operacional do incremento

CLI: `python -m sie_api.conductor_cli restructuring/examples/f07_condutores_demo.json`.
Persistência local opcional: `--database local.sqlite --expected-revision N`, após cadastro canônico F05. Código de saída zero indica execução da análise, não aprovação: conferir `status` e critérios na saída.

API: POST `/api/v1/condutores/analisar`; PUT/GET `/api/v1/local/projetos/{UUID}/condutores`. PUT requer study e expected_revision, token local e ambiente permitido. Histórico imutável: novo UUID para cada revisão. GET informa stale, dependências de proteção e documentos. Conflito concorrente 409; entradas incompatíveis 422. Histórico retém entradas, memória e fingerprints.

Interface: `condutores.html`, link no painel, importação JSON, exemplo sintético, critérios por trecho, totais inclusive alimentadores, memória JSON e impressão pelo navegador. Editar dados invalida memória/exportação imediatamente. Requisições tardias não restauram memória de dados/API alterados.

## Grandezas e cálculo

Comprimento unidirecional em m; Rca e XL em ohm/km, para seção/material/isolação/arranjo e temperatura informados. Frequência é conferida pelo agregado F02 com a fonte ancestral. Não há conversão Rdc→Rca, extrapolação de temperatura ou impedância transportada para outra seção. Mono FN exige retorno com mesma seção para este modelo. Trifásico é equilibrado/senoidal; harmônicas, desequilíbrio, retorno desigual e carga capacitiva não pertencem ao regime aceito.

Fórmula longitudinal de regime permanente: k·L/1000·Ib·(Rca·cosφ+XL·sqrt(1−cos²φ)); k=2 mono e sqrt(3) trifásico. Modelo preexistente em voltage_checks.py com referência Schneider Electrical Installation Guide, Fig.G29. Fórmula não equivale a fluxo de carga exato, partida transitória ou homologação ABNT.

Acumulação exige percurso único, mesma base nominal, fases e cosφ, identidade explícita de fases e queda anterior à origem com fonte (inclusive zero). Outros casos ficam PENDENTE. Queda total é verificada para cada circuito/alimentador e caminho de carga; não apenas terminais. Não soma alternativas, tensões fase-neutro com fase-fase ou redes mistas sem modelo fasorial.

Precisão: entradas F07 limitadas a30 dígitos e expoente absoluto30 (agregado canônico preservado); cálculo200 dígitos. Limite de queda a menos de1e−100 ponto percentual recebe PENDENTE. Apresentação0,01 separada. Capacidade é decidida no valor integral sem arredondamento; catálogo F01 contém decimais finitos pequenos, mantidos exatos no contexto. Comparações independentes usam Fractions e erro absoluto<1e−90 para fórmula/teste irracional. Isso é tolerância matemática e não tolerância normativa.

## Critérios e segurança de conclusão

Capacidade e fatores usam somente células do servidor e condições exatas do lote F01; incompatibilidade recebe BLOQUEADO com motivo. Mínimos de fase, neutro e PE são entradas com fonte declarada; verificação retorna ATENDE_ESTUDO/REPROVADO ou PENDENTE, sem validar aplicabilidade normativa. Ausência de neutro é declaração condicionada à conexão; FN não aceita ausência. PE mínimo declarado não conclui adiabático/proteção integral.

`status=PENDENTE` permanece mesmo que todas comparações numéricas atendam. `REPROVADO` identifica falha numérica observada. `selected_commercial_section_mm2=null` é intencional: seleção automática de todos os critérios exige catálogo e referências normativas completos. Não existe rotina de escolha comercial completa neste incremento. `normative_conformity_verified=false` e `authoritative_for_sizing=false` não são aceitos como flags do cliente.

Salvar estudo invalida execuções canônicas VALID/PENDING→STALE e sinaliza documentos/proteção dependentes. Mudança de topologia, seção, Ib, percurso, método, levantamento, catálogo ou parâmetros invalida consultas de memória anteriores; histórico permanece reproduzível. Documentos externos já exportados não são apagados/revogados remotamente; seu hash/revisão precisa ser conferido antes do uso.

## Retomada específica

Para concluir a F07: incorporar fonte rastreável e condições aplicáveis para mínimos fase/neutro/PE, Rca/XL por seção e limites, ampliar catálogo necessário, implementar seleção multicritério sobre candidatos completos e comparar com casos normativos independentes auditados. Não reabrir aceites anteriores, não inventar tabelas e não declarar F08 liberada antes destes gates.
