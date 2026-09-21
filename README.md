# The AI Coding Blueprint for Non-Developers
### A repeatable system for shipping a real product with AI, without losing the thread

**Version 2.0.0** · MIT licensed · See [CHANGELOG.md](CHANGELOG.md)

> AI can write the code. It cannot run the project. This is the system that does.

**715 commits · 127 working sessions · 1 non-developer · 1 live product**

Built [Sociarion](https://sociarion.com) from an empty folder to a running multi-tenant SaaS.
This is the system that did it, packaged.

---

## Start here

**Read [`docs/HOW_TO_OPERATE.md`](docs/HOW_TO_OPERATE.md) first.** It is the step by step for
the human running this: your first session on an empty folder, every session after that, how to
split a build into phases, and how to reuse this on your next project. Everything else in this
README is background, not instructions.

---

## The real problem with building software using AI

It is not that the AI writes bad code. It usually does not.

It is that the work does not accumulate. Every session starts from nothing. You re-explain the
project, the AI re-discovers decisions you already made, and it rebuilds things you already had.
You have no idea what is finished and what is half done. You keep moving and the product does
not.

Then somewhere in there you get told something is working when it is not, and you find out two
weeks later.

None of that is a coding problem. It is a project management problem, and AI tools ship with no
answer to it at all.

## What this is

The operating system that goes around the AI. Three files to fill in, everything else copies
as-is. About five minutes to set up. Free, MIT licensed.

It gives your project things it does not have by default:

| | |
|---|---|
| **Memory** | One file the AI reads at the start of every session. Write it once, stop repeating yourself. |
| **Direction** | A phase structure, so you always know what you are building now and what comes next. |
| **Continuity** | One always-current status file that ends with "Next up". Start tomorrow by saying "go". |
| **Proof** | A hook that blocks claims of tested or deployed work when no such command ran. Building on a step that never happened is the most expensive rework there is. |
| **A team** | A lead-developer mode that hands each piece of work to a specialist: a builder, a code reviewer, a security reviewer, a UX reviewer, a responsive reviewer, a debugger. Separate eyes catch what one pair misses. |
| **Guardrails** | A hook that blocks the git commands that can lose work, so the AI asks you instead of doing it. |
| **Efficiency** | Which model to use for planning, building and escalation, plus the six things that actually control what a project costs you. |

## Why files and not prompts

Every AI has a context window: a fixed amount it can hold at once. In a long session the older
material gets compressed into a summary, and detail is lost. That is why hour four feels
different from hour one. It suggests things you already ruled out, contradicts decisions you
made together, quietly drops an instruction it was following at the start.

Files do not have a context window. A fresh session reads them at full detail, exactly as
written, every time.

**Anything that only lives in a conversation will eventually be forgotten. Anything written to
a file will not.** That is the entire reason this exists in the shape it does.

## This is not a theory

It is the setup that built [Sociarion](https://sociarion.com), a multi-tenant social media
automation platform, from an empty folder to a live product. 715 commits across 127 logged
working sessions, driven entirely through Claude Code, run by someone who does not write code.

Everything here is the real thing, stripped of anything specific to that project.

Built by [Usarion](https://usarion.com).

---

## What's included

Three files to fill in. Everything else copies as-is. Nothing to sign up for.

```
CLAUDE.md.template                 rename to CLAUDE.md, fill in every [BRACKET]
.ai/PROJECT.md.template            rename to PROJECT.md: what the product IS
.ai/STATUS.md.template             rename to STATUS.md: where the build IS
docs/HOW_TO_OPERATE.md             read this one yourself, start to finish

.claude/settings.json              registers the hooks and permissions, copy as is
.claude/hooks/verify-claims.py     blocks unproven "verified / tested / deployed"
.claude/hooks/git-guard.sh         blocks the git commands that lose work
.claude/commands/                  11 slash commands: /lead, /wrap-up, /commit, /spec ...
.claude/agents/                    6 subagents: builder, code-reviewer, security-reviewer,
                                   ux-reviewer, responsive-reviewer, debugger

CHANGELOG.md                       what changed, and how to update safely
LICENSE                            MIT
```

1. **`CLAUDE.md.template`, the project's memory.** The file the AI reads automatically at the
   start of every session: who you are, how you want to be spoken to, the verification rules,
   the real commands to run, and how work is delegated. Fill it in once. Stop re-explaining
   your project forever.
2. **`.ai/PROJECT.md.template`, what the product is.** Positioning, the words you use, who the
   users are, the rules every change respects, and the list of things you have decided not to
   build. `CLAUDE.md` pulls it in at the top of every session. Changes rarely.
3. **`.ai/STATUS.md.template`, where you actually are.** Phase table readable in ten seconds,
   the last five sessions, current state, and "Next up", so tomorrow starts with "go".
   Changes every session.
4. **`docs/HOW_TO_OPERATE.md`, the part written for you.** Numbered jobs in plain language:
   your first session on an empty folder, every session after that, splitting a long build
   into phases, ending a session, reusing the whole thing on your next project, and what each
   of the tools below actually does. No code in it.
5. **The verification hook** (`.claude/hooks/verify-claims.py`). Runs automatically when the AI
   finishes a reply. If it claims something was tested, verified, or deployed, the hook checks
   whether a matching command actually ran. If not, the reply is blocked.
6. **The git guard** (`.claude/hooks/git-guard.sh`). Runs before every command. Blocks
   force-pushes, history rewrites, throwing away uncommitted work, and pushing straight to
   `main`. The AI asks you to do those yourself, which is the point.
7. **Slash commands** (`.claude/commands/`). `/lead <task>` puts the AI in lead-developer
   mode. `/wrap-up` ends the session properly. `/clarify`, `/spec`, `/task`, `/review`,
   `/commit`, `/explore` cover the rest of the loop. Three GitHub helpers if you use issues.
8. **Subagents** (`.claude/agents/`). A builder that writes, a code reviewer that only
   reports, a security reviewer that only flags what is exploitable, a UX reviewer for
   hierarchy, missing states and accessibility, a responsive reviewer for breakpoints and
   touch targets, and a debugger that finds the cause before anyone fixes. The main session
   stays the lead and never reviews its own work.
9. **The settings file** (`.claude/settings.json`). Registers both hooks, pre-allows
   read-only git, denies reading `.env`. Add your build tool to the allow list and you are done.

## Who it is for

- Founders and operators building a real product with AI, who cannot read the code
- Anyone whose AI project has stalled in a pile of sessions that never became a thing
- People who keep re-explaining the same project every single time they open a session
- Developers who want the phase and status structure and will ignore the rest, which is fine

## Who it is not for

- One-off scripts and throwaway experiments. The structure costs more than it returns.
- Anyone who wants the AI to go faster by planning less. This does the opposite deliberately.

---

## Setup (about 5 minutes)

1. Copy this folder into your project root (clone it, or download the zip from GitHub and
   unzip it). If you cloned, delete the `.git` folder so this repo's history does not
   become your project's.
2. Rename the three `.template` files, dropping the suffix:
   `CLAUDE.md.template` → `CLAUDE.md`, `.ai/PROJECT.md.template` → `.ai/PROJECT.md`,
   `.ai/STATUS.md.template` → `.ai/STATUS.md`.
3. Fill in every `[BRACKET]`. The **Commands** table in `CLAUDE.md` matters most: every slash
   command and subagent reads it to know what to run.
4. Add your build tool to the allow list in `.claude/settings.json` (e.g. `"Bash(npm *)"`).
   Leave the rest of `.claude/` alone. It works as is for any project.
5. Open your first session and follow Job 0 in the operate guide.

**Easier option for step 3:** tell the AI what your project is in plain language and ask it to
fill in the three files for you, then read them back and correct anything wrong.

## The part you should NOT copy verbatim

The "Verification" section in `CLAUDE.md.template` is a shape, not a script. Name your project's
actual deploy steps and actual check command in place of the placeholders. If your project has no
deploy step, delete that rule rather than leaving it sitting there doing nothing.

The git guard blocks pushing straight to `main`, which means feature branches and pull requests.
If you are solo and work on `main`, delete that one block in `git-guard.sh`; the file says which.

## Honest limitations

The hook checks that a matching command ran. It does not read the output and confirm the command
proved the right thing. It moves you from "took the AI's word for it" to "something was actually
run", which is a real jump and is not a guarantee. It also does not police "fixed" or "done":
those words are used honestly far too often ("fixed the typo") for a pattern to tell the
difference. The rule still applies; the hook enforces the rest.

The hooks, commands and agents are Claude Code specific, because they use Claude Code's hook,
command and subagent systems. The three files you fill in work with any AI coding tool.

The six subagents are deliberately generic. As your project grows you will want specialists
that know your stack. Ask the AI to draft them from `builder.md`; the operate guide says how.

The templates are a starting shape, not a finished process. Rewrite the rules to match how your
project actually builds and deploys, and delete any rule that does not apply to you rather than
leaving it sitting there doing nothing.

## Updating

See [CHANGELOG.md](CHANGELOG.md). Short version: everything under `.claude/` is safe to
overwrite because it holds nothing of yours (re-add your build tool to the allow list after).
Never overwrite `CLAUDE.md`, `.ai/PROJECT.md`, or `.ai/STATUS.md`, which hold your project.

## Licence

MIT. Use it, change it, ship it. No attribution required.

---

## Get the blueprint

Free, MIT licensed. Copy into your project folder, rename three files, fill in the blanks.
[`docs/HOW_TO_OPERATE.md`](docs/HOW_TO_OPERATE.md) walks you through your first session from an
empty folder.
