"""Durable local registry for F10 artifacts and publication state.

The registry is deliberately separate from the artifact directory. It records
the authoritative snapshot/manifest digests and an append-only transition log,
but it does not claim a distributed transaction between SQLite and filesystem.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any
from uuid import UUID, uuid4

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised on Windows
    fcntl = None
    import msvcrt


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_STATES = {"PREPARING", "STAGED", "PUBLISHED", "FAILED", "RECOVERY_REQUIRED"}
_TRANSITIONS = {
    "PREPARING": {"STAGED", "PUBLISHED", "FAILED", "RECOVERY_REQUIRED"},
    "STAGED": {"PUBLISHED", "FAILED", "RECOVERY_REQUIRED"},
    "RECOVERY_REQUIRED": {"PUBLISHED", "FAILED"},
    "PUBLISHED": set(),
    "FAILED": set(),
}


@contextmanager
def _directory_lock(path: Path, already_locked: bool):
    if already_locked:
        yield
        return
    if fcntl is not None:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    else:
        lock_path = path / ".sie-f10-publisher.lock"
        if lock_path.is_symlink():
            raise ArtifactRegistryError("artifact lock path cannot be a symlink")
        descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        if os.fstat(descriptor).st_size == 0:
            os.write(descriptor, b"\0")
            os.fsync(descriptor)
    try:
        if fcntl is not None:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
        else:
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_LOCK, 1)
        yield
    finally:
        if fcntl is not None:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        else:
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
        os.close(descriptor)


class ArtifactRegistryError(ValueError):
    """Registry input or state transition is invalid."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_relative_destination(root: str | Path, destination: str | Path) -> tuple[Path, str]:
    """Return canonical root and relative target, refusing traversal/symlinks."""
    root_path = Path(root).expanduser().resolve()
    target = Path(destination).expanduser()
    if not target.is_absolute():
        target = root_path / target
    # First enforce lexical containment; resolve the parent afterwards to catch
    # symlinked ancestors without requiring that the final directory exists.
    try:
        lexical_relative = target.relative_to(root_path)
    except ValueError as exc:
        raise ArtifactRegistryError("artifact destination is outside configured root") from exc
    if not lexical_relative.parts or any(part in {"", ".", ".."} for part in lexical_relative.parts):
        raise ArtifactRegistryError("invalid artifact destination")
    cursor = root_path
    for part in lexical_relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ArtifactRegistryError("artifact destination path cannot contain symlinks")
    resolved_parent = target.parent.resolve()
    try:
        resolved_parent.relative_to(root_path)
    except ValueError as exc:
        raise ArtifactRegistryError("artifact destination escapes configured root") from exc
    if target.is_symlink():
        raise ArtifactRegistryError("artifact destination cannot be a symlink")
    return root_path, lexical_relative.as_posix()


class ArtifactRegistryF10:
    """SQLite registry bound to the repository's existing local connection."""

    def __init__(self, repository: Any):
        if not callable(getattr(repository, "_conectar", None)):
            raise TypeError("repository must expose the project's SQLite connection")
        self.repository = repository
        with repository._conectar() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS artefatos_f10(
                    artifact_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    revision_id INTEGER NOT NULL CHECK(revision_id >= 1),
                    calculation_run_id TEXT NOT NULL,
                    template_version TEXT NOT NULL,
                    snapshot_sha256 TEXT NOT NULL CHECK(length(snapshot_sha256)=64),
                    manifest_sha256 TEXT,
                    artifact_root TEXT NOT NULL,
                    destination_relative TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN
                        ('PREPARING','STAGED','PUBLISHED','FAILED','RECOVERY_REQUIRED')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(project_id, revision_id, calculation_run_id,
                           template_version, snapshot_sha256),
                    FOREIGN KEY(project_id,revision_id)
                        REFERENCES versoes_projeto(projeto_id,revisao)
                );
                CREATE TABLE IF NOT EXISTS eventos_artefato_f10(
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artifact_id TEXT NOT NULL REFERENCES artefatos_f10(artifact_id),
                    previous_state TEXT,
                    new_state TEXT NOT NULL,
                    detail_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS f10_artifact_project_history
                    ON artefatos_f10(project_id,revision_id,created_at);
                CREATE INDEX IF NOT EXISTS f10_artifact_recovery
                    ON artefatos_f10(state,updated_at);
                CREATE TRIGGER IF NOT EXISTS f10_artifact_events_no_update
                    BEFORE UPDATE ON eventos_artefato_f10
                    BEGIN SELECT RAISE(ABORT, 'evento de artefato imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f10_artifact_events_no_delete
                    BEFORE DELETE ON eventos_artefato_f10
                    BEGIN SELECT RAISE(ABORT, 'evento de artefato imutavel'); END;
            """)

    def reserve(
        self, *, project_id: str, revision_id: int, calculation_run_id: str,
        template_version: str, snapshot_sha256: str, artifact_root: str | Path,
        destination: str | Path, artifact_id: str | None = None,
    ) -> dict[str, Any]:
        """Create PREPARING before filesystem writes; repeated logical keys reuse row."""
        try:
            project_id = str(UUID(str(project_id)))
            artifact_id = str(UUID(str(artifact_id))) if artifact_id else str(uuid4())
        except (ValueError, TypeError, AttributeError) as exc:
            raise ArtifactRegistryError("project_id and artifact_id must be UUIDs") from exc
        if type(revision_id) is not int or revision_id < 1:
            raise ArtifactRegistryError("revision_id must be a positive integer")
        try:
            calculation_run_id = str(UUID(str(calculation_run_id)))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ArtifactRegistryError("calculation_run_id must be a UUID") from exc
        if not isinstance(template_version, str) or not template_version.strip():
            raise ArtifactRegistryError("template_version is required")
        if not isinstance(snapshot_sha256, str) or not _SHA256.fullmatch(snapshot_sha256):
            raise ArtifactRegistryError("snapshot_sha256 must be lowercase SHA-256")
        root_path, relative = _safe_relative_destination(artifact_root, destination)
        now = _now()
        with self.repository._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute(
                "SELECT * FROM artefatos_f10 WHERE project_id=? AND revision_id=? "
                "AND calculation_run_id=? AND template_version=? AND snapshot_sha256=?",
                (project_id, revision_id, calculation_run_id, template_version.strip(), snapshot_sha256),
            ).fetchone()
            if existing is not None:
                return dict(existing)
            db.execute(
                "INSERT INTO artefatos_f10(artifact_id,project_id,revision_id,calculation_run_id,"
                "template_version,snapshot_sha256,artifact_root,destination_relative,state,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (artifact_id, project_id, revision_id, calculation_run_id, template_version.strip(),
                 snapshot_sha256, str(root_path), relative, "PREPARING", now, now),
            )
            db.execute(
                "INSERT INTO eventos_artefato_f10(artifact_id,previous_state,new_state,detail_json,created_at) "
                "VALUES(?,NULL,'PREPARING',?,?)",
                (artifact_id, json.dumps({"destination": relative}, sort_keys=True), now),
            )
            row = db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?", (artifact_id,)).fetchone()
            return dict(row)

    def transition(
        self, artifact_id: str, expected_state: str, new_state: str, *,
        manifest_sha256: str | None = None, detail: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Compare-and-set state and append an immutable event in one transaction."""
        try:
            artifact_id = str(UUID(str(artifact_id)))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ArtifactRegistryError("artifact_id must be a UUID") from exc
        if expected_state not in _STATES or new_state not in _STATES:
            raise ArtifactRegistryError("unknown artifact state")
        if new_state not in _TRANSITIONS[expected_state]:
            raise ArtifactRegistryError(f"transition {expected_state}->{new_state} is not allowed")
        if manifest_sha256 is not None and not _SHA256.fullmatch(manifest_sha256):
            raise ArtifactRegistryError("manifest_sha256 must be lowercase SHA-256")
        if detail is not None and not isinstance(detail, dict):
            raise ArtifactRegistryError("detail must be an object")
        detail_json = json.dumps(detail or {}, sort_keys=True, ensure_ascii=False, allow_nan=False)
        now = _now()
        with self.repository._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?", (artifact_id,)).fetchone()
            if row is None:
                raise ArtifactRegistryError("artifact not found")
            if row["state"] != expected_state:
                raise ArtifactRegistryError("artifact state changed concurrently")
            if new_state == "PUBLISHED" and not manifest_sha256:
                raise ArtifactRegistryError("PUBLISHED requires an authoritative manifest hash")
            if (new_state == "PUBLISHED" and row["manifest_sha256"]
                    and row["manifest_sha256"] != manifest_sha256):
                raise ArtifactRegistryError("manifest hash differs from prepublication authority")
            cursor = db.execute(
                "UPDATE artefatos_f10 SET state=?,manifest_sha256=coalesce(?,manifest_sha256),updated_at=? "
                "WHERE artifact_id=? AND state=?",
                (new_state, manifest_sha256, now, artifact_id, expected_state),
            )
            if cursor.rowcount != 1:
                raise ArtifactRegistryError("artifact state changed concurrently")
            db.execute(
                "INSERT INTO eventos_artefato_f10(artifact_id,previous_state,new_state,detail_json,created_at) "
                "VALUES(?,?,?,?,?)", (artifact_id, expected_state, new_state, detail_json, now),
            )
            return dict(db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?", (artifact_id,)).fetchone())

    def record_expected_manifest(self, artifact_id: str, state: str,
                                 manifest_sha256: str) -> dict[str, Any]:
        """Persist the exact manifest digest before writing package bytes."""
        try:
            artifact_id = str(UUID(str(artifact_id)))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ArtifactRegistryError("artifact_id must be a UUID") from exc
        if state not in {"PREPARING", "STAGED"}:
            raise ArtifactRegistryError("manifest can only be prepared before publication")
        if not isinstance(manifest_sha256, str) or not _SHA256.fullmatch(manifest_sha256):
            raise ArtifactRegistryError("manifest_sha256 must be lowercase SHA-256")
        now = _now()
        with self.repository._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT state,manifest_sha256 FROM artefatos_f10 WHERE artifact_id=?",
                             (artifact_id,)).fetchone()
            if row is None or row["state"] != state:
                raise ArtifactRegistryError("artifact state changed concurrently")
            if row["manifest_sha256"]:
                if row["manifest_sha256"] != manifest_sha256:
                    raise ArtifactRegistryError("another publication attempt owns this reservation")
                return dict(db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?",
                                       (artifact_id,)).fetchone())
            db.execute("UPDATE artefatos_f10 SET manifest_sha256=?,updated_at=? "
                       "WHERE artifact_id=? AND state=?",
                       (manifest_sha256, now, artifact_id, state))
            detail = json.dumps({"expected_manifest_sha256": manifest_sha256},
                                sort_keys=True, ensure_ascii=False, allow_nan=False)
            db.execute(
                "INSERT INTO eventos_artefato_f10(artifact_id,previous_state,new_state,detail_json,created_at) "
                "VALUES(?,?,?,?,?)", (artifact_id, state, state, detail, now),
            )
            return dict(db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?",
                                   (artifact_id,)).fetchone())

    def get(self, artifact_id: str) -> dict[str, Any] | None:
        with self.repository._conectar() as db:
            row = db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?", (str(artifact_id),)).fetchone()
        return dict(row) if row else None

    def history(self, project_id: str) -> list[dict[str, Any]]:
        project_id = str(UUID(str(project_id)))
        with self.repository._conectar() as db:
            rows = db.execute(
                "SELECT * FROM artefatos_f10 WHERE project_id=? ORDER BY created_at,artifact_id",
                (project_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def events(self, artifact_id: str) -> list[dict[str, Any]]:
        with self.repository._conectar() as db:
            rows = db.execute(
                "SELECT * FROM eventos_artefato_f10 WHERE artifact_id=? ORDER BY event_id",
                (str(artifact_id),),
            ).fetchall()
        return [dict(row) for row in rows]

    def recoverable(self) -> list[dict[str, Any]]:
        with self.repository._conectar() as db:
            rows = db.execute(
                "SELECT * FROM artefatos_f10 WHERE state IN ('PREPARING','STAGED','RECOVERY_REQUIRED') "
                "ORDER BY created_at,artifact_id"
            ).fetchall()
        return [dict(row) for row in rows]

    def start_retry(self, artifact_id: str, *, lock_held: bool = False) -> dict[str, Any]:
        """Re-arm a failed reconciliation only when its destination is absent.

        The check uses the same parent-directory advisory lock as the F10
        publisher. The lock is released after the PREPARING transition; the
        publisher still enforces no-overwrite when it reacquires that lock.
        """
        try:
            artifact_id = str(UUID(str(artifact_id)))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ArtifactRegistryError("artifact_id must be a UUID") from exc
        row = self.get(artifact_id)
        if row is None:
            raise ArtifactRegistryError("artifact not found")
        if row["state"] == "PUBLISHED":
            return row
        if row["state"] != "RECOVERY_REQUIRED":
            raise ArtifactRegistryError("retry requires RECOVERY_REQUIRED state")
        stored_root = Path(row["artifact_root"])
        root = stored_root.resolve()
        if root != stored_root:
            raise ArtifactRegistryError("stored artifact root was redirected")
        target = root / row["destination_relative"]
        checked_root, relative = _safe_relative_destination(root, target)
        if relative != row["destination_relative"]:
            raise ArtifactRegistryError("stored destination is not canonical")
        root.mkdir(parents=True, exist_ok=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not checked_root.is_dir() or not target.parent.is_dir():
            raise ArtifactRegistryError("artifact root or destination parent is unavailable")
        # Re-resolve parent to detect a symlink substitution before acquiring the
        # cooperative lock used by publish_verified_bundle().
        try:
            target.parent.resolve().relative_to(checked_root)
        except ValueError as exc:
            raise ArtifactRegistryError("artifact destination escapes configured root") from exc
        try:
            with _directory_lock(target.parent, lock_held):
                if target.exists() or target.is_symlink():
                    raise ArtifactRegistryError("retry refused while destination exists")
                now = _now()
                with self.repository._conectar() as db:
                    db.execute("BEGIN IMMEDIATE")
                    current = db.execute(
                        "SELECT state,manifest_sha256 FROM artefatos_f10 WHERE artifact_id=?",
                        (artifact_id,),
                    ).fetchone()
                    if current is not None and current["state"] == "PUBLISHED":
                        return dict(db.execute("SELECT * FROM artefatos_f10 WHERE artifact_id=?",
                                               (artifact_id,)).fetchone())
                    if current is None or current["state"] != "RECOVERY_REQUIRED":
                        raise ArtifactRegistryError("artifact state changed concurrently")
                    cursor = db.execute(
                        "UPDATE artefatos_f10 SET state='PREPARING',manifest_sha256=NULL,updated_at=? "
                        "WHERE artifact_id=? AND state='RECOVERY_REQUIRED'",
                        (now, artifact_id),
                    )
                    if cursor.rowcount != 1:
                        raise ArtifactRegistryError("artifact state changed concurrently")
                    detail = json.dumps({
                        "retry": True,
                        "previous_manifest_sha256": current["manifest_sha256"],
                        "destination": relative,
                    }, sort_keys=True, ensure_ascii=False, allow_nan=False)
                    db.execute(
                        "INSERT INTO eventos_artefato_f10(artifact_id,previous_state,new_state,detail_json,created_at) "
                        "VALUES(?,'RECOVERY_REQUIRED','PREPARING',?,?)",
                        (artifact_id, detail, now),
                    )
                    return dict(db.execute(
                        "SELECT * FROM artefatos_f10 WHERE artifact_id=?", (artifact_id,)
                    ).fetchone())
        except OSError as exc:
            raise ArtifactRegistryError("artifact destination lock unavailable") from exc

    def reconcile_published(self, artifact_id: str, verifier, *,
                            lock_held: bool = False) -> dict[str, Any]:
        """Adopt a valid renamed package after crash; otherwise demand recovery.

        The supplied verifier must validate the bundle's internal integrity. The
        registry separately checks the artifact ID, snapshot digest, and manifest
        digest against values persisted before filesystem publication.
        """
        row = self.get(artifact_id)
        if row is None:
            raise ArtifactRegistryError("artifact not found")
        if row["state"] not in {"PREPARING", "STAGED", "RECOVERY_REQUIRED"}:
            return row
        target = Path(row["artifact_root"]) / row["destination_relative"]
        try:
            checked_root, checked_relative = _safe_relative_destination(
                row["artifact_root"], row["destination_relative"])
            if checked_relative != row["destination_relative"]:
                raise ArtifactRegistryError("registered destination is not canonical")
            target = checked_root / checked_relative
        except (ArtifactRegistryError, OSError):
            if row["state"] == "RECOVERY_REQUIRED":
                return row
            return self.transition(
                row["artifact_id"], row["state"], "RECOVERY_REQUIRED",
                detail={"reconciled": False, "reason": "registered destination path is unsafe"},
            )
        try:
            target.parent.stat()
        except OSError:
            if row["state"] == "RECOVERY_REQUIRED":
                return row
            return self.transition(
                row["artifact_id"], row["state"], "RECOVERY_REQUIRED",
                detail={"reconciled": False, "reason": "destination parent unavailable"},
            )
        try:
            with _directory_lock(target.parent, lock_held):
                latest = self.get(row["artifact_id"])
                if latest is None:
                    raise ArtifactRegistryError("artifact disappeared during reconciliation")
                if latest["state"] == "PUBLISHED":
                    return latest
                row = latest
                valid = False
                manifest_digest = None
                try:
                    result = verifier(target)
                    manifest_bytes = (target / "manifest.json").read_bytes()
                    manifest = json.loads(manifest_bytes)
                    manifest_digest = hashlib.sha256(manifest_bytes).hexdigest()
                    dependencies = manifest.get("dependencies")
                    valid = (
                        result.get("integrity") == "VERIFIED"
                        and manifest.get("artifact_id") == row["artifact_id"]
                        and manifest.get("snapshot_sha256") == row["snapshot_sha256"]
                        and isinstance(dependencies, dict)
                        and dependencies.get("project_id") == row["project_id"]
                        and dependencies.get("revision_id") == str(row["revision_id"])
                        and dependencies.get("calculation_run_id") == row["calculation_run_id"]
                        and dependencies.get("template_version") == row["template_version"]
                    )
                    if row["manifest_sha256"]:
                        valid = valid and manifest_digest == row["manifest_sha256"]
                except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
                    valid = False
                if valid:
                    return self.transition(
                        row["artifact_id"], row["state"], "PUBLISHED",
                        manifest_sha256=manifest_digest,
                        detail={"reconciled": True, "destination": row["destination_relative"]},
                    )
                if row["state"] == "RECOVERY_REQUIRED":
                    return row
                return self.transition(
                    row["artifact_id"], row["state"], "RECOVERY_REQUIRED",
                    detail={"reconciled": False, "reason": "published directory absent or failed authoritative checks"},
                )
        except OSError:
            if row["state"] == "RECOVERY_REQUIRED":
                return row
            return self.transition(
                row["artifact_id"], row["state"], "RECOVERY_REQUIRED",
                detail={"reconciled": False, "reason": "destination lock unavailable"},
            )
