#!/usr/bin/env bash
# =============================================================================
# Slides Creator v2 — Render Tests
# =============================================================================
# Validates D2 -> SVG, Mermaid via Kroki, and SVG -> PNG via cairosvg.
# Run: bash squads/slides-creator/scripts/test-renders-v2.sh
#
# Prerequisites:
#   - D2 CLI installed (brew install d2)
#   - Kroki running (docker compose -f docker-compose.slides-v2.yml up -d)
#   - cairosvg installed (pip install cairosvg)
#   - Cairo native libs (brew install cairo pango gdk-pixbuf libffi)
# =============================================================================

set -euo pipefail

PASS=0
FAIL=0
TMPDIR="/tmp/slides-v2-render-tests"
mkdir -p "$TMPDIR"

pass() { echo "  [PASS] $1"; ((PASS++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "============================================"
echo " Slides Creator v2 — Render Tests"
echo "============================================"
echo ""

# --- Test 1: D2 -> SVG -------------------------------------------------------
echo "1. D2 -> SVG"
cat > "$TMPDIR/test.d2" << 'D2EOF'
direction: right
slides-creator: {
  label: "Slides Creator v2"
  shape: rectangle
}
visual-engine: {
  label: "Visual Engine"
  shape: rectangle
}
slides-creator -> visual-engine: "renders"
D2EOF

if d2 "$TMPDIR/test.d2" "$TMPDIR/test-d2.svg" 2>/dev/null; then
  if [ -s "$TMPDIR/test-d2.svg" ]; then
    SIZE=$(wc -c < "$TMPDIR/test-d2.svg" | tr -d ' ')
    pass "D2 -> SVG rendered successfully ($SIZE bytes): $TMPDIR/test-d2.svg"
  else
    fail "D2 produced empty SVG file"
  fi
else
  fail "D2 render failed. Is D2 installed? (brew install d2)"
fi
echo ""

# --- Test 2: Mermaid via Kroki ------------------------------------------------
echo "2. Mermaid via Kroki"
KROKI_URL="${KROKI_URL:-http://localhost:8000}"

MERMAID_DIAGRAM='graph TD
    A[Briefing] --> B[Content Architect]
    B --> C[Visual Scout]
    C --> D[Design Renderer]
    D --> E[QA Inspector]'

HTTP_CODE=$(curl -s -o "$TMPDIR/test-mermaid.svg" -w "%{http_code}" \
  --connect-timeout 5 \
  -X POST "$KROKI_URL/mermaid/svg" \
  -H "Content-Type: text/plain" \
  -d "$MERMAID_DIAGRAM" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ] && [ -s "$TMPDIR/test-mermaid.svg" ]; then
  SIZE=$(wc -c < "$TMPDIR/test-mermaid.svg" | tr -d ' ')
  pass "Mermaid via Kroki rendered successfully ($SIZE bytes): $TMPDIR/test-mermaid.svg"
else
  fail "Mermaid via Kroki failed (HTTP $HTTP_CODE). Is Kroki running? (docker compose -f docker-compose.slides-v2.yml up -d)"
fi
echo ""

# --- Test 3: SVG -> PNG via cairosvg ------------------------------------------
echo "3. SVG -> PNG via cairosvg (DPI 300)"

# Use either the D2-rendered SVG or a minimal inline SVG
if [ -s "$TMPDIR/test-d2.svg" ]; then
  SVG_SOURCE="$TMPDIR/test-d2.svg"
else
  SVG_SOURCE="$TMPDIR/test-inline.svg"
  cat > "$SVG_SOURCE" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">
  <rect width="200" height="100" fill="#4A90D9" rx="8"/>
  <text x="100" y="55" text-anchor="middle" fill="white" font-size="16">Test SVG</text>
</svg>
SVGEOF
fi

if python3 -c "
import cairosvg
cairosvg.svg2png(url='$SVG_SOURCE', write_to='$TMPDIR/test-output.png', dpi=300)
print('ok')
" 2>/dev/null; then
  if [ -s "$TMPDIR/test-output.png" ]; then
    SIZE=$(wc -c < "$TMPDIR/test-output.png" | tr -d ' ')
    pass "SVG -> PNG conversion successful ($SIZE bytes, DPI 300): $TMPDIR/test-output.png"
  else
    fail "cairosvg produced empty PNG"
  fi
else
  fail "cairosvg conversion failed. Check: brew install cairo pango gdk-pixbuf libffi && pip install cairosvg"
fi
echo ""

# --- Summary ------------------------------------------------------------------
echo "============================================"
echo " Render Tests: $PASS passed, $FAIL failed"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "Some render tests FAILED. Fix the issues above."
  exit 1
else
  echo ""
  echo "All render tests passed. Visual pipeline is operational."
  exit 0
fi
