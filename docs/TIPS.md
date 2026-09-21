# Getting more out of Claude Code

Things that make a difference once the blueprint is running. None of them are required.
The first group ships with the blueprint and is already on; the rest you turn on yourself,
in about a minute each.

---

## Already on

### The status line

Bottom of the terminal: `[model] · folder · branch · 42% context`. The percentage is the one
number worth watching. When it passes ~70%, the session is about to start forgetting things
(see "Start fresh sessions" in `HOW_TO_OPERATE.md`). Say `/wrap-up` and start a new one.

Script: `.claude/statusline.sh`. Registered in `.claude/settings.json`.

### Git state at session start

Claude sees your branch and any uncommitted changes the moment a session opens, so it never
starts working on the wrong branch or over the top of something unfinished. A `SessionStart`
hook in `.claude/settings.json`.

### Format after every edit

Every time Claude writes or edits a file, the project's Format command runs. Claude reads the
command from the **Format** row of the Commands table in `CLAUDE.md`, so there is nothing
else to configure: fill in that row and it is on, leave it as "none" and it is off.

Hook: `.claude/hooks/format-on-edit.py`. It never blocks and never fails the edit; a broken
formatter shows up at the next Check run instead.

### Read-only commands pre-allowed

`git status`, `git diff`, `git log`, `git branch` never ask for permission. Add your build
tool once (`"Bash(npm *)"`, `"Bash(cargo *)"`, whatever it is) to
`permissions.allow` in `.claude/settings.json` and the prompts for routine work stop. Keep
the allow list to things that cannot lose work; the deny list and `git-guard.sh` handle the
rest.

---

## Worth turning on

### `/loop`: check something on a timer

Built into Claude Code. Runs a prompt on an interval while you keep working:

```
/loop 5m check whether the deploy finished and tell me
/loop 10m /review
```

Good for anything you would otherwise tab away to check. Stop it when the thing it is
watching is done.

### `/goal`: work in rounds until it is actually done

Ships with the blueprint. State a goal with a checkable success condition:

```
/goal make the Check command pass with no warnings
/goal the signup form rejects an empty email and says why
```

Claude builds, checks, and then hands the result to a separate reviewer to judge whether the
condition is met. Not met, another round. Five rounds and still not met, an honest report of
what is blocking. The point is that the judge is never the one who did the work.

### A language server plugin for your language

The single biggest quality improvement available. A language server gives Claude real type
information and live error reporting instead of guesses. Run `/plugin` inside Claude Code,
open Discover, and install the one for your language (TypeScript, PHP, Python, Go and others
are there).

### Other plugins worth a look

Same `/plugin` menu. Three that pay for themselves:

- **Browser automation**: Claude can open the page, click through it and take a screenshot,
  which is what rule 2 in `CLAUDE.md` asks for and what `responsive-reviewer` cannot do
  alone.
- **Documentation lookup**: Claude fetches the current docs for a library instead of relying
  on what it remembers, which may be a version behind.
- **Security guidance**: passive scanning for hardcoded secrets and injection patterns as code
  is written. `security-reviewer` catches these at review; this catches them earlier.

### Skills, and skill packs for your stack

A skill is a folder with a `SKILL.md` in `.claude/skills/`. Unlike a slash command, which
runs when you type it, a skill loads when Claude decides it is relevant to what it is doing.
Use commands for things you want to control; use skills for knowledge Claude should just
have, like your framework's conventions.

There are shared skill packs for most stacks. Search for one for yours, read what it does
before installing it, and keep the count low: every skill Claude loads takes space on the
desk. A dozen is plenty; fifty is noise.

One trick worth knowing: adding `context: fork` to a skill's frontmatter runs it in its own
subagent, so a heavy research skill does not fill your main session. The blueprint's
`Explore` agent does the same job for one-off searches; say "use a subagent for this search".

### Share a session as a replay

`npx claude-replay <transcript.jsonl> -o replay.html` turns a session transcript (they live
in `~/.claude/projects/`) into a self-contained page that plays the session back with speed
controls. Useful for showing a collaborator how something was built, or for keeping a record
of a session that mattered, without pasting the terminal.

### Compress command output

Test runs, build logs and progress bars fill the context window with text nobody reads.
Tools exist that sit between the command and Claude and trim the noise; `rtk` is one
(`rtk init --global` after installing). Optional, and most useful on projects with chatty
build output.

---

## Things the blueprint already does, so you don't need the "pro tip" for them

- **"Write a spec, then ask for the implementation."** That is `/spec` and `/task`.
- **"Make Claude interview you before it builds."** That is `/clarify`.
- **"Don't let the main session write and review its own code."** That is `/lead` and the
  delegation policy.
- **"Block dangerous git commands."** That is `git-guard.sh`.
- **"Don't let it say tests pass when they didn't run."** That is `verify-claims.py`.
- **"Keep CLAUDE.md short."** The template is the short version; `PROJECT.md` and
  `STATUS.md` hold what would otherwise bloat it.

## Things deliberately left out

- **Undocumented environment flags** that change how Claude Code thinks or remembers. They
  are experimental, they change between versions, and a non-developer cannot tell when one
  has started doing harm. If you want more consistent behaviour, pin models per agent (the
  shipped agents already do) and keep sessions short.
- **A Stop hook that runs the whole test suite every time Claude finishes a reply.** On a
  real project that is minutes of waiting per reply. `verify-claims.py` closes the honesty
  gap without the cost; run the suite at `/wrap-up` and before a deploy.
