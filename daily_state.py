#!/usr/bin/env python3
"""Daily State of AI written editions.

Fail closed. An edition is published only when its frozen script, sources,
public QA snapshot, and recorded episode verification all agree. Invalid
input writes nothing: no edition HTML, no listing change, no recovery from
an already built page.

    python3 daily_state.py                 # write generated HTML
    python3 daily_state.py --check         # compare, write nothing
    python3 build.py --daily-state-only
    python3 build.py --daily-state-check

Essay pages, the archive, and the RSS feed are not inputs or outputs.
"""

import hashlib
import html
import ipaddress
import json
import os
import re
import sys
import tempfile
from datetime import date as date_cls
from urllib.parse import urlsplit

import build


BASE_URL = build.BASE_URL
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EPISODE_RE = re.compile(r"^https://open\.spotify\.com/episode/([A-Za-z0-9]{22})$")
HOST_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
)
VERIFIED_AT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
NAMED_GATES = ("length", "clean", "coverage", "grounded", "fresh", "coherent")
SCHEMA_VERSION = 1
CONTENT_FILES = ("script.txt", "sources.json", "qa.json", "edition.json")
LISTING_REL = "daily-state/index.html"
DESC_MAX = 200

QA_KEYS = {
    "schema_version", "date", "status", "semantic_qa", "sources",
    "source_count", "gate", "run_sha256",
}
EDITION_KEYS = {
    "schema_version", "date", "title", "canonical_url", "episode_id",
    "episode_url", "verified_at", "verification", "hashes",
}
EDITION_OPTIONAL = {"spotify_episode_fallback"}
HASH_KEYS = {"script_sha256", "sources_sha256", "qa_sha256", "run_sha256"}
VERIFICATION_KEYS = {"method", "checked_at", "episode", "show"}
EPISODE_EVIDENCE_KEYS = {"title", "canonical_url", "id"}
SHOW_KEYS = {"id", "episodes"}
SHOW_EPISODE_KEYS = {"id", "title", "uri"}


class Hold(Exception):
    """Publication stops. Callers must not write edition output."""


def edition_title(iso_date):
    return f"Daily State of AI - {iso_date}"


def edition_url(iso_date):
    return f"{BASE_URL}/daily-state/{iso_date}/"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _read_once(path):
    """Read a regular file without following a final symlink."""
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise Hold(f"unreadable input: {os.path.basename(path)}") from exc
    try:
        chunks = []
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block:
                break
            chunks.append(block)
        return b"".join(chunks)
    except OSError as exc:
        raise Hold(f"unreadable input: {os.path.basename(path)}") from exc
    finally:
        os.close(fd)


def read_stable(path):
    """Read twice so a file that changes mid-read cannot be published."""
    first = _read_once(path)
    second = _read_once(path)
    if first != second:
        raise Hold(f"{os.path.basename(path)} changed during read")
    return first


def decode_utf8(data, label):
    if data.startswith(b"\xef\xbb\xbf"):
        raise Hold(f"{label} has a byte-order mark")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Hold(f"{label} is not utf-8") from exc


def parse_json_object(data, label):
    def pairs(items):
        keys = [key for key, _value in items]
        if len(keys) != len(set(keys)):
            raise Hold(f"{label} contains a duplicate key")
        return dict(items)

    text = decode_utf8(data, label)
    try:
        value = json.loads(text, object_pairs_hook=pairs)
    except Hold:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise Hold(f"{label} is not valid json") from exc
    if type(value) is not dict:
        raise Hold(f"{label} must be a json object")
    return value


def require_keys(obj, required, label, optional=frozenset()):
    keys = set(obj)
    if keys - required - optional or required - keys:
        raise Hold(f"unknown schema: {label}")


def is_real_date(value):
    if type(value) is not str or not DATE_RE.fullmatch(value):
        return False
    try:
        parsed = date_cls.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value


def content_root(repo):
    return os.path.join(repo, "content", "daily-state")


def assert_real_child(root, path, label):
    """Reject traversal, missing paths, and any symlink component."""
    root_abs = os.path.abspath(root)
    path_abs = os.path.abspath(path)
    if os.path.islink(root_abs):
        raise Hold(f"{label} escapes through a symlink")
    try:
        if os.path.commonpath([root_abs, path_abs]) != root_abs:
            raise Hold(f"{label} escapes the edition directory")
    except ValueError as exc:
        raise Hold(f"{label} escapes the edition directory") from exc
    if not os.path.lexists(path_abs):
        raise Hold(f"missing {label}")
    current = root_abs
    rel = os.path.relpath(path_abs, root_abs)
    if rel == ".":
        return
    for part in rel.split(os.sep):
        if part in ("", ".", ".."):
            raise Hold(f"{label} escapes the edition directory")
        current = os.path.join(current, part)
        if os.path.islink(current):
            raise Hold(f"{label} escapes through a symlink")


def validate_public_https_url(url):
    """Accept an absolute public HTTPS URL and return it unchanged."""
    if type(url) is not str or url != url.strip() or any(ch in url for ch in " \t\r\n\\"):
        raise Hold("malformed source url")
    lowered = url.lower()
    if "app.link" in lowered or lowered.startswith(("javascript:", "data:")):
        raise Hold("rejected source url")
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise Hold("source url must be https")
    if parts.username is not None or parts.password is not None:
        raise Hold("source url contains credentials")
    if parts.fragment:
        raise Hold("source url contains a fragment")
    host = parts.hostname
    if not host:
        raise Hold("source url is missing a hostname")
    host = host.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith(
        (".local", ".localhost", ".internal")
    ):
        raise Hold("source url uses a local hostname")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise Hold("source url uses an ip address")
    if not HOST_RE.fullmatch(host):
        raise Hold("source url hostname is not a public hostname")
    if parts.port not in (None, 443):
        raise Hold("source url uses a non-https port")
    return url


def script_paragraphs(text):
    if text.strip() == "":
        raise Hold("script is empty")
    body = text[:-1] if text.endswith("\n") else text
    parts = body.split("\n\n")
    if not parts or any(part.strip() == "" for part in parts):
        raise Hold("script contains an empty paragraph")
    return parts


def validate_gates(gate, *, allow_detail):
    if type(gate) is not list or len(gate) != len(NAMED_GATES):
        raise Hold("named gates are missing or incomplete")
    seen = []
    allowed = {"name", "ok", "detail"} if allow_detail else {"name", "ok"}
    for item in gate:
        if type(item) is not dict or set(item) - allowed or "name" not in item or "ok" not in item:
            raise Hold("unknown gate schema")
        if item["name"] not in NAMED_GATES:
            raise Hold("unknown gate name")
        # Identity, not truthiness: the string "false" and the string "true" both hold.
        if item["ok"] is not True:
            raise Hold("named gate is not ok")
        seen.append(item["name"])
    if len(set(seen)) != len(NAMED_GATES):
        raise Hold("named gates are duplicated or missing")
    return [{"name": name, "ok": True} for name in NAMED_GATES]


def validate_run(run, iso_date, source_count):
    """Current run.json shape. Extra producer fields are ignored, not copied."""
    required = {"date", "status", "semantic_qa", "sources", "source_count", "gate", "attempts"}
    if type(run) is not dict or required - set(run):
        raise Hold("unknown run schema")
    if not is_real_date(run["date"]) or run["date"] != iso_date:
        raise Hold("run date does not match the edition")
    if run["status"] != "ok":
        raise Hold("run status is not ok")
    if run["semantic_qa"] != "pass":
        raise Hold("semantic_qa is not pass")
    if run["sources"] != "ok":
        raise Hold("run sources are not ok")
    if type(run["source_count"]) is not int or run["source_count"] != source_count:
        raise Hold("run source_count does not match sources")
    if type(source_count) is not int or source_count < 1:
        raise Hold("run source_count does not match sources")
    gates = validate_gates(run["gate"], allow_detail=True)
    attempts = run["attempts"]
    if type(attempts) is not list or not attempts or any(type(item) is not dict for item in attempts):
        raise Hold("unknown run schema")
    accepted = [item for item in attempts if item.get("accepted") is True]
    # Top-level success does not stand in for a missing accepted attempt.
    if len(accepted) != 1:
        raise Hold("accepted attempt is missing or conflicting")
    attempt = accepted[0]
    if attempt.get("semantic_qa") != "pass":
        raise Hold("accepted attempt conflicts with semantic_qa")
    if "gate" not in attempt:
        raise Hold("accepted attempt conflicts with semantic_qa")
    validate_gates(attempt["gate"], allow_detail=True)
    return gates


def project_qa(run, run_sha256, iso_date, source_count):
    """Public snapshot. Model names, delivery logs, and paths stay out."""
    if type(run_sha256) is not str or not SHA256_RE.fullmatch(run_sha256):
        raise Hold("run hash is missing")
    gates = validate_run(run, iso_date, source_count)
    return {
        "schema_version": SCHEMA_VERSION,
        "date": iso_date,
        "status": "ok",
        "semantic_qa": "pass",
        "sources": "ok",
        "source_count": source_count,
        "gate": gates,
        "run_sha256": run_sha256,
    }


def validate_qa(qa, iso_date):
    require_keys(qa, QA_KEYS, "qa.json")
    if type(qa["schema_version"]) is not int or qa["schema_version"] != SCHEMA_VERSION:
        raise Hold("unknown qa schema")
    if not is_real_date(qa["date"]) or qa["date"] != iso_date:
        raise Hold("qa date does not match the edition")
    if qa["status"] != "ok":
        raise Hold("qa status is not ok")
    if qa["semantic_qa"] != "pass":
        raise Hold("semantic_qa is not pass")
    if qa["sources"] != "ok":
        raise Hold("qa sources are not ok")
    if type(qa["source_count"]) is not int or qa["source_count"] < 1:
        raise Hold("qa source_count is invalid")
    if type(qa["run_sha256"]) is not str or not SHA256_RE.fullmatch(qa["run_sha256"]):
        raise Hold("qa run hash is invalid")
    gates = validate_gates(qa["gate"], allow_detail=False)
    if qa["gate"] != gates:
        raise Hold("named gates are not in the public order")
    return qa


def validate_sources(sources, iso_date, source_count):
    require_keys(sources, {"date", "urls", "stories"}, "sources.json")
    if not is_real_date(sources["date"]) or sources["date"] != iso_date:
        raise Hold("sources date does not match the edition")
    urls = sources["urls"]
    if type(urls) is not list or not urls or any(type(url) is not str for url in urls):
        raise Hold("sources urls are missing")
    if len(urls) != len(set(urls)):
        raise Hold("sources urls are duplicated")
    if len(urls) != source_count:
        raise Hold("sources count does not match qa")
    for url in urls:
        validate_public_https_url(url)
    stories = sources["stories"]
    if type(stories) is not list or not stories or any(type(story) is not dict for story in stories):
        raise Hold("sources stories are missing")
    for position, story in enumerate(stories, start=1):
        require_keys(story, {"title", "outlets", "urls"}, "story", optional={"index"})
        if "index" in story and (type(story["index"]) is not int or story["index"] != position):
            raise Hold("story index does not match order")
        title = story["title"]
        if type(title) is not str or title.strip() == "":
            raise Hold("story title is blank")
        outlets = story["outlets"]
        if (
            type(outlets) is not list or not outlets
            or any(type(outlet) is not str or outlet.strip() == "" for outlet in outlets)
        ):
            raise Hold("story outlets are blank")
        story_urls = story["urls"]
        if type(story_urls) is not list or not story_urls or any(type(url) is not str for url in story_urls):
            raise Hold("story urls are missing")
        for url in story_urls:
            if url not in urls:
                raise Hold("story url is not in the source list")
            validate_public_https_url(url)
    return sources


def select_episode(episodes, title):
    """Choose the episode whose title matches exactly.

    Position is not a rule. The first item and the latest item are not
    substitutes when the exact title is elsewhere or absent.
    """
    if type(episodes) is not list or not episodes:
        raise Hold("show evidence has no episodes")
    matches = []
    for item in episodes:
        if type(item) is not dict or set(item) != SHOW_EPISODE_KEYS:
            raise Hold("unknown show episode schema")
        if any(type(item[key]) is not str for key in SHOW_EPISODE_KEYS):
            raise Hold("unknown show episode schema")
        if item["title"] == title:
            matches.append(item)
    if len(matches) != 1:
        raise Hold("show evidence does not contain the exact episode title")
    return matches[0]


def episode_id_from_url(url):
    if type(url) is not str:
        raise Hold("episode url is missing or malformed")
    match = EPISODE_RE.fullmatch(url)
    if not match or "app.link" in url.lower():
        raise Hold("episode url is missing or malformed")
    return match.group(1)


def validate_recorded_verification(edition, iso_date, episode_url, episode_id):
    verification = edition["verification"]
    require_keys(verification, VERIFICATION_KEYS, "verification")
    if verification["method"] != "public_episode_and_show":
        raise Hold("unknown verification schema")
    if verification["checked_at"] != edition["verified_at"]:
        raise Hold("verification time does not match")
    episode = verification["episode"]
    require_keys(episode, EPISODE_EVIDENCE_KEYS, "episode evidence")
    title = edition_title(iso_date)
    if episode["title"] != title:
        raise Hold("verified episode title does not match the edition")
    if episode["canonical_url"] != episode_url:
        raise Hold("verified episode canonical url does not match")
    if episode["id"] != episode_id:
        raise Hold("verified episode id does not match")
    show = verification["show"]
    require_keys(show, SHOW_KEYS, "show evidence")
    if type(show["id"]) is not str or not re.fullmatch(r"[A-Za-z0-9]{22}", show["id"]):
        raise Hold("show id is malformed")
    chosen = select_episode(show["episodes"], title)
    if chosen["id"] != episode_id:
        raise Hold("show episode id does not match the episode url")
    if chosen["uri"] != f"spotify:episode:{episode_id}":
        raise Hold("show episode uri does not match the episode url")
    return chosen


def validate_edition(edition, iso_date):
    require_keys(edition, EDITION_KEYS, "edition.json", optional=EDITION_OPTIONAL)
    if type(edition["schema_version"]) is not int or edition["schema_version"] != SCHEMA_VERSION:
        raise Hold("unknown edition schema")
    if "spotify_episode_fallback" in edition:
        if edition["spotify_episode_fallback"] is not False:
            raise Hold("episode url is a show fallback")
    if not is_real_date(edition["date"]) or edition["date"] != iso_date:
        raise Hold("edition date does not match")
    title = edition_title(iso_date)
    if edition["title"] != title:
        raise Hold("edition title does not match the date")
    if edition["canonical_url"] != edition_url(iso_date):
        raise Hold("edition canonical url does not match the date")
    verified = edition["verified_at"]
    matched = VERIFIED_AT_RE.fullmatch(verified) if type(verified) is str else None
    if not matched or matched.group(1) != iso_date:
        raise Hold("verification time is missing or stale")
    episode_url = edition["episode_url"]
    episode_id = episode_id_from_url(episode_url)
    if edition["episode_id"] != episode_id:
        raise Hold("episode id does not match the episode url")
    validate_recorded_verification(edition, iso_date, episode_url, episode_id)
    hashes = edition["hashes"]
    require_keys(hashes, HASH_KEYS, "hashes")
    for key in HASH_KEYS:
        if type(hashes[key]) is not str or not SHA256_RE.fullmatch(hashes[key]):
            raise Hold(f"{key} is malformed")
    return edition


def parse_episode_document(document):
    if type(document) is not dict:
        raise Hold("verification parse failed")
    require_keys(document, EPISODE_EVIDENCE_KEYS, "fetched episode")
    if any(type(document[key]) is not str for key in EPISODE_EVIDENCE_KEYS):
        raise Hold("verification parse failed")
    return document


def parse_show_document(document):
    if type(document) is not dict or set(document) != {"episodes"}:
        raise Hold("verification parse failed")
    return document["episodes"]


def verify_public_episode(fetcher, iso_date, episode_url, show_url):
    """Live identity check. Fetch and parse errors hold; tests pass a fake fetcher.

    The file publisher uses the recorded evidence instead, so CI does not
    need network access or secrets.
    """
    if not is_real_date(iso_date):
        raise Hold("edition date is invalid")
    episode_id = episode_id_from_url(episode_url)
    if type(show_url) is not str or not re.fullmatch(
        r"https://open\.spotify\.com/(embed/)?show/[A-Za-z0-9]{22}", show_url
    ):
        raise Hold("show url is missing or malformed")
    try:
        episode_doc = fetcher(episode_url)
        show_doc = fetcher(show_url)
    except Hold:
        raise
    except Exception as exc:
        raise Hold("verification fetch failed") from exc
    try:
        episode = parse_episode_document(episode_doc)
        episodes = parse_show_document(show_doc)
    except Hold:
        raise
    except Exception as exc:
        raise Hold("verification parse failed") from exc
    title = edition_title(iso_date)
    if episode["title"] != title:
        raise Hold("verified episode title does not match the edition")
    if episode["canonical_url"] != episode_url:
        raise Hold("verified episode canonical url does not match")
    if episode["id"] != episode_id:
        raise Hold("verified episode id does not match")
    chosen = select_episode(episodes, title)
    if chosen["id"] != episode_id:
        raise Hold("show episode id does not match the episode url")
    if chosen["uri"] != f"spotify:episode:{episode_id}":
        raise Hold("show episode uri does not match the episode url")
    return chosen


def check_hashes(edition, script_bytes, sources_bytes, qa_bytes):
    hashes = edition["hashes"]
    actual = {
        "script_sha256": sha256_bytes(script_bytes),
        "sources_sha256": sha256_bytes(sources_bytes),
        "qa_sha256": sha256_bytes(qa_bytes),
    }
    for key, value in actual.items():
        if hashes[key] != value:
            raise Hold(f"{key} does not match the frozen bytes")


def description_from_paragraphs(paragraphs):
    first = " ".join(paragraphs[0].splitlines()).strip()
    match = re.match(r".+?[.!?](?=\s|$)", first)
    sentence = match.group(0).strip() if match else first
    if len(sentence) <= DESC_MAX:
        return sentence
    clipped = sentence[:DESC_MAX]
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped


def render_sources(sources):
    blocks = []
    represented = set()
    for story in sources["stories"]:
        for url in story["urls"]:
            represented.add(url)
        outlets = ", ".join(html.escape(outlet, quote=True) for outlet in story["outlets"])
        links = "\n".join(
            f'<li><a href="{html.escape(url, quote=True)}">{html.escape(url, quote=True)}</a></li>'
            for url in story["urls"]
        )
        blocks.append(
            "<section class=\"story\">\n"
            f"<h3>{html.escape(story['title'], quote=True)}</h3>\n"
            f"<p>{outlets}</p>\n"
            f"<ul>\n{links}\n</ul>\n"
            "</section>"
        )
    # Flat URLs already shown inside a story stay there. Append the rest once.
    extra = [url for url in sources["urls"] if url not in represented]
    if extra:
        links = "\n".join(
            f'<li><a href="{html.escape(url, quote=True)}">{html.escape(url, quote=True)}</a></li>'
            for url in extra
        )
        blocks.append(
            "<section class=\"story\">\n"
            "<h3>Other URLs</h3>\n"
            f"<ul>\n{links}\n</ul>\n"
            "</section>"
        )
    return "\n".join(blocks)


def daily_footer(root):
    home = root or "/"
    return (
        "<footer class=\"site-foot\">\n"
        "  <p>Daily State of AI is an AI-generated spoken briefing from Signal &amp; Noise. "
        "The script is model wording, published verbatim, and it may contain errors. "
        "It is not a human essay and not a machine companion essay.</p>\n"
        f"  <p><a href=\"{home}\">Home</a> · "
        f"<a href=\"{root}daily-state/\">Daily State</a> · "
        f"<a href=\"{root}archive/\">Archive</a> · "
        f"<a href=\"{root}about/\">About</a> · "
        f"<a href=\"{root}subscribe/\">Follow</a></p>\n"
        "</footer>"
    )


def apply_daily_footer(page, root):
    start = page.index('<footer class="site-foot">')
    end = page.index("</footer>", start) + len("</footer>")
    return page[:start] + daily_footer(root) + page[end:]


def render_page(title, description, root, main, path, ogtype):
    page = build.render(title, description, root, main, path, ogtype=ogtype)
    return apply_daily_footer(page, root)


def render_edition_html(edition, paragraphs, sources):
    body = "\n".join(f"<p>{html.escape(paragraph, quote=True)}</p>" for paragraph in paragraphs)
    shown = build.display_date(edition["date"], "day")
    main = (
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(edition['title'], quote=True)}</h1>\n"
        f"<p><time datetime=\"{edition['date']}\">{html.escape(shown)}</time></p>\n"
        f"<p><a href=\"{html.escape(edition['episode_url'], quote=True)}\">Audio on Spotify</a></p>\n"
        "<div class=\"script\">\n"
        f"{body}\n"
        "</div>\n"
        "<p class=\"disclaimer\">AI-generated \u00b7 may contain errors</p>\n"
        "<section class=\"sources\">\n"
        "<h2>Sources</h2>\n"
        f"{render_sources(sources)}\n"
        "</section>\n"
        "</article>"
    )
    return render_page(
        edition["title"],
        description_from_paragraphs(paragraphs),
        "../../",
        main,
        f"/daily-state/{edition['date']}/",
        "article",
    )


def render_listing_html(editions):
    ordered = sorted(editions, key=lambda item: item["date"], reverse=True)
    rows = []
    for item in ordered:
        document = item["edition"]
        shown = build.display_date(item["date"], "day")
        rows.append(
            f"<p class=\"row\"><a href=\"{item['date']}/\">{html.escape(document['title'], quote=True)}</a> "
            f"<span class=\"meta\"><time datetime=\"{item['date']}\">{html.escape(shown)}</time></span></p>"
        )
    main = (
        "<h1>Daily State of AI</h1>\n"
        "<p class=\"intro\">Written editions of the daily spoken briefing. "
        "Each page is the approved script, with its sources and a link to the audio.</p>\n"
        + "\n".join(rows)
    )
    return render_page(
        "Daily State of AI",
        "Written editions of the Daily State of AI spoken briefing.",
        "../",
        main,
        "/daily-state/",
        "website",
    )


def list_edition_dates(repo):
    root = content_root(repo)
    assert_real_child(repo, root, "content/daily-state")
    if not os.path.isdir(root):
        raise Hold("missing content/daily-state")
    dates = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not is_real_date(name) or os.path.islink(path) or not os.path.isdir(path):
            raise Hold(f"unexpected content entry: {name}")
        assert_real_child(root, path, name)
        dates.append(name)
    if not dates:
        raise Hold("no daily state editions")
    return dates


def load_edition(repo, iso_date):
    if not is_real_date(iso_date) or os.sep in iso_date or "/" in iso_date:
        raise Hold("edition date is invalid")
    root = content_root(repo)
    directory = os.path.join(root, iso_date)
    assert_real_child(root, directory, iso_date)
    if not os.path.isdir(directory):
        raise Hold("missing edition directory")
    names = sorted(os.listdir(directory))
    if names != sorted(CONTENT_FILES):
        raise Hold("edition directory does not contain the frozen public inputs")
    paths = {}
    raw = {}
    for name in CONTENT_FILES:
        path = os.path.join(directory, name)
        assert_real_child(directory, path, name)
        if not os.path.isfile(path):
            raise Hold(f"missing {name}")
        paths[name] = path
        raw[name] = read_stable(path)
    script_text = decode_utf8(raw["script.txt"], "script.txt")
    paragraphs = script_paragraphs(script_text)
    sources = parse_json_object(raw["sources.json"], "sources.json")
    qa = parse_json_object(raw["qa.json"], "qa.json")
    edition = parse_json_object(raw["edition.json"], "edition.json")
    validate_qa(qa, iso_date)
    validate_sources(sources, iso_date, qa["source_count"])
    validate_edition(edition, iso_date)
    if qa["run_sha256"] != edition["hashes"]["run_sha256"]:
        raise Hold("run_sha256 does not match the qa snapshot")
    check_hashes(edition, raw["script.txt"], raw["sources.json"], raw["qa.json"])
    for field in ("date",):
        if sources[field] != iso_date or qa[field] != iso_date or edition[field] != iso_date:
            raise Hold("edition dates do not agree")
    return {
        "date": iso_date,
        "paragraphs": paragraphs,
        "sources": sources,
        "qa": qa,
        "edition": edition,
        "html": render_edition_html(edition, paragraphs, sources),
    }


def render_output(loaded):
    files = {LISTING_REL: render_listing_html(loaded)}
    for edition in loaded:
        files[f"daily-state/{edition['date']}/index.html"] = edition["html"]
    return files


def list_output_files(repo):
    root = os.path.join(repo, "daily-state")
    if not os.path.lexists(root):
        return set()
    if os.path.islink(root):
        raise Hold("daily-state output is a symlink")
    found = set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        if os.path.islink(dirpath):
            raise Hold("symlink in generated output")
        for name in dirnames:
            if os.path.islink(os.path.join(dirpath, name)):
                raise Hold("symlink in generated output")
        for name in filenames:
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                raise Hold("symlink in generated output")
            rel = os.path.relpath(path, repo).replace(os.sep, "/")
            found.add(rel)
    return found


def commit_output(repo, files, write, allow_correction):
    found = list_output_files(repo)
    expected = set(files)
    if found - expected:
        raise Hold("unexpected generated output")
    changed = []
    for rel, html_text in files.items():
        path = os.path.join(repo, rel)
        if os.path.lexists(path) and (os.path.islink(path) or not os.path.isfile(path)):
            raise Hold(f"refusing to replace {rel}")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as handle:
                current = handle.read()
            if current == html_text:
                continue
            # A new date may refresh the listing. A changed edition page may not.
            # Check mode never takes this branch: it reports drift and writes nothing.
            if write and rel != LISTING_REL and not allow_correction:
                raise Hold(
                    f"same-day output already published; refusing to overwrite {rel}"
                )
        changed.append(rel)
    if not write:
        if found != expected or changed:
            raise Hold("generated output does not match the validated editions")
        return {"wrote": 0, "noop": True}
    if not changed:
        return {"wrote": 0, "noop": True}
    temps = []
    try:
        for rel in changed:
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".ds-", suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(files[rel])
            temps.append((tmp, path))
        for tmp, path in temps:
            os.replace(tmp, path)
    except Exception:
        for tmp, _path in temps:
            if os.path.exists(tmp):
                os.remove(tmp)
        raise
    return {"wrote": len(changed), "noop": False}


def publish(repo, *, write=True, allow_correction=False):
    """Validate every edition before replacing any generated file."""
    loaded = [load_edition(repo, iso_date) for iso_date in list_edition_dates(repo)]
    files = render_output(loaded)
    return commit_output(repo, files, write=write, allow_correction=allow_correction)


def main(argv=None, repo=None):
    if argv is None:
        argv = sys.argv[1:]
    repo = repo or os.path.dirname(os.path.abspath(__file__))
    check_only = "--check" in argv or "--daily-state-check" in argv
    allow_correction = "--allow-correction" in argv and not check_only
    try:
        result = publish(repo, write=not check_only, allow_correction=allow_correction)
    except Hold as exc:
        print(f"HOLD: {exc}", file=sys.stderr)
        return 1
    if check_only:
        print("daily state check: ok")
    elif result["noop"]:
        print("daily state: up to date")
    else:
        print(f"daily state: wrote {result['wrote']} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
