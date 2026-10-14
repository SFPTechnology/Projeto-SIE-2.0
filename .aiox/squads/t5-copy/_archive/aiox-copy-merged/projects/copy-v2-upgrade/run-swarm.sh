#!/bin/bash
# Copy Framework v2.0 - Swarm Runner (wrapper)
# Usage: ./run-swarm.sh [workers]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUM_WORKERS=${1:-8}

# Use canonical Ralph tmux swarm script
# NOTE: This script delegates to the ralph squad tmux swarm runner (external repo: mmos/squads/ralph/scripts/ralph-tmux-swarm.sh)
# Set RALPH_SWARM_SCRIPT env var or update this path to point to your local copy.
RALPH_SWARM_SCRIPT="${RALPH_SWARM_SCRIPT:-$(git rev-parse --show-toplevel 2>/dev/null)/../mmos/squads/ralph/scripts/ralph-tmux-swarm.sh}"
exec "$RALPH_SWARM_SCRIPT" "$SCRIPT_DIR" "$NUM_WORKERS"
