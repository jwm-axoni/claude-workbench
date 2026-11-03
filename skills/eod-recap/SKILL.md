---
name: eod-recap
description: Workbench routine. Sweeps every reachable source once at the end of the workday and writes the one account of the day to Daily/YYYY-MM-DD_DAILY_RECAP.md, with a source and date on every line, then grades the morning briefing's claims into Tracking/Signals/YYYY-MM-DD_recap.md. The nightly dream and the weekly build on this file instead of going back to the sources. Runs as "[Workbench] End-of-Day Recap"; can be run by hand with /workbench:eod-recap.
---

# End-of-day recap

The recap is **the record of the day**. Every source reaches the vault through it. The dream and
the weekly read it instead of forming their own picture, so two routines never describe the same
day differently. Completeness and provenance matter more here than polish.

**You own two files:** `Daily/<today>_DAILY_RECAP.md` and `Tracking/Signals/<today>_recap.md`.
Nothing else.

## Read first

Root `CLAUDE.md`, `Context/me.md`, `People/NAME_VARIANTS.md`, `Resources/GLOSSARY.md`, and today's
`Daily/<today>_MORNING_BRIEFING.md` (including intraday updates) and `_CALENDAR.md` if present.
Then `Tracking/Captures/<today>.md` if it exists: the owner's project chats from today.

## Sweep the sources

Every tool `Context/me.md` marks reachable, for the whole workday, in the role pack's order:
calendar (what actually happened, not what was planned), email (received **and sent**: sent items
are how you learn what the owner did), chat DMs, mentions and key channels, tickets and tasks,
CRM or other role sources, code host, docs edited. If `Meetings/` exists, every meeting file dated
today, **above the `## Transcript` marker only**, plus their `Next Steps` and `Decisions` lines.

Skip personal email and personal meetings entirely. Skip anything in "Calendar blocks that never
appear in a brief".

## Recap file shape

```markdown
---
type: daily-recap
date: YYYY-MM-DD
tags: [daily, recap]
status: active
source: claude-routine
---

# Daily recap — YYYY-MM-DD (Weekday)

## Decisions made today
- Moved the Acme pilot to January — decided by [[Pat Lee]] `source: email 14:02` `date: YYYY-MM-DD`

## Commitments
### Owed by {owner}
- [ ] Send revised pricing — to [[Sam Ortiz]], by Fri `source: meeting 2026-…-acme-sync` `date: …`
### Owed to {owner}
- [ ] Legal review of MSA — [[Dana Kim]], no date `source: chat DM 11:40` `date: …`

## What happened
Grouped by project or relationship, each line with `source:` and `date:`. People, orgs, projects
and tools as bare [[wikilinks]] where a page exists; plain names where one doesn't.

## Wins
## Open follow-ups (carrying into tomorrow)
## Tomorrow — prep
Meetings tomorrow that need something prepared, from tomorrow's calendar file or the connector.

## New names and terms
People, orgs, tools or terms seen today with no page or glossary entry. The dream decides what to
create; you only list them, with the source each came from.

## Notes
Sources unreachable or skipped, and anything ambiguous the dream should know about.
```

Every line under Decisions, Commitments and What happened carries `source:` (which tool, which
message/meeting/time) and `date:`. A line without provenance can't be filed by the dream, so it's a
bug. Don't merge two sources' versions of an event into one claim; if they disagree, write both and
say they disagree.

## Grade the briefing

The morning briefing ends with a `## Claims` list (`c-NNNN | kind | text | confidence`), and each
intraday update may add more. For each claim, decide from today's evidence:

| Outcome | Means |
|---|---|
| `kept` | it held exactly |
| `edited` | partly right, or right but the details changed |
| `deleted` | it was wrong |
| `unaddressed` | nothing today confirms or contradicts it |

Write `Tracking/Signals/<today>_recap.md`:

```markdown
---
type: reference
date: YYYY-MM-DD
tags: [signals, recap]
routine: eod-recap
---

# Briefing scoring — YYYY-MM-DD

- c-0001 | commitment | kept | Draft sent to Pat at 16:10 (sent mail)
- c-0002 | status | deleted | Call stayed on Tuesday; the move was a different meeting
```

One line per claim, with the evidence. You grade; you never edit the briefing. Also note any
correction the owner made today in chat or captures (`correction:` lines) under a `## Corrections`
heading here; the dream turns them into rules.

## If the recap already exists

Append an `## Update — HH:MM` section with only what's new since; don't rewrite. Same for the
Signals file.
