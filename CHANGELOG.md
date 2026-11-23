# Changelog

## Unreleased (0.3.0)

A proactive Workbench: something now watches between the scheduled briefings, and a small team does the work before the owner gets to it.

- New routine `sweep` (`[Workbench] Sweep`): hourly through the working day, the first run just before the morning briefing. Reads every reachable source for what came in since its last `ok` line in the run ledger (capped at 96 hours, the rest recorded as a gap; a source a `partial` run couldn't reach gets its own longer window, so one broken connector doesn't make every run reread everything), sorts items as `urgent`, `reply-owed`, `prep-needed`, `commitment-candidate` or `fyi`, dedupes by source id, and appends one section to `Tracking/Queue/YYYY-MM-DD_sweep.md`. Never drafts, sends or edits a page. A closed-laptop night is covered by the next morning's first run, so the sweep stays local; a Cowork cloud task was tested and rejected (its files land in a throwaway sandbox, and nothing reads them until the laptop opens)
- The briefing and midday update read the queue first and go to live sources only for what it doesn't cover; lines that came from a queue item carry its `q-` id. A missed sweep hour isn't a gap; the briefing names the sweep only when it has no `ok` line since the last briefing or reports a capped window
- Every routine names a `model` (`haiku`, `sonnet` or `opus`) in `.workbench/schedules.json`: the sweep and calendar sync default to `haiku`, the rest to `sonnet`. Override per routine with `models` in the profile. The `schedules` skill sets it on each task, or tells the owner which to pick when the tool can't, and keeps any model the owner already chose by hand by writing it into `models`
- The librarian's missed-routine check and the weekly's ran-vs-expected count the sweep once per workday, not per hourly run
- Working hours that cross midnight wrap the sweep's hours instead of failing
- New routine `team` (`[Workbench] Team`, Sonnet): runs at :45 at least 15 minutes before the briefing and before the midday update, right after a sweep. Stops after one cheap check when nothing is queued. Three personas, each switchable in `Context/roster.md`: the drafter writes reply drafts into `Tracking/Drafts/` (`by: team-drafter`, `queue: q-…`, graded by the recap like any draft), prep writes `Tracking/Prep/YYYY-MM-DD_<slug>.md`, and the editor checks both (facts traced, voice rules, never-surface, no secrets) and holds what fails twice. Records what it handled in `Tracking/Signals/YYYY-MM-DD_team.md`. Never sends
- Roster `Context/roster.md` (user-owned): personas on or off, daily limits, role workers from the role pack (`workers` in `roles.json`; sales ships a deal desk), and urgent pings (off by default)
- `Tracking/NEEDS_YOU.md`: decisions only the owner can make, each with a recommended answer, append-only like the run ledger. The team appends `open` items, the recap appends `answered` lines from digest replies and `answer: n-…` captures. The briefing asks open items right after the dream's questions, with their `n-` ids
- The sweep may send the owner one urgent ping per run, only when `Context/roster.md` turns it on; a new dated standing exception in the root `CLAUDE.md`. Every routine's prompt now points at the standing exceptions
- The briefing links team drafts under **Replies owed** and prep pages under **Today**, and the digest lists what was drafted
- Migration: `/workbench:migrate` adds `Tracking/Queue/README.md`, `Tracking/Prep/README.md`, `Context/roster.md`, `Tracking/NEEDS_YOU.md` and the fallback routine copies; `/workbench:schedules` then offers the Sweep and Team tasks

## 0.2.0 — 2026-11-07

Dual-runtime support and memory that behaves more like judgment than storage.

- Dual-runtime support: one package for Claude Code and Cowork-only users. Three runners (Cowork local, Code Desktop local, Code cloud), derived by setup from which Claude you have and a new vault-home question (local folder or private GitHub repo), with the guarantee for each stated the same way in the schedules and setup skills, the README and the explainer. Notes the Team and Enterprise "Run Cowork in the cloud" organization toggle, and that tasks needing local files run locally either way
- Repo vaults: setup creates the repo private and verifies it before the first push; the scaffolder writes a `.gitignore`; cloud runs merge earlier `claude/` branches before reading and push to their own `claude/` branch; the first local session of the day pulls and merges; never force-push
- Run ledger and gap detection: every routine appends one line to `Tracking/Signals/RUN_LEDGER.md` (the one documented exception to one writer per file). The briefing checks it first and names any missed routine with its consequence; the dream files every unprocessed capture whatever its date; the recap writes a short `reconstructed` file for a missed day; late runs label themselves. The librarian's missed-routine check reads the ledger, and so does the SessionStart hook
- Commitments register `Tracking/COMMITMENTS.md`: the dream adds rows and sets `looks-done` / `looks-stale`; the briefing asks about overdue rows as questions; only the weekly closes rows, moving them to `Archive/Superseded/`
- Contradiction queue: the weekly turns the oldest three `## Needs reconciling` sections into numbered questions; the dream files the answers as supersessions with the losing claim's history kept
- Surfacing layer `Context/surfacing.md`: always surface, never surface, quiet hours, format preferences. The briefing applies it; the dream learns rules the way it learns voice rules (standing after two signals)
- Claim lineage: new briefing and recap claims carry `evidence:` (a quote of 25 words or fewer, or a page reference) and `confidence:`. New read-only command `/workbench:why <claim>` shows the evidence, confidence, entry date and supersession chain
- Capture works from any chat in any surface; a chat that can't reach the folder hands back the capture lines to paste
- Project instructions gain Cowork-only and repo-vault blocks, kept or dropped by the scaffolder to match the profile
- Librarian: 34 checks (five new: commitments register shape, surfacing page sections, reconciling sections older than 14 days, repo clone behind its remote, dormant pages nobody has mentioned in 90 days)
- How memory works: the root `CLAUDE.md` gains a table of the memory layers (captures, diary, long-term pages, measurement, meetings, archive), what each holds, how long it stays live, and what moves it. Nothing new is archived by age
- Meetings, connector first: setup uses the recorder's connector when it works (no `Meetings/` folder, no transcripts in the vault; the recap and briefing read summaries, decisions and next steps through it), falls back to pointing the tool's own export at `Meetings/`, and keeps full transcripts only on request, after explaining the privacy cost. No sync script. `Meetings/` is owned by the recorder and never moved by the workbench
- Package hygiene test: fails if the package ever gains a `bin/` folder, an LSP server, output styles, themes, or a `settings` component, any of which makes Cowork refuse the plugin

Content migrations:
- New files, created by `/workbench:migrate` through the normal `apply` path: `Tracking/COMMITMENTS.md`, `Tracking/Signals/RUN_LEDGER.md`, `Context/surfacing.md`, and `.gitignore` for repo vaults. A file you already have under one of those names is never overwritten; it becomes a `.workbench-new` conflict to merge.
- Profile gains `surface`, `vault_home`, `repo` and `meetings_via` (`connector` or `export`); migrate asks for them if missing. A profile that names a `meetings_source` without `meetings_via` keeps its `Meetings/` folder, as before.
- Claim lines written before 0.2.0 keep their old shape (bare confidence, no evidence). Nothing is rewritten.
- Scheduled task prompts change (each routine's "writes" now names its run-ledger line); `/workbench:schedules` updates them in place.

## 0.1.0 — 2026-11-03

First public release.

- Onboarding interview with connector checks and role packs (11 roles)
- Vault layout: Context, Daily, Projects, People, Organizations, Resources, Tracking, Meetings (optional), Archive, each with its own CLAUDE.md
- Six routines as `[Workbench]` scheduled tasks: calendar sync, morning briefing, midday update, end-of-day recap, nightly dream, weekly plan and maintenance
- Self-improvement loop: captures from the one project, corrections turned into rules by the dream, claims graded by the recap, thresholds tuned weekly on evidence
- Safe upgrades via a hash manifest and `.workbench-new` conflict files; adoption of existing vaults
- Read-only commands: person, project, vault-search
- Daily digest delivery chosen at setup (Slack DM, email, Claude, or none), tested during setup; replies flow back as answers
- Outcome learning: drafts saved to `Tracking/Drafts/` and graded against what was actually sent; voice rules learned from repeated edits; `Tracking/IMPROVEMENTS.md` tracks proposed skills/rules through adoption and verification; weekly learning scorecard
- Project instructions in READ / CAPTURE / DRAFTS / WRITE form
- Optional starter Obsidian config
- Visual explainer at `docs/index.html`
- Schedules pause older look-alike tasks instead of deleting them
- Relationship graph in frontmatter: typed, two-way edges (person↔org, person↔project, reports_to↔direct_reports, project↔org/tool) as quoted wikilinks, built nightly by the dream, repaired weekly, audited by the librarian

Content migrations: none.
