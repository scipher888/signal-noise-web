#!/usr/bin/env python3
"""Draft a 4-10 word Daily State headline from the episode script.

Uses the box OpenRouter helper (Ember, then Terra, then GPT-6.1 Sol).
Prints compact JSON and writes the cleaned headline to --out.

    python3 tools/draft_headline.py --date D --out FILE
    python3 tools/draft_headline.py --date D --script PATH --out FILE
    python3 tools/neon_edition.py set-headline --date D --headline "$(cat FILE)"
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

import daily_state  # noqa: E402

OR_CALL = os.environ.get(
    "OR_CALL",
    "/workspace/tools/or-offload/or-call",
)
PROMPT = (
    "Write a 4-10 word headline for this Daily State of AI episode that "
    "captures its central insight. Plain text, no quotes."
)
BOT = "J - Sam"


def script_path(date, variant, explicit):
    if explicit:
        return explicit
    root = daily_state.content_root(REPO)
    if variant:
        return os.path.join(root, date, variant, "script.txt")
    return os.path.join(root, date, "script.txt")


def clean_reply(text):
    line = text.strip().splitlines()[0].strip() if text.strip() else ""
    return daily_state.validate_headline(line)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--script", default=None)
    parser.add_argument("--variant", default=None)
    parser.add_argument("--bot", default=BOT)
    args = parser.parse_args(argv)
    if not daily_state.is_real_date(args.date):
        print("HOLD: date is invalid", file=sys.stderr)
        return 1
    variant = args.variant or None
    path = script_path(args.date, variant, args.script)
    if not os.path.isfile(path):
        print("HOLD: missing script.txt", file=sys.stderr)
        return 1
    if not os.path.isfile(OR_CALL):
        print(f"HOLD: or-call is missing at {OR_CALL}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [
            OR_CALL,
            "--bot", args.bot,
            "--task-type", "draft",
            "--context-file", path,
            "--out", args.out + ".raw",
        ],
        input=PROMPT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or "HOLD: or-call failed\n")
        return 1
    try:
        meta = json.loads(result.stdout)
    except ValueError:
        print("HOLD: or-call did not return JSON", file=sys.stderr)
        return 1
    raw_path = args.out + ".raw"
    try:
        with open(raw_path, encoding="utf-8") as handle:
            raw = handle.read()
        headline = clean_reply(raw)
    except (OSError, daily_state.Hold) as exc:
        print(f"HOLD: {exc}", file=sys.stderr)
        return 1
    daily_state._write_text_atomic(args.out, headline + "\n")
    meta["headline"] = headline
    meta["out"] = args.out
    print(json.dumps(meta, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
