---
type: reference
tags: [tracking, queue]
status: active
updated: {{created_date}}
---

# Queue

What came in through the day, sorted before {{preferred_name}} has to look for it. The hourly
`sweep` routine reads the reachable sources (email, chat, calendar, the role's tools) for
everything since its last run, and writes what matters here. The briefing and midday update
read it, so they don't go back to every source on their own.

One file per day, `YYYY-MM-DD_sweep.md`, written only by `sweep`. Each run appends one section
and never edits an earlier one. A run that finds nothing new writes nothing here, only its line
in `Tracking/Signals/RUN_LEDGER.md`.

## Why it catches up

Each run starts where the last good run ended, read from the run ledger. If the laptop was
closed overnight, the first run of the morning covers the whole night (up to 96 hours, which covers a long weekend; anything
older is recorded as a gap and the briefing names it). Nothing that stayed in the source is lost
by checking late.

## Item kinds

| Kind | Means | Who acts on it |
|---|---|---|
| `urgent` | matches "what urgent means" in `Context/me.md` | the next briefing or midday update puts it first |
| `reply-owed` | someone is waiting on {{preferred_name}} | the briefing's **Replies owed** |
| `prep-needed` | a meeting soon needs something prepared | the briefing's **Today** |
| `commitment-candidate` | a promise made, either way | the briefing; the dream files it if a capture or the recap confirms it |
| `fyi` | worth knowing, nothing to do | the briefing, only if `Context/surfacing.md` says to show it |

## Entry shape

```markdown
## 10:20 (window 09:20–10:20)
- q-20261123-004 | reply-owed | [[Pat Lee]] | asks for the Q4 draft by Friday | evidence: "can you get me the Q4 draft by Friday" (email 09:12) | source-id: <message or thread id>
```

Nothing personal or HR-related goes here, no secrets, and never transcript text.
