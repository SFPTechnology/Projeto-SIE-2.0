#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SQUAD_DIR}/../.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${REPO_ROOT}/workspace}"

python3 - "${SQUAD_DIR}" "${REPO_ROOT}" "${WORKSPACE_ROOT}" <<'PY'
import sys
from pathlib import Path

import yaml

squad_dir = Path(sys.argv[1])
repo_root = Path(sys.argv[2])
workspace_root = Path(sys.argv[3])
config_path = squad_dir / "config.yaml"

errors = []
warnings = []

if not config_path.exists():
    errors.append(f"missing config: {config_path}")
else:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    ws = cfg.get("workspace_integration")
    if not isinstance(ws, dict):
        errors.append("config.yaml missing workspace_integration block")
    else:
        level = ws.get("level")
        allowed = {"none", "read_only", "read_write", "workspace_first"}
        if level not in allowed:
            errors.append(f"invalid workspace_integration.level: {level}")

        read_paths = ws.get("read_paths") or []
        write_paths = ws.get("write_paths") or []
        if not isinstance(read_paths, list) or len(read_paths) == 0:
            errors.append("workspace_integration.read_paths must be a non-empty list")
        if not isinstance(write_paths, list):
            errors.append("workspace_integration.write_paths must be a list")

        for rel in read_paths + write_paths:
            p = repo_root / rel
            if not p.exists():
                errors.append(f"declared workspace path not found: {rel}")

        if level == "workspace_first":
            required_scripts = [
                squad_dir / "scripts" / "bootstrap-copy-workspace.sh",
                squad_dir / "scripts" / "validate-copy-essentials.sh",
            ]
            for script_path in required_scripts:
                if not script_path.exists():
                    errors.append(f"workspace_first requires script: {script_path.relative_to(repo_root)}")

required_files = [
    workspace_root / "domains/content/copy-governance.yaml",
    workspace_root / "domains/content/entities.yaml",
    workspace_root / "domains/content/workflows.yaml",
    workspace_root / "_templates/product-offerbook/headlines.yaml",
    workspace_root / "_templates/product-offerbook/sales-page.yaml",
    workspace_root / "_templates/product-offerbook/email-sequences.yaml",
    workspace_root / "_templates/sales-process/call-script.yaml",
]

for file_path in required_files:
    if not file_path.exists():
        errors.append(f"missing workspace essential: {file_path.relative_to(repo_root)}")

copy_task = squad_dir / "tasks" / "load-workspace-context.md"
if not copy_task.exists():
    errors.append("missing task: squads/aiox-copy/tasks/load-workspace-context.md")

if errors:
    print("validate-copy-essentials: FAIL")
    for item in errors:
        print(f"  - {item}")
    sys.exit(1)

print("validate-copy-essentials: PASS")
for item in warnings:
    print(f"  - warning: {item}")
PY
