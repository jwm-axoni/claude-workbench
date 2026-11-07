---
type: system
updated: {{created_date}}
---

# Tracking

Things tracked over time. Unlike the rest of the vault these are **living logs that get
appended to**, not pages per entity.

## Files

- `GOALS.md` — the objectives that count and the hard external dates
- `COMMITMENTS.md` — every promise in flight, both ways, one row each, with its state
- `FRICTION_LOG.md` — what went wrong in Claude's own setup, and the fix
- `DREAM_LOG.md` — what `nightly-dream` read, learned and changed each night
- `Captures/` — one file per day, written only by the Claude project
- `Signals/` — one file per date per routine: claims, outcomes, changes, archive moves
- `Signals/RUN_LEDGER.md` — one line per routine run; a missing line is a missed run
- `Drafts/` — every draft the project hands the owner to send, saved as given, graded by the recap
- `IMPROVEMENTS.md` — what the system proposed to change about itself, and whether it worked

## Frontmatter

```yaml
---
type: reference
tags: [tracking, <topic>]
status: active
updated: YYYY-MM-DD
---
```

## Who writes what

- `DREAM_LOG.md`: `nightly-dream`, plus {{preferred_name}} ticking `- [x]` under `Needs your yes`.
- `GOALS.md`: {{preferred_name}} owns the objectives; `nightly-dream` writes `## Current state (dream)`.
- `FRICTION_LOG.md`: `nightly-dream` maintains `## Open` / `## Resolved`; anyone may add an Open line.
- `Captures/`: the Claude project only. `nightly-dream` reads and files it, never edits it.
- `Signals/`: each file has one writer, fixed by its name (`YYYY-MM-DD_<routine>.md`).
- `Signals/RUN_LEDGER.md`: every routine appends one line when it finishes, and none edits or
  deletes a line. The librarian reads it. The one documented exception to one writer per file.
- `COMMITMENTS.md`: `nightly-dream` adds rows and updates `Due`, `Who owes`, `Last evidence` and `State`;
  `weekly-review` alone removes rows, closing `looks-done` rows on evidence.
- `Drafts/`: the project (and the briefing, for reply drafts). Final once its chat ends.
- `IMPROVEMENTS.md`: `weekly-review` only. The dream proposes in `DREAM_LOG.md`; the weekly logs and follows up.

## Conventions

Every entry carries a date and links the people and projects involved. Nothing is deleted from a
log: an item that's done moves to `Resolved`. A grader never edits what it grades.
