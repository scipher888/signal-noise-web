import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-cset-data-lag-caveat', 'artifact': 'episode', 'type': 'objection', 'story': 'CSET Cyber Report', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'interpretive, and its authors note data may lag')
    if not ctx.art_has(r'(?:lag|lagging|too early|hypothesis|interpretive|may not hold)'):
        return ctx.fail('framing', s, 'Episode omits caveat that CSET attack-impact analysis is interpretive and data may lag')
    return ctx.ok('framing', s, 'Episode notes that CSET attack-impact data may lag')


if __name__ == '__main__':
    run_cli(CLAIM, check)
