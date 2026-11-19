# CLAUDE.md — claudeaux

This repository is Claudeaux's home: the persona (skills/), the GitHub
App registration material (app/, scripts/), and the icon (assets/).

Rules for working here:

- **No credentials, ever.** The app's private key lives in
  `~/.config/claudeaux/`, never in the tree. `.gitignore` guards key
  patterns; do not weaken it.
- The persona is defined once, in `skills/claudeaux-voice/SKILL.md`.
  Voice changes happen there — not ad hoc in comments — so the
  character stays consistent and reviewable.
- `skills/collab-conventions/SKILL.md` is the shareable subset of the
  operator's workflow rules. Keep it generic: anything specific to a
  particular org or engagement belongs in that org's own layer.
- Lint locally before pushing: `pre-commit run --all-files` in a clean
  environment. CI runs the same hooks via
  felddy/reusable-workflows common-lint.
- Scripts are stdlib-only Python (plus the system `openssl`); keep
  them that way so the helpers run anywhere without a venv.
