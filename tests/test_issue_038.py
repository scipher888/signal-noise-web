"""Issue 38: the verbatim machine question outside the frozen prose, no corrective note above the author essay,
and a source page that reproduces the published brain dump."""

import hashlib
import html
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

AUTHOR = ROOT / "p/the-smartest-people-in-the-room-are-the-easiest-to-fool/index.html"
MACHINE = ROOT / "p/what-intelligence-cant-tell-you-about-your-own-life/index.html"
SOURCE = ROOT / "p/issue-038-source-material/index.html"
# sha256 of the published brain dump (verbatim except the removed private link
# and the stripped X tracking parameters).
SOURCE_SHA256 = "78c9c61cdbf7cb233c22d4a90ee39bac9845fbd052731ffa17f137aeb8935faa"
Q = "To what extent, if any, does intelligence help people make wise life choices involving needs, wants, desires, and emotions? And what, if anything, does that imply about how highly intelligent people should approach these decisions that can have a major impact on their quality of life?"


class Issue38(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build()

    def test_question_verbatim_before_body(self):
        self.assertEqual(build.MACHINE_QUESTIONS[38][0], Q)
        page = MACHINE.read_text(encoding="utf-8")
        aside = re.search(r'<aside class="mq".*?</aside>', page, re.S).group(0)
        self.assertIn(f'<p class="mq-question">{html.escape(Q)}</p>', aside)
        self.assertIn("The question given to the AI:", aside)
        self.assertLess(page.index("</aside>"), page.index("<p>Intelligence, in the sense that IQ tests measure"))

    def test_author_page_has_no_corrective_note(self):
        # Ruling A, audit only: the corrections live in the audit, not above the essay.
        page = AUTHOR.read_text(encoding="utf-8")
        self.assertNotIn("ednote", page)
        self.assertNotIn("Editor&rsquo;s note", page)
        self.assertNotIn("suspected of being a Chinese spy", page)
        self.assertNotIn('<aside class="mq"', page)
        # the audit stays linked from the companion nav
        nav = re.search(r'<nav class="cnav top".*?</nav>', page, re.S).group(0)
        self.assertIn("signal-noise-audit-snapshot/issues/issue-038/", nav)
        # the frozen wording is untouched, including the approved phrase
        self.assertIn("subcultures among staffers at top AI labs", page)
        self.assertNotIn("staffers at OpenAI", page)
        self.assertLess(page.index('<p class="dek">'), page.index("<p>We like to believe"))

    def test_source_text_published_version(self):
        page = SOURCE.read_text(encoding="utf-8")
        mix = re.search(r'<div class="src-mix">(.*?)</div>', page, re.S).group(1)
        text = html.unescape(re.sub(r"<[^>]+>", "", mix))
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), SOURCE_SHA256)
        self.assertIn("[private link removed]", text)
        for bad in ("dropbox.com", "rlkey=", "?a=", "s=46"):
            self.assertNotIn(bad, page)

    def test_source_leaf_name(self):
        href = "https://www.signalandnoise.email/p/issue-038-source-material/"
        expected = (
            f'<p class="essay-sources"><span class="essay-sources-label">Sources</span>'
            f' <a href="{href}">Source material</a></p>'
        )
        for p in (AUTHOR, MACHINE):
            page = p.read_text(encoding="utf-8")
            navs = re.findall(r'<nav class="cnav[^"]*".*?</nav>', page, re.S)
            self.assertTrue(navs)
            for nav in navs:
                self.assertNotIn("Source material", nav)
                self.assertNotIn("Written without AI", nav)
            self.assertIn(expected, page)
            body_end = page.index(expected)
            foot = page.index('<nav class="cnav" aria-label="Issue 38 companions">')
            self.assertLess(body_end, foot)
        source = SOURCE.read_text(encoding="utf-8")
        source_navs = re.findall(r'<nav class="cnav[^"]*".*?</nav>', source, re.S)
        self.assertTrue(source_navs)
        for nav in source_navs:
            self.assertNotIn("Source material", nav)
            self.assertNotIn("Written without AI", nav)
        self.assertNotIn("essay-sources", source)

    def test_audio_companions(self):
        a = "https://open.spotify.com/episode/5OFFH1zNdvsnvBcVFcC9MT"
        m = "https://open.spotify.com/episode/7dHpfFFhp5RkpHi1R9QKgX"
        for p in (AUTHOR, MACHINE):
            page = p.read_text(encoding="utf-8")
            for nav in re.findall(r'<nav class="cnav[^"]*".*?</nav>', page, re.S):
                self.assertIn(f'<a href="{a}">Audio companion</a>', nav)
                self.assertIn(f'<a href="{m}">Audio companion</a>', nav)
            self.assertEqual(page.count("Audio companion"), 4)
            self.assertNotIn("open.spotify.com/embed", page)
        src = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("Audio companion", src)
        self.assertNotIn(a, src)
        self.assertNotIn(m, src)

if __name__ == "__main__":
    unittest.main()
