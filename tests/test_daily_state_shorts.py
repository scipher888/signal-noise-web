"""Site-hosted daily and audit shorts lead the edition page and the listing. No network."""

import json
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
from test_daily_neon_edition import (  # noqa: E402
    DATE, HOUSE, MP4, SPOTIFY_ANCHOR, X_AUDIT_SHORT, X_SHORT, Repo, sha,
)

DAILY_SRC = f"/content/daily-state/{DATE}/daily-short.mp4"
AUDIT_SRC = f"/content/daily-state/{DATE}/audit-short.mp4"
AUDIT_MP4 = MP4 + b"audit"


class HostedShortsTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.assertEqual(self.repo.build(short=False), 0)
        self.daily = self.repo.root / "daily.mp4"
        self.daily.write_bytes(MP4)
        self.audit = self.repo.root / "audit.mp4"
        self.audit.write_bytes(AUDIT_MP4)

    def tearDown(self):
        self.repo.close()

    def run_tool(self, *argv):
        with mock.patch.object(neon_edition, "REPO", str(self.repo.root)):
            return neon_edition.main(list(argv))

    def set_both(self):
        self.assertEqual(self.run_tool(
            "set-short-url", "--date", DATE, "--url", X_SHORT, "--mp4", str(self.daily)), 0)
        self.assertEqual(self.run_tool(
            "set-audit-short-url", "--date", DATE, "--url", X_AUDIT_SHORT, "--mp4", str(self.audit)), 0)

    def page(self):
        return (self.repo.root / "daily-state" / DATE / "index.html").read_text(encoding="utf-8")

    def edition(self):
        return json.loads((self.repo.edition_dir() / "edition.json").read_text())

    def test_edition_page_leads_with_both_shorts_then_links_then_report(self):
        self.set_both()
        page = self.page()
        daily = page.index(f'src="{DAILY_SRC}"')
        audit = page.index(f'src="{AUDIT_SRC}"')
        row = page.index('<p class="ds-links">')
        label = page.index(f'<p class="disclaimer">{HOUSE}</p>')
        report = page.index('id="report"')
        script = page.index('<div class="script">')
        self.assertLess(page.index("<h1>"), daily)
        self.assertTrue(daily < audit < row < label < report < script)
        self.assertEqual(page.count('<video controls playsinline preload="metadata"'), 2)
        self.assertEqual(page.count(f'<a href="{X_SHORT}">Watch on X</a>'), 1)
        self.assertEqual(page.count(f'<a href="{X_AUDIT_SHORT}">Watch on X</a>'), 1)
        self.assertIn(
            f'<p class="ds-links"><a href="#report">Written report</a> · {SPOTIFY_ANCHOR}'
            ' · <a href="audit/">Audit</a></p>', page)
        # The 11:15 routine's checks.
        self.assertEqual(page.count(HOUSE), 1)
        self.assertEqual(page.count('<a href="audit/">Audit</a>'), 1)
        self.assertEqual(page.count("Audio on Spotify"), 1)
        self.assertNotIn(">Short</a>", page)
        self.assertNotIn(">Audit short</a>", page)
        self.assertIn('<section class="sources">', page)

    def test_videos_are_copied_unchanged_and_hashed(self):
        self.set_both()
        directory = self.repo.edition_dir()
        self.assertEqual((directory / "daily-short.mp4").read_bytes(), MP4)
        self.assertEqual((directory / "audit-short.mp4").read_bytes(), AUDIT_MP4)
        hashes = self.edition()["hashes"]
        self.assertEqual(hashes["daily_short_sha256"], sha(MP4))
        self.assertEqual(hashes["audit_short_sha256"], sha(AUDIT_MP4))
        self.assertEqual(self.edition()["video_url"], X_SHORT)

    def test_rerun_is_a_noop(self):
        self.set_both()
        edition = (self.repo.edition_dir() / "edition.json").read_bytes()
        page = self.page()
        self.set_both()
        self.assertEqual((self.repo.edition_dir() / "edition.json").read_bytes(), edition)
        self.assertEqual(self.page(), page)

    def test_different_bytes_for_a_published_short_are_refused(self):
        self.set_both()
        before = (self.repo.edition_dir() / "edition.json").read_bytes()
        self.daily.write_bytes(MP4 + b"changed")
        self.assertEqual(self.run_tool(
            "set-short-url", "--date", DATE, "--url", X_SHORT, "--mp4", str(self.daily)), 1)
        self.assertEqual((self.repo.edition_dir() / "edition.json").read_bytes(), before)
        self.assertEqual((self.repo.edition_dir() / "daily-short.mp4").read_bytes(), MP4)

    def test_oversize_or_broken_mp4_is_refused_without_writing(self):
        before = (self.repo.edition_dir() / "edition.json").read_bytes()
        with mock.patch.object(neon_edition, "MAX_SHORT_BYTES", 10):
            self.assertEqual(self.run_tool(
                "set-short-url", "--date", DATE, "--url", X_SHORT, "--mp4", str(self.daily)), 1)
        self.daily.write_bytes(b"not a video at all, no box header here")
        self.assertEqual(self.run_tool(
            "set-short-url", "--date", DATE, "--url", X_SHORT, "--mp4", str(self.daily)), 1)
        self.assertEqual((self.repo.edition_dir() / "edition.json").read_bytes(), before)
        self.assertFalse((self.repo.edition_dir() / "daily-short.mp4").exists())

    def test_tampered_short_holds(self):
        self.set_both()
        (self.repo.edition_dir() / "audit-short.mp4").write_bytes(AUDIT_MP4 + b"x")
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_hash_without_file_holds(self):
        edition = self.edition()
        edition["hashes"]["daily_short_sha256"] = sha(MP4)
        (self.repo.edition_dir() / "edition.json").write_text(json.dumps(edition))
        with self.assertRaises(daily_state.Hold):
            self.repo.load()

    def test_audit_short_without_hosted_mp4_falls_back_to_the_x_link(self):
        self.assertEqual(self.run_tool(
            "set-short-url", "--date", DATE, "--url", X_SHORT, "--mp4", str(self.daily)), 0)
        self.assertEqual(self.run_tool(
            "set-audit-short-url", "--date", DATE, "--url", X_AUDIT_SHORT), 0)
        page = self.page()
        self.assertEqual(page.count("<video "), 1)
        self.assertIn(
            f'<a href="audit/">Audit</a> · <a href="{X_AUDIT_SHORT}">Audit short</a></p>', page)

    def test_without_hosted_shorts_the_old_layout_stays(self):
        self.assertEqual(self.run_tool("set-short-url", "--date", DATE, "--url", X_SHORT), 0)
        page = self.page()
        self.assertNotIn("<video", page)
        self.assertNotIn("ds-shorts", page)
        self.assertIn(f'{SPOTIFY_ANCHOR} · <a href="{X_SHORT}">Short</a>', page)
        listing = (self.repo.root / "daily-state" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("ds-latest", listing)

    def test_listing_leads_with_the_latest_shorts_then_the_list(self):
        self.set_both()
        listing = (self.repo.root / "daily-state" / "index.html").read_text(encoding="utf-8")
        daily = listing.index(f'src="{DAILY_SRC}"')
        audit = listing.index(f'src="{AUDIT_SRC}"')
        row = listing.index('<p class="ds-links">')
        month = listing.index("<h2>November 2026</h2>")
        self.assertTrue(daily < audit < row < month)
        self.assertIn(f'<a href="{DATE}/#report">Written report</a>', listing)
        self.assertIn(f'<a href="{DATE}/audit/">Audit</a>', listing)
        self.assertEqual(listing.count(SPOTIFY_ANCHOR), 1)
        self.assertEqual(listing, daily_state.render_listing_html(
            daily_state.load_editions(str(self.repo.root))))


class PublishedShortsTest(unittest.TestCase):
    """The live repo: 2026-11-25 leads with both hosted shorts; older pages are untouched."""

    def test_2026_11_25_page(self):
        loaded = daily_state.load_edition(str(ROOT), "2026-11-25")
        self.assertEqual(set(loaded["shorts"]), {"daily", "audit"})
        page = loaded["html"]
        self.assertLess(page.index("daily-short.mp4"), page.index("audit-short.mp4"))
        self.assertEqual(page.count(HOUSE), 1)

    def test_legacy_short_mp4_never_switches_the_layout(self):
        loaded = daily_state.load_edition(str(ROOT), "2026-11-22")
        self.assertEqual(loaded["shorts"], {})
        self.assertNotIn("<video", loaded["html"])


if __name__ == "__main__":
    unittest.main()
