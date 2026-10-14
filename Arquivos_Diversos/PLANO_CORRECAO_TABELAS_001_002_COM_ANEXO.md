# Plano de Correcao - Tabelas 001/002 EDP com Anexo Oficial

**Data:** 2026-06-21  
**Autor:** Atlas (`aios-analyst`)  
**Objetivo:** definir um plano de correcao rastreavel para o modulo `Padrao de Entrada`, usando apenas os artefatos fornecidos e o estado atual do codigo.

## 1. Fontes consideradas

1. Prompt de correcao:
   `Arquivos_Diversos/Prompt_Correcao_Tabela_001_002_com_Anexo.md`
2. Anexo consolidado:
   `Arquivos_Diversos/tabelas_001_002_padrao_edp.md`
3. Codigo atual do modulo EDP-SP:
   `sistema-de-instala-es-el-tricas-sie-main/src/domain/distribuidora/edp-sp/`
4. Story tecnica ja existente:
   `sistema-de-instala-es-el-tricas-sie-main/docs/stories/story-4-conformidade-edp-sp.md`

## 2. Resumo executivo

O prompt define uma correcao fail-closed e auditavel: nenhuma subcategoria, disjuntor ou secao de condutor pode sair do sistema sem linha de origem, status da linha e validacao estrutural. O anexo fornece a base normativa consolidada para as 13 subcategorias oficiais (`U2`, `D2`, `D4`, `D6`, `D7`, `D9`, `D10`, `T2`, `T4`, `T6`, `T7`, `T9`, `T10`).

O codigo atual ja esta em estado melhor do que o defeito historico descrito no prompt, porque:

- o runtime ja carrega um catalogo preenchido em `subcategorias-fornecimento.catalogo.data.json`;
- o seletor ja escolhe a menor subcategoria suficiente por categoria em `seletor-subcategoria.ts`;
- a Saida B ja volta `null` quando o catalogo vier vazio em `contratos.ts`.

Mas o alvo do prompt ainda nao foi atingido integralmente. Permanecem lacunas importantes:

1. A Saida B nao publica `fonte_linha` nem `status_linha`.
2. O seletor nao valida `IB <= In <= Iz` antes de devolver a linha.
3. O seletor nao trata linha `VERIFICAR` como bloqueio ou confirmacao humana.
4. O status do catalogo e global (`VERIFICADO`) e nao por linha.
5. O editor de parametros ainda permite inserir linha manual com exemplo hardcoded.
6. O editor exibe referencia de fonte `PT.DT.PDN.03.14.020 v06`, enquanto o anexo e o catalogo gerado apontam para `PT.DT.PDN.00068 v09`.
7. O script de ingestao deriva `corrente_demanda_max_A` a partir da secao 22 do anexo consolidado e nao de um campo explicito da tabela oficial.

Conclusao: o plano correto nao e "popular tabela vazia", e sim fechar o delta entre o estado atual do repositorio e o estado auditavel exigido pelo prompt.

## 3. Diagnostico consolidado

### 3.1 Requisito-alvo do prompt

O prompt exige, simultaneamente:

- eliminacao total de fallback silencioso;
- importacao fiel do anexo sem inventar numeros;
- algoritmo de selecao por menor faixa suficiente dentro da categoria;
- validacao estrutural da linha antes da publicacao;
- diagnosticos claros quando nao houver cobertura;
- rastreabilidade ate a linha de origem na Saida B e na UI.

### 3.2 Estado atual do codigo

Arquivos centrais identificados:

- `src/domain/distribuidora/edp-sp/seletor-subcategoria.ts`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.ts`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json`
- `src/domain/distribuidora/edp-sp/contratos.ts`
- `src/components/app/edp-sp/ParametrosEDPEditor.tsx`
- `scripts/ingest-edp-tabelas-001-002.mjs`
- `src/domain/distribuidora/edp-sp/__tests__/seletor-subcategoria.test.ts`
- `src/domain/distribuidora/edp-sp/__tests__/contratos.test.ts`

Leitura objetiva do estado atual:

- `seletor-subcategoria.ts` filtra por categoria e escolhe a menor linha com `corrente_demanda_max_A >= I_A`.
- `contratos.ts` zera `sub_categoria`, `disjuntor_A` e `condutor_mm2` quando a selecao nao estiver em `status: "ok"`.
- `subcategorias-fornecimento.ts` valida integridade basica do catalogo, mas nao calcula nem bloqueia `In <= Iz`.
- `ParametrosEDPEditor.tsx` ainda contem comportamento manual legado:
  - texto de aba dizendo que as tabelas podem estar vazias;
  - botao de adicionar linha com default `U2 / U / 50 A / 50 A / 10 mm2`;
  - cabecalho de fonte apontando para `v06`.
- `ingest-edp-tabelas-001-002.mjs` ja gera o catalogo a partir do anexo consolidado, mas:
  - marca o catalogo inteiro como `VERIFICADO`;
  - usa faixas da secao 22 para `corrente_demanda_max_A`;
  - nao registra status por linha nem motivo por linha.

### 3.3 Gap entre estado atual e estado-alvo

| Tema | Estado atual | Estado-alvo |
|---|---|---|
| Origem na Saida B | so retorna subcategoria/disjuntor/secao | retornar tambem `fonte_linha` e `status_linha` |
| Status de verificacao | status global do catalogo | status por linha com motivo estruturado |
| Validacao de ampacidade | inexistente na selecao | bloquear linha que viole `IB <= In <= Iz` |
| Linha provisoria | nao existe fluxo especial | `VERIFICAR` nao pode ser publicada automaticamente |
| UI de parametros | ainda aceita insercao manual exemplificativa | importacao controlada, diff e bloqueios |
| Auditoria reversa | nao existe exportacao especifica do importado | exportar CSV auditavel e comparavel ao anexo |
| Fonte normativa | conflito entre `v06` e `v09` | decisao explicita de governanca e rastreio no catalogo |

## 4. Divergencias entre artefatos que precisam ser decididas antes da implementacao

### 4.1 Versao normativa

Ha divergencia objetiva entre os artefatos:

- o prompt e a UI atual citam `PT.DT.PDN.03.14.020 v06`;
- o anexo consolidado e o catalogo gerado citam `PT.DT.PDN.00068 v09`.

Decisao obrigatoria:

1. confirmar qual documento e a fonte normativa oficial que deve governar o sistema;
2. congelar essa decisao em metadata do catalogo, testes e UI;
3. se o repositorio continuar usando o anexo consolidado atual, a UI nao pode continuar anunciando `v06`.

### 4.2 Origem de `corrente_demanda_max_A`

No repositorio atual, `corrente_demanda_max_A` e derivada da secao 22 do anexo consolidado, nao da tabela resumida oficial de secoes 13 e 15. Isso nao invalida o uso do anexo, mas exige transparencia.

Decisao obrigatoria:

- ou manter essa derivacao com `fonte_linha` explicita dizendo que a faixa veio da secao 22 da consolidacao;
- ou exigir um artefato oficial bruto que traga a faixa diretamente.

Enquanto isso nao for esclarecido, o plano deve tratar essa faixa como dado auditavel do anexo consolidado, e nao como inferencia "de memoria".

## 5. Plano de correcao proposto

## Fase 0 - Governanca da fonte e congelamento do escopo

**Objetivo:** impedir que a equipe corrija o comportamento tecnico usando referencia normativa ambigua.

**Acoes:**

1. Registrar a decisao de fonte normativa oficial para a correcao.
2. Atualizar o cabecalho da UI, o catalogo e os testes para a mesma referencia.
3. Documentar se `corrente_demanda_max_A` vem:
   - da tabela oficial;
   - ou da secao 22 do anexo consolidado.
4. Definir o criterio de promocao de `VERIFICAR` para `VERIFICADO` por linha.

**Arquivos impactados:**

- `src/components/app/edp-sp/ParametrosEDPEditor.tsx`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json`
- `scripts/ingest-edp-tabelas-001-002.mjs`
- `docs/stories/story-4-conformidade-edp-sp.md`

**Criterio de aceite:**

- nao existe mais referencia simultanea e contraditoria entre `v06` e `v09` nos artefatos ativos da funcionalidade;
- o catalogo declara claramente a origem de cada campo normativo usado pelo seletor.

## Fase 1 - Eliminar residuos de fallback e exemplos operacionais indevidos

**Objetivo:** remover qualquer caminho que reintroduza numeros exemplificativos ou comportamento manual enganoso.

**Acoes:**

1. Remover do editor o `Adicionar linha` com default hardcoded.
2. Remover mensagens que assumem "default vazio" como comportamento esperado quando o sistema passar a operar por importacao controlada.
3. Garantir que a unica forma de popular subcategorias produtivas seja:
   - catalogo versionado gerado por ingestao;
   - ou importacao auditada via fluxo explicito.
4. Revisar testes e fixtures que ainda usem valores exemplificativos sem provenance.

**Arquivos impactados:**

- `src/components/app/edp-sp/ParametrosEDPEditor.tsx`
- `src/domain/distribuidora/edp-sp/__tests__/contratos.test.ts`
- `src/domain/distribuidora/edp-sp/__tests__/parametros.test.ts`

**Criterio de aceite:**

- o front nao sugere nem cria linha normativa ficticia;
- nao existe UX que normalize preenchimento manual ad hoc das Tabelas 001/002.

## Fase 2 - Remodelar o catalogo para rastreabilidade por linha

**Objetivo:** tornar cada linha da tabela uma unidade auditavel completa.

**Acoes:**

1. Evoluir o modelo de `CategoriaAtendimentoEstruturalEDP` para incluir, por linha:
   - `fonte_linha`;
   - `status_linha`;
   - `motivos_verificacao`;
   - flag de origem da faixa de corrente, quando vier da secao 22.
2. Adaptar `subcategorias-fornecimento.ts` para expor tambem esses campos ao dominio.
3. Ajustar `ingest-edp-tabelas-001-002.mjs` para classificar cada linha como:
   - `VERIFICADO`;
   - `VERIFICAR`.
4. Implementar checagens estruturais na ingestao:
   - prefixo x categoria;
   - monotonicidade por categoria;
   - consistencia de `disjuntor_A`;
   - cobertura dos 13 IDs oficiais;
   - preparacao dos dados necessarios para a regra `In <= Iz`.
5. Importar mesmo a linha suspeita, mas carregar o motivo no catalogo.

**Arquivos impactados:**

- `scripts/ingest-edp-tabelas-001-002.mjs`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.ts`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json`
- `src/domain/distribuidora/edp-sp/__tests__/subcategorias-fornecimento.test.ts`

**Criterio de aceite:**

- cada uma das 13 linhas oficiais possui status proprio e provenance propria;
- qualquer anomalia estrutural fica visivel no catalogo, sem alteracao do numero de origem.

## Fase 3 - Reescrever a selecao para fail-closed com validacao tecnica

**Objetivo:** impedir publicacao automatica de linha sem validacao completa.

**Acoes:**

1. Evoluir `ResultadoSubcategoria` para comportar:
   - sucesso validado;
   - linha provisoria;
   - ausencia por tabela vazia;
   - ausencia por categoria sem linhas validas;
   - ausencia por corrente acima do maior padrao;
   - ausencia por linha inconsistente.
2. Validar, antes de devolver a linha:
   - `I_A <= corrente_demanda_max_A`;
   - `I_A <= disjuntor_A`;
   - `disjuntor_A <= ampacidade(secao)`.
3. Recusar selecao automatica de linha `VERIFICAR`.
4. Nunca cruzar letras de categoria.
5. Propagar `fonte_linha` e `status_linha` para a Saida B.

**Arquivos impactados:**

- `src/domain/distribuidora/edp-sp/seletor-subcategoria.ts`
- `src/domain/distribuidora/edp-sp/contratos.ts`
- `src/domain/distribuidora/edp-sp/validacao.ts`
- `src/domain/distribuidora/edp-sp/motor-edp-sp.ts`
- `src/domain/distribuidora/edp-sp/__tests__/seletor-subcategoria.test.ts`
- `src/domain/distribuidora/edp-sp/__tests__/contratos.test.ts`
- `tests/api/padrao-entrada.test.ts`

**Criterio de aceite:**

- para corrente `107.4 A` na categoria `T`, a resposta so pode sair se a linha candidata estiver validada e rastreavel;
- a Saida B sempre carrega `sub_categoria`, `disjuntor_A`, `condutor_mm2`, `fonte_linha` e `status_linha`, ou tudo nulo com diagnostico.

## Fase 4 - Diagnosticos, UI e auditoria reversa

**Objetivo:** tornar o comportamento transparente para usuario e auditor.

**Acoes:**

1. Exibir diagnosticos dedicados:
   - `ERRO - TABELA-001-002-VAZIA`
   - `ERRO - CATEGORIA-SEM-LINHAS`
   - `ERRO - CORRENTE-ACIMA-DO-MAIOR-PADRAO`
   - `ERRO - LINHA-INCONSISTENTE`
   - `ATENCAO - LINHA-PROVISORIA`
   - `ATENCAO - SUB-CAT-AUSENTE`
2. Fazer a UI da aba 001/002 listar status e motivos por linha.
3. Criar fluxo de importacao com diff antes de salvar.
4. Criar exportacao CSV da tabela importada para conferencia reversa.
5. Exibir no card de categoria/subcategoria o rastro para a linha de origem.

**Arquivos impactados:**

- `src/components/app/edp-sp/ParametrosEDPEditor.tsx`
- `src/components/app/edp-sp/CategoriaSubcategoriaCard.tsx`
- `src/components/app/edp-sp/ContratosEDPCard.tsx`
- `src/components/app/edp-sp/DiagnosticosEDPCard.tsx`
- `src/routes/api/v1/distribuidora/edp-sp.parametros.ts`
- `src/domain/servicos/servico-parametros-edp.ts`

**Criterio de aceite:**

- o usuario consegue ver a linha exata que originou a resposta;
- o sistema consegue exportar a tabela importada para conferencia humana.

## Fase 5 - Evidencia, testes e gate de qualidade

**Objetivo:** fechar a correcao com prova reproduzivel e alinhada ao `AGENTS.md`.

**Acoes:**

1. Atualizar checklist e file list da story relacionada.
2. Cobrir testes de:
   - tabela vazia;
   - categoria sem linhas validas;
   - corrente na fronteira;
   - linha `VERIFICAR`;
   - linha com violacao `In <= Iz`;
   - exportacao reversa;
   - divergencia de source metadata.
3. Rodar gates obrigatorios:
   - `npm run lint`
   - `npm run typecheck`
   - `npm test`

**Arquivos impactados:**

- `docs/stories/story-4-conformidade-edp-sp.md`
- `src/domain/distribuidora/edp-sp/__tests__/...`
- `tests/api/parametros-edp.test.ts`
- `tests/api/padrao-entrada.test.ts`

**Criterio de aceite:**

- o comportamento fail-closed esta coberto por teste automatizado;
- a story reflete exatamente o que foi alterado;
- os gates de qualidade passam.

## 6. Base normativa minima a preservar no catalogo

Os degraus abaixo sao os que aparecem no anexo consolidado e hoje alimentam o catalogo do sistema:

| ID | Categoria | Corrente max A | Disjuntor A | Condutor EPR/XLPE mm2 |
|---|---:|---:|---:|---:|
| U2 | U | 70 | 70 | responsabilidade_distribuidora |
| D2 | D | 63 | 63 | responsabilidade_distribuidora |
| D4 | D | 100 | 100 | 25 |
| D6 | D | 150 | 150 | 50 |
| D7 | D | 200 | 200 | 70 |
| D9 | D | 300 | 300 | 120 |
| D10 | D | 350 | 350 | 185 |
| T2 | T | 63 | 63 | responsabilidade_distribuidora |
| T4 | T | 100 | 100 | 25 |
| T6 | T | 150 | 150 | 50 |
| T7 | T | 200 | 200 | 70 |
| T9 | T | 300 | 300 | 120 |
| T10 | T | 350 | 350 | 185 |

Observacoes importantes:

1. As correntes maximas acima sao as usadas hoje pelo script de ingestao a partir da secao 22 do anexo consolidado.
2. Os condutores retornados pelo motor atual usam a projecao `condutor_entrada_epr_xlpe` quando numerica.
3. `U2`, `D2` e `T2` tem retorno `null` para `secao_mm2` no motor atual quando a fonte diz "responsabilidade da distribuidora"; isso deve permanecer explicito e rastreavel.

## 7. Priorizacao recomendada

1. Resolver a governanca da fonte (`v06` x `v09`).
2. Remover defaults manuais do editor.
3. Introduzir status por linha e motivos.
4. Reforcar seletor e contratos com provenance e bloqueios tecnicos.
5. Fechar UX de importacao/exportacao e diagnosticos.
6. Congelar tudo com testes e atualizacao da story.

## 8. Riscos e pontos de atencao

1. Se a divergencia `v06` x `v09` nao for resolvida, a correcao continua auditavelmente fraca.
2. Se `corrente_demanda_max_A` continuar sendo derivada sem provenance explicita, a rastreabilidade fica incompleta.
3. Se a ampacidade nao for ancorada em fonte declarada, a regra `In <= Iz` vira opinativa, o que o prompt proibe.
4. Se a UI continuar permitindo edicao manual livre das subcategorias, o sistema volta a aceitar numeros sem cadeia de custodia.

## 9. Estimativa derivada dos artefatos existentes

A story tecnica existente (`story-4-conformidade-edp-sp.md`) estima de `64-96 h` para a frente mais ampla de conformidade EDP-SP. Para esta correcao especifica de rastreabilidade das Tabelas 001/002, a execucao pratica tende a se concentrar em:

- dominio e ingestao;
- contratos e diagnosticos;
- UI de parametros/auditoria;
- testes.

Essa estimativa deve ser refinada somente depois da decisao formal sobre a fonte normativa e sobre a tabela de ampacidade de referencia.

## 10. Resultado esperado ao final

Ao concluir este plano, o sistema deve operar assim:

1. Seleciona subcategoria somente a partir de linha importada e identificavel.
2. Publica na Saida B a cadeia completa de rastreabilidade.
3. Falha de forma honesta quando faltar cobertura ou consistencia.
4. Nao permite que UI ou script reintroduzam valores exemplificativos.
5. Permite auditoria reversa do dado exibido ate o anexo de origem.

## 11. Recomendacao final

O melhor caminho nao e reabrir a implementacao do zero. O repositorio ja possui:

- catalogo estruturado;
- seletor funcional por faixa;
- testes basicos;
- story tecnica aberta.

Portanto, a estrategia recomendada e executar uma **correcao incremental orientada a rastreabilidade**, fechando os deltas identificados neste documento, em vez de substituir todo o modulo.
