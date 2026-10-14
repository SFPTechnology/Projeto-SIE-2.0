# EXTRACAO-COMPLEMENTAR-SIE

## 1. Validacao do catalogo

Caminho real: `src/domain/nbr/catalog.ts` ? total de linhas: 170

```ts
export function validarCatalogo(): ReadonlyArray<ErroValidacao> {
  const erros: ErroValidacao[] = [];

  // IDs únicos
  const ids = new Set<string>();
  for (const r of CATALOG.regras) {
    if (ids.has(r.id)) erros.push({ id: r.id, mensagem: "ID de regra duplicado" });
    ids.add(r.id);
    if (!r.referencia?.item) erros.push({ id: r.id, mensagem: "referencia.item ausente" });
    if (!r.fonte) erros.push({ id: r.id, mensagem: "fonte ausente" });
  }

  // Toda categoria mapeada precisa de cobertura nas tabelas TUG
  const categoriasUsadas = new Set<Categoria>(Object.values(CATALOG.dependencia_categoria));
  for (const c of categoriasUsadas) {
    if (!CATALOG.tabelas.tugQtd.find((t) => t.categoria === c))
      erros.push({ id: c, mensagem: `T-TUG-QTD sem entrada para ${c}` });
    if (!CATALOG.tabelas.tugCarga.find((t) => t.categoria === c))
      erros.push({ id: c, mensagem: `T-TUG-CARGA sem entrada para ${c}` });
  }

  // Tabelas precisam de referência e fonte
  for (const t of todasTabelas()) {
    if (!t.referencia?.item) erros.push({ id: t.id, mensagem: "referencia.item ausente" });
    if (!t.fonte) erros.push({ id: t.id, mensagem: "fonte ausente" });
  }

  return erros;
}

export interface ErroValidacao {
  readonly id: string;
  readonly mensagem: string;
}
```

Caminho real: `src/domain/nbr/catalog.ts` ? total de linhas: 170

```ts
import rawCatalog from "./catalog.data.json";
import type {
  Categoria,
  Dependencia,
  FormulaId,
  RegraNBR,
  TabelaIluminacao,
  TabelaTugQtd,
  TabelaTugCarga,
} from "./types";

interface RawCatalog {
  readonly fonte_padrao: string;
  readonly dependencia_categoria: Readonly<Record<Dependencia, Categoria>>;
  readonly regras: ReadonlyArray<RegraNBR>;
  readonly tabelas: {
    readonly iluminacao: TabelaIluminacao;
    readonly tugQtd: ReadonlyArray<TabelaTugQtd>;
    readonly tugCarga: ReadonlyArray<TabelaTugCarga>;
  };
}

const CATALOG = rawCatalog as unknown as RawCatalog;

export function categoriaDe(dependencia: Dependencia): Categoria {
  const cat = CATALOG.dependencia_categoria[dependencia];
  if (!cat) {
    throw new Error(`Dependência sem categoria mapeada no catálogo: ${dependencia}`);
  }
  return cat;
}

export function regra(id: FormulaId): RegraNBR {
  const r = CATALOG.regras.find((x) => x.id === id);
  if (!r) throw new Error(`Regra normativa ausente do catálogo: ${id}`);
  return r;
}

export function todasRegras(): ReadonlyArray<RegraNBR> {
  return CATALOG.regras;
}

export function regrasPendentes(): ReadonlyArray<FormulaId> {
  return CATALOG.regras.filter((r) => r.status_verificacao === "VERIFICAR").map((r) => r.id);
}

export function dependenciasSuportadas(): ReadonlyArray<Dependencia> {
  return Object.keys(CATALOG.dependencia_categoria) as Dependencia[];
}

export const FONTE_PADRAO = CATALOG.fonte_padrao;

// ===== Tabelas normativas (T-*) =====

export function tabelaIluminacao(): TabelaIluminacao {
  return CATALOG.tabelas.iluminacao;
}

export function tugQtdPara(categoria: Categoria): TabelaTugQtd {
  const t = CATALOG.tabelas.tugQtd.find((x) => x.categoria === categoria);
  if (!t) throw new Error(`T-TUG-QTD ausente para categoria ${categoria}`);
  return t;
}

export function tugCargaPara(categoria: Categoria): TabelaTugCarga {
  const t = CATALOG.tabelas.tugCarga.find((x) => x.categoria === categoria);
  if (!t) throw new Error(`T-TUG-CARGA ausente para categoria ${categoria}`);
  return t;
}

export function todasTabelas(): ReadonlyArray<TabelaIluminacao | TabelaTugQtd | TabelaTugCarga> {
  return [CATALOG.tabelas.iluminacao, ...CATALOG.tabelas.tugQtd, ...CATALOG.tabelas.tugCarga];
}

export interface ItemPendencia {
  readonly id: string;
  readonly tipo: "REGRA" | "TABELA";
  readonly categoria: string;
  readonly descricao: string;
  readonly itemNBR: string;
  readonly status: StatusVerificacao;
  readonly fonteRequerida: string;
  readonly validadorResponsavel: string;
}

const VALIDADOR_PADRAO = "Eng. Eletricista responsável técnico (ART)";

function fonteRequeridaDefault(item: string): string {
  return `ABNT NBR 5410:2004, item ${item} — texto integral`;
}

/**
 * Tracker de pendências derivado do próprio catálogo: lista toda regra ou
 * tabela com `status_verificacao = "VERIFICAR"`, incluindo a fonte que
 * precisa ser consultada e o validador responsável.
 */
export function pendenciasCatalogo(): ReadonlyArray<ItemPendencia> {
  const itens: ItemPendencia[] = [];
  for (const r of CATALOG.regras) {
    if (r.status_verificacao !== "VERIFICAR") continue;
    itens.push({
      id: r.id,
      tipo: "REGRA",
      categoria: r.categoria,
      descricao: r.descricao,
      itemNBR: r.referencia.item,
      status: r.status_verificacao,
      fonteRequerida: fonteRequeridaDefault(r.referencia.item),
      validadorResponsavel: VALIDADOR_PADRAO,
    });
  }
  for (const t of todasTabelas()) {
    if (t.status_verificacao !== "VERIFICAR") continue;
    const categoria = "categoria" in t ? (t as TabelaTugQtd).categoria : "GERAL";
    const descricao = "descricao" in t ? (t as TabelaIluminacao).descricao : t.id;
    itens.push({
      id: t.id,
      tipo: "TABELA",
      categoria,
      descricao,
      itemNBR: t.referencia.item,
      status: t.status_verificacao,
      fonteRequerida: t.fonte_requerida ?? fonteRequeridaDefault(t.referencia.item),
      validadorResponsavel: t.validador_responsavel ?? VALIDADOR_PADRAO,
    });
  }
  return itens;
}

export interface ErroValidacao {
  readonly id: string;
  readonly mensagem: string;
}

/**
 * Valida a integridade interna do catálogo. Retorna lista de erros — vazio
 * quando o catálogo é coerente.
 */
export function validarCatalogo(): ReadonlyArray<ErroValidacao> {
  const erros: ErroValidacao[] = [];

  // IDs únicos
  const ids = new Set<string>();
  for (const r of CATALOG.regras) {
    if (ids.has(r.id)) erros.push({ id: r.id, mensagem: "ID de regra duplicado" });
    ids.add(r.id);
    if (!r.referencia?.item) erros.push({ id: r.id, mensagem: "referencia.item ausente" });
    if (!r.fonte) erros.push({ id: r.id, mensagem: "fonte ausente" });
  }

  // Toda categoria mapeada precisa de cobertura nas tabelas TUG
  const categoriasUsadas = new Set<Categoria>(Object.values(CATALOG.dependencia_categoria));
  for (const c of categoriasUsadas) {
    if (!CATALOG.tabelas.tugQtd.find((t) => t.categoria === c))
      erros.push({ id: c, mensagem: `T-TUG-QTD sem entrada para ${c}` });
    if (!CATALOG.tabelas.tugCarga.find((t) => t.categoria === c))
      erros.push({ id: c, mensagem: `T-TUG-CARGA sem entrada para ${c}` });
  }

  // Tabelas precisam de referência e fonte
  for (const t of todasTabelas()) {
    if (!t.referencia?.item) erros.push({ id: t.id, mensagem: "referencia.item ausente" });
    if (!t.fonte) erros.push({ id: t.id, mensagem: "fonte ausente" });
  }

  return erros;
}

// Re-export de tipos auxiliares
import type { StatusVerificacao } from "./types";
```

## 2. Motor de calculo ? integral

Caminho real: `src/domain/calculo/motor.ts` ? total de linhas: 130

```ts
import { regrasPendentes, tabelaIluminacao, tugQtdPara, tugCargaPara } from "../nbr/catalog";
import type { Categoria, FormulaId, ResultadoCalculo } from "../nbr/types";
import type { DependenciaEntrada } from "../modelo/dependencia";
import { categoriaDaEntrada } from "../modelo/dependencia";
import type { Projeto } from "../modelo/projeto";
import { area, perimetro } from "./geometria";
import { cargaIluminacao } from "./iluminacao";
import { cargaTUG } from "./tomadas";
import { cargasAdicionais } from "./cargas-adicionais";
import { diagnosticosConformidadeNBR5410 } from "./conformidade-nbr5410";

function statusDeTabela(cat: Categoria) {
  return {
    ilum: tabelaIluminacao().status_verificacao,
    qtd: tugQtdPara(cat).status_verificacao,
    carga: tugCargaPara(cat).status_verificacao,
  };
}

/** Calcula uma dependência (resultado tipado e rastreável). */
export function calcularDependencia(d: DependenciaEntrada): ResultadoCalculo {
  const cat = categoriaDaEntrada(d);
  const A = area(d);
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
    readonly tomadas_qtd: number;
    readonly cargas_adicionais_va: number;
    readonly cargas_adicionais_por_categoria: {
      readonly iluminacao_va: number;
      readonly tue_va: number;
      readonly outra_va: number;
    };
  };
  readonly pendencias: ReadonlyArray<FormulaId>;
}

export function calcularProjeto(p: Projeto): ResultadoProjeto {
  const deps = p.dependencias.map(calcularDependencia);
  const totais = deps.reduce(
    (acc, r) => ({
      iluminacao_va: acc.iluminacao_va + r.iluminacao.valor.vaTotal,
      tomadas_va: acc.tomadas_va + r.tomadas.valor.vaTotal,
      tomadas_qtd: acc.tomadas_qtd + r.tomadas.valor.quantidade,
      cargas_adicionais_va: acc.cargas_adicionais_va + r.cargasAdicionais.valor.vaTotal,
      cargas_adicionais_por_categoria: {
        iluminacao_va:
          acc.cargas_adicionais_por_categoria.iluminacao_va +
          r.cargasAdicionais.valor.vaPorCategoria.iluminacao,
        tue_va:
          acc.cargas_adicionais_por_categoria.tue_va + r.cargasAdicionais.valor.vaPorCategoria.tue,
        outra_va:
          acc.cargas_adicionais_por_categoria.outra_va +
          r.cargasAdicionais.valor.vaPorCategoria.outra,
      },
    }),
    {
      iluminacao_va: 0,
      tomadas_va: 0,
      tomadas_qtd: 0,
      cargas_adicionais_va: 0,
      cargas_adicionais_por_categoria: {
        iluminacao_va: 0,
        tue_va: 0,
        outra_va: 0,
      },
    },
  );
  const pend = Array.from(new Set(deps.flatMap((d) => d.pendencias)));
  return {
    projeto: { id: p.id, nome: p.nome },
    dependencias: deps,
    totais,
    pendencias: pend,
  };
}
```

## 3. Amostra do catalogo

Caminho real: `src/domain/nbr/catalog.data.json` ? total de linhas: 192

```json
{
  "fonte_padrao": "Especificação Técnica Orientadora — Bloco 1 v13 (NBR 5410:2004)",
  "regras": [
    {
      "id": "F-01",
      "categoria": "GERAL",
      "descricao": "Área da dependência: A = C · L (m²)",
      "parametros": {},
      "referencia": {
        "norma": "NBR 5410:2004",
        "item": "9.5.2.1.1"
      },
      "status_verificacao": "verificado",
      "fonte": "Geometria — base-fonte"
    },
    {
      "id": "F-02",
      "categoria": "GERAL",
      "descricao": "Perímetro da dependência: P = 2·(C + L) (m)",
      "parametros": {},
      "referencia": {
        "norma": "NBR 5410:2004",
        "item": "9.5.2.1.1"
      },
      "status_verificacao": "verificado",
      "fonte": "Geometria — base-fonte"
    }
  ],
  "tabelas": [
    {
      "id": "T-ILUM-CARGA",
      "descricao": "Carga mínima de iluminação a atribuir por recinto — previsão de carga (NÃO projeto luminotécnico). A ≤ 6 m²: 100 VA; A > 6 m²: 100 + 60·⌊(A−6)/4⌋ VA. Nível de iluminância (lux) por tarefa: NBR ISO/CIE 8995-1, fora deste critério.",
      "vaBase": 100,
      "areaLimiteM2": 6,
      "vaAdicional": 60,
      "passoAreaM2": 4,
      "pontosMin": 1,
      "referencia": {
        "norma": "NBR 5410:2004",
        "item": "9.5.2.1.2"
      },
      "status_verificacao": "VERIFICAR",
      "fonte": "Especificação Técnica Orientadora — Bloco 1 v13",
      "fonte_requerida": "ABNT NBR 5410:2004, item 9.5.2.1.2 — texto integral",
      "validador_responsavel": "Eng. Eletricista responsável técnico (ART)"
    },
    {
      "id": "T-TUG-QTD/CAT-A",
      "categoria": "CAT-A",
      "regra": "ceil(P/5)",
      "espacamentoMaxM": 5,
      "referencia": {
        "norma": "NBR 5410:2004",
        "item": "9.5.2.2.1.c"
      },
      "status_verificacao": "VERIFICAR",
      "fonte": "Especificação Técnica Orientadora — Bloco 1 v13",
      "fonte_requerida": "ABNT NBR 5410:2004, item 9.5.2.2.1.c",
      "validador_responsavel": "Eng. Eletricista responsável técnico (ART)"
    }
  ]
}
```

## 4. Isolacao de condutores

Caminho real: `src/domain/modelo/projeto.ts` ? total de linhas: 32

```ts
import type { DependenciaEntrada } from "./dependencia";
import type { DivisaoCircuitosConfig } from "./divisao-circuitos";
import type { FatorDemanda, PadraoEntrada } from "./padrao-entrada";
import type { PadraoFornecimento } from "./padrao-fornecimento";
import type { AtribuicaoFases } from "../calculo/balanceamento-fases";

export type IsolacaoCondutor = "PVC" | "EPR/XLPE";

/** Configuração persistida no projeto: catálogo da distribuidora + fatores
 *  de demanda + override manual do padrão (quando ambiguidade). */
export interface PadraoEntradaConfig {
  readonly catalogo: ReadonlyArray<PadraoFornecimento>;
  readonly fatoresDemanda: ReadonlyArray<FatorDemanda>;
  /** Override manual de seleção; vazio = automático. */
  readonly padraoSelecionadoIdOverride?: string;
  /** Limite (A) para ATN-IB-TERMINAL-ALTA. Default 63 quando ausente. */
  readonly ibAtencaoA?: number;
  /** Atribuição persistida de fases A/B/C por circuito (LPT). */
  readonly balanceamentoFases?: AtribuicaoFases;
  /** Isolação adotada para a seção do condutor de entrada exibida na Saída B. */
  readonly isolacaoCondutor?: IsolacaoCondutor;
  readonly divisaoCircuitos?: DivisaoCircuitosConfig;
}

export interface Projeto {
  readonly id: string;
  readonly nome: string;
  readonly dependencias: ReadonlyArray<DependenciaEntrada>;
  /** Padrão de entrada do projeto (Fase 1: opcional; preenchido na Fase 2). */
  readonly padraoEntrada?: PadraoEntrada;
  readonly padraoEntradaConfig?: PadraoEntradaConfig;
}
```

Caminho real: `src/domain/queda-tensao/contratos.ts` ? total de linhas: 134

```ts
/**
 * Contratos INTERNOS do MOD-QT (motor de queda de tensão).
 *
 * ATENÇÃO: nada aqui é contrato público. O contrato público do endpoint
 * (`RetornoMODQT` / `RetornoMODQTSchema` / `ValidarMODQTSchema`) é INALTERÁVEL e
 * vive em `@/domain/dimensionamento-condutores/contratos` e
 * `@/api/schemas/otimizar-condutor.schema` — ver PROMPT-QUEDA-TENSAO-v2.2 §15.1 e §31.
 *
 * Fonte: PROMPT-QUEDA-TENSAO-v2.2 (MOD-QT-v2.2) §15.2.
 */

/** Versão do módulo, exposta no campo `fonte` do contrato público (§16.1). */
export const VERSAO_MODULO_QT = "MOD-QT-v2.2";

export type MaterialCondutorQT = "Cu" | "Al";
export type IsolacaoCondutorQT = "PVC" | "EPR" | "XLPE";
export type NumeroFasesQT = 1 | 2 | 3;
export type MetodoCalculoQuedaTensao = "SIMPLIFICADO" | "COMPLETO";

/** R-01: todo valor normativo carrega status de verificação explícito. */
export type StatusVerificacaoQT = "CONFIRMADO" | "PENDENTE" | "[VERIFICAR]";

/**
 * Requisição do motor — espelha os campos do `ValidarMODQTSchema` já em produção
 * (§15.1.1). NÃO é o schema Zod: é apenas a forma esperada pelo motor, para que o
 * handler possa repassar `v.data` sem conversão.
 */
export interface RequisicaoQuedaTensao {
  readonly dependencia_id: string;
  readonly corrente_a: number;
  readonly comprimento_m: number;
  readonly secao_mm2: number;
  readonly limite_percentual: number;
  readonly origem: string;
}

/**
 * Contexto do circuito/projeto que NÃO trafega no contrato público de request
 * (§15.1.1 não carrega material, isolação, número de fases, fp nem tensão).
 * Todos os campos são opcionais; os padrões estão em `CONTEXTO_PADRAO_ENDPOINT`.
 */
export interface ContextoQuedaTensao {
  readonly material?: MaterialCondutorQT;
  readonly isolacao?: IsolacaoCondutorQT;
  readonly num_fases?: NumeroFasesQT;
  readonly fp_carga?: number;
  readonly tensao_v?: number;
  readonly comprimento_alimentador_m?: number | null;
  readonly secao_alimentador_mm2?: number | null;
  readonly material_alimentador?: MaterialCondutorQT;
  // ── Story MOD-QT-2-03 (AC16 / Task 5B) — campos controlados do parecer §3.2 ──
  // Trafegam POR AQUI (contrato interno, extensível), NUNCA por `ValidarMODQTSchema`.
  // Dos cinco campos controlados, `secao_mm2` vem de `RequisicaoQuedaTensao` e `metal`
  // é derivado de `material` (Cu→CU / Al→AL). Não há valor padrão: ausência é rejeição
  // determinística no resolvedor (decisão PO-02, fail-closed).
  /** Alias comercial de família de cabo (13 opções do catálogo). Sem padrão. */
  readonly familia_id?: string;
  /** Topologia de instalação (12 opções publicadas). Sem padrão. */
  readonly topologia_coluna_id?: string;
  /** Validado por coerência com a topologia — nunca usado como filtro do catálogo. */
  readonly quantidade_de_condutores_carregados?: number;
  /** Topologia do trecho de alimentador, quando difere da do circuito terminal. */
  readonly topologia_alimentador_coluna_id?: string;
  /** Família do trecho de alimentador, quando difere da do circuito terminal. */
  readonly familia_alimentador_id?: string;
  // ── Story MOD-QT-2-04 (C-05 / AC9) — escopo de atendimento do projeto ────────
  /**
   * `perfil_id` do perfil de limite de atendimento explicitamente selecionado
   * (`PERFIS_LIMITE_ATENDIMENTO`). Ausente = nenhum perfil resolvido: o limite total
   * segue sendo o valor informado na requisição e a marcação `[VERIFICAR — alínea
   * 6.2.7.1]` permanece (VER-QT-07 aberto fora do perfil). Nunca tem valor padrão.
   */
  readonly perfil_limite_id?: string;
}

…10805 tokens truncated…Condutor;
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

## 8. Onde os retornos downstream sao consumidos

Caminho real: `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts` ? total de linhas: 415

```ts
import type {
  CircuitoParaDimensionamento,
  ParametrosDimensionamento,
  RastreioValor,
  ResultadoDimensionamento,
  StatusCriterio,
} from "./contratos";
import { resolverStatusDimensionamento, resumirResultadosDimensionamento } from "./estados";
import { calcularCapacidadeCorrenteC1 } from "./motores/motor-capacidade-corrente";
import { calcularSecaoMinimaC6 } from "./motores/motor-secao-minima";
import { verificarSobrecargaC2 } from "./motores/motor-sobrecarga";
import { dimensionarNeutro } from "./motores/motor-neutro";
import { dimensionarPe, dimensionarPen } from "./motores/motor-pe-pen";
import { validarEntradasDimensionamento } from "./validacao/validador-entradas";
import { BASE_NORMATIVA_CONDUTORES } from "./normativa/base-normativa";
import {
  ErroConsultaNormativa,
  RepositorioNormativoMemoria,
} from "./normativa/repositorio-normativo";

const ordemCriterios = ["C1", "C2", "C5", "C6"] as const;
const SERIE_SECOES = [
  0.5, 0.75, 1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630,
];

/** Normaliza um valor de secao para a serie comercial (>= valor). */
function normalizarSecao(valor: number): number {
  return SERIE_SECOES.find((secao) => secao >= valor) ?? SERIE_SECOES[SERIE_SECOES.length - 1];
}

function criterioDecisivo(
  valores: Readonly<Record<(typeof ordemCriterios)[number], number | null>>,
): string | null {
  let decisivo: string | null = null;
  let maior = -Infinity;
  for (const criterio of ordemCriterios) {
    const valor = valores[criterio];
    if (valor != null && valor > maior) {
      maior = valor;
      decisivo = criterio;
    }
  }
  return decisivo;
}

function fatorTotalC1(fatores: Readonly<Record<string, number>>): number | null {
  const valores = ["FCT", "FRS", "FCA", "neutro"].map((chave) => fatores[chave]);
  if (valores.some((valor) => valor == null)) return null;
  return valores.reduce((acc, valor) => acc * valor, 1);
}

function izCorrigidaParaSecao(args: {
  readonly secao: number;
  readonly c1: ReturnType<typeof calcularCapacidadeCorrenteC1>;
  readonly parametros: ParametrosDimensionamento;
  readonly repo?: RepositorioNormativoMemoria;
}): number | null {
  const fatorTotal = fatorTotalC1(args.c1.fatores);
  if (fatorTotal == null || args.parametros.metodo_referencia == null) return null;

  try {
    const repo = args.repo ?? new RepositorioNormativoMemoria();
    const isolacaoNormativa =
      args.parametros.isolacao === "XLPE" ? "EPR" : args.parametros.isolacao;
    const linha = repo.consultarTabelaIz({
      tabela_nbr: args.parametros.isolacao === "PVC" ? "36" : "37",
      material: args.parametros.material,
      isolacao: isolacaoNormativa,
      metodo_referencia: args.parametros.metodo_referencia,
      num_condutores_carregados: args.c1.condutores.coluna_tabela_iz,
      secao_mm2: args.secao,
    });
    return linha.corrente_a * fatorTotal;
  } catch (erro) {
    if (erro instanceof ErroConsultaNormativa) return null;
    throw erro;
  }
}

function resolverSobrecargaC2PorSecao(args: {
  readonly circuito: CircuitoParaDimensionamento;
  readonly parametros: ParametrosDimensionamento;
  readonly c1: ReturnType<typeof calcularCapacidadeCorrenteC1>;
  readonly secaoBase: number;
}): ReturnType<typeof verificarSobrecargaC2> {
  const base = verificarSobrecargaC2({
    ib_a: args.circuito.corrente_projeto_a,
    in_a: args.parametros.in_a,
    i2_a: args.parametros.i2_a,
    iz_corrigida_a: args.c1.iz_corrigida_a,
    secao_candidata_mm2: args.secaoBase || null,
    parametros: args.parametros,
  });

  // IB > In nao e corrigido por aumentar secao: a protecao esta subdimensionada para a carga.
  if (base.ib_menor_igual_in === false) return base;
  if (!base.reprovado) return base;

  let tentouSecaoSemDadoNormativo = false;
  for (const secao of SERIE_SECOES) {
    if (secao < args.secaoBase) continue;
    const izCorrigida = izCorrigidaParaSecao({
      secao,
      c1: args.c1,
      parametros: args.parametros,
    });
    if (izCorrigida == null) {
      tentouSecaoSemDadoNormativo = true;
      continue;
    }

    const candidato = verificarSobrecargaC2({
      ib_a: args.circuito.corrente_projeto_a,
      in_a: args.parametros.in_a,
      i2_a: args.parametros.i2_a,
      iz_corrigida_a: izCorrigida,
      secao_candidata_mm2: secao,
      parametros: args.parametros,
    });
    if (!candidato.reprovado) return candidato;
  }

  if (tentouSecaoSemDadoNormativo) {
    const tabela = args.parametros.isolacao === "PVC" ? "36" : "37";
    return {
      ...base,
      pendencias: [...base.pendencias, `VER-DC-01-TABELA-${tabela}-INCOMPLETA-C2`],
      reprovado: false,
    };
  }

  return base;
}

interface ResolucaoCriterioDownstream {
  readonly status: StatusCriterio;
  readonly pendencia: string | null;
  readonly secao_mm2: number | null;
  readonly rastreio: RastreioValor | null;
}

/**
 * Resolve C3 (curto-circuito) a partir do retorno do MOD-CC. Sem retorno o
 * criterio permanece PENDENTE com `AGUARDANDO-CC` (PRD MOD-DC §12.4). Este
 * modulo NAO calcula a integral de Joule; apenas consome o veredito downstream.
 */
function resolverC3Curto(
  retorno: CircuitoParaDimensionamento["retorno_cc"],
  secaoFase: number,
): ResolucaoCriterioDownstream {
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
      status_verificacao: "CONFIRMADO",
    },
  };
}

/**
 * Resolve C4 (seccionamento automatico) a partir do retorno do MOD-SEC. Em
 * esquema TT o criterio e NAO-APLICAVEL (registrado, nao omitido); em TN/IT
 * permanece PENDENTE com `AGUARDANDO-SECCIONAMENTO` ate o retorno (§12.5).
 */
function resolverC4Seccionamento(
  retorno: CircuitoParaDimensionamento["retorno_seccionamento"],
  esquemaAterramento: ParametrosDimensionamento["esquema_aterramento"],
  secaoFase: number,
): ResolucaoCriterioDownstream {
  if (esquemaAterramento === "TT") {
    return { status: "NAO-APLICAVEL", pendencia: null, secao_mm2: null, rastreio: null };
  }
  if (retorno == null) {
    return {
      status: "PENDENTE",
      pendencia: "AGUARDANDO-SECCIONAMENTO",
      secao_mm2: null,
      rastreio: null,
    };
  }
  return {
    status: retorno.aprovado ? "APROVADO" : "REPROVADO",
    pendencia: null,
    secao_mm2: retorno.aprovado ? secaoFase : null,
    rastreio: {
      fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "5.1.2.2.4" },
      valor: retorno.tempo_seccionamento_s,
      status_verificacao: "CONFIRMADO",
    },
  };
}

/**
 * Resolve C5 (queda de tensao) a partir do retorno do MOD-QT. Sem retorno o
 * criterio permanece PENDENTE com `AGUARDANDO-QT` (§12.6). Este modulo NAO
 * calcula queda de tensao; apenas integra o veredito e a eventual secao exigida.
 */
function resolverC5Queda(
  retorno: CircuitoParaDimensionamento["retorno_qt"],
): ResolucaoCriterioDownstream {
  if (retorno == null) {
    return { status: "PENDENTE", pendencia: "AGUARDANDO-QT", secao_mm2: null, rastreio: null };
  }
  const secaoRequerida =
    retorno.secao_requerida_mm2 != null ? normalizarSecao(retorno.secao_requerida_mm2) : null;
  return {
    status: retorno.atende ? "APROVADO" : "REPROVADO",
    pendencia: null,
    secao_mm2: secaoRequerida,
    rastreio: {
      fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "6.2.7" },
      valor: retorno.queda_percentual,
      status_verificacao: "CONFIRMADO",
    },
  };
}

export function dimensionarCircuito(
  circuito: CircuitoParaDimensionamento,
  parametros: ParametrosDimensionamento,
): ResultadoDimensionamento {
  const diagnosticosEntrada = validarEntradasDimensionamento(circuito, parametros);
  const erros = diagnosticosEntrada.map((diagnostico) => diagnostico.codigo);
  if (erros.length > 0) {
    const criterios: ResultadoDimensionamento["criterios"] = {
      C1: "SEM-DADOS",
      C2: "SEM-DADOS",
      C3: "PENDENTE",
      C4: "PENDENTE",
      C5: "PENDENTE",
      C6: "SEM-DADOS",
    };
    return {
      circuito_id: circuito.id,
      versao_base_normativa: BASE_NORMATIVA_CONDUTORES.versao,
      material: parametros.material,
      isolacao: parametros.isolacao,
      metodo_referencia: parametros.metodo_referencia,
      temperatura_c: parametros.temperatura_c,
      num_condutores_carregados: null,
      fator_neutro_carregado: null,
      fatores: {},
      secao_c1_capacidade_mm2: null,
      secao_c2_sobrecarga_mm2: null,
      secao_c6_minima_mm2: null,
      secao_c5_queda_tensao_mm2: null,
      secao_c3_curto_mm2: null,
      secao_c4_seccionamento_mm2: null,
      secao_fase_mm2: null,
      secao_neutro_mm2: null,
      secao_pe_mm2: null,
      secao_pen_mm2: null,
      iz_corrigida_a: null,
      ib_a: circuito.corrente_projeto_a,
      in_a: parametros.in_a ?? null,
      origem_in: parametros.origem_in ?? null,
      i2_a: parametros.i2_a ?? null,
      fonte_i2: parametros.fonte_i2 ?? null,
      norma_dispositivo: parametros.norma_dispositivo ?? null,
      capacidade_interrupcao: parametros.capacidade_interrupcao ?? null,
      tempo_atuacao_s: parametros.tempo_atuacao_s ?? null,
      criterio_decisivo: null,
      ib_menor_igual_in: null,
      in_menor_igual_iz: null,
      i2_menor_igual_145iz: null,
      status: resolverStatusDimensionamento({ erros, pendencias: [], criterios }),
      criterios,
      alertas: [],
      pendencias: [],
      erros,
      rastreio: {},
    };
  }

  const c1 = calcularCapacidadeCorrenteC1(circuito, parametros);
  const c6 = calcularSecaoMinimaC6(circuito, parametros);
  const secaoBase = Math.max(c1.secao_mm2 ?? 0, c6);
  const c2 = resolverSobrecargaC2PorSecao({
    circuito,
    parametros,
    c1,
    secaoBase,
  });
  const secaoC2Ajustada = c2.secao_mm2;
  const c2Reprovado = c2.reprovado;

  // Secao de fase pelos criterios obrigatorios ja conhecidos (C1, C2, C6).
  const secaoFaseObrigatoria = Math.max(c1.secao_mm2 ?? 0, secaoC2Ajustada ?? 0, c6);

  // Criterios downstream (C3/C4/C5). C5 pode exigir secao maior e revalidar a fase.
  const c5 = resolverC5Queda(circuito.retorno_qt);
  const secaoFase = Math.max(secaoFaseObrigatoria, c5.secao_mm2 ?? 0);
  const c3 = resolverC3Curto(circuito.retorno_cc, secaoFase);
  const c4 = resolverC4Seccionamento(
    circuito.retorno_seccionamento,
    parametros.esquema_aterramento,
    secaoFase,
  );

  // Neutro/PE/PEN dimensionados sobre a secao de fase final (pos-revalidacao C5).
  const neutro = dimensionarNeutro(circuito, secaoFase, parametros);

  const decisivo = criterioDecisivo({
    C1: c1.secao_mm2,
    C2: secaoC2Ajustada,
    C5: c5.secao_mm2,
    C6: c6,
  });

  const c5ElevouSecao = (c5.secao_mm2 ?? 0) > secaoFaseObrigatoria;
  const alertas = [...c1.alertas, ...(c5ElevouSecao ? ["C5-QUEDA-TENSAO-ELEVOU-SECAO"] : [])];

  const pendencias = [
    ...c1.pendencias,
    ...c2.pendencias,
    ...neutro.pendencias,
    c3.pendencia,
    c4.pendencia,
    c5.pendencia,
  ].filter((item): item is string => Boolean(item));
  const criterios: Record<"C1" | "C2" | "C3" | "C4" | "C5" | "C6", StatusCriterio> = {
    C1: c1.erros.length > 0 ? "PENDENTE" : "APROVADO",
    C2: c2Reprovado ? "REPROVADO" : c2.pendencias.length > 0 ? "PENDENTE" : "APROVADO",
    C3: c3.status,
    C4: c4.status,
    C5: c5.status,
    C6: "APROVADO",
  };
  const errosFinais = [...c1.erros];

  const rastreioDownstream: Record<string, RastreioValor> = {};
  if (c3.rastreio) rastreioDownstream.c3_curto = c3.rastreio;
  if (c4.rastreio) rastreioDownstream.c4_seccionamento = c4.rastreio;
  if (c5.rastreio) rastreioDownstream.c5_queda_tensao = c5.rastreio;
  if (parametros.origem_in === "MOD-PROT") {
    // Story MOD-PROT-5: rastreabilidade da decisao de protecao, mesmo padrao
    // de c4_seccionamento (fonte/valor/status_verificacao).
    rastreioDownstream.protecao = {
      fonte: {
        documento: "MOD-PROT",
        edicao: "1.0",
        tabela: parametros.norma_dispositivo ?? undefined,
      },
      valor: parametros.in_a ?? null,
      status_verificacao: parametros.capacidade_interrupcao != null ? "CONFIRMADO" : "VERIFICAR",
    };
  }

  return {
    circuito_id: circuito.id,
    versao_base_normativa: BASE_NORMATIVA_CONDUTORES.versao,
    material: parametros.material,
    isolacao: parametros.isolacao,
    metodo_referencia: parametros.metodo_referencia,
    temperatura_c: parametros.temperatura_c,
    num_condutores_carregados: c1.condutores.num_condutores_carregados,
    fator_neutro_carregado: c1.condutores.fator_neutro_carregado,
    fatores: c1.fatores,
    secao_c1_capacidade_mm2: c1.secao_mm2,
    secao_c2_sobrecarga_mm2: secaoC2Ajustada,
    secao_c6_minima_mm2: c6,
    secao_c5_queda_tensao_mm2: c5.secao_mm2,
    secao_c3_curto_mm2: c3.secao_mm2,
    secao_c4_seccionamento_mm2: c4.secao_mm2,
    secao_fase_mm2: secaoFase || null,
    secao_neutro_mm2: neutro.secao_neutro_mm2,
    secao_pe_mm2: dimensionarPe(secaoFase || null),
    secao_pen_mm2: dimensionarPen(secaoFase || null, parametros),
    iz_corrigida_a: c1.iz_corrigida_a,
    ib_a: circuito.corrente_projeto_a,
    in_a: parametros.in_a ?? null,
    origem_in: parametros.origem_in ?? null,
    i2_a: parametros.i2_a ?? null,
    fonte_i2: parametros.fonte_i2 ?? null,
    norma_dispositivo: parametros.norma_dispositivo ?? null,
    capacidade_interrupcao: parametros.capacidade_interrupcao ?? null,
    tempo_atuacao_s: parametros.tempo_atuacao_s ?? null,
    criterio_decisivo: decisivo,
    ib_menor_igual_in: c2.ib_menor_igual_in,
    in_menor_igual_iz: c2.in_menor_igual_iz,
    i2_menor_igual_145iz: c2.i2_menor_igual_limite,
    status: resolverStatusDimensionamento({ erros: errosFinais, pendencias, criterios }),
    criterios,
    alertas,
    pendencias,
    erros: errosFinais,
    rastreio: {
      c1_iz: {
        fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "36" },
        valor: c1.iz_base_a,
        status_verificacao: c1.erros.length > 0 ? "VERIFICAR" : "CONFIRMADO",
      },
      c6_minima: {
        fonte: { documento: "ABNT NBR 5410", edicao: "2004", tabela: "47" },
        valor: c6,
        status_verificacao: "CONFIRMADO",
      },
      ...rastreioDownstream,
    },
  };
}

export function dimensionarLote(
  circuitos: ReadonlyArray<CircuitoParaDimensionamento>,
  parametros: ParametrosDimensionamento,
) {
  const resultados = circuitos.map((circuito) => dimensionarCircuito(circuito, parametros));
  return { resultados, resumo: resumirResultadosDimensionamento(resultados) };
}
```

## 9. Uso do resultado pelo unifilar

Caminho real: `src/domain/unifilar/montar-unifilar-graph.ts` ? total de linhas: 432

```ts
export function indexarOrigensPorCircuito(
  dependencias: ReadonlyArray<DependenciaAgregado>,
): Map<string, OrigemDependenciaCircuito> {
  const mapa = new Map<string, OrigemDependenciaCircuito>();
  const contagemPorTipo = new Map<string, number>();

  for (const dependencia of dependencias) {
    contagemPorTipo.set(
      dependencia.entrada.tipo,
      (contagemPorTipo.get(dependencia.entrada.tipo) ?? 0) + 1,
    );
  }

  const indicePorTipo = new Map<string, number>();

  for (const dependencia of dependencias) {
    const base = tipoDependenciaLabel(dependencia.entrada.tipo);
    const total = contagemPorTipo.get(dependencia.entrada.tipo) ?? 1;
    const indice = indicePorTipo.get(dependencia.entrada.tipo) ?? 0;
    indicePorTipo.set(dependencia.entrada.tipo, indice + 1);
    const dependenciaLabel = total > 1 ? `${base}-${indice + 1}` : base;
    const resultado = dependencia.resultado;

    if (resultado?.iluminacao.valor.vaTotal) {
      mapa.set(`ILUM-${dependenciaLabel}`, { dependencia, dependenciaLabel });
    }
    if (resultado?.tomadas.valor.vaTotal) {
      mapa.set(`TUG-${dependenciaLabel}`, { dependencia, dependenciaLabel });
    }

    const contagemCarga = new Map<string, number>();
    for (const carga of dependencia.entrada.cargasAdicionais ?? []) {
      if (carga.vaUnitario <= 0) continue;
      const idBase = `ADD-${dependenciaLabel}-${limparNomeCarga(carga.nome) || "Carga"}`;
      const atual = contagemCarga.get(idBase) ?? 0;
      contagemCarga.set(idBase, atual + 1);
      const idCircuito = atual === 0 ? idBase : `${idBase}-${atual + 1}`;
      mapa.set(idCircuito, { dependencia, dependenciaLabel, carga });

      if (carga.quantidade > 1) {
        for (let unidade = 1; unidade <= carga.quantidade; unidade += 1) {
          mapa.set(`${idCircuito}-U${unidade}`, { dependencia, dependenciaLabel, carga });
        }
      }
    }
  }

  return mapa;
}

export function pendenciasDoCircuito(
  origem: OrigemDependenciaCircuito | undefined,
  circuito: Circuito,
): string[] {
  const lista: string[] = [];
  if (circuito.tensao_resolucao && !circuito.tensao_resolucao.confirmada) {
    lista.push(`Tensao a confirmar: ${circuito.tensao_resolucao.rotulo}`);
  }
  if (origem) {
    for (const campo of camposObrigatoriosConformidadePendentes(origem.dependencia.entrada)) {
      lista.push(`${campo.rotulo} pendente (${campo.referencia.item})`);
    }
  }
  return lista;
}
```

As funcoes apenas leem campos nomeados; nao usam spread, Object.assign, JSON.parse ou JSON.stringify sobre ResultadoCalculo.

## 10. Contagem em producao

SEM ACESSO AO BANCO

