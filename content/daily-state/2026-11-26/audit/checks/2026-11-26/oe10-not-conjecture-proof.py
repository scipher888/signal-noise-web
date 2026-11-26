import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe10-not-conjecture-proof', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'not a proof of the conjecture')
    return ctx.ok('framing', q) if ctx.art_has(r'not (?:a proof of|prove|solve) the (?:log[- ]rank )?conjecture|log[- ]rank conjecture remains open') else ctx.fail('framing', q, 'The improvement does not prove the conjecture.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
