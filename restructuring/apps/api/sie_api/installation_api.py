"""F02 model boundary; stateless, no mutations to a project or production database."""
from uuid import UUID

from fastapi import APIRouter, HTTPException
from .installation_contracts import LegacyAnalysisRequest, InvalidationRequest, ReferenceRequest, ValidityResponse

from .domain.installation import Installation
from .analysis_contracts import AnaliseCircuito
from .installation_service import (InstallationSnapshot, CalculationRecord, RevisionReference,
    algorithm_identity, create_snapshot, analyze_legacy, calculation_status, require_same_revision)

router = APIRouter(prefix='/api/v1/modelo', tags=['Canonical installation model'])


@router.post('/validar')
def validate_installation(installation: Installation):
    return {'schema_version': 'SIE_MODEL_RESULT_V1', 'valid': True,
            'project_id': str(installation.project.id), 'revision': installation.project.revision,
            'normative_conformity_verified': False}


@router.post('/snapshots', response_model=InstallationSnapshot)
def snapshot_installation(installation: Installation):
    return create_snapshot(installation)


@router.post('/ensaiar-legado', response_model=CalculationRecord)
def analyze_installation(request: LegacyAnalysisRequest):
    try:
        return analyze_legacy(request.snapshot, request.circuit_id, request.parameters, request.rule_version)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={'code': 'LEGACY_MODEL_INCOMPATIBLE',
                                                   'message': str(exc)}) from exc


@router.post('/invalidacao', response_model=ValidityResponse)
def invalidate_installation(request: InvalidationRequest):
    return calculation_status(request.record, request.snapshot, algorithm_identity(),
                              request.rule_version, request.input_sha256)


@router.post('/referencias/validar')
def validate_reference(request: ReferenceRequest):
    try:
        require_same_revision(request.snapshot, request.reference)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={'code': 'REVISION_REFERENCE_MISMATCH',
                                                   'message': str(exc)}) from exc
    return {'valid': True, 'normative_conformity_verified': False}
