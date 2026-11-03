---
type: reference
tags: [tracking, drafts]
status: active
updated: {{created_date}}
---

# Drafts

Every draft Claude hands {{preferred_name}} that's meant to go to someone else (an email, a Slack
message, a doc section, a post) is saved here at the moment it's given, as
`YYYY-MM-DD_<short-slug>.md`. One writer: the Claude project (and the briefing, if it drafts
replies). The chat that wrote a draft may overwrite it with its final revision; after that chat,
it's never edited.

This is how the workbench learns from what {{preferred_name}} actually sends, not just from what
they say. The end-of-day recap compares each draft with what really went out and grades it in
`Tracking/Signals/YYYY-MM-DD_recap.md`:

| Grade | Means |
|---|---|
| `verbatim` | sent as written, or with typo-level changes |
| `light-edit` | same message, some wording changed |
| `heavy-edit` | rewritten: structure, tone or substance changed |
| `not-sent` | nothing matching it went out within two workdays |
| `unknown` | the channel isn't reachable, so there's no way to tell |

The nightly dream reads `light-edit` and `heavy-edit` grades, works out what changed (tone, length,
openers, sign-offs, word choice) and writes the pattern into `Context/voice.md` under
`## Learned rules (dream)`. The weekly reports the acceptance rate over time. A rising `verbatim`
share means the voice rules are working.

## File shape

```markdown
---
type: draft
date: YYYY-MM-DD
channel: email | slack | doc | post | other
to: "[[Pat Lee]]"
about: "[[Acme Expansion]]"
---

<the draft exactly as given>
```

Nothing personal or HR-related is saved here, and no secrets.
