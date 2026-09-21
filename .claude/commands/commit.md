---
description: Write a commit message for staged changes (explains why, not just what)
---

# Commit

Generate a commit message for staged changes.

## Instructions

1. Run `git diff --staged` to see changes. If nothing is staged, say so and stop.
2. Write a commit message that explains WHY, not just WHAT.
3. Show the message and ask before running `git commit`.

## Format

<type>(<scope>): <subject>

<body>

### Types
- feat: New feature
- fix: Bug fix
- refactor: Code change (not fix or feature)
- style: Formatting / visual-only change
- docs: Documentation
- chore: Maintenance, tooling, deps

Scope is optional; when used, prefer the page / module / area name.

### Rules
- Subject: max 50 chars, imperative mood, no trailing period
- Body: explain WHY this change was needed
- Reference issues if applicable

## Example

feat(settings): add export-all-data button

Users had no way to get their data out without emailing support.
This adds a one-click export that produces the same archive the
support team was building by hand.

Closes #234

## Guidelines

- Future you will search git blame at 2am
- If you can't summarise it, the change might be too big
