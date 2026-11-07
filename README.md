<div align="center">

<img alt="Claude Workbench: a second brain Claude runs for you, in plain markdown files you own. Hand-drawn loop: morning briefing, evening recap, nightly dream, your pages, every workday." src="docs/assets/workbench-header.png" width="100%">

One plugin interviews you, builds a folder of markdown around your role and tools, schedules the routines that keep it current, and learns from what you correct and what you actually send.

![Plugin: Claude Code and Cowork](https://img.shields.io/badge/plugin-Claude_Code_%26_Cowork-232323)
![Files: plain Markdown](https://img.shields.io/badge/files-plain_Markdown-FF824D)
![Routines: six, scheduled](https://img.shields.io/badge/routines-six_scheduled-232323)
![Learning: measured weekly](https://img.shields.io/badge/learning-measured_weekly-FF824D)
![Role packs: 11](https://img.shields.io/badge/role_packs-11-232323)
![License: MIT](https://img.shields.io/badge/license-MIT-FF824D)

[Quick start](#quick-start) · [Setup](#say-set-me-up) · [The folder](#your-folder) · [The routines](#the-routines) · [How it learns](#how-it-learns) · [Skills](#the-skills) · [Visual explainer](docs/index.html)

</div>

## The problem it solves

Out of the box, Claude is smart and knows nothing about you. Not your team, not your accounts, not what "urgent" means to you, not the words your group uses that appear in no manual. So you re-explain yourself in every chat, and drafts sound like a polite stranger wrote them.

The Workbench gives Claude a memory that lives in plain files you own, six routines that run your day on a schedule, and a nightly pass where Claude reads what happened, learns from it, and updates what it knows. It measures whether it's getting better instead of assuming it is.

It's the public, company-neutral version of a setup that's been running daily since September 2026. Nothing in it names a company, a person or a tool instance. Everything specific to you is gathered during onboarding.

## Quick start

You need Claude Code or Cowork, and Python 3 on the same machine (macOS and most Linux installs already have it). If you want routines that run with the laptop closed, or you use more than one computer, you'll also want a GitHub account for a private repo; setup explains the choice.

**1. Install the plugin.** Type these two lines into Claude:

```
/plugin marketplace add jwm-axoni/claude-workbench
/plugin install workbench@claude-workbench
```

**2. Start onboarding.** Type the command:

```
/workbench:setup
```

Or just say it in plain words. Any of these work:

```
Set up my workbench
```

```
Set me up. I'm a Senior AE at Acme Data in Austin, I work 8:30 to 5:30, and I live in Gmail, Slack and Salesforce.
```

The second one is the fast version: the more you tell it up front, the fewer questions it asks.

**3. Answer its questions (about 10 minutes).** It asks who you are, how you work, which tools you use (and checks each one), whether you record meetings, which Claude you have, whether the folder should be a local folder or a private GitHub repo, and how you want your morning digest: Slack, email, a Claude message, or nothing. From those answers it works out where your routines run and tells you what that guarantees. It shows you a preview before it builds anything.

**4. Make one project your home.** When setup finishes, it shows you your project instructions. Create one Claude project named after you, attach the workbench folder, and paste them in. Start all your work there from now on.

**5. Try it on day one.** Inside that project:

```
What do you know about Pat Lee?
```

```
We decided to push the Acme pilot to January. Remember that.
```

```
Run the librarian.
```

```
Why do you think the Acme pilot starts in January?
```

The first one shows what it already knows. The second gets captured and filed into the right page that night. The third gives you a health check of the folder. The fourth, a day or two in, shows the evidence behind a fact and what it replaced. Your first morning digest arrives the next workday.

**Changed roles, tools or hours later?** Say "redo my setup" or run `/workbench:setup` again. It only asks about what changed.

![What's in the box: ten skills, six of which run themselves on a schedule](docs/assets/workbench-whats-in-the-box.png)

## Say "set me up"

![The setup walkthrough, from checking the folder to making one project your home](docs/assets/workbench-setup.png)

About ten minutes, and you never touch a file by hand. Re-run it whenever your role, tools, hours or delivery preference change; it asks only what changed and never overwrites a file you've edited.

![Role packs decide which sources each routine watches first](docs/assets/workbench-role-packs.png)

Your title picks one of 11 role packs: sales, customer success, marketing, engineering, product, operations, people, IT and security, finance, leadership, or general. The pack sets the tag vocabulary, which sources the recap sweeps first, what the briefing and weekly watch for, and any guardrails, such as keeping candidate and employee data out of the folder entirely.

## Your folder

![The folder layout, with a CLAUDE.md schema in every folder](docs/assets/workbench-folder.png)

Three files keep the memory honest rather than just full:

- `Tracking/COMMITMENTS.md`: every promise in flight, both ways, one row each. The dream adds rows and flags ones that look done or stale; the briefing asks about overdue ones as questions; only the weekly closes a row, on evidence.
- `Context/surfacing.md`: what your briefing should always raise, never raise, when to stay quiet, and the shape you want per topic. Edit it yourself, or just correct a briefing twice and the dream writes the rule.
- `Tracking/Signals/RUN_LEDGER.md`: one line per routine run, so a missed run is visible (see [The routines](#the-routines)).

When two sources disagree, the page gets a `## Needs reconciling` section instead of a guess. The weekly turns the oldest three into numbered questions, and your answer becomes a supersession with the losing claim's history kept. New briefing and recap claims carry an `evidence:` quote or page reference and a `confidence:`, so `/workbench:why` can show you where any fact came from.

Every folder carries its own `CLAUDE.md` with the schema and a page shape to copy, so there is no templates folder to drift out of sync. Each routine owns specific files and writes nothing else; your chats write only to `Tracking/Captures/` and `Tracking/Drafts/`. Nothing is ever deleted: a fact that stops being true is marked superseded with a link to what replaced it, then archived.

![Sources feed one page per project, person and account, and everything reads the page instead of the source](docs/assets/workbench-read-the-page.png)

Pages connect through **relationship properties** in their frontmatter. A person carries `org`, `reports_to` and `projects`; a project carries `owner`, `people`, `orgs` and `tools`; an organization carries `people`. Values are quoted wikilinks, so Obsidian's graph and backlinks use them, and every link is kept on both pages:

```yaml
---
type: project
owner: "[[Jane Rivera]]"
people: ["[[Jane Rivera]]", "[[Sam Ortiz]]"]
orgs: ["[[Acme Data]]"]
tools: ["[[Salesforce]]"]
---
```

## The routines

![The daily chain: the briefing, recap and nightly dream each read what the one before wrote](docs/assets/workbench-daily-chain.png)

Times come from your working hours and timezone, and you can switch any routine off. Where they run follows from two setup answers: which Claude you have, and where the folder lives. You don't pick a runner; setup works it out:

| You have | The vault lives in | Routines run on | What's guaranteed |
|---|---|---|---|
| Cowork only | a local folder | Cowork local | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. |
| Cowork only | a private GitHub repo, worked from a local clone | Cowork local, on the clone | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. The repo adds backup, history and safe use from more than one computer. |
| Claude Code | a local folder | Code Desktop local | Runs while the desktop app is open. Exactly one catch-up run for the most recent missed run within 7 days. |
| Claude Code | a private GitHub repo, worked from a local clone | Code cloud | Runs with the laptop closed. Research preview: fresh clone per run, pushes to `claude/` branches, minimum interval one hour. No documented catch-up: the run ledger and gap detection cover misses. |

On Team and Enterprise plans, Cowork can run sessions in the cloud only if your organization turns on "Run Cowork in the cloud" (Organization settings > Cowork), and a task that needs local files still runs locally. So a folder on your laptop always means routines that need the laptop. For a team rollout, or more than one computer, setup recommends the private repo.

**Missed runs show up instead of vanishing.** Every routine appends one line to `Tracking/Signals/RUN_LEDGER.md` when it finishes. The next morning's briefing checks that ledger before anything else and tells you in plain words what didn't run and what that cost ("the dream didn't run last night, so 4 captures are unfiled"). The dream then files every unfiled capture whatever its date, a recap for a day that never got one is written as a short file marked reconstructed that says what it couldn't sweep, and a routine that runs late says so in its own file. None of that depends on a scheduler promising to catch up.

![The nightly dream: four things it produces, all landing on your pages with a receipt](docs/assets/workbench-nightly-dream.png)

![What a week looks like once it's running](docs/assets/workbench-week.png)

## How it learns

![The digest arrives by Slack, email, Claude, or not at all](docs/assets/workbench-delivery.png)

Most people won't open a folder every morning. Setup asks where your digest should land, sends a test, and reads your replies back in as answers. The digest is the only thing a routine ever sends, and only to you. Routines read your tools; they never post, reply or change anything in them.

![Three learning loops and the weekly scorecard that tracks whether it's working](docs/assets/workbench-learning.png)

- **Corrections** become rules in `Context/voice.md` or `Context/me.md`. If the same correction comes back after the rule exists, the rule is flagged as not working.
- **Briefing feedback** ("stop telling me about X", "always show pipeline numbers first") becomes a rule in `Context/surfacing.md` once you've said it twice.
- **Drafts** are saved when handed over and compared with what you actually sent. The same edit twice becomes a voice rule.
- **Proposals** for skills, rules or connectors are tracked in `Tracking/IMPROVEMENTS.md` from proposed to built to verified.

![Work from one project: read, capture, drafts, write](docs/assets/workbench-one-project.png)

After setup, create one Claude project named after you, attach the folder, and paste in the instructions setup writes to `.workbench/PROJECT_INSTRUCTIONS.md`. Separate projects split your memory; one keeps it whole.

## The skills

![All ten skills: what each does, how you use it, and what it writes](docs/assets/workbench-skills.png)

| Command | Use it to |
|---|---|
| `/workbench:setup` | Onboard, or change your role, tools, hours, delivery or routines. |
| `/workbench:schedules` | Make your scheduled tasks match the plan. Older look-alikes are paused, not deleted. |
| `/workbench:migrate` | Upgrade after a plugin update without losing your edits, or adopt an older vault. |
| `/workbench:librarian` | Get a health report across 34 checks: stale pages, broken links, duplicates, one-sided relationships, missed routines, a malformed commitments register, conflicts left unreconciled, pages gone quiet. |
| `/workbench:capture` | Log what a chat settled, from any chat in any surface. Usually happens on its own. |
| `/workbench:daily-briefing`, `eod-recap`, `nightly-dream`, `weekly-review`, `calendar-sync` | The routines. They run on schedule, and you can run any of them by hand. |
| `/workbench:person <name>` | Everything the folder knows about someone and what's open between you. |
| `/workbench:project <name>` | Where a project stands, what's decided, what's owed. |
| `/workbench:vault-search <question>` | Search with the folder's own rules: name variants, trust order, sources cited. |
| `/workbench:why <claim>` | Why the folder believes something: the evidence, confidence, date it came in, and what it replaced. |

## Memory and moving over

![Claude's three kinds of memory and how much to trust each](docs/assets/workbench-memory.png)

![Moving over from an older version or your own notes vault](docs/assets/workbench-moving-over.png)

**How long things stay.** The folders are layers. Captures are working memory until the dream files them that night. `Daily/` is a diary: past days are frozen and kept. People, project and org pages are long-term memory, kept current by state (live above superseded) rather than by age. Only superseded, shipped or former things move to `Archive/`, on the weekly's rules, and a page nobody has mentioned in 90 days is flagged for you to confirm, never moved. The full table is in your folder's root `CLAUDE.md`.

**Meetings come in through your recorder, not a script.** If Claude can connect to your recording tool, setup uses that: the recap reads each day's summaries, decisions and next steps, and no transcripts land in your folder. If it can't connect but the tool can export notes to a folder, setup shows you how to point the export at `Meetings/`, which the workbench then only reads. Full transcripts are kept only if you ask, after setup explains that they hold other people's exact words.

**Upgrading from 0.1?** Run `/workbench:migrate`. It adds the three new files (commitments, surfacing, run ledger), asks which Claude you have and where the folder lives so it can pick the right runner, and updates your scheduled tasks. Nothing you wrote is touched, and older claims and meeting exports keep working as they are.

**Safe upgrades.** The plugin records a hash of every file it writes in `.workbench/manifest.json`. Files nobody touched are refreshed; files you edited stay as they are and the new version lands beside them as `*.workbench-new`; content pages (people, projects, goals, logs) are never rewritten by the plugin. `/workbench:migrate` walks you through merging.

## Privacy

The folder holds real names and internal detail on your machine or in your private repo. Setup creates the repo as private and checks before the first push; repo vaults get a `.gitignore` that keeps out Obsidian workspace state, OS files and `.env` files. Never put the folder in OneDrive, Google Drive or iCloud underneath a `.git` folder: sync clients duplicate files instead of merging them. Calendar copies strip passcodes and show outside guests as a count and domain only. No secrets are ever written. Keep any repo private and never commit credentials.

## Development

```bash
python3 -m unittest discover -s tests
claude plugin validate .
```

- `scripts/workbench.py` is the stdlib-only scaffolder every skill calls.
- `blueprints/` defines the layout, routines and role packs.
- `templates/` holds the pages it renders.
- The test suite includes a package hygiene check: it fails if the plugin ever gains a `bin/` folder, an LSP server, output styles, themes or a `settings` component, any of which makes Cowork refuse to install it. One package serves Claude Code and Cowork; keep it that way.
- `docs/index.html` is the visual explainer. The images in `docs/assets/` are rendered from it by `node docs/render-assets.js`; re-run it whenever the explainer changes.

See [`CLAUDE.md`](CLAUDE.md) for contributor notes and [`CHANGELOG.md`](CHANGELOG.md) for what changed.

## License

MIT
