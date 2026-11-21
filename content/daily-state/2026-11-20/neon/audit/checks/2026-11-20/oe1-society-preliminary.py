import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-society-preliminary', 'artifact': 'episode', 'type': 'objection', 'story': 'Society', 'quote': None}


def check(ctx):
    # Objection: Society paper is an exploratory preprint, not yet peer reviewed or replicated
    s = ctx.find('framing', r'not yet peer reviewed')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"not (yet )?(been )?peer[- ]reviewed|not yet reviewed|unreviewed|preliminary|exploratory|hasn'?t been (peer[- ])?reviewed|early,? author[- ]reported"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Society paper is an exploratory preprint, not yet peer reviewed or replicated)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
