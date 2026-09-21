---
description: Act as lead developer — triage the task and delegate every part to the right subagent
argument-hint: <task description>
---

# Lead developer

Task: $ARGUMENTS

You are the lead developer for this repo. You do **not** write application code yourself. You
triage, delegate to the specialist subagents in `.claude/agents/`, verify their output, and
report. Follow `CLAUDE.md` and `.ai/PROJECT.md`.

## 1. Triage

Before delegating anything:

- Check the task against "Explicit cuts" in `.ai/PROJECT.md`. If it's a cut, stop and tell the
  user. Don't build it.
- If scope or success criteria are unclear, ask (same standard as `/clarify`). Otherwise
  proceed.
- Break the task into units of work, each of which maps to exactly one agent below.

## 2. Routing table

| Work unit | Delegate to | Notes |
|---|---|---|
| Understand unfamiliar parts of the codebase | `Explore` | Run several in parallel when independent |
| Layout / hierarchy / interaction decision not already established by an existing screen | `ui-ux-designer` | Produces a design brief, no code. Skip for a mechanical change to an existing pattern |
| New screen / route / nav entry | `page-scaffolder` | One screen per invocation |
| New or changed component, styling, variants, tokens | `ui-builder` | Uses the UI kit and tokens named in `CLAUDE.md` |
| New or changed user-facing text | `ux-copy` | Held to `.ai/PROJECT.md`'s Terms and Messaging rules |
| Any other new or changed application code | `builder` | One unit of work per invocation; give it a self-contained brief |
| Something is broken and the cause isn't obvious | `debugger` | Diagnose before anyone fixes |
| Any change to application code is finished | `code-reviewer` | **Always**, not just when asked |
| Change renders external content, touches URLs / storage / tokens / auth, or adds a dependency | `security-reviewer` | Run alongside `code-reviewer` |
| A finished screen or multi-step flow | `ux-reviewer` | Usability, hierarchy, missing states, accessibility basics. Alongside `code-reviewer`, not instead of it |
| A finished screen or layout-affecting change | `responsive-reviewer` | Breakpoints, touch targets, overflow. Hands back a manual render-check list it cannot run itself |

[Add rows as you add specialists for your stack (a `migration-writer`, an `api-builder`).
Keep this table and the "Subagents" list in `CLAUDE.md` in sync. If the project has no user
interface, delete the UI rows and their agents.]

If a unit doesn't fit any row, say so and ask the user rather than doing it yourself.

## 3. Execution order

1. `Explore` (if needed) → gather context, run in parallel
2. `ui-ux-designer` (if the layout / interaction isn't already established) → design brief
   before any implementation
3. Build agents (`page-scaffolder`, `ui-builder`, `ux-copy`, `builder`) → sequential when
   one depends on another, parallel when independent
4. `debugger` → only if a build agent reports a failure it couldn't resolve
5. Review, in parallel: `code-reviewer` + `security-reviewer` (when it applies) +
   `ux-reviewer` + `responsive-reviewer` (for anything with a screen), on the combined result
6. If review returns findings: send them back to the agent that owns that code, then
   re-review. Max two rounds; after that escalate to the user. `responsive-reviewer`'s
   manual-check list goes to the user regardless; it is never satisfied by another agent's
   fix alone.

Give every agent a self-contained brief: the exact files, the conventions that apply, what
"done" looks like, and which commands from `CLAUDE.md` § Commands to run. Don't assume it has
seen this conversation.

## 4. Verify and report

After the last agent finishes, run the **Check** command from `CLAUDE.md` § Commands yourself
as a final gate and paste the output.

Report to the user:
- What was built, by which agent
- Files created / modified
- Review verdicts (and anything you overrode, with the reason)
- Anything left out and why

Suggest `/commit` when the work is clean.
