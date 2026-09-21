---
description: End the session — update .ai/STATUS.md, verify, commit, push, name the model
---

# Wrap up

Close this session so the next one can start with "go". Follow the "Session end" rules in
`CLAUDE.md`.

## 1. Update `.ai/STATUS.md`

Read the current file, then edit in place (don't rewrite sections that haven't changed):

- **Phases**: update the Status column for any phase that moved
- **Recent sessions**: add one bullet at the top, newest first, named
  "Phase N Session M (YYYY-MM-DD)": what happened, what shipped, what's still open. Keep only
  the last five; drop the oldest.
- **Current state**: refresh the table (check status, open blockers, last commit)
- **Next up**: the next concrete task with enough detail to start without clarifying
  questions, plus any "watch out for" traps
- **Settled decisions**: add anything the user decided firmly this session that shouldn't be
  re-raised

Keep the file short. If it's past ~150 lines, trim the oldest material rather than appending.

## 2. Verify

Run the **Check** command from `CLAUDE.md` § Commands and paste the result. If it fails, fix
it or record the failure in Current state. Don't leave it silent.

## 3. Commit and push

- `git status`: nothing should be left uncommitted that belongs to this session's work
- Stage and use `/commit` for the message (WHY, not just WHAT)
- `git push` to the current branch. The git-guard hook blocks pushing to `main`; push a
  feature branch and open a PR instead (or delete that block in `git-guard.sh` if you work
  directly on `main`)
- Confirm `git log origin/<branch>..HEAD` shows 0 unpushed commits and paste it

## 4. Recap

Short, plain-language summary for the user:
- What shipped this session
- What was verified and how (with the output from step 2)
- What was NOT verified, explicitly
- Next up (one line, mirrors STATUS.md)
- Which model ran this session
