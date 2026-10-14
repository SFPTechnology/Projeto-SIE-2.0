#!/usr/bin/env bash
# run-deep-research-bench.sh — Execute AIOX /tech-research against Deep Research Bench tasks
#
# Origin: STORY-153.7 (EPIC-153)
#
# Modes:
#   --pilot 5     Run first N tasks (default 5, ~$1-3 USD)
#   --full        Run all tasks (~$5-15 USD, ~1-2h)
#   --dry-run     Show what would be executed
#
# Each task -> 1 .jsonl in task-runs/
# Aggregate via scripts/aggregate-scores.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMISSION_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || cd "$SCRIPT_DIR/../../../.." && pwd)"
BENCH_DIR="$REPO_ROOT/../bench/deep-research-bench"
TASK_RUNS_DIR="$SUBMISSION_DIR/task-runs"

MODE="pilot"
PILOT_COUNT=5
DRY_RUN=false
BUDGET_CAP_USD=20.00

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pilot)
      MODE="pilot"
      if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
        PILOT_COUNT="$2"
        shift
      fi
      shift
      ;;
    --full) MODE="full"; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --budget) BUDGET_CAP_USD="$2"; shift 2 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 3 ;;
  esac
done

if [[ ! -d "$BENCH_DIR" ]]; then
  echo "ERROR: Bench not cloned at $BENCH_DIR" >&2
  echo "  Run: bash $SCRIPT_DIR/clone-bench.sh" >&2
  exit 1
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "ERROR: ANTHROPIC_API_KEY not set" >&2
  exit 3
fi

mkdir -p "$TASK_RUNS_DIR"

TASKS_FILE="$BENCH_DIR/tasks.jsonl"
if [[ ! -f "$TASKS_FILE" ]]; then
  TASKS_FILE="$(find "$BENCH_DIR" -name "tasks.jsonl" -o -name "queries.jsonl" -o -name "questions.jsonl" 2>/dev/null | head -1)"
fi

if [[ -z "$TASKS_FILE" || ! -f "$TASKS_FILE" ]]; then
  echo "ERROR: Cannot find tasks file in $BENCH_DIR" >&2
  echo "  Inspect bench structure after clone and update this script." >&2
  exit 1
fi

TOTAL_TASKS="$(wc -l < "$TASKS_FILE")"

if [[ "$MODE" == "pilot" ]]; then
  N_TASKS="$PILOT_COUNT"
else
  N_TASKS="$TOTAL_TASKS"
fi

echo "==========================================================="
echo "  AIOX Research x Deep Research Bench - RUN"
echo "==========================================================="
echo "  Mode:          $MODE"
echo "  Tasks to run:  $N_TASKS / $TOTAL_TASKS"
echo "  Budget cap:    \$${BUDGET_CAP_USD} USD"
echo "  Bench:         $BENCH_DIR"
echo "  Bench SHA:     $(git -C "$BENCH_DIR" rev-parse HEAD)"
echo "  Output:        $TASK_RUNS_DIR"
echo "  Dry run:       $DRY_RUN"
echo "==========================================================="
echo

if [[ "$DRY_RUN" == true ]]; then
  echo "DRY-RUN: would execute $N_TASKS tasks. Exiting."
  exit 0
fi

EXECUTED=0
START_TIME="$(date +%s)"

while IFS= read -r task_line && [[ $EXECUTED -lt $N_TASKS ]]; do
  TASK_ID="$(echo "$task_line" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('id','task-'+str($EXECUTED+1)))")"
  TASK_PROMPT="$(echo "$task_line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('prompt') or d.get('query') or d.get('question',''))")"

  echo "[$((EXECUTED+1))/$N_TASKS] Task: $TASK_ID"
  echo "  Prompt: ${TASK_PROMPT:0:80}..."

  TASK_OUT="$TASK_RUNS_DIR/${TASK_ID}.jsonl"
  TASK_START="$(date +%s)"

  # TODO: invocar /tech-research --yolo via claude CLI
  # claude -p "/tech-research \"$TASK_PROMPT\" --yolo" \
  #   --model claude-sonnet-4-6 \
  #   --max-turns 50 \
  #   --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash" \
  #   --dangerously-skip-permissions \
  #   > "$TASK_OUT.raw" 2>&1

  echo "  WARN: Run real nao implementado nesta scaffold (STORY-153.7 wave deferred)"
  echo "  Estimated cost per task: \$0.10-0.30"

  TASK_END="$(date +%s)"
  TASK_DURATION=$((TASK_END - TASK_START))

  python3 -c "
import json
print(json.dumps({
  'task_id': '$TASK_ID',
  'prompt_preview': '${TASK_PROMPT:0:80}',
  'status': 'scaffold_placeholder',
  'score': None,
  'cost_usd': 0,
  'wall_time_sec': $TASK_DURATION,
  'note': 'Run real desabilitado. Implementar invocacao /tech-research aqui.'
}))" >> "$TASK_OUT"

  EXECUTED=$((EXECUTED + 1))
done < "$TASKS_FILE"

END_TIME="$(date +%s)"
TOTAL_DURATION=$((END_TIME - START_TIME))

echo
echo "==========================================================="
echo "  COMPLETE"
echo "==========================================================="
echo "  Executed:      $EXECUTED tasks"
echo "  Wall time:     ${TOTAL_DURATION}s"
echo "  Output files:  $TASK_RUNS_DIR/*.jsonl"
echo
echo "Next: python3 $SCRIPT_DIR/aggregate-scores.py $([[ "$MODE" == "pilot" ]] && echo "--pilot" || echo "")"
