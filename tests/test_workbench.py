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
                    "Tracking/Signals/README.md", "Archive/CLAUDE.md", ".workbench/manifest.json",
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
        self.apply(dict(PROFILE, meetings_source="Granola"))
        self.assertIn("Granola", (self.root / "Meetings/CLAUDE.md").read_text())
        self.assertIn("`Meetings/`", (self.root / "CLAUDE.md").read_text())


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


class Hook(Base):
    def test_hook_is_silent_outside_a_workbench_and_speaks_inside(self):
        self.root.mkdir()
        self.assertEqual(wb.hook_line(self.root), "")
        self.apply()
        self.assertIn("Claude Workbench", wb.hook_line(self.root))


if __name__ == "__main__":
    unittest.main()
