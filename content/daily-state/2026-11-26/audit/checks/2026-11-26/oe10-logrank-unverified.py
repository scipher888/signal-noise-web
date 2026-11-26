import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe10-logrank-unverified', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'tiny improvement.*not independently verified')
    p = r'(?:log.rank[^.!?]{0,220}(?:not (?:yet )?(?:been )?independently verified|no independent verification|unverified)|(?:not independently verified|unverified)[^.!?]{0,180}log.rank)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State independent verification is lacking for log-rank.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
