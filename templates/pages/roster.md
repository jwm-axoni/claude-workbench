---
type: context
tags: [context, team]
status: active
updated: {{created_date}}
---

# Team roster

Who works for {{preferred_name}} between the scheduled briefings, and how much. The `team`
routine reads this page at the start of every run and does only what it says here. Edit it
freely: switch a persona off, change a limit, add a job under **Role workers**.

<!--
Who writes this file: {{preferred_name}} only. Routines read it and never edit it.
Models are set in .workbench/profile.json under "models", not here; /workbench:setup changes them.
-->

## Personas

- **drafter**: on · at most 5 drafts a day · replies only, for people waiting on {{preferred_name}}
- **prep**: on · at most 4 pages a day · meetings in the next 24 hours with people outside the team, and meetings {{preferred_name}} runs
- **editor**: on · checks every draft and prep page before it's saved

## Role workers

Extra jobs for the {{role_label}} role. Each one writes prep pages or Needs-you items, never
anything else.

{{role_workers}}

## Urgent pings

off

<!--
Set to "on" to let the hourly sweep send {{preferred_name}} one short message per run for items
it marks urgent, by the briefing's delivery channel, outside quiet hours in Context/surfacing.md.
Never to anyone else.
-->
