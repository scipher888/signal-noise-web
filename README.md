# Signal & Noise — essay site

The web home of **Signal & Noise** (wave 3 of the beehiiv extrication, 2026-08-12).
Static HTML on GitHub Pages, in the publication's Night design system.

- Essay pages replicate the beehiiv `/p/<slug>` paths so every existing link keeps
  resolving after the `signalandnoise.email` CNAME cutover.
- **Fidelity by construction:** essay bodies are the as-published paste/final
  sources from the (private) editorial repo, wrapped by `build.py` — never retyped.
  `python3 build.py --check` verifies every page still contains its source body
  verbatim.
- Dates policy: exact dates only where an as-published byline or the publication
  record states one; month-year where the issue's origin page states it; bare
  "2026" otherwise. The beehiiv archive export upgrades the coarse ones.
- `/bio/` and `/subscribe/` are meta-refresh redirects to `/about/` (legacy
  beehiiv paths). `feed.xml` is the static RSS feed.

Publisher notes (the audit-snapshot repo's standing guards apply here too):
push → confirm the page is live (Pages takes ~a minute and briefly serves stale
HTML) → then place links; a rejected push is rebased, never force-pushed.

**CNAME cutover is deliberately not done at build time.** `BASE_URL` in
`build.py` flips to `https://www.signalandnoise.email` when DNS moves; adding
the CNAME file before DNS moves would redirect the github.io URL into the old
beehiiv site.
