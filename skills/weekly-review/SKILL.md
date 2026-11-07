---
name: weekly-review
description: Workbench routine. On the first workday of the week it writes the week-ahead plan to Daily/YYYY-MM-DD_NEXT_WEEK_PLAN.md from last week's recaps, runs the librarian's checks and fixes what they find (frontmatter, links, index rows, stale claims, unfiled captures), makes every move into Archive/, grades the dream, and tunes the confidence bar on evidence in Tracking/Signals/YYYY-MM-DD_weekly.md. Runs as "[Workbench] Weekly Plan & Maintenance"; can be run by hand with /workbench:weekly-review.
---

# Weekly plan and maintenance

Two jobs: tell the owner what the week ahead needs, and keep the vault healthy. You run when
nothing else does, which is why you're the one routine allowed to move files and fix structure.

**You own:** `Daily/<today>_NEXT_WEEK_PLAN.md`, `Tracking/Signals/<today>_weekly.md`,
`Tracking/IMPROVEMENTS.md`, frontmatter
(`type`, `tags`, `reviewed`), link repairs, missing standard headings, `Projects/INDEX.md` row
repairs, stale claims in page prose **outside** dream-owned blocks, every move into `Archive/`,
and closing rows in `Tracking/COMMITMENTS.md`: `nightly-dream` adds rows and updates `Due`, `Who owes`, `Last evidence` and `State`; `weekly-review` alone removes rows, closing `looks-done` rows on
evidence. You also append your one
line to `Tracking/Signals/RUN_LEDGER.md`.
You never write inside a `(dream)` block or a ledger the dream owns, any `CLAUDE.md`, another
routine's `Daily/` file, `Captures/`, or the contents of `Archive/`. You never delete.

## Inputs

Root `CLAUDE.md`, `Context/me.md` (role lens), `Tracking/GOALS.md`, last week's
`Daily/*_DAILY_RECAP.md` files, last week's `Tracking/Signals/*_recap.md` and `*_dream.md`, the
last five `DREAM_LOG.md` entries, `Projects/INDEX.md` and active project pages, this week's calendar
(calendar files or connector). Build on the recaps; don't re-sweep the sources.

## 1. The plan

```markdown
---
type: weekly-plan
date: YYYY-MM-DD
tags: [weekly, plan]
status: active
source: claude-routine
---

# Week ahead — YYYY-MM-DD (week of … to …)

## Health
Routines that ran vs. expected last week (from `Tracking/Signals/RUN_LEDGER.md`, falling back to
Signals and Daily files for weeks before the ledger existed), captures unfiled for more than two
workdays, pages past their review date, open FRICTION_LOG items. Three to six lines.

## Priorities this week
Three to five, each tied to a goal in GOALS.md or a hard date.

## Carryover
Open commitments owed by the owner, oldest first, from project ledgers.
Then what the owner is waiting on from others, and who to chase.

## Role lens
The weekly checks listed under "Role lens" in Context/me.md.

## Meetings needing prep
## What the system learned
The scorecard headline (is it getting better?), rules the dream promoted last week, changes to the
confidence bar and why, and improvements done or verified.
## Proposals waiting on you
At most two, each one line with its evidence and a yes/no question.
## Needs reconciling
At most three, numbered, from the contradiction queue (step 7).
## Commitments closed
Rows closed this week (step 8), one line each with the evidence.
## Notes
```

## 2. Maintenance (the librarian's checks, fixed)

Run the checks from the `librarian` skill across every live folder, then **fix** what is safe to fix
and list the rest in the plan's Health section:

| Finding | Fix |
|---|---|
| missing `type`/`tags`/`status` | add them from the folder's `CLAUDE.md` schema |
| path-style or broken wikilinks | rewrite to bare form; repoint to the right page if unambiguous |
| a standard heading missing (e.g. `## Open commitments (mine)` on a project) | add it, empty |
| `INDEX.md` row out of step with a project page | fix the row to match the page |
| stale claim in page prose outside dream blocks | demote it to `superseded` with a forward link |
| page confirmed current | set `reviewed:` to today |
| capture lines unfiled > 2 workdays | list them in Health; the dream files them |
| near-duplicate pages | list them, propose a survivor; never merge unattended |
| one-sided relationship edge (project lists Pat, Pat doesn't list the project) | add the missing inverse |
| `## Related` disagrees with the relationship properties | rewrite the body lines from the properties |
| relationship property pointing at a page that doesn't exist | move it to plain text in `## Related`; list it for the dream |
| YAML wikilink not quoted (`org: [[Acme]]`) | quote it (`org: "[[Acme]]"`); unquoted breaks the YAML |

## 3. Archive moves

You're the only writer of moves into `Archive/`. Move, never delete, and mirror the folder:

- a `superseded` ledger entry unreferenced for 30 days → cut it into
  `Archive/Superseded/<page> ledger.md` (append), leaving the forward links intact
- a `shipped` project with no mention in 30 days → `Archive/Projects/`, and move its row to `## Archived` in `INDEX.md`
- a `former` organization quiet for 45 days → `Archive/Organizations/`, `status: archived`
- a `former` person quiet for 90 days → `Archive/People/`

Log every move under `## Moved` in your Signals file: what, from, to, when, which rule fired.

## 4. Measure and tune

From last week's `*_recap.md` (graded briefing claims) and `*_dream.md` (dream claims, graded against
whether the owner kept, edited or reverted them in the pages and git history if available), compute
per kind (status, commitment, priority, decision, person, term): kept, edited, deleted, unaddressed,
and precision = kept ÷ (kept + edited + deleted).

Write `Tracking/Signals/<today>_weekly.md` with a **Thresholds in force** table
(`kind | threshold | precision | n | changed from | why`). Move a threshold by at most 0.05 a week,
and only with at least 5 graded claims of that kind: up if precision < 80%, down if precision ≥ 95%
and many items sat in Needs your yes unanswered. If most claims are `unaddressed` (the owner isn't
giving feedback), hold every threshold and say so; silence is not agreement. Anything that would
leave the vault (send, post, change another tool) always asks, at any confidence.

## 5. Is it learning? The scorecard

Put a **Learning** table in the Signals file and its headline in the plan's What the system learned.
Compare this week with the previous four from earlier `*_weekly.md` files:

| Measure | From | Good direction |
|---|---|---|
| Draft acceptance: % `verbatim` + `light-edit` of graded drafts | recap `## Drafts` | up |
| Heavy edits per week | recap `## Drafts` | down |
| Briefing precision by kind | recap claims | up, or steady above 85% |
| Repeat corrections: a correction on a topic that already has a learned rule | captures, voice/me rules | down (a repeat means the rule isn't working: mark it `not-working` and say why) |
| Questions answered: % of digest questions with an answer within 2 workdays | recap `## Answers`, `answer:` captures | up; if low, ask fewer |
| Proposals adopted / verified | `IMPROVEMENTS.md` | up |

Say in one or two plain sentences whether the workbench is getting better and what's holding it
back. If there's too little data (fewer than 5 graded drafts, for example), say so rather than
reporting a percentage.

## 6. Improvements ledger

You own `Tracking/IMPROVEMENTS.md`.

1. **Log** every new item under **Proposals** in last week's DREAM_LOG entries, plus your own from
   FRICTION_LOG `## Open`, as `proposed` with an id (`i-NNNN`), kind and evidence. Dedupe.
2. **Follow up** on each open item, checking the real state rather than asking:
   - `accepted` → `done` when the change exists: the rule is in the named file, the skill or playbook
     exists (in the plugin, the user's skills folder, or `Resources/`), the routine prompt or schedule
     changed, the connector now shows reachable in `Context/me.md`.
   - `done` → `verified` when two weeks pass without the triggering correction or friction coming
     back; `not-working` if it comes back, with the evidence.
   - The owner accepts or declines by answering the digest question, a capture, or editing the line.
     Move declined items to `## Declined` with the date.
3. **Ask** about at most two `proposed` items per week, as questions in the plan (the next morning's
   briefing carries them into the digest). Lead with the one with the strongest evidence.

Changes to any `CLAUDE.md` are applied by the owner or by `/workbench:migrate`, never by you. Skill
proposals include a one-paragraph spec the owner can hand to Claude to build it.

## 7. The contradiction queue

Collect every `## Needs reconciling` section across the live vault. Sort the conflicts oldest
first (by the `added:` date, or the page's `updated:` if there's none). Put **at most three** in
the plan under `## Needs reconciling`, as numbered questions the next briefing carries into the
digest, each with both conflicting claims and the page each one sits on:

```
Reconcile 1. When does the Acme pilot start? [[Acme Expansion]] says 2027-01-15 (recap 11-02);
[[Acme Data]] says 2027-03-01 (capture 10-28). Which is right?
```

The owner's answers are filed by the next dream run as supersessions on the affected pages, with
the losing claim's history kept. You don't edit the sections yourself. Conflicts you didn't reach
stay queued for next week; list how many are waiting in Health.

## 8. Commitment closure

In `Tracking/COMMITMENTS.md`, for each row the dream marked `looks-done`: check the completion
evidence it cites. If it holds, close the row: cut it from the register and append it, with
today's date and the evidence, to `Archive/Superseded/COMMITMENTS ledger.md` (create it if
missing). Log the move under `## Moved` in your Signals file and list it under
`## Commitments closed` in the plan. Closing is removal from the register, never deletion: the row
survives in the archive. This is the only step in any routine that removes register rows. If the
evidence doesn't hold, leave the row as it is and say why in Health; the dream will revisit it.
Never close an `open` or `looks-stale` row.

## Finish: the run ledger

Last, append exactly one line to the bottom of `Tracking/Signals/RUN_LEDGER.md`, and never edit or
delete an existing line. Every routine appends one line when it finishes, and none edits or deletes a line; the librarian reads it:

```
- YYYY-MM-DD HH:MM | weekly | <ok|partial|failed> | wrote: <file names, or "nothing"> | gaps: <none, or a short description>
```
