---
name: nightly-dream
description: Workbench routine and the heart of the self-improving loop. Each workday night it reads the day's recap and the owner's project captures, files them into people, projects, organizations, tools, the glossary and goals (dream-owned blocks and ledgers only), learns from corrections, digest answers and how drafts were edited before sending, proposes improvements, and writes what it read, changed and wasn't sure about to Tracking/DREAM_LOG.md. Runs as "[Workbench] Nightly Dream"; can be run by hand with /workbench:nightly-dream.
---

# Nightly dream

You consolidate the day into long-term memory, the way sleep does. The recap is the account of
the day; captures are what the owner settled in chat. You file both into the pages they belong
on, learn from corrections, and leave a log the owner can audit in two minutes.

You do **not** go back to the sources (see the escape hatch). You do **not** send or change
anything outside the vault.

## What you own, and nothing else

| Where | What you may write |
|---|---|
| `Tracking/DREAM_LOG.md` | a new entry at the top of `## Entries`, `## Processed captures` lines |
| `Tracking/Signals/<today>_dream.md` | the whole file (new each night) |
| `Projects/*` | `## Open commitments (mine)`, `## Decisions`, `## Current state (dream)`; relationship properties (`owner`, `people`, `orgs`, `tools`); new project pages |
| `Projects/INDEX.md` | status cells, new rows, moving rows (never change a row's link) |
| `People/*` | `## Recent (dream)`; new stubs; `role:`/`role_confirmed:`/`role_source:`/`status:` on a stated change; relationship properties (`org`, `reports_to`, `direct_reports`, `projects`, `relationship`) and `last_contact` |
| `People/NAME_VARIANTS.md` | new rows |
| `Organizations/*` | new pages; `## Recent (dream)`; `status:`; `people`, `projects`, `tools` |
| `Resources/Tools/*` | new tool pages; `## Current state (dream)`; `owner`, `vendor`, `projects` |
| `Resources/GLOSSARY.md` | `## Needs confirmation` entries; promoting confirmed terms into the table |
| `Context/me.md`, other `Context/` org pages | `## Current state (dream)` |
| `Context/voice.md` | `## Learned rules (dream)` |
| `Tracking/GOALS.md` | `## Current state (dream)` |
| `Tracking/FRICTION_LOG.md` | entries under `## Open` and `## Resolved` |
| `Tracking/COMMITMENTS.md` | new rows; `Due`, `Who owes`, `Last evidence` and `State` on existing rows. `nightly-dream` adds rows and updates `Due`, `Who owes`, `Last evidence` and `State`; `weekly-review` alone removes rows, closing `looks-done` rows on evidence. Never delete or close a row yourself. |
| `Context/surfacing.md` | learned rules, appended as dated lines; marking a line `(superseded YYYY-MM-DD)`. You append learned rules; the owner edits it directly. |
| `Tracking/Signals/RUN_LEDGER.md` | one appended line when you finish. Every routine appends here and none edits or deletes a line; it's the one documented exception to one writer per file. |

Never write any `CLAUDE.md`, any `Daily/` file, any `Meetings/` file, anything in `Captures/`, or
anything in `Archive/`. Never delete. Never move files (the weekly does that). If the root
`CLAUDE.md` lists a **standing exception** for you, it applies; otherwise these limits are absolute.
Whenever you write to a page, bump its `updated:` to today.

## Step 0: gap recovery

Before anything else, scan **every** file in `Tracking/Captures/`, whatever its date, and list each
capture line not yet recorded under `## Processed captures` in `Tracking/DREAM_LOG.md`. File all of
them in this run, oldest first, along with tonight's. A night the dream didn't run must never
strand a capture: the next run picks up everything.

Also read `Tracking/Signals/RUN_LEDGER.md` for your own last line. If one or more nights were
missed, say so in the log entry (`**Backlog:** 2 missed nights, 7 captures from 11-05 and 11-06
filed tonight`).

Step 0 runs even when tonight's recap is missing (see Inputs): filing captures doesn't depend on it.

## Inputs

1. Root `CLAUDE.md`, `Context/me.md`, `People/NAME_VARIANTS.md`, `Resources/GLOSSARY.md`.
2. The confidence bar: the newest `Tracking/Signals/*_weekly.md` "Thresholds in force" table if one
   exists, otherwise the defaults in `DREAM_LOG.md` (status 0.70 · commitment 0.80 ·
   decision/person/term 0.90).
3. Today's `Daily/<date>_DAILY_RECAP.md`. If it's missing, finish Step 0 (file the backlog
   captures), write a DREAM_LOG entry saying so, add a FRICTION_LOG `## Open` line ("recap missing
   for <date>"), append your ledger line as `partial`, and stop. Don't rebuild the day yourself.
3b. Every `Daily/*_RECONSTRUCTED_RECAP.md`, whatever its date, not yet listed under
   `## Processed captures` in `DREAM_LOG.md`. The recap writes these for a missed day, usually the
   evening after, so tonight's may cover yesterday. File them like a recap, before today's, but
   only what they state, and mark everything you file from one `source: reconstructed recap`.
   Then list each under `## Processed captures` (see Outputs) so it's never filed twice. Do this
   even when today's recap is missing.
4. `Tracking/Signals/<date>_recap.md`: graded claims, graded drafts, answers to the digest, corrections.
5. Every `Tracking/Captures/*.md` file with lines not yet listed under `## Processed captures`.
6. If `Meetings/` exists, today's meeting files above `## Transcript` only, to cross-check the
   recap's commitments and decisions.
7. Answers to yesterday's **Needs your yes**: lines the owner ticked `- [x]` (approved) or deleted
   (declined) in the previous DREAM_LOG entry, `answer:` captures, and `## Answers` in the recap
   Signals (replies to the digest).
8. For drafts graded `light-edit` or `heavy-edit`: the draft file in `Tracking/Drafts/`, and the
   recap's note of what changed.
9. `Tracking/IMPROVEMENTS.md` `## Open`, so you don't re-propose what's already pending or declined.
10. `Tracking/COMMITMENTS.md`, `Archive/Superseded/COMMITMENTS ledger.md` if it exists (closed rows,
    for the duplicate check only), and `Context/surfacing.md`.
11. The newest `Daily/*_NEXT_WEEK_PLAN.md`, for contradiction-queue questions, and any answers to
    them (captures or digest replies like "reconcile 2: the March date is right").

## What to do

**a. Apply answers.** Ticked items: write them. Deleted items: drop them and don't propose them
again for 30 days.

**Contradiction-queue answers.** When the owner answers one of the weekly's numbered reconcile
questions, file the answer as a supersession on each affected page: the winning claim stays
`live`, the losing claim is demoted to `superseded` with a forward link to the winner and the
answer as its source (`source: answer 2026-11-09 reconcile 2`). Keep the losing claim's history;
nothing is deleted. Then remove that conflict from the page's `## Needs reconciling` section, and
drop the section when it's empty. This is the one edit you make to a `## Needs reconciling`
section other than adding to it.

**b. File the day.** For each line in the recap and each unprocessed capture line:
- Decision → the project's `## Decisions` ledger (`source`, `since`, `state: live`). If it reverses
  an earlier decision, demote the old one to `superseded` with a forward link.
- Commitment owed by the owner → that project's `## Open commitments (mine)`, only at or above the
  commitment bar. Below it, it becomes a **Needs your yes** item. A commitment the recap shows done
  gets ticked `- [x]` with the evidence as its source.
- Status or progress → `## Current state (dream)` on the project, person, org, tool or goal: a few
  dated lines, newest first, replacing lines that are no longer true (demote, don't delete, if it
  was a claim someone relied on).
- Person: if named in two sources within 30 days and no page exists, create a stub using the page
  shape in `People/CLAUDE.md`. **Never guess a role.** One mention only → list under New in the log.
- Organization: create a page only for a live relationship (today's sources plus one other in 30
  days), and check `Resources/Tools/` first for a same-name tool page.
- Tool: create a page when a tool is used, not just mentioned.
- Term: unknown terms go under `## Needs confirmation` in the glossary, `state: unconfirmed`. A term
  heard three or more times unconfirmed becomes a Needs your yes question.
- Name variant: when a misspelling clearly maps to an existing person, add an `UNCONFIRMED` row to
  `NAME_VARIANTS.md` unless the owner confirmed it, then `confirmed`.
- Projects index: keep `INDEX.md` rows in step with project pages' status.

**b2. Build the relationships.** This is what turns notes into a graph. For every person, org,
project and tool touched tonight, follow **Relationships** in the root `CLAUDE.md`:
- Add each edge the day's sources state or clearly show: who works on which project, who owns it,
  which org it involves, which tools it uses, who someone reports to, which org they're at.
  "Pat and Sam discussed the Acme rollout" puts Pat and Sam on that project's `people` and the project
  on both their `projects`, and Acme on the project's `orgs`.
- **Always write both sides in the same pass** (project `people` ↔ person `projects`, org `people` ↔
  person `org`, `reports_to` ↔ `direct_reports`), and mirror the edge as a line in each page's
  `## Related` with its source.
- Set `last_contact` on a person to the date of the newest recap line, meeting or capture involving
  them and the owner directly (not just a mention).
- Edges below the person/decision confidence bar (a guess from one ambiguous line) go under Needs your
  yes instead: "Is [[Sam Ortiz]] on [[Acme Expansion]]?"
- A relationship a source says has ended (left the company, rolled off the project, churned) moves to
  `former_*` with the end date; never just deleted.
- Record edge counts in the log entry: `Relationships: +6 edges, 1 moved to former`.

**b3. Contradictions.** When two sources disagree about the same thing (two dates, two owners, two
figures), add both to a `## Needs reconciling` section on the page, each with its source and the
date you added it (`added: YYYY-MM-DD`). Never pick one. The weekly queues these for the owner.

**b4. Commitments maintenance.** After the contradiction pass, scan the pages you touched tonight
and today's captures (plus any backlog captures from Step 0) for commitment language: promises,
deadlines, "I will", "I'll send", "owes", "waiting on", "by Friday". For each:

- **New** commitment: add a row to `Tracking/COMMITMENTS.md`: `Commitment` in plain words,
  `Who owes` (`me`, a person's name, or `them:<name>` when someone else owes the owner), `Due`
  (`none` if no date was given; never guess), `Source` (the page or capture), `State: open`,
  `Last evidence` set to the date of the newest dated mention in the sources, never the date
  you're filing it (a backlog capture from two weeks ago gives a two-week-old date, so an overdue
  promise still surfaces). Skip it if a row for the same commitment already exists, **or if it was
  already closed**: check `Archive/Superseded/COMMITMENTS ledger.md` (the weekly's closed rows; read
  it for this check only) and skip anything ticked `- [x]` on its page. A closed commitment comes
  back only when a newer source than its closure date makes a genuinely new promise.
- **Changed**: when a capture or recap line states a new deadline or a new owner for an existing
  row ("pushed the Q4 draft to the 15th", "Sam's taking over the MSA review"), update `Due` or
  `Who owes` and keep the old value in `Source` with its provenance
  (`capture 11-03; due 11-05→11-15: capture 11-07`). Only on a stated change, never on a guess. A
  `looks-stale` row whose new date is in the future goes back to `open`.
- **Mentioned tonight**: set its `Last evidence` to the date of the newest mention (the source's date, not tonight's).
- **Past due, no evidence in 7 or more days**: set `State` to `looks-stale`.
- **A page tonight shows it done** (sent mail, a ticked item, a recap line): set `State` to
  `looks-done` and put the evidence in `Source` alongside the original (`capture 11-03; done: recap 11-07`).

You never delete a row and never close one. Closure is the weekly's job, on evidence. Record the
counts in the log entry: `**Commitments:** +3 rows, 2 updated, 1 rescheduled, 1 looks-done, 1 looks-stale`.

**c. Learn.** This is how the workbench improves itself:
- Every `correction:` capture and every correction in the recap Signals becomes a rule. Writing
  preferences → `## Learned rules (dream)` in `Context/voice.md`. How-they-work facts →
  `## Current state (dream)` in `Context/me.md`. A routine getting something wrong → a
  `FRICTION_LOG.md` `## Open` entry with the cause and a proposed fix.
- Claims graded `deleted` in the recap Signals: find the cause (stale page, wrong source, name
  variant) and fix the page or log the friction.
- **Drafts.** For each edited draft, compare the draft with the recap's note of what changed and
  extract the pattern: tone, length, openers, sign-offs, structure, words they add or strike. One
  edit is an anecdote; write a rule into `## Learned rules (dream)` in `Context/voice.md` only when
  the same change shows up in two or more drafts, citing them. If a learned rule is contradicted by
  later edits, demote it to `superseded`. `verbatim` drafts are evidence a rule works; note them.
- **Surfacing rules.** Same machinery as voice rules, different target. When the owner says a
  topic should always or never be in the briefing, says when not to be bothered, or corrects a
  briefing's shape for a topic ("put the numbers first for pipeline"), append the rule to the
  right section of `Context/surfacing.md` as a dated line with its source, marked `pending`. When
  the same signal shows up a second time, drop `pending`: the rule is standing and the briefing
  follows it. A rule the owner later contradicts is marked `(superseded YYYY-MM-DD)` and the new
  one goes below it. Never delete a line, and never touch lines the owner wrote.
- **Questions answered or ignored.** Act on answers. If questions keep going unanswered for a week,
  that's friction: log it, and ask fewer, sharper questions.
- **Proposals.** Notice repeated manual work (the same kind of task three times in two weeks),
  repeated corrections, and friction without a fix. Propose one concrete change for each under
  **Proposals** in the log entry, with its kind (`rule`, `skill`, `routine`, `source`, `cleanup`) and
  evidence. Skip anything already open or declined in `IMPROVEMENTS.md`. You only propose; the weekly
  logs it and follows up.

**d. Escape hatch.** If a recap line is genuinely ambiguous about one entity, you may make one
read-only source lookup for it, **at most five a night**, each recorded under Lookups. Anything past
the cap becomes a question for tomorrow's briefing.

## Outputs

**`Tracking/DREAM_LOG.md`**: insert at the top of `## Entries`:

```markdown
### YYYY-MM-DD (Weekday)

**Mode:** live
**Read:** recap YYYY-MM-DD · captures YYYY-MM-DD (N lines) · N meeting files
**Confidence bar:** status 0.70 · commitment 0.80 · decision/person/term 0.90

**Updated**
- [[Page]] — what changed. Traces to: `Daily/YYYY-MM-DD_DAILY_RECAP.md`

**New**
- [[New Person]] stub — named in recap and capture. Traces to: …

**Relationships:** +6 edges (Sam Ortiz ↔ Acme Expansion, Acme Expansion ↔ Acme Data, …), 1 moved to former

**Needs your yes**
- [ ] Mark "Send pricing to Sam" done? (sent mail 16:10 looks like it) — [[Acme Expansion]]

**Learned about how {owner} works**
- Drafts: 3 graded (1 verbatim, 2 light-edit). New voice rule: no "Hope you're well" openers (2 drafts).

**Proposals**
- skill · a /qbr-prep skill: QBR prep done by hand 3 times since 10-21 · evidence: recaps 10-21, 10-28, 11-03

**Lookups**
- none
```

Then append under `## Processed captures`: `- YYYY-MM-DD.md · N lines · filed YYYY-MM-DD`, one line
per capture file you filed from, backlog files included, and
`- YYYY-MM-DD_RECONSTRUCTED_RECAP.md · reconstructed recap · filed YYYY-MM-DD` for each
reconstructed recap you filed.

**`Tracking/Signals/RUN_LEDGER.md`**: last of all, append exactly one line to the bottom, and never
edit or delete an existing line. Every routine appends one line when it finishes, and none edits or deletes a line; the librarian reads it. Say how many backlog captures you filed:

```
- YYYY-MM-DD HH:MM | nightly-dream | <ok|partial|failed> | wrote: <file names, or "nothing"> | gaps: <none, or a short description>
```

Example: `- 2026-11-07 22:14 | nightly-dream | ok | wrote: DREAM_LOG.md, 2026-11-07_dream.md, COMMITMENTS.md, Acme Expansion.md | gaps: none; backlog: 3 captures from 11-06 filed`

**`Tracking/Signals/<today>_dream.md`**: what you claimed tonight, for future grading:

```markdown
---
type: reference
date: YYYY-MM-DD
tags: [signals, dream]
routine: nightly-dream
---

# Dream signals — YYYY-MM-DD

## Claims written tonight
- d-0001 | commitment | [[Acme Expansion]] "Send revised pricing" | 0.86 | source: …

## Lookups
## Changes
- none
```

## Quality bar

- Everything you write traces to a recap line, capture line or meeting file, and says which.
- When two sources disagree, add a `## Needs reconciling` section to the page with both, not a pick (b3).
- Position on a page follows state (live above superseded), not recency of writing.
- Keep `Recent (dream)` and `Current state (dream)` blocks short: five lines or fewer, newest first.
- Report-only is fine: on the first three nights of a new workbench, or if anything looks off
  (missing recap, many deleted claims), write only the DREAM_LOG entry with `Mode: report-only`
  and put everything else under Needs your yes.
