/**
 * SIE — Styleguide do Design System (validação visual de interface).
 * Tema escuro g100 conforme observado no produto. Exibe: tokens, gramática de
 * badges (severidade × disciplina), rastreio inline, faixa provisória, estados
 * do unifilar (normal / pendente / selecionado / foco) e a evidência de
 * contraste WCAG. Espelha tokens_sie.css + primitivas_validacao.tsx.
 */

import React, { useState } from "react";

// ---- Tokens (fallbacks g100 de tokens_sie.css) ----
const T = {
  fundo: "#161616", camada: "#262626", camadaHover: "#333333",
  bordaSutil: "#393939", bordaInterativa: "#6f6f6f",
  texto: "#f4f4f4", textoSec: "#c6c6c6", textoInverso: "#161616",
  link: "#78a9ff", interativo: "#0f62fe", foco: "#ffffff", selecao: "#001d6c",
  info: "#4589ff", infoTexto: "#001d6c",
  atencao: "#f1c21b", atencaoTexto: "#161616",
  erro: "#fa4d56", erroTexto: "#161616",
  sucesso: "#42be65",
  verificarFill: "#393939", verificarTexto: "#e0e0e0",
  modificadoFill: "#0043ce", modificadoTexto: "#d0e2ff",
};
const SANS = "'IBM Plex Sans','Segoe UI',sans-serif";
const MONO = "'IBM Plex Mono',Menlo,monospace";

// ---- Primitivas (espelho de primitivas_validacao.tsx) ----
const badge = (bg, fg, extra = {}) => ({
  display: "inline-flex", alignItems: "center", borderRadius: 2,
  padding: "2px 8px", fontFamily: SANS, fontSize: 12, fontWeight: 600,
  background: bg, color: fg, whiteSpace: "nowrap", ...extra,
});
const BadgeSeveridade = ({ nivel }) => {
  const m = { INFO: [T.info, T.infoTexto], "ATENÇÃO": [T.atencao, T.atencaoTexto], ERRO: [T.erro, T.erroTexto] };
  return <span style={badge(m[nivel][0], m[nivel][1])}>{nivel}</span>;
};
const BadgeVerificar = () => (
  <span style={badge(T.verificarFill, T.verificarTexto, { fontFamily: MONO, fontWeight: 400 })}>[VERIFICAR]</span>
);
const BadgeModificado = () => <span style={badge(T.modificadoFill, T.modificadoTexto)}>Modificado</span>;
const BadgeOrigem = ({ origem }) => {
  const cor = origem === "manual" ? T.atencao : T.info;
  return <span style={badge("transparent", cor, { border: `1px solid ${cor}`, padding: "2px 6px" })}>{origem === "manual" ? "M" : "A"}</span>;
};
const Rastreio = ({ children }) => (
  <code style={{ fontFamily: MONO, fontSize: 12, color: T.textoSec }}>{children}</code>
);

// ---- Símbolos IEC (traço claro — tema escuro) ----
const st = (dash, cor = T.texto) => ({ stroke: cor, strokeWidth: 1.5, fill: "none", strokeDasharray: dash ? "5 4" : undefined });
const SymDisjuntor = ({ x, y, dash, cor }) => (
  <g transform={`translate(${x},${y})`}>
    <line x1={-10} y1={0} x2={-4} y2={0} {...st(dash, cor)} />
    <line x1={-4} y1={0} x2={6} y2={-6} {...st(dash, cor)} />
    <line x1={6} y1={0} x2={10} y2={0} {...st(dash, cor)} />
    <polyline points="-4,0 -4,-3 -1,-3" {...st(dash, cor)} />
  </g>
);
const SymCargaTUE = ({ x, y, dash, cor }) => (
  <g transform={`translate(${x},${y})`}>
    <path d="M 0 -7 A 7 7 0 0 1 0 7" {...st(dash, cor)} />
    <line x1={0} y1={0} x2={-9} y2={0} {...st(dash, cor)} />
    <line x1={3} y1={-9.5} x2={3} y2={9.5} {...st(dash, cor)} />
  </g>
);

const Secao = ({ titulo, children }) => (
  <section style={{ background: T.camada, border: `1px solid ${T.bordaSutil}`, padding: 20, marginBottom: 16 }}>
    <div style={{ fontSize: 12, letterSpacing: ".4px", color: T.textoSec, marginBottom: 12, textTransform: "uppercase" }}>{titulo}</div>
    {children}
  </section>
);

const CONTRASTE = [
  ["texto-primário / fundo", "16,45:1", true], ["texto-secundário / fundo", "10,59:1", true],
  ["link / fundo", "7,68:1", true], ["texto branco / botão azul", "5,00:1", true],
  ["badge INFO", "4,51:1", true], ["badge ATENÇÃO", "10,75:1", true],
  ["badge ERRO (texto escuro)", "5,40:1", true], ["badge ERRO texto branco — PROIBIDO", "3,35:1", false],
  ["badge [VERIFICAR]", "8,75:1", true], ["badge Modificado", "5,94:1", true],
  ["traço do diagrama / fundo", "16,45:1", true], ["foco / fundo", "18,10:1", true],
  ["borda interativa / fundo (3:1)", "3,60:1", true],
];

export default function StyleguideSIE() {
  const [sel, setSel] = useState(1);
  const linhas = [
    { id: "ILUM-Sala", va: "520 VA · 127 V", ib: "IB 4,09 A", pend: false, sev: null },
    { id: "ADD-Banheiro-2-Chuveiro-2", va: "4.400 VA · 127 V", ib: "IB 34,65 A", pend: false, sev: null },
    { id: "ADD-Area-Externa-1-LuminariaDeParede", va: "2.400 VA · [VERIFICAR]", ib: "IB [VERIFICAR]", pend: true, sev: "ATENÇÃO" },
  ];
  return (
    <div style={{ background: T.fundo, minHeight: "100vh", color: T.texto, fontFamily: SANS, padding: 20 }}>
      <header style={{ marginBottom: 20 }}>
        <div style={{ fontSize: 12, color: T.textoSec, letterSpacing: ".4px" }}>SIE · DESIGN SYSTEM · TEMA G100</div>
        <h1 style={{ margin: "4px 0 4px", fontSize: 22, fontWeight: 600 }}>Validação de Interface — Camada de Visualização</h1>
        <div style={{ fontSize: 13, color: T.textoSec }}>
          Tokens, primitivas e estados canônicos. Tudo que a Camada B renderiza deve ser componível a partir desta página.
        </div>
      </header>

      <Secao titulo="1 · Paleta de tokens">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(150px,1fr))", gap: 8 }}>
          {[["fundo", T.fundo], ["camada", T.camada], ["texto", T.texto], ["texto-sec", T.textoSec],
            ["interativo", T.interativo], ["link", T.link], ["info", T.info], ["atenção", T.atencao],
            ["erro", T.erro], ["sucesso", T.sucesso], ["verificar-fill", T.verificarFill], ["modificado-fill", T.modificadoFill],
          ].map(([nome, hex]) => (
            <div key={nome} style={{ border: `1px solid ${T.bordaSutil}` }}>
              <div style={{ height: 36, background: hex, borderBottom: `1px solid ${T.bordaSutil}` }} />
              <div style={{ padding: "4px 8px", fontSize: 11 }}>
                <div>--sie-{nome}</div>
                <div style={{ fontFamily: MONO, color: T.textoSec }}>{hex}</div>
              </div>
            </div>
          ))}
        </div>
      </Secao>

      <Secao titulo="2 · Gramática de estado — severidade ≠ disciplina">
        <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
          <div>
            <div style={{ fontSize: 12, color: T.textoSec, marginBottom: 6 }}>Severidade (diagnóstico)</div>
            <div style={{ display: "flex", gap: 8 }}>
              <BadgeSeveridade nivel="INFO" /><BadgeSeveridade nivel="ATENÇÃO" /><BadgeSeveridade nivel="ERRO" />
            </div>
          </div>
          <div>
            <div style={{ fontSize: 12, color: T.textoSec, marginBottom: 6 }}>Disciplina (pendência / trilha)</div>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <BadgeVerificar /><BadgeModificado /><BadgeOrigem origem="automatica" /><BadgeOrigem origem="manual" />
            </div>
          </div>
        </div>
        <div style={{ marginTop: 12, fontSize: 12, color: T.textoSec }}>
          [VERIFICAR] é cinza neutro — pendente de revisão humana, não é alerta. ERRO usa texto escuro
          (branco sobre {T.erro} = 3,35:1, reprovado — DS-04).
        </div>
      </Secao>

      <Secao titulo="3 · Rastreio inline — todo valor calculado">
        <div style={{ display: "grid", gap: 6 }}>
          <div>IB <strong style={{ fontFamily: MONO }}>2,68 A</strong> <BadgeOrigem origem="automatica" /><br />
            <Rastreio>IB = S / V; S=340 VA; V=127 V</Rastreio></div>
          <div>Tomadas <strong style={{ fontFamily: MONO }}>4 pts · 400 VA</strong> <BadgeVerificar /><br />
            <Rastreio>F-03: ⌈P/5⌉ pontos · 100 VA/ponto — NBR 5410 9.5.2</Rastreio></div>
        </div>
      </Secao>

      <Secao titulo="4 · Estados do unifilar (linha de circuito)">
        <div role="note" style={{ fontSize: 12, fontWeight: 600, color: T.erro, borderLeft: `3px solid ${T.erro}`, padding: "4px 8px", marginBottom: 10 }}>
          ÁRVORE PROVISÓRIA — adaptador 1:1 (pré-Divisão de Circuitos)
        </div>
        <svg viewBox="0 0 640 130" width="100%" style={{ display: "block" }}>
          {linhas.map((l, i) => {
            const y = 24 + i * 40;
            const ativo = sel === i;
            const cor = l.pend ? T.atencao : T.texto;
            return (
              <g key={l.id} role="button" tabIndex={0} style={{ cursor: "pointer", outline: "none" }}
                onClick={() => setSel(i)}
                onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && setSel(i)}>
                <rect x={4} y={y - 17} width={632} height={34} rx={4}
                  fill={ativo ? T.selecao : "transparent"}
                  stroke={ativo ? T.foco : "transparent"} strokeWidth={1.5} />
                <line x1={16} y1={y} x2={60} y2={y} {...st(l.pend, cor)} />
                <SymDisjuntor x={72} y={y} dash={l.pend} cor={cor} />
                <line x1={84} y1={y} x2={120} y2={y} {...st(l.pend, cor)} />
                <SymCargaTUE x={134} y={y} dash={l.pend} cor={cor} />
                <text x={156} y={y - 2} fontSize={11.5} fill={T.texto} fontFamily={SANS}>{l.id}</text>
                <text x={156} y={y + 11} fontSize={10} fill={T.textoSec} fontFamily={MONO}>{l.va} · {l.ib}</text>
                {l.sev && (
                  <g transform={`translate(560, ${y - 8})`}>
                    <rect width={64} height={15} rx={2} fill={T.atencao} />
                    <text x={32} y={11} fontSize={9} textAnchor="middle" fontWeight={600} fill={T.atencaoTexto}>{l.sev}</text>
                  </g>
                )}
              </g>
            );
          })}
        </svg>
        <div style={{ fontSize: 12, color: T.textoSec }}>
          Clique/Tab+Enter seleciona (fundo {T.selecao} + anel de foco branco). Pendência INC-04 = traço
          tracejado amarelo + badge ATENÇÃO. Selecionado: <span style={{ fontFamily: MONO, color: T.texto }}>{linhas[sel].id}</span>
        </div>
      </Secao>

      <Secao titulo="5 · Evidência de contraste WCAG 2.1 (RNF-01 / DS-10)">
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, fontFamily: MONO }}>
          <tbody>
            {CONTRASTE.map(([par, razao, ok]) => (
              <tr key={par} style={{ borderBottom: `1px solid ${T.bordaSutil}` }}>
                <td style={{ padding: "5px 8px 5px 0", color: T.texto, fontFamily: SANS }}>{par}</td>
                <td style={{ padding: "5px 8px", color: T.textoSec }}>{razao}</td>
                <td style={{ padding: "5px 0", color: ok ? T.sucesso : T.erro, fontWeight: 700 }}>{ok ? "PASS" : "FAIL"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: 8, fontSize: 12, color: T.textoSec }}>
          Recalculado automaticamente pelo teste test_ds_contraste.py (DS-10) a cada alteração de token.
        </div>
      </Secao>

      <footer style={{ fontSize: 11, color: T.textoSec }}>
        Canônico: tokens_sie.css · primitivas_validacao.tsx · DESIGN-SYSTEM.md (critérios DS-01 a DS-10) — IBM Plex · Carbon g100.
      </footer>
    </div>
  );
}
