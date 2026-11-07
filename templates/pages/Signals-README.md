---
type: reference
tags: [tracking, signals, meta]
status: active
updated: {{created_date}}
---

# Signals

The measurement layer. One append-only file per date per routine: `YYYY-MM-DD_<routine>.md`.
The name fixes the writer, so two routines never contend for one file.

The one exception is `RUN_LEDGER.md`: every routine appends one line when it finishes, and none
edits or deletes a line. The librarian reads it. Appends are dated lines, never edits, so nothing
contends.

## What goes in

A routine's **claims** (what it asserted and how confident it was), the **outcomes** (what
{{preferred_name}} actually did with them), and any **change** to its own thresholds. That triplet
is what lets the weekly move a threshold on evidence. The weekly also logs every archive move
here under `## Moved`: what, from where, to where, when, which rule.

## Three rules

- **One writer per file.** Guaranteed by the filename.
- **A grader never edits what it grades.** Scoring a briefing writes a verdict here; it doesn't touch the briefing.
- **Append-only, including the misses.** A measurement layer that loses its wrong calls reports a precision it never had.

## Entry shape

```markdown
## YYYY-MM-DD — nightly-dream

### Claims
- `c-0001` commitment · "Send Pat the Q4 draft" → [[Project]] `confidence: 0.86` `source: <file>`

### Outcomes (graded YYYY-MM-DD)
- `c-0001` kept verbatim → **true positive**

### Changes
- none this run
```
