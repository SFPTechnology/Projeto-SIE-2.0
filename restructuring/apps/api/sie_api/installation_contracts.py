"""Versioned F02 request DTOs shared by CLI and HTTP; no framework or database."""
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from .installation_service import InstallationSnapshot, CalculationRecord, RevisionReference
from .analysis_contracts import AnaliseCircuito


class LegacyAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    snapshot: InstallationSnapshot
    circuit_id: UUID
    parameters: AnaliseCircuito
    rule_version: str = Field(min_length=1, max_length=200)


class InvalidationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    record: CalculationRecord
    snapshot: InstallationSnapshot
    rule_version: str = Field(min_length=1, max_length=200)
    input_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


class ReferenceRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    snapshot: InstallationSnapshot
    reference: RevisionReference



class ValidityResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: Literal['VALID', 'PENDING', 'INVALID', 'STALE']
    reason: str

