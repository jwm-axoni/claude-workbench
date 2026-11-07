---
name: migrate
description: Upgrade, repair or adopt a workbench. Brings an existing workbench up to the installed plugin version without overwriting anything the person edited, resolves .workbench-new conflicts, repairs missing folders or CLAUDE.md files, refreshes connector status, and converts an older or hand-built vault into the workbench layout with the person's approval. Use for "upgrade my workbench", "something's broken", "I updated the plugin", "migrate my vault", or /workbench:migrate.
---

# Workbench migrate

Three jobs, one skill: **upgrade** a workbench to the installed plugin version, **repair** one
that's drifted, and **adopt** a folder that predates the workbench.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workbench.py" detect --root "<workbench>"
```

## If `state` is `fresh` or `foreign`

There's no workbench here yet. Run the `setup` skill instead; it handles adoption.

## If `state` is `workbench`

### 1. Snapshot first

If the workbench is a git repo, check that the working tree is clean, or commit what's there with
message `pre-migrate snapshot`. If it isn't a git repo, copy `.workbench/` and every `CLAUDE.md` to
`.workbench/backup-YYYY-MM-DD/` before changing anything. Say which one you did.

### 2. Refresh the profile

Load `.workbench/profile.json`. Re-check connections the way `setup` step 3 does (one read-only
call per tool) and update each tool's `status` in the profile. New connections are the most common
reason a routine starts doing more after an upgrade. Ask whether anything else changed: role,
hours, tools, routines. Don't re-interview from scratch.

If the profile is missing (for example the workbench was built by hand), reconstruct it from
`Context/me.md` and the root `CLAUDE.md`, confirm it with them, and save it.

### 3. Plan and apply

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workbench.py" plan  --root "<workbench>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workbench.py" apply --root "<workbench>"
```

Summarize the plan before applying: folders to add, files to update, conflicts. What each op means:

- `create`: missing file, written fresh.
- `update`: a plugin-managed file nobody edited, refreshed to the new version.
- `keep`: a content page (people, projects, logs, me.md, GOALS.md…) or a pinned file. Never touched.
- `conflict`: a plugin-managed file someone edited. Theirs stays; the new version lands beside it
  as `<file>.workbench-new`.

#### New vault files in v0.2.0

Upgrading from 0.1.x, `apply` creates four files additively, through the same hash-manifest path:

- `Tracking/COMMITMENTS.md` — the commitments register (dream maintains, weekly closes)
- `Tracking/Signals/RUN_LEDGER.md` — the run ledger (every routine appends one line)
- `Context/surfacing.md` — what the briefing always or never raises
- `.gitignore` — only if the vault is a git repository (`vault_home: repo`, or a `.git` folder when
  the profile doesn't say)

Missing files are created. A file the person already has under one of those names is **never
overwritten**: `apply` reports it as a `conflict` and writes `<file>.workbench-new` beside it. Merge
it like any other conflict (step 4): usually keep theirs, add the template's headings or columns
the routines need, then `pin` it. While you're in the profile, set `surface` and `vault_home` if
they're missing (ask; detect's `git_repo` is a hint, not an answer), so the `schedules` skill can
derive the runner.

### 4. Resolve conflicts

For each `.workbench-new` (also run `status` to catch older leftovers):

1. Diff it against their file. Most conflicts are a root or folder `CLAUDE.md` where they added a
   rule or a **standing exception**. Those additions are deliberate; keep every one.
2. Merge: start from their file, bring in the new version's changes that don't contradict their
   edits, and keep their additions verbatim.
3. Show the merged result in brief and get a yes. Write it over their file, delete the
   `.workbench-new`, then run `pin --path "<file>"` so the merge is recorded as their version.

If they'd rather take the new version wholesale, move theirs to `Archive/Superseded/` with the
date in the name first, then put the new one in place.

### 5. Content migrations

Some versions change the shape of content pages (a renamed section, a new frontmatter field). The
script never edits content, so do these by hand, and only the ones listed in the plugin's
`CHANGELOG.md` between the installed version and the current one. Respect ownership: change a
dream-owned block only in the format the dream will keep writing. Log each one.

### 6. Reschedule

Run the `schedules` skill. Routine prompts rarely change, but times or the routine set might.

### 7. Record it

Append to `Tracking/FRICTION_LOG.md` under `## Resolved`: date, "migrated vX → vY", files updated,
conflicts merged, content migrations done. Then tell them what changed in plain words: what they'll
notice tomorrow morning, not a file list.

## Adopting an older or hand-built vault

When `setup` hands you a `foreign` folder, or someone asks to bring an existing vault into the
workbench:

1. `detect` gives `adopt_suggestions` (e.g. `Journal/ → Daily/`, `Clients/ → Organizations/`).
   Walk through them with the person. For each yes, move the folder's **contents** into the
   workbench folder, one folder at a time. Bare wikilinks survive moves; path-style links
   (`[[Clients/Acme]]`) don't, so rewrite those to bare form as you go.
2. Old templates folders: don't carry them over. The schema now lives in each folder's
   `CLAUDE.md`. Move the old templates to `Archive/Superseded/`.
3. Old scheduled prompts or slash commands that duplicate a routine: list them, and let the
   `schedules` skill replace them.
4. Pages without frontmatter: leave them. The weekly maintenance pass adds `type` and `tags` over
   the following weeks without a big-bang rewrite.
5. Log each move in this week's `Tracking/Signals/YYYY-MM-DD_weekly.md` under `## Moved` (create the
   file if it doesn't exist, with that one section), so the moves are reversible.

Never delete. If something doesn't fit anywhere, it goes to `Archive/Superseded/`.
