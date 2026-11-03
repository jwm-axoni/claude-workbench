---
name: calendar-sync
description: Workbench routine. Copies today's and the next workday's calendar into Daily/YYYY-MM-DD_CALENDAR.md and records moves, adds and cancellations since the last sync. Runs as the "[Workbench] Calendar Sync" scheduled task; can also be run by hand with /workbench:calendar-sync.
---

# Calendar sync

You keep a dated copy of the workbench owner's calendar so the briefing and recap read a file
instead of rebuilding the day from the connector each time, and so moves and cancellations leave
a record.

**You own exactly two files per run:** `Daily/<today>_CALENDAR.md` and
`Daily/<next workday>_CALENDAR.md`. Never touch an earlier date: a past day is frozen at its last
sync. Never write anything else.

## Steps

1. Read the workbench root `CLAUDE.md` and `Context/me.md`: timezone, working days, and the
   **calendar blocks that never appear in a brief**.
2. Read the calendar for today and the next workday through the connected calendar tool, in the
   owner's timezone. If the read fails, keep whatever file exists, set `status: stale` and
   `synced:` to now in its frontmatter, add a line under `## Changes since last sync` saying the
   read failed, and stop. A stale file must never look like an empty day.
3. For each day, if a file exists, compare the new events with it. Under `## Changes since last
   sync`, append one dated line per moved, added or cancelled event
   (`- 11:32 moved: Pipeline review 14:00 → 15:30`). Never remove earlier change lines.
4. Rewrite `## All day` and `## Events` from the fresh read, and update the frontmatter.

## Privacy rules

- Strip meeting passcodes, dial-in PINs and join links' secrets. Keep the plain meeting link only
  if it has no embedded password.
- External attendees: show a count and their email domain only (`3 external · acme.com`), not names.
  Internal attendees by name, as bare `[[wikilinks]]` only if a `People/` page already exists.
- Private events and blocks listed in `Context/me.md` appear as `Busy` with the time only.
- Never create People pages from calendar data.

## File shape

```markdown
---
type: calendar
date: YYYY-MM-DD
tags: [daily, calendar]
status: active | stale
source: calendar-connector
synced: YYYY-MM-DD HH:MM
---

# Calendar — YYYY-MM-DD (Weekday)

## All day
- …

## Events
- 09:00–09:30 · Team standup · [[Pat Lee]], [[Sam Ortiz]]
- 11:00–12:00 · Acme renewal call · 3 external · acme.com · you organize
- 15:00–15:30 · Busy

## Changes since last sync
- 11:32 moved: Pipeline review 14:00 → 15:30
```

Times in the owner's timezone, 24-hour. Mark events they organize, declined events
(`declined`), and tentative ones (`tentative`). No commentary; this file is a record.
