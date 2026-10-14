# Plano T3 — Isolação de Condutores

**Sistema:** SIE — Sistema de Instalações Elétricas
**Trilha:** 3 de 3 (independente das trilhas T1 e T2)
**Esforço:** baixo para investigar, variável para corrigir
**Prioridade:** menor do que se supunha — ver "Revisão do diagnóstico"

---

## Contexto mínimo

O SIE calcula projetos elétricos prediais de baixa tensão com rastreabilidade normativa por valor. A isolação do condutor (PVC, EPR ou XLPE) é propriedade física que afeta cálculo: PVC opera a 70 °C, EPR e XLPE a 90 °C. Isso muda capacidade de condução de corrente e, por variação de resistividade com a temperatura, também a queda de tensão.

Na NBR 5410, as tabelas de capacidade de condução separam **PVC (tabela 36)** de **EPR/XLPE (tabela 37)** — os dois últimos compartilham tabela por serem ambos de 90 °C.

---

## Revisão do diagnóstico

O levantamento técnico anterior registrava:

> Três representações do mesmo conceito. Há conversão implícita no pipeline. **Esta é a única inconsistência de tipo identificada com potencial de afetar resultado numérico.** Prioridade 🔴 3.

A leitura do código **não confirma** esse diagnóstico. Não há conversão implícita corrompendo número. O que existe é diferente e menos perigoso, mas exige decisão.

### O que realmente existe: quatro declarações desconectadas

| # | Onde | Tipo | Observação |
|---|---|---|---|
| 1 | `src/domain/modelo/projeto.ts` | `IsolacaoCondutor = "PVC" \| "EPR/XLPE"` | Campo `padraoEntradaConfig.isolacaoCondutor`. Comentário no código: *"Isolação adotada para a seção do condutor de entrada exibida na Saída B"* |
| 2 | `src/domain/queda-tensao/contratos.ts` | `IsolacaoCondutorQT = "PVC" \| "EPR" \| "XLPE"` | Campo opcional em `ContextoQuedaTensao` |
| 3 | `src/domain/dimensionamento-condutores/normativa` | `IsolacaoCondutor` | Importado por `contratos.ts`; aceita XLPE |
| 4 | `src/domain/unifilar/unifilar-graph.ts` | `UnifilarCondutores.isolacao` | Representação de saída |

**Não há conversão entre elas.** Verificado: não existe, em `src/domain/queda-tensao/`, transformação do valor agrupado `"EPR/XLPE"` do projeto para `"EPR"` ou `"XLPE"`.

### A única conversão que existe está correta

Em `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts`, dentro de `izCorrigidaParaSecao`:

```typescript
const isolacaoNormativa =
  args.parametros.isolacao === "XLPE" ? "EPR" : args.parametros.isolacao;
const linha = repo.consultarTabelaIz({
  tabela_nbr: args.parametros.isolacao === "PVC" ? "36" : "37",
  material: args.parametros.material,
  isolacao: isolacaoNormativa,
  ...
```

Tratar XLPE como EPR na consulta de Iz é **normativamente defensável**: a tabela 37 da NBR 5410 cobre ambos, por serem isolações de 90 °C. O mapeamento reflete a norma, não a contraria.

O problema aqui não é o número. É que a decisão é um ternário sem registro: nada no `RastreioValor` documenta que XLPE foi consultado na tabela 37 como EPR. Num produto cuja proposta de valor é rastreabilidade auditável, essa é a lacuna real — e é bem menor do que "resultado numérico errado".

---

## A pergunta que continua aberta

Esta é a única questão de T3 com potencial de consequência prática, e ela **não foi respondida** pela leitura de código feita até aqui.

`CONTEXTO_PADRAO_ENDPOINT`, em `src/domain/queda-tensao/motores/motor-queda-tensao.ts`, define `isolacao: "PVC"` como padrão. O campo `ContextoQuedaTensao.isolacao` é opcional.

Se o usuário declarar EPR/XLPE no projeto e o MOD-QT calcular com o padrão PVC, a queda de tensão sai **subestimada** — não por conversão errada, mas por desconexão entre a declaração e o cálculo.

**Isso pode não estar acontecendo.** É plausível que a UI de queda de tensão colete a isolação separadamente e sempre preencha o contexto, tornando o padrão inalcançável na prática. Também é plausível que a isolação do projeto sirva apenas à exibição da Saída B, como o comentário sugere, e que a duplicação seja deliberada.

Descobrir qual é o caso é o primeiro passo, e é barato.

---

## Passos

### Passo 1 — Responder a pergunta aberta

Três verificações, nesta ordem:

**1a.** Em `src/lib/api-client.ts`, a função `quedaTensaoLote` chama `quedaTensao.calcularLoteProjeto(projetoId)`. Rastrear dentro do serviço: quem monta o `ContextoQuedaTensao`? A isolação vem de `padraoEntradaConfig.isolacaoCondutor`, de outro campo, ou fica ausente e cai no padrão PVC?

**1b.** Na UI, o usuário declara isolação em quantas telas? Se declara em mais de uma, as declarações são independentes?

**1c.** Em `dimensionarLoteProjeto`, quem preenche `ParametrosDimensionamento.isolacao`? Aceita XLPE — logo, vem de algum lugar que distingue EPR de XLPE, e não do tipo agrupado do projeto.

**Saída do passo:** uma frase por caminho, dizendo de onde a isolação vem. Se algum caminho cair no padrão PVC sem declaração explícita, isso é o achado e define o resto da trilha.

### Passo 2 — Bifurcação

**Cenário A — o padrão PVC é alcançável em produção.**
Há impacto numérico real. Corrigir tornando a isolação obrigatória no contexto, em vez de opcional com padrão silencioso. O MOD-QT já tem precedente para isso: os campos controlados de `ContextoQuedaTensao` documentam a decisão *"não há valor padrão: ausência é rejeição determinística no resolvedor (decisão PO-02, fail-closed)"*. Aplicar a mesma política à isolação.

**Cenário B — a isolação sempre chega explícita.**
Não há impacto numérico. A trilha se reduz ao Passo 3, e a prioridade cai para baixa.

**Cenário C — a isolação do projeto é mesmo só para a Saída B.**
Documentar a decisão no tipo, para que a duplicação deixe de parecer inconsistência:

```typescript
/**
 * Isolação adotada APENAS para exibição da seção do condutor de entrada
 * na Saída B. NÃO alimenta MOD-QT nem MOD-DC, que recebem isolação por
 * seus próprios contratos, com granularidade EPR/XLPE separada.
 */
export type IsolacaoCondutor = "PVC" | "EPR/XLPE";
```

Renomear para `IsolacaoCondutorSaidaB` seria mais honesto, mas é mudança de superfície ampla — avaliar custo.

### Passo 3 — Rastrear a consulta à tabela

Independente do cenário. Em `izCorrigidaParaSecao`, registrar a decisão que hoje é invisível:

```typescript
const usaTabela37 = args.parametros.isolacao !== "PVC";
const isolacaoNormativa = args.parametros.isolacao === "XLPE" ? "EPR" : args.parametros.isolacao;
```

E incluir no `RastreioValor` correspondente a nota de que a tabela 37 cobre EPR e XLPE conjuntamente, com o item normativo. Isso alinha o comportamento à invariante de rastreabilidade sem alterar nenhum número.

### Passo 4 — Testes

- **Trava normativa:** PVC consulta tabela 36; EPR e XLPE consultam tabela 37 — o teste que impede alguém "corrigir" o mapeamento XLPE→EPR por engano no futuro
- **Rastreio:** o resultado para XLPE registra que a consulta usou a tabela 37 na linha de EPR
- **Cenário A, se confirmado:** ausência de isolação no contexto produz rejeição determinística, não cálculo com PVC
- **Regressão:** nenhum valor numérico de dimensionamento muda (exceto no Cenário A, onde a mudança é a correção)

---

## O que T3 não deve fazer

**Não unificar os quatro tipos numa única representação sem antes responder o Passo 1.** Se a granularidade agrupada do projeto for deliberada — porque a Saída B realmente não precisa distinguir EPR de XLPE —, unificar cria trabalho sem ganho e força uma declaração que o usuário não tem como fazer naquele contexto.

**Não migrar dados.** Um registro `"EPR/XLPE"` não carrega informação para virar `"EPR"` ou `"XLPE"`. Qualquer migration que escolha por conta própria está inventando valor normativo, o que viola a invariante central do produto. Se a unificação vier a ser necessária, o caminho é marcar os registros ambíguos com `VERIFICAR` e usar o mecanismo de pendências existente, deixando o engenheiro redeclarar ao reabrir o projeto.

**Não tratar o mapeamento XLPE→EPR como bug.** Ele reflete a norma. O que falta é registro, não correção.

---

## Riscos

| ID | Risco | Mitigação |
|---|---|---|
| T3-R1 | Refatorar tipos antes de saber se a duplicação é deliberada | Passo 1 é bloqueante |
| T3-R2 | "Corrigir" o mapeamento XLPE→EPR e quebrar a conformidade com a tabela 37 | Teste do Passo 4 trava o comportamento correto |
| T3-R3 | Cenário A confirmado e a correção mudar valores já entregues a clientes | Se houver projetos calculados com padrão PVC indevido, tratar como recálculo com justificativa registrada, conforme a invariante de override manual |

## Invariantes

| # | Invariante | Situação |
|---|---|---|
| 6 | Nenhum valor normativo inventado | **Determina o plano** — é por isso que não há migration automática |
| 12 | Todo override manual carrega origem e justificativa | Reusada se o Cenário A exigir recálculo |
| 4 | Contrato público do MOD-QT é inalterável | Preservada — mudanças vão pelo contrato interno `ContextoQuedaTensao`, como o próprio código documenta |

---

## Critérios de pronto

- [ ] Passo 1 respondido: origem da isolação documentada para MOD-QT, MOD-DC e Saída B
- [ ] Cenário identificado (A, B ou C) e registrado
- [ ] Se A: isolação deixou de ter padrão silencioso
- [ ] Se C: comentário no tipo documentando o escopo restrito
- [ ] Consulta à tabela 36/37 rastreada no resultado
- [ ] Teste travando PVC→36 e EPR/XLPE→37
- [ ] Nenhum registro histórico teve isolação escolhida automaticamente

---

## Nota sobre prioridade

O levantamento anterior classificava esta trilha como 🔴 alta, com potencial de afetar resultado numérico. A evidência de código sugere rebaixamento: a conversão existente está normativamente correta, e o único risco numérico plausível depende de um cenário ainda não confirmado.

Recomendação: executar o Passo 1 — que custa uma leitura — antes de alocar esforço de correção. Se o Cenário B ou C se confirmar, T3 é a trilha de menor urgência das três.
