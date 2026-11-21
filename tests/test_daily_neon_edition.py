"""Daily (root) Gemini 4 Neon audit editions from 2026-11-21. No network."""

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import daily_state  # noqa: E402
import neon_edition  # noqa: E402

DATE = "2026-11-21"
HOUSE = "AI-generated \u00b7 may contain errors"
SCRIPT = "Welcome to the Daily State of AI.\n\nSecond paragraph with the insight.\n\nThird paragraph.\n"
PROMPT = "Here are today's AI news reports and X threads. What's the non-obvious insight others are missing?\n"
MP3 = b"ID3" + b"\x00" * 200
MP4 = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 200


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sources():
    return {
        "date": DATE,
        "urls": ["https://example.com/paper", "https://x.com/someone/status/1"],
        "stories": [{
            "index": 1, "title": "A story", "outlets": ["Example", "X"],
            "urls": ["https://example.com/paper", "https://x.com/someone/status/1"],
            "verification_status": "author_reported",
        }],
    }


def mini_run(**over):
    run = {
        "date": DATE, "status": "ok", "pipeline": "neon", "model": "google/gemini-4-neon",
        "reasoning_effort": "medium", "system_prompt": None, "editor": None, "qa": None,
        "edits_after_generation": "none (published as produced)", "fallback": "none (fail closed)",
        "prompts": {"episode": PROMPT}, "model_attempts": [{"model": "google/gemini-4-neon", "outcome": "ok"}],
        "words": 9, "duration_seconds": 300.0, "bundle_sha256": "a" * 64,
        "script_sha256": sha(SCRIPT.encode()), "material": {"source": "box_material", "sha256": "b" * 64, "chars": 10},
        "audit": {"gate": False, "status": "runs after publish"},
    }
    run.update(over)
    return run


class Repo:
    """A throwaway repo root with content/daily-state and a Mini mirror dir."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "content" / "daily-state").mkdir(parents=True)
        self.mirror = self.root / "mirror"
        self.mirror.mkdir()
        (self.mirror / "script.txt").write_text(SCRIPT, encoding="utf-8")
        (self.mirror / "sources.json").write_text(json.dumps(sources(), indent=2), encoding="utf-8")
        (self.mirror / "episode.mp3").write_bytes(MP3)
        (self.mirror / "run.json").write_text(json.dumps(mini_run()), encoding="utf-8")
        self.short = self.root / "short.mp4"
        self.short.write_bytes(MP4)

    def edition_dir(self):
        return self.root / "content" / "daily-state" / DATE

    def build(self, short=True, run=None):
        if run is not None:
            (self.mirror / "run.json").write_text(json.dumps(run), encoding="utf-8")
        argv = ["build", "--date", DATE, "--episode-dir", str(self.mirror)]
        if short:
            argv += ["--short", str(self.short)]
        with mock.patch.object(neon_edition, "REPO", str(self.root)):
            return neon_edition.main(argv)

    def load(self):
        return daily_state.load_edition(str(self.root), DATE)

    def close(self):
        self.tmp.cleanup()


def write_audit(repo, script_sha=None, status="FAIL", takeaways=False):
    kit = repo.root / "kit"
    checks = kit / "checks" / DATE
    checks.mkdir(parents=True)
    (kit / "lib").mkdir()
    (kit / "lib" / "auditlib.py").write_text("# helpers\n")
    (kit / "run_audit.py").write_text("# runner\n")
    (checks / "e01-claim.py").write_text("CLAIM = {}\n")
    out = repo.root / "audit-out"
    out.mkdir()
    audit = {
        "meta": {
            "date": DATE,
            "artifacts": {"episode": {"path": "script.txt", "sha256": script_sha or sha(SCRIPT.encode())}},
            "summary": {"episode": {"PASS": 0, "FAIL": 1, "NEEDS-HUMAN": 0, "ERROR": 0}},
        },
        "results": [{
            "id": "e01-claim", "artifact": "episode", "quote": "the insight", "status": status,
            "source_quote": "a source line", "check_file": f"checks/{DATE}/e01-claim.py", "note": "",
        }],
    }
    if status != "FAIL":
        audit["meta"]["summary"]["episode"] = {"PASS": 1, "FAIL": 0, "NEEDS-HUMAN": 0, "ERROR": 0}
    if takeaways:
        (checks / "t01-claim.py").write_text("CLAIM = {}\n")
        (checks / "tc01-citation.py").write_text("CLAIM = {}\n")
        audit["results"] += [
            {"id": "t01-claim", "artifact": "takeaways", "quote": "a takeaway claim", "status": "PASS",
             "source_quote": "a source line", "check_file": f"checks/{DATE}/t01-claim.py", "note": ""},
            {"id": "tc01-citation", "artifact": "takeaways", "quote": None, "status": "FAIL",
             "source_quote": None, "check_file": f"checks/{DATE}/tc01-citation.py",
             "note": "Takeaway 1 cites https://elsewhere.example/x, which is not in the episode sources.json."},
        ]
        audit["meta"]["summary"]["takeaways"] = {"PASS": 1, "FAIL": 1, "NEEDS-HUMAN": 0, "ERROR": 0}
    (out / "audit.json").write_text(json.dumps(audit), encoding="utf-8")
    return kit, out


class DailyNeonEditionTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.close()

    def test_build_renders_raw_page_with_pending_audit(self):
        self.assertEqual(self.repo.build(), 0)
        loaded = self.repo.load()
        self.assertTrue(loaded["root_audit"])
        page = loaded["html"]
        self.assertIn(f"<h1>Daily State of AI - {DATE}</h1>", page)
        self.assertEqual(page.count(HOUSE), 1)
        self.assertIn(' · <a href="audit/">Audit</a></p>', page)
        self.assertIn(f'<audio controls src="/content/daily-state/{DATE}/episode.mp3"></audio>', page)
        self.assertIn(f'<a href="/content/daily-state/{DATE}/short.mp4">Short</a>', page)
        self.assertNotIn("open.spotify.com", page)
        self.assertIn(f'<link rel="canonical" href="https://www.signalandnoise.email/daily-state/{DATE}/">', page)
        self.assertIn("Welcome to the Daily State of AI.", page)
        self.assertIn(daily_state.AUDIT_PENDING_MARKER, loaded["audit_html"])
        self.assertEqual(sorted(loaded["files"]), [f"daily-state/{DATE}/audit/index.html", f"daily-state/{DATE}/index.html"])
        edition = json.loads((self.repo.edition_dir() / "edition.json").read_text())
        self.assertEqual(edition["mode"], "audit")
        self.assertIsNone(edition["variant"])
        self.assertEqual(edition["audit"], {"gate": False, "attach": "after_publish"})
        self.assertEqual((self.repo.edition_dir() / "script.txt").read_text(), SCRIPT)

    def test_build_without_short_has_no_short_link(self):
        self.assertEqual(self.repo.build(short=False), 0)
        page = self.repo.load()["html"]
        self.assertNotIn(">Short</a>", page)

    def test_build_refuses_failed_or_non_neon_runs(self):
        self.assertEqual(self.repo.build(run=mini_run(status="failed")), 1)
        self.assertFalse(self.repo.edition_dir().exists())
        self.assertEqual(self.repo.build(run=mini_run(pipeline="editor")), 1)
        self.assertEqual(self.repo.build(run=mini_run(script_sha256="c" * 64)), 1)

    def test_build_refuses_an_existing_edition(self):
        self.assertEqual(self.repo.build(), 0)
        self.assertEqual(self.repo.build(), 1)

    def test_edited_script_holds(self):
        self.repo.build()
        (self.repo.edition_dir() / "script.txt").write_text(SCRIPT + "edit\n")
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_video_url_without_short_holds(self):
        self.repo.build()
        (self.repo.edition_dir() / "short.mp4").unlink()
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_editor_receipt_or_gate_holds(self):
        self.repo.build()
        path = self.repo.edition_dir() / "edition.json"
        edition = json.loads(path.read_text())
        edition["audit"] = {"gate": True, "attach": "after_publish"}
        path.write_text(json.dumps(edition))
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_unknown_file_holds(self):
        self.repo.build()
        (self.repo.edition_dir() / "qa.json").write_text("{}")
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_attach_audit_renders_counts(self):
        self.repo.build()
        kit, out = write_audit(self.repo)
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            rc = neon_edition.main(["attach-audit", "--date", DATE, "--audit-out", str(out), "--kit", str(kit)])
        self.assertEqual(rc, 0)
        loaded = self.repo.load()
        self.assertNotIn(daily_state.AUDIT_PENDING_MARKER, loaded["audit_html"])
        self.assertIn("Episode 0 PASS / 1 FAIL / 0 NEEDS-HUMAN", loaded["audit_html"])
        self.assertIn(f"content/daily-state/{DATE}/audit/checks/{DATE}/e01-claim.py", loaded["audit_html"])
        # The edition page itself does not change when the audit lands.
        self.assertIn(' · <a href="audit/">Audit</a></p>', loaded["html"])

    def test_attach_audit_shows_takeaway_checks(self):
        self.repo.build()
        kit, out = write_audit(self.repo, takeaways=True)
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            rc = neon_edition.main(["attach-audit", "--date", DATE, "--audit-out", str(out), "--kit", str(kit)])
        self.assertEqual(rc, 0)
        html_text = self.repo.load()["audit_html"]
        self.assertIn("Takeaways 1 PASS / 1 FAIL / 0 NEEDS-HUMAN", html_text)
        self.assertIn("<h2>Takeaways</h2>", html_text)
        self.assertIn("not in the episode sources.json", html_text)

    def test_audit_without_takeaways_has_no_takeaways_row(self):
        self.repo.build()
        kit, out = write_audit(self.repo)
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            neon_edition.main(["attach-audit", "--date", DATE, "--audit-out", str(out), "--kit", str(kit)])
        self.assertNotIn("Takeaways", self.repo.load()["audit_html"])

    def test_attach_audit_for_another_script_holds(self):
        self.repo.build()
        kit, out = write_audit(self.repo, script_sha="d" * 64)
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            rc = neon_edition.main(["attach-audit", "--date", DATE, "--audit-out", str(out), "--kit", str(kit)])
        self.assertEqual(rc, 1)
        self.assertFalse((self.repo.edition_dir() / "audit").exists())

    def test_only_the_pending_audit_page_may_be_replaced(self):
        self.repo.build()
        repo = str(self.repo.root)
        first = daily_state.render_output([self.repo.load()])
        daily_state.commit_output(repo, first, write=True, allow_correction=False)
        kit, out = write_audit(self.repo)
        with mock.patch.object(neon_edition, "REPO", repo):
            neon_edition.main(["attach-audit", "--date", DATE, "--audit-out", str(out), "--kit", str(kit)])
        second = daily_state.render_output([self.repo.load()])
        result = daily_state.commit_output(repo, second, write=True, allow_correction=False)
        self.assertEqual(result["wrote"], 1)
        # A finished audit page is now frozen like the edition page.
        changed = dict(second)
        changed[f"daily-state/{DATE}/audit/index.html"] += "<!-- changed -->"
        with self.assertRaises(daily_state.Hold):
            daily_state.commit_output(repo, changed, write=True, allow_correction=False)
        edited = dict(second)
        edited[f"daily-state/{DATE}/index.html"] += "<!-- changed -->"
        with self.assertRaises(daily_state.Hold):
            daily_state.commit_output(repo, edited, write=True, allow_correction=False)


if __name__ == "__main__":
    unittest.main()
