---
description: Write an implementation spec to .ai/specs/<slug>.md for a feature
argument-hint: <feature description>
---

# Spec

Generate a specification for AI-assisted implementation.

## Feature

$ARGUMENTS

## Instructions

Read `CLAUDE.md` and `.ai/PROJECT.md` first. Check the feature against "Feature areas" and
"Explicit cuts". If it's a cut, stop and say so. Ask only if blocked.

Create `.ai/specs/<feature-slug>.md`:

```markdown
# Feature Name

## Why

[1-2 sentences: problem solved. Why now.]

## What

[Concrete deliverable. How you'll know it's done.]

## Context

**Relevant files:**
- `path/to/file` — [what it does]

**Patterns to follow:**
- [Existing convention to match, with an example file]

**Key decisions already made:**
- [Tech choices, libraries, approaches locked in]

## Constraints

**Must:**
- [Required patterns / conventions from CLAUDE.md]
- [Global rules from .ai/PROJECT.md that apply here]

**Must not:**
- No new dependencies unless specified
- Don't modify unrelated code; don't refactor existing code
- [Anything from "Explicit cuts" adjacent to this feature]

**Out of scope:**
- [Adjacent features explicitly not included]

## Tasks

Break into tasks that:
- Can each be completed in one session
- Have a clear verify step
- Are safe to commit independently

### T1: [Noun phrase — what gets built]

**Do:** [Specific changes]

**Files:** `path/to/file`

**Verify:** the Check command from CLAUDE.md, or "Manual: open X, see Y"

### T2: [Title]
...

## Done

- [ ] Check + Build commands from CLAUDE.md pass
- [ ] Manual: [what to verify by using it]
- [ ] No regressions in [related area]
```

## Guidelines

**Sizing tasks:**
- Group changes that must ship together (a page + its route + its nav entry = 1 task)
- Split at natural commit boundaries
- If a task might hit context limits, it's too big

**Writing good verify steps:**
- Prefer commands over manual checks
- Manual checks should be specific: "Click X, see Y", not "verify it works"
- Include the unhappy path when relevant (empty state, error state, long input)

**Context section tips:**
- List only files the agent will actually touch or need to reference
- "Patterns to follow" with a concrete example file beats abstract description
- Capture decisions so the agent doesn't re-litigate them

**When to skip sections:**
- Trivial features (< 3 files): inline everything, skip Context
- Bug fixes: Why + What + single Task may suffice

## Scaling

**Small (1-3 files):** abbreviated spec, 1-2 tasks, ~20 lines
**Medium (4-10 files):** full spec, 2-4 tasks, ~40 lines
**Large (10+ files):** consider splitting into multiple specs

## Output

After writing:
1. Spec saved to `.ai/specs/<slug>.md`
2. Review for completeness: could a new agent implement T1 with no other context?
3. To implement: `/task .ai/specs/<slug>.md T1`
