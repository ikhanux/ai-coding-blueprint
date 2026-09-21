---
description: Work toward a stated goal in rounds — build, check, get judged by a separate evaluator, repeat — until it is met or the round limit is hit
argument-hint: <goal, with a checkable success condition>
---

# Goal

Goal: $ARGUMENTS

Work in rounds until the goal is genuinely met, judged by someone other than the agent that
did the work. This exists because "I think it's done" and "it is done" are different things,
and the difference is expensive.

## 0. Pin the success condition

Before any work, write down, in one or two lines, what "met" means in checkable terms: a
command that must pass, a screen that must show X, a file that must exist with Y. If the goal
as stated has no checkable condition, ask for one and stop. Do not start without it.

Note the round limit: **5 rounds**, unless the user gave a different number.

## 1. Each round

1. **Build**: delegate the work per the delegation policy in `CLAUDE.md` (`builder` /
   `ui-builder` / `page-scaffolder` / `ux-copy`; `debugger` first if something is broken).
   Self-contained brief every time: the goal, the success condition, what the previous round
   found.
2. **Check**: run the success condition and the **Check** command from `CLAUDE.md`
   § Commands yourself. Paste the output.
3. **Judge**: hand the diff, the success condition and the output to a fresh `code-reviewer`
   with exactly this question: "Is the success condition met, yes or no, and what is the
   evidence?" The builder's own opinion does not count. The reviewer's verdict does.
4. **Decide**: met → go to Report. Not met → next round, with the reviewer's findings as the
   brief. Round limit hit → Report anyway.

Never reword the goal to make it easier to meet. Never mark it met on "should work".

## 2. Report

- Rounds used, and what each one changed
- The success condition, and the evaluator's final verdict with its evidence
- The Check output from the last round
- If the limit was hit: the specific blocker, what was tried, and what the user should decide

Say plainly whether the goal was met. If it was not, say so in the first line.
