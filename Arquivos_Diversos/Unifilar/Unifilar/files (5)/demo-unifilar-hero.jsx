/**
 * SIE — Demo do Diagrama Unifilar Interativo (Hero) — PRD 4.1.
 * Dados de exemplo no perfil do proj-1 (44 circuitos via adaptador 1:1).
 * Valida: UF-01 (44 sem sobreposição), UF-02 (tracejado + ATENÇÃO p/ INC-04),
 * UF-03 (click-to-trace → memorial), UF-06 (Tab + Enter), R-04 (faixa provisória).
 */

import React, { useMemo, useState } from "react";

// ---- Tokens Carbon g10 (RNF-04) ----
const T = {
  fundo: "#ffffff", camada: "#f4f4f4", borda: "#e0e0e0",
  texto: "#161616", textoSec: "#525252", traco: "#161616",
  interativo: "#0f62fe", atencao: "#f1c21b", erro: "#da1e28", ok: "#24a148",
};
const FONT = "'IBM Plex Sans','Segoe UI',sans-serif";
const MONO = "'IBM Plex Mono',monospace";

// ---- Símbolos IEC 60617 (espelho de simbolos_iec.tsx / BLK_* do DXF) ----
const st = (dash) => ({ stroke: T.traco, strokeWidth: 1.5, fill: "none", strokeDasharray: dash ? "5 4" : undefined });
const SymMedidor = ({ x, y }) => (
  <g transform={`translate(${x},${y})`}>
    <circle r={10} {...st()} />
    <text textAnchor="middle" dominantBaseline="central" fontSize={6.5} fill={T.texto} style={{ fontFamily: FONT }}>kWh</text>
  </g>
);
const SymDisjuntor = ({ x, y, dash }) => (
  <g transform={`translate(${x},${y})`}>
    <line x1={-10} y1={0} x2={-4} y2={0} {...st(dash)} />
    <line x1={-4} y1={0} x2={6} y2={-6} {...st(dash)} />
    <line x1={6} y1={0} x2={10} y2={0} {...st(dash)} />
    <polyline points="-4,0 -4,-3 -1,-3" {...st(dash)} />
  </g>
);
const SymDR = ({ x, y, dash }) => (
  <g transform={`translate(${x},${y})`}>
    <line x1={-10} y1={0} x2={-4} y2={0} {...st(dash)} />
    <line x1={-4} y1={0} x2={6} y2={-6} {...st(dash)} />
    <line x1={6} y1={0} x2={10} y2={0} {...st(dash)} />
    <ellipse cx={1} cy={5} rx={6} ry={2.7} {...st(dash)} />
  </g>
);
const SymBarr = ({ x, y }) => (
  <g transform={`translate(${x},${y})`}>
    {[-4, 0, 4].map((dy, i) => <line key={i} x1={0} y1={dy} x2={26} y2={dy} {...st()} />)}
    <text x={13} y={-9} textAnchor="middle" fontSize={5.5} fill={T.texto} style={{ fontFamily: MONO }}>R S T</text>
  </g>
);
const SymCarga = ({ x, y, tipo, dash }) => {
  const b = st(dash); const d = 7 * 0.7071;
  if (tipo === "iluminacao") return (
    <g transform={`translate(${x},${y})`}>
      <circle r={7} {...b} />
      <line x1={-d} y1={-d} x2={d} y2={d} {...b} /><line x1={-d} y1={d} x2={d} y2={-d} {...b} />
    </g>
  );
  return (
    <g transform={`translate(${x},${y})`}>
      <path d="M 0 -7 A 7 7 0 0 1 0 7" {...b} />
      <line x1={0} y1={0} x2={-9} y2={0} {...b} />
      {tipo !== "tug" && <line x1={3} y1={-9.5} x2={3} y2={9.5} {...b} />}
    </g>
  );
};

// ---- Dados de exemplo (perfil proj-1: 44 circuitos, adaptador 1:1) ----
function gerarCircuitos() {
  const cs = [];
  const mk = (id, tipo, dep, va, v, fases, grupo, dr, pend = []) => {
    const ib = v ? +(va / v).toFixed(2) : null;
    const status = pend.length ? "ATENÇÃO" : "INFO";
    cs.push({
      id, tipo, dependencias: [dep], va_total: va, tensao_v: v,
      corrente_projeto_a: ib, fases, requisito_dr: dr, grupo_edp: grupo,
      disjuntor_a: null, secao_mm2: null, fonte_linha: `IB:${id}`,
      status_linha: status, provisorio: true, pendencias: pend,
      derivacao: {
        regra_id: "SIE-IB-01",
        referencia_normativa: "ABNT NBR 5410:2004 §6.2.7",
        formula: "IB = S / V (S em VA direto — INC-01)",
        entradas: { S_va: va, V_v: v, IB_a: ib },
      },
    });
  };
  const deps = ["Dormitorio-1", "Dormitorio-2", "Dormitorio-3", "Suite", "Sala", "Copa", "Cozinha", "Corredor", "Banheiro-1", "Banheiro-2", "Lavabo", "AreaServico", "AreaGourmet", "Varanda", "Garagem", "AreaExterna"];
  const fase3 = [["R"], ["S"], ["T"]];
  // Iluminação (16)
  deps.forEach((d, i) => mk(`ILUM-${d}`, "iluminacao", d, 100 + (i % 3) * 60, 127, fase3[i % 3], "A", false));
  // TUG (16)
  deps.forEach((d, i) => {
    const molhada = /Banheiro|Cozinha|AreaServico|Lavabo|AreaExterna|AreaGourmet/.test(d);
    mk(`TUG-${d}`, "tug", d, molhada ? 600 : 300 + (i % 2) * 300, 127, fase3[(i + 1) % 3], "C", molhada);
  });
  // TUE (12) — incluindo casos de auditoria
  mk("TUE-Banheiro-1-Chuveiro", "tue", "Banheiro-1", 5500, 220, ["R", "S"], "B", true);
  mk("TUE-Banheiro-2-Chuveiro", "tue", "Banheiro-2", 5500, 220, ["S", "T"], "B", true);
  mk("TUE-Cozinha-FornoEletrico", "tue", "Cozinha", 4500, 220, ["R", "T"], "D", false); // Grupo D, não E (INC-02)
  mk("TUE-Cozinha-TorneiraEletrica", "tue", "Cozinha", 3200, 220, ["R", "S"], "B", true);
  mk("TUE-AreaServico-Lavadora", "tue", "AreaServico", 1000, 127, ["T"], "F", true);
  mk("TUE-Suite-ArCondicionado", "tue", "Suite", 1400, 220, ["S", "T"], "G", false);
  mk("TUE-Dormitorio-1-ArCondicionado", "tue", "Dormitorio-1", 1400, 220, ["R", "S"], "G", false);
  mk("TUE-Sala-ArCondicionado", "tue", "Sala", 2100, 220, ["R", "T"], "G", false);
  mk("TUE-AreaExterna-BombaPiscina", "tue", "AreaExterna", 1500, 220, ["S", "T"], "H", true);
  mk("TUE-Garagem-PortaoMotor", "tue", "Garagem", 400, 127, ["R"], "H", false);
  // INC-04: TUE > 600 VA SEM tensão declarada → nunca 127V
  mk("TUE-AreaGourmet-Churrasqueira", "tue", "AreaGourmet", 2400, null, [], "B", true,
    ["[VERIFICAR] Tensão não declarada — IB indisponível (INC-04)"]);
  // INC-03: zona molhada não classificada → DR pendente
  mk("TUE-Copa-MicroOndas", "tue", "Copa", 1200, 127, ["T"], "F", null,
    ["[VERIFICAR] Zona molhada não classificada — requisito DR pendente (INC-03)"]);
  return cs; // 16 + 16 + 12 = 44
}

// ---- Layout determinístico (DT-02) ----
const TOP = 120, ROW_H = 36, X_BARR = 80, X_DR = 180, X_DISJ = 260, X_CARGA = 360;

export default function DemoUnifilarHero() {
  const circuitos = useMemo(gerarCircuitos, []);
  const [sel, setSel] = useState(null);
  const altura = TOP + circuitos.length * ROW_H + 40;
  const largura = 760;
  const y0 = 46, yFim = TOP + (circuitos.length - 1) * ROW_H;
  const pendentes = circuitos.filter((c) => c.status_linha !== "INFO").length;

  return (
    <div style={{ fontFamily: FONT, background: T.camada, minHeight: "100vh", color: T.texto }}>
      <header style={{ background: T.fundo, borderBottom: `1px solid ${T.borda}`, padding: "14px 20px" }}>
        <div style={{ fontSize: 12, color: T.textoSec, letterSpacing: ".4px" }}>SIE · Camada de Visualização · Camada B</div>
        <h1 style={{ margin: "2px 0 6px", fontSize: 19, fontWeight: 600 }}>Diagrama Unifilar Interativo — proj-1</h1>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <span style={{ background: T.erro, color: "#fff", fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 2 }}>
            ÁRVORE PROVISÓRIA — adaptador 1:1
          </span>
          <span style={{ fontSize: 12, color: T.textoSec }}>
            {circuitos.length} circuitos · {pendentes} com ATENÇÃO · IEC 60617 · NBR 5410:2004
          </span>
        </div>
      </header>

      <div style={{ display: "flex", gap: 16, padding: 16, alignItems: "flex-start" }}>
        {/* Unifilar */}
        <div style={{ flex: "1 1 60%", background: T.fundo, border: `1px solid ${T.borda}`, overflow: "auto", maxHeight: "78vh" }}>
          <svg viewBox={`0 0 ${largura} ${altura}`} width={largura} role="img"
            aria-label={`Diagrama unifilar com ${circuitos.length} circuitos`} style={{ display: "block" }}>
            <text x={8} y={y0 + 4} fontSize={11} fill={T.textoSec}>Rede EDP</text>
            <line x1={62} y1={y0} x2={X_BARR - 40} y2={y0} {...st()} />
            <SymMedidor x={X_BARR - 28} y={y0} />
            <line x1={X_BARR - 18} y1={y0} x2={X_BARR - 12} y2={y0} {...st()} />
            <SymDisjuntor x={X_BARR} y={y0} />
            <text x={X_BARR} y={y0 - 12} fontSize={9} fill={T.textoSec} textAnchor="middle">Geral</text>
            <SymBarr x={X_BARR + 14} y={y0} />
            <line x1={X_BARR} y1={y0 + 6} x2={X_BARR} y2={yFim} {...st()} />

            {circuitos.map((c, i) => {
              const y = TOP + i * ROW_H;
              const pend = c.tensao_v === null;
              const ib = c.corrente_projeto_a !== null ? `${c.corrente_projeto_a.toFixed(2).replace(".", ",")} A` : "[VERIFICAR]";
              const v = c.tensao_v !== null ? `${c.tensao_v} V` : "[VERIFICAR]";
              const ativo = sel && sel.id === c.id;
              return (
                <g key={c.id} role="button" tabIndex={0}
                  aria-label={`Circuito ${c.id}. Ativar para abrir o memorial.`}
                  style={{ cursor: "pointer", outline: "none" }}
                  onClick={() => setSel(c)}
                  onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setSel(c); } }}>
                  <rect x={X_BARR - 4} y={y - ROW_H / 2 + 2} width={largura - X_BARR - 2} height={ROW_H - 4}
                    fill={ativo ? "#edf5ff" : "transparent"} stroke={ativo ? T.interativo : "transparent"} strokeWidth={2} rx={4} />
                  <line x1={X_BARR} y1={y} x2={(c.requisito_dr ? X_DR : X_DISJ) - 10} y2={y} {...st(pend)} />
                  {c.requisito_dr && (<>
                    <SymDR x={X_DR} y={y} dash={pend} />
                    <line x1={X_DR + 10} y1={y} x2={X_DISJ - 10} y2={y} {...st(pend)} />
                  </>)}
                  <SymDisjuntor x={X_DISJ} y={y} dash={pend} />
                  <line x1={X_DISJ + 10} y1={y} x2={X_CARGA - 12} y2={y} {...st(pend)} />
                  <SymCarga x={X_CARGA} y={y} tipo={c.tipo} dash={pend} />
                  <text x={X_CARGA + 20} y={y - 1} fontSize={10.5} fill={T.texto}>{c.id}</text>
                  <text x={X_CARGA + 20} y={y + 11} fontSize={9} fill={T.textoSec} style={{ fontFamily: MONO }}>
                    {c.va_total} VA · {v} · IB {ib}
                  </text>
                  {c.status_linha !== "INFO" && (
                    <g transform={`translate(${largura - 78}, ${y - 8})`}>
                      <rect width={62} height={14} rx={2} fill={c.status_linha === "ERRO" ? T.erro : T.atencao} />
                      <text x={31} y={10} fontSize={8.5} textAnchor="middle" fontWeight={600}
                        fill={c.status_linha === "ERRO" ? "#fff" : "#161616"}>{c.status_linha}</text>
                    </g>
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        {/* Memorial — Click-to-Trace (UF-03) */}
        <aside style={{ flex: "1 1 40%", position: "sticky", top: 16, background: T.fundo, border: `1px solid ${T.borda}`, padding: 16, minHeight: 300 }}>
          <div style={{ fontSize: 12, color: T.textoSec, letterSpacing: ".4px", marginBottom: 6 }}>MEMORIAL DE CÁLCULO</div>
          {!sel ? (
            <p style={{ fontSize: 13, color: T.textoSec, lineHeight: 1.5 }}>
              Selecione um circuito no diagrama (clique ou Tab + Enter) para abrir o registro de derivação:
              regra NBR aplicada, fórmula, entradas e rastreabilidade fonte_linha / status_linha.
            </p>
          ) : (
            <div style={{ fontSize: 13 }}>
              <h2 style={{ margin: "0 0 4px", fontSize: 16, fontWeight: 600 }}>{sel.id}</h2>
              <div style={{ color: T.textoSec, marginBottom: 12 }}>
                {sel.dependencias.join(", ")} · Grupo EDP {sel.grupo_edp} · tipo {sel.tipo}
                {sel.fases.length ? ` · fases ${sel.fases.join("+")}` : ""}
              </div>
              <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: MONO, fontSize: 12 }}>
                <tbody>
                  {[
                    ["Regra", sel.derivacao.regra_id],
                    ["Referência", sel.derivacao.referencia_normativa],
                    ["Fórmula", sel.derivacao.formula],
                    ["S (VA)", sel.derivacao.entradas.S_va],
                    ["V (V)", sel.derivacao.entradas.V_v ?? "[VERIFICAR]"],
                    ["IB (A)", sel.derivacao.entradas.IB_a ?? "[VERIFICAR]"],
                    ["Disjuntor", sel.disjuntor_a ?? "[VERIFICAR] — aguarda P1"],
                    ["Seção", sel.secao_mm2 ? `${sel.secao_mm2} mm²` : "[VERIFICAR] — aguarda P1"],
                    ["DR", sel.requisito_dr === null ? "[VERIFICAR] (INC-03)" : sel.requisito_dr ? "Sim" : "Não"],
                    ["fonte_linha", sel.fonte_linha],
                    ["status_linha", sel.status_linha],
                  ].map(([k, val]) => (
                    <tr key={k} style={{ borderBottom: `1px solid ${T.borda}` }}>
                      <td style={{ padding: "6px 8px 6px 0", color: T.textoSec, whiteSpace: "nowrap", verticalAlign: "top" }}>{k}</td>
                      <td style={{ padding: "6px 0", wordBreak: "break-word" }}>{String(val)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {sel.pendencias.length > 0 && (
                <div style={{ marginTop: 12, background: "#fdf6dd", borderLeft: `3px solid ${T.atencao}`, padding: "8px 10px" }}>
                  {sel.pendencias.map((p) => <div key={p} style={{ fontSize: 12 }}>{p}</div>)}
                </div>
              )}
              <div style={{ marginTop: 12, fontSize: 11, color: T.textoSec }}>
                Valores lidos do contrato canônico — a visualização é projeção, não recálculo (INC-01).
              </div>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
