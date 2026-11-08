# Daily State written editions

Daily State of AI publishes one immutable page per edition at `/daily-state/YYYY-MM-DD/`. The 2026-11-08 page is `https://www.signalandnoise.email/daily-state/2026-11-08/`. These pages are the approved spoken script, its sources, and a plain link to the canonical Spotify episode. They are not Signal & Noise issues, and they are not added to the essay archive or `feed.xml`.

Merging generated HTML to the published branch is what makes a page public. This repository's GitHub Pages deployment follows that branch. The check workflow only reads the tree and runs tests. It does not deploy, and it does not grant deployment permissions.

## Frozen inputs

Each edition lives in `content/daily-state/YYYY-MM-DD/`:

- `script.txt` — the approved script, byte for byte
- `sources.json` — the source list and story groups, byte for byte
- `qa.json` — a public snapshot: date, status, semantic QA, source status and count, the six named gates, and the sha256 of the original `run.json`
- `edition.json` — title, canonical page URL, episode id and URL, the recorded public verification, and the content hashes

Do not commit `run.json`, model logs, recipient lists, credentials, or private paths. `qa.json` is written only after the full private receipt has been validated (`status` ok, `semantic_qa` pass, all six gates ok, sources ok). A pass is never invented in this repo.

The episode link must be `https://open.spotify.com/episode/` plus a 22-character id. A show URL, an `app.link` URL, a query string, or `spotify_episode_fallback: true` does not publish. The 2026-11-08 episode `4BrflfgytoeU5dAro96ig7` was verified at `2026-11-08T17:53Z` as `Daily State of AI - 2026-11-08`. CI rechecks that recorded evidence and the frozen hashes. It does not call Spotify.

## Commands

```bash
python3 daily_state.py                  # validate, then write HTML
python3 daily_state.py --check          # validate and compare; write nothing
python3 build.py --daily-state-only     # same writer, without rebuilding essays
python3 build.py --daily-state-check    # same check, without rebuilding essays
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`python3 build.py` and `python3 build.py --check` do not build Daily State. Essay pages, the archive, and the RSS feed keep their existing behavior.

## Fail closed

The writer validates every edition and stages output before it replaces any generated file. It writes nothing when any of these fail:

- the date is not a real `YYYY-MM-DD`, or the path escapes the edition directory
- the script, sources, or QA snapshot is missing, unreadable, empty, or not the expected shape
- dates or source counts disagree
- QA status is not `ok`, semantic QA is not `pass`, or any of the six gates (`length`, `clean`, `coverage`, `grounded`, `fresh`, `coherent`) is missing, duplicated, or not boolean `true`
- a source URL is not public HTTPS, or it carries credentials, a private address, or a `javascript:` / `data:` / `app.link` target
- the episode URL is missing, malformed, a show URL, or a fallback
- a frozen hash does not match the bytes, or a file changes while it is being read

On failure the command prints `HOLD:` and exits nonzero. An existing edition page and the listing stay as they were. A bad new date does not update the listing or any other edition. Nothing is recovered from already built HTML.

Publishing the same bytes again changes nothing. The same date with different bytes is a revision: it needs a new passing QA snapshot and an explicit `python3 daily_state.py --allow-correction`. That flag does not skip validation. The check workflow never passes it.

## After merge

Wait until GitHub Pages has finished the merged commit, then open the canonical URL and confirm the title, date, script, four source links, Spotify href, and stylesheet. Only then is the page live. The page check does not prove how a phone opens Spotify.
