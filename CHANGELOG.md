# Changelog

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
- Relationship graph in frontmatter: typed, two-way edges (person↔org, person↔project, reports_to↔direct_reports, project↔org/tool) as quoted wikilinks, built nightly by the dream, repaired weekly, audited by the librarian

Content migrations: none.
