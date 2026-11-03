#!/usr/bin/env python3
"""Claude Workbench scaffolder.

Deterministic, idempotent, stdlib-only. The skills call this so every workbench has the same
shape and re-runs are safe.

    workbench.py detect    --root PATH
    workbench.py plan      --root PATH [--profile PROFILE.json]
    workbench.py apply     --root PATH [--profile PROFILE.json]
    workbench.py schedules --root PATH [--profile PROFILE.json]
    workbench.py status    --root PATH [--hook]
    workbench.py pin|unpin --root PATH --path REL

Safety rules this script enforces:
  * It never deletes or moves a user file.
  * A file it wrote earlier that nobody has touched may be updated in place.
  * A file someone edited (or one that existed before the workbench) is never overwritten;
    the new version goes beside it as `<name>.workbench-new` and is reported as a conflict.
  * Content pages (me.md, GOALS.md, logs, people, tools...) are written once, then belong to
    the user and the routines. Upgrades never touch them.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS = PLUGIN_ROOT / "blueprints"
TEMPLATES = PLUGIN_ROOT / "templates"
SKILLS = PLUGIN_ROOT / "skills"
SYSTEM_DIR = ".workbench"
MANIFEST = f"{SYSTEM_DIR}/manifest.json"
PROFILE = f"{SYSTEM_DIR}/profile.json"
NEW_SUFFIX = ".workbench-new"
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
REACH = {"connected": "yes", "available": "no (needs auth)", "missing": "no", "manual": "manual"}


# ---------------------------------------------------------------- small helpers

def plugin_version() -> str:
    try:
        return json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]
    except Exception:
        return "0.0.0"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render(template: str, ctx: dict) -> str:
    """Replace {{key}} for known keys only; unknown keys are left untouched."""
    return re.sub(r"\{\{([a-z_]+)\}\}", lambda m: str(ctx[m.group(1)]) if m.group(1) in ctx else m.group(0), template)


def bullets(items, empty="_Not set yet._") -> str:
    items = [str(i).strip() for i in (items or []) if str(i).strip()]
    return "\n".join(f"- {i}" for i in items) if items else empty


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|#^\[\]]', "", name).strip() or "Untitled"


def hhmm(value, default: str) -> tuple[int, int]:
    m = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", str(value or "")) or re.match(r"^(\d{1,2}):(\d{2})$", default)
    return min(int(m.group(1)), 23), min(int(m.group(2)), 59)


def shift(t: tuple[int, int], minutes: int) -> tuple[int, int]:
    total = (t[0] * 60 + t[1] + minutes) % (24 * 60)
    return total // 60, total % 60


def fmt(t: tuple[int, int]) -> str:
    return f"{t[0]:02d}:{t[1]:02d}"


def parse_workdays(value) -> list[int]:
    if not value:
        return [1, 2, 3, 4, 5]
    if isinstance(value, str):
        value = value.strip()
        if re.fullmatch(r"[A-Za-z]{3,}\s*-\s*[A-Za-z]{3,}", value):
            a, b = [DAYS.index(x.strip()[:3].title()) for x in value.split("-")]
            return list(range(a, b + 1)) if a <= b else list(range(a, 7)) + list(range(0, b + 1))
        value = re.split(r"[,\s]+", value)
    out = sorted({DAYS.index(str(d)[:3].title()) for d in value if str(d)[:3].title() in DAYS})
    return out or [1, 2, 3, 4, 5]


def cron_days(days: list[int]) -> str:
    days = sorted(days)
    if len(days) > 1 and days == list(range(days[0], days[-1] + 1)):
        return f"{days[0]}-{days[-1]}"
    return ",".join(map(str, days))


def strip_frontmatter(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S).lstrip()


# ---------------------------------------------------------------- profile -> context

def load_blueprints():
    return (json.loads((BLUEPRINTS / "base.json").read_text()),
            json.loads((BLUEPRINTS / "roles.json").read_text()))


def resolve_role_pack(profile: dict, roles: dict) -> str:
    explicit = (profile.get("role_pack") or "").strip()
    if explicit in roles:
        return explicit
    role = f" {(profile.get('role') or '').lower()} "
    best, best_len = "general", 0
    for key, pack in roles.items():
        for term in pack.get("match", []):
            if re.search(rf"(?<![a-z]){re.escape(term)}(?![a-z])", role) and len(term) > best_len:
                best, best_len = key, len(term)
    return best


def routine_times(profile: dict) -> dict:
    hours = profile.get("work_hours") or {}
    start, end = hhmm(hours.get("start"), "09:00"), hhmm(hours.get("end"), "17:30")
    days = parse_workdays(hours.get("days"))
    custom = profile.get("routine_times") or {}
    t = {
        "brief": hhmm(custom.get("daily-briefing"), fmt(shift(start, -30))),
        "midday": hhmm(custom.get("midday-update"), "12:00"),
        "recap": hhmm(custom.get("eod-recap"), fmt(shift(end, 30))),
        "dream": hhmm(custom.get("nightly-dream"), "22:00"),
        "weekly": hhmm(custom.get("weekly"), fmt(shift(start, -90))),
    }
    cal = shift(start, -60)
    return {"start": start, "end": end, "days": days, "t": t,
            "cal_minute": cal[1], "cal_hours": sorted({cal[0], 11, end[0]})}


def build_context(profile: dict, root: Path):
    base, roles = load_blueprints()
    pack_key = resolve_role_pack(profile, roles)
    pack = roles[pack_key]
    times = routine_times(profile)

    name = (profile.get("name") or "Workbench Owner").strip()
    preferred = profile.get("preferred_name") or name.split()[0]
    company = (profile.get("company") or "").strip()
    team = (profile.get("team") or "").strip()
    tools = profile.get("tools") or []
    conns = {c.get("tool"): c for c in profile.get("connections", []) if c.get("tool")}

    rows = []
    for tool in list(dict.fromkeys(tools + list(conns))):
        c = conns.get(tool, {})
        rows.append(f"| [[{safe_filename(tool)}]] | {REACH.get(c.get('status'), 'unchecked')} | "
                    f"{c.get('via') or c.get('notes') or '—'} |")

    guardrails = pack.get("guardrails", []) + profile.get("guardrails", [])
    meetings_source = (profile.get("meetings_source") or "").strip()
    function_tags = list(dict.fromkeys(pack.get("function_tags", []) + profile.get("extra_tags", [])))

    delivery = profile.get("delivery") or {}
    channel = (delivery.get("channel") or "claude").lower()
    target = delivery.get("target") or {"slack": "a DM to themselves", "email": "their own inbox"}.get(channel, "")
    delivery_label = {
        "slack": f"a Slack message ({target})",
        "email": f"an email ({target})",
        "claude": "the scheduled task's own message in the Claude app",
        "none": "nothing sent; the briefing file only",
    }.get(channel, channel)

    ctx = {
        "version": plugin_version(),
        "delivery_channel": channel,
        "delivery_label": delivery_label,
        "meetings_rule": ("`Meetings/` is the authoritative record of what was said and assigned. Read only above\n"
                          "the `## Transcript` marker. Files sharing an export id are one meeting exported more than\n"
                          "once: read the longest.\n") if meetings_source else "",
        "meetings_never": " `Meetings/`," if meetings_source else "",
        "created_date": profile.get("created_date") or dt.date.today().isoformat(),
        "name": name,
        "preferred_name": preferred,
        "role": profile.get("role") or "role not recorded",
        "role_pack": pack_key,
        "role_label": pack["label"],
        "company": company or "their company",
        "company_description": profile.get("company_description") or "not recorded yet.",
        "industry": profile.get("industry") or "not recorded",
        "team_suffix": f", {team} team" if team else "",
        "manager": (profile.get("manager") or "").strip(),
        "reports_to_yaml": f'"[[{profile["manager"]}]]"' if profile.get("manager") else '""',
        "manager_related": f"- [[{profile['manager']}]] — manager `source: workbench-setup`" if profile.get("manager") else "",
        "manager_yaml_item": f', "[[{profile["manager"]}]]"' if profile.get("manager") else "",
        "manager_line": f"Reports to [[{profile['manager']}]]." if profile.get("manager") else "",
        "location": profile.get("location") or "location not recorded",
        "timezone": profile.get("timezone") or "UTC",
        "work_start": fmt(times["start"]),
        "work_end": fmt(times["end"]),
        "workdays": ", ".join(DAYS[d] for d in times["days"]),
        "communication_style": profile.get("communication_style") or "Direct and concise. Lead with the answer.",
        "work_style": bullets(profile.get("work_style"),
                              "_Fill in as you learn it: how they plan, when they do deep work, what they hate._"),
        "urgent_means": bullets(profile.get("urgent_means"),
                                "- A request from their manager or a customer with a same-day deadline\n"
                                "- Anything blocking someone else's work"),
        "private_blocks": bullets(profile.get("private_blocks"),
                                  "_None recorded. Personal or focus blocks listed here are never mentioned in a briefing._"),
        "goals_list": bullets(profile.get("goals"), "_Not set yet. Add them in `Tracking/GOALS.md`._"),
        "goals_inline": "; ".join(profile.get("goals", [])) or "not set yet",
        "tools_inline": ", ".join(tools) or "none listed",
        "connections_rows": "\n".join(rows) or "| _none listed_ | | |",
        "briefing_lens": bullets(pack.get("briefing_lens", []) + pack.get("weekly_lens", [])),
        "function_tags": ", ".join(f"`{x}`" for x in function_tags),
        "guardrails_rules": "\n".join(f"{4 + i}. {g}" for i, g in enumerate(guardrails)),
        "meetings_source": meetings_source or "a meeting recorder",
        "meetings_row": ("\n| `Meetings/` | One file per meeting, exported from " + meetings_source +
                         " | Never by hand: the export writes it |") if meetings_source else "",
        "workbench_path": str(profile.get("workbench_path") or root),
        "workdays_cron": cron_days(times["days"]),
        "first_workday_cron": str(times["days"][0]),
        "cal_minute": times["cal_minute"],
        "cal_hours": ",".join(map(str, times["cal_hours"])),
        "cal_times": ", ".join(fmt((h, times["cal_minute"])) for h in times["cal_hours"]),
    }
    for k, v in times["t"].items():
        ctx[f"{k}_time"], ctx[f"{k}_hour"], ctx[f"{k}_minute"] = fmt(v), v[0], v[1]
    return ctx, base, pack


# ---------------------------------------------------------------- desired state

def desired_routines(profile: dict, ctx: dict, base: dict) -> list[dict]:
    toggles = profile.get("routines") or {}
    has_calendar = any(re.search(r"calendar|outlook", str(t), re.I) for t in profile.get("tools", []))
    out = []
    for r in base["routines"]:
        default = has_calendar if r["id"] == "calendar-sync" else True
        if not toggles.get(r["id"], default):
            continue
        mode = f" in **{r['mode']}** mode" if r.get("mode") else ""
        prompt = (
            f"Run the Claude Workbench `{r['skill']}` routine{mode} for the workbench at `{ctx['workbench_path']}`.\n\n"
            f"1. If the `workbench:{r['skill']}` skill is available, invoke it{mode} and follow it exactly.\n"
            f"2. Otherwise read `{ctx['workbench_path']}/{SYSTEM_DIR}/routines/{r['skill']}.md` and follow it exactly.\n\n"
            f"Today's date is the date this runs, in {ctx['timezone']}. Read the workbench's root `CLAUDE.md` first. "
            f"This routine writes only: {r['writes']}. Read sources; never send, post or change anything outside the workbench."
        )
        out.append({"id": r["id"], "name": r["name"], "skill": r["skill"], "mode": r.get("mode"),
                    "when": render(r["when"], ctx), "cron": render(r["cron"], ctx),
                    "timezone": ctx["timezone"], "writes": r["writes"], "prompt": prompt})
    return out


TOOL_PAGE = """---
type: tool
category: {category}
tags: [tool]
status: active
connected: {connected}
projects: []
updated: {{{{created_date}}}}
---

# {tool}

What {{{{preferred_name}}}} uses {tool} for: _fill in._

## How Claude reaches it
{via}

## Current state (dream)
_Maintained nightly by nightly-dream._

## Related
### People
- [[{{{{name}}}}]]
"""


def desired_state(profile: dict, root: Path):
    ctx, base, _pack = build_context(profile, root)
    flags = {"meetings": bool(profile.get("meetings_source")), "company": bool(profile.get("company")),
             "obsidian": profile.get("obsidian", True) is not False, "manager": bool(profile.get("manager"))}
    dirs, files = [], []

    def add(path: str, content: str, user_owned: bool):
        files.append({"path": path, "content": content, "user_owned": user_owned})

    routines = desired_routines(profile, ctx, base)
    table = ["| Routine (scheduled task) | When | Owns, and writes nothing else |", "|---|---|---|"]
    table += [f"| `{r['skill']}`{' (' + r['mode'] + ')' if r.get('mode') else ''} | {r['when']} | {r['writes']} |"
              for r in routines]
    ctx["routine_table"] = "\n".join(table) if routines else "_No routines enabled. Run `/workbench:schedules` to add them._"

    for f in base["folders"]:
        if f.get("when") and not flags.get(f["when"]):
            continue
        dirs.append(f["path"])
        if f.get("template"):
            add(f"{f['path']}/CLAUDE.md", render((TEMPLATES / f["template"]).read_text(), ctx), False)

    for f in base["files"]:
        if f.get("when") and not flags.get(f["when"]):
            continue
        path = render(f["path"], {k: safe_filename(str(v)) for k, v in ctx.items()})
        add(path, render((TEMPLATES / f["template"]).read_text(), ctx), bool(f.get("user_owned")))

    conns = {c.get("tool"): c for c in profile.get("connections", []) if c.get("tool")}
    for tool in profile.get("tools", []):
        c = conns.get(tool, {})
        status = c.get("status")
        via = c.get("via") or ("Manual: paste or export." if status == "manual"
                               else "Not connected yet. Connect it, then run `/workbench:setup` again.")
        page = TOOL_PAGE.format(tool=tool, category=c.get("category", "productivity"),
                                connected={"connected": "yes", "manual": "manual"}.get(status, "no"), via=via)
        add(f"Resources/Tools/{safe_filename(tool)}.md", render(page, ctx), True)

    for skill in sorted({r["skill"] for r in base["routines"]} | {"librarian"}):
        src = SKILLS / skill / "SKILL.md"
        if src.exists():
            add(f"{SYSTEM_DIR}/routines/{skill}.md",
                f"<!-- Copied from the Claude Workbench plugin v{ctx['version']} (skills/{skill}). Fallback for "
                f"scheduled tasks when the plugin skill isn't loaded. Don't edit; run /workbench:migrate. -->\n\n"
                + strip_frontmatter(src.read_text()), False)

    add(f"{SYSTEM_DIR}/schedules.json",
        json.dumps({"timezone": ctx["timezone"], "routines": routines}, indent=2, ensure_ascii=False) + "\n", False)
    stored = dict(profile)
    stored.setdefault("created_date", ctx["created_date"])
    stored["role_pack"] = ctx["role_pack"]
    add(PROFILE, json.dumps(stored, indent=2, ensure_ascii=False) + "\n", False)
    return ctx, dirs, files, routines


# ---------------------------------------------------------------- detect / plan / apply

def read_manifest(root: Path) -> dict | None:
    p = root / MANIFEST
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return {"corrupt": True, "files": {}}


ADOPT_HINTS = [
    (r"^context$|about|^me$", "Context"),
    (r"daily|journal|briefing|recap", "Daily"),
    (r"project", "Projects"),
    (r"people|person|contacts", "People"),
    (r"org|compan|account|customer|client", "Organizations"),
    (r"resource|reference|knowledge|tools?$|research|wiki", "Resources"),
    (r"track|goal|metric|log", "Tracking"),
    (r"meeting|transcript|call", "Meetings"),
    (r"archive|old|done|past", "Archive"),
]
KNOWN = {"Context", "Daily", "Projects", "People", "Organizations", "Resources", "Tracking", "Meetings", "Archive"}


def detect(root: Path) -> dict:
    if not root.exists():
        return {"state": "fresh", "root": str(root), "exists": False}
    entries = [e for e in root.iterdir() if not e.name.startswith(".") and e.name != "Thumbs.db"]
    manifest = read_manifest(root)
    info = {
        "root": str(root),
        "exists": True,
        "obsidian_vault": (root / ".obsidian").exists(),
        "git_repo": (root / ".git").exists(),
        "has_claude_md": (root / "CLAUDE.md").exists(),
        "markdown_files": sum(1 for _ in root.rglob("*.md")) if entries else 0,
        "top_level": sorted(e.name + ("/" if e.is_dir() else "") for e in entries),
    }
    if manifest is not None:
        info.update(state="workbench", installed_version=manifest.get("plugin_version"),
                    plugin_version=plugin_version(), created=manifest.get("created"),
                    updated=manifest.get("updated"), corrupt=bool(manifest.get("corrupt")),
                    upgrade_available=manifest.get("plugin_version") != plugin_version(),
                    has_profile=(root / PROFILE).exists())
        return info
    if not entries:
        info["state"] = "fresh"
        return info
    info["state"] = "foreign"
    suggestions = {}
    for e in entries:
        if e.is_dir() and e.name not in KNOWN:
            for pattern, target in ADOPT_HINTS:
                if re.search(pattern, e.name, re.I):
                    suggestions[e.name + "/"] = target + "/"
                    break
    info["adopt_suggestions"] = suggestions
    return info


def plan(root: Path, profile: dict) -> dict:
    ctx, dirs, files, routines = desired_state(profile, root)
    known = (read_manifest(root) or {}).get("files", {})
    actions = []
    for d in dirs:
        if not (root / d).is_dir():
            actions.append({"op": "mkdir", "path": d})
    for f in files:
        target, new_hash, entry = root / f["path"], sha(f["content"]), known.get(f["path"]) or {}
        if not target.exists():
            actions.append({"op": "create", "path": f["path"], "hash": new_hash})
            continue
        current = sha(target.read_text(encoding="utf-8", errors="replace"))
        if current == new_hash:
            actions.append({"op": "keep", "path": f["path"], "hash": new_hash, "reason": "already current"})
        elif f["user_owned"] or entry.get("pinned"):
            actions.append({"op": "keep", "path": f["path"], "hash": entry.get("hash", current),
                            "pinned": bool(entry.get("pinned")),
                            "reason": "pinned" if entry.get("pinned") else "content page; belongs to you and the routines"})
        elif entry.get("hash") == current:
            actions.append({"op": "update", "path": f["path"], "hash": new_hash,
                            "reason": "untouched since the workbench wrote it"})
        else:
            actions.append({"op": "conflict", "path": f["path"], "write": f["path"] + NEW_SUFFIX,
                            "hash": entry.get("hash"),
                            "reason": "edited since the workbench wrote it" if entry else "existed before the workbench"})
    summary = {}
    for a in actions:
        summary[a["op"]] = summary.get(a["op"], 0) + 1
    return {"root": str(root), "detected": detect(root), "role_pack": ctx["role_pack"],
            "summary": summary, "actions": actions, "routines": routines,
            "_files": {f["path"]: f["content"] for f in files}}


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp-wb")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def apply(root: Path, profile: dict) -> dict:
    result = plan(root, profile)
    contents = result.pop("_files")
    root.mkdir(parents=True, exist_ok=True)
    manifest = read_manifest(root) or {}
    if manifest.get("corrupt"):
        manifest = {}
    meta = manifest.get("files", {})
    for a in result["actions"]:
        if a["op"] == "mkdir":
            (root / a["path"]).mkdir(parents=True, exist_ok=True)
    for a in result["actions"]:
        p = a["path"]
        if a["op"] in ("create", "update"):
            atomic_write(root / p, contents[p])
            meta[p] = {"hash": a["hash"]}
        elif a["op"] == "keep":
            meta[p] = {"hash": a.get("hash") or sha(contents[p]), **({"pinned": True} if a.get("pinned") else {})}
        elif a["op"] == "conflict":
            atomic_write(root / a["write"], contents[p])
            if a.get("hash"):
                meta[p] = {"hash": a["hash"]}
    now = dt.datetime.now().isoformat(timespec="seconds")
    atomic_write(root / MANIFEST, json.dumps({
        "plugin_version": plugin_version(),
        "created": manifest.get("created", now),
        "updated": now,
        "role_pack": result["role_pack"],
        "files": dict(sorted(meta.items())),
    }, indent=2) + "\n")
    result["applied"] = True
    return result


def pin(root: Path, rel: str | None, on: bool) -> int:
    """Keep the user's version of a plugin-managed file and stop reporting it as a conflict."""
    manifest = read_manifest(root)
    if not manifest or not rel or not (root / rel).exists():
        print(json.dumps({"error": "need a workbench root and an existing --path"}), file=sys.stderr)
        return 2
    entry = manifest.setdefault("files", {}).setdefault(rel, {})
    entry["hash"] = sha((root / rel).read_text(encoding="utf-8", errors="replace"))
    if on:
        entry["pinned"] = True
        new = root / (rel + NEW_SUFFIX)
        if new.exists():
            new.unlink()
    else:
        entry.pop("pinned", None)
    atomic_write(root / MANIFEST, json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"path": rel, "pinned": on}))
    return 0


# ---------------------------------------------------------------- status

def last_signal(root: Path, routine: str) -> str | None:
    files = sorted((root / "Tracking" / "Signals").glob(f"*_{routine}.md"))
    return files[-1].name[:10] if files else None


def status(root: Path) -> dict:
    det = detect(root)
    if det["state"] != "workbench":
        return {"state": det["state"]}
    cap = root / "Tracking" / "Captures" / f"{dt.date.today().isoformat()}.md"
    captures_today = sum(1 for l in cap.read_text().splitlines() if l.startswith("- ")) if cap.exists() else 0
    return {"state": "workbench", "version": det.get("installed_version"),
            "upgrade_available": det.get("upgrade_available"),
            "last_recap": last_signal(root, "recap"), "last_dream": last_signal(root, "dream"),
            "last_weekly": last_signal(root, "weekly"), "captures_today": captures_today,
            "pending_conflicts": sorted(str(p.relative_to(root)) for p in root.rglob(f"*{NEW_SUFFIX}"))}


def days_since(iso: str | None) -> int | None:
    try:
        return (dt.date.today() - dt.date.fromisoformat(iso)).days
    except (TypeError, ValueError):
        return None


def hook_line(root: Path) -> str:
    s = status(root)
    if s["state"] != "workbench":
        return ""
    bits = [f"This folder is a Claude Workbench (v{s['version']}). Read CLAUDE.md before substantial work; "
            "from chat, write only to Tracking/Captures/<today>.md."]
    d = days_since(s["last_dream"])
    if d is not None and d > 3:
        bits.append(f"The nightly dream last ran {d} days ago; check the [Workbench] scheduled tasks.")
    if s["pending_conflicts"]:
        bits.append(f"{len(s['pending_conflicts'])} .workbench-new file(s) need review (/workbench:migrate).")
    if s["upgrade_available"]:
        bits.append("A newer workbench version is installed (/workbench:migrate).")
    return " ".join(bits)


# ---------------------------------------------------------------- cli

def find_root(start: Path) -> Path | None:
    for p in [start, *start.parents]:
        if (p / MANIFEST).exists():
            return p
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["detect", "plan", "apply", "schedules", "status", "pin", "unpin"])
    ap.add_argument("--root", help="workbench folder (default: nearest workbench above cwd, else cwd)")
    ap.add_argument("--profile", help=f"profile JSON (default: <root>/{PROFILE})")
    ap.add_argument("--path", help="pin/unpin: workbench-relative file")
    ap.add_argument("--hook", action="store_true", help="status: one line for a SessionStart hook")
    ap.add_argument("--full", action="store_true", help="plan/apply: include unchanged files and full prompts")
    args = ap.parse_args(argv)

    cwd = Path.cwd()
    root = Path(args.root).expanduser().resolve() if args.root else (find_root(cwd) or cwd)

    if args.command == "status":
        if args.hook:
            if args.root or find_root(cwd):
                line = hook_line(root)
                if line:
                    print(line)
            return 0
        print(json.dumps(status(root), indent=2))
        return 0
    if args.command == "detect":
        print(json.dumps(detect(root), indent=2))
        return 0
    if args.command in ("pin", "unpin"):
        return pin(root, args.path, args.command == "pin")

    prof_path = Path(args.profile).expanduser() if args.profile else root / PROFILE
    if not prof_path.exists():
        print(json.dumps({"error": f"profile not found: {prof_path}"}), file=sys.stderr)
        return 2
    profile = json.loads(prof_path.read_text())
    profile.setdefault("workbench_path", str(root))

    if args.command == "schedules":
        _, _, _, routines = desired_state(profile, root)
        print(json.dumps({"timezone": profile.get("timezone", "UTC"), "routines": routines},
                         indent=2, ensure_ascii=False))
        return 0
    out = apply(root, profile) if args.command == "apply" else plan(root, profile)
    out.pop("_files", None)
    if not args.full:
        out["actions"] = [a for a in out["actions"] if a["op"] != "keep"]
        out["routines"] = [{k: r[k] for k in ("id", "name", "when", "cron")} for r in out["routines"]]
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
