# Daily State written editions

Daily State of AI publishes one immutable page per edition at `/daily-state/YYYY-MM-DD/`. The 2026-11-08 page is `https://www.signalandnoise.email/daily-state/2026-11-08/`. These pages are the approved spoken script, its sources, and a plain link to the canonical Spotify episode. They are not Signal & Noise issues, and they are not added to the essay archive or `feed.xml`.

The site header and both footers link to `/daily-state/`. The homepage has a card for the latest parent edition (never a Neon raw variant): the date, a short lede, links to the edition, Spotify, and Audit when that page exists, and "All editions →". The `/daily-state/` listing is grouped by month, newest first.

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

`python3 build.py` still does not build Daily State edition pages. It does write the homepage through `build.render_home()`, using the Daily State card from `daily_state.render_home_teaser()` so the two cannot drift. `python3 build.py --check` stays an essay fidelity check. `python3 daily_state.py --check` also verifies the homepage teaser in a separate step; `index.html` is not part of `list_output_files()`. Essay pages, the essay archive list, and the RSS feed keep their existing behavior.

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

Generated files. The shared listing stays `daily-state/index.html`, grouped by month. A new date may also refresh the homepage teaser in `index.html` the same way it refreshes the listing. That homepage write is a separate step, not a `list_output_files()` entry.

- live: `daily-state/YYYY-MM-DD/index.html`
- editor: that page, plus `daily-state/YYYY-MM-DD/editors-notes/index.html`

The edition page links `Editor's notes` in the same line as the AI-generated label. The notes page groups outstanding items under `Episode`, `Short`, and `Written edition`. Each item shows its summary, one-line reason, and status in plain words: `Unresolved` or `Partly resolved`. An empty list says `No outstanding issues`. Overruled objections are not listed.

### Offline package command

No network. `--check-links` is the only form that fetches source URLs (HEAD, then GET, browser user agent, one retry on 5xx).

```bash
python3 daily_state.py --package DIR --check
python3 daily_state.py --package DIR --out OUT
```

`DIR` is either a frozen edition directory or a pipeline directory containing `script.txt`, `sources.json`, `run.json`, and `editor_notes.json`. Other pipeline files are ignored and are not copied into the page. `OUT` receives `daily-state/YYYY-MM-DD/index.html`, `daily-state/YYYY-MM-DD/sources/index.html`, and, in editor mode, `daily-state/YYYY-MM-DD/editors-notes/index.html`. An audit variant directory is checked the same way, offline, and writes the audit-mode pages below, including `sources/`.

## Audit mode

This path is off unless a variant directory opts in. The live page at `daily-state/YYYY-MM-DD/` and, when that date is an editor edition, its editor's notes stay on the checks above. A variant is a subfolder of that date. The only one today is `neon/`. `list_edition_dates()` treats that subfolder as a known edition input, not as a stray directory and not as a second date. `load_edition_directory()` loads it when the directory is the variant, and leaves it out of the parent allowlist so the parent still publishes from its frozen files alone.

Opt in with `edition.json` `"mode": "audit"`. The receipt is the audit counts and the sha256 of `audit/audit.json`:

```json
{
  "mode": "audit",
  "variant": "neon",
  "audit": {
    "sha256": "<sha256 of audit/audit.json>",
    "gate": false,
    "episode": {"PASS": 42, "FAIL": 7, "NEEDS-HUMAN": 8, "ERROR": 0},
    "short": {"PASS": 14, "FAIL": 5, "NEEDS-HUMAN": 3, "ERROR": 0}
  }
}
```

`gate` is false. There is no `qa.json`, no editor receipt, and no `semantic_qa`. A pass is not invented here. The audit is published with its failures. It is for transparency and is not a gate.

`sources.json` in this mode may include `reference_snapshot` and a `verification_status` on each story. Those fields stay in the frozen file, so its hash does not change. Live and editor editions still reject both keys.

The variant directory holds `script.txt`, `sources.json`, `edition.json`, `neon_run.json`, `episode.mp3`, `short.mp4`, and `audit/`. The page quotes the episode prompt from `neon_run.json` verbatim. It says the script was written by Google Gemini 4 Neon (medium) from that one prompt, with no rules, editor or edits, published as produced. It embeds `<audio controls>` for `/content/daily-state/YYYY-MM-DD/neon/episode.mp3`, links the short MP4, and uses its own canonical URL and `og:url`. Spotify is not required. Primary artifact links (the short, when one shipped) sit on one line. Audit sits on a quieter second line, pointing at the audit page, with Audit short when `audit_short_url` is set. A readable Sources page stays at `/daily-state/YYYY-MM-DD/neon/sources/` (the raw `sources.json` stays published, with a Raw data link on that page), and the edition lists its sources at the bottom of the essay rather than in the top links. The disclaimer `AI-generated · may contain errors` appears once as a small line directly under that link group. The h1 for this edition is `Daily State of AI - 2026-11-20 (Gemini 4 Neon, raw)`.

The audit page uses the site stylesheet and is built from `audit.json`. After a line that each claim is a small Python check run against the source texts and that the audit is not a gate, the counts sit in a `Check results` callout that matches the edition Minimal prompt block (episode 42 PASS / 7 FAIL / 8 NEEDS-HUMAN, short 14 PASS / 5 FAIL / 3 NEEDS-HUMAN). FAIL items are open. PASS and NEEDS-HUMAN items are collapsed in `<details>`. Each item shows the claim, the result, the source quote, and a link to its check script in the repo.

Generated files. The shared listing stays `daily-state/index.html`, grouped by month. The existing row for the date stays, and the variant is an added row under that date. The homepage teaser still uses the parent edition, not the variant.

- `daily-state/YYYY-MM-DD/neon/index.html`
- `daily-state/YYYY-MM-DD/neon/audit/index.html`
- `daily-state/YYYY-MM-DD/neon/sources/index.html`

The 2026-11-20 neon edition is that raw page. Its sibling at `/daily-state/2026-11-20/` is the editor edition and is a different page.

`python3 daily_state.py --check` covers the variant with the other editions. `--pipeline live` and `--pipeline editor` do not load it.

## Fail closed

The writer validates every edition and stages output before it replaces any generated file. It writes nothing when any of these fail:

- the date is not a real `YYYY-MM-DD`, or the path escapes the edition directory
- the script, sources, or QA snapshot is missing, unreadable, empty, or not the expected shape
- dates or source counts disagree
- QA status is not `ok`, semantic QA is not `pass`, or any of the six gates (`length`, `clean`, `coverage`, `grounded`, `fresh`, `coherent`) is missing, duplicated, or not boolean `true`
- a source URL is not public HTTPS, or it carries credentials, a private address, or a `javascript:` / `data:` / `app.link` target
- the episode URL is missing, malformed, a show URL, or a fallback
- a frozen hash does not match the bytes, or a file changes while it is being read

On failure the command prints `HOLD:` and exits nonzero. An existing edition page, the listing, and the homepage teaser stay as they were. A bad new date does not update the listing, the homepage teaser, or any other edition. Nothing is recovered from already built HTML.

Publishing the same bytes again changes nothing. The same date with different bytes is a revision: it needs a new passing QA snapshot and an explicit `python3 daily_state.py --allow-correction`. That flag does not skip validation. The check workflow never passes it.

## After merge

Wait until GitHub Pages has finished the merged commit, then open the canonical URL and confirm the title, date, script, four source links, Spotify href, and stylesheet. Confirm the homepage card shows that date, with working edition, Spotify, and Audit links when the audit exists. Only then is the page live. The page check does not prove how a phone opens Spotify.

A daily publish PR may include `content/daily-state/YYYY-MM-DD/`, that date's generated pages, `daily-state/index.html`, and `index.html` (the teaser). It must not include earlier edition pages, the essay archive list, or `feed.xml`.

## Daily Gemini 4 Neon editions (from 2026-11-21)

Joel approved on 2026-11-20 that the daily edition itself is the raw Gemini 4 Neon minimal-prompt edition. Neon writes it, it is published as produced, and nothing is edited. `content/daily-state/YYYY-MM-DD/` then holds `edition.json` (mode `"audit"`, `"variant": null`), `script.txt`, `sources.json`, `neon_run.json`, and `short.mp4` when the short shipped. It holds no `qa.json` and no editor receipt.

Audio (from 2026-11-22, Synthia 2026-11-21): the page links the canonical Spotify episode as `<p><a href="https://open.spotify.com/episode/ID">Audio on Spotify</a></p>`, the same as the pre-audit editions, and no `episode.mp3` is published. `edition.json` carries `episode_id`, `episode_url`, `verified_at` and the recorded `verification` (method `public_episode_and_show`), with `audio_url: null` and `hashes.episode_sha256: null`. The build reads the URL from `--episode-url`, else `spotify_episode_url` in the mirror's `takeaways.json`, else `spotify_episode_url`/`episode_url` in `run.json`, checks the public episode and show pages for the exact title `Daily State of AI - YYYY-MM-DD` (or reads `--verification FILE`), and refuses to stage on a missing, malformed or unverified episode. `verified_at` is UTC and must fall on the edition date. `daily_state.py --check` holds an edition after 2026-11-21 with no Spotify episode, or with a self-hosted `episode.mp3`. Only 2026-11-21 keeps the self-hosted player it was published with.

The page stacks primary artifact links on one line (`Audio on Spotify`, plus `Short` when a short shipped) and audit links on a second line in the same style (`Audit`, plus `Audit short` when `audit_short_url` is set). There is no top Sources link: the essay lists its sources at the bottom, and a readable Sources page remains at `/daily-state/YYYY-MM-DD/sources/`, built from `sources.json`. The raw JSON file stays at `/content/daily-state/YYYY-MM-DD/sources.json`. `Audit` points at `/daily-state/YYYY-MM-DD/audit/`. The audit page follows the same link style: after the sentence explaining the Python checks, the per-artifact counts sit in a `Check results` callout that reuses the edition's Minimal prompt block (`figure.ds-prompt`, with each artifact on its own line in the inner box). Then a `Daily State of AI` link back to the edition, then `Audit short` when `audit_short_url` is set, then the house label. If an artifact in the audit has no checks, that artifact gets no summary line, and the callout is omitted when every artifact is empty. The label `AI-generated · may contain errors` appears once on the edition page, as small text directly under the link group, and once on the audit page under those links.

1. Stage it from the Mini mirror. This refuses a run that is not `status: ok` on the `neon` pipeline, or a script whose hash differs from the run's:

   ```bash
   python3 tools/neon_edition.py build --date D --episode-dir /workspace/daily-state-slim/out/D \
     --short /workspace/dsoai-shorts/D/short-*.mp4 --short-report /workspace/dsoai-shorts/D/report.json
   # Spotify URL: takeaways.json spotify_episode_url (or --episode-url URL); verified live, recorded in edition.json
   python3 daily_state.py && python3 daily_state.py --check
   ```

2. The executable audit runs after publishing, for transparency only. It never blocks or edits the edition. Until it is attached, `/audit/` is a pending placeholder, and that placeholder is the only edition page that may be replaced later. Attach the audit in a follow-up PR:

   ```bash
   python3 tools/neon_edition.py attach-audit --date D --audit-out AUDIT_OUT --kit AUDIT_KIT
   python3 daily_state.py && python3 daily_state.py --check
   ```

   `audit.json` must be for D, and its episode hash must match `script.txt`. An audit of the episode alone, with no short that day, is valid.

3. After Max posts the Neon short (around 10 AM PT), point **Short** at the public X status URL. A local `short.mp4` is not required. The command accepts only `https://x.com/signalnoisepub/status/<digits>` and strips any query string, fragment, or trailing `/video/1`. Rerunning with the same URL is a no-op. Then check:

   ```bash
   python3 tools/neon_edition.py set-short-url --date D --url https://x.com/signalnoisepub/status/ID
   python3 daily_state.py --check
   ```

4. After the audit short is posted on X as a reply in that day's short thread, point the audit page at that public X status URL. This writes `audit_short_url` in `edition.json` and regenerates only `/daily-state/D/audit/` (the edition page is unchanged). The same URL shape and normalization rules as `set-short-url` apply. When the field is absent, the audit page has no short link. Then check:

   ```bash
   python3 tools/neon_edition.py set-audit-short-url --date D --url https://x.com/signalnoisepub/status/ID
   python3 daily_state.py --check
   ```

5. After the edition is staged, add a 4-10 word `headline` in `edition.json`. It is labelling metadata only: it never edits the script. The listing and homepage card use it as the link text, with the date beside it; the edition page keeps `h1` as `Daily State of AI - D` and shows the headline as a subtitle. Generate it from the episode script at 7:20 (the Neon short usually is not ready yet, and short captions are often format copy rather than the insight):

   ```bash
   python3 tools/draft_headline.py --date D --out /tmp/ds-headline-D.txt
   python3 tools/neon_edition.py set-headline --date D --headline "$(cat /tmp/ds-headline-D.txt)"
   python3 daily_state.py --check
   ```
