# Contributing to Tributary — Working Rule

Adopted by the owner, November 8, 2026. This rule binds every contributor to this repository — the owner, Codex, Muse, and ChatGPT — for all work in any clone or checkout of Tributary.

## Source of truth

**GitHub `main` is the source of truth.** A local clone is a working copy. If a local copy and GitHub disagree, GitHub wins until the divergence is resolved under the rules below.

## Before editing

1. Check the working tree for local changes (`git status`).
2. Fetch GitHub (`git fetch origin`).
3. On a clean `main`, update with a fast-forward pull only: `git pull --ff-only`.
4. Create a task branch from the updated `main` and work there.
5. For an existing task branch: pull that branch first, then reconcile it with the current `origin/main` before doing new work.

## Preserve work

- Preserve uncommitted work. Never discard, stash-and-forget, or overwrite local changes to make a pull succeed.
- **Stop and resolve divergence or conflicts before proceeding.** A failed fast-forward is a signal to reconcile deliberately, not to force.

## Completion

Work is complete only when **all** of the following hold:

- the test suite passes,
- the changes are committed and pushed,
- the remote commit is verified on GitHub.

Report the **branch, commit, and PR link** for every piece of completed work. **Only merged work is considered shipped on `main`.**

## Daily collector state

- The daily collector keeps its generated state in its ignored output directory (`out/`) inside the working clone. Runtime state does not get committed as if it were code.
- Code changes follow the push-and-PR rule above, without exception.
- **Backup policy for runtime data** (owner-confirmed November 8, 2026): runtime data is never committed to git, so it is backed up separately. The operating clone lives in the owner's iCloud-synced Documents folder, and all iCloud data is backed up daily; that daily backup covers the whole clone, including `out/` and the private feedback database. Two known limits: sync propagates deletions (the daily backup is the protection against that), and a restore from this backup has not yet been test-run.

## One-time git setup (every clone)

Configure pull to allow fast-forward updates only, so unexpected divergence fails visibly instead of silently merging:

```bash
git config pull.ff only
```

Run it once inside each clone (or set it globally with `git config --global pull.ff only`).
