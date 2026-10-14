# Plano T2 — Ausência de Motor como Tipo

**Sistema:** SIE — Sistema de Instalações Elétricas
**Trilha:** 2 de 3 (independente das trilhas T1 e T3)
**Esforço:** baixo
**Bloqueio:** nenhum — verificação de segurança já concluída

---

## Contexto mínimo

O SIE calcula projetos elétricos prediais de baixa tensão, com rastreabilidade normativa por valor. O dimensionamento de condutores (MOD-DC) consolida seis critérios, C1 a C6, alguns calculados internamente e outros delegados a módulos downstream:

| Critério | Origem | Estado |
|---|---|---|
| C1 capacidade de corrente | interno | implementado |
| C2 sobrecarga | interno | implementado |
| C3 curto-circuito | **MOD-CC** | 🔴 mock |
| C4 seccionamento automático | **MOD-SEC** | 🔴 mock |
| C5 queda de tensão | MOD-QT | motor real |
| C6 seção mínima | interno | implementado |

Os três módulos downstream foram desenhados com a mesma arquitetura — contrato tipado, endpoint, timeout de 5 s, degradação graciosa, persistência em `dependencia_retornos_downstream`. O MOD-QT seguiu até o motor real. MOD-CC e MOD-SEC pararam no mock.

Vale a invariante do produto: **nenhum valor normativo é inventado**. Sem fonte, marca-se pendência e ela propaga até a UI.

---

## O problema

### Os mocks decidem por limiar arbitrário

`src/routes/api/v1/modulos.mod-cc.validar.ts`:

```typescript
/**
 * MOCK inicial: retorna resultado fixo baseado em parâmetros.
 * TODO: Substituir por chamada HTTP real ao serviço MOD-CC quando disponível.
 */
async function validarModCCMock(params: RequestModCC): Promise<Record<string, unknown>> {
  await new Promise((resolve) => setTimeout(resolve, 50));
  const aprovado = params.icc_presumida_a < 5000;       // ← limiar fixo
  return { ..., aprovado, fonte: "MOD-CC v1.0" };
}
```

O critério real da NBR 5410 para C3 é a solicitação térmica **I²t ≤ k²S²**, que depende da seção do condutor e do fator k do material. O mock recebe `integral_joule_dispositivo` e `tempo_atuacao_s` e **não os usa na decisão**.

`src/routes/api/v1/modulos.mod-sec.validar.ts`:

```typescript
async function validarModSECMock(params: RequestModSEC): Promise<Record<string, unknown>> {
  const aprovado = params.tempo_atuacao_s <= 0.4;       // ← limite único
  ...
}
```

A Tabela 25 da NBR 5410 traz tempos distintos por U0 e por esquema de aterramento. O mock aplica 0,4 s universalmente.

*Correção a um relato anterior:* o **handler** do MOD-SEC usa corretamente o `esquema_aterramento` — desvia TT para `NAO-APLICAVEL` sem chamar o módulo. Quem ignora o esquema é o mock, nos demais casos.

### O agravante: o veredito do mock sai carimbado como confirmado

Em `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts`:

```typescript
function resolverC3Curto(retorno, secaoFase): ResolucaoCriterioDownstream {
  if (retorno == null) {
    return { status: "PENDENTE", pendencia: "AGUARDANDO-CC", secao_mm2: null, rastreio: null };
  }
  return {
    status: retorno.aprovado ? "APROVADO" : "REPROVADO",
    pendencia: null,
    secao_mm2: retorno.aprovado ? secaoFase : null,
    rastreio: {
      fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "30" },
      valor: retorno.icc_presumida_a,
      status_verificacao: "CONFIRMADO",          // ← literal, incondicional
    },
  };
}
```

`resolverC4Seccionamento` tem a mesma forma, com `tabela: "5.1.2.2.4"`.

Ou seja: `Icc < 5000` não seria apenas exibido como aprovado — seria **carimbado como confirmado contra a ABNT NBR 5410:2004, tabela 30**, indistinguível de um resultado real no envelope de rastreabilidade.

Não é aprovação silenciosa. É aprovação silenciosa com selo de auditoria.

---

## O que já foi verificado — a mudança é segura

A fachada de produção `src/lib/api-client.ts` e os hooks `src/hooks/queries.ts` **não contêm** nenhuma menção a `MOD-CC`, `MOD-SEC`, `mod-cc`, `mod-sec`, `retorno_cc` ou `retorno_seccionamento`. A produção roda em build SPA estático, sem as 39 rotas HTTP.

Consequência prática: hoje, em produção, `retorno_cc` é sempre `null`, C3 fica `PENDENTE` com `AGUARDANDO-CC`, C4 fica `PENDENTE` com `AGUARDANDO-SECCIONAMENTO` (exceto TT, `NAO-APLICAVEL`), e `StatusDimensionamento` não atinge `VERIFICADO-COMPLETO` em TN/IT.

**O comportamento honesto já é o comportamento de produção. T2 não muda o que o usuário vê — torna o comportamento honesto o único possível.** Isso reduz o risco da mudança a praticamente zero.

---

## O padrão já existe no código

Não é preciso introduzir conceito novo. `src/api/schemas/otimizar-condutor.schema.ts` já tem uma resposta de forma diferente para o caso sem veredito:

```typescript
export const NaoAplicavelMODSECSchema = z.object({
  status: z.literal("NAO-APLICAVEL"),
  esquema_aterramento: z.literal("TT"),
  motivo: z.string(),
});
```

T2 generaliza esse precedente: em vez de uma forma alternativa apenas para TT, um conjunto fechado de formas onde `aprovado` só existe quando há motor.

---

## Passos

### Passo 1 — Schema Zod da ausência

`src/api/schemas/otimizar-condutor.schema.ts`:

```typescript
export const SemMotorSchema = z.object({
  status: z.literal("SEM-MOTOR"),
  modulo: z.enum(["MOD-CC", "MOD-SEC"]),
  motivo: z.string().min(1),
});

export const RespostaMODCCSchema = z.union([RetornoMODCCSchema, SemMotorSchema]);
export const RespostaMODSECSchema = z.union([
  RetornoMODSECSchema,
  NaoAplicavelMODSECSchema,
  SemMotorSchema,
]);
```

`RetornoMODCCSchema` e `RetornoMODSECSchema` permanecem intactos — são a forma do veredito real, que o motor produzirá.

### Passo 2 — Contrato de domínio como união discriminada

`src/domain/dimensionamento-condutores/contratos.ts`:

```typescript
export interface VeredictoMODCC {
  readonly tipo: "VEREDICTO";
  readonly icc_presumida_a: number;
  readonly tempo_atuacao_s: number;
  readonly integral_joule_dispositivo: number;
  readonly aprovado: boolean;
  readonly fonte: string;
}

export interface SemMotor {
  readonly tipo: "SEM-MOTOR";
  readonly modulo: "MOD-CC" | "MOD-SEC";
  readonly motivo: string;
}

export type RetornoMODCC = VeredictoMODCC | SemMotor;
```

Análogo para `RetornoMODSEC`, incluindo a variante `NAO-APLICAVEL` já existente.

**O ponto central:** não existe `aprovado` fora de `VEREDICTO`. Um mock não consegue produzir aprovação sem construir um `VEREDICTO`, e fazer isso é uma decisão visível no diff, não um esquecimento.

### Passo 3 — Os mocks passam a declarar ausência

Nos dois handlers, substituir o corpo do mock:

```typescript
async function validarModCCMock(): Promise<Record<string, unknown>> {
  return {
    status: "SEM-MOTOR",
    modulo: "MOD-CC",
    motivo: "Motor de curto-circuito não implementado — C3 permanece pendente.",
  };
}
```

Somem: o `setTimeout(50)`, o limiar de 5000 A, o limite de 0,4 s e a string `fonte: "MOD-CC v1.0"`, que hoje mimetiza uma fonte real.

Preservar `_setClienteModCCParaTeste` e `_resetClienteModCCParaTeste` — são o ponto de injeção pelo qual o motor real entrará depois, sem tocar no handler.

### Passo 4 — Resolvedores tratam a variante

Em `servico-dimensionamento-condutores.ts`:

```typescript
function resolverC3Curto(
  retorno: CircuitoParaDimensionamento["retorno_cc"],
  secaoFase: number,
): ResolucaoCriterioDownstream {
  if (retorno == null || retorno.tipo === "SEM-MOTOR") {
    return { status: "PENDENTE", pendencia: "AGUARDANDO-CC", secao_mm2: null, rastreio: null };
  }
  return {
    status: retorno.aprovado ? "APROVADO" : "REPROVADO",
    pendencia: null,
    secao_mm2: retorno.aprovado ? secaoFase : null,
    rastreio: {
      fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "30" },
      valor: retorno.icc_presumida_a,
      status_verificacao: statusVerificacaoDe(retorno),   // ver Passo 5
    },
  };
}
```

`StatusCriterio` já tem `"PENDENTE"` e `"SEM-DADOS"` no vocabulário — nenhum tipo novo entra aqui.

### Passo 5 — O selo deixa de ser literal

Mesmo com motor real, `status_verificacao: "CONFIRMADO"` fixo está errado: o selo deve refletir o que o módulo downstream informou, não uma constante.

```typescript
function statusVerificacaoDe(retorno: VeredictoMODCC | VeredictoMODSEC): StatusVerificacaoRastreio {
  return retorno.fonte && retorno.fonte.trim().length > 0 ? "CONFIRMADO" : "[VERIFICAR]";
}
```

Se o contrato downstream ganhar um campo próprio de status no futuro, este é o ponto único a ajustar.

### Passo 6 — Testes

Vitest, sem mocks de infraestrutura (o projeto usa `InMemoryRepository`):

- **Contrato:** `validarModCCMock` não produz `tipo: "VEREDICTO"` sob nenhuma entrada — o teste que impede a regressão
- **Contrato:** o mesmo para `validarModSECMock`
- **Integração:** `SEM-MOTOR` em C3 mantém `status: "PENDENTE"` e pendência `AGUARDANDO-CC`
- **Integração:** `SEM-MOTOR` em C4 mantém `AGUARDANDO-SECCIONAMENTO`; TT continua `NAO-APLICAVEL`
- **Integração:** com C3 ou C4 pendente, `StatusDimensionamento` não atinge `VERIFICADO-COMPLETO` em TN/IT
- **Rastreio:** nenhum `status_verificacao: "CONFIRMADO"` é emitido para retorno sem `fonte`
- **Regressão:** o resultado do caminho SPA permanece idêntico ao anterior

---

## O que T2 não faz

Não implementa `src/domain/curto-circuito/` nem `src/domain/seccionamento/`. Os motores reais permanecem trabalho separado, de esforço alto.

O que T2 garante é que, até lá, a ausência seja **declarada** em vez de **simulada** — e deixa o encaixe pronto: quando o motor vier, ele passa a ser o único produtor de `VEREDICTO`, entrando pelo ponto de injeção já existente.

---

## Riscos

| ID | Risco | Mitigação |
|---|---|---|
| T2-R1 | Consumidor não mapeado dos endpoints | Verificado: `api-client.ts` e `queries.ts` não os mencionam; produção é SPA sem rotas de API |
| T2-R2 | Testes existentes que afirmam `aprovado` vindo do mock | Localizar antes de mudar; são exatamente os testes que codificam o comportamento errado e devem ser reescritos |
| T2-R3 | Persistência em `dependencia_retornos_downstream` com payload de forma nova | Coluna é JSONB; a união serializa sem migration. Confirmar que nenhum leitor assume `aprovado` presente |
| T2-R4 | Testes sem CI não protegem | O repositório tem apenas `docs-tutorial-check.yml`; sem workflow de vitest, a rede de segurança depende de disciplina local |

## Invariantes

| # | Invariante | Situação |
|---|---|---|
| 4 | Contrato público do MOD-QT é inalterável | **Não tocada** — T2 mexe apenas em MOD-CC e MOD-SEC |
| 5 | Direção única de dependência entre MOD-DC e MOD-PROT | Preservada |
| 6 | Nenhum valor normativo inventado | **Reforçada** — é o objetivo da trilha |
| 3 | `domain/` não importa de `infra/`/`api/`/`components/` | Preservada |

---

## Critérios de pronto

- [ ] Nenhum handler de mock consegue retornar `tipo: "VEREDICTO"`
- [ ] Sumiram do código o limiar de 5000 A e o limite fixo de 0,4 s
- [ ] Sumiu a string `fonte: "MOD-CC v1.0"` e equivalente do MOD-SEC
- [ ] `SEM-MOTOR` mapeia para `PENDENTE` em C3 e C4
- [ ] TT continua `NAO-APLICAVEL` em C4
- [ ] `VERIFICADO-COMPLETO` inalcançável em TN/IT sem motor real
- [ ] `status_verificacao` do rastreio deixou de ser literal
- [ ] Comportamento do caminho SPA idêntico ao anterior
- [ ] Ponto de injeção (`_setClienteModCCParaTeste`) preservado
