"""Fail-closed tests for Daily State written editions. No network."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import daily_state  # noqa: E402


DATE = "2026-11-08"
EPISODE_ID = "4BrflfgytoeU5dAro96ig7"
EPISODE_URL = "https://open.spotify.com/episode/" + EPISODE_ID
EDITION_URL = "https://www.signalandnoise.email/daily-state/2026-11-08/"
SCRIPT_SHA = "15e371c987882d228c1700c6cf2a91b7eb3b3fa204b1d94aac0a25e7b157b33f"
SOURCES_SHA = "55ca2f6ec889c88fa3f62dd35b5982304ec189ce91aed13ccddf72ad0df1225b"
RUN_SHA = "b1bb60187258f6687b278f02adda1e86b20c2309e9108f5533abd50471806fd5"
SHOW_ID = "1AC7qV1tyVIICLtJVwBapp"
HOUSE = "AI-generated \u00b7 may contain errors"
SCRIPT_DISCLAIMER = "AI-generated; may contain errors."


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def reseal(directory):
    directory = Path(directory)
    edition = load_json(directory / "edition.json")
    edition["hashes"]["script_sha256"] = daily_state.sha256_bytes(
        (directory / "script.txt").read_bytes()
    )
    edition["hashes"]["sources_sha256"] = daily_state.sha256_bytes(
        (directory / "sources.json").read_bytes()
    )
    edition["hashes"]["qa_sha256"] = daily_state.sha256_bytes(
        (directory / "qa.json").read_bytes()
    )
    dump_json(directory / "edition.json", edition)


def mutate_qa(directory, fn):
    path = Path(directory) / "qa.json"
    qa = load_json(path)
    fn(qa)
    dump_json(path, qa)
    edition = load_json(Path(directory) / "edition.json")
    edition["hashes"]["run_sha256"] = qa["run_sha256"]
    dump_json(Path(directory) / "edition.json", edition)
    reseal(directory)


def mutate_sources(directory, fn, sync_count=True):
    path = Path(directory) / "sources.json"
    sources = load_json(path)
    fn(sources)
    dump_json(path, sources)
    if sync_count:
        qa_path = Path(directory) / "qa.json"
        qa = load_json(qa_path)
        qa["source_count"] = len(sources["urls"])
        dump_json(qa_path, qa)
    reseal(directory)


def mutate_edition(directory, fn):
    path = Path(directory) / "edition.json"
    edition = load_json(path)
    fn(edition)
    dump_json(path, edition)


def retarget(directory, iso_date, episode_id):
    directory = Path(directory)
    sources = load_json(directory / "sources.json")
    sources["date"] = iso_date
    dump_json(directory / "sources.json", sources)
    qa = load_json(directory / "qa.json")
    qa["date"] = iso_date
    dump_json(directory / "qa.json", qa)
    episode_url = "https://open.spotify.com/episode/" + episode_id
    title = "Daily State of AI - " + iso_date
    edition = load_json(directory / "edition.json")
    edition["date"] = iso_date
    edition["title"] = title
    edition["canonical_url"] = "https://www.signalandnoise.email/daily-state/%s/" % iso_date
    edition["episode_id"] = episode_id
    edition["episode_url"] = episode_url
    edition["verified_at"] = iso_date + "T17:53Z"
    edition["verification"]["checked_at"] = edition["verified_at"]
    edition["verification"]["episode"] = {
        "title": title,
        "canonical_url": episode_url,
        "id": episode_id,
    }
    edition["verification"]["show"]["episodes"] = [{
        "id": episode_id,
        "title": title,
        "uri": "spotify:episode:" + episode_id,
    }]
    dump_json(directory / "edition.json", edition)
    reseal(directory)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.script_depth = 0
        self.capture = None
        self.buf = []
        self.script_paragraphs = []
        self.h1 = None
        self.disclaimer = None
        self.anchors = []
        self.anchor_at = None
        self.metas = []
        self.links = []
        self.times = []
        self.time_at = None
        self.story_titles = []
        self.forbidden = []
        self.title = None

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.stack.append((tag, attr))
        if tag in ("iframe", "script"):
            self.forbidden.append(tag)
        classes = attr.get("class", "").split()
        if tag == "div" and "script" in classes:
            self.script_depth += 1
        if tag == "title":
            self.capture = "title"
            self.buf = []
        elif tag == "h1":
            self.capture = "h1"
            self.buf = []
        elif tag == "h3":
            self.capture = "h3"
            self.buf = []
        elif tag == "p" and self.script_depth:
            self.capture = "script-p"
            self.buf = []
        elif tag == "p" and "disclaimer" in classes:
            self.capture = "disclaimer"
            self.buf = []
        if tag == "a":
            self.anchors.append({"attrs": attr, "text": ""})
            self.anchor_at = len(self.anchors) - 1
        if tag == "meta":
            self.metas.append(attr)
        if tag == "link":
            self.links.append(attr)
        if tag == "time":
            self.times.append({"datetime": attr.get("datetime"), "text": ""})
            self.time_at = len(self.times) - 1

    def handle_endtag(self, tag):
        if self.capture == "script-p" and tag == "p":
            self.script_paragraphs.append("".join(self.buf))
            self.capture = None
        elif self.capture == "h1" and tag == "h1":
            self.h1 = "".join(self.buf)
            self.capture = None
        elif self.capture == "h3" and tag == "h3":
            self.story_titles.append("".join(self.buf))
            self.capture = None
        elif self.capture == "disclaimer" and tag == "p":
            self.disclaimer = "".join(self.buf)
            self.capture = None
        elif self.capture == "title" and tag == "title":
            self.title = "".join(self.buf)
            self.capture = None
        if tag == "a":
            self.anchor_at = None
        if tag == "time":
            self.time_at = None
        if (
            tag == "div" and self.stack
            and self.stack[-1][0] == "div"
            and "script" in self.stack[-1][1].get("class", "").split()
        ):
            self.script_depth -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data)
        if self.anchor_at is not None:
            self.anchors[self.anchor_at]["text"] += data
        if self.time_at is not None:
            self.times[self.time_at]["text"] += data


def parse_page(text):
    page = Page()
    page.feed(text)
    return page


def meta_map(page):
    found = {}
    for item in page.metas:
        key = item.get("property") or item.get("name") or item.get("http-equiv")
        if key:
            found[key] = item.get("content")
    return found


def minimal_run(**overrides):
    gate = [{"name": name, "ok": True, "detail": "checked"} for name in daily_state.NAMED_GATES]
    attempt = {
        "accepted": True,
        "semantic_qa": "pass",
        "gate": [dict(item) for item in gate],
        "model": "hidden",
    }
    run = {
        "date": DATE,
        "status": "ok",
        "semantic_qa": "pass",
        "sources": "ok",
        "source_count": 4,
        "gate": gate,
        "attempts": [attempt],
        "model": "should-not-leak",
        "telegram": "sent",
        "bundle_file": "/private/conversation_bundle.v1.json",
    }
    run.update(overrides)
    return run


class DailyStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def copy_edition(self, iso_date=DATE, episode_id=None):
        source = ROOT / "content" / "daily-state" / DATE
        dest = self.root / "content" / "daily-state" / iso_date
        if dest.is_symlink():
            dest.unlink()
        elif dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.mkdir()
        for name in daily_state.CONTENT_FILES:
            shutil.copyfile(source / name, dest / name)
        if iso_date != DATE:
            retarget(dest, iso_date, episode_id or ("B" * 22))
        return dest

    def generated(self):
        return self.root / "daily-state"

    def assert_no_output(self):
        self.assertFalse(self.generated().exists(), "invalid input wrote edition HTML")

    def hold(self):
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.publish(str(self.root), write=True)
        self.assert_no_output()
        return str(caught.exception)

    def test_today_fixture_page(self):
        directory = ROOT / "content" / "daily-state" / DATE
        script = (directory / "script.txt").read_bytes()
        sources_bytes = (directory / "sources.json").read_bytes()
        self.assertEqual(hashlib.sha256(script).hexdigest(), SCRIPT_SHA)
        self.assertEqual(hashlib.sha256(sources_bytes).hexdigest(), SOURCES_SHA)
        self.assertEqual(len(script.decode("utf-8").split()), 645)

        loaded = daily_state.load_edition(str(ROOT), DATE)
        page_path = ROOT / "daily-state" / DATE / "index.html"
        html = page_path.read_text(encoding="utf-8")
        self.assertEqual(html, loaded["html"])
        self.assertEqual(html, daily_state.load_edition(str(ROOT), DATE)["html"])

        page = parse_page(html)
        self.assertEqual(page.h1, "Daily State of AI - 2026-11-08")
        self.assertEqual(page.script_paragraphs, daily_state.script_paragraphs(script.decode("utf-8")))
        self.assertEqual(len(" ".join(page.script_paragraphs).split()), 645)
        self.assertEqual(page.script_paragraphs[-1], SCRIPT_DISCLAIMER)
        self.assertEqual(page.disclaimer, HOUSE)
        self.assertNotIn(HOUSE, page.script_paragraphs)
        self.assertEqual(page.times[0]["datetime"], DATE)
        self.assertEqual(page.times[0]["text"], "November 8, 2026")
        self.assertNotIn("T17:53", html)

        audio = [item for item in page.anchors if item["text"].strip() == "Audio on Spotify"]
        self.assertEqual(len(audio), 1)
        self.assertEqual(audio[0]["attrs"], {"href": EPISODE_URL})
        self.assertEqual(html.count(EPISODE_URL), 1)
        self.assertNotIn("open.spotify.com/show", html)
        self.assertNotIn("app.link", html.lower())
        self.assertEqual(page.forbidden, [])
        self.assertNotIn("<iframe", html.lower())
        self.assertNotIn("<script", html.lower())
        self.assertNotIn('http-equiv="refresh"', html.lower())
        self.assertNotIn("onclick", html.lower())
        self.assertNotIn("window.location", html)

        source_doc = load_json(directory / "sources.json")
        self.assertEqual(page.story_titles, [story["title"] for story in source_doc["stories"]])
        hrefs = [item["attrs"].get("href") for item in page.anchors]
        for url in source_doc["urls"]:
            self.assertEqual(hrefs.count(url), 1)
        self.assertEqual(len(source_doc["urls"]), 4)
        self.assertEqual(len(source_doc["stories"]), 2)

        metas = meta_map(page)
        self.assertEqual(metas["og:url"], EDITION_URL)
        self.assertEqual(metas["og:title"], "Daily State of AI - 2026-11-08")
        self.assertEqual(metas["og:type"], "article")
        self.assertEqual(metas["og:site_name"], "Signal & Noise")
        self.assertEqual(metas["twitter:card"], "summary_large_image")
        self.assertEqual(metas["twitter:title"], "Daily State of AI - 2026-11-08")
        self.assertIn("twitter:description", metas)
        self.assertTrue(metas["og:image"].startswith("https://www.signalandnoise.email/assets/preview.png?v="))
        self.assertEqual(metas["twitter:image"], metas["og:image"])
        self.assertNotIn("article:published_time", metas)
        canonical = [item["href"] for item in page.links if item.get("rel") == "canonical"]
        self.assertEqual(canonical, [EDITION_URL])
        self.assertEqual(canonical[0], metas["og:url"])
        css = [item["href"] for item in page.links if item.get("rel") == "stylesheet"]
        self.assertEqual(css, ["../../styles.css"])
        self.assertTrue((page_path.parent / css[0]).resolve().is_file())
        image_path = ROOT / "assets" / "preview.png"
        self.assertTrue(image_path.is_file())
        self.assertIn(page.h1, page.title)
        self.assertNotIn("The human author owns the wording", html)
        self.assertIn("not a human essay", html)

        listing = (ROOT / "daily-state" / "index.html").read_text(encoding="utf-8")
        listed = parse_page(listing)
        self.assertEqual(listed.h1, "Daily State of AI")
        self.assertIn(DATE + "/", [item["attrs"].get("href") for item in listed.anchors])
        self.assertIn("../styles.css", listing)
        feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
        archive = (ROOT / "archive" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("/daily-state/", feed)
        self.assertNotIn("/daily-state/", archive)

    def test_public_qa_projection_drops_private_fields(self):
        projected = daily_state.project_qa(minimal_run(), RUN_SHA, DATE, 4)
        committed = load_json(ROOT / "content" / "daily-state" / DATE / "qa.json")
        self.assertEqual(committed, projected)
        self.assertEqual(set(projected), daily_state.QA_KEYS)
        blob = json.dumps(projected)
        self.assertNotIn("telegram", blob)
        self.assertNotIn("should-not-leak", blob)
        self.assertNotIn("bundle_file", blob)
        self.assertEqual(projected["run_sha256"], RUN_SHA)
        self.assertEqual([item["name"] for item in projected["gate"]], list(daily_state.NAMED_GATES))
        self.assertTrue(all(item["ok"] is True and set(item) == {"name", "ok"} for item in projected["gate"]))

    def test_episode_selection_uses_exact_title(self):
        yesterday = "1" * 22
        today = EPISODE_ID
        latest = "2" * 22
        episodes = [
            {"id": yesterday, "title": "Daily State of AI - 2026-11-07", "uri": "spotify:episode:" + yesterday},
            {"id": today, "title": "Daily State of AI - " + DATE, "uri": "spotify:episode:" + today},
            {"id": latest, "title": "Daily State of AI - 2026-11-09", "uri": "spotify:episode:" + latest},
        ]
        chosen = daily_state.select_episode(episodes, "Daily State of AI - " + DATE)
        self.assertEqual(chosen["id"], today)
        self.assertNotEqual(chosen["id"], episodes[0]["id"])
        self.assertNotEqual(chosen["id"], episodes[-1]["id"])
        with self.assertRaises(daily_state.Hold):
            daily_state.select_episode(episodes[:1] + episodes[2:], "Daily State of AI - " + DATE)

        def fetcher(url):
            if "/episode/" in url:
                return {
                    "title": "Daily State of AI - " + DATE,
                    "canonical_url": EPISODE_URL,
                    "id": today,
                }
            return {"episodes": episodes}

        found = daily_state.verify_public_episode(
            fetcher, DATE, EPISODE_URL, "https://open.spotify.com/show/" + SHOW_ID
        )
        self.assertEqual(found["id"], today)

    def test_episode_identity_failures_hold(self):
        yesterday = "1" * 22
        latest = "2" * 22
        decoys = [
            {"id": yesterday, "title": "Daily State of AI - 2026-11-07", "uri": "spotify:episode:" + yesterday},
            {"id": EPISODE_ID, "title": "Daily State of AI - " + DATE, "uri": "spotify:episode:" + EPISODE_ID},
            {"id": latest, "title": "Daily State of AI - 2026-11-09", "uri": "spotify:episode:" + latest},
        ]

        def fetcher_factory(episode_doc, show_doc=None, boom=None):
            def fetcher(url):
                if boom:
                    raise boom
                if "/episode/" in url:
                    return episode_doc
                return show_doc if show_doc is not None else {"episodes": decoys}
            return fetcher

        show = "https://open.spotify.com/show/" + SHOW_ID
        cases = [
            (fetcher_factory({"title": "Daily State of AI - 2026-11-07", "canonical_url": EPISODE_URL, "id": EPISODE_ID}), EPISODE_URL, "yesterday"),
            (fetcher_factory({"title": "Daily State of AI - " + DATE, "canonical_url": "https://open.spotify.com/show/" + SHOW_ID, "id": EPISODE_ID}), EPISODE_URL, "canonical"),
            (fetcher_factory(
                {"title": "Daily State of AI - " + DATE, "canonical_url": EPISODE_URL, "id": EPISODE_ID},
                {"episodes": [{
                    "id": "3" * 22,
                    "title": "Daily State of AI - " + DATE,
                    "uri": "spotify:episode:" + ("3" * 22),
                }]},
            ), EPISODE_URL, "show"),
            (fetcher_factory(None, boom=TimeoutError("timed out")), EPISODE_URL, "fetch"),
            (fetcher_factory("not-a-document"), EPISODE_URL, "parse"),
        ]
        for fetcher, episode_url, label in cases:
            with self.subTest(label=label):
                with self.assertRaises(daily_state.Hold):
                    daily_state.verify_public_episode(fetcher, DATE, episode_url, show)
        with self.assertRaises(daily_state.Hold):
            daily_state.verify_public_episode(
                fetcher_factory({}), DATE, "https://open.spotify.com/show/" + SHOW_ID, show
            )
        with self.assertRaises(daily_state.Hold):
            daily_state.verify_public_episode(
                fetcher_factory({}), DATE, "https://spotify.app.link/episode", show
            )

    def test_recorded_episode_gates_write_nothing(self):
        self.copy_edition()
        reason = self._hold_after(lambda directory: mutate_edition(
            directory, lambda edition: edition.__setitem__("episode_url", "https://open.spotify.com/show/" + SHOW_ID)
        ))
        self.assertIn("episode", reason.lower())

        self.copy_edition()
        self._hold_after(lambda directory: mutate_edition(
            directory, lambda edition: edition.__setitem__("spotify_episode_fallback", True)
        ))

        self.copy_edition()
        self._hold_after(lambda directory: mutate_edition(directory, lambda edition: edition.pop("episode_url")))

        self.copy_edition()
        self._hold_after(lambda directory: mutate_edition(
            directory,
            lambda edition: edition["verification"]["episode"].__setitem__(
                "title", "Daily State of AI - 2026-11-07"
            ),
        ))

        self.copy_edition()
        self._hold_after(lambda directory: mutate_edition(
            directory,
            lambda edition: edition["verification"]["episode"].__setitem__(
                "canonical_url", "https://open.spotify.com/episode/" + ("A" * 22)
            ),
        ))

        self.copy_edition()
        self._hold_after(lambda directory: mutate_edition(
            directory,
            lambda edition: edition["verification"]["show"]["episodes"][0].__setitem__("id", "C" * 22),
        ))

    def _hold_after(self, mutate):
        directory = self.root / "content" / "daily-state" / DATE
        mutate(directory)
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.publish(str(self.root), write=True)
        self.assert_no_output()
        return str(caught.exception)

    def test_missing_empty_and_bad_inputs_write_nothing(self):
        self.copy_edition()
        (self.root / "content" / "daily-state" / DATE / "script.txt").unlink()
        self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        script = self.root / "content" / "daily-state" / DATE / "script.txt"
        script.write_text("", encoding="utf-8")
        reseal(script.parent)
        self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        script = self.root / "content" / "daily-state" / DATE / "script.txt"
        script.write_bytes(b"\xff\xfe not utf-8")
        reseal(script.parent)
        self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        sources = self.root / "content" / "daily-state" / DATE / "sources.json"
        sources.write_text("{", encoding="utf-8")
        reseal(sources.parent)
        self.hold()

        real_open = os.open

        def denied(path, flags, *args, **kwargs):
            if str(path).endswith("script.txt"):
                raise PermissionError("denied")
            return real_open(path, flags, *args, **kwargs)

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        os.open = denied
        try:
            self.hold()
        finally:
            os.open = real_open

    def test_qa_and_source_failures_write_nothing(self):
        mutations = [
            lambda qa: qa.__setitem__("status", "fail"),
            lambda qa: qa.__setitem__("status", None),
            lambda qa: qa.__setitem__("semantic_qa", "fail"),
            lambda qa: qa.__setitem__("semantic_qa", None),
            lambda qa: qa.pop("semantic_qa"),
            lambda qa: qa.__setitem__("sources", "fail"),
            lambda qa: qa.__setitem__("source_count", "4"),
            lambda qa: qa.__setitem__("source_count", 3),
            lambda qa: qa.__setitem__("date", "2026-11-07"),
            lambda qa: qa.__setitem__("gate", []),
            lambda qa: qa.__setitem__("gate", qa["gate"][:-1]),
            lambda qa: qa["gate"].append(dict(qa["gate"][0])),
            lambda qa: qa["gate"][0].__setitem__("ok", False),
            lambda qa: qa["gate"][0].__setitem__("ok", "false"),
            lambda qa: qa["gate"][0].__setitem__("ok", "true"),
            lambda qa: qa.__setitem__("schema_version", 2),
            lambda qa: qa.__setitem__("telegram", "sent"),
        ]
        for mutate in mutations:
            with self.subTest(mutate=getattr(mutate, "__code__", mutate).co_consts):
                shutil.rmtree(self.root / "content", ignore_errors=True)
                shutil.rmtree(self.generated(), ignore_errors=True)
                self.copy_edition()
                mutate_qa(self.root / "content" / "daily-state" / DATE, mutate)
                self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        mutate_sources(
            self.root / "content" / "daily-state" / DATE,
            lambda sources: sources.__setitem__("date", "2026-11-07"),
            sync_count=False,
        )
        self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        mutate_sources(
            self.root / "content" / "daily-state" / DATE,
            lambda sources: sources["stories"][0].__setitem__("title", "  "),
        )
        self.hold()

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        mutate_sources(
            self.root / "content" / "daily-state" / DATE,
            lambda sources: sources["urls"].pop(),
        )
        self.hold()

    def test_run_schema_failures_do_not_project_a_pass(self):
        base = minimal_run()
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            del broken["attempts"]
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            del broken["semantic_qa"]
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["attempts"] = [{
                "accepted": False,
                "semantic_qa": "pass",
                "gate": broken["gate"],
            }]
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["attempts"][0]["semantic_qa"] = "fail"
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["gate"] = []
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["gate"][0]["ok"] = "false"
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["gate"][0]["ok"] = "true"
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        with self.assertRaises(daily_state.Hold):
            broken = minimal_run()
            broken["source_count"] = 3
            daily_state.project_qa(broken, RUN_SHA, DATE, 4)
        reversed_run = minimal_run()
        reversed_run["gate"] = list(reversed(reversed_run["gate"]))
        projected = daily_state.project_qa(reversed_run, RUN_SHA, DATE, 4)
        self.assertEqual([item["name"] for item in projected["gate"]], list(daily_state.NAMED_GATES))
        self.assertNotIn("model", projected)
        self.assertEqual(base["status"], "ok")

    def test_dangerous_urls_are_rejected_and_write_nothing(self):
        rejected = [
            "javascript:alert(1)",
            "data:text/html,hi",
            "https://user:pass@example.com/a",
            "https://user@example.com/a",
            "http://example.com/a",
            "https://127.0.0.1/a",
            "https://10.1.2.3/a",
            "https://192.168.0.5/a",
            "https://localhost/a",
            "https://evil.app.link/x",
            "https://example.com/a#frag",
        ]
        for url in rejected:
            with self.subTest(url=url):
                with self.assertRaises(daily_state.Hold):
                    daily_state.validate_public_https_url(url)
                shutil.rmtree(self.root / "content", ignore_errors=True)
                shutil.rmtree(self.generated(), ignore_errors=True)
                self.copy_edition()

                def plant(sources, bad=url):
                    sources["urls"][0] = bad
                    sources["stories"][0]["urls"][0] = bad

                mutate_sources(self.root / "content" / "daily-state" / DATE, plant)
                self.hold()
        allowed = daily_state.validate_public_https_url("https://example.com/a?b=1&c=2")
        self.assertEqual(allowed, "https://example.com/a?b=1&c=2")

    def test_escaping_preserves_paragraphs_and_exact_hrefs(self):
        self.copy_edition()
        directory = self.root / "content" / "daily-state" / DATE
        paragraphs = [
            'Tom & Jerry <script>alert("xss")</script> say "hello" and \'goodbye\'.',
            "Unicode \u201cquotes\u201d \u2019 \u2014 \u2013 \u2026 stay words.",
            "**not markdown** and <em>not html</em>.",
            SCRIPT_DISCLAIMER,
        ]
        (directory / "script.txt").write_text("\n\n".join(paragraphs) + "\n", encoding="utf-8")
        mutate_sources(directory, lambda sources: sources.update({
            "urls": [
                "https://example.com/a?b=1&c=2",
                "https://x.com/example/status/1",
            ],
            "stories": [{
                "index": 1,
                "title": 'A & B <script>alert("t")</script>',
                "outlets": ["Q&A <outlet>"],
                "urls": [
                    "https://example.com/a?b=1&c=2",
                    "https://x.com/example/status/1",
                ],
            }],
        }))
        qa = load_json(directory / "qa.json")
        self.assertEqual(qa["source_count"], 2)
        result = daily_state.publish(str(self.root), write=True)
        self.assertGreater(result["wrote"], 0)
        html = (self.generated() / DATE / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<script", html.lower())
        self.assertIn("&amp;", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&quot;", html)
        page = parse_page(html)
        self.assertEqual(page.script_paragraphs, paragraphs)
        self.assertEqual(page.script_paragraphs[-1], SCRIPT_DISCLAIMER)
        self.assertEqual(page.disclaimer, HOUSE)
        self.assertEqual(page.story_titles, ['A & B <script>alert("t")</script>'])
        hrefs = [item["attrs"].get("href") for item in page.anchors]
        self.assertIn("https://example.com/a?b=1&c=2", hrefs)
        self.assertIn("https://x.com/example/status/1", hrefs)
        self.assertEqual(
            [item["attrs"].get("href") for item in page.anchors if item["text"].strip() == "Audio on Spotify"],
            [EPISODE_URL],
        )
        metas = meta_map(page)
        self.assertIn("Tom & Jerry", metas["og:description"])
        self.assertIn("<script>", metas["og:description"])
        self.assertNotIn("<script", html.lower())
        self.assertEqual(metas["og:url"], EDITION_URL)
        self.assertEqual(page.times[0]["datetime"], DATE)
        self.assertIn("../../styles.css", html)
        self.assertTrue(metas["twitter:title"])
        self.assertTrue(metas["twitter:description"])
        self.assertTrue(metas["twitter:image"].startswith("https://"))

    def test_flat_urls_missing_from_stories_are_appended_once(self):
        self.copy_edition()
        directory = self.root / "content" / "daily-state" / DATE
        mutate_sources(directory, lambda sources: sources["stories"][0]["urls"].pop())
        daily_state.publish(str(self.root), write=True)
        html = (self.generated() / DATE / "index.html").read_text(encoding="utf-8")
        page = parse_page(html)
        self.assertIn("Other URLs", page.story_titles)
        dropped = "https://x.com/IntCyberDigest/status/2119380660238303715"
        hrefs = [item["attrs"].get("href") for item in page.anchors]
        self.assertEqual(hrefs.count(dropped), 1)

    def test_hash_symlink_traversal_and_schema_block_import(self):
        self.copy_edition()
        mutate_edition(
            self.root / "content" / "daily-state" / DATE,
            lambda edition: edition["hashes"].__setitem__(
                "script_sha256", "0" * 64
            ),
        )
        reason = self.hold()
        self.assertIn("script_sha256", reason)

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        (self.root / "content" / "daily-state" / DATE / "qa.json").write_text(
            '{"date": "2026-11-08", "date": "2026-11-07"}\n',
            encoding="utf-8",
        )
        reseal(self.root / "content" / "daily-state" / DATE)
        self.hold()

        shutil.rmtree(self.root / "content")
        outside = self.root / "outside"
        outside.mkdir()
        for name in daily_state.CONTENT_FILES:
            shutil.copyfile(
                ROOT / "content" / "daily-state" / DATE / name,
                outside / name,
            )
        linked = self.root / "content" / "daily-state" / DATE
        linked.parent.mkdir(parents=True, exist_ok=True)
        linked.symlink_to(outside)
        self.hold()

        for bad in ("..", "2026-11-08/../../etc/passwd", "/tmp", "2026-02-31"):
            with self.subTest(bad=bad):
                with self.assertRaises(daily_state.Hold):
                    daily_state.load_edition(str(self.root), bad)

        real = daily_state._read_once
        calls = {"n": 0}

        def flaky(path):
            calls["n"] += 1
            data = real(path)
            if calls["n"] == 2:
                return data + b"\n"
            return data

        shutil.rmtree(self.root / "content")
        self.copy_edition()
        daily_state._read_once = flaky
        try:
            reason = self.hold()
        finally:
            daily_state._read_once = real
        self.assertIn("changed during read", reason)

        extra = self.root / "content" / "daily-state" / DATE / "run.json"
        # The hold above removed nothing from content. Replace with a clean copy.
        shutil.rmtree(self.root / "content")
        self.copy_edition()
        extra.write_text("{}", encoding="utf-8")
        self.hold()

    def test_identical_rerun_is_a_noop_and_same_day_changes_do_not_overwrite(self):
        self.copy_edition()
        first = daily_state.publish(str(self.root), write=True)
        self.assertGreater(first["wrote"], 0)
        edition_path = self.generated() / DATE / "index.html"
        listing_path = self.generated() / "index.html"
        edition_bytes = edition_path.read_bytes()
        listing_bytes = listing_path.read_bytes()
        edition_mtime = edition_path.stat().st_mtime_ns
        listing_mtime = listing_path.stat().st_mtime_ns
        second = daily_state.publish(str(self.root), write=True)
        self.assertTrue(second["noop"])
        self.assertEqual(second["wrote"], 0)
        self.assertEqual(edition_path.stat().st_mtime_ns, edition_mtime)
        self.assertEqual(listing_path.stat().st_mtime_ns, listing_mtime)

        script = self.root / "content" / "daily-state" / DATE / "script.txt"
        script.write_text(script.read_text(encoding="utf-8") + "\nA correction paragraph.\n", encoding="utf-8")
        reseal(script.parent)
        with self.assertRaises(daily_state.Hold):
            daily_state.publish(str(self.root), write=True)
        self.assertEqual(edition_path.read_bytes(), edition_bytes)
        self.assertEqual(listing_path.read_bytes(), listing_bytes)

        corrected = daily_state.publish(str(self.root), write=True, allow_correction=True)
        self.assertGreater(corrected["wrote"], 0)
        self.assertNotEqual(edition_path.read_bytes(), edition_bytes)
        self.assertIn("A correction paragraph.", edition_path.read_text(encoding="utf-8"))

    def test_invalid_new_edition_does_not_touch_listing_or_other_output(self):
        self.copy_edition()
        daily_state.publish(str(self.root), write=True)
        original_edition = (self.generated() / DATE / "index.html").read_bytes()
        original_listing = (self.generated() / "index.html").read_bytes()
        edition_mtime = (self.generated() / DATE / "index.html").stat().st_mtime_ns
        self.copy_edition("2026-11-07", "D" * 22)
        mutate_qa(
            self.root / "content" / "daily-state" / "2026-11-07",
            lambda qa: qa.__setitem__("status", "fail"),
        )
        with self.assertRaises(daily_state.Hold):
            daily_state.publish(str(self.root), write=True)
        self.assertEqual((self.generated() / DATE / "index.html").read_bytes(), original_edition)
        self.assertEqual((self.generated() / "index.html").read_bytes(), original_listing)
        self.assertEqual((self.generated() / DATE / "index.html").stat().st_mtime_ns, edition_mtime)
        self.assertFalse((self.generated() / "2026-11-07" / "index.html").exists())

        mutate_qa(
            self.root / "content" / "daily-state" / "2026-11-07",
            lambda qa: qa.__setitem__("status", "ok"),
        )
        daily_state.publish(str(self.root), write=True)
        self.assertTrue((self.generated() / "2026-11-07" / "index.html").is_file())
        listing = (self.generated() / "index.html").read_text(encoding="utf-8")
        self.assertLess(listing.index("2026-11-08/"), listing.index("2026-11-07/"))
        self.assertEqual((self.generated() / DATE / "index.html").read_bytes(), original_edition)
        self.assertEqual((self.generated() / DATE / "index.html").stat().st_mtime_ns, edition_mtime)

    def test_correction_flag_does_not_bypass_a_failed_gate(self):
        self.copy_edition()
        daily_state.publish(str(self.root), write=True)
        before = (self.generated() / DATE / "index.html").read_bytes()
        mutate_qa(
            self.root / "content" / "daily-state" / DATE,
            lambda qa: qa.__setitem__("semantic_qa", "fail"),
        )
        with self.assertRaises(daily_state.Hold):
            daily_state.publish(str(self.root), write=True, allow_correction=True)
        self.assertEqual((self.generated() / DATE / "index.html").read_bytes(), before)

    def test_check_mode_writes_nothing_and_rejects_edited_html(self):
        self.copy_edition()
        daily_state.publish(str(self.root), write=True)
        stamps = {
            path: path.stat().st_mtime_ns
            for path in self.generated().rglob("*")
            if path.is_file()
        }
        created = {"temps": 0}
        real_mkstemp = tempfile.mkstemp

        def counting_mkstemp(*args, **kwargs):
            created["temps"] += 1
            return real_mkstemp(*args, **kwargs)

        tempfile.mkstemp = counting_mkstemp
        try:
            code = daily_state.main(["--check"], repo=str(self.root))
        finally:
            tempfile.mkstemp = real_mkstemp
        self.assertEqual(code, 0)
        self.assertEqual(created["temps"], 0)
        for path, stamp in stamps.items():
            self.assertEqual(path.stat().st_mtime_ns, stamp)

        target = self.generated() / DATE / "index.html"
        original = target.read_text(encoding="utf-8")
        target.write_text(original.replace("Audio on Spotify", "Audio elsewhere"), encoding="utf-8")
        code = daily_state.main(["--check"], repo=str(self.root))
        self.assertEqual(code, 1)
        self.assertIn("Audio elsewhere", target.read_text(encoding="utf-8"))
        self.assertNotIn("Audio on Spotify", target.read_text(encoding="utf-8"))

    def test_description_is_a_bounded_prefix(self):
        sentence = ("Alpha " * 80).strip() + "."
        description = daily_state.description_from_paragraphs([sentence])
        self.assertLessEqual(len(description), daily_state.DESC_MAX)
        self.assertTrue(sentence.startswith(description))
        self.assertNotIn("...", description)

    def test_repo_check_leaves_essays_byte_identical(self):
        tracked = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
        ).stdout.split(b"\0")
        before = {}
        for rel in tracked:
            if not rel:
                continue
            path = ROOT / rel.decode()
            if path.is_file():
                before[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        proc = subprocess.run(
            [sys.executable, "build.py", "--daily-state-check"],
            cwd=ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("daily state check: ok", proc.stdout)
        self.assertNotIn("built:", proc.stdout)
        self.assertNotIn("fidelity check:", proc.stdout)
        direct = subprocess.run(
            [sys.executable, "daily_state.py", "--check"],
            cwd=ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(direct.returncode, 0, direct.stderr)
        after = {}
        for rel in before:
            path = ROOT / rel.decode()
            after[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        essay = (
            ROOT / "p"
            / "stop-trying-to-out-willpower-your-appetite-stuff-it-into-submission-instead"
            / "index.html"
        ).read_text(encoding="utf-8")
        self.assertIn("The human author owns the wording", essay)


if __name__ == "__main__":
    unittest.main()
