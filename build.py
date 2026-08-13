#!/usr/bin/env python3
"""Signal & Noise — static essay site builder (wave 3, beehiiv extrication).

Fidelity by construction: essay bodies are the repo's as-published paste/final
sources wrapped in the site template, never retyped. `--check` verifies every
built page still contains its source body byte-for-byte (after the same
normalization the wrap applies).

Dates policy (no fabrication): exact dates only where an as-published byline or
the publication record states one; month-year where the origin pages state it;
bare "2026" otherwise. J's beehiiv export upgrades the coarse ones later.

Run:    python3 build.py            # writes the site into ./ (docs at repo root)
        python3 build.py --check    # fidelity verification, exit 1 on any drift
"""

import html
import os
import re
import sys

import markdown  # available on this machine; used only for issues 1-3 (md sources)

SRC = os.path.expanduser("~/Code/signal-noise/projects/newsletter")
OUT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.signalandnoise.email"  # flipped at CNAME cutover 2026-08-12
AUDIT_BASE = "https://scipher888.github.io/signal-noise-audit-snapshot/issues"

# slug -> (issue_no|None for companions, source path relative to SRC, date, date_precision)
# date_precision: "day" (as-published byline or publication record), "month" (origin page), "year"
MANIFEST = {
    "is-it-possible-to-be-a-good-person-on-x-d0fc": (1, "past-issues/issue-001-final.md", "2026-03-07", "day"),
    "can-you-fake-it": (2, "past-issues/issue-002-final.md", "2026", "year"),
    "the-accessibility-illusion": (3, "past-issues/issue-003-final.md", "2026", "year"),
    "the-coherence-illusion": (4, "past-issues/issue-004-paste.html", "2026", "year"),
    "what-we-changed-after-issue-4": (None, "past-issues/issue-004-companion-paste.html", "2026", "year"),
    "the-ai-that-tells-you-what-you-want-to-hear": (5, "past-issues/issue-005-paste.html", "2026", "year"),
    "the-homer-car-problem": (6, "past-issues/issue-006-paste.html", "2026", "year"),
    "when-help-becomes-harm": (7, "past-issues/issue-007-paste.html", "2026", "year"),
    "regret-as-raw-material": (8, "past-issues/issue-008-paste.html", "2026", "year"),
    "what-changed-after-issue-8": (None, "process-notes/what-changed-after-issue-8-paste.html", "2026", "year"),
    "when-right-most-of-the-time-makes-wrong-harder-to-catch": (9, "past-issues/issue-009-paste.html", "2026", "year"),
    "when-everything-sounds-insightful-nothing-sounds-trustworthy": (10, "past-issues/issue-010-paste.html", "2026-05-10", "day"),
    "when-words-arrive-without-a-world": (11, "past-issues/issue-011-paste.html", "2026", "year"),
    "the-world-behind-the-words": (12, "past-issues/issue-012-paste.html", "2026", "year"),
    "when-conscience-has-a-payroll": (13, "past-issues/issue-013-paste.html", "2026", "year"),
    "am-i-building": (14, "past-issues/issue-014-paste.html", "2026-06", "month"),
    "the-appeal-button": (15, "past-issues/issue-015-paste.html", "2026-06", "month"),
    "the-gary-marcus-audit": (16, "drafts/issue-016-paste.html", "2026-06", "month"),
    "when-the-accusation-becomes-the-agenda": (17, "drafts/issue-017-paste.html", "2026-06", "month"),
    "principle-and-process": (18, "drafts/issue-018-beehiiv-web-update-v0.10.html", "2026-07-04", "day"),
    "unseen-and-unenforced": (19, "drafts/issue-019-beehiiv-paste-2026-07-11.html", "2026-07-11", "day"),
    "who-has-to-check-the-ai-in-your-medical-record": (20, "drafts/issue-020-beehiiv-paste-2026-07-19-rev.html", "2026-07-19", "day"),
    "delivered-then-invisible": (21, "drafts/issue-021-beehiiv-paste-2026-07-25.html", "2026-07-25", "day"),
    "the-price-of-being-read": (22, "drafts/issue-022-postW-web-paste-2026-08-01.html", "2026-08-01", "day"),
    "ai-can-hallucinate-a-jury": (23, "drafts/issue-023-postW-web-paste-2026-08-09.html", "2026-08-09", "day"),
}

# Sources whose title/dek live outside the body (beehiiv field lines / build comments).
FIELD_OVERRIDES = {
    "principle-and-process": ("Principle and Process", "Two levels of the birthright citizenship debate"),
}

MONTHS = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May",
          "06": "June", "07": "July", "08": "August", "09": "September",
          "10": "October", "11": "November", "12": "December"}


def display_date(date, precision):
    if precision == "day":
        y, m, d = date.split("-")
        return f"{MONTHS[m]} {int(d)}, {y}"
    if precision == "month":
        y, m = date.split("-")
        return f"{MONTHS[m]} {y}"
    return date  # "2026"


def load_source(path, slug=None):
    """Return (title, dek_html, body_html) from a paste/final source.

    HTML sources: strip a leading <meta charset> line; title = first h1/h2;
    dek = a <p><em>...</em></p> immediately following the title (whole paragraph
    italic only); body = everything after the title (dek included — it is part
    of the published body).
    Markdown sources (issues 1-3): byline/footer scaffolding above the first
    "---" is dropped (title/dek are re-set in the template); body = markdown
    below, converted once.
    """
    raw = open(path, encoding="utf-8").read()
    if path.endswith(".md"):
        title = None
        dek = None
        lines = raw.split("\n")
        body_start = 0
        for i, line in enumerate(lines[:20]):
            s = line.strip()
            if s.startswith("## ") and (title is None or title.startswith("Signal & Noise")):
                title = s[3:].strip()  # real title when "# " was the issue-number header
            elif title is None and s.startswith("# "):
                title = s[2:].strip()
            elif title and dek is None and re.fullmatch(r"\*[^*].*\*", s):
                dek = s.strip("*")
            elif s == "---":
                body_start = i + 1
                break
        body_md = "\n".join(lines[body_start:])
        body = markdown.markdown(body_md, extensions=["extra"])
        dek_html = f"<p class=\"dek\"><em>{html.escape(dek)}</em></p>" if dek else ""
        return title, dek_html, body

    # html sources
    # beehiiv "HTML snippet" blocks were rendered as real HTML on the live page —
    # unescape them so our page shows what readers saw, not the escaped source.
    def unsnippet(m):
        return html.unescape(m.group(1))
    raw = re.sub(r"<pre data-type=\"htmlSnippet\"><code>(.*?)</code></pre>", unsnippet, raw, flags=re.S)

    if slug in FIELD_OVERRIDES:
        title, dek = FIELD_OVERRIDES[slug]
        dek_html = f"<p class=\"dek\"><em>{html.escape(dek)}</em></p>"
        return title, dek_html, raw.strip()

    if raw.lstrip().startswith("<!--"):
        # postW pastes: title/dek live in the build comment (beehiiv field values)
        cm = re.match(r"\s*<!--(.*?)-->", raw, re.S)
        comment = cm.group(1)
        tm = re.search(r"Beehiiv title field:\s*(.*?)\s*\|", comment)
        dm2 = re.search(r"Beehiiv subtitle (?:AND SEO description fields, both identical|field):\s*(.*?)\s*\|", comment)
        if not (tm and dm2):
            raise SystemExit(f"could not parse field comment in {path}")
        title = tm.group(1).strip()
        dek = dm2.group(1).strip()
        body = raw[cm.end():].strip()
        dek_html = f"<p class=\"dek\"><em>{html.escape(dek)}</em></p>"
        return title, dek_html, body

    text = re.sub(r"^\s*<meta charset[^>]*>\s*", "", raw)
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", text, re.S)
    if not m:
        raise SystemExit(f"no title heading in {path}")
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    title = html.unescape(title)
    body = text[m.end():].strip()
    dm = re.match(r"\s*<p><em>(.*?)</em></p>", body, re.S)
    dek_html = f"<p class=\"dek\"><em>{dm.group(1)}</em></p>" if dm else ""
    if dm:
        body = body[dm.end():].strip()
    return title, dek_html, body


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Signal &amp; Noise</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="{root}styles.css">
  <link rel="alternate" type="application/rss+xml" title="Signal &amp; Noise" href="{root}feed.xml">
  <link rel="icon" href="{root}assets/mark.svg">
</head>
<body>
<header class="site-head">
  <a class="masthead" href="{root}">Signal &amp; Noise</a>
  <nav><a href="{root}archive/">Archive</a> <a href="{root}about/">About</a></nav>
</header>
<main>
{main}
</main>
<footer class="site-foot">
  <p>Signal &amp; Noise is written under the pen name Synthia Cipher. AI tools draft and critique; the human author owns the editorial judgment, final wording, published claims, and errors.</p>
  <p><a href="{root}">Home</a> · <a href="{root}archive/">Archive</a> · <a href="{root}about/">About</a> · <a href="{root}feed.xml">RSS</a> · <a href="https://scipher888.github.io/signal-noise-audit-snapshot/world/">The World Behind the Words</a></p>
</footer>
</body>
</html>
"""


def essay_page(slug, issue, title, dek_html, body, date, precision):
    kicker = f"Issue {issue}" if issue else "Process note"
    dateline = display_date(date, precision)
    audit = ""
    if issue:
        audit = (f"\n<aside class=\"audit-link\"><p>The published record of what checking found for this piece — "
                 f"objections, changes, and what could not be checked — is in "
                 f"<a href=\"{AUDIT_BASE}/issue-{issue:03d}/\">The World Behind the Words</a>.</p></aside>")
    main = (f"<article>\n<p class=\"kicker\">{kicker} · {dateline}</p>\n"
            f"<h1>{html.escape(title)}</h1>\n{dek_html}\n{body}\n{audit}\n</article>")
    desc = re.sub(r"<[^>]+>", "", dek_html).strip() or f"Signal & Noise — {title}"
    return PAGE.format(title=html.escape(title), desc=html.escape(desc, quote=True), root="../../", main=main)


def build():
    entries = []
    for slug, (issue, rel, date, precision) in MANIFEST.items():
        path = os.path.join(SRC, rel)
        title, dek_html, body = load_source(path, slug)
        entries.append(dict(slug=slug, issue=issue, title=title, dek=re.sub(r"<[^>]+>", "", dek_html).strip(),
                            dek_html=dek_html, body=body, date=date, precision=precision, src=rel))
        d = os.path.join(OUT, "p", slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            essay_page(slug, issue, title, dek_html, body, date, precision))

    essays = sorted([e for e in entries if e["issue"]], key=lambda e: e["issue"], reverse=True)
    companions = [e for e in entries if not e["issue"]]

    # archive
    rows = []
    for e in essays:
        rows.append(f"<p class=\"row\"><a href=\"../p/{e['slug']}/\">{html.escape(e['title'])}</a> "
                    f"<span class=\"meta\">Issue {e['issue']} · {display_date(e['date'], e['precision'])}</span>"
                    + (f"<span class=\"line\">{html.escape(e['dek'])}</span>" if e["dek"] else "") + "</p>")
    comp_rows = [f"<p class=\"row\"><a href=\"../p/{e['slug']}/\">{html.escape(e['title'])}</a> "
                 f"<span class=\"meta\">Process note</span></p>" for e in companions]
    archive_main = ("<h1>Archive</h1>\n<p class=\"intro\">Every issue, newest first. Each piece links its published "
                    "audit in The World Behind the Words.</p>\n" + "\n".join(rows)
                    + "\n<h2>Process notes</h2>\n" + "\n".join(comp_rows))
    os.makedirs(os.path.join(OUT, "archive"), exist_ok=True)
    open(os.path.join(OUT, "archive", "index.html"), "w", encoding="utf-8").write(
        PAGE.format(title="Archive", desc="Every Signal & Noise issue, newest first.", root="../", main=archive_main))

    # home
    latest = essays[0]
    home_main = f"""<section class="hero">
<h1>Signal &amp; Noise</h1>
<p class="tagline">One idea at a time, taken seriously.</p>
<p>Essays about AI, judgment, and human consequences. Every piece comes in two layers: <strong>the essay</strong> — the argument I wanted to make — and <strong>the audit</strong> — what the machine found when it checked, published in <a href="https://scipher888.github.io/signal-noise-audit-snapshot/world/">The World Behind the Words</a>.</p>
</section>
<section class="latest">
<p class="kicker">Latest — Issue {latest['issue']} · {display_date(latest['date'], latest['precision'])}</p>
<h2><a href="p/{latest['slug']}/">{html.escape(latest['title'])}</a></h2>
{latest['dek_html']}
</section>
<section class="recent">
<h2>Recent</h2>
""" + "\n".join(f"<p class=\"row\"><a href=\"p/{e['slug']}/\">{html.escape(e['title'])}</a> <span class=\"meta\">Issue {e['issue']}</span></p>" for e in essays[1:6]) + """
<p><a href="archive/">Full archive →</a></p>
</section>"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        PAGE.format(title="Signal & Noise", desc="Essays about AI, judgment, and human consequences — every piece an essay plus a published audit.", root="", main=home_main).replace("<title>Signal &amp; Noise — Signal &amp; Noise</title>", "<title>Signal &amp; Noise</title>"))

    # about (from the live About v3 copy)
    about_main = """<h1>About</h1>
<p>Signal &amp; Noise is for people who want to think clearly about AI, judgment, and human consequences.</p>
<p>One idea at a time, taken seriously.</p>
<h2>Who Writes This</h2>
<p>I'm Synthia Cipher. I use a pen name because of strict professional privacy obligations.</p>
<p>I use AI to draft and pressure-test — surfacing counterarguments and exposing weak reasoning. But the editorial judgment, final wording, and published claims are mine. If something here is wrong, the fault is mine, not the algorithm's.</p>
<h2>Every Piece Comes in Two Layers</h2>
<p><strong>The essay</strong> is the argument I wanted to make, the way I wanted to make it.</p>
<p><strong>The audit</strong> is what the machine found when it checked: which objections were raised, what was verified against sources, what changed because of it — and what couldn't be checked at all.</p>
<p>The essay goes through an accuracy-and-fairness check before it publishes. Then the audit digs into everything else — and we publish it, including what it weakens, in The World Behind the Words.</p>
<p>The audit isn't there to prove the essay right. It's there to show you where it might not be. The audits are run and published by AI, and each one states exactly which models ran it.</p>
<h2>Where Intuition Went</h2>
<p>I used to publish less disciplined takes in a companion publication called <a href="https://scipher888.github.io/intuition/">Intuition</a> — the version of an idea I wanted to be true, set down before the checking. Those issues stay up, unchanged. But the gap Intuition existed to display — between what I want to be true and what survives scrutiny — now lives inside every issue: the essay shows my hand, the audit shows the work.</p>
<h2>Process Transparency</h2>
<p>Public audit trail: <a href="https://github.com/scipher888/signal-noise-audit-snapshot">Editorial Audit Snapshot</a>.</p>
<h2>Subscribe</h2>
<p>Free. New issues by <a href="../feed.xml">RSS</a>.</p>
<p>One idea at a time, taken seriously.</p>"""
    os.makedirs(os.path.join(OUT, "about"), exist_ok=True)
    open(os.path.join(OUT, "about", "index.html"), "w", encoding="utf-8").write(
        PAGE.format(title="About", desc="Signal & Noise is for people who want to think clearly about AI, judgment, and human consequences.", root="../", main=about_main))

    # redirects for legacy beehiiv paths
    for old, target in [("bio", "../about/"), ("subscribe", "../about/"), ("archive-legacy", None)]:
        if target is None:
            continue
        d = os.path.join(OUT, old)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Signal &amp; Noise</title>"
            f"<meta http-equiv=\"refresh\" content=\"0; url={target}\">"
            f"<link rel=\"canonical\" href=\"{BASE_URL}/about/\"></head>"
            f"<body><p><a href=\"{target}\">Continue to Signal &amp; Noise</a></p></body></html>")

    # 404 — served at arbitrary depth, so it needs absolute paths; derive the
    # prefix from BASE_URL so the CNAME-cutover rebuild fixes it automatically.
    from urllib.parse import urlparse
    root404 = (urlparse(BASE_URL).path.rstrip("/") or "") + "/"
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        PAGE.format(title="Not found", desc="Page not found.", root=root404,
                    main=f"<h1>Not found</h1><p>That page isn't here. The <a href=\"{root404}archive/\">archive</a> lists every issue.</p>"))

    # RSS — pubDate only where the date is exact
    items = []
    for e in essays + companions:
        pub = ""
        if e["precision"] == "day":
            y, m, d = e["date"].split("-")
            import datetime as _dt
            dt = _dt.datetime(int(y), int(m), int(d), 12, 0)
            pub = f"\n      <pubDate>{dt.strftime('%a, %d %b %Y %H:%M:%S')} +0000</pubDate>"
        desc = e["dek"] or e["title"]
        items.append(f"""    <item>
      <title>{html.escape(e['title'])}</title>
      <link>{BASE_URL}/p/{e['slug']}/</link>
      <guid isPermaLink="false">signal-noise-{e['slug']}</guid>
      <description>{html.escape(desc)}</description>{pub}
    </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Signal &amp; Noise</title>
    <link>{BASE_URL}/</link>
    <description>Essays about AI, judgment, and human consequences — every piece an essay plus a published audit.</description>
    <language>en</language>
{chr(10).join(items)}
  </channel>
</rss>
"""
    open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8").write(feed)

    print(f"built: {len(essays)} essays + {len(companions)} process notes + home/archive/about/redirects/404/feed")
    for e in essays:
        print(f"  issue {e['issue']:>2}  {e['slug']:<55} {e['title'][:48]}")
    return entries


def check(entries):
    """Every built page must contain its source body verbatim."""
    bad = 0
    for e in entries:
        built = open(os.path.join(OUT, "p", e["slug"], "index.html"), encoding="utf-8").read()
        if e["body"] not in built:
            print(f"DRIFT: {e['slug']}")
            bad += 1
    print(f"fidelity check: {len(entries) - bad}/{len(entries)} pages contain their source body verbatim")
    return bad


if __name__ == "__main__":
    entries = build()
    if "--check" in sys.argv:
        sys.exit(1 if check(entries) else 0)
