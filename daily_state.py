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

    # Opt-in editor mode, offline, from a package directory:
    python3 daily_state.py --package DIR --check
    python3 daily_state.py --package DIR --out OUT

Essay pages, the essay archive, and the RSS feed are not inputs or outputs. The homepage teaser in index.html is refreshed alongside the Daily State listing.
The editor path is not the default. It runs only when a package or edition
opts in (run.json pipeline "editor" or an editor object, edition.json
pipeline "editor", or --pipeline editor).

From 2026-11-21 the daily edition itself can be an audit edition: the date
directory holds edition.json mode "audit" with "variant": null, the raw
Neon script, sources.json and neon_run.json (plus short.mp4 when the short
shipped). From 2026-11-22 the page links the canonical Spotify episode
("Audio on Spotify", with the recorded public verification, as before the
audit editions) and no episode.mp3 is published; a missing or unverified
Spotify episode holds. Only 2026-11-21 keeps its self-hosted episode.mp3. The executable audit is attached
later as an audit/ subdirectory. Until then the audit page says the audit
is pending, and only that pending page may be replaced once the audit lands.

Audit mode is a second opt-in. A variant directory such as
content/daily-state/YYYY-MM-DD/neon/ with edition.json mode "audit"
publishes its own page and an audit page. The receipt is the audit counts
and the sha256 of audit.json. It does not use qa.json, an editor receipt,
or a fabricated QA pass. The parent edition is unchanged.
"""

import hashlib
import html
import ipaddress
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
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
# Editor mode adds one public file. run.json stays out of the edition directory.
EDITOR_CONTENT_FILES = CONTENT_FILES + ("editor_notes.json",)
EDITOR_EDITION_KEYS = frozenset({"pipeline", "editor", "hard_stops"})
HARD_STOP_KINDS = frozenset({"audio", "video", "dead_link", "label"})
EDITOR_NOTE_ARTIFACTS = frozenset({"episode", "short", "written"})
EDITOR_NOTE_STATUSES = frozenset({"accepted_unresolved", "accepted_partial"})
# Notes page wording. Raw status tokens stay in the JSON.
EDITOR_NOTE_STATUS_LABELS = {
    "accepted_unresolved": "Unresolved",
    "accepted_partial": "Partly resolved",
}
# Group order on the notes page.
EDITOR_NOTE_GROUPS = (
    ("episode", "Episode"),
    ("short", "Short"),
    ("written", "Written edition"),
)
_EDITOR_ALLOWED = frozenset({
    "model", "accepted", "overruled", "partially", "completed", "outstanding",
    "reasoning_effort", "decisions", "word_min", "word_max", "within_word_target",
})
# Canonical decisions from the editor pipeline, plus the older three-count form.
_DECISION_CANONICAL = ("overruled", "accepted_resolved", "accepted_unresolved", "accepted_partial")
_DECISION_LEGACY = ("accepted", "overruled", "partially")
_DECISION_ALLOWED = frozenset(set(_DECISION_CANONICAL) | set(_DECISION_LEGACY) | {"total"})
LISTING_REL = "daily-state/index.html"
HOME_REL = "index.html"
TEASER_SECTION_RE = re.compile(
    r'<section class="[^"]*\bdaily-latest\b[^"]*">.*?</section>',
    re.S,
)
GREETING_RE = re.compile(r"^Welcome to the Daily State of AI\b", re.I)
DESC_MAX = 200
# A browser user agent. 403 from a script is not evidence a source is gone.
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
_BOT_MARKERS = (
    "just a moment",
    "verify you are human",
    "cf-browser-verification",
    "attention required",
    "captcha",
    "enable javascript",
)
# The page template prints this once. Upstream scripts sometimes repeat it,
# as its own paragraph or as the final sentence of the body. Separators,
# a trailing period, and case all vary; a sentence that merely mentions AI
# does not match.
_AI_LABEL = r"ai-generated\s*[;\u00b7\-]\s*may\s+contain\s+errors\.?"
AI_LABEL_RE = re.compile(r"(?i)" + _AI_LABEL)
_AI_LABEL_LINE_RE = re.compile(r"(?i)^" + _AI_LABEL + r"$")
_TRAILING_AI_LABEL_RE = re.compile(r"(?i)(?<=[.!?])\s+" + _AI_LABEL + r"\s*$")
AI_LABEL_EXACT = "AI-generated \u00b7 may contain errors"
X_POST_RE = re.compile(
    r"^https://(?:www\.)?(?:x\.com|twitter\.com)/([^/?#]+)/status/\d+(?:[/?#].*)?$",
    re.IGNORECASE,
)

QA_KEYS = {
    "schema_version", "date", "status", "semantic_qa", "sources",
    "source_count", "gate", "run_sha256",
}
EDITION_KEYS = {
    "schema_version", "date", "title", "canonical_url", "episode_id",
    "episode_url", "verified_at", "verification", "hashes",
}
EDITION_OPTIONAL = {"spotify_episode_fallback", "pipeline", "editor", "hard_stops", "video_url", "headline"}
HEADLINE_OPTIONAL = frozenset({"headline"})
HEADLINE_MAX_WORDS = 14
HEADLINE_MAX_CHARS = 140
HASH_KEYS = {"script_sha256", "sources_sha256", "qa_sha256", "run_sha256"}
# A raw variant sits beside a published date. It is not a date of its own.
VARIANT_NAMES = frozenset({"neon"})
AUDIT_ROOT_FILES = (
    "edition.json", "script.txt", "sources.json", "neon_run.json",
    "episode.mp3", "short.mp4",
)
AUDIT_EDITION_KEYS = frozenset({
    "schema_version", "date", "mode", "variant", "title", "canonical_url",
    "model", "reasoning_effort", "audio_url", "video_url", "sources_url",
    "audit", "hashes",
})
AUDIT_HASH_KEYS = frozenset({
    "script_sha256", "sources_sha256", "neon_run_sha256", "audit_sha256",
    "episode_sha256", "short_sha256",
})
AUDIT_RECEIPT_KEYS = frozenset({"sha256", "gate", "episode", "short"})
# The daily (root) audit edition. The audit lands after publish, so the
# edition receipt cannot carry its hash; audit.json is tied to the edition by
# its script hash instead.
ROOT_AUDIT_REQUIRED_FILES = ("edition.json", "script.txt", "sources.json", "neon_run.json", "episode.mp3")
ROOT_AUDIT_OPTIONAL_FILES = ("short.mp4",)
ROOT_AUDIT_HASH_KEYS = frozenset({
    "script_sha256", "sources_sha256", "neon_run_sha256", "episode_sha256", "short_sha256",
})
ROOT_AUDIT_RECEIPT = {"gate": False, "attach": "after_publish"}
# From 2026-11-22 (Synthia, 2026-11-21) a daily audit edition links the
# Spotify episode like the pre-audit editions and publishes no episode.mp3.
# Dates up to this one keep the self-hosted player they were published with.
SELF_HOSTED_AUDIO_LAST_DATE = "2026-11-21"
ROOT_AUDIT_SPOTIFY_KEYS = frozenset({"episode_id", "episode_url", "verified_at", "verification"})
ROOT_NEON_PIPELINE = "neon"
NEON_MODEL = "google/gemini-4-neon"
AUDIT_PENDING_MARKER = "<!-- daily-state-audit-pending -->"
AUDIT_STATUSES = ("PASS", "FAIL", "NEEDS-HUMAN", "ERROR")
# FAIL stays expanded. ERROR is the same kind of open item. The rest collapse.
AUDIT_STATUS_ORDER = ("FAIL", "ERROR", "NEEDS-HUMAN", "PASS")
AUDIT_OPEN_STATUSES = frozenset({"FAIL", "ERROR"})
# takeaways: the claims in the takeaways extracted from the episode (2026-11-21);
# shown on the audit page only when that day's audit tested them.
AUDIT_ARTIFACTS = ("episode", "short", "takeaways")
REPO_FILE_URL = "https://github.com/scipher888/signal-noise-web/blob/main/"
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


def is_ai_label(text):
    """True when text is only the AI-generated / may-contain-errors label."""
    return _AI_LABEL_LINE_RE.fullmatch(" ".join(text.split())) is not None


def count_ai_labels(text):
    return len(AI_LABEL_RE.findall(text))


def body_paragraphs(paragraphs):
    """Script paragraphs for the page body, without a duplicate AI label.

    Drops a paragraph that is only the label, and a final sentence that is
    only the label. Any other sentence stays, including ones that mention AI.
    """
    visible = []
    for paragraph in paragraphs:
        if is_ai_label(paragraph):
            continue
        stripped = _TRAILING_AI_LABEL_RE.sub("", paragraph)
        if stripped.strip() == "":
            continue
        visible.append(stripped)
    return visible


def validate_gates(gate, *, allow_detail, advisory=False):
    if type(gate) is not list or len(gate) != len(NAMED_GATES):
        raise Hold("named gates are missing or incomplete")
    seen = []
    allowed = {"name", "ok"}
    if allow_detail:
        allowed = allowed | {"detail"}
    if advisory:
        allowed = allowed | {"advisory", "findings"}
    for item in gate:
        if type(item) is not dict or set(item) - allowed or "name" not in item or "ok" not in item:
            raise Hold("unknown gate schema")
        if item["name"] not in NAMED_GATES:
            raise Hold("unknown gate name")
        # Identity, not truthiness: the string "false" and the string "true" both hold.
        if item["ok"] is not True:
            raise Hold("named gate is not ok")
        if advisory:
            if item.get("advisory") is not True:
                raise Hold("advisory gate is not marked advisory")
            findings = item.get("findings")
            if type(findings) is not int or findings < 0:
                raise Hold("advisory gate findings are invalid")
        seen.append(item["name"])
    if len(set(seen)) != len(NAMED_GATES):
        raise Hold("named gates are duplicated or missing")
    return [{"name": name, "ok": True} for name in NAMED_GATES]


def _editor_count(value, label):
    if type(value) is not int or value < 0:
        raise Hold(f"editor {label} is invalid")
    return value


def editor_mode_of(run, editor_mode):
    """True when this receipt takes the experimental editor path.

    The default is the live path. Opt in with pipeline "editor", an editor
    object, or editor_mode=True. editor_mode=False keeps the live rules.
    """
    if editor_mode is True:
        return True
    if editor_mode is False:
        return False
    if type(run) is not dict:
        return False
    return run.get("pipeline") == "editor" or type(run.get("editor")) is dict


def _legacy_decision_counts(accepted, overruled, partially):
    return {
        "overruled": overruled,
        "accepted_resolved": accepted,
        "accepted_unresolved": 0,
        "accepted_partial": partially,
        "total": accepted + overruled + partially,
        "canonical": False,
    }


def _decision_counts(decisions):
    """Canonical counts, or the older accepted/overruled/partially object."""
    if type(decisions) is not dict or set(decisions) - _DECISION_ALLOWED:
        raise Hold("unknown editor schema")
    canonical = all(key in decisions for key in _DECISION_CANONICAL)
    legacy = all(key in decisions for key in _DECISION_LEGACY)
    if canonical:
        counts = {key: _editor_count(decisions[key], key) for key in _DECISION_CANONICAL}
        if legacy and (
            counts["accepted_resolved"] != _editor_count(decisions["accepted"], "accepted")
            or counts["accepted_partial"] != _editor_count(decisions["partially"], "partially")
        ):
            raise Hold("editor decisions do not match")
        expected = sum(counts[key] for key in _DECISION_CANONICAL)
        counts["canonical"] = True
    elif legacy:
        counts = _legacy_decision_counts(
            _editor_count(decisions["accepted"], "accepted"),
            _editor_count(decisions["overruled"], "overruled"),
            _editor_count(decisions["partially"], "partially"),
        )
        expected = counts["total"]
    else:
        raise Hold("unknown editor schema")
    if "total" in decisions and _editor_count(decisions["total"], "total") != expected:
        raise Hold("editor decisions do not match")
    counts["total"] = expected
    return counts


def normalize_editor(editor):
    """Public editor receipt.

    The canonical decisions object is overruled, accepted_resolved,
    accepted_unresolved, accepted_partial, and total. The older
    accepted/overruled/partially counts, flat or nested, still pass.
    """
    if type(editor) is not dict or set(editor) - _EDITOR_ALLOWED or "model" not in editor:
        raise Hold("unknown editor schema")
    model = editor["model"]
    if type(model) is not str or model.strip() == "" or any(ch in model for ch in "\r\n"):
        raise Hold("unknown editor schema")
    decisions = editor.get("decisions")
    if "decisions" in editor and type(decisions) is not dict:
        raise Hold("unknown editor schema")
    flat = all(key in editor for key in _DECISION_LEGACY)
    if type(decisions) is dict:
        counts = _decision_counts(decisions)
    elif flat:
        counts = _legacy_decision_counts(
            _editor_count(editor["accepted"], "accepted"),
            _editor_count(editor["overruled"], "overruled"),
            _editor_count(editor["partially"], "partially"),
        )
    else:
        raise Hold("unknown editor schema")
    if flat and type(decisions) is dict:
        flat_counts = _legacy_decision_counts(
            _editor_count(editor["accepted"], "accepted"),
            _editor_count(editor["overruled"], "overruled"),
            _editor_count(editor["partially"], "partially"),
        )
        if (
            flat_counts["overruled"] != counts["overruled"]
            or flat_counts["accepted_resolved"] != counts["accepted_resolved"]
            or flat_counts["accepted_partial"] != counts["accepted_partial"]
        ):
            raise Hold("editor decisions do not match")
    for key in ("word_min", "word_max"):
        if key in editor and (type(editor[key]) is not int or editor[key] < 0):
            raise Hold("unknown editor schema")
    if "within_word_target" in editor and type(editor["within_word_target"]) is not bool:
        raise Hold("unknown editor schema")
    if "reasoning_effort" in editor and (
        type(editor["reasoning_effort"]) is not str or editor["reasoning_effort"].strip() == ""
    ):
        raise Hold("unknown editor schema")
    if "completed" not in editor or type(editor["completed"]) is not bool:
        raise Hold("editor completed flag is missing")
    if "outstanding" not in editor:
        raise Hold("editor outstanding count is missing")
    outstanding = _editor_count(editor["outstanding"], "outstanding")
    if counts["canonical"] and outstanding != counts["accepted_unresolved"] + counts["accepted_partial"]:
        raise Hold("editor outstanding count does not match decisions")
    return {
        "model": model,
        "overruled": counts["overruled"],
        "accepted_resolved": counts["accepted_resolved"],
        "accepted_unresolved": counts["accepted_unresolved"],
        "accepted_partial": counts["accepted_partial"],
        "accepted": counts["accepted_resolved"],
        "partially": counts["accepted_partial"],
        "total": counts["total"],
        "completed": editor["completed"],
        "outstanding": outstanding,
    }


def validate_hard_stops(stops):
    """Schema-check hard_stops. An empty list is a pass. Callers hold on items."""
    if type(stops) is not list:
        raise Hold("hard_stops must be a list")
    cleaned = []
    for item in stops:
        if type(item) is not dict or set(item) != {"kind", "detail"}:
            raise Hold("unknown hard stop schema")
        if item["kind"] not in HARD_STOP_KINDS:
            raise Hold("unknown hard stop kind")
        detail = item["detail"]
        if type(detail) is not str or detail.strip() == "" or any(ch in detail for ch in "\r\n"):
            raise Hold("hard stop detail is blank")
        cleaned.append({"kind": item["kind"], "detail": detail})
    return cleaned


def format_hard_stops(stops):
    rendered = "; ".join(f"{item['kind']}: {item['detail']}" for item in stops)
    return f"hard stop: {rendered}"


def raise_hard_stops(stops):
    if stops:
        raise Hold(format_hard_stops(stops))


def edition_declares_editor(edition):
    present = EDITOR_EDITION_KEYS & set(edition)
    if not present:
        return False
    if present != EDITOR_EDITION_KEYS or edition.get("pipeline") != "editor":
        raise Hold("unknown schema: edition.json")
    return True


def validate_run(run, iso_date, source_count, *, editor_mode=None):
    """Current run.json shape. Extra producer fields are ignored, not copied.

    Editor mode passes when editor.completed is true, hard_stops is empty,
    and the six gates are advisory ok. QA findings do not hold. A recorded
    hard stop does. The live path ignores this and still requires plain gates.
    """
    selected = editor_mode_of(run, editor_mode)
    required = {"date", "status", "semantic_qa", "sources", "source_count", "gate", "attempts"}
    if selected:
        required = set(required) | {"editor", "hard_stops"}
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
    gates = validate_gates(run["gate"], allow_detail=True, advisory=selected)
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
    validate_gates(attempt["gate"], allow_detail=True, advisory=selected)
    if not selected:
        return gates
    if run.get("pipeline") not in (None, "editor"):
        raise Hold("unknown run schema")
    if type(run.get("hard_stop")) is str and run["hard_stop"].strip() != "":
        detail = run["error"] if type(run.get("error")) is str and run["error"].strip() else run["hard_stop"]
        raise Hold(f"hard stop: {run['hard_stop']}: {detail}")
    receipt = normalize_editor(run["editor"])
    stops = validate_hard_stops(run["hard_stops"])
    if receipt["completed"] is not True:
        raise Hold("editor pass is not complete")
    raise_hard_stops(stops)
    return gates


def project_qa(run, run_sha256, iso_date, source_count, *, editor_mode=None):
    """Public snapshot. Model names, delivery logs, and paths stay out.

    Advisory findings are not copied. The public gate list stays name and ok.
    """
    if type(run_sha256) is not str or not SHA256_RE.fullmatch(run_sha256):
        raise Hold("run hash is missing")
    gates = validate_run(run, iso_date, source_count, editor_mode=editor_mode)
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


def validate_sources(sources, iso_date, source_count, *, audit=False):
    """Live and editor editions reject unknown keys.

    Audit mode keeps the same required shape and also allows the frozen
    reference_snapshot object and a verification_status on each story.
    Those fields stay in sources.json so the recorded hash does not change.
    """
    optional = {"reference_snapshot"} if audit else frozenset()
    require_keys(sources, {"date", "urls", "stories"}, "sources.json", optional=optional)
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
    story_optional = {"index", "verification_status"} if audit else {"index"}
    for position, story in enumerate(stories, start=1):
        require_keys(story, {"title", "outlets", "urls"}, "story", optional=story_optional)
        if "index" in story and (type(story["index"]) is not int or story["index"] != position):
            raise Hold("story index does not match order")
        if "verification_status" in story:
            status = story["verification_status"]
            if type(status) is not str or status.strip() == "" or any(ch in status for ch in "\r\n"):
                raise Hold("story verification_status is blank")
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
    if audit and "reference_snapshot" in sources and type(sources["reference_snapshot"]) is not dict:
        raise Hold("reference_snapshot is invalid")
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


def validate_headline(value):
    """Return a cleaned 1-14 word headline, or raise Hold."""
    if type(value) is not str:
        raise Hold("headline is invalid")
    text = value.strip()
    quotes = '"\'' + '\u201c\u201d\u2018\u2019'
    if len(text) >= 2 and text[0] == text[-1] and text[0] in quotes:
        text = text[1:-1].strip()
    if text == "" or any(ch in text for ch in "\r\n"):
        raise Hold("headline is invalid")
    words = text.split()
    if not (1 <= len(words) <= HEADLINE_MAX_WORDS) or len(text) > HEADLINE_MAX_CHARS:
        raise Hold("headline is invalid")
    return text


def edition_headline(edition):
    """Optional headline, already validated when present."""
    value = edition.get("headline")
    if type(value) is not str or value.strip() == "":
        return None
    return value.strip()


def listing_link_text(edition):
    headline = edition_headline(edition)
    return headline if headline else edition["title"]


def headline_block(edition):
    headline = edition_headline(edition)
    if not headline:
        return ""
    return f"<p class=\"ds-headline\">{html.escape(headline, quote=True)}</p>\n"


def apply_headline(edition):
    if "headline" in edition:
        edition["headline"] = validate_headline(edition["headline"])


def validate_edition(edition, iso_date):
    require_keys(edition, EDITION_KEYS, "edition.json", optional=EDITION_OPTIONAL)
    apply_headline(edition)
    editor_mode = edition_declares_editor(edition)
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
    hash_optional = {"editor_notes_sha256"} if editor_mode else frozenset()
    require_keys(hashes, HASH_KEYS, "hashes", optional=hash_optional)
    if editor_mode and "editor_notes_sha256" not in hashes:
        raise Hold("editor_notes_sha256 is missing")
    for key in HASH_KEYS | hash_optional:
        if key not in hashes:
            continue
        if type(hashes[key]) is not str or not SHA256_RE.fullmatch(hashes[key]):
            raise Hold(f"{key} is malformed")
    if "video_url" in edition:
        problem = video_reference_problem(edition["video_url"])
        if problem:
            raise Hold(f"hard stop: video: {problem}")
    if editor_mode:
        receipt = normalize_editor(edition["editor"])
        stops = validate_hard_stops(edition["hard_stops"])
        if receipt["completed"] is not True:
            raise Hold("editor pass is not complete")
        raise_hard_stops(stops)
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


def check_hashes(edition, script_bytes, sources_bytes, qa_bytes, notes_bytes=None):
    hashes = edition["hashes"]
    actual = {
        "script_sha256": sha256_bytes(script_bytes),
        "sources_sha256": sha256_bytes(sources_bytes),
        "qa_sha256": sha256_bytes(qa_bytes),
    }
    if notes_bytes is not None:
        actual["editor_notes_sha256"] = sha256_bytes(notes_bytes)
    for key, value in actual.items():
        if hashes[key] != value:
            raise Hold(f"{key} does not match the frozen bytes")


def _is_bot_block(body):
    if type(body) is bytes:
        text = body.decode("utf-8", "replace")
    else:
        text = str(body or "")
    lowered = text.lower()
    return any(marker in lowered for marker in _BOT_MARKERS)


def link_verdict(status, body=b""):
    """Classify one HTTP response: ok, dead, or retry.

    401, 403, 405, 429, and bot-block pages are reachable. 404 and 410 are
    dead. A 5xx is retried once by the caller; a bot-block page is not a 5xx
    failure.
    """
    if type(status) is not int:
        return "dead"
    if status in (401, 403, 405, 429):
        return "ok"
    if status in (404, 410):
        return "dead"
    if 500 <= status <= 599:
        if _is_bot_block(body):
            return "ok"
        return "retry"
    return "ok"


def _call_link_opener(opener, method, url):
    try:
        result = opener(method, url)
    except urllib.error.HTTPError as exc:
        body = b""
        if exc.fp is not None:
            try:
                body = exc.fp.read(8192)
            except Exception:
                body = b""
        return exc.code, body
    except (urllib.error.URLError, TimeoutError, OSError):
        return None, b""
    if type(result) is not tuple or len(result) != 2:
        raise Hold("link probe returned an unexpected result")
    status, body = result
    if type(body) is str:
        body = body.encode("utf-8", "replace")
    if body is None:
        body = b""
    if type(body) is not bytes:
        raise Hold("link probe returned an unexpected result")
    return status, body


def url_is_dead(url, opener):
    """True when a source URL is actually dead.

    Sends HEAD, then GET, with one extra GET when the first GET is a 5xx.
    DNS and connection failures are dead. opener(method, url) returns
    (status, body) or raises HTTPError / URLError.
    """
    validate_public_https_url(url)
    head_status, _head_body = _call_link_opener(opener, "HEAD", url)
    if head_status is None:
        return True
    status, body = _call_link_opener(opener, "GET", url)
    if status is None:
        return True
    verdict = link_verdict(status, body)
    if verdict == "retry":
        status, body = _call_link_opener(opener, "GET", url)
        if status is None:
            return True
        verdict = link_verdict(status, body)
        if verdict == "retry":
            return True
    return verdict == "dead"


def source_link_hard_stops(urls, opener):
    stops = []
    for url in urls:
        if url_is_dead(url, opener):
            stops.append({"kind": "dead_link", "detail": url})
    return stops


def build_link_request(url, method):
    return urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": BROWSER_UA},
    )


def live_link_opener(method, url):
    """Network probe for --check-links. Tests pass their own opener."""
    request = build_link_request(url, method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read(8192)
    except urllib.error.HTTPError:
        raise
    except (urllib.error.URLError, TimeoutError, OSError):
        raise


def _within_directory(directory, ref):
    if type(ref) is not str or ref.strip() == "" or ref != ref.strip():
        return None
    if "\\" in ref or ref.startswith("/") or "://" in ref:
        return None
    parts = ref.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return None
    root = os.path.abspath(directory)
    path = os.path.abspath(os.path.join(root, ref))
    try:
        if os.path.commonpath([root, path]) != root:
            return None
    except ValueError:
        return None
    return path


def _local_media_problem(kind, ref, directory):
    path = _within_directory(directory, ref) if directory is not None else None
    if path is None or os.path.islink(path) or not os.path.isfile(path):
        return f"missing {kind} reference"
    try:
        with open(path, "rb") as handle:
            header = handle.read(128)
    except OSError:
        return f"missing {kind} reference"
    if len(header) < 16:
        return f"broken {kind} reference"
    if kind == "video" and b"ftyp" not in header:
        return "broken video reference"
    if kind == "audio":
        frame = len(header) > 1 and header[0] == 0xFF and (header[1] & 0xE0) == 0xE0
        if not (header.startswith(b"ID3") or frame):
            return "broken audio reference"
    return None


def audio_reference_problem(ref, directory=None):
    """Missing or broken audio. A Spotify episode URL is a sound reference."""
    if type(ref) is not str or ref.strip() == "":
        return "missing audio reference"
    if ref.startswith("https://"):
        try:
            episode_id_from_url(ref)
        except Hold:
            return "broken audio reference"
        return None
    if directory is None:
        return "broken audio reference"
    return _local_media_problem("audio", ref, directory)


def video_reference_problem(ref, directory=None):
    """Missing or broken video. Absent is not an error; the caller decides."""
    if type(ref) is not str or ref.strip() == "":
        return "missing video reference"
    if ref.startswith("https://"):
        try:
            validate_public_https_url(ref)
        except Hold:
            return "broken video reference"
        return None
    if directory is None:
        return "broken video reference"
    return _local_media_problem("video", ref, directory)


def validate_editor_notes(notes, iso_date):
    require_keys(notes, {"date", "outstanding", "generated_by"}, "editor_notes.json")
    if not is_real_date(notes["date"]) or notes["date"] != iso_date:
        raise Hold("editor notes date does not match the edition")
    outstanding = notes["outstanding"]
    if type(outstanding) is not list:
        raise Hold("editor notes outstanding is invalid")
    for item in outstanding:
        require_keys(item, {"artifact", "summary", "reason", "status"}, "editor note")
        if item["artifact"] not in EDITOR_NOTE_ARTIFACTS:
            raise Hold("editor note artifact is invalid")
        if item["status"] not in EDITOR_NOTE_STATUSES:
            raise Hold("editor note status is invalid")
        for key in ("summary", "reason"):
            value = item[key]
            if type(value) is not str or value.strip() == "" or any(ch in value for ch in "\r\n"):
                raise Hold(f"editor note {key} is blank")
    generated_by = notes["generated_by"]
    require_keys(generated_by, {"model"}, "generated_by")
    model = generated_by["model"]
    if type(model) is not str or model.strip() == "" or any(ch in model for ch in "\r\n"):
        raise Hold("unknown editor notes schema")
    return notes


def assert_headline_block(html_text, edition):
    """The h1 stays the edition title. A headline, if any, follows it in p.ds-headline."""
    title_h1 = f"<h1>{html.escape(edition['title'], quote=True)}</h1>"
    block = headline_block(edition)
    if not block:
        if 'class="ds-headline"' in html_text:
            raise Hold("edition headline does not match")
        return
    if html_text.count(block) != 1:
        raise Hold("edition headline does not match")
    if html_text.index(block) < html_text.index(title_h1):
        raise Hold("headline must sit under the h1")


def assert_edition_page(html_text, edition):
    """h1, og:url, canonical, Spotify href, and the AI label, once each."""
    title = edition["title"]
    h1 = f"<h1>{html.escape(title, quote=True)}</h1>"
    if h1 not in html_text:
        raise Hold("edition h1 does not match")
    assert_headline_block(html_text, edition)
    canonical = edition["canonical_url"]
    escaped = html.escape(canonical, quote=True)
    og = f'<meta property="og:url" content="{escaped}">'
    if html_text.count(og) != 1:
        raise Hold("og:url does not match the edition")
    canonical_link = f'<link rel="canonical" href="{escaped}">'
    if canonical_link not in html_text:
        raise Hold("canonical url does not match the edition")
    spotify = (
        f'<a href="{html.escape(edition["episode_url"], quote=True)}">Audio on Spotify</a>'
    )
    if html_text.count(spotify) != 1:
        raise Hold("hard stop: audio: missing or broken audio reference")
    sources_link = (
        f'<a href="{html.escape(sources_page_url(edition["date"]), quote=True)}">Sources</a>'
    )
    if html_text.count(sources_link) != 1:
        raise Hold("sources link is missing")
    if html_text.count(AI_LABEL_EXACT) != 1 or count_ai_labels(html_text) != 1:
        raise Hold("hard stop: label: AI-generated label must appear exactly once")
    assert_disclaimer_above_script(html_text)


def assert_disclaimer_above_script(html_text):
    """The house label sits once, under the top links and above the script."""
    marker = '<p class="disclaimer">'
    if html_text.count(marker) != 1:
        raise Hold("hard stop: label: AI-generated label must appear exactly once")
    if "<div class=\"script\">" not in html_text:
        raise Hold("edition script is missing")
    if html_text.index(marker) > html_text.index('<div class="script">'):
        raise Hold("disclaimer must sit above the script")


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


def is_x_post_url(url):
    return bool(X_POST_RE.match(url))


def source_link_label(url):
    """Readable label for a source URL. X posts become '@handle on X'."""
    matched = X_POST_RE.match(url)
    if matched:
        handle = matched.group(1)
        if handle.lower() not in {"i", "intent", "share"}:
            return f"@{handle} on X"
        return "Post on X"
    return url


def primary_source_url(urls):
    """Prefer a non-X URL as the story title target, else the first URL."""
    for url in urls:
        if not is_x_post_url(url):
            return url
    return urls[0]


def story_meta_line(story):
    """Outlet / author / date / verification, when the source record has them."""
    parts = []
    outlets = story.get("outlets") or []
    if type(outlets) is list:
        named = [outlet.strip() for outlet in outlets if type(outlet) is str and outlet.strip()]
        if named:
            parts.append(", ".join(named))
    for key in ("author", "by", "date", "published", "published_at", "published_on"):
        value = story.get(key)
        if type(value) is str and value.strip():
            parts.append(value.strip())
    status = story.get("verification_status")
    if type(status) is str and status.strip():
        parts.append(status.replace("_", " "))
    return " \u00b7 ".join(parts)


def render_sources_page_list(sources):
    """Story groups for the dedicated Sources page. Title links to the primary URL."""
    blocks = []
    represented = set()
    for story in sources["stories"]:
        urls = story["urls"]
        for url in urls:
            represented.add(url)
        primary = html.escape(primary_source_url(urls), quote=True)
        title = html.escape(story["title"], quote=True)
        meta = story_meta_line(story)
        meta_html = f"<p>{html.escape(meta, quote=True)}</p>\n" if meta else ""
        links = "\n".join(
            f'<li><a href="{html.escape(url, quote=True)}">'
            f"{html.escape(source_link_label(url), quote=True)}</a></li>"
            for url in urls
        )
        blocks.append(
            "<section class=\"story\">\n"
            f"<h2><a href=\"{primary}\">{title}</a></h2>\n"
            f"{meta_html}"
            f"<ul>\n{links}\n</ul>\n"
            "</section>"
        )
    extra = [url for url in sources["urls"] if url not in represented]
    if extra:
        links = "\n".join(
            f'<li><a href="{html.escape(url, quote=True)}">'
            f"{html.escape(source_link_label(url), quote=True)}</a></li>"
            for url in extra
        )
        blocks.append(
            "<section class=\"story\">\n"
            "<h2>Other URLs</h2>\n"
            f"<ul>\n{links}\n</ul>\n"
            "</section>"
        )
    return "\n".join(blocks)


def render_sources_page_html(iso_date, sources, variant=None, edition=None):
    """Readable Sources page at /daily-state/<date>/sources/ (or .../<variant>/sources/)."""
    kicker = edition_title(iso_date)
    heading = "Sources"
    if edition is not None:
        page_title = f"Sources \u2014 {edition['title']}"
    else:
        page_title = f"Sources \u2014 {kicker}"
    listing = render_sources_page_list(sources)
    raw_href = html.escape(variant_asset_url(iso_date, variant, "sources.json"), quote=True)
    main = (
        "<article>\n"
        f"<p class=\"kicker\">{html.escape(kicker, quote=True)}</p>\n"
        f"<h1>{html.escape(heading, quote=True)}</h1>\n"
        f"{listing}\n"
        f"<p><a href=\"{raw_href}\">Raw data</a></p>\n"
        "<p><a href=\"../\">Back to the edition</a></p>\n"
        "</article>"
    )
    if variant is None:
        root, path = "../../../", f"/daily-state/{iso_date}/sources/"
    else:
        root, path = "../../../../", f"/daily-state/{iso_date}/{variant}/sources/"
    return render_page(
        page_title,
        f"Sources for {kicker}.",
        root,
        main,
        path,
        "article",
    )


def assert_sources_page(html_text, iso_date, sources, variant=None, edition=None):
    """Kicker, title, back link, raw JSON link, and every source URL."""
    kicker = edition_title(iso_date)
    kicker_html = f'<p class="kicker">{html.escape(kicker, quote=True)}</p>'
    if html_text.count(kicker_html) != 1:
        raise Hold("sources page kicker does not match")
    if html_text.count("<h1>Sources</h1>") != 1:
        raise Hold("sources page title does not match")
    if '<p><a href="../">Back to the edition</a></p>' not in html_text:
        raise Hold("sources page is missing the back link")
    raw = variant_asset_url(iso_date, variant, "sources.json")
    raw_link = f'<a href="{html.escape(raw, quote=True)}">Raw data</a>'
    if html_text.count(raw_link) != 1:
        raise Hold("sources page is missing the raw data link")
    for url in sources["urls"]:
        href = f'href="{html.escape(url, quote=True)}"'
        if href not in html_text:
            raise Hold("sources page is missing a source url")
    for story in sources["stories"]:
        if html.escape(story["title"], quote=True) not in html_text:
            raise Hold("sources page is missing a story title")
    if html_text.count(AI_LABEL_EXACT) != 0 or count_ai_labels(html_text) != 0:
        raise Hold("sources page must not carry the AI-generated label")
    page_url = f"{BASE_URL}{sources_page_url(iso_date, variant)}"
    escaped = html.escape(page_url, quote=True)
    canonical = f'<link rel="canonical" href="{escaped}">'
    if canonical not in html_text:
        raise Hold("sources page canonical url does not match")
    og = f'<meta property="og:url" content="{escaped}">'
    if html_text.count(og) != 1:
        raise Hold("sources page og:url does not match")


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


def styles_cache_token():
    """Short hash of styles.css so Daily State pages pick up CSS changes immediately."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()[:8]


def render_page(title, description, root, main, path, ogtype):
    page = build.render(title, description, root, main, path, ogtype=ogtype)
    page = apply_daily_footer(page, root)
    href = f"{root}styles.css"
    needle = f'<link rel="stylesheet" href="{href}">'
    versioned = f'<link rel="stylesheet" href="{href}?v={styles_cache_token()}">'
    if needle not in page:
        raise Hold("stylesheet link is missing")
    return page.replace(needle, versioned, 1)


def render_edition_html(edition, paragraphs, sources, *, editor_mode=False):
    # The description stays on the frozen script. The body omits a duplicate
    # AI label; p.disclaimer under the top links is the one copy on the page.
    body = "\n".join(
        f"<p>{html.escape(paragraph, quote=True)}</p>"
        for paragraph in body_paragraphs(paragraphs)
    )
    shown = build.display_date(edition["date"], "day")
    audio = (
        f"<a href=\"{html.escape(edition['episode_url'], quote=True)}\">Audio on Spotify</a>"
    )
    if editor_mode and edition.get("video_url"):
        audio += (
            " · "
            f"<a href=\"{html.escape(edition['video_url'], quote=True)}\">Video</a>"
        )
    if editor_mode:
        disclaimer = (
            f"<p class=\"disclaimer\">{AI_LABEL_EXACT}"
            " · <a href=\"editors-notes/\">Editor's notes</a></p>"
        )
    else:
        disclaimer = f"<p class=\"disclaimer\">{AI_LABEL_EXACT}</p>"
    main = (
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(edition['title'], quote=True)}</h1>\n"
        f"{headline_block(edition)}"
        f"<p><time datetime=\"{edition['date']}\">{html.escape(shown)}</time></p>\n"
        f"<p>{audio}</p>\n"
        f"<p><a href=\"{html.escape(sources_page_url(edition['date']), quote=True)}\">Sources</a></p>\n"
        f"{disclaimer}\n"
        "<div class=\"script\">\n"
        f"{body}\n"
        "</div>\n"
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


def render_editors_notes_html(iso_date, notes):
    """Outstanding items only, grouped by artifact. Overruled objections stay off."""
    title = f"Editor's notes — {iso_date}"
    shown = build.display_date(iso_date, "day")
    grouped = {key: [] for key, _label in EDITOR_NOTE_GROUPS}
    for item in notes["outstanding"]:
        status = item.get("status")
        artifact = item.get("artifact")
        if status not in EDITOR_NOTE_STATUS_LABELS or artifact not in grouped:
            continue
        grouped[artifact].append(item)
    sections = []
    for key, label in EDITOR_NOTE_GROUPS:
        items = grouped[key]
        if not items:
            continue
        blocks = []
        for item in items:
            blocks.append(
                "<section class=\"story\">\n"
                f"<p>{html.escape(item['summary'], quote=True)}</p>\n"
                f"<p class=\"note\">{html.escape(item['reason'], quote=True)}</p>\n"
                f"<p class=\"row\"><span class=\"meta\">"
                f"{html.escape(EDITOR_NOTE_STATUS_LABELS[item['status']], quote=True)}</span></p>\n"
                "</section>"
            )
        sections.append("<h2>%s</h2>\n%s" % (html.escape(label, quote=True), "\n".join(blocks)))
    if sections:
        listing = "\n".join(sections)
    else:
        listing = "<p>No outstanding issues</p>"
    main = (
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(title, quote=True)}</h1>\n"
        f"<p><time datetime=\"{iso_date}\">{html.escape(shown)}</time></p>\n"
        "<p class=\"intro\">Outstanding items from the editor pass.</p>\n"
        f"{listing}\n"
        "<p><a href=\"../\">Back to the edition</a></p>\n"
        "</article>"
    )
    return render_page(
        title,
        f"Outstanding items from the editor pass for {edition_title(iso_date)}.",
        "../../../",
        main,
        f"/daily-state/{iso_date}/editors-notes/",
        "article",
    )


def audit_title(iso_date, variant):
    if variant is None:
        return edition_title(iso_date)
    if variant == "neon":
        return f"{edition_title(iso_date)} (Gemini 4 Neon, raw)"
    raise Hold("unknown variant")


def audit_page_url(iso_date, variant):
    if variant is None:
        return edition_url(iso_date)
    return f"{BASE_URL}/daily-state/{iso_date}/{variant}/"


def variant_asset_url(iso_date, variant, name):
    if variant is None:
        return f"/content/daily-state/{iso_date}/{name}"
    return f"/content/daily-state/{iso_date}/{variant}/{name}"


def sources_page_url(iso_date, variant=None):
    """Site-relative URL of the readable Sources page."""
    if variant is None:
        return f"/daily-state/{iso_date}/sources/"
    return f"/daily-state/{iso_date}/{variant}/sources/"


def audit_model_label(model, variant):
    if variant in (None, "neon") and model == NEON_MODEL:
        return "Google Gemini 4 Neon"
    raise Hold("edition model does not match the variant")


def audit_check_href(iso_date, variant, check_file):
    if variant is None:
        prefix = f"content/daily-state/{iso_date}/audit/"
    else:
        prefix = f"content/daily-state/{iso_date}/{variant}/audit/"
    return REPO_FILE_URL + prefix + check_file


def variant_subfolders(directory):
    """Known variant directories. A file that uses a variant name still holds."""
    found = []
    for name in sorted(os.listdir(directory)):
        if name not in VARIANT_NAMES:
            continue
        path = os.path.join(directory, name)
        if os.path.islink(path) or not os.path.isdir(path):
            raise Hold(f"unexpected content entry: {name}")
        assert_real_child(directory, path, name)
        found.append(name)
    return found


def _listing_key(item):
    parts = [int(part) for part in item["date"].split("-")]
    variant = item.get("variant") or ""
    rank = 1 if variant else 0
    return (-parts[0], -parts[1], -parts[2], rank, variant)


def audit_counts(results):
    counts = {
        artifact: {status: 0 for status in AUDIT_STATUSES}
        for artifact in AUDIT_ARTIFACTS
    }
    for item in results:
        counts[item["artifact"]][item["status"]] += 1
    return counts


def require_audit_counts(actual, claimed, label):
    for artifact in AUDIT_ARTIFACTS:
        row = claimed.get(artifact) if type(claimed) is dict else None
        if row is None and type(claimed) is dict and not any(actual[artifact].values()):
            # An audit of the episode alone (no short that day) has no short row.
            continue
        if type(row) is not dict or set(row) != set(AUDIT_STATUSES):
            raise Hold(f"{label} counts are invalid")
        for status in AUDIT_STATUSES:
            if type(row[status]) is not int or row[status] != actual[artifact][status]:
                raise Hold(f"{label} counts do not match the audit results")


def validate_audit_edition(edition, iso_date, variant):
    """Audit receipt only. A QA pass or an editor receipt is a different mode."""
    require_keys(edition, AUDIT_EDITION_KEYS, "edition.json", optional=HEADLINE_OPTIONAL)
    apply_headline(edition)
    if type(edition["schema_version"]) is not int or edition["schema_version"] != SCHEMA_VERSION:
        raise Hold("unknown edition schema")
    if edition["mode"] != "audit" or edition["variant"] != variant:
        raise Hold("unknown edition schema")
    if not is_real_date(edition["date"]) or edition["date"] != iso_date:
        raise Hold("edition date does not match")
    if edition["title"] != audit_title(iso_date, variant):
        raise Hold("edition title does not match the date")
    if edition["canonical_url"] != audit_page_url(iso_date, variant):
        raise Hold("edition canonical url does not match the date")
    if type(edition["model"]) is not str or edition["model"].strip() == "":
        raise Hold("edition model is missing")
    if type(edition["reasoning_effort"]) is not str or edition["reasoning_effort"].strip() == "":
        raise Hold("edition reasoning effort is missing")
    if edition["audio_url"] != variant_asset_url(iso_date, variant, "episode.mp3"):
        raise Hold("edition audio url does not match")
    if edition["video_url"] != variant_asset_url(iso_date, variant, "short.mp4"):
        raise Hold("edition video url does not match")
    if edition["sources_url"] != sources_page_url(iso_date, variant):
        raise Hold("edition sources url does not match")
    receipt = edition["audit"]
    if type(receipt) is not dict:
        raise Hold("unknown edition schema")
    require_keys(receipt, AUDIT_RECEIPT_KEYS, "audit receipt")
    if receipt["gate"] is not False:
        raise Hold("audit edition must not be recorded as a gate")
    if type(receipt["sha256"]) is not str or not SHA256_RE.fullmatch(receipt["sha256"]):
        raise Hold("audit receipt hash is malformed")
    hashes = edition["hashes"]
    require_keys(hashes, AUDIT_HASH_KEYS, "hashes")
    for key in AUDIT_HASH_KEYS:
        if type(hashes[key]) is not str or not SHA256_RE.fullmatch(hashes[key]):
            raise Hold(f"{key} is malformed")
    if hashes["audit_sha256"] != receipt["sha256"]:
        raise Hold("audit receipt does not match audit.json")
    return edition


def validate_neon_run(run, iso_date, variant):
    """The raw run is evidence. It is not a QA snapshot and it is not copied into one."""
    if type(run) is not dict:
        raise Hold("unknown neon run schema")
    if run.get("date") != iso_date:
        raise Hold("neon run date does not match the edition")
    if variant is None:
        if run.get("pipeline") != ROOT_NEON_PIPELINE:
            raise Hold("neon run pipeline is not the daily neon pipeline")
        if run.get("model") != NEON_MODEL:
            raise Hold("neon run model does not match")
        if run.get("status") != "ok":
            raise Hold("neon run did not finish")
    if variant == "neon":
        if run.get("pipeline") != "neon-minimal-raw":
            raise Hold("neon run pipeline is not the raw edition")
        if run.get("model") != "google/gemini-4-neon":
            raise Hold("neon run model does not match")
    effort = run.get("reasoning_effort")
    if type(effort) is not str or not re.fullmatch(r"[A-Za-z0-9-]{1,32}", effort):
        raise Hold("neon run reasoning effort is invalid")
    if run.get("editor") is not None or run.get("qa") is not None:
        raise Hold("audit edition must not carry an editor or QA receipt")
    if run.get("system_prompt") is not None:
        raise Hold("audit edition must not carry a system prompt")
    edits = run.get("edits_after_generation")
    if type(edits) is not str or not edits.startswith("none"):
        raise Hold("audit edition was edited")
    prompts = run.get("prompts")
    if type(prompts) is not dict or type(prompts.get("episode")) is not str or prompts["episode"].strip() == "":
        raise Hold("neon run prompt is missing")
    audit = run.get("audit")
    if type(audit) is not dict or audit.get("gate") is not False:
        raise Hold("audit edition must not be recorded as a gate")
    if variant is not None and type(audit.get("summary")) is not dict:
        raise Hold("neon run audit summary is missing")
    return run


def validate_audit_document(audit, iso_date, script_sha):
    if type(audit) is not dict or set(audit) != {"meta", "results"}:
        raise Hold("unknown audit schema")
    meta = audit["meta"]
    results = audit["results"]
    if type(meta) is not dict or type(results) is not list or not results:
        raise Hold("unknown audit schema")
    if meta.get("date") != iso_date:
        raise Hold("audit date does not match the edition")
    artifacts = meta.get("artifacts")
    if type(artifacts) is not dict or type(artifacts.get("episode")) is not dict:
        raise Hold("unknown audit schema")
    if artifacts["episode"].get("sha256") != script_sha:
        raise Hold("audit script hash does not match script.txt")
    summary = meta.get("summary")
    if type(summary) is not dict:
        raise Hold("audit summary is missing")
    seen = set()
    clean = []
    for item in results:
        if type(item) is not dict:
            raise Hold("audit result is invalid")
        for key in ("id", "artifact", "quote", "status", "source_quote", "check_file", "note"):
            if key not in item:
                raise Hold("audit result is invalid")
        if type(item["id"]) is not str or not re.fullmatch(r"[a-z0-9-]{1,80}", item["id"]):
            raise Hold("audit result id is invalid")
        if item["id"] in seen:
            raise Hold("audit result id is duplicated")
        seen.add(item["id"])
        if item["artifact"] not in AUDIT_ARTIFACTS:
            raise Hold("audit result artifact is invalid")
        if item["status"] not in AUDIT_STATUSES:
            raise Hold("audit result status is invalid")
        if type(item["note"]) is not str:
            raise Hold("audit result note is invalid")
        quote = item["quote"]
        if quote is not None and (type(quote) is not str or quote.strip() == ""):
            raise Hold("audit result claim is blank")
        if quote is None and item["note"].strip() == "":
            raise Hold("audit result claim is blank")
        if item["source_quote"] is not None and type(item["source_quote"]) is not str:
            raise Hold("audit result source quote is invalid")
        if type(item["check_file"]) is not str:
            raise Hold("audit result check is invalid")
        clean.append(item)
    counts = audit_counts(clean)
    require_audit_counts(counts, summary, "audit.json")
    return clean, counts


def audit_check_path(directory, iso_date, item):
    rel = item["check_file"]
    expected = f"checks/{iso_date}/{item['id']}.py"
    if rel != expected:
        raise Hold("audit check path does not match the claim")
    path = _within_directory(os.path.join(directory, "audit"), rel)
    if path is None or os.path.islink(path) or not os.path.isfile(path):
        raise Hold("audit check script is missing")
    return rel


def assert_audit_directory(directory):
    files = []
    dirs = []
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.islink(path):
            raise Hold(f"unexpected content entry: {name}")
        if os.path.isdir(path):
            dirs.append(name)
        elif os.path.isfile(path):
            files.append(name)
        else:
            raise Hold(f"unexpected content entry: {name}")
    if files != sorted(AUDIT_ROOT_FILES) or dirs != ["audit"]:
        raise Hold("edition directory does not contain the frozen public inputs")
    audit_json = os.path.join(directory, "audit", "audit.json")
    if os.path.islink(audit_json) or not os.path.isfile(audit_json):
        raise Hold("missing audit.json")


def check_audit_hashes(edition, raw):
    actual = {
        "script_sha256": sha256_bytes(raw["script.txt"]),
        "sources_sha256": sha256_bytes(raw["sources.json"]),
        "neon_run_sha256": sha256_bytes(raw["neon_run.json"]),
        "audit_sha256": sha256_bytes(raw["audit.json"]),
        "episode_sha256": sha256_bytes(raw["episode.mp3"]),
        "short_sha256": sha256_bytes(raw["short.mp4"]),
    }
    for key, value in actual.items():
        if edition["hashes"][key] != value:
            raise Hold(f"{key} does not match the frozen bytes")


def assert_audit_edition_page(html_text, edition, prompt):
    title = edition["title"]
    h1 = f"<h1>{html.escape(title, quote=True)}</h1>"
    if h1 not in html_text:
        raise Hold("edition h1 does not match")
    assert_headline_block(html_text, edition)
    canonical = edition["canonical_url"]
    escaped = html.escape(canonical, quote=True)
    og = f'<meta property="og:url" content="{escaped}">'
    if html_text.count(og) != 1:
        raise Hold("og:url does not match the edition")
    canonical_link = f'<link rel="canonical" href="{escaped}">'
    if canonical_link not in html_text:
        raise Hold("canonical url does not match the edition")
    if edition.get("variant") is None and root_audit_keeps_player(edition, edition["date"]):
        audio = f'<audio controls src="{html.escape(edition["audio_url"], quote=True)}"></audio>'
        spotify = (
            f'<p><a href="{html.escape(edition["episode_url"], quote=True)}">Audio on Spotify</a></p>'
        )
        if html_text.count(f"<p>{audio}</p>\n{spotify}") != 1 or html_text.count(spotify) != 1:
            raise Hold("hard stop: audio: missing or broken audio reference")
    elif edition.get("variant") is None and root_audit_uses_spotify(edition):
        spotify = (
            f'<a href="{html.escape(edition["episode_url"], quote=True)}">Audio on Spotify</a>'
        )
        if html_text.count(spotify) != 1:
            raise Hold("hard stop: audio: missing or broken Spotify episode link")
        if "<audio" in html_text:
            raise Hold("hard stop: audio: a Spotify edition must not self-host episode.mp3")
    else:
        audio = f'<audio controls src="{html.escape(edition["audio_url"], quote=True)}"></audio>'
        if html_text.count(audio) != 1:
            raise Hold("hard stop: audio: missing or broken audio reference")
        if "open.spotify.com" in html_text or "Audio on Spotify" in html_text:
            raise Hold("audit edition must not link Spotify")
    if edition["video_url"] is not None:
        short = f'<a href="{html.escape(edition["video_url"], quote=True)}">Short</a>'
        if html_text.count(short) != 1:
            raise Hold("hard stop: video: missing short")
    elif ">Short</a>" in html_text:
        raise Hold("hard stop: video: short link without a short")
    sources_link = f'<a href="{html.escape(edition["sources_url"], quote=True)}">Sources</a>'
    if html_text.count(sources_link) != 1:
        raise Hold("sources link is missing")
    audit_link = '<p><a href="audit/">Audit</a></p>'
    disclaimer = f'<p class="disclaimer">{AI_LABEL_EXACT}</p>'
    if html_text.count(audit_link) != 1:
        raise Hold("hard stop: label: missing Audit link")
    if html_text.count(disclaimer) != 1 or html_text.count(AI_LABEL_EXACT) != 1:
        raise Hold("hard stop: label: AI-generated label must appear exactly once")
    if count_ai_labels(html_text) != 1:
        raise Hold("hard stop: label: AI-generated label must appear exactly once")
    assert_disclaimer_above_script(html_text)
    if html_text.index(audit_link) > html_text.index(disclaimer):
        raise Hold("audit link must sit with the top links, above the disclaimer")
    if html.escape(prompt, quote=True) not in html_text:
        raise Hold("edition prompt does not match the neon run")
    if '<figure class="ds-prompt">' not in html_text:
        raise Hold("edition prompt box is missing")
    if '<figcaption class="kicker ds-prompt-label">Minimal prompt</figcaption>' not in html_text:
        raise Hold("edition prompt is missing the Minimal prompt label")
    if "semantic_qa" in html_text or "qa.json" in html_text:
        raise Hold("audit edition must not carry a QA receipt")


def render_audit_edition_html(edition, paragraphs, sources, prompt, variant):
    body = "\n".join(
        f"<p>{html.escape(paragraph, quote=True)}</p>"
        for paragraph in body_paragraphs(paragraphs)
    )
    shown = build.display_date(edition["date"], "day")
    label = html.escape(audit_model_label(edition["model"], variant), quote=True)
    effort = html.escape(edition["reasoning_effort"], quote=True)
    note = (
        f"Written by {label} ({effort}) from one minimal prompt, "
        "with no rules, editor or edits, published as produced."
    )
    quoted = (
        "<figure class=\"ds-prompt\">\n"
        "<figcaption class=\"kicker ds-prompt-label\">Minimal prompt</figcaption>\n"
        "<blockquote>\n"
        "<pre>" + html.escape(prompt, quote=True) + "</pre>\n"
        "</blockquote>\n"
        "</figure>"
    )
    spotify_link = None
    if variant is None and root_audit_uses_spotify(edition):
        spotify_link = (
            f"<a href=\"{html.escape(edition['episode_url'], quote=True)}\">Audio on Spotify</a>"
        )
    if spotify_link and not root_audit_keeps_player(edition, edition["date"]):
        audio = spotify_link
    else:
        audio = (
            f"<audio controls src=\"{html.escape(edition['audio_url'], quote=True)}\"></audio>"
        )
        if spotify_link:
            # 2026-11-21: the Spotify link sits under the self-hosted player.
            audio += f"</p>\n<p>{spotify_link}"
    link_parts = []
    if edition["video_url"] is not None:
        link_parts.append(f"<a href=\"{html.escape(edition['video_url'], quote=True)}\">Short</a>")
    link_parts.append(f"<a href=\"{html.escape(edition['sources_url'], quote=True)}\">Sources</a>")
    links = " · ".join(link_parts)
    audit_link = '<p><a href="audit/">Audit</a></p>'
    disclaimer = f'<p class="disclaimer">{AI_LABEL_EXACT}</p>'
    main = (
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(edition['title'], quote=True)}</h1>\n"
        f"{headline_block(edition)}"
        f"<p><time datetime=\"{edition['date']}\">{html.escape(shown)}</time></p>\n"
        f"<p class=\"intro\">{note}</p>\n"
        f"{quoted}\n"
        f"<p>{audio}</p>\n"
        f"<p>{links}</p>\n"
        f"{audit_link}\n"
        f"{disclaimer}\n"
        "<div class=\"script\">\n"
        f"{body}\n"
        "</div>\n"
        "<section class=\"sources\">\n"
        "<h2>Sources</h2>\n"
        f"{render_sources(sources)}\n"
        "</section>\n"
        "</article>"
    )
    if variant is None:
        root, path = "../../", f"/daily-state/{edition['date']}/"
    else:
        root, path = "../../../", f"/daily-state/{edition['date']}/{variant}/"
    return render_page(
        edition["title"],
        description_from_paragraphs(paragraphs),
        root,
        main,
        path,
        "article",
    )


def audit_claim_text(item):
    """Spoken claim, or the omission note when the check has no quote."""
    if type(item["quote"]) is str and item["quote"].strip() != "":
        return item["quote"]
    return item["note"]


def render_audit_item(edition, item, variant):
    claim = html.escape(audit_claim_text(item), quote=True)
    status = html.escape(item["status"], quote=True)
    if item["source_quote"] is None:
        quote = "(none)"
    else:
        quote = html.escape(item["source_quote"], quote=True)
    href = html.escape(audit_check_href(edition["date"], variant, item["check_file"]), quote=True)
    check = html.escape(item["check_file"], quote=True)
    open_attr = " open" if item["status"] in AUDIT_OPEN_STATUSES else ""
    note = ""
    if item["note"].strip() and item["note"] != audit_claim_text(item):
        note = f"<p>{html.escape(item['note'], quote=True)}</p>\n"
    return (
        f"<details{open_attr}>\n"
        f"<summary>{status} · {claim}</summary>\n"
        f"<p>Claim: {claim}</p>\n"
        f"<p>Result: {status}</p>\n"
        f"<p>Source quote: {quote}</p>\n"
        f"{note}"
        f"<p><a href=\"{href}\">{check}</a></p>\n"
        "</details>"
    )


def _audit_count_line(label, row):
    text = (
        f"{label} {row['PASS']} PASS / {row['FAIL']} FAIL / "
        f"{row['NEEDS-HUMAN']} NEEDS-HUMAN"
    )
    if row["ERROR"]:
        text += f" / {row['ERROR']} ERROR"
    return f"<p class=\"row\">{html.escape(text, quote=True)}</p>"


def render_audit_html(edition, results, counts, variant):
    iso_date = edition["date"]
    title = f"Audit — {edition['title']}"
    shown = build.display_date(iso_date, "day")
    summary_lines = [
        _audit_count_line("Episode", counts["episode"]),
        _audit_count_line("Short", counts["short"]),
    ]
    if any(counts["takeaways"].values()):
        summary_lines.append(_audit_count_line("Takeaways", counts["takeaways"]))
    summary = "\n".join(summary_lines)
    explanation = (
        "<p>Each claim is a small Python check run against the source texts. "
        "The audit is for transparency and is not a gate.</p>"
    )
    buckets = {
        artifact: {status: [] for status in AUDIT_STATUS_ORDER}
        for artifact in AUDIT_ARTIFACTS
    }
    for item in results:
        buckets[item["artifact"]][item["status"]].append(item)
    headings = {"episode": "Episode", "short": "Short", "takeaways": "Takeaways"}
    groups = []
    for artifact in AUDIT_ARTIFACTS:
        blocks = []
        for status in AUDIT_STATUS_ORDER:
            for item in buckets[artifact][status]:
                blocks.append(render_audit_item(edition, item, variant))
        if not blocks:
            continue
        groups.append(f"<h2>{headings[artifact]}</h2>\n" + "\n".join(blocks))
    main = (
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(title, quote=True)}</h1>\n"
        f"<p><time datetime=\"{iso_date}\">{html.escape(shown)}</time></p>\n"
        f"{summary}\n"
        f"{explanation}\n"
        + "\n".join(groups)
        + "\n<p><a href=\"../\">Back to the edition</a></p>\n"
        "</article>"
    )
    if variant is None:
        root, path = "../../../", f"/daily-state/{iso_date}/audit/"
    else:
        root, path = "../../../../", f"/daily-state/{iso_date}/{variant}/audit/"
    return render_page(
        title,
        f"Claim audit for {edition['title']}. The audit is for transparency and is not a gate.",
        root,
        main,
        path,
        "article",
    )


def render_audit_pending_html(edition):
    """Placeholder until the executable audit is attached. Only this page may change later."""
    iso_date = edition["date"]
    title = f"Audit — {edition['title']}"
    shown = build.display_date(iso_date, "day")
    main = (
        f"{AUDIT_PENDING_MARKER}\n"
        "<article>\n"
        "<p class=\"kicker\">Daily State of AI</p>\n"
        f"<h1>{html.escape(title, quote=True)}</h1>\n"
        f"<p><time datetime=\"{iso_date}\">{html.escape(shown)}</time></p>\n"
        "<p>The executable claim audit for this edition runs after publication and will appear here. "
        "The audit is for transparency and is not a gate.</p>\n"
        "<p><a href=\"../\">Back to the edition</a></p>\n"
        "</article>"
    )
    return render_page(
        title,
        f"Claim audit for {edition['title']} (pending).",
        "../../../",
        main,
        f"/daily-state/{iso_date}/audit/",
        "article",
    )


def _load_audit_edition(directory, iso_date, variant, *, link_opener=None):
    if not is_real_date(iso_date):
        raise Hold("edition date is invalid")
    if os.path.islink(directory) or not os.path.isdir(directory):
        raise Hold("missing edition directory")
    parent = os.path.basename(os.path.dirname(os.path.abspath(directory)))
    if parent != iso_date:
        raise Hold("edition date does not match")
    assert_audit_directory(directory)
    raw = _read_named(directory, AUDIT_ROOT_FILES)
    audit_path = os.path.join(directory, "audit", "audit.json")
    assert_real_child(directory, audit_path, "audit.json")
    raw["audit.json"] = read_stable(audit_path)
    script_text = decode_utf8(raw["script.txt"], "script.txt")
    paragraphs = script_paragraphs(script_text)
    sources = parse_json_object(raw["sources.json"], "sources.json")
    edition = parse_json_object(raw["edition.json"], "edition.json")
    run = parse_json_object(raw["neon_run.json"], "neon_run.json")
    audit = parse_json_object(raw["audit.json"], "audit.json")
    validate_audit_edition(edition, iso_date, variant)
    validate_neon_run(run, iso_date, variant)
    urls = sources.get("urls")
    source_count = len(urls) if type(urls) is list else 0
    validate_sources(sources, iso_date, source_count, audit=True)
    script_sha = sha256_bytes(raw["script.txt"])
    results, counts = validate_audit_document(audit, iso_date, script_sha)
    for item in results:
        audit_check_path(directory, iso_date, item)
    check_audit_hashes(edition, raw)
    if edition["model"] != run["model"] or edition["reasoning_effort"] != run["reasoning_effort"]:
        raise Hold("edition receipt does not match the neon run")
    require_audit_counts(counts, {
        "episode": edition["audit"]["episode"],
        "short": edition["audit"]["short"],
    }, "edition.json")
    require_audit_counts(counts, run["audit"]["summary"], "neon run")
    problem = _local_media_problem("audio", "episode.mp3", directory)
    if problem:
        raise Hold(f"hard stop: audio: {problem}")
    problem = _local_media_problem("video", "short.mp4", directory)
    if problem:
        raise Hold(f"hard stop: video: {problem}")
    prompt = run["prompts"]["episode"]
    html_text = render_audit_edition_html(edition, paragraphs, sources, prompt, variant)
    audit_html = render_audit_html(edition, results, counts, variant)
    sources_html = render_sources_page_html(iso_date, sources, variant, edition)
    assert_audit_edition_page(html_text, edition, prompt)
    assert_sources_page(sources_html, iso_date, sources, variant, edition)
    if link_opener is not None:
        raise_hard_stops(source_link_hard_stops(sources["urls"], link_opener))
    loaded = {
        "date": iso_date,
        "variant": variant,
        "paragraphs": paragraphs,
        "sources": sources,
        "qa": None,
        "edition": edition,
        "notes": None,
        "editor_mode": False,
        "audit_mode": True,
        "html": html_text,
        "notes_html": None,
        "audit_html": audit_html,
        "sources_html": sources_html,
        "audit_counts": counts,
        "prompt": prompt,
    }
    loaded["files"] = _edition_files(loaded)
    return loaded


def directory_declares_root_audit(directory):
    """True when the date directory's edition.json is a daily audit edition."""
    path = os.path.join(directory, "edition.json")
    if os.path.islink(path) or not os.path.isfile(path):
        return False
    try:
        edition = json.loads(read_stable(path).decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    return type(edition) is dict and edition.get("mode") == "audit" and edition.get("variant") is None


def root_audit_uses_spotify(edition):
    """True for the Spotify-linked daily audit edition (from 2026-11-22)."""
    return type(edition) is dict and any(key in edition for key in ROOT_AUDIT_SPOTIFY_KEYS)


def root_audit_keeps_player(edition, iso_date):
    """2026-11-21 only: the self-hosted player stays and the Spotify link is added under it."""
    return (
        root_audit_uses_spotify(edition)
        and edition.get("audio_url") is not None
        and is_real_date(iso_date)
        and iso_date <= SELF_HOSTED_AUDIO_LAST_DATE
    )


def validate_root_audit_audio(edition, iso_date):
    """Spotify episode link with recorded public verification, as pre-audit editions."""
    require_keys(edition, AUDIT_EDITION_KEYS | ROOT_AUDIT_SPOTIFY_KEYS, "edition.json", optional=HEADLINE_OPTIONAL)
    if root_audit_keeps_player(edition, iso_date):
        if edition["audio_url"] != variant_asset_url(iso_date, None, "episode.mp3"):
            raise Hold("edition audio url does not match")
    elif edition["audio_url"] is not None:
        raise Hold("hard stop: audio: a Spotify edition must not self-host episode.mp3")
    elif edition["hashes"].get("episode_sha256") is not None:
        raise Hold("hard stop: audio: a Spotify edition must not self-host episode.mp3")
    verified = edition["verified_at"]
    matched = VERIFIED_AT_RE.fullmatch(verified) if type(verified) is str else None
    if not matched or matched.group(1) != iso_date:
        raise Hold("verification time is missing or stale")
    episode_url = edition["episode_url"]
    episode_id = episode_id_from_url(episode_url)
    if edition["episode_id"] != episode_id:
        raise Hold("episode id does not match the episode url")
    validate_recorded_verification(edition, iso_date, episode_url, episode_id)


def validate_root_audit_edition(edition, iso_date, has_short):
    spotify = root_audit_uses_spotify(edition)
    if spotify:
        require_keys(edition, AUDIT_EDITION_KEYS | ROOT_AUDIT_SPOTIFY_KEYS, "edition.json", optional=HEADLINE_OPTIONAL)
    else:
        require_keys(edition, AUDIT_EDITION_KEYS, "edition.json", optional=HEADLINE_OPTIONAL)
    apply_headline(edition)
    if type(edition["schema_version"]) is not int or edition["schema_version"] != SCHEMA_VERSION:
        raise Hold("unknown edition schema")
    if edition["mode"] != "audit" or edition["variant"] is not None:
        raise Hold("unknown edition schema")
    if not is_real_date(edition["date"]) or edition["date"] != iso_date:
        raise Hold("edition date does not match")
    if edition["title"] != audit_title(iso_date, None):
        raise Hold("edition title does not match the date")
    if edition["canonical_url"] != audit_page_url(iso_date, None):
        raise Hold("edition canonical url does not match the date")
    if edition["model"] != NEON_MODEL:
        raise Hold("edition model does not match the daily neon pipeline")
    if type(edition["reasoning_effort"]) is not str or edition["reasoning_effort"].strip() == "":
        raise Hold("edition reasoning effort is missing")
    if spotify:
        validate_root_audit_audio(edition, iso_date)
    elif not is_real_date(iso_date) or iso_date > SELF_HOSTED_AUDIO_LAST_DATE:
        raise Hold("hard stop: audio: the Spotify episode url is missing")
    elif edition["audio_url"] != variant_asset_url(iso_date, None, "episode.mp3"):
        raise Hold("edition audio url does not match")
    expected_video = variant_asset_url(iso_date, None, "short.mp4") if has_short else None
    # A posted public short (for example an X status URL) may be the
    # video_url with or without a local short.mp4. The mp4, when present, stays hashed.
    if edition["video_url"] != expected_video:
        if video_reference_problem(edition["video_url"]) is not None:
            raise Hold("edition video url does not match")
    if edition["sources_url"] != sources_page_url(iso_date, None):
        raise Hold("edition sources url does not match")
    if edition["audit"] != ROOT_AUDIT_RECEIPT:
        raise Hold("audit edition must not be recorded as a gate")
    hashes = edition["hashes"]
    require_keys(hashes, ROOT_AUDIT_HASH_KEYS, "hashes")
    for key in ROOT_AUDIT_HASH_KEYS:
        value = hashes[key]
        if key == "short_sha256" and not has_short:
            if value is not None:
                raise Hold("short_sha256 is set without a short")
            continue
        if key == "episode_sha256" and spotify and not root_audit_keeps_player(edition, iso_date):
            continue
        if type(value) is not str or not SHA256_RE.fullmatch(value):
            raise Hold(f"{key} is malformed")
    return edition


def _load_root_audit_edition(directory, iso_date, *, link_opener=None):
    files = []
    dirs = []
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.islink(path):
            raise Hold(f"unexpected content entry: {name}")
        if os.path.isdir(path):
            dirs.append(name)
        elif os.path.isfile(path):
            files.append(name)
        else:
            raise Hold(f"unexpected content entry: {name}")
    allowed = set(ROOT_AUDIT_REQUIRED_FILES) | set(ROOT_AUDIT_OPTIONAL_FILES)
    required = set(ROOT_AUDIT_REQUIRED_FILES) - {"episode.mp3"}
    if not required <= set(files) or not set(files) <= allowed:
        raise Hold("edition directory does not contain the frozen public inputs")
    if dirs not in ([], ["audit"]):
        raise Hold("edition directory does not contain the frozen public inputs")
    has_short = "short.mp4" in files
    raw = _read_named(directory, [name for name in files])
    script_text = decode_utf8(raw["script.txt"], "script.txt")
    paragraphs = script_paragraphs(script_text)
    sources = parse_json_object(raw["sources.json"], "sources.json")
    edition = parse_json_object(raw["edition.json"], "edition.json")
    run = parse_json_object(raw["neon_run.json"], "neon_run.json")
    validate_root_audit_edition(edition, iso_date, has_short)
    keeps_player = root_audit_keeps_player(edition, iso_date)
    spotify = root_audit_uses_spotify(edition) and not keeps_player
    if spotify and "episode.mp3" in files:
        raise Hold("hard stop: audio: a Spotify edition must not self-host episode.mp3")
    if not spotify and "episode.mp3" not in files:
        raise Hold("edition directory does not contain the frozen public inputs")
    validate_neon_run(run, iso_date, None)
    urls = sources.get("urls")
    source_count = len(urls) if type(urls) is list else 0
    validate_sources(sources, iso_date, source_count, audit=True)
    actual = {
        "script_sha256": sha256_bytes(raw["script.txt"]),
        "sources_sha256": sha256_bytes(raw["sources.json"]),
        "neon_run_sha256": sha256_bytes(raw["neon_run.json"]),
        "episode_sha256": None if spotify else sha256_bytes(raw["episode.mp3"]),
        "short_sha256": sha256_bytes(raw["short.mp4"]) if has_short else None,
    }
    for key, value in actual.items():
        if edition["hashes"][key] != value:
            raise Hold(f"{key} does not match the frozen bytes")
    if edition["reasoning_effort"] != run["reasoning_effort"]:
        raise Hold("edition receipt does not match the neon run")
    if run.get("script_sha256") not in (None, actual["script_sha256"]):
        raise Hold("neon run script hash does not match script.txt")
    if not spotify:
        problem = _local_media_problem("audio", "episode.mp3", directory)
        if problem:
            raise Hold(f"hard stop: audio: {problem}")
    if has_short:
        problem = _local_media_problem("video", "short.mp4", directory)
        if problem:
            raise Hold(f"hard stop: video: {problem}")
    prompt = run["prompts"]["episode"]
    html_text = render_audit_edition_html(edition, paragraphs, sources, prompt, None)
    sources_html = render_sources_page_html(iso_date, sources, None, edition)
    assert_audit_edition_page(html_text, edition, prompt)
    assert_sources_page(sources_html, iso_date, sources, None, edition)
    counts = None
    if dirs == ["audit"]:
        audit_path = os.path.join(directory, "audit", "audit.json")
        assert_real_child(directory, audit_path, "audit.json")
        if os.path.islink(audit_path) or not os.path.isfile(audit_path):
            raise Hold("missing audit.json")
        audit = parse_json_object(read_stable(audit_path), "audit.json")
        results, counts = validate_audit_document(audit, iso_date, actual["script_sha256"])
        for item in results:
            audit_check_path(directory, iso_date, item)
        audit_html = render_audit_html(edition, results, counts, None)
    else:
        audit_html = render_audit_pending_html(edition)
    if link_opener is not None:
        raise_hard_stops(source_link_hard_stops(sources["urls"], link_opener))
    loaded = {
        "date": iso_date,
        "variant": None,
        "paragraphs": paragraphs,
        "sources": sources,
        "qa": None,
        "edition": edition,
        "notes": None,
        "editor_mode": False,
        "audit_mode": True,
        "root_audit": True,
        "html": html_text,
        "notes_html": None,
        "audit_html": audit_html,
        "sources_html": sources_html,
        "audit_counts": counts,
        "prompt": prompt,
    }
    loaded["files"] = _edition_files(loaded)
    return loaded



def latest_parent_edition(editions):
    """Newest parent edition. Neon raw variants are never the latest card."""
    parents = [item for item in editions if not item.get("variant")]
    if not parents:
        raise Hold("no daily state editions")
    return sorted(parents, key=_listing_key)[0]


def edition_has_public_audit(item):
    """True when the parent edition has a published /audit/ page."""
    if item.get("variant"):
        return False
    return bool(item.get("root_audit") or item.get("audit_html"))


def is_greeting_paragraph(text):
    return bool(GREETING_RE.match((text or "").strip()))


def first_sentence(text):
    """First sentence of a paragraph, or the whole paragraph if it has no closer."""
    text = (text or "").strip()
    match = re.search(r"(.*?[.!?])(\s|$)", text)
    if match:
        return match.group(1).strip()
    return text


def edition_lede(item):
    """Short lede: first substantive script sentence, else the first story title."""
    for paragraph in body_paragraphs(item["paragraphs"]):
        if is_greeting_paragraph(paragraph):
            continue
        sentence = first_sentence(paragraph)
        if sentence:
            return sentence
    sources = item.get("sources") or {}
    stories = sources.get("stories") if type(sources) is dict else None
    if type(stories) is list:
        for story in stories:
            if type(story) is dict and story.get("title"):
                return story["title"]
    raise Hold("latest edition has no lede")


def month_heading(iso_date):
    year, month, _day = iso_date.split("-")
    return f"{build.MONTHS[month]} {year}"


def render_home_teaser(editions):
    """Homepage Daily State card. Shared with build.render_home()."""
    item = latest_parent_edition(editions)
    document = item["edition"]
    iso_date = item["date"]
    shown = build.display_date(iso_date, "day")
    href = f"daily-state/{iso_date}/"
    lede = html.escape(edition_lede(item), quote=True)
    headline = edition_headline(document)
    if headline:
        heading = html.escape(headline, quote=True)
        date_line = f'<p><time datetime="{iso_date}">{html.escape(shown)}</time></p>\n'
    else:
        heading = html.escape(shown, quote=True)
        date_line = ""
    links = [f'<a href="{html.escape(href, quote=True)}">Read the edition</a>']
    episode_url = document.get("episode_url")
    if episode_url:
        links.append(
            f'<a href="{html.escape(episode_url, quote=True)}">Audio on Spotify</a>'
        )
    if edition_has_public_audit(item):
        links.append(
            f'<a href="{html.escape(href + "audit/", quote=True)}">Audit</a>'
        )
    return (
        '<section class="latest daily-latest">\n'
        '<p class="kicker">Daily State of AI</p>\n'
        f'<h2><a href="{html.escape(href, quote=True)}">{heading}</a></h2>\n'
        f'{date_line}'
        f'<p class="dek">{lede}</p>\n'
        f'<p class="pair">{" · ".join(links)}</p>\n'
        '<p><a href="daily-state/">All editions →</a></p>\n'
        "</section>"
    )


def render_home_teaser_from_repo(repo):
    return render_home_teaser(load_editions(repo))


def apply_home_teaser(page, teaser):
    """Replace the Daily State card on the homepage, or insert it above Recent."""
    teaser = teaser.strip()
    if TEASER_SECTION_RE.search(page):
        return TEASER_SECTION_RE.sub(teaser, page, count=1)
    marker = '<section class="recent">'
    if marker in page:
        return page.replace(marker, teaser + "\n" + marker, 1)
    raise Hold("homepage is missing the Daily State teaser and a place to put it")


def _write_text_atomic(path, text):
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".ds-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def commit_home_teaser(repo, loaded, write):
    """Refresh index.html's Daily State card. Not part of list_output_files()."""
    path = os.path.join(repo, HOME_REL)
    if not os.path.isfile(path) or os.path.islink(path):
        raise Hold("missing homepage")
    with open(path, encoding="utf-8") as handle:
        current = handle.read()
    expected = apply_home_teaser(current, render_home_teaser(loaded))
    if current == expected:
        return {"wrote": 0, "noop": True}
    if not write:
        raise Hold("homepage teaser does not match the latest edition")
    _write_text_atomic(path, expected)
    return {"wrote": 1, "noop": False}


def render_listing_html(editions):
    ordered = sorted(editions, key=_listing_key)
    rows = []
    current_month = None
    for item in ordered:
        heading = month_heading(item["date"])
        if heading != current_month:
            current_month = heading
            rows.append(f"<h2>{html.escape(heading, quote=True)}</h2>")
        document = item["edition"]
        shown = build.display_date(item["date"], "day")
        variant = item.get("variant")
        href = f"{item['date']}/{variant}/" if variant else f"{item['date']}/"
        label = listing_link_text(document)
        rows.append(
            f"<p class=\"row\"><a href=\"{href}\">{html.escape(label, quote=True)}</a> "
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
        # neon/ and any other known variant is an edition, not a stray directory.
        variant_subfolders(path)
        dates.append(name)
    if not dates:
        raise Hold("no daily state editions")
    return dates


def edition_content_files(editor_mode):
    """Allowed files inside one edition directory. Nothing else publishes."""
    return EDITOR_CONTENT_FILES if editor_mode else CONTENT_FILES


def edition_output_paths(iso_date, editor_mode, variant=None, root_audit=False):
    """Allowed generated files for one edition, besides the shared listing."""
    if root_audit:
        base = f"daily-state/{iso_date}"
        return [f"{base}/index.html", f"{base}/audit/index.html", f"{base}/sources/index.html"]
    if variant:
        base = f"daily-state/{iso_date}/{variant}"
        return [f"{base}/index.html", f"{base}/audit/index.html", f"{base}/sources/index.html"]
    paths = [f"daily-state/{iso_date}/index.html", f"daily-state/{iso_date}/sources/index.html"]
    if editor_mode:
        paths.append(f"daily-state/{iso_date}/editors-notes/index.html")
    return paths


def _read_named(directory, names):
    raw = {}
    for name in names:
        path = os.path.join(directory, name)
        assert_real_child(directory, path, name)
        if not os.path.isfile(path):
            raise Hold(f"missing {name}")
        raw[name] = read_stable(path)
    return raw


def load_edition_directory(directory, iso_date, *, link_opener=None, editor_mode=None, variant=None):
    """Validate one frozen edition directory and render its pages.

    editor_mode=True requires editor_notes.json. editor_mode=False keeps the
    live allowlist. The default follows the edition: notes plus pipeline
    "editor", or the four frozen inputs. A known variant subfolder such as
    neon/ is an audit edition and is not one of the parent files.
    """
    base = os.path.basename(os.path.normpath(directory))
    if variant is None and base in VARIANT_NAMES:
        variant = base
    if variant is not None:
        if variant not in VARIANT_NAMES or base != variant:
            raise Hold("unknown variant")
        if editor_mode is True:
            raise Hold("audit edition is not an editor edition")
        if editor_mode is False:
            raise Hold("audit edition is not a live edition")
        return _load_audit_edition(
            directory, iso_date, variant, link_opener=link_opener,
        )
    if not is_real_date(iso_date):
        raise Hold("edition date is invalid")
    if os.path.islink(directory) or not os.path.isdir(directory):
        raise Hold("missing edition directory")
    if directory_declares_root_audit(directory):
        if editor_mode is True:
            raise Hold("audit edition is not an editor edition")
        if editor_mode is False:
            raise Hold("audit edition is not a live edition")
        return _load_root_audit_edition(directory, iso_date, link_opener=link_opener)
    variants = variant_subfolders(directory)
    names = sorted(name for name in os.listdir(directory) if name not in variants)
    notes_present = "editor_notes.json" in names
    if editor_mode is True and not notes_present:
        raise Hold("editor notes are missing")
    if editor_mode is False:
        selected = False
    else:
        selected = notes_present if editor_mode is None else True
    expected = edition_content_files(selected)
    if names != sorted(expected):
        raise Hold("edition directory does not contain the frozen public inputs")
    raw = _read_named(directory, expected)
    script_text = decode_utf8(raw["script.txt"], "script.txt")
    paragraphs = script_paragraphs(script_text)
    sources = parse_json_object(raw["sources.json"], "sources.json")
    qa = parse_json_object(raw["qa.json"], "qa.json")
    edition = parse_json_object(raw["edition.json"], "edition.json")
    validate_qa(qa, iso_date)
    validate_sources(sources, iso_date, qa["source_count"])
    validate_edition(edition, iso_date)
    declared = edition_declares_editor(edition)
    if selected != declared:
        if selected:
            raise Hold("editor mode is not marked on the edition")
        raise Hold("editor notes are missing")
    if qa["run_sha256"] != edition["hashes"]["run_sha256"]:
        raise Hold("run_sha256 does not match the qa snapshot")
    notes = None
    notes_html = None
    if selected:
        notes = parse_json_object(raw["editor_notes.json"], "editor_notes.json")
        validate_editor_notes(notes, iso_date)
        receipt = normalize_editor(edition["editor"])
        if receipt["outstanding"] != len(notes["outstanding"]):
            raise Hold("editor outstanding count does not match editor notes")
        check_hashes(
            edition, raw["script.txt"], raw["sources.json"], raw["qa.json"],
            notes_bytes=raw["editor_notes.json"],
        )
    else:
        check_hashes(edition, raw["script.txt"], raw["sources.json"], raw["qa.json"])
    for field in ("date",):
        if sources[field] != iso_date or qa[field] != iso_date or edition[field] != iso_date:
            raise Hold("edition dates do not agree")
    html_text = render_edition_html(edition, paragraphs, sources, editor_mode=selected)
    sources_html = render_sources_page_html(iso_date, sources, None, edition)
    assert_sources_page(sources_html, iso_date, sources, None, edition)
    if selected:
        assert_edition_page(html_text, edition)
        notes_html = render_editors_notes_html(iso_date, notes)
        if link_opener is not None:
            raise_hard_stops(source_link_hard_stops(sources["urls"], link_opener))
    return {
        "date": iso_date,
        "paragraphs": paragraphs,
        "sources": sources,
        "qa": qa,
        "edition": edition,
        "notes": notes,
        "editor_mode": selected,
        "html": html_text,
        "notes_html": notes_html,
        "sources_html": sources_html,
    }


def load_edition(repo, iso_date, *, link_opener=None, editor_mode=None):
    if not is_real_date(iso_date) or os.sep in iso_date or "/" in iso_date:
        raise Hold("edition date is invalid")
    root = content_root(repo)
    directory = os.path.join(root, iso_date)
    assert_real_child(root, directory, iso_date)
    if not os.path.isdir(directory):
        raise Hold("missing edition directory")
    return load_edition_directory(
        directory, iso_date, link_opener=link_opener, editor_mode=editor_mode,
    )


def render_output(loaded):
    files = {LISTING_REL: render_listing_html(loaded)}
    for edition in loaded:
        variant = edition.get("variant")
        if variant:
            base = f"daily-state/{edition['date']}/{variant}"
            files[f"{base}/index.html"] = edition["html"]
            files[f"{base}/audit/index.html"] = edition["audit_html"]
            files[f"{base}/sources/index.html"] = edition["sources_html"]
            continue
        files[f"daily-state/{edition['date']}/index.html"] = edition["html"]
        if edition.get("root_audit"):
            files[f"daily-state/{edition['date']}/audit/index.html"] = edition["audit_html"]
        files[f"daily-state/{edition['date']}/sources/index.html"] = edition["sources_html"]
        if edition.get("notes_html"):
            files[f"daily-state/{edition['date']}/editors-notes/index.html"] = edition["notes_html"]
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
            # The pending audit placeholder is the one edition page that may be replaced.
            pending_audit = rel.endswith("/audit/index.html") and AUDIT_PENDING_MARKER in current
            if write and rel != LISTING_REL and not allow_correction and not pending_audit:
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


def load_editions(repo, *, link_opener=None):
    """Parent editions, then each known variant, newest date last in this list."""
    loaded = []
    root = content_root(repo)
    for iso_date in list_edition_dates(repo):
        loaded.append(load_edition(repo, iso_date, link_opener=link_opener))
        directory = os.path.join(root, iso_date)
        for variant in variant_subfolders(directory):
            loaded.append(load_edition_directory(
                os.path.join(directory, variant),
                iso_date,
                link_opener=link_opener,
                variant=variant,
            ))
    return loaded


def publish(repo, *, write=True, allow_correction=False):
    """Validate every edition before replacing any generated file.

    The Daily State listing and the homepage teaser may refresh when a new
    date is added. index.html is checked and written separately; it is not
    part of list_output_files().
    """
    loaded = load_editions(repo)
    files = render_output(loaded)
    # Fail closed: a missing homepage holds before any edition HTML is written.
    home_path = os.path.join(repo, HOME_REL)
    if not os.path.isfile(home_path) or os.path.islink(home_path):
        raise Hold("missing homepage")
    with open(home_path, encoding="utf-8") as handle:
        apply_home_teaser(handle.read(), render_home_teaser(loaded))
    result = commit_output(repo, files, write=write, allow_correction=allow_correction)
    home = commit_home_teaser(repo, loaded, write=write)
    wrote = result["wrote"] + home["wrote"]
    return {"wrote": wrote, "noop": wrote == 0}


def _optional_package_hashes(run, script_bytes, sources_bytes, notes_bytes):
    hashes = run.get("hashes")
    if hashes is None:
        return
    if type(hashes) is not dict:
        raise Hold("unknown run schema")
    actual = {
        "script_sha256": sha256_bytes(script_bytes),
        "sources_sha256": sha256_bytes(sources_bytes),
        "editor_notes_sha256": sha256_bytes(notes_bytes),
    }
    for key, value in hashes.items():
        if key not in actual or type(value) is not str or value != actual[key]:
            raise Hold(f"{key} does not match the frozen bytes")


def load_pipeline_package(directory, *, editor_mode=None, link_opener=None):
    """Validate a pipeline package and render the edition offline.

    Required files, next to any other pipeline output: script.txt,
    sources.json, run.json, editor_notes.json. Extra files are not rendered.
    """
    required = ("script.txt", "sources.json", "run.json", "editor_notes.json")
    for name in required:
        path = os.path.join(directory, name)
        if os.path.islink(path) or not os.path.isfile(path):
            raise Hold(f"missing {name}")
    raw = {name: read_stable(os.path.join(directory, name)) for name in required}
    run = parse_json_object(raw["run.json"], "run.json")
    selected = editor_mode_of(run, editor_mode)
    if not selected:
        if type(run) is dict and is_real_date(run.get("date")) and type(run.get("source_count")) is int:
            validate_run(run, run["date"], run["source_count"], editor_mode=False)
        raise Hold("package has no frozen edition")
    if not is_real_date(run.get("date")):
        raise Hold("run date does not match the edition")
    iso_date = run["date"]
    sources = parse_json_object(raw["sources.json"], "sources.json")
    urls = sources.get("urls")
    source_count = len(urls) if type(urls) is list else 0
    validate_run(run, iso_date, source_count, editor_mode=True)
    validate_sources(sources, iso_date, source_count)
    notes = parse_json_object(raw["editor_notes.json"], "editor_notes.json")
    validate_editor_notes(notes, iso_date)
    receipt = normalize_editor(run["editor"])
    if receipt["outstanding"] != len(notes["outstanding"]):
        raise Hold("editor outstanding count does not match editor notes")
    _optional_package_hashes(run, raw["script.txt"], raw["sources.json"], raw["editor_notes.json"])
    episode_url = run.get("episode_url")
    problem = audio_reference_problem(episode_url)
    if problem:
        raise Hold(f"hard stop: audio: {problem}")
    if "audio" in run:
        problem = audio_reference_problem(run["audio"], directory)
        if problem:
            raise Hold(f"hard stop: audio: {problem}")
    edition = {
        "date": iso_date,
        "title": edition_title(iso_date),
        "canonical_url": edition_url(iso_date),
        "episode_url": episode_url,
        "episode_id": episode_id_from_url(episode_url),
    }
    if "video" in run or "video_url" in run:
        video_ref = run["video_url"] if "video_url" in run else run.get("video")
        problem = video_reference_problem(video_ref, directory)
        if problem:
            raise Hold(f"hard stop: video: {problem}")
        if type(video_ref) is str and video_ref.startswith("https://"):
            edition["video_url"] = video_ref
    paragraphs = script_paragraphs(decode_utf8(raw["script.txt"], "script.txt"))
    html_text = render_edition_html(edition, paragraphs, sources, editor_mode=True)
    notes_html = render_editors_notes_html(iso_date, notes)
    sources_html = render_sources_page_html(iso_date, sources, None, edition)
    assert_edition_page(html_text, edition)
    assert_sources_page(sources_html, iso_date, sources, None, edition)
    if link_opener is not None:
        raise_hard_stops(source_link_hard_stops(sources["urls"], link_opener))
    loaded = {
        "date": iso_date,
        "paragraphs": paragraphs,
        "sources": sources,
        "qa": None,
        "edition": edition,
        "notes": notes,
        "editor_mode": True,
        "html": html_text,
        "notes_html": notes_html,
        "sources_html": sources_html,
    }
    loaded["files"] = _edition_files(loaded)
    return loaded


def _edition_files(loaded):
    files = {}
    variant = loaded.get("variant")
    for rel in edition_output_paths(
        loaded["date"], loaded["editor_mode"], variant, root_audit=bool(loaded.get("root_audit")),
    ):
        if rel.endswith("/audit/index.html"):
            files[rel] = loaded["audit_html"]
        elif rel.endswith("/editors-notes/index.html"):
            files[rel] = loaded["notes_html"]
        elif rel.endswith("/sources/index.html"):
            files[rel] = loaded["sources_html"]
        else:
            files[rel] = loaded["html"]
    return files


def validate_package(path, *, editor_mode=None, link_opener=None):
    """Validate one package directory. Offline unless link_opener is set.

    A frozen edition directory (the public inputs, and editor_notes.json in
    editor mode) uses the same checks as publish. A pipeline directory
    (script.txt, sources.json, run.json, editor_notes.json, plus any other
    files the pipeline wrote) is rendered from the editor receipt.
    """
    if os.path.islink(path) or not os.path.isdir(path):
        raise Hold("missing package directory")
    names = set(os.listdir(path))
    if "edition.json" in names or "qa.json" in names:
        edition_path = os.path.join(path, "edition.json")
        if os.path.islink(edition_path) or not os.path.isfile(edition_path):
            raise Hold("missing edition.json")
        edition = parse_json_object(read_stable(edition_path), "edition.json")
        iso_date = edition.get("date")
        if not is_real_date(iso_date):
            raise Hold("edition date is invalid")
        loaded = load_edition_directory(
            path, iso_date, link_opener=link_opener, editor_mode=editor_mode,
        )
        loaded["files"] = _edition_files(loaded)
        return loaded
    return load_pipeline_package(path, editor_mode=editor_mode, link_opener=link_opener)


def write_rendered(out_dir, files):
    if os.path.lexists(out_dir) and (os.path.islink(out_dir) or not os.path.isdir(out_dir)):
        raise Hold("output path is not a directory")
    temps = []
    try:
        for rel, text in files.items():
            if rel.startswith("/") or ".." in rel.split("/"):
                raise Hold("refusing to write outside the output directory")
            path = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".ds-", suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
            temps.append((tmp, path))
        for tmp, path in temps:
            os.replace(tmp, path)
    except Exception:
        for tmp, _path in temps:
            if os.path.exists(tmp):
                os.remove(tmp)
        raise


def parse_cli(argv):
    options = {
        "check": False,
        "allow_correction": False,
        "check_links": False,
        "package": None,
        "out": None,
        "pipeline": None,
    }
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--check", "--daily-state-check"):
            options["check"] = True
        elif arg == "--allow-correction":
            options["allow_correction"] = True
        elif arg == "--check-links":
            options["check_links"] = True
        elif arg in ("--package", "--out", "--pipeline"):
            index += 1
            if index >= len(argv):
                raise Hold(f"missing value for {arg}")
            options[arg[2:]] = argv[index]
        else:
            raise Hold(f"unknown argument: {arg}")
        index += 1
    if options["pipeline"] not in (None, "editor", "live"):
        raise Hold("unknown pipeline")
    if options["check_links"] and not options["package"]:
        raise Hold("--check-links applies to a package directory")
    return options


def main(argv=None, repo=None):
    if argv is None:
        argv = sys.argv[1:]
    repo = repo or os.path.dirname(os.path.abspath(__file__))
    try:
        options = parse_cli(argv)
        if options["package"]:
            editor_mode = {"editor": True, "live": False}.get(options["pipeline"])
            opener = live_link_opener if options["check_links"] else None
            loaded = validate_package(
                options["package"], editor_mode=editor_mode, link_opener=opener,
            )
            kind = "audit" if loaded.get("audit_mode") else "editor"
            if options["out"] and not options["check"]:
                write_rendered(options["out"], loaded["files"])
                print(f"{kind} package: wrote {len(loaded['files'])} file(s)")
            else:
                print(f"{kind} package check: ok")
            return 0
        check_only = options["check"]
        allow_correction = options["allow_correction"] and not check_only
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
