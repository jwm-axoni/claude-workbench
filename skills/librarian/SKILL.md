---
name: librarian
description: Audit the workbench vault and report what's wrong with it: missing frontmatter, broken or path-style links, orphan and duplicate pages, superseded entries without forward links, stale pages, ledger entries missing provenance, unfiled captures, one-writer violations, files in the wrong folder. Read-only by default; the weekly routine runs these checks and fixes what's safe. Use for "audit my vault", "is my workbench healthy", "clean up my notes", "find duplicates", or /workbench:librarian.
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
8. Live pages whose `reviewed:` (or `updated:` if no `reviewed`) is older than 30 days.

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
20. Routines that didn't run: workdays in the last two weeks with no recap file, no dream entry, or a
    missing weekly. These are routine defects; name the scheduled task to check.
21. One-writer violations: if the vault is a git repo, commits from the last two weeks that touched a
    file outside the committing routine's ownership table in the root `CLAUDE.md`.
22. Glossary terms `unconfirmed` and seen 3+ times; `UNCONFIRMED` name variants older than 14 days.
23. Drafts in `Tracking/Drafts/` older than three workdays with no grade in any `*_recap.md`.
24. `IMPROVEMENTS.md` items `accepted` for 14+ days but not `done`, or `done` for 30+ days but not
    `verified` / `not-working`.
25. Digests not delivered: briefings in the last two weeks with no `Delivered:` note, or a failure note.

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
