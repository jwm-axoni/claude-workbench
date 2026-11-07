---
type: system
updated: {{created_date}}
---

# Meetings

One file per meeting, exported from {{meetings_source}}. This folder is the record of what was
said, decided and assigned. It is **append-only and machine-written**: don't hand-edit a file
here; the next export may overwrite it, and the fix belongs on the project page anyway.

**{{meetings_source}} owns this folder; the workbench only reads it.** No routine writes, moves or
archives a file here, whatever its age. The routines read only recent files, and what matters in a
meeting (decisions, next steps) is lifted onto project and people pages by the recap and the
dream, so old files cost nothing.

## The rule that matters most

**Read only what is above the `## Transcript` marker** (or the export's equivalent). Summaries,
next steps and decisions sit above it; below it is a raw transcript that can run past 100 KB.
Read a transcript body only when someone asks what was literally said, and then only that file.

## Next steps are the open-loops ledger

A next-step line owned by {{preferred_name}} is a commitment **they owe**. Any other owner is
something **they're waiting on**. An unattributed line in a meeting {{preferred_name}} attended is
probably theirs, but say so rather than asserting it. A next step is only true *as of that
meeting*; check the project page's `## Open commitments (mine)` for current state.

## Conventions

- Participant names are transcription output. Run them through `People/NAME_VARIANTS.md`.
- Not every meeting is work. Check the title and participants before pulling one into a briefing.
- If two files share an export id, they're the same meeting exported twice: read the longest.
- A routine that finds no meeting file for a date says there's no record, not that nothing happened.
