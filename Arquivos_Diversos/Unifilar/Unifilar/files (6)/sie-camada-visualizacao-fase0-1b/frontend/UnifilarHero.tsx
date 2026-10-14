/**
 * SIE — Diagrama Unifilar Interativo (Hero) — PRD 4.1.
 *
 * DT-02: layout determinístico em árvore. Linha do circuito i em
 * Y = TOP + i·ROW_H; colunas fixas para DR, disjuntor e carga.
 * Sem physics, sem force-directed. Mesma entrada → mesmo SVG (UF-04/RNF-03):
 * nenhum Math.random(), Date.now() ou dependência de ordem de objeto —
 * a ordem dos circuitos vem pronta do backend (adaptador/Divisão).
 *
 * UF-02: circuito com tensao_v === null renderiza tracejado + badge ATENÇÃO.
 * UF-03: clique/Enter abre memorial via onTrace(circuito) — o registro de
 *        derivação (regra NBR, fórmula, entradas) vem no próprio contrato.
 * UF-06: role="button", aria-label, foco por teclado (Tab + Enter/Espaço).
 * R-04:  payload.provisorio === true exibe a faixa 'Árvore provisória'.
 */

import React from "react";
import {
  SymBarramento,
  SymCarga,
  SymDisjuntor,
  SymDR,
  SymMedidor,
  TipoCarga,
} from "./simbolos_iec";

// --- Contrato (espelho TS do CircuitoCanonico Pydantic) --------------------
export interface DerivacaoRegistro {
  regra_id: string;
  referencia_normativa: string;
  formula: string;
  entradas: Record<string, string | number | null>;
}

export interface CircuitoCanonico {
  id: string;
  tipo: TipoCarga;
  pontos: string[];
  dependencias: string[];
  va_total: number;
  tensao_v: number | null;
  corrente_projeto_a: number | null;
  fases: ("R" | "S" | "T")[];
  requisito_dr: boolean | null;
  grupo_edp: string;
  disjuntor_a: number | null;
  secao_mm2: number | null;
  fonte_linha: string;
  status_linha: "INFO" | "ATENÇÃO" | "ERRO";
  provisorio: boolean;
  derivacao?: DerivacaoRegistro | null;
  pendencias: string[];
}

export interface UnifilarHeroProps {
  circuitos: CircuitoCanonico[];
  provisorio: boolean;
  onTrace?: (c: CircuitoCanonico) => void; // abre o memorial (UF-03)
  larguraRotulo?: number;
}

// --- Constantes de layout (DT-02) — espelham export_dxf.py -----------------
const TOP = 120;
const ROW_H = 36;
const X_BARR = 80;
const X_DR = 180;
const X_DISJ = 260;
const X_CARGA = 360;

// Tokens Carbon (RNF-04)
// Tokens do design system SIE (tokens_sie.css) — tema escuro g100 observado (RNF-04)
const T = {
  texto: "var(--sie-texto, #f4f4f4)",
  textoSec: "var(--sie-texto-sec, #c6c6c6)",
  traco: "var(--sie-diagrama-traco, #f4f4f4)",
  atencao: "var(--sie-atencao-fill, #f1c21b)",
  atencaoTexto: "var(--sie-atencao-fill-texto, #161616)",
  erro: "var(--sie-erro-fill, #fa4d56)",
  erroTexto: "var(--sie-erro-fill-texto, #161616)",
  foco: "var(--sie-foco, #ffffff)",
};

export const UnifilarHero: React.FC<UnifilarHeroProps> = ({
  circuitos,
  provisorio,
  onTrace,
  larguraRotulo = 320,
}) => {
  const altura = TOP + circuitos.length * ROW_H + 40;
  const largura = X_CARGA + 30 + larguraRotulo;
  const yTronco0 = 46;
  const yTroncoFim = TOP + (circuitos.length - 1) * ROW_H;

  return (
    <svg
      viewBox={`0 0 ${largura} ${altura}`}
      width="100%"
      role="img"
      aria-label={`Diagrama unifilar com ${circuitos.length} circuitos`}
      style={{ fontFamily: "'IBM Plex Sans', sans-serif", display: "block" }}
    >
      {/* Faixa 'Árvore provisória' — mitigação R-04 */}
      {provisorio && (
        <text x={8} y={16} fontSize={11} fill={T.erro} fontWeight={600}>
          ÁRVORE PROVISÓRIA — adaptador 1:1 (pré-Divisão de Circuitos)
        </text>
      )}

      {/* Cabeçalho: Rede EDP → Medição → Proteção Geral → Barramento */}
      <text x={8} y={yTronco0 + 4} fontSize={11} fill={T.textoSec}>Rede EDP</text>
      <line x1={62} y1={yTronco0} x2={X_BARR - 40} y2={yTronco0}
        stroke={T.traco} strokeWidth={1.5} />
      <SymMedidor x={X_BARR - 28} y={yTronco0} />
      <line x1={X_BARR - 18} y1={yTronco0} x2={X_BARR - 12} y2={yTronco0}
        stroke={T.traco} strokeWidth={1.5} />
      <SymDisjuntor x={X_BARR} y={yTronco0} />
      <text x={X_BARR} y={yTronco0 - 12} fontSize={9} fill={T.textoSec}
        textAnchor="middle">Geral</text>
      <SymBarramento x={X_BARR + 14} y={yTronco0} largura={26} />

      {/* Tronco vertical */}
      <line x1={X_BARR} y1={yTronco0 + 6} x2={X_BARR} y2={yTroncoFim}
        stroke={T.traco} strokeWidth={1.5} />

      {/* Circuitos — uma linha por índice (DT-02) */}
      {circuitos.map((c, i) => {
        const y = TOP + i * ROW_H;
        const pendente = c.tensao_v === null; // UF-02 / INC-04
        const dash = pendente ? "5 4" : undefined;
        const ib =
          c.corrente_projeto_a !== null
            ? `${c.corrente_projeto_a.toFixed(2).replace(".", ",")} A`
            : "[VERIFICAR]";
        const v = c.tensao_v !== null ? `${c.tensao_v} V` : "[VERIFICAR]";
        const rotulo = `${c.id} — ${c.va_total} VA · ${v} · IB ${ib}`;
        const ariaLabel =
          `Circuito ${c.id}, ${c.va_total} volt-ampère, tensão ${v}, ` +
          `corrente de projeto ${ib}. Ativar para abrir o memorial de cálculo.`;

        return (
          <g
            key={c.id}
            role="button"
            tabIndex={0}
            aria-label={ariaLabel}
            style={{ cursor: "pointer", outline: "none" }}
            onClick={() => onTrace?.(c)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onTrace?.(c); // UF-06: Tab + Enter/Espaço
              }
            }}
            onFocus={(e) =>
              (e.currentTarget.querySelector("rect")!.setAttribute(
                "stroke", T.foco))
            }
            onBlur={(e) =>
              (e.currentTarget.querySelector("rect")!.setAttribute(
                "stroke", "transparent"))
            }
          >
            {/* Área de foco/clique (WCAG: alvo ≥ 24px, foco visível) */}
            <rect x={X_BARR - 4} y={y - ROW_H / 2 + 2}
              width={largura - X_BARR - 4} height={ROW_H - 4}
              fill="transparent" stroke="transparent" strokeWidth={2} rx={4} />

            {/* Derivação: barramento → (DR) → disjuntor → carga */}
            <line x1={X_BARR} y1={y} x2={(c.requisito_dr ? X_DR : X_DISJ) - 10}
              y2={y} stroke={T.traco} strokeWidth={1.5} strokeDasharray={dash} />
            {c.requisito_dr && (
              <>
                <SymDR x={X_DR} y={y} tracejado={pendente} />
                <line x1={X_DR + 10} y1={y} x2={X_DISJ - 10} y2={y}
                  stroke={T.traco} strokeWidth={1.5} strokeDasharray={dash} />
              </>
            )}
            <SymDisjuntor x={X_DISJ} y={y} tracejado={pendente} />
            <line x1={X_DISJ + 10} y1={y} x2={X_CARGA - 12} y2={y}
              stroke={T.traco} strokeWidth={1.5} strokeDasharray={dash} />
            <SymCarga x={X_CARGA} y={y} tipo={c.tipo} tracejado={pendente} />

            {/* Rótulo técnico */}
            <text x={X_CARGA + 20} y={y + 3.5} fontSize={10.5} fill={T.texto}>
              {rotulo}
            </text>

            {/* Badge de severidade (UF-02 / TE-03) */}
            {c.status_linha !== "INFO" && (
              <g transform={`translate(${X_CARGA + 20}, ${y + 8})`}>
                <rect width={64} height={13} rx={2}
                  fill={c.status_linha === "ERRO" ? T.erro : T.atencao} />
                <text x={32} y={9.5} fontSize={8.5} textAnchor="middle"
                  fill={c.status_linha === "ERRO" ? T.erroTexto : T.atencaoTexto}
                  fontWeight={600}>
                  {c.status_linha}
                </text>
              </g>
            )}
          </g>
        );
      })}
    </svg>
  );
};

export default UnifilarHero;
