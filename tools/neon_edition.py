#!/usr/bin/env python3
"""Stage a daily Gemini 4 Neon audit edition, then attach its executable audit.

    python3 tools/neon_edition.py build --date D --episode-dir DIR [--short MP4 --short-report JSON]
        [--episode-url URL] [--verification JSON]
    python3 tools/neon_edition.py attach-audit --date D --audit-out DIR --kit DIR
    python3 tools/neon_edition.py set-short-url --date D --url URL
    python3 tools/neon_edition.py set-audit-short-url --date D --url URL
    python3 tools/neon_edition.py set-headline --date D --headline TEXT [--variant neon]

build copies the frozen Neon run (script.txt, sources.json and run.json from
the Mac Mini mirror) into content/daily-state/D/ with edition.json mode
"audit" and "variant": null. Nothing is edited: the script bytes are the
model's reply. The page links the Spotify episode ("Audio on Spotify"), as
the pre-audit editions did; episode.mp3 is not copied (from 2026-11-22).
The episode URL comes from --episode-url, else spotify_episode_url in the
mirror's takeaways.json, else spotify_episode_url / episode_url in run.json.
It must be an open.spotify.com/episode/<22-char id> URL whose public page and
the show's public page both name "Daily State of AI - D"; that evidence is
recorded in edition.json (or read from --verification, a recorded evidence
file). A missing, malformed or unverified episode refuses the build.
It also refuses an existing directory, a run that is not status ok on the
neon pipeline, or a script whose hash does not match the run. The audit page
is a pending placeholder until attach-audit.

attach-audit copies the audit (audit.json, audit.md, the per-claim checks,
the helper library, the runner, and the source snapshots) into
content/daily-state/D/audit/. audit.json must be for D and for this script.
The audit is for transparency and never blocks or edits the edition.

set-short-url writes a public X short URL into edition.json video_url and
regenerates that date's edition page. The URL must be
https://x.com/signalnoisepub/status/<digits>; any query string, fragment, or
trailing /video/1 is stripped. Rerunning with the same URL is a no-op. A
local short.mp4 is not required. This is the post-publish step: the 7:20
edition may ship before Max posts the Neon short around 10 AM.

set-audit-short-url writes a public X URL into edition.json audit_short_url
and regenerates that date's audit page only (the edition page is untouched).
The URL must be https://x.com/signalnoisepub/status/<digits>; any query
string, fragment, or trailing /video/1 is stripped. When the field is set,
the audit page shows a prominent "Watch the audit short" link near the top.
When it is absent, the audit page renders no such link. Rerunning with the
same URL is a no-op. This is the post-publish step after the audit short is
posted as a reply in that day's Daily State short thread.

set-headline writes an optional 4-10 word (max 14) teaser into edition.json
and regenerates the edition page, the Daily State listing, and the homepage
card when needed. Rerunning with the same headline is a no-op. The h1 stays
Daily State of AI - <date>. Use tools/draft_headline.py to generate the text
from the episode script.

All commands validate with daily_state.py's loader before returning 0.
"""
import argparse
import hashlib
import html as html_lib
import json
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

import daily_state  # noqa: E402

RUN_KEYS = (
    "date", "status", "pipeline", "model", "reasoning_effort", "system_prompt",
    "editor", "qa", "edits_after_generation", "fallback", "prompts",
    "model_attempts", "words", "duration_seconds", "bundle_sha256", "script_sha256",
)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


SHOW_URL = "https://open.spotify.com/show/1AC7qV1tyVIICLtJVwBapp"
USER_AGENT = "Mozilla/5.0 (signal-noise-web daily-state verifier)"


def _get(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def _meta(page, attr, name):
    match = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, re.escape(name)), page)
    return html_lib.unescape(match.group(1)) if match else None


def spotify_fetch(url):
    """Public-page documents for daily_state.verify_public_episode."""
    if "/episode/" in url:
        page = _get(url)
        canonical = re.search(r'<link rel="canonical" href="([^"]*)"', page)
        return {
            "title": _meta(page, "property", "og:title"),
            "canonical_url": html_lib.unescape(canonical.group(1)) if canonical else _meta(page, "property", "og:url"),
            "id": url.rsplit("/", 1)[-1],
        }
    show_id = url.rstrip("/").rsplit("/", 1)[-1]
    page = _get(f"https://open.spotify.com/embed/show/{show_id}")
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', page, re.S)
    if not match:
        raise daily_state.Hold("verification parse failed")
    entity = json.loads(match.group(1))["props"]["pageProps"]["state"]["data"]["entity"]
    episodes = []
    items = [entity] if entity.get("type") == "episode" else []
    items += [item for item in entity.get("trackList") or [] if isinstance(item, dict)]
    for item in items:
        uri = item.get("uri") or ""
        if uri.startswith("spotify:episode:"):
            episode = {"id": uri.split(":")[-1], "title": item.get("title") or item.get("name"), "uri": uri}
            if episode not in episodes:
                episodes.append(episode)
    return {"episodes": episodes}


def utc_now():
    return datetime.now(timezone.utc)


def resolve_episode_url(args, src, run):
    if args.episode_url:
        return args.episode_url
    try:
        with open(os.path.join(src, "takeaways.json"), encoding="utf-8") as handle:
            takeaways = json.load(handle)
    except (OSError, ValueError):
        takeaways = {}
    for value in (takeaways.get("spotify_episode_url"), run.get("spotify_episode_url"), run.get("episode_url")):
        if value:
            return value
    return None


def record_verification(args, date, episode_url):
    """Recorded public verification, the same evidence as the pre-audit editions."""
    if args.verification:
        with open(args.verification, encoding="utf-8") as handle:
            verification = json.load(handle)
        return verification["checked_at"], verification
    show_url = args.show_url or SHOW_URL
    chosen = daily_state.verify_public_episode(spotify_fetch, date, episode_url, show_url)
    checked_at = utc_now().strftime("%Y-%m-%dT%H:%MZ")
    title = daily_state.edition_title(date)
    verification = {
        "method": "public_episode_and_show",
        "checked_at": checked_at,
        "episode": {"title": title, "canonical_url": episode_url, "id": daily_state.episode_id_from_url(episode_url)},
        "show": {"id": show_url.rstrip("/").rsplit("/", 1)[-1], "episodes": [chosen]},
    }
    return checked_at, verification


def fail(message):
    print(f"HOLD: {message}", file=sys.stderr)
    return 1


def build(args):
    date = args.date
    if not daily_state.is_real_date(date):
        return fail("date is invalid")
    src = args.episode_dir
    run_path = os.path.join(src, "run.json")
    try:
        with open(run_path, encoding="utf-8") as handle:
            run = json.load(handle)
    except (OSError, ValueError):
        return fail("run.json is missing or unreadable")
    if run.get("date") != date or run.get("status") != "ok":
        return fail("neon run is not an ok run for this date")
    if run.get("pipeline") != daily_state.ROOT_NEON_PIPELINE or run.get("model") != daily_state.NEON_MODEL:
        return fail("run is not the daily neon pipeline")
    for name in ("script.txt", "sources.json"):
        if not os.path.isfile(os.path.join(src, name)):
            return fail(f"missing {name}")
    episode_url = resolve_episode_url(args, src, run)
    if not episode_url:
        return fail("hard stop: audio: the Spotify episode url is missing")
    try:
        episode_id = daily_state.episode_id_from_url(episode_url)
        verified_at, verification = record_verification(args, date, episode_url)
    except daily_state.Hold as exc:
        return fail(f"hard stop: audio: {exc}")
    except Exception as exc:  # noqa: BLE001  network or parse failure holds
        return fail(f"hard stop: audio: Spotify verification failed ({type(exc).__name__})")
    script_sha = sha256_file(os.path.join(src, "script.txt"))
    if run.get("script_sha256") != script_sha:
        return fail("script.txt does not match the neon run")
    dest = os.path.join(daily_state.content_root(REPO), date)
    if os.path.lexists(dest):
        return fail(f"{dest} already exists; editions are immutable")
    has_short = bool(args.short)
    if has_short and not os.path.isfile(args.short):
        return fail("short mp4 is missing")
    neon_run = {key: run.get(key) for key in RUN_KEYS}
    material = run.get("material") or {}
    neon_run["material"] = {key: material.get(key) for key in ("source", "sha256", "chars")}
    neon_run["audit"] = {"gate": False, "status": "runs after publish"}
    if has_short:
        short = {"file": "short.mp4", "sha256": sha256_file(args.short)}
        if args.short_report:
            with open(args.short_report, encoding="utf-8") as handle:
                report = json.load(handle)
            short.update({
                "model": report.get("model"),
                "words": report.get("words"),
                "duration_seconds": report.get("duration_seconds"),
                "prompt_sha256": report.get("prompt_sha256"),
                "edits_after_generation": report.get("edits_after_generation"),
            })
            if report.get("prompt"):
                neon_run["prompts"] = {**(neon_run.get("prompts") or {}), "short": report["prompt"]}
        neon_run["short"] = short
    os.makedirs(dest)
    try:
        for name in ("script.txt", "sources.json"):
            shutil.copyfile(os.path.join(src, name), os.path.join(dest, name))
        if has_short:
            shutil.copyfile(args.short, os.path.join(dest, "short.mp4"))
        run_bytes = (json.dumps(neon_run, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        with open(os.path.join(dest, "neon_run.json"), "wb") as handle:
            handle.write(run_bytes)
        edition = {
            "schema_version": daily_state.SCHEMA_VERSION,
            "date": date,
            "mode": "audit",
            "variant": None,
            "title": daily_state.audit_title(date, None),
            "canonical_url": daily_state.audit_page_url(date, None),
            "model": run["model"],
            "reasoning_effort": run["reasoning_effort"],
            "audio_url": None,
            "episode_id": episode_id,
            "episode_url": episode_url,
            "verified_at": verified_at,
            "verification": verification,
            "video_url": daily_state.variant_asset_url(date, None, "short.mp4") if has_short else None,
            "sources_url": daily_state.sources_page_url(date, None),
            "audit": dict(daily_state.ROOT_AUDIT_RECEIPT),
            "hashes": {
                "script_sha256": script_sha,
                "sources_sha256": sha256_file(os.path.join(dest, "sources.json")),
                "neon_run_sha256": hashlib.sha256(run_bytes).hexdigest(),
                "episode_sha256": None,
                "short_sha256": sha256_file(os.path.join(dest, "short.mp4")) if has_short else None,
            },
        }
        with open(os.path.join(dest, "edition.json"), "w", encoding="utf-8") as handle:
            handle.write(json.dumps(edition, indent=2, ensure_ascii=False) + "\n")
        daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        shutil.rmtree(dest, ignore_errors=True)
        return fail(str(exc))
    except Exception:
        shutil.rmtree(dest, ignore_errors=True)
        raise
    print(json.dumps({"staged": dest, "short": has_short, "words": run.get("words")}))
    return 0


def _copy_tree(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def attach_audit(args):
    date = args.date
    dest_root = os.path.join(daily_state.content_root(REPO), date)
    if not daily_state.directory_declares_root_audit(dest_root):
        return fail("no daily audit edition for this date")
    dest = os.path.join(dest_root, "audit")
    if os.path.lexists(dest):
        return fail("the audit is already attached")
    audit_json = os.path.join(args.audit_out, "audit.json")
    try:
        with open(audit_json, encoding="utf-8") as handle:
            audit = json.load(handle)
    except (OSError, ValueError):
        return fail("audit.json is missing or unreadable")
    if (audit.get("meta") or {}).get("date") != date:
        return fail("audit.json is for another date")
    kit = args.kit
    checks = os.path.join(kit, "checks", date)
    if not os.path.isdir(checks):
        return fail("checks for this date are missing")
    os.makedirs(dest)
    try:
        shutil.copyfile(audit_json, os.path.join(dest, "audit.json"))
        md = os.path.join(args.audit_out, "audit.md")
        if os.path.isfile(md):
            shutil.copyfile(md, os.path.join(dest, "audit.md"))
        _copy_tree(checks, os.path.join(dest, "checks", date))
        _copy_tree(os.path.join(kit, "lib"), os.path.join(dest, "lib"))
        shutil.copyfile(os.path.join(kit, "run_audit.py"), os.path.join(dest, "run_audit.py"))
        sources = os.path.join(kit, "sources", date)
        if os.path.isdir(sources):
            _copy_tree(sources, os.path.join(dest, "sources", date))
        loaded = daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        shutil.rmtree(dest, ignore_errors=True)
        return fail(str(exc))
    except Exception:
        shutil.rmtree(dest, ignore_errors=True)
        raise
    print(json.dumps({"attached": dest, "counts": loaded.get("audit_counts")}))
    return 0



SHORT_X_HOSTS = {"x.com", "www.x.com"}
SHORT_X_USER = "signalnoisepub"
SHORT_URL_ERROR = "short url must be https://x.com/signalnoisepub/status/<id>"


def normalize_short_x_url(url):
    """Return the clean https://x.com/signalnoisepub/status/<digits> form."""
    if type(url) is not str or url != url.strip() or any(ch in url for ch in " \t\r\n\\"):
        raise daily_state.Hold(SHORT_URL_ERROR)
    parts = urllib.parse.urlsplit(url.strip())
    host = (parts.hostname or "").lower().rstrip(".")
    if parts.scheme != "https" or host not in SHORT_X_HOSTS:
        raise daily_state.Hold(SHORT_URL_ERROR)
    segs = [seg for seg in parts.path.split("/") if seg]
    if (
        len(segs) < 3
        or segs[0].lower() != SHORT_X_USER
        or segs[1].lower() != "status"
        or not segs[2].isdigit()
    ):
        raise daily_state.Hold(SHORT_URL_ERROR)
    extra = [seg.lower() for seg in segs[3:]]
    if extra not in ([], ["video", "1"]):
        raise daily_state.Hold(SHORT_URL_ERROR)
    return f"https://x.com/{SHORT_X_USER}/status/{segs[2]}"


def set_short_url(args):
    date = args.date
    if not daily_state.is_real_date(date):
        return fail("date is invalid")
    try:
        url = normalize_short_x_url(args.url)
    except daily_state.Hold as exc:
        return fail(str(exc))
    dest = os.path.join(daily_state.content_root(REPO), date)
    if not daily_state.directory_declares_root_audit(dest):
        return fail("no daily audit edition for this date")
    edition_path = os.path.join(dest, "edition.json")
    try:
        raw = daily_state.read_stable(edition_path)
        edition = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError, daily_state.Hold):
        return fail("edition.json is missing or unreadable")
    page_rel = f"daily-state/{date}/index.html"
    page_path = os.path.join(REPO, page_rel)
    previous = raw
    already = edition.get("video_url") == url
    if not already:
        edition["video_url"] = url
        daily_state._write_text_atomic(
            edition_path, json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
        )
    try:
        loaded = daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
        return fail(str(exc))
    html_text = loaded["html"]
    marker = f'<a href="{url}">Short</a>'
    if marker not in html_text:
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
        return fail("edition page is missing the Short link")
    current = None
    if os.path.isfile(page_path) and not os.path.islink(page_path):
        with open(page_path, encoding="utf-8") as handle:
            current = handle.read()
    if already and current == html_text:
        print(json.dumps({"noop": True, "date": date, "video_url": url}))
        return 0
    os.makedirs(os.path.dirname(page_path), exist_ok=True)
    daily_state._write_text_atomic(page_path, html_text)
    print(json.dumps({"date": date, "video_url": url, "wrote": [page_rel]}))
    return 0



def set_audit_short_url(args):
    date = args.date
    if not daily_state.is_real_date(date):
        return fail("date is invalid")
    try:
        url = normalize_short_x_url(args.url)
    except daily_state.Hold as exc:
        return fail(str(exc).replace("short url must be", "audit short url must be"))
    dest = os.path.join(daily_state.content_root(REPO), date)
    if not daily_state.directory_declares_root_audit(dest):
        return fail("no daily audit edition for this date")
    edition_path = os.path.join(dest, "edition.json")
    try:
        raw = daily_state.read_stable(edition_path)
        edition = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError, daily_state.Hold):
        return fail("edition.json is missing or unreadable")
    page_rel = f"daily-state/{date}/audit/index.html"
    page_path = os.path.join(REPO, page_rel)
    previous = raw
    already = edition.get("audit_short_url") == url
    if not already:
        edition["audit_short_url"] = url
        daily_state._write_text_atomic(
            edition_path, json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
        )
    try:
        loaded = daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
        return fail(str(exc))
    html_text = loaded["audit_html"]
    marker = f'<a href="{url}">Watch the audit short</a>'
    if marker not in html_text:
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
        return fail("audit page is missing the audit short link")
    current = None
    if os.path.isfile(page_path) and not os.path.islink(page_path):
        with open(page_path, encoding="utf-8") as handle:
            current = handle.read()
    if already and current == html_text:
        print(json.dumps({"noop": True, "date": date, "audit_short_url": url}))
        return 0
    os.makedirs(os.path.dirname(page_path), exist_ok=True)
    daily_state._write_text_atomic(page_path, html_text)
    print(json.dumps({"date": date, "audit_short_url": url, "wrote": [page_rel]}))
    return 0


def set_headline(args):
    date = args.date
    if not daily_state.is_real_date(date):
        return fail("date is invalid")
    variant = args.variant or None
    if variant is not None and variant not in daily_state.VARIANT_NAMES:
        return fail("unknown variant")
    try:
        headline = daily_state.validate_headline(args.headline)
    except daily_state.Hold as exc:
        return fail(str(exc))
    dest = os.path.join(daily_state.content_root(REPO), date)
    if variant:
        dest = os.path.join(dest, variant)
    edition_path = os.path.join(dest, "edition.json")
    if os.path.islink(edition_path) or not os.path.isfile(edition_path):
        return fail("no edition for this date")
    try:
        raw = daily_state.read_stable(edition_path)
        edition = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError, daily_state.Hold):
        return fail("edition.json is missing or unreadable")
    already = edition.get("headline") == headline
    previous = raw
    if not already:
        edition["headline"] = headline
        daily_state._write_text_atomic(
            edition_path, json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
        )
    if already:
        try:
            daily_state.publish(REPO, write=False)
            print(json.dumps({"noop": True, "date": date, "variant": variant, "headline": headline}))
            return 0
        except daily_state.Hold:
            pass
    try:
        result = daily_state.publish(REPO, write=True, allow_correction=True)
    except daily_state.Hold as exc:
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
        return fail(str(exc))
    print(json.dumps({
        "date": date,
        "variant": variant,
        "headline": headline,
        "wrote": result["wrote"],
        "noop": result["noop"],
    }))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--date", required=True)
    b.add_argument("--episode-dir", required=True)
    b.add_argument("--short", default=None)
    b.add_argument("--short-report", default=None)
    b.add_argument("--episode-url", default=None)
    b.add_argument("--show-url", default=None)
    b.add_argument("--verification", default=None)
    a = sub.add_parser("attach-audit")
    a.add_argument("--date", required=True)
    a.add_argument("--audit-out", required=True)
    a.add_argument("--kit", required=True)
    s = sub.add_parser("set-short-url")
    s.add_argument("--date", required=True)
    s.add_argument("--url", required=True)
    a_short = sub.add_parser("set-audit-short-url")
    a_short.add_argument("--date", required=True)
    a_short.add_argument("--url", required=True)
    h = sub.add_parser("set-headline")
    h.add_argument("--date", required=True)
    h.add_argument("--headline", required=True)
    h.add_argument("--variant", default=None)
    args = parser.parse_args(argv)
    if args.cmd == "build":
        return build(args)
    if args.cmd == "attach-audit":
        return attach_audit(args)
    if args.cmd == "set-short-url":
        return set_short_url(args)
    if args.cmd == "set-audit-short-url":
        return set_audit_short_url(args)
    return set_headline(args)


if __name__ == "__main__":
    sys.exit(main())
