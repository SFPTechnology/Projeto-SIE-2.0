# EXTRACAO-COMPLEMENTAR-SIE-2

## 1. Contratos do MOD-DC ? arquivo integral

Caminho real: `src/domain/dimensionamento-condutores/contratos.ts` ? total de linhas: 227

```ts
import type {
  FonteNormativa,
  IsolacaoCondutor,
  MaterialCondutor,
  MetodoReferencia,
} from "./normativa";

export type TipoCircuitoDimensionamento = "ILU" | "TUG" | "TUE";
export type TaxaH3 = "nao_declarada" | "ate_15" | "de_15_a_33" | "acima_33";
export type EsquemaAterramento = "TT" | "TN-S" | "TN-C" | "TN-C-S" | "IT";
export type TipoInstalacao = "residencial" | "comercial" | "industrial";
export type OrigemIn = "INFORMADO" | "SUGESTAO" | "MOD-PROT";
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

/**
 * Retorno do MOD-SEC (seccionamento automatico, C4). Contrato conforme PRD
 * MOD-DC §12.5 (ABNT NBR 5410 5.1.2.2.4 via 6.2.6.1.2 d). Aplicavel a esquemas
 * TN e IT; em TT o criterio e NAO-APLICAVEL (nao aguarda retorno).
 */
export interface RetornoMODSEC {
  readonly aprovado: boolean;
  readonly tempo_seccionamento_s: number;
  readonly fonte: string;
}

/**
 * Retorno do MOD-QT (queda de tensao, C5). Contrato conforme PRD MOD-DC §12.6
 * (ABNT NBR 5410 6.2.7). `secao_requerida_mm2` permite ao MOD-QT exigir secao
 * maior; nesse caso o motor revalida a secao de fase (laco do §20).
 */
export interface RetornoMODQT {
  readonly atende: boolean;
  readonly queda_percentual: number;
  readonly limite_aplicado: number;
  readonly secao_requerida_mm2?: number | null;
  readonly fonte: string;
}

/**
 * Retorno do MOD-PROT (protecao/disjuntores), ja resolvido pela camada de
 * aplicacao (global ou override do circuito - PRD MOD-PROT, Story
 * MOD-PROT-3). Diferente de RetornoMODCC/SEC/QT, MOD-PROT nao e um criterio
 * downstream (C3/C4/C5) - e uma entrada de parametro que substitui a
 * heuristica de motor-protecao.ts quando presente (ver ADR
 * mod-prot-contrato-integracao.md, Decisao D5/D6). Tipo definido localmente
 * (nao importado de dimensionamento-disjuntores) para preservar a direcao
 * unica de dependencia entre os dois modulos (ADR, Decisao D2).
 */
export interface RetornoMODPROT {
  readonly in_a: number | null;
  readonly i2_a: number | null;
  readonly norma_dispositivo: string | null;
  readonly capacidade_interrupcao: number | null;
  readonly tempo_atuacao_s: number | null;
}

export interface CircuitoParaDimensionamento {
  readonly id: string;
  readonly descricao: string;
  /** Dependencias de origem para buscar retornos downstream persistidos (MOD-CC/SEC/QT). */
  readonly origem_dependencia_ids?: ReadonlyArray<string>;
  readonly tipo: TipoCircuitoDimensionamento;
  readonly potencia_va: number;
  readonly tensao_v: number | null;
  readonly corrente_projeto_a: number;
  readonly num_fases: 1 | 2 | 3;
  readonly fases: ReadonlyArray<string>;
  readonly tem_neutro: boolean;
  readonly fp_carga?: number | null;
  readonly taxa_h3?: TaxaH3;
  readonly fonte_ib: string;
  /** Retorno do MOD-CC para resolver C3 (curto-circuito). Ausente => PENDENTE. */
  readonly retorno_cc?: RetornoMODCC | null;
  /** Retorno do MOD-SEC para resolver C4 (seccionamento). Ausente => PENDENTE (exceto TT). */
  readonly retorno_seccionamento?: RetornoMODSEC | null;
  /** Retorno do MOD-QT para resolver C5 (queda de tensao). Ausente => PENDENTE. */
  readonly retorno_qt?: RetornoMODQT | null;
  /**
   * Resultado de protecao ja resolvido (global ou override) pela camada de
   * aplicacao. Quando presente e com in_a preenchido, `aplicarSugestaoProtecaoSeAusente`
   * usa este valor em vez de chamar o motor diretamente - unico jeito de um
   * override de MOD-PROT (Story MOD-PROT-2) chegar ate o criterio C2.
   */
  readonly retorno_protecao?: RetornoMODPROT | null;
}

export interface ParametrosDimensionamento {
  readonly material: MaterialCondutor;
  readonly isolacao: IsolacaoCondutor;
  readonly metodo_referencia: MetodoReferencia | null;
  readonly tipo_linha_tabela33?: string | null;
  readonly temperatura_c: number;
  readonly disposicao_agrupamento: string;
  readonly linha_agrupamento_tabela42?: string;
  readonly num_circuitos_agrupados: number;
  readonly isencao_espacamento_2d?: boolean;
  /**
   * Grupo nao semelhante (condutores de secoes/carregamentos diferentes). Quando
   * verdadeiro, o fator de agrupamento tabelado (Tab. 42-45) e substituido por
   * F = 1/sqrt(n), com n = num_circuitos_agrupados (NBR 5410 6.2.5.5).
   */
  readonly grupo_nao_semelhante?: boolean;
  /**
   * Numero de circuitos do agrupamento que podem ser desprezados por conduzirem
   * <= 30% de sua capacidade (isencao NBR 5410 6.2.5.5). Subtraido de n antes da
   * consulta ao fator de agrupamento. Default 0 (nenhum desprezado).
   */
  readonly circuitos_desprezaveis_ate_30pct?: number;
  readonly resistividade_solo_k_m_w?: number;
  readonly esquema_aterramento: EsquemaAterramento;
  readonly tipo_instalacao: TipoInstalacao;
  readonly condicoes_ba5?: boolean;
  readonly condicao_bd?: "BD1" | "BD4" | "outro";
  readonly regime_sobrecarga_severo?: boolean;
  readonly in_a?: number | null;
  readonly origem_in?: OrigemIn | null;
  readonly i2_a?: number | null;
  readonly fonte_i2?: string | null;
  /**
   * Campos publicados pelo MOD-PROT (PRD-MOD-PROT-dimensionamento-disjuntores.md,
   * FR6) quando origem_in === "MOD-PROT". Aditivos - nao alteram o contrato
   * consumido pelo criterio C2 (in_a/origem_in/i2_a/fonte_i2 preservados).
   */
  readonly norma_dispositivo?: string | null;
  readonly capacidade_interrupcao?: number | null;
  readonly tempo_atuacao_s?: number | null;
  readonly neutro_protegido?: boolean;
  readonly circuito_equilibrado?: boolean;
}

export type FonteParametrosDimensionamento = "GLOBAL" | "CUSTOMIZADO";

export type ParametrosDimensionamentoOverride = Partial<ParametrosDimensionamento>;

export interface CircuitoOverrideHistorico {
  readonly timestamp: string;
  readonly acao: "CRIADO" | "MODIFICADO" | "DESCARTADO";
  readonly usuario: string;
  readonly mudancas: ReadonlyArray<{
    readonly campo: string;
    readonly valorAnterior?: unknown;
    readonly valorNovo?: unknown;
  }>;
}

export interface CircuitoOverride {
  readonly useGlobal: boolean;
  readonly customParams?: ParametrosDimensionamentoOverride;
  readonly justificativa?: string;
  readonly criadoEm?: string;
  readonly modificadoEm?: string;
  readonly modificadoPor?: string;
  readonly history?: ReadonlyArray<CircuitoOverrideHistorico>;
}

export interface ResultadoDimensionamentoComParametros extends ResultadoDimensionamento {
  readonly baseadoEm: FonteParametrosDimensionamento;
  readonly parametrosUsados: ParametrosDimensionamento;
  readonly justificativaOverride?: string;
}

export interface RastreioValor {
  readonly fonte: FonteNormativa;
  readonly valor: number | string | null;
  readonly status_verificacao: string;
}

export interface ResultadoDimensionamento {
  readonly circuito_id: string;
  readonly versao_base_normativa: string;
  readonly material: MaterialCondutor;
  readonly isolacao: IsolacaoCondutor;
  readonly metodo_referencia: MetodoReferencia | null;
  readonly temperatura_c: number;
  readonly num_condutores_carregados: number | null;
  readonly fator_neutro_carregado: number | null;
  readonly fatores: Readonly<Record<string, number>>;
  readonly secao_c1_capacidade_mm2: number | null;
  readonly secao_c2_sobrecarga_mm2: number | null;
  readonly secao_c6_minima_mm2: number | null;
  readonly secao_c5_queda_tensao_mm2: number | null;
  readonly secao_c3_curto_mm2: number | null;
  readonly secao_c4_seccionamento_mm2: number | null;
  readonly secao_fase_mm2: number | null;
  readonly secao_neutro_mm2: number | null;
  readonly secao_pe_mm2: number | null;
  readonly secao_pen_mm2: number | null;
  readonly iz_corrigida_a: number | null;
  readonly ib_a: number | null;
  readonly in_a: number | null;
  readonly origem_in: OrigemIn | null;
  readonly i2_a?: number | null;
  readonly fonte_i2?: string | null;
  /** Publicados pelo MOD-PROT quando origem_in === "MOD-PROT" (ver ParametrosDimensionamento). */
  readonly norma_dispositivo?: string | null;
  readonly capacidade_interrupcao?: number | null;
  readonly tempo_atuacao_s?: number | null;
  readonly criterio_decisivo: string | null;
  readonly ib_menor_igual_in: boolean | null;
  readonly in_menor_igual_iz: boolean | null;
  readonly i2_menor_igual_145iz: boolean | null;
  readonly status: StatusDimensionamento;
  readonly criterios: Readonly<Record<"C1" | "C2" | "C3" | "C4" | "C5" | "C6", StatusCriterio>>;
  readonly alertas: ReadonlyArray<string>;
  readonly pendencias: ReadonlyArray<string>;
  readonly erros: ReadonlyArray<string>;
  readonly rastreio: Readonly<Record<string, RastreioValor>>;
}
```

O arquivo importa `IsolacaoCondutor`: linhas 1?4, no import de `./normativa/base-normativa`.

## 2. Schemas Zod dos modulos

Caminho real: `src/api/schemas/otimizar-condutor.schema.ts` ? total de linhas: 145

```ts
import { z } from "@/api/http";
import {
  CircuitoParaDimensionamentoSchema,
  ParametrosDimensionamentoSchema,
} from "./dimensionamento-condutores";

/**
 * Schemas Zod para a rota `POST /api/v1/otimizar-condutor` (Story AUTO-OTI-1.1).
 *
 * REUSO (IDS): `CircuitoParaDimensionamentoSchema` e `ParametrosDimensionamentoSchema`
 * são reaproveitados de `dimensionamento-condutores.ts`. O circuito é estendido com
 * os retornos downstream (MOD-CC/MOD-SEC/MOD-QT) que resolvem C3/C4/C5, presentes no
 * contrato `CircuitoParaDimensionamento` mas ausentes do schema base.
 */

const StatusCriterioSchema = z.enum([
  "APROVADO",
  "REPROVADO",
  "PENDENTE",
  "NAO-APLICAVEL",
  "SEM-DADOS",
]);

/**
 * Schema para request do endpoint MOD-CC (validação de curto-circuito, C3).
 *
 * `dependencia_id` identifica a dependência para persistência em
 * `dependencia_retornos_downstream` (AC4). Não está listado no gherkin do AC1
 * (que documenta apenas os parâmetros de curto-circuito), mas é exigido pela
 * FK da migration 0009 — sem ele o retorno não pode ser auditável por dependência.
 */
export const ValidarMODCCSchema = z.object({
  dependencia_id: z.string().uuid(),
  icc_presumida_a: z.number().positive(),
  tempo_atuacao_s: z.number().positive(),
  integral_joule_dispositivo: z.number().nonnegative(),
  origem: z.string().min(1).max(200),
});

export const RetornoMODCCSchema = z.object({
  icc_presumida_a: z.number(),
  tempo_atuacao_s: z.number(),
  integral_joule_dispositivo: z.number(),
  aprovado: z.boolean(),
  fonte: z.string().min(1),
});

export const RetornoMODSECSchema = z.object({
  aprovado: z.boolean(),
  tempo_seccionamento_s: z.number(),
  fonte: z.string().min(1),
});

/**
 * Schema para request do endpoint MOD-SEC (seccionamento automático, C4 — Story MOD-SEC-1).
 * `dependencia_id` exigido pela FK da migration 0009 (mesma razão do MOD-CC).
 * Enum de aterramento espelha `EsquemaAterramento` do domínio (inclui TN-C).
 * Em esquema TT o endpoint NÃO chama MOD-SEC (AC2): responde NAO-APLICAVEL sem persistir.
 */
export const ValidarMODSECSchema = z.object({
  dependencia_id: z.string().uuid(),
  esquema_aterramento: z.enum(["TT", "TN-S", "TN-C", "TN-C-S", "IT"]),
  tempo_atuacao_s: z.number().positive(),
  origem: z.string().min(1).max(200),
});

/** Resposta do endpoint MOD-SEC quando esquema TT: C4 não aplicável, sem chamada downstream. */
export const NaoAplicavelMODSECSchema = z.object({
  status: z.literal("NAO-APLICAVEL"),
  esquema_aterramento: z.literal("TT"),
  motivo: z.string(),
});

export const RetornoMODQTSchema = z.object({
  atende: z.boolean(),
  queda_percentual: z.number(),
  limite_aplicado: z.number(),
  secao_requerida_mm2: z.number().positive().nullable().optional(),
  fonte: z.string().min(1),
});

/**
 * Schema para request do endpoint MOD-QT (queda de tensão, C5 — Story MOD-QT-1 AC1).
 * Campos do gherkin AC1 + `dependencia_id` (FK migration 0009) + `origem` (auditoria).
 */
export const ValidarMODQTSchema = z.object({
  dependencia_id: z.string().uuid(),
  corrente_a: z.number().positive(),
  comprimento_m: z.number().positive(),
  secao_mm2: z.number().positive(),
  limite_percentual: z.number().positive(),
  origem: z.string().min(1).max(200),
});

export const CircuitoParaOtimizacaoSchema = CircuitoParaDimensionamentoSchema.extend({
  retorno_cc: RetornoMODCCSchema.nullable().optional(),
  retorno_seccionamento: RetornoMODSECSchema.nullable().optional(),
  retorno_qt: RetornoMODQTSchema.nullable().optional(),
});

/** Corpo de requisição da rota de otimização. */
export const OtimizarCondutorSchema = z.object({
  circuito: CircuitoParaOtimizacaoSchema,
  parametros: ParametrosDimensionamentoSchema,
});

// ---- Saída (AC4: validação Zod de entrada/saída) ----

const AvaliacaoCriterioSecaoSchema = z.object({
  criterio: z.enum(["C1", "C2", "C3", "C4", "C5", "C6"]),
  status: StatusCriterioSchema,
  secao_requerida_mm2: z.number().nullable(),
  motivo: z.string().nullable(),
});

const IteracaoOtimizacaoSchema = z.object({
  secao_mm2: z.number(),
  aprovada: z.boolean(),
  criterios: z.array(AvaliacaoCriterioSecaoSchema),
  motivo_reprovacao: z.string().nullable(),
});

const ResumoDimensionamentoOtimizadoSchema = z.object({
  secao_fase_mm2: z.number().nullable(),
  secao_neutro_mm2: z.number().nullable(),
  secao_pe_mm2: z.number().nullable(),
  secao_pen_mm2: z.number().nullable(),
  criterio_decisivo: z.string().nullable(),
  versao_base_normativa: z.string(),
});

export const ResultadoOtimizacaoSchema = z.object({
  status: z.enum(["APROVADO", "IMPOSSIVEL_ATENDER", "PENDENTE_VERIFICACAO"]),
  secaoFinal: z.number().nullable(),
  criterios: z.record(z.enum(["C1", "C2", "C3", "C4", "C5", "C6"]), StatusCriterioSchema),
  criterio_decisivo: z.string().nullable(),
  secoes_testadas: z.number().int().nonnegative(),
  iteracoes: z.array(IteracaoOtimizacaoSchema),
  dimensionamento: ResumoDimensionamentoOtimizadoSchema,
  pendencias: z.array(z.string()),
  erros: z.array(z.string()),
});

export type OtimizarCondutorInput = z.infer<typeof OtimizarCondutorSchema>;
export type ResultadoOtimizacaoOutput = z.infer<typeof ResultadoOtimizacaoSchema>;
```

## 3. Fachada de producao

Caminho real: `src/lib/api-client.ts` ? total de linhas: 501

```ts
import { getServicos } from "@/api/contexto-singleton";
import type { DependenciaAgregado } from "@/domain/agregado/dependencia-agregado";
import type { ProjetoAgregado } from "@/domain/agregado/projeto-agregado";
import type { DependenciaEntradaDTO } from "@/domain/modelo/dependencia";
import type { EventoAuditoria } from "@/domain/estado/eventos";
import type { ResultadoTelaPadraoEntrada } from "@/domain/servicos/servico-padrao-entrada";
import type {
  ResultadoPreparoDimensionamento,
  ResultadoTelaCorrente,
} from "@/domain/servicos/servico-corrente";
import type { PadraoEntradaConfig } from "@/domain/modelo/projeto";
import type { ResultadoTelaParametrosEDP } from "@/domain/servicos/servico-parametros-edp";
import type { ParametrosEDPSPOverrides } from "@/domain/distribuidora/edp-sp/parametros";
import type {
  DivisaoCircuitosManualConfig,
  ResultadoTelaDivisaoCircuitos,
} from "@/domain/modelo/divisao-circuitos";
import type {
  CircuitoParaDimensionamento,
  CircuitoOverride,
  ParametrosDimensionamento,
  TipoInstalacao,
} from "@/domain/dimensionamento-condutores";
import type {
  HistoricoOverrideCircuitoProjetoItem,
  ResultadoDimensionamentoProjeto,
} from "@/domain/servicos/servico-dimensionamento-condutores";
import type { DisjuntorOverride } from "@/domain/dimensionamento-disjuntores";
import type { ResultadoDisjuntoresProjeto } from "@/domain/servicos/servico-dimensionamento-disjuntores";
import type { ResultadoOtimizacao } from "@/domain/calculo/otimizador";
import type { AplicarSecoesResult } from "@/infra/repositorios/repositorio-secoes-otimizadas";
import type { CenarioSimulacao } from "@/domain/queda-tensao";
import type {
  ResultadoAplicacaoCenario,
  ResultadoQuedaTensaoLote,
  ResumoQuedaTensao,
} from "@/domain/servicos/servico-queda-tensao";
import type {
  ConfiguracaoAlimentador,
  PerfilCaboProjeto,
  QuedaTensaoConfig,
} from "@/infra/repositorios/repositorio-queda-tensao-config";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface ApiErrorDetail {
  path: string;
  message: string;
}

function isApiErrorDetailArray(details: unknown): details is ApiErrorDetail[] {
  return (
    Array.isArray(details) &&
    details.every(
      (item) =>
        typeof item === "object" &&
        item !== null &&
        "path" in item &&
        "message" in item &&
        typeof item.path === "string" &&
        typeof item.message === "string",
    )
  );
}

export function formatApiError(err: unknown): string {
  if (err instanceof ApiError && isApiErrorDetailArray(err.details) && err.details.length > 0) {
    const first = err.details[0];
    return first.path ? `${first.path}: ${first.message}` : first.message;
  }
  if (err instanceof Error) return err.message;
  return "Erro inesperado. Tente novamente.";
}

// Mantido para compatibilidade com imports existentes
export interface OkAgregado {
  data: DependenciaAgregado;
  meta: { versao: number; atualizadoEm: string; pendencias: ReadonlyArray<string> };
}

export const api = {
  listarProjetos: (): Promise<ProjetoAgregado[]> => {
    const { ctx } = getServicos();
    return ctx.repoProj.listar().then((r) => Array.from(r));
  },

  projeto: async (projetoId: string): Promise<ProjetoAgregado> => {
    const { ctx } = getServicos();
    const p = await ctx.repoProj.porId(projetoId);
    if (!p) throw new ApiError(404, "not_found", "Projeto não encontrado");
    return p;
  },

  criarProjeto: async (nome: string, _autor: string): Promise<ProjetoAgregado> => {
    const { ctx } = getServicos();
    const id = ctx.idGen.proximo("proj");
    const proj: ProjetoAgregado = { id, nome, dependenciaIds: [], criadoEm: ctx.clock.agora() };
    await ctx.repoProj.salvar(proj);
    return proj;
  },

  editarProjetoNome: async (
    projetoId: string,
    nome: string,
    _autor: string,
  ): Promise<ProjetoAgregado> => {
    const { ctx } = getServicos();
    const proj = await ctx.repoProj.porId(projetoId);
    if (!proj) throw new ApiError(404, "not_found", "Projeto não encontrado");
    const atualizado: ProjetoAgregado = { ...proj, nome: nome.trim() };
    await ctx.repoProj.salvar(atualizado);
    return atualizado;
  },

  listarDependencias: (projetoId: string): Promise<DependenciaAgregado[]> => {
    const { ctx } = getServicos();
    return ctx.repoDep.listar({ projetoId }).then((r) => Array.from(r));
  },

  criarDependencia: async (
    projetoId: string,
    entrada: DependenciaEntradaDTO,
    autor: string,
  ): Promise<DependenciaAgregado> => {
    const { criacao, ctx } = getServicos();
    const proj = await ctx.repoProj.porId(projetoId);
    if (!proj) throw new ApiError(404, "not_found", "Projeto não encontrado");
    const ag = await criacao.criar({ projetoId, entrada, autor });
    await ctx.repoProj.salvar({ ...proj, dependenciaIds: [...proj.dependenciaIds, ag.id] });
    return ag;
  },

  dependencia: async (depId: string): Promise<DependenciaAgregado> => {
    const { ctx } = getServicos();
    const ag = await ctx.repoDep.porId(depId);
    if (!ag) throw new ApiError(404, "not_found", `Dependência ausente: ${depId}`);
    return ag;
  },

  calcular: (depId: string, autor: string): Promise<DependenciaAgregado> => {
    const { calculo } = getServicos();
    return calculo.calcular({ depId, autor });
  },

  editar: (
    depId: string,
    body: {
      campo: string;
      valorNovo: number | string | boolean;
      justificativa: string;
      autor: string;
    },
  ): Promise<DependenciaAgregado> => {
    const { edicao } = getServicos();
    return edicao.editar({
      depId,
      campo: body.campo,
      valorNovo: body.valorNovo,
      justificativa: body.justificativa,
      autor: body.autor,
    });
  },

  validar: (
    depId: string,
    responsavelTecnico: string,
    autor: string,
  ): Promise<DependenciaAgregado> => {
    const { validacao } = getServicos();
    return validacao.validar({ depId, responsavelTecnico, autor });
  },

  recalcular: (
    depId: string,
    novaEntrada: DependenciaEntradaDTO,
    motivo: string,
    autor: string,
  ): Promise<DependenciaAgregado> => {
    const { recalculo } = getServicos();
    return recalculo.onEntradaAlterada({ depId, novaEntrada, motivo, autor });
  },

  excluirDependencia: async (
    depId: string,
    body: { confirmacaoId: string; justificativa: string; autor: string },
  ): Promise<{ id: string; excluidoEm: string }> => {
    if (body.confirmacaoId !== depId) {
      throw new ApiError(
        400,
        "confirmacao_invalida",
        "Confirmação digitada não corresponde ao identificador da dependência.",
      );
    }
    const { ctx } = getServicos();
    const ag = await ctx.repoDep.porId(depId);
    if (!ag) throw new ApiError(404, "not_found", `Dependência ausente: ${depId}`);
    if (ag.estado === "VALIDADA") {
      throw new ApiError(
        409,
        "exclusao_bloqueada",
        "Dependências validadas (CREA/ART) não podem ser excluídas. Revogue a validação primeiro.",
      );
    }
    const em = ctx.clock.agora();
    await ctx.repoAud.append({
      tipo: "DEPENDENCIA_EXCLUIDA",
      depId: ag.id,
      projetoId: ag.projetoId,
      justificativa: body.justificativa,
      autor: body.autor,
      em,
    });
    await ctx.repoDep.excluir(ag.id);
    return { id: ag.id, excluidoEm: em };
  },

  historico: (depId: string): Promise<EventoAuditoria[]> => {
    const { auditoria } = getServicos();
    return auditoria.historico(depId).then((r) => Array.from(r));
  },

  padraoEntrada: (projetoId: string): Promise<ResultadoTelaPadraoEntrada> => {
    const { padraoEntrada } = getServicos();
    return padraoEntrada.obter(projetoId);
  },

  salvarPadraoEntradaConfig: (
    projetoId: string,
    config: PadraoEntradaConfig,
    autor: string,
  ): Promise<ResultadoTelaPadraoEntrada> => {
    const { padraoEntrada } = getServicos();
    return padraoEntrada.atualizarConfig({ projetoId, config, autor });
  },

  correntes: (projetoId: string): Promise<ResultadoTelaCorrente> => {
    const { corrente } = getServicos();
    return corrente.obter(projetoId);
  },

  preparoDimensionamento: (projetoId: string): Promise<ResultadoPreparoDimensionamento> => {
    const { corrente } = getServicos();
    return corrente.obterPreparoDimensionamento(projetoId);
  },

  dimensionarCondutoresLote: (
    projetoId: string,
    parametros: ParametrosDimensionamento,
    circuitoOverrides?: Readonly<Record<string, CircuitoOverride>>,
  ): Promise<ResultadoDimensionamentoProjeto> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.dimensionarLoteProjeto({
      projetoId,
      parametros,
      circuitoOverrides,
    });
  },

  dimensionarCondutorProjeto: (
    projetoId: string,
    circuitoId: string,
    parametros: ParametrosDimensionamento,
    circuitoOverrides?: Readonly<Record<string, CircuitoOverride>>,
  ): Promise<ResultadoDimensionamentoProjeto> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.dimensionarCircuitoProjeto({
      projetoId,
      circuitoId,
      parametros,
      circuitoOverrides,
    });
  },

  /** Auto-Otimização Completa de seção de condutor (Story AUTO-OTI-1.2). */
  otimizarCondutor: (
    circuito: CircuitoParaDimensionamento,
    parametros: ParametrosDimensionamento,
  ): Promise<ResultadoOtimizacao> => {
    const { dimensionamentoCondutores } = getServicos();
    return Promise.resolve(
      dimensionamentoCondutores.otimizarCondutorDireto({ circuito, parametros }),
    );
  },

  aplicarSecoesOtimizadasProjeto: (input: {
    projetoId: string;
    operacaoId: string;
    itens: Array<{
      circuitoId: string;
      parametrosEfetivos: unknown;
      secaoMm2: number;
      secaoEsperadaMm2?: number;
      retornosDownstream?: unknown;
    }>;
  }): Promise<AplicarSecoesResult> => getServicos().aplicarSecoesOtimizadasProjeto(input),

  listarOverridesDimensionamentoCondutores: (
    projetoId: string,
  ): Promise<Readonly<Record<string, CircuitoOverride>>> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.obterOverridesProjeto(projetoId);
  },

  salvarOverrideDimensionamentoCondutores: (
    projetoId: string,
    circuitoId: string,
    override: CircuitoOverride,
    autor: string,
  ): Promise<Readonly<Record<string, CircuitoOverride>>> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.salvarOverrideCircuitoProjeto({
      projetoId,
      circuitoId,
      override,
      autor,
    });
  },

  removerOverrideDimensionamentoCondutores: (
    projetoId: string,
    circuitoId: string,
    autor: string,
  ): Promise<Readonly<Record<string, CircuitoOverride>>> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.removerOverrideCircuitoProjeto({
      projetoId,
      circuitoId,
      autor,
    });
  },

  historicoOverrideDimensionamentoCondutores: (
    projetoId: string,
    circuitoId: string,
  ): Promise<ReadonlyArray<HistoricoOverrideCircuitoProjetoItem>> => {
    const { dimensionamentoCondutores } = getServicos();
    return dimensionamentoCondutores.historicoOverrideCircuitoProjeto(projetoId, circuitoId);
  },

  // ── MOD-PROT (dimensionamento de disjuntores) ─────────────────────────────

  resolverProtecaoLote: (
    projetoId: string,
    tipoInstalacao: TipoInstalacao,
    circuitoOverrides?: Readonly<Record<string, DisjuntorOverride>>,
  ): Promise<ResultadoDisjuntoresProjeto> => {
    const { dimensionamentoDisjuntores } = getServicos();
    return dimensionamentoDisjuntores.resolverProtecaoLoteProjeto({
      projetoId,
      tipoInstalacao,
      circuitoOverrides,
    });
  },

  listarOverridesDimensionamentoDisjuntores: (
    projetoId: string,
  ): Promise<Readonly<Record<string, DisjuntorOverride>>> => {
    const { dimensionamentoDisjuntores } = getServicos();
    return dimensionamentoDisjuntores.obterOverridesProjeto(projetoId);
  },

  salvarOverrideDimensionamentoDisjuntores: (
    projetoId: string,
    circuitoId: string,
    override: DisjuntorOverride,
    autor: string,
  ): Promise<Readonly<Record<string, DisjuntorOverride>>> => {
    const { dimensionamentoDisjuntores } = getServicos();
    return dimensionamentoDisjuntores.salvarOverrideCircuitoProjeto({
      projetoId,
      circuitoId,
      override,
      autor,
    });
  },

  removerOverrideDimensionamentoDisjuntores: (
    projetoId: string,
    circuitoId: string,
    autor: string,
  ): Promise<Readonly<Record<string, DisjuntorOverride>>> => {
    const { dimensionamentoDisjuntores } = getServicos();
    return dimensionamentoDisjuntores.removerOverrideCircuitoProjeto({
      projetoId,
      circuitoId,
      autor,
    });
  },

  // ── MOD-QT (queda de tensão) — Story MOD-QT-2-02, §23.2 ──────────────────────
  // Sempre via `servicoQuedaTensao`, que delega o cálculo ao motor de MOD-QT-2-01.

  quedaTensaoLote: (projetoId: string): Promise<ResultadoQuedaTensaoLote> => {
    const { quedaTensao } = getServicos();
    return quedaTensao.calcularLoteProjeto(projetoId);
  },

  quedaTensaoResumo: (projetoId: string): Promise<ResumoQuedaTensao> => {
    const { quedaTensao } = getServicos();
    return quedaTensao.resumo(projetoId);
  },

  /**
   * MOD-QT-2-04 (C-03): `perfilCabo` é o resultado do fluxo de entrada FECHADO
   * (`SeletorPerfilCabo`). Ausente ⇒ a configuração anterior é preservada pelo serviço e
   * o motor continua fail-closed — nunca um cabo presumido (decisão PO-02).
   */
  configurarAlimentador: (
    projetoId: string,
    alimentador: ConfiguracaoAlimentador,
    autor: string,
    perfilCabo?: PerfilCaboProjeto,
  ): Promise<{ config: QuedaTensaoConfig; atualizadoEm: string }> => {
    const { quedaTensao } = getServicos();
    return quedaTensao.configurarAlimentador({ projetoId, alimentador, autor, perfilCabo });
  },

  definirComprimentoCircuito: (
    projetoId: string,
    circuitoId: string,
    comprimentoM: number,
  ): Promise<QuedaTensaoConfig> => {
    const { quedaTensao } = getServicos();
    return quedaTensao.definirComprimentoCircuito({ projetoId, circuitoId, comprimentoM });
  },

  simularQuedaTensao: (
    projetoId: string,
    circuitoId: string,
    cenarios: ReadonlyArray<CenarioSimulacao>,
    comprimentoM?: number | null,
  ) => {
    const { quedaTensao } = getServicos();
    return quedaTensao.simularCircuito({ projetoId, circuitoId, cenarios, comprimentoM });
  },

  aplicarCenarioQuedaTensao: (args: {
    projetoId: string;
    circuitoId: string;
    cenarioId: string;
    secaoMm2: number;
    comprimentoM: number;
    justificativa: string;
    autor: string;
    parametros: ParametrosDimensionamento;
  }): Promise<ResultadoAplicacaoCenario> => {
    const { quedaTensao } = getServicos();
    return quedaTensao.aplicarCenario(args);
  },

  balancearFases: (projetoId: string, autor: string): Promise<ResultadoTelaCorrente> => {
    const { corrente } = getServicos();
    return corrente.balancear({ projetoId, autor });
  },

  divisaoCircuitos: (projetoId: string): Promise<ResultadoTelaDivisaoCircuitos> => {
    const { divisaoCircuitos } = getServicos();
    return divisaoCircuitos.obter(projetoId);
  },

  salvarDivisaoCircuitosManual: (
    projetoId: string,
    manual: DivisaoCircuitosManualConfig,
    autor: string,
  ): Promise<ResultadoTelaDivisaoCircuitos> => {
    const { divisaoCircuitos } = getServicos();
    return divisaoCircuitos.salvarManual({ projetoId, manual, autor });
  },

  resetarDivisaoCircuitosManual: (
    projetoId: string,
    autor: string,
  ): Promise<ResultadoTelaDivisaoCircuitos> => {
    const { divisaoCircuitos } = getServicos();
    return divisaoCircuitos.resetarManual({ projetoId, autor });
  },

  parametrosEDP: (projetoId: string): Promise<ResultadoTelaParametrosEDP> => {
    const { parametrosEDP } = getServicos();
    return parametrosEDP.obter(projetoId);
  },

  salvarParametrosEDP: (
    projetoId: string,
    overrides: ParametrosEDPSPOverrides,
    autor: string,
  ): Promise<ResultadoTelaParametrosEDP> => {
    const { parametrosEDP } = getServicos();
    return parametrosEDP.atualizar({ projetoId, overrides, autor });
  },
};
```

## 4. Hooks de query

Caminho real: `src/hooks/queries.ts` ? total de linhas: 118

```ts
import { queryOptions } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import { obterCapacidadesExport } from "@/components/unifilar/exportar-unifilar";

export const projetosQuery = () =>
  queryOptions({
    queryKey: ["projetos"],
    queryFn: () => api.listarProjetos(),
  });

export const projetoQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId],
    queryFn: () => api.projeto(projetoId),
    retry: false,
  });

export const dependenciasQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dependencias"],
    queryFn: () => api.listarDependencias(projetoId),
  });

export const historicoQuery = (depId: string) =>
  queryOptions({
    queryKey: ["dependencias", depId, "historico"],
    queryFn: () => api.historico(depId),
  });

export const padraoEntradaQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "padrao-entrada"],
    queryFn: () => api.padraoEntrada(projetoId),
  });

export const correntesQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "correntes"],
    queryFn: () => api.correntes(projetoId),
  });

export const divisaoCircuitosQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "divisao-circuitos"],
    queryFn: () => api.divisaoCircuitos(projetoId),
  });

export const preparoDimensionamentoQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "correntes", "dimensionamento"],
    queryFn: () => api.preparoDimensionamento(projetoId),
  });

export const dimensionamentoCondutoresQuery = (
  projetoId: string,
  parametros: Parameters<typeof api.dimensionarCondutoresLote>[1],
) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dimensionamento-condutores", parametros],
    queryFn: () => api.dimensionarCondutoresLote(projetoId, parametros),
    enabled: false,
  });

export const dimensionamentoCondutoresOverridesQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dimensionamento-condutores", "overrides"],
    queryFn: () => api.listarOverridesDimensionamentoCondutores(projetoId),
  });

export const dimensionamentoCondutoresHistoricoQuery = (projetoId: string, circuitoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dimensionamento-condutores", "historico", circuitoId],
    queryFn: () => api.historicoOverrideDimensionamentoCondutores(projetoId, circuitoId),
  });

export const dimensionamentoDisjuntoresQuery = (
  projetoId: string,
  tipoInstalacao: Parameters<typeof api.resolverProtecaoLote>[1],
) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dimensionamento-disjuntores", tipoInstalacao],
    queryFn: () => api.resolverProtecaoLote(projetoId, tipoInstalacao),
  });

export const dimensionamentoDisjuntoresOverridesQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "dimensionamento-disjuntores", "overrides"],
    queryFn: () => api.listarOverridesDimensionamentoDisjuntores(projetoId),
  });

/** MOD-QT §23.2 — lote de queda de tensão do projeto (Story MOD-QT-2-02). */
export const quedaTensaoLoteQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "queda-tensao", "lote"],
    queryFn: () => api.quedaTensaoLote(projetoId),
  });

/** MOD-QT §23.2 / §24.1 — resumo de conformidade geral. */
export const quedaTensaoResumoQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "queda-tensao", "resumo"],
    queryFn: () => api.quedaTensaoResumo(projetoId),
  });

export const parametrosEDPQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "edp-sp", "parametros"],
    queryFn: () => api.parametrosEDP(projetoId),
  });

export const capacidadesExportQuery = (projetoId: string) =>
  queryOptions({
    queryKey: ["projetos", projetoId, "unifilar", "capacidades-export"],
    // Nunca lança: no SPA (sem servidor) degrada para JSON-only.
    queryFn: () => obterCapacidadesExport(projetoId),
    staleTime: 30_000,
    retry: false,
  });
```

## 5. Perguntas de fechamento

### 5.1

Nao. Nenhum dos arquivos `src/lib/api-client.ts` e `src/hooks/queries.ts` contem MOD-CC, MOD-SEC, mod-cc, mod-sec, retorno_cc ou retorno_seccionamento. Evidencia: busca textual nesses dois caminhos sem ocorrencias.

### 5.2

`src/domain/queda-tensao/motores/motor-queda-tensao.ts`, linhas 69?73: `CONTEXTO_PADRAO_ENDPOINT` define `isolacao: "PVC"`. Nao ha conversao do valor agrupado `EPR/XLPE` do projeto para `EPR` ou `XLPE` em `src/domain/queda-tensao/`; portanto o valor do projeto nao chega ao MOD-QT por esse caminho.

### 5.3

Caminho real: `src/domain/nbr/catalog.data.json` ? total de linhas: 192

```text
F-01 | 9.5.2.1.1 | verificado
F-02 | 9.5.2.1.1 | verificado
F-03 | 9.5.2.2.1.c | VERIFICAR
F-04 | 9.5.2.2.1.a | VERIFICAR
F-05 | 9.5.2.2.1.b | VERIFICAR
F-06 | 9.5.2.2.1.d | VERIFICAR
F-07 | 9.5.2.1.2 | VERIFICAR
F-08 | 9.5.2.1.2 | VERIFICAR
F-09 | 9.5.2.2.1 (nota) | VERIFICAR
```

