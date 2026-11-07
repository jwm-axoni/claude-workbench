---
name: daily-briefing
description: Workbench routine. Writes the morning briefing to Daily/YYYY-MM-DD_MORNING_BRIEFING.md (what today needs, replies owed, risks, focus, what the dream learned, questions) and, in midday mode, appends an intraday update below it. Runs as the "[Workbench] Morning Briefing" and "[Workbench] Midday Update" scheduled tasks; can be run by hand with /workbench:daily-briefing.
---

# Daily briefing

The briefing is the surface the owner reads to start the day. It is not the record (the recap
is), so it can be opinionated about priorities, but every fact in it must trace to a source.

**You own one file:** `Daily/<today>_MORNING_BRIEFING.md`. In midday mode you append to it. You
write nothing else in the vault, except your one appended line in `Tracking/Signals/RUN_LEDGER.md`. The one thing you may send is the **digest**, to the owner only,
by the channel in `.workbench/profile.json` → `delivery` (the root `CLAUDE.md` standing exception).

## Step 0: system health

Before composing anything, read `Tracking/Signals/RUN_LEDGER.md` and `.workbench/schedules.json`.
From the schedules, work out which routines should have run since the last briefing (normally
yesterday's recap and dream, the calendar syncs, and on the first workday the weekly). For each
one, look for its ledger line.

- A routine with no line, or a line marked `failed`, is a gap. Name it in the briefing, first line
  under **Urgent and at risk**, in plain words with the consequence: "The dream didn't run last
  night, so 4 captures are unfiled." "Yesterday's recap didn't run, so this briefing has no record
  of yesterday afternoon." Count the consequence from the vault (unfiled capture lines, the missing
  file), don't guess it.
- A `partial` line: mention its `gaps:` text under Notes.
- Put the same one-line warning first in the digest.

Never silently compose over a gap. If the ledger itself is missing (a vault older than v0.2.0),
fall back to checking for the files those routines write, and say under Notes that you did.

In a repo vault, if the root `CLAUDE.md` or the project instructions say cloud runs push to
`claude/` branches, check that the working copy has merged them first (see the `schedules` skill).
If unmerged `claude/` branches are newer than the working copy, say so as a gap: the vault you're
reading is behind.

## Read first, in this order

1. Root `CLAUDE.md`, then `Context/me.md` (role lens, what urgent means, reachable tools, blocks
   that never appear), then **`Context/surfacing.md`**, then `People/NAME_VARIANTS.md`,
   `Tracking/GOALS.md`, `Resources/GLOSSARY.md`.

   Apply `surfacing.md` to everything that follows. **Always surface** topics go in even when
   there's little news on them. **Never surface** topics stay out of the file and the digest.
   During **Quiet hours**, hold proactive items (a midday update in quiet hours writes its file
   but sends nothing). **Format preferences** set the shape for their topic. Lines marked
   `pending` or `superseded` aren't rules yet; ignore them.
2. The **ledgers**, before any live source, so you don't re-report what the vault already knows:
   - yesterday's (or the last workday's) `Daily/*_DAILY_RECAP.md`, especially open follow-ups and
     tomorrow-prep
   - the newest entry in `Tracking/DREAM_LOG.md`, especially **Needs your yes**
   - `## Open commitments (mine)` on active projects in `Projects/INDEX.md`
   - **`Tracking/COMMITMENTS.md`** (see Commitments below)
   - today's `Daily/<today>_CALENDAR.md` if it exists and isn't `stale`; otherwise the calendar connector
3. Then the live sources, **only tools `Context/me.md` marks reachable**, since the last recap:
   email, chat DMs and mentions, tickets or tasks due today or tomorrow, the role-specific sources
   (CRM, code host, etc.). If meetings come through the recorder's connector
   (`meetings_via: connector` in the profile), yesterday's meeting summaries and next steps there,
   never transcripts. If `Meetings/` exists, yesterday's meeting files, **above the
   `## Transcript` marker only**.

If a source can't be reached, say so in one line under Notes. Never fill a gap with a guess.

## Commitments

From `Tracking/COMMITMENTS.md`:

- A row past its `Due` date with no `Last evidence` in 7 or more days goes under **Urgent and at
  risk**, phrased as a question, never an assertion: "Did the Q4 draft go to [[Pat Lee]]? It was
  due 11-03 and nothing's mentioned it since 10-29." For `them:<name>` rows, ask whether to chase.
- A row due within 2 days is mentioned once, in **Today**.
- Rows marked `looks-done` are not surfaced. The weekly closes them.
- You never write to the register. If a question you ask gets answered, the answer comes back as a
  capture and the dream updates the row.

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
- c-0001 | commitment | Send Pat the Q4 draft today | confidence: 0.85 | evidence: "can you get me the Q4 draft by Friday" (email from [[Pat Lee]] 09:12)
- c-0002 | status | Acme renewal call moved to Thursday | confidence: 0.95 | evidence: [[Acme Data]] Current state (dream)/line 1
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
- **Every new claim carries its lineage.** `confidence:` is the 0–1 grade. `evidence:` is either a
  verbatim quote of 25 words or fewer in double quotes, with where it came from, or a page
  reference in the form `[[Page]] section/line`. Claims written before v0.2.0 have the confidence
  as a bare fourth field and no evidence; leave them as they are, never rewrite them.

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
- c-00NN | … | confidence: … | evidence: … (continue numbering)
```

Never edit anything above it. What was known in the morning has value precisely because it
wasn't rewritten. If nothing changed, append one line saying so.

If the update runs more than 2 hours after its scheduled time, say so in its heading:
`## Intraday update — HH:MM (ran late; scheduled HH:MM)`.

## Deliver the digest

After writing the file, send a short digest by `delivery.channel`:

- **slack**: a DM to the owner themselves (or the private channel named in `delivery.target`).
  Never any other person or shared channel.
- **email**: one email to the owner's own address, subject `Briefing — <Weekday> <date>`.
- **claude**: make the digest your final message for this run; the Claude app shows it.
- **none**: skip.

Digest shape, at most 15 lines, no tables:

```
Morning, <name>. <Weekday> <date>.
Focus: 1) … 2) … 3) …
Watch: <the one or two real risks>
Today: <N meetings>; prep needed for <meeting> (<what>)
From the dream: <one line>
Questions (reply with the number):
1. Is "Send Pat the draft" done? (yes/no)
2. Is "JT" Jamie Torres? (yes/no)
Full briefing: Daily/<date>_MORNING_BRIEFING.md
```

Number questions `Q1…` to match the file's `## Questions`, so replies like "1 yes, 2 no it's Jo
Tan" map back. Put **Needs your yes** items from the dream log first. On the first workday, also
carry the newest weekly plan's `## Needs reconciling` questions, keeping their "Reconcile N" labels
so the answer ("reconcile 2: March") maps back. Record the channel and time
sent under `## Notes` in the file (e.g. `Delivered: slack 07:58`). If sending fails, note the
failure there and in the digest's next successful send; don't retry in a loop.

In **midday mode**, send only if the update has something new that needs action (when
`delivery.midday` is `if-changed`, the default), as a reply in the same Slack thread or email thread
when possible.

Never put anything in a digest that the briefing itself must not show: private calendar blocks,
personal meetings, secrets, guarded data.

## If the file already exists in morning mode

The task ran twice or someone re-ran it. Don't overwrite. Append an `## Intraday update` instead.

## Late runs

If the morning briefing runs more than 2 hours after its scheduled time (a laptop that was asleep,
a catch-up run), add `late: true` and `scheduled: HH:MM` to the frontmatter and say it under the
title: "_Ran at 11:40, scheduled 08:00._" Items already past by then go under Notes, not Today.

## Finish: the run ledger

Last, append exactly one line to the bottom of `Tracking/Signals/RUN_LEDGER.md`, and never edit or
delete an existing line. Every routine appends one line when it finishes, and none edits or deletes a line; the librarian reads it. The routine is `daily-briefing` in morning mode and `midday-update` in
midday mode. Include every gap Step 0 found.

```
- YYYY-MM-DD HH:MM | daily-briefing | <ok|partial|failed> | wrote: <file names, or "nothing"> | gaps: <none, or a short description>
```

Example: `- 2026-11-09 08:01 | daily-briefing | ok | wrote: 2026-11-09_MORNING_BRIEFING.md | gaps: nightly-dream missing for 11-06`
