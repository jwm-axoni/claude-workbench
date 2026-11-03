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
| `Projects/*` | `## Open commitments (mine)`, `## Decisions`, `## Current state (dream)`; new project pages |
| `Projects/INDEX.md` | status cells, new rows, moving rows (never change a row's link) |
| `People/*` | `## Recent (dream)`; new stubs; `role:`/`role_confirmed:`/`role_source:`/`status:` on a stated change |
| `People/NAME_VARIANTS.md` | new rows |
| `Organizations/*` | new pages; `## Recent (dream)`; `status:` |
| `Resources/Tools/*` | new tool pages; `## Current state (dream)` |
| `Resources/GLOSSARY.md` | `## Needs confirmation` entries; promoting confirmed terms into the table |
| `Context/me.md`, other `Context/` org pages | `## Current state (dream)` |
| `Context/voice.md` | `## Learned rules (dream)` |
| `Tracking/GOALS.md` | `## Current state (dream)` |
| `Tracking/FRICTION_LOG.md` | entries under `## Open` and `## Resolved` |

Never write any `CLAUDE.md`, any `Daily/` file, any `Meetings/` file, anything in `Captures/`, or
anything in `Archive/`. Never delete. Never move files (the weekly does that). If the root
`CLAUDE.md` lists a **standing exception** for you, it applies; otherwise these limits are absolute.
Whenever you write to a page, bump its `updated:` to today.

## Inputs

1. Root `CLAUDE.md`, `Context/me.md`, `People/NAME_VARIANTS.md`, `Resources/GLOSSARY.md`.
2. The confidence bar: the newest `Tracking/Signals/*_weekly.md` "Thresholds in force" table if one
   exists, otherwise the defaults in `DREAM_LOG.md` (status 0.70 · commitment 0.80 ·
   decision/person/term 0.90).
3. Today's `Daily/<date>_DAILY_RECAP.md`. If it's missing, write a DREAM_LOG entry saying so, add a
   FRICTION_LOG `## Open` line ("recap missing for <date>"), and stop. Don't rebuild the day yourself.
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

## What to do

**a. Apply answers.** Ticked items: write them. Deleted items: drop them and don't propose them
again for 30 days.

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

**Needs your yes**
- [ ] Mark "Send pricing to Sam" done? (sent mail 16:10 looks like it) — [[Acme Expansion]]

**Learned about how {owner} works**
- Drafts: 3 graded (1 verbatim, 2 light-edit). New voice rule: no "Hope you're well" openers (2 drafts).

**Proposals**
- skill · a /qbr-prep skill: QBR prep done by hand 3 times since 10-21 · evidence: recaps 10-21, 10-28, 11-03

**Lookups**
- none
```

Then append under `## Processed captures`: `- YYYY-MM-DD.md · N lines · filed YYYY-MM-DD`.

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
- When two sources disagree, add a `## Needs reconciling` section to the page with both, not a pick.
- Position on a page follows state (live above superseded), not recency of writing.
- Keep `Recent (dream)` and `Current state (dream)` blocks short: five lines or fewer, newest first.
- Report-only is fine: on the first three nights of a new workbench, or if anything looks off
  (missing recap, many deleted claims), write only the DREAM_LOG entry with `Mode: report-only`
  and put everything else under Needs your yes.
