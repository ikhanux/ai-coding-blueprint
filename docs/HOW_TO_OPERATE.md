# How to operate a project built on this blueprint

Written for the project owner, not for Claude. This is your side of the loop, what
you do, in order, from the very first session onward.

---

## Job 0: The very first session of a brand-new project

Do this once, when the folder is empty and nothing exists yet.

1. **Create the project folder** on your machine.
2. **Copy the blueprint into it**: `.claude/`, `.ai/`, `docs/`, `CLAUDE.md.template` land at
   the root.
3. **Make it a git repo**, if it isn't one:
   ```bash
   git init
   ```
   Safe and reversible, just turns the folder into something Claude can commit to.
4. **Open Claude Code in that folder.**
5. **Talk to Claude about the project in plain language**: what it does, who it's
   for, any tech preference you already have (or "you pick"), and that you're not a
   developer. Don't try to write `CLAUDE.md` yourself.
6. **Ask Claude to draft `CLAUDE.md`, `.ai/PROJECT.md` and `.ai/STATUS.md`** from that
   conversation. It fills in the brackets from what you just said. Read the drafts
   back, correct anything wrong, especially the "Working with" and "Verification"
   sections of `CLAUDE.md`, since those set how it treats you from here on, and the
   "Explicit cuts" list in `PROJECT.md`, since that is what stops it building things
   you did not ask for.
7. **Leave deploy/test-specific verification rules loose if nothing is built yet.**
   You can't write "deploy is X, Y, Z" before X, Y, Z exist. Tighten those rules once
   the first version is actually running somewhere, that's normal, not a gap.
8. **Decide on a GitHub remote now or later, your call, not urgent day one.**
   Without a remote, commits work but have nowhere to push yet.
9. **Work through Job 1 below** to lay out the project's phases before any real
   building starts, it's much easier to sketch this on an empty project than to
   retrofit it later.
10. **Let the first real work happen**: scaffolding, first feature, whatever you
    came to build.
11. **Close with `/wrap-up`** (Job 4 below), except `STATUS.md` will honestly say
    something like "Phase 0, nothing built yet" and its "Next up" points at the very
    first real task.

From session 2 onward, the loop is Job 2 → Job 3 → Job 4, repeating.

---

## Job 1: Breaking the project into phases

A project that runs over many sessions needs a checkpoint bigger than "today's
session is done." Phases are that checkpoint, each one a recognizable chunk of the
product, made up of however many sessions it takes to finish it.

For example, a project might define Phase 1 as basic setup and config, Phase 2 as
core functionality, Phase 3 as a major integration, and so on, each a real,
describable piece of the build. Sessions are numbered as one continuous count across
the *whole* project, not reset per phase, only the phase label changes, e.g.
"Phase 3 Session 17" is later than "Phase 3 Session 3" but earlier than "Phase 5
Session 53". A session's name always tells you two things at once: which chunk of
work it belongs to, and where it falls in the project's overall timeline.

1. **Sketch a rough phase list with Claude, early**: during Job 0 if this is a new
   project, or in your next session if the project's already underway. 4-8 phases
   covering the whole build is typical, e.g. "Phase 1: basic setup", "Phase 2: user
   accounts", "Phase 3: core feature", "Phase 4: payments", "Phase 5: polish &
   launch." It doesn't need to be exact, it will change.
2. **Record it in `.ai/STATUS.md`** as a table, one row per phase, with what "done"
   means for that phase and a status (not started / in progress / done). It's the
   thing you check to answer "where are we, overall?" without reading a single
   session recap.
3. **Name every session by its current phase**: "Phase 2 Session 7", in the recap
   and in the status file. It's how the session list stays legible instead of
   becoming an undifferentiated pile.
4. **A phase is done when its own defined chunk works end-to-end and is verified.
   Not when every possible improvement to it has been made.** Don't let a phase
   balloon. If new work doesn't fit its definition, that's the start of a new phase,
   not scope creep on the current one.
5. **Revisit the phase list as you learn things.** Phases you didn't foresee (a bug
   that turns into its own body of work, a pivot) get added; phases that turn out
   unnecessary get dropped or merged. Update the table in `STATUS.md` when this
   happens, and say so plainly in that session's recap, don't silently renumber
   history.
6. **When it's unclear whether something belongs to the current phase or the next
   one, ask Claude to check the current phase's definition in `STATUS.md` before
   starting the work.** Keeps the boundary a real decision, not a vibe.

---

## Job 2: Starting a session

1. Open the project folder in Claude Code.
2. Say **"go"**. Claude reads `CLAUDE.md`, `.ai/PROJECT.md` and `.ai/STATUS.md`, and
   the "Next up" section of `STATUS.md` tells it exactly where to pick up. You don't
   need to re-explain context, that file exists so you never have to.

   For anything that touches the code, say **`/lead`** followed by the task, e.g.
   `/lead add a settings page`. That puts Claude in lead-developer mode (see "The tools
   in plain language" below).

---

## Job 3: What happens during a session

1. Claude reads `CLAUDE.md`, `.ai/PROJECT.md` and `.ai/STATUS.md` automatically, you
   never paste those in yourself.
2. Any action-item for you arrives as a **numbered Job**, not buried in a paragraph.
3. Claude checks in with you for exactly two things: **entering a secret/password**,
   or a **destructive/go-live action**. Everything else it just does.
4. Any claim like "deployed", "tests pass", or "verified" must come with the actual
   command output pasted in the same reply, a hook blocks the reply otherwise. If
   you ever see one of those words with no proof attached, something's wrong with the
   setup, say so.
5. If Claude hits a decision that's genuinely yours to make (not technical), it asks
   you directly instead of guessing.
6. If the task is on the "Explicit cuts" list in `.ai/PROJECT.md`, Claude stops and
   tells you rather than building it. Move it off the list if you've changed your mind.
7. A second hook blocks the handful of git commands that can lose work (force-push,
   history rewrites, throwing away uncommitted changes, pushing straight to `main`). If
   one of those is genuinely needed, Claude will ask you to run it yourself.

---

## Job 4: Ending a session

Say **`/wrap-up`**. Claude then does this on its own; check that it actually did:

1. `.ai/STATUS.md` updated: phase table, last-five-sessions digest, current state, and
   "Next up" rewritten for next time, named for the current phase (e.g. "Phase 2
   Session 8").
2. The project's Check command run, with the output pasted.
3. Committed and pushed, with "0 unpushed commits" shown.
4. A short recap: what shipped, what was verified and how, what was **not** verified,
   and which model ran the session.

If a session ends without these four, ask for them before you close the terminal.

"Next up" in `STATUS.md` is what the next session reads; git log and Claude Code's own
transcripts are the history. One file to keep honest.

---

## Job 5: Starting another new project later

1. Copy the blueprint into the new project's root.
2. Rename the three `.template` files (drop the `.template` suffix):
   - `CLAUDE.md.template` → `CLAUDE.md`
   - `.ai/PROJECT.md.template` → `.ai/PROJECT.md`
   - `.ai/STATUS.md.template` → `.ai/STATUS.md`
3. Follow Job 0 above for the first session, including sketching phases (Job 1)
   before real building starts.
4. Leave everything under `.claude/` untouched. It works for any project as-is. The
   one exception: add your build tool to the allow list in `.claude/settings.json`
   (e.g. `"Bash(npm *)"`) so you are not asked for permission on every command.

---

## The tools in plain language

Everything under `.claude/` is copied as-is and needs no editing. This is what each piece
does for you, so you know what to expect and what to ask for.

### Slash commands: things you type

A slash command is a saved instruction. You type it in the session and Claude follows it.
The ones you will actually use:

| You type | What happens |
|---|---|
| `/lead <task>` | Claude acts as the lead developer: breaks the task up, hands each piece to a specialist (below), reviews the result, runs the checks, reports back. **Use this for anything that touches the code.** |
| `/wrap-up` | Ends the session properly (Job 4). |
| `/commit` | Writes the commit message and asks before committing. |
| `/clarify <task>` | Claude asks you questions and writes a plan before touching anything. Good for a task you can't fully describe yet. |
| `/spec <feature>` then `/task <spec> T1` | For a bigger feature: write it up as numbered tasks first, then do them one at a time. |
| `/review` | A second look at whatever changed, as a senior engineer would. |

The GitHub helpers (`/issue-read`, `/fix-issue`, `/pr-summary`) need the `gh` command-line
tool installed and signed in; ignore them if you don't use GitHub issues.

### Subagents: the specialists

A subagent is a separate Claude with its own instructions and its own memory, started by the
main session for one job and then finished. The main session stays the lead: it plans,
delegates, checks and reports; the specialists do the work. Four ship with the blueprint:

- **builder** writes the code for one well-defined piece of work
- **code-reviewer** checks every finished change against your conventions and rules,
  reports problems, fixes nothing
- **security-reviewer** looks only for things an attacker could actually exploit, and gives
  a SAFE TO MERGE or BLOCK verdict
- **debugger** finds the real cause of a failure before anyone tries a fix

Why this shape: a builder that reviews its own work misses the same things twice. Separate
eyes catch more, and the reviewer's verdict becomes part of the proof rule 1 asks for.

As the project grows, ask Claude to add specialists for your stack ("draft a `ui-builder`
agent from `builder.md` that knows our component library") and to add a row to the routing
table in `/lead` and the list in `CLAUDE.md`.

### Hooks: the things that run without being asked

- **verify-claims** runs when Claude finishes a reply. If the reply says something was
  tested, verified or deployed and no such command ran, the reply is blocked and Claude has
  to either run it or say plainly what it did not check.
- **git-guard** runs before any command. It blocks the handful of git operations that can
  lose work. You'll be asked to do those yourself, which is the point.

### The two files that hold your project

- **`.ai/PROJECT.md`** is what the product *is*: what it does, who it's for, the words you
  use, the rules every change respects, the things you have decided not to build. It changes
  rarely.
- **`.ai/STATUS.md`** is where the build *is*: phases, the last five sessions, current
  state, what's next, what's settled. It changes every session.

`CLAUDE.md` pulls `PROJECT.md` in at the top of every session, and points at `STATUS.md`,
so you never paste either one.

---

## Which model to use for what

Claude Code lets you switch models with `/model`. Most people either never touch it or
leave it on the most expensive one permanently. Both waste money, and one of them also
wastes time.

The principle is simple: **use the deeper model where a mistake is expensive, and the
faster model where a mistake is cheap to undo.**

| Work | Model | Why |
|------|-------|-----|
| Writing code, making changes, running things, fixing small bugs | **Sonnet** | This is most of your sessions. Iteration here is cheap: if it gets something wrong you see it immediately and it fixes it. Speed matters more than depth. |
| Planning, architecture, breaking work into phases, reviewing what was built, hard debugging | **Opus** | A bad plan is expensive, because you then build on top of it for a week. Pay for depth at the points where being wrong compounds. |
| A problem both have now failed on more than once | **Fable** | The escalation, not the default. If two models have each had a real attempt and neither got there, a different one is worth trying before you start rewriting the problem yourself. |

**What this looks like in practice**

- Start a phase on Opus. Plan it, agree what you are building, write it into
  `STATUS.md`.
- Switch to Sonnet and build it. This is the bulk of the hours.
- Switch back to Opus at the end of the phase to review what actually got built against
  what you planned.
- Reach for Fable only when you are properly stuck, not when you are impatient.

**Why this matters more than it sounds**

Planning on a fast model produces plausible plans with holes in them, and you do not find
the holes until you have built on them. Building on the deepest model costs several times
more for work where the extra depth changes almost nothing.

The end-of-session checklist asks which model ran the session for exactly this reason. Over
a few weeks it tells you where your time and money actually went.

---

## Getting more out of what you spend

Model choice is the visible lever. It is not the biggest one. These are, roughly in order
of how much they actually save you.

### 1. Rework is the real cost

Building the wrong thing and rebuilding it costs many times more than any model choice.
An hour of planning on the deeper model routinely saves a day of building the wrong thing
on the faster one.

This is the whole reason the phase structure in Job 1 exists. It is not admin. It is the
single largest cost control in this entire blueprint.

### 2. Start fresh sessions, do not drag one along forever

There are two reasons, and the second one matters more.

**The cost reason.** Everything said earlier in a session is carried along with every later
message. A session running all day is paying for the whole morning on every afternoon reply,
most of which is no longer relevant.

**The context window reason, which is the important one.**

The AI can only hold so much at once. That limit is called the context window, and every model
has one. Think of it as a desk with a fixed amount of space on it.

While there is room, everything you have said this session stays on the desk and the AI can
see all of it. When the desk fills up, the older material does not simply stay there. It gets
compressed into a summary, and some of the detail in it is lost.

That is why a very long session starts to feel different. It is not the AI getting worse. It
is that the specifics of what you agreed four hours ago have been squeezed into a few lines,
and the exact wording of a decision, a constraint you mentioned once, or a thing you told it
never to do can go missing.

**What that looks like when it happens to you**

- It suggests something you already ruled out earlier in the session.
- It contradicts a decision you both made a few hours ago.
- It asks a question you already answered.
- It quietly stops following an instruction it was following at the start.

None of these mean it is broken. They mean the desk is full.

**Why this blueprint fixes it rather than just warning you about it**

Files do not have a context window. `STATUS.md`, `PROJECT.md` and `CLAUDE.md` sit on disk,
and a fresh session reads them at full detail, exactly as written, every time.

That is the actual reason this blueprint exists in the file form it does. **Anything that only
lives in a conversation will eventually be forgotten. Anything written to a file will not.**

So when you notice the symptoms above, or when you switch to genuinely different work, start a
new session. The "Next up" section of `STATUS.md` is what makes that cheap: without it,
starting fresh means re-explaining everything, so people avoid it and let sessions sprawl
until quality degrades. With it, a fresh session costs you a single word.

**The habit worth building:** when a decision matters, ask for it to be written into
`STATUS.md` rather than left in the chat. That one sentence is the difference between a
decision that survives and one that quietly evaporates around hour four.

### 3. One specific request beats five vague ones

"Make the signup page better" produces questions, guesses, and several rounds of correction.
"On the signup page, move the submit button below the password field and make the error text
red" produces one change.

Every round trip costs. Vagueness is what generates round trips.

### 4. Let it finish before interrupting

Interrupting mid-task, then asking it to resume, means it re-reads and re-reasons about work
it had already done. If the direction is right, let the whole task run.

Interrupt when the direction is wrong. That is cheap. Interrupting because you are impatient
is not.

### 5. Batch related work into one session

Five related changes in one session share all the context they need. The same five spread
across five sessions each pay to rebuild it.

The reverse of point 2, and both are the same rule: **context should match the work.** Group
what belongs together, separate what does not.

### 6. Let the specialists carry the weight

This is what `/lead` and the subagents are for. Every file a builder or reviewer opens stays
in *its* memory, not the main session's. The lead session sees briefs and reports, so it stays
light for hours where a single session doing everything itself would have filled its desk by
lunch.

For a one-off broad search, the same idea: "use a subagent for this search."

### The one-line version

Plan on the deeper model, build on the faster one, keep sessions matched to the work, and be
specific. Model choice is worth maybe a third of what avoiding rework is worth.

---

## Your ongoing role, at a glance

| When | What you do |
|------|--------------|
| Brand-new project | Job 0 |
| Laying out (or revising) phases | Job 1, on Opus |
| Building the thing | Sonnet |
| Reviewing a finished phase | Opus |
| Both models stuck on the same problem | Fable |
| Every session start | Job 2, say "go" |
| Anything touching the code | `/lead <task>` |
| Mid-session | Answer direct questions; nothing else needed |
| Secrets requested | Type/paste them yourself, Claude never enters these |
| Destructive or go-live action proposed | Say yes or no, your word is the gate |
| Session end | Job 4, say `/wrap-up`, confirm the 4 items happened |
| Next new project | Job 5 |

You're not expected to read code or logs. The verification rule exists specifically
so you don't have to trust claims, you get shown proof instead.
