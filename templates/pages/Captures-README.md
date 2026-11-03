---
type: reference
tags: [tracking, captures]
status: active
updated: {{created_date}}
---

# Captures

One file per day, `YYYY-MM-DD.md`, written **only** by {{preferred_name}}'s Claude project. Each
line is a summary, in that chat's own words, of something settled in the chat:

```
- decision: <what was decided and why> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- process: <what changed in how something is done> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- fact: <something worth knowing next time> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- correction: <what Claude got wrong and the rule going forward> `source: project-chat` `date: YYYY-MM-DD`
```

`nightly-dream` files each line into the page it belongs on and records what it filed under
`## Processed captures` in `Tracking/DREAM_LOG.md`. `correction:` lines feed `Context/voice.md`,
`Context/me.md` or `FRICTION_LOG.md`. `weekly-review` flags lines unfiled for more than two
workdays. Lines are appended, never edited; a later line that contradicts an earlier one supersedes it.
