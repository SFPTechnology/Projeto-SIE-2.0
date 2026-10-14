#!/usr/bin/env bash
# =============================================================================
# Slides Creator v2 — Infrastructure Health Check
# =============================================================================
# Validates all dependencies required by the slides-creator v2 pipeline.
# Run: bash squads/slides-creator/scripts/health-check-v2.sh
# =============================================================================

set -euo pipefail

PASS=0
FAIL=0
WARN=0

pass() { echo "  [PASS] $1"; ((PASS++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }
warn() { echo "  [WARN] $1"; ((WARN++)); }

echo "============================================"
echo " Slides Creator v2 — Health Check"
echo "============================================"
echo ""

# --- 1. D2 CLI ---------------------------------------------------------------
echo "1. D2 CLI"
if command -v d2 &>/dev/null; then
  D2_VERSION=$(d2 --version 2>&1 | head -1)
  D2_MAJOR=$(echo "$D2_VERSION" | grep -oE '[0-9]+\.[0-9]+' | head -1)
  if [ -n "$D2_MAJOR" ]; then
    pass "D2 installed: $D2_VERSION"
  else
    warn "D2 found but could not parse version: $D2_VERSION"
  fi
else
  fail "D2 not installed. Run: brew install d2"
fi
echo ""

# --- 2. Kroki Gateway --------------------------------------------------------
echo "2. Kroki Gateway"
KROKI_URL="${KROKI_URL:-http://localhost:8000}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$KROKI_URL/health" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
  pass "Kroki healthy at $KROKI_URL (HTTP $HTTP_CODE)"
else
  warn "Kroki not reachable at $KROKI_URL (HTTP $HTTP_CODE). Start with: docker compose -f docker-compose.slides-v2.yml up -d"
fi
echo ""

# --- 3. Python packages ------------------------------------------------------
echo "3. Python Packages"

check_python_pkg() {
  local pkg="$1"
  local import_name="${2:-$1}"
  if python3 -c "import $import_name" 2>/dev/null; then
    pass "$pkg installed"
  else
    fail "$pkg not installed. Run: pip install $pkg"
  fi
}

check_python_pkg "python-pptx" "pptx"
check_python_pkg "cairosvg" "cairosvg"
check_python_pkg "plotly" "plotly"
check_python_pkg "kaleido" "kaleido"
check_python_pkg "EasyPPTX" "easypptx"
check_python_pkg "PySceneDetect" "scenedetect"
echo ""

# --- 4. Cairo native libraries -----------------------------------------------
echo "4. Cairo Native Libraries"

check_brew_pkg() {
  local pkg="$1"
  if brew list "$pkg" &>/dev/null; then
    pass "$pkg installed (brew)"
  else
    fail "$pkg not installed. Run: brew install $pkg"
  fi
}

if command -v brew &>/dev/null; then
  check_brew_pkg "cairo"
  check_brew_pkg "pango"
  check_brew_pkg "gdk-pixbuf"
  check_brew_pkg "libffi"
else
  warn "Homebrew not found. Cannot verify native Cairo dependencies."
fi
echo ""

# --- 5. SVG -> PNG conversion test -------------------------------------------
echo "5. cairosvg Render Test"
if python3 -c "import cairosvg" 2>/dev/null; then
  TEST_SVG='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="blue"/></svg>'
  TEST_PNG="/tmp/slides-v2-healthcheck-test.png"
  if python3 -c "
import cairosvg
cairosvg.svg2png(bytestring=b'$TEST_SVG', write_to='$TEST_PNG', dpi=300)
print('ok')
" 2>/dev/null; then
    pass "SVG -> PNG conversion works (DPI 300)"
    rm -f "$TEST_PNG"
  else
    fail "cairosvg SVG -> PNG conversion failed. Check native Cairo libs."
  fi
else
  fail "cairosvg not importable. Skipping render test."
fi
echo ""

# --- 6. Cache directories ----------------------------------------------------
echo "6. Cache Directories"
PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CACHE_DIR="${SLIDES_CACHE_DIR:-$PROJECT_ROOT/cache/slides-v2}"

for subdir in diagrams images videos; do
  if [ -d "$CACHE_DIR/$subdir" ]; then
    pass "Cache dir exists: $CACHE_DIR/$subdir"
  else
    fail "Cache dir missing: $CACHE_DIR/$subdir. Run: mkdir -p $CACHE_DIR/{diagrams,images,videos}"
  fi
done
echo ""

# --- 7. Environment variables ------------------------------------------------
echo "7. Environment Variables"

check_env_var() {
  local var="$1"
  local required="${2:-optional}"
  if [ -n "${!var:-}" ]; then
    pass "$var is set"
  elif [ "$required" = "required" ]; then
    fail "$var not set (required)"
  else
    warn "$var not set (optional, has fallback)"
  fi
}

check_env_var "KROKI_URL" "optional"
check_env_var "SLIDES_CACHE_DIR" "optional"
check_env_var "SLIDES_COST_CAP" "optional"
check_env_var "SLIDES_VIDEO_COST_CAP" "optional"
check_env_var "RECRAFT_API_KEY" "optional"
check_env_var "ENABLE_VISUAL_GENERATION" "optional"
check_env_var "ENABLE_ANDRAGOGIC_VALIDATION" "optional"
check_env_var "ENABLE_YOUTUBE_ENTRYPOINT" "optional"
echo ""

# --- Summary ------------------------------------------------------------------
echo "============================================"
echo " Summary: $PASS passed, $FAIL failed, $WARN warnings"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "Some checks FAILED. Fix the issues above before running the pipeline."
  exit 1
else
  echo ""
  echo "All critical checks passed. Pipeline is ready."
  exit 0
fi
