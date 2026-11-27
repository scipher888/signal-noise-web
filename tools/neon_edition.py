#!/usr/bin/env python3
"""Stage a daily Gemini 4 Neon audit edition, then attach its executable audit.

    python3 tools/neon_edition.py build --date D --episode-dir DIR [--short MP4 --short-report JSON]
        [--episode-url URL] [--verification JSON]
    python3 tools/neon_edition.py attach-audit --date D --audit-out DIR [--kit DIR]
    python3 tools/neon_edition.py set-short-url --date D --url URL [--mp4 PATH]
    python3 tools/neon_edition.py set-audit-short-url --date D [--url URL] [--mp4 PATH]
    python3 tools/neon_edition.py set-headline --date D --headline TEXT [--variant neon]

build copies the frozen Neon run (script.txt, sources.json and run.json from
the Mac Mini mirror) into content/daily-state/D/ with edition.json mode
"audit" and "variant": null. Nothing is edited: the script bytes are the
model's reply. The page links the Spotify episode ("Audio on Spotify"), as
the pre-audit editions did; episode.mp3 is not copied (from 2026-11-22).
The episode URL comes from --episode-url, else spotify_episode_url in the
mirror's takeaways.json, else spotify_episode_url / episode_url in run.json.
It must be an open.spotify.com/episode/<22-char id> URL whose public page and
the show's public page both name "Daily State of AI - D" or
"<headline> | Daily State of AI - D"; that evidence is
recorded in edition.json (or read from --verification, a recorded evidence
file). A missing, malformed or unverified episode refuses the build.
It also refuses an existing directory, a run that is not status ok on the
neon pipeline, or a script whose hash does not match the run. The audit page
is a pending placeholder until attach-audit.

attach-audit copies the audit (audit.json, audit.md, the per-claim checks,
the helper library, the runner, and the source snapshots) into
content/daily-state/D/audit/. audit.json must be for D and for this script.
The audit is for transparency and never blocks or edits the edition.
From 2026-11-27 the audit normally runs upstream on the Mini before TTS
(synthia-workspace ethical_floor.py) and is mirrored as DAY/audit/ with its kit
at DAY/audit/kit/, so `attach-audit --audit-out MIRROR/audit` reuses it with no
second Astra run. Its audit.json may carry an "ethical_floor" record (one
surgical fix pass at most, with before/after text and the pre-fix script hash),
which the audit page renders. When the Mini has no audit/audit.json, the box
audit (prepare_daily.sh + run_audit.py) runs after publish as before.

set-short-url writes a public X short URL into edition.json video_url and
regenerates that date's edition page. The URL must be
https://x.com/signalnoisepub/status/<digits>; any query string, fragment, or
trailing /video/1 is stripped. Rerunning with the same URL is a no-op. A
local short.mp4 is not required. This is the post-publish step: the 7:20
edition may ship before Max posts the Neon short around 10 AM. With --mp4 PATH
it also copies the posted short, unchanged, into the edition as
daily-short.mp4 (hash in edition.json, poster frame when ffmpeg is present),
and the edition page and the listing lead with the playable short. It then
drops hosted shorts (mp4, poster and hash fields) of editions more than 30
days older than D, keeps their X links, and regenerates those pages.

set-audit-short-url hosts the audit short and/or records its public X URL,
then regenerates that date's audit page and edition page. At least one of
--url or --mp4 is required. The URL, when given, must be
https://x.com/signalnoisepub/status/<digits>; any query string, fragment, or
trailing /video/1 is stripped, and is written to edition.json audit_short_url.
When the field is set, the listing, edition page, and audit page each show
one "Watch on X" or "Audit short" link. When it is absent, those pages still
embed a hosted audit-short.mp4, with the caption "Audit short" and no X link.
Rerunning with the same URL and bytes is a no-op. --mp4 PATH works as for
set-short-url and hosts the audit short as audit-short.mp4. From 2026-11-27
the audit short is website-only, so the daily routine passes --mp4 and omits
--url.

set-headline writes an optional 4-10 word (max 14) teaser into edition.json
and regenerates the edition page, the Daily State listing, and the homepage
card when needed. Rerunning with the same headline is a no-op. The h1 stays
Daily State of AI - <date>. Use tools/draft_headline.py to generate the text
(it reuses a mirrored headline.txt when that file is present and valid)
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
from datetime import date as date_cls, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

import daily_state  # noqa: E402

RUN_KEYS = (
    "date", "status", "pipeline", "model", "reasoning_effort", "system_prompt",
    "editor", "qa", "edits_after_generation", "fallback", "prompts",
    "model_attempts", "words", "duration_seconds", "bundle_sha256", "script_sha256",
    "ethical_floor", "script_sha256_before_ethical_floor",
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
    if isinstance(run.get("ethical_floor"), dict) and (run.get("audit") or {}).get("file"):
        # Upstream audit (synthia-workspace ethical_floor.py): ran before TTS on the Mini.
        neon_run["audit"] = {"gate": False, "status": "ran before TTS (ethical floor check)"}
    else:
        neon_run["audit"] = {"gate": False, "status": "runs after publish"}
    for key in ("ethical_floor", "script_sha256_before_ethical_floor"):
        if neon_run.get(key) is None:
            neon_run.pop(key, None)
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
        headline_src = os.path.join(src, "headline.txt")
        if os.path.isfile(headline_src):
            shutil.copyfile(headline_src, os.path.join(dest, "headline.txt"))
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
    kit = args.kit or os.path.join(args.audit_out, "kit")
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


# Keep each committed short well under GitHub's 100 MB file limit (no LFS).
MAX_SHORT_BYTES = 50 * 1024 * 1024


def stage_hosted_short(dest, kind, mp4_path, edition):
    """Copy a posted short into the edition as daily-short.mp4 or audit-short.mp4.

    Records its sha256 in edition.json hashes and adds a poster frame when
    ffmpeg is available. The video bytes are copied as posted. Returns the
    paths this call created, for rollback.
    """
    item = next(entry for entry in daily_state.HOSTED_SHORTS if entry[0] == kind)
    _kind, mp4_name, poster_name, hash_key, _label = item
    if not os.path.isfile(mp4_path):
        raise daily_state.Hold(f"{kind} short mp4 is missing")
    size = os.path.getsize(mp4_path)
    if size > MAX_SHORT_BYTES:
        raise daily_state.Hold(f"{kind} short mp4 is {size} bytes, over {MAX_SHORT_BYTES}")
    digest = sha256_file(mp4_path)
    target = os.path.join(dest, mp4_name)
    created = []
    if os.path.exists(target):
        if sha256_file(target) != digest:
            raise daily_state.Hold(f"{mp4_name} is already published with different bytes")
    else:
        shutil.copyfile(mp4_path, target)
        created.append(target)
    edition["hashes"][hash_key] = digest
    poster = os.path.join(dest, poster_name)
    if not os.path.exists(poster) and shutil.which("ffmpeg"):
        import subprocess
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", target, "-frames:v", "1",
             "-vf", "scale=540:-2", "-q:v", "4", poster],
            capture_output=True,
        )
        if result.returncode == 0 and os.path.isfile(poster):
            created.append(poster)
        elif os.path.exists(poster):
            os.remove(poster)
    return created


def _remove_created(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


# Hosted shorts stay on the site for this many days; older days fall back to
# their X links (Synthia, 2026-11-25). Git history keeps the old files.
HOSTED_SHORT_DAYS = 30


def prune_hosted_shorts(newest):
    """Drop hosted shorts more than HOSTED_SHORT_DAYS older than newest.

    Removes the mp4 and poster files and their hash fields, keeps every X URL,
    and regenerates that day's edition page and audit page. A website-only
    audit short (no audit_short_url) leaves no X link after it is pruned.
    Returns the repo paths changed.
    """
    cutoff = date_cls.fromisoformat(newest).toordinal() - HOSTED_SHORT_DAYS
    root = daily_state.content_root(REPO)
    changed = []
    for iso in daily_state.list_edition_dates(REPO):
        if date_cls.fromisoformat(iso).toordinal() >= cutoff:
            continue
        directory = os.path.join(root, iso)
        names = [
            name for entry in daily_state.HOSTED_SHORTS for name in (entry[1], entry[2])
            if os.path.isfile(os.path.join(directory, name))
        ]
        if not names:
            continue
        edition_path = os.path.join(directory, "edition.json")
        previous = daily_state.read_stable(edition_path)
        edition = json.loads(previous.decode("utf-8"))
        for entry in daily_state.HOSTED_SHORTS:
            edition["hashes"].pop(entry[3], None)
        saved = {name: daily_state.read_stable(os.path.join(directory, name)) for name in names}
        for name in names:
            os.remove(os.path.join(directory, name))
        daily_state._write_text_atomic(
            edition_path, json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
        )
        try:
            loaded = daily_state.load_edition(REPO, iso)
        except daily_state.Hold:
            for name, data in saved.items():
                with open(os.path.join(directory, name), "wb") as handle:
                    handle.write(data)
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))
            raise
        page_rel = f"daily-state/{iso}/index.html"
        daily_state._write_text_atomic(os.path.join(REPO, page_rel), loaded["html"])
        rel_dir = os.path.relpath(directory, REPO).replace(os.sep, "/")
        changed += [f"{rel_dir}/{name}" for name in names]
        changed += [f"{rel_dir}/edition.json", page_rel]
        if loaded.get("audit_html"):
            audit_rel = f"daily-state/{iso}/audit/index.html"
            os.makedirs(os.path.dirname(os.path.join(REPO, audit_rel)), exist_ok=True)
            daily_state._write_text_atomic(os.path.join(REPO, audit_rel), loaded["audit_html"])
            changed.append(audit_rel)
    return changed


def refresh_listing_needed():
    path = os.path.join(REPO, daily_state.LISTING_REL)
    expected = daily_state.render_listing_html(daily_state.load_editions(REPO))
    if not os.path.isfile(path):
        return True
    with open(path, encoding="utf-8") as handle:
        return handle.read() != expected


def refresh_listing():
    """Rewrite the Daily State listing when its top shorts changed. Returns the rel path or None."""
    rel = daily_state.LISTING_REL
    path = os.path.join(REPO, rel)
    expected = daily_state.render_listing_html(daily_state.load_editions(REPO))
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as handle:
            if handle.read() == expected:
                return None
    daily_state._write_text_atomic(path, expected)
    return rel


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
    created = []
    try:
        if args.mp4:
            created = stage_hosted_short(dest, "daily", args.mp4, edition)
    except (OSError, daily_state.Hold) as exc:
        _remove_created(created)
        return fail(str(exc))
    edition["video_url"] = url
    text = json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
    already = text.encode("utf-8") == previous and not created

    def rollback():
        _remove_created(created)
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))

    if not already:
        daily_state._write_text_atomic(edition_path, text)
    try:
        loaded = daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        rollback()
        return fail(str(exc))
    html_text = loaded["html"]
    if f'href="{url}"' not in html_text:
        rollback()
        return fail("edition page is missing the Short link")
    current = None
    if os.path.isfile(page_path) and not os.path.islink(page_path):
        with open(page_path, encoding="utf-8") as handle:
            current = handle.read()
    wrote = []
    if current != html_text:
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        daily_state._write_text_atomic(page_path, html_text)
        wrote.append(page_rel)
    if args.mp4:
        wrote += prune_hosted_shorts(date)
    listing = refresh_listing()
    if listing:
        wrote.append(listing)
    if already and not wrote:
        print(json.dumps({"noop": True, "date": date, "video_url": url}))
        return 0
    wrote = [os.path.relpath(path, REPO) for path in created] + wrote
    print(json.dumps({"date": date, "video_url": url, "wrote": wrote}))
    return 0



def set_audit_short_url(args):
    date = args.date
    if not daily_state.is_real_date(date):
        return fail("date is invalid")
    url_arg = getattr(args, "url", None)
    mp4_arg = getattr(args, "mp4", None)
    if not url_arg and not mp4_arg:
        return fail("set-audit-short-url requires --url or --mp4")
    url = None
    if url_arg:
        try:
            url = normalize_short_x_url(url_arg)
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
    audit_rel = f"daily-state/{date}/audit/index.html"
    edition_rel = f"daily-state/{date}/index.html"
    audit_path = os.path.join(REPO, audit_rel)
    edition_page_path = os.path.join(REPO, edition_rel)
    previous = raw
    created = []
    try:
        if mp4_arg:
            created = stage_hosted_short(dest, "audit", mp4_arg, edition)
    except (OSError, daily_state.Hold) as exc:
        _remove_created(created)
        return fail(str(exc))
    if url:
        edition["audit_short_url"] = url
    text = json.dumps(edition, indent=2, ensure_ascii=False) + "\n"
    already = text.encode("utf-8") == previous and not created

    def rollback():
        _remove_created(created)
        if not already:
            daily_state._write_text_atomic(edition_path, previous.decode("utf-8"))

    if not already:
        daily_state._write_text_atomic(edition_path, text)
    try:
        loaded = daily_state.load_edition(REPO, date)
    except daily_state.Hold as exc:
        rollback()
        return fail(str(exc))
    audit_html = loaded["audit_html"]
    edition_html = loaded["html"]
    if url:
        if f'href="{url}"' not in audit_html:
            rollback()
            return fail("audit page is missing the audit short link")
        if f'href="{url}"' not in edition_html:
            rollback()
            return fail("edition page is missing the audit short link")
    else:
        if "audit-short.mp4" not in audit_html:
            rollback()
            return fail("audit page is missing the hosted audit short")
        if "audit-short.mp4" not in edition_html:
            rollback()
            return fail("edition page is missing the hosted audit short")

    def _current(path):
        if os.path.isfile(path) and not os.path.islink(path):
            with open(path, encoding="utf-8") as handle:
                return handle.read()
        return None

    current_audit = _current(audit_path)
    current_edition = _current(edition_page_path)
    pruned = prune_hosted_shorts(date) if args.mp4 else []
    listing_stale = refresh_listing_needed()
    if already and current_audit == audit_html and current_edition == edition_html and not listing_stale and not pruned:
        payload = {"noop": True, "date": date}
        if url:
            payload["audit_short_url"] = url
        print(json.dumps(payload))
        return 0
    wrote = [os.path.relpath(path, REPO) for path in created] + pruned
    if current_audit != audit_html:
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        daily_state._write_text_atomic(audit_path, audit_html)
        wrote.append(audit_rel)
    if current_edition != edition_html:
        os.makedirs(os.path.dirname(edition_page_path), exist_ok=True)
        daily_state._write_text_atomic(edition_page_path, edition_html)
        wrote.append(edition_rel)
    listing = refresh_listing()
    if listing:
        wrote.append(listing)
    payload = {"date": date, "wrote": wrote}
    if url:
        payload["audit_short_url"] = url
    print(json.dumps(payload))
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
    a.add_argument("--kit", default=None,
                   help="audit kit dir (default AUDIT_OUT/kit, the upstream Mini audit layout)")
    s = sub.add_parser("set-short-url")
    s.add_argument("--date", required=True)
    s.add_argument("--url", required=True)
    s.add_argument("--mp4", default=None)
    a_short = sub.add_parser("set-audit-short-url")
    a_short.add_argument("--date", required=True)
    a_short.add_argument("--url", default=None)
    a_short.add_argument("--mp4", default=None)
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
