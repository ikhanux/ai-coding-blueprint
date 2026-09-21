---
description: Investigate and fix a GitHub issue by number
argument-hint: <issue-number>
allowed-tools: Bash(gh *)
---

!`gh issue view $ARGUMENTS`

Investigate and fix the issue above.

1. Reproduce it first, using the Run / Check / Test commands from `CLAUDE.md` § Commands
2. Trace the bug to its root cause: read the actual code, don't guess (delegate to
   `debugger` if the cause isn't obvious)
3. Implement the minimal fix; no drive-by refactors
4. Run the Check command, then the Format command on touched files if one exists
5. Summarise what you changed and why, referencing the issue number
