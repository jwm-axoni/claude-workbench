---
type: system
updated: {{created_date}}
---

# Resources

Durable reference material: knowledge that outlives any one project.

- `Tools/` — one page per tool or platform {{preferred_name}} uses: what it is, how it's used
  here, whether Claude can reach it, who owns it, which projects touch it.
- `GLOSSARY.md` — terms, acronyms, internal names.

## What does not belong

- Anything tied to one project goes in `Projects/`. Anything dated goes in `Daily/`.

## Frontmatter

Tool pages:

```yaml
---
type: tool
category: data | security | gtm | ai | productivity | devtools | hr | finance | comms
tags: [tool, <category>]
status: active
connected: yes | no | manual   # can Claude reach it from this workbench?
updated: YYYY-MM-DD
---
```

Other reference pages: `type: reference`, `tags`, `updated`.

## Glossary states

| State | Means |
|---|---|
| `confirmed` | {{preferred_name}} or a source defined it |
| `unconfirmed` | inferred from use, still a guess |
| `asked` | it's a numbered question in a briefing, waiting on an answer |

An `unconfirmed` term heard three or more times becomes a briefing question. `nightly-dream`
appends under `## Needs confirmation`; {{preferred_name}} answers by editing the entry.

## Who writes what

`nightly-dream` creates new tool pages and writes `## Current state (dream)` blocks and glossary
entries. `weekly-review` fixes frontmatter and links. Everything else is {{preferred_name}}'s.

## Tool page shape

```markdown
---
type: tool
category: productivity
tags: [tool, productivity]
status: active
connected: yes
updated: YYYY-MM-DD
---

# <Tool>

What it is and what {{preferred_name}} uses it for.

## How Claude reaches it
Connector name, or "not connected — export/paste manually".

## Current state (dream)
_Maintained nightly by nightly-dream._

## Vendor relationship
_Only if the vendor is a live relationship._

## Related
### Projects
### People
```
