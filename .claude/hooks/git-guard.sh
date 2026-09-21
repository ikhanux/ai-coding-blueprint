#!/bin/bash
# PreToolUse hook for Bash: blocks destructive git operations before they run.
#
# AI Coding Blueprint for Non-Developers, v2.0.0 (MIT).
# Safe to overwrite with a newer version: this file holds nothing project-specific.
#
# Claude Code passes the tool call as JSON on stdin. Exit 2 blocks the call and feeds
# the message back to Claude, which then asks you to do it by hand if it is genuinely
# needed. Exit 0 lets it through.
#
# Needs only python3 (which verify-claims.py already needs). No jq.

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | python3 -c \
  'import json,sys
try:
    print(json.load(sys.stdin).get("tool_input", {}).get("command", ""))
except Exception:
    pass' 2>/dev/null)"

[ -z "$COMMAND" ] && exit 0

# Only look at git invocations
printf '%s' "$COMMAND" | grep -qE '(^|[;&|]\s*)git\s' || exit 0

# 1. Force pushes, to any branch
if printf '%s' "$COMMAND" | grep -qE 'git push .*(--force|-f( |$)|--force-with-lease|\+[A-Za-z])'; then
  echo "Blocked: force-pushing is not allowed. Push a normal commit or open a PR." >&2
  exit 2
fi

# 2. Direct pushes to main/master.
#    Matches "git push origin main", "git push origin HEAD:main", "git push -u origin main".
#    Does not match "git push origin feature/main-page".
#    Delete this block if you work directly on main and do not use pull requests.
if printf '%s' "$COMMAND" | grep -qE 'git push( +-[A-Za-z-]+)*( +[^ :]+)? +([^ ]+:)?(main|master)( |$)'; then
  echo "Blocked: pushing directly to main is not allowed. Push a feature branch and open a PR." >&2
  exit 2
fi

# 3. History rewrites, destructive resets, and throwing away uncommitted work
if printf '%s' "$COMMAND" | grep -qE 'git (reset --hard|clean -[A-Za-z]*f|branch -D|rebase|checkout -- \.|restore( --worktree)? \.|stash (drop|clear)|push --delete|filter-branch|filter-repo)'; then
  echo "Blocked: history-rewriting/destructive git commands are not allowed from Claude. Ask the user to run this manually." >&2
  exit 2
fi

exit 0
