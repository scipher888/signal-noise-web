"""Deterministic claim-check helpers. No network, no model calls.
A check module defines CLAIM (dict) and check(ctx) -> Result, and ends with `run_cli(CLAIM, check)`.
ctx gives source and artifact text; every helper returns the exact source sentence it relied on."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PASS, FAIL, NEEDS = 'PASS', 'FAIL', 'NEEDS-HUMAN'
WORDNUM = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen '
           'fifteen sixteen seventeen eighteen nineteen twenty'.split())}
WORDNUM.update({'thirty': 30, 'thirty-five': 35, 'fifty': 50})

def norm(t):
    t = t.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    t = re.sub('[\u2013\u2014\u2011]', '-', t).replace('\u00a0', ' ')
    return re.sub(r'[ \t]+', ' ', t)

def sentences(t):
    out = []
    for block in re.split(r'\n\s*\n|\n', norm(t)):
        out += [s.strip() for s in re.split(r'(?:(?<=[.!?])|(?<=[.!?]\[p\d\])|(?<=[.!?]\[p\d\d\]))\s+(?=[A-Z0-9@"*\u2022])', block) if s.strip()]
    return out

def resolve(p):
    """Artifact paths in artifacts.json are relative to the audit root (absolute paths still work)."""
    p = Path(p); return p if p.is_absolute() else (ROOT / p).resolve()

class Result(dict):
    pass

class Ctx:
    def __init__(self, date, artifact):
        self.date = date; self.artifact = artifact
        d = ROOT / 'checks' / date
        self.alias = json.load(open(d / 'sources.json'))
        self.index = json.load(open(ROOT / 'sources' / date / 'index.json'))['sources']
        arts = json.load(open(d / 'artifacts.json'))
        self.arts = {k: norm(resolve(v).read_text()) for k, v in arts.items()}
        self.used = []
    # ---- sources
    def key(self, alias): return self.alias.get(alias, alias)
    def src(self, alias):
        k = self.key(alias); f = ROOT / 'sources' / self.date / Path(self.index[k]['file']).name
        if not f.is_file():
            raise FileNotFoundError(f"source snapshot {f.name} is not present (published copies keep only URL + sha256 for third-party texts); "
                                    f"re-fetch {self.index[k]['url']} and compare sha256 {self.index[k]['sha256']}")
        return norm(f.read_text())
    def url(self, alias): return self.index[self.key(alias)]['url']
    def find(self, alias, pattern, flags=re.I):
        """First source sentence matching regex `pattern` (case-insensitive), or None."""
        for s in sentences(self.src(alias)):
            if re.search(pattern, s, flags): return s
        # fall back to a window match across line breaks (leaderboards, tables)
        m = re.search(pattern, re.sub(r'\s+', ' ', self.src(alias)), flags)
        return m.group(0) if m else None
    def absent(self, alias, pattern):
        return re.search(pattern, self.src(alias), re.I) is None
    # ---- artifact
    def art(self): return self.arts[self.artifact]
    def art_sentence(self, quote):
        q = norm(quote).lower()
        for s in sentences(self.art()):
            if q in s.lower(): return s
        return None
    def art_has(self, pattern): return re.search(pattern, self.art(), re.I) is not None
    # ---- results
    def _r(self, status, alias, quote, note):
        return Result(status=status, source=self.key(alias) if alias else None, url=self.url(alias) if alias else None,
                      source_quote=quote, note=note)
    def ok(self, alias, quote, note=''): return self._r(PASS, alias, quote, note)
    def fail(self, alias, quote, note): return self._r(FAIL, alias, quote, note)
    def need(self, alias, quote, note): return self._r(NEEDS, alias, quote, note)
    def require(self, alias, *patterns, note=''):
        """PASS if every pattern matches a source sentence; else NEEDS-HUMAN naming the missing one."""
        qs = []
        for p in patterns:
            s = self.find(alias, p)
            if not s: return self.need(alias, None, f'no source sentence matches /{p}/. ' + note)
            if s not in qs: qs.append(s)
        return self.ok(alias, ' … '.join(qs), note)
    def support_or_contradict(self, alias, support, contradict, note):
        """PASS if `support` matches; FAIL (quoting the contradicting sentence) if only `contradict` does."""
        s = self.find(alias, support)
        if s: return self.ok(alias, s)
        c = self.find(alias, contradict)
        if c: return self.fail(alias, c, note)
        return self.need(alias, None, 'neither support nor contradiction found. ' + note)

def run(module, date):
    claim, check = module.CLAIM, module.check
    ctx = Ctx(date, claim['artifact'])
    if claim.get('quote') and ctx.art_sentence(claim['quote']) is None:
        return Result(status='ERROR', note='claim quote not found verbatim in artifact', source=None, url=None, source_quote=None)
    r = check(ctx)
    r.setdefault('note', '')
    return r

def run_cli(claim, check):
    import importlib, types
    date = Path(sys.modules['__main__'].__file__).resolve().parent.name
    m = types.SimpleNamespace(CLAIM=claim, check=check)
    r = run(m, date)
    print(f"{r['status']}  [{claim['id']}] {claim.get('quote','')}")
    if r.get('source_quote'): print(f"  source ({r['source']}): \"{r['source_quote']}\"")
    if r.get('note'): print(f"  note: {r['note']}")
    sys.exit(0 if r['status'] in (PASS, NEEDS) else 1)
