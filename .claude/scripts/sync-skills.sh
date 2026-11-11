#!/usr/bin/env bash
# Copy the shared skills + CLAUDE.md into another repo: sync-skills.sh /path/to/repo
# Non-destructive: skills that already exist in the target are skipped; only missing ones are added.
set -euo pipefail
src="$(cd "$(dirname "$0")/../.." && pwd)"; dst="${1:?target repo path}"
mkdir -p "$dst/.claude/skills" "$dst/.claude/scripts"
added=0
for d in "$src"/.claude/skills/*/; do
  n=$(basename "$d")
  if [ -e "$dst/.claude/skills/$n" ]; then continue; fi
  cp -r "$d" "$dst/.claude/skills/$n"; added=$((added+1))
done
for f in INDEX.md SOURCES.md LICENSE-marketingskills-MIT; do
  [ -f "$src/.claude/skills/$f" ] && [ ! -e "$dst/.claude/skills/$f" ] && cp "$src/.claude/skills/$f" "$dst/.claude/skills/$f"
done
if [ -d "$src/.claude/templates" ]; then mkdir -p "$dst/.claude/templates"; cp -rn "$src/.claude/templates/." "$dst/.claude/templates/"; fi
if [ -d "$src/templates/video" ]; then mkdir -p "$dst/templates/video"; cp -rn "$src/templates/video/." "$dst/templates/video/"; fi
cp "$src/.claude/scripts/sync-skills.sh" "$dst/.claude/scripts/"
[ -f "$dst/CLAUDE.md" ] || cp "$src/CLAUDE.md" "$dst/CLAUDE.md"
[ -f "$dst/.mcp.json" ] || { [ -f "$src/.mcp.json" ] && cp "$src/.mcp.json" "$dst/.mcp.json"; } || true
echo "Skills synced to $dst ($added new skills added)"
