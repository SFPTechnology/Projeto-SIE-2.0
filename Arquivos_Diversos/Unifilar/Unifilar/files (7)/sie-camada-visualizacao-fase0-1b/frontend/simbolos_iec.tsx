/**
 * SIE — Biblioteca de símbolos IEC 60617 (PRD 4.1, DT-01/DT-03).
 *
 * Definição canônica única: cada componente React espelha o bloco DXF
 * correspondente em backend/export_dxf.py (mesma geometria, escala 1:1 em
 * unidades de usuário SVG = mm do DXF). Alterou aqui? Altere lá.
 *
 * Sem lib genérica (GoJS/React Flow/mxGraph) — DT-01.
 * Cores via design system SIE (tokens_sie.css — RNF-04): prop `stroke`,
 * default var(--sie-diagrama-traco) — tema escuro g100 observado no produto.
 */

import React from "react";

export interface SimboloProps {
  x: number;
  y: number;
  stroke?: string;
  tracejado?: boolean; // INC-04: elemento com pendência de tensão (UF-02)
}

const S = "var(--sie-diagrama-traco, var(--cds-icon-primary, #f4f4f4))";
const dash = (t?: boolean) => (t ? "4 3" : undefined);

const base = (p: SimboloProps) => ({
  stroke: p.stroke ?? S,
  strokeWidth: 1.5,
  fill: "none" as const,
  strokeDasharray: dash(p.tracejado),
});

/** Medidor de energia (kWh) — medição EDP. Bloco DXF: BLK_MEDIDOR */
export const SymMedidor: React.FC<SimboloProps> = (p) => (
  <g transform={`translate(${p.x},${p.y})`}>
    <circle r={10} {...base(p)} />
    <text textAnchor="middle" dominantBaseline="central" fontSize={6.5}
      fill={p.stroke ?? S} style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>
      kWh
    </text>
  </g>
);

/** Disjuntor termomagnético — IEC 60617. Bloco DXF: BLK_DISJUNTOR */
export const SymDisjuntor: React.FC<SimboloProps> = (p) => (
  <g transform={`translate(${p.x},${p.y})`}>
    <line x1={-10} y1={0} x2={-4} y2={0} {...base(p)} />
    <line x1={-4} y1={0} x2={6} y2={-6} {...base(p)} />
    <line x1={6} y1={0} x2={10} y2={0} {...base(p)} />
    <polyline points="-4,0 -4,-3 -1,-3" {...base(p)} />
  </g>
);

/** Dispositivo DR (residual) — disjuntor + toroide. Bloco DXF: BLK_DR */
export const SymDR: React.FC<SimboloProps> = (p) => (
  <g transform={`translate(${p.x},${p.y})`}>
    <line x1={-10} y1={0} x2={-4} y2={0} {...base(p)} />
    <line x1={-4} y1={0} x2={6} y2={-6} {...base(p)} />
    <line x1={6} y1={0} x2={10} y2={0} {...base(p)} />
    <ellipse cx={1} cy={5} rx={6} ry={2.7} {...base(p)} />
  </g>
);

/** Barramento trifásico R/S/T. Bloco DXF: BLK_BARR */
export const SymBarramento: React.FC<SimboloProps & { largura?: number }> = (p) => (
  <g transform={`translate(${p.x},${p.y})`}>
    {[-4, 0, 4].map((dy, i) => (
      <line key={i} x1={0} y1={dy} x2={p.largura ?? 20} y2={dy} {...base(p)} />
    ))}
    <text x={(p.largura ?? 20) / 2} y={-9} textAnchor="middle" fontSize={5.5}
      fill={p.stroke ?? S} style={{ fontFamily: "'IBM Plex Mono', monospace" }}>
      R S T
    </text>
  </g>
);

/** Motor / bomba. Bloco DXF: BLK_MOTOR */
export const SymMotor: React.FC<SimboloProps> = (p) => (
  <g transform={`translate(${p.x},${p.y})`}>
    <circle r={8} {...base(p)} />
    <text textAnchor="middle" dominantBaseline="central" fontSize={8}
      fill={p.stroke ?? S} style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>
      M
    </text>
  </g>
);

export type TipoCarga = "iluminacao" | "tug" | "tue" | "outra";

/**
 * Carga terminal — variante por tipo.
 * ILU: círculo com X (BLK_ILU) · TUG: semicírculo com haste (BLK_TUG)
 * TUE/outra: TUG + traço duplo (BLK_TUE)
 */
export const SymCarga: React.FC<SimboloProps & { tipo: TipoCarga }> = (p) => {
  const b = base(p);
  const d = 7 * 0.7071;
  if (p.tipo === "iluminacao")
    return (
      <g transform={`translate(${p.x},${p.y})`}>
        <circle r={7} {...b} />
        <line x1={-d} y1={-d} x2={d} y2={d} {...b} />
        <line x1={-d} y1={d} x2={d} y2={-d} {...b} />
      </g>
    );
  return (
    <g transform={`translate(${p.x},${p.y})`}>
      <path d="M 0 -7 A 7 7 0 0 1 0 7" {...b} />
      <line x1={0} y1={0} x2={-9} y2={0} {...b} />
      {p.tipo !== "tug" && <line x1={3} y1={-9.5} x2={3} y2={9.5} {...b} />}
    </g>
  );
};
