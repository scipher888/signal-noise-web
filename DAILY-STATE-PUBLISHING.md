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

## Experimental editor mode

This path is off unless an edition opts in. Existing editions and the live daily flow use the checks above. Opt in with any one of:

- `run.json` `"pipeline": "editor"`
- `run.json` editor object
- `edition.json` `"pipeline": "editor"` (with the editor receipt and `hard_stops`)
- `--pipeline editor` on the package command

`--pipeline live` forces the current rules. Omit the flag and the file is what decides.

Editor mode passes when `editor.completed` is true and `hard_stops` is empty. Advisory QA gates (`ok: true`, `advisory: true`, `findings`) do not hold. These do:

- a recorded hard stop, or one found while checking the package
- a missing or broken audio reference, or a missing or broken video reference when a video is named
- a source link that is actually dead: DNS or connection failure, 404, 410, or a 5xx that is still a 5xx after one retry. 401, 403, 405, 429, and bot-block pages are not dead. `https://openai.com/index/step-toward-defining-the-standard-model` returns 403 to scripts and still passes
- the label `AI-generated · may contain errors` appearing any number of times other than once on the edition page

Hash, file scope, `h1`, `og:url`, and the Spotify episode href still hold.

`run.json` in editor mode keeps `semantic_qa: "pass"` and adds:

```json
{
  "pipeline": "editor",
  "editor": {
    "model": "meta/muse-ember",
    "reasoning_effort": "max",
    "decisions": {
      "overruled": 1,
      "accepted_resolved": 2,
      "accepted_unresolved": 1,
      "accepted_partial": 0,
      "total": 4
    },
    "completed": true,
    "outstanding": 1
  },
  "hard_stops": []
}
```

That decisions object is the canonical receipt. `outstanding` counts `accepted_unresolved` plus `accepted_partial`. `completed: false` holds. The older counts `accepted`, `overruled`, and `partially` — flat on `editor`, or under `editor.decisions` with `total` — still pass. `hard_stops` items are `{"kind": "audio"|"video"|"dead_link"|"label", "detail": "..."}`. A non-empty list holds even when `completed` is true.

`editor_notes.json` sits next to `script.txt`, `sources.json`, and `run.json` in a pipeline package. Only the outstanding items are public:

```json
{
  "date": "YYYY-MM-DD",
  "outstanding": [
    {
      "artifact": "episode",
      "summary": "One sentence.",
      "reason": "One line.",
      "status": "accepted_unresolved"
    }
  ],
  "generated_by": {"model": "meta/muse-ember"}
}
```

`artifact` is `episode`, `short`, or `written`. `status` is `accepted_unresolved` or `accepted_partial`. Overruled objections are not a status and are not rendered.

### File scope

Live edition directory, unchanged:

- `content/daily-state/YYYY-MM-DD/script.txt`
- `content/daily-state/YYYY-MM-DD/sources.json`
- `content/daily-state/YYYY-MM-DD/qa.json`
- `content/daily-state/YYYY-MM-DD/edition.json`

Editor edition directory. `run.json` is still not committed. `edition.json` adds `pipeline`, `editor`, `hard_stops`, and `hashes.editor_notes_sha256`:

- the four files above
- `content/daily-state/YYYY-MM-DD/editor_notes.json`

Generated files. The shared listing stays `daily-state/index.html`.

- live: `daily-state/YYYY-MM-DD/index.html`
- editor: that page, plus `daily-state/YYYY-MM-DD/editors-notes/index.html`

The edition page links `Editor's notes` in the same line as the AI-generated label. The notes page groups outstanding items under `Episode`, `Short`, and `Written edition`. Each item shows its summary, one-line reason, and status in plain words: `Unresolved` or `Partly resolved`. An empty list says `No outstanding issues`. Overruled objections are not listed.

### Offline package command

No network. `--check-links` is the only form that fetches source URLs (HEAD, then GET, browser user agent, one retry on 5xx).

```bash
python3 daily_state.py --package DIR --check
python3 daily_state.py --package DIR --out OUT
```

`DIR` is either a frozen edition directory or a pipeline directory containing `script.txt`, `sources.json`, `run.json`, and `editor_notes.json`. Other pipeline files are ignored and are not copied into the page. `OUT` receives `daily-state/YYYY-MM-DD/index.html` and, in editor mode, `daily-state/YYYY-MM-DD/editors-notes/index.html`.

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
