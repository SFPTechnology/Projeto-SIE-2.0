"""
DS-10 — Verificação automatizada de contraste WCAG 2.1 dos tokens do design
system (RNF-01). Lê os fallbacks hex de tokens_sie.css e valida cada par
texto/fundo declarado no DESIGN-SYSTEM.md §3.

Falha aqui = alguém alterou um token sem recalcular contraste.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CSS = Path(__file__).resolve().parents[1] / "frontend" / "tokens_sie.css"


def _luminancia(hexcor: str) -> float:
    r, g, b = (int(hexcor[i : i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def razao(a: str, b: str) -> float:
    la, lb = _luminancia(a), _luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _tokens() -> dict[str, str]:
    texto = CSS.read_text(encoding="utf-8")
    # captura o último hex de cada declaração (fallback final do var encadeado),
    # mantendo apenas a PRIMEIRA ocorrência do token — as redeclarações do bloco
    # @media print (tema claro de impressão) não participam da validação g100.
    tokens: dict[str, str] = {}
    for nome, valor in re.findall(r"(--sie-[\w-]+):\s*([^;]+);", texto):
        hexes = re.findall(r"#[0-9a-fA-F]{6}", valor)
        if hexes:
            tokens.setdefault(nome, hexes[-1].lower())
    return tokens


# (token_texto, token_fundo, alvo)
PARES = [
    ("--sie-texto", "--sie-fundo", 4.5),
    ("--sie-texto-sec", "--sie-fundo", 4.5),
    ("--sie-texto", "--sie-camada", 4.5),
    ("--sie-texto-sec", "--sie-camada", 4.5),
    ("--sie-link", "--sie-fundo", 4.5),
    ("--sie-interativo-texto", "--sie-interativo", 4.5),
    ("--sie-info", "--sie-fundo", 4.5),
    ("--sie-info-fill-texto", "--sie-info-fill", 4.5),
    ("--sie-atencao-fill-texto", "--sie-atencao-fill", 4.5),
    ("--sie-erro-fill-texto", "--sie-erro-fill", 4.5),
    ("--sie-atencao", "--sie-fundo", 4.5),
    ("--sie-erro", "--sie-fundo", 4.5),
    ("--sie-verificar-texto", "--sie-verificar-fill", 4.5),
    ("--sie-modificado-texto", "--sie-modificado-fill", 4.5),
    ("--sie-diagrama-traco", "--sie-fundo", 4.5),
    ("--sie-foco", "--sie-fundo", 3.0),
    ("--sie-borda-interativa", "--sie-fundo", 3.0),
    ("--sie-borda-interativa", "--sie-camada", 3.0),
]


def test_ds10_contraste_tokens():
    tokens = _tokens()
    faltantes = [t for par in PARES for t in par[:2] if t not in tokens]
    assert not faltantes, f"Tokens sem hex resolvível no CSS: {faltantes}"
    reprovados = []
    for fg, bg, alvo in PARES:
        r = razao(tokens[fg], tokens[bg])
        if r < alvo:
            reprovados.append(f"{fg} sobre {bg}: {r:.2f}:1 < {alvo}:1")
    assert not reprovados, "Contraste WCAG reprovado:\n" + "\n".join(reprovados)


def test_ds04_erro_nunca_texto_branco():
    """Guarda específica do achado da auditoria: branco sobre --sie-erro-fill = 3,35:1."""
    tokens = _tokens()
    assert tokens["--sie-erro-fill-texto"] != "#ffffff"
    assert razao("#ffffff", tokens["--sie-erro-fill"]) < 4.5  # documenta o porquê da proibição
