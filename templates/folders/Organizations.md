---
type: system
updated: {{created_date}}
---

# Organizations

Organizations that are a **live relationship** right now: {{preferred_name}}'s employer,
customers, vendors, partners. A company mentioned once doesn't need a page.

## Same-name vendors live in `Resources/Tools/`

When a company's product already has a tool page with the same name (Salesforce, Slack,
GitHub…), that tool page is the one page for it, and the vendor relationship goes in its
`## Vendor relationship` section. Two files with one name make every bare `[[Name]]` link
ambiguous. Check `Resources/Tools/` before creating a page here.

## Frontmatter

```yaml
---
type: organization
relationship: employer | customer | vendor | partner | prospect
people: ["[[Person]]"]
projects: ["[[Project]]"]
tools: ["[[Tool]]"]
status: current | former | archived
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD
---
```

## Who writes what

- `nightly-dream` creates a page for a company named in today's sources and at least one other
  source in the last 30 days, rewrites `## Recent (dream)`, and sets `status: former` when a
  source says the relationship ended.
- `weekly-review` moves `former` orgs quiet for 45 days to `Archive/Organizations/` and sets
  `status: archived`.

## Page shape

```markdown
---
type: organization
relationship: customer
people: []
projects: []
tools: []
tags: [organization, customer]
status: current
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD
---

# <Organization Name>

One or two sentences: what this org is and why it's a live relationship.

## Recent (dream)
_Maintained nightly by nightly-dream._

## Related
### People
### Projects
### Tools
```
