"""F10 W1 persisted source adapter tests; built for the real SIE API package.

These cases use an immutable-revision repository double for deterministic input
faults and a real filesystem for package publication. Full application
integration tests still need to run against the project's SQLite repository.
"""
from copy import deepcopy
import json
from types import SimpleNamespace as NS
from uuid import uuid4

import pytest

from sie_api.persisted_source_f10 import (
    resolve_persisted_source, publish_from_repository, verify_against_repository,
)
from sie_api.representation_f10 import ArtifactError


class FakeRun(NS):
    def model_dump(self, mode="json"):
        assert mode == "json"
        return {"id": str(self.id), "circuit_id": str(self.circuit_id),
                "project_revision": self.project_revision, "state": self.state,
                "input_sha256": "a" * 64, "output_sha256": self.output_sha256,
                "algorithm_version": self.algorithm_version, "rule_version": self.rule_version}


class VersionedRepo:
    """Imitates only the contract of already-hash-verified carregar_revisao."""
    def __init__(self, pid, data, database_path):
        from sie_api.storage import RepositorioProjetos
        self._storage = RepositorioProjetos(database_path)
        self._storage.salvar(pid, "Projeto de fixture", data, 0)
        self.pid = pid
        self.history = {1: {"id": pid, "revisao": 1, "hash_sha256": "a"*64,
                            "dados": data, "historico_recuperavel": True}}
        self.current = 1

    def carregar_revisao(self, pid, revision):
        return deepcopy(self.history.get(revision)) if pid == self.pid else None

    def consultar_calculo_f10(self, pid, revision, rid):
        if getattr(self, "execution_missing", False):
            return None
        run = self.documents[revision].installation.calculation_runs[0]
        return {"project_id": pid, "revision": revision, "run_id": rid,
                "source_sha256": self.history[revision]["hash_sha256"],
                "hash_sha256": "e" * 64,
                "record": {"project_id": pid, "revision": run.project_revision,
                           "circuit_id": str(run.circuit_id),
                           "input_sha256": run.input_sha256,
                           "result_sha256": run.output_sha256,
                           "algorithm_version": run.algorithm_version,
                           "rule_version": run.rule_version}}

    def carregar(self, pid):
        return {"id": pid, "revisao": self.current} if pid == self.pid else None

    def verificar_revisao_atual(self, pid, revision):
        if pid == self.pid and self.current == revision:
            return {"status": "CURRENT"}
        return {"status": "SOURCE_INVALID", "reason": "projection diverges"}

    def _conectar(self):
        return self._storage._conectar()


def make_doc():
    pid, board_id, circ_id, load_id, run_id, segment_id, device_id, calc_id = [uuid4() for _ in range(8)]
    cable = NS(id=run_id, circuit_id=circ_id, segment_ids=[segment_id])
    segment = NS(id=segment_id, length=NS(value="5.5"))
    document = NS(
        installation=NS(
            project=NS(id=pid, revision=1),
            boards=[NS(id=board_id)],
            circuits=[NS(id=circ_id, kind="TERMINAL", board_id=board_id,
                         load_ids=[load_id], phases=1, device_id=device_id)],
            loads=[NS(id=load_id, apparent_power=NS(value="500", unit="VA"))],
            cable_runs=[cable], segments=[segment],
            calculation_runs=[FakeRun(id=calc_id, circuit_id=circ_id,
                  project_revision=1, state="VALID", input_sha256="a"*64, output_sha256="b"*64,
                  rule_version="declared-rule-1", algorithm_version="unverified-algorithm-1")],
        ),
        segment_details={segment_id: NS(route_status="DOCUMENTED", origin=NS(
            reference="declared-document:1", method="DOCUMENTED"))},
    )
    data = {"installation_snapshot": {"project_id": str(pid), "revision": 1,
                                    "snapshot_sha256": "c"*64}}
    return document, str(pid), str(calc_id), data


@pytest.fixture
def sources(monkeypatch, tmp_path):
    from sie_api import topology
    doc, pid, calc_id, data = make_doc()
    repo = VersionedRepo(pid, data, tmp_path / "fake-authority.sqlite")
    repo.documents = {1: doc}
    repo.history[1]["dados"]["test_document_revision"] = 1
    monkeypatch.setattr(topology, "load_document",
                        lambda d: repo.documents[d["test_document_revision"]])
    monkeypatch.setattr(topology, "topology_hash", lambda document: "d" * 64)
    return repo, doc, pid, calc_id


def test_identity_canonical_revision_and_declared_provenance(sources):
    repo, doc, pid, rid = sources
    snap, contract = resolve_persisted_source(repo, pid, 1, rid, "template-v1")
    assert snap["project_id"] == pid
    assert snap["revision_id"] == "1"
    assert snap["calculation_run_id"] == rid
    assert contract.rule_version == "declared-rule-1"
    assert snap["source_evidence_f10"]["historical_revision_sha256"] == "a" * 64
    assert snap["source_evidence_f10"]["source_kind"].endswith("SERVER_EXECUTED_LEGACY_MOTOR")
    assert snap["circuits"][0]["load_va"] == 500.0
    assert snap["segments"][0]["length_m"] == 5.5
    assert snap["source_evidence_f10"]["normative_conformity_verified"] is False


def test_unsupported_multi_circuit_fails_closed(sources):
    repo, doc, pid, rid = sources
    doc.installation.circuits.append(deepcopy(doc.installation.circuits[0]))
    with pytest.raises(ArtifactError, match="multiple circuits"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_other_project_and_unknown_revision_fail(sources):
    repo, doc, pid, rid = sources
    with pytest.raises(ArtifactError, match="historical revision absent"):
        resolve_persisted_source(repo, str(uuid4()), 1, rid, "t")
    with pytest.raises(ArtifactError, match="historical revision absent"):
        resolve_persisted_source(repo, pid, 2, rid, "t")
    with pytest.raises(ArtifactError, match="revision must be"):
        resolve_persisted_source(repo, pid, True, rid, "t")
    with pytest.raises(ArtifactError, match="UUID required"):
        resolve_persisted_source(repo, pid, 1, "CALC-FAKE", "t")


def test_unknown_run_and_wrong_circuit_fail(sources):
    repo, doc, pid, rid = sources
    with pytest.raises(ArtifactError, match="calculation run not present"):
        resolve_persisted_source(repo, pid, 1, str(uuid4()), "t")
    doc.installation.calculation_runs[0].circuit_id = uuid4()
    with pytest.raises(ArtifactError, match="another circuit"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_stale_run_fails(sources):
    repo, doc, pid, rid = sources
    doc.installation.calculation_runs[0].state = "STALE"
    with pytest.raises(ArtifactError, match="invalid, stale"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_unknown_load_power_rejected_without_inference(sources):
    repo, doc, pid, rid = sources
    doc.installation.loads[0].apparent_power = None
    with pytest.raises(ArtifactError, match="apparent_power"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_f10_float_precision_cannot_silently_round(sources):
    repo, doc, pid, rid = sources
    doc.installation.loads[0].apparent_power.value = "0.123456789012345678901"
    with pytest.raises(ArtifactError, match="losslessly"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_declared_route_is_not_mislabeled_estimated(sources):
    repo, doc, pid, rid = sources
    detail = next(iter(doc.segment_details.values()))
    detail.route_status = "DECLARED"
    with pytest.raises(ArtifactError, match="measured/documented"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_historical_revision_cannot_be_rewritten_by_source_adapter(sources):
    repo, doc, pid, rid = sources
    before = deepcopy(repo.history)
    resolve_persisted_source(repo, pid, 1, rid, "t")
    assert repo.history == before


def test_invalid_source_revision_fails(sources):
    repo, doc, pid, rid = sources
    doc.installation.project.revision = 10
    with pytest.raises(ArtifactError, match="installation revision incompatible"):
        resolve_persisted_source(repo, pid, 1, rid, "t")


def test_publish_and_validate_authoritative_current_source(tmp_path, sources):
    repo, doc, pid, rid = sources
    output = tmp_path / 'generated'
    manifest = publish_from_repository(repo, pid, 1, rid, 'template-v1', output)
    assert manifest['dependencies']['project_id'] == pid
    assert (output / 'snapshot.json').is_file()
    result = verify_against_repository(repo, output)
    assert result['integrity'] == 'VERIFIED'
    assert result['currentness'] == 'CURRENT'


def test_revision_change_without_dependency_change_is_historical(tmp_path, sources):
    repo, doc, pid, rid = sources
    output = tmp_path / 'generated'
    publish_from_repository(repo, pid, 1, rid, 'template-v1', output)
    repo.current = 2
    repo.history[2] = {**deepcopy(repo.history[1]), 'revisao': 2}
    repo.history[2]['dados']['test_document_revision'] = 2
    repo.documents[2] = deepcopy(doc)
    result = verify_against_repository(repo, output)
    assert result['currentness'] == 'HISTORICAL'


def test_new_revision_with_invalidated_run_is_stale(tmp_path, sources):
    repo, doc, pid, rid = sources
    output = tmp_path / 'generated'
    publish_from_repository(repo, pid, 1, rid, 'template-v1', output)
    repo.current = 2
    repo.history[2] = {**deepcopy(repo.history[1]), 'revisao': 2}
    repo.history[2]['dados']['test_document_revision'] = 2
    repo.documents[2] = deepcopy(doc)
    repo.documents[2].installation.calculation_runs[0].state = 'STALE'
    result = verify_against_repository(repo, output)
    assert result['currentness'] == 'STALE'


def test_saved_source_changes_invalidates_derived_artifact(tmp_path, sources):
    repo, doc, pid, rid = sources
    output = tmp_path / 'generated'
    publish_from_repository(repo, pid, 1, rid, 'template-v1', output)
    doc.installation.loads[0].apparent_power.value = '1234'
    result = verify_against_repository(repo, output)
    assert result['currentness'] == 'SOURCE_INVALID'


def test_original_snapshot_tamper_is_blocked(tmp_path, sources):
    repo, doc, pid, rid = sources
    output = tmp_path / 'generated'
    publish_from_repository(repo, pid, 1, rid, 'template-v1', output)
    with (output / 'snapshot.json').open('ab') as fh:
        fh.write(b'INVALID')
    result = verify_against_repository(repo, output)
    assert result["integrity"] == "INVALID"
    assert result["currentness"] == "SOURCE_INVALID"


def test_current_projection_divergence_is_not_labeled_current(tmp_path, sources, monkeypatch):
    repo, _doc, pid, rid = sources
    output = tmp_path / "generated"
    publish_from_repository(repo, pid, 1, rid, "template-v1", output)
    monkeypatch.setattr(repo, "verificar_revisao_atual",
                        lambda _pid, _rev: {"status": "SOURCE_INVALID", "reason": "tampered"})
    result = verify_against_repository(repo, output)
    assert result["currentness"] == "SOURCE_INVALID"


def test_registry_detects_manifest_rewrite_not_covered_by_bundle_hashes(tmp_path, sources):
    repo, _doc, pid, rid = sources
    output = tmp_path / "registered-bundle"
    publish_from_repository(repo, pid, 1, rid, "template-v1", output)
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes())
    manifest["generated_at"] = "2000-01-01T00:00:00+00:00"
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":")) + "\n", encoding="utf-8")
    result = verify_against_repository(repo, output)
    assert result["integrity"] == "INVALID"
    assert result["currentness"] == "SOURCE_INVALID"


def test_persisted_source_cli_generate_verify_and_recover(tmp_path, sources, monkeypatch, capsys):
    from sie_api import topology
    from sie_api.persisted_source_f10 import main

    repo, doc, pid, rid = sources
    monkeypatch.setattr(topology, "load_document", lambda _data: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _document: "d" * 64)
    from sie_api.storage import RepositorioProjetos
    def execution_seam(storage, project_id, revision, run_id):
        evidence = repo.consultar_calculo_f10(project_id, revision, run_id)
        evidence["source_sha256"] = storage.carregar_revisao(project_id, revision)["hash_sha256"]
        return evidence
    monkeypatch.setattr(RepositorioProjetos, "consultar_calculo_f10", execution_seam)
    destination = tmp_path / "cli-bundle"
    assert main(["generate", "--db", repo._storage.caminho,
                 "--project-id", pid, "--revision", "1", "--run-id", rid,
                 "--template-version", "template-v1", "--output-dir", str(destination)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "STUDY"
    assert main(["verify", "--db", repo._storage.caminho,
                 "--directory", str(destination)]) == 0
    assert json.loads(capsys.readouterr().out)["currentness"] == "CURRENT"
    assert main(["recover", "--db", repo._storage.caminho]) == 0
    assert json.loads(capsys.readouterr().out) == []


def test_concurrent_same_logical_publication_is_idempotent(tmp_path, sources):
    from concurrent.futures import ThreadPoolExecutor
    from sie_api.artifact_registry_f10 import ArtifactRegistryF10

    repo, _doc, pid, rid = sources
    destination = tmp_path / "concurrent" / "bundle"
    with ThreadPoolExecutor(max_workers=2) as pool:
        manifests = list(pool.map(
            lambda _index: publish_from_repository(
                repo, pid, 1, rid, "template-v1", destination), range(2)))
    assert manifests[0]["artifact_id"] == manifests[1]["artifact_id"]
    rows = ArtifactRegistryF10(repo).history(pid)
    assert len(rows) == 1
    assert rows[0]["state"] == "PUBLISHED"


def test_generation_rejects_declared_run_without_server_execution(sources):
    repo, doc, pid, rid = sources
    repo.execution_missing = True
    with pytest.raises(ArtifactError, match="execution absent"):
        resolve_persisted_source(repo, pid, 1, rid, "template-v1")


@pytest.mark.parametrize('field', ['circuit_id', 'project_id', 'revision', 'input_sha256',
                                   'result_sha256', 'algorithm_version', 'rule_version'])
def test_server_execution_record_mismatch_fails_closed(sources, monkeypatch, field):
    repo, doc, pid, rid = sources
    evidence = repo.consultar_calculo_f10(pid, 1, rid)
    evidence['record'][field] = 999 if field == 'revision' else 'incompatible'
    monkeypatch.setattr(repo, 'consultar_calculo_f10', lambda *_: evidence)
    with pytest.raises(ArtifactError, match='execution incompatible'):
        resolve_persisted_source(repo, pid, 1, rid, 'template-v1')
