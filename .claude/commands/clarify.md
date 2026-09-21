---
description: Ask clarifying questions, then plan the task before writing any code
argument-hint: [task description]
---

Task: $ARGUMENTS

Do not implement yet.

## 1. Clarify

Interview the user about this task until you share an understanding of it. Walk down the
design tree: each answer opens the next question, and dependencies between decisions get
resolved one at a time rather than all at once. Ask at least 3 questions covering scope,
success criteria, and technical context; if anything is still unclear after that, keep
going. Don't cap it.

Rules for the questions:

- **If the codebase can answer it, don't ask.** Read the code (or send `Explore`) and state
  what you found instead.
- **Give your recommended answer with every question**, and why. The user should be
  choosing, not generating.
- Ground them in this repo: which feature area and actor from `.ai/PROJECT.md` the work
  belongs to, which existing file or pattern it should follow, what "done" looks like when
  the user tries it. Add examples and edge cases so the intent is unambiguous.
- No filler, no yes/no questions, nothing the task already answers.

Stop and wait for the answers.

## 2. Plan

After the answers, give:

- Restated task (1-2 sentences)
- Numbered steps, concrete and executable (file paths, names)
- Assumptions for anything left ambiguous
- Risks / open questions

Wait for confirmation before writing any code.
