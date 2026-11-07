---
name: eod-recap
description: Workbench routine. Sweeps every reachable source once at the end of the workday and writes the one account of the day to Daily/YYYY-MM-DD_DAILY_RECAP.md, with a source and date on every line, then grades the morning briefing's claims and every saved draft (sent verbatim, edited, or not sent) into Tracking/Signals/YYYY-MM-DD_recap.md, and collects answers to the briefing digest. The nightly dream and the weekly build on this file instead of going back to the sources. Runs as "[Workbench] End-of-Day Recap"; can be run by hand with /workbench:eod-recap.
---

# End-of-day recap

The recap is **the record of the day**. Every source reaches the vault through it. The dream and
the weekly read it instead of forming their own picture, so two routines never describe the same
day differently. Completeness and provenance matter more here than polish.

**You own two files:** `Daily/<today>_DAILY_RECAP.md` and `Tracking/Signals/<today>_recap.md`,
plus `Daily/<date>_RECONSTRUCTED_RECAP.md` for a workday whose recap never ran (see below). Nothing
else, except your one appended line in `Tracking/Signals/RUN_LEDGER.md`.

## Read first

Root `CLAUDE.md`, `Context/me.md`, `People/NAME_VARIANTS.md`, `Resources/GLOSSARY.md`, and today's
`Daily/<today>_MORNING_BRIEFING.md` (including intraday updates) and `_CALENDAR.md` if present.
Then `Tracking/Captures/<today>.md` if it exists: the owner's project chats from today.

## Source order (binding)

Read in this order, and let the earlier source win when it already settles something:

1. **Today's captures** (`Tracking/Captures/<today>.md`), first. Cite the capture for any claim it
   supports (`source: capture 14:20`). A settled fact that's already in a capture is never
   re-derived from scratch from email or chat; the capture is the owner's own account of it.
2. **Calendar events**: what actually happened, from today's calendar file or the connector.
3. **Meeting notes**, if `Meetings/` exists.
4. **Project and people pages**, for what was already known going in.
5. **Git activity**, if the vault is a git repository: commits made today, including cloud
   routine branches.

The live sweep below fills in what those don't cover.

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
- Moved the Acme pilot to January — decided by [[Pat Lee]] `source: email 14:02` `date: YYYY-MM-DD` `evidence: "let's move the pilot to January"` `confidence: 0.95`

## Commitments
### Owed by {owner}
- [ ] Send revised pricing — to [[Sam Ortiz]], by Fri `source: meeting 2026-…-acme-sync` `date: …` `evidence: "I'll send revised pricing by Friday"` `confidence: 0.90`
### Owed to {owner}
- [ ] Legal review of MSA — [[Dana Kim]], no date `source: chat DM 11:40` `date: …` `evidence: [[Acme MSA]] Open commitments (mine)/line 2` `confidence: 0.80`

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
bug. Every new line there also carries its lineage: `evidence:`, a verbatim quote of 25 words or
fewer in double quotes or a page reference in the form `[[Page]] section/line`, and `confidence:`,
the same 0–1 grade the briefing's claims use. Lines written before v0.2.0 don't have them; leave
those as they are. Don't merge two sources' versions of an event into one claim; if they disagree, write both and
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

## Grade the drafts

For each file in `Tracking/Drafts/` dated today or in the previous two workdays and not yet graded
in an earlier `*_recap.md`, look for what was actually sent: sent email, the owner's own Slack
messages, edited docs, as reachable. Compare by recipient, topic and wording, and grade:

| Grade | Means |
|---|---|
| `verbatim` | sent as written, or typo-level changes |
| `light-edit` | same message, some wording changed |
| `heavy-edit` | rewritten: structure, tone or substance changed |
| `not-sent` | nothing matching went out within two workdays (grade only once the window has passed) |
| `unknown` | the channel isn't reachable |

Add to the Signals file under `## Drafts`, one line each, and for edits say **what** changed in a
few words, without copying the sent text:

```markdown
## Drafts
- 2026-11-03_pricing-reply-pat | email | light-edit | cut the opening pleasantry; "Hi Pat" not "Hello Pat"; shorter close
- 2026-11-03_launch-update | slack | heavy-edit | reordered to lead with the date; dropped two bullets; more casual
```

## Collect answers to the digest

If the briefing digest went out by Slack or email, read the owner's replies to it today. Each
answer to a numbered question goes under `## Answers` in the Signals file:
`- briefing YYYY-MM-DD Q2 — yes, it's Jamie Torres`. Answers given in the project arrive as
`answer:` captures; list those too, so the dream has one place to read them.

## If the recap already exists

Append an `## Update — HH:MM` section with only what's new since; don't rewrite. Same for the
Signals file.

## Late runs

If you run more than 2 hours after the scheduled time, add `late: true` and `scheduled: HH:MM` to
the frontmatter and say so under the title: "_Ran at 23:05, scheduled 18:00. Sources read up to
23:05._" Never present a late recap as if it ran on time.

## A missed day: the reconstructed recap

Check the previous workday. If it has no `Daily/<that date>_DAILY_RECAP.md` and no
`_RECONSTRUCTED_RECAP.md` yet, it has no record, whatever `Tracking/Signals/RUN_LEDGER.md` says:
no `eod-recap` line at all, or a `failed` line from a run that died before writing its file. Cover
that day in a **separate, short file**, `Daily/<that date>_RECONSTRUCTED_RECAP.md`, before writing
today's. A ledger line is never proof the day was recorded; only the file is.

```markdown
---
type: daily-recap
date: YYYY-MM-DD
tags: [daily, recap]
status: reconstructed
source: claude-routine
reconstructed_on: YYYY-MM-DD
---

# Reconstructed recap — YYYY-MM-DD (Weekday)

_Reconstructed on YYYY-MM-DD because this day's recap didn't run. Not a full record._

## Could not be swept
- Chat history for that day isn't reachable now
- No calendar history: only the copy in `Daily/YYYY-MM-DD_CALENDAR.md`, last synced HH:MM

## Decisions made / Commitments / What happened
Only what the sources still show, same line shape as a normal recap (`source:`, `date:`,
`evidence:`, `confidence:`).
```

List every source you couldn't sweep for that date, honestly. Don't grade that day's briefing
(nobody can tell now what was kept). Never present it as a normal recap, and never reconstruct
more than the one previous workday; older gaps go under Notes in today's recap as days with no
record.

## Finish: the run ledger

Last, append exactly one line to the bottom of `Tracking/Signals/RUN_LEDGER.md`, and never edit or
delete an existing line. Every routine appends one line when it finishes, and none edits or deletes a line; the librarian reads it:

```
- YYYY-MM-DD HH:MM | eod-recap | <ok|partial|failed> | wrote: <file names, or "nothing"> | gaps: <none, or a short description>
```

Name the reconstructed file under `wrote:` when you wrote one, and the missed day under `gaps:`.
