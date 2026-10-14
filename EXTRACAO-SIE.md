# EXTRACAO-SIE

## 1. Catalogo NBR

Caminho: `src/domain/nbr/catalog.data.json` ? total de linhas: 192

```json
{
  "chavesPrimeiroNivel": [
    "fonte_padrao",
    "dependencia_categoria",
    "regras",
    "tabelas"
  ],
  "campos": []
}
```

## 2. Tipos centrais do dominio NBR

Caminho: `src/domain/nbr/types.ts` ? total de linhas: 173

```ts
/**
 * Tipos centrais do domínio NBR 5410:2004 — módulo de tomadas e iluminação.
 *
 * Fonte da verdade: Especificação Técnica Orientadora — Sistema Construtor
 * de Projetos Elétricos (Bloco 1, v13). Nenhuma regra ou valor normativo
 * deve ser inventado fora do catálogo (`catalog.data.json`).
 */
import type { ConformidadeNBR5410 } from "../modelo/conformidade-nbr5410";
import type { OrigemTUG } from "../modelo/dependencia";

/** Categorias de dependência segundo a Especificação (Etapa 6). */
export type Categoria = "CAT-A" | "CAT-B" | "CAT-C";

/**
 * Dependências suportadas no módulo inicial. Mapeadas para uma categoria
 * no catálogo. Manter este union exaustivo — adicionar novas dependências
 * exige atualizar `DEPENDENCIA_CATEGORIA` no catálogo.
 */

export type Dependencia =
  | "dormitorio"
  | "sala"
  | "cozinha"
  | "area-servico"
  | "banheiro"
  | "hall-corredor"
  | "varanda"
  | "area-externa";

/** Estado de verificação normativa de uma regra. */
export type StatusVerificacao = "verificado" | "VERIFICAR";

/** Referência rastreável a um item da norma. */
export interface ReferenciaNBR {
  readonly norma: string;
  readonly item: string;
}

/** Identificadores estáveis das fórmulas extraídas (F-01..F-09). */
export type FormulaId =
  | "F-01"
  | "F-02"
  | "F-03"
  | "F-04"
  | "F-05"
  | "F-06"
  | "F-07"
  | "F-08"
  | "F-09";

/**
 * Regra normativa do catálogo. `parametros` é deliberadamente um mapa
 * aberto para acomodar diferentes fórmulas; cada consumidor faz a leitura
 * tipada que precisa (ver `catalog.ts`).
 */
export interface RegraNBR {
  readonly id: FormulaId;
  readonly categoria: Categoria | "GERAL";
  readonly descricao: string;
  readonly parametros: Readonly<Record<string, number | string | boolean>>;
  readonly referencia: ReferenciaNBR;
  readonly status_verificacao: StatusVerificacao;
  readonly fonte: string;
}

/** Entrada-base comum às tabelas normativas (T-*). */
export interface EntradaTabela {
  readonly id: string;
  readonly referencia: ReferenciaNBR;
  readonly status_verificacao: StatusVerificacao;
  readonly fonte: string;
  readonly fonte_requerida?: string;
  readonly validador_responsavel?: string;
}

/** T-ILUM — carga mínima de iluminação. */
export interface TabelaIluminacao extends EntradaTabela {
  readonly descricao: string;
  readonly vaBase: number;
  readonly areaLimiteM2: number;
  readonly vaAdicional: number;
  readonly passoAreaM2: number;
  readonly pontosMin: number;
}

/** T-TUG-QTD — quantidade mínima de tomadas por categoria. */
export interface TabelaTugQtd extends EntradaTabela {
  readonly categoria: Categoria;
  readonly regra: string;
  readonly espacamentoMaxM?: number;
  readonly areaLimiteM2?: number;
  readonly pontosMinAbaixoLimite?: number;
  readonly pontosMinBanheiro?: number;
}

/** T-TUG-CARGA — VA por ponto por categoria/posição. */
export interface TabelaTugCarga extends EntradaTabela {
  readonly categoria: Categoria;
  readonly vaPorTomada?: number;
  readonly vaPorTomadaPrimeiras?: number;
  readonly qtdPrimeiras?: number;
  readonly vaPorTomadaAdicionais?: number;
  readonly vaPorTomadaBanheiro?: number;
}

/**
 * Envelope de rastreabilidade: cada valor calculado carrega a referência
 * normativa que o originou e seu status de verificação. A UI exibe esses
 * metadados ao lado do número.
 */
export interface ItemRastreado<T> {
  readonly valor: T;
  readonly referencia: ReferenciaNBR;
  readonly status: StatusVerificacao;
  readonly formula: FormulaId;
}

export type SeveridadeDiagnosticoDependencia = "ERRO" | "ATENCAO" | "INFO";

export type CodigoDiagnosticoDependencia =
  | "ERR-NBR5410-ZONA-BANHEIRO-AUSENTE"
  | "ERR-NBR5410-ZONA-PISCINA-AUSENTE"
  | "ERR-NBR5410-DR-AUSENTE"
  | "ERR-NBR5410-IP-AUSENTE"
  | "ATN-NBR5410-BANHEIRO-SEM-TUE-BANHO"
  | "ATN-NBR5410-CARGA-MOTORIZADA-CATEGORIA"
  | "ATN-NBR5410-TUE-EXCLUSIVO-QUANTIDADE"
  | "INF-NBR5410-CONFORMIDADE-DECLARADA";

export interface DiagnosticoDependencia {
  readonly codigo: CodigoDiagnosticoDependencia;
  readonly severidade: SeveridadeDiagnosticoDependencia;
  readonly mensagem: string;
  readonly referencia: ReferenciaNBR;
  readonly detalhes?: Readonly<Record<string, unknown>>;
}

/** Resultado consolidado do cálculo de uma dependência. */
export interface ResultadoCalculo {
  readonly dependencia: Dependencia;
  readonly categoria: Categoria;
  readonly conformidadeNBR5410?: ConformidadeNBR5410;
  readonly perimetroReal_m?: number;
  readonly areaReal_m?: number;
  readonly tugOrigem?: OrigemTUG;
  readonly tugJustificativa?: string;
  readonly area: ItemRastreado<number>;
  readonly perimetro: ItemRastreado<number>;
  readonly tomadas: ItemRastreado<{ quantidade: number; vaTotal: number }>;
  readonly iluminacao: ItemRastreado<{ quantidade: number; pontosMin: number; vaTotal: number }>;
  readonly cargasAdicionais: ItemRastreado<{
    itens: ReadonlyArray<{
      nome: string;
      vaUnitario: number;
      quantidade: number;
      vaTotal: number;
      categoria: "iluminacao" | "tue" | "outra";
      tensaoFixa?: 127 | 220 | 380;
      tipoAparelho?: string;
      trifasica?: boolean;
    }>;
    vaTotal: number;
    vaPorCategoria: {
      iluminacao: number;
      tue: number;
      outra: number;
    };
  }>;
  /** IDs de regras [VERIFICAR] usadas no cálculo. */
  readonly pendencias: ReadonlyArray<FormulaId>;
  /** Diagnósticos complementares de conformidade NBR 5410 desta dependência. */
  readonly diagnosticos: ReadonlyArray<DiagnosticoDependencia>;
}
```

## 3. Persistencia do resultado de calculo

### a) ResultadoCalculo

Caminho: `src/domain/nbr/types.ts` ? total de linhas: 173

```ts
export interface ResultadoCalculo {
  readonly dependencia: Dependencia;
  readonly categoria: Categoria;
  readonly conformidadeNBR5410?: ConformidadeNBR5410;
  readonly perimetroReal_m?: number;
  readonly areaReal_m?: number;
  readonly tugOrigem?: OrigemTUG;
  readonly tugJustificativa?: string;
  readonly area: ItemRastreado<number>;
  readonly perimetro: ItemRastreado<number>;
  readonly tomadas: ItemRastreado<{ quantidade: number; vaTotal: number }>;
  readonly iluminacao: ItemRastreado<{ quantidade: number; pontosMin: number; vaTotal: number }>;
  readonly cargasAdicionais: ItemRastreado<{
    itens: ReadonlyArray<{
      nome: string;
      vaUnitario: number;
      quantidade: number;
      vaTotal: number;
      categoria: "iluminacao" | "tue" | "outra";
      tensaoFixa?: 127 | 220 | 380;
      tipoAparelho?: string;
      trifasica?: boolean;
    }>;
    vaTotal: number;
    vaPorCategoria: {
      iluminacao: number;
      tue: number;
      outra: number;
    };
  }>;
  /** IDs de regras [VERIFICAR] usadas no cálculo. */
  readonly pendencias: ReadonlyArray<FormulaId>;
  /** Diagnósticos complementares de conformidade NBR 5410 desta dependência. */
  readonly diagnosticos: ReadonlyArray<DiagnosticoDependencia>;
}
```

### b) Mapeadores Dependencia/DependenciaAgregado

Caminho: `src/infra/supabase/mapeadores.ts` ? total de linhas: 412

```ts
export function linhasParaDependencia(l: LinhaDependencia): DependenciaAgregado {
  const bancadas: ReadonlyArray<Bancada> = (l.dependencia_bancadas ?? [])
    .slice()
    .sort((a, b) => a.ordem - b.ordem)
    .map((b) => ({
      largura_m: Number(b.largura_m),
      em_cozinha_ou_copa: b.em_cozinha_ou_copa,
    }));

  const cargasPersistidas: ReadonlyArray<CargaAdicional> = (l.dependencia_cargas_adicionais ?? [])
    .slice()
    .sort((a, b) => a.ordem - b.ordem)
    .map((c) => ({
      nome: c.nome,
      vaUnitario: Number(c.va_unitario),
      quantidade: c.quantidade,
      categoria: c.categoria as CategoriaCargaAdicional,
      ...(c.tensao_fixa != null ? { tensaoFixa: c.tensao_fixa as Tensao } : {}),
      ...(c.tipo_aparelho ? { tipoAparelho: c.tipo_aparelho as TipoAparelho } : {}),
      ...(c.trifasica === true ? { trifasica: true } : {}),
      ...(c.unidade_original
        ? { unidadeOriginal: c.unidade_original as UnidadeCargaAdicional }
        : {}),
      ...(c.valor_original != null ? { valorOriginal: Number(c.valor_original) } : {}),
      ...(c.fator_potencia != null ? { fatorPotencia: Number(c.fator_potencia) } : {}),
    }));

  // Fallback de reidratação: dependências salvas antes da coluna `trifasica`
  // existir tiveram o INSERT nas filhas abortado, mas o `resultado` JSONB foi
  // gravado com os itens. Reconstitui o mínimo (nome/va/qtd/categoria) para que
  // a modal Editar não abra vazia. Campos não persistidos no resultado
  // (tipoAparelho, tensaoFixa, trifasica) ficam como default — o usuário
  // reajusta se necessário e o próximo salvar grava completo.
  const itensResultado = l.resultado?.cargasAdicionais?.valor?.itens ?? [];
  const cargasAdicionais: ReadonlyArray<CargaAdicional> =
    cargasPersistidas.length === 0 && itensResultado.length > 0
      ? itensResultado.map((i) => ({
          nome: i.nome,
          vaUnitario: Number(i.vaUnitario),
          quantidade: Number(i.quantidade),
          categoria: i.categoria as CategoriaCargaAdicional,
          ...(i.tensaoFixa !== undefined ? { tensaoFixa: i.tensaoFixa as Tensao } : {}),
          ...(i.tipoAparelho ? { tipoAparelho: i.tipoAparelho as TipoAparelho } : {}),
          ...(i.trifasica === true ? { trifasica: true } : {}),
        }))
      : cargasPersistidas;

  const edicoesManuais: ReadonlyArray<EdicaoManual> = (l.dependencia_edicoes_manuais ?? [])
    .slice()
    .sort((a, b) => a.ordem - b.ordem)
    .map((e) => ({
      campo: e.campo,
      valorAnterior: e.valor_anterior,
      valorNovo: e.valor_novo,
      justificativa: e.justificativa,
      autor: e.autor,
      em: e.em,
    }));

  const v = pickValidacao(l.dependencia_validacao);
  const validacao: ValidacaoTecnica | undefined = v
    ? { responsavelTecnico: v.responsavel_tecnico, em: v.em }
    : undefined;
  const conformidadePersistida =
    pickUltimaConformidadePersistida(l.dependencia_edicoes_manuais ?? []) ??
    (l.resultado?.conformidadeNBR5410 as ConformidadeNBR5410 | undefined);
  const perimetroRealPersistido =
    (l.perimetro_real_m != null && Number(l.perimetro_real_m) > PERIMETRO_REAL_AUSENTE_M
      ? Number(l.perimetro_real_m)
      : undefined) ?? l.resultado?.perimetroReal_m;
  const areaRealPersistida =
    (l.area_real_m != null && Number(l.area_real_m) > AREA_REAL_AUSENTE_M2
      ? Number(l.area_real_m)
      : undefined) ?? l.resultado?.areaReal_m;

  const entradaBase: DependenciaEntrada = {
    id: l.id,
    tipo: l.tipo as Dependencia,
    ...(l.nome_personalizado ? { nomePersonalizado: l.nome_personalizado } : {}),
    dimensoes: {
      largura_m: Number(l.largura_m),
      comprimento_m: Number(l.comprimento_m),
      ...(l.pe_direito_m != null && Number(l.pe_direito_m) > PE_DIREITO_AUSENTE_M
        ? { pe_direito_m: Number(l.pe_direito_m) }
        : {}),
    },
    ...(bancadas.length ? { bancadas } : {}),
    ...(l.perimetro_excluido_m != null &&
    Number(l.perimetro_excluido_m) > PERIMETRO_EXCLUIDO_AUSENTE_M
      ? { perimetroExcluido_m: Number(l.perimetro_excluido_m) }
      : {}),
    ...(perimetroRealPersistido != null
      ? { perimetroReal_m: Number(perimetroRealPersistido) }
      : {}),
    ...(areaRealPersistida != null ? { areaReal_m: Number(areaRealPersistida) } : {}),
    ...(cargasAdicionais.length ? { cargasAdicionais } : {}),
    ...(conformidadePersistida ? { conformidadeNBR5410: conformidadePersistida } : {}),
  };
  const tugAutomatico = quantidadeTUGAutomatica(entradaBase);
  const tugPersistido = l.resultado?.tomadas?.valor?.quantidade;
  const tugOrigemPersistida =
    (l.tug_origem as OrigemTUG | null | undefined) ?? l.resultado?.tugOrigem;
  const tugOrigem =
    tugOrigemPersistida ??
    (tugPersistido !== undefined ? detectarOrigemTUG(tugPersistido, tugAutomatico) : "AUTOMATICA");
  const tugJustificativaPersistida = l.tug_justificativa ?? l.resultado?.tugJustificativa;
  const entrada: DependenciaEntrada = {
    ...entradaBase,
    ...(tugOrigem === "MANUAL" && tugPersistido !== undefined
      ? {
          quantidadeTUGOverride: tugPersistido,
          tugOrigem,
          tugJustificativa: tugJustificativaPersistida ?? undefined,
        }
      : {
          tugOrigem,
          ...(tugJustificativaPersistida ? { tugJustificativa: tugJustificativaPersistida } : {}),
        }),
  };

  // Fallback de reidratação: dependências calculadas antes do campo
  // `iluminacao.valor.quantidade` existir no motor de cálculo tiveram apenas
  // `pontosMin` gravado no `resultado` JSONB. Sem este fallback, a UI exibe
  // "undefined ponto" nos cards em vez do número real de pontos.
  const iluminacaoQuantidadePersistida = l.resultado?.iluminacao?.valor?.quantidade;
  const resultado =
    l.resultado && iluminacaoQuantidadePersistida === undefined
      ? {
          ...l.resultado,
          iluminacao: {
            ...l.resultado.iluminacao,
            valor: {
              ...l.resultado.iluminacao.valor,
              quantidade: quantidadeIluminacaoAutomatica(entradaBase),
            },
          },
        }
      : l.resultado;

  return {
    id: l.id,
    projetoId: l.projeto_id,
    versao: l.versao,
    estado: estadoDependenciaEfetivoPorConformidade({
      estado: l.estado as EstadoDependencia,
      entrada,
      resultadoPresente: l.resultado != null,
    }),
    entrada,
    ...(resultado ? { resultado } : {}),
    edicoesManuais,
    ...(validacao ? { validacao } : {}),
    criadoEm: l.criado_em,
    atualizadoEm: l.atualizado_em,
  };
}

export function dependenciaParaLinhas(d: DependenciaAgregado): DecomposicaoDependencia {
  const dim = d.entrada.dimensoes;
  const entradaBase: DependenciaEntrada = { ...d.entrada };
  const tugAutomatico = quantidadeTUGAutomatica(entradaBase);
  const tugPersistido =
    d.resultado?.tomadas?.valor?.quantidade ??
    (d.entrada.quantidadeTUGOverride !== undefined
      ? d.entrada.quantidadeTUGOverride
      : tugAutomatico);
  const tugOrigem =
    d.entrada.tugOrigem ??
    d.resultado?.tugOrigem ??
    detectarOrigemTUG(
      tugPersistido,
      tugAutomatico,
      d.entrada.quantidadeTUGOverride !== undefined && d.entrada.quantidadeTUGOverride > 0,
    );
  const tugJustificativaPersistida =
    d.entrada.tugJustificativa ?? d.resultado?.tugJustificativa ?? undefined;
  return {
    dep: {
      id: d.id,
      projeto_id: d.projetoId,
      versao: d.versao,
      estado: d.estado,
      tipo: d.entrada.tipo,
      nome_personalizado: d.entrada.nomePersonalizado ?? null,
      largura_m: dim.largura_m,
      comprimento_m: dim.comprimento_m,
      pe_direito_m: dim.pe_direito_m ?? PE_DIREITO_AUSENTE_M,
      perimetro_excluido_m: d.entrada.perimetroExcluido_m ?? PERIMETRO_EXCLUIDO_AUSENTE_M,
      perimetro_real_m: d.entrada.perimetroReal_m ?? PERIMETRO_REAL_AUSENTE_M,
      area_real_m: d.entrada.areaReal_m ?? AREA_REAL_AUSENTE_M2,
      tug_origem: tugOrigem,
      tug_justificativa:
        tugJustificativaPersistida ??
        (tugOrigem === "MANUAL" ? (d.edicoesManuais.at(-1)?.justificativa ?? null) : null),
      resultado: d.resultado ?? null,
      criado_em: d.criadoEm,
      atualizado_em: d.atualizadoEm,
    },
    bancadas: (d.entrada.bancadas ?? []).map((b, i) => ({
      dependencia_id: d.id,
      ordem: i,
      largura_m: b.largura_m,
      em_cozinha_ou_copa: b.em_cozinha_ou_copa,
    })),
    cargas: (d.entrada.cargasAdicionais ?? []).map((c, i) => ({
      dependencia_id: d.id,
      ordem: i,
      nome: c.nome,
      va_unitario: c.vaUnitario,
      quantidade: c.quantidade,
      categoria: c.categoria,
      tensao_fixa: c.tensaoFixa ?? null,
      tipo_aparelho: c.tipoAparelho ?? null,
      trifasica: c.trifasica === true,
      unidade_original: c.unidadeOriginal ?? null,
      valor_original: c.valorOriginal ?? null,
      fator_potencia: c.fatorPotencia ?? null,
    })),
    edicoes: d.edicoesManuais.map((e, i) => ({
      dependencia_id: d.id,
      ordem: i,
      campo: e.campo,
      valor_anterior: e.valorAnterior,
      valor_novo: e.valorNovo,
      justificativa: e.justificativa,
      autor: e.autor,
      em: e.em,
    })),
    validacao: d.validacao
      ? {
          dependencia_id: d.id,
          responsavel_tecnico: d.validacao.responsavelTecnico,
          em: d.validacao.em,
        }
      : undefined,
  };
}
```

### c) Tabela dependencias e ALTERs posteriores

Caminho: `docs/supabase/0001_init.sql` ? total de linhas: 133

```sql
CREATE TABLE IF NOT EXISTS public.dependencias (
  id                       text PRIMARY KEY,
  projeto_id               text NOT NULL REFERENCES public.projetos(id) ON DELETE CASCADE,
  versao                   integer NOT NULL,
  estado                   text NOT NULL,
  tipo                     text NOT NULL,
  largura_m                numeric NOT NULL,
  comprimento_m            numeric NOT NULL,
  pe_direito_m             numeric,
  perimetro_excluido_m     numeric,
  perimetro_real_m         numeric,
  area_real_m              numeric,
  resultado                jsonb,
  criado_em                timestamptz NOT NULL,
  atualizado_em            timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS dependencias_projeto_id_idx
  ON public.dependencias (projeto_id);
GRANT ALL ON public.dependencias TO service_role;
ALTER TABLE public.dependencias ENABLE ROW LEVEL SECURITY;
```

Caminho: `docs/supabase/0003_add_perimetro_real.sql` ? total de linhas: 8

```sql
-- P-PERIM — Adiciona perímetro útil real para cômodos não retangulares (em L, U, T).
-- Quando informado (> 0), substitui o cálculo P = 2(L+C) no dimensionamento de TUG.
-- Run this in the Supabase SQL Editor of your project.

ALTER TABLE public.dependencias
  ADD COLUMN IF NOT EXISTS perimetro_real_m numeric;

NOTIFY pgrst, 'reload schema';

```

Caminho: `docs/supabase/0004_add_area_real.sql` ? total de linhas: 8

```sql
-- P-AREAREAL - Adiciona área útil real para cômodos não retangulares.
-- Quando informada (> 0), substitui A = L*C nos cálculos baseados em área.
-- Run this in the Supabase SQL Editor of your project.

ALTER TABLE public.dependencias
  ADD COLUMN IF NOT EXISTS area_real_m numeric;

NOTIFY pgrst, 'reload schema';

```

Caminho: `docs/supabase/0005_add_tug_origin.sql` ? total de linhas: 13

```sql
-- ============================================================================
-- Adiciona rastreabilidade de origem da TUG nas dependências.
-- ============================================================================

ALTER TABLE public.dependencias
  ADD COLUMN IF NOT EXISTS tug_origem text,
  ADD COLUMN IF NOT EXISTS tug_justificativa text;

COMMENT ON COLUMN public.dependencias.tug_origem IS
  'Origem da quantidade de TUG persistida: AUTOMATICA ou MANUAL.';

COMMENT ON COLUMN public.dependencias.tug_justificativa IS
  'Justificativa opcional quando a quantidade de TUG foi sobrescrita manualmente.';

```

Caminho: `docs/supabase/0006_add_nome_pers…410 tokens truncated…area(d);
  const P = perimetro(d);
  const ilum = cargaIluminacao(d);
  const tom = cargaTUG(d);
  const extras = cargasAdicionais(d);
  const diagnosticos = diagnosticosConformidadeNBR5410(d);

  const ref = { norma: "NBR 5410:2004", item: "9.5.2" } as const;
  const pend = new Set<FormulaId>(regrasPendentes());
  const regrasUsadas: FormulaId[] = ["F-01", "F-02", ...ilum.regras, ...tom.regras];
  const pendencias = regrasUsadas.filter((r) => pend.has(r));
  // dedup
  const unique = Array.from(new Set(pendencias));

  // status_verificacao das tabelas é consultado (efeito colateral nulo, garante invariante)
  statusDeTabela(cat);

  return {
    dependencia: d.tipo,
    categoria: cat,
    conformidadeNBR5410: d.conformidadeNBR5410,
    ...(d.perimetroReal_m !== undefined ? { perimetroReal_m: d.perimetroReal_m } : {}),
    ...(d.areaReal_m !== undefined ? { areaReal_m: d.areaReal_m } : {}),
    area: { valor: A, referencia: ref, status: "verificado", formula: "F-01" },
    perimetro: { valor: P, referencia: ref, status: "verificado", formula: "F-02" },
    iluminacao: {
      valor: { quantidade: ilum.quantidade, pontosMin: ilum.pontosMin, vaTotal: ilum.vaTotal },
      referencia: ref,
      status: "VERIFICAR",
      formula: "F-08",
    },
    tomadas: {
      valor: { quantidade: tom.quantidade, vaTotal: tom.vaTotal },
      referencia: ref,
      status: "VERIFICAR",
      formula: tom.regras[0] ?? "F-03",
    },
    cargasAdicionais: {
      valor: {
        itens: extras.itens,
        vaTotal: extras.vaTotal,
        vaPorCategoria: extras.vaPorCategoria,
      },
      referencia: { norma: "Entrada do usuário", item: "previsão adicional" },
      status: "verificado",
      formula: "F-09",
    },
    pendencias: unique,
    diagnosticos,
  };
}

export interface ResultadoProjeto {
  readonly projeto: { readonly id: string; readonly nome: string };
  readonly dependencias: ReadonlyArray<ResultadoCalculo>;
  readonly totais: {
    readonly iluminacao_va: number;
    readonly tomadas_va: number;
```

## 5. Contratos dos modulos downstream

Caminho: `src/domain/dimensionamento-condutores/contratos.ts` ? total de linhas: 227

```ts
export interface RetornoMODCC {
  readonly icc_presumida_a: number;
  readonly tempo_atuacao_s: number;
  readonly integral_joule_dispositivo: number;
  readonly aprovado: boolean;
  readonly fonte: string;
}

export interface RetornoMODSEC {
  readonly aprovado: boolean;
  readonly tempo_seccionamento_s: number;
  readonly fonte: string;
}

export type StatusCriterio = "APROVADO" | "REPROVADO" | "PENDENTE" | "NAO-APLICAVEL" | "SEM-DADOS";
export type StatusDimensionamento =
  | "DADOS-INCOMPLETOS"
  | "DIMENSIONAMENTO-PARCIAL"
  | "VERIFICADO-COMPLETO"
  | "REPROVADO"
  | "REQUER-ESTUDO-PARALELO";

/**
 * Retorno do MOD-CC (curto-circuito, C3). Contrato de entrada esperado do
 * modulo downstream conforme PRD MOD-DC §12.4 (ABNT NBR 5410 5.3.5 / 6.3.4.3).
 * Enquanto ausente, C3 permanece PENDENTE com pendencia `AGUARDANDO-CC`.
 */
export interface RetornoMODCC {
  readonly icc_presumida_a: number;
  readonly tempo_atuacao_s: number;
  readonly integral_joule_dispositivo: number;
  readonly aprovado: boolean;
  readonly fonte: string;
}

export type StatusDimensionamento =
  | "DADOS-INCOMPLETOS"
  | "DIMENSIONAMENTO-PARCIAL"
  | "VERIFICADO-COMPLETO"
  | "REPROVADO"
  | "REQUER-ESTUDO-PARALELO";

/**
 * Retorno do MOD-CC (curto-circuito, C3). Contrato de entrada esperado do
 * modulo downstream conforme PRD MOD-DC §12.4 (ABNT NBR 5410 5.3.5 / 6.3.4.3).
 * Enquanto ausente, C3 permanece PENDENTE com pendencia `AGUARDANDO-CC`.
 */
export interface RetornoMODCC {
  readonly icc_presumida_a: number;
  readonly tempo_atuacao_s: number;
  readonly integral_joule_dispositivo: number;
  readonly aprovado: boolean;
  readonly fonte: string;
}
```

## 6. Handlers de mock

Caminho: `src/routes/api/v1/modulos.mod-cc.validar.ts` ? total de linhas: 119

```ts
import { createFileRoute } from "@tanstack/react-router";
import { ValidarMODCCSchema, RetornoMODCCSchema } from "@/api/schemas/otimizar-condutor.schema";
import { erro, ok, withZod } from "@/api/http";
import { getServicos } from "@/api/contexto-singleton";

const TIMEOUT_MS = 5000;

/**
 * POST /api/v1/modulos/mod-cc/validar
 *
 * Valida curto-circuito (C3) conforme ABNT NBR 5410 5.3.5.
 * - Request: dependencia_id, icc_presumida_a, tempo_atuacao_s, integral_joule_dispositivo, origem
 * - Response: RetornoMODCC com aprovado boolean + parametros
 * - Timeout: 5 segundos (AC2, AC5) — corrida entre o cliente MOD-CC e o AbortSignal
 * - Persistência: grava o retorno em dependencia_retornos_downstream (AC4)
 * - Error handling: graceful degradation (timeout/erro → PENDENTE, não lança exceção)
 */
export const Route = createFileRoute("/api/v1/modulos/mod-cc/validar")({
  server: {
    handlers: {
      POST: async ({ request }) => {
        const v = await withZod(request, ValidarMODCCSchema);
        if (!v.ok) return v.response;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

        try {
          const retorno = await Promise.race([
            clienteModCC.validar(v.data),
            aguardarAbort(controller.signal),
          ]);

          const validacao = RetornoMODCCSchema.safeParse(retorno);
          if (!validacao.success) {
            return erro("mod_cc_contrato_invalido", "MOD-CC retornou contrato inválido", 422, {
              issues: validacao.error.issues,
            });
          }

          const { retornosDownstream } = getServicos();
          await retornosDownstream.registrar({
            dependenciaId: v.data.dependencia_id,
            modulo: "MOD-CC",
            payload: validacao.data,
            recebidoEm: new Date().toISOString(),
          });

          return ok(validacao.data);
        } catch (e) {
          if (e instanceof Error && e.name === "AbortError") {
            console.warn(`[MOD-CC] Timeout ${TIMEOUT_MS}ms atingido para origem=${v.data.origem}`);
            return erro("mod_cc_timeout", "MOD-CC timeout", 504, {
              status: "PENDENTE",
              origem: v.data.origem,
            });
          }
          const detalhe = e instanceof Error ? e.message : String(e);
          console.error("[MOD-CC] Erro ao validar curto-circuito:", detalhe);
          return erro("mod_cc_erro", "MOD-CC retornou erro", 500, {
            status: "PENDENTE",
            detalhes: detalhe,
          });
        } finally {
          clearTimeout(timeoutId);
        }
      },
    },
  },
});

/** Rejeita quando o AbortSignal dispara, permitindo Promise.race com a chamada downstream. */
function aguardarAbort(signal: AbortSignal): Promise<never> {
  return new Promise((_, reject) => {
    signal.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
  });
}

export interface RequestModCC {
  readonly dependencia_id: string;
  readonly icc_presumida_a: number;
  readonly tempo_atuacao_s: number;
  readonly integral_joule_dispositivo: number;
  readonly origem: string;
}

export interface ClienteModCC {
  validar(params: RequestModCC): Promise<Record<string, unknown>>;
}

/**
 * MOCK inicial: retorna resultado fixo baseado em parâmetros.
 * TODO: Substituir por chamada HTTP real ao serviço MOD-CC quando disponível.
 */
async function validarModCCMock(params: RequestModCC): Promise<Record<string, unknown>> {
  await new Promise((resolve) => setTimeout(resolve, 50));

  const aprovado = params.icc_presumida_a < 5000;

  return {
    icc_presumida_a: params.icc_presumida_a,
    tempo_atuacao_s: params.tempo_atuacao_s,
    integral_joule_dispositivo: params.integral_joule_dispositivo,
    aprovado,
    fonte: "MOD-CC v1.0",
  };
}

let clienteModCC: ClienteModCC = { validar: validarModCCMock };

/** Apenas para testes: substitui o cliente MOD-CC (ex.: simular timeout/erro/hang). */
export function _setClienteModCCParaTeste(cliente: ClienteModCC): void {
  clienteModCC = cliente;
}

/** Apenas para testes: restaura o cliente MOD-CC mock padrão. */
export function _resetClienteModCCParaTeste(): void {
  clienteModCC = { validar: validarModCCMock };
}
```

Caminho: `src/routes/api/v1/modulos.mod-sec.validar.ts` ? total de linhas: 127

```ts
import { createFileRoute } from "@tanstack/react-router";
import { ValidarMODSECSchema, RetornoMODSECSchema } from "@/api/schemas/otimizar-condutor.schema";
import { erro, ok, withZod } from "@/api/http";
import { getServicos } from "@/api/contexto-singleton";

const TIMEOUT_MS = 5000;

/**
 * POST /api/v1/modulos/mod-sec/validar
 *
 * Valida seccionamento automático (C4) conforme ABNT NBR 5410 5.1.2.2.4 (Story MOD-SEC-1).
 * - Request: dependencia_id, esquema_aterramento, tempo_atuacao_s, origem
 * - Regra TT (AC2): MOD-SEC NÃO é chamado; responde NAO-APLICAVEL sem persistir
 * - Response: RetornoMODSEC com aprovado + tempo_seccionamento_s + fonte
 * - Timeout: 5 segundos — corrida entre o cliente MOD-SEC e o AbortSignal
 * - Persistência: grava o retorno em dependencia_retornos_downstream
 * - Error handling: graceful degradation (timeout/erro → PENDENTE, não lança exceção)
 */
export const Route = createFileRoute("/api/v1/modulos/mod-sec/validar")({
  server: {
    handlers: {
      POST: async ({ request }) => {
        const v = await withZod(request, ValidarMODSECSchema);
        if (!v.ok) return v.response;

        if (v.data.esquema_aterramento === "TT") {
          return ok({
            status: "NAO-APLICAVEL",
            esquema_aterramento: "TT",
            motivo:
              "Esquema TT: seccionamento automático (C4) não aplicável — MOD-SEC não é chamado (NBR 5410 5.1.2.2.4)",
          });
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

        try {
          const retorno = await Promise.race([
            clienteModSEC.validar(v.data),
            aguardarAbort(controller.signal),
          ]);

          const validacao = RetornoMODSECSchema.safeParse(retorno);
          if (!validacao.success) {
            return erro("mod_sec_contrato_invalido", "MOD-SEC retornou contrato inválido", 422, {
              issues: validacao.error.issues,
            });
          }

          const { retornosDownstream } = getServicos();
          await retornosDownstream.registrar({
            dependenciaId: v.data.dependencia_id,
            modulo: "MOD-SEC",
            payload: validacao.data,
            recebidoEm: new Date().toISOString(),
          });

          return ok(validacao.data);
        } catch (e) {
          if (e instanceof Error && e.name === "AbortError") {
            console.warn(`[MOD-SEC] Timeout ${TIMEOUT_MS}ms atingido para origem=${v.data.origem}`);
            return erro("mod_sec_timeout", "MOD-SEC timeout", 504, {
              status: "PENDENTE",
              origem: v.data.origem,
            });
          }
          const detalhe = e instanceof Error ? e.message : String(e);
          console.error("[MOD-SEC] Erro ao validar seccionamento:", detalhe);
          return erro("mod_sec_erro", "MOD-SEC retornou erro", 500, {
            status: "PENDENTE",
            detalhes: detalhe,
          });
        } finally {
          clearTimeout(timeoutId);
        }
      },
    },
  },
});

/** Rejeita quando o AbortSignal dispara, permitindo Promise.race com a chamada downstream. */
function aguardarAbort(signal: AbortSignal): Promise<never> {
  return new Promise((_, reject) => {
    signal.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
  });
}

export interface RequestModSEC {
  readonly dependencia_id: string;
  readonly esquema_aterramento: "TT" | "TN-S" | "TN-C" | "TN-C-S" | "IT";
  readonly tempo_atuacao_s: number;
  readonly origem: string;
}

export interface ClienteModSEC {
  validar(params: RequestModSEC): Promise<Record<string, unknown>>;
}

/**
 * MOCK inicial: aprova quando o tempo de atuação respeita o limite de 0,4 s
 * (NBR 5410 tabela 25, U0 = 220 V em esquema TN).
 * TODO: Substituir por chamada HTTP real ao serviço MOD-SEC quando disponível.
 */
async function validarModSECMock(params: RequestModSEC): Promise<Record<string, unknown>> {
  await new Promise((resolve) => setTimeout(resolve, 50));

  const aprovado = params.tempo_atuacao_s <= 0.4;

  return {
    aprovado,
    tempo_seccionamento_s: params.tempo_atuacao_s,
    fonte: "MOD-SEC v1.0",
  };
}

let clienteModSEC: ClienteModSEC = { validar: validarModSECMock };

/** Apenas para testes: substitui o cliente MOD-SEC (ex.: simular timeout/erro/hang). */
export function _setClienteModSECParaTeste(cliente: ClienteModSEC): void {
  clienteModSEC = cliente;
}

/** Apenas para testes: restaura o cliente MOD-SEC mock padrão. */
export function _resetClienteModSECParaTeste(): void {
  clienteModSEC = { validar: validarModSECMock };
}
```

## 7. Consumo dos endpoints MOD-CC e MOD-SEC

N?O ENCONTRADO

## 8. Isolacao de condutores

N?O ENCONTRADO

## 9. Construtor do unifilar

Caminho: `src/domain/unifilar/montar-unifilar-graph.ts` ? total de linhas: 432

```ts
import { classificacaoDe } from "../distribuidora/edp-sp/tipos-aparelho";
import type { DependenciaAgregado } from "../agregado/dependencia-agregado";
import type { CargaAdicional } from "../modelo/dependencia";
import type { Diagnostico } from "../calculo/validacao-padrao-entrada";
import { camposObrigatoriosConformidadePendentes, exigeDr } from "../calculo/conformidade-nbr5410";
import type { Circuito, RastreioIB } from "../modelo/circuito";
import type { Fase, AtribuicaoFases } from "../calculo/balanceamento-fases";
import type { ModoConsumoDivisao } from "../modelo/divisao-circuitos";
import type { ResumoCorrentes } from "../servicos/servico-corrente";
import type {
  CircuitoParaDimensionamento,
  ResultadoDimensionamento,
} from "../dimensionamento-condutores/contratos";
import {
  UNIFILAR_GRAPH_VERSAO,
  UNIFILAR_NODE_BARRAMENTO,
  exportRefDe,
  type ControleUnifilar,
  type FaseRST,
  type SeveridadeUnifilar,
  type TipoCargaUnifilar,
  type UnifilarEdge,
  type UnifilarGraph,
  type UnifilarGroup,
  type UnifilarNode,
  type UnifilarRastreio,
  type UnifilarCondutores,
  type UnifilarSecaoCondutor,
} from "./unifilar-graph";
```

Caminho: `src/domain/unifilar/montar-unifilar-graph.ts` ? total de linhas: 432

```ts
export function montarUnifilarGraph(
  dados: EntradaUnifilarGraph,
  dependencias: ReadonlyArray<DependenciaAgregado>,
  opcoes: OpcoesUnifilarGraph = {},
): UnifilarGraph {
  const piorSeveridade = piorSeveridadePorCircuito(dados.diagnosticos);
  const origemPorCircuito = indexarOrigensPorCircuito(dependencias);
  const provisorio = dados.resumo.provisorio;
  const controle = controleDe(dados.divisaoCircuitos.modoConsumo);
  const resultadosDc = new Map(
    (dados.dimensionamentoCondutores ?? []).map((item) => [item.circuito_id, item]),
  );
  const circuitosDc = new Map(
    (dados.circuitosDimensionamento ?? []).map((item) => [item.id, item]),
  );

  const nodesCircuito: UnifilarNode[] = dados.circuitos.map((circuito) => {
    const origem = origemPorCircuito.get(circuito.id);
    const rastreioIB = dados.rastreios[circuito.id];
    const diagnosticos = diagnosticosDoCircuito(dados.diagnosticos, circuito.id).map(
      (diagnostico) => ({
        codigo: String(diagnostico.codigo),
        severidade: diagnostico.severidade,
        mensagem: diagnostico.mensagem,
      }),
    );
    const rastreio: UnifilarRastreio = {
      regraId: "SIE-IB-01",
      referenciaNormativa: REFERENCIA_IB,
      formula: rastreioIB ? formulaRastreio(rastreioIB) : "IB pendente",
      entradas: entradasRastreio(circuito, rastreioIB),
    };

    const resultadoDc = resultadosDc.get(circuito.id);
    const circuitoDc = circuitosDc.get(circuito.id);
    return {
      id: circuito.id,
      tipoNode: "circuito",
      nome: circuito.nome ?? circuito.id,
      tipoCarga: paraTipoCarga(circuito.tipo),
      fases: paraFasesRST(dados.balanceamentoFases?.[circuito.id], circuito.tipo_ligacao),
      potenciaVA: Math.round(circuito.potencia_total_VA),
      tensaoV: circuito.tensao_V ?? null,
      tensaoConfirmada: circuito.tensao_resolucao ? circuito.tensao_resolucao.confirmada : true,
      ibA: circuito.corrente_projeto_A ?? null,
      requisitoDr: requisitoDr(origem),
      grupoEdp: grupoEDP(origem),
      severidade: severidadeNode(piorSeveridade.get(circuito.id), circuito, origem),
      controle,
      dependenciaId: origem?.dependencia.id ?? null,
      origem: {
        dependenciaId: origem?.dependencia.id ?? null,
        dependenciaLabel: origem?.dependenciaLabel ?? null,
        cargaNome: origem?.carga?.nome ?? null,
      },
      pontos: circuito.cargas.map((carga) => carga.id),
      diagnosticos,
      pendencias: pendenciasDoCircuito(origem, circuito),
      rastreio,
      fonteLinha: rastreioIB ? `IB:${circuito.id}` : "Sem rastreio",
      provisorio,
      exportRef: exportRefDe(circuito.id),
      condutores:
        resultadoDc && circuitoDc ? projetarCondutoresModDc(resultadoDc, circuitoDc) : null,
    };
  });

  const edges: UnifilarEdge[] = nodesCircuito.map((node) => ({
    id: `E-${UNIFILAR_NODE_BARRAMENTO}-${node.id}`,
    de: UNIFILAR_NODE_BARRAMENTO,
    para: node.id,
    tipo: "alimentacao",
  }));

  const grupos = new Map<string, UnifilarNode[]>();
  for (const node of nodesCircuito) {
    const rotulo = node.origem.dependenciaLabel ?? "Sem dependencia";
    const lista = grupos.get(rotulo) ?? [];
    lista.push(node);
    grupos.set(rotulo, lista);
  }
  const groups: UnifilarGroup[] = [...grupos.entries()].map(([rotulo, nodes]) => ({
    id: `G-${rotulo.replace(/\s+/g, "-")}`,
    rotulo,
    criterio: "dependencia",
    nodeIds: nodes.map((node) => node.id),
  }));

  return {
    meta: {
      projetoId: opcoes.projetoId ?? null,
      versao: UNIFILAR_GRAPH_VERSAO,
      origem: "adaptador_1_1",
      modoDivisao: dados.divisaoCircuitos.modoConsumo,
      fallbackMotivo: dados.divisaoCircuitos.fallbackMotivo,
      calculadoEm: opcoes.calculadoEm ?? null,
      provisorio,
    },
    summary: {
      circuitos: nodesCircuito.length,
      ibMaxA: dados.resumo.IB_max_A,
      desequilibrioPct: dados.resumo.desequilibrio_percentual,
      alertas: nodesCircuito.filter((node) => node.severidade === "ATENCAO").length,
      erros: nodesCircuito.filter((node) => node.severidade === "ERRO").length,
      manuais: controle === "manual" ? nodesCircuito.length : 0,
      tensoesPendentes: nodesCircuito.filter((node) => !node.tensaoConfirmada).length,
    },
    nodes: [nodeBarramento(provisorio), ...nodesCircuito],
    edges,
    groups,
  };
}
```

Essa funcao recebe ResultadoCalculo, direta ou indiretamente? Sim. Evidencia: `montarUnifilarGraph` recebe `ReadonlyArray<DependenciaAgregado>`; `DependenciaAgregado.resultado` e `ResultadoCalculo`.

## 10. Validador de catalogo

Caminho: `scripts/validar-catalogo.ts` ? total de linhas: 9

```ts
import { validarCatalogo } from "../src/domain/nbr";

const erros = validarCatalogo();
if (erros.length > 0) {
  console.error("Catálogo NBR inválido:");
  for (const e of erros) console.error(`  - [${e.id}] ${e.mensagem}`);
  process.exit(1);
}
console.log("Catálogo NBR íntegro.");
```

