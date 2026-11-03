# Claude Workbench (plugin source)

This repo is the **Claude Workbench** plugin: a Claude Code / Cowork plugin that builds and runs a
personal knowledge vault ("workbench") for anyone, adapted to their role. It's the public,
company-neutral version of a vault design proven in daily use. Keep it neutral: no company names,
no real people, no tool instances, no internal URLs in anything shipped.

## Layout

```
.claude-plugin/   plugin.json + marketplace.json (the repo is its own marketplace)
skills/           one folder per skill; the routines' logic lives here
commands/         read-only gatherers: person, project, vault-search
hooks/            SessionStart hook -> scripts/workbench.py status --hook
scripts/          workbench.py: stdlib-only scaffolder (detect/plan/apply/schedules/status/pin)
blueprints/       base.json (folders, files, routines) + roles.json (role packs)
templates/        folders/*.md -> each folder's CLAUDE.md; pages/*.md -> starter pages
tests/            unittest suite for the scaffolder
docs/index.html   the visual explainer (self-contained, no external assets); keep it in step with the skills
```

## How the pieces fit

- **Skills hold behavior; the script holds structure.** The script never decides content. Skills
  never hand-build the folder tree. Keep that split.
- **Scheduled task prompts stay tiny.** They invoke `workbench:<skill>` and fall back to the copy
  the scaffolder writes to `<workbench>/.workbench/routines/<skill>.md`. So changing a routine means
  editing its `SKILL.md` and shipping a version; users pick it up via `/workbench:migrate` without
  touching their schedules.
- **Ownership table is a contract.** The root template (`templates/pages/root-CLAUDE.md`), each
  folder template, and each routine skill all state who writes what. If you change what a routine
  writes, change all three, plus `blueprints/base.json` `writes`.
- **Safe upgrades depend on the manifest.** `apply` records the sha256 of every file it writes.
  Plugin-managed files (every `CLAUDE.md`, READMEs in Tracking, `.workbench/*`) update only when
  untouched; content pages (`user_owned: true`) are written once and never again.

## Conventions

- Template placeholders are `{{snake_case}}` and must be supplied by `build_context`. The test
  `test_no_unrendered_placeholders` fails if one slips through.
- Prose in templates and skills: plain, direct, contractions fine, no filler. Write for a smart
  reader who's busy.
- When a skill's behavior changes, update `docs/index.html` and the README in the same change, so the
  explainer never promises something the plugin doesn't do.
- Bump `version` in both `.claude-plugin/plugin.json` and `marketplace.json`, and add a
  `CHANGELOG.md` entry. If a release changes content-page shapes, list the migration under the
  version so `/workbench:migrate` can apply it.

## Test

```bash
python3 -m unittest discover -s tests
claude plugin validate .
```
