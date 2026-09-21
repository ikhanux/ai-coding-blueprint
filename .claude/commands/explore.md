---
description: Explore the codebase for a task using parallel Explore agents, then synthesize
argument-hint: <main-task-description>
---

## Your task
Explore the codebase to understand: $ARGUMENTS

Break this into 2-4 focused sub-tasks and investigate each in parallel using Explore agents.

Example: "add a settings page"
- Find the existing page + route registration pattern (where pages live, how they're wired)
- Find the shared components already available that the page can reuse
- Find how existing pages get their data and how forms are handled
- Check `.ai/PROJECT.md` for the feature area, actors, and any cuts that constrain the feature

Run all explorations in parallel, then synthesise findings into:
1. Current architecture overview (only what's relevant to the task)
2. Files to modify and files to create
3. What can be reused vs. what needs to be built
4. Recommended implementation approach
