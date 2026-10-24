"""SIE integration-seam test: actual RepositorioProjetos with isolated SQLite.

Includes both an isolated storage seam and a real F05 parser/topology fixture.
"""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from test_persisted_source_f10 import make_doc
from sie_api.persisted_source_f10 import (
    publish_from_repository, recover_registered_artifacts, resolve_persisted_source,
    verify_against_repository,
)
from sie_api.artifact_registry_f10 import ArtifactRegistryF10


def mock_motor_evidence(monkeypatch, doc):
    """Narrow seam only: these registry tests do not attest a real motor."""
    from sie_api.storage import RepositorioProjetos
    def evidence(repo, pid, revision, rid):
        run = doc.installation.calculation_runs[0]
        return {"project_id": pid, "revision": revision, "run_id": rid,
                "source_sha256": repo.carregar_revisao(pid, revision)["hash_sha256"],
                "hash_sha256": "e" * 64,
                "record": {"project_id": pid, "revision": run.project_revision,
                           "circuit_id": str(run.circuit_id),
                           "input_sha256": run.input_sha256,
                           "result_sha256": run.output_sha256,
                           "algorithm_version": run.algorithm_version,
                           "rule_version": run.rule_version}}
    monkeypatch.setattr(RepositorioProjetos, "consultar_calculo_f10", evidence)


def test_real_repository_readonly_historical_revision(tmp_path, monkeypatch):
    from sie_api.storage import RepositorioProjetos
    from sie_api import topology

    doc, pid, calc_id, data = make_doc()
    repo = RepositorioProjetos(tmp_path / "f10_w1_test.sqlite")
    assert repo.salvar(pid, "Projeto de ensaio", data, 0) == 1
    # This verifies SQLite repository's real historical-read + digest boundary.
    # F05 parser must be exercised separately with a genuine Topology fixture.
    mock_motor_evidence(monkeypatch, doc)
    monkeypatch.setattr(topology, "load_document", lambda _: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _: "d" * 64)
    snapshot, contract = resolve_persisted_source(repo, pid, 1, calc_id, "template-v1")
    assert contract.project_id == pid
    assert snapshot["source_evidence_f10"]["historical_revision_sha256"] == repo.carregar_revisao(pid, 1)["hash_sha256"]
    assert repo.carregar(pid)["revisao"] == 1
    assert repo.salvar(pid, "Revisão 2", {"other": True}, 1) == 2
    # The old saved revision, not the project's mutable current copy, was read.
    assert repo.carregar_revisao(pid, 1)["dados"] == data


def test_sqlite_registry_publisher_and_current_verification(tmp_path, monkeypatch):
    from sie_api.storage import RepositorioProjetos
    from sie_api import topology

    doc, pid, calc_id, data = make_doc()
    repo = RepositorioProjetos(tmp_path / "integrated.sqlite")
    repo.salvar(pid, "Projeto integrado", data, 0)
    mock_motor_evidence(monkeypatch, doc)
    monkeypatch.setattr(topology, "load_document", lambda _: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _: "d" * 64)

    destination = tmp_path / "exports" / "bundle"
    manifest = publish_from_repository(repo, pid, 1, calc_id, "template-v1", destination)
    assert manifest["artifact_id"]
    rows = ArtifactRegistryF10(repo).history(pid)
    assert len(rows) == 1
    assert rows[0]["state"] == "PUBLISHED"
    assert len(ArtifactRegistryF10(repo).events(rows[0]["artifact_id"])) == 3
    assert verify_against_repository(repo, destination)["currentness"] == "CURRENT"


def test_sqlite_recovery_retries_interrupted_preparing_record(tmp_path, monkeypatch):
    from sie_api.storage import RepositorioProjetos
    from sie_api import topology
    import sie_api.persisted_source_f10 as adapter

    doc, pid, calc_id, data = make_doc()
    repo = RepositorioProjetos(tmp_path / "recover.sqlite")
    repo.salvar(pid, "Projeto recovery", data, 0)
    mock_motor_evidence(monkeypatch, doc)
    monkeypatch.setattr(topology, "load_document", lambda _: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _: "d" * 64)
    destination = tmp_path / "exports" / "retry-bundle"

    def fail_before_files(*_args, **_kwargs):
        raise OSError("injected interruption before filesystem publication")

    monkeypatch.setattr(adapter, "publish_prebuilt_bundle", fail_before_files)
    try:
        publish_from_repository(repo, pid, 1, calc_id, "template-v1", destination)
    except adapter.ArtifactError:
        pass
    else:
        raise AssertionError("interrupted publication should fail")
    row = ArtifactRegistryF10(repo).history(pid)[0]
    assert row["state"] == "RECOVERY_REQUIRED"

    monkeypatch.undo()
    mock_motor_evidence(monkeypatch, doc)
    monkeypatch.setattr(topology, "load_document", lambda _: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _: "d" * 64)
    result = recover_registered_artifacts(repo)
    assert result == [{"artifact_id": row["artifact_id"], "state": "PUBLISHED",
                       "action": "republished"}]


def test_sqlite_reconciles_rename_completed_before_registry_commit(tmp_path, monkeypatch):
    from sie_api.storage import RepositorioProjetos
    from sie_api import topology
    import sie_api.persisted_source_f10 as adapter

    doc, pid, calc_id, data = make_doc()
    repo = RepositorioProjetos(tmp_path / "after-rename.sqlite")
    repo.salvar(pid, "Projeto after rename", data, 0)
    mock_motor_evidence(monkeypatch, doc)
    monkeypatch.setattr(topology, "load_document", lambda _: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _: "d" * 64)
    actual_publish = adapter.publish_prebuilt_bundle
    destination = tmp_path / "exports" / "renamed-bundle"

    def publish_then_interrupt(*args, **kwargs):
        actual_publish(*args, **kwargs)
        raise OSError("injected crash after atomic rename, before registry commit")

    monkeypatch.setattr(adapter, "publish_prebuilt_bundle", publish_then_interrupt)
    manifest = publish_from_repository(repo, pid, 1, calc_id, "template-v1", destination)
    row = ArtifactRegistryF10(repo).history(pid)[0]
    assert row["state"] == "PUBLISHED"
    assert destination.is_dir()
    assert manifest["artifact_id"] == row["artifact_id"]
    assert ArtifactRegistryF10(repo).get(row["artifact_id"])["state"] == "PUBLISHED"


def test_process_death_during_partial_staging_releases_lock_and_recovers(tmp_path, monkeypatch):
    import multiprocessing
    import os
    from sie_api import topology
    from sie_api.artifact_store_f10 import publish_verified_bundle
    from test_persisted_source_f10 import VersionedRepo

    doc, pid, run_id, data = make_doc()
    repo = VersionedRepo(pid, data, tmp_path / "crash-fixture.sqlite")
    repo.documents = {1: doc}
    repo.history[1]["dados"]["test_document_revision"] = 1
    monkeypatch.setattr(topology, "load_document", lambda _data: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _document: "d" * 64)
    snapshot, contract = resolve_persisted_source(repo, pid, 1, run_id, "template-v1")
    root = tmp_path / "crash-stage"
    target = root / "bundle"
    row = ArtifactRegistryF10(repo).reserve(
        project_id=pid, revision_id=1, calculation_run_id=run_id,
        template_version="template-v1",
        snapshot_sha256=hashlib.sha256(
            json.dumps(snapshot, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"
        ).hexdigest(),
        artifact_root=root, destination="bundle",
    )

    def die_before_rename():
        import sie_api.artifact_store_f10 as store
        real_fsync = os.fsync

        def crash_after_first_file_sync(fd):
            real_fsync(fd)
            os._exit(73)

        store.os.fsync = crash_after_first_file_sync
        publish_verified_bundle(snapshot, contract, target, row["artifact_id"])

    process = multiprocessing.get_context("fork").Process(target=die_before_rename)
    process.start()
    process.join(timeout=10)
    if process.is_alive():
        process.kill()
        process.join()
        raise AssertionError("crash-injection child did not exit")
    assert process.exitcode == 73
    assert not target.exists()
    orphan = root / (".f10-stage-" + row["artifact_id"])
    assert orphan.is_dir()
    assert len(list(orphan.iterdir())) == 1

    outcomes = recover_registered_artifacts(repo)
    assert outcomes[0]["state"] == "PUBLISHED"
    assert not orphan.exists()
    assert ArtifactRegistryF10(repo).get(row["artifact_id"])["state"] == "PUBLISHED"
    assert recover_registered_artifacts(repo) == []


def test_process_death_after_rename_reconciles_from_durable_manifest_hash(tmp_path, monkeypatch):
    import multiprocessing
    import os
    from sie_api import topology
    from sie_api.storage import RepositorioProjetos
    from test_persisted_source_f10 import VersionedRepo

    doc, pid, run_id, data = make_doc()
    db_path = tmp_path / "after-rename-crash.sqlite"
    repo = VersionedRepo(pid, data, db_path)
    repo.documents = {1: doc}
    repo.history[1]["dados"]["test_document_revision"] = 1
    monkeypatch.setattr(topology, "load_document", lambda _data: doc)
    monkeypatch.setattr(topology, "topology_hash", lambda _document: "d" * 64)
    destination = tmp_path / "after-rename-crash-exports" / "bundle"

    def die_after_rename():
        import sie_api.persisted_source_f10 as adapter
        real_publish = adapter.publish_prebuilt_bundle

        def publish_then_exit(*args, **kwargs):
            real_publish(*args, **kwargs)
            os._exit(74)

        adapter.publish_prebuilt_bundle = publish_then_exit
        adapter.publish_from_repository(repo, pid, 1, run_id, "template-v1", destination)

    process = multiprocessing.get_context("fork").Process(target=die_after_rename)
    process.start()
    process.join(timeout=10)
    if process.is_alive():
        process.kill()
        process.join()
        raise AssertionError("crash-injection child did not exit")
    assert process.exitcode == 74
    assert destination.is_dir()

    reopened = RepositorioProjetos(db_path)
    registry = ArtifactRegistryF10(reopened)
    rows = registry.history(pid)
    assert len(rows) == 1
    assert rows[0]["state"] == "PREPARING"
    assert len(rows[0]["manifest_sha256"]) == 64
    recovered = recover_registered_artifacts(reopened)
    assert recovered == [{"artifact_id": rows[0]["artifact_id"], "state": "PUBLISHED",
                          "action": "reconciled"}]
    assert registry.get(rows[0]["artifact_id"])["state"] == "PUBLISHED"


def test_real_f05_parser_run_and_sqlite_publish_without_parser_mocks(tmp_path):
    from sie_api.storage import RepositorioProjetos
    from sie_api.domain.installation import Installation
    from sie_api.installation_service import create_snapshot
    from sie_api.topology import load_document, topology_hash

    fixture = Path(__file__).resolve().parents[3] / "examples/f05_topologia_demo.json"
    raw = json.loads(fixture.read_text(encoding="utf-8"))
    inst = raw["installation"]
    circuit_id = "00000000-0000-0000-0000-000000000019"
    board_id = "00000000-0000-0000-0000-000000000008"
    segment_id = "00000000-0000-0000-0000-00000000001b"
    load_id = "00000000-0000-0000-0000-00000000000c"
    device_id = "00000000-0000-0000-0000-000000000018"
    cable_run_id = "00000000-0000-0000-0000-00000000001a"
    supply_id = "00000000-0000-0000-0000-000000000006"
    inst["boards"] = [next(item for item in inst["boards"] if item["id"] == board_id)]
    inst["boards"][0]["supply_id"] = supply_id
    inst["circuits"] = [next(item for item in inst["circuits"] if item["id"] == circuit_id)]
    inst["loads"] = [next(item for item in inst["loads"] if item["id"] == load_id)]
    inst["devices"] = [next(item for item in inst["devices"] if item["id"] == device_id)]
    inst["cable_runs"] = [next(item for item in inst["cable_runs"] if item["id"] == cable_run_id)]
    inst["segments"] = [next(item for item in inst["segments"] if item["id"] == segment_id)]
    run = deepcopy(inst["calculation_runs"][0])
    run.update(circuit_id=circuit_id, state="VALID", output_sha256="b" * 64,
               project_revision=1)
    inst["calculation_runs"] = [run]
    inst["rooms"] = [next(item for item in inst["rooms"] if item["id"] == "00000000-0000-0000-0000-000000000005")]
    inst["load_points"] = [next(item for item in inst["load_points"] if item["id"] == "00000000-0000-0000-0000-00000000000a")]
    raw["board_details"] = {board_id: raw["board_details"][board_id]}
    raw["board_details"][board_id]["buses"][0]["circuit_ids"] = [circuit_id]
    raw["segment_details"] = {segment_id: next(iter(raw["segment_details"].values()))}
    raw["segment_details"][segment_id]["origin"]["method"] = "DOCUMENTED"
    raw["segment_details"][segment_id]["route_status"] = "DOCUMENTED"

    project_id = inst["project"]["id"]
    from sie_api.analysis_contracts import AnaliseCircuito
    from sie_api.installation_service import analyze_legacy
    parameters = AnaliseCircuito.model_validate({
        "corrente_a": 5, "comprimento_m": 5, "tensao_v": 220,
        "resistencia_ohm_km": 7.41, "fator_correcao": 1,
        "tabela_condutores": [{"secao_mm2": 4, "capacidade_a": 32}],
        "evidencia": {"documento": "Synthetic test, not normative",
                      "edicao": "TEST", "referencia": "fixture"}})
    first = analyze_legacy(create_snapshot(Installation.model_validate(inst)),
                           Installation.model_validate(inst).circuits[0].id,
                           parameters, run["rule_version"])
    run.update(input_sha256=first.input_sha256, output_sha256=first.result_sha256,
               algorithm_version=first.algorithm_version)
    model = Installation.model_validate(inst)
    saved_data = {
        "installation_snapshot": create_snapshot(model).model_dump(mode="json"),
        "calculation_inputs_f10": {run["id"]: parameters.model_dump(mode="json")},
        "topology_metadata": {key: value for key, value in raw.items() if key != "installation"},
    }
    parsed = load_document(saved_data)
    assert len(parsed.installation.circuits) == 1
    assert topology_hash(parsed) != ""

    repo = RepositorioProjetos(tmp_path / "real-f05.sqlite")
    repo.salvar(project_id, "F05 synthetic integration fixture", saved_data, 0)
    run_id = str(parsed.installation.calculation_runs[0].id)
    from sie_api.persisted_source_f10 import main
    assert main(["execute", "--db", str(repo.caminho), "--project-id", project_id,
                 "--revision", "1", "--run-id", run_id]) == 0
    evidence = repo.executar_calculo_f10(project_id, 1, run_id)
    assert evidence["record"]["result_sha256"] == run["output_sha256"]
    snapshot, contract = resolve_persisted_source(repo, project_id, 1, run_id, "template-v1")
    assert snapshot["source_evidence_f10"]["topology_sha256"] == topology_hash(parsed)
    destination = tmp_path / "real-f05-exports" / "bundle"
    publish_from_repository(repo, project_id, 1, run_id, "template-v1", destination)
    assert verify_against_repository(repo, destination)["currentness"] == "CURRENT"
