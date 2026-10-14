# Plano T1 — Eixo Temporal e Roteamento do Catálogo

**Sistema:** SIE — Sistema de Instalações Elétricas
**Trilha:** 1 de 3 (independente das trilhas T2 e T3)
**Esforço:** baixo — horas, não dias
**Janela:** fecha com a publicação da revisão da NBR 5410, prevista para o fim de 2026

---

## Contexto mínimo

O SIE calcula projetos elétricos prediais de baixa tensão. Sua proposta de valor declarada não é calcular, é **calcular com rastreabilidade auditável**: todo valor numérico carrega a referência normativa que o originou, o status de verificação daquele dado e a fórmula que o gerou.

Esse envelope é o tipo `ItemRastreado<T>` em `src/domain/nbr/types.ts`:

```typescript
export interface ItemRastreado<T> {
  readonly valor: T;
  readonly referencia: ReferenciaNBR;   // { norma, item }
  readonly status: StatusVerificacao;   // "verificado" | "VERIFICAR"
  readonly formula: FormulaId;          // "F-01".."F-09"
}
```

O catálogo `src/domain/nbr/catalog.data.json` é a fonte única declarada. Vale a invariante: **nenhum valor normativo é inventado** — sem fonte, marca-se `VERIFICAR` e a marca propaga até a UI.

---

## O problema

### Parte 1 — O motor não lê o catálogo; ele inventa

Em `src/domain/calculo/motor.ts`, `calcularDependencia()`:

```typescript
const ref = { norma: "NBR 5410:2004", item: "9.5.2" } as const;
...
area:       { valor: A, referencia: ref, status: "verificado", formula: "F-01" },
perimetro:  { valor: P, referencia: ref, status: "verificado", formula: "F-02" },
iluminacao: { valor: {...}, referencia: ref, status: "VERIFICAR", formula: "F-08" },
tomadas:    { valor: {...}, referencia: ref, status: "VERIFICAR", formula: tom.regras[0] ?? "F-03" },
```

Enquanto isso, o catálogo tem as referências corretas, uma por regra:

| Regra | Item no catálogo | Status no catálogo |
|---|---|---|
| F-01 | `9.5.2.1.1` | verificado |
| F-02 | `9.5.2.1.1` | verificado |
| F-03 | `9.5.2.2.1.c` | VERIFICAR |
| F-04 | `9.5.2.2.1.a` | VERIFICAR |
| F-05 | `9.5.2.2.1.b` | VERIFICAR |
| F-06 | `9.5.2.2.1.d` | VERIFICAR |
| F-07 | `9.5.2.1.2` | VERIFICAR |
| F-08 | `9.5.2.1.2` | VERIFICAR |
| F-09 | `9.5.2.2.1 (nota)` | VERIFICAR |

O motor entrega `9.5.2` para todas — um item mais genérico que o disponível. E `catalog.ts` já exporta `regra(id: FormulaId): RegraNBR`, que devolve a referência certa.

Há ainda uma chamada morta:

```typescript
// status_verificacao das tabelas é consultado (efeito colateral nulo, garante invariante)
statusDeTabela(cat);
```

O retorno é descartado.

### Parte 2 — Os valores coincidem hoje, e vão divergir

Os status hardcoded batem com o catálogo neste momento. O defeito é **latente, não ativo** — nada está errado na tela hoje.

Mas o SIE tem `pendenciasCatalogo()`, um tracker que lista toda regra ou tabela `VERIFICAR` com a fonte a consultar e o validador responsável (`"Eng. Eletricista responsável técnico (ART)"`). Ele existe para dirigir o trabalho de validação normativa.

Quando alguém executar esse trabalho e marcar F-08 como `verificado` no catálogo:

- `pendencias` para de listar F-08 — correto, via `regrasPendentes()`
- `iluminacao.status` continua `"VERIFICAR"` — hardcoded

Os dois canais passam a discordar dentro do mesmo objeto, e o trabalho de validação fica invisível exatamente onde o usuário olha. **O mecanismo desenhado para ser resolvido não consegue registrar a própria resolução.**

### Parte 3 — Não há eixo temporal

O SIE tem um eixo de verificação (*este valor foi conferido?*) e não tem um eixo temporal (*conferido contra qual edição?*).

A edição existe hoje apenas embutida em strings: `norma: "NBR 5410:2004"` no catálogo, e `const ref` no motor.

**Por que tem prazo.** Enquanto existe uma única edição, carimbar projetos históricos é trivialmente correto — tudo foi calculado sob a de 2004. Depois da revisão, essa certeza acaba: a data de cálculo não determina a edição aplicável, porque um projeto recalculado em 2027 pode legitimamente seguir a de 2004 se o protocolo foi anterior. **A janela de carimbo barato fecha sozinha.**

### O padrão já existe no próprio código

Não é preciso inventar formato. Em `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts`:

```typescript
rastreio: {
  fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "30" },
  ...
}
```

O `RastreioValor` do MOD-DC já tem campo `edicao`. T1 estende ao domínio NBR clássico um padrão que os módulos novos já adotam.

---

## O que já foi verificado

| Verificação | Resultado | Consequência |
|---|---|---|
| Persistência de `ResultadoCalculo` | Coluna `resultado jsonb` em `dependencias` | **Sem migration** |
| Vazamento para `UnifilarGraph` | `indexarOrigensPorCircuito` e `pendenciasDoCircuito` leem só campos nomeados — sem spread, sem serialização | **Sem risco de quebrar determinismo de snapshot** |
| Cobertura de `regrasPendentes()` | Filtra apenas `CATALOG.regras`; `pendenciasCatalogo()` cobre regras e tabelas | Assimetria estrutural — tratada no Passo 4 |
| `validarCatalogo()` | Exige `referencia.item` e `fonte`; não valida edição | Estender no Passo 5 |

---

## Passos

### Passo 1 — Declarar a edição no catálogo

`src/domain/nbr/catalog.data.json`, novo bloco de primeiro nível:

```jsonc
{
  "edicao": {
    "norma": "ABNT NBR 5410",
    "edicao": "2004",
    "emenda": "versão corrigida 2008",
    "vigencia_inicio": "2005-03-31"
  },
  "fonte_padrao": "...",
  "dependencia_categoria": { ... },
  "regras": [ ... ],
  "tabelas": { ... }
}
```

**Regra a fixar desde já:** edição prevista mas não publicada **não entra no catálogo**. Só publicação entra. Sem isso, previsão vira fato por descuido.

### Passo 2 — Tipar

`src/domain/nbr/types.ts`. Campo opcional, aditivo — nenhum consumidor existente quebra:

```typescript
export interface ReferenciaNBR {
  readonly norma: string;
  readonly item: string;
  readonly edicao?: string;
}

export interface EdicaoCatalogo {
  readonly norma: string;
  readonly edicao: string;
  readonly emenda?: string;
  readonly vigencia_inicio?: string;
}
```

### Passo 3 — Expor no catálogo

`src/domain/nbr/catalog.ts`, ao lado de `regrasPendentes()`. Atualizar também a interface `RawCatalog` com o campo `edicao`.

```typescript
export function edicaoCatalogo(): EdicaoCatalogo {
  const e = CATALOG.edicao;
  if (!e) throw new Error("Catálogo sem bloco `edicao` — ver validarCatalogo()");
  return e;
}
```

### Passo 4 — O motor passa a ler o catálogo

`src/domain/calculo/motor.ts`. Substitui a constante `ref` e os status literais por um helper.

```typescript
import { edicaoCatalogo, regra, regrasPendentes, tabelaIluminacao,
         tugQtdPara, tugCargaPara } from "../nbr/catalog";
import type { ItemRastreado, StatusVerificacao } from "../nbr/types";

/** VERIFICAR em qualquer fonte contamina o item — regra conservadora. */
function piorStatus(...valores: ReadonlyArray<StatusVerificacao | undefined>): StatusVerificacao {
  return valores.includes("VERIFICAR") ? "VERIFICAR" : "verificado";
}

function rastrear<T>(
  valor: T,
  formula: FormulaId,
  statusTabela?: StatusVerificacao,
): ItemRastreado<T> {
  const r = regra(formula);
  return {
    valor,
    referencia: { ...r.referencia, edicao: edicaoCatalogo().edicao },
    status: piorStatus(r.status_verificacao, statusTabela),
    formula,
  };
}
```

E no corpo de `calcularDependencia()` — note que `statusDeTabela(cat)` deixa de ser chamada morta:

```typescript
const st = statusDeTabela(cat);   // retorno agora é usado

return {
  dependencia: d.tipo,
  categoria: cat,
  // ...
  area:       rastrear(A, "F-01"),
  perimetro:  rastrear(P, "F-02"),
  iluminacao: rastrear(
    { quantidade: ilum.quantidade, pontosMin: ilum.pontosMin, vaTotal: ilum.vaTotal },
    "F-08",
    st.ilum,
  ),
  tomadas: rastrear(
    { quantidade: tom.quantidade, vaTotal: tom.vaTotal },
    tom.regras[0] ?? "F-03",
    piorStatus(st.qtd, st.carga),
  ),
  // cargasAdicionais — ver Decisão D-1 abaixo
  pendencias: unique,
  diagnosticos,
};
```

Isso resolve, de uma vez: referência correta por item, status sincronizado com o catálogo, edição carimbada, chamada morta reaproveitada e pendências de tabela passando a contaminar o status do item.

### Passo 5 — Validação do catálogo

`validarCatalogo()` em `catalog.ts` passa a falhar se o bloco `edicao` estiver ausente ou incompleto:

```typescript
if (!CATALOG.edicao?.edicao) {
  erros.push({ id: "CATALOGO", mensagem: "bloco `edicao` ausente ou sem campo `edicao`" });
}
if (!CATALOG.edicao?.norma) {
  erros.push({ id: "CATALOGO", mensagem: "bloco `edicao` sem campo `norma`" });
}
```

O script `scripts/validar-catalogo.ts` já chama essa função e sai com código 1 em caso de erro — nada a mudar lá.

### Passo 6 — Registros históricos

Sem migration. `src/infra/supabase/mapeadores.ts` já tem o padrão de **fallback de reidratação**, com dois exemplos comentados no código para campos que não existiam antes. Usar o mesmo padrão em `linhasParaDependencia`:

```typescript
// Fallback de reidratação: resultados gravados antes de `referencia.edicao` existir
// foram todos calculados sob a NBR 5410:2004 — única edição catalogada até aqui.
// O carimbo retroativo é não-ambíguo ENQUANTO isso for verdade. Depois da revisão
// deixa de ser: manter este fallback congelado em "2004" e nunca generalizá-lo
// para "a edição corrente".
```

Preferir isso a `UPDATE`: reversível, sem downtime, coerente com a convenção da casa.

### Passo 7 — Testes

Em `src/domain/calculo/` (Vitest, sem mocks — o projeto usa `InMemoryRepository`):

- `calcularDependencia` devolve `area.referencia.item === "9.5.2.1.1"` — trava a correção da referência genérica
- `iluminacao.referencia.item === "9.5.2.1.2"`
- Toda `ItemRastreado` de origem normativa traz `referencia.edicao === "2004"`
- Alterar `status_verificacao` de uma regra no catálogo altera o status no resultado — prova que não está hardcoded
- Marcar uma tabela como `VERIFICAR` com a regra `verificado` produz item `VERIFICAR` — prova o `piorStatus`
- `validarCatalogo()` retorna erro quando o bloco `edicao` é removido
- Regressão: `npx vitest run` sem snapshot quebrado

---

## Decisão pendente

### D-1 — `cargasAdicionais`

Hoje o motor entrega:

```typescript
cargasAdicionais: {
  valor: {...},
  referencia: { norma: "Entrada do usuário", item: "previsão adicional" },
  status: "verificado",
  formula: "F-09",
}
```

O catálogo declara F-09 no item `9.5.2.2.1 (nota)` com status `VERIFICAR`.

São afirmações incompatíveis: o motor diz que a origem é o usuário e o dado está verificado; o catálogo diz que é regra normativa pendente de conferência.

Rotear do catálogo mudaria esse item de `verificado` para `VERIFICAR` — **a única mudança visível de todo o T1**. Antes de aplicar, decidir qual das duas afirmações é a correta. Se a origem é mesmo entrada do usuário, F-09 não deveria estar no catálogo como regra normativa.

Sugestão: manter `cargasAdicionais` fora do `rastrear()` nesta trilha e tratar D-1 separadamente, para que T1 não carregue mudança de comportamento.

---

## Riscos

| ID | Risco | Mitigação |
|---|---|---|
| T1-R1 | Snapshots quebrarem com o campo novo | Rodar `npx vitest run` antes e depois; revisar cada diff conscientemente |
| T1-R2 | Mudança de status visível ao usuário | Só ocorre em D-1. Fora dela, os valores roteados coincidem com os hardcoded hoje |
| T1-R3 | Fallback de reidratação virar regra geral | Comentário explícito no código congelando em "2004"; nunca ler `edicaoCatalogo()` no fallback |
| T1-R4 | Testes sem CI não protegem | O repositório tem apenas `docs-tutorial-check.yml`. Um workflow de lint/typecheck/vitest ativa 85 arquivos de teste já escritos |

## Invariantes

| # | Invariante | Situação |
|---|---|---|
| 3 | `domain/` não importa de `infra/`/`api/`/`components/` | Preservada — tudo em `domain/` |
| 6 | Nenhum valor normativo inventado | **Reforçada** — é o objetivo da trilha |
| 7 | `ItemRastreado<T>` por valor calculado | Preservada — campo aditivo |
| 17 | `meta.calculadoEm` pode ser `null` de propósito | Sem risco: o unifilar lê só campos nomeados, e nenhum timestamp é adicionado |

---

## Critérios de pronto

- [ ] Nenhuma referência normativa hardcoded em `motor.ts`
- [ ] `statusDeTabela()` deixou de ser chamada com retorno descartado
- [ ] `area.referencia.item` é `9.5.2.1.1`, não `9.5.2`
- [ ] Toda referência normativa carrega `edicao`
- [ ] Teste que prova que alterar o catálogo altera o resultado
- [ ] `validarCatalogo()` falha sem bloco `edicao`
- [ ] Fallback de reidratação congelado em "2004", com comentário
- [ ] Nenhum snapshot quebrado sem revisão
- [ ] D-1 decidida e registrada

---

## O que esta trilha deixa pronto para depois

Quando a revisão da NBR 5410 for publicada, a etapa seguinte (resolução por data de referência) encontra o terreno preparado: catálogo com bloco de edição, referências roteadas da fonte e todo resultado histórico carimbado. Sem T1, essa etapa começa com uma base de projetos que não sabe sob qual edição foi calculada — e essa informação não é recuperável.
