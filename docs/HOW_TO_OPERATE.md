# How to operate a project built on this blueprint

Written for the project owner, not for Claude. This is your side of the loop, what
you do, in order, from the very first session onward.

---

## Job 0: The very first session of a brand-new project

Do this once, when the folder is empty and nothing exists yet.

1. **Create the project folder** on your machine.
2. **Unzip the blueprint into it**: `.claude/`, `docs/`, `CLAUDE.md.template` land at
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
6. **Ask Claude to draft `CLAUDE.md` and `docs/PROJECT_STATUS.md`** from that
   conversation. It fills in the brackets from what you just said. Read the draft
   back, correct anything wrong, especially the "Me" and "Verification" sections,
   since those set how it treats you from here on.
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
11. **Close with the normal 4-item checklist** (Job 4 below), except
    `PROJECT_STATUS.md` will honestly say something like "day 0, nothing built yet"
    and `NEXT_SESSION_PROMPT.md` points at the very first real task.

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
2. **Record it in `docs/PROJECT_STATUS.md`** as a table, one row per phase, with a
   status (not started / in progress / done). This is the table format your project
   status file uses, and it's the thing you check to answer "where are we, overall?"
   without reading a single session recap.
3. **Name every session by its current phase**: "Phase 2 Session 7", in the recap
   file, the status table, and when you start a session. It's how a pile of
   `docs/history/` files stays legible instead of becoming an undifferentiated list.
4. **A phase is done when its own defined chunk works end-to-end and is verified.
   Not when every possible improvement to it has been made.** Don't let a phase
   balloon. If new work doesn't fit its definition, that's the start of a new phase,
   not scope creep on the current one.
5. **Revisit the phase list as you learn things.** Phases you didn't foresee (a bug
   that turns into its own body of work, a pivot) get added; phases that turn out
   unnecessary get dropped or merged. Update the table in `PROJECT_STATUS.md` when
   this happens, and say so plainly in that session's recap, don't silently renumber
   history.
6. **When it's unclear whether something belongs to the current phase or the next
   one, ask Claude to check the current phase's definition in `PROJECT_STATUS.md`
   before starting the work.** Keeps the boundary a real decision, not a vibe.

---

## Job 2: Starting a session

1. Open the project folder in Claude Code.
2. Say **"go"**, or paste the contents of `docs/NEXT_SESSION_PROMPT.md`. You don't
   need to re-explain context, that file exists so you never have to.

---

## Job 3: What happens during a session

1. Claude reads `CLAUDE.md` and `docs/PROJECT_STATUS.md` automatically, you never
   paste those in yourself.
2. Any action-item for you arrives as a **numbered Job**, not buried in a paragraph.
3. Claude checks in with you for exactly two things: **entering a secret/password**,
   or a **destructive/go-live action**. Everything else it just does.
4. Any claim like "deployed", "tests pass", or "verified" must come with the actual
   command output pasted in the same reply, a hook blocks the reply otherwise. If
   you ever see one of those words with no proof attached, something's wrong with the
   setup, say so.
5. If Claude hits a decision that's genuinely yours to make (not technical), it asks
   you directly instead of guessing.

---

## Job 4: Ending a session

Claude is instructed to do this on its own, check that it actually did:

1. `docs/PROJECT_STATUS.md` updated, current state, kept short (including the phase
   table from Job 1, if the current phase's status changed).
2. Committed and pushed, confirm "0 unpushed commits" if unsure.
3. `docs/NEXT_SESSION_PROMPT.md` rewritten for next time, named for the current
   phase (e.g. "Phase 2 Session 8").
4. Claude tells you which model ran the session.

If a session ends without these four, ask for them before you close the terminal.

---

## Job 5: Starting another new project later

1. Unzip `ai-coding-blueprint.zip` into the new project's root.
2. Rename the three `.template` files (drop the `.template` suffix):
   - `CLAUDE.md.template` → `CLAUDE.md`
   - `docs/PROJECT_STATUS.md.template` → `docs/PROJECT_STATUS.md`
   - `docs/NEXT_SESSION_PROMPT.md.template` → `docs/NEXT_SESSION_PROMPT.md`
3. Follow Job 0 above for the first session, including sketching phases (Job 1)
   before real building starts.
4. Leave `.claude/settings.json` and `.claude/hooks/verify-claims.py` untouched.
   They work for any project as-is.

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
  `PROJECT_STATUS.md`.
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

Files do not have a context window. `PROJECT_STATUS.md`, `CLAUDE.md`, and the session history
sit on disk, and a fresh session reads them at full detail, exactly as written, every time.

That is the actual reason this blueprint exists in the file form it does. **Anything that only
lives in a conversation will eventually be forgotten. Anything written to a file will not.**

So when you notice the symptoms above, or when you switch to genuinely different work, start a
new session. `NEXT_SESSION_PROMPT.md` is what makes that cheap: without a handoff note, starting
fresh means re-explaining everything, so people avoid it and let sessions sprawl until quality
degrades. With one, a fresh session costs you a single sentence.

**The habit worth building:** when a decision matters, ask for it to be written into
`PROJECT_STATUS.md` rather than left in the chat. That one sentence is the difference between a
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

### 6. Ask for research to be delegated

For anything that means reading a lot of files or searching broadly, ask for it to be handled
by a subagent. The searching happens separately and you get the answer back, instead of every
file it opened staying in your session forever.

Just say: "use a subagent for this search."

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
| Mid-session | Answer direct questions; nothing else needed |
| Secrets requested | Type/paste them yourself, Claude never enters these |
| Destructive or go-live action proposed | Say yes or no, your word is the gate |
| Session end | Job 4, confirm the 4-item checklist happened |
| Next new project | Job 5 |

You're not expected to read code or logs. The verification rule exists specifically
so you don't have to trust claims, you get shown proof instead.
