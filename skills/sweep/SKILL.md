---
name: sweep
description: Workbench routine. Runs hourly through the working day on a small model. Reads every reachable source for what came in since its last good run (so after a closed-laptop night it covers the whole night), sorts each item (urgent, reply owed, prep needed, possible commitment, FYI) and appends one section to Tracking/Queue/YYYY-MM-DD_sweep.md for the briefing to use. Runs as the "[Workbench] Sweep" scheduled task; can be run by hand with /workbench:sweep.
---

# Sweep

You notice what came in, so the owner doesn't have to go looking and the briefing doesn't have to
rebuild the day from every source. You're quick and cheap: read, sort, write a short list. You
don't draft, judge priorities, or file anything into pages. Later routines do that.

**You own one file:** `Tracking/Queue/<today>_sweep.md`, which you only append to. You write
nothing else, except your one appended line in `Tracking/Signals/RUN_LEDGER.md`. You never send,
post, reply, react or mark anything read, with one exception: the urgent ping in step 6, only
when the owner has turned it on.

## Step 1: the window

Read `Tracking/Signals/RUN_LEDGER.md`. Find the newest `sweep` line marked `ok` or `partial`. The
window runs from that line's date and time to now.

- No earlier `ok` or `partial` line (first run, or a new install): the window starts 24 hours ago.
- A `failed` line doesn't move the window, so the next run reads that stretch again.
- A source that a `partial` line named in its `gaps:` gets a longer window of its own: from the
  newest sweep line that didn't name it. Every other source uses the normal window. So one broken
  connector doesn't make every run reread every source.
- Any window longer than 96 hours (that covers a long weekend): start it 96 hours ago, and record
  the rest as a gap in your ledger line (`gaps: window capped; <source> not read before
  YYYY-MM-DD HH:MM`). The briefing names it.

The dedupe in step 4 keeps an overlap from listing anything twice.

Laptops sleep and the app closes, so runs get missed. That's fine: the next run covers everything
since the last good one, because the sources keep their history.

## Step 2: read, in this order

1. The workbench root `CLAUDE.md`, then `Context/me.md` (which tools are reachable, what urgent
   means, blocks that never appear), `Context/surfacing.md` (apply **Never surface**; ignore lines
   marked `pending` or `superseded`), and `People/NAME_VARIANTS.md`.
2. The last 3 days of `Tracking/Queue/*_sweep.md`, for the `source-id`s already listed.
3. The sources, **only tools `Context/me.md` marks reachable**, for the window only:
   - email: new mail to the owner, and replies in threads they're on
   - chat: DMs, mentions, and threads the owner posted in
   - the role's tools listed as reachable (CRM, tickets, code host, and so on): items assigned to
     the owner or changed on things they own
   - the calendar: read `Daily/<today>_CALENDAR.md` if it exists and isn't `stale`, else the
     connector; meetings in the next 24 hours, for `prep-needed`
   Never read meeting transcripts. If meetings come through a recorder's connector, read only its
   summaries and next steps.

If a source can't be reached, carry on with the rest and mark the run `partial`, naming the source
in `gaps:` exactly as `me.md` names it (`gaps: CRM unreachable`), so the next run can find it.

## Step 3: sort

Each thing worth the owner's attention becomes one item, with exactly one kind:

| Kind | When |
|---|---|
| `urgent` | It matches "what urgent means" in `Context/me.md`, or `Context/surfacing.md` says always surface it and it needs action today |
| `reply-owed` | Someone asked the owner something, or is waiting on them, and they haven't answered in that thread |
| `prep-needed` | A meeting in the next 24 hours with someone outside the team, or one the owner organizes, where something should be read or brought |
| `commitment-candidate` | A promise in either direction: "I'll send it Friday", "they'll get back to us next week" |
| `fyi` | Worth knowing, nothing to do: a decision made in a thread, a date moved, a deal or ticket changed state |

Leave out: newsletters, automated notifications with nothing to act on, messages the owner already
answered, anything on the **Never surface** list, personal mail and personal events, and anything
HR-related or sensitive.

Be strict. Five good items beat thirty mixed ones. When unsure between `fyi` and nothing, pick
nothing.

## Step 4: dedupe

Skip any item whose `source-id` (message id, thread id, ticket key, event id) is already in the
last 3 days of queue files. If a thread you already listed has a new message that changes what's
needed (a new ask, a new date), list it again as a new item and say what changed.

## Step 5: write

If there are no new items, don't touch the queue file. Go to step 6.

Otherwise append one section to `Tracking/Queue/<today>_sweep.md`. Create the file with this
frontmatter if it doesn't exist:

```markdown
---
type: queue
date: YYYY-MM-DD
tags: [tracking, queue]
source: claude-routine
---

# Queue — YYYY-MM-DD (Weekday)
```

Section shape, `urgent` items first, then the order of the table above:

```markdown
## 10:20 (window 09:20–10:20)
- q-20261123-004 | reply-owed | [[Pat Lee]] | asks for the Q4 draft by Friday | evidence: "can you get me the Q4 draft by Friday" (email 09:12) | source-id: <id>
- q-20261123-005 | prep-needed | [[Acme Data]] | renewal call 15:00; last QBR notes and the open pricing question | evidence: [[Acme Data]] Current state (dream)/line 2 | source-id: <event id>
```

Rules:
- Number items `q-YYYYMMDD-NNN`, continuing from the highest number already in today's file.
- One line per item. The summary is what's needed, in plain words, in 15 words or fewer.
- `evidence:` is a verbatim quote of 25 words or fewer in double quotes with where it came from,
  or a page reference `[[Page]] section/line`. Never more than 25 quoted words.
- Run every name through `NAME_VARIANTS.md`. Link people, projects and orgs with bare
  `[[wikilinks]]` only when the page exists; otherwise write the name plainly.
- A window that crosses midnight still writes to today's file. The heading shows the real window.
- No secrets, passcodes or join-link credentials. Private calendar blocks don't appear.
- If urgent pings are on (step 6), end each `urgent` item you're about to ping with `| pinged`, so
  the briefing knows the owner already heard. Decide this now, while writing; never edit the
  section afterwards.

## Step 6: urgent ping (only if turned on)

Read `## Urgent pings` in `Context/roster.md`. Unless it says `on`, skip this step.

If this run wrote any `urgent` item, and it isn't quiet hours by `Context/surfacing.md`, send one
short message to the owner only, by the channel in `.workbench/profile.json` → `delivery`
(Slack: a DM to themselves; email: their own address; `claude` or `none`: skip). One message per
run, however many items:

```
Urgent (sweep 10:20): Pat Lee needs the Q4 draft by noon (email 09:12). 1 more in Tracking/Queue.
```

Never to anyone else, never into a shared channel. Ping exactly the items step 5 marked
`| pinged`. The dedupe keeps an item from being pinged twice. If sending fails, note it in your ledger line's `gaps:` and
don't retry.

## Step 7: the run ledger

Last, append exactly one line to the bottom of `Tracking/Signals/RUN_LEDGER.md`, and never edit or
delete an existing line. Every routine appends one line when it finishes, and none edits or deletes
a line; the librarian reads it.

```
- YYYY-MM-DD HH:MM | sweep | <ok|partial|failed> | wrote: <file name, or "nothing"> | gaps: <none, or a short description>
```

The time is when this run read up to: the end of its window. Example:
`- 2026-11-23 10:20 | sweep | partial | wrote: 2026-11-23_sweep.md | gaps: CRM unreachable`
