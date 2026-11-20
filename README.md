# Claudeaux 🪷 #

Claudeaux is a swamp-seasoned identity for Claude on GitHub: a GitHub
App the bot comments through, a Claude Code plugin that carries their
voice and collaboration conventions, and the helper scripts that hold
it all together. Claude + the Cajun `-eaux`; pronounce it "claw-doh."

Claudeaux is **they/them**, lives in the bayou, and has seen worse code
than yours in the Atchafalaya.

## What's here ##

| Path | Purpose |
| ---- | ------- |
| `.claude-plugin/` | Claude Code plugin manifest |
| `skills/claudeaux-voice/` | The persona: identity, vocabulary, dial |
| `skills/collab-conventions/` | Review and git-history conventions |
| `app/manifest.json` | GitHub App registration manifest |
| `scripts/register-app.py` | One-shot app registration helper |
| `scripts/claudeaux-token` | Mint installation tokens for `gh`/git |
| `assets/` | Icon (fleur-de-lis with a spark) |

## The app ##

Claudeaux comments as `claudeaux[bot]` so humans and bot are never
confused on a thread. Registration uses GitHub's create-from-manifest
flow:

```console
scripts/register-app.py            # personal account
scripts/register-app.py --org ORG  # an organization you own
```

The helper serves a local form, catches the conversion code, and
writes the app id and private key under `~/.config/claudeaux/`.

**The private key never enters this repository.** `.gitignore` guards
`*.pem` and friends; keep it that way.

Mint a token for any installation:

```console
scripts/claudeaux-token OWNER      # prints a 1-hour installation token
```

## The plugin ##

Install the plugin in Claude Code to give Claude the voice and the
conventions wherever you work:

```console
claude plugin install claudeaux --marketplace felddy/claude-plugins
```

The plugin is published through the
[felddy/claude-plugins](https://github.com/felddy/claude-plugins)
marketplace, which pins each release by commit.

Or try it for one session from a local checkout:

```console
claude --plugin-dir /path/to/claudeaux
```

Authority stays human: approvals, merges, publishes, and conversation
resolution are never Claudeaux's to perform.

## The voice, briefly ##

- `Fais attention, cher:` — this will bite you.
- `Ça c'est bon.` — genuine praise.
- `Lagniappe:` — a little something extra, never blocking.

Seasoning, not gumbo: the persona stays in the frame; the technical
content stays plain.

## License ##

MIT. See [`LICENSE`](LICENSE).
