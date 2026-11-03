---
name: capture
description: Write back from a chat into the workbench the only way a chat is allowed to - one line appended to Tracking/Captures/YYYY-MM-DD.md per decision, process change, fact, correction or briefing answer settled in the conversation, plus a copy of every draft handed over to send, saved to Tracking/Drafts/ so the recap can compare it with what was actually sent. The nightly dream files these into the right pages. Use whenever a chat in the workbench project settles something worth remembering, when the user corrects Claude or says "always"/"never", or says "remember this", "capture that", "log this decision", or /workbench:capture.
---

# Capture

Chats are invisible to the routines. Captures are how what's settled in a chat reaches the vault:
you append one line per item; the nightly dream files it into the right page and the weekly flags
anything left unfiled.

**You write two places: `Tracking/Captures/<today>.md` and `Tracking/Drafts/`** (today in the owner's timezone, from
`Context/me.md`). Append only. Never edit or delete an earlier line, never write any other vault
file from a chat. Everything else has an owner, and a second writer causes conflicts.

## When to capture

Without being asked, at the moment it happens:
- a **decision** gets made ("let's go with vendor B", "we're pushing launch to March")
- a **process** changes ("from now on, QBR decks go through Dana first")
- a **fact** comes up that the next session should know (a new owner, a date, a number, a name)
- the owner **corrects** you, or says "always" or "never". Capture before continuing.
- the owner **answers** a numbered question from a briefing ("3 yes, 5 it's Dana"). One `answer:` line per answer.

Don't capture chit-chat, drafts, half-formed ideas, or anything already in the vault and unchanged.
If the owner says "don't save this" or the topic is personal, don't.

## Line format

```
- decision: <what was decided, and why if stated> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- process: <what changed in how something is done> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- fact: <the fact, with who said it if relevant> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
- correction: <what was wrong> → <the rule going forward> `source: project-chat` `date: YYYY-MM-DD`
- answer: briefing YYYY-MM-DD Q<n> — <the answer> — about [[Page]] `source: project-chat` `date: YYYY-MM-DD`
```

Write every line in your own words as a summary of what was settled. Never paste text from an
email, document, message or web page into a capture. Something discussed but not decided is not a
capture.

- One item per line, in plain words a stranger could act on. Name people in full, as `[[wikilinks]]`
  when they have a page, and name every org, project and tool involved the same way. The dream
  builds relationship edges from these names, so "Pat said Acme wants it" is weaker than
  "[[Pat Lee]] said [[Acme Data]] wants the pilot moved — about [[Acme Expansion]]".
- When a chat establishes a relationship ("Sam's taking over the Acme account", "Dana reports to
  Lee now"), capture it as a `fact:` so the edge gets built.
- `about [[Page]]` names the page it belongs on: a project, person, org, tool, or `Context/me` /
  `Context/voice` for how the owner works or writes. Use the page's exact name; check it exists. If
  there's no page yet, use the plain name without brackets; the dream decides whether to create one.
- If a line supersedes an earlier capture, say so: `(supersedes 10:40 line about launch date)`.

If the file doesn't exist yet, create it with this frontmatter first:

```yaml
---
type: reference
tags: [tracking, captures]
date: YYYY-MM-DD
---
```

Then tell the owner in a few words what you captured ("Captured: decision to push launch to March").
No ceremony.

## Drafts

Separately from captures: whenever you hand the owner a draft they'll send to someone else (email,
Slack message, post, doc section), save it exactly as given to
`Tracking/Drafts/YYYY-MM-DD_<short-slug>.md`:

```markdown
---
type: draft
date: YYYY-MM-DD
channel: email | slack | doc | post | other
to: "[[Name]]"
about: "[[Page]]"
---

<the draft exactly as given>
```

If you revise it in the same chat, save the final version under the same name (it's the one they'll
send). Don't announce it. The recap compares it with what was actually sent, and the dream learns
the owner's voice from the differences. Never save personal or HR drafts.

## Secrets and sensitive data

Never capture passwords, keys, tokens, account numbers, or anything the role guardrails in the root
`CLAUDE.md` exclude (e.g. candidate or employee personal data). Capture that the thing exists and
where it lives, not its value.
