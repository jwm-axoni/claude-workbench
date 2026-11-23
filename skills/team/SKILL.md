---
name: team
description: Workbench routine. Runs before the morning briefing and before the midday update. Takes what the hourly sweep queued and does the work ahead of time with three personas, as Context/roster.md allows: the drafter writes reply drafts into Tracking/Drafts/, prep writes meeting prep pages into Tracking/Prep/, and the editor checks both before they're saved. Decisions it shouldn't make alone go to Tracking/NEEDS_YOU.md with a recommended answer. Never sends anything. Runs as the "[Workbench] Team" scheduled task; can be run by hand with /workbench:team.
---

# Team

The sweep noticed what came in. You do the work before the owner gets to it, so the briefing can
say "a reply to Pat is drafted" instead of "Pat is waiting". Everything you make is a draft or a
page. The owner decides what goes out. You never send, post, reply or change anything outside
the workbench.

**You own:**
- new draft files in `Tracking/Drafts/`, marked `by: team-drafter`
- new pages in `Tracking/Prep/`
- `Tracking/Signals/<today>_team.md`
- `open` lines appended to `Tracking/NEEDS_YOU.md`
- your one appended line in `Tracking/Signals/RUN_LEDGER.md`

You write nothing else. A file you saved in an earlier run is final: never edit it.

## Step 0: is there work?

This check comes first, before any other reading, because most runs should be cheap.

1. Read `Context/roster.md`. Personas marked `off` don't run.
2. Read the queue: `Tracking/Queue/*_sweep.md` for today and the last workday.
3. Read the `### Handled` lists in `Tracking/Signals/*_team.md` for the last 3 days. A `q-` id
   listed there is done.
4. Read `Tracking/NEEDS_YOU.md` for `answered` lines dated in the same 3 days, on items you raised,
   that no `### Answers acted on` list in those Signals files mentions yet. Older answers were
   acted on by an earlier run (or are past acting on); never go back to them.

If there's no unhandled `urgent`, `reply-owed` or `prep-needed` item, no new answer, and (for
prep) no meeting in the next 24 hours that needs a page and has none, append your ledger line
with `wrote: nothing` and stop.

## Read, for the items you'll work on

The workbench root `CLAUDE.md`, then `Context/me.md`, `Context/voice.md` (all of it, including
`## Learned rules (dream)`), `Context/surfacing.md` and `People/NAME_VARIANTS.md`. Then, for each
item, the pages it touches: the person's `People/` page, the project or organization page,
`Tracking/COMMITMENTS.md` rows that name them, and the source thread itself through the tool
`me.md` marks reachable. Never read meeting transcripts; read only above the `## Transcript`
marker in `Meetings/`.

## Drafter

For each unhandled `reply-owed` item, and each `urgent` item that needs a reply, oldest first,
up to the day's limit in `roster.md` (count today's files in `Tracking/Drafts/` marked
`by: team-drafter`):

- Write the reply the owner would send, in their voice from `voice.md`, sized to the
  channel. Answer what was asked. Don't invent facts, dates or commitments: every claim in the
  draft must come from the thread, a page, or the calendar.
- Save it as `Tracking/Drafts/<today>_reply-<person>-<topic>.md`, in the shape in
  `Tracking/Drafts/README.md`, with two more frontmatter fields: `by: team-drafter` and
  `queue: <q- id>`. The recap grades it against what was really sent, like every other draft.
- Don't draft when the reply needs a decision only the owner can make (a price, a date, a yes or
  no on a request, anything about a person's job). Add a Needs-you item instead.
- Never draft anything personal or HR-related, or to someone on the **Never surface** list.

## Prep

For each unhandled `prep-needed` item, and each meeting in the next 24 hours with people outside
the team or that the owner organizes that has no page yet, up to the day's limit:

- Write `Tracking/Prep/<meeting date>_<slug>.md` in the shape in `Tracking/Prep/README.md`, with
  `by: team-prep` and `queue: <q- id>` when it came from the queue.
- Who's coming (linked to existing `People/` pages), where things stand, what's open both ways
  (from `COMMITMENTS.md` and the pages), and the one or two things to bring. Every line traces to
  a source or a page.
- Skip routine internal meetings, and anything in a calendar block `me.md` says never appears.

**Role workers.** Each line under `## Role workers` in `roster.md` is one more job. Do what it says,
writing only prep pages (`Tracking/Prep/<date>_<worker>-<slug>.md`, `by: team-<worker>`) or
Needs-you items. If a line asks for anything else (sending, editing a page, writing elsewhere),
skip it and record why under `### Held`.

## Editor

Check every draft and page from this run before it's saved:

1. Every fact traces to the thread, a page, or the calendar. Nothing is guessed.
2. It follows `voice.md`, including the learned rules, and fits the channel's length.
3. Names went through `NAME_VARIANTS.md`; links point only to pages that exist.
4. Nothing from **Never surface**, no private calendar block, no secrets, no transcript text.
5. A draft doesn't promise anything the owner hasn't already promised.

If it fails, send it back once, naming what to fix, and check the revision. If the revision still
fails, don't save it: list it under `### Held` with the reason, and add a Needs-you item if the
owner still needs to act ("Pat is waiting on the Q4 draft; I couldn't draft it without the new
numbers. Send it yourself today?").

## Needs you

Append at most 3 new items per run to `Tracking/NEEDS_YOU.md`, under `## Items`, numbered `n-NNN`
from the highest id already in the file:

```
- 2026-11-23 07:46 | n-007 | Reply to Pat now, or after Thursday's call? | recommend: after the call, so the reply can include the new numbers | from: q-20261123-004 | open
```

Each question is answerable in a word or two, and the recommendation says which answer you'd pick
and why, in one line.

**Answers.** For each new answer from step 0 (the last 3 days only), act within what you own: write a new
draft (`-v2` in its slug) if the answer changes what to say, or do nothing if it doesn't. Never
change an earlier file. List it under `### Answers acted on`.

## Signals file

Append one section per run to `Tracking/Signals/<today>_team.md` (create it with frontmatter
`type: signals`, `date:`, `routine: team` if it doesn't exist):

```markdown
## 07:45 run

### Handled
- q-20261123-004 → Tracking/Drafts/2026-11-23_reply-pat-q4-draft.md
- q-20261123-005 → Tracking/Prep/2026-11-23_acme-renewal.md
- q-20261123-006 → skipped: needs a pricing decision (n-007)

### Editor
- 2026-11-23_reply-pat-q4-draft | sent back once: opened with a pleasantry voice.md says to cut | passed
- 2026-11-23_acme-renewal | passed

### Held
- none

### Answers acted on
- n-005 → Tracking/Drafts/2026-11-23_reply-jo-dates-v2.md
```

Every queue item you looked at goes under `### Handled`, including the ones you skipped and why,
so the next run doesn't look at it again.

## Finish: the run ledger

Last, append exactly one line to the bottom of `Tracking/Signals/RUN_LEDGER.md`, and never edit or
delete an existing line.

```
- YYYY-MM-DD HH:MM | team | <ok|partial|failed> | wrote: <file names, or "nothing"> | gaps: <none, or a short description>
```

Mark the run `partial` if a source the items needed couldn't be reached.
