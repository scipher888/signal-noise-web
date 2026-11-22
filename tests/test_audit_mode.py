"""Opt-in audit mode for a raw variant edition. No network.

The live and editor publishers stay the default. A neon/ directory is a
second page for the same date, with an audit receipt instead of qa.json.
"""

import hashlib
import html as html_lib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import daily_state  # noqa: E402


DATE = "2026-11-20"
VARIANT = "neon"
LIVE_DATE = "2026-11-08"
HOUSE = "AI-generated \u00b7 may contain errors"
NEON_URL = "https://www.signalandnoise.email/daily-state/2026-11-20/neon/"
AUDIT_URL = "https://www.signalandnoise.email/daily-state/2026-11-20/neon/audit/"
AUDIO = "/content/daily-state/2026-11-20/neon/episode.mp3"
SHORT = "/content/daily-state/2026-11-20/neon/short.mp4"
SOURCES = "/content/daily-state/2026-11-20/neon/sources.json"
NOTE = (
    "Written by Google Gemini 4 Neon (medium) from one minimal prompt, "
    "with no rules, editor or edits, published as produced."
)
EXPLANATION = (
    "Each claim is a small Python check run against the source texts. "
    "The audit is for transparency and is not a gate."
)
PRIMARY_ROW = (
    '<p class="row"><a href="2026-11-20/">Daily State of AI - 2026-11-20</a> '
    '<span class="meta"><time datetime="2026-11-20">November 20, 2026</time></span></p>'
)
NEON_ROW = (
    '<p class="row"><a href="2026-11-20/neon/">'
    "Daily State of AI - 2026-11-20 (Gemini 4 Neon, raw)</a> "
    '<span class="meta"><time datetime="2026-11-20">November 20, 2026</time></span></p>'
)
ASSET_SHA256 = {
    "script.txt": "c89ccd3e741350f0569e938129259f4e6436804a4d833b7a0c5584d0fa6d8b66",
    "episode.mp3": "90bba3f20b8cd170159b19031c58cf88c08096acff8bd097ae353d9c1804ed09",
    "short.mp4": "459f1d2fa7bfe46e500ee0a9f43e7088d13a1757b3e92e59d00a2e8e6ee4ce77",
    "sources.json": "cf10b56b83d1f21c77994b7d2f75d02448679a54347e2b8d3183c1ee8d834d0a",
    "neon_run.json": "ce87bd6c328a3d737339429604178c94232232c2a16edc6b18c60d4d035c9e1b",
    "audit/audit.json": "0314fbe7098d60a044c3f036dccac527661a3320345c15b2e4b2a4a0e1089e9d",
}
LIVE_PAGE_SHA256 = {
    "daily-state/2026-11-20/index.html":
        "2f7b5340910a8ca8a5953064c0ac5cfe9b6e970c770c87e248982a62421e307c",
    "daily-state/2026-11-20/editors-notes/index.html":
        "ecb7099cc1e69a402852832efad021997b1da422fcce4798b63c72dc8e58e02b",
}


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def neon_dir():
    return ROOT / "content" / "daily-state" / DATE / VARIANT


class AuditModeTests(unittest.TestCase):
    def test_asset_bytes_and_live_pages_keep_their_hashes(self):
        for name, digest in ASSET_SHA256.items():
            self.assertEqual(sha256_file(neon_dir() / name), digest, name)
        self.assertFalse((neon_dir() / "qa.json").exists())
        for rel, digest in LIVE_PAGE_SHA256.items():
            path = ROOT / rel
            self.assertEqual(sha256_file(path), digest, rel)
        loaded = daily_state.load_edition(str(ROOT), DATE)
        self.assertEqual(
            (ROOT / "daily-state" / DATE / "index.html").read_text(encoding="utf-8"),
            loaded["html"],
        )
        self.assertEqual(
            (ROOT / "daily-state" / DATE / "editors-notes" / "index.html").read_text(encoding="utf-8"),
            loaded["notes_html"],
        )
        self.assertIn("Audio on Spotify", loaded["html"])
        self.assertTrue(loaded["editor_mode"])
        self.assertFalse(loaded.get("audit_mode"))

    def test_variant_is_known_and_dates_stay_dates(self):
        dates = daily_state.list_edition_dates(str(ROOT))
        self.assertIn(DATE, dates)
        self.assertTrue(all(daily_state.is_real_date(item) for item in dates))
        self.assertNotIn(f"{DATE}/{VARIANT}", dates)
        directory = ROOT / "content" / "daily-state" / DATE
        self.assertEqual(
            daily_state.variant_subfolders(str(directory)),
            [VARIANT],
        )

    def test_neon_page_quotes_the_prompt_and_embeds_audio(self):
        loaded = daily_state.load_edition_directory(str(neon_dir()), DATE, variant=VARIANT)
        html = loaded["html"]
        edition = loaded["edition"]
        self.assertEqual(edition["mode"], "audit")
        self.assertIsNone(loaded["qa"])
        self.assertNotIn("semantic_qa", edition)
        self.assertNotIn("status", edition)
        self.assertIs(edition["audit"]["gate"], False)
        self.assertEqual(edition["audit"]["sha256"], ASSET_SHA256["audit/audit.json"])
        self.assertEqual(edition["hashes"]["audit_sha256"], edition["audit"]["sha256"])
        self.assertEqual(
            html.count(f"<h1>{edition['title']}</h1>"),
            1,
        )
        self.assertEqual(edition["title"], "Daily State of AI - 2026-11-20 (Gemini 4 Neon, raw)")
        self.assertEqual(edition["canonical_url"], NEON_URL)
        self.assertEqual(html.count(f'<link rel="canonical" href="{NEON_URL}">'), 1)
        self.assertEqual(html.count(f'<meta property="og:url" content="{NEON_URL}">'), 1)
        self.assertIn(NOTE, html)
        prompt = load_json(neon_dir() / "neon_run.json")["prompts"]["episode"]
        figure = re.search(r'<figure class="ds-prompt">(.*?)</figure>', html, re.S)
        self.assertIsNotNone(figure)
        self.assertIn('<figcaption class="ds-prompt-label">Minimal prompt</figcaption>', figure.group(1))
        pre = re.search(r"<pre>(.*?)</pre>", figure.group(1), re.S).group(1)
        self.assertEqual(html_lib.unescape(pre), prompt)
        self.assertEqual(html.count(f'<audio controls src="{AUDIO}"></audio>'), 1)
        self.assertEqual(html.count(f'<a href="{SHORT}">Short</a>'), 1)
        self.assertEqual(html.count(f'<a href="{SOURCES}">Sources</a>'), 1)
        disclaimer = (
            f'<p class="disclaimer">{HOUSE} · <a href="audit/">Audit</a></p>'
        )
        self.assertEqual(html.count(disclaimer), 1)
        self.assertEqual(html.count(HOUSE), 1)
        self.assertEqual(daily_state.count_ai_labels(html), 1)
        self.assertNotIn("spotify", html.lower())
        self.assertNotIn("semantic_qa", html)
        self.assertIn('href="../../../styles.css"', html)
        self.assertEqual(
            loaded["audit_counts"]["episode"],
            {"PASS": 42, "FAIL": 7, "NEEDS-HUMAN": 8, "ERROR": 0},
        )
        self.assertEqual(
            loaded["audit_counts"]["short"],
            {"PASS": 14, "FAIL": 5, "NEEDS-HUMAN": 3, "ERROR": 0},
        )

    def test_audit_page_opens_failures_and_collapses_the_rest(self):
        loaded = daily_state.load_edition_directory(str(neon_dir()), DATE, variant=VARIANT)
        html = loaded["audit_html"]
        self.assertIn("Episode 42 PASS / 7 FAIL / 8 NEEDS-HUMAN", html)
        self.assertIn("Short 14 PASS / 5 FAIL / 3 NEEDS-HUMAN", html)
        self.assertIn(EXPLANATION, html)
        self.assertIn('href="../../../../styles.css"', html)
        self.assertEqual(html.count(f'<link rel="canonical" href="{AUDIT_URL}">'), 1)
        self.assertEqual(html.count(f'<meta property="og:url" content="{AUDIT_URL}">'), 1)
        blocks = re.findall(r"<details( open)?>(.*?)</details>", html, re.S)
        audit = load_json(neon_dir() / "audit" / "audit.json")
        self.assertEqual(len(blocks), len(audit["results"]))
        by_check = {}
        for open_attr, body in blocks:
            found = [item for item in audit["results"] if item["check_file"] in body]
            self.assertEqual(len(found), 1, body[:80])
            by_check[found[0]["check_file"]] = (open_attr, body)
        open_count = 0
        for item in audit["results"]:
            open_attr, body = by_check[item["check_file"]]
            claim = daily_state.audit_claim_text(item)
            self.assertIn("Claim: " + html_lib.escape(claim, quote=True), body)
            self.assertIn("Result: " + item["status"], body)
            if item["source_quote"] is None:
                self.assertIn("Source quote: (none)", body)
            else:
                quoted = html_lib.escape(item["source_quote"], quote=True)
                self.assertIn("Source quote: " + quoted, body)
            href = daily_state.audit_check_href(DATE, VARIANT, item["check_file"])
            self.assertIn(f'<a href="{href}">{item["check_file"]}</a>', body)
            if item["status"] in daily_state.AUDIT_OPEN_STATUSES:
                self.assertEqual(open_attr, " open")
                open_count += 1
            else:
                self.assertEqual(open_attr, "")
                self.assertIn(item["status"], ("PASS", "NEEDS-HUMAN"))
        self.assertEqual(open_count, 12)

    def test_listing_keeps_the_nov20_row_and_adds_the_variant(self):
        listing = (ROOT / "daily-state" / "index.html").read_text(encoding="utf-8")
        self.assertIn(PRIMARY_ROW + "\n" + NEON_ROW, listing)
        loaded = daily_state.load_editions(str(ROOT))
        files = daily_state.render_output(loaded)
        self.assertEqual(files["daily-state/index.html"], listing)
        self.assertEqual(
            files[f"daily-state/{DATE}/index.html"],
            (ROOT / "daily-state" / DATE / "index.html").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            files[f"daily-state/{DATE}/editors-notes/index.html"],
            (ROOT / "daily-state" / DATE / "editors-notes" / "index.html").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            files[f"daily-state/{DATE}/{VARIANT}/index.html"],
            (ROOT / "daily-state" / DATE / VARIANT / "index.html").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            files[f"daily-state/{DATE}/{VARIANT}/audit/index.html"],
            (ROOT / "daily-state" / DATE / VARIANT / "audit" / "index.html").read_text(encoding="utf-8"),
        )

    def test_live_sources_still_reject_the_snapshot_keys(self):
        sources = load_json(neon_dir() / "sources.json")
        daily_state.validate_sources(sources, DATE, len(sources["urls"]), audit=True)
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.validate_sources(sources, DATE, len(sources["urls"]))
        self.assertIn("unknown schema: sources.json", str(caught.exception))

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dest = Path(tmp.name) / "content" / "daily-state" / LIVE_DATE
        dest.parent.mkdir(parents=True)
        dest.mkdir()
        source = ROOT / "content" / "daily-state" / LIVE_DATE
        for name in daily_state.CONTENT_FILES:
            shutil.copyfile(source / name, dest / name)
        path = dest / "sources.json"
        document = load_json(path)
        document["stories"][0]["verification_status"] = "preliminary"
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.load_edition(tmp.name, LIVE_DATE)
        self.assertIn("unknown schema: story", str(caught.exception))

    def test_unknown_entries_still_hold(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dest = Path(tmp.name) / "content" / "daily-state" / LIVE_DATE
        dest.parent.mkdir(parents=True)
        dest.mkdir()
        source = ROOT / "content" / "daily-state" / LIVE_DATE
        for name in daily_state.CONTENT_FILES:
            shutil.copyfile(source / name, dest / name)
        (dest / "side").mkdir()
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.load_edition(tmp.name, LIVE_DATE)
        self.assertIn("frozen public inputs", str(caught.exception))
        (dest / "side").rmdir()
        (dest / "neon").write_text("not a directory\n", encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.list_edition_dates(tmp.name)
        self.assertIn("unexpected content entry: neon", str(caught.exception))

    def test_a_wrong_audit_count_or_a_qa_file_holds(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dest = Path(tmp.name) / DATE / VARIANT
        shutil.copytree(neon_dir(), dest)
        edition_path = dest / "edition.json"
        edition = load_json(edition_path)
        edition["audit"]["episode"]["FAIL"] = 8
        edition_path.write_text(json.dumps(edition, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.load_edition_directory(str(dest), DATE, variant=VARIANT)
        self.assertIn("counts do not match", str(caught.exception))

        edition["audit"]["episode"]["FAIL"] = 7
        edition["semantic_qa"] = "pass"
        edition_path.write_text(json.dumps(edition, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.load_edition_directory(str(dest), DATE, variant=VARIANT)
        self.assertIn("unknown schema: edition.json", str(caught.exception))

        edition.pop("semantic_qa")
        edition_path.write_text(json.dumps(edition, indent=2) + "\n", encoding="utf-8")
        (dest / "qa.json").write_text('{"status": "ok"}\n', encoding="utf-8")
        with self.assertRaises(daily_state.Hold) as caught:
            daily_state.load_edition_directory(str(dest), DATE, variant=VARIANT)
        self.assertIn("frozen public inputs", str(caught.exception))

    def test_package_check_accepts_audit_and_refuses_the_other_pipelines(self):
        ok = daily_state.main(["--package", str(neon_dir()), "--check"])
        self.assertEqual(ok, 0)
        for pipeline in ("live", "editor"):
            code = daily_state.main([
                "--package", str(neon_dir()), "--check", "--pipeline", pipeline,
            ])
            self.assertEqual(code, 1, pipeline)


if __name__ == "__main__":
    unittest.main()
