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

SRC = os.path.expanduser("~/Code/signal-noise/projects/newsletter")
OUT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.signalandnoise.email"  # flipped at CNAME cutover 2026-08-12
AUDIT_BASE = "https://scipher888.github.io/signal-noise-audit-snapshot/issues"

# Audio companions (Spotify episode pages; issue -> URL). Sources: the canonical
# Anchor RSS feed's per-episode links (issues 10-22, verified 2026-08-14) and the
# episode URL J supplied for issue 23 (share ?si= tracker stripped, house style).
_EP = "https://podcasters.spotify.com/pod/show/editorial-process-synthia/episodes/"
AUDIO = {
    10: _EP + "When-Everything-Sounds-Insightful--Nothing-Sounds-Trustworthy-e3j610l",
    11: _EP + "When-Words-Arrive-Without-a-World-e3jfavv",
    12: _EP + "The-World-Behind-the-Words-e3jnicp",
    13: _EP + "When-Conscience-Has-a-Payroll-e3k3f18",
    14: _EP + "Am-I-Building-e3kejja",
    15: _EP + "The-Appeal-Button-e3kom81",
    16: _EP + "The-Gary-Marcus-Audit-e3l2l9j",
    17: _EP + "When-The-Accusation-Becomes-The-Agenda-e3lc8t2",
    18: _EP + "Principle-and-Process-e3lmd0k",
    19: _EP + "Unseen-and-Unenforced-e3lvc4e",
    20: _EP + "Who-Checks-the-AI-in-Your-Medical-Record-e3m8pib",
    21: _EP + "Delivered--Then-Invisible-e3mi62e",
    22: _EP + "The-Price-of-Being-Read-e3msuek",
    23: "https://open.spotify.com/episode/4k8AoL3DxcAJekX82fgdlj",
    24: "https://open.spotify.com/episode/2jInS7rz9AszmaTLJbFSbR",
    25: "https://open.spotify.com/episode/6pElPtOkGUskt05bYx612u",
}

# Issues with a published Extended Development Record (verbatim author + AI
# conversation) at AUDIT_BASE/issue-0NN/development/ — verified on disk 2026-08-14.
# The EDR is no longer a top-level essay-chrome leaf (J, 2026-08-29); it stays
# reachable from the audit pages.
EDR_ISSUES = {14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}

# Issues carrying the machine's-version experiment (an AI-written companion essay
# published inside the audit record; J's rulings 2026-08-23) at
# AUDIT_BASE/issue-0NN/machine-version/. The machine row appears only for these.
MACHINE_VERSION_ISSUES = {25, 26}

# In-body audit-status blocks retired per J's 2026-08-14 ruling: the companions
# line is now the piece's audit-status link, so the beehiiv-era "<hr> The audit:
# ... Audit complete." block is page chrome made redundant, stripped at wrap time
# (the fidelity check runs on the post-strip body; the paste sources stay
# untouched as the as-published record). Regex must match EXACTLY once per slug.
CHROME_STRIPS = {
    "the-price-of-being-read": r"<hr />\s*<p><strong>The audit:</strong>.*?</p>\n?",
    "ai-can-hallucinate-a-jury": r"<hr />\s*<p><strong>The audit:</strong>.*?</p>\n?",
}

# slug -> (issue_no|None for companions, source path relative to SRC, date, date_precision)
# date_precision: "day" (as-published byline, publication record, or the 2026-08-13 beehiiv
# posts export: created_at converted to US-Pacific — validated against the record dates of
# issues 19/21/22/23; where an explicit byline or record disagrees (issues 1, 20), the record wins)
MANIFEST = {
    "is-it-possible-to-be-a-good-person-on-x-d0fc": (1, "past-issues/issue-001-final.md", "2026-03-07", "day"),
    "can-you-fake-it": (2, "past-issues/issue-002-final.md", "2026-03-14", "day"),
    "the-accessibility-illusion": (3, "past-issues/issue-003-final.md", "2026-03-21", "day"),
    "the-coherence-illusion": (4, "past-issues/issue-004-paste.html", "2026-03-28", "day"),
    "what-we-changed-after-issue-4": (None, "past-issues/issue-004-companion-paste.html", "2026-03-28", "day"),
    "the-ai-that-tells-you-what-you-want-to-hear": (5, "past-issues/issue-005-paste.html", "2026-04-04", "day"),
    "the-homer-car-problem": (6, "past-issues/issue-006-paste.html", "2026-04-11", "day"),
    "when-help-becomes-harm": (7, "past-issues/issue-007-paste.html", "2026-04-17", "day"),
    "regret-as-raw-material": (8, "past-issues/issue-008-paste.html", "2026-04-25", "day"),
    "what-changed-after-issue-8": (None, "process-notes/what-changed-after-issue-8-as-published-2026-08-13.html", "2026-05-06", "day"),
    "when-right-most-of-the-time-makes-wrong-harder-to-catch": (9, "past-issues/issue-009-paste.html", "2026-05-02", "day"),
    "when-everything-sounds-insightful-nothing-sounds-trustworthy": (10, "past-issues/issue-010-paste.html", "2026-05-10", "day"),
    "when-words-arrive-without-a-world": (11, "past-issues/issue-011-paste.html", "2026-05-15", "day"),
    "the-world-behind-the-words": (12, "past-issues/issue-012-paste.html", "2026-05-21", "day"),
    "when-conscience-has-a-payroll": (13, "past-issues/issue-013-paste.html", "2026-05-29", "day"),
    "am-i-building": (14, "past-issues/issue-014-paste.html", "2026-06-07", "day"),
    "the-appeal-button": (15, "past-issues/issue-015-paste.html", "2026-06-13", "day"),
    "the-gary-marcus-audit": (16, "drafts/issue-016-paste.html", "2026-06-20", "day"),
    "when-the-accusation-becomes-the-agenda": (17, "drafts/issue-017-paste.html", "2026-06-27", "day"),
    "principle-and-process": (18, "drafts/issue-018-beehiiv-web-update-v0.10.html", "2026-07-05", "day"),
    "unseen-and-unenforced": (19, "drafts/issue-019-beehiiv-paste-2026-07-11.html", "2026-07-11", "day"),
    "who-has-to-check-the-ai-in-your-medical-record": (20, "drafts/issue-020-beehiiv-paste-2026-07-19-rev.html", "2026-07-19", "day"),
    "delivered-then-invisible": (21, "drafts/issue-021-beehiiv-paste-2026-07-25.html", "2026-07-25", "day"),
    "the-price-of-being-read": (22, "drafts/issue-022-postW-web-paste-2026-08-01.html", "2026-08-01", "day"),
    "ai-can-hallucinate-a-jury": (23, "drafts/issue-023-postW-web-paste-2026-08-09.html", "2026-08-09", "day"),
    "the-gift-is-not-the-product": (24, "drafts/issue-024-web-paste-2026-08-14.html", "2026-08-16", "day"),
    "perfect-ai-alignment-is-not-alignment": (25, "drafts/issue-025-web-paste-2026-08-22.html", "2026-08-22", "day"),
    "civilization-at-machine-speed": (26, "drafts/issue-026-web-paste-2026-08-29.html", "2026-08-29", "day"),
}

# Sources whose title/dek live outside the body (beehiiv field lines / build comments).
FIELD_OVERRIDES = {
    "principle-and-process": ("Principle and Process", "Two levels of the birthright citizenship debate"),
    "what-changed-after-issue-8": ("What Changed After Issue 8", "Why Signal & Noise retired Synthia-as-author framing and moved to named-process language."),
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
        import markdown  # issues 1-3 only; not required when recovering built HTML
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
        body = re.sub(r"^\s*<!--.*?-->\s*", "", raw, flags=re.S)
        return title, dek_html, body.strip()

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


def resolve_source(rel):
    """Editorial repo first (canonical pastes), then this repo's drafts/."""
    for root in (SRC, OUT):
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            return path
    return None


def recover_from_built(slug):
    """Rebuild chrome from an already-published page when the paste is absent.

    This web repo ships built HTML; the as-published pastes live in a private
    editorial repo. Recovering title/dek/body lets `python3 build.py` refresh
    companions (and wrap a new local draft) without that tree.
    """
    path = os.path.join(OUT, "p", slug, "index.html")
    if not os.path.isfile(path):
        raise SystemExit(f"missing source and no built page for {slug}")
    text = open(path, encoding="utf-8").read()
    art = re.search(r"<article>(.*?)</article>", text, re.S)
    if not art:
        raise SystemExit(f"no article in built page {slug}")
    inner = art.group(1)
    inner = re.sub(r"\s*<p class=\"kicker\">.*?</p>", "", inner, count=1)
    hm = re.search(r"<h1>(.*?)</h1>", inner, re.S)
    if not hm:
        raise SystemExit(f"no title heading in built page {slug}")
    title = html.unescape(re.sub(r"<[^>]+>", "", hm.group(1)).strip())
    rest = inner[hm.end():]
    dm = re.match(r"\s*(<p class=\"dek\">.*?</p>)", rest, re.S)
    dek_html = dm.group(1) if dm else ""
    if dm:
        rest = rest[dm.end():]
    rest = re.sub(r"\s*<nav class=\"cnav\".*?</nav>\s*$", "", rest, flags=re.S)
    return title, dek_html, rest.strip()


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Signal &amp; Noise</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="{root}styles.css">
  <link rel="alternate" type="application/rss+xml" title="Signal &amp; Noise" href="{root}feed.xml">
  <link rel="icon" href="{root}assets/mark.svg">
  <meta property="og:site_name" content="Signal &amp; Noise">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{base}/assets/preview.png">
  <meta name="twitter:card" content="summary_large_image">
</head>
<body>
<header class="site-head">
  <a class="masthead" href="{home}"><svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="17.5" r="11.5" fill="none" stroke="#10283a" stroke-width="2.4"/><circle cx="16" cy="17.5" r="6.8" fill="#0e2738"/><circle cx="16" cy="6" r="3.1" fill="#f3ca79"/></svg>Signal &amp; Noise</a>
  <nav><a href="{root}archive/">Archive</a> <a href="{root}about/">About</a> <a href="{root}subscribe/">Follow</a></nav>
</header>
<main>
{main}
</main>
<footer class="site-foot">
  <p>Signal &amp; Noise is written under the pen name Synthia Cipher. AI tools draft and critique; the human author owns the editorial judgment, final wording, published claims, and errors.</p>
  <p><a href="{home}">Home</a> · <a href="{root}archive/">Archive</a> · <a href="{root}about/">About</a> · <a href="{root}subscribe/">Follow</a> · <a href="{root}feed.xml">RSS</a> · <a href="https://scipher888.github.io/signal-noise-audit-snapshot/world/">The World Behind the Words</a></p>
</footer>
</body>
</html>
"""


def render(title, desc, root, main, path, ogtype="website"):
    """Wrap page content in the site template. `path` is the site-absolute path
    (e.g. "/about/") — it feeds the canonical link and the og:url.
    Homepage `root` is empty, so Home links use "/" instead of an empty href."""
    home = root or "/"
    return PAGE.format(title=html.escape(title), desc=html.escape(desc, quote=True),
                       root=root, home=home, main=main, url=BASE_URL + path, ogtype=ogtype, base=BASE_URL)


# Night Observatory hero — rebuilt from the original brand sources
# (~/Code/sn-brand-assets/{hero,hero-centered,cover}.html, June 2026): dashed orbit
# rings, the eclipse, three haloed satellites (gold/signal-blue/sage), faint stars.
# Same geometry relationships and hexes as cover.html; decorative (H1 carries the name).
OBSERVATORY = """<svg class="observatory" viewBox="0 0 640 470" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="320" cy="235" r="225" fill="none" stroke="#10283a" stroke-opacity="0.20" stroke-width="2" stroke-dasharray="3 13" stroke-linecap="round"/>
  <circle cx="320" cy="235" r="157" fill="none" stroke="#10283a" stroke-opacity="0.30" stroke-width="2"/>
  <circle cx="320" cy="235" r="105" fill="none" stroke="#10283a" stroke-opacity="0.16" stroke-width="2" stroke-dasharray="2 12" stroke-linecap="round"/>
  <circle cx="456" cy="126" r="20" fill="#fffdf8"/><circle cx="456" cy="126" r="11.5" fill="#f3ca79"/>
  <circle cx="175" cy="262" r="20" fill="#fffdf8"/><circle cx="175" cy="262" r="11.5" fill="#6fb5be"/>
  <circle cx="384" cy="390" r="20" fill="#fffdf8"/><circle cx="384" cy="390" r="11.5" fill="#6fa184"/>
  <circle cx="320" cy="18" r="6" fill="#0e2738" fill-opacity="0.45"/>
  <circle cx="573" cy="301" r="5" fill="#0e2738" fill-opacity="0.40"/>
  <circle cx="93" cy="165" r="5" fill="#0e2738" fill-opacity="0.36"/>
  <circle cx="320" cy="235" r="87" fill="#fffdf8"/>
  <circle cx="320" cy="235" r="78" fill="#0e2738"/>
  <text x="320" y="235" text-anchor="middle" dominant-baseline="central" font-family="'Iowan Old Style', Palatino, Georgia, serif" font-size="54" font-weight="500" fill="#f4efe6">S&amp;N</text>
</svg>"""


def essay_page(slug, issue, title, dek_html, body, date, precision):
    kicker = f"Issue {issue}" if issue else "Process note"
    dateline = display_date(date, precision)
    # Companion map (J, 2026-08-29). Two parallel rows, same three leaf names:
    #   The author's  — The essay · Audio companion · The audit
    #   The machine's — The essay · Audio companion · The audit
    # Audio appears on a row only when that companion exists. The machine row
    # appears only when a machine companion exists (MACHINE_VERSION_ISSUES).
    # Richer leaves (plain words, conversation/EDR, separately named machine
    # audit) live inside the audit-snapshot pages, not essay chrome.
    # Standing rules from 2026-08-23 still hold:
    #   1. ONE ABSOLUTE NAME PER DESTINATION, identical on every page that shows it.
    #   2. The current page is PINNED (.here, aria-current) rather than omitted.
    #   3. The block sits at the FOOT.
    companions = ""
    if issue:
        base = f"{AUDIT_BASE}/issue-{issue:03d}"
        author = ['<span class="here" aria-current="page">The essay</span>']
        if issue in AUDIO:
            author.append(f'<a href="{AUDIO[issue]}">Audio companion</a>')
        author.append(f'<a href="{base}/">The audit</a>')
        rows = [("The author&rsquo;s", author)]
        if issue in MACHINE_VERSION_ISSUES:
            machine = [f'<a href="{base}/machine-version/">The essay</a>']
            # No machine-row audio yet; add here only when that companion exists.
            machine.append(f'<a href="{base}/machine-version/audit/">The audit</a>')
            rows.append(("The machine&rsquo;s", machine))
        items = "".join(f"<dt>{lbl}</dt><dd>{' · '.join(ls)}</dd>" for lbl, ls in rows)
        companions = (f'\n<nav class="cnav" aria-label="Issue {issue} companions">'
                      f"<dl>{items}</dl></nav>")
    main = (f"<article>\n<p class=\"kicker\">{kicker} · {dateline}</p>\n"
            f"<h1>{html.escape(title)}</h1>\n{dek_html}\n{body}\n{companions}\n</article>")
    desc = re.sub(r"<[^>]+>", "", dek_html).strip() or f"Signal & Noise — {title}"
    return render(title, desc, "../../", main, f"/p/{slug}/", ogtype="article")


def build():
    entries = []
    for slug, (issue, rel, date, precision) in MANIFEST.items():
        path = resolve_source(rel)
        if path:
            title, dek_html, body = load_source(path, slug)
            if slug in CHROME_STRIPS:
                matches = re.findall(CHROME_STRIPS[slug], body, re.S)
                assert len(matches) == 1, f"chrome strip must match exactly once in {slug}, got {len(matches)}"
                body = re.sub(CHROME_STRIPS[slug], "", body, flags=re.S).strip()
        else:
            title, dek_html, body = recover_from_built(slug)
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
        render("Archive", "Every Signal & Noise issue, newest first.", "../", archive_main, "/archive/"))

    # home
    latest = essays[0]
    home_main = f"""<section class="hero hero-centered">
{OBSERVATORY}
<h1>Signal &amp; Noise</h1>
<div class="gold-rule"></div>
<p class="tagline">One idea at a time, taken seriously.</p>
<p class="hero-intro">Essays about AI, judgment, and human consequences. Every piece comes in two layers: <strong>the essay</strong> — the argument I wanted to make — and <strong>the audit</strong> — what the machine found when it checked, published in <a href="https://scipher888.github.io/signal-noise-audit-snapshot/world/">The World Behind the Words</a>.</p>
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
        render("Signal & Noise", "Essays about AI, judgment, and human consequences — every piece an essay plus a published audit.", "", home_main, "/").replace("<title>Signal &amp; Noise — Signal &amp; Noise</title>", "<title>Signal &amp; Noise</title>"))

    # about (from the live About v3 copy)
    about_main = """<h1>About</h1>
<p>Signal &amp; Noise is for people who want to think clearly about AI, judgment, and human consequences.</p>
<p>One idea at a time, taken seriously.</p>
<h2>Who Writes This</h2>
<p>I'm Synthia Cipher. I use a pen name because of strict professional privacy obligations.</p>
<p>I use AI to draft and pressure-test — surfacing counterarguments and exposing weak reasoning. But the editorial judgment, final wording, and published claims are mine. If something here is wrong, the fault is mine, not the algorithm's.</p>
<p>I'm a novice — at AI, at computers, at creating things, at writing. More than anything else, Signal &amp; Noise is a transparent public record of my trying to learn to create things with AI. Any value may reside in that record more than in the content of the essays.</p>
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
<p>Free. New issues by <a href="../subscribe/">RSS or email</a>.</p>
<p>One idea at a time, taken seriously.</p>"""
    os.makedirs(os.path.join(OUT, "about"), exist_ok=True)
    open(os.path.join(OUT, "about", "index.html"), "w", encoding="utf-8").write(
        render("About", "Signal & Noise is for people who want to think clearly about AI, judgment, and human consequences.", "../", about_main, "/about/"))

    # follow page — /subscribe/ keeps the legacy path but is a real page now (nav label: Follow).
    # The email option's address is PENDING J's ruling; the paragraph ships only once it is set.
    follow_main = """<h1>Follow</h1>
<p class="intro">Signal &amp; Noise is free, and there's no algorithm between you and it — just two quiet ways to know when a new issue is up.</p>
<h2>By RSS</h2>
<p>RSS is the old, calm way to follow things on the web: a reader app checks this site for you and shows new issues as they appear. No account here, no ranking, no inbox required.</p>
<p>Never used one? Either of these is free and takes about a minute to set up:</p>
<ul>
<li><a href="https://netnewswire.com/">NetNewsWire</a> — iPhone, iPad, and Mac. Free and open source; no account needed.</li>
<li><a href="https://feedly.com/news-reader">Feedly</a> — works in any browser, with apps for Android and iPhone. Asks you to create a free account first.</li>
</ul>
<p>Then add this site: paste <code>www.signalandnoise.email</code> into the reader's search or "add feed" box, and tap Add (or Follow) when it finds Signal &amp; Noise. If it asks for a feed address instead, give it <code>https://www.signalandnoise.email/feed.xml</code>.</p>
<h2>By email</h2>
<p>Prefer a note in your inbox? Write "keep me posted" to <a href="mailto:synthia@signalandnoise.email">synthia@signalandnoise.email</a> and each new issue will arrive as a short note with a link. To stop, send a blank mail to the same address with the subject <code>unsubscribe</code> — or use Unsubscribe in Gmail if you see it. You do not need to write a request.</p>"""
    os.makedirs(os.path.join(OUT, "subscribe"), exist_ok=True)
    open(os.path.join(OUT, "subscribe", "index.html"), "w", encoding="utf-8").write(
        render("Follow", "How to follow Signal & Noise — by RSS or by email.", "../", follow_main, "/subscribe/"))

    # redirects for legacy beehiiv paths
    for old, target in [("bio", "../about/"), ("archive-legacy", None)]:
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
        render("Not found", "Page not found.", root404,
               f"<h1>Not found</h1><p>That page isn't here. The <a href=\"{root404}archive/\">archive</a> lists every issue.</p>",
               "/404.html"))

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
