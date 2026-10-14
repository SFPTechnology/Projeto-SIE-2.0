# Plano de Correcao C2 e Retencao da Auto-Otimizacao

**Data da analise:** 2026-07-21  
**Responsavel pela analise:** Atlas (`aiox-analyst`)  
**Escopo:** MOD-DC, C2, parametros `Ib/In/I2/Iz`, overrides por circuito e retencao da auto-otimizacao  
**Status:** InReview  
**Origem:** `docs/stories/HANDOFF-CORRECAO-C2-PROTECAO-DEFAULTS-to-DEV.md` e resultado QA `FAIL`

## 1. Objetivo

Eliminar resultados tecnicamente obsoletos depois de qualquer alteracao que possa mudar o dimensionamento ou a auto-otimizacao, mantendo a causa original investigavel: a secao de 6 mm2 em circuitos leves era coerente com `In=40 A` e `I2=58 A`, mas esses valores eram defaults globais e nao representavam a carga real.

O plano cobre duas propriedades distintas que precisam permanecer alinhadas:

1. O calculo deve usar os parametros efetivos atuais de cada circuito.
2. Um resultado retido so pode ser exibido ou reutilizado se tiver sido calculado com a mesma entrada efetiva atual.

## 2. Resultado da Varredura

### 2.1 Fluxo atualmente implementado

```text
Tela MOD-DC
  -> parametros globais e overrides
  -> POST de dimensionamento em lote
  -> resolverParametrosCircuito()
  -> sugestao de protecao quando In esta ausente
  -> dimensionarCircuito()
  -> tabela com Ib/In/I2/origem/C2
  -> auto-otimizacao por circuito
  -> localStorage da retencao
```

O motor C2 continua sendo a autoridade de verificacao. A sugestao de protecao e aplicada em `overrides.ts`; a auto-otimizacao chama o dominio por `api.otimizarCondutor`.

### 2.2 Evidencia do defeito principal

Em `src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx:230-239`, o mapa `parametrosPorCircuito` e construido a partir de `resultado.parametrosUsados`, isto e, do ultimo dimensionamento concluido. Esse mapa e passado para a assinatura da retencao.

Em `src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx:293-301`, o mesmo mapa e usado como entrada da auto-otimizacao. Consequentemente, apos o usuario alterar `In` ou `I2` globalmente:

- a assinatura pode continuar representando os parametros antigos;
- um resultado antigo pode continuar sendo exibido como retido;
- o clique em `Otimizar` pode enviar os parametros antigos para o dominio;
- a tela pode misturar parametros atuais no formulario com resultados antigos na tabela.

### 2.3 Evidencias positivas preservadas

- Os defaults globais `40/58` foram removidos da rota.
- A sugestao por circuito foi criada e marcada como `SUGESTAO`.
- Overrides customizados continuam sendo resolvidos antes do dimensionamento.
- O resultado exibe `Ib`, `In`, `I2` e origem de `In`.
- O diagnostico de C2 passou a apresentar valores numericos.
- A funcao de retencao ja descarta uma assinatura alterada em teste unitario, mas o consumidor fornece a assinatura errada quando existe resultado anterior.

### 2.4 Lacunas e riscos adjacentes

1. Nao existe teste UI do fluxo completo: calcular, otimizar, alterar `In/I2`, verificar descarte e otimizar novamente.
2. A rota pai conserva `resultado` enquanto `parametros` muda; nao existe estado explicito `resultadoDesatualizado`.
3. A retencao mistura resultado de auto-otimizacao e secao confirmada. Ambos precisam invalidar juntos.
4. O ciclo de efeitos de leitura/escrita do `localStorage` precisa evitar regravar um resultado antigo com uma assinatura nova durante a transicao.
5. `I2 = 1,45 * In` continua sendo uma sugestao provisoria. A regra final depende do dispositivo e nao deve ser promovida a decisao normativa sem validacao de produto/arquitetura.
6. A serie comercial e o piso residencial de 10 A sao decisoes de produto declaradas na story, mas devem permanecer parametrizaveis e rastreaveis.
7. O lint global possui falha pre-existente de CRLF registrada na story; isso deve ser separado da validacao da correcao.

## 3. Causa Raiz Consolidada

O sistema nao possui uma unica representacao explicita de **parametros efetivos atuais**. Hoje existem tres fontes com semanticas diferentes:

- `parametros`: formulario global atual;
- `circuitoOverrides`: customizacao atual por circuito;
- `resultado.parametrosUsados`: fotografia do ultimo calculo.

O codigo usa a terceira fonte onde deveria usar a primeira e a segunda. O defeito nao esta no algoritmo de comparacao da assinatura, mas na escolha da entrada usada para produzi-la e para chamar novamente o otimizador.

## 4. Decisoes Necessarias Antes da Implementacao

Estas decisoes devem ser registradas na story ou em decision log antes do codigo:

1. Alterar parametro global invalida automaticamente todos os resultados de dimensionamento e auto-otimizacao, ou apenas a auto-otimizacao? Recomendacao: marcar o dimensionamento como desatualizado e invalidar auto-otimizacao imediatamente.
2. Alterar um override invalida somente o circuito afetado? Recomendacao: sim.
3. Uma alteracao global que nao afeta um circuito customizado deve invalidar a retencao desse circuito? Recomendacao: nao, desde que o override efetivo continue identico e a assinatura seja calculada sobre os parametros efetivos atuais.
4. O usuario pode executar auto-otimizacao antes de clicar em `Dimensionar condutores` novamente? Recomendacao: nao para resultado global desatualizado; o botao deve exigir ou executar recalculo explicito.
5. A alteracao de `In` sem `I2` deve manter `I2` customizado, derivar sugestao ou deixar C2 pendente? A regra precisa ser explicitada; nao inferir uma escolha final do dispositivo.

## 5. Plano de Correcao por Fases

### Fase 0 - Reproducao e baseline

1. Criar um caso deterministico com ILU de 160 VA e TUG de 300 VA.
2. Registrar `Ib`, `Iz`, `In`, `I2`, secao final e criterio decisivo antes e depois da sugestao.
3. Reproduzir o defeito de retencao:
   - dimensionar com `In=10`, `I2=14,5`;
   - otimizar e confirmar a secao;
   - alterar para `In=40`, `I2=58`, sem redimensionar;
   - verificar que a retencao antiga nao aparece nem e enviada ao otimizador.
4. Repetir com a ordem inversa e com override por circuito.

**Saida:** fixture e roteiro de regressao reproduzivel.

### Fase 1 - Definir parametros efetivos atuais

1. Reutilizar `resolverParametrosCircuito()` como autoridade para combinar global, override e sugestao.
2. Criar uma funcao/adaptador puro que produza, para cada circuito, os parametros efetivos a partir de:
   - circuito atual;
   - parametros globais atuais;
   - override atual.
3. Proibir que `resultado.parametrosUsados` participe da entrada atual da auto-otimizacao ou da assinatura.
4. Manter `resultado.parametrosUsados` apenas para auditoria do calculo que ja ocorreu.
5. Garantir que o adaptador preserve `GLOBAL`, `CUSTOMIZADO`, `SUGESTAO`, `INFORMADO` e os campos de fonte.

**Saida:** um mapa de parametros atuais efetivos, independente do ultimo resultado.

### Fase 2 - Corrigir assinatura e invalidacao

1. Alterar `mapearAssinaturasRetencaoAutoOtimizacao()` para receber os parametros efetivos atuais, nao parametros historicos.
2. Incluir na assinatura apenas dados que realmente alteram o resultado:
   - circuito e retornos downstream;
   - parametros efetivos de calculo;
   - origem/fonte de protecao;
   - versao da base normativa, se aplicavel ao contrato.
3. Manter a assinatura deterministica, com serializacao estavel.
4. Incrementar a versao do payload de retencao se o formato mudar; payload antigo deve ser descartado sem erro.
5. Garantir descarte atomico de `resultadosOtimizacao` e `secoesConfirmadas` quando a assinatura nao coincidir.
6. Evitar o ciclo `leitura -> escrita` regravar estado antigo com assinatura nova. A escrita deve ocorrer somente depois que o estado carregado estiver sincronizado com a assinatura atual.

**Saida:** qualquer mudanca efetiva remove imediatamente o resultado retido correspondente.

### Fase 3 - Corrigir entrada da auto-otimizacao

1. Em `executarOtimizacao()`, usar o mapa de parametros efetivos atuais.
2. Nunca usar `resultado.parametrosUsados` como fallback para uma nova chamada.
3. Antes da chamada, verificar que o resultado base visivel corresponde aos mesmos parametros atuais; se nao corresponder, bloquear com estado explicito ou exigir novo dimensionamento.
4. Depois de uma nova otimizacao, armazenar a assinatura usada junto do resultado, mesmo que a persistencia continue em `localStorage`.

**Saida:** o botao `Otimizar` calcula sempre contra a entrada que o usuario esta vendo.

### Fase 4 - Tratar resultado de dimensionamento desatualizado

1. Na rota pai, separar `parametrosAtuais` de `resultadoCalculado`.
2. Criar derivacao deterministica `resultadoEstaDesatualizado` comparando parametros globais atuais, overrides atuais e parametros efetivos retornados.
3. Ao alterar parametro global, manter o resultado para auditoria visual, mas marcar claramente como desatualizado e impedir uso silencioso para novas acoes.
4. Ao salvar um override sem recalcular, marcar somente o circuito como desatualizado.
5. Ao recalcular, substituir resultado e remover o marcador de desatualizacao.
6. Nao alterar o contrato normativo do motor C2; esta fase trata estado de aplicacao e observabilidade.

**Saida:** nenhuma tabela apresenta resultado antigo como se fosse atual.

### Fase 5 - Preservar regras de protecao

1. Manter prioridade de `In/I2` informados manualmente.
2. Manter overrides por circuito acima do global.
3. Aplicar sugestao somente quando `In` estiver ausente, conforme a decisao registrada.
4. Exibir origem e fonte da protecao em todas as saidas relevantes.
5. Manter C2 como verificador de `Ib <= In <= Iz` e `I2 <= limite`; nao mover regra normativa para a UI.
6. Registrar como pendencia a natureza provisoria de `I2 = 1,45 * In` ate existir contrato de dispositivo/MOD-PROT.

**Saida:** a correcao de estado nao reintroduz defaults globais nem altera a autoridade do C2.

### Fase 6 - Testes e validacao de aceite

Implementar os cenarios abaixo antes de atualizar a story para aprovada:

#### Dominio/retencao

- assinatura muda quando `In` global muda;
- assinatura muda quando `I2` global muda;
- assinatura muda quando a sugestao muda por alteracao de `Ib`;
- override customizado permanece valido quando a alteracao global nao muda seus parametros efetivos;
- override afetado pela alteracao de origem/protecao e invalidado;
- resultado e secao confirmada sao descartados juntos;
- payload de versao antiga e ignorado;
- serializacao nao regrava resultado obsoleto com assinatura nova.

#### UI/componente

- renderizar resultado otimizado;
- alterar `In` global e verificar remocao do selo de secao confirmada;
- alterar `I2` global e verificar remocao do resultado retido;
- verificar que `Otimizar` envia os parametros atuais, nao os parametros do ultimo resultado;
- alterar override de um circuito e verificar isolamento em relacao aos demais;
- impedir ou sinalizar claramente auto-otimizacao com dimensionamento base desatualizado;
- manter exibicao de `Ib`, `In`, `I2`, `Iz`, origem e motivo C2.

#### API/servico

- lote sem protecao usa sugestao por circuito;
- lote manual preserva `INFORMADO`;
- override retorna `CUSTOMIZADO` e parametros efetivos corretos;
- auto-otimizacao direta recebe exatamente os parametros fornecidos;
- nenhuma rota passa regra normativa para a UI.

#### Ponta a ponta

- ILU 160 VA com protecao sugerida nao cai em 6 mm2 por `40/58`;
- TUG 300 VA com protecao sugerida respeita o piso C6;
- regressao explicativa `40/58` continua exigindo 6 mm2 quando esses valores sao informados conscientemente;
- alteracao de protecao seguida de nova otimizacao produz resultado diferente quando a entrada exigir isso.

### Fase 7 - Gates e entrega

Executar no submodulo:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

Executar tambem o lint focado dos arquivos alterados e documentar separadamente a falha global de CRLF, caso permaneça. Atualizar a story somente nos campos autorizados pelo agente responsavel; o QA deve registrar seu resultado em `QA Results`.

## 6. Arquivos Envolvidos

### Codigo principal

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/motores/motor-protecao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/calculo/otimizador.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`

### Testes

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/OtimizarCondutorModal.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/dimensionamento-condutores.vrt.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/dimensionamento-condutores/motor-c2-c6.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/dimensionamento-condutores/motor-protecao.test.ts`

## 7. Criterios de Aceite do Plano

- [x] Uma alteracao global em `In` invalida a auto-otimizacao retida de todos os circuitos afetados.
- [x] Uma alteracao global em `I2` invalida a auto-otimizacao retida de todos os circuitos afetados.
- [x] Um override customizado continua isolado e somente e invalidado quando seus parametros efetivos mudam.
- [x] O botao de auto-otimizacao nunca envia parametros do ultimo resultado quando existem parametros atuais diferentes.
- [x] Resultado de dimensionamento desatualizado e identificado antes de nova acao.
- [x] Resultado e secao confirmada nao ficam parcialmente retidos.
- [x] A sugestao de protecao e mantida rastreavel e nao altera o motor C2.
- [x] Os testes unitarios, UI, API e ponta a ponta cobrem a regressao.
- [x] `typecheck`, `test` e `build` passam; lint global e qualquer baseline de CRLF ficam documentados sem mascarar falhas novas.

## 8. Ordem Recomendada de Execucao

1. Fase 0: reproduzir e capturar o caso.
2. Fase 1: criar parametros efetivos atuais.
3. Fases 2 e 3: corrigir assinatura e entrada da auto-otimizacao.
4. Fase 4: marcar resultado base como desatualizado.
5. Fase 6: adicionar testes antes de refatoracoes visuais.
6. Fase 5: validar que a regra de protecao nao regrediu.
7. Fase 7: executar gates e solicitar nova revisao QA.

## 9. Decisao Analitica

O problema deve ser tratado como falha de consistencia de estado e proveniencia de parametros, nao como nova alteracao do motor C2. A correcao minima aceitavel e substituir a dependencia de `resultado.parametrosUsados` por parametros efetivos atuais derivados do formulario e dos overrides. A correcao completa inclui estado de resultado desatualizado, invalidacao atomica da retencao e testes de comportamento observavel.
