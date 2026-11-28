#!/usr/bin/env bash
set -euo pipefail

# Selective per-agent installer for Skill Agent (Linux / macOS)
# Usage: ./install.sh <target_dir> <agent_name>
# Example: ./install.sh . antigravity

if [ $# -lt 2 ]; then
  echo "Usage: ./install.sh <target_dir> <agent_name>"
  echo "Agents: antigravity | claude | opencode | codex | gemini | cursor | cursor-legacy | windsurf | cline | roo | copilot | all"
  exit 1
fi

TARGET_DIR="$1"
AGENT="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "${SCRIPT_DIR}/scripts/setup_skill.py" "${TARGET_DIR}" --agent "${AGENT}" --force --sync-global
