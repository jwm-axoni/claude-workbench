---
name: daily-briefing
description: Workbench routine. Writes the morning briefing to Daily/YYYY-MM-DD_MORNING_BRIEFING.md (what today needs, replies owed, risks, focus, what the dream learned, questions) and, in midday mode, appends an intraday update below it. Runs as the "[Workbench] Morning Briefing" and "[Workbench] Midday Update" scheduled tasks; can be run by hand with /workbench:daily-briefing.
---

# Daily briefing

The briefing is the surface the owner reads to start the day. It is not the record (the recap
is), so it can be opinionated about priorities, but every fact in it must trace to a source.

**You own one file:** `Daily/<today>_MORNING_BRIEFING.md`. In midday mode you append to it. You
write nothing else in the vault.

## Read first, in this order

1. Root `CLAUDE.md`, then `Context/me.md` (role lens, what urgent means, reachable tools, blocks
   that never appear), `People/NAME_VARIANTS.md`, `Tracking/GOALS.md`, `Resources/GLOSSARY.md`.
2. The **ledgers**, before any live source, so you don't re-report what the vault already knows:
   - yesterday's (or the last workday's) `Daily/*_DAILY_RECAP.md`, especially open follow-ups and
     tomorrow-prep
   - the newest entry in `Tracking/DREAM_LOG.md`, especially **Needs your yes**
   - `## Open commitments (mine)` on active projects in `Projects/INDEX.md`
   - today's `Daily/<today>_CALENDAR.md` if it exists and isn't `stale`; otherwise the calendar connector
3. Then the live sources, **only tools `Context/me.md` marks reachable**, since the last recap:
   email, chat DMs and mentions, tickets or tasks due today or tomorrow, the role-specific sources
   (CRM, code host, etc.). If `Meetings/` exists, yesterday's meeting files, **above the
   `## Transcript` marker only**.

If a source can't be reached, say so in one line under Notes. Never fill a gap with a guess.

## Morning mode: file shape

```markdown
---
type: morning-briefing
date: YYYY-MM-DD
tags: [daily, briefing]
status: active
source: claude-routine
---

# Morning briefing — YYYY-MM-DD (Weekday)

## Today
Meetings worth attention, each with one line of context from People/Projects/Organizations
and what to bring. Skip routine internal meetings unless something is due in them.

## Urgent and at risk
Only things that match "what urgent means" in Context/me.md, or a hard date in GOALS.md within 7 days.

## Replies owed
Grouped by person, oldest first, with where it came from (email, DM, ticket).

## Due today or tomorrow
Tasks, tickets, deliverables, commitments from project pages.

## Role lens
The checks listed under "Role lens" in Context/me.md that have something to report today.

## From the dream
Two to five lines from the newest DREAM_LOG entry: what it changed, and anything under
**Needs your yes**, each answerable with one word.

## Suggested focus
Three things, in order, each tied to a goal or a deadline.

## Terms I didn't recognize
Only terms not in GLOSSARY.md and heard more than once.

## Questions
Numbered, one line each, answerable in one word where possible. Max five.

## Notes
Sources skipped or unreachable.

## Claims
- c-0001 | commitment | Send Pat the Q4 draft today | 0.85
- c-0002 | status | Acme renewal call moved to Thursday | 0.95
```

Rules:
- Link people, projects, orgs and tools with bare `[[wikilinks]]`, first mention only, and only
  to pages that exist.
- Run every name through `NAME_VARIANTS.md` before using it. Unconfirmed variants are named as such.
- Never mention a block listed in "Calendar blocks that never appear in a brief".
- Never surface a personal meeting or personal email in the briefing.
- Keep it to one screen where possible. The owner reads this on a phone sometimes.
- **Claims** lists every forward-looking assertion the recap can later check: `commitment` (the
  owner owes it), `status` (a fact about the state of something), `priority` (what you said
  matters most), `question`. Number them `c-0001` upward per day, with your confidence 0–1. The
  recap grades them; that is how the system measures whether its briefings are right.

## Midday mode

Re-read the morning file, then only what changed since it was written: new email, DMs and
mentions, calendar changes (from the calendar file's `## Changes since last sync` or the
connector), new actions. **Append** at the bottom:

```markdown
## Intraday update — HH:MM
### New and needs a reply
### Calendar changes
### Newly surfaced actions
### Claims
- c-00NN | … (continue numbering)
```

Never edit anything above it. What was known in the morning has value precisely because it
wasn't rewritten. If nothing changed, append one line saying so.

## If the file already exists in morning mode

The task ran twice or someone re-ran it. Don't overwrite. Append an `## Intraday update` instead.
