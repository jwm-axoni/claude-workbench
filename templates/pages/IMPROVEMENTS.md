---
type: reference
tags: [tracking, improvements, meta]
status: active
updated: {{created_date}}
---

# Improvements

Every change the workbench proposes to itself, and whether it worked. Owned by the weekly routine.
The dream and the weekly *propose*; {{preferred_name}} decides; the weekly then *checks* whether the
change was made and whether it fixed the problem.

## How an entry moves

`proposed` → `accepted` / `declined` → `done` → `verified` (the problem stopped) or `not-working`
(the same correction or friction came back after the fix)

```markdown
- i-0001 · skill · "A /qbr-prep skill: QBR prep was done by hand 4 times in 3 weeks"
  `proposed: 2026-11-10` `state: proposed` `evidence: 2026-10-21, 10-28, 11-04, 11-06 recaps`
```

Kinds: `rule` (a line in a CLAUDE.md or voice.md), `skill` (a new skill or playbook), `routine` (a
change to a scheduled routine), `source` (connect a tool), `cleanup`.

A declined proposal isn't raised again for 60 days unless the evidence doubles.

## Open

## Done

## Declined
