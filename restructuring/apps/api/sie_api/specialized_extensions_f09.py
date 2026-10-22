"""Optional, isolated extension contracts. No specialized engine is enabled here."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ExtensionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    extension_id: Literal["SPDA", "PHOTOVOLTAIC", "EV_CHARGING", "SPECIAL_ENVIRONMENT"]
    applicable: bool
    context: dict = Field(default_factory=dict)


_EXTENSIONS = {
    "SPDA": {
        "standard": "ABNT NBR 5419 (Parts 1–4, corrected 2026 editions listed in ABNT Catalog)",
        "scope": "SPDA isolado do núcleo de instalações de baixa tensão; análise de risco, medidas, equipotencialização e coordenação com DPS.",
        "engine_status": "NOT_CONFIGURED",
    },
    "PHOTOVOLTAIC": {
        "standard": None,
        "scope": "Geração fotovoltaica, inversores, proteção e requisitos de conexão; selecionar normas e regras vigentes para o caso.",
        "engine_status": "NOT_CONFIGURED",
    },
    "EV_CHARGING": {
        "standard": "ABNT NBR 17019:2022 (catalog metadata only; applicability still case-specific)",
        "scope": "Pontos de recarga, circuitos, proteções, potência e controle de demanda; requer recorte de uso e fontes aplicáveis.",
        "engine_status": "NOT_CONFIGURED",
    },
    "SPECIAL_ENVIRONMENT": {
        "standard": None,
        "scope": "Ambientes hospitalares, industriais e locais especiais; exige classificação do ambiente e seleção normativa específica.",
        "engine_status": "NOT_CONFIGURED",
    },
}


def avaliar_extensao(payload: ExtensionRequest | dict) -> dict:
    request = ExtensionRequest.model_validate(payload)
    metadata = _EXTENSIONS[request.extension_id]
    if not request.applicable:
        return {
            "extension_id": request.extension_id,
            "status": "NOT_APPLICABLE_BY_DECLARATION",
            "engine_status": metadata["engine_status"],
            "scope": metadata["scope"],
            "warnings": ["A não aplicabilidade foi declarada pelo usuário e não foi verificada pelo sistema."],
            "release": False,
        }
    return {
        "extension_id": request.extension_id,
        "status": "PENDING_SPECIALIST_ENGINE_AND_SOURCES",
        "engine_status": metadata["engine_status"],
        "standard": metadata["standard"],
        "scope": metadata["scope"],
        "warnings": ["Extensão condicional sem motor normativo habilitado; encaminhar para análise especializada."],
        "release": False,
    }


def catalogo_extensoes() -> list[dict]:
    return [
        {"extension_id": key, **value, "optional": True, "release": False}
        for key, value in _EXTENSIONS.items()
    ]
