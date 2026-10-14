# Plano para @dev - Motor explicativo automatico na UI de queda de tensao

Data: 2026-07-30  
Origem: `docs/analysis/SISTEMATICA-MOTOR-EXPLICACAO-AUTOMATICA-QUEDA-TENSAO.md`  
Interface alvo: secao "Simulador de cenarios" representada nas imagens de Ar-condicionado e Banheira Hidro.

## 1. Objetivo

Adicionar uma explicacao automatica, didatica e rastreavel ao simulador de cenarios de queda de tensao, sempre que um circuito estiver selecionado.

O usuario deve conseguir entender, sem consultar o rodape tecnico:

1. quais dados do circuito foram usados;
2. qual e a queda do circuito terminal;
3. qual e a queda do alimentador;
4. como a queda total foi formada;
5. quais limites foram comparados;
6. por que o circuito esta `OK`, `ACIMA` ou `PENDENTE`;
7. como interpretar cada cenario;
8. o que significa aplicar um cenario com justificativa R-11;
9. qual formula conceitual e rastreabilidade sustentam o resultado.

## 2. Principio de implementacao

Nao substituir o modelo original. A UI atual deve continuar exibindo:

1. titulo `Simulador de cenarios - {descricao}`;
2. grafico de barras com linhas de limite;
3. bloco `Queda acumulada (alimentador + circuito)`;
4. campo `Justificativa da aplicacao (R-11 - override auditado)`;
5. lista de cenarios `CEN-01`, `CEN-02`, `CEN-03`;
6. status visual `OK` ou `ACIMA`;
7. botoes `Aplicar CEN-*`;
8. rodape `Fonte: ...`.

A mudanca deve ser uma camada explicativa adicional, derivada dos mesmos dados ja calculados pelo MOD-QT.

## 3. Ponto exato de insercao na interface

Para que a mudanca seja percebida imediatamente, renderizar o painel explicativo no topo da secao do simulador:

```text
Simulador de cenarios - {descricao}

[NOVO] Motor explicativo ativo
[NOVO] Como interpretar este cenario
[NOVO] Resumo executivo + blocos didaticos

Queda de tensao por cenario - linhas de limite...
[grafico original]

Queda acumulada (alimentador + circuito)
[arvore original]

Justificativa da aplicacao...
[input original]

[linhas originais dos cenarios]

Fonte: ...
```

Nao inserir apenas abaixo da arvore, abaixo do input ou apenas no rodape, porque nessas posicoes o usuario pode abrir a tela e perceber a mesma estrutura inicial das imagens antigas.

## 4. Escopo tecnico

### 4.1 Criar motor puro de explicacao

Arquivo recomendado:

```text
sistema-de-instala-es-el-tricas-sie-main/src/components/app/queda-tensao/explicacao-queda-tensao.ts
```

Responsabilidade:

1. receber `ItemQuedaTensaoCircuito` e `ResultadoSimulacao[]`;
2. nunca recalcular queda de tensao normativa;
3. apenas interpretar campos ja calculados em `item.resultado` e `simulacao.resultado`;
4. classificar o estado em `OK`, `ACIMA_CIRCUITO`, `ACIMA_TOTAL`, `ACIMA_AMBOS` ou `PENDENTE`;
5. classificar cenarios em `resolve_total`, `melhora_mas_nao_resolve`, `mantem_ok`, `piora` ou `invalido`;
6. devolver uma estrutura pronta para renderizacao.

Contrato conceitual minimo:

```typescript
interface ExplicacaoQuedaTensao {
  circuitoId: string;
  titulo: string;
  estado: "OK" | "ACIMA_CIRCUITO" | "ACIMA_TOTAL" | "ACIMA_AMBOS" | "PENDENTE";
  resumoExecutivo: string;
  blocos: ReadonlyArray<BlocoExplicacao>;
  cenarios: ReadonlyArray<ExplicacaoCenario>;
  alertas: ReadonlyArray<string>;
}
```

### 4.2 Criar componente didatico

Arquivo recomendado:

```text
sistema-de-instala-es-el-tricas-sie-main/src/components/app/queda-tensao/PainelExplicacaoQuedaTensao.tsx
```

Responsabilidade:

1. chamar o motor puro;
2. renderizar um painel com `data-testid="qt-explicacao-automatica"`;
3. usar titulo visivel `Motor explicativo ativo`;
4. usar subtitulo `Como interpretar este cenario`;
5. exibir os blocos em ordem didatica:
   - `1. Leitura dos dados`;
   - `2. Comparacao com limites`;
   - `3. Diagnostico`;
   - `4. Interpretacao dos cenarios`;
   - `5. Decisao de aplicacao`;
   - `6. Formula e rastreabilidade`;
   - `Atencoes tecnicas`, quando houver alertas.

### 4.3 Integrar no simulador existente

Arquivo alvo:

```text
sistema-de-instala-es-el-tricas-sie-main/src/components/app/queda-tensao/PainelSimulacaoQuedaTensao.tsx
```

Acao:

1. importar `PainelExplicacaoQuedaTensao`;
2. passar `base` e `simulacoes`;
3. inserir o painel imediatamente depois do `h3` do simulador e antes do grafico;
4. preservar todo o JSX original abaixo.

### 4.4 Estilizar com destaque suficiente

Arquivo alvo:

```text
sistema-de-instala-es-el-tricas-sie-main/src/styles.css
```

Requisitos de estilo:

1. painel deve ser visualmente distinto do fundo;
2. usar borda lateral ou destaque informativo;
3. manter legibilidade em tema escuro;
4. evitar ocupar a tela inteira;
5. usar grid responsivo para blocos explicativos;
6. nao criar cards dentro de cards de forma excessiva;
7. garantir que textos longos quebrem linha sem sobrepor botoes ou grafico.

Classes sugeridas:

```text
.qt-explanation
.qt-explanation-header
.qt-explanation-kicker
.qt-explanation-grid
.qt-explanation-block
.qt-explanation-block--wide
.qt-explanation-scenarios
.qt-explanation-alerts
```

## 5. Regras de conteudo

### 5.1 Estado `PENDENTE`

Quando `item.resultado` estiver ausente, nao inferir valores. Renderizar explicacao de pendencia:

```text
Este circuito ainda nao possui resultado tecnico de queda de tensao. O sistema nao estimou valores ausentes.
```

Tambem informar a acao necessaria, quando existir alerta: comprimento, secao, perfil de cabo, topologia ou alimentador.

### 5.2 Estado `OK`

Explicar que:

1. a queda do circuito terminal atende o limite do circuito;
2. a queda acumulada atende o limite total;
3. os cenarios representam margem adicional, padronizacao ou criterio de projeto, nao correcao obrigatoria.

### 5.3 Estado `ACIMA_CIRCUITO`

Explicar que:

1. a nao conformidade esta no trecho terminal;
2. aumentar secao, reduzir comprimento ou revisar dados ataca diretamente a causa;
3. um cenario so resolve se circuito e total ficarem dentro dos limites.

### 5.4 Estado `ACIMA_TOTAL`

Explicar que:

1. o circuito terminal pode estar dentro do limite isolado;
2. a soma alimentador + circuito ultrapassa o limite total;
3. se o alimentador domina a queda, apenas alterar a secao terminal pode nao resolver.

### 5.5 Estado `ACIMA_AMBOS`

Explicar em duas partes:

1. reprova do circuito terminal;
2. reprova do total acumulado.

O melhor cenario e aquele que corrige os dois limites.

## 6. Formula e rastreabilidade

Renderizar formula conceitual conforme o metodo vindo do resultado:

```text
SIMPLIFICADO: Delta V (%) = (k x Ib x R x L / 1000) / V x 100.
COMPLETO: Delta V (%) = (k x Ib x (R x cos(phi) + X x sen(phi)) x L / 1000) / V x 100.
```

Mostrar, quando disponivel:

1. `R` em ohm/km;
2. `X` em ohm/km;
3. `L` em m;
4. `V` em V;
5. numero de fases;
6. material;
7. isolacao;
8. secao;
9. perfil de impedancia.

Se o perfil de impedancia nao estiver rastreado, exibir alerta no corpo da explicacao, nao apenas no rodape.

## 7. Regras de arredondamento e linguagem

1. Percentuais principais no texto: preferir duas casas decimais.
2. Rotulos do grafico podem continuar com uma casa decimal.
3. Diferencas entre percentuais devem ser chamadas de `p.p.`.
4. A explicacao deve mencionar que pequenas diferencas podem ocorrer por arredondamento visual.
5. Nao usar a palavra `resolve` para cenario que ainda esteja `ACIMA`.
6. Nao recomendar aplicacao automatica; aplicar e sempre decisao do projetista.

## 8. Testes obrigatorios para @dev

Arquivo alvo:

```text
sistema-de-instala-es-el-tricas-sie-main/tests/ui/queda-tensao.vrt.test.tsx
```

Adicionar ou ajustar teste para garantir:

1. existencia de `data-testid="qt-explicacao-automatica"`;
2. renderizacao de `Motor explicativo ativo`;
3. renderizacao de `Como interpretar este cenario`;
4. renderizacao dos seis blocos didaticos;
5. preservacao das strings originais:
   - `Queda de tensao por cenario`;
   - `Queda acumulada (alimentador + circuito)`;
   - `Justificativa da aplicacao`;
   - `Aplicar CEN-01`;
   - `Fonte:`;
6. painel renderizado antes do grafico no markup.

## 9. Gates de validacao

Executar no subprojeto:

```powershell
cd sistema-de-instala-es-el-tricas-sie-main
npx prettier --write src/components/app/queda-tensao/explicacao-queda-tensao.ts src/components/app/queda-tensao/PainelExplicacaoQuedaTensao.tsx src/components/app/queda-tensao/PainelSimulacaoQuedaTensao.tsx tests/ui/queda-tensao.vrt.test.tsx
npx vitest run tests/ui/queda-tensao.vrt.test.tsx -u
npx tsc --noEmit
npx eslint src/components/app/queda-tensao/explicacao-queda-tensao.ts src/components/app/queda-tensao/PainelExplicacaoQuedaTensao.tsx src/components/app/queda-tensao/PainelSimulacaoQuedaTensao.tsx tests/ui/queda-tensao.vrt.test.tsx
npm run build
npm test
```

Se `npm run lint` global for exigido pela story, executar tambem. Caso demore ou trave, registrar tempo, comando e que o lint escopado passou.

## 10. Criterios de aceite

1. Ao selecionar Ar-condicionado, a explicacao deve indicar claramente se a restricao esta no circuito, no total ou em ambos.
2. Ao selecionar Banheira Hidro, a explicacao deve indicar que o circuito esta `OK` quando circuito e total atendem.
3. A primeira dobra visual da secao deve mostrar o novo painel explicativo antes do grafico.
4. Nenhuma funcionalidade original do simulador deve desaparecer.
5. O motor deve ser deterministico: mesmos dados geram mesma explicacao.
6. O motor deve ser passivo: nao altera dados, nao aplica cenario e nao recalcula MOD-QT.
7. Alertas tecnicos devem aparecer no corpo quando impactarem interpretacao.
8. O teste VRT deve falhar se o painel for removido ou movido para depois do grafico.

## 11. Controle de risco

1. Se a tela continuar parecida com as imagens antigas, verificar se o dev server esta usando o subprojeto correto e se o painel esta realmente antes do grafico.
2. Se ja existir implementacao parcial, ajustar a implementacao existente em vez de duplicar arquivos.
3. Se houver divergencia entre valores arredondados do grafico e do texto, manter o texto com maior precisao e explicar arredondamento.
4. Se houver worktree sujo, preservar alteracoes de outros arquivos e editar somente o escopo do simulador.
5. Se nao houver story ativa para desenvolvimento, criar ou vincular uma story antes de codigo, conforme Constitution.

## 12. Handoff para @dev

Implemente o motor explicativo como camada adicional ao simulador de cenarios. A principal exigencia de UX e visibilidade imediata: o painel deve aparecer logo abaixo do titulo `Simulador de cenarios - {circuito}` e antes do grafico.

Nao remova nem reordene os blocos originais do modelo. Apenas acrescente a interpretacao automatica e ajuste estilo/testes para garantir que qualquer circuito selecionado receba uma explicacao completa, coerente e rastreavel a partir dos resultados MOD-QT existentes.
