# Execução da correção do Padrão compatível — EDP São Paulo V9

**Status:** guia operacional para criação de stories e execução incremental  
**Escopo:** campo "Padrão compatível" da rota EDP São Paulo V9  
**PRD base:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Plano base:** `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`  
**QA preflight:** `docs/qa/QA-PREFLIGHT-SDC-EDP-V9.md`  
**Fonte normativa oficial DP-01/DP-05:** `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`

## 1. Objetivo

Executar a correção do campo "Padrão compatível" sem transformar um defeito de interface em ajuste superficial. O comportamento visto na tela ocorre porque a rota EDP ainda passa pelo catálogo genérico de fornecimento e, quando o motor retorna `sem-padrao`, o componente `FornecimentoSelector` monta um conjunto vazio de candidatos válidos e desabilita todas as opções.

A correção deve produzir um resultado canônico EDP V9, rastreável e compartilhado por CLI, API, UI, Correntes, Dimensionamento, Unifilar e Relatório. A UI só deve ser alterada depois de existir domínio capaz de avaliar alternativas EDP V9 com estado, motivo e próxima ação.

## 2. Estado atual e limite de autorização

O QA preflight vigente liberou somente o **Pacote 1 — Modelo normativo e catálogo estrutural** para criação de stories. Pacotes posteriores permanecem em `HOLD` ou `BLOCK` até seus gates próprios.

Consequências práticas:

- `@sm` e `@po` podem criar stories do pacote 1.
- `@dev` não deve implementar código EDP V9 sem story válida.
- A correção visual do seletor não deve ser iniciada antes do contrato e do catálogo EDP V9.
- A Release 1 EDP V9 ainda não está autorizada para ativação.
- Remoção do legado ou do catálogo genérico fora da rota EDP não está autorizada.

## 3. Artefatos de entrada obrigatórios

Antes de iniciar qualquer story, conferir:

- `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`
- `docs/qa/QA-PREFLIGHT-SDC-EDP-V9.md`
- `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`
- `docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md`
- `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md`
- `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md`
- `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md`
- `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`
- Código brownfield:
  - `sistema-de-instala-es-el-tricas-sie-main/src/components/app/FornecimentoSelector.tsx`
  - `sistema-de-instala-es-el-tricas-sie-main/src/domain/nbr/catalogo-fornecimento.data.json`
  - `sistema-de-instala-es-el-tricas-sie-main/src/domain/calculo/padrao-entrada.ts`
  - `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-padrao-entrada.ts`
  - `sistema-de-instala-es-el-tricas-sie-main/src/domain/distribuidora/edp-sp/`

## 4. Sequência executiva

### Passo 1 — Criar a story implementável do Pacote 1

**Responsáveis:** `@sm` ou `@po`  
**Autoridade:** criação de story  
**Resultado esperado:** uma ou mais stories em `docs/stories/` cobrindo o modelo normativo e catálogo estrutural EDP V9.

#### Como executar

1. Abrir o QA preflight e confirmar que o pacote 1 está em `PASS — LIBERADO`.
2. Abrir o PRD e extrair somente requisitos do pacote 1, sem trazer implementação dos pacotes 2 a 8.
3. Criar story em `docs/stories/` com status inicial adequado ao workflow local.
4. Rastrear cada critério para FR, NFR, CR, AC, DP-01, DP-05, RV-01 e DP-10 quando aplicável.
5. Declarar explicitamente fora de escopo:
   - alterar UI final do seletor;
   - persistir decisão final de usuário;
   - ativar Release 1;
   - remover catálogo genérico;
   - implementar fluxo completo de motor/API/UI.
6. Incluir File List inicial com arquivos prováveis, mantendo a lista aberta para ajuste durante implementação.

#### Critérios mínimos da story

- Representar sistemas EDP V9 sem depender do catálogo genérico.
- Representar estrela e delta no modelo, mesmo que a ativação operacional do delta seja faseada.
- Registrar documento, versão, fonte normativa, hash/fonte do catálogo e proveniência.
- Modelar estados pendentes, fora de escopo, análise da concessionária e estudo técnico.
- Impedir que topologia seja inferida automaticamente por município.
- Manter confirmação técnica por projeto como condição fail-closed de DP-01.
- Garantir que `380 V` não seja alternativa EDP V9.

#### Saída do passo

- Story criada e pronta para validação por `@po`/`@sm`.
- Nenhum código alterado ainda.

### Passo 2 — Definir o catálogo EDP V9 canônico, versionado e rastreável

**Responsável de implementação:** `@dev`, somente após story válida  
**Dependência:** story do passo 1 aprovada  
**Resultado esperado:** estrutura de catálogo EDP V9 separada do catálogo genérico.

#### Como executar

1. Criar ou ajustar tipos do domínio EDP V9 em `src/domain/distribuidora/edp-sp/`.
2. Separar as dimensões normativas que hoje estão colapsadas em opções genéricas:
   - distribuidora;
   - área de concessão;
   - unidade individual;
   - tipo de rede;
   - topologia;
   - sistema;
   - tensões;
   - categoria;
   - subcategoria;
   - limites e estados especiais.
3. Usar a fonte normativa oficial `PT.DT.PDN.00068_V9_chunks.json` como referência de consulta para DP-01 e DP-05.
4. Preservar o catálogo genérico `src/domain/nbr/catalogo-fornecimento.data.json` para contextos não EDP.
5. Criar validação estrutural do catálogo EDP:
   - IDs únicos;
   - versão normativa obrigatória;
   - fonte obrigatória;
   - ausência de `380 V`;
   - estados explícitos para pendência e fora de escopo;
   - nenhuma categoria inventada quando a norma exigir análise ou estudo.
6. Criar testes unitários do catálogo e dos tipos.

#### Critérios de saída

- A rota EDP tem catálogo próprio e não depende de `catalogoFornecimentoDefault()`.
- Nenhuma opção EDP V9 vem do catálogo `GENERICO`.
- Metadados normativos são obrigatórios.
- `380 V` não passa em validação EDP.

### Passo 3 — Corrigir a regra de candidatos antes da UI

**Responsável de implementação:** `@dev`  
**Dependência:** catálogo/modelo EDP V9 do passo 2  
**Resultado esperado:** avaliador de candidatos EDP V9 retorna alternativas com estado e motivo.

#### Como executar

1. Implementar uma função pura de avaliação EDP V9 no domínio, sem dependência de React, API ou Supabase.
2. Definir um contrato de retorno com, no mínimo:
   - status global;
   - padrão recomendado quando houver;
   - lista de alternativas avaliadas;
   - motivo de validade ou incompatibilidade por alternativa;
   - próxima ação;
   - entradas usadas;
   - versão/fonte normativa;
   - estado de obsolescência quando aplicável.
3. Substituir a lógica "sem-padrao = lista vazia" por estados acionáveis.
4. Cobrir os estados obrigatórios do PRD:
   - compatível;
   - pendente de consulta à concessionária;
   - pendente de confirmação técnica;
   - fora da área de concessão;
   - requer análise da concessionária;
   - requer estudo técnico;
   - demanda acima do limite;
   - delta representável, mas operacionalmente bloqueado quando aplicável.
5. Garantir que cargas com tensão fixa sejam avaliadas, mas nunca alteradas silenciosamente.
6. Escrever testes de fronteira:
   - 12 kW;
   - 25 kW;
   - 75 kW;
   - carga com 127/220 V;
   - tentativa de 380 V;
   - ausência de topologia;
   - município fora da área EDP-SP;
   - equipamento especial sem dados suficientes.

#### Critérios de saída

- O domínio consegue explicar por que uma alternativa é compatível, incompatível ou pendente.
- Nenhum caso EDP V9 retorna apenas uma lista vazia sem motivo.
- A UI ainda pode não estar reestruturada, mas já existe contrato correto para consumi-la.

### Passo 4 — Substituir a origem das opções da rota EDP

**Responsável de implementação:** `@dev`  
**Dependência:** avaliador EDP V9 do passo 3  
**Resultado esperado:** a rota EDP deixa de montar opções a partir de `estado.config.catalogo`.

#### Como executar

1. Ajustar `servico-padrao-entrada` para expor o resultado EDP V9 canônico.
2. Garantir que `ResultadoTelaPadraoEntrada.edpSp` contenha alternativas avaliadas suficientes para a tela.
3. Manter o contrato genérico disponível apenas como legado, diagnóstico ou contexto não EDP.
4. Ajustar API/serviço para rejeitar seleção EDP baseada em ID genérico.
5. Garantir invalidação dos consumidores downstream após mudança válida:
   - Padrão de entrada;
   - Correntes;
   - Dimensionamento;
   - Unifilar;
   - Relatório.
6. Adicionar testes de integração de serviço/API:
   - rota EDP não retorna `MONO-127`, `MONO-220`, `BI-127-220`, `TRI-220-380` como catálogo EDP;
   - seleção obsoleta é rejeitada;
   - decisão usa versão/hash do catálogo avaliado;
   - contexto não EDP continua preservado.

#### Critérios de saída

- `FornecimentoSelector` ou seu sucessor não precisa mais ler `estado.config.catalogo` para contexto EDP.
- O servidor valida a seleção contra o avaliador EDP V9, não contra o catálogo genérico.
- A rota EDP não produz novos resultados pelo contrato genérico.

### Passo 5 — Bloquear 380 V no contexto EDP V9

**Responsável de implementação:** `@dev`  
**Dependência:** passos 2 a 4  
**Resultado esperado:** `380 V` não aparece, não é salvo e não é publicado em projeto EDP V9.

#### Como executar

1. Localizar todos os usos EDP de `380` no domínio, testes, UI e contratos.
2. Classificar cada ocorrência:
   - contexto genérico fora de EDP;
   - dado legado somente leitura;
   - fixture/teste antigo;
   - candidato publicado na rota EDP;
   - conversão indevida.
3. Preservar `380 V` somente quando o contexto for explicitamente não EDP ou histórico/diagnóstico.
4. Rejeitar `TRI-220-380` como seleção EDP V9.
5. Adicionar testes para:
   - ausência de `380 V` nas alternativas EDP;
   - rejeição de seleção genérica trifásica;
   - relatório/contrato sem publicação de `380 V` em EDP V9;
   - regressão positiva do catálogo genérico fora da EDP.
6. Conferir critérios do PRD:
   - `FR22`;
   - `AC-18`;
   - métrica "Ocorrências de 380 V em projeto EDP V9 = 0".

#### Critérios de saída

- Nenhuma alternativa EDP V9 publica `380 V`.
- O catálogo genérico pode continuar contendo `TRI-220-380` fora da rota EDP.
- Não há conversão automática de `TRI-220-380` para padrão EDP.

### Passo 6 — Reestruturar o campo "Padrão compatível"

**Responsável de implementação:** `@dev`, após story específica e dependências anteriores  
**Dependências:** passos 2 a 5; gates de pacote aplicáveis  
**Resultado esperado:** campo deixa de ser um select mudo e passa a exibir alternativas EDP V9 avaliadas.

#### Como executar

1. Criar story específica para `PE-EDP-V9-06 — Reestruturação do campo Padrão compatível`, quando o pacote correspondente estiver liberado.
2. Substituir ou adaptar `FornecimentoSelector` para consumir o contrato EDP V9.
3. Exibir alternativas com:
   - identificação do fornecimento;
   - status;
   - motivo;
   - próxima ação;
   - pendências;
   - evidência normativa;
   - bloqueio explícito quando não selecionável.
4. Tratar o estado sem candidato automaticamente compatível sem deixar todas as opções mudas.
5. Diferenciar visualmente:
   - alternativa selecionável;
   - alternativa incompatível;
   - pendência por consulta à EDP;
   - pendência por confirmação técnica;
   - caso que exige análise/estudo;
   - fora de escopo.
6. Manter a UI como observadora do domínio:
   - não calcular regra normativa em componente React;
   - não inventar alternativa;
   - não reescrever tensão de carga;
   - não habilitar opção que o servidor rejeitaria.
7. Garantir acessibilidade e validações:
   - labels claros;
   - estado desabilitado com motivo;
   - mensagens acionáveis;
   - navegação por teclado;
   - sem dependência exclusiva de cor.
8. Atualizar testes de componente, rota e integração.

#### Critérios de saída

- `AC-01`: em estado sem candidato automaticamente compatível, o campo mostra alternativas avaliadas e motivos.
- `AC-02`: nenhuma opção da tela EDP é carregada do catálogo genérico.
- `AC-18`: não aparece `380 V` em projeto EDP V9.
- A seleção válida persiste somente se o servidor confirmar a mesma versão/hash avaliada.
- Correntes e Dimensionamento são invalidados após mudança válida.

## 5. Ordem recomendada de stories

1. `PE-EDP-V9-01` — Modelo normativo e catálogo estrutural.
2. `PE-EDP-V9-02` — Avaliador de candidatos e estados de compatibilidade.
3. `PE-EDP-V9-03` — Contrato canônico de serviço/API para EDP V9.
4. `PE-EDP-V9-04` — Persistência versionada, obsolescência e auditoria.
5. `PE-EDP-V9-05` — Integração com consumidores downstream.
6. `PE-EDP-V9-06` — Reestruturação do campo "Padrão compatível".

Somente a primeira linha está liberada agora para criação de stories pelo QA preflight vigente. As demais dependem do fechamento sequencial dos pacotes e gates correspondentes.

## 6. Comandos de validação

Executar no diretório `sistema-de-instala-es-el-tricas-sie-main` quando houver implementação:

```powershell
npm run lint
npm run typecheck
npm test
npm run build
```

Para validação documental sem implementação:

```powershell
git diff --check -- docs/EXECUCAO-CORRECAO-PADRAO-COMPATIVEL-EDP-V9.md
```

Para localizar usos críticos durante a implementação:

```powershell
rg -n "380|TRI-220-380|FornecimentoSelector|catalogoFornecimentoDefault|estado.config.catalogo|sem-padrao" sistema-de-instala-es-el-tricas-sie-main/src docs -S
```

## 7. Definition of Done mínima por story

Cada story deve fechar com:

- critérios de aceitação marcados;
- File List atualizado;
- rastreabilidade para PRD/AC/gates;
- testes adicionados ou justificativa formal de não aplicabilidade;
- `npm run lint` aprovado;
- `npm run typecheck` aprovado;
- `npm test` aprovado;
- `npm run build` aprovado quando houver alteração executável;
- registro de pendências remanescentes por pacote, sem reabrir gates já aprovados.

## 8. Riscos de execução a evitar

- Habilitar todas as opções do select sem mudar o domínio.
- Adicionar opções EDP no catálogo genérico.
- Converter `TRI-220-380` em padrão EDP.
- Inferir topologia por município.
- Tratar ausência de resposta da EDP como compatibilidade.
- Misturar regra normativa dentro de componente React.
- Persistir escolha sem versão/hash do catálogo avaliado.
- Remover catálogo genérico fora da rota EDP sem story e gate próprios.

## 9. Próxima ação

Executar `DRAFT_PACKAGE_1_STORIES` com `@sm` ou `@po`, criando a story do **Pacote 1 — Modelo normativo e catálogo estrutural**. Após validação da story, `@dev` pode iniciar a implementação limitada ao escopo aprovado.
