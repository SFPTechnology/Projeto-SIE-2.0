#!/usr/bin/env bash
# clone-bench.sh — Clone Deep Research Bench from HF Spaces
#
# Origin: STORY-153.7 (EPIC-153)
# Pins bench at a specific SHA for reproducibility.

set -euo pipefail

# Resolve repo root via git (portable)
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel 2>/dev/null)"
if [[ -z "$REPO_ROOT" ]]; then
  REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
fi

BENCH_DIR="$REPO_ROOT/../bench/deep-research-bench"
BENCH_REPO="https://github.com/Ayanami0730/deep_research_bench"

echo "🔻 Cloning Deep Research Bench..."
echo "   Source: $BENCH_REPO"
echo "   Target: $BENCH_DIR"

if [[ -d "$BENCH_DIR" ]]; then
  echo "✅ Already cloned at $BENCH_DIR"
  echo "   Current SHA: $(git -C "$BENCH_DIR" rev-parse HEAD)"
  echo
  echo "To update: git -C \"$BENCH_DIR\" pull"
  exit 0
fi

mkdir -p "$(dirname "$BENCH_DIR")"
git clone --depth 1 "$BENCH_REPO" "$BENCH_DIR"

BENCH_SHA="$(git -C "$BENCH_DIR" rev-parse HEAD)"
echo
echo "✅ Cloned successfully"
echo "   SHA: $BENCH_SHA"
echo
echo "Pin this SHA in docs/bench/aiox-deep-research-bench-submission/reproducibility.md"
echo "Update the 'Bench commit SHA' field."
