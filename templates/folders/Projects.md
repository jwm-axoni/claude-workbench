---
type: system
updated: {{created_date}}
---

# Projects

One page (or folder) per project. A project earns a page when it has its own thread of
decisions, not just a task.

- Simple project: a single `<Project Name>.md`
- Project with artifacts: a folder holding the main page plus specs and notes

`INDEX.md` lists active projects with status and a one-line "what's next" each. Point inbound
links there. Top level holds projects with activity in the last 30 days; the rest move to
`Archive/Projects/` and are listed under `## Archived` in `INDEX.md`.

## Frontmatter

```yaml
---
type: project
tags: [project, <domain>]
status: active | paused | shipped | archived
owner: <who drives it>
repo: <local folder holding the code, optional>
artifacts: <local folder holding decks/docs, optional>
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD
---
```

`repo:` and `artifacts:` point at where the work itself lives, as a `~/` path. The page is the
record; the folder is the workshop. Never copy code, media or transcripts into the vault.

## Who writes what

- `nightly-dream` owns `## Open commitments (mine)`, `## Decisions` and `## Current state (dream)`
  on project pages, plus the status cells and rows of `INDEX.md`. Nothing else on them.
- `weekly-review` fixes frontmatter and links, repairs index rows the dream missed, and moves
  quiet `shipped` projects to `Archive/Projects/`.
- {{preferred_name}} edits everything freely. Their edits to the commitments ledger are the label
  the dream is scored against.

## Page shape

```markdown
---
type: project
tags: [project, <domain>]
status: active
owner: {{name}}
updated: YYYY-MM-DD
---

# <Project Name>

One or two sentences: what this is and why it exists.

## <Whatever sections the project needs>

Freeform: status, a dated log, specs.

## Current state (dream)
_Maintained nightly by nightly-dream._

## Open commitments (mine)

What {{preferred_name}} owes, to whom, by when. If nothing, say "No open commitments recorded"
rather than dropping the heading; the commitment sweep reads it.

- [ ] Send the draft — owed to [[Name]], due YYYY-MM-DD
      `source: <file>` `since: YYYY-MM-DD` `state: live`

## Decisions

What was decided, by whom, when. Same fields and states as commitments, so a reversed decision
demotes instead of disappearing.

## Related
### People
- [[Name]]
### Organizations
### Tools
```

Include only the `### Related` subheadings that have entries.
