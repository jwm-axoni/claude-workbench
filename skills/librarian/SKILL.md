---
name: librarian
description: Audit the workbench vault against 33 checks and report what's wrong with it: missing frontmatter, broken or path-style links, orphan and duplicate pages, superseded entries without forward links, stale pages, ledger entries missing provenance, unfiled captures, missed routines from the run ledger, a malformed commitments register or surfacing page, unreconciled conflicts, a repo clone behind its remote, one-writer violations, files in the wrong folder. Read-only by default; the weekly routine runs these checks and fixes what's safe. Use for "audit my vault", "is my workbench healthy", "clean up my notes", "find duplicates", or /workbench:librarian.
---

# Librarian

You audit the vault against its own rules. The rules live in the root `CLAUDE.md` and each folder's
`CLAUDE.md`; read them first and check against them, not against your own taste.

**By default you change nothing.** You produce a report. The `weekly-review` routine runs these
same checks every week and fixes what's safe. Run by hand, offer at the end to fix the safe items
now, and do so only with a yes, following the same ownership rules the weekly follows (never inside a
`(dream)` block, never a `CLAUDE.md`, never `Archive/` contents, never delete).

## Scope

Every live folder: `Context/`, `Projects/`, `People/`, `Organizations/`, `Resources/`, `Tracking/`.
Skip `Archive/` (read-only history), `Meetings/` (machine-written) and `Daily/` content (generated;
only check naming). Skip `.workbench/`, `.obsidian/`, `.git/`.

## Checks

33 checks, numbered 1–29, with the relationship checks as 13a–13d.

**Structure**
1. Files in the wrong folder: an entity page in `Daily/`, a dated note in `Resources/`, a person
   in `Organizations/`.
2. `Daily/` filenames not matching `YYYY-MM-DD_<KIND>.md`.
3. Two files with the same name anywhere in the live vault (makes every bare `[[Name]]` ambiguous),
   especially an `Organizations/X.md` and a `Resources/Tools/X.md`.
4. Stray files at the root besides `CLAUDE.md` and `README.md`.

**Frontmatter**
5. Pages missing `type`, `tags`, or `status`; a `type` value not in the root `CLAUDE.md` list.
6. Tags not lowercase kebab-case; function tags not in the vocabulary in `People/CLAUDE.md`.
7. People with a `role:` but no `role_confirmed:`, or a role with no source anywhere.
8. Live pages whose `reviewed:` (or `updated:` if no `reviewed`) is older than 30 days (append-only
   logs such as `RUN_LEDGER.md`, `DREAM_LOG.md` and `FRICTION_LOG.md` excepted).

**Links**
9. Path-style links (`[[People/Name]]`). They break on the next move.
10. Wikilinks to pages that don't exist (check name variants first; it may be a misspelling).
11. Orphans: live pages nothing links to (excluding `CLAUDE.md`, logs, `INDEX.md`).
12. Active pages linking forward into `Archive/` without the history being the point.

**Relationships**
13a. One-sided edges: a property on one page with no inverse on the other (see the table under
     Relationships in the root `CLAUDE.md`).
13b. Relationship properties that are unquoted, path-style, or point at missing pages.
13c. Entity pages with no edges at all: a person with no `org` or `projects`, a project with no
     `owner` or `people`, an org with no `people`. These are graph islands.
13d. People with `last_contact` older than 45 days who are still on an active project's `people`.

**Ledgers and freshness**
13. Ledger entries (commitments, decisions, role claims, glossary terms) missing `source`, a date,
    or `state`.
14. `superseded` entries without a forward link `→`.
15. `superseded` entries unreferenced for 30+ days (candidates for the weekly's archive move).
16. `live` entries sitting below `superseded` ones (position must follow state).
17. Pages with two figures for the same thing and no `## Needs reconciling` section.
18. Project pages missing `## Open commitments (mine)` or `## Decisions`; `INDEX.md` rows that
    disagree with the page's `status`.

**The loop**
19. `Tracking/Captures/` lines not listed under `## Processed captures` in `DREAM_LOG.md` after two
    workdays.
20. Routines that didn't run, from `Tracking/Signals/RUN_LEDGER.md`: for each workday in the last
    two weeks, compare the routines `.workbench/schedules.json` expects with the ledger's lines.
    A missing line, or one marked `failed`, is a miss; a `partial` line is reported with its
    `gaps:` text. Infer from file dates only for days before the ledger existed, and say so.
    These are routine defects; name the scheduled task to check.
21. One-writer violations: if the vault is a git repo, commits from the last two weeks that touched a
    file outside the committing routine's ownership table in the root `CLAUDE.md`.
22. Glossary terms `unconfirmed` and seen 3+ times; `UNCONFIRMED` name variants older than 14 days.
23. Drafts in `Tracking/Drafts/` older than three workdays with no grade in any `*_recap.md`.
24. `IMPROVEMENTS.md` items `accepted` for 14+ days but not `done`, or `done` for 30+ days but not
    `verified` / `not-working`.
25. Digests not delivered: briefings in the last two weeks with no `Delivered:` note, or a failure note.

**Registers and the queue**
26. `Tracking/COMMITMENTS.md` exists, its table has exactly the six columns
    (`Commitment | Who owes | Due | Source | State | Last evidence`), and no row has a `State`
    other than `open`, `looks-done` or `looks-stale`. Report each bad row with its line.
27. `Context/surfacing.md` exists and its sections match the template: `## Always surface`,
    `## Never surface`, `## Quiet hours`, `## Format preferences`, in that order.
28. Any `## Needs reconciling` section older than 14 days (by its `added:` dates, or the page's
    `updated:` if there are none) is a defect. Report it with its page; the weekly's contradiction
    queue should have reached it.
29. Repo vaults only; skip silently if the vault has no `.git` directory. The local clone is not
    behind its remote by more than one day of commits: fetch read-only (`git fetch --dry-run` or
    compare `git log HEAD..@{u}`), and include unmerged `claude/` branches from cloud runs. If it's
    behind, report the gap: how many commits, how old the oldest, which branches.

## Report

Write the report in your reply (or, when the weekly calls you, hand the findings to it). Group by
severity, most important first, and keep it short:

```markdown
## Workbench health — YYYY-MM-DD

**Broken (fix soon):** routine misses, one-writer violations, duplicates causing ambiguous links
**Drift (safe to auto-fix):** frontmatter, path links, missing headings, index rows
**Stale (needs a human or the dream):** old reviews, unconfirmed terms and variants, reconciling
**Counts:** N live pages · N with full frontmatter · N broken links · N orphans
```

Each finding names the file and the rule it breaks, with one line on the fix. If everything's
healthy, say so in one line. Don't pad.
