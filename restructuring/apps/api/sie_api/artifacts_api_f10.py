"""Authenticated local F10 service; paths and bytes remain server controlled."""
import copy
from hashlib import sha256
import json
import os
from dataclasses import replace
from pathlib import Path
from uuid import UUID, uuid4
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field
from .storage_api import _storage
from .storage import ConflitoRevisao
from .artifact_registry_f10 import ArtifactRegistryF10, _safe_relative_destination
from .persisted_source_f10 import resolve_persisted_source, publish_from_repository, verify_against_repository

router = APIRouter(prefix='/api/v1/local/projetos/{project_id}/f10', tags=['F10 local'])

class Generation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    revision: int = Field(ge=1)
    calculation_run_id: UUID
    template_version: str = Field(default='F10_FULL_V1', min_length=1, max_length=100)

class Geometry(Generation):
    floor_plan: dict


def _root():
    root = os.environ.get('SIE_F10_ARTIFACT_ROOT')
    if not root:
        raise HTTPException(503, 'Diretório de artefatos local não configurado')
    return Path(root).resolve()


def _error(exc):
    return HTTPException(409 if isinstance(exc, ConflitoRevisao) else 422,
                         'Operação F10 recusada: dados ausentes, incompatíveis ou obsoletos')


def _artifact(repo, pid, aid):
    row = ArtifactRegistryF10(repo).get(str(aid))
    if row is None or row['project_id'] != str(pid):
        raise HTTPException(404, 'Artefato não encontrado')
    root, relative = _safe_relative_destination(_root(), Path(row['artifact_root']) / row['destination_relative'])
    return row, root / relative

@router.get('/geometry')
def get_geometry(project_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    saved = repo.carregar(str(project_id))
    if saved is None:
        raise HTTPException(404, 'Projeto não encontrado')
    return {'revision': saved['revisao'], 'floor_plan': saved['dados'].get('floor_plan_f10')}

@router.put('/geometry')
def save_geometry(project_id: UUID, body: Geometry, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        if len(json.dumps(body.floor_plan, allow_nan=False).encode()) > 3_000_000:
            raise ValueError('size')
        snapshot, contract = resolve_persisted_source(repo, str(project_id), body.revision,
            str(body.calculation_run_id), body.template_version)
        saved = repo.carregar_revisao(str(project_id), body.revision)
        current = repo.carregar(str(project_id))
        if current is None or current['revisao'] != body.revision:
            raise ConflitoRevisao('revision')
        from .floorplan_f10 import import_floor_plan
        next_revision = body.revision + 1
        snapshot = copy.deepcopy(snapshot)
        snapshot['revision_id'] = str(next_revision)
        plan = copy.deepcopy(body.floor_plan)
        plan['revision_id'] = str(next_revision)
        previous = saved['dados'].get('floor_plan_f10') or {}
        if plan.get('geometry_revision') != previous.get('geometry_revision', 0) + 1:
            raise ConflitoRevisao('geometry revision')
        snapshot['floor_plan'] = plan
        normalized = import_floor_plan(plan, snapshot, replace(contract, revision_id=str(next_revision)))
        data = copy.deepcopy(saved['dados'])
        data['floor_plan_f10'] = normalized
        revision = repo.salvar(str(project_id), saved['nome'], data, body.revision)
        return {'revision': revision, 'floor_plan': normalized, 'motor_execution_required': True}
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

@router.post('/execute')
def execute(project_id: UUID, body: Generation, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        saved = repo.carregar_revisao(str(project_id), body.revision)
        mapping = saved['dados'].get('calculation_runs_f10') if saved else None
        runs = list(mapping.values()) if isinstance(mapping, dict) and mapping else [str(body.calculation_run_id)]
        evidence = [repo.executar_calculo_f10(str(project_id), body.revision, str(run)) for run in runs]
        return {'state': 'EXECUTED', 'executions': [{'run_id': run, 'evidence_sha256': item['hash_sha256']} for run, item in zip(runs, evidence)]}
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

@router.post('/generate')
def generate(project_id: UUID, body: Generation, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        result = publish_from_repository(repo, str(project_id), body.revision,
            str(body.calculation_run_id), body.template_version, _root() / str(uuid4()), full=True)
        return result
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

@router.get('/artifacts')
def history(project_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    return {'artifacts': [{k: row[k] for k in ('artifact_id','revision_id','state','created_at','calculation_run_id')}
        for row in ArtifactRegistryF10(repo).history(str(project_id))]}

@router.get('/artifacts/{artifact_id}')
def inspect(project_id: UUID, artifact_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        row, path = _artifact(repo, project_id, artifact_id)
        result = verify_against_repository(repo, path)
        manifest_bytes = (path / 'manifest.json').read_bytes() if result.get('integrity') == 'VERIFIED' else None
        if manifest_bytes is not None and sha256(manifest_bytes).hexdigest() != row['manifest_sha256']:
            raise HTTPException(409, 'Manifesto alterado durante consulta')
        manifest = json.loads(manifest_bytes) if manifest_bytes is not None else None
        return {'verification': result, 'manifest': manifest, 'state': row['state']}
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

@router.get('/artifacts/{artifact_id}/files/{name}')
def download(project_id: UUID, artifact_id: UUID, name: str, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        row, path = _artifact(repo, project_id, artifact_id)
        result = verify_against_repository(repo, path)
        if result.get('integrity') != 'VERIFIED':
            raise HTTPException(409, 'Artefato não íntegro; download bloqueado')
        manifest_bytes = (path / 'manifest.json').read_bytes()
        if sha256(manifest_bytes).hexdigest() != row['manifest_sha256']:
            raise HTTPException(409, 'Manifesto alterado durante consulta')
        manifest = json.loads(manifest_bytes)
        if name not in manifest['files_sha256'] and name != 'manifest.json':
            raise HTTPException(404, 'Arquivo não encontrado')
        file = path / name
        if file.is_symlink() or file.parent != path:
            raise HTTPException(409, 'Caminho inválido')
        content = file.read_bytes()
        expected = row['manifest_sha256'] if name == 'manifest.json' else manifest['files_sha256'][name]
        if sha256(content).hexdigest() != expected:
            raise HTTPException(409, 'Arquivo alterado durante leitura')
        # Download as attachment; browser preview uses isolated blob sandbox.
        return Response(content, media_type='application/octet-stream', headers={
            'Content-Disposition': f'attachment; filename="{name}"',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': "default-src 'none'; sandbox"})
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

class AssetImport(BaseModel):
    model_config = ConfigDict(extra='forbid')
    content_base64: str = Field(max_length=3_000_000)
    source_ref: str = Field(min_length=1, max_length=500)
    authorization_reference: str = Field(min_length=1, max_length=500)

@router.post('/import')
def import_asset(project_id: UUID, body: AssetImport, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    if repo.carregar(str(project_id)) is None:
        raise HTTPException(404, 'Projeto não encontrado')
    try:
        import base64
        from .floorplan_f10 import import_svg_asset
        return import_svg_asset(base64.b64decode(body.content_base64, validate=True), body.source_ref, body.authorization_reference)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc

@router.post('/model')
def model(project_id: UUID, body: Generation, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        snapshot, _ = resolve_persisted_source(repo, str(project_id), body.revision,
            str(body.calculation_run_id), body.template_version)
        saved = repo.carregar_revisao(str(project_id), body.revision)
        return {'elements': snapshot['elements'], 'revision': body.revision, 'calculation_runs': saved['dados'].get('calculation_runs_f10', {})}
    except (ValueError, OSError, TypeError, KeyError) as exc:
        raise _error(exc) from exc
