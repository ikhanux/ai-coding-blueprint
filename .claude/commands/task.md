---
description: Implement a single task from a spec file, nothing more
argument-hint: <path/to/spec.md> <TN>
---

# Task

Execute a single task from a spec file.

## Input

$ARGUMENTS — expected as `path/to/spec.md TN`

## Process

1. Read the spec file
2. Find the specified task
3. Review Why, What, Constraints, and Context
4. Implement exactly what the task describes, nothing more (delegate to `builder` if the
   delegation policy in `CLAUDE.md` applies)
5. Run the task's Verify step, then the **Check** command from `CLAUDE.md` § Commands
6. Run the **Format** command from `CLAUDE.md` on the files you touched, if one exists

## Rules

- Only this task; ignore others in the spec
- Only files listed in the task
- No drive-by refactors or additions
- Follow constraints strictly
- Do NOT add dependencies unless specified in Constraints
- Follow `CLAUDE.md` conventions

## After completion

Report:
- What was implemented
- Files created or modified
- Verification result (pass / fail, with output)
- Any issues or blockers

Suggest the next step:
- If more tasks remain: `/task <spec> TN+1`
- If all tasks are complete: run the Done checklist from the spec
