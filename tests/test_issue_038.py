"""Issue 38: the verbatim machine question, editor's notes outside the frozen prose,
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

    def test_author_note_outside_prose_and_before_body(self):
        page = AUTHOR.read_text(encoding="utf-8")
        aside = re.search(r'<aside class="mq ednote".*?</aside>', page, re.S).group(0)
        for s in ("Editor&rsquo;s note", "resigned as Nvidia&rsquo;s CEO on November 12, 2026",
                  "suspected of being a Chinese spy", "an Anthropic researcher", "issue-038/#audit"):
            self.assertIn(s, aside)
        self.assertLess(page.index('<p class="dek">'), page.index('<aside class="mq ednote"'))
        self.assertLess(page.index("</aside>"), page.index("<p>We like to believe"))
        # the frozen wording is untouched, including the approved phrase
        self.assertIn("subcultures among staffers at top AI labs", page)
        self.assertNotIn("staffers at OpenAI", page)

    def test_source_text_published_version(self):
        page = SOURCE.read_text(encoding="utf-8")
        mix = re.search(r'<div class="src-mix">(.*?)</div>', page, re.S).group(1)
        text = html.unescape(re.sub(r"<[^>]+>", "", mix))
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), SOURCE_SHA256)
        self.assertIn("[private link removed]", text)
        for bad in ("dropbox.com", "rlkey=", "?a=", "s=46"):
            self.assertNotIn(bad, page)

    def test_source_leaf_name(self):
        for p in (AUTHOR, SOURCE):
            nav = re.search(r'<nav class="cnav top".*?</nav>', p.read_text(encoding="utf-8"), re.S).group(0)
            self.assertIn("Source material", nav)
            self.assertNotIn("Written without AI", nav)

    def test_no_audio_yet(self):
        for p in (AUTHOR, MACHINE, SOURCE):
            self.assertNotIn("Audio companion", p.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
