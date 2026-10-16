"""EDP São Paulo PT.DT.PDN.00068 v09 catalog, with provenance kept in code.

The category entries below are transcribed from the repository's verified
Tables 001/002 consolidation. Selecting a category by current is an explicit
automation aid only: final EDP eligibility still depends on the distributor.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class StatusFonte(str, Enum):
    VERIFICADO = "VERIFICADO"
    DOCUMENTADO_SEM_FONTE_PRIMARIA = "DOCUMENTADO_SEM_FONTE_PRIMARIA"


@dataclass(frozen=True)
class CategoriaEDP:
    categoria: str
    modalidade: str
    disjuntor_a: Decimal
    medicao: str
    condutor_pvc: str
    condutor_epr_xlpe: str
    aterramento_pvc: str
    aterramento_epr_xlpe: str


# O arquivo do repo e a conferencia local NAO homologam o documento oficial;
# manter dados como candidatos legados, sem sinalizar valores verificados.
FONTE_EDP = {"documento": "PT.DT.PDN.00068", "versao": "09", "vigencia": "A_CONFIRMAR", "referencia": "Anexo A, Tabelas 001 e 002, páginas a conferir na fonte primária autorizada", "url_fonte_edp": "https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf", "publicacao_portal": "2026-04-15", "confirmacao_binaria_pdf": False, "status": StatusFonte.DOCUMENTADO_SEM_FONTE_PRIMARIA.value, "evidencia_repositorio": "Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md", "normative_conformity_verified": False, "release_allowed": False}

# Values transcribed from verified source-data. No fallback values are allowed.
CATALOGO_EDP = (
    CategoriaEDP("U2", "U", Decimal("70"), "direta", "responsabilidade_distribuidora", "responsabilidade_distribuidora", "16 mm²", "16 mm²"),
    CategoriaEDP("D2", "D", Decimal("63"), "direta", "responsabilidade_distribuidora", "responsabilidade_distribuidora", "16 mm²", "16 mm²"),
    CategoriaEDP("D4", "D", Decimal("100"), "direta", "35 mm²", "25 mm²", "16 mm²", "16 mm²"),
    CategoriaEDP("D6", "D", Decimal("150"), "direta", "70 mm²", "50 mm²", "35 mm²", "25 mm²"),
    CategoriaEDP("D7", "D", Decimal("200"), "indireta", "95 mm²", "70 mm²", "50 mm²", "35 mm²"),
    CategoriaEDP("D9", "D", Decimal("300"), "indireta", "185 mm²", "120 mm²", "95 mm²", "70 mm²"),
    CategoriaEDP("D10", "D", Decimal("350"), "indireta", "240 mm²", "185 mm²", "120 mm²", "95 mm²"),
    CategoriaEDP("T2", "T", Decimal("63"), "direta", "responsabilidade_distribuidora", "responsabilidade_distribuidora", "16 mm²", "16 mm²"),
    CategoriaEDP("T4", "T", Decimal("100"), "direta", "35 mm²", "25 mm²", "16 mm²", "16 mm²"),
    CategoriaEDP("T6", "T", Decimal("150"), "direta", "70 mm²", "50 mm²", "35 mm²", "25 mm²"),
    CategoriaEDP("T7", "T", Decimal("200"), "indireta", "95 mm²", "70 mm²", "50 mm²", "35 mm²"),
    CategoriaEDP("T9", "T", Decimal("300"), "indireta", "185 mm²", "120 mm²", "95 mm²", "70 mm²"),
    CategoriaEDP("T10", "T", Decimal("350"), "indireta", "240 mm²", "185 mm²", "120 mm²", "95 mm²"),
)


def enquadrar_edp(modalidade: str, corrente_demanda_a: Decimal, carga_instalada_kw: Decimal, tem_carga_trifasica: bool) -> dict:
    if modalidade not in {"U", "D", "T"}:
        raise ValueError("Modalidade EDP deve ser U, D ou T")
    if not corrente_demanda_a.is_finite() or not carga_instalada_kw.is_finite() or corrente_demanda_a <= 0 or carga_instalada_kw <= 0:
        raise ValueError("Corrente de demanda e carga instalada devem ser positivas")
    alertas = []
    if carga_instalada_kw > Decimal("75"):
        alertas.append({"codigo": "EDP-001", "nivel": "BLOQUEANTE", "mensagem": "Carga instalada acima de 75 kW: consultar a distribuidora para viabilidade em tensão secundária."})
    if modalidade == "T" and not tem_carga_trifasica:
        alertas.append({"codigo": "EDP-002", "nivel": "BLOQUEANTE", "mensagem": "Modalidade T requer carga trifásica declarada."})
    if modalidade in {"U", "D"} and tem_carga_trifasica:
        alertas.append({"codigo": "EDP-003", "nivel": "BLOQUEANTE",
                        "mensagem": "Carga trifasica declarada e modalidade U/D incompativeis para selecao automatica; requer avaliacao do padrao EDP aplicavel."})
    candidatos = sorted((c for c in CATALOGO_EDP if c.modalidade == modalidade and c.disjuntor_a >= corrente_demanda_a), key=lambda c: c.disjuntor_a)
    if not candidatos:
        alertas.append({"codigo": "EDP-004", "nivel": "BLOQUEANTE", "mensagem": "Não há categoria do catálogo para a corrente informada."})
        categoria = None
    else:
        categoria = candidatos[0]
    return {"catalogo": FONTE_EDP, "regra_selecao": {"descricao": "Candidato do catálogo legado ainda não homologado, selecionado por corrente de demanda, filtrado pela modalidade.", "status": StatusFonte.DOCUMENTADO_SEM_FONTE_PRIMARIA.value, "observacao": "A regra automatiza a interpretação do catálogo; a aprovação final depende do padrão vigente e da análise EDP."}, "categoria": None if categoria is None else {"codigo": categoria.categoria, "modalidade": categoria.modalidade, "disjuntor_entrada_a": float(categoria.disjuntor_a), "medicao": categoria.medicao, "condutor_entrada_pvc": categoria.condutor_pvc, "condutor_entrada_epr_xlpe": categoria.condutor_epr_xlpe, "aterramento_pvc": categoria.aterramento_pvc, "aterramento_epr_xlpe": categoria.aterramento_epr_xlpe}, "alertas": alertas, "candidato_para_estudo": not alertas and categoria is not None, "status_engenharia": "PENDENTE" if not alertas else "BLOQUEADO", "liberado_para_padrao_entrada": False}
