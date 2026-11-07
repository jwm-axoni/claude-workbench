---
type: reference
tags: [tracking, commitments]
status: active
updated: {{created_date}}
---

# Commitments

Every promise in flight, both ways: what {{preferred_name}} owes, and what other people owe {{preferred_name}}.

<!--
One row per commitment. Rules for each column:
- Who owes: `me`, a person's name (as a bare [[wikilink]] when they have a page), or `them:<name>` when someone else owes {{preferred_name}}.
- Due: YYYY-MM-DD, or `none` when no date was given. Never guess one.
- Source: the page or capture the commitment came from.
- State: exactly one of `open`, `looks-done`, `looks-stale`.
- Last evidence: the most recent date any vault page mentioned progress.

Who writes this file: `nightly-dream` adds rows and updates `Last evidence` and `State`;
`weekly-review` alone removes rows, closing `looks-done` rows on evidence. The dream never
deletes a row and never closes one. A closed row is moved to `Archive/Superseded/COMMITMENTS ledger.md`, not deleted.
-->

| Commitment | Who owes | Due | Source | State | Last evidence |
|---|---|---|---|---|---|
