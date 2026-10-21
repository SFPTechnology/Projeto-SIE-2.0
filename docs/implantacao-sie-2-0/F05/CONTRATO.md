# F05 — Contrato e operação local

## Limites
Topologia preliminar; não dimensiona, não calcula fatores normativos, não concede conformidade e não libera curto-circuito definitivo. Dados de fonte não confirmados são preservados e sinalizados. Nenhuma geometria é inventada. Fontes múltiplas são admitidas em árvores isoladas; paralelismo/transferência automática não fazem parte deste contrato.

## Fonte de conectividade
O grafo autoritativo continua sendo `Installation` F02. Transporte `SIE_TOPOLOGY_V1`: `installation` mais `source_details`, `board_details` e `segment_details`, associados por UUID. Não alterar snapshots históricos para acrescentar campos.
No SQLite F03, `installation_snapshot` guarda exclusivamente a conectividade e grandezas F02; `topology_metadata` guarda exclusivamente os dados complementares. Não existem arestas paralelas. Metadados órfãos, barras de outro quadro, IDs duplicados e descontinuidades físicas dentro de um percurso são recusados.

`source_details`: concessionária e transformador opcionais (`null` quando desconhecidos), estado PENDING/DECLARED/CONFIRMED, origem/método, impedância R/X em ohm opcional com frequência e confirmação próprias. Confirmação cadastral não é homologação normativa.
`board_details`: origem e barras com UUID, nome, função e circuitos vinculados. Localização vem de room_id → floor → building canônicos.
`segment_details`: origem, método de obtenção, início/fim declarados, número de condutores, material da passagem, ambiente, solo e influências externas declaradas. Comprimento em m, método de instalação, temperaturas, agrupamento e exposição solar permanecem no trecho canônico F02. As condições não são generalizadas para o circuito.
F05 exige `phases` explícito em cada circuito; o default histórico F02 não é usado para novos documentos F05.

## Revisão e resultados
PUT exige token local F03 e expected_revision inteiro. O projeto deve ser da rota e a revisão do modelo deve ser expected_revision+1. Conflito retorna HTTP409 sem sobrescrever; conteúdo inválido retorna422; credencial ausente401; armazenamento não configurado503. Banco temporário nos testes, nunca banco de produção.
`topology_sha256` abrange entradas físicas, elétricas e metadados; exclui resultados e contadores históricos. Alteração invalida conservadoramente todos os resultados dependentes, marcando runs VALID/PENDING como STALE. Revisões antigas permanecem consultáveis. `topology_results_stale` não é limpo por salvar ou reabrir: somente um futuro recálculo verificável poderá fazê-lo.
Uma gravação direta pela rota F02 também remove o fingerprint F05 e marca resultados desatualizados. Metadados incompatíveis serão recusados na reabertura; devem ser corrigidos/importados. Comparações F02 continuam vinculadas ao hash e revisão do snapshot. Futuros motores F06 precisam usar o documento completo e seu fingerprint, nunca apenas metadados do cliente.
O levantamento F04 é preservado; cargas canônicas F02 e cargas de levantamento F04 não são fundidas automaticamente nem duplicadas. A fase admite fixtures sintéticas coerentes como entrada.

## Percursos
O relatório percorre alimentadores ancestrais até a fonte e devolve cada circuito, seus percursos e seus trechos ordenados com condições e comprimentos próprios. Soma decimal exata somente quando existe um percurso por circuito. Vários percursos de cabo no mesmo circuito produzem AMBIGUOUS_RUNS e total nulo, sem somar alternativas como série. O documento mantém impedâncias por trecho e fonte para futuros cálculos segmentados; nenhum motor F05 de queda/falta é anunciado.

## Executar sem navegador
Na raiz, com Python e dependências da API instaladas:
```
python -m pip install -e "./restructuring/apps/api[test,e2e]"
python -m sie_api.topology_cli restructuring/examples/f05_topologia_demo.json
python -m sie_api.topology_cli restructuring/examples/f05_topologia_demo.json --database /tmp/sie-f05.sqlite --expected-revision 0
```
A segunda gravação exige edição explícita da revisão do projeto e expected-revision correspondente; não repita expected0 sobre projeto existente.
API: POST `/api/v1/topologia/validar` (relatório valid/errors/warnings); POST `/api/v1/topologia/percursos` (documento tipado); GET/PUT `/api/v1/local/projetos/{uuid}/topologia` (token opt-in).

## Editor técnico passo a passo
1. Abra `topologia.html` pelo servidor estático usado pelo projeto, a partir do atalho **Topologia elétrica** no painel. Configure a API local; use token somente para persistir/reabrir.
2. Clique **Abrir exemplo sintético** para conhecer QDG → QD1 → circuitos. Esses dados não servem para obra real. Para dados próprios, importe JSON F05.
3. Selecione circuito/alimentador; confira quadro, dispositivo, destino e cargas. Aplique vínculos ao rascunho. Circuito final exige cargas; alimentador exige quadro descendente.
4. Selecione trecho físico; edite comprimento, método, temperatura e agrupamento. Clique **Aplicar trecho ao rascunho**. Os demais trechos mantêm suas próprias condições.
5. Use **Documento completo** para cadastrar ou incluir fontes, barras, quadros, dispositivos, trechos e seus metadados. UUID único é obrigatório. A inclusão é técnica, via JSON estruturado, sem editor gráfico de desenho.
6. Clique **Validar e recompor percursos**. Corrija erros; o botão de trecho leva à seleção afetada. Leia avisos de fonte e percurso declarado. Não confunda integridade com aprovação de engenharia.
7. Informe token e **Validar e salvar nova revisão**. Em409, **Reabrir projeto salvo**, reconcilie o rascunho e tente novamente. Não há sobrescrita forçada.
8. **Desfazer rascunho** restaura a última abertura; **Exportar rascunho JSON** permite guardar o documento. Rascunhos não persistidos não sobrevivem ao fechamento da página. O token não é guardado em localStorage nem incluído na exportação.
