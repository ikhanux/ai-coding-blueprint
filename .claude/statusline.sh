#!/bin/bash
# Status line: model · folder · branch · context used.
#
# AI Coding Blueprint for Non-Developers, v2.0.0 (MIT).
# Registered by .claude/settings.json. Needs only python3.
#
# The context percentage is the one number worth watching: when it climbs past
# ~70%, the session is about to start forgetting things. Wrap up and start fresh
# (docs/HOW_TO_OPERATE.md, "Start fresh sessions").

INPUT="$(cat)"
printf '%s' "$INPUT" | python3 -c '
import json, os, subprocess, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
model = (d.get("model") or {}).get("display_name") or "?"
cwd = (d.get("workspace") or {}).get("current_dir") or os.getcwd()
pct = (d.get("context_window") or {}).get("used_percentage")
try:
    branch = subprocess.run(["git", "-C", cwd, "branch", "--show-current"],
                            capture_output=True, text=True, timeout=2).stdout.strip()
except Exception:
    branch = ""
parts = [f"[{model}]", os.path.basename(cwd.rstrip("/")) or cwd]
if branch:
    parts.append(f"⎇ {branch}")
if pct is not None:
    parts.append(f"{int(pct)}% context")
print(" · ".join(parts))
'
