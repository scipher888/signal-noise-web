"""Opt-in editor mode. The live publisher stays the default. No network."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import daily_state  # noqa: E402


DATE = "2026-11-08"
EPISODE_ID = "4BrflfgytoeU5dAro96ig7"
EPISODE_URL = "https://open.spotify.com/episode/" + EPISODE_ID
OPENAI = "https://openai.com/index/step-toward-defining-the-standard-model"
HOUSE = "AI-generated \u00b7 may contain errors"
OVERRULED = "OVERRULED-SENTINEL-do-not-publish"
RUN_SHA = "b1bb60187258f6687b278f02adda1e86b20c2309e9108f5533abd50471806fd5"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def editor_receipt(**overrides):
    receipt = {
        "model": "meta/muse-ember",
        "accepted": 1,
        "overruled": 2,
        "partially": 0,
        "completed": True,
        "outstanding": 0,
    }
    receipt.update(overrides)
    return receipt


def empty_notes():
    return {
        "date": DATE,
        "outstanding": [],
        "generated_by": {"model": "meta/muse-ember"},
    }


def sample_notes():
    return {
        "date": DATE,
        "outstanding": [
            {
                "artifact": "written",
                "summary": "The written edition still names a figure the source does not.",
                "reason": "The editor kept the sentence and marked it unresolved.",
                "status": "accepted_unresolved",
            },
            {
                "artifact": "short",
                "summary": "The short drops the company-reported caveat.",
                "reason": "One clause was tightened and the rest was left.",
                "status": "accepted_partial",
            },
            {
                "artifact": "episode",
                "summary": "The episode leaves one claim open.",
                "reason": "The line stayed in the read.",
                "status": "accepted_unresolved",
            },
        ],
        "generated_by": {"model": "meta/muse-ember"},
    }


def advisory_gates(findings=2):
    return [
        {
            "name": name,
            "ok": True,
            "advisory": True,
            "findings": findings,
            "detail": "advisory",
        }
        for name in daily_state.NAMED_GATES
    ]


def editor_run(**overrides):
    gate = advisory_gates()
    attempt = {
        "accepted": True,
        "advisory": True,
        "semantic_qa": "pass",
        "gate": [dict(item) for item in gate],
        "model": "hidden-model",
    }
    run = {
        "date": DATE,
        "status": "ok",
        "pipeline": "editor",
        "semantic_qa": "pass",
        "sources": "ok",
        "source_count": 4,
        "gate": gate,
        "attempts": [attempt],
        "hard_stops": [],
        "editor": editor_receipt(),
        "episode_url": EPISODE_URL,
        "model": "should-not-leak",
        "telegram": "sent",
    }
    run.update(overrides)
    return run


def constant_opener(status, body=b""):
    seen = []

    def opener(method, url):
        seen.append((method, url))
        return status, body

    return opener, seen


def queued_opener(responses):
    seen = []

    def opener(method, url):
        seen.append(method)
        status, body = responses.pop(0)
        return status, body

    return opener, seen


class EditorModeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "index.html").write_text(
            """<!doctype html><html><body>
<main>
<section class="latest"><h2>Essay</h2></section>
<section class="latest daily-latest"></section>
<section class="recent"><h2>Recent</h2></section>
</main>
</body></html>
""",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def copy_edition(self):
        source = ROOT / "content" / "daily-state" / DATE
        dest = self.root / "content" / "daily-state" / DATE
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.mkdir()
        for name in daily_state.CONTENT_FILES:
            shutil.copyfile(source / name, dest / name)
        return dest

    def seal_editor(self, directory, notes, receipt=None, hard_stops=None):
        directory = Path(directory)
        dump_json(directory / "editor_notes.json", notes)
        edition = load_json(directory / "edition.json")
        edition["pipeline"] = "editor"
        edition["editor"] = receipt or editor_receipt(outstanding=len(notes["outstanding"]))
        edition["hard_stops"] = [] if hard_stops is None else hard_stops
        edition["hashes"]["editor_notes_sha256"] = daily_state.sha256_bytes(
            (directory / "editor_notes.json").read_bytes()
        )
        dump_json(directory / "edition.json", edition)
        return directory

    def write_script(self, directory, text):
        path = Path(directory) / "script.txt"
        path.write_text(text, encoding="utf-8")
        edition = load_json(directory / "edition.json")
        edition["hashes"]["script_sha256"] = daily_state.sha256_bytes(path.read_bytes())
        dump_json(directory / "edition.json", edition)

    def hold_publish(self):
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.publish(str(self.root), write=True)
        self.assertFalse((self.root / "daily-state").exists())
        return str(caught.exception)

    def test_403_is_not_a_dead_link_and_404_is(self):
        opener, seen = constant_opener(403, b"Forbidden")
        self.assertFalse(daily_state.url_is_dead(OPENAI, opener))
        self.assertEqual([item[0] for item in seen], ["HEAD", "GET"])
        self.assertTrue(all(item[1] == OPENAI for item in seen))

        def raise_403(method, url):
            raise urllib.error.HTTPError(url, 403, "Forbidden", hdrs=None, fp=None)

        self.assertFalse(daily_state.url_is_dead(OPENAI, raise_403))

        for status in (401, 405, 429):
            alive, _seen = constant_opener(status, b"no")
            self.assertFalse(daily_state.url_is_dead("https://example.com/page", alive), status)

        for status in (404, 410):
            dead, _seen = constant_opener(status, b"missing")
            self.assertTrue(daily_state.url_is_dead("https://example.com/missing", dead), status)

        persistent, methods = queued_opener([(500, b"down"), (500, b"down"), (500, b"down")])
        self.assertTrue(daily_state.url_is_dead("https://example.com/down", persistent))
        self.assertEqual(methods, ["HEAD", "GET", "GET"])

        recovered, _methods = queued_opener([(500, b"down"), (500, b"down"), (200, b"ok")])
        self.assertFalse(daily_state.url_is_dead("https://example.com/down", recovered))

        challenge, _seen = constant_opener(503, b"Just a moment while we verify your browser")
        self.assertFalse(daily_state.url_is_dead("https://example.com/challenge", challenge))

        def dns_failure(method, url):
            raise urllib.error.URLError(OSError("nodename nor servname provided, or not known"))

        self.assertTrue(daily_state.url_is_dead("https://example.invalid/missing", dns_failure))

        request = daily_state.build_link_request(OPENAI, "GET")
        self.assertIn("Mozilla/5.0", request.get_header("User-agent"))
        self.assertEqual(request.get_method(), "GET")

    def test_package_holds_on_404_and_passes_on_403(self):
        package = self.make_package()
        dead, _seen = constant_opener(404, b"missing")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_package(str(package), link_opener=dead)
        self.assertIn("dead_link", str(caught.exception))

        package = self.make_package()
        alive, seen = constant_opener(403, b"Forbidden")
        loaded = daily_state.validate_package(str(package), link_opener=alive)
        self.assertTrue(loaded["editor_mode"])
        self.assertEqual(daily_state.count_ai_labels(loaded["html"]), 1)
        self.assertTrue(seen)
        self.assertTrue(all(item[0] in ("HEAD", "GET") for item in seen))

    def test_offline_package_does_not_fetch_links(self):
        package = self.make_package(source_url="https://example.invalid/offline-check")
        loaded = daily_state.validate_package(str(package))
        self.assertIn("https://example.invalid/offline-check", loaded["html"])
        self.assertEqual(daily_state.count_ai_labels(loaded["html"]), 1)
        code = daily_state.main(["--package", str(package), "--check"])
        self.assertEqual(code, 0)

    def test_label_must_appear_exactly_once_in_editor_mode(self):
        directory = self.seal_editor(self.copy_edition(), empty_notes())
        daily_state.publish(str(self.root), write=True)
        html = (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count(HOUSE), 1)
        self.assertEqual(daily_state.count_ai_labels(html), 1)
        self.assertIn(
            '<p class="disclaimer">%s · <a href="editors-notes/">Editor\'s notes</a></p>' % HOUSE,
            html,
        )

        shutil.rmtree(self.root / "content")
        shutil.rmtree(self.root / "daily-state")
        directory = self.copy_edition()
        paragraphs = (
            "Models improved on clean tasks.\n\n"
            "The note says %s before the close.\n" % HOUSE
        )
        self.write_script(directory, paragraphs)
        self.seal_editor(directory, empty_notes())
        reason = self.hold_publish()
        self.assertIn("label", reason)

        shutil.rmtree(self.root / "content", ignore_errors=True)
        legacy = self.copy_edition()
        self.write_script(legacy, paragraphs)
        daily_state.publish(str(self.root), write=True)
        legacy_html = (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        self.assertGreater(daily_state.count_ai_labels(legacy_html), 1)
        self.assertNotIn("editors-notes", legacy_html)

    def test_hard_stops_hold_and_a_completed_editor_pass_does_not(self):
        blocked = editor_run(hard_stops=[{"kind": "audio", "detail": "episode file is empty"}])
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_run(blocked, DATE, 4)
        self.assertIn("audio", str(caught.exception))

        for kind in ("video", "dead_link", "label"):
            run = editor_run(hard_stops=[{"kind": kind, "detail": "blocked " + kind}])
            with self.assertRaises(daily_state.Hold):
                daily_state.validate_run(run, DATE, 4)

        incomplete = editor_run()
        incomplete["editor"] = editor_receipt(completed=False)
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_run(incomplete, DATE, 4)
        self.assertIn("not complete", str(caught.exception))

        projected = daily_state.project_qa(editor_run(), RUN_SHA, DATE, 4)
        self.assertEqual([item["name"] for item in projected["gate"]], list(daily_state.NAMED_GATES))
        self.assertTrue(all(item["ok"] is True and set(item) == {"name", "ok"} for item in projected["gate"]))
        blob = json.dumps(projected)
        self.assertNotIn("advisory", blob)
        self.assertNotIn("findings", blob)
        self.assertNotIn("should-not-leak", blob)
        self.assertNotIn("meta/muse-ember", blob)

        legacy = editor_run()
        legacy.pop("pipeline")
        legacy.pop("editor")
        legacy.pop("hard_stops")
        with self.assertRaises(daily_state.Hold):
            daily_state.project_qa(legacy, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            daily_state.validate_run(editor_run(), DATE, 4, editor_mode=False)

        section_only = editor_run()
        section_only.pop("pipeline")
        daily_state.validate_run(section_only, DATE, 4)

        nested = editor_run()
        nested["editor"] = {
            "model": "meta/muse-ember",
            "reasoning_effort": "max",
            "completed": True,
            "outstanding": 0,
            "decisions": {"accepted": 1, "overruled": 2, "partially": 0, "total": 3},
        }
        self.assertEqual(
            daily_state.normalize_editor(nested["editor"])["overruled"],
            2,
        )
        daily_state.validate_run(nested, DATE, 4)

        canonical = editor_run()
        canonical["editor"] = {
            "model": "meta/muse-ember",
            "reasoning_effort": "max",
            "completed": True,
            "outstanding": 2,
            "decisions": {
                "overruled": 1,
                "accepted_resolved": 3,
                "accepted_unresolved": 1,
                "accepted_partial": 1,
                "total": 6,
            },
        }
        receipt = daily_state.normalize_editor(canonical["editor"])
        self.assertEqual(receipt["overruled"], 1)
        self.assertEqual(receipt["accepted_resolved"], 3)
        self.assertEqual(receipt["accepted_unresolved"], 1)
        self.assertEqual(receipt["accepted_partial"], 1)
        self.assertEqual(receipt["outstanding"], 2)
        daily_state.validate_run(canonical, DATE, 4)
        canonical["editor"]["completed"] = False
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_run(canonical, DATE, 4)
        self.assertIn("not complete", str(caught.exception))
        canonical["editor"]["completed"] = True
        canonical["editor"]["outstanding"] = 9
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_run(canonical, DATE, 4)
        self.assertIn("outstanding", str(caught.exception))

        package = self.make_package()
        packaged = load_json(package / "run.json")
        packaged["editor"] = {
            "model": "meta/muse-ember",
            "reasoning_effort": "max",
            "completed": True,
            "outstanding": 0,
            "decisions": {
                "overruled": 1,
                "accepted_resolved": 2,
                "accepted_unresolved": 0,
                "accepted_partial": 0,
                "total": 3,
            },
        }
        dump_json(package / "run.json", packaged)
        self.assertTrue(daily_state.validate_package(str(package))["editor_mode"])
        packaged["editor"]["completed"] = False
        dump_json(package / "run.json", packaged)
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_package(str(package))
        self.assertIn("not complete", str(caught.exception))

        directory = self.seal_editor(
            self.copy_edition(),
            empty_notes(),
            hard_stops=[{"kind": "dead_link", "detail": "https://example.com/missing"}],
        )
        reason = self.hold_publish()
        self.assertIn("dead_link", reason)
        self.assertTrue((directory / "editor_notes.json").is_file())

    def test_notes_page_lists_outstanding_items_and_hides_overruled(self):
        notes = sample_notes()
        self.seal_editor(self.copy_edition(), notes)
        daily_state.publish(str(self.root), write=True)
        page = (self.root / "daily-state" / DATE / "editors-notes" / "index.html").read_text(encoding="utf-8")
        edition = (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        self.assertIn(notes["outstanding"][0]["summary"], page)
        self.assertIn(notes["outstanding"][0]["reason"], page)
        self.assertIn(notes["outstanding"][1]["summary"], page)
        self.assertIn("<h2>Episode</h2>", page)
        self.assertIn("<h2>Short</h2>", page)
        self.assertIn("<h2>Written edition</h2>", page)
        self.assertLess(page.index("<h2>Episode</h2>"), page.index("<h2>Short</h2>"))
        self.assertLess(page.index("<h2>Short</h2>"), page.index("<h2>Written edition</h2>"))
        self.assertIn("Unresolved", page)
        self.assertIn("Partly resolved", page)
        self.assertNotIn("accepted_unresolved", page)
        self.assertNotIn("accepted_partial", page)
        self.assertNotIn("<h2>written</h2>", page)
        self.assertNotIn(OVERRULED, page)
        self.assertNotIn(OVERRULED, edition)
        self.assertNotIn("overruled", page.lower())
        self.assertIn('href="editors-notes/"', edition)
        self.assertIn("../../../styles.css", page)
        self.assertIn("<h1>Editor&#x27;s notes — %s</h1>" % DATE, page)
        self.assertEqual(
            page.count('content="https://www.signalandnoise.email/daily-state/%s/editors-notes/"' % DATE),
            1,
        )

        rendered = daily_state.render_editors_notes_html(DATE, {
            "date": DATE,
            "outstanding": notes["outstanding"] + [{
                "artifact": "episode",
                "summary": OVERRULED,
                "reason": "the objection was set aside",
                "status": "overruled",
            }],
            "generated_by": {"model": "meta/muse-ember"},
        })
        self.assertIn("Unresolved", rendered)
        self.assertIn("Partly resolved", rendered)
        self.assertNotIn("accepted_unresolved", rendered)
        self.assertNotIn("accepted_partial", rendered)
        self.assertNotIn(OVERRULED, rendered)
        self.assertNotIn("overruled", rendered.lower())
        doubled = daily_state.render_editors_notes_html(DATE, {
            "date": DATE,
            "outstanding": [
                {
                    "artifact": "episode",
                    "summary": "First open claim.",
                    "reason": "Left as spoken.",
                    "status": "accepted_unresolved",
                },
                {
                    "artifact": "episode",
                    "summary": "Second open claim.",
                    "reason": "Tightened one clause.",
                    "status": "accepted_partial",
                },
            ],
            "generated_by": {"model": "meta/muse-ember"},
        })
        self.assertEqual(doubled.count("<h2>Episode</h2>"), 1)
        self.assertNotIn("<h2>Short</h2>", doubled)
        self.assertNotIn("<h2>Written edition</h2>", doubled)
        self.assertLess(doubled.index("First open claim."), doubled.index("Second open claim."))

    def test_empty_notes_page_says_there_are_none(self):
        self.seal_editor(self.copy_edition(), empty_notes())
        daily_state.publish(str(self.root), write=True)
        page = (self.root / "daily-state" / DATE / "editors-notes" / "index.html").read_text(encoding="utf-8")
        self.assertIn("<p>No outstanding issues</p>", page)
        self.assertNotIn("<h2>", page)
        self.assertNotIn("Unresolved", page)
        self.assertNotIn("Partly resolved", page)
        self.assertNotIn("accepted_unresolved", page)
        self.assertNotIn(OVERRULED, page)
        edition = (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Editor's notes", edition)
        self.assertEqual(edition.count(HOUSE), 1)

    def test_editor_output_scope_includes_the_notes_page(self):
        self.seal_editor(self.copy_edition(), empty_notes())
        daily_state.publish(str(self.root), write=True)
        found = daily_state.list_output_files(str(self.root))
        self.assertEqual(found, {
            "daily-state/index.html",
            "daily-state/%s/index.html" % DATE,
            "daily-state/%s/editors-notes/index.html" % DATE,
        })
        stray = self.root / "daily-state" / DATE / "decision_log.json"
        stray.write_text(json.dumps({"why": OVERRULED}), encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.publish(str(self.root), write=True)
        self.assertIn("unexpected generated output", str(caught.exception))
        self.assertIn(OVERRULED, stray.read_text(encoding="utf-8"))

        stray.unlink()
        notes_page = self.root / "daily-state" / DATE / "editors-notes" / "index.html"
        notes_page.unlink()
        with self.assertRaises(daily_state.Hold):
            daily_state.publish(str(self.root), write=False)

    def test_legacy_path_is_unchanged(self):
        expected = daily_state.load_edition(str(ROOT), DATE)
        self.copy_edition()
        daily_state.publish(str(self.root), write=True)
        html = (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html, expected["html"])
        self.assertNotIn("editors-notes", html)
        self.assertFalse((self.root / "daily-state" / DATE / "editors-notes").exists())
        self.assertEqual(html.count(HOUSE), 1)
        page_h1 = "Daily State of AI - %s" % DATE
        self.assertIn("<h1>%s</h1>" % page_h1, html)
        self.assertIn(
            '<meta property="og:url" content="https://www.signalandnoise.email/daily-state/%s/">' % DATE,
            html,
        )
        self.assertEqual(html.count('<a href="%s">Audio on Spotify</a>' % EPISODE_URL), 1)

        projected = daily_state.project_qa(
            {
                "date": DATE,
                "status": "ok",
                "semantic_qa": "pass",
                "sources": "ok",
                "source_count": 4,
                "gate": [{"name": name, "ok": True, "detail": "checked"} for name in daily_state.NAMED_GATES],
                "attempts": [{
                    "accepted": True,
                    "semantic_qa": "pass",
                    "gate": [{"name": name, "ok": True} for name in daily_state.NAMED_GATES],
                }],
            },
            RUN_SHA,
            DATE,
            4,
        )
        committed = load_json(ROOT / "content" / "daily-state" / DATE / "qa.json")
        self.assertEqual(projected, committed)

        extra = self.root / "content" / "daily-state" / DATE / "run.json"
        extra.write_text("{}\n", encoding="utf-8")
        with self.assertRaises(daily_state.Hold):
            daily_state.publish(str(self.root), write=True)
        self.assertEqual(
            (self.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8"),
            expected["html"],
        )

    def test_editor_page_keeps_h1_og_url_and_spotify_href(self):
        self.seal_editor(self.copy_edition(), sample_notes())
        loaded = daily_state.load_edition(str(self.root), DATE)
        html = loaded["html"]
        daily_state.assert_edition_page(html, loaded["edition"])
        self.assertIn("<h1>Daily State of AI - %s</h1>" % DATE, html)
        self.assertEqual(
            html.count('<meta property="og:url" content="https://www.signalandnoise.email/daily-state/%s/">' % DATE),
            1,
        )
        self.assertEqual(html.count('<a href="%s">Audio on Spotify</a>' % EPISODE_URL), 1)
        self.assertEqual(
            loaded["edition"]["hashes"]["editor_notes_sha256"],
            daily_state.sha256_bytes(
                (self.root / "content" / "daily-state" / DATE / "editor_notes.json").read_bytes()
            ),
        )

    def test_missing_audio_and_broken_video_hold(self):
        package = self.make_package()
        run = load_json(package / "run.json")
        run.pop("episode_url")
        dump_json(package / "run.json", run)
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_package(str(package))
        self.assertIn("audio", str(caught.exception))

        package = self.make_package()
        run = load_json(package / "run.json")
        run["video"] = "clip.mp4"
        dump_json(package / "run.json", run)
        (package / "clip.mp4").write_bytes(b"not-video")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_package(str(package))
        self.assertIn("video", str(caught.exception))

        (package / "clip.mp4").write_bytes(b"\x00\x00\x00\x18ftypisom" + b"\x00" * 64)
        loaded = daily_state.validate_package(str(package))
        self.assertTrue(loaded["editor_mode"])

        run["audio"] = "episode.mp3"
        dump_json(package / "run.json", run)
        (package / "episode.mp3").write_bytes(b"nope")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_package(str(package))
        self.assertIn("audio", str(caught.exception))

    def test_package_command_renders_offline_and_hides_overruled_files(self):
        package = self.make_package(notes=sample_notes())
        (package / "decision_log.json").write_text(
            json.dumps({"decisions": [{"disposition": "overruled", "why": OVERRULED}]}) + "\n",
            encoding="utf-8",
        )
        out = self.root / "rendered"
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "daily_state.py"),
                "--package",
                str(package),
                "--out",
                str(out),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("editor package: wrote 2 file(s)", proc.stdout)
        edition = (out / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")
        notes = (out / "daily-state" / DATE / "editors-notes" / "index.html").read_text(encoding="utf-8")
        self.assertIn(sample_notes()["outstanding"][0]["summary"], notes)
        self.assertIn("<h2>Written edition</h2>", notes)
        self.assertIn("<h2>Short</h2>", notes)
        self.assertIn("<h2>Episode</h2>", notes)
        self.assertIn("Partly resolved", notes)
        self.assertNotIn("accepted_partial", notes)
        self.assertNotIn(OVERRULED, edition)
        self.assertNotIn(OVERRULED, notes)
        self.assertNotIn("decision_log", edition)
        self.assertEqual(edition.count(HOUSE), 1)
        self.assertIn("<h1>Daily State of AI - %s</h1>" % DATE, edition)
        self.assertIn('href="%s"' % EPISODE_URL, edition)

        check = subprocess.run(
            [sys.executable, str(ROOT / "daily_state.py"), "--package", str(package), "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("editor package check: ok", check.stdout)
        self.assertFalse((package / "daily-state").exists())

        live = subprocess.run(
            [
                sys.executable,
                str(ROOT / "daily_state.py"),
                "--package",
                str(package),
                "--pipeline",
                "live",
                "--check",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(live.returncode, 1)
        self.assertIn("HOLD:", live.stderr)
        self.assertNotIn(OVERRULED, live.stderr)

    def make_package(self, notes=None, source_url=None):
        package = self.root / ("package-%s" % len(list(self.root.iterdir())))
        if package.exists():
            shutil.rmtree(package)
        package.mkdir()
        source = ROOT / "content" / "daily-state" / DATE
        shutil.copyfile(source / "script.txt", package / "script.txt")
        sources = load_json(source / "sources.json")
        if source_url:
            old = sources["urls"][0]
            sources["urls"][0] = source_url
            for story in sources["stories"]:
                story["urls"] = [source_url if url == old else url for url in story["urls"]]
        dump_json(package / "sources.json", sources)
        notes = empty_notes() if notes is None else notes
        dump_json(package / "editor_notes.json", notes)
        run = editor_run()
        run["editor"] = editor_receipt(outstanding=len(notes["outstanding"]))
        run["source_count"] = len(sources["urls"])
        dump_json(package / "run.json", run)
        return package


if __name__ == "__main__":
    unittest.main()
