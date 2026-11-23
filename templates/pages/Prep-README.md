---
type: reference
tags: [tracking, prep]
status: active
updated: {{created_date}}
---

# Prep

One page per meeting or job the team prepared ahead of time, as `YYYY-MM-DD_<slug>.md` (the
meeting's date). Written only by the `team` routine's prep persona and role workers; final once
that run ends. The briefing links today's pages under **Today**.

## Page shape

```markdown
---
type: prep
date: YYYY-MM-DD
meeting: "Acme renewal call 15:00"
by: team-prep
queue: q-20261123-005
---

# Prep — Acme renewal call, 15:00

## Who
- [[Pat Lee]] — their side's decision maker; last spoke 11-14 about pricing

## Where it stands
- Two lines, each with `source:` or a `[[Page]]` reference.

## Open both ways
- Owed by {{preferred_name}}: …
- Owed to {{preferred_name}}: …

## Bring
- The one or two things to have ready.
```

Nothing personal or HR-related, no secrets, never transcript text.
