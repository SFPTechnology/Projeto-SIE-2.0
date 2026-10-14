#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SQUAD_DIR}/../.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${REPO_ROOT}/workspace}"

declare -a REQUIRED_DIRS=(
  "${WORKSPACE_ROOT}"
  "${WORKSPACE_ROOT}/businesses"
  "${WORKSPACE_ROOT}/domains/content"
  "${WORKSPACE_ROOT}/domains/content/inputs"
  "${WORKSPACE_ROOT}/domains/content/swipe"
  "${WORKSPACE_ROOT}/domains/content/copy"
  "${WORKSPACE_ROOT}/_templates/product-offerbook"
  "${WORKSPACE_ROOT}/_templates/sales-process"
  "${REPO_ROOT}/outputs/copy"
)

created=0
for dir in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "${dir}" ]]; then
    mkdir -p "${dir}"
    created=$((created + 1))
    echo "created: ${dir}"
  fi
done

declare -a REQUIRED_FILES=(
  "${WORKSPACE_ROOT}/domains/content/copy-governance.yaml"
  "${WORKSPACE_ROOT}/domains/content/entities.yaml"
  "${WORKSPACE_ROOT}/domains/content/workflows.yaml"
)

missing=0
for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "${file}" ]]; then
    missing=$((missing + 1))
    echo "warning: missing required workspace file ${file}"
  fi
done

echo "bootstrap-copy-workspace: created_dirs=${created} missing_required_files=${missing}"
