---
type: reference
tags: [tracking, signals, ledger]
status: active
updated: {{created_date}}
---

# Run ledger

One line per routine run, appended when the run finishes. A missing line is how a missed run
shows up: the briefing names it, the dream recovers what it can, the librarian counts it.

<!--
Line format, newest last:
- YYYY-MM-DD HH:MM | <routine> | <ok|partial|failed> | wrote: <comma-separated file names, or "nothing"> | gaps: <none, or a short description>

<routine> is the routine id from `.workbench/schedules.json` (calendar-sync, daily-briefing,
midday-update, eod-recap, nightly-dream, weekly). Times are in {{preferred_name}}'s timezone.

Who writes this file: every routine appends one line when it finishes, and none edits or deletes
a line. The librarian reads it. This is the one documented exception to one writer per file (see
the root CLAUDE.md). It's safe because appends are dated lines, never edits. Nothing above
`## Runs`, frontmatter included, is ever touched by a routine.
-->

## Runs
