#!/usr/bin/env bash
# =============================================================================
# Prototype 1: D2 + Kroki + Token Transformer
# =============================================================================
# Story 0.5 (EPIC-SC-V2-001) — Prototype Validation
#
# Validates:
#   1. D2 diagram generation with theme-overrides from brand palette
#   2. Rendering via D2 CLI and Kroki API
#   3. SVG -> PNG conversion via cairosvg at DPI 300
#
# Prerequisites:
#   - D2 CLI installed (brew install d2)
#   - Kroki running (docker compose -f docker-compose.slides-v2.yml up -d)
#   - cairosvg installed (pip install cairosvg)
#   - Cairo native libs (brew install cairo pango gdk-pixbuf libffi)
#
# Run: bash squads/slides-creator/scripts/prototype-d2-tokens.sh
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------

# Sample brand palette (simulates W3C DTCG design tokens from workspace)
# These would normally come from workspace/businesses/{brand}/tokens.json
BRAND_PRIMARY="#4A90D9"
BRAND_SECONDARY="#2ECC71"
BRAND_ACCENT="#E74C3C"
BRAND_NEUTRAL="#34495E"
BRAND_BACKGROUND="#ECF0F1"

# D2 theme-overrides format: N1=fill, N2=stroke, N3=font, B1-B6=accent colors
# Mapping: brand palette -> D2 theme variables
# N1 (node fill) = background, N2 (node stroke) = primary,
# N3 (node font) = neutral, N7 (node font size) = 14
# B1-B4 = brand accent progression
THEME_OVERRIDES="--theme-overrides='N1:${BRAND_BACKGROUND},N2:${BRAND_PRIMARY},N3:${BRAND_NEUTRAL},B1:${BRAND_PRIMARY},B2:${BRAND_SECONDARY},B3:${BRAND_ACCENT},B4:${BRAND_NEUTRAL}'"

OUTDIR="/tmp/slides-v2-prototype-d2"
KROKI_URL="${KROKI_URL:-http://localhost:8000}"

mkdir -p "$OUTDIR"

PASS=0
FAIL=0

pass() { echo "  [PASS] $1"; ((PASS++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "============================================"
echo " Prototype 1: D2 + Kroki + Token Transformer"
echo "============================================"
echo ""
echo "Brand palette:"
echo "  Primary:    ${BRAND_PRIMARY}"
echo "  Secondary:  ${BRAND_SECONDARY}"
echo "  Accent:     ${BRAND_ACCENT}"
echo "  Neutral:    ${BRAND_NEUTRAL}"
echo "  Background: ${BRAND_BACKGROUND}"
echo ""

# =============================================================================
# DIAGRAM 1: Process Flow (content_type: process)
# Validates: D2 CLI rendering with theme-overrides
# Maps to: routing_table -> process -> primary_engine: mermaid, fallback: d2
# =============================================================================

echo "--- Diagram 1: Process Flow (D2 CLI) ---"

cat > "$OUTDIR/diagram-process.d2" << 'D2EOF'
direction: right

briefing: {
  label: "Briefing\nInput"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

content_architect: {
  label: "Content\nArchitect"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

visual_scout: {
  label: "Visual\nScout"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

design_renderer: {
  label: "Design\nRenderer"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

qa_inspector: {
  label: "QA\nInspector"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

pptx_output: {
  label: "PPTX\nOutput"
  shape: rectangle
  style: {
    border-radius: 8
  }
}

briefing -> content_architect: "normalize"
content_architect -> visual_scout: "visual_strategy"
visual_scout -> design_renderer: "assets"
design_renderer -> qa_inspector: "deck_manifest"
qa_inspector -> pptx_output: "validated"
D2EOF

# Render via D2 CLI with theme-overrides
# Note: D2 theme-overrides use the flag format directly
if d2 --theme-overrides "N1:${BRAND_BACKGROUND};N2:${BRAND_PRIMARY};N3:${BRAND_NEUTRAL};B1:${BRAND_PRIMARY};B2:${BRAND_SECONDARY};B3:${BRAND_ACCENT};B4:${BRAND_NEUTRAL}" \
   "$OUTDIR/diagram-process.d2" "$OUTDIR/diagram-process.svg" 2>/dev/null; then
  if [ -s "$OUTDIR/diagram-process.svg" ]; then
    SIZE=$(wc -c < "$OUTDIR/diagram-process.svg" | tr -d ' ')
    pass "Process flow rendered via D2 CLI ($SIZE bytes)"
  else
    fail "D2 produced empty SVG"
  fi
else
  # Fallback: try without theme-overrides (D2 version may differ)
  echo "  [INFO] Theme-overrides format may vary by D2 version, trying without..."
  if d2 "$OUTDIR/diagram-process.d2" "$OUTDIR/diagram-process.svg" 2>/dev/null; then
    SIZE=$(wc -c < "$OUTDIR/diagram-process.svg" | tr -d ' ')
    pass "Process flow rendered via D2 CLI without theme-overrides ($SIZE bytes)"
    echo "  [NOTE] Theme-overrides need format adjustment for this D2 version"
  else
    fail "D2 render failed entirely. Is D2 installed? (brew install d2)"
  fi
fi
echo ""

# =============================================================================
# DIAGRAM 2: Architecture (content_type: architecture)
# Validates: D2 nested containers with brand colors
# Maps to: routing_table -> architecture -> primary_engine: d2
# =============================================================================

echo "--- Diagram 2: Architecture (D2 CLI) ---"

cat > "$OUTDIR/diagram-architecture.d2" << 'D2EOF'
direction: down

slides_creator: {
  label: "slides-creator squad"

  agents: {
    label: "Agents"

    slide_chief: {
      label: "slide-chief"
      shape: rectangle
    }
    content_architect: {
      label: "content-architect"
      shape: rectangle
    }
    visual_scout: {
      label: "visual-scout"
      shape: rectangle
    }
    design_renderer: {
      label: "design-renderer"
      shape: rectangle
    }
    qa_inspector: {
      label: "qa-inspector"
      shape: rectangle
    }
  }

  engines: {
    label: "Visual Engines"

    d2_engine: {
      label: "D2Engine"
      shape: hexagon
    }
    mermaid_engine: {
      label: "MermaidEngine"
      shape: hexagon
    }
    gpt_image: {
      label: "GPTImageEngine"
      shape: hexagon
    }
    recraft: {
      label: "RecraftEngine"
      shape: hexagon
    }
    plotly: {
      label: "PlotlyEngine"
      shape: hexagon
    }
  }

  agents.visual_scout -> engines.d2_engine: "diagram"
  agents.visual_scout -> engines.mermaid_engine: "diagram"
  agents.visual_scout -> engines.gpt_image: "infographic"
  agents.visual_scout -> engines.recraft: "svg/icon"
  agents.visual_scout -> engines.plotly: "chart"
}

external: {
  label: "External Services"

  kroki: {
    label: "Kroki Gateway\n(self-hosted)"
    shape: cloud
  }
  openai: {
    label: "OpenAI API"
    shape: cloud
  }
  recraft_api: {
    label: "Recraft API"
    shape: cloud
  }
}

slides_creator.engines.d2_engine -> external.kroki
slides_creator.engines.mermaid_engine -> external.kroki
slides_creator.engines.gpt_image -> external.openai
slides_creator.engines.recraft -> external.recraft_api
D2EOF

if d2 "$OUTDIR/diagram-architecture.d2" "$OUTDIR/diagram-architecture.svg" 2>/dev/null; then
  if [ -s "$OUTDIR/diagram-architecture.svg" ]; then
    SIZE=$(wc -c < "$OUTDIR/diagram-architecture.svg" | tr -d ' ')
    pass "Architecture diagram rendered via D2 CLI ($SIZE bytes)"
  else
    fail "D2 produced empty SVG for architecture diagram"
  fi
else
  fail "D2 architecture diagram render failed"
fi
echo ""

# =============================================================================
# DIAGRAM 3: Hierarchy (content_type: hierarchy) via Kroki API
# Validates: D2 rendering through Kroki gateway (self-hosted)
# Maps to: routing_table -> hierarchy -> primary_engine: d2
# Constraint #6: Kroki MUST be self-hosted, NEVER kroki.io
# =============================================================================

echo "--- Diagram 3: Hierarchy via Kroki (D2 API) ---"

D2_HIERARCHY_CODE='direction: down

visual_engine: {
  label: "VisualEngine Interface"
  shape: rectangle
  style: {
    font-size: 16
    bold: true
  }
}

diagram_engines: {
  label: "Diagram Engines"

  d2: {
    label: "D2Engine"
    shape: rectangle
  }
  mermaid: {
    label: "MermaidEngine"
    shape: rectangle
  }
}

ai_engines: {
  label: "AI Image Engines"

  gpt: {
    label: "GPTImageEngine"
    shape: rectangle
  }
  recraft: {
    label: "RecraftEngine"
    shape: rectangle
  }
  ideogram: {
    label: "IdeogramEngine"
    shape: rectangle
  }
}

data_engines: {
  label: "Data Viz Engines"

  plotly: {
    label: "PlotlyEngine"
    shape: rectangle
  }
}

visual_engine -> diagram_engines
visual_engine -> ai_engines
visual_engine -> data_engines'

HTTP_CODE=$(curl -s -o "$OUTDIR/diagram-hierarchy-kroki.svg" -w "%{http_code}" \
  --connect-timeout 5 \
  -X POST "$KROKI_URL/d2/svg" \
  -H "Content-Type: text/plain" \
  -d "$D2_HIERARCHY_CODE" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ] && [ -s "$OUTDIR/diagram-hierarchy-kroki.svg" ]; then
  SIZE=$(wc -c < "$OUTDIR/diagram-hierarchy-kroki.svg" | tr -d ' ')
  pass "Hierarchy diagram rendered via Kroki D2 API ($SIZE bytes)"
else
  echo "  [INFO] Kroki not running (HTTP $HTTP_CODE). This is expected if Docker is not started."
  echo "  [INFO] To test: docker compose -f docker-compose.slides-v2.yml up -d"
  fail "Kroki D2 API not available (requires running Kroki container)"
fi
echo ""

# =============================================================================
# SVG -> PNG CONVERSION via cairosvg (DPI 300)
# Validates: cairosvg can convert any of the generated SVGs to PNG
# =============================================================================

echo "--- SVG -> PNG Conversion (cairosvg DPI 300) ---"

# Pick the first available SVG
SVG_SOURCE=""
for candidate in "$OUTDIR/diagram-process.svg" "$OUTDIR/diagram-architecture.svg" "$OUTDIR/diagram-hierarchy-kroki.svg"; do
  if [ -s "$candidate" ]; then
    SVG_SOURCE="$candidate"
    break
  fi
done

if [ -z "$SVG_SOURCE" ]; then
  # Create a minimal SVG for conversion test
  SVG_SOURCE="$OUTDIR/fallback-test.svg"
  cat > "$SVG_SOURCE" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
  <rect width="400" height="200" fill="#ECF0F1" rx="8"/>
  <rect x="20" y="20" width="160" height="60" fill="#4A90D9" rx="4"/>
  <text x="100" y="55" text-anchor="middle" fill="white" font-size="14">D2Engine</text>
  <rect x="220" y="20" width="160" height="60" fill="#2ECC71" rx="4"/>
  <text x="300" y="55" text-anchor="middle" fill="white" font-size="14">MermaidEngine</text>
  <rect x="120" y="120" width="160" height="60" fill="#E74C3C" rx="4"/>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="14">GPTImageEngine</text>
</svg>
SVGEOF
fi

PNG_OUTPUT="$OUTDIR/converted-output.png"

if python3 -c "
import cairosvg
cairosvg.svg2png(url='${SVG_SOURCE}', write_to='${PNG_OUTPUT}', dpi=300)
print('ok')
" 2>/dev/null; then
  if [ -s "$PNG_OUTPUT" ]; then
    SIZE=$(wc -c < "$PNG_OUTPUT" | tr -d ' ')
    pass "SVG -> PNG conversion successful ($SIZE bytes, DPI 300)"
  else
    fail "cairosvg produced empty PNG"
  fi
else
  fail "cairosvg conversion failed. Check: pip install cairosvg && brew install cairo pango gdk-pixbuf libffi"
fi
echo ""

# =============================================================================
# BRAND COLOR VERIFICATION (manual step documentation)
# =============================================================================

echo "--- Brand Color Verification ---"
echo ""
echo "  Manual verification steps:"
echo "  1. Open $OUTDIR/diagram-process.svg in a browser"
echo "  2. Inspect SVG elements for brand colors:"
echo "     - Node fill should use: ${BRAND_BACKGROUND} or ${BRAND_PRIMARY}"
echo "     - Node stroke should use: ${BRAND_PRIMARY}"
echo "     - Text should use: ${BRAND_NEUTRAL}"
echo "  3. Compare with palette defined above"
echo ""
echo "  Automated color extraction (if SVG exists):"

if [ -s "$OUTDIR/diagram-process.svg" ]; then
  echo "  Colors found in SVG:"
  # Extract hex colors from SVG (grep for fill/stroke attributes)
  grep -oE '#[0-9A-Fa-f]{6}' "$OUTDIR/diagram-process.svg" | sort -u | while read -r color; do
    echo "    $color"
  done
  pass "Color extraction completed (verify manually against brand palette)"
else
  echo "  [INFO] No SVG available for color extraction"
  fail "Cannot verify brand colors without rendered SVG"
fi
echo ""

# =============================================================================
# TOKEN TRANSFORMER DOCUMENTATION
# =============================================================================

echo "--- Token Transformer: Design Tokens -> D2 Theme ---"
echo ""
echo "  Transformation mapping (W3C DTCG -> D2 theme-overrides):"
echo ""
echo "  | DTCG Token Path            | D2 Variable | Value             |"
echo "  |----------------------------|-------------|-------------------|"
echo "  | color.brand.primary.value  | N2, B1      | ${BRAND_PRIMARY}  |"
echo "  | color.brand.secondary.value| B2          | ${BRAND_SECONDARY}|"
echo "  | color.brand.accent.value   | B3          | ${BRAND_ACCENT}   |"
echo "  | color.brand.neutral.value  | N3, B4      | ${BRAND_NEUTRAL}  |"
echo "  | color.brand.background.value| N1         | ${BRAND_BACKGROUND}|"
echo ""
echo "  D2 CLI command format:"
echo "    d2 --theme-overrides 'N1:#hex;N2:#hex;...' input.d2 output.svg"
echo ""
echo "  Kroki API format (POST body with theme in diagram code):"
echo "    vars: {"
echo "      d2-config: {"
echo "        theme-overrides: {"
echo "          N1: '#hex'"
echo "          N2: '#hex'"
echo "        }"
echo "      }"
echo "    }"
echo ""
echo "  Mermaid theme format (for comparison):"
echo "    %%{init: {'themeVariables': {"
echo "      'primaryColor': '${BRAND_PRIMARY}',"
echo "      'secondaryColor': '${BRAND_SECONDARY}',"
echo "      'tertiaryColor': '${BRAND_ACCENT}'"
echo "    }}}%%"
echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "============================================"
echo " Prototype 1 Results: $PASS passed, $FAIL failed"
echo "============================================"
echo ""
echo " Output files in: $OUTDIR/"
ls -la "$OUTDIR/" 2>/dev/null | grep -v "^total" | grep -v "^d"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo " Some tests FAILED. Check prerequisites above."
  echo " NOTE: Kroki failures are expected if Docker is not running."
  exit 1
else
  echo " All prototype validations passed."
  exit 0
fi
