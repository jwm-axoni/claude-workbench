---
type: system
updated: {{created_date}}
---

# People

One page per person, named `First Last.md`. This is the spine of the graph: almost every
other page links back to someone here. People seen once go in `OTHERS_SEEN.md` until they
recur in a second source.

## Frontmatter

```yaml
---
type: person
tags: [person, <function>, <relationship>]
org: <company>
role: <title>              # omit entirely if unknown, never guess
role_confirmed: YYYY-MM-DD # when a source last stated it
role_source: <file>
status: active | former
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD
---
```

**Never infer a role from a name, an email domain, or a vibe.** If no source says what someone
does, leave `role:` out. When a newer source gives a different title, the old one goes in the
body as a `superseded` line with a forward link. Who someone used to report to is often exactly
what a briefing needs.

## Tag vocabulary

Function: {{function_tags}}

Relationship to {{preferred_name}}: `manager`, `direct-report`, `peer`, `collaborator`, `exec`,
`customer`, `partner`, `vendor`, `vault-owner`

If a person's function has no tag here, add one to this list rather than forcing a bad fit.

## Who writes what

`nightly-dream` creates stubs for anyone named in two sources within 30 days, rewrites
`## Recent (dream)`, and updates `role:`/`status:` when a source states a change. It adds rows
to `NAME_VARIANTS.md` when it sees a misspelling. `weekly-review` fixes frontmatter and links.

## Page shape

```markdown
---
type: person
tags: [person, <function>, <relationship>]
org: <company>
status: active
updated: YYYY-MM-DD
---

# First Last

One line on who they are and why they matter to {{preferred_name}}'s work.

## What matters right now

## Recent (dream)
_Maintained nightly by nightly-dream._

## Related
### Organizations
### Projects
### People
```

Bare wikilinks only: `[[First Last]]`.
