---
type: system
tags: [system, vault]
status: active
updated: {{created_date}}
---

# {{preferred_name}}'s Workbench

A folder of plain markdown files that works as {{preferred_name}}'s second brain and as the
memory for their AI agents. Open it in any editor; it's also a valid Obsidian vault.

**[`CLAUDE.md`](CLAUDE.md) is the operating contract**: folder map, what to read first, who
writes which file, frontmatter, links and archive policy. Humans and agents both read it.
Each folder has its own `CLAUDE.md` with the schema for pages in it.

This README covers the repository side only and deliberately repeats nothing from `CLAUDE.md`.
A fact kept in two files drifts.

## One fact, one place

- **One writer per file.** Two writers racing a file produce conflicts.
- **One home per schema.** The folder's `CLAUDE.md`. No templates folder.
- **One source per fact.** Where two pages disagree, the detail page wins.

## Sync (optional)

The workbench works as a plain local folder. To get history and an undo button, put it in a
private git repo and sync it (Obsidian Git works well). If you do, keep the one-writer rule:
it's what keeps the sync conflict-free.

## Privacy

This folder will hold real names and internal detail. Keep any repo private, and never commit
credentials, API keys or `.env` files.

Built with the Claude Workbench plugin v{{version}}. Plugin bookkeeping lives in `.workbench/`.
