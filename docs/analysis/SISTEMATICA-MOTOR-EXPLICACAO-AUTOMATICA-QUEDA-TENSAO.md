# Sistematica para Motor de Explicacao Automatica de Queda de Tensao

Data: 2026-07-30  
Base: `docs/analysis/EXPLICACAO-SIMULADOR-CENARIOS-QUEDA-TENSAO.md`, stories `MOD-QT-2-01`, `MOD-QT-2-02`, `MOD-QT-2-03`, contratos internos de `src/domain/queda-tensao` e servico de projeto `servico-queda-tensao`.

## 1. Objetivo

Definir uma sistematica de interpretacao, analise e explicacao passo a passo para que o sistema gere automaticamente uma explicacao completa sempre que um circuito for selecionado na tela de queda de tensao.

O motor de explicacao nao deve recalcular queda de tensao. Ele deve consumir os resultados ja calculados pelo motor MOD-QT e transformar esses dados em narrativa tecnica rastreavel, consistente e adaptada ao estado do circuito.

## 2. Principio central

A explicacao deve separar quatro camadas:

1. Dados de entrada do circuito.
2. Resultado tecnico calculado pelo MOD-QT.
3. Diagnostico de conformidade.
4. Interpretacao operacional e recomendacao de leitura.

Essa separacao impede que o usuario confunda:

1. Queda do circuito terminal.
2. Queda do alimentador.
3. Queda total acumulada.
4. Efeito dos cenarios simulados.
5. Decisao manual de aplicar um cenario.

## 3. Fontes de dados do motor de explicacao

O motor deve operar sobre dados ja existentes no dominio.

### 3.1 Entrada principal

Tipo conceitual:

```text
ExplicacaoQuedaTensaoInput
```

Campos derivados de `ItemQuedaTensaoCircuito`:

| Campo | Origem | Uso na explicacao |
|---|---|---|
| `circuito_id` | item | Identificar o circuito |
| `descricao` | item | Titulo da explicacao |
| `corrente_a` | item | Explicar corrente de projeto |
| `secao_mm2` | item | Explicar secao atual |
| `comprimento_m` | item | Explicar comprimento usado |
| `resultado` | item | Base tecnica do texto |
| `retorno_publico` | item | Compatibilidade com contrato publico |
| `alertas` | item + motor | Bloco de atencoes |
| `status` | item | Classificacao geral: `OK`, `ACIMA`, `PENDENTE` |

Campos de `ResultadoInternoQuedaTensao` quando `resultado != null`:

| Campo | Uso |
|---|---|
| `delta_v_percentual` | Queda do circuito terminal |
| `delta_v_alimentador_pct` | Queda do alimentador |
| `delta_v_total_pct` | Queda acumulada |
| `limite_circuito_pct` | Comparacao do circuito |
| `limite_total_pct` | Comparacao total |
| `atende_circuito` | Diagnostico do trecho terminal |
| `atende_total` | Diagnostico acumulado |
| `secao_requerida_mm2` | Indicacao de secao minima, quando calculada |
| `metodo_calculo` | Explicacao da formula |
| `rastreio` | Rodape tecnico e transparencia |
| `alertas` | Riscos, degradacoes ou pendencias |
| `sugestoes` | Sugestoes textuais existentes do motor |

Campos de simulacao:

| Campo | Origem | Uso |
|---|---|---|
| `base` | `simularCircuito()` | Estado atual |
| `simulacoes[]` | `ResultadoSimulacao[]` | Cenarios comparativos |
| `delta_vs_original` | simulacao | Explicar o que mudou |
| `cenario_id` | simulacao | Rotulo CEN-01, CEN-02 etc. |
| `descricao` | simulacao | Texto curto do cenario |
| `resultado` | simulacao | Novo resultado tecnico |

## 4. Estados interpretativos

Antes de renderizar texto, o motor deve classificar o circuito.

### 4.1 Estado `PENDENTE`

Condicao:

```text
item.resultado == null
ou item.status == "PENDENTE"
ou resultado.rastreio.erro existe
```

Explicacao deve responder:

1. O calculo nao foi concluido.
2. Quais dados faltam ou qual erro bloqueou o calculo.
3. Que nenhum resultado tecnico deve ser inferido.
4. Qual acao de entrada e necessaria: informar comprimento, secao, perfil de cabo, topologia ou configurar alimentador.

Frase padrao:

```text
Este circuito ainda nao possui resultado tecnico de queda de tensao. O sistema nao estimou valores ausentes. Informe os dados pendentes e recalcule antes de interpretar conformidade.
```

### 4.2 Estado `OK`

Condicao:

```text
resultado.atende_circuito == true
e resultado.atende_total == true
```

Explicacao deve responder:

1. O circuito terminal esta dentro do limite.
2. A queda acumulada tambem esta dentro do limite total.
3. Os cenarios, se existirem, representam margem adicional, nao correcao obrigatoria.

Frase padrao:

```text
O circuito atende ao criterio de queda de tensao porque a queda do circuito e a queda total acumulada permanecem dentro dos limites aplicados.
```

### 4.3 Estado `ACIMA` por circuito terminal

Condicao:

```text
resultado.atende_circuito == false
e resultado.atende_total pode ser true ou false
```

Explicacao deve priorizar:

1. A queda do circuito terminal excede o limite do circuito.
2. O problema esta no trecho final selecionado.
3. Aumentar secao, reduzir comprimento ou revisar dados do circuito pode atacar diretamente a causa.
4. Cenarios com secao maior devem ser comparados para ver quando a queda terminal cai abaixo do limite.

Frase padrao:

```text
A nao conformidade esta no circuito terminal: a queda calculada para este trecho excede o limite de circuito. Os cenarios devem ser lidos como alternativas para reduzir a queda do proprio circuito.
```

### 4.4 Estado `ACIMA` por acumulado total

Condicao:

```text
resultado.atende_circuito == true
e resultado.atende_total == false
```

Explicacao deve priorizar:

1. O circuito terminal esta dentro do limite isolado.
2. A soma alimentador + circuito excede o limite total.
3. A causa pode estar no alimentador, no circuito, ou na combinacao.
4. Se o alimentador sozinho ja estiver acima do limite total, aumentar o circuito terminal dificilmente resolve a conformidade total.

Frase padrao:

```text
O circuito terminal, isoladamente, esta dentro do limite. A reprova ocorre na queda acumulada, porque alimentador e circuito somados ultrapassam o limite total aplicado.
```

### 4.5 Estado `ACIMA` por ambos

Condicao:

```text
resultado.atende_circuito == false
e resultado.atende_total == false
```

Explicacao deve dividir o diagnostico:

1. Primeiro, reprova do circuito terminal.
2. Segundo, reprova do total acumulado.
3. O cenario ideal deve corrigir os dois limites.
4. Se um cenario corrige apenas o circuito mas nao o total, explicar que ainda ha restricao acumulada.

Frase padrao:

```text
Ha duas nao conformidades simultaneas: o circuito terminal excede seu limite e a soma com o alimentador tambem excede o limite total.
```

## 5. Pipeline de interpretacao

O motor deve seguir sempre a mesma ordem.

### Passo 1: Validar disponibilidade de resultado

```text
se resultado ausente:
  renderizar explicacao PENDENTE
  renderizar alertas
  interromper blocos de formula, grafico e cenarios tecnicos
```

### Passo 2: Normalizar numeros para exibicao

Regras:

| Tipo de valor | Exibicao recomendada |
|---|---|
| Percentual principal | 2 casas decimais |
| Rotulo de grafico | 1 casa decimal quando houver pouco espaco |
| Corrente | 2 casas decimais, preservando mais casas em rastreio tecnico se necessario |
| Comprimento | 1 ou 2 casas, conforme entrada |
| Secao | sem casa quando inteiro; manter decimal se IEC exigir |
| Tensao | sem casa quando inteiro |
| R/X | 3 casas ou valor bruto no rodape tecnico |

O texto deve explicar quando houver arredondamento:

```text
Os valores exibidos podem apresentar pequena diferenca de centesimos por arredondamento visual; o motor usa maior precisao internamente.
```

### Passo 3: Calcular componentes explicativos

O motor de explicacao pode somar valores ja calculados para fins narrativos:

```text
queda_alimentador = resultado.delta_v_alimentador_pct ?? 0
queda_circuito = resultado.delta_v_percentual
queda_total = resultado.delta_v_total_pct
limite_circuito = resultado.limite_circuito_pct
limite_total = resultado.limite_total_pct
margem_circuito = limite_circuito - queda_circuito
margem_total = limite_total - queda_total
participacao_alimentador = queda_alimentador / queda_total
participacao_circuito = queda_circuito / queda_total
```

Esses calculos sao explicativos; nao substituem o resultado do MOD-QT.

### Passo 4: Classificar causa dominante

Regra:

```text
se queda_alimentador >= limite_total:
  causa = "alimentador domina e ja excede o limite total"
senao se queda_circuito > limite_circuito:
  causa = "circuito terminal excede o limite proprio"
senao se queda_total > limite_total:
  causa = "soma acumulada excede o limite total"
senao:
  causa = "dentro dos limites"
```

Essa classificacao direciona a explicacao principal.

### Passo 5: Avaliar cenarios

Para cada simulacao:

```text
cenario.queda_circuito = simulacao.resultado.delta_v_percentual
cenario.queda_total = simulacao.resultado.delta_v_total_pct
cenario.atende_circuito = simulacao.resultado.atende_circuito
cenario.atende_total = simulacao.resultado.atende_total
cenario.status = atende_circuito && atende_total ? "OK" : "ACIMA"
cenario.reducao_circuito = base.delta_v_percentual - cenario.queda_circuito
cenario.reducao_total = base.delta_v_total_pct - cenario.queda_total
```

Classificacao de cada cenario:

| Classe | Condicao | Texto |
|---|---|---|
| `resolve_total` | base ACIMA e cenario OK | Cenario corrige a nao conformidade |
| `melhora_mas_nao_resolve` | reducao > 0 e cenario ACIMA | Cenario reduz queda, mas ainda nao aprova |
| `mantem_ok` | base OK e cenario OK | Cenario amplia margem |
| `piora` | cenario.queda_total > base.queda_total | Cenario aumenta queda |
| `invalido` | simulacao rejeitada | Nao ha resultado tecnico para esse cenario |

### Passo 6: Decidir bloco de recomendacao

O motor nao deve mandar aplicar automaticamente. A recomendacao deve ser interpretativa.

Regras:

1. Se existe cenario `resolve_total`, destacar o primeiro cenario que resolve.
2. Se todos melhoram mas continuam `ACIMA`, explicar que a causa pode estar fora do circuito terminal.
3. Se o circuito ja esta `OK`, explicar que aplicar cenario e decisao de margem, padronizacao ou criterio de projeto.
4. Se existe alerta, mencionar que a decisao deve considerar os alertas antes de aplicar.
5. Se aplicacao exige justificativa, explicar R-11: override auditado.

## 6. Blocos narrativos obrigatorios

A explicacao automatica deve ser montada por blocos independentes.

### Bloco A: Identificacao

Objetivo: dizer qual circuito esta sendo analisado.

Template:

```text
Circuito selecionado: {descricao} ({circuito_id}).
Corrente de projeto: {corrente_a} A.
Secao atual: {secao_mm2} mm2.
Comprimento considerado: {comprimento_m} m.
```

Se algum campo estiver ausente:

```text
{campo} nao informado. O sistema nao deve estimar esse valor.
```

### Bloco B: Resultado atual

Template:

```text
A queda do circuito terminal e {queda_circuito}%.
A queda do alimentador e {queda_alimentador}%.
A queda total acumulada e {queda_alimentador}% + {queda_circuito}% = {queda_total}%.
```

Se `delta_v_alimentador_pct == null`:

```text
Nao ha queda de alimentador informada; a queda total coincide com a queda do circuito terminal.
```

### Bloco C: Comparacao com limites

Template:

```text
Limite do circuito: {limite_circuito}%.
Limite total: {limite_total}%.
Circuito terminal: {queda_circuito}% {operador} {limite_circuito}% -> {status_circuito}.
Total acumulado: {queda_total}% {operador} {limite_total}% -> {status_total}.
```

Operador:

```text
<= quando atende
> quando nao atende
```

### Bloco D: Diagnostico

Selecionar pelo estado:

| Estado | Diagnostico |
|---|---|
| `OK` | O circuito e o acumulado atendem aos limites |
| `ACIMA_CIRCUITO` | O circuito terminal e o ponto critico |
| `ACIMA_TOTAL` | A soma acumulada e o ponto critico |
| `ACIMA_AMBOS` | Ha reprova simultanea no circuito e no total |
| `PENDENTE` | Faltam dados ou perfil para resultado tecnico |

### Bloco E: Formula e rastreabilidade

Template para metodo simplificado:

```text
O metodo usado foi SIMPLIFICADO. A queda e calculada com corrente, resistencia do cabo, comprimento, fator de fases e tensao nominal.
Formula conceitual: Delta V (%) = (k x Ib x R x L / 1000) / V x 100.
```

Template para metodo completo:

```text
O metodo usado foi COMPLETO. Alem da resistencia, o calculo considera a reatancia do cabo e o fator de potencia.
Formula conceitual: Delta V (%) = (k x Ib x (R x cos(phi) + X x sen(phi)) x L / 1000) / V x 100.
```

Rastreio:

```text
R={R_ohm_km} ohm/km; X={X_ohm_km} ohm/km; L={L_m} m; V={V_nominal} V; fases={num_fases}; material={material}; isolacao={isolacao}; perfil={perfil_id}.
```

Se `perfil_id` ausente em resultado tecnico, renderizar alerta forte:

```text
Perfil de impedancia nao rastreado. O resultado nao deve ser apresentado como calculo tecnico fechado.
```

### Bloco F: Cenarios

Para cada cenario:

```text
{cenario_id} - {descricao}
Mudanca: {delta_vs_original}
Queda do circuito: {queda_circuito_cenario}%.
Queda total: {queda_total_cenario}%.
Status: {status}.
Interpretacao: {classe_do_cenario}.
```

Comparacao com base:

```text
Reducao no circuito: {reducao_circuito} p.p.
Reducao no total: {reducao_total} p.p.
```

Use `p.p.` para pontos percentuais, pois a diferenca entre 6,79% e 6,55% e 0,24 ponto percentual, nao 0,24%.

### Bloco G: Decisao de aplicacao

Template:

```text
Aplicar um cenario altera a secao/comprimento do circuito, dispara recalculo do MOD-DC com a secao aplicada como piso e exige justificativa de override auditado (R-11).
```

Se cenario resolve:

```text
O primeiro cenario que resolve a conformidade e {cenario_id}. A aplicacao ainda depende de decisao do projetista e justificativa.
```

Se nenhum resolve:

```text
Os cenarios reduzem a queda, mas nenhum elimina a nao conformidade total. Revise tambem alimentador, comprimento, limite aplicado ou dados de entrada.
```

Se base ja esta OK:

```text
Como o circuito ja esta conforme, aplicar uma secao maior nao e necessario para atender queda de tensao. A decisao pode ser justificada por margem, padronizacao ou outro criterio de projeto.
```

### Bloco H: Alertas

Renderizar sempre que `item.alertas` ou `resultado.alertas` nao estiver vazio.

Template:

```text
Atencoes tecnicas:
- {alerta_1}
- {alerta_2}
```

Regra: alertas nao devem ir apenas no rodape; devem aparecer tambem no corpo da explicacao quando impactam interpretacao.

## 7. Modelo de saida estruturada

O motor deve produzir primeiro uma estrutura, depois renderizar Markdown/HTML/UI.

```typescript
interface ExplicacaoQuedaTensao {
  circuitoId: string;
  titulo: string;
  estado: "OK" | "ACIMA_CIRCUITO" | "ACIMA_TOTAL" | "ACIMA_AMBOS" | "PENDENTE";
  resumoExecutivo: string;
  blocos: ReadonlyArray<BlocoExplicacao>;
  cenarios: ReadonlyArray<ExplicacaoCenario>;
  alertas: ReadonlyArray<string>;
  rastreabilidade: ReadonlyArray<ItemRastreabilidade>;
}

interface BlocoExplicacao {
  id: string;
  titulo: string;
  prioridade: number;
  markdown: string;
}

interface ExplicacaoCenario {
  cenarioId: string;
  classe:
    | "resolve_total"
    | "melhora_mas_nao_resolve"
    | "mantem_ok"
    | "piora"
    | "invalido";
  resumo: string;
  deltaCircuitoPct: number | null;
  deltaTotalPct: number | null;
  reducaoCircuitoPp: number | null;
  reducaoTotalPp: number | null;
  podeAplicar: boolean;
  justificativaNecessaria: boolean;
}
```

## 8. Regras de renderizacao por tipo de circuito

O motor deve adaptar a explicacao ao tipo de circuito, mas sem inventar regra normativa especifica por carga.

### 8.1 Circuito de ar-condicionado

Foco de texto:

1. Carga dedicada.
2. Corrente relevante.
3. Sensibilidade a comprimento e secao.
4. Comparar se o problema e terminal ou acumulado.

Nao afirmar automaticamente que precisa aumentar secao; isso depende do resultado.

### 8.2 Circuito de banheira hidro

Foco de texto:

1. Carga dedicada.
2. Verificar margem total.
3. Se ja estiver `OK`, explicar que cenarios sao margem adicional.

Nao introduzir criterios de DR, aterramento ou protecao se esses dados nao vierem do artefato selecionado.

### 8.3 Circuitos de iluminacao, TUG, TUE ou genericos

Foco de texto:

1. Usar `descricao` como rotulo principal.
2. Nao inferir comportamento da carga se nao existir campo especifico.
3. Explicar sempre pelos dados calculados: corrente, secao, comprimento, queda e limites.

Regra geral:

```text
tipo de circuito personaliza vocabulario; resultado tecnico define diagnostico.
```

## 9. Casos especiais que o motor deve cobrir

### 9.1 Sem alimentador

Condicao:

```text
delta_v_alimentador_pct == null
```

Texto:

```text
Nao ha queda de alimentador associada ao resultado. A analise considera apenas o circuito terminal, e a queda total coincide com a queda do circuito.
```

### 9.2 Alimentador domina o problema

Condicao:

```text
delta_v_alimentador_pct != null
e delta_v_alimentador_pct >= limite_total_pct
```

Texto:

```text
O alimentador sozinho ja consome ou excede o limite total. Reduzir a queda do circuito terminal melhora o resultado, mas pode nao ser suficiente para aprovar o conjunto.
```

### 9.3 Cenario melhora mas nao aprova

Condicao:

```text
base.status == "ACIMA"
e cenario.delta_v_total_pct < base.delta_v_total_pct
e cenario ainda nao atende total ou circuito
```

Texto:

```text
Este cenario reduz a queda, mas ainda nao atinge conformidade. Ele e uma melhoria parcial, nao uma solucao completa.
```

### 9.4 Cenario piora

Condicao:

```text
cenario.delta_v_total_pct > base.delta_v_total_pct
```

Texto:

```text
Este cenario aumenta a queda total em relacao ao estado atual e nao deve ser interpretado como melhoria de queda de tensao.
```

### 9.5 Resultado com alerta

Condicao:

```text
alertas.length > 0
```

Texto:

```text
O resultado foi calculado, mas contem alertas que afetam a leitura tecnica. Leia as atencoes antes de aplicar qualquer cenario.
```

### 9.6 Cenario sem resultado

Condicao:

```text
simulacao rejeitada por dados insuficientes ou perfil nao resolvido
```

Texto:

```text
O cenario nao produziu resultado tecnico. O sistema nao deve comparar ou recomendar uma alternativa sem perfil e dados suficientes.
```

## 10. Ordem final de apresentacao ao usuario

Para qualquer circuito selecionado, renderizar nesta ordem:

1. Resumo executivo em uma frase.
2. Dados do circuito.
3. Resultado atual.
4. Comparacao com limites.
5. Diagnostico da causa.
6. Cenarios simulados.
7. Decisao de aplicacao e auditoria.
8. Formula usada.
9. Rastreabilidade tecnica.
10. Alertas e pendencias.

Essa ordem privilegia compreensao operacional antes de detalhe matematico.

## 11. Exemplo de resumo executivo por estado

| Estado | Resumo |
|---|---|
| `OK` | Este circuito atende a queda de tensao: circuito terminal e acumulado total estao dentro dos limites. |
| `ACIMA_CIRCUITO` | Este circuito nao atende porque a queda do trecho terminal excede o limite do circuito. |
| `ACIMA_TOTAL` | Este circuito nao atende no acumulado: o terminal esta aceitavel, mas alimentador + circuito excedem o limite total. |
| `ACIMA_AMBOS` | Este circuito nao atende nem no trecho terminal nem no acumulado total. |
| `PENDENTE` | Este circuito ainda nao possui dados suficientes para uma explicacao tecnica conclusiva. |

## 12. Criterios de qualidade da explicacao

A explicacao gerada deve cumprir estes criterios:

1. Nunca apresentar resultado tecnico quando `resultado == null`.
2. Nunca ocultar alerta do motor.
3. Nunca dizer que um cenario "resolve" se `atende_circuito` ou `atende_total` for falso.
4. Nunca recomendar aplicacao automatica; aplicar e decisao do projetista.
5. Sempre diferenciar percentual de ponto percentual.
6. Sempre mostrar o calculo acumulado quando houver alimentador.
7. Sempre explicar se a nao conformidade vem do circuito, do total ou dos dois.
8. Sempre preservar rastreabilidade: metodo, R, X, L, V, perfil e fonte quando disponiveis.
9. Sempre sinalizar arredondamento quando o texto conferir soma exibida.
10. Sempre manter o texto derivado dos dados calculados, nao do tipo nominal da carga.

## 13. Pseudocodigo

```text
gerarExplicacao(item, simulacoes):
  se item.resultado ausente:
    return explicacaoPendente(item)

  r = item.resultado
  componentes = extrairComponentes(r)
  estado = classificarEstado(r)
  causa = classificarCausaDominante(r)
  cenarios = simulacoes.map(classificarCenario(base=r))

  blocos = []
  blocos.add(renderIdentificacao(item))
  blocos.add(renderResultadoAtual(componentes))
  blocos.add(renderComparacaoLimites(r))
  blocos.add(renderDiagnostico(estado, causa))

  se cenarios existem:
    blocos.add(renderCenarios(cenarios))
    blocos.add(renderAplicacao(cenarios, estado))

  blocos.add(renderFormula(r.metodo_calculo, r.rastreio))
  blocos.add(renderRastreabilidade(r.rastreio))

  se item.alertas ou r.alertas:
    blocos.add(renderAlertas(item.alertas + r.alertas))

  return {
    circuitoId: item.circuito_id,
    titulo: "Explicacao de queda de tensao - " + item.descricao,
    estado,
    resumoExecutivo: resumoPorEstado(estado, causa),
    blocos,
    cenarios,
    alertas,
    rastreabilidade
  }
```

## 14. Resultado esperado

Com essa sistematica, qualquer circuito selecionado pode receber uma explicacao consistente, mesmo que:

1. Esteja aprovado.
2. Esteja reprovado apenas pelo circuito.
3. Esteja reprovado apenas pelo acumulado.
4. Esteja reprovado por ambos.
5. Esteja pendente por falta de dados.
6. Tenha cenarios que resolvem.
7. Tenha cenarios que melhoram mas nao resolvem.
8. Tenha cenarios apenas de margem.

O motor de renderizacao passa a ser deterministico: os mesmos dados geram a mesma explicacao, e cada frase importante tem origem rastreavel em um campo do resultado do MOD-QT.
