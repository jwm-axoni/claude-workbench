---
type: system
updated: {{created_date}}
workbench_version: {{version}}
---

# {{preferred_name}}'s Workbench

Personal knowledge vault for {{name}}, {{role}} at {{company}}{{team_suffix}}.

This vault is the **record**: who people are, which organizations matter, what projects
are running, and what happened. It is not a scratchpad and not a task runner. It is also
the memory for {{preferred_name}}'s AI agents: every scheduled routine reads this vault,
and the routines keep it current so {{preferred_name}} doesn't have to.

## Where things go

| Folder | Holds | Write here when |
|---|---|---|
| `Context/` | How {{preferred_name}} works, and how the org around them works | You learn how a team, stakeholder or process actually operates |
| `Daily/` | Dated briefings, recaps, calendar copies, weekly plans | A routine generates a file for a date |
| `Projects/` | Active and recent work, `INDEX.md` | A piece of work has its own thread of decisions |
| `People/` | One page per person | Someone recurs enough to be worth tracking |
| `Organizations/` | Live relationships: employer, customers, vendors, partners | An org generates ongoing decisions |
| `Resources/` | Durable reference, `Tools/` nested, `GLOSSARY.md` | Knowledge that outlives one project |
| `Tracking/` | Goals, friction, the dream log; `Captures/` and `Signals/` nested | Something is tracked over time |{{meetings_row}}
| `Archive/` | Closed chapters, read-only | Only the weekly moves things here |

Each folder has its own `CLAUDE.md` with the schema and a copyable page shape for pages
in it. Read it before writing into a folder. That file is the only place its schema lives:
there's no templates folder, because a second copy of a schema is one more place to drift.

## Read these first

For any routine or any question about {{preferred_name}}'s work, in this order:

1. **`Context/me.md`** — role, rhythm, what counts as urgent, which tools are reachable.
2. **`People/NAME_VARIANTS.md`** — before using any name from a transcript or a quick note.
   Rendering a misspelling as a separate person is the most common way a briefing goes wrong.
3. **`Tracking/GOALS.md`** — the objectives that count and the hard dates.
4. **`Resources/GLOSSARY.md`** — before flagging a term as unfamiliar.
5. **`Context/voice.md`** — before drafting anything in {{preferred_name}}'s voice.

A page with a `## Needs reconciling` section has a known unresolved conflict, usually two
figures for the same thing. **Report both, never pick one.**

## Who writes what

Six routines write here on a schedule, each as a `[Workbench] …` scheduled task. **One
writer per file** is the rule most worth respecting: two writers racing one file produce
conflicts, and if the vault syncs through git a conflict can silently halt the sync.

{{routine_table}}

**The Claude project → `Tracking/Captures/YYYY-MM-DD.md` and `Tracking/Drafts/`, and nothing
else.** Chats in the project are invisible to the routines, so each time a chat settles a
decision, a process change, a fact, a correction, or an answer to a briefing question, the
project appends one line to today's capture file. Every draft it hands {{preferred_name}} to send
to someone else is saved, as given, in `Tracking/Drafts/`. The dream files captures into the right
pages nightly; the recap compares drafts with what was actually sent.

**How {{preferred_name}} gets the day:** {{delivery_label}}. The briefing writes the full file and
sends a short digest (focus, risks, numbered questions) by that channel. Replies to it, or answers
given in the project, come back as captures or through the recap, and the dream acts on them.

**The recap is the one account of the day.** Every source reaches the vault through it.
The dream and the weekly build on that account instead of going back to the sources, which
is what stops two routines describing the same day differently. The briefing still
collects, because a midday pass catches what a next-morning read would report late.

**Escape hatch.** The dream may go back to a source for one entity when a recap line is
genuinely ambiguous, capped at five lookups a night, each logged in `Tracking/Signals/`.
Anything past that becomes a question in the next briefing.

What no routine may write, whatever it concludes: any `CLAUDE.md`, another routine's
`Daily/` file, or anything inside `Archive/`. No routine deletes anything. Only the weekly
moves files, and only into `Archive/`.

### Standing exceptions

When you decide a routine may do something this file forbids, write the exception here,
dated, with the reason, rather than quietly editing the rule. A later reader can then tell a
decision was made. Revoking one means deleting its entry here and in the routine on the same day.

**{{created_date}} — the briefing may send its digest to {{preferred_name}}.** Routines never send
anything, except that `daily-briefing` may deliver its digest to the owner alone, by the channel in
`.workbench/profile.json` (`delivery`). Never to anyone else, never into a shared channel.
*Reason: not everyone opens the folder every morning; the digest is how the day reaches them.*

## Conventions

### Frontmatter

Every entity page opens with YAML:

```yaml
---
type: person | organization | tool | project | system | context | reference
tags: [lowercase-kebab-case]
status: active | former | archived | current
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD   # set by the weekly when it confirms the page still holds
---
```

`updated:` moves only when content changes. `reviewed:` moves when the weekly confirms the
page against current sources. Routine-only types: `morning-briefing`, `daily-recap`,
`calendar`, `weekly-plan`, plus `draft` (written only by the project). Add a new `type` value here before using it anywhere.

### Links

**Bare wikilinks: `[[Jane Rivera]]`, never `[[People/Jane Rivera]]`.** Bare links survive
moves; path links break the first time a file moves. Link a person, org, project or tool the
first time it appears on a page. Don't link a page that doesn't exist unless you're creating it.

### Relationships

The graph is built from **relationship properties in frontmatter**, not just links in prose. Each
property value is a quoted bare wikilink (`"[[Pat Lee]]"`), so Obsidian draws it in the graph, lists it
in backlinks, and a query (Dataview, Bases) can read it. The `## Related` section in the body mirrors
the properties for humans; when they disagree, the properties win and the weekly fixes the body.

| On a… | Property | Points to | Inverse kept on the other page |
|---|---|---|---|
| person | `org` | organization (or tool page for a same-name vendor) | org `people` |
| person | `reports_to` | person | that person's `direct_reports` |
| person | `projects` | projects | project `people` |
| person | `relationship` | `manager · direct-report · peer · collaborator · exec · customer · partner · vendor · vault-owner` (a value, not a link) | — |
| project | `owner` | person | that person's `projects` |
| project | `people` | people | each person's `projects` |
| project | `orgs` | organizations | each org's `projects` |
| project | `tools` | tools | each tool's `projects` |
| organization | `relationship` | `employer · customer · vendor · partner · prospect` | — |
| organization | `people`, `projects`, `tools` | as named | the inverse on each |
| tool | `owner`, `projects`, `vendor` | person, projects, org | the inverse on each |

Rules:

1. **Every edge is two-way.** Whoever adds `people: ["[[Pat Lee]]"]` to a project also adds that project
   to Pat's `projects` in the same change. A one-sided edge is a bug the librarian reports.
2. **Only link pages that exist.** A name with no page stays plain text in the body until the dream
   creates the page (two sources in 30 days), then the edge is added on both sides.
3. **Edges carry evidence when they could be wrong.** Put the source in the body's `## Related` line:
   `- [[Pat Lee]] — owner, since 2026-10-02 (`source: 2026-10-02_DAILY_RECAP`)`.
4. **Ended relationships are demoted, not deleted.** Move the link from the live property to
   `former_people` / `former_orgs` / `former_projects`, and note the end date in `## Related`.
5. Lists are YAML lists: `projects: ["[[Acme Expansion]]", "[[Q4 Forecast]]"]`.

### Tags

Lowercase kebab-case. Function tags describe what something does; relationship tags describe
how it relates to {{preferred_name}}. The vocabulary lives in `People/CLAUDE.md`. If nothing
fits, **add a tag to the vocabulary rather than forcing a bad fit**.

### Freshness

Every ledger entry (a commitment, a decision, a role claim, a glossary term) carries a
source, a date, and one of three states:

| State | Means | Where it sits |
|---|---|---|
| `live` | current, nothing contradicts it | top of its section |
| `superseded` | a newer source contradicts it | below `live`, with a forward link to what replaced it |
| `archived` | superseded and unreferenced for 30 days | moved to `Archive/`, links intact |

```markdown
- [ ] Send the Q4 draft — owed to [[Pat Lee]], due 2026-09-25
      `source: 2026-09-18_DAILY_RECAP` `since: 2026-09-18` `state: live`
```

Position on a page is set by state, not by when it was written. A `superseded` entry without
a forward link is a bug. **Nothing is deleted:** superseded is a demotion, archived is a move.

### Honesty

Never infer a fact you weren't given: no guessed job titles, no guessed dates, no invented
numbers. An empty field is honest; a wrong one gets repeated back as truth. If a source is
missing, say there's no record rather than that nothing happened.

### Keeping `updated:` honest

Any routine that writes to a page bumps that page's `updated:` in the same change.

## Rules that never bend

1. No secrets in the vault: no passwords, API keys, tokens, or `.env` contents.
2. This vault holds real names and internal detail. None of it goes anywhere shared or public
   without {{preferred_name}} checking first.
3. Write, send or change things in other tools (email, chat, CRM, tickets) only when
   {{preferred_name}} asks in that session. Routines read; they don't act. The one standing
   exception is the briefing digest to the owner, below.
{{guardrails_rules}}

## Archive policy

`Archive/` is read-only history. Move something there when it stops being referenced, not
when it stops being true. Search it only when the active vault comes up empty or the
question is explicitly historical.

## How the workbench learns

Three feedback loops, all measured rather than assumed:

1. **Corrections.** Every `correction:` capture becomes a rule (voice, how-they-work, or a friction
   fix). The weekly checks whether the same correction comes back after the rule exists.
2. **Outcomes.** The recap grades the briefing's claims (kept, edited, wrong) and every saved draft
   (sent verbatim, lightly edited, rewritten, not sent). The dream turns the edits into voice rules;
   the weekly reports the trend and tunes the confidence bar on evidence.
3. **Proposals.** When the dream sees repeated manual work or friction, it proposes a fix: a rule, a
   skill, a routine change, a connector. The weekly logs each in `Tracking/IMPROVEMENTS.md` and
   checks later whether it was adopted and whether it worked.

## Maintaining this system

The workbench was built by the **Claude Workbench** plugin (v{{version}}). The plugin keeps
its own bookkeeping in `.workbench/`. To change your role, tools, hours or routines, run
`/workbench:setup` again. To upgrade after the plugin updates, run `/workbench:migrate`:
it never overwrites a file you've edited, it writes a `.workbench-new` copy beside it.
