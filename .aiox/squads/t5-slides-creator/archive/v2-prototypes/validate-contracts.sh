#!/usr/bin/env bash
# =============================================================================
# validate-contracts.sh
# Cross-Squad Contract Testing — Story 4.4 (EPIC-SC-V2-001)
#
# Validates all cross-squad contract fixtures against their JSON Schemas
# using ajv-cli. Tests backward compatibility (v1 fixtures against v1.1.0).
#
# Usage:
#   ./squads/slides-creator/scripts/validate-contracts.sh
#   ./squads/slides-creator/scripts/validate-contracts.sh --verbose
#   ./squads/slides-creator/scripts/validate-contracts.sh --ci
#
# Prerequisites:
#   npm install -g ajv-cli
#   (or use npx — script auto-detects)
# =============================================================================

set -euo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCHEMAS_DIR="$PROJECT_ROOT/schemas/contracts"
FIXTURES_DIR="$SCHEMAS_DIR/fixtures"
BRIEFING_SCHEMA="$PROJECT_ROOT/squads/slides-creator/templates/briefing.normalized.json"

VERBOSE=false
CI_MODE=false
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
TOTAL_COUNT=0

# --- Parse args ---
for arg in "$@"; do
  case $arg in
    --verbose) VERBOSE=true ;;
    --ci) CI_MODE=true ;;
    --help|-h)
      echo "Usage: $0 [--verbose] [--ci]"
      echo "  --verbose  Show detailed validation output"
      echo "  --ci       Exit with non-zero on any failure (for CI pipelines)"
      exit 0
      ;;
  esac
done

# --- Detect ajv ---
AJV_CMD=""
if command -v ajv &>/dev/null; then
  AJV_CMD="ajv"
elif command -v npx &>/dev/null; then
  AJV_CMD="npx --yes ajv-cli"
else
  echo "ERROR: ajv-cli not found. Install with: npm install -g ajv-cli"
  echo "       Or ensure npx is available."
  exit 1
fi

# --- Helpers ---
log_pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  TOTAL_COUNT=$((TOTAL_COUNT + 1))
  echo "  PASS  $1"
}

log_fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  TOTAL_COUNT=$((TOTAL_COUNT + 1))
  echo "  FAIL  $1"
  if [ -n "${2:-}" ]; then
    echo "        $2"
  fi
}

log_skip() {
  SKIP_COUNT=$((SKIP_COUNT + 1))
  TOTAL_COUNT=$((TOTAL_COUNT + 1))
  echo "  SKIP  $1 ($2)"
}

validate() {
  local schema="$1"
  local fixture="$2"
  local label="$3"

  if [ ! -f "$schema" ]; then
    log_skip "$label" "schema not found: $schema"
    return
  fi

  if [ ! -f "$fixture" ]; then
    log_skip "$label" "fixture not found: $fixture"
    return
  fi

  local output
  if output=$($AJV_CMD validate -s "$schema" -d "$fixture" --spec=draft2020 --strict=false 2>&1); then
    log_pass "$label"
  else
    log_fail "$label" "$output"
  fi
}

# =============================================================================
echo ""
echo "Cross-Squad Contract Validation"
echo "==============================="
echo "Project root: $PROJECT_ROOT"
echo "Schemas dir:  $SCHEMAS_DIR"
echo "Fixtures dir: $FIXTURES_DIR"
echo ""

# --- Section 1: etl-ops YouTube output ---
echo "--- Contract: etl-ops -> slides-creator (YouTube Extraction) ---"
echo ""

validate \
  "$SCHEMAS_DIR/youtube-extraction.schema.json" \
  "$FIXTURES_DIR/youtube-extraction.fixture.json" \
  "youtube-extraction: happy path (with chapters)"

validate \
  "$SCHEMAS_DIR/youtube-extraction.schema.json" \
  "$FIXTURES_DIR/youtube-extraction-no-chapters.fixture.json" \
  "youtube-extraction: edge case (no chapters)"

validate \
  "$SCHEMAS_DIR/youtube-extraction.schema.json" \
  "$FIXTURES_DIR/youtube-extraction-whisper-fallback.fixture.json" \
  "youtube-extraction: edge case (Whisper fallback, no visual analysis)"

echo ""

# --- Section 2: slides-creator -> face-forge (Visual Generation) ---
echo "--- Contract: slides-creator -> face-forge (Visual Generation Request) ---"
echo ""

validate \
  "$SCHEMAS_DIR/visual-generation-request.schema.json" \
  "$FIXTURES_DIR/visual-generation-request.fixture.json" \
  "visual-generation-request: happy path (full fields)"

validate \
  "$SCHEMAS_DIR/visual-generation-request.schema.json" \
  "$FIXTURES_DIR/visual-generation-request-minimal.fixture.json" \
  "visual-generation-request: edge case (minimal required fields only)"

echo ""

# --- Section 3: face-forge -> slides-creator (Visual Generation Response) ---
echo "--- Contract: face-forge -> slides-creator (Visual Generation Response) ---"
echo ""

validate \
  "$SCHEMAS_DIR/visual-generation-response.schema.json" \
  "$FIXTURES_DIR/visual-generation-response.fixture.json" \
  "visual-generation-response: happy path (success)"

validate \
  "$SCHEMAS_DIR/visual-generation-response.schema.json" \
  "$FIXTURES_DIR/visual-generation-response-fallback.fixture.json" \
  "visual-generation-response: edge case (fallback to secondary engine)"

validate \
  "$SCHEMAS_DIR/visual-generation-response.schema.json" \
  "$FIXTURES_DIR/visual-generation-response-failed.fixture.json" \
  "visual-generation-response: edge case (all engines failed)"

echo ""

# --- Section 4: slides-creator -> Kroki (Diagram Generation) ---
echo "--- Contract: slides-creator -> Kroki (Diagram Generation Request) ---"
echo ""

validate \
  "$SCHEMAS_DIR/diagram-generation-request.schema.json" \
  "$FIXTURES_DIR/diagram-generation-request.fixture.json" \
  "diagram-generation-request: happy path (D2 with theme overrides)"

echo ""

# --- Section 5: Backward Compatibility (briefing v1 against v1.1.0 schema) ---
echo "--- Backward Compatibility: briefing v1 -> schema v1.1.0 ---"
echo ""

validate \
  "$BRIEFING_SCHEMA" \
  "$FIXTURES_DIR/briefing-v1-no-education.json" \
  "briefing backward compat: v1 payload (no education fields) against v1.1.0"

validate \
  "$BRIEFING_SCHEMA" \
  "$FIXTURES_DIR/briefing-v1-corporate.fixture.json" \
  "briefing backward compat: v1 corporate (warnings, no education) against v1.1.0"

validate \
  "$BRIEFING_SCHEMA" \
  "$FIXTURES_DIR/briefing-v2-education.json" \
  "briefing v1.1.0: education_mode=true with audience_profile"

echo ""

# --- Summary ---
echo "==============================="
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed, $SKIP_COUNT skipped (total: $TOTAL_COUNT)"
echo ""

if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "STATUS: FAIL"
  if [ "$CI_MODE" = true ]; then
    exit 1
  fi
  exit 0
else
  echo "STATUS: PASS"
fi
