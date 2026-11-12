"""Synthetic-only GREENFIELD aggregate for E01--E11."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from .v201_c_greenfield_e01_e05 import GreenfieldInputError, evaluate_e01_e05
from .v201_c_greenfield_e06_e11 import (
    evaluate_e06_protection, evaluate_e07_dr_dps, evaluate_e08_grounding,
    evaluate_e09_utility_catalog, evaluate_e11_integrity,
)

router = APIRouter(prefix="/api/v1/greenfield", tags=["SIE2 GREENFIELD synthetic"])


class GreenfieldEvidenceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    e01_e05: dict | None = None
    e06: dict | None = None
    e07: dict | None = None
    e08: dict | None = None
    e09: dict | None = None
    e11_payload: dict | None = None
    e11_expected_sha256: str | None = None
    e11_catalog_version: str | None = None


def _blocked(code: str, reason: str) -> dict:
    return {"check": code, "status": "BLOCKED", "synthetic_only": True,
            "normative_approval": False, "reason": reason}


@router.post("/e01-e11/evaluate")
def evaluate_e01_e11_synthetic(body: GreenfieldEvidenceIn):
    """Evaluate supplied synthetic evidence without normative approval."""
    checks: dict[str, dict] = {}
    evaluators = {
        "E01_E05": (body.e01_e05, evaluate_e01_e05),
        "E06": (body.e06, evaluate_e06_protection),
        "E07": (body.e07, evaluate_e07_dr_dps),
        "E08": (body.e08, evaluate_e08_grounding),
        "E09": (body.e09, evaluate_e09_utility_catalog),
    }
    for code, (payload, evaluator) in evaluators.items():
        if payload is None:
            checks[code] = _blocked(code, "input_not_provided")
            continue
        try:
            checks[code] = evaluator(payload)
        except (GreenfieldInputError, ValueError, TypeError) as exc:
            checks[code] = _blocked(code, str(exc) or "invalid_or_incomplete_input")
    e11 = (body.e11_payload, body.e11_expected_sha256, body.e11_catalog_version)
    if any(value is None for value in e11):
        checks["E11"] = _blocked("E11", "input_not_provided")
    else:
        try:
            checks["E11"] = evaluate_e11_integrity(*e11)
        except (ValueError, TypeError) as exc:
            checks["E11"] = _blocked("E11", str(exc) or "invalid_or_incomplete_input")
    return {"schema_version": 1, "scope": "GREENFIELD_SYNTHETIC_ONLY",
            "status": "PENDING_EVIDENCE", "liberado_para_uso_normativo": False,
            "release_allowed": False, "checks": checks,
            "deferred": {"E10": "DEFERRED_OPTIONAL_LEGACY_IMPORT_ONLY"}}
