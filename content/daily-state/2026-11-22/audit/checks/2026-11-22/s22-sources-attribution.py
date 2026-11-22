import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's22-sources-attribution', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'Sources: METR, Lean Community and Nathan Lambert.'}


def check(ctx):
    q1 = ctx.find('metr', r'METR')
    q2 = ctx.find('lean', r'Lean community')
    q3 = ctx.find('lambert', r'Nathan Lambert')
    if q1 and q2 and q3:
        return ctx.ok('metr', q1, 'All three cited primary sources (METR, Lean Community, Nathan Lambert) are present')
    return ctx.need(None, None, 'One or more cited sources missing')


if __name__ == '__main__':
    run_cli(CLAIM, check)
