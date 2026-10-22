"""Consultative distributor screening for F09.

This module deliberately separates a legacy category candidate from distributor
eligibility or approval. A missing/unsupported standard never falls back to EDP.
"""
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .edp_context import ContextoEDP, enquadrar_com_contexto


class DistributorAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)

    distributor_id: str = Field(min_length=2, max_length=80)
    modality: Literal["U", "D", "T"]
    demand_current_a: float = Field(gt=0)
    installed_load_kw: float = Field(gt=0)
    has_three_phase_load: bool
    context: ContextoEDP

    @field_validator("distributor_id")
    @classmethod
    def nonblank_distributor_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("distributor_id cannot be blank")
        return value.strip().upper()


_EDP_V09 = {
    "distributor_id": "EDP_SP",
    "document_code": "PT.DT.PDN.00068",
    "edition": "09",
    "territory": {"uf": "SP", "network": "AEREA_SECUNDARIA"},
    "valid_from": "2026-04-14",
    "valid_until": None,
    "validity_note": "Encerramento condicionado; verificar publicação vigente na data do projeto.",
    "source_url": "https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf",
    "official_publication_observed_on": "2026-10-22",
    "source_status": "OFFICIAL_PORTAL_LISTED; CRITERIA_PENDING_INDEPENDENT_REVIEW",
    "criteria_registry": "sie_api/data/edp_context_v1.json",
    "criteria_references": ["5.3.1/5.3.2", "Anexo A Tabelas 001/002"],
}

_MANDATORY_GATES = (
    ("territory_confirmed", "Confirmar município e área de concessão da unidade consumidora."),
    ("standard_current", "Conferir edição e vigência do padrão na data do projeto."),
    ("supply_conditions", "Verificar modalidade, tensão, fases e condições de fornecimento."),
    ("demand_and_metering", "Conferir demanda, carga instalada e modalidade de medição."),
    ("entry_design", "Conferir ramal, condutores e limites de conexão do padrão aplicável."),
    ("protection_coordination", "Revisar proteção e coordenação com o estudo elétrico atual."),
    ("distributor_process", "Submeter o caso ao processo aplicável da distribuidora."),
)


def diagnosticar_distribuidora(payload: DistributorAssessment | dict) -> dict:
    """Return a source-scoped candidate and explicit unresolved gates.

    The API input is evidence of project conditions, not proof that those
    conditions or the distributor's current rules were independently verified.
    Consequently ``connection_release`` is permanently false in this engine.
    """
    request = DistributorAssessment.model_validate(payload)
    context = request.context.model_dump(mode="json")
    if request.distributor_id != _EDP_V09["distributor_id"]:
        return {
            "status": "PADRAO_NAO_CADASTRADO",
            "distributor_id": request.distributor_id,
            "candidate": None,
            "alerts": [{
                "code": "DISTRIBUTOR_STANDARD_UNAVAILABLE",
                "severity": "BLOCKING",
                "message": "Não há padrão cadastrado e verificado para esta distribuidora; nenhum dado EDP foi reutilizado.",
            }],
            "pending_gates": ["Cadastrar fonte, escopo territorial, edição, vigência e critérios verificáveis."],
            "connection_release": False,
        }

    result = enquadrar_com_contexto(
        request.modality,
        Decimal(str(request.demand_current_a)),
        Decimal(str(request.installed_load_kw)),
        request.has_three_phase_load,
        context,
    )
    if date.fromisoformat(context["data_referencia"]) > date.fromisoformat(_EDP_V09["official_publication_observed_on"]):
        result["alertas"].append({
            "codigo": "DISTRIBUTOR_SOURCE_REFRESH_REQUIRED",
            "nivel": "BLOQUEANTE",
            "mensagem": "A data do projeto é posterior à última consulta registrada ao portal oficial; atualizar a edição antes de sugerir categoria.",
        })
        result["categoria"] = None
        result["candidato_para_estudo"] = False
        result["status_engenharia"] = "BLOQUEADO"
    result["candidate"] = result.pop("categoria")
    result["distributor_standard"] = dict(_EDP_V09)
    result["pending_gates"] = [
        {"id": gate_id, "status": "PENDING", "message": message}
        for gate_id, message in _MANDATORY_GATES
    ]
    result["status"] = "CANDIDATE_FOR_REVIEW" if result["candidate"] else "BLOCKED"
    result["diagnostic_scope"] = "EDP São Paulo / rede aérea secundária / triagem parcial V09"
    result["connection_release"] = False
    return result


def catalogo_distribuidoras() -> list[dict]:
    """Expose only entries with explicit identity and applicability metadata."""
    item = dict(_EDP_V09)
    item["territory"] = dict(_EDP_V09["territory"])
    return [item]
