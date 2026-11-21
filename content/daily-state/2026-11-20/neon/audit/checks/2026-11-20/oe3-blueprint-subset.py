import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-blueprint-subset', 'artifact': 'episode', 'type': 'objection', 'story': 'Blueprint', 'quote': None}


def check(ctx):
    # Objection: human baseline covers only 12 of 50 apartments
    s = ctx.find('framing', r'human baseline covers only 12 of the 50 apartments')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r'(12|twelve) apartments'): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (human baseline covers only 12 of 50 apartments)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
