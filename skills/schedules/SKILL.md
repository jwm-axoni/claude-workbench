---
name: schedules
description: Create, update or remove the workbench's scheduled routines so they exactly match .workbench/schedules.json. Finds every existing "[Workbench] …" scheduled task (and older look-alikes), then updates, replaces, deletes or creates as needed, never leaving duplicates. Use after setup or migrate, when someone changes their hours or turns a routine on or off, or says "fix my scheduled tasks", "my briefing didn't run", /workbench:schedules.
---

# Workbench schedules

Make the real scheduled tasks match the desired set. Desired state lives in the workbench at
`.workbench/schedules.json`. Regenerate it first so it reflects the current profile:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workbench.py" schedules --root "<workbench>"
```

Each routine there has `id`, `name` (always `[Workbench] …`), `cron`, `timezone`, `when` (human
text) and `prompt`. The prompt is deliberately short: it invokes the plugin skill, with the copy in
`.workbench/routines/` as a fallback, so upgrading the plugin upgrades the routines without
touching the schedule.

## 1. Pick the runner

The routines need to read and write the workbench folder, so where they run decides what's
guaranteed. The runner follows from two facts in `.workbench/profile.json`: which surface the owner
has (`surface`: `cowork` or `code`) and where the vault lives (`vault_home`: `local` or `repo`).
Setup records both. Don't ask the owner to pick a runner; derive it:

| You have | The vault lives in | Routines run on | What's guaranteed |
|---|---|---|---|
| Cowork only | a local folder | Cowork local | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. |
| Cowork only | a private GitHub repo, worked from a local clone | Cowork local, on the clone | Runs only while the computer is on and the desktop app is open. No documented catch-up: the run ledger and gap detection recover missed runs. The repo adds backup, history and safe use from more than one computer. |
| Claude Code | a local folder | Code Desktop local | Runs while the desktop app is open. Exactly one catch-up run for the most recent missed run within 7 days. |
| Claude Code | a private GitHub repo, worked from a local clone | Code cloud | Runs with the laptop closed. Research preview: fresh clone per run, pushes to `claude/` branches, minimum interval one hour. No documented catch-up: the run ledger and gap detection cover misses. |

Store the result as `runner` in the profile (`cowork-local`, `code-desktop`, `code-cloud`).

**Runner 1, Cowork local** (Cowork-only users). Scheduled tasks in Cowork, against the local vault
folder (or the local clone of a repo vault). They run only while the computer is on and the
desktop app is open. A task that needs local files runs locally even where Cowork can run tasks in
the cloud. Anthropic documents no catch-up, retry or failure notice for this case, so recovery is
built into the routines: each one appends to `Tracking/Signals/RUN_LEDGER.md`, the briefing names
any routine missing from it, the dream files every unprocessed capture whatever its date, and the
recap writes a reconstructed file for a missed day.

**Runner 2, Code Desktop local** (Code users, local vault). Scheduled tasks in the Claude Code
desktop app. Documented behavior: on wake or app start, exactly one catch-up run for the most
recent missed run within 7 days; older misses are skipped and listed in the task's History. The
run ledger still records every run, so the briefing can tell a catch-up from a skip.

**Runner 3, Code cloud** (Code users, repo vault). Cloud scheduled tasks against the private
GitHub repo. A research preview. Each run starts from a fresh clone, can push only to `claude/`
branches, and the minimum interval is one hour. No catch-up and no automatic retry are documented.
Add this to the end of each prompt:

"The workbench is the repository `<owner/repo>`. Before reading anything, fetch and merge every
unmerged `claude/workbench-*` branch into your working copy, so you see the earlier runs' work;
if a merge conflicts, stop, append a `failed` line to the run ledger naming the branches, and
push nothing else. When done, commit only the files this routine owns, with message
`<routine-id>: YYYY-MM-DD`, and push to the branch `claude/workbench-<routine-id>-YYYY-MM-DD`.
Never force-push."

The owner's side is one ritual: **the first local session of the day pulls and merges the
`claude/` branches before the briefing reads the vault** (or the owner merges the newest one in
one click on GitHub; each branch already contains the earlier ones). Because each routine commits
only files it owns, merges conflict only where git can show it. If cloud tasks are unavailable or
switched off for the account, fall back to Runner 2 against the local clone; never run both for the
same routine.

**Plan notes.** On Team and Enterprise plans, Cowork sessions run in the cloud only if the
organization turns on "Run Cowork in the cloud" (Organization settings > Cowork), and even then a
task that requires local files runs locally. On personal plans there's no location choice. Either
way, a workbench in a local folder runs locally.

**What isn't a scheduler.** A session-only cron (one that dies when the chat closes) is not a
scheduler for this; don't use it. If the tools for the derived runner aren't in this session
(for example, Cowork-only and you're in a plain chat), write the table from `schedules.json` into
your reply and tell them how to create the tasks by hand in the Claude desktop app (the Scheduled
section) with each prompt. Stop there.

**Duplicates across surfaces.** The same routine can exist on more than one surface (a Cowork task
and a Code Desktop task, or a desktop task and a cloud task). Inventory every surface you can see
in step 2, and keep exactly one per routine, on the derived runner.

## 2. Inventory what exists

List every scheduled task you can see. Sort each into:

- **Ours, current:** name starts with `[Workbench]` and matches a desired `id`/`name`.
- **Ours, retired:** name starts with `[Workbench]` but no desired routine has that name.
- **Look-alikes:** not prefixed, but clearly an older version of the same job, e.g. "daily
  briefing", "vault-dream", "EOD recap", "weekly plan", or any task whose prompt points at this
  workbench folder. Show these to the person and ask, one line each: replace with the workbench
  version, or leave alone? Replacing means **pausing** (disabling) the old task, not deleting it,
  so its wording survives and it can be switched back on. Delete only if the tool can't pause, and
  only with an explicit yes.
- **Unrelated:** leave alone and don't mention them.

If two tasks map to the same routine, that's a duplicate. Keep one (prefer the one already
named correctly) and delete the other after saying so.

## 3. Reconcile

Show the plan as one small table (routine · action · when) and get a yes, then apply it:

| Situation | Action |
|---|---|
| desired, not present | **create** with the exact `name`, `cron`, `timezone`, `prompt` |
| present, cron/prompt/timezone differ | **update** in place (keeps its history); if the tool can't update, delete then create |
| present and identical | leave it |
| ours, retired | **delete** |
| look-alike the person said to replace | pause it, then create ours |

Cron expressions are in the routine's `timezone`. If the scheduling tool only accepts UTC, convert
it and note the conversion, since daylight saving shifts it twice a year; prefer a tool option that
takes a timezone when there is one.

If the tool supports it, turn on notifications only for failures. Nobody needs six pings a day.

## 4. Verify and record

1. List tasks again and confirm each desired routine exists exactly once with the right schedule.
2. Offer to run the Morning Briefing once now as a test, and look at the file it wrote.
3. Append to `Tracking/FRICTION_LOG.md` under `## Resolved` one line: today's date, "routines
   reconciled", and what was created, updated or deleted. That's the audit trail if a routine
   later goes missing.

Finish with the final table: routine, when (in their timezone), where it runs.
