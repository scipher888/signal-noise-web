import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe4-blueprint-operator', 'artifact': 'episode', 'type': 'objection', 'story': 'Blueprint', 'quote': None}


def check(ctx):
    # Objection: leaderboard is run by the benchmark operator (named as source)
    s = ctx.find('framing', r'Benchmark operator.s own leaderboard')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"andon labs'? blueprint|andon labs|on blueprint-bench"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (leaderboard is run by the benchmark operator (named as source))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
