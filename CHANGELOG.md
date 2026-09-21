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

## [2.0.0]: 2026-09-21

The 1.0.0 layout was three files and a hook. Using it for a while showed where the seams
were: two files saying the same thing, history that was written and never read, and one
session doing everything itself, including reviewing its own work. 2.0.0 is the shape that
came out of that.

**Major because the file layout changed.** An existing 1.x project keeps working untouched;
nothing here breaks it. But the templates, the operate guide and the commands now assume the
new layout, so read "Migrating from 1.x" below before adopting.

### Added

- **`.ai/PROJECT.md.template`**: what the product *is*. Positioning, terms glossary, actors,
  feature areas, global rules, and an "Explicit cuts" list the AI checks every task against.
  `CLAUDE.md` imports it at the top of every session.
- **`.claude/hooks/git-guard.sh`**: a PreToolUse hook that blocks force-pushes, pushes to
  `main`, `reset --hard`, `rebase`, `branch -D`, `clean -f`, discarding all working changes,
  and stash drops. Needs only python3, same as the other hook. The push-to-`main` block is
  one clearly marked section you can delete if you work on `main`.
- **Eleven slash commands** in `.claude/commands/`: `/lead`, `/wrap-up`, `/commit`,
  `/clarify`, `/spec`, `/task`, `/review`, `/explore`, `/issue-read`, `/fix-issue`,
  `/pr-summary`. None hardcode a build tool; they all read the **Commands** table in
  `CLAUDE.md`.
- **Six subagents** in `.claude/agents/`: `builder` (Sonnet), `code-reviewer` (Opus),
  `security-reviewer` (Opus), `ux-reviewer` (Opus), `responsive-reviewer` (Sonnet),
  `debugger` (Sonnet). Reviewers report and never fix. `responsive-reviewer` cannot render
  a page, so it ends every review with a manual check list rather than a verdict.
- **Lead-developer delegation policy** in `CLAUDE.md.template` and `/lead`: the main session
  plans, delegates, verifies and reports; it does not write application code or review its
  own work.
- **Permissions** in `.claude/settings.json`: read-only git pre-allowed; force-push,
  `reset --hard`, and reading `.env` / `settings.local.json` denied.
- **"The tools in plain language"** section in `docs/HOW_TO_OPERATE.md`: what each command,
  agent and hook does, written for the person who will never open them.
- **Commands table** in `CLAUDE.md.template`: one place for the real run / check / test /
  format / build / deploy commands. Everything else points at it.

### Changed

- **`docs/PROJECT_STATUS.md.template` → `.ai/STATUS.md.template`.** Phase table gains a
  "Done means" column. "Next up" plus "Watch out for" absorb the old handoff note. Cap is
  now ~150 lines, down from 300-400, because it is read every session.
- **`CLAUDE.md.template`** restructured: imports `PROJECT.md`, adds the Commands table,
  Architecture and Conventions sections, a "Session end" rule pointing at `/wrap-up`, and the
  tooling / delegation section. Verification rules gain "every change goes through
  `code-reviewer`" and "never run two builds at once".
- **`verify-claims.py`**:
  - Catches "type check **passes**", "lint is clean", "build succeeds", "tests are green"
    (1.0.0 only matched `pass` / `clean`).
  - Recognises `npm|pnpm|yarn|bun run test|typecheck|lint|build|check`, `npx tsc|eslint|
    vitest|jest|playwright`, `pyright`, `go vet`, `cargo check|clippy`, `phpunit`, `rspec`,
    `mix test`, `dotnet test`, `gradle test`, `mvn test`, `make test|check|lint|ci` as test
    evidence; `rsync`, `helm`, `wrangler`, `gcloud`, `aws`, `az`, `terraform`, `pulumi` as
    deploy evidence.
  - A test file now counts as evidence only when **executed** (`python3 test_x.py`,
    `./run_tests.sh`), not merely opened (`cat test_x.py`). 1.0.0 counted both.
  - A denial stops at `;` and `:` as well as sentence ends, so "Before this change it broke;
    now tests pass" is checked. Commas still do not end a denial, so "nothing was deployed,
    verified, or tested" stays one honest sentence.
  - Docstring states plainly that "fixed" and "done" are covered by the rule but not by
    the hook, and why.
- **`docs/HOW_TO_OPERATE.md`**: Jobs 0-5 updated for the new layout; Job 2 introduces
  `/lead`; Job 4 is `/wrap-up`; cost tip 6 explains why subagents keep the main session
  light.
- **README**: "nine files" is now "three files to fill in, everything else copies as-is";
  setup steps updated; limitations updated.

### Removed

- **`docs/NEXT_SESSION_PROMPT.md.template`.** Its job ("where did we leave off, what's
  next, what to watch for") is the "Next up" section of `STATUS.md`. Two files saying the
  same thing drift; one file does not.
- **`docs/history/`** and the one-file-per-session recap. In practice they were written at
  the end of each session and never read at the start of the next; `STATUS.md`'s last-five
  digest was what got read. Git log and Claude Code's own transcripts are the history.
  (The 1.0.0 README listed `docs/history/` but git does not track an empty folder, so it
  was never actually in the download.)
- The `"description"` key from `settings.json`, which is not part of Claude Code's schema.

### Migrating from 1.x

Optional. A 1.x project keeps working as it is.

1. Copy the whole of `.claude/` over yours. It holds nothing of yours. Then re-add your
   build tool to `permissions.allow` in `settings.json`.
2. Create `.ai/`. Move `docs/PROJECT_STATUS.md` to `.ai/STATUS.md` and add a "Next up"
   section with the content of your `NEXT_SESSION_PROMPT.md`. Delete the latter.
3. Create `.ai/PROJECT.md` from the template. Move the "Projects" and "Terms" tables out of
   your `CLAUDE.md` into it.
4. Rebuild `CLAUDE.md` from the new template, carrying over your "Me", "Verification" and
   "Preferences" content. The new **Commands** table is the important addition; fill it in.
5. Delete `docs/history/` or keep it as an archive; nothing reads it now.
6. Say "go". If the next session starts without re-explaining anything, the migration
   worked.

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
2. **Patch or minor:** replace everything under `.claude/` with the new versions, then re-add
   your build tool to `permissions.allow` in `settings.json`. Nothing under `.claude/` holds
   project-specific content, so overwriting is safe. If you added your own agents or
   commands, they are untouched (different filenames).
3. **Never overwrite** `CLAUDE.md`, `.ai/PROJECT.md`, or `.ai/STATUS.md`. Those hold your
   project. Copy across any new sections by hand if you want them.
4. **Major:** read the notes for that version first. It will say what breaks.

Record which version you are on in your project's `CLAUDE.md`, so a future session knows.
