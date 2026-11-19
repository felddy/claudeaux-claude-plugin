---
name: collab-conventions
description: GitHub collaboration conventions Claudeaux follows — draft-PR approval flow, opener-resolves conversations, rebase-don't-merge branch updates, no squash, signed commits. Use when opening or updating PRs or working review feedback.
---

# Collaboration conventions

## Pull requests

- PRs that await the operator's review are opened as **drafts**; the
  operator moving draft → "ready for review" is the approval signal.
  Never mark a PR ready yourself.
- PR descriptions flow naturally: no hard-wrapping at a column.
  Commit message bodies keep conventional git wrapping.
- Commits are GPG-signed and end with
  `Co-Authored-By: Claude <noreply@anthropic.com>`.

## Review conversations

- **The opener resolves.** Never resolve a review conversation you did
  not open — maintainers verify fixes themselves before closing a
  thread. After addressing a comment, reply with the fixing commit SHA
  and leave the thread open.
- When a conversation has been addressed and awaits the operator's
  closure, say so explicitly rather than resolving it.

## Branch history

- Never add merge commits to a PR branch. When a branch falls behind
  its base: rebase locally onto `origin/<base>` (commits re-sign
  during the rebase), verify content is unchanged with
  `git range-diff`, then `git push --force-with-lease`.
- The lease is load-bearing: when it refuses, someone pushed — fetch,
  inspect what you would have clobbered, and rebase on top of it.
- Never squash: per-commit history is kept for posterity.

## CI

- Watch checks after every push. Before re-running a failed job,
  inspect it: `conclusion: cancelled` with no failing step is runner
  flake (re-run); a real failing step means fix the branch.
- Run the repository's own lint gates locally before pushing, in a
  clean environment — CI's lint job has nothing exported that your
  shell might.
