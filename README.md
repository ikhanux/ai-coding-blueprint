# The AI Coding Blueprint for Non-Developers

**Version 1.0.0** · MIT licensed · See [CHANGELOG.md](CHANGELOG.md)

A repeatable system for shipping a real product with AI, without losing the thread.

AI can write the code. It cannot run the project. This is the system that does.

---

## The problem this solves

It is not that the AI writes bad code. It usually does not.

It is that the work does not accumulate. Every session starts from nothing. You re-explain the
project, the AI re-discovers decisions you already made, and it rebuilds things you already had.
You have no idea what is finished and what is half done. You keep moving and the product does
not.

That is a project management problem, and AI coding tools ship with no answer to it.

## What this gives your project

| | |
|---|---|
| **Memory** | One file the AI reads at the start of every session. Write it once, stop repeating yourself. |
| **Direction** | A phase structure, so you always know what you are building now and what comes next. |
| **Continuity** | An always-current status file and a handoff note. Start tomorrow by saying "go". |
| **Proof** | A hook that blocks claims of tested or deployed work when no such command ran. Building on a step that never happened is the most expensive rework there is. |
| **Efficiency** | Which model to use for planning, building and escalation, plus the six things that actually control what a project costs you. |

## Why files and not prompts

Every AI has a context window: a fixed amount it can hold at once. In a long session the older
material gets compressed into a summary, and detail is lost. That is why hour four feels
different from hour one. It suggests things you already ruled out, contradicts decisions you
made together, quietly drops an instruction it was following at the start.

Files do not have a context window. A fresh session reads them at full detail, exactly as
written, every time.

**Anything that only lives in a conversation will eventually be forgotten. Anything written to
a file will not.** That is the reason this is a set of files rather than a set of prompts.

## Not a theory

This is the setup that built [Sociarion](https://sociarion.com), a multi-tenant social media
automation platform, from an empty folder to a live product. 715 commits across 127 working
sessions, driven entirely through Claude Code, run by someone who does not write code.

Everything here is the real thing, stripped of anything specific to that project.

---

## What is in here

```
CLAUDE.md.template                 rename to CLAUDE.md, fill in every [BRACKET]
docs/HOW_TO_OPERATE.md             read this one yourself, start to finish
docs/PROJECT_STATUS.md.template    rename to PROJECT_STATUS.md, fill in
docs/NEXT_SESSION_PROMPT.md.template
docs/history/                      one file per session goes here later
.claude/settings.json              registers the hook, copy as is
.claude/hooks/verify-claims.py     the hook itself, copy as is
CHANGELOG.md                       what changed, and how to update safely
LICENSE                            MIT
```

**Start with `docs/HOW_TO_OPERATE.md`.** It is the step by step for the human running this:
your first session on an empty folder, every session after that, how to split a build into
phases, and how to reuse this on your next project. It also covers which model to use for what,
and why long sessions start forgetting things. Everything below is reference. That file is the
walkthrough.

## Setup (about 5 minutes)

1. Copy this folder into your project root.
2. Rename `CLAUDE.md.template` to `CLAUDE.md`. Fill in every `[BRACKET]`: who you are, what the
   project is, and what counts as done for your setup.
3. Rename `docs/PROJECT_STATUS.md.template` and `docs/NEXT_SESSION_PROMPT.md.template`, dropping
   the `.template` suffix. Fill in the placeholders.
4. Leave `.claude/settings.json` and `.claude/hooks/verify-claims.py` alone. They work as is for
   any project.
5. Open your first session and follow Job 0 in the operate guide.

**Easier option for step 2:** tell the AI what your project is in plain language and ask it to
fill in `CLAUDE.md` for you, then read it back and correct anything wrong.

## The part you should NOT copy verbatim

The "Verification" section in `CLAUDE.md.template` is a shape, not a script. Name your project's
actual deploy steps and actual test command in place of the placeholders. If your project has no
deploy step, delete that rule rather than leaving it sitting there doing nothing.

## Honest limitations

The hook checks that a matching command ran. It does not read the output and confirm the command
proved the right thing. It moves you from "took the AI's word for it" to "something was actually
run", which is a real jump and is not a guarantee.

The hook is Claude Code specific, because it uses Claude Code's hook system. The rest of the
structure works with any AI coding tool.

## Updating

See [CHANGELOG.md](CHANGELOG.md). Short version: the two files in `.claude/` are safe to
overwrite because they hold nothing of yours. Never overwrite `CLAUDE.md`,
`docs/PROJECT_STATUS.md`, or `docs/NEXT_SESSION_PROMPT.md`, which hold your project.

## Licence

MIT. Use it, change it, ship it. No attribution required.
