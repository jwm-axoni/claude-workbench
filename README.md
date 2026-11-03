<div align="center">

<img alt="Claude Workbench: a second brain Claude runs for you, in plain markdown files you own. Hand-drawn loop: morning briefing, evening recap, nightly dream, your pages, every workday." src="docs/assets/workbench-header.png" width="100%">

One plugin interviews you, builds a folder of markdown around your role and tools, schedules the routines that keep it current, and learns from what you correct and what you actually send.

![Plugin: Claude Code and Cowork](https://img.shields.io/badge/plugin-Claude_Code_%26_Cowork-232323)
![Files: plain Markdown](https://img.shields.io/badge/files-plain_Markdown-FF824D)
![Routines: six, scheduled](https://img.shields.io/badge/routines-six_scheduled-232323)
![Learning: measured weekly](https://img.shields.io/badge/learning-measured_weekly-FF824D)
![Role packs: 11](https://img.shields.io/badge/role_packs-11-232323)
![License: MIT](https://img.shields.io/badge/license-MIT-FF824D)

[Install](#install) · [Setup](#say-set-me-up) · [The folder](#your-folder) · [The routines](#the-routines) · [How it learns](#how-it-learns) · [Skills](#the-skills) · [Visual explainer](docs/index.html)

</div>

## The problem it solves

Out of the box, Claude is smart and knows nothing about you. Not your team, not your accounts, not what "urgent" means to you, not the words your group uses that appear in no manual. So you re-explain yourself in every chat, and drafts sound like a polite stranger wrote them.

The Workbench gives Claude a memory that lives in plain files you own, six routines that run your day on a schedule, and a nightly pass where Claude reads what happened, learns from it, and updates what it knows. It measures whether it's getting better instead of assuming it is.

It's the public, company-neutral version of a setup that's been running daily since September 2026. Nothing in it names a company, a person or a tool instance. Everything specific to you is gathered during onboarding.

## Install

In Claude Code or Cowork:

```
/plugin marketplace add jwm-axoni/claude-workbench
/plugin install workbench@claude-workbench
```

Then run `/workbench:setup`, or just say "set me up". You need Python 3 on the machine that runs setup; macOS and most Linux installs already have it.

![What's in the box: ten skills, six of which run themselves on a schedule](docs/assets/workbench-whats-in-the-box.png)

## Say "set me up"

![The setup walkthrough, from checking the folder to making one project your home](docs/assets/workbench-setup.png)

About ten minutes, and you never touch a file by hand. Re-run it whenever your role, tools, hours or delivery preference change; it asks only what changed and never overwrites a file you've edited.

![Role packs decide which sources each routine watches first](docs/assets/workbench-role-packs.png)

Your title picks one of 11 role packs: sales, customer success, marketing, engineering, product, operations, people, IT and security, finance, leadership, or general. The pack sets the tag vocabulary, which sources the recap sweeps first, what the briefing and weekly watch for, and any guardrails, such as keeping candidate and employee data out of the folder entirely.

## Your folder

![The folder layout, with a CLAUDE.md schema in every folder](docs/assets/workbench-folder.png)

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

Times come from your working hours and timezone, and you can switch any routine off. They run either as scheduled tasks in the Claude desktop app or Cowork, which need the computer awake, or as cloud routines, which need the folder in a private GitHub repo. Setup asks which.

![The nightly dream: four things it produces, all landing on your pages with a receipt](docs/assets/workbench-nightly-dream.png)

![What a week looks like once it's running](docs/assets/workbench-week.png)

## How it learns

![The digest arrives by Slack, email, Claude, or not at all](docs/assets/workbench-delivery.png)

Most people won't open a folder every morning. Setup asks where your digest should land, sends a test, and reads your replies back in as answers. The digest is the only thing a routine ever sends, and only to you. Routines read your tools; they never post, reply or change anything in them.

![Three learning loops and the weekly scorecard that tracks whether it's working](docs/assets/workbench-learning.png)

- **Corrections** become rules in `Context/voice.md` or `Context/me.md`. If the same correction comes back after the rule exists, the rule is flagged as not working.
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
| `/workbench:librarian` | Get a health report: stale pages, broken links, duplicates, one-sided relationships, missed routines. |
| `/workbench:capture` | Log what a chat settled. Usually happens on its own. |
| `/workbench:daily-briefing`, `eod-recap`, `nightly-dream`, `weekly-review`, `calendar-sync` | The routines. They run on schedule, and you can run any of them by hand. |
| `/workbench:person <name>` | Everything the folder knows about someone and what's open between you. |
| `/workbench:project <name>` | Where a project stands, what's decided, what's owed. |
| `/workbench:vault-search <question>` | Search with the folder's own rules: name variants, trust order, sources cited. |

## Memory and moving over

![Claude's three kinds of memory and how much to trust each](docs/assets/workbench-memory.png)

![Moving over from an older version or your own notes vault](docs/assets/workbench-moving-over.png)

**Safe upgrades.** The plugin records a hash of every file it writes in `.workbench/manifest.json`. Files nobody touched are refreshed; files you edited stay as they are and the new version lands beside them as `*.workbench-new`; content pages (people, projects, goals, logs) are never rewritten by the plugin. `/workbench:migrate` walks you through merging.

## Privacy

The folder holds real names and internal detail on your machine or in your private repo. Calendar copies strip passcodes and show outside guests as a count and domain only. No secrets are ever written. Keep any repo private and never commit credentials.

## Development

```bash
python3 -m unittest discover -s tests
claude plugin validate .
```

- `scripts/workbench.py` is the stdlib-only scaffolder every skill calls.
- `blueprints/` defines the layout, routines and role packs.
- `templates/` holds the pages it renders.
- `docs/index.html` is the visual explainer. The images in `docs/assets/` are rendered from it by `node docs/render-assets.js`; re-run it whenever the explainer changes.

See [`CLAUDE.md`](CLAUDE.md) for contributor notes and [`CHANGELOG.md`](CHANGELOG.md) for what changed.

## License

MIT
