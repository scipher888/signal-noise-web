#!/usr/bin/env python3
"""Stage a daily Gemini 4 Neon audit edition, then attach its executable audit.

    python3 tools/neon_edition.py build --date D --episode-dir DIR [--short MP4 --short-report JSON]
    python3 tools/neon_edition.py attach-audit --date D --audit-out DIR --kit DIR

build copies the frozen Neon run (script.txt, sources.json, episode.mp3 and
run.json from the Mac Mini mirror) into content/daily-state/D/ with
edition.json mode "audit" and "variant": null. Nothing is edited: the
script bytes are the model's reply. It refuses an existing directory, a run
that is not status ok on the neon pipeline, or a script whose hash does not
match the run. The audit page is a pending placeholder until attach-audit.

attach-audit copies the audit (audit.json, audit.md, the per-claim checks,
the helper library, the runner, and the source snapshots) into
content/daily-state/D/audit/. audit.json must be for D and for this script.
The audit is for transparency and never blocks or edits the edition.

Both commands validate with daily_state.py's loader before returning 0.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

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
    for name in ("script.txt", "sources.json", "episode.mp3"):
        if not os.path.isfile(os.path.join(src, name)):
            return fail(f"missing {name}")
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
        for name in ("script.txt", "sources.json", "episode.mp3"):
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
            "audio_url": daily_state.variant_asset_url(date, None, "episode.mp3"),
            "video_url": daily_state.variant_asset_url(date, None, "short.mp4") if has_short else None,
            "sources_url": daily_state.variant_asset_url(date, None, "sources.json"),
            "audit": dict(daily_state.ROOT_AUDIT_RECEIPT),
            "hashes": {
                "script_sha256": script_sha,
                "sources_sha256": sha256_file(os.path.join(dest, "sources.json")),
                "neon_run_sha256": hashlib.sha256(run_bytes).hexdigest(),
                "episode_sha256": sha256_file(os.path.join(dest, "episode.mp3")),
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--date", required=True)
    b.add_argument("--episode-dir", required=True)
    b.add_argument("--short", default=None)
    b.add_argument("--short-report", default=None)
    a = sub.add_parser("attach-audit")
    a.add_argument("--date", required=True)
    a.add_argument("--audit-out", required=True)
    a.add_argument("--kit", required=True)
    args = parser.parse_args(argv)
    return build(args) if args.cmd == "build" else attach_audit(args)


if __name__ == "__main__":
    sys.exit(main())
