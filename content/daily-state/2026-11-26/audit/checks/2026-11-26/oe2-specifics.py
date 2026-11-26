import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-specifics', 'artifact': 'episode', 'type': 'objection', 'story': 'Factoring rumor', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'declines to vouch for the specifics')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:not vouch|declin\w* to vouch|less confident about the exact|specifics can get mangled|uncertain about the specifics)') else ctx.fail('framing', q, 'Carry Aaronson’s reservation about specifics.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
