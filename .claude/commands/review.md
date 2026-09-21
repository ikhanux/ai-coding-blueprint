---
description: Senior-engineer review of changed files (or a given target)
argument-hint: [file, directory, or nothing for all changed files]
---

# Review

Review code as a senior engineer would.

## Target

$ARGUMENTS

If no target is specified, review all changed files (`git diff HEAD --name-only` plus untracked
files under the source folder named in `CLAUDE.md`).

## Instructions

Read `CLAUDE.md` and `.ai/PROJECT.md` first. Then look at the code and ask:

### Simplicity
- Is this over-engineered?
- Could it be shorter without losing clarity?
- Are there unnecessary abstractions?

### Clarity
- Are names descriptive?
- Is the logic easy to follow?
- Would a new teammate understand this?

### Consistency
- Does it match `CLAUDE.md` § Conventions and § Architecture?
- Does it match its sibling files?
- Does it respect every rule in `.ai/PROJECT.md` § Global rules?

### Correctness
- Are edge cases handled? (empty, loading, error, long content)
- Any obvious bugs, race conditions, resource leaks, stale state?

Run the **Check** command from `CLAUDE.md` § Commands and include failures.

## Output

If changes are needed:
1. List specific issues with `file:line`
2. Provide the fixed code

If the code is good:
- Say so briefly and move on

## Guidelines

- Be constructive, not nitpicky
- Focus on what matters: bugs, clarity, maintainability
- Don't suggest changes just to suggest changes
