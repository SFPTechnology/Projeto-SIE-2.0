#!/bin/bash
# Copy Workflow Loop Script for Claude Code
# Executes Copy workflows by PHASES (not stories) with checkpoints
# Usage: ./copy.sh <project-dir> [max-iterations]

set -e

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COPY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$COPY_DIR/templates"
WORKFLOWS_DIR="$COPY_DIR/workflows"
REPO_ROOT="$(cd "$COPY_DIR/../.." && pwd)"
CANONICAL_PROJECTS_DIR="$REPO_ROOT/outputs/copy"
LEGACY_PROJECTS_DIR="$COPY_DIR/projects"

# Detect unbuffered output command (platform-agnostic)
if command -v stdbuf &> /dev/null; then
  UNBUFFER_CMD="stdbuf -oL"
elif command -v unbuffer &> /dev/null; then
  UNBUFFER_CMD="unbuffer"
else
  UNBUFFER_CMD=""
fi

# ═══════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════

if [[ -z "$1" ]]; then
  echo "📝 Copy Workflow Runner"
  echo ""
  echo "Usage: $0 <project-dir> [max-iterations]"
  echo ""
  echo "Examples:"
  echo "  $0 outputs/copy/launch-2024/             # Canonical full-launch root"
  echo "  $0 outputs/copy/ads-campaign/            # Canonical paid-traffic root"
  echo "  $0 outputs/copy/my-project/ 30           # Canonical root, 30 iters"
  echo ""
  echo "Project directory must contain:"
  echo "  - copy-state.json  (or will use template)"
  echo "  - progress.txt     (created if missing)"
  echo "  - prompt.md        (uses default if missing)"
  echo "  - phase folders at project root (legacy nested outputs/ still supported)"
  echo ""
  echo "Available Workflows:"
  if [[ -d "$WORKFLOWS_DIR" ]]; then
    shopt -s nullglob
    for wf in "$WORKFLOWS_DIR"/*.yaml; do
      wf_name=$(basename "$wf" .yaml)
      wf_desc=$(grep -m1 "^  name:" "$wf" 2>/dev/null | sed 's/.*name: *"\?\([^"]*\)"\?.*/\1/' || echo "")
      echo "  📋 $wf_name - $wf_desc"
    done
    shopt -u nullglob
  else
    echo "  (No workflows found in $WORKFLOWS_DIR)"
  fi
  echo ""
  echo "Active projects:"
  for scan_root in "$CANONICAL_PROJECTS_DIR" "$LEGACY_PROJECTS_DIR"; do
    [[ -d "$scan_root" ]] || continue
    find "$scan_root" -name "copy-state.json" 2>/dev/null | while read f; do
      dir=$(dirname "$f")
      project=$(cat "$f" | jq -r '.project // .project_slug // "Unknown"' 2>/dev/null)
      workflow=$(cat "$f" | jq -r '.workflow_id // .workflow // "none"' 2>/dev/null)
      phase=$(cat "$f" | jq -r '.current_phase // "PHASE-0"' 2>/dev/null)
      echo "  📁 $dir"
      echo "      Project: $project | Workflow: $workflow | Phase: $phase"
    done
  done
  exit 0
fi

PROJECT_DIR="$1"
MAX_ITERATIONS=${2:-30}

# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════

# Resolve to absolute path
if [[ ! "$PROJECT_DIR" = /* ]]; then
  PROJECT_DIR="$(pwd)/$PROJECT_DIR"
fi

# Remove trailing slash
PROJECT_DIR="${PROJECT_DIR%/}"

# Check project directory exists
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "❌ Project directory not found: $PROJECT_DIR"
  echo "   Create it first with copy-state.json or run decision matrix."
  exit 1
fi

# Workspace preflight (can be skipped with COPY_SKIP_WORKSPACE_CHECK=1)
if [[ "${COPY_SKIP_WORKSPACE_CHECK:-0}" != "1" ]]; then
  WORKSPACE_BOOTSTRAP="$SCRIPT_DIR/bootstrap-copy-workspace.sh"
  WORKSPACE_VALIDATE="$SCRIPT_DIR/validate-copy-essentials.sh"

  if [[ ! -f "$WORKSPACE_BOOTSTRAP" || ! -f "$WORKSPACE_VALIDATE" ]]; then
    echo "❌ Workspace preflight scripts are missing."
    echo "   Required: scripts/bootstrap-copy-workspace.sh + scripts/validate-copy-essentials.sh"
    exit 1
  fi

  echo "🔧 Running workspace bootstrap..."
  bash "$WORKSPACE_BOOTSTRAP"
  echo "✅ Running workspace essentials validation..."
  bash "$WORKSPACE_VALIDATE"
fi

# ═══════════════════════════════════════════════════════════════
# SETUP FILES
# ═══════════════════════════════════════════════════════════════

STATE_FILE="$PROJECT_DIR/copy-state.json"
PROGRESS_FILE="$PROJECT_DIR/progress.txt"
HANDOFF_FILE="$PROJECT_DIR/handoff.md"
LEGACY_OUTPUTS_DIR="$PROJECT_DIR/outputs"

# New projects store phase artifacts directly under PROJECT_DIR. If an existing
# project still uses nested outputs/, keep that structure for compatibility.
if [[ -d "$LEGACY_OUTPUTS_DIR" ]]; then
  OUTPUTS_DIR="$LEGACY_OUTPUTS_DIR"
else
  OUTPUTS_DIR="$PROJECT_DIR"
fi

mkdir -p "$OUTPUTS_DIR"/{diagnosis,research,foundation,planning,copy,email,testing,offer}

# Create copy-state.json if missing
if [[ ! -f "$STATE_FILE" ]]; then
  if [[ -f "$TEMPLATES_DIR/copy-state.json" ]]; then
    cp "$TEMPLATES_DIR/copy-state.json" "$STATE_FILE"
    echo "📝 Created copy-state.json from template"
  else
    # Create minimal state
    cat > "$STATE_FILE" << 'EOF'
{
  "project": "New Copy Project",
  "workflow_id": null,
  "current_phase": "PHASE-0",
  "iteration": 0,
  "tasks_completed": [],
  "artifacts": [],
  "checkpoints": [],
  "decision_matrix": {
    "awareness_level": null,
    "market_sophistication": null,
    "price_point": null,
    "traffic_temperature": null,
    "primary_output": null
  },
  "agents_used": [],
  "history": []
}
EOF
    echo "📝 Created minimal copy-state.json"
  fi
fi

# Create progress.txt if missing
if [[ ! -f "$PROGRESS_FILE" ]]; then
  if [[ -f "$TEMPLATES_DIR/progress-copy.txt" ]]; then
    cp "$TEMPLATES_DIR/progress-copy.txt" "$PROGRESS_FILE"
    sed -i '' "s/YYYY-MM-DD/$(date +%Y-%m-%d)/g" "$PROGRESS_FILE" 2>/dev/null || true
    echo "📝 Created progress.txt from template"
  else
    cat > "$PROGRESS_FILE" << EOF
# Copy Project Progress
Started: $(date +%Y-%m-%d)

## Phase Progress
- [ ] PHASE-1: Foundation
- [ ] PHASE-2: Strategy
- [ ] PHASE-3: Execution
- [ ] PHASE-4: Optimization

## Artifacts Generated
(none yet)

## Session Log
EOF
    echo "📝 Created minimal progress.txt"
  fi
fi

# Use project prompt.md or default
if [[ -f "$PROJECT_DIR/prompt.md" ]]; then
  PROMPT_FILE="$PROJECT_DIR/prompt.md"
elif [[ -f "$TEMPLATES_DIR/prompt-copy.md" ]]; then
  PROMPT_FILE="$TEMPLATES_DIR/prompt-copy.md"
else
  echo "⚠️  No prompt.md found, using inline prompt"
  PROMPT_FILE=""
fi

# Get project info from state
PROJECT_NAME=$(cat "$STATE_FILE" | jq -r '.project // "Unknown Project"' 2>/dev/null)
WORKFLOW_ID=$(cat "$STATE_FILE" | jq -r '.workflow_id // "none"' 2>/dev/null)
CURRENT_PHASE=$(cat "$STATE_FILE" | jq -r '.current_phase // "PHASE-0"' 2>/dev/null)

# ═══════════════════════════════════════════════════════════════
# SHOW STATUS
# ═══════════════════════════════════════════════════════════════

echo ""
echo "📝 Copy Workflow Runner"
echo "═══════════════════════════════════════════════════════════"
echo "   Project:    $PROJECT_NAME"
echo "   Directory:  $PROJECT_DIR"
echo "   Workflow:   $WORKFLOW_ID"
echo "   Phase:      $CURRENT_PHASE"
echo "   State:      $STATE_FILE"
echo "   Progress:   $PROGRESS_FILE"
echo "   Handoff:    $HANDOFF_FILE"
echo "   Artifacts:  $OUTPUTS_DIR"
echo "   Max iters:  $MAX_ITERATIONS"
if [[ -n "$UNBUFFER_CMD" ]]; then
  echo "   Streaming:  ✅ Real-time ($UNBUFFER_CMD)"
else
  echo "   Streaming:  ⚠️  Buffered (install 'expect' for real-time)"
fi
echo "═══════════════════════════════════════════════════════════"
echo ""

# Show tasks completed
TASKS_DONE=$(cat "$STATE_FILE" | jq -r '.tasks_completed | length' 2>/dev/null)
echo "📋 Progress: $TASKS_DONE tasks completed"
cat "$STATE_FILE" | jq -r '.tasks_completed[]? // empty' 2>/dev/null | while read task; do
  echo "   ✅ $task"
done
echo ""

# Show artifacts generated
ARTIFACTS=$(cat "$STATE_FILE" | jq -r '.artifacts | length' 2>/dev/null)
if [[ "$ARTIFACTS" -gt 0 ]]; then
  echo "📄 Artifacts: $ARTIFACTS generated"
  cat "$STATE_FILE" | jq -r '.artifacts[]?.name // empty' 2>/dev/null | while read art; do
    echo "   📄 $art"
  done
  echo ""
fi

# ═══════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "═══════════════════════════════════════"
  echo "═══ Iteration $i of $MAX_ITERATIONS ═══"
  echo "═══════════════════════════════════════"

  # Read current state
  CURRENT_PHASE=$(cat "$STATE_FILE" | jq -r '.current_phase // "PHASE-0"' 2>/dev/null)
  WORKFLOW_ID=$(cat "$STATE_FILE" | jq -r '.workflow_id // "none"' 2>/dev/null)

  echo "🎯 Current Phase: $CURRENT_PHASE"
  echo "📋 Workflow: $WORKFLOW_ID"

  # Timestamp start
  ITER_START=$(date +%s)
  echo "⏱️  Started: $(date +%H:%M:%S)"
  echo ""

  # Export environment variables for tracking
  export COPY_ITERATION=$i
  export COPY_PHASE="$CURRENT_PHASE"
  export COPY_WORKFLOW="$WORKFLOW_ID"
  export COPY_PROJECT_DIR="$PROJECT_DIR"

  # Build the prompt with project context
  if [[ -n "$PROMPT_FILE" && -f "$PROMPT_FILE" ]]; then
    FULL_PROMPT="PROJECT_DIR=$PROJECT_DIR
STATE_FILE=$STATE_FILE
PROGRESS_FILE=$PROGRESS_FILE
HANDOFF_FILE=$HANDOFF_FILE
OUTPUTS_DIR=$OUTPUTS_DIR
WORKFLOWS_DIR=$WORKFLOWS_DIR
CURRENT_PHASE=$CURRENT_PHASE
WORKFLOW_ID=$WORKFLOW_ID
ITERATION=$i

$(cat $PROMPT_FILE)"
  else
    # Inline prompt if no file
    FULL_PROMPT="PROJECT_DIR=$PROJECT_DIR
STATE_FILE=$STATE_FILE
PROGRESS_FILE=$PROGRESS_FILE
HANDOFF_FILE=$HANDOFF_FILE
OUTPUTS_DIR=$OUTPUTS_DIR
WORKFLOWS_DIR=$WORKFLOWS_DIR
CURRENT_PHASE=$CURRENT_PHASE
WORKFLOW_ID=$WORKFLOW_ID
ITERATION=$i

Execute the Copy workflow phase. Read copy-state.json first, then:
1. If workflow_id is null, run decision matrix to select workflow
2. Execute current phase tasks using appropriate agents
3. Update copy-state.json with progress
4. When phase complete, emit <promise>CHECKPOINT:PHASE-X</promise>
5. When all phases complete, emit <promise>COMPLETE</promise>

If blocked, emit <promise>BLOCKED:reason</promise>"
  fi

  # Run Claude Code with the prompt
  echo "─────────────────────────────────────"
  if [[ -n "$UNBUFFER_CMD" ]]; then
    OUTPUT=$($UNBUFFER_CMD claude -p --dangerously-skip-permissions "$FULL_PROMPT" 2>&1 | tee /dev/stderr) || true
  else
    OUTPUT=$(claude -p --dangerously-skip-permissions "$FULL_PROMPT" 2>&1 | tee /dev/stderr) || true
  fi
  echo "─────────────────────────────────────"

  # Calculate iteration duration
  ITER_END=$(date +%s)
  ITER_DURATION=$((ITER_END - ITER_START))
  ITER_MINS=$((ITER_DURATION / 60))
  ITER_SECS=$((ITER_DURATION % 60))

  echo ""
  echo "⏱️  Completed: $(date +%H:%M:%S) (${ITER_MINS}m ${ITER_SECS}s)"

  # Update iteration count in state
  jq --argjson iter "$i" '.iteration = $iter' "$STATE_FILE" > /tmp/copy_state_update.json
  mv /tmp/copy_state_update.json "$STATE_FILE"

  # Check for checkpoint signal
  if echo "$OUTPUT" | grep -qE "<promise>CHECKPOINT:PHASE-[0-9]+</promise>"; then
    CHECKPOINT_PHASE=$(echo "$OUTPUT" | grep -oE "CHECKPOINT:PHASE-[0-9]+" | head -1 | sed 's/CHECKPOINT://')
    echo ""
    echo "═══════════════════════════════════════"
    echo "🔄 Checkpoint: $CHECKPOINT_PHASE"
    echo "═══════════════════════════════════════"

    # Add checkpoint to state
    jq --arg cp "$CHECKPOINT_PHASE" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      '.checkpoints += [{"phase": $cp, "timestamp": $ts}]' "$STATE_FILE" > /tmp/copy_state_update.json
    mv /tmp/copy_state_update.json "$STATE_FILE"

    # Log checkpoint
    echo "" >> "$PROGRESS_FILE"
    echo "### Checkpoint: $CHECKPOINT_PHASE - $(date +%Y-%m-%d\ %H:%M:%S)" >> "$PROGRESS_FILE"

    echo "   ✅ Checkpoint recorded"
  fi

  # Check for blocked signal
  if echo "$OUTPUT" | grep -qE "<promise>BLOCKED:"; then
    BLOCKED_REASON=$(echo "$OUTPUT" | grep -oE "BLOCKED:[^<]+" | head -1 | sed 's/BLOCKED://')
    echo ""
    echo "═══════════════════════════════════════"
    echo "⛔ BLOCKED: $BLOCKED_REASON"
    echo "═══════════════════════════════════════"

    # Log block
    echo "" >> "$PROGRESS_FILE"
    echo "### BLOCKED: $BLOCKED_REASON - $(date +%Y-%m-%d\ %H:%M:%S)" >> "$PROGRESS_FILE"

    echo "   Review and resolve blocker manually."
    exit 2
  fi

  # Check for completion signal
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "═══════════════════════════════════════"
    echo "✅ Workflow Complete!"
    echo "═══════════════════════════════════════"
    echo "   Project:    $PROJECT_NAME"
    echo "   Workflow:   $WORKFLOW_ID"
    echo "   Iterations: $i"
    echo "   Finished:   $(date +%H:%M:%S)"

    # Mark completion in progress file
    echo "" >> "$PROGRESS_FILE"
    echo "## COMPLETED: $(date +%Y-%m-%d)" >> "$PROGRESS_FILE"

    # Show artifacts
    echo ""
    echo "📄 Generated Artifacts:"
    cat "$STATE_FILE" | jq -r '.artifacts[]? | "   📄 \(.name): \(.path)"' 2>/dev/null || echo "   (none recorded)"

    exit 0
  fi

  # Show updated status
  echo ""
  TASKS_DONE=$(cat "$STATE_FILE" | jq -r '.tasks_completed | length' 2>/dev/null)
  CHECKPOINTS=$(cat "$STATE_FILE" | jq -r '.checkpoints | length' 2>/dev/null)
  echo "📊 Status: $TASKS_DONE tasks | $CHECKPOINTS checkpoints"

  # Brief pause between iterations
  echo ""
  echo "⏳ Waiting 2 seconds before next iteration..."
  sleep 2
done

echo ""
echo "⚠️  Max iterations ($MAX_ITERATIONS) reached"
echo "   Project: $PROJECT_NAME"
echo "   Workflow may be incomplete."
echo ""
echo "   Check status:"
echo "   cat $STATE_FILE | jq '.'"
exit 1
