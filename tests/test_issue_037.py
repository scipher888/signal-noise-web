"""Issue 37: two verbatim machine questions, an editor's note outside the prose,
and a source page whose verbatim text is marked by author."""

import hashlib
import html
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

MACHINE = ROOT / "p/where-the-starship-catch-ranks-and-what-it-could-change/index.html"
AUTHOR = ROOT / "p/what-spacex-caught-in-those-mechanical-arms-is-bigger-than-a-rocket/index.html"
SOURCE = ROOT / "p/issue-037-source-material/index.html"
# sha256 of the author's source text (brain dump + Grok Heavy), byte-for-byte.
SOURCE_SHA256 = "7bc92f1e095b06ec03881eef0f3b09ef6dc69e02814cca3298afccff929243ba"
# The author's own passages, verbatim (typos kept).
HUMAN = [
    "The successful capture of Starship Fight 15 is the #1 greatest engineering achievement of all time",
    "For context, I would rank the following to round out the top 5 achievements:",
    "But who cares? What does proof of concept of fully reusable large payload spaceships of imply about your future?",
    "I\u2019m so glad you asked.",
]
Q = (
    "1. Please rank in order the greatest engineering achievements of all time based solely on the magnitude of the engineering/technological challenge and assuming modern (2026-era) technology, materials, computing, simulation, and manufacturing could be applied to al of them - and keep ranking them until you can place the successful capture of Starship Fight 15 (happened today - on 11/14/2026) somewhere in this list.",
    "2. Taking on optimistic but realistic/possible view, what does this proof of concept of fully reusable large payload spaceships imply about the future for ordinary people over the next 10, 25, 50, and 100 years?",
)


class Issue37(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build.build()

    def test_questions_verbatim(self):
        self.assertEqual(build.MACHINE_QUESTIONS[37][0], Q)
        page = MACHINE.read_text(encoding="utf-8")
        aside = re.search(r'<aside class="mq".*?</aside>', page, re.S).group(0)
        for q in Q:
            self.assertIn(f'<p class="mq-question">{html.escape(q)}</p>', aside)
        self.assertIn("The questions given to the AI:", aside)

    def test_editor_note_outside_prose_and_before_body(self):
        page = MACHINE.read_text(encoding="utf-8")
        aside_end = page.index("</aside>")
        self.assertIn("Editor&rsquo;s note", page[:aside_end])
        self.assertIn("space.com", page[:aside_end])
        self.assertLess(page.index('<p class="dek">'), page.index('<aside class="mq"'))
        self.assertLess(aside_end, page.index("<p>Judged purely by difficulty"))
        # the model's own caveat is still in the prose, unchanged
        self.assertIn("I can't independently confirm the flight", page)

    def test_source_text_verbatim(self):
        page = SOURCE.read_text(encoding="utf-8")
        mix = re.search(r'<div class="src-mix">(.*?)</div>', page, re.S).group(1)
        text = html.unescape(re.sub(r"<[^>]+>", "", mix))
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), SOURCE_SHA256)

    def test_human_passages_marked(self):
        page = SOURCE.read_text(encoding="utf-8")
        spans = [html.unescape(s) for s in re.findall(r'<span class="src-h">(.*?)</span>', page, re.S)]
        for h in HUMAN:
            self.assertIn(h, spans)
        self.assertTrue(any(s.startswith("In short, Elon Musk has repeatedly told audiences to read Ian Banks culture series.") for s in spans))
        self.assertEqual(len(spans), 5)

    def test_source_leaf_name(self):
        for p in (AUTHOR, SOURCE):
            nav = re.search(r'<nav class="cnav top".*?</nav>', p.read_text(encoding="utf-8"), re.S).group(0)
            self.assertIn("Source material", nav)
            self.assertNotIn("Written without AI", nav)


if __name__ == "__main__":
    unittest.main()
