---
name: setup
description: Onboard someone into their personal Claude Workbench. Interviews them (role, company, location and timezone, hours, tools, goals, how they like answers), checks which tools Claude can actually reach, works out whether the folder is new, already a workbench, or an existing notes vault, builds the folder structure and every CLAUDE.md, hands off to schedule the routines, and writes the instructions for their one Claude project. Use for "set up my workbench", "onboard me", "build my second brain", /workbench:setup, and later whenever their role, tools, hours or goals change.
---

# Workbench setup

You're building this person's workbench: one folder of markdown that becomes their long-term
memory and the memory for their AI routines. Keep it to about ten minutes of their time. Be
quick and plain. Don't explain the architecture up front; show them the result at the end.

The folder structure is built by a script, so every workbench comes out the same and re-runs
are safe:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workbench.py" <detect|plan|apply|schedules|status|pin> --root "<folder>" [--profile "<file>"]
```

If `${CLAUDE_PLUGIN_ROOT}` isn't set, find the installed plugin folder that contains
`scripts/workbench.py`. If you can't run commands at all, use **No-shell fallback** at the end.

## 1. Find the folder and look before touching it

Ask where the workbench should live. Suggest `~/Workbench` unless they already keep notes
somewhere (an Obsidian vault, a Notes folder). In Cowork, the folder they shared with you is
usually the answer. Then run `detect --root "<folder>"`:

| `state` | Meaning | What to do |
|---|---|---|
| `fresh` | empty or missing | Full setup. |
| `workbench` | already set up (`.workbench/manifest.json` exists) | **Re-run.** Load `.workbench/profile.json`, show a short summary of what's on file, ask only what changed, then continue from step 4. If `upgrade_available` is true, run the `migrate` skill afterwards. |
| `foreign` | existing notes, no workbench | **Adopt mode.** Nothing is moved or overwritten. Show `adopt_suggestions` (e.g. `Journal/ → Daily/`) and ask whether to move those folders after setup. Never move anything without a yes. If `has_claude_md` is true, their CLAUDE.md stays put and the workbench's lands beside it as `CLAUDE.md.workbench-new`, merged in step 6. |

Also check for older routines: if a `[Workbench] …` scheduled task already exists, or the folder
has its own scheduled-task prompts, mention that the `schedules` skill will reconcile them in step 7.

## 2. Interview

Ask in three short rounds, not one long form. Use a multiple-choice tool if you have one. Infer
what you can and confirm it instead of asking cold: the timezone from the system clock, the name
from the account, the company from an email domain.

**Round 1: who you are**
- Full name, and what to call you
- Role or title, team, and who you report to
- Company, one line on what it does, and the industry
- Where you're based. Convert it to an IANA timezone like `America/Chicago`; the routines run on it.

**Round 2: how you work**
- Working hours and days (default 09:00–17:30, Mon–Fri)
- The tools you use every day: email, calendar, chat, CRM, docs, tickets, project tool, meeting recorder
- One to three things you're trying to get done this quarter
- What counts as urgent for you
- How you like answers: length, tone, format, pet peeves
- Any calendar blocks that should never show up in a briefing (personal, focus time)
- Do you record meetings? If yes, with which tool? (How the notes reach the workbench is settled
  in step 3, connector first.)

**Round 2b: which Claude, and where the vault lives.** Ask this before the routines, because it
decides where they run.

- **Which Claude do you have?** Claude Code (the desktop app's Code tab or the CLI), or Cowork
  only. Infer it from this session where you can (a Code session means they have Code) and confirm.
  Record it as `surface`: `code` or `cowork`.
- **Where should the vault live?** A local folder, or a private GitHub repo with a local clone as
  the working folder (Obsidian and the desktop app open the clone, so day to day it feels the same).
  Recommend the **repo** for anyone rolling the workbench out to a team or using more than one
  computer: it adds backup, version history, safe multi-device use, and the only route for routines
  that run with the laptop closed. A **local folder** is fine for one person on one machine.
  Record it as `vault_home`: `local` or `repo`, and the repo as `repo` (`owner/name`).

Then derive the runner from those two answers with this table (the same table the `schedules`
skill uses). Don't ask them to pick a runner; tell them which one they get and what it guarantees,
in one line:

| You have | The vault lives in | Routines run on | What's guaranteed |
|---|---|---|---|
| Cowork only | a local folder | Cowork local | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. |
| Cowork only | a private GitHub repo, worked from a local clone | Cowork local, on the clone | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. The repo adds backup, history and safe use from more than one computer. |
| Claude Code | a local folder | Code Desktop local | Runs while the desktop app is open. Exactly one catch-up run for the most recent missed run within 7 days. |
| Claude Code | a private GitHub repo, worked from a local clone | Code cloud | Runs with the laptop closed. Research preview: fresh clone per run, pushes to `claude/` branches, minimum interval one hour. No documented catch-up: the run ledger and gap detection cover misses. |

On Team and Enterprise plans, Cowork sessions run in the cloud only if the organization turns on
"Run Cowork in the cloud" (Organization settings > Cowork), and even then a task that needs local
files runs locally. Mention it only if they ask why their routines need the laptop.

**Round 3: routines** (show the defaults with times in their timezone, let them switch any off)

| Routine | Default | Why |
|---|---|---|
| Calendar Sync | before work, 11:30, end of day (only if a calendar is connected) | keeps a record of moves and cancellations |
| Morning Briefing | 30 min before work | what today needs |
| Midday Update | 12:00 | appends what changed since the morning |
| End-of-Day Recap | 30 min after work | the one account of the day; everything else builds on it |
| Nightly Dream | 22:00 on workdays | files the day into people, projects, orgs; learns from corrections |
| Weekly Plan & Maintenance | 90 min before work on the first workday | next week's plan plus the librarian's checks and fixes |

**Round 4: how the day reaches you.** Most people won't open the folder every morning, so ask how
they want the briefing delivered:

| Option | What they get | Needs |
|---|---|---|
| **Slack** | a DM to themselves (or a private channel they name) with today's focus, risks and numbered questions; they reply in the thread | a Slack connector that can post |
| **Email** | the same digest in their inbox; they reply to it | an email connector that can send (if it can only draft, say so and offer another option) |
| **Claude** | the digest is the scheduled task's own message, in the Claude app; they answer in the project | nothing extra |
| **None** | just the file in `Daily/` | nothing extra |

Also ask whether the midday update should message them too (default: only if something changed),
and whether they want **Obsidian** (free, obsidian.md) to browse the workbench: it shows the folders,
links and a graph of people and projects, which is far easier than a file browser. Default yes; the
workbench ships a starter Obsidian config.

Pick the role pack by matching their role against `blueprints/roles.json` (`sales`,
`customer-success`, `marketing`, `engineering`, `product`, `operations`, `people`, `it-security`,
`finance`, `leadership`, `general`). Tell them which you picked and let them override it. The pack
shapes the tag vocabulary, which sources the recap sweeps first, and what the briefing and weekly
watch for.

## 3. Check what Claude can actually reach

For each tool they named:

1. Look at the tools available in this session (MCP servers and connectors). Map each named tool to
   one: Gmail → a Gmail or Google Workspace connector, Salesforce → a Salesforce/CRM connector, etc.
2. If one exists, make one cheap **read-only** call to prove it works (list one calendar event,
   search one email). Works → `connected`. Exists but fails auth → `available`.
3. Nothing matches → `missing`. No connector exists anywhere for it (an internal system) → `manual`.
4. If you can suggest connectors to install, do that for the missing ones.

### Meetings: connector first

If they record meetings, settle how the notes reach the workbench, in this order. There's no
sync script and never will be; every recorder is different, so the workbench only reads.

1. **A connector for the recorder works** (it passed the read-only call above): use it. Set
   `meetings_source` to the tool and `meetings_via` to `connector`. No `Meetings/` folder is made.
   The recap reads each day's meeting summaries, decisions and next steps through the connector,
   never the transcripts. This is the default and the right answer for most people.
2. **No connector, but the tool can export notes to a folder**: show them how to point that
   export at `<workbench>/Meetings/` (from the tool's own settings; you don't know every tool, so
   say what to look for rather than inventing menu names). Set `meetings_via` to `export`. That
   turns on `Meetings/`, which the tool writes and the workbench only reads.
3. **Neither**: if a connector exists for the tool but isn't installed, suggest it. Otherwise
   skip meetings (`meetings_source: ""`). Say plainly that the recap still sees meetings through
   the calendar, email and chat; it just won't have the recorder's notes.

Only if they ask to keep **full transcripts** in the vault (they need exact quotes long-term)
does an export make sense when a connector also works. Say the cost once before they choose:
transcripts hold other people's exact words, some employers don't allow keeping them outside the
recording tool, recording-consent rules vary by place, and in a repo vault they'd sit in git
history. Then let them decide.

Never send, post or change anything in another tool during setup. Tell them plainly what's missing
and where to fix it: **Settings → Connectors** in the Claude apps, or `claude mcp add` in Claude
Code. Missing tools don't block setup; every routine skips what it can't reach and says so.

## 4. Write the profile and preview

Write the profile as JSON to a scratch file:

```json
{
  "name": "Jane Rivera",
  "preferred_name": "Jane",
  "role": "Senior Account Executive",
  "role_pack": "sales",
  "team": "Mid-Market East",
  "manager": "Pat Lee",
  "company": "Acme Data",
  "company_description": "B2B data platform for mid-market retailers.",
  "industry": "SaaS",
  "location": "Austin, TX",
  "timezone": "America/Chicago",
  "work_hours": { "start": "08:30", "end": "17:30", "days": "Mon-Fri" },
  "tools": ["Gmail", "Google Calendar", "Slack", "Salesforce", "Gong"],
  "connections": [
    { "tool": "Gmail", "status": "connected", "via": "Gmail connector" },
    { "tool": "Salesforce", "status": "missing" }
  ],
  "meetings_source": "",
  "meetings_via": "",
  "goals": ["Hit 120% of Q4 quota"],
  "urgent_means": ["A customer escalation", "Anything from my manager marked today"],
  "private_blocks": ["School pickup 15:00"],
  "communication_style": "Short and direct. Bullets over paragraphs.",
  "work_style": [],
  "guardrails": [],
  "extra_tags": [],
  "delivery": { "channel": "slack", "target": "DM to myself", "midday": "if-changed" },
  "surface": "code",
  "vault_home": "repo",
  "repo": "jrivera/workbench",
  "obsidian": true,
  "routines": { "calendar-sync": true, "daily-briefing": true, "midday-update": true,
                "eod-recap": true, "nightly-dream": true, "weekly": true },
  "routine_times": {}
}
```

`routine_times` overrides a default time, e.g. `{"nightly-dream": "23:00"}`.

Run `plan --root "<folder>" --profile "<file>"`. Show a short preview: the top-level tree, how many
files will be created, any conflicts, and the routine list with times. Get a yes.

## 5. Build it

**Repo vaults, before `apply`:** create the repository as **private** (with the GitHub tools or
`gh repo create --private`), clone it, and use the clone as the folder. Verify privacy before the
first push (`gh repo view --json visibility` must say `PRIVATE`); if you can't verify it, stop and
ask them to check on GitHub. Never push a workbench to a public repo, even briefly. `apply` writes a
`.gitignore` for repo vaults (Obsidian workspace state, OS files, local backups, `.env`). Never
put credentials or `.env` files in the vault. After `apply`, make the first commit with message
`setup: YYYY-MM-DD` and push to the default branch. Never force-push.

Run `apply` with the same arguments. It creates the folders, writes every `CLAUDE.md`, the starter
pages (`Context/me.md`, `voice.md`, `GOALS.md`, the logs, their own person page, their employer's
org page, one page per tool), the routine fallbacks in `.workbench/routines/`, and
`.workbench/manifest.json`, which records file hashes so later upgrades never clobber their edits.

## 6. Settle conflicts (adopt mode and re-runs)

Each `conflict` left a `<file>.workbench-new` beside the original. For each: summarize the
difference in a few lines, then either merge the useful parts of the new version into their file
or replace theirs with it, and delete the `.workbench-new`. If they want to keep their version for
good, run `pin --path "<file>"`. If they agreed to the adopt moves, make them now, one folder at a
time, and note each in `Tracking/FRICTION_LOG.md` under `## Resolved` so there's a record.

## 7. Routines

Hand off to the `schedules` skill. It finds any existing `[Workbench] …` scheduled tasks,
updates or removes them, and creates the current set from `.workbench/schedules.json`. Don't
create scheduled tasks yourself here.

## 7b. Test delivery

Send one test digest through the chosen channel, to the owner only: "Your workbench is set up.
Tomorrow's briefing arrives here at <time>. Reply to it to answer its questions." Confirm they got
it. If it fails, fix the connector or pick another channel now. A briefing nobody receives is the
most common reason a workbench goes quiet. Record the working channel in the profile and re-run
`apply` if it changed.

If they chose Obsidian and don't have it: point them to obsidian.md, then **Open folder as vault**
and pick the workbench folder. Tell them where to look first: `CLAUDE.md`, `Context/me.md`, and
the graph view.

## 8. The one project

Tell them to work from **one** Claude project from now on:

1. Create a project named "<Name>'s Workbench" (Claude desktop or Cowork) with the workbench
   folder attached.
2. Paste everything below the line in `.workbench/PROJECT_INSTRUCTIONS.md` into the project's
   instructions. Show them the text so they can copy it. If they already have a project with its
   own instructions, merge: keep their additions, and make sure the READ / CAPTURE / DRAFTS / WRITE
   sections are present.
   Setup fills in the instructions to match: a repo vault gets the pull-and-merge line, a
   Cowork-only user gets the line on where folder work happens. You don't edit those by hand.
3. Start every piece of work there. The project reads the vault and writes only to
   `Tracking/Captures/`, which the nightly dream files into the right pages. That's the loop that
   makes the workbench learn from their chats.

**Cowork-only users:** say this once, plainly: "Folder work happens in the Claude desktop app.
Claude on the web and on your phone is for reading the digest, answering its questions, and
chatting in the project; it can't reach the folder on your computer."

## 9. Wrap up

A short summary, not a wall:
- where the workbench lives, as a small tree
- connected vs. missing tools, with the single action to fix each missing one
- routines and their times, in their timezone, and the runner with its one-line guarantee
- three things to try today: ask "what do you know about <a colleague>?", have a chat settle a
  decision and watch it land in today's capture file, and correct Claude once on purpose

## Re-running later

Re-running is how anything changes: a new role, new tools, new hours, routines on or off. Load
`.workbench/profile.json`, ask what changed, update it, then `plan` → `apply` → `schedules`.
Content pages are never rewritten; only plugin-managed files that nobody edited get updated.

## No-shell fallback

If you can write files but can't run the script: read `blueprints/base.json` and
`blueprints/roles.json`, render each template in `templates/` by replacing every `{{key}}` with the
profile value, and write the same paths. Skip `manifest.json` and tell them to run
`/workbench:migrate` from Claude Code or Cowork later so upgrades are safe.

If you can't write files at all (plain chat), give them the profile summary, the folder tree, and
the project instructions to paste, and tell them to finish from Cowork or Claude Code with the
folder shared.
