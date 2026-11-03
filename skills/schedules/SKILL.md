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

## 1. Pick where routines run

The routines need to read and write the workbench folder, so where they run matters. Find out
what this session can schedule:

| Option | How to tell you have it | Fits when |
|---|---|---|
| **Desktop scheduled tasks** (Cowork / Claude desktop) | a scheduled-tasks tool: list / create / update | The workbench is a local folder. The computer must be on and the app running at those times; missed runs fire when it wakes. |
| **Cloud routines** (claude.ai/code) | a tool that creates triggers or routines in the cloud | The workbench is a **private GitHub repo**. Each run clones it, writes, commits, pushes. Runs even when the laptop is closed. |

If both exist, ask which they want and explain the tradeoff in one line each. A session-only cron
(one that dies when the chat closes) is **not** a scheduler for this; don't use it.

For cloud routines, add this to the end of each prompt: "The workbench is the repository
`<owner/repo>`. Pull first. When done, commit only the files this routine owns with message
`<routine-id>: YYYY-MM-DD`, push to the default branch, and if the push is rejected, pull with
rebase and push again. Never force-push."

If neither exists, write the table from `schedules.json` into your reply and tell them how to
create the tasks by hand in the Claude desktop app (the Scheduled section) with each prompt.
Stop there.

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
