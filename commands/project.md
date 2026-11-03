---
description: Where a project stands, what's decided, and what's owed — from the workbench, read-only
argument-hint: "[project name or topic]"
---

Brief me on the project: **$ARGUMENTS**

**Read-only. Change nothing.** If no project was named, list the active rows in
`Projects/INDEX.md` and ask which. Find the workbench root first (nearest folder with
`.workbench/manifest.json`, or the project's attached folder).

## Find it

Match against `Projects/INDEX.md` rows and filenames in `Projects/`, then aliases and glossary
terms in `Resources/GLOSSARY.md`. If two projects could match, say so and ask. If it's only in
`Archive/Projects/`, say it's archived and lead with that.

## Gather

1. The project page, whole: description, `## Current state (dream)`, `## Decisions` (live entries
   first; mention superseded ones only if they explain the current state), `## Open commitments (mine)`.
2. `Projects/INDEX.md` row. If it disagrees with the page, the page wins; say they disagree.
3. People on it (`### Related`), with roles only as recorded on their pages.
4. The last two weeks of `Daily/` recaps and any `Tracking/Captures/` lines mentioning it, for
   movement not yet filed.
5. Meetings (if `Meetings/` exists) mentioning it, above `## Transcript` only: the latest decisions
   and next steps.
6. `repo:` / `artifacts:` paths: name them, don't open them unless asked.

A `## Needs reconciling` section means a known conflict: report both sides, never pick one. A
meeting's next step only knew what was true on its date; the project page is current state.

## Output

One or two sentences on what it is and where it stands, then:

- **Status**: as of the newest dated source, with that date
- **Decided**: live decisions, newest first, with who and when
- **Owed by you** / **Owed to you**: oldest first
- **Next**: the next concrete step and its date if one exists
- **Gaps**: what the vault doesn't know (no owner, no date, stale page)
