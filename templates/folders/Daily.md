---
type: system
updated: {{created_date}}
---

# Daily

Dated files written by routines. One file per date per kind.

## Naming

| File | Writer | When |
|---|---|---|
| `YYYY-MM-DD_CALENDAR.md` | `calendar-sync` | workdays, before work, midday, end of day |
| `YYYY-MM-DD_MORNING_BRIEFING.md` | `daily-briefing` | workdays before work; midday appends below it |
| `YYYY-MM-DD_DAILY_RECAP.md` | `eod-recap` | workdays after work |
| `YYYY-MM-DD_RECONSTRUCTED_RECAP.md` | `eod-recap` | the next recap, when the recap for that day never ran |
| `YYYY-MM-DD_NEXT_WEEK_PLAN.md` | `weekly-review` | first workday of the week |

The date prefix sorts chronologically. Keep it.

## Frontmatter

```yaml
---
type: morning-briefing | daily-recap | calendar | weekly-plan
date: YYYY-MM-DD
tags: [daily, <kind>]
status: active | stale | reconstructed
source: claude-routine | manual
---
```

`status: stale` on a calendar file means the connector read failed, so a stale file can be
told apart from a day with no meetings.

`status: reconstructed` on a recap means the day's recap never ran and a later one rebuilt what it
could. It lists what couldn't be swept. Never read it as a full record of that day.

## Conventions

- **Briefings are append-only after the fact.** The midday pass appends an `## Intraday update`
  block below the morning content and never rewrites it. What was known at the start of the day
  has value precisely because it wasn't edited later.
- **The recap is the record.** It's the one account of the day: every source reaches the vault
  through it, every line carries its source and date, and the dream and weekly read it instead
  of going back to the sources.
- **A past calendar file is frozen.** `calendar-sync` rewrites only today and the next workday.
- Link people and projects with bare `[[wikilinks]]` so a person's page collects backlinks from
  every day they came up. That backlink trail is the point of keeping dailies.
- Don't hand-edit or duplicate a routine's file. Write notes in the Claude project instead; it
  appends to `Tracking/Captures/`.

## Structure

These files are generated. Each routine's skill carries its exact output shape, so there's no
page shape to copy here.
