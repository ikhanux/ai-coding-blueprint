# Changelog

All notable changes to the AI Coding Blueprint for Non-Developers.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [semantic](https://semver.org/), interpreted for a blueprint rather than a library:

| Bump | Means |
|---|---|
| **Major** (2.0.0) | A change that breaks an existing setup, or requires you to redo work you already did. Read the notes before updating. |
| **Minor** (1.1.0) | New file, new capability, or a meaningful improvement. Safe to adopt, nothing existing breaks. |
| **Patch** (1.0.1) | Wording, typos, clarifications, false-positive fixes in the hook. Always safe. |

---

## [1.0.0]: 2026-08-12

First public release. Extracted from a live production project rather than written as an
example: the system that built [Sociarion](https://sociarion.com) across 715 commits and 127
working sessions, stripped of everything specific to it.

### Added

- **`CLAUDE.md.template`**: the project's memory. Read automatically at the start of every
  session. Covers who you are, how you want to work, what the project is, and what counts as
  done.
- **`docs/HOW_TO_OPERATE.md`**: the guide written for the human, not the AI. Six numbered jobs
  covering the first session on an empty folder, every session after, splitting a build into
  phases, the end-of-session checklist, and reusing the blueprint on the next project.
- **`docs/PROJECT_STATUS.md.template`**: always-current status, with a phase table readable in
  ten seconds, plus the rule that keeps it short.
- **`docs/NEXT_SESSION_PROMPT.md.template`**: the handoff note, so the next session starts with
  "go" instead of twenty minutes of context rebuilding.
- **`.claude/hooks/verify-claims.py`**: blocks replies claiming something was tested, verified
  or deployed when no matching command ran in the session. Deploy detection covers Docker,
  compose, ssh, Vercel, Netlify, Fly, Heroku and generic deploy scripts. Test detection covers
  pytest, npm/yarn/pnpm test, vitest, jest, tsc, mypy, ruff, go test, cargo test and unittest.
- **`.claude/settings.json`**: registers the hook. No editing needed.
- **`docs/history/`**: one file per session, so the project has a record rather than living in
  your head.
- **Context window explanation**: why long sessions start forgetting things, what that looks
  like when it happens, and why files survive where conversations do not. This is the reason
  the blueprint is a set of files rather than a set of prompts.
- **Model and cost guidance** in `docs/HOW_TO_OPERATE.md` and `CLAUDE.md.template`: which
  model to use for planning, building, and escalation, plus six ways to get more out of what
  you spend. Rework, session length and request specificity all cost more than model choice.
- **`LICENSE`**: MIT.

### Known limitations in this version

- The hook confirms a matching command ran. It does not read the output to confirm the command
  proved the right thing. It moves you from "took the AI's word for it" to "something was
  actually run".
- The hook is Claude Code specific, because it uses Claude Code's hook system. The rest of the
  structure works with any AI coding tool.
- Deploy and test detection is pattern based. If your stack uses tooling not in the lists above,
  add it to the regex in `verify-claims.py` or the hook will block claims it cannot recognise
  as verified.

---

## How to update an existing project

The blueprint is copied into your project, so updating is deliberate rather than automatic.

1. Check this file for what changed and which bump it was.
2. **Patch or minor:** replace `.claude/hooks/verify-claims.py` and `.claude/settings.json` with
   the new versions. These are the only files with no project-specific content in them, so
   overwriting is safe.
3. **Never overwrite** `CLAUDE.md`, `docs/PROJECT_STATUS.md`, or `docs/NEXT_SESSION_PROMPT.md`.
   Those hold your project. Copy across any new sections by hand if you want them.
4. **Major:** read the notes for that version first. It will say what breaks.

Record which version you are on in your project's `CLAUDE.md`, so a future session knows.
