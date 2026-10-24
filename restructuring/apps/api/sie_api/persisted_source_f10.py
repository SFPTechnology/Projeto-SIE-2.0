"""W1 local adapter: persisted F02/F05 revision and server-executed motor to F10.

Only a single persisted, VALID F02 calculation run/circuit is supported by the
current F10 scalar contract. Other cases fail closed. The existing legacy motor
is executed repository-side; no synthetic run IDs or normative approvals are introduced.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
from typing import Any
from uuid import UUID

from .representation_f10 import ArtifactContract, ArtifactError
from .artifact_store_f10 import (
    artifact_parent_lock, build_verified_bundle, publish_prebuilt_bundle,
    verify_verified_bundle,
)
from .artifact_registry_f10 import ArtifactRegistryF10, ArtifactRegistryError


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, OverflowError) as exc:
        raise ArtifactError("noncanonical authoritative input") from exc


def _id(value: Any, name: str) -> str:
    try:
        return str(UUID(str(value)))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ArtifactError(f"{name}: UUID required") from exc


def _exact_float(value: Any, name: str) -> float:
    """F10 currently renders floats; forbid silent loss in authoritative amounts."""
    try:
        value = Decimal(str(value))
        result = float(value)
    except (ValueError, TypeError, OverflowError, InvalidOperation) as exc:
        raise ArtifactError(f"{name}: invalid declared magnitude") from exc
    if not isfinite(result) or Decimal(str(result)) != value or value < 0:
        raise ArtifactError(f"{name}: magnitude is not losslessly representable in F10")
    return result


def _source(repo: Any, project_id: str, revision: int):
    from .topology import load_document, topology_hash
    if type(revision) is not int or revision < 1:
        raise ArtifactError("revision must be a positive integer")
    saved = repo.carregar_revisao(project_id, revision)
    if saved is None:
        raise ArtifactError("historical revision absent: no synthetic reconstruction")
    if saved["id"] != project_id or saved["revisao"] != revision:
        raise ArtifactError("repository returned another project/revision")
    import re
    if (saved.get("historico_recuperavel") is not True
            or not isinstance(saved.get("hash_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", saved["hash_sha256"])):
        raise ArtifactError("historical revision has no verified digest")
    try:
        document = load_document(saved["dados"])
    except (KeyError, ValueError, TypeError) as exc:
        raise ArtifactError("stored F02/F05 source absent or invalid") from exc
    inst = document.installation
    if str(inst.project.id) != project_id or inst.project.revision > revision:
        raise ArtifactError("installation revision incompatible with historical source")
    saved_snapshot = saved["dados"]["installation_snapshot"]
    if str(saved_snapshot["project_id"]) != project_id or saved_snapshot["revision"] != inst.project.revision:
        raise ArtifactError("installation snapshot identity mismatch")
    return saved, document, topology_hash(document)


def _resolve_persisted_source(
    repo: Any, project_id: str, revision: int, calculation_run_id: str,
    template_version: str,
) -> tuple[dict[str, Any], ArtifactContract]:
    """Project an immutable verified *stored* source; never accept a caller's F10 data.

    Deliberate W1 vertical-slice restriction: the current renderer's single
    run ID cannot attest to calculations for an entire multicircuit topology.
    """
    pid = _id(project_id, "project_id")
    rid = _id(calculation_run_id, "calculation_run_id")
    if not isinstance(template_version, str) or not template_version.strip():
        raise ArtifactError("template_version required")
    saved, document, topo_hash = _source(repo, pid, revision)
    inst = document.installation
    if len(inst.circuits) != 1:
        raise ArtifactError("F10 scalar calculation contract cannot attest to multiple circuits")
    circuit = inst.circuits[0]
    if circuit.kind != "TERMINAL":
        raise ArtifactError("F10 feeder mapping not implemented: do not infer apparent loads")
    matches = [r for r in inst.calculation_runs if str(r.id) == rid]
    if len(matches) != 1:
        raise ArtifactError("calculation run not present in historical installation")
    run = matches[0]
    if (run.state != "VALID" or run.circuit_id != circuit.id
            or run.project_revision != inst.project.revision
            or not run.output_sha256):
        raise ArtifactError("calculation run invalid, stale or for another circuit")
    evidence_reader = getattr(repo, "consultar_calculo_f10", None)
    if evidence_reader is None:
        raise ArtifactError("repository cannot attest server-side motor execution")
    evidence = evidence_reader(pid, revision, rid)
    if evidence is None:
        raise ArtifactError("server-side motor execution absent; execute persisted calculation first")
    record = evidence.get("record", {})
    if (evidence.get("project_id") != pid or evidence.get("revision") != revision
            or evidence.get("run_id") != rid
            or evidence.get("source_sha256") != saved["hash_sha256"]
            or record.get("circuit_id") != str(circuit.id)
            or record.get("project_id") != pid
            or record.get("revision") != inst.project.revision
            or record.get("input_sha256") != run.input_sha256
            or record.get("result_sha256") != run.output_sha256
            or record.get("algorithm_version") != run.algorithm_version
            or record.get("rule_version") != run.rule_version):
        raise ArtifactError("server-side execution incompatible with calculation run")
    runs = [r for r in inst.cable_runs if r.circuit_id == circuit.id]
    if len(runs) != 1:
        raise ArtifactError("ambiguous conductor mapping: one cable run is required")
    cable_run = runs[0]
    all_loads = {load.id: load for load in inst.loads}
    from .topology import exact_sum
    declared_components: list[Decimal] = []
    for load_id in circuit.load_ids:
        load = all_loads[load_id]
        if load.apparent_power is None or load.apparent_power.unit != "VA":
            raise ArtifactError("load missing declared apparent_power in VA; conversion prohibited")
        declared_components.append(Decimal(str(load.apparent_power.value)))
    if not declared_components:
        raise ArtifactError("terminal circuit has no load")
    declared_va = Decimal(exact_sum(declared_components))
    segments = {segment.id: segment for segment in inst.segments}
    physical_segments = []
    for segment_id in cable_run.segment_ids:
        seg = segments[segment_id]
        details = document.segment_details.get(seg.id)
        if details is None or details.route_status not in {"MEASURED", "DOCUMENTED"}:
            raise ArtifactError("route requires measured/documented provenance")
        if details.origin.method not in {"MEASURED", "DOCUMENTED"}:
            raise ArtifactError("segment origin is not measured/documented")
        physical_segments.append({
            "id": str(seg.id), "circuit_id": str(circuit.id),
            "conductor_id": str(cable_run.id),
            "length_m": _exact_float(seg.length.value, "segment.length_m"),
            "status": details.route_status, "origin": details.origin.reference,
        })
    calc_payload = run.model_dump(mode="json")
    snapshot = {
        "project_id": pid, "revision_id": str(revision),
        "calculation_run_id": rid, "rule_version": run.rule_version,
        "elements": [{"id": str(board.id), "kind": "panel"} for board in inst.boards],
        "circuits": [{
            "id": str(circuit.id), "panel_id": str(circuit.board_id),
            "load_va": _exact_float(declared_va, "circuit.load_va"),
            "phase": str(circuit.phases), "breaker_id": str(circuit.device_id),
            "conductor_id": str(cable_run.id),
        }],
        "segments": physical_segments,
        "source_evidence_f10": {
            "source_kind": "LOCAL_F02_F05_SERVER_EXECUTED_LEGACY_MOTOR",
            "motor_execution_sha256": evidence["hash_sha256"],
            "historical_revision": revision,
            "historical_revision_sha256": saved["hash_sha256"],
            "installation_snapshot_sha256": saved["dados"]["installation_snapshot"]["snapshot_sha256"],
            "installation_revision": inst.project.revision,
            "topology_sha256": topo_hash,
            "calculation_run_sha256": sha256(_canonical(calc_payload)).hexdigest(),
            "calculation_output_sha256": run.output_sha256,
            "algorithm_version": run.algorithm_version,
            "power_kind": "SUM_OF_DECLARED_APPARENT_POWER_VA_NOT_DEMAND",
            "conductor_kind": "CABLE_RUN_UUID_NOT_APPROVED_SECTION",
            "normative_conformity_verified": False,
        },
    }
    return snapshot, ArtifactContract(pid, str(revision), rid, run.rule_version, template_version)


def resolve_persisted_source(
    repo: Any, project_id: str, revision: int, calculation_run_id: str,
    template_version: str,
) -> tuple[dict[str, Any], ArtifactContract]:
    """Normalize malformed persisted records into a stable fail-closed error."""
    try:
        return _resolve_persisted_source(
            repo, project_id, revision, calculation_run_id, template_version)
    except ArtifactError:
        raise
    except (KeyError, IndexError, TypeError, ValueError, AttributeError) as exc:
        raise ArtifactError("persisted source is malformed or internally inconsistent") from exc


def publish_from_repository(
    repo: Any, project_id: str, revision: int, calculation_run_id: str,
    template_version: str, destination: str | Path,
) -> dict[str, Any]:
    snapshot, contract = resolve_persisted_source(
        repo, project_id, revision, calculation_run_id, template_version)
    target = Path(destination).expanduser().absolute()
    root = target.parent
    snapshot_sha = sha256(_canonical(snapshot) + b"\n").hexdigest()
    registry = ArtifactRegistryF10(repo)
    try:
        row = registry.reserve(
            project_id=contract.project_id, revision_id=revision,
            calculation_run_id=contract.calculation_run_id,
            template_version=contract.template_version,
            snapshot_sha256=snapshot_sha, artifact_root=root,
            destination=target.name,
        )
    except ArtifactRegistryError as exc:
        raise ArtifactError(str(exc)) from exc
    registered_target = Path(row["artifact_root"]) / row["destination_relative"]
    try:
        with artifact_parent_lock(registered_target):
            row = registry.get(row["artifact_id"])
            return _publish_reserved_locked(registry, row, snapshot, contract)
    except ArtifactRegistryError as exc:
        raise ArtifactError(str(exc)) from exc


def _publish_reserved_locked(
    registry: ArtifactRegistryF10, row: dict[str, Any],
    snapshot: dict[str, Any], contract: ArtifactContract,
) -> dict[str, Any]:
    artifact_id = row["artifact_id"]
    target = Path(row["artifact_root"]) / row["destination_relative"]
    snapshot_sha = sha256(_canonical(snapshot) + b"\n").hexdigest()
    if row["state"] == "PUBLISHED":
        try:
            result = verify_verified_bundle(target, lock_held=True)
            manifest_bytes = (target / "manifest.json").read_bytes()
            manifest = json.loads(manifest_bytes)
            if (result["integrity"] != "VERIFIED"
                    or manifest.get("artifact_id") != artifact_id
                    or manifest.get("snapshot_sha256") != snapshot_sha
                    or sha256(manifest_bytes).hexdigest() != row["manifest_sha256"]):
                raise ArtifactError("registered artifact no longer matches authoritative hashes")
            return manifest
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ArtifactError("registered artifact is missing or invalid") from exc

    if target.exists() or target.is_symlink():
        row = registry.reconcile_published(
            artifact_id, lambda path: verify_verified_bundle(path, lock_held=True),
            lock_held=True,
        )
        if row["state"] == "PUBLISHED":
            return json.loads((target / "manifest.json").read_bytes())
        raise ArtifactError("existing artifact requires recovery; refusing to overwrite")

    if row["state"] == "RECOVERY_REQUIRED":
        row = registry.start_retry(artifact_id, lock_held=True)
    elif row["state"] in {"PREPARING", "STAGED"} and row["manifest_sha256"]:
        # The previous process died while holding the directory lock. A stale
        # expected manifest with no destination is safe to reset and regenerate.
        row = registry.transition(
            artifact_id, row["state"], "RECOVERY_REQUIRED",
            detail={"recovered": False, "reason": "publication reservation left without destination"},
        )
        row = registry.start_retry(artifact_id, lock_held=True)
    if row["state"] not in {"PREPARING", "STAGED"}:
        raise ArtifactError(f"artifact publication cannot continue from {row['state']}")

    try:
        files, manifest = build_verified_bundle(snapshot, contract, artifact_id)
        expected_manifest_sha = sha256(files["manifest.json"]).hexdigest()
        row = registry.record_expected_manifest(
            artifact_id, row["state"], expected_manifest_sha)
        published = publish_prebuilt_bundle(files, manifest, target, lock_held=True)
        row = registry.transition(
            artifact_id, row["state"], "PUBLISHED",
            manifest_sha256=expected_manifest_sha,
            detail={"published": True, "destination": row["destination_relative"]},
        )
        if row["state"] != "PUBLISHED":
            raise ArtifactError("artifact registry did not confirm publication")
        return published
    except BaseException as exc:
        latest = registry.get(artifact_id)
        if target.exists() or target.is_symlink():
            try:
                reconciled = registry.reconcile_published(
                    artifact_id,
                    lambda path: verify_verified_bundle(path, lock_held=True),
                    lock_held=True,
                )
                if reconciled["state"] == "PUBLISHED":
                    return json.loads((target / "manifest.json").read_bytes())
            except (ArtifactRegistryError, OSError, ValueError, TypeError, json.JSONDecodeError):
                pass
        if latest and latest["state"] in {"PREPARING", "STAGED"}:
            try:
                registry.transition(
                    artifact_id, latest["state"], "RECOVERY_REQUIRED",
                    detail={"published": False, "error_type": type(exc).__name__},
                )
            except ArtifactRegistryError:
                pass
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        if isinstance(exc, ArtifactError):
            raise
        raise ArtifactError("artifact publication interrupted; recovery is required") from exc


def recover_registered_artifacts(repo: Any) -> list[dict[str, Any]]:
    """Reconcile interrupted publications and safely retry missing targets."""
    registry = ArtifactRegistryF10(repo)
    outcomes: list[dict[str, Any]] = []
    for initial in registry.recoverable():
        artifact_id = initial["artifact_id"]
        try:
            root = Path(initial["artifact_root"]).resolve()
            relative = Path(initial["destination_relative"])
            if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
                raise ArtifactError("registered destination path is unsafe")
            target = root / relative
            try:
                target.parent.resolve().relative_to(root)
            except ValueError as exc:
                raise ArtifactError("registered destination escapes root") from exc
            with artifact_parent_lock(target):
                row = registry.get(artifact_id)
                if row is None:
                    raise ArtifactError("registered artifact disappeared")
                if row["state"] == "PUBLISHED":
                    outcomes.append({"artifact_id": artifact_id, "state": "PUBLISHED",
                                     "action": "already_published"})
                    continue
                if target.exists() or target.is_symlink():
                    row = registry.reconcile_published(
                        artifact_id,
                        lambda path: verify_verified_bundle(path, lock_held=True),
                        lock_held=True,
                    )
                    outcomes.append({"artifact_id": artifact_id, "state": row["state"],
                                     "action": "reconciled"})
                    continue

                snapshot, contract = resolve_persisted_source(
                    repo, row["project_id"], row["revision_id"],
                    row["calculation_run_id"], row["template_version"],
                )
                snapshot_sha = sha256(_canonical(snapshot) + b"\n").hexdigest()
                if snapshot_sha != row["snapshot_sha256"]:
                    raise ArtifactError("authoritative source changed since reservation")
                if row["state"] == "RECOVERY_REQUIRED":
                    row = registry.start_retry(artifact_id, lock_held=True)
                elif row["state"] in {"PREPARING", "STAGED"}:
                    row = registry.transition(
                        artifact_id, row["state"], "RECOVERY_REQUIRED",
                        detail={"recovered": False, "reason": "previous process released publication lock"},
                    )
                    row = registry.start_retry(artifact_id, lock_held=True)
                files, manifest = build_verified_bundle(snapshot, contract, artifact_id)
                manifest_sha = sha256(files["manifest.json"]).hexdigest()
                row = registry.record_expected_manifest(artifact_id, row["state"], manifest_sha)
                published = publish_prebuilt_bundle(files, manifest, target, lock_held=True)
                final = registry.transition(
                    artifact_id, row["state"], "PUBLISHED", manifest_sha256=manifest_sha,
                    detail={"recovered": True, "destination": row["destination_relative"]},
                )
                outcomes.append({"artifact_id": artifact_id, "state": final["state"],
                                 "action": "republished" if published else "blocked"})
        except (ArtifactError, ArtifactRegistryError, OSError, ValueError, TypeError,
                KeyError, json.JSONDecodeError) as exc:
            latest = registry.get(artifact_id)
            outcomes.append({"artifact_id": artifact_id,
                             "state": latest["state"] if latest else "NOT_FOUND",
                             "action": "blocked", "reason": str(exc)})
    return outcomes


def _verify_against_repository_locked(repo: Any, root: Path) -> dict[str, Any]:
    """Verify historical derivation and currentness against the persisted source.

    CURRENT means current revision and original calculation still match. A
    valid historical revision remains intact but is labeled HISTORICAL/STALE.
    Failure to retrieve/validate a source is never reported CURRENT.
    """
    # Integrity failures are a verification result, not an exception that
    # should escape the CLI/API boundary. In particular, a malformed or
    # modified bundle must never be treated as current merely because the
    # verifier could not parse it.
    try:
        integrity = verify_verified_bundle(root, lock_held=True)
    except (ArtifactError, ValueError, KeyError, TypeError, OSError,
            UnicodeError, json.JSONDecodeError) as exc:
        return {
            "currentness": "SOURCE_INVALID",
            "integrity": "INVALID",
            "reason": str(exc),
        }
    try:
        stored = json.loads((root / "snapshot.json").read_bytes())
        manifest_bytes = (root / "manifest.json").read_bytes()
        manifest = json.loads(manifest_bytes)
        registry = ArtifactRegistryF10(repo)
        registered = registry.get(manifest.get("artifact_id"))
        expected_target = (Path(registered["artifact_root"]) / registered["destination_relative"]
                           if registered else None)
        if (registered is None or registered["state"] != "PUBLISHED"
                or registered["snapshot_sha256"] != manifest.get("snapshot_sha256")
                or registered["manifest_sha256"] != sha256(manifest_bytes).hexdigest()
                or expected_target is None
                or expected_target.resolve() != root.resolve()):
            return {**integrity, "integrity": "INVALID", "currentness": "SOURCE_INVALID",
                    "reason": "bundle is not consistent with the durable artifact registry"}
        snapshot_bytes = (root / "snapshot.json").read_bytes()

        def finish(currentness: str, reason: str | None = None,
                   live_snapshot: dict[str, Any] | None = None,
                   live_contract: ArtifactContract | None = None) -> dict[str, Any]:
            try:
                checked = verify_verified_bundle(
                    root, live_snapshot, live_contract, lock_held=True)
                final_manifest = (root / "manifest.json").read_bytes()
                final_snapshot = (root / "snapshot.json").read_bytes()
                if (final_manifest != manifest_bytes or final_snapshot != snapshot_bytes
                        or sha256(final_manifest).hexdigest() != registered["manifest_sha256"]):
                    return {**checked, "integrity": "INVALID", "currentness": "SOURCE_INVALID",
                            "reason": "artifact bytes changed during authoritative verification"}
                answer = {**checked, "currentness": currentness}
                if reason:
                    answer["reason"] = reason
                return answer
            except (ArtifactError, ValueError, KeyError, TypeError, OSError,
                    UnicodeError, json.JSONDecodeError) as exc:
                return {**integrity, "integrity": "INVALID", "currentness": "SOURCE_INVALID",
                        "reason": str(exc)}

        deps = manifest["dependencies"]
        pid = _id(deps["project_id"], "project_id")
        revision = int(deps["revision_id"])
        if str(revision) != deps["revision_id"]:
            raise ValueError("noncanonical revision")
        template = deps["template_version"]
        fresh, contract = resolve_persisted_source(
            repo, pid, revision, deps["calculation_run_id"], template)
        if fresh != stored:
            return finish("SOURCE_INVALID", "not derived from stored source")
        current = repo.carregar(pid)
        if current is None:
            return finish("CURRENTNESS_UNVERIFIED", "active project unavailable")
        consistency_check = getattr(repo, "verificar_revisao_atual", None)
        if consistency_check is None:
            return finish("CURRENTNESS_UNVERIFIED",
                          "repository cannot prove current row matches immutable revision")
        consistency = consistency_check(pid, current["revisao"])
        if not isinstance(consistency, dict) or consistency.get("status") != "CURRENT":
            source_status = consistency.get("status") if isinstance(consistency, dict) else None
            return finish(
                "SOURCE_INVALID" if source_status == "SOURCE_INVALID" else "CURRENTNESS_UNVERIFIED",
                consistency.get("reason") if isinstance(consistency, dict)
                else "repository returned no currentness contract",
            )
        if current["revisao"] != revision:
            try:
                _new_saved, new_doc, new_topo_hash = _source(repo, pid, current["revisao"])
                if new_topo_hash != stored["source_evidence_f10"]["topology_sha256"]:
                    return finish("STALE", "physical topology changed")
                old_evidence = stored["source_evidence_f10"]
                latest_run = [r for r in new_doc.installation.calculation_runs
                              if str(r.id) == deps["calculation_run_id"]]
                if (len(latest_run) != 1 or latest_run[0].state != "VALID"
                        or sha256(_canonical(latest_run[0].model_dump(mode="json"))).hexdigest()
                           != old_evidence["calculation_run_sha256"]):
                    return finish("STALE", "calculation run changed or invalidated")
                return finish("HISTORICAL", "new revision with unchanged declared dependencies")
            except (ArtifactError, ValueError, KeyError, TypeError) as exc:
                return finish("CURRENTNESS_UNVERIFIED", str(exc))
        return finish("CURRENT", "authoritative revision and calculation checked", fresh, contract)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {**integrity, "currentness": "SOURCE_INVALID", "reason": str(exc)}


def verify_against_repository(repo: Any, directory: str | Path) -> dict[str, Any]:
    """Verify using the same advisory directory lock as publishers/recovery."""
    root = Path(directory).expanduser().absolute()
    try:
        with artifact_parent_lock(root, shared=True, create_parent=False):
            return _verify_against_repository_locked(repo, root)
    except OSError as exc:
        return {"integrity": "INVALID", "currentness": "SOURCE_INVALID", "reason": str(exc)}


def main(argv: list[str] | None = None) -> int:
    from .storage import RepositorioProjetos
    parser = argparse.ArgumentParser(description="F10 experimental local persisted source adapter")
    sub = parser.add_subparsers(dest="action", required=True)
    produce = sub.add_parser("generate")
    produce.add_argument("--db", required=True)
    produce.add_argument("--project-id", required=True)
    produce.add_argument("--revision", type=int, required=True)
    produce.add_argument("--run-id", required=True)
    produce.add_argument("--template-version", required=True)
    produce.add_argument("--output-dir", required=True)
    execute = sub.add_parser("execute")
    execute.add_argument("--db", required=True)
    execute.add_argument("--project-id", required=True)
    execute.add_argument("--revision", type=int, required=True)
    execute.add_argument("--run-id", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--db", required=True)
    verify.add_argument("--directory", required=True)
    recover = sub.add_parser("recover")
    recover.add_argument("--db", required=True)
    args = parser.parse_args(argv)
    # Prevent typo-created SQLite databases on read operations.
    if not Path(args.db).is_file():
        parser.error("SQLite database does not exist")
    repository = RepositorioProjetos(args.db)
    if args.action == "execute":
        evidence = repository.executar_calculo_f10(
            args.project_id, args.revision, args.run_id)
        print(json.dumps({"run_id": evidence["run_id"],
                          "execution_sha256": evidence["hash_sha256"],
                          "normative_conformity_verified": False}))
        return 0
    if args.action == "generate":
        manifest = publish_from_repository(repository, args.project_id, args.revision,
                                           args.run_id, args.template_version, args.output_dir)
        print(json.dumps({"artifact_id": manifest["artifact_id"], "status": "STUDY"}))
        return 0
    if args.action == "recover":
        outcomes = recover_registered_artifacts(repository)
        print(json.dumps(outcomes, ensure_ascii=False))
        return 0 if all(item["state"] in {"PUBLISHED", "FAILED"} for item in outcomes) else 2
    result = verify_against_repository(repository, args.directory)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["currentness"] in {"CURRENT", "HISTORICAL"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
