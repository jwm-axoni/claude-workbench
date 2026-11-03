---
name: weekly-review
description: Workbench routine. On the first workday of the week it writes the week-ahead plan to Daily/YYYY-MM-DD_NEXT_WEEK_PLAN.md from last week's recaps, runs the librarian's checks and fixes what they find (frontmatter, links, index rows, stale claims, unfiled captures), makes every move into Archive/, grades the dream, and tunes the confidence bar on evidence in Tracking/Signals/YYYY-MM-DD_weekly.md. Runs as "[Workbench] Weekly Plan & Maintenance"; can be run by hand with /workbench:weekly-review.
---

# Weekly plan and maintenance

Two jobs: tell the owner what the week ahead needs, and keep the vault healthy. You run when
nothing else does, which is why you're the one routine allowed to move files and fix structure.

**You own:** `Daily/<today>_NEXT_WEEK_PLAN.md`, `Tracking/Signals/<today>_weekly.md`, frontmatter
(`type`, `tags`, `reviewed`), link repairs, missing standard headings, `Projects/INDEX.md` row
repairs, stale claims in page prose **outside** dream-owned blocks, and every move into `Archive/`.
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
Routines that ran vs. expected last week (from Signals and Daily files), captures unfiled for
more than two workdays, pages past their review date, open FRICTION_LOG items. Three to six lines.

## Priorities this week
Three to five, each tied to a goal in GOALS.md or a hard date.

## Carryover
Open commitments owed by the owner, oldest first, from project ledgers.
Then what the owner is waiting on from others, and who to chase.

## Role lens
The weekly checks listed under "Role lens" in Context/me.md.

## Meetings needing prep
## What the system learned
What the dream promoted into rules last week, what changed in the confidence bar, and why.
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

## 5. One improvement

Pick the single most useful fix for the system itself from FRICTION_LOG `## Open` and last week's
"Learned about how they work" notes, and propose it in the plan under What the system learned:
a rule to add to a folder `CLAUDE.md`, a routine tweak, or a new playbook. Write it as a proposal;
the owner (or `/workbench:migrate`) applies changes to `CLAUDE.md` files.
