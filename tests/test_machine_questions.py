"""Origin notes on machine essays 34–36. Exact questions; frozen prose stays put."""

import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

# Approved questions. Issue 36 uses an em dash, not a hyphen.
QUESTIONS = {
    34: (
        "What single element is most vital to protecting humanity's "
        "long-term quality of life? What primary action should we take to safeguard it?"
    ),
    35: "What is the best strategy to optimize weight (prevent weight gain) without medications?",
    36: (
        "What core alignment failures do everyday users currently encounter when "
        "interacting with agentic AI systems, and what implications do these practical "
        "misalignments have for future alignment frameworks\u2014specifically regarding "
        "the balance between user intent, safety guardrails, and broader moral frameworks?"
    ),
}

MACHINE = {
    34: "the-machinery-of-being-wrong",
    35: "the-long-game-of-not-gaining",
    36: "alignment-at-human-scale",
}
AUTHOR = {
    34: "we-are-arguing-about-the-speed-of-ai-we-have-no-plan-for-the-crash",
    35: "stop-trying-to-out-willpower-your-appetite-stuff-it-into-submission-instead",
    36: "my-son-his-calorie-tracker-and-the-tyranny-of-the-nanny-bot",
}
UNAIDED = {
    34: "nothing-matters-more-than-civilization",
    35: "what-is-the-best-strategy-to-optimize-weight-prevent-weight-gain-without-medications",
    36: "issue-036-written-without-ai",
}

AUDIT = "https://scipher888.github.io/signal-noise-audit-snapshot/issues"
FULL_PROMPT = {
    34: f"{AUDIT}/issue-034/development/",
    35: f"{AUDIT}/issue-035/development/",
    36: f"{AUDIT}/issue-036/development/#machine-question",
}


class AsideText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._in = None
        self.parts = []
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "aside" and ad.get("class") == "mq":
            self._in = "aside"
        if self._in and tag == "a":
            self.hrefs.append(ad.get("href"))
        if self._in and tag == "p":
            self._in = ad.get("class") or "p"
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "p" and self._in and self._in != "aside":
            self.parts.append((self._in, "".join(self._buf)))
            self._in = "aside"
        if tag == "aside":
            self._in = None

    def handle_data(self, data):
        if self._in and self._in != "aside":
            self._buf.append(data)


def page(slug):
    return (ROOT / "p" / slug / "index.html").read_text(encoding="utf-8")


class MachineQuestionTests(unittest.TestCase):
    def test_builder_quotes_are_the_approved_questions(self):
        for issue, question in QUESTIONS.items():
            stored, _meta = build.MACHINE_QUESTIONS[issue]
            self.assertEqual(stored, question)
            self.assertNotIn("machine-seed", build.MACHINE_QUESTIONS[issue][1])
            self.assertNotIn("leak-check", build.MACHINE_QUESTIONS[issue][1])

    def test_machine_pages_quote_the_question_outside_the_frozen_body(self):
        for issue, slug in MACHINE.items():
            html = page(slug)
            _title, dek_html, body = build.load_source(
                build.resolve_source(build.SIDE_PAGES[slug][2]), slug)
            self.assertIn(body, html)
            self.assertNotIn("The question given to the AI", body)
            self.assertIn(build.machine_question_html(issue), html)
            # The note is before the essay, and the essay bytes are untouched.
            self.assertLess(html.index('class="mq"'), html.index(body))
            parsed = AsideText()
            parsed.feed(html)
            classes = [cls for cls, _text in parsed.parts]
            self.assertEqual(classes, ["mq-label", "mq-question", "mq-meta"])
            by_class = dict(parsed.parts)
            self.assertEqual(by_class["mq-label"], "The question given to the AI:")
            self.assertEqual(by_class["mq-question"], QUESTIONS[issue])
            self.assertEqual(parsed.hrefs[0], FULL_PROMPT[issue])
            self.assertIn(dek_html, html)
            self.assertEqual(html.count('class="mq"'), 1)
            # Companion audio still sits on both navs.
            self.assertEqual(html.count(build.AUDIO[issue]), 2)
            self.assertEqual(html.count(build.MACHINE_AUDIO[issue]), 2)
            self.assertNotIn("?", build.AUDIO[issue])

    def test_issue_facts_are_specific(self):
        notes = {n: build.MACHINE_QUESTIONS[n][1] for n in (34, 35, 36)}
        self.assertIn("not one unchanged generation", notes[34])
        self.assertIn("second Opus run plus one paragraph from the first", notes[34])
        self.assertIn("returned Opus essay was not edited", notes[35])
        self.assertIn("Astra essay unchanged", notes[36])
        self.assertIn(f"{AUDIT}/issue-036/source/metadata/isolation.json", notes[36])
        self.assertIn("no author essay", notes[36])

    def test_author_unaided_feed_and_archive_stay_clear_of_the_note(self):
        for issue in (34, 35, 36):
            for slug in (AUTHOR[issue], UNAIDED[issue]):
                html = page(slug)
                self.assertNotIn('class="mq"', html)
                self.assertNotIn(build.machine_question_html(issue), html)
        feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
        archive = (ROOT / "archive" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("The question given to the AI", feed)
        self.assertNotIn("The question given to the AI", archive)
        self.assertNotIn('class="mq"', archive)


if __name__ == "__main__":
    unittest.main()
