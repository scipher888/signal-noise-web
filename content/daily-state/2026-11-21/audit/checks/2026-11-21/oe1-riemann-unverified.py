import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-riemann-unverified', 'artifact': 'episode', 'type': 'objection', 'story': 'Riemann Hypothesis proof', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'no independent check of the Lean files')
    if ctx.art_has(r'(?:not (?:been )?independently verified|isn\'t verified|unverified|awaiting .*verification|not yet verified)'):
        return ctx.ok('framing', s, 'Episode carries unverified-proof caveat')
    return ctx.fail('framing', s, 'Episode omits caveat that the Lean proof has not been independently verified')


if __name__ == '__main__':
    run_cli(CLAIM, check)
