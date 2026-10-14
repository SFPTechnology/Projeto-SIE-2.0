/**
 * SIE — Design System · Primitivas de validação de interface.
 *
 * Componentes transversais que padronizam COMO o estado normativo aparece na
 * tela (Seções 8 e 10 da referência). A Camada B usa exclusivamente estas
 * primitivas para severidade, pendência, origem e rastreio — nunca markup
 * ad hoc. Cores exclusivamente via tokens de tokens_sie.css (nunca hex aqui).
 *
 * Regras de uso (validáveis — ver DESIGN-SYSTEM.md):
 * - Severidade (INFO/ATENÇÃO/ERRO) ≠ disciplina ([VERIFICAR]/Modificado):
 *   sistemas visuais distintos, nunca misturar.
 * - Texto do badge ERRO é sempre escuro (branco reprova AA: 3,35:1).
 * - Todo valor calculado exibido vem acompanhado de RastreioInline.
 */

import React from "react";

export type Severidade = "INFO" | "ATENÇÃO" | "ERRO";

const estiloBase: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  gap: "0.25rem",
  borderRadius: 2,
  padding: "0.125rem 0.5rem",
  fontFamily: "var(--sie-fonte)",
  fontSize: "var(--sie-tam-rotulo)",
  fontWeight: 600,
  lineHeight: 1.4,
  whiteSpace: "nowrap",
};

/** Badge de severidade — INFO azul, ATENÇÃO amarelo, ERRO vermelho (Seção 8). */
export const BadgeSeveridade: React.FC<{ nivel: Severidade }> = ({ nivel }) => {
  const mapa: Record<Severidade, { bg: string; fg: string }> = {
    INFO: { bg: "var(--sie-info-fill)", fg: "var(--sie-info-fill-texto)" },
    "ATENÇÃO": { bg: "var(--sie-atencao-fill)", fg: "var(--sie-atencao-fill-texto)" },
    ERRO: { bg: "var(--sie-erro-fill)", fg: "var(--sie-erro-fill-texto)" },
  };
  const { bg, fg } = mapa[nivel];
  return (
    <span role="status" style={{ ...estiloBase, background: bg, color: fg }}>
      {nivel}
    </span>
  );
};

/** Badge [VERIFICAR] — pendência de confirmação humana. Cinza neutro: NÃO é severidade. */
export const BadgeVerificar: React.FC<{ titulo?: string }> = ({ titulo }) => (
  <span
    role="status"
    title={titulo ?? "Campo pendente de confirmação humana"}
    style={{
      ...estiloBase,
      background: "var(--sie-verificar-fill)",
      color: "var(--sie-verificar-texto)",
      fontFamily: "var(--sie-fonte-mono)",
      fontWeight: 400,
    }}
  >
    [VERIFICAR]
  </span>
);

/** Badge "Modificado" — parâmetro EDP editado pelo projetista (tabelas 001/002). */
export const BadgeModificado: React.FC = () => (
  <span
    role="status"
    style={{ ...estiloBase, background: "var(--sie-modificado-fill)", color: "var(--sie-modificado-texto)" }}
  >
    Modificado
  </span>
);

/** Badge de origem do dado: A = Automático · M = Manual (sempre visível — Seção 10). */
export const BadgeOrigem: React.FC<{ origem: "automatica" | "manual" }> = ({ origem }) => (
  <span
    role="status"
    aria-label={origem === "manual" ? "Origem: manual" : "Origem: automática"}
    style={{
      ...estiloBase,
      padding: "0.125rem 0.375rem",
      background: "transparent",
      border: `1px solid ${origem === "manual" ? "var(--sie-origem-manual)" : "var(--sie-origem-auto)"}`,
      color: origem === "manual" ? "var(--sie-origem-manual)" : "var(--sie-origem-auto)",
    }}
  >
    {origem === "manual" ? "M" : "A"}
  </span>
);

/**
 * Rastreio inline — fórmula com substituição literal de valores, padrão
 * observado em toda a aplicação (ex.: "IB = S / V; S=340 VA; V=127 V").
 * Recebe a string pronta do backend/derivação; NUNCA monta cálculo aqui (RG-02).
 */
export const RastreioInline: React.FC<{ formula: string; entradas?: string }> = ({
  formula,
  entradas,
}) => (
  <code
    style={{
      fontFamily: "var(--sie-fonte-mono)",
      fontSize: "var(--sie-tam-rotulo)",
      color: "var(--sie-texto-sec)",
      background: "transparent",
    }}
  >
    {formula}
    {entradas ? `; ${entradas}` : ""}
  </code>
);

/** Faixa "Árvore provisória" — obrigatória em todo artefato pré-Divisão (R-04). */
export const FaixaProvisoria: React.FC<{ visivel: boolean }> = ({ visivel }) =>
  !visivel ? null : (
    <div
      role="note"
      style={{
        fontFamily: "var(--sie-fonte)",
        fontSize: "var(--sie-tam-rotulo)",
        fontWeight: 600,
        color: "var(--sie-erro)",
        borderLeft: "3px solid var(--sie-erro)",
        padding: "0.25rem 0.5rem",
        marginBottom: "var(--sie-esp-03)",
      }}
    >
      ÁRVORE PROVISÓRIA — adaptador 1:1 (pré-Divisão de Circuitos)
    </div>
  );

/** Bloco de pendências [VERIFICAR] de um circuito (memorial). */
export const ListaPendencias: React.FC<{ pendencias: string[] }> = ({ pendencias }) =>
  pendencias.length === 0 ? null : (
    <div
      role="note"
      style={{
        borderLeft: "3px solid var(--sie-atencao)",
        background: "var(--sie-camada)",
        padding: "var(--sie-esp-03)",
        fontFamily: "var(--sie-fonte)",
        fontSize: "var(--sie-tam-rotulo)",
        color: "var(--sie-texto)",
        display: "grid",
        gap: "0.25rem",
      }}
    >
      {pendencias.map((p) => (
        <span key={p}>{p}</span>
      ))}
    </div>
  );
