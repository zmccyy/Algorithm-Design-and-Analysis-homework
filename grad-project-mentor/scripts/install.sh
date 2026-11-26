#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
root="$(dirname "$here")"
src="$root/skills"
license="$root/LICENSE"
target="${1:-both}"

install_to() {
  local dest="$1"
  mkdir -p "$dest"
  cp -R "$src"/. "$dest"/
  cp "$license" "$dest/LICENSE-grad-project-mentor.txt"
  echo "Installed grad-project-mentor skills -> $dest"
}

case "$target" in
  claude) install_to "$HOME/.claude/skills" ;;
  codex) install_to "$HOME/.codex/skills" ;;
  both) install_to "$HOME/.claude/skills"; install_to "$HOME/.codex/skills" ;;
  *) echo "Usage: $0 [claude|codex|both]"; exit 1 ;;
esac

echo "Restart Claude Code / Codex to load the skills."
