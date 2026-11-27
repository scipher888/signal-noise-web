"""Ethical floor record on the daily audit page (synthia-workspace ethical_floor.py, 2026-11-26). No network."""

import json
import shutil
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))

import daily_state  # noqa: E402
import neon_edition  # noqa: E402
from test_daily_neon_edition import DATE, SCRIPT, Repo, mini_run, sha, write_audit  # noqa: E402

ORIGINAL = SCRIPT.replace("the insight", "the invented insight")
BEFORE = "Viral posts were warning that labs had secretly cracked RSA."
AFTER = "Posts speculated that a rumored method could crack RSA."


def floor(status="clean", script_sha=None):
    record = {
        "version": 1, "checked": True, "triggered": False, "status": status,
        "fail_rows_reviewed": 1, "violations": [], "fix": {"status": "not_needed"},
        "audit_counts": {"initial": {"episode": {"PASS": 0, "FAIL": 1, "NEEDS-HUMAN": 0, "ERROR": 0}},
                         "final": {"episode": {"PASS": 0, "FAIL": 1, "NEEDS-HUMAN": 0, "ERROR": 0}}},
    }
    if status.startswith("fixed") or status.startswith("edit"):
        record.update({
            "triggered": True,
            "violations": [{"id": "e09-secret-crack", "category": "misattribution", "artifact": "episode",
                            "quote": BEFORE, "why": "The posts were conditional.", "source_quote": "This would crack RSA."}],
            "pre_fix": {"script_sha256": sha(ORIGINAL.encode())},
            "post_fix": {"script_sha256": script_sha or sha(SCRIPT.encode())},
            "fix": {"status": "applied" if status.startswith("fixed") else status,
                    "edits": [{"artifact": "episode", "before": BEFORE, "after": AFTER}]
                    if status.startswith("fixed") else []},
        })
        record["audit_counts"]["initial"]["episode"] = {"PASS": 0, "FAIL": 3, "NEEDS-HUMAN": 0, "ERROR": 0}
    return record


class EthicalFloorAuditTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.close()

    def attach(self, record, run=None, upstream=False):
        self.repo.build(run=run)
        kit, out = write_audit(self.repo)
        audit = json.loads((out / "audit.json").read_text())
        if record is not None:
            audit["ethical_floor"] = record
        (out / "audit.json").write_text(json.dumps(audit))
        argv = ["attach-audit", "--date", DATE, "--audit-out", str(out)]
        if upstream:  # the Mini layout: DAY/audit/ with the kit inside
            shutil.move(str(kit), str(out / "kit"))
        else:
            argv += ["--kit", str(kit)]
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            return neon_edition.main(argv)

    def test_clean_floor_renders_a_short_note(self):
        self.assertEqual(self.attach(floor("clean"), upstream=True), 0)
        loaded = self.repo.load()
        page = loaded["audit_html"]
        self.assertIn("<h2>Ethical floor</h2>", page)
        self.assertIn("None fell below it, so nothing was edited.", page)
        self.assertNotIn("Original script SHA-256", page)
        self.assertIn("published as produced.", loaded["html"])

    def test_fixed_floor_shows_violation_edit_and_prefix_hash(self):
        run = mini_run(edits_after_generation="ethical floor fix: 1 surgical edit(s) before TTS",
                       ethical_floor={"status": "fixed"}, audit={"gate": False, "status": "ran before TTS",
                                                                 "file": "audit/audit.json"})
        self.assertEqual(self.attach(floor("fixed"), run=run), 0)
        loaded = self.repo.load()
        page = loaded["audit_html"]
        self.assertIn("Wrong person or company", page)
        self.assertIn("pinned on the wrong person or company, a fabricated event, "
                      "or exposed non-public personal information", page)
        self.assertNotIn("invented or fused number", page)
        self.assertIn("One surgical edit pass corrected only those items", page)
        self.assertIn(sha(ORIGINAL.encode()), page)
        self.assertIn("<del>Viral posts were warning that labs had secretly cracked RSA.</del>", page)
        self.assertIn("<ins>Posts speculated that a rumored method could crack RSA.</ins>", page)
        self.assertIn("First audit: episode 0 PASS / 3 FAIL", page)
        self.assertIn("Refreshed audit: episode 0 PASS / 1 FAIL", page)
        self.assertIn("ethical floor check made one surgical correction pass", loaded["html"])
        self.assertNotIn("published as produced.", loaded["html"])
        neon_run = json.loads((self.repo.edition_dir() / "neon_run.json").read_text())
        self.assertEqual(neon_run["audit"]["status"], "ran before TTS (ethical floor check)")
        self.assertEqual(neon_run["ethical_floor"], {"status": "fixed"})

    def test_unfixed_violation_says_published_as_written(self):
        self.assertEqual(self.attach(floor("edit_failed")), 0)
        page = self.repo.load()["audit_html"]
        self.assertIn("The fix did not apply (edit_failed)", page)
        self.assertNotIn("<h3>Edits</h3>", page)

    def test_fix_for_another_script_holds(self):
        self.assertEqual(self.attach(floor("fixed", script_sha="e" * 64)), 1)

    def test_run_naming_a_fix_without_a_floor_record_holds(self):
        run = mini_run(edits_after_generation="ethical floor fix: 1 surgical edit(s) before TTS")
        self.assertEqual(self.attach(None, run=run), 1)

    def test_other_edits_still_hold(self):
        with self.assertRaises(daily_state.Hold):
            daily_state.validate_neon_run(mini_run(edits_after_generation="editor rewrote it"), DATE, None)

    def test_unknown_category_holds(self):
        bad = floor("fixed")
        bad["violations"][0]["category"] = "framing"
        self.assertEqual(self.attach(bad), 1)

    def test_audit_without_a_floor_record_is_unchanged(self):
        self.assertEqual(self.attach(None), 0)
        self.assertNotIn("Ethical floor", self.repo.load()["audit_html"])


if __name__ == "__main__":
    unittest.main()
