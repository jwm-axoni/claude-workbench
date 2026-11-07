---
type: system
updated: {{created_date}}
---

# Context

How {{preferred_name}} works and how the organization around them works: stakeholder
briefings, team structure, operating agreements. An agent reads this folder to understand
the terrain before doing anything else. It answers "who decides this" and "how does this
team operate", not "what happened today".

## Files that always exist

- `me.md` — role, rhythm, what urgent means, which tools are reachable. Read first, always.
- `voice.md` — how {{preferred_name}} writes, and how to write back to them.
- `surfacing.md` — what the briefing always raises, never raises, when it stays quiet, and the
  shape {{preferred_name}} wants for each topic.

## Frontmatter

```yaml
---
type: context
tags: [context, <topic>]
status: active
updated: YYYY-MM-DD
---
```

## What belongs here

- Stakeholder briefings: a named person's org, priorities, and how they work
- Team and org structure (e.g. `ORG_CHART.md`)
- Operating protocols and working agreements

## What does not

- A person's own page goes in `People/`. A briefing about their **organization** goes here.
- Anything dated goes in `Daily/`.

## Who writes what

{{preferred_name}} edits these pages freely. `nightly-dream` writes only the
`## Current state (dream)` block on `me.md` and on org-structure pages, and the
`## Learned rules (dream)` block on `voice.md`. On `surfacing.md`, `nightly-dream` appends learned
rules; {{preferred_name}} edits it directly. Nothing else here is routine-written.

## Page shape

```markdown
---
type: context
tags: [context, stakeholder]
status: active
updated: YYYY-MM-DD
---

# <Team or stakeholder> — how they operate

What this org is, who leads it ([[Name]]), and what they care about.

## How decisions get made
## What they need from {{preferred_name}}
## Current state (dream)
_Maintained nightly by nightly-dream._

## Related
### People
### Projects
```
