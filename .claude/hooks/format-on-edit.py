#!/usr/bin/env python3
"""PostToolUse hook on Write/Edit: run the project's Format command after every edit.

AI Coding Blueprint for Non-Developers, v2.0.0 (MIT).
Safe to overwrite with a newer version: this file holds nothing project-specific.

Reads the Format row of the Commands table in CLAUDE.md, so there is one place to
say how this project formats code. Does nothing until that row is filled in:
"none", an empty cell, or a still-bracketed placeholder all mean skip.

Never blocks. Never fails the edit. If the formatter errors, that shows up at the
next Check run, which is where it belongs.
"""
import json
import os
import re
import subprocess
import sys


def format_command(project_dir):
    try:
        with open(os.path.join(project_dir, "CLAUDE.md"), encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return None
    # | Format | `npm run format` |
    m = re.search(r"^\|\s*Format\s*\|\s*`([^`\n]*)`\s*\|", text, re.M | re.I)
    if not m:
        return None
    cmd = m.group(1).strip()
    if not cmd or "[" in cmd or cmd.lower().startswith("none"):
        return None
    return cmd


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if payload.get("tool_name") not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    cmd = format_command(project_dir)
    if not cmd:
        sys.exit(0)

    try:
        subprocess.run(cmd, shell=True, cwd=project_dir, timeout=60,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
