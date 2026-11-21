#!/usr/bin/env python3
"""Executable audit runner. Runs every checks/<DATE>/*.py claim check against the source snapshot
(sources/<DATE>/, built by build_sources.py) and writes audit.json, audit.md and audit.html.
Each check is deterministic code; nothing here calls a model or the network.
Usage: run_audit.py DATE [--out DIR] [--artifacts artifacts.json]
  --artifacts lets you point the same checks at other versions of the artifacts."""
import argparse, hashlib, html, importlib.util, json, shutil, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H / 'lib'))
import auditlib
ap = argparse.ArgumentParser(); ap.add_argument('date'); ap.add_argument('--out', default=None); ap.add_argument('--artifacts', default=None)
a = ap.parse_args(); CK = H / 'checks' / a.date; OUT = Path(a.out or H / 'out' / a.date); OUT.mkdir(parents=True, exist_ok=True)
if a.artifacts: shutil.copyfile(a.artifacts, CK / 'artifacts.json')
arts = json.load(open(CK / 'artifacts.json')); idx = json.load(open(H / 'sources' / a.date / 'index.json'))['sources']
rows = []
for f in sorted(CK.glob('[!_]*.py')):
    spec = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    try: r = auditlib.run(m, a.date)
    except Exception as e: r = {'status': 'ERROR', 'note': f'{type(e).__name__}: {e}', 'source': None, 'url': None, 'source_quote': None}
    ctx = auditlib.Ctx(a.date, m.CLAIM['artifact'])
    code = f.read_text(); body = code[code.index('def check'):code.index("if __name__")].rstrip()
    rows.append({**m.CLAIM, **r, 'artifact_sentence': ctx.art_sentence(m.CLAIM['quote']) if m.CLAIM.get('quote') else None,
                 'check_file': str(f.relative_to(H)), 'check_code': body})
order = {'FAIL': 0, 'ERROR': 0, 'NEEDS-HUMAN': 1, 'PASS': 2}
summary = {}
for r in rows:
    s = summary.setdefault(r['artifact'], {'PASS': 0, 'FAIL': 0, 'NEEDS-HUMAN': 0, 'ERROR': 0}); s[r['status']] += 1
meta = {'date': a.date, 'generated_at': time.strftime('%Y-%m-%d %H:%M %Z'), 'artifacts': {k: {'path': v if not Path(v).is_absolute() else Path(v).name, 'sha256': hashlib.sha256(auditlib.resolve(v).read_bytes()).hexdigest()} for k, v in arts.items()},
        'sources': idx, 'summary': summary, 'method': 'Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. '
        'PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.'}
json.dump({'meta': meta, 'results': rows}, open(OUT / 'audit.json', 'w'), indent=1, ensure_ascii=False)
# ---- markdown
md = [f"# Executable audit, Daily State of AI {a.date}", '', meta['method'], '', '| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |', '|---|---|---|---|---|']
md += [f"| {k} | {v['PASS']} | {v['FAIL']} | {v['NEEDS-HUMAN']} | {v['ERROR']} |" for k, v in summary.items()]
md += ['', '## Sources'] + [f"- `{k}`: [{v['title']}]({v['url']}) (sha256 {v['sha256'][:12]}…)" for k, v in idx.items()]
for art in arts:
    md += ['', f'## {art}']
    for r in sorted([r for r in rows if r['artifact'] == art], key=lambda r: (order[r['status']], r['id'])):
        md += ['', f"### {r['status']} · {r['id']} ({r['type']}, {r['story']})"]
        if r.get('quote'): md += [f"> Claim: {r['quote']}"]
        if r.get('source_quote'): md += ['', f"Source ([{r['source']}]({r['url']})): \"{r['source_quote']}\""]
        if r.get('note'): md += ['', f"Note: {r['note']}"]
        md += ['', '```python', r['check_code'], '```']
(OUT / 'audit.md').write_text('\n'.join(md) + '\n')
# ---- html
e = html.escape; col = {'PASS': '#1f7a3a', 'FAIL': '#b3261e', 'NEEDS-HUMAN': '#8a6100', 'ERROR': '#b3261e'}
h = [f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Executable audit · Daily State of AI · {a.date}</title>",
     "<style>body{font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#1b1b1f}"
     "details{border:1px solid #ddd;border-radius:8px;margin:.5rem 0;padding:.5rem .8rem}summary{cursor:pointer}"
     ".b{display:inline-block;color:#fff;border-radius:4px;padding:0 .4rem;font-weight:600;font-size:12px;margin-right:.4rem}"
     "pre{background:#f5f5f7;padding:.6rem;overflow:auto;font-size:12.5px}blockquote{margin:.4rem 0;padding-left:.8rem;border-left:3px solid #ccc;color:#444}"
     "table{border-collapse:collapse}td,th{border:1px solid #ddd;padding:.2rem .6rem}</style>",
     f"<h1>Executable audit · Daily State of AI · {a.date}</h1><p>{e(meta['method'])} The audit is for transparency, not a gate: the artifacts are published as the model wrote them. FAIL items are expanded; PASS and NEEDS-HUMAN items are collapsed (click to open).</p>",
     '<table><tr><th>artifact</th><th>PASS</th><th>FAIL</th><th>NEEDS-HUMAN</th></tr>' + ''.join(f"<tr><td>{k}</td><td>{v['PASS']}</td><td>{v['FAIL']}</td><td>{v['NEEDS-HUMAN']}</td></tr>" for k, v in summary.items()) + '</table>',
     '<h2>Sources</h2><ul>' + ''.join(f"<li><a href='{e(v['url'])}'>{e(v['title'])}</a> <code>{k}</code></li>" for k, v in idx.items()) + '</ul>']
for art in arts:
    h.append(f'<h2>{e(art)}</h2>')
    for r in sorted([r for r in rows if r['artifact'] == art], key=lambda r: (order[r['status']], r['id'])):
        h.append(f"<details{' open' if r['status'] in ('FAIL', 'ERROR') else ''}><summary><span class=b style='background:{col[r['status']]}'>{r['status']}</span>"
                 f"{e(r.get('quote') or r['id'])} <small>({e(r['type'])} · {e(r['story'])})</small></summary>")
        if r.get('source_quote'): h.append(f"<blockquote>{e(r['source_quote'])}<br><small>source: <a href='{e(r['url'])}'>{e(r['source'])}</a></small></blockquote>")
        if r.get('note'): h.append(f"<p><b>Note:</b> {e(r['note'])}</p>")
        h.append(f"<pre>{e(r['check_code'])}</pre></details>")
(OUT / 'audit.html').write_text('\n'.join(h) + '\n')
print(json.dumps(summary)); print('wrote', OUT / 'audit.json', OUT / 'audit.html', OUT / 'audit.md')
sys.exit(0)
