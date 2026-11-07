"""Tests for scripts/workbench.py. Run: python3 -m unittest discover -s tests"""
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import workbench as wb  # noqa: E402

PROFILE = {
    "name": "Jane Rivera",
    "preferred_name": "Jane",
    "role": "Senior Account Executive",
    "team": "Mid-Market East",
    "manager": "Pat Lee",
    "company": "Acme Data",
    "company_description": "B2B data platform for mid-market retailers.",
    "location": "Austin, TX",
    "timezone": "America/Chicago",
    "work_hours": {"start": "08:30", "end": "17:30", "days": "Mon-Fri"},
    "tools": ["Gmail", "Google Calendar", "Slack", "Salesforce"],
    "connections": [{"tool": "Gmail", "status": "connected", "via": "Gmail connector"},
                    {"tool": "Salesforce", "status": "missing"}],
    "goals": ["Hit 120% of Q4 quota"],
}


def run(*args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = wb.main(list(args))
    return code, buf.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "Workbench"
        self.profile_path = Path(self.tmp.name) / "profile.json"
        self.profile_path.write_text(json.dumps(PROFILE))

    def tearDown(self):
        self.tmp.cleanup()

    def apply(self, profile=None):
        if profile is not None:
            self.profile_path.write_text(json.dumps(profile))
        code, out = run("apply", "--root", str(self.root), "--profile", str(self.profile_path))
        self.assertEqual(code, 0)
        return json.loads(out)


class FreshBuild(Base):
    def test_builds_the_vault_layout(self):
        self.apply()
        for rel in ["CLAUDE.md", "README.md", "Context/me.md", "Context/voice.md", "Projects/INDEX.md",
                    "People/NAME_VARIANTS.md", "People/Jane Rivera.md", "Organizations/Acme Data.md",
                    "Resources/GLOSSARY.md", "Resources/Tools/Salesforce.md", "Tracking/GOALS.md",
                    "Tracking/DREAM_LOG.md", "Tracking/FRICTION_LOG.md", "Tracking/Captures/README.md",
                    "Tracking/Signals/README.md", "Tracking/Drafts/README.md", "Tracking/IMPROVEMENTS.md",
                    ".obsidian/app.json", ".obsidian/graph.json", "Archive/CLAUDE.md", ".workbench/manifest.json",
                    ".workbench/profile.json", ".workbench/schedules.json",
                    ".workbench/PROJECT_INSTRUCTIONS.md", ".workbench/routines/nightly-dream.md"]:
            self.assertTrue((self.root / rel).exists(), rel)
        for folder in ["Context", "Daily", "Projects", "People", "Organizations", "Resources", "Tracking", "Archive"]:
            self.assertTrue((self.root / folder / "CLAUDE.md").exists(), folder)
        self.assertFalse((self.root / "Meetings").exists(), "Meetings only when a recorder export exists")

    def test_no_unrendered_placeholders(self):
        self.apply()
        for p in self.root.rglob("*.md"):
            leftovers = set(re.findall(r"\{\{([a-z_]+)\}\}", p.read_text()))
            self.assertFalse(leftovers, f"{p.relative_to(self.root)}: {leftovers}")

    def test_profile_details_land_in_pages(self):
        self.apply()
        claude = (self.root / "CLAUDE.md").read_text()
        self.assertIn("Senior Account Executive at Acme Data, Mid-Market East team", claude)
        me = (self.root / "Context/me.md").read_text()
        self.assertIn("Reports to [[Pat Lee]]", me)
        self.assertIn("| [[Gmail]] | yes | Gmail connector |", me)
        self.assertIn("| [[Salesforce]] | no |", me)
        self.assertIn("`sales`", (self.root / "People/CLAUDE.md").read_text())

    def test_meetings_folder_when_recorder_export(self):
        instructions = self.root / ".workbench/PROJECT_INSTRUCTIONS.md"
        self.apply()
        self.assertNotIn("## Transcript", instructions.read_text())
        self.apply(dict(PROFILE, meetings_source="Granola"))
        self.assertIn("Granola", (self.root / "Meetings/CLAUDE.md").read_text())
        self.assertIn("`Meetings/`", (self.root / "CLAUDE.md").read_text())
        self.assertIn("## Transcript", instructions.read_text())

    def test_delivery_channel_lands_in_the_contract(self):
        self.apply(dict(PROFILE, delivery={"channel": "slack", "target": "DM to myself"}))
        self.assertIn("a Slack message (DM to myself)", (self.root / "CLAUDE.md").read_text())

    def test_obsidian_config_optional_and_never_overwritten(self):
        self.apply(dict(PROFILE, obsidian=False))
        self.assertFalse((self.root / ".obsidian").exists())
        (self.root / ".obsidian").mkdir()
        (self.root / ".obsidian/app.json").write_text("{}")
        self.apply()
        self.assertEqual((self.root / ".obsidian/app.json").read_text(), "{}")


class Relationships(Base):
    def test_starter_edges_parse_and_are_two_way(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        self.apply()
        pages = {}
        for p in self.root.rglob("*.md"):
            text = p.read_text()
            if text.startswith("---\n") and "/Archive/" not in str(p):
                fm = yaml.safe_load(text.split("---\n")[1])
                pages[p.stem] = fm
        link = lambda v: v.strip("[]") if isinstance(v, str) else v
        jane, pat, acme = pages["Jane Rivera"], pages["Pat Lee"], pages["Acme Data"]
        self.assertEqual(link(jane["org"]), "Acme Data")
        self.assertIn("[[Jane Rivera]]", acme["people"])
        self.assertIn("[[Pat Lee]]", acme["people"])
        self.assertEqual(link(jane["reports_to"]), "Pat Lee")
        self.assertIn("[[Jane Rivera]]", pat["direct_reports"])

    def test_no_manager_means_no_dangling_edge(self):
        p = dict(PROFILE)
        p.pop("manager")
        self.apply(p)
        self.assertIn('reports_to: ""', (self.root / "People/Jane Rivera.md").read_text())
        self.assertNotIn("Pat Lee", (self.root / "Organizations/Acme Data.md").read_text())


class Upgrades(Base):
    def test_reapply_is_a_noop(self):
        self.apply()
        out = self.apply()
        self.assertEqual(out["actions"], [], out["actions"])

    def test_edited_managed_file_is_never_overwritten(self):
        self.apply()
        f = self.root / "Projects/CLAUDE.md"
        f.write_text(f.read_text() + "\n## Standing exception\nmine\n")
        before = f.read_text()
        profile = dict(PROFILE, role="Account Executive, Enterprise")
        out = self.apply(profile)
        ops = {a["path"]: a["op"] for a in out["actions"]}
        self.assertEqual(ops.get("Projects/CLAUDE.md"), "conflict")
        self.assertEqual(f.read_text(), before)
        self.assertTrue((self.root / "Projects/CLAUDE.md.workbench-new").exists())

    def test_untouched_managed_file_updates_in_place(self):
        self.apply()
        out = self.apply(dict(PROFILE, role="Enterprise Account Executive"))
        ops = {a["path"]: a["op"] for a in out["actions"]}
        self.assertEqual(ops.get("CLAUDE.md"), "update")
        self.assertIn("Enterprise Account Executive", (self.root / "CLAUDE.md").read_text())

    def test_content_pages_belong_to_the_user(self):
        self.apply()
        goals = self.root / "Tracking/GOALS.md"
        goals.write_text("my goals\n")
        self.apply(dict(PROFILE, goals=["Something else"]))
        self.assertEqual(goals.read_text(), "my goals\n")

    def test_pin_settles_a_conflict(self):
        self.apply()
        f = self.root / "Daily/CLAUDE.md"
        f.write_text("custom\n")
        self.apply(dict(PROFILE, role="AE"))
        self.assertEqual(run("pin", "--root", str(self.root), "--path", "Daily/CLAUDE.md")[0], 0)
        self.assertFalse((self.root / "Daily/CLAUDE.md.workbench-new").exists())
        out = self.apply(dict(PROFILE, role="AE II"))
        self.assertNotIn("Daily/CLAUDE.md", [a["path"] for a in out["actions"]])
        self.assertEqual(f.read_text(), "custom\n")


class Detection(Base):
    def test_states(self):
        self.assertEqual(wb.detect(self.root)["state"], "fresh")
        self.root.mkdir()
        (self.root / ".obsidian").mkdir()
        self.assertEqual(wb.detect(self.root)["state"], "fresh")
        (self.root / "Journal").mkdir()
        (self.root / "Clients").mkdir()
        (self.root / "CLAUDE.md").write_text("# my own rules\n")
        d = wb.detect(self.root)
        self.assertEqual(d["state"], "foreign")
        self.assertEqual(d["adopt_suggestions"], {"Journal/": "Daily/", "Clients/": "Organizations/"})
        out = self.apply()
        ops = {a["path"]: a["op"] for a in out["actions"]}
        self.assertEqual(ops["CLAUDE.md"], "conflict")
        self.assertEqual((self.root / "CLAUDE.md").read_text(), "# my own rules\n")
        self.assertEqual(wb.detect(self.root)["state"], "workbench")


class Roles(unittest.TestCase):
    def test_role_matching_prefers_the_specific_term(self):
        _, roles = wb.load_blueprints()
        cases = {
            "Account Manager": "sales",
            "VP of Customer Success": "customer-success",
            "Senior Software Engineer": "engineering",
            "Head of People": "people",
            "Chief of Staff": "operations",
            "Founder & CEO": "leadership",
            "Barista": "general",
        }
        for role, pack in cases.items():
            self.assertEqual(wb.resolve_role_pack({"role": role}, roles), pack, role)
        self.assertEqual(wb.resolve_role_pack({"role": "Barista", "role_pack": "marketing"}, roles), "marketing")


class Routines(Base):
    def routines(self, profile):
        ctx, base, _ = wb.build_context(profile, self.root)
        return {r["id"]: r for r in wb.desired_routines(profile, ctx, base)}

    def test_default_times_follow_working_hours(self):
        r = self.routines(PROFILE)
        self.assertEqual(r["daily-briefing"]["cron"], "0 8 * * 1-5")
        self.assertEqual(r["eod-recap"]["cron"], "0 18 * * 1-5")
        self.assertEqual(r["nightly-dream"]["cron"], "0 22 * * 1-5")
        self.assertEqual(r["weekly"]["cron"], "0 7 * * 1")
        self.assertEqual(r["calendar-sync"]["cron"], "30 7,11,17 * * 1-5")
        self.assertTrue(all(x["name"].startswith("[Workbench] ") for x in r.values()))

    def test_workweek_and_toggles(self):
        p = dict(PROFILE, work_hours={"start": "09:00", "end": "18:00", "days": "Sun-Thu"},
                 tools=["Slack"], routines={"midday-update": False})
        r = self.routines(p)
        self.assertNotIn("calendar-sync", r, "no calendar tool, no calendar sync by default")
        self.assertNotIn("midday-update", r)
        self.assertEqual(r["daily-briefing"]["cron"], "30 8 * * 0-4")
        self.assertEqual(r["weekly"]["cron"], "30 7 * * 0")

    def test_custom_time_and_prompt_points_at_skill_and_fallback(self):
        r = self.routines(dict(PROFILE, routine_times={"nightly-dream": "23:15"}))
        self.assertEqual(r["nightly-dream"]["cron"], "15 23 * * 1-5")
        self.assertIn("workbench:nightly-dream", r["nightly-dream"]["prompt"])
        self.assertIn(".workbench/routines/nightly-dream.md", r["nightly-dream"]["prompt"])

    def test_cron_days(self):
        self.assertEqual(wb.cron_days(wb.parse_workdays("Mon-Fri")), "1-5")
        self.assertEqual(wb.cron_days(wb.parse_workdays(["Mon", "Wed", "Fri"])), "1,3,5")
        self.assertEqual(wb.cron_days(wb.parse_workdays("Fri-Mon")), "0,1,5,6")


class NewVaultFiles(Base):
    def test_fresh_vault_has_the_v020_files(self):
        self.apply()
        commitments = (self.root / "Tracking/COMMITMENTS.md").read_text()
        self.assertIn("# Commitments", commitments)
        self.assertIn("| Commitment | Who owes | Due | Source | State | Last evidence |", commitments)
        self.assertNotRegex(commitments.split("|---|---|---|---|---|---|")[1], r"\|",
                            "the register ships with no rows")
        ledger = (self.root / "Tracking/Signals/RUN_LEDGER.md").read_text()
        self.assertIn("# Run ledger", ledger)
        self.assertIn("- YYYY-MM-DD HH:MM | <routine> | <ok|partial|failed> | wrote:", ledger)
        self.assertTrue(ledger.rstrip().endswith("## Runs"))
        surfacing = (self.root / "Context/surfacing.md").read_text()
        headings = re.findall(r"^## (.+)$", surfacing, re.M)
        self.assertEqual(headings, ["Always surface", "Never surface", "Quiet hours", "Format preferences"])

    def test_repo_vault_gets_a_gitignore_and_local_does_not(self):
        self.apply(dict(PROFILE, vault_home="local"))
        self.assertFalse((self.root / ".gitignore").exists())
        self.assertNotIn("GIT\n", (self.root / ".workbench/PROJECT_INSTRUCTIONS.md").read_text())
        self.apply(dict(PROFILE, vault_home="repo"))
        ignore = (self.root / ".gitignore").read_text().splitlines()
        for entry in [".obsidian/workspace.json", ".obsidian/workspace-mobile.json", ".DS_Store", "Thumbs.db"]:
            self.assertIn(entry, ignore)
        self.assertTrue(any(line.startswith(".workbench/") for line in ignore))
        self.assertIn("GIT\n", (self.root / ".workbench/PROJECT_INSTRUCTIONS.md").read_text())

    def test_instruction_blocks_follow_the_profile(self):
        self.apply(dict(PROFILE, surface="cowork"))
        text = (self.root / ".workbench/PROJECT_INSTRUCTIONS.md").read_text()
        self.assertIn("WHERE THIS WORKS", text)
        self.assertNotIn("<!-- workbench:", text)
        self.apply(dict(PROFILE, surface="code"))
        self.assertNotIn("WHERE THIS WORKS", (self.root / ".workbench/PROJECT_INSTRUCTIONS.md").read_text())

    def test_migrate_adds_missing_files_and_never_overwrites_a_users_own(self):
        self.apply()
        new = ["Tracking/COMMITMENTS.md", "Tracking/Signals/RUN_LEDGER.md", "Context/surfacing.md"]
        # Make this look like a 0.1.0 vault: the files don't exist and the manifest never saw them.
        manifest_path = self.root / ".workbench/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        for rel in new:
            (self.root / rel).unlink()
            manifest["files"].pop(rel)
        manifest["plugin_version"] = "0.1.0"
        manifest_path.write_text(json.dumps(manifest))
        mine = self.root / "Tracking/COMMITMENTS.md"
        mine.write_text("my own commitments list\n")
        out = self.apply()
        ops = {a["path"]: a["op"] for a in out["actions"]}
        self.assertEqual(ops["Tracking/Signals/RUN_LEDGER.md"], "create")
        self.assertEqual(ops["Context/surfacing.md"], "create")
        self.assertEqual(ops["Tracking/COMMITMENTS.md"], "conflict")
        self.assertEqual(mine.read_text(), "my own commitments list\n")
        self.assertIn("| Commitment |", (self.root / "Tracking/COMMITMENTS.md.workbench-new").read_text())
        for rel in new:
            self.assertTrue((self.root / rel).exists(), rel)

    def test_run_ledger_feeds_status(self):
        self.apply()
        ledger = self.root / "Tracking/Signals/RUN_LEDGER.md"
        ledger.write_text(ledger.read_text() + "- 2026-11-05 22:10 | nightly-dream | ok | wrote: DREAM_LOG.md | gaps: none\n"
                          "- 2026-11-06 22:10 | nightly-dream | failed | wrote: nothing | gaps: recap missing\n")
        self.assertEqual(wb.status(self.root)["last_dream"], "2026-11-05")


class PackageHygiene(unittest.TestCase):
    """Cowork refuses a plugin with Code-only components. This keeps the package installable there."""

    ROOT = Path(__file__).resolve().parent.parent

    def walk(self):
        for p in self.ROOT.rglob("*"):
            if ".git" not in p.relative_to(self.ROOT).parts:
                yield p

    def test_no_cowork_rejected_components(self):
        for p in self.walk():
            rel = p.relative_to(self.ROOT)
            if p.is_dir():
                self.assertNotIn(p.name, {"bin", "output-styles", "themes"}, f"Code-only directory: {rel}")
            self.assertNotEqual(p.name, ".lsp.json", f"LSP server config: {rel}")
        for manifest in (self.ROOT / ".claude-plugin").glob("*.json"):
            text = manifest.read_text()
            self.assertNotIn('"lspServers"', text, manifest.name)
            for plugin in [json.loads(text)] + json.loads(text).get("plugins", []):
                for key in ("lspServers", "outputStyles", "themes", "settings"):
                    self.assertNotIn(key, plugin, f"{manifest.name} declares {key}")

    def test_both_manifests_carry_the_same_version(self):
        plugin = json.loads((self.ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((self.ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual({p["version"] for p in market["plugins"]}, {plugin["version"]})


class Hook(Base):
    def test_hook_is_silent_outside_a_workbench_and_speaks_inside(self):
        self.root.mkdir()
        self.assertEqual(wb.hook_line(self.root), "")
        self.apply()
        self.assertIn("Claude Workbench", wb.hook_line(self.root))


if __name__ == "__main__":
    unittest.main()
