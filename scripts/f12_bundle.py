#!/usr/bin/env python3
"""Create and verify a deterministic, non-production SIE F12 source bundle.

This packages only allowlisted tracked source files at HEAD, never production
configuration, credentials, databases or private state. SHA256 is integrity,
NOT identity/attestation/signature or authorization to deploy.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile

ALLOWED = (
    "restructuring/apps/api/sie_api/",
    "restructuring/apps/api/pyproject.toml",
    "restructuring/apps/web/",
    "restructuring/docs/",
    "docs/implantacao-sie-2-0/F12/",
    "scripts/f12_release_gate.py",
    "scripts/f12_bundle.py",
    "scripts/f12_staging_smoke.py",
)
BASENAME = "sie-f12-local-qa"
FORBIDDEN_ENDINGS = (".pem", ".key", ".p12", ".pfx", ".sqlite", ".db", ".env", ".secret")


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args],
                            capture_output=True, check=True)
    return result.stdout


def selected(path):
    p = PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts or "\\" in path or not path:
        return False
    if not any(path == x or path.startswith(x) for x in ALLOWED):
        return False
    if any(part.startswith(".env") or part in ("__pycache__", ".git", ".venv", "node_modules")
           for part in p.parts):
        return False
    if p.name.lower().endswith(FORBIDDEN_ENDINGS):
        return False
    return True


def enumerate_tracked(root):
    records = git(root, "ls-tree", "-rz", "HEAD").split(b"\0")
    result = []
    for rec in records:
        if not rec:
            continue
        lhs, raw = rec.split(b"\t", 1)
        mode, kind, oid = lhs.decode("ascii").split(" ")
        path = raw.decode("utf-8")
        if not selected(path):
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError("Entry not a regular source file: " + path)
        data = git(root, "show", "HEAD:" + path)
        result.append((path, data))
    if not result:
        raise ValueError("No tracked payload selected")
    return sorted(result)


def manifest_for(root, files):
    sha = git(root, "rev-parse", "HEAD").decode("ascii").strip()
    return {
        "schema": "SIE-F12-REPRO-BUNDLE-1",
        "source_commit": sha,
        "distribution": "LOCAL_QA_ONLY_NOT_APPROVED_FOR_PRODUCTION",
        "files": [{"path": p, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
                  for p, data in files],
    }


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _member(tf, name, data):
    ti = tarfile.TarInfo(name)
    ti.size, ti.mode, ti.mtime = len(data), 0o644, 0
    ti.uid = ti.gid = 0
    ti.uname = ti.gname = ""
    tf.addfile(ti, io.BytesIO(data))


def build(root, out):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Destination must be empty: " + str(out))
    out.mkdir(parents=True, exist_ok=True)
    files = enumerate_tracked(root)
    manifest = manifest_for(root, files)
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for path, data in files:
            _member(tf, "payload/" + path, data)
        _member(tf, "payload/MANIFEST.json", _json_bytes(manifest))
    gz_file = out / (BASENAME + ".tar.gz")
    with gz_file.open("wb") as stream:
        with gzip.GzipFile(fileobj=stream, mode="wb", filename="", mtime=0, compresslevel=9) as gz:
            gz.write(raw.getvalue())
    sha = hashlib.sha256(gz_file.read_bytes()).hexdigest()
    (out / (BASENAME + ".sha256")).write_text(sha + "  " + gz_file.name + "\n", encoding="ascii")
    (out / (BASENAME + "-manifest.json")).write_bytes(_json_bytes(manifest))
    return {"source_commit": manifest["source_commit"], "file_count": len(files), "sha256": sha,
            "production_authorized": False}


def verify(out):
    out = Path(out)
    archive = out / (BASENAME + ".tar.gz")
    sha_file = out / (BASENAME + ".sha256")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if sha_file.read_text(encoding="ascii") != digest + "  " + archive.name + "\n":
        raise ValueError("Archive checksum mismatch")
    man = json.loads((out / (BASENAME + "-manifest.json")).read_text(encoding="utf-8"))
    if man.get("distribution") != "LOCAL_QA_ONLY_NOT_APPROVED_FOR_PRODUCTION":
        raise ValueError("Invalid release scope")
    expected = {"payload/" + item["path"]: item for item in man["files"]}
    expected["payload/MANIFEST.json"] = None
    with tarfile.open(archive, mode="r:gz") as tf:
        actual = tf.getmembers()
        if set(x.name for x in actual) != set(expected) or len(actual) != len(expected):
            raise ValueError("Unexpected, missing or duplicate archive members")
        for member in actual:
            if not member.isfile() or member.issym() or member.islnk():
                raise ValueError("Archive contains non-regular file")
            p = PurePosixPath(member.name)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError("Archive traversal path")
            body = tf.extractfile(member).read()
            if member.name == "payload/MANIFEST.json":
                if body != _json_bytes(man):
                    raise ValueError("Embedded manifest mismatch")
                continue
            entry = expected[member.name]
            if not selected(entry["path"]) or hashlib.sha256(body).hexdigest() != entry["sha256"] or len(body) != entry["size"]:
                raise ValueError("Source data does not match manifest")
    return {"integrity": "VERIFIED", "source_commit": man["source_commit"],
            "file_count": len(man["files"]), "production_authorized": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "verify"))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    result = build(args.root.resolve(), args.out) if args.action == "build" else verify(args.out)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
