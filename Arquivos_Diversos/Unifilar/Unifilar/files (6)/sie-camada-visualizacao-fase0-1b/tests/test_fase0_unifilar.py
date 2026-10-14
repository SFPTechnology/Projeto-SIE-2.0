"""
Testes de aceite — Fase 0 (contrato + adaptador) e exportação DXF.

T1 — INC-01: VA direto preservado; nenhum campo sofre divisão por FP.
T2 — INC-04: tensão ausente => None + corrente None + ATENÇÃO + [VERIFICAR].
T3 — INC-07: seção fora da série IEC 60228 é rejeitada; valor da série passa.
T4 — UF-04/RNF-03: mesma entrada => JSON byte-identical e ordenação estável.
T5 — INC-03: zona molhada não classificada => requisito_dr=None + pendência.
T6 — UF-05: DXF R2010 gerado com layers SIE_* e blocos BLK_*.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

import ezdxf
import pytest
from pydantic import ValidationError

from backend.adaptador_1x1 import (
    FONTE_TENSAO_SAIDA_A,
    adaptar_ponto,
    adaptar_projeto,
    mapear_fase_abc_para_rst,
)
from backend.contrato_circuito import (
    CircuitoCanonico,
    Fase,
    GrupoEDP,
    PontoCarga,
    StatusLinha,
    TipoCircuito,
)
from backend.export_dxf import exportar_unifilar_dxf


def _ponto(**kw) -> PontoCarga:
    base = dict(
        id="P1",
        descricao="Chuveiro",
        tipo=TipoCircuito.TUE,
        dependencia_id="Banheiro-1",
        va=5500,
        tensao_v=220,
        corrente_ib_a=25.0,
        fases=(Fase.R, Fase.S),
        grupo_edp=GrupoEDP.B,
        zona_molhada=True,
    )
    base.update(kw)
    return PontoCarga(**base)


def test_t1_inc01_va_direto():
    c = adaptar_ponto(_ponto(va=4400, corrente_ib_a=20.0))
    assert c.va_total == 4400                     # VA direto, intocado
    assert c.corrente_projeto_a == 20.0           # copiado do IB, não recalculado
    assert "VA direto" in c.derivacao.formula     # disciplina INC-01 rastreável
    assert c.id == "P1"                           # CONF-02: id real do banco preservado


def test_t2_inc04_tensao_pendente():
    c = adaptar_ponto(_ponto(tensao_v=None, corrente_ib_a=None))
    assert c.tensao_v is None                     # jamais 127V implícito
    assert c.corrente_projeto_a is None
    assert c.status_linha is StatusLinha.ATENCAO
    assert any("INC-04" in p for p in c.pendencias)


def test_t3_inc07_secao_iec60228():
    kw = dict(
        id="C1", tipo=TipoCircuito.TUE, pontos=("P1",), dependencias=("D1",),
        va_total=5500, tensao_v=220, grupo_edp=GrupoEDP.B, fonte_linha="IB:P1",
    )
    with pytest.raises(ValidationError):
        CircuitoCanonico(**kw, secao_mm2=185.5)   # fora da série — rejeitado
    ok = CircuitoCanonico(**kw, secao_mm2=185.0)  # série IEC 60228 — aceito
    assert ok.secao_mm2 == 185.0


def test_t4_determinismo():
    pontos = [
        _ponto(id="P3", tipo=TipoCircuito.TUG, dependencia_id="Sala", va=600,
               tensao_v=127, corrente_ib_a=4.72, fases=(Fase.T,), zona_molhada=False),
        _ponto(id="P1"),
        _ponto(id="P2", tipo=TipoCircuito.ILUMINACAO, dependencia_id="Sala", va=160,
               tensao_v=127, corrente_ib_a=1.26, fases=(Fase.R,),
               grupo_edp=GrupoEDP.A, zona_molhada=False),
    ]
    a = adaptar_projeto(list(pontos))
    b = adaptar_projeto(list(reversed(pontos)))
    dump = lambda cs: json.dumps([c.model_dump(mode="json") for c in cs], sort_keys=True)
    assert dump(a) == dump(b)                     # ordem de entrada não altera saída
    assert [c.tipo for c in a][0] is TipoCircuito.ILUMINACAO  # ILU < TUG < TUE


def test_t5_inc03_dr_pendente():
    c = adaptar_ponto(_ponto(zona_molhada=None))
    assert c.requisito_dr is None
    assert any("INC-03" in p for p in c.pendencias)
    assert c.status_linha is StatusLinha.ATENCAO


def test_t6_dxf_uf05(tmp_path):
    circuitos = adaptar_projeto([_ponto(id=f"P{i}", va=1000 + i) for i in range(5)])
    caminho = str(tmp_path / "unifilar.dxf")
    exportar_unifilar_dxf(circuitos, caminho, "proj-1")
    doc = ezdxf.readfile(caminho)
    assert doc.dxfversion == "AC1024"             # R2010 (mitigação R-05)
    nomes_layers = {l.dxf.name for l in doc.layers}
    assert {"SIE_PROTECAO", "SIE_CARGAS", "SIE_CONDUTORES"} <= nomes_layers
    nomes_blocos = {b.name for b in doc.blocks if b.name.startswith("BLK_")}
    assert {"BLK_MEDIDOR", "BLK_DISJUNTOR", "BLK_DR", "BLK_TUE", "BLK_BARR"} <= nomes_blocos
    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) >= 5 + 3                  # cargas + cabeçalho


# --- Testes das decisões do operador (Anexo A, 08/07/2026) -----------------

def test_t7_conf01_mapeamento_fases():
    """CONF-01: convenção oficial R/S/T; tela legada A/B/C convertida no loader."""
    assert mapear_fase_abc_para_rst("A") is Fase.R
    assert mapear_fase_abc_para_rst("b") is Fase.S
    assert mapear_fase_abc_para_rst("C") is Fase.T
    assert mapear_fase_abc_para_rst("R") is Fase.R  # idempotente
    with pytest.raises(ValueError):
        mapear_fase_abc_para_rst("X")


def test_t8_conf02_id_real_preservado():
    """CONF-02: adaptador não inventa ids — usa o id do banco (ex.: ADD-*)."""
    c = adaptar_ponto(_ponto(id="ADD-Banheiro-2-Chuveiro-2", va=4400,
                             tensao_v=127, corrente_ib_a=34.65, fases=(Fase.R,)))
    assert c.id == "ADD-Banheiro-2-Chuveiro-2"
    assert c.pontos == ("ADD-Banheiro-2-Chuveiro-2",)


def test_t9_conf03_tensao_saida_a():
    """CONF-03: ILU/TUG com 127 V via Saída A => INFO + fonte rastreável (não é fallback)."""
    c = adaptar_ponto(_ponto(id="ILUM-Sala", tipo=TipoCircuito.ILUMINACAO,
                             dependencia_id="Sala", va=520, tensao_v=127,
                             corrente_ib_a=4.09, fases=(Fase.T,),
                             grupo_edp=GrupoEDP.A, zona_molhada=False,
                             tensao_resolvida_por_contrato=True))
    assert c.status_linha is StatusLinha.INFO
    assert FONTE_TENSAO_SAIDA_A in c.fonte_linha
    assert c.tensao_v == 127


def test_t10_conf03_tue_nunca_por_contrato():
    """CONF-03/INC-04: TUE com tensão 'resolvida por contrato' é rejeitada pelo adaptador."""
    with pytest.raises(ValueError, match="INC-04"):
        adaptar_ponto(_ponto(tensao_resolvida_por_contrato=True))
